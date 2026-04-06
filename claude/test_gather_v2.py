"""
Gather Test v2 - Two modes:
  Mode A: Simple (no 0x0023 AUTH) - should get 0x00B8 like old bot
  Mode B: PCAP mode with ENABLE_VIEW(0) between view and troops

Goal: reproduce 0x00B8, then figure out what's needed for 0x0071.
"""
import sys, time, struct, subprocess, random
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from game_server import GameConnection
from codec import CMsgCodec
from packets import build_packet
from protocol import opname, OP_ENABLE_VIEW, OP_START_MARCH

KINGDOM = 182
MARCH_TYPE = 0x1749
TURF_X, TURF_Y = 653, 567

# Formation troop type IDs (from successful PCAP)
FORMATION_TROOPS = [1046, 3002, 1035, 2008, 2019, 1009, 1024, 1016, 2009, 1025]
TROOP_IDS = [403, 405, 407, 411]  # 4 troops (NOT 5)

def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def node_login(email, password, igg_id):
    result = subprocess.run(
        ['node', r'D:\CascadeProjects\lords_bot\http_login.mjs', email, password, str(igg_id)],
        capture_output=True, text=True, timeout=30
    )
    return result.stdout.strip() if len(result.stdout.strip()) == 32 else None

# ──── PACKET BUILDERS ────

def build_enable_view(codec, igg_id, view_type=0x01):
    data = bytearray(10)
    data[0] = view_type
    struct.pack_into('<I', data, 1, igg_id)
    data[9] = 0x01
    return codec.encode(OP_ENABLE_VIEW, bytes(data))

def build_tile_select(x, y):
    return build_packet(0x006E, struct.pack('<HHB', x, y, 0x01))

def build_troop_select(troop_id):
    return build_packet(0x099D, struct.pack('<I', troop_id))

def build_formation():
    data = struct.pack('<H', len(FORMATION_TROOPS))
    for tid in FORMATION_TROOPS:
        data += struct.pack('<I', tid)
    return build_packet(0x0834, data)

def build_gather_0ce8(codec, tile_x, tile_y, hero_id=255, march_slot=1):
    data = bytearray(46)
    data[0] = march_slot & 0xFF
    data[1] = random.randint(0, 255)
    data[2] = random.randint(0, 255)
    data[3] = random.randint(0, 255)
    struct.pack_into('<H', data, 4, MARCH_TYPE)
    struct.pack_into('<H', data, 9, tile_x)
    struct.pack_into('<H', data, 11, tile_y)
    data[13] = 0x01
    data[14] = hero_id & 0xFF
    data[18] = KINGDOM & 0xFF
    data[22] = 0x04
    struct.pack_into('<I', data, 33, IGG_ID)
    log(f"  0x0CE8 plaintext ({len(data)}B): {data.hex()}")
    return codec.encode(OP_START_MARCH, bytes(data))

# ──── RESPONSE TRACKING ────

responses = []
def on_packet(opcode, payload):
    responses.append((opcode, payload))

def collect(label, timeout=3):
    time.sleep(timeout)
    found = []
    while responses:
        op, pl = responses.pop(0)
        if op not in (0x0042, 0x036C, 0x0002):
            found.append((op, pl))
    if found:
        log(f"  [{label}] {len(found)} responses:")
        for op, pl in found:
            prefix = pl[:20].hex() if pl else ""
            log(f"    <- 0x{op:04X} {opname(op)} ({len(pl)}B) {prefix}")
    else:
        log(f"  [{label}] no responses")
    return found

def search_resource(gc):
    """Send 0x033E to find food tile."""
    # Format from PCAP: [level, 0x04, 0x00, 0x03]
    gc.send(build_packet(0x033E, bytes([0x01, 0x04, 0x00, 0x03])))
    time.sleep(3)
    tiles = []
    while responses:
        op, pl = responses.pop(0)
        if op == 0x033F and len(pl) >= 5:
            tx = struct.unpack('<H', pl[1:3])[0]
            ty = struct.unpack('<H', pl[3:5])[0]
            log(f"  Found resource: ({tx},{ty}) from 0x033F ({len(pl)}B)")
            tiles.append((tx, ty))
        elif op not in (0x0042, 0x036C, 0x0002):
            log(f"  Search side: 0x{op:04X} ({len(pl)}B)")
    return tiles

def main():
    log("=== GATHER TEST v2 (Simple Mode - No 0x0023) ===")

    access_key = node_login(EMAIL, PASSWORD, IGG_ID)
    if not access_key:
        log("Login failed!"); return
    log(f"Access key: {access_key[:8]}...")

    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    gc = GameConnection(IGG_ID, gw['ip'], gw['port'], gw['token'])
    gc.on_packet(on_packet)
    gc.connect()

    if not gc.codec:
        log("No codec!"); gc.disconnect(); return

    codec = gc.codec
    time.sleep(3)
    responses.clear()

    # ════════════════════════════════════════
    # PHASE 1: Setup (matching PCAP)
    # ════════════════════════════════════════
    log("\n=== PHASE 1: Setup ===")
    gc.send(build_packet(0x0840))                    # INIT
    gc.send(build_packet(0x0245))                    # MARCH_SCREEN
    gc.send(build_formation())                        # FORMATION (real data!)
    gc.send(build_packet(0x0709))                    # EXTRA_A
    gc.send(build_packet(0x0A2C))                    # EXTRA_B
    collect("SETUP", timeout=2)

    # ════════════════════════════════════════
    # PHASE 2: Search for resource tile
    # ════════════════════════════════════════
    log("\n=== PHASE 2: Search resource tile ===")
    tiles = search_resource(gc)
    if tiles:
        target_x, target_y = tiles[0]
    else:
        target_x, target_y = 650, 576
        log(f"  Using default target: ({target_x},{target_y})")

    # ════════════════════════════════════════
    # PHASE 3: ENABLE_VIEW(1) + view tile
    # ════════════════════════════════════════
    log("\n=== PHASE 3: ENABLE_VIEW(1) + view tile ===")
    gc.send(build_enable_view(codec, IGG_ID, 0x01))
    gc.send(build_tile_select(target_x, target_y))
    collect("VIEW1", timeout=2)

    # ════════════════════════════════════════
    # PHASE 4: ENABLE_VIEW(0) + troop selection
    # ════════════════════════════════════════
    log("\n=== PHASE 4: ENABLE_VIEW(0) + troops ===")
    gc.send(build_enable_view(codec, IGG_ID, 0x00))
    for tid in TROOP_IDS:
        gc.send(build_troop_select(tid))
    collect("TROOPS", timeout=2)

    # ════════════════════════════════════════
    # PHASE 5: Sync
    # ════════════════════════════════════════
    log("\n=== PHASE 5: Sync ===")
    gc.send(build_packet(0x0767))
    gc.send(build_packet(0x0769))
    collect("SYNC", timeout=2)

    # ════════════════════════════════════════
    # PHASE 6: ENABLE_VIEW(1) + source tile + target tile
    # ════════════════════════════════════════
    log("\n=== PHASE 6: Second ENABLE_VIEW + tiles ===")
    gc.send(build_enable_view(codec, IGG_ID, 0x01))
    gc.send(build_tile_select(TURF_X, TURF_Y))  # source = castle
    time.sleep(1)
    gc.send(build_tile_select(target_x, target_y))  # target
    collect("VIEW2", timeout=3)

    # ════════════════════════════════════════
    # PHASE 7: Heartbeat + GATHER
    # ════════════════════════════════════════
    log("\n=== PHASE 7: GATHER ===")
    ms = int((time.time() - gc.start_time) * 1000)
    gc.send(build_packet(0x0042, struct.pack('<II', ms, 0)))
    time.sleep(1.5)

    gc.send(build_gather_0ce8(codec, target_x, target_y))

    log("  Waiting for response chain (0x00B8 → 0x0071 → 0x076C)...")
    r = collect("GATHER", timeout=15)

    # ════════════════════════════════════════
    # ANALYSIS
    # ════════════════════════════════════════
    log("\n=== RESULT ===")
    opcodes_got = [op for op, _ in r]
    has_00b8 = 0x00B8 in opcodes_got
    has_0071 = 0x0071 in opcodes_got
    has_076c = 0x076C in opcodes_got
    has_00b9 = 0x00B9 in opcodes_got

    log(f"  0x00B8 MARCH_ACCEPT:  {'YES' if has_00b8 else 'no'}")
    log(f"  0x0071 MARCH_STATE:   {'YES' if has_0071 else 'no'}")
    log(f"  0x076C MARCH_BUNDLE:  {'YES' if has_076c else 'no'}")
    log(f"  0x00B9 MARCH_ACK:     {'YES' if has_00b9 else 'no'}")

    if has_0071:
        log("\n  >>> GATHER SUCCESS! March created! <<<")
    elif has_00b8:
        log("\n  >>> PARTIAL: Format accepted but march NOT created <<<")
        # Print 0x00B8 payload for analysis
        for op, pl in r:
            if op == 0x00B8:
                log(f"  >>> 0x00B8 payload ({len(pl)}B): {pl.hex()}")
            if op == 0x00B9:
                log(f"  >>> 0x00B9 payload ({len(pl)}B): {pl.hex()}")
    else:
        log("\n  >>> GATHER FAILED - no response <<<")

    # Wait for late responses
    time.sleep(10)
    late = []
    while responses:
        op, pl = responses.pop(0)
        if op not in (0x0042, 0x036C, 0x0002):
            late.append((op, pl))
    if late:
        log("\n  Late responses:")
        for op, pl in late:
            log(f"    <- 0x{op:04X} {opname(op)} ({len(pl)}B)")

    gc.disconnect()
    log("=== DONE ===")

if __name__ == '__main__':
    main()

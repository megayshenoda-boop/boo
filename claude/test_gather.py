"""
Gather Test - Full sequence matching PCAP exactly
Key differences from old bot:
  1. Send 0x0023 AUTH early
  2. Send 0x0CEB ENABLE_VIEW 3 times (not 1)
  3. Send 0x01D6 READY_SIG before gather
  4. Correct 46-byte 0x0CE8 payload
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
MARCH_TYPE = 0x1749  # gather type (verified from 7 PCAPs)
TURF_X, TURF_Y = 653, 567  # castle location

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

def build_auth_0023(access_key, igg_id):
    """0x0023 AUTH - MUST be sent early (PCAP verified structure)."""
    data = bytearray(58)
    struct.pack_into('<Q', data, 0, 1)           # flag = 1
    struct.pack_into('<I', data, 8, igg_id)      # IGG_ID
    struct.pack_into('<H', data, 16, 32)         # str_len = 32
    key_bytes = access_key[:32].encode('ascii')
    data[18:18+len(key_bytes)] = key_bytes
    data[50] = 0x0E
    data[51] = 0xFF
    data[52] = 0x00
    data[53] = 0x3F
    return build_packet(0x0023, bytes(data))

def build_enable_view(codec, igg_id, view_type=0x01):
    """0x0CEB ENABLE_VIEW - 10B plaintext."""
    data = bytearray(10)
    data[0] = view_type
    struct.pack_into('<I', data, 1, igg_id)
    data[9] = 0x01
    return codec.encode(OP_ENABLE_VIEW, bytes(data))

def build_tile_select(x, y):
    """0x006E TILE_SELECT - 5B."""
    data = struct.pack('<HHB', x, y, 0x01)
    return build_packet(0x006E, data)

def build_troop_select(troop_id):
    """0x099D troop selection."""
    return build_packet(0x099D, struct.pack('<I', troop_id))

def build_gather_0ce8(codec, tile_x, tile_y, hero_id=255, march_slot=1,
                       kingdom=KINGDOM, igg_id=IGG_ID):
    """0x0CE8 GATHER - 46B plaintext (verified from 7 PCAPs)."""
    data = bytearray(46)
    data[0] = march_slot & 0xFF
    data[1] = random.randint(0, 255)  # nonce
    data[2] = random.randint(0, 255)
    data[3] = random.randint(0, 255)
    struct.pack_into('<H', data, 4, MARCH_TYPE)   # 0x1749
    # [6:9] = zeros
    struct.pack_into('<H', data, 9, tile_x)
    struct.pack_into('<H', data, 11, tile_y)
    data[13] = 0x01                               # action flag
    data[14] = hero_id & 0xFF                     # hero
    # [15:18] = zeros
    data[18] = kingdom & 0xFF                     # 0xB6 = 182
    # [19:22] = zeros
    data[22] = 0x04                               # constant
    # [23:33] = zeros
    struct.pack_into('<I', data, 33, igg_id)
    # [37:46] = zeros
    log(f"  0x0CE8 plaintext ({len(data)}B): {data.hex()}")
    return codec.encode(OP_START_MARCH, bytes(data))

# ──── RESPONSE TRACKING ────

responses = []
def on_packet(opcode, payload):
    responses.append((opcode, payload))

def collect_responses(label, timeout=8):
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

def search_resource_tile(gc):
    """Send 0x033E to find a resource tile near castle."""
    # Search for food tile (type=1) near castle
    # Format from PCAP: level, search params
    data = struct.pack('<BBBB', 0x01, 0x00, 0x00, 0x00)
    gc.send(build_packet(0x033E, data))
    time.sleep(3)
    # Check for 0x033F response
    tiles = []
    while responses:
        op, pl = responses.pop(0)
        if op == 0x033F and len(pl) >= 8:
            # Try to parse tile coordinates from response
            tiles.append((op, pl))
            log(f"  Search result 0x033F ({len(pl)}B): {pl[:30].hex()}")
        elif op not in (0x0042, 0x036C, 0x0002):
            log(f"  Search side-effect: 0x{op:04X} ({len(pl)}B)")
    return tiles

def main():
    log("=== GATHER TEST (Full PCAP Sequence) ===")

    # Login
    access_key = node_login(EMAIL, PASSWORD, IGG_ID)
    if not access_key:
        log("Login failed!"); return
    log(f"Access key: {access_key[:8]}...")

    # Gateway
    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)

    # Connect
    gc = GameConnection(IGG_ID, gw['ip'], gw['port'], gw['token'])
    gc.on_packet(on_packet)
    gc.connect()

    if not gc.codec:
        log("No codec!"); gc.disconnect(); return

    codec = gc.codec
    time.sleep(3)
    responses.clear()

    # ════════════════════════════════════════
    # PHASE 1: AUTH (missing from old bot!)
    # ════════════════════════════════════════
    log("\n=== PHASE 1: Send 0x0023 AUTH ===")
    gc.send(build_auth_0023(access_key, IGG_ID))
    collect_responses("AUTH", timeout=3)

    # ════════════════════════════════════════
    # PHASE 2: INIT (matching PCAP order)
    # ════════════════════════════════════════
    log("\n=== PHASE 2: INIT packets ===")
    gc.send(build_packet(0x0840))           # INIT
    gc.send(build_packet(0x0245))           # MARCH_SCREEN
    # Formation data (42B from PCAP - simplified)
    gc.send(build_packet(0x0834, b'\x00' * 38))
    gc.send(build_packet(0x0709))           # EXTRA_A
    gc.send(build_packet(0x0A2C))           # EXTRA_B
    collect_responses("INIT", timeout=3)

    # ════════════════════════════════════════
    # PHASE 3: ENABLE_VIEW #1 (before troops)
    # ════════════════════════════════════════
    log("\n=== PHASE 3: ENABLE_VIEW #1 ===")
    gc.send(build_enable_view(codec, IGG_ID, 0x01))
    collect_responses("ENABLE_VIEW_1", timeout=3)

    # ════════════════════════════════════════
    # PHASE 4: Tile select (source = castle)
    # ════════════════════════════════════════
    log("\n=== PHASE 4: TILE_SELECT (source=castle) ===")
    gc.send(build_tile_select(TURF_X, TURF_Y))
    collect_responses("TILE_SOURCE", timeout=2)

    # ════════════════════════════════════════
    # PHASE 5: Troop selection (4 troops from PCAP)
    # ════════════════════════════════════════
    log("\n=== PHASE 5: TROOP SELECTION ===")
    for tid in [403, 405, 407, 411]:
        gc.send(build_troop_select(tid))
    collect_responses("TROOPS", timeout=2)

    # ════════════════════════════════════════
    # PHASE 6: SYNC
    # ════════════════════════════════════════
    log("\n=== PHASE 6: SYNC ===")
    gc.send(build_packet(0x0767))
    gc.send(build_packet(0x0769))
    collect_responses("SYNC", timeout=2)

    # ════════════════════════════════════════
    # PHASE 7: ENABLE_VIEW #2
    # ════════════════════════════════════════
    log("\n=== PHASE 7: ENABLE_VIEW #2 ===")
    gc.send(build_enable_view(codec, IGG_ID, 0x01))
    collect_responses("ENABLE_VIEW_2", timeout=3)

    # ════════════════════════════════════════
    # PHASE 8: Select target tile (resource near castle)
    # ════════════════════════════════════════
    log("\n=== PHASE 8: TARGET TILE ===")
    # Use a known good tile from PCAP: (650, 576)
    target_x, target_y = 650, 576
    gc.send(build_tile_select(target_x, target_y))
    collect_responses("TILE_TARGET", timeout=2)

    # ════════════════════════════════════════
    # PHASE 9: READY_SIG (newer PCAPs send this)
    # ════════════════════════════════════════
    log("\n=== PHASE 9: READY_SIG (0x01D6) ===")
    gc.send(build_packet(0x01D6))
    collect_responses("READY_SIG", timeout=3)

    # ════════════════════════════════════════
    # PHASE 10: HEARTBEAT then GATHER
    # ════════════════════════════════════════
    log("\n=== PHASE 10: GATHER (0x0CE8) ===")
    ms = int((time.time() - gc.start_time) * 1000)
    gc.send(build_packet(0x0042, struct.pack('<II', ms, 0)))  # heartbeat
    time.sleep(1)

    gc.send(build_gather_0ce8(codec, target_x, target_y, hero_id=255,
                               march_slot=1, igg_id=IGG_ID))

    # Wait longer for gather response chain
    log("  Waiting for response chain (0x00B8 → 0x0071 → 0x076C)...")
    r = collect_responses("GATHER", timeout=12)

    # ════════════════════════════════════════
    # ANALYSIS
    # ════════════════════════════════════════
    log("\n=== RESULT ANALYSIS ===")
    opcodes_got = [op for op, _ in r]

    has_00b8 = 0x00B8 in opcodes_got
    has_0071 = 0x0071 in opcodes_got
    has_076c = 0x076C in opcodes_got
    has_007c = 0x007C in opcodes_got
    has_00b9 = 0x00B9 in opcodes_got

    log(f"  0x00B8 MARCH_ACCEPT:  {'YES' if has_00b8 else 'no'}")
    log(f"  0x0071 MARCH_STATE:   {'YES' if has_0071 else 'no'}")
    log(f"  0x076C MARCH_BUNDLE:  {'YES' if has_076c else 'no'}")
    log(f"  0x007C COLLECT_STATE: {'YES' if has_007c else 'no'}")
    log(f"  0x00B9 MARCH_ACK:    {'YES' if has_00b9 else 'no'}")

    if has_0071:
        log("\n  >>> GATHER SUCCESS! March actually created! <<<")
    elif has_00b8 and not has_0071:
        log("\n  >>> PARTIAL: Server accepted format (0x00B8) but march NOT created (no 0x0071)")
        log("  >>> Still missing something - maybe 0x1B8B session or troop context")
    else:
        log("\n  >>> GATHER FAILED - no acceptance signal")

    # Wait for late responses (collect state etc)
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
            if op == 0x0071:
                log("    >>> LATE 0x0071 = MARCH CREATED!")
            if op == 0x007C:
                log("    >>> LATE 0x007C = COLLECTING RESOURCES!")

    gc.disconnect()
    log("=== DONE ===")

if __name__ == '__main__':
    main()

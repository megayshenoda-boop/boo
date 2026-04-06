"""
Gather Test v3 - Minimal approach matching old bot's working 0x00B8 sequence.
Includes 0x17A3, 5 troops, and verifies encryption by also sending a known-working train.
"""
import sys, time, struct, subprocess, random
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from game_server import GameConnection
from codec import CMsgCodec
from packets import build_packet
from protocol import opname, OP_ENABLE_VIEW, OP_START_MARCH, OP_TRAIN

KINGDOM = 182
MARCH_TYPE = 0x1749
TURF_X, TURF_Y = 653, 567
TROOP_IDS = [403, 405, 406, 407, 411]  # 5 troops (old bot used 5)
FORMATION_TROOPS = [1046, 3002, 1035, 2008, 2019, 1009, 1024, 1016, 2009, 1025]

def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def node_login(email, password, igg_id):
    result = subprocess.run(
        ['node', r'D:\CascadeProjects\lords_bot\http_login.mjs', email, password, str(igg_id)],
        capture_output=True, text=True, timeout=30
    )
    return result.stdout.strip() if len(result.stdout.strip()) == 32 else None

def build_enable_view(codec, igg_id, view_type=0x01):
    data = bytearray(10)
    data[0] = view_type
    struct.pack_into('<I', data, 1, igg_id)
    data[9] = 0x01
    return codec.encode(OP_ENABLE_VIEW, bytes(data))

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

def build_train(codec, troop_type=1, count=10):
    """Known-working train command to verify encryption."""
    data = bytearray(19)
    data[0] = troop_type & 0xFF
    struct.pack_into('<I', data, 4, count)
    struct.pack_into('<I', data, 8, 0x24254900 | (troop_type & 0xFF))
    return codec.encode(OP_TRAIN, bytes(data))

responses = []
def on_packet(opcode, payload):
    responses.append((opcode, payload))

def collect(label, timeout=5):
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

def main():
    log("=== GATHER TEST v3 ===")

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

    # ──── VERIFY ENCRYPTION: Send a train (known working) ────
    log("\n=== VERIFY: Train 10 infantry ===")
    gc.send(build_train(codec, troop_type=1, count=10))
    r_train = collect("TRAIN", timeout=5)
    has_06c4 = any(op == 0x06C4 for op, _ in r_train)
    if has_06c4:
        log("  >>> TRAIN SUCCESS - encryption verified <<<")
    else:
        log("  >>> TRAIN FAILED - encryption might be broken! <<<")
        # Don't abort, still try gather

    # ──── Check active marches ────
    log("\n=== Check active marches from 0x0078 ===")
    raw_0078 = gc.game_state.raw_packets.get(0x0078, [])
    for i, pl in enumerate(raw_0078):
        if len(pl) >= 2:
            count = struct.unpack('<H', pl[0:2])[0]
            log(f"  0x0078 chunk {i}: {count} march entries ({len(pl)}B)")

    # ──── GATHER SEQUENCE (old bot style) ────
    log("\n=== GATHER SEQUENCE ===")

    # Phase 1: Setup
    log("Phase 1: Setup")
    gc.send(build_packet(0x0840))
    gc.send(build_packet(0x0245))
    data = struct.pack('<H', len(FORMATION_TROOPS))
    for tid in FORMATION_TROOPS:
        data += struct.pack('<I', tid)
    gc.send(build_packet(0x0834, data))
    gc.send(build_packet(0x0709))
    gc.send(build_packet(0x0A2C))
    time.sleep(1)

    # Phase 2: 0x17A3 (old bot had this, PCAP mode doesn't)
    log("Phase 2: 0x17A3")
    gc.send(build_packet(0x17A3, b'\x02\x00\x00\x00'))
    time.sleep(0.5)

    # Phase 3: Troops (5 troops like old bot)
    log(f"Phase 3: {len(TROOP_IDS)} troops")
    for tid in TROOP_IDS:
        gc.send(build_packet(0x099D, struct.pack('<I', tid)))
    time.sleep(0.5)

    # Phase 4: Sync
    log("Phase 4: Sync")
    gc.send(build_packet(0x0767))
    gc.send(build_packet(0x0769))
    time.sleep(1)

    # Phase 5: ENABLE_VIEW(1) - after troops (old bot order)
    log("Phase 5: ENABLE_VIEW(1)")
    gc.send(build_enable_view(codec, IGG_ID, 0x01))
    time.sleep(0.5)

    # Phase 6: Source tile (castle)
    log(f"Phase 6: Source tile ({TURF_X},{TURF_Y})")
    gc.send(build_packet(0x006E, struct.pack('<HHB', TURF_X, TURF_Y, 0x01)))
    time.sleep(1)

    # Phase 7: Target tile
    target_x, target_y = 650, 576  # nearby tile
    log(f"Phase 7: Target tile ({target_x},{target_y})")
    gc.send(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 0x01)))
    time.sleep(1.5)

    # Drain pre-gather responses
    pre = collect("PRE-GATHER", timeout=0.1)

    # Phase 8: Heartbeat
    log("Phase 8: Heartbeat")
    ms = int((time.time() - gc.start_time) * 1000)
    gc.send(build_packet(0x0042, struct.pack('<II', ms, 0)))
    time.sleep(1.5)

    # Phase 9: GATHER!
    log(f"\nPhase 9: GATHER 0x0CE8 -> ({target_x},{target_y})")
    gc.send(build_gather_0ce8(codec, target_x, target_y, hero_id=255, march_slot=1))

    log("  Waiting 15s for response...")
    r = collect("GATHER", timeout=15)

    # Analysis
    opcodes_got = [op for op, _ in r]
    has_00b8 = 0x00B8 in opcodes_got
    has_0071 = 0x0071 in opcodes_got
    has_00b9 = 0x00B9 in opcodes_got
    has_0033 = 0x0033 in opcodes_got

    log(f"\n=== RESULT ===")
    log(f"  0x00B8 MARCH_ACCEPT: {'YES' if has_00b8 else 'no'}")
    log(f"  0x0071 MARCH_STATE:  {'YES' if has_0071 else 'no'}")
    log(f"  0x00B9 MARCH_ACK:    {'YES' if has_00b9 else 'no'}")
    log(f"  0x0033 ATTR_CHANGE:  {'YES' if has_0033 else 'no'}")

    for op, pl in r:
        if op in (0x00B8, 0x00B9, 0x0071, 0x076C, 0x0033):
            log(f"  >>> 0x{op:04X} payload: {pl.hex()}")

    if has_0071:
        log("\n  GATHER SUCCESS!")
    elif has_00b8:
        log("\n  PARTIAL: got 0x00B8 (format ok) but no 0x0071 (march not created)")
    else:
        log("\n  FAILED: no response to gather at all")

    # Late responses
    time.sleep(8)
    while responses:
        op, pl = responses.pop(0)
        if op not in (0x0042, 0x036C, 0x0002):
            log(f"  Late: 0x{op:04X} ({len(pl)}B)")

    gc.disconnect()
    log("=== DONE ===")

if __name__ == '__main__':
    main()

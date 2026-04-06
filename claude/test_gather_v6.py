"""
Gather Test v6 - Based on FRESH PCAP analysis.
Key changes from previous tests:
1. ADD 0x0323 right before 0x0CE8 (was completely missing!)
2. NO 0x0023 AUTH (PCAP doesn't send it!)
3. NO 0x01D6 READY_SIG (PCAP doesn't send it!)
4. Add extra init packets: 0x17D4, 0x0AF2, 0x1357, 0x170D, 0x11FF
5. Add 0x0043 timing, 0x0674
6. 7 troops (403-411), not 4
7. Only 1 ENABLE_VIEW, not 3
8. Use march_slot=2 (slot 1 may be occupied from previous PCAP gather)
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
TROOP_IDS = [403, 405, 407, 408, 409, 410, 411]  # ALL 7 troops from PCAP!
FORMATION_TROOPS = [3002, 1035, 2008, 2019, 1009, 1024, 1016, 2009, 1025, 1046]

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

def build_gather_0ce8(codec, tile_x, tile_y, hero_id=255, march_slot=2):
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

def build_0323(march_slot=2, hero_id=255):
    """0x0323 PRE-GATHER command - from PCAP: [0,slot,0,hero,0,0,0]"""
    data = bytearray(7)
    data[0] = 0x00
    data[1] = march_slot & 0xFF
    data[2] = 0x00
    data[3] = hero_id & 0xFF
    # [4:7] = zeros
    return build_packet(0x0323, data)

responses = []
def on_packet(opcode, payload):
    responses.append((opcode, payload))

def drain(label="", timeout=3):
    time.sleep(timeout)
    found = []
    while responses:
        op, pl = responses.pop(0)
        if op not in (0x0042, 0x036C, 0x0002):
            found.append((op, pl))
    if found and label:
        log(f"  [{label}] {len(found)} responses:")
        for op, pl in found:
            prefix = pl[:20].hex() if pl else ""
            log(f"    <- 0x{op:04X} {opname(op)} ({len(pl)}B) {prefix}")
    return found


def main():
    log("=== GATHER TEST v6 (Fresh PCAP Sequence) ===")

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
    # EXACT PCAP SEQUENCE (from gather_fresh.pcap)
    # ════════════════════════════════════════

    # Phase 1: Init packets (PCAP order)
    log("\n=== Phase 1: Init ===")
    gc.send(build_packet(0x0840))           # INIT
    gc.send(build_packet(0x17D4))           # NEW! from PCAP
    gc.send(build_packet(0x0AF2))           # NEW! from PCAP
    gc.send(build_packet(0x0245))           # MARCH_SCREEN
    # Formation with real troop IDs
    fdata = struct.pack('<H', len(FORMATION_TROOPS))
    for tid in FORMATION_TROOPS:
        fdata += struct.pack('<I', tid)
    gc.send(build_packet(0x0834, fdata))    # FORMATION
    gc.send(build_packet(0x0709))           # EXTRA_A
    gc.send(build_packet(0x0A2C))           # EXTRA_B
    gc.send(build_packet(0x1357, struct.pack('<I', 2)))  # NEW!
    gc.send(build_packet(0x170D, struct.pack('<I', 2)))  # NEW!
    drain("INIT", timeout=2)

    # Phase 2: 0x0043 timing + 0x0674
    log("\n=== Phase 2: Timing ===")
    # 0x0043 from PCAP: first 8B = timestamp (same as heartbeat), rest zeros
    ms = int((time.time() - gc.start_time) * 1000)
    timing = struct.pack('<II', ms, 0) + b'\x00' * 8
    gc.send(build_packet(0x0043, timing))
    gc.send(build_packet(0x0674))
    time.sleep(0.5)

    # Phase 3: Troop selection (7 troops from PCAP!)
    log("\n=== Phase 3: 7 Troops ===")
    for tid in TROOP_IDS:
        gc.send(build_packet(0x099D, struct.pack('<I', tid)))
    time.sleep(0.5)

    # Phase 4: Sync
    log("\n=== Phase 4: Sync ===")
    gc.send(build_packet(0x0767))
    gc.send(build_packet(0x0769))
    gc.send(build_packet(0x11FF, struct.pack('<I', 1)))  # NEW!
    time.sleep(1)

    # Phase 5: ENABLE_VIEW + view tile (only 1 time!)
    log("\n=== Phase 5: ENABLE_VIEW + tile ===")
    gc.send(build_enable_view(codec, IGG_ID, 0x01))
    gc.send(build_packet(0x006E, struct.pack('<HHB', TURF_X, TURF_Y, 0x01)))
    time.sleep(1)

    # Phase 6: Heartbeat + 0x0043
    log("\n=== Phase 6: Heartbeat ===")
    ms = int((time.time() - gc.start_time) * 1000)
    gc.send(build_packet(0x0042, struct.pack('<II', ms, 0)))
    gc.send(build_packet(0x0043, struct.pack('<II', ms, 0) + b'\x00' * 8))
    time.sleep(0.5)

    # Phase 7: Search for resource tile
    log("\n=== Phase 7: Search ===")
    gc.send(build_packet(0x033E, bytes([0x01, 0x04, 0x00, 0x03])))
    time.sleep(3)
    target_x, target_y = None, None
    while responses:
        op, pl = responses.pop(0)
        if op == 0x033F and len(pl) >= 5:
            tx = struct.unpack('<H', pl[1:3])[0]
            ty = struct.unpack('<H', pl[3:5])[0]
            log(f"  Found resource: ({tx},{ty})")
            if target_x is None:
                target_x, target_y = tx, ty
        elif op not in (0x0042, 0x036C, 0x0002):
            pass  # skip noise
    if target_x is None:
        target_x, target_y = 555, 853
        log(f"  Default target: ({target_x},{target_y})")

    # Drain remaining
    drain("PRE-GATHER", timeout=1)

    # Phase 8: Target tile select
    log(f"\n=== Phase 8: Target tile ({target_x},{target_y}) ===")
    gc.send(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 0x01)))
    time.sleep(0.5)

    # Phase 9: 0x0323 PRE-GATHER COMMAND (the NEW discovery!)
    march_slot = 2
    log(f"\n=== Phase 9: 0x0323 PRE-GATHER (slot={march_slot}, hero=255) ===")
    gc.send(build_0323(march_slot=march_slot, hero_id=255))
    time.sleep(0.5)

    # Phase 10: GATHER!
    log(f"\n=== Phase 10: 0x0CE8 GATHER slot={march_slot} -> ({target_x},{target_y}) ===")
    gc.send(build_gather_0ce8(codec, target_x, target_y, hero_id=255, march_slot=march_slot))

    log("  Waiting 20s for response chain...")
    r = drain("GATHER", timeout=20)

    # Analysis
    opcodes_got = [op for op, _ in r]
    has_00b8 = 0x00B8 in opcodes_got
    has_0071 = 0x0071 in opcodes_got
    has_076c = 0x076C in opcodes_got
    has_007c = 0x007C in opcodes_got
    has_00b9 = 0x00B9 in opcodes_got
    has_0033 = 0x0033 in opcodes_got

    log(f"\n{'='*50}")
    log(f"  0x00B8 MARCH_ACCEPT:  {'YES!' if has_00b8 else 'no'}")
    log(f"  0x0071 MARCH_STATE:   {'YES!' if has_0071 else 'no'}")
    log(f"  0x076C MARCH_BUNDLE:  {'YES!' if has_076c else 'no'}")
    log(f"  0x007C COLLECT_STATE: {'YES!' if has_007c else 'no'}")
    log(f"  0x00B9 MARCH_ACK:     {'YES!' if has_00b9 else 'no'}")
    log(f"  0x0033 ATTR_CHANGE:   {'YES!' if has_0033 else 'no'}")
    log(f"{'='*50}")

    for op, pl in r:
        if op in (0x00B8, 0x0071, 0x076C, 0x007C, 0x0033, 0x0037, 0x00B9):
            log(f"  0x{op:04X}: {pl.hex()}")

    if has_0071:
        log("\n  >>> GATHER SUCCESS! MARCH CREATED! <<<")
    elif has_00b8:
        log("\n  >>> PARTIAL: 0x00B8 received but no 0x0071 <<<")
    else:
        log("\n  >>> FAILED <<<")

    # Late responses
    time.sleep(15)
    while responses:
        op, pl = responses.pop(0)
        if op not in (0x0042, 0x036C, 0x0002):
            log(f"  Late: 0x{op:04X} ({len(pl)}B)")
            if op == 0x0071:
                log("  >>> LATE 0x0071 = MARCH CREATED! <<<")
            if op == 0x007C:
                log("  >>> LATE 0x007C = COLLECTING! <<<")

    gc.disconnect()
    log("=== DONE ===")

if __name__ == '__main__':
    main()

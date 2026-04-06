"""
Gather Test v8 - Replicates EXACT successful codex_lab/gather_v3 sequence.
From gather_v3_20260322_074726.log (SUCCESS with 0x076C).

Key differences from v7:
  - NO 0x1B8B (causes disconnection)
  - NO 0x0323 (not needed)
  - 0x17A3 instead of 0x17D4/0x0AF2/0x1357/0x170D
  - Order: troops -> sync -> prelude -> source -> target -> heartbeat -> DRAIN -> 0x0CE8
  - Active packet drain before 0x0CE8 (wait for heartbeat echo)
  - Template-based 0x0CE8 plaintext from successful PCAP
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
TURF_X, TURF_Y = 653, 567  # Our castle position
TROOP_IDS = [403, 405, 406, 407, 411]  # 5 troops (same as successful run)
FORMATION_TROOPS = [1025, 1046, 2014, 3002, 1035, 2008, 2019, 1009, 1024, 1016]

# PCAP-verified 0x0CE8 template (hero=255, from successful captures)
TEMPLATE_HERO255 = "011be0c649170000008a02400201ff000000b60000000400000000000000000000ed027322000000000000000000"

def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def node_login(email, password, igg_id):
    result = subprocess.run(
        ['node', r'D:\CascadeProjects\lords_bot\http_login.mjs', email, password, str(igg_id)],
        capture_output=True, text=True, timeout=30
    )
    return result.stdout.strip() if len(result.stdout.strip()) == 32 else None

def build_gather_from_template(tile_x, tile_y, hero_id=255, march_slot=2):
    """Build 0x0CE8 plaintext from PCAP template, patching dynamic fields."""
    plain = bytearray.fromhex(TEMPLATE_HERO255)
    assert len(plain) == 46
    # Patch dynamic fields
    plain[0] = march_slot & 0xFF
    plain[1] = random.randint(0, 255)  # nonce bytes
    plain[2] = random.randint(0, 255)
    plain[3] = random.randint(0, 255)
    struct.pack_into('<H', plain, 4, MARCH_TYPE)
    struct.pack_into('<H', plain, 9, tile_x)
    struct.pack_into('<H', plain, 11, tile_y)
    plain[13] = 0x01
    plain[14] = hero_id & 0xFF
    plain[18] = KINGDOM & 0xFF
    plain[22] = 0x04
    struct.pack_into('<I', plain, 33, IGG_ID)
    return bytes(plain)

def build_enable_view(codec, igg_id, view_type=0x01):
    data = bytearray(10)
    data[0] = view_type
    struct.pack_into('<I', data, 1, igg_id)
    data[9] = 0x01
    return codec.encode(OP_ENABLE_VIEW, bytes(data))

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
        for op, pl in found[:10]:
            prefix = pl[:20].hex() if pl else ""
            log(f"    <- 0x{op:04X} {opname(op)} ({len(pl)}B) {prefix}")
        if len(found) > 10:
            log(f"    ... and {len(found)-10} more")
    return found

def wait_for_heartbeat_echo(timeout=5):
    """Wait for heartbeat echo while draining all other packets."""
    start = time.time()
    count = 0
    while time.time() - start < timeout:
        if not responses:
            time.sleep(0.1)
            continue
        op, pl = responses.pop(0)
        if op == 0x0042:
            log(f"  Heartbeat echo received! (drained {count} packets)")
            return True
        if op not in (0x0002, 0x036C):
            count += 1
    log(f"  Heartbeat echo timeout (drained {count} packets)")
    return False


def main():
    log("=== GATHER TEST v8 (codex_lab v3 replica) ===")

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

    # ══════════════════════════════════════════════════
    # EXACT codex_lab v3 SUCCESSFUL sequence
    # From gather_v3_20260322_074726.log
    # ══════════════════════════════════════════════════

    # Step 1: UI Setup (0x0840 + 0x0245 + 0x0834 formation)
    log("\n=== Step 1: UI Setup ===")
    gc.send(build_packet(0x0840))
    gc.send(build_packet(0x0245))
    fdata = struct.pack('<H', len(FORMATION_TROOPS))
    for tid in FORMATION_TROOPS:
        fdata += struct.pack('<I', tid)
    gc.send(build_packet(0x0834, fdata))

    # Step 2: Setup extras (0x0709 + 0x0A2C + 0x17A3)
    log("=== Step 2: Setup extras ===")
    gc.send(build_packet(0x0709))
    gc.send(build_packet(0x0A2C))
    gc.send(build_packet(0x17A3, b'\x02\x00\x00\x00'))
    log("  Sent 0x0709 + 0x0A2C + 0x17A3")
    drain("SETUP", timeout=1)

    # Step 3: Troop selection (5 troops - same as successful run)
    log("\n=== Step 3: 5 Troops ===")
    for tid in TROOP_IDS:
        gc.send(build_packet(0x099D, struct.pack('<I', tid)))
    log(f"  Sent {len(TROOP_IDS)}x 0x099D: {TROOP_IDS}")

    # Step 4: Sync (0x0767 + 0x0769)
    log("\n=== Step 4: Sync ===")
    gc.send(build_packet(0x0767))
    gc.send(build_packet(0x0769))

    # Step 5: Prelude (0x0CEB enable_view)
    log("\n=== Step 5: Prelude 0x0CEB ===")
    prelude_data = bytearray(10)
    prelude_data[0] = 0x01
    struct.pack_into('<I', prelude_data, 1, IGG_ID)
    prelude_data[9] = 0x01
    gc.send(codec.encode(OP_ENABLE_VIEW, bytes(prelude_data)))
    log(f"  0x0CEB prelude: {prelude_data.hex()}")

    # Step 6: Source tile (our castle) then Target tile
    log("\n=== Step 6: Source + Target tiles ===")
    gc.send(build_packet(0x006E, struct.pack('<HHB', TURF_X, TURF_Y, 0x01)))
    log(f"  Source tile: ({TURF_X},{TURF_Y})")
    time.sleep(0.2)

    # Search for resource tile
    log("  Searching for resource tile...")
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
    if target_x is None:
        target_x, target_y = 555, 853
        log(f"  Default target: ({target_x},{target_y})")

    # Send target tile
    gc.send(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 0x01)))
    log(f"  Target tile: ({target_x},{target_y})")

    # Step 7: Pre-0x0CE8 heartbeat + ACTIVE DRAIN
    log("\n=== Step 7: Heartbeat + Drain ===")
    time.sleep(0.5)
    responses.clear()
    ms = int((time.time() - gc.start_time) * 1000)
    gc.send(build_packet(0x0042, struct.pack('<II', ms, 0)))
    log(f"  Sent heartbeat ms={ms}")

    # CRITICAL: Wait for heartbeat echo while draining ALL server packets
    # The codex_lab bot receives 100+ packets here before sending 0x0CE8
    wait_for_heartbeat_echo(timeout=5)

    # Extra drain to catch any remaining flood
    time.sleep(1.5)
    pre_count = 0
    while responses:
        op, pl = responses.pop(0)
        if op not in (0x0042, 0x036C, 0x0002):
            pre_count += 1
            if op in (0x0022, 0x1B8A, 0x0071):
                log(f"  Pre-0x0CE8 important: 0x{op:04X} ({len(pl)}B)")
    log(f"  Drained {pre_count} additional packets")

    # Step 8: 0x0CE8 GATHER!
    log(f"\n=== Step 8: 0x0CE8 GATHER slot=2 -> ({target_x},{target_y}) ===")
    march_slot = 2
    gather_plain = build_gather_from_template(target_x, target_y, hero_id=244, march_slot=march_slot)
    log(f"  Plaintext ({len(gather_plain)}B): {gather_plain.hex()}")
    gather_pkt = codec.encode(OP_START_MARCH, gather_plain)
    gc.send(gather_pkt)

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
    has_0076 = 0x0076 in opcodes_got
    has_0077 = 0x0077 in opcodes_got
    has_0078 = 0x0078 in opcodes_got

    log(f"\n{'='*50}")
    log(f"  0x0076 MARCH_DATA:    {'YES!' if has_0076 else 'no'}")
    log(f"  0x0077 MARCH_DATA:    {'YES!' if has_0077 else 'no'}")
    log(f"  0x0078 MARCH_DATA:    {'YES!' if has_0078 else 'no'}")
    log(f"  0x00B8 MARCH_ACCEPT:  {'YES!' if has_00b8 else 'no'}")
    log(f"  0x0071 MARCH_STATE:   {'YES!' if has_0071 else 'no'}")
    log(f"  0x076C MARCH_BUNDLE:  {'YES!' if has_076c else 'no'}")
    log(f"  0x007C COLLECT_STATE: {'YES!' if has_007c else 'no'}")
    log(f"  0x00B9 MARCH_ACK:     {'YES!' if has_00b9 else 'no'}")
    log(f"  0x0033 ATTR_CHANGE:   {'YES!' if has_0033 else 'no'}")
    log(f"{'='*50}")

    for op, pl in r:
        if op in (0x0076, 0x0077, 0x0078, 0x00B8, 0x0071, 0x076C, 0x007C, 0x0033, 0x0037, 0x00B9):
            log(f"  0x{op:04X}: {pl.hex()[:80]}")

    if has_076c:
        log("\n  >>> GATHER SUCCESS! 0x076C RECEIVED! <<<")
    elif has_0071:
        log("\n  >>> SUCCESS! MARCH CREATED (0x0071)! <<<")
    elif has_00b8:
        log("\n  >>> PARTIAL: 0x00B8 received but no 0x0071/0x076C <<<")
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
            if op == 0x076C:
                log("  >>> LATE 0x076C = MARCH BUNDLE! <<<")

    gc.disconnect()
    log("=== DONE ===")

if __name__ == '__main__':
    main()

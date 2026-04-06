"""
Gather Test v4 - Debug focus:
1. Verify encryption via CommandEngine train()
2. Parse active marches from 0x076A + 0x0244
3. Try multiple march slots (1,2,3)
4. Use search-found tile
"""
import sys, time, struct, subprocess, random
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from game_server import GameConnection
from commands import CommandEngine
from packets import build_packet
from protocol import opname, OP_ENABLE_VIEW, OP_START_MARCH

KINGDOM = 182
MARCH_TYPE = 0x1749
TURF_X, TURF_Y = 653, 567
TROOP_IDS = [403, 405, 407, 411]
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
    log(f"  Plaintext ({len(data)}B) slot={march_slot}: {data.hex()}")
    return codec.encode(OP_START_MARCH, bytes(data))

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
    log("=== GATHER TEST v4 (Debug) ===")

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
    cmd = CommandEngine(IGG_ID, codec)
    time.sleep(3)
    responses.clear()

    # ──── 1. Verify encryption with CommandEngine train ────
    log("\n=== 1. VERIFY ENCRYPTION: CommandEngine.train() ===")
    gc.send(cmd.train(troop_type=1, count=1))
    r = drain("TRAIN", timeout=5)
    has_06c4 = any(op == 0x06C4 for op, _ in r)
    log(f"  Train result: 0x06C4 = {'YES' if has_06c4 else 'NO'}")
    if not has_06c4:
        log("  WARNING: Train failed! All encrypted commands may fail.")
        for op, pl in r:
            log(f"    Response: 0x{op:04X} ({len(pl)}B) {pl[:20].hex() if pl else ''}")

    # ──── 2. Parse active marches ────
    log("\n=== 2. ACTIVE MARCHES ===")
    # Check 0x0078 (march detail list from initial data)
    raw_0078 = gc.game_state.raw_packets.get(0x0078, [])
    total_marches = 0
    for pl in raw_0078:
        if len(pl) >= 2:
            cnt = struct.unpack('<H', pl[0:2])[0]
            total_marches += cnt
    log(f"  Initial march entries (0x0078): {total_marches}")

    # Check 0x0082 (march territory?)
    raw_0082 = gc.game_state.raw_packets.get(0x0082, [])
    for pl in raw_0082:
        log(f"  0x0082 ({len(pl)}B): {pl.hex()}")

    # Send sync and check
    gc.send(build_packet(0x0767))
    gc.send(build_packet(0x0769))
    time.sleep(2)
    while responses:
        op, pl = responses.pop(0)
        if op == 0x076A and len(pl) >= 2:
            log(f"  0x076A march sync ({len(pl)}B): {pl[:40].hex()}")
            # Try to parse: first byte might be active march count
            log(f"    byte[0] = {pl[0]} (active marches?)")
        elif op == 0x0768:
            log(f"  0x0768 sync response ({len(pl)}B): {pl.hex()}")
        elif op not in (0x0042, 0x036C, 0x0002):
            log(f"  Sync: 0x{op:04X} ({len(pl)}B)")

    # ──── 3. Setup ────
    log("\n=== 3. SETUP ===")
    gc.send(build_packet(0x0840))
    gc.send(build_packet(0x0245))
    data = struct.pack('<H', len(FORMATION_TROOPS))
    for tid in FORMATION_TROOPS:
        data += struct.pack('<I', tid)
    gc.send(build_packet(0x0834, data))
    gc.send(build_packet(0x0709))
    gc.send(build_packet(0x0A2C))
    drain("SETUP", timeout=2)

    # ──── 4. Search for resource tile ────
    log("\n=== 4. SEARCH RESOURCE ===")
    gc.send(build_packet(0x033E, bytes([0x01, 0x04, 0x00, 0x03])))
    time.sleep(3)
    target_x, target_y = None, None
    while responses:
        op, pl = responses.pop(0)
        if op == 0x033F and len(pl) >= 5:
            tx = struct.unpack('<H', pl[1:3])[0]
            ty = struct.unpack('<H', pl[3:5])[0]
            log(f"  Found resource: ({tx},{ty}) payload: {pl.hex()}")
            if target_x is None:
                target_x, target_y = tx, ty
        elif op not in (0x0042, 0x036C, 0x0002):
            log(f"  Search: 0x{op:04X} ({len(pl)}B)")
    if target_x is None:
        target_x, target_y = 650, 576
        log(f"  Using default: ({target_x},{target_y})")

    # ──── 5. ENABLE_VIEW + tiles + troops ────
    log("\n=== 5. VIEW + TROOPS ===")
    gc.send(build_enable_view(codec, IGG_ID, 0x01))
    gc.send(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 0x01)))
    time.sleep(1)
    gc.send(build_enable_view(codec, IGG_ID, 0x00))
    for tid in TROOP_IDS:
        gc.send(build_packet(0x099D, struct.pack('<I', tid)))
    gc.send(build_packet(0x0767))
    gc.send(build_packet(0x0769))
    time.sleep(2)
    gc.send(build_enable_view(codec, IGG_ID, 0x01))
    gc.send(build_packet(0x006E, struct.pack('<HHB', TURF_X, TURF_Y, 0x01)))
    time.sleep(1)
    gc.send(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 0x01)))
    drain("PRE-GATHER", timeout=2)

    # ──── 6. Try multiple march slots ────
    for slot in [1, 2, 3]:
        log(f"\n=== 6.{slot}. GATHER slot={slot} -> ({target_x},{target_y}) ===")
        ms = int((time.time() - gc.start_time) * 1000)
        gc.send(build_packet(0x0042, struct.pack('<II', ms, 0)))
        time.sleep(0.5)

        gc.send(build_gather_0ce8(codec, target_x, target_y, hero_id=255, march_slot=slot))

        r = drain(f"GATHER_SLOT{slot}", timeout=8)

        has_00b8 = any(op == 0x00B8 for op, _ in r)
        has_0071 = any(op == 0x0071 for op, _ in r)
        has_00b9 = any(op == 0x00B9 for op, _ in r)

        if has_0071:
            log(f"  >>> SLOT {slot}: MARCH CREATED! <<<")
            break
        elif has_00b8:
            log(f"  >>> SLOT {slot}: 0x00B8 received (format ok)")
            for op, pl in r:
                if op in (0x00B8, 0x00B9, 0x0033):
                    log(f"    Detail 0x{op:04X}: {pl.hex()}")
        else:
            log(f"  >>> SLOT {slot}: no response")

    # Wait for late
    time.sleep(8)
    late = []
    while responses:
        op, pl = responses.pop(0)
        if op not in (0x0042, 0x036C, 0x0002):
            late.append((op, pl))
    if late:
        log("\nLate responses:")
        for op, pl in late:
            log(f"  <- 0x{op:04X} ({len(pl)}B)")

    gc.disconnect()
    log("=== DONE ===")

if __name__ == '__main__':
    main()

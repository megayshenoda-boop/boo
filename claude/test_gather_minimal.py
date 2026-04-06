"""
MINIMAL gather test. Strip everything to essentials.
Try slot=1 (ALL PCAPs use slot=1).
Try with AND without 0x1B8B.
Try minimal sequence vs PCAP sequence.
"""
import sys, time, struct, subprocess, random
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from game_server import GameConnection
from codec import CMsgCodec
from packets import build_packet
from protocol import OP_ENABLE_VIEW, OP_START_MARCH

KINGDOM = 182
MARCH_TYPE = 0x1749
TURF_X, TURF_Y = 653, 567
TROOPS = [403, 405, 406, 407, 411]
FORMATION = [1025, 1046, 2014, 3002, 1035, 2008, 2019, 1009, 1024, 1016]

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def node_login():
    for i in range(3):
        result = subprocess.run(
            ['node', r'D:\CascadeProjects\lords_bot\http_login.mjs', EMAIL, PASSWORD, str(IGG_ID)],
            capture_output=True, text=True, timeout=30
        )
        key = result.stdout.strip()
        if len(key) == 32:
            return key
        time.sleep(5)
    return None

def build_gather(tile_x, tile_y, hero_id=255, slot=1):
    plain = bytearray(46)
    plain[0] = slot
    plain[1] = random.randint(0, 255)
    plain[2] = random.randint(0, 255)
    plain[3] = random.randint(0, 255)
    struct.pack_into('<H', plain, 4, MARCH_TYPE)
    struct.pack_into('<H', plain, 9, tile_x)
    struct.pack_into('<H', plain, 11, tile_y)
    plain[13] = 0x01
    plain[14] = hero_id & 0xFF
    plain[18] = KINGDOM
    plain[22] = 0x04
    struct.pack_into('<I', plain, 33, IGG_ID)
    return bytes(plain)


responses = []
def on_pkt(op, pl):
    responses.append((op, pl))

def collect(timeout=3):
    time.sleep(timeout)
    r = list(responses)
    responses.clear()
    return [(op, pl) for op, pl in r if op not in (0x0042, 0x036C, 0x0002)]

def show_gather_result(r):
    ops = [op for op, _ in r]
    log(f"  Got {len(r)} packets")
    for op, pl in r:
        if op in (0x00B8, 0x0071, 0x076C, 0x007C, 0x0033, 0x00B9, 0x0076, 0x0077, 0x0078, 0x0037):
            log(f"    0x{op:04X} ({len(pl)}B): {pl.hex()[:60]}")
    if 0x076C in ops:
        log("  >>> SUCCESS! 0x076C <<<")
    elif 0x0071 in ops:
        log("  >>> SUCCESS! 0x0071 <<<")
    elif 0x00B8 in ops:
        log("  >>> PARTIAL: 0x00B8 only <<<")
    else:
        log("  >>> NO RESPONSE <<<")
    return 0x076C in ops or 0x0071 in ops


def run_gather(label, slot=1, hero=255, do_setup=True, do_search=True):
    log(f"\n{'='*50}")
    log(f"TEST: {label} (slot={slot}, hero={hero})")
    log(f"{'='*50}")

    key = node_login()
    if not key:
        log("LOGIN FAILED"); return False

    gw = connect_gateway(IGG_ID, key, WORLD_ID)
    gc = GameConnection(IGG_ID, gw['ip'], gw['port'], gw['token'])
    gc.on_packet(on_pkt)
    gc.connect()
    if not gc.codec:
        log("NO CODEC"); gc.disconnect(); return False

    codec = gc.codec
    time.sleep(2)
    responses.clear()

    if do_setup:
        gc.send(build_packet(0x0840))
        gc.send(build_packet(0x0245))
        fdata = struct.pack('<H', len(FORMATION))
        for t in FORMATION:
            fdata += struct.pack('<I', t)
        gc.send(build_packet(0x0834, fdata))
        gc.send(build_packet(0x0709))
        gc.send(build_packet(0x0A2C))
        gc.send(build_packet(0x17A3, b'\x02\x00\x00\x00'))
        collect(1)

    # Troops
    for t in TROOPS:
        gc.send(build_packet(0x099D, struct.pack('<I', t)))

    # Sync
    gc.send(build_packet(0x0767))
    gc.send(build_packet(0x0769))

    # Prelude
    pdata = bytearray(10)
    pdata[0] = 0x01
    struct.pack_into('<I', pdata, 1, IGG_ID)
    pdata[9] = 0x01
    gc.send(codec.encode(OP_ENABLE_VIEW, bytes(pdata)))

    # Source tile
    gc.send(build_packet(0x006E, struct.pack('<HHB', TURF_X, TURF_Y, 1)))

    # Target tile
    target_x, target_y = None, None
    if do_search:
        gc.send(build_packet(0x033E, bytes([0x01, 0x04, 0x00, 0x03])))
        time.sleep(3)
        for op, pl in list(responses):
            if op == 0x033F and len(pl) >= 5:
                target_x = struct.unpack('<H', pl[1:3])[0]
                target_y = struct.unpack('<H', pl[3:5])[0]
                break
        responses.clear()

    if not target_x:
        target_x, target_y = 550, 851  # fallback from PCAP
    log(f"  Target: ({target_x},{target_y})")
    gc.send(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 1)))

    # Heartbeat + wait
    time.sleep(0.5)
    responses.clear()
    ms = int(time.time() * 1000) & 0xFFFFFFFF
    gc.send(build_packet(0x0042, struct.pack('<II', ms, 0)))
    time.sleep(2)
    responses.clear()

    # GATHER
    gather_plain = build_gather(target_x, target_y, hero_id=hero, slot=slot)
    log(f"  0x0CE8 plain: {gather_plain.hex()}")
    gc.send(codec.encode(OP_START_MARCH, gather_plain))
    r = collect(15)
    success = show_gather_result(r)

    # Late packets
    time.sleep(10)
    late = collect(1)
    if late:
        log(f"  Late packets: {len(late)}")
        for op, pl in late:
            if op in (0x0071, 0x076C):
                log(f"    LATE 0x{op:04X}!")
                success = True

    gc.disconnect()
    return success


def main():
    log("=== MINIMAL GATHER TESTS ===\n")

    # Test 1: slot=1, hero=255 (like ALL PCAPs)
    r1 = run_gather("slot=1, hero=255", slot=1, hero=255)
    time.sleep(5)

    # Test 2: slot=1, hero=244
    r2 = run_gather("slot=1, hero=244", slot=1, hero=244)
    time.sleep(5)

    # Test 3: slot=2, hero=255 (our previous tests)
    r3 = run_gather("slot=2, hero=255", slot=2, hero=255)

    log(f"\n{'='*50}")
    log("SUMMARY:")
    log(f"  slot=1, hero=255: {'SUCCESS' if r1 else 'FAIL'}")
    log(f"  slot=1, hero=244: {'SUCCESS' if r2 else 'FAIL'}")
    log(f"  slot=2, hero=255: {'SUCCESS' if r3 else 'FAIL'}")


if __name__ == '__main__':
    main()

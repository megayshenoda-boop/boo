"""
Gather Test v7 - v6 + 0x1B8B SESSION packet
The ONLY significant difference between our bot and the PCAP is 0x1B8B.
0x1B8B plaintext (18B) = seed(4B) + derived bytes from formula.
Encrypted with CMsgCodec using session server key.
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
TROOP_IDS = [403, 405, 407, 408, 409, 410, 411]
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

def build_1b8b_plain(seed32):
    """Build 0x1B8B plaintext (18B) from a 32-bit seed.
    Formula reverse-engineered from PCAP analysis across 7 sessions."""
    seed = seed32.to_bytes(4, 'little')
    x_lo = (seed[2] + 0x13) & 0xFF
    x_hi = (seed[3] - 0x02) & 0xFF
    x = x_lo | (x_hi << 8)
    mid = ((x_hi + 0x22) & 0xFF) << 8 | ((x_lo + 0x73) & 0xFF)
    y = ((x_hi - 0x01) & 0xFF) << 8 | ((x_lo - 0x01) & 0xFF)
    return seed + struct.pack('<H', mid) + struct.pack('<H', x) * 2 + struct.pack('<H', y) * 4

def build_1b8b_packet(codec, seed32=None):
    """Build 0x1B8B packet with manual CMsgCodec encoding.
    PCAP shows 0x1B8B uses CMsgCodec encryption but with a NON-STANDARD
    verify byte (not msg_lo^0xB7 like other encrypted packets).
    We manually encrypt to avoid the standard verify byte."""
    from protocol import CMSG_TABLE
    if seed32 is None:
        seed32 = random.getrandbits(32)
    plain = build_1b8b_plain(seed32)

    msg_lo = random.randint(0, 255)
    msg_hi = random.randint(0, 255)
    msg = [msg_lo, msg_hi]

    payload_len = 4 + len(plain)  # 4B codec header + 18B data
    total_len = 4 + payload_len   # 4B game header + payload
    pkt = bytearray(total_len)
    struct.pack_into('<H', pkt, 0, total_len)
    struct.pack_into('<H', pkt, 2, 0x1B8B)

    # Copy plaintext to encrypt position
    for j, b in enumerate(plain):
        pkt[8 + j] = b

    # Encrypt (same CMsgCodec algorithm)
    checksum = 0
    for i in range(8, total_len):
        table_b = CMSG_TABLE[i % 7]
        sk_b = codec.sk[i % 4]
        msg_b = msg[i % 2]
        intermediate = (pkt[i] + msg_b * 17) & 0xFF
        enc_byte = (intermediate ^ sk_b ^ table_b) & 0xFF
        pkt[i] = enc_byte
        checksum = (checksum + enc_byte) & 0xFFFFFFFF

    pkt[4] = checksum & 0xFF
    pkt[5] = msg_lo
    # Set verify byte to 0 (confirmed not to cause disconnect)
    pkt[6] = 0x00
    pkt[7] = msg_hi

    return bytes(pkt), seed32, plain

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
    data = bytearray(7)
    data[1] = march_slot & 0xFF
    data[3] = hero_id & 0xFF
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
    log("=== GATHER TEST v7 (v6 + 0x1B8B SESSION) ===")

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
    gc.send(build_packet(0x0840))
    gc.send(build_packet(0x17D4))
    gc.send(build_packet(0x0AF2))
    gc.send(build_packet(0x0245))
    fdata = struct.pack('<H', len(FORMATION_TROOPS))
    for tid in FORMATION_TROOPS:
        fdata += struct.pack('<I', tid)
    gc.send(build_packet(0x0834, fdata))
    gc.send(build_packet(0x0709))
    gc.send(build_packet(0x0A2C))
    gc.send(build_packet(0x1357, struct.pack('<I', 2)))
    gc.send(build_packet(0x170D, struct.pack('<I', 2)))
    drain("INIT", timeout=2)

    # Phase 1.5: 0x1B8B SESSION (CMsgCodec with verify=0)
    log("\n=== Phase 1.5: 0x1B8B SESSION ===")
    seed32 = random.getrandbits(32)
    plain_1b8b = build_1b8b_plain(seed32)
    pkt_1b8b, _, _ = build_1b8b_packet(codec, seed32)
    gc.send(pkt_1b8b)
    log(f"  0x1B8B sent! seed=0x{seed32:08x}, plain={plain_1b8b.hex()}")
    r1b8b = drain("1B8B", timeout=3)
    # Check for 0x1B8A
    for op, pl in r1b8b:
        if op == 0x1B8A:
            log(f"  Got 0x1B8A response: {pl.hex()}")

    # Phase 2: Skip timing - go straight to troops
    log("\n=== Phase 2: (skipping timing) ===")
    time.sleep(1)

    # Phase 3: Troop selection (7 troops)
    log("\n=== Phase 3: 7 Troops ===")
    for tid in TROOP_IDS:
        gc.send(build_packet(0x099D, struct.pack('<I', tid)))
    time.sleep(0.5)

    # Phase 4: Sync
    log("\n=== Phase 4: Sync ===")
    gc.send(build_packet(0x0767))
    gc.send(build_packet(0x0769))
    gc.send(build_packet(0x11FF, struct.pack('<I', 1)))
    time.sleep(1)

    # Phase 5: ENABLE_VIEW + view tile
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
            pass
    if target_x is None:
        target_x, target_y = 555, 853
        log(f"  Default target: ({target_x},{target_y})")

    drain("PRE-GATHER", timeout=1)

    # Phase 8: Target tile select
    log(f"\n=== Phase 8: Target tile ({target_x},{target_y}) ===")
    gc.send(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 0x01)))
    time.sleep(0.5)

    # Phase 9: 0x0323 PRE-GATHER
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

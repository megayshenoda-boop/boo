"""
Test ONLY 0x1B8B in isolation.
Try different encodings to find which one doesn't get us kicked.
"""
import sys, time, struct, subprocess, random
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from game_server import GameConnection
from codec import CMsgCodec
from packets import build_packet
from protocol import CMSG_TABLE

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
    seed = seed32.to_bytes(4, 'little')
    x_lo = (seed[2] + 0x13) & 0xFF
    x_hi = (seed[3] - 0x02) & 0xFF
    x = x_lo | (x_hi << 8)
    mid = ((x_hi + 0x22) & 0xFF) << 8 | ((x_lo + 0x73) & 0xFF)
    y = ((x_hi - 0x01) & 0xFF) << 8 | ((x_lo - 0x01) & 0xFF)
    return seed + struct.pack('<H', mid) + struct.pack('<H', x) * 2 + struct.pack('<H', y) * 4

def encode_1b8b_manual(sk_bytes, plain, msg_lo, msg_hi, verify_byte):
    """Manually encode 0x1B8B with full control over verify byte."""
    msg = [msg_lo, msg_hi]
    encrypted = bytearray(18)
    checksum = 0
    for j in range(18):
        i = j + 8  # position in full packet
        table_b = CMSG_TABLE[i % 7]
        sk_b = sk_bytes[i % 4]
        msg_b = msg[i % 2]
        intermediate = (plain[j] + msg_b * 17) & 0xFF
        enc_byte = (intermediate ^ sk_b ^ table_b) & 0xFF
        encrypted[j] = enc_byte
        checksum = (checksum + enc_byte) & 0xFFFFFFFF

    payload = bytearray(22)
    payload[0] = checksum & 0xFF
    payload[1] = msg_lo
    payload[2] = verify_byte
    payload[3] = msg_hi
    payload[4:] = encrypted
    return build_packet(0x1B8B, bytes(payload))

responses = []
def on_packet(opcode, payload):
    responses.append((opcode, payload))

def test_variant(name, pkt_1b8b):
    """Connect, send init + 0x1B8B variant, check if we survive."""
    log(f"\n{'='*60}")
    log(f"TEST: {name}")
    log(f"  Packet ({len(pkt_1b8b)}B): {pkt_1b8b.hex()}")

    access_key = node_login(EMAIL, PASSWORD, IGG_ID)
    if not access_key:
        log("Login failed!"); return False

    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    gc = GameConnection(IGG_ID, gw['ip'], gw['port'], gw['token'])
    gc.on_packet(on_packet)
    gc.connect()

    if not gc.codec:
        log("No codec!"); gc.disconnect(); return False

    codec = gc.codec
    sk = codec.sk
    time.sleep(2)
    responses.clear()

    # Send init
    gc.send(build_packet(0x0840))
    gc.send(build_packet(0x0245))
    fdata = struct.pack('<H', 10)
    for tid in [3002, 1035, 2008, 2019, 1009, 1024, 1016, 2009, 1025, 1046]:
        fdata += struct.pack('<I', tid)
    gc.send(build_packet(0x0834, fdata))
    gc.send(build_packet(0x0709))
    gc.send(build_packet(0x0A2C))
    time.sleep(1)
    responses.clear()

    # Send 0x1B8B
    try:
        gc.send(pkt_1b8b)
        log(f"  Sent OK!")
    except Exception as e:
        log(f"  Send FAILED: {e}")
        gc.disconnect()
        return False

    # Wait and check if connection survives
    time.sleep(3)

    # Try sending heartbeat to test connection
    try:
        ms = int((time.time() - gc.start_time) * 1000)
        gc.send(build_packet(0x0042, struct.pack('<II', ms, 0)))
        log(f"  Heartbeat after 1B8B: OK")
    except Exception as e:
        log(f"  Heartbeat FAILED (kicked): {e}")
        gc.disconnect()
        return False

    # Check responses
    time.sleep(2)
    got_1b8a = False
    while responses:
        op, pl = responses.pop(0)
        if op == 0x1B8A:
            got_1b8a = True
            log(f"  Got 0x1B8A response ({len(pl)}B): {pl.hex()}")
        elif op not in (0x0042, 0x036C, 0x0002):
            log(f"  Got 0x{op:04X} ({len(pl)}B)")

    log(f"  0x1B8A response: {'YES' if got_1b8a else 'NO'}")
    log(f"  Connection alive: {gc.connected}")

    # Try troop selection to really confirm
    try:
        gc.send(build_packet(0x099D, struct.pack('<I', 403)))
        time.sleep(1)
        gc.send(build_packet(0x099D, struct.pack('<I', 405)))
        log(f"  Troop select: OK - CONNECTION SURVIVED!")
        survived = True
    except Exception as e:
        log(f"  Troop select FAILED: {e}")
        survived = False

    gc.disconnect()
    return survived


def main():
    log("=== 0x1B8B VARIANT TESTING ===")

    # First, just test WITHOUT 0x1B8B (sanity check)
    log("\n--- Variant 0: No 0x1B8B (control) ---")
    access_key = node_login(EMAIL, PASSWORD, IGG_ID)
    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    gc = GameConnection(IGG_ID, gw['ip'], gw['port'], gw['token'])
    gc.on_packet(on_packet)
    gc.connect()
    codec = gc.codec
    sk = codec.sk
    time.sleep(2); responses.clear()
    gc.send(build_packet(0x0840))
    gc.send(build_packet(0x0245))
    fdata = struct.pack('<H', 10)
    for tid in [3002, 1035, 2008, 2019, 1009, 1024, 1016, 2009, 1025, 1046]:
        fdata += struct.pack('<I', tid)
    gc.send(build_packet(0x0834, fdata))
    gc.send(build_packet(0x0709))
    gc.send(build_packet(0x0A2C))
    time.sleep(2)
    try:
        gc.send(build_packet(0x099D, struct.pack('<I', 403)))
        time.sleep(1)
        gc.send(build_packet(0x099D, struct.pack('<I', 405)))
        log("  Control (no 1B8B): ALIVE")
    except Exception as e:
        log(f"  Control FAILED: {e}")
    gc.disconnect()

    # Get a fresh connection for the test variants
    seed32 = random.getrandbits(32)
    plain = build_1b8b_plain(seed32)
    log(f"\nPlaintext seed=0x{seed32:08x}: {plain.hex()}")

    # Variant 1: Standard CMsgCodec (verify = msg_lo ^ 0xB7)
    access_key = node_login(EMAIL, PASSWORD, IGG_ID)
    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    gc = GameConnection(IGG_ID, gw['ip'], gw['port'], gw['token'])
    gc.connect()
    sk = gc.codec.sk
    gc.disconnect()
    time.sleep(1)

    msg_lo = random.randint(0, 255)
    msg_hi = random.randint(0, 255)

    pkt1 = encode_1b8b_manual(sk, plain, msg_lo, msg_hi, msg_lo ^ 0xB7)
    test_variant("Standard verify (lo^B7)", pkt1)

    # Variant 2: verify = 0
    pkt2 = encode_1b8b_manual(sk, plain, msg_lo, msg_hi, 0x00)
    test_variant("Verify = 0x00", pkt2)

    # Variant 3: Use codec.encode directly
    access_key = node_login(EMAIL, PASSWORD, IGG_ID)
    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    gc = GameConnection(IGG_ID, gw['ip'], gw['port'], gw['token'])
    gc.connect()
    pkt3 = gc.codec.encode(0x1B8B, plain)
    gc.disconnect()
    time.sleep(1)
    test_variant("codec.encode()", pkt3)

    # Variant 4: Send just 22 bytes of zeros as payload
    pkt4 = build_packet(0x1B8B, bytes(22))
    test_variant("22B zeros payload", pkt4)

    # Variant 5: send ONLY the 18B plaintext (no codec, short packet)
    pkt5 = build_packet(0x1B8B, plain)
    test_variant("18B raw plaintext", pkt5)

    log("\n=== DONE ===")


if __name__ == '__main__':
    main()

"""
Test 0x1B8B variants - each variant gets its own fresh connection.
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

def encode_1b8b_custom(sk_list, plain, verify_byte=None):
    """Encode 0x1B8B with CMsgCodec but custom verify byte."""
    msg_lo = random.randint(0, 255)
    msg_hi = random.randint(0, 255)
    msg = [msg_lo, msg_hi]

    encrypted = bytearray(len(plain))
    checksum = 0
    for j in range(len(plain)):
        i = j + 8
        table_b = CMSG_TABLE[i % 7]
        sk_b = sk_list[i % 4]
        msg_b = msg[i % 2]
        intermediate = (plain[j] + msg_b * 17) & 0xFF
        enc_byte = (intermediate ^ sk_b ^ table_b) & 0xFF
        encrypted[j] = enc_byte
        checksum = (checksum + enc_byte) & 0xFFFFFFFF

    payload = bytearray(4 + len(plain))
    payload[0] = checksum & 0xFF
    payload[1] = msg_lo
    payload[2] = verify_byte if verify_byte is not None else (msg_lo ^ 0xB7)
    payload[3] = msg_hi
    payload[4:] = encrypted
    return build_packet(0x1B8B, bytes(payload))

responses = []
def on_packet(opcode, payload):
    responses.append((opcode, payload))

def do_test(variant_name, build_1b8b_fn):
    """
    Fresh connection -> send init -> build_1b8b_fn(codec) -> send -> check survival.
    build_1b8b_fn receives (codec_sk_list) and returns packet bytes, or None to skip 0x1B8B.
    """
    log(f"\n{'='*60}")
    log(f"TEST: {variant_name}")

    for attempt in range(3):
        access_key = node_login(EMAIL, PASSWORD, IGG_ID)
        if access_key:
            break
        time.sleep(2)
    if not access_key:
        log("  Login failed after 3 attempts"); return None

    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    gc = GameConnection(IGG_ID, gw['ip'], gw['port'], gw['token'])
    gc.on_packet(on_packet)
    gc.connect()

    if not gc.codec:
        log("  No codec!"); gc.disconnect(); return None

    sk = gc.codec.sk
    time.sleep(2)
    responses.clear()

    # Init packets
    gc.send(build_packet(0x0840))
    gc.send(build_packet(0x0245))
    fdata = struct.pack('<H', 10)
    for tid in [3002, 1035, 2008, 2019, 1009, 1024, 1016, 2009, 1025, 1046]:
        fdata += struct.pack('<I', tid)
    gc.send(build_packet(0x0834, fdata))
    gc.send(build_packet(0x0709))
    gc.send(build_packet(0x0A2C))
    time.sleep(1.5)
    responses.clear()

    # Build and send 0x1B8B
    pkt = build_1b8b_fn(sk)
    if pkt is not None:
        try:
            gc.send(pkt)
            log(f"  Sent 0x1B8B ({len(pkt)}B): {pkt.hex()}")
        except Exception as e:
            log(f"  Send FAILED: {e}")
            gc.disconnect(); return False
    else:
        log("  Skipped 0x1B8B")

    # Wait for response
    time.sleep(4)

    # Check responses
    got_1b8a = False
    for op, pl in responses:
        if op == 0x1B8A:
            got_1b8a = True
            log(f"  Got 0x1B8A ({len(pl)}B): {pl.hex()}")
    responses.clear()

    # Test if connection is alive
    survived = False
    try:
        gc.send(build_packet(0x099D, struct.pack('<I', 403)))
        time.sleep(1)
        gc.send(build_packet(0x099D, struct.pack('<I', 405)))
        time.sleep(0.5)
        log(f"  Post-1B8B troop select: OK")
        survived = True
    except Exception as e:
        log(f"  KICKED! {e}")
        survived = False

    result = "SURVIVED" if survived else "KICKED"
    log(f"  1B8A={'YES' if got_1b8a else 'NO'}  Result: {result}")
    gc.disconnect()
    time.sleep(2)
    return survived


def main():
    log("=== 0x1B8B VARIANT TESTING ===")

    seed32 = random.getrandbits(32)
    plain = build_1b8b_plain(seed32)
    log(f"Plaintext seed=0x{seed32:08x}: {plain.hex()}")

    results = {}

    # 0: Control - no 0x1B8B
    results['no_1b8b'] = do_test("Control: No 0x1B8B", lambda sk: None)

    # 1: Standard CMsgCodec (verify = msg_lo ^ 0xB7)
    results['std_verify'] = do_test("Standard CMsgCodec (lo^B7)",
        lambda sk: encode_1b8b_custom(sk, plain, verify_byte=None))

    # 2: verify = 0x00
    results['ver_00'] = do_test("Verify byte = 0x00",
        lambda sk: encode_1b8b_custom(sk, plain, verify_byte=0x00))

    # 3: verify = random
    results['ver_rand'] = do_test("Verify byte = random",
        lambda sk: encode_1b8b_custom(sk, plain, verify_byte=random.randint(0, 255)))

    # 4: codec.encode directly (same as #1 but using the class method)
    def codec_encode_test(sk):
        codec = CMsgCodec(sk)
        return codec.encode(0x1B8B, plain)
    results['codec_encode'] = do_test("codec.encode() direct", codec_encode_test)

    # 5: All-zeros 22B payload
    results['zeros_22'] = do_test("22B zeros payload",
        lambda sk: build_packet(0x1B8B, bytes(22)))

    # 6: Raw 18B plaintext (wrong size)
    results['raw_18'] = do_test("Raw 18B plaintext",
        lambda sk: build_packet(0x1B8B, plain))

    # Summary
    log(f"\n{'='*60}")
    log("SUMMARY:")
    for name, result in results.items():
        status = "SURVIVED" if result == True else "KICKED" if result == False else "ERROR"
        log(f"  {name:20s} -> {status}")

if __name__ == '__main__':
    main()

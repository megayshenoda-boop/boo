"""
Test 0x1B8B with different verify bytes.
Goal: find which verify byte values DON'T cause server disconnect.

Approach:
1. Login
2. Send setup packets
3. Send 0x1B8B with specific verify byte
4. Wait 8 seconds - if still connected, verify byte is accepted
5. Try sending heartbeat to confirm connection is alive
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

def build_1b8b_plain(seed32=None):
    """Build 0x1B8B plaintext using verified formula."""
    if seed32 is None:
        seed32 = random.getrandbits(32)
    seed = seed32.to_bytes(4, 'little')
    x_lo = (seed[2] + 0x13) & 0xFF
    x_hi = (seed[3] - 0x02) & 0xFF
    x = x_lo | (x_hi << 8)
    mid = ((x_hi + 0x22) & 0xFF) << 8 | ((x_lo + 0x73) & 0xFF)
    y = ((x_hi - 0x01) & 0xFF) << 8 | ((x_lo - 0x01) & 0xFF)
    return struct.pack('<I', seed32) + struct.pack('<H', mid) + struct.pack('<H', x) * 2 + struct.pack('<H', y) * 4

def build_1b8b_with_verify(codec, verify_byte):
    """Build 0x1B8B packet using standard codec, then patch verify byte."""
    plain = build_1b8b_plain()
    # Use codec.encode to get correctly encrypted packet
    pkt = bytearray(codec.encode(0x1B8B, plain))
    # Patch verify byte at offset 6 (game header[4] + codec header: ck[0], ml[1], verify[2])
    # Full packet: [0:2]=len, [2:4]=opcode, [4]=checksum, [5]=msg_lo, [6]=verify, [7]=msg_hi, [8:]=enc
    old_verify = pkt[6]
    pkt[6] = verify_byte & 0xFF
    return bytes(pkt), plain, old_verify

def test_verify(verify_mode, verify_value=None, delay=10):
    """Test a specific verify byte. Returns True if connection survives."""
    log(f"\n--- Testing verify={verify_mode} ---")

    for attempt in range(3):
        access_key = node_login(EMAIL, PASSWORD, IGG_ID)
        if access_key:
            break
        log(f"  Login attempt {attempt+1} failed, retrying...")
        time.sleep(5)
    else:
        log("  Login failed after 3 attempts")
        return None

    responses = []
    disconnected = [False]

    def on_packet(opcode, payload):
        responses.append((opcode, payload))

    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    gc = GameConnection(IGG_ID, gw['ip'], gw['port'], gw['token'])
    gc.on_packet(on_packet)
    gc.connect()

    if not gc.codec:
        log("  No codec!")
        gc.disconnect()
        return None

    codec = gc.codec
    time.sleep(2)
    responses.clear()

    # Send setup packets (like PCAPs)
    gc.send(build_packet(0x0840))
    gc.send(build_packet(0x0245))
    fdata = struct.pack('<H', 10)
    for tid in [1025, 1046, 2014, 3002, 1035, 2008, 2019, 1009, 1024, 1016]:
        fdata += struct.pack('<I', tid)
    gc.send(build_packet(0x0834, fdata))
    gc.send(build_packet(0x0709))
    gc.send(build_packet(0x0A2C))
    gc.send(build_packet(0x17A3, b'\x02\x00\x00\x00'))
    time.sleep(0.5)

    # Now send 0x1B8B
    if verify_mode == 'standard':
        pkt = codec.encode(0x1B8B, build_1b8b_plain())
        log(f"  Sent 0x1B8B standard verify (msg_lo^0xB7)")
    elif verify_mode == 'value':
        pkt, plain, old_v = build_1b8b_with_verify(codec, verify_value)
        log(f"  Sent 0x1B8B verify=0x{verify_value:02X} (was 0x{old_v:02X})")
    elif verify_mode == 'skip':
        pkt = None
        log(f"  Skipping 0x1B8B (control)")

    if pkt:
        gc.send(pkt)

    # Wait and check if we get disconnected
    log(f"  Waiting {delay}s...")
    time.sleep(delay)

    alive = gc.connected

    # Try heartbeat to confirm
    if alive:
        try:
            ms = int(time.time() * 1000) & 0xFFFFFFFF
            gc.send(build_packet(0x0042, struct.pack('<II', ms, 0)))
            time.sleep(2)
            got_hb = any(op == 0x0042 for op, _ in responses)
            log(f"  Heartbeat echo: {'YES' if got_hb else 'no'}")
        except:
            alive = False

    # Check for 0x1B8A response
    got_1b8a = any(op == 0x1B8A for op, _ in responses)

    result = "ALIVE" if alive else "DISCONNECTED"
    log(f"  Result: {result} | 0x1B8A response: {'YES' if got_1b8a else 'no'}")

    gc.disconnect()
    return alive


def main():
    log("=== 0x1B8B VERIFY BYTE TEST ===\n")

    results = {}

    # Test 1: Control - no 0x1B8B
    r = test_verify('skip')
    results['skip'] = r
    time.sleep(3)

    # Test 2: Standard verify (msg_lo^0xB7) - expected to fail
    r = test_verify('standard')
    results['standard'] = r
    time.sleep(3)

    # Test 3-7: Try specific verify bytes
    for v in [0x00, 0x01, 0xFF, 0xB7, 0x42]:
        r = test_verify('value', v)
        results[f'0x{v:02X}'] = r
        time.sleep(3)

    log(f"\n\n{'='*50}")
    log("RESULTS SUMMARY:")
    for name, r in results.items():
        status = "ALIVE" if r else ("DISCONNECTED" if r is False else "ERROR")
        log(f"  {name:>12}: {status}")
    log(f"{'='*50}")


if __name__ == '__main__':
    main()

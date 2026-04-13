#!/usr/bin/env python3
"""
Debug 0x1B8B disconnect - test multiple hypotheses:
1. Maybe extra bytes [4:5] must be specific values (not random)
2. Maybe 0x1B8B must be sent IMMEDIATELY (no delay)
3. Maybe the S2C 0x1B8A is encrypted and gate=0 means DON'T send
4. Maybe the plaintext checkId should be 0 instead of IGG_ID
5. Maybe use standard Encode instead of NewEncode

Tests each hypothesis in sequence, checking alive after each.
"""
import sys, time, struct, random, subprocess, socket, os
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from codec import CMsgCodec
from packets import build_packet, build_game_login, build_world_entry, recv_packet
from game_state import GameState

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def node_login():
    for attempt in range(3):
        try:
            result = subprocess.run(
                ['node', r'D:\CascadeProjects\lords_bot\http_login.mjs', EMAIL, PASSWORD, str(IGG_ID)],
                capture_output=True, text=True, timeout=30
            )
            key = result.stdout.strip()
            if len(key) == 32: return key
        except: pass
        if attempt < 2: time.sleep(3)
    return None

def recv_flood(sock, timeout=3):
    packets = []
    deadline = time.time() + timeout
    while time.time() < deadline:
        sock.settimeout(max(0.1, deadline - time.time()))
        try:
            header = b''
            while len(header) < 4:
                chunk = sock.recv(4 - len(header))
                if not chunk: return packets
                header += chunk
            pkt_len, opcode = struct.unpack('<HH', header)
            payload_len = pkt_len - 4
            if payload_len < 0 or payload_len > 100000: return packets
            payload = b''
            while len(payload) < payload_len:
                chunk = sock.recv(payload_len - len(payload))
                if not chunk: return packets
                payload += chunk
            packets.append((opcode, payload))
        except socket.timeout: break
        except: break
    return packets

def check_alive(sock):
    try:
        ms = int(time.time() * 1000) & 0xFFFFFFFF
        sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
        time.sleep(1.5)
        resp = recv_flood(sock, timeout=2)
        return len(resp) > 0
    except:
        return False

def connect_and_init():
    """Login, connect, get init flood, return (sock, codec, init_pkts, server_key)."""
    access_key = node_login()
    if not access_key: return None
    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((gw['ip'], gw['port']))
    sock.sendall(build_game_login(IGG_ID, gw['token']))
    r = recv_packet(sock, timeout=10)
    if r is None or r[0] != 0x0020:
        sock.close(); return None
    sock.sendall(build_world_entry(IGG_ID))
    init_pkts = recv_flood(sock, timeout=6)
    gs = GameState()
    for op, pl in init_pkts: gs.update(op, pl)
    if gs.server_key is None:
        for op in [0x0840, 0x17D4, 0x0709]: sock.sendall(build_packet(op))
        more = recv_flood(sock, timeout=4)
        for op, pl in more:
            gs.update(op, pl)
            init_pkts.append((op, pl))
    if gs.server_key is None:
        sock.close(); return None
    codec = CMsgCodec.from_u32(gs.server_key)
    return sock, codec, init_pkts, gs.server_key

CMSG_TABLE = [0x58, 0xEF, 0xD7, 0x14, 0xA2, 0x3B, 0x9C]

def test_variant(label, sock, codec, server_key, build_fn):
    """Send a 0x1B8B variant and check if we're still alive."""
    log(f"  [{label}] Building packet...")
    pkt = build_fn(codec, server_key)
    log(f"  [{label}] Sending ({len(pkt)}B): {pkt.hex()}")
    try:
        sock.sendall(pkt)
    except Exception as e:
        log(f"  [{label}] Send FAILED: {e}")
        return False
    time.sleep(1)
    resp = recv_flood(sock, timeout=2)
    log(f"  [{label}] Response: {len(resp)} packets")
    for op, pl in resp:
        log(f"    {op:#06x} ({len(pl)}B): {pl[:20].hex()}")
    alive = check_alive(sock)
    log(f"  [{label}] Alive: {alive}")
    return alive

def main():
    log("=== 0x1B8B DEBUG - Testing Multiple Hypotheses ===")
    log(f"IGG_ID = {IGG_ID} (0x{IGG_ID:08X})")

    PLAIN_IGGID = bytes.fromhex("ed02732200000000ffffffffffffffff")  # checkId=IGG_ID
    PLAIN_ZERO  = bytes(8) + bytes.fromhex("ffffffffffffffff")        # checkId=0
    PLAIN_ALL_FF= bytes.fromhex("ffffffffffffffffffffffffffffffff")   # all -1

    variants = [
        # 1: NewEncode + correct plaintext + extra=0x0000 (not random)
        ("NewEnc+extra0000", lambda c, sk: c.encode_offset6(0x1B8B, PLAIN_IGGID, extra=b'\x00\x00')),
        # 2: NewEncode + correct plaintext + extra=0x000D (LCG step 1 from seed=0)
        ("NewEnc+extra000D", lambda c, sk: c.encode_offset6(0x1B8B, PLAIN_IGGID, extra=b'\x0d\x00')),
        # 3: NewEncode + checkId=0 instead of IGG_ID
        ("NewEnc+checkId0", lambda c, sk: c.encode_offset6(0x1B8B, PLAIN_ZERO)),
        # 4: NewEncode + all FF plaintext
        ("NewEnc+allFF", lambda c, sk: c.encode_offset6(0x1B8B, PLAIN_ALL_FF)),
        # 5: Standard Encode with 18B plaintext (old theory)
        ("StdEnc+18B", lambda c, sk: c.encode(0x1B8B, PLAIN_IGGID + b'\x00\x00')),
        # 6: Standard Encode with 16B plaintext
        ("StdEnc+16B", lambda c, sk: c.encode(0x1B8B, PLAIN_IGGID)),
        # 7: Completely empty payload (just header)
        ("Empty4B", lambda c, sk: struct.pack('<HH', 4, 0x1B8B)),
        # 8: Raw unencrypted (len+opcode+plaintext)
        ("RawPlain", lambda c, sk: struct.pack('<HH', 4 + len(PLAIN_IGGID), 0x1B8B) + PLAIN_IGGID),
    ]

    results = {}
    for i, (label, build_fn) in enumerate(variants):
        log(f"\n{'='*60}")
        log(f"  VARIANT {i+1}/{len(variants)}: {label}")
        log(f"{'='*60}")

        conn = connect_and_init()
        if conn is None:
            log(f"  [{label}] Connection FAILED!")
            results[label] = "conn_fail"
            time.sleep(3)
            continue
        sock, codec, init_pkts, sk = conn

        log(f"  [{label}] SK=0x{sk:08X}")

        # Verify alive before sending
        alive_before = check_alive(sock)
        if not alive_before:
            log(f"  [{label}] Dead BEFORE sending!")
            results[label] = "dead_before"
            sock.close()
            time.sleep(3)
            continue

        alive_after = test_variant(label, sock, codec, sk, build_fn)
        results[label] = "ALIVE" if alive_after else "DISCONNECT"
        sock.close()
        time.sleep(3)

    # ═══════════════════════════════════════════════════════════
    log(f"\n{'='*60}")
    log(f"  RESULTS SUMMARY")
    log(f"{'='*60}")
    for label, status in results.items():
        marker = "✓" if status == "ALIVE" else "✗"
        log(f"  {marker} {label:30s} → {status}")
    log(f"{'='*60}")

if __name__ == '__main__':
    main()

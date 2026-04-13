#!/usr/bin/env python3
"""
Raw gather debug - test multiple hypotheses:
1. Does 0x0CEB actually need encryption? (send plain vs encrypted)
2. Do we get tile responses even WITHOUT 0x0CEB?
3. Does the server respond to ANY 0x0CE8? (correct vs wrong SK)
4. Does the OLD march opcode (0x0072) work?
5. Log EVERY SINGLE PACKET with full hex for 30s after gather
"""
import sys, time, struct, random, subprocess, socket, os
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from codec import CMsgCodec
from packets import build_packet, build_game_login, build_world_entry, recv_packet
from protocol import opname, OP_START_MARCH
from game_state import GameState

KINGDOM = 182
FORMATION_DATA = bytes.fromhex("0900ba0b00000b040000d8070000e3070000f103000000040000f8030000d907000001040000")

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

def connect_session():
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
        for op, pl in more: gs.update(op, pl)
    if gs.server_key is None:
        sock.close(); return None
    codec = CMsgCodec.from_u32(gs.server_key)
    # Setup
    sock.sendall(build_packet(0x0840))
    time.sleep(0.15)
    sock.sendall(build_packet(0x17D4))
    time.sleep(0.05)
    sock.sendall(build_packet(0x0AF2))
    time.sleep(0.15)
    sock.sendall(build_packet(0x0245))
    sock.sendall(build_packet(0x0834, FORMATION_DATA))
    time.sleep(0.25)
    sock.sendall(build_packet(0x0709))
    time.sleep(0.05)
    sock.sendall(build_packet(0x0A2C))
    time.sleep(0.5)
    recv_flood(sock, timeout=3)
    return sock, codec, gs.server_key

def build_gather_plain(tx, ty):
    p = bytearray(46)
    p[0] = 1
    p[1:4] = os.urandom(3)
    struct.pack_into('<H', p, 4, 0x1749)
    struct.pack_into('<H', p, 9, tx)
    struct.pack_into('<H', p, 11, ty)
    p[13] = 0x01
    p[14] = 0xFF
    p[18] = KINGDOM & 0xFF
    p[22] = 0x04
    struct.pack_into('<I', p, 33, IGG_ID)
    return bytes(p)

def wait_and_log(sock, label, seconds=15):
    """Log ALL packets received for N seconds."""
    log(f"  [{label}] Listening for {seconds}s...")
    unique_ops = {}
    deadline = time.time() + seconds
    hb_count = 0
    while time.time() < deadline:
        pkts = recv_flood(sock, timeout=3)
        for op, pl in pkts:
            if op == 0x0042:
                hb_count += 1
                continue
            if op == 0x036C:
                continue
            unique_ops[op] = unique_ops.get(op, 0) + 1
            if op in (0x026D,):  # skip chat spam
                continue
            log(f"    0x{op:04X} ({len(pl)}B): {pl[:40].hex() if pl else '(empty)'}")
        # Keep alive
        ms = int(time.time() * 1000) & 0xFFFFFFFF
        try:
            sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
        except:
            log(f"  [{label}] Connection lost!")
            return unique_ops
    log(f"  [{label}] Done. Heartbeats={hb_count}, Unique ops: {dict(sorted(unique_ops.items()))}")
    return unique_ops

def main():
    log("=== RAW GATHER DEBUG ===")

    # ══════════════════════════════════════════════════════
    # TEST 1: Send 0x0CE8 encrypted (baseline)
    # ══════════════════════════════════════════════════════
    log("\n" + "="*60)
    log("TEST 1: Encrypted 0x0CE8 (baseline)")
    log("="*60)
    
    conn = connect_session()
    if conn is None:
        log("Connection failed!"); return
    sock, codec, sk = conn
    log(f"SK=0x{sk:08X}")

    # Search for tile
    sock.sendall(build_packet(0x033E, bytes.fromhex("01040003")))
    time.sleep(2)
    pkts = recv_flood(sock, timeout=3)
    tx, ty = 570, 805  # fallback
    for op, pl in pkts:
        if op == 0x033F and len(pl) >= 5:
            tx = struct.unpack('<H', pl[1:3])[0]
            ty = struct.unpack('<H', pl[3:5])[0]
    log(f"Target: ({tx},{ty})")

    # Send encrypted gather
    gather_pkt = codec.encode(OP_START_MARCH, build_gather_plain(tx, ty))
    log(f"Sending encrypted 0x0CE8 ({len(gather_pkt)}B)")
    sock.sendall(gather_pkt)
    ops1 = wait_and_log(sock, "encrypted", seconds=15)
    sock.close()
    time.sleep(3)

    # ══════════════════════════════════════════════════════
    # TEST 2: Send 0x0CE8 with WRONG server key (garbage decrypt)
    # ══════════════════════════════════════════════════════
    log("\n" + "="*60)
    log("TEST 2: 0x0CE8 with WRONG key (should fail checksum)")
    log("="*60)
    
    conn = connect_session()
    if conn is None:
        log("Connection failed!"); return
    sock, codec, sk = conn
    log(f"SK=0x{sk:08X}")

    # Use wrong key to encode
    wrong_codec = CMsgCodec.from_u32(sk ^ 0xDEADBEEF)
    gather_pkt2 = wrong_codec.encode(OP_START_MARCH, build_gather_plain(tx, ty))
    log(f"Sending WRONG-KEY 0x0CE8 ({len(gather_pkt2)}B)")
    sock.sendall(gather_pkt2)
    ops2 = wait_and_log(sock, "wrong_key", seconds=15)
    sock.close()
    time.sleep(3)

    # ══════════════════════════════════════════════════════
    # TEST 3: Send 0x0CE8 as PLAIN (no encryption)
    # ══════════════════════════════════════════════════════
    log("\n" + "="*60)
    log("TEST 3: 0x0CE8 PLAIN (no encryption)")
    log("="*60)
    
    conn = connect_session()
    if conn is None:
        log("Connection failed!"); return
    sock, codec, sk = conn
    log(f"SK=0x{sk:08X}")

    plain_gather = build_gather_plain(tx, ty)
    raw_pkt = struct.pack('<HH', 4 + len(plain_gather), OP_START_MARCH) + plain_gather
    log(f"Sending PLAIN 0x0CE8 ({len(raw_pkt)}B)")
    sock.sendall(raw_pkt)
    ops3 = wait_and_log(sock, "plain", seconds=15)
    sock.close()
    time.sleep(3)

    # ══════════════════════════════════════════════════════
    # TEST 4: Send OLD march 0x0072 encrypted
    # ══════════════════════════════════════════════════════
    log("\n" + "="*60)
    log("TEST 4: OLD march 0x0072 encrypted")
    log("="*60)
    
    conn = connect_session()
    if conn is None:
        log("Connection failed!"); return
    sock, codec, sk = conn
    log(f"SK=0x{sk:08X}")

    # Old march with same plaintext
    old_pkt = codec.encode(0x0072, build_gather_plain(tx, ty))
    log(f"Sending encrypted OLD 0x0072 ({len(old_pkt)}B)")
    sock.sendall(old_pkt)
    ops4 = wait_and_log(sock, "old_march", seconds=15)
    sock.close()
    time.sleep(3)

    # ══════════════════════════════════════════════════════
    # TEST 5: Send 0x0CE8 encrypted TWICE 
    # ══════════════════════════════════════════════════════
    log("\n" + "="*60)
    log("TEST 5: Send 0x0CE8 TWICE (different msg values)")
    log("="*60)
    
    conn = connect_session()
    if conn is None:
        log("Connection failed!"); return
    sock, codec, sk = conn
    log(f"SK=0x{sk:08X}")

    for i in range(3):
        pkt = codec.encode(OP_START_MARCH, build_gather_plain(tx, ty))
        log(f"  Attempt {i+1}: msg_lo=0x{pkt[5]:02X} msg_hi=0x{pkt[7]:02X}")
        sock.sendall(pkt)
        time.sleep(2)
        pkts = recv_flood(sock, timeout=3)
        for op, pl in pkts:
            if op not in (0x0042, 0x036C, 0x026D):
                log(f"    → 0x{op:04X} ({len(pl)}B): {pl[:30].hex()}")
    ops5 = wait_and_log(sock, "multi", seconds=10)
    sock.close()

    # ══════════════════════════════════════════════════════
    log("\n" + "="*60)
    log("SUMMARY")
    log("="*60)
    tests = [
        ("Encrypted correct", ops1),
        ("Wrong key", ops2),
        ("Plain (no enc)", ops3),
        ("Old 0x0072", ops4),
        ("Multi-send", ops5),
    ]
    for name, ops in tests:
        march = any(o in ops for o in (0x0071, 0x076C, 0x00B8))
        error = 0x0037 in ops
        response = 0x0079 in ops or 0x0267 in ops
        non_noise = {k: v for k, v in ops.items() if k not in (0x0042, 0x036C, 0x026D, 0x0032, 0x0033, 0x0002)}
        log(f"  {name:25s} march={march} error={error} resp={response} ops={dict(sorted(non_noise.items()))}")

if __name__ == '__main__':
    main()

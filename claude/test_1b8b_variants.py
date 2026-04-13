#!/usr/bin/env python3
"""
0x1B8B Encoding Variants Test
==============================
Tests multiple encoding approaches for 0x1B8B:
A) offset6 (NewEncode) - matches PCAPs byte-perfect
B) standard encode - maybe server changed?
C) offset6 with setup packets in EXACT PCAP order
D) No 0x1B8B (control) - should stay connected

Also captures raw disconnect data to understand WHY the server drops us.
"""
import sys, time, struct, random, subprocess, socket, os, select
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from codec import CMsgCodec
from packets import build_packet, build_game_login, build_world_entry, recv_packet
from protocol import opname
from game_state import GameState

PASSWORD_CHECK_PLAIN = bytes.fromhex("ed02732200000000ffffffffffffffff")
FORMATION_DATA = bytes.fromhex("0900ba0b00000b040000d8070000e3070000f103000000040000f8030000d907000001040000")

def log(msg):
    ts = time.time()
    ms = int((ts % 1) * 1000)
    print(f"[{time.strftime('%H:%M:%S')}.{ms:03d}] {msg}")

def node_login():
    for attempt in range(3):
        try:
            result = subprocess.run(
                ['node', r'D:\CascadeProjects\lords_bot\http_login.mjs', EMAIL, PASSWORD, str(IGG_ID)],
                capture_output=True, text=True, timeout=30, encoding='utf-8', errors='replace'
            )
            key = result.stdout.strip()
            if len(key) == 32: return key
        except: pass
        if attempt < 2: time.sleep(3)
    return None

def recv_one(sock, timeout=5):
    sock.settimeout(timeout)
    try:
        header = b''
        while len(header) < 4:
            chunk = sock.recv(4 - len(header))
            if not chunk: return None
            header += chunk
        pkt_len, opcode = struct.unpack('<HH', header)
        pl_len = pkt_len - 4
        if pl_len < 0 or pl_len > 100000: return None
        payload = b''
        while len(payload) < pl_len:
            chunk = sock.recv(pl_len - len(payload))
            if not chunk: return None
            payload += chunk
        return (opcode, payload)
    except: return None

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
            pl_len = pkt_len - 4
            if pl_len < 0 or pl_len > 100000: return packets
            payload = b''
            while len(payload) < pl_len:
                chunk = sock.recv(pl_len - len(payload))
                if not chunk: return packets
                payload += chunk
            packets.append((opcode, payload))
        except socket.timeout: break
        except: break
    return packets

def recv_raw(sock, timeout=3):
    """Read raw bytes to catch any disconnect data."""
    sock.settimeout(timeout)
    try:
        data = sock.recv(4096)
        return data
    except:
        return b''

def run_variant(label, encode_fn, setup_before=False):
    """
    Connect, login, optionally send setup, send 0x1B8B variant, check alive.
    encode_fn(codec) -> bytes (the 0x1B8B packet) or None to skip
    """
    log(f"\n{'='*60}")
    log(f"  {label}")
    log(f"{'='*60}")
    
    access_key = node_login()
    if not access_key:
        log("  Login failed!"); return "login_fail"
    
    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((gw['ip'], gw['port']))
    
    # Game login
    sock.sendall(build_game_login(IGG_ID, gw['token']))
    r = recv_one(sock, timeout=10)
    if r is None or r[0] != 0x0020:
        log("  Game login failed"); sock.close(); return "game_login_fail"
    
    # World entry
    t0 = time.time()
    sock.sendall(build_world_entry(IGG_ID))
    
    if setup_before:
        # Send EXACT PCAP setup sequence IMMEDIATELY (plain packets, no key needed)
        for op in [0x0840, 0x17D4, 0x0AF2, 0x0245]:
            sock.sendall(build_packet(op))
        sock.sendall(build_packet(0x0834, FORMATION_DATA))
        for op in [0x0709, 0x0A2C]:
            sock.sendall(build_packet(op))
        sock.sendall(build_packet(0x1357, struct.pack('<I', 2)))
        sock.sendall(build_packet(0x170D, struct.pack('<I', 2)))
        log(f"  Setup packets sent at +{time.time()-t0:.3f}s")
    
    # Stream-parse for server key
    gs = GameState()
    server_key = None
    pkt_count = 0
    
    while pkt_count < 300:
        pkt = recv_one(sock, timeout=8)
        if pkt is None: break
        op, pl = pkt
        pkt_count += 1
        gs.update(op, pl)
        
        if gs.server_key is not None and server_key is None:
            server_key = gs.server_key
            codec = CMsgCodec.from_u32(server_key)
            log(f"  SK=0x{server_key:08X} at pkt #{pkt_count} (+{time.time()-t0:.3f}s)")
            
            # Send 0x1B8B
            pw_pkt = encode_fn(codec)
            if pw_pkt is not None:
                sock.sendall(pw_pkt)
                log(f"  → 0x1B8B sent ({len(pw_pkt)}B) at +{time.time()-t0:.3f}s")
                log(f"    hex: {pw_pkt.hex()}")
            else:
                log(f"  → 0x1B8B SKIPPED")
            break
    
    if server_key is None:
        log("  No server key!"); sock.close(); return "no_key"
    
    # Read remaining flood + any 0x1B8B response
    time.sleep(0.5)
    remaining = recv_flood(sock, timeout=4)
    got_1b8c = False
    got_error = False
    for op, pl in remaining:
        if op == 0x1B8C:
            got_1b8c = True
            log(f"  *** 0x1B8C RETURN ({len(pl)}B): {pl.hex()}")
        elif op == 0x0037:
            got_error = True
            log(f"  *** ERROR 0x0037 ({len(pl)}B): {pl.hex()}")
    log(f"  {len(remaining)} remaining packets, 1B8C={got_1b8c}, error={got_error}")
    
    # Alive check with raw read
    log("  Checking alive...")
    try:
        ms = int((time.time() - t0) * 1000)
        sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
        time.sleep(2)
        alive_pkts = recv_flood(sock, timeout=3)
        alive = len(alive_pkts) > 0
        for op, pl in alive_pkts:
            if op == 0x1B8C:
                log(f"  *** LATE 0x1B8C ({len(pl)}B): {pl.hex()}")
            elif op == 0x0037:
                log(f"  *** LATE ERROR ({len(pl)}B): {pl.hex()}")
    except Exception as e:
        alive = False
    
    log(f"  ALIVE: {alive}")
    
    # Try raw read for any disconnect data
    if not alive:
        try:
            raw = recv_raw(sock, timeout=2)
            if raw:
                log(f"  Disconnect data ({len(raw)}B): {raw.hex()}")
        except: pass
    
    sock.close()
    return "alive" if alive else "dead"

def main():
    log("=== 0x1B8B ENCODING VARIANTS TEST ===")
    
    results = {}
    
    # A) offset6 (NewEncode) - what PCAPs use
    results['A_offset6'] = run_variant(
        "A: offset6 (NewEncode) - PCAP encoding",
        lambda codec: codec.encode_offset6(0x1B8B, PASSWORD_CHECK_PLAIN, extra=os.urandom(2)),
        setup_before=False
    )
    time.sleep(3)
    
    # B) standard encode - maybe server changed?
    results['B_standard'] = run_variant(
        "B: standard encode - different header format",
        lambda codec: codec.encode(0x1B8B, PASSWORD_CHECK_PLAIN),
        setup_before=False
    )
    time.sleep(3)
    
    # C) offset6 with FULL PCAP setup before
    results['C_pcap_setup'] = run_variant(
        "C: offset6 + EXACT PCAP setup sequence before",
        lambda codec: codec.encode_offset6(0x1B8B, PASSWORD_CHECK_PLAIN, extra=os.urandom(2)),
        setup_before=True
    )
    time.sleep(3)
    
    # D) Control - no 0x1B8B
    results['D_skip'] = run_variant(
        "D: NO 0x1B8B (control - should stay alive)",
        lambda codec: None,
        setup_before=False
    )
    time.sleep(3)
    
    # E) offset6 with EMPTY plaintext (just 0x1B8B opcode + minimal data)
    def make_empty_1b8b(codec):
        # Just the opcode with 1 byte of data
        return codec.encode_offset6(0x1B8B, bytes([0x00]), extra=os.urandom(2))
    results['E_empty'] = run_variant(
        "E: offset6 with MINIMAL plaintext (1 byte)",
        make_empty_1b8b,
        setup_before=False
    )
    
    # Summary
    log(f"\n{'='*60}")
    log(f"  SUMMARY")
    log(f"{'='*60}")
    for k, v in results.items():
        log(f"  {k:20s}: {v}")

if __name__ == '__main__':
    main()

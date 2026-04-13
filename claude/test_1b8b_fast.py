#!/usr/bin/env python3
"""
Fast 0x1B8B Test - Send ASAP after server key extraction
=========================================================
PCAP shows: world_entry → 0x0834 → 0x1B8B within ~1 second.
Previous A/B test waited 10+ seconds → disconnect.
Hypothesis: server has a timeout window for 0x1B8B.

Test A: Fast path - send 0x0834 + 0x1B8B ASAP (stream-parse for server key)
Test B: Slow path (original) - wait for full init flood first
"""
import sys, time, struct, random, subprocess, socket, os
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
                capture_output=True, text=True, timeout=30
            )
            key = result.stdout.strip()
            if len(key) == 32: return key
        except: pass
        if attempt < 2: time.sleep(3)
    return None

def recv_one_packet(sock, timeout=5):
    """Receive exactly one packet. Returns (opcode, payload) or None."""
    sock.settimeout(timeout)
    try:
        header = b''
        while len(header) < 4:
            chunk = sock.recv(4 - len(header))
            if not chunk: return None
            header += chunk
        pkt_len, opcode = struct.unpack('<HH', header)
        payload_len = pkt_len - 4
        if payload_len < 0 or payload_len > 100000: return None
        payload = b''
        while len(payload) < payload_len:
            chunk = sock.recv(payload_len - len(payload))
            if not chunk: return None
            payload += chunk
        return (opcode, payload)
    except:
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

def run_fast_test(access_key):
    """FAST PATH: Stream-parse init flood, send 0x0834+0x1B8B ASAP after server key."""
    log("=== FAST PATH: Send 0x1B8B ASAP ===")
    
    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((gw['ip'], gw['port']))
    
    # Game login
    sock.sendall(build_game_login(IGG_ID, gw['token']))
    r = recv_one_packet(sock, timeout=10)
    if r is None or r[0] != 0x0020:
        log("Game login FAILED"); sock.close(); return False
    log("Game login OK")
    
    # World entry
    world_entry_time = time.time()
    sock.sendall(build_world_entry(IGG_ID))
    
    # Stream-parse: read packets one by one until server key found
    gs = GameState()
    server_key = None
    pkt_count = 0
    sent_1b8b = False
    got_1b8a = False
    
    log("Streaming init flood, looking for server key...")
    
    while True:
        pkt = recv_one_packet(sock, timeout=8)
        if pkt is None:
            log(f"  Stream ended after {pkt_count} packets")
            break
        
        op, pl = pkt
        pkt_count += 1
        gs.update(op, pl)
        
        if op == 0x1B8A:
            got_1b8a = True
            log(f"  [{pkt_count}] S2C 0x1B8A ({len(pl)}B): {pl.hex()}")
        
        if gs.server_key is not None and server_key is None:
            server_key = gs.server_key
            elapsed = time.time() - world_entry_time
            log(f"  [{pkt_count}] Server key found: 0x{server_key:08X} (after {elapsed:.3f}s)")
            
            # IMMEDIATELY send 0x0834 + 0x1B8B (matching PCAP order)
            codec = CMsgCodec.from_u32(server_key)
            
            # 0x0834 FORMATION (plain packet)
            sock.sendall(build_packet(0x0834, FORMATION_DATA))
            log(f"  → Sent 0x0834 FORMATION")
            
            # 0x1B8B PASSWORD CHECK (encrypted, offset6)
            extra = os.urandom(2)
            pw_pkt = codec.encode_offset6(0x1B8B, PASSWORD_CHECK_PLAIN, extra=extra)
            sock.sendall(pw_pkt)
            sent_1b8b = True
            elapsed2 = time.time() - world_entry_time
            log(f"  → Sent 0x1B8B ({len(pw_pkt)}B) at {elapsed2:.3f}s after world entry")
            log(f"    raw: {pw_pkt.hex()}")
        
        # Keep reading for a bit more
        if pkt_count > 300 or (sent_1b8b and pkt_count > 50):
            break
    
    if not sent_1b8b:
        log("FAILED: Could not send 0x1B8B (no server key)")
        sock.close()
        return False
    
    # Drain remaining init flood
    log("Draining remaining flood...")
    remaining = recv_flood(sock, timeout=3)
    log(f"  {len(remaining)} remaining packets")
    
    # Check for 0x1B8C (password return)
    for op, pl in remaining:
        if op == 0x1B8C:
            log(f"  *** 0x1B8C PASSWORD_RETURN ({len(pl)}B): {pl.hex()} ***")
        elif op == 0x0037:
            log(f"  *** 0x0037 ERROR ({len(pl)}B): {pl.hex()} ***")
    
    # Alive check
    log("Checking alive...")
    ms = int((time.time() - world_entry_time) * 1000)
    try:
        sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
        time.sleep(2)
        alive_resp = recv_flood(sock, timeout=3)
        alive = len(alive_resp) > 0
        log(f"  Alive: {alive} ({len(alive_resp)} packets)")
        
        # Check for 0x1B8C in alive response
        for op, pl in alive_resp:
            if op == 0x1B8C:
                log(f"  *** 0x1B8C PASSWORD_RETURN ({len(pl)}B): {pl.hex()} ***")
            elif op == 0x0037:
                log(f"  *** 0x0037 ERROR ({len(pl)}B): {pl.hex()} ***")
    except Exception as e:
        alive = False
        log(f"  Alive: False ({e})")
    
    sock.close()
    return alive

def run_slow_test(access_key):
    """SLOW PATH: Wait for full init flood, then send 0x1B8B (original behavior)."""
    log("=== SLOW PATH: Send 0x1B8B after full init flood ===")
    
    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((gw['ip'], gw['port']))
    
    sock.sendall(build_game_login(IGG_ID, gw['token']))
    r = recv_one_packet(sock, timeout=10)
    if r is None or r[0] != 0x0020:
        log("Game login FAILED"); sock.close(); return False
    log("Game login OK")
    
    world_entry_time = time.time()
    sock.sendall(build_world_entry(IGG_ID))
    
    # Wait for FULL init flood
    log("Waiting for full init flood...")
    init_pkts = recv_flood(sock, timeout=6)
    elapsed = time.time() - world_entry_time
    log(f"  {len(init_pkts)} packets in {elapsed:.3f}s")
    
    gs = GameState()
    for op, pl in init_pkts:
        gs.update(op, pl)
    
    if gs.server_key is None:
        for op in [0x0840, 0x17D4, 0x0709]:
            sock.sendall(build_packet(op))
        more = recv_flood(sock, timeout=4)
        for op, pl in more:
            gs.update(op, pl)
    
    if gs.server_key is None:
        log("No server key!"); sock.close(); return False
    
    codec = CMsgCodec.from_u32(gs.server_key)
    log(f"Server key: 0x{gs.server_key:08X}")
    
    # Send 0x0834 + 0x1B8B (same as fast, but after delay)
    sock.sendall(build_packet(0x0834, FORMATION_DATA))
    extra = os.urandom(2)
    pw_pkt = codec.encode_offset6(0x1B8B, PASSWORD_CHECK_PLAIN, extra=extra)
    sock.sendall(pw_pkt)
    elapsed2 = time.time() - world_entry_time
    log(f"  Sent 0x0834 + 0x1B8B at {elapsed2:.3f}s after world entry")
    
    time.sleep(2)
    resp = recv_flood(sock, timeout=3)
    log(f"  Response: {len(resp)} packets")
    for op, pl in resp:
        if op == 0x1B8C:
            log(f"  *** 0x1B8C PASSWORD_RETURN ({len(pl)}B): {pl.hex()} ***")
        elif op == 0x0037:
            log(f"  *** 0x0037 ERROR ({len(pl)}B): {pl.hex()} ***")
    
    # Alive check
    ms = int((time.time() - world_entry_time) * 1000)
    try:
        sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
        time.sleep(2)
        alive_resp = recv_flood(sock, timeout=3)
        alive = len(alive_resp) > 0
        log(f"  Alive: {alive}")
        for op, pl in alive_resp:
            if op == 0x1B8C:
                log(f"  *** 0x1B8C PASSWORD_RETURN ({len(pl)}B): {pl.hex()} ***")
    except:
        alive = False
        log(f"  Alive: False")
    
    sock.close()
    return alive

def main():
    log("=== FAST vs SLOW 0x1B8B TIMING TEST ===")
    log(f"Hypothesis: server has timeout window for 0x1B8B after 0x1B8A")
    
    # Test A: FAST
    access_key = node_login()
    if not access_key:
        log("Login failed!"); return
    fast_result = run_fast_test(access_key)
    
    time.sleep(5)
    
    # Test B: SLOW
    access_key2 = node_login()
    if not access_key2:
        log("Re-login failed!"); return
    slow_result = run_slow_test(access_key2)
    
    # Summary
    log(f"\n{'='*60}")
    log(f"  RESULTS")
    log(f"{'='*60}")
    log(f"  FAST (ASAP):  alive={fast_result}")
    log(f"  SLOW (delayed): alive={slow_result}")
    if fast_result and not slow_result:
        log(f"  *** TIMING CONFIRMED: Server has timeout for 0x1B8B! ***")
    elif fast_result and slow_result:
        log(f"  Both alive - timing not the issue, but 0x1B8B accepted!")
    elif not fast_result and not slow_result:
        log(f"  Both dead - timing is NOT the issue, encoding problem persists")
    else:
        log(f"  Mixed results - need more investigation")

if __name__ == '__main__':
    main()

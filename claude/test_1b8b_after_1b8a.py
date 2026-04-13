#!/usr/bin/env python3
"""
0x1B8B AFTER 0x1B8A Test
=========================
PCAP proof: Client ALWAYS sends 0x1B8B ~0.83s AFTER receiving 0x1B8A.
Previous tests failed because:
  - Fast test: sent BEFORE 0x1B8A arrived (too early)
  - Slow test: sent 10s AFTER 0x1B8A (too late)

This test: stream init flood, wait for BOTH server key AND 0x1B8A,
then immediately send 0x1B8B.
"""
import sys, time, struct, random, subprocess, socket, os
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from codec import CMsgCodec
from packets import build_packet, build_game_login, build_world_entry
from protocol import opname, OP_ENABLE_VIEW, OP_START_MARCH
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

def recv_one(sock, timeout=10):
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

def main():
    log("=== 0x1B8B AFTER 0x1B8A TIMING TEST ===")
    log(f"Strategy: Wait for 0x1B8A, THEN send 0x1B8B immediately")
    
    access_key = node_login()
    if not access_key:
        log("Login failed!"); return
    
    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((gw['ip'], gw['port']))
    
    # Game login
    sock.sendall(build_game_login(IGG_ID, gw['token']))
    r = recv_one(sock, timeout=10)
    if r is None or r[0] != 0x0020:
        log("Game login failed"); sock.close(); return
    log("Game login OK")
    
    # World entry
    t0 = time.time()
    sock.sendall(build_world_entry(IGG_ID))
    log("World entry sent")
    
    # Stream init flood, tracking both server key AND 0x1B8A
    gs = GameState()
    server_key = None
    codec = None
    got_1b8a = False
    sent_1b8b = False
    sent_setup = False
    pkt_count = 0
    t_1b8a = None
    t_key = None
    
    log("Streaming init flood...")
    
    while pkt_count < 350:
        pkt = recv_one(sock, timeout=10)
        if pkt is None:
            log(f"  Stream ended at {pkt_count} packets")
            break
        
        op, pl = pkt
        pkt_count += 1
        gs.update(op, pl)
        
        # Track server key
        if gs.server_key is not None and server_key is None:
            server_key = gs.server_key
            codec = CMsgCodec.from_u32(server_key)
            t_key = time.time() - t0
            log(f"  [{pkt_count:3d}] Server key: 0x{server_key:08X} at +{t_key:.3f}s")
            
            # Send setup packets immediately (plain, no encryption needed)
            # Matches PCAP: setup is sent between server key and 0x1B8B
            for setup_op in [0x0840, 0x17D4, 0x0AF2, 0x0245]:
                sock.sendall(build_packet(setup_op))
            sock.sendall(build_packet(0x0834, FORMATION_DATA))
            for setup_op in [0x0709, 0x0A2C]:
                sock.sendall(build_packet(setup_op))
            sock.sendall(build_packet(0x1357, struct.pack('<I', 2)))
            sock.sendall(build_packet(0x170D, struct.pack('<I', 2)))
            sent_setup = True
            log(f"  → Setup packets sent at +{time.time()-t0:.3f}s")
        
        # Track 0x1B8A
        if op == 0x1B8A:
            got_1b8a = True
            t_1b8a = time.time() - t0
            log(f"  [{pkt_count:3d}] *** 0x1B8A received at +{t_1b8a:.3f}s ***")
            log(f"       payload ({len(pl)}B): {pl.hex()}")
            
            # If we have the server key, send 0x1B8B NOW
            if codec is not None and not sent_1b8b:
                extra = os.urandom(2)
                pw_pkt = codec.encode_offset6(0x1B8B, PASSWORD_CHECK_PLAIN, extra=extra)
                sock.sendall(pw_pkt)
                sent_1b8b = True
                t_1b8b = time.time() - t0
                delay = t_1b8b - t_1b8a
                log(f"  → 0x1B8B sent ({len(pw_pkt)}B) at +{t_1b8b:.3f}s (delay after 1B8A: {delay:.3f}s)")
                log(f"    hex: {pw_pkt.hex()}")
        
        # Also track 0x1B8C (password return - expected response)
        if op == 0x1B8C:
            log(f"  [{pkt_count:3d}] *** 0x1B8C PASSWORD_RETURN ({len(pl)}B): {pl.hex()} ***")
        
        # If we've sent 0x1B8B, read a few more packets for the response
        if sent_1b8b and pkt_count > 260:
            break
    
    if not sent_1b8b:
        if not got_1b8a:
            log("FAILED: No 0x1B8A received!")
        elif codec is None:
            log("FAILED: No server key!")
        sock.close(); return
    
    # Drain remaining flood
    log("Draining remaining flood...")
    remaining = recv_flood(sock, timeout=4)
    for op, pl in remaining:
        if op == 0x1B8C:
            log(f"  *** 0x1B8C PASSWORD_RETURN ({len(pl)}B): {pl.hex()} ***")
        elif op == 0x0037:
            log(f"  *** ERROR 0x0037 ({len(pl)}B): {pl.hex()}")
    log(f"  {len(remaining)} remaining packets")
    
    # Alive check
    log("Checking alive...")
    ms = int((time.time() - t0) * 1000)
    try:
        sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
        time.sleep(2)
        alive_resp = recv_flood(sock, timeout=3)
        alive = len(alive_resp) > 0
        for op, pl in alive_resp:
            name = opname(op)
            if op == 0x1B8C:
                log(f"  *** 0x1B8C ({len(pl)}B): {pl.hex()} ***")
            elif op == 0x0037:
                log(f"  *** ERROR ({len(pl)}B): {pl.hex()} ***")
    except:
        alive = False
    log(f"  ALIVE: {alive}")
    
    if alive:
        log("\n*** CONNECTION SURVIVED 0x1B8B! ***")
        log("Attempting gather...")
        
        # Enable view
        enable_data = bytearray(10)
        enable_data[0] = 0x01
        struct.pack_into('<I', enable_data, 1, IGG_ID)
        enable_data[9] = 0x01
        sock.sendall(codec.encode(OP_ENABLE_VIEW, bytes(enable_data)))
        time.sleep(1)
        recv_flood(sock, timeout=2)
        
        # View tile
        sock.sendall(build_packet(0x006E, struct.pack('<HHB', 579, 574, 0x01)))
        time.sleep(1)
        recv_flood(sock, timeout=2)
        
        # Hero select
        hero_sel = struct.pack('<BBBBBBB', 0, 1, 0, 0xF4, 0, 0, 0)
        sock.sendall(codec.encode(0x0323, hero_sel))
        time.sleep(0.5)
        
        # Gather
        gather_plain = bytearray(46)
        gather_plain[0] = 2
        struct.pack_into('<H', gather_plain, 4, 0x1749)
        struct.pack_into('<H', gather_plain, 9, 579)
        struct.pack_into('<H', gather_plain, 11, 574)
        gather_plain[13] = 0x01
        gather_plain[14] = 244
        gather_plain[18] = 182
        gather_plain[22] = 0x04
        struct.pack_into('<I', gather_plain, 33, IGG_ID)
        
        gather_pkt = codec.encode(OP_START_MARCH, bytes(gather_plain))
        sock.sendall(gather_pkt)
        log(f"Sent GATHER ({len(gather_pkt)}B)")
        
        # Wait for response
        log("Waiting for gather response...")
        for _ in range(10):
            resp = recv_flood(sock, timeout=3)
            for op, pl in resp:
                name = opname(op)
                if op in (0x0037, 0x076C, 0x0071, 0x00B8):
                    log(f"  *** {name} 0x{op:04X} ({len(pl)}B): {pl[:32].hex()} ***")
            if not resp:
                ms2 = int((time.time() - t0) * 1000)
                sock.sendall(build_packet(0x0042, struct.pack('<II', ms2, 0)))
    else:
        log("\n*** STILL DISCONNECTED AFTER 0x1B8B ***")
    
    sock.close()

if __name__ == '__main__':
    main()

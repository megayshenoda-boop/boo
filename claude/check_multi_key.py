#!/usr/bin/env python3
"""
Check if init flood has MULTIPLE 0x0038 packets with different server keys.
If the key changes mid-flood, we might be using the wrong key for 0x1B8B.
Also check ALL S2C opcodes around 0x1B8A to understand the context.
"""
import sys, time, struct, socket, subprocess
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from packets import build_packet, build_game_login, build_world_entry

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

def recv_flood(sock, timeout=8):
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

def extract_all_keys(packets):
    """Extract ALL server key values from ALL 0x0038 packets."""
    keys = []
    for idx, (op, pl) in enumerate(packets):
        if op == 0x0038 and len(pl) > 6:
            entry_count = struct.unpack('<H', pl[0:2])[0]
            for i in range(entry_count):
                off = 2 + i * 12
                if off + 12 > len(pl): break
                fid = struct.unpack('<I', pl[off:off+4])[0]
                val = struct.unpack('<I', pl[off+4:off+8])[0]
                if fid == 0x4F:
                    keys.append((idx, val))
    return keys

def main():
    log("=== CHECK MULTIPLE SERVER KEYS IN INIT FLOOD ===")
    
    access_key = node_login()
    if not access_key:
        log("Login failed!"); return
    
    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((gw['ip'], gw['port']))
    
    # Game login
    sock.sendall(build_game_login(IGG_ID, gw['token']))
    
    # Wait for login ack
    init_pkts = recv_flood(sock, timeout=2)
    login_ok = any(op == 0x0020 for op, _ in init_pkts)
    log(f"Login ack: {login_ok} ({len(init_pkts)} packets)")
    if not login_ok:
        log("No login ack!"); sock.close(); return
    
    # World entry
    sock.sendall(build_world_entry(IGG_ID))
    
    # Receive FULL init flood
    flood = recv_flood(sock, timeout=8)
    log(f"Init flood: {len(flood)} packets")
    
    # Extract ALL server keys
    keys = extract_all_keys(flood)
    log(f"\nServer keys found: {len(keys)}")
    for idx, val in keys:
        log(f"  Packet #{idx}: SK=0x{val:08X}")
    
    if len(keys) > 1:
        if keys[0][1] != keys[-1][1]:
            log(f"  *** KEY CHANGED! First=0x{keys[0][1]:08X} Last=0x{keys[-1][1]:08X} ***")
        else:
            log(f"  All keys identical: 0x{keys[0][1]:08X}")
    
    # Find 0x1B8A and nearby opcodes
    log(f"\n--- Packets around 0x1B8A ---")
    for idx, (op, pl) in enumerate(flood):
        if op == 0x1B8A:
            # Show 5 packets before and after
            start = max(0, idx - 3)
            end = min(len(flood), idx + 4)
            for j in range(start, end):
                o, p = flood[j]
                marker = " <<<" if o == 0x1B8A else ""
                if o == 0x0038:
                    marker += " [SK packet]"
                log(f"  [{j:3d}] 0x{o:04X} ({len(p):4d}B){marker}")
            log(f"  0x1B8A payload: {pl.hex()}")
            break
    
    # Count unique opcodes
    from collections import Counter
    op_counts = Counter(op for op, _ in flood)
    log(f"\nTop 20 S2C opcodes:")
    for op, cnt in op_counts.most_common(20):
        log(f"  0x{op:04X}: {cnt}")
    
    # Also check: what if 0x0038 arrives AFTER some packets we need?
    first_key_idx = keys[0][0] if keys else -1
    log(f"\nFirst SK at packet #{first_key_idx} of {len(flood)}")
    
    # Send heartbeat to confirm alive (without sending 0x1B8B)
    ms = 5000
    sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
    time.sleep(2)
    resp = recv_flood(sock, timeout=3)
    log(f"\nHeartbeat response: {len(resp)} packets (alive={len(resp) > 0})")
    
    sock.close()

if __name__ == '__main__':
    main()

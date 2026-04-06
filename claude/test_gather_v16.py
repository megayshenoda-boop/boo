#!/usr/bin/env python3
"""
Gather Test v16 - Find castle position first, then gather nearby
"""
import sys, time, struct, subprocess, socket, os
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from codec import CMsgCodec
from packets import build_packet, build_game_login, build_world_entry, recv_packet
from protocol import OP_ENABLE_VIEW, OP_START_MARCH
from game_state import GameState

KINGDOM = 182
MARCH_TYPE = 0x1749

def log(msg):
    try: print(f"[{time.strftime('%H:%M:%S')}] {msg}")
    except: print(f"[{time.strftime('%H:%M:%S')}] {msg.encode('ascii','replace').decode()}")

def node_login():
    for a in range(3):
        try:
            r = subprocess.run(['node', r'D:\CascadeProjects\lords_bot\http_login.mjs', EMAIL, PASSWORD, str(IGG_ID)], capture_output=True, text=True, timeout=30)
            k = r.stdout.strip()
            if len(k) == 32: return k
        except: pass
        if a < 2: time.sleep(3)
    return None

def recv_flood(sock, timeout=3):
    pkts = []
    deadline = time.time() + timeout
    while time.time() < deadline:
        sock.settimeout(max(0.1, deadline - time.time()))
        try:
            hdr = b''
            while len(hdr) < 4:
                c = sock.recv(4 - len(hdr))
                if not c: return pkts
                hdr += c
            plen, op = struct.unpack('<HH', hdr)
            plen -= 4
            if plen < 0 or plen > 100000: return pkts
            pl = b''
            while len(pl) < plen:
                c = sock.recv(plen - len(pl))
                if not c: return pkts
                pl += c
            pkts.append((op, pl))
        except socket.timeout: break
        except: break
    return pkts

def main():
    log("=== GATHER v16 ===")
    ak = node_login()
    if not ak: log("LOGIN FAIL"); return

    gw = connect_gateway(IGG_ID, ak, WORLD_ID)
    log(f"Server: {gw['ip']}:{gw['port']}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((gw['ip'], gw['port']))
    sock.sendall(build_game_login(IGG_ID, gw['token']))
    r = recv_packet(sock, timeout=10)
    if r is None or r[0] != 0x0020: log("Login fail"); sock.close(); return
    log("Login OK")

    sock.sendall(build_world_entry(IGG_ID))
    t0 = time.time()
    init = recv_flood(sock, timeout=6)
    log(f"{len(init)} init packets")

    gs = GameState()
    for op, pl in init: gs.update(op, pl)
    if not gs.server_key: log("No SK!"); sock.close(); return
    codec = CMsgCodec.from_u32(gs.server_key)
    log(f"SK: 0x{gs.server_key:08X}")

    # Dump ALL 0x0038 attributes
    log("\n--- 0x0038 Attributes ---")
    castle_x, castle_y = 0, 0
    for op, pl in init:
        if op == 0x0038 and len(pl) > 50:
            ec = struct.unpack('<H', pl[0:2])[0]
            for idx in range(ec):
                off = 2 + idx * 12
                if off + 12 > len(pl): break
                fid = struct.unpack('<I', pl[off:off+4])[0]
                val = struct.unpack('<I', pl[off+4:off+8])[0]
                # Castle X is typically field 1 or 3, Castle Y is field 2 or 4
                if fid <= 0x10 or (100 < val < 2000):
                    log(f"  field 0x{fid:04X} = {val} (0x{val:08X})")

    # Also check 0x0034 profile for position
    for op, pl in init:
        if op == 0x0034 and len(pl) > 20:
            log(f"\n--- 0x0034 Profile ({len(pl)}B) ---")
            # Try to find X,Y in profile - dump first 100 bytes with offsets
            for i in range(0, min(100, len(pl)-1), 2):
                v = struct.unpack('<H', pl[i:i+2])[0]
                if 100 < v < 1500:
                    log(f"  offset {i}: u16={v}")

    # Check 0x0022 session packet
    for op, pl in init:
        if op == 0x0022:
            log(f"\n--- 0x0022 Session ({len(pl)}B): {pl[:40].hex()} ---")

    # Setup
    log("\nSetup...")
    for opc in [0x0840, 0x17D4, 0x0AF2, 0x0245]:
        sock.sendall(build_packet(opc))
    sock.sendall(build_packet(0x0709))
    sock.sendall(build_packet(0x0A2C))
    time.sleep(1)
    recv_flood(sock, timeout=2)

    # Enable view
    ev = bytearray(10)
    ev[0] = 0x01
    struct.pack_into('<I', ev, 1, IGG_ID)
    ev[9] = 0x01
    sock.sendall(codec.encode(OP_ENABLE_VIEW, bytes(ev)))
    time.sleep(1)
    recv_flood(sock, timeout=2)

    # Request our own turf info which might contain coords
    sock.sendall(build_packet(0x0021, struct.pack('<IIbIBBBB', IGG_ID, 0, 0x0e, 0x3F00FF0E, 0xb0, 0x02, 0x5c, 0x00)))
    time.sleep(1)
    turf = recv_flood(sock, timeout=2)
    for op, pl in turf:
        if op in (0x0076, 0x0077, 0x0022):
            log(f"  Turf 0x{op:04X} ({len(pl)}B): {pl[:30].hex()}")

    # Try viewing a central area first, then search
    log("\nViewing center and searching...")

    # Search for ANY food tile (type 1, any level)
    sock.sendall(build_packet(0x033E, bytes.fromhex("01040001")))  # food lv1
    time.sleep(2)
    sp = recv_flood(sock, timeout=3)
    tx, ty = 0, 0
    for op, pl in sp:
        if op == 0x033F and len(pl) >= 5:
            tx = struct.unpack('<H', pl[1:3])[0]
            ty = struct.unpack('<H', pl[3:5])[0]
            log(f"  Search result: ({tx},{ty}) type={pl[0]}")

    if tx == 0:
        # Try food lv5
        sock.sendall(build_packet(0x033E, bytes.fromhex("01040005")))
        time.sleep(2)
        sp = recv_flood(sock, timeout=3)
        for op, pl in sp:
            if op == 0x033F and len(pl) >= 5:
                tx = struct.unpack('<H', pl[1:3])[0]
                ty = struct.unpack('<H', pl[3:5])[0]
                log(f"  Search lv5: ({tx},{ty}) type={pl[0]}")

    if tx == 0:
        log("  Search failed, using (570,805)")
        tx, ty = 570, 805

    # View the target
    sock.sendall(build_packet(0x006E, struct.pack('<HHB', tx, ty, 1)))
    time.sleep(2)
    recv_flood(sock, timeout=3)

    # HB
    ms = int((time.time() - t0) * 1000)
    sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
    time.sleep(1)
    hb = recv_flood(sock, timeout=2)
    alive = any(op == 0x0042 for op, _ in hb)
    log(f"Alive: {alive}")
    if not alive: sock.close(); return

    # ══════ GATHER ══════
    log(f"\n=== GATHER ({tx},{ty}) ===")

    plain = bytearray(46)
    plain[0] = 1  # slot
    plain[1:4] = os.urandom(3)
    struct.pack_into('<H', plain, 4, MARCH_TYPE)
    struct.pack_into('<H', plain, 9, tx)
    struct.pack_into('<H', plain, 11, ty)
    plain[13] = 0x01
    plain[14] = 0xFF  # hero 255
    plain[18] = KINGDOM & 0xFF
    plain[22] = 0x04
    struct.pack_into('<I', plain, 33, IGG_ID)
    log(f"  Plain: {plain.hex()}")

    pkt = codec.encode(OP_START_MARCH, bytes(plain))
    sock.sendall(pkt)
    log(f"  Sent 0x0CE8 ({len(pkt)}B)")

    # Get responses
    time.sleep(3)
    resp = recv_flood(sock, timeout=8)
    march = False
    log(f"\nResponses ({len(resp)}):")
    for op, pl in resp:
        if op == 0x0071:
            march = True
            log(f"  *** MARCH 0x0071 ({len(pl)}B) ***")
        elif op == 0x076C:
            march = True
            log(f"  *** START 0x076C ({len(pl)}B) ***")
        elif op == 0x0037:
            s = struct.unpack('<I', pl[8:12])[0] if len(pl) >= 12 else -1
            log(f"  0x0037 sub=0x{pl[0]:02X} status={s}")
        elif op == 0x00B8:
            log(f"  0x00B8 ACK: {pl.hex()}")
        elif op not in (0x0042, 0x036C):
            log(f"  0x{op:04X} ({len(pl)}B): {pl[:20].hex()}")

    # Wait more
    for _ in range(6):
        pkts = recv_flood(sock, timeout=5)
        for op, pl in pkts:
            if op in (0x0071, 0x076C):
                march = True
                log(f"  *** {op:#06x} MARCH! ***")
            elif op == 0x0037:
                s = struct.unpack('<I', pl[8:12])[0] if len(pl) >= 12 else -1
                log(f"  0x0037 status={s}")
        if march: break
        ms = int((time.time() - t0) * 1000)
        try: sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
        except: break

    log(f"\n{'*'*40}")
    log(f"RESULT: {'SUCCESS!' if march else 'FAILED'}")
    log(f"{'*'*40}")
    sock.close()

if __name__ == '__main__':
    main()

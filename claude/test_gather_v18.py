#!/usr/bin/env python3
"""
Gather Test v18 - LCG msg_index + detailed response logging
=============================================================
Key findings:
- LCG seed=0, one step pre-consumed → initial state=13
- Server validates msg_index for action opcodes (0x0CE8)
- seed=13 got RESPONSE for gather (0x0079 + 0x0267) but no march
- Need to decode responses and fix game-logic issue
"""
import sys, time, struct, random, subprocess, socket, os
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from codec import CMsgCodec
from packets import build_packet, build_game_login, build_world_entry, recv_packet
from protocol import opname, OP_ENABLE_VIEW, OP_START_MARCH
from game_state import GameState

KINGDOM = 182
FORMATION_DATA = bytes.fromhex("0900ba0b00000b040000d8070000e3070000f103000000040000f8030000d907000001040000")

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

class MsgIndexLCG:
    """getMsgIndex LCG: next = (prev * 37 + 13) & 0xFFFF"""
    def __init__(self, seed=0):
        self.state = seed & 0xFFFF
    def next(self):
        self.state = (self.state * 37 + 13) & 0xFFFF
        return self.state

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

def build_gather_plain(tx, ty, march_slot=1, hero_id=0xFF):
    p = bytearray(46)
    p[0] = march_slot
    p[1:4] = os.urandom(3)
    struct.pack_into('<H', p, 4, 0x1749)  # gather march type
    struct.pack_into('<H', p, 9, tx)
    struct.pack_into('<H', p, 11, ty)
    p[13] = 0x01
    p[14] = hero_id
    p[18] = KINGDOM & 0xFF
    p[22] = 0x04  # gather purpose
    struct.pack_into('<I', p, 33, IGG_ID)
    return bytes(p)

def main():
    log("=== GATHER TEST v18 - LCG + Detailed Response ===")
    log(f"IGG_ID: {IGG_ID} (0x{IGG_ID:08X})")

    # LCG: seed=0, one step pre-consumed → start at state=13
    lcg = MsgIndexLCG(seed=0)
    lcg.next()  # consume step 1 → state becomes 13
    log(f"LCG initialized: state={lcg.state} (seed=0, 1 step consumed)")

    access_key = node_login()
    if not access_key:
        log("LOGIN FAILED!"); return
    log(f"Access key: {access_key[:8]}...")

    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    log(f"Game server: {gw['ip']}:{gw['port']}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((gw['ip'], gw['port']))

    sock.sendall(build_game_login(IGG_ID, gw['token']))
    r = recv_packet(sock, timeout=10)
    if r is None or r[0] != 0x0020:
        log("Game login failed"); sock.close(); return
    log("Game login OK")

    sock.sendall(build_world_entry(IGG_ID))
    start_time = time.time()

    # Init flood
    log("Receiving init flood...")
    init_pkts = recv_flood(sock, timeout=6)
    gs = GameState()
    s2c_1b8a = None
    existing_marches = []
    for op, pl in init_pkts:
        gs.update(op, pl)
        if op == 0x1B8A:
            s2c_1b8a = pl
            log(f"  S2C 0x1B8A: {pl.hex()}")
        if op == 0x0071:
            existing_marches.append(pl)
        if op == 0x00B8:
            log(f"  MARCH_ACK: {pl.hex()}")
    log(f"  {len(init_pkts)} init packets")
    if existing_marches:
        log(f"  *** {len(existing_marches)} EXISTING MARCHES ***")
        for m in existing_marches:
            if len(m) >= 4:
                mid = struct.unpack('<I', m[:4])[0]
                log(f"      march_id=0x{mid:08X}")

    if gs.server_key is None:
        for op in [0x0840, 0x17D4, 0x0709]: sock.sendall(build_packet(op))
        more = recv_flood(sock, timeout=4)
        for op, pl in more: gs.update(op, pl)

    if gs.server_key is None:
        log("No server key!"); sock.close(); return

    codec = CMsgCodec.from_u32(gs.server_key)
    log(f"Server key: 0x{gs.server_key:08X}")

    # Setup
    log("Setup packets...")
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
    setup_resp = recv_flood(sock, timeout=3)
    log(f"  {len(setup_resp)} setup responses")

    # Heartbeat
    ms = int((time.time() - start_time) * 1000)
    sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
    time.sleep(1)
    recv_flood(sock, timeout=1)

    # 0x0CEB ENABLE_VIEW with LCG msg
    msg_ceb = lcg.next()
    ceb_plain = bytearray(10)
    ceb_plain[0] = 0x01
    struct.pack_into('<I', ceb_plain, 1, IGG_ID)
    ceb_plain[9] = 0x01
    ceb_pkt = codec.encode(0x0CEB, bytes(ceb_plain), msg_value=msg_ceb)
    log(f"0x0CEB msg=0x{msg_ceb:04X} (LCG state={lcg.state})")
    sock.sendall(ceb_pkt)
    time.sleep(1)
    ceb_resp = recv_flood(sock, timeout=3)
    log(f"  0x0CEB response: {len(ceb_resp)} packets")

    # Search tile
    sock.sendall(build_packet(0x033E, bytes.fromhex("01040003")))
    time.sleep(2)
    search_resp = recv_flood(sock, timeout=3)
    target_x, target_y = None, None
    for op, pl in search_resp:
        if op == 0x033F and len(pl) >= 5:
            target_x = struct.unpack('<H', pl[1:3])[0]
            target_y = struct.unpack('<H', pl[3:5])[0]
            log(f"  Found tile: ({target_x},{target_y})")
    if target_x is None:
        target_x, target_y = 570, 805
        log(f"  Using fallback tile: ({target_x},{target_y})")

    # View tile
    sock.sendall(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 0x01)))
    time.sleep(1)
    recv_flood(sock, timeout=2)

    # Hero select
    sock.sendall(build_packet(0x0323, bytes([0x00, 0x01, 0x00, 0xFF, 0x00, 0x00, 0x00])))
    time.sleep(0.5)
    recv_flood(sock, timeout=1)

    # Heartbeat
    ms = int((time.time() - start_time) * 1000)
    sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
    time.sleep(1)
    recv_flood(sock, timeout=1)

    # *** GATHER with LCG msg ***
    msg_ce8 = lcg.next()
    log(f"\n{'='*60}")
    log(f"  GATHER to ({target_x},{target_y})")
    log(f"  msg=0x{msg_ce8:04X} (LCG state={lcg.state})")
    log(f"{'='*60}")

    gather_plain = build_gather_plain(target_x, target_y, march_slot=1, hero_id=0xFF)
    log(f"  Plain: {gather_plain.hex()}")
    gather_pkt = codec.encode(OP_START_MARCH, gather_plain, msg_value=msg_ce8)
    sock.sendall(gather_pkt)

    # Wait for response with DETAILED logging
    log("\nWaiting for response...")
    all_responses = []
    got_march = False

    for wait_round in range(8):
        time.sleep(2)
        pkts = recv_flood(sock, timeout=3)
        for op, pl in pkts:
            all_responses.append((op, pl))
            if op in (0x0042, 0x036C):
                continue
            elif op == 0x0037:
                log(f"  *** ERROR 0x0037 ({len(pl)}B): {pl.hex()}")
                if len(pl) >= 12:
                    log(f"      sub={pl[0]:#04x} eid={struct.unpack('<I', pl[4:8])[0]:#010x} status={struct.unpack('<I', pl[8:12])[0]}")
            elif op == 0x0071:
                got_march = True
                log(f"  *** MARCH 0x0071 ({len(pl)}B): {pl[:30].hex()}...")
            elif op == 0x076C:
                got_march = True
                log(f"  *** MARCH_START 0x076C ({len(pl)}B)")
            elif op == 0x00B8:
                log(f"  *** MARCH_ACK 0x00B8 ({len(pl)}B): {pl.hex()}")
            elif op == 0x0079:
                log(f"  *** 0x0079 ({len(pl)}B): {pl.hex()}")
                if len(pl) >= 4:
                    log(f"      u32[0]={struct.unpack('<I', pl[0:4])[0]}")
                if len(pl) >= 8:
                    log(f"      u32[1]={struct.unpack('<I', pl[4:8])[0]}")
                if len(pl) >= 12:
                    log(f"      u32[2]={struct.unpack('<I', pl[8:12])[0]}")
            elif op == 0x0267:
                log(f"  *** 0x0267 ({len(pl)}B): {pl.hex()}")
                if len(pl) >= 4:
                    log(f"      u32[0]={struct.unpack('<I', pl[0:4])[0]}")
            elif op in (0x026D, 0x0033, 0x0032, 0x0002):
                pass  # chat/sync noise
            else:
                log(f"  {opname(op)} ({len(pl)}B): {pl[:20].hex() if pl else '(empty)'}")

        if got_march:
            log("  *** MARCH STARTED! ***")
            break
        ms = int((time.time() - start_time) * 1000)
        sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))

    # Summary
    log(f"\n{'='*60}")
    log(f"  RESULT")
    log(f"{'='*60}")
    unique_ops = sorted(set(op for op, _ in all_responses))
    log(f"  Response opcodes: {[f'0x{o:04X}' for o in unique_ops]}")
    log(f"  March started: {got_march}")

    # Try second gather with different slot if first didn't work
    if not got_march:
        log("\n  Trying slot=2, hero=226...")
        msg_ce8_2 = lcg.next()
        gather_plain2 = build_gather_plain(target_x, target_y, march_slot=2, hero_id=226)
        gather_pkt2 = codec.encode(OP_START_MARCH, gather_plain2, msg_value=msg_ce8_2)
        log(f"  msg=0x{msg_ce8_2:04X}")
        sock.sendall(gather_pkt2)
        time.sleep(3)
        pkts2 = recv_flood(sock, timeout=5)
        for op, pl in pkts2:
            if op in (0x0042, 0x036C, 0x026D): continue
            log(f"  {opname(op)} ({len(pl)}B): {pl[:30].hex() if pl else '(empty)'}")
            if op == 0x0071:
                got_march = True
                log(f"  *** MARCH STARTED on slot 2! ***")

    # Final alive
    try:
        ms = int((time.time() - start_time) * 1000)
        sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
        time.sleep(1)
        alive_pkts = recv_flood(sock, timeout=2)
        log(f"  Connection alive: {len(alive_pkts) > 0}")
    except:
        log(f"  Connection alive: False")

    sock.close()
    log("Done.")

if __name__ == '__main__':
    main()

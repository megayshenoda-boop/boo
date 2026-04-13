#!/usr/bin/env python3
"""
Test LCG msg_index hypothesis for 0x0CE8 gather.
Theory: server tracks getMsgIndex LCG and silently drops packets with wrong msg values.
LCG formula: next = (prev * 37 + 13) & 0xFFFF
Tests multiple LCG seeds to find the right one.
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

class LCG:
    """getMsgIndex LCG from ARM64 disassembly."""
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

def build_gather_plain(tx, ty):
    p = bytearray(46)
    p[0] = 1  # march_slot
    p[1:4] = os.urandom(3)  # nonce
    struct.pack_into('<H', p, 4, 0x1749)  # gather march type
    struct.pack_into('<H', p, 9, tx)
    struct.pack_into('<H', p, 11, ty)
    p[13] = 0x01
    p[14] = 0xFF  # hero_id=255 (any)
    p[18] = KINGDOM & 0xFF
    p[22] = 0x04  # gather purpose
    struct.pack_into('<I', p, 33, IGG_ID)
    return bytes(p)

def test_with_lcg_seed(seed_name, lcg):
    """Run a single gather test with a specific LCG seed."""
    log(f"\n{'='*60}")
    log(f"  LCG SEED: {seed_name} (state={lcg.state})")
    log(f"{'='*60}")

    access_key = node_login()
    if not access_key:
        log("  Login FAILED!"); return "login_fail"

    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((gw['ip'], gw['port']))

    sock.sendall(build_game_login(IGG_ID, gw['token']))
    r = recv_packet(sock, timeout=10)
    if r is None or r[0] != 0x0020:
        sock.close(); return "game_login_fail"

    sock.sendall(build_world_entry(IGG_ID))
    start_time = time.time()

    init_pkts = recv_flood(sock, timeout=6)
    gs = GameState()
    for op, pl in init_pkts: gs.update(op, pl)

    if gs.server_key is None:
        for op in [0x0840, 0x17D4, 0x0709]: sock.sendall(build_packet(op))
        more = recv_flood(sock, timeout=4)
        for op, pl in more: gs.update(op, pl)

    if gs.server_key is None:
        sock.close(); return "no_server_key"

    codec = CMsgCodec.from_u32(gs.server_key)
    log(f"  SK=0x{gs.server_key:08X}")

    # Setup packets
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
    recv_flood(sock, timeout=2)

    # Heartbeat
    ms = int((time.time() - start_time) * 1000)
    sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
    time.sleep(1)
    recv_flood(sock, timeout=1)

    # 0x0CEB with LCG msg
    msg1 = lcg.next()
    ceb_plain = bytearray(10)
    ceb_plain[0] = 0x01
    struct.pack_into('<I', ceb_plain, 1, IGG_ID)
    ceb_plain[9] = 0x01
    ceb_pkt = codec.encode(0x0CEB, bytes(ceb_plain), msg_value=msg1)
    log(f"  0x0CEB msg_value=0x{msg1:04X}")
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
    if target_x is None:
        target_x, target_y = 570, 805

    # View tile
    sock.sendall(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 0x01)))
    time.sleep(1)
    recv_flood(sock, timeout=1)

    # Hero select
    sock.sendall(build_packet(0x0323, bytes([0x00, 0x01, 0x00, 0xFF, 0x00, 0x00, 0x00])))
    time.sleep(0.5)
    recv_flood(sock, timeout=1)

    # Heartbeat
    ms = int((time.time() - start_time) * 1000)
    sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
    time.sleep(1)
    recv_flood(sock, timeout=1)

    # 0x0CE8 GATHER with next LCG msg
    msg2 = lcg.next()
    gather_pkt = codec.encode(OP_START_MARCH, build_gather_plain(target_x, target_y), msg_value=msg2)
    log(f"  0x0CE8 msg_value=0x{msg2:04X} → ({target_x},{target_y})")
    sock.sendall(gather_pkt)

    # Wait for response
    time.sleep(2)
    got_response = False
    got_error = False
    got_march = False
    for _ in range(5):
        pkts = recv_flood(sock, timeout=3)
        for op, pl in pkts:
            if op == 0x0037:
                got_error = True
                log(f"  *** ERROR 0x0037 ({len(pl)}B): {pl[:20].hex()}")
            elif op == 0x0071:
                got_march = True
                log(f"  *** MARCH 0x0071! ***")
            elif op == 0x076C:
                got_march = True
                log(f"  *** MARCH 0x076C! ***")
            elif op == 0x00B8:
                got_response = True
                log(f"  *** ACK 0x00B8 ({len(pl)}B): {pl[:20].hex()}")
            elif op not in (0x0042, 0x036C, 0x026D, 0x0033, 0x0032, 0x0002):
                log(f"  {opname(op)} ({len(pl)}B)")
                got_response = True
        if got_march: break
        ms = int((time.time() - start_time) * 1000)
        sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))

    # Alive check
    try:
        ms = int((time.time() - start_time) * 1000)
        sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
        time.sleep(1)
        alive_pkts = recv_flood(sock, timeout=2)
        alive = len(alive_pkts) > 0
    except:
        alive = False

    sock.close()

    if got_march:
        return "MARCH_SUCCESS"
    elif got_error:
        return "ERROR"
    elif got_response:
        return "RESPONSE_NO_MARCH"
    elif alive:
        return "SILENT_DROP"
    else:
        return "DISCONNECT"

def main():
    log("=== LCG MSG_INDEX HYPOTHESIS TEST ===")

    seeds = [
        ("seed=0", LCG(0)),
        ("seed=1", LCG(1)),
        ("seed=13", LCG(13)),
        ("seed=random(control)", LCG(random.randint(0, 0xFFFF))),
    ]

    results = {}
    for name, lcg in seeds:
        result = test_with_lcg_seed(name, lcg)
        results[name] = result
        log(f"  → RESULT: {result}")
        time.sleep(3)

    log(f"\n{'='*60}")
    log(f"  SUMMARY")
    log(f"{'='*60}")
    for name, result in results.items():
        marker = "✓" if "SUCCESS" in result else "✗"
        log(f"  {marker} {name:30s} → {result}")

if __name__ == '__main__':
    main()

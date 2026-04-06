#!/usr/bin/env python3
"""
Gather Test v13 - Two approaches:
A) Match PCAP packet sequence EXACTLY (with 0x1B8B in correct position)
B) Skip 0x1B8B entirely, go straight to gather

Tests both to isolate the issue.
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
MARCH_TYPE = 0x1749
PASSWORD_CHECK_PLAIN = bytes.fromhex("ed02732200000000ffffffffffffffff")

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def node_login(email, password, igg_id):
    for attempt in range(3):
        try:
            result = subprocess.run(
                ['node', r'D:\CascadeProjects\lords_bot\http_login.mjs', email, password, str(igg_id)],
                capture_output=True, text=True, timeout=30
            )
            key = result.stdout.strip()
            if len(key) == 32: return key
        except Exception as e:
            log(f"  Login attempt {attempt+1} failed: {e}")
        if attempt < 2: time.sleep(3)
    return None

def recv_flood(sock, timeout=3):
    packets = []
    deadline = time.time() + timeout
    while time.time() < deadline:
        remaining = max(0.1, deadline - time.time())
        sock.settimeout(remaining)
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

def extract_server_key(packets):
    gs = GameState()
    for op, pl in packets:
        gs.update(op, pl)
        if gs.server_key is not None: return gs.server_key
    return None

def build_gather_plain(tile_x, tile_y, hero_id=244, march_slot=2):
    plain = bytearray(46)
    plain[0] = march_slot & 0xFF
    plain[1:4] = os.urandom(3)
    struct.pack_into('<H', plain, 4, MARCH_TYPE)
    struct.pack_into('<H', plain, 9, tile_x)
    struct.pack_into('<H', plain, 11, tile_y)
    plain[13] = 0x01
    plain[14] = hero_id & 0xFF
    plain[18] = KINGDOM & 0xFF
    plain[22] = 0x04
    struct.pack_into('<I', plain, 33, IGG_ID)
    return bytes(plain)

def check_heartbeat(sock, start_time):
    """Send heartbeat and check if we get echo back."""
    ms = int((time.time() - start_time) * 1000)
    sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
    time.sleep(1)
    pkts = recv_flood(sock, timeout=2)
    return any(op == 0x0042 for op, _ in pkts)

def do_login():
    """Full login sequence. Returns (sock, codec, start_time) or None."""
    access_key = node_login(EMAIL, PASSWORD, IGG_ID)
    if not access_key:
        log("LOGIN FAILED!"); return None

    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    log(f"Game server: {gw['ip']}:{gw['port']}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((gw['ip'], gw['port']))

    sock.sendall(build_game_login(IGG_ID, gw['token']))
    result = recv_packet(sock, timeout=10)
    if result is None or result[0] != 0x0020:
        log(f"Game login failed"); sock.close(); return None
    log("Game login OK")

    sock.sendall(build_world_entry(IGG_ID))
    start_time = time.time()

    init_pkts = recv_flood(sock, timeout=5)
    log(f"  {len(init_pkts)} init packets")

    # Check for S2C 0x1B8B in init
    for op, pl in init_pkts:
        if op == 0x1B8B:
            log(f"  *** SERVER sent 0x1B8B in init! ({len(pl)}B): {pl.hex()}")

    server_key = extract_server_key(init_pkts)
    if server_key is None:
        log("ERROR: No server key!"); sock.close(); return None
    log(f"  Server key: 0x{server_key:08X}")
    codec = CMsgCodec.from_u32(server_key)

    return sock, codec, start_time

def test_approach(label, send_1b8b=False):
    log(f"\n{'#'*60}")
    log(f"# TEST: {label}")
    log(f"{'#'*60}")

    result = do_login()
    if result is None: return
    sock, codec, start_time = result

    # ─── Setup (matching PCAP sequence) ───
    log("Setup...")

    # Phase 1: Basic setup requests (from PCAP)
    for opcode in [0x0840, 0x17D4, 0x0AF2, 0x0245]:
        sock.sendall(build_packet(opcode))

    # Formation data from PCAP
    formation = bytes.fromhex("0a00ba0b00000b040000d8070000e3070000f103000000040000f8030000d90700000104000016040000")
    sock.sendall(build_packet(0x0834, formation))

    sock.sendall(build_packet(0x0709))
    time.sleep(0.5)

    # Wait for 0x070A response
    r1 = recv_flood(sock, timeout=2)
    got_070a = any(op == 0x070A for op, _ in r1)
    log(f"  0x070A response: {'YES' if got_070a else 'NO'}")

    sock.sendall(build_packet(0x0A2C))
    time.sleep(0.3)

    # Some PCAPs show 0x1357, 0x170D before 0x1B8B
    sock.sendall(build_packet(0x1357, struct.pack('<I', 2)))
    sock.sendall(build_packet(0x170D, struct.pack('<I', 2)))
    time.sleep(0.3)

    # ─── 0x1B8B (optional) ───
    if send_1b8b:
        log("Sending 0x1B8B PASSWORD_CHECK...")
        pw_pkt = codec.encode_offset6(0x1B8B, PASSWORD_CHECK_PLAIN, extra=os.urandom(2))
        sock.sendall(pw_pkt)
        log(f"  Sent ({len(pw_pkt)}B): {pw_pkt.hex()}")

    time.sleep(1)
    r2 = recv_flood(sock, timeout=3)
    log(f"  Responses: {len(r2)} packets")
    for op, pl in r2:
        if op == 0x1B8B:
            log(f"  *** 0x1B8B response: {pl.hex()}")
        elif op in (0x1358, 0x170E, 0x0A2D):
            log(f"  {opname(op)} ({len(pl)}B)")

    # ─── Heartbeat check ───
    alive = check_heartbeat(sock, start_time)
    log(f"  Session alive: {'YES' if alive else 'NO'}")
    if not alive:
        log("  SESSION DEAD!")
        sock.close()
        return

    # ─── Extra setup (from PCAP) ───
    ms = int((time.time() - start_time) * 1000)
    sock.sendall(build_packet(0x0043, struct.pack('<IIII', ms, 0, 0, 0)))
    sock.sendall(build_packet(0x0674))

    # Troop info requests
    for tid in [0x0193, 0x0195, 0x0196, 0x0197, 0x0198, 0x0199, 0x019A, 0x019B]:
        sock.sendall(build_packet(0x099D, struct.pack('<I', tid)))

    sock.sendall(build_packet(0x0767))
    sock.sendall(build_packet(0x0769))
    time.sleep(1)
    recv_flood(sock, timeout=2)

    # ─── Enable view ───
    log("Enable view...")
    enable_data = bytearray(10)
    enable_data[0] = 0x01
    struct.pack_into('<I', enable_data, 1, IGG_ID)
    enable_data[9] = 0x01
    sock.sendall(codec.encode(OP_ENABLE_VIEW, bytes(enable_data)))

    # ─── Search for resource tile ───
    log("Search for resource tile...")
    sock.sendall(build_packet(0x006E, bytes.fromhex("43023e0301")))
    sock.sendall(build_packet(0x033E, bytes.fromhex("01040003")))
    time.sleep(2)
    search_pkts = recv_flood(sock, timeout=3)
    target_x, target_y = None, None
    for op, pl in search_pkts:
        if op == 0x033F and len(pl) >= 5:
            tx = struct.unpack('<H', pl[1:3])[0]
            ty = struct.unpack('<H', pl[3:5])[0]
            if target_x is None:
                target_x, target_y = tx, ty
                log(f"  Target: ({tx},{ty})")

    if target_x is None:
        target_x, target_y = 644, 576
        log(f"  Fallback: ({target_x},{target_y})")

    # View target
    sock.sendall(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 0x01)))
    time.sleep(1)
    recv_flood(sock, timeout=2)

    # Heartbeat
    alive = check_heartbeat(sock, start_time)
    log(f"  Pre-gather alive: {'YES' if alive else 'NO'}")
    if not alive:
        sock.close(); return

    # ═══════════════════════════════════════════
    # GATHER
    # ═══════════════════════════════════════════
    log(f"\n{'='*50}")
    log(f"GATHER to ({target_x},{target_y})")
    log(f"{'='*50}")

    gather_plain = build_gather_plain(target_x, target_y, hero_id=244, march_slot=2)
    log(f"  Plain: {gather_plain.hex()}")
    gather_pkt = codec.encode(OP_START_MARCH, gather_plain)
    sock.sendall(gather_pkt)
    log(f"  Sent 0x0CE8 ({len(gather_pkt)}B)")

    # Wait for response
    got_0071 = False
    got_076c = False
    got_0037 = False
    got_0037_status = None

    time.sleep(2)
    resp = recv_flood(sock, timeout=5)
    log(f"  Response: {len(resp)} packets")
    for op, pl in resp:
        if op == 0x0037:
            got_0037 = True
            if len(pl) >= 12:
                got_0037_status = struct.unpack('<I', pl[8:12])[0]
                log(f"  0x0037: status={got_0037_status} sub=0x{pl[0]:02X} ({len(pl)}B)")
                log(f"    full: {pl.hex()}")
        elif op == 0x0071:
            got_0071 = True
            log(f"  *** 0x0071 MARCH STATE ({len(pl)}B) ***")
        elif op == 0x076C:
            got_076c = True
            log(f"  *** 0x076C MARCH START ({len(pl)}B) ***")
        elif op == 0x00B8:
            log(f"  0x00B8 ACK: {pl.hex()}")
        elif op in (0x06C2, 0x00AA):
            log(f"  {opname(op)} ({len(pl)}B)")

    # Extended wait
    log("Extended wait (30s)...")
    for _ in range(6):
        pkts = recv_flood(sock, timeout=5)
        for op, pl in pkts:
            if op == 0x0071:
                got_0071 = True
                log(f"  *** 0x0071 MARCH! ***")
            elif op == 0x076C:
                got_076c = True
                log(f"  *** 0x076C START! ***")
            elif op == 0x0037:
                if len(pl) >= 12:
                    s = struct.unpack('<I', pl[8:12])[0]
                    log(f"  0x0037: status={s}")

        if got_0071 or got_076c:
            break
        ms = int((time.time() - start_time) * 1000)
        try:
            sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
        except:
            log("  Connection lost!")
            break

    log(f"\nRESULT: 0x0037={'Y' if got_0037 else 'N'}(status={got_0037_status}) | 0x0071={'Y' if got_0071 else 'N'} | 0x076C={'Y' if got_076c else 'N'}")
    if got_0071 or got_076c:
        log("*** SUCCESS! ***")
    sock.close()

def main():
    log("=== GATHER TEST v13 ===")

    # Test A: WITHOUT 0x1B8B
    test_approach("Without 0x1B8B", send_1b8b=False)

    time.sleep(3)

    # Test B: WITH 0x1B8B
    test_approach("With 0x1B8B (NewEncode)", send_1b8b=True)

if __name__ == '__main__':
    main()

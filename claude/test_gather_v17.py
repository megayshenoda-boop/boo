#!/usr/bin/env python3
"""
Gather Test v17 - Skip 0x1B8B + Send 0x0CEB prerequisite
==========================================================
Key findings:
- 0x1B8B: DO NOT SEND (gate=0 causes disconnect)
- 0x0CEB: Must be sent BEFORE 0x0CE8 (found in all PCAP gathers)
- 0x0CEB plaintext: 01 + IGG_ID(LE) + 00000000 + 01
- march_slot=1, hero_id=0xFF (from PCAPs)
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
# Formation data from PCAP 28_Mar (9 troop IDs)
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
        except Exception as e:
            log(f"  Login attempt {attempt+1} failed: {e}")
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

def send_heartbeat(sock, start_time):
    ms = int((time.time() - start_time) * 1000)
    try:
        sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
        return True
    except:
        return False

def main():
    log("=== GATHER TEST v17 - Skip 1B8B + 0x0CEB prereq ===")
    log(f"IGG_ID: {IGG_ID} (0x{IGG_ID:08X})")

    # Login
    log("Login...")
    access_key = node_login()
    if not access_key:
        log("LOGIN FAILED!"); return
    log(f"Access key: {access_key[:8]}...")

    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    log(f"Game server: {gw['ip']}:{gw['port']}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((gw['ip'], gw['port']))

    # Game login
    sock.sendall(build_game_login(IGG_ID, gw['token']))
    r = recv_packet(sock, timeout=10)
    if r is None or r[0] != 0x0020:
        log(f"Game login failed"); sock.close(); return
    log("Game login OK")

    sock.sendall(build_world_entry(IGG_ID))
    start_time = time.time()

    # Init flood
    log("Receiving init flood...")
    init_pkts = recv_flood(sock, timeout=6)
    log(f"  {len(init_pkts)} init packets")

    gs = GameState()
    for op, pl in init_pkts: gs.update(op, pl)

    if gs.server_key is None:
        for op in [0x0840, 0x17D4, 0x0709, 0x0674, 0x0767, 0x0769]:
            sock.sendall(build_packet(op))
        more = recv_flood(sock, timeout=5)
        for op, pl in more: gs.update(op, pl)
        init_pkts.extend(more)

    if gs.server_key is None:
        log("No server key!"); sock.close(); return

    codec = CMsgCodec.from_u32(gs.server_key)
    log(f"Server key: 0x{gs.server_key:08X}")

    # *** SKIP 0x1B8B - gate=0 means don't send ***
    log("*** SKIPPING 0x1B8B (gate=0, server says don't send) ***")

    # Setup packets (matching PCAP order exactly)
    log("Setup packets...")
    sock.sendall(build_packet(0x0840))
    time.sleep(0.15)
    sock.sendall(build_packet(0x17D4))
    time.sleep(0.05)
    sock.sendall(build_packet(0x0AF2))
    time.sleep(0.15)
    sock.sendall(build_packet(0x0245))
    sock.sendall(build_packet(0x0834, FORMATION_DATA))  # FORMATION - was missing!
    time.sleep(0.25)
    sock.sendall(build_packet(0x0709))
    time.sleep(0.05)
    sock.sendall(build_packet(0x0A2C))
    time.sleep(0.15)
    setup_resp = recv_flood(sock, timeout=3)
    log(f"  {len(setup_resp)} setup responses")

    # Heartbeat
    send_heartbeat(sock, start_time)
    time.sleep(1)
    recv_flood(sock, timeout=2)

    # *** Send 0x0CEB - PCAP prerequisite before gather ***
    log("*** Sending 0x0CEB (march prerequisite) ***")
    ceb_plain = bytearray(10)
    ceb_plain[0] = 0x01
    struct.pack_into('<I', ceb_plain, 1, IGG_ID)
    # bytes [5:9] = 0x00000000
    ceb_plain[9] = 0x01
    ceb_pkt = codec.encode(0x0CEB, bytes(ceb_plain))
    log(f"  0x0CEB plain: {bytes(ceb_plain).hex()}")
    log(f"  0x0CEB packet ({len(ceb_pkt)}B): {ceb_pkt.hex()}")
    sock.sendall(ceb_pkt)

    time.sleep(1)
    ceb_resp = recv_flood(sock, timeout=3)
    log(f"  0x0CEB response: {len(ceb_resp)} packets")
    for op, pl in ceb_resp:
        log(f"    {opname(op)} ({len(pl)}B): {pl[:30].hex() if pl else '(empty)'}")

    # Search for resource tile
    log("Searching for resource tile...")
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
                log(f"  Found tile: ({tx},{ty})")
    if target_x is None:
        target_x, target_y = 644, 576
        log(f"  Using fallback tile: ({target_x},{target_y})")

    # View tile (like PCAP)
    log(f"Viewing tile ({target_x},{target_y})...")
    sock.sendall(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 0x01)))
    time.sleep(1)
    view_resp = recv_flood(sock, timeout=2)
    log(f"  View response: {len(view_resp)} packets")

    # Heartbeat before gather
    send_heartbeat(sock, start_time)
    time.sleep(1)
    recv_flood(sock, timeout=1)

    # *** HERO SELECT (0x0323) - required before gather ***
    log(f"Selecting hero for march...")
    hero_payload = bytes([0x00, 0x01, 0x00, 0xFF, 0x00, 0x00, 0x00])  # slot=1, hero=255(any)
    sock.sendall(build_packet(0x0323, hero_payload))
    log(f"  Sent 0x0323 hero_select: {hero_payload.hex()}")
    time.sleep(0.5)
    recv_flood(sock, timeout=1)

    # *** GATHER ***
    log(f"\n{'='*60}")
    log(f"  SENDING GATHER to ({target_x},{target_y})")
    log(f"{'='*60}")

    gather_plain = bytearray(46)
    gather_plain[0] = 1  # march_slot=1 (PCAP uses 1, not 2)
    gather_plain[1:4] = os.urandom(3)  # nonce
    struct.pack_into('<H', gather_plain, 4, 0x1749)  # gather march type
    # [6:9] = zeros
    struct.pack_into('<H', gather_plain, 9, target_x)
    struct.pack_into('<H', gather_plain, 11, target_y)
    gather_plain[13] = 0x01  # flag
    gather_plain[14] = 0xFF  # hero_id=255 (any hero, from PCAP)
    # [15:18] = zeros
    gather_plain[18] = KINGDOM & 0xFF
    # [19:22] = zeros
    gather_plain[22] = 0x04  # gather purpose
    # [23:33] = zeros
    struct.pack_into('<I', gather_plain, 33, IGG_ID)
    # [37:46] = zeros

    log(f"  Plain ({len(gather_plain)}B): {bytes(gather_plain).hex()}")
    gather_pkt = codec.encode(OP_START_MARCH, bytes(gather_plain))
    log(f"  Encrypted ({len(gather_pkt)}B): {gather_pkt.hex()}")
    sock.sendall(gather_pkt)

    # Wait for response with verbose logging
    log("\nWaiting for response...")
    got_error = False
    got_march = False
    got_ack = False
    all_resp_ops = []

    for wait_round in range(10):
        time.sleep(2)
        pkts = recv_flood(sock, timeout=3)
        if pkts:
            for op, pl in pkts:
                all_resp_ops.append(op)
                if op == 0x0037:
                    got_error = True
                    log(f"  *** 0x0037 ERROR ({len(pl)}B): {pl.hex()}")
                    if len(pl) >= 12:
                        sub = pl[0]
                        eid = struct.unpack('<I', pl[4:8])[0]
                        status = struct.unpack('<I', pl[8:12])[0]
                        log(f"      sub=0x{sub:02X} id=0x{eid:08X} status={status}")
                elif op == 0x00B8:
                    got_ack = True
                    log(f"  *** 0x00B8 MARCH_ACK ({len(pl)}B): {pl.hex()}")
                elif op == 0x0071:
                    got_march = True
                    log(f"  *** 0x0071 MARCH_STATE ({len(pl)}B) ***")
                elif op == 0x076C:
                    got_march = True
                    log(f"  *** 0x076C MARCH_START ({len(pl)}B) ***")
                elif op == 0x0CEB:
                    log(f"  *** 0x0CEB response ({len(pl)}B): {pl[:20].hex()}")
                elif op == 0x0CE8:
                    log(f"  *** 0x0CE8 response ({len(pl)}B): {pl[:20].hex()}")
                elif op not in (0x0042, 0x036C, 0x0002, 0x0033):
                    log(f"  {opname(op)} ({len(pl)}B)")

        if got_march:
            log("  *** MARCH DETECTED - SUCCESS! ***")
            break

        # Keep alive
        send_heartbeat(sock, start_time)

    # Result
    log(f"\n{'='*60}")
    log(f"  RESULT")
    log(f"{'='*60}")
    log(f"  March started:  {got_march}")
    log(f"  March ACK:      {got_ack}")
    log(f"  Error:          {got_error}")
    unique_ops = sorted(set(all_resp_ops))
    log(f"  Response ops:   {[f'0x{o:04X}' for o in unique_ops]}")

    if got_march:
        log("  *** GATHER SUCCEEDED! ***")
    elif got_error:
        log("  Server returned error - check error details above")
    elif got_ack:
        log("  Got ACK but no march state - partial success?")
    else:
        log("  No response at all - packet might be silently dropped")

    # Final alive check
    alive = False
    try:
        send_heartbeat(sock, start_time)
        time.sleep(1)
        r = recv_flood(sock, timeout=2)
        alive = len(r) > 0
    except:
        pass
    log(f"  Connection alive: {alive}")
    log(f"{'='*60}")

    sock.close()
    log("Done.")

if __name__ == '__main__':
    main()

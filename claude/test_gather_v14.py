#!/usr/bin/env python3
"""
Gather Test v14 - PCAP-exact sequence
======================================
Fixes from PCAP analysis:
1. Send 0x0323 (PRE_MARCH) before 0x0CE8
2. hero=255 (0xFF), slot=1
3. Skip 0x1B8B (kills session - needs PRNG sync work)
4. Better tile search sequence
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

def build_gather_plain(tile_x, tile_y, hero_id=0xFF, march_slot=1):
    """Build 0x0CE8 START_MARCH plaintext - PCAP-matched."""
    plain = bytearray(46)
    plain[0] = march_slot & 0xFF
    plain[1:4] = os.urandom(3)  # nonce
    struct.pack_into('<H', plain, 4, MARCH_TYPE)
    # [6:9] stays zero
    struct.pack_into('<H', plain, 9, tile_x)
    struct.pack_into('<H', plain, 11, tile_y)
    plain[13] = 0x01  # action flag
    plain[14] = hero_id & 0xFF
    # [15:18] stays zero
    plain[18] = KINGDOM & 0xFF
    # [19:22] stays zero
    plain[22] = 0x04  # gather purpose
    # [23:33] stays zero
    struct.pack_into('<I', plain, 33, IGG_ID)
    # [37:46] stays zero
    return bytes(plain)

def build_pre_march(slot=1, hero=0xFF):
    """Build 0x0323 PRE_MARCH packet (from PCAP: 000100ff000000)."""
    payload = bytearray(7)
    payload[0] = 0x00
    payload[1] = slot & 0xFF
    payload[2] = 0x00
    payload[3] = hero & 0xFF
    # [4:7] = zeros
    return build_packet(0x0323, bytes(payload))

def main():
    log("=== GATHER TEST v14 - PCAP-Exact Sequence ===")

    # ---- Login ----
    access_key = node_login(EMAIL, PASSWORD, IGG_ID)
    if not access_key:
        log("LOGIN FAILED!"); return

    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    log(f"Game server: {gw['ip']}:{gw['port']}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((gw['ip'], gw['port']))

    sock.sendall(build_game_login(IGG_ID, gw['token']))
    result = recv_packet(sock, timeout=10)
    if result is None or result[0] != 0x0020:
        log("Game login failed"); sock.close(); return
    log("Game login OK")

    sock.sendall(build_world_entry(IGG_ID))
    start_time = time.time()

    # ---- Init flood ----
    init_pkts = recv_flood(sock, timeout=5)
    log(f"{len(init_pkts)} init packets")

    server_key = extract_server_key(init_pkts)
    if server_key is None:
        log("ERROR: No server key!"); sock.close(); return
    log(f"Server key: 0x{server_key:08X}")
    codec = CMsgCodec.from_u32(server_key)

    # ---- Setup (PCAP sequence) ----
    log("Setup...")
    for opcode in [0x0840, 0x17D4, 0x0AF2, 0x0245]:
        sock.sendall(build_packet(opcode))
    formation = bytes.fromhex("0a00ba0b00000b040000d8070000e3070000f103000000040000f8030000d90700000104000016040000")
    sock.sendall(build_packet(0x0834, formation))
    sock.sendall(build_packet(0x0709))
    time.sleep(0.5)
    recv_flood(sock, timeout=2)

    sock.sendall(build_packet(0x0A2C))
    sock.sendall(build_packet(0x1357, struct.pack('<I', 2)))
    sock.sendall(build_packet(0x170D, struct.pack('<I', 2)))
    time.sleep(1)
    recv_flood(sock, timeout=2)

    # Skip 0x1B8B (kills session, needs PRNG sync)

    # Extras
    ms = int((time.time() - start_time) * 1000)
    sock.sendall(build_packet(0x0043, struct.pack('<IIII', ms, 0, 0, 0)))
    sock.sendall(build_packet(0x0674))
    for tid in [0x0193, 0x0195, 0x0196, 0x0197, 0x0198, 0x0199, 0x019A, 0x019B]:
        sock.sendall(build_packet(0x099D, struct.pack('<I', tid)))
    sock.sendall(build_packet(0x0767))
    sock.sendall(build_packet(0x0769))
    time.sleep(1)
    recv_flood(sock, timeout=2)

    # ---- Enable view ----
    log("Enable view...")
    enable_data = bytearray(10)
    enable_data[0] = 0x01
    struct.pack_into('<I', enable_data, 1, IGG_ID)
    enable_data[9] = 0x01
    sock.sendall(codec.encode(OP_ENABLE_VIEW, bytes(enable_data)))

    # View near our castle area first (from PCAP: 579,830)
    sock.sendall(build_packet(0x006E, struct.pack('<HHB', 579, 830, 1)))
    time.sleep(2)
    recv_flood(sock, timeout=3)

    # ---- Search for resource tile ----
    log("Searching resource tile...")
    sock.sendall(build_packet(0x033E, bytes.fromhex("01040003")))  # food lv3
    time.sleep(2)
    search_pkts = recv_flood(sock, timeout=3)

    target_x, target_y = None, None
    for op, pl in search_pkts:
        if op == 0x033F and len(pl) >= 5:
            rtype = pl[0]
            tx = struct.unpack('<H', pl[1:3])[0]
            ty = struct.unpack('<H', pl[3:5])[0]
            log(f"  Search result: type={rtype} ({tx},{ty})")
            if tx > 0 and ty > 0 and target_x is None:
                target_x, target_y = tx, ty

    if target_x is None or target_x == 0:
        # Fallback: use coordinates near PCAP known tile
        target_x, target_y = 570, 805
        log(f"  Using PCAP fallback: ({target_x},{target_y})")
    else:
        log(f"  Using: ({target_x},{target_y})")

    # View the target tile
    sock.sendall(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 1)))
    time.sleep(2)
    recv_flood(sock, timeout=3)

    # ---- Heartbeat ----
    ms = int((time.time() - start_time) * 1000)
    sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
    time.sleep(1)
    hb_resp = recv_flood(sock, timeout=2)
    alive = any(op == 0x0042 for op, _ in hb_resp)
    log(f"Pre-gather alive: {'YES' if alive else 'NO'}")
    if not alive:
        log("SESSION DEAD!"); sock.close(); return

    # ═══════════════════════════════════════════════════
    # GATHER (PCAP-exact: 0x0323 then 0x0CE8)
    # ═══════════════════════════════════════════════════
    log(f"\n{'='*60}")
    log(f"GATHER to ({target_x},{target_y}) - hero=0xFF, slot=1")
    log(f"{'='*60}")

    # Step 1: PRE_MARCH (0x0323)
    pre_march = build_pre_march(slot=1, hero=0xFF)
    sock.sendall(pre_march)
    log(f"  Sent 0x0323 PRE_MARCH ({len(pre_march)}B): {pre_march.hex()}")

    # Step 2: START_MARCH (0x0CE8)
    gather_plain = build_gather_plain(target_x, target_y, hero_id=0xFF, march_slot=1)
    log(f"  Gather plain: {gather_plain.hex()}")
    gather_pkt = codec.encode(OP_START_MARCH, gather_plain)
    sock.sendall(gather_pkt)
    log(f"  Sent 0x0CE8 ({len(gather_pkt)}B)")

    # ---- Wait for response ----
    got_0071 = False
    got_076c = False
    got_0037 = False
    got_0037_status = None
    got_00b8 = False

    time.sleep(2)
    resp = recv_flood(sock, timeout=5)
    log(f"\nResponse: {len(resp)} packets")
    for op, pl in resp:
        if op == 0x0037:
            got_0037 = True
            if len(pl) >= 12:
                got_0037_status = struct.unpack('<I', pl[8:12])[0]
            log(f"  0x0037 sub=0x{pl[0]:02X} status={got_0037_status} full={pl.hex()}")
        elif op == 0x0071:
            got_0071 = True
            log(f"  *** 0x0071 MARCH_STATE ({len(pl)}B) ***")
            log(f"      {pl[:40].hex()}")
        elif op == 0x076C:
            got_076c = True
            log(f"  *** 0x076C MARCH_START ({len(pl)}B) ***")
        elif op == 0x00B8:
            got_00b8 = True
            log(f"  0x00B8 ACK: {pl.hex()}")
        elif op == 0x06C2:
            log(f"  0x06C2 SOLDIER_INFO ({len(pl)}B)")
        elif op == 0x00AA:
            log(f"  0x00AA HERO_INFO ({len(pl)}B)")
        else:
            if op not in (0x0042, 0x036C, 0x0043):
                log(f"  0x{op:04X} ({len(pl)}B)")

    # Extended wait
    if not (got_0071 or got_076c):
        log("\nExtended wait (30s)...")
        for _ in range(6):
            pkts = recv_flood(sock, timeout=5)
            for op, pl in pkts:
                if op == 0x0071:
                    got_0071 = True
                    log(f"  *** 0x0071 MARCH_STATE! ***")
                elif op == 0x076C:
                    got_076c = True
                    log(f"  *** 0x076C MARCH_START! ***")
                elif op == 0x0037:
                    if len(pl) >= 12:
                        s = struct.unpack('<I', pl[8:12])[0]
                        log(f"  0x0037 status={s}")
            if got_0071 or got_076c: break
            ms = int((time.time() - start_time) * 1000)
            try:
                sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
            except:
                log("  Connection lost!"); break

    # ---- Result ----
    log(f"\n{'='*60}")
    if got_0071 or got_076c:
        log("*** GATHER SUCCEEDED! ***")
    elif got_00b8 and got_0037 and got_0037_status == 0:
        log("Server accepted (ACK+status 0) but no march started.")
        log("Possible: tile occupied, no troops, or 0x0323 issue.")
    else:
        log(f"No success. B8={got_00b8} 0037={got_0037}(s={got_0037_status})")
    log(f"  0x00B8={got_00b8} 0x0037={got_0037}(s={got_0037_status}) 0x0071={got_0071} 0x076C={got_076c}")
    log(f"{'='*60}")

    sock.close()

if __name__ == '__main__':
    main()

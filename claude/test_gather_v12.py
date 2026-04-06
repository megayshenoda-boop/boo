#!/usr/bin/env python3
"""
Gather Test v12 - FIXED 0x1B8B using NewEncode (CMsgCodec::NewEncode)
=====================================================================
Key discovery: 0x1B8B uses NewEncode (header shifted +2, 2 extra bytes at [4:6]).
Plaintext is CONSTANT across all 84 PCAPs: ED02732200000000FFFFFFFFFFFFFFFF
Extra bytes at [4:6] are from getMsgIndex PRNG - we use random.
"""
import sys, time, struct, random, subprocess, socket, os
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from codec import CMsgCodec
from packets import build_packet, build_game_login, build_world_entry, recv_packet
from protocol import opname, OP_ENABLE_VIEW, OP_START_MARCH
from game_state import GameState

# ═══════════════════════════════════════════════════════════════
# CONSTANTS (from PCAP analysis)
# ═══════════════════════════════════════════════════════════════
KINGDOM = 182
MARCH_TYPE = 0x1749  # resource gather
PASSWORD_CHECK_PLAIN = bytes.fromhex("ed02732200000000ffffffffffffffff")  # 16 bytes, constant
IMPORTANT_OPS = {0x0022, 0x0037, 0x0071, 0x076C, 0x00B8, 0x00B9, 0x0033,
                 0x0076, 0x0077, 0x0078, 0x06C2, 0x00AA, 0x0636, 0x0768, 0x076A,
                 0x1B8B}

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

def build_password_check(codec):
    """Build 0x1B8B using NewEncode (encode_offset6).
    Extra bytes = random (getMsgIndex PRNG in real client).
    Plaintext = constant ED02732200000000FFFFFFFFFFFFFFFF."""
    extra = os.urandom(2)  # getMsgIndex output, server doesn't validate
    return codec.encode_offset6(0x1B8B, PASSWORD_CHECK_PLAIN, extra=extra)

def build_gather_plain(tile_x, tile_y, hero_id=244, march_slot=2):
    """Build 0x0CE8 START_MARCH plaintext (46 bytes, PCAP-verified)."""
    plain = bytearray(46)
    plain[0] = march_slot & 0xFF
    plain[1:4] = os.urandom(3)  # nonce
    struct.pack_into('<H', plain, 4, MARCH_TYPE)
    struct.pack_into('<H', plain, 9, tile_x)
    struct.pack_into('<H', plain, 11, tile_y)
    plain[13] = 0x01  # action flag
    plain[14] = hero_id & 0xFF
    plain[18] = KINGDOM & 0xFF
    plain[22] = 0x04  # gather purpose
    struct.pack_into('<I', plain, 33, IGG_ID)
    return bytes(plain)

def log_packet(op, pl, prefix=""):
    if op == 0x0037:
        log(f"{prefix}*** 0x0037 ({len(pl)}B): {pl.hex()}")
        if len(pl) >= 12:
            sub_type = pl[0]
            id_val = struct.unpack('<I', pl[4:8])[0]
            status = struct.unpack('<I', pl[8:12])[0]
            log(f"{prefix}    sub=0x{sub_type:02X} id=0x{id_val:08X} status={status}")
    elif op == 0x0071:
        log(f"{prefix}*** 0x0071 MARCH_STATE ({len(pl)}B) ***")
    elif op == 0x076C:
        log(f"{prefix}*** 0x076C MARCH_START ({len(pl)}B) ***")
    elif op == 0x00B8:
        log(f"{prefix}0x00B8 ACK ({len(pl)}B): {pl.hex()}")
    elif op == 0x1B8B:
        log(f"{prefix}0x1B8B PASSWORD_CHECK response ({len(pl)}B): {pl.hex()}")
    elif op in IMPORTANT_OPS:
        log(f"{prefix}{opname(op)} ({len(pl)}B)")

def main():
    log("=== GATHER TEST v12 - NewEncode 0x1B8B Fix ===")

    # ─── Login ───
    log("Login...")
    access_key = node_login(EMAIL, PASSWORD, IGG_ID)
    if not access_key:
        log("LOGIN FAILED!"); return
    log(f"Access key: {access_key[:8]}...")

    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    log(f"Game server: {gw['ip']}:{gw['port']}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((gw['ip'], gw['port']))

    # ─── Game login ───
    sock.sendall(build_game_login(IGG_ID, gw['token']))
    result = recv_packet(sock, timeout=10)
    if result is None or result[0] != 0x0020:
        log(f"Game login failed: {result}"); sock.close(); return
    log("Game login OK")

    sock.sendall(build_world_entry(IGG_ID))
    start_time = time.time()

    # ─── Init flood ───
    log("Receiving init flood...")
    init_pkts = recv_flood(sock, timeout=5)
    log(f"  {len(init_pkts)} init packets")

    server_key = extract_server_key(init_pkts)
    if server_key is None:
        log("ERROR: Server key not found!"); sock.close(); return
    log(f"  Server key: 0x{server_key:08X}")
    codec = CMsgCodec.from_u32(server_key)

    # ─── Send 0x1B8B PASSWORD_CHECK ───
    log("\n*** Sending 0x1B8B PASSWORD_CHECK (NewEncode) ***")
    pw_pkt = build_password_check(codec)
    log(f"  Packet ({len(pw_pkt)}B): {pw_pkt.hex()}")
    sock.sendall(pw_pkt)

    time.sleep(1)
    pw_resp = recv_flood(sock, timeout=3)
    log(f"  Response: {len(pw_resp)} packets")
    pw_ok = False
    for op, pl in pw_resp:
        log_packet(op, pl, "    ")
        if op == 0x1B8B:
            pw_ok = True
            log(f"    >>> 0x1B8B response received!")

    # ─── Heartbeat check (verify session is alive) ───
    ms = int((time.time() - start_time) * 1000)
    sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
    time.sleep(1)
    hb_resp = recv_flood(sock, timeout=3)
    hb_echo = any(op == 0x0042 for op, _ in hb_resp)
    log(f"\n  Heartbeat echo: {'YES' if hb_echo else 'NO'}")
    if not hb_echo:
        log("  WARNING: No heartbeat echo - session may be dead")

    # ─── Setup packets ───
    log("\nSending setup...")
    for opcode in [0x0840, 0x17D4, 0x0AF2, 0x0245]:
        sock.sendall(build_packet(opcode))
    sock.sendall(build_packet(0x0709))
    sock.sendall(build_packet(0x0A2C))
    time.sleep(1)
    recv_flood(sock, timeout=2)

    # ─── Enable view ───
    log("Enable view...")
    enable_data = bytearray(10)
    enable_data[0] = 0x01
    struct.pack_into('<I', enable_data, 1, IGG_ID)
    enable_data[9] = 0x01
    sock.sendall(codec.encode(OP_ENABLE_VIEW, bytes(enable_data)))
    time.sleep(1)
    recv_flood(sock, timeout=2)

    # ─── Search for gather target ───
    log("Searching for resource tile...")
    sock.sendall(build_packet(0x033E, bytes.fromhex("01040003")))  # search food tile
    time.sleep(2)
    search_pkts = recv_flood(sock, timeout=3)
    target_x, target_y = None, None
    for op, pl in search_pkts:
        if op == 0x033F and len(pl) >= 5:
            tx = struct.unpack('<H', pl[1:3])[0]
            ty = struct.unpack('<H', pl[3:5])[0]
            log(f"  Found tile: ({tx},{ty})")
            if target_x is None:
                target_x, target_y = tx, ty

    if target_x is None:
        target_x, target_y = 644, 576
        log(f"  Using fallback: ({target_x},{target_y})")

    # View target tile
    sock.sendall(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 0x01)))
    time.sleep(1)
    recv_flood(sock, timeout=2)

    # ─── Heartbeat ───
    ms = int((time.time() - start_time) * 1000)
    sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
    time.sleep(1)
    recv_flood(sock, timeout=2)

    # ═══════════════════════════════════════════
    # GATHER
    # ═══════════════════════════════════════════
    log(f"\n{'='*60}")
    log(f"SENDING GATHER to ({target_x},{target_y})")
    log(f"{'='*60}")

    gather_plain = build_gather_plain(target_x, target_y, hero_id=244, march_slot=2)
    log(f"  Plain ({len(gather_plain)}B): {gather_plain.hex()}")
    gather_pkt = codec.encode(OP_START_MARCH, gather_plain)
    sock.sendall(gather_pkt)
    log(f"  Sent 0x0CE8 ({len(gather_pkt)}B)")

    # ─── Wait for response ───
    time.sleep(2)
    resp_pkts = recv_flood(sock, timeout=5)
    log(f"\nResponse: {len(resp_pkts)} packets")
    got_0037 = False
    got_0071 = False
    got_076c = False

    for op, pl in resp_pkts:
        log_packet(op, pl, "  ")
        if op == 0x0037:
            got_0037 = True
            if len(pl) >= 12:
                status = struct.unpack('<I', pl[8:12])[0]
                log(f"  0x0037 status = {status}")
        if op == 0x0071: got_0071 = True
        if op == 0x076C: got_076c = True

    # Extended wait with heartbeats
    log("\nExtended wait (45s)...")
    end_time = time.time() + 45
    while time.time() < end_time:
        pkts = recv_flood(sock, timeout=5)
        for op, pl in pkts:
            if op in IMPORTANT_OPS or op in (0x0076, 0x0077, 0x0032):
                log_packet(op, pl, "  ")
            if op == 0x0071: got_0071 = True
            if op == 0x076C: got_076c = True

        if got_0071 or got_076c:
            log("  *** MARCH DETECTED! ***")
            break

        ms = int((time.time() - start_time) * 1000)
        sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))

    # ─── Result ───
    log(f"\n{'='*60}")
    if got_0071 or got_076c:
        log("*** GATHER SUCCEEDED! ***")
    elif got_0037:
        log("Server responded with 0x0037 but no march started.")
        log("Possible: wrong hero/slot, no troops, or 0x1B8B still needed.")
    else:
        log("No significant response received.")
    log(f"  0x0037={got_0037} | 0x0071={got_0071} | 0x076C={got_076c}")
    log(f"{'='*60}")

    sock.close()
    log("Done.")

if __name__ == '__main__':
    main()

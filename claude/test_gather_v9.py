"""
Gather Test v9 - Raw socket replay of PCAP 27_Mar_09_17_04.
No threading, no GameConnection class. Just raw socket + exact PCAP sequence.

Key insight: replicate the EXACT C2S packet sequence from a SUCCESSFUL gather PCAP.
The PCAP sends 0x0323 (hero select) right before 0x0CE8.
Skip 0x1B8B (breaks our session) and 0x1C87 (unknown large packet).
"""
import sys, time, struct, random, subprocess, socket
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from codec import CMsgCodec
from packets import build_packet, build_game_login, build_world_entry, recv_packet, recv_all_packets
from protocol import opname, OP_ENABLE_VIEW, OP_START_MARCH
from game_state import GameState

KINGDOM = 182
MARCH_TYPE = 0x1749

# From PCAP: 0x0834 formation data (exact bytes)
# Updated from fresh PCAP 28_Mar: 9 entries instead of 10
FORMATION_DATA = bytes.fromhex("0900ba0b00000b040000d8070000e3070000f103000000040000f8030000d907000001040000")

# From PCAP: 0x099D troop IDs (8 troops)
# Updated from fresh PCAP 28_Mar: 5 troop IDs (not 8)
TROOP_IDS_PCAP = [0x0193, 0x0196, 0x0197, 0x019A, 0x019B]

def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def node_login(email, password, igg_id):
    for attempt in range(3):
        try:
            result = subprocess.run(
                ['node', r'D:\CascadeProjects\lords_bot\http_login.mjs', email, password, str(igg_id)],
                capture_output=True, text=True, timeout=30
            )
            key = result.stdout.strip()
            if len(key) == 32:
                return key
        except Exception as e:
            log(f"  Login attempt {attempt+1} failed: {e}")
        if attempt < 2:
            time.sleep(3)
    return None

def recv_flood(sock, timeout=3):
    """Receive all packets within timeout, return list of (opcode, payload)."""
    packets = []
    deadline = time.time() + timeout
    while time.time() < deadline:
        remaining = max(0.1, deadline - time.time())
        sock.settimeout(remaining)
        try:
            header = b''
            while len(header) < 4:
                chunk = sock.recv(4 - len(header))
                if not chunk:
                    return packets
                header += chunk
            pkt_len, opcode = struct.unpack('<HH', header)
            payload_len = pkt_len - 4
            if payload_len < 0 or payload_len > 100000:
                return packets
            payload = b''
            while len(payload) < payload_len:
                chunk = sock.recv(payload_len - len(payload))
                if not chunk:
                    return packets
                payload += chunk
            packets.append((opcode, payload))
        except socket.timeout:
            break
        except Exception as e:
            log(f"  recv error: {e}")
            break
    return packets

def extract_server_key(packets):
    """Extract server key from 0x0038 packet."""
    gs = GameState()
    for op, pl in packets:
        gs.update(op, pl)
        if gs.server_key is not None:
            return gs.server_key
    return None

def build_gather_plain(tile_x, tile_y, hero_id=255, march_slot=1):
    """Build 46-byte gather plaintext (matches PCAP structure exactly)."""
    plain = bytearray(46)
    plain[0] = march_slot & 0xFF
    # Random nonce bytes 1-3
    plain[1] = random.randint(0, 255)
    plain[2] = random.randint(0, 255)
    plain[3] = random.randint(0, 255)
    # March type
    struct.pack_into('<H', plain, 4, MARCH_TYPE)
    # Bytes 6-8: zeros
    # Target coordinates
    struct.pack_into('<H', plain, 9, tile_x)
    struct.pack_into('<H', plain, 11, tile_y)
    plain[13] = 0x01  # flag
    plain[14] = hero_id & 0xFF  # hero
    plain[18] = KINGDOM & 0xFF  # kingdom
    plain[22] = 0x04  # troop group count
    struct.pack_into('<I', plain, 33, IGG_ID)
    return bytes(plain)

def main():
    log("=== GATHER TEST v9 - Raw PCAP Replay ===")

    # Step 1: HTTP Login
    log("\n--- Step 1: HTTP Login ---")
    access_key = node_login(EMAIL, PASSWORD, IGG_ID)
    if not access_key:
        log("LOGIN FAILED!"); return
    log(f"Access key: {access_key[:8]}...")

    # Step 2: Gateway
    log("\n--- Step 2: Gateway ---")
    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    log(f"Game server: {gw['ip']}:{gw['port']}")

    # Step 3: Raw TCP connection to game server
    log("\n--- Step 3: Game Server Connect ---")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((gw['ip'], gw['port']))
    log(f"Connected to {gw['ip']}:{gw['port']}")

    # 0x001F Login
    login_pkt = build_game_login(IGG_ID, gw['token'])
    sock.sendall(login_pkt)
    log(f"Sent 0x001F ({len(login_pkt)}B)")

    # Wait for 0x0020
    result = recv_packet(sock, timeout=10)
    if result is None or result[0] != 0x0020:
        log(f"Expected 0x0020, got {result}"); sock.close(); return
    log(f"Got 0x0020 OK (status={result[1][0] if result[1] else -1})")

    # 0x0021 World Entry
    entry_pkt = build_world_entry(IGG_ID)
    sock.sendall(entry_pkt)
    log(f"Sent 0x0021 ({len(entry_pkt)}B)")
    start_time = time.time()

    # Step 4: Receive FULL init flood first
    log("\n--- Step 4: Receive Init Flood ---")
    gs = GameState()
    codec = None
    init_pkts = recv_flood(sock, timeout=6)
    for op, pl in init_pkts:
        gs.update(op, pl)
    log(f"  Init packets: {len(init_pkts)}")

    if gs.server_key is None:
        log("ERROR: Server key not found!"); sock.close(); return
    server_key = gs.server_key
    log(f"  Server key: 0x{server_key:08X}")
    codec = CMsgCodec.from_u32(server_key)

    # Step 5: Send setup packets with pacing (like real client ~200ms apart)
    log("\n--- Step 5: Setup Packets (paced) ---")
    sock.sendall(build_packet(0x0840))
    time.sleep(0.15)

    # Drain any responses
    mid_pkts = recv_flood(sock, timeout=0.5)
    log(f"  After 0x0840: {len(mid_pkts)} S2C responses")

    sock.sendall(build_packet(0x17D4))
    time.sleep(0.05)
    sock.sendall(build_packet(0x0AF2))
    time.sleep(0.15)

    mid_pkts = recv_flood(sock, timeout=0.5)
    log(f"  After 0x17D4+0x0AF2: {len(mid_pkts)} S2C responses")

    sock.sendall(build_packet(0x0245))
    sock.sendall(build_packet(0x0834, FORMATION_DATA))
    time.sleep(0.25)

    mid_pkts = recv_flood(sock, timeout=0.5)
    log(f"  After 0x0245+0x0834: {len(mid_pkts)} S2C responses")

    sock.sendall(build_packet(0x0709))
    time.sleep(0.05)
    sock.sendall(build_packet(0x0A2C))
    time.sleep(0.15)

    sock.sendall(build_packet(0x1357, bytes.fromhex("02000000")))
    time.sleep(0.05)
    sock.sendall(build_packet(0x170D, bytes.fromhex("02000000")))
    time.sleep(0.15)

    mid_pkts = recv_flood(sock, timeout=0.5)
    log(f"  After 0x1357+0x170D: {len(mid_pkts)} S2C responses")

    # NOW send 0x1B8B
    log("  Sending 0x1B8B...")
    igg_bytes = struct.pack('<I', IGG_ID)
    plain_1b8b = igg_bytes + b'\x00\x00\x00\x00' + b'\xff' * 8
    pkt_1b8b = codec.encode_offset6(0x1B8B, plain_1b8b)
    sock.sendall(pkt_1b8b)
    log(f"  Sent 0x1B8B ({len(pkt_1b8b)}B): {pkt_1b8b.hex()}")

    # Check 0x1B8B response
    time.sleep(1)
    resp_pkts = recv_flood(sock, timeout=2)
    log(f"  0x1B8B response: {len(resp_pkts)} packets")
    session_alive = True
    for op, pl in resp_pkts:
        log(f"    0x{op:04X} ({len(pl)}B): {pl[:20].hex() if pl else 'empty'}")
        if op == 0x02F2:
            log("    *** 0x02F2 = ERROR RESPONSE - session will die ***")
            session_alive = False

    if not session_alive:
        log("ERROR: 0x1B8B rejected by server"); sock.close(); return
    log("  0x1B8B accepted! Session alive.")

    # Step 6: Enable View + Search (matches fresh PCAP 28_Mar sequence)
    log("\n--- Step 6: Enable View + Search ---")

    # 0x0CEB (encrypted)
    enable_data = bytearray(10)
    enable_data[0] = 0x01
    struct.pack_into('<I', enable_data, 1, IGG_ID)
    enable_data[9] = 0x01
    sock.sendall(codec.encode(OP_ENABLE_VIEW, bytes(enable_data)))
    log(f"  Sent 0x0CEB")

    # 0x006E source tile (579,830)
    sock.sendall(build_packet(0x006E, bytes.fromhex("43023e0301")))

    # 0x099D troop queries
    for tid in TROOP_IDS_PCAP:
        sock.sendall(build_packet(0x099D, struct.pack('<I', tid)))
        time.sleep(0.05)
    log(f"  Sent {len(TROOP_IDS_PCAP)}x 0x099D")

    # 0x0767 + 0x0769 + 0x01D6
    sock.sendall(build_packet(0x0767))
    sock.sendall(build_packet(0x0769))
    sock.sendall(build_packet(0x01D6))
    log("  Sent 0x0767 + 0x0769 + 0x01D6")

    # 0x033E search for level 2 wheat
    sock.sendall(build_packet(0x033E, bytes.fromhex("02040003")))
    log("  Sent 0x033E search (lv2 wheat)")

    # Wait for view responses + search result
    time.sleep(2)
    view_pkts = recv_flood(sock, timeout=3)
    log(f"  View responses: {len(view_pkts)} packets")

    # Find target from 0x033F response
    target_x, target_y = None, None
    for op, pl in view_pkts:
        if op == 0x033F and len(pl) >= 5:
            tx = struct.unpack('<H', pl[1:3])[0]
            ty = struct.unpack('<H', pl[3:5])[0]
            log(f"    Search result: ({tx},{ty})")
            if target_x is None:
                target_x, target_y = tx, ty
        elif op not in (0x0042, 0x0043, 0x036C, 0x0076, 0x0077, 0x0078, 0x007A, 0x0091, 0x0080, 0x0082):
            log(f"    {opname(op)} ({len(pl)}B)")

    if target_x is None:
        # Use PCAP target as fallback
        target_x, target_y = 570, 805
        log(f"  Using PCAP target: ({target_x},{target_y})")

    # 0x006E target tile
    sock.sendall(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 0x01)))
    log(f"  Sent target 0x006E ({target_x},{target_y})")

    # Wait + heartbeat
    time.sleep(1)
    ms = int((time.time() - start_time) * 1000)
    sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
    log(f"  Sent heartbeat (ms={ms})")

    # Drain everything before gather
    time.sleep(2)
    pre_pkts = recv_flood(sock, timeout=3)
    log(f"  Pre-gather drain: {len(pre_pkts)} packets")
    for op, pl in pre_pkts:
        if op == 0x0071:
            log(f"    *** EXISTING MARCH 0x0071 ({len(pl)}B)")
        elif op == 0x00B8:
            log(f"    *** 0x00B8 ({len(pl)}B): {pl.hex()}")
        elif op not in (0x0042, 0x0043, 0x036C):
            log(f"    {opname(op)} ({len(pl)}B)")

    # Step 9: 0x0323 HERO SELECT + 0x0CE8 GATHER
    # Fresh PCAP 28_Mar: hero=226 (Arslan), slot=1
    for march_slot in [1, 2]:
        log(f"\n--- Step 9: GATHER slot={march_slot} ---")
        hero_id = 226  # 0xE2 = Arslan (from fresh PCAP)

        # 0x0323 hero select
        hero_payload = bytes([0x00, march_slot, 0x00, hero_id, 0x00, 0x00, 0x00])
        sock.sendall(build_packet(0x0323, hero_payload))
        log(f"  Sent 0x0323 hero_select: {hero_payload.hex()}")
        time.sleep(0.5)

        # 0x0CE8 gather
        gather_plain = build_gather_plain(target_x, target_y, hero_id=hero_id, march_slot=march_slot)
        log(f"  Gather plaintext ({len(gather_plain)}B): {gather_plain.hex()}")
        gather_pkt = codec.encode(OP_START_MARCH, gather_plain)
        sock.sendall(gather_pkt)
        log(f"  Sent 0x0CE8 ({len(gather_pkt)}B)")

        # Check response for this slot
        time.sleep(2)
        slot_pkts = recv_flood(sock, timeout=5)
        log(f"  Response: {len(slot_pkts)} packets")
        got_71 = False
        for op, pl in slot_pkts:
            if op in (0x0042, 0x036C): continue
            log(f"  0x{op:04X} ({len(pl)}B): {pl[:20].hex() if pl else 'empty'}")
            if op == 0x0071:
                got_71 = True
        if got_71:
            log("  *** MARCH STARTED! ***")
            break
        # Heartbeat between attempts
        ms = int((time.time() - start_time) * 1000)
        sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
        time.sleep(1)

    # Step 10: Wait for response
    log("\n--- Step 10: Waiting for Response (30s) ---")

    got_b8 = False
    got_71 = False
    got_76c = False

    deadline = time.time() + 30
    while time.time() < deadline:
        pkts = recv_flood(sock, timeout=3)
        if not pkts:
            # Send heartbeat to keep alive
            ms = int((time.time() - start_time) * 1000)
            sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
            continue

        for op, pl in pkts:
            if op == 0x00B8:
                got_b8 = True
                log(f"  *** 0x00B8 PARTIAL_ACK ({len(pl)}B): {pl.hex()}")
            elif op == 0x0071:
                got_71 = True
                log(f"  *** 0x0071 MARCH_STATE ({len(pl)}B): {pl.hex()}")
            elif op == 0x076C:
                got_76c = True
                log(f"  *** 0x076C ({len(pl)}B)")
            elif op == 0x0033:
                log(f"  SYN_ATTRIBUTE ({len(pl)}B): {pl.hex()}")
            elif op == 0x06C2:
                log(f"  SOLDIER_INFO ({len(pl)}B)")
            elif op == 0x00AA:
                log(f"  HERO_INFO ({len(pl)}B)")
            elif op == 0x00B9:
                log(f"  0x00B9 ACK ({len(pl)}B)")
            elif op == 0x0037:
                log(f"  *** 0x0037 ERROR? ({len(pl)}B): {pl.hex()}")
            elif op not in (0x0042, 0x036C, 0x0002):
                log(f"  {opname(op)} ({len(pl)}B): {pl[:20].hex() if pl else 'empty'}")

        if got_71 or got_76c:
            log("\n  SUCCESS! March started!")
            break

    # Summary
    log("\n" + "="*60)
    log(f"RESULT: B8={'YES' if got_b8 else 'NO'} | 0x0071={'YES' if got_71 else 'NO'} | 0x076C={'YES' if got_76c else 'NO'}")
    if got_71 or got_76c:
        log("GATHER SUCCEEDED!")
    elif got_b8:
        log("PARTIAL - Server accepted but march not confirmed")
    else:
        log("FAILED - No response")
    log("="*60)

    sock.close()
    log("Done.")

if __name__ == '__main__':
    main()

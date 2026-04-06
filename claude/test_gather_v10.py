"""
Gather Test v10 - Diagnostic version.
Key changes from v9:
1. Logs ALL received opcodes (to check for 0x0022 session verification)
2. Tries hero=244 (matching codex_lab success) instead of 255
3. Skips 0x0323 hero select (matching codex_lab success)
4. More detailed 0x0037 analysis
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

# From PCAP: 0x0834 formation data
FORMATION_DATA = bytes.fromhex("0a00ba0b00000b040000d8070000e3070000f103000000040000f8030000d90700000104000016040000")

# Troop IDs
TROOP_IDS_PCAP = [0x0193, 0x0195, 0x0196, 0x0197, 0x0198, 0x0199, 0x019A, 0x019B]

# Track ALL received opcodes
all_opcodes = {}

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
    """Receive all packets within timeout."""
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
            if payload_len < 0 or payload_len > 100000:
                return packets
            payload = b''
            while len(payload) < payload_len:
                chunk = sock.recv(payload_len - len(payload))
                if not chunk: return packets
                payload += chunk
            packets.append((opcode, payload))
            # Track opcode
            all_opcodes[opcode] = all_opcodes.get(opcode, 0) + 1
        except socket.timeout:
            break
        except Exception as e:
            log(f"  recv error: {e}")
            break
    return packets

def extract_server_key(packets):
    gs = GameState()
    for op, pl in packets:
        gs.update(op, pl)
        if gs.server_key is not None:
            return gs.server_key
    return None

def build_gather_plain(tile_x, tile_y, hero_id=244, march_slot=2):
    plain = bytearray(46)
    plain[0] = march_slot & 0xFF
    plain[1] = random.randint(0, 255)
    plain[2] = random.randint(0, 255)
    plain[3] = random.randint(0, 255)
    struct.pack_into('<H', plain, 4, MARCH_TYPE)
    struct.pack_into('<H', plain, 9, tile_x)
    struct.pack_into('<H', plain, 11, tile_y)
    plain[13] = 0x01
    plain[14] = hero_id & 0xFF
    plain[18] = KINGDOM & 0xFF
    plain[22] = 0x04
    struct.pack_into('<I', plain, 33, IGG_ID)
    return bytes(plain)

def main():
    log("=== GATHER TEST v10 - Diagnostic ===")

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

    # Step 3: Connect
    log("\n--- Step 3: Game Server Connect ---")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((gw['ip'], gw['port']))
    log(f"Connected to {gw['ip']}:{gw['port']}")

    # Login
    login_pkt = build_game_login(IGG_ID, gw['token'])
    sock.sendall(login_pkt)
    log(f"Sent 0x001F ({len(login_pkt)}B)")

    result = recv_packet(sock, timeout=10)
    if result is None or result[0] != 0x0020:
        log(f"Expected 0x0020, got {result}"); sock.close(); return
    log(f"Got 0x0020 OK (status={result[1][0] if result[1] else -1})")

    # World Entry
    entry_pkt = build_world_entry(IGG_ID)
    sock.sendall(entry_pkt)
    log(f"Sent 0x0021 ({len(entry_pkt)}B)")
    start_time = time.time()

    # Step 4: Init flood
    log("\n--- Step 4: Init Flood ---")
    init_pkts = recv_flood(sock, timeout=5)
    log(f"Received {len(init_pkts)} init packets")

    server_key = extract_server_key(init_pkts)
    if server_key is None:
        log("ERROR: Server key not found!"); sock.close(); return
    log(f"Server key: 0x{server_key:08X}")
    codec = CMsgCodec.from_u32(server_key)

    # Check for 0x0022 in init
    for op, pl in init_pkts:
        if op == 0x0022:
            log(f"  *** 0x0022 SESSION VERIFICATION in init: {pl.hex()}")
        if op == 0x0071:
            log(f"  *** 0x0071 EXISTING MARCH in init ({len(pl)}B)")
        if op == 0x1EAA:
            log(f"  *** 0x1EAA HERO_AVAIL ({len(pl)}B): {pl.hex()}")

    # Step 5: Setup (matching PCAP order)
    log("\n--- Step 5: Setup Sequence ---")
    sock.sendall(build_packet(0x0840)); log("  Sent 0x0840")
    sock.sendall(build_packet(0x17D4)); log("  Sent 0x17D4")
    sock.sendall(build_packet(0x0AF2)); log("  Sent 0x0AF2")
    sock.sendall(build_packet(0x0245)); log("  Sent 0x0245")
    sock.sendall(build_packet(0x0834, FORMATION_DATA)); log(f"  Sent 0x0834 formation ({len(FORMATION_DATA)}B)")
    sock.sendall(build_packet(0x0709)); log("  Sent 0x0709")
    sock.sendall(build_packet(0x0A2C)); log("  Sent 0x0A2C")
    sock.sendall(build_packet(0x1357, bytes.fromhex("02000000"))); log("  Sent 0x1357")
    sock.sendall(build_packet(0x170D, bytes.fromhex("02000000"))); log("  Sent 0x170D")

    # SKIP 0x1B8B
    log("  SKIP 0x1B8B (can't compute checksum/verify)")

    time.sleep(1)
    setup_pkts = recv_flood(sock, timeout=3)
    log(f"  Setup responses: {len(setup_pkts)} packets")
    for op, pl in setup_pkts:
        if op == 0x0022:
            log(f"    *** 0x0022 SESSION VERIFICATION: {pl.hex()}")
        elif op == 0x0071:
            log(f"    *** 0x0071 EXISTING MARCH ({len(pl)}B)")
        elif op == 0x1EAA:
            log(f"    *** 0x1EAA HERO_AVAIL ({len(pl)}B): {pl.hex()}")
        elif op not in (0x0042, 0x036C, 0x0002):
            log(f"    {opname(op)} ({len(pl)}B)")

    # Step 6: Server time + extras
    log("\n--- Step 6: Extras ---")
    ms = int((time.time() - start_time) * 1000)
    sock.sendall(build_packet(0x0043, struct.pack('<IIII', ms, 0, 0, 0)))
    sock.sendall(build_packet(0x0674))
    for tid in TROOP_IDS_PCAP:
        sock.sendall(build_packet(0x099D, struct.pack('<I', tid)))
    sock.sendall(build_packet(0x0767))
    sock.sendall(build_packet(0x0769))
    log(f"  Sent 0x0043 + 0x0674 + 8x099D + 0x0767 + 0x0769")

    time.sleep(1)
    extra_pkts = recv_flood(sock, timeout=2)
    log(f"  Extra responses: {len(extra_pkts)} packets")
    for op, pl in extra_pkts:
        if op == 0x0022:
            log(f"    *** 0x0022 SESSION VERIFICATION: {pl.hex()}")
        elif op == 0x1EAA:
            log(f"    *** 0x1EAA HERO_AVAIL ({len(pl)}B): {pl.hex()}")

    # Step 7: Heartbeat
    log("\n--- Step 7: Heartbeat ---")
    ms = int((time.time() - start_time) * 1000)
    sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
    sock.sendall(build_packet(0x0043, struct.pack('<IIII', ms, 0, 0, 0)))
    sock.sendall(build_packet(0x11FF, bytes.fromhex("01000000")))
    log(f"  Sent heartbeat + server_time + 0x11FF (ms={ms})")

    time.sleep(1)
    hb_pkts = recv_flood(sock, timeout=2)
    log(f"  Heartbeat responses: {len(hb_pkts)} packets")
    for op, pl in hb_pkts:
        if op == 0x0022:
            log(f"    *** 0x0022 SESSION VERIFICATION: {pl.hex()}")

    # Step 8: Enable View + search
    log("\n--- Step 8: Enable View + Search ---")
    enable_data = bytearray(10)
    enable_data[0] = 0x01
    struct.pack_into('<I', enable_data, 1, IGG_ID)
    enable_data[9] = 0x01
    sock.sendall(codec.encode(OP_ENABLE_VIEW, bytes(enable_data)))
    log(f"  Sent 0x0CEB")

    sock.sendall(build_packet(0x006E, bytes.fromhex("43023e0301")))
    log("  Sent source 0x006E (579,830)")

    sock.sendall(build_packet(0x033E, bytes.fromhex("01040003")))
    log("  Sent 0x033E search")

    time.sleep(2)
    view_pkts = recv_flood(sock, timeout=3)
    log(f"  View responses: {len(view_pkts)} packets")

    target_x, target_y = None, None
    for op, pl in view_pkts:
        if op == 0x033F and len(pl) >= 5:
            tx = struct.unpack('<H', pl[1:3])[0]
            ty = struct.unpack('<H', pl[3:5])[0]
            log(f"    Search result: ({tx},{ty})")
            if target_x is None:
                target_x, target_y = tx, ty
        elif op == 0x0022:
            log(f"    *** 0x0022 SESSION VERIFICATION: {pl.hex()}")

    if target_x is None:
        target_x, target_y = 644, 576
        log(f"  Using fallback target: ({target_x},{target_y})")

    sock.sendall(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 0x01)))
    log(f"  Sent target 0x006E ({target_x},{target_y})")

    # Pre-gather drain
    time.sleep(1)
    ms = int((time.time() - start_time) * 1000)
    sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))

    time.sleep(2)
    pre_pkts = recv_flood(sock, timeout=3)
    log(f"  Pre-gather drain: {len(pre_pkts)} packets")
    for op, pl in pre_pkts:
        if op == 0x0022:
            log(f"    *** 0x0022 SESSION VERIFICATION: {pl.hex()}")
        elif op == 0x0071:
            log(f"    *** 0x0071 EXISTING MARCH ({len(pl)}B)")

    # Step 9: GATHER (hero=244, no 0x0323 - matching codex_lab success)
    log("\n--- Step 9: GATHER (hero=244, NO 0x0323) ---")

    march_slot = 2
    hero_id = 244

    # NO 0x0323 hero select (matching codex_lab success)
    log("  SKIP 0x0323 hero select (matching codex_lab success)")

    gather_plain = build_gather_plain(target_x, target_y, hero_id=hero_id, march_slot=march_slot)
    log(f"  Gather plaintext ({len(gather_plain)}B): {gather_plain.hex()}")
    gather_pkt = codec.encode(OP_START_MARCH, gather_plain)
    sock.sendall(gather_pkt)
    log(f"  Sent 0x0CE8 ({len(gather_pkt)}B)")

    # Step 10: Wait for response
    log("\n--- Step 10: Response (30s) ---")
    got_b8 = False
    got_71 = False
    got_76c = False
    got_0037 = False

    deadline = time.time() + 30
    while time.time() < deadline:
        pkts = recv_flood(sock, timeout=3)
        if not pkts:
            ms = int((time.time() - start_time) * 1000)
            sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
            continue

        for op, pl in pkts:
            if op == 0x00B8:
                got_b8 = True
                log(f"  *** 0x00B8 PARTIAL_ACK ({len(pl)}B): {pl.hex()}")
            elif op == 0x0071:
                got_71 = True
                log(f"  *** 0x0071 MARCH_STATE ({len(pl)}B)")
            elif op == 0x076C:
                got_76c = True
                log(f"  *** 0x076C SUCCESS ({len(pl)}B)")
            elif op == 0x0037:
                got_0037 = True
                log(f"  *** 0x0037 ({len(pl)}B): {pl.hex()}")
                if len(pl) >= 12:
                    sub_type = pl[0]
                    id_val = struct.unpack('<I', pl[4:8])[0]
                    status = struct.unpack('<I', pl[8:12])[0]
                    log(f"      sub_type=0x{sub_type:02X}({sub_type}) id=0x{id_val:08X} status={status}")
            elif op == 0x0033:
                log(f"  SYN_ATTRIBUTE ({len(pl)}B)")
            elif op == 0x06C2:
                log(f"  SOLDIER_INFO ({len(pl)}B)")
            elif op == 0x00AA:
                log(f"  HERO_INFO ({len(pl)}B)")
            elif op == 0x00B9:
                log(f"  0x00B9 ACK ({len(pl)}B)")
            elif op == 0x0022:
                log(f"  *** 0x0022 SESSION VERIFICATION: {pl.hex()}")
            elif op not in (0x0042, 0x036C, 0x0002):
                log(f"  {opname(op)} ({len(pl)}B)")

        if got_71 or got_76c:
            log("\n  SUCCESS! March started!")
            break

    # Summary
    log("\n" + "="*60)
    log(f"RESULT: B8={'YES' if got_b8 else 'NO'} | 0x0071={'YES' if got_71 else 'NO'} | 0x076C={'YES' if got_76c else 'NO'} | 0x0037={'YES' if got_0037 else 'NO'}")

    # Check for 0x0022
    if 0x0022 in all_opcodes:
        log(f"*** 0x0022 WAS received ({all_opcodes[0x0022]} times) ***")
    else:
        log("*** 0x0022 was NEVER received (session NOT verified!) ***")

    # All unique opcodes received
    log(f"\nAll opcodes received ({len(all_opcodes)} unique):")
    for op in sorted(all_opcodes.keys()):
        log(f"  0x{op:04X} ({opname(op)}) x{all_opcodes[op]}")

    log("="*60)
    sock.close()
    log("Done.")

if __name__ == '__main__':
    main()

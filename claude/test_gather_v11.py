"""
Gather Test v11 - Post-gather probing.
Based on v10 success (hero=244, no 0x0323 → 0x0037 status=0).
Now: probe march state after gather to verify if march started.
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
FORMATION_DATA = bytes.fromhex("0a00ba0b00000b040000d8070000e3070000f103000000040000f8030000d90700000104000016040000")
TROOP_IDS_PCAP = [0x0193, 0x0195, 0x0196, 0x0197, 0x0198, 0x0199, 0x019A, 0x019B]

# Important opcodes to watch
IMPORTANT_OPS = {0x0022, 0x0037, 0x0071, 0x076C, 0x00B8, 0x00B9, 0x0033,
                 0x0076, 0x0077, 0x0078, 0x06C2, 0x00AA, 0x0636, 0x0768, 0x076A}

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
            all_opcodes[opcode] = all_opcodes.get(opcode, 0) + 1
        except socket.timeout: break
        except Exception as e:
            log(f"  recv error: {e}"); break
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

def log_packet(op, pl, prefix=""):
    """Log a packet with context-appropriate detail."""
    if op == 0x0037:
        log(f"{prefix}*** 0x0037 ({len(pl)}B): {pl.hex()}")
        if len(pl) >= 12:
            sub_type = pl[0]
            id_val = struct.unpack('<I', pl[4:8])[0]
            status = struct.unpack('<I', pl[8:12])[0]
            log(f"{prefix}    sub_type=0x{sub_type:02X}({sub_type}) id=0x{id_val:08X} status={status}")
    elif op == 0x0071:
        log(f"{prefix}*** 0x0071 MARCH_STATE ({len(pl)}B): {pl[:40].hex()}")
    elif op == 0x076C:
        log(f"{prefix}*** 0x076C MARCH_START ({len(pl)}B)")
    elif op == 0x00B8:
        log(f"{prefix}*** 0x00B8 ACK ({len(pl)}B): {pl.hex()}")
    elif op == 0x0636:
        log(f"{prefix}0x0636 MARCH_DATA ({len(pl)}B): {pl[:40].hex()}")
    elif op == 0x0768:
        log(f"{prefix}0x0768 MARCH_SLOT ({len(pl)}B): {pl.hex()}")
    elif op == 0x076A:
        log(f"{prefix}0x076A MARCH_QUEUE ({len(pl)}B): {pl.hex()}")
    elif op == 0x06C2:
        log(f"{prefix}SOLDIER_INFO ({len(pl)}B)")
    elif op == 0x00AA:
        log(f"{prefix}HERO_INFO ({len(pl)}B)")
    elif op == 0x0033:
        log(f"{prefix}SYN_ATTRIBUTE ({len(pl)}B)")
    elif op == 0x0022:
        log(f"{prefix}*** 0x0022 SESSION ({len(pl)}B): {pl.hex()}")
    elif op in IMPORTANT_OPS:
        log(f"{prefix}{opname(op)} ({len(pl)}B): {pl[:20].hex() if pl else 'empty'}")
    elif op not in (0x0042, 0x036C, 0x0002, 0x0043):
        pass  # Don't log spam

def main():
    log("=== GATHER TEST v11 - Post-Gather Probe ===")

    # Login
    log("\n--- Login ---")
    access_key = node_login(EMAIL, PASSWORD, IGG_ID)
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
    result = recv_packet(sock, timeout=10)
    if result is None or result[0] != 0x0020:
        log(f"Login failed: {result}"); sock.close(); return
    log("Login OK")

    sock.sendall(build_world_entry(IGG_ID))
    start_time = time.time()

    # Init flood
    log("\n--- Init Flood ---")
    init_pkts = recv_flood(sock, timeout=5)
    log(f"Received {len(init_pkts)} init packets")

    server_key = extract_server_key(init_pkts)
    if server_key is None:
        log("ERROR: Server key not found!"); sock.close(); return
    log(f"Server key: 0x{server_key:08X}")
    codec = CMsgCodec.from_u32(server_key)

    # Check init for important packets
    has_0022 = False
    existing_marches = 0
    for op, pl in init_pkts:
        if op == 0x0022: has_0022 = True
        if op == 0x0071:
            existing_marches += 1
            log(f"  EXISTING MARCH: {pl[:30].hex()}")
        if op == 0x0636:
            log(f"  MARCH_DATA ({len(pl)}B): {pl[:40].hex()}")
        if op == 0x0768:
            log(f"  MARCH_SLOT ({len(pl)}B): {pl.hex()}")
        if op == 0x076A:
            log(f"  MARCH_QUEUE ({len(pl)}B): {pl.hex()}")
    log(f"  0x0022={'YES' if has_0022 else 'NO'}, existing_marches={existing_marches}")

    # Setup
    log("\n--- Setup ---")
    sock.sendall(build_packet(0x0840))
    sock.sendall(build_packet(0x17D4))
    sock.sendall(build_packet(0x0AF2))
    sock.sendall(build_packet(0x0245))
    sock.sendall(build_packet(0x0834, FORMATION_DATA))
    sock.sendall(build_packet(0x0709))
    sock.sendall(build_packet(0x0A2C))
    sock.sendall(build_packet(0x1357, bytes.fromhex("02000000")))
    sock.sendall(build_packet(0x170D, bytes.fromhex("02000000")))
    log("  Sent setup (0x0840..0x170D)")

    time.sleep(1)
    setup_pkts = recv_flood(sock, timeout=3)
    log(f"  Setup responses: {len(setup_pkts)} packets")

    # Extras
    ms = int((time.time() - start_time) * 1000)
    sock.sendall(build_packet(0x0043, struct.pack('<IIII', ms, 0, 0, 0)))
    sock.sendall(build_packet(0x0674))
    for tid in TROOP_IDS_PCAP:
        sock.sendall(build_packet(0x099D, struct.pack('<I', tid)))
    sock.sendall(build_packet(0x0767))
    sock.sendall(build_packet(0x0769))
    log("  Sent extras (0x0043..0x0769)")

    time.sleep(1)
    recv_flood(sock, timeout=2)

    # Heartbeat
    ms = int((time.time() - start_time) * 1000)
    sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
    sock.sendall(build_packet(0x0043, struct.pack('<IIII', ms, 0, 0, 0)))
    sock.sendall(build_packet(0x11FF, bytes.fromhex("01000000")))

    time.sleep(1)
    recv_flood(sock, timeout=2)

    # Enable view + search
    log("\n--- Enable View + Search ---")
    enable_data = bytearray(10)
    enable_data[0] = 0x01
    struct.pack_into('<I', enable_data, 1, IGG_ID)
    enable_data[9] = 0x01
    sock.sendall(codec.encode(OP_ENABLE_VIEW, bytes(enable_data)))
    sock.sendall(build_packet(0x006E, bytes.fromhex("43023e0301")))
    sock.sendall(build_packet(0x033E, bytes.fromhex("01040003")))

    time.sleep(2)
    view_pkts = recv_flood(sock, timeout=3)
    target_x, target_y = None, None
    for op, pl in view_pkts:
        if op == 0x033F and len(pl) >= 5:
            tx = struct.unpack('<H', pl[1:3])[0]
            ty = struct.unpack('<H', pl[3:5])[0]
            log(f"  Search result: ({tx},{ty})")
            if target_x is None:
                target_x, target_y = tx, ty

    if target_x is None:
        target_x, target_y = 644, 576
        log(f"  Using fallback target: ({target_x},{target_y})")

    sock.sendall(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 0x01)))
    log(f"  Viewing target tile ({target_x},{target_y})")

    # Pre-gather drain
    time.sleep(1)
    ms = int((time.time() - start_time) * 1000)
    sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
    time.sleep(2)
    recv_flood(sock, timeout=3)

    # ═══════════════════════════════════════════
    # GATHER
    # ═══════════════════════════════════════════
    log("\n" + "=" * 60)
    log("GATHER: hero=244, slot=2, NO 0x0323")
    log("=" * 60)

    march_slot = 2
    hero_id = 244
    gather_plain = build_gather_plain(target_x, target_y, hero_id=hero_id, march_slot=march_slot)
    log(f"  Plaintext: {gather_plain.hex()}")
    gather_pkt = codec.encode(OP_START_MARCH, gather_plain)
    sock.sendall(gather_pkt)
    log(f"  Sent 0x0CE8 ({len(gather_pkt)}B) to ({target_x},{target_y})")

    # Immediate response
    time.sleep(1)
    resp_pkts = recv_flood(sock, timeout=5)
    log(f"\n--- Immediate Response: {len(resp_pkts)} packets ---")
    got_0037_ok = False
    got_071 = False
    got_076c = False

    for op, pl in resp_pkts:
        log_packet(op, pl, "  ")
        if op == 0x0037 and len(pl) >= 12:
            status = struct.unpack('<I', pl[8:12])[0]
            if status == 0: got_0037_ok = True
        if op == 0x0071: got_071 = True
        if op == 0x076C: got_076c = True

    # ═══════════════════════════════════════════
    # POST-GATHER PROBING
    # ═══════════════════════════════════════════
    log(f"\n--- Post-Gather Probe ---")

    # Request march data
    sock.sendall(build_packet(0x0767))
    sock.sendall(build_packet(0x0769))
    log("  Sent 0x0767 + 0x0769 (march query)")

    time.sleep(2)
    march_pkts = recv_flood(sock, timeout=5)
    log(f"  March query response: {len(march_pkts)} packets")
    for op, pl in march_pkts:
        log_packet(op, pl, "    ")
        if op == 0x0071: got_071 = True
        if op == 0x076C: got_076c = True

    # Request view at target to see if troops are there
    sock.sendall(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 0x01)))
    log(f"  Re-sent 0x006E target ({target_x},{target_y})")

    time.sleep(2)
    tile_pkts = recv_flood(sock, timeout=3)
    log(f"  Tile response: {len(tile_pkts)} packets")
    for op, pl in tile_pkts:
        if op in (0x0076, 0x0077, 0x0078, 0x007A, 0x0071, 0x076C):
            log_packet(op, pl, "    ")
        if op == 0x0071: got_071 = True
        if op == 0x076C: got_076c = True

    # Extended wait with heartbeats (60 more seconds)
    log(f"\n--- Extended Wait (60s) ---")
    end_time = time.time() + 60
    while time.time() < end_time:
        pkts = recv_flood(sock, timeout=5)
        for op, pl in pkts:
            if op in IMPORTANT_OPS or op in (0x0076, 0x0077, 0x0032):
                log_packet(op, pl, "  ")
            if op == 0x0071: got_071 = True
            if op == 0x076C: got_076c = True

        if got_071 or got_076c:
            log("  *** MARCH DETECTED! ***")
            break

        # Heartbeat
        ms = int((time.time() - start_time) * 1000)
        sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))

    # Final summary
    log("\n" + "=" * 60)
    log(f"RESULT: 0x0037_OK={got_0037_ok} | 0x0071={got_071} | 0x076C={got_076c}")
    if got_071 or got_076c:
        log("*** GATHER SUCCEEDED! ***")
    elif got_0037_ok:
        log("Server accepted (status=0) but no march notification. Possible causes:")
        log("  - Troops not available for march")
        log("  - Formation data doesn't match account troops")
        log("  - March slot issue")
    else:
        log("Server rejected the gather.")
    log("=" * 60)

    sock.close()
    log("Done.")

if __name__ == '__main__':
    main()

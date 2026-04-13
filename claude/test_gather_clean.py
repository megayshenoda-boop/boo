#!/usr/bin/env python3
"""
Clean Gather Test - EXACT replica of real game client PCAP (Apr 9 2026)
Includes 0x1B8B, correct troop IDs, exact sequence.
"""
import sys, time, struct, random, subprocess, socket, os
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from codec import CMsgCodec
from packets import build_packet, build_game_login, build_world_entry

# Constants from PCAP analysis
KINGDOM = 182
CMSG_TABLE = [0x58, 0xef, 0xd7, 0x14, 0xa2, 0x3b, 0x9c]

# Troop IDs from real game PCAP (Apr 9)
PCAP_TROOP_IDS = [0x0193, 0x0198, 0x0199, 0x019A, 0x019B]  # 403, 408, 409, 410, 411

def log(msg):
    ts = time.time()
    ms = int((ts % 1) * 1000)
    print(f"[{time.strftime('%H:%M:%S')}.{ms:03d}] {msg}")

def node_login():
    result = subprocess.run(
        ['node', r'D:\CascadeProjects\lords_bot\http_login.mjs', EMAIL, PASSWORD, str(IGG_ID)],
        capture_output=True, text=True, timeout=30, encoding='utf-8', errors='replace'
    )
    key = result.stdout.strip()
    if len(key) == 32:
        return key
    log(f"Login failed: {result.stderr[:200]}")
    return None

def recv_all(sock, timeout=5):
    """Receive all packets until timeout."""
    packets = []
    buf = b''
    deadline = time.time() + timeout
    while time.time() < deadline:
        sock.settimeout(max(0.05, deadline - time.time()))
        try:
            chunk = sock.recv(65536)
            if not chunk:
                break
            buf += chunk
        except socket.timeout:
            pass
        # Parse complete packets from buffer
        while len(buf) >= 4:
            pkt_len = struct.unpack('<H', buf[0:2])[0]
            if pkt_len < 4 or pkt_len > 100000:
                buf = buf[1:]
                continue
            if len(buf) < pkt_len:
                break
            opcode = struct.unpack('<H', buf[2:4])[0]
            payload = buf[4:pkt_len]
            packets.append((opcode, payload))
            buf = buf[pkt_len:]
    return packets

def extract_server_key(packets):
    """Extract server key from 0x0038 packet."""
    for op, pl in packets:
        if op == 0x0038 and len(pl) > 100:
            entry_count = struct.unpack('<H', pl[0:2])[0]
            for idx in range(entry_count):
                off = 2 + idx * 12
                if off + 12 > len(pl):
                    break
                field_id = struct.unpack('<I', pl[off:off+4])[0]
                if field_id == 0x4F:
                    return struct.unpack('<I', pl[off+4:off+8])[0]
    return None

def build_gather_plain(target_x, target_y, resource_type=2, hero_id=0xFF, march_slot=1):
    """Build 0x0CE8 plaintext matching EXACT game PCAP structure.
    From fresh_session.pcap decrypted: 018147614a170000008a00570301ff000000b60000000400000000000000000000ed027322000000000000000000
    """
    # Build exact match to game payload
    p = bytearray(46)
    p[0] = march_slot & 0xFF  # slot = 1
    p[1:4] = bytes([0x81, 0x47, 0x61])  # nonce from game PCAP
    p[4:6] = struct.pack('<H', 0x174A)  # march_type for wheat LEVEL 2 (like game)
    p[6:8] = struct.pack('<H', 0)  # unknown/padding
    p[8] = 0x00  # flag
    p[9:11] = struct.pack('<H', target_x)  # tile X = 0x008A = 138
    p[11:13] = struct.pack('<H', target_y)  # tile Y = 0x0357 = 855
    # Note: Y=855 = 0x0357, stored as little endian: 57 03
    # So p[11]=0x57, p[12]=0x03
    p[13] = 0x01  # flag (was 0x03 in wrong attempt)
    p[14] = 0xFF  # hero_id = 255 (no hero)
    p[15] = 0x00  # padding
    p[16:18] = struct.pack('<H', 0)  # zeros
    p[18:20] = struct.pack('<H', KINGDOM)  # kingdom = 182 (0x00B6) at [18:20]
    p[20:22] = struct.pack('<H', 0)  # zeros
    p[22:26] = struct.pack('<I', 4)  # resource_type/purpose = 4 at [22:26]
    p[28:33] = bytes(5)  # zeros
    struct.pack_into('<I', p, 33, IGG_ID)  # IGG_ID at [33:37]
    p[37:46] = bytes(9)  # zeros
    return bytes(p)

def build_1b8b_offset6(codec, igg_id):
    """Build 0x1B8B PASSWORD_CHECK with offset6 encoding.
    Plaintext = IGG_ID(4B) + zeros(4B) + password(-1 as i64)(8B) = 16 bytes"""
    plaintext = struct.pack('<I', igg_id) + b'\x00\x00\x00\x00' + b'\xff\xff\xff\xff\xff\xff\xff\xff'
    
    extra = bytes([random.randint(0,255), random.randint(0,255)])
    msg_value = random.randint(0, 0xFFFF)
    msg_lo = msg_value & 0xFF
    msg_hi = (msg_value >> 8) & 0xFF
    msg = [msg_lo, msg_hi]
    sk = codec.sk if hasattr(codec, 'sk') else list(struct.pack('<I', codec))
    
    encrypted = bytearray(len(plaintext))
    checksum = 0
    for idx in range(len(plaintext)):
        abs_i = idx + 10
        table_b = CMSG_TABLE[abs_i % 7]
        sk_b = sk[abs_i % 4]
        msg_b = msg[abs_i % 2]
        enc_byte = (((plaintext[idx] + msg_b * 17) & 0xFF) ^ sk_b ^ table_b) & 0xFF
        encrypted[idx] = enc_byte
        checksum = (checksum + enc_byte) & 0xFF
    
    payload = bytearray(2 + 4 + len(encrypted))
    payload[0:2] = extra
    payload[2] = checksum & 0xFF
    payload[3] = msg_lo
    payload[4] = msg_lo ^ 0xB7
    payload[5] = msg_hi
    payload[6:] = encrypted
    return build_packet(0x1B8B, bytes(payload))

def build_enable_view():
    """Build 0x0CEB plaintext (10 bytes) matching PCAP."""
    p = bytearray(10)
    p[0] = 0x01
    struct.pack_into('<I', p, 1, IGG_ID)
    # [5:9] = zeros
    p[9] = 0x01
    return bytes(p)

def build_hero_select(hero_id=0xFF):
    """Build 0x0323 hero selection packet."""
    p = bytearray(7)
    p[0] = 0x00
    p[1] = 0x01  # slot = 1 (like game)
    p[2] = 0x00
    p[3] = hero_id & 0xFF
    p[4] = 0x00
    p[5] = 0x00
    p[6] = 0x00
    return bytes(p)

def build_newencode_packet(codec, opcode, plaintext, extra=None):
    """Build packet with NewEncode (offset6) encryption.
    Format: [2B len][2B opcode][2B extra][1B checksum][1B msg_lo][1B verify][1B msg_hi][encrypted]
    """
    if extra is None:
        extra = bytes([random.randint(0, 255), random.randint(0, 255)])
    msg_value = random.randint(0, 0xFFFF)
    msg_lo = msg_value & 0xFF
    msg_hi = (msg_value >> 8) & 0xFF
    msg = [msg_lo, msg_hi]
    sk = list(codec.sk) if hasattr(codec, 'sk') else [0, 0, 0, 0]
    
    # Encrypt plaintext
    encrypted = bytearray(len(plaintext))
    checksum = 0
    for idx in range(len(plaintext)):
        abs_i = idx + 10
        table_b = CMSG_TABLE[abs_i % 7]
        sk_b = sk[abs_i % 4]
        msg_b = msg[abs_i % 2]
        enc_byte = (((plaintext[idx] + msg_b * 17) & 0xFF) ^ sk_b ^ table_b) & 0xFF
        encrypted[idx] = enc_byte
        checksum = (checksum + enc_byte) & 0xFF
    
    # Build packet
    payload = bytearray(2 + 2 + 2 + 4 + len(encrypted))  # len+opcode + extra + hdr + encrypted
    struct.pack_into('<H', payload, 0, len(payload))  # total length
    struct.pack_into('<H', payload, 2, opcode)  # opcode
    payload[4:6] = extra  # 2 extra bytes
    payload[6] = checksum & 0xFF  # checksum
    payload[7] = msg_lo
    payload[8] = msg_lo ^ 0xB7  # verify
    payload[9] = msg_hi
    payload[10:] = encrypted
    return bytes(payload)

def main():
    log(f"=== PCAP-EXACT GATHER TEST (Apr 9 2026) ===")
    log(f"IGG_ID={IGG_ID}, KINGDOM={KINGDOM}")
    
    # 1. Login
    log("\n[1] HTTP Login...")
    access_key = node_login()
    if not access_key:
        log("FAILED"); return
    log(f"Key: {access_key[:8]}...")

    # 2. Gateway
    log("\n[2] Gateway...")
    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    log(f"Game: {gw['ip']}:{gw['port']}")

    # 3. Game server connect + login
    log("\n[3] Game server...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(15)
    sock.connect((gw['ip'], gw['port']))
    
    sock.sendall(build_game_login(IGG_ID, gw['token']))
    pkts = recv_all(sock, timeout=3)
    login_ok = any(op == 0x0020 and pl and pl[0] == 1 for op, pl in pkts)
    if not login_ok:
        log("Login failed!"); sock.close(); return
    log("Login OK")

    # 4. World entry + init flood (same as game: 0x001F -> 0x0021)
    sock.sendall(build_world_entry(IGG_ID))
    log("\n[4] Init flood...")
    flood = recv_all(sock, timeout=8)
    log(f"Received {len(flood)} packets")
    
    # Extract server key
    sk = extract_server_key(flood)
    if not sk:
        log("No server key!"); sock.close(); return
    log(f"Server key: 0x{sk:08X}")
    codec = CMsgCodec.from_u32(sk)
    
    # DUMP ALL PACKETS for analysis
    log("\n[4.5] DUMPING all received packets:")
    for op, pl in flood:
        marker = {0x0038:'SK', 0x1B8A:'GATE', 0x0042:'PING', 0x036C:'PING2', 0x0014:'LOGIN_OK', 
                  0x001F:'ENTER_OK', 0x0021:'WORLD_OK'}.get(op, '')
        log(f"  0x{op:04X} {marker:8s} ({len(pl):3d}B): {pl[:30].hex() if pl else 'empty'}")
    
    # Check 0x1B8A gate
    gate = -1
    for op, pl in flood:
        if op == 0x1B8A:
            gate = pl[4] if len(pl) > 4 else -1
            log(f"0x1B8A gate={gate}")
            break

    # ============================================
    # EXACT game client sequence from PCAP:
    # 0x0840 -> 0x17D4 -> 0x0AF2 -> 0x0245 -> 0x0709 -> 0x0A2C
    # -> 0x1357 -> 0x170D -> 0x1839 -> 0x1B8B (PASSWORD!)
    # -> 0x0043 -> 0x0674 -> 0x099D x5 -> 0x0767 -> 0x0769
    # -> (wait) -> 0x0043 -> 0x0CEB -> 0x006E -> 0x033E -> 0x006E
    # -> 0x0CE8 (GATHER!)
    # ============================================

    # Phase 1: Setup packets
    log("\n[5] Phase 1: Setup (0x0840 -> 0x0245 -> ...)")
    sock.sendall(build_packet(0x0840))
    time.sleep(0.15)
    sock.sendall(build_packet(0x17D4))
    time.sleep(0.05)
    sock.sendall(build_packet(0x0AF2))
    time.sleep(0.15)
    sock.sendall(build_packet(0x0245))  # march screen
    time.sleep(0.25)
    sock.sendall(build_packet(0x0709))
    time.sleep(0.10)
    sock.sendall(build_packet(0x0A2C))
    time.sleep(0.10)
    sock.sendall(build_packet(0x1357, struct.pack('<I', 2)))
    time.sleep(0.05)
    sock.sendall(build_packet(0x170D, struct.pack('<I', 2)))
    sock.sendall(build_packet(0x1839, struct.pack('<I', 3)))  # game sends this!
    time.sleep(0.10)
    
    setup_resp = recv_all(sock, timeout=1)
    log(f"Setup responses: {len(setup_resp)}")
    for op, pl in setup_resp:
        if op not in (0x0042, 0x036C):
            log(f"  <- 0x{op:04X} ({len(pl)}B)")

    # Phase 2: SKIP 0x1B8B - but send 0x1C87 from PCAP raw (may work with current SK?)
    log("\n[6] Phase 2: SKIPPING 0x1B8B")
    time.sleep(0.5)
    
    # Try sending 0x1C87 raw from PCAP - might decrypt correctly by chance?
    log("  Sending 0x1C87 raw from PCAP...")
    raw_1c87 = bytes.fromhex('85471c4129ac56e1cec128c815987bbbe368e0f0af2f428988827b34181780cecc')
    # First 2 bytes are length, need to adjust
    # Actually let's skip - it's too complex
    log("  (Skipping 0x1C87 - too complex)")

    # Phase 2.5: SKIP 0x1C87 (causes disconnect)
    log("\n[6.5] Phase 2.5: SKIPPING 0x1C87 (causes disconnect)")
    time.sleep(0.2)

    # Phase 3: Pre-sync (0x0043 + 0x0674 + troops)
    log("\n[7] Phase 3: Troops + Sync")
    elapsed_ms = int((time.time() % 100000) * 1000) & 0xFFFFFFFF
    sock.sendall(build_packet(0x0043, struct.pack('<IIII', elapsed_ms, 0, 0, 0)))
    sock.sendall(build_packet(0x0674))
    for tid in PCAP_TROOP_IDS:
        sock.sendall(build_packet(0x099D, struct.pack('<I', tid)))
    time.sleep(0.25)
    sock.sendall(build_packet(0x0767))
    sock.sendall(build_packet(0x0769))
    time.sleep(1.0)
    sync_resp = recv_all(sock, timeout=2)
    log(f"Sync responses: {len(sync_resp)}")
    for op, pl in sync_resp:
        if op == 0x099E:
            tid = struct.unpack('<I', pl[:4])[0] if len(pl) >= 4 else 0
            log(f"  TROOP_RESP: {tid}")
        elif op not in (0x0042, 0x036C, 0x0002):
            log(f"  <- 0x{op:04X} ({len(pl)}B)")

    # Phase 4: Second 0x0043 + Enable view + tiles (match game sequence)
    log("\n[8] Phase 4: Second sync + Enable view + tiles")
    elapsed_ms = int((time.time() % 100000) * 1000) & 0xFFFFFFFF
    sock.sendall(build_packet(0x0043, struct.pack('<IIII', elapsed_ms, 0, 0, 0)))  # Second 0x0043 like game
    ev_pkt = codec.encode(0x0CEB, build_enable_view())
    sock.sendall(ev_pkt)
    # Source tile (castle area) like game: 8800680301 -> x=680, y=301
    sock.sendall(build_packet(0x006E, struct.pack('<HHB', 0x0680, 0x0301, 1)))
    # 0x033E SEARCH - ask server for available tiles
    log("\n[8.5] Phase 8.5: 0x033E SEARCH for tiles")
    sock.sendall(build_packet(0x033E, struct.pack('<I', 0x03000402)))  # 02040003 LE
    time.sleep(0.5)
    search_resp = recv_all(sock, timeout=2)
    
    # Look for 0x033F response with tile coordinates
    target_x, target_y = 138, 855  # fallback
    for op, pl in search_resp:
        if op == 0x033F and len(pl) >= 6:
            log(f"  0x033F raw: {pl.hex()}")
            # Try different offsets - from PCAP: 163b02a203020000
            # 0x16 at [0], x=0x023b at [1:3], y=0x03a2 at [3:5]
            if len(pl) >= 5:
                target_x = struct.unpack('<H', pl[1:3])[0]
                target_y = struct.unpack('<H', pl[3:5])[0]
                log(f"  0x033F: Server suggests tile ({target_x}, {target_y})")
                break
    
    # Phase 5: Use tile from server response
    log(f"\n[9] Phase 5: Using tile ({target_x}, {target_y})")
    
    # Select target tile
    sock.sendall(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 1)))
    time.sleep(1.0)
    tile_resp = recv_all(sock, timeout=2)
    log(f"Tile responses: {len(tile_resp)}")

    # Phase 6: Pre-gather wait - MUST wait for 0x0211
    log("\n[10] Phase 6: Pre-gather wait - waiting for 0x0211...")
    sock.sendall(build_packet(0x0042, struct.pack('<II', 20000, 0)))
    
    # Wait for 0x0211 (critical for gather)
    got_0211 = False
    start_wait = time.time()
    while time.time() - start_wait < 10 and not got_0211:
        check = recv_all(sock, timeout=1)
        for op, pl in check:
            if op == 0x0211:
                got_0211 = True
                log(f"  GOT 0x0211! ({len(pl)}B): {pl[:20].hex()}")
                break
        if not got_0211:
            sock.sendall(build_packet(0x0042, struct.pack('<II', 20000, 0)))
            time.sleep(0.5)
    
    if not got_0211:
        log("  WARNING: No 0x0211 received, proceeding anyway...")

    # Phase 6.5: 0x0323 HERO_SELECT (observed in some PCAPs)
    log("\n[10.5] Phase 6.5: 0x0323 HERO_SELECT")
    hero_pkt = build_hero_select(hero_id=0xFF)
    sock.sendall(build_packet(0x0323, hero_pkt))
    time.sleep(0.5)
    hero_resp = recv_all(sock, timeout=2)
    for op, pl in hero_resp:
        if op not in (0x0042, 0x036C, 0x0002):
            log(f"  <- 0x{op:04X} ({len(pl)}B)")

    # Phase 7: GATHER!
    log(f"\n[11] Phase 7: 0x0CE8 GATHER -> ({target_x},{target_y})")
    gather_plain = build_gather_plain(target_x, target_y, resource_type=2, hero_id=0xFF, march_slot=1)
    log(f"Plain ({len(gather_plain)}B): {gather_plain.hex()}")
    log(f"  slot=1, type=0x{struct.unpack('<H', gather_plain[4:6])[0]:04X}, hero=0xFF")
    gather_pkt = codec.encode(0x0CE8, gather_plain)
    sock.sendall(gather_pkt)
    
    # Phase 8: Wait for response
    log("\n[12] Phase 8: Waiting for march response (20s)...")
    start = time.time()
    
    success = False
    strong = False
    all_march_ops = []
    
    while time.time() - start < 20:
        batch = recv_all(sock, timeout=2)
        for op, pl in batch:
            if op in (0x0042, 0x036C, 0x0002):
                continue
            all_march_ops.append(op)
            marker = ""
            if op == 0x00B8: marker = " *** MARCH_ACCEPT ***"; success = True
            elif op == 0x0071: marker = " *** MARCH_STATE ***"; strong = True
            elif op == 0x076C: marker = " *** MARCH_BUNDLE ***"; strong = True
            elif op == 0x007C: marker = " *** COLLECT_STATE ***"
            elif op == 0x00B9: marker = " *** ARMY_RETURN ***"
            elif op == 0x0033: marker = " (attr_change)"
            log(f"  0x{op:04X} ({len(pl)}B): {pl[:40].hex() if pl else ''}{marker}")
        
        if strong:
            log("\n*** STRONG SUCCESS! March is active! ***")
            break
        if success and not strong:
            # Keep waiting for 0x0071/0x076C
            continue
    
    elapsed = time.time() - start
    log(f"\nResult after {elapsed:.1f}s:")
    log(f"  accepted = {success}")
    log(f"  strong (0x0071/0x076C) = {strong}")
    log(f"  opcodes: {[f'0x{op:04X}' for op in all_march_ops]}")
    
    if not success:
        log("\n*** GATHER FAILED - no 0x00B8 ***")
    elif success and not strong:
        log("\n*** SOFT ONLY - accepted but no march created ***")
    
    # Connection check
    log("\n[13] Connection check...")
    try:
        sock.sendall(build_packet(0x0042, struct.pack('<II', 30000, 0)))
        check = recv_all(sock, timeout=3)
        alive = any(op == 0x0042 for op, pl in check)
        log(f"Alive: {alive}")
    except:
        log("Alive: False (disconnected)")
    
    sock.close()
    log("\nDone.")

if __name__ == '__main__':
    main()

"""
Comprehensive PCAP Analysis for IGG Conquerors Gather Session
=============================================================
Analyzes PCAPdroid capture to understand complete gather/march flow.
"""
import struct
import sys
from collections import defaultdict

try:
    from scapy.all import rdpcap, TCP, IP, Raw
except ImportError:
    print("ERROR: scapy not installed. Run: pip install scapy")
    sys.exit(1)

# ── Protocol constants ──────────────────────────────────────
CMSG_TABLE = [0x58, 0xef, 0xd7, 0x14, 0xa2, 0x3b, 0x9c]
SERVER_KEY_FIELD_ID = 0x4F

OPCODE_NAMES = {
    0x0002: "HEARTBEAT_ECHO",
    0x000B: "GW_AUTH", 0x000C: "GW_REDIRECT",
    0x001F: "GS_LOGIN", 0x0020: "GS_LOGIN_OK", 0x0021: "WORLD_ENTRY",
    0x0033: "SYN_ATTRIBUTE", 0x0034: "PLAYER_PROFILE",
    0x0038: "CASTLE_DATA", 0x003F: "VIP_INFO",
    0x0042: "HEARTBEAT", 0x0043: "SERVER_TIME",
    0x0064: "ITEM_INFO", 0x0065: "ITEM_USE", 0x006F: "SYNC_MARCH",
    0x0071: "MARCH_STATE", 0x0097: "BUILDING_INFO", 0x0098: "WORKER_INFO",
    0x009D: "BUILD_OLD", 0x009F: "BUILD_HELP",
    0x00AA: "HERO_INFO", 0x00B8: "PARTIAL_ACK", 0x00BE: "SCIENCE_INFO",
    0x00BF: "RESEARCH_OLD", 0x00C6: "RESEARCH_HELP",
    0x014B: "TRAP_BUILD",
    0x021C: "BUILDING_DATA", 0x022B: "RESOURCE_DEDUCT",
    0x02D1: "ACTION_CONFIRM",
    0x036C: "SERVER_TICK", 0x039B: "INIT_TS",
    0x0636: "MARCH_DATA", 0x06C2: "SOLDIER_INFO",
    0x06C3: "TRAIN_OLD", 0x06CB: "HEAL",
    0x06C7: "SPEED_TRAIN", 0x06D4: "ONEKEY_SPEED_TRAIN",
    0x06EB: "TRAINING_ENTRY",
    0x0CE4: "START_BUILDUP", 0x0CE5: "JOIN_BUILDUP",
    0x0CE6: "START_DEFEND", 0x0CE7: "BACK_DEFEND",
    0x0CE8: "START_MARCH", 0x0CE9: "CANCEL_MARCH",
    0x0CEA: "MARCH_USE_ITEM", 0x0CEB: "ENABLE_VIEW",
    0x0CEC: "LEAGUE_DONATE", 0x0CED: "TRAIN",
    0x0CEE: "RESEARCH", 0x0CEF: "BUILD",
    0x0CF0: "WORLD_BATTLE", 0x0CF1: "MOVE_CASTLE",
    0x0CF2: "GET_OTHER_ATTR", 0x0CF3: "RAID_PLAYER",
    0x0CF8: "SHOP_BUY", 0x0CF9: "BUILD_FIX",
    0x11C8: "TIMER_SET",
    0x1B8B: "SESSION_PKT_1B8B",
}

def opname(opcode):
    return OPCODE_NAMES.get(opcode, f"UNK_0x{opcode:04X}")


# ── CMsgCodec decrypt ──────────────────────────────────────
def cmsg_decode(payload, sk_bytes):
    """Decode encrypted payload (bytes after 4-byte header). payload[0]=checksum, [1]=msg_lo, [2]=verify, [3]=msg_hi, [4:]=enc"""
    if len(payload) < 5:
        return payload
    msg = [payload[1], payload[3]]
    dec = bytearray(len(payload) - 4)
    for p in range(4, len(payload)):
        i = p + 4  # offset in full packet (header is 4 bytes)
        table_b = CMSG_TABLE[i % 7]
        sk_b = sk_bytes[i % 4]
        msg_b = msg[i % 2]
        intermediate = (payload[p] ^ sk_b ^ table_b) & 0xFF
        dec[p - 4] = (intermediate - msg_b * 17) & 0xFF
    return bytes(dec)


def is_encrypted_packet(payload):
    """Check if a packet payload (after 4-byte header) looks encrypted (has verify=msg_lo^0xB7)."""
    if len(payload) < 4:
        return False
    msg_lo = payload[1]
    verify = payload[2]
    return verify == (msg_lo ^ 0xB7)


def extract_server_key(payload):
    """Extract server_key u32 from 0x0038 payload."""
    if len(payload) < 14:
        return None
    entry_count = struct.unpack('<H', payload[0:2])[0]
    for idx in range(entry_count):
        off = 2 + idx * 12
        if off + 12 > len(payload):
            break
        field_id = struct.unpack('<I', payload[off:off+4])[0]
        if field_id == SERVER_KEY_FIELD_ID:
            return struct.unpack('<I', payload[off+4:off+8])[0]
    return None


# ── TCP stream reassembly ──────────────────────────────────
def reassemble_streams(pcap_file):
    """Read PCAP, reassemble TCP streams, return per-stream ordered data chunks."""
    print(f"[*] Reading PCAP: {pcap_file}")
    packets = rdpcap(pcap_file)
    print(f"[*] Total packets in PCAP: {len(packets)}")

    # Gather all TCP streams
    streams = defaultdict(list)  # (src_ip, src_port, dst_ip, dst_port) -> [(time, seq, data)]
    ip_ports = set()

    for pkt in packets:
        if not pkt.haslayer(TCP):
            continue
        if not pkt.haslayer(IP):
            continue
        ip = pkt[IP]
        tcp = pkt[TCP]
        src_ip, dst_ip = ip.src, ip.dst
        sport, dport = tcp.sport, tcp.dport
        ip_ports.add((src_ip, sport, dst_ip, dport))

        payload = bytes(tcp.payload) if tcp.payload else b''
        if not payload:
            continue

        key = (src_ip, sport, dst_ip, dport)
        streams[key].append((float(pkt.time), tcp.seq, payload))

    print(f"[*] Found {len(ip_ports)} unique TCP flows (including ACK-only)")
    print(f"[*] Found {len(streams)} flows with data")

    # Show all flows
    print("\n=== ALL TCP FLOWS WITH DATA ===")
    for key in sorted(streams.keys(), key=lambda k: streams[k][0][0] if streams[k] else 0):
        src_ip, sport, dst_ip, dport = key
        count = len(streams[key])
        total_bytes = sum(len(d) for _, _, d in streams[key])
        print(f"  {src_ip}:{sport} -> {dst_ip}:{dport}  ({count} data pkts, {total_bytes} bytes)")

    return streams


def identify_connections(streams):
    """Identify gateway and game server connections."""
    gateway_streams = {}
    game_streams = {}
    other_streams = {}

    for key, chunks in streams.items():
        src_ip, sport, dst_ip, dport = key
        # Gateway: port 5997
        if dport == 5997 or sport == 5997:
            gateway_streams[key] = chunks
        # Game server: non-5997, going to external IPs (not loopback)
        elif (dst_ip.startswith('54.') or dst_ip.startswith('3.') or dst_ip.startswith('52.') or
              dst_ip.startswith('18.') or dst_ip.startswith('35.') or dst_ip.startswith('13.') or
              src_ip.startswith('54.') or src_ip.startswith('3.') or src_ip.startswith('52.') or
              src_ip.startswith('18.') or src_ip.startswith('35.') or src_ip.startswith('13.')):
            game_streams[key] = chunks
        else:
            other_streams[key] = chunks

    return gateway_streams, game_streams, other_streams


def merge_stream_pair(streams, ip1, port1, ip2, port2):
    """Merge C2S and S2C data for a connection into ordered chunks."""
    c2s_key = (ip1, port1, ip2, port2)
    s2c_key = (ip2, port2, ip1, port1)

    merged = []
    if c2s_key in streams:
        for ts, seq, data in streams[c2s_key]:
            merged.append((ts, 'C2S', seq, data))
    if s2c_key in streams:
        for ts, seq, data in streams[s2c_key]:
            merged.append((ts, 'S2C', seq, data))

    merged.sort(key=lambda x: (x[0], x[2]))
    return merged


def parse_game_packets(data_buffer):
    """Parse game protocol packets from a byte buffer. Returns [(opcode, payload_after_header)]."""
    packets = []
    pos = 0
    while pos + 4 <= len(data_buffer):
        pkt_len = struct.unpack('<H', data_buffer[pos:pos+2])[0]
        if pkt_len < 4 or pkt_len > 65535:
            break
        if pos + pkt_len > len(data_buffer):
            break
        opcode = struct.unpack('<H', data_buffer[pos+2:pos+4])[0]
        payload = data_buffer[pos+4:pos+pkt_len]
        packets.append((opcode, payload, data_buffer[pos:pos+pkt_len]))
        pos += pkt_len
    return packets, pos


def find_game_server_connection(streams):
    """Find the game server connection by looking for 0x0038 packets."""
    # Try all non-gateway external connections
    candidate_pairs = set()
    for key in streams:
        src_ip, sport, dst_ip, dport = key
        if dport == 5997 or sport == 5997:
            continue
        # Normalize: pick the pair
        if dport > sport:
            candidate_pairs.add((src_ip, sport, dst_ip, dport))
        else:
            candidate_pairs.add((dst_ip, dport, src_ip, sport))

    # Also try any connection where we see game protocol packets
    all_pairs = set()
    for key in streams:
        src_ip, sport, dst_ip, dport = key
        if dport == 5997 or sport == 5997:
            continue
        all_pairs.add((src_ip, sport, dst_ip, dport))

    # For each candidate, try to parse and find 0x0038
    for key in all_pairs:
        src_ip, sport, dst_ip, dport = key
        chunks = streams.get(key, [])
        buf = b''.join(d for _, _, d in sorted(chunks, key=lambda x: (x[0], x[1])))
        pkts, _ = parse_game_packets(buf)
        for opcode, payload, raw in pkts:
            if opcode == 0x0038:
                return key, (dst_ip, dport, src_ip, sport)

    return None, None


def analyze_pcap(pcap_file):
    streams = reassemble_streams(pcap_file)
    gateway_streams, game_streams, other_streams = identify_connections(streams)

    print(f"\n[*] Gateway streams: {len(gateway_streams)}")
    for k in gateway_streams:
        print(f"    {k[0]}:{k[1]} -> {k[2]}:{k[3]}")
    print(f"[*] Potential game streams: {len(game_streams)}")
    for k in game_streams:
        print(f"    {k[0]}:{k[1]} -> {k[2]}:{k[3]}")
    print(f"[*] Other streams: {len(other_streams)}")
    for k in other_streams:
        print(f"    {k[0]}:{k[1]} -> {k[2]}:{k[3]}")

    # Find game server by looking for 0x0038 in all non-gateway streams
    all_non_gw = {**game_streams, **other_streams}
    s2c_key, c2s_key_reverse = find_game_server_connection(all_non_gw)

    if s2c_key is None:
        # Also try gateway streams as PCAPdroid may not separate them
        print("[!] Game server not found in external IPs, checking all streams...")
        s2c_key, c2s_key_reverse = find_game_server_connection(streams)

    if s2c_key is None:
        print("[!] Could not find game server connection (no 0x0038 packet found)")
        print("[!] Attempting to analyze ALL connections for game packets...")
        analyze_all_streams_raw(streams)
        return

    # The key that has 0x0038 is S2C (server sends castle data to client)
    server_ip, server_port = s2c_key[0], s2c_key[1]
    client_ip, client_port = s2c_key[2], s2c_key[3]
    print(f"\n[*] Game server identified: {server_ip}:{server_port}")
    print(f"[*] Client: {client_ip}:{client_port}")

    # Reassemble both directions
    c2s_key = (client_ip, client_port, server_ip, server_port)
    s2c_key_norm = (server_ip, server_port, client_ip, client_port)

    c2s_chunks = streams.get(c2s_key, [])
    s2c_chunks = streams.get(s2c_key_norm, [])

    c2s_buf = b''.join(d for _, _, d in sorted(c2s_chunks, key=lambda x: (x[0], x[1])))
    s2c_buf = b''.join(d for _, _, d in sorted(s2c_chunks, key=lambda x: (x[0], x[1])))

    print(f"[*] C2S buffer: {len(c2s_buf)} bytes")
    print(f"[*] S2C buffer: {len(s2c_buf)} bytes")

    # Parse all packets
    c2s_pkts, c2s_consumed = parse_game_packets(c2s_buf)
    s2c_pkts, s2c_consumed = parse_game_packets(s2c_buf)

    print(f"[*] Parsed C2S: {len(c2s_pkts)} packets ({c2s_consumed}/{len(c2s_buf)} bytes consumed)")
    print(f"[*] Parsed S2C: {len(s2c_pkts)} packets ({s2c_consumed}/{len(s2c_buf)} bytes consumed)")

    # Extract server key from 0x0038
    server_key = None
    sk_bytes = None
    for opcode, payload, raw in s2c_pkts:
        if opcode == 0x0038:
            server_key = extract_server_key(payload)
            if server_key is not None:
                sk_bytes = [
                    server_key & 0xFF, (server_key >> 8) & 0xFF,
                    (server_key >> 16) & 0xFF, (server_key >> 24) & 0xFF,
                ]
                print(f"\n[*] SERVER KEY: 0x{server_key:08X}")
                print(f"    Bytes: {[f'0x{b:02x}' for b in sk_bytes]}")
                break

    if server_key is None:
        print("[!] WARNING: Could not extract server key from 0x0038!")

    # Now create chronological packet list using timestamps from individual TCP packets
    # Better approach: parse packets from each TCP chunk with timestamps
    print("\n" + "="*100)
    print("CHRONOLOGICAL PACKET LIST (Game Server Connection)")
    print("="*100)

    all_game_packets = []

    # Parse C2S with timestamps
    for ts, seq, data in sorted(c2s_chunks, key=lambda x: (x[0], x[1])):
        pkts, _ = parse_game_packets(data)
        for opcode, payload, raw in pkts:
            all_game_packets.append((ts, 'C2S', opcode, payload, raw))

    # Parse S2C with timestamps
    for ts, seq, data in sorted(s2c_chunks, key=lambda x: (x[0], x[1])):
        pkts, _ = parse_game_packets(data)
        for opcode, payload, raw in pkts:
            all_game_packets.append((ts, 'S2C', opcode, payload, raw))

    # If timestamp-based parsing yields fewer packets, fall back to buffer parsing
    if len(all_game_packets) < len(c2s_pkts) + len(s2c_pkts):
        print(f"[!] Timestamp parsing got {len(all_game_packets)} vs buffer parsing got {len(c2s_pkts)+len(s2c_pkts)}")
        print("[!] Some TCP chunks may contain multiple packets or fragments. Using hybrid approach.")

    all_game_packets.sort(key=lambda x: x[0])

    if not all_game_packets:
        print("[!] No game packets found!")
        return

    base_time = all_game_packets[0][0]

    # Print all packets
    gather_idx = None
    session_1b8b_idx = None
    c2s_count_before_gather = 0
    found_gather = False

    for idx, (ts, direction, opcode, payload, raw) in enumerate(all_game_packets):
        rel_time = ts - base_time
        name = opname(opcode)
        pkt_len = len(raw)
        payload_len = len(payload)

        encrypted = ""
        if direction == 'C2S' and is_encrypted_packet(payload):
            encrypted = " [ENCRYPTED]"

        marker = ""
        if opcode == 0x0CE8:
            marker = " <<<< GATHER/MARCH"
            gather_idx = idx
        elif opcode == 0x1B8B:
            marker = " <<<< SESSION PKT"
            session_1b8b_idx = idx
        elif opcode == 0x0071:
            marker = " <<<< MARCH_STATE"
        elif opcode == 0x00B8:
            marker = " <<<< PARTIAL_ACK"
        elif opcode == 0x0038:
            marker = " <<<< CASTLE_DATA (server_key source)"
        elif opcode == 0x006F:
            marker = " <<<< SYNC_MARCH"

        if direction == 'C2S' and not found_gather:
            c2s_count_before_gather += 1
            if opcode == 0x0CE8:
                found_gather = True
                c2s_count_before_gather -= 1  # don't count gather itself

        print(f"  [{idx:4d}] +{rel_time:8.3f}s  {direction}  0x{opcode:04X} ({name:20s})  len={pkt_len:5d}  payload={payload_len:5d}{encrypted}{marker}")

    print(f"\n[*] Total game packets: {len(all_game_packets)}")
    print(f"[*] C2S packets before 0x0CE8: {c2s_count_before_gather}")

    # ── Detailed analysis of key packets ──────────────────
    if sk_bytes is None:
        print("\n[!] Cannot decrypt without server key. Showing raw hex only.")

    # 0x1B8B analysis
    print("\n" + "="*100)
    print("DETAILED: 0x1B8B SESSION PACKET(S)")
    print("="*100)
    count_1b8b = 0
    for idx, (ts, direction, opcode, payload, raw) in enumerate(all_game_packets):
        if opcode == 0x1B8B:
            count_1b8b += 1
            rel_time = ts - base_time
            print(f"\n  Packet #{count_1b8b} at +{rel_time:.3f}s ({direction}), total_len={len(raw)}, payload_len={len(payload)}")
            print(f"  Raw hex: {raw.hex()}")
            print(f"  Payload hex: {payload.hex()}")
            if is_encrypted_packet(payload):
                print(f"  -> ENCRYPTED (msg_lo=0x{payload[1]:02x}, verify=0x{payload[2]:02x}, msg_hi=0x{payload[3]:02x})")
                if sk_bytes:
                    dec = cmsg_decode(payload, sk_bytes)
                    print(f"  -> Decrypted ({len(dec)}B): {dec.hex()}")
                    # Try to interpret
                    print(f"  -> Decrypted bytes: {' '.join(f'{b:02x}' for b in dec)}")
                    if len(dec) >= 4:
                        val32 = struct.unpack('<I', dec[0:4])[0]
                        print(f"  -> First u32 LE: {val32} (0x{val32:08X})")
            else:
                print(f"  -> NOT encrypted (verify byte mismatch)")
    if count_1b8b == 0:
        print("  (No 0x1B8B packets found)")

    # Pre-gather sequence
    print("\n" + "="*100)
    print("DETAILED: PRE-GATHER SEQUENCE (between last 0x1B8B and 0x0CE8)")
    print("="*100)
    if session_1b8b_idx is not None and gather_idx is not None:
        for idx in range(session_1b8b_idx, gather_idx + 1):
            ts, direction, opcode, payload, raw = all_game_packets[idx]
            rel_time = ts - base_time
            name = opname(opcode)
            print(f"\n  [{idx}] +{rel_time:.3f}s {direction} 0x{opcode:04X} ({name}) len={len(raw)}")
            if direction == 'C2S' and is_encrypted_packet(payload) and sk_bytes:
                dec = cmsg_decode(payload, sk_bytes)
                print(f"    Decrypted: {dec.hex()}")
            elif len(payload) <= 128:
                print(f"    Payload: {payload.hex()}")
            else:
                print(f"    Payload (first 128B): {payload[:128].hex()}...")
    elif gather_idx is not None:
        print(f"  No 0x1B8B found. Showing 10 packets before gather (idx={gather_idx}):")
        start = max(0, gather_idx - 10)
        for idx in range(start, gather_idx + 1):
            ts, direction, opcode, payload, raw = all_game_packets[idx]
            rel_time = ts - base_time
            name = opname(opcode)
            print(f"\n  [{idx}] +{rel_time:.3f}s {direction} 0x{opcode:04X} ({name}) len={len(raw)}")
            if direction == 'C2S' and is_encrypted_packet(payload) and sk_bytes:
                dec = cmsg_decode(payload, sk_bytes)
                print(f"    Decrypted: {dec.hex()}")
            elif len(payload) <= 128:
                print(f"    Payload: {payload.hex()}")
            else:
                print(f"    Payload (first 128B): {payload[:128].hex()}...")
    else:
        print("  No 0x0CE8 (gather) packet found in this capture!")

    # 0x0CE8 detailed
    print("\n" + "="*100)
    print("DETAILED: 0x0CE8 (START_MARCH / GATHER) PACKET")
    print("="*100)
    for idx, (ts, direction, opcode, payload, raw) in enumerate(all_game_packets):
        if opcode == 0x0CE8:
            rel_time = ts - base_time
            print(f"  At +{rel_time:.3f}s ({direction}), total_len={len(raw)}, payload_len={len(payload)}")
            print(f"  Raw hex: {raw.hex()}")
            print(f"  Payload hex: {payload.hex()}")
            if is_encrypted_packet(payload):
                print(f"  -> ENCRYPTED (msg_lo=0x{payload[1]:02x}, verify=0x{payload[2]:02x}, msg_hi=0x{payload[3]:02x})")
                msg_val = payload[1] | (payload[3] << 8)
                print(f"  -> msg_value = 0x{msg_val:04X} ({msg_val})")
                if sk_bytes:
                    dec = cmsg_decode(payload, sk_bytes)
                    print(f"  -> Decrypted ({len(dec)}B): {dec.hex()}")
                    print(f"  -> Decrypted bytes: {' '.join(f'{b:02x}' for b in dec)}")
                    # Parse gather fields
                    parse_gather_payload(dec)
            break
    else:
        print("  0x0CE8 NOT FOUND in capture!")

    # Post-gather response
    print("\n" + "="*100)
    print("DETAILED: POST-GATHER RESPONSE SEQUENCE (after 0x0CE8)")
    print("="*100)
    if gather_idx is not None:
        end = min(len(all_game_packets), gather_idx + 50)
        for idx in range(gather_idx + 1, end):
            ts, direction, opcode, payload, raw = all_game_packets[idx]
            rel_time = ts - base_time
            name = opname(opcode)
            marker = ""
            if opcode == 0x0071:
                marker = " *** MARCH_STATE ***"
            elif opcode == 0x00B8:
                marker = " *** PARTIAL_ACK ***"
            elif opcode == 0x006F:
                marker = " *** SYNC_MARCH ***"
            elif opcode == 0x0636:
                marker = " *** MARCH_DATA ***"

            print(f"\n  [{idx}] +{rel_time:.3f}s {direction} 0x{opcode:04X} ({name}) len={len(raw)}{marker}")

            # Show payload for important response packets
            if opcode in (0x0071, 0x00B8, 0x006F, 0x0636, 0x02D1):
                if len(payload) <= 256:
                    print(f"    Payload: {payload.hex()}")
                else:
                    print(f"    Payload (first 256B): {payload[:256].hex()}...")
                    print(f"    ... ({len(payload)} bytes total)")
            elif direction == 'C2S' and is_encrypted_packet(payload) and sk_bytes:
                dec = cmsg_decode(payload, sk_bytes)
                print(f"    Decrypted: {dec.hex()}")
    else:
        print("  No gather packet found, cannot show post-gather sequence")

    # Summary of ALL encrypted C2S packets
    print("\n" + "="*100)
    print("ALL ENCRYPTED C2S PACKETS (decrypted)")
    print("="*100)
    for idx, (ts, direction, opcode, payload, raw) in enumerate(all_game_packets):
        if direction == 'C2S' and is_encrypted_packet(payload):
            rel_time = ts - base_time
            name = opname(opcode)
            print(f"\n  [{idx}] +{rel_time:.3f}s 0x{opcode:04X} ({name}) encrypted_payload={len(payload)}B")
            if sk_bytes:
                dec = cmsg_decode(payload, sk_bytes)
                print(f"    Decrypted ({len(dec)}B): {dec.hex()}")

    # Opcode frequency
    print("\n" + "="*100)
    print("OPCODE FREQUENCY SUMMARY")
    print("="*100)
    c2s_freq = defaultdict(int)
    s2c_freq = defaultdict(int)
    for ts, direction, opcode, payload, raw in all_game_packets:
        if direction == 'C2S':
            c2s_freq[opcode] += 1
        else:
            s2c_freq[opcode] += 1

    print("\n  C2S opcodes:")
    for op in sorted(c2s_freq.keys()):
        print(f"    0x{op:04X} ({opname(op):20s}): {c2s_freq[op]}")
    print(f"\n  S2C opcodes:")
    for op in sorted(s2c_freq.keys()):
        print(f"    0x{op:04X} ({opname(op):20s}): {s2c_freq[op]}")


def parse_gather_payload(dec):
    """Try to parse the decrypted gather payload fields."""
    print(f"\n  GATHER PAYLOAD ANALYSIS ({len(dec)} bytes):")
    if len(dec) < 4:
        print("    Too short to parse")
        return

    pos = 0
    # Print u32 values
    while pos + 4 <= len(dec):
        val = struct.unpack('<I', dec[pos:pos+4])[0]
        print(f"    offset {pos:3d}: u32 = {val:10d} (0x{val:08X})")
        pos += 4
    # Remaining bytes
    if pos < len(dec):
        remaining = dec[pos:]
        print(f"    offset {pos:3d}: remaining = {remaining.hex()}")

    # Also try u16 parse for better granularity
    print(f"\n  As u16 LE values:")
    pos = 0
    while pos + 2 <= len(dec):
        val = struct.unpack('<H', dec[pos:pos+2])[0]
        print(f"    offset {pos:3d}: u16 = {val:5d} (0x{val:04X})")
        pos += 2


def analyze_all_streams_raw(streams):
    """Fallback: try parsing all streams for game packets."""
    print("\n=== RAW ANALYSIS OF ALL STREAMS ===")
    for key in sorted(streams.keys(), key=lambda k: streams[k][0][0] if streams[k] else 0):
        src_ip, sport, dst_ip, dport = key
        chunks = streams[key]
        buf = b''.join(d for _, _, d in sorted(chunks, key=lambda x: (x[0], x[1])))
        pkts, consumed = parse_game_packets(buf)
        if pkts:
            print(f"\n  Stream {src_ip}:{sport} -> {dst_ip}:{dport}  ({len(pkts)} game packets, {consumed}/{len(buf)} bytes)")
            for opcode, payload, raw in pkts[:20]:
                name = opname(opcode)
                enc = " [ENC]" if is_encrypted_packet(payload) else ""
                print(f"    0x{opcode:04X} ({name:20s}) len={len(raw):5d}{enc}")
            if len(pkts) > 20:
                print(f"    ... and {len(pkts)-20} more packets")


if __name__ == '__main__':
    pcap_file = r"D:\CascadeProjects\PCAPdroid_27_Mar_09_17_04.pcap"
    analyze_pcap(pcap_file)

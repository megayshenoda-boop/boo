"""
Fresh PCAP Analyzer - Parse gather PCAP from scratch
No assumptions, no existing analysis. Extract everything.
"""
import struct
import sys

def read_pcap(filepath):
    """Read PCAP file, return list of (timestamp, src_port, dst_port, data) for TCP packets."""
    with open(filepath, 'rb') as f:
        # PCAP global header (24 bytes)
        magic = struct.unpack('<I', f.read(4))[0]
        if magic == 0xa1b2c3d4:
            endian = '<'
        elif magic == 0xd4c3b2a1:
            endian = '>'
        else:
            print(f"Unknown magic: {magic:#x}")
            return []

        ver_major, ver_minor = struct.unpack(endian + 'HH', f.read(4))
        thiszone, sigfigs = struct.unpack(endian + 'II', f.read(8))
        snaplen, network = struct.unpack(endian + 'II', f.read(8))

        print(f"PCAP: v{ver_major}.{ver_minor}, snaplen={snaplen}, link={network}")

        packets = []
        pkt_num = 0
        while True:
            hdr = f.read(16)
            if len(hdr) < 16:
                break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
            data = f.read(incl_len)
            if len(data) < incl_len:
                break
            pkt_num += 1

            # Parse Ethernet or raw IP
            if network == 1:  # Ethernet
                if len(data) < 14:
                    continue
                eth_type = struct.unpack('>H', data[12:14])[0]
                if eth_type != 0x0800:  # IPv4
                    continue
                ip_start = 14
            elif network == 101:  # Raw IP
                ip_start = 0
            elif network == 113:  # Linux cooked capture
                if len(data) < 16:
                    continue
                ip_start = 16
            else:
                ip_start = 0

            # Parse IP header
            if ip_start + 20 > len(data):
                continue
            ip_data = data[ip_start:]
            version_ihl = ip_data[0]
            ihl = (version_ihl & 0x0F) * 4
            protocol = ip_data[9]
            src_ip = ip_data[12:16]
            dst_ip = ip_data[16:20]

            if protocol != 6:  # TCP only
                continue

            # Parse TCP header
            tcp_data = ip_data[ihl:]
            if len(tcp_data) < 20:
                continue
            src_port = struct.unpack('>H', tcp_data[0:2])[0]
            dst_port = struct.unpack('>H', tcp_data[2:4])[0]
            tcp_data_offset = ((tcp_data[12] >> 4) & 0xF) * 4

            payload = tcp_data[tcp_data_offset:]
            if len(payload) > 0:
                src_ip_str = f"{src_ip[0]}.{src_ip[1]}.{src_ip[2]}.{src_ip[3]}"
                dst_ip_str = f"{dst_ip[0]}.{dst_ip[1]}.{dst_ip[2]}.{dst_ip[3]}"
                packets.append({
                    'num': pkt_num,
                    'ts': ts_sec + ts_usec / 1000000.0,
                    'src_ip': src_ip_str,
                    'dst_ip': dst_ip_str,
                    'src_port': src_port,
                    'dst_port': dst_port,
                    'data': payload,
                })

        print(f"Total TCP packets with data: {len(packets)}")
        return packets


def extract_game_packets(tcp_packets):
    """
    Reassemble TCP streams and extract game protocol packets.
    Game packet format: [2B LE length][2B LE opcode][payload]
    """
    # Group by stream (src_ip:src_port -> dst_ip:dst_port)
    streams = {}
    for pkt in tcp_packets:
        key = (pkt['src_ip'], pkt['src_port'], pkt['dst_ip'], pkt['dst_port'])
        if key not in streams:
            streams[key] = bytearray()
        streams[key] += pkt['data']

    print(f"\nTCP streams: {len(streams)}")
    for key, data in streams.items():
        print(f"  {key[0]}:{key[1]} -> {key[2]}:{key[3]}: {len(data)} bytes")

    # Find game server streams (not HTTP, not gateway on 5997)
    game_packets = []

    for key, raw in streams.items():
        src_ip, src_port, dst_ip, dst_port = key

        # Skip non-game traffic
        if dst_port in (80, 443, 8080) or src_port in (80, 443, 8080):
            continue

        # Determine direction
        # Client -> Server: dst_port is game port (usually 7001-7999 or 5997)
        # Server -> Client: src_port is game port
        is_gateway = (dst_port == 5997 or src_port == 5997)

        if dst_port >= 7000 or src_port >= 7000 or is_gateway:
            direction = "C2S" if (dst_port >= 7000 or dst_port == 5997) else "S2C"

            # Parse game packets from stream
            pos = 0
            while pos + 4 <= len(raw):
                pkt_len = struct.unpack('<H', raw[pos:pos+2])[0]
                opcode = struct.unpack('<H', raw[pos+2:pos+4])[0]

                if pkt_len < 4 or pkt_len > 65535:
                    pos += 1  # skip garbage
                    continue

                if pos + pkt_len > len(raw):
                    break  # incomplete packet

                payload = raw[pos+4:pos+pkt_len]
                game_packets.append({
                    'direction': direction,
                    'opcode': opcode,
                    'payload': payload,
                    'pkt_len': pkt_len,
                    'gateway': is_gateway,
                    'stream': f"{src_ip}:{src_port}->{dst_ip}:{dst_port}",
                })
                pos += pkt_len

    return game_packets


def analyze_gather(game_packets):
    """Analyze game packets for gather-related activity."""

    print(f"\n{'='*80}")
    print(f"  TOTAL GAME PACKETS: {len(game_packets)}")
    print(f"{'='*80}")

    # Separate gateway and game server packets
    gw_packets = [p for p in game_packets if p['gateway']]
    gs_packets = [p for p in game_packets if not p['gateway']]

    print(f"\nGateway packets: {len(gw_packets)}")
    print(f"Game server packets: {len(gs_packets)}")

    # Show ALL C2S (client to server) packets in order - these are what the game client sends
    c2s = [p for p in gs_packets if p['direction'] == 'C2S']
    s2c = [p for p in gs_packets if p['direction'] == 'S2C']

    print(f"\nC2S (client -> server): {len(c2s)} packets")
    print(f"S2C (server -> client): {len(s2c)} packets")

    # Print ALL C2S packets (the ones we need to replicate)
    print(f"\n{'='*80}")
    print(f"  ALL C2S PACKETS (what game client sends)")
    print(f"{'='*80}")
    for i, p in enumerate(c2s):
        op = p['opcode']
        pl = p['payload']
        pl_hex = pl[:40].hex() if pl else ""
        extra = ""

        # Annotate known opcodes
        if op == 0x001F: extra = " [LOGIN]"
        elif op == 0x0021: extra = " [WORLD_ENTRY]"
        elif op == 0x0023: extra = " [AUTH]"
        elif op == 0x0042: extra = " [HEARTBEAT]"
        elif op == 0x006E: extra = " [TILE_SELECT]"
        elif op == 0x0767: extra = " [SYNC_A]"
        elif op == 0x0769: extra = " [SYNC_B]"
        elif op == 0x099D: extra = " [TROOP_SELECT]"
        elif op == 0x0245: extra = " [MARCH_SCREEN]"
        elif op == 0x0834: extra = " [FORMATION]"
        elif op == 0x0840: extra = " [INIT]"
        elif op == 0x0709: extra = " [EXTRA_A]"
        elif op == 0x0A2C: extra = " [EXTRA_B]"
        elif op == 0x033E: extra = " [SEARCH_REQ]"
        elif op == 0x01D6: extra = " [READY_SIG]"
        elif op == 0x17A3: extra = " [EXTRA_17A3]"
        elif op == 0x1B8B: extra = " [SESSION]"
        elif op == 0x0CE8: extra = " [GATHER/MARCH] <<<<<"
        elif op == 0x0CEB: extra = " [ENABLE_VIEW]"
        elif op == 0x0CED: extra = " [TRAIN]"
        elif op == 0x0CEF: extra = " [BUILD]"
        elif op == 0x0CEE: extra = " [RESEARCH]"
        elif op == 0x000B: extra = " [GW_AUTH]"

        print(f"  [{i:3d}] 0x{op:04X} ({p['pkt_len']:4d}B) {pl_hex}{extra}")

    # Print important S2C responses
    print(f"\n{'='*80}")
    print(f"  KEY S2C RESPONSES")
    print(f"{'='*80}")
    for i, p in enumerate(s2c):
        op = p['opcode']
        pl = p['payload']
        # Only show interesting opcodes
        if op in (0x0020, 0x0024, 0x0038, 0x00B8, 0x00B9, 0x0071, 0x076C,
                  0x007C, 0x0033, 0x0037, 0x033F, 0x1B8A, 0x0082, 0x099E,
                  0x0244, 0x076A, 0x0768):
            pl_hex = pl[:40].hex() if pl else ""
            extra = ""
            if op == 0x0020: extra = " [LOGIN_OK]"
            elif op == 0x0024: extra = " [AUTH_RESP]"
            elif op == 0x0038: extra = " [CASTLE_DATA]"
            elif op == 0x00B8: extra = " [MARCH_ACCEPT] <<<<<"
            elif op == 0x00B9: extra = " [MARCH_ACK]"
            elif op == 0x0071: extra = " [MARCH_STATE] <<<<< TROOPS MARCHING!"
            elif op == 0x076C: extra = " [MARCH_BUNDLE]"
            elif op == 0x007C: extra = " [COLLECT_STATE]"
            elif op == 0x0033: extra = " [ATTR_CHANGE]"
            elif op == 0x0037: extra = " [TIMER]"
            elif op == 0x033F: extra = " [SEARCH_RESULT]"
            elif op == 0x1B8A: extra = " [SESSION_RESP]"
            elif op == 0x0082: extra = " [MARCH_TERR]"
            elif op == 0x099E: extra = " [TROOP_RESP]"

            print(f"  [{i:3d}] 0x{op:04X} ({p['pkt_len']:4d}B) {pl_hex}{extra}")

    # Detailed analysis of specific packets
    print(f"\n{'='*80}")
    print(f"  DETAILED PACKET ANALYSIS")
    print(f"{'='*80}")

    for p in c2s:
        op = p['opcode']
        pl = p['payload']

        if op == 0x0023:  # AUTH
            print(f"\n  0x0023 AUTH ({len(pl)}B):")
            print(f"    Full payload: {pl.hex()}")
            if len(pl) >= 50:
                flag = struct.unpack('<Q', pl[0:8])[0]
                igg_id = struct.unpack('<I', pl[8:12])[0]
                str_len = struct.unpack('<H', pl[16:18])[0] if len(pl) > 17 else 0
                key_str = pl[18:50].decode('ascii', errors='replace') if len(pl) >= 50 else ""
                print(f"    flag={flag}, IGG_ID={igg_id}, str_len={str_len}")
                print(f"    access_key={key_str}")
                if len(pl) >= 54:
                    print(f"    trailer={pl[50:54].hex()}")

        elif op == 0x1B8B:  # SESSION
            print(f"\n  0x1B8B SESSION ({len(pl)}B):")
            print(f"    Full payload: {pl.hex()}")

        elif op == 0x0CE8:  # GATHER
            print(f"\n  0x0CE8 GATHER ({len(pl)}B):")
            print(f"    Full encrypted payload: {pl.hex()}")
            if len(pl) >= 4:
                print(f"    Codec header: checksum={pl[0]:02x} msg_lo={pl[1]:02x} verify={pl[2]:02x} msg_hi={pl[3]:02x}")
                msg_value = pl[1] | (pl[3] << 8)
                print(f"    msg_value=0x{msg_value:04x} ({msg_value})")
                print(f"    Encrypted data ({len(pl)-4}B): {pl[4:].hex()}")

        elif op == 0x0CEB:  # ENABLE_VIEW
            print(f"\n  0x0CEB ENABLE_VIEW ({len(pl)}B):")
            print(f"    Full encrypted payload: {pl.hex()}")
            if len(pl) >= 4:
                msg_value = pl[1] | (pl[3] << 8)
                print(f"    msg_value=0x{msg_value:04x}")

        elif op == 0x006E:  # TILE_SELECT
            print(f"\n  0x006E TILE_SELECT ({len(pl)}B):")
            if len(pl) >= 5:
                tx = struct.unpack('<H', pl[0:2])[0]
                ty = struct.unpack('<H', pl[2:4])[0]
                flag = pl[4]
                print(f"    tile=({tx},{ty}) flag={flag}")

        elif op == 0x099D:  # TROOP_SELECT
            if len(pl) >= 4:
                tid = struct.unpack('<I', pl[0:4])[0]
                print(f"  0x099D TROOP_SELECT: troop_id={tid}")

        elif op == 0x033E:  # SEARCH
            print(f"\n  0x033E SEARCH ({len(pl)}B): {pl.hex()}")

        elif op == 0x0834:  # FORMATION
            print(f"\n  0x0834 FORMATION ({len(pl)}B):")
            if len(pl) >= 2:
                count = struct.unpack('<H', pl[0:2])[0]
                troops = []
                for i in range(count):
                    off = 2 + i * 4
                    if off + 4 <= len(pl):
                        tid = struct.unpack('<I', pl[off:off+4])[0]
                        troops.append(tid)
                print(f"    count={count}, troops={troops}")

    # Show S2C details for critical packets
    for p in s2c:
        op = p['opcode']
        pl = p['payload']

        if op == 0x0024:  # AUTH response
            print(f"\n  0x0024 AUTH_RESP ({len(pl)}B): {pl.hex()}")

        elif op == 0x1B8A:
            print(f"\n  0x1B8A SESSION_RESP ({len(pl)}B): {pl.hex()}")

        elif op == 0x00B8:  # MARCH_ACCEPT
            print(f"\n  0x00B8 MARCH_ACCEPT ({len(pl)}B): {pl.hex()}")

        elif op == 0x0071:  # MARCH_STATE
            print(f"\n  0x0071 MARCH_STATE ({len(pl)}B):")
            print(f"    Full: {pl.hex()}")

        elif op == 0x076C:
            print(f"\n  0x076C MARCH_BUNDLE ({len(pl)}B):")
            print(f"    First 60B: {pl[:60].hex()}")

        elif op == 0x007C:
            print(f"\n  0x007C COLLECT_STATE ({len(pl)}B): {pl.hex()}")

        elif op == 0x033F:
            print(f"\n  0x033F SEARCH_RESULT ({len(pl)}B): {pl.hex()}")

        elif op == 0x0038 and len(pl) > 100:
            # Extract server key
            entry_count = struct.unpack('<H', pl[0:2])[0]
            for idx in range(entry_count):
                off = 2 + idx * 12
                if off + 12 > len(pl):
                    break
                field_id = struct.unpack('<I', pl[off:off+4])[0]
                value = struct.unpack('<I', pl[off+4:off+8])[0]
                if field_id == 0x4F:
                    print(f"\n  0x0038: SERVER_KEY = 0x{value:08x} (field 0x4F)")
                    break


if __name__ == '__main__':
    pcap_file = sys.argv[1] if len(sys.argv) > 1 else r"D:\CascadeProjects\codex_lab\gather_fresh.pcap"
    print(f"Analyzing: {pcap_file}")
    print(f"{'='*80}")

    tcp_packets = read_pcap(pcap_file)
    game_packets = extract_game_packets(tcp_packets)
    analyze_gather(game_packets)

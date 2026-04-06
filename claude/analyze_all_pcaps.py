"""
Comprehensive PCAP analyzer - analyze ALL gather PCAPs from Mar 20+
Extract EVERY C2S packet, decrypt encrypted ones, compare across sessions.
Focus on finding what makes gather work vs fail.
"""
import struct
import sys
import os
import glob

TABLE = [0x58, 0xef, 0xd7, 0x14, 0xa2, 0x3b, 0x9c]
IGG_ID = 577962733

def read_pcap(filepath):
    packets = []
    try:
        with open(filepath, 'rb') as f:
            magic = struct.unpack('<I', f.read(4))[0]
            if magic == 0xa1b2c3d4:
                endian = '<'
            elif magic == 0xd4c3b2a1:
                endian = '>'
            else:
                return []
            f.read(20)  # rest of global header
            while True:
                hdr = f.read(16)
                if len(hdr) < 16: break
                ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
                data = f.read(incl_len)
                if len(data) < incl_len: break
                # Try to find TCP payload
                for ip_start in [0, 14, 16]:  # raw IP, ethernet, linux cooked
                    if ip_start + 40 > len(data): continue
                    ip_data = data[ip_start:]
                    if (ip_data[0] >> 4) != 4: continue  # IPv4
                    ihl = (ip_data[0] & 0x0F) * 4
                    if ip_data[9] != 6: continue  # TCP
                    tcp = ip_data[ihl:]
                    if len(tcp) < 20: continue
                    sp = struct.unpack('>H', tcp[0:2])[0]
                    dp = struct.unpack('>H', tcp[2:4])[0]
                    doff = ((tcp[12] >> 4) & 0xF) * 4
                    payload = tcp[doff:]
                    if len(payload) > 0:
                        src_ip = f"{ip_data[12]}.{ip_data[13]}.{ip_data[14]}.{ip_data[15]}"
                        dst_ip = f"{ip_data[16]}.{ip_data[17]}.{ip_data[18]}.{ip_data[19]}"
                        packets.append({
                            'ts': ts_sec + ts_usec/1e6,
                            'src': src_ip, 'sp': sp,
                            'dst': dst_ip, 'dp': dp,
                            'data': payload
                        })
                    break
    except Exception as e:
        pass
    return packets

def find_game_streams(packets):
    """Find game server streams (port 5991-5997 or 7000+)"""
    from collections import Counter
    port_count = Counter()
    for p in packets:
        for port in [p['sp'], p['dp']]:
            if 5990 <= port <= 5999 or 7000 <= port <= 8000:
                port_count[port] += 1
    if not port_count:
        return None, None, None, None
    game_port = port_count.most_common(1)[0][0]

    # Find the server IP for this port
    for p in packets:
        if p['dp'] == game_port:
            return p['dst'], game_port, p['src'], p['sp']
        if p['sp'] == game_port:
            return p['src'], game_port, p['dst'], p['dp']
    return None, None, None, None

def extract_game_packets(packets, server_ip, server_port):
    """Extract game protocol packets with proper C2S/S2C separation"""
    c2s_buf = bytearray()
    s2c_buf = bytearray()

    for p in packets:
        if p['dst'] == server_ip and p['dp'] == server_port:
            c2s_buf.extend(p['data'])
        elif p['src'] == server_ip and p['sp'] == server_port:
            s2c_buf.extend(p['data'])

    def parse_stream(buf):
        pkts = []
        pos = 0
        while pos + 4 <= len(buf):
            pkt_len = struct.unpack('<H', buf[pos:pos+2])[0]
            opcode = struct.unpack('<H', buf[pos+2:pos+4])[0]
            if pkt_len < 4 or pkt_len > 65535:
                pos += 1; continue
            if pos + pkt_len > len(buf): break
            payload = bytes(buf[pos+4:pos+pkt_len])
            pkts.append((opcode, payload))
            pos += pkt_len
        return pkts

    return parse_stream(c2s_buf), parse_stream(s2c_buf)

def extract_server_key(s2c_packets):
    """Extract server key from 0x0038 packet"""
    for op, pl in s2c_packets:
        if op == 0x0038 and len(pl) > 50:
            entry_count = struct.unpack('<H', pl[0:2])[0]
            for idx in range(entry_count):
                off = 2 + idx * 12
                if off + 12 > len(pl): break
                fid = struct.unpack('<I', pl[off:off+4])[0]
                val = struct.unpack('<I', pl[off+4:off+8])[0]
                if fid == 0x4F:
                    return val
    return None

def codec_decode(payload, sk_bytes):
    """CMsgCodec decode"""
    if len(payload) < 5: return payload
    msg = [payload[1], payload[3]]
    dec = bytearray(len(payload) - 4)
    for p in range(4, len(payload)):
        i = p + 4
        table_b = TABLE[i % 7]
        sk_b = sk_bytes[i % 4]
        msg_b = msg[i % 2]
        intermediate = (payload[p] ^ sk_b ^ table_b) & 0xFF
        dec[p - 4] = (intermediate - msg_b * 17) & 0xFF
    return bytes(dec)

ENCRYPTED_OPS = {0x0CE8, 0x0CEB, 0x0CED, 0x0CEE, 0x0CEF, 0x1B8B}
OPNAMES = {
    0x001F: "LOGIN", 0x0020: "LOGIN_OK", 0x0021: "WORLD_ENTRY",
    0x0023: "AUTH", 0x0024: "AUTH_RESP",
    0x0033: "SYN_ATTR", 0x0038: "CASTLE_DATA",
    0x0042: "HEARTBEAT", 0x0043: "SERVER_TIME",
    0x006E: "TILE_SEL", 0x0071: "MARCH_STATE",
    0x0078: "MARCH_DET", 0x007C: "COLLECT",
    0x0082: "MARCH_TERR", 0x0085: "WORLD_DATA",
    0x0091: "UNK_91",
    0x0245: "MARCH_SCR", 0x0323: "PRE_GATHER",
    0x033E: "SEARCH", 0x033F: "SEARCH_RES",
    0x0674: "TIMING", 0x0675: "TIMING_R",
    0x0709: "EXTRA_A", 0x070A: "EXTRA_A_R",
    0x0767: "SYNC_A", 0x0769: "SYNC_B",
    0x076C: "MARCH_BUNDLE",
    0x0834: "FORMATION", 0x0840: "INIT",
    0x099D: "TROOP_SEL", 0x099E: "TROOP_R",
    0x0A2C: "EXTRA_B",
    0x0CE8: "GATHER", 0x0CEB: "ENABLE_VIEW",
    0x0CED: "TRAIN", 0x0CEE: "RESEARCH", 0x0CEF: "BUILD",
    0x0AF2: "INIT_AF2", 0x1357: "INIT_1357", 0x170D: "INIT_170D",
    0x11FF: "INIT_11FF", 0x17D4: "INIT_17D4",
    0x1B8B: "SESSION", 0x1B8A: "SESSION_R",
    0x00B8: "MARCH_ACC", 0x00B9: "MARCH_ACK",
    0x01D6: "READY_SIG",
}

def analyze_pcap(filepath):
    """Full analysis of one PCAP. Returns dict of findings."""
    packets = read_pcap(filepath)
    if not packets:
        return None

    server_ip, server_port, _, _ = find_game_streams(packets)
    if not server_ip:
        return None

    c2s, s2c = extract_game_packets(packets, server_ip, server_port)
    if not c2s:
        return None

    sk = extract_server_key(s2c)
    sk_bytes = [sk & 0xFF, (sk >> 8) & 0xFF, (sk >> 16) & 0xFF, (sk >> 24) & 0xFF] if sk else None

    result = {
        'file': os.path.basename(filepath),
        'server': f"{server_ip}:{server_port}",
        'c2s_count': len(c2s),
        's2c_count': len(s2c),
        'server_key': sk,
        'c2s_ops': [],
        'has_gather': False,
        'has_0323': False,
        'has_1b8b': False,
        'has_0023': False,
        'has_01d6': False,
        'gather_plain': None,
        'session_raw': None,
        'session_decoded': None,
        'enable_view_decoded': None,
        'pre_gather_raw': None,
        'gather_response': [],  # S2C after gather
        'has_0071': False,
        'has_007c': False,
        'troop_ids': [],
        'formation_ids': [],
        'search_payload': None,
        'tile_selects': [],
    }

    # Analyze C2S
    for op, pl in c2s:
        name = OPNAMES.get(op, f"0x{op:04X}")
        result['c2s_ops'].append((op, name, len(pl)))

        if op == 0x0CE8:
            result['has_gather'] = True
            if sk_bytes and len(pl) >= 5:
                dec = codec_decode(pl, sk_bytes)
                result['gather_plain'] = dec.hex()

        if op == 0x0323:
            result['has_0323'] = True
            result['pre_gather_raw'] = pl.hex()

        if op == 0x1B8B:
            result['has_1b8b'] = True
            result['session_raw'] = pl.hex()
            if sk_bytes and len(pl) >= 5:
                # Check if it's CMsgCodec (verify byte)
                verify_ok = (pl[2] == (pl[1] ^ 0xB7)) if len(pl) > 2 else False
                dec = codec_decode(pl, sk_bytes)
                result['session_decoded'] = dec.hex()
                result['session_verify_std'] = verify_ok

        if op == 0x0CEB and sk_bytes:
            dec = codec_decode(pl, sk_bytes)
            result['enable_view_decoded'] = dec.hex()

        if op == 0x0023:
            result['has_0023'] = True
        if op == 0x01D6:
            result['has_01d6'] = True

        if op == 0x099D and len(pl) >= 4:
            tid = struct.unpack('<I', pl[0:4])[0]
            result['troop_ids'].append(tid)

        if op == 0x0834 and len(pl) >= 2:
            cnt = struct.unpack('<H', pl[0:2])[0]
            for i in range(cnt):
                off = 2 + i * 4
                if off + 4 <= len(pl):
                    result['formation_ids'].append(struct.unpack('<I', pl[off:off+4])[0])

        if op == 0x033E:
            result['search_payload'] = pl.hex()

        if op == 0x006E and len(pl) >= 4:
            tx = struct.unpack('<H', pl[0:2])[0]
            ty = struct.unpack('<H', pl[2:4])[0]
            result['tile_selects'].append((tx, ty))

    # Analyze S2C for gather responses
    gather_sent = False
    for op, pl in c2s:
        if op == 0x0CE8:
            gather_sent = True

    if gather_sent:
        # Find S2C responses after the gather
        # Look for key response opcodes
        for op, pl in s2c:
            if op == 0x00B8:
                result['gather_response'].append(('0x00B8', len(pl), pl.hex()))
            elif op == 0x0071:
                result['has_0071'] = True
                result['gather_response'].append(('0x0071', len(pl), pl[:40].hex()))
            elif op == 0x007C:
                result['has_007c'] = True
                result['gather_response'].append(('0x007C', len(pl), pl.hex()))
            elif op == 0x076C:
                result['gather_response'].append(('0x076C', len(pl), pl[:30].hex()))

    return result


def main():
    # Find all PCAPs from Mar 20+
    pcap_dirs = [
        r"D:\CascadeProjects\codex_lab",
        r"D:\CascadeProjects\lords_bot",
        r"D:\CascadeProjects",
    ]

    all_pcaps = []
    for d in pcap_dirs:
        for f in glob.glob(os.path.join(d, "*.pcap")):
            basename = os.path.basename(f)
            # Include Mar 20+ PCAPs and any gather-specific ones
            if any(x in basename for x in ["20_Mar", "21_Mar", "22_Mar", "23_Mar", "24_Mar",
                                            "25_Mar", "26_Mar", "27_Mar", "28_Mar",
                                            "gather", "manual"]):
                all_pcaps.append(f)

    # Also add specific known files
    for extra in [
        r"D:\CascadeProjects\codex_lab\gather_fresh.pcap",
        r"D:\CascadeProjects\PCAPdroid_25_Mar_07_05_12.pcap",
        r"D:\CascadeProjects\PCAPdroid_25_Mar_07_29_40.pcap",
    ]:
        if os.path.exists(extra) and extra not in all_pcaps:
            all_pcaps.append(extra)

    all_pcaps = sorted(set(all_pcaps))
    print(f"Found {len(all_pcaps)} PCAPs to analyze")
    print("=" * 100)

    gather_sessions = []

    for pcap_path in all_pcaps:
        result = analyze_pcap(pcap_path)
        if result is None:
            continue

        if result['has_gather']:
            gather_sessions.append(result)
            print(f"\n{'='*100}")
            print(f"GATHER SESSION: {result['file']}")
            print(f"  Server: {result['server']}, Key: 0x{result['server_key']:08x}" if result['server_key'] else "  No key")
            print(f"  C2S: {result['c2s_count']} pkts, S2C: {result['s2c_count']} pkts")
            print(f"  has_0323={result['has_0323']} has_1b8b={result['has_1b8b']} has_0023={result['has_0023']} has_01d6={result['has_01d6']}")
            print(f"  Troops: {result['troop_ids']}")
            print(f"  Formation: {result['formation_ids']}")
            print(f"  Tiles: {result['tile_selects']}")
            print(f"  Search: {result['search_payload']}")

            if result['session_raw']:
                print(f"  0x1B8B raw ({len(result['session_raw'])//2}B): {result['session_raw']}")
                print(f"  0x1B8B decoded: {result['session_decoded']}")
                print(f"  0x1B8B verify_std: {result.get('session_verify_std', '?')}")

            if result['pre_gather_raw']:
                print(f"  0x0323 raw: {result['pre_gather_raw']}")

            if result['gather_plain']:
                gp = bytes.fromhex(result['gather_plain'])
                slot = gp[0]
                mt = struct.unpack('<H', gp[4:6])[0] if len(gp) > 5 else 0
                tx = struct.unpack('<H', gp[9:11])[0] if len(gp) > 10 else 0
                ty = struct.unpack('<H', gp[11:13])[0] if len(gp) > 12 else 0
                hero = gp[14] if len(gp) > 14 else 0
                kingdom = gp[18] if len(gp) > 18 else 0
                igg = struct.unpack('<I', gp[33:37])[0] if len(gp) > 36 else 0
                print(f"  GATHER: slot={slot} type=0x{mt:04x} tile=({tx},{ty}) hero={hero} kingdom={kingdom} igg={igg}")
                print(f"  GATHER plain: {result['gather_plain']}")

            # C2S sequence (abbreviated)
            print(f"\n  C2S SEQUENCE:")
            for i, (op, name, sz) in enumerate(result['c2s_ops']):
                if op not in (0x0042, 0x036C, 0x0002):  # skip noise
                    marker = " <<<" if op in (0x0CE8, 0x0323, 0x1B8B) else ""
                    print(f"    [{i:3d}] 0x{op:04X} {name:15s} ({sz:4d}B){marker}")

            # Gather response chain
            print(f"\n  GATHER RESPONSES: 0x0071={'YES' if result['has_0071'] else 'NO'} 0x007C={'YES' if result['has_007c'] else 'NO'}")
            for rname, rsize, rhex in result['gather_response']:
                print(f"    {rname} ({rsize}B): {rhex[:80]}")

    # Summary comparison
    print(f"\n\n{'='*100}")
    print(f"SUMMARY: {len(gather_sessions)} gather sessions found")
    print(f"{'='*100}")
    for s in gather_sessions:
        success = "SUCCESS" if s['has_0071'] else "FAIL"
        print(f"  [{success:7s}] {s['file']:50s} 0323={s['has_0323']} 1B8B={s['has_1b8b']} 0023={s['has_0023']} 01D6={s['has_01d6']} troops={len(s['troop_ids'])}")


if __name__ == '__main__':
    main()

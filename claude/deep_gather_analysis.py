"""
Deep analysis of ALL gather PCAPs - extract and decrypt 0x0CE8 byte-by-byte.
Uses same PCAP parsing as decrypt_gather2.py (proven working).
"""
import struct, sys, os
from pathlib import Path

sys.path.insert(0, r'D:\CascadeProjects\claude')

TABLE = [0x58, 0xef, 0xd7, 0x14, 0xa2, 0x3b, 0x9c]


def read_pcap_streams(filepath):
    """Read PCAP, return C2S and S2C byte streams for game server."""
    with open(filepath, 'rb') as f:
        magic = struct.unpack('<I', f.read(4))[0]
        endian = '<' if magic == 0xa1b2c3d4 else '>'
        f.read(20)

        streams = {}
        while True:
            hdr = f.read(16)
            if len(hdr) < 16:
                break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
            data = f.read(incl_len)
            if len(data) < incl_len:
                break

            ip_data = data
            if len(ip_data) < 20:
                continue
            ihl = (ip_data[0] & 0x0F) * 4
            protocol = ip_data[9]
            if protocol != 6:
                continue

            tcp = ip_data[ihl:]
            if len(tcp) < 20:
                continue
            src_port = struct.unpack('>H', tcp[0:2])[0]
            dst_port = struct.unpack('>H', tcp[2:4])[0]
            tcp_off = ((tcp[12] >> 4) & 0xF) * 4
            payload = tcp[tcp_off:]
            if len(payload) == 0:
                continue

            # Game server ports: 7001-7010
            game_ports = set(range(7001, 7011))
            if dst_port in game_ports:
                streams.setdefault('C2S', bytearray()).extend(payload)
            elif src_port in game_ports:
                streams.setdefault('S2C', bytearray()).extend(payload)

    return streams


def parse_packets(raw):
    packets = []
    pos = 0
    while pos + 4 <= len(raw):
        pkt_len = struct.unpack('<H', raw[pos:pos+2])[0]
        opcode = struct.unpack('<H', raw[pos+2:pos+4])[0]
        if pkt_len < 4 or pkt_len > 65535 or pos + pkt_len > len(raw):
            break
        payload = bytes(raw[pos+4:pos+pkt_len])
        packets.append((opcode, payload))
        pos += pkt_len
    return packets


def decrypt_cmsg(payload, server_key_u32):
    if len(payload) < 5:
        return None
    sk = [server_key_u32 & 0xFF, (server_key_u32 >> 8) & 0xFF,
          (server_key_u32 >> 16) & 0xFF, (server_key_u32 >> 24) & 0xFF]
    msg = [payload[1], payload[3]]
    verify = payload[2]
    dec = bytearray(len(payload) - 4)
    for p in range(4, len(payload)):
        i = p + 4  # absolute position in full packet
        table_b = TABLE[i % 7]
        sk_b = sk[i % 4]
        msg_b = msg[i % 2]
        intermediate = (payload[p] ^ sk_b ^ table_b) & 0xFF
        dec[p - 4] = (intermediate - msg_b * 17) & 0xFF
    return bytes(dec)


def extract_server_key(s2c_pkts):
    for op, pl in s2c_pkts:
        if op == 0x0038 and len(pl) > 100:
            entry_count = struct.unpack('<H', pl[0:2])[0]
            for idx in range(entry_count):
                off = 2 + idx * 12
                if off + 12 > len(pl):
                    break
                field_id = struct.unpack('<I', pl[off:off+4])[0]
                value = struct.unpack('<I', pl[off+4:off+8])[0]
                if field_id == 0x4F:
                    return value
    return None


def analyze_pcap(filepath):
    try:
        streams = read_pcap_streams(filepath)
    except Exception as e:
        return

    if 'C2S' not in streams or 'S2C' not in streams:
        return

    c2s = parse_packets(streams['C2S'])
    s2c = parse_packets(streams['S2C'])

    sk = extract_server_key(s2c)
    if not sk:
        return

    # Find 0x0CE8 in C2S
    gather_indices = [i for i, (op, _) in enumerate(c2s) if op == 0x0CE8]
    if not gather_indices:
        return

    print(f"\n{'='*70}")
    print(f"PCAP: {filepath.name}  |  Server key: 0x{sk:08X}")
    print(f"C2S: {len(c2s)} pkts  |  S2C: {len(s2c)} pkts  |  Gathers: {len(gather_indices)}")
    print(f"{'='*70}")

    for gi in gather_indices:
        op, pl = c2s[gi]
        print(f"\n  --- 0x0CE8 (C2S index {gi}, {len(pl)}B raw) ---")

        plain = decrypt_cmsg(pl, sk)
        if not plain:
            print(f"  Decrypt failed!")
            continue

        print(f"  Plaintext ({len(plain)}B): {plain.hex()}")

        if len(plain) >= 46:
            march_type = struct.unpack('<H', plain[4:6])[0]
            tile_x = struct.unpack('<H', plain[9:11])[0]
            tile_y = struct.unpack('<H', plain[11:13])[0]
            hero = struct.unpack('<I', plain[14:18])[0]
            igg_id = struct.unpack('<I', plain[33:37])[0]

            print(f"  [0]  slot={plain[0]}  [1:4] nonce={plain[1]:02x}{plain[2]:02x}{plain[3]:02x}")
            print(f"  [4:6]  march_type=0x{march_type:04X}  [6:9]={plain[6]:02x}{plain[7]:02x}{plain[8]:02x}")
            print(f"  [9:13] tile=({tile_x},{tile_y})  [13]flag={plain[13]:02x}")
            print(f"  [14:18] hero={hero}  [18]={plain[18]:02x}  [19:22]={plain[19]:02x}{plain[20]:02x}{plain[21]:02x}")
            print(f"  [22]={plain[22]:02x}  [23:33]={plain[23:33].hex()}")
            print(f"  [33:37] igg_id={igg_id}  [37:46]={plain[37:46].hex()}")

        # Show last 20 C2S packets before 0x0CE8
        print(f"\n  C2S BEFORE 0x0CE8:")
        start = max(0, gi - 20)
        for j in range(start, gi):
            op2, pl2 = c2s[j]
            ann = ""
            if op2 == 0x0CEB:
                dec = decrypt_cmsg(pl2, sk)
                ann = f" plain={dec.hex()}" if dec else ""
            elif op2 == 0x006E and len(pl2) >= 4:
                tx, ty = struct.unpack('<HH', pl2[:4])
                ann = f" tile=({tx},{ty})"
            elif op2 == 0x099D and len(pl2) >= 4:
                ann = f" troop={struct.unpack('<I', pl2[:4])[0]}"
            elif op2 == 0x1B8B:
                dec = decrypt_cmsg(pl2, sk)
                ann = f" plain={dec.hex()}" if dec else ""
            elif op2 == 0x0834 and len(pl2) >= 2:
                cnt = struct.unpack('<H', pl2[:2])[0]
                ann = f" count={cnt}"
            elif op2 == 0x0323:
                ann = f" payload={pl2.hex()}"
            print(f"    [{j:4d}] 0x{op2:04X} ({len(pl2)}B){ann}")

        # Find S2C responses after 0x0CE8 by looking at S2C packets
        # Since we don't have timestamps, look at S2C packets that appear
        # "around" the same position ratio
        print(f"\n  S2C after 0x0CE8 (next 20 relevant):")
        # Simple approach: find the first S2C 0x00B8 or 0x0076 after the
        # corresponding position in S2C stream
        ratio = gi / max(len(c2s), 1)
        s2c_start = max(0, int(ratio * len(s2c)) - 20)
        found = 0
        interesting = {0x00B8, 0x0071, 0x076C, 0x007C, 0x0033, 0x00B9,
                       0x0076, 0x0077, 0x0078, 0x007A, 0x0037}
        for j in range(s2c_start, len(s2c)):
            op2, pl2 = s2c[j]
            if op2 in interesting:
                print(f"    [{j:4d}] 0x{op2:04X} ({len(pl2)}B) {pl2.hex()[:60]}")
                found += 1
                if found >= 20:
                    break


def main():
    pcap_dir = Path(r'D:\CascadeProjects')
    pcaps = sorted(pcap_dir.glob('*.pcap'))
    for subdir in ['rebel_attack', 'codex_lab']:
        sub = pcap_dir / subdir
        if sub.exists():
            pcaps.extend(sorted(sub.glob('*.pcap')))

    print(f"Scanning {len(pcaps)} PCAP files for gather data...\n")

    count = 0
    for pcap in pcaps:
        analyze_pcap(pcap)
        count += 1

    print(f"\n\nDone. Scanned {count} PCAPs.")


if __name__ == '__main__':
    main()

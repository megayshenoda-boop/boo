"""
Analyze 0x1B8B packets from ALL PCAPs.
Focus on: verify byte, msg bytes, plaintext, and encoding pattern.
Key question: is verify = msg_lo ^ 0xB7 (standard) or something else?
"""
import struct, sys
from pathlib import Path

sys.path.insert(0, r'D:\CascadeProjects\claude')

TABLE = [0x58, 0xef, 0xd7, 0x14, 0xa2, 0x3b, 0x9c]


def read_pcap_streams(filepath):
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


def decrypt_cmsg(payload, server_key_u32):
    if len(payload) < 5:
        return None
    sk = [server_key_u32 & 0xFF, (server_key_u32 >> 8) & 0xFF,
          (server_key_u32 >> 16) & 0xFF, (server_key_u32 >> 24) & 0xFF]
    checksum_byte = payload[0]
    msg_lo = payload[1]
    verify = payload[2]
    msg_hi = payload[3]
    msg = [msg_lo, msg_hi]
    enc_data = payload[4:]
    plain = bytearray(len(enc_data))
    calc_checksum = 0
    for i in range(len(enc_data)):
        abs_i = i + 8
        table_b = TABLE[abs_i % 7]
        sk_b = sk[abs_i % 4]
        msg_b = msg[abs_i % 2]
        enc_byte = enc_data[i]
        calc_checksum = (calc_checksum + enc_byte) & 0xFFFFFFFF
        intermediate = enc_byte ^ sk_b ^ table_b
        plain_byte = (intermediate - msg_b * 17) & 0xFF
        plain[i] = plain_byte
    return plain, msg_lo, msg_hi, verify, checksum_byte, (calc_checksum & 0xFF)


def main():
    pcap_dir = Path(r'D:\CascadeProjects')
    pcaps = sorted(pcap_dir.glob('*.pcap'))
    for subdir in ['rebel_attack', 'codex_lab']:
        sub = pcap_dir / subdir
        if sub.exists():
            pcaps.extend(sorted(sub.glob('*.pcap')))

    print(f"Scanning {len(pcaps)} PCAPs for 0x1B8B...\n")
    print(f"{'PCAP':<40} {'SK':<12} {'raw_hex':<50} {'msg_lo':>6} {'msg_hi':>6} {'verify':>8} {'std_verify':>10} {'match':>6} {'plain':<40}")
    print("-" * 180)

    results = []

    for pcap in pcaps:
        try:
            streams = read_pcap_streams(pcap)
            if 'C2S' not in streams or 'S2C' not in streams:
                continue
            c2s = parse_packets(streams['C2S'])
            s2c = parse_packets(streams['S2C'])
            sk = extract_server_key(s2c)
            if not sk:
                continue

            for op, pl in c2s:
                if op == 0x1B8B and len(pl) >= 4:
                    result = decrypt_cmsg(pl, sk)
                    if result:
                        plain, msg_lo, msg_hi, verify, checksum_byte, calc_checksum = result
                        std_verify = (msg_lo ^ 0xB7) & 0xFF
                        match = "YES" if verify == std_verify else "NO"
                        results.append({
                            'pcap': pcap.name,
                            'sk': sk,
                            'raw': pl.hex(),
                            'msg_lo': msg_lo,
                            'msg_hi': msg_hi,
                            'verify': verify,
                            'std_verify': std_verify,
                            'match': match,
                            'plain': bytes(plain).hex(),
                            'checksum_byte': checksum_byte,
                            'calc_checksum': calc_checksum,
                        })
                        print(f"{pcap.name:<40} 0x{sk:08X} {pl.hex()[:50]:<50} 0x{msg_lo:02X}   0x{msg_hi:02X}   0x{verify:02X}     0x{std_verify:02X}       {match:<6} {bytes(plain).hex()}")
        except Exception as e:
            continue

    print(f"\n\nTotal 0x1B8B packets found: {len(results)}")

    # Analysis
    matches = sum(1 for r in results if r['match'] == 'YES')
    non_matches = sum(1 for r in results if r['match'] == 'NO')
    print(f"Standard verify (msg_lo^0xB7): {matches} match, {non_matches} don't match")

    if non_matches > 0:
        print(f"\nNon-standard verify bytes:")
        for r in results:
            if r['match'] == 'NO':
                # Try other common patterns
                ml = r['msg_lo']
                mh = r['msg_hi']
                v = r['verify']
                patterns = {
                    'ml^0xB7': (ml ^ 0xB7) & 0xFF,
                    'mh^0xB7': (mh ^ 0xB7) & 0xFF,
                    'ml^mh': (ml ^ mh) & 0xFF,
                    '(ml+mh)&0xFF': (ml + mh) & 0xFF,
                    '(ml*17)&0xFF': (ml * 17) & 0xFF,
                    '0x00': 0x00,
                    'ml': ml,
                    'mh': mh,
                    'checksum': r['calc_checksum'],
                    'checksum_byte': r['checksum_byte'],
                    'ml^sk[0]': (ml ^ (r['sk'] & 0xFF)) & 0xFF,
                    'ml^sk[1]': (ml ^ ((r['sk'] >> 8) & 0xFF)) & 0xFF,
                    '~ml&0xFF': (~ml) & 0xFF,
                    'ml^0xFF': ml ^ 0xFF,
                    '(ml+0xB7)&0xFF': (ml + 0xB7) & 0xFF,
                    'plain[0]^ml': (r['plain'] and (int(r['plain'][:2], 16) ^ ml)) & 0xFF if r['plain'] else -1,
                }
                found = [name for name, val in patterns.items() if val == v]
                print(f"  {r['pcap']}: verify=0x{v:02X} msg_lo=0x{ml:02X} msg_hi=0x{mh:02X} matches={found or 'NONE'}")
                print(f"    raw[0:8]: {r['raw'][:16]}")
                print(f"    All pattern values: ", end="")
                for name, val in patterns.items():
                    print(f"{name}=0x{val:02X} ", end="")
                print()

    # Also check: does verify have any consistent formula across ALL results?
    print(f"\n\nCheck ALL results for pattern:")
    for r in results:
        ml = r['msg_lo']
        mh = r['msg_hi']
        v = r['verify']
        ck = r['checksum_byte']
        calc_ck = r['calc_checksum']
        sk0 = r['sk'] & 0xFF
        plain_bytes = bytes.fromhex(r['plain']) if r['plain'] else b''
        p0 = plain_bytes[0] if plain_bytes else 0

        print(f"  ml=0x{ml:02X} mh=0x{mh:02X} v=0x{v:02X} ck=0x{ck:02X} calc_ck=0x{calc_ck:02X} sk0=0x{sk0:02X} p0=0x{p0:02X} | v^ml=0x{v^ml:02X} v^mh=0x{v^mh:02X} v^ck=0x{v^ck:02X} v==ml^0xB7:{v==(ml^0xB7)&0xFF}")


if __name__ == '__main__':
    main()

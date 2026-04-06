"""Check 0x0834 formation data across ALL PCAPs."""
import sys, struct
from pathlib import Path
sys.path.insert(0, r'D:\CascadeProjects\claude')


def read_pcap_streams(filepath):
    with open(filepath, 'rb') as f:
        magic = struct.unpack('<I', f.read(4))[0]
        endian = '<' if magic == 0xa1b2c3d4 else '>'
        f.read(20)
        c2s = bytearray()
        s2c = bytearray()
        while True:
            hdr = f.read(16)
            if len(hdr) < 16: break
            ts_sec, ts_usec, incl_len, _ = struct.unpack(endian + 'IIII', hdr)
            data = f.read(incl_len)
            if len(data) < incl_len: break
            if len(data) < 20: continue
            ihl = (data[0] & 0x0F) * 4
            if data[9] != 6: continue
            tcp = data[ihl:]
            if len(tcp) < 20: continue
            sp = struct.unpack('>H', tcp[0:2])[0]
            dp = struct.unpack('>H', tcp[2:4])[0]
            toff = ((tcp[12] >> 4) & 0xF) * 4
            pl = tcp[toff:]
            if not pl: continue
            gp = set(range(5990, 5999)) | set(range(7001, 7011))
            if dp in gp: c2s.extend(pl)
            elif sp in gp: s2c.extend(pl)
    return bytes(c2s), bytes(s2c)


def parse_packets(raw):
    packets = []
    pos = 0
    while pos + 4 <= len(raw):
        pkt_len = struct.unpack('<H', raw[pos:pos+2])[0]
        opcode = struct.unpack('<H', raw[pos+2:pos+4])[0]
        if pkt_len < 4 or pkt_len > 65535 or pos + pkt_len > len(raw): break
        packets.append((opcode, bytes(raw[pos+4:pos+pkt_len])))
        pos += pkt_len
    return packets


def main():
    pcap_dir = Path(r'D:\CascadeProjects')
    pcaps = sorted(pcap_dir.glob('*.pcap'))
    for sub in ['rebel_attack', 'codex_lab']:
        p = pcap_dir / sub
        if p.exists(): pcaps.extend(sorted(p.glob('*.pcap')))

    print("0x0834 FORMATION DATA ACROSS ALL PCAPs")
    print("=" * 80)

    formations = {}
    for pcap in pcaps:
        try:
            c2s, s2c = read_pcap_streams(pcap)
            pkts = parse_packets(c2s)
            for op, pl in pkts:
                if op == 0x0834 and pl:
                    key = pl.hex()
                    if key not in formations:
                        formations[key] = []
                    formations[key].append(pcap.name)
                    count = struct.unpack('<H', pl[0:2])[0] if len(pl) >= 2 else 0
                    entries = []
                    for i in range(count):
                        off = 2 + i * 4
                        if off + 4 <= len(pl):
                            entries.append(struct.unpack('<I', pl[off:off+4])[0])
                    print(f"\n{pcap.name}:")
                    print(f"  count={count} entries={[f'0x{e:04X}' for e in entries]}")
                    print(f"  hex: {pl.hex()}")
        except:
            continue

    print(f"\n\nUNIQUE FORMATIONS: {len(formations)}")
    for hex_val, pcap_names in formations.items():
        count = struct.unpack('<H', bytes.fromhex(hex_val[:4]))[0]
        print(f"  count={count} ({len(pcap_names)} PCAPs): {', '.join(pcap_names[:5])}")


if __name__ == '__main__':
    main()

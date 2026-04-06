"""Check 0x0021 world entry packet across ALL PCAPs - is the trailer always the same?"""
import sys, struct
from pathlib import Path
sys.path.insert(0, r'D:\CascadeProjects\claude')


def read_pcap_streams(filepath):
    with open(filepath, 'rb') as f:
        magic = struct.unpack('<I', f.read(4))[0]
        endian = '<' if magic == 0xa1b2c3d4 else '>'
        f.read(20)
        c2s = bytearray()
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
            dp = struct.unpack('>H', tcp[2:4])[0]
            toff = ((tcp[12] >> 4) & 0xF) * 4
            pl = tcp[toff:]
            if not pl: continue
            gp = set(range(5990, 5999)) | set(range(7001, 7011))
            if dp in gp: c2s.extend(pl)
    return bytes(c2s)


def parse_packets(raw):
    packets = []
    pos = 0
    while pos + 4 <= len(raw):
        pkt_len = struct.unpack('<H', raw[pos:pos+2])[0]
        opcode = struct.unpack('<H', raw[pos+2:pos+4])[0]
        if pkt_len < 4 or pkt_len > 65535 or pos + pkt_len > len(raw): break
        packets.append((opcode, bytes(raw[pos:pos+pkt_len])))
        pos += pkt_len
    return packets


def main():
    pcap_dir = Path(r'D:\CascadeProjects')
    pcaps = sorted(pcap_dir.glob('*.pcap'))
    for sub in ['rebel_attack', 'codex_lab']:
        p = pcap_dir / sub
        if p.exists(): pcaps.extend(sorted(p.glob('*.pcap')))

    print("=== 0x001F LOGIN + 0x0021 WORLD ENTRY across PCAPs ===\n")

    trailers_001f = {}
    trailers_0021 = {}

    for pcap in pcaps:
        try:
            c2s = read_pcap_streams(pcap)
            pkts = parse_packets(c2s)
            for op, raw in pkts:
                if op == 0x001F:
                    # Full raw hex for comparison
                    payload = raw[4:]
                    # Check specific fields
                    if len(payload) >= 60:
                        ver = struct.unpack('<I', payload[0:4])[0]
                        pad1 = struct.unpack('<I', payload[4:8])[0]
                        igg = struct.unpack('<I', payload[8:12])[0]
                        pad2 = struct.unpack('<I', payload[12:16])[0]
                        tlen = struct.unpack('<H', payload[16:18])[0]
                        marker = payload[50]
                        gid = struct.unpack('<I', payload[51:55])[0]
                        pad3 = struct.unpack('<I', payload[55:59])[0]
                        tail = payload[59]
                        key = f"ver={ver} pad1={pad1} pad2={pad2} marker=0x{marker:02X} gid=0x{gid:08X} pad3={pad3} tail=0x{tail:02X}"
                        trailers_001f.setdefault(key, []).append(pcap.name)

                if op == 0x0021:
                    payload = raw[4:]
                    if len(payload) >= 17:
                        igg = struct.unpack('<I', payload[0:4])[0]
                        pad = struct.unpack('<I', payload[4:8])[0]
                        marker = payload[8]
                        gid = struct.unpack('<I', payload[9:13])[0]
                        trailer = payload[13:17]
                        key = f"pad={pad} marker=0x{marker:02X} gid=0x{gid:08X} trailer={trailer.hex()}"
                        trailers_0021.setdefault(key, []).append(pcap.name)
        except:
            continue

    print("0x001F LOGIN variants:")
    for key, names in trailers_001f.items():
        print(f"  [{len(names)} PCAPs] {key}")
        if len(names) <= 3:
            for n in names: print(f"    - {n}")

    print(f"\n0x0021 WORLD ENTRY variants:")
    for key, names in trailers_0021.items():
        print(f"  [{len(names)} PCAPs] {key}")
        if len(names) <= 3:
            for n in names: print(f"    - {n}")

    # Our values
    print("\n\nOUR BUILDER VALUES:")
    print(f"  0x001F: ver=1 pad1=0 pad2=0 marker=0x0E gid=0x{0x3F00FF0E:08X} pad3=0 tail=0x00")
    print(f"  0x0021: pad=0 marker=0x0E gid=0x{0x3F00FF0E:08X} trailer=b0025c00")


if __name__ == '__main__':
    main()

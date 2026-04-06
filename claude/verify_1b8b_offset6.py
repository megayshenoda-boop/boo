"""
BREAKTHROUGH: 0x1B8B uses Function 2 encode with header at offset 6!

Packet structure:
[len:2][opcode:2][extra:2][ck:1][ml:1][v:1][mh:1][encrypted:16]

- ck (pkt[6]) = sum(encrypted bytes from index 10) & 0xFF
- ml (pkt[7]) = random msg_lo
- v  (pkt[8]) = ml ^ 0xB7  (STANDARD FORMULA!)
- mh (pkt[9]) = random msg_hi
- encrypted data starts at index 10 (not 8)
- extra (pkt[4:6]) = 2 unencrypted header bytes
"""
import struct, sys
from pathlib import Path

sys.path.insert(0, r'D:\CascadeProjects\claude')
from protocol import CMSG_TABLE as TABLE


def read_pcap_streams(filepath):
    with open(filepath, 'rb') as f:
        magic = struct.unpack('<I', f.read(4))[0]
        endian = '<' if magic == 0xa1b2c3d4 else '>'
        f.read(20)
        streams = {}
        while True:
            hdr = f.read(16)
            if len(hdr) < 16: break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
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
            if dp in gp:
                streams.setdefault('C2S', bytearray()).extend(pl)
            elif sp in gp:
                streams.setdefault('S2C', bytearray()).extend(pl)
    return streams


def parse_packets_raw(raw):
    """Return raw packets including header."""
    packets = []
    pos = 0
    while pos + 4 <= len(raw):
        pkt_len = struct.unpack('<H', raw[pos:pos+2])[0]
        opcode = struct.unpack('<H', raw[pos+2:pos+4])[0]
        if pkt_len < 4 or pkt_len > 65535 or pos + pkt_len > len(raw): break
        packets.append((opcode, bytes(raw[pos:pos+pkt_len])))  # FULL packet including header
        pos += pkt_len
    return packets


def extract_server_key(raw):
    packets = []
    pos = 0
    while pos + 4 <= len(raw):
        pkt_len = struct.unpack('<H', raw[pos:pos+2])[0]
        opcode = struct.unpack('<H', raw[pos+2:pos+4])[0]
        if pkt_len < 4 or pkt_len > 65535 or pos + pkt_len > len(raw): break
        pl = bytes(raw[pos+4:pos+pkt_len])
        if opcode == 0x0038 and len(pl) > 100:
            ec = struct.unpack('<H', pl[0:2])[0]
            for idx in range(ec):
                off = 2 + idx * 12
                if off + 12 > len(pl): break
                fid = struct.unpack('<I', pl[off:off+4])[0]
                val = struct.unpack('<I', pl[off+4:off+8])[0]
                if fid == 0x4F: return val
        pos += pkt_len
    return None


def main():
    pcap_dir = Path(r'D:\CascadeProjects')
    pcaps = sorted(pcap_dir.glob('*.pcap'))
    for sub in ['rebel_attack', 'codex_lab']:
        p = pcap_dir / sub
        if p.exists(): pcaps.extend(sorted(p.glob('*.pcap')))

    total = 0
    ck_match = 0
    v_match = 0
    both_match = 0
    decrypt_match = 0

    print("=" * 80)
    print("VERIFYING: 0x1B8B uses offset-6 header")
    print("pkt: [len:2][op:2][extra:2][ck:1][ml:1][v:1][mh:1][enc:16]")
    print("=" * 80)

    for pcap in pcaps:
        try:
            s = read_pcap_streams(pcap)
            if 'C2S' not in s or 'S2C' not in s: continue

            sk_u32 = extract_server_key(s['S2C'])
            if not sk_u32: continue
            sk = [sk_u32 & 0xFF, (sk_u32>>8) & 0xFF, (sk_u32>>16) & 0xFF, (sk_u32>>24) & 0xFF]

            c2s_raw = parse_packets_raw(s['C2S'])

            for op, raw_pkt in c2s_raw:
                if op != 0x1B8B or len(raw_pkt) != 26:
                    continue

                total += 1

                # NEW PARSING: header at offset 6
                extra1 = raw_pkt[4]
                extra2 = raw_pkt[5]
                ck = raw_pkt[6]     # checksum
                ml = raw_pkt[7]     # msg_lo
                v = raw_pkt[8]      # verify
                mh = raw_pkt[9]     # msg_hi
                enc = raw_pkt[10:26]  # 16 bytes encrypted

                # Check verify = ml ^ 0xB7
                expected_v = ml ^ 0xB7
                v_ok = (v == expected_v)
                if v_ok: v_match += 1

                # Check checksum = sum(encrypted bytes) & 0xFF
                expected_ck = sum(enc) & 0xFF
                ck_ok = (ck == expected_ck)
                if ck_ok: ck_match += 1

                if v_ok and ck_ok: both_match += 1

                # Decrypt with new offsets (abs_i starts at 10)
                msg = [ml, mh]
                plain = bytearray(16)
                for i in range(16):
                    abs_i = i + 10
                    tb = TABLE[abs_i % 7]
                    sb = sk[abs_i % 4]
                    mb = msg[abs_i % 2]
                    plain[i] = ((enc[i] ^ sb ^ tb) - mb * 17) & 0xFF

                # Check seed pattern
                if len(plain) >= 16:
                    seed = plain[0:4]
                    x_lo = (seed[2] + 0x13) & 0xFF
                    x_hi = (seed[3] - 0x02) & 0xFF
                    # Check bytes 6,7 match x
                    if len(plain) > 7 and plain[6] == x_lo and plain[7] == x_hi:
                        decrypt_match += 1

                if total <= 15:
                    mark_v = "✓" if v_ok else "✗"
                    mark_ck = "✓" if ck_ok else "✗"
                    print(f"\n{pcap.name}:")
                    print(f"  extra=[{extra1:02X},{extra2:02X}] ck=0x{ck:02X} ml=0x{ml:02X} v=0x{v:02X} mh=0x{mh:02X}")
                    print(f"  verify: v=0x{v:02X} ml^0xB7=0x{expected_v:02X} {mark_v}")
                    print(f"  chksum: ck=0x{ck:02X} sum(enc)=0x{expected_ck:02X} {mark_ck}")
                    print(f"  plain: {plain.hex()}")

        except Exception as e:
            continue

    print("\n" + "=" * 80)
    print(f"RESULTS: {total} packets analyzed")
    print(f"  Verify  (v == ml^0xB7):     {v_match}/{total} {'✓✓✓ CONFIRMED!' if v_match == total else '✗'}")
    print(f"  Checksum (ck == sum(enc)):   {ck_match}/{total} {'✓✓✓ CONFIRMED!' if ck_match == total else '✗'}")
    print(f"  Both match:                  {both_match}/{total}")
    print(f"  Decrypt pattern match:       {decrypt_match}/{total}")
    print("=" * 80)


if __name__ == '__main__':
    main()

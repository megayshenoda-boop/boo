"""
Extended 0x1B8B analysis: What if bytes [4] and [6] are ALSO encrypted?
If the entire payload (22 bytes) is encrypted starting at abs_i=4,
then bytes[4] and [6] have "plaintext" values we can compute.
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


def extract_server_key(s2c_pkts):
    for op, pl in s2c_pkts:
        if op == 0x0038 and len(pl) > 100:
            ec = struct.unpack('<H', pl[0:2])[0]
            for idx in range(ec):
                off = 2 + idx * 12
                if off + 12 > len(pl): break
                fid = struct.unpack('<I', pl[off:off+4])[0]
                val = struct.unpack('<I', pl[off+4:off+8])[0]
                if fid == 0x4F: return val
    return None


def decrypt_byte(enc_byte, abs_i, sk, msg):
    """Decrypt a single byte at given absolute position."""
    tb = TABLE[abs_i % 7]
    sb = sk[abs_i % 4]
    mb = msg[abs_i % 2]
    return ((enc_byte ^ sb ^ tb) - mb * 17) & 0xFF


def encrypt_byte(plain_byte, abs_i, sk, msg):
    """Encrypt a single byte at given absolute position."""
    tb = TABLE[abs_i % 7]
    sb = sk[abs_i % 4]
    mb = msg[abs_i % 2]
    return (((plain_byte + mb * 17) & 0xFF) ^ sb ^ tb) & 0xFF


def main():
    pcap_dir = Path(r'D:\CascadeProjects')
    pcaps = sorted(pcap_dir.glob('*.pcap'))
    for sub in ['rebel_attack', 'codex_lab']:
        p = pcap_dir / sub
        if p.exists(): pcaps.extend(sorted(p.glob('*.pcap')))

    data = []
    for pcap in pcaps:
        try:
            s = read_pcap_streams(pcap)
            if 'C2S' not in s or 'S2C' not in s: continue
            c2s = parse_packets(s['C2S']); s2c = parse_packets(s['S2C'])
            sk_u32 = extract_server_key(s2c)
            if not sk_u32: continue
            sk = [sk_u32 & 0xFF, (sk_u32>>8) & 0xFF, (sk_u32>>16) & 0xFF, (sk_u32>>24) & 0xFF]
            for op, pl in c2s:
                if op == 0x1B8B and len(pl) == 22:
                    ml = pl[1]; mh = pl[3]
                    msg = [ml, mh]
                    # Decrypt ALL 22 bytes as if encrypted from abs_i=4
                    full_plain = bytearray(22)
                    for i in range(22):
                        full_plain[i] = decrypt_byte(pl[i], i + 4, sk, msg)
                    # Also decrypt standard way (bytes 8+)
                    std_plain = bytearray(18)
                    for i in range(18):
                        std_plain[i] = decrypt_byte(pl[4+i], i + 8, sk, msg)
                    data.append({
                        'pcap': pcap.name, 'pl': pl, 'sk': sk, 'ml': ml, 'mh': mh,
                        'full_plain': bytes(full_plain), 'std_plain': bytes(std_plain),
                        'ck': pl[0], 'v': pl[2],
                    })
        except: continue

    print(f"Loaded {len(data)} packets\n")

    # ══════════════════════════════════════════════════════════════
    # ANALYSIS: What are the "plaintext" values at positions 4-7?
    # ══════════════════════════════════════════════════════════════
    print("=" * 80)
    print("HYPOTHESIS: All 22 bytes encrypted from abs_i=4")
    print("Decrypted bytes [0:4] (normally header) vs [4:22] (normally data)")
    print("=" * 80)

    print(f"\n{'PCAP':<35} {'hdr_plain[0:4]':>16} {'data_plain[0:4]':>16} {'ml':>4} {'mh':>4}")
    print("-" * 80)
    for d in data[:20]:
        fp = d['full_plain']
        sp = d['std_plain']
        print(f"{d['pcap']:<35} [{fp[0]:02X},{fp[1]:02X},{fp[2]:02X},{fp[3]:02X}] "
              f"[{sp[0]:02X},{sp[1]:02X},{sp[2]:02X},{sp[3]:02X}] "
              f"0x{d['ml']:02X} 0x{d['mh']:02X}")

    # Check: is full_plain[1] always == msg_lo and full_plain[3] always == msg_hi?
    # (would mean bytes 5,7 are NOT encrypted - just happen to equal msg values)
    ml_match = sum(1 for d in data if d['full_plain'][1] == d['ml'])
    mh_match = sum(1 for d in data if d['full_plain'][3] == d['mh'])
    print(f"\nfull_plain[1]==msg_lo: {ml_match}/{len(data)}")
    print(f"full_plain[3]==msg_hi: {mh_match}/{len(data)}")

    # Check: are full_plain[0] and full_plain[2] constant?
    vals_0 = set(d['full_plain'][0] for d in data)
    vals_2 = set(d['full_plain'][2] for d in data)
    print(f"\nfull_plain[0] unique values: {len(vals_0)} - {sorted(vals_0)[:10]}...")
    print(f"full_plain[2] unique values: {len(vals_2)} - {sorted(vals_2)[:10]}...")

    if len(vals_0) == 1:
        print(f"  *** full_plain[0] is CONSTANT: 0x{list(vals_0)[0]:02X}")
    if len(vals_2) == 1:
        print(f"  *** full_plain[2] is CONSTANT: 0x{list(vals_2)[0]:02X}")

    # ══════════════════════════════════════════════════════════════
    # Check relationship between full_plain[0], full_plain[2] and seed
    # ══════════════════════════════════════════════════════════════
    print("\n" + "=" * 80)
    print("Relationship between decrypted header and seed data")
    print("=" * 80)

    for d in data[:15]:
        fp = d['full_plain']
        sp = d['std_plain']
        seed = sp[0:4]
        print(f"\n{d['pcap']}:")
        print(f"  header_plain = [{fp[0]:02X},{fp[1]:02X},{fp[2]:02X},{fp[3]:02X}]")
        print(f"  seed         = [{seed[0]:02X},{seed[1]:02X},{seed[2]:02X},{seed[3]:02X}]")
        print(f"  hp[0]^seed[0]=0x{fp[0]^seed[0]:02X} hp[0]+seed[0]=0x{(fp[0]+seed[0])&0xFF:02X} "
              f"hp[0]-seed[0]=0x{(fp[0]-seed[0])&0xFF:02X}")
        print(f"  hp[2]^seed[0]=0x{fp[2]^seed[0]:02X} hp[2]^seed[2]=0x{fp[2]^seed[2]:02X} "
              f"hp[2]+seed[2]=0x{(fp[2]+seed[2])&0xFF:02X}")

    # ══════════════════════════════════════════════════════════════
    # Try: what if the "checksum" is sum of ALL encrypted bytes [4:26] (not just [8:26])?
    # ══════════════════════════════════════════════════════════════
    print("\n\n" + "=" * 80)
    print("Alternative checksum: sum of ALL payload bytes?")
    print("=" * 80)

    for d in data[:10]:
        pl = d['pl']
        # Sum of bytes [4:] (enc data only, 18 bytes)
        sum_enc = sum(pl[4:]) & 0xFF
        # Sum of bytes [1:] (everything except checksum)
        sum_no_ck = sum(pl[1:]) & 0xFF
        # Sum of bytes [0:] (everything)
        sum_all = sum(pl) & 0xFF
        # XOR of all bytes
        xor_all = 0
        for b in pl: xor_all ^= b

        print(f"  ck=0x{d['ck']:02X} sum_enc=0x{sum_enc:02X} sum_no_ck=0x{sum_no_ck:02X} "
              f"sum_all=0x{sum_all:02X} xor_all=0x{xor_all:02X}")

    # ══════════════════════════════════════════════════════════════
    # What if ck and v form a 16-bit value together?
    # ══════════════════════════════════════════════════════════════
    print("\n" + "=" * 80)
    print("Check: ck and v as combined value")
    print("=" * 80)

    for d in data[:10]:
        ck = d['ck']; v = d['v']; ml = d['ml']; mh = d['mh']
        fp = d['full_plain']
        sp = d['std_plain']
        ck_v = (ck << 8) | v
        v_ck = (v << 8) | ck
        seed32 = struct.unpack('<I', sp[0:4])[0]

        print(f"  ck_v=0x{ck_v:04X} v_ck=0x{v_ck:04X} seed32=0x{seed32:08X} "
              f"(seed>>16)=0x{(seed32>>16)&0xFFFF:04X}")


if __name__ == '__main__':
    main()

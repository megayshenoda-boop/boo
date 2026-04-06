"""
Quick test: do 0x1B8B checksum/verify formulas involve the opcode bytes?
Opcode 0x1B8B = lo=0x8B, hi=0x1B
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


def main():
    pcap_dir = Path(r'D:\CascadeProjects')
    pcaps = sorted(pcap_dir.glob('*.pcap'))
    for sub in ['rebel_attack', 'codex_lab']:
        p = pcap_dir / sub
        if p.exists(): pcaps.extend(sorted(p.glob('*.pcap')))

    OP_LO = 0x8B
    OP_HI = 0x1B

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
                    ck = pl[0]; ml = pl[1]; v = pl[2]; mh = pl[3]
                    # Standard checksum = sum of encrypted bytes [4:]
                    std_ck = sum(pl[4:]) & 0xFF
                    # Standard verify
                    std_v = ml ^ 0xB7

                    # Decrypt encrypted data
                    enc = pl[4:]
                    plain = bytearray(18)
                    for i in range(18):
                        tb = TABLE[(i+8) % 7]
                        sb = sk[(i+8) % 4]
                        mb = [ml, mh][(i+8) % 2]
                        plain[i] = ((enc[i] ^ sb ^ tb) - mb * 17) & 0xFF

                    data.append({
                        'ck': ck, 'ml': ml, 'v': v, 'mh': mh,
                        'std_ck': std_ck, 'std_v': std_v,
                        'sk': sk, 'sk_u32': sk_u32,
                        'enc': enc, 'plain': plain,
                    })
        except: continue

    print(f"Loaded {len(data)} 0x1B8B packets\n")

    # Test VERIFY formulas involving opcode
    print("=" * 80)
    print("VERIFY BYTE FORMULAS (testing against opcode 0x1B8B)")
    print("=" * 80)

    formulas_v = {
        'ml^0x8B': lambda d: d['ml'] ^ OP_LO,
        'ml^0x1B': lambda d: d['ml'] ^ OP_HI,
        'ml^0x8B^0xB7': lambda d: d['ml'] ^ OP_LO ^ 0xB7,
        'ml^0x1B^0xB7': lambda d: d['ml'] ^ OP_HI ^ 0xB7,
        'ml+0x8B': lambda d: (d['ml'] + OP_LO) & 0xFF,
        'ml-0x8B': lambda d: (d['ml'] - OP_LO) & 0xFF,
        'ml+0x1B': lambda d: (d['ml'] + OP_HI) & 0xFF,
        'ml-0x1B': lambda d: (d['ml'] - OP_HI) & 0xFF,
        'mh^0xB7': lambda d: d['mh'] ^ 0xB7,
        'mh^0x8B': lambda d: d['mh'] ^ OP_LO,
        'mh^0x1B': lambda d: d['mh'] ^ OP_HI,
        '(ml+mh)^0xB7': lambda d: ((d['ml'] + d['mh']) & 0xFF) ^ 0xB7,
        '(ml^mh)^0xB7': lambda d: (d['ml'] ^ d['mh']) ^ 0xB7,
        'ml^mh': lambda d: d['ml'] ^ d['mh'],
        'ml*17&0xFF': lambda d: (d['ml'] * 17) & 0xFF,
        'mh*17&0xFF': lambda d: (d['mh'] * 17) & 0xFF,
        '(ml*17)^0xB7': lambda d: ((d['ml'] * 17) & 0xFF) ^ 0xB7,
        'ml^sk[0]': lambda d: d['ml'] ^ d['sk'][0],
        'ml^sk[1]': lambda d: d['ml'] ^ d['sk'][1],
        'ml^sk[2]': lambda d: d['ml'] ^ d['sk'][2],
        'ml^sk[3]': lambda d: d['ml'] ^ d['sk'][3],
        'ml^(sk[0]^sk[2])': lambda d: d['ml'] ^ (d['sk'][0] ^ d['sk'][2]),
        'ml^(sk[1]^sk[3])': lambda d: d['ml'] ^ (d['sk'][1] ^ d['sk'][3]),
        '(ml^0xB7)^sk[0]': lambda d: (d['ml'] ^ 0xB7) ^ d['sk'][0],
        '(ml+sk[0])&0xFF': lambda d: (d['ml'] + d['sk'][0]) & 0xFF,
        '(ml-sk[0])&0xFF': lambda d: (d['ml'] - d['sk'][0]) & 0xFF,
        # Try with seed bytes
        'ml^plain[0]': lambda d: d['ml'] ^ d['plain'][0],
        'ml^plain[1]': lambda d: d['ml'] ^ d['plain'][1],
        'ml^plain[2]': lambda d: d['ml'] ^ d['plain'][2],
        'ml^plain[3]': lambda d: d['ml'] ^ d['plain'][3],
        '(ml^0xB7)+plain[0]': lambda d: ((d['ml'] ^ 0xB7) + d['plain'][0]) & 0xFF,
        'sum(plain)&0xFF': lambda d: sum(d['plain']) & 0xFF,
        'sum(plain[:4])&0xFF': lambda d: sum(d['plain'][:4]) & 0xFF,
        # XOR of all plain
        'xor_plain': lambda d: eval("__import__('functools').reduce(lambda a,b: a^b, d['plain'])"),
    }

    for name, fn in formulas_v.items():
        matches = sum(1 for d in data if fn(d) == d['v'])
        if matches > 0:
            print(f"  {name}: {matches}/{len(data)} match")

    # Test CHECKSUM formulas involving opcode
    print("\n" + "=" * 80)
    print("CHECKSUM BYTE FORMULAS")
    print("=" * 80)

    formulas_ck = {
        'std (sum enc)': lambda d: sum(d['enc']) & 0xFF,
        'sum(enc)+ml': lambda d: (sum(d['enc']) + d['ml']) & 0xFF,
        'sum(enc)+mh': lambda d: (sum(d['enc']) + d['mh']) & 0xFF,
        'sum(enc)+ml+mh': lambda d: (sum(d['enc']) + d['ml'] + d['mh']) & 0xFF,
        'sum(enc)+v': lambda d: (sum(d['enc']) + d['v']) & 0xFF,
        'sum(enc)^0x8B': lambda d: (sum(d['enc']) & 0xFF) ^ OP_LO,
        'sum(enc)^0x1B': lambda d: (sum(d['enc']) & 0xFF) ^ OP_HI,
        'sum(enc)+0x8B': lambda d: (sum(d['enc']) + OP_LO) & 0xFF,
        'sum(enc)+0x1B': lambda d: (sum(d['enc']) + OP_HI) & 0xFF,
        'sum(all pl[1:])': lambda d: None,  # Need full payload
        'sum(plain)': lambda d: sum(d['plain']) & 0xFF,
        'sum(plain)^sk[0]': lambda d: (sum(d['plain']) & 0xFF) ^ d['sk'][0],
        'xor(enc)': lambda d: eval("__import__('functools').reduce(lambda a,b: a^b, d['enc'])"),
        'sum(enc)+sum(plain)': lambda d: (sum(d['enc']) + sum(d['plain'])) & 0xFF,
    }

    for name, fn in formulas_ck.items():
        try:
            matches = sum(1 for d in data if fn(d) == d['ck'])
            if matches > 0:
                print(f"  {name}: {matches}/{len(data)} match")
        except: pass

    # Brute-force: try ALL constant XOR masks on verify
    print("\n" + "=" * 80)
    print("BRUTE FORCE: v = ml ^ CONST (checking all 256 values)")
    print("=" * 80)

    for const in range(256):
        matches = sum(1 for d in data if (d['ml'] ^ const) == d['v'])
        if matches > 5:
            print(f"  ml^0x{const:02X}: {matches}/{len(data)}")

    for const in range(256):
        matches = sum(1 for d in data if (d['mh'] ^ const) == d['v'])
        if matches > 5:
            print(f"  mh^0x{const:02X}: {matches}/{len(data)}")

    # Brute-force: try v = (ml OP X) where X is some combination
    print("\n" + "=" * 80)
    print("BRUTE FORCE: v = f(ml, mh) for 2-var formulas")
    print("=" * 80)

    # v = ml ROT N
    for n in range(1, 8):
        matches = sum(1 for d in data if ((d['ml'] << n | d['ml'] >> (8-n)) & 0xFF) == d['v'])
        if matches > 3:
            print(f"  ml ROL {n}: {matches}/{len(data)}")
        matches = sum(1 for d in data if ((d['ml'] >> n | d['ml'] << (8-n)) & 0xFF) == d['v'])
        if matches > 3:
            print(f"  ml ROR {n}: {matches}/{len(data)}")

    # v = ml ^ mh ^ CONST
    for const in range(256):
        matches = sum(1 for d in data if ((d['ml'] ^ d['mh'] ^ const) & 0xFF) == d['v'])
        if matches > 5:
            print(f"  ml^mh^0x{const:02X}: {matches}/{len(data)}")

    # v = (ml + mh + CONST) & 0xFF
    for const in range(256):
        matches = sum(1 for d in data if ((d['ml'] + d['mh'] + const) & 0xFF) == d['v'])
        if matches > 5:
            print(f"  (ml+mh+0x{const:02X})&0xFF: {matches}/{len(data)}")

    # v = (ml * CONST) & 0xFF
    for const in range(256):
        matches = sum(1 for d in data if ((d['ml'] * const) & 0xFF) == d['v'])
        if matches > 5:
            print(f"  (ml*0x{const:02X})&0xFF: {matches}/{len(data)}")

    # NEW: What if v is derived from encrypted bytes?
    print("\n" + "=" * 80)
    print("CHECK: v relationship with encrypted bytes")
    print("=" * 80)

    for idx in range(18):
        matches = sum(1 for d in data if d['enc'][idx] == d['v'])
        if matches > 3:
            print(f"  v == enc[{idx}]: {matches}/{len(data)}")
        matches = sum(1 for d in data if (d['enc'][idx] ^ d['ml']) == d['v'])
        if matches > 3:
            print(f"  v == enc[{idx}]^ml: {matches}/{len(data)}")

    # What if v is from plaintext?
    for idx in range(18):
        matches = sum(1 for d in data if d['plain'][idx] == d['v'])
        if matches > 3:
            print(f"  v == plain[{idx}]: {matches}/{len(data)}")

    # Print raw data for manual inspection
    print("\n" + "=" * 80)
    print("RAW DATA (first 15)")
    print("=" * 80)
    print(f"{'ck':>4} {'ml':>4} {'v':>4} {'mh':>4} | {'std_ck':>6} {'std_v':>6} | {'v^ml':>5} {'v^mh':>5} {'ck^std':>6}")
    for d in data[:15]:
        print(f"0x{d['ck']:02X} 0x{d['ml']:02X} 0x{d['v']:02X} 0x{d['mh']:02X} | "
              f"0x{d['std_ck']:02X}  0x{d['std_v']:02X}  | "
              f"0x{d['v']^d['ml']:02X}  0x{d['v']^d['mh']:02X}  0x{d['ck']^d['std_ck']:02X}")


if __name__ == '__main__':
    main()

"""
Deep analysis of 0x1B8B checksum and verify byte formulas.
We know: encryption is standard CMsgCodec. But bytes [4] (checksum) and [6] (verify) differ.
Goal: find formulas for both.
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
        payload = bytes(raw[pos+4:pos+pkt_len])
        packets.append((opcode, payload))
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


def decrypt_payload(payload, sk_u32):
    if len(payload) < 5: return None
    sk = [sk_u32 & 0xFF, (sk_u32 >> 8) & 0xFF, (sk_u32 >> 16) & 0xFF, (sk_u32 >> 24) & 0xFF]
    ck = payload[0]; ml = payload[1]; v = payload[2]; mh = payload[3]
    msg = [ml, mh]; enc = payload[4:]
    plain = bytearray(len(enc)); calc_ck = 0
    for i in range(len(enc)):
        ai = i + 8
        tb = TABLE[ai % 7]; sb = sk[ai % 4]; mb = msg[ai % 2]
        calc_ck = (calc_ck + enc[i]) & 0xFFFFFFFF
        plain[i] = ((enc[i] ^ sb ^ tb) - mb * 17) & 0xFF
    return bytes(plain), ml, mh, v, ck, (calc_ck & 0xFF), sk, enc


def encrypt_plaintext(plain, sk, ml, mh):
    msg = [ml, mh]; enc = bytearray(len(plain)); ck = 0
    for i in range(len(plain)):
        ai = i + 8
        tb = TABLE[ai % 7]; sb = sk[ai % 4]; mb = msg[ai % 2]
        eb = ((plain[i] + mb * 17) & 0xFF) ^ sb ^ tb
        enc[i] = eb & 0xFF
        ck = (ck + enc[i]) & 0xFFFFFFFF
    return bytes(enc), ck & 0xFF


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
            for op, pl in c2s:
                if op == 0x1B8B and len(pl) == 22:
                    r = decrypt_payload(pl, sk_u32)
                    if r:
                        plain, ml, mh, v, ck, calc_ck, sk, enc = r
                        data.append({
                            'pcap': pcap.name, 'plain': plain, 'ml': ml, 'mh': mh,
                            'v': v, 'ck': ck, 'calc_ck': calc_ck, 'sk': sk,
                            'enc': enc, 'raw': pl, 'sk_u32': sk_u32
                        })
        except: continue

    print(f"Loaded {len(data)} 0x1B8B packets\n")

    # ══════════════════════════════════════════════════════════════
    # PART 1: Crack CHECKSUM (byte[4])
    # ══════════════════════════════════════════════════════════════
    print("=" * 80)
    print("PART 1: CHECKSUM BYTE (byte[4]) FORMULA")
    print("=" * 80)

    ck_formulas = {}
    for d in data:
        p = d['plain']; ml = d['ml']; mh = d['mh']; sk = d['sk']
        enc = d['enc']; ck = d['ck']; calc_ck = d['calc_ck']

        tests = {
            'std(sum_enc&FF)':      calc_ck,
            'sum_plain&FF':         sum(p) & 0xFF,
            'xor_plain':            0,  # computed below
            'xor_enc':              0,
            'sum_all22&FF':         sum(d['raw']) & 0xFF,
            'sum_enc+ml+mh&FF':    (calc_ck + ml + mh) & 0xFF,
            'sum_enc+v&FF':        (calc_ck + d['v']) & 0xFF,
            'sum_enc+ml+v+mh&FF':  (calc_ck + ml + d['v'] + mh) & 0xFF,
            'sum_plain+ml+mh&FF':  (sum(p) + ml + mh) & 0xFF,
            'p[0]':                p[0],
            'p[0]^p[1]':           (p[0] ^ p[1]) & 0xFF,
            'p[0]+p[1]&FF':        (p[0] + p[1]) & 0xFF,
            'p[0]^ml':             (p[0] ^ ml) & 0xFF,
            'p[0]+ml&FF':          (p[0] + ml) & 0xFF,
            'seed_u32&FF':         struct.unpack('<I', p[0:4])[0] & 0xFF,
            '(seed>>8)&FF':        (struct.unpack('<I', p[0:4])[0] >> 8) & 0xFF,
            '(seed>>16)&FF':       (struct.unpack('<I', p[0:4])[0] >> 16) & 0xFF,
            '(seed>>24)&FF':       (struct.unpack('<I', p[0:4])[0] >> 24) & 0xFF,
            'sum_seed&FF':         (p[0]+p[1]+p[2]+p[3]) & 0xFF,
            'xor_seed':            (p[0]^p[1]^p[2]^p[3]) & 0xFF,
            'ml^calc_ck':          (ml ^ calc_ck) & 0xFF,
            'mh^calc_ck':          (mh ^ calc_ck) & 0xFF,
            '(ml*17+calc_ck)&FF':  (ml*17 + calc_ck) & 0xFF,
            'sum_hdr4_7&FF':       (ck + ml + d['v'] + mh) & 0xFF,
        }
        # XOR of all plain bytes
        xp = 0
        for b in p: xp ^= b
        tests['xor_plain'] = xp
        # XOR of all enc bytes
        xe = 0
        for b in enc: xe ^= b
        tests['xor_enc'] = xe

        # Sum of enc + header fields
        tests['sum_enc+ck&FF'] = (calc_ck + ck) & 0xFF

        d['ck_tests'] = tests

    print(f"\n{'Formula':<30} {'Matches':>8}")
    print("-" * 40)
    if data:
        for fname in data[0]['ck_tests']:
            matches = sum(1 for d in data if d['ck_tests'][fname] == d['ck'])
            if matches > 0:
                marker = " <<<< FOUND!" if matches == len(data) else ""
                print(f"  {fname:<28} {matches:3d}/{len(data)}{marker}")

    # ══════════════════════════════════════════════════════════════
    # PART 2: Crack VERIFY (byte[6])
    # ══════════════════════════════════════════════════════════════
    print("\n" + "=" * 80)
    print("PART 2: VERIFY BYTE (byte[6]) FORMULA")
    print("=" * 80)

    v_formulas = {}
    for d in data:
        p = d['plain']; ml = d['ml']; mh = d['mh']; sk = d['sk']
        enc = d['enc']; ck = d['ck']; calc_ck = d['calc_ck']
        seed_u32 = struct.unpack('<I', p[0:4])[0]

        tests = {
            'ml^0xB7':             (ml ^ 0xB7) & 0xFF,
            'p[0]':                p[0],
            'p[1]':                p[1],
            'p[2]':                p[2],
            'p[3]':                p[3],
            'p[0]^ml':             (p[0] ^ ml) & 0xFF,
            'p[0]^mh':             (p[0] ^ mh) & 0xFF,
            'p[1]^ml':             (p[1] ^ ml) & 0xFF,
            'p[0]+ml&FF':          (p[0] + ml) & 0xFF,
            'p[0]-ml&FF':          (p[0] - ml) & 0xFF,
            'ml-p[0]&FF':          (ml - p[0]) & 0xFF,
            'p[0]^p[1]':           (p[0] ^ p[1]) & 0xFF,
            'p[0]+p[1]&FF':        (p[0] + p[1]) & 0xFF,
            'p[0]^p[2]':           (p[0] ^ p[2]) & 0xFF,
            'p[0]^p[3]':           (p[0] ^ p[3]) & 0xFF,
            'xor_seed':            (p[0]^p[1]^p[2]^p[3]) & 0xFF,
            'sum_seed&FF':         (p[0]+p[1]+p[2]+p[3]) & 0xFF,
            'seed_u32&FF':         seed_u32 & 0xFF,
            'ml^ck':               (ml ^ ck) & 0xFF,
            'ck^0xB7':             (ck ^ 0xB7) & 0xFF,
            'ck+ml&FF':            (ck + ml) & 0xFF,
            'ck-ml&FF':            (ck - ml) & 0xFF,
            'ml+mh&FF':            (ml + mh) & 0xFF,
            'ml-mh&FF':            (ml - mh) & 0xFF,
            'ml*mh&FF':            (ml * mh) & 0xFF,
            'ml^mh':               (ml ^ mh) & 0xFF,
            'enc[0]':              enc[0] if enc else -1,
            'enc[0]^ml':           (enc[0] ^ ml) & 0xFF if enc else -1,
            'enc[0]^mh':           (enc[0] ^ mh) & 0xFF if enc else -1,
            'enc[0]^0xB7':         (enc[0] ^ 0xB7) & 0xFF if enc else -1,
            # Try involving both plain and server key
            'p[0]^sk[0]':          (p[0] ^ sk[0]) & 0xFF,
            'p[0]^sk[1]':          (p[0] ^ sk[1]) & 0xFF,
            'p[0]^sk[2]':          (p[0] ^ sk[2]) & 0xFF,
            'p[0]^sk[3]':          (p[0] ^ sk[3]) & 0xFF,
            'p[1]^sk[0]':          (p[1] ^ sk[0]) & 0xFF,
            'sum_plain^ml':        (sum(p) ^ ml) & 0xFF,
            'sum_plain^mh':        (sum(p) ^ mh) & 0xFF,
            # Try: verify might be derived from ck
            'ck':                  ck,
            'ck^p[0]':             (ck ^ p[0]) & 0xFF,
            'ck^p[1]':             (ck ^ p[1]) & 0xFF,
            'ck+p[0]&FF':          (ck + p[0]) & 0xFF,
            '(ck-p[0])&FF':        (ck - p[0]) & 0xFF,
            '(p[0]-ck)&FF':        (p[0] - ck) & 0xFF,
            # rotation
            '(p[0]<<1|p[0]>>7)&FF': ((p[0] << 1) | (p[0] >> 7)) & 0xFF,
            '(ml<<1|ml>>7)&FF':    ((ml << 1) | (ml >> 7)) & 0xFF,
        }

        d['v_tests'] = tests

    print(f"\n{'Formula':<30} {'Matches':>8}")
    print("-" * 40)
    if data:
        for fname in data[0]['v_tests']:
            matches = sum(1 for d in data if d['v_tests'][fname] == d['v'])
            if matches > 0:
                marker = " <<<< FOUND!" if matches == len(data) else ""
                print(f"  {fname:<28} {matches:3d}/{len(data)}{marker}")

    # ══════════════════════════════════════════════════════════════
    # PART 3: Brute force - try all single-byte XOR combinations
    # ══════════════════════════════════════════════════════════════
    print("\n" + "=" * 80)
    print("PART 3: BRUTE FORCE - Check if ck or v = a ^ b for any two values")
    print("=" * 80)

    # For each packet, we have: ml, mh, sk[0:4], p[0:18], enc[0:18], calc_ck
    # Try: for verify, is v = X ^ Y where X and Y are from known values?

    # Collect all "known bytes" per packet
    for d in data:
        p = d['plain']; sk = d['sk']; ml = d['ml']; mh = d['mh']
        vals = {
            'ml': ml, 'mh': mh,
            'sk0': sk[0], 'sk1': sk[1], 'sk2': sk[2], 'sk3': sk[3],
        }
        for i in range(min(18, len(p))):
            vals[f'p{i}'] = p[i]
        for i in range(min(18, len(d['enc']))):
            vals[f'e{i}'] = d['enc'][i]
        vals['calc_ck'] = d['calc_ck']
        d['vals'] = vals

    # For VERIFY: try v = valA ^ valB for all pairs
    val_names = list(data[0]['vals'].keys())
    print(f"\nTesting {len(val_names)}×{len(val_names)} XOR pairs for VERIFY...")
    verify_hits = {}
    for na in val_names:
        for nb in val_names:
            if na >= nb: continue  # avoid duplicates
            matches = sum(1 for d in data if (d['vals'][na] ^ d['vals'][nb]) & 0xFF == d['v'])
            if matches == len(data):
                print(f"  VERIFY = {na} ^ {nb}  ({matches}/{len(data)}) <<<< PERFECT MATCH!")
                verify_hits[f'{na}^{nb}'] = matches
            elif matches > len(data) * 0.8:
                print(f"  VERIFY ~ {na} ^ {nb}  ({matches}/{len(data)})")

    # For CHECKSUM: try ck = valA ^ valB
    print(f"\nTesting {len(val_names)}×{len(val_names)} XOR pairs for CHECKSUM...")
    ck_hits = {}
    for na in val_names:
        for nb in val_names:
            if na >= nb: continue
            matches = sum(1 for d in data if (d['vals'][na] ^ d['vals'][nb]) & 0xFF == d['ck'])
            if matches == len(data):
                print(f"  CHECKSUM = {na} ^ {nb}  ({matches}/{len(data)}) <<<< PERFECT MATCH!")
                ck_hits[f'{na}^{nb}'] = matches
            elif matches > len(data) * 0.8:
                print(f"  CHECKSUM ~ {na} ^ {nb}  ({matches}/{len(data)})")

    # Also try v = valA + valB, v = valA - valB
    print(f"\nTesting ADD pairs for VERIFY...")
    for na in val_names:
        for nb in val_names:
            if na >= nb: continue
            matches = sum(1 for d in data if (d['vals'][na] + d['vals'][nb]) & 0xFF == d['v'])
            if matches == len(data):
                print(f"  VERIFY = ({na} + {nb}) & 0xFF  ({matches}/{len(data)}) <<<< PERFECT!")

    print(f"\nTesting ADD pairs for CHECKSUM...")
    for na in val_names:
        for nb in val_names:
            if na >= nb: continue
            matches = sum(1 for d in data if (d['vals'][na] + d['vals'][nb]) & 0xFF == d['ck'])
            if matches == len(data):
                print(f"  CHECKSUM = ({na} + {nb}) & 0xFF  ({matches}/{len(data)}) <<<< PERFECT!")

    # Try single value match
    print(f"\nTesting single value match...")
    for na in val_names:
        v_matches = sum(1 for d in data if d['vals'][na] == d['v'])
        ck_matches = sum(1 for d in data if d['vals'][na] == d['ck'])
        if v_matches == len(data):
            print(f"  VERIFY = {na}  ({v_matches}/{len(data)}) <<<< PERFECT!")
        if ck_matches == len(data):
            print(f"  CHECKSUM = {na}  ({ck_matches}/{len(data)}) <<<< PERFECT!")

    # ══════════════════════════════════════════════════════════════
    # PART 4: Raw data dump for manual inspection
    # ══════════════════════════════════════════════════════════════
    print(f"\n{'='*80}")
    print("PART 4: Raw data for manual inspection (first 10)")
    print(f"{'='*80}\n")

    for d in data[:10]:
        p = d['plain']; sk = d['sk']
        print(f"PCAP: {d['pcap']}")
        print(f"  sk=[{sk[0]:02X},{sk[1]:02X},{sk[2]:02X},{sk[3]:02X}]  ml=0x{d['ml']:02X}  mh=0x{d['mh']:02X}")
        print(f"  ck=0x{d['ck']:02X}  v=0x{d['v']:02X}  calc_ck=0x{d['calc_ck']:02X}")
        print(f"  plain: {p.hex()}")
        print(f"  enc:   {d['enc'].hex()}")
        print(f"  seed:  [{p[0]:02X},{p[1]:02X},{p[2]:02X},{p[3]:02X}]")
        print()


if __name__ == '__main__':
    main()

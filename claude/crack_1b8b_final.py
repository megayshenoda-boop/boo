"""
HYPOTHESIS: 0x1B8B bytes[0] and [2] are standard ck/verify values ENCRYPTED at abs_i=4,6.

That is:
  plain_ck = sum(encrypted_data_bytes) & 0xFF    (standard checksum)
  plain_v  = msg_lo ^ 0xB7                        (standard verify)
  byte[0] = encrypt_byte(plain_ck, abs_i=4, sk, msg)
  byte[2] = encrypt_byte(plain_v, abs_i=6, sk, msg)

Also test: various abs_i offsets and different plaintext values for ck/v.
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


def encrypt_byte(plain_byte, abs_i, sk, msg):
    tb = TABLE[abs_i % 7]
    sb = sk[abs_i % 4]
    mb = msg[abs_i % 2]
    return (((plain_byte + mb * 17) & 0xFF) ^ sb ^ tb) & 0xFF


def decrypt_byte(enc_byte, abs_i, sk, msg):
    tb = TABLE[abs_i % 7]
    sb = sk[abs_i % 4]
    mb = msg[abs_i % 2]
    return ((enc_byte ^ sb ^ tb) - mb * 17) & 0xFF


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
                    ck = pl[0]; ml = pl[1]; v = pl[2]; mh = pl[3]
                    enc = pl[4:]
                    msg = [ml, mh]
                    # Decrypt data bytes (standard, abs_i starts at 8)
                    plain = bytearray(18)
                    for i in range(18):
                        plain[i] = decrypt_byte(enc[i], i + 8, sk, msg)
                    calc_ck = sum(enc) & 0xFF
                    data.append({
                        'pcap': pcap.name, 'ck': ck, 'ml': ml, 'v': v, 'mh': mh,
                        'enc': enc, 'plain': bytes(plain), 'sk': sk, 'msg': msg,
                        'calc_ck': calc_ck, 'sk_u32': sk_u32
                    })
        except: continue

    print(f"Loaded {len(data)} packets\n")

    # ══════════════════════════════════════════════════════════════
    # TEST 1: ck/v are encrypted standard values at abs_i=4,6
    # ══════════════════════════════════════════════════════════════
    print("=" * 80)
    print("TEST 1: Are ck/v = encrypt(standard_value, abs_i=4/6)?")
    print("=" * 80)

    for base_offset in [0, 2, 4, 6, 8]:
        ck_matches = 0
        v_matches = 0
        for d in data:
            std_ck = d['calc_ck']
            std_v = d['ml'] ^ 0xB7

            enc_ck = encrypt_byte(std_ck, base_offset + 0, d['sk'], d['msg'])
            enc_v = encrypt_byte(std_v, base_offset + 2, d['sk'], d['msg'])

            if enc_ck == d['ck']: ck_matches += 1
            if enc_v == d['v']: v_matches += 1

        print(f"  base_offset={base_offset}: ck={ck_matches}/{len(data)}, v={v_matches}/{len(data)}")

    # ══════════════════════════════════════════════════════════════
    # TEST 2: Try encrypting various plaintext candidates for ck position
    # ══════════════════════════════════════════════════════════════
    print("\n" + "=" * 80)
    print("TEST 2: Brute-force what plaintext byte at abs_i=4 produces observed ck")
    print("=" * 80)

    # For each packet, decrypt byte[0] at various abs_i to see what plaintext would be
    for ai in [0, 2, 4, 6]:
        plains_ck = []
        plains_v = []
        for d in data:
            p_ck = decrypt_byte(d['ck'], ai, d['sk'], d['msg'])
            p_v = decrypt_byte(d['v'], ai + 2, d['sk'], d['msg'])
            plains_ck.append(p_ck)
            plains_v.append(p_v)

        ck_unique = set(plains_ck)
        v_unique = set(plains_v)
        print(f"\n  abs_i={ai} for ck, abs_i={ai+2} for v:")
        print(f"    ck plaintext unique: {len(ck_unique)}  {sorted(ck_unique)[:10]}...")
        print(f"    v  plaintext unique: {len(v_unique)}  {sorted(v_unique)[:10]}...")

        # Check if ck_plain is always == calc_ck (standard checksum)
        ck_std_match = sum(1 for i, d in enumerate(data) if plains_ck[i] == d['calc_ck'])
        # Check if v_plain is always == ml ^ 0xB7
        v_std_match = sum(1 for i, d in enumerate(data) if plains_v[i] == (d['ml'] ^ 0xB7))
        # Check if ck_plain is always == sum(plain) & 0xFF
        ck_plain_sum = sum(1 for i, d in enumerate(data) if plains_ck[i] == (sum(d['plain']) & 0xFF))

        print(f"    ck_plain == calc_ck(sum_enc): {ck_std_match}/{len(data)}")
        print(f"    v_plain  == ml^0xB7:          {v_std_match}/{len(data)}")
        print(f"    ck_plain == sum(plain)&0xFF:   {ck_plain_sum}/{len(data)}")

    # ══════════════════════════════════════════════════════════════
    # TEST 3: What if msg bytes for ck/v encryption are DIFFERENT?
    # Like msg = [0, 0] or msg = [mh, ml] reversed
    # ══════════════════════════════════════════════════════════════
    print("\n" + "=" * 80)
    print("TEST 3: Different msg bytes for header encryption")
    print("=" * 80)

    msg_variants = [
        ('zero', lambda d: [0, 0]),
        ('reversed', lambda d: [d['mh'], d['ml']]),
        ('ml_ml', lambda d: [d['ml'], d['ml']]),
        ('mh_mh', lambda d: [d['mh'], d['mh']]),
        ('ck_v', lambda d: [d['ck'], d['v']]),
    ]

    for name, msg_fn in msg_variants:
        for ai_base in [0, 4]:
            ck_match = 0
            v_match = 0
            for d in data:
                alt_msg = msg_fn(d)
                enc_ck = encrypt_byte(d['calc_ck'], ai_base, d['sk'], alt_msg)
                enc_v = encrypt_byte(d['ml'] ^ 0xB7, ai_base + 2, d['sk'], alt_msg)
                if enc_ck == d['ck']: ck_match += 1
                if enc_v == d['v']: v_match += 1
            if ck_match > 5 or v_match > 5:
                print(f"  msg={name}, ai_base={ai_base}: ck={ck_match}/{len(data)}, v={v_match}/{len(data)}")

    # ══════════════════════════════════════════════════════════════
    # TEST 4: What if ck position uses sk_byte from a DIFFERENT index?
    # Try all 256 possible (abs_i % 7, abs_i % 4, abs_i % 2) combos
    # ══════════════════════════════════════════════════════════════
    print("\n" + "=" * 80)
    print("TEST 4: Brute force abs_i (0-27) for ck and v independently")
    print("=" * 80)

    # For ck: find which abs_i, when used to encrypt standard_ck, gives observed byte[0]
    for ai in range(28):  # cover all TABLE and SK indices
        match = sum(1 for d in data if encrypt_byte(d['calc_ck'], ai, d['sk'], d['msg']) == d['ck'])
        if match == len(data):
            print(f"  *** CK: encrypt(calc_ck, abs_i={ai}) PERFECT MATCH! ***")
        elif match > len(data) * 0.5:
            print(f"  CK: abs_i={ai}: {match}/{len(data)}")

    for ai in range(28):
        match = sum(1 for d in data if encrypt_byte(d['ml'] ^ 0xB7, ai, d['sk'], d['msg']) == d['v'])
        if match == len(data):
            print(f"  *** V: encrypt(ml^0xB7, abs_i={ai}) PERFECT MATCH! ***")
        elif match > len(data) * 0.5:
            print(f"  V: abs_i={ai}: {match}/{len(data)}")

    # Also try: encrypt(sum_plain, abs_i) for ck
    for ai in range(28):
        match = sum(1 for d in data if encrypt_byte(sum(d['plain']) & 0xFF, ai, d['sk'], d['msg']) == d['ck'])
        if match == len(data):
            print(f"  *** CK: encrypt(sum_plain, abs_i={ai}) PERFECT MATCH! ***")
        elif match > len(data) * 0.5:
            print(f"  CK(sum_plain): abs_i={ai}: {match}/{len(data)}")

    # ══════════════════════════════════════════════════════════════
    # TEST 5: Triple XOR/ADD combos (a op b op c)
    # ══════════════════════════════════════════════════════════════
    print("\n" + "=" * 80)
    print("TEST 5: Triple XOR combos for ck and v")
    print("=" * 80)

    # Use smaller set of key values to keep combinatorics manageable
    key_vals = ['ml', 'mh', 'sk0', 'sk1', 'sk2', 'sk3', 'calc_ck', 'p0', 'p1', 'p2', 'p3']

    # Build value dict for each packet
    for d in data:
        d['kv'] = {
            'ml': d['ml'], 'mh': d['mh'],
            'sk0': d['sk'][0], 'sk1': d['sk'][1], 'sk2': d['sk'][2], 'sk3': d['sk'][3],
            'calc_ck': d['calc_ck'],
            'p0': d['plain'][0], 'p1': d['plain'][1], 'p2': d['plain'][2], 'p3': d['plain'][3],
        }

    # Try ck = a ^ b ^ c
    for i, a in enumerate(key_vals):
        for j, b in enumerate(key_vals):
            if j <= i: continue
            for k, c in enumerate(key_vals):
                if k <= j: continue
                ck_m = sum(1 for d in data if (d['kv'][a] ^ d['kv'][b] ^ d['kv'][c]) & 0xFF == d['ck'])
                v_m = sum(1 for d in data if (d['kv'][a] ^ d['kv'][b] ^ d['kv'][c]) & 0xFF == d['v'])
                if ck_m == len(data):
                    print(f"  *** CK = {a} ^ {b} ^ {c} PERFECT! ***")
                if v_m == len(data):
                    print(f"  *** V = {a} ^ {b} ^ {c} PERFECT! ***")

    # Try ck = a + b + c
    for i, a in enumerate(key_vals):
        for j, b in enumerate(key_vals):
            if j <= i: continue
            for k, c in enumerate(key_vals):
                if k <= j: continue
                ck_m = sum(1 for d in data if (d['kv'][a] + d['kv'][b] + d['kv'][c]) & 0xFF == d['ck'])
                v_m = sum(1 for d in data if (d['kv'][a] + d['kv'][b] + d['kv'][c]) & 0xFF == d['v'])
                if ck_m == len(data):
                    print(f"  *** CK = ({a} + {b} + {c}) & 0xFF PERFECT! ***")
                if v_m == len(data):
                    print(f"  *** V = ({a} + {b} + {c}) & 0xFF PERFECT! ***")

    # ══════════════════════════════════════════════════════════════
    # TEST 6: CRC-8 of various data segments
    # ══════════════════════════════════════════════════════════════
    print("\n" + "=" * 80)
    print("TEST 6: CRC-8 and other hashes")
    print("=" * 80)

    def crc8(data_bytes, poly=0x07, init=0x00):
        crc = init
        for b in data_bytes:
            crc ^= b
            for _ in range(8):
                if crc & 0x80:
                    crc = ((crc << 1) ^ poly) & 0xFF
                else:
                    crc = (crc << 1) & 0xFF
        return crc

    crc_polys = [0x07, 0x31, 0x1D, 0x9B, 0xD5, 0x39, 0x2F, 0x4D]
    segments = [
        ('plain', lambda d: d['plain']),
        ('enc', lambda d: d['enc']),
        ('plain[:4]', lambda d: d['plain'][:4]),
        ('enc+ml_mh', lambda d: bytes([d['ml'], d['mh']]) + d['enc']),
        ('ml_v_mh_enc', lambda d: bytes([d['ml'], d['v'], d['mh']]) + d['enc']),
        ('full_payload', lambda d: bytes([d['ck'], d['ml'], d['v'], d['mh']]) + d['enc']),
    ]

    for seg_name, seg_fn in segments:
        for poly in crc_polys:
            for init in [0x00, 0xFF]:
                ck_m = sum(1 for d in data if crc8(seg_fn(d), poly, init) == d['ck'])
                v_m = sum(1 for d in data if crc8(seg_fn(d), poly, init) == d['v'])
                if ck_m == len(data):
                    print(f"  *** CK = CRC8({seg_name}, poly=0x{poly:02X}, init=0x{init:02X}) PERFECT! ***")
                if v_m == len(data):
                    print(f"  *** V = CRC8({seg_name}, poly=0x{poly:02X}, init=0x{init:02X}) PERFECT! ***")

    # ══════════════════════════════════════════════════════════════
    # TEST 7: What if ck and v involve the TABLE directly?
    # ══════════════════════════════════════════════════════════════
    print("\n" + "=" * 80)
    print("TEST 7: Formulas involving TABLE values and sk")
    print("=" * 80)

    for ti in range(7):
        for si in range(4):
            # ck = calc_ck ^ TABLE[ti] ^ sk[si]
            m = sum(1 for d in data if (d['calc_ck'] ^ TABLE[ti] ^ d['sk'][si]) & 0xFF == d['ck'])
            if m == len(data):
                print(f"  *** CK = calc_ck ^ TABLE[{ti}] ^ sk[{si}] PERFECT! ***")
            # ck = (calc_ck + ml*17) ^ TABLE[ti] ^ sk[si]
            m = sum(1 for d in data if (((d['calc_ck'] + d['ml']*17) & 0xFF) ^ TABLE[ti] ^ d['sk'][si]) == d['ck'])
            if m == len(data):
                print(f"  *** CK = (calc_ck + ml*17) ^ TABLE[{ti}] ^ sk[{si}] PERFECT! ***")
            # v = (ml^0xB7 + msg*17) ^ TABLE[ti] ^ sk[si]
            for mi in range(2):
                msg_byte = [0, 0]  # will be set per-packet
                m = sum(1 for d in data if (((d['ml'] ^ 0xB7) + d['msg'][mi]*17) & 0xFF) ^ TABLE[ti] ^ d['sk'][si] == d['v'])
                if m == len(data):
                    print(f"  *** V = ((ml^0xB7)+msg[{mi}]*17)^TABLE[{ti}]^sk[{si}] PERFECT! ***")

    # ══════════════════════════════════════════════════════════════
    # TEST 8: Completely different idea - maybe ck/v use a PACKET COUNTER
    # Check if the ck/v pattern repeats or is sequential within each PCAP
    # ══════════════════════════════════════════════════════════════
    print("\n" + "=" * 80)
    print("TEST 8: Check for per-PCAP packet counting pattern")
    print("=" * 80)

    from collections import defaultdict
    pcap_groups = defaultdict(list)
    for d in data:
        pcap_groups[d['pcap']].append(d)

    for pname, pkts in sorted(pcap_groups.items()):
        if len(pkts) > 1:
            print(f"\n  {pname} ({len(pkts)} packets):")
            for i, d in enumerate(pkts):
                diff_ck = (pkts[1]['ck'] - pkts[0]['ck']) & 0xFF if len(pkts) > 1 and i == 0 else 0
                print(f"    #{i}: ck=0x{d['ck']:02X} v=0x{d['v']:02X} ml=0x{d['ml']:02X} mh=0x{d['mh']:02X}")

    print(f"\n\nTotal packets per PCAP: {dict((k, len(v)) for k, v in pcap_groups.items())}")
    print("\nDone.")


if __name__ == '__main__':
    main()

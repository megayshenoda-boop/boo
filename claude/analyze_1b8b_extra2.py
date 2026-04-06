"""
Deep analysis: check if extra bytes are encrypted versions of something,
or if they relate to the full encrypted payload, or are simply random.
"""
import struct, sys
from pathlib import Path
from collections import Counter

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
    packets = []
    pos = 0
    while pos + 4 <= len(raw):
        pkt_len = struct.unpack('<H', raw[pos:pos+2])[0]
        opcode = struct.unpack('<H', raw[pos+2:pos+4])[0]
        if pkt_len < 4 or pkt_len > 65535 or pos + pkt_len > len(raw): break
        packets.append((opcode, bytes(raw[pos:pos+pkt_len])))
        pos += pkt_len
    return packets


def extract_server_key(raw):
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
    for sub in ['rebel_attack', 'codex_lab', 'config-decryptor']:
        p = pcap_dir / sub
        if p.exists():
            pcaps.extend(sorted(p.glob('*.pcap')))

    results = []

    for pcap in pcaps:
        try:
            s = read_pcap_streams(pcap)
            if 'C2S' not in s or 'S2C' not in s: continue
            sk_u32 = extract_server_key(s['S2C'])
            if not sk_u32: continue
            sk = [sk_u32 & 0xFF, (sk_u32 >> 8) & 0xFF, (sk_u32 >> 16) & 0xFF, (sk_u32 >> 24) & 0xFF]
            c2s_raw = parse_packets_raw(s['C2S'])
            for op, raw_pkt in c2s_raw:
                if op != 0x1B8B or len(raw_pkt) != 26:
                    continue
                results.append({
                    'extra0': raw_pkt[4],
                    'extra1': raw_pkt[5],
                    'ck': raw_pkt[6],
                    'ml': raw_pkt[7],
                    'v': raw_pkt[8],
                    'mh': raw_pkt[9],
                    'enc': raw_pkt[10:26],
                    'sk': sk,
                    'sk_u32': sk_u32,
                    'raw': raw_pkt,
                })
        except:
            continue

    print(f"Total packets: {len(results)}")

    # ============================================================
    # TEST 1: Are extra bytes encrypted using the same formula at offset 4,5?
    # If the encryption applies to the ENTIRE payload (not just offset 10+),
    # then extra[0] = encrypt(plain_extra0, abs_i=4), extra[1] = encrypt(plain_extra1, abs_i=5)
    # ============================================================
    print("\n=== TEST 1: Decrypt extra bytes as if encrypted at abs_i=4,5 ===")
    for r in results[:10]:
        sk = r['sk']
        msg = [r['ml'], r['mh']]
        for test_offset in [0, 4, 6]:
            d = []
            for j in range(2):
                abs_i = j + test_offset
                tb = TABLE[abs_i % 7]
                sb = sk[abs_i % 4]
                mb = msg[abs_i % 2]
                d.append(((r['extra0' if j==0 else 'extra1'] ^ sb ^ tb) - mb * 17) & 0xFF)
            print(f"  e=({r['extra0']:02X},{r['extra1']:02X}) offset={test_offset}: decrypted=({d[0]:02X},{d[1]:02X})")

    # ============================================================
    # TEST 2: Are extra bytes = encrypt(0x00, 0x00) at some offset?
    # i.e. extra[i] = ((0x00 + msg*17) ^ sk ^ tbl) & 0xFF
    # ============================================================
    print("\n=== TEST 2: Check if extra = encrypt(0,0) at various offsets ===")
    for test_offset in range(20):
        match_count = 0
        for r in results:
            sk = r['sk']
            msg = [r['ml'], r['mh']]
            e0_expected = ((0 + msg[(test_offset) % 2] * 17) ^ sk[(test_offset) % 4] ^ TABLE[(test_offset) % 7]) & 0xFF
            e1_expected = ((0 + msg[(test_offset+1) % 2] * 17) ^ sk[(test_offset+1) % 4] ^ TABLE[(test_offset+1) % 7]) & 0xFF
            if e0_expected == r['extra0'] and e1_expected == r['extra1']:
                match_count += 1
        if match_count > 0:
            print(f"  offset={test_offset}: {match_count}/{len(results)} match encrypt(0,0)")

    # ============================================================
    # TEST 3: Check if extra bytes are just encrypt(known_plain) for known values
    # The plaintext is always ed027322... so check with those bytes at offset 4,5
    # ============================================================
    print("\n=== TEST 3: Check extra = encrypt(known_plain_bytes) at various offsets ===")
    known_plain_bytes = [0xED, 0x02, 0x73, 0x22, 0x00, 0x00, 0x00, 0x00]
    for test_offset in range(20):
        match_count = 0
        for r in results:
            sk = r['sk']
            msg = [r['ml'], r['mh']]
            match = True
            for j in range(2):
                abs_i = j + test_offset
                p_idx = j  # use first 2 known plain bytes
                pb = known_plain_bytes[p_idx] if p_idx < len(known_plain_bytes) else 0
                expected = ((pb + msg[abs_i % 2] * 17) ^ sk[abs_i % 4] ^ TABLE[abs_i % 7]) & 0xFF
                actual = r['extra0'] if j == 0 else r['extra1']
                if expected != actual:
                    match = False
                    break
            if match:
                match_count += 1
        if match_count > 0:
            print(f"  offset={test_offset}, plain=[ED,02]: {match_count}/{len(results)} match")

    # Also try all plain bytes combos at common offsets
    for test_offset in [0, 2, 4, 6, 8]:
        for p0 in range(256):
            match_count = 0
            for r in results[:5]:  # quick check on first 5
                sk = r['sk']
                msg = [r['ml'], r['mh']]
                abs_i = test_offset
                expected = ((p0 + msg[abs_i % 2] * 17) ^ sk[abs_i % 4] ^ TABLE[abs_i % 7]) & 0xFF
                if expected == r['extra0']:
                    match_count += 1
            if match_count == 5:
                # Found a constant plain[0] that works for all first 5
                # Verify on all
                full_match = all(
                    ((p0 + r['ml'] * 17 if test_offset % 2 == 0 else p0 + r['mh'] * 17) ^ r['sk'][test_offset % 4] ^ TABLE[test_offset % 7]) & 0xFF == r['extra0']
                    for r in results
                )
                if full_match:
                    print(f"  *** extra[0] = encrypt(0x{p0:02X}) at abs_i={test_offset} ***")

    # ============================================================
    # TEST 4: Statistical randomness check
    # ============================================================
    print("\n=== TEST 4: Statistical analysis ===")
    e0_vals = [r['extra0'] for r in results]
    e1_vals = [r['extra1'] for r in results]
    print(f"  extra[0]: min={min(e0_vals):02X} max={max(e0_vals):02X} mean={sum(e0_vals)/len(e0_vals):.1f} "
          f"(ideal for uniform: 127.5)")
    print(f"  extra[1]: min={min(e1_vals):02X} max={max(e1_vals):02X} mean={sum(e1_vals)/len(e1_vals):.1f}")

    # Check bit distribution
    for name, vals in [('extra[0]', e0_vals), ('extra[1]', e1_vals)]:
        bit_counts = [0] * 8
        for v in vals:
            for b in range(8):
                if v & (1 << b):
                    bit_counts[b] += 1
        print(f"  {name} bit distribution: {bit_counts} (ideal: {len(vals)/2:.0f} each)")

    # ============================================================
    # TEST 5: Check if extra as u16 relates to sk as u16 pairs
    # ============================================================
    print("\n=== TEST 5: Extra u16 vs SK u16 ===")
    for r in results[:10]:
        extra_u16 = r['extra0'] | (r['extra1'] << 8)
        sk_lo = r['sk_u32'] & 0xFFFF
        sk_hi = (r['sk_u32'] >> 16) & 0xFFFF
        msg_u16 = r['ml'] | (r['mh'] << 8)
        # Check: extra = (sk_lo * msg_lo) & 0xFFFF etc
        print(f"  extra=0x{extra_u16:04X} sk_lo=0x{sk_lo:04X} sk_hi=0x{sk_hi:04X} msg=0x{msg_u16:04X} "
              f"| (sk_lo*ml)&FFFF=0x{(sk_lo*r['ml'])&0xFFFF:04X} "
              f"| (sk_lo+msg)&FFFF=0x{(sk_lo+msg_u16)&0xFFFF:04X} "
              f"| (sk_hi+msg)&FFFF=0x{(sk_hi+msg_u16)&0xFFFF:04X} "
              f"| (sk_lo^msg)=0x{sk_lo^msg_u16:04X} "
              f"| (sk_hi^msg)=0x{sk_hi^msg_u16:04X}")

    # ============================================================
    # TEST 6: Duplicate server key case - sk=0x88587D29 has 2 packets
    # ============================================================
    print("\n=== TEST 6: Same server_key, different extras ===")
    from collections import defaultdict
    by_sk = defaultdict(list)
    for r in results:
        by_sk[r['sk_u32']].append(r)
    for sk_val, items in by_sk.items():
        if len(items) > 1:
            print(f"  sk=0x{sk_val:08X} has {len(items)} packets:")
            for it in items:
                print(f"    extra=({it['extra0']:02X},{it['extra1']:02X}) ml={it['ml']:02X} mh={it['mh']:02X} ck={it['ck']:02X}")

    # ============================================================
    # TEST 7: Are they encrypted with a DIFFERENT key/formula?
    # Maybe extra = enc(plain) using Function 1 (the standard header formula at offset 4)
    # Standard header: [ck][ml][v][mh] at offsets 4,5,6,7
    # But maybe the extra bytes use a simpler scheme
    # ============================================================
    print("\n=== TEST 7: Check extra[0] XOR TABLE[i] for all i ===")
    for tbl_idx in range(7):
        vals = set()
        for r in results:
            vals.add(r['extra0'] ^ TABLE[tbl_idx])
        print(f"  extra[0] ^ TABLE[{tbl_idx}] (0x{TABLE[tbl_idx]:02X}): {len(vals)} unique values (80=random)")

    # ============================================================
    # TEST 8: Could they be random bytes from the client?
    # Check entropy
    # ============================================================
    import math
    print("\n=== TEST 8: Entropy analysis ===")
    for name, vals in [('extra[0]', e0_vals), ('extra[1]', e1_vals), ('ml', [r['ml'] for r in results]), ('mh', [r['mh'] for r in results])]:
        counter = Counter(vals)
        total = len(vals)
        entropy = -sum((c/total) * math.log2(c/total) for c in counter.values())
        max_entropy = math.log2(total) if total > 0 else 0
        print(f"  {name}: entropy={entropy:.2f} bits (max possible for {total} values: {max_entropy:.2f})")

    print("\n=== CONCLUSION ===")
    print("If no systematic patterns found, extra bytes are likely RANDOM (client-generated nonce).")
    print("They may serve as a session-specific salt or sequence identifier.")


if __name__ == '__main__':
    main()

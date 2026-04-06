"""
Analyze 0x1B8B packet extra bytes (pkt[4:6]) across ALL PCAPs.

Packet structure:
[len:2][opcode:2][extra:2][ck:1][ml:1][v:1][mh:1][encrypted:16]

Goal: find what determines extra[0] and extra[1].
"""
import struct, sys, os
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


def decrypt_1b8b(enc, sk_bytes, msg):
    plain = bytearray(16)
    for i in range(16):
        abs_i = i + 10
        tb = TABLE[abs_i % 7]
        sb = sk_bytes[abs_i % 4]
        mb = msg[abs_i % 2]
        plain[i] = ((enc[i] ^ sb ^ tb) - mb * 17) & 0xFF
    return plain


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

                extra0 = raw_pkt[4]
                extra1 = raw_pkt[5]
                ck = raw_pkt[6]
                ml = raw_pkt[7]
                v = raw_pkt[8]
                mh = raw_pkt[9]
                enc = raw_pkt[10:26]

                msg = [ml, mh]
                plain = decrypt_1b8b(enc, sk, msg)

                # Extract IGG ID from plaintext (first 4 bytes LE)
                igg_id = struct.unpack('<I', plain[0:4])[0]

                results.append({
                    'file': pcap.name,
                    'extra0': extra0,
                    'extra1': extra1,
                    'sk_u32': sk_u32,
                    'sk': sk,
                    'ml': ml,
                    'mh': mh,
                    'ck': ck,
                    'v': v,
                    'enc': enc,
                    'plain': plain,
                    'igg_id': igg_id,
                    'raw': raw_pkt,
                })
        except Exception as e:
            continue

    if not results:
        print("No 0x1B8B packets found!")
        return

    # ============================================================
    # DISPLAY ALL RESULTS
    # ============================================================
    print("=" * 100)
    print(f"Found {len(results)} 0x1B8B packets across all PCAPs")
    print("=" * 100)

    for i, r in enumerate(results):
        print(f"\n[{i}] {r['file']}")
        print(f"  extra=[0x{r['extra0']:02X}, 0x{r['extra1']:02X}]  "
              f"sk=0x{r['sk_u32']:08X} [{r['sk'][0]:02X},{r['sk'][1]:02X},{r['sk'][2]:02X},{r['sk'][3]:02X}]  "
              f"ml=0x{r['ml']:02X} mh=0x{r['mh']:02X} ck=0x{r['ck']:02X}")
        print(f"  plain: {r['plain'].hex()}  IGG_ID={r['igg_id']}")

    # ============================================================
    # PATTERN ANALYSIS
    # ============================================================
    print("\n" + "=" * 100)
    print("PATTERN ANALYSIS")
    print("=" * 100)

    # Check uniqueness of extra bytes
    extras = [(r['extra0'], r['extra1']) for r in results]
    unique_extras = set(extras)
    print(f"\nUnique extra pairs: {len(unique_extras)} out of {len(results)} packets")
    for ex in sorted(unique_extras):
        count = extras.count(ex)
        print(f"  (0x{ex[0]:02X}, 0x{ex[1]:02X}) -> {count} times")

    # Check: are extra bytes the same across all packets?
    if len(unique_extras) == 1:
        print("\n*** CONSTANT: extra bytes are always the same! ***")

    # Check: per server_key grouping
    print("\n--- Grouped by server_key ---")
    by_sk = {}
    for r in results:
        by_sk.setdefault(r['sk_u32'], []).append(r)
    for sk_val, items in sorted(by_sk.items()):
        sk_extras = set((it['extra0'], it['extra1']) for it in items)
        print(f"  sk=0x{sk_val:08X}: {len(items)} packets, unique extras: {sk_extras}")

    # Check: XOR relationships
    print("\n--- XOR/ADD/SUB with server_key bytes ---")
    for r in results[:10]:
        e0, e1 = r['extra0'], r['extra1']
        sk = r['sk']
        ml, mh = r['ml'], r['mh']
        print(f"  e0=0x{e0:02X} e1=0x{e1:02X} | "
              f"e0^sk0=0x{e0^sk[0]:02X} e0^sk1=0x{e0^sk[1]:02X} e0^sk2=0x{e0^sk[2]:02X} e0^sk3=0x{e0^sk[3]:02X} | "
              f"e1^sk0=0x{e1^sk[0]:02X} e1^sk1=0x{e1^sk[1]:02X} e1^sk2=0x{e1^sk[2]:02X} e1^sk3=0x{e1^sk[3]:02X}")

    print("\n--- XOR with msg bytes ---")
    for r in results[:10]:
        e0, e1 = r['extra0'], r['extra1']
        ml, mh = r['ml'], r['mh']
        print(f"  e0=0x{e0:02X} e1=0x{e1:02X} | "
              f"e0^ml=0x{e0^ml:02X} e0^mh=0x{e0^mh:02X} | "
              f"e1^ml=0x{e1^ml:02X} e1^mh=0x{e1^mh:02X}")

    print("\n--- Relationship with plaintext bytes ---")
    for r in results[:10]:
        e0, e1 = r['extra0'], r['extra1']
        p = r['plain']
        print(f"  e0=0x{e0:02X} e1=0x{e1:02X} | "
              f"p[0]=0x{p[0]:02X} p[1]=0x{p[1]:02X} p[2]=0x{p[2]:02X} p[3]=0x{p[3]:02X} | "
              f"e0^p0=0x{e0^p[0]:02X} e0^p1=0x{e0^p[1]:02X} e1^p0=0x{e1^p[0]:02X} e1^p1=0x{e1^p[1]:02X}")

    print("\n--- Relationship with checksum and verify ---")
    for r in results[:10]:
        e0, e1 = r['extra0'], r['extra1']
        ck, v = r['ck'], r['v']
        print(f"  e0=0x{e0:02X} e1=0x{e1:02X} | ck=0x{ck:02X} v=0x{v:02X} | "
              f"e0^ck=0x{e0^ck:02X} e1^ck=0x{e1^ck:02X} | "
              f"e0^v=0x{e0^v:02X} e1^v=0x{e1^v:02X}")

    # Check: ADD/SUB relationships with sk bytes
    print("\n--- ADD/SUB with server_key bytes ---")
    for r in results[:10]:
        e0, e1 = r['extra0'], r['extra1']
        sk = r['sk']
        print(f"  e0=0x{e0:02X} e1=0x{e1:02X} | "
              f"(e0-sk0)&FF=0x{(e0-sk[0])&0xFF:02X} (e0-sk1)&FF=0x{(e0-sk[1])&0xFF:02X} "
              f"(e0-sk2)&FF=0x{(e0-sk[2])&0xFF:02X} (e0-sk3)&FF=0x{(e0-sk[3])&0xFF:02X} | "
              f"(e1-sk0)&FF=0x{(e1-sk[0])&0xFF:02X} (e1-sk1)&FF=0x{(e1-sk[1])&0xFF:02X} "
              f"(e1-sk2)&FF=0x{(e1-sk[2])&0xFF:02X} (e1-sk3)&FF=0x{(e1-sk[3])&0xFF:02X}")

    # Check: are extra bytes derived from IGG ID?
    print("\n--- Relationship with IGG_ID ---")
    for r in results[:10]:
        e0, e1 = r['extra0'], r['extra1']
        igg = r['igg_id']
        igg_bytes = [(igg >> (8*j)) & 0xFF for j in range(4)]
        print(f"  e0=0x{e0:02X} e1=0x{e1:02X} | IGG_ID={igg} (0x{igg:08X}) | "
              f"igg[0]=0x{igg_bytes[0]:02X} igg[1]=0x{igg_bytes[1]:02X} | "
              f"e0^igg0=0x{e0^igg_bytes[0]:02X} e0^igg1=0x{e0^igg_bytes[1]:02X} "
              f"e1^igg0=0x{e1^igg_bytes[0]:02X} e1^igg1=0x{e1^igg_bytes[1]:02X}")

    # Check: extra = msg_lo/msg_hi related?
    print("\n--- Are extra bytes correlated with msg across packets? ---")
    # Group by same extra pair
    for ex_pair in sorted(unique_extras):
        matching = [r for r in results if (r['extra0'], r['extra1']) == ex_pair]
        mls = [r['ml'] for r in matching]
        mhs = [r['mh'] for r in matching]
        sks = set(r['sk_u32'] for r in matching)
        iggs = set(r['igg_id'] for r in matching)
        print(f"  extra=(0x{ex_pair[0]:02X},0x{ex_pair[1]:02X}): "
              f"ml_range=[0x{min(mls):02X}-0x{max(mls):02X}] "
              f"mh_range=[0x{min(mhs):02X}-0x{max(mhs):02X}] "
              f"unique_sks={len(sks)} unique_iggs={iggs}")

    # Check: as uint16
    print("\n--- Extra as uint16 LE ---")
    for r in results[:10]:
        extra_u16 = r['extra0'] | (r['extra1'] << 8)
        msg_u16 = r['ml'] | (r['mh'] << 8)
        print(f"  extra_u16={extra_u16} (0x{extra_u16:04X}) | "
              f"msg_u16={msg_u16} (0x{msg_u16:04X}) | "
              f"sk_u32=0x{r['sk_u32']:08X} | "
              f"extra^msg=0x{extra_u16^msg_u16:04X} | "
              f"extra-msg={(extra_u16-msg_u16)&0xFFFF} | "
              f"extra^sk_lo=0x{extra_u16^(r['sk_u32']&0xFFFF):04X} | "
              f"extra^sk_hi=0x{extra_u16^((r['sk_u32']>>16)&0xFFFF):04X}")

    # Systematic: check if extra[0] == f(any_other_field) for simple ops
    print("\n--- SYSTEMATIC: checking extra[0] against all single-byte fields ---")
    fields = {
        'sk[0]': lambda r: r['sk'][0],
        'sk[1]': lambda r: r['sk'][1],
        'sk[2]': lambda r: r['sk'][2],
        'sk[3]': lambda r: r['sk'][3],
        'ml': lambda r: r['ml'],
        'mh': lambda r: r['mh'],
        'ck': lambda r: r['ck'],
        'v': lambda r: r['v'],
        'p[0]': lambda r: r['plain'][0],
        'p[1]': lambda r: r['plain'][1],
        'p[2]': lambda r: r['plain'][2],
        'p[3]': lambda r: r['plain'][3],
        'p[4]': lambda r: r['plain'][4],
        'p[5]': lambda r: r['plain'][5],
        'p[6]': lambda r: r['plain'][6],
        'p[7]': lambda r: r['plain'][7],
        'enc[0]': lambda r: r['enc'][0],
        'enc[1]': lambda r: r['enc'][1],
    }
    ops = {
        'XOR': lambda a, b: a ^ b,
        'ADD': lambda a, b: (a + b) & 0xFF,
        'SUB': lambda a, b: (a - b) & 0xFF,
        'EQ': lambda a, b: a,
    }

    for fname, fget in fields.items():
        for opname, opfn in ops.items():
            # Check if extra[0] == op(field_val) for all packets (constant result)
            vals = set()
            for r in results:
                fv = fget(r)
                if opname == 'EQ':
                    vals.add(r['extra0'] == fv)
                else:
                    vals.add(opfn(r['extra0'], fv))
            if opname == 'EQ':
                if all(vals):
                    print(f"  *** MATCH: extra[0] == {fname} for ALL packets! ***")
            else:
                if len(vals) == 1:
                    print(f"  *** CONSTANT: extra[0] {opname} {fname} = 0x{list(vals)[0]:02X} for ALL packets! ***")

    # Same for extra[1]
    print("\n--- SYSTEMATIC: checking extra[1] against all single-byte fields ---")
    for fname, fget in fields.items():
        for opname, opfn in ops.items():
            vals = set()
            for r in results:
                fv = fget(r)
                if opname == 'EQ':
                    vals.add(r['extra1'] == fv)
                else:
                    vals.add(opfn(r['extra1'], fv))
            if opname == 'EQ':
                if all(vals):
                    print(f"  *** MATCH: extra[1] == {fname} for ALL packets! ***")
            else:
                if len(vals) == 1:
                    print(f"  *** CONSTANT: extra[1] {opname} {fname} = 0x{list(vals)[0]:02X} for ALL packets! ***")

    # Check two-field combinations: extra[0] = f(a, b)
    print("\n--- SYSTEMATIC: checking extra[0] = field_a XOR field_b ---")
    field_names = list(fields.keys())
    for i_a, fa_name in enumerate(field_names):
        for i_b, fb_name in enumerate(field_names):
            if i_b <= i_a: continue
            fa_get = fields[fa_name]
            fb_get = fields[fb_name]
            match = all(r['extra0'] == (fa_get(r) ^ fb_get(r)) & 0xFF for r in results)
            if match:
                print(f"  *** MATCH: extra[0] == {fa_name} XOR {fb_name} ***")
            match2 = all(r['extra0'] == (fa_get(r) + fb_get(r)) & 0xFF for r in results)
            if match2:
                print(f"  *** MATCH: extra[0] == ({fa_name} + {fb_name}) & 0xFF ***")

    print("\n--- SYSTEMATIC: checking extra[1] = field_a XOR field_b ---")
    for i_a, fa_name in enumerate(field_names):
        for i_b, fb_name in enumerate(field_names):
            if i_b <= i_a: continue
            fa_get = fields[fa_name]
            fb_get = fields[fb_name]
            match = all(r['extra1'] == (fa_get(r) ^ fb_get(r)) & 0xFF for r in results)
            if match:
                print(f"  *** MATCH: extra[1] == {fa_name} XOR {fb_name} ***")
            match2 = all(r['extra1'] == (fa_get(r) + fb_get(r)) & 0xFF for r in results)
            if match2:
                print(f"  *** MATCH: extra[1] == ({fa_name} + {fb_name}) & 0xFF ***")

    # Final: raw hex dump of all extra pairs for visual inspection
    print("\n--- RAW EXTRA PAIRS (all packets) ---")
    for i, r in enumerate(results):
        print(f"  [{i:2d}] extra=({r['extra0']:02X},{r['extra1']:02X})  "
              f"ml={r['ml']:02X} mh={r['mh']:02X} ck={r['ck']:02X}  "
              f"sk=[{r['sk'][0]:02X},{r['sk'][1]:02X},{r['sk'][2]:02X},{r['sk'][3]:02X}]  "
              f"IGG={r['igg_id']}")


if __name__ == '__main__':
    main()

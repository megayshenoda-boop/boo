#!/usr/bin/env python3
"""
41_march_and_castle_decode.py - Comprehensive march, castle, chat, and opcode analysis
======================================================================================
1. Find march-related server responses (0x0071, 0x006F, 0x00B8, 0x0037, 0x0CE9, post-0x0CE8)
2. Decode CASTLE_DATA (0x0038) TLV format
3. Decode 0x026D chat messages
4. Top 30 most frequent opcodes with format analysis
"""
import struct, os, glob, sys, collections, textwrap

PCAP_DIR = r"D:\CascadeProjects"
OUT_DIR = r"D:\CascadeProjects\analysis\findings"

def read_all_packets(pcap_path):
    """Read all game packets from a PCAP, preserving per-stream order."""
    packets = []
    try:
        with open(pcap_path, 'rb') as f:
            magic = f.read(4)
            endian = '<' if magic == b'\xd4\xc3\xb2\xa1' else '>'
            rest = f.read(20)
            network = struct.unpack(endian + 'I', rest[16:20])[0]

            tcp_streams = {}
            pkt_order = []  # (key, ts, raw_payload)
            pkt_idx = 0
            while True:
                hdr = f.read(16)
                if len(hdr) < 16: break
                ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
                pkt = f.read(incl_len)
                if len(pkt) < incl_len: break

                if network == 101: ip_start = 0
                elif network == 113: ip_start = 16
                else:
                    if len(pkt) < 14: continue
                    if struct.unpack('>H', pkt[12:14])[0] != 0x0800: continue
                    ip_start = 14

                if ip_start + 20 > len(pkt): continue
                ip_hdr_len = (pkt[ip_start] & 0x0F) * 4
                if pkt[ip_start + 9] != 6: continue

                tcp_start = ip_start + ip_hdr_len
                if tcp_start + 20 > len(pkt): continue
                sp = struct.unpack('>H', pkt[tcp_start:tcp_start+2])[0]
                dp = struct.unpack('>H', pkt[tcp_start+2:tcp_start+4])[0]
                tcp_hdr_len = ((pkt[tcp_start + 12] >> 4) & 0xF) * 4
                payload = pkt[tcp_start + tcp_hdr_len:]
                if not payload: continue

                key = (sp, dp)
                if key not in tcp_streams:
                    tcp_streams[key] = bytearray()
                tcp_streams[key] += payload
                pkt_idx += 1

            for (sp, dp), buf in tcp_streams.items():
                pos = 0
                while pos + 4 <= len(buf):
                    pkt_len = struct.unpack('<H', buf[pos:pos+2])[0]
                    opcode = struct.unpack('<H', buf[pos+2:pos+4])[0]
                    if pkt_len < 4 or pkt_len > 65000:
                        pos += 1; continue
                    if pos + pkt_len > len(buf): break
                    payload = bytes(buf[pos+4:pos+pkt_len])
                    packets.append((opcode, payload, sp, dp, pos))
                    pos += pkt_len
    except Exception as e:
        pass
    return packets


def read_all_packets_ordered(pcap_path):
    """Read packets preserving chronological order across streams."""
    ordered = []
    try:
        with open(pcap_path, 'rb') as f:
            magic = f.read(4)
            endian = '<' if magic == b'\xd4\xc3\xb2\xa1' else '>'
            rest = f.read(20)
            network = struct.unpack(endian + 'I', rest[16:20])[0]

            raw_packets = []
            while True:
                hdr = f.read(16)
                if len(hdr) < 16: break
                ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
                pkt = f.read(incl_len)
                if len(pkt) < incl_len: break

                if network == 101: ip_start = 0
                elif network == 113: ip_start = 16
                else:
                    if len(pkt) < 14: continue
                    if struct.unpack('>H', pkt[12:14])[0] != 0x0800: continue
                    ip_start = 14

                if ip_start + 20 > len(pkt): continue
                ip_hdr_len = (pkt[ip_start] & 0x0F) * 4
                if pkt[ip_start + 9] != 6: continue

                tcp_start = ip_start + ip_hdr_len
                if tcp_start + 20 > len(pkt): continue
                sp = struct.unpack('>H', pkt[tcp_start:tcp_start+2])[0]
                dp = struct.unpack('>H', pkt[tcp_start+2:tcp_start+4])[0]
                tcp_hdr_len = ((pkt[tcp_start + 12] >> 4) & 0xF) * 4
                payload = pkt[tcp_start + tcp_hdr_len:]
                if not payload: continue

                raw_packets.append((ts_sec, ts_usec, sp, dp, payload))

            # Reassemble per-stream, extracting game packets with timestamps
            tcp_streams = {}
            for ts_sec, ts_usec, sp, dp, payload in raw_packets:
                key = (sp, dp)
                if key not in tcp_streams:
                    tcp_streams[key] = {'buf': bytearray(), 'ts_list': []}
                start_off = len(tcp_streams[key]['buf'])
                tcp_streams[key]['buf'] += payload
                tcp_streams[key]['ts_list'].append((start_off, ts_sec, ts_usec))

            for (sp, dp), stream in tcp_streams.items():
                buf = stream['buf']
                ts_list = stream['ts_list']
                pos = 0
                while pos + 4 <= len(buf):
                    pkt_len = struct.unpack('<H', buf[pos:pos+2])[0]
                    opcode = struct.unpack('<H', buf[pos+2:pos+4])[0]
                    if pkt_len < 4 or pkt_len > 65000:
                        pos += 1; continue
                    if pos + pkt_len > len(buf): break
                    payload_data = bytes(buf[pos+4:pos+pkt_len])
                    # Find approximate timestamp
                    ts = 0
                    for off, ts_s, ts_u in ts_list:
                        if off <= pos:
                            ts = ts_s + ts_u / 1e6
                    ordered.append((ts, opcode, payload_data, sp, dp))
                    pos += pkt_len
    except:
        pass
    ordered.sort(key=lambda x: x[0])
    return ordered


# ─── Load all PCAPs ───
pcaps = sorted(glob.glob(os.path.join(PCAP_DIR, "*.pcap")) +
               glob.glob(os.path.join(PCAP_DIR, "codex_lab", "*.pcap")))

all_pkts = []
all_ordered = []
for p_file in pcaps:
    pkts = read_all_packets(p_file)
    all_pkts.extend(pkts)
    ordered = read_all_packets_ordered(p_file)
    all_ordered.extend(ordered)

all_ordered.sort(key=lambda x: x[0])

print(f"Loaded {len(pcaps)} PCAPs, {len(all_pkts)} packets, {len(all_ordered)} ordered")

out = []
def p(msg=""):
    out.append(msg)
    try: print(msg)
    except: print(msg.encode('ascii','replace').decode())

def hexdump(data, max_bytes=64):
    """Short hex dump."""
    h = data[:max_bytes].hex()
    return ' '.join(h[i:i+2] for i in range(0, len(h), 2))

def try_ascii(data):
    """Extract printable ASCII."""
    return ''.join(chr(b) if 32 <= b < 127 else '.' for b in data)

# Known opcode names from discoveries
OPCODE_NAMES = {
    0x0037: "LOGIN_ACK/ERROR?",
    0x0038: "CASTLE_DATA",
    0x0039: "UNKNOWN_0039",
    0x006F: "MARCH_SYNC?",
    0x0064: "ITEM_INFO",
    0x0065: "ITEM_USE",
    0x0071: "MARCH_STATE",
    0x00B8: "MARCH_ACK?",
    0x0111: "CITY_BUFF_USE",
    0x026D: "CHAT_MSG",
    0x0284: "SIGN_REQUEST",
    0x028F: "ONLINE_REWARD",
    0x0292: "RANDOM_ONLINE_REWARD",
    0x0312: "EVERYDAY_GIFT",
    0x0323: "HERO_SOLDIER_RECRUIT",
    0x033E: "REQUEST_MONSTER_POS",
    0x062C: "RECEIVE_REWARD",
    0x0CE8: "START_MARCH_NEW",
    0x0CE9: "RECALL_MARCH_NEW?",
    0x0CEB: "ENABLE_VIEW",
    0x0CED: "TRAIN",
    0x0CEE: "RESEARCH",
    0x0CEF: "BUILD",
    0x1ACD: "ALLIANCE_HELP",
    0x1B8B: "PASSWORD_CHECK",
}

# ═══════════════════════════════════════════════════════════════
# SECTION 1: March-related server responses
# ═══════════════════════════════════════════════════════════════
p("=" * 70)
p("SECTION 1: MARCH-RELATED SERVER RESPONSES")
p("=" * 70)

MARCH_OPCODES = [0x0071, 0x006F, 0x00B8, 0x0037, 0x0CE9, 0x0CE8]
for target_op in MARCH_OPCODES:
    hits = [(op, pl, sp, dp, pos) for op, pl, sp, dp, pos in all_pkts if op == target_op]
    name = OPCODE_NAMES.get(target_op, "UNKNOWN")
    p(f"\n--- Opcode 0x{target_op:04X} ({name}) --- {len(hits)} packets ---")
    for i, (op, pl, sp, dp, pos) in enumerate(hits[:15]):
        direction = "S->C" if sp in (5997, 6001, 6002, 6003, 6004, 6005, 6006, 6007, 6008, 6009, 6010) or sp > 10000 else "C->S"
        # Heuristic: server ports are typically the well-known game ports or ephemeral high ports
        # Actually, server sends FROM game port. Client sends TO game port.
        if dp in range(5990, 6100) or dp in range(22000, 23000):
            direction = "C->S"
        elif sp in range(5990, 6100) or sp in range(22000, 23000):
            direction = "S->C"
        p(f"  [{i+1:2d}] {direction} len={len(pl):4d} ports={sp}->{dp}")
        p(f"       hex: {hexdump(pl, 48)}")
        if len(pl) >= 2:
            vals = []
            for off in range(0, min(16, len(pl)), 2):
                if off + 2 <= len(pl):
                    vals.append(f"u16@{off}=0x{struct.unpack('<H', pl[off:off+2])[0]:04X}")
            p(f"       u16s: {', '.join(vals)}")
        if len(pl) >= 4:
            vals = []
            for off in range(0, min(16, len(pl)), 4):
                if off + 4 <= len(pl):
                    vals.append(f"u32@{off}=0x{struct.unpack('<I', pl[off:off+4])[0]:08X}")
            p(f"       u32s: {', '.join(vals)}")

# Find what opcodes appear right after 0x0CE8 in chronological order
p(f"\n--- Opcodes appearing within 5 packets after 0x0CE8 (START_MARCH_NEW) ---")
for idx, (ts, op, pl, sp, dp) in enumerate(all_ordered):
    if op == 0x0CE8:
        p(f"\n  0x0CE8 at ts={ts:.3f} ports={sp}->{dp} len={len(pl)}")
        p(f"    payload: {hexdump(pl, 48)}")
        # Show next 10 packets
        for j in range(1, min(11, len(all_ordered) - idx)):
            ts2, op2, pl2, sp2, dp2 = all_ordered[idx + j]
            name2 = OPCODE_NAMES.get(op2, "")
            p(f"    +{j}: 0x{op2:04X} ({name2:20s}) ts={ts2:.3f} len={len(pl2):4d} {sp2}->{dp2} | {hexdump(pl2, 24)}")


# ═══════════════════════════════════════════════════════════════
# SECTION 2: CASTLE_DATA (0x0038) TLV decode
# ═══════════════════════════════════════════════════════════════
p(f"\n\n{'=' * 70}")
p("SECTION 2: CASTLE_DATA (0x0038) TLV DECODE")
p("=" * 70)

castle_packets = [(op, pl, sp, dp, pos) for op, pl, sp, dp, pos in all_pkts if op == 0x0038]
p(f"\nFound {len(castle_packets)} CASTLE_DATA (0x0038) packets")

for pkt_i, (op, pl, sp, dp, pos) in enumerate(castle_packets[:5]):
    p(f"\n--- 0x0038 packet #{pkt_i+1}, len={len(pl)}, ports={sp}->{dp} ---")
    p(f"  First 64 bytes: {hexdump(pl, 64)}")
    if len(pl) < 4:
        p("  Too short"); continue

    # Try multiple TLV formats
    p(f"\n  --- TLV Format A: u16 count, then (u16 field_id + u64 value = 10 bytes each) ---")
    if len(pl) >= 2:
        count_a = struct.unpack('<H', pl[0:2])[0]
        expected_len_a = 2 + count_a * 10
        p(f"  count={count_a}, expected_total={expected_len_a}, actual={len(pl)}")
        if abs(expected_len_a - len(pl)) <= 10 and count_a < 500:
            off = 2
            fields_a = {}
            for i in range(count_a):
                if off + 10 > len(pl): break
                fid = struct.unpack('<H', pl[off:off+2])[0]
                val = struct.unpack('<Q', pl[off+2:off+10])[0]
                fields_a[fid] = val
                off += 10
            p(f"  Parsed {len(fields_a)} fields:")
            for fid in sorted(fields_a.keys())[:60]:
                val = fields_a[fid]
                note = ""
                if fid == 0x4F: note = " *** SERVER_KEY ***"
                elif fid == 0x01: note = " (player_id?)"
                elif fid == 0x02: note = " (level?)"
                elif fid == 0x03: note = " (vip_level?)"
                elif fid == 0x09: note = " (power?)"
                p(f"    field 0x{fid:04X} ({fid:4d}) = {val:>20d}  (0x{val:016X}){note}")
            if len(fields_a) > 60:
                p(f"    ... and {len(fields_a)-60} more fields")
        else:
            p(f"  Mismatch: count*10+2={expected_len_a} vs payload={len(pl)}")

    p(f"\n  --- TLV Format B: u8 count, then (u8 field_id + u64 value = 9 bytes each) ---")
    if len(pl) >= 1:
        count_b = pl[0]
        expected_len_b = 1 + count_b * 9
        p(f"  count={count_b}, expected_total={expected_len_b}, actual={len(pl)}")
        if abs(expected_len_b - len(pl)) <= 10 and count_b < 200:
            off = 1
            fields_b = {}
            for i in range(count_b):
                if off + 9 > len(pl): break
                fid = pl[off]
                val = struct.unpack('<Q', pl[off+1:off+9])[0]
                fields_b[fid] = val
                off += 9
            p(f"  Parsed {len(fields_b)} fields:")
            for fid in sorted(fields_b.keys())[:30]:
                val = fields_b[fid]
                p(f"    field 0x{fid:02X} ({fid:3d}) = {val:>20d}  (0x{val:016X})")

    p(f"\n  --- TLV Format C: u16 count, then (u8 field_id + u8 type + variable_value) ---")
    if len(pl) >= 2:
        count_c = struct.unpack('<H', pl[0:2])[0]
        if count_c < 500:
            off = 2
            fields_c = {}
            ok = True
            for i in range(count_c):
                if off + 2 > len(pl): ok = False; break
                fid = pl[off]
                ftype = pl[off+1]
                off += 2
                if ftype == 0: # u8
                    if off + 1 > len(pl): ok = False; break
                    fields_c[fid] = ('u8', pl[off])
                    off += 1
                elif ftype == 1: # u16
                    if off + 2 > len(pl): ok = False; break
                    fields_c[fid] = ('u16', struct.unpack('<H', pl[off:off+2])[0])
                    off += 2
                elif ftype == 2: # u32
                    if off + 4 > len(pl): ok = False; break
                    fields_c[fid] = ('u32', struct.unpack('<I', pl[off:off+4])[0])
                    off += 4
                elif ftype == 3 or ftype == 4: # u64
                    if off + 8 > len(pl): ok = False; break
                    fields_c[fid] = ('u64', struct.unpack('<Q', pl[off:off+8])[0])
                    off += 8
                else:
                    ok = False; break
            if ok and len(fields_c) > 5:
                p(f"  count={count_c}, parsed OK with {len(fields_c)} fields, consumed {off}/{len(pl)} bytes")
                for fid in sorted(fields_c.keys())[:30]:
                    t, v = fields_c[fid]
                    p(f"    field 0x{fid:02X} ({fid:3d}) [{t}] = {v}  (0x{v:X})")
            else:
                p(f"  Format C did not parse cleanly (ok={ok}, fields={len(fields_c)})")

    p(f"\n  --- TLV Format D: u16 count, then (u16 field_id + u32 value = 6 bytes each) ---")
    if len(pl) >= 2:
        count_d = struct.unpack('<H', pl[0:2])[0]
        expected_len_d = 2 + count_d * 6
        p(f"  count={count_d}, expected_total={expected_len_d}, actual={len(pl)}")
        if abs(expected_len_d - len(pl)) <= 6 and count_d < 500:
            off = 2
            fields_d = {}
            for i in range(count_d):
                if off + 6 > len(pl): break
                fid = struct.unpack('<H', pl[off:off+2])[0]
                val = struct.unpack('<I', pl[off+2:off+6])[0]
                fields_d[fid] = val
                off += 6
            p(f"  Parsed {len(fields_d)} fields:")
            for fid in sorted(fields_d.keys())[:30]:
                val = fields_d[fid]
                note = ""
                if fid == 0x4F: note = " *** SERVER_KEY ***"
                p(f"    field 0x{fid:04X} ({fid:4d}) = {val:>12d}  (0x{val:08X}){note}")

    # Also try Format E: raw scan for 0x4F pattern
    p(f"\n  --- Scanning for field 0x4F (server_key) at all offsets ---")
    for off in range(len(pl) - 10):
        fid_u16 = struct.unpack('<H', pl[off:off+2])[0]
        if fid_u16 == 0x004F:
            if off + 10 <= len(pl):
                val8 = struct.unpack('<Q', pl[off+2:off+10])[0]
                val4 = struct.unpack('<I', pl[off+2:off+6])[0]
                p(f"    Found 0x004F at offset {off}: u64={val8} (0x{val8:016X}), u32={val4} (0x{val4:08X})")
            if off + 6 <= len(pl):
                val4 = struct.unpack('<I', pl[off+2:off+6])[0]
                p(f"      as u32 = {val4} (0x{val4:08X})")
        # Also check u8 = 0x4F
        if pl[off] == 0x4F and off + 9 <= len(pl):
            val8 = struct.unpack('<Q', pl[off+1:off+9])[0]
            if val8 < 0xFFFFFFFF and val8 > 0:  # reasonable range
                p(f"    Found byte 0x4F at offset {off}: next_u64={val8} (0x{val8:016X})")


# ═══════════════════════════════════════════════════════════════
# SECTION 3: Decode 0x026D chat messages
# ═══════════════════════════════════════════════════════════════
p(f"\n\n{'=' * 70}")
p("SECTION 3: DECODE 0x026D CHAT MESSAGES")
p("=" * 70)

chat_pkts = [(op, pl, sp, dp, pos) for op, pl, sp, dp, pos in all_pkts if op == 0x026D]
p(f"\nFound {len(chat_pkts)} chat (0x026D) packets")

# Group by payload length
len_dist = collections.Counter(len(pl) for op, pl, sp, dp, pos in chat_pkts)
p(f"\nPayload length distribution:")
for sz, cnt in sorted(len_dist.items(), key=lambda x: -x[1])[:20]:
    p(f"  len={sz:4d}: {cnt} packets")

p(f"\nDetailed decode (first 30):")
for i, (op, pl, sp, dp, pos) in enumerate(chat_pkts[:30]):
    p(f"\n  [{i+1:2d}] len={len(pl):4d} ports={sp}->{dp}")
    p(f"    hex: {hexdump(pl, 64)}")

    # Try decode structures
    if len(pl) >= 2:
        ch_type = struct.unpack('<H', pl[0:2])[0]
        p(f"    u16[0]=0x{ch_type:04X} (channel/type?)")

    # Look for length-prefixed strings
    off = 2
    while off < len(pl) and off < 50:
        # u16 length prefix + string
        if off + 2 <= len(pl):
            slen = struct.unpack('<H', pl[off:off+2])[0]
            if 1 <= slen <= 200 and off + 2 + slen <= len(pl):
                s = pl[off+2:off+2+slen]
                ascii_s = try_ascii(s)
                try:
                    utf8_s = s.decode('utf-8', errors='replace')
                except:
                    utf8_s = ascii_s
                if sum(1 for c in ascii_s if c != '.') > len(s) * 0.3:
                    p(f"    str@{off} (len={slen}): {utf8_s[:60]}")
                    off += 2 + slen
                    continue
        # u8 length prefix
        if off < len(pl):
            slen = pl[off]
            if 1 <= slen <= 200 and off + 1 + slen <= len(pl):
                s = pl[off+1:off+1+slen]
                ascii_s = try_ascii(s)
                try:
                    utf8_s = s.decode('utf-8', errors='replace')
                except:
                    utf8_s = ascii_s
                if sum(1 for c in ascii_s if c != '.') > len(s) * 0.4:
                    p(f"    str@{off} (u8 len={slen}): {utf8_s[:60]}")
                    off += 1 + slen
                    continue
        off += 1

    # Try to find UTF-8 text anywhere
    try:
        full_text = pl.decode('utf-8', errors='replace')
        printable = ''.join(c if c.isprintable() or c in '\n\r\t' else '.' for c in full_text)
        if sum(1 for c in printable if c != '.') > 5:
            p(f"    raw_utf8: {printable[:80]}")
    except:
        pass


# ═══════════════════════════════════════════════════════════════
# SECTION 4: Top 30 most frequent opcodes with format analysis
# ═══════════════════════════════════════════════════════════════
p(f"\n\n{'=' * 70}")
p("SECTION 4: TOP 30 MOST FREQUENT OPCODES")
p("=" * 70)

opcode_counter = collections.Counter()
opcode_payloads = collections.defaultdict(list)
opcode_ports = collections.defaultdict(set)

for op, pl, sp, dp, pos in all_pkts:
    opcode_counter[op] += 1
    if len(opcode_payloads[op]) < 10:
        opcode_payloads[op].append(pl)
    opcode_ports[op].add((sp, dp))

p(f"\nTotal unique opcodes: {len(opcode_counter)}")
p(f"\n{'Opcode':>8s}  {'Name':25s}  {'Count':>6s}  {'MinLen':>6s}  {'MaxLen':>6s}  {'AvgLen':>6s}  Direction")
p("-" * 95)

for op, count in opcode_counter.most_common(50):
    name = OPCODE_NAMES.get(op, "")
    samples = opcode_payloads[op]
    lengths = [len(s) for s in samples]
    min_l = min(lengths) if lengths else 0
    max_l = max(lengths) if lengths else 0
    avg_l = sum(lengths) / len(lengths) if lengths else 0

    # Determine direction from port patterns
    ports = opcode_ports[op]
    directions = set()
    for sp, dp in ports:
        if dp in range(5990, 6100) or dp in range(22000, 23000):
            directions.add("C->S")
        elif sp in range(5990, 6100) or sp in range(22000, 23000):
            directions.add("S->C")
        elif dp > 30000:
            directions.add("S->C")
        elif sp > 30000:
            directions.add("C->S")
        else:
            directions.add("???")
    dir_str = "/".join(sorted(directions))

    p(f"  0x{op:04X}  {name:25s}  {count:6d}  {min_l:6d}  {max_l:6d}  {avg_l:6.0f}  {dir_str}")

# Detailed analysis of top 30
p(f"\n\n--- Detailed format analysis for top opcodes ---")
for op, count in opcode_counter.most_common(30):
    name = OPCODE_NAMES.get(op, "")
    samples = opcode_payloads[op]
    if not samples: continue

    p(f"\n  0x{op:04X} ({name}) - {count} packets")

    # Length distribution
    all_lens = [len(s) for s in samples]
    len_set = sorted(set(all_lens))
    if len(len_set) == 1:
        p(f"    Fixed length: {len_set[0]}")
    else:
        p(f"    Lengths: {len_set[:10]}")

    # Show first 3 samples
    for si, sample in enumerate(samples[:3]):
        p(f"    sample[{si}] len={len(sample):4d}: {hexdump(sample, 32)}")
        # Decode first few fields
        vals = []
        if len(sample) >= 1: vals.append(f"u8[0]={sample[0]}")
        if len(sample) >= 2: vals.append(f"u16[0]=0x{struct.unpack('<H', sample[0:2])[0]:04X}")
        if len(sample) >= 4: vals.append(f"u32[0]=0x{struct.unpack('<I', sample[0:4])[0]:08X}")
        if len(sample) >= 8: vals.append(f"u64[0]=0x{struct.unpack('<Q', sample[0:8])[0]:016X}")
        p(f"      {', '.join(vals)}")

    # Check if payload is always same (heartbeat-like)
    if len(set(s.hex() for s in samples)) == 1 and samples:
        p(f"    ** All payloads identical (heartbeat/keepalive?) **")

    # Check for string content
    for sample in samples[:1]:
        try:
            txt = sample.decode('utf-8', errors='replace')
            printable = ''.join(c if c.isprintable() else '.' for c in txt)
            if sum(1 for c in printable if c != '.') > 5:
                p(f"    text: {printable[:60]}")
        except:
            pass


# ═══════════════════════════════════════════════════════════════
# SECTION 5: Extra - Opcodes in range 0x0060-0x00C0 (march/battle area)
# ═══════════════════════════════════════════════════════════════
p(f"\n\n{'=' * 70}")
p("SECTION 5: ALL OPCODES IN 0x0060-0x00C0 RANGE (MARCH/BATTLE)")
p("=" * 70)

for op in sorted(opcode_counter.keys()):
    if 0x0060 <= op <= 0x00C0:
        count = opcode_counter[op]
        name = OPCODE_NAMES.get(op, "")
        samples = opcode_payloads[op]
        p(f"\n  0x{op:04X} ({name:20s}) count={count}")
        for si, sample in enumerate(samples[:3]):
            p(f"    [{si}] len={len(sample):4d}: {hexdump(sample, 48)}")
            if len(sample) >= 4:
                p(f"         u32[0]=0x{struct.unpack('<I', sample[0:4])[0]:08X}")


# ═══════════════════════════════════════════════════════════════
# SECTION 6: TCP stream analysis - what port pairs exist?
# ═══════════════════════════════════════════════════════════════
p(f"\n\n{'=' * 70}")
p("SECTION 6: TCP STREAM PORT ANALYSIS")
p("=" * 70)

port_pairs = collections.Counter()
for op, pl, sp, dp, pos in all_pkts:
    port_pairs[(sp, dp)] += 1

p(f"\nAll port pairs (packet counts):")
for (sp, dp), cnt in sorted(port_pairs.items(), key=lambda x: -x[1])[:30]:
    p(f"  {sp:>6d} -> {dp:>6d}: {cnt:5d} packets")


# ═══════════════════════════════════════════════════════════════
# Write markdown report
# ═══════════════════════════════════════════════════════════════
os.makedirs(OUT_DIR, exist_ok=True)
md_path = os.path.join(OUT_DIR, "march_castle_decoded.md")
with open(md_path, 'w', encoding='utf-8') as f:
    f.write("# March, Castle, Chat & Opcode Analysis\n\n")
    f.write("Generated by `41_march_and_castle_decode.py`\n\n")
    f.write("```\n")
    f.write('\n'.join(out))
    f.write("\n```\n")

print(f"\n\nResults written to {md_path}")
print("DONE.")

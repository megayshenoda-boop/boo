#!/usr/bin/env python3
"""
47_packet_flow_analysis.py - Complete packet flow analysis across all PCAPs
==========================================================================
Analyzes session lifecycle, march flow, heartbeat patterns, request/response pairs,
session initialization, and frequency statistics.
"""
import struct, os, glob, sys, collections, statistics
from pathlib import Path

PCAP_DIR = r"D:\CascadeProjects"

sys.path.insert(0, r'D:\CascadeProjects\analysis\findings')
from cmsg_opcodes import CMSG_OPCODES
NAMES = CMSG_OPCODES  # {0x000B: 'CMSG_LOGIN', ...}

out_lines = []
def p(msg=""):
    out_lines.append(str(msg))
    try:
        print(msg)
    except:
        print(str(msg).encode('ascii', 'replace').decode())

# Game server ports
GAME_PORTS = set(range(5990, 5999)) | set(range(7001, 7011)) | {7000, 5997}

def opname(op):
    n = NAMES.get(op, '')
    if n:
        return n.replace('CMSG_', '')
    return ''

def read_pcap_ordered(filepath):
    """Read ALL game packets from PCAP in timestamp order, handling link types."""
    events = []
    try:
        with open(filepath, 'rb') as f:
            magic_raw = f.read(4)
            if len(magic_raw) < 4:
                return events
            magic = struct.unpack('<I', magic_raw)[0]
            if magic == 0xa1b2c3d4:
                endian = '<'
            elif magic == 0xd4c3b2a1:
                endian = '>'
            else:
                return events

            rest_hdr = f.read(20)
            if len(rest_hdr) < 20:
                return events
            network = struct.unpack(endian + 'I', rest_hdr[16:20])[0]

            # Per-stream TCP reassembly buffers, keyed by (src_port, dst_port)
            stream_bufs = {}
            stream_timestamps = {}

            while True:
                pkt_hdr = f.read(16)
                if len(pkt_hdr) < 16:
                    break
                ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', pkt_hdr)
                pkt_data = f.read(incl_len)
                if len(pkt_data) < incl_len:
                    break

                ts = ts_sec + ts_usec / 1e6

                # Link type -> IP offset
                if network == 101:  # RAW_IP
                    ip_start = 0
                elif network == 113:  # Linux SLL
                    ip_start = 16
                elif network == 1:  # Ethernet
                    if len(pkt_data) < 14:
                        continue
                    eth_type = struct.unpack('>H', pkt_data[12:14])[0]
                    if eth_type != 0x0800:
                        continue
                    ip_start = 14
                else:
                    continue

                if ip_start + 20 > len(pkt_data):
                    continue

                # IP header
                ip_ver = (pkt_data[ip_start] >> 4) & 0xF
                if ip_ver != 4:
                    continue
                ip_hdr_len = (pkt_data[ip_start] & 0x0F) * 4
                ip_proto = pkt_data[ip_start + 9]
                if ip_proto != 6:  # TCP only
                    continue

                # TCP header
                tcp_start = ip_start + ip_hdr_len
                if tcp_start + 20 > len(pkt_data):
                    continue
                src_port = struct.unpack('>H', pkt_data[tcp_start:tcp_start+2])[0]
                dst_port = struct.unpack('>H', pkt_data[tcp_start+2:tcp_start+4])[0]
                tcp_hdr_len = ((pkt_data[tcp_start + 12] >> 4) & 0xF) * 4
                tcp_payload = pkt_data[tcp_start + tcp_hdr_len:]

                if not tcp_payload:
                    continue

                # Only process streams involving game ports
                is_c2s = dst_port in GAME_PORTS
                is_s2c = src_port in GAME_PORTS
                if not is_c2s and not is_s2c:
                    continue

                key = (src_port, dst_port)
                direction = 'C2S' if is_c2s else 'S2C'

                if key not in stream_bufs:
                    stream_bufs[key] = bytearray()
                stream_bufs[key].extend(tcp_payload)
                stream_timestamps[key] = ts

                # Parse complete game packets from buffer
                buf = stream_bufs[key]
                while len(buf) >= 4:
                    pkt_len = struct.unpack('<H', buf[0:2])[0]
                    if pkt_len < 4 or pkt_len > 65535:
                        buf = buf[1:]
                        stream_bufs[key] = buf
                        continue
                    if len(buf) < pkt_len:
                        break
                    opcode = struct.unpack('<H', buf[2:4])[0]
                    raw = bytes(buf[:pkt_len])
                    events.append((ts, direction, opcode, raw, src_port, dst_port))
                    buf = buf[pkt_len:]
                stream_bufs[key] = buf

    except Exception as e:
        pass

    return sorted(events, key=lambda x: x[0])


# ============================================================
# Collect all PCAP files
# ============================================================
pcap_files = []
for pattern in [
    os.path.join(PCAP_DIR, "*.pcap"),
    os.path.join(PCAP_DIR, "codex_lab", "*.pcap"),
    os.path.join(PCAP_DIR, "codex_lab", "rebel_attack", "*.pcap"),
    os.path.join(PCAP_DIR, "config-decryptor", "*.pcap"),
]:
    pcap_files.extend(glob.glob(pattern))

# Deduplicate and sort by size (largest first for session flow analysis)
pcap_files = sorted(set(pcap_files), key=lambda f: os.path.getsize(f), reverse=True)
p(f"Found {len(pcap_files)} PCAP files total")

# ============================================================
# Parse ALL PCAPs
# ============================================================
all_pcap_events = {}  # path -> events list
total_events = 0
largest_pcap = None
largest_events = []

for i, fpath in enumerate(pcap_files):
    events = read_pcap_ordered(fpath)
    if events:
        all_pcap_events[fpath] = events
        total_events += len(events)
        if not largest_events or len(events) > len(largest_events):
            largest_events = events
            largest_pcap = fpath
    if (i + 1) % 20 == 0:
        p(f"  Parsed {i+1}/{len(pcap_files)} PCAPs...")

p(f"Parsed {len(all_pcap_events)} PCAPs with game packets, {total_events} total events")
if largest_pcap:
    p(f"Largest PCAP: {os.path.basename(largest_pcap)} ({len(largest_events)} events, {os.path.getsize(largest_pcap)} bytes)")

# ============================================================
# TASK 1: Session flow - first 200 packets of largest PCAP
# ============================================================
p("\n" + "=" * 120)
p("TASK 1: SESSION FLOW (first 200 packets of largest PCAP)")
p("=" * 120)

if largest_events:
    base_ts = largest_events[0][0]
    p(f"\nPCAP: {os.path.basename(largest_pcap)}")
    p(f"{'#':>4} {'Time':>10} {'Dir':>3} {'Opcode':>8} {'Name':<45} {'Size':>5} {'First 16 bytes payload'}")
    p("-" * 120)
    for idx, (ts, d, op, raw, sp, dp) in enumerate(largest_events[:200]):
        t = ts - base_ts
        payload = raw[4:]  # skip len+opcode
        first16 = payload[:16].hex() if payload else ''
        name = opname(op)
        p(f"{idx:4d} {t:10.3f} {d:>3} 0x{op:04X}   {name:<45} {len(raw):5d} {first16}")

# ============================================================
# TASK 2: March flow - context around 0x0CE8
# ============================================================
p("\n" + "=" * 120)
p("TASK 2: MARCH FLOW (20 packets before/after 0x0CE8)")
p("=" * 120)

march_found = 0
for fpath, events in all_pcap_events.items():
    march_indices = [i for i, e in enumerate(events) if e[2] == 0x0CE8]
    if not march_indices:
        continue

    p(f"\n--- {os.path.basename(fpath)} ({len(march_indices)} march packets) ---")
    base_ts = events[0][0]

    for mi in march_indices[:5]:  # max 5 per PCAP
        march_found += 1
        start = max(0, mi - 20)
        end = min(len(events), mi + 21)
        p(f"\n  March #{march_found} at index {mi}:")
        p(f"  {'#':>4} {'Time':>10} {'Dir':>3} {'Opcode':>8} {'Name':<40} {'Size':>5} {'First 16 bytes'}")
        p("  " + "-" * 110)
        for idx in range(start, end):
            ts, d, op, raw, sp, dp = events[idx]
            t = ts - base_ts
            marker = " >>>" if idx == mi else "    "
            payload = raw[4:]
            first16 = payload[:16].hex() if payload else ''
            name = opname(op)
            p(f"  {idx:4d} {t:10.3f} {d:>3} 0x{op:04X}   {name:<40} {len(raw):5d} {first16}{marker}")

if march_found == 0:
    p("  No 0x0CE8 (START_MARCH_NEW) packets found in any PCAP.")

# ============================================================
# TASK 3: Gather flow - trace gather-related opcodes
# ============================================================
p("\n" + "=" * 120)
p("TASK 3: GATHER FLOW")
p("=" * 120)

gather_opcodes = {
    0x033E: 'REQUEST_MONSTER_POS',
    0x033F: 'RESPONSE_MONSTER_POS',
    0x0CE8: 'START_MARCH_NEW',
    0x0CEB: 'ENABLE_VIEW',
    0x006E: 'VIEW_TILE',
    0x0076: 'TILE_INFO',
    0x0077: 'RESOURCE_TILE_INFO',
    0x0071: 'MARCH_STATE',
    0x076C: 'MARCH_START_NOTIFY',
    0x0767: 'MARCH_DETAIL',
    0x0769: 'MARCH_RETURN',
}

for fpath, events in all_pcap_events.items():
    gather_events = [(i, e) for i, e in enumerate(events) if e[2] in gather_opcodes]
    if not gather_events:
        continue
    base_ts = events[0][0]
    p(f"\n--- {os.path.basename(fpath)} ({len(gather_events)} gather-related packets) ---")
    p(f"  {'#':>4} {'Time':>10} {'Dir':>3} {'Opcode':>8} {'Name':<35} {'Size':>5} {'First 16 bytes'}")
    p("  " + "-" * 100)
    for idx, (ts, d, op, raw, sp, dp) in gather_events[:60]:
        t = ts - base_ts
        payload = raw[4:]
        first16 = payload[:16].hex() if payload else ''
        gname = gather_opcodes.get(op, opname(op))
        p(f"  {idx:4d} {t:10.3f} {d:>3} 0x{op:04X}   {gname:<35} {len(raw):5d} {first16}")

# ============================================================
# TASK 4: Heartbeat pattern (0x0042)
# ============================================================
p("\n" + "=" * 120)
p("TASK 4: HEARTBEAT PATTERN (0x0042)")
p("=" * 120)

heartbeat_op = 0x0042
total_hb = 0
all_intervals = []

for fpath, events in all_pcap_events.items():
    hb_events = [(ts, d) for ts, d, op, raw, sp, dp in events if op == heartbeat_op]
    if len(hb_events) < 2:
        continue

    c2s_hb = [ts for ts, d in hb_events if d == 'C2S']
    s2c_hb = [ts for ts, d in hb_events if d == 'S2C']

    intervals = [c2s_hb[i+1] - c2s_hb[i] for i in range(len(c2s_hb)-1)] if len(c2s_hb) > 1 else []
    all_intervals.extend(intervals)
    total_hb += len(hb_events)

    if intervals:
        p(f"\n  {os.path.basename(fpath)}:")
        p(f"    Client heartbeats: {len(c2s_hb)}, Server heartbeats: {len(s2c_hb)}")
        p(f"    Interval: min={min(intervals):.2f}s, max={max(intervals):.2f}s, avg={statistics.mean(intervals):.2f}s")
        if len(intervals) >= 3:
            p(f"    Median interval: {statistics.median(intervals):.2f}s")
        p(f"    Server responds to each? {len(s2c_hb)} responses for {len(c2s_hb)} requests ({len(s2c_hb)/max(len(c2s_hb),1)*100:.0f}%)")

# Also check 0x0043 (SYN_SERVER_TIME) as potential heartbeat
alt_hb_ops = {0x0042: 'HEARTBEAT(0x0042)', 0x0043: 'SYN_SERVER_TIME(0x0043)', 0x0047: 'TIME_REFRESH(0x0047)'}
p(f"\n  -- Alternative heartbeat/keepalive opcodes across ALL PCAPs --")
for op, name in alt_hb_ops.items():
    cnt_c2s = sum(1 for evts in all_pcap_events.values() for ts,d,o,r,sp,dp in evts if o == op and d == 'C2S')
    cnt_s2c = sum(1 for evts in all_pcap_events.values() for ts,d,o,r,sp,dp in evts if o == op and d == 'S2C')
    p(f"    {name}: C2S={cnt_c2s}, S2C={cnt_s2c}")

if all_intervals:
    p(f"\n  Global heartbeat stats ({len(all_intervals)} intervals):")
    p(f"    Mean: {statistics.mean(all_intervals):.2f}s, Median: {statistics.median(all_intervals):.2f}s")
    p(f"    Min: {min(all_intervals):.2f}s, Max: {max(all_intervals):.2f}s")
else:
    p("  No 0x0042 heartbeat intervals found. Checking other timing patterns...")
    # Find the most frequent opcode pair to detect heartbeat-like behavior
    for fpath, events in list(all_pcap_events.items())[:3]:
        if len(events) < 50:
            continue
        c2s_times = collections.defaultdict(list)
        for ts, d, op, raw, sp, dp in events:
            if d == 'C2S':
                c2s_times[op].append(ts)
        for op, times in sorted(c2s_times.items(), key=lambda x: -len(x[1])):
            if len(times) < 5:
                break
            intervals = [times[i+1] - times[i] for i in range(len(times)-1)]
            avg = statistics.mean(intervals)
            if 1.0 < avg < 120.0 and len(times) >= 5:
                p(f"    Periodic C2S opcode 0x{op:04X} ({opname(op)}): {len(times)} packets, avg interval={avg:.2f}s in {os.path.basename(fpath)}")

# ============================================================
# TASK 5: Request->Response pairs (consecutive C2S -> S2C)
# ============================================================
p("\n" + "=" * 120)
p("TASK 5: REQUEST -> RESPONSE PAIRS")
p("=" * 120)

pair_counts = collections.Counter()  # (c2s_op, s2c_op) -> count

for fpath, events in all_pcap_events.items():
    for i in range(len(events) - 1):
        ts1, d1, op1, raw1, sp1, dp1 = events[i]
        ts2, d2, op2, raw2, sp2, dp2 = events[i + 1]
        if d1 == 'C2S' and d2 == 'S2C':
            pair_counts[(op1, op2)] += 1

p(f"\nTop 60 request->response pairs (by frequency):")
p(f"  {'Count':>5}  {'Request':>8} {'Req Name':<40} -> {'Response':>8} {'Resp Name':<40}")
p("  " + "-" * 130)
for (req_op, resp_op), cnt in pair_counts.most_common(60):
    req_name = opname(req_op)
    resp_name = opname(resp_op)
    p(f"  {cnt:5d}  0x{req_op:04X}   {req_name:<40} -> 0x{resp_op:04X}   {resp_name:<40}")

# Also find likely request/response pairs where opcode differs by 1
p(f"\n  Request/Response pairs where response = request + 1:")
p(f"  {'Count':>5}  {'Request':>8} {'Req Name':<40} -> {'Response':>8} {'Resp Name':<40}")
p("  " + "-" * 130)
for (req_op, resp_op), cnt in pair_counts.most_common(200):
    if resp_op == req_op + 1 and cnt >= 2:
        req_name = opname(req_op)
        resp_name = opname(resp_op)
        p(f"  {cnt:5d}  0x{req_op:04X}   {req_name:<40} -> 0x{resp_op:04X}   {resp_name:<40}")

# ============================================================
# TASK 6: Session initialization (first 50 packets only)
# ============================================================
p("\n" + "=" * 120)
p("TASK 6: SESSION INITIALIZATION (opcodes in first 50 packets)")
p("=" * 120)

init_opcodes = collections.Counter()
all_opcodes = collections.Counter()
session_count = 0

for fpath, events in all_pcap_events.items():
    if len(events) < 20:
        continue
    session_count += 1
    seen_init = set()
    for ts, d, op, raw, sp, dp in events[:50]:
        init_opcodes[(d, op)] += 1
        seen_init.add((d, op))
    for ts, d, op, raw, sp, dp in events:
        all_opcodes[(d, op)] += 1

# Find opcodes that appear MOSTLY in the first 50 packets
p(f"\nAnalyzed {session_count} sessions")
p(f"\nOpcodes that appear predominantly in first 50 packets (>70% of occurrences):")
p(f"  {'Dir':>3} {'Opcode':>8} {'Name':<45} {'Init':>5} {'Total':>6} {'%Init':>6}")
p("  " + "-" * 90)

init_only = []
for (d, op), init_cnt in init_opcodes.most_common():
    total_cnt = all_opcodes.get((d, op), 0)
    if total_cnt > 0:
        pct = init_cnt / total_cnt * 100
        if pct > 70 and init_cnt >= 3:
            init_only.append((d, op, init_cnt, total_cnt, pct))

init_only.sort(key=lambda x: -x[4])
for d, op, init_cnt, total_cnt, pct in init_only:
    name = opname(op)
    p(f"  {d:>3} 0x{op:04X}   {name:<45} {init_cnt:5d} {total_cnt:6d} {pct:5.1f}%")

# Show exact first 30 packets from sessions with most events for init pattern
p(f"\n  Typical session start (first 30 packets from 3 largest sessions):")
sorted_sessions = sorted(all_pcap_events.items(), key=lambda x: -len(x[1]))
for fpath, events in sorted_sessions[:3]:
    p(f"\n  --- {os.path.basename(fpath)} ({len(events)} total) ---")
    base_ts = events[0][0]
    for idx, (ts, d, op, raw, sp, dp) in enumerate(events[:30]):
        t = ts - base_ts
        name = opname(op)
        p(f"    {idx:3d} {t:8.3f}s {d:>3} 0x{op:04X} {name:<40} {len(raw):5d}B")

# ============================================================
# TASK 7: Frequency analysis
# ============================================================
p("\n" + "=" * 120)
p("TASK 7: FREQUENCY ANALYSIS (all opcodes across all PCAPs)")
p("=" * 120)

opcode_stats = collections.defaultdict(lambda: {
    'count': 0, 'sizes': [], 'directions': collections.Counter(),
    'pcap_count': 0
})

for fpath, events in all_pcap_events.items():
    seen_in_pcap = set()
    for ts, d, op, raw, sp, dp in events:
        s = opcode_stats[op]
        s['count'] += 1
        s['sizes'].append(len(raw))
        s['directions'][d] += 1
        seen_in_pcap.add(op)
    for op in seen_in_pcap:
        opcode_stats[op]['pcap_count'] += 1

# Sort by count descending
sorted_ops = sorted(opcode_stats.items(), key=lambda x: -x[1]['count'])

p(f"\n{'Opcode':>8} {'Name':<45} {'Count':>6} {'PCAPs':>5} {'AvgSz':>6} {'MinSz':>6} {'MaxSz':>6} {'C2S':>5} {'S2C':>5} {'Dir':<6}")
p("-" * 145)

for op, s in sorted_ops:
    name = opname(op)
    sizes = s['sizes']
    avg_sz = statistics.mean(sizes) if sizes else 0
    min_sz = min(sizes) if sizes else 0
    max_sz = max(sizes) if sizes else 0
    c2s = s['directions'].get('C2S', 0)
    s2c = s['directions'].get('S2C', 0)
    if c2s > 0 and s2c > 0:
        dirstr = 'BOTH'
    elif c2s > 0:
        dirstr = 'C2S'
    else:
        dirstr = 'S2C'
    p(f"0x{op:04X}   {name:<45} {s['count']:6d} {s['pcap_count']:5d} {avg_sz:6.0f} {min_sz:6d} {max_sz:6d} {c2s:5d} {s2c:5d} {dirstr:<6}")

# Summary statistics
p(f"\n{'='*60}")
p(f"SUMMARY")
p(f"{'='*60}")
p(f"Total unique opcodes: {len(opcode_stats)}")
p(f"Total packets across all PCAPs: {total_events}")
p(f"PCAPs with game data: {len(all_pcap_events)}/{len(pcap_files)}")

c2s_only = [op for op, s in opcode_stats.items() if s['directions'].get('C2S', 0) > 0 and s['directions'].get('S2C', 0) == 0]
s2c_only = [op for op, s in opcode_stats.items() if s['directions'].get('S2C', 0) > 0 and s['directions'].get('C2S', 0) == 0]
both_dir = [op for op, s in opcode_stats.items() if s['directions'].get('C2S', 0) > 0 and s['directions'].get('S2C', 0) > 0]

p(f"Client-only opcodes: {len(c2s_only)}")
p(f"Server-only opcodes: {len(s2c_only)}")
p(f"Both directions: {len(both_dir)}")

# List "both direction" opcodes (unusual - worth investigating)
if both_dir:
    p(f"\nOpcodes seen in BOTH directions (potential shared/reused opcodes):")
    for op in sorted(both_dir):
        s = opcode_stats[op]
        name = opname(op)
        p(f"  0x{op:04X} {name:<40} C2S={s['directions']['C2S']:4d} S2C={s['directions']['S2C']:4d}")

# ============================================================
# Save report
# ============================================================
findings_dir = os.path.join(os.path.dirname(__file__), 'findings')
os.makedirs(findings_dir, exist_ok=True)
report_path = os.path.join(findings_dir, 'packet_flow_analysis.md')
with open(report_path, 'w', encoding='utf-8') as f:
    f.write("# Packet Flow Analysis\n\n")
    f.write("```\n")
    f.write("\n".join(out_lines))
    f.write("\n```\n")

p(f"\nReport saved to: {report_path}")

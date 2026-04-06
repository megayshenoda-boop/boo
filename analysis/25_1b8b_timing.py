#!/usr/bin/env python3
"""
25_1b8b_timing.py - When does 0x1B8B appear in PCAP? C2S vs S2C timing.
Check if server sends a challenge BEFORE client sends password check.
"""
import struct
from pathlib import Path

def read_pcap_ordered(filepath):
    """Read PCAP with timestamps and direction preserved."""
    with open(filepath, 'rb') as f:
        magic = struct.unpack('<I', f.read(4))[0]
        endian = '<' if magic == 0xa1b2c3d4 else '>'
        f.read(20)
        events = []  # (timestamp, direction, raw_bytes)
        c2s_buf = bytearray()
        s2c_buf = bytearray()
        while True:
            hdr = f.read(16)
            if len(hdr) < 16: break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
            d = f.read(incl_len)
            if len(d) < incl_len: break
            if len(d) < 20: continue
            ihl = (d[0] & 0x0F) * 4
            if d[9] != 6: continue
            tcp = d[ihl:]
            if len(tcp) < 20: continue
            sp = struct.unpack('>H', tcp[0:2])[0]
            dp = struct.unpack('>H', tcp[2:4])[0]
            toff = ((tcp[12] >> 4) & 0xF) * 4
            pl = tcp[toff:]
            if not pl: continue
            ts = ts_sec + ts_usec / 1e6
            gp = set(range(5990, 5999)) | set(range(7001, 7011))
            if dp in gp:
                c2s_buf.extend(pl)
                # Try to parse complete packets
                while len(c2s_buf) >= 4:
                    pkt_len = struct.unpack('<H', c2s_buf[0:2])[0]
                    if pkt_len < 4 or pkt_len > 65535: c2s_buf = c2s_buf[1:]; continue
                    if len(c2s_buf) < pkt_len: break
                    opcode = struct.unpack('<H', c2s_buf[2:4])[0]
                    raw = bytes(c2s_buf[:pkt_len])
                    events.append((ts, 'C2S', opcode, raw))
                    c2s_buf = c2s_buf[pkt_len:]
            elif sp in gp:
                s2c_buf.extend(pl)
                while len(s2c_buf) >= 4:
                    pkt_len = struct.unpack('<H', s2c_buf[0:2])[0]
                    if pkt_len < 4 or pkt_len > 65535: s2c_buf = s2c_buf[1:]; continue
                    if len(s2c_buf) < pkt_len: break
                    opcode = struct.unpack('<H', s2c_buf[2:4])[0]
                    raw = bytes(s2c_buf[:pkt_len])
                    events.append((ts, 'S2C', opcode, raw))
                    s2c_buf = s2c_buf[pkt_len:]
    return sorted(events, key=lambda x: x[0])

pcap_dir = Path(r'D:\CascadeProjects')
pcaps = sorted(pcap_dir.glob('*.pcap'))[:10]  # First 10 PCAPs

for pcap in pcaps:
    try:
        events = read_pcap_ordered(pcap)
        if not events: continue

        # Find 0x1B8B in both directions
        has_1b8b = any(op == 0x1B8B for _, _, op, _ in events)
        if not has_1b8b: continue

        print(f"\n{'='*80}")
        print(f"PCAP: {pcap.name} ({len(events)} events)")
        print(f"{'='*80}")

        first_ts = events[0][0]
        # Show context around 0x1B8B
        for i, (ts, direction, opcode, raw) in enumerate(events):
            t = ts - first_ts
            if opcode == 0x1B8B:
                # Show 5 events before and after
                start = max(0, i-5)
                end = min(len(events), i+6)
                if start > 0:
                    print(f"  ... ({start} events before)")
                for j in range(start, end):
                    ts2, d2, op2, raw2 = events[j]
                    t2 = ts2 - first_ts
                    marker = " <<<" if j == i else ""
                    pl_info = ""
                    if op2 == 0x1B8B:
                        pl_info = f" [{len(raw2)}B] {raw2[4:].hex()}" if len(raw2) > 4 else ""
                    elif op2 == 0x0038:
                        pl_info = f" [{len(raw2)}B]"
                    elif op2 in (0x0042, 0x001F, 0x0021, 0x000B, 0x000C, 0x0020):
                        pl_info = f" [{len(raw2)}B]"
                    print(f"  [{t2:8.3f}s] {d2:3s} 0x{op2:04X} ({len(raw2):5d}B){pl_info}{marker}")
                if end < len(events):
                    print(f"  ... ({len(events)-end} events after)")
                break
    except Exception as e:
        continue

# Now check ALL PCAPs: does S2C 0x1B8B always precede C2S 0x1B8B?
print(f"\n\n{'='*80}")
print("SUMMARY: S2C vs C2S 0x1B8B order across all PCAPs")
print(f"{'='*80}")

all_pcaps = sorted(pcap_dir.glob('*.pcap'))
for sub in ['rebel_attack', 'codex_lab']:
    p = pcap_dir / sub
    if p.exists(): all_pcaps.extend(sorted(p.glob('*.pcap')))

s2c_first = 0
c2s_first = 0
only_c2s = 0
only_s2c = 0
neither = 0

for pcap in all_pcaps:
    try:
        events = read_pcap_ordered(pcap)
        s2c_1b8b = [(ts, d, raw) for ts, d, op, raw in events if op == 0x1B8B and d == 'S2C']
        c2s_1b8b = [(ts, d, raw) for ts, d, op, raw in events if op == 0x1B8B and d == 'C2S']

        if s2c_1b8b and c2s_1b8b:
            if s2c_1b8b[0][0] <= c2s_1b8b[0][0]:
                s2c_first += 1
            else:
                c2s_first += 1
        elif c2s_1b8b:
            only_c2s += 1
        elif s2c_1b8b:
            only_s2c += 1
        else:
            neither += 1
    except:
        continue

print(f"  S2C first (server challenge → client response): {s2c_first}")
print(f"  C2S first (client sends first):                 {c2s_first}")
print(f"  Only C2S (no server challenge):                  {only_c2s}")
print(f"  Only S2C (no client response):                   {only_s2c}")
print(f"  Neither (no 0x1B8B):                             {neither}")

# Also check: what's the S2C 0x1B8B payload?
print(f"\n\nS2C 0x1B8B payload samples:")
count = 0
for pcap in all_pcaps[:20]:
    try:
        events = read_pcap_ordered(pcap)
        for ts, d, op, raw in events:
            if op == 0x1B8B and d == 'S2C':
                print(f"  {pcap.name}: [{len(raw)}B] {raw.hex()}")
                count += 1
                break
    except: continue
    if count >= 5: break

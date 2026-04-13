#!/usr/bin/env python3
"""Check TIMING: does the real client send 0x1B8B BEFORE or AFTER receiving 0x1B8A?
Also check: does 0x1B8A arrive before/after the server key (0x0038)?
This uses the actual PCAP TCP segment ordering to determine real timing."""
import struct
from pathlib import Path

def parse_pcap_ordered(filepath):
    """Parse PCAP and return ALL packets in timestamp order with direction."""
    with open(filepath, 'rb') as f:
        header = f.read(24)
        magic = struct.unpack('<I', header[0:4])[0]
        endian = '<' if magic == 0xa1b2c3d4 else '>'
        link_type = struct.unpack(endian + 'I', header[20:24])[0]
        game_ports = set(range(5990, 6000)) | set(range(7001, 7011))
        
        # Collect TCP segments with timestamps and direction
        segments = []
        while True:
            rec_hdr = f.read(16)
            if len(rec_hdr) < 16: break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', rec_hdr)
            pdata = f.read(incl_len)
            if len(pdata) < incl_len: break
            ts = ts_sec + ts_usec / 1000000.0
            if link_type == 1:
                if len(pdata) < 14: continue
                pdata = pdata[14:]
            elif link_type == 113:
                if len(pdata) < 16: continue
                pdata = pdata[16:]
            if len(pdata) < 20: continue
            if (pdata[0] >> 4) != 4: continue
            ihl = (pdata[0] & 0x0F) * 4
            if pdata[9] != 6: continue
            if len(pdata) < ihl + 20: continue
            tcp = pdata[ihl:]
            sp = struct.unpack('>H', tcp[0:2])[0]
            dp = struct.unpack('>H', tcp[2:4])[0]
            toff = ((tcp[12] >> 4) & 0xF) * 4
            if len(tcp) <= toff: continue
            pl = tcp[toff:]
            if not pl: continue
            if dp in game_ports:
                segments.append((ts, 'C2S', bytes(pl)))
            elif sp in game_ports:
                segments.append((ts, 'S2C', bytes(pl)))
        return segments

def extract_game_packets(raw):
    """Extract game protocol packets from raw TCP data."""
    packets = []
    pos = 0
    while pos + 4 <= len(raw):
        pkt_len = struct.unpack('<H', raw[pos:pos+2])[0]
        opcode = struct.unpack('<H', raw[pos+2:pos+4])[0]
        if pkt_len < 4 or pkt_len > 65535 or pos + pkt_len > len(raw): break
        packets.append((opcode, pkt_len))
        pos += pkt_len
    return packets

pcap_dir = Path(r'D:\CascadeProjects')
pcaps = sorted(pcap_dir.glob('PCAPdroid*.pcap'))

for pcap in pcaps:
    segments = parse_pcap_ordered(str(pcap))
    if not segments: continue
    
    t0 = segments[0][0]
    
    print(f"\n{'='*70}")
    print(f"  {pcap.name}")
    print(f"{'='*70}")
    
    # Find timestamp of key events
    ts_1b8a = None  # S2C 0x1B8A
    ts_1b8b = None  # C2S 0x1B8B
    ts_0038 = None  # S2C 0x0038 (server key)
    ts_first_c2s_after_login = None
    
    c2s_buf = bytearray()
    s2c_buf = bytearray()
    
    events = []
    
    for ts, direction, data in segments:
        rel_ts = ts - t0
        if direction == 'C2S':
            c2s_buf.extend(data)
        else:
            s2c_buf.extend(data)
        
        # Try to parse complete packets from buffer
        buf = c2s_buf if direction == 'C2S' else s2c_buf
        while len(buf) >= 4:
            pkt_len = struct.unpack('<H', buf[0:2])[0]
            if pkt_len < 4 or pkt_len > 65535: 
                buf.clear()
                break
            if len(buf) < pkt_len: break
            opcode = struct.unpack('<H', buf[2:4])[0]
            
            # Record interesting events
            if direction == 'S2C' and opcode == 0x1B8A:
                ts_1b8a = rel_ts
                events.append((rel_ts, 'S2C', '0x1B8A', pkt_len))
            elif direction == 'C2S' and opcode == 0x1B8B:
                ts_1b8b = rel_ts
                events.append((rel_ts, 'C2S', '0x1B8B', pkt_len))
            elif direction == 'S2C' and opcode == 0x0038:
                if ts_0038 is None: ts_0038 = rel_ts
                events.append((rel_ts, 'S2C', '0x0038', pkt_len))
            elif direction == 'C2S' and opcode in (0x001F, 0x0021, 0x0023, 0x0834):
                events.append((rel_ts, 'C2S', f'0x{opcode:04X}', pkt_len))
            
            # Remove parsed packet
            del buf[:pkt_len]
        
        # Restore buffer
        if direction == 'C2S':
            c2s_buf = buf
        else:
            s2c_buf = buf
    
    # Print timeline
    events.sort(key=lambda x: x[0])
    print(f"  Timeline (seconds from start):")
    for ts, d, name, size in events:
        marker = ""
        if name == '0x1B8A': marker = " ← SERVER PASSWORD INFO"
        elif name == '0x1B8B': marker = " ← CLIENT PASSWORD CHECK"
        elif name == '0x0038': marker = " ← SERVER KEY"
        print(f"    {ts:8.3f}s [{d}] {name} ({size}B){marker}")
    
    if ts_1b8a is not None and ts_1b8b is not None:
        if ts_1b8b < ts_1b8a:
            print(f"\n  *** CLIENT sends 0x1B8B {ts_1b8a - ts_1b8b:.3f}s BEFORE receiving 0x1B8A! ***")
        else:
            print(f"\n  *** CLIENT sends 0x1B8B {ts_1b8b - ts_1b8a:.3f}s AFTER receiving 0x1B8A ***")
    
    if ts_0038 is not None and ts_1b8b is not None:
        print(f"  Server key → 0x1B8B: {ts_1b8b - ts_0038:.3f}s")

print("\nDONE")

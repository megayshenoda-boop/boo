#!/usr/bin/env python3
"""Dump ALL C2S packets from PCAPs (not filtered), showing complete sequence before 0x1B8B."""
import struct
from pathlib import Path

def parse_pcap(filepath):
    with open(filepath, 'rb') as f:
        header = f.read(24)
        magic = struct.unpack('<I', header[0:4])[0]
        endian = '<' if magic == 0xa1b2c3d4 else '>'
        link_type = struct.unpack(endian + 'I', header[20:24])[0]
        c2s = bytearray()
        s2c = bytearray()
        game_ports = set(range(5990, 6000)) | set(range(7001, 7011))
        while True:
            rec_hdr = f.read(16)
            if len(rec_hdr) < 16: break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', rec_hdr)
            pdata = f.read(incl_len)
            if len(pdata) < incl_len: break
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
            if dp in game_ports: c2s.extend(pl)
            elif sp in game_ports: s2c.extend(pl)
    return c2s, s2c

def parse_packets(raw):
    packets = []
    pos = 0
    while pos + 4 <= len(raw):
        pkt_len = struct.unpack('<H', raw[pos:pos+2])[0]
        opcode = struct.unpack('<H', raw[pos+2:pos+4])[0]
        if pkt_len < 4 or pkt_len > 65535 or pos + pkt_len > len(raw): break
        packets.append(bytes(raw[pos:pos+pkt_len]))
        pos += pkt_len
    return packets

pcap_dir = Path(r'D:\CascadeProjects')
pcaps = sorted(pcap_dir.glob('PCAPdroid*.pcap'))

for pcap in pcaps:
    c2s_raw, s2c_raw = parse_pcap(str(pcap))
    c2s_pkts = parse_packets(c2s_raw)
    
    print(f"\n{'='*70}")
    print(f"  {pcap.name} - ALL {len(c2s_pkts)} C2S packets")
    print(f"{'='*70}")
    
    found_1b8b = False
    for idx, pkt in enumerate(c2s_pkts):
        pkt_len = struct.unpack('<H', pkt[0:2])[0]
        opcode = struct.unpack('<H', pkt[2:4])[0]
        marker = " <<<" if opcode == 0x1B8B else ""
        if opcode == 0x1B8B: found_1b8b = True
        
        print(f"  [{idx:2d}] 0x{opcode:04X} ({pkt_len:4d}B) payload={pkt[4:min(20,pkt_len)].hex()}{marker}")
        
        # Stop a few packets after 0x1B8B
        if found_1b8b and idx > c2s_pkts.index(pkt) + 5:
            print(f"  ... {len(c2s_pkts) - idx - 1} more packets")
            break

print("\nDONE")

#!/usr/bin/env python3
"""Extract S2C 0x1B8A and 0x1B8C packets from PCAPs to compare gate values."""
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
        packets.append((opcode, bytes(raw[pos+4:pos+pkt_len])))
        pos += pkt_len
    return packets

pcap_dir = Path(r'D:\CascadeProjects')
pcaps = sorted(pcap_dir.glob('PCAPdroid*.pcap'))

for pcap in pcaps:
    c2s_raw, s2c_raw = parse_pcap(str(pcap))
    s2c_pkts = parse_packets(s2c_raw)
    c2s_pkts = parse_packets(c2s_raw)
    
    print(f"\n{'='*60}")
    print(f"  {pcap.name}")
    print(f"{'='*60}")
    
    # Find S2C 0x1B8A
    for op, pl in s2c_pkts:
        if op == 0x1B8A:
            print(f"  S2C 0x1B8A ({len(pl)}B): {pl.hex()}")
            if len(pl) >= 5:
                print(f"    byte[0]={pl[0]} byte[1]={pl[1]} byte[2]={pl[2]} byte[3]={pl[3]} byte[4]={pl[4]} (gate)")
                if len(pl) >= 21:
                    print(f"    Full: [{' '.join(f'{b:02X}' for b in pl)}]")
    
    # Find S2C 0x1B8C (password return)
    for op, pl in s2c_pkts:
        if op == 0x1B8C:
            print(f"  S2C 0x1B8C ({len(pl)}B): {pl.hex()}")
    
    # Find C2S 0x1B8B
    has_1b8b = any(op == 0x1B8B for op, _ in c2s_pkts)
    has_ce8 = any(op == 0x0CE8 for op, _ in c2s_pkts)
    print(f"  C2S 0x1B8B: {'YES' if has_1b8b else 'NO'}")
    print(f"  C2S 0x0CE8: {'YES' if has_ce8 else 'NO'}")
    
    # Also look for 0x00B8 (MARCH_ACK) in init flood
    for op, pl in s2c_pkts:
        if op == 0x00B8:
            print(f"  S2C 0x00B8 MARCH_ACK ({len(pl)}B): {pl.hex()}")
            break
    
    # Look for any 0x0037 error after 0x1B8B
    found_1b8b = False
    for op, pl in s2c_pkts:
        if op == 0x1B8C:
            found_1b8b = True
        if found_1b8b and op == 0x0037:
            print(f"  S2C 0x0037 ERROR after password ({len(pl)}B): {pl.hex()}")

print("\n\n=== CURRENT BOT SESSION ===")
print("  S2C 0x1B8A: 010000000000000000000000000000000000000000")
print("    byte[0]=1 byte[4]=0 (gate=0)")
print("  C2S 0x1B8B: NO (gate=0, don't send)")
print("  C2S 0x0CE8: YES (silently dropped)")

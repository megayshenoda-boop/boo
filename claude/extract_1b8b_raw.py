#!/usr/bin/env python3
"""Extract exact raw bytes of 0x1B8B packets from ALL PCAPs."""
import struct
from pathlib import Path

def parse_pcap_packets(filepath):
    """Parse PCAP and return (c2s_packets, s2c_packets) as raw bytes lists."""
    with open(filepath, 'rb') as f:
        header = f.read(24)
        magic = struct.unpack('<I', header[0:4])[0]
        endian = '<' if magic == 0xa1b2c3d4 else '>'
        link_type = struct.unpack(endian + 'I', header[20:24])[0]
        c2s_raw = bytearray()
        s2c_raw = bytearray()
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
            if dp in game_ports: c2s_raw.extend(pl)
            elif sp in game_ports: s2c_raw.extend(pl)
    
    # Parse packet stream
    def parse_stream(raw):
        pkts = []
        pos = 0
        while pos + 4 <= len(raw):
            pkt_len = struct.unpack('<H', raw[pos:pos+2])[0]
            opcode = struct.unpack('<H', raw[pos+2:pos+4])[0]
            if pkt_len < 4 or pkt_len > 65535 or pos + pkt_len > len(raw): break
            pkts.append(bytes(raw[pos:pos+pkt_len]))
            pos += pkt_len
        return pkts
    
    return parse_stream(c2s_raw), parse_stream(s2c_raw)

def extract_server_key(s2c_pkts):
    for pkt in s2c_pkts:
        opcode = struct.unpack('<H', pkt[2:4])[0]
        if opcode == 0x0038 and len(pkt) > 18:
            pl = pkt[4:]
            entry_count = struct.unpack('<H', pl[0:2])[0]
            for idx in range(entry_count):
                off = 2 + idx * 12
                if off + 12 > len(pl): break
                fid = struct.unpack('<I', pl[off:off+4])[0]
                if fid == 0x4F:
                    return struct.unpack('<I', pl[off+4:off+8])[0]
    return None

pcap_dir = Path(r'D:\CascadeProjects')
pcaps = sorted(pcap_dir.glob('PCAPdroid*.pcap'))

print("ALL 0x1B8B RAW BYTES FROM PCAPs")
print("=" * 70)

all_1b8b = []

for pcap in pcaps:
    c2s_pkts, s2c_pkts = parse_pcap_packets(str(pcap))
    sk = extract_server_key(s2c_pkts)
    
    print(f"\n  {pcap.name}  SK={'0x{:08X}'.format(sk) if sk else 'NONE'}")
    
    for pkt in c2s_pkts:
        opcode = struct.unpack('<H', pkt[2:4])[0]
        if opcode == 0x1B8B:
            print(f"    RAW ({len(pkt)}B): {pkt.hex()}")
            print(f"    Bytes: [{' '.join(f'{b:02X}' for b in pkt)}]")
            
            # Try ALL possible header layouts
            if len(pkt) >= 10:
                # Layout A: [4:6]=extra [6]=ck [7]=msg_lo [8]=verify [9]=msg_hi
                a_verify = pkt[7] ^ 0xB7
                print(f"    Layout A: extra=[{pkt[4]:02X},{pkt[5]:02X}] ck={pkt[6]:02X} ml={pkt[7]:02X} v={pkt[8]:02X} mh={pkt[9]:02X} → {pkt[7]:02X}^B7={a_verify:02X} {'✓' if a_verify==pkt[8] else '✗'}")
                
                # Layout B: [4]=ck [5]=msg_lo [6]=verify [7]=msg_hi [8:10]=extra
                b_verify = pkt[5] ^ 0xB7
                print(f"    Layout B: ck={pkt[4]:02X} ml={pkt[5]:02X} v={pkt[6]:02X} mh={pkt[7]:02X} extra=[{pkt[8]:02X},{pkt[9]:02X}] → {pkt[5]:02X}^B7={b_verify:02X} {'✓' if b_verify==pkt[6] else '✗'}")
                
                # Layout C: [4]=msg_lo [5]=verify [6]=msg_hi [7:9]=extra [9]=ck
                c_verify = pkt[4] ^ 0xB7
                print(f"    Layout C: ml={pkt[4]:02X} v={pkt[5]:02X} mh={pkt[6]:02X} extra=[{pkt[7]:02X},{pkt[8]:02X}] ck={pkt[9]:02X} → {pkt[4]:02X}^B7={c_verify:02X} {'✓' if c_verify==pkt[5] else '✗'}")
                
                # Layout D: [4:6]=extra [6]=msg_lo [7]=verify [8]=msg_hi [9]=ck
                d_verify = pkt[6] ^ 0xB7
                print(f"    Layout D: extra=[{pkt[4]:02X},{pkt[5]:02X}] ml={pkt[6]:02X} v={pkt[7]:02X} mh={pkt[8]:02X} ck={pkt[9]:02X} → {pkt[6]:02X}^B7={d_verify:02X} {'✓' if d_verify==pkt[7] else '✗'}")
                
                all_1b8b.append((pcap.name, sk, pkt))

print(f"\n\nTotal 0x1B8B packets found: {len(all_1b8b)}")

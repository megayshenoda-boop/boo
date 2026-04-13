#!/usr/bin/env python3
"""
Dump ALL raw C2S packets from PCAPs with full hex.
Focus on: 0x0043, 0x0834, 0x0CEB, 0x0CE8, 0x0323
Also extract the exact encrypted bytes for comparison.
"""
import struct
from pathlib import Path

CMSG_TABLE = [0x58, 0xEF, 0xD7, 0x14, 0xA2, 0x3B, 0x9C]

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

def extract_server_key(s2c_raw):
    packets = parse_packets(s2c_raw)
    for pkt in packets:
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

def decrypt_standard(pkt, sk_bytes):
    """Decrypt standard CMsgCodec packet, return plaintext or None."""
    if len(pkt) < 8: return None
    ck = pkt[4]; msg_lo = pkt[5]; verify = pkt[6]; msg_hi = pkt[7]
    if verify != (msg_lo ^ 0xB7): return None
    msg = [msg_lo, msg_hi]
    check = 0
    for i in range(8, len(pkt)):
        check = (check + pkt[i]) & 0xFFFFFFFF
    if (check & 0xFF) != ck: return None
    dec = bytearray(len(pkt) - 8)
    for i in range(8, len(pkt)):
        table_b = CMSG_TABLE[i % 7]
        sk_b = sk_bytes[i % 4]
        msg_b = msg[i % 2]
        intermediate = (pkt[i] ^ sk_b ^ table_b) & 0xFF
        dec[i - 8] = (intermediate - msg_b * 17) & 0xFF
    return bytes(dec)

INTERESTING = {0x0043, 0x0834, 0x0CEB, 0x0CE8, 0x0323, 0x1B8B, 0x0042, 0x006E}

pcap_dir = Path(r'D:\CascadeProjects')
pcaps = sorted(pcap_dir.glob('PCAPdroid*.pcap'))

for pcap in pcaps:
    c2s_raw, s2c_raw = parse_pcap(str(pcap))
    sk = extract_server_key(s2c_raw)
    if not sk: continue
    sk_bytes = [(sk >> (8*i)) & 0xFF for i in range(4)]
    
    c2s_pkts = parse_packets(c2s_raw)
    
    print(f"\n{'='*70}")
    print(f"  {pcap.name}  SK=0x{sk:08X}")
    print(f"  C2S packets: {len(c2s_pkts)}")
    print(f"{'='*70}")
    
    for idx, pkt in enumerate(c2s_pkts):
        pkt_len = struct.unpack('<H', pkt[0:2])[0]
        opcode = struct.unpack('<H', pkt[2:4])[0]
        
        if opcode not in INTERESTING:
            continue
        
        print(f"\n  [{idx}] 0x{opcode:04X} ({pkt_len}B)")
        print(f"       RAW: {pkt.hex()}")
        
        # Header analysis
        if pkt_len >= 8:
            print(f"       [0:2]=len={pkt_len} [2:4]=op=0x{opcode:04X}")
            print(f"       [4]=0x{pkt[4]:02X} [5]=0x{pkt[5]:02X} [6]=0x{pkt[6]:02X} [7]=0x{pkt[7]:02X}")
            
            # Standard check
            if pkt[6] == (pkt[5] ^ 0xB7):
                print(f"       STD verify OK: [5]^0xB7 = 0x{pkt[5]^0xB7:02X} == [6]=0x{pkt[6]:02X}")
                plain = decrypt_standard(pkt, sk_bytes)
                if plain:
                    print(f"       STD PLAIN ({len(plain)}B): {plain.hex()}")
                    # Parse gather fields
                    if opcode == 0x0CE8 and len(plain) >= 46:
                        slot = plain[0]
                        nonce = plain[1:4].hex()
                        mtype = struct.unpack('<H', plain[4:6])[0]
                        tx = struct.unpack('<H', plain[9:11])[0]
                        ty = struct.unpack('<H', plain[11:13])[0]
                        flag = plain[13]
                        hero = plain[14]
                        kingdom = plain[18]
                        purpose = plain[22]
                        igg = struct.unpack('<I', plain[33:37])[0]
                        print(f"       GATHER: slot={slot} type=0x{mtype:04X} ({tx},{ty}) flag={flag} hero={hero} kingdom={kingdom} purpose={purpose} igg={igg}")
                else:
                    print(f"       STD checksum FAIL")
            
            # Offset6 check
            if pkt_len >= 10 and pkt[8] == (pkt[7] ^ 0xB7):
                print(f"       OFF6 verify OK: [7]^0xB7 = 0x{pkt[7]^0xB7:02X} == [8]=0x{pkt[8]:02X}")
        
        # For plain packets
        if opcode in (0x0043, 0x0834, 0x006E, 0x0323, 0x0042):
            print(f"       PAYLOAD ({pkt_len-4}B): {pkt[4:].hex()}")
            if opcode == 0x0043 and pkt_len >= 12:
                vals = []
                for o in range(4, pkt_len, 4):
                    if o + 4 <= pkt_len:
                        vals.append(struct.unpack('<I', pkt[o:o+4])[0])
                print(f"       u32 values: {[f'0x{v:08X}' for v in vals]}")
            elif opcode == 0x0323:
                pl = pkt[4:]
                print(f"       HERO_SEL: raw={pl.hex()} slot={pl[1] if len(pl)>1 else '?'} hero={pl[3] if len(pl)>3 else '?'}")

print("\nDONE")

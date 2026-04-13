#!/usr/bin/env python3
"""
Decode ALL C2S encrypted packets from PCAPs, focusing on 0x0CE8 (gather).
Also decode other encrypted packets to verify codec works on PCAPs.
"""
import struct
from pathlib import Path

CMSG_TABLE = [0x58, 0xEF, 0xD7, 0x14, 0xA2, 0x3B, 0x9C]

def decode_standard(raw_pkt, sk_bytes):
    """Decode a full packet using standard CMsgCodec::Encode format."""
    if len(raw_pkt) < 8:
        return None, None, False
    pkt_len = struct.unpack('<H', raw_pkt[0:2])[0]
    opcode = struct.unpack('<H', raw_pkt[2:4])[0]
    
    ck = raw_pkt[4]
    msg_lo = raw_pkt[5]
    verify = raw_pkt[6]
    msg_hi = raw_pkt[7]
    
    v_ok = verify == (msg_lo ^ 0xB7)
    msg = [msg_lo, msg_hi]
    
    encrypted = bytearray(raw_pkt[8:pkt_len])
    plain = bytearray(len(encrypted))
    check = 0
    for j in range(len(encrypted)):
        i = 8 + j
        table_b = CMSG_TABLE[i % 7]
        sk_b = sk_bytes[i % 4]
        msg_b = msg[i % 2]
        enc_byte = encrypted[j]
        check = (check + enc_byte) & 0xFFFFFFFF
        intermediate = (enc_byte ^ sk_b ^ table_b) & 0xFF
        plain_byte = (intermediate - msg_b * 17) & 0xFF
        plain[j] = plain_byte
    
    ck_ok = (check & 0xFF) == ck
    return opcode, bytes(plain), ck_ok and v_ok

def decode_offset6(raw_pkt, sk_bytes):
    """Decode a full packet using NewEncode format."""
    if len(raw_pkt) < 10:
        return None, None, False
    pkt_len = struct.unpack('<H', raw_pkt[0:2])[0]
    opcode = struct.unpack('<H', raw_pkt[2:4])[0]
    
    extra = raw_pkt[4:6]
    ck = raw_pkt[6]
    msg_lo = raw_pkt[7]
    verify = raw_pkt[8]
    msg_hi = raw_pkt[9]
    
    v_ok = verify == (msg_lo ^ 0xB7)
    msg = [msg_lo, msg_hi]
    
    encrypted = bytearray(raw_pkt[10:pkt_len])
    plain = bytearray(len(encrypted))
    check = 0
    for j in range(len(encrypted)):
        i = 10 + j
        table_b = CMSG_TABLE[i % 7]
        sk_b = sk_bytes[i % 4]
        msg_b = msg[i % 2]
        enc_byte = encrypted[j]
        check = (check + enc_byte) & 0xFFFFFFFF
        intermediate = (enc_byte ^ sk_b ^ table_b) & 0xFF
        plain_byte = (intermediate - msg_b * 17) & 0xFF
        plain[j] = plain_byte
    
    ck_ok = (check & 0xFF) == ck
    return opcode, bytes(plain), ck_ok and v_ok

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
            if dp in game_ports:
                c2s.extend(pl)
            elif sp in game_ports:
                s2c.extend(pl)
        
        return c2s, s2c

def parse_raw_packets(raw):
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
    packets = parse_raw_packets(s2c_raw)
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

# Known encrypted C2S opcodes
ENCRYPTED_OPS = {0x0CE8, 0x0CEB, 0x0CED, 0x1B8B, 0x0769, 0x006E, 0x0042}

pcap_dir = Path(r'D:\CascadeProjects')
pcaps = sorted(pcap_dir.glob('PCAPdroid*.pcap'))

print(f"Found {len(pcaps)} PCAPs")

for pcap in pcaps:
    c2s_raw, s2c_raw = parse_pcap(str(pcap))
    sk = extract_server_key(s2c_raw)
    if not sk: continue
    sk_bytes = [(sk >> (8*i)) & 0xFF for i in range(4)]
    
    c2s_pkts = parse_raw_packets(c2s_raw)
    
    print(f"\n{'='*80}")
    print(f"  {pcap.name}  SK=0x{sk:08X}")
    print(f"{'='*80}")
    
    for pkt in c2s_pkts:
        pkt_len = struct.unpack('<H', pkt[0:2])[0]
        opcode = struct.unpack('<H', pkt[2:4])[0]
        
        # Try standard decode
        op_s, plain_s, ok_s = decode_standard(pkt, sk_bytes)
        # Try offset6 decode
        op_o, plain_o, ok_o = decode_offset6(pkt, sk_bytes)
        
        if opcode == 0x0CE8:
            print(f"\n  *** 0x0CE8 GATHER ({pkt_len}B) ***")
            if ok_s:
                print(f"    StdDecode OK: {plain_s.hex()}")
                print(f"    Plain ({len(plain_s)}B) breakdown:")
                if len(plain_s) >= 46:
                    print(f"      [0]  march_slot  = {plain_s[0]}")
                    print(f"      [1:4] nonce      = {plain_s[1:4].hex()}")
                    print(f"      [4:6] march_type = 0x{struct.unpack('<H', plain_s[4:6])[0]:04X}")
                    print(f"      [6:9]            = {plain_s[6:9].hex()}")
                    print(f"      [9:11] tile_x    = {struct.unpack('<H', plain_s[9:11])[0]}")
                    print(f"      [11:13] tile_y   = {struct.unpack('<H', plain_s[11:13])[0]}")
                    print(f"      [13] flag        = {plain_s[13]}")
                    print(f"      [14] hero_id     = {plain_s[14]}")
                    print(f"      [15:18]          = {plain_s[15:18].hex()}")
                    print(f"      [18] kingdom     = {plain_s[18]}")
                    print(f"      [19:22]          = {plain_s[19:22].hex()}")
                    print(f"      [22] purpose     = {plain_s[22]}")
                    print(f"      [23:33]          = {plain_s[23:33].hex()}")
                    print(f"      [33:37] igg_id   = {struct.unpack('<I', plain_s[33:37])[0]}")
                    print(f"      [37:46]          = {plain_s[37:46].hex()}")
            elif ok_o:
                print(f"    Offset6 OK: {plain_o.hex()}")
            else:
                print(f"    BOTH FAIL!")
                print(f"    StdDecode: ck={ok_s}")
                print(f"    Offset6: ck={ok_o}")
        
        elif opcode == 0x1B8B:
            enc_type = "Offset6" if ok_o else ("Std" if ok_s else "NONE")
            print(f"  0x1B8B ({pkt_len}B): decoded={enc_type}")
        
        elif ok_s and pkt_len > 8:
            # Other encrypted packet that decodes OK
            print(f"  0x{opcode:04X} ({pkt_len}B): StdDecode OK, plain({len(plain_s)}B)={plain_s[:20].hex()}{'...' if len(plain_s)>20 else ''}")
        
        elif pkt_len <= 8:
            # Plain/unencrypted
            pass
        
        elif not ok_s and not ok_o and pkt_len > 8:
            print(f"  0x{opcode:04X} ({pkt_len}B): CANNOT DECODE (std_ok={ok_s}, off6_ok={ok_o})")

print("\nDONE")

#!/usr/bin/env python3
"""
Verify 0x1B8B across ALL PCAPs:
1. Decode each C2S 0x1B8B with offset6 (NewEncode) using correct server key
2. Check if getCheckId (first 8 bytes) is constant
3. Check if encodePassword (last 8 bytes) is constant (0xFFFFFFFFFFFFFFFF)
4. Also verify with STANDARD decode to compare
"""
import struct
from pathlib import Path

CMSG_TABLE = [0x58, 0xEF, 0xD7, 0x14, 0xA2, 0x3B, 0x9C]

def decode_offset6(payload, sk_bytes):
    """Decode with NewEncode layout: header at [6:9], encrypted from [10:]"""
    if len(payload) < 18:
        return None, None, None
    ck = payload[0]      # [6] in full packet = [0] in payload after opcode... 
    # Wait - payload here is AFTER [len][opcode], so:
    # payload[0:2] = extra bytes (getMsgIndex output)
    # payload[2] = checksum
    # payload[3] = msg_lo
    # payload[4] = verify
    # payload[5] = msg_hi
    # payload[6:22] = encrypted data (16 bytes)
    
    extra = payload[0:2]
    ck = payload[2]
    msg_lo = payload[3]
    verify = payload[4]
    msg_hi = payload[5]
    encrypted = bytearray(payload[6:])
    
    msg = [msg_lo, msg_hi]
    
    # Decrypt starting from position 10 in full packet
    # Full packet: [0:2]=len [2:4]=opcode [4:6]=extra [6]=ck [7]=ml [8]=v [9]=mh [10:]=encrypted
    # So encrypted[j] is at full packet position (10 + j)
    plain = bytearray(len(encrypted))
    check = 0
    for j in range(len(encrypted)):
        i = 10 + j  # position in full packet
        table_b = CMSG_TABLE[i % 7]
        sk_b = sk_bytes[i % 4]
        msg_b = msg[i % 2]
        enc_byte = encrypted[j]
        check = (check + enc_byte) & 0xFFFFFFFF
        intermediate = (enc_byte ^ sk_b ^ table_b) & 0xFF
        plain_byte = (intermediate - msg_b * 17) & 0xFF
        plain[j] = plain_byte
    
    ck_ok = (check & 0xFF) == ck
    v_ok = verify == (msg_lo ^ 0xB7)
    
    return bytes(plain), ck_ok, v_ok

def decode_standard(payload, sk_bytes):
    """Decode with standard Encode layout: header at [4:7], encrypted from [8:]"""
    if len(payload) < 4:
        return None, None, None
    
    ck = payload[0]
    msg_lo = payload[1]
    verify = payload[2]
    msg_hi = payload[3]
    encrypted = bytearray(payload[4:])
    
    msg = [msg_lo, msg_hi]
    
    plain = bytearray(len(encrypted))
    check = 0
    for j in range(len(encrypted)):
        i = 8 + j  # position in full packet
        table_b = CMSG_TABLE[i % 7]
        sk_b = sk_bytes[i % 4]
        msg_b = msg[i % 2]
        enc_byte = encrypted[j]
        check = (check + enc_byte) & 0xFFFFFFFF
        intermediate = (enc_byte ^ sk_b ^ table_b) & 0xFF
        plain_byte = (intermediate - msg_b * 17) & 0xFF
        plain[j] = plain_byte
    
    ck_ok = (check & 0xFF) == ck
    v_ok = verify == (msg_lo ^ 0xB7)
    
    return bytes(plain), ck_ok, v_ok

def read_pcap_streams(filepath):
    """Read PCAP and split into C2S and S2C streams."""
    with open(filepath, 'rb') as f:
        magic = struct.unpack('<I', f.read(4))[0]
        endian = '<' if magic == 0xa1b2c3d4 else '>'
        f.read(20)
        streams = {}
        while True:
            hdr = f.read(16)
            if len(hdr) < 16: break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
            pdata = f.read(incl_len)
            if len(pdata) < incl_len: break
            if len(pdata) < 20: continue
            if pdata[0] == 0x45:  # IPv4
                ihl = (pdata[0] & 0x0F) * 4
                proto = pdata[9]
            elif len(pdata) > 14 and pdata[14] == 0x45:  # Ethernet + IPv4
                pdata = pdata[14:]
                ihl = (pdata[0] & 0x0F) * 4
                proto = pdata[9]
            else:
                continue
            if proto != 6: continue  # TCP only
            tcp = pdata[ihl:]
            if len(tcp) < 20: continue
            sp = struct.unpack('>H', tcp[0:2])[0]
            dp = struct.unpack('>H', tcp[2:4])[0]
            toff = ((tcp[12] >> 4) & 0xF) * 4
            pl = tcp[toff:]
            if not pl: continue
            gp = set(range(5990, 6000)) | set(range(7001, 7011))
            if dp in gp:
                streams.setdefault('C2S', bytearray()).extend(pl)
            elif sp in gp:
                streams.setdefault('S2C', bytearray()).extend(pl)
    return streams

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

def extract_server_key(s2c_packets):
    """Extract server key from 0x0038 packet field 0x4F."""
    for op, pl in s2c_packets:
        if op == 0x0038 and len(pl) > 10:
            pos = 0
            while pos + 3 <= len(pl):
                fid = struct.unpack('<H', pl[pos:pos+2])[0]
                flen = pl[pos+2]
                if pos + 3 + flen > len(pl): break
                if fid == 0x4F and flen == 4:
                    return struct.unpack('<I', pl[pos+3:pos+7])[0]
                pos += 3 + flen
    return None

# Process all PCAPs
pcap_dir = Path(r'D:\CascadeProjects')
pcaps = sorted(pcap_dir.glob('*.pcap'))

print("=" * 100)
print("PCAP 0x1B8B VERIFICATION")
print("=" * 100)

all_check_ids = []
all_passwords = []

for pcap in pcaps:
    try:
        streams = read_pcap_streams(str(pcap))
        if 'S2C' not in streams or 'C2S' not in streams:
            continue
        
        s2c = parse_packets(streams['S2C'])
        c2s = parse_packets(streams['C2S'])
        
        sk = extract_server_key(s2c)
        if not sk:
            continue
        
        sk_bytes = [(sk >> (8*i)) & 0xFF for i in range(4)]
        
        # Find C2S 0x1B8B packets
        for op, pl in c2s:
            if op == 0x1B8B:
                print(f"\n{pcap.name}  SK=0x{sk:08X}  payload({len(pl)}B): {pl.hex()}")
                
                # Offset6 decode (NewEncode)
                plain6, ck6, v6 = decode_offset6(pl, sk_bytes)
                if plain6:
                    check_id = plain6[:8]
                    password = plain6[8:]
                    all_check_ids.append(check_id)
                    all_passwords.append(password)
                    print(f"  OFFSET6: plain={plain6.hex()}  ck={ck6}  v={v6}")
                    print(f"    checkId={check_id.hex()} ({struct.unpack('<q', check_id)[0]})")
                    print(f"    password={password.hex()} ({struct.unpack('<q', password)[0]})")
                    if password == b'\xff' * 8:
                        print(f"    => PASSWORD = -1 (EMPTY/NO SECONDARY PASSWORD)")
                
                # Standard decode (Encode) for comparison
                plain_s, ck_s, v_s = decode_standard(pl, sk_bytes)
                if plain_s:
                    print(f"  STANDARD: plain={plain_s.hex()}  ck={ck_s}  v={v_s}")
                
    except Exception as e:
        print(f"  ERROR {pcap.name}: {e}")
        continue

# Summary
print(f"\n{'='*100}")
print(f"SUMMARY: {len(all_check_ids)} 0x1B8B packets decoded")
print(f"{'='*100}")

if all_check_ids:
    unique_cids = set(cid.hex() for cid in all_check_ids)
    print(f"  Unique checkId values: {len(unique_cids)}")
    for cid in unique_cids:
        count = sum(1 for c in all_check_ids if c.hex() == cid)
        print(f"    {cid} (x{count})")
    
    unique_pws = set(pw.hex() for pw in all_passwords)
    print(f"  Unique password values: {len(unique_pws)}")
    for pw in unique_pws:
        count = sum(1 for p in all_passwords if p.hex() == pw)
        val = struct.unpack('<q', bytes.fromhex(pw))[0]
        print(f"    {pw} = {val} (x{count})")
    
    if len(unique_cids) == 1:
        print(f"\n  *** getCheckId IS CONSTANT: {list(unique_cids)[0]} ***")
    else:
        print(f"\n  *** getCheckId VARIES across sessions! ***")
    
    if len(unique_pws) == 1 and list(unique_pws)[0] == 'ffffffffffffffff':
        print(f"  *** Password is ALWAYS -1 (no secondary password) ***")

print("\nDONE")

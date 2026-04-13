#!/usr/bin/env python3
"""
Verify 0x1B8B across PCAPs - fixed parser.
"""
import struct
from pathlib import Path

CMSG_TABLE = [0x58, 0xEF, 0xD7, 0x14, 0xA2, 0x3B, 0x9C]

def decode_offset6(payload, sk_bytes):
    """NewEncode: extra[0:2], ck[2], ml[3], v[4], mh[5], encrypted[6:]"""
    if len(payload) < 8:
        return None, False, False
    extra = payload[0:2]
    ck = payload[2]
    msg_lo = payload[3]
    verify = payload[4]
    msg_hi = payload[5]
    encrypted = bytearray(payload[6:])
    msg = [msg_lo, msg_hi]
    
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
    
    return bytes(plain), (check & 0xFF) == ck, verify == (msg_lo ^ 0xB7)

def decode_standard(payload, sk_bytes):
    """Standard Encode: ck[0], ml[1], v[2], mh[3], encrypted[4:]"""
    if len(payload) < 5:
        return None, False, False
    ck = payload[0]
    msg_lo = payload[1]
    verify = payload[2]
    msg_hi = payload[3]
    encrypted = bytearray(payload[4:])
    msg = [msg_lo, msg_hi]
    
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
    
    return bytes(plain), (check & 0xFF) == ck, verify == (msg_lo ^ 0xB7)

def parse_pcap(filepath):
    """Parse PCAP with robust link-layer detection."""
    with open(filepath, 'rb') as f:
        header = f.read(24)
        if len(header) < 24:
            return {}
        magic = struct.unpack('<I', header[0:4])[0]
        if magic == 0xa1b2c3d4:
            endian = '<'
        elif magic == 0xd4c3b2a1:
            endian = '>'
        else:
            return {}
        
        link_type = struct.unpack(endian + 'I', header[20:24])[0]
        
        c2s = bytearray()
        s2c = bytearray()
        game_ports = set(range(5990, 6000)) | set(range(7001, 7011))
        
        while True:
            rec_hdr = f.read(16)
            if len(rec_hdr) < 16:
                break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', rec_hdr)
            pdata = f.read(incl_len)
            if len(pdata) < incl_len:
                break
            
            # Strip link layer
            if link_type == 1:  # Ethernet
                if len(pdata) < 14:
                    continue
                pdata = pdata[14:]
            elif link_type == 101:  # Raw IP
                pass
            elif link_type == 113:  # Linux cooked
                if len(pdata) < 16:
                    continue
                pdata = pdata[16:]
            else:
                # Try raw IP
                pass
            
            if len(pdata) < 20:
                continue
            
            # Check IPv4
            ver = (pdata[0] >> 4) & 0xF
            if ver != 4:
                continue
            
            ihl = (pdata[0] & 0x0F) * 4
            proto = pdata[9]
            if proto != 6:  # TCP
                continue
            
            if len(pdata) < ihl + 20:
                continue
            
            tcp = pdata[ihl:]
            sp = struct.unpack('>H', tcp[0:2])[0]
            dp = struct.unpack('>H', tcp[2:4])[0]
            toff = ((tcp[12] >> 4) & 0xF) * 4
            
            if len(tcp) <= toff:
                continue
            
            pl = tcp[toff:]
            if not pl:
                continue
            
            if dp in game_ports:
                c2s.extend(pl)
            elif sp in game_ports:
                s2c.extend(pl)
        
        return {'C2S': c2s, 'S2C': s2c}

def parse_packets(raw):
    packets = []
    pos = 0
    while pos + 4 <= len(raw):
        pkt_len = struct.unpack('<H', raw[pos:pos+2])[0]
        opcode = struct.unpack('<H', raw[pos+2:pos+4])[0]
        if pkt_len < 4 or pkt_len > 65535 or pos + pkt_len > len(raw):
            break
        packets.append((opcode, bytes(raw[pos+4:pos+pkt_len])))
        pos += pkt_len
    return packets

def extract_server_key(s2c_packets):
    """Extract server key from 0x0038 using [2B count][12B entries] format."""
    for op, pl in s2c_packets:
        if op == 0x0038 and len(pl) >= 14:
            entry_count = struct.unpack('<H', pl[0:2])[0]
            for idx in range(entry_count):
                off = 2 + idx * 12
                if off + 12 > len(pl):
                    break
                field_id = struct.unpack('<I', pl[off:off+4])[0]
                if field_id == 0x4F:
                    return struct.unpack('<I', pl[off+4:off+8])[0]
    return None

# Process PCAPs
pcap_dir = Path(r'D:\CascadeProjects')
pcaps = sorted(pcap_dir.glob('*.pcap'))

print(f"Found {len(pcaps)} PCAP files")
print("=" * 100)

all_check_ids = []
all_passwords = []
all_plains = []

for pcap in pcaps:
    try:
        streams = parse_pcap(str(pcap))
        c2s_raw = streams.get('C2S', bytearray())
        s2c_raw = streams.get('S2C', bytearray())
        
        if not c2s_raw or not s2c_raw:
            continue
        
        s2c = parse_packets(s2c_raw)
        c2s = parse_packets(c2s_raw)
        
        sk = extract_server_key(s2c)
        if not sk:
            continue
        
        sk_bytes = [(sk >> (8*i)) & 0xFF for i in range(4)]
        
        c2s_1b8b = [(op, pl) for op, pl in c2s if op == 0x1B8B]
        
        if not c2s_1b8b:
            continue
        
        for op, pl in c2s_1b8b:
            print(f"\n{pcap.name}  SK=0x{sk:08X}  payload({len(pl)}B): {pl[:30].hex()}{'...' if len(pl)>30 else ''}")
            
            # Offset6 (NewEncode)
            plain6, ck6, v6 = decode_offset6(pl, sk_bytes)
            if plain6 and len(plain6) >= 16:
                check_id = plain6[:8]
                password = plain6[8:16]
                all_check_ids.append(check_id)
                all_passwords.append(password)
                all_plains.append(plain6)
                ci_val = struct.unpack('<q', check_id)[0]
                pw_val = struct.unpack('<q', password)[0]
                print(f"  OFFSET6: ck_ok={ck6} v_ok={v6}")
                print(f"    plain    = {plain6.hex()}")
                print(f"    checkId  = {check_id.hex()} (={ci_val})")
                print(f"    password = {password.hex()} (={pw_val})")
                if pw_val == -1:
                    print(f"    => EMPTY PASSWORD (encodePassword returns -1)")
            
            # Standard (Encode) for comparison
            plain_s, ck_s, v_s = decode_standard(pl, sk_bytes)
            if plain_s:
                print(f"  STANDARD: ck_ok={ck_s} v_ok={v_s}")
                print(f"    plain    = {plain_s.hex()}")

    except Exception as e:
        import traceback
        print(f"  ERROR {pcap.name}: {e}")
        traceback.print_exc()

# Summary
print(f"\n{'='*100}")
print(f"SUMMARY: {len(all_check_ids)} packets from {len(pcaps)} PCAPs")
print(f"{'='*100}")

if all_check_ids:
    unique_cids = list(set(cid.hex() for cid in all_check_ids))
    print(f"  Unique checkId values: {len(unique_cids)}")
    for cid in sorted(unique_cids):
        count = sum(1 for c in all_check_ids if c.hex() == cid)
        val = struct.unpack('<q', bytes.fromhex(cid))[0]
        print(f"    {cid} = {val} (x{count})")
    
    unique_pws = list(set(pw.hex() for pw in all_passwords))
    print(f"\n  Unique password values: {len(unique_pws)}")
    for pw in sorted(unique_pws):
        count = sum(1 for p in all_passwords if p.hex() == pw)
        val = struct.unpack('<q', bytes.fromhex(pw))[0]
        print(f"    {pw} = {val} (x{count})")
    
    unique_plains = list(set(p.hex() for p in all_plains))
    print(f"\n  Unique full plaintexts: {len(unique_plains)}")
    for p in sorted(unique_plains):
        print(f"    {p}")
    
    if len(unique_cids) == 1:
        print(f"\n  *** getCheckId IS CONSTANT ***")
    else:
        print(f"\n  *** getCheckId VARIES ***")
else:
    print("  No 0x1B8B packets found!")
    # Debug: show what we DID find
    for pcap in pcaps[:5]:
        try:
            streams = parse_pcap(str(pcap))
            c2s = parse_packets(streams.get('C2S', bytearray()))
            s2c = parse_packets(streams.get('S2C', bytearray()))
            opcodes_c2s = set(hex(op) for op, _ in c2s[:50])
            opcodes_s2c = set(hex(op) for op, _ in s2c[:50])
            print(f"  {pcap.name}: C2S={len(c2s)} pkts, S2C={len(s2c)} pkts")
            if c2s:
                print(f"    C2S opcodes: {sorted(opcodes_c2s)[:20]}")
            if s2c:
                print(f"    S2C opcodes: {sorted(opcodes_s2c)[:20]}")
        except:
            pass

print("\nDONE")

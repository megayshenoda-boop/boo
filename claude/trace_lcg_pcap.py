#!/usr/bin/env python3
"""
Extract msg_lo/msg_hi from ALL encrypted C2S packets in PCAPs.
Trace the LCG sequence and find the initial seed.
LCG: next = (prev * 37 + 13) & 0xFFFF
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

def verify_standard(pkt, sk_bytes):
    """Check if standard encode header is valid. Returns (ok, msg_value)."""
    if len(pkt) < 8: return False, 0
    ck = pkt[4]; msg_lo = pkt[5]; verify = pkt[6]; msg_hi = pkt[7]
    if verify != (msg_lo ^ 0xB7): return False, 0
    msg = [msg_lo, msg_hi]
    check = 0
    for i in range(8, len(pkt)):
        check = (check + pkt[i]) & 0xFFFFFFFF
    if (check & 0xFF) != ck: return False, 0
    return True, (msg_hi << 8) | msg_lo

def verify_offset6(pkt, sk_bytes):
    """Check NewEncode header. Returns (ok, extra_value, msg_value)."""
    if len(pkt) < 10: return False, 0, 0
    extra = (pkt[5] << 8) | pkt[4]
    ck = pkt[6]; msg_lo = pkt[7]; verify = pkt[8]; msg_hi = pkt[9]
    if verify != (msg_lo ^ 0xB7): return False, 0, 0
    check = 0
    for i in range(10, len(pkt)):
        check = (check + pkt[i]) & 0xFFFFFFFF
    if (check & 0xFF) != ck: return False, 0, 0
    return True, extra, (msg_hi << 8) | msg_lo

def lcg_next(state):
    return (state * 37 + 13) & 0xFFFF

def find_lcg_seed(msg_values):
    """Given a sequence of msg values, find the LCG seed that produces them."""
    if not msg_values: return None
    first_msg = msg_values[0]
    # Brute force: try all 65536 seeds
    for seed in range(65536):
        state = seed
        match = True
        for expected_msg in msg_values:
            state = lcg_next(state)
            if state != expected_msg:
                match = False
                break
        if match:
            return seed
    return None

pcap_dir = Path(r'D:\CascadeProjects')
pcaps = sorted(pcap_dir.glob('PCAPdroid*.pcap'))

print(f"Found {len(pcaps)} PCAPs\n")

for pcap in pcaps:
    c2s_raw, s2c_raw = parse_pcap(str(pcap))
    sk = extract_server_key(s2c_raw)
    if not sk: continue
    sk_bytes = [(sk >> (8*i)) & 0xFF for i in range(4)]
    
    c2s_pkts = parse_raw_packets(c2s_raw)
    
    print(f"{'='*70}")
    print(f"  {pcap.name}  SK=0x{sk:08X}")
    print(f"{'='*70}")
    
    msg_sequence = []  # (opcode, msg_value, encode_type)
    
    for pkt in c2s_pkts:
        pkt_len = struct.unpack('<H', pkt[0:2])[0]
        opcode = struct.unpack('<H', pkt[2:4])[0]
        
        # Try standard
        ok_s, msg_s = verify_standard(pkt, sk_bytes)
        # Try offset6
        ok_o, extra_o, msg_o = verify_offset6(pkt, sk_bytes)
        
        if ok_o and opcode == 0x1B8B:
            # NewEncode: extra bytes also from LCG
            msg_sequence.append((opcode, extra_o, "extra"))
            msg_sequence.append((opcode, msg_o, "msg"))
            print(f"  0x{opcode:04X} NewEncode  extra=0x{extra_o:04X}  msg=0x{msg_o:04X}")
        elif ok_s and pkt_len > 8:
            msg_sequence.append((opcode, msg_s, "msg"))
            print(f"  0x{opcode:04X} StdEncode  msg=0x{msg_s:04X}")
        # else: plain packet, skip
    
    # Extract just the msg values in order
    all_msg_vals = [v for _, v, _ in msg_sequence]
    print(f"\n  LCG sequence: {['0x{:04X}'.format(v) for v in all_msg_vals]}")
    
    # Find seed
    seed = find_lcg_seed(all_msg_vals)
    if seed is not None:
        print(f"  *** LCG SEED = {seed} (0x{seed:04X}) ***")
        # Verify
        state = seed
        for i, (op, v, t) in enumerate(msg_sequence):
            state = lcg_next(state)
            ok = "✓" if state == v else "✗"
            print(f"    step {i+1}: LCG={state:#06x} pkt={v:#06x} {ok} ({t} of 0x{op:04X})")
    else:
        print(f"  *** NO SEED FOUND ***")
        # Try with partial sequences
        if len(all_msg_vals) >= 2:
            # Maybe first msg starts the sequence
            first = all_msg_vals[0]
            # Find what seed produces this first value
            for s in range(65536):
                if lcg_next(s) == first:
                    print(f"    Seed candidate for first msg: {s} (0x{s:04X})")
                    state = s
                    for v in all_msg_vals:
                        state = lcg_next(state)
                        ok = "✓" if state == v else "✗"
                        print(f"      LCG={state:#06x} pkt={v:#06x} {ok}")
                    break
    
    # Check relationship with server key
    print(f"\n  SK analysis:")
    print(f"    SK & 0xFFFF = 0x{sk & 0xFFFF:04X}")
    print(f"    SK >> 16    = 0x{(sk >> 16) & 0xFFFF:04X}")
    print(f"    SK bytes: [{sk_bytes[0]:#04x}, {sk_bytes[1]:#04x}, {sk_bytes[2]:#04x}, {sk_bytes[3]:#04x}]")
    if seed is not None:
        print(f"    SEED = {seed} (0x{seed:04X})")
    print()

print("DONE")

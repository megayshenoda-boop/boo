#!/usr/bin/env python3
"""
27_pcap_gather_sequence.py - Extract the EXACT packet sequence from a successful gather PCAP.
Find: tile search request/response, view commands, gather target coords.
"""
import struct
from pathlib import Path

TABLE = [0x58, 0xef, 0xd7, 0x14, 0xa2, 0x3b, 0x9c]

def read_pcap_ordered(filepath):
    with open(filepath, 'rb') as f:
        magic = struct.unpack('<I', f.read(4))[0]
        endian = '<' if magic == 0xa1b2c3d4 else '>'
        f.read(20)
        events = []
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

def extract_sk(events):
    for ts, d, op, raw in events:
        if op == 0x0038 and d == 'S2C':
            pl = raw[4:]
            if len(pl) > 100:
                ec = struct.unpack('<H', pl[0:2])[0]
                for idx in range(ec):
                    off = 2 + idx * 12
                    if off + 12 > len(pl): break
                    if struct.unpack('<I', pl[off:off+4])[0] == 0x4F:
                        return struct.unpack('<I', pl[off+4:off+8])[0]
    return None

def decrypt_cmsg(raw, sk_u32):
    """Decrypt standard Encode packet."""
    if len(raw) < 12: return None
    pl = raw[4:]  # payload after [len][op]
    sk = [sk_u32 & 0xFF, (sk_u32>>8) & 0xFF, (sk_u32>>16) & 0xFF, (sk_u32>>24) & 0xFF]
    ml = pl[1]; mh = pl[3]
    msg = [ml, mh]
    enc = pl[4:]
    plain = bytearray(len(enc))
    for j in range(len(enc)):
        abs_i = j + 8
        plain[j] = ((enc[j] ^ sk[abs_i%4] ^ TABLE[abs_i%7]) - msg[abs_i%2]*17) & 0xFF
    return bytes(plain)

# Use the fresh gather PCAP
pcap_path = Path(r'D:\CascadeProjects\gather_fresh.pcap')
if not pcap_path.exists():
    # Try another PCAP with gather
    pcap_path = Path(r'D:\CascadeProjects\PCAPdroid_27_Mar_09_17_04.pcap')

print(f"Analyzing: {pcap_path.name}")
events = read_pcap_ordered(pcap_path)
sk = extract_sk(events)
print(f"Server key: 0x{sk:08X}")
print(f"Total events: {len(events)}")

# Find 0x0CE8 (START_MARCH) and show context
gather_opcodes = {0x0CE8, 0x033E, 0x033F, 0x006E, 0x0076, 0x0077, 0x0CEB, 0x0071, 0x076C, 0x00B8, 0x0037, 0x06C2, 0x00AA, 0x0323, 0x0767, 0x0769}

first_ts = events[0][0] if events else 0
print(f"\nAll gather-related packets:")
print(f"{'Time':>8} {'Dir':>3} {'Op':>6} {'Size':>5} {'Details'}")
print("-" * 100)

for ts, d, op, raw in events:
    if op in gather_opcodes or op == 0x1B8B:
        t = ts - first_ts
        details = ""

        if op == 0x033E and d == 'C2S':
            pl = raw[4:]
            details = f"SEARCH req: {pl.hex()}"
        elif op == 0x033F and d == 'S2C':
            pl = raw[4:]
            if len(pl) >= 5:
                rtype = pl[0]
                tx = struct.unpack('<H', pl[1:3])[0]
                ty = struct.unpack('<H', pl[3:5])[0]
                details = f"SEARCH result: type={rtype} ({tx},{ty})"
                if len(pl) > 5:
                    details += f" extra={pl[5:min(20,len(pl))].hex()}"
        elif op == 0x006E and d == 'C2S':
            pl = raw[4:]
            if len(pl) >= 5:
                vx = struct.unpack('<H', pl[0:2])[0]
                vy = struct.unpack('<H', pl[2:4])[0]
                details = f"VIEW ({vx},{vy}) flag={pl[4]}"
        elif op == 0x0CE8:
            if d == 'C2S' and sk:
                plain = decrypt_cmsg(raw, sk)
                if plain:
                    slot = plain[0]
                    mt = struct.unpack('<H', plain[4:6])[0]
                    tx = struct.unpack('<H', plain[9:11])[0]
                    ty = struct.unpack('<H', plain[11:13])[0]
                    hero = plain[14]
                    kingdom = plain[18]
                    purpose = plain[22]
                    igg = struct.unpack('<I', plain[33:37])[0]
                    details = f"MARCH: slot={slot} type=0x{mt:04X} ({tx},{ty}) hero={hero} k={kingdom} purpose={purpose} igg={igg}"
                    details += f"\n           plain={plain.hex()}"
        elif op == 0x0CEB:
            if d == 'C2S' and sk:
                plain = decrypt_cmsg(raw, sk)
                if plain:
                    details = f"ENABLE_VIEW: {plain.hex()}"
        elif op == 0x0071:
            details = f"MARCH_STATE ({len(raw)-4}B)"
        elif op == 0x076C:
            details = f"MARCH_START ({len(raw)-4}B)"
        elif op == 0x00B8:
            details = f"ACK: {raw[4:].hex()}"
        elif op == 0x0037:
            pl = raw[4:]
            if len(pl) >= 12:
                sub = pl[0]
                id_val = struct.unpack('<I', pl[4:8])[0]
                status = struct.unpack('<I', pl[8:12])[0]
                details = f"STATUS: sub=0x{sub:02X} id=0x{id_val:08X} status={status}"
        elif op == 0x0323:
            if d == 'C2S':
                details = f"PRE_MARCH: {raw[4:].hex()}"
        elif op == 0x06C2:
            details = f"SOLDIER_INFO ({len(raw)-4}B)"
        elif op == 0x00AA:
            details = f"HERO_INFO ({len(raw)-4}B)"
        elif op == 0x1B8B:
            if d == 'C2S':
                details = f"PASSWORD_CHECK: {raw[4:].hex()}"

        print(f"{t:8.3f} {d:>3} 0x{op:04X} {len(raw):5d} {details}")

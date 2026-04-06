#!/usr/bin/env python3
"""
49_decode_soldiers_heroes_chat.py - Fix soldier parsing, decode chat, analyze hero entries
"""
import struct, os, glob, sys

PCAP_DIR = r"D:\CascadeProjects"

out = []
def p(msg):
    out.append(msg)
    try: print(msg)
    except: print(msg.encode('ascii','replace').decode())

def read_all_packets(pcap_path):
    packets = []
    try:
        with open(pcap_path, 'rb') as f:
            magic = f.read(4)
            endian = '<' if magic == b'\xd4\xc3\xb2\xa1' else '>'
            rest = f.read(20)
            network = struct.unpack(endian + 'I', rest[16:20])[0]
            tcp_streams = {}
            while True:
                hdr = f.read(16)
                if len(hdr) < 16: break
                ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
                pkt = f.read(incl_len)
                if len(pkt) < incl_len: break
                if network == 101: ip_start = 0
                elif network == 113: ip_start = 16
                else:
                    if len(pkt) < 14: continue
                    if struct.unpack('>H', pkt[12:14])[0] != 0x0800: continue
                    ip_start = 14
                if ip_start + 20 > len(pkt): continue
                ip_hdr_len = (pkt[ip_start] & 0x0F) * 4
                if pkt[ip_start + 9] != 6: continue
                tcp_start = ip_start + ip_hdr_len
                if tcp_start + 20 > len(pkt): continue
                sp = struct.unpack('>H', pkt[tcp_start:tcp_start+2])[0]
                dp = struct.unpack('>H', pkt[tcp_start+2:tcp_start+4])[0]
                tcp_hdr_len = ((pkt[tcp_start + 12] >> 4) & 0xF) * 4
                payload = pkt[tcp_start + tcp_hdr_len:]
                if not payload: continue
                key = (sp, dp)
                if key not in tcp_streams:
                    tcp_streams[key] = bytearray()
                tcp_streams[key] += payload
            for (sp, dp), buf in tcp_streams.items():
                pos = 0
                while pos + 4 <= len(buf):
                    pkt_len = struct.unpack('<H', buf[pos:pos+2])[0]
                    opcode = struct.unpack('<H', buf[pos+2:pos+4])[0]
                    if pkt_len < 4 or pkt_len > 65000:
                        pos += 1; continue
                    if pos + pkt_len > len(buf): break
                    payload = bytes(buf[pos+4:pos+pkt_len])
                    packets.append((opcode, payload, sp, dp))
                    pos += pkt_len
    except: pass
    return packets

pcaps = glob.glob(os.path.join(PCAP_DIR, "*.pcap")) + \
        glob.glob(os.path.join(PCAP_DIR, "codex_lab", "*.pcap"))

all_pkts = []
for pf in pcaps[:10]:
    all_pkts.extend(read_all_packets(pf))

p(f"Total packets: {len(all_pkts)}")

# ═══════════════════════════════════════════════════════════════
# 1. SOLDIER_INFO - Try all possible entry sizes
# ═══════════════════════════════════════════════════════════════
p(f"\n{'='*60}")
p("SOLDIER_INFO (0x06C2) - All Occurrences")
p("=" * 60)

soldier_pkts = [(op, pay, sp, dp) for op, pay, sp, dp in all_pkts if op == 0x06C2 and len(pay) >= 8]
p(f"  Found {len(soldier_pkts)} 0x06C2 packets")

for idx, (op, payload, sp, dp) in enumerate(soldier_pkts[:5]):
    num = struct.unpack('<I', payload[0:4])[0]
    remaining = len(payload) - 4
    entry_size = remaining // num if num > 0 else 0
    p(f"\n  Packet {idx+1}: len={len(payload)}, count={num}, remaining={remaining}, entry_size={entry_size}")

    if entry_size == 0:
        continue

    for i in range(min(num, 8)):
        start = 4 + i * entry_size
        e = payload[start:start+entry_size]
        if len(e) < entry_size:
            break
        p(f"    Entry {i+1} ({entry_size}B): {e.hex()}")

        if entry_size == 14:
            # u32 type, u16 count, u32 extra1, u32 extra2
            t = struct.unpack('<I', e[0:4])[0]
            c = struct.unpack('<H', e[4:6])[0]
            e1 = struct.unpack('<I', e[6:10])[0]
            e2 = struct.unpack('<I', e[10:14])[0]
            p(f"      [14B] type={t}, count={c}, extra1={e1}, extra2={e2}")

            # Alt: u32 type, u16 tier, u32 count_u32, u32 extra
            t2 = struct.unpack('<I', e[0:4])[0]
            tier = struct.unpack('<H', e[4:6])[0]
            cnt = struct.unpack('<I', e[6:10])[0]
            ex = struct.unpack('<I', e[10:14])[0]
            p(f"      [14B alt] type={t2}, tier={tier}, count32={cnt}, extra={ex}")

        elif entry_size == 27:
            # Maybe it's variable - try sub-parsing
            # First try: two 14-byte sub-entries (misaligned)
            # Or: u32 type, u16 count, u16 tier, u32 alive, u32 wounded, u32 training, u32 queued, u8 state
            t = struct.unpack('<I', e[0:4])[0]
            f1 = struct.unpack('<H', e[4:6])[0]
            f2 = struct.unpack('<H', e[6:8])[0]
            f3 = struct.unpack('<I', e[8:12])[0]
            f4 = struct.unpack('<I', e[12:16])[0]
            f5 = struct.unpack('<I', e[16:20])[0]
            f6 = struct.unpack('<H', e[20:22])[0]
            f7 = struct.unpack('<I', e[22:26])[0]
            f8 = e[26]
            p(f"      [27B] type={t}, f1={f1}, f2={f2}, f3={f3}, f4={f4}, f5={f5}, f6={f6}, f7={f7}, f8={f8}")

# ═══════════════════════════════════════════════════════════════
# 2. HERO_INFO - Detailed field mapping
# ═══════════════════════════════════════════════════════════════
p(f"\n\n{'='*60}")
p("HERO_INFO (0x00AA) - Detailed Field Mapping")
p("=" * 60)

hero_pkts = [(op, pay, sp, dp) for op, pay, sp, dp in all_pkts if op == 0x00AA and len(pay) > 50]
p(f"  Found {len(hero_pkts)} 0x00AA packets")

for idx, (op, payload, sp, dp) in enumerate(hero_pkts[:3]):
    num = struct.unpack('<I', payload[0:4])[0]
    remaining = len(payload) - 4
    entry_size = remaining // num if num > 0 else 0
    p(f"\n  Packet {idx+1}: len={len(payload)}, heroes={num}, entry_size={entry_size}")

    for i in range(min(num, 5)):
        start = 4 + i * entry_size
        e = payload[start:start+entry_size]
        if len(e) < 4:
            break

        hero_id = struct.unpack('<I', e[0:4])[0]
        p(f"\n    Hero {i+1} (id={hero_id}):")

        # Dump all u32 non-zero
        p(f"      Non-zero u32 fields:")
        for j in range(0, min(entry_size, 109), 4):
            if j + 4 <= len(e):
                v = struct.unpack('<I', e[j:j+4])[0]
                if v != 0:
                    p(f"        [{j:3d}]: {v:10d} (0x{v:08X})")

        # First 20 bytes detailed
        if len(e) >= 20:
            hero_id = struct.unpack('<I', e[0:4])[0]
            f2 = struct.unpack('<I', e[4:8])[0]
            f3 = e[8]
            f4 = struct.unpack('<I', e[9:13])[0]
            f5 = struct.unpack('<I', e[13:17])[0]
            f6 = struct.unpack('<I', e[17:21])[0] if len(e) >= 21 else 0
            p(f"      hero_id={hero_id}, level_or_exp={f2}, star_or_flag={f3}")
            p(f"      field4={f4}, field5={f5}, field6={f6}")

# ═══════════════════════════════════════════════════════════════
# 3. CHAT_HISTORY (0x026D) - Decode messages
# ═══════════════════════════════════════════════════════════════
p(f"\n\n{'='*60}")
p("CHAT_HISTORY (0x026D) - Message Decoding")
p("=" * 60)

chat_pkts = [(op, pay, sp, dp) for op, pay, sp, dp in all_pkts if op == 0x026D]
p(f"  Found {len(chat_pkts)} chat packets")

# Analyze header pattern
p(f"\n  First 30 bytes of each (looking for header structure):")
for idx, (op, payload, sp, dp) in enumerate(chat_pkts[:10]):
    p(f"  [{idx+1}] len={len(payload):4d}: {payload[:30].hex()}")

# Pattern from data:
# All start with 0a00 or 0100
# 0a00 = channel 10 (kingdom chat?)
# 0100 = channel 1 (alliance chat?)
# Then: u16 at [2:4], then what appears to be a u32 timestamp at [4:8]

p(f"\n  Header analysis:")
for idx, (op, payload, sp, dp) in enumerate(chat_pkts[:10]):
    if len(payload) < 30:
        continue
    channel = struct.unpack('<H', payload[0:2])[0]
    count_or_id = struct.unpack('<H', payload[2:4])[0]
    # Next 8 bytes could be timestamp or castle_id
    ts_or_id = struct.unpack('<Q', payload[4:12])[0]
    # Could also be u32+u32
    val1 = struct.unpack('<I', payload[4:8])[0]
    val2 = struct.unpack('<I', payload[8:12])[0]
    p(f"  [{idx+1}] channel={channel}, count/id=0x{count_or_id:04X}, v1=0x{val1:08X}, v2=0x{val2:08X}")

# Try to find text in the payloads
p(f"\n  Searching for readable text in chat payloads:")
for idx, (op, payload, sp, dp) in enumerate(chat_pkts[:5]):
    # Find sequences of printable ASCII
    text_regions = []
    current = b''
    current_start = 0
    for i in range(len(payload)):
        b = payload[i]
        if 0x20 <= b < 0x7F:
            if not current:
                current_start = i
            current += bytes([b])
        else:
            if len(current) >= 3:
                text_regions.append((current_start, current.decode('ascii', errors='replace')))
            current = b''
    if len(current) >= 3:
        text_regions.append((current_start, current.decode('ascii', errors='replace')))

    if text_regions:
        p(f"\n  Chat {idx+1} (len={len(payload)}):")
        for off, txt in text_regions:
            p(f"    [{off:4d}] \"{txt}\"")

    # Also try UTF-8 decode of larger chunks
    # Chat messages in Arabic would be UTF-8
    for start_off in range(20, min(len(payload), 200)):
        try:
            chunk = payload[start_off:start_off+100]
            # Check for UTF-8 multibyte sequences (Arabic: 0xD8-0xDB start byte)
            if any(0xD8 <= b <= 0xDB for b in chunk[:5]):
                decoded = chunk.decode('utf-8', errors='ignore')
                if len(decoded) > 3:
                    p(f"    [{start_off:4d}] UTF-8: {decoded[:60]}")
                    break
        except:
            pass

# ═══════════════════════════════════════════════════════════════
# 4. Analyze 0x0033 (SYN_ATTRIBUTE) - Resource/stat sync
# ═══════════════════════════════════════════════════════════════
p(f"\n\n{'='*60}")
p("SYN_ATTRIBUTE (0x0033) - Resource Sync Messages")
p("=" * 60)

syn_pkts = [(op, pay, sp, dp) for op, pay, sp, dp in all_pkts if op == 0x0033]
p(f"  Found {len(syn_pkts)} SYN_ATTRIBUTE packets")

# Show size distribution
sizes = [len(pay) for op, pay, sp, dp in syn_pkts]
if sizes:
    p(f"  Size range: {min(sizes)}-{max(sizes)} bytes")
    size_counts = {}
    for s in sizes:
        size_counts[s] = size_counts.get(s, 0) + 1
    p(f"  Most common sizes:")
    for s, c in sorted(size_counts.items(), key=lambda x: -x[1])[:10]:
        p(f"    {s:4d} bytes: {c:3d}x")

# Parse first few
p(f"\n  First 10 packets:")
for idx, (op, payload, sp, dp) in enumerate(syn_pkts[:10]):
    p(f"  [{idx+1}] len={len(payload):3d}: {payload[:40].hex()}")

    # Try: u16 count, then (u16 attr_id, u64 value) pairs
    if len(payload) >= 2:
        count = struct.unpack('<H', payload[0:2])[0]
        p(f"    count(u16)={count}")
        pos = 2
        for i in range(min(count, 5)):
            if pos + 10 > len(payload):
                # Try shorter entries
                if pos + 6 <= len(payload):
                    attr = struct.unpack('<H', payload[pos:pos+2])[0]
                    val = struct.unpack('<I', payload[pos+2:pos+6])[0]
                    p(f"      attr=0x{attr:04X}, val={val} (4B)")
                    pos += 6
                break
            attr = struct.unpack('<H', payload[pos:pos+2])[0]
            val = struct.unpack('<Q', payload[pos+2:pos+10])[0]
            p(f"      attr=0x{attr:04X}, val={val}")
            pos += 10

# ═══════════════════════════════════════════════════════════════
# 5. Analyze 0x0043 (SERVER_TIME)
# ═══════════════════════════════════════════════════════════════
p(f"\n\n{'='*60}")
p("SERVER_TIME (0x0043)")
p("=" * 60)

time_pkts = [(op, pay, sp, dp) for op, pay, sp, dp in all_pkts if op == 0x0043]
p(f"  Found {len(time_pkts)} packets")
for idx, (op, payload, sp, dp) in enumerate(time_pkts[:5]):
    p(f"  [{idx+1}] len={len(payload)}: {payload.hex()}")
    if len(payload) >= 8:
        ts = struct.unpack('<Q', payload[0:8])[0]
        p(f"    timestamp_u64: {ts}")
    if len(payload) >= 4:
        ts32 = struct.unpack('<I', payload[0:4])[0]
        p(f"    timestamp_u32: {ts32}")
        # Unix timestamp interpretation
        import time
        try:
            p(f"    as unix time: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(ts32))}")
        except:
            pass

# ═══════════════════════════════════════════════════════════════
# 6. Analyze 0x0037 (unknown - possible error)
# ═══════════════════════════════════════════════════════════════
p(f"\n\n{'='*60}")
p("0x0037 UNKNOWN - Error/Status?")
p("=" * 60)

unk_pkts = [(op, pay, sp, dp) for op, pay, sp, dp in all_pkts if op == 0x0037]
p(f"  Found {len(unk_pkts)} 0x0037 packets")
for idx, (op, payload, sp, dp) in enumerate(unk_pkts[:10]):
    p(f"  [{idx+1}] len={len(payload)}: {payload.hex()}")
    if len(payload) >= 4:
        v1 = struct.unpack('<I', payload[0:4])[0]
        p(f"    u32[0]: {v1} (0x{v1:08X})")
    if len(payload) >= 8:
        v2 = struct.unpack('<I', payload[4:8])[0]
        p(f"    u32[4]: {v2} (0x{v2:08X})")

# ═══════════════════════════════════════════════════════════════
# 7. Analyze 0x00B8 (march ACK?)
# ═══════════════════════════════════════════════════════════════
p(f"\n\n{'='*60}")
p("0x00B8 - March ACK?")
p("=" * 60)

b8_pkts = [(op, pay, sp, dp) for op, pay, sp, dp in all_pkts if op == 0x00B8]
p(f"  Found {len(b8_pkts)} 0x00B8 packets")
for idx, (op, payload, sp, dp) in enumerate(b8_pkts[:10]):
    p(f"  [{idx+1}] len={len(payload)} src={sp}: {payload[:40].hex()}")

# ═══════════════════════════════════════════════════════════════
# 8. Find march-related opcodes: 0x0071, 0x006F
# ═══════════════════════════════════════════════════════════════
p(f"\n\n{'='*60}")
p("March-Related Opcodes Search")
p("=" * 60)

march_ops = [0x0071, 0x006F, 0x0070, 0x0072, 0x0073, 0x0074, 0x0075,
             0x00B8, 0x00B9, 0x00BA, 0x0CE8, 0x0CE9, 0x0CEA]
for target_op in march_ops:
    pkts = [(op, pay, sp, dp) for op, pay, sp, dp in all_pkts if op == target_op]
    if pkts:
        p(f"\n  0x{target_op:04X}: {len(pkts)} packets")
        for idx, (op, pay, sp, dp) in enumerate(pkts[:3]):
            p(f"    [{idx+1}] len={len(pay)} src={sp}: {pay[:30].hex()}")

# ═══════════════════════════════════════════════════════════════
# 9. Load opcode map and identify ALL packets
# ═══════════════════════════════════════════════════════════════
p(f"\n\n{'='*60}")
p("Full Opcode Coverage in PCAPs")
p("=" * 60)

sys.path.insert(0, r'D:\CascadeProjects\analysis\findings')
try:
    from cmsg_opcodes import CMSG_OPCODES
except:
    CMSG_OPCODES = {}

opcode_counts = {}
for op, payload, sp, dp in all_pkts:
    if op not in opcode_counts:
        opcode_counts[op] = 0
    opcode_counts[op] += 1

named = 0
unnamed = 0
p(f"\n  Top 60 opcodes by frequency:")
for op, count in sorted(opcode_counts.items(), key=lambda x: -x[1])[:60]:
    name = CMSG_OPCODES.get(op, "UNKNOWN")
    tag = "" if name != "UNKNOWN" else " <-- UNMAPPED"
    p(f"    0x{op:04X} ({name:45s}): {count:4d}x{tag}")
    if name != "UNKNOWN":
        named += 1
    else:
        unnamed += 1

p(f"\n  Named: {named}, Unnamed: {unnamed} (out of top 60)")
p(f"  Total unique opcodes in PCAPs: {len(opcode_counts)}")

# SAVE
with open(r'D:\CascadeProjects\analysis\findings\soldiers_heroes_chat.md', 'w', encoding='utf-8') as f:
    f.write("# Soldiers, Heroes, Chat, and Sync Decoding\n\n")
    f.write('\n'.join(out))

p(f"\nSaved to findings/soldiers_heroes_chat.md")

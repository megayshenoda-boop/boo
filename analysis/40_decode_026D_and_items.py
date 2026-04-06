#!/usr/bin/env python3
"""
40_decode_026D_and_items.py - Decode 0x026D (march response) and full item list
================================================================================
"""
import struct, os, glob, sys

PCAP_DIR = r"D:\CascadeProjects"

def read_all_packets(pcap_path, link_type=None):
    """Read all game packets from a PCAP."""
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

# Load all PCAPs
pcaps = glob.glob(os.path.join(PCAP_DIR, "*.pcap")) + \
        glob.glob(os.path.join(PCAP_DIR, "codex_lab", "*.pcap"))

all_pkts = []
for p_file in pcaps[:10]:
    pkts = read_all_packets(p_file)
    all_pkts.extend(pkts)

print(f"Total packets: {len(all_pkts)}")

out = []
def p(msg):
    out.append(msg)
    try: print(msg)
    except: print(msg.encode('ascii','replace').decode())

# ═══════════════════════════════════════════════════════════════
# 1. Decode 0x026D (march status/error)
# ═══════════════════════════════════════════════════════════════
p("=" * 60)
p("0x026D MARCH RESPONSE - All occurrences")
p("=" * 60)

count = 0
for op, payload, sp, dp in all_pkts:
    if op == 0x026D:
        count += 1
        if count <= 20:
            p(f"  [{count:2d}] len={len(payload):3d} src={sp} dst={dp}: {payload[:30].hex()}")

# Parse the structure
p(f"\n  Total 0x026D packets: {count}")
p(f"\n  Parsing first few:")
for op, payload, sp, dp in all_pkts:
    if op == 0x026D and len(payload) >= 4:
        # Try various formats
        if len(payload) >= 2:
            status = struct.unpack('<H', payload[0:2])[0]
        if len(payload) >= 4:
            val2 = struct.unpack('<H', payload[2:4])[0]
        if len(payload) >= 8:
            val3 = struct.unpack('<I', payload[4:8])[0]
        p(f"    status=0x{status:04X}, field2=0x{val2:04X}")
        break

# ═══════════════════════════════════════════════════════════════
# 2. Full ITEM_INFO (0x0064) decode
# ═══════════════════════════════════════════════════════════════
p(f"\n{'='*60}")
p("FULL ITEM_INFO (0x0064) Decode")
p("=" * 60)

for op, payload, sp, dp in all_pkts:
    if op == 0x0064 and len(payload) > 100:
        # First 4 bytes = item count
        num_items = struct.unpack('<I', payload[0:4])[0]
        p(f"  Item count: {num_items}")
        p(f"  Payload size: {len(payload)}")
        p(f"  Bytes per item: {(len(payload)-4)/max(num_items,1):.1f}")

        # Parse items as (u32 item_id, u32 count) = 8 bytes each
        pos = 4
        items = []
        for i in range(num_items):
            if pos + 8 > len(payload):
                break
            item_id = struct.unpack('<I', payload[pos:pos+4])[0]
            qty = struct.unpack('<I', payload[pos+4:pos+8])[0]
            items.append((item_id, qty))
            pos += 8

        p(f"  Parsed {len(items)} items:")
        for item_id, qty in items:
            p(f"    ID {item_id:5d} (0x{item_id:04X}): qty={qty}")
        break

# ═══════════════════════════════════════════════════════════════
# 3. Full SOLDIER_INFO decode
# ═══════════════════════════════════════════════════════════════
p(f"\n{'='*60}")
p("FULL SOLDIER_INFO (0x06C2) Decode")
p("=" * 60)

for op, payload, sp, dp in all_pkts:
    if op == 0x06C2 and len(payload) > 10:
        num = struct.unpack('<I', payload[0:4])[0]
        p(f"  Troop types: {num}")
        p(f"  Payload size: {len(payload)}")

        # Each entry might be variable. Let me try (u32 type, u16 tier, u16 count, ...) or
        # u32 type, u32 sub, u32 count = 12 bytes? (112-4)/4 = 27... nope
        # u32=4, then 4 entries * 27B = 108. 4+108=112. So 27B per entry.
        entry_size = (len(payload) - 4) // num if num > 0 else 0
        p(f"  Entry size: {entry_size}")

        pos = 4
        for i in range(num):
            if pos + entry_size > len(payload): break
            entry = payload[pos:pos+entry_size]
            p(f"  Troop {i+1}: {entry.hex()}")
            # Parse
            if entry_size >= 12:
                t1 = struct.unpack('<I', entry[0:4])[0]
                t2 = struct.unpack('<I', entry[4:8])[0]
                t3 = struct.unpack('<I', entry[8:12])[0]
                p(f"    field1={t1}, field2=0x{t2:08X}, field3={t3}")
            pos += entry_size
        break

# ═══════════════════════════════════════════════════════════════
# 4. Full HERO_INFO decode
# ═══════════════════════════════════════════════════════════════
p(f"\n{'='*60}")
p("FULL HERO_INFO (0x00AA) Decode")
p("=" * 60)

for op, payload, sp, dp in all_pkts:
    if op == 0x00AA and len(payload) > 10:
        num = struct.unpack('<I', payload[0:4])[0]
        p(f"  Hero count: {num}")
        p(f"  Payload size: {len(payload)}")
        entry_size = (len(payload) - 4) // num if num > 0 else 0
        p(f"  Entry size: {entry_size}")

        pos = 4
        for i in range(min(num, 5)):
            if pos + entry_size > len(payload): break
            entry = payload[pos:pos+entry_size]
            p(f"  Hero {i+1}: {entry[:40].hex()}...")
            # First u32 might be hero_id
            hero_id = struct.unpack('<I', entry[0:4])[0]
            p(f"    hero_id={hero_id}")
            pos += entry_size
        break

# ═══════════════════════════════════════════════════════════════
# 5. Full BUILDING_INFO decode
# ═══════════════════════════════════════════════════════════════
p(f"\n{'='*60}")
p("FULL BUILDING_INFO (0x0097) Decode")
p("=" * 60)

for op, payload, sp, dp in all_pkts:
    if op == 0x0097 and len(payload) > 10:
        num = struct.unpack('<H', payload[0:2])[0]
        p(f"  Building count (u16): {num}")
        p(f"  Payload size: {len(payload)}")
        entry_size = (len(payload) - 2) // num if num > 0 else 0
        p(f"  Entry size: {entry_size}")

        # 19 bytes per building: (610-2)/32 = 19
        pos = 2
        for i in range(min(num, 10)):
            if pos + entry_size > len(payload): break
            entry = payload[pos:pos+entry_size]
            p(f"  Building {i+1}: {entry.hex()}")
            if entry_size >= 6:
                slot = struct.unpack('<H', entry[0:2])[0]
                btype = struct.unpack('<H', entry[2:4])[0]
                level = struct.unpack('<H', entry[4:6])[0]
                p(f"    slot={slot}, type={btype}, level={level}")
            pos += entry_size
        break

# ═══════════════════════════════════════════════════════════════
# 6. Map 0x026D to opcode name from our map
# ═══════════════════════════════════════════════════════════════
p(f"\n{'='*60}")
p("0x026D Identification")
p("=" * 60)

# Check in our opcode map
try:
    sys.path.insert(0, r'D:\CascadeProjects\analysis\findings')
    from cmsg_opcodes import CMSG_OPCODES
    if 0x026D in CMSG_OPCODES:
        p(f"  0x026D = {CMSG_OPCODES[0x026D]}")
    else:
        p(f"  0x026D NOT in opcode map")
        # Check nearby
        for off in range(-3, 4):
            if (0x026D + off) in CMSG_OPCODES:
                p(f"  0x{0x026D+off:04X} = {CMSG_OPCODES[0x026D+off]}")
except Exception as e:
    p(f"  Error loading map: {e}")

# SAVE
with open(r'D:\CascadeProjects\analysis\findings\game_data_decoded.md', 'w', encoding='utf-8') as f:
    f.write("# Decoded Game Data\n\n")
    f.write('\n'.join(out))

p(f"\nSaved to findings/game_data_decoded.md")

#!/usr/bin/env python3
"""
38_pcap_item_ids.py - Extract game IDs from PCAPs
==================================================
Parse server responses to find actual item IDs, reward IDs, building IDs etc.
Focus on 0x0064 (ITEM_INFO), 0x0097 (BUILDING_INFO), 0x00BE (SCIENCE_INFO),
0x06C2 (SOLDIER_INFO), 0x00AA (HERO_INFO), 0x0038 (CASTLE_DATA).
"""
import struct, os, glob, sys

PCAP_DIR = r"D:\CascadeProjects"

out = []
def p(msg):
    out.append(msg)
    try: print(msg)
    except: print(msg.encode('ascii','replace').decode())

def read_pcap_packets(path, direction='server'):
    """Read packets from PCAP. Returns list of (opcode, payload) tuples."""
    packets = []
    try:
        with open(path, 'rb') as f:
            magic = f.read(4)
            if magic == b'\xd4\xc3\xb2\xa1':
                endian = '<'
            elif magic == b'\xa1\xb2\xc3\xd4':
                endian = '>'
            else:
                return packets

            rest_hdr = f.read(20)
            network = struct.unpack(endian + 'I', rest_hdr[16:20])[0]
            # network: 1=Ethernet, 101=RAW_IP, 113=Linux_SLL

            tcp_buffers = {}  # (src_port, dst_port) -> bytes

            while True:
                pkt_hdr = f.read(16)
                if len(pkt_hdr) < 16:
                    break
                ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', pkt_hdr)
                pkt_data = f.read(incl_len)
                if len(pkt_data) < incl_len:
                    break

                # Determine IP start based on link type
                if network == 101:  # RAW_IP
                    ip_start = 0
                elif network == 113:  # Linux SLL
                    ip_start = 16
                else:  # Ethernet
                    if len(pkt_data) < 34:
                        continue
                    eth_type = struct.unpack('>H', pkt_data[12:14])[0]
                    if eth_type != 0x0800:
                        continue
                    ip_start = 14

                if ip_start >= len(pkt_data):
                    continue

                # Parse IP
                ip_hdr_len = (pkt_data[ip_start] & 0x0F) * 4
                ip_proto = pkt_data[ip_start + 9]
                if ip_proto != 6:  # TCP
                    continue

                # Parse TCP
                tcp_start = ip_start + ip_hdr_len
                if tcp_start + 20 > len(pkt_data):
                    continue
                src_port = struct.unpack('>H', pkt_data[tcp_start:tcp_start+2])[0]
                dst_port = struct.unpack('>H', pkt_data[tcp_start+2:tcp_start+4])[0]
                tcp_hdr_len = ((pkt_data[tcp_start + 12] >> 4) & 0xF) * 4
                tcp_payload = pkt_data[tcp_start + tcp_hdr_len:]

                if not tcp_payload:
                    continue

                # Determine direction: server sends from high port
                is_server = src_port > 5000 and dst_port > 5000
                # Actually: server port is the game server port (from config)
                # Just collect all TCP payloads and parse game packets from them
                key = (src_port, dst_port)
                if key not in tcp_buffers:
                    tcp_buffers[key] = bytearray()
                tcp_buffers[key] += tcp_payload

            # Parse game packets from each stream
            for (sp, dp), buf in tcp_buffers.items():
                # Server→client: server sends from game port
                if direction == 'server' and sp < 1000:
                    continue

                pos = 0
                while pos + 4 <= len(buf):
                    if pos + 4 > len(buf):
                        break
                    pkt_len = struct.unpack('<H', buf[pos:pos+2])[0]
                    opcode = struct.unpack('<H', buf[pos+2:pos+4])[0]

                    if pkt_len < 4 or pkt_len > 65000:
                        pos += 1
                        continue

                    if pos + pkt_len > len(buf):
                        break

                    payload = buf[pos+4:pos+pkt_len]
                    packets.append((opcode, payload, sp, dp))
                    pos += pkt_len

    except Exception as e:
        pass

    return packets

# Find all PCAPs
pcap_files = glob.glob(os.path.join(PCAP_DIR, "*.pcap")) + \
             glob.glob(os.path.join(PCAP_DIR, "codex_lab", "*.pcap")) + \
             glob.glob(os.path.join(PCAP_DIR, "*.pcapng"))

p(f"Found {len(pcap_files)} PCAP files in {PCAP_DIR}")

# Collect packets from all PCAPs
all_packets = []
for f in pcap_files[:5]:  # Limit to first 5
    pkts = read_pcap_packets(f)
    p(f"  {os.path.basename(f)}: {len(pkts)} packets")
    all_packets.extend(pkts)

p(f"\nTotal packets: {len(all_packets)}")

# Count opcodes
opcode_counts = {}
for op, payload, sp, dp in all_packets:
    opcode_counts[op] = opcode_counts.get(op, 0) + 1

p(f"\n## Opcode Frequency (top 50):")
for op, count in sorted(opcode_counts.items(), key=lambda x: -x[1])[:50]:
    p(f"  0x{op:04X}: {count:4d} packets")

# ═══════════════════════════════════════════════════════════════
# Analyze specific opcodes
# ═══════════════════════════════════════════════════════════════

# 0x0064 = ITEM_INFO - parse item IDs
p(f"\n\n## Item Info (0x0064) Payloads:")
for op, payload, sp, dp in all_packets:
    if op == 0x0064 and len(payload) >= 4:
        # Try to extract item entries
        p(f"  len={len(payload)}: {payload[:40].hex()}")
        break  # Just first one for now

# 0x0097 = BUILDING_INFO
p(f"\n## Building Info (0x0097) Payloads:")
for op, payload, sp, dp in all_packets:
    if op == 0x0097 and len(payload) >= 4:
        p(f"  len={len(payload)}: {payload[:60].hex()}")
        break

# 0x0038 = CASTLE_DATA (EXTRA_ATTRIBUTE_INFO)
p(f"\n## Castle Data (0x0038) Payloads:")
count = 0
for op, payload, sp, dp in all_packets:
    if op == 0x0038 and len(payload) >= 4:
        p(f"  len={len(payload)}: {payload[:60].hex()}")
        count += 1
        if count >= 3:
            break

# 0x06C2 = SOLDIER_INFO
p(f"\n## Soldier Info (0x06C2) Payloads:")
for op, payload, sp, dp in all_packets:
    if op == 0x06C2 and len(payload) >= 4:
        p(f"  len={len(payload)}: {payload[:60].hex()}")
        break

# 0x00AA = HERO_INFO
p(f"\n## Hero Info (0x00AA) Payloads:")
for op, payload, sp, dp in all_packets:
    if op == 0x00AA and len(payload) >= 4:
        p(f"  len={len(payload)}: {payload[:60].hex()}")
        break

# 0x006F = SYNC_MARCH
p(f"\n## March Sync (0x006F) Payloads:")
count = 0
for op, payload, sp, dp in all_packets:
    if op == 0x006F and len(payload) >= 4:
        p(f"  len={len(payload)}: {payload[:80].hex()}")
        count += 1
        if count >= 3:
            break

# 0x0CE8 = START_MARCH_NEW (client sent)
p(f"\n## START_MARCH_NEW (0x0CE8) Client Payloads (encrypted):")
count = 0
for op, payload, sp, dp in all_packets:
    if op == 0x0CE8:
        p(f"  len={len(payload)} src={sp} dst={dp}: {payload[:80].hex()}")
        count += 1
        if count >= 5:
            break

# 0x0323 = HERO_RECRUIT
p(f"\n## HERO_RECRUIT (0x0323) Payloads:")
count = 0
for op, payload, sp, dp in all_packets:
    if op == 0x0323:
        p(f"  len={len(payload)} src={sp} dst={dp}: {payload.hex()}")
        count += 1
        if count >= 5:
            break

# Any 0x1B8B = PASSWORD_CHECK
p(f"\n## PASSWORD_CHECK (0x1B8B) Payloads:")
count = 0
for op, payload, sp, dp in all_packets:
    if op == 0x1B8B:
        p(f"  len={len(payload)} src={sp} dst={dp}: {payload[:40].hex()}")
        count += 1
        if count >= 5:
            break

# Save
with open(r'D:\CascadeProjects\analysis\findings\pcap_analysis.md', 'w', encoding='utf-8') as f:
    f.write("# PCAP Data Analysis\n\n")
    f.write('\n'.join(out))

p(f"\nSaved to findings/pcap_analysis.md")

"""Verify: does ARM64 packData layout match PCAP plaintext?
If not, the binary version may be outdated."""
import struct

# All PCAP decoded plaintexts for 0x0CE8 (from gather_pcap_output.txt)
pcap_plains = [
    bytes.fromhex("01f8fcde49170000002602530301ff000000b60000000400000000000000000000ed027322000000000000000000"),
    bytes.fromhex("0109d5de49170000005302550301ff000000b60000000400000000000000000000ed027322000000000000000000"),
    bytes.fromhex("016014f049170000003a02250301ff000000b60000000400000000000000000000ed027322000000000000000000"),
    bytes.fromhex("017f93f7491700000039026a0301e2000000b60000000400000000000000000000ed027322000000000000000000"),
]

print("="*80)
print("LAYOUT COMPARISON: PCAP (working) vs ARM64 (from binary)")
print("="*80)

for i, p in enumerate(pcap_plains):
    print(f"\n--- PCAP Session {i+1} ({len(p)}B) ---")
    
    # My working PCAP-derived layout
    print("\n  [PCAP layout - WORKS]:")
    print(f"    [0]     slot       = {p[0]}")
    print(f"    [1:4]   nonce      = {p[1:4].hex()}")
    print(f"    [4:6]   march_type = 0x{struct.unpack('<H', p[4:6])[0]:04X}")
    print(f"    [9:11]  tile_x     = {struct.unpack('<H', p[9:11])[0]}")
    print(f"    [11:13] tile_y     = {struct.unpack('<H', p[11:13])[0]}")
    print(f"    [13]    flag       = {p[13]}")
    print(f"    [14]    hero_id    = {p[14]} (0x{p[14]:02X})")
    print(f"    [18]    kingdom    = {p[18]}")
    print(f"    [22]    purpose    = {p[22]}")
    print(f"    [33:37] igg_id     = {struct.unpack('<I', p[33:37])[0]}")
    
    # ARM64 layout from march_payload_format.md
    print("\n  [ARM64 layout - from binary analysis]:")
    sub_type = struct.unpack('<H', p[0:2])[0]
    march_type = struct.unpack('<H', p[2:4])[0]
    print(f"    [0:2]   sub_type   = 0x{sub_type:04X} = {sub_type}")
    print(f"    [2:4]   march_type = 0x{march_type:04X} = {march_type}")
    print(f"    [4:9]   flags      = {p[4:9].hex()}")
    if len(p) >= 17:
        tx = struct.unpack('<I', p[9:13])[0]
        ty = struct.unpack('<I', p[13:17])[0]
        print(f"    [9:13]  target_x   = {tx}")
        print(f"    [13:17] target_y   = {ty}")
    if len(p) >= 19:
        kingdom = struct.unpack('<H', p[17:19])[0]
        print(f"    [17:19] kingdom    = {kingdom}")
    if len(p) >= 21:
        slot = struct.unpack('<H', p[19:21])[0]
        print(f"    [19:21] slot       = {slot}")
    print(f"    [21]    arr_count  = {p[21]}")

print("\n" + "="*80)
print("CONCLUSION:")
print("="*80)
print("""
PCAP layout gives correct values:
  - march_type = 0x1749 (gather)
  - tile coords = 550,851 or similar valid coords
  - kingdom = 182
  - hero_id = 0xFF or 0xE2 (226)

ARM64 layout gives WRONG values:
  - sub_type = 0xF801 (nonsense)
  - march_type = 0xDEFC (nonsense)
  - flags = random-looking
  - coords as u32 are meaningless

This means the binary's packData analysis does NOT match the wire format.
Possible causes:
  1. The analysis script misidentified the write order
  2. The binary version doesn't match the server version
  3. The packData function has been modified between versions
""")

# Also check: what version might the binary be from?
print("\nPCAP march_type = 0x1749:")
print(f"  Binary has CMSG_START_MARCH_NEW at 0x05212294")
print(f"  Binary has CMSG_START_MARCH_EX at 0x05212ADC (NEWER!)")
print(f"  If server expects CMSG_START_MARCH_EX, our 0x0CE8 might be outdated")
print(f"  But 0x0CE8 DOES get 0x00B8+0x00B9 responses, so it still works")
print(f"  Hero assignment might use the EX version's format")

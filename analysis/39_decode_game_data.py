#!/usr/bin/env python3
"""
39_decode_game_data.py - Decode game state from PCAP server responses
=====================================================================
Parse the actual field values from key server messages.
"""
import struct, os, glob, sys

out = []
def p(msg):
    out.append(msg)
    try: print(msg)
    except: print(msg.encode('ascii','replace').decode())

# ═══════════════════════════════════════════════════════════════
# Parse ITEM_INFO (0x0064)
# ═══════════════════════════════════════════════════════════════
p("=" * 60)
p("ITEM_INFO (0x0064) Parsing")
p("=" * 60)

item_payload = bytes.fromhex('a8000000c900000028000000cb00000001000000cd00000003000000ce00000052000000d1000000')
# Extended from PCAP - 1348 bytes total, this is just first 40 bytes
# Pattern seems to be: u32 entries, then per-entry data

# First 4 bytes = number of items? 0x000000A8 = 168 items
num_items = struct.unpack('<I', item_payload[0:4])[0]
p(f"  Number of items: {num_items}")
p(f"  Remaining bytes: {len(item_payload) - 4}")
p(f"  Bytes per item (if fixed): {(len(item_payload) - 4) / max(num_items, 1):.1f}")

# Try parsing as pairs: (item_id u32, count u32)
p(f"  First few entries as (id, count) pairs:")
pos = 4
for i in range(min(5, (len(item_payload)-4)//8)):
    item_id = struct.unpack('<I', item_payload[pos:pos+4])[0]
    count = struct.unpack('<I', item_payload[pos+4:pos+8])[0]
    p(f"    Item {item_id} (0x{item_id:04X}): qty={count}")
    pos += 8

# ═══════════════════════════════════════════════════════════════
# Parse BUILDING_INFO (0x0097)
# ═══════════════════════════════════════════════════════════════
p(f"\n{'='*60}")
p("BUILDING_INFO (0x0097) Parsing")
p("=" * 60)

bld_payload = bytes.fromhex('200001000100080000000000000000000000000000020002000700000000000000000000000000000300030001000000000000000000000000000004')
# 0x20 = 32 buildings?
num_bld = struct.unpack('<H', bld_payload[0:2])[0]
p(f"  First u16: {num_bld} (0x{num_bld:04X})")

# Try different parsing strategies
p(f"  Raw hex dump (60B):")
for i in range(0, min(60, len(bld_payload)), 20):
    chunk = bld_payload[i:i+20]
    hex_str = ' '.join(f'{b:02x}' for b in chunk)
    p(f"    [{i:3d}] {hex_str}")

# It looks like: u16 count, then per building:
# bytes [2:4] = 0x0001 = slot_id?
# bytes [4:6] = 0x0001 = building_type?
# bytes [6:8] = 0x0008 = level?
# Pattern: 2+2+2+2+4+4 = 16 bytes per building?
p(f"\n  Try 14-byte building entries:")
pos = 2
entry_idx = 0
while pos + 14 <= len(bld_payload) and entry_idx < 5:
    slot = struct.unpack('<H', bld_payload[pos:pos+2])[0]
    btype = struct.unpack('<H', bld_payload[pos+2:pos+4])[0]
    level = struct.unpack('<H', bld_payload[pos+4:pos+6])[0]
    rest = bld_payload[pos+6:pos+14].hex()
    p(f"    slot={slot}, type={btype}, level={level}, rest={rest}")
    pos += 14
    entry_idx += 1

# ═══════════════════════════════════════════════════════════════
# Parse CASTLE_DATA (0x0038) - contains server_key!
# ═══════════════════════════════════════════════════════════════
p(f"\n{'='*60}")
p("CASTLE_DATA (0x0038) Parsing")
p("=" * 60)

castle_hex = '4500020000007a010000000000000300000000000000000000000500000001000000000000000c00000070170000000000000d000000f31e00000000'
castle_payload = bytes.fromhex(castle_hex)

# This is CMSG_EXTRA_ATTRIBUTE_INFO - contains field_id, value pairs
# Format: u16 count, then per field: u8 field_id, varies value
# But actually from previous analysis: field 0x4F = server key

p(f"  Total length: {len(castle_payload)}")
# First byte might be count
first = castle_payload[0]
p(f"  First byte: 0x{first:02X} ({first})")

# Try: u8 count, then (u8 field_id, u32 value) pairs
count = first  # 0x45 = 69 entries
p(f"  Entries (if u8 count): {count}")
p(f"  Bytes for entries: {len(castle_payload) - 1}")
p(f"  Bytes per entry: {(len(castle_payload) - 1) / max(count, 1):.1f}")

# 12 bytes per entry: (830-1)/69 = 12.01 -> 12 bytes per entry!
p(f"\n  Parsing as 12-byte entries (field_id u8 + type u8 + value up to 10B):")
# Actually let's try: u16 field_id + value
# Or maybe: tag-length-value

# From memory: the 0x0038 packet has field 0x4F = server_key
# Let's just dump looking for 0x4F
p(f"\n  Searching for field 0x4F (server_key):")
for i in range(len(castle_payload)):
    if castle_payload[i] == 0x4F:
        context = castle_payload[max(0,i-4):i+12]
        p(f"    Found 0x4F at offset {i}: ...{context.hex()}")

# Let's try: 1-byte count at offset 0, then TLV: u8 field_id, u8 type, then value
# type 0=u32, type 2=u16, etc?
pos = 0
# Actually re-read: 0x45 0x00 0x02 0x00 0x00...
# Could be: u16 count = 0x0045 = 69
count = struct.unpack('<H', castle_payload[0:2])[0]
p(f"\n  u16 count = {count}")
# Then 2 bytes type? 0x0002 at offset 2
p(f"  Next u16 = 0x{struct.unpack('<H', castle_payload[2:4])[0]:04X}")

# Let's try: u8 num_entries, u8 padding, then entries
# Entry format from game_state.py analysis
p(f"\n  Dumping as (u16 field_id, u32 low, u32 high) = 10B entries:")
pos = 2  # skip first u16
entry_idx = 0
while pos + 10 <= len(castle_payload) and entry_idx < 15:
    fid = struct.unpack('<H', castle_payload[pos:pos+2])[0]
    val_lo = struct.unpack('<I', castle_payload[pos+2:pos+6])[0]
    val_hi = struct.unpack('<I', castle_payload[pos+6:pos+10])[0]
    if fid < 0x100:
        val = val_lo | (val_hi << 32)
        p(f"    field 0x{fid:02X}: {val} (lo=0x{val_lo:08X}, hi=0x{val_hi:08X})")
    pos += 10
    entry_idx += 1

# Try 12-byte entries
p(f"\n  Dumping as 12B entries (u8 fid, u8 ?, u16 ?, u32 val_lo, u32 val_hi):")
pos = 1  # skip first byte
entry_idx = 0
while pos + 12 <= len(castle_payload) and entry_idx < 10:
    fid = castle_payload[pos]
    extra1 = castle_payload[pos+1]
    extra2 = struct.unpack('<H', castle_payload[pos+2:pos+4])[0]
    val_lo = struct.unpack('<I', castle_payload[pos+4:pos+8])[0]
    val_hi = struct.unpack('<I', castle_payload[pos+8:pos+12])[0]
    if fid < 0x100 and extra1 < 0x10:
        p(f"    field 0x{fid:02X}: type={extra1}, sub={extra2}, val={val_lo} ({val_hi})")
    pos += 12
    entry_idx += 1

# ═══════════════════════════════════════════════════════════════
# Parse SOLDIER_INFO (0x06C2)
# ═══════════════════════════════════════════════════════════════
p(f"\n{'='*60}")
p("SOLDIER_INFO (0x06C2) Parsing")
p("=" * 60)

soldier_hex = '04000000010000000200f828000000000000020000000200301c000000000000040000000100a83f000000000000080000000100ce41000000000000'
soldier_payload = bytes.fromhex(soldier_hex)

# First u32 = count = 4
num_soldiers = struct.unpack('<I', soldier_payload[0:4])[0]
p(f"  Soldier types: {num_soldiers}")

# Each entry - try different sizes
# (112 - 4) / 4 = 27 bytes? not clean. Try from hex:
# Entry 1: 01000000 0200 f828000000000000
# Entry 2: 02000000 0200 301c000000000000
# = u32 type_id, u16 tier?, u16 count, u32 ?, u32 ?
# Actually: 01000000 02 00 f828 0000 00000000
# type=1, ?, ?, count?, ...

# Let's try 14-byte entries: (112-4)/4 = 27... not clean
# Try: u32 type, u32 count, u32 ?, u32 ? = 16 bytes? (112-4)/4 = 27 nope
# 04000000 | 01000000 0200 f828 00000000 0000 | 02000000 ...
# entry = 14 bytes? (112-4)/4 = 27...
# Actually maybe each entry is different size

# Let's just dump as u32 pairs
p(f"  Raw u32 dump:")
for i in range(0, len(soldier_payload), 4):
    val = struct.unpack('<I', soldier_payload[i:i+4])[0]
    p(f"    [{i:3d}] 0x{val:08X} = {val}")

# ═══════════════════════════════════════════════════════════════
# Parse HERO_RECRUIT (0x0323) payload
# ═══════════════════════════════════════════════════════════════
p(f"\n{'='*60}")
p("HERO_RECRUIT (0x0323) Parsing")
p("=" * 60)

recruit_hex = '000200c9000000ce000000'
recruit_payload = bytes.fromhex(recruit_hex)
p(f"  Length: {len(recruit_payload)}")
p(f"  Raw: {recruit_hex}")

# Parse as fields
p(f"  u16[0]: {struct.unpack('<H', recruit_payload[0:2])[0]} (0x{struct.unpack('<H', recruit_payload[0:2])[0]:04X})")
p(f"  u8[2]: {recruit_payload[2]} (0x{recruit_payload[2]:02X})")
p(f"  u32[3]: {struct.unpack('<I', recruit_payload[3:7])[0]} (0x{struct.unpack('<I', recruit_payload[3:7])[0]:08X})")
p(f"  u32[7]: {struct.unpack('<I', recruit_payload[7:11])[0]} (0x{struct.unpack('<I', recruit_payload[7:11])[0]:08X})")
# 0x0002, 0x02, 0x000000C9, 0x000000CE
# = slot=2?, count=2?, hero_id_1=201, hero_id_2=206?

# ═══════════════════════════════════════════════════════════════
# Analyze encrypted march payloads
# ═══════════════════════════════════════════════════════════════
p(f"\n{'='*60}")
p("START_MARCH_NEW (0x0CE8) - Encrypted payloads")
p("=" * 60)

marches = [
    bytes.fromhex('4c55e2b23630a2a2aaca8b580daf727b4533f760cecf3e2b8282d9a3785643ef35bac715e1f18b580d309baec2353c60cecfe82b8282'),
    bytes.fromhex('cf41f64ac3493e68dfe16e07f8789604b6cfd83f3b345b747779e5fc8dadaab0c041224a14376cb0da8294d3b3ced93f3b34'),
    bytes.fromhex('11f84fba472ee82e2b7791017e23692036992939bd62a472f12f1afa0bfb55b64617dd4c924193969cd46bd535982639bd62'),
]

for i, m in enumerate(marches):
    p(f"\n  March {i+1}: {len(m)} bytes")
    # First 4 bytes are crypto header: msg_lo, verify, sk_lo
    msg_lo = m[0]
    verify = m[1]
    sk_lo = m[2]
    p(f"    crypto: msg_lo=0x{msg_lo:02X}, verify=0x{verify:02X}, sk_lo=0x{sk_lo:02X}")
    p(f"    payload_len (encrypted): {len(m) - 4}")

# ═══════════════════════════════════════════════════════════════
# Look at interesting opcodes
# ═══════════════════════════════════════════════════════════════
p(f"\n{'='*60}")
p("KEY OPCODE OBSERVATIONS")
p("=" * 60)

opcode_names = {
    0x026D: "MARCH_ERROR/STATUS",
    0x0042: "HEARTBEAT",
    0x0001: "HEARTBEAT_ECHO",
    0x0033: "SYN_ATTRIBUTE",
    0x099D: "ACTION_EXCHAGE_COUNT?",
    0x099E: "COMMON_EXCHAGE_COUNT_RETURN",
    0x036C: "SERVER_TICK",
    0x0043: "SERVER_TIME",
    0x0078: "TILE_DATA?",
    0x0601: "UNKNOWN",
    0x009E: "BUILDING_OPERAT_RETURN",
    0x0077: "TILE_DETAIL?",
    0x007A: "MAP_DATA?",
    0x11F8: "UNKNOWN_HIGH",
    0x0CEB: "ENABLE_VIEW",
}

for op, name in sorted(opcode_names.items()):
    p(f"  0x{op:04X} = {name}")

p(f"\n  Note: 0x026D appears 66 times - this is likely the march ACK/error response")
p(f"  Note: 0x099D/0x099E appear 31 times each - exchange activity sync")

# SAVE
with open(r'D:\CascadeProjects\analysis\findings\game_data_decoded.md', 'w', encoding='utf-8') as f:
    f.write("# Decoded Game Data from PCAPs\n\n")
    f.write('\n'.join(out))

p(f"\nSaved to findings/game_data_decoded.md")

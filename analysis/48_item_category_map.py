#!/usr/bin/env python3
"""
48_item_category_map.py - Map item IDs to categories and decode soldier entries
===============================================================================
"""
import struct, os, glob, re, sys

LIBGAME = r"D:\CascadeProjects\libgame.so"
PCAP_DIR = r"D:\CascadeProjects"

with open(LIBGAME, "rb") as f:
    data = f.read()

out = []
def p(msg):
    out.append(msg)
    try: print(msg)
    except: print(msg.encode('ascii','replace').decode())

# ═══════════════════════════════════════════════════════════════
# 1. Item ID Category Map from .rodata strings
# ═══════════════════════════════════════════════════════════════
p("# Item & Game ID Analysis")
p("=" * 60)

# Search .rodata for item category strings
# .rodata is typically after .text
RODATA_OFF = 0x2560000  # approximate start of rodata
RODATA_SIZE = min(0x800000, len(data) - RODATA_OFF)

# Known item ID ranges from PCAP data:
# 201-247: low IDs (heroes? potions?)
# 400-424: medium items
# 520-577: resources?
# 620-626: resources?
# 653, 723, 732: misc
# 768, 902-970: equipment?
# 1000-1442: equipment/materials
# 2000-2560: special items
# 4024-4064: high tier items
# 6008-6202: very high items (hero shards?)
# 6603-6604: gear?
# 8562-8575: ultra high items
# 9150-9324: top tier

# Search for item-related strings in rodata
item_keywords = [
    b'speedup', b'speed_up', b'SpeedUp', b'SPEED_UP',
    b'resource', b'Resource', b'RESOURCE',
    b'equipment', b'Equipment', b'EQUIP',
    b'material', b'Material', b'MATERIAL',
    b'gem', b'Gem', b'GEM',
    b'shield', b'Shield', b'SHIELD',
    b'chest', b'Chest', b'CHEST',
    b'key', b'Key', b'KEY',
    b'boost', b'Boost', b'BOOST',
    b'item_type', b'ItemType', b'ITEM_TYPE',
    b'hero_shard', b'HeroShard',
    b'troop', b'Troop', b'TROOP',
    b'food', b'Food', b'FOOD',
    b'stone', b'Stone', b'STONE',
    b'wood', b'Wood', b'WOOD',
    b'ore', b'Ore', b'ORE',
    b'gold', b'Gold', b'GOLD',
    b'scroll', b'Scroll', b'SCROLL',
]

p("\n## Item-related strings in .rodata:")
for keyword in item_keywords:
    positions = []
    search_area = data[RODATA_OFF:RODATA_OFF + RODATA_SIZE]
    start = 0
    while True:
        pos = search_area.find(keyword, start)
        if pos == -1:
            break
        # Extract surrounding string
        str_start = pos
        while str_start > 0 and search_area[str_start-1] >= 0x20 and search_area[str_start-1] < 0x7F:
            str_start -= 1
        str_end = pos + len(keyword)
        while str_end < len(search_area) and search_area[str_end] >= 0x20 and search_area[str_end] < 0x7F:
            str_end += 1
        context = search_area[str_start:str_end].decode('ascii', errors='replace')
        if len(context) > 3 and len(context) < 200:
            positions.append((RODATA_OFF + pos, context))
        start = pos + 1
        if len(positions) > 10:
            break
    if positions:
        p(f"\n  '{keyword.decode()}':")
        for addr, ctx in positions[:5]:
            p(f"    0x{addr:08X}: {ctx}")

# ═══════════════════════════════════════════════════════════════
# 2. Find item_type enum in .rodata
# ═══════════════════════════════════════════════════════════════
p(f"\n\n{'='*60}")
p("Item Type Constants / Enums")
p("=" * 60)

# Search for sequences of small integers near item-related strings
# Also search for "type" in XML file names
xml_patterns = [
    b'item.xml', b'Item.xml', b'ItemConf', b'item_conf',
    b'equip.xml', b'Equip.xml', b'EquipConf',
    b'hero.xml', b'Hero.xml', b'HeroConf',
    b'soldier.xml', b'Soldier.xml', b'SoldierConf',
    b'building.xml', b'Building.xml', b'BuildConf',
    b'science.xml', b'Science.xml', b'ScienceConf',
    b'monster.xml', b'Monster.xml', b'MonsterConf',
    b'skill.xml', b'Skill.xml', b'SkillConf',
    b'buff.xml', b'Buff.xml', b'BuffConf',
    b'reward.xml', b'Reward.xml', b'RewardConf',
    b'vip.xml', b'Vip.xml', b'VipConf',
    b'map.xml', b'Map.xml', b'MapConf',
    b'quest.xml', b'Quest.xml', b'QuestConf',
    b'task.xml', b'Task.xml', b'TaskConf',
]

p("\n## XML Config references:")
for pattern in xml_patterns:
    pos = data.find(pattern)
    if pos != -1:
        # Get full string
        start = pos
        while start > 0 and data[start-1] >= 0x20 and data[start-1] < 0x7F:
            start -= 1
        end = pos + len(pattern)
        while end < len(data) and data[end] >= 0x20 and data[end] < 0x7F:
            end += 1
        full_str = data[start:end].decode('ascii', errors='replace')
        p(f"  0x{pos:08X}: {full_str}")

# ═══════════════════════════════════════════════════════════════
# 3. Decode SOLDIER_INFO properly
# ═══════════════════════════════════════════════════════════════
p(f"\n\n{'='*60}")
p("SOLDIER_INFO (0x06C2) - Proper Decoding")
p("=" * 60)

soldier_hex = '04000000010000000200f828000000000000020000000200301c000000000000040000000100a83f000000000000080000000100ce41000000000000'
soldier_payload = bytes.fromhex(soldier_hex)

num = struct.unpack('<I', soldier_payload[0:4])[0]
p(f"  Count: {num}")

# 27 bytes per entry. Let me try multiple parsing strategies:
strategies = [
    # Strategy A: u32 type, u16 tier, u16 count, u32 extra1, u32 extra2, u32 extra3, u8 flag
    ("A: u32+u16+u16+u32+u32+u32+u8+u16", "IHHIIIbH"),
    # Strategy B: u32 type, u32 tier, u16 count, u32+u32+u32+u8
    # Can't do 27 with this...
]

# Manual parse - try different field combos
p(f"\n  Raw hex of all entries:")
for i in range(num):
    start = 4 + i * 27
    entry = soldier_payload[start:start+27]
    p(f"  Entry {i+1}: {entry.hex()}")

    # Space it out in groups
    hex_spaced = ' '.join(entry[j:j+2].hex() for j in range(0, len(entry), 2))
    p(f"    Pairs: {hex_spaced}")

p(f"\n  Strategy 1: u32 type + u16 sub + (5x u32) + u8")
for i in range(num):
    start = 4 + i * 27
    e = soldier_payload[start:start+27]
    type_id = struct.unpack('<I', e[0:4])[0]
    sub = struct.unpack('<H', e[4:6])[0]
    # 21 remaining bytes... try 5 u32 + 1 u8 = 21
    vals = []
    pos = 6
    for j in range(5):
        if pos + 4 <= 27:
            vals.append(struct.unpack('<I', e[pos:pos+4])[0])
            pos += 4
    flag = e[26] if len(e) > 26 else 0
    p(f"    type={type_id}, sub={sub}, vals={vals}, flag={flag}")

p(f"\n  Strategy 2: u32 type + u16 sub + u16 count + u32 hp + u32 wounded + u32 ? + u32 ? + u8")
for i in range(num):
    start = 4 + i * 27
    e = soldier_payload[start:start+27]
    type_id = struct.unpack('<I', e[0:4])[0]
    sub = struct.unpack('<H', e[4:6])[0]
    count = struct.unpack('<H', e[6:8])[0]
    val1 = struct.unpack('<I', e[8:12])[0]
    val2 = struct.unpack('<I', e[12:16])[0]
    val3 = struct.unpack('<I', e[16:20])[0]
    val4 = struct.unpack('<H', e[20:22])[0]
    val5 = struct.unpack('<I', e[22:26])[0]
    flag = e[26]
    p(f"    type={type_id}, sub={sub}, count={count}, v1={val1}, v2={val2}, v3={val3}, v4={val4}, v5={val5}, flag={flag}")

p(f"\n  Strategy 3: u32 type + u8 tier + u32 total + u32 alive + u32 wounded + u32 training + u32 queued + u16 ?")
for i in range(num):
    start = 4 + i * 27
    e = soldier_payload[start:start+27]
    type_id = struct.unpack('<I', e[0:4])[0]
    tier = e[4]
    total = struct.unpack('<I', e[5:9])[0]
    alive = struct.unpack('<I', e[9:13])[0]
    wounded = struct.unpack('<I', e[13:17])[0]
    training = struct.unpack('<I', e[17:21])[0]
    queued = struct.unpack('<I', e[21:25])[0]
    extra = struct.unpack('<H', e[25:27])[0]
    p(f"    type={type_id}, tier={tier}, total={total}, alive={alive}, wound={wounded}, train={training}, queue={queued}, ex={extra}")

# ═══════════════════════════════════════════════════════════════
# 4. Decode HERO_INFO properly
# ═══════════════════════════════════════════════════════════════
p(f"\n\n{'='*60}")
p("HERO_INFO (0x00AA) - Proper Decoding")
p("=" * 60)

# Read hero data from PCAP
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

# Find hero data
for op, payload, sp, dp in all_pkts:
    if op == 0x00AA and len(payload) > 100:
        num_heroes = struct.unpack('<I', payload[0:4])[0]
        entry_size = (len(payload) - 4) // num_heroes if num_heroes > 0 else 0
        p(f"  Heroes: {num_heroes}, entry_size: {entry_size}")

        for i in range(min(num_heroes, 5)):
            start = 4 + i * entry_size
            e = payload[start:start+entry_size]

            # Try: u32 hero_id, u32 level, u8 star, ...
            hero_id = struct.unpack('<I', e[0:4])[0]
            val2 = struct.unpack('<I', e[4:8])[0]
            val3 = e[8] if len(e) > 8 else 0

            p(f"\n  Hero {i+1}:")
            p(f"    hero_id: {hero_id}")
            p(f"    field2 (level?): {val2}")
            p(f"    field3 (star?): {val3}")

            # Dump all as u32 values
            p(f"    All u32 values:")
            for j in range(0, min(entry_size, 80), 4):
                if j + 4 <= len(e):
                    v = struct.unpack('<I', e[j:j+4])[0]
                    if v != 0:
                        p(f"      [{j:3d}] = {v} (0x{v:08X})")

            # Also try u16 values
            p(f"    Non-zero u16 values:")
            for j in range(0, min(entry_size, 80), 2):
                if j + 2 <= len(e):
                    v = struct.unpack('<H', e[j:j+2])[0]
                    if v != 0 and v < 10000:
                        p(f"      [{j:3d}] = {v}")
        break

# ═══════════════════════════════════════════════════════════════
# 5. Building type mapping
# ═══════════════════════════════════════════════════════════════
p(f"\n\n{'='*60}")
p("BUILDING Type Mapping")
p("=" * 60)

# Search for building name strings
building_keywords = [
    b'Castle', b'Barrack', b'Hospital', b'Academy', b'Workshop',
    b'Embassy', b'Prison', b'Altar', b'Watchtower', b'Treasury',
    b'Warehouse', b'Infirmary', b'Wall', b'Gate', b'Tower',
    b'Farm', b'Quarry', b'Mine', b'Lumber', b'Manor',
    b'Forge', b'Gymnasium', b'Colosseum', b'Hall', b'Shelter',
    b'Battle Hall', b'BattleHall', b'Familiar',
]

p(f"\n  Building name strings in binary:")
for kw in building_keywords:
    pos = data.find(kw)
    if pos != -1:
        start = pos
        while start > 0 and data[start-1] >= 0x20 and data[start-1] < 0x7F:
            start -= 1
        end = pos + len(kw)
        while end < len(data) and data[end] >= 0x20 and data[end] < 0x7F:
            end += 1
        ctx = data[start:end].decode('ascii', errors='replace')
        if len(ctx) < 100:
            p(f"    0x{pos:08X}: {ctx}")

# From PCAP: slot=type pattern (slot 1=type 1 level 8 = Castle)
p(f"\n  Building types from PCAP (slot=type=ID):")
building_names_guess = {
    1: "Castle", 2: "Wall", 3: "Watchtower?", 4: "Prison?",
    5: "Altar?", 6: "Embassy?", 7: "Battle Hall?", 8: "Shelter?",
    13: "Farm?", 14: "Quarry/Mine?",
}
for slot, name in sorted(building_names_guess.items()):
    p(f"    Slot {slot:2d}: type={slot} -> {name}")

# ═══════════════════════════════════════════════════════════════
# 6. Search for troop type / tier constants
# ═══════════════════════════════════════════════════════════════
p(f"\n\n{'='*60}")
p("Troop Type/Tier Constants")
p("=" * 60)

troop_keywords = [
    b'Infantry', b'Ranged', b'Cavalry', b'Siege',
    b'infantry', b'ranged', b'cavalry', b'siege',
    b'Tier', b'tier', b'T1', b'T2', b'T3', b'T4',
    b'Warrior', b'Archer', b'Knight', b'Catapult',
    b'Grunt', b'Guard', b'Swordsman', b'Gladiator',
]

p(f"\n  Troop strings in binary:")
for kw in troop_keywords:
    positions = []
    search_start = 0
    while True:
        pos = data.find(kw, search_start)
        if pos == -1: break
        start = pos
        while start > 0 and data[start-1] >= 0x20 and data[start-1] < 0x7F:
            start -= 1
        end = pos + len(kw)
        while end < len(data) and data[end] >= 0x20 and data[end] < 0x7F:
            end += 1
        ctx = data[start:end].decode('ascii', errors='replace')
        if 3 < len(ctx) < 80 and not any(c in ctx for c in '{}()[]<>'):
            positions.append((pos, ctx))
        search_start = pos + 1
        if len(positions) > 3: break
    if positions:
        for addr, ctx in positions[:2]:
            p(f"    0x{addr:08X}: {ctx}")

# ═══════════════════════════════════════════════════════════════
# 7. Map ALL server response opcodes from PCAPs
# ═══════════════════════════════════════════════════════════════
p(f"\n\n{'='*60}")
p("All Unique Opcodes by Direction")
p("=" * 60)

# Load opcode names
sys.path.insert(0, r'D:\CascadeProjects\analysis\findings')
try:
    from cmsg_opcodes import CMSG_OPCODES
except:
    CMSG_OPCODES = {}

# Server port is 7000 based on PCAP data
client_ops = {}
server_ops = {}

for op, payload, sp, dp in all_pkts:
    name = CMSG_OPCODES.get(op, "?")
    if sp == 7000:
        # Server -> Client
        if op not in server_ops:
            server_ops[op] = {'count': 0, 'sizes': [], 'name': name}
        server_ops[op]['count'] += 1
        server_ops[op]['sizes'].append(len(payload))
    else:
        # Client -> Server
        if op not in client_ops:
            client_ops[op] = {'count': 0, 'sizes': [], 'name': name}
        client_ops[op]['count'] += 1
        client_ops[op]['sizes'].append(len(payload))

p(f"\n  Server -> Client opcodes ({len(server_ops)} unique):")
for op in sorted(server_ops.keys()):
    info = server_ops[op]
    avg_size = sum(info['sizes']) / len(info['sizes']) if info['sizes'] else 0
    min_size = min(info['sizes']) if info['sizes'] else 0
    max_size = max(info['sizes']) if info['sizes'] else 0
    p(f"    0x{op:04X} ({info['name']:40s}): {info['count']:4d}x, size {min_size}-{max_size} (avg {avg_size:.0f})")

p(f"\n  Client -> Server opcodes ({len(client_ops)} unique):")
for op in sorted(client_ops.keys()):
    info = client_ops[op]
    avg_size = sum(info['sizes']) / len(info['sizes']) if info['sizes'] else 0
    min_size = min(info['sizes']) if info['sizes'] else 0
    max_size = max(info['sizes']) if info['sizes'] else 0
    p(f"    0x{op:04X} ({info['name']:40s}): {info['count']:4d}x, size {min_size}-{max_size} (avg {avg_size:.0f})")

# SAVE
with open(r'D:\CascadeProjects\analysis\findings\item_category_map.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

p(f"\nSaved to findings/item_category_map.md")

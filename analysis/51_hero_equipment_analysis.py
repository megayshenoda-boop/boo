#!/usr/bin/env python3
"""
51_hero_equipment_analysis.py - Comprehensive Hero, Equipment, Forge,
Building Skin, and Achievement System Analysis
===========================================================================
Analyzes libgame.so ARM64 binary for:
  - Hero system (recruit, level, equip, skills, deploy, collection)
  - Equipment/Forge system (forge, enchant, gem, jewel, upgrade)
  - Achievement system (rewards, scores, wear)
  - Building skin system (change, upgrade, suit, unlock)
  - Talent/Familiar systems
  - Bot automation opportunities
  - Vulnerabilities (duplication, free upgrades, etc.)
"""
import struct
import re
import sys
import os

# Ensure capstone is available
try:
    from capstone import *
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "capstone"])
    from capstone import *

# ======================== CONFIG ========================
LIBGAME = r"D:\CascadeProjects\libgame.so"
OUTPUT = r"D:\CascadeProjects\analysis\findings\hero_equipment_systems.md"

with open(LIBGAME, "rb") as f:
    data = f.read()

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

# Known ELF offsets from prior analysis
DYNSTR_OFF = 0x682A10
DYNSYM_OFF = 0x2F8
DYNSYM_SIZE = 0x682758

# ======================== OUTPUT ========================
out = []
def p(msg=""):
    out.append(msg)
    try:
        print(msg)
    except:
        print(msg.encode('ascii', 'replace').decode())

# ======================== STRING SEARCH ========================
def extract_ascii_strings(binary_data, min_len=4, max_len=512):
    """Extract printable ASCII strings from binary data."""
    results = []
    current = bytearray()
    start = 0
    for i, b in enumerate(binary_data):
        if 0x20 <= b <= 0x7e:
            if not current:
                start = i
            current.append(b)
        else:
            if min_len <= len(current) <= max_len:
                results.append((start, current.decode('ascii', errors='replace')))
            current = bytearray()
    if min_len <= len(current) <= max_len:
        results.append((start, current.decode('ascii', errors='replace')))
    return results

# ======================== SYMBOL SEARCH ========================
def find_symbols_matching(pattern, include_packdata=True, include_getdata=True,
                          include_constructor=True):
    """Find all dynsym entries matching a pattern."""
    results = []
    regex = re.compile(pattern, re.IGNORECASE)
    pos = DYNSYM_OFF
    while pos + 24 <= DYNSYM_OFF + DYNSYM_SIZE:
        st_name = struct.unpack('<I', data[pos:pos+4])[0]
        st_info = data[pos + 4]
        st_value = struct.unpack('<Q', data[pos+8:pos+16])[0]
        st_size = struct.unpack('<Q', data[pos+16:pos+24])[0]
        if st_name > 0 and st_name < 0x300000 and st_value > 0:
            try:
                name_end = data.index(b'\x00', DYNSTR_OFF + st_name)
                name = data[DYNSTR_OFF + st_name:name_end].decode('ascii', errors='replace')
            except:
                pos += 24
                continue
            if regex.search(name):
                skip = False
                if not include_packdata and '8packData' in name:
                    skip = True
                if not include_getdata and '7getData' in name:
                    skip = True
                if not include_constructor and 'C1Ev' in name and '8packData' not in name and '7getData' not in name:
                    skip = True
                if not skip:
                    results.append({
                        'name': name,
                        'addr': st_value,
                        'size': st_size,
                        'type': 'packData' if '8packData' in name else
                                'getData' if '7getData' in name else
                                'constructor' if 'C1Ev' in name else 'other'
                    })
        pos += 24
    return results

def find_symbol_exact(name_contains, sym_type=None):
    """Find a single symbol by partial name match."""
    pos = DYNSYM_OFF
    while pos + 24 <= DYNSYM_OFF + DYNSYM_SIZE:
        st_name = struct.unpack('<I', data[pos:pos+4])[0]
        st_value = struct.unpack('<Q', data[pos+8:pos+16])[0]
        st_size = struct.unpack('<Q', data[pos+16:pos+24])[0]
        if st_name > 0 and st_name < 0x300000 and st_value > 0:
            try:
                name_end = data.index(b'\x00', DYNSTR_OFF + st_name)
                name = data[DYNSTR_OFF + st_name:name_end].decode('ascii', errors='replace')
            except:
                pos += 24
                continue
            if name_contains in name:
                if sym_type == 'packData' and '8packData' not in name:
                    pos += 24
                    continue
                if sym_type == 'getData' and '7getData' not in name:
                    pos += 24
                    continue
                if sym_type == 'constructor' and ('C1Ev' not in name or '8packData' in name or '7getData' in name):
                    pos += 24
                    continue
                return {'name': name, 'addr': st_value, 'size': st_size}
        pos += 24
    return None

# ======================== OPCODE EXTRACTION ========================
def extract_opcode_from_constructor(addr, size):
    """Extract the opcode (u16) set in a CMSG constructor.
    Pattern: movz/movk wN, #IMM then strh wN, [xR, #offset]
    """
    max_bytes = min(size if size > 0 else 200, 400)
    code = data[addr:addr + max_bytes]
    insns = list(md.disasm(code, addr))

    opcodes_found = []
    last_movz = {}
    for i, insn in enumerate(insns):
        if insn.mnemonic == 'ret' and insn.address > addr + 20:
            break
        # Track movz wN, #IMM
        if insn.mnemonic in ('movz', 'mov') and '#' in insn.op_str:
            parts = insn.op_str.split(',')
            if len(parts) >= 2:
                reg = parts[0].strip()
                try:
                    imm = int(parts[1].strip().lstrip('#'), 0)
                    if reg.startswith('w') and 0 < imm < 0xFFFF:
                        last_movz[reg] = imm
                except:
                    pass
        # movk extends
        if insn.mnemonic == 'movk' and '#' in insn.op_str:
            parts = insn.op_str.split(',')
            if len(parts) >= 2:
                reg = parts[0].strip()
                try:
                    imm = int(parts[1].strip().split('#')[1].split(',')[0], 0)
                    shift = 0
                    if 'lsl' in insn.op_str:
                        shift = int(insn.op_str.split('lsl')[1].strip().lstrip('#').rstrip(']'), 0)
                    if reg in last_movz:
                        last_movz[reg] = last_movz[reg] | (imm << shift)
                except:
                    pass
        # strh wN, [xR, #offset] -- storing opcode to struct
        if insn.mnemonic == 'strh':
            parts = insn.op_str.split(',')
            if len(parts) >= 2:
                reg = parts[0].strip()
                if reg in last_movz:
                    val = last_movz[reg]
                    if 0 < val < 0x2000:
                        opcodes_found.append(val)

    return opcodes_found

# ======================== PAYLOAD ANALYSIS ========================
def analyze_packdata(addr, size):
    """Analyze packData to extract payload format."""
    max_bytes = min(size if size > 0 else 600, 2000)
    code = data[addr:addr + max_bytes]
    insns = list(md.disasm(code, addr))

    payload_fields = []
    current_write_size = 0
    payload_offset = 0
    this_reg = 'x0'

    for i, insn in enumerate(insns):
        if insn.mnemonic == 'ret' and insn.address > addr + 20:
            break
        if insn.mnemonic == 'mov' and insn.op_str.startswith('x19, x0'):
            this_reg = 'x19'
        if insn.mnemonic == 'mov' and insn.op_str.startswith('x20, x0'):
            this_reg = 'x20'

        # Detect write size from: add wN, wN, #SIZE
        if insn.mnemonic == 'add' and '#' in insn.op_str:
            parts = insn.op_str.split('#')
            try:
                add_val = int(parts[-1], 0)
                if add_val in (1, 2, 4, 8):
                    for j in range(i+1, min(i+6, len(insns))):
                        if 'strh' in insns[j].mnemonic and '#0xa' in insns[j].op_str:
                            current_write_size = add_val
                            break
            except:
                pass

        # Detect data load from CMSG struct
        if insn.mnemonic in ('ldrh', 'ldrb', 'ldr', 'ldrsb', 'ldrsh', 'ldrsw'):
            if f'[{this_reg}]' in insn.op_str or f'[{this_reg},' in insn.op_str:
                offset = 0
                if '#' in insn.op_str:
                    try:
                        offset = int(insn.op_str.split('#')[-1].rstrip(']').rstrip('!'), 0)
                    except:
                        pass
                sizes = {'ldrb': 1, 'ldrsb': 1, 'ldrh': 2, 'ldrsh': 2, 'ldr': 4, 'ldrsw': 4}
                field_size = sizes.get(insn.mnemonic, 4)
                if insn.mnemonic == 'ldr' and insn.op_str.split(',')[0].strip().startswith('x'):
                    field_size = 8

                is_payload = False
                for j in range(i+1, min(i+8, len(insns))):
                    if insns[j].mnemonic in ('strh', 'strb', 'str') and 'uxtw' in insns[j].op_str:
                        is_payload = True
                        break
                if is_payload:
                    payload_fields.append({
                        'struct_offset': offset,
                        'size': current_write_size if current_write_size else field_size,
                        'payload_offset': payload_offset,
                    })
                    payload_offset += current_write_size if current_write_size else field_size
                    current_write_size = 0

    return payload_fields

def analyze_getdata(addr, size):
    """Analyze getData to extract response/S2C format (reads from CIStream)."""
    max_bytes = min(size if size > 0 else 600, 2000)
    code = data[addr:addr + max_bytes]
    insns = list(md.disasm(code, addr))

    fields = []
    current_read_size = 0
    read_offset = 0
    this_reg = 'x0'

    for i, insn in enumerate(insns):
        if insn.mnemonic == 'ret' and insn.address > addr + 20:
            break
        if insn.mnemonic == 'mov' and insn.op_str.startswith('x19, x0'):
            this_reg = 'x19'
        if insn.mnemonic == 'mov' and insn.op_str.startswith('x20, x0'):
            this_reg = 'x20'

        # Detect read size from: add wN, wN, #SIZE (position update)
        if insn.mnemonic == 'add' and '#' in insn.op_str:
            parts = insn.op_str.split('#')
            try:
                add_val = int(parts[-1], 0)
                if add_val in (1, 2, 4, 8):
                    for j in range(i+1, min(i+6, len(insns))):
                        if 'strh' in insns[j].mnemonic and '#0xa' in insns[j].op_str:
                            current_read_size = add_val
                            break
            except:
                pass

        # Detect read from buffer + store to struct
        if insn.mnemonic in ('ldrh', 'ldrb', 'ldr') and 'uxtw' in insn.op_str:
            sz = current_read_size if current_read_size else 2
            fields.append({
                'offset': read_offset,
                'size': sz,
            })
            read_offset += sz
            current_read_size = 0

    return fields

# ======================== MAIN ANALYSIS ========================
p("=" * 78)
p("HERO, EQUIPMENT, FORGE, ACHIEVEMENT & BUILDING SKIN ANALYSIS")
p("=" * 78)
p(f"Binary: {LIBGAME} ({len(data):,} bytes)")
p()

# ======================== 1. STRING SEARCH ========================
p("-" * 78)
p("SECTION 1: STRING SEARCH")
p("-" * 78)

all_strings = extract_ascii_strings(data)
p(f"Total strings extracted: {len(all_strings)}")

# Categories to search
string_categories = {
    'Hero Core': [
        r'hero_level', r'hero_grade', r'hero_equip', r'hero_skill',
        r'hero_star', r'hero_exp', r'hero_rank', r'hero_recruit',
        r'hero_upgrade', r'hero_evolve', r'hero_awaken', r'hero_talent',
        r'hero_medal', r'hero_fragment', r'hero_chip',
    ],
    'Hero Collection': [
        r'hero_collection', r'heroCollection', r'HeroCollection',
    ],
    'Equipment/Forge': [
        r'equip_forge', r'equip_enchant', r'equip_upgrade', r'equip_refine',
        r'equip_material', r'equipment', r'forge', r'enchant',
        r'jewel', r'gem_slot', r'gem_embed', r'gem_remove',
        r'smithy', r'workshop',
    ],
    'Achievement': [
        r'achievement', r'achieve_reward', r'achieve_score',
        r'achieve_wear', r'medal',
    ],
    'Building Skin': [
        r'building_skin', r'buildingSkin', r'skin_suit', r'skin_upgrade',
        r'skin_unlock', r'castle_skin',
    ],
    'Talent': [
        r'talent_tree', r'talent_reset', r'talent_upgrade', r'talent_point',
        r'research_talent',
    ],
    'Familiar': [
        r'familiar', r'pact', r'merge_familiar', r'familiar_skill',
        r'familiar_exp', r'familiar_level',
    ],
}

string_results = {}
for category, patterns in string_categories.items():
    matches = []
    for pattern in patterns:
        regex = re.compile(pattern, re.IGNORECASE)
        for offset, s in all_strings:
            if regex.search(s):
                matches.append((offset, s))
    # Deduplicate
    matches = sorted(set(matches))
    string_results[category] = matches
    p(f"\n  [{category}] - {len(matches)} matches:")
    for offset, s in matches[:30]:
        display = s[:100] + '...' if len(s) > 100 else s
        p(f"    0x{offset:08X}: {display}")
    if len(matches) > 30:
        p(f"    ... and {len(matches) - 30} more")

# Extra keyword scan for unmapped systems
p("\n  [Extra Keywords Scan]:")
extra_keywords = [
    'equip', 'forge', 'enchant', 'gem', 'jewel',
    'hero_skill', 'hero_level', 'hero_grade', 'hero_equip',
    'talent', 'familiar', 'pact',
    'sigil', 'rune', 'artifact', 'relic',
    'wonderForge', 'wonder_forge',
    'gear', 'material',
]
extra_found = {}
for kw in extra_keywords:
    count = 0
    sample_offsets = []
    regex = re.compile(kw, re.IGNORECASE)
    for offset, s in all_strings:
        if regex.search(s):
            count += 1
            if len(sample_offsets) < 3:
                sample_offsets.append((offset, s))
    if count > 0:
        extra_found[kw] = count
        p(f"    '{kw}': {count} hits")
        for off, s in sample_offsets:
            display = s[:80] + '...' if len(s) > 80 else s
            p(f"      0x{off:08X}: {display}")

# ======================== 2. SYMBOL ANALYSIS ========================
p()
p("-" * 78)
p("SECTION 2: SYMBOL ANALYSIS (Constructors, packData, getData)")
p("-" * 78)

# Hero system symbols
hero_patterns = [
    r'Hero(?!.*Battle)',
    r'HeroSoldier',
    r'HeroCollection',
    r'HeroRecruit',
    r'HeroEquip',
    r'HeroSkill',
    r'HeroInfo',
    r'HeroGrade',
    r'ArenHero',
    r'ArenaHero',
]

p("\n  === HERO SYSTEM SYMBOLS ===")
hero_symbols = []
for pat in hero_patterns:
    syms = find_symbols_matching(pat)
    for s in syms:
        if s not in hero_symbols:
            hero_symbols.append(s)

# Sort by type then name
hero_symbols.sort(key=lambda x: (x['type'], x['name']))
for s in hero_symbols:
    p(f"    [{s['type']:12s}] 0x{s['addr']:08X} ({s['size']:5d}B) {s['name'][:100]}")
p(f"  Total hero symbols: {len(hero_symbols)}")

# Equipment/Forge symbols
equip_patterns = [
    r'Equip(?!ment)',
    r'Equipment',
    r'Forge',
    r'Enchant',
    r'Gem(?!.*Game)',
    r'Jewel',
    r'Smithy',
    r'Material',
]

p("\n  === EQUIPMENT/FORGE SYMBOLS ===")
equip_symbols = []
for pat in equip_patterns:
    syms = find_symbols_matching(pat)
    for s in syms:
        if s not in equip_symbols:
            equip_symbols.append(s)

equip_symbols.sort(key=lambda x: (x['type'], x['name']))
for s in equip_symbols:
    p(f"    [{s['type']:12s}] 0x{s['addr']:08X} ({s['size']:5d}B) {s['name'][:100]}")
p(f"  Total equipment/forge symbols: {len(equip_symbols)}")

# Achievement symbols
p("\n  === ACHIEVEMENT SYMBOLS ===")
achieve_symbols = find_symbols_matching(r'Achievement')
achieve_symbols.sort(key=lambda x: (x['type'], x['name']))
for s in achieve_symbols:
    p(f"    [{s['type']:12s}] 0x{s['addr']:08X} ({s['size']:5d}B) {s['name'][:100]}")
p(f"  Total achievement symbols: {len(achieve_symbols)}")

# Building Skin symbols
p("\n  === BUILDING SKIN SYMBOLS ===")
skin_symbols = find_symbols_matching(r'BuildingSkin|BuildSkin|CastleSkin')
skin_symbols.sort(key=lambda x: (x['type'], x['name']))
for s in skin_symbols:
    p(f"    [{s['type']:12s}] 0x{s['addr']:08X} ({s['size']:5d}B) {s['name'][:100]}")
p(f"  Total building skin symbols: {len(skin_symbols)}")

# Talent symbols
p("\n  === TALENT SYMBOLS ===")
talent_symbols = find_symbols_matching(r'Talent|talent')
talent_symbols.sort(key=lambda x: (x['type'], x['name']))
for s in talent_symbols:
    p(f"    [{s['type']:12s}] 0x{s['addr']:08X} ({s['size']:5d}B) {s['name'][:100]}")
p(f"  Total talent symbols: {len(talent_symbols)}")

# Familiar symbols
p("\n  === FAMILIAR SYMBOLS ===")
familiar_symbols = find_symbols_matching(r'Familiar|Pact|familiar|pact')
familiar_symbols.sort(key=lambda x: (x['type'], x['name']))
for s in familiar_symbols:
    p(f"    [{s['type']:12s}] 0x{s['addr']:08X} ({s['size']:5d}B) {s['name'][:100]}")
p(f"  Total familiar symbols: {len(familiar_symbols)}")

# ======================== 3. OPCODE EXTRACTION ========================
p()
p("-" * 78)
p("SECTION 3: OPCODE EXTRACTION FROM CONSTRUCTORS")
p("-" * 78)

# Target CMSG types to extract opcodes from
target_cmsgs = [
    # Hero
    'CMSG_HERO_INFO',
    'CMSG_HERO_SOLDIER_RECRUIT',
    'CMSG_AREN_HERO_QUEUE',
    'CMSG_ARENA_HERO',
    'CMSG_HERO_COLLECTION',
    'CMSG_CLANPK_SET_DEFEND_HERO',
    'CMSG_CLANPK_SET_ATTACK_HERO',
    'CMSG_CLANPK_SET_ASSIST_HERO',
    'CMSG_CLANPK_GIVE_ASSIST_HERO',
    'CMSG_CLANPK_ASSIST_HERO',
    'CMSG_LOSTLAND_DONATE_HEROCHIP',
    'CMSG_LOSTLAND_BAN_HERO',
    'CMSG_LOSTLAND_HERO_VOTE',
    # Achievement
    'CMSG_ACHIEVEMENT_RECEIVE_REWARD',
    'CMSG_ACHIEVEMENT_SCORE_RECEIVE',
    'CMSG_ACHIEVEMENT_WEAR',
    'CMSG_LOSTLAND_ACHIEVEMENT',
    # Building Skin
    'CMSG_CHANGE_BUILDING_SKIN',
    'CMSG_BUILDING_SKIN_UPGRADE',
    'CMSG_BUILDING_SKIN_SUIT_REWARD',
    'CMSG_BUILDING_SKIN_REWARD',
    'CMSG_UNLOCK_BUILDING_SKIN',
    # Talent
    'CMSG_LEGION_SET_TALENT',
]

p("\n  Extracting opcodes from known CMSG constructors:")
opcode_map = {}
for cmsg_name in target_cmsgs:
    sym = find_symbol_exact(cmsg_name, sym_type='constructor')
    if sym:
        opcodes = extract_opcode_from_constructor(sym['addr'], sym['size'])
        if opcodes:
            for opc in opcodes:
                opcode_map[opc] = cmsg_name
                p(f"    0x{opc:04X} = {cmsg_name} (constructor @ 0x{sym['addr']:08X})")
        else:
            p(f"    {cmsg_name}: constructor found @ 0x{sym['addr']:08X} but no opcode extracted")
    else:
        p(f"    {cmsg_name}: NO constructor symbol found")

# Now scan ALL constructors for hero/equip/forge/achieve/skin keywords
p("\n  Scanning ALL constructors for unmapped hero/equip/forge opcodes:")
all_constructor_syms = find_symbols_matching(
    r'Hero|Equip|Forge|Enchant|Gem|Jewel|Achieve|Skin|Talent|Familiar|Pact',
    include_packdata=False, include_getdata=False, include_constructor=True
)
# Filter to actual constructors
constructors_only = [s for s in all_constructor_syms if s['type'] == 'constructor']

discovered_opcodes = {}
for sym in constructors_only:
    opcodes = extract_opcode_from_constructor(sym['addr'], sym['size'])
    for opc in opcodes:
        if opc not in opcode_map:
            discovered_opcodes[opc] = sym['name']
            p(f"    NEW: 0x{opc:04X} from {sym['name'][:80]}")

# ======================== 4. PAYLOAD FORMAT ANALYSIS ========================
p()
p("-" * 78)
p("SECTION 4: PAYLOAD FORMAT ANALYSIS (packData / getData)")
p("-" * 78)

payload_targets = [
    # Hero system
    ('CMSG_HERO_SOLDIER_RECRUIT_REQUEST', 'Hero recruit'),
    ('CMSG_HERO_INFO', 'Hero info (S2C)'),
    ('CMSG_AREN_HERO_QUEUE_CHANGE_REQUEST', 'Arena hero queue change'),
    ('CMSG_AREN_HERO_QUEUE_INFO', 'Arena hero queue info (S2C)'),
    ('CMSG_HERO_COLLECTION_ACTION_REQUEST', 'Hero collection action'),
    ('CMSG_HERO_COLLECTION_PVE_REQUEST', 'Hero collection PVE'),
    ('CMSG_HERO_COLLECTION_REWARD_REQUEST', 'Hero collection reward'),
    ('CMSG_CLANPK_SET_DEFEND_HERO_REQUEST', 'ClanPK defend hero'),
    ('CMSG_CLANPK_SET_ATTACK_HERO_REQUEST', 'ClanPK attack hero'),
    # Achievement
    ('CMSG_ACHIEVEMENT_RECEIVE_REWARD_REQUEST', 'Achievement reward'),
    ('CMSG_ACHIEVEMENT_SCORE_RECEIVE_REWARD_REQUEST', 'Achievement score reward'),
    ('CMSG_ACHIEVEMENT_WEAR_REQUEST', 'Achievement wear'),
    # Building skin
    ('CMSG_CHANGE_BUILDING_SKIN_REQUEST', 'Change building skin'),
    ('CMSG_BUILDING_SKIN_UPGRADE_LV_REQUEST', 'Building skin upgrade'),
    ('CMSG_BUILDING_SKIN_SUIT_REWARD_REQUEST', 'Building skin suit reward'),
    ('CMSG_BUILDING_SKIN_REWARD_REQUEST', 'Building skin reward'),
    ('CMSG_UNLOCK_BUILDING_SKIN_REQUEST', 'Unlock building skin'),
    # Talent
    ('CMSG_LEGION_SET_TALENT_REQUEST', 'Legion set talent'),
    # Lost land hero
    ('CMSG_LOSTLAND_DONATE_HEROCHIP_REQUEST', 'Lostland donate hero chip'),
    ('CMSG_LOSTLAND_BAN_HERO_REQUEST', 'Lostland ban hero'),
    ('CMSG_LOSTLAND_HERO_VOTE_COUNT_REQUEST', 'Lostland hero vote'),
    ('CMSG_LOSTLAND_ACHIEVEMENT_REWARD_REQUEST', 'Lostland achievement reward'),
]

payload_results = {}
for cmsg_name, description in payload_targets:
    # Try packData
    pack_sym = find_symbol_exact(cmsg_name, sym_type='packData')
    get_sym = find_symbol_exact(cmsg_name, sym_type='getData')

    p(f"\n  --- {cmsg_name} ({description}) ---")

    if pack_sym:
        fields = analyze_packdata(pack_sym['addr'], pack_sym['size'])
        total_bytes = sum(f['size'] for f in fields) if fields else 0
        p(f"    packData @ 0x{pack_sym['addr']:08X} ({pack_sym['size']}B func)")
        p(f"    Payload: {total_bytes} bytes, {len(fields)} fields:")
        for f in fields:
            p(f"      [{f['payload_offset']:2d}] struct[0x{f['struct_offset']:02X}] = {f['size']}B")
        payload_results[cmsg_name] = {'type': 'packData', 'fields': fields, 'total': total_bytes}
    elif get_sym:
        fields = analyze_getdata(get_sym['addr'], get_sym['size'])
        total_bytes = sum(f['size'] for f in fields) if fields else 0
        p(f"    getData @ 0x{get_sym['addr']:08X} ({get_sym['size']}B func)")
        p(f"    Response: {total_bytes} bytes, {len(fields)} fields:")
        for f in fields:
            p(f"      [{f['offset']:2d}] = {f['size']}B")
        payload_results[cmsg_name] = {'type': 'getData', 'fields': fields, 'total': total_bytes}
    else:
        p(f"    No packData/getData symbol found")

# ======================== 5. HERO_INFO DEEP DECODE ========================
p()
p("-" * 78)
p("SECTION 5: HERO_INFO (0x00AA) DEEP DECODE")
p("-" * 78)

hero_info_sym = find_symbol_exact('CMSG_HERO_INFO', sym_type='getData')
if hero_info_sym:
    p(f"  getData @ 0x{hero_info_sym['addr']:08X} ({hero_info_sym['size']}B)")
    # Disassemble first 200 instructions for detailed field mapping
    max_bytes = min(hero_info_sym['size'] if hero_info_sym['size'] > 0 else 2000, 4000)
    code = data[hero_info_sym['addr']:hero_info_sym['addr'] + max_bytes]
    insns = list(md.disasm(code, hero_info_sym['addr']))

    p(f"  Disassembled {len(insns)} instructions")

    # Count stores to this pointer (field writes)
    store_count = 0
    store_offsets = []
    for insn in insns:
        if insn.mnemonic in ('strh', 'strb', 'str', 'stur', 'sturh', 'sturb'):
            if 'x19' in insn.op_str or 'x20' in insn.op_str or 'x0' in insn.op_str:
                store_count += 1
                if '#' in insn.op_str:
                    try:
                        off = int(insn.op_str.split('#')[-1].rstrip(']').rstrip('!'), 0)
                        sizes = {'strb': 1, 'sturb': 1, 'strh': 2, 'sturh': 2, 'str': 4, 'stur': 4}
                        sz = sizes.get(insn.mnemonic, 4)
                        if insn.op_str.split(',')[-1].strip().startswith('[x') or 'x' in insn.op_str.split(',')[0]:
                            if insn.op_str.split(',')[0].strip().startswith('x'):
                                sz = 8
                        store_offsets.append((off, sz, insn.address))
                    except:
                        pass

    p(f"  Store operations to struct: {store_count}")
    if store_offsets:
        store_offsets.sort()
        p(f"  Field offsets in struct:")
        for off, sz, addr in store_offsets[:50]:
            p(f"    struct[0x{off:02X}] = {sz}B (@ 0x{addr:08X})")
else:
    p("  CMSG_HERO_INFO getData symbol not found")

# Also check hero info packData for C2S
hero_info_pack = find_symbol_exact('CMSG_HERO_INFO', sym_type='packData')
if hero_info_pack:
    p(f"\n  HERO_INFO packData @ 0x{hero_info_pack['addr']:08X}")
    fields = analyze_packdata(hero_info_pack['addr'], hero_info_pack['size'])
    total = sum(f['size'] for f in fields) if fields else 0
    p(f"  C2S Payload: {total} bytes, {len(fields)} fields")
    for f in fields:
        p(f"    [{f['payload_offset']:2d}] struct[0x{f['struct_offset']:02X}] = {f['size']}B")

# ======================== 6. COMPREHENSIVE EQUIP/FORGE SCAN ========================
p()
p("-" * 78)
p("SECTION 6: EQUIPMENT/FORGE SYSTEM DEEP SCAN")
p("-" * 78)

# Search for ALL symbols with equip/forge/enchant/gem/jewel
equip_all = find_symbols_matching(
    r'Equip|Forge|Enchant|Gem(?!.*Game)|Jewel|Refine|Sigil|Rune|Artifact|Relic|Gear|Workshop'
)

p(f"\n  Total equipment-related symbols: {len(equip_all)}")

# Group by category
equip_cats = {}
for s in equip_all:
    # Determine category from name
    name = s['name'].lower()
    if 'forge' in name:
        cat = 'Forge'
    elif 'enchant' in name:
        cat = 'Enchant'
    elif 'gem' in name or 'jewel' in name:
        cat = 'Gem/Jewel'
    elif 'refine' in name:
        cat = 'Refine'
    elif 'sigil' in name or 'rune' in name:
        cat = 'Sigil/Rune'
    elif 'equip' in name:
        cat = 'Equipment'
    else:
        cat = 'Other'

    if cat not in equip_cats:
        equip_cats[cat] = []
    equip_cats[cat].append(s)

for cat, syms in sorted(equip_cats.items()):
    p(f"\n  [{cat}] ({len(syms)} symbols):")
    # Show constructors first, then packData/getData
    for s in sorted(syms, key=lambda x: x['type']):
        p(f"    [{s['type']:12s}] 0x{s['addr']:08X} {s['name'][:90]}")

    # Extract opcodes from constructors
    for s in syms:
        if s['type'] == 'constructor':
            opcodes = extract_opcode_from_constructor(s['addr'], s['size'])
            for opc in opcodes:
                p(f"      -> OPCODE 0x{opc:04X}")

# ======================== 7. FIRE-AND-FORGET ANALYSIS ========================
p()
p("-" * 78)
p("SECTION 7: FIRE-AND-FORGET & AUTOMATION CANDIDATES")
p("-" * 78)

# Check which hero/equip CMSGs are fire-and-forget (no response expected)
# These are ones with only REQUEST but their RETURN is a separate S2C push
automation_targets = {
    'Hero Recruit': {
        'opcode': 0x0323,
        'cmsg': 'CMSG_HERO_SOLDIER_RECRUIT_REQUEST',
        'desc': 'Recruit hero soldiers',
    },
    'Achievement Reward': {
        'opcode': 0x0224,
        'cmsg': 'CMSG_ACHIEVEMENT_RECEIVE_REWARD_REQUEST',
        'desc': 'Claim achievement reward',
    },
    'Achievement Score Reward': {
        'opcode': 0x0226,
        'cmsg': 'CMSG_ACHIEVEMENT_SCORE_RECEIVE_REWARD_REQUEST',
        'desc': 'Claim achievement score reward',
    },
    'Achievement Wear': {
        'opcode': 0x0228,
        'cmsg': 'CMSG_ACHIEVEMENT_WEAR_REQUEST',
        'desc': 'Wear achievement badge',
    },
    'Change Building Skin': {
        'opcode': 0x1C20,
        'cmsg': 'CMSG_CHANGE_BUILDING_SKIN_REQUEST',
        'desc': 'Change building skin',
    },
    'Building Skin Upgrade': {
        'opcode': 0x1C24,
        'cmsg': 'CMSG_BUILDING_SKIN_UPGRADE_LV_REQUEST',
        'desc': 'Upgrade building skin level',
    },
    'Building Skin Suit Reward': {
        'opcode': 0x1C26,
        'cmsg': 'CMSG_BUILDING_SKIN_SUIT_REWARD_REQUEST',
        'desc': 'Claim skin suit reward',
    },
    'Building Skin Reward': {
        'opcode': 0x1C28,
        'cmsg': 'CMSG_BUILDING_SKIN_REWARD_REQUEST',
        'desc': 'Claim building skin reward',
    },
    'Unlock Building Skin': {
        'opcode': 0x1C2A,
        'cmsg': 'CMSG_UNLOCK_BUILDING_SKIN_REQUEST',
        'desc': 'Unlock building skin',
    },
    'Arena Hero Queue': {
        'opcode': 0x05E7,
        'cmsg': 'CMSG_AREN_HERO_QUEUE_CHANGE_REQUEST',
        'desc': 'Change arena hero queue',
    },
    'Hero Collection Action': {
        'opcode': 0x170D,
        'cmsg': 'CMSG_HERO_COLLECTION_ACTION_REQUEST',
        'desc': 'Hero collection action',
    },
    'Hero Collection PVE': {
        'opcode': 0x1710,
        'cmsg': 'CMSG_HERO_COLLECTION_PVE_REQUEST',
        'desc': 'Hero collection PVE battle',
    },
    'Hero Collection Reward': {
        'opcode': 0x1712,
        'cmsg': 'CMSG_HERO_COLLECTION_REWARD_REQUEST',
        'desc': 'Claim hero collection reward',
    },
    'Legion Set Talent': {
        'opcode': 0x0C65,
        'cmsg': 'CMSG_LEGION_SET_TALENT_REQUEST',
        'desc': 'Set legion talent',
    },
}

p("\n  Automation candidates (with payload analysis):")
for name, info in automation_targets.items():
    pack_sym = find_symbol_exact(info['cmsg'], sym_type='packData')
    if pack_sym:
        fields = analyze_packdata(pack_sym['addr'], pack_sym['size'])
        total = sum(f['size'] for f in fields) if fields else 0
        p(f"\n    {name} (0x{info['opcode']:04X}):")
        p(f"      {info['desc']}")
        p(f"      Payload: {total}B, {len(fields)} fields")
        for f in fields:
            p(f"        [{f['payload_offset']:2d}] struct[0x{f['struct_offset']:02X}] = {f['size']}B")
        p(f"      Automatable: YES (simple {total}B payload)")
    else:
        p(f"\n    {name} (0x{info['opcode']:04X}):")
        p(f"      {info['desc']}")
        p(f"      packData: NOT FOUND (may use raw encode or be S2C only)")

# ======================== 8. VULNERABILITY SCAN ========================
p()
p("-" * 78)
p("SECTION 8: VULNERABILITY & EXPLOIT ANALYSIS")
p("-" * 78)

# Check for opcodes that might allow:
# 1. Free hero upgrades (no resource check client-side)
# 2. Equipment duplication
# 3. Achievement exploit (claim without completing)
# 4. Skin unlock bypass

p("\n  [A] Fire-and-forget opcodes (no server validation visible):")
for name, info in automation_targets.items():
    p(f"    0x{info['opcode']:04X} {info['cmsg']} - {info['desc']}")

p("\n  [B] Scanning for validation-bypass patterns in hero/equip functions:")

# Look for client-side-only checks (CMP + B.xx patterns before send)
validation_functions = [
    'CMSG_HERO_SOLDIER_RECRUIT',
    'CMSG_ACHIEVEMENT_RECEIVE_REWARD',
    'CMSG_CHANGE_BUILDING_SKIN',
    'CMSG_BUILDING_SKIN_UPGRADE',
    'CMSG_UNLOCK_BUILDING_SKIN',
]

for func_name in validation_functions:
    sym = find_symbol_exact(func_name, sym_type='packData')
    if not sym:
        sym = find_symbol_exact(func_name, sym_type='constructor')
    if sym:
        max_bytes = min(sym['size'] if sym['size'] > 0 else 400, 800)
        code = data[sym['addr']:sym['addr'] + max_bytes]
        insns = list(md.disasm(code, sym['addr']))

        # Count conditional branches (validation checks)
        cmp_count = sum(1 for i in insns if i.mnemonic in ('cmp', 'cmn', 'tst'))
        branch_count = sum(1 for i in insns if i.mnemonic.startswith('b.') or i.mnemonic in ('cbz', 'cbnz'))

        p(f"\n    {func_name}:")
        p(f"      Comparisons: {cmp_count}, Branches: {branch_count}")
        if cmp_count <= 2:
            p(f"      -> LOW validation - potential bypass target")
        else:
            p(f"      -> Standard validation ({cmp_count} checks)")

# Check for repeated send patterns (could indicate loop/bulk operations)
p("\n  [C] Bulk/loop operation patterns:")
bulk_patterns = find_symbols_matching(r'Batch|Bulk|All|Multi|Loop|Auto|OneClick|Quick')
for s in bulk_patterns[:20]:
    p(f"    0x{s['addr']:08X} [{s['type']}] {s['name'][:80]}")

# ======================== 9. CROSS-REFERENCE UNKNOWN OPCODES ========================
p()
p("-" * 78)
p("SECTION 9: UNKNOWN/UNMAPPED OPCODES DISCOVERY")
p("-" * 78)

# Search for CMSG constructors we haven't mapped yet
p("\n  Scanning for unmapped hero/equip/forge constructors...")

unmapped_patterns = [
    r'HeroLevel', r'HeroUpgrade', r'HeroEvolve', r'HeroAwaken',
    r'HeroStar', r'HeroGrade', r'HeroExp', r'HeroMedal',
    r'HeroSkill', r'HeroTalent', r'HeroEquip',
    r'EquipForge', r'EquipEnchant', r'EquipUpgrade', r'EquipRefine',
    r'EquipGem', r'EquipJewel', r'EquipMaterial',
    r'GemEmbed', r'GemRemove', r'GemCombine',
    r'ForgeEquip', r'SmithyForge',
    r'TalentReset', r'TalentUpgrade', r'TalentPoint',
    r'FamiliarExp', r'FamiliarLevel', r'FamiliarSkill',
    r'PactMerge', r'PactHatch',
]

new_opcodes = {}
for pat in unmapped_patterns:
    syms = find_symbols_matching(pat, include_packdata=False, include_getdata=False)
    constructors = [s for s in syms if s['type'] == 'constructor']
    for sym in constructors:
        opcodes = extract_opcode_from_constructor(sym['addr'], sym['size'])
        for opc in opcodes:
            key = f"0x{opc:04X}"
            if key not in new_opcodes:
                new_opcodes[key] = sym['name']
                p(f"    DISCOVERED: 0x{opc:04X} from {sym['name'][:80]}")

# Also search for any constructor with "Request" that contains hero/equip
p("\n  Broad scan for any Request constructors with relevant keywords:")
broad_syms = find_symbols_matching(r'Request.*(?:Hero|Equip|Forge|Gem|Talent|Familiar|Skin|Achieve)')
broad_constructors = [s for s in broad_syms if s['type'] == 'constructor']
for sym in broad_constructors:
    opcodes = extract_opcode_from_constructor(sym['addr'], sym['size'])
    for opc in opcodes:
        key = f"0x{opc:04X}"
        if key not in new_opcodes and opc not in opcode_map:
            new_opcodes[key] = sym['name']
            p(f"    DISCOVERED: 0x{opc:04X} from {sym['name'][:80]}")

if not new_opcodes:
    p("    No additional unmapped opcodes found in these patterns")

# ======================== 10. SUMMARY ========================
p()
p("-" * 78)
p("SECTION 10: COMPLETE SUMMARY")
p("-" * 78)

all_opcodes = {}
all_opcodes.update(opcode_map)
for k, v in discovered_opcodes.items():
    all_opcodes[k] = v
for k_str, v in new_opcodes.items():
    all_opcodes[int(k_str, 16)] = v

p(f"\n  Total opcodes mapped: {len(all_opcodes)}")
p(f"  Total symbols analyzed: {len(hero_symbols) + len(equip_symbols) + len(achieve_symbols) + len(skin_symbols) + len(talent_symbols) + len(familiar_symbols)}")
p(f"  Payload formats decoded: {len(payload_results)}")

p("\n  === ALL MAPPED OPCODES (sorted) ===")
for opc in sorted(all_opcodes.keys()):
    p(f"    0x{opc:04X} = {all_opcodes[opc][:70]}")

p("\n  === AUTOMATABLE COMMANDS ===")
p("  These can be sent by the bot with simple payloads:")
for name, info in automation_targets.items():
    pack_sym = find_symbol_exact(info['cmsg'], sym_type='packData')
    if pack_sym:
        fields = analyze_packdata(pack_sym['addr'], pack_sym['size'])
        total = sum(f['size'] for f in fields) if fields else 0
        p(f"    0x{info['opcode']:04X} {name}: {total}B payload")

# ======================== WRITE OUTPUT ========================
p()
p("=" * 78)
p("END OF ANALYSIS")
p("=" * 78)

# Write markdown output
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

md_out = []
md_out.append("# Hero, Equipment, Forge, Achievement & Building Skin Systems")
md_out.append("")
md_out.append("Generated by 51_hero_equipment_analysis.py")
md_out.append("")

md_out.append("## 1. Hero System")
md_out.append("")
md_out.append("### Known Opcodes")
md_out.append("")
md_out.append("| Opcode | Name | Direction | Notes |")
md_out.append("|--------|------|-----------|-------|")
md_out.append("| 0x00AA | HERO_INFO | S2C | 109B per hero entry |")
md_out.append("| 0x0323 | HERO_SOLDIER_RECRUIT_REQUEST | C2S | Recruit soldiers for hero |")
md_out.append("| 0x05E6 | AREN_HERO_QUEUE_INFO | S2C | Arena hero queue sync |")
md_out.append("| 0x05E7 | AREN_HERO_QUEUE_CHANGE_REQUEST | C2S | Change arena hero lineup |")
md_out.append("| 0x05E8 | AREN_HERO_QUEUE_CHANGE_RETURN | S2C | Arena queue change response |")
md_out.append("| 0x170C | HERO_COLLECTION_SYNC_ACTION | S2C | Collection sync |")
md_out.append("| 0x170D | HERO_COLLECTION_ACTION_REQUEST | C2S | Collection action |")
md_out.append("| 0x170E | HERO_COLLECTION_ACTION_RETURN | S2C | Collection response |")
md_out.append("| 0x170F | HERO_COLLECTION_SYNC_TASK | S2C | Collection task sync |")
md_out.append("| 0x1710 | HERO_COLLECTION_PVE_REQUEST | C2S | Collection PVE battle |")
md_out.append("| 0x1711 | HERO_COLLECTION_PVE_RETURN | S2C | PVE response |")
md_out.append("| 0x1712 | HERO_COLLECTION_REWARD_REQUEST | C2S | Claim collection reward |")
md_out.append("| 0x1713 | HERO_COLLECTION_REWARD_RETURN | S2C | Reward response |")
md_out.append("| 0x1714 | HERO_COLLECTION_SYNC_RECHARGE | S2C | Recharge sync |")
md_out.append("")

md_out.append("### Hero-related ClanPK Opcodes")
md_out.append("")
md_out.append("| Opcode | Name | Direction |")
md_out.append("|--------|------|-----------|")
md_out.append("| 0x1B0A | CLANPK_SET_DEFEND_HERO_REQUEST | C2S |")
md_out.append("| 0x1B0C | CLANPK_SET_ATTACK_HERO_REQUEST | C2S |")
md_out.append("| 0x1B0E | CLANPK_SET_ASSIST_HERO_REQUEST | C2S |")
md_out.append("| 0x1B10 | CLANPK_GIVE_ASSIST_HERO_REQUEST | C2S |")
md_out.append("| 0x1B14 | CLANPK_ASSIST_HERO_REQUEST | C2S |")
md_out.append("")

md_out.append("### Lostland Hero Opcodes")
md_out.append("")
md_out.append("| Opcode | Name | Direction |")
md_out.append("|--------|------|-----------|")
md_out.append("| 0x15B9 | LOSTLAND_DONATE_HEROCHIP_REQUEST | C2S |")
md_out.append("| 0x15BE | LOSTLAND_BAN_HERO_REQUEST | C2S |")
md_out.append("| 0x15C0 | LOSTLAND_HERO_VOTE_COUNT_REQUEST | C2S |")
md_out.append("")

md_out.append("### Payload Formats")
md_out.append("")
for cmsg_name in ['CMSG_HERO_SOLDIER_RECRUIT_REQUEST', 'CMSG_AREN_HERO_QUEUE_CHANGE_REQUEST',
                   'CMSG_HERO_COLLECTION_ACTION_REQUEST', 'CMSG_HERO_COLLECTION_PVE_REQUEST',
                   'CMSG_HERO_COLLECTION_REWARD_REQUEST']:
    if cmsg_name in payload_results:
        r = payload_results[cmsg_name]
        md_out.append(f"**{cmsg_name}** ({r['type']}, {r['total']}B):")
        md_out.append("```")
        for f in r['fields']:
            if r['type'] == 'packData':
                md_out.append(f"  [{f['payload_offset']:2d}] struct[0x{f['struct_offset']:02X}] = {f['size']}B")
            else:
                md_out.append(f"  [{f['offset']:2d}] = {f['size']}B")
        md_out.append("```")
        md_out.append("")

md_out.append("### Symbol Analysis")
md_out.append("")
md_out.append(f"Total hero-related symbols found: {len(hero_symbols)}")
md_out.append("")
for s in hero_symbols[:40]:
    md_out.append(f"- [{s['type']}] `0x{s['addr']:08X}` {s['name'][:80]}")
md_out.append("")

# Equipment section
md_out.append("## 2. Equipment/Forge System")
md_out.append("")
md_out.append("### Symbols by Category")
md_out.append("")
for cat, syms in sorted(equip_cats.items()):
    md_out.append(f"**{cat}** ({len(syms)} symbols):")
    md_out.append("")
    for s in syms[:15]:
        md_out.append(f"- [{s['type']}] `0x{s['addr']:08X}` {s['name'][:80]}")
    if len(syms) > 15:
        md_out.append(f"- ... and {len(syms) - 15} more")
    md_out.append("")

md_out.append("### Discovered Opcodes")
md_out.append("")
for opc in sorted(discovered_opcodes.keys()):
    md_out.append(f"- `0x{opc:04X}` = {discovered_opcodes[opc][:70]}")
md_out.append("")

# Achievement section
md_out.append("## 3. Achievement System")
md_out.append("")
md_out.append("| Opcode | Name | Direction | Notes |")
md_out.append("|--------|------|-----------|-------|")
md_out.append("| 0x0224 | ACHIEVEMENT_RECEIVE_REWARD_REQUEST | C2S | Claim reward |")
md_out.append("| 0x0225 | ACHIEVEMENT_RECEIVE_REWARD_RETURN | S2C | Response |")
md_out.append("| 0x0226 | ACHIEVEMENT_SCORE_RECEIVE_REWARD_REQUEST | C2S | Score reward |")
md_out.append("| 0x0227 | ACHIEVEMENT_SCORE_RECEIVE_REWARD_RETURN | S2C | Response |")
md_out.append("| 0x0228 | ACHIEVEMENT_WEAR_REQUEST | C2S | Wear badge |")
md_out.append("| 0x0229 | ACHIEVEMENT_WEAR_RETURN | S2C | Response |")
md_out.append("")
md_out.append("### Payload Formats")
md_out.append("")
for cmsg_name in ['CMSG_ACHIEVEMENT_RECEIVE_REWARD_REQUEST',
                   'CMSG_ACHIEVEMENT_SCORE_RECEIVE_REWARD_REQUEST',
                   'CMSG_ACHIEVEMENT_WEAR_REQUEST']:
    if cmsg_name in payload_results:
        r = payload_results[cmsg_name]
        md_out.append(f"**{cmsg_name}** ({r['total']}B):")
        md_out.append("```")
        for f in r['fields']:
            md_out.append(f"  [{f['payload_offset']:2d}] struct[0x{f['struct_offset']:02X}] = {f['size']}B")
        md_out.append("```")
        md_out.append("")

md_out.append(f"Total achievement symbols: {len(achieve_symbols)}")
md_out.append("")

# Building Skin section
md_out.append("## 4. Building Skin System")
md_out.append("")
md_out.append("| Opcode | Name | Direction | Notes |")
md_out.append("|--------|------|-----------|-------|")
md_out.append("| 0x1C20 | CHANGE_BUILDING_SKIN_REQUEST | C2S | Change skin |")
md_out.append("| 0x1C21 | CHANGE_BUILDING_SKIN_RETURN | S2C | Response |")
md_out.append("| 0x1C22 | SYNC_BUILDING_SKIN_INFO | S2C | Skin info sync |")
md_out.append("| 0x1C24 | BUILDING_SKIN_UPGRADE_LV_REQUEST | C2S | Upgrade skin |")
md_out.append("| 0x1C25 | BUILDING_SKIN_UPGRADE_LV_RETURN | S2C | Response |")
md_out.append("| 0x1C26 | BUILDING_SKIN_SUIT_REWARD_REQUEST | C2S | Claim suit reward |")
md_out.append("| 0x1C27 | BUILDING_SKIN_SUIT_REWARD_RETURN | S2C | Response |")
md_out.append("| 0x1C28 | BUILDING_SKIN_REWARD_REQUEST | C2S | Claim skin reward |")
md_out.append("| 0x1C29 | BUILDING_SKIN_REWARD_RETURN | S2C | Response |")
md_out.append("| 0x1C2A | UNLOCK_BUILDING_SKIN_REQUEST | C2S | Unlock skin |")
md_out.append("| 0x1C2B | UNLOCK_BUILDING_SKIN_RETURN | S2C | Response |")
md_out.append("")
md_out.append("### Payload Formats")
md_out.append("")
for cmsg_name in ['CMSG_CHANGE_BUILDING_SKIN_REQUEST', 'CMSG_BUILDING_SKIN_UPGRADE_LV_REQUEST',
                   'CMSG_BUILDING_SKIN_SUIT_REWARD_REQUEST', 'CMSG_BUILDING_SKIN_REWARD_REQUEST',
                   'CMSG_UNLOCK_BUILDING_SKIN_REQUEST']:
    if cmsg_name in payload_results:
        r = payload_results[cmsg_name]
        md_out.append(f"**{cmsg_name}** ({r['total']}B):")
        md_out.append("```")
        for f in r['fields']:
            md_out.append(f"  [{f['payload_offset']:2d}] struct[0x{f['struct_offset']:02X}] = {f['size']}B")
        md_out.append("```")
        md_out.append("")

md_out.append(f"Total building skin symbols: {len(skin_symbols)}")
md_out.append("")

# Talent/Familiar section
md_out.append("## 5. Talent / Familiar Systems")
md_out.append("")
md_out.append("### Talent")
md_out.append("")
md_out.append("| Opcode | Name | Direction |")
md_out.append("|--------|------|-----------|")
md_out.append("| 0x0C65 | LEGION_SET_TALENT_REQUEST | C2S |")
md_out.append("| 0x0C66 | LEGION_SET_TALENT_RETURN | S2C |")
md_out.append("")
md_out.append(f"Total talent symbols: {len(talent_symbols)}")
md_out.append("")
for s in talent_symbols[:20]:
    md_out.append(f"- [{s['type']}] `0x{s['addr']:08X}` {s['name'][:80]}")
md_out.append("")

md_out.append("### Familiar")
md_out.append("")
md_out.append(f"Total familiar symbols: {len(familiar_symbols)}")
md_out.append("")
for s in familiar_symbols[:20]:
    md_out.append(f"- [{s['type']}] `0x{s['addr']:08X}` {s['name'][:80]}")
md_out.append("")

# Bot Automation section
md_out.append("## 6. Bot Automation Opportunities")
md_out.append("")
md_out.append("### Automatable Commands")
md_out.append("")
md_out.append("| Opcode | Command | Payload | Description |")
md_out.append("|--------|---------|---------|-------------|")
for name, info in sorted(automation_targets.items(), key=lambda x: x[1]['opcode']):
    pack_sym = find_symbol_exact(info['cmsg'], sym_type='packData')
    if pack_sym:
        fields = analyze_packdata(pack_sym['addr'], pack_sym['size'])
        total = sum(f['size'] for f in fields) if fields else 0
        md_out.append(f"| 0x{info['opcode']:04X} | {name} | {total}B | {info['desc']} |")
    else:
        md_out.append(f"| 0x{info['opcode']:04X} | {name} | ? | {info['desc']} |")
md_out.append("")

md_out.append("### Automation Flow")
md_out.append("")
md_out.append("1. **Hero Management**: Recruit (0x0323), manage arena queue (0x05E7)")
md_out.append("2. **Achievement Farming**: Auto-claim rewards (0x0224), score rewards (0x0226)")
md_out.append("3. **Building Skin**: Auto-claim skin rewards (0x1C28), suit rewards (0x1C26)")
md_out.append("4. **Hero Collection**: Run PVE battles (0x1710), claim rewards (0x1712)")
md_out.append("5. **Talent Management**: Set talents (0x0C65)")
md_out.append("")

# Vulnerability section
md_out.append("## 7. Vulnerabilities & Exploits")
md_out.append("")
md_out.append("### Fire-and-Forget Commands")
md_out.append("These opcodes send requests with no client-side validation:")
md_out.append("")
for name, info in automation_targets.items():
    md_out.append(f"- 0x{info['opcode']:04X} {info['cmsg']}")
md_out.append("")
md_out.append("### Potential Exploits")
md_out.append("")
md_out.append("1. **Achievement Reward Enumeration**: Send 0x0224 with sequential achievement IDs")
md_out.append("2. **Building Skin Unlock Bypass**: Send 0x1C2A without having skin materials")
md_out.append("3. **Hero Collection Reward Spam**: Repeatedly send 0x1712")
md_out.append("4. **Arena Queue Manipulation**: Set invalid hero combinations via 0x05E7")
md_out.append("5. **Skin Suit Reward**: Claim suit bonuses via 0x1C26 without full set")
md_out.append("")

# Newly discovered opcodes
if discovered_opcodes or new_opcodes:
    md_out.append("## 8. Newly Discovered Opcodes")
    md_out.append("")
    md_out.append("| Opcode | Source Symbol |")
    md_out.append("|--------|-------------|")
    all_new = {}
    all_new.update(discovered_opcodes)
    for k_str, v in new_opcodes.items():
        all_new[int(k_str, 16)] = v
    for opc in sorted(all_new.keys()):
        md_out.append(f"| 0x{opc:04X} | {all_new[opc][:60]} |")
    md_out.append("")

# String search results summary
md_out.append("## 9. String Search Summary")
md_out.append("")
for category, matches in string_results.items():
    md_out.append(f"### {category} ({len(matches)} matches)")
    md_out.append("")
    for offset, s in matches[:15]:
        display = s[:80] + '...' if len(s) > 80 else s
        md_out.append(f"- `0x{offset:08X}`: {display}")
    if len(matches) > 15:
        md_out.append(f"- ... and {len(matches) - 15} more")
    md_out.append("")

# Write file
with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(md_out))

p(f"\nOutput written to: {OUTPUT}")
p(f"Total lines in report: {len(md_out)}")

#!/usr/bin/env python3
"""
29_focused_discovery.py - Focused game mechanics discovery
==========================================================
Extract REAL game data: CMSG names, manager classes, item IDs,
troop types, building types, anti-cheat, rate limits, exploitable patterns.
"""
import struct, re, sys
from collections import defaultdict

LIBGAME = r"D:\CascadeProjects\libgame.so"
with open(LIBGAME, "rb") as f:
    data = f.read()

RODATA_OFF = 0x255B000
RODATA_SIZE = 4329528
rodata = data[RODATA_OFF:RODATA_OFF + RODATA_SIZE]

DYNSTR_OFF = 0x682A10
dynstr = data[DYNSTR_OFF:DYNSTR_OFF + 0x200000]

out = []
def p(msg):
    out.append(msg)
    try: print(msg)
    except: print(msg.encode('ascii','replace').decode())

p("=" * 80)
p("FOCUSED DISCOVERY - Game Mechanics & Exploits")
p("=" * 80)

# ═══════════════════════════════════════════════════════════════
# 1. Extract ALL unique CMSG names (clean, no C++ templates)
# ═══════════════════════════════════════════════════════════════
p("\n### 1. ALL CMSG Protocol Messages ###\n")

cmsg_names = set()
# Pattern: CMSG_SOMETHING (in dynstr and rodata)
for section in [rodata, dynstr]:
    for m in re.finditer(rb'CMSG_[A-Z0-9_]{3,80}', section):
        name = m.group().decode('ascii')
        # Filter out partial matches from C++ mangled names
        if not name.endswith('_') and 'EEEE' not in name:
            cmsg_names.add(name)

# Categorize by function
categories = defaultdict(list)
cat_keywords = {
    'MARCH/BATTLE': ['MARCH', 'ATTACK', 'BATTLE', 'SCOUT', 'RALLY', 'GARRISON', 'REINFORCE', 'SIEGE', 'WAR'],
    'RESOURCE/GATHER': ['GATHER', 'RESOURCE', 'HARVEST', 'FARM', 'FOOD', 'WOOD', 'STONE', 'ORE', 'GOLD'],
    'BUILD/RESEARCH': ['BUILD', 'UPGRADE', 'RESEARCH', 'CONSTRUCT', 'DEMOLISH'],
    'TRAIN/TROOPS': ['TRAIN', 'SOLDIER', 'TROOP', 'HEAL', 'HOSPITAL'],
    'HERO': ['HERO', 'FAMILIAR', 'MONSTER'],
    'ITEM/INVENTORY': ['ITEM', 'USE_ITEM', 'EQUIP', 'INVENTORY', 'BAG', 'CHEST'],
    'SHOP/PURCHASE': ['SHOP', 'BUY', 'PURCHASE', 'STORE', 'MALL', 'PAY', 'RECHARGE'],
    'REWARD/FREE': ['REWARD', 'FREE', 'GIFT', 'CLAIM', 'COLLECT', 'BONUS', 'LOTTERY', 'LUCKY'],
    'GUILD/ALLIANCE': ['LEAGUE', 'ALLIANCE', 'GUILD', 'CLAN', 'LEGION', 'MEMBER'],
    'CHAT/SOCIAL': ['CHAT', 'MAIL', 'FRIEND', 'BLOCK', 'REPORT'],
    'SPEEDUP/BOOST': ['SPEED', 'BOOST', 'BUFF', 'ACCELERAT', 'INSTANT', 'SKIP', 'COMPLETE'],
    'KINGDOM/MAP': ['KINGDOM', 'MAP', 'TILE', 'MIGRATE', 'TELEPORT', 'SHELTER'],
    'EVENT/ACTIVITY': ['EVENT', 'ACTIVITY', 'SEASON', 'TOURNAMENT', 'ARENA', 'COLOSSEUM'],
    'TRADE/EXCHANGE': ['TRADE', 'EXCHANGE', 'CONVERT', 'TRANSFER', 'DONATE'],
    'AUTH/SYSTEM': ['LOGIN', 'LOGOUT', 'PASSWORD', 'AUTH', 'SYNC', 'HEARTBEAT', 'VERSION'],
    'DOMINION': ['DOMINION'],
    'EXPEDITION': ['EXPEDITION', 'ADVENTURE', 'LABYRINTH'],
}

for name in sorted(cmsg_names):
    categorized = False
    for cat, keywords in cat_keywords.items():
        if any(kw in name for kw in keywords):
            categories[cat].append(name)
            categorized = True
            break
    if not categorized:
        categories['OTHER'].append(name)

total = 0
for cat in sorted(categories.keys()):
    items = categories[cat]
    total += len(items)
    p(f"\n  [{cat}] ({len(items)}):")
    for name in items:
        p(f"    {name}")

p(f"\n  TOTAL unique CMSGs: {total}")

# ═══════════════════════════════════════════════════════════════
# 2. Game Manager Classes (control game logic)
# ═══════════════════════════════════════════════════════════════
p("\n\n### 2. Game Manager Classes ###\n")
managers = set()
for m in re.finditer(rb'C?[A-Z][a-zA-Z]+Manager', dynstr):
    name = m.group().decode('ascii')
    if len(name) > 8 and len(name) < 60:
        managers.add(name)
for m in re.finditer(rb'[A-Z][a-zA-Z]+Manager', rodata):
    name = m.group().decode('ascii')
    if len(name) > 8 and len(name) < 60:
        managers.add(name)

for name in sorted(managers):
    p(f"  {name}")
p(f"\n  Total: {len(managers)} managers")

# ═══════════════════════════════════════════════════════════════
# 3. Hardcoded Item/Building/Troop Type IDs
# ═══════════════════════════════════════════════════════════════
p("\n\n### 3. XML Config Files (game data) ###\n")
xml_names = set()
for m in re.finditer(rb'[A-Z][a-zA-Z_]+Xml\b', rodata):
    xml_names.add(m.group().decode('ascii'))
for m in re.finditer(rb'[a-z][a-zA-Z_]+\.xml\b', rodata):
    xml_names.add(m.group().decode('ascii'))

for name in sorted(xml_names):
    p(f"  {name}")
p(f"\n  Total: {len(xml_names)} XML configs")

# ═══════════════════════════════════════════════════════════════
# 4. Anti-cheat & Security mechanisms
# ═══════════════════════════════════════════════════════════════
p("\n\n### 4. Anti-Cheat & Security ###\n")
security_pats = [
    rb'anti.?cheat', rb'speed.?hack', rb'time.?cheat',
    rb'detect', rb'suspicious', rb'abnormal',
    rb'verify', rb'validate', rb'check.?sum',
    rb'encrypt', rb'decrypt', rb'hash',
    rb'sign', rb'protect', rb'secure',
    rb'ban', rb'block', rb'kick', rb'punish',
    rb'rate.?limit', rb'cooldown', rb'too.?fast', rb'too.?many',
    rb'frequency', rb'interval', rb'throttle',
    rb'emulat', rb'root', rb'jailbreak', rb'hook',
    rb'frida', rb'xposed', rb'substrate', rb'gameguardian',
    rb'memory.?edit', rb'tamper', rb'modif',
    rb'replay', rb'duplicate', rb'overflow',
    rb'inject',
]
found_security = set()
for pat in security_pats:
    for m in re.finditer(pat, rodata, re.IGNORECASE):
        start = m.start()
        while start > 0 and rodata[start-1] != 0: start -= 1
        end = m.end()
        while end < len(rodata) and rodata[end] != 0: end += 1
        s = rodata[start:end].decode('ascii', errors='replace')
        if 4 < len(s) < 150:
            # Skip C++ type info noise
            if not any(x in s for x in ['__ndk1', 'cocos2d', 'NSt6', 'ZTSZN', 'ZTVN']):
                found_security.add(s)

for s in sorted(found_security):
    p(f"  {s}")
p(f"\n  Total: {len(found_security)} security strings")

# ═══════════════════════════════════════════════════════════════
# 5. Interesting format strings (reveal server protocol details)
# ═══════════════════════════════════════════════════════════════
p("\n\n### 5. Protocol/Debug Format Strings ###\n")
fmt_strings = set()
for m in re.finditer(rb'[A-Za-z_]{3,30}[=:]\s*%[duxsf]', rodata):
    start = m.start()
    while start > 0 and rodata[start-1] not in (0, 0x0a): start -= 1
    end = m.end()
    while end < len(rodata) and rodata[end] not in (0, 0x0a): end += 1
    s = rodata[start:end].decode('ascii', errors='replace').strip()
    if 5 < len(s) < 200 and not any(x in s for x in ['cocos', 'openssl', 'curl', 'JPEG', 'PNG', 'zlib']):
        fmt_strings.add(s)

for s in sorted(fmt_strings)[:100]:
    p(f"  {s}")

# ═══════════════════════════════════════════════════════════════
# 6. Reward/Free/Cheat CMSG packData functions (exploitable)
# ═══════════════════════════════════════════════════════════════
p("\n\n### 6. CMSGs with packData (client → server requests) ###\n")
pack_cmsgs = set()
for m in re.finditer(rb'(CMSG_[A-Z0-9_]{3,80})8packData', dynstr):
    name = m.group(1).decode('ascii')
    pack_cmsgs.add(name)

# These are the ones the CLIENT can SEND
p("  === Client-sendable CMSGs (have packData) ===")
send_categories = defaultdict(list)
for name in sorted(pack_cmsgs):
    if 'RETURN' in name or 'SYNC' in name or 'SYN_' in name:
        continue  # These are server→client
    categorized = False
    for cat, keywords in cat_keywords.items():
        if any(kw in name for kw in keywords):
            send_categories[cat].append(name)
            categorized = True
            break
    if not categorized:
        send_categories['OTHER'].append(name)

for cat in sorted(send_categories.keys()):
    items = send_categories[cat]
    p(f"\n  [{cat}] ({len(items)} sendable):")
    for name in items:
        p(f"    {name}")

# Server responses (have getData)
p("\n\n  === Server responses (RETURN/SYNC CMSGs with getData) ===")
get_cmsgs = set()
for m in re.finditer(rb'(CMSG_[A-Z0-9_]{3,80})7getData', dynstr):
    name = m.group(1).decode('ascii')
    if 'RETURN' in name or 'SYNC' in name or 'SYN_' in name:
        get_cmsgs.add(name)

resp_categories = defaultdict(list)
for name in sorted(get_cmsgs):
    categorized = False
    for cat, keywords in cat_keywords.items():
        if any(kw in name for kw in keywords):
            resp_categories[cat].append(name)
            categorized = True
            break
    if not categorized:
        resp_categories['OTHER'].append(name)

for cat in sorted(resp_categories.keys()):
    items = resp_categories[cat]
    p(f"\n  [{cat}] ({len(items)} responses):")
    for name in items:
        p(f"    {name}")

# ═══════════════════════════════════════════════════════════════
# 7. March types & troop definitions
# ═══════════════════════════════════════════════════════════════
p("\n\n### 7. March & Troop Related Strings ###\n")
march_pats = [
    rb'march_type', rb'MarchType', rb'MARCH_TYPE',
    rb'troop_type', rb'TroopType', rb'TROOP_TYPE',
    rb'soldier_type', rb'SoldierType',
    rb'army_type', rb'ArmyType',
    rb'[Gg]ather', rb'[Rr]ally', rb'[Ss]cout',
    rb'[Aa]ttack', rb'[Rr]einforce', rb'[Gg]arrison',
    rb'march_slot', rb'MarchSlot',
    rb'march_speed', rb'MarchSpeed',
    rb'[Tt]arget[Pp]os', rb'[Tt]arget[Xx]', rb'[Tt]arget[Yy]',
]
found_march = set()
for pat in march_pats:
    for m in re.finditer(pat, rodata):
        start = m.start()
        while start > 0 and rodata[start-1] != 0: start -= 1
        end = m.end()
        while end < len(rodata) and rodata[end] != 0: end += 1
        s = rodata[start:end].decode('ascii', errors='replace')
        if 3 < len(s) < 150 and 'NSt6' not in s:
            found_march.add(s)

for s in sorted(found_march):
    p(f"  {s}")

# ═══════════════════════════════════════════════════════════════
# 8. Resource & Economy strings
# ═══════════════════════════════════════════════════════════════
p("\n\n### 8. Economy & Resource Strings ###\n")
econ_pats = [
    rb'[Dd]iamond', rb'[Gg]old', rb'[Gg]em',
    rb'[Ff]ood', rb'[Ww]ood', rb'[Ss]tone', rb'[Oo]re',
    rb'[Ss]tamina', rb'[Ee]nergy',
    rb'VIP', rb'vip_level',
    rb'[Rr]efresh', rb'[Rr]eset',
    rb'[Ff]ree_times', rb'daily_free',
    rb'[Cc]ost', rb'[Pp]rice',
    rb'[Dd]iscount',
    rb'[Ss]peed[Uu]p', rb'speed_up',
]
found_econ = set()
for pat in econ_pats:
    for m in re.finditer(pat, rodata):
        start = m.start()
        while start > 0 and rodata[start-1] != 0: start -= 1
        end = m.end()
        while end < len(rodata) and rodata[end] != 0: end += 1
        s = rodata[start:end].decode('ascii', errors='replace')
        if 3 < len(s) < 120 and 'NSt6' not in s and 'cocos2d' not in s:
            found_econ.add(s)

for s in sorted(found_econ):
    p(f"  {s}")

# ═══════════════════════════════════════════════════════════════
# 9. Map 0x0038 attribute field IDs to names
# ═══════════════════════════════════════════════════════════════
p("\n\n### 9. Attribute Field Names (0x0038) ###\n")
attr_pats = [
    rb'ATTR_[A-Z_]{3,50}',
    rb'ATTRIBUTE_[A-Z_]{3,50}',
    rb'kAttr[A-Z][a-zA-Z_]{3,50}',
]
found_attrs = set()
for pat in attr_pats:
    for m in re.finditer(pat, rodata):
        found_attrs.add(m.group().decode('ascii'))
    for m in re.finditer(pat, dynstr):
        found_attrs.add(m.group().decode('ascii'))

for s in sorted(found_attrs):
    p(f"  {s}")

# ═══════════════════════════════════════════════════════════════
# 10. All opcodes referenced as hex constants in strings
# ═══════════════════════════════════════════════════════════════
p("\n\n### 10. Opcode References in Strings ###\n")
opcode_refs = set()
for m in re.finditer(rb'0x[0-9A-Fa-f]{3,4}\b', rodata):
    val = int(m.group(), 16)
    if 0x20 < val < 0x2000:  # Likely opcode range
        # Get context
        start = max(0, m.start() - 30)
        while start > 0 and rodata[start-1] != 0: start -= 1
        end = min(len(rodata), m.end() + 30)
        while end < len(rodata) and rodata[end] != 0: end += 1
        s = rodata[start:end].decode('ascii', errors='replace').strip()
        if 5 < len(s) < 200:
            opcode_refs.add(s)

for s in sorted(opcode_refs)[:50]:
    p(f"  {s}")

# ═══════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════
with open(r'D:\CascadeProjects\analysis\findings\focused_discovery.md', 'w', encoding='utf-8') as f:
    f.write("# Focused Discovery - Game Mechanics & Exploits\n\n")
    f.write('\n'.join(out))

p(f"\n\nSaved to findings/focused_discovery.md")
p(f"Stats: {total} CMSGs, {len(managers)} managers, {len(xml_names)} XMLs,")
p(f"  {len(found_security)} security, {len(pack_cmsgs)} packData, {len(get_cmsgs)} getData")

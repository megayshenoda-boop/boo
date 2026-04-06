#!/usr/bin/env python3
"""
30_clean_discovery.py - Clean game mechanics discovery
======================================================
Properly extract CMSG names, managers, configs WITHOUT C++ noise.
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
p("CLEAN DISCOVERY - Game Mechanics")
p("=" * 80)

# ═══════════════════════════════════════════════════════════════
# 1. Clean CMSG names from dynstr (match packData/getData/C1Ev patterns)
# ═══════════════════════════════════════════════════════════════
p("\n### 1. ALL Protocol Messages (Clean) ###\n")

# Extract from packData (client→server) and getData (server→client)
client_msgs = set()  # Have packData = client sends these
server_msgs = set()  # Have getData = server sends these

for m in re.finditer(rb'(CMSG_[A-Z0-9_]{4,60})8packData', dynstr):
    client_msgs.add(m.group(1).decode('ascii'))

for m in re.finditer(rb'(CMSG_[A-Z0-9_]{4,60})7getData', dynstr):
    server_msgs.add(m.group(1).decode('ascii'))

# Also get from constructor pattern C1Ev
all_msgs = set()
for m in re.finditer(rb'(CMSG_[A-Z0-9_]{4,60})C1Ev', dynstr):
    all_msgs.add(m.group(1).decode('ascii'))

# Combine
all_msgs.update(client_msgs)
all_msgs.update(server_msgs)

# Categorize
cat_keywords = {
    'MARCH/BATTLE': ['MARCH', 'ATTACK', 'BATTLE', 'SCOUT', 'RALLY', 'GARRISON', 'REINFORCE', 'SIEGE'],
    'RESOURCE/GATHER': ['GATHER', 'RESOURCE', 'HARVEST'],
    'BUILD': ['BUILD', 'UPGRADE_BUILD', 'CONSTRUCT', 'DEMOLISH', 'BUILDING'],
    'RESEARCH': ['RESEARCH', 'TECH'],
    'TRAIN': ['TRAIN', 'SOLDIER', 'TROOP', 'HEAL', 'HOSPITAL'],
    'HERO': ['HERO', 'FAMILIAR'],
    'ITEM': ['ITEM', 'EQUIP', 'INVENTORY', 'BAG', 'CHEST', 'USE_'],
    'SHOP/BUY': ['SHOP', 'BUY', 'PURCHASE', 'STORE', 'MALL', 'PAY', 'RECHARGE'],
    'REWARD/FREE': ['REWARD', 'FREE', 'GIFT', 'CLAIM', 'COLLECT', 'BONUS', 'LOTTERY', 'LUCKY'],
    'GUILD': ['LEAGUE', 'ALLIANCE', 'GUILD', 'CLAN', 'LEGION', 'MEMBER', 'HELP'],
    'CHAT/SOCIAL': ['CHAT', 'MAIL', 'FRIEND', 'BLOCK_CONDITION'],
    'SPEED/BOOST': ['SPEED', 'BOOST', 'BUFF', 'ACCELERAT'],
    'KINGDOM/MAP': ['KINGDOM', 'MAP', 'TILE', 'MIGRATE', 'TELEPORT', 'SHELTER', 'MONSTER', 'WORLD'],
    'EVENT': ['EVENT', 'ACTIVITY', 'SEASON', 'TOURNAMENT', 'ARENA', 'COLOSSEUM', 'LOSTLAND'],
    'TRADE': ['TRADE', 'EXCHANGE', 'CONVERT', 'TRANSFER', 'DONATE', 'DESERT'],
    'AUTH': ['LOGIN', 'LOGOUT', 'PASSWORD', 'USERINFO', 'VERSION'],
    'SYNC': ['SYNC_', 'SYN_'],
    'DOMINION': ['DOMINION'],
    'EXPEDITION': ['EXPEDITION', 'ADVENTURE', 'LABYRINTH'],
    'CAMEL': ['CAMEL'],
    'CLANPK': ['CLANPK', 'CLAN_WAR'],
}

cat_msgs = defaultdict(list)
for name in sorted(all_msgs):
    found = False
    for cat, keywords in cat_keywords.items():
        if any(kw in name for kw in keywords):
            cat_msgs[cat].append(name)
            found = True
            break
    if not found:
        cat_msgs['OTHER'].append(name)

total_client = 0
total_server = 0
for cat in sorted(cat_msgs.keys()):
    items = cat_msgs[cat]
    p(f"\n  [{cat}] ({len(items)}):")
    for name in items:
        marker = ""
        if name in client_msgs and name in server_msgs:
            marker = " [BOTH]"
        elif name in client_msgs:
            marker = " [→SERVER]"
            total_client += 1
        elif name in server_msgs:
            marker = " [←SERVER]"
            total_server += 1
        p(f"    {name}{marker}")

p(f"\n  Total: {len(all_msgs)} unique CMSGs ({len(client_msgs)} client→server, {len(server_msgs)} server→client)")

# ═══════════════════════════════════════════════════════════════
# 2. BOT-USEFUL: Client-sendable commands (REQUEST type)
# ═══════════════════════════════════════════════════════════════
p("\n\n### 2. BOT-USEFUL Client Commands ###\n")
p("  (These are CMSGs the client sends that could be automated)\n")

bot_useful = {
    'REWARD/FREE STUFF': [],
    'TRAINING': [],
    'BUILDING': [],
    'RESEARCH': [],
    'MARCHING': [],
    'ITEMS': [],
    'SHOPPING': [],
    'GUILD HELP': [],
    'SPEEDUPS': [],
    'OTHER AUTOMATION': [],
}

for name in sorted(client_msgs):
    if 'RETURN' in name or 'SYNC' in name or 'SYN_' in name:
        continue
    n = name.upper()
    if any(kw in n for kw in ['REWARD', 'FREE', 'GIFT', 'CLAIM', 'COLLECT', 'BONUS', 'LOTTERY', 'LUCKY', 'RECEIVE']):
        bot_useful['REWARD/FREE STUFF'].append(name)
    elif any(kw in n for kw in ['TRAIN', 'SOLDIER', 'HEAL']):
        bot_useful['TRAINING'].append(name)
    elif any(kw in n for kw in ['BUILD', 'UPGRADE', 'CONSTRUCT']):
        bot_useful['BUILDING'].append(name)
    elif any(kw in n for kw in ['RESEARCH', 'TECH']):
        bot_useful['RESEARCH'].append(name)
    elif any(kw in n for kw in ['MARCH', 'ATTACK', 'RALLY', 'GATHER', 'SCOUT']):
        bot_useful['MARCHING'].append(name)
    elif any(kw in n for kw in ['ITEM', 'USE', 'EQUIP', 'CHEST', 'OPEN']):
        bot_useful['ITEMS'].append(name)
    elif any(kw in n for kw in ['BUY', 'SHOP', 'PURCHASE']):
        bot_useful['SHOPPING'].append(name)
    elif any(kw in n for kw in ['HELP', 'DONATE', 'ALLIANCE']):
        bot_useful['GUILD HELP'].append(name)
    elif any(kw in n for kw in ['SPEED', 'BOOST', 'ACCELERAT', 'INSTANT']):
        bot_useful['SPEEDUPS'].append(name)

for cat, items in sorted(bot_useful.items()):
    if items:
        p(f"  [{cat}]:")
        for name in items:
            p(f"    {name}")
        p("")

# ═══════════════════════════════════════════════════════════════
# 3. Manager classes
# ═══════════════════════════════════════════════════════════════
p("\n### 3. Game Managers ###\n")
managers = set()
# Match: digit + ManagerName + digit pattern in dynstr (C++ mangled)
for m in re.finditer(rb'\d{1,2}([A-Z][A-Za-z]+Manager)\d', dynstr):
    managers.add(m.group(1).decode('ascii'))

for name in sorted(managers):
    p(f"  {name}")
p(f"\n  Total: {len(managers)}")

# ═══════════════════════════════════════════════════════════════
# 4. XML Config files
# ═══════════════════════════════════════════════════════════════
p("\n\n### 4. Game Config XMLs ###\n")
xmls = set()
for m in re.finditer(rb'(\d{1,2}[A-Z][a-zA-Z_]+Xml)\b', rodata):
    name = m.group(1).decode('ascii')
    # Strip leading digits (C++ mangled length prefix)
    clean = re.sub(r'^\d+', '', name)
    xmls.add(clean)
for m in re.finditer(rb'([a-zA-Z_]{3,40}\.xml)\b', rodata):
    xmls.add(m.group(1).decode('ascii'))

for name in sorted(xmls):
    p(f"  {name}")
p(f"\n  Total: {len(xmls)}")

# ═══════════════════════════════════════════════════════════════
# 5. Anti-cheat (clean)
# ═══════════════════════════════════════════════════════════════
p("\n\n### 5. Security & Anti-Cheat ###\n")
security_terms = set()
for m in re.finditer(rb'[a-zA-Z_]*(?:cheat|hack|ban|detect|suspicious|abnormal|verify|tamper|emulat|root|jailbreak|frida|xposed|gameguardian|speedhack)[a-zA-Z_]*', rodata, re.IGNORECASE):
    start = m.start()
    while start > 0 and rodata[start-1] != 0: start -= 1
    end = m.end()
    while end < len(rodata) and rodata[end] != 0: end += 1
    s = rodata[start:end].decode('ascii', errors='replace')
    if 3 < len(s) < 100 and 'NSt6' not in s and '__ndk' not in s and 'cocos' not in s:
        security_terms.add(s)

for s in sorted(security_terms):
    p(f"  {s}")

# ═══════════════════════════════════════════════════════════════
# 6. March-related strings
# ═══════════════════════════════════════════════════════════════
p("\n\n### 6. March/Battle Strings ###\n")
march_terms = set()
for pat in [rb'[Mm]arch', rb'[Tt]roop', rb'[Ss]oldier', rb'[Aa]rmy', rb'[Rr]ally',
            rb'[Gg]ather', rb'[Ss]cout', rb'[Gg]arrison', rb'[Rr]einforce']:
    for m in re.finditer(pat, rodata):
        start = m.start()
        while start > 0 and rodata[start-1] != 0: start -= 1
        end = m.end()
        while end < len(rodata) and rodata[end] != 0: end += 1
        s = rodata[start:end].decode('ascii', errors='replace')
        if 3 < len(s) < 100 and 'NSt6' not in s and '__ndk' not in s and 'cocos' not in s:
            march_terms.add(s)

for s in sorted(march_terms):
    p(f"  {s}")

# ═══════════════════════════════════════════════════════════════
# 7. Vulnerability patterns - race conditions, integer overflow, etc
# ═══════════════════════════════════════════════════════════════
p("\n\n### 7. Potential Vulnerability Patterns ###\n")

# Find functions that do FREE/REWARD without proper checks
p("  === Interesting CMSG pairs (REQUEST without validation?) ===")
requests = set()
returns = set()
for name in all_msgs:
    if name.endswith('_REQUEST'):
        base = name[:-8]
        ret = base + '_RETURN'
        if ret in all_msgs:
            requests.add((name, ret))
        else:
            p(f"    {name} - NO MATCHING RETURN (fire-and-forget?)")

# Find duplicate/cancel patterns
p("\n  === Cancel/Undo Patterns ===")
for name in sorted(client_msgs):
    if any(kw in name for kw in ['CANCEL', 'UNDO', 'REFUND', 'ROLLBACK', 'RESET']):
        p(f"    {name}")

# ═══════════════════════════════════════════════════════════════
# 8. Interesting hardcoded constants
# ═══════════════════════════════════════════════════════════════
p("\n\n### 8. Game Constants ###\n")
const_pats = [
    (rb'MAX_MARCH_SLOT', "Max march slots"),
    (rb'MAX_QUEUE', "Max queue"),
    (rb'VIP_LEVEL', "VIP levels"),
    (rb'MAX_TROOP', "Max troops"),
    (rb'STAMINA', "Stamina"),
    (rb'FREE_TIMES', "Free attempts"),
    (rb'DAILY_LIMIT', "Daily limits"),
    (rb'COOLDOWN', "Cooldowns"),
]
for pat, desc in const_pats:
    found = set()
    for m in re.finditer(pat, rodata, re.IGNORECASE):
        start = m.start()
        while start > 0 and rodata[start-1] != 0: start -= 1
        end = m.end()
        while end < len(rodata) and rodata[end] != 0: end += 1
        s = rodata[start:end].decode('ascii', errors='replace')
        if 3 < len(s) < 100:
            found.add(s)
    if found:
        p(f"  [{desc}]:")
        for s in sorted(found):
            p(f"    {s}")

# ═══════════════════════════════════════════════════════════════
# 9. Opcode → CMSG name mapping (from registerListener patterns)
# ═══════════════════════════════════════════════════════════════
p("\n\n### 9. Key Opcodes → CMSG Mapping ###\n")
# From registerListener patterns, we can map opcodes to CMSG names
# The opcode is embedded in the binary near the handler registration
# Let's look for known opcodes referenced near CMSG names

known_ops = {
    0x0CE8: 'START_MARCH_NEW', 0x0CED: 'TRAIN', 0x0CEF: 'BUILD',
    0x0CEE: 'RESEARCH', 0x0CEB: 'ENABLE_VIEW', 0x1B8B: 'PASSWORD_CHECK',
    0x0323: 'PRE_MARCH?', 0x0038: 'ATTRIBUTE_CHANGE',
}
for op, name in sorted(known_ops.items()):
    p(f"  0x{op:04X} = {name}")

p("\n  (See protocol.py for full 2272 opcode map)")

# ═══════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════
with open(r'D:\CascadeProjects\analysis\findings\clean_discovery.md', 'w', encoding='utf-8') as f:
    f.write("# Clean Discovery - Game Mechanics & Exploits\n\n")
    f.write('\n'.join(out))

p(f"\n\nSaved to findings/clean_discovery.md")
p(f"Stats: {len(all_msgs)} total CMSGs, {len(client_msgs)} sendable, {len(server_msgs)} receivable")
p(f"  {len(managers)} managers, {len(xmls)} XMLs")

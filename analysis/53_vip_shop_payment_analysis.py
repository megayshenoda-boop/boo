#!/usr/bin/env python3
"""
VIP, Shop, Payment, and Investment system analysis of libgame.so.
Searches for all purchase/shop/payment/VIP related opcodes, strings,
and cross-references to build a comprehensive map of monetization systems.
"""

import sys
import struct
import os
import re
from collections import defaultdict

sys.path.insert(0, r'D:\CascadeProjects\claude')
sys.path.insert(0, r'D:\CascadeProjects\analysis\findings')

from cmsg_opcodes import CMSG_OPCODES

# Binary config
BINARY = r'D:\CascadeProjects\libgame.so'
DYNSTR_OFFSET = 0x682A10
DYNSYM_OFFSET = 0x2F8
DYNSYM_SIZE = 0x682758
OUTPUT_PATH = r'D:\CascadeProjects\analysis\findings\vip_shop_payment.md'

# Load binary
with open(BINARY, 'rb') as f:
    data = f.read()

print(f"[*] Loaded {len(data):,} bytes from libgame.so")
print(f"[*] {len(CMSG_OPCODES)} opcodes in CMSG_OPCODES map")
print()

# ================================================================
# Helper: extract all ASCII strings from binary
# ================================================================
def extract_all_strings(min_len=4, max_len=300):
    """Extract all printable ASCII strings from binary."""
    strings = []
    current = bytearray()
    start_off = 0
    for i in range(len(data)):
        b = data[i]
        if 0x20 <= b < 0x7F:
            if len(current) == 0:
                start_off = i
            current.append(b)
        else:
            if min_len <= len(current) <= max_len:
                s = current.decode('ascii', errors='ignore')
                strings.append((start_off, s))
            current = bytearray()
    return strings

print("[*] Extracting all strings from binary...")
ALL_STRINGS = extract_all_strings()
print(f"[*] Found {len(ALL_STRINGS):,} strings total")

# ================================================================
# Helper: search strings by pattern
# ================================================================
def search_strings(patterns, case_insensitive=True):
    """Search extracted strings for patterns."""
    results = defaultdict(list)
    for off, s in ALL_STRINGS:
        s_check = s.lower() if case_insensitive else s
        for pat in patterns:
            pat_check = pat.lower() if case_insensitive else pat
            if pat_check in s_check:
                results[pat].append((off, s))
                break
    return results

# ================================================================
# Helper: parse dynsym for symbol names
# ================================================================
def parse_dynsym():
    """Parse ELF64 .dynsym to get exported/imported symbols."""
    symbols = []
    end = DYNSYM_OFFSET + DYNSYM_SIZE
    i = DYNSYM_OFFSET
    while i + 24 <= end:
        st_name, st_info, st_other, st_shndx = struct.unpack_from('<IBBH', data, i)
        st_value, st_size = struct.unpack_from('<QQ', data, i + 8)
        i += 24
        if st_name == 0:
            continue
        name_off = DYNSTR_OFFSET + st_name
        if name_off >= len(data):
            continue
        null_pos = data.find(b'\x00', name_off, name_off + 512)
        if null_pos < 0:
            continue
        name = data[name_off:null_pos].decode('utf-8', errors='replace')
        if name:
            symbols.append({
                'name': name,
                'value': st_value,
                'size': st_size,
                'info': st_info,
                'shndx': st_shndx,
            })
    return symbols

print("[*] Parsing dynamic symbols...")
ALL_SYMBOLS = parse_dynsym()
print(f"[*] Found {len(ALL_SYMBOLS):,} symbols")

# ================================================================
# Helper: search symbols by pattern
# ================================================================
def search_symbols(patterns, case_insensitive=True):
    """Search symbols for patterns."""
    results = defaultdict(list)
    for sym in ALL_SYMBOLS:
        name = sym['name']
        n_check = name.lower() if case_insensitive else name
        for pat in patterns:
            p_check = pat.lower() if case_insensitive else pat
            if p_check in n_check:
                results[pat].append(sym)
                break
    return results

# ================================================================
# Helper: opcode name helpers
# ================================================================
def get_name(opcode):
    return CMSG_OPCODES.get(opcode, f'UNKNOWN_0x{opcode:04X}')

def strip_prefix(name):
    return name[5:] if name.startswith('CMSG_') else name

# Build reverse lookup
name_to_opcode = {v: k for k, v in CMSG_OPCODES.items()}

# ================================================================
# Begin analysis
# ================================================================
report = []
report.append("# VIP, Shop, Payment & Investment System Analysis")
report.append(f"# Generated from libgame.so ({len(data):,} bytes)")
report.append(f"# Total mapped opcodes: {len(CMSG_OPCODES)}")
report.append("")

# ================================================================
# 1. VIP SYSTEM
# ================================================================
print("=" * 60)
print("  1. VIP SYSTEM ANALYSIS")
print("=" * 60)

report.append("## 1. VIP System")
report.append("")

# Find VIP opcodes
vip_opcodes = []
for opcode, name in sorted(CMSG_OPCODES.items()):
    if 'VIP' in name.upper():
        vip_opcodes.append((opcode, name))
        print(f"  VIP opcode: 0x{opcode:04X} = {name}")

# Search for VIP strings in binary
vip_strings = search_strings(['vip', 'VIP', 'Vip'])
vip_count = sum(len(v) for v in vip_strings.values())
print(f"  Found {vip_count} VIP-related strings in binary")

# Search for VIP symbols
vip_symbols = search_symbols(['vip', 'VIP', 'Vip'])
vip_sym_count = sum(len(v) for v in vip_symbols.values())
print(f"  Found {vip_sym_count} VIP-related symbols")

report.append("### VIP Opcodes")
report.append("")
if vip_opcodes:
    report.append("| Opcode | Name | Type |")
    report.append("|--------|------|------|")
    for opcode, name in vip_opcodes:
        sname = strip_prefix(name)
        typ = "REQUEST" if "_REQUEST" in sname else "RETURN" if "_RETURN" in sname else "SYNC" if "SYN" in sname or "SYS" in sname else "ACTION"
        report.append(f"| 0x{opcode:04X} | {name} | {typ} |")
else:
    report.append("No VIP-specific opcodes found in CMSG map.")
report.append("")

# VIP data also in SYS_LEAGUE_BATTLEFIELD_INFO
report.append("### VIP Data Sources")
report.append("")
report.append("- 0x07E4 SYS_LEAGUE_BATTLEFIELD_INFO - Contains VIP level data")
report.append("- 0x0033 SYN_ATTRIBUTE_CHANGE - VIP level synced as attribute ID")
report.append("- 0x0037 SYN_EXTRA_ATTRIBUTE_CHANGE - Extended VIP attributes")
report.append("")

# VIP-related strings
report.append("### VIP Strings in Binary")
report.append("")
report.append("| Offset | String |")
report.append("|--------|--------|")
all_vip = []
for pat, matches in vip_strings.items():
    for off, s in matches:
        all_vip.append((off, s))
all_vip.sort()
# Deduplicate and limit
seen = set()
count = 0
for off, s in all_vip:
    if s not in seen and count < 80:
        seen.add(s)
        report.append(f"| 0x{off:08X} | {s[:120]} |")
        count += 1
report.append("")

# VIP class symbols
report.append("### VIP Class Methods (from symbols)")
report.append("")
vip_methods = []
for pat, syms in vip_symbols.items():
    for sym in syms:
        vip_methods.append(sym)
vip_methods.sort(key=lambda x: x['name'])
seen_names = set()
for sym in vip_methods:
    if sym['name'] not in seen_names:
        seen_names.add(sym['name'])
        if sym['size'] > 0:
            report.append(f"- `{sym['name']}` @ 0x{sym['value']:08X} (size={sym['size']})")
report.append("")

# ================================================================
# 2. CHARGE / PAYMENT SYSTEM
# ================================================================
print()
print("=" * 60)
print("  2. CHARGE / PAYMENT SYSTEM")
print("=" * 60)

report.append("## 2. Charge / Payment System")
report.append("")

# Charge/payment opcodes
charge_opcodes = []
for opcode, name in sorted(CMSG_OPCODES.items()):
    sname = strip_prefix(name).upper()
    if any(kw in sname for kw in ['CHARGE', 'PAY', 'PURCHASE', 'RECHARGE', 'MICROPAY', 'DINAR']):
        charge_opcodes.append((opcode, name))
        print(f"  Charge opcode: 0x{opcode:04X} = {name}")

report.append("### Charge/Payment Opcodes")
report.append("")
report.append("| Opcode | Name | Direction |")
report.append("|--------|------|-----------|")
for opcode, name in charge_opcodes:
    sname = strip_prefix(name)
    direction = "C->S" if "REQUEST" in sname else "S->C" if "RETURN" in sname or "INFO" in sname or "SYN" in sname else "BOTH"
    report.append(f"| 0x{opcode:04X} | {name} | {direction} |")
report.append("")

# Charge strings
charge_strings = search_strings(['charge', 'payment', 'recharge', 'dinar', 'micropay', 'iap', 'purchase'])
report.append("### Payment Strings in Binary")
report.append("")
report.append("| Offset | String |")
report.append("|--------|--------|")
all_charge = []
for pat, matches in charge_strings.items():
    for off, s in matches:
        all_charge.append((off, s))
all_charge.sort()
seen = set()
count = 0
for off, s in all_charge:
    if s not in seen and count < 80:
        seen.add(s)
        report.append(f"| 0x{off:08X} | {s[:120]} |")
        count += 1
report.append("")

# Payment symbols
charge_syms = search_symbols(['Charge', 'charge', 'Payment', 'payment', 'Recharge', 'recharge',
                               'Purchase', 'purchase', 'Dinar', 'dinar', 'MicroPay', 'micropay',
                               'IAP', 'iap'])
report.append("### Payment Class Methods")
report.append("")
all_csyms = []
for pat, syms in charge_syms.items():
    all_csyms.extend(syms)
all_csyms.sort(key=lambda x: x['name'])
seen_names = set()
for sym in all_csyms:
    if sym['name'] not in seen_names and sym['size'] > 0:
        seen_names.add(sym['name'])
        report.append(f"- `{sym['name']}` @ 0x{sym['value']:08X} (size={sym['size']})")
report.append("")

# ================================================================
# 3. SHOP SYSTEMS
# ================================================================
print()
print("=" * 60)
print("  3. SHOP SYSTEMS")
print("=" * 60)

report.append("## 3. Shop Systems")
report.append("")

# Shop opcodes by category
shop_categories = {
    'ROYAL_SHOP': (0x0794, 0x079F),
    'REWARD_POINT_SHOP': (0x0AF0, 0x0AF5),
    'NOVICE_FREE_PURCHASE': (0x0CB2, 0x0CB8),
    'CAMEL_SHOP': (0x038E, 0x0395),
}

# Find ALL shop-related opcodes
shop_opcodes = []
for opcode, name in sorted(CMSG_OPCODES.items()):
    sname = strip_prefix(name).upper()
    if any(kw in sname for kw in ['SHOP', 'BUY', 'SELL', 'STORE', 'PURCHASE', 'MALL', 'MARKET']):
        shop_opcodes.append((opcode, name))
        print(f"  Shop opcode: 0x{opcode:04X} = {name}")

report.append("### All Shop-Related Opcodes")
report.append("")
report.append("| Opcode | Name | Has Return? |")
report.append("|--------|------|-------------|")
for opcode, name in shop_opcodes:
    sname = strip_prefix(name)
    # Check for matching return
    if '_REQUEST' in sname:
        ret_name = name.replace('_REQUEST', '_RETURN')
        has_ret = "YES" if ret_name in name_to_opcode else "NO (fire-and-forget)"
    elif '_RETURN' in sname:
        has_ret = "(is return)"
    else:
        has_ret = "N/A"
    report.append(f"| 0x{opcode:04X} | {name} | {has_ret} |")
report.append("")

# Shop-specific categories
for cat_name, (start, end) in shop_categories.items():
    cat_opcodes = [(op, nm) for op, nm in sorted(CMSG_OPCODES.items()) if start <= op <= end]
    if cat_opcodes:
        report.append(f"#### {cat_name} (0x{start:04X}-0x{end:04X})")
        report.append("")
        for opcode, name in cat_opcodes:
            report.append(f"- 0x{opcode:04X} = {name}")
        report.append("")

# Shop strings
shop_strings = search_strings(['shop', 'store', 'mall', 'market', 'buy', 'sell'])
report.append("### Shop Strings in Binary")
report.append("")
report.append("| Offset | String |")
report.append("|--------|--------|")
all_shop = []
for pat, matches in shop_strings.items():
    for off, s in matches:
        all_shop.append((off, s))
all_shop.sort()
seen = set()
count = 0
for off, s in all_shop:
    if s not in seen and count < 100:
        seen.add(s)
        report.append(f"| 0x{off:08X} | {s[:120]} |")
        count += 1
report.append("")

# Shop symbols
shop_syms = search_symbols(['Shop', 'shop', 'Store', 'store', 'Mall', 'mall', 'Market', 'market'])
report.append("### Shop Class Methods")
report.append("")
all_ssyms = []
for pat, syms in shop_syms.items():
    all_ssyms.extend(syms)
all_ssyms.sort(key=lambda x: x['name'])
seen_names = set()
for sym in all_ssyms:
    if sym['name'] not in seen_names and sym['size'] > 0:
        seen_names.add(sym['name'])
        report.append(f"- `{sym['name']}` @ 0x{sym['value']:08X} (size={sym['size']})")
report.append("")

# ================================================================
# 4. GOLD / GEM SYSTEM
# ================================================================
print()
print("=" * 60)
print("  4. GOLD / GEM / CURRENCY SYSTEM")
print("=" * 60)

report.append("## 4. Gold / Gem / Currency System")
report.append("")

# Gold/gem opcodes
gold_opcodes = []
for opcode, name in sorted(CMSG_OPCODES.items()):
    sname = strip_prefix(name).upper()
    if any(kw in sname for kw in ['GOLD', 'GEM', 'DIAMOND', 'COIN', 'CURRENCY', 'FUND']):
        gold_opcodes.append((opcode, name))
        print(f"  Gold/gem opcode: 0x{opcode:04X} = {name}")

report.append("### Gold/Gem Opcodes")
report.append("")
if gold_opcodes:
    report.append("| Opcode | Name |")
    report.append("|--------|------|")
    for opcode, name in gold_opcodes:
        report.append(f"| 0x{opcode:04X} | {name} |")
else:
    report.append("(Gold/gem amounts are tracked via SYN_ATTRIBUTE_CHANGE attribute IDs)")
report.append("")

# Gold consumption tracking
report.append("### Gold Consumption Tracking (ACCUMULATION)")
report.append("")
accum_opcodes = [(op, nm) for op, nm in sorted(CMSG_OPCODES.items()) if 'ACCUMULATION' in nm.upper()]
for opcode, name in accum_opcodes:
    report.append(f"- 0x{opcode:04X} = {name}")
report.append("")

# Gold/gem strings
gold_strings = search_strings(['gold', 'gem', 'diamond', 'coin', 'currency', 'fund'])
report.append("### Gold/Gem/Currency Strings")
report.append("")
all_gold = []
for pat, matches in gold_strings.items():
    for off, s in matches:
        all_gold.append((off, s))
all_gold.sort()
seen = set()
count = 0
for off, s in all_gold:
    if s not in seen and count < 80:
        seen.add(s)
        report.append(f"- 0x{off:08X}: `{s[:120]}`")
        count += 1
report.append("")

# ================================================================
# 5. INVEST SYSTEM
# ================================================================
print()
print("=" * 60)
print("  5. INVEST SYSTEM")
print("=" * 60)

report.append("## 5. Investment System")
report.append("")

# Invest opcodes (0x0925-0x092A range)
invest_opcodes = []
for opcode, name in sorted(CMSG_OPCODES.items()):
    sname = strip_prefix(name).upper()
    if 'INVEST' in sname or (0x0920 <= opcode <= 0x0935):
        invest_opcodes.append((opcode, name))
        print(f"  Invest opcode: 0x{opcode:04X} = {name}")

report.append("### Investment Opcodes")
report.append("")
if invest_opcodes:
    report.append("| Opcode | Name | Type |")
    report.append("|--------|------|------|")
    for opcode, name in invest_opcodes:
        sname = strip_prefix(name)
        typ = "REQUEST" if "REQUEST" in sname else "RETURN" if "RETURN" in sname else "SYNC" if "SYN" in sname else "INFO" if "INFO" in sname else "ACTION"
        report.append(f"| 0x{opcode:04X} | {name} | {typ} |")
else:
    report.append("No invest opcodes found in range 0x0920-0x0935.")
report.append("")

# Invest strings
invest_strings = search_strings(['invest', 'Invest', 'INVEST'])
report.append("### Investment Strings")
report.append("")
all_invest = []
for pat, matches in invest_strings.items():
    for off, s in matches:
        all_invest.append((off, s))
all_invest.sort()
seen = set()
for off, s in all_invest:
    if s not in seen:
        seen.add(s)
        report.append(f"- 0x{off:08X}: `{s[:120]}`")
report.append("")

# Invest symbols
invest_syms = search_symbols(['Invest', 'invest'])
report.append("### Investment Class Methods")
report.append("")
all_isyms = []
for pat, syms in invest_syms.items():
    all_isyms.extend(syms)
all_isyms.sort(key=lambda x: x['name'])
seen_names = set()
for sym in all_isyms:
    if sym['name'] not in seen_names and sym['size'] > 0:
        seen_names.add(sym['name'])
        report.append(f"- `{sym['name']}` @ 0x{sym['value']:08X} (size={sym['size']})")
report.append("")

# ================================================================
# 6. DAILY RECHARGE SYSTEM
# ================================================================
print()
print("=" * 60)
print("  6. DAILY RECHARGE SYSTEM")
print("=" * 60)

report.append("## 6. Daily Recharge System")
report.append("")

# Daily recharge opcodes (0x0EA6-0x0EA9)
daily_recharge = []
for opcode, name in sorted(CMSG_OPCODES.items()):
    sname = strip_prefix(name).upper()
    if 'DAILY_RECHARGE' in sname or 'RECHARGE' in sname or (0x0EA0 <= opcode <= 0x0EB0):
        daily_recharge.append((opcode, name))
        print(f"  Daily recharge: 0x{opcode:04X} = {name}")

report.append("### Daily Recharge Opcodes")
report.append("")
if daily_recharge:
    report.append("| Opcode | Name |")
    report.append("|--------|------|")
    for opcode, name in daily_recharge:
        report.append(f"| 0x{opcode:04X} | {name} |")
else:
    report.append("No daily recharge opcodes found in mapped range.")
report.append("")

# ================================================================
# 7. REWARD SYSTEMS (gifts, sign-in, online, etc.)
# ================================================================
print()
print("=" * 60)
print("  7. REWARD SYSTEMS")
print("=" * 60)

report.append("## 7. Reward / Gift Systems")
report.append("")

# All reward-related opcodes
reward_opcodes = []
for opcode, name in sorted(CMSG_OPCODES.items()):
    sname = strip_prefix(name).upper()
    if any(kw in sname for kw in ['REWARD', 'GIFT', 'SIGN', 'ONLINE_REWARD', 'DOWNLOAD_REWARD']):
        reward_opcodes.append((opcode, name))

report.append("### All Reward-Related Opcodes")
report.append("")
report.append("| Opcode | Name | Fire-and-Forget? |")
report.append("|--------|------|------------------|")
for opcode, name in reward_opcodes:
    sname = strip_prefix(name)
    # Check if request without return
    ff = "NO"
    if '_REQUEST' in sname:
        ret_name = name.replace('_REQUEST', '_RETURN')
        if ret_name not in name_to_opcode:
            ff = "YES - ABUSE TARGET"
    elif '_RETURN' not in sname and '_INFO' not in sname and 'SYN' not in sname and 'SYNC' not in sname:
        ff = "POSSIBLE"
    report.append(f"| 0x{opcode:04X} | {name} | {ff} |")
    print(f"  Reward: 0x{opcode:04X} = {name} [{ff}]")
report.append("")

# ================================================================
# 8. ALLIANCE FUND (AF) SYSTEM
# ================================================================
print()
print("=" * 60)
print("  8. ALLIANCE FUND SYSTEM")
print("=" * 60)

report.append("## 8. Alliance Fund (AF) System")
report.append("")

af_opcodes = []
for opcode, name in sorted(CMSG_OPCODES.items()):
    sname = strip_prefix(name).upper()
    if 'AF_' in sname or 'ALLIANCE_FUND' in sname or (0x0650 <= opcode <= 0x065F):
        af_opcodes.append((opcode, name))
        print(f"  AF opcode: 0x{opcode:04X} = {name}")

report.append("### AF Opcodes")
report.append("")
if af_opcodes:
    report.append("| Opcode | Name |")
    report.append("|--------|------|")
    for opcode, name in af_opcodes:
        report.append(f"| 0x{opcode:04X} | {name} |")
report.append("")

# AF symbols
af_syms = search_symbols(['AllianceFund', 'alliance_fund', 'AF_', 'AddAF'])
report.append("### AF Class Methods")
report.append("")
all_af = []
for pat, syms in af_syms.items():
    all_af.extend(syms)
all_af.sort(key=lambda x: x['name'])
seen_names = set()
for sym in all_af:
    if sym['name'] not in seen_names and sym['size'] > 0:
        seen_names.add(sym['name'])
        report.append(f"- `{sym['name']}` @ 0x{sym['value']:08X} (size={sym['size']})")
report.append("")

# ================================================================
# 9. MOBILIZATION / TASK PURCHASE
# ================================================================
print()
print("=" * 60)
print("  9. MOBILIZATION / MICROPAYMENT / DOWNLOAD REWARD")
print("=" * 60)

report.append("## 9. Mobilization, Micropayment, Download Reward")
report.append("")

mob_opcodes = []
for opcode, name in sorted(CMSG_OPCODES.items()):
    sname = strip_prefix(name).upper()
    if any(kw in sname for kw in ['MOBILIZATION', 'MICROPAY', 'DOWNLOAD_REWARD']):
        mob_opcodes.append((opcode, name))
        print(f"  Mob opcode: 0x{opcode:04X} = {name}")

report.append("### Mobilization/Micropayment Opcodes")
report.append("")
report.append("| Opcode | Name | Has Return? |")
report.append("|--------|------|-------------|")
for opcode, name in mob_opcodes:
    sname = strip_prefix(name)
    if '_REQUEST' in sname:
        ret_name = name.replace('_REQUEST', '_RETURN')
        has_ret = "YES" if ret_name in name_to_opcode else "NO"
    elif '_RETURN' in sname:
        has_ret = "(is return)"
    else:
        has_ret = "N/A"
    report.append(f"| 0x{opcode:04X} | {name} | {has_ret} |")
report.append("")

# ================================================================
# 10. DINAR BACK SYSTEM
# ================================================================
print()
print("=" * 60)
print("  10. DINAR BACK SYSTEM")
print("=" * 60)

report.append("## 10. Dinar Back System (0x1A90-0x1A91)")
report.append("")

dinar_opcodes = []
for opcode, name in sorted(CMSG_OPCODES.items()):
    sname = strip_prefix(name).upper()
    if 'DINAR' in sname or (0x1A90 <= opcode <= 0x1A95):
        dinar_opcodes.append((opcode, name))
        print(f"  Dinar opcode: 0x{opcode:04X} = {name}")

if dinar_opcodes:
    report.append("| Opcode | Name |")
    report.append("|--------|------|")
    for opcode, name in dinar_opcodes:
        report.append(f"| 0x{opcode:04X} | {name} |")
else:
    report.append("No DINAR opcodes found in mapped range.")
report.append("")

# Dinar strings
dinar_strings = search_strings(['dinar', 'Dinar', 'DINAR'])
report.append("### Dinar Strings")
report.append("")
all_dinar = []
for pat, matches in dinar_strings.items():
    for off, s in matches:
        all_dinar.append((off, s))
all_dinar.sort()
seen = set()
for off, s in all_dinar:
    if s not in seen:
        seen.add(s)
        report.append(f"- 0x{off:08X}: `{s[:120]}`")
report.append("")

# ================================================================
# 11. LUCKY / GACHA / TURNTABLE / RANDOM SYSTEMS
# ================================================================
print()
print("=" * 60)
print("  11. GACHA / TURNTABLE / RANDOM SYSTEMS")
print("=" * 60)

report.append("## 11. Gacha / Lucky / Turntable Systems")
report.append("")

gacha_opcodes = []
for opcode, name in sorted(CMSG_OPCODES.items()):
    sname = strip_prefix(name).upper()
    if any(kw in sname for kw in ['LUCKY', 'TURNTABLE', 'RANDOM', 'GACHA', 'DRAW', 'LOTTERY', 'SPIN']):
        gacha_opcodes.append((opcode, name))
        print(f"  Gacha: 0x{opcode:04X} = {name}")

report.append("### Gacha/Lucky Opcodes")
report.append("")
report.append("| Opcode | Name | Exploitable? |")
report.append("|--------|------|-------------|")
for opcode, name in gacha_opcodes:
    sname = strip_prefix(name)
    exploit = "POTENTIAL" if 'REQUEST' in sname and 'TURN' in sname.upper() else "LOW"
    report.append(f"| 0x{opcode:04X} | {name} | {exploit} |")
report.append("")

# Gacha strings
gacha_strings = search_strings(['lucky', 'turntable', 'gacha', 'lottery', 'spin', 'draw'])
report.append("### Gacha Strings")
report.append("")
all_gacha = []
for pat, matches in gacha_strings.items():
    for off, s in matches:
        all_gacha.append((off, s))
all_gacha.sort()
seen = set()
count = 0
for off, s in all_gacha:
    if s not in seen and count < 50:
        seen.add(s)
        report.append(f"- 0x{off:08X}: `{s[:120]}`")
        count += 1
report.append("")

# ================================================================
# 12. NOVICE FREE PURCHASE
# ================================================================
print()
print("=" * 60)
print("  12. NOVICE FREE PURCHASE SYSTEM")
print("=" * 60)

report.append("## 12. Novice Free Purchase System (0x0CB2-0x0CB6)")
report.append("")

novice_opcodes = []
for opcode, name in sorted(CMSG_OPCODES.items()):
    sname = strip_prefix(name).upper()
    if 'NOVICE' in sname or (0x0CB0 <= opcode <= 0x0CBA):
        novice_opcodes.append((opcode, name))
        print(f"  Novice: 0x{opcode:04X} = {name}")

if novice_opcodes:
    report.append("| Opcode | Name |")
    report.append("|--------|------|")
    for opcode, name in novice_opcodes:
        report.append(f"| 0x{opcode:04X} | {name} |")
else:
    report.append("No NOVICE opcodes in mapped range. Checking binary for references...")
report.append("")

# Search for novice strings
novice_strings = search_strings(['novice', 'Novice', 'NOVICE', 'free_purchase', 'FreePurchase'])
report.append("### Novice/FreePurchase Strings")
report.append("")
all_novice = []
for pat, matches in novice_strings.items():
    for off, s in matches:
        all_novice.append((off, s))
all_novice.sort()
seen = set()
for off, s in all_novice:
    if s not in seen:
        seen.add(s)
        report.append(f"- 0x{off:08X}: `{s[:120]}`")
report.append("")

# ================================================================
# 13. COMPREHENSIVE PAYMENT STRING SEARCH
# ================================================================
print()
print("=" * 60)
print("  13. COMPREHENSIVE PAYMENT STRING SEARCH")
print("=" * 60)

report.append("## 13. Comprehensive Payment/Monetization Strings")
report.append("")

# Deep search for all monetization-related strings
payment_patterns = [
    'price', 'cost', 'discount', 'free', 'premium',
    'subscription', 'bundle', 'offer', 'deal', 'promo',
    'refund', 'receipt', 'billing', 'wallet',
    'token', 'credit', 'point',
]
pay_results = search_strings(payment_patterns)

for pat in sorted(pay_results.keys()):
    matches = pay_results[pat]
    if matches:
        report.append(f"### '{pat}' strings ({len(matches)} found)")
        report.append("")
        seen = set()
        count = 0
        for off, s in sorted(matches):
            if s not in seen and count < 30:
                seen.add(s)
                report.append(f"- 0x{off:08X}: `{s[:120]}`")
                count += 1
        report.append("")
        print(f"  '{pat}': {len(matches)} matches")

# ================================================================
# 14. PAYMENT FLOW ANALYSIS
# ================================================================
print()
print("=" * 60)
print("  14. PAYMENT FLOW ANALYSIS")
print("=" * 60)

report.append("## 14. Payment Flow Analysis")
report.append("")
report.append("### Purchase Flow Patterns")
report.append("")
report.append("Typical purchase flow in IGG games:")
report.append("1. Client requests shop config (e.g., ROYAL_SHOP_ITEM_CONFIG_REQUEST)")
report.append("2. Server sends item configs with prices")
report.append("3. Client sends buy request (e.g., BUY_ROYAL_SHOP_ITEM_REQUEST)")
report.append("4. Server validates gold/gems, deducts, sends RETURN")
report.append("")
report.append("### Potential Abuse Vectors")
report.append("")

# Find all BUY requests without returns
buy_no_return = []
for opcode, name in sorted(CMSG_OPCODES.items()):
    sname = strip_prefix(name)
    if 'BUY' in sname.upper() and 'REQUEST' in sname.upper():
        ret_name = name.replace('_REQUEST', '_RETURN')
        if ret_name not in name_to_opcode:
            buy_no_return.append((opcode, name))

if buy_no_return:
    report.append("#### BUY Requests Without Returns (fire-and-forget)")
    report.append("")
    for opcode, name in buy_no_return:
        report.append(f"- **0x{opcode:04X}** {name} - No matching RETURN!")
    report.append("")
    report.append("These could potentially be spammed for free items if server")
    report.append("doesn't properly validate/rate-limit.")
else:
    report.append("All BUY requests have matching RETURN opcodes (server validates).")
report.append("")

# Find reward claims without returns
reward_no_return = []
for opcode, name in sorted(CMSG_OPCODES.items()):
    sname = strip_prefix(name).upper()
    if 'REWARD' in sname and 'REQUEST' in sname:
        ret_name = name.replace('_REQUEST', '_RETURN')
        if ret_name not in name_to_opcode:
            reward_no_return.append((opcode, name))

if reward_no_return:
    report.append("#### Reward Claims Without Returns")
    report.append("")
    for opcode, name in reward_no_return:
        report.append(f"- **0x{opcode:04X}** {name}")
    report.append("")

# ================================================================
# 15. UNMAPPED SHOP/PAYMENT OPCODES
# ================================================================
print()
print("=" * 60)
print("  15. SEARCHING FOR UNMAPPED PAYMENT OPCODES")
print("=" * 60)

report.append("## 15. Unmapped Payment Opcodes (Binary Search)")
report.append("")

# Search binary for opcode constants near known shop ranges
# Look for 2-byte little-endian values in .rodata matching shop ranges
shop_ranges_to_check = [
    ('ROYAL_SHOP extended', 0x0790, 0x07A0),
    ('REWARD_POINT_SHOP extended', 0x0AE0, 0x0B00),
    ('NOVICE_PURCHASE extended', 0x0CB0, 0x0CC0),
    ('DAILY_RECHARGE extended', 0x0EA0, 0x0EB0),
    ('INVEST extended', 0x0920, 0x0940),
    ('DINAR extended', 0x1A88, 0x1A98),
]

for range_name, start, end in shop_ranges_to_check:
    found_unmapped = []
    for op in range(start, end):
        if op not in CMSG_OPCODES:
            # Check if this value appears as a 2-byte LE constant
            needle = struct.pack('<H', op)
            pos = 0
            count = 0
            while True:
                pos = data.find(needle, pos)
                if pos < 0:
                    break
                count += 1
                pos += 1
            if count >= 3:  # appears multiple times = likely an opcode
                found_unmapped.append((op, count))

    if found_unmapped:
        report.append(f"### {range_name}")
        report.append("")
        for op, count in sorted(found_unmapped):
            report.append(f"- 0x{op:04X} (found {count}x in binary) - UNMAPPED")
        report.append("")
        print(f"  {range_name}: {len(found_unmapped)} unmapped values found")

# ================================================================
# 16. SUMMARY
# ================================================================
print()
print("=" * 60)
print("  16. WRITING SUMMARY")
print("=" * 60)

report.append("## 16. Summary")
report.append("")
report.append(f"- Total mapped opcodes: {len(CMSG_OPCODES)}")
report.append(f"- VIP opcodes found: {len(vip_opcodes)}")
report.append(f"- Charge/payment opcodes: {len(charge_opcodes)}")
report.append(f"- Shop opcodes: {len(shop_opcodes)}")
report.append(f"- Gold/gem opcodes: {len(gold_opcodes)}")
report.append(f"- Investment opcodes: {len(invest_opcodes)}")
report.append(f"- Daily recharge opcodes: {len(daily_recharge)}")
report.append(f"- Reward opcodes: {len(reward_opcodes)}")
report.append(f"- AF opcodes: {len(af_opcodes)}")
report.append(f"- Mobilization opcodes: {len(mob_opcodes)}")
report.append(f"- Dinar opcodes: {len(dinar_opcodes)}")
report.append(f"- Gacha/lucky opcodes: {len(gacha_opcodes)}")
report.append(f"- Novice opcodes: {len(novice_opcodes)}")
report.append(f"- BUY requests without RETURN: {len(buy_no_return)}")
report.append(f"- Reward requests without RETURN: {len(reward_no_return)}")
report.append("")

# Write output
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

print(f"\n[*] Report written to {OUTPUT_PATH}")
print(f"[*] Report size: {len(report)} lines")
print("[*] Done!")

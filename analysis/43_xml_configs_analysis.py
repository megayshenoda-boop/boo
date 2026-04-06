#!/usr/bin/env python3
"""
43_xml_configs_analysis.py
Extracts and analyzes all game configuration data from libgame.so (ARM64 ELF).
Searches .rodata for XML configs, URLs, error messages, debug strings, item types, JSON patterns.
"""

import struct
import re
import os
from collections import defaultdict

BINARY = r"D:\CascadeProjects\libgame.so"
OUTPUT = r"D:\CascadeProjects\analysis\findings\xml_configs_analysis.md"

# ── ELF parsing ──────────────────────────────────────────────────────────────

def parse_elf_sections(data):
    """Parse ELF64 section headers, return dict of name -> (offset, size)."""
    assert data[:4] == b'\x7fELF', "Not an ELF file"
    assert data[4] == 2, "Not 64-bit ELF"

    e_shoff = struct.unpack_from('<Q', data, 40)[0]
    e_shentsize = struct.unpack_from('<H', data, 58)[0]
    e_shnum = struct.unpack_from('<H', data, 60)[0]
    e_shstrndx = struct.unpack_from('<H', data, 62)[0]

    # Read shstrtab
    shstr_off = e_shoff + e_shstrndx * e_shentsize
    shstr_sh_offset = struct.unpack_from('<Q', data, shstr_off + 24)[0]
    shstr_sh_size = struct.unpack_from('<Q', data, shstr_off + 32)[0]
    shstrtab = data[shstr_sh_offset:shstr_sh_offset + shstr_sh_size]

    sections = {}
    for i in range(e_shnum):
        base = e_shoff + i * e_shentsize
        sh_name_idx = struct.unpack_from('<I', data, base)[0]
        sh_offset = struct.unpack_from('<Q', data, base + 24)[0]
        sh_size = struct.unpack_from('<Q', data, base + 32)[0]
        # Extract name
        end = shstrtab.index(b'\x00', sh_name_idx)
        name = shstrtab[sh_name_idx:end].decode('ascii', 'replace')
        sections[name] = (sh_offset, sh_size)
    return sections


def extract_strings(data, offset, size, min_len=4):
    """Extract null-terminated ASCII strings from a region."""
    region = data[offset:offset + size]
    results = []
    current = bytearray()
    start = 0
    for i, b in enumerate(region):
        if 0x20 <= b < 0x7f:
            if len(current) == 0:
                start = i
            current.append(b)
        else:
            if b == 0 and len(current) >= min_len:
                results.append((offset + start, current.decode('ascii', 'replace')))
            current = bytearray()
    return results


# ── Analysis functions ───────────────────────────────────────────────────────

def find_xml_configs(strings):
    """Find all .xml file references."""
    xml_files = []
    categories = defaultdict(list)

    cat_keywords = {
        'items': ['item', 'equip', 'gem', 'material', 'chest', 'box', 'gift', 'resource', 'loot', 'drop', 'reward', 'treasure', 'inventory', 'bag', 'prop', 'goods', 'consume'],
        'buildings': ['build', 'castle', 'city', 'wall', 'tower', 'gate', 'farm', 'mine', 'lumber', 'quarry', 'barrack', 'hospital', 'workshop', 'academy', 'prison', 'altar', 'hall', 'depot', 'embassy', 'watchtower', 'trap', 'shelter'],
        'troops': ['troop', 'soldier', 'army', 'unit', 'infantry', 'cavalry', 'archer', 'siege', 'warrior', 'knight', 'pikeman'],
        'research': ['research', 'tech', 'technology', 'science', 'study', 'academy'],
        'heroes': ['hero', 'leader', 'commander', 'skill', 'talent', 'star', 'familiar'],
        'maps': ['map', 'world', 'tile', 'kingdom', 'terrain', 'zone', 'region', 'coordinate', 'monster', 'darknest'],
        'quests': ['quest', 'mission', 'task', 'daily', 'event', 'campaign', 'chapter', 'stage', 'challenge'],
        'alliance': ['alliance', 'guild', 'clan', 'rally', 'war', 'battle', 'reinforce', 'help'],
        'vip': ['vip', 'privilege', 'premium', 'subscription'],
        'ui': ['ui', 'icon', 'panel', 'dialog', 'menu', 'hud', 'button', 'layout', 'window', 'popup', 'tip', 'guide', 'tutorial'],
        'localization': ['lang', 'language', 'locale', 'text', 'string', 'translate', 'i18n'],
        'audio': ['sound', 'audio', 'music', 'sfx', 'bgm', 'voice'],
        'animation': ['anim', 'spine', 'skeleton', 'effect', 'particle', 'action'],
        'chat': ['chat', 'message', 'mail', 'notice', 'announce'],
        'shop': ['shop', 'store', 'purchase', 'pay', 'iap', 'pack', 'bundle', 'offer', 'deal'],
        'gacha': ['gacha', 'summon', 'draw', 'roll', 'lottery', 'wheel', 'fortune'],
        'pvp': ['pvp', 'arena', 'colosseum', 'rank', 'league', 'season', 'match'],
    }

    for addr, s in strings:
        if s.lower().endswith('.xml'):
            xml_files.append((addr, s))
            categorized = False
            sl = s.lower()
            for cat, keywords in cat_keywords.items():
                if any(kw in sl for kw in keywords):
                    categories[cat].append((addr, s))
                    categorized = True
                    break
            if not categorized:
                categories['other'].append((addr, s))

    return xml_files, categories


def find_urls_and_endpoints(strings):
    """Find URLs, IPs, API paths, CDN paths."""
    urls = []
    ips = []
    api_paths = []
    cdn_paths = []

    ip_pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')

    for addr, s in strings:
        sl = s.lower()
        if sl.startswith('http://') or sl.startswith('https://'):
            urls.append((addr, s))
        elif ip_pattern.search(s) and not s.endswith('.xml') and not s.endswith('.png') and not s.endswith('.json'):
            ips.append((addr, s))
        elif sl.startswith('/api/') or sl.startswith('/v1/') or sl.startswith('/v2/') or '/api/' in sl:
            api_paths.append((addr, s))
        elif 'cdn' in sl or 'asset' in sl or 'download' in sl or 'update' in sl or 'patch' in sl:
            if '/' in s or '.' in s:
                cdn_paths.append((addr, s))

    return urls, ips, api_paths, cdn_paths


def find_error_messages(strings):
    """Find error/constraint messages."""
    error_keywords = [
        'error', 'fail', 'invalid', 'denied', 'cannot', 'not enough',
        'full', 'exceed', 'overflow', 'timeout', 'disconnect', 'reject',
        'forbidden', 'unauthorized', 'expired', 'locked', 'limit',
        'insufficient', 'unavailable', 'blocked', 'busy', 'cooldown',
        'maximum', 'minimum', 'already', 'duplicate', 'conflict',
        'mismatch', 'corrupt', 'broken', 'missing', 'empty',
        'not found', 'no permission', 'too many', 'too few',
        'not allow', 'illegal', 'abnormal', 'exception',
    ]
    results = []
    for addr, s in strings:
        sl = s.lower()
        if any(kw in sl for kw in error_keywords):
            if len(s) >= 8:  # skip very short matches
                results.append((addr, s))
    return results


def find_debug_strings(strings):
    """Find debug/log strings revealing game mechanics."""
    mechanic_keywords = {
        'march': ['march', 'marching', 'marchid', 'march_id'],
        'gather': ['gather', 'collecting', 'harvest', 'collect_resource'],
        'attack': ['attack', 'assault', 'strike', 'combat', 'damage', 'hit'],
        'scout': ['scout', 'scouting', 'explore', 'spy'],
        'rally': ['rally', 'rallying', 'war_rally'],
        'reinforce': ['reinforce', 'garrison', 'defend', 'support'],
        'train': ['train', 'training', 'recruit', 'conscript'],
        'build': ['build', 'construct', 'upgrade_build'],
        'research': ['research', 'studying', 'tech_research'],
        'upgrade': ['upgrade', 'level_up', 'evolve', 'enhance', 'promote'],
        'reward': ['reward', 'bonus', 'prize', 'claim'],
        'gift': ['gift', 'present', 'free_gift'],
        'chest': ['chest', 'treasure_chest', 'open_chest'],
        'box': ['box', 'loot_box', 'mystery_box'],
        'gacha': ['gacha', 'summon', 'lottery', 'draw', 'fortune_wheel'],
        'heal': ['heal', 'hospital', 'cure', 'recovery'],
        'shield': ['shield', 'peace_shield', 'bubble', 'protection'],
        'teleport': ['teleport', 'relocate', 'random_teleport', 'migration'],
        'speedup': ['speedup', 'speed_up', 'accelerate', 'boost', 'rush'],
        'alliance': ['alliance_help', 'alliance_war', 'alliance_gift', 'alliance_shop'],
    }

    results = defaultdict(list)
    for addr, s in strings:
        sl = s.lower()
        for category, keywords in mechanic_keywords.items():
            if any(kw in sl for kw in keywords):
                results[category].append((addr, s))
                break
    return results


def find_item_types(strings):
    """Find item type/category constants."""
    item_keywords = [
        'speedup', 'resource', 'equipment', 'gem', 'material',
        'scroll', 'boost', 'shield', 'teleport', 'buff',
        'food', 'stone', 'wood', 'ore', 'gold', 'coin',
        'stamina', 'energy', 'token', 'fragment', 'shard',
        'blueprint', 'rune', 'jewel', 'crystal', 'essence',
        'potion', 'elixir', 'medallion', 'insignia', 'badge',
        'key', 'ticket', 'voucher', 'coupon', 'chest',
        'helm', 'armor', 'weapon', 'boots', 'ring', 'amulet',
        'accessory', 'artifact', 'relic', 'trophy',
    ]
    results = []
    for addr, s in strings:
        sl = s.lower()
        if any(kw in sl for kw in item_keywords):
            if len(s) >= 4:
                results.append((addr, s))
    return results


def find_json_patterns(strings):
    """Find JSON-related strings."""
    json_keywords = ['"type"', '"id"', '"level"', '"name"', '"count"',
                     '"value"', '"data"', '"list"', '"items"', '"config"',
                     '"param"', '"result"', '"status"', '"code"', '"msg"',
                     '"time"', '"key"', '"index"', '"reward"', '"cost"',
                     '.json', 'json_', 'parse_json', 'to_json', 'from_json',
                     'rapidjson', 'cjson', 'nlohmann', 'json_spirit']
    results = []
    for addr, s in strings:
        sl = s.lower()
        if any(kw in sl for kw in json_keywords):
            results.append((addr, s))
    return results


# ── Report generation ────────────────────────────────────────────────────────

def generate_report(xml_files, xml_categories, urls, ips, api_paths, cdn_paths,
                    error_msgs, debug_strings, item_types, json_patterns):
    lines = []
    lines.append("# Game Configuration Data Analysis - libgame.so")
    lines.append("")
    lines.append("Extracted from ARM64 ELF binary `.rodata` section.")
    lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Category | Count |")
    lines.append(f"|---|---|")
    lines.append(f"| XML config files | {len(xml_files)} |")
    lines.append(f"| URLs | {len(urls)} |")
    lines.append(f"| IP addresses | {len(ips)} |")
    lines.append(f"| API paths | {len(api_paths)} |")
    lines.append(f"| CDN/asset paths | {len(cdn_paths)} |")
    lines.append(f"| Error messages | {len(error_msgs)} |")
    debug_total = sum(len(v) for v in debug_strings.values())
    lines.append(f"| Debug/mechanic strings | {debug_total} |")
    lines.append(f"| Item type strings | {len(item_types)} |")
    lines.append(f"| JSON-related strings | {len(json_patterns)} |")
    lines.append("")

    # 1. XML Configs
    lines.append("---")
    lines.append("## 1. XML Configuration Files")
    lines.append("")
    lines.append(f"**Total: {len(xml_files)} XML references found**")
    lines.append("")

    for cat in sorted(xml_categories.keys()):
        items = xml_categories[cat]
        lines.append(f"### {cat.title()} ({len(items)} files)")
        lines.append("")
        lines.append("| Offset | Filename |")
        lines.append("|---|---|")
        for addr, s in sorted(items, key=lambda x: x[1].lower()):
            lines.append(f"| `0x{addr:08X}` | `{s}` |")
        lines.append("")

    # 2. URLs and Endpoints
    lines.append("---")
    lines.append("## 2. URLs and Server Endpoints")
    lines.append("")

    lines.append("### URLs")
    lines.append("")
    if urls:
        lines.append("| Offset | URL |")
        lines.append("|---|---|")
        for addr, s in sorted(urls, key=lambda x: x[1]):
            lines.append(f"| `0x{addr:08X}` | `{s}` |")
    else:
        lines.append("*None found*")
    lines.append("")

    lines.append("### IP Addresses")
    lines.append("")
    if ips:
        lines.append("| Offset | String |")
        lines.append("|---|---|")
        for addr, s in sorted(set(ips), key=lambda x: x[1]):
            lines.append(f"| `0x{addr:08X}` | `{s}` |")
    else:
        lines.append("*None found*")
    lines.append("")

    lines.append("### API Paths")
    lines.append("")
    if api_paths:
        lines.append("| Offset | Path |")
        lines.append("|---|---|")
        for addr, s in sorted(api_paths, key=lambda x: x[1]):
            lines.append(f"| `0x{addr:08X}` | `{s}` |")
    else:
        lines.append("*None found*")
    lines.append("")

    lines.append("### CDN / Asset Paths")
    lines.append("")
    if cdn_paths:
        lines.append("| Offset | Path |")
        lines.append("|---|---|")
        for addr, s in sorted(cdn_paths, key=lambda x: x[1])[:200]:  # cap at 200
            lines.append(f"| `0x{addr:08X}` | `{s}` |")
        if len(cdn_paths) > 200:
            lines.append(f"| ... | *({len(cdn_paths) - 200} more)* |")
    else:
        lines.append("*None found*")
    lines.append("")

    # 3. Error Messages
    lines.append("---")
    lines.append("## 3. Error / Constraint Messages")
    lines.append("")
    lines.append(f"**Total: {len(error_msgs)} error strings found**")
    lines.append("")

    # Group by keyword
    error_groups = defaultdict(list)
    priority_keywords = ['not enough', 'full', 'limit', 'cannot', 'fail', 'invalid',
                         'denied', 'expired', 'locked', 'busy', 'cooldown',
                         'already', 'too many', 'not allow', 'error', 'timeout',
                         'disconnect', 'missing', 'insufficient']
    for addr, s in error_msgs:
        sl = s.lower()
        grouped = False
        for kw in priority_keywords:
            if kw in sl:
                error_groups[kw].append((addr, s))
                grouped = True
                break
        if not grouped:
            error_groups['other'].append((addr, s))

    for kw in priority_keywords + ['other']:
        if kw in error_groups:
            items = error_groups[kw]
            lines.append(f"### \"{kw}\" ({len(items)} strings)")
            lines.append("")
            for addr, s in sorted(items, key=lambda x: x[1])[:50]:
                lines.append(f"- `0x{addr:08X}`: `{s}`")
            if len(items) > 50:
                lines.append(f"- *...and {len(items)-50} more*")
            lines.append("")

    # 4. Debug/Mechanic Strings
    lines.append("---")
    lines.append("## 4. Debug / Game Mechanic Strings")
    lines.append("")
    lines.append(f"**Total: {debug_total} strings across {len(debug_strings)} categories**")
    lines.append("")

    for cat in sorted(debug_strings.keys()):
        items = debug_strings[cat]
        lines.append(f"### {cat.title()} ({len(items)} strings)")
        lines.append("")
        for addr, s in sorted(items, key=lambda x: x[1])[:80]:
            lines.append(f"- `0x{addr:08X}`: `{s}`")
        if len(items) > 80:
            lines.append(f"- *...and {len(items)-80} more*")
        lines.append("")

    # 5. Item Types
    lines.append("---")
    lines.append("## 5. Item Type / Category Constants")
    lines.append("")
    lines.append(f"**Total: {len(item_types)} item-related strings**")
    lines.append("")

    item_groups = defaultdict(list)
    item_cats = ['speedup', 'resource', 'equipment', 'gem', 'material', 'shield',
                 'teleport', 'boost', 'food', 'stone', 'wood', 'ore', 'gold',
                 'token', 'fragment', 'scroll', 'chest', 'key', 'weapon',
                 'armor', 'helm', 'boots', 'ring', 'amulet', 'artifact']
    for addr, s in item_types:
        sl = s.lower()
        grouped = False
        for ic in item_cats:
            if ic in sl:
                item_groups[ic].append((addr, s))
                grouped = True
                break
        if not grouped:
            item_groups['other'].append((addr, s))

    for ic in item_cats + ['other']:
        if ic in item_groups:
            items = item_groups[ic]
            lines.append(f"### {ic.title()} ({len(items)})")
            lines.append("")
            for addr, s in sorted(items, key=lambda x: x[1])[:40]:
                lines.append(f"- `0x{addr:08X}`: `{s}`")
            if len(items) > 40:
                lines.append(f"- *...and {len(items)-40} more*")
            lines.append("")

    # 6. JSON Patterns
    lines.append("---")
    lines.append("## 6. JSON-Related Strings")
    lines.append("")
    lines.append(f"**Total: {len(json_patterns)} JSON-related strings**")
    lines.append("")

    if json_patterns:
        lines.append("| Offset | String |")
        lines.append("|---|---|")
        for addr, s in sorted(json_patterns, key=lambda x: x[1])[:200]:
            # Escape pipe chars in markdown
            s_escaped = s.replace('|', '\\|')
            lines.append(f"| `0x{addr:08X}` | `{s_escaped}` |")
        if len(json_patterns) > 200:
            lines.append(f"| ... | *({len(json_patterns) - 200} more)* |")
    lines.append("")

    return '\n'.join(lines)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print(f"[*] Loading {BINARY} ...")
    with open(BINARY, 'rb') as f:
        data = f.read()
    print(f"    Size: {len(data):,} bytes")

    print("[*] Parsing ELF sections ...")
    sections = parse_elf_sections(data)
    for name in ['.rodata', '.dynstr', '.data', '.text']:
        if name in sections:
            off, sz = sections[name]
            print(f"    {name}: offset=0x{off:08X} size=0x{sz:08X} ({sz:,} bytes)")

    # Extract strings from .rodata (primary) and .dynstr (symbols)
    print("[*] Extracting strings from .rodata ...")
    rodata_off, rodata_sz = sections.get('.rodata', (0, 0))
    if rodata_sz == 0:
        # Fallback: scan entire file if .rodata not found
        print("    WARNING: .rodata not found, scanning full binary")
        rodata_off, rodata_sz = 0, len(data)

    strings = extract_strings(data, rodata_off, rodata_sz, min_len=4)
    print(f"    Found {len(strings):,} strings (min 4 chars)")

    # Also get dynstr strings
    dynstr_off, dynstr_sz = sections.get('.dynstr', (0, 0))
    if dynstr_sz > 0:
        print(f"[*] Extracting strings from .dynstr ...")
        dynstr_strings = extract_strings(data, dynstr_off, dynstr_sz, min_len=4)
        print(f"    Found {len(dynstr_strings):,} dynstr strings")
        strings.extend(dynstr_strings)

    # Also scan .data section
    data_off, data_sz = sections.get('.data', (0, 0))
    if data_sz > 0:
        print(f"[*] Extracting strings from .data ...")
        data_strings = extract_strings(data, data_off, data_sz, min_len=4)
        print(f"    Found {len(data_strings):,} data strings")
        strings.extend(data_strings)

    print(f"[*] Total strings to analyze: {len(strings):,}")

    # Run all analyses
    print("[*] Finding XML config files ...")
    xml_files, xml_categories = find_xml_configs(strings)
    print(f"    Found {len(xml_files)} XML files in {len(xml_categories)} categories")

    print("[*] Finding URLs and endpoints ...")
    urls, ips, api_paths, cdn_paths = find_urls_and_endpoints(strings)
    print(f"    URLs={len(urls)}, IPs={len(ips)}, APIs={len(api_paths)}, CDN={len(cdn_paths)}")

    print("[*] Finding error messages ...")
    error_msgs = find_error_messages(strings)
    print(f"    Found {len(error_msgs)} error strings")

    print("[*] Finding debug/mechanic strings ...")
    debug_strings = find_debug_strings(strings)
    total_debug = sum(len(v) for v in debug_strings.values())
    print(f"    Found {total_debug} strings in {len(debug_strings)} categories")

    print("[*] Finding item type constants ...")
    item_types = find_item_types(strings)
    print(f"    Found {len(item_types)} item strings")

    print("[*] Finding JSON patterns ...")
    json_patterns = find_json_patterns(strings)
    print(f"    Found {len(json_patterns)} JSON strings")

    # Generate report
    print("[*] Generating report ...")
    report = generate_report(xml_files, xml_categories, urls, ips, api_paths, cdn_paths,
                             error_msgs, debug_strings, item_types, json_patterns)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"[+] Report saved to {OUTPUT}")
    print(f"    Report size: {len(report):,} chars, {report.count(chr(10)):,} lines")


if __name__ == '__main__':
    main()

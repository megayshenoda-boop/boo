"""
Analysis Script 55: Arena/PvP/Expedition System Deep Analysis
Analyzes libgame.so for arena, colosseum, expedition, and PvP battle systems.
"""
import struct
import re
import os

LIBGAME = r"D:\CascadeProjects\libgame.so"
OUTPUT = r"D:\CascadeProjects\analysis\findings\arena_pvp_systems.md"

# Arena/PvP opcodes from CMSG map
ARENA_OPCODES = {
    0x05E6: ('AREN_HERO_QUEUE_INFO', 'S2C', 'Hero queue sync'),
    0x05E7: ('AREN_HERO_QUEUE_CHANGE_REQUEST', 'C2S', 'Change arena hero lineup'),
    0x05E8: ('AREN_HERO_QUEUE_CHANGE_RETURN', 'S2C', 'Change result'),
    0x05E9: ('ARENA_RANK_INFO_REQUEST', 'C2S', 'Request arena ranking'),
    0x05EA: ('ARENA_RANK_INFO_RETURN', 'S2C', 'Ranking data'),
    0x05EB: ('ARENA_TIMES_RESTORE_REQUEST', 'C2S', 'Restore arena attempts'),
    0x05EC: ('ARENA_BUY_TIMES_REQUEST', 'C2S', 'Buy more arena attempts'),
    0x05EE: ('ARENA_MATCH_INFO_RETURN', 'S2C', 'Match info'),
    0x05F0: ('ARENA_CHANGE_MATCH_RETURN', 'S2C', 'Change match result'),
    0x05F1: ('ARENA_CHALLENGE_MATCH_REQUEST', 'C2S', 'Start arena challenge'),
    0x05F2: ('ARENA_CHALLENGE_MATCH_RETURN', 'S2C', 'Challenge result'),
    0x05F4: ('SYNC_ARENA_INFO', 'S2C', 'Arena info sync'),
    0x05F5: ('ARENA_BATTLE_RECORD_INFO', 'S2C', 'Battle record'),
    0x05F6: ('ARENA_DELETE_BATTLE_RECORD_REQUEST', 'C2S', 'Delete battle record'),
    0x05F7: ('ARENA_DELETE_BATTLE_RECORD_RETURN', 'S2C', 'Delete result'),
    0x05F8: ('ARENA_SET_BATTLE_RECORD_FLAG_REQUEST', 'C2S', 'Flag battle record'),
    0x05F9: ('ARENA_SET_BATTLE_RECORD_FLAG_RETURN', 'S2C', 'Flag result'),
    # New-style encrypted
    0x0CF4: ('ARENA_MATCH_INFO_REQUEST_NEW', 'C2S', 'Arena match info (encrypted)'),
    0x0CF5: ('ARENA_CHANGE_MATCH_REQUEST_NEW', 'C2S', 'Change match (encrypted)'),
}

EXPEDITION_OPCODES = {
    0x02B2: ('EXPEDITION_INFO_REQUEST', 'C2S', 'Request expedition info'),
    0x02B3: ('EXPEDITION_INFO_RETURN', 'S2C', 'Expedition info'),
    0x02B5: ('RAID_PLAYER_ERROR_RETURN', 'S2C', 'Raid error'),
    0x02B6: ('EXPEDITION_BATTLE_REQUEST', 'C2S', 'Start expedition battle'),
    0x02B7: ('EXPEDITION_BUILDUP_REQUEST', 'C2S', 'Expedition buildup'),
}

RANK_OPCODES = {
    0x029E: ('RANK_INFO_REQUEST', 'C2S', 'Request ranking info'),
    0x029F: ('RANK_INFO_RETURN', 'S2C', 'Ranking data'),
    0x02A2: ('RANK_SIMPLE_INFO_REQUEST', 'C2S', 'Simple ranking'),
    0x02A3: ('RANK_SIMPLE_INFO_RETURN', 'S2C', 'Simple ranking data'),
}

BATTLE_OPCODES = {
    0x0176: ('BATTLE_DETAIL_REPORT_REQUEST', 'C2S', 'Request battle report'),
    0x0177: ('BATTLE_DETAIL_REPORT', 'S2C', 'Battle report data'),
    0x0751: ('CANNON_BATTLE_DAMAGE', 'S2C', 'Cannon battle damage event'),
}

# Raid/attack new-style
RAID_OPCODES = {
    0x0CF3: ('RAID_PLAYER_REQUEST_NEW', 'C2S', 'Raid player (encrypted)'),
}

def read_binary():
    with open(LIBGAME, 'rb') as f:
        return f.data if hasattr(f, 'data') else f.read()

def find_opcode_refs(data, opcode):
    """Find all locations where opcode appears as u16 LE."""
    target = struct.pack('<H', opcode)
    refs = []
    start = 0
    while True:
        idx = data.find(target, start)
        if idx == -1:
            break
        refs.append(idx)
        start = idx + 1
    return refs

def find_nearby_strings(data, offset, window=512):
    """Find readable strings near an offset."""
    start = max(0, offset - window)
    end = min(len(data), offset + window)
    chunk = data[start:end]
    strings = []
    for m in re.finditer(rb'[\x20-\x7e]{6,}', chunk):
        s = m.group().decode('ascii', errors='ignore')
        if any(kw in s.lower() for kw in ['arena', 'battle', 'hero', 'match', 'rank',
                                            'challenge', 'record', 'queue', 'fight',
                                            'expedition', 'raid', 'attack', 'cannon',
                                            'packdata', 'getdata', 'cmsg', 'send',
                                            'request', 'return', 'reward', 'times',
                                            'score', 'point', 'win', 'lose']):
            strings.append((m.start() + start, s))
    return strings

def find_packdata_near(data, offset, window=2048):
    """Search for packData/getData patterns near constructor."""
    start = max(0, offset - window)
    end = min(len(data), offset + window)
    chunk = data[start:end]
    results = []

    # Look for struct packing patterns (push/write calls)
    for pattern_name, pattern in [
        ('packData', b'packData'),
        ('getData', b'getData'),
        ('putShort', b'putShort'),
        ('putInt', b'putInt'),
        ('putLong', b'putLong'),
        ('putByte', b'putByte'),
        ('getShort', b'getShort'),
        ('getInt', b'getInt'),
        ('getLong', b'getLong'),
        ('getByte', b'getByte'),
    ]:
        idx = chunk.find(pattern)
        if idx != -1:
            results.append((pattern_name, idx + start))

    return results

def analyze_constructor_region(data, offset, opcode):
    """Analyze the region around an opcode reference for constructor patterns."""
    info = {
        'offset': offset,
        'strings': find_nearby_strings(data, offset),
        'pack_methods': find_packdata_near(data, offset),
        'has_packdata': False,
        'has_getdata': False,
        'payload_fields': [],
    }

    for name, _ in info['pack_methods']:
        if name == 'packData':
            info['has_packdata'] = True
        elif name == 'getData':
            info['has_getdata'] = True
        elif name.startswith('put'):
            info['payload_fields'].append(name)
        elif name.startswith('get'):
            info['payload_fields'].append(name)

    return info

def search_strings_bulk(data, keywords):
    """Search for all occurrences of keywords in binary."""
    results = {}
    for kw in keywords:
        kw_bytes = kw.encode('ascii')
        refs = []
        start = 0
        while True:
            idx = data.find(kw_bytes, start)
            if idx == -1:
                break
            # Get surrounding context
            ctx_start = max(0, idx - 50)
            ctx_end = min(len(data), idx + len(kw_bytes) + 100)
            ctx = data[ctx_start:ctx_end]
            readable = ''.join(chr(b) if 32 <= b < 127 else '.' for b in ctx)
            refs.append((idx, readable))
            start = idx + 1
        if refs:
            results[kw] = refs
    return results

def main():
    print("Loading libgame.so...")
    data = read_binary()
    print(f"  Size: {len(data):,} bytes")

    lines = []
    lines.append("# Arena / PvP / Expedition System Analysis")
    lines.append("=" * 70)
    lines.append("")
    lines.append("Generated by analysis script 55")
    lines.append("")

    # ============================================================
    # SECTION 1: Arena System
    # ============================================================
    lines.append("## 1. ARENA SYSTEM (Colosseum)")
    lines.append("-" * 50)
    lines.append("")
    lines.append("### Opcode Table")
    lines.append("")
    lines.append("| Opcode | Name | Dir | Notes |")
    lines.append("|--------|------|-----|-------|")

    all_opcodes = {}
    all_opcodes.update(ARENA_OPCODES)
    all_opcodes.update(EXPEDITION_OPCODES)
    all_opcodes.update(RANK_OPCODES)
    all_opcodes.update(BATTLE_OPCODES)
    all_opcodes.update(RAID_OPCODES)

    arena_analysis = {}

    for opcode in sorted(ARENA_OPCODES.keys()):
        name, direction, desc = ARENA_OPCODES[opcode]
        refs = find_opcode_refs(data, opcode)

        # Analyze best reference
        best_info = None
        for ref in refs[:5]:
            info = analyze_constructor_region(data, ref, opcode)
            if best_info is None or len(info['pack_methods']) > len(best_info['pack_methods']):
                best_info = info

        arena_analysis[opcode] = best_info

        pack_note = ""
        if best_info:
            if best_info['has_packdata']:
                pack_note += " [packData]"
            if best_info['has_getdata']:
                pack_note += " [getData]"
            if best_info['payload_fields']:
                pack_note += f" fields: {', '.join(best_info['payload_fields'][:5])}"

        lines.append(f"| 0x{opcode:04X} | {name} | {direction} | {desc}{pack_note} |")

    lines.append("")
    lines.append("### Arena Flow")
    lines.append("")
    lines.append("1. Client requests match info: 0x0CF4 (ARENA_MATCH_INFO_REQUEST_NEW)")
    lines.append("2. Server sends opponents: 0x05EE (ARENA_MATCH_INFO_RETURN)")
    lines.append("3. Client can refresh opponents: 0x0CF5 (ARENA_CHANGE_MATCH_REQUEST_NEW)")
    lines.append("4. Client challenges: 0x05F1 (ARENA_CHALLENGE_MATCH_REQUEST)")
    lines.append("5. Server returns result: 0x05F2 (ARENA_CHALLENGE_MATCH_RETURN)")
    lines.append("6. Ranking updates: 0x05F4 (SYNC_ARENA_INFO)")
    lines.append("")
    lines.append("### Arena Hero Queue")
    lines.append("")
    lines.append("- 0x05E6 SYNC: Server sends current hero lineup")
    lines.append("- 0x05E7 REQUEST: Client changes hero lineup for arena")
    lines.append("- 0x05E8 RETURN: Server confirms change")
    lines.append("")
    lines.append("### Arena Automation")
    lines.append("")
    lines.append("- Buy attempts: 0x05EC (fire-and-forget? check for RETURN)")
    lines.append("- Restore attempts: 0x05EB (fire-and-forget)")
    lines.append("- Auto-challenge: loop 0x0CF4 -> 0x05F1 -> wait 0x05F2 -> repeat")
    lines.append("- Note: 0x0CF4 and 0x0CF5 use NEW encrypted format (CMsgCodec)")
    lines.append("")

    # ============================================================
    # SECTION 2: Expedition System
    # ============================================================
    lines.append("## 2. EXPEDITION SYSTEM")
    lines.append("-" * 50)
    lines.append("")
    lines.append("| Opcode | Name | Dir | Notes |")
    lines.append("|--------|------|-----|-------|")

    for opcode in sorted(EXPEDITION_OPCODES.keys()):
        name, direction, desc = EXPEDITION_OPCODES[opcode]
        refs = find_opcode_refs(data, opcode)
        pack_info = ""
        for ref in refs[:3]:
            info = analyze_constructor_region(data, ref, opcode)
            if info['payload_fields']:
                pack_info = f" fields: {', '.join(info['payload_fields'][:5])}"
                break
        lines.append(f"| 0x{opcode:04X} | {name} | {direction} | {desc}{pack_info} |")

    lines.append("")
    lines.append("### Expedition Flow")
    lines.append("")
    lines.append("1. Request info: 0x02B2 -> Response: 0x02B3")
    lines.append("2. Battle: 0x02B6 (EXPEDITION_BATTLE_REQUEST)")
    lines.append("3. Buildup: 0x02B7 (EXPEDITION_BUILDUP_REQUEST)")
    lines.append("4. Raid errors: 0x02B5")
    lines.append("")

    # ============================================================
    # SECTION 3: Ranking System
    # ============================================================
    lines.append("## 3. RANKING SYSTEM")
    lines.append("-" * 50)
    lines.append("")
    lines.append("| Opcode | Name | Dir | Notes |")
    lines.append("|--------|------|-----|-------|")

    for opcode in sorted(RANK_OPCODES.keys()):
        name, direction, desc = RANK_OPCODES[opcode]
        lines.append(f"| 0x{opcode:04X} | {name} | {direction} | {desc} |")

    lines.append("")
    lines.append("- Ranking is read-only (C2S request, S2C data)")
    lines.append("- Can be used for reconnaissance: find top players, check power levels")
    lines.append("")

    # ============================================================
    # SECTION 4: Battle Reports
    # ============================================================
    lines.append("## 4. BATTLE REPORT SYSTEM")
    lines.append("-" * 50)
    lines.append("")
    lines.append("| Opcode | Name | Dir | Notes |")
    lines.append("|--------|------|-----|-------|")

    for opcode in sorted(BATTLE_OPCODES.keys()):
        name, direction, desc = BATTLE_OPCODES[opcode]
        lines.append(f"| 0x{opcode:04X} | {name} | {direction} | {desc} |")

    lines.append("")

    # ============================================================
    # SECTION 5: String Analysis - Hidden PvP Features
    # ============================================================
    lines.append("## 5. STRING ANALYSIS - Hidden PvP Features")
    lines.append("-" * 50)
    lines.append("")

    pvp_keywords = [
        'arena_auto', 'auto_arena', 'auto_challenge', 'auto_fight',
        'arena_reward', 'arena_rank', 'arena_score',
        'colosseum', 'colos',
        'expedition_auto', 'expedition_sweep',
        'battle_auto', 'auto_battle',
        'pvp_', 'duel_',
        'arena_shop', 'arena_buy',
        'arena_times', 'arena_free',
        'challenge_free', 'free_challenge',
    ]

    print("Searching for PvP-related strings...")
    string_results = search_strings_bulk(data, pvp_keywords)

    if string_results:
        for kw, refs in sorted(string_results.items()):
            lines.append(f"### String: '{kw}' ({len(refs)} refs)")
            for offset, ctx in refs[:3]:
                lines.append(f"  - 0x{offset:08X}: ...{ctx[40:110]}...")
            lines.append("")
    else:
        lines.append("No direct PvP automation strings found.")
        lines.append("")

    # Search for broader arena/battle strings
    print("Searching for broader arena strings...")
    broad_keywords = [
        'LogicArena', 'ArenaManager', 'ArenaView',
        'LogicExpedition', 'ExpeditionManager',
        'BattleManager', 'BattleResult',
        'ChallengeManager', 'MatchManager',
    ]
    broad_results = search_strings_bulk(data, broad_keywords)

    if broad_results:
        lines.append("### Class/Manager References")
        lines.append("")
        for kw, refs in sorted(broad_results.items()):
            lines.append(f"- **{kw}**: {len(refs)} references")
            for offset, ctx in refs[:2]:
                clean = ctx.strip('.')[:80]
                lines.append(f"  - 0x{offset:08X}: {clean}")
        lines.append("")

    # ============================================================
    # SECTION 6: Fire-and-Forget Analysis
    # ============================================================
    lines.append("## 6. FIRE-AND-FORGET ANALYSIS")
    lines.append("-" * 50)
    lines.append("")

    # Check which REQUEST opcodes have no RETURN
    request_opcodes = []
    return_opcodes = set()

    for opcode, (name, direction, _) in all_opcodes.items():
        if 'RETURN' in name:
            return_opcodes.add(opcode)
        elif 'REQUEST' in name:
            request_opcodes.append((opcode, name))

    lines.append("| Request Opcode | Name | Has RETURN? | Fire-and-Forget? |")
    lines.append("|---------------|------|-------------|-----------------|")

    for opcode, name in sorted(request_opcodes):
        # Check if there's a RETURN with opcode+1
        has_return = (opcode + 1) in return_opcodes or (opcode + 1) in all_opcodes
        ff = "YES - exploitable" if not has_return else "No"
        lines.append(f"| 0x{opcode:04X} | {name} | {'Yes' if has_return else 'NO'} | {ff} |")

    lines.append("")
    lines.append("### Exploitable Fire-and-Forget:")
    lines.append("")
    lines.append("- 0x05EB ARENA_TIMES_RESTORE: No RETURN opcode found")
    lines.append("  - Could potentially be spammed to restore arena attempts")
    lines.append("- 0x05EC ARENA_BUY_TIMES: No explicit RETURN (check 0x05ED)")
    lines.append("  - Buying attempts might not have server-side rate limit")
    lines.append("")

    # ============================================================
    # SECTION 7: Bot Automation Opportunities
    # ============================================================
    lines.append("## 7. BOT AUTOMATION OPPORTUNITIES")
    lines.append("-" * 50)
    lines.append("")
    lines.append("### Auto-Arena Bot Flow:")
    lines.append("```")
    lines.append("1. Send 0x0CF4 (ARENA_MATCH_INFO_REQUEST_NEW) - get opponents")
    lines.append("2. Parse 0x05EE response - pick weakest opponent")
    lines.append("3. Send 0x05F1 (ARENA_CHALLENGE_MATCH_REQUEST) - start fight")
    lines.append("4. Wait for 0x05F2 (ARENA_CHALLENGE_MATCH_RETURN) - result")
    lines.append("5. If attempts exhausted: 0x05EB or 0x05EC to get more")
    lines.append("6. Repeat until daily limit")
    lines.append("```")
    lines.append("")
    lines.append("### Auto-Expedition Bot Flow:")
    lines.append("```")
    lines.append("1. Send 0x02B2 (EXPEDITION_INFO_REQUEST) - get available stages")
    lines.append("2. Parse 0x02B3 response")
    lines.append("3. Send 0x02B6 (EXPEDITION_BATTLE_REQUEST) for each stage")
    lines.append("4. Repeat until all stages cleared")
    lines.append("```")
    lines.append("")
    lines.append("### Reconnaissance:")
    lines.append("```")
    lines.append("1. 0x029E (RANK_INFO_REQUEST) - get top players")
    lines.append("2. 0x0176 (BATTLE_DETAIL_REPORT_REQUEST) - read battle reports")
    lines.append("3. Use data to choose weakest targets for attack")
    lines.append("```")
    lines.append("")

    # ============================================================
    # SECTION 8: Vulnerability Notes
    # ============================================================
    lines.append("## 8. VULNERABILITY NOTES")
    lines.append("-" * 50)
    lines.append("")
    lines.append("### [MEDIUM] Arena Attempt Restoration Spam")
    lines.append("- 0x05EB (ARENA_TIMES_RESTORE_REQUEST) has no visible RETURN")
    lines.append("- May allow unlimited arena attempts if server doesn't track cooldown")
    lines.append("- Test: Send 0x05EB repeatedly, check if attempts increase")
    lines.append("")
    lines.append("### [MEDIUM] Arena Match Refresh Spam")
    lines.append("- 0x0CF5 (ARENA_CHANGE_MATCH_REQUEST_NEW) refreshes opponents")
    lines.append("- Keep refreshing until you find weak opponents")
    lines.append("- No known cooldown on refresh")
    lines.append("")
    lines.append("### [LOW] Battle Record Manipulation")
    lines.append("- 0x05F6 can delete battle records")
    lines.append("- 0x05F8 can flag records")
    lines.append("- Unlikely to be exploitable but worth testing")
    lines.append("")
    lines.append("### [MEDIUM] Expedition Skip/Bypass")
    lines.append("- 0x02B6 EXPEDITION_BATTLE_REQUEST might accept stage IDs out of order")
    lines.append("- Test: Send battle request for final stage without clearing earlier ones")
    lines.append("")
    lines.append("### [HIGH] New-Style Encrypted Arena Opcodes")
    lines.append("- 0x0CF4 and 0x0CF5 use CMsgCodec encryption")
    lines.append("- We have the codec cracked - can forge arena requests")
    lines.append("- Combined with auto-challenge: fully automated arena farming")
    lines.append("")

    # Write output
    print(f"Writing {len(lines)} lines to {OUTPUT}...")
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print("DONE - Arena/PvP analysis complete!")
    print(f"Output: {OUTPUT}")

if __name__ == '__main__':
    main()

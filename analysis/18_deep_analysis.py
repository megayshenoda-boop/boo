#!/usr/bin/env python3
"""
18_deep_analysis.py - Deep analysis of key constructors + vulnerability scan
=============================================================================
1. Disassemble 0x1B8B (PASSWORD_CHECK) constructor to find field layout
2. Disassemble 0x0CE8 (START_MARCH) constructor to find march fields
3. Disassemble other bot-useful constructors
4. Scan for hardcoded secrets, bypass patterns, interesting logic
"""
import struct, os, re
from capstone import *

LIBGAME = r"D:\CascadeProjects\libgame.so"
FINDINGS = r"D:\CascadeProjects\analysis\findings"
os.makedirs(FINDINGS, exist_ok=True)

with open(LIBGAME, "rb") as f:
    data = f.read()

text_addr, text_off, text_size = 0x3250E80, 0x3250E80, 43562076
rodata_addr, rodata_off, rodata_size = 0x255B000, 0x255B000, 4329528
dynstr_off = 0x682A10
dynsym_off, dynsym_size = 0x2F8, 0x3DA688

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

def disasm(addr, count=100):
    foff = text_off + (addr - text_addr)
    code = data[foff:foff + count * 4]
    lines = []
    for insn in md.disasm(code, addr):
        lines.append((insn.address, insn.mnemonic, insn.op_str))
    return lines

def read_string_at(addr):
    if rodata_addr <= addr < rodata_addr + rodata_size:
        off = rodata_off + (addr - rodata_addr)
        try:
            end = data.index(b'\x00', off, off + 200)
            return data[off:end].decode('ascii', errors='replace')
        except:
            pass
    return None

def resolve_adrp_add(insns, idx):
    """Resolve ADRP+ADD pair to get target address and string"""
    if idx + 1 >= len(insns):
        return None, None
    addr1, mnem1, op1 = insns[idx]
    addr2, mnem2, op2 = insns[idx + 1]
    if mnem1 != 'adrp' or mnem2 != 'add':
        return None, None
    try:
        page = int(op1.split('#')[1], 0)
        add_imm = int(op2.split('#')[1], 0)
        full = page + add_imm
        s = read_string_at(full)
        return full, s
    except:
        return None, None

def analyze_constructor(ctor_addr, name, count=200):
    """Analyze a CMSG constructor to find field layout"""
    result = {"name": name, "addr": ctor_addr, "fields": [], "strings": [], "calls": [], "stores": []}

    insns = disasm(ctor_addr, count)

    for i, (addr, mnem, ops) in enumerate(insns):
        # Track stores to understand field layout
        if mnem in ('strb', 'strh', 'str', 'stp', 'stur'):
            result["stores"].append(f"0x{addr:08X}: {mnem} {ops}")

        # Track string references
        if mnem == 'adrp':
            full, s = resolve_adrp_add(insns, i)
            if s and len(s) > 3:
                result["strings"].append(f"0x{addr:08X}: \"{s}\"")

        # Track function calls
        if mnem in ('bl', 'blr'):
            result["calls"].append(f"0x{addr:08X}: {mnem} {ops}")

        # Track MOV immediate values (potential field values/sizes)
        if mnem == 'mov' and '#' in ops:
            try:
                val = int(ops.split('#')[1].split(',')[0], 0)
                if 0 < val < 0x10000 and val not in (0, 1):
                    parts = ops.split(',')
                    reg = parts[0].strip()
                    result["fields"].append(f"0x{addr:08X}: {reg} = {val} (0x{val:X})")
            except:
                pass

        # Detect RET to find function boundary
        if mnem == 'ret' and addr > ctor_addr + 16:
            # Check if this is the actual end (not an early return)
            # Look for next function prologue
            if i + 1 < len(insns):
                next_addr, next_mnem, next_ops = insns[i + 1]
                if next_mnem in ('stp', 'sub') and ('sp' in next_ops):
                    break

    return result

def get_full_disasm(addr, count=150):
    """Get formatted disassembly text"""
    insns = disasm(addr, count)
    lines = []
    for a, m, o in insns:
        # Resolve strings inline
        if m == 'adrp':
            idx = insns.index((a, m, o))
            full, s = resolve_adrp_add(insns, idx)
            if s:
                lines.append(f"  0x{a:08X}: {m:10s} {o}  ; -> \"{s[:50]}\"")
                continue
        lines.append(f"  0x{a:08X}: {m:10s} {o}")

        if m == 'ret' and a > addr + 16:
            # Check next
            idx = insns.index((a, m, o))
            if idx + 1 < len(insns):
                na, nm, no = insns[idx + 1]
                if nm in ('stp', 'sub') and 'sp' in no:
                    lines.append(f"  ; --- END OF FUNCTION ---")
                    break
    return "\n".join(lines)

# Key constructors to analyze
targets = {
    0x0527367C: ("0x1B8B", "CMSG_PASSWORD_CHECK_REQUEST"),
    0x05212268: ("0x0CE8", "CMSG_START_MARCH_NEW"),
    0x05139714: ("0x0CE7", "CMSG_BACK_DEFEND_NEW (cancel march)"),
    0x052C6740: ("0x0CED", "CMSG_SOLDIER_NORMAL_PRODUCE_REQUEST_NEW (train)"),
    0x04FCC358: ("0x0CEF", "CMSG_BUILDING_OPERAT_REQUEST_NEW (build)"),
    0x052B4EFC: ("0x0CEE", "CMSG_SCIENCE_NORMAL_STUDY_REQUEST_NEW (research)"),
    0x051F53FC: ("0x0CEB", "CMSG_ENABLE_VIEW_NEW"),
    0x0527CA48: ("0x0042", "CMSG_KEEP_LIVE_TEST (heartbeat)"),
    0x0505D838: ("0x0038", "CMSG_EXTRA_ATTRIBUTE_INFO (init data)"),
}

# Also find interesting bot opcodes
# Search for specific CMSG names in the opcode map
bot_interesting = [
    "ITEM_USE", "ITEM_SELL", "SPEED_UP", "ONEKEY",
    "AUTO_JOIN", "REWARD", "VIP_STORE", "MARCH_QUEUE",
    "HERO_QUEUE", "GOLD_PRODUCE", "ACTIVITY_GAIN",
    "CHARGE", "FREE", "COLLECT", "REFRESH",
]

print("=" * 80)
print("DEEP ANALYSIS OF KEY CONSTRUCTORS")
print("=" * 80)

report = []
report.append("# Deep Constructor & Vulnerability Analysis")
report.append("")

# ============================================================
# PART 1: Key Constructor Analysis
# ============================================================
report.append("# PART 1: Key Constructor Disassembly")
report.append("")

for ctor_addr, (opcode_hex, name) in sorted(targets.items(), key=lambda x: x[1][0]):
    print(f"\nAnalyzing {opcode_hex} ({name}) at 0x{ctor_addr:08X}...")

    info = analyze_constructor(ctor_addr, name, 200)

    report.append(f"## {opcode_hex} - {name}")
    report.append(f"Constructor: 0x{ctor_addr:08X}")
    report.append("")

    # Full disassembly
    report.append("### Disassembly")
    report.append("```asm")
    report.append(get_full_disasm(ctor_addr, 150))
    report.append("```")
    report.append("")

    # Analysis summary
    report.append("### Analysis")
    if info["fields"]:
        report.append("**Immediate values (potential field sizes/IDs):**")
        for f in info["fields"][:20]:
            report.append(f"  - {f}")
    if info["strings"]:
        report.append("**String references:**")
        for s in info["strings"][:10]:
            report.append(f"  - {s}")
    if info["calls"]:
        report.append(f"**Function calls:** {len(info['calls'])}")
        for c in info["calls"][:10]:
            report.append(f"  - {c}")
    report.append(f"**Store instructions:** {len(info['stores'])}")
    report.append("")

# ============================================================
# PART 2: Find symbols near constructors for field info
# ============================================================
report.append("# PART 2: CMSG Symbol Analysis")
report.append("")

# Find all CMSG-related symbols with sizes
print("\nFinding CMSG symbols with field info...")
cmsg_symbols = []
for i in range(dynsym_size // 24):
    off = dynsym_off + i * 24
    st_name = struct.unpack_from('<I', data, off)[0]
    st_value = struct.unpack_from('<Q', data, off + 8)[0]
    st_size = struct.unpack_from('<Q', data, off + 16)[0]
    if st_value == 0:
        continue
    name_end = data.index(b'\x00', dynstr_off + st_name)
    name = data[dynstr_off + st_name:name_end].decode('ascii', errors='replace')

    # Look for our key CMSG types
    for key in ["PASSWORD_CHECK", "START_MARCH_NEW", "BACK_DEFEND", "SOLDIER_NORMAL_PRODUCE",
                "BUILDING_OPERAT", "SCIENCE_NORMAL_STUDY", "ENABLE_VIEW_NEW", "KEEP_LIVE"]:
        if key in name:
            cmsg_symbols.append((name, st_value, st_size))

report.append(f"Found {len(cmsg_symbols)} relevant CMSG symbols:")
report.append("")
report.append("| Symbol | Address | Size |")
report.append("|--------|---------|------|")
for name, addr, size in sorted(cmsg_symbols, key=lambda x: x[0])[:50]:
    # Demangle basic C++ names
    clean = re.sub(r'^_ZN\d+', '', name)
    clean = re.sub(r'E[A-Za-z0-9]*$', '', clean)
    report.append(f"| `{name[:80]}` | 0x{addr:08X} | {size} |")
report.append("")

# ============================================================
# PART 3: Vulnerability Analysis
# ============================================================
report.append("# PART 3: Vulnerability Analysis")
report.append("")

# 3a. Find hardcoded keys/secrets in .rodata
print("\nScanning for hardcoded secrets...")
secrets = []
secret_patterns = [
    (b'secret', 'secret'),
    (b'password', 'password'),
    (b'api_key', 'api_key'),
    (b'token', 'token'),
    (b'private', 'private'),
    (b'-----BEGIN', 'PEM key'),
    (b'AES', 'AES reference'),
    (b'RSA', 'RSA reference'),
    (b'SHA256', 'SHA256'),
    (b'HMAC', 'HMAC'),
]

for pattern, label in secret_patterns:
    idx = rodata_off
    count = 0
    examples = []
    while count < 20:
        idx = data.find(pattern, idx, rodata_off + rodata_size)
        if idx == -1:
            break
        # Read surrounding context
        start = max(idx - 20, rodata_off)
        end = min(idx + 60, rodata_off + rodata_size)
        try:
            nul = data.index(b'\x00', idx, end)
            s = data[max(idx-5, rodata_off):nul].decode('ascii', errors='replace')
            if s.isprintable() and len(s) > 3:
                examples.append(s.strip())
        except:
            pass
        idx += 1
        count += 1
    if examples:
        secrets.append((label, list(set(examples))[:5]))

report.append("## 3a. Hardcoded Secrets & Crypto References")
report.append("")
for label, examples in secrets:
    report.append(f"**{label}** ({len(examples)} unique):")
    for e in examples:
        report.append(f"  - `{e[:80]}`")
report.append("")

# 3b. Find validation bypass opportunities
print("Scanning for validation patterns...")
report.append("## 3b. Protocol Vulnerabilities")
report.append("")
report.append("### Known Weaknesses")
report.append("1. **Weak encryption**: XOR + add*17 with static 7-byte table - trivially reversible")
report.append("2. **Hardcoded CQ_secret**: Gateway token XOR key is in .rodata")
report.append("3. **No TLS**: Game protocol uses raw TCP with custom encoding")
report.append("4. **Single-byte server key**: Server key from 0x0038 is reused for all packets")
report.append("5. **Predictable checksum**: Just sum of encrypted bytes mod 256")
report.append("6. **Static CMSG_TABLE**: XOR table never changes, shared across all connections")
report.append("7. **No replay protection**: No nonce/sequence number in protocol (except msg random byte)")
report.append("")

# 3c. Interesting C2S opcodes for exploitation
report.append("## 3c. Interesting Opcodes for Bot/Exploit")
report.append("")

# Read the opcode map we generated
opcode_map = {}
try:
    with open(os.path.join(FINDINGS, "opcode_map_complete.md"), "r") as f:
        for line in f:
            if line.startswith("|") and "0x" in line:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 5:
                    try:
                        op = int(parts[2], 16)
                        name = parts[3]
                        opcode_map[op] = name
                    except:
                        pass
except:
    pass

# Categorize interesting opcodes
categories = {
    "Free Resources / Rewards": ["FREE", "REWARD", "GAIN", "COLLECT", "CLAIM", "GIFT"],
    "Speed / Skip": ["SPEED", "ONEKEY", "INSTANT", "SKIP", "FINISH", "QUICK"],
    "Item Manipulation": ["ITEM_USE", "ITEM_SELL", "ITEM_BUY", "BAG", "EQUIP"],
    "VIP / Premium": ["VIP", "CHARGE", "PREMIUM", "DIAMOND", "GEM"],
    "Auto / Helper": ["AUTO_JOIN", "AUTO_", "HELPER", "ASSIST"],
    "March / Attack": ["MARCH", "ATTACK", "RALLY", "SCOUT", "REINFORCE"],
    "Troop / Army": ["SOLDIER", "ARMY", "TROOP", "RECRUIT", "CURE", "TRAIN"],
    "Building": ["BUILDING", "CONSTRUCT", "UPGRADE"],
    "Research": ["SCIENCE", "RESEARCH", "STUDY", "TECH"],
    "Alliance": ["LEAGUE_DONATE", "LEAGUE_HELP", "LEAGUE_GIFT", "ALLIANCE"],
}

for cat_name, keywords in categories.items():
    matches = []
    for op, name in opcode_map.items():
        # Clean the C2E suffix
        clean_name = re.sub(r'C2E$', '', name)
        if any(kw in clean_name for kw in keywords):
            if "REQUEST" in clean_name or "SEND" in clean_name:  # C2S only
                matches.append((op, clean_name))
    if matches:
        report.append(f"### {cat_name} ({len(matches)} C2S opcodes)")
        for op, name in sorted(matches)[:15]:
            report.append(f"  - `0x{op:04X}` = {name}")
        if len(matches) > 15:
            report.append(f"  - ... and {len(matches) - 15} more")
        report.append("")

# ============================================================
# PART 4: Key insights summary
# ============================================================
report.append("# PART 4: Key Insights")
report.append("")
report.append("## 0x1B8B (PASSWORD_CHECK_REQUEST)")
report.append("- This is NOT a session heartbeat - it's a password/auth verification")
report.append("- Server sends this to verify account ownership mid-session")
report.append("- Sending wrong data causes immediate disconnect")
report.append("- Need to find: what hash/token format is expected")
report.append("")
report.append("## 0x0CE8 (START_MARCH_NEW)")
report.append("- Constructor sets up march parameters")
report.append("- Conditional opcode: bit flag selects 0x0CE8 vs 0x0D08")
report.append("- Fields likely include: target coords, march type, troop composition, hero IDs")
report.append("")
report.append("## Bot Automation Priority")
report.append("1. Fix 0x1B8B response (password check) - stops disconnects")
report.append("2. Implement reward collection (ACTIVITY_GAIN, REWARD_INFO)")
report.append("3. Implement item usage (ITEM_USE for speedups)")
report.append("4. Implement alliance help (AUTO_JOIN_BUILDUP)")
report.append("5. Implement march/gather once 0x1B8B is fixed")

# Write report
out_path = os.path.join(FINDINGS, "deep_analysis.md")
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print(f"\nReport written to {out_path} ({len(report)} lines)")

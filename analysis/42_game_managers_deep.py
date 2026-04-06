#!/usr/bin/env python3
"""Deep analysis of game manager classes and auto-features in libgame.so (ARM64 ELF)."""

import sys
import struct
import os
import re
from collections import defaultdict

sys.path.insert(0, r'D:\CascadeProjects\claude')
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

# --- Constants ---
LIBGAME_PATH = r'D:\CascadeProjects\libgame.so'
DYNSTR_OFF = 0x682A10
DYNSYM_OFF = 0x2F8
DYNSYM_SIZE = 0x682758
TEXT_OFF = 0x5B4D0
OUTPUT_PATH = r'D:\CascadeProjects\analysis\findings\game_managers_deep.md'

# Manager classes to analyze
KEY_MANAGERS = [
    'OneClickAccelerateManager',
    'AutoHangupManager',
    'AutoAttackRebelManager',
    'MarchManager',
    'GatherManager',
    'BattleManager',
    'AllianceManager',
    'MonsterManager',
    'ScoutManager',
]

# Deep disassembly targets (class, method keywords)
DEEP_TARGETS = {
    'AutoHangupManager': ['start', 'execute', 'request', 'send', 'run', 'do', 'tick', 'update', 'process'],
    'OneClickAccelerateManager': ['start', 'execute', 'request', 'send', 'run', 'do', 'tick', 'accelerate', 'speed'],
    'MarchManager': ['march', 'create', 'start', 'send', 'new', 'begin', 'dispatch'],
}

# Search categories
SEARCH_CATEGORIES = {
    'Auto Features': ['Auto', 'auto_', 'AUTO'],
    'VIP Related': ['VIP', 'Vip', 'vip'],
    'Shield/Protection': ['shield', 'Shield', 'peace', 'Peace', 'protect', 'Protect', 'bubble', 'Bubble'],
    'Speed/Boost': ['speed', 'Speed', 'accelerate', 'Accelerate', 'boost', 'Boost', 'buff', 'Buff'],
}


def load_binary():
    with open(LIBGAME_PATH, 'rb') as f:
        return f.read()


def parse_dynsym(data):
    """Parse ELF64 .dynsym entries. Each is 24 bytes: st_name(4) st_info(1) st_other(1) st_shndx(2) st_value(8) st_size(8)."""
    symbols = []
    end = DYNSYM_OFF + DYNSYM_SIZE
    i = DYNSYM_OFF
    while i + 24 <= end:
        st_name, st_info, st_other, st_shndx = struct.unpack_from('<IBBH', data, i)
        st_value, st_size = struct.unpack_from('<QQ', data, i + 8)
        i += 24
        # Read name from dynstr
        if st_name == 0:
            continue
        name_off = DYNSTR_OFF + st_name
        if name_off >= len(data):
            continue
        # Read null-terminated string
        end_name = data.index(b'\x00', name_off) if b'\x00' in data[name_off:name_off+512] else name_off
        name = data[name_off:end_name].decode('utf-8', errors='replace')
        if name:
            symbols.append({
                'name': name,
                'value': st_value,
                'size': st_size,
                'info': st_info,
                'shndx': st_shndx,
            })
    return symbols


def demangle_simple(name):
    """Basic C++ demangling for display - just return the raw name."""
    return name


def find_manager_methods(symbols, manager_name):
    """Find all symbols containing the manager class name."""
    methods = []
    for sym in symbols:
        if manager_name in sym['name']:
            methods.append(sym)
    methods.sort(key=lambda s: s['value'])
    return methods


def disassemble_function(data, addr, size, max_insns=200):
    """Disassemble a function at given virtual address."""
    cs = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
    cs.detail = True

    # Calculate file offset from virtual address
    # For a typical ELF, .text vaddr ~= file offset for PIE/shared libs
    # Try direct mapping first
    file_off = addr
    if file_off >= len(data) or file_off < TEXT_OFF:
        # Try with typical load address adjustments
        file_off = addr  # In shared libs, vaddr often == file offset

    if file_off >= len(data):
        return []

    chunk_size = min(size if size > 0 else max_insns * 4, max_insns * 4)
    chunk = data[file_off:file_off + chunk_size]

    instructions = []
    for insn in cs.disasm(chunk, addr):
        instructions.append(insn)
        if len(instructions) >= max_insns:
            break
        # Stop at RET
        if insn.mnemonic == 'ret':
            break
    return instructions


def find_opcodes_in_function(instructions):
    """Look for opcode constants in MOV/MOVZ/MOVK instructions."""
    opcodes_found = []
    for insn in instructions:
        if insn.mnemonic in ('mov', 'movz', 'movk'):
            # Check for immediate values that look like opcodes (0x0000-0x2000 range)
            op_str = insn.op_str
            # Extract immediate value
            m = re.search(r'#(0x[0-9a-fA-F]+|\d+)', op_str)
            if m:
                val = int(m.group(1), 0)
                if 0x20 <= val <= 0x2000:
                    opcodes_found.append((insn.address, insn.mnemonic, op_str, val))
    return opcodes_found


def find_bl_targets(instructions):
    """Find BL (branch-and-link = function call) targets."""
    calls = []
    for insn in instructions:
        if insn.mnemonic in ('bl', 'b'):
            m = re.search(r'#(0x[0-9a-fA-F]+)', insn.op_str)
            if m:
                target = int(m.group(1), 0)
                calls.append((insn.address, target))
    return calls


def search_symbols(symbols, patterns):
    """Search symbols for any of the given patterns."""
    results = []
    seen = set()
    for sym in symbols:
        for pat in patterns:
            if pat in sym['name'] and sym['name'] not in seen:
                results.append(sym)
                seen.add(sym['name'])
                break
    results.sort(key=lambda s: s['name'])
    return results


def build_addr_to_name(symbols):
    """Build a reverse lookup from address to symbol name."""
    addr_map = {}
    for sym in symbols:
        if sym['value'] != 0:
            addr_map[sym['value']] = sym['name']
    return addr_map


def main():
    print("[*] Loading libgame.so...")
    data = load_binary()
    print(f"    Size: {len(data):,} bytes")

    print("[*] Parsing dynsym...")
    symbols = parse_dynsym(data)
    print(f"    Found {len(symbols)} symbols")

    addr_map = build_addr_to_name(symbols)

    # Load known opcodes if available
    known_opcodes = {}
    try:
        sys.path.insert(0, r'D:\CascadeProjects\analysis\findings')
        from cmsg_opcodes import CMSG_OPCODES
        known_opcodes = {v: k for k, v in CMSG_OPCODES.items()}  # opcode -> name
        print(f"    Loaded {len(known_opcodes)} known opcode mappings")
    except ImportError:
        print("    [!] Could not load cmsg_opcodes.py")

    output_lines = []
    def out(line=""):
        output_lines.append(line)
        print(line)

    out("# Deep Game Manager Analysis - libgame.so")
    out(f"## Generated: 2026-04-04")
    out()

    # ========== TASK 1: Find all methods for key managers ==========
    out("---")
    out("## 1. Key Manager Class Methods")
    out()

    manager_methods = {}
    for mgr in KEY_MANAGERS:
        methods = find_manager_methods(symbols, mgr)
        manager_methods[mgr] = methods
        out(f"### {mgr} ({len(methods)} symbols)")
        out()
        if methods:
            out("| Address | Size | Symbol |")
            out("|---------|------|--------|")
            for m in methods:
                short_name = m['name']
                # Try to shorten very long mangled names
                if len(short_name) > 100:
                    short_name = short_name[:97] + "..."
                out(f"| 0x{m['value']:08X} | {m['size']} | `{short_name}` |")
            out()
        else:
            out("*No symbols found*\n")

    # ========== TASK 2: Deep disassembly of key methods ==========
    out("---")
    out("## 2. Deep Disassembly - Key Methods")
    out()

    for cls_name, keywords in DEEP_TARGETS.items():
        out(f"### {cls_name} - Key Method Analysis")
        out()
        methods = manager_methods.get(cls_name, [])
        if not methods:
            out("*No methods found for this class*\n")
            continue

        # Filter to methods matching keywords
        key_methods = []
        for m in methods:
            name_lower = m['name'].lower()
            for kw in keywords:
                if kw.lower() in name_lower:
                    key_methods.append(m)
                    break

        if not key_methods:
            # If no keyword match, take all methods
            key_methods = methods
            out(f"*No keyword matches, analyzing all {len(key_methods)} methods*\n")

        for m in key_methods:
            addr = m['value']
            size = m['size'] if m['size'] > 0 else 400
            if addr == 0 or addr >= len(data):
                continue

            out(f"#### `{m['name']}`")
            out(f"- Address: 0x{addr:08X}, Size: {size}")
            out()

            instructions = disassemble_function(data, addr, size)
            if not instructions:
                out("*Could not disassemble*\n")
                continue

            # Find opcodes
            opcodes = find_opcodes_in_function(instructions)
            if opcodes:
                out("**Potential opcode constants:**")
                out()
                out("| Insn Addr | Instruction | Value | Known CMSG |")
                out("|-----------|-------------|-------|------------|")
                for iaddr, mnem, ops, val in opcodes:
                    cmsg_name = known_opcodes.get(val, "?")
                    out(f"| 0x{iaddr:08X} | {mnem} {ops} | 0x{val:04X} ({val}) | {cmsg_name} |")
                out()

            # Find function calls
            calls = find_bl_targets(instructions)
            if calls:
                named_calls = []
                for caddr, target in calls:
                    tname = addr_map.get(target, f"0x{target:08X}")
                    named_calls.append((caddr, target, tname))

                # Show only interesting calls (skip plt stubs)
                interesting = [c for c in named_calls if not c[2].startswith('0x')]
                if interesting:
                    out("**Function calls:**")
                    out()
                    for caddr, target, tname in interesting[:20]:
                        short = tname[:120] if len(tname) > 120 else tname
                        out(f"- 0x{caddr:08X}: `{short}`")
                    out()

            # Show first N disassembled instructions
            out("<details><summary>Disassembly (first 40 insns)</summary>")
            out()
            out("```asm")
            for insn in instructions[:40]:
                out(f"  0x{insn.address:08X}: {insn.mnemonic:8s} {insn.op_str}")
            out("```")
            out("</details>")
            out()

    # ========== TASK 3-6: Symbol searches ==========
    out("---")
    out("## 3. Symbol Searches by Category")
    out()

    for cat_name, patterns in SEARCH_CATEGORIES.items():
        results = search_symbols(symbols, patterns)
        out(f"### {cat_name} ({len(results)} symbols)")
        out()
        if results:
            # Group by likely class
            by_class = defaultdict(list)
            for sym in results:
                # Try to extract class name from mangled symbol
                name = sym['name']
                # Look for common patterns like _ZN<len><classname>
                cm = re.search(r'_ZN\d+(\w+?)(?:\d+[a-z]|E)', name)
                if cm:
                    by_class[cm.group(1)].append(sym)
                else:
                    by_class['(other)'].append(sym)

            for cls, syms in sorted(by_class.items()):
                out(f"**{cls}** ({len(syms)} methods):")
                out()
                for s in syms[:30]:
                    sn = s['name'][:140]
                    out(f"- `{sn}` @ 0x{s['value']:08X}")
                if len(syms) > 30:
                    out(f"- ... and {len(syms)-30} more")
                out()
        else:
            out("*No symbols found*\n")

    # ========== TASK 7: MarchManager march creation flow ==========
    out("---")
    out("## 4. MarchManager - March Creation Flow")
    out()

    march_methods = manager_methods.get('MarchManager', [])
    march_create = [m for m in march_methods if any(kw in m['name'].lower() for kw in
                    ['create', 'start', 'new', 'begin', 'send', 'march', 'dispatch', 'request'])]

    if not march_create:
        march_create = march_methods  # Analyze all if no keyword match

    out(f"Found {len(march_create)} march-related methods to analyze:")
    out()

    for m in march_create:
        addr = m['value']
        size = m['size'] if m['size'] > 0 else 400
        if addr == 0 or addr >= len(data):
            continue

        out(f"#### `{m['name']}`")
        out(f"- Address: 0x{addr:08X}, Size: {size}")
        out()

        instructions = disassemble_function(data, addr, size)
        if not instructions:
            out("*Could not disassemble*\n")
            continue

        opcodes = find_opcodes_in_function(instructions)
        if opcodes:
            out("**Opcode constants found:**")
            out()
            for iaddr, mnem, ops, val in opcodes:
                cmsg_name = known_opcodes.get(val, "?")
                out(f"- 0x{iaddr:08X}: {mnem} {ops} => 0x{val:04X} = {cmsg_name}")
            out()

        calls = find_bl_targets(instructions)
        named_calls = [(ca, t, addr_map.get(t, f"0x{t:08X}")) for ca, t in calls]
        interesting = [c for c in named_calls if not c[2].startswith('0x')]
        if interesting:
            out("**Calls:**")
            out()
            for ca, t, tn in interesting[:15]:
                out(f"- `{tn[:120]}`")
            out()

        out("<details><summary>Disassembly</summary>")
        out()
        out("```asm")
        for insn in instructions[:50]:
            out(f"  0x{insn.address:08X}: {insn.mnemonic:8s} {insn.op_str}")
        out("```")
        out("</details>")
        out()

    # ========== Summary ==========
    out("---")
    out("## Summary")
    out()
    out("### Manager Method Counts")
    out()
    out("| Manager | Methods Found |")
    out("|---------|---------------|")
    for mgr in KEY_MANAGERS:
        count = len(manager_methods.get(mgr, []))
        out(f"| {mgr} | {count} |")
    out()

    # Count auto features
    auto_syms = search_symbols(symbols, ['Auto', 'auto_', 'AUTO'])
    auto_classes = set()
    for s in auto_syms:
        cm = re.search(r'_ZN\d+(\w*Auto\w*)', s['name'])
        if cm:
            auto_classes.add(cm.group(1))

    if auto_classes:
        out("### Auto-Feature Classes Found")
        out()
        for cls in sorted(auto_classes):
            out(f"- {cls}")
        out()

    # Write output
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    print(f"\n[*] Results saved to {OUTPUT_PATH}")
    print(f"    Total output lines: {len(output_lines)}")


if __name__ == '__main__':
    main()

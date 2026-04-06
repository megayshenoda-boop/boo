#!/usr/bin/env python3
"""
Disassemble CMSG_START_MARCH_NEW::packData (0x05212294, 1252 bytes)
and the constructor (0x05212268, ~44 bytes) from libgame.so to
produce the exact packet field layout for opcode 0x0CE8.

Output: findings/march_fields.md
"""

import os
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM, CS_GRP_CALL

LIBGAME = r"D:\CascadeProjects\libgame.so"
OUTPUT  = r"D:\CascadeProjects\analysis\findings\march_fields.md"

# .text section: file offset == virtual address (no ASLR shift)
TEXT_FILE_OFFSET = 0x3250E80
TEXT_VADDR       = 0x3250E80

# Addresses from symbol table
CTOR_ADDR     = 0x05212268
PACKDATA_ADDR = 0x05212294
PACKDATA_SIZE = 1252  # from symbol table
CTOR_SIZE     = PACKDATA_ADDR - CTOR_ADDR  # 44 bytes

# Known PLT helpers from previous analysis
KNOWN_PLT = {
    0x5c6dbd0: "write_u16",
    0x5c6dbe0: "write_u64_or_string",
    0x5c6dbc0: "get_server_key",
    0x5c6dbb0: "helper_unknown",
    0x5c6dba0: "encode_packet",
}


def va_to_file_offset(va):
    """Convert virtual address to file offset."""
    return va - TEXT_VADDR + TEXT_FILE_OFFSET


def read_bytes(f, va, size):
    """Read bytes from the ELF at a given virtual address."""
    offset = va_to_file_offset(va)
    f.seek(offset)
    data = f.read(size)
    if len(data) != size:
        raise ValueError(f"Short read at VA 0x{va:08X}: got {len(data)}, expected {size}")
    return data


def disassemble_function(md, code, base_addr, label="function"):
    """Disassemble code and return list of (addr, mnemonic, op_str, groups, detail) tuples."""
    instructions = []
    for insn in md.disasm(code, base_addr):
        instructions.append({
            'addr': insn.address,
            'mnemonic': insn.mnemonic,
            'op_str': insn.op_str,
            'bytes': bytes(insn.bytes),
            'size': insn.size,
            'groups': list(insn.groups) if insn.groups else [],
            'detail': insn,
        })
    return instructions


def resolve_bl_target(insn_dict):
    """Extract BL target address from op_str like '#0x5c6dbd0'."""
    op = insn_dict['op_str']
    if op.startswith('#'):
        try:
            return int(op[1:], 16)
        except ValueError:
            pass
    return None


def annotate_instruction(insn, prev_insns):
    """Add semantic annotation to an instruction."""
    mn = insn['mnemonic']
    op = insn['op_str']
    notes = []

    # BL calls
    if mn == 'bl':
        target = resolve_bl_target(insn)
        if target and target in KNOWN_PLT:
            notes.append(f"-> {KNOWN_PLT[target]}")
        elif target:
            notes.append(f"-> PLT 0x{target:08X}")

    # LDR variants from struct
    if mn in ('ldr', 'ldrb', 'ldrh', 'ldrsw', 'ldrsb', 'ldrsh', 'ldp', 'ldur', 'ldurh', 'ldurb'):
        if 'x19' in op or 'x20' in op:
            # Extract offset
            import re
            m = re.search(r'\[x(19|20)(?:,\s*#(0x[0-9a-fA-F]+|\d+))?\]', op)
            if m:
                reg = f"x{m.group(1)}"
                off = m.group(2)
                off_str = off if off else "0"
                size_map = {'ldr': '4/8', 'ldrb': '1', 'ldrh': '2', 'ldrsw': '4',
                            'ldrsb': '1', 'ldrsh': '2', 'ldur': '4/8', 'ldurh': '2', 'ldurb': '1'}
                sz = size_map.get(mn, '?')
                notes.append(f"STRUCT[{reg}+{off_str}] ({sz}B)")

    # MOV immediate
    if mn in ('mov', 'movz', 'movk', 'orr') and '#' in op:
        import re
        m = re.search(r'#(0x[0-9a-fA-F]+|\d+)', op)
        if m:
            val = int(m.group(1), 0)
            notes.append(f"imm={val} (0x{val:X})")

    # STR to struct (in packData, writes to stream buffer)
    if mn in ('str', 'strb', 'strh', 'stp', 'stur', 'sturh', 'sturb'):
        if 'x19' in op or 'x20' in op or 'x21' in op:
            notes.append("STORE to stream/struct")

    return "; ".join(notes)


def analyze_packdata(instructions):
    """Analyze packData instructions to extract serialization sequence."""
    bl_calls = []
    struct_loads = []
    mov_immediates = []
    serialization_sequence = []

    import re

    for i, insn in enumerate(instructions):
        mn = insn['mnemonic']
        op = insn['op_str']

        # Track BL calls
        if mn == 'bl':
            target = resolve_bl_target(insn)
            name = KNOWN_PLT.get(target, f"PLT_0x{target:08X}") if target else "unknown"
            bl_calls.append({'addr': insn['addr'], 'target': target, 'name': name})

            # Look back for the value being passed (in w1 or x1)
            source = "?"
            for j in range(max(0, i-8), i):
                prev = instructions[j]
                pmn = prev['mnemonic']
                pop = prev['op_str']
                # Check if w1 or x1 is being set
                if pmn in ('ldrh', 'ldrb', 'ldr', 'ldrsw', 'ldur', 'ldurh', 'ldurb') and pop.startswith(('w1,', 'x1,')):
                    m = re.search(r'\[x(19|20)(?:,\s*#(0x[0-9a-fA-F]+|\d+))?\]', pop)
                    if m:
                        reg = f"x{m.group(1)}"
                        off = m.group(2) if m.group(2) else "0"
                        size_map = {'ldr': 'u32/u64', 'ldrb': 'u8', 'ldrh': 'u16',
                                    'ldrsw': 's32', 'ldur': 'u32/u64', 'ldurh': 'u16', 'ldurb': 'u8'}
                        dtype = size_map.get(pmn, '?')
                        source = f"self[{reg}+{off}] as {dtype}"
                elif pmn == 'mov' and pop.startswith(('w1,', 'x1,')):
                    if 'w0' in pop or 'x0' in pop:
                        source = "return value of previous call"
                    elif '#' in pop:
                        m2 = re.search(r'#(0x[0-9a-fA-F]+|\d+)', pop)
                        if m2:
                            source = f"immediate {m2.group(1)}"

            serialization_sequence.append({
                'addr': insn['addr'],
                'call': name,
                'target': target,
                'source': source,
            })

        # Track struct loads
        if mn in ('ldr', 'ldrb', 'ldrh', 'ldrsw', 'ldrsb', 'ldrsh', 'ldp', 'ldur', 'ldurh', 'ldurb'):
            m = re.search(r'\[x(19|20)(?:,\s*#(0x[0-9a-fA-F]+|\d+))?\]', op)
            if m:
                reg = f"x{m.group(1)}"
                off = m.group(2) if m.group(2) else "0"
                size_map = {'ldr': 4, 'ldrb': 1, 'ldrh': 2, 'ldrsw': 4,
                            'ldrsb': 1, 'ldrsh': 2, 'ldur': 4, 'ldurh': 2, 'ldurb': 1}
                # For 64-bit loads, check destination register
                sz = size_map.get(mn, 0)
                if mn in ('ldr', 'ldur') and op.startswith('x'):
                    sz = 8
                struct_loads.append({
                    'addr': insn['addr'],
                    'reg': reg,
                    'offset': off,
                    'size': sz,
                    'dest': op.split(',')[0].strip(),
                })

        # Track MOV immediates
        if mn in ('mov', 'movz', 'movk') and '#' in op:
            m = re.search(r'#(0x[0-9a-fA-F]+|\d+)', op)
            if m:
                val = int(m.group(1), 0)
                mov_immediates.append({
                    'addr': insn['addr'],
                    'value': val,
                    'hex': f"0x{val:X}",
                    'op': op,
                })

    return bl_calls, struct_loads, mov_immediates, serialization_sequence


def format_disassembly(instructions, label):
    """Format instructions as annotated assembly."""
    lines = [f"; === {label} ==="]
    for insn in instructions:
        hex_bytes = insn['bytes'].hex().upper()
        annotation = annotate_instruction(insn, [])
        base = f"  0x{insn['addr']:08X}: {hex_bytes:12s}  {insn['mnemonic']:10s} {insn['op_str']}"
        if annotation:
            base += f"    ; {annotation}"
        lines.append(base)
    return "\n".join(lines)


def main():
    print(f"[*] Opening {LIBGAME}")
    with open(LIBGAME, "rb") as f:
        # Read constructor bytes
        ctor_code = read_bytes(f, CTOR_ADDR, CTOR_SIZE)
        print(f"[*] Read {len(ctor_code)} bytes for constructor at 0x{CTOR_ADDR:08X}")

        # Read packData bytes
        pd_code = read_bytes(f, PACKDATA_ADDR, PACKDATA_SIZE)
        print(f"[*] Read {len(pd_code)} bytes for packData at 0x{PACKDATA_ADDR:08X}")

    # Initialize capstone
    md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
    md.detail = True

    # Disassemble constructor
    print("[*] Disassembling constructor...")
    ctor_insns = disassemble_function(md, ctor_code, CTOR_ADDR, "constructor")
    print(f"    -> {len(ctor_insns)} instructions")

    # Disassemble packData
    print("[*] Disassembling packData...")
    pd_insns = disassemble_function(md, pd_code, PACKDATA_ADDR, "packData")
    print(f"    -> {len(pd_insns)} instructions")

    # Analyze packData
    print("[*] Analyzing packData serialization...")
    bl_calls, struct_loads, mov_imms, serial_seq = analyze_packdata(pd_insns)

    # Count BL call frequencies
    bl_freq = {}
    for call in bl_calls:
        key = (call['target'], call['name'])
        bl_freq[key] = bl_freq.get(key, 0) + 1

    # Format annotated disassembly
    ctor_disasm = format_disassembly(ctor_insns, "CMSG_START_MARCH_NEW::constructor (0x05212268)")
    pd_disasm = format_disassembly(pd_insns, "CMSG_START_MARCH_NEW::packData (0x05212294)")

    # Build output markdown
    out = []
    out.append("# CMSG_START_MARCH_NEW (0x0CE8) - packData Deep Analysis")
    out.append("")
    out.append("## Constructor Disassembly (0x05212268)")
    out.append("```asm")
    out.append(ctor_disasm)
    out.append("```")
    out.append("")

    out.append("## Constructor Struct Layout")
    out.append("From the constructor's store instructions:")
    out.append("```")
    out.append("Offset   Size   Value   Description")
    out.append("------   ----   -----   -----------")
    out.append("0x00     4      0x0CE8  opcode (stored as w8 = 0xCE80000, big-endian u32)")
    out.append("0x08     1      0       byte field (strb wzr)")
    out.append("0x10     8      0       zeroed (str xzr)")
    out.append("0x20     8      0       zeroed (str xzr)")
    out.append("0x28     16     0       zeroed (stp xzr,xzr -> 0x28-0x37)")
    out.append("0x35     8      0       zeroed (stur xzr, overlaps with 0x28 range)")
    out.append("0x48     2      0       zeroed (strh wzr)")
    out.append("0x50     8      0       zeroed (str xzr)")
    out.append("0x58     1      0       zeroed (strb wzr)")
    out.append("```")
    out.append("Struct spans at least 0x59 (89) bytes.")
    out.append("")

    out.append("## packData Full Annotated Disassembly (0x05212294)")
    out.append(f"Total instructions: {len(pd_insns)}")
    out.append("```asm")
    out.append(pd_disasm)
    out.append("```")
    out.append("")

    # PLT call summary
    out.append("## PLT Call Summary")
    out.append(f"Total BL calls: {len(bl_calls)}")
    out.append("")
    out.append("| Target Address | Name | Count |")
    out.append("|---|---|---|")
    for (target, name), count in sorted(bl_freq.items(), key=lambda x: -x[1]):
        out.append(f"| 0x{target:08X} | {name} | {count} |")
    out.append("")

    out.append("### All BL Calls in Order")
    out.append("| # | Address | Target | Name |")
    out.append("|---|---|---|---|")
    for i, call in enumerate(bl_calls, 1):
        out.append(f"| {i} | 0x{call['addr']:08X} | 0x{call['target']:08X} | {call['name']} |")
    out.append("")

    # Struct field accesses
    out.append("## Struct Field Accesses (loads from x19/x20)")
    out.append(f"Total struct loads: {len(struct_loads)}")
    out.append("")
    out.append("| Address | Register | Offset | Size | Dest Reg |")
    out.append("|---|---|---|---|---|")
    for sl in struct_loads:
        out.append(f"| 0x{sl['addr']:08X} | {sl['reg']} | {sl['offset']} | {sl['size']}B | {sl['dest']} |")
    out.append("")

    # Unique struct offsets accessed
    unique_offsets = {}
    for sl in struct_loads:
        off_key = (sl['reg'], sl['offset'])
        if off_key not in unique_offsets:
            unique_offsets[off_key] = sl
    out.append("### Unique Struct Fields Accessed")
    out.append("| Register | Offset | Size | First Access |")
    out.append("|---|---|---|---|")
    for (reg, off), sl in sorted(unique_offsets.items(), key=lambda x: (x[0][0], int(x[0][1], 0) if x[0][1].startswith('0x') else int(x[0][1]))):
        out.append(f"| {reg} | {off} | {sl['size']}B | 0x{sl['addr']:08X} |")
    out.append("")

    # MOV immediates
    out.append("## MOV Immediate Values")
    out.append(f"Total MOV imm instructions: {len(mov_imms)}")
    out.append("")
    out.append("| Address | Value (dec) | Value (hex) | Operand |")
    out.append("|---|---|---|---|")
    for mi in mov_imms:
        out.append(f"| 0x{mi['addr']:08X} | {mi['value']} | {mi['hex']} | {mi['op']} |")
    out.append("")

    # Serialization sequence
    out.append("## Serialization Sequence (BL calls with data sources)")
    out.append("This shows the ORDER in which fields are written to the packet buffer:")
    out.append("")
    out.append("| # | Address | PLT Call | Data Source |")
    out.append("|---|---|---|---|")
    for i, s in enumerate(serial_seq, 1):
        out.append(f"| {i} | 0x{s['addr']:08X} | {s['call']} | {s['source']} |")
    out.append("")

    # Expected march fields
    out.append("## Expected March Packet Fields")
    out.append("A march/gather packet (0x0CE8) logically needs:")
    out.append("")
    out.append("| Field | Expected Type | Notes |")
    out.append("|---|---|---|")
    out.append("| March type | u8/u16 | gather=4, attack=1, scout=6, rally=?, reinforce=? |")
    out.append("| Target X | u32 | world map X coordinate |")
    out.append("| Target Y | u32 | world map Y coordinate |")
    out.append("| Target kingdom | u16? | kingdom/server ID |")
    out.append("| Troop slots | array | each: troop_type(u32) + count(u32), typically 1-5 slots |")
    out.append("| Hero IDs | array | each: hero_id(u32), 1-3 heroes |")
    out.append("| Familiar IDs | array? | optional familiar slots |")
    out.append("| Equipment set | u8? | which gear set to use |")
    out.append("| Boost items | array? | optional march boost items |")
    out.append("| Target entity ID | u64? | for attacks: target player/castle ID |")
    out.append("")

    out.append("## Analysis Notes")
    out.append("")
    out.append("The packData function is 1252 bytes (~313 instructions), which is significantly")
    out.append("larger than simpler packets like TRAIN (19B payload) or BUILD (22B payload).")
    out.append("This suggests the march packet has many conditional fields and complex")
    out.append("serialization logic (e.g., variable-length troop arrays, optional hero slots).")
    out.append("")
    out.append("Key patterns to look for in the disassembly:")
    out.append("- Loops writing arrays (CBZ/CBNZ with counter registers)")
    out.append("- Conditional branches selecting different field sets based on march type")
    out.append("- write_u16 calls for enum values and counts")
    out.append("- write_u32/u64 calls for coordinates and IDs")
    out.append("")

    # Write output
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    print(f"[+] Output written to {OUTPUT}")
    print(f"    Constructor: {len(ctor_insns)} instructions")
    print(f"    packData: {len(pd_insns)} instructions")
    print(f"    BL calls: {len(bl_calls)} (unique targets: {len(bl_freq)})")
    print(f"    Struct loads: {len(struct_loads)} (unique offsets: {len(unique_offsets)})")
    print(f"    MOV immediates: {len(mov_imms)}")


if __name__ == "__main__":
    main()

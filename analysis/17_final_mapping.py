#!/usr/bin/env python3
"""
17_final_mapping.py - Map opcodes to CMSG names using .data.rel.ro vtables
===========================================================================
Strategy: Each CMSG struct has a vtable in .data.rel.ro that points to:
1. The constructor (which has the opcode)
2. A typeinfo pointer (which has the CMSG name string)

So: find vtable entries near constructor addresses, read typeinfo -> name
"""
import struct, os, re
from collections import defaultdict

LIBGAME = r"D:\CascadeProjects\libgame.so"
FINDINGS = r"D:\CascadeProjects\analysis\findings"
os.makedirs(FINDINGS, exist_ok=True)

with open(LIBGAME, "rb") as f:
    data = f.read()

# Section info
text_addr, text_off, text_size = 0x3250E80, 0x3250E80, 43562076
rodata_addr, rodata_off, rodata_size = 0x255B000, 0x255B000, 4329528
# .data.rel.ro
drelro_addr, drelro_off, drelro_size = 0x05C9BF00, 0x05C97F00, 0x607940
# .dynstr
dynstr_off = 0x682A10

text_data = data[text_off:text_off + text_size]

# ============================================================
# STEP 1: Find all opcodes from MOVZ LSL#16 + STR pattern
# ============================================================
print("Step 1: Finding opcodes from constructors...")
opcodes = {}  # opcode -> constructor_addr

for offset in range(0, text_size - 8, 4):
    insn = struct.unpack_from("<I", text_data, offset)[0]
    if (insn & 0xFFE00000) != 0x52A00000:
        continue
    imm16 = (insn >> 5) & 0xFFFF
    rd = insn & 0x1F
    if imm16 < 0x0020 or imm16 > 0x2000:
        continue
    for look in range(1, 5):
        look_off = offset + look * 4
        if look_off + 4 > text_size:
            break
        next_insn = struct.unpack_from("<I", text_data, look_off)[0]
        if (next_insn & 0xFFFFF800) == 0xB9000000 and (next_insn & 0x1F) == rd:
            opcodes[imm16] = text_addr + offset
            break

print(f"  Found {len(opcodes)} unique opcodes")

# ============================================================
# STEP 2: Build CMSG name -> address map from .rodata strings
# ============================================================
print("Step 2: Extracting CMSG strings...")
cmsg_name_addrs = {}  # string -> rodata address

idx = rodata_off
while True:
    idx = data.find(b'CMSG_', idx, rodata_off + rodata_size)
    if idx == -1:
        break
    end = idx
    while end < idx + 200 and data[end] != 0 and data[end] >= 0x20:
        end += 1
    s = data[idx:end].decode('ascii', errors='replace')
    if len(s) > 5:
        addr = rodata_addr + (idx - rodata_off)
        cmsg_name_addrs[s] = addr
    idx += 1

print(f"  Found {len(cmsg_name_addrs)} CMSG strings")

# ============================================================
# STEP 3: Scan .data.rel.ro for function pointers near constructors
# Each vtable entry has: [ptr_to_typeinfo, ptr_to_func1, ptr_to_func2, ...]
# typeinfo has: [vtable_ptr, name_ptr]
# ============================================================
print("Step 3: Scanning .data.rel.ro for vtables...")

# Build set of constructor addresses for fast lookup
ctor_addrs = set(opcodes.values())
ctor_to_opcode = {v: k for k, v in opcodes.items()}

# Scan .data.rel.ro for pointers to our constructors
ctor_refs = defaultdict(list)  # ctor_addr -> list of (drelro_offset, slot_index)

drelro_data = data[drelro_off:drelro_off + drelro_size]
for off in range(0, drelro_size - 8, 8):
    ptr = struct.unpack_from("<Q", drelro_data, off)[0]
    if ptr in ctor_addrs:
        drelro_addr_here = drelro_addr + off
        ctor_refs[ptr].append(drelro_addr_here)

print(f"  Found {sum(len(v) for v in ctor_refs.values())} vtable references to {len(ctor_refs)} constructors")

# ============================================================
# STEP 4: For each vtable ref, look backward for typeinfo pointer
# Vtable layout: [0]=typeinfo_ptr, [8+]=method_ptrs
# typeinfo: [0]=vtable_for_typeinfo, [8]=name_ptr (points to mangled name in .rodata)
# ============================================================
print("Step 4: Resolving typeinfo -> CMSG names...")

opcode_to_name = {}

for ctor_addr, refs in ctor_refs.items():
    opcode = ctor_to_opcode[ctor_addr]

    for ref_addr in refs:
        # The ctor is at some slot. Look backward for the typeinfo pointer
        # Try slots -1, -2, -3 (the ctor could be at different vtable offsets)
        for back in range(1, 8):
            ti_ptr_addr = ref_addr - back * 8
            if ti_ptr_addr < drelro_addr:
                continue
            ti_ptr_off = drelro_off + (ti_ptr_addr - drelro_addr)
            ti_ptr = struct.unpack_from("<Q", data, ti_ptr_off)[0]

            # typeinfo should be in .data.rel.ro too
            if not (drelro_addr <= ti_ptr < drelro_addr + drelro_size):
                continue

            # Read typeinfo: [8] = name pointer
            ti_off = drelro_off + (ti_ptr - drelro_addr)
            if ti_off + 16 > drelro_off + drelro_size:
                continue
            name_ptr = struct.unpack_from("<Q", data, ti_off + 8)[0]

            # Name should be in .rodata (mangled C++ name)
            if rodata_addr <= name_ptr < rodata_addr + rodata_size:
                name_off = rodata_off + (name_ptr - rodata_addr)
                end = data.index(b'\x00', name_off, name_off + 200)
                name = data[name_off:end].decode('ascii', errors='replace')

                # Look for CMSG in the name
                if 'CMSG' in name or 'cmsg' in name:
                    # Demangle: typically "4CMSG_NAME_HERE" format
                    clean = re.sub(r'^\d+', '', name)
                    if clean.startswith('CMSG_'):
                        opcode_to_name[opcode] = clean
                        break

        if opcode in opcode_to_name:
            break

print(f"  Mapped {len(opcode_to_name)} opcodes to CMSG names via vtables")

# ============================================================
# STEP 5: Alternative - match by proximity in .dynstr symbols
# ============================================================
print("Step 5: Trying symbol-based mapping for unmapped opcodes...")

# Find all CMSG symbols in .dynsym with their addresses
dynsym_off = 0x2F8
dynsym_size = 0x3DA688

cmsg_sym_addrs = {}  # function_addr -> demangled name
for i in range(dynsym_size // 24):
    off = dynsym_off + i * 24
    st_name = struct.unpack_from('<I', data, off)[0]
    st_value = struct.unpack_from('<Q', data, off + 8)[0]
    st_size = struct.unpack_from('<Q', data, off + 16)[0]

    if st_value == 0 or st_size == 0:
        continue
    if not (text_addr <= st_value < text_addr + text_size):
        continue

    name_end = data.index(b'\x00', dynstr_off + st_name)
    name = data[dynstr_off + st_name:name_end].decode('ascii', errors='replace')

    # Look for CMSG in symbol name
    if 'CMSG' not in name and 'cmsg' not in name:
        continue

    cmsg_sym_addrs[st_value] = name

print(f"  Found {len(cmsg_sym_addrs)} CMSG-related symbols with addresses")

# Match: find symbol closest to each unmapped constructor
for opcode, ctor_addr in opcodes.items():
    if opcode in opcode_to_name:
        continue

    best_dist = 999999
    best_name = None
    for sym_addr, sym_name in cmsg_sym_addrs.items():
        dist = abs(sym_addr - ctor_addr)
        if dist < best_dist and dist < 4096:  # within 4KB
            best_dist = dist
            best_name = sym_name

    if best_name:
        # Extract CMSG name from mangled symbol
        m = re.search(r'(CMSG_[A-Z0-9_]+)', best_name)
        if m:
            opcode_to_name[opcode] = m.group(1)

print(f"  Total mapped: {len(opcode_to_name)} opcodes")

# ============================================================
# STEP 6: Write all results
# ============================================================
print("Step 6: Writing results...")

# Sort by opcode
lines = []
lines.append("# Complete Opcode Map")
lines.append(f"# {len(opcodes)} opcodes found, {len(opcode_to_name)} mapped to CMSG names")
lines.append("")
lines.append("| Opcode | Hex | CMSG Name | Constructor | Direction |")
lines.append("|--------|-----|-----------|-------------|-----------|")

for opcode in sorted(opcodes.keys()):
    name = opcode_to_name.get(opcode, "")
    addr = opcodes[opcode]
    direction = ""
    if "REQUEST" in name or "SEND" in name:
        direction = "C2S"
    elif "RETURN" in name or "RECV" in name:
        direction = "S2C"
    elif "SYNC" in name or "SYN" in name:
        direction = "SYNC"
    lines.append(f"| {opcode} | 0x{opcode:04X} | {name} | 0x{addr:08X} | {direction} |")

# Write main opcode map
with open(os.path.join(FINDINGS, "opcode_map_complete.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# Write summary with known opcodes highlighted
known = {
    0x0020: "GAME_LOGIN", 0x0021: "WORLD_ENTRY", 0x0038: "INIT_DATA",
    0x0042: "HEARTBEAT", 0x0834: "FORMATION_SET",
    0x0CE7: "CANCEL_MARCH", 0x0CE8: "START_MARCH", 0x0D08: "ALT_MARCH",
    0x0CEB: "ENABLE_VIEW", 0x0CED: "TRAIN", 0x0CEE: "RESEARCH",
    0x0CEF: "BUILD", 0x1B8B: "SESSION_PKT",
}

summary = []
summary.append("# Key Opcodes Summary")
summary.append("")
summary.append("## Known Opcodes (from bot)")
summary.append("| Opcode | Our Name | CMSG Name | Constructor |")
summary.append("|--------|----------|-----------|-------------|")
for op, our_name in sorted(known.items()):
    cmsg = opcode_to_name.get(op, "NOT MAPPED")
    addr = opcodes.get(op, 0)
    summary.append(f"| 0x{op:04X} | {our_name} | {cmsg} | 0x{addr:08X} |")

summary.append("")
summary.append(f"## Statistics")
summary.append(f"- Total opcodes found: {len(opcodes)}")
summary.append(f"- Mapped to CMSG names: {len(opcode_to_name)}")
summary.append(f"- Unmapped: {len(opcodes) - len(opcode_to_name)}")
summary.append(f"- C2S (REQUEST/SEND): {sum(1 for n in opcode_to_name.values() if 'REQUEST' in n or 'SEND' in n)}")
summary.append(f"- S2C (RETURN/RECV): {sum(1 for n in opcode_to_name.values() if 'RETURN' in n or 'RECV' in n)}")
summary.append(f"- SYNC: {sum(1 for n in opcode_to_name.values() if 'SYNC' in n or 'SYN_' in n)}")

with open(os.path.join(FINDINGS, "key_opcodes.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(summary))

print(f"\nDone! Written:")
print(f"  findings/opcode_map_complete.md ({len(lines)} lines)")
print(f"  findings/key_opcodes.md ({len(summary)} lines)")

# Print key opcodes
print("\n=== KEY OPCODES ===")
for op, our_name in sorted(known.items()):
    cmsg = opcode_to_name.get(op, "NOT MAPPED")
    print(f"  0x{op:04X} {our_name:20s} = {cmsg}")

#!/usr/bin/env python3
"""
28_march_packdata.py - Disassemble CMSG_START_MARCH_NEW constructor + packData
===============================================================================
Constructor at 0x05212268, packData at 0x05212294 (1252 bytes)
Goal: Map EVERY field in the 46-byte march payload from ARM64 code.
"""
import struct, sys
sys.path.insert(0, r'D:\CascadeProjects\claude')
from capstone import *

LIBGAME = r"D:\CascadeProjects\libgame.so"
with open(LIBGAME, "rb") as f:
    data = f.read()

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

def disasm(addr, count=400):
    code = data[addr:addr + count * 4]
    return list(md.disasm(code, addr))

def fmt(i):
    return f"  0x{i.address:08X}: {i.mnemonic:10s} {i.op_str}"

# Known PLT stubs
PLT_NAMES = {
    0x05C6DBA0: "CMsgCodec::Encode",
    0x05C6DBB0: "CMsgCodec::NewEncode",
    0x05C6DBC0: "CMsgCodec::getServerKey",
    0x05C6DBD0: "CMsgCodec::getMsgIndex",
    0x05C6DBE0: "CMsgCodec::getCheckId",
}

# ═══════════════════════════════════════════════════════════════
# PART 1: Constructor (small, ~10 instructions)
# ═══════════════════════════════════════════════════════════════
print("=" * 80)
print("CMSG_START_MARCH_NEW Constructor (0x05212268)")
print("=" * 80)
insns = disasm(0x05212268, 20)
for i in insns:
    print(fmt(i))
    if i.mnemonic == 'ret' or (i.mnemonic == 'b' and i.address > 0x05212268 + 8):
        break

# ═══════════════════════════════════════════════════════════════
# PART 2: packData - full disassembly with annotations
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("CMSG_START_MARCH_NEW::packData (0x05212294, ~1252 bytes)")
print("=" * 80)

insns = disasm(0x05212294, 350)
bl_calls = {}
struct_reads = []  # (addr, reg, offset, size)

for i in insns:
    line = fmt(i)

    # Annotate BL calls
    if i.mnemonic == 'bl':
        try:
            target = int(i.op_str.split('#')[1], 0) if '#' in i.op_str else int(i.op_str, 0)
            if target in PLT_NAMES:
                line += f"  ; << {PLT_NAMES[target]} >>"
            bl_calls[target] = bl_calls.get(target, 0) + 1
        except: pass

    # Annotate struct field reads (ldr/ldrb/ldrh from x19 = this pointer)
    if i.mnemonic in ('ldrb', 'ldrh', 'ldr', 'ldrsb', 'ldrsh') and 'x19' in i.op_str:
        offset_str = i.op_str.split('#')[-1].rstrip(']') if '#' in i.op_str else ''
        try:
            offset = int(offset_str, 0)
            size = {'ldrb': 1, 'ldrsb': 1, 'ldrh': 2, 'ldrsh': 2, 'ldr': 4}.get(i.mnemonic, 0)
            if 'x' in i.op_str.split(',')[0].lower():
                size = 8  # ldr xN = 8 bytes
            struct_reads.append((i.address, i.mnemonic, offset, size))
            line += f"  ; << struct[0x{offset:X}] ({size}B) >>"
        except: pass

    # Annotate struct field reads from x21 (might also be this)
    if i.mnemonic in ('ldrb', 'ldrh', 'ldr') and 'x21' in i.op_str and '#' in i.op_str:
        offset_str = i.op_str.split('#')[-1].rstrip(']')
        try:
            offset = int(offset_str, 0)
            line += f"  ; << x21[0x{offset:X}] >>"
        except: pass

    # Annotate buffer writes (strb/strh/str to buffer)
    if i.mnemonic in ('strb', 'strh', 'str') and 'w8, uxtw' in i.op_str:
        line += "  ; << WRITE to buffer >>"

    print(line)

    # Stop at ret after significant code
    if i.mnemonic == 'ret' and i.address > 0x05212294 + 100:
        break

# ═══════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print("\nBL call counts:")
for addr, count in sorted(bl_calls.items()):
    name = PLT_NAMES.get(addr, f"0x{addr:08X}")
    print(f"  {name}: {count}x")

print(f"\nStruct field reads (from x19/this):")
for addr, mnem, offset, size in sorted(struct_reads, key=lambda x: x[2]):
    print(f"  0x{addr:08X}: {mnem} struct[0x{offset:02X}] ({size}B)")

# Deduplicate offsets
offsets = sorted(set((offset, size) for _, _, offset, size in struct_reads))
print(f"\nUnique struct fields:")
for offset, size in offsets:
    print(f"  offset 0x{offset:02X} ({size} bytes)")

#!/usr/bin/env python3
"""
23_newencode_disasm.py - Disassemble CMsgCodec::NewEncode at 0x04F97F40
Compare with CMsgCodec::Encode at 0x04F97C24 to find differences.
Also disassemble getMsgIndex and getCheckId helpers.
"""
import struct, sys
sys.path.insert(0, r'D:\CascadeProjects\claude')
from capstone import *

LIBGAME = r"D:\CascadeProjects\libgame.so"
with open(LIBGAME, "rb") as f:
    data = f.read()

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

def disasm_at(addr, count=100):
    code = data[addr:addr + count * 4]
    return list(md.disasm(code, addr))

def fmt(insn):
    return f"  0x{insn.address:08X}: {insn.mnemonic:10s} {insn.op_str}"

# ═══════════════════════════════════════════════════════════════
# CMsgCodec::NewEncode at 0x04F97F40 (size: 284 bytes = 71 insns)
# ═══════════════════════════════════════════════════════════════
print("=" * 80)
print("CMsgCodec::NewEncode (0x04F97F40) - 284 bytes")
print("=" * 80)
insns = disasm_at(0x04F97F40, 80)
for insn in insns:
    line = fmt(insn)
    # Annotate known patterns
    if insn.mnemonic == 'adrp' and '#0x28b7000' in insn.op_str:
        line += "  ; CMSG_TABLE page"
    if 'add' == insn.mnemonic and '#0x23a' in insn.op_str:
        line += "  ; CMSG_TABLE offset (0x028B723A)"
    if insn.mnemonic == 'mov' and '#0x2493' in insn.op_str:
        line += "  ; magic constant for %7"
    if insn.mnemonic == 'mov' and '#0xb7' in insn.op_str:
        line += "  ; XOR 0xB7 constant"
    print(line)
    if insn.mnemonic == 'ret' and insn.address > 0x04F97F40 + 32:
        break

# ═══════════════════════════════════════════════════════════════
# CMsgCodec::Encode at 0x04F97C24 for side-by-side comparison
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("CMsgCodec::Encode (0x04F97C24) - for comparison")
print("=" * 80)
insns = disasm_at(0x04F97C24, 80)
for insn in insns:
    line = fmt(insn)
    if insn.mnemonic == 'adrp' and '#0x28b7000' in insn.op_str:
        line += "  ; CMSG_TABLE page"
    if 'add' == insn.mnemonic and '#0x23a' in insn.op_str:
        line += "  ; CMSG_TABLE offset"
    if insn.mnemonic == 'mov' and '#0x2493' in insn.op_str:
        line += "  ; magic for %7"
    if insn.mnemonic == 'mov' and '#0xb7' in insn.op_str:
        line += "  ; XOR 0xB7"
    print(line)
    if insn.mnemonic == 'ret' and insn.address > 0x04F97C24 + 32:
        break

# ═══════════════════════════════════════════════════════════════
# getMsgIndex at 0x04F9828C (32 bytes)
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("CMsgCodec::getMsgIndex (0x04F9828C) - 32 bytes")
print("=" * 80)
insns = disasm_at(0x04F9828C, 12)
for insn in insns:
    print(fmt(insn))
    if insn.mnemonic == 'ret':
        break

# ═══════════════════════════════════════════════════════════════
# getCheckId at 0x04F982BC (16 bytes)
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("CMsgCodec::getCheckId (0x04F982BC) - 16 bytes")
print("=" * 80)
insns = disasm_at(0x04F982BC, 8)
for insn in insns:
    print(fmt(insn))
    if insn.mnemonic == 'ret':
        break

# ═══════════════════════════════════════════════════════════════
# getServerKey at 0x04F9826C (16 bytes)
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("CMsgCodec::getServerKey (0x04F9826C) - 16 bytes")
print("=" * 80)
insns = disasm_at(0x04F9826C, 8)
for insn in insns:
    print(fmt(insn))
    if insn.mnemonic == 'ret':
        break

# ═══════════════════════════════════════════════════════════════
# Function called before NewEncode in packData: 0x5bde0b0
# (same function called in standard Encode too)
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("Helper function at 0x05BDE0B0 (called by both Encode/NewEncode)")
print("=" * 80)
insns = disasm_at(0x05BDE0B0, 40)
for insn in insns:
    print(fmt(insn))
    if insn.mnemonic == 'ret' and insn.address > 0x05BDE0B0 + 16:
        break

print("\nDone.")

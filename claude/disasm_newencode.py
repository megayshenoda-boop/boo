#!/usr/bin/env python3
"""
Find and disassemble CMsgCodec::NewEncode, getMsgIndex, getCheckId, getServerKey
"""
import struct
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

LIBGAME = r"D:\CascadeProjects\libgame.so"
with open(LIBGAME, "rb") as f:
    data = f.read()

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

# Parse ELF to find .dynsym and .dynstr
elf_shoff = struct.unpack('<Q', data[0x28:0x30])[0]
elf_shentsize = struct.unpack('<H', data[0x3A:0x3C])[0]
elf_shnum = struct.unpack('<H', data[0x3C:0x3E])[0]
elf_shstrndx = struct.unpack('<H', data[0x3E:0x40])[0]

shstr_off = struct.unpack('<Q', data[elf_shoff + elf_shstrndx * elf_shentsize + 0x18:
                                     elf_shoff + elf_shstrndx * elf_shentsize + 0x20])[0]

sections = {}
for i in range(elf_shnum):
    sh = elf_shoff + i * elf_shentsize
    sh_name_idx = struct.unpack('<I', data[sh:sh+4])[0]
    sh_type = struct.unpack('<I', data[sh+4:sh+8])[0]
    sh_offset = struct.unpack('<Q', data[sh+0x18:sh+0x20])[0]
    sh_size = struct.unpack('<Q', data[sh+0x20:sh+0x28])[0]
    sh_entsize = struct.unpack('<Q', data[sh+0x38:sh+0x40])[0]
    name_end = data.index(b'\x00', shstr_off + sh_name_idx)
    name = data[shstr_off + sh_name_idx:name_end].decode('ascii', errors='replace')
    sections[name] = {'offset': sh_offset, 'size': sh_size, 'entsize': sh_entsize, 'type': sh_type}

# Find symbols in .dynsym
dynsym = sections['.dynsym']
dynstr_off = sections['.dynstr']['offset']

targets = ['NewEncode', 'getMsgIndex', 'getCheckId', 'getServerKey', 'Encode']
found = {}

num_syms = dynsym['size'] // dynsym['entsize']
for i in range(num_syms):
    off = dynsym['offset'] + i * dynsym['entsize']
    st_name = struct.unpack('<I', data[off:off+4])[0]
    st_value = struct.unpack('<Q', data[off+8:off+16])[0]
    st_size = struct.unpack('<Q', data[off+16:off+24])[0]
    
    name_end = data.index(b'\x00', dynstr_off + st_name)
    sym_name = data[dynstr_off + st_name:name_end].decode('ascii', errors='replace')
    
    if 'CMsgCodec' in sym_name and any(t in sym_name for t in targets):
        if st_value != 0:
            found[sym_name] = st_value
            print(f"  {sym_name} @ 0x{st_value:08X} (size={st_size})")

# Disassemble each found function
def disasm(addr, max_bytes=800, label=""):
    code = data[addr:addr + max_bytes]
    insns = list(md.disasm(code, addr))
    print(f"\n{'='*80}")
    print(f"  {label} @ 0x{addr:08X}")
    print(f"{'='*80}")
    for insn in insns:
        line = f"  0x{insn.address:08X}: {insn.mnemonic:10s} {insn.op_str}"
        # Annotate key values
        if insn.mnemonic in ('mov', 'movz', 'movk') and '#' in insn.op_str:
            try:
                v = int(insn.op_str.split('#')[1].split(',')[0], 0)
                if v == 0xB7: line += "  ; 0xB7 XOR constant"
                elif v == 0x2493: line += "  ; div7 magic"
            except: pass
        if insn.mnemonic == 'adrp' and '#' in insn.op_str:
            try:
                page = int(insn.op_str.split('#')[1], 0)
                line += f"  ; page=0x{page:08X}"
            except: pass
        print(line)
        if insn.mnemonic == 'ret':
            break

for name, addr in sorted(found.items(), key=lambda x: x[1]):
    short = name.split('::')[-1] if '::' in name else name
    # Demangle roughly
    for t in targets:
        if t in name:
            short = f"CMsgCodec::{t}"
            break
    disasm(addr, 800, short)

# Also check: what does CMsgCodec::Encode table at 0x28B723A look like?
# (Referenced in the Encode function)
print(f"\n{'='*80}")
print(f"  CMSG_TABLE at 0x028B723A (7 bytes)")
print(f"{'='*80}")
tbl = data[0x028B723A:0x028B723A+7]
print(f"  Bytes: {[hex(b) for b in tbl]}")
print(f"  Known CMSG_TABLE: [0x58, 0xEF, 0xD7, 0x14, 0xA2, 0x3B, 0x9C]")
print(f"  Match: {list(tbl) == [0x58, 0xEF, 0xD7, 0x14, 0xA2, 0x3B, 0x9C]}")

# Check if NewEncode uses the SAME table
# Look for adrp referencing the table page in NewEncode
print(f"\n{'='*80}")
print(f"  SEARCHING for table reference in NewEncode")
print(f"{'='*80}")
ne_addr = found.get('_ZN9CMsgCodec9NewEncodeEPhj', 0)
if ne_addr:
    code = data[ne_addr:ne_addr+800]
    insns = list(md.disasm(code, ne_addr))
    for insn in insns:
        if insn.mnemonic == 'adrp' and '#0x28b7000' in insn.op_str:
            print(f"  Found table page ref at 0x{insn.address:08X}: {insn.mnemonic} {insn.op_str}")
        if 'add' in insn.mnemonic and '#0x23a' in insn.op_str:
            print(f"  Found table offset at 0x{insn.address:08X}: {insn.mnemonic} {insn.op_str}")
        if insn.mnemonic == 'ret':
            break

print("\nDONE")

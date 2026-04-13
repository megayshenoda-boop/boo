"""Analyze CMSG_START_MARCH_EX vs CMSG_START_MARCH_NEW in libgame.so"""
import struct, re

BINARY = r"d:\CascadeProjects\libgame.so"
data = open(BINARY, "rb").read()

# Find all march-related packData symbols
print("=== MARCH VARIANTS ===\n")
march_syms = []
for m in re.finditer(rb'_ZN\d+(CMSG_START_MARCH[A-Z_]*)(\d+)(packData|getData)E', data):
    cls = m.group(1).decode()
    func = m.group(3).decode()
    march_syms.append((m.start(), cls, func))
    print(f"  0x{m.start():08X}: {cls}::{func}")

# Find CMSG_START_MARCH_EX packData address from symtab
print("\n=== Finding packData addresses from .symtab ===\n")

# ELF parsing to find symbol table
# Simple approach: search for known symbol names and nearby addresses
for name in [b'CMSG_START_MARCH_NEW8packData', b'CMSG_START_MARCH_EX8packData', b'CMSG_START_MARCH8packData']:
    # The mangled name pattern
    mangled = b'_ZN' + str(len(name.split(b'8')[0])).encode() + name.split(b'8')[0] + b'8packDataER8CIStream'
    for m in re.finditer(re.escape(mangled), data):
        print(f"  Found: {mangled.decode()} at str_offset 0x{m.start():08X}")

# Now search for the EX opcode
# The opcode is usually stored near the class constructor or in a vtable
# Let's look for numeric opcode assignments near CMSG_START_MARCH_EX
print("\n=== Searching for CMSG_START_MARCH_EX opcode ===\n")

# Find EX constructor - look for the pattern
ex_pattern = rb'CMSG_START_MARCH_EX'
for m in re.finditer(ex_pattern, data):
    ctx_start = max(0, m.start()-20)
    ctx = data[ctx_start:m.end()+60].replace(b'\x00', b'|')
    print(f"  0x{m.start():08X}: {ctx.decode('ascii', errors='replace')}")

# Look in .dynsym for the function addresses
# ELF64 format: e_shoff at offset 40 (8 bytes)
print("\n=== ELF Section Headers ===")
e_shoff = struct.unpack('<Q', data[40:48])[0]
e_shentsize = struct.unpack('<H', data[58:60])[0]
e_shnum = struct.unpack('<H', data[60:62])[0]
e_shstrndx = struct.unpack('<H', data[62:64])[0]
print(f"  Section headers at 0x{e_shoff:X}, size={e_shentsize}, count={e_shnum}")

# Read section headers
sections = []
for i in range(e_shnum):
    off = e_shoff + i * e_shentsize
    sh_name = struct.unpack('<I', data[off:off+4])[0]
    sh_type = struct.unpack('<I', data[off+4:off+8])[0]
    sh_offset = struct.unpack('<Q', data[off+24:off+32])[0]
    sh_size = struct.unpack('<Q', data[off+32:off+40])[0]
    sh_link = struct.unpack('<I', data[off+40:off+44])[0]
    sh_entsize = struct.unpack('<Q', data[off+56:off+64])[0]
    sections.append({
        'name_off': sh_name, 'type': sh_type, 'offset': sh_offset,
        'size': sh_size, 'link': sh_link, 'entsize': sh_entsize
    })

# Get section name string table
shstrtab = sections[e_shstrndx]
strtab_data = data[shstrtab['offset']:shstrtab['offset']+shstrtab['size']]

for i, s in enumerate(sections):
    name_end = strtab_data.find(b'\x00', s['name_off'])
    name = strtab_data[s['name_off']:name_end].decode('ascii', errors='replace')
    s['name'] = name

# Find .symtab and .strtab
symtab = None
strtab = None
dynsym = None
dynstr = None
for s in sections:
    if s['name'] == '.symtab': symtab = s
    if s['name'] == '.strtab': strtab = s
    if s['name'] == '.dynsym': dynsym = s
    if s['name'] == '.dynstr': dynstr = s

print(f"  .symtab: {'found' if symtab else 'NOT FOUND'}")
print(f"  .strtab: {'found' if strtab else 'NOT FOUND'}")
print(f"  .dynsym: {'found' if dynsym else 'NOT FOUND'}")
print(f"  .dynstr: {'found' if dynstr else 'NOT FOUND'}")

# Search in dynsym for march functions
if dynsym and dynstr:
    print("\n=== Dynamic Symbol Table: March functions ===\n")
    dynstr_data = data[dynstr['offset']:dynstr['offset']+dynstr['size']]
    ent_size = dynsym['entsize'] or 24  # ELF64 Sym entry size
    num_syms = dynsym['size'] // ent_size
    
    march_funcs = []
    for i in range(num_syms):
        off = dynsym['offset'] + i * ent_size
        st_name = struct.unpack('<I', data[off:off+4])[0]
        st_info = data[off+4]
        st_other = data[off+5]
        st_shndx = struct.unpack('<H', data[off+6:off+8])[0]
        st_value = struct.unpack('<Q', data[off+8:off+16])[0]
        st_size = struct.unpack('<Q', data[off+16:off+24])[0]
        
        name_end = dynstr_data.find(b'\x00', st_name)
        sym_name = dynstr_data[st_name:name_end].decode('ascii', errors='replace')
        
        if 'START_MARCH' in sym_name and 'pack' in sym_name.lower():
            print(f"  {sym_name}")
            print(f"    Address: 0x{st_value:08X}, Size: {st_size}")
            march_funcs.append((sym_name, st_value, st_size))
        
        # Also find HERO_SOLDIER_RECRUIT (0x0323)
        if 'HERO_SOLDIER_RECRUIT' in sym_name and 'pack' in sym_name.lower():
            print(f"  {sym_name}")
            print(f"    Address: 0x{st_value:08X}, Size: {st_size}")

# If we have .symtab, use that (more complete)
if symtab and strtab:
    print("\n=== Full Symbol Table: March + Hero functions ===\n")
    strtab_full = data[strtab['offset']:strtab['offset']+strtab['size']]
    ent_size = symtab['entsize'] or 24
    num_syms = symtab['size'] // ent_size
    print(f"  Total symbols: {num_syms}")
    
    for i in range(num_syms):
        off = symtab['offset'] + i * ent_size
        st_name = struct.unpack('<I', data[off:off+4])[0]
        st_value = struct.unpack('<Q', data[off+8:off+16])[0]
        st_size = struct.unpack('<Q', data[off+16:off+24])[0]
        
        if st_name >= len(strtab_full):
            continue
        name_end = strtab_full.find(b'\x00', st_name)
        sym_name = strtab_full[st_name:name_end].decode('ascii', errors='replace')
        
        if ('START_MARCH' in sym_name or 'HERO_SOLDIER' in sym_name) and ('pack' in sym_name.lower() or 'getData' in sym_name):
            print(f"  {sym_name}")
            print(f"    Addr: 0x{st_value:08X}, Size: {st_size}")

print("\nDone.")

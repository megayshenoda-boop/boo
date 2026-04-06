#!/usr/bin/env python3
"""
37_remaining_opcodes.py - Find the remaining ~1400 opcodes
==========================================================
The NEW-style opcodes (0x0CE4-0x0CFB range) use a different pattern.
They're created by a generic base class and opcode is set via a table/switch.

Strategy:
1. Find all _NEW suffix CMSGs in dynsym
2. Search for opcode constants in .text near function references
3. Look for the opcode dispatch table
"""
import struct, re, sys
sys.path.insert(0, r'D:\CascadeProjects\claude')
from capstone import *

LIBGAME = r"D:\CascadeProjects\libgame.so"
with open(LIBGAME, "rb") as f:
    data = f.read()

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

DYNSTR_OFF = 0x682A10
DYNSYM_OFF = 0x2F8
DYNSYM_SIZE = 0x682758

out = []
def p(msg):
    out.append(msg)

# ═══════════════════════════════════════════════════════════════
# 1. Find ALL _NEW suffix CMSG functions
# ═══════════════════════════════════════════════════════════════
p("# Remaining Opcode Analysis")
p("=" * 60)

new_cmsgs = {}
pos = DYNSYM_OFF
while pos + 24 <= DYNSYM_OFF + DYNSYM_SIZE:
    st_name = struct.unpack('<I', data[pos:pos+4])[0]
    st_value = struct.unpack('<Q', data[pos+8:pos+16])[0]
    st_size = struct.unpack('<Q', data[pos+16:pos+24])[0]
    if st_name > 0 and st_name < 0x200000 and st_value > 0:
        name_end = data.index(b'\x00', DYNSTR_OFF + st_name)
        name = data[DYNSTR_OFF + st_name:name_end].decode('ascii', errors='replace')
        # Find _NEW packData or C1Ev
        if '_NEW' in name and ('8packData' in name or 'C1Ev' in name):
            m = re.search(r'(CMSG_[A-Z0-9_]+_NEW)', name)
            if m:
                cmsg = m.group(1)
                if cmsg not in new_cmsgs:
                    new_cmsgs[cmsg] = {}
                if '8packData' in name:
                    new_cmsgs[cmsg]['packdata'] = (st_value, st_size)
                elif 'C1Ev' in name:
                    new_cmsgs[cmsg]['ctor'] = (st_value, st_size)
    pos += 24

p(f"\n## _NEW CMSGs found: {len(new_cmsgs)}")
for name in sorted(new_cmsgs.keys()):
    info = new_cmsgs[name]
    ctor = info.get('ctor', (0,0))
    pack = info.get('packdata', (0,0))
    p(f"  {name}")
    if ctor[0]: p(f"    ctor: 0x{ctor[0]:08X} ({ctor[1]}B)")
    if pack[0]: p(f"    pack: 0x{pack[0]:08X} ({pack[1]}B)")

# ═══════════════════════════════════════════════════════════════
# 2. Analyze _NEW constructors - they may set opcode differently
# ═══════════════════════════════════════════════════════════════
p(f"\n\n## _NEW Constructor Analysis")

# For _NEW types, constructor might call base class with opcode parameter
for name in sorted(new_cmsgs.keys()):
    info = new_cmsgs[name]
    if 'ctor' not in info:
        continue
    addr, size = info['ctor']
    if addr == 0 or size == 0:
        continue

    max_bytes = min(size, 200)
    code = data[addr:addr + max_bytes]
    insns = list(md.disasm(code, addr))

    # Look for MOV with immediate values that could be opcodes
    for insn in insns[:20]:
        if insn.mnemonic == 'ret':
            break
        if insn.mnemonic in ('mov', 'movz') and '#' in insn.op_str:
            try:
                imm_str = insn.op_str.split('#')[-1].split(',')[0].strip()
                imm = int(imm_str, 0)
                # Check if it looks like an opcode (shifted or not)
                if imm >= 0x10000 and (imm & 0xFFFF) == 0:
                    opcode = (imm >> 16) & 0xFFFF
                    if 0x0001 <= opcode <= 0x2000:
                        p(f"  {name}: opcode = 0x{opcode:04X}")
                elif 0x0001 <= imm <= 0x2000:
                    p(f"  {name}: possible opcode = 0x{imm:04X} (direct)")
            except:
                pass

# ═══════════════════════════════════════════════════════════════
# 3. Find ALL remaining CMSGs that have packData but NOT in our map
# ═══════════════════════════════════════════════════════════════
p(f"\n\n## ALL CMSGs with packData (comprehensive)")

# Load existing map
existing = set()
try:
    sys.path.insert(0, r'D:\CascadeProjects\analysis\findings')
    from cmsg_opcodes import CMSG_OPCODES
    existing = set(CMSG_OPCODES.values())
except:
    pass

all_packdata = {}
pos = DYNSYM_OFF
while pos + 24 <= DYNSYM_OFF + DYNSYM_SIZE:
    st_name = struct.unpack('<I', data[pos:pos+4])[0]
    st_value = struct.unpack('<Q', data[pos+8:pos+16])[0]
    st_size = struct.unpack('<Q', data[pos+16:pos+24])[0]
    if st_name > 0 and st_name < 0x200000 and st_value > 0:
        name_end = data.index(b'\x00', DYNSTR_OFF + st_name)
        name = data[DYNSTR_OFF + st_name:name_end].decode('ascii', errors='replace')
        if '8packData' in name:
            m = re.search(r'(CMSG_[A-Z0-9_]+)', name)
            if m:
                cmsg = m.group(1)
                all_packdata[cmsg] = (st_value, st_size)
    pos += 24

# Find ones NOT in existing map
unmapped = {}
for cmsg, (addr, size) in all_packdata.items():
    if cmsg not in existing:
        unmapped[cmsg] = (addr, size)

p(f"\n  Total with packData: {len(all_packdata)}")
p(f"  Already mapped: {len(all_packdata) - len(unmapped)}")
p(f"  Unmapped: {len(unmapped)}")

p(f"\n  ### Unmapped CMSGs with packData:")
for name in sorted(unmapped.keys()):
    addr, size = unmapped[name]
    p(f"    {name} @ 0x{addr:08X} ({size}B)")

# ═══════════════════════════════════════════════════════════════
# 4. Search for opcode dispatch/registration table
# ═══════════════════════════════════════════════════════════════
p(f"\n\n## Opcode Registration Patterns")

# The game must register handlers: registerListener<CMSG_XXX>(opcode, handler)
# Search for the pattern in .text where opcodes 0x0CE4-0x0CFB are used
# These are MOV w0, #0xCE4 etc. in ARM64

# Search in code sections for known opcodes as immediate values
TEXT_OFF = 0x5B4D0  # .text start
TEXT_SIZE = 0x24FFB30

interesting_ranges = [
    (0x0CE0, 0x0D00, "NEW-style encrypted"),
    (0x1B80, 0x1B90, "PASSWORD range"),
    (0x1930, 0x1940, "AUTO_HANDUP range"),
]

for range_start, range_end, desc in interesting_ranges:
    p(f"\n  ### Searching for opcodes 0x{range_start:04X}-0x{range_end:04X} ({desc})")
    for opcode in range(range_start, range_end):
        # ARM64 MOV Wd, #imm pattern - search for the opcode as u16 in instructions
        # movz wd, #imm encodes imm in bits [20:5]
        # We'll search for the byte pattern

        # Simpler: search for u16 LE bytes followed by common patterns
        target_le = struct.pack('<H', opcode)

        # Search in a region likely to contain handler registration
        # The registerListener calls are usually grouped together
        search_data = data[TEXT_OFF:TEXT_OFF + TEXT_SIZE]

        count = 0
        for m in re.finditer(re.escape(target_le), search_data):
            # Check if this is part of an ARM64 MOV instruction
            off = m.start()
            if off % 4 == 0:  # Instructions are 4-byte aligned
                insn_bytes = search_data[off:off+4]
                if len(insn_bytes) == 4:
                    word = struct.unpack('<I', insn_bytes)[0]
                    # Check if it's a MOV/MOVZ instruction with our value
                    # movz: 0101_0010_1xxx_xxxx_xxxx_xxxx_xxxx_xxxx
                    if (word >> 23) == 0xA5:  # movz w
                        imm16 = (word >> 5) & 0xFFFF
                        if imm16 == opcode:
                            count += 1
                            if count <= 3:
                                real_addr = TEXT_OFF + off
                                p(f"    0x{opcode:04X} found at 0x{real_addr:08X}")
        if count > 3:
            p(f"    ... ({count} total occurrences)")
        elif count == 0:
            # Try movz with lsl #16
            pass

# ═══════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════
with open(r'D:\CascadeProjects\analysis\findings\remaining_opcodes.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

print(f"Done! {len(new_cmsgs)} _NEW CMSGs, {len(unmapped)} unmapped")
print(f"Saved to findings/remaining_opcodes.md")

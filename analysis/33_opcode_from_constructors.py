#!/usr/bin/env python3
"""
33_opcode_from_constructors.py - Extract opcodes from ALL CMSG constructors
============================================================================
Each CMSG constructor does: mov w8, #OPCODE0000; str w8, [x0]
The opcode is in bits [31:16] of the immediate value.
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

# Find ALL CMSG constructors
constructors = []
pos = DYNSYM_OFF
while pos + 24 <= DYNSYM_OFF + DYNSYM_SIZE:
    st_name = struct.unpack('<I', data[pos:pos+4])[0]
    st_value = struct.unpack('<Q', data[pos+8:pos+16])[0]
    st_size = struct.unpack('<Q', data[pos+16:pos+24])[0]
    if st_name > 0 and st_name < 0x200000 and st_value > 0 and st_size > 0:
        name_end = data.index(b'\x00', DYNSTR_OFF + st_name)
        name = data[DYNSTR_OFF + st_name:name_end].decode('ascii', errors='replace')
        if 'C1Ev' in name and '8packData' not in name and '7getData' not in name:
            # Extract CMSG name
            m = re.search(r'(CMSG_[A-Z0-9_]+)C1Ev', name)
            if m:
                cmsg_name = m.group(1)
                constructors.append((cmsg_name, st_value, st_size))
    pos += 24

print(f"Found {len(constructors)} CMSG constructors")

# Disassemble each to find the MOV immediate that sets the opcode
opcode_map = {}
for cmsg_name, addr, size in constructors:
    if addr == 0 or addr > len(data) - 20:
        continue

    max_bytes = min(size, 100)
    code = data[addr:addr + max_bytes]
    insns = list(md.disasm(code, addr))

    for insn in insns[:15]:
        if insn.mnemonic == 'ret':
            break
        # Look for: mov wN, #IMMEDIATE
        if insn.mnemonic in ('mov', 'movz', 'orr') and '#' in insn.op_str:
            try:
                imm_str = insn.op_str.split('#')[-1].split(',')[0].strip()
                imm = int(imm_str, 0)
                # Opcode is in upper 16 bits if value >= 0x10000
                if imm >= 0x10000 and (imm & 0xFFFF) == 0:
                    opcode = (imm >> 16) & 0xFFFF
                    if 0x0001 <= opcode <= 0x2000:
                        opcode_map[cmsg_name] = opcode
                        break
            except:
                pass

        # Also handle: movz wN, #val, lsl #16
        if insn.mnemonic in ('movz',) and 'lsl #16' in insn.op_str:
            try:
                imm_str = insn.op_str.split('#')[1].split(',')[0].strip()
                opcode = int(imm_str, 0)
                if 0x0001 <= opcode <= 0x2000:
                    opcode_map[cmsg_name] = opcode
                    break
            except:
                pass

# Also check for str w8, [x0] with movz w8, #val, lsl #0x10
# Some may use: mov w8, #val; movk w8, #val, lsl #16
for cmsg_name, addr, size in constructors:
    if cmsg_name in opcode_map:
        continue
    if addr == 0 or addr > len(data) - 20:
        continue

    max_bytes = min(size, 100)
    code = data[addr:addr + max_bytes]
    insns = list(md.disasm(code, addr))

    # Try to find any constant being stored at [x0]
    last_mov_val = None
    for insn in insns[:15]:
        if insn.mnemonic == 'ret':
            break
        if insn.mnemonic in ('mov', 'movz') and insn.op_str.startswith('w') and '#' in insn.op_str:
            try:
                imm = int(insn.op_str.split('#')[-1].split(',')[0].strip(), 0)
                last_mov_val = imm
            except:
                pass
        if insn.mnemonic == 'str' and 'x0' in insn.op_str and last_mov_val is not None:
            if last_mov_val >= 0x10000 and (last_mov_val & 0xFFFF) == 0:
                opcode = (last_mov_val >> 16) & 0xFFFF
                if 0x0001 <= opcode <= 0x2000:
                    opcode_map[cmsg_name] = opcode
            break

print(f"Extracted {len(opcode_map)} opcodes\n")

# Print sorted by opcode
out = []
out.append("# CMSG → Opcode Map (from constructors)\n")

# Group by direction (REQUEST = client sends, RETURN = server sends)
client_ops = {}
server_ops = {}
other_ops = {}

for name, op in sorted(opcode_map.items(), key=lambda x: x[1]):
    if 'RETURN' in name or name.startswith('CMSG_SYNC_') or name.startswith('CMSG_SYN_'):
        server_ops[name] = op
    elif 'REQUEST' in name:
        client_ops[name] = op
    else:
        other_ops[name] = op

out.append(f"\n## Client->Server ({len(client_ops)} + {len(other_ops)} other):\n")
for name, op in sorted(client_ops.items(), key=lambda x: x[1]):
    out.append(f"  0x{op:04X} = {name}")

out.append(f"\n## Other (direction unclear) ({len(other_ops)}):\n")
for name, op in sorted(other_ops.items(), key=lambda x: x[1]):
    out.append(f"  0x{op:04X} = {name}")

out.append(f"\n## Server->Client ({len(server_ops)}):\n")
for name, op in sorted(server_ops.items(), key=lambda x: x[1]):
    out.append(f"  0x{op:04X} = {name}")

text = '\n'.join(out)

with open(r'D:\CascadeProjects\analysis\findings\cmsg_opcode_map.md', 'w', encoding='utf-8') as f:
    f.write(text)
print(f"\nSaved to findings/cmsg_opcode_map.md")

# Also output as Python dict for protocol.py
out2 = ["# Auto-generated CMSG opcode map\nCMSG_OPCODES = {"]
for name, op in sorted(opcode_map.items(), key=lambda x: x[1]):
    out2.append(f"    0x{op:04X}: '{name}',")
out2.append("}")
with open(r'D:\CascadeProjects\analysis\findings\cmsg_opcodes.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out2))
print(f"Saved Python dict to findings/cmsg_opcodes.py")

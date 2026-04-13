#!/usr/bin/env python3
"""
Resolve the key unknowns for 0x1B8B:
1. Are PLT 0x5C6DBA0 and 0x5C6DBB0 the same function? (.rela.plt symbol check)
2. What's the second distribution range in encodePassword? (rodata at 0x255B238)
3. What does encodePassword return for empty string? (disasm at 0x039FADD0)
4. What are the exact serialized fields from packData?
5. Resolve PLT 0x5C6DBD0 and 0x5C6DBE0 and 0x5C6DBC0
"""
import struct
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

LIBGAME = r"D:\CascadeProjects\libgame.so"
with open(LIBGAME, "rb") as f:
    data = f.read()

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

# ═══════════════════════════════════════════════════════════════
# 1. Resolve PLT symbols via .rela.plt
# ═══════════════════════════════════════════════════════════════
print("=" * 80)
print("1. RESOLVE PLT SYMBOLS via .rela.plt")
print("=" * 80)

# ELF headers
elf_shoff = struct.unpack('<Q', data[0x28:0x30])[0]
elf_shentsize = struct.unpack('<H', data[0x3A:0x3C])[0]
elf_shnum = struct.unpack('<H', data[0x3C:0x3E])[0]
elf_shstrndx = struct.unpack('<H', data[0x3E:0x40])[0]

shstr_off = struct.unpack('<Q', data[elf_shoff + elf_shstrndx * elf_shentsize + 0x18:
                                     elf_shoff + elf_shstrndx * elf_shentsize + 0x20])[0]

# Find sections
sections = {}
for i in range(elf_shnum):
    sh = elf_shoff + i * elf_shentsize
    sh_name_idx = struct.unpack('<I', data[sh:sh+4])[0]
    sh_type = struct.unpack('<I', data[sh+4:sh+8])[0]
    sh_offset = struct.unpack('<Q', data[sh+0x18:sh+0x20])[0]
    sh_size = struct.unpack('<Q', data[sh+0x20:sh+0x28])[0]
    name_end = data.index(b'\x00', shstr_off + sh_name_idx)
    name = data[shstr_off + sh_name_idx:name_end].decode('ascii', errors='replace')
    sections[name] = (sh_offset, sh_size)

# Resolve GOT addresses for target PLTs
plt_targets = {
    0x05C6DBA0: "CMsgCodec::Encode (known)",
    0x05C6DBB0: "UNKNOWN used by 0x1B8B packData",
    0x05C6DBC0: "PLT_unknown_2 (called before encoder)",
    0x05C6DBD0: "PLT_write_u16_helper",
    0x05C6DBE0: "PLT_write_u64_helper",
}

plt_got = {}
for plt_addr in plt_targets:
    code = data[plt_addr:plt_addr + 16]
    insns = list(md.disasm(code, plt_addr))
    if len(insns) >= 2 and insns[0].mnemonic == 'adrp' and insns[1].mnemonic == 'ldr':
        page = int(insns[0].op_str.split('#')[1], 0)
        off = int(insns[1].op_str.split('#')[1].rstrip(']'), 0)
        got = page + off
        plt_got[plt_addr] = got

# Read .rela.plt
dynstr_off = sections.get('.dynstr', (0x682A10, 0))[0] if '.dynstr' in sections else 0x682A10
dynsym_off = sections.get('.dynsym', (0x2F8, 0))[0] if '.dynsym' in sections else 0x2F8

if '.rela.plt' in sections:
    rela_off, rela_size = sections['.rela.plt']
    for plt_addr, desc in sorted(plt_targets.items()):
        got = plt_got.get(plt_addr)
        if not got:
            continue
        for j in range(rela_size // 24):
            entry = rela_off + j * 24
            r_offset = struct.unpack('<Q', data[entry:entry+8])[0]
            r_info = struct.unpack('<Q', data[entry+8:entry+16])[0]
            if r_offset == got:
                sym_idx = r_info >> 32
                sym_off = dynsym_off + sym_idx * 24
                st_name = struct.unpack('<I', data[sym_off:sym_off+4])[0]
                name_end = data.index(b'\x00', dynstr_off + st_name)
                sym_name = data[dynstr_off + st_name:name_end].decode('ascii', errors='replace')
                print(f"  PLT 0x{plt_addr:08X} ({desc})")
                print(f"    GOT: 0x{got:08X} -> Symbol #{sym_idx}: {sym_name}")
                break

# ═══════════════════════════════════════════════════════════════
# 2. Rodata for second distribution range (0x255B238)
# ═══════════════════════════════════════════════════════════════
print(f"\n{'='*80}")
print("2. RODATA at 0x0255B238 (second distribution params)")
print("=" * 80)

rodata_addr = 0x0255B238
raw8 = data[rodata_addr:rodata_addr+8]
as_u64 = struct.unpack('<Q', raw8)[0]
as_i64 = struct.unpack('<q', raw8)[0]
as_double = struct.unpack('<d', raw8)[0]
as_2u32 = struct.unpack('<II', raw8)
as_2i32 = struct.unpack('<ii', raw8)
print(f"  Bytes: {raw8.hex()}")
print(f"  As u64: {as_u64} (0x{as_u64:016X})")
print(f"  As i64: {as_i64}")
print(f"  As double: {as_double}")
print(f"  As 2×u32: {as_2u32[0]}, {as_2u32[1]} (0x{as_2u32[0]:08X}, 0x{as_2u32[1]:08X})")
print(f"  As 2×i32: {as_2i32[0]}, {as_2i32[1]}")

# The distribution is uniform_int_distribution which takes (min, max) as int32
# The params were stored via `stp w8, w9, [sp]` initially as {1, 999999}
# Then overwritten by `str d0, [sp]` from rodata
# So the two i32 values ARE the min and max of the second distribution
print(f"\n  => Second distribution: uniform_int({as_2i32[0]}, {as_2i32[1]})")

# ═══════════════════════════════════════════════════════════════
# 3. What happens for empty password string? (0x039FADD0)
# ═══════════════════════════════════════════════════════════════
print(f"\n{'='*80}")
print("3. EMPTY PASSWORD PATH (0x039FADD0)")
print("=" * 80)

code = data[0x039FADD0:0x039FADD0 + 100]
insns = list(md.disasm(code, 0x039FADD0))
for insn in insns[:15]:
    print(f"  0x{insn.address:08X}: {insn.mnemonic:10s} {insn.op_str}")
    if insn.mnemonic == 'ret':
        break

# ═══════════════════════════════════════════════════════════════
# 4. packData field reads - trace exactly what gets serialized
# ═══════════════════════════════════════════════════════════════
print(f"\n{'='*80}")
print("4. packData FIELD READS from CMSG object (x19)")
print("=" * 80)

pack_code = data[0x05273690:0x05273690 + 0x300]
pack_insns = list(md.disasm(pack_code, 0x05273690))

for insn in pack_insns:
    # Find reads from x19 (the CMSG object)
    if 'x19' in insn.op_str and insn.mnemonic.startswith('ldr'):
        offset = "?"
        if '#' in insn.op_str:
            try:
                offset = insn.op_str.split('#')[1].rstrip(']')
            except:
                pass
        size = "u8" if insn.mnemonic == "ldrb" else "u16" if insn.mnemonic == "ldrh" else "u32/u64"
        if insn.mnemonic == "ldr" and insn.op_str.startswith("x"):
            size = "u64"
        elif insn.mnemonic == "ldr" and insn.op_str.startswith("w"):
            size = "u32"
        print(f"  0x{insn.address:08X}: {insn.mnemonic} {insn.op_str}  => READ {size} from obj+{offset}")
    
    if insn.mnemonic == 'ret' and insn.address > 0x05273700:
        break

# ═══════════════════════════════════════════════════════════════
# 5. Verify MAGIC constant in encodePassword
# ═══════════════════════════════════════════════════════════════
print(f"\n{'='*80}")
print("5. VERIFY encodePassword MAGIC constant")
print("=" * 80)

# mov x9, #0x1000
# movk x9, #0xd4a5, lsl #16
# movk x9, #0xe8, lsl #32
val = 0x1000 | (0xd4a5 << 16) | (0xe8 << 32)
print(f"  MAGIC = 0x{val:016X} = {val}")
print(f"  Is it 1 trillion? {val == 1_000_000_000_000}")

# ═══════════════════════════════════════════════════════════════
# 6. Check the S2C 0x1B8A payload from PCAPs to see gate byte
# ═══════════════════════════════════════════════════════════════
print(f"\n{'='*80}")
print("6. S2C 0x1B8A PAYLOADS from PCAPs (checking gate byte)")
print("=" * 80)

from pathlib import Path

def read_pcap_streams(filepath):
    with open(filepath, 'rb') as f:
        magic = struct.unpack('<I', f.read(4))[0]
        endian = '<' if magic == 0xa1b2c3d4 else '>'
        f.read(20)
        streams = {}
        while True:
            hdr = f.read(16)
            if len(hdr) < 16: break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
            pdata = f.read(incl_len)
            if len(pdata) < incl_len: break
            if len(pdata) < 20: continue
            ihl = (pdata[0] & 0x0F) * 4
            if pdata[9] != 6: continue
            tcp = pdata[ihl:]
            if len(tcp) < 20: continue
            sp = struct.unpack('>H', tcp[0:2])[0]
            dp = struct.unpack('>H', tcp[2:4])[0]
            toff = ((tcp[12] >> 4) & 0xF) * 4
            pl = tcp[toff:]
            if not pl: continue
            gp = set(range(5990, 5999)) | set(range(7001, 7011))
            if dp in gp:
                streams.setdefault('C2S', bytearray()).extend(pl)
            elif sp in gp:
                streams.setdefault('S2C', bytearray()).extend(pl)
    return streams

def parse_packets(raw):
    packets = []
    pos = 0
    while pos + 4 <= len(raw):
        pkt_len = struct.unpack('<H', raw[pos:pos+2])[0]
        opcode = struct.unpack('<H', raw[pos+2:pos+4])[0]
        if pkt_len < 4 or pkt_len > 65535 or pos + pkt_len > len(raw): break
        packets.append((opcode, bytes(raw[pos+4:pos+pkt_len])))
        pos += pkt_len
    return packets

pcap_dir = Path(r'D:\CascadeProjects')
pcaps = sorted(pcap_dir.glob('*.pcap'))[:20]

count_1b8a = 0
count_1b8b_c2s = 0
count_1b8b_s2c = 0
for pcap in pcaps:
    try:
        s = read_pcap_streams(pcap)
        if 'S2C' not in s: continue
        s2c = parse_packets(s['S2C'])
        c2s = parse_packets(s.get('C2S', bytearray()))
        
        for op, pl in s2c:
            if op == 0x1B8A:
                count_1b8a += 1
                if count_1b8a <= 5:
                    print(f"  {pcap.name}: S2C 0x1B8A ({len(pl)}B): {pl.hex()}")
                    if len(pl) >= 5:
                        print(f"    byte[0]=0x{pl[0]:02X} byte[4]=0x{pl[4]:02X} (gate byte candidate)")
            if op == 0x1B8B:
                count_1b8b_s2c += 1
        
        for op, pl in c2s:
            if op == 0x1B8B:
                count_1b8b_c2s += 1
    except:
        continue

print(f"\n  Totals: S2C 0x1B8A={count_1b8a}, S2C 0x1B8B={count_1b8b_s2c}, C2S 0x1B8B={count_1b8b_c2s}")

print("\nDONE")

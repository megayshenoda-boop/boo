"""Deep analysis of CMSG_START_MARCH_EX and CMSG_HERO_SOLDIER_RECRUIT_REQUEST packData"""
import struct

BINARY = r"d:\CascadeProjects\libgame.so"
data = open(BINARY, "rb").read()

# ELF loading - need to translate virtual addresses to file offsets
# Parse program headers to find LOAD segments
e_phoff = struct.unpack('<Q', data[32:40])[0]
e_phentsize = struct.unpack('<H', data[54:56])[0]
e_phnum = struct.unpack('<H', data[56:58])[0]

load_segments = []
for i in range(e_phnum):
    off = e_phoff + i * e_phentsize
    p_type = struct.unpack('<I', data[off:off+4])[0]
    if p_type == 1:  # PT_LOAD
        p_offset = struct.unpack('<Q', data[off+8:off+16])[0]
        p_vaddr = struct.unpack('<Q', data[off+16:off+24])[0]
        p_filesz = struct.unpack('<Q', data[off+32:off+40])[0]
        p_memsz = struct.unpack('<Q', data[off+40:off+48])[0]
        load_segments.append((p_vaddr, p_offset, p_filesz))
        print(f"LOAD: vaddr=0x{p_vaddr:X} -> file_off=0x{p_offset:X}, size=0x{p_filesz:X}")

def vaddr_to_fileoff(vaddr):
    for v, f, s in load_segments:
        if v <= vaddr < v + s:
            return f + (vaddr - v)
    return vaddr  # fallback

# ARM64 instruction decoder helpers
def decode_adr(insn, pc):
    """Decode ADR/ADRP instruction"""
    op = (insn >> 31) & 1  # 0=ADR, 1=ADRP
    immlo = (insn >> 29) & 3
    immhi = (insn >> 5) & 0x7FFFF
    rd = insn & 0x1F
    imm = (immhi << 2) | immlo
    if imm & (1 << 20): imm -= (1 << 21)  # sign extend
    if op: # ADRP
        return rd, (pc & ~0xFFF) + (imm << 12)
    return rd, pc + imm

def decode_add_imm(insn):
    """Decode ADD Xd, Xn, #imm"""
    rd = insn & 0x1F
    rn = (insn >> 5) & 0x1F
    imm12 = (insn >> 10) & 0xFFF
    shift = (insn >> 22) & 3
    if shift == 1: imm12 <<= 12
    return rd, rn, imm12

def decode_ldr_imm(insn):
    """Decode LDR with immediate offset"""
    rt = insn & 0x1F
    rn = (insn >> 5) & 0x1F
    if (insn >> 24) & 0xFF in (0xF9, 0xB9, 0x79, 0x39):
        # Unsigned offset
        imm12 = (insn >> 10) & 0xFFF
        size = (insn >> 30) & 3
        offset = imm12 << size
        return rt, rn, offset
    return None

def decode_str_imm(insn):
    """Decode STR/STRB/STRH with immediate offset"""
    rt = insn & 0x1F
    rn = (insn >> 5) & 0x1F
    imm12 = (insn >> 10) & 0xFFF
    size = (insn >> 30) & 3
    offset = imm12 << size
    return rt, rn, offset

def analyze_packdata(name, vaddr, size):
    """Analyze a packData function by looking at its instruction pattern"""
    file_off = vaddr_to_fileoff(vaddr)
    print(f"\n{'='*80}")
    print(f"  {name}::packData")
    print(f"  VAddr: 0x{vaddr:08X}, FileOff: 0x{file_off:08X}, Size: {size} bytes")
    print(f"{'='*80}")
    
    num_insns = size // 4
    
    # Track writes to the stream buffer
    # The pattern is: BL to write_u8/write_u16/write_u32/write_u64
    # Before each BL, there's usually a LDR from the struct (this+offset)
    
    writes = []
    struct_accesses = []
    bl_targets = set()
    
    for i in range(num_insns):
        addr = vaddr + i * 4
        foff = vaddr_to_fileoff(addr)
        insn = struct.unpack('<I', data[foff:foff+4])[0]
        
        # BL instruction: bits[31:26] = 100101
        if (insn >> 26) == 0x25:
            offset = insn & 0x3FFFFFF
            if offset & (1 << 25): offset -= (1 << 26)
            target = addr + offset * 4
            bl_targets.add(target)
            
        # LDR from [x19, #offset] - x19 is usually 'this'
        if (insn >> 24) & 0xFF in (0xF9, 0xB9, 0x79, 0x39):
            result = decode_ldr_imm(insn)
            if result:
                rt, rn, offset = result
                if rn == 19:  # x19 = this
                    size_bits = (insn >> 30) & 3
                    sz = 1 << size_bits
                    struct_accesses.append((i, addr, rt, offset, sz))
        
        # LDP from [x19, #offset]
        if (insn >> 22) & 0x3FF in (0x2E9, 0x2C5):  # LDP x,x,[Xn,#imm]
            rt = insn & 0x1F
            rt2 = (insn >> 10) & 0x1F
            rn = (insn >> 5) & 0x1F
            imm7 = (insn >> 15) & 0x7F
            if imm7 & 0x40: imm7 -= 0x80
            if rn == 19:
                opc = (insn >> 30) & 3
                scale = 4 if opc == 0 else 8
                off = imm7 * scale
                struct_accesses.append((i, addr, rt, off, 8))
                struct_accesses.append((i, addr, rt2, off+8, 8))
    
    # Print struct accesses (fields read from 'this')
    print(f"\n  Struct fields accessed (from this/x19):")
    seen_offsets = set()
    for idx, addr, rt, offset, sz in sorted(struct_accesses, key=lambda x: x[3]):
        if offset not in seen_offsets:
            seen_offsets.add(offset)
            print(f"    this+0x{offset:02X} ({sz}B) -> x{rt}  [at 0x{addr:08X}]")
    
    # Print BL targets (function calls)
    print(f"\n  BL targets (called functions): {len(bl_targets)}")
    for t in sorted(bl_targets):
        print(f"    -> 0x{t:08X}")
    
    # Now let's do a more detailed trace
    print(f"\n  Instruction trace (first {min(num_insns, 150)} insns):")
    for i in range(min(num_insns, 150)):
        addr = vaddr + i * 4
        foff = vaddr_to_fileoff(addr)
        insn = struct.unpack('<I', data[foff:foff+4])[0]
        
        desc = ""
        # Decode common instructions
        if (insn >> 26) == 0x25:  # BL
            offset = insn & 0x3FFFFFF
            if offset & (1 << 25): offset -= (1 << 26)
            target = addr + offset * 4
            desc = f"BL 0x{target:08X}"
        elif (insn >> 24) & 0xFF == 0xF9:  # LDR X
            result = decode_ldr_imm(insn)
            if result:
                rt, rn, off = result
                desc = f"LDR x{rt}, [x{rn}, #0x{off:X}]"
        elif (insn >> 24) & 0xFF == 0xB9:  # LDR W
            result = decode_ldr_imm(insn)
            if result:
                rt, rn, off = result
                desc = f"LDR w{rt}, [x{rn}, #0x{off:X}]"
        elif (insn >> 24) & 0xFF == 0x39:  # LDRB
            result = decode_ldr_imm(insn)
            if result:
                rt, rn, off = result
                desc = f"LDRB w{rt}, [x{rn}, #0x{off:X}]"
        elif (insn >> 24) & 0xFF == 0x79:  # LDRH
            result = decode_ldr_imm(insn)
            if result:
                rt, rn, off = result
                desc = f"LDRH w{rt}, [x{rn}, #0x{off:X}]"
        elif (insn & 0xFFE00C00) == 0xA9400000:  # LDP
            rt = insn & 0x1F
            rt2 = (insn >> 10) & 0x1F
            rn = (insn >> 5) & 0x1F
            imm7 = (insn >> 15) & 0x7F
            if imm7 & 0x40: imm7 -= 0x80
            desc = f"LDP x{rt}, x{rt2}, [x{rn}, #{imm7*8}]"
        elif insn == 0xD65F03C0:
            desc = "RET"
        elif (insn >> 24) & 0xFF == 0xAA:  # MOV (ORR)
            rd = insn & 0x1F
            rm = (insn >> 16) & 0x1F
            desc = f"MOV x{rd}, x{rm}"
        elif (insn >> 23) & 0x1FF == 0x122:  # ADD imm 64-bit
            rd, rn, imm = decode_add_imm(insn)
            desc = f"ADD x{rd}, x{rn}, #0x{imm:X}"
        elif (insn >> 23) & 0x1FF == 0x022:  # ADD imm 32-bit
            rd, rn, imm = decode_add_imm(insn)
            desc = f"ADD w{rd}, w{rn}, #0x{imm:X}"
        elif (insn >> 24) & 0x7F == 0x34:  # CBZ
            rt = insn & 0x1F
            imm19 = (insn >> 5) & 0x7FFFF
            if imm19 & (1<<18): imm19 -= (1<<19)
            target = addr + imm19 * 4
            desc = f"CBZ x{rt}, 0x{target:08X}"
        elif (insn >> 24) & 0x7F == 0x35:  # CBNZ
            rt = insn & 0x1F
            imm19 = (insn >> 5) & 0x7FFFF
            if imm19 & (1<<18): imm19 -= (1<<19)
            target = addr + imm19 * 4
            desc = f"CBNZ x{rt}, 0x{target:08X}"
        elif (insn >> 24) & 0xFF == 0x52:  # MOVZ W
            rd = insn & 0x1F
            imm16 = (insn >> 5) & 0xFFFF
            hw = (insn >> 21) & 3
            desc = f"MOVZ w{rd}, #0x{imm16 << (hw*16):X}"
        elif (insn >> 24) & 0xFF == 0xD2:  # MOVZ X
            rd = insn & 0x1F
            imm16 = (insn >> 5) & 0xFFFF
            hw = (insn >> 21) & 3
            desc = f"MOVZ x{rd}, #0x{imm16 << (hw*16):X}"
        
        if desc:
            print(f"    0x{addr:08X}: {insn:08X}  {desc}")

# Analyze all three
funcs = [
    ("CMSG_START_MARCH_EX", 0x05212ADC, 488),
    ("CMSG_HERO_SOLDIER_RECRUIT_REQUEST", 0x050AF814, 428),
]

for name, addr, sz in funcs:
    analyze_packdata(name, addr, sz)

print("\n\nDone.")

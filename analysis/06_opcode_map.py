"""
Phase 6: Map opcodes to CMSG names.
Find the dispatch table that maps opcode numbers to CMSG handler functions.
Also, search for opcode constants referenced near CMSG struct names.
"""
import re, struct, sys
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection

SO_PATH = r"D:\CascadeProjects\libgame.so"

def main():
    with open(SO_PATH, 'rb') as f:
        raw = f.read()

    # Known opcodes from reverse engineering
    known = {
        0x000B: 'GATEWAY_AUTH', 0x000C: 'GATEWAY_REDIRECT',
        0x001F: 'GAME_LOGIN', 0x0020: 'LOGIN_RETURN',
        0x0021: 'ENTER_GAME', 0x0022: 'ENTER_GAME_RETURN',
        0x0033: 'SYN_ATTRIBUTE', 0x0037: 'TIMESTAMP', 0x0038: 'INIT_DATA',
        0x0042: 'HEARTBEAT', 0x0043: 'HEARTBEAT2',
        0x006E: 'SET_VIEW', 0x0071: 'MARCH_STATE',
        0x00AA: 'HERO_INFO', 0x00B8: 'MARCH_ACK', 0x00B9: 'MARCH_ACK2',
        0x02F2: 'SESSION_ERROR',
        0x0323: 'HERO_SELECT', 0x033E: 'SEARCH_TILE', 0x033F: 'SEARCH_RESULT',
        0x06C2: 'SOLDIER_INFO',
        0x0709: 'UNK_0709', 0x0834: 'FORMATION_SET', 0x0840: 'UNK_0840',
        0x099D: 'TROOP_QUERY', 0x0A2C: 'UNK_0A2C', 0x0AF2: 'UNK_0AF2',
        0x0CE7: 'CANCEL_MARCH', 0x0CE8: 'START_MARCH',
        0x0CEB: 'ENABLE_VIEW', 0x0CED: 'TRAIN', 0x0CEE: 'RESEARCH', 0x0CEF: 'BUILD',
        0x1357: 'UNK_1357', 0x170D: 'UNK_170D', 0x17D4: 'UNK_17D4',
        0x1B8B: 'SESSION_PKT', 0x1C87: 'UNK_1C87',
    }

    # ═══ 1. Find CMSG struct names near opcode values ═══
    # Strategy: find opcode as u32 LE in .rodata, then look for nearby CMSG string refs
    print("=" * 80)
    print("1. OPCODE CONSTANTS IN .rodata (as u32 LE)")
    print("=" * 80)

    with open(SO_PATH, 'rb') as f:
        elf = ELFFile(f)
        for s in elf.iter_sections():
            if s.name == '.rodata':
                rodata_off = s['sh_offset']
                rodata_size = s['sh_size']
                rodata_addr = s['sh_addr']

    rodata = raw[rodata_off:rodata_off + rodata_size]

    for opcode in sorted(known.keys()):
        if opcode < 0x0040:
            continue  # skip very common values
        needle = struct.pack('<I', opcode)
        pos = 0
        finds = []
        while len(finds) < 3:
            idx = rodata.find(needle, pos)
            if idx < 0: break
            # Check surrounding bytes for patterns (e.g., tables of opcode entries)
            ctx_start = max(0, idx - 16)
            ctx_end = min(len(rodata), idx + 20)
            ctx = rodata[ctx_start:ctx_end]
            finds.append((rodata_off + idx, ctx))
            pos = idx + 1
        if finds:
            print(f"\n  0x{opcode:04X} ({known[opcode]}):")
            for abs_off, ctx in finds:
                print(f"    0x{abs_off:08X}: {ctx.hex()}")

    # ═══ 2. Find CMSG struct references with opcode field ═══
    # In C++, CMSG structs likely have an opcode as first field
    # Look for patterns where opcode is followed by string pointer
    print("\n" + "=" * 80)
    print("2. CMSG NAMES -> find which opcode each uses")
    print("=" * 80)

    # Strategy: find CMSG_*_REQUEST/_RETURN strings in binary,
    # then look for code that references both the string AND an opcode constant

    # First, find all unique clean CMSG names from binary
    cmsg_pattern = re.compile(rb'CMSG_[A-Z_]+(?:_REQUEST|_RETURN|_SEND|_RECV|_INFO)')
    cmsg_offsets = {}
    for m in cmsg_pattern.finditer(raw):
        name = m.group().decode()
        # Strip mangling
        clean = name
        for suffix in ['C1E', 'C2E', 'D2E', 'EE', 'EEE']:
            if clean.endswith(suffix):
                clean = clean[:-len(suffix)]
        if clean not in cmsg_offsets:
            cmsg_offsets[clean] = m.start()

    # For march/battle related ones, try to find opcode references nearby
    march_related = {k: v for k, v in cmsg_offsets.items() if any(
        w in k.lower() for w in ['march', 'battle', 'attack', 'gather', 'scout',
                                   'rally', 'troop', 'soldier', 'hero_select',
                                   'formation', 'army', 'siege', 'reinforce',
                                   'building_operat', 'train_soldier',
                                   'cancel_march', 'start_march', 'enable_view'])}

    print(f"\nMarch/Battle related CMSG names ({len(march_related)}):")
    for name in sorted(march_related.keys()):
        off = march_related[name]
        print(f"  {name} at 0x{off:08X}")

    # ═══ 3. Find pairs of opcode + handler in register tables ═══
    print("\n" + "=" * 80)
    print("3. OPCODE DISPATCH - looking for register patterns")
    print("=" * 80)

    # In ARM64, opcode dispatch often uses:
    # MOV Wn, #opcode  ;  then BL to handler
    # Or table of [opcode, handler_ptr] pairs
    # Let's look for MOV instructions with known opcodes

    # The text section
    with open(SO_PATH, 'rb') as f:
        elf2 = ELFFile(f)
        for s in elf2.iter_sections():
            if s.name == '.text':
                text_off = s['sh_offset']
                text_size = s['sh_size']
                text_addr = s['sh_addr']

    md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
    md.detail = True

    # For key opcodes, find MOV Wn, #opcode instructions
    target_opcodes = [0x0CE8, 0x0CED, 0x0CEE, 0x0CEF, 0x0CEB, 0x1B8B, 0x0CE7]

    for target in target_opcodes:
        # ARM64: MOV Wn, #imm16 is encoded as MOVZ Wd, #imm16
        # MOVZ W0..W30, #target
        # Encoding: 0x52800000 | (imm16 << 5) | Rd
        # But we can search for the immediate in the instruction

        # Search for immediate in 4-byte aligned positions
        imm_bytes = struct.pack('<H', target)
        locations = []
        pos = text_off
        while len(locations) < 5:
            idx = raw.find(imm_bytes, pos, text_off + text_size)
            if idx < 0: break
            # Check if this is part of a MOV/MOVZ instruction
            # ARM64 instructions are 4-byte aligned
            aligned = idx & ~3
            insn_bytes = raw[aligned:aligned+4]
            if len(insn_bytes) == 4:
                word = struct.unpack('<I', insn_bytes)[0]
                # MOVZ Wd, #imm: 0101001000 + imm16(5:20) + Rd(0:4)
                # Check if it's a MOV-like instruction
                if (word >> 23) & 0x1FF in [0x0A5, 0x1A5]:  # MOVZ W/X
                    imm = (word >> 5) & 0xFFFF
                    rd = word & 0x1F
                    if imm == target:
                        va = aligned - text_off + text_addr
                        locations.append((va, rd))

            pos = idx + 1

        if locations:
            print(f"\n  0x{target:04X} ({known.get(target, '???')}):")
            for va, rd in locations:
                print(f"    MOV W{rd}, #0x{target:04X} at 0x{va:X}")
                # Disassemble context (16 instructions around it)
                file_off = va - text_addr + text_off
                ctx_start = max(text_off, file_off - 32)
                ctx_code = raw[ctx_start:ctx_start + 96]
                ctx_va = ctx_start - text_off + text_addr
                for insn in md.disasm(ctx_code, ctx_va):
                    marker = " <<<<" if insn.address == va else ""
                    print(f"      0x{insn.address:X}: {insn.mnemonic}\t{insn.op_str}{marker}")
        else:
            print(f"\n  0x{target:04X} ({known.get(target, '???')}): no MOVZ found")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
15_find_real_handlers.py - Find REAL game opcode handlers
=========================================================
Previous MOVZ scan (script 09) found FALSE POSITIVES - the 0x1B8B and 0x0CE8
references were in OpenSSL/libcurl code statically linked into libgame.so.

This script uses a better approach:
1. Find cross-references to CMSG_TABLE (0x028B723A) to locate encode/decode functions
2. Find cross-references to sendMsg to locate packet sending code
3. Search for opcode constants being written to packet buffers (STRH pattern)
4. Look for registerListener instantiations to find handler registration
"""

import struct, sys, os
from collections import defaultdict

try:
    from capstone import *
except ImportError:
    os.system("pip install capstone")
    from capstone import *

LIBGAME = r"D:\CascadeProjects\libgame.so"
FINDINGS_DIR = r"D:\CascadeProjects\analysis\findings"
os.makedirs(FINDINGS_DIR, exist_ok=True)

# Known addresses
CMSG_TABLE_ADDR = 0x028B723A  # 7-byte XOR table in .rodata
CMSG_TABLE_PAGE = CMSG_TABLE_ADDR & ~0xFFF  # 0x028B7000 for ADRP

# Key opcodes we want to find
TARGET_OPCODES = {
    0x1B8B: "SESSION_PKT",
    0x0CE8: "START_MARCH",
    0x0CE7: "CANCEL_MARCH",
    0x0CEF: "BUILD",
    0x0CED: "TRAIN",
    0x0CEE: "RESEARCH",
    0x0CEB: "ENABLE_VIEW",
    0x0038: "INIT_DATA",
    0x0042: "HEARTBEAT",
    0x0834: "FORMATION_SET",
    0x0D08: "ALT_MARCH",
}

def read_binary():
    with open(LIBGAME, "rb") as f:
        return f.read()

def find_text_section(data):
    """Find .text section boundaries from ELF headers"""
    # Parse ELF header
    e_shoff = struct.unpack_from("<Q", data, 0x28)[0]
    e_shentsize = struct.unpack_from("<H", data, 0x3A)[0]
    e_shnum = struct.unpack_from("<H", data, 0x3C)[0]
    e_shstrndx = struct.unpack_from("<H", data, 0x3E)[0]

    # Get string table
    str_sh_offset = e_shoff + e_shstrndx * e_shentsize
    str_sh_off = struct.unpack_from("<Q", data, str_sh_offset + 0x18)[0]

    for i in range(e_shnum):
        sh_offset = e_shoff + i * e_shentsize
        sh_name_idx = struct.unpack_from("<I", data, sh_offset)[0]
        sh_type = struct.unpack_from("<I", data, sh_offset + 4)[0]
        sh_addr = struct.unpack_from("<Q", data, sh_offset + 0x10)[0]
        sh_off = struct.unpack_from("<Q", data, sh_offset + 0x18)[0]
        sh_size = struct.unpack_from("<Q", data, sh_offset + 0x20)[0]

        name_end = data.index(b'\x00', str_sh_off + sh_name_idx)
        name = data[str_sh_off + sh_name_idx:name_end].decode('ascii', errors='replace')

        if name == '.text':
            return sh_addr, sh_off, sh_size
        if name == '.rodata':
            global RODATA_ADDR, RODATA_OFF, RODATA_SIZE
            RODATA_ADDR = sh_addr
            RODATA_OFF = sh_off
            RODATA_SIZE = sh_size

    return None, None, None

RODATA_ADDR = 0
RODATA_OFF = 0
RODATA_SIZE = 0

def approach1_find_table_xrefs(data, text_addr, text_off, text_size):
    """Find functions that reference CMSG_TABLE via ADRP+ADD"""
    print("\n=== APPROACH 1: Cross-references to CMSG_TABLE ===")

    table_page = CMSG_TABLE_ADDR >> 12  # Page number
    table_offset = CMSG_TABLE_ADDR & 0xFFF  # Offset within page = 0x23A

    md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
    md.detail = True

    text_data = data[text_off:text_off + text_size]
    xrefs = []

    # Scan for ADRP instructions that target the CMSG_TABLE page
    # ADRP format: sets register to (PC & ~0xFFF) + (imm << 12)
    CHUNK = 4 * 1024 * 1024  # Process 4MB at a time

    for chunk_start in range(0, text_size, CHUNK):
        chunk_end = min(chunk_start + CHUNK, text_size)
        chunk_data = text_data[chunk_start:chunk_end]
        chunk_addr = text_addr + chunk_start

        # Quick scan for potential ADRP instructions (look for the right immediate)
        for offset in range(0, len(chunk_data) - 8, 4):
            insn_bytes = struct.unpack_from("<I", chunk_data, offset)[0]

            # Check if it's an ADRP instruction (bits [28:24] = 10000, bit 31 = 1)
            if (insn_bytes & 0x9F000000) != 0x90000000:
                continue

            # Extract ADRP immediate
            immhi = (insn_bytes >> 5) & 0x7FFFF  # bits [23:5]
            immlo = (insn_bytes >> 29) & 0x3       # bits [30:29]
            imm = (immhi << 2) | immlo
            if imm & 0x100000:  # sign extend 21-bit
                imm |= ~0x1FFFFF
                imm &= 0xFFFFFFFFFFFFFFFF

            pc_page = (chunk_addr + offset) & ~0xFFF
            target_page = (pc_page + (imm << 12)) & 0xFFFFFFFFFFFFFFFF

            if target_page == (CMSG_TABLE_ADDR & ~0xFFF):
                rd = insn_bytes & 0x1F  # destination register

                # Check next instruction for ADD with offset 0x23A
                if offset + 4 < len(chunk_data):
                    next_insn = struct.unpack_from("<I", chunk_data, offset + 4)[0]
                    # ADD Xd, Xn, #imm12 format: 1001000100_imm12_Rn_Rd
                    if (next_insn & 0xFFC00000) == 0x91000000:
                        add_imm = (next_insn >> 10) & 0xFFF
                        add_rn = (next_insn >> 5) & 0x1F
                        add_rd = next_insn & 0x1F

                        if add_rn == rd and add_imm >= 0x230 and add_imm <= 0x250:
                            addr = chunk_addr + offset
                            xrefs.append((addr, rd, add_rd, add_imm))
                            print(f"  XREF at 0x{addr:08X}: ADRP X{rd}, page -> ADD X{add_rd}, X{rd}, #0x{add_imm:X}")

    return xrefs

def approach2_find_strh_opcodes(data, text_addr, text_off, text_size):
    """Find where game opcodes are written to memory as u16 (STRH instruction)
    Game packets have opcode at offset 2, so look for MOVZ + STRH patterns"""
    print("\n=== APPROACH 2: Find opcode STRH (store halfword) patterns ===")

    md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
    md.detail = True

    text_data = data[text_off:text_off + text_size]
    results = defaultdict(list)

    # For each target opcode, find MOVZ+STRH within a few instructions
    CHUNK = 4 * 1024 * 1024

    for chunk_start in range(0, text_size, CHUNK):
        chunk_end = min(chunk_start + CHUNK, text_size)
        chunk_data = text_data[chunk_start:chunk_end]
        chunk_addr = text_addr + chunk_start

        for offset in range(0, len(chunk_data) - 4, 4):
            insn_bytes = struct.unpack_from("<I", chunk_data, offset)[0]

            # MOVZ Wd, #imm16: 0101_0010_100_imm16_Rd (for shift=0)
            if (insn_bytes & 0xFFE00000) != 0x52800000:
                continue

            imm16 = (insn_bytes >> 5) & 0xFFFF
            rd = insn_bytes & 0x1F

            if imm16 not in TARGET_OPCODES:
                continue

            addr = chunk_addr + offset

            # Look at surrounding instructions for STRH (store halfword)
            # Check next 20 instructions
            found_strh = False
            found_str_context = []

            for look in range(1, 20):
                look_off = offset + look * 4
                if look_off + 4 > len(chunk_data):
                    break
                look_insn = struct.unpack_from("<I", chunk_data, look_off)[0]

                # STRH Wt, [Xn, #imm]: 0111_1001_00_imm12_Rn_Rt
                if (look_insn & 0xFFC00000) == 0x79000000:
                    strh_rt = look_insn & 0x1F
                    strh_rn = (look_insn >> 5) & 0x1F
                    strh_imm = ((look_insn >> 10) & 0xFFF) * 2  # scaled by 2 for halfword
                    found_str_context.append(f"STRH W{strh_rt}, [X{strh_rn}, #0x{strh_imm:X}] at +{look*4}")
                    if strh_rt == rd:
                        found_strh = True

                # STR Wt (word store) - opcode might be part of a larger write
                if (look_insn & 0xFFC00000) == 0xB9000000:
                    str_rt = look_insn & 0x1F
                    str_rn = (look_insn >> 5) & 0x1F
                    str_imm = ((look_insn >> 10) & 0xFFF) * 4
                    found_str_context.append(f"STR W{str_rt}, [X{str_rn}, #0x{str_imm:X}] at +{look*4}")

            # Also check what strings are referenced nearby
            nearby_strings = []
            for look in range(-10, 30):
                look_off = offset + look * 4
                if look_off < 0 or look_off + 4 > len(chunk_data):
                    continue
                look_insn = struct.unpack_from("<I", chunk_data, look_off)[0]

                # Check for ADRP
                if (look_insn & 0x9F000000) == 0x90000000:
                    immhi = (look_insn >> 5) & 0x7FFFF
                    immlo = (look_insn >> 29) & 0x3
                    imm = (immhi << 2) | immlo
                    if imm & 0x100000:
                        imm |= ~0x1FFFFF
                        imm &= 0xFFFFFFFFFFFFFFFF
                    pc_page = (chunk_addr + look_off) & ~0xFFF
                    target_page = (pc_page + (imm << 12)) & 0xFFFFFFFFFFFFFFFF

                    # Check for ADD after ADRP to get full string address
                    if look_off + 4 < len(chunk_data):
                        next_insn = struct.unpack_from("<I", chunk_data, look_off + 4)[0]
                        if (next_insn & 0xFFC00000) == 0x91000000:
                            add_imm = (next_insn >> 10) & 0xFFF
                            full_addr = target_page + add_imm
                            # Try to read string at this address from rodata
                            if RODATA_ADDR <= full_addr < RODATA_ADDR + RODATA_SIZE:
                                str_off = RODATA_OFF + (full_addr - RODATA_ADDR)
                                try:
                                    end = data.index(b'\x00', str_off, str_off + 100)
                                    s = data[str_off:end].decode('ascii', errors='replace')
                                    if len(s) > 2 and s.isprintable():
                                        nearby_strings.append(s)
                                except:
                                    pass

            # Filter: skip if strings indicate SSL/HTTP code
            ssl_indicators = ['ssl', 'SSL', 'NTLM', 'Digest', 'Basic', 'Bearer',
                            'Content-Type', 'Host:', 'HTTP', 'Certificate',
                            'cipher', 'handshake', 'tls', 'TLS']
            is_ssl = any(any(ind in s for ind in ssl_indicators) for s in nearby_strings)

            # Game indicators
            game_indicators = ['CMSG', 'cmsg', 'send', 'recv', 'opcode', 'packet',
                             'march', 'train', 'build', 'attack', 'army', 'troop',
                             'cocos', 'game', 'battle', 'hero', 'soldier']
            is_game = any(any(ind in s.lower() for ind in game_indicators) for s in nearby_strings)

            category = "GAME" if is_game else ("SSL/HTTP" if is_ssl else "UNKNOWN")

            results[imm16].append({
                'addr': addr,
                'category': category,
                'has_strh': found_strh,
                'stores': found_str_context[:5],
                'strings': nearby_strings[:10],
                'is_ssl': is_ssl,
            })

    return results

def approach3_find_17_multiply(data, text_addr, text_off, text_size):
    """Find the *17 multiply used in CMsgCodec encryption
    Looking for: MUL or MADD with constant 17, or ADD+LSL#4 pattern (x*16+x = x*17)"""
    print("\n=== APPROACH 3: Find *17 multiply (CMsgCodec core) ===")

    text_data = data[text_off:text_off + text_size]
    results = []

    CHUNK = 4 * 1024 * 1024
    for chunk_start in range(0, text_size, CHUNK):
        chunk_end = min(chunk_start + CHUNK, text_size)
        chunk_data = text_data[chunk_start:chunk_end]
        chunk_addr = text_addr + chunk_start

        for offset in range(0, len(chunk_data) - 8, 4):
            insn_bytes = struct.unpack_from("<I", chunk_data, offset)[0]

            # Look for MOVZ Wx, #17 (0x11)
            if (insn_bytes & 0xFFE0001F) == 0x52800000 | 0:  # any register
                pass
            if (insn_bytes & 0xFFE00000) == 0x52800000:
                imm16 = (insn_bytes >> 5) & 0xFFFF
                if imm16 == 17:
                    rd = insn_bytes & 0x1F
                    addr = chunk_addr + offset

                    # Check if nearby instructions have MUL/MADD using this register
                    has_mul = False
                    has_xor = False
                    has_loop = False
                    context = []

                    for look in range(-5, 20):
                        look_off = offset + look * 4
                        if look_off < 0 or look_off + 4 > len(chunk_data):
                            continue
                        li = struct.unpack_from("<I", chunk_data, look_off)[0]

                        # MUL: 0001_1011_000_Rm_01111_1_Rn_Rd
                        if (li & 0xFFE0FC00) == 0x1B007C00:
                            rm = (li >> 16) & 0x1F
                            if rm == rd:
                                has_mul = True
                                context.append(f"MUL at +{look*4}")

                        # MADD: 0001_1011_000_Rm_0_Ra_Rn_Rd
                        if (li & 0xFFE00000) == 0x1B000000:
                            rm = (li >> 16) & 0x1F
                            if rm == rd:
                                has_mul = True
                                context.append(f"MADD at +{look*4}")

                        # EOR (XOR): 0100_1010_000_Rm_...
                        if (li & 0xFF200000) == 0x4A000000:
                            has_xor = True
                            context.append(f"EOR at +{look*4}")

                        # LDRB (byte load - loop indicator)
                        if (li & 0xFFC00000) == 0x39400000 or (li & 0xFFE00C00) == 0x38400000:
                            has_loop = True

                    # Only report if we see MUL+XOR pattern (encryption)
                    if has_mul and has_xor:
                        results.append({
                            'addr': addr,
                            'register': rd,
                            'has_loop': has_loop,
                            'context': context,
                        })
                        print(f"  CANDIDATE at 0x{addr:08X}: MOV W{rd}, #17 + MUL + XOR {'+LOOP' if has_loop else ''}")

    return results

def disasm_around(data, text_addr, text_off, addr, count=100):
    """Disassemble 'count' instructions around an address"""
    md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
    md.detail = True

    start_addr = addr - (count // 2) * 4
    file_off = text_off + (start_addr - text_addr)

    if file_off < text_off:
        file_off = text_off
        start_addr = text_addr

    size = count * 4
    code = data[file_off:file_off + size]

    lines = []
    for insn in md.disasm(code, start_addr):
        marker = ""
        if insn.address == addr:
            marker = "  ; <<< TARGET >>>"
        lines.append(f"  0x{insn.address:08X}:  {insn.mnemonic:12s} {insn.op_str}{marker}")

    return "\n".join(lines)

def main():
    print("Loading libgame.so...")
    data = read_binary()
    print(f"Size: {len(data):,} bytes")

    text_addr, text_off, text_size = find_text_section(data)
    print(f".text: addr=0x{text_addr:X}, offset=0x{text_off:X}, size={text_size:,}")
    print(f".rodata: addr=0x{RODATA_ADDR:X}, offset=0x{RODATA_OFF:X}, size={RODATA_SIZE:,}")

    report = []
    report.append("# Real Game Handler Analysis")
    report.append(f"# Generated by 15_find_real_handlers.py")
    report.append("")
    report.append("## CRITICAL CORRECTION")
    report.append("Previous analysis (scripts 09/10/14) found MOVZ instructions matching game opcodes,")
    report.append("but these were **FALSE POSITIVES** in OpenSSL/libcurl code statically linked in libgame.so.")
    report.append("Evidence: strings like 'ssl/ssl_lib.c', 'NTLM', 'Digest', 'Basic', 'Bearer' near the references.")
    report.append("")
    report.append("This script uses better approaches to find the REAL game handlers.")
    report.append("")

    # Approach 1: CMSG_TABLE cross-references
    report.append("=" * 80)
    report.append("# APPROACH 1: CMSG_TABLE Cross-References")
    report.append(f"Looking for ADRP+ADD targeting 0x{CMSG_TABLE_ADDR:08X}")
    report.append("")

    xrefs = approach1_find_table_xrefs(data, text_addr, text_off, text_size)
    report.append(f"Found {len(xrefs)} cross-references to CMSG_TABLE:")

    for addr, adrp_rd, add_rd, add_imm in xrefs:
        report.append(f"\n### XREF at 0x{addr:08X}")
        report.append(f"ADRP X{adrp_rd} + ADD X{add_rd}, #0x{add_imm:X} (target = page + 0x{add_imm:X})")
        report.append("```asm")
        report.append(disasm_around(data, text_addr, text_off, addr, 120))
        report.append("```")

    # Approach 2: STRH opcode patterns
    report.append("")
    report.append("=" * 80)
    report.append("# APPROACH 2: Opcode Store Patterns (MOVZ + context)")
    report.append("")

    strh_results = approach2_find_strh_opcodes(data, text_addr, text_off, text_size)

    for opcode in sorted(strh_results.keys()):
        name = TARGET_OPCODES.get(opcode, "UNKNOWN")
        hits = strh_results[opcode]
        game_hits = [h for h in hits if not h['is_ssl']]
        ssl_hits = [h for h in hits if h['is_ssl']]

        report.append(f"\n## Opcode 0x{opcode:04X} ({name})")
        report.append(f"Total references: {len(hits)} (Game/Unknown: {len(game_hits)}, SSL/HTTP: {len(ssl_hits)})")

        for h in game_hits[:10]:  # Limit to 10 per opcode
            report.append(f"\n### 0x{h['addr']:08X} [{h['category']}]")
            if h['strings']:
                report.append(f"Nearby strings: {h['strings'][:5]}")
            if h['stores']:
                report.append(f"Store instructions: {h['stores']}")
            if h['has_strh']:
                report.append("**Has STRH with same register - likely writing opcode to packet!**")
            report.append("```asm")
            report.append(disasm_around(data, text_addr, text_off, h['addr'], 60))
            report.append("```")

    # Approach 3: *17 multiply pattern
    report.append("")
    report.append("=" * 80)
    report.append("# APPROACH 3: CMsgCodec Encryption Core (*17 multiply + XOR)")
    report.append("")

    mul17_results = approach3_find_17_multiply(data, text_addr, text_off, text_size)
    report.append(f"Found {len(mul17_results)} candidates with MOV #17 + MUL + XOR pattern:")

    for r in mul17_results[:20]:  # Show top 20
        report.append(f"\n### Candidate at 0x{r['addr']:08X}")
        report.append(f"Register: W{r['register']}, Has loop: {r['has_loop']}")
        report.append(f"Context: {r['context']}")
        report.append("```asm")
        report.append(disasm_around(data, text_addr, text_off, r['addr'], 80))
        report.append("```")

    # Write report
    out_path = os.path.join(FINDINGS_DIR, "real_handlers.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report))

    print(f"\nReport written to {out_path}")
    print(f"Total lines: {len(report)}")

if __name__ == "__main__":
    main()

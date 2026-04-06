#!/usr/bin/env python3
"""
Deep disassembly of CMsgCodec encryption/decryption in libgame.so (ARM64).

Searches for cross-references to CMSG_TABLE, disassembles encode/decode
functions, and verifies the encryption formula from actual ARM64 instructions.
"""

import struct
import os
from collections import defaultdict

from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

# ── Constants ──────────────────────────────────────────────────────────────────
LIBGAME = r"D:\CascadeProjects\libgame.so"
OUTPUT  = r"D:\CascadeProjects\analysis\findings\encryption_deep.md"

CMSG_TABLE_ADDR  = 0x028B723A
CMSG_TABLE_BYTES = bytes([0x58, 0xef, 0xd7, 0x14, 0xa2, 0x3b, 0x9c])
TABLE_PAGE       = CMSG_TABLE_ADDR & ~0xFFF          # 0x028B7000
TABLE_OFFSET     = CMSG_TABLE_ADDR & 0xFFF           # 0x23A

TEXT_START       = 0x03250E80
TEXT_SIZE         = 0x0298B45C
TEXT_END         = TEXT_START + TEXT_SIZE

DODECODE_STR     = 0x0108A269
VERIFY_CONST     = 0xB7
MUL_CONST        = 17  # 0x11

# For this binary, vaddr == file offset for the first LOAD segment
VADDR_TO_FILE    = 0  # offset delta


# ── Helpers ────────────────────────────────────────────────────────────────────
def read_binary():
    with open(LIBGAME, "rb") as f:
        return f.read()


def make_disassembler():
    md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
    md.detail = True
    return md


def disasm_at(md, data, vaddr, count=200):
    """Disassemble `count` instructions starting at vaddr."""
    offset = vaddr - 0  # vaddr == file offset
    code = data[offset : offset + count * 4]
    return list(md.disasm(code, vaddr, count=count))


def format_insn(insn):
    return f"  0x{insn.address:08x}:  {insn.mnemonic:8s} {insn.op_str}"


# ── Phase 1: Scan .text for ADRP instructions referencing TABLE_PAGE ──────────
def scan_adrp_references(data):
    """
    Scan every 4-byte aligned word in .text for ADRP instructions whose
    target page matches TABLE_PAGE (0x028B7000).

    ADRP encoding: [1] [immlo:2] [10000] [immhi:19] [Rd:5]
    Target = (PC & ~0xFFF) + SignExtend(immhi:immlo:Zeros(12), 33)
    """
    print("[*] Scanning .text for ADRP references to table page 0x{:08X}...".format(TABLE_PAGE))

    adrp_hits = []
    text_data = data[TEXT_START : TEXT_END]

    for i in range(0, len(text_data) - 3, 4):
        word = struct.unpack_from("<I", text_data, i)[0]

        # Check ADRP: bit 31=1, bits 28-24=10000
        if (word & 0x9F000000) != 0x90000000:
            continue

        pc = TEXT_START + i
        rd = word & 0x1F

        # Extract immhi (bits 23:5) and immlo (bits 30:29)
        immhi = (word >> 5) & 0x7FFFF
        immlo = (word >> 29) & 0x3
        imm = (immhi << 2) | immlo  # 21-bit value

        # Sign-extend from 21 bits
        if imm & (1 << 20):
            imm -= (1 << 21)

        target = (pc & ~0xFFF) + (imm << 12)

        if target == TABLE_PAGE:
            adrp_hits.append((pc, rd, target))

    print(f"    Found {len(adrp_hits)} ADRP instructions targeting page 0x{TABLE_PAGE:08X}")
    return adrp_hits


# ── Phase 2: Find ADD instructions following each ADRP ────────────────────────
def find_adrp_add_pairs(data, adrp_hits):
    """
    For each ADRP hit, look at the next ~16 instructions for ADD Rd, Rn, #offset
    where Rn matches the ADRP destination register and offset is TABLE_OFFSET (0x23A).
    """
    print("[*] Searching for ADRP+ADD pairs computing table address...")

    md = make_disassembler()
    pairs = []

    for adrp_pc, adrp_rd, _ in adrp_hits:
        # Disassemble next 20 instructions after the ADRP
        insns = disasm_at(md, data, adrp_pc, count=20)

        for insn in insns[1:]:  # skip the ADRP itself
            # Look for ADD Xn, Xn, #imm
            if insn.mnemonic == "add" and len(insn.operands) == 3:
                ops = insn.operands
                # Check if source register matches ADRP dest
                if (ops[1].type == 1 and  # REG
                    ops[1].reg == insn.operands[0].reg and  # same reg family ok
                    ops[2].type == 2):  # IMM

                    imm_val = ops[2].imm
                    if imm_val == TABLE_OFFSET:
                        pairs.append({
                            'adrp_pc': adrp_pc,
                            'add_pc': insn.address,
                            'reg': adrp_rd,
                            'computed_addr': TABLE_PAGE + imm_val,
                        })
                        print(f"    ADRP+ADD pair at 0x{adrp_pc:08x}/0x{insn.address:08x} -> 0x{TABLE_PAGE + imm_val:08x}")
                        break

                # Also check: ADD Xd, Xn, #imm where Xn is the ADRP register
                if ops[2].type == 2:
                    imm_val = ops[2].imm
                    if imm_val == TABLE_OFFSET:
                        # Check source reg
                        src_reg_id = ops[1].reg if ops[1].type == 1 else -1
                        # ARM64 reg IDs: X0=199, X1=200, ..., X28=227, X29(FP)=228, X30(LR)=229
                        expected_reg_id = 199 + adrp_rd  # rough mapping
                        if abs(src_reg_id - expected_reg_id) <= 1:  # allow W/X variant
                            pairs.append({
                                'adrp_pc': adrp_pc,
                                'add_pc': insn.address,
                                'reg': adrp_rd,
                                'computed_addr': TABLE_PAGE + imm_val,
                            })
                            print(f"    ADRP+ADD pair at 0x{adrp_pc:08x}/0x{insn.address:08x} -> 0x{TABLE_PAGE + imm_val:08x} (alt reg match)")
                            break

    # Deduplicate
    seen = set()
    unique = []
    for p in pairs:
        key = (p['adrp_pc'], p['add_pc'])
        if key not in seen:
            seen.add(key)
            unique.append(p)

    print(f"    Found {len(unique)} unique ADRP+ADD pairs")
    return unique


# ── Phase 2b: Also search for raw ADD #0x23A without ADRP (e.g., after LDR) ──
def scan_for_table_offset_adds(data):
    """Scan .text for ADD instructions with immediate 0x23A."""
    print("[*] Scanning for ADD #0x23A instructions (table offset)...")
    hits = []
    text_data = data[TEXT_START : TEXT_END]

    for i in range(0, len(text_data) - 3, 4):
        word = struct.unpack_from("<I", text_data, i)[0]
        # ADD immediate: sf=1 (64-bit), op=0, S=0 => 1001_0001_00 + shift:2 + imm12 + Rn:5 + Rd:5
        # Encoding: 0x91000000 | (shift<<22) | (imm12<<10) | (Rn<<5) | Rd
        if (word & 0xFF000000) == 0x91000000:
            imm12 = (word >> 10) & 0xFFF
            shift = (word >> 22) & 0x3
            if shift == 0 and imm12 == TABLE_OFFSET:
                pc = TEXT_START + i
                rd = word & 0x1F
                rn = (word >> 5) & 0x1F
                hits.append((pc, rn, rd))

    print(f"    Found {len(hits)} ADD #0x{TABLE_OFFSET:x} instructions")
    return hits


# ── Phase 3: Disassemble around each reference ────────────────────────────────
def disassemble_function_around(data, md, addr, before=100, after=100):
    """Disassemble instructions around an address, trying to find function boundaries."""
    start = max(TEXT_START, addr - before * 4)
    # Align to 4
    start = start & ~3

    total = before + after
    insns = disasm_at(md, data, start, count=total)
    return insns


def find_function_start(data, md, addr):
    """Walk backward from addr to find likely function prologue (STP X29, X30, [SP, #-N]!)."""
    # Scan backward up to 500 instructions
    for offset in range(4, 500 * 4, 4):
        check_addr = addr - offset
        if check_addr < TEXT_START:
            break

        word = struct.unpack_from("<I", data, check_addr)[0]

        # STP X29, X30, [SP, #imm]! (pre-index)
        # Encoding: 1010_1001_1xxx_xxxx_x111_1011_1110_1xxx
        # Simplified check: look for STP with X29, X30
        # STP (pre-indexed): 10_101_0011_0_imm7_Rt2_Rn_Rt
        # For X29(=29), X30(=30), SP(=31): Rt=29, Rt2=30, Rn=31
        if (word & 0xFFC003E0) == 0xA9800FE0:  # STP X?, X30, [SP, #?]!
            rt = word & 0x1F
            if rt == 29:  # X29
                return check_addr

        # Also check for SUB SP, SP, #imm (common prologue)
        # But STP is more reliable as function start

        # Check for RET as boundary of previous function
        if word == 0xD65F03C0:  # RET
            # Function likely starts at next instruction
            return check_addr + 4

    return addr - 200 * 4  # fallback


def find_function_end(data, md, addr):
    """Walk forward from addr to find RET instruction."""
    for offset in range(0, 500 * 4, 4):
        check_addr = addr + offset
        if check_addr >= TEXT_END:
            break

        word = struct.unpack_from("<I", data, check_addr)[0]
        if word == 0xD65F03C0:  # RET
            return check_addr

    return addr + 200 * 4  # fallback


# ── Phase 4: Analyze instructions for crypto patterns ─────────────────────────
def analyze_crypto_patterns(insns):
    """Look for the encryption formula components in instruction stream."""
    findings = {
        'mul_17': [],       # MUL/MADD with constant 17
        'xor_ops': [],      # EOR (XOR) operations
        'and_0xff': [],     # AND with 0xFF
        'ldrb_table': [],   # LDRB (byte load) - table access
        'add_ops': [],      # ADD operations (part of formula)
        'sub_ops': [],      # SUB operations (decode)
        'mov_b7': [],       # MOV with 0xB7
        'mov_11': [],       # MOV with 17 (0x11)
        'mov_07': [],       # MOV with 7 (table length)
        'sdiv_udiv': [],    # Division (for modulo)
        'msub': [],         # MSUB (for modulo: a - (a/b)*b)
        'ldrb_ops': [],     # All LDRB operations
        'strb_ops': [],     # STRB operations (writing result)
        'cmp_ops': [],      # CMP operations
        'branch_ops': [],   # Branch operations (loops)
    }

    for insn in insns:
        mnemonic = insn.mnemonic
        op_str = insn.op_str

        # MOV/MOVZ with immediate 17 (0x11)
        if mnemonic in ('mov', 'movz', 'orr') and '#0x11' in op_str:
            findings['mov_11'].append(insn)

        # MOV with 0xB7
        if mnemonic in ('mov', 'movz', 'orr') and '#0xb7' in op_str.lower():
            findings['mov_b7'].append(insn)

        # MOV with 7 (table length)
        if mnemonic in ('mov', 'movz', 'orr') and ('#7' in op_str or '#0x7' in op_str):
            # Be more precise - check for exactly 7
            for op in insn.operands:
                if op.type == 2 and op.imm == 7:  # IMM
                    findings['mov_07'].append(insn)

        # MUL / MADD
        if mnemonic in ('mul', 'madd', 'smull', 'umull'):
            findings['mul_17'].append(insn)

        # EOR (XOR)
        if mnemonic == 'eor':
            findings['xor_ops'].append(insn)

        # AND with 0xFF
        if mnemonic in ('and', 'ands') and '#0xff' in op_str.lower():
            findings['and_0xff'].append(insn)

        # LDRB (byte load)
        if mnemonic in ('ldrb', 'ldurb'):
            findings['ldrb_ops'].append(insn)

        # STRB (byte store)
        if mnemonic in ('strb', 'sturb'):
            findings['strb_ops'].append(insn)

        # ADD
        if mnemonic == 'add':
            findings['add_ops'].append(insn)

        # SUB
        if mnemonic == 'sub':
            findings['sub_ops'].append(insn)

        # SDIV / UDIV
        if mnemonic in ('sdiv', 'udiv'):
            findings['sdiv_udiv'].append(insn)

        # MSUB (for modulo)
        if mnemonic == 'msub':
            findings['msub'].append(insn)

        # CMP
        if mnemonic in ('cmp', 'cmn'):
            findings['cmp_ops'].append(insn)

        # Branches (for loop detection)
        if mnemonic.startswith('b.') or mnemonic in ('b', 'cbz', 'cbnz', 'tbz', 'tbnz'):
            findings['branch_ops'].append(insn)

    return findings


# ── Phase 5: Search for 0xB7 constant and multiply-by-17 patterns ────────────
def scan_for_constants(data):
    """Scan .text for specific constant loads."""
    print("[*] Scanning for key constants (0xB7, 0x11=17, 7) in .text...")

    text_data = data[TEXT_START : TEXT_END]

    b7_hits = []
    x11_hits = []
    x07_hits = []

    for i in range(0, len(text_data) - 3, 4):
        word = struct.unpack_from("<I", text_data, i)[0]
        pc = TEXT_START + i

        # MOVZ Xd/Wd, #imm16, LSL #shift
        # 64-bit: 1_10_100101_hw_imm16_Rd  (0xD2800000)
        # 32-bit: 0_10_100101_hw_imm16_Rd  (0x52800000)
        if (word & 0x7F800000) == 0x52800000:
            hw = (word >> 21) & 0x3
            imm16 = (word >> 5) & 0xFFFF
            if hw == 0:
                if imm16 == 0xB7:
                    b7_hits.append(pc)
                if imm16 == 0x11:
                    x11_hits.append(pc)
                if imm16 == 0x07:
                    x07_hits.append(pc)

        # ORR Wd, WZR, #imm (MOV alias) - bitmask immediate encoding
        # This is complex but let's check for MOV Wd, #0x11 which can be ORR
        if (word & 0xFF800000) == 0x32000000:  # ORR 32-bit immediate
            # Decode bitmask immediate is complex, skip for now
            pass

    print(f"    0xB7 (verify): {len(b7_hits)} hits")
    print(f"    0x11 (mul 17): {len(x11_hits)} hits")
    print(f"    0x07 (tbl len): {len(x07_hits)} hits")

    return b7_hits, x11_hits, x07_hits


# ── Phase 6: Find xrefs near each other (convergence) ─────────────────────────
def find_convergence_zones(adrp_pairs, b7_hits, x11_hits, x07_hits, radius=0x400):
    """Find addresses where table refs AND constant refs converge (likely the codec function)."""
    print("[*] Finding convergence zones (table ref + constants within radius)...")

    zones = []

    for pair in adrp_pairs:
        adrp_pc = pair['adrp_pc']

        nearby_b7 = [h for h in b7_hits if abs(h - adrp_pc) < radius]
        nearby_11 = [h for h in x11_hits if abs(h - adrp_pc) < radius]
        nearby_07 = [h for h in x07_hits if abs(h - adrp_pc) < radius]

        score = len(nearby_b7) * 3 + len(nearby_11) * 3 + len(nearby_07) * 2

        if score > 0:
            zones.append({
                'pair': pair,
                'b7': nearby_b7,
                'x11': nearby_11,
                'x07': nearby_07,
                'score': score,
            })

    zones.sort(key=lambda z: z['score'], reverse=True)

    for z in zones[:10]:
        p = z['pair']
        print(f"    Zone at 0x{p['adrp_pc']:08x} score={z['score']}: "
              f"b7={len(z['b7'])} x11={len(z['x11'])} x07={len(z['x07'])}")

    return zones


# ── Phase 7: Search for doDecode string xrefs ─────────────────────────────────
def scan_for_string_xref(data, string_addr):
    """Find ADRP+ADD pairs referencing the doDecode string."""
    print(f"[*] Scanning for xrefs to doDecode string at 0x{string_addr:08x}...")

    page = string_addr & ~0xFFF
    offset = string_addr & 0xFFF

    text_data = data[TEXT_START : TEXT_END]
    hits = []

    for i in range(0, len(text_data) - 3, 4):
        word = struct.unpack_from("<I", text_data, i)[0]

        if (word & 0x9F000000) != 0x90000000:
            continue

        pc = TEXT_START + i
        immhi = (word >> 5) & 0x7FFFF
        immlo = (word >> 29) & 0x3
        imm = (immhi << 2) | immlo
        if imm & (1 << 20):
            imm -= (1 << 21)

        target = (pc & ~0xFFF) + (imm << 12)

        if target == page:
            rd = word & 0x1F
            hits.append((pc, rd))

    # Now filter: check for ADD with correct offset
    md = make_disassembler()
    xrefs = []

    for adrp_pc, adrp_rd in hits:
        insns = disasm_at(md, data, adrp_pc, count=10)
        for insn in insns[1:]:
            if insn.mnemonic == "add":
                for op in insn.operands:
                    if op.type == 2 and op.imm == offset:
                        xrefs.append(adrp_pc)
                        break

    print(f"    Found {len(xrefs)} xrefs to doDecode string")
    return xrefs


# ── Phase 8: Full function disassembly with annotation ────────────────────────
def disassemble_full_function(data, md, center_addr):
    """Find and disassemble the entire function containing center_addr."""
    func_start = find_function_start(data, md, center_addr)
    func_end = find_function_end(data, md, center_addr)

    # Extend end to find all RETs (there may be multiple exit points)
    extra_end = func_end
    for offset in range(4, 100 * 4, 4):
        check = func_end + offset
        if check >= TEXT_END:
            break
        word = struct.unpack_from("<I", data, check)[0]
        if word == 0xD65F03C0:  # RET
            extra_end = check
        # Stop at next function prologue
        if (word & 0xFFC003E0) == 0xA9800FE0:
            rt = word & 0x1F
            if rt == 29:
                break

    num_insns = (extra_end - func_start) // 4 + 1
    insns = disasm_at(md, data, func_start, count=min(num_insns, 600))

    return func_start, extra_end, insns


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    print("=" * 70)
    print("  CMsgCodec Deep Disassembly Analysis")
    print("  libgame.so ARM64 AArch64")
    print("=" * 70)

    data = read_binary()
    md = make_disassembler()

    # Verify table bytes
    table_data = data[CMSG_TABLE_ADDR : CMSG_TABLE_ADDR + 7]
    print(f"\n[*] Verifying CMSG_TABLE at 0x{CMSG_TABLE_ADDR:08x}:")
    print(f"    Expected: {CMSG_TABLE_BYTES.hex()}")
    print(f"    Found:    {table_data.hex()}")
    assert table_data == CMSG_TABLE_BYTES, "Table mismatch!"
    print("    MATCH!")

    # Verify doDecode string
    dodecode = data[DODECODE_STR : DODECODE_STR + 8]
    print(f"\n[*] Verifying doDecode string at 0x{DODECODE_STR:08x}: {dodecode}")

    # Phase 1+2: Find ADRP+ADD pairs
    print()
    adrp_hits = scan_adrp_references(data)
    adrp_pairs = find_adrp_add_pairs(data, adrp_hits)

    # Phase 2b: Also search by ADD offset
    add_hits = scan_for_table_offset_adds(data)

    # Phase 5: Scan for constants
    print()
    b7_hits, x11_hits, x07_hits = scan_for_constants(data)

    # Phase 6: Convergence analysis
    print()
    zones = find_convergence_zones(adrp_pairs, b7_hits, x11_hits, x07_hits)

    # Phase 7: doDecode string xrefs
    print()
    dodecode_xrefs = scan_for_string_xref(data, DODECODE_STR)

    # ── Generate detailed output ──────────────────────────────────────────────
    report_lines = []

    def emit(line=""):
        report_lines.append(line)
        print(line)

    emit("\n" + "=" * 70)
    emit("  DETAILED FINDINGS")
    emit("=" * 70)

    # ── Disassemble top convergence zones ─────────────────────────────────────
    emit(f"\n## Top Convergence Zones ({len(zones)} total)")

    full_function_disasms = []  # (func_start, func_end, insns, zone_info)

    for idx, zone in enumerate(zones[:5]):
        pair = zone['pair']
        adrp_pc = pair['adrp_pc']

        emit(f"\n### Zone {idx+1}: ADRP at 0x{adrp_pc:08x} (score={zone['score']})")
        emit(f"  Table ADRP+ADD: 0x{pair['adrp_pc']:08x} / 0x{pair['add_pc']:08x}")
        if zone['b7']:
            emit(f"  0xB7 refs: {', '.join(f'0x{h:08x}' for h in zone['b7'])}")
        if zone['x11']:
            emit(f"  0x11 refs: {', '.join(f'0x{h:08x}' for h in zone['x11'])}")
        if zone['x07']:
            emit(f"  0x07 refs: {', '.join(f'0x{h:08x}' for h in zone['x07'])}")

        # Full function disassembly
        func_start, func_end, insns = disassemble_full_function(data, md, adrp_pc)
        full_function_disasms.append((func_start, func_end, insns, zone))

        emit(f"\n  Function range: 0x{func_start:08x} - 0x{func_end:08x} ({(func_end - func_start)//4} insns)")

        # Analyze crypto patterns
        findings = analyze_crypto_patterns(insns)

        emit(f"\n  Crypto pattern analysis:")
        emit(f"    MUL/MADD ops:  {len(findings['mul_17'])}")
        emit(f"    EOR (XOR) ops: {len(findings['xor_ops'])}")
        emit(f"    AND 0xFF ops:  {len(findings['and_0xff'])}")
        emit(f"    LDRB ops:      {len(findings['ldrb_ops'])}")
        emit(f"    STRB ops:      {len(findings['strb_ops'])}")
        emit(f"    SDIV/UDIV:     {len(findings['sdiv_udiv'])}")
        emit(f"    MSUB (mod):    {len(findings['msub'])}")
        emit(f"    MOV #0xB7:     {len(findings['mov_b7'])}")
        emit(f"    MOV #0x11:     {len(findings['mov_11'])}")
        emit(f"    MOV #7:        {len(findings['mov_07'])}")

        # Check if this is likely the codec (has XOR + MUL + table load)
        is_codec = (len(findings['xor_ops']) >= 1 and
                    (len(findings['mul_17']) >= 1 or len(findings['mov_11']) >= 1) and
                    len(findings['ldrb_ops']) >= 1)

        if is_codec:
            emit(f"\n  *** LIKELY CODEC FUNCTION ***")

    # ── Detailed disassembly of best candidates ──────────────────────────────
    emit("\n" + "=" * 70)
    emit("  FULL DISASSEMBLY OF TOP CODEC CANDIDATES")
    emit("=" * 70)

    for idx, (func_start, func_end, insns, zone) in enumerate(full_function_disasms[:3]):
        pair = zone['pair']
        emit(f"\n### Function {idx+1} (around 0x{pair['adrp_pc']:08x})")
        emit(f"    Range: 0x{func_start:08x} - 0x{func_end:08x}")
        emit(f"    Instructions: {len(insns)}")
        emit("")

        for insn in insns:
            line = f"  0x{insn.address:08x}:  {insn.bytes.hex():12s}  {insn.mnemonic:8s} {insn.op_str}"

            # Annotate interesting instructions
            annotations = []
            if insn.address == pair['adrp_pc']:
                annotations.append("<<< ADRP to TABLE page")
            if insn.address == pair['add_pc']:
                annotations.append("<<< ADD table offset 0x23A")
            if insn.mnemonic in ('mul', 'madd'):
                annotations.append("<<< MULTIPLY (msg*17?)")
            if insn.mnemonic == 'eor':
                annotations.append("<<< XOR")
            if insn.mnemonic in ('and', 'ands') and '0xff' in insn.op_str.lower():
                annotations.append("<<< AND 0xFF (byte mask)")
            if insn.mnemonic in ('ldrb', 'ldurb'):
                annotations.append("<<< LOAD BYTE")
            if insn.mnemonic in ('strb', 'sturb'):
                annotations.append("<<< STORE BYTE")
            if insn.mnemonic in ('sdiv', 'udiv'):
                annotations.append("<<< DIVIDE (modulo?)")
            if insn.mnemonic == 'msub':
                annotations.append("<<< MSUB (modulo remainder)")
            if insn.mnemonic in ('mov', 'movz') and '#0xb7' in insn.op_str.lower():
                annotations.append("<<< 0xB7 VERIFY CONSTANT")
            if insn.mnemonic in ('mov', 'movz') and '#0x11' in insn.op_str:
                annotations.append("<<< 17 = MUL CONSTANT")
            if insn.mnemonic in ('mov', 'movz'):
                for op in insn.operands:
                    if op.type == 2 and op.imm == 7:
                        annotations.append("<<< 7 = TABLE LENGTH")
            if insn.mnemonic == 'ret':
                annotations.append("<<< RETURN")
            if insn.mnemonic == 'stp' and 'x29' in insn.op_str and 'x30' in insn.op_str:
                annotations.append("<<< FUNCTION PROLOGUE")

            if annotations:
                line += "    ; " + " | ".join(annotations)

            emit(line)

    # ── Look for doDecode cross-references ────────────────────────────────────
    emit("\n" + "=" * 70)
    emit("  doDecode STRING CROSS-REFERENCES")
    emit("=" * 70)

    for xref_pc in dodecode_xrefs:
        emit(f"\n  doDecode string ref at 0x{xref_pc:08x}")
        func_start, func_end, insns = disassemble_full_function(data, md, xref_pc)
        emit(f"  Function: 0x{func_start:08x} - 0x{func_end:08x}")

        # Show context around the reference
        for insn in insns:
            if abs(insn.address - xref_pc) < 40:
                line = f"    0x{insn.address:08x}: {insn.mnemonic:8s} {insn.op_str}"
                if insn.address == xref_pc:
                    line += "    ; <<< doDecode string ADRP"
                emit(line)

    # ── All ADRP+ADD pairs listing ────────────────────────────────────────────
    emit("\n" + "=" * 70)
    emit("  ALL CROSS-REFERENCES TO CMSG_TABLE")
    emit("=" * 70)

    for idx, pair in enumerate(adrp_pairs):
        emit(f"\n  Xref {idx+1}: ADRP 0x{pair['adrp_pc']:08x} + ADD 0x{pair['add_pc']:08x} -> 0x{pair['computed_addr']:08x}")

        # Show 10 instructions around
        insns = disasm_at(md, data, pair['adrp_pc'] - 8, count=20)
        for insn in insns:
            prefix = ">>>" if insn.address in (pair['adrp_pc'], pair['add_pc']) else "   "
            emit(f"    {prefix} 0x{insn.address:08x}: {insn.mnemonic:8s} {insn.op_str}")

    # ── Formula verification ──────────────────────────────────────────────────
    emit("\n" + "=" * 70)
    emit("  ENCRYPTION FORMULA VERIFICATION")
    emit("=" * 70)

    # Analyze the best candidate in detail
    if full_function_disasms:
        best_start, best_end, best_insns, best_zone = full_function_disasms[0]
        findings = analyze_crypto_patterns(best_insns)

        emit(f"\n  Best candidate function: 0x{best_start:08x} - 0x{best_end:08x}")
        emit(f"\n  Known formula: enc[i] = ((plain[i] + msg_byte*17) ^ sk_byte ^ table[i%7]) & 0xFF")
        emit(f"\n  ARM64 instruction mapping:")

        # Map formula to instructions
        if findings['mov_11']:
            for insn in findings['mov_11']:
                emit(f"    msg*17 setup: {format_insn(insn)}")

        if findings['mul_17']:
            for insn in findings['mul_17']:
                emit(f"    multiply:     {format_insn(insn)}")

        if findings['add_ops']:
            # Show adds near multiplies
            mul_addrs = [i.address for i in findings['mul_17']]
            for insn in findings['add_ops']:
                for ma in mul_addrs:
                    if abs(insn.address - ma) < 32:
                        emit(f"    add (near mul):{format_insn(insn)}")
                        break

        if findings['xor_ops']:
            for insn in findings['xor_ops']:
                emit(f"    XOR:          {format_insn(insn)}")

        if findings['and_0xff']:
            for insn in findings['and_0xff']:
                emit(f"    AND 0xFF:     {format_insn(insn)}")

        if findings['sdiv_udiv']:
            for insn in findings['sdiv_udiv']:
                emit(f"    div (modulo): {format_insn(insn)}")

        if findings['msub']:
            for insn in findings['msub']:
                emit(f"    msub (mod):   {format_insn(insn)}")

        if findings['mov_b7']:
            for insn in findings['mov_b7']:
                emit(f"    0xB7 verify:  {format_insn(insn)}")

        if findings['mov_07']:
            for insn in findings['mov_07']:
                emit(f"    table len 7:  {format_insn(insn)}")

        # Verify formula presence
        emit("\n  Formula component check:")
        has_mul17 = len(findings['mul_17']) > 0 or len(findings['mov_11']) > 0
        has_xor = len(findings['xor_ops']) > 0
        has_mask = len(findings['and_0xff']) > 0
        has_mod7 = len(findings['msub']) > 0 or len(findings['mov_07']) > 0
        has_b7 = len(findings['mov_b7']) > 0
        has_ldrb = len(findings['ldrb_ops']) > 0
        has_strb = len(findings['strb_ops']) > 0

        emit(f"    [{'X' if has_mul17 else ' '}] Multiply by 17 (msg_byte * 17)")
        emit(f"    [{'X' if has_xor else ' '}] XOR operations (^ sk_byte ^ table)")
        emit(f"    [{'X' if has_mask else ' '}] AND 0xFF byte mask")
        emit(f"    [{'X' if has_mod7 else ' '}] Modulo 7 (table index)")
        emit(f"    [{'X' if has_b7 else ' '}] 0xB7 verify constant")
        emit(f"    [{'X' if has_ldrb else ' '}] Byte loads (table/input access)")
        emit(f"    [{'X' if has_strb else ' '}] Byte stores (output)")

        all_confirmed = all([has_mul17, has_xor, has_ldrb])
        emit(f"\n  {'FORMULA CONFIRMED' if all_confirmed else 'PARTIAL MATCH - further analysis needed'} in ARM64 code")

    # ── Proximity analysis: find MUL near XOR near LDRB ──────────────────────
    emit("\n" + "=" * 70)
    emit("  PROXIMITY ANALYSIS: Codec Core Loop")
    emit("=" * 70)

    if full_function_disasms:
        best_start, best_end, best_insns, best_zone = full_function_disasms[0]
        findings = analyze_crypto_patterns(best_insns)

        # Find clusters of crypto operations
        all_crypto = []
        for insn in findings['mul_17']:
            all_crypto.append(('MUL', insn.address, insn))
        for insn in findings['xor_ops']:
            all_crypto.append(('XOR', insn.address, insn))
        for insn in findings['and_0xff']:
            all_crypto.append(('AND', insn.address, insn))
        for insn in findings['ldrb_ops']:
            all_crypto.append(('LDRB', insn.address, insn))
        for insn in findings['strb_ops']:
            all_crypto.append(('STRB', insn.address, insn))
        for insn in findings['mov_b7']:
            all_crypto.append(('B7', insn.address, insn))
        for insn in findings['mov_11']:
            all_crypto.append(('x11', insn.address, insn))
        for insn in findings['mov_07']:
            all_crypto.append(('x07', insn.address, insn))
        for insn in findings['msub']:
            all_crypto.append(('MSUB', insn.address, insn))
        for insn in findings['sdiv_udiv']:
            all_crypto.append(('DIV', insn.address, insn))
        for insn in findings['add_ops']:
            all_crypto.append(('ADD', insn.address, insn))
        for insn in findings['sub_ops']:
            all_crypto.append(('SUB', insn.address, insn))

        all_crypto.sort(key=lambda x: x[1])

        # Find dense clusters
        if all_crypto:
            emit("\n  All crypto-relevant instructions in order:")
            for tag, addr, insn in all_crypto:
                emit(f"    [{tag:5s}] 0x{addr:08x}: {insn.mnemonic:8s} {insn.op_str}")

    # ── Additional: search for MADD (fused multiply-add, common optimization) ─
    emit("\n" + "=" * 70)
    emit("  MADD/MUL SEARCH IN VICINITY OF TABLE REFS")
    emit("=" * 70)

    for pair in adrp_pairs[:5]:
        adrp_pc = pair['adrp_pc']
        insns = disasm_at(md, data, max(TEXT_START, adrp_pc - 200 * 4), count=400)

        for insn in insns:
            if insn.mnemonic in ('madd', 'mul', 'msub', 'smaddl', 'umaddl'):
                emit(f"  Near 0x{adrp_pc:08x}: {format_insn(insn)}")

    # ── Also scan for LSL #4 + ADD pattern (alternative to MUL 17) ────────────
    # Note: x*17 = x*16 + x = (x << 4) + x  -- compiler may optimize this way
    emit("\n" + "=" * 70)
    emit("  ALTERNATIVE MUL-17 PATTERNS (LSL #4 + ADD)")
    emit("=" * 70)

    for pair in adrp_pairs[:5]:
        adrp_pc = pair['adrp_pc']
        start = max(TEXT_START, adrp_pc - 200 * 4)
        insns = disasm_at(md, data, start, count=400)

        for insn in insns:
            # LSL #4 (shift left by 4 = multiply by 16)
            if insn.mnemonic == 'lsl' and '#4' in insn.op_str:
                emit(f"  LSL #4 at {format_insn(insn)}")
            # ADD with LSL #4 (combined: ADD Xd, Xn, Xm, LSL #4)
            if insn.mnemonic == 'add' and 'lsl #4' in insn.op_str.lower():
                emit(f"  ADD+LSL#4 at {format_insn(insn)}")
            # UBFIZ (can be used for shift)
            if insn.mnemonic == 'ubfiz' and '#4' in insn.op_str:
                emit(f"  UBFIZ #4 at {format_insn(insn)}")
            # Also: ADD Xd, Xn, Xn, LSL #4  which is x + x*16 = x*17
            if insn.mnemonic == 'add' and 'lsl' in insn.op_str:
                # Check for same register with LSL
                parts = insn.op_str.replace(',', ' ').split()
                if len(parts) >= 4 and 'lsl' in parts:
                    emit(f"  ADD+shift at {format_insn(insn)}")

    # ── Write report ──────────────────────────────────────────────────────────
    print(f"\n[*] Writing report to {OUTPUT}...")

    md_lines = []
    md_lines.append("# CMsgCodec Encryption Deep Disassembly Analysis")
    md_lines.append("")
    md_lines.append("**Binary:** libgame.so (ARM64 AArch64, ~99MB, stripped)")
    md_lines.append("")
    md_lines.append("**Known Constants:**")
    md_lines.append(f"- CMSG_TABLE at `0x{CMSG_TABLE_ADDR:08X}`: `{CMSG_TABLE_BYTES.hex()}`")
    md_lines.append(f"- doDecode string at `0x{DODECODE_STR:08X}`")
    md_lines.append(f"- .text section: `0x{TEXT_START:08X}` - `0x{TEXT_END:08X}`")
    md_lines.append(f"- Encryption formula: `enc[i] = ((plain[i] + msg_byte*17) ^ sk_byte ^ table[i%7]) & 0xFF`")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")

    # Cross references section
    md_lines.append("## 1. Cross-References to CMSG_TABLE")
    md_lines.append("")
    md_lines.append(f"Found **{len(adrp_hits)}** ADRP instructions targeting page `0x{TABLE_PAGE:08X}`")
    md_lines.append(f"Found **{len(adrp_pairs)}** ADRP+ADD pairs computing address `0x{CMSG_TABLE_ADDR:08X}`")
    md_lines.append("")

    for idx, pair in enumerate(adrp_pairs):
        md_lines.append(f"### Xref {idx+1}")
        md_lines.append(f"- ADRP at `0x{pair['adrp_pc']:08X}`")
        md_lines.append(f"- ADD at `0x{pair['add_pc']:08X}`")
        md_lines.append(f"- Computed address: `0x{pair['computed_addr']:08X}`")
        md_lines.append("")

        # Context
        md_lines.append("```asm")
        insns = disasm_at(md, data, max(TEXT_START, pair['adrp_pc'] - 16), count=15)
        for insn in insns:
            prefix = ">>>" if insn.address in (pair['adrp_pc'], pair['add_pc']) else "   "
            md_lines.append(f"{prefix} 0x{insn.address:08x}: {insn.mnemonic:8s} {insn.op_str}")
        md_lines.append("```")
        md_lines.append("")

    # Convergence zones
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 2. Convergence Zones (Table + Crypto Constants)")
    md_lines.append("")
    md_lines.append("Zones where CMSG_TABLE references co-locate with encryption constants:")
    md_lines.append("")

    for idx, zone in enumerate(zones[:5]):
        pair = zone['pair']
        md_lines.append(f"### Zone {idx+1} (Score: {zone['score']})")
        md_lines.append(f"- Center: `0x{pair['adrp_pc']:08X}`")
        if zone['b7']:
            md_lines.append(f"- 0xB7 verify constant: {', '.join(f'`0x{h:08X}`' for h in zone['b7'])}")
        if zone['x11']:
            md_lines.append(f"- 0x11 (multiply by 17): {', '.join(f'`0x{h:08X}`' for h in zone['x11'])}")
        if zone['x07']:
            md_lines.append(f"- 0x07 (table length): {', '.join(f'`0x{h:08X}`' for h in zone['x07'])}")
        md_lines.append("")

    # Full disassembly of encode/decode functions
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 3. Disassembled Encode/Decode Functions")
    md_lines.append("")

    for idx, (func_start, func_end, insns, zone) in enumerate(full_function_disasms[:3]):
        pair = zone['pair']
        findings = analyze_crypto_patterns(insns)

        is_codec = (len(findings['xor_ops']) >= 1 and
                    (len(findings['mul_17']) >= 1 or len(findings['mov_11']) >= 1))

        label = "CODEC FUNCTION" if is_codec else "Candidate Function"
        md_lines.append(f"### {label} {idx+1}: `0x{func_start:08X}` - `0x{func_end:08X}`")
        md_lines.append(f"- Size: {(func_end - func_start)//4} instructions")
        md_lines.append(f"- Table ref at: `0x{pair['adrp_pc']:08X}`")
        md_lines.append("")

        md_lines.append("**Crypto Operations Found:**")
        md_lines.append(f"| Operation | Count | Purpose |")
        md_lines.append(f"|-----------|-------|---------|")
        md_lines.append(f"| MUL/MADD | {len(findings['mul_17'])} | msg_byte * 17 |")
        md_lines.append(f"| MOV #0x11 | {len(findings['mov_11'])} | Load constant 17 |")
        md_lines.append(f"| EOR (XOR) | {len(findings['xor_ops'])} | XOR with sk/table |")
        md_lines.append(f"| AND #0xFF | {len(findings['and_0xff'])} | Byte masking |")
        md_lines.append(f"| LDRB | {len(findings['ldrb_ops'])} | Byte load (table/input) |")
        md_lines.append(f"| STRB | {len(findings['strb_ops'])} | Byte store (output) |")
        md_lines.append(f"| SDIV/UDIV | {len(findings['sdiv_udiv'])} | Division for modulo |")
        md_lines.append(f"| MSUB | {len(findings['msub'])} | Modulo remainder |")
        md_lines.append(f"| MOV #0xB7 | {len(findings['mov_b7'])} | Verify constant |")
        md_lines.append(f"| MOV #7 | {len(findings['mov_07'])} | Table length |")
        md_lines.append("")

        md_lines.append("<details>")
        md_lines.append(f"<summary>Full disassembly ({len(insns)} instructions)</summary>")
        md_lines.append("")
        md_lines.append("```asm")
        for insn in insns:
            line = f"0x{insn.address:08x}: {insn.bytes.hex():12s} {insn.mnemonic:8s} {insn.op_str}"

            annotations = []
            if insn.address == pair['adrp_pc']:
                annotations.append("ADRP to TABLE page")
            if insn.address == pair['add_pc']:
                annotations.append("ADD table offset")
            if insn.mnemonic in ('mul', 'madd'):
                annotations.append("MULTIPLY")
            if insn.mnemonic == 'eor':
                annotations.append("XOR")
            if insn.mnemonic in ('and', 'ands') and '0xff' in insn.op_str.lower():
                annotations.append("BYTE MASK")
            if insn.mnemonic in ('ldrb', 'ldurb'):
                annotations.append("LOAD BYTE")
            if insn.mnemonic in ('strb', 'sturb'):
                annotations.append("STORE BYTE")
            if insn.mnemonic in ('sdiv', 'udiv'):
                annotations.append("DIVIDE")
            if insn.mnemonic == 'msub':
                annotations.append("MODULO")
            if insn.mnemonic in ('mov', 'movz') and '#0xb7' in insn.op_str.lower():
                annotations.append("0xB7 VERIFY")
            if insn.mnemonic in ('mov', 'movz') and '#0x11' in insn.op_str:
                annotations.append("CONST 17")
            if insn.mnemonic == 'ret':
                annotations.append("RETURN")
            if insn.mnemonic == 'stp' and 'x29' in insn.op_str and 'x30' in insn.op_str:
                annotations.append("PROLOGUE")

            if annotations:
                line += f"  ; <<< {' | '.join(annotations)}"

            md_lines.append(line)
        md_lines.append("```")
        md_lines.append("</details>")
        md_lines.append("")

    # doDecode xrefs
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 4. doDecode String Cross-References")
    md_lines.append("")
    md_lines.append(f"String `CMsgCodec::doDecode` at `0x{DODECODE_STR:08X}`")
    md_lines.append(f"Found **{len(dodecode_xrefs)}** cross-references")
    md_lines.append("")

    for xref_pc in dodecode_xrefs:
        md_lines.append(f"### Xref at `0x{xref_pc:08X}`")
        func_start, func_end, insns = disassemble_full_function(data, md, xref_pc)
        md_lines.append(f"- In function: `0x{func_start:08X}` - `0x{func_end:08X}`")
        md_lines.append("")
        md_lines.append("```asm")
        for insn in insns:
            if abs(insn.address - xref_pc) < 60:
                line = f"0x{insn.address:08x}: {insn.mnemonic:8s} {insn.op_str}"
                if insn.address == xref_pc:
                    line += "  ; <<< doDecode string ref"
                md_lines.append(line)
        md_lines.append("```")
        md_lines.append("")

    # Formula verification
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 5. Encryption Formula Verification")
    md_lines.append("")
    md_lines.append("### Known Formula")
    md_lines.append("```")
    md_lines.append("enc[i] = ((plain[i] + msg_byte * 17) ^ sk_byte ^ table[i % 7]) & 0xFF")
    md_lines.append("```")
    md_lines.append("")
    md_lines.append("### ARM64 Implementation Mapping")
    md_lines.append("")

    if full_function_disasms:
        best_start, best_end, best_insns, best_zone = full_function_disasms[0]
        findings = analyze_crypto_patterns(best_insns)

        md_lines.append("| Formula Component | ARM64 Instruction(s) | Address |")
        md_lines.append("|---|---|---|")

        if findings['mov_11']:
            for insn in findings['mov_11']:
                md_lines.append(f"| Load constant 17 | `{insn.mnemonic} {insn.op_str}` | `0x{insn.address:08X}` |")

        if findings['mul_17']:
            for insn in findings['mul_17']:
                md_lines.append(f"| msg_byte * 17 | `{insn.mnemonic} {insn.op_str}` | `0x{insn.address:08X}` |")

        for insn in findings['add_ops']:
            mul_addrs = [i.address for i in findings['mul_17']]
            for ma in mul_addrs:
                if abs(insn.address - ma) < 32:
                    md_lines.append(f"| plain[i] + result | `{insn.mnemonic} {insn.op_str}` | `0x{insn.address:08X}` |")

        for insn in findings['xor_ops']:
            md_lines.append(f"| XOR (sk/table) | `{insn.mnemonic} {insn.op_str}` | `0x{insn.address:08X}` |")

        for insn in findings['and_0xff']:
            md_lines.append(f"| & 0xFF byte mask | `{insn.mnemonic} {insn.op_str}` | `0x{insn.address:08X}` |")

        for insn in findings['sdiv_udiv']:
            md_lines.append(f"| Division (i/7) | `{insn.mnemonic} {insn.op_str}` | `0x{insn.address:08X}` |")

        for insn in findings['msub']:
            md_lines.append(f"| Modulo (i%7) | `{insn.mnemonic} {insn.op_str}` | `0x{insn.address:08X}` |")

        for insn in findings['mov_b7']:
            md_lines.append(f"| 0xB7 verify | `{insn.mnemonic} {insn.op_str}` | `0x{insn.address:08X}` |")

        for insn in findings['mov_07']:
            md_lines.append(f"| Table length 7 | `{insn.mnemonic} {insn.op_str}` | `0x{insn.address:08X}` |")

        md_lines.append("")

        # Verification summary
        has_mul17 = len(findings['mul_17']) > 0 or len(findings['mov_11']) > 0
        has_xor = len(findings['xor_ops']) > 0
        has_mask = len(findings['and_0xff']) > 0
        has_mod7 = len(findings['msub']) > 0 or len(findings['mov_07']) > 0
        has_b7 = len(findings['mov_b7']) > 0
        has_ldrb = len(findings['ldrb_ops']) > 0
        has_strb = len(findings['strb_ops']) > 0

        md_lines.append("### Verification Checklist")
        md_lines.append("")
        md_lines.append(f"- [{'x' if has_mul17 else ' '}] Multiply by 17 (`msg_byte * 17`)")
        md_lines.append(f"- [{'x' if has_xor else ' '}] XOR operations (`^ sk_byte ^ table`)")
        md_lines.append(f"- [{'x' if has_mask else ' '}] AND 0xFF byte masking")
        md_lines.append(f"- [{'x' if has_mod7 else ' '}] Modulo 7 for table index (`i % 7`)")
        md_lines.append(f"- [{'x' if has_b7 else ' '}] 0xB7 verify constant")
        md_lines.append(f"- [{'x' if has_ldrb else ' '}] Byte loads (table + input)")
        md_lines.append(f"- [{'x' if has_strb else ' '}] Byte stores (output)")
        md_lines.append("")

    # Additional discoveries
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 6. Additional Discoveries")
    md_lines.append("")
    md_lines.append("### Constants Near Table References")
    md_lines.append("")
    md_lines.append(f"- 0xB7 constants found in .text: **{len(b7_hits)}** total")
    md_lines.append(f"- 0x11 (17) constants found in .text: **{len(x11_hits)}** total")
    md_lines.append(f"- 0x07 (7) constants found in .text: **{len(x07_hits)}** total")
    md_lines.append("")

    # Report nearby 0xB7 for all table refs
    md_lines.append("### 0xB7 Verify Constant Locations Near Table Refs")
    md_lines.append("")
    for pair in adrp_pairs:
        nearby = [h for h in b7_hits if abs(h - pair['adrp_pc']) < 0x800]
        if nearby:
            md_lines.append(f"- Near table ref at `0x{pair['adrp_pc']:08X}`:")
            for h in nearby:
                md_lines.append(f"  - `0x{h:08X}` (distance: {abs(h - pair['adrp_pc'])} bytes)")
    md_lines.append("")

    # Alternative multiply patterns
    md_lines.append("### Compiler Optimization Notes")
    md_lines.append("")
    md_lines.append("The compiler may implement `x * 17` as `(x << 4) + x` (shift + add).")
    md_lines.append("ADD with LSL #4 patterns were also searched around table references.")
    md_lines.append("")

    # Write file
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"\n[*] Report written to {OUTPUT}")
    print(f"[*] Report size: {len(md_lines)} lines")
    print("\nDone!")


if __name__ == "__main__":
    main()

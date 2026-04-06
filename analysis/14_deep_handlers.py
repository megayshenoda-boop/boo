#!/usr/bin/env python3
"""
14_deep_handlers.py - Deep disassembly analysis of critical packet handler
functions in libgame.so (ARM64 AArch64 ELF, stripped).

Analyzes:
  1. 0x1B8B opcode handler (MOVZ at 0x58EA650, calls 0x5C851B0)
  2. 0x0CE8 START_MARCH handler (MOVZ at 0x555FE3C, 0x5566714, 0x5566B68)
  3. 0x5C851B0 function (send wrapper)
  4. 0x0CE7 CANCEL_MARCH handler (at 0x5AFE404)
  5. Cross-reference comparison of march-related opcodes

Output: D:\\CascadeProjects\\analysis\\findings\\handler_analysis.md
"""

import struct
import sys
import os
import time
from collections import defaultdict

try:
    from capstone import (
        Cs, CS_ARCH_ARM64, CS_MODE_ARM,
        CS_GRP_CALL, CS_GRP_JUMP, CS_GRP_RET,
        CS_OP_IMM, CS_OP_REG, CS_OP_MEM
    )
except ImportError:
    print("ERROR: capstone not installed. Run: pip install capstone")
    sys.exit(1)

# ─── Configuration ───────────────────────────────────────────────────────
LIBGAME_PATH = r"D:\CascadeProjects\libgame.so"
OUTPUT_PATH = r"D:\CascadeProjects\analysis\findings\handler_analysis.md"

# Known addresses
ADDR_1B8B_MOVZ      = 0x58EA650
ADDR_1B8B_TARGET_FN = 0x5C851B0
ADDR_0CE8_REFS      = [0x555FE3C, 0x5566714, 0x5566B68]
ADDR_0CE7_MOVZ      = 0x5AFE404
ADDR_GOSOCKET_SEND  = 0x4F95CA8

# How many instructions to disassemble in each direction
INSTR_BEFORE = 500
INSTR_AFTER  = 200
INSTR_FN     = 500   # for function-level analysis

# ARM64 instruction size
INSN_SIZE = 4

# ELF constants
ELF_MAGIC = b'\x7fELF'

# ─── Globals ─────────────────────────────────────────────────────────────
binary_data = None
elf_base = 0          # virtual address of first LOAD segment
elf_segments = []     # list of (vaddr, offset, filesz, memsz)
md = None             # capstone disassembler
report_lines = []     # output report


def log(msg=""):
    """Print and append to report."""
    print(msg)
    report_lines.append(msg)


def load_binary():
    """Load the ELF binary and parse segment info."""
    global binary_data, elf_segments, elf_base, md

    print(f"Loading {LIBGAME_PATH} ...")
    with open(LIBGAME_PATH, "rb") as f:
        binary_data = f.read()
    print(f"  Loaded {len(binary_data):,} bytes")

    # Verify ELF
    assert binary_data[:4] == ELF_MAGIC, "Not an ELF file"

    # Parse ELF64 header
    ei_class = binary_data[4]
    assert ei_class == 2, "Not 64-bit ELF"
    ei_data = binary_data[5]
    assert ei_data == 1, "Not little-endian"

    e_phoff = struct.unpack_from('<Q', binary_data, 0x20)[0]
    e_phentsize = struct.unpack_from('<H', binary_data, 0x36)[0]
    e_phnum = struct.unpack_from('<H', binary_data, 0x38)[0]

    print(f"  Program headers: {e_phnum} at offset 0x{e_phoff:X}, size {e_phentsize}")

    # Parse program headers - find LOAD segments
    for i in range(e_phnum):
        off = e_phoff + i * e_phentsize
        p_type = struct.unpack_from('<I', binary_data, off)[0]
        if p_type == 1:  # PT_LOAD
            p_offset = struct.unpack_from('<Q', binary_data, off + 0x08)[0]
            p_vaddr = struct.unpack_from('<Q', binary_data, off + 0x10)[0]
            p_filesz = struct.unpack_from('<Q', binary_data, off + 0x20)[0]
            p_memsz = struct.unpack_from('<Q', binary_data, off + 0x28)[0]
            p_flags = struct.unpack_from('<I', binary_data, off + 0x04)[0]
            elf_segments.append((p_vaddr, p_offset, p_filesz, p_memsz, p_flags))
            flag_str = ""
            if p_flags & 1: flag_str += "X"
            if p_flags & 2: flag_str += "W"
            if p_flags & 4: flag_str += "R"
            print(f"  LOAD: vaddr=0x{p_vaddr:X} offset=0x{p_offset:X} "
                  f"filesz=0x{p_filesz:X} flags={flag_str}")

    if elf_segments:
        elf_base = min(s[0] for s in elf_segments)
    print(f"  ELF base: 0x{elf_base:X}")

    # Initialize capstone
    md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
    md.detail = True
    print("  Capstone ARM64 disassembler ready")


def vaddr_to_offset(vaddr):
    """Convert virtual address to file offset using segment mapping."""
    for seg_vaddr, seg_offset, seg_filesz, seg_memsz, _ in elf_segments:
        if seg_vaddr <= vaddr < seg_vaddr + seg_filesz:
            return seg_offset + (vaddr - seg_vaddr)
    # Fallback: direct offset (for position-independent)
    return vaddr


def read_bytes_at_vaddr(vaddr, size):
    """Read bytes from the binary at a virtual address."""
    offset = vaddr_to_offset(vaddr)
    if offset < 0 or offset + size > len(binary_data):
        return None
    return binary_data[offset:offset + size]


def disassemble_at(vaddr, count=100):
    """Disassemble `count` instructions starting at vaddr."""
    # Read enough bytes (count * 4 for ARM64 fixed-width)
    raw = read_bytes_at_vaddr(vaddr, count * INSN_SIZE + 64)
    if raw is None:
        return []
    instructions = []
    for insn in md.disasm(raw, vaddr):
        instructions.append(insn)
        if len(instructions) >= count:
            break
    return instructions


def disassemble_range(start_vaddr, end_vaddr):
    """Disassemble all instructions in a virtual address range."""
    size = end_vaddr - start_vaddr
    if size <= 0 or size > 0x100000:
        return []
    raw = read_bytes_at_vaddr(start_vaddr, size)
    if raw is None:
        return []
    return list(md.disasm(raw, start_vaddr))


def find_function_prologue(target_addr, max_search_bytes=4096):
    """Search backwards from target_addr for a function prologue.

    ARM64 function prologues typically start with:
      STP X29, X30, [SP, #-N]!   (save frame pointer and link register)
    or sometimes:
      SUB SP, SP, #N             (allocate stack)
      STP X29, X30, [SP, ...]
    """
    search_start = target_addr - max_search_bytes
    raw = read_bytes_at_vaddr(search_start, max_search_bytes + 256)
    if raw is None:
        return None, []

    instructions = list(md.disasm(raw, search_start))

    # Build index by address
    addr_to_idx = {}
    for i, insn in enumerate(instructions):
        addr_to_idx[insn.address] = i

    # Find the target instruction index
    target_idx = None
    for i, insn in enumerate(instructions):
        if insn.address >= target_addr:
            target_idx = i
            break

    if target_idx is None:
        return None, instructions

    # Search backwards for STP X29, X30 pattern (function prologue)
    best_prologue = None
    for i in range(target_idx - 1, max(0, target_idx - INSTR_BEFORE), -1):
        insn = instructions[i]
        mnem = insn.mnemonic.lower()
        ops = insn.op_str.lower()

        # Classic ARM64 prologue: stp x29, x30, [sp, #-N]!
        if mnem == 'stp' and 'x29' in ops and 'x30' in ops and 'sp' in ops:
            best_prologue = insn.address
            # Check if there's a sub sp before it
            if i > 0:
                prev = instructions[i - 1]
                if prev.mnemonic.lower() == 'sub' and 'sp' in prev.op_str.lower():
                    best_prologue = prev.address
            break

        # Also check for PACIASP (pointer auth, common in newer ARM64)
        if mnem == 'paciasp':
            best_prologue = insn.address
            break

        # RET or another function's epilogue means we've gone too far
        if mnem == 'ret':
            # The function likely starts right after this ret
            if i + 1 < len(instructions):
                best_prologue = instructions[i + 1].address
            break

    return best_prologue, instructions


def format_instruction(insn, annotations=None):
    """Format a single instruction with optional annotations."""
    ann = ""
    if annotations and insn.address in annotations:
        ann = f"  ; {annotations[insn.address]}"
    return f"  0x{insn.address:08X}:  {insn.mnemonic:10s} {insn.op_str}{ann}"


def analyze_instruction_details(insn):
    """Extract detailed information from an instruction."""
    info = {
        'mnemonic': insn.mnemonic,
        'op_str': insn.op_str,
        'address': insn.address,
        'is_call': False,
        'is_branch': False,
        'is_ret': False,
        'call_target': None,
        'imm_values': [],
        'regs_read': [],
        'regs_written': [],
        'mem_ops': [],
    }

    try:
        # Check groups (capstone 5.x uses insn.groups directly)
        for g in insn.groups:
            if g == CS_GRP_CALL:
                info['is_call'] = True
            if g == CS_GRP_JUMP:
                info['is_branch'] = True
            if g == CS_GRP_RET:
                info['is_ret'] = True

        # Extract operands (capstone 5.x uses insn.operands directly)
        for op in insn.operands:
            if op.type == CS_OP_IMM:
                info['imm_values'].append(op.imm)
            elif op.type == CS_OP_REG:
                info['regs_written'].append(insn.reg_name(op.reg))
            elif op.type == CS_OP_MEM:
                info['mem_ops'].append({
                    'base': insn.reg_name(op.mem.base) if op.mem.base else None,
                    'index': insn.reg_name(op.mem.index) if op.mem.index else None,
                    'disp': op.mem.disp
                })

        # BL instruction -> call target
        if insn.mnemonic.lower() == 'bl':
            for op in insn.operands:
                if op.type == CS_OP_IMM:
                    info['call_target'] = op.imm
                    info['is_call'] = True
    except Exception:
        pass

    return info


def find_movz_movk_sequences(instructions):
    """Find MOVZ/MOVK sequences that build immediate values."""
    sequences = []
    i = 0
    while i < len(instructions):
        insn = instructions[i]
        if insn.mnemonic.lower() == 'movz':
            # Start of a potential sequence
            seq = [insn]
            reg = insn.op_str.split(',')[0].strip()
            j = i + 1
            while j < len(instructions):
                next_insn = instructions[j]
                if next_insn.mnemonic.lower() == 'movk' and next_insn.op_str.startswith(reg):
                    seq.append(next_insn)
                    j += 1
                else:
                    break

            # Reconstruct value
            value = 0
            for s in seq:
                parts = s.op_str.split(',')
                imm_part = parts[1].strip()
                shift = 0
                if len(parts) > 2 and 'lsl' in parts[2].lower():
                    shift_str = parts[2].strip().replace('lsl', '').replace('#', '').strip()
                    try:
                        shift = int(shift_str)
                    except:
                        pass
                try:
                    if imm_part.startswith('#'):
                        imm_part = imm_part[1:]
                    if imm_part.startswith('0x'):
                        imm_val = int(imm_part, 16)
                    else:
                        imm_val = int(imm_part)
                except:
                    imm_val = 0

                if s.mnemonic.lower() == 'movz':
                    value = imm_val << shift
                else:
                    # Clear the bits at the shift position and OR in new value
                    mask = ~(0xFFFF << shift) & 0xFFFFFFFFFFFFFFFF
                    value = (value & mask) | (imm_val << shift)

            sequences.append({
                'address': insn.address,
                'register': reg,
                'value': value,
                'instructions': seq,
                'hex': f"0x{value:X}"
            })
            i = j
        else:
            i += 1

    return sequences


def find_str_stp_sequences(instructions):
    """Find STR/STP sequences (memory writes) that indicate packet field construction."""
    stores = []
    for insn in instructions:
        mnem = insn.mnemonic.lower()
        if mnem in ('str', 'strb', 'strh', 'stur', 'sturb', 'sturh', 'stp'):
            info = analyze_instruction_details(insn)
            store_info = {
                'address': insn.address,
                'mnemonic': mnem,
                'op_str': insn.op_str,
                'mem_ops': info['mem_ops'],
            }
            # Determine field size
            if mnem in ('strb', 'sturb'):
                store_info['size'] = 1
                store_info['type'] = 'u8'
            elif mnem in ('strh', 'sturh'):
                store_info['size'] = 2
                store_info['type'] = 'u16'
            elif mnem in ('str', 'stur'):
                # Check if it's a W register (32-bit) or X register (64-bit)
                first_reg = insn.op_str.split(',')[0].strip().lower()
                if first_reg.startswith('w'):
                    store_info['size'] = 4
                    store_info['type'] = 'u32'
                elif first_reg.startswith('x'):
                    store_info['size'] = 8
                    store_info['type'] = 'u64'
                elif first_reg.startswith('s'):
                    store_info['size'] = 4
                    store_info['type'] = 'f32'
                elif first_reg.startswith('d'):
                    store_info['size'] = 8
                    store_info['type'] = 'f64'
                else:
                    store_info['size'] = 0
                    store_info['type'] = 'unknown'
            elif mnem == 'stp':
                first_reg = insn.op_str.split(',')[0].strip().lower()
                if first_reg.startswith('w'):
                    store_info['size'] = 8  # 2x32
                    store_info['type'] = '2xu32'
                elif first_reg.startswith('x'):
                    store_info['size'] = 16  # 2x64
                    store_info['type'] = '2xu64'
                else:
                    store_info['size'] = 0
                    store_info['type'] = 'unknown'
            else:
                store_info['size'] = 0
                store_info['type'] = 'unknown'

            stores.append(store_info)

    return stores


def find_bl_calls(instructions):
    """Find all BL (branch-link) calls in the instruction stream."""
    calls = []
    for insn in instructions:
        if insn.mnemonic.lower() == 'bl':
            info = analyze_instruction_details(insn)
            if info['call_target']:
                calls.append({
                    'address': insn.address,
                    'target': info['call_target'],
                    'target_hex': f"0x{info['call_target']:X}"
                })
    return calls


def find_cmp_branch_patterns(instructions):
    """Find CMP + conditional branch patterns (used for opcode selection)."""
    patterns = []
    for i, insn in enumerate(instructions):
        mnem = insn.mnemonic.lower()
        if mnem in ('cmp', 'cmn', 'tst'):
            # Look ahead for conditional branch
            for j in range(i + 1, min(i + 5, len(instructions))):
                next_insn = instructions[j]
                next_mnem = next_insn.mnemonic.lower()
                if next_mnem.startswith('b.') or next_mnem.startswith('cb') or next_mnem.startswith('tb'):
                    info = analyze_instruction_details(next_insn)
                    branch_target = None
                    for imm in info['imm_values']:
                        branch_target = imm
                    patterns.append({
                        'cmp_addr': insn.address,
                        'cmp_op': f"{insn.mnemonic} {insn.op_str}",
                        'branch_addr': next_insn.address,
                        'branch_op': f"{next_insn.mnemonic} {next_insn.op_str}",
                        'branch_target': branch_target,
                        'condition': next_mnem,
                    })
                    break
    return patterns


def find_adrp_add_pairs(instructions):
    """Find ADRP + ADD pairs used for loading addresses/string pointers."""
    pairs = []
    for i, insn in enumerate(instructions):
        if insn.mnemonic.lower() == 'adrp':
            # Extract the page address
            info = analyze_instruction_details(insn)
            reg = insn.op_str.split(',')[0].strip()
            page_addr = None
            for imm in info['imm_values']:
                page_addr = imm

            if page_addr is not None and i + 1 < len(instructions):
                next_insn = instructions[i + 1]
                if next_insn.mnemonic.lower() == 'add' and next_insn.op_str.startswith(reg):
                    next_info = analyze_instruction_details(next_insn)
                    offset = 0
                    for imm in next_info['imm_values']:
                        offset = imm
                    full_addr = page_addr + offset

                    # Try to read string at that address
                    string_data = read_bytes_at_vaddr(full_addr, 128)
                    string_val = None
                    if string_data:
                        try:
                            null_idx = string_data.index(0)
                            if null_idx > 0 and null_idx < 100:
                                candidate = string_data[:null_idx]
                                if all(0x20 <= b < 0x7f for b in candidate):
                                    string_val = candidate.decode('ascii')
                        except (ValueError, UnicodeDecodeError):
                            pass

                    pairs.append({
                        'address': insn.address,
                        'register': reg,
                        'page': page_addr,
                        'offset': offset,
                        'full_addr': full_addr,
                        'full_addr_hex': f"0x{full_addr:X}",
                        'string': string_val,
                    })
    return pairs


# ─── Analysis Functions ──────────────────────────────────────────────────

def analyze_1b8b_handler():
    """Deep analysis of the 0x1B8B opcode handler."""
    log("\n" + "=" * 80)
    log("# 1. OPCODE 0x1B8B DEEP ANALYSIS")
    log("=" * 80)
    log()
    log(f"Known: MOVZ with 0x1B8B at 0x{ADDR_1B8B_MOVZ:08X}")
    log(f"Known: Calls function at 0x{ADDR_1B8B_TARGET_FN:08X}")
    log()

    # 1a. Find function prologue
    log("## 1.1 Finding Function Entry Point")
    log()
    prologue_addr, all_insns = find_function_prologue(ADDR_1B8B_MOVZ, max_search_bytes=INSTR_BEFORE * 4)

    if prologue_addr:
        log(f"Function prologue found at: **0x{prologue_addr:08X}**")
        log(f"Distance from MOVZ: {ADDR_1B8B_MOVZ - prologue_addr} bytes "
            f"({(ADDR_1B8B_MOVZ - prologue_addr) // 4} instructions)")
    else:
        log("WARNING: Could not find function prologue, using search start")
        prologue_addr = ADDR_1B8B_MOVZ - (INSTR_BEFORE * 4)

    # 1b. Disassemble the full function region
    log()
    log("## 1.2 Full Disassembly: Before 0x1B8B MOVZ")
    log()

    start_addr = max(prologue_addr, ADDR_1B8B_MOVZ - INSTR_BEFORE * 4)
    end_addr = ADDR_1B8B_MOVZ + INSTR_AFTER * 4

    insns_before = disassemble_at(start_addr, INSTR_BEFORE + INSTR_AFTER + 100)

    # Build annotations
    annotations = {
        ADDR_1B8B_MOVZ: "<<< 0x1B8B OPCODE MOVZ HERE >>>",
    }
    if prologue_addr in [i.address for i in insns_before]:
        annotations[prologue_addr] = "<<< FUNCTION ENTRY >>>"

    # Find MOVZ/MOVK sequences for context
    movz_seqs = find_movz_movk_sequences(insns_before)
    for seq in movz_seqs:
        if seq['value'] == 0x1B8B:
            annotations[seq['address']] = f"<<< BUILDS VALUE 0x{seq['value']:X} (0x1B8B) >>>"
        elif seq['value'] > 0x100:
            if seq['address'] not in annotations:
                annotations[seq['address']] = f"builds value 0x{seq['value']:X} ({seq['value']})"

    # Find all BL calls
    calls = find_bl_calls(insns_before)
    for call in calls:
        tgt = call['target']
        note = f"CALL -> 0x{tgt:X}"
        if tgt == ADDR_1B8B_TARGET_FN:
            note = f"<<< CALL TO 0x1B8B HANDLER FUNCTION 0x{tgt:X} >>>"
        elif tgt == ADDR_GOSOCKET_SEND:
            note = "CALL -> GoSocket::sendData"
        annotations[call['address']] = note

    # Find ADRP+ADD pairs (string references)
    adrp_pairs = find_adrp_add_pairs(insns_before)
    for pair in adrp_pairs:
        if pair['string']:
            annotations[pair['address']] = f"ADRP+ADD -> 0x{pair['full_addr']:X} = \"{pair['string']}\""

    # Print annotated disassembly (around the MOVZ, 60 before + 40 after)
    movz_idx = None
    for i, insn in enumerate(insns_before):
        if insn.address == ADDR_1B8B_MOVZ:
            movz_idx = i
            break

    if movz_idx is not None:
        range_start = max(0, movz_idx - 80)
        range_end = min(len(insns_before), movz_idx + 80)
    else:
        range_start = 0
        range_end = min(len(insns_before), 160)

    log("```asm")
    log("; Region around 0x1B8B MOVZ (context window)")
    for i in range(range_start, range_end):
        insn = insns_before[i]
        log(format_instruction(insn, annotations))
    log("```")

    # 1c. Analyze the data flow
    log()
    log("## 1.3 Data Flow Analysis")
    log()

    # Find what happens between prologue and MOVZ
    if movz_idx:
        pre_movz = insns_before[:movz_idx]

        # Find all store instructions (packet field writes)
        stores = find_str_stp_sequences(pre_movz)
        if stores:
            log(f"Found {len(stores)} store instructions before 0x1B8B MOVZ:")
            log()
            log("| Address | Instruction | Size | Type |")
            log("|---------|-------------|------|------|")
            for s in stores[-30:]:  # Last 30 stores before MOVZ
                log(f"| 0x{s['address']:08X} | `{s['mnemonic']} {s['op_str']}` | {s['size']} | {s['type']} |")

        # Find CMP/branch patterns
        cmp_patterns = find_cmp_branch_patterns(pre_movz)
        if cmp_patterns:
            log()
            log(f"Found {len(cmp_patterns)} comparison/branch patterns:")
            log()
            for p in cmp_patterns[-20:]:
                log(f"  - 0x{p['cmp_addr']:08X}: `{p['cmp_op']}` -> "
                    f"`{p['branch_op']}` (target: 0x{p['branch_target']:X})" if p['branch_target'] else
                    f"  - 0x{p['cmp_addr']:08X}: `{p['cmp_op']}` -> `{p['branch_op']}`")

    # 1d. MOVZ/MOVK value construction
    log()
    log("## 1.4 Immediate Value Construction")
    log()

    important_values = []
    for seq in movz_seqs:
        v = seq['value']
        if v >= 0x100 or v == 0x1B8B:
            important_values.append(seq)

    if important_values:
        log("Significant values built with MOVZ/MOVK:")
        log()
        log("| Address | Register | Value (hex) | Value (dec) | Notes |")
        log("|---------|----------|-------------|-------------|-------|")
        for seq in important_values:
            notes = ""
            v = seq['value']
            if v == 0x1B8B:
                notes = "OPCODE"
            elif 0x0C00 <= v <= 0x0FFF:
                notes = f"possible opcode?"
            elif v == ADDR_1B8B_TARGET_FN:
                notes = "target function"
            elif v == ADDR_GOSOCKET_SEND:
                notes = "GoSocket::sendData"
            log(f"| 0x{seq['address']:08X} | {seq['register']} | 0x{v:X} | {v} | {notes} |")

    # 1e. String references
    log()
    log("## 1.5 String References")
    log()
    if adrp_pairs:
        found_strings = [p for p in adrp_pairs if p['string']]
        if found_strings:
            log("Strings referenced in the function:")
            log()
            for p in found_strings:
                log(f"  - 0x{p['address']:08X}: `\"{p['string']}\"` (at 0x{p['full_addr']:X})")
        else:
            log("No ASCII strings found in ADRP+ADD pairs (data may be in non-string format)")

        no_string = [p for p in adrp_pairs if not p['string']]
        if no_string:
            log()
            log(f"  {len(no_string)} ADRP+ADD pairs reference non-string data addresses")
            for p in no_string[:15]:
                # Read raw bytes to see what's there
                raw = read_bytes_at_vaddr(p['full_addr'], 32)
                hex_preview = ""
                if raw:
                    hex_preview = " ".join(f"{b:02x}" for b in raw[:16])
                log(f"    0x{p['address']:08X} -> 0x{p['full_addr']:X}: [{hex_preview}]")
    else:
        log("No ADRP+ADD pairs found")

    return insns_before, calls, movz_seqs


def analyze_target_function():
    """Analyze the function at 0x5C851B0 called with 0x1B8B."""
    log("\n" + "=" * 80)
    log("# 2. FUNCTION 0x5C851B0 ANALYSIS (Called with 0x1B8B)")
    log("=" * 80)
    log()
    log(f"Disassembling {INSTR_FN} instructions at 0x{ADDR_1B8B_TARGET_FN:08X}")
    log()

    insns = disassemble_at(ADDR_1B8B_TARGET_FN, INSTR_FN)
    if not insns:
        log("ERROR: Could not disassemble at target address")
        return []

    log(f"Successfully disassembled {len(insns)} instructions")

    # Build annotations
    annotations = {
        ADDR_1B8B_TARGET_FN: "<<< FUNCTION ENTRY >>>"
    }

    # Find calls
    calls = find_bl_calls(insns)
    call_targets = defaultdict(int)
    for call in calls:
        tgt = call['target']
        call_targets[tgt] += 1
        note = f"CALL -> 0x{tgt:X}"
        if tgt == ADDR_GOSOCKET_SEND:
            note = "<<< CALL GoSocket::sendData >>>"
        annotations[call['address']] = note

    # Find MOVZ/MOVK
    movz_seqs = find_movz_movk_sequences(insns)
    for seq in movz_seqs:
        v = seq['value']
        if v >= 0x100:
            annotations[seq['address']] = f"builds 0x{v:X} ({v})"

    # Find ADRP pairs
    adrp_pairs = find_adrp_add_pairs(insns)
    for pair in adrp_pairs:
        if pair['string']:
            annotations[pair['address']] = f"-> \"{pair['string']}\""

    # Find stores
    stores = find_str_stp_sequences(insns)

    # Find returns
    ret_addrs = []
    for insn in insns:
        if insn.mnemonic.lower() == 'ret':
            ret_addrs.append(insn.address)
            annotations[insn.address] = "RETURN"

    # Print first 200 instructions with annotations
    log("## 2.1 Disassembly Listing")
    log()
    log("```asm")
    log(f"; Function at 0x{ADDR_1B8B_TARGET_FN:X}")
    for insn in insns[:200]:
        log(format_instruction(insn, annotations))
    log("```")

    # Summarize call targets
    log()
    log("## 2.2 Call Graph")
    log()
    if call_targets:
        log("Functions called from 0x5C851B0:")
        log()
        log("| Target | Count | Notes |")
        log("|--------|-------|-------|")
        for tgt, cnt in sorted(call_targets.items()):
            notes = ""
            if tgt == ADDR_GOSOCKET_SEND:
                notes = "GoSocket::sendData"
            log(f"| 0x{tgt:X} | {cnt} | {notes} |")

    # Determine function type
    log()
    log("## 2.3 Function Classification")
    log()

    has_gosocket_call = ADDR_GOSOCKET_SEND in call_targets
    num_calls = len(calls)
    num_stores = len(stores)

    if has_gosocket_call:
        log(f"- **Calls GoSocket::sendData directly** - this is a send wrapper or sendMsg")
        log(f"- Total calls: {num_calls}")
        log(f"- Total stores: {num_stores}")
    else:
        log(f"- Does NOT call GoSocket::sendData directly")
        log(f"- Total calls: {num_calls} (one of these likely leads to sendData)")
        log(f"- Total stores: {num_stores}")

    if ret_addrs:
        fn_size = ret_addrs[0] - ADDR_1B8B_TARGET_FN
        log(f"- First RET at 0x{ret_addrs[0]:X} (function size ~{fn_size} bytes, ~{fn_size//4} insns)")

    # String references
    str_refs = [p for p in adrp_pairs if p['string']]
    if str_refs:
        log()
        log("## 2.4 String References")
        log()
        for p in str_refs:
            log(f"  - `\"{p['string']}\"` (0x{p['full_addr']:X})")

    return insns


def analyze_0ce8_march():
    """Deep analysis of 0x0CE8 START_MARCH handler."""
    log("\n" + "=" * 80)
    log("# 3. OPCODE 0x0CE8 START_MARCH DEEP ANALYSIS")
    log("=" * 80)
    log()
    log("Known MOVZ references:")
    for addr in ADDR_0CE8_REFS:
        log(f"  - 0x{addr:08X}")
    log()

    all_march_data = {}

    for ref_idx, ref_addr in enumerate(ADDR_0CE8_REFS):
        log(f"### 3.{ref_idx + 1} Analysis of reference at 0x{ref_addr:08X}")
        log()

        # Find function prologue
        prologue_addr, all_insns = find_function_prologue(ref_addr, max_search_bytes=INSTR_BEFORE * 4)

        if prologue_addr:
            log(f"Function entry: **0x{prologue_addr:08X}** "
                f"({ref_addr - prologue_addr} bytes before MOVZ)")
        else:
            prologue_addr = ref_addr - 200 * 4
            log(f"No prologue found, analyzing from 0x{prologue_addr:08X}")

        # Disassemble the region
        insns = disassemble_at(prologue_addr, INSTR_BEFORE + INSTR_AFTER)
        if not insns:
            log("ERROR: Could not disassemble")
            continue

        # Build annotations
        annotations = {}
        if prologue_addr:
            annotations[prologue_addr] = "FUNCTION ENTRY"
        annotations[ref_addr] = "<<< 0x0CE8 MOVZ HERE >>>"

        # Find all MOVZ/MOVK sequences
        movz_seqs = find_movz_movk_sequences(insns)
        opcode_values = []
        for seq in movz_seqs:
            v = seq['value']
            annotations[seq['address']] = f"builds 0x{v:X}"
            if 0x0C00 <= v <= 0x0FFF:
                opcode_values.append(seq)

        # Find BL calls
        calls = find_bl_calls(insns)
        for call in calls:
            tgt = call['target']
            note = f"CALL -> 0x{tgt:X}"
            if tgt == ADDR_1B8B_TARGET_FN:
                note = f"CALL -> sendMsg wrapper (0x{tgt:X})"
            elif tgt == ADDR_GOSOCKET_SEND:
                note = "CALL -> GoSocket::sendData"
            annotations[call['address']] = note

        # Find stores
        stores = find_str_stp_sequences(insns)

        # Find CMP/branch patterns (for 0x0CE8 vs 0x0D08)
        cmp_patterns = find_cmp_branch_patterns(insns)

        # Find ADRP pairs
        adrp_pairs = find_adrp_add_pairs(insns)
        for pair in adrp_pairs:
            if pair['string']:
                annotations[pair['address']] = f"-> \"{pair['string']}\""

        # Print annotated disassembly (focused around MOVZ)
        movz_idx = None
        for i, insn in enumerate(insns):
            if insn.address == ref_addr:
                movz_idx = i
                break

        if movz_idx is not None:
            range_start = max(0, movz_idx - 60)
            range_end = min(len(insns), movz_idx + 60)
        else:
            range_start = 0
            range_end = min(len(insns), 120)

        log()
        log("```asm")
        log(f"; 0x0CE8 handler context at ref 0x{ref_addr:X}")
        for i in range(range_start, range_end):
            insn = insns[i]
            log(format_instruction(insn, annotations))
        log("```")

        # Report opcode values found
        if opcode_values:
            log()
            log(f"**Opcode values in this function:**")
            for ov in opcode_values:
                log(f"  - 0x{ov['value']:X} at 0x{ov['address']:X} in {ov['register']}")

        # Report CMP/branch patterns (key for 0x0CE8 vs 0x0D08)
        if cmp_patterns:
            log()
            log("**Conditional branches (may determine 0x0CE8 vs 0x0D08):**")
            for p in cmp_patterns:
                tgt_str = f"0x{p['branch_target']:X}" if p['branch_target'] else "?"
                log(f"  - `{p['cmp_op']}` at 0x{p['cmp_addr']:X} -> "
                    f"`{p['branch_op']}` -> {tgt_str}")

        # Report string references
        str_refs = [p for p in adrp_pairs if p['string']]
        if str_refs:
            log()
            log("**String references:**")
            for p in str_refs:
                log(f"  - `\"{p['string']}\"` at 0x{p['full_addr']:X}")

        # Store data for cross-reference
        all_march_data[ref_addr] = {
            'prologue': prologue_addr,
            'stores': stores,
            'calls': calls,
            'movz_seqs': movz_seqs,
            'cmp_patterns': cmp_patterns,
            'opcode_values': opcode_values,
        }

        log()

    # Cross-reference: look for 0x0D08 in any of these functions
    log("## 3.4 Cross-reference: 0x0CE8 vs 0x0D08 Selection")
    log()

    found_0d08 = False
    for ref_addr, data in all_march_data.items():
        for seq in data['movz_seqs']:
            if seq['value'] == 0x0D08:
                log(f"**FOUND 0x0D08 at 0x{seq['address']:X}** (in function containing 0x{ref_addr:X})")
                found_0d08 = True

    if not found_0d08:
        log("0x0D08 not found in the immediate vicinity of 0x0CE8 references.")
        log("The conditional selection may happen in a caller function or through")
        log("an indirect mechanism (e.g., vtable or function pointer).")

    # Analyze packet structure from stores
    log()
    log("## 3.5 Packet Field Analysis (Store Instructions)")
    log()

    for ref_addr, data in all_march_data.items():
        stores = data['stores']
        if stores:
            log(f"**Stores near 0x{ref_addr:X}:**")
            log()
            log("| Address | Type | Size | Instruction |")
            log("|---------|------|------|-------------|")
            for s in stores[-40:]:
                log(f"| 0x{s['address']:08X} | {s['type']} | {s['size']}B | "
                    f"`{s['mnemonic']} {s['op_str']}` |")
            log()

    return all_march_data


def analyze_0ce7_cancel():
    """Analysis of 0x0CE7 CANCEL_MARCH handler."""
    log("\n" + "=" * 80)
    log("# 4. OPCODE 0x0CE7 CANCEL_MARCH ANALYSIS")
    log("=" * 80)
    log()
    log(f"Known: MOVZ at 0x{ADDR_0CE7_MOVZ:08X}")
    log()

    # Find prologue
    prologue_addr, all_insns = find_function_prologue(ADDR_0CE7_MOVZ, max_search_bytes=INSTR_BEFORE * 4)

    if prologue_addr:
        log(f"Function entry: **0x{prologue_addr:08X}** "
            f"({ADDR_0CE7_MOVZ - prologue_addr} bytes before MOVZ)")
    else:
        prologue_addr = ADDR_0CE7_MOVZ - 100 * 4

    # Disassemble
    insns = disassemble_at(prologue_addr, 300)
    if not insns:
        log("ERROR: Could not disassemble")
        return

    annotations = {}
    annotations[ADDR_0CE7_MOVZ] = "<<< 0x0CE7 CANCEL_MARCH MOVZ >>>"
    if prologue_addr:
        annotations[prologue_addr] = "FUNCTION ENTRY"

    calls = find_bl_calls(insns)
    for call in calls:
        tgt = call['target']
        note = f"CALL -> 0x{tgt:X}"
        if tgt == ADDR_1B8B_TARGET_FN:
            note = f"CALL -> sendMsg wrapper"
        elif tgt == ADDR_GOSOCKET_SEND:
            note = "CALL -> GoSocket::sendData"
        annotations[call['address']] = note

    movz_seqs = find_movz_movk_sequences(insns)
    for seq in movz_seqs:
        v = seq['value']
        if v >= 0x100:
            annotations[seq['address']] = f"builds 0x{v:X}"

    adrp_pairs = find_adrp_add_pairs(insns)
    for pair in adrp_pairs:
        if pair['string']:
            annotations[pair['address']] = f"-> \"{pair['string']}\""

    stores = find_str_stp_sequences(insns)

    # Print focused disassembly
    movz_idx = None
    for i, insn in enumerate(insns):
        if insn.address == ADDR_0CE7_MOVZ:
            movz_idx = i
            break

    if movz_idx is not None:
        range_start = max(0, movz_idx - 40)
        range_end = min(len(insns), movz_idx + 40)
    else:
        range_start = 0
        range_end = min(len(insns), 80)

    log("```asm")
    log(f"; 0x0CE7 CANCEL_MARCH handler")
    for i in range(range_start, range_end):
        insn = insns[i]
        log(format_instruction(insn, annotations))
    log("```")

    # Stores analysis
    if stores:
        log()
        log("## 4.1 Cancellation Packet Fields")
        log()
        log("| Address | Type | Size | Instruction |")
        log("|---------|------|------|-------------|")
        for s in stores[-20:]:
            log(f"| 0x{s['address']:08X} | {s['type']} | {s['size']}B | "
                f"`{s['mnemonic']} {s['op_str']}` |")

    # String references
    str_refs = [p for p in adrp_pairs if p['string']]
    if str_refs:
        log()
        log("## 4.2 String References")
        log()
        for p in str_refs:
            log(f"  - `\"{p['string']}\"` at 0x{p['full_addr']:X}")

    # Call targets
    call_targets = defaultdict(int)
    for call in calls:
        call_targets[call['target']] += 1

    if call_targets:
        log()
        log("## 4.3 Functions Called")
        log()
        for tgt, cnt in sorted(call_targets.items()):
            notes = ""
            if tgt == ADDR_1B8B_TARGET_FN:
                notes = " (sendMsg wrapper)"
            elif tgt == ADDR_GOSOCKET_SEND:
                notes = " (GoSocket::sendData)"
            log(f"  - 0x{tgt:X} x{cnt}{notes}")


def analyze_gosocket_senddata():
    """Quick analysis of GoSocket::sendData."""
    log("\n" + "=" * 80)
    log("# 5. GoSocket::sendData (0x4F95CA8) ANALYSIS")
    log("=" * 80)
    log()

    insns = disassemble_at(ADDR_GOSOCKET_SEND, 200)
    if not insns:
        log("ERROR: Could not disassemble GoSocket::sendData")
        return

    annotations = {ADDR_GOSOCKET_SEND: "<<< GoSocket::sendData ENTRY >>>"}

    calls = find_bl_calls(insns)
    for call in calls:
        annotations[call['address']] = f"CALL -> 0x{call['target']:X}"

    adrp_pairs = find_adrp_add_pairs(insns)
    for pair in adrp_pairs:
        if pair['string']:
            annotations[pair['address']] = f"-> \"{pair['string']}\""

    movz_seqs = find_movz_movk_sequences(insns)
    for seq in movz_seqs:
        if seq['value'] >= 0x100:
            annotations[seq['address']] = f"builds 0x{seq['value']:X}"

    # Find returns
    for insn in insns:
        if insn.mnemonic.lower() == 'ret':
            annotations[insn.address] = "RETURN"

    log("```asm")
    log("; GoSocket::sendData")
    for insn in insns[:150]:
        log(format_instruction(insn, annotations))
    log("```")

    str_refs = [p for p in adrp_pairs if p['string']]
    if str_refs:
        log()
        log("## 5.1 Strings in GoSocket::sendData")
        log()
        for p in str_refs:
            log(f"  - `\"{p['string']}\"` at 0x{p['full_addr']:X}")

    call_targets = defaultdict(int)
    for call in calls:
        call_targets[call['target']] += 1

    if call_targets:
        log()
        log("## 5.2 Call Graph")
        log()
        for tgt, cnt in sorted(call_targets.items()):
            log(f"  - 0x{tgt:X} x{cnt}")


def scan_nearby_opcodes():
    """Scan for other opcode values near the known march handler locations."""
    log("\n" + "=" * 80)
    log("# 6. NEARBY OPCODE SCAN")
    log("=" * 80)
    log()
    log("Scanning for game opcode values (0x0C00-0x0FFF range) near known handlers...")
    log()

    scan_regions = [
        ("0x0CE8 ref1", ADDR_0CE8_REFS[0] - 2000*4, 4000),
        ("0x0CE8 ref2", ADDR_0CE8_REFS[1] - 500*4, 1000),
        ("0x0CE8 ref3", ADDR_0CE8_REFS[2] - 500*4, 1000),
        ("0x0CE7 cancel", ADDR_0CE7_MOVZ - 500*4, 1000),
        ("0x1B8B handler", ADDR_1B8B_MOVZ - 500*4, 1000),
    ]

    all_opcodes = defaultdict(list)

    for label, start, count in scan_regions:
        insns = disassemble_at(start, count)
        if not insns:
            continue
        movz_seqs = find_movz_movk_sequences(insns)
        for seq in movz_seqs:
            v = seq['value']
            if 0x0C00 <= v <= 0x0FFF or v == 0x1B8B or v == 0x0D08:
                all_opcodes[v].append({
                    'address': seq['address'],
                    'region': label,
                    'register': seq['register'],
                })

    if all_opcodes:
        log("| Opcode | Value | Locations |")
        log("|--------|-------|-----------|")
        for opcode in sorted(all_opcodes.keys()):
            locs = all_opcodes[opcode]
            loc_strs = [f"0x{l['address']:X} ({l['region']})" for l in locs]

            # Try to name the opcode
            opcode_names = {
                0x0CE7: "CANCEL_MARCH",
                0x0CE8: "START_MARCH",
                0x0CE9: "?",
                0x0CEA: "?",
                0x0CEB: "ENABLE_VIEW",
                0x0CEC: "?",
                0x0CED: "TRAIN",
                0x0CEE: "RESEARCH",
                0x0CEF: "BUILD",
                0x0D08: "ALTERNATE_MARCH",
                0x1B8B: "UNKNOWN_1B8B",
            }
            name = opcode_names.get(opcode, "")

            log(f"| 0x{opcode:04X} | {name} | {', '.join(loc_strs)} |")
    else:
        log("No game opcodes found in scan regions")


def deep_trace_0ce8_first_ref():
    """Extra-deep trace of the first 0x0CE8 reference to map full packet layout."""
    log("\n" + "=" * 80)
    log("# 7. DEEP PACKET LAYOUT TRACE: 0x0CE8 (First Reference)")
    log("=" * 80)
    log()

    ref_addr = ADDR_0CE8_REFS[0]  # 0x555FE3C

    # Go much further back to find the full function
    prologue_addr, _ = find_function_prologue(ref_addr, max_search_bytes=8000)

    if prologue_addr:
        log(f"Function starts at: 0x{prologue_addr:08X}")
        fn_size_estimate = ref_addr - prologue_addr + INSTR_AFTER * 4
        insn_count = fn_size_estimate // 4 + 100
    else:
        prologue_addr = ref_addr - 500 * 4
        insn_count = 700

    insns = disassemble_at(prologue_addr, min(insn_count, 2000))
    if not insns:
        log("ERROR: Could not disassemble")
        return

    log(f"Disassembled {len(insns)} instructions from 0x{prologue_addr:X}")
    log()

    # Focused analysis: Find all stores relative to a buffer pointer
    # In packet construction, you typically see:
    # 1. A buffer pointer in some register (e.g., X0, X19, X20)
    # 2. STR/STRB/STRH to offsets from that register

    # Find all stores with their offsets
    buffer_stores = defaultdict(list)  # base_reg -> [(offset, size, type, addr)]

    for insn in insns:
        mnem = insn.mnemonic.lower()
        if mnem in ('str', 'strb', 'strh', 'stur', 'sturb', 'sturh', 'stp'):
            info = analyze_instruction_details(insn)
            for mem in info['mem_ops']:
                if mem['base']:
                    base = mem['base']
                    disp = mem['disp']

                    if mnem in ('strb', 'sturb'):
                        size, typ = 1, 'u8'
                    elif mnem in ('strh', 'sturh'):
                        size, typ = 2, 'u16'
                    elif mnem in ('str', 'stur'):
                        first_reg = insn.op_str.split(',')[0].strip().lower()
                        if first_reg.startswith('w'):
                            size, typ = 4, 'u32'
                        elif first_reg.startswith('x'):
                            size, typ = 8, 'u64'
                        else:
                            size, typ = 4, 'unknown'
                    elif mnem == 'stp':
                        first_reg = insn.op_str.split(',')[0].strip().lower()
                        if first_reg.startswith('w'):
                            size, typ = 8, '2xu32'
                        else:
                            size, typ = 16, '2xu64'
                    else:
                        size, typ = 0, '?'

                    # Only care about non-SP stores (SP stores are local vars)
                    if base != 'sp':
                        buffer_stores[base].append((disp, size, typ, insn.address, insn.op_str))

    # Report the most-used buffer base registers
    log("## 7.1 Buffer Store Analysis")
    log()
    log("Stores grouped by base register (excluding SP):")
    log()

    for base_reg in sorted(buffer_stores.keys(), key=lambda r: -len(buffer_stores[r])):
        stores = buffer_stores[base_reg]
        if len(stores) < 3:
            continue

        log(f"### Base register: `{base_reg}` ({len(stores)} stores)")
        log()
        log("| Offset | Type | Size | Address | Instruction |")
        log("|--------|------|------|---------|-------------|")
        for disp, size, typ, addr, op_str in sorted(stores, key=lambda x: x[0]):
            log(f"| +0x{disp:X} ({disp}) | {typ} | {size}B | 0x{addr:08X} | `{op_str}` |")
        log()

    # Look for coordinate-related patterns
    log("## 7.2 Potential Coordinate Fields")
    log()
    log("Looking for paired stores (x, y coordinates typically stored adjacently)...")
    log()

    for base_reg, stores in buffer_stores.items():
        if len(stores) < 2:
            continue
        sorted_stores = sorted(stores, key=lambda x: x[0])
        for i in range(len(sorted_stores) - 1):
            disp1, size1, typ1, addr1, _ = sorted_stores[i]
            disp2, size2, typ2, addr2, _ = sorted_stores[i + 1]
            # Adjacent same-sized stores could be coordinate pairs
            if size1 == size2 and disp2 - disp1 == size1 and size1 >= 4:
                log(f"  Possible (x,y) pair in `{base_reg}`: "
                    f"offset +{disp1} and +{disp2} ({typ1}, {size1}B each)")


def compare_known_senders():
    """Compare the send patterns of known working opcodes vs march."""
    log("\n" + "=" * 80)
    log("# 8. COMPARISON: KNOWN WORKING OPCODES vs MARCH")
    log("=" * 80)
    log()

    # Search for known working opcodes in the broader binary
    known_opcodes = {
        0x0CED: "TRAIN",
        0x0CEF: "BUILD",
        0x0CEE: "RESEARCH",
        0x0CEB: "ENABLE_VIEW",
    }

    # We need to find these opcodes' MOVZ locations
    # Let's scan the executable segments
    log("Scanning for known opcode MOVZ instructions in executable segments...")
    log()

    for seg_vaddr, seg_offset, seg_filesz, seg_memsz, seg_flags in elf_segments:
        if not (seg_flags & 1):  # Not executable
            continue
        if seg_filesz < 1000:
            continue

        log(f"Scanning segment at 0x{seg_vaddr:X} (size: 0x{seg_filesz:X}, "
            f"flags: {'X' if seg_flags & 1 else ''}{'W' if seg_flags & 2 else ''}{'R' if seg_flags & 4 else ''})")

        # Read the segment
        seg_data = binary_data[seg_offset:seg_offset + seg_filesz]

        for opcode, name in known_opcodes.items():
            # ARM64 MOVZ encoding for W register:
            # MOVZ Wd, #imm16 -> 0x52800000 | (imm16 << 5) | Rd
            # We search for the immediate value pattern

            # For MOVZ Wn, #opcode (no shift):
            # Encoding: 0101_0010_100x_xxxx_xxxx_xxxx_xxxd_dddd
            # Where x = imm16 bits, d = dest register
            base = 0x52800000
            imm_shifted = (opcode & 0xFFFF) << 5

            # Search for any destination register (0-30)
            found_addrs = []
            for rd in range(31):
                target_word = base | imm_shifted | rd
                target_bytes = struct.pack('<I', target_word)

                pos = 0
                while pos < len(seg_data) - 4:
                    idx = seg_data.find(target_bytes, pos)
                    if idx < 0:
                        break
                    # Must be 4-byte aligned
                    if idx % 4 == 0:
                        vaddr = seg_vaddr + idx
                        found_addrs.append((vaddr, rd))
                    pos = idx + 4

            if found_addrs:
                log(f"  0x{opcode:04X} ({name}): found {len(found_addrs)} MOVZ instruction(s)")
                for vaddr, rd in found_addrs[:5]:
                    log(f"    - 0x{vaddr:08X} (W{rd})")

                # Do a quick analysis of the first reference
                if found_addrs:
                    first_addr = found_addrs[0][0]
                    quick_insns = disassemble_at(first_addr - 20*4, 60)
                    if quick_insns:
                        quick_calls = find_bl_calls(quick_insns)
                        call_targets = set()
                        for c in quick_calls:
                            call_targets.add(c['target'])

                        # Check if it calls the same send wrapper
                        if ADDR_1B8B_TARGET_FN in call_targets:
                            log(f"    >> Uses same send wrapper as 0x1B8B (0x{ADDR_1B8B_TARGET_FN:X})")

                        if call_targets:
                            log(f"    >> Calls: {', '.join(f'0x{t:X}' for t in sorted(call_targets))}")
            else:
                log(f"  0x{opcode:04X} ({name}): not found via MOVZ scan")

        break  # Only scan first executable segment
    log()


def scan_gosocket_callers():
    """Scan for BL instructions that call GoSocket::sendData."""
    log("\n" + "=" * 80)
    log("# 8c. GoSocket::sendData CALLER SCAN")
    log("=" * 80)
    log()
    log(f"Scanning for BL instructions targeting 0x{ADDR_GOSOCKET_SEND:X}...")
    log()

    # BL encoding: 0x94000000 | (offset >> 2) where offset = target - pc
    # offset is a signed 26-bit value

    exec_seg = None
    for seg_vaddr, seg_offset, seg_filesz, seg_memsz, seg_flags in elf_segments:
        if (seg_flags & 1) and seg_filesz > 1000000:
            exec_seg = (seg_vaddr, seg_offset, seg_filesz)
            break

    if not exec_seg:
        log("No executable segment found")
        return

    seg_vaddr, seg_offset, seg_filesz = exec_seg
    seg_data = binary_data[seg_offset:seg_offset + seg_filesz]

    callers = []
    # Scan every 4-byte aligned word in the executable segment
    for i in range(0, seg_filesz - 4, 4):
        word = struct.unpack_from('<I', seg_data, i)[0]
        # Check if this is a BL instruction (top 6 bits = 100101)
        if (word >> 26) == 0x25:  # BL
            # Extract signed 26-bit offset
            imm26 = word & 0x3FFFFFF
            if imm26 & 0x2000000:  # Sign extend
                imm26 -= 0x4000000
            pc = seg_vaddr + i
            target = pc + (imm26 << 2)
            if target == ADDR_GOSOCKET_SEND:
                callers.append(pc)

    log(f"Found {len(callers)} call(s) to GoSocket::sendData")
    log()

    if callers:
        log("| Caller Address | Context (function prologue search) |")
        log("|---------------|-----------------------------------|")

        for caller_addr in callers[:30]:
            # Find function prologue
            prologue, _ = find_function_prologue(caller_addr, max_search_bytes=2000)
            if prologue:
                log(f"| 0x{caller_addr:08X} | Function at 0x{prologue:08X} (offset -{caller_addr - prologue}) |")
            else:
                log(f"| 0x{caller_addr:08X} | (prologue not found) |")

        # For each caller, show some context
        log()
        log("### Detailed Context for First 10 Callers")
        log()
        for idx, caller_addr in enumerate(callers[:10]):
            log(f"#### Caller #{idx+1}: 0x{caller_addr:08X}")
            log()
            ctx_insns = disassemble_at(caller_addr - 15*4, 35)
            if not ctx_insns:
                continue

            annotations = {caller_addr: "<<< BL GoSocket::sendData >>>"}

            # Find MOVZ/MOVK in context
            movz_seqs = find_movz_movk_sequences(ctx_insns)
            for seq in movz_seqs:
                v = seq['value']
                if v >= 0x20:
                    note = f"value 0x{v:X} ({v})"
                    if 0x0C00 <= v <= 0x1FFF:
                        note += " **POSSIBLE OPCODE?**"
                    annotations[seq['address']] = note

            # Find strings
            adrp_pairs = find_adrp_add_pairs(ctx_insns)
            for pair in adrp_pairs:
                if pair['string']:
                    annotations[pair['address']] = f"-> \"{pair['string']}\""

            # Find other calls
            calls = find_bl_calls(ctx_insns)
            for call in calls:
                if call['address'] != caller_addr:
                    annotations[call['address']] = f"CALL -> 0x{call['target']:X}"

            log("```asm")
            for insn in ctx_insns:
                log(format_instruction(insn, annotations))
            log("```")
            log()

    return callers


def scan_for_game_opcodes_broad():
    """Broader scan: search for game opcodes via multiple instruction encodings."""
    log("\n" + "=" * 80)
    log("# 8b. BROAD OPCODE SCAN (Multiple Encodings)")
    log("=" * 80)
    log()
    log("The previous MOVZ scan found no game opcodes. This scan tries additional")
    log("ARM64 encodings: MOVZ Xn (64-bit), MOV (ORR alias), and two-byte LE patterns.")
    log()

    # Read the executable segment
    exec_seg = None
    for seg_vaddr, seg_offset, seg_filesz, seg_memsz, seg_flags in elf_segments:
        if (seg_flags & 1) and seg_filesz > 1000000:
            exec_seg = (seg_vaddr, seg_offset, seg_filesz)
            break

    if not exec_seg:
        log("No executable segment found")
        return

    seg_vaddr, seg_offset, seg_filesz = exec_seg
    seg_data = binary_data[seg_offset:seg_offset + seg_filesz]

    opcodes_to_find = {
        0x0CE7: "CANCEL_MARCH",
        0x0CE8: "START_MARCH",
        0x0CEB: "ENABLE_VIEW",
        0x0CED: "TRAIN",
        0x0CEE: "RESEARCH",
        0x0CEF: "BUILD",
        0x0D08: "ALT_MARCH",
        0x1B8B: "UNKNOWN_1B8B",
    }

    for opcode, name in sorted(opcodes_to_find.items()):
        all_hits = []

        # Method 1: MOVZ Wn, #imm16 (32-bit dest, no shift)
        # Encoding: 0101_0010_100|imm16|Rd
        for rd in range(31):
            target = 0x52800000 | ((opcode & 0xFFFF) << 5) | rd
            target_bytes = struct.pack('<I', target)
            pos = 0
            while pos < len(seg_data) - 4:
                idx = seg_data.find(target_bytes, pos)
                if idx < 0: break
                if idx % 4 == 0:
                    all_hits.append((seg_vaddr + idx, f"MOVZ W{rd}"))
                pos = idx + 4

        # Method 2: MOVZ Xn, #imm16 (64-bit dest, no shift)
        # Encoding: 1101_0010_100|imm16|Rd
        for rd in range(31):
            target = 0xD2800000 | ((opcode & 0xFFFF) << 5) | rd
            target_bytes = struct.pack('<I', target)
            pos = 0
            while pos < len(seg_data) - 4:
                idx = seg_data.find(target_bytes, pos)
                if idx < 0: break
                if idx % 4 == 0:
                    all_hits.append((seg_vaddr + idx, f"MOVZ X{rd}"))
                pos = idx + 4

        # Method 3: MOV Wn, #imm (ORR alias) - check if opcode is encodable
        # ARM64 MOV (wide immediate): depends on bitmask logic, skip for now

        # Method 4: Raw 2-byte LE search (for values stored in memory/data)
        # This finds the opcode as a 16-bit little-endian value in .rodata or tables
        le_bytes = struct.pack('<H', opcode)
        data_count = 0
        pos = 0
        while pos < len(seg_data) - 2 and data_count < 5:
            idx = seg_data.find(le_bytes, pos)
            if idx < 0: break
            # Skip if it's part of an instruction we already found
            vaddr = seg_vaddr + idx
            already_found = any(abs(vaddr - h[0]) < 4 for h in all_hits)
            if not already_found and idx % 2 == 0:
                # Check context: is this in a data region or instruction?
                # Disassemble to check
                data_count += 1
            pos = idx + 2

        if all_hits:
            log(f"### 0x{opcode:04X} ({name}): {len(all_hits)} hit(s)")
            log()
            for vaddr, enc_type in all_hits[:10]:
                # Get surrounding context
                ctx_insns = disassemble_at(vaddr - 8*4, 20)
                context_strs = []
                for ci in ctx_insns:
                    if abs(ci.address - vaddr) <= 20:
                        marker = " <<<" if ci.address == vaddr else ""
                        context_strs.append(
                            f"    0x{ci.address:08X}: {ci.mnemonic:8s} {ci.op_str}{marker}")

                # Check nearby strings
                nearby_adrp = find_adrp_add_pairs(ctx_insns)
                nearby_strings = [p['string'] for p in nearby_adrp if p['string']]

                log(f"  - 0x{vaddr:08X} ({enc_type})")
                if nearby_strings:
                    log(f"    Nearby strings: {', '.join(nearby_strings[:3])}")
                if context_strs:
                    log("    Context:")
                    for cs in context_strs:
                        log(cs)
                log()
        else:
            log(f"  0x{opcode:04X} ({name}): NOT FOUND in any encoding")
            log()


def write_summary():
    """Write final summary section."""
    log("\n" + "=" * 80)
    log("# 10. CRITICAL FINDINGS & CONCLUSIONS")
    log("=" * 80)
    log()

    log("## CRITICAL FINDING: FALSE POSITIVE IDENTIFICATION")
    log()
    log("**The previously identified addresses for game opcodes are FALSE POSITIVES.**")
    log("They reside in embedded third-party libraries, NOT in the game's protocol code:")
    log()
    log("| Address | Claimed Purpose | Actual Location | Evidence |")
    log("|---------|----------------|-----------------|----------|")
    log(f"| 0x{ADDR_1B8B_MOVZ:08X} | 0x1B8B game opcode | **OpenSSL** (ssl/ssl_lib.c) | String refs: ssl_lib.c, ssl_cache_cipherlist, 0123456789abcdef |")
    for addr in ADDR_0CE8_REFS:
        log(f"| 0x{addr:08X} | 0x0CE8 START_MARCH | **libcurl** HTTP auth | String refs: NTLM, Digest, Basic, Bearer, HTTP headers |")
    log(f"| 0x{ADDR_0CE7_MOVZ:08X} | 0x0CE7 CANCEL_MARCH | **OpenSSL** crypto (ml_dsa) | String refs: crypto/ml_dsa/ml_dsa_key.c, SHAKE-128 |")
    log()

    log("### Why these are false positives:")
    log()
    log("1. **0x1B8B at 0x58EA650**: Lives in OpenSSL's `ssl_lib.c` code. The value 0x1B8B")
    log("   is a line number constant used for OpenSSL error reporting, NOT a game opcode.")
    log("   The hex-encoding loop (using '0123456789abcdef') is OpenSSL's cipher suite")
    log("   hex-encoding, not game packet construction.")
    log()
    log("2. **0x0CE8 at 0x555FE3C/0x5566714/0x5566B68**: These are in libcurl's HTTP")
    log("   authentication code. The value 0x0CE8 is a structure field offset (3304 decimal)")
    log("   used to access HTTP proxy/connection authentication state. The CSEL with 0x0D08")
    log("   selects between proxy (offset 0x0D08=3336) and server (offset 0x0CE8=3304)")
    log("   authentication contexts.")
    log()
    log("3. **0x0CE7 at 0x5AFE404**: Lives in OpenSSL's ML-DSA (post-quantum crypto) code.")
    log("   The value 0x0CE7 is likely a field offset or loop bound in the ML-DSA key")
    log("   generation algorithm.")
    log()
    log("4. **0x5C851B0 (target function)**: This is a PLT (Procedure Linkage Table) stub,")
    log("   a GOT trampoline (`ADRP x16 + LDR x17 + BR x17`). It's a dynamic linker")
    log("   entry point, not a game function.")
    log()

    log("### GoSocket::sendData (0x4F95CA8)")
    log()
    log("This function IS a real game function. Its structure shows:")
    log("- Socket file descriptor loaded from object+8")
    log("- Calls `sendto` (0x5C6DB10) with flags=0")
    log("- Error handling checks errno for EAGAIN(0x0B) or ENOBUFS(0x73)")
    log("- Buffer management with 0x800 (2048) byte buffers")
    log("- Opcode header stored as 2-byte fields at offsets +8 and +0xA")
    log()

    log("## Implications for Opcode Search")
    log()
    log("The game opcodes (0x0CE8, 0x0CE7, 0x0CED, etc.) are likely NOT loaded via")
    log("simple MOVZ instructions. Possible alternatives:")
    log()
    log("1. **Loaded from a dispatch table** in .rodata (16-bit values in an array)")
    log("2. **Passed as function arguments** from Java/JNI layer")
    log("3. **Computed at runtime** (e.g., base + offset)")
    log("4. **Stored in class member fields** and loaded via LDR/LDRH")
    log("5. **Part of a protobuf-generated switch statement** with computed gotos")
    log()

    log("## Key Addresses (Verified)")
    log()
    log("| Address | Description | Status |")
    log("|---------|-------------|--------|")
    log(f"| 0x{ADDR_GOSOCKET_SEND:08X} | GoSocket::sendData | VERIFIED REAL |")
    log(f"| 0x{ADDR_1B8B_MOVZ:08X} | Was: 0x1B8B opcode | FALSE POSITIVE (OpenSSL) |")
    for addr in ADDR_0CE8_REFS:
        log(f"| 0x{addr:08X} | Was: 0x0CE8 march | FALSE POSITIVE (libcurl) |")
    log(f"| 0x{ADDR_0CE7_MOVZ:08X} | Was: 0x0CE7 cancel | FALSE POSITIVE (OpenSSL crypto) |")
    log(f"| 0x{ADDR_1B8B_TARGET_FN:08X} | Was: sendMsg wrapper | PLT trampoline stub |")
    log()

    log("## Recommended Next Steps")
    log()
    log("1. **Find the real opcode dispatch**: Search for GoSocket::sendData callers")
    log("   by scanning for BL instructions that target 0x4F95CA8")
    log("2. **Search for opcode tables**: Scan .rodata for arrays of 16-bit values")
    log("   containing known opcodes (0x0CED, 0x0CEF, 0x0CEE, etc.)")
    log("3. **Trace from JNI**: Find Java_*_sendMsg or similar JNI entry points")
    log("4. **Use Frida**: Hook GoSocket::sendData at runtime to capture actual")
    log("   opcode values being sent with march commands")
    log("5. **Search for the CMsgCodec**: The encryption codec likely sits between")
    log("   the opcode dispatch and GoSocket::sendData")


# ─── Main ────────────────────────────────────────────────────────────────

def main():
    start_time = time.time()

    log("# Deep Handler Analysis Report")
    log(f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"# Binary: {LIBGAME_PATH}")
    log()

    # Load binary
    load_binary()

    # Run all analyses
    print("\n[1/8] Analyzing 0x1B8B handler...")
    insns_1b8b, calls_1b8b, movz_1b8b = analyze_1b8b_handler()

    print("\n[2/8] Analyzing target function 0x5C851B0...")
    analyze_target_function()

    print("\n[3/8] Analyzing 0x0CE8 START_MARCH...")
    analyze_0ce8_march()

    print("\n[4/8] Analyzing 0x0CE7 CANCEL_MARCH...")
    analyze_0ce7_cancel()

    print("\n[5/8] Analyzing GoSocket::sendData...")
    analyze_gosocket_senddata()

    print("\n[6/8] Scanning for nearby opcodes...")
    scan_nearby_opcodes()

    print("\n[7/8] Deep packet layout trace for 0x0CE8...")
    deep_trace_0ce8_first_ref()

    print("\n[8/10] Comparing known working opcodes...")
    compare_known_senders()

    print("\n[9/10] Broad opcode scan (multiple encodings)...")
    scan_for_game_opcodes_broad()

    print("\n[10/10] Scanning for GoSocket::sendData callers...")
    scan_gosocket_callers()

    write_summary()

    elapsed = time.time() - start_time
    log(f"\n---\nAnalysis completed in {elapsed:.1f} seconds")

    # Write report
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"\n{'='*60}")
    print(f"Report written to: {OUTPUT_PATH}")
    print(f"Report size: {len(report_lines)} lines")
    print(f"Total time: {elapsed:.1f}s")


if __name__ == "__main__":
    main()

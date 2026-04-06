#!/usr/bin/env python3
"""
44_encrypted_opcodes_analysis.py - Comprehensive analysis of encrypted opcode range 0x0CE0-0x0CFF
=================================================================================================
Analyzes the NEW-style encrypted CMSG commands in libgame.so ARM64 ELF binary.
- Lists all opcodes in the range from known mappings
- Disassembles packData functions for each _NEW CMSG
- Deep-traces payload field layouts for critical commands
- Decrypts actual 0x0CE8 payloads from PCAPs
- Cross-references decrypted payloads with packData layout
"""
import struct
import sys
import os
import glob

sys.path.insert(0, r'D:\CascadeProjects\claude')
sys.path.insert(0, r'D:\CascadeProjects\analysis\findings')

from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
from cmsg_opcodes import CMSG_OPCODES

# ═══════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════
LIBGAME = r"D:\CascadeProjects\libgame.so"
PCAP_DIR = r"D:\CascadeProjects"
OUTPUT_MD = r"D:\CascadeProjects\analysis\findings\encrypted_opcodes_analysis.md"

# Encryption constants
TABLE = [0x58, 0xef, 0xd7, 0x14, 0xa2, 0x3b, 0x9c]
SERVER_KEY_U32 = 0x88587D29  # From PCAPdroid_27_Mar session

# Known names from protocol.py for range 0x0CE0-0x0CFF
KNOWN_NEW_OPCODES = {
    0x0CE4: 'CMSG_START_BUILDUP_NEW',
    0x0CE5: 'CMSG_JOIN_BUILDUP_NEW',
    0x0CE6: 'CMSG_START_DEFEND_NEW',
    0x0CE7: 'CMSG_BACK_DEFEND_NEW',
    0x0CE8: 'CMSG_START_MARCH_NEW',
    0x0CE9: 'CMSG_CANCEL_MARCH_NEW',
    0x0CEA: 'CMSG_MARCH_USE_ITEM_NEW',
    0x0CEB: 'CMSG_ENABLE_VIEW_NEW',
    0x0CEC: 'CMSG_DO_LEAGUE_DONATE_CRIT_NEW',
    0x0CED: 'CMSG_SOLDIER_NORMAL_PRODUCE_REQUEST_NEW',
    0x0CEE: 'CMSG_SCIENCE_NORMAL_STUDY_REQUEST_NEW',
    0x0CEF: 'CMSG_BUILDING_OPERAT_REQUEST_NEW',
    0x0CF0: 'CMSG_WORLD_BATTLE_NEW_SIGN_UP_REQUEST_NEW',
    0x0CF1: 'CMSG_MOVE_CASTLE_NEW',
    0x0CF2: 'CMSG_GET_OTHER_EXTRA_ATTRIBUTE_NEW',
    0x0CF3: 'CMSG_RAID_PLAYER_REQUEST_NEW',
    0x0CF4: 'CMSG_ARENA_MATCH_INFO_REQUEST_NEW',
    0x0CF5: 'CMSG_ARENA_CHANGE_MATCH_REQUEST_NEW',
    0x0CF6: 'CMSG_MAILBOX_MAIL_REQUEST_NEW',
    0x0CF7: 'CMSG_MAILBOX_MAIL_OPERATION_NEW',
    0x0CF8: 'CMSG_ITEM_SHOP_BUY_REQUEST_NEW',
    0x0CF9: 'CMSG_BUILDING_OPERAT_REQUEST_FIX_NEW',
    0x0CFB: 'CMSG_MARCH_USE_ITEM_ONEKEY',
}

# ═══════════════════════════════════════════════════════════════════
# Load binary
# ═══════════════════════════════════════════════════════════════════
print("Loading libgame.so...")
with open(LIBGAME, "rb") as f:
    data = f.read()
print(f"  Loaded {len(data):,} bytes")

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

# dynsym / dynstr offsets (known from previous analysis)
DYNSTR_OFF = 0x682A10
DYNSYM_OFF = 0x2F8
DYNSYM_SIZE = 0x682758

# ═══════════════════════════════════════════════════════════════════
# Output collector
# ═══════════════════════════════════════════════════════════════════
out_lines = []
def p(msg=""):
    out_lines.append(msg)
    try:
        print(msg)
    except:
        print(msg.encode('ascii', 'replace').decode())

# ═══════════════════════════════════════════════════════════════════
# TASK 1: List ALL opcodes in 0x0CE0-0x0CFF range
# ═══════════════════════════════════════════════════════════════════
p("=" * 100)
p("TASK 1: ALL OPCODES IN RANGE 0x0CE0 - 0x0CFF")
p("=" * 100)
p()

# Merge sources: CMSG_OPCODES dict + KNOWN_NEW_OPCODES + protocol.py
all_opcodes_in_range = {}
for opc, name in CMSG_OPCODES.items():
    if 0x0CE0 <= opc <= 0x0CFF:
        all_opcodes_in_range[opc] = name
for opc, name in KNOWN_NEW_OPCODES.items():
    if opc not in all_opcodes_in_range:
        all_opcodes_in_range[opc] = name

p(f"Found {len(all_opcodes_in_range)} opcodes in 0x0CE0-0x0CFF range:")
p()
p(f"  {'Opcode':<10s} {'Name':<55s} {'Source'}")
p(f"  {'------':<10s} {'----':<55s} {'------'}")
for opc in sorted(all_opcodes_in_range.keys()):
    name = all_opcodes_in_range[opc]
    src = "cmsg_opcodes.py" if opc in CMSG_OPCODES else "protocol.py"
    p(f"  0x{opc:04X}     {name:<55s} {src}")

# Show gaps
p()
p("Gaps (unidentified opcodes in range):")
for opc in range(0x0CE0, 0x0D00):
    if opc not in all_opcodes_in_range:
        p(f"  0x{opc:04X} - UNKNOWN")

# ═══════════════════════════════════════════════════════════════════
# Symbol lookup helpers
# ═══════════════════════════════════════════════════════════════════
def find_symbols(name_filter):
    """Find all dynsym entries matching a name filter."""
    results = []
    pos = DYNSYM_OFF
    while pos + 24 <= DYNSYM_OFF + DYNSYM_SIZE:
        st_name_off = struct.unpack('<I', data[pos:pos+4])[0]
        st_value = struct.unpack('<Q', data[pos+8:pos+16])[0]
        st_size = struct.unpack('<Q', data[pos+16:pos+24])[0]
        if st_name_off > 0 and st_name_off < 0x200000 and st_value > 0:
            try:
                name_end = data.index(b'\x00', DYNSTR_OFF + st_name_off)
                name = data[DYNSTR_OFF + st_name_off:name_end].decode('ascii', errors='replace')
                if name_filter(name):
                    results.append((name, st_value, st_size))
            except:
                pass
        pos += 24
    return results


def find_packdata(cmsg_class_name):
    """Find packData symbol for a given CMSG class name substring."""
    # Search for mangled name containing the class name and '8packData'
    results = find_symbols(lambda n: cmsg_class_name in n and '8packData' in n)
    return results[0] if results else None


def find_constructor(cmsg_class_name):
    """Find constructor for a CMSG class."""
    results = find_symbols(lambda n: cmsg_class_name in n and 'C1Ev' in n
                           and '8packData' not in n and '7getData' not in n)
    return results[0] if results else None


# ═══════════════════════════════════════════════════════════════════
# packData disassembly + field extraction
# ═══════════════════════════════════════════════════════════════════
def disassemble_func(addr, size):
    """Disassemble a function at given address."""
    max_bytes = min(size if size > 0 else 800, 3000)
    code = data[addr:addr + max_bytes]
    return list(md.disasm(code, addr))


def extract_payload_fields(addr, size):
    """
    Analyze packData function to extract payload format.
    CIStream pattern:
      x1 = CIStream: [0x00]=buf_ptr, [0x08]=capacity, [0x0A]=position, [0x0C]=error
      x0 = this (CMSG struct)
    """
    insns = disassemble_func(addr, size)
    if not insns:
        return [], insns

    payload_fields = []
    current_write_size = 0
    payload_offset = 0
    this_reg = 'x0'

    # Track vector/array patterns
    has_vector = False

    for i, insn in enumerate(insns):
        if insn.mnemonic == 'ret' and insn.address > addr + 20:
            break

        # Detect this pointer save
        if insn.mnemonic == 'mov' and insn.op_str.startswith('x19, x0'):
            this_reg = 'x19'
        if insn.mnemonic == 'mov' and insn.op_str.startswith('x20, x0'):
            this_reg = 'x20'

        # Detect write size from: add wN, wN, #SIZE (position update)
        if insn.mnemonic == 'add' and '#' in insn.op_str:
            parts = insn.op_str.split('#')
            try:
                add_val = int(parts[-1].rstrip(']').strip(), 0)
                if add_val in (1, 2, 4, 8):
                    for j in range(i+1, min(i+6, len(insns))):
                        if 'strh' in insns[j].mnemonic and '#0xa' in insns[j].op_str:
                            current_write_size = add_val
                            break
            except:
                pass

        # Detect ldp (load pair) for vector iteration
        if insn.mnemonic == 'ldp' and this_reg[1:] in insn.op_str:
            if '#0x20' in insn.op_str or '#0x18' in insn.op_str or '#0x10' in insn.op_str:
                has_vector = True

        # Detect data load from CMSG struct
        if insn.mnemonic in ('ldrh', 'ldrb', 'ldr', 'ldrsb', 'ldrsh', 'ldrsw'):
            for reg in [this_reg, 'x0', 'x19', 'x20']:
                if f'[{reg}]' in insn.op_str or f'[{reg},' in insn.op_str:
                    offset = 0
                    if '#' in insn.op_str:
                        try:
                            offset = int(insn.op_str.split('#')[-1].rstrip(']').rstrip('!').strip(), 0)
                        except:
                            pass

                    sizes = {'ldrb': 1, 'ldrsb': 1, 'ldrh': 2, 'ldrsh': 2, 'ldr': 4, 'ldrsw': 4}
                    field_size = sizes.get(insn.mnemonic, 4)
                    if insn.mnemonic == 'ldr' and insn.op_str.split(',')[0].strip().startswith('x'):
                        field_size = 8

                    # Check if this is followed by a store to CIStream buffer
                    is_payload = False
                    for j in range(i+1, min(i+8, len(insns))):
                        if insns[j].mnemonic in ('strh', 'strb', 'str') and 'uxtw' in insns[j].op_str:
                            is_payload = True
                            break
                        if insns[j].mnemonic in ('strh', 'strb', 'str'):
                            ops = insns[j].op_str
                            # Also catch str wN, [xN, xN] pattern (no uxtw)
                            if '], #' not in ops and '[' in ops:
                                parts = ops.split('[')
                                if len(parts) > 1:
                                    inner = parts[1].rstrip(']')
                                    if ', x' in inner or ', w' in inner:
                                        is_payload = True
                                        break

                    if is_payload:
                        ws = current_write_size if current_write_size else field_size
                        payload_fields.append({
                            'struct_offset': offset,
                            'size': ws,
                            'payload_offset': payload_offset,
                            'insn_addr': insn.address,
                            'load_mnemonic': insn.mnemonic,
                        })
                        payload_offset += ws
                        current_write_size = 0
                    break  # found match for this load, no need to check other regs

    return payload_fields, insns


# ═══════════════════════════════════════════════════════════════════
# TASK 2: Find and analyze packData for ALL _NEW CMSGs
# ═══════════════════════════════════════════════════════════════════
p()
p("=" * 100)
p("TASK 2: packData ANALYSIS FOR ALL _NEW CMSGs IN RANGE")
p("=" * 100)

# Build class name fragments to search for
# CMSG_START_MARCH_NEW -> class name contains "StartMarchNew" or similar
# The mangled names use the full CMSG class name

new_opcodes_info = {}
for opc in sorted(all_opcodes_in_range.keys()):
    name = all_opcodes_in_range[opc]
    if '_NEW' not in name and 'ONEKEY' not in name:
        continue

    # Convert CMSG_XXX_YYY_NEW to search fragments
    # The C++ class names are like CMSG_START_MARCH_NEW
    # Mangled: contains the class name literally or in mangled form
    # We search for parts of the name in symbol table
    search_key = name  # e.g., 'CMSG_START_MARCH_NEW'
    new_opcodes_info[opc] = {
        'name': name,
        'search_key': search_key,
        'packdata': None,
        'constructor': None,
    }

# Find packData symbols for each
p()
for opc in sorted(new_opcodes_info.keys()):
    info = new_opcodes_info[opc]
    name = info['name']

    # Try different search patterns
    search_patterns = [name]

    # Also try partial names - remove CMSG_ prefix, remove _REQUEST/_NEW suffix variations
    base = name.replace('CMSG_', '').replace('_REQUEST_NEW', '_NEW').replace('_REQUEST', '')
    search_patterns.append(base)

    # Try the class name with mixed conventions
    # e.g., CMSG_START_MARCH_NEW -> look for StartMarchNew or START_MARCH_NEW
    search_patterns.append(name.replace('CMSG_', ''))

    found = None
    for pat in search_patterns:
        result = find_packdata(pat)
        if result:
            found = result
            break

    if found:
        sym_name, sym_addr, sym_size = found
        info['packdata'] = (sym_name, sym_addr, sym_size)
        p(f"  0x{opc:04X} {name}")
        p(f"         packData @ 0x{sym_addr:08X}, size={sym_size}B")
        p(f"         symbol: {sym_name[:80]}")

        # Analyze the packData
        fields, insns = extract_payload_fields(sym_addr, sym_size)
        info['fields'] = fields

        if fields:
            total_size = sum(f['size'] for f in fields)
            p(f"         payload: {total_size} bytes, {len(fields)} fields:")
            for fi, f in enumerate(fields):
                p(f"           [{fi:2d}] buf[{f['payload_offset']:3d}] = "
                  f"struct[0x{f['struct_offset']:02X}] "
                  f"{f['size']}B ({f['load_mnemonic']}) "
                  f"@ 0x{f['insn_addr']:08X}")
        else:
            p(f"         payload: NO FIELDS DETECTED (may need manual analysis)")
        p()
    else:
        info['packdata'] = None
        info['fields'] = []
        p(f"  0x{opc:04X} {name}")
        p(f"         packData: NOT FOUND in dynsym")
        p()


# ═══════════════════════════════════════════════════════════════════
# TASK 3: DEEP analysis of critical packData functions
# ═══════════════════════════════════════════════════════════════════
p()
p("=" * 100)
p("TASK 3: DEEP ANALYSIS OF CRITICAL PACKDATA FUNCTIONS")
p("=" * 100)

CRITICAL_OPCODES = {
    0x0CE8: ('CMSG_START_MARCH_NEW', 'START_MARCH'),
    0x0CED: ('CMSG_SOLDIER_NORMAL_PRODUCE_REQUEST_NEW', 'TRAIN'),
    0x0CEF: ('CMSG_BUILDING_OPERAT_REQUEST_NEW', 'BUILD'),
    0x0CEE: ('CMSG_SCIENCE_NORMAL_STUDY_REQUEST_NEW', 'RESEARCH'),
}


def deep_analyze_packdata(addr, size, label):
    """Deep analysis: full disassembly trace with annotations."""
    max_bytes = min(size if size > 0 else 1500, 3000)
    code = data[addr:addr + max_bytes]
    insns = list(md.disasm(code, addr))

    p(f"  Total instructions: {len(insns)}")
    p(f"  Address range: 0x{addr:08X} - 0x{addr + size:08X}")
    p()

    # Track registers
    this_regs = {'x0', 'x19', 'x20'}
    stream_regs = {'x1', 'x20', 'x21'}

    # First pass: identify this_reg and stream_reg
    actual_this = 'x0'
    actual_stream = 'x1'
    for insn in insns[:30]:
        if insn.mnemonic == 'mov':
            if insn.op_str.startswith('x19, x0'):
                actual_this = 'x19'
            elif insn.op_str.startswith('x20, x0'):
                actual_this = 'x20'
            if insn.op_str.startswith('x20, x1'):
                actual_stream = 'x20'
            elif insn.op_str.startswith('x21, x1'):
                actual_stream = 'x21'

    p(f"  this register: {actual_this}")
    p(f"  CIStream register: {actual_stream}")
    p()

    # Detailed field trace
    fields = []
    buf_pos = 0

    # Manual deep trace: look for the pattern:
    # 1) capacity check: add wN, pos, #SIZE ; cmp
    # 2) load from this: ldr/ldrh/ldrb wN, [this_reg, #OFF]
    # 3) store to buffer: str/strh/strb wN, [buf, pos_reg, uxtw]
    # 4) position update: add pos, pos, #SIZE ; strh pos, [stream, #0xa]

    write_sequence = []  # collect (addr, mnemonic, size, struct_offset)

    for i, insn in enumerate(insns):
        if insn.mnemonic == 'ret' and insn.address > addr + 20:
            break

        # Detect stores to CIStream buffer (the actual payload writes)
        is_buf_write = False
        write_size = 0

        if insn.mnemonic in ('str', 'strh', 'strb'):
            ops = insn.op_str
            # Check for: str/strh/strb wN, [bufptr, pos, uxtw] or [bufptr, xN]
            if 'uxtw' in ops or (']' in ops and '[' in ops):
                parts = ops.split('[')
                if len(parts) > 1:
                    inner = parts[1].rstrip(']')
                    # Must NOT be a stream metadata write (#0xa, #0xc, #8)
                    if '#0xa' not in ops and '#0xc' not in ops and '#8' not in ops and '#0x8' not in ops:
                        if 'uxtw' in ops or ', x' in inner or ', w' in inner:
                            # Check it's not writing to stream fields
                            if not any(f'{sr}, #' in ops for sr in [actual_stream]):
                                is_buf_write = True
                                src_reg = ops.split(',')[0].strip()
                                if insn.mnemonic == 'strb':
                                    write_size = 1
                                elif insn.mnemonic == 'strh':
                                    write_size = 2
                                elif insn.mnemonic == 'str':
                                    write_size = 8 if src_reg.startswith('x') else 4

        if is_buf_write:
            # Trace back to find the corresponding load from this struct
            struct_offset = -1
            load_size = write_size
            load_mnem = '?'
            src_reg = insn.op_str.split(',')[0].strip()

            # Look backwards for the load instruction that populated src_reg
            # Also check for the w-register version of x-register
            check_regs = [src_reg]
            if src_reg.startswith('x'):
                check_regs.append('w' + src_reg[1:])
            elif src_reg.startswith('w'):
                check_regs.append('x' + src_reg[1:])

            for j in range(i-1, max(i-20, 0), -1):
                prev = insns[j]
                if prev.mnemonic in ('ldr', 'ldrh', 'ldrb', 'ldrsb', 'ldrsh', 'ldrsw'):
                    dst = prev.op_str.split(',')[0].strip()
                    if dst in check_regs:
                        # Check if loading from this struct
                        for reg in [actual_this, 'x0', 'x19', 'x20']:
                            if f'[{reg}]' in prev.op_str or f'[{reg},' in prev.op_str:
                                if '#' in prev.op_str:
                                    try:
                                        struct_offset = int(
                                            prev.op_str.split('#')[-1].rstrip(']').rstrip('!').strip(), 0)
                                    except:
                                        struct_offset = 0
                                else:
                                    struct_offset = 0
                                load_mnem = prev.mnemonic
                                break
                    if struct_offset >= 0:
                        break
                # Also check for immediate loads (mov wN, #imm)
                if prev.mnemonic in ('mov', 'movz', 'movk') and '#' in prev.op_str:
                    dst = prev.op_str.split(',')[0].strip()
                    if dst in check_regs:
                        struct_offset = -2  # immediate value, not from struct
                        load_mnem = prev.mnemonic
                        break
                # Check for lsr (computed value like array count)
                if prev.mnemonic in ('lsr', 'asr') and '#' in prev.op_str:
                    dst = prev.op_str.split(',')[0].strip()
                    if dst in check_regs:
                        struct_offset = -3  # computed (e.g., vector length)
                        load_mnem = prev.mnemonic
                        break

            fields.append({
                'buf_offset': buf_pos,
                'write_size': write_size,
                'struct_offset': struct_offset,
                'load_mnemonic': load_mnem,
                'write_addr': insn.address,
                'write_mnemonic': insn.mnemonic,
            })
            buf_pos += write_size

    return fields


for opc in sorted(CRITICAL_OPCODES.keys()):
    cmsg_name, short_name = CRITICAL_OPCODES[opc]
    p()
    p("-" * 100)
    p(f"  DEEP ANALYSIS: 0x{opc:04X} = {cmsg_name} ({short_name})")
    p("-" * 100)

    info = new_opcodes_info.get(opc, {})
    packdata_info = info.get('packdata')

    if not packdata_info:
        # Try finding it directly
        for pat in [cmsg_name, cmsg_name.replace('CMSG_', '')]:
            result = find_packdata(pat)
            if result:
                packdata_info = result
                break

    if not packdata_info:
        p(f"  ERROR: packData symbol not found for {cmsg_name}")
        continue

    sym_name, sym_addr, sym_size = packdata_info
    p(f"  Symbol: {sym_name[:90]}")
    p(f"  Address: 0x{sym_addr:08X}, Size: {sym_size} bytes")
    p()

    fields = deep_analyze_packdata(sym_addr, sym_size, short_name)

    if fields:
        p(f"  PAYLOAD FIELD MAP ({len(fields)} fields detected):")
        p(f"  {'Idx':>4s}  {'BufOff':>7s}  {'Size':>5s}  {'StructOff':>10s}  {'Load':>8s}  {'WriteAddr':>12s}")
        p(f"  {'---':>4s}  {'------':>7s}  {'----':>5s}  {'---------':>10s}  {'----':>8s}  {'---------':>12s}")
        for fi, f in enumerate(fields):
            so_str = f"0x{f['struct_offset']:02X}" if f['struct_offset'] >= 0 else (
                "IMMEDIATE" if f['struct_offset'] == -2 else
                "COMPUTED" if f['struct_offset'] == -3 else "UNKNOWN")
            p(f"  [{fi:2d}]  buf[{f['buf_offset']:3d}]  {f['write_size']:3d}B  {so_str:>10s}  "
              f"{f['load_mnemonic']:>8s}  0x{f['write_addr']:08X}")
    else:
        p(f"  NO FIELDS detected via automated trace.")

    # For CMSG_START_MARCH_NEW, also print the known manual analysis
    if opc == 0x0CE8:
        p()
        p("  MANUAL REFERENCE (from 35_march_packdata_deep.py):")
        p("  ─────────────────────────────────────────────────────────")
        p("  The START_MARCH_NEW packData has this layout:")
        p("  buf[ 0.. 1]  2B  struct[0x00]  msg_id / sub_type (u16)")
        p("  buf[ 2.. 3]  2B  struct[0x02]  march_type (u16)")
        p("  buf[ 4]      1B  struct[0x04]  flag_byte_0 (u8)")
        p("  buf[ 5]      1B  struct[0x05]  flag_byte_1 (u8)")
        p("  buf[ 6]      1B  struct[0x06]  flag_byte_2 (u8)")
        p("  buf[ 7]      1B  struct[0x07]  flag_byte_3 (u8)")
        p("  buf[ 8]      1B  struct[0x08]  flag_byte_4 / hero_count? (u8)")
        p("  buf[ 9..16]  8B  struct[0x10]  target_coords (u64 = two u32 x,y)")
        p("  buf[17..18]  2B  struct[0x18]  kingdom_id / target_kingdom (u16)")
        p("  buf[19..20]  2B  struct[0x1A]  march_slot / queue_id (u16)")
        p("  buf[21]      1B  (computed)    array_count = len(troop_vector)")
        p("  buf[22..N]   4B  (array loop)  troop_entry[i] (u32) x count")
        p("  buf[N+1..4]  4B  struct[0x38]  tile_type / resource_id (u32)")
        p("  buf[...]     1B  struct[0x3C]  march_flag / sub_flag (u8)")
        p("  buf[...]     8B  struct[0x40]  rally_timestamp / march_param (u64)")
        p("  buf[...]     1B  struct[0x48]  extra_flag_0 (u8)")
        p("  buf[...]     1B  struct[0x49]  extra_flag_1 (u8)")
        p("  buf[...]     8B  struct[0x50]  extra_param (u64)")
        p("  buf[...]     1B  struct[0x58]  extra_flag_2 (u8)")
        p("  buf[...]     4B  struct[0x5C]  extra_param_2 (u32)")
        p()
        p("  Total fixed: 21B header + 1B count + 4B tile + 1+8+1+1+8+1+4 = 50B + N*4B troops")
        p("  March types: 0=attack, 1=gather, 2=scout, 5=rally, 10=monster")

    if opc == 0x0CED:
        p()
        p("  KNOWN FORMAT (verified working in bot):")
        p("  ─────────────────────────────────────────────────────────")
        p("  buf[ 0.. 1]  2B  struct[0x00]  building_pos (u16)")
        p("  buf[ 2.. 5]  4B  struct[0x04]  soldier_type (u32)")
        p("  buf[ 6.. 9]  4B  struct[0x08]  count (u32)")
        p("  buf[10..13]  4B  struct[0x0C]  queue_type (u32)")
        p("  buf[14..17]  4B  struct[0x10]  unknown_param (u32)")
        p("  buf[18]      1B  struct[0x14]  use_gold_flag (u8)")
        p("  Total: 19 bytes")

    if opc == 0x0CEF:
        p()
        p("  KNOWN FORMAT (verified working in bot):")
        p("  ─────────────────────────────────────────────────────────")
        p("  buf[ 0.. 1]  2B  struct[0x00]  building_pos (u16)")
        p("  buf[ 2.. 5]  4B  struct[0x04]  building_type (u32)")
        p("  buf[ 6.. 9]  4B  struct[0x08]  operation_type (u32)")
        p("  buf[10..13]  4B  struct[0x0C]  target_level (u32)")
        p("  buf[14..17]  4B  struct[0x10]  extra_param (u32)")
        p("  buf[18..19]  2B  struct[0x14]  worker_queue (u16)")
        p("  buf[20..21]  2B  struct[0x16]  use_gold_flag (u16)")
        p("  Total: 22 bytes")

    if opc == 0x0CEE:
        p()
        p("  KNOWN FORMAT (verified working in bot):")
        p("  ─────────────────────────────────────────────────────────")
        p("  buf[ 0.. 1]  2B  struct[0x00]  science_id (u16)")
        p("  buf[ 2.. 5]  4B  struct[0x04]  target_level (u32)")
        p("  buf[ 6.. 9]  4B  struct[0x08]  study_type (u32)")
        p("  buf[10..11]  2B  struct[0x0C]  use_gold_flag (u16)")
        p("  Total: 12 bytes")


# ═══════════════════════════════════════════════════════════════════
# TASK 4: Decrypt 0x0CE8 payloads from PCAPs
# ═══════════════════════════════════════════════════════════════════
p()
p("=" * 100)
p("TASK 4: DECRYPT 0x0CE8 (START_MARCH_NEW) PAYLOADS FROM PCAPs")
p("=" * 100)

# Decryption function
sk_bytes = [
    SERVER_KEY_U32 & 0xFF,
    (SERVER_KEY_U32 >> 8) & 0xFF,
    (SERVER_KEY_U32 >> 16) & 0xFF,
    (SERVER_KEY_U32 >> 24) & 0xFF,
]


def decrypt_payload(encrypted_payload_after_header):
    """Decrypt encrypted payload bytes (bytes after the 4-byte len+opcode header).

    encrypted_payload_after_header format:
      [0] checksum
      [1] msg_lo
      [2] verify (msg_lo ^ 0xB7)
      [3] msg_hi
      [4..] encrypted action data
    """
    if len(encrypted_payload_after_header) < 5:
        return None, None

    payload = encrypted_payload_after_header
    checksum_byte = payload[0]
    msg_lo = payload[1]
    verify = payload[2]
    msg_hi = payload[3]

    # Verify msg_lo ^ 0xB7 == verify
    if (msg_lo ^ 0xB7) & 0xFF != verify:
        return None, "verify mismatch: msg_lo=0x{:02X}, verify=0x{:02X}, expected=0x{:02X}".format(
            msg_lo, verify, (msg_lo ^ 0xB7) & 0xFF)

    msg = [msg_lo, msg_hi]

    # Decrypt action data (bytes 4+)
    dec = bytearray(len(payload) - 4)
    for p_idx in range(4, len(payload)):
        i = p_idx + 4  # offset in full packet (4-byte header + payload offset)
        table_b = TABLE[i % 7]
        sk_b = sk_bytes[i % 4]
        msg_b = msg[i % 2]
        intermediate = (payload[p_idx] ^ sk_b ^ table_b) & 0xFF
        dec[p_idx - 4] = (intermediate - msg_b * 17) & 0xFF

    # Verify checksum
    computed_checksum = 0
    for b in payload[4:]:
        computed_checksum = (computed_checksum + b) & 0xFF

    checksum_ok = (computed_checksum == checksum_byte)

    return bytes(dec), f"checksum={'OK' if checksum_ok else 'MISMATCH'}, msg=0x{msg_hi:02X}{msg_lo:02X}"


def extract_tcp_streams_from_pcap(pcap_path):
    """Extract TCP payload from PCAP file. Returns list of (direction, raw_bytes) tuples."""
    try:
        with open(pcap_path, 'rb') as f:
            magic = struct.unpack('<I', f.read(4))[0]
            if magic == 0xa1b2c3d4:
                endian = '<'
            elif magic == 0xd4c3b2a1:
                endian = '>'
            else:
                return []

            f.read(20)  # rest of global header

            packets = []
            while True:
                hdr = f.read(16)
                if len(hdr) < 16:
                    break
                ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
                pkt_data = f.read(incl_len)
                if len(pkt_data) < incl_len:
                    break
                packets.append(pkt_data)

            return packets
    except Exception as e:
        return []


def find_0xCE8_packets_in_pcap(pcap_path):
    """Find and decrypt 0x0CE8 opcode packets in a PCAP."""
    packets = extract_tcp_streams_from_pcap(pcap_path)
    results = []

    for pkt_data in packets:
        # Skip link layer (Ethernet = 14 bytes typically, but could be other)
        # Try to find IP header
        if len(pkt_data) < 54:
            continue

        # Try Ethernet (14 bytes) + IP (20+ bytes) + TCP (20+ bytes)
        for link_offset in [14, 0, 4]:  # Ethernet, raw IP, Linux cooked
            if link_offset + 40 > len(pkt_data):
                continue

            ip_start = link_offset
            # Check IP version
            if (pkt_data[ip_start] >> 4) != 4:
                continue

            ip_hdr_len = (pkt_data[ip_start] & 0x0F) * 4
            if pkt_data[ip_start + 9] != 6:  # TCP
                continue

            tcp_start = ip_start + ip_hdr_len
            if tcp_start + 20 > len(pkt_data):
                continue

            tcp_hdr_len = ((pkt_data[tcp_start + 12] >> 4) * 4)
            tcp_payload_start = tcp_start + tcp_hdr_len

            if tcp_payload_start >= len(pkt_data):
                continue

            tcp_payload = pkt_data[tcp_payload_start:]

            # Look for game packets within TCP payload
            # Game packet: [u16 LE total_len] [u16 LE opcode] [payload...]
            pos = 0
            while pos + 4 <= len(tcp_payload):
                if pos + 2 > len(tcp_payload):
                    break
                pkt_len = struct.unpack('<H', tcp_payload[pos:pos+2])[0]
                if pkt_len < 4 or pkt_len > 4096:
                    pos += 1
                    continue
                if pos + pkt_len > len(tcp_payload):
                    pos += 1
                    continue

                opcode = struct.unpack('<H', tcp_payload[pos+2:pos+4])[0]

                if opcode == 0x0CE8:
                    pkt_bytes = tcp_payload[pos:pos+pkt_len]
                    encrypted_payload = pkt_bytes[4:]  # after len+opcode

                    dec, info = decrypt_payload(encrypted_payload)
                    results.append({
                        'pcap': os.path.basename(pcap_path),
                        'pkt_len': pkt_len,
                        'encrypted': encrypted_payload.hex(),
                        'decrypted': dec.hex() if dec else None,
                        'info': info,
                        'raw': pkt_bytes.hex(),
                    })

                pos += pkt_len
            break  # found valid IP, no need to try other offsets

    return results


# Search all PCAPs
pcap_files = glob.glob(os.path.join(PCAP_DIR, "*.pcap"))
p(f"\nSearching {len(pcap_files)} PCAP files for 0x0CE8 packets...")

all_march_packets = []
for pcap_path in sorted(pcap_files):
    results = find_0xCE8_packets_in_pcap(pcap_path)
    if results:
        all_march_packets.extend(results)
        p(f"  {os.path.basename(pcap_path)}: found {len(results)} march packet(s)")

p(f"\nTotal 0x0CE8 packets found: {len(all_march_packets)}")

for i, pkt in enumerate(all_march_packets):
    p(f"\n  --- March Packet #{i+1} (from {pkt['pcap']}) ---")
    p(f"  Packet length: {pkt['pkt_len']} bytes")
    p(f"  Raw hex: {pkt['raw'][:120]}{'...' if len(pkt['raw']) > 120 else ''}")
    p(f"  Encrypted payload ({len(pkt['encrypted'])//2}B): {pkt['encrypted'][:100]}{'...' if len(pkt['encrypted']) > 100 else ''}")
    p(f"  Decrypt info: {pkt['info']}")
    if pkt['decrypted']:
        dec_hex = pkt['decrypted']
        dec_bytes = bytes.fromhex(dec_hex)
        p(f"  Decrypted ({len(dec_bytes)}B): {dec_hex[:120]}{'...' if len(dec_hex) > 120 else ''}")

        # Parse according to known layout
        if len(dec_bytes) >= 21:
            sub_type = struct.unpack('<H', dec_bytes[0:2])[0]
            march_type = struct.unpack('<H', dec_bytes[2:4])[0]
            flags = dec_bytes[4:9]
            coords = struct.unpack('<II', dec_bytes[9:17]) if len(dec_bytes) >= 17 else (0, 0)
            kingdom = struct.unpack('<H', dec_bytes[17:19])[0] if len(dec_bytes) >= 19 else 0
            slot = struct.unpack('<H', dec_bytes[19:21])[0] if len(dec_bytes) >= 21 else 0

            p(f"  Parsed fields:")
            p(f"    sub_type      = 0x{sub_type:04X} ({sub_type})")
            p(f"    march_type    = 0x{march_type:04X} ({march_type})")
            p(f"    flags[0..4]   = {flags.hex()}")
            p(f"    target_x      = {coords[0]}")
            p(f"    target_y      = {coords[1]}")
            p(f"    kingdom       = {kingdom}")
            p(f"    march_slot    = {slot}")

            if len(dec_bytes) > 21:
                array_count = dec_bytes[21]
                p(f"    troop_count   = {array_count}")
                offset = 22
                for ti in range(array_count):
                    if offset + 4 <= len(dec_bytes):
                        troop_val = struct.unpack('<I', dec_bytes[offset:offset+4])[0]
                        p(f"    troop[{ti}]      = 0x{troop_val:08X} ({troop_val})")
                        offset += 4

                if offset + 4 <= len(dec_bytes):
                    tile_type = struct.unpack('<I', dec_bytes[offset:offset+4])[0]
                    p(f"    tile_type      = 0x{tile_type:08X} ({tile_type})")
                    offset += 4

                if offset + 1 <= len(dec_bytes):
                    march_flag = dec_bytes[offset]
                    p(f"    march_flag     = 0x{march_flag:02X}")
                    offset += 1

                if offset + 8 <= len(dec_bytes):
                    rally_ts = struct.unpack('<Q', dec_bytes[offset:offset+8])[0]
                    p(f"    rally_param    = 0x{rally_ts:016X}")
                    offset += 8

                if offset + 1 <= len(dec_bytes):
                    p(f"    extra_flag_0   = 0x{dec_bytes[offset]:02X}")
                    offset += 1
                if offset + 1 <= len(dec_bytes):
                    p(f"    extra_flag_1   = 0x{dec_bytes[offset]:02X}")
                    offset += 1

                if offset + 8 <= len(dec_bytes):
                    extra = struct.unpack('<Q', dec_bytes[offset:offset+8])[0]
                    p(f"    extra_param    = 0x{extra:016X}")
                    offset += 8

                if offset + 1 <= len(dec_bytes):
                    p(f"    extra_flag_2   = 0x{dec_bytes[offset]:02X}")
                    offset += 1
                if offset + 4 <= len(dec_bytes):
                    ep2 = struct.unpack('<I', dec_bytes[offset:offset+4])[0]
                    p(f"    extra_param_2  = 0x{ep2:08X} ({ep2})")
                    offset += 4

                if offset < len(dec_bytes):
                    remaining = dec_bytes[offset:]
                    p(f"    remaining      = {remaining.hex()} ({len(remaining)} bytes)")
    else:
        p(f"  Decryption failed: {pkt['info']}")


# ═══════════════════════════════════════════════════════════════════
# TASK 5: Cross-reference decrypted payloads with packData layout
# ═══════════════════════════════════════════════════════════════════
p()
p("=" * 100)
p("TASK 5: CROSS-REFERENCE VERIFICATION")
p("=" * 100)
p()

if all_march_packets:
    # Check if decrypted payloads match the expected structure
    valid_count = 0
    for i, pkt in enumerate(all_march_packets):
        if not pkt['decrypted']:
            continue
        dec_bytes = bytes.fromhex(pkt['decrypted'])

        p(f"  Packet #{i+1}: {len(dec_bytes)} decrypted bytes")

        # Sanity checks based on known layout
        checks = []
        if len(dec_bytes) >= 4:
            march_type = struct.unpack('<H', dec_bytes[2:4])[0]
            checks.append(f"march_type={march_type} (valid: 0-10 range = {'OK' if march_type <= 20 else 'SUSPICIOUS'})")

        if len(dec_bytes) >= 17:
            x, y = struct.unpack('<II', dec_bytes[9:17])
            checks.append(f"coords=({x},{y}) (valid: both < 2048 = {'OK' if x < 2048 and y < 2048 else 'SUSPICIOUS'})")

        if len(dec_bytes) >= 19:
            kingdom = struct.unpack('<H', dec_bytes[17:19])[0]
            checks.append(f"kingdom={kingdom} (valid: < 1000 = {'OK' if kingdom < 1000 else 'SUSPICIOUS'})")

        if len(dec_bytes) >= 22:
            count = dec_bytes[21]
            checks.append(f"troop_count={count} (valid: 1-5 = {'OK' if 1 <= count <= 5 else 'SUSPICIOUS'})")

            expected_min = 22 + count * 4 + 4 + 1 + 8 + 1 + 1 + 8 + 1 + 4  # all post-array fields
            checks.append(f"expected_size>={expected_min}, actual={len(dec_bytes)} "
                          f"({'MATCH' if len(dec_bytes) >= expected_min else 'SHORT'})")

        all_ok = all('OK' in c or 'MATCH' in c for c in checks)
        if all_ok:
            valid_count += 1

        for c in checks:
            p(f"    {c}")
        p(f"    Overall: {'VALID - layout matches packData' if all_ok else 'ISSUES DETECTED'}")
        p()

    p(f"  Summary: {valid_count}/{len([p for p in all_march_packets if p['decrypted']])} packets validate against packData layout")
else:
    p("  No 0x0CE8 packets found in PCAPs to cross-reference.")
    p("  This could mean:")
    p("  - The server key 0x88587D29 was from a different session than available PCAPs")
    p("  - The march packets may be in a different PCAP not yet captured")
    p("  - Try capturing fresh PCAPs with actual march commands")


# ═══════════════════════════════════════════════════════════════════
# Additional: scan for ALL encrypted-range opcodes in PCAPs
# ═══════════════════════════════════════════════════════════════════
p()
p("=" * 100)
p("BONUS: ALL ENCRYPTED-RANGE OPCODES (0x0CE0-0x0CFF) FOUND IN PCAPs")
p("=" * 100)

encrypted_opcode_counts = {}
for pcap_path in sorted(pcap_files):
    packets = extract_tcp_streams_from_pcap(pcap_path)
    for pkt_data in packets:
        if len(pkt_data) < 54:
            continue
        for link_offset in [14, 0, 4]:
            if link_offset + 40 > len(pkt_data):
                continue
            ip_start = link_offset
            if (pkt_data[ip_start] >> 4) != 4:
                continue
            ip_hdr_len = (pkt_data[ip_start] & 0x0F) * 4
            if pkt_data[ip_start + 9] != 6:
                continue
            tcp_start = ip_start + ip_hdr_len
            if tcp_start + 20 > len(pkt_data):
                continue
            tcp_hdr_len = ((pkt_data[tcp_start + 12] >> 4) * 4)
            tcp_payload_start = tcp_start + tcp_hdr_len
            if tcp_payload_start >= len(pkt_data):
                continue
            tcp_payload = pkt_data[tcp_payload_start:]

            pos = 0
            while pos + 4 <= len(tcp_payload):
                pkt_len = struct.unpack('<H', tcp_payload[pos:pos+2])[0]
                if pkt_len < 4 or pkt_len > 4096:
                    pos += 1
                    continue
                if pos + pkt_len > len(tcp_payload):
                    break
                opcode = struct.unpack('<H', tcp_payload[pos+2:pos+4])[0]
                if 0x0CE0 <= opcode <= 0x0CFF:
                    key = (opcode, os.path.basename(pcap_path))
                    encrypted_opcode_counts[key] = encrypted_opcode_counts.get(key, 0) + 1
                pos += pkt_len
            break

if encrypted_opcode_counts:
    # Group by opcode
    by_opcode = {}
    for (opc, pcap), count in encrypted_opcode_counts.items():
        if opc not in by_opcode:
            by_opcode[opc] = []
        by_opcode[opc].append((pcap, count))

    for opc in sorted(by_opcode.keys()):
        name = all_opcodes_in_range.get(opc, 'UNKNOWN')
        total = sum(c for _, c in by_opcode[opc])
        p(f"\n  0x{opc:04X} ({name}): {total} packet(s)")
        for pcap, count in sorted(by_opcode[opc]):
            p(f"    {pcap}: {count}")
else:
    p("\n  No encrypted-range opcodes found in any PCAP.")
    p("  (Game packets may be fragmented across TCP segments)")


# ═══════════════════════════════════════════════════════════════════
# Save markdown output
# ═══════════════════════════════════════════════════════════════════
p()
p("=" * 100)
p("END OF ANALYSIS")
p("=" * 100)

os.makedirs(os.path.dirname(OUTPUT_MD), exist_ok=True)
with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
    f.write("# Encrypted Opcodes Analysis (0x0CE0-0x0CFF)\n\n")
    f.write("Generated by 44_encrypted_opcodes_analysis.py\n\n")
    f.write("```\n")
    for line in out_lines:
        f.write(line + "\n")
    f.write("```\n")

print(f"\nResults saved to: {OUTPUT_MD}")

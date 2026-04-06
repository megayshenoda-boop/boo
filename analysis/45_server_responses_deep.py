#!/usr/bin/env python3
"""
45_server_responses_deep.py - Deep analysis of server response formats.
Part A: Binary analysis of getData methods in libgame.so
Part B: PCAP analysis of server response packets
"""
import struct, os, sys, glob, collections, traceback
from pathlib import Path

sys.path.insert(0, r'D:\CascadeProjects\claude')
sys.path.insert(0, r'D:\CascadeProjects\analysis\findings')

try:
    from cmsg_opcodes import CMSG_OPCODES
except ImportError:
    CMSG_OPCODES = {}

try:
    from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
    HAS_CAPSTONE = True
except ImportError:
    HAS_CAPSTONE = False

# ------------------------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------------------------
LIBGAME = Path(r'D:\CascadeProjects\libgame.so')
DYNSTR_OFF = 0x682A10
DYNSYM_OFF = 0x2F8
DYNSYM_SIZE = 0x682758
OUTPUT = Path(r'D:\CascadeProjects\analysis\findings\server_responses_deep.md')

TABLE = [0x58, 0xef, 0xd7, 0x14, 0xa2, 0x3b, 0x9c]

PCAP_DIRS = [
    Path(r'D:\CascadeProjects'),
    Path(r'D:\CascadeProjects\codex_lab'),
    Path(r'D:\CascadeProjects\config-decryptor'),
]

# Key opcodes to analyze in detail
KEY_OPCODES = [0x0033, 0x0043, 0x0042, 0x000C, 0x0071, 0x006F, 0x00B8, 0x0037, 0x06C2]

report = []
def log(s=""):
    print(s)
    report.append(s)

# ------------------------------------------------------------------------------
# PART A: BINARY ANALYSIS
# ------------------------------------------------------------------------------

def read_elf_data():
    """Read libgame.so and parse dynsym for getData symbols."""
    with open(LIBGAME, 'rb') as f:
        elf = f.read()
    return elf

def parse_dynstr(elf, offset):
    """Extract null-terminated strings from dynstr starting at offset."""
    # We just need an accessor
    def get_str(idx):
        end = elf.index(b'\x00', offset + idx)
        return elf[offset + idx : end].decode('ascii', errors='replace')
    return get_str

def parse_dynsym(elf):
    """Parse DYNSYM entries (ELF64 Sym: 24 bytes each)."""
    get_str = parse_dynstr(elf, DYNSTR_OFF)

    sym_entry_size = 24  # Elf64_Sym
    num_entries = DYNSYM_SIZE // sym_entry_size

    symbols = []
    for i in range(num_entries):
        off = DYNSYM_OFF + i * sym_entry_size
        if off + sym_entry_size > len(elf):
            break
        st_name = struct.unpack_from('<I', elf, off)[0]
        st_info = elf[off + 4]
        st_other = elf[off + 5]
        st_shndx = struct.unpack_from('<H', elf, off + 6)[0]
        st_value = struct.unpack_from('<Q', elf, off + 8)[0]
        st_size = struct.unpack_from('<Q', elf, off + 16)[0]

        if st_name == 0:
            continue
        try:
            name = get_str(st_name)
        except:
            continue

        symbols.append({
            'name': name,
            'value': st_value,
            'size': st_size,
            'info': st_info,
            'shndx': st_shndx,
        })
    return symbols

def find_getData_symbols(symbols):
    """Find all symbols containing 'getData'."""
    results = []
    for s in symbols:
        if 'getData' in s['name'] and s['value'] != 0:
            results.append(s)
    return sorted(results, key=lambda x: x['name'])

def demangle_simple(name):
    """Simple C++ name demangling for CMSG classes."""
    # Pattern: _ZN14CMSG_CLASSNAME7getDataER9CIStream
    # or _ZNK...
    parts = []
    i = 0
    if name.startswith('_ZNK'):
        i = 4
    elif name.startswith('_ZN'):
        i = 3
    else:
        return name, name

    class_parts = []
    while i < len(name) and name[i].isdigit():
        nlen = 0
        while i < len(name) and name[i].isdigit():
            nlen = nlen * 10 + int(name[i])
            i += 1
        part = name[i:i+nlen]
        class_parts.append(part)
        i += nlen

    if len(class_parts) >= 2:
        cls = class_parts[0]
        method = class_parts[1]
        return cls, method
    elif len(class_parts) == 1:
        return class_parts[0], '?'
    return name, name

def disassemble_getData(elf, addr, size, sym_name):
    """Disassemble a getData method and trace CIStream reads."""
    if not HAS_CAPSTONE:
        return "capstone not available"

    if addr == 0 or size == 0:
        return "no code"

    # Read code bytes
    code = elf[addr:addr+min(size, 4096)]
    if not code:
        return "no code at address"

    md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
    md.detail = True

    reads = []
    read_types = []
    current_offset = None

    instructions = list(md.disasm(code, addr))

    # Track patterns:
    # LDR Wn, [Xm, #off] - 4-byte read
    # LDRH Wn, [Xm, #off] - 2-byte read
    # LDRB Wn, [Xm, #off] - 1-byte read
    # STR after read = storing parsed value
    # ADD to increment position pointer

    field_reads = []
    for idx, insn in enumerate(instructions):
        mnem = insn.mnemonic
        op_str = insn.op_str

        # Detect loads from stream buffer (CIStream pattern)
        if mnem in ('ldr', 'ldrh', 'ldrb', 'ldrsw', 'ldrsh', 'ldrsb'):
            if mnem == 'ldr' and 'w' in op_str.split(',')[0].lower():
                field_reads.append(('u32', insn.address, op_str))
            elif mnem == 'ldr' and 'x' in op_str.split(',')[0].lower():
                field_reads.append(('u64', insn.address, op_str))
            elif mnem == 'ldrh':
                field_reads.append(('u16', insn.address, op_str))
            elif mnem == 'ldrb':
                field_reads.append(('u8', insn.address, op_str))
            elif mnem == 'ldrsw':
                field_reads.append(('s32', insn.address, op_str))
            elif mnem == 'ldrsh':
                field_reads.append(('s16', insn.address, op_str))
            elif mnem == 'ldrsb':
                field_reads.append(('s8', insn.address, op_str))

    # Also look for BL calls (calls to read helpers like readU32, readU16 etc)
    call_reads = []
    for idx, insn in enumerate(instructions):
        if insn.mnemonic == 'bl':
            target_str = insn.op_str
            call_reads.append((insn.address, target_str))

    return field_reads, call_reads, instructions

def analyze_getData_detailed(elf, symbols, target_classes):
    """Deep analysis of specific getData methods."""
    results = {}

    for sym in symbols:
        cls, method = demangle_simple(sym['name'])
        if method != 'getData':
            continue

        for target in target_classes:
            if target.upper() in cls.upper() or cls.upper() in target.upper():
                addr = sym['value']
                size = sym['size']

                if not HAS_CAPSTONE:
                    results[cls] = {
                        'addr': addr, 'size': size, 'sym': sym['name'],
                        'note': 'capstone not available - install with: pip install capstone'
                    }
                    continue

                try:
                    field_reads, call_reads, instructions = disassemble_getData(elf, addr, size, sym['name'])
                except Exception as e:
                    results[cls] = {'addr': addr, 'size': size, 'error': str(e)}
                    continue

                # Summarize the function
                total_insns = len(instructions)

                # Count read types
                read_summary = collections.Counter()
                for r in field_reads:
                    read_summary[r[0]] += 1

                # Find BL targets (function calls - likely readU32, readString, etc.)
                bl_targets = []
                for addr_bl, target in call_reads:
                    bl_targets.append(f"0x{int(target.replace('#', ''), 16) if target.startswith('#') else 0:X}" if target.startswith('#') else target)

                results[cls] = {
                    'addr': sym['value'],
                    'size': size,
                    'sym': sym['name'],
                    'total_insns': total_insns,
                    'field_reads': field_reads,
                    'read_summary': dict(read_summary),
                    'call_count': len(call_reads),
                    'bl_targets': bl_targets[:20],  # First 20 calls
                }
    return results


# ------------------------------------------------------------------------------
# PART B: PCAP PARSING
# ------------------------------------------------------------------------------

def read_pcap_ordered(filepath):
    """Parse PCAP and extract game protocol packets."""
    try:
        with open(filepath, 'rb') as f:
            magic_raw = f.read(4)
            if len(magic_raw) < 4:
                return []
            magic = struct.unpack('<I', magic_raw)[0]
            if magic == 0xa1b2c3d4:
                endian = '<'
            elif magic == 0xd4c3b2a1:
                endian = '>'
            else:
                return []
            f.read(20)  # rest of global header

            events = []
            c2s_buf = bytearray()
            s2c_buf = bytearray()

            game_ports = set(range(5990, 5999)) | set(range(7001, 7011))

            while True:
                hdr = f.read(16)
                if len(hdr) < 16:
                    break
                ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
                d = f.read(incl_len)
                if len(d) < incl_len:
                    break

                # Skip non-IP or too small
                # Check for Ethernet header (14 bytes) or raw IP
                ip_start = 0
                if len(d) > 14 and d[12:14] == b'\x08\x00':
                    ip_start = 14  # Ethernet
                elif len(d) > 4 and (d[0] >> 4) == 4:
                    ip_start = 0  # Raw IP
                elif len(d) > 4 and d[2:4] == b'\x08\x00':
                    ip_start = 4  # Linux cooked or SLL
                else:
                    continue

                ip = d[ip_start:]
                if len(ip) < 20:
                    continue
                if (ip[0] >> 4) != 4:
                    continue
                if ip[9] != 6:  # TCP
                    continue

                ihl = (ip[0] & 0x0F) * 4
                tcp = ip[ihl:]
                if len(tcp) < 20:
                    continue
                sp = struct.unpack('>H', tcp[0:2])[0]
                dp = struct.unpack('>H', tcp[2:4])[0]
                toff = ((tcp[12] >> 4) & 0xF) * 4
                pl = tcp[toff:]
                if not pl:
                    continue

                ts = ts_sec + ts_usec / 1e6

                if dp in game_ports:
                    c2s_buf.extend(pl)
                    while len(c2s_buf) >= 4:
                        pkt_len = struct.unpack('<H', c2s_buf[0:2])[0]
                        if pkt_len < 4 or pkt_len > 65535:
                            c2s_buf = c2s_buf[1:]
                            continue
                        if len(c2s_buf) < pkt_len:
                            break
                        opcode = struct.unpack('<H', c2s_buf[2:4])[0]
                        raw = bytes(c2s_buf[:pkt_len])
                        events.append((ts, 'C2S', opcode, raw))
                        c2s_buf = c2s_buf[pkt_len:]
                elif sp in game_ports:
                    s2c_buf.extend(pl)
                    while len(s2c_buf) >= 4:
                        pkt_len = struct.unpack('<H', s2c_buf[0:2])[0]
                        if pkt_len < 4 or pkt_len > 65535:
                            s2c_buf = s2c_buf[1:]
                            continue
                        if len(s2c_buf) < pkt_len:
                            break
                        opcode = struct.unpack('<H', s2c_buf[2:4])[0]
                        raw = bytes(s2c_buf[:pkt_len])
                        events.append((ts, 'S2C', opcode, raw))
                        s2c_buf = s2c_buf[pkt_len:]
        return events
    except Exception as e:
        return []

def collect_pcap_files():
    """Find all PCAP files."""
    files = []
    for d in PCAP_DIRS:
        if d.exists():
            for f in d.glob('*.pcap'):
                files.append(f)
    return files

def hex_dump(data, max_bytes=40):
    """Hex dump first N bytes."""
    return ' '.join(f'{b:02X}' for b in data[:max_bytes])

def parse_soldier_entry(data, offset=0):
    """Try multiple parsing strategies for 27-byte soldier entries."""
    if len(data) < offset + 27:
        return None

    chunk = data[offset:offset+27]

    strategies = {}

    # Strategy 1: u32 type, u16 tier, u32 count, u32 wounded, u32 ?, u32 ?, u8 ?
    # = 4+2+4+4+4+4+1 = 23... no, 27-23=4 leftover
    # Strategy 1: u32 type, u32 tier, u32 count, u32 wounded, u32 ?, u32 ?, u16 ?, u8 ?
    # = 4+4+4+4+4+4+2+1 = 27
    try:
        s1 = struct.unpack_from('<IIIIIIBB', chunk, 0)  # 4+4+4+4+4+4+1+1 = 26, need 27
    except:
        pass

    # Strategy A: u32 type_id, u32 subtype, u32 count, u32 wounded, u32 ?, u32 ?, u16 ?, u8 flags
    try:
        type_id = struct.unpack_from('<I', chunk, 0)[0]
        subtype = struct.unpack_from('<I', chunk, 4)[0]
        count = struct.unpack_from('<I', chunk, 8)[0]
        wounded = struct.unpack_from('<I', chunk, 12)[0]
        f5 = struct.unpack_from('<I', chunk, 16)[0]
        f6 = struct.unpack_from('<I', chunk, 20)[0]
        f7 = struct.unpack_from('<H', chunk, 24)[0]
        f8 = chunk[26]
        strategies['A: u32x6+u16+u8'] = {
            'type_id': type_id, 'subtype': subtype, 'count': count,
            'wounded': wounded, 'f5': f5, 'f6': f6, 'f7': f7, 'f8': f8
        }
    except:
        pass

    # Strategy B: u32 type, u16 tier, u32 count, u32 wounded, u32 training, u32 max, u16 ?, u8 ?
    # = 4+2+4+4+4+4+4+1 = 27
    try:
        type_id = struct.unpack_from('<I', chunk, 0)[0]
        tier = struct.unpack_from('<H', chunk, 4)[0]
        count = struct.unpack_from('<I', chunk, 6)[0]
        wounded = struct.unpack_from('<I', chunk, 10)[0]
        f5 = struct.unpack_from('<I', chunk, 14)[0]
        f6 = struct.unpack_from('<I', chunk, 18)[0]
        f7 = struct.unpack_from('<H', chunk, 22)[0]
        f8 = struct.unpack_from('<H', chunk, 24)[0]
        f9 = chunk[26]
        strategies['B: u32+u16+u32x4+u16x2+u8'] = {
            'type_id': type_id, 'tier': tier, 'count': count,
            'wounded': wounded, 'f5': f5, 'f6': f6, 'f7': f7, 'f8': f8, 'f9': f9
        }
    except:
        pass

    # Strategy C: u16 type, u8 tier, u32 count, u32 wounded, u32 ?, u32 ?, u32 ?, u16 ?
    # = 2+1+4+4+4+4+4+4 = 27
    try:
        type_id = struct.unpack_from('<H', chunk, 0)[0]
        tier = chunk[2]
        count = struct.unpack_from('<I', chunk, 3)[0]
        wounded = struct.unpack_from('<I', chunk, 7)[0]
        f5 = struct.unpack_from('<I', chunk, 11)[0]
        f6 = struct.unpack_from('<I', chunk, 15)[0]
        f7 = struct.unpack_from('<I', chunk, 19)[0]
        f8 = struct.unpack_from('<I', chunk, 23)[0]
        strategies['C: u16+u8+u32x6'] = {
            'type_id': type_id, 'tier': tier, 'count': count,
            'wounded': wounded, 'f5': f5, 'f6': f6, 'f7': f7, 'f8': f8
        }
    except:
        pass

    # Strategy D: u32 id, u8 type, u8 tier, u8 level, u32 count, u32 wounded, u32 ?, u32 ?, u32 ?
    # = 4+1+1+1+4+4+4+4+4 = 27
    try:
        sid = struct.unpack_from('<I', chunk, 0)[0]
        stype = chunk[4]
        stier = chunk[5]
        slevel = chunk[6]
        count = struct.unpack_from('<I', chunk, 7)[0]
        wounded = struct.unpack_from('<I', chunk, 11)[0]
        f5 = struct.unpack_from('<I', chunk, 15)[0]
        f6 = struct.unpack_from('<I', chunk, 19)[0]
        f7 = struct.unpack_from('<I', chunk, 23)[0]
        strategies['D: u32+u8x3+u32x5'] = {
            'id': sid, 'type': stype, 'tier': stier, 'level': slevel,
            'count': count, 'wounded': wounded, 'f5': f5, 'f6': f6, 'f7': f7
        }
    except:
        pass

    # Strategy E: u16 type, u16 tier, u8 level, u32 count, u32 wounded, u32 ?, u32 ?, u32 ?
    # = 2+2+1+4+4+4+4+4+2 = 27
    try:
        type_id = struct.unpack_from('<H', chunk, 0)[0]
        tier = struct.unpack_from('<H', chunk, 2)[0]
        level = chunk[4]
        count = struct.unpack_from('<I', chunk, 5)[0]
        wounded = struct.unpack_from('<I', chunk, 9)[0]
        f5 = struct.unpack_from('<I', chunk, 13)[0]
        f6 = struct.unpack_from('<I', chunk, 17)[0]
        f7 = struct.unpack_from('<I', chunk, 21)[0]
        f8 = struct.unpack_from('<H', chunk, 25)[0]
        strategies['E: u16x2+u8+u32x5+u16'] = {
            'type_id': type_id, 'tier': tier, 'level': level,
            'count': count, 'wounded': wounded, 'f5': f5, 'f6': f6, 'f7': f7, 'f8': f8
        }
    except:
        pass

    # Strategy F: All u32 except last 3 bytes (u16+u8)
    # u32 x6 = 24, then u16+u8 = 3, total 27
    try:
        vals = struct.unpack_from('<IIIIII', chunk, 0)
        last_u16 = struct.unpack_from('<H', chunk, 24)[0]
        last_u8 = chunk[26]
        strategies['F: u32x6+u16+u8'] = {
            'f1': vals[0], 'f2': vals[1], 'f3': vals[2],
            'f4': vals[3], 'f5': vals[4], 'f6': vals[5],
            'f7': last_u16, 'f8': last_u8
        }
    except:
        pass

    return chunk, strategies


# ------------------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------------------
def main():
    log("=" * 80)
    log("DEEP SERVER RESPONSE FORMAT ANALYSIS")
    log("=" * 80)

    # ------------------------------------------
    # PART A: Binary Analysis
    # ------------------------------------------
    log("\n" + "=" * 80)
    log("PART A: BINARY ANALYSIS OF libgame.so")
    log("=" * 80)

    elf = read_elf_data()
    log(f"\nLoaded libgame.so: {len(elf):,} bytes")
    log(f"DYNSTR offset: 0x{DYNSTR_OFF:X}")
    log(f"DYNSYM offset: 0x{DYNSYM_OFF:X}, size: 0x{DYNSYM_SIZE:X}")

    # Step 1: Parse all symbols
    log("\n--- Step 1: Finding all getData symbols ---")
    symbols = parse_dynsym(elf)
    log(f"Total dynsym entries parsed: {len(symbols)}")

    getData_syms = find_getData_symbols(symbols)
    log(f"Symbols containing 'getData': {len(getData_syms)}")

    # Group by class
    class_methods = {}
    for s in getData_syms:
        cls, method = demangle_simple(s['name'])
        if cls not in class_methods:
            class_methods[cls] = []
        class_methods[cls].append({
            'method': method,
            'addr': s['value'],
            'size': s['size'],
            'mangled': s['name'],
        })

    log(f"\nUnique classes with getData: {len(class_methods)}")
    log(f"\n{'Class Name':<55} {'Address':>12} {'Size':>8}")
    log("-" * 80)
    for cls in sorted(class_methods.keys()):
        for m in class_methods[cls]:
            log(f"  {cls:<53} 0x{m['addr']:08X} {m['size']:6d}B")

    # Step 2: Deep disassembly of key getData methods
    log("\n\n--- Step 2: Deep Disassembly of Key getData Methods ---")

    target_classes = [
        'CMSG_LOGIN_RETURN',
        'CMSG_ITEM_USE_RETURN',
        'CMSG_SYN_ATTRIBUTE',
        'CMSG_SYNC_MARCH',
        'CMSG_BUILDING_OPERAT_RETURN',
        'CMSG_TRAIN_SOLDIER',
        'CMSG_START_MARCH_RETURN',
        'CMSG_START_MARCH_NEW_RETURN',
        'CMSG_SOLDIER_INFO',
        'CMSG_SYN_EXTRA_ATTRIBUTE',
        'CMSG_HERO_INFO',
        'CMSG_SYN_SERVER_TIME',
        'CMSG_MARCH_STATE',
    ]

    detailed = analyze_getData_detailed(elf, getData_syms, target_classes)

    for cls, info in sorted(detailed.items()):
        log(f"\n{'-' * 70}")
        log(f"  {cls}::getData")
        log(f"  Address: 0x{info['addr']:08X}, Size: {info['size']}B")

        if 'note' in info:
            log(f"  NOTE: {info['note']}")
            continue
        if 'error' in info:
            log(f"  ERROR: {info['error']}")
            continue

        log(f"  Total instructions: {info.get('total_insns', '?')}")
        log(f"  Memory reads: {info.get('read_summary', {})}")
        log(f"  Function calls (BL): {info.get('call_count', '?')}")

        if info.get('field_reads'):
            log(f"  Field read pattern (first 30):")
            for rtype, raddr, rop in info['field_reads'][:30]:
                log(f"    0x{raddr:08X}: {rtype:4s}  {rop}")

        if info.get('bl_targets'):
            log(f"  Called functions (first 20):")
            for t in info['bl_targets'][:20]:
                log(f"    BL {t}")

    # Step 3: Find all _RETURN opcodes
    log("\n\n--- Step 3: All _RETURN Opcodes (Server Responses) ---")

    return_opcodes = {}
    non_return_server = {}

    for opcode, name in sorted(CMSG_OPCODES.items()):
        if '_RETURN' in name:
            return_opcodes[opcode] = name
        elif name.startswith('CMSG_SYN_') or name.startswith('CMSG_SYNC_'):
            non_return_server[opcode] = name

    # Categorize
    categories = collections.defaultdict(list)
    for opcode, name in sorted(return_opcodes.items()):
        # Extract category from name
        parts = name.replace('CMSG_', '').split('_')
        if len(parts) >= 2:
            cat = parts[0]
        else:
            cat = 'OTHER'

        # Better categorization
        upper = name.upper()
        if any(k in upper for k in ['LOGIN', 'ENTER_GAME', 'QUICK_LOGIN', 'USERINFO']):
            cat = 'AUTH/LOGIN'
        elif any(k in upper for k in ['BUILDING', 'BUILD']):
            cat = 'BUILDING'
        elif any(k in upper for k in ['TRAIN', 'SOLDIER', 'TROOP']):
            cat = 'TROOPS'
        elif any(k in upper for k in ['MARCH', 'ATTACK', 'RALLY']):
            cat = 'MARCH/COMBAT'
        elif any(k in upper for k in ['HERO']):
            cat = 'HERO'
        elif any(k in upper for k in ['ITEM', 'EQUIP', 'FORGE']):
            cat = 'ITEMS/EQUIP'
        elif any(k in upper for k in ['ALLIANCE', 'GUILD']):
            cat = 'ALLIANCE'
        elif any(k in upper for k in ['CHAT', 'MAIL']):
            cat = 'SOCIAL'
        elif any(k in upper for k in ['QUEST', 'TASK', 'ACHIEVEMENT', 'REWARD']):
            cat = 'QUESTS/REWARDS'
        elif any(k in upper for k in ['RESEARCH', 'TECH']):
            cat = 'RESEARCH'
        elif any(k in upper for k in ['SHOP', 'BUY', 'SELL', 'STORE']):
            cat = 'SHOP'
        elif any(k in upper for k in ['EVENT', 'ACTIVITY']):
            cat = 'EVENTS'
        elif any(k in upper for k in ['MONSTER', 'BOSS']):
            cat = 'MONSTERS'
        else:
            cat = 'OTHER'

        categories[cat].append((opcode, name))

    log(f"\nTotal _RETURN opcodes: {len(return_opcodes)}")
    log(f"Total SYN/SYNC opcodes: {len(non_return_server)}")

    for cat in sorted(categories.keys()):
        items = categories[cat]
        log(f"\n  [{cat}] ({len(items)} opcodes)")
        for opcode, name in items:
            log(f"    0x{opcode:04X} = {name}")

    log(f"\n  [SYN/SYNC - Server Push] ({len(non_return_server)} opcodes)")
    for opcode, name in sorted(non_return_server.items()):
        log(f"    0x{opcode:04X} = {name}")

    # ------------------------------------------
    # PART B: PCAP Analysis
    # ------------------------------------------
    log("\n\n" + "=" * 80)
    log("PART B: PCAP ANALYSIS OF SERVER RESPONSES")
    log("=" * 80)

    # Collect all PCAP files
    pcap_files = collect_pcap_files()
    log(f"\nFound {len(pcap_files)} PCAP files")

    # Parse PCAPs (limit to most useful ones for speed)
    # Prefer codex_lab and root-level ones
    priority_pcaps = []
    for f in pcap_files:
        if 'codex_lab' in str(f) or str(f.parent) == str(Path(r'D:\CascadeProjects')):
            priority_pcaps.append(f)

    # Limit to ~20 PCAPs for speed
    if len(priority_pcaps) > 25:
        priority_pcaps = priority_pcaps[:25]

    log(f"Scanning {len(priority_pcaps)} priority PCAPs...")

    # Collect all S2C packets by opcode
    s2c_by_opcode = collections.defaultdict(list)
    total_s2c = 0

    for pcap_file in priority_pcaps:
        try:
            events = read_pcap_ordered(pcap_file)
            for ts, direction, opcode, raw in events:
                if direction == 'S2C':
                    s2c_by_opcode[opcode].append((pcap_file.name, raw))
                    total_s2c += 1
        except Exception as e:
            pass

    log(f"Total S2C packets collected: {total_s2c}")
    log(f"Unique S2C opcodes seen: {len(s2c_by_opcode)}")

    # Step 4: Find _RETURN opcodes in PCAPs
    log("\n\n--- Step 4: _RETURN Opcodes Found in PCAPs ---")

    found_returns = []
    for opcode in sorted(return_opcodes.keys()):
        if opcode in s2c_by_opcode:
            samples = s2c_by_opcode[opcode]
            found_returns.append((opcode, return_opcodes[opcode], len(samples)))

    log(f"\n_RETURN opcodes with PCAP data: {len(found_returns)} / {len(return_opcodes)}")

    for opcode, name, count in found_returns:
        log(f"\n  0x{opcode:04X} = {name} ({count} samples)")
        # Show first sample
        sample = s2c_by_opcode[opcode][0][1]
        payload = sample[4:]  # skip len+opcode header
        log(f"    Total len: {len(sample)}, Payload len: {len(payload)}")
        log(f"    First 40B payload: {hex_dump(payload, 40)}")

        # Show payload size distribution
        sizes = [len(s[1]) - 4 for s in s2c_by_opcode[opcode]]
        if len(sizes) > 1:
            log(f"    Payload sizes: min={min(sizes)}, max={max(sizes)}, avg={sum(sizes)//len(sizes)}")

    # Step 5: Decode specific server responses
    log("\n\n--- Step 5: Detailed Decoding of Key Server Responses ---")

    for target_op in KEY_OPCODES:
        op_name = CMSG_OPCODES.get(target_op, f'UNKNOWN_0x{target_op:04X}')
        log(f"\n{'-' * 70}")
        log(f"  0x{target_op:04X} = {op_name}")

        if target_op not in s2c_by_opcode:
            log(f"  ** NOT FOUND in any PCAP **")
            continue

        samples = s2c_by_opcode[target_op]
        log(f"  Samples found: {len(samples)}")

        # Show up to 3 samples with detailed parsing
        for i, (fname, raw) in enumerate(samples[:3]):
            payload = raw[4:]
            log(f"\n  Sample {i+1} from {fname}:")
            log(f"    Total raw: {len(raw)}B, Payload: {len(payload)}B")
            log(f"    Hex: {hex_dump(payload, 60)}")

            # Attempt field parsing based on opcode
            if target_op == 0x0033:  # SYN_ATTRIBUTE_CHANGE
                # Typically: u16 count, then pairs of (u16 attr_id, u32/variable value)
                if len(payload) >= 2:
                    count = struct.unpack_from('<H', payload, 0)[0]
                    log(f"    Parsed: entry_count={count}")
                    off = 2
                    for j in range(min(count, 20)):
                        if off + 12 > len(payload):
                            # Try smaller entries
                            if off + 8 <= len(payload):
                                attr_id = struct.unpack_from('<I', payload, off)[0]
                                attr_val = struct.unpack_from('<I', payload, off + 4)[0]
                                log(f"      [{j}] id=0x{attr_id:04X}({attr_id}), val={attr_val}")
                                off += 8
                            elif off + 6 <= len(payload):
                                attr_id = struct.unpack_from('<H', payload, off)[0]
                                attr_val = struct.unpack_from('<I', payload, off + 2)[0]
                                log(f"      [{j}] id=0x{attr_id:04X}, val={attr_val}")
                                off += 6
                            else:
                                break
                        else:
                            # Try: u32 id, u32 type, u32 value format (12 bytes)
                            attr_id = struct.unpack_from('<I', payload, off)[0]
                            attr_type = struct.unpack_from('<I', payload, off + 4)[0]
                            attr_val = struct.unpack_from('<I', payload, off + 8)[0]
                            log(f"      [{j}] id=0x{attr_id:04X}({attr_id}), type={attr_type}, val={attr_val}")
                            off += 12

            elif target_op == 0x0043:  # SYN_SERVER_TIME
                if len(payload) >= 4:
                    ts_val = struct.unpack_from('<I', payload, 0)[0]
                    log(f"    Parsed: server_time={ts_val} (unix timestamp)")
                    import datetime
                    try:
                        dt = datetime.datetime.fromtimestamp(ts_val)
                        log(f"    Date: {dt}")
                    except:
                        pass
                if len(payload) >= 8:
                    ts2 = struct.unpack_from('<I', payload, 4)[0]
                    log(f"    field2={ts2}")

            elif target_op == 0x000C:  # LOGIN_RETURN
                if len(payload) >= 2:
                    result = struct.unpack_from('<H', payload, 0)[0]
                    log(f"    Parsed: result_code={result}")
                if len(payload) >= 4:
                    f2 = struct.unpack_from('<H', payload, 2)[0]
                    log(f"    field2=0x{f2:04X}")
                if len(payload) >= 8:
                    f3 = struct.unpack_from('<I', payload, 4)[0]
                    log(f"    field3=0x{f3:08X} ({f3})")
                # Dump more fields
                off = 8
                fidx = 4
                while off + 4 <= len(payload) and fidx < 20:
                    val = struct.unpack_from('<I', payload, off)[0]
                    log(f"    field{fidx}=0x{val:08X} ({val})")
                    off += 4
                    fidx += 1

            elif target_op == 0x0037:  # SYN_EXTRA_ATTRIBUTE_CHANGE
                if len(payload) >= 2:
                    count = struct.unpack_from('<H', payload, 0)[0]
                    log(f"    Parsed: entry_count={count}")
                    off = 2
                    for j in range(min(count, 15)):
                        if off + 12 <= len(payload):
                            attr_id = struct.unpack_from('<I', payload, off)[0]
                            attr_type = struct.unpack_from('<I', payload, off + 4)[0]
                            attr_val = struct.unpack_from('<I', payload, off + 8)[0]
                            log(f"      [{j}] id=0x{attr_id:04X}({attr_id}), type={attr_type}, val={attr_val}")
                            off += 12
                        else:
                            break

            elif target_op == 0x00B8:
                # Unknown ACK - try simple u16/u32 fields
                if len(payload) >= 2:
                    f1 = struct.unpack_from('<H', payload, 0)[0]
                    log(f"    field1=0x{f1:04X} ({f1})")
                if len(payload) >= 4:
                    f2 = struct.unpack_from('<H', payload, 2)[0]
                    log(f"    field2=0x{f2:04X} ({f2})")
                if len(payload) >= 8:
                    f3 = struct.unpack_from('<I', payload, 4)[0]
                    log(f"    field3=0x{f3:08X} ({f3})")

            elif target_op == 0x06C2:  # SOLDIER_INFO
                if len(payload) >= 4:
                    header = struct.unpack_from('<I', payload, 0)[0]
                    log(f"    Header u32: {header}")
                    # Or u16 count + u16 ?
                    count_h = struct.unpack_from('<H', payload, 0)[0]
                    f2_h = struct.unpack_from('<H', payload, 2)[0]
                    log(f"    Alt: count_u16={count_h}, field2_u16={f2_h}")

    # Step 6: SOLDIER_INFO deep analysis
    log("\n\n--- Step 6: SOLDIER_INFO (0x06C2) 27-Byte Entry Analysis ---")

    if 0x06C2 in s2c_by_opcode:
        samples = s2c_by_opcode[0x06C2]
        log(f"  Total SOLDIER_INFO packets: {len(samples)}")

        for i, (fname, raw) in enumerate(samples[:5]):
            payload = raw[4:]
            log(f"\n  Sample {i+1} from {fname}: {len(payload)}B payload")
            log(f"  Full hex: {hex_dump(payload, 120)}")

            # Try header parsing
            if len(payload) < 4:
                continue

            # Determine entry count
            # Assuming 4-byte header, rest is entries
            entry_size = 27

            # Try different header sizes
            for hdr_size in [2, 4]:
                body = payload[hdr_size:]
                if len(body) % entry_size == 0 and len(body) >= entry_size:
                    n_entries = len(body) // entry_size
                    hdr_val = struct.unpack_from('<H' if hdr_size == 2 else '<I', payload, 0)[0]
                    log(f"\n  Header={hdr_size}B (val={hdr_val}), {n_entries} entries of {entry_size}B")

                    for eidx in range(min(n_entries, 6)):
                        entry_off = hdr_size + eidx * entry_size
                        entry_data = payload[entry_off:entry_off + entry_size]
                        log(f"\n    Entry {eidx}: {hex_dump(entry_data, 27)}")

                        chunk, strategies = parse_soldier_entry(payload, entry_off)
                        for strat_name, fields in strategies.items():
                            # Check if values are reasonable
                            reasonable = True
                            notes = []
                            for k, v in fields.items():
                                if 'count' in k and (v > 10000000 or v < 0):
                                    reasonable = False
                                if 'type' in k.lower() and v > 100000:
                                    notes.append(f"{k} seems high")
                                if 'tier' in k.lower() and v > 20:
                                    notes.append(f"{k} > 20")

                            flag = " <<LIKELY" if reasonable and not notes else ""
                            log(f"      [{strat_name}]{flag}")
                            for k, v in fields.items():
                                if isinstance(v, int) and v > 255:
                                    log(f"        {k}: {v} (0x{v:X})")
                                else:
                                    log(f"        {k}: {v}")
    else:
        log("  ** 0x06C2 NOT FOUND in PCAPs **")
        # Try to find any soldier-related opcodes
        soldier_ops = [op for op in s2c_by_opcode if CMSG_OPCODES.get(op, '').upper().find('SOLDIER') >= 0]
        if soldier_ops:
            log(f"  Found other soldier opcodes: {[f'0x{op:04X}' for op in soldier_ops]}")

    # ------------------------------------------
    # SUMMARY: Opcode frequency in PCAPs
    # ------------------------------------------
    log("\n\n--- BONUS: Top 50 Most Frequent S2C Opcodes ---")
    freq = [(op, len(pkts)) for op, pkts in s2c_by_opcode.items()]
    freq.sort(key=lambda x: -x[1])

    log(f"\n{'Opcode':>8} {'Count':>6} {'Name':<50} {'Avg Size':>8}")
    log("-" * 80)
    for op, cnt in freq[:50]:
        name = CMSG_OPCODES.get(op, '???')
        avg_sz = sum(len(p[1]) - 4 for p in s2c_by_opcode[op]) // cnt
        log(f"  0x{op:04X} {cnt:6d} {name:<50} {avg_sz:6d}B")

    # ------------------------------------------
    # SAVE REPORT
    # ------------------------------------------
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write("# Deep Server Response Format Analysis\n\n")
        f.write("```\n")
        f.write('\n'.join(report))
        f.write("\n```\n")

    log(f"\n\nReport saved to: {OUTPUT}")

if __name__ == '__main__':
    main()

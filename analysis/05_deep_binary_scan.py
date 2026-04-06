"""
Phase 5: Deep binary scan
- Find the CMSG_TABLE (0x58,0xef,0xd7,0x14,0xa2,0x3b,0x9c)
- Find CQ_secret string
- Find opcode dispatch table
- Find GoSocket::sendData internals
- Disassemble key functions around encode/decode
"""
import struct, re, sys
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection

SO_PATH = r"D:\CascadeProjects\libgame.so"

def find_section(elf, name):
    for s in elf.iter_sections():
        if s.name == name:
            return s
    return None

def main():
    with open(SO_PATH, 'rb') as f:
        raw = f.read()

    with open(SO_PATH, 'rb') as f:
        elf = ELFFile(f)
        text_sec = find_section(elf, '.text')
        rodata_sec = find_section(elf, '.rodata')
        data_sec = find_section(elf, '.data')
        data_rel_ro = find_section(elf, '.data.rel.ro')

        text_offset = text_sec['sh_offset'] if text_sec else 0
        text_size = text_sec['sh_size'] if text_sec else 0
        text_addr = text_sec['sh_addr'] if text_sec else 0

        rodata_offset = rodata_sec['sh_offset'] if rodata_sec else 0
        rodata_size = rodata_sec['sh_size'] if rodata_sec else 0

    # ═══ 1. Find CMSG_TABLE bytes ═══
    print("=" * 80)
    print("1. CMSG_TABLE (encryption table)")
    print("=" * 80)
    table = bytes([0x58, 0xef, 0xd7, 0x14, 0xa2, 0x3b, 0x9c])
    pos = 0
    count = 0
    while True:
        idx = raw.find(table, pos)
        if idx < 0: break
        # Show surrounding context
        ctx_start = max(0, idx - 16)
        ctx_end = min(len(raw), idx + len(table) + 16)
        ctx = raw[ctx_start:ctx_end]
        section = "unknown"
        if text_offset <= idx < text_offset + text_size: section = ".text"
        elif rodata_offset <= idx < rodata_offset + rodata_size: section = ".rodata"
        print(f"  Found at offset 0x{idx:08X} ({section})")
        print(f"    Context: {ctx.hex()}")
        # Show extended context (32 bytes before and after)
        ext_start = max(0, idx - 32)
        ext_end = min(len(raw), idx + len(table) + 64)
        ext = raw[ext_start:ext_end]
        print(f"    Extended ({ext_end-ext_start}B): {ext.hex()}")
        count += 1
        pos = idx + 1
    print(f"  Total: {count} occurrences")

    # ═══ 2. Find CQ_secret string ═══
    print("\n" + "=" * 80)
    print("2. CQ_secret and related strings")
    print("=" * 80)
    for needle in [b'CQ_secret', b'CQ_sec', b'cq_secret', b'CQ_']:
        pos = 0
        while True:
            idx = raw.find(needle, pos)
            if idx < 0: break
            ctx = raw[max(0, idx-16):min(len(raw), idx+64)]
            print(f"  '{needle.decode()}' at 0x{idx:08X}: {ctx}")
            pos = idx + 1

    # ═══ 3. Find opcode constant 0x1B8B in immediate values ═══
    print("\n" + "=" * 80)
    print("3. Key opcode references in code")
    print("=" * 80)

    # Search for 0x1B8B (7051 decimal) as LE u16
    needle_1b8b = struct.pack('<H', 0x1B8B)
    offsets_1b8b = []
    pos = 0
    while len(offsets_1b8b) < 20:
        idx = raw.find(needle_1b8b, pos)
        if idx < 0: break
        if text_offset <= idx < text_offset + text_size:
            offsets_1b8b.append(idx)
        pos = idx + 1

    print(f"  0x1B8B in .text: {len(offsets_1b8b)} occurrences")
    for o in offsets_1b8b[:5]:
        print(f"    0x{o:08X}")

    # Same for other key opcodes
    for opcode, name in [(0x0CE8, 'START_MARCH'), (0x0CED, 'TRAIN'), (0x0CEF, 'BUILD'),
                          (0x001F, 'GAME_LOGIN'), (0x0038, 'INIT_DATA'), (0x1B8B, 'SESSION')]:
        needle = struct.pack('<H', opcode)
        count = 0
        first_text = []
        pos = 0
        while True:
            idx = raw.find(needle, pos)
            if idx < 0: break
            if text_offset <= idx < text_offset + text_size:
                count += 1
                if len(first_text) < 3:
                    first_text.append(idx)
            pos = idx + 1
        print(f"  0x{opcode:04X} ({name}): {count} in .text, first: {[hex(x) for x in first_text]}")

    # ═══ 4. GoSocket::sendData disassembly ═══
    print("\n" + "=" * 80)
    print("4. GoSocket::sendData DISASSEMBLY")
    print("=" * 80)

    # Find the symbol
    with open(SO_PATH, 'rb') as f:
        elf2 = ELFFile(f)
        send_addr = None
        send_size = 0
        for s in elf2.iter_sections():
            if isinstance(s, SymbolTableSection):
                for sym in s.iter_symbols():
                    if 'GoSocket' in sym.name and 'sendData' in sym.name:
                        send_addr = sym['st_value']
                        send_size = sym['st_size']
                        print(f"  Found: {sym.name} at 0x{send_addr:016X} size={send_size}")

    if send_addr and send_size > 0:
        # Convert VA to file offset
        file_offset = send_addr  # For shared objects, VA ≈ file offset usually
        # Actually need to use segments
        with open(SO_PATH, 'rb') as f:
            elf3 = ELFFile(f)
            for seg in elf3.iter_segments():
                if seg['p_type'] == 'PT_LOAD' and seg['p_flags'] & 1:  # executable
                    if seg['p_vaddr'] <= send_addr < seg['p_vaddr'] + seg['p_memsz']:
                        file_offset = send_addr - seg['p_vaddr'] + seg['p_offset']
                        break

        code = raw[file_offset:file_offset + min(send_size, 512)]
        md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
        md.detail = True

        print(f"  Disassembly (offset=0x{file_offset:X}, VA=0x{send_addr:X}):")
        for insn in md.disasm(code, send_addr):
            print(f"    0x{insn.address:X}: {insn.mnemonic}\t{insn.op_str}")

    # ═══ 5. Find GoSocket::connectSocket ═══
    print("\n" + "=" * 80)
    print("5. GoSocket::connectSocket DISASSEMBLY")
    print("=" * 80)

    with open(SO_PATH, 'rb') as f:
        elf4 = ELFFile(f)
        conn_addr = None
        conn_size = 0
        for s in elf4.iter_sections():
            if isinstance(s, SymbolTableSection):
                for sym in s.iter_symbols():
                    if 'GoSocket' in sym.name and 'connectSocket' in sym.name:
                        conn_addr = sym['st_value']
                        conn_size = sym['st_size']
                        print(f"  Found: {sym.name} at 0x{conn_addr:016X} size={conn_size}")

    if conn_addr and conn_size > 0:
        with open(SO_PATH, 'rb') as f:
            elf5 = ELFFile(f)
            for seg in elf5.iter_segments():
                if seg['p_type'] == 'PT_LOAD' and seg['p_flags'] & 1:
                    if seg['p_vaddr'] <= conn_addr < seg['p_vaddr'] + seg['p_memsz']:
                        file_offset = conn_addr - seg['p_vaddr'] + seg['p_offset']
                        break

        code = raw[file_offset:file_offset + min(conn_size, 1024)]
        md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
        for insn in md.disasm(code, conn_addr):
            print(f"    0x{insn.address:X}: {insn.mnemonic}\t{insn.op_str}")

    # ═══ 6. Search for XOR patterns and magic constants ═══
    print("\n" + "=" * 80)
    print("6. XOR constants & magic values in .rodata")
    print("=" * 80)

    # 0xB7 (verify byte XOR constant)
    needle_b7 = b'\xb7'
    # Search for patterns like the table + 0xB7
    combined = bytes([0x58, 0xef, 0xd7, 0x14, 0xa2, 0x3b, 0x9c, 0xb7])
    idx = raw.find(combined)
    if idx >= 0:
        print(f"  TABLE+0xB7 found at 0x{idx:08X}")
    else:
        print(f"  TABLE+0xB7 not found as contiguous")

    # Search for 17 (mul constant in encryption)
    # Look for MUL/MADD instructions near known encryption code
    # The encryption formula: enc[i] = ((plain[i] + msg*17) ^ sk ^ tbl) & 0xFF

    print(f"\n  Searching for 0x11 (17) near table locations...")
    for table_off in [idx for idx in [raw.find(table)] if idx >= 0]:
        # Look in .text for references near this data
        nearby = raw[max(0, table_off-256):table_off+256]
        for i, b in enumerate(nearby):
            if b == 0x11:
                abs_off = max(0, table_off-256) + i
                print(f"    0x11 at 0x{abs_off:08X} (relative to table: {i-256})")

    # ═══ 7. Find all exported JNI functions ═══
    print("\n" + "=" * 80)
    print("7. JNI Functions (Java -> Native)")
    print("=" * 80)

    with open(SO_PATH, 'rb') as f:
        elf6 = ELFFile(f)
        jni_funcs = []
        for s in elf6.iter_sections():
            if isinstance(s, SymbolTableSection):
                for sym in s.iter_symbols():
                    if sym.name.startswith('Java_'):
                        jni_funcs.append((sym['st_value'], sym['st_size'], sym.name))

    jni_funcs.sort()
    print(f"  Total JNI functions: {len(jni_funcs)}")
    for addr, size, name in jni_funcs:
        print(f"    0x{addr:016X}  {size:8d}  {name}")


if __name__ == '__main__':
    main()

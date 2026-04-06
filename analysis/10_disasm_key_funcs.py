"""
Phase 10: Disassemble around key opcode MOVZ locations.
Focus on: 0x1B8B (session), 0x0CE8 (start_march), CMsgCodec, doDecode
"""
import struct, sys
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
from elftools.elf.elffile import ELFFile

SO_PATH = r"D:\CascadeProjects\libgame.so"

def disasm_at(raw, va, text_off, text_addr, count=40, label=""):
    """Disassemble `count` instructions starting at VA."""
    file_off = va - text_addr + text_off
    code = raw[file_off:file_off + count * 4]
    md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
    md.detail = True

    print(f"\n  --- {label} @ 0x{va:X} ---")
    for insn in md.disasm(code, va):
        print(f"    0x{insn.address:X}: {insn.mnemonic}\t{insn.op_str}")

def main():
    with open(SO_PATH, 'rb') as f:
        raw = f.read()

    with open(SO_PATH, 'rb') as f:
        elf = ELFFile(f)
        for s in elf.iter_sections():
            if s.name == '.text':
                text_off = s['sh_offset']
                text_size = s['sh_size']
                text_addr = s['sh_addr']

    # ═══ 1. 0x1B8B session packet handler ═══
    print("=" * 80)
    print("1. 0x1B8B SESSION PACKET (MOVZ W3, #0x1B8B at 0x58EA650)")
    print("=" * 80)
    # Show wide context: 60 instructions before and 60 after
    disasm_at(raw, 0x58EA650 - 120, text_off, text_addr, 120,
              "Context around MOVZ W3, #0x1B8B")

    # ═══ 2. 0x0CE8 START_MARCH locations ═══
    print("\n\n" + "=" * 80)
    print("2. 0x0CE8 START_MARCH")
    print("=" * 80)
    for va in [0x555FE3C, 0x5566714, 0x5566B68]:
        disasm_at(raw, va - 48, text_off, text_addr, 40,
                  f"Context around MOVZ #0xCE8 at 0x{va:X}")

    # ═══ 3. 0x02F2 SESSION_ERROR ═══
    print("\n\n" + "=" * 80)
    print("3. 0x02F2 SESSION_ERROR")
    print("=" * 80)
    for va in [0x34A4A84, 0x593F154]:
        disasm_at(raw, va - 48, text_off, text_addr, 40,
                  f"Context around MOVZ #0x2F2 at 0x{va:X}")

    # ═══ 4. CMsgCodec reference ═══
    print("\n\n" + "=" * 80)
    print("4. CMsgCodec string reference")
    print("=" * 80)
    # Found at 0x006C9BA1 in raw. Find code that references this
    print("  String 'CMsgCodec' at raw offset 0x006C9BA1")
    # This is in .dynstr section (string table). Look for actual code.

    # Search for 'doDecode' in the binary
    idx_decode = raw.find(b'doDecode')
    print(f"  'doDecode' at 0x{idx_decode:08X}")

    # Look at 0x0108A269 (doDecode string location)
    # This is in .rodata. Let's find code referencing nearby pages
    decode_page = 0x0108A269 & ~0xFFF
    print(f"  doDecode page: 0x{decode_page:08X}")

    # ═══ 5. sendMsg reference ═══
    print("\n\n" + "=" * 80)
    print("5. 'sendMsg' at 0x00684FFF")
    print("=" * 80)
    # Look at bytes around sendMsg
    idx = 0x00684FFF
    ctx = raw[idx-32:idx+64]
    # Extract readable strings
    strs = []
    cur = b""
    for b in ctx:
        if 32 <= b < 127:
            cur += bytes([b])
        else:
            if len(cur) > 3:
                strs.append(cur.decode())
            cur = b""
    if cur and len(cur) > 3:
        strs.append(cur.decode())
    print(f"  Nearby strings: {strs}")

    # ═══ 6. 0x0CE7 CANCEL_MARCH ═══
    print("\n\n" + "=" * 80)
    print("6. 0x0CE7 CANCEL_MARCH")
    print("=" * 80)
    disasm_at(raw, 0x5AFE404 - 48, text_off, text_addr, 40,
              "Context around MOVZ #0xCE7")

    # ═══ 7. 0x033E SEARCH_TILE ═══
    print("\n\n" + "=" * 80)
    print("7. 0x033E SEARCH_TILE")
    print("=" * 80)
    disasm_at(raw, 0x5AC2EF8 - 48, text_off, text_addr, 40,
              "Context around MOVZ #0x33E")

    # ═══ 8. 0x0AF2 ═══
    print("\n\n" + "=" * 80)
    print("8. 0x0AF2 UNK_0AF2")
    print("=" * 80)
    disasm_at(raw, 0x5953140 - 48, text_off, text_addr, 40,
              "Context around MOVZ #0xAF2")


if __name__ == '__main__':
    main()

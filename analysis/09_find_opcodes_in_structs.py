"""
Phase 9: Find opcode values for CMSG structs.
Strategy: CMSG structs have a static opcode member. In C++ compiled code,
this shows up as a constant near the struct's typeinfo or vtable.
Alternative: look at *_RECV/*_SEND logging strings with nearby constants.
"""
import re, struct, sys

SO_PATH = r"D:\CascadeProjects\libgame.so"

def main():
    with open(SO_PATH, 'rb') as f:
        raw = f.read()

    # ═══ 1. Find *_RECV and *_SEND strings ═══
    print("=" * 80)
    print("1. ALL *_RECV / *_SEND LOGGING STRINGS")
    print("=" * 80)

    # These are bare strings (not CMSG_ prefixed) used in logging
    recv_send = re.compile(rb'[A-Z][A-Z_]{5,}_(?:RECV|SEND)\x00')
    found = []
    for m in recv_send.finditer(raw):
        name = m.group()[:-1].decode()  # strip null
        off = m.start()
        found.append((off, name))

    found.sort(key=lambda x: x[1])
    print(f"  Found {len(found)} strings:")
    for off, name in found:
        print(f"    0x{off:08X}: {name}")

    # ═══ 2. Look for opcode values near these strings ═══
    print("\n" + "=" * 80)
    print("2. OPCODES NEAR RECV/SEND STRINGS")
    print("=" * 80)

    # For each string, look at surrounding data for u16 opcode-like values
    for off, name in found[:30]:
        # Look 128 bytes before and after
        region_start = max(0, off - 128)
        region_end = min(len(raw), off + len(name) + 128)
        region = raw[region_start:region_end]
        # Find all u16 values that could be opcodes (0x0001-0x2FFF)
        opcodes_near = []
        for i in range(0, len(region) - 1, 2):
            val = struct.unpack('<H', region[i:i+2])[0]
            if 0x0020 <= val <= 0x2FFF and val not in opcodes_near:
                abs_pos = region_start + i
                opcodes_near.append((val, abs_pos))

    # ═══ 3. Better approach: Find the CMsgCodec initialization ═══
    # The CMSG_TABLE [0x58,0xef,0xd7,0x14,0xa2,0x3b,0x9c] is at 0x028B723A
    # Find code that references this address
    print("\n" + "=" * 80)
    print("3. CMSG_TABLE USAGE (references to 0x028B723A)")
    print("=" * 80)

    table_addr = 0x028B723A
    # In ARM64, this would be loaded via ADRP + ADD/LDR
    # ADRP calculates page address, so we look for the page
    page = table_addr & ~0xFFF  # 0x028B7000
    offset_in_page = table_addr & 0xFFF  # 0x23A

    print(f"  Table addr: 0x{table_addr:08X}")
    print(f"  Page:       0x{page:08X}")
    print(f"  Offset:     0x{offset_in_page:03X}")

    # Search for the offset 0x23A as a 12-bit immediate in ADD instructions
    # ADD Xd, Xn, #0x23A -> look for this in .text
    # But this is complex. Let's try another approach.

    # ═══ 4. Find the CMSG struct opcode through vtable scanning ═══
    print("\n" + "=" * 80)
    print("4. SEARCHING FOR OPCODE REGISTRATION PATTERN")
    print("=" * 80)

    # The game likely has a function like:
    # GoSocket::registerHandler(uint16_t opcode, handler_func)
    # or: MessageSubject::registerListener<T>(callback)
    # where T::OPCODE is a compile-time constant

    # Let's search for sequences of known opcodes in code
    # If the game registers handlers, opcodes might appear as MOV Wn, #opcode
    # or as immediate loads

    # For ARM64, MOVZ Wd, #imm16 encoding:
    # 0101_0010_100x_xxxx_xxxx_xxxx_xxxx_xxxx
    # bits 20:5 = imm16, bits 4:0 = Rd

    from elftools.elf.elffile import ELFFile
    with open(SO_PATH, 'rb') as f2:
        elf = ELFFile(f2)
        for s in elf.iter_sections():
            if s.name == '.text':
                text_off = s['sh_offset']
                text_size = s['sh_size']
                text_addr = s['sh_addr']

    text = raw[text_off:text_off + text_size]

    # Scan for MOVZ instructions with known opcodes
    targets = {
        0x0CE8: 'START_MARCH', 0x0CE7: 'CANCEL_MARCH',
        0x0CED: 'TRAIN', 0x0CEE: 'RESEARCH', 0x0CEF: 'BUILD',
        0x0CEB: 'ENABLE_VIEW', 0x1B8B: 'SESSION_PKT',
        0x0038: 'INIT_DATA', 0x0042: 'HEARTBEAT',
        0x0071: 'MARCH_STATE', 0x00B8: 'MARCH_ACK',
        0x06C2: 'SOLDIER_INFO', 0x0323: 'HERO_SELECT',
        0x033E: 'SEARCH_TILE', 0x02F2: 'SESSION_ERROR',
        0x0840: 'UNK_0840', 0x0834: 'FORMATION_SET',
        0x0AF2: 'UNK_0AF2', 0x17D4: 'UNK_17D4',
        0x099D: 'TROOP_QUERY', 0x1C87: 'UNK_1C87',
    }

    print(f"\n  Scanning {text_size:,} bytes of .text for MOVZ Wd, #opcode...")

    for target_op, target_name in sorted(targets.items()):
        # MOVZ Wd, #imm: 0101_0010_1000_xxxx_xxxx_xxxx_xxxd_dddd
        # Encoding: 0x52800000 | (imm16 << 5)
        expected = 0x52800000 | (target_op << 5)
        mask = 0xFFFFFFE0  # mask out Rd (bits 0-4)

        locations = []
        for i in range(0, len(text) - 4, 4):
            word = struct.unpack('<I', text[i:i+4])[0]
            if (word & mask) == (expected & mask):
                rd = word & 0x1F
                va = text_addr + i
                locations.append((va, rd))

        if locations:
            print(f"\n  0x{target_op:04X} ({target_name}): {len(locations)} MOVZ locations")
            for va, rd in locations[:5]:
                print(f"    0x{va:X}: MOVZ W{rd}, #0x{target_op:X}")

    # ═══ 5. Find GoSocket send function - trace what opcode it uses ═══
    print("\n" + "=" * 80)
    print("5. FIND 'sendMsg' / 'sendPacket' PATTERNS")
    print("=" * 80)

    # Search for strings like "sendMsg", "sendPacket", "sendData", "onRecv"
    for needle in [b'sendMsg', b'sendPacket', b'sendData', b'onRecv', b'onMessage',
                   b'processMessage', b'dispatchMessage', b'handleMessage',
                   b'registerHandler', b'registerListener',
                   b'GoSocket', b'CMsgCodec', b'doDecode', b'doEncode',
                   b'onPacket', b'recvPacket']:
        idx = raw.find(needle)
        if idx >= 0:
            ctx = raw[max(0, idx-16):min(len(raw), idx+64)]
            print(f"  '{needle.decode()}' at 0x{idx:08X}")

if __name__ == '__main__':
    main()

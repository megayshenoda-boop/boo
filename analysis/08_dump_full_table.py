"""
Phase 8: Dump the FULL opcode dispatch table from libgame.so.
Table found at ~0x028BE37A, 8-byte entries, sorted descending by opcode.
Format: [u16 opcode][4B zeros][u8 data1][u8 index]
"""
import struct, sys

SO_PATH = r"D:\CascadeProjects\libgame.so"

def main():
    with open(SO_PATH, 'rb') as f:
        raw = f.read()

    # Known anchor: 0x0CEF at offset 0x028BE3FA
    # Table has 8-byte entries, opcodes descending
    # Find table boundaries by scanning backwards and forwards

    anchor = 0x028BE3FA

    # Scan backwards to find table start
    pos = anchor
    while pos >= 8:
        pos -= 8
        entry = raw[pos:pos+8]
        opcode = struct.unpack('<H', entry[0:2])[0]
        mid = struct.unpack('<I', entry[2:6])[0]
        # Table entries have mid=0 and valid opcode
        if mid != 0 or opcode > 0xFFFF or opcode == 0:
            pos += 8  # went too far
            break

    table_start = pos
    print(f"Table start: 0x{table_start:08X}")

    # Scan forward to find table end
    pos = anchor
    while pos < len(raw) - 8:
        pos += 8
        entry = raw[pos:pos+8]
        opcode = struct.unpack('<H', entry[0:2])[0]
        mid = struct.unpack('<I', entry[2:6])[0]
        if mid != 0 or opcode == 0:
            break

    table_end = pos
    print(f"Table end:   0x{table_end:08X}")

    num_entries = (table_end - table_start) // 8
    print(f"Entries:     {num_entries}")

    # Known opcodes for annotation
    known = {
        0x000B: 'GATEWAY_AUTH', 0x000C: 'GATEWAY_REDIRECT',
        0x001F: 'GAME_LOGIN', 0x0020: 'LOGIN_RETURN',
        0x0021: 'ENTER_GAME', 0x0022: 'ENTER_GAME_RETURN',
        0x0033: 'SYN_ATTRIBUTE', 0x0037: 'TIMESTAMP', 0x0038: 'INIT_DATA',
        0x0042: 'HEARTBEAT', 0x0043: 'HEARTBEAT2',
        0x006E: 'SET_VIEW', 0x0071: 'MARCH_STATE',
        0x0076: 'MAP_TILE', 0x0077: 'MAP_DATA', 0x0078: 'MAP_DATA2',
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
        0x11FF: 'UNK_11FF', 0x0674: 'UNK_0674',
        0x0245: 'UNK_0245', 0x0767: 'UNK_0767', 0x0769: 'UNK_0769',
        0x01D6: 'UNK_01D6',
    }

    # Dump all entries
    print(f"\n{'='*80}")
    print(f"FULL OPCODE DISPATCH TABLE ({num_entries} entries)")
    print(f"{'='*80}")
    print(f"{'Offset':>12} {'Opcode':>8} {'Mid':>10} {'D1':>4} {'D2':>4}  {'Name'}")
    print(f"{'-'*12} {'-'*8} {'-'*10} {'-'*4} {'-'*4}  {'-'*30}")

    entries = []
    for i in range(num_entries):
        off = table_start + i * 8
        entry = raw[off:off+8]
        opcode = struct.unpack('<H', entry[0:2])[0]
        mid = struct.unpack('<I', entry[2:6])[0]
        d1 = entry[6]
        d2 = entry[7]
        name = known.get(opcode, '')
        entries.append((opcode, mid, d1, d2, name))
        marker = ' <<<' if name else ''
        print(f"  0x{off:08X}  0x{opcode:04X}  0x{mid:08X}  0x{d1:02X}  0x{d2:02X}  {name}{marker}")

    # Sort by opcode for reference
    print(f"\n{'='*80}")
    print(f"SORTED BY OPCODE (ascending)")
    print(f"{'='*80}")
    for opcode, mid, d1, d2, name in sorted(entries):
        marker = ' <<<' if name else ''
        print(f"  0x{opcode:04X}  d1=0x{d1:02X} d2=0x{d2:02X}  {name}{marker}")

    # Write to file
    with open(r'D:\CascadeProjects\analysis\opcode_table.txt', 'w') as f:
        f.write(f"# Opcode Dispatch Table from libgame.so\n")
        f.write(f"# {num_entries} entries, sorted ascending\n\n")
        for opcode, mid, d1, d2, name in sorted(entries):
            f.write(f"0x{opcode:04X}  d1=0x{d1:02X}  d2=0x{d2:02X}  {name}\n")
    print(f"\nWritten to analysis/opcode_table.txt")


if __name__ == '__main__':
    main()

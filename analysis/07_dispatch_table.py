"""
Phase 7: Find and dump the opcode dispatch table.
Found a pattern at 0x028BE3FA: entries of [opcode:2][4B][index:2] = 8 bytes each.
"""
import struct, sys, re

SO_PATH = r"D:\CascadeProjects\libgame.so"

def main():
    with open(SO_PATH, 'rb') as f:
        raw = f.read()

    # Known opcode 0x0CEF at offset 0x028BE3FA
    # Let's look at the region around it to find the table start/end
    anchor = 0x028BE3FA
    # Read a wide region
    region_start = anchor - 4096
    region_end = anchor + 4096
    region = raw[region_start:region_end]

    # ═══ Strategy 1: 8-byte entries with opcode at offset 0 ═══
    print("=" * 80)
    print("OPCODE DISPATCH TABLE (8-byte entries)")
    print("=" * 80)

    # Scan for table pattern: consecutive entries where bytes[2:6] == 00000000
    # and bytes[0:2] is a valid opcode (< 0x3000)
    # and bytes[6:8] has incrementing values

    # Let's first understand the exact structure by looking at known anchor
    print(f"\nAnchor area (offset 0x{anchor:08X}):")
    for i in range(-40, 48, 8):
        off = anchor + i
        chunk = raw[off:off+8]
        if len(chunk) == 8:
            op = struct.unpack('<H', chunk[0:2])[0]
            mid = struct.unpack('<I', chunk[2:6])[0]
            idx = struct.unpack('<H', chunk[6:8])[0]
            marker = " <<<" if i == 0 else ""
            print(f"  0x{off:08X}: op=0x{op:04X} mid=0x{mid:08X} idx=0x{idx:04X}{marker}")

    # ═══ Strategy 2: Search for any table-like structure ═══
    # Look for sequences where opcode values are reasonable and mid bytes are structured
    print("\n" + "=" * 80)
    print("SEARCHING FOR TABLE PATTERNS")
    print("=" * 80)

    # Alternative pattern: maybe entries are different size
    # Let's look at the raw hex around the anchor more carefully
    for chunk_size in [6, 7, 8, 10, 12]:
        print(f"\n  Trying {chunk_size}-byte entries at anchor:")
        for i in range(-3, 4):
            off = anchor + i * chunk_size
            chunk = raw[off:off+chunk_size]
            print(f"    0x{off:08X}: {chunk.hex()}")

    # ═══ Strategy 3: Better pattern - look at raw bytes ═══
    print("\n" + "=" * 80)
    print("RAW HEX DUMP around anchor (256 bytes)")
    print("=" * 80)

    dump_start = anchor - 128
    for i in range(0, 256, 16):
        off = dump_start + i
        chunk = raw[off:off+16]
        hex_str = ' '.join(f'{b:02x}' for b in chunk)
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        marker = " <<<" if off <= anchor < off + 16 else ""
        print(f"  0x{off:08X}: {hex_str}  {ascii_str}{marker}")

    # ═══ Strategy 4: The table might have variable-length entries ═══
    # Let's look for a pattern: 2-byte opcode followed by string name
    # Many game engines store [opcode][string] pairs
    print("\n" + "=" * 80)
    print("LOOKING FOR [opcode][padding][string] PATTERN")
    print("=" * 80)

    # Search for known CMSG names preceded by their opcode
    known_pairs = [
        (0x0CEF, b'BUILD'),
        (0x0CE8, b'MARCH'),
        (0x0CED, b'TRAIN'),
        (0x1B8B, b'SESSION'),
    ]

    for opcode, name_part in known_pairs:
        needle_le = struct.pack('<H', opcode)
        pos = 0
        while True:
            idx = raw.find(needle_le, pos)
            if idx < 0: break
            # Check if there's a readable string nearby (within 32 bytes)
            nearby = raw[idx:idx+64]
            if name_part in nearby:
                print(f"  0x{opcode:04X} + '{name_part.decode()}' at 0x{idx:08X}:")
                print(f"    {nearby}")
            pos = idx + 1

    # ═══ Strategy 5: Find the CMSG_TABLE opcode dispatch ═══
    # The real dispatch is probably a switch/case or a sorted array
    # In ARM64, this often uses a jump table
    # Let's look for the pattern differently - find where all opcodes are
    # stored consecutively

    print("\n" + "=" * 80)
    print("CONSECUTIVE OPCODE PAIRS IN .rodata")
    print("=" * 80)

    # Look for regions where multiple known opcodes appear within 200 bytes
    known_ops_bytes = {struct.pack('<H', op): name for op, name in [
        (0x0CE8, 'START_MARCH'), (0x0CE7, 'CANCEL_MARCH'),
        (0x0CED, 'TRAIN'), (0x0CEE, 'RESEARCH'), (0x0CEF, 'BUILD'),
        (0x0CEB, 'ENABLE_VIEW'), (0x1B8B, 'SESSION'),
    ]}

    # For each known opcode, find all locations and check if others are nearby
    for op_bytes, op_name in known_ops_bytes.items():
        pos = 0
        while True:
            idx = raw.find(op_bytes, pos)
            if idx < 0: break
            # Check if any other known opcodes are within 128 bytes
            nearby_ops = []
            for other_bytes, other_name in known_ops_bytes.items():
                if other_bytes == op_bytes: continue
                for delta in range(-128, 128, 2):
                    check_off = idx + delta
                    if 0 <= check_off < len(raw) - 1:
                        if raw[check_off:check_off+2] == other_bytes:
                            nearby_ops.append((delta, other_name))
            if len(nearby_ops) >= 2:
                print(f"\n  0x{idx:08X} ({op_name}): {len(nearby_ops)} neighbors")
                for delta, name in sorted(nearby_ops):
                    print(f"    +{delta}: {name}")
            pos = idx + 1

    # ═══ Strategy 6: Scan .data.rel.ro for vtables / dispatch arrays ═══
    print("\n" + "=" * 80)
    print("SCAN FOR OPCODE DISPATCH ARRAYS")
    print("=" * 80)

    # In .rodata, look for sorted arrays of u16 opcodes
    # Scan for regions with many valid opcode-like u16 values (0x0001-0x2FFF)
    window = 64
    best_regions = []
    for start in range(0, len(raw) - window, 4):
        count = 0
        for i in range(0, window, 2):
            val = struct.unpack('<H', raw[start+i:start+i+2])[0]
            if 0x0001 <= val <= 0x2FFF:
                count += 1
        if count >= window // 2 - 2:  # Nearly all values are valid opcodes
            # Check if they're sorted or semi-sorted
            vals = [struct.unpack('<H', raw[start+i:start+i+2])[0] for i in range(0, window, 2)]
            known_count = sum(1 for v in vals if v in {0x0CE8, 0x0CED, 0x0CEE, 0x0CEF, 0x0CEB, 0x1B8B, 0x0CE7})
            if known_count >= 2:
                best_regions.append((start, known_count, vals))

    best_regions.sort(key=lambda x: -x[1])
    for start, kc, vals in best_regions[:10]:
        print(f"\n  0x{start:08X}: {kc} known opcodes, values={[f'0x{v:04X}' for v in vals]}")

if __name__ == '__main__':
    main()

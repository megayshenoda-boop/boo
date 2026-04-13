"""
Analyze the actual byte layout of 0x0CE8 (START_MARCH_NEW) plaintext.
Compare all known plaintexts to find field positions, session bytes (VA/VB),
and the relationship between struct layout and wire format.
"""
import struct

IGG_ID = 577962733  # 0x2273_02ED
IGG_LE = struct.pack('<I', IGG_ID)

# All known decoded plaintexts (46 bytes each) with their known parameters
CAPTURES = {
    "cap1": {"tx": 682, "ty": 570, "hero": 255, "type": "gather_wheat",
             "plain": "217f0aec696000a920ed027322b6ffa920b7b6a920b704a920b700a920b700a920aa023a02b700a920b700a920b7"},
    "cap2": {"tx": 682, "ty": 570, "hero": 244, "type": "gather_wheat",
             "plain": "217f0afc695000a920ed027322c6f4a920c7b6a920c704a920c700a920c700a920aa023a02c700a920c700a920c7"},
    "cap3": {"tx": 653, "ty": 565, "hero": 255, "type": "gather_wheat",
             "plain": "2144f3f329b700c220ed02732261ffc22060b6c2206004c2206000c2206000c2208d0235026000c2206000c22060"},
    "cap4": {"tx": 653, "ty": 565, "hero": 241, "type": "gather_wheat",
             "plain": "2144f3f3e9b700ba20ed02732261f1ba2060b6ba206004ba206000ba206000ba208d0235026000ba206000ba2060"},
    "cap5": {"tx": 643, "ty": 536, "hero": 255, "type": "gather_wheat_l2",
             "plain": "2163e6d86969006b20ed0273226fff6b206eb66b206e046b206e006b206e006b20830218026e006b206e006b206e"},
    "cap6": {"tx": None, "ty": None, "hero": 255, "type": "gather_wheat_l2",
             "plain": "219b6ae869bc00a320ed02732256ffa32053b6a3205304a3205300a3205300a3206a0210025300a3205300a32053"},
    "cap7": {"tx": 672, "ty": 605, "hero": 237, "type": "gather_wheat_l2",
             "plain": "21a9c90b696a00ce20ed0273228cedce208db6ce208d04ce208d00ce208d00ce20a0025d028d00ce208d00ce208d"},
    "cap8": {"tx": 665, "ty": 594, "hero": 255, "type": "gather_manual",
             "plain": "21a1d99f697300e120ed02732285ffe12084b6e1208404e1208400e1208400e120990252028400e1208400e12084"},
    "cap9": {"tx": 638, "ty": 568, "hero": 255, "type": "gather_search",
             "plain": "210d1e0ce94800cb20ed02732252ffcb204fb6cb204f04cb204f00cb204f00cb207e0238024f00cb204f00cb204f"},
}

def analyze():
    print("=" * 90)
    print("BYTE-BY-BYTE ANALYSIS OF 0x0CE8 PLAINTEXTS")
    print("=" * 90)

    plains = {}
    for name, cap in CAPTURES.items():
        plains[name] = bytes.fromhex(cap["plain"])

    # 1. Find known value positions
    print("\n--- STEP 1: Locate known values in each capture ---")
    for name, cap in CAPTURES.items():
        p = plains[name]
        print(f"\n{name}: tx={cap['tx']}, ty={cap['ty']}, hero={cap['hero']}, type={cap['type']}")

        # Find IGG_ID
        igg_pos = p.find(IGG_LE)
        print(f"  IGG_ID (ED027322) at byte: {igg_pos}")

        # Find hero
        hero_positions = [i for i in range(len(p)) if p[i] == cap['hero']]
        print(f"  hero ({cap['hero']:02X}) at bytes: {hero_positions}")

        # Find tile_x
        if cap['tx']:
            tx_le = struct.pack('<H', cap['tx'])
            tx_pos = p.find(tx_le)
            print(f"  tile_x ({cap['tx']}={tx_le.hex()}) at byte: {tx_pos}")

            ty_le = struct.pack('<H', cap['ty'])
            ty_pos = p.find(ty_le)
            print(f"  tile_y ({cap['ty']}={ty_le.hex()}) at byte: {ty_pos}")

    # 2. Per-position analysis
    print("\n\n--- STEP 2: Per-position analysis (all 46 bytes) ---")
    print(f"{'Pos':>3} {'mod4':>4} | ", end="")
    for name in sorted(plains.keys()):
        print(f"{name:>6} ", end="")
    print(" | Analysis")
    print("-" * 120)

    for pos in range(46):
        mod4 = pos % 4
        values = {}
        for name in sorted(plains.keys()):
            values[name] = plains[name][pos]

        unique = set(values.values())

        # Classification
        analysis = ""
        if len(unique) == 1:
            v = list(unique)[0]
            analysis = f"CONSTANT = 0x{v:02X} ({v})"
        else:
            # Check if it matches known fields
            known_match = False

            # Check hero
            hero_match = all(values[n] == CAPTURES[n]['hero'] for n in values)
            if hero_match:
                analysis = "= hero_id"
                known_match = True

            # Check IGG_ID bytes
            if 9 <= pos <= 12:
                igg_byte = IGG_LE[pos - 9]
                if all(v == igg_byte for v in values.values()):
                    analysis = f"= IGG_ID[{pos-9}] (0x{igg_byte:02X})"
                    known_match = True

            if not known_match:
                vals_str = "/".join(f"{values[n]:02X}" for n in sorted(values.keys()))

                # Check if same within session pairs (cap1/cap2, cap3/cap4 same session?)
                # Check mod4 pattern
                if mod4 == 0 and all(v == 0x20 for v in values.values()):
                    analysis = f"SESSION mask[0]=0x20 (constant)"
                elif mod4 == 0:
                    analysis = f"mod4=0 vals={vals_str}"
                elif mod4 == 1:
                    analysis = f"mod4=1 (VB?) vals={vals_str}"
                elif mod4 == 2:
                    analysis = f"mod4=2 vals={vals_str}"
                elif mod4 == 3:
                    analysis = f"mod4=3 (VA?) vals={vals_str}"
                else:
                    analysis = f"VARYING vals={vals_str}"

        print(f"{pos:3d} {mod4:4d} | ", end="")
        for name in sorted(plains.keys()):
            print(f"  {values[name]:02X}  ", end="")
        print(f" | {analysis}")

    # 3. Extract session bytes
    print("\n\n--- STEP 3: Session byte extraction ---")
    print("For positions known to be zero (struct fields zeroed by ctor, not set by callers):")
    print("If plain[pos] != 0, then it's a session-dependent mask byte")

    # Positions that should be zero: bytes 0-3 (struct +0x04 to +0x07)
    # And many later positions for zero-valued fields

    for name in sorted(plains.keys()):
        p = plains[name]
        # Extract values at regular zero positions (far from known data)
        # bytes 24-36 should have mostly zeros (struct fields zeroed)
        m0 = p[24] if pos % 4 == 0 else p[8]   # mod 0 position
        m1 = p[25]  # mod 1 position
        m2 = p[26]  # mod 2 position
        m3 = p[27]  # mod 3 position

        # Better: use positions where we're sure data is zero
        # byte 8 (mod 0) = 0x20 in all captures
        # byte 17 (mod 1) = varies
        # byte 6 (mod 2) = 0x00 in most
        # byte 7 (mod 3) = varies
        mask = [p[8], p[17], p[6], p[7]]
        print(f"  {name}: mask = [{mask[0]:02X}, {mask[1]:02X}, {mask[2]:02X}, {mask[3]:02X}]")

        # Now XOR-strip and show the actual data
        actual = bytearray(46)
        for i in range(46):
            actual[i] = p[i] ^ mask[i % 4]

        print(f"    plain:  {p.hex()}")
        print(f"    XOR'd:  {actual.hex()}")

        # Verify known values after XOR
        igg_pos_actual = actual.find(IGG_LE)
        print(f"    IGG after XOR at: {igg_pos_actual}")
        if CAPTURES[name]['tx']:
            tx_le = struct.pack('<H', CAPTURES[name]['tx'])
            tx_pos_actual = actual.find(tx_le)
            print(f"    tile_x after XOR at: {tx_pos_actual}")

    # 4. Cross-capture comparison: same session?
    print("\n\n--- STEP 4: Session grouping ---")
    print("Captures with identical session bytes (bytes 7,15,17) = same session:")
    sessions = {}
    for name in sorted(plains.keys()):
        p = plains[name]
        session_key = (p[7], p[15], p[17])
        sessions.setdefault(session_key, []).append(name)

    for sk, caps in sessions.items():
        print(f"  Session ({sk[0]:02X},{sk[1]:02X},{sk[2]:02X}): {', '.join(caps)}")

    # 5. Within same session, diff to find data-dependent bytes
    print("\n\n--- STEP 5: Same-session diffs (isolate data-dependent bytes) ---")
    for sk, caps in sessions.items():
        if len(caps) > 1:
            print(f"\n  Session ({sk[0]:02X},{sk[1]:02X},{sk[2]:02X}):")
            base_name = caps[0]
            base = plains[base_name]
            for other_name in caps[1:]:
                other = plains[other_name]
                diffs = []
                for i in range(46):
                    if base[i] != other[i]:
                        diffs.append((i, base[i], other[i]))
                print(f"    {base_name} vs {other_name}: {len(diffs)} diffs at positions:")
                for pos, v1, v2 in diffs:
                    b_hero = CAPTURES[base_name]['hero']
                    o_hero = CAPTURES[other_name]['hero']
                    note = ""
                    if v1 == b_hero and v2 == o_hero:
                        note = " ← HERO"
                    elif pos in range(37, 41):
                        note = " ← TILE area"
                    print(f"      pos {pos}: {v1:02X} -> {v2:02X}{note}")

    # 6. Tile position verification
    print("\n\n--- STEP 6: Precise tile byte positions ---")
    # From cap3 vs cap4 (same session, same tiles, different hero)
    # The diff should ONLY be hero byte
    # From cap1 vs cap5 (different session, different tiles)
    # Look for tile bytes precisely
    for name, cap in CAPTURES.items():
        if not cap['tx']:
            continue
        p = plains[name]
        tx_le = struct.pack('<H', cap['tx'])
        ty_le = struct.pack('<H', cap['ty'])

        # Find all occurrences
        tx_positions = []
        ty_positions = []
        for i in range(45):
            if p[i:i+2] == tx_le:
                tx_positions.append(i)
            if p[i:i+2] == ty_le:
                ty_positions.append(i)

        print(f"  {name}: tx={cap['tx']} at {tx_positions}, ty={cap['ty']} at {ty_positions}")

if __name__ == "__main__":
    analyze()

"""
Derive the EXTRA 4-byte XOR key from each capture using IGG_ID as anchor.
Theory: decoded_plaintext = real_data XOR extra_key[pos % 4]
IGG_ID is at bytes 33-36 of the real data.
extra[0] = decoded[36] XOR IGG_LE[3]
extra[1] = decoded[33] XOR IGG_LE[0]
extra[2] = decoded[34] XOR IGG_LE[1]
extra[3] = decoded[35] XOR IGG_LE[2]
"""
import struct

IGG_ID = 577962733
IGG_LE = struct.pack('<I', IGG_ID)  # ED 02 73 22

CAPTURES = {
    "cap1": {"tx": 682, "ty": 570, "hero": 255,
             "plain": "217f0aec696000a920ed027322b6ffa920b7b6a920b704a920b700a920b700a920aa023a02b700a920b700a920b7"},
    "cap2": {"tx": 682, "ty": 570, "hero": 244,
             "plain": "217f0afc695000a920ed027322c6f4a920c7b6a920c704a920c700a920c700a920aa023a02c700a920c700a920c7"},
    "cap3": {"tx": 653, "ty": 565, "hero": 255,
             "plain": "2144f3f329b700c220ed02732261ffc22060b6c2206004c2206000c2206000c2208d0235026000c2206000c22060"},
    "cap4": {"tx": 653, "ty": 565, "hero": 241,
             "plain": "2144f3f3e9b700ba20ed02732261f1ba2060b6ba206004ba206000ba206000ba208d0235026000ba206000ba2060"},
    "cap5": {"tx": 643, "ty": 536, "hero": 255,
             "plain": "2163e6d86969006b20ed0273226fff6b206eb66b206e046b206e006b206e006b20830218026e006b206e006b206e"},
    "cap6": {"tx": None, "ty": None, "hero": 255,
             "plain": "219b6ae869bc00a320ed02732256ffa32053b6a3205304a3205300a3205300a3206a0210025300a3205300a32053"},
    "cap7": {"tx": 672, "ty": 605, "hero": 237,
             "plain": "21a9c90b696a00ce20ed0273228cedce208db6ce208d04ce208d00ce208d00ce20a0025d028d00ce208d00ce208d"},
    "cap8": {"tx": 665, "ty": 594, "hero": 255,
             "plain": "21a1d99f697300e120ed02732285ffe12084b6e1208404e1208400e1208400e120990252028400e1208400e12084"},
    "cap9": {"tx": 638, "ty": 568, "hero": 255,
             "plain": "210d1e0ce94800cb20ed02732252ffcb204fb6cb204f04cb204f00cb204f00cb207e0238024f00cb204f00cb204f"},
}

# Known server keys from prior KPA analysis
KNOWN_SK = {
    "cap1": 0x49C80A45,
    "cap3": 0x4924F331,
    "cap5": 0x490DE6B3,
    "cap7": 0x4924C9C5,
    "cap8": 0x4925D97E,
    "cap9": 0x49421EC7,
}

def derive():
    print("=" * 90)
    print("EXTRA XOR KEY DERIVATION FROM IGG_ID ANCHOR")
    print("=" * 90)

    all_extra = {}
    all_real = {}

    for name in sorted(CAPTURES.keys()):
        cap = CAPTURES[name]
        p = bytes.fromhex(cap["plain"])

        # Derive extra key from IGG_ID at bytes 33-36
        extra = [0] * 4
        extra[0] = p[36] ^ IGG_LE[3]  # byte 36 mod4=0, IGG[3]=0x22
        extra[1] = p[33] ^ IGG_LE[0]  # byte 33 mod4=1, IGG[0]=0xED
        extra[2] = p[34] ^ IGG_LE[1]  # byte 34 mod4=2, IGG[1]=0x02
        extra[3] = p[35] ^ IGG_LE[2]  # byte 35 mod4=3, IGG[2]=0x73

        all_extra[name] = extra
        print(f"\n{name}: extra = [{extra[0]:02X}, {extra[1]:02X}, {extra[2]:02X}, {extra[3]:02X}]")

        # Apply XOR to get real data
        real = bytearray(46)
        for i in range(46):
            real[i] = p[i] ^ extra[i % 4]
        all_real[name] = real

        # Verify known values
        checks = []

        # Check tiles at bytes 9-12
        if cap['tx']:
            tx = struct.unpack('<H', real[9:11])[0]
            ty = struct.unpack('<H', real[11:13])[0]
            checks.append(f"tile=({tx},{ty}) {'✓' if tx == cap['tx'] and ty == cap['ty'] else '✗ EXPECTED '+str((cap['tx'],cap['ty']))}")

        # Check hero at byte 14
        hero = real[14]
        checks.append(f"hero={hero} {'✓' if hero == cap['hero'] else '✗ EXPECTED '+str(cap['hero'])}")

        # Check kingdom at byte 18
        kingdom = real[18]
        checks.append(f"kingdom={kingdom} (0xB6={0xB6})")

        # Check resource at byte 22
        resource = real[22]
        checks.append(f"resource={resource}")

        # Check IGG at bytes 33-36
        igg = struct.unpack('<I', real[33:37])[0]
        checks.append(f"IGG={igg} {'✓' if igg == IGG_ID else '✗'}")

        print(f"  Checks: {' | '.join(checks)}")
        print(f"  Real data: {real.hex()}")

    # Analyze extra keys across captures
    print("\n\n" + "=" * 90)
    print("EXTRA KEY ANALYSIS")
    print("=" * 90)

    print("\n--- Extra key values ---")
    print(f"{'Name':>6} | extra[0] extra[1] extra[2] extra[3] | extra as u32 LE")
    for name in sorted(all_extra.keys()):
        e = all_extra[name]
        eu32 = e[0] | (e[1] << 8) | (e[2] << 16) | (e[3] << 24)
        print(f"{name:>6} | {e[0]:5X}    {e[1]:5X}    {e[2]:5X}    {e[3]:5X}    | 0x{eu32:08X}")

    print("\nextra[0] is ALWAYS 0x20:", all(all_extra[n][0] == 0x20 for n in all_extra))
    print("extra[2] is ALWAYS 0x00:", all(all_extra[n][2] == 0x00 for n in all_extra))

    # Compare extra with server keys
    print("\n--- Extra key vs Server key ---")
    for name in sorted(KNOWN_SK.keys()):
        if name in all_extra:
            e = all_extra[name]
            sk = KNOWN_SK[name]
            sk_bytes = [(sk >> (8*i)) & 0xFF for i in range(4)]
            print(f"\n{name}: sk={sk_bytes}, extra={e}")
            # Try various derivations
            xor_val = [sk_bytes[i] ^ e[i] for i in range(4)]
            add_val = [(e[i] - sk_bytes[i]) & 0xFF for i in range(4)]
            print(f"  sk XOR extra = {[f'{v:02X}' for v in xor_val]}")
            print(f"  extra - sk   = {[f'{v:02X}' for v in add_val]}")
            print(f"  sk bytes:  {[f'{v:02X}' for v in sk_bytes]}")

    # Analyze real data patterns
    print("\n\n" + "=" * 90)
    print("REAL DATA FIELD ANALYSIS (after XOR removal)")
    print("=" * 90)

    print(f"\n{'Pos':>3} | ", end="")
    for name in sorted(all_real.keys()):
        print(f"{name:>6} ", end="")
    print(" | Field")
    print("-" * 110)

    for pos in range(46):
        vals = {n: all_real[n][pos] for n in sorted(all_real.keys())}
        unique = set(vals.values())

        field = ""
        if pos == 0: field = "march_slot?"
        elif pos in (1,2,3): field = "header bytes"
        elif pos == 4: field = "march_type_lo? (0x49=73)"
        elif pos == 5: field = "?"
        elif pos in (6,7,8): field = "padding?"
        elif pos == 9: field = "tile_x_lo"
        elif pos == 10: field = "tile_x_hi"
        elif pos == 11: field = "tile_y_lo"
        elif pos == 12: field = "tile_y_hi"
        elif pos == 13: field = "troop_count?"
        elif pos == 14: field = "hero_id"
        elif pos == 18: field = "kingdom_id (0xB6)"
        elif pos == 22: field = "resource_type (4=wheat)"
        elif pos >= 33 and pos <= 36: field = f"IGG_ID[{pos-33}]"
        elif len(unique) == 1 and list(unique)[0] == 0:
            field = "= 0"

        print(f"{pos:3d} | ", end="")
        for name in sorted(all_real.keys()):
            print(f"  {vals[name]:02X}  ", end="")
        print(f" | {field}")

    # Check bytes 0-8 patterns
    print("\n\n--- Header analysis (bytes 0-8) ---")
    for name in sorted(all_real.keys()):
        r = all_real[name]
        cap = CAPTURES[name]
        print(f"{name}: [{r[0]:02X} {r[1]:02X} {r[2]:02X} {r[3]:02X}] [{r[4]:02X} {r[5]:02X} {r[6]:02X} {r[7]:02X} {r[8]:02X}] hero={cap['hero']}")

    # Check byte 4 relationship with march_type
    print("\n--- Byte 4 analysis ---")
    for name in sorted(all_real.keys()):
        r = all_real[name]
        cap = CAPTURES[name]
        print(f"{name}: byte4={r[4]:02X} type={cap.get('type','?')}")

    # Look at non-zero patterns at "padding" positions
    print("\n--- Non-zero padding analysis ---")
    padding_pos = [7, 13, 15, 16, 17, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
    for name in sorted(all_real.keys()):
        r = all_real[name]
        nonzero = [(pos, r[pos]) for pos in padding_pos if r[pos] != 0]
        if nonzero:
            nz_str = ", ".join(f"pos{p}={v:02X}" for p, v in nonzero)
            print(f"  {name}: {nz_str}")
        else:
            print(f"  {name}: ALL ZERO ✓")

if __name__ == "__main__":
    derive()

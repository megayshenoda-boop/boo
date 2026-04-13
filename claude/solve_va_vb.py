"""
Brute-force VA/VB derivation from server_key.
We have 7 pairs of (server_key, VA, VB) from PCAP captures.
Try ALL possible 1-2 operation combinations on sk bytes.
"""
import struct
import itertools

# Known (server_key_u32, VA, VB) pairs from PCAP analysis
PAIRS = [
    (0xA7CD45BE, 0xA9, 0xB7),
    (0x7D336BBB, 0xC2, 0x60),
    (0xD914C849, 0xBA, 0x60),
    (0x0D0508A0, 0x6B, 0x6E),
    (0x13CF850E, 0xCE, 0x8D),
    (0xD09DE03D, 0xE1, 0x84),
    (0x362E5849, 0xCB, 0x4F),
]

def sk_bytes(sk):
    return [(sk >> (i*8)) & 0xFF for i in range(4)]

# Try all simple formulas: VA = f(s0,s1,s2,s3)
# f can be: single byte, XOR of 2, ADD of 2, SUB of 2, ROT, etc.

def test_formula(formula_fn, target_idx):
    """Test if formula_fn(sk_bytes) == target (VA=0 or VB=1) for ALL pairs."""
    target_name = "VA" if target_idx == 0 else "VB"
    for sk, va, vb in PAIRS:
        s = sk_bytes(sk)
        result = formula_fn(s) & 0xFF
        expected = va if target_idx == 0 else vb
        if result != expected:
            return False
    return True

# Generate formulas
formulas = []

# Single byte
for i in range(4):
    formulas.append((f"s[{i}]", lambda s, i=i: s[i]))

# NOT
for i in range(4):
    formulas.append((f"~s[{i}]", lambda s, i=i: ~s[i]))

# Pairs: XOR, ADD, SUB
for i in range(4):
    for j in range(4):
        if i != j:
            formulas.append((f"s[{i}]^s[{j}]", lambda s, i=i, j=j: s[i] ^ s[j]))
            formulas.append((f"s[{i}]+s[{j}]", lambda s, i=i, j=j: s[i] + s[j]))
            formulas.append((f"s[{i}]-s[{j}]", lambda s, i=i, j=j: s[i] - s[j]))
            formulas.append((f"s[{i}]*s[{j}]", lambda s, i=i, j=j: s[i] * s[j]))

# Triple XOR
for i in range(4):
    for j in range(i+1, 4):
        for k in range(j+1, 4):
            formulas.append((f"s[{i}]^s[{j}]^s[{k}]", lambda s, i=i, j=j, k=k: s[i]^s[j]^s[k]))

# All 4 XOR
formulas.append(("s[0]^s[1]^s[2]^s[3]", lambda s: s[0]^s[1]^s[2]^s[3]))

# Rotations
for i in range(4):
    for r in range(1, 8):
        formulas.append((f"ROL(s[{i}],{r})", lambda s, i=i, r=r: ((s[i] << r) | (s[i] >> (8-r)))))
        formulas.append((f"ROR(s[{i}],{r})", lambda s, i=i, r=r: ((s[i] >> r) | (s[i] << (8-r)))))

# XOR with constant
for i in range(4):
    for c in [0x17, 0x20, 0xB7, 0xFF, 0x58, 0xEF, 0xD7, 0x14, 0xA2, 0x3B, 0x9C]:
        formulas.append((f"s[{i}]^0x{c:02X}", lambda s, i=i, c=c: s[i] ^ c))

# ADD with constant
for i in range(4):
    for c in range(1, 256):
        formulas.append((f"s[{i}]+{c}", lambda s, i=i, c=c: s[i] + c))

# Two-step: (s[i] OP s[j]) OP2 s[k]
for i in range(4):
    for j in range(4):
        if i == j: continue
        for k in range(4):
            if k == i or k == j: continue
            formulas.append((f"(s[{i}]^s[{j}])+s[{k}]", lambda s, i=i, j=j, k=k: (s[i]^s[j])+s[k]))
            formulas.append((f"(s[{i}]^s[{j}])-s[{k}]", lambda s, i=i, j=j, k=k: (s[i]^s[j])-s[k]))
            formulas.append((f"(s[{i}]+s[{j}])^s[{k}]", lambda s, i=i, j=j, k=k: (s[i]+s[j])^s[k]))
            formulas.append((f"(s[{i}]-s[{j}])^s[{k}]", lambda s, i=i, j=j, k=k: (s[i]-s[j])^s[k]))
            formulas.append((f"(s[{i}]+s[{j}])+s[{k}]", lambda s, i=i, j=j, k=k: s[i]+s[j]+s[k]))
            formulas.append((f"(s[{i}]*s[{j}])^s[{k}]", lambda s, i=i, j=j, k=k: (s[i]*s[j])^s[k]))
            formulas.append((f"(s[{i}]*s[{j}])+s[{k}]", lambda s, i=i, j=j, k=k: (s[i]*s[j])+s[k]))

# Byte swap / reorder
for perm in itertools.permutations(range(4)):
    formulas.append((f"s[{perm[0]}]<<4|s[{perm[1]}]&0xF",
                     lambda s, p=perm: (s[p[0]] << 4) | (s[p[1]] & 0xF)))
    formulas.append((f"s[{perm[0]}]&0xF0|s[{perm[1]}]>>4",
                     lambda s, p=perm: (s[p[0]] & 0xF0) | (s[p[1]] >> 4)))

# CRC-like
TABLE = [0x58, 0xef, 0xd7, 0x14, 0xa2, 0x3b, 0x9c]
for i in range(4):
    for t in range(7):
        formulas.append((f"s[{i}]^TABLE[{t}]", lambda s, i=i, t=t: s[i] ^ TABLE[t]))
        formulas.append((f"s[{i}]+TABLE[{t}]", lambda s, i=i, t=t: s[i] + TABLE[t]))

# Higher-byte access (treat sk as u32, shift by 4,12,20)
for shift in [4, 12, 20]:
    formulas.append((f"(sk>>{shift})&0xFF", lambda s, sh=shift:
                     ((s[0]|(s[1]<<8)|(s[2]<<16)|(s[3]<<24)) >> sh) & 0xFF))

print(f"Testing {len(formulas)} formulas...")
print()

for target_name, target_idx in [("VA", 0), ("VB", 1)]:
    print(f"=== Searching for {target_name} ===")
    found = 0
    for name, fn in formulas:
        if test_formula(fn, target_idx):
            print(f"  MATCH: {target_name} = {name}")
            # Show values for verification
            for sk, va, vb in PAIRS:
                s = sk_bytes(sk)
                result = fn(s) & 0xFF
                expected = va if target_idx == 0 else vb
                print(f"    sk=0x{sk:08X} → {result:#04x} (expected {expected:#04x})")
            found += 1
    if found == 0:
        print("  No simple formula found")
    print()

# Also try: VA derived from sk as u16 pairs
print("=== Trying u16 pair operations ===")
for sk, va, vb in PAIRS:
    s = sk_bytes(sk)
    lo16 = s[0] | (s[1] << 8)
    hi16 = s[2] | (s[3] << 8)
    print(f"  sk=0x{sk:08X}: lo16=0x{lo16:04X} hi16=0x{hi16:04X} "
          f"lo16%256=0x{lo16&0xFF:02X} hi16%256=0x{hi16&0xFF:02X} "
          f"(lo16>>8)=0x{(lo16>>8)&0xFF:02X} (hi16>>8)=0x{(hi16>>8)&0xFF:02X} "
          f"VA=0x{va:02X} VB=0x{vb:02X}")

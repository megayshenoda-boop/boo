#!/usr/bin/env python3
"""
24_verify_newencode.py - Verify NewEncode format against ALL 0x1B8B PCAPs
=========================================================================
NewEncode format (full packet):
  [0:2]  = total_length (u16 LE)
  [2:4]  = opcode (u16 LE, 0x1B8B)
  [4:6]  = 2 extra bytes (NOT encrypted)
  [6]    = checksum = sum(encrypted_bytes[10:]) & 0xFF
  [7]    = msg_lo
  [8]    = msg_lo ^ 0xB7
  [9]    = msg_hi
  [10:]  = encrypted data, abs_i starts at 10
"""
import struct, sys
from pathlib import Path
sys.path.insert(0, r'D:\CascadeProjects\claude')
from protocol import CMSG_TABLE as TABLE

def read_pcap_streams(filepath):
    with open(filepath, 'rb') as f:
        magic = struct.unpack('<I', f.read(4))[0]
        endian = '<' if magic == 0xa1b2c3d4 else '>'
        f.read(20)
        streams = {}
        while True:
            hdr = f.read(16)
            if len(hdr) < 16: break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
            d = f.read(incl_len)
            if len(d) < incl_len: break
            if len(d) < 20: continue
            ihl = (d[0] & 0x0F) * 4
            if d[9] != 6: continue
            tcp = d[ihl:]
            if len(tcp) < 20: continue
            sp = struct.unpack('>H', tcp[0:2])[0]
            dp = struct.unpack('>H', tcp[2:4])[0]
            toff = ((tcp[12] >> 4) & 0xF) * 4
            pl = tcp[toff:]
            if not pl: continue
            gp = set(range(5990, 5999)) | set(range(7001, 7011))
            if dp in gp:
                streams.setdefault('C2S', bytearray()).extend(pl)
            elif sp in gp:
                streams.setdefault('S2C', bytearray()).extend(pl)
    return streams

def parse_packets(raw):
    packets = []
    pos = 0
    while pos + 4 <= len(raw):
        pkt_len = struct.unpack('<H', raw[pos:pos+2])[0]
        opcode = struct.unpack('<H', raw[pos+2:pos+4])[0]
        if pkt_len < 4 or pkt_len > 65535 or pos + pkt_len > len(raw): break
        packets.append((opcode, bytes(raw[pos:pos+pkt_len])))
        pos += pkt_len
    return packets

def extract_sk(s2c):
    for op, raw in s2c:
        if op == 0x0038:
            pl = raw[4:]
            if len(pl) > 100:
                ec = struct.unpack('<H', pl[0:2])[0]
                for idx in range(ec):
                    off = 2 + idx * 12
                    if off + 12 > len(pl): break
                    if struct.unpack('<I', pl[off:off+4])[0] == 0x4F:
                        return struct.unpack('<I', pl[off+4:off+8])[0]
    return None

# Collect
pcap_dir = Path(r'D:\CascadeProjects')
pcaps = sorted(pcap_dir.glob('*.pcap'))
for sub in ['rebel_attack', 'codex_lab']:
    p = pcap_dir / sub
    if p.exists(): pcaps.extend(sorted(p.glob('*.pcap')))

print("Verifying NewEncode format for ALL 0x1B8B packets...")
print(f"{'PCAP':<40} {'ck_ok':>6} {'v_ok':>5} {'extra':<12} {'msg':>10} {'plaintext'}")
print("-" * 130)

total = 0
ck_pass = 0
v_pass = 0
all_plains = []

for pcap in pcaps:
    try:
        s = read_pcap_streams(pcap)
        if 'C2S' not in s or 'S2C' not in s: continue
        c2s = parse_packets(s['C2S'])
        s2c = parse_packets(s['S2C'])
        sk_u32 = extract_sk(s2c)
        if not sk_u32: continue
        sk = [sk_u32 & 0xFF, (sk_u32>>8) & 0xFF, (sk_u32>>16) & 0xFF, (sk_u32>>24) & 0xFF]

        for op, raw in c2s:
            if op != 0x1B8B: continue
            if len(raw) < 11: continue
            total += 1

            # NewEncode format
            extra = raw[4:6]  # 2 extra bytes
            ck = raw[6]       # checksum
            ml = raw[7]       # msg_lo
            v = raw[8]        # verify
            mh = raw[9]       # msg_hi
            enc = raw[10:]    # encrypted data
            msg = [ml, mh]

            # Verify checksum
            sum_enc = sum(enc) & 0xFF
            ck_ok = ck == sum_enc

            # Verify v = ml ^ 0xB7
            v_ok = v == ((ml ^ 0xB7) & 0xFF)

            if ck_ok: ck_pass += 1
            if v_ok: v_pass += 1

            # Decrypt
            plain = bytearray(len(enc))
            for j in range(len(enc)):
                abs_i = j + 10
                tb = TABLE[abs_i % 7]
                sb = sk[abs_i % 4]
                mb = msg[abs_i % 2]
                plain[j] = ((enc[j] ^ sb ^ tb) - mb * 17) & 0xFF

            extra_hex = extra.hex()
            msg_hex = f"0x{ml:02X},0x{mh:02X}"
            plain_hex = plain.hex()
            status = "OK" if (ck_ok and v_ok) else f"ck={'Y' if ck_ok else 'N'} v={'Y' if v_ok else 'N'}"

            print(f"{pcap.name:<40} {status:>6} {'Y' if v_ok else 'N':>5} {extra_hex:<12} {msg_hex:>10} {plain_hex}")
            all_plains.append((pcap.name, sk_u32, extra, bytes(plain)))
    except: continue

print(f"\n{'='*80}")
print(f"RESULTS: {total} packets")
print(f"  Checksum match: {ck_pass}/{total}")
print(f"  Verify match:   {v_pass}/{total}")
print(f"{'='*80}")

if all_plains:
    print(f"\n\nPlaintext Analysis:")
    print(f"  Plaintext size: {len(all_plains[0][3])} bytes")
    print(f"\n  Decoding first 5 plaintexts as fields:")
    for pname, sk, extra, plain in all_plains[:5]:
        print(f"\n  {pname} (SK=0x{sk:08X}, extra={extra.hex()}):")
        print(f"    Raw: {plain.hex()}")
        if len(plain) >= 8:
            # Try various interpretations
            print(f"    As u16+u16+u16+u16+u64: {struct.unpack('<H', plain[0:2])[0]}, {struct.unpack('<H', plain[2:4])[0]}, {struct.unpack('<H', plain[4:6])[0]}, {struct.unpack('<H', plain[6:8])[0]}", end="")
            if len(plain) >= 16:
                print(f", 0x{struct.unpack('<Q', plain[8:16])[0]:016X}")
            else:
                print()
            # Bytes interpretation
            print(f"    Bytes: {' '.join(f'{b:02X}' for b in plain)}")

    # Check for patterns across all plaintexts
    print(f"\n\n  Pattern analysis across {len(all_plains)} plaintexts:")

    # Check which bytes are constant
    if all_plains:
        plen = len(all_plains[0][3])
        for pos in range(plen):
            vals = set(p[3][pos] for p in all_plains if len(p[3]) > pos)
            if len(vals) == 1:
                print(f"    Byte {pos}: CONSTANT = 0x{list(vals)[0]:02X}")
            elif len(vals) <= 5:
                print(f"    Byte {pos}: {len(vals)} values: {sorted(vals)}")

    # Check extra bytes pattern
    print(f"\n  Extra bytes [4:6] analysis:")
    extra_vals = set(e.hex() for _, _, e, _ in all_plains)
    print(f"    Unique values: {len(extra_vals)}")
    if len(extra_vals) <= 10:
        print(f"    Values: {sorted(extra_vals)}")

    # Check if extra bytes relate to struct fields
    print(f"\n  Checking extra bytes vs plaintext relationship:")
    for pname, sk, extra, plain in all_plains[:10]:
        extra_u16 = struct.unpack('<H', extra)[0]
        p0 = struct.unpack('<H', plain[0:2])[0] if len(plain) >= 2 else 0
        print(f"    extra=0x{extra_u16:04X}, plain[0:2]=0x{p0:04X}, diff=0x{(extra_u16-p0)&0xFFFF:04X}")

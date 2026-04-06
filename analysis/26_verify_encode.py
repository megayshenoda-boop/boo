#!/usr/bin/env python3
"""
26_verify_encode.py - Verify encode_offset6 exactly matches PCAP samples.
Take a known PCAP, decrypt with NewEncode offsets, re-encrypt, compare byte-for-byte.
"""
import struct, sys
sys.path.insert(0, r'D:\CascadeProjects\claude')
from codec import CMsgCodec
from protocol import CMSG_TABLE as TABLE

# PCAP sample: PCAPdroid_25_Mar_07_05_12.pcap
# Full 0x1B8B packet: 1a008b1b6cd2d690276f0ec14661afb239374a676d7a078be580
# Server key: 0x02677C7E
pcap_hex = "1a008b1b6cd2d690276f0ec14661afb239374a676d7a078be580"
pcap_raw = bytes.fromhex(pcap_hex)
sk_u32 = 0x02677C7E

# Parse NewEncode format
assert pcap_raw[0:2] == b'\x1a\x00'  # length = 26
assert pcap_raw[2:4] == b'\x8b\x1b'  # opcode = 0x1B8B
extra = pcap_raw[4:6]
ck = pcap_raw[6]
ml = pcap_raw[7]
v = pcap_raw[8]
mh = pcap_raw[9]
enc = pcap_raw[10:]
msg_value = ml | (mh << 8)

print(f"PCAP packet: {pcap_hex}")
print(f"Server key: 0x{sk_u32:08X}")
print(f"Extra bytes: {extra.hex()}")
print(f"msg_lo=0x{ml:02X}, msg_hi=0x{mh:02X}, msg_value=0x{msg_value:04X}")
print(f"Checksum byte: 0x{ck:02X}")
print(f"Verify byte: 0x{v:02X} (expected: 0x{ml^0xB7:02X})")
print(f"Encrypted ({len(enc)}B): {enc.hex()}")

# Decrypt manually
sk = [sk_u32 & 0xFF, (sk_u32>>8) & 0xFF, (sk_u32>>16) & 0xFF, (sk_u32>>24) & 0xFF]
print(f"SK bytes: {[f'0x{b:02X}' for b in sk]}")
msg = [ml, mh]

plain = bytearray(len(enc))
for j in range(len(enc)):
    abs_i = j + 10
    tb = TABLE[abs_i % 7]
    sb = sk[abs_i % 4]
    mb = msg[abs_i % 2]
    plain[j] = ((enc[j] ^ sb ^ tb) - mb * 17) & 0xFF

print(f"Plaintext ({len(plain)}B): {plain.hex()}")

# Now re-encode using codec.encode_offset6
codec = CMsgCodec.from_u32(sk_u32)
re_encoded = codec.encode_offset6(0x1B8B, bytes(plain), extra=extra, msg_value=msg_value)
print(f"\nRe-encoded ({len(re_encoded)}B): {re_encoded.hex()}")
print(f"PCAP orig  ({len(pcap_raw)}B): {pcap_raw.hex()}")
print(f"Match: {re_encoded == pcap_raw}")

if re_encoded != pcap_raw:
    print("\nByte-by-byte comparison:")
    for i in range(len(pcap_raw)):
        orig = pcap_raw[i]
        enc_b = re_encoded[i] if i < len(re_encoded) else 0xFF
        match = "OK" if orig == enc_b else f"MISMATCH (want 0x{orig:02X}, got 0x{enc_b:02X})"
        if orig != enc_b:
            print(f"  byte[{i:2d}]: {match}")

# Test 5 more PCAPs
print(f"\n{'='*80}")
print("Testing 5 more PCAPs:")
print(f"{'='*80}")

test_cases = [
    ("PCAPdroid_27_Mar", "1a008b1bda3d3e3a8d3a8bf65f1ddabd24b3236a6cfc6e86e406", 0x88587D29),
    ("PCAPdroid_28_Mar", "1a008b1b07921a19aed6c4910627b7d25fc14c05158e01e99d74", 0x0B46E321),
    ("PCAPdroid_29_Mar", "1a008b1b9aee68c473cc854d0b4c3c0294e6c1d1d8ad8c3d5057", 0x61607E47),
    ("PCAPdroid_30_Mar", "1a008b1b445212d86f1f900e8dccc15df27a3488b63779643ecd", 0xBDC1617D),
    ("gather_fresh", "1a008b1bf96a1cda6d704efedc731fb1a719e67aef4aab9667b0", 0x2E3D7D0A),
]

for name, hex_pkt, sk_val in test_cases:
    raw = bytes.fromhex(hex_pkt)
    extra_t = raw[4:6]
    ml_t = raw[7]
    mh_t = raw[9]
    msg_val_t = ml_t | (mh_t << 8)
    enc_t = raw[10:]

    # Decrypt
    sk_t = [sk_val & 0xFF, (sk_val>>8) & 0xFF, (sk_val>>16) & 0xFF, (sk_val>>24) & 0xFF]
    msg_t = [ml_t, mh_t]
    plain_t = bytearray(len(enc_t))
    for j in range(len(enc_t)):
        abs_i = j + 10
        plain_t[j] = ((enc_t[j] ^ sk_t[abs_i%4] ^ TABLE[abs_i%7]) - msg_t[abs_i%2]*17) & 0xFF

    # Re-encode
    codec_t = CMsgCodec.from_u32(sk_val)
    re_enc_t = codec_t.encode_offset6(0x1B8B, bytes(plain_t), extra=extra_t, msg_value=msg_val_t)
    match = re_enc_t == raw
    print(f"  {name}: {'MATCH' if match else 'MISMATCH'}  plain={plain_t.hex()}")
    if not match:
        for i in range(len(raw)):
            if i >= len(re_enc_t) or raw[i] != re_enc_t[i]:
                print(f"    byte[{i}]: want 0x{raw[i]:02X} got 0x{re_enc_t[i] if i<len(re_enc_t) else -1:02X}")

# Also test: encode with the KNOWN plaintext and see if our bot would produce valid output
print(f"\n{'='*80}")
print("Test bot-style encode (random msg, known plaintext):")
print(f"{'='*80}")
codec_test = CMsgCodec.from_u32(0x3ABBAEA2)  # server key from test run
plain_data = bytes.fromhex("ed02732200000000ffffffffffffffff")
for i in range(3):
    pkt = codec_test.encode_offset6(0x1B8B, plain_data)
    # Verify our own packet
    ck_t = pkt[6]
    ml_t = pkt[7]
    v_t = pkt[8]
    mh_t = pkt[9]
    sum_enc = sum(pkt[10:]) & 0xFF
    v_expect = (ml_t ^ 0xB7) & 0xFF
    print(f"  Attempt {i}: ck={ck_t==sum_enc} v={v_t==v_expect} len={len(pkt)} hex={pkt.hex()}")
    if v_t != v_expect:
        print(f"    BUG! v=0x{v_t:02X} but ml^0xB7=0x{v_expect:02X}")

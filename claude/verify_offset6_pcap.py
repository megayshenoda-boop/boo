#!/usr/bin/env python3
"""
CRITICAL: Verify encode_offset6 produces byte-perfect match against PCAP 0x1B8B packets.
We verified standard encode() matches PCAPs. Now verify offset6.
"""
import struct, sys
sys.path.insert(0, r'D:\CascadeProjects\claude')
from codec import CMsgCodec

CMSG_TABLE = [0x58, 0xEF, 0xD7, 0x14, 0xA2, 0x3B, 0x9C]

# All PCAP 0x1B8B raw packets and their server keys
PCAP_1B8B = [
    {
        "name": "PCAP1 (25_Mar_07_05)",
        "sk": 0x02677C7E,
        "raw": bytes.fromhex("1a008b1b6cd2dfb06f3cd7c5a8e11b2bfa7a340093faed03b0d7"),
    },
    {
        "name": "PCAP2 (25_Mar_07_29)",
        "sk": 0xB4B19AD1,
        "raw": bytes.fromhex("1a008b1b5d92b4a1af17deb2c8dfa64f87edb00f0fa6ebe7f60a"),
    },
    {
        "name": "PCAP3 (27_Mar_09_17)",
        "sk": 0x88587D29,
        "raw": bytes.fromhex("1a008b1bda3d423a3d3a6c95d3a13a90c999a23a18ece5d05cc2"),
    },
    {
        "name": "PCAP4 (28_Mar_10_41)",
        "sk": 0x0B46E321,
        "raw": bytes.fromhex("1a008b1b07921a19aed6c4910627b7d25fc14c05158e01e99d74"),
    },
    {
        "name": "PCAP5 (29_Mar_10_53)",
        "sk": 0x61607E47,
        "raw": bytes.fromhex("1a008b1b9aee68c473cc854d0b4c3c0294e6c1d1d8ad8c3d5057"),
    },
    {
        "name": "PCAP6 (30_Mar_19_56)",
        "sk": 0xBDC1617D,
        "raw": bytes.fromhex("1a008b1b445212d86f1f900e8dccc15df27a3488b63779643ecd"),
    },
]

EXPECTED_PLAIN = bytes.fromhex("ED02732200000000FFFFFFFFFFFFFFFF")

for pcap in PCAP_1B8B:
    raw = pcap["raw"]
    sk = pcap["sk"]
    name = pcap["name"]
    sk_bytes = [(sk >> (8*i)) & 0xFF for i in range(4)]
    
    print(f"\n{'='*60}")
    print(f"  {name}  SK=0x{sk:08X}")
    print(f"{'='*60}")
    print(f"  RAW: {raw.hex()}")
    
    # Parse offset6 header
    pkt_len = struct.unpack('<H', raw[0:2])[0]
    opcode = struct.unpack('<H', raw[2:4])[0]
    extra_lo = raw[4]
    extra_hi = raw[5]
    ck = raw[6]
    msg_lo = raw[7]
    verify = raw[8]
    msg_hi = raw[9]
    
    extra = bytes([extra_lo, extra_hi])
    msg_value = (msg_hi << 8) | msg_lo
    
    print(f"  len={pkt_len} op=0x{opcode:04X} extra=[0x{extra_lo:02X},0x{extra_hi:02X}]")
    print(f"  ck=0x{ck:02X} msg_lo=0x{msg_lo:02X} verify=0x{verify:02X} msg_hi=0x{msg_hi:02X}")
    print(f"  msg_value=0x{msg_value:04X}")
    
    # Verify header
    assert verify == (msg_lo ^ 0xB7), f"Verify mismatch: {verify:#04x} != {msg_lo^0xB7:#04x}"
    
    # Decrypt to get plaintext
    msg = [msg_lo, msg_hi]
    dec = bytearray(pkt_len - 10)
    for i in range(10, pkt_len):
        table_b = CMSG_TABLE[i % 7]
        sk_b = sk_bytes[i % 4]
        msg_b = msg[i % 2]
        intermediate = (raw[i] ^ sk_b ^ table_b) & 0xFF
        dec[i - 10] = (intermediate - msg_b * 17) & 0xFF
    print(f"  Decoded: {dec.hex()}")
    assert bytes(dec) == EXPECTED_PLAIN, f"Plaintext mismatch!"
    
    # NOW: encode with our encode_offset6 and compare
    codec = CMsgCodec.from_u32(sk)
    our_pkt = codec.encode_offset6(0x1B8B, EXPECTED_PLAIN, extra=extra, msg_value=msg_value)
    
    print(f"  OURS: {our_pkt.hex()}")
    print(f"  MATCH: {our_pkt == raw}")
    
    if our_pkt != raw:
        for i in range(max(len(raw), len(our_pkt))):
            p = raw[i] if i < len(raw) else None
            o = our_pkt[i] if i < len(our_pkt) else None
            if p != o:
                print(f"    DIFF at [{i}]: pcap=0x{p:02X} ours=0x{o:02X}")
    else:
        print(f"  *** BYTE-PERFECT MATCH ***")

print("\n\nSUMMARY: All 6 PCAPs tested.")

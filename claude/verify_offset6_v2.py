#!/usr/bin/env python3
"""Verify encode_offset6 against FRESH correct PCAP raw bytes for ALL 6 PCAPs."""
import struct, sys
sys.path.insert(0, r'D:\CascadeProjects\claude')
from codec import CMsgCodec

CMSG_TABLE = [0x58, 0xEF, 0xD7, 0x14, 0xA2, 0x3B, 0x9C]
EXPECTED_PLAIN = bytes.fromhex("ED02732200000000FFFFFFFFFFFFFFFF")

# FRESH extraction from extract_1b8b_raw.py
PCAPS = [
    {"name": "PCAP1", "sk": 0x02677C7E, "raw": "1a008b1b6cd2d690276f0ec14661afb239374a676d7a078be580"},
    {"name": "PCAP2", "sk": 0xB4B19AD1, "raw": "1a008b1b5d92bab700a1b1a570d5ceea213f353f6b7278d3e388"},
    {"name": "PCAP3", "sk": 0x88587D29, "raw": "1a008b1bda3d3e3a8d3a8bf65f1ddabd24b3236a6cfc6e86e406"},
    {"name": "PCAP4", "sk": 0x0B46E321, "raw": "1a008b1b07921a19aed6c4910627b7d25fc14c05158e01e99d74"},
    {"name": "PCAP5", "sk": 0x61607E47, "raw": "1a008b1b9aee68c473cc854d0b4c3c0294e6c1d1d8ad8c3d5057"},
    {"name": "PCAP6", "sk": 0xBDC1617D, "raw": "1a008b1b445212d86f1f900e8dccc15df27a3488b63779643ecd"},
]

all_match = True
for p in PCAPS:
    raw = bytes.fromhex(p["raw"])
    sk = p["sk"]
    sk_bytes = [(sk >> (8*i)) & 0xFF for i in range(4)]
    
    # Parse offset6 header
    extra = bytes([raw[4], raw[5]])
    msg_lo = raw[7]
    msg_hi = raw[9]
    msg_value = (msg_hi << 8) | msg_lo
    
    # Decrypt to verify plaintext
    msg = [msg_lo, msg_hi]
    dec = bytearray(len(raw) - 10)
    for i in range(10, len(raw)):
        table_b = CMSG_TABLE[i % 7]
        sk_b = sk_bytes[i % 4]
        msg_b = msg[i % 2]
        intermediate = (raw[i] ^ sk_b ^ table_b) & 0xFF
        dec[i - 10] = (intermediate - msg_b * 17) & 0xFF
    
    plain_ok = bytes(dec) == EXPECTED_PLAIN
    
    # Encode with our codec
    codec = CMsgCodec.from_u32(sk)
    our_pkt = codec.encode_offset6(0x1B8B, EXPECTED_PLAIN, extra=extra, msg_value=msg_value)
    
    match = our_pkt == raw
    if not match:
        all_match = False
    
    print(f"{p['name']} SK=0x{sk:08X} msg=0x{msg_value:04X} extra={extra.hex()}")
    print(f"  Plain: {dec.hex()} {'✓' if plain_ok else '✗'}")
    print(f"  PCAP: {raw.hex()}")
    print(f"  OURS: {our_pkt.hex()}")
    print(f"  {'*** BYTE-PERFECT MATCH ***' if match else '*** MISMATCH ***'}")
    
    if not match:
        for i in range(max(len(raw), len(our_pkt))):
            pb = raw[i] if i < len(raw) else None
            ob = our_pkt[i] if i < len(our_pkt) else None
            if pb != ob:
                print(f"    DIFF [{i}]: pcap=0x{pb:02X} ours=0x{ob:02X}")
    print()

print(f"ALL MATCH: {all_match}")

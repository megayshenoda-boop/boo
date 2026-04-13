#!/usr/bin/env python3
"""Verify codec.encode() produces byte-perfect match against PCAP packets."""
import sys
sys.path.insert(0, r'D:\CascadeProjects\claude')
from codec import CMsgCodec

# PCAP 4 (28_Mar_10_41_12) exact values
SK = 0x0B46E321
PLAIN = bytes.fromhex('017f93f7491700000039026a0301e2000000b60000000400000000000000000000ed027322000000000000000000')
MSG_VALUE = 0xBFDA
PCAP_RAW = bytes.fromhex('3600e80c75da6dbfb51a5f0fd9b9644b8c1f9829c00bf5734fee4d3803a3efb0f977a0fcb49b280660e362c66a589e9fc714d3734fee')

codec = CMsgCodec.from_u32(SK)
our_pkt = codec.encode(0x0CE8, PLAIN, msg_value=MSG_VALUE)

print(f'PCAP:  {PCAP_RAW.hex()}')
print(f'OURS:  {our_pkt.hex()}')
print(f'MATCH: {our_pkt == PCAP_RAW}')

if our_pkt != PCAP_RAW:
    for i in range(max(len(PCAP_RAW), len(our_pkt))):
        p = PCAP_RAW[i] if i < len(PCAP_RAW) else None
        o = our_pkt[i] if i < len(our_pkt) else None
        if p != o:
            print(f'  DIFF at [{i}]: pcap=0x{p:02X} ours=0x{o:02X}')
else:
    print('*** BYTE-PERFECT MATCH ***')

# Also verify 0x0CEB from same PCAP
print()
CEB_RAW = bytes.fromhex('1200eb0ccd3c8b32330bac6c042de2b60aa4')
CEB_PLAIN = bytes.fromhex('01ed0273220000000001')
CEB_MSG = (0x32 << 8) | 0x3C  # msg_hi=0x32, msg_lo=0x3C
our_ceb = codec.encode(0x0CEB, CEB_PLAIN, msg_value=CEB_MSG)
print(f'0x0CEB PCAP:  {CEB_RAW.hex()}')
print(f'0x0CEB OURS:  {our_ceb.hex()}')
print(f'0x0CEB MATCH: {our_ceb == CEB_RAW}')
if our_ceb != CEB_RAW:
    for i in range(max(len(CEB_RAW), len(our_ceb))):
        p = CEB_RAW[i] if i < len(CEB_RAW) else None
        o = our_ceb[i] if i < len(our_ceb) else None
        if p != o:
            print(f'  DIFF at [{i}]: pcap=0x{p:02X} ours=0x{o:02X}')
else:
    print('*** 0x0CEB BYTE-PERFECT MATCH ***')

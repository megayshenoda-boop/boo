#!/usr/bin/env python3
"""Extract ALL C2S packet payloads from game server connection in a PCAP file.

Reassembles the TCP stream from client->server direction by sorting packets
by sequence number, then parses game packets from the reassembled buffer.

Game packet format: [2B LE length][2B LE opcode][payload]
"""

import struct
import sys
from scapy.all import rdpcap, TCP, IP

PCAP_FILE = r"D:\CascadeProjects\PCAPdroid_27_Mar_09_17_04.pcap"
SERVER_IP = "54.93.175.57"
SERVER_PORT = 7001
CLIENT_IP = "10.215.173.1"
CLIENT_PORT = 58240


def main():
    print(f"Reading {PCAP_FILE} ...")
    packets = rdpcap(PCAP_FILE)
    print(f"Total packets in PCAP: {len(packets)}")

    # Collect C2S TCP segments (client -> server)
    segments = []  # list of (seq, payload_bytes)
    for pkt in packets:
        if not pkt.haslayer(IP) or not pkt.haslayer(TCP):
            continue
        ip = pkt[IP]
        tcp = pkt[TCP]
        # C2S: src=client, dst=server
        if (ip.src == CLIENT_IP and ip.dst == SERVER_IP and
                tcp.sport == CLIENT_PORT and tcp.dport == SERVER_PORT):
            payload = bytes(tcp.payload)
            if len(payload) > 0:
                segments.append((tcp.seq, payload))

    if not segments:
        print("No C2S segments found!")
        sys.exit(1)

    print(f"Found {len(segments)} C2S TCP segments with data")

    # Sort by sequence number and reassemble
    segments.sort(key=lambda x: x[0])

    # Deduplicate overlapping/retransmitted segments
    stream = bytearray()
    next_seq = segments[0][0]
    for seq, data in segments:
        if seq >= next_seq:
            # Gap or exact continuation
            if seq > next_seq:
                # There's a gap - fill or just append (gaps shouldn't happen in clean capture)
                pass
            stream.extend(data)
            next_seq = seq + len(data)
        elif seq + len(data) > next_seq:
            # Overlapping retransmit - take only the new part
            overlap = next_seq - seq
            stream.extend(data[overlap:])
            next_seq = next_seq + len(data) - overlap

    print(f"Reassembled C2S stream: {len(stream)} bytes")
    print("=" * 80)

    # Parse game packets from the stream
    offset = 0
    idx = 0
    while offset + 4 <= len(stream):
        pkt_len = struct.unpack_from('<H', stream, offset)[0]
        opcode = struct.unpack_from('<H', stream, offset + 2)[0]

        # Sanity check
        if pkt_len < 4 or pkt_len > 65535:
            print(f"[!] Bad packet length {pkt_len} at offset {offset}, stopping.")
            break

        if offset + pkt_len > len(stream):
            remaining = len(stream) - offset
            print(f"[!] Incomplete packet at offset {offset}: need {pkt_len} bytes, have {remaining}. Stopping.")
            break

        payload = stream[offset + 4 : offset + pkt_len]
        payload_hex = payload.hex() if len(payload) > 0 else "(empty)"

        print(f"Pkt #{idx:4d} | Opcode: 0x{opcode:04X} | Len: {pkt_len:5d} | Payload ({pkt_len - 4} bytes): {payload_hex}")

        offset += pkt_len
        idx += 1

    print("=" * 80)
    print(f"Total C2S game packets parsed: {idx}")
    if offset < len(stream):
        print(f"Remaining unparsed bytes: {len(stream) - offset}")


if __name__ == "__main__":
    main()

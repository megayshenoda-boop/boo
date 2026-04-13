"""Decode the fresh gather PCAP capture from the emulator"""
import struct
import sys
import os

# Try to use scapy for PCAP parsing
try:
    from scapy.all import rdpcap, TCP, Raw
    HAS_SCAPY = True
except ImportError:
    HAS_SCAPY = False

PCAP_FILE = r"d:\CascadeProjects\claude\gather_capture.pcap"

def parse_pcap_raw(filepath):
    """Parse PCAP file manually without scapy"""
    with open(filepath, 'rb') as f:
        # PCAP global header (24 bytes)
        magic = f.read(4)
        if magic == b'\xd4\xc3\xb2\xa1':
            endian = '<'
        elif magic == b'\xa1\xb2\xc3\xd4':
            endian = '>'
        else:
            print(f"Not a PCAP file! Magic: {magic.hex()}")
            return []
        
        ver_major, ver_minor, tz, sigfigs, snaplen, network = struct.unpack(endian + 'HHIIII', f.read(20))
        print(f"PCAP: v{ver_major}.{ver_minor}, snaplen={snaplen}, linktype={network}")
        
        packets = []
        pkt_num = 0
        while True:
            hdr = f.read(16)
            if len(hdr) < 16:
                break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
            data = f.read(incl_len)
            if len(data) < incl_len:
                break
            pkt_num += 1
            packets.append((pkt_num, ts_sec, ts_usec, data, orig_len))
        
        return packets

def extract_tcp_payload(pkt_data, linktype=113):
    """Extract TCP payload from raw packet data"""
    # Linux cooked capture (SLL) = linktype 113
    if linktype == 113:
        # SLL header: 16 bytes
        if len(pkt_data) < 16:
            return None, None
        pkt_type = struct.unpack('>H', pkt_data[0:2])[0]  # 0=incoming, 4=outgoing
        proto = struct.unpack('>H', pkt_data[14:16])[0]
        if proto != 0x0800:  # Not IPv4
            return None, None
        ip_start = 16
    else:
        # Ethernet (linktype 1)
        if len(pkt_data) < 14:
            return None, None
        proto = struct.unpack('>H', pkt_data[12:14])[0]
        if proto != 0x0800:
            return None, None
        ip_start = 14
        pkt_type = 0  # unknown direction
    
    # IP header
    if len(pkt_data) < ip_start + 20:
        return None, None
    ip_hdr = pkt_data[ip_start:]
    ip_ver_ihl = ip_hdr[0]
    ip_ihl = (ip_ver_ihl & 0x0F) * 4
    ip_proto = ip_hdr[9]
    ip_src = ip_hdr[12:16]
    ip_dst = ip_hdr[16:20]
    
    if ip_proto != 6:  # Not TCP
        return None, None
    
    # TCP header
    tcp_start = ip_start + ip_ihl
    if len(pkt_data) < tcp_start + 20:
        return None, None
    tcp_hdr = pkt_data[tcp_start:]
    src_port = struct.unpack('>H', tcp_hdr[0:2])[0]
    dst_port = struct.unpack('>H', tcp_hdr[2:4])[0]
    tcp_data_offset = ((tcp_hdr[12] >> 4) & 0xF) * 4
    
    payload_start = tcp_start + tcp_data_offset
    payload = pkt_data[payload_start:]
    
    # Direction: outgoing to port 7001 = C2S, from port 7001 = S2C
    if dst_port == 7001:
        direction = "C2S"
    elif src_port == 7001:
        direction = "S2C"
    else:
        direction = f"{src_port}->{dst_port}"
    
    # SLL pkt_type can also help
    if linktype == 113:
        if pkt_type == 4:
            direction = "C2S"
        elif pkt_type == 0:
            direction = "S2C"
    
    return direction, payload

def parse_game_packets(direction, tcp_payload):
    """Parse game protocol packets from TCP payload"""
    packets = []
    offset = 0
    while offset + 4 <= len(tcp_payload):
        pkt_len = struct.unpack('<H', tcp_payload[offset:offset+2])[0]
        opcode = struct.unpack('<H', tcp_payload[offset+2:offset+4])[0]
        
        if pkt_len < 4 or pkt_len > 10000:
            break
        if offset + pkt_len > len(tcp_payload):
            break
        
        payload = tcp_payload[offset+4:offset+pkt_len]
        packets.append((direction, opcode, payload, pkt_len))
        offset += pkt_len
    
    return packets

def main():
    packets = parse_pcap_raw(PCAP_FILE)
    print(f"Total PCAP packets: {len(packets)}\n")
    
    all_game_pkts = []
    
    for pkt_num, ts_sec, ts_usec, data, orig_len in packets:
        direction, tcp_payload = extract_tcp_payload(data)
        if tcp_payload and len(tcp_payload) > 0:
            game_pkts = parse_game_packets(direction, tcp_payload)
            for d, op, pl, plen in game_pkts:
                all_game_pkts.append((pkt_num, ts_sec, ts_usec, d, op, pl, plen))
    
    print(f"Game protocol packets: {len(all_game_pkts)}\n")
    print("=" * 90)
    
    for pkt_num, ts_sec, ts_usec, d, op, pl, plen in all_game_pkts:
        ts = f"{ts_usec/1000000:.3f}"
        hex_preview = pl[:60].hex() if pl else ""
        
        marker = ""
        if op == 0x0CE8: marker = " *** GATHER! ***"
        elif op == 0x0323: marker = " *** HERO_SELECT! ***"
        elif op == 0x006E: marker = " *** TILE_SELECT ***"
        elif op == 0x0CEB: marker = " *** ENABLE_VIEW ***"
        elif op == 0x099D: marker = " *** TROOP_SELECT ***"
        elif op == 0x0042: marker = " (heartbeat)"
        elif op == 0x00B8: marker = " *** MARCH_ACCEPT ***"
        elif op == 0x00B9: marker = " *** MARCH_ACK ***"
        elif op == 0x0071: marker = " *** MARCH_STATE ***"
        elif op == 0x076C: marker = " *** MARCH_BUNDLE ***"
        elif op == 0x007C: marker = " *** COLLECT_STATE ***"
        elif op == 0x0245: marker = " (march_screen)"
        elif op == 0x0834: marker = " (formation)"
        
        print(f"#{pkt_num:3d} {d} 0x{op:04X} {plen:4d}B {hex_preview[:80]}{marker}")
    
    # Detailed dump of key packets
    print("\n" + "=" * 90)
    print("DETAILED KEY PACKETS:")
    print("=" * 90)
    
    for pkt_num, ts_sec, ts_usec, d, op, pl, plen in all_game_pkts:
        if op in (0x0CE8, 0x0323, 0x099D, 0x006E, 0x0CEB, 0x00B8, 0x00B9, 0x0071, 0x076C, 0x007C, 0x0245, 0x0834):
            print(f"\n### #{pkt_num} {d} 0x{op:04X} ({len(pl)}B payload)")
            # Print full hex
            for i in range(0, len(pl), 32):
                chunk = pl[i:i+32]
                hex_str = ' '.join(f'{b:02x}' for b in chunk)
                print(f"  [{i:3d}] {hex_str}")

if __name__ == '__main__':
    main()

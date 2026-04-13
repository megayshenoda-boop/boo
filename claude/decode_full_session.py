"""Decode full session PCAP - extract SK from login, decrypt 0x0CE8"""
import struct, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from codec import CMsgCodec

PCAP_FILE = r"d:\CascadeProjects\claude\full_session.pcap"
CMSG_TABLE = [0x8B, 0x3A, 0xF1, 0x65, 0xCE, 0x07, 0x52]

def parse_pcap(filepath):
    with open(filepath, 'rb') as f:
        magic = f.read(4)
        endian = '<' if magic == b'\xd4\xc3\xb2\xa1' else '>'
        f.read(20)  # rest of global header
        packets = []
        while True:
            hdr = f.read(16)
            if len(hdr) < 16: break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
            data = f.read(incl_len)
            if len(data) < incl_len: break
            packets.append((ts_sec, ts_usec, data))
    return packets

def extract_tcp(pkt_data):
    """Extract direction and TCP payload from SLL frame"""
    if len(pkt_data) < 16: return None, None, None, None
    pkt_type = struct.unpack('>H', pkt_data[0:2])[0]
    proto = struct.unpack('>H', pkt_data[14:16])[0]
    if proto != 0x0800: return None, None, None, None
    
    ip_start = 16
    if len(pkt_data) < ip_start + 20: return None, None, None, None
    ip_ihl = (pkt_data[ip_start] & 0x0F) * 4
    if pkt_data[ip_start + 9] != 6: return None, None, None, None  # not TCP
    
    tcp_start = ip_start + ip_ihl
    if len(pkt_data) < tcp_start + 20: return None, None, None, None
    src_port = struct.unpack('>H', pkt_data[tcp_start:tcp_start+2])[0]
    dst_port = struct.unpack('>H', pkt_data[tcp_start+2:tcp_start+4])[0]
    tcp_off = ((pkt_data[tcp_start + 12] >> 4) & 0xF) * 4
    payload = pkt_data[tcp_start + tcp_off:]
    
    if dst_port in (5997, 7001):
        direction = "C2S"
    elif src_port in (5997, 7001):
        direction = "S2C"
    else:
        return None, None, None, None
    
    return direction, payload, src_port, dst_port

def parse_game_packets(tcp_payload):
    """Parse multiple game packets from TCP stream"""
    pkts = []
    off = 0
    while off + 4 <= len(tcp_payload):
        pkt_len = struct.unpack('<H', tcp_payload[off:off+2])[0]
        opcode = struct.unpack('<H', tcp_payload[off+2:off+4])[0]
        if pkt_len < 4 or pkt_len > 50000 or off + pkt_len > len(tcp_payload):
            break
        payload = tcp_payload[off+4:off+pkt_len]
        pkts.append((opcode, payload))
        off += pkt_len
    return pkts

def main():
    raw_packets = parse_pcap(PCAP_FILE)
    print(f"Raw PCAP packets: {len(raw_packets)}")
    
    # Reassemble TCP streams
    c2s_buffer = bytearray()
    s2c_buffer = bytearray()
    game_port = None
    sk = None
    codec = None
    
    all_game_pkts = []
    
    for ts_sec, ts_usec, data in raw_packets:
        direction, tcp_payload, src_port, dst_port = extract_tcp(data)
        if not tcp_payload or len(tcp_payload) == 0:
            continue
        
        # Parse game packets from this TCP segment
        game_pkts = parse_game_packets(tcp_payload)
        
        for opcode, payload in game_pkts:
            ts_str = f"{ts_sec % 86400 // 3600:02d}:{ts_sec % 3600 // 60:02d}:{ts_sec % 60:02d}.{ts_usec//1000:03d}"
            
            all_game_pkts.append((ts_str, direction, opcode, payload))
            
            # Extract SK from login response (S2C 0x0014)
            if direction == "S2C" and opcode == 0x0014 and len(payload) >= 4:
                sk = struct.unpack('<I', payload[0:4])[0]
                print(f"\n*** FOUND SK: 0x{sk:08X} ***\n")
                codec = CMsgCodec(sk)
    
    print(f"Total game packets: {len(all_game_pkts)}")
    
    # Print all C2S packets and important S2C
    print("\n" + "=" * 90)
    print("SESSION PACKETS (filtered):")
    print("=" * 90)
    
    for ts, d, op, pl in all_game_pkts:
        marker = ""
        show = False
        
        if d == "C2S" and op != 0x0042:
            show = True
        if op == 0x0CE8: marker = " *** GATHER! ***"; show = True
        elif op == 0x0323: marker = " *** HERO_SELECT ***"; show = True
        elif op == 0x006E: marker = " *** TILE_SELECT ***"; show = True
        elif op == 0x0CEB: marker = " *** ENABLE_VIEW ***"; show = True
        elif op == 0x099D: marker = " *** TROOP_SELECT ***"; show = True
        elif op == 0x0834: marker = " *** FORMATION ***"; show = True
        elif op == 0x0245: marker = " *** MARCH_SCREEN ***"; show = True
        elif op == 0x033E: marker = " *** SEARCH ***"; show = True
        elif op == 0x00B8: marker = " *** MARCH_ACCEPT ***"; show = True
        elif op == 0x00B9: marker = " *** MARCH_ACK ***"; show = True
        elif op == 0x0071: marker = " *** MARCH_STATE ***"; show = True
        elif op == 0x076C: marker = " *** MARCH_BUNDLE ***"; show = True
        elif op == 0x007C: marker = " *** COLLECT ***"; show = True
        elif op == 0x0014: marker = " *** LOGIN_RESP ***"; show = True
        elif op == 0x0033: marker = " (attr_change)"; show = True
        elif op == 0x0037: marker = " (extra_attr)"; show = True
        
        if show:
            hex_preview = pl[:40].hex() if pl else ""
            print(f"  {ts} {d} 0x{op:04X} {len(pl)+4:4d}B {hex_preview}{marker}")
    
    # Now decrypt 0x0CE8 if we have the codec
    if codec:
        print("\n" + "=" * 90)
        print("DECRYPTED KEY PACKETS:")
        print("=" * 90)
        
        for ts, d, op, pl in all_game_pkts:
            if d == "C2S" and op in (0x0CE8, 0x0CEB, 0x0323):
                try:
                    plain = codec.decode(pl)
                    if plain is not None:
                        print(f"\n### {ts} C2S 0x{op:04X} - DECRYPTED ({len(plain)}B):")
                        for i in range(0, len(plain), 32):
                            chunk = plain[i:i+32]
                            hex_str = ' '.join(f'{b:02x}' for b in chunk)
                            print(f"  [{i:3d}] {hex_str}")
                        
                        if op == 0x0CE8 and len(plain) >= 46:
                            print(f"\n  GATHER PAYLOAD DECODE:")
                            print(f"    slot      = {plain[0]}")
                            print(f"    nonce     = {plain[1:4].hex()}")
                            print(f"    march_type= 0x{struct.unpack('<H', plain[4:6])[0]:04X}")
                            print(f"    tile_x    = {struct.unpack('<H', plain[9:11])[0]}")
                            print(f"    tile_y    = {struct.unpack('<H', plain[11:13])[0]}")
                            print(f"    flag      = {plain[13]}")
                            print(f"    hero_id   = {plain[14]} (0x{plain[14]:02X})")
                            print(f"    kingdom   = {plain[18]}")
                            print(f"    purpose   = {plain[22]}")
                            print(f"    igg_id    = {struct.unpack('<I', plain[33:37])[0]}")
                            
                            # Compare with our bot's payload
                            print(f"\n  FULL HEX: {plain.hex()}")
                    else:
                        print(f"\n### {ts} C2S 0x{op:04X} - DECODE FAILED (pl={pl[:20].hex()})")
                except Exception as e:
                    print(f"\n### {ts} C2S 0x{op:04X} - ERROR: {e}")
            
            # Also show raw S2C march responses
            if d == "S2C" and op in (0x0071, 0x076C, 0x007C, 0x00B8, 0x00B9):
                print(f"\n### {ts} S2C 0x{op:04X} ({len(pl)}B):")
                for i in range(0, min(len(pl), 128), 32):
                    chunk = pl[i:i+32]
                    hex_str = ' '.join(f'{b:02x}' for b in chunk)
                    print(f"  [{i:3d}] {hex_str}")

if __name__ == '__main__':
    main()

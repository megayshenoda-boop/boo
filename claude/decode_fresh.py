"""Decode fresh session - full login + gather"""
import struct, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from codec import CMsgCodec

PCAP_FILE = r"d:\CascadeProjects\claude\fresh_session.pcap"

def parse_pcap(filepath):
    with open(filepath, 'rb') as f:
        magic = f.read(4)
        endian = '<' if magic == b'\xd4\xc3\xb2\xa1' else '>'
        f.read(20)
        packets = []
        while True:
            hdr = f.read(16)
            if len(hdr) < 16: break
            ts_sec, ts_usec, incl_len, _ = struct.unpack(endian + 'IIII', hdr)
            data = f.read(incl_len)
            if len(data) < incl_len: break
            packets.append((ts_sec, ts_usec, data))
    return packets

def extract_tcp(pkt_data):
    if len(pkt_data) < 16: return None, None, None, None
    proto = struct.unpack('>H', pkt_data[14:16])[0]
    if proto != 0x0800: return None, None, None, None
    ip_start = 16
    if len(pkt_data) < ip_start + 20: return None, None, None, None
    ip_ihl = (pkt_data[ip_start] & 0x0F) * 4
    if pkt_data[ip_start + 9] != 6: return None, None, None, None
    tcp_start = ip_start + ip_ihl
    if len(pkt_data) < tcp_start + 20: return None, None, None, None
    src_port = struct.unpack('>H', pkt_data[tcp_start:tcp_start+2])[0]
    dst_port = struct.unpack('>H', pkt_data[tcp_start+2:tcp_start+4])[0]
    tcp_off = ((pkt_data[tcp_start + 12] >> 4) & 0xF) * 4
    payload = pkt_data[tcp_start + tcp_off:]
    if dst_port in (5997, 7001): d = "C2S"
    elif src_port in (5997, 7001): d = "S2C"
    else: return None, None, None, None
    port = dst_port if d == "C2S" else src_port
    return d, payload, port, (src_port, dst_port)

def parse_game_packets(tcp_payload):
    pkts = []
    off = 0
    while off + 4 <= len(tcp_payload):
        pkt_len = struct.unpack('<H', tcp_payload[off:off+2])[0]
        opcode = struct.unpack('<H', tcp_payload[off+2:off+4])[0]
        if pkt_len < 4 or pkt_len > 50000 or off + pkt_len > len(tcp_payload): break
        payload = tcp_payload[off+4:off+pkt_len]
        pkts.append((opcode, payload))
        off += pkt_len
    return pkts

def check_codec(pl):
    if len(pl) < 4: return False
    return pl[2] == ((pl[1] ^ 0xB7) & 0xFF)

def main():
    raw = parse_pcap(PCAP_FILE)
    print(f"Raw PCAP packets: {len(raw)}")
    
    all_pkts = []
    sk = None
    codec = None
    
    for ts_sec, ts_usec, data in raw:
        result = extract_tcp(data)
        if not result[0]: continue
        d, payload, port, ports = result
        if len(payload) == 0: continue
        game_pkts = parse_game_packets(payload)
        for op, pl in game_pkts:
            all_pkts.append((ts_sec, ts_usec, d, op, pl, port))
            
            # Find SK from login response
            if d == "S2C" and op == 0x0014 and len(pl) >= 4:
                sk = struct.unpack('<I', pl[0:4])[0]
                codec = CMsgCodec(sk)
                print(f"*** FOUND SK: 0x{sk:08X} ***")
    
    print(f"Game packets: {len(all_pkts)}")
    
    if not codec:
        print("\n!!! NO SK FOUND - checking all S2C packets for potential SK !!!")
        for ts_sec, ts_usec, d, op, pl, port in all_pkts:
            if d == "S2C":
                ts = f"{ts_sec % 3600 // 60:02d}:{ts_sec % 60:02d}.{ts_usec//1000:03d}"
                print(f"  {ts} p={port} 0x{op:04X} {len(pl)+4:4d}B {pl[:30].hex() if pl else ''}")
                if len(all_pkts) > 200:
                    # Just first 30
                    pass
    
    # Print ALL C2S (non-heartbeat)
    print("\n" + "=" * 90)
    print("C2S PACKETS:")
    print("=" * 90)
    for ts_sec, ts_usec, d, op, pl, port in all_pkts:
        if d == "C2S" and op != 0x0042:
            ts = f"{ts_sec % 3600 // 60:02d}:{ts_sec % 60:02d}.{ts_usec//1000:03d}"
            enc = "ENC" if check_codec(pl) else "   "
            marker = ""
            if op == 0x0CE8: marker = " <<< GATHER_0CE8"
            elif op == 0x0CE7: marker = " <<< GATHER_0CE7"
            elif op == 0x0323: marker = " <<< HERO_SELECT"
            elif op == 0x006E: marker = " <<< TILE"
            elif op == 0x099D: marker = " <<< TROOP"
            elif op == 0x0CEB: marker = " <<< VIEW"
            elif op == 0x0245: marker = " <<< MARCH_SCREEN"
            elif op == 0x0834: marker = " <<< FORMATION"
            elif op == 0x033E: marker = " <<< SEARCH"
            elif op == 0x000B: marker = " <<< GATEWAY_LOGIN"
            elif op == 0x0014: marker = " <<< GAME_LOGIN"
            elif op == 0x1B8B: marker = " <<< PASSWORD"
            print(f"  {ts} p={port} 0x{op:04X} {len(pl)+4:4d}B {enc} {pl[:30].hex() if pl else ''}{marker}")
    
    # March-related S2C
    print("\n" + "=" * 90)
    print("MARCH S2C:")
    print("=" * 90)
    for ts_sec, ts_usec, d, op, pl, port in all_pkts:
        if d == "S2C" and op in (0x0014, 0x00B8, 0x00B9, 0x0071, 0x076C, 0x007C, 0x0033, 0x0037):
            ts = f"{ts_sec % 3600 // 60:02d}:{ts_sec % 60:02d}.{ts_usec//1000:03d}"
            marker = {0x0014:"LOGIN_RESP",0x00B8:"MARCH_ACCEPT",0x00B9:"ARMY_RETURN",
                      0x0071:"MARCH_STATE",0x076C:"MARCH_BUNDLE",0x007C:"COLLECT"}.get(op,"")
            print(f"  {ts} 0x{op:04X} {len(pl)+4:4d}B {marker} {pl[:40].hex() if pl else ''}")
    
    # Decrypt gather packets
    if codec:
        print("\n" + "=" * 90)
        print("DECRYPTED PACKETS:")
        print("=" * 90)
        
        for ts_sec, ts_usec, d, op, pl, port in all_pkts:
            if d == "C2S" and op in (0x0CE8, 0x0CE7, 0x0CEB, 0x0323) and check_codec(pl):
                try:
                    plain = codec.decode(pl)
                    name = {0x0CE8:"GATHER_NEW",0x0CE7:"GATHER_0CE7",0x0CEB:"ENABLE_VIEW",0x0323:"HERO_SELECT"}.get(op,"?")
                    print(f"\n### 0x{op:04X} {name} - plaintext ({len(plain)}B):")
                    print(f"  HEX: {plain.hex()}")
                    for i in range(0, len(plain), 16):
                        chunk = plain[i:i+16]
                        hex_str = ' '.join(f'{b:02x}' for b in chunk)
                        print(f"  [{i:3d}] {hex_str}")
                    
                    if op == 0x0CE8 and len(plain) >= 46:
                        print(f"\n  slot={plain[0]} nonce={plain[1:4].hex()} type=0x{struct.unpack('<H',plain[4:6])[0]:04X}")
                        print(f"  tile=({struct.unpack('<H',plain[9:11])[0]},{struct.unpack('<H',plain[11:13])[0]}) flag={plain[13]} hero={plain[14]}")
                        print(f"  kingdom={plain[18]} purpose={plain[22]} igg={struct.unpack('<I',plain[33:37])[0]}")
                    
                    if op == 0x0CE7:
                        print(f"\n  0x0CE7 plaintext analysis:")
                        if len(plain) >= 2:
                            print(f"  Bytes: {' '.join(f'{b:02x}' for b in plain)}")
                            for i in range(0, len(plain)-1, 2):
                                val = struct.unpack('<H', plain[i:i+2])[0]
                                print(f"  u16@{i}: {val} (0x{val:04X})")
                            if len(plain) >= 4:
                                for i in range(0, len(plain)-3, 4):
                                    val = struct.unpack('<I', plain[i:i+4])[0]
                                    print(f"  u32@{i}: {val} (0x{val:08X})")
                except Exception as e:
                    print(f"\n### 0x{op:04X} DECODE ERROR: {e}")
    
    # Also check: does 0x0CE7 exist in opcode map?
    print("\n" + "=" * 90)
    print("ALL UNIQUE C2S OPCODES:")
    print("=" * 90)
    ops = {}
    for _, _, d, op, _, _ in all_pkts:
        if d == "C2S": ops[op] = ops.get(op, 0) + 1
    for op in sorted(ops.keys()):
        print(f"  0x{op:04X}: {ops[op]}x")

if __name__ == '__main__':
    main()

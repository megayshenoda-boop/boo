"""Decode full session - find SK and decrypt everything"""
import struct, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from codec import CMsgCodec

PCAP_FILE = r"d:\CascadeProjects\claude\full_session.pcap"

def parse_pcap(filepath):
    with open(filepath, 'rb') as f:
        magic = f.read(4)
        endian = '<' if magic == b'\xd4\xc3\xb2\xa1' else '>'
        f.read(20)
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

def check_codec_header(pl):
    """Check if payload has valid CMsgCodec header"""
    if len(pl) < 4: return False
    verify = pl[1] ^ 0xB7
    return pl[2] == (verify & 0xFF)

def main():
    raw = parse_pcap(PCAP_FILE)
    print(f"Raw packets: {len(raw)}")
    
    all_pkts = []
    sk = None
    
    for ts_sec, ts_usec, data in raw:
        result = extract_tcp(data)
        if not result[0]: continue
        d, payload, port, ports = result
        if len(payload) == 0: continue
        
        game_pkts = parse_game_packets(payload)
        for op, pl in game_pkts:
            all_pkts.append((ts_sec, ts_usec, d, op, pl, port))
            
            # Find SK - try multiple login response opcodes
            if d == "S2C" and op == 0x0014 and len(pl) >= 4:
                sk = struct.unpack('<I', pl[0:4])[0]
                print(f"*** SK from 0x0014: 0x{sk:08X}")
            # Also check 0x000B response on gateway
            if d == "S2C" and op == 0x000C and len(pl) >= 4:
                print(f"*** Gateway resp 0x000C ({len(pl)}B): {pl[:20].hex()}")
    
    print(f"Total game packets: {len(all_pkts)}")
    
    # Show ALL unique opcodes
    c2s_ops = {}
    s2c_ops = {}
    for _, _, d, op, pl, _ in all_pkts:
        if d == "C2S": c2s_ops[op] = c2s_ops.get(op, 0) + 1
        else: s2c_ops[op] = s2c_ops.get(op, 0) + 1
    
    print(f"\nC2S opcodes ({len(c2s_ops)}):")
    for op in sorted(c2s_ops.keys()):
        print(f"  0x{op:04X}: {c2s_ops[op]}x")
    
    print(f"\nS2C opcodes ({len(s2c_ops)}):")
    for op in sorted(s2c_ops.keys()):
        if s2c_ops[op] <= 3 or op in (0x0071, 0x076C, 0x007C, 0x00B8, 0x00B9, 0x0014):
            print(f"  0x{op:04X}: {s2c_ops[op]}x")
    
    # Show ALL non-heartbeat C2S packets
    print("\n" + "=" * 90)
    print("ALL C2S PACKETS (non-heartbeat):")
    print("=" * 90)
    for ts_sec, ts_usec, d, op, pl, port in all_pkts:
        if d == "C2S" and op != 0x0042:
            ts = f"{ts_sec % 3600 // 60:02d}:{ts_sec % 60:02d}.{ts_usec//1000:03d}"
            codec_ok = "🔐" if check_codec_header(pl) else "  "
            print(f"  {ts} 0x{op:04X} {len(pl)+4:4d}B {codec_ok} {pl[:30].hex() if pl else ''}")
    
    # Show important S2C 
    print("\n" + "=" * 90)
    print("MARCH-RELATED S2C:")
    print("=" * 90)
    for ts_sec, ts_usec, d, op, pl, port in all_pkts:
        if d == "S2C" and op in (0x0014, 0x00B8, 0x00B9, 0x0071, 0x076C, 0x007C, 0x0033, 0x0037):
            ts = f"{ts_sec % 3600 // 60:02d}:{ts_sec % 60:02d}.{ts_usec//1000:03d}"
            print(f"  {ts} 0x{op:04X} {len(pl)+4:4d}B {pl[:40].hex() if pl else ''}")
    
    # Try to find SK from any packet pattern
    # The login flow: C2S 0x000B -> gateway -> redirect -> C2S 0x0014 login -> S2C 0x0014 with SK
    print("\n" + "=" * 90)
    print("LOOKING FOR SK IN FIRST 20 S2C PACKETS:")
    print("=" * 90)
    count = 0
    for ts_sec, ts_usec, d, op, pl, port in all_pkts:
        if d == "S2C" and count < 20:
            ts = f"{ts_sec % 3600 // 60:02d}:{ts_sec % 60:02d}.{ts_usec//1000:03d}"
            print(f"  {ts} port={port} 0x{op:04X} {len(pl)+4:4d}B {pl[:40].hex() if pl else ''}")
            count += 1

    # Check 0x0CE7 specifically
    print("\n" + "=" * 90)
    print("0x0CE7 ANALYSIS:")
    print("=" * 90)
    for ts_sec, ts_usec, d, op, pl, port in all_pkts:
        if op == 0x0CE7:
            print(f"  Direction: {d}")
            print(f"  Payload ({len(pl)}B): {pl.hex()}")
            print(f"  Codec header valid: {check_codec_header(pl)}")
            if check_codec_header(pl):
                print(f"  msg_lo=0x{pl[1]:02X} verify=0x{pl[2]:02X} (expected 0x{(pl[1]^0xB7)&0xFF:02X}) msg_hi=0x{pl[3]:02X}")
                print(f"  msg_idx = 0x{(pl[3]<<8)|pl[1]:04X}")
                print(f"  Encrypted body ({len(pl)-4}B): {pl[4:].hex()}")

if __name__ == '__main__':
    main()

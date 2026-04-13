"""Decode fresh session with proper TCP reassembly to find SK and decrypt 0x0CE8"""
import struct, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"d:\CascadeProjects\lords_bot")
from connection import CMsgCodec

PCAP_FILE = r"d:\CascadeProjects\claude\fresh_session.pcap"
SERVER_KEY_FIELD_ID = 0x4F

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
    """Returns (direction, payload, tcp_seq, src_port, dst_port)"""
    if len(pkt_data) < 16: return None
    proto = struct.unpack('>H', pkt_data[14:16])[0]
    if proto != 0x0800: return None
    ip_start = 16
    if len(pkt_data) < ip_start + 20: return None
    ip_ihl = (pkt_data[ip_start] & 0x0F) * 4
    if pkt_data[ip_start + 9] != 6: return None
    tcp_start = ip_start + ip_ihl
    if len(pkt_data) < tcp_start + 20: return None
    src_port = struct.unpack('>H', pkt_data[tcp_start:tcp_start+2])[0]
    dst_port = struct.unpack('>H', pkt_data[tcp_start+2:tcp_start+4])[0]
    tcp_seq = struct.unpack('>I', pkt_data[tcp_start+4:tcp_start+8])[0]
    tcp_off = ((pkt_data[tcp_start + 12] >> 4) & 0xF) * 4
    payload = pkt_data[tcp_start + tcp_off:]
    
    if dst_port in (5997, 7001): d = "C2S"
    elif src_port in (5997, 7001): d = "S2C"
    else: return None
    
    return (d, bytes(payload), tcp_seq, src_port, dst_port)

def extract_sk_from_0x0038(payload):
    """Extract server key from 0x0038 CASTLE_DATA"""
    if len(payload) < 14: return None
    entry_count = struct.unpack('<H', payload[0:2])[0]
    for idx in range(entry_count):
        off = 2 + idx * 12
        if off + 12 > len(payload): break
        field_id = struct.unpack('<I', payload[off:off+4])[0]
        if field_id == SERVER_KEY_FIELD_ID:
            return struct.unpack('<I', payload[off+4:off+8])[0]
    return None

def main():
    raw = parse_pcap(PCAP_FILE)
    print(f"Raw PCAP packets: {len(raw)}")
    
    # Reassemble TCP streams by direction
    c2s_stream = bytearray()
    s2c_stream = bytearray()
    
    for ts_sec, ts_usec, data in raw:
        result = extract_tcp(data)
        if not result: continue
        d, payload, seq, sp, dp = result
        if len(payload) == 0: continue
        if d == "C2S":
            c2s_stream.extend(payload)
        else:
            s2c_stream.extend(payload)
    
    print(f"C2S stream: {len(c2s_stream)} bytes")
    print(f"S2C stream: {len(s2c_stream)} bytes")
    
    # Parse game packets from reassembled streams
    def parse_stream(stream, label):
        pkts = []
        off = 0
        while off + 4 <= len(stream):
            pkt_len = struct.unpack('<H', stream[off:off+2])[0]
            opcode = struct.unpack('<H', stream[off+2:off+4])[0]
            if pkt_len < 4 or pkt_len > 50000:
                print(f"  [{label}] Bad packet at offset {off}: len={pkt_len} op=0x{opcode:04X}")
                # Try to resync
                off += 1
                continue
            if off + pkt_len > len(stream):
                break
            payload = bytes(stream[off+4:off+pkt_len])
            pkts.append((opcode, payload))
            off += pkt_len
        return pkts
    
    c2s_pkts = parse_stream(c2s_stream, "C2S")
    s2c_pkts = parse_stream(s2c_stream, "S2C")
    
    print(f"C2S packets: {len(c2s_pkts)}")
    print(f"S2C packets: {len(s2c_pkts)}")
    
    # Find SK from 0x0038
    sk = None
    codec = None
    for op, pl in s2c_pkts:
        if op == 0x0038:
            sk_candidate = extract_sk_from_0x0038(pl)
            if sk_candidate:
                sk = sk_candidate
                codec = CMsgCodec(struct.pack('<I', sk))
                print(f"\n*** FOUND SK: 0x{sk:08X} ***\n")
                break
    
    if not sk:
        # Also check: the game_state.py uses 0x0038 specifically
        print("\nSearching ALL S2C for field 0x4F...")
        for i, (op, pl) in enumerate(s2c_pkts):
            if op == 0x0038:
                print(f"  Found 0x0038 at index {i}, {len(pl)}B payload")
                sk_candidate = extract_sk_from_0x0038(pl)
                if sk_candidate:
                    sk = sk_candidate
                    codec = CMsgCodec(struct.pack('<I', sk))
                    print(f"  *** SK: 0x{sk:08X} ***")
    
    # Print S2C opcode summary
    s2c_ops = {}
    for op, pl in s2c_pkts:
        s2c_ops[op] = s2c_ops.get(op, 0) + 1
    print(f"\nS2C unique opcodes: {len(s2c_ops)}")
    for op in sorted(s2c_ops.keys()):
        count = s2c_ops[op]
        if count <= 5 or op in (0x0038, 0x00B8, 0x0071, 0x076C, 0x007C):
            print(f"  0x{op:04X}: {count}x")
    
    # Print C2S non-heartbeat
    print("\n" + "=" * 80)
    print("C2S PACKETS:")
    print("=" * 80)
    for op, pl in c2s_pkts:
        if op != 0x0042:
            marker = {0x0CE8:"GATHER!",0x0CE7:"GATHER_CE7!",0x0323:"HERO_SEL",
                      0x006E:"TILE",0x099D:"TROOP",0x0CEB:"VIEW",0x033E:"SEARCH",
                      0x0245:"MARCH_SCR",0x1B8B:"PASSWORD"}.get(op,"")
            print(f"  0x{op:04X} {len(pl)+4:4d}B {marker:12s} {pl[:30].hex() if pl else ''}")
    
    # Decrypt 0x0CE8 if we have codec
    if codec:
        print("\n" + "=" * 80)
        print("DECRYPTED GATHER PAYLOAD:")
        print("=" * 80)
        for op, pl in c2s_pkts:
            if op in (0x0CE8, 0x0CE7, 0x0CEB):
                # Check codec header
                if len(pl) >= 4 and pl[2] == ((pl[1] ^ 0xB7) & 0xFF):
                    dec = codec.decode(pl)
                    name = {0x0CE8:"GATHER_NEW",0x0CE7:"GATHER_CE7",0x0CEB:"ENABLE_VIEW"}.get(op,"?")
                    print(f"\n  0x{op:04X} ({name}) - decrypted ({len(dec)}B):")
                    print(f"  HEX: {dec.hex()}")
                    for i in range(0, len(dec), 16):
                        chunk = dec[i:i+16]
                        print(f"  [{i:3d}] {' '.join(f'{b:02x}' for b in chunk)}")
                    
                    if op == 0x0CE8 and len(dec) >= 46:
                        slot = dec[0]
                        mtype = struct.unpack('<H', dec[4:6])[0]
                        tx = struct.unpack('<H', dec[9:11])[0]
                        ty = struct.unpack('<H', dec[11:13])[0]
                        flag = dec[13]
                        hero = dec[14]
                        kingdom = dec[18]
                        purpose = dec[22]
                        igg = struct.unpack('<I', dec[33:37])[0]
                        print(f"\n  DECODED:")
                        print(f"    slot       = {slot}")
                        print(f"    march_type = 0x{mtype:04X}")
                        print(f"    tile       = ({tx}, {ty})")
                        print(f"    flag       = {flag}")
                        print(f"    hero_id    = {hero} (0x{hero:02X})")
                        print(f"    kingdom    = {kingdom}")
                        print(f"    purpose    = {purpose}")
                        print(f"    igg_id     = {igg}")
                        
                        # Compare with our bot's payload
                        print(f"\n  === COMPARISON WITH BOT ===")
                        print(f"    Bot sends:  slot=2 type=0x1749 hero=0xFF kingdom=182 purpose=4")
                        print(f"    Game sends: slot={slot} type=0x{mtype:04X} hero={hero} kingdom={kingdom} purpose={purpose}")
                else:
                    print(f"\n  0x{op:04X} - NOT codec encrypted? payload: {pl[:20].hex()}")
    else:
        print("\n!!! NO SK FOUND - Cannot decrypt !!!")
        # Try brute force from known S2C data
        print("Trying to find SK by checking all u32 values in 0x0038-like packets...")
        for op, pl in s2c_pkts:
            if len(pl) > 100 and len(pl) < 5000:
                # Check if this could be 0x0038
                if len(pl) >= 2:
                    ec = struct.unpack('<H', pl[0:2])[0]
                    if ec > 0 and ec < 500 and 2 + ec * 12 <= len(pl):
                        # Could be entry-based format
                        for idx in range(ec):
                            off = 2 + idx * 12
                            if off + 12 > len(pl): break
                            fid = struct.unpack('<I', pl[off:off+4])[0]
                            val = struct.unpack('<I', pl[off+4:off+8])[0]
                            if fid == SERVER_KEY_FIELD_ID:
                                print(f"  Found field 0x4F in 0x{op:04X}! Value=0x{val:08X}")
                                sk = val
                                codec = CMsgCodec(struct.pack('<I', sk))
                                # Try to decrypt 0x0CE8
                                for op2, pl2 in c2s_pkts:
                                    if op2 == 0x0CE8 and len(pl2) >= 4:
                                        if pl2[2] == ((pl2[1] ^ 0xB7) & 0xFF):
                                            dec = codec.decode(pl2)
                                            print(f"  DECRYPTED 0x0CE8: {dec.hex()}")

if __name__ == '__main__':
    main()

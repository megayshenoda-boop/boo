"""Deep decode - decrypt 0x1B8B, check 0x1B8A gate, analyze 0x1C87"""
import struct, sys, os
sys.path.insert(0, r"d:\CascadeProjects\lords_bot")
from connection import CMsgCodec
from protocol import CMSG_TABLE, SERVER_KEY_FIELD_ID

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
    tcp_off = ((pkt_data[tcp_start + 12] >> 4) & 0xF) * 4
    payload = pkt_data[tcp_start + tcp_off:]
    if dst_port in (5997, 7001): d = "C2S"
    elif src_port in (5997, 7001): d = "S2C"
    else: return None
    return (d, bytes(payload))

def parse_stream(stream):
    pkts = []
    off = 0
    while off + 4 <= len(stream):
        pkt_len = struct.unpack('<H', stream[off:off+2])[0]
        opcode = struct.unpack('<H', stream[off+2:off+4])[0]
        if pkt_len < 4 or pkt_len > 50000:
            off += 1; continue
        if off + pkt_len > len(stream): break
        payload = bytes(stream[off+4:off+pkt_len])
        pkts.append((opcode, payload))
        off += pkt_len
    return pkts

def extract_sk(payload):
    if len(payload) < 14: return None
    ec = struct.unpack('<H', payload[0:2])[0]
    for i in range(ec):
        off = 2 + i * 12
        if off + 12 > len(payload): break
        fid = struct.unpack('<I', payload[off:off+4])[0]
        if fid == SERVER_KEY_FIELD_ID:
            return struct.unpack('<I', payload[off+4:off+8])[0]
    return None

def decode_offset6(codec, payload):
    """Decode 0x1B8B offset6 format: [2B extra][4B codec_hdr][encrypted]"""
    if len(payload) < 6: return None
    extra = payload[0:2]
    hdr = payload[2:6]
    chk, msg_lo, verify, msg_hi = hdr[0], hdr[1], hdr[2], hdr[3]
    if verify != ((msg_lo ^ 0xB7) & 0xFF):
        return None  # not offset6
    
    msg = [msg_lo, msg_hi]
    encrypted = payload[6:]
    sk = codec.sk
    
    dec = bytearray(len(encrypted))
    for idx in range(len(encrypted)):
        abs_i = idx + 10
        table_b = CMSG_TABLE[abs_i % 7]
        sk_b = sk[abs_i % 4]
        msg_b = msg[abs_i % 2]
        intermediate = (encrypted[idx] ^ sk_b ^ table_b) & 0xFF
        plain_byte = (intermediate - msg_b * 17) & 0xFF
        dec[idx] = plain_byte
    
    return bytes(dec), extra, (msg_hi << 8 | msg_lo)

def main():
    raw = parse_pcap(PCAP_FILE)
    c2s = bytearray()
    s2c = bytearray()
    for _, _, data in raw:
        r = extract_tcp(data)
        if not r: continue
        d, pl = r
        if d == "C2S": c2s.extend(pl)
        else: s2c.extend(pl)
    
    c2s_pkts = parse_stream(c2s)
    s2c_pkts = parse_stream(s2c)
    
    # Find SK
    sk = None
    codec = None
    for op, pl in s2c_pkts:
        if op == 0x0038:
            sk = extract_sk(pl)
            if sk:
                codec = CMsgCodec(struct.pack('<I', sk))
                print(f"SK: 0x{sk:08X}")
                print(f"SK bytes: {struct.pack('<I', sk).hex()}")
                break
    
    if not codec:
        print("NO SK!"); return
    
    # === 1. Check 0x1B8A gate byte ===
    print("\n" + "=" * 60)
    print("0x1B8A (PASSWORD_INFO) from server:")
    print("=" * 60)
    for op, pl in s2c_pkts:
        if op == 0x1B8A:
            print(f"  Payload ({len(pl)}B): {pl.hex()}")
            if len(pl) >= 5:
                gate = pl[4]
                print(f"  gate byte [4] = {gate}")
                if gate == 0:
                    print(f"  gate=0 → DON'T send 0x1B8B")
                else:
                    print(f"  gate={gate} → MUST send 0x1B8B!")
    
    # === 2. Decode 0x1B8B from game client ===
    print("\n" + "=" * 60)
    print("0x1B8B (PASSWORD_CHECK) from game client:")
    print("=" * 60)
    for op, pl in c2s_pkts:
        if op == 0x1B8B:
            print(f"  Raw ({len(pl)}B): {pl.hex()}")
            
            # Try offset6 decode
            result = decode_offset6(codec, pl)
            if result:
                dec, extra, msg_idx = result
                print(f"  Offset6 decode SUCCESS!")
                print(f"  Extra: {extra.hex()}")
                print(f"  msg_idx: 0x{msg_idx:04X}")
                print(f"  Plaintext ({len(dec)}B): {dec.hex()}")
                
                if len(dec) >= 8:
                    igg = struct.unpack('<I', dec[0:4])[0]
                    print(f"  igg_id (u32 LE) = {igg} (0x{igg:08X})")
                    print(f"  seed32 = {dec[0:4].hex()}")
                if len(dec) >= 16:
                    pwd = struct.unpack('<q', dec[8:16])[0]
                    print(f"  password (i64 LE) = {pwd}")
                
                # Verify formulas from PCAP_1B8B_DECODED_AUDIT
                if len(dec) >= 18:
                    seed32 = dec[0:4]
                    x_lo = (seed32[2] + 0x13) & 0xFF
                    x_hi = (seed32[3] - 0x02) & 0xFF
                    print(f"  Formulas check:")
                    print(f"    seed32[2]=0x{seed32[2]:02X}, seed32[3]=0x{seed32[3]:02X}")
                    print(f"    x_lo = seed32[2] + 0x13 = 0x{x_lo:02X}")
                    print(f"    x_hi = seed32[3] - 0x02 = 0x{x_hi:02X}")
                    print(f"    x in plaintext = {dec[6:8].hex()}")
                    print(f"    Formula match: x_lo={dec[6]==x_lo}, x_hi={dec[7]==x_hi}")
            else:
                print(f"  Offset6 decode FAILED")
                # Try standard codec
                if len(pl) >= 4 and pl[2] == ((pl[1] ^ 0xB7) & 0xFF):
                    dec = codec.decode(pl)
                    print(f"  Standard decode: {dec.hex()}")
    
    # === 3. Analyze 0x1C87 ===
    print("\n" + "=" * 60)
    print("0x1C87 from game client:")
    print("=" * 60)
    for op, pl in c2s_pkts:
        if op == 0x1C87:
            print(f"  Raw ({len(pl)}B): {pl.hex()}")
            # Check if codec encrypted
            if len(pl) >= 4 and pl[2] == ((pl[1] ^ 0xB7) & 0xFF):
                print(f"  Standard CMsgCodec header valid!")
                dec = codec.decode(pl)
                print(f"  Standard Decrypted ({len(dec)}B): {dec.hex()}")
            else:
                print(f"  NOT standard codec encrypted")
                # Try NewEncode (offset6) format
                if len(pl) >= 10:
                    result = decode_offset6(codec, pl)
                    if result:
                        dec, extra, msg_idx = result
                        print(f"  NewEncode (offset6) SUCCESS!")
                        print(f"    Extra: {extra.hex()}")
                        print(f"    msg_idx: 0x{msg_idx:04X}")
                        print(f"    Decrypted ({len(dec)}B): {dec.hex()}")
                    else:
                        print(f"  NewEncode decode FAILED")
    
    # === 4. Show the actual gather comparison ===
    print("\n" + "=" * 60)
    print("GATHER COMPARISON:")
    print("=" * 60)
    for op, pl in c2s_pkts:
        if op == 0x0CE8:
            dec = codec.decode(pl)
            print(f"  GAME 0x0CE8 plaintext ({len(dec)}B): {dec.hex()}")
            
            # Build what the bot would send
            bot_plain = bytearray(46)
            bot_plain[0] = 2  # slot=2
            bot_plain[1:4] = bytes([0xAA, 0xBB, 0xCC])  # nonce
            struct.pack_into('<H', bot_plain, 4, 0x1749)  # march_type (food)
            struct.pack_into('<H', bot_plain, 9, 550)     # tile_x
            struct.pack_into('<H', bot_plain, 11, 851)    # tile_y
            bot_plain[13] = 0x01
            bot_plain[14] = 0xFF  # hero
            bot_plain[18] = 182   # kingdom
            bot_plain[22] = 0x04
            struct.pack_into('<I', bot_plain, 33, 577962733)  # igg_id
            print(f"  BOT  0x0CE8 plaintext ({len(bot_plain)}B): {bot_plain.hex()}")
            
            # Diff
            for i in range(46):
                if dec[i] != bot_plain[i]:
                    print(f"  DIFF at [{i}]: game=0x{dec[i]:02X} bot=0x{bot_plain[i]:02X}")

if __name__ == '__main__':
    main()

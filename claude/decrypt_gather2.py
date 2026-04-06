"""
Read fresh PCAP, extract server key from 0x0038, decrypt 0x0CE8 and 0x0CEB.
"""
import struct
import sys
sys.path.insert(0, r'D:\CascadeProjects\claude')

def read_pcap_game_stream(filepath):
    """Read PCAP and return concatenated game server TCP payload (both directions)."""
    with open(filepath, 'rb') as f:
        magic = struct.unpack('<I', f.read(4))[0]
        endian = '<' if magic == 0xa1b2c3d4 else '>'
        f.read(20)  # rest of global header

        streams = {}
        while True:
            hdr = f.read(16)
            if len(hdr) < 16:
                break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
            data = f.read(incl_len)
            if len(data) < incl_len:
                break

            # Raw IP (link type 101)
            ip_data = data
            if len(ip_data) < 20:
                continue
            ihl = (ip_data[0] & 0x0F) * 4
            protocol = ip_data[9]
            if protocol != 6:
                continue

            tcp = ip_data[ihl:]
            if len(tcp) < 20:
                continue
            src_port = struct.unpack('>H', tcp[0:2])[0]
            dst_port = struct.unpack('>H', tcp[2:4])[0]
            tcp_off = ((tcp[12] >> 4) & 0xF) * 4
            payload = tcp[tcp_off:]

            if len(payload) == 0:
                continue

            # Game server is on port 7001
            if src_port == 7001 or dst_port == 7001:
                direction = "C2S" if dst_port == 7001 else "S2C"
                key = direction
                if key not in streams:
                    streams[key] = bytearray()
                streams[key] += payload

    return streams


def parse_game_packets(raw_stream):
    """Parse game protocol packets from raw stream."""
    packets = []
    pos = 0
    while pos + 4 <= len(raw_stream):
        pkt_len = struct.unpack('<H', raw_stream[pos:pos+2])[0]
        opcode = struct.unpack('<H', raw_stream[pos+2:pos+4])[0]
        if pkt_len < 4 or pkt_len > 65535 or pos + pkt_len > len(raw_stream):
            break
        payload = raw_stream[pos+4:pos+pkt_len]
        packets.append((opcode, payload))
        pos += pkt_len
    return packets


# CMsgCodec
TABLE = [0x58, 0xef, 0xd7, 0x14, 0xa2, 0x3b, 0x9c]

def decode_cmsg(payload, sk):
    if len(payload) < 5:
        return payload
    msg = [payload[1], payload[3]]
    dec = bytearray(len(payload) - 4)
    for p in range(4, len(payload)):
        i = p + 4
        table_b = TABLE[i % 7]
        sk_b = sk[i % 4]
        msg_b = msg[i % 2]
        intermediate = (payload[p] ^ sk_b ^ table_b) & 0xFF
        dec[p - 4] = (intermediate - msg_b * 17) & 0xFF
    return bytes(dec)


def main():
    pcap = r"D:\CascadeProjects\codex_lab\gather_fresh.pcap"
    print(f"Reading: {pcap}")

    streams = read_pcap_game_stream(pcap)
    for d, raw in streams.items():
        print(f"  {d}: {len(raw)} bytes")

    c2s_pkts = parse_game_packets(streams.get('C2S', b''))
    s2c_pkts = parse_game_packets(streams.get('S2C', b''))

    print(f"\nC2S packets: {len(c2s_pkts)}")
    print(f"S2C packets: {len(s2c_pkts)}")

    # 1. Extract server key from 0x0038
    server_key = None
    for op, pl in s2c_pkts:
        if op == 0x0038 and len(pl) > 100:
            entry_count = struct.unpack('<H', pl[0:2])[0]
            for idx in range(entry_count):
                off = 2 + idx * 12
                if off + 12 > len(pl):
                    break
                field_id = struct.unpack('<I', pl[off:off+4])[0]
                value = struct.unpack('<I', pl[off+4:off+8])[0]
                if field_id == 0x4F:
                    server_key = value
                    break
            break

    if not server_key:
        print("ERROR: Server key not found!")
        return

    print(f"\nSERVER KEY: 0x{server_key:08x}")
    sk = [server_key & 0xFF, (server_key >> 8) & 0xFF,
          (server_key >> 16) & 0xFF, (server_key >> 24) & 0xFF]

    # 2. Show ALL C2S packets
    print(f"\n{'='*70}")
    print(f"ALL C2S PACKETS")
    print(f"{'='*70}")
    for i, (op, pl) in enumerate(c2s_pkts):
        ann = ""
        if op == 0x001F: ann = " LOGIN"
        elif op == 0x0021: ann = " WORLD_ENTRY"
        elif op == 0x0042: ann = " HB"
        elif op == 0x0CE8: ann = " <<< GATHER >>>"
        elif op == 0x0CEB: ann = " ENABLE_VIEW"
        elif op == 0x1B8B: ann = " SESSION"
        elif op == 0x099D: ann = f" TROOP={struct.unpack('<I',pl[0:4])[0] if len(pl)>=4 else '?'}"
        elif op == 0x006E:
            if len(pl) >= 4:
                tx = struct.unpack('<H', pl[0:2])[0]
                ty = struct.unpack('<H', pl[2:4])[0]
                ann = f" TILE=({tx},{ty})"
        elif op == 0x033E: ann = " SEARCH"
        elif op == 0x0323: ann = " PRE_GATHER_CMD"
        elif op == 0x0834: ann = " FORMATION"
        elif op == 0x0840: ann = " INIT"
        elif op == 0x0245: ann = " MARCH_SCR"

        prefix = pl[:30].hex() if pl else ""
        print(f"  [{i:2d}] 0x{op:04X} ({len(pl):3d}B) {prefix}{ann}")

    # 3. Decrypt 0x0CE8
    print(f"\n{'='*70}")
    print(f"DECRYPT 0x0CE8 GATHER")
    print(f"{'='*70}")
    for op, pl in c2s_pkts:
        if op == 0x0CE8:
            print(f"Encrypted ({len(pl)}B): {pl.hex()}")
            plain = decode_cmsg(pl, sk)
            print(f"Plaintext ({len(plain)}B): {plain.hex()}")

            if len(plain) >= 37:
                print(f"\nParsed:")
                print(f"  [0]     march_slot = {plain[0]}")
                print(f"  [1:4]   nonce = {plain[1:4].hex()}")
                mt = struct.unpack('<H', plain[4:6])[0]
                print(f"  [4:6]   march_type = 0x{mt:04x}")
                print(f"  [6:9]   = {plain[6:9].hex()}")
                tx = struct.unpack('<H', plain[9:11])[0]
                ty = struct.unpack('<H', plain[11:13])[0]
                print(f"  [9:11]  tile_x = {tx}")
                print(f"  [11:13] tile_y = {ty}")
                print(f"  [13]    action = {plain[13]}")
                print(f"  [14]    hero_id = {plain[14]} (0x{plain[14]:02x})")
                print(f"  [15:18] = {plain[15:18].hex()}")
                print(f"  [18]    kingdom = {plain[18]} (0x{plain[18]:02x})")
                print(f"  [19:22] = {plain[19:22].hex()}")
                print(f"  [22]    const = {plain[22]} (0x{plain[22]:02x})")
                print(f"  [23:33] = {plain[23:33].hex()}")
                igg = struct.unpack('<I', plain[33:37])[0]
                print(f"  [33:37] IGG_ID = {igg}")
                if len(plain) > 37:
                    print(f"  [37:]   rest = {plain[37:].hex()}")

    # 4. Decrypt 0x0CEB
    print(f"\n{'='*70}")
    print(f"DECRYPT 0x0CEB ENABLE_VIEW")
    print(f"{'='*70}")
    for op, pl in c2s_pkts:
        if op == 0x0CEB:
            plain = decode_cmsg(pl, sk)
            print(f"Plaintext ({len(plain)}B): {plain.hex()}")
            if len(plain) >= 5:
                vt = plain[0]
                igg = struct.unpack('<I', plain[1:5])[0]
                print(f"  view_type={vt}, IGG_ID={igg}, rest={plain[5:].hex()}")

    # 5. Show 0x1B8B
    print(f"\n{'='*70}")
    print(f"0x1B8B SESSION")
    print(f"{'='*70}")
    for op, pl in c2s_pkts:
        if op == 0x1B8B:
            print(f"Payload ({len(pl)}B): {pl.hex()}")
            # Try CMsgCodec decode
            dec = decode_cmsg(pl, sk)
            print(f"CMsgCodec decoded ({len(dec)}B): {dec.hex()}")

    # 6. Show 0x0323
    print(f"\n{'='*70}")
    print(f"0x0323 PRE-GATHER")
    print(f"{'='*70}")
    for op, pl in c2s_pkts:
        if op == 0x0323:
            print(f"Payload ({len(pl)}B): {pl.hex()}")
            print(f"Bytes: {list(pl)}")

    # 7. Show 0x0022
    print(f"\n{'='*70}")
    print(f"0x0022 POST-LOGIN")
    print(f"{'='*70}")
    for op, pl in c2s_pkts:
        if op == 0x0022:
            print(f"Payload ({len(pl)}B): {pl.hex()}")
            if pl[0] == 0x20:
                key = pl[1:33].decode('ascii', errors='replace')
                print(f"  access_key = {key}")
                print(f"  trailer = {pl[33:].hex()}")

    # 8. Show S2C gather response chain
    print(f"\n{'='*70}")
    print(f"S2C GATHER RESPONSE CHAIN")
    print(f"{'='*70}")
    for op, pl in s2c_pkts:
        if op in (0x00B8, 0x0071, 0x076C, 0x007C, 0x0033, 0x0037, 0x00B9):
            print(f"  0x{op:04X} ({len(pl)}B): {pl[:50].hex()}")

    # 9. Show 0x1B8A
    print(f"\n{'='*70}")
    print(f"0x1B8A SESSION RESPONSE")
    print(f"{'='*70}")
    for op, pl in s2c_pkts:
        if op == 0x1B8A:
            print(f"Payload ({len(pl)}B): {pl.hex()}")


if __name__ == '__main__':
    main()

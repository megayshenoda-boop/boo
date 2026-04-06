"""
Compare FULL C2S stream from successful PCAP vs what our bot builders produce.
Goal: find ANY difference in packets BEFORE 0x1B8B that could cause server rejection.
"""
import sys, struct
from pathlib import Path

sys.path.insert(0, r'D:\CascadeProjects\claude')
from config import IGG_ID, GAME_ID_HEX


def read_pcap_raw_streams(filepath):
    """Read raw IP packets, return C2S and S2C as lists of (timestamp, payload)."""
    with open(filepath, 'rb') as f:
        magic = struct.unpack('<I', f.read(4))[0]
        endian = '<' if magic == 0xa1b2c3d4 else '>'
        f.read(20)  # rest of global header

        c2s_raw = bytearray()
        s2c_raw = bytearray()

        while True:
            hdr = f.read(16)
            if len(hdr) < 16: break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
            data = f.read(incl_len)
            if len(data) < incl_len: break
            if len(data) < 20: continue

            ihl = (data[0] & 0x0F) * 4
            if data[9] != 6: continue  # TCP only
            tcp = data[ihl:]
            if len(tcp) < 20: continue

            sp = struct.unpack('>H', tcp[0:2])[0]
            dp = struct.unpack('>H', tcp[2:4])[0]
            toff = ((tcp[12] >> 4) & 0xF) * 4
            pl = tcp[toff:]
            if not pl: continue

            gp = set(range(5990, 5999)) | set(range(7001, 7011))
            if dp in gp:
                c2s_raw.extend(pl)
            elif sp in gp:
                s2c_raw.extend(pl)

    return bytes(c2s_raw), bytes(s2c_raw)


def parse_all_packets(raw):
    """Parse raw stream into list of (opcode, full_raw_packet)."""
    packets = []
    pos = 0
    while pos + 4 <= len(raw):
        pkt_len = struct.unpack('<H', raw[pos:pos+2])[0]
        opcode = struct.unpack('<H', raw[pos+2:pos+4])[0]
        if pkt_len < 4 or pkt_len > 65535 or pos + pkt_len > len(raw):
            break
        packets.append((opcode, bytes(raw[pos:pos+pkt_len])))
        pos += pkt_len
    return packets


def extract_server_key(s2c_raw):
    """Extract server key from 0x0038."""
    pkts = parse_all_packets(s2c_raw)
    for op, raw in pkts:
        if op != 0x0038: continue
        pl = raw[4:]
        if len(pl) < 14: continue
        ec = struct.unpack('<H', pl[0:2])[0]
        for idx in range(ec):
            off = 2 + idx * 12
            if off + 12 > len(pl): break
            fid = struct.unpack('<I', pl[off:off+4])[0]
            val = struct.unpack('<I', pl[off+4:off+8])[0]
            if fid == 0x4F:
                return val
    return None


def main():
    # Use the fresh successful PCAP
    pcap_path = Path(r'D:\CascadeProjects\PCAPdroid_27_Mar_09_17_04.pcap')
    if not pcap_path.exists():
        print(f"PCAP not found: {pcap_path}")
        return

    c2s_raw, s2c_raw = read_pcap_raw_streams(pcap_path)
    print(f"C2S: {len(c2s_raw)} bytes, S2C: {len(s2c_raw)} bytes")

    c2s_pkts = parse_all_packets(c2s_raw)
    s2c_pkts = parse_all_packets(s2c_raw)
    sk = extract_server_key(s2c_raw)
    print(f"Server key: 0x{sk:08X}" if sk else "Server key: NOT FOUND")
    print(f"C2S packets: {len(c2s_pkts)}, S2C packets: {len(s2c_pkts)}")

    print("\n" + "=" * 90)
    print("ALL C2S PACKETS (client -> server)")
    print("=" * 90)

    for i, (op, raw) in enumerate(c2s_pkts):
        pkt_len = len(raw)
        payload = raw[4:]

        print(f"\n[{i:3d}] 0x{op:04X}  len={pkt_len:5d}B")

        # Show full hex for small packets, first 80 bytes for large
        show_bytes = raw if pkt_len <= 100 else raw[:100]
        hex_str = show_bytes.hex()
        # Format in groups of 2 (bytes)
        formatted = ' '.join(hex_str[j:j+2] for j in range(0, len(hex_str), 2))
        print(f"       {formatted}")
        if pkt_len > 100:
            print(f"       ... ({pkt_len - 100} more bytes)")

        # Decode known packets
        if op == 0x000B:  # Gateway auth
            print(f"       GATEWAY_AUTH:")
            if len(payload) >= 75:
                ver = struct.unpack('<I', payload[0:4])[0]
                igg = struct.unpack('<I', payload[8:12])[0]
                tlen = struct.unpack('<H', payload[16:18])[0]
                token = payload[18:18+tlen]
                plat = struct.unpack('<I', payload[54:58])[0]
                wid = struct.unpack('<I', payload[62:66])[0]
                gid = struct.unpack('<I', payload[66:70])[0]
                print(f"       ver={ver} igg_id={igg} token_len={tlen} platform={plat} world_id={wid} game_id=0x{gid:08X}")
                print(f"       token: {token.hex()}")

        elif op == 0x001F:  # Game login
            print(f"       GAME_LOGIN:")
            if len(payload) >= 60:
                ver = struct.unpack('<I', payload[0:4])[0]
                pad1 = struct.unpack('<I', payload[4:8])[0]
                igg = struct.unpack('<I', payload[8:12])[0]
                pad2 = struct.unpack('<I', payload[12:16])[0]
                tlen = struct.unpack('<H', payload[16:18])[0]
                token = payload[18:18+tlen]
                marker = payload[50]
                gid = struct.unpack('<I', payload[51:55])[0]
                pad3 = struct.unpack('<I', payload[55:59])[0]
                tail = payload[59]
                print(f"       ver={ver} pad1={pad1} igg_id={igg} pad2={pad2}")
                print(f"       token_len={tlen} token: {token.hex()}")
                print(f"       marker=0x{marker:02X} game_id=0x{gid:08X} pad3={pad3} tail=0x{tail:02X}")

                # Compare with our builder
                our_marker = 0x0E
                our_gid = GAME_ID_HEX
                our_tail = 0x00
                if marker != our_marker:
                    print(f"       *** MISMATCH: marker 0x{marker:02X} vs our 0x{our_marker:02X}")
                if gid != our_gid:
                    print(f"       *** MISMATCH: game_id 0x{gid:08X} vs our 0x{our_gid:08X}")
                if tail != our_tail:
                    print(f"       *** MISMATCH: tail 0x{tail:02X} vs our 0x{our_tail:02X}")
                if pad1 != 0:
                    print(f"       *** MISMATCH: pad1={pad1} vs our 0")
                if pad2 != 0:
                    print(f"       *** MISMATCH: pad2={pad2} vs our 0")
                if pad3 != 0:
                    print(f"       *** MISMATCH: pad3={pad3} vs our 0")

        elif op == 0x0021:  # World entry
            print(f"       WORLD_ENTRY:")
            if len(payload) >= 17:
                igg = struct.unpack('<I', payload[0:4])[0]
                pad = struct.unpack('<I', payload[4:8])[0]
                marker = payload[8]
                gid = struct.unpack('<I', payload[9:13])[0]
                trailer = payload[13:17]
                print(f"       igg_id={igg} pad={pad} marker=0x{marker:02X} game_id=0x{gid:08X}")
                print(f"       trailer: {trailer.hex()}")

                # Compare with our builder
                our_trailer = bytes([0xb0, 0x02, 0x5c, 0x00])
                if trailer != our_trailer:
                    print(f"       *** MISMATCH: trailer {trailer.hex()} vs our {our_trailer.hex()}")
                if pad != 0:
                    print(f"       *** MISMATCH: pad={pad} vs our 0")

        elif op == 0x0042:  # Heartbeat
            if len(payload) >= 8:
                ms = struct.unpack('<I', payload[0:4])[0]
                v2 = struct.unpack('<I', payload[4:8])[0]
                print(f"       HEARTBEAT: ms={ms} v2={v2}")

        elif op == 0x1B8B:
            print(f"       0x1B8B SESSION PACKET:")
            print(f"       Full hex: {raw.hex()}")
            if len(raw) >= 26:
                extra = raw[4:6]
                ck = raw[6]
                ml = raw[7]
                v = raw[8]
                mh = raw[9]
                enc = raw[10:]
                print(f"       extra={extra.hex()} ck=0x{ck:02X} ml=0x{ml:02X} v=0x{v:02X} mh=0x{mh:02X}")
                print(f"       enc: {enc.hex()}")

        if op == 0x1B8B:
            print("\n       --- Everything above is BEFORE 0x1B8B ---")
            # Also show what comes after
            remaining = c2s_pkts[i+1:i+6]
            if remaining:
                print(f"\n       Next {len(remaining)} C2S packets after 0x1B8B:")
                for j, (op2, raw2) in enumerate(remaining):
                    print(f"         [{i+1+j}] 0x{op2:04X} ({len(raw2)}B)")

    # Also check: are there C2S packets during the init flood?
    print("\n\n" + "=" * 90)
    print("CHECKING: C2S packets interleaved during init flood")
    print("(Looking for packets between 0x0021 and 0x0840)")
    print("=" * 90)

    # Find positions
    saw_0021 = False
    saw_0840 = False
    between = []
    for i, (op, raw) in enumerate(c2s_pkts):
        if op == 0x0021:
            saw_0021 = True
            continue
        if op == 0x0840:
            saw_0840 = True
            break
        if saw_0021 and not saw_0840:
            between.append((i, op, raw))

    if between:
        print(f"\nFOUND {len(between)} C2S packets between 0x0021 and 0x0840:")
        for idx, op, raw in between:
            print(f"  [{idx}] 0x{op:04X} ({len(raw)}B): {raw[:40].hex()}")
    else:
        print("\nNo C2S packets between 0x0021 and 0x0840 (our bot does the same)")

    # Check ALL C2S packets between world entry and 0x1B8B
    print("\n" + "=" * 90)
    print("FULL C2S SEQUENCE: 0x0021 -> 0x1B8B")
    print("=" * 90)

    in_range = False
    for i, (op, raw) in enumerate(c2s_pkts):
        if op == 0x0021:
            in_range = True
            print(f"  [{i}] 0x0021 WORLD_ENTRY")
            continue
        if op == 0x1B8B:
            print(f"  [{i}] 0x1B8B SESSION_PKT")
            break
        if in_range:
            payload = raw[4:]
            print(f"  [{i}] 0x{op:04X} ({len(raw)}B) payload: {payload.hex() if len(payload) <= 50 else payload[:50].hex() + '...'}")

    # Now check: what about the 0x0834 payload?
    print("\n" + "=" * 90)
    print("SPECIFIC PAYLOAD CHECKS")
    print("=" * 90)

    for i, (op, raw) in enumerate(c2s_pkts):
        if op == 0x0834:
            payload = raw[4:]
            print(f"\n0x0834 payload ({len(payload)}B): {payload.hex()}")
            our_formation = bytes.fromhex("0900ba0b00000b040000d8070000e3070000f103000000040000f8030000d907000001040000")
            if payload == our_formation:
                print("  MATCHES our FORMATION_DATA")
            else:
                print(f"  *** MISMATCH with our formation data!")
                print(f"  Our: {our_formation.hex()}")

        if op == 0x1357:
            payload = raw[4:]
            print(f"\n0x1357 payload ({len(payload)}B): {payload.hex()}")
            our_payload = bytes.fromhex("02000000")
            if payload == our_payload:
                print("  MATCHES our payload")
            else:
                print(f"  *** MISMATCH! Our: {our_payload.hex()}")

        if op == 0x170D:
            payload = raw[4:]
            print(f"\n0x170D payload ({len(payload)}B): {payload.hex()}")
            our_payload = bytes.fromhex("02000000")
            if payload == our_payload:
                print("  MATCHES our payload")
            else:
                print(f"  *** MISMATCH! Our: {our_payload.hex()}")


if __name__ == '__main__':
    main()

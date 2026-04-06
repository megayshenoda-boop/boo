"""
Decrypt the 0x0CE8 gather payload from fresh PCAP.
Also decrypt 0x0CEB and analyze 0x1B8B, 0x0323.
"""
import struct

# From PCAP 0x0038 packet (834B payload)
raw_0038 = bytes.fromhex(
    "450002000000af26ef5b000000000300000046330000000000000500000083320000000000000c00"
    "0000b401000000000000100000001f00000000000000110000001e00000000000000120000001f00"
    "000000000000130000001f000000000000001400000020000000000000001500000020000000000000"
    "0016000000200000000000000017000000200000000000000019000000040000000000000023000000"
    "0b000000000000002400000007000000000000002500000009000000000000002600000009000000"
    "000000002700000009000000000000002800000009000000000000002b00000009000000000000002c"
    "0000000900000000000000310000000800000000000000320000000700000000000000330000000900"
    "00000000000034000000080000000000000035000000b7000000000000003600000026000000000000"
    "003700000006000000000000003b00000002000000000000003e0000000a000000000000003f000000"
    "0a000000000000004000000003000000000000004500000004000000000000004600000009000000"
    "00000000470000000a000000000000004800000009000000000000004900000003000000000000004a"
    "0000001c000000000000004b000000040000000000000000000000000000000000000000000000"
    "0000000000000000000000000000000000000000000000004f000000880bd1d7000000005100000025"
    "0000000000000052000000060000000000000053000000380c00000000000054000000380c000000"
    "00000055000000030000000000000056000000060000000000000057000000860000000000000058"
    "0000000700000000000000590000000a000000000000005a000000060000000000000061000000a30200"
    "00000000006200000003000000000000006e00000003000000000000007600000003000000000000"
    "0077000000030000000000000078000000030000000000000079000000030000000000000082000000"
    "22000000000000008b0000001000000000000000"
)

# Extract server key
entry_count = struct.unpack('<H', raw_0038[0:2])[0]
print(f"0x0038 entries: {entry_count}")
server_key = None
for idx in range(entry_count):
    off = 2 + idx * 12
    if off + 12 > len(raw_0038):
        break
    field_id = struct.unpack('<I', raw_0038[off:off+4])[0]
    value = struct.unpack('<I', raw_0038[off+4:off+8])[0]
    if field_id == 0x4F:
        server_key = value
        print(f"SERVER KEY: field=0x{field_id:02X}, value=0x{server_key:08x}")
        break

if not server_key:
    print("SERVER KEY NOT FOUND!")
    exit(1)

# CMsgCodec decrypt
TABLE = [0x58, 0xef, 0xd7, 0x14, 0xa2, 0x3b, 0x9c]

sk = [server_key & 0xFF, (server_key >> 8) & 0xFF,
      (server_key >> 16) & 0xFF, (server_key >> 24) & 0xFF]
print(f"SK bytes: {[f'0x{b:02x}' for b in sk]}")

def decode_payload(payload):
    """Decode CMsgCodec encrypted payload (after 4B game header removed)."""
    if len(payload) < 5:
        return payload
    msg = [payload[1], payload[3]]  # msg_lo, msg_hi
    dec = bytearray(len(payload) - 4)
    for p in range(4, len(payload)):
        i = p + 4  # offset in full packet
        table_b = TABLE[i % 7]
        sk_b = sk[i % 4]
        msg_b = msg[i % 2]
        intermediate = (payload[p] ^ sk_b ^ table_b) & 0xFF
        dec[p - 4] = (intermediate - msg_b * 17) & 0xFF
    return bytes(dec)


# Decrypt 0x0CE8 GATHER
print("\n" + "="*60)
print("0x0CE8 GATHER DECRYPT")
print("="*60)
gather_payload = bytes.fromhex("c9ae19bc6a0e04efe672ebbd53ce0fc407585f8590a342cedcee7846263a2f0a6bd6a7f0bf88f52e6d15116918595c8590a3")
print(f"Encrypted ({len(gather_payload)}B): {gather_payload.hex()}")
msg_lo = gather_payload[1]
msg_hi = gather_payload[3]
msg_value = msg_lo | (msg_hi << 8)
print(f"msg_lo=0x{msg_lo:02x}, msg_hi=0x{msg_hi:02x}, msg_value=0x{msg_value:04x}")

plaintext = decode_payload(gather_payload)
print(f"Plaintext ({len(plaintext)}B): {plaintext.hex()}")

# Parse plaintext
if len(plaintext) >= 46:
    print(f"\nParsed:")
    print(f"  [0]     march_slot = {plaintext[0]}")
    print(f"  [1:4]   nonce = {plaintext[1:4].hex()}")
    march_type = struct.unpack('<H', plaintext[4:6])[0]
    print(f"  [4:6]   march_type = 0x{march_type:04x}")
    print(f"  [6:9]   = {plaintext[6:9].hex()}")
    tile_x = struct.unpack('<H', plaintext[9:11])[0]
    tile_y = struct.unpack('<H', plaintext[11:13])[0]
    print(f"  [9:11]  tile_x = {tile_x}")
    print(f"  [11:13] tile_y = {tile_y}")
    print(f"  [13]    flag = {plaintext[13]}")
    print(f"  [14]    hero_id = {plaintext[14]}")
    print(f"  [15:18] = {plaintext[15:18].hex()}")
    print(f"  [18]    kingdom = {plaintext[18]}")
    print(f"  [19:22] = {plaintext[19:22].hex()}")
    print(f"  [22]    constant = {plaintext[22]}")
    print(f"  [23:33] = {plaintext[23:33].hex()}")
    igg_id = struct.unpack('<I', plaintext[33:37])[0]
    print(f"  [33:37] IGG_ID = {igg_id}")
    print(f"  [37:46] = {plaintext[37:46].hex()}")


# Decrypt 0x0CEB ENABLE_VIEW
print("\n" + "="*60)
print("0x0CEB ENABLE_VIEW DECRYPT")
print("="*60)
ev_payload = bytes.fromhex("eae95ee99fcc5260aa981cb8a413")
print(f"Encrypted ({len(ev_payload)}B): {ev_payload.hex()}")
ev_plain = decode_payload(ev_payload)
print(f"Plaintext ({len(ev_plain)}B): {ev_plain.hex()}")
if len(ev_plain) >= 10:
    view_type = ev_plain[0]
    ev_igg = struct.unpack('<I', ev_plain[1:5])[0]
    print(f"  view_type = {view_type}")
    print(f"  IGG_ID = {ev_igg}")
    print(f"  rest = {ev_plain[5:].hex()}")


# Analyze 0x1B8B SESSION
print("\n" + "="*60)
print("0x1B8B SESSION ANALYSIS")
print("="*60)
session_payload = bytes.fromhex("f96a1cda6d704efedc731fb1a719e67aef4aab9667b0")
print(f"Payload ({len(session_payload)}B): {session_payload.hex()}")
print(f"  As bytes: {list(session_payload)}")

# Try decoding with CMsgCodec (maybe it's encrypted?)
session_dec = decode_payload(session_payload)
print(f"\n  Decoded with CMsgCodec: {session_dec.hex()}")
print(f"  Decoded bytes: {list(session_dec)}")


# Analyze 0x0323
print("\n" + "="*60)
print("0x0323 PRE-GATHER COMMAND")
print("="*60)
cmd_0323 = bytes.fromhex("000100ff000000")
print(f"Payload ({len(cmd_0323)}B): {cmd_0323.hex()}")
print(f"  As bytes: {list(cmd_0323)}")
print(f"  [0] = {cmd_0323[0]} (action?)")
print(f"  [1] = {cmd_0323[1]} (count?)")
print(f"  [2] = {cmd_0323[2]} (pad)")
print(f"  [3] = 0x{cmd_0323[3]:02x} = {cmd_0323[3]} (hero_id = 255?)")
print(f"  [4:7] = {cmd_0323[4:7].hex()}")


# Analyze 0x0022 (appears in PCAP)
print("\n" + "="*60)
print("0x0022 PACKET (appears after game data)")
print("="*60)
pkt_0022 = bytes.fromhex("2000386233393232306136626562376335663134656231386233363462373534343901")
print(f"Payload ({len(pkt_0022)}B): {pkt_0022.hex()}")
str_len = pkt_0022[0]
if str_len == 32:
    key_str = pkt_0022[1:33].decode('ascii', errors='replace')
    print(f"  str_len = {str_len}")
    print(f"  access_key = {key_str}")
    print(f"  trailer = {pkt_0022[33:].hex()}")


# Show 0x0071 MARCH_STATE for reference
print("\n" + "="*60)
print("0x0071 MARCH_STATE (SUCCESS RESPONSE)")
print("="*60)
march_state = bytes.fromhex("ff870900b60000000100ed0273220000000001b003000043023e032b025503c900000000000e0031")
print(f"Payload ({len(march_state)}B):")
# This is partial - first 40 bytes
print(f"  [0:4] = 0x{struct.unpack('<I', march_state[0:4])[0]:08x} (march_id?)")
print(f"  [4] = {march_state[4]} (kingdom={march_state[4]})")
print(f"  [5:8] = {march_state[5:8].hex()}")
print(f"  [8] = {march_state[8]} (status?)")
igg_at_9 = struct.unpack('<I', march_state[9:13])[0]
print(f"  [9:13] = {igg_at_9} (IGG_ID={igg_at_9})")
print(f"  rest: {march_state[13:].hex()}")


# Show troop IDs
print("\n" + "="*60)
print("TROOP SELECTION")
print("="*60)
troop_ids = [403, 405, 407, 408, 409, 410, 411]
print(f"Troops selected: {troop_ids} (count={len(troop_ids)})")


# Show 0x007C COLLECT_STATE
print("\n" + "="*60)
print("0x007C COLLECT_STATE (TROOPS ARRIVED)")
print("="*60)
collect = bytes.fromhex("380c0000380c00002b025503010001000000302a0000")
print(f"Payload ({len(collect)}B): {collect.hex()}")
v1 = struct.unpack('<I', collect[0:4])[0]
v2 = struct.unpack('<I', collect[4:8])[0]
tx = struct.unpack('<H', collect[8:10])[0]
ty = struct.unpack('<H', collect[10:12])[0]
print(f"  [0:4] = {v1} (resource amount?)")
print(f"  [4:8] = {v2}")
print(f"  [8:10] = {tx} (tile_x)")
print(f"  [10:12] = {ty} (tile_y)")
print(f"  rest: {collect[12:].hex()}")

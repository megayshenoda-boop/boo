"""
CMsgCodec Encoder/Decoder - CRACKED!

Algorithm: enc[i] = ((plain[i] + msg_byte*17) ^ sk_byte ^ table_byte) & 0xFF
  - i = byte offset from start of full packet (encrypted portion starts at 8)
  - table_byte = TABLE[i % 7]
  - sk_byte = server_key[i % 4]  
  - msg_byte = msg_value_bytes[i % 2]
  - msg_value stored in packet metadata bytes 4-7

Packet format:
  [2B LE] total_length (includes these 2 bytes)
  [2B LE] opcode
  [payload]:
    [0] checksum (low byte of sum of encrypted bytes)
    [1] msg_value & 0xFF
    [2] (msg_value & 0xFF) ^ 0xB7
    [3] (msg_value >> 8) & 0xFF
    [4:] encrypted action data
"""
import struct, random

TABLE = [0x58, 0xef, 0xd7, 0x14, 0xa2, 0x3b, 0x9c]

# Server key field ID in 0x0038 packet
SERVER_KEY_FIELD_ID = 0x4F  # field 79 in the key-value structure


class CMsgCodec:
    def __init__(self, server_key_bytes):
        """server_key_bytes: list of 4 bytes [sk0, sk1, sk2, sk3]"""
        self.sk = list(server_key_bytes)
    
    @classmethod
    def from_u32(cls, key_u32):
        """Create from a u32 server key."""
        return cls([
            key_u32 & 0xFF,
            (key_u32 >> 8) & 0xFF,
            (key_u32 >> 16) & 0xFF,
            (key_u32 >> 24) & 0xFF,
        ])
    
    def decode(self, payload):
        """Decode a packet payload (after removing 2B length + 2B opcode).
        Returns the decrypted action data (without 4-byte CMsgCodec metadata)."""
        if len(payload) < 5:
            return payload
        msg = [payload[1], payload[3]]
        dec = bytearray(len(payload) - 4)
        for p in range(4, len(payload)):
            i = p + 4  # full packet offset
            table_b = TABLE[i % 7]
            sk_b = self.sk[i % 4]
            msg_b = msg[i % 2]
            intermediate = (payload[p] ^ sk_b ^ table_b) & 0xFF
            dec[p - 4] = (intermediate - msg_b * 17) & 0xFF
        return bytes(dec)
    
    def encode(self, opcode, action_data, msg_value=None):
        """Encode action data into a full packet (including 2B length + 2B opcode).
        Returns the complete encrypted packet bytes ready to send."""
        if msg_value is None:
            msg_value = random.randint(0, 0xFFFF)
        
        msg_lo = msg_value & 0xFF
        msg_hi = (msg_value >> 8) & 0xFF
        msg = [msg_lo, msg_hi]
        
        payload_len = 4 + len(action_data)
        total_len = 4 + payload_len  # 2B len + 2B opcode + payload
        
        pkt = bytearray(total_len)
        struct.pack_into('<H', pkt, 0, total_len)
        struct.pack_into('<H', pkt, 2, opcode)
        
        # Copy plaintext action data to positions 8+ in full packet
        for j, b in enumerate(action_data):
            pkt[8 + j] = b
        
        # Encrypt bytes 8+
        checksum = 0
        for i in range(8, total_len):
            p = i - 4  # payload offset
            table_b = TABLE[i % 7]
            sk_b = self.sk[i % 4]
            msg_b = msg[i % 2]
            intermediate = (pkt[i] + msg_b * 17) & 0xFF
            enc_byte = (intermediate ^ sk_b ^ table_b) & 0xFF
            pkt[i] = enc_byte
            checksum = (checksum + enc_byte) & 0xFFFFFFFF
        
        # Write CMsgCodec metadata at packet bytes 4-7
        pkt[4] = checksum & 0xFF
        pkt[5] = msg_lo
        pkt[6] = msg_lo ^ 0xB7
        pkt[7] = msg_hi
        
        return bytes(pkt)
    
    def decode_packet(self, raw_packet):
        """Decode a full raw packet (including 2B length + 2B opcode).
        Returns (opcode, action_data)."""
        if len(raw_packet) < 8:
            return None, None
        total_len = struct.unpack('<H', raw_packet[0:2])[0]
        opcode = struct.unpack('<H', raw_packet[2:4])[0]
        payload = raw_packet[4:total_len]
        action_data = self.decode(payload)
        return opcode, action_data


# ====== SERVER KEY EXTRACTION ======

def extract_server_key_from_0x0038(payload):
    """Extract server_key u32 from 0x0038 packet payload.
    Structure: [2B LE entry_count] then [entry_count * 12B entries]
    Each entry: [4B LE field_id][8B LE value]
    Field 0x4F (79) contains the server key.
    Returns the key as u32, or None if not found."""
    if len(payload) < 14:
        return None
    entry_count = struct.unpack('<H', payload[0:2])[0]
    for idx in range(entry_count):
        off = 2 + idx * 12
        if off + 12 > len(payload):
            break
        field_id = struct.unpack('<I', payload[off:off+4])[0]
        if field_id == SERVER_KEY_FIELD_ID:
            return struct.unpack('<I', payload[off+4:off+8])[0]
    return None


def extract_server_key_from_stream(s2c_packets):
    """Search all server->client packets for the server key.
    s2c_packets: list of (opcode, payload) tuples.
    Returns server_key as u32, or None."""
    for opcode, payload in s2c_packets:
        if opcode == 0x0038:
            key = extract_server_key_from_0x0038(payload)
            if key is not None:
                return key
    return None


# ====== ACTION DATA STRUCTURES ======
# Decoded from capture1.pcap action packets
#
# 0x0CE8 GATHER (62 bytes):
#   [0]     u8  march_slot (1 or 2)
#   [1:4]   3B  variable (nonce/sub-ID per march)
#   [4:6]   u16 march_type_id (0x1748 = 5960 observed)
#   [6:9]   3B  zeros
#   [9]     u8  target_info_1 (varies: 0x77, 0x71)
#   [10]    u8  0x04 (constant)
#   [11]    u8  target_info_2 (varies: 0x8c, 0x89)
#   [12]    u8  0x02 (constant)
#   [13]    u8  0x05 (constant)
#   [14:18] u32 troop_type_1 (0xc9 = 201)
#   [18:22] u32 troop_type_2 (0xd4 = 212)
#   [22:26] u32 troop_type_3 (0xce = 206)
#   [26:30] u32 troop_type_4 (0xd8 = 216)
#   [30:34] u32 troop_type_5 (0xe0 = 224)
#   [34:38] u32 troop_type_6 (0xd3 = 211)
#   [38:42] u32 troop_count (2 or 4)
#   [42:46] 4B  zeros
#   [46:49] 3B  flag area (0x00,0x01,0x00 or 0x00,0x00,0x00)
#   [49:53] u32 IGG_ID (0x7c1eaac9)
#   [53:62] 9B  zeros
#
# 0x0CEB TRAIN (10 bytes):
#   [0]     u8  type (0x01)
#   [1:5]   u32 IGG_ID
#   [5:9]   4B  zeros
#   [9]     u8  flag (0x01)
#
# 0x0CED BUILD (19 bytes):
#   [0:4]   u32 building_type (0x01)
#   [4:8]   u32 building_id (0x01e0 = 480)
#   [8]     u8  zero
#   [9:13]  u32 IGG_ID
#   [13:19] 6B  zeros
#
# 0x0CEF UNKNOWN (22 bytes):
#   [0]     u8  sub_type (2 or 8)
#   [1:3]   u16 constant (0x0037 = 55)
#   [3]     u8  constant (0x34 = 52)
#   [4:7]   3B  zeros
#   [7:11]  4B  variable
#   [11]    u8  flag (0 or 1)
#   [12:16] u32 IGG_ID
#   [16:22] 6B  zeros


def build_train_action(igg_id, train_type=0x01, flag=0x01):
    """Build 0x0CEB train action data (10 bytes)."""
    data = bytearray(10)
    data[0] = train_type
    struct.pack_into('<I', data, 1, igg_id)
    data[9] = flag
    return bytes(data)


def build_build_action(igg_id, building_type=0x01, building_id=480):
    """Build 0x0CED build action data (19 bytes)."""
    data = bytearray(19)
    struct.pack_into('<I', data, 0, building_type)
    struct.pack_into('<I', data, 4, building_id)
    struct.pack_into('<I', data, 9, igg_id)
    return bytes(data)


def build_gather_action(igg_id, march_slot=1, march_type=0x1748,
                        troop_types=None, troop_count=2):
    """Build 0x0CE8 gather action data (62 bytes).
    troop_types: list of up to 6 u32 troop type IDs."""
    if troop_types is None:
        troop_types = [201, 212, 206, 216, 224, 211]  # default from capture
    data = bytearray(62)
    data[0] = march_slot
    data[1] = random.randint(0, 255)
    data[2] = random.randint(0, 255)
    data[3] = random.randint(0, 255)
    struct.pack_into('<H', data, 4, march_type)
    data[12] = 0x02
    data[13] = 0x05
    for i, tid in enumerate(troop_types[:6]):
        struct.pack_into('<I', data, 14 + i*4, tid)
    struct.pack_into('<I', data, 38, troop_count)
    struct.pack_into('<I', data, 49, igg_id)
    return bytes(data)


# ====== SELF TEST ======
if __name__ == '__main__':
    # Test with known server key from capture1.pcap
    SK = [0x9b, 0x1d, 0x8b, 0x22]
    codec = CMsgCodec(SK)
    
    # Test roundtrip
    print("=== Roundtrip Test ===")
    test_data = bytes(range(20))
    pkt = codec.encode(0x0CE8, test_data, msg_value=0x1234)
    opcode, dec = codec.decode_packet(pkt)
    assert opcode == 0x0CE8
    assert dec == test_data
    print(f"  PASSED: encode->decode roundtrip for {len(test_data)} bytes")
    
    # Verify against captured packet
    print("\n=== Verify Against Captured Packets ===")
    captured = [
        (0x0CEF, "64ab1c342961c428fbf588c1487d726c235b1d05d4cbebca9886"),
        (0x0CEB, "b52196f8468b44160df9e2b57d70"),
    ]
    for op, hexdata in captured:
        pay = bytes.fromhex(hexdata)
        dec = codec.decode(pay)
        print(f"  0x{op:04X}: {dec.hex()}")
        
        # Re-encode and verify
        msg_val = pay[1] | (pay[3] << 8)
        re_pkt = codec.encode(op, dec, msg_value=msg_val)
        re_pay = re_pkt[4:]  # extract payload
        match = re_pay[4:] == pay[4:]
        print(f"    Re-encode match: {match}")
    
    print("\n=== Server Key Info ===")
    print(f"  Key bytes: {[f'0x{b:02x}' for b in SK]}")
    print(f"  Key u32: 0x{SK[0] | (SK[1]<<8) | (SK[2]<<16) | (SK[3]<<24):08x}")
    print(f"  TABLE: {[f'0x{b:02x}' for b in TABLE]}")

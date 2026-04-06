"""
IGG Conquerors Bot - CMsgCodec Encryption/Decryption
=====================================================
Algorithm: enc[i] = ((plain[i] + msg_byte*17) ^ sk_byte ^ table_byte) & 0xFF
Cracked from libgame.so ARM64 disassembly. Verified via PCAP roundtrip tests.
"""
import struct
import random

from protocol import CMSG_TABLE, SERVER_KEY_FIELD_ID


class CMsgCodec:
    """CMsgCodec Encoder/Decoder.

    Encrypted packet format:
        [0:2]  u16 LE  total_length
        [2:4]  u16 LE  opcode
        [4]    u8      checksum (low byte of sum of encrypted bytes)
        [5]    u8      msg_lo
        [6]    u8      msg_lo ^ 0xB7
        [7]    u8      msg_hi
        [8:]   NB      encrypted action data
    """

    def __init__(self, server_key_bytes):
        self.sk = list(server_key_bytes)

    @classmethod
    def from_u32(cls, key_u32):
        """Create codec from server key as u32 (little-endian byte order)."""
        return cls([
            key_u32 & 0xFF, (key_u32 >> 8) & 0xFF,
            (key_u32 >> 16) & 0xFF, (key_u32 >> 24) & 0xFF,
        ])

    def decode(self, payload):
        """Decode encrypted payload (bytes 4+ of packet, after the 4-byte header).
        Returns decrypted action data."""
        if len(payload) < 5:
            return payload
        msg = [payload[1], payload[3]]
        dec = bytearray(len(payload) - 4)
        for p in range(4, len(payload)):
            i = p + 4  # offset in full packet
            table_b = CMSG_TABLE[i % 7]
            sk_b = self.sk[i % 4]
            msg_b = msg[i % 2]
            intermediate = (payload[p] ^ sk_b ^ table_b) & 0xFF
            dec[p - 4] = (intermediate - msg_b * 17) & 0xFF
        return bytes(dec)

    def encode(self, opcode, action_data, msg_value=None):
        """Encode action data into a full encrypted packet ready to send.
        Returns complete packet bytes including header."""
        if msg_value is None:
            msg_value = random.randint(0, 0xFFFF)
        msg_lo = msg_value & 0xFF
        msg_hi = (msg_value >> 8) & 0xFF
        msg = [msg_lo, msg_hi]

        payload_len = 4 + len(action_data)
        total_len = 4 + payload_len
        pkt = bytearray(total_len)
        struct.pack_into('<H', pkt, 0, total_len)
        struct.pack_into('<H', pkt, 2, opcode)

        for j, b in enumerate(action_data):
            pkt[8 + j] = b

        checksum = 0
        for i in range(8, total_len):
            table_b = CMSG_TABLE[i % 7]
            sk_b = self.sk[i % 4]
            msg_b = msg[i % 2]
            intermediate = (pkt[i] + msg_b * 17) & 0xFF
            enc_byte = (intermediate ^ sk_b ^ table_b) & 0xFF
            pkt[i] = enc_byte
            checksum = (checksum + enc_byte) & 0xFFFFFFFF

        pkt[4] = checksum & 0xFF
        pkt[5] = msg_lo
        pkt[6] = msg_lo ^ 0xB7
        pkt[7] = msg_hi
        return bytes(pkt)

    def encode_offset6(self, opcode, action_data, extra=None, msg_value=None):
        """Encode with header at offset 6 (used by 0x1B8B and similar).

        Packet format:
            [0:2]  u16 LE  total_length
            [2:4]  u16 LE  opcode
            [4:6]  2 bytes extra header (caller-provided or random)
            [6]    u8      checksum (sum of encrypted bytes from offset 10)
            [7]    u8      msg_lo
            [8]    u8      msg_lo ^ 0xB7
            [9]    u8      msg_hi
            [10:]  NB      encrypted action data
        """
        if msg_value is None:
            msg_value = random.randint(0, 0xFFFF)
        msg_lo = msg_value & 0xFF
        msg_hi = (msg_value >> 8) & 0xFF
        msg = [msg_lo, msg_hi]

        if extra is None:
            extra = bytes([random.randint(0, 255), random.randint(0, 255)])

        total_len = 10 + len(action_data)
        pkt = bytearray(total_len)
        struct.pack_into('<H', pkt, 0, total_len)
        struct.pack_into('<H', pkt, 2, opcode)
        pkt[4] = extra[0]
        pkt[5] = extra[1]

        for j, b in enumerate(action_data):
            pkt[10 + j] = b

        checksum = 0
        for i in range(10, total_len):
            table_b = CMSG_TABLE[i % 7]
            sk_b = self.sk[i % 4]
            msg_b = msg[i % 2]
            intermediate = (pkt[i] + msg_b * 17) & 0xFF
            enc_byte = (intermediate ^ sk_b ^ table_b) & 0xFF
            pkt[i] = enc_byte
            checksum = (checksum + enc_byte) & 0xFFFFFFFF

        pkt[6] = checksum & 0xFF
        pkt[7] = msg_lo
        pkt[8] = msg_lo ^ 0xB7
        pkt[9] = msg_hi
        return bytes(pkt)

    def decode_packet(self, raw_packet):
        """Decode a full raw packet. Returns (opcode, decrypted_action_data)."""
        if len(raw_packet) < 8:
            return None, None
        total_len = struct.unpack('<H', raw_packet[0:2])[0]
        opcode = struct.unpack('<H', raw_packet[2:4])[0]
        payload = raw_packet[4:total_len]
        action_data = self.decode(payload)
        return opcode, action_data


def extract_server_key_from_0x0038(payload):
    """Extract server_key u32 from 0x0038 (CASTLE_DATA) packet.
    Structure: [2B LE entry_count] then [entry_count * 12B entries]
    Each entry: [4B LE field_id][4B LE value][4B reserved]
    Server key is at field_id = 0x4F (79).
    """
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


if __name__ == '__main__':
    # Self-test: encode then decode should return original data
    test_key = [0x9b, 0x1d, 0x8b, 0x22]
    codec = CMsgCodec(test_key)

    original = bytes([0x01, 0x00, 0x00, 0x00, 0x0a, 0x00, 0x00, 0x00,
                      0x00, 0x49, 0x24, 0x25, 0x7c, 0x00, 0x00, 0x00,
                      0x00, 0x00, 0x00])

    # Encode with fixed msg_value for reproducibility
    encrypted = codec.encode(0x0CED, original, msg_value=0x1234)

    # Decode
    opcode, decrypted = codec.decode_packet(encrypted)

    assert opcode == 0x0CED, f"Opcode mismatch: {opcode:#06x}"
    assert decrypted == original, f"Roundtrip failed!\n  Original:  {original.hex()}\n  Decrypted: {decrypted.hex()}"
    print("CMsgCodec self-test PASSED")
    print(f"  Key: {[f'0x{b:02x}' for b in test_key]}")
    print(f"  Original ({len(original)}B): {original.hex()}")
    print(f"  Encrypted ({len(encrypted)}B): {encrypted.hex()}")
    print(f"  Decrypted ({len(decrypted)}B): {decrypted.hex()}")

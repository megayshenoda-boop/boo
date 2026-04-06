# IGG Conquerors - Protocol Reference

## Connection Flow

```
[HTTP Login] -> access_token (4 steps via account.igg.com)
     |
[Gateway Auth] -> TCP 54.93.167.80:5997 -> redirect IP:port + session_token
     |
[Game Server] -> TCP game_ip:game_port -> game data flood (~95KB)
     |
[Extract Server Key] -> from 0x0038 packet, field 0x4F
     |
[Send Actions] -> encrypted via CMsgCodec
```

## Packet Format

### Generic Packet
```
[0:2]  u16 LE  total_length (includes these 2 bytes)
[2:4]  u16 LE  opcode
[4:]   NB      payload
```

### CMsgCodec Encrypted Packet
```
[0:2]  u16 LE  total_length
[2:4]  u16 LE  opcode
[4]    u8      checksum (low byte of sum of encrypted bytes)
[5]    u8      msg_lo
[6]    u8      msg_lo ^ 0xB7
[7]    u8      msg_hi
[8:]   NB      encrypted action data
```

## CMsgCodec Algorithm

```
Encryption: enc[i] = ((plain[i] + msg_byte * 17) ^ sk_byte ^ table_byte) & 0xFF
Decryption: plain[i] = ((enc[i] ^ sk_byte ^ table_byte) - msg_byte * 17) & 0xFF

Where:
  i          = byte offset in full packet (starts at 8)
  table_byte = TABLE[i % 7]
  sk_byte    = server_key[i % 4]
  msg_byte   = msg_value[i % 2]

TABLE = [0x58, 0xef, 0xd7, 0x14, 0xa2, 0x3b, 0x9c]
Period = LCM(2, 4, 7) = 28 bytes
```

## Server Key Extraction (0x0038)
```
[0:2]   u16 LE  entry_count
[2:]    12B * entry_count entries:
  [+0]  u32 LE  field_id
  [+4]  u32 LE  value      <- server_key when field_id == 0x4F
  [+8]  u32 LE  reserved
```

## Gateway Auth Token
```python
token = XOR(access_key_ascii[0:32], "CQ_secretCQ_secretCQ_secretCQ_se")
```

## Action Opcodes (Encrypted, ARM64 Confirmed)

| Opcode | Name | Payload | Status |
|--------|------|---------|--------|
| 0x0CED | TRAIN | 19B: [type:4B][count:4B][0:1B][igg_id:4B][0:6B] | VERIFIED |
| 0x0CEF | BUILD | 22B: [op:1B][type:1B][0:1B][slot:1B][0:7B][flag:1B][igg_id:4B][0:6B] | VERIFIED |
| 0x0CEE | RESEARCH | 12B: [tech_id:4B][category:4B][0:4B] | VERIFIED |
| 0x0CEB | ENABLE_VIEW | 10B: [type:1B][igg_id:4B][0:4B][flag:1B] | VERIFIED |
| 0x0CE8 | START_MARCH | Variable: [slot:4B][type:4B][x:4B][y:4B][n_troops:4B]... | EXPERIMENTAL |
| 0x0CE9 | CANCEL_MARCH | 8B: [march_id:8B] | UNVERIFIED |
| 0x0CF1 | MOVE_CASTLE | 16B: [x:4B][y:4B][random:1B][0:3B][item:4B] | UNVERIFIED |
| 0x0CF3 | RAID_PLAYER | Variable: [slot:4B][target:8B][n:4B]... | UNVERIFIED |

## Old-Style Opcodes (Unencrypted)

| Opcode | Name | Payload |
|--------|------|---------|
| 0x0065 | ITEM_USE | [item_id:2B][count:4B][target:4B] |
| 0x06C7 | SPEED_TRAIN | [slot:2B][item_id:4B][0:4B] |
| 0x06CB | HEAL | [slot:2B][0:2B][troop:8B] |
| 0x009F | BUILD_HELP | [slot:2B][building_id:2B] |
| 0x00C4 | SPEED_RESEARCH | [research_id:2B][item_id:4B][0:4B] |

## Heartbeat
- Opcode: 0x0042
- Interval: 15 seconds
- Payload: [ms_elapsed:4B LE][0:4B]

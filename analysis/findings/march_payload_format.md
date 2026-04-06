# CMSG_START_MARCH_NEW (0x0CE8) Payload Format

- **Function**: `packData` at `0x05212294`
- **Size**: 1252 bytes (313 instructions)
- **Opcode**: 0x0CE8

## Payload Layout

The payload is variable-length due to a troop/hero array.
Fixed portion (without array) = 46 bytes + N*4 bytes for each array entry.

| # | Offset | Size | Struct Field | Type | Description |
|---|--------|------|-------------|------|-------------|
| 0 | 0 | 2B | [0x00] | u16 | msg_id / sub_type (u16) |
| 1 | 2 | 2B | [0x02] | u16 | march_type (u16) |
| 2 | 4 | 1B | [0x04] | u8 | flag_byte_0 (u8) |
| 3 | 5 | 1B | [0x05] | u8 | flag_byte_1 (u8) |
| 4 | 6 | 1B | [0x06] | u8 | flag_byte_2 (u8) |
| 5 | 7 | 1B | [0x07] | u8 | flag_byte_3 (u8) |
| 6 | 8 | 1B | [0x08] | u8 | flag_byte_4 / hero_count? (u8) |
| 7 | 9 | 8B | [0x10] | u64 | target_coords (u64 = two u32: x,y) |
| 8 | 17 | 2B | [0x18] | u16 | kingdom_id / target_kingdom (u16) |
| 9 | 19 | 2B | [0x1A] | u16 | march_slot / queue_id (u16) |
| 10 | 21 | 1B | [computed] | u8 | array_count (u8) = len(troop_vector) |
| 11 | 22+ | 4B each | vector[0x20] | u32[] | Troop/hero array (N entries) |
| 12 | 26 | 4B | [0x38] | u32 | tile_type / resource_id (u32) |
| 13 | 30 | 1B | [0x3C] | u8 | march_flag / sub_flag (u8) |
| 14 | 31 | 8B | [0x40] | u64 | rally_timestamp / march_param (u64) |
| 15 | 39 | 1B | [0x48] | u8 | extra_flag_0 (u8) |
| 16 | 40 | 1B | [0x49] | u8 | extra_flag_1 (u8) |
| 17 | 41 | 8B | [0x50] | u64 | extra_param (u64) |
| 18 | 49 | 1B | [0x58] | u8 | extra_flag_2 (u8) |
| 19 | 50 | 4B | [0x5C] | u32 | extra_param_2 (u32) |

**Base payload**: 46 bytes (0 array entries) + N*4 per troop entry

## CMSG Struct Layout

| Offset | Type | Field |
|--------|------|-------|
| 0x00 | u16 | msg_id / sub_type |
| 0x02 | u16 | march_type |
| 0x04 | u8 | flag_0 |
| 0x05 | u8 | flag_1 |
| 0x06 | u8 | flag_2 |
| 0x07 | u8 | flag_3 |
| 0x08 | u8 | flag_4 / hero_count? |
| 0x10 | u64 | target_coords (likely two u32: x, y packed) |
| 0x18 | u16 | kingdom_id |
| 0x1A | u16 | march_slot / queue_id |
| 0x20 | ptr | vector<u32>.begin (troop/hero array) |
| 0x28 | ptr | vector<u32>.end |
| 0x30 | ptr | vector<u32>.capacity_end (unused in packData) |
| 0x38 | u32 | tile_type / resource_id |
| 0x3C | u8 | march_flag / sub_flag |
| 0x40 | u64 | rally_timestamp / march_param_1 |
| 0x48 | u8 | extra_flag_0 |
| 0x49 | u8 | extra_flag_1 |
| 0x50 | u64 | march_param_2 |
| 0x58 | u8 | extra_flag_2 |
| 0x5C | u32 | extra_param / march_param_3 |

## Control Flow

```
packData(this=x0, stream=x1):
  x19 = this, x20 = stream
  
  write_u16 this[0x00]          ; msg sub-type
  if no_error: goto main_body (0x05212418)
  
main_body:
  write_u16 this[0x02]          ; march type
  write_u8  this[0x04]          ; flag 0
  write_u8  this[0x05]          ; flag 1
  write_u8  this[0x06]          ; flag 2
  write_u8  this[0x07]          ; flag 3
  write_u8  this[0x08]          ; flag 4
  write_u64 this[0x10]          ; target x,y (packed)
  write_u16 this[0x18]          ; kingdom
  write_u16 this[0x1A]          ; march slot
  
  ; Load vector from this+0x20
  begin, end = ldp [this, #0x20]
  count = (end - begin) / 4
  write_u8 count                ; array element count
  for i in 0..count:
    write_u32 begin[i]          ; array entry
  
  write_u32 this[0x38]          ; tile/resource type
  
  ; --- continues at 0x0521261C ---
  write_u8  this[0x3C]          ; sub-flag
  write_u64 this[0x40]          ; rally/param
  write_u8  this[0x48]          ; extra flag 0
  write_u8  this[0x49]          ; extra flag 1
  write_u64 this[0x50]          ; param 2
  write_u8  this[0x58]          ; extra flag 2
  write_u32 this[0x5C]          ; param 3
  
  ; Encryption epilogue (0x052123B8)
  buf[0] = position             ; write payload length
  key = getServerKey()
  Encode(buf, key)
  buf[0] = position             ; update after encoding
  return success
```

## Array (Troop/Hero List)

The vector at struct offset 0x20-0x28 is a `std::vector<uint32_t>`.
- `this[0x20]` = begin pointer
- `this[0x28]` = end pointer
- Element count = `(end - begin) / 4`
- Count is written as a u8 (max 255 entries)
- Each entry is a u32, likely encoding `troop_type << 16 | troop_count` or similar

## Key Addresses

| Address | Description |
|---------|-------------|
| 0x05212294 | Function entry (prologue) |
| 0x052122E0 | First write: this[0x00] u16 |
| 0x05212418 | Main body start (after first field) |
| 0x05212324 | Array loop body |
| 0x05212604 | Array count write |
| 0x0521261C | Post-array fields start |
| 0x052123B8 | Encryption epilogue |
| 0x05212414 | Return |

## Encoding

After all fields are serialized, the function:
1. Writes the current position (payload length) to `buf[0]` as u16
2. Calls `CMsgCodec::getServerKey()` -> server_key
3. Calls `CMsgCodec::Encode(buf, server_key)` to encrypt
4. Writes the final encoded position back to `buf[0]`

## Python Payload Builder (Template)

```python
import struct

def build_march_payload(
    sub_type,       # u16 - msg sub-type
    march_type,     # u16 - march type (attack, gather, etc.)
    flag_0,         # u8
    flag_1,         # u8
    flag_2,         # u8
    flag_3,         # u8
    flag_4,         # u8  (possibly hero count)
    target_x,      # u32 - target tile X
    target_y,      # u32 - target tile Y
    kingdom_id,    # u16 - target kingdom
    march_slot,    # u16 - march queue slot
    troop_array,   # list of u32 - troop entries
    tile_type,     # u32 - resource/tile type
    sub_flag,      # u8
    rally_param,   # u64
    extra_flag_0,  # u8
    extra_flag_1,  # u8
    param_2,       # u64
    extra_flag_2,  # u8
    param_3,       # u32
):
    buf = b''
    buf += struct.pack('<H', sub_type)
    buf += struct.pack('<H', march_type)
    buf += struct.pack('<5B', flag_0, flag_1, flag_2, flag_3, flag_4)
    buf += struct.pack('<II', target_x, target_y)  # u64 = two u32
    buf += struct.pack('<H', kingdom_id)
    buf += struct.pack('<H', march_slot)
    buf += struct.pack('<B', len(troop_array))
    for entry in troop_array:
        buf += struct.pack('<I', entry)
    buf += struct.pack('<I', tile_type)
    buf += struct.pack('<B', sub_flag)
    buf += struct.pack('<Q', rally_param)
    buf += struct.pack('<BB', extra_flag_0, extra_flag_1)
    buf += struct.pack('<Q', param_2)
    buf += struct.pack('<B', extra_flag_2)
    buf += struct.pack('<I', param_3)
    return buf  # 46 + N*4 bytes
```

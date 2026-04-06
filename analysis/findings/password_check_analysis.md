# 0x1B8B - CMSG_PASSWORD_CHECK_REQUEST - Complete Analysis

## Constructor (0x0527367C)
```c
struct CMSG_PASSWORD_CHECK_REQUEST {
    uint16_t size;      // offset 0 - set to 0
    uint16_t opcode;    // offset 2 - set to 0x1B8B
    uint16_t field_4;   // offset 4 - set to 0
    // offset 6-7: padding?
    uint64_t field_8;   // offset 8 - zeroed (stp xzr, xzr covers 0x10-0x1F)
    uint64_t field_10;  // offset 0x10 - zeroed
    uint64_t field_18;  // offset 0x18 - zeroed
};
// Total struct size: ~0x20 (32 bytes)
```

## packData Serialization (0x05273690) - Field Order
Analyzing the strh/strb/str instructions to the packet buffer:

1. **u16** from `[x19]` = `self.size` (at offset 0) → written as u16
2. **u16** from `[x19, #2]` = `self.opcode` (0x1B8B) → written as u16
3. **u8** from `[x19, #6]` → written as byte (1 byte)
4. **u8** from `[x19, #7]` → written as byte (1 byte)
5. **u8** from `[x19, #8]` → written as byte (1 byte)
6. **u8** from `[x19, #9]` → written as byte (1 byte)
7. **u64** from `[x19, #0x18]` → written as 8 bytes

### Packet Layout (after header)
```
Offset  Size  Source         Description
------  ----  ------         -----------
0       2     [x19]          length prefix (u16)
2       2     [x19, #2]      opcode echo? or sub-field (u16)
3       1     BL result      Result of PLT call 0x5c6dbd0 (u16, written as u16)
5       1     [x19, #6]      byte field 1
6       1     [x19, #7]      byte field 2
7       1     [x19, #8]      byte field 3
8       1     [x19, #9]      byte field 4
9-16    8     [x19, #0x18]   u64 field (possibly a hash or token)
```

## Key Observations

### The BL calls in packData:
- `bl 0x5c6dbd0` - Called 3 times. This is a PLT stub - likely a "write u16" helper
- `bl 0x5c6dbe0` - Called once. Likely "write u64" or "write string"
- `bl 0x5c6dbc0` - Called at end. Gets server key for encryption
- `bl 0x5c6dbb0` - Called at end. This is NOT Encode, it's a different PLT entry

### Total payload fields:
- 1x u16 (self.size echo)
- 1x u16 (self.opcode echo or sub-opcode)
- Result of external call (u16)
- 4x u8 bytes (offsets 6-9 in struct)
- 1x u64 (offset 0x18 in struct)

**Estimated encrypted payload size**: 2+2+2+4+8 = **18 bytes** (+ 8 header = 26 total)

## CMSG_PASSWORD_CHECK_RETURN (Server Response)
From getData at 0x05273AC0:
```c
struct CMSG_PASSWORD_CHECK_RETURN {
    uint16_t field_0;   // read if size >= 2
    uint16_t field_2;   // read if size >= 4
    uint64_t field_8;   // read if size >= 12 (0xC)
};
```

The server sends back: u16 + u16 + u64 = 12 bytes

## LogicPassword::respCheckPassword (0x039FA52C)
The handler that processes the RETURN:
1. Calls some init function with w1=0
2. Calls function with `w2 = 0xF4240` (1,000,000 decimal!) - this is likely a timer/timeout value
3. Reads `[x20, #8]` = the u64 from the RETURN packet
4. Stores it at `[x19, #0x40]` offset in the LogicPassword object
5. Calls several manager functions to update state
6. Calls function with `w1=0` at the end

## Critical Insight
The PASSWORD_CHECK flow is:
1. Server sends PASSWORD_CHECK_RETURN with a challenge (u64 value)
2. Client must respond with PASSWORD_CHECK_REQUEST containing:
   - The 4-byte password/hash (bytes at offset 6-9)
   - A u64 token/hash (at offset 0x18)
3. If wrong, server disconnects

The "password" is likely a secondary password (二次密码) feature common in Chinese mobile games,
NOT the login password. Many players don't set this, in which case the bot might need to
send empty/zero values.

## What the Bot Should Do
1. Listen for incoming 0x1B8B RETURN packet
2. Parse the challenge u64
3. If no secondary password is set: respond with all zeros
4. If secondary password exists: compute the expected hash/response
5. Send the REQUEST with proper fields

The fact that the constructor zeroes everything suggests the DEFAULT response is all zeros -
which might be correct for accounts without a secondary password!

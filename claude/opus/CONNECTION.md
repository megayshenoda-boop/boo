# Connection & Encryption - IGG Conquerors (الفاتحون)

## Server Constants
```python
GATEWAY_IP      = "54.93.167.80"
GATEWAY_PORT    = 5997          # primary
GATEWAY_PORT_2  = 5993          # backup
WORLD_ID        = 211
GAME_ID         = "1057029902"
GAME_ID_HEX     = 0x3F00FF0E   # or 0x3F0C03AE
HEARTBEAT_SEC   = 15.0
```

## Encryption Keys
```python
CQ_XOR_KEY = "CQ_secretCQ_secretCQ_secretCQ_se"  # 32 chars, repeating
HMAC_KEY   = "07Z8D2AoYFGGivw40fEOj9swnpyF7Pw3ilKpVKnJ"
```

## CMsgCodec Encryption
```python
TABLE = [0x58, 0xef, 0xd7, 0x14, 0xa2, 0x3b, 0x9c]  # 7 bytes

# Encrypt:
enc[i] = ((plain[i] + msg_b * 17) ^ sk_b ^ TABLE[i % 7]) & 0xFF

# Where:
#   msg = random u16 → msg_lo, msg_hi
#   msg_b = msg_bytes[i % 2]   (alternating msg_lo, msg_hi)
#   sk_b  = sk_bytes[i % 4]    (server_key as 4 LE bytes)

# Decrypt:
plain[i] = ((enc[i] ^ sk_b ^ TABLE[i % 7]) - msg_b * 17) & 0xFF
```

## Server Key
- Found in opcode **0x0038** (CASTLE_DATA) response
- Field ID: **0x4F** (field 79)
- Format: u32 LE
- Must be extracted after login to decrypt/encrypt action packets

---

## Full Connection Flow

### Step 1: HTTP Login (4-step)
```
1. POST /api/login → get access_token
2. POST /api/verify → verify token
3. POST /api/gameinfo → get game server list
4. Select correct world server
```
Result: `igg_id` + `access_key` (32-char hex)

### Step 2: Gateway Auth (TCP → 54.93.167.80:5997)
```
→ Send 0x000B (79 bytes):
  [0:2]   u16  length = 79
  [2:4]   u16  opcode = 0x000B
  [4:8]   u32  version = 1
  [8:12]  u32  zeros
  [12:16] u32  IGG_ID
  [16:20] u32  zeros
  [20:22] u16  token_len = 32
  [22:54] 32B  token = XOR(access_key, CQ_XOR_KEY)
  [54:58] u32  zeros
  [58:62] u32  platform = 2 (Android)
  [62:66] u32  zeros
  [66:70] u32  WORLD_ID
  [70:74] u32  GAME_ID_HEX
  [74:78] u32  zeros
  [78]    u8   flag = 1

← Recv 0x000C (68+ bytes):
  [0:4]   u32  IGG_ID
  [4:8]   u32  padding
  [8:10]  u16  IP_str_len
  [10:X]  ASCII game_server_ip
  [X:X+2] u16  game_port
  [X+2:]  session_token (32 chars) + status + world_id
```

### Step 3: Game Server Login (TCP → game_server_ip:game_port)
```
→ Send 0x001F (64 bytes):
  [0:2]   u16  length = 64
  [2:4]   u16  opcode = 0x001F
  [4:8]   u32  version = 1
  [8:12]  u32  zeros
  [12:16] u32  IGG_ID
  [16:20] u32  zeros
  [20:22] u16  token_len = 32
  [22:54] 32B  session_token (from 0x000C)
  [54]    u8   0x0E
  [55:59] u32  GAME_ID_HEX
  [59:63] u32  zeros
  [63]    u8   0x00

← Recv 0x0020 (5 bytes): Login OK
```

### Step 4: World Entry
```
→ Send 0x0021 (21 bytes):
  [0:2]   u16  length = 21
  [2:4]   u16  opcode = 0x0021
  [4:8]   u32  IGG_ID
  [8:12]  u32  zeros
  [12]    u8   0x0E
  [13:17] u32  GAME_ID_HEX
  [17:21] 4B   [0xb0, 0x02, 0x5c, 0x00]
```

### Step 5: Receive Game Data
Server pushes multiple packets:
```
← 0x0034  PLAYER_PROFILE (resources, power)
← 0x0038  CASTLE_DATA (**extract server_key from field 0x4F!**)
← 0x003F  VIP_INFO
← 0x0064  ITEM_INFO (inventory)
← 0x0097  BUILDING_INFO (all buildings + levels)
← 0x00AA  HERO_INFO
← 0x00BE  SCIENCE_INFO (research tree)
← 0x06C2  SOLDIER_INFO (troop counts)
```

### Step 6: Auth Packet (required for march!)
```
→ Send 0x0023 (58 bytes payload, NOT encrypted):
  [0:8]   u64  flag = 1
  [8:12]  u32  IGG_ID
  [12:16] u32  zeros
  [16:18] u16  str_len = 32
  [18:50] 32B  access_key (ASCII hex)
  [50]    u8   0x0E
  [51]    u8   0xFF
  [52]    u8   0x00
  [53]    u8   0x3F
  [54:58] u32  zeros
```

### Step 7: Heartbeat (every 15 seconds)
```
→ Send 0x0042 (8-12 bytes):
  [0:2]   u16  length = 8
  [2:4]   u16  opcode = 0x0042
  [4:8]   u32  milliseconds_elapsed
  [8:12]  u32  zeros (optional)
```

---

## Resource Parsing (from 0x0034 PLAYER_PROFILE)
```
Base offset = res_start (31 bytes into payload)
[+0]   u32  food
[+8]   u32  stone
[+16]  u32  wood
[+24]  u32  ore
[+32]  u32  unknown
[+40]  u32  gold
```

## Resource Types
| ID | Resource | الاسم |
|----|----------|-------|
| 1 | Food | طعام |
| 2 | Stone | حجر |
| 3 | Wood | خشب |
| 4 | Ore | حديد |
| 5 | Gold | ذهب |

## Castle Attributes (from 0x0038)
| Field ID | Attribute | Notes |
|----------|-----------|-------|
| 0x37 (55) | Castle X | Packed coordinate |
| 0x38 (56) | Castle Y | Packed coordinate |
| 0x4F (79) | Server Key | **Critical for encryption!** |
| 0x51 (81) | Workers | Number of builders (e.g. 3) |
| 0x61 (97) | Power | Total power |

## Test Account Data
```python
IGG_ID     = 577962733   # 0x227302ED / 0x225F6F0D
KINGDOM    = 182         # 0xB6
TURF_X     = 653
TURF_Y     = 567
WORKERS    = 3
POWER      = 3235
CASTLE_LVL = 8           # (field 34 or 24)
```

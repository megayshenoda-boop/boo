# Complete Opcode Reference - IGG Conquerors (الفاتحون)

## Packet Format (Universal)
```
[0:2]  u16 LE  packet_length (includes 4-byte header)
[2:4]  u16 LE  opcode
[4+]   payload (variable)
```

## Encrypted Packet Header (8 bytes, for 0x0CE4-0x0CFB range)
```
[0:2]  u16 LE  packet_length
[2:4]  u16 LE  opcode
[4]    u8      checksum & 0xFF
[5]    u8      msg_lo
[6]    u8      msg_lo ^ 0xB7
[7]    u8      msg_hi
[8+]   encrypted payload
```

---

## 1. CONNECTION & AUTH OPCODES

| Opcode | Direction | Name | Size | Description |
|--------|-----------|------|------|-------------|
| 0x000B | → Server | GATEWAY_AUTH | 79B | Gateway login request |
| 0x000C | ← Server | GATEWAY_REDIRECT | 68B | Redirect to game server |
| 0x001F | → Server | GAME_LOGIN | 64B | Game server login |
| 0x0020 | ← Server | GAME_LOGIN_OK | 5B | Login success |
| 0x0021 | → Server | WORLD_ENTRY | 21B | Request game data |
| 0x0023 | → Server | AUTH_PACKET | 58B | Auth (IGG_ID + access_key hash) |
| 0x0042 | ↔ Both | HEARTBEAT | 8-12B | Keep-alive (every 15s) |
| 0x1B8B | → Server | SESSION | 22B | Session derivation (NOT encrypted) |

## 2. GAME DATA (Server → Client)

| Opcode | Name | Size | Description |
|--------|------|------|-------------|
| 0x0033 | SYN_ATTRIBUTE | var | Attribute change sync |
| 0x0034 | PLAYER_PROFILE | var | Player profile (resources, power, etc.) |
| 0x0038 | CASTLE_DATA | ~834B | **Contains server_key at field 0x4F!** |
| 0x003F | VIP_INFO | var | VIP login info |
| 0x0064 | ITEM_INFO | var | Inventory items |
| 0x006F | SYNC_MARCH | var | March sync data |
| 0x0097 | BUILDING_INFO | var | All building slots + levels |
| 0x0098 | WORKER_INFO | var | Worker availability |
| 0x00AA | HERO_INFO | var | Hero data |
| 0x00BE | SCIENCE_INFO | var | Research tree info |
| 0x06C2 | SOLDIER_INFO | var | Troop counts per type |

## 3. ENCRYPTED ACTION OPCODES (0x0CE4-0x0CFB)
All use CMsgCodec encryption. Payload sizes are PLAINTEXT (add 4B for encrypted header).

| Opcode | Name | Plain Size | Description | Status |
|--------|------|-----------|-------------|--------|
| 0x0CE4 | START_BUILDUP | var | Alliance rally start | Protocol only |
| 0x0CE5 | JOIN_BUILDUP | var | Join rally | Protocol only |
| 0x0CE6 | START_DEFEND | var | Garrison | Protocol only |
| 0x0CE7 | BACK_DEFEND | var | Return from garrison | Protocol only |
| **0x0CE8** | **START_MARCH** | **46-62B** | **March/Gather/Attack/Scout** | **Partially working** |
| 0x0CE9 | CANCEL_MARCH | var | Cancel march | Protocol only |
| 0x0CEA | MARCH_USE_ITEM | var | Use item on march | Protocol only |
| **0x0CEB** | **ENABLE_VIEW** | **10B** | **Scout/view map** | **✅ Verified** |
| 0x0CEC | LEAGUE_DONATE | var | Alliance donation | Protocol only |
| **0x0CED** | **TRAIN** | **19B** | **Train troops** | **✅ Verified** |
| **0x0CEE** | **RESEARCH** | **12-19B** | **Research** | **Got response** |
| **0x0CEF** | **BUILD** | **22B** | **Build/Upgrade/Demolish** | **Got response** |
| 0x0CF0 | WORLD_BATTLE | var | World battle signup | Protocol only |
| 0x0CF1 | MOVE_CASTLE | var | Move/relocate castle | Protocol only |
| 0x0CF2 | GET_OTHER_ATTR | var | Get other player info | Protocol only |
| 0x0CF3 | RAID_PLAYER | var | Attack/raid player | Protocol only |
| 0x0CF4 | ARENA_INFO | var | Arena match info | Protocol only |
| 0x0CF5 | ARENA_CHANGE | var | Change arena match | Protocol only |
| 0x0CF6 | MAIL_REQUEST | var | Read mail | Protocol only |
| 0x0CF7 | MAIL_OPERATION | var | Mail operations | Protocol only |
| 0x0CF8 | SHOP_BUY | var | Buy from shop | Protocol only |
| 0x0CF9 | BUILD_FIX | 19B | Building fix | Protocol only |
| 0x0CFB | MARCH_ONEKEY | var | March onekey item | Protocol only |

## 4. OLD-STYLE ITEM OPCODES (unencrypted)

| Opcode | Name | Description |
|--------|------|-------------|
| 0x0065 | ITEM_USE | Use item |
| 0x0066 | ITEM_USE_RESULT | Item use response |
| 0x0067 | ITEM_SELL | Sell item |
| 0x0069 | ITEM_USE_CHOOSE | Choose item variant |

## 5. OLD-STYLE BUILDING OPCODES (unencrypted)

| Opcode | Name | Description |
|--------|------|-------------|
| 0x009D | BUILD_OLD | Old build/demolish (op=05 for demolish) |
| 0x009E | BUILD_RESPONSE | Build result |
| 0x009F | BUILD_HELP | Alliance help for building |
| 0x00A1 | EXCHANGE_BUILD | Swap buildings |
| 0x00A4 | BUILD_ONEKEY | Instant build |

## 6. OLD-STYLE RESEARCH OPCODES (unencrypted)

| Opcode | Name | Description |
|--------|------|-------------|
| 0x00BF | RESEARCH_OLD | Start research |
| 0x00C0 | RESEARCH_GOLD | Research with gold |
| 0x00C1 | RESEARCH_CANCEL | Cancel research |
| 0x00C3 | RESEARCH_GOLD_SPD | Gold speed research |
| 0x00C4 | RESEARCH_ITEM_SPD | Item speedup for research |
| 0x00C6 | RESEARCH_HELP | Alliance help for research |
| 0x00C7 | RESEARCH_ONEKEY | Instant research |

## 7. OLD-STYLE TRAINING OPCODES (unencrypted)

| Opcode | Name | Description |
|--------|------|-------------|
| 0x06C3 | TRAIN_OLD | Old train command |
| 0x06C5 | TRAIN_GOLD | Train with gold |
| 0x06C6 | TRAIN_GOLD_SPD | Gold speed train |
| 0x06C7 | TRAIN_ITEM_SPD | Item speedup train |
| 0x06C9 | TRAIN_COMPLETE | Training complete |
| 0x06D4 | TRAIN_ONEKEY | Instant train |

## 8. HEALING OPCODES (unencrypted)

| Opcode | Name | Description |
|--------|------|-------------|
| 0x06CB | HEAL | Heal troops |
| 0x06CD | HEAL_GOLD | Heal with gold |
| 0x06CE | HEAL_GOLD_SPD | Gold speed heal |
| 0x06CF | HEAL_ITEM_SPD | Item speedup heal |
| 0x06D1 | HEAL_COMPLETE | Healing complete |
| 0x06D6 | HEAL_ONEKEY | Instant heal |

## 9. TRAP OPCODES (unencrypted)

| Opcode | Name | Description |
|--------|------|-------------|
| 0x014B | TRAP_BUILD | Build trap |
| 0x014E | TRAP_CANCEL | Cancel trap |
| 0x0150 | TRAP_GOLD_SPD | Gold speed trap |
| 0x0151 | TRAP_ITEM_SPD | Item speedup trap |
| 0x0154 | TRAP_DESTROY | Destroy trap |
| 0x0156 | TRAP_ONEKEY | Instant trap |

## 10. MARCH OPCODES (old-style, unencrypted)

| Opcode | Name | Description |
|--------|------|-------------|
| 0x006E | TILE_SELECT | Select map tile (5B) |
| 0x0071 | MARCH_STATE | March state return |
| 0x0072 | START_MARCH_OLD | Old march command |
| 0x0073 | CANCEL_MARCH_OLD | Cancel march |
| 0x0074 | MOVE_CASTLE_OLD | Old relocate |
| 0x007C | COLLECT_STATE | Resource collection |
| 0x007E | MARCH_COMPLETE | March finished |
| 0x007F | MARCH_END | March clear |
| 0x0078 | MARCH_DETAIL | March details |
| 0x00B8 | MARCH_STATUS_ACK | March status ack |
| 0x0323 | HERO_SELECT | Hero selection (7B) |
| 0x033E | SEARCH_MAP_REQ | Search map (4B) |
| 0x033F | SEARCH_MAP_RESP | Search result |
| 0x076C | MARCH_VALIDATION | Tile + hero + state validation |

## 11. ALLIANCE OPCODES (unencrypted)

| Opcode | Name | Description |
|--------|------|-------------|
| 0x01EC | LEAGUE_TECH_UP | Alliance tech upgrade |
| 0x01ED | LEAGUE_DONATE_OLD | Alliance donation (old) |
| 0x01FE | LEAGUE_SHOP_BUY | Alliance shop purchase |

## 12. SERVER RESPONSE OPCODES

| Opcode | Name | Description |
|--------|------|-------------|
| 0x011C | ERROR_CODE | Error response (u32 error code) |
| 0x01D6 | READY_SIG | Ready signal |
| 0x021C | BUILDING_DATA | Building state update |
| 0x022B | RESOURCE_DEDUCT | Resource deducted |
| 0x026D | GENERIC_UPDATE | Generic update |
| 0x02D1 | ACTION_CONFIRM | Action confirmed |
| 0x036C | SERVER_TICK | Timestamp sync |
| 0x0636 | MARCH_DATA | March info |
| 0x06EB | TRAINING_ENTRY | Training queue entry |
| 0x11C8 | TIMER_SET | Timer started |

## 13. MERGE GAME EVENT (2048-style mini game)

| Opcode | Direction | Name |
|--------|-----------|------|
| 0x173E | ← Push | SYNC_MERGE_EVENT_ACTION |
| 0x173F | ← Push | SYNC_MERGE_EVENT_CONFIG |
| 0x1740 | → Send | MERGE_EVENT_REWARD_REQ |
| 0x1741 | ← Recv | MERGE_EVENT_REWARD_RET |
| 0x203A | ← Push | SYNC_MERGE_GAME_INFO (board state) |
| 0x203B | ← Push | SYNC_MERGE_GAME_CHARGE |
| 0x203C | → Send | MERGE_GAME_START_REQ |
| 0x203D | ← Recv | MERGE_GAME_START_RET |
| 0x203E | → Send | MERGE_GAME_MOVE_REQ (swipe) |
| 0x203F | ← Recv | MERGE_GAME_MOVE_RET |
| 0x2040 | → Send | MERGE_GAME_USE_ITEM_REQ |
| 0x2041 | ← Recv | MERGE_GAME_USE_ITEM_RET |
| 0x2042 | → Send | MERGE_GAME_ACHIEVEMENT_REQ |
| 0x2043 | ← Recv | MERGE_GAME_ACHIEVEMENT_RET |
| 0x2044 | → Send | MERGE_GAME_PASS_REQ |
| 0x2045 | ← Recv | MERGE_GAME_PASS_RET |
| 0x2046 | ← Push | MERGE_GAME_ENERGY_CD_END |
| 0x2047 | → Send | MERGE_GAME_ADD_ENERGY_REQ |
| 0x2048 | ← Recv | MERGE_GAME_ADD_ENERGY_RET |
| 0x2049 | ← Push | SYNC_MERGE_GAME_ENERGY |

## 14. MISC / UNKNOWN OPCODES (seen in PCAP)

| Opcode | Name | Notes |
|--------|------|-------|
| 0x0245 | MARCH_SCREEN | March screen open |
| 0x0709 | UNKNOWN | Formation-related |
| 0x0767 | SYNC | Generic sync |
| 0x0769 | SYNC_2 | Generic sync variant |
| 0x0834 | FORMATION | Formation data |
| 0x0840 | INIT | Initialization |
| 0x099D | EQUIPMENT | Equipment/item purchase |
| 0x0A2C | UNKNOWN | Formation-related |

## getData Field Counts (from libgame.so disassembly)
| Action | Fields | Hex |
|--------|--------|-----|
| TRAIN | 27 | 0x1B |
| BUILD | 30 | 0x1E |
| RESEARCH | 21 | 0x15 |
| MARCH | 22 | 0x16 |

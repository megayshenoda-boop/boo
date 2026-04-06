# Alliance & War Systems - Binary Analysis Report
# Generated: 2026-04-05 22:50:33
# Source: libgame.so (104,080,728 bytes)
# Total opcodes analyzed: 388
# Symbols found: 387 constructors, 174 packData, 225 getData

## Quick Reference - All Systems

| System | Opcodes | C2S | S2C | Fire&Forget | Key Actions |
|--------|---------|-----|-----|-------------|-------------|
| LEAGUE_TECH_DONATE_SHOP | 3 | 3 | 0 | 3 | DONATE |
| LEAGUE_BOARD | 4 | 2 | 2 | 1 | BOARD_REQUEST, BOARD_LEAVE_WORD |
| LEAGUE_LATEST | 2 | 1 | 1 | 0 | LATEST_REQUEST |
| LEAGUE_STATUS | 3 | 1 | 2 | 0 | STATUS_REQUEST |
| LEAGUE_BATTLEFIELD | 17 | 8 | 9 | 4 | ENTER_BATTLEFIELD_VIEW, QUERY_BATTLEFIELD_ACTION, BATTLEFIELD_RANK_VIEW_REQUEST |
| DAMAGE_HELP | 12 | 6 | 6 | 6 | GIFT_INFO, HELP, BUY |
| AUTO_JOIN_BUILDUP | 3 | 0 | 3 | 0 | - |
| DOMINION | 12 | 6 | 6 | 4 | QUERY_INFO, QUERY_SIMPLE_BATTLE_INFO, QUERY_OFFICIAL_INFO |
| DOMINION_ACTION_KING | 18 | 9 | 9 | 1 | QUERY_ACTION_INTEGRAL_REQUEST, QUERY_ACTION_HISTORY_REQUEST, QUERY_KING_INFO_REQUEST |
| WORLD_BATTLE | 28 | 15 | 13 | 4 | QUERY_BATTLE_ACTION_CONFIG, BATTLE_ACTION_REQUEST, BATTLE_ACTION_DETAIL_REQUEST |
| WORLD_BATTLE_GROUPS | 15 | 7 | 8 | 1 | BATTLE_GROUP_INFO_REQUEST, BATTLE_GROUP_MEMBER_REQUEST, BATTLE_JOIN_GROUP_REQUEST |
| FORTRESS | 21 | 11 | 10 | 4 | ENTER_VIEW, QUERY_ACTION, SIGNUP_REQUEST |
| LOSTLAND | 49 | 28 | 21 | 13 | QUERY_ACTION_CONFIG, ENTER_VIEW, MAPINFO_REQUEST |
| LOSTLAND_BUILDINGS | 20 | 8 | 12 | 3 | LEAGUE_BUILDING_OPERAT_REQUEST, LEAGUE_BUILDING_DETAIL_REQUEST, QUERY_LEAGUEBUILD_DEFEND_INFO |
| LOSTLAND_RUSH_EVENT | 6 | 3 | 3 | 1 | QUERY_RUSH_EVENT, RUSH_EVENT_REWARD_REQUEST, RUSH_EVENT_RANK_REQUEST |
| LEGION | 42 | 20 | 22 | 3 | ACTION_REQUEST, CREATE_REQUEST, LIST_REQUEST |
| LEGION_SEASON | 20 | 11 | 9 | 2 | SEASON_ACTION_REQUEST, SEASON_ACTION_SELF_SCHEDULE_REQUEST, SEASON_ACTION_GUESS_INFO_REQUEST |
| CLANPK | 62 | 29 | 33 | 12 | SIGNUP_REQUEST, ENTER_VIEW, BATTLE_RECORD_REQUEST |
| LEAGUEPASS | 16 | 6 | 10 | 0 | ACTION_TASK_INFO_REQUEST, GROUP_RANK_INFO_REQUEST, CONTRIBUTE_INFO_REQUEST |
| LEAGUE_BIG_BOSS | 13 | 5 | 8 | 0 | BIG_BOSS_DONATE_POINT_REQUEST, BIG_BOSS_DONATE_REQUEST, BIG_BOSS_POINT_REQUEST |
| KING_CHESS | 18 | 9 | 10 | 4 | SYNC_CHESS_ACTION, CHESS_ACTION_DETAIL_INFO_REQUEST, CHESS_RANK_REQUEST |
| KING_ROAD | 4 | 1 | 3 | 0 | ROAD_REWARD_REQUEST |

## Fire-and-Forget Opcodes (No Server Response Expected)

These C2S opcodes have no matching _RETURN pair. They may be:
- One-way notifications to server
- Exploitable for rapid-fire actions without waiting
- Toggle/state changes that take effect immediately

| Opcode | Name | System | packData Size |
|--------|------|--------|---------------|
| 0x01EC | CMSG_LEAGUE_TECH_UP | LEAGUE_TECH_DONATE_SHOP | ? |
| 0x01ED | CMSG_LEAGUE_DONATE | LEAGUE_TECH_DONATE_SHOP | 2B |
| 0x01FE | CMSG_LEAGUE_SHOP_BUY | LEAGUE_TECH_DONATE_SHOP | ? |
| 0x02AA | CMSG_LEAGUE_BOARD_LEAVE_WORD | LEAGUE_BOARD | 2B |
| 0x07E5 | CMSG_ENTER_LEAGUE_BATTLEFIELD_VIEW | LEAGUE_BATTLEFIELD | 2B |
| 0x07E7 | CMSG_QUERY_LEAGUE_BATTLEFIELD_ACTION | LEAGUE_BATTLEFIELD | 2B |
| 0x07F1 | CMSG_ENTER_LEAGUE_BATTLEFIELD_REQUEST | LEAGUE_BATTLEFIELD | 2B |
| 0x07F2 | CMSG_EXIT_LEAGUE_BATTLEFIELD_REQUEST | LEAGUE_BATTLEFIELD | 2B |
| 0x1AC3 | CMSG_DAMAGE_GIFT_INFO | DAMAGE_HELP | 2B |
| 0x1AC5 | CMSG_DAMAGE_HELP | DAMAGE_HELP | 2B |
| 0x1AC7 | CMSG_DAMAGE_BUY | DAMAGE_HELP | 2B |
| 0x1AC9 | CMSG_DAMAGE_BUY_ITEM | DAMAGE_HELP | 2B |
| 0x1ACB | CMSG_DAMAGE_SHARE | DAMAGE_HELP | 5B |
| 0x1ACD | CMSG_DAMAGE_HELP_NOTIFY | DAMAGE_HELP | ? |
| 0x0245 | CMSG_QUERY_DOMINION_INFO | DOMINION | 2B |
| 0x0246 | CMSG_QUERY_DOMINION_SIMPLE_BATTLE_INFO | DOMINION | 2B |
| 0x0258 | CMSG_QUERY_DOMINION_OFFICIAL_INFO | DOMINION | 2B |
| 0x025A | CMSG_SET_DOMINION_OFFICIAL | DOMINION | 2B |
| 0x060A | CMSG_DOMINION_ACTION_END | DOMINION_ACTION_KING | ? |
| 0x083E | CMSG_QUERY_WORLD_BATTLE_ACTION_CONFIG | WORLD_BATTLE | 2B |
| 0x084C | CMSG_WORLD_BATTLE_ENTER_REQUEST | WORLD_BATTLE | 2B |
| 0x084D | CMSG_WORLD_BATTLE_EXIT_REQUEST | WORLD_BATTLE | 2B |
| 0x0CF0 | CMSG_WORLD_BATTLE_NEW_SIGN_UP_REQUEST_NEW | WORLD_BATTLE | 2B |
| 0x096D | CMSG_WORLD_BATTLEFIELD_SELF_GROUP_REQUEST | WORLD_BATTLE_GROUPS | 2B |
| 0x0F0B | CMSG_ENTER_FORTRESS_VIEW | FORTRESS | 2B |
| 0x0F0D | CMSG_QUERY_FORTRESS_ACTION | FORTRESS | 2B |
| 0x0F13 | CMSG_ENTER_FORTRESS_REQUEST | FORTRESS | 2B |
| 0x0F14 | CMSG_EXIT_FORTRESS_REQUEST | FORTRESS | 2B |
| 0x15AE | CMSG_QUERY_LOSTLAND_ACTION_CONFIG | LOSTLAND | 2B |
| 0x15B1 | CMSG_ENTER_LOSTLAND_VIEW | LOSTLAND | 2B |
| 0x15B3 | CMSG_LOSTLAND_MAPINFO_REQUEST | LOSTLAND | 2B |
| 0x15B4 | CMSG_LOSTLAND_MAPINFO_RESPONSE | LOSTLAND | ? |
| 0x15B5 | CMSG_ENTER_LOSTLAND_REQUEST | LOSTLAND | 2B |
| 0x15B6 | CMSG_EXIT_LOSTLAND_REQUEST | LOSTLAND | 2B |
| 0x15C8 | CMSG_LOSTLAND_DONATE_CD_END | LOSTLAND | 2B |
| 0x15C9 | CMSG_LOSTLAND_DONATE_INFO | LOSTLAND | ? |
| 0x15D2 | CMSG_LOSTLAND_SELF_CAMP_AREA | LOSTLAND | ? |
| 0x15D3 | CMSG_LOSTLAND_SELF_DOMINION_REQUEST | LOSTLAND | 2B |
| 0x15D4 | CMSG_LOSTLAND_SELF_DOMINION_RESPONSE | LOSTLAND | ? |
| 0x15D5 | CMSG_LOSTLAND_LEAGUE_BUILD_REQUEST | LOSTLAND | 2B |
| 0x15DB | CMSG_LOSTLAND_ACHIEVEMENT_COMPLETE | LOSTLAND | ? |
| 0x15E3 | CMSG_SELF_LEAGUEBUILD_SYNC | LOSTLAND_BUILDINGS | ? |
| 0x15EA | CMSG_QUERY_LEAGUEBUILD_DEFEND_INFO | LOSTLAND_BUILDINGS | 2B |
| 0x15EC | CMSG_KICK_LEAGUE_BUILD_DEFEND_ARMY | LOSTLAND_BUILDINGS | 2B |
| 0x1FAB | CMSG_QUERY_LOSTLAND_RUSH_EVENT | LOSTLAND_RUSH_EVENT | 5B |
| 0x0C4F | CMSG_LEGION_ACTION_REQUEST | LEGION | 2B |
| 0x0C59 | CMSG_KICK_LEGION_MEMBER | LEGION | 2B |
| 0x0C5E | CMSG_CHANGE_LEGION_POSTION | LEGION | 2B |
| 0x0E10 | CMSG_LEGION_SEASON_ACTION_REQUEST | LEGION_SEASON | 2B |
| 0x0E26 | CMSG_LEGION_FINAL_POINT | LEGION_SEASON | ? |
| 0x1AF9 | CMSG_ENTER_CLANPK_VIEW | CLANPK | 2B |
| 0x1B03 | CMSG_EXIT_CLANPK_REQUEST | CLANPK | 2B |
| 0x1B16 | CMSG_CLANPK_QUERY_DEFEND_INFO | CLANPK | 2B |
| 0x1B18 | CMSG_CLANPK_QUERY_ATTACK_INFO | CLANPK | 2B |
| 0x1B1A | CMSG_CLANPK_START_ATTACK | CLANPK | 5B |
| 0x1B1F | CMSG_CLANPK_MAILBOX_MAIL_REQUEST | CLANPK | 2B |
| 0x1B20 | CMSG_CLANPK_MAILBOX_MAIL | CLANPK | 2B |
| 0x1B21 | CMSG_CLANPK_START_DEFEND | CLANPK | 5B |
| 0x1B23 | CMSG_CLANPK_ATTACK_BUILDING_BEGIN | CLANPK | ? |
| 0x1B24 | CMSG_CLANPK_ATTACK_BUILDING_END | CLANPK | ? |
| 0x1B26 | CMSG_CLANPK_THUNDER_ATTACK_END | CLANPK | ? |
| 0x1B27 | CMSG_CLANPK_CHAT_HISTORY | CLANPK | ? |
| 0x0A30 | CMSG_KING_CHESS_ENABLE_VIEW | KING_CHESS | 2B |
| 0x0A36 | CMSG_KING_CHESS_SET_LOOK_CHAT | KING_CHESS | 2B |
| 0x0A4B | CMSG_KING_CHESS_SELF_INFO_REQUEST | KING_CHESS | 2B |
| 0x0A4C | CMSG_KING_CHESS_ALL_LEAGUE_INFO_REQUEST | KING_CHESS | 2B |

## LEAGUE_TECH_DONATE_SHOP - Alliance tech upgrades, donations, and shop

### Opcode Table

| Opcode | Name | Dir | Payload | Fields | Symbol Found |
|--------|------|-----|---------|--------|--------------|
| 0x01EC | LEAGUE_TECH_UP | C2S? | - | - | - F&F |
| 0x01ED | LEAGUE_DONATE | C2S | 2B (pack) | u16@0x0 | C+P+G F&F |
| 0x01FE | LEAGUE_SHOP_BUY | C2S | 0B (get) | - | C+G F&F |

### System Flow

### Bot-Useful Findings

- **Auto-donate**: 0x01ED CMSG_LEAGUE_DONATE (2B payload) [FIRE-AND-FORGET]
- **Auto-purchase**: 0x01FE CMSG_LEAGUE_SHOP_BUY [FIRE-AND-FORGET]

### Vulnerability Notes

- **3 fire-and-forget opcodes** - can be sent without waiting for response
  - 0x01EC CMSG_LEAGUE_TECH_UP
  - 0x01ED CMSG_LEAGUE_DONATE
  - 0x01FE CMSG_LEAGUE_SHOP_BUY

---

## LEAGUE_BOARD - Alliance message board / bulletin

### Opcode Table

| Opcode | Name | Dir | Payload | Fields | Symbol Found |
|--------|------|-----|---------|--------|--------------|
| 0x02A8 | LEAGUE_BOARD_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x02A9 | LEAGUE_BOARD_RETURN | S2C | 0B (get) | - | C+G |
| 0x02AA | LEAGUE_BOARD_LEAVE_WORD | C2S | 2B (pack) | u16@0x0 | C+P+G F&F |
| 0x02AB | LEAGUE_BOARD_LEAVE_WORD_RETURN | S2C | 0B (get) | - | C+G |

### System Flow

### Bot-Useful Findings

- No obvious automatable actions found (mostly query/view opcodes)

### Vulnerability Notes

- **1 fire-and-forget opcodes** - can be sent without waiting for response
  - 0x02AA CMSG_LEAGUE_BOARD_LEAVE_WORD

---

## LEAGUE_LATEST - Alliance latest news/log

### Opcode Table

| Opcode | Name | Dir | Payload | Fields | Symbol Found |
|--------|------|-----|---------|--------|--------------|
| 0x02DA | LEAGUE_LATEST_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x02DB | LEAGUE_LATEST_RETURN | S2C | 0B (get) | - | C+G |

### System Flow

### Bot-Useful Findings

- No obvious automatable actions found (mostly query/view opcodes)

### Vulnerability Notes

- All C2S opcodes have matching server responses (well-validated)

---

## LEAGUE_STATUS - Alliance status queries

### Opcode Table

| Opcode | Name | Dir | Payload | Fields | Symbol Found |
|--------|------|-----|---------|--------|--------------|
| 0x0F3C | LEAGUE_STATUS_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0F3D | LEAGUE_STATUS_RETURN | S2C | 0B (get) | - | C+G |
| 0x0F3E | LEAGUE_UPDATE_STATUS_RETURN | S2C | 0B (get) | - | C+G |

### System Flow

### Bot-Useful Findings

- No obvious automatable actions found (mostly query/view opcodes)

### Vulnerability Notes

- All C2S opcodes have matching server responses (well-validated)

---

## LEAGUE_BATTLEFIELD - Alliance battlefield (Baron/guild fest)

### Opcode Table

| Opcode | Name | Dir | Payload | Fields | Symbol Found |
|--------|------|-----|---------|--------|--------------|
| 0x07E4 | SYS_LEAGUE_BATTLEFIELD_INFO | S2C | 0B (get) | - | C+G |
| 0x07E5 | ENTER_LEAGUE_BATTLEFIELD_VIEW | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x07E6 | LEAGUE_BATTLEFIELD_ACTIVITY_VIEW_RETURN | S2C | 0B (get) | - | C+G |
| 0x07E7 | QUERY_LEAGUE_BATTLEFIELD_ACTION | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x07E8 | SYNC_LEAGUE_BATTLEFIELD_ACTION | S2C | 0B (get) | - | C+G |
| 0x07EA | LEAGUE_BATTLEFIELD_SIGNUP_RETURN | S2C | 0B (get) | - | C+G |
| 0x07EB | LEAGUE_BATTLEFIELD_RANK_VIEW_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x07EC | LEAGUE_BATTLEFIELD_RANK_VIEW_RETURN | S2C | 0B (get) | - | C+G |
| 0x07ED | LEAGUE_BATTLEFIELD_REWARD_CONFIG_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x07EE | LEAGUE_BATTLEFIELD_REWARD_CONFIG_RETURN | S2C | 0B (get) | - | C+G |
| 0x07EF | LEAGUE_BATTLEFIELD_GET_REWARD_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x07F0 | LEAGUE_BATTLEFIELD_GET_REWARD_RETURN | S2C | 0B (get) | - | C+G |
| 0x07F1 | ENTER_LEAGUE_BATTLEFIELD_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x07F2 | EXIT_LEAGUE_BATTLEFIELD_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x07F5 | LEAGUE_BATTLEFIELD_POINT_VIEW_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x07F6 | LEAGUE_BATTLEFIELD_POINT_VIEW_RETURN | S2C | 0B (get) | - | C+G |
| 0x0C4E | SYNC_LEAGUE_BATTLEFIELD_CONFIG | S2C | 0B (get) | - | C+G |

### System Flow

**Entry Sequence:**
1. Send 0x07E5 (CMSG_ENTER_LEAGUE_BATTLEFIELD_VIEW) - Open view
1. Send 0x07EB (CMSG_LEAGUE_BATTLEFIELD_RANK_VIEW_REQUEST) - Open view
1. Send 0x07F5 (CMSG_LEAGUE_BATTLEFIELD_POINT_VIEW_REQUEST) - Open view
2. Send 0x07E5 (CMSG_ENTER_LEAGUE_BATTLEFIELD_VIEW) - Enter
2. Send 0x07F1 (CMSG_ENTER_LEAGUE_BATTLEFIELD_REQUEST) - Enter

**Query/Info:**
- 0x07E7 (CMSG_QUERY_LEAGUE_BATTLEFIELD_ACTION)

**Exit:**
- 0x07F2 (CMSG_EXIT_LEAGUE_BATTLEFIELD_REQUEST)

### Bot-Useful Findings

- **Reward collection**: 0x07ED CMSG_LEAGUE_BATTLEFIELD_REWARD_CONFIG_REQUEST (2B payload)
- **Reward collection**: 0x07EF CMSG_LEAGUE_BATTLEFIELD_GET_REWARD_REQUEST (2B payload)

### Vulnerability Notes

- **4 fire-and-forget opcodes** - can be sent without waiting for response
  - 0x07E5 CMSG_ENTER_LEAGUE_BATTLEFIELD_VIEW
  - 0x07E7 CMSG_QUERY_LEAGUE_BATTLEFIELD_ACTION
  - 0x07F1 CMSG_ENTER_LEAGUE_BATTLEFIELD_REQUEST
  - 0x07F2 CMSG_EXIT_LEAGUE_BATTLEFIELD_REQUEST
- **2 REQUEST opcodes without matching RETURN** - server may not validate:
  - 0x07F1 CMSG_ENTER_LEAGUE_BATTLEFIELD_REQUEST
  - 0x07F2 CMSG_EXIT_LEAGUE_BATTLEFIELD_REQUEST

---

## DAMAGE_HELP - Alliance help/damage system (speed up timers)

### Opcode Table

| Opcode | Name | Dir | Payload | Fields | Symbol Found |
|--------|------|-----|---------|--------|--------------|
| 0x1AC2 | SYNC_DAMAGE_INFO | S2C | 0B (get) | - | C+G |
| 0x1AC3 | DAMAGE_GIFT_INFO | C2S? | 2B (pack) | u16@0x0 | C+P+G F&F |
| 0x1AC4 | DAMAGE_GIFT_INFO_RETURN | S2C | 0B (get) | - | C+G |
| 0x1AC5 | DAMAGE_HELP | C2S? | 2B (pack) | u16@0x0 | C+P+G F&F |
| 0x1AC6 | DAMAGE_HELP_RETURN | S2C | 0B (get) | - | C+G |
| 0x1AC7 | DAMAGE_BUY | C2S | 2B (pack) | u16@0x0 | C+P+G F&F |
| 0x1AC8 | DAMAGE_BUY_RETURN | S2C | 0B (get) | - | C+G |
| 0x1AC9 | DAMAGE_BUY_ITEM | C2S | 2B (pack) | u16@0x0 | C+P+G F&F |
| 0x1ACA | DAMAGE_BUY_ITEM_RETURN | S2C | 0B (get) | - | C+G |
| 0x1ACB | DAMAGE_SHARE | C2S? | 5B (pack) | u16@0x0 u8@0x7 u8@0x8 u8@0x9 | C+P+G F&F |
| 0x1ACC | DAMAGE_SHARE_RETURN | S2C | 0B (get) | - | C+G |
| 0x1ACD | DAMAGE_HELP_NOTIFY | C2S? | 0B (get) | - | C+G F&F |

### System Flow

### Bot-Useful Findings

- **Auto-help alliance**: 0x1AC5 CMSG_DAMAGE_HELP (2B payload) [FIRE-AND-FORGET]
- **Auto-purchase**: 0x1AC7 CMSG_DAMAGE_BUY (2B payload) [FIRE-AND-FORGET]
- **Auto-purchase**: 0x1AC9 CMSG_DAMAGE_BUY_ITEM (2B payload) [FIRE-AND-FORGET]
- **Auto-help alliance**: 0x1ACD CMSG_DAMAGE_HELP_NOTIFY [FIRE-AND-FORGET]

### Vulnerability Notes

- **6 fire-and-forget opcodes** - can be sent without waiting for response
  - 0x1AC3 CMSG_DAMAGE_GIFT_INFO
  - 0x1AC5 CMSG_DAMAGE_HELP
  - 0x1AC7 CMSG_DAMAGE_BUY
  - 0x1AC9 CMSG_DAMAGE_BUY_ITEM
  - 0x1ACB CMSG_DAMAGE_SHARE
  - 0x1ACD CMSG_DAMAGE_HELP_NOTIFY

---

## AUTO_JOIN_BUILDUP - Auto-join alliance building rally

### Opcode Table

| Opcode | Name | Dir | Payload | Fields | Symbol Found |
|--------|------|-----|---------|--------|--------------|
| 0x1EAA | SYNC_AUTO_JOIN_BUILDUP_INFO | S2C | 0B (get) | - | C+G |
| 0x1EAC | AUTO_JOIN_BUILDUP_OPEN_RETURN | S2C | 0B (get) | - | C+G |
| 0x1EAE | AUTO_JOIN_BUILDUP_CLOSE_RETURN | S2C | 0B (get) | - | C+G |

### System Flow

### Bot-Useful Findings

- No obvious automatable actions found (mostly query/view opcodes)

### Vulnerability Notes

- All C2S opcodes have matching server responses (well-validated)

---

## DOMINION - Dominion/kingdom control system

### Opcode Table

| Opcode | Name | Dir | Payload | Fields | Symbol Found |
|--------|------|-----|---------|--------|--------------|
| 0x0244 | SYNC_DOMINION_INFO | S2C | 0B (get) | - | C+G |
| 0x0245 | QUERY_DOMINION_INFO | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x0246 | QUERY_DOMINION_SIMPLE_BATTLE_INFO | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x0247 | SYNC_DOMINION_SIMPLE_BATTLE_INFO | S2C | 0B (get) | - | C+G |
| 0x0258 | QUERY_DOMINION_OFFICIAL_INFO | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x0259 | SYNC_DOMINION_OFFICIAL_INFO | S2C | 0B (get) | - | C+G |
| 0x025A | SET_DOMINION_OFFICIAL | C2S | 2B (pack) | u16@0x0 | C+P+G F&F |
| 0x025B | SET_DOMINION_OFFICIAL_RESULT | S2C | 0B (get) | - | C+G |
| 0x0260 | QUERY_DOMINION_DEFEND_NUM_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0261 | QUERY_DOMINION_DEFEND_NUM_RETURN | S2C | 0B (get) | - | C+G |
| 0x02F8 | DOMINION_LATEST_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x02F9 | DOMINION_LATEST_RETURN | S2C | 0B (get) | - | C+G |

### System Flow

**Query/Info:**
- 0x0245 (CMSG_QUERY_DOMINION_INFO)
- 0x0246 (CMSG_QUERY_DOMINION_SIMPLE_BATTLE_INFO)
- 0x0258 (CMSG_QUERY_DOMINION_OFFICIAL_INFO)
- 0x0260 (CMSG_QUERY_DOMINION_DEFEND_NUM_REQUEST)

### Bot-Useful Findings

- No obvious automatable actions found (mostly query/view opcodes)

### Vulnerability Notes

- **4 fire-and-forget opcodes** - can be sent without waiting for response
  - 0x0245 CMSG_QUERY_DOMINION_INFO
  - 0x0246 CMSG_QUERY_DOMINION_SIMPLE_BATTLE_INFO
  - 0x0258 CMSG_QUERY_DOMINION_OFFICIAL_INFO
  - 0x025A CMSG_SET_DOMINION_OFFICIAL
- **2 SET operations** - potential for privilege escalation:
  - 0x025A CMSG_SET_DOMINION_OFFICIAL
  - 0x025B CMSG_SET_DOMINION_OFFICIAL_RESULT

---

## DOMINION_ACTION_KING - Dominion action / King system (KvK rewards, officials)

### Opcode Table

| Opcode | Name | Dir | Payload | Fields | Symbol Found |
|--------|------|-----|---------|--------|--------------|
| 0x0604 | QUERY_DOMINION_ACTION_INTEGRAL_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0605 | QUERY_DOMINION_ACTION_INTEGRAL_RETURN | S2C | 0B (get) | - | C+G |
| 0x0606 | QUERY_DOMINION_ACTION_HISTORY_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0607 | QUERY_DOMINION_ACTION_HISTORY_RETURN | S2C | 0B (get) | - | C+G |
| 0x0608 | QUERY_KING_INFO_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0609 | QUERY_KING_INFO_RETURN | S2C | 0B (get) | - | C+G |
| 0x060A | DOMINION_ACTION_END | C2S? | 0B (get) | - | C+G F&F |
| 0x060C | DOMINION_ACTION_SET_SLAVE_RETURN | S2C | 0B (get) | - | C+G |
| 0x060E | KING_REWARD_INFO_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x060F | KING_REWARD_INFO_RETURN | S2C | 0B (get) | - | C+G |
| 0x0610 | BESTOW_KING_REWARD_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0611 | BESTOW_KING_REWARD_RETURN | S2C | 0B (get) | - | C+G |
| 0x0612 | QUERY_SERVER_DOMINION_ACTION_INTEGRAL_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0613 | QUERY_SERVER_DOMINION_ACTION_INTEGRAL_RETURN | S2C | 0B (get) | - | C+G |
| 0x0614 | QUERY_SERVER_DOMINION_ACTION_HISTORY_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0615 | QUERY_SERVER_DOMINION_ACTION_HISTORY_RETURN | S2C | 0B (get) | - | C+G |
| 0x0616 | QUERY_SERVER_KING_INFO_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0617 | QUERY_SERVER_KING_INFO_RETURN | S2C | 0B (get) | - | C+G |

### System Flow

**Query/Info:**
- 0x0604 (CMSG_QUERY_DOMINION_ACTION_INTEGRAL_REQUEST)
- 0x0606 (CMSG_QUERY_DOMINION_ACTION_HISTORY_REQUEST)
- 0x0608 (CMSG_QUERY_KING_INFO_REQUEST)
- 0x0612 (CMSG_QUERY_SERVER_DOMINION_ACTION_INTEGRAL_REQUEST)
- 0x0614 (CMSG_QUERY_SERVER_DOMINION_ACTION_HISTORY_REQUEST)
- 0x0616 (CMSG_QUERY_SERVER_KING_INFO_REQUEST)

### Bot-Useful Findings

- **Reward collection**: 0x060E CMSG_KING_REWARD_INFO_REQUEST (2B payload)
- **Reward collection**: 0x0610 CMSG_BESTOW_KING_REWARD_REQUEST (2B payload)

### Vulnerability Notes

- **1 fire-and-forget opcodes** - can be sent without waiting for response
  - 0x060A CMSG_DOMINION_ACTION_END

---

## WORLD_BATTLE - World Battle / Wonder War system

### Opcode Table

| Opcode | Name | Dir | Payload | Fields | Symbol Found |
|--------|------|-----|---------|--------|--------------|
| 0x083E | QUERY_WORLD_BATTLE_ACTION_CONFIG | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x083F | SYNC_WORLD_BATTLE_ACTION_CONFIG | S2C | 0B (get) | - | C+G |
| 0x0840 | WORLD_BATTLE_ACTION_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0841 | WORLD_BATTLE_ACTION_RETURN | S2C | 0B (get) | - | C+G |
| 0x0842 | WORLD_BATTLE_ACTION_DETAIL_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0843 | WORLD_BATTLE_ACTION_DETAIL_RETURN | S2C | 0B (get) | - | C+G |
| 0x0846 | WORLD_BATTLE_PLAYER_RANK_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0847 | WORLD_BATTLE_PLAYER_RANK_RETURN | S2C | 0B (get) | - | C+G |
| 0x0848 | WORLD_BATTLE_GROUP_RANK_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0849 | WORLD_BATTLE_GROUP_RANK_RETURN | S2C | 0B (get) | - | C+G |
| 0x084A | WORLD_BATTLE_OVERLORD_RECORD_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x084B | WORLD_BATTLE_OVERLORD_RECORD_RETURN | S2C | 0B (get) | - | C+G |
| 0x084C | WORLD_BATTLE_ENTER_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x084D | WORLD_BATTLE_EXIT_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x084E | WORLD_BATTLEFIELD_SYS_INFO | S2C | 0B (get) | - | C+G |
| 0x084F | WORLD_BATTLE_SERVER_OFFICIAL_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0850 | WORLD_BATTLE_SERVER_OFFICIAL_RETURN | S2C | 0B (get) | - | C+G |
| 0x0851 | WORLD_BATTLE_PLAYER_OFFICIAL_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0852 | WORLD_BATTLE_PLAYER_OFFICIAL_RETURN | S2C | 0B (get) | - | C+G |
| 0x0853 | WORLD_BATTLE_SET_SERVER_OFFICIAL_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0854 | WORLD_BATTLE_SET_SERVER_OFFICIAL_RETURN | S2C | 0B (get) | - | C+G |
| 0x0855 | WORLD_BATTLE_SET_PLAYER_OFFICIAL_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0856 | WORLD_BATTLE_SET_PLAYER_OFFICIAL_RETURN | S2C | 0B (get) | - | C+G |
| 0x085B | WORLD_BATTLE_ENTER_VIEW_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x085C | WORLD_BATTLE_ENTER_VIEW_RETURN | S2C | 0B (get) | - | C+G |
| 0x085F | WORLD_BATTLE_DOMINION_RECORD_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0860 | WORLD_BATTLE_DOMINION_RECORD_RETURN | S2C | 0B (get) | - | C+G |
| 0x0CF0 | WORLD_BATTLE_NEW_SIGN_UP_REQUEST_NEW | C2S | 2B (pack) | u16@0x0 | C+P F&F |

### System Flow

**Entry Sequence:**
1. Send 0x085B (CMSG_WORLD_BATTLE_ENTER_VIEW_REQUEST) - Open view
2. Send 0x084C (CMSG_WORLD_BATTLE_ENTER_REQUEST) - Enter
2. Send 0x085B (CMSG_WORLD_BATTLE_ENTER_VIEW_REQUEST) - Enter

**Query/Info:**
- 0x083E (CMSG_QUERY_WORLD_BATTLE_ACTION_CONFIG)

**Exit:**
- 0x084D (CMSG_WORLD_BATTLE_EXIT_REQUEST)

### Bot-Useful Findings

- No obvious automatable actions found (mostly query/view opcodes)

### Vulnerability Notes

- **4 fire-and-forget opcodes** - can be sent without waiting for response
  - 0x083E CMSG_QUERY_WORLD_BATTLE_ACTION_CONFIG
  - 0x084C CMSG_WORLD_BATTLE_ENTER_REQUEST
  - 0x084D CMSG_WORLD_BATTLE_EXIT_REQUEST
  - 0x0CF0 CMSG_WORLD_BATTLE_NEW_SIGN_UP_REQUEST_NEW
- **3 REQUEST opcodes without matching RETURN** - server may not validate:
  - 0x084C CMSG_WORLD_BATTLE_ENTER_REQUEST
  - 0x084D CMSG_WORLD_BATTLE_EXIT_REQUEST
  - 0x0CF0 CMSG_WORLD_BATTLE_NEW_SIGN_UP_REQUEST_NEW
- **2 SET operations** - potential for privilege escalation:
  - 0x0853 CMSG_WORLD_BATTLE_SET_SERVER_OFFICIAL_REQUEST
  - 0x0855 CMSG_WORLD_BATTLE_SET_PLAYER_OFFICIAL_REQUEST

---

## WORLD_BATTLE_GROUPS - World Battle group/team management

### Opcode Table

| Opcode | Name | Dir | Payload | Fields | Symbol Found |
|--------|------|-----|---------|--------|--------------|
| 0x0961 | WORLD_BATTLE_NEW_SIGN_UP_RETURN | S2C | 0B (get) | - | C+G |
| 0x0962 | WORLD_BATTLE_GROUP_INFO_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0963 | WORLD_BATTLE_GROUP_INFO_RETURN | S2C | 0B (get) | - | C+G |
| 0x0964 | WORLD_BATTLE_GROUP_MEMBER_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0965 | WORLD_BATTLE_GROUP_MEMBER_RETURN | S2C | 0B (get) | - | C+G |
| 0x0966 | WORLD_BATTLE_JOIN_GROUP_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0967 | WORLD_BATTLE_JOIN_GROUP_RETURN | S2C | 0B (get) | - | C+G |
| 0x0968 | WORLD_BATTLE_SET_POWER_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0969 | WORLD_BATTLE_SET_POWER_RETURN | S2C | 0B (get) | - | C+G |
| 0x096A | WORLD_BATTLE_KICK_MEMBER_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x096B | WORLD_BATTLE_KICK_MEMBER_RETURN | S2C | 0B (get) | - | C+G |
| 0x096C | WORLD_BATTLE_SYNC_BE_KICKED | S2C | 0B (get) | - | C+G |
| 0x096D | WORLD_BATTLEFIELD_SELF_GROUP_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x096F | WORLD_BATTLE_LEAVE_GROUP_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0970 | WORLD_BATTLE_LEAVE_GROUP_RETURN | S2C | 0B (get) | - | C+G |

### System Flow

### Bot-Useful Findings

- No obvious automatable actions found (mostly query/view opcodes)

### Vulnerability Notes

- **1 fire-and-forget opcodes** - can be sent without waiting for response
  - 0x096D CMSG_WORLD_BATTLEFIELD_SELF_GROUP_REQUEST
- **1 REQUEST opcodes without matching RETURN** - server may not validate:
  - 0x096D CMSG_WORLD_BATTLEFIELD_SELF_GROUP_REQUEST
- **1 SET operations** - potential for privilege escalation:
  - 0x0968 CMSG_WORLD_BATTLE_SET_POWER_REQUEST

---

## FORTRESS - Fortress battle system (Darknest/Fortress)

### Opcode Table

| Opcode | Name | Dir | Payload | Fields | Symbol Found |
|--------|------|-----|---------|--------|--------------|
| 0x0F0A | SYS_FORTRESS_INFO | S2C | 0B (get) | - | C+G |
| 0x0F0B | ENTER_FORTRESS_VIEW | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x0F0C | FORTRESS_ACTIVITY_VIEW_RETURN | S2C | 0B (get) | - | C+G |
| 0x0F0D | QUERY_FORTRESS_ACTION | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x0F0E | SYNC_FORTRESS_ACTION | S2C | 0B (get) | - | C+G |
| 0x0F0F | FORTRESS_SIGNUP_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0F10 | FORTRESS_SIGNUP_RETURN | S2C | 0B (get) | - | C+G |
| 0x0F11 | FORTRESS_RANK_VIEW_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0F12 | FORTRESS_RANK_VIEW_RETURN | S2C | 0B (get) | - | C+G |
| 0x0F13 | ENTER_FORTRESS_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x0F14 | EXIT_FORTRESS_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x0F1C | FORTRESS_LEVEL_RANK_VIEW_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0F1D | FORTRESS_LEVEL_RANK_VIEW_RETURN | S2C | 0B (get) | - | C+G |
| 0x0F1E | FORTRESS_LEVEL_USER_RANK_VIEW_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0F1F | FORTRESS_LEVEL_USER_RANK_VIEW_RETURN | S2C | 0B (get) | - | C+G |
| 0x0F20 | FORTRESS_DISTRIBUTE_REWARD_INFO_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0F21 | FORTRESS_DISTRIBUTE_REWARD_INFO_RETURN | S2C | 0B (get) | - | C+G |
| 0x0F22 | BESTOW_FORTRESS_REWARD_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0F23 | BESTOW_FORTRESS_REWARD_RETURN | S2C | 0B (get) | - | C+G |
| 0x0F24 | FORTRESS_USER_VALUE_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0F25 | FORTRESS_USER_VALUE_RETURN | S2C | 0B (get) | - | C+G |

### System Flow

**Entry Sequence:**
1. Send 0x0F0B (CMSG_ENTER_FORTRESS_VIEW) - Open view
1. Send 0x0F11 (CMSG_FORTRESS_RANK_VIEW_REQUEST) - Open view
1. Send 0x0F1C (CMSG_FORTRESS_LEVEL_RANK_VIEW_REQUEST) - Open view
1. Send 0x0F1E (CMSG_FORTRESS_LEVEL_USER_RANK_VIEW_REQUEST) - Open view
2. Send 0x0F0B (CMSG_ENTER_FORTRESS_VIEW) - Enter
2. Send 0x0F13 (CMSG_ENTER_FORTRESS_REQUEST) - Enter
3. Send 0x0F0F (CMSG_FORTRESS_SIGNUP_REQUEST) - Sign up

**Query/Info:**
- 0x0F0D (CMSG_QUERY_FORTRESS_ACTION)

**Exit:**
- 0x0F14 (CMSG_EXIT_FORTRESS_REQUEST)

### Bot-Useful Findings

- **Auto-signup**: 0x0F0F CMSG_FORTRESS_SIGNUP_REQUEST (2B payload)
- **Automatable**: 0x0F1E CMSG_FORTRESS_LEVEL_USER_RANK_VIEW_REQUEST (2B payload)
- **Reward collection**: 0x0F20 CMSG_FORTRESS_DISTRIBUTE_REWARD_INFO_REQUEST (2B payload)
- **Reward collection**: 0x0F22 CMSG_BESTOW_FORTRESS_REWARD_REQUEST (2B payload)
- **Automatable**: 0x0F24 CMSG_FORTRESS_USER_VALUE_REQUEST (2B payload)

### Vulnerability Notes

- **4 fire-and-forget opcodes** - can be sent without waiting for response
  - 0x0F0B CMSG_ENTER_FORTRESS_VIEW
  - 0x0F0D CMSG_QUERY_FORTRESS_ACTION
  - 0x0F13 CMSG_ENTER_FORTRESS_REQUEST
  - 0x0F14 CMSG_EXIT_FORTRESS_REQUEST
- **2 REQUEST opcodes without matching RETURN** - server may not validate:
  - 0x0F13 CMSG_ENTER_FORTRESS_REQUEST
  - 0x0F14 CMSG_EXIT_FORTRESS_REQUEST

---

## LOSTLAND - Lost Land / Lost Kingdom system

### Opcode Table

| Opcode | Name | Dir | Payload | Fields | Symbol Found |
|--------|------|-----|---------|--------|--------------|
| 0x15AE | QUERY_LOSTLAND_ACTION_CONFIG | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x15AF | SYNC_LOSTLAND_ACTION_CONFIG | S2C | 0B (get) | - | C+G |
| 0x15B0 | SYS_LOSTLAND_INFO | S2C | 0B (get) | - | C+G |
| 0x15B1 | ENTER_LOSTLAND_VIEW | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x15B2 | LOSTLAND_ACTIVITY_VIEW_RETURN | S2C | 0B (get) | - | C+G |
| 0x15B3 | LOSTLAND_MAPINFO_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x15B4 | LOSTLAND_MAPINFO_RESPONSE | C2S? | 0B (get) | - | C+G F&F |
| 0x15B5 | ENTER_LOSTLAND_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x15B6 | EXIT_LOSTLAND_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x15B7 | LOSTLAND_DONATE_RESOURCE_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x15B8 | LOSTLAND_DONATE_RESOURCE_RETURN | S2C | 0B (get) | - | C+G |
| 0x15B9 | LOSTLAND_DONATE_HEROCHIP_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x15BA | LOSTLAND_DONATE_HEROCHIP_RETURN | S2C | 0B (get) | - | C+G |
| 0x15BB | LOSTLAND_SHOP_BUY_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x15BC | LOSTLAND_SHOP_BUY_RETURN | S2C | 0B (get) | - | C+G |
| 0x15BD | SYNC_LOSTLAND_SHOP_BUY_TIMES | S2C | 0B (get) | - | C+G |
| 0x15BE | LOSTLAND_BAN_HERO_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x15BF | LOSTLAND_BAN_HERO_RETURN | S2C | 0B (get) | - | C+G |
| 0x15C0 | LOSTLAND_HERO_VOTE_COUNT_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x15C1 | LOSTLAND_HERO_VOTE_COUNT_RETURN | S2C | 0B (get) | - | C+G |
| 0x15C2 | LOSTLAND_CAMP_RANK_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x15C3 | LOSTLAND_CAMP_RANK_RETURN | S2C | 0B (get) | - | C+G |
| 0x15C4 | LOSTLAND_LEAGUE_RANK_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x15C5 | LOSTLAND_LEAGUE_RANK_RETURN | S2C | 0B (get) | - | C+G |
| 0x15C6 | LOSTLAND_PLAYER_RANK_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x15C7 | LOSTLAND_PLAYER_RANK_RETURN | S2C | 0B (get) | - | C+G |
| 0x15C8 | LOSTLAND_DONATE_CD_END | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x15C9 | LOSTLAND_DONATE_INFO | C2S | 0B (get) | - | C+G F&F |
| 0x15CA | LOSTLAND_MARK_REWARD_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x15CB | LOSTLAND_MARK_REWARD_RETURN | S2C | 0B (get) | - | C+G |
| 0x15CC | LOSTLAND_HISTORY_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x15CD | LOSTLAND_HISTORY_RETURN | S2C | 0B (get) | - | C+G |
| 0x15CE | LOSTLAND_LEAGUE_HISTORY_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x15CF | LOSTLAND_LEAGUE_HISTORY_RETURN | S2C | 0B (get) | - | C+G |
| 0x15D0 | LOSTLAND_PLAYER_HISTORY_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x15D1 | LOSTLAND_PLAYER_HISTORY_RETURN | S2C | 0B (get) | - | C+G |
| 0x15D2 | LOSTLAND_SELF_CAMP_AREA | C2S? | 0B (get) | - | C+G F&F |
| 0x15D3 | LOSTLAND_SELF_DOMINION_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x15D4 | LOSTLAND_SELF_DOMINION_RESPONSE | C2S? | 0B (get) | - | C+G F&F |
| 0x15D5 | LOSTLAND_LEAGUE_BUILD_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x15D7 | SYS_LOSTLAND_WEEK_BAN_HERO | S2C | 0B (get) | - | C+G |
| 0x15D8 | ENTER_LOSTLAND_ERROR_RETURN | S2C | 0B (get) | - | C+G |
| 0x15D9 | LOSTLAND_ACHIEVEMENT_LIST_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x15DA | LOSTLAND_ACHIEVEMENT_LIST_RETURN | S2C | 0B (get) | - | C+G |
| 0x15DB | LOSTLAND_ACHIEVEMENT_COMPLETE | C2S? | 0B (get) | - | C+G F&F |
| 0x15DC | LOSTLAND_ACHIEVEMENT_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x15DD | LOSTLAND_ACHIEVEMENT_RETURN | S2C | 0B (get) | - | C+G |
| 0x15DE | LOSTLAND_ACHIEVEMENT_REWARD_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x15DF | LOSTLAND_ACHIEVEMENT_REWARD_RETURN | S2C | 0B (get) | - | C+G |

### System Flow

**Entry Sequence:**
1. Send 0x15B1 (CMSG_ENTER_LOSTLAND_VIEW) - Open view
2. Send 0x15B1 (CMSG_ENTER_LOSTLAND_VIEW) - Enter
2. Send 0x15B5 (CMSG_ENTER_LOSTLAND_REQUEST) - Enter

**Query/Info:**
- 0x15AE (CMSG_QUERY_LOSTLAND_ACTION_CONFIG)

**Exit:**
- 0x15B6 (CMSG_EXIT_LOSTLAND_REQUEST)

### Bot-Useful Findings

- **Auto-donate**: 0x15B7 CMSG_LOSTLAND_DONATE_RESOURCE_REQUEST (2B payload)
- **Auto-donate**: 0x15B9 CMSG_LOSTLAND_DONATE_HEROCHIP_REQUEST (2B payload)
- **Auto-purchase**: 0x15BB CMSG_LOSTLAND_SHOP_BUY_REQUEST (2B payload)
- **Auto-purchase**: 0x15BD CMSG_SYNC_LOSTLAND_SHOP_BUY_TIMES
- **Auto-donate**: 0x15C8 CMSG_LOSTLAND_DONATE_CD_END (2B payload) [FIRE-AND-FORGET]
- **Auto-donate**: 0x15C9 CMSG_LOSTLAND_DONATE_INFO [FIRE-AND-FORGET]
- **Reward collection**: 0x15CA CMSG_LOSTLAND_MARK_REWARD_REQUEST (2B payload)
- **Reward collection**: 0x15DE CMSG_LOSTLAND_ACHIEVEMENT_REWARD_REQUEST (2B payload)

### Vulnerability Notes

- **13 fire-and-forget opcodes** - can be sent without waiting for response
  - 0x15AE CMSG_QUERY_LOSTLAND_ACTION_CONFIG
  - 0x15B1 CMSG_ENTER_LOSTLAND_VIEW
  - 0x15B3 CMSG_LOSTLAND_MAPINFO_REQUEST
  - 0x15B4 CMSG_LOSTLAND_MAPINFO_RESPONSE
  - 0x15B5 CMSG_ENTER_LOSTLAND_REQUEST
  - 0x15B6 CMSG_EXIT_LOSTLAND_REQUEST
  - 0x15C8 CMSG_LOSTLAND_DONATE_CD_END
  - 0x15C9 CMSG_LOSTLAND_DONATE_INFO
  - 0x15D2 CMSG_LOSTLAND_SELF_CAMP_AREA
  - 0x15D3 CMSG_LOSTLAND_SELF_DOMINION_REQUEST
  - 0x15D4 CMSG_LOSTLAND_SELF_DOMINION_RESPONSE
  - 0x15D5 CMSG_LOSTLAND_LEAGUE_BUILD_REQUEST
  - 0x15DB CMSG_LOSTLAND_ACHIEVEMENT_COMPLETE
- **5 REQUEST opcodes without matching RETURN** - server may not validate:
  - 0x15B3 CMSG_LOSTLAND_MAPINFO_REQUEST
  - 0x15B5 CMSG_ENTER_LOSTLAND_REQUEST
  - 0x15B6 CMSG_EXIT_LOSTLAND_REQUEST
  - 0x15D3 CMSG_LOSTLAND_SELF_DOMINION_REQUEST
  - 0x15D5 CMSG_LOSTLAND_LEAGUE_BUILD_REQUEST

---

## LOSTLAND_BUILDINGS - Lost Land buildings and structures

### Opcode Table

| Opcode | Name | Dir | Payload | Fields | Symbol Found |
|--------|------|-----|---------|--------|--------------|
| 0x15E0 | LEAGUE_BUILDING_OPERAT_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x15E1 | LEAGUE_BUILDING_OPERAT_RETURN | S2C | 0B (get) | - | C+G |
| 0x15E3 | SELF_LEAGUEBUILD_SYNC | C2S? | 0B (get) | - | C+G F&F |
| 0x15E4 | LEAGUE_BUILDING_DETAIL_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x15E5 | LEAGUE_BUILDING_DETAIL_RETURN | S2C | 0B (get) | - | C+G |
| 0x15E6 | SYNC_ALL_LEAGUEBUILD_BATTLE_COUNT | S2C | 0B (get) | - | C+G |
| 0x15E7 | ADD_LEAGUEBUILD | S2C | 0B (get) | - | C+G |
| 0x15E8 | UPDATE_LEAGUEBUILD | S2C | 0B (get) | - | C+G |
| 0x15E9 | DELETE_LEAGUEBUILD | S2C | 0B (get) | - | C+G |
| 0x15EA | QUERY_LEAGUEBUILD_DEFEND_INFO | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x15EB | SYNC_LEAGUEBUILD_DEFEND_INFO | S2C | 0B (get) | - | C+G |
| 0x15EC | KICK_LEAGUE_BUILD_DEFEND_ARMY | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x15F1 | LOSTLAND_LEAGUE_LATEST_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x15F2 | LOSTLAND_LEAGUE_LATEST_RETURN | S2C | 0B (get) | - | C+G |
| 0x15F3 | UPDATE_LEAGUEBUILD_CONNECT_STATUS | S2C | 0B (get) | - | C+G |
| 0x15FA | LOSTLAND_BUILDING_INDEX_OPEN_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x15FB | LOSTLAND_BUILDING_INDEX_OPEN_RETURN | S2C | 0B (get) | - | C+G |
| 0x15FE | SYNC_LOSTLAND_MONTH_CARD_INFO | S2C | 0B (get) | - | C+G |
| 0x15FF | LOSTLAND_MONTH_CARD_REWARD_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x1600 | LOSTLAND_MONTH_CARD_REWARD_RETURN | S2C | 0B (get) | - | C+G |

### System Flow

**Query/Info:**
- 0x15EA (CMSG_QUERY_LEAGUEBUILD_DEFEND_INFO)

### Bot-Useful Findings

- **Reward collection**: 0x15FF CMSG_LOSTLAND_MONTH_CARD_REWARD_REQUEST (2B payload)

### Vulnerability Notes

- **3 fire-and-forget opcodes** - can be sent without waiting for response
  - 0x15E3 CMSG_SELF_LEAGUEBUILD_SYNC
  - 0x15EA CMSG_QUERY_LEAGUEBUILD_DEFEND_INFO
  - 0x15EC CMSG_KICK_LEAGUE_BUILD_DEFEND_ARMY

---

## LOSTLAND_RUSH_EVENT - Lost Land rush event

### Opcode Table

| Opcode | Name | Dir | Payload | Fields | Symbol Found |
|--------|------|-----|---------|--------|--------------|
| 0x1FAB | QUERY_LOSTLAND_RUSH_EVENT | C2S | 5B (pack) | u16@0x0 u8@0x7 u8@0x8 u8@0x9 | C+P F&F |
| 0x1FAC | SYNC_LOSTLAND_RUSH_EVENT | S2C | 0B (get) | - | C+G |
| 0x1FAD | LOSTLAND_RUSH_EVENT_REWARD_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x1FAE | LOSTLAND_RUSH_EVENT_REWARD_RETURN | S2C | 0B (get) | - | C+G |
| 0x1FAF | LOSTLAND_RUSH_EVENT_RANK_REQUEST | C2S | 5B (pack) | u16@0x0 u8@0x7 u8@0x8 u8@0x9 | C+P |
| 0x1FB0 | LOSTLAND_RUSH_EVENT_RANK_RETURN | S2C | 0B (get) | - | C+G |

### System Flow

**Query/Info:**
- 0x1FAB (CMSG_QUERY_LOSTLAND_RUSH_EVENT)

### Bot-Useful Findings

- **Reward collection**: 0x1FAD CMSG_LOSTLAND_RUSH_EVENT_REWARD_REQUEST (2B payload)

### Vulnerability Notes

- **1 fire-and-forget opcodes** - can be sent without waiting for response
  - 0x1FAB CMSG_QUERY_LOSTLAND_RUSH_EVENT

---

## LEGION - Legion system (cross-server guild wars)

### Opcode Table

| Opcode | Name | Dir | Payload | Fields | Symbol Found |
|--------|------|-----|---------|--------|--------------|
| 0x0C4F | LEGION_ACTION_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x0C51 | LEGION_CREATE_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0C52 | LEGION_CREATE_RETURN | S2C | 0B (get) | - | C+G |
| 0x0C53 | LEGION_LIST_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0C54 | LEGION_LIST_RETURN | S2C | 0B (get) | - | C+G |
| 0x0C55 | LEGION_INFO_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0C56 | LEGION_INFO_RETURN | S2C | 0B (get) | - | C+G |
| 0x0C57 | LEGION_JOIN_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0C58 | LEGION_JOIN_RETURN | S2C | 0B (get) | - | C+G |
| 0x0C59 | KICK_LEGION_MEMBER | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x0C5A | NOTIFY_LEGION_MEMBER_JOIN | S2C | 0B (get) | - | C+G |
| 0x0C5B | NOTIFY_LEGION_MEMBER_LEAVE | S2C | 0B (get) | - | C+G |
| 0x0C5C | LEGION_ADD_MEMBER_LIST_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0C5D | LEGION_ADD_MEMBER_LIST_RETURN | S2C | 0B (get) | - | C+G |
| 0x0C5E | CHANGE_LEGION_POSTION | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x0C5F | NOTIFY_LEGION_MEMBER_CHANGE | S2C | 0B (get) | - | C+G |
| 0x0C60 | CHANGE_LEGION_CHANGE_NAME_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0C61 | CHANGE_LEGION_CHANGE_NAME_RETURN | S2C | 0B (get) | - | C+G |
| 0x0C62 | NOTIFY_LEGION_NAME_CHANGE | S2C | 0B (get) | - | C+G |
| 0x0C63 | LEGION_RANK_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0C64 | LEGION_RANK_RETURN | S2C | 0B (get) | - | C+G |
| 0x0C65 | LEGION_SET_TALENT_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0C66 | LEGION_SET_TALENT_RETURN | S2C | 0B (get) | - | C+G |
| 0x0C67 | LEGION_CHANGE_POS_TIMES_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0C68 | LEGION_CHANGE_POS_TIMES_RETURN | S2C | 0B (get) | - | C+G |
| 0x0C69 | NOTIFY_LEGION_CHANGE_POS_TIMES | S2C | 0B (get) | - | C+G |
| 0x0C6E | LEGION_LATEST_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0C6F | LEGION_LATEST_RETURN | S2C | 0B (get) | - | C+G |
| 0x0C70 | LEGION_SELF_JOIN_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0C71 | LEGION_SELF_JOIN_RETURN | S2C | 0B (get) | - | C+G |
| 0x0C72 | LEGION_SELF_LEAVE_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0C73 | LEGION_SELF_LEAVE_RETURN | S2C | 0B (get) | - | C+G |
| 0x0C74 | LEGION_BATTLE_MAP_INFO_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0C75 | LEGION_BATTLE_MAP_INFO_RETURN | S2C | 0B (get) | - | C+G |
| 0x0C76 | LEGION_RESOURCE_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0C77 | LEGION_RESOURCE_RETURN | S2C | 0B (get) | - | C+G |
| 0x0C78 | LEGION_MEMBER_INFO_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0C79 | LEGION_MEMBER_INFO_RETURN | S2C | 0B (get) | - | C+G |
| 0x0C7A | LEGION_ENEMY_POS_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0C7B | LEGION_ENEMY_POS_RETURN | S2C | 0B (get) | - | C+G |
| 0x0C7C | LEGION_VALUE_DETAIL_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0C7D | LEGION_VALUE_DETAIL_RETURN | S2C | 0B (get) | - | C+G |

### System Flow

### Bot-Useful Findings

- No obvious automatable actions found (mostly query/view opcodes)

### Vulnerability Notes

- **3 fire-and-forget opcodes** - can be sent without waiting for response
  - 0x0C4F CMSG_LEGION_ACTION_REQUEST
  - 0x0C59 CMSG_KICK_LEGION_MEMBER
  - 0x0C5E CMSG_CHANGE_LEGION_POSTION
- **1 REQUEST opcodes without matching RETURN** - server may not validate:
  - 0x0C4F CMSG_LEGION_ACTION_REQUEST
- **1 SET operations** - potential for privilege escalation:
  - 0x0C65 CMSG_LEGION_SET_TALENT_REQUEST

---

## LEGION_SEASON - Legion Season / Championship system

### Opcode Table

| Opcode | Name | Dir | Payload | Fields | Symbol Found |
|--------|------|-----|---------|--------|--------------|
| 0x0E10 | LEGION_SEASON_ACTION_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x0E12 | LEGION_SEASON_ACTION_SELF_SCHEDULE_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0E13 | LEGION_SEASON_ACTION_SELF_SCHEDULE_RETURN | S2C | 0B (get) | - | C+G |
| 0x0E16 | LEGION_SEASON_ACTION_GUESS_INFO_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0E17 | LEGION_SEASON_ACTION_GUESS_INFO_RETURN | S2C | 0B (get) | - | C+G |
| 0x0E18 | LEGION_SEASON_ACTION_GUESS_BET_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0E19 | LEGION_SEASON_ACTION_GUESS_BET_RETURN | S2C | 0B (get) | - | C+G |
| 0x0E1A | LEGION_SEASON_ACTION_PLAYOFF_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0E1B | LEGION_SEASON_ACTION_PLAYOFF_RETURN | S2C | 0B (get) | - | C+G |
| 0x0E1C | LEGION_SEASON_ACTION_HIS_PLAYER_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0E1D | LEGION_SEASON_ACTION_HIS_PLAYER_RETURN | S2C | 0B (get) | - | C+G |
| 0x0E1E | LEGION_SEASON_ACTION_HIS_MVP_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0E1F | LEGION_SEASON_ACTION_HIS_MVP_RETURN | S2C | 0B (get) | - | C+G |
| 0x0E20 | LEGION_SEASON_ACTION_HIS_BEST_PLAYER_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0E21 | LEGION_SEASON_ACTION_HIS_BEST_PLAYER_RETURN | S2C | 0B (get) | - | C+G |
| 0x0E22 | LEGION_SEASON_ACTION_LIKE_PLAYER_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0E23 | LEGION_SEASON_ACTION_LIKE_PLAYER_RETURN | S2C | 0B (get) | - | C+G |
| 0x0E26 | LEGION_FINAL_POINT | C2S? | 0B (get) | - | C+G F&F |
| 0x0E27 | LEGION_MEMBER_HIS_INFO_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0E28 | LEGION_MEMBER_HIS_INFO_RETURN | S2C | 0B (get) | - | C+G |

### System Flow

### Bot-Useful Findings

- No obvious automatable actions found (mostly query/view opcodes)

### Vulnerability Notes

- **2 fire-and-forget opcodes** - can be sent without waiting for response
  - 0x0E10 CMSG_LEGION_SEASON_ACTION_REQUEST
  - 0x0E26 CMSG_LEGION_FINAL_POINT
- **1 REQUEST opcodes without matching RETURN** - server may not validate:
  - 0x0E10 CMSG_LEGION_SEASON_ACTION_REQUEST

---

## CLANPK - Clan PK / Guild Showdown system

### Opcode Table

| Opcode | Name | Dir | Payload | Fields | Symbol Found |
|--------|------|-----|---------|--------|--------------|
| 0x1AF4 | SYNC_CLANPK_CONFIG | S2C | 0B (get) | - | C+G |
| 0x1AF5 | SYNC_CLANPK_INFO | S2C | 0B (get) | - | C+G |
| 0x1AF6 | SYNC_CLANPK_FINAL_DETAIL_INFO | S2C | 0B (get) | - | C+G |
| 0x1AF7 | CLANPK_SIGNUP_REQUEST | C2S | 5B (pack) | u16@0x0 u8@0x7 u8@0x8 u8@0x9 | C+P |
| 0x1AF8 | CLANPK_SIGNUP_RETURN | S2C | 0B (get) | - | C+G |
| 0x1AF9 | ENTER_CLANPK_VIEW | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x1AFA | CLANPK_ACTIVITY_VIEW_RETURN | S2C | 0B (get) | - | C+G |
| 0x1AFB | CLANPK_BATTLE_RECORD_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x1AFC | CLANPK_BATTLE_RECORD_RETURN | S2C | 0B (get) | - | C+G |
| 0x1AFD | CLANPK_LEVEL_RANK_VIEW_REQUEST | C2S | 5B (pack) | u16@0x0 u8@0x7 u8@0x8 u8@0x9 | C+P |
| 0x1AFE | CLANPK_LEVEL_RANK_VIEW_RETURN | S2C | 0B (get) | - | C+G |
| 0x1AFF | CLANPK_USER_RANK_VIEW_REQUEST | C2S | 5B (pack) | u16@0x0 u8@0x7 u8@0x8 u8@0x9 | C+P |
| 0x1B00 | CLANPK_USER_RANK_VIEW_RETURN | S2C | 0B (get) | - | C+G |
| 0x1B01 | ENTER_CLANPK_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x1B02 | ENTER_CLANPK_RETURN | S2C | 0B (get) | - | C+G |
| 0x1B03 | EXIT_CLANPK_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x1B04 | CLANPK_BUILDING_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x1B05 | CLANPK_BUILDING_RETURN | S2C | 0B (get) | - | C+G |
| 0x1B06 | CLANPK_BUILD_UPGRADE_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x1B07 | CLANPK_BUILD_UPGRADE_RETURN | S2C | 0B (get) | - | C+G |
| 0x1B08 | CLANPK_DONATE_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x1B09 | CLANPK_DONATE_RETURN | S2C | 0B (get) | - | C+G |
| 0x1B0A | CLANPK_SET_DEFEND_HERO_REQUEST | C2S | 1B (pack) | u8@0x48 | C+P |
| 0x1B0B | CLANPK_SET_DEFEND_HERO_RETURN | S2C | 0B (get) | - | C+G |
| 0x1B0C | CLANPK_SET_ATTACK_HERO_REQUEST | C2S | 1B (pack) | u8@0x48 | C+P |
| 0x1B0D | CLANPK_SET_ATTACK_HERO_RETURN | S2C | 0B (get) | - | C+G |
| 0x1B0E | CLANPK_SET_ASSIST_HERO_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x1B0F | CLANPK_SET_ASSIST_HERO_RETURN | S2C | 0B (get) | - | C+G |
| 0x1B10 | CLANPK_GIVE_ASSIST_HERO_REQUEST | C2S | 5B (pack) | u16@0x0 u8@0x7 u8@0x8 u8@0x9 | C+P |
| 0x1B11 | CLANPK_GIVE_ASSIST_HERO_RETURN | S2C | 0B (get) | - | C+G |
| 0x1B14 | CLANPK_ASSIST_HERO_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x1B15 | CLANPK_ASSIST_HERO_RETURN | S2C | 0B (get) | - | C+G |
| 0x1B16 | CLANPK_QUERY_DEFEND_INFO | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x1B17 | SYNC_CLANPK_DEFEND_INFO | S2C | 0B (get) | - | C+G |
| 0x1B18 | CLANPK_QUERY_ATTACK_INFO | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x1B19 | SYNC_CLANPK_ATTACK_INFO | S2C | 0B (get) | - | C+G |
| 0x1B1A | CLANPK_START_ATTACK | C2S | 5B (pack) | u16@0x0 u8@0x7 u8@0x8 u8@0x9 | C+P+G F&F |
| 0x1B1B | CLANPK_START_ATTACK_RETURN | S2C | 0B (get) | - | C+G |
| 0x1B1D | SET_CLANPK_DEFEND_AMRY_INFO_RESULT | S2C | 0B (get) | - | C+G |
| 0x1B1F | CLANPK_MAILBOX_MAIL_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x1B20 | CLANPK_MAILBOX_MAIL | C2S? | 2B (pack) | u16@0x0 | C+P+G F&F |
| 0x1B21 | CLANPK_START_DEFEND | C2S | 5B (pack) | u16@0x0 u8@0x7 u8@0x8 u8@0x9 | C+P+G F&F |
| 0x1B22 | CLANPK_START_DEFEND_RETURN | S2C | 0B (get) | - | C+G |
| 0x1B23 | CLANPK_ATTACK_BUILDING_BEGIN | C2S? | 0B (get) | - | C+G F&F |
| 0x1B24 | CLANPK_ATTACK_BUILDING_END | C2S? | 0B (get) | - | C+G F&F |
| 0x1B26 | CLANPK_THUNDER_ATTACK_END | C2S? | 0B (get) | - | C+G F&F |
| 0x1B27 | CLANPK_CHAT_HISTORY | C2S? | 0B (get) | - | C+G F&F |
| 0x1B28 | UPDATE_CLANPK_DEFEND_AMRY_INFO | S2C | 0B (get) | - | C+G |
| 0x1B29 | UPDATE_CLANPK_ATTACK_AMRY_INFO | S2C | 0B (get) | - | C+G |
| 0x1B2A | CLANPK_UPDATE_ASSIST_HERO | S2C | 0B (get) | - | C+G |
| 0x1B2B | CLANPK_UPDATE_BUILDING_INFO | S2C | 0B (get) | - | C+G |
| 0x1B2C | UPDATE_CLANPK_AMRY_INFO | S2C | 0B (get) | - | C+G |
| 0x1B2D | CLANPK_DEFEND_AMRY_REQUEST | C2S | 5B (pack) | u16@0x0 u8@0x7 u8@0x8 u8@0x9 | C+P |
| 0x1B2E | CLANPK_DEFEND_AMRY_RETURN | S2C | 0B (get) | - | C+G |
| 0x1B30 | CLANPK_DEFEND_BUILDING_RETURN | S2C | 0B (get) | - | C+G |
| 0x1B31 | CLANPK_ADD_KILL_VALUE | S2C | 0B (get) | - | C+G |
| 0x1B32 | CLANPK_ACTIVITY_INFO_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x1B33 | CLANPK_ACTIVITY_INFO_RETURN | S2C | 0B (get) | - | C+G |
| 0x1B34 | CLANPK_CHECK_SET_DEF_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x1B35 | CLANPK_CHECK_SET_DEF_RETURN | S2C | 0B (get) | - | C+G |
| 0x1B36 | CLANPK_FIRST_LEVEL_REWARD_REQUEST | C2S | 5B (pack) | u16@0x0 u8@0x7 u8@0x8 u8@0x9 | C+P |
| 0x1B37 | CLANPK_FIRST_LEVEL_REWARD_RETURN | S2C | 0B (get) | - | C+G |

### System Flow

**Entry Sequence:**
1. Send 0x1AF9 (CMSG_ENTER_CLANPK_VIEW) - Open view
1. Send 0x1AFD (CMSG_CLANPK_LEVEL_RANK_VIEW_REQUEST) - Open view
1. Send 0x1AFF (CMSG_CLANPK_USER_RANK_VIEW_REQUEST) - Open view
2. Send 0x1AF9 (CMSG_ENTER_CLANPK_VIEW) - Enter
2. Send 0x1B01 (CMSG_ENTER_CLANPK_REQUEST) - Enter
3. Send 0x1AF7 (CMSG_CLANPK_SIGNUP_REQUEST) - Sign up

**Query/Info:**
- 0x1B16 (CMSG_CLANPK_QUERY_DEFEND_INFO)
- 0x1B18 (CMSG_CLANPK_QUERY_ATTACK_INFO)

**Exit:**
- 0x1B03 (CMSG_EXIT_CLANPK_REQUEST)

### Bot-Useful Findings

- **Auto-signup**: 0x1AF7 CMSG_CLANPK_SIGNUP_REQUEST (5B payload)
- **Automatable**: 0x1AFF CMSG_CLANPK_USER_RANK_VIEW_REQUEST (5B payload)
- **Auto-donate**: 0x1B08 CMSG_CLANPK_DONATE_REQUEST (2B payload)
- **Reward collection**: 0x1B36 CMSG_CLANPK_FIRST_LEVEL_REWARD_REQUEST (5B payload)

### Vulnerability Notes

- **12 fire-and-forget opcodes** - can be sent without waiting for response
  - 0x1AF9 CMSG_ENTER_CLANPK_VIEW
  - 0x1B03 CMSG_EXIT_CLANPK_REQUEST
  - 0x1B16 CMSG_CLANPK_QUERY_DEFEND_INFO
  - 0x1B18 CMSG_CLANPK_QUERY_ATTACK_INFO
  - 0x1B1A CMSG_CLANPK_START_ATTACK
  - 0x1B1F CMSG_CLANPK_MAILBOX_MAIL_REQUEST
  - 0x1B20 CMSG_CLANPK_MAILBOX_MAIL
  - 0x1B21 CMSG_CLANPK_START_DEFEND
  - 0x1B23 CMSG_CLANPK_ATTACK_BUILDING_BEGIN
  - 0x1B24 CMSG_CLANPK_ATTACK_BUILDING_END
  - 0x1B26 CMSG_CLANPK_THUNDER_ATTACK_END
  - 0x1B27 CMSG_CLANPK_CHAT_HISTORY
- **2 REQUEST opcodes without matching RETURN** - server may not validate:
  - 0x1B03 CMSG_EXIT_CLANPK_REQUEST
  - 0x1B1F CMSG_CLANPK_MAILBOX_MAIL_REQUEST
- **5 SET operations** - potential for privilege escalation:
  - 0x1B0A CMSG_CLANPK_SET_DEFEND_HERO_REQUEST
  - 0x1B0C CMSG_CLANPK_SET_ATTACK_HERO_REQUEST
  - 0x1B0E CMSG_CLANPK_SET_ASSIST_HERO_REQUEST
  - 0x1B1D CMSG_SET_CLANPK_DEFEND_AMRY_INFO_RESULT
  - 0x1B34 CMSG_CLANPK_CHECK_SET_DEF_REQUEST

---

## LEAGUEPASS - League Pass / Guild Pass system

### Opcode Table

| Opcode | Name | Dir | Payload | Fields | Symbol Found |
|--------|------|-----|---------|--------|--------------|
| 0x1663 | SYNC_LEAGUEPASS_ACTION | S2C | 0B (get) | - | C+G |
| 0x1666 | LEAGUEPASS_ACTION_TASK_INFO_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x1667 | LEAGUEPASS_ACTION_TASK_INFO_RETURN | S2C | 0B (get) | - | C+G |
| 0x1668 | LEAGUEPASS_GROUP_RANK_INFO_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x1669 | LEAGUEPASS_GROUP_RANK_INFO_RETURN | S2C | 0B (get) | - | C+G |
| 0x166A | LEAGUEPASS_CONTRIBUTE_INFO_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x166B | LEAGUEPASS_CONTRIBUTE_INFO_RETURN | S2C | 0B (get) | - | C+G |
| 0x166C | LEAGUEPASS_GET_REWARD_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x166D | LEAGUEPASS_GET_REWARD_RETURN | S2C | 0B (get) | - | C+G |
| 0x166E | LEAGUEPASS_FRESH_TASK_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x166F | LEAGUEPASS_FRESH_TASK_RETURN | S2C | 0B (get) | - | C+G |
| 0x1670 | LEAGUEPASS_FINISH_TASK_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x1671 | LEAGUEPASS_FINISH_TASK_RETURN | S2C | 0B (get) | - | C+G |
| 0x1672 | SYNC_LEAGUEPASS_TASK_REFRESH | S2C | 0B (get) | - | C+G |
| 0x1673 | SYNC_LEAGUEPASS_UPDATE_MY_TASK | S2C | 0B (get) | - | C+G |
| 0x1674 | SYNC_LEAGUEPASS_ADVANCEDGIFT | S2C | 0B (get) | - | C+G |

### System Flow

### Bot-Useful Findings

- **Reward collection**: 0x166C CMSG_LEAGUEPASS_GET_REWARD_REQUEST (2B payload)
- **Auto-refresh task**: 0x166E CMSG_LEAGUEPASS_FRESH_TASK_REQUEST (2B payload)
- **Auto-complete task**: 0x1670 CMSG_LEAGUEPASS_FINISH_TASK_REQUEST (2B payload)

### Vulnerability Notes

- All C2S opcodes have matching server responses (well-validated)

---

## LEAGUE_BIG_BOSS - League Big Boss / Guild Boss system

### Opcode Table

| Opcode | Name | Dir | Payload | Fields | Symbol Found |
|--------|------|-----|---------|--------|--------------|
| 0x1F0E | SYNC_LEAGUE_BIG_BOSS_CONFIG | S2C | 0B (get) | - | C+G |
| 0x1F0F | LEAGUE_BIG_BOSS_DONATE_POINT_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x1F10 | LEAGUE_BIG_BOSS_DONATE_POINT_RETURN | S2C | 0B (get) | - | C+G |
| 0x1F11 | LEAGUE_BIG_BOSS_DONATE_REQUEST | C2S | 5B (pack) | u16@0x0 u8@0x7 u8@0x8 u8@0x9 | C+P |
| 0x1F12 | LEAGUE_BIG_BOSS_DONATE_RETURN | S2C | 0B (get) | - | C+G |
| 0x1F13 | LEAGUE_BIG_BOSS_POINT_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x1F14 | LEAGUE_BIG_BOSS_POINT_RETURN | S2C | 0B (get) | - | C+G |
| 0x1F17 | LEAGUE_BIG_BOSS_SET_BATTLE_TIME_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x1F18 | LEAGUE_BIG_BOSS_SET_BATTLE_TIME_RETURN | S2C | 0B (get) | - | C+G |
| 0x1F19 | SYNC_LEAGUE_BIG_BOSS_INFO | S2C | 0B (get) | - | C+G |
| 0x1F1A | SYNC_LEAGUE_BIG_BOSS_REWARD_TIMES | S2C | 0B (get) | - | C+G |
| 0x1F1B | LEAGUE_BIG_BOSS_EMPTYPOS_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x1F1C | LEAGUE_BIG_BOSS_EMPTYPOS_RETURN | S2C | 0B (get) | - | C+G |

### System Flow

### Bot-Useful Findings

- **Auto-donate**: 0x1F0F CMSG_LEAGUE_BIG_BOSS_DONATE_POINT_REQUEST (2B payload)
- **Auto-donate**: 0x1F11 CMSG_LEAGUE_BIG_BOSS_DONATE_REQUEST (5B payload)
- **Reward collection**: 0x1F1A CMSG_SYNC_LEAGUE_BIG_BOSS_REWARD_TIMES

### Vulnerability Notes

- All C2S opcodes have matching server responses (well-validated)
- **1 SET operations** - potential for privilege escalation:
  - 0x1F17 CMSG_LEAGUE_BIG_BOSS_SET_BATTLE_TIME_REQUEST

---

## KING_CHESS - King Chess / Kingdom Clash board game

### Opcode Table

| Opcode | Name | Dir | Payload | Fields | Symbol Found |
|--------|------|-----|---------|--------|--------------|
| 0x0A29 | KING_CHESS_SIGNUP_RETURN | S2C | 0B (get) | - | C+G |
| 0x0A2B | SYNC_KING_CHESS_ACTION | BIDI | 2B (pack) | u16@0x0 | C+P+G |
| 0x0A2C | KING_CHESS_ACTION_DETAIL_INFO_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0A2D | KING_CHESS_ACTION_DETAIL_INFO_RETURN | S2C | 0B (get) | - | C+G |
| 0x0A2E | KING_CHESS_RANK_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0A2F | KING_CHESS_RANK_RETURN | S2C | 0B (get) | - | C+G |
| 0x0A30 | KING_CHESS_ENABLE_VIEW | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x0A33 | KING_CHESS_OCCUPY_INFO_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0A34 | KING_CHESS_OCCUPY_INFO_RETURN | S2C | 0B (get) | - | C+G |
| 0x0A36 | KING_CHESS_SET_LOOK_CHAT | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x0A37 | KING_CHESS_SYNC_ALL_LEAGUE_INFO | S2C | 0B (get) | - | C+G |
| 0x0A3D | SYNC_LEAGUE_KING_CHESS_DEL | S2C | 0B (get) | - | C+G |
| 0x0A3E | SYNC_LEAGUE_KING_CHESS_ADD | S2C | 0B (get) | - | C+G |
| 0x0A41 | SYNC_DEFEND_INFO_KING_CHESS | S2C | 0B (get) | - | C+G |
| 0x0A49 | KING_CHESS_USER_VALUE_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0A4A | KING_CHESS_USER_VALUE_RETURN | S2C | 0B (get) | - | C+G |
| 0x0A4B | KING_CHESS_SELF_INFO_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P F&F |
| 0x0A4C | KING_CHESS_ALL_LEAGUE_INFO_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P F&F |

### System Flow

**Entry Sequence:**
1. Send 0x0A30 (CMSG_KING_CHESS_ENABLE_VIEW) - Open view

### Bot-Useful Findings

- **Automatable**: 0x0A49 CMSG_KING_CHESS_USER_VALUE_REQUEST (2B payload)

### Vulnerability Notes

- **4 fire-and-forget opcodes** - can be sent without waiting for response
  - 0x0A30 CMSG_KING_CHESS_ENABLE_VIEW
  - 0x0A36 CMSG_KING_CHESS_SET_LOOK_CHAT
  - 0x0A4B CMSG_KING_CHESS_SELF_INFO_REQUEST
  - 0x0A4C CMSG_KING_CHESS_ALL_LEAGUE_INFO_REQUEST
- **2 REQUEST opcodes without matching RETURN** - server may not validate:
  - 0x0A4B CMSG_KING_CHESS_SELF_INFO_REQUEST
  - 0x0A4C CMSG_KING_CHESS_ALL_LEAGUE_INFO_REQUEST
- **1 SET operations** - potential for privilege escalation:
  - 0x0A36 CMSG_KING_CHESS_SET_LOOK_CHAT

---

## KING_ROAD - King's Road quests

### Opcode Table

| Opcode | Name | Dir | Payload | Fields | Symbol Found |
|--------|------|-----|---------|--------|--------------|
| 0x0992 | SYNC_KING_ROAD_QUEST_INFO | S2C | 0B (get) | - | C+G |
| 0x0993 | KING_ROAD_REWARD_REQUEST | C2S | 2B (pack) | u16@0x0 | C+P |
| 0x0994 | KING_ROAD_REWARD_RETURN | S2C | 0B (get) | - | C+G |
| 0x0995 | SYNC_KING_ROAD_ONE_QUEST_INFO | S2C | 0B (get) | - | C+G |

### System Flow

### Bot-Useful Findings

- **Reward collection**: 0x0993 CMSG_KING_ROAD_REWARD_REQUEST (2B payload)

### Vulnerability Notes

- All C2S opcodes have matching server responses (well-validated)

---

## Detailed Payload Formats

Opcodes where packData was found and disassembled:

### 0x01ED CMSG_LEAGUE_DONATE (LEAGUE_TECH_DONATE_SHOP)
- Symbol: `_ZN33CMSG_LEAGUE_DONATE_REWARD_REQUEST8packDataER8CIStream`
- Address: 0x05178F64, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x02A8 CMSG_LEAGUE_BOARD_REQUEST (LEAGUE_BOARD)
- Symbol: `_ZN25CMSG_LEAGUE_BOARD_REQUEST8packDataER8CIStream`
- Address: 0x04FC6BF4, Size: 320
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x02AA CMSG_LEAGUE_BOARD_LEAVE_WORD (LEAGUE_BOARD)
- Symbol: `_ZN28CMSG_LEAGUE_BOARD_LEAVE_WORD8packDataER8CIStream`
- Address: 0x04FC7E1C, Size: 624
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x02DA CMSG_LEAGUE_LATEST_REQUEST (LEAGUE_LATEST)
- Symbol: `_ZN26CMSG_LEAGUE_LATEST_REQUEST8packDataER8CIStream`
- Address: 0x0504358C, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0F3C CMSG_LEAGUE_STATUS_REQUEST (LEAGUE_STATUS)
- Symbol: `_ZN26CMSG_LEAGUE_STATUS_REQUEST8packDataER8CIStream`
- Address: 0x0517A418, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x07E5 CMSG_ENTER_LEAGUE_BATTLEFIELD_VIEW (LEAGUE_BATTLEFIELD)
- Symbol: `_ZN34CMSG_ENTER_LEAGUE_BATTLEFIELD_VIEW8packDataER8CIStream`
- Address: 0x051100C8, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x07E7 CMSG_QUERY_LEAGUE_BATTLEFIELD_ACTION (LEAGUE_BATTLEFIELD)
- Symbol: `_ZN36CMSG_QUERY_LEAGUE_BATTLEFIELD_ACTION8packDataER8CIStream`
- Address: 0x051124B0, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x07EB CMSG_LEAGUE_BATTLEFIELD_RANK_VIEW_REQUEST (LEAGUE_BATTLEFIELD)
- Symbol: `_ZN41CMSG_LEAGUE_BATTLEFIELD_RANK_VIEW_REQUEST8packDataER8CIStream`
- Address: 0x05110DB8, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x07ED CMSG_LEAGUE_BATTLEFIELD_REWARD_CONFIG_REQUEST (LEAGUE_BATTLEFIELD)
- Symbol: `_ZN45CMSG_LEAGUE_BATTLEFIELD_REWARD_CONFIG_REQUEST8packDataER8CIStream`
- Address: 0x05112950, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x07EF CMSG_LEAGUE_BATTLEFIELD_GET_REWARD_REQUEST (LEAGUE_BATTLEFIELD)
- Symbol: `_ZN42CMSG_LEAGUE_BATTLEFIELD_GET_REWARD_REQUEST8packDataER8CIStream`
- Address: 0x05113120, Size: 376
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x07F1 CMSG_ENTER_LEAGUE_BATTLEFIELD_REQUEST (LEAGUE_BATTLEFIELD)
- Symbol: `_ZN37CMSG_ENTER_LEAGUE_BATTLEFIELD_REQUEST8packDataER8CIStream`
- Address: 0x05111740, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x07F2 CMSG_EXIT_LEAGUE_BATTLEFIELD_REQUEST (LEAGUE_BATTLEFIELD)
- Symbol: `_ZN36CMSG_EXIT_LEAGUE_BATTLEFIELD_REQUEST8packDataER8CIStream`
- Address: 0x05111838, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x07F5 CMSG_LEAGUE_BATTLEFIELD_POINT_VIEW_REQUEST (LEAGUE_BATTLEFIELD)
- Symbol: `_ZN42CMSG_LEAGUE_BATTLEFIELD_POINT_VIEW_REQUEST8packDataER8CIStream`
- Address: 0x05113558, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1AC3 CMSG_DAMAGE_GIFT_INFO (DAMAGE_HELP)
- Symbol: `_ZN21CMSG_DAMAGE_GIFT_INFO8packDataER8CIStream`
- Address: 0x05027FB8, Size: 812
- Total payload: 2 bytes
- Direction: C2S?

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1AC5 CMSG_DAMAGE_HELP (DAMAGE_HELP)
- Symbol: `_ZN16CMSG_DAMAGE_HELP8packDataER8CIStream`
- Address: 0x05028D14, Size: 860
- Total payload: 2 bytes
- Direction: C2S?

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1AC7 CMSG_DAMAGE_BUY (DAMAGE_HELP)
- Symbol: `_ZN20CMSG_DAMAGE_BUY_ITEM8packDataER8CIStream`
- Address: 0x050298D4, Size: 760
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1AC9 CMSG_DAMAGE_BUY_ITEM (DAMAGE_HELP)
- Symbol: `_ZN20CMSG_DAMAGE_BUY_ITEM8packDataER8CIStream`
- Address: 0x050298D4, Size: 760
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1ACB CMSG_DAMAGE_SHARE (DAMAGE_HELP)
- Symbol: `_ZN17CMSG_DAMAGE_SHARE8packDataER8CIStream`
- Address: 0x05029E24, Size: 668
- Total payload: 5 bytes
- Direction: C2S?

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |
| 2 | 1 | u8 | 0x07 |
| 3 | 1 | u8 | 0x08 |
| 4 | 1 | u8 | 0x09 |

### 0x0245 CMSG_QUERY_DOMINION_INFO (DOMINION)
- Symbol: `_ZN24CMSG_QUERY_DOMINION_INFO8packDataER8CIStream`
- Address: 0x05045744, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0246 CMSG_QUERY_DOMINION_SIMPLE_BATTLE_INFO (DOMINION)
- Symbol: `_ZN38CMSG_QUERY_DOMINION_SIMPLE_BATTLE_INFO8packDataER8CIStream`
- Address: 0x0504596C, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0258 CMSG_QUERY_DOMINION_OFFICIAL_INFO (DOMINION)
- Symbol: `_ZN33CMSG_QUERY_DOMINION_OFFICIAL_INFO8packDataER8CIStream`
- Address: 0x05045A9C, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x025A CMSG_SET_DOMINION_OFFICIAL (DOMINION)
- Symbol: `_ZN26CMSG_SET_DOMINION_OFFICIAL8packDataER8CIStream`
- Address: 0x050461BC, Size: 324
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0260 CMSG_QUERY_DOMINION_DEFEND_NUM_REQUEST (DOMINION)
- Symbol: `_ZN38CMSG_QUERY_DOMINION_DEFEND_NUM_REQUEST8packDataER8CIStream`
- Address: 0x05044698, Size: 392
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x02F8 CMSG_DOMINION_LATEST_REQUEST (DOMINION)
- Symbol: `_ZN28CMSG_DOMINION_LATEST_REQUEST8packDataER8CIStream`
- Address: 0x05043C80, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0604 CMSG_QUERY_DOMINION_ACTION_INTEGRAL_REQUEST (DOMINION_ACTION_KING)
- Symbol: `_ZN43CMSG_QUERY_DOMINION_ACTION_INTEGRAL_REQUEST8packDataER8CIStream`
- Address: 0x0503C1A0, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0606 CMSG_QUERY_DOMINION_ACTION_HISTORY_REQUEST (DOMINION_ACTION_KING)
- Symbol: `_ZN42CMSG_QUERY_DOMINION_ACTION_HISTORY_REQUEST8packDataER8CIStream`
- Address: 0x0503CA7C, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0608 CMSG_QUERY_KING_INFO_REQUEST (DOMINION_ACTION_KING)
- Symbol: `_ZN28CMSG_QUERY_KING_INFO_REQUEST8packDataER8CIStream`
- Address: 0x0503D364, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x060E CMSG_KING_REWARD_INFO_REQUEST (DOMINION_ACTION_KING)
- Symbol: `_ZN29CMSG_KING_REWARD_INFO_REQUEST8packDataER8CIStream`
- Address: 0x0503E654, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0610 CMSG_BESTOW_KING_REWARD_REQUEST (DOMINION_ACTION_KING)
- Symbol: `_ZN31CMSG_BESTOW_KING_REWARD_REQUEST8packDataER8CIStream`
- Address: 0x0503F21C, Size: 272
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0612 CMSG_QUERY_SERVER_DOMINION_ACTION_INTEGRAL_REQUEST (DOMINION_ACTION_KING)
- Symbol: `_ZN50CMSG_QUERY_SERVER_DOMINION_ACTION_INTEGRAL_REQUEST8packDataER8CIStream`
- Address: 0x0503F750, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0614 CMSG_QUERY_SERVER_DOMINION_ACTION_HISTORY_REQUEST (DOMINION_ACTION_KING)
- Symbol: `_ZN49CMSG_QUERY_SERVER_DOMINION_ACTION_HISTORY_REQUEST8packDataER8CIStream`
- Address: 0x050408E4, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0616 CMSG_QUERY_SERVER_KING_INFO_REQUEST (DOMINION_ACTION_KING)
- Symbol: `_ZN35CMSG_QUERY_SERVER_KING_INFO_REQUEST8packDataER8CIStream`
- Address: 0x05041204, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x083E CMSG_QUERY_WORLD_BATTLE_ACTION_CONFIG (WORLD_BATTLE)
- Symbol: `_ZN37CMSG_QUERY_WORLD_BATTLE_ACTION_CONFIG8packDataER8CIStream`
- Address: 0x052F62E4, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0840 CMSG_WORLD_BATTLE_ACTION_REQUEST (WORLD_BATTLE)
- Symbol: `_ZN32CMSG_WORLD_BATTLE_ACTION_REQUEST8packDataER8CIStream`
- Address: 0x052F6810, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0842 CMSG_WORLD_BATTLE_ACTION_DETAIL_REQUEST (WORLD_BATTLE)
- Symbol: `_ZN39CMSG_WORLD_BATTLE_ACTION_DETAIL_REQUEST8packDataER8CIStream`
- Address: 0x052F7280, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0846 CMSG_WORLD_BATTLE_PLAYER_RANK_REQUEST (WORLD_BATTLE)
- Symbol: `_ZN37CMSG_WORLD_BATTLE_PLAYER_RANK_REQUEST8packDataER8CIStream`
- Address: 0x052FBFFC, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0848 CMSG_WORLD_BATTLE_GROUP_RANK_REQUEST (WORLD_BATTLE)
- Symbol: `_ZN36CMSG_WORLD_BATTLE_GROUP_RANK_REQUEST8packDataER8CIStream`
- Address: 0x052FC9C0, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x084A CMSG_WORLD_BATTLE_OVERLORD_RECORD_REQUEST (WORLD_BATTLE)
- Symbol: `_ZN41CMSG_WORLD_BATTLE_OVERLORD_RECORD_REQUEST8packDataER8CIStream`
- Address: 0x052FD340, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x084C CMSG_WORLD_BATTLE_ENTER_REQUEST (WORLD_BATTLE)
- Symbol: `_ZN31CMSG_WORLD_BATTLE_ENTER_REQUEST8packDataER8CIStream`
- Address: 0x052FEB2C, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x084D CMSG_WORLD_BATTLE_EXIT_REQUEST (WORLD_BATTLE)
- Symbol: `_ZN30CMSG_WORLD_BATTLE_EXIT_REQUEST8packDataER8CIStream`
- Address: 0x052FEC24, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x084F CMSG_WORLD_BATTLE_SERVER_OFFICIAL_REQUEST (WORLD_BATTLE)
- Symbol: `_ZN41CMSG_WORLD_BATTLE_SERVER_OFFICIAL_REQUEST8packDataER8CIStream`
- Address: 0x052FF398, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0851 CMSG_WORLD_BATTLE_PLAYER_OFFICIAL_REQUEST (WORLD_BATTLE)
- Symbol: `_ZN41CMSG_WORLD_BATTLE_PLAYER_OFFICIAL_REQUEST8packDataER8CIStream`
- Address: 0x052FFAEC, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0853 CMSG_WORLD_BATTLE_SET_SERVER_OFFICIAL_REQUEST (WORLD_BATTLE)
- Symbol: `_ZN45CMSG_WORLD_BATTLE_SET_SERVER_OFFICIAL_REQUEST8packDataER8CIStream`
- Address: 0x05300324, Size: 544
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0855 CMSG_WORLD_BATTLE_SET_PLAYER_OFFICIAL_REQUEST (WORLD_BATTLE)
- Symbol: `_ZN45CMSG_WORLD_BATTLE_SET_PLAYER_OFFICIAL_REQUEST8packDataER8CIStream`
- Address: 0x05300B1C, Size: 684
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x085B CMSG_WORLD_BATTLE_ENTER_VIEW_REQUEST (WORLD_BATTLE)
- Symbol: `_ZN36CMSG_WORLD_BATTLE_ENTER_VIEW_REQUEST8packDataER8CIStream`
- Address: 0x052FF170, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x085F CMSG_WORLD_BATTLE_DOMINION_RECORD_REQUEST (WORLD_BATTLE)
- Symbol: `_ZN41CMSG_WORLD_BATTLE_DOMINION_RECORD_REQUEST8packDataER8CIStream`
- Address: 0x053017AC, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0CF0 CMSG_WORLD_BATTLE_NEW_SIGN_UP_REQUEST_NEW (WORLD_BATTLE)
- Symbol: `_ZN41CMSG_WORLD_BATTLE_NEW_SIGN_UP_REQUEST_NEW8packDataER8CIStream`
- Address: 0x052FA1C8, Size: 492
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0962 CMSG_WORLD_BATTLE_GROUP_INFO_REQUEST (WORLD_BATTLE_GROUPS)
- Symbol: `_ZN36CMSG_WORLD_BATTLE_GROUP_INFO_REQUEST8packDataER8CIStream`
- Address: 0x052F8938, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0964 CMSG_WORLD_BATTLE_GROUP_MEMBER_REQUEST (WORLD_BATTLE_GROUPS)
- Symbol: `_ZN38CMSG_WORLD_BATTLE_GROUP_MEMBER_REQUEST8packDataER8CIStream`
- Address: 0x052F7E40, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0966 CMSG_WORLD_BATTLE_JOIN_GROUP_REQUEST (WORLD_BATTLE_GROUPS)
- Symbol: `_ZN36CMSG_WORLD_BATTLE_JOIN_GROUP_REQUEST8packDataER8CIStream`
- Address: 0x052FAC20, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0968 CMSG_WORLD_BATTLE_SET_POWER_REQUEST (WORLD_BATTLE_GROUPS)
- Symbol: `_ZN35CMSG_WORLD_BATTLE_SET_POWER_REQUEST8packDataER8CIStream`
- Address: 0x052FB52C, Size: 324
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x096A CMSG_WORLD_BATTLE_KICK_MEMBER_REQUEST (WORLD_BATTLE_GROUPS)
- Symbol: `_ZN37CMSG_WORLD_BATTLE_KICK_MEMBER_REQUEST8packDataER8CIStream`
- Address: 0x052FB8F4, Size: 272
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x096D CMSG_WORLD_BATTLEFIELD_SELF_GROUP_REQUEST (WORLD_BATTLE_GROUPS)
- Symbol: `_ZN41CMSG_WORLD_BATTLEFIELD_SELF_GROUP_REQUEST8packDataER8CIStream`
- Address: 0x052F95A4, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x096F CMSG_WORLD_BATTLE_LEAVE_GROUP_REQUEST (WORLD_BATTLE_GROUPS)
- Symbol: `_ZN37CMSG_WORLD_BATTLE_LEAVE_GROUP_REQUEST8packDataER8CIStream`
- Address: 0x052F9E24, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0F0B CMSG_ENTER_FORTRESS_VIEW (FORTRESS)
- Symbol: `_ZN24CMSG_ENTER_FORTRESS_VIEW8packDataER8CIStream`
- Address: 0x050686DC, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0F0D CMSG_QUERY_FORTRESS_ACTION (FORTRESS)
- Symbol: `_ZN26CMSG_QUERY_FORTRESS_ACTION8packDataER8CIStream`
- Address: 0x0506C738, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0F0F CMSG_FORTRESS_SIGNUP_REQUEST (FORTRESS)
- Symbol: `_ZN28CMSG_FORTRESS_SIGNUP_REQUEST8packDataER8CIStream`
- Address: 0x05069184, Size: 268
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0F11 CMSG_FORTRESS_RANK_VIEW_REQUEST (FORTRESS)
- Symbol: `_ZN31CMSG_FORTRESS_RANK_VIEW_REQUEST8packDataER8CIStream`
- Address: 0x05069424, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0F13 CMSG_ENTER_FORTRESS_REQUEST (FORTRESS)
- Symbol: `_ZN27CMSG_ENTER_FORTRESS_REQUEST8packDataER8CIStream`
- Address: 0x0506BAC0, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0F14 CMSG_EXIT_FORTRESS_REQUEST (FORTRESS)
- Symbol: `_ZN26CMSG_EXIT_FORTRESS_REQUEST8packDataER8CIStream`
- Address: 0x0506BBB8, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0F1C CMSG_FORTRESS_LEVEL_RANK_VIEW_REQUEST (FORTRESS)
- Symbol: `_ZN37CMSG_FORTRESS_LEVEL_RANK_VIEW_REQUEST8packDataER8CIStream`
- Address: 0x0506A5E8, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0F1E CMSG_FORTRESS_LEVEL_USER_RANK_VIEW_REQUEST (FORTRESS)
- Symbol: `_ZN42CMSG_FORTRESS_LEVEL_USER_RANK_VIEW_REQUEST8packDataER8CIStream`
- Address: 0x0506B054, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0F20 CMSG_FORTRESS_DISTRIBUTE_REWARD_INFO_REQUEST (FORTRESS)
- Symbol: `_ZN44CMSG_FORTRESS_DISTRIBUTE_REWARD_INFO_REQUEST8packDataER8CIStream`
- Address: 0x0506E580, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0F22 CMSG_BESTOW_FORTRESS_REWARD_REQUEST (FORTRESS)
- Symbol: `_ZN35CMSG_BESTOW_FORTRESS_REWARD_REQUEST8packDataER8CIStream`
- Address: 0x0506F6BC, Size: 272
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0F24 CMSG_FORTRESS_USER_VALUE_REQUEST (FORTRESS)
- Symbol: `_ZN32CMSG_FORTRESS_USER_VALUE_REQUEST8packDataER8CIStream`
- Address: 0x05069DAC, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15AE CMSG_QUERY_LOSTLAND_ACTION_CONFIG (LOSTLAND)
- Symbol: `_ZN33CMSG_QUERY_LOSTLAND_ACTION_CONFIG8packDataER8CIStream`
- Address: 0x051A6EE0, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15B1 CMSG_ENTER_LOSTLAND_VIEW (LOSTLAND)
- Symbol: `_ZN24CMSG_ENTER_LOSTLAND_VIEW8packDataER8CIStream`
- Address: 0x051A8814, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15B3 CMSG_LOSTLAND_MAPINFO_REQUEST (LOSTLAND)
- Symbol: `_ZN29CMSG_LOSTLAND_MAPINFO_REQUEST8packDataER8CIStream`
- Address: 0x051A97CC, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15B5 CMSG_ENTER_LOSTLAND_REQUEST (LOSTLAND)
- Symbol: `_ZN27CMSG_ENTER_LOSTLAND_REQUEST8packDataER8CIStream`
- Address: 0x051AB990, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15B6 CMSG_EXIT_LOSTLAND_REQUEST (LOSTLAND)
- Symbol: `_ZN26CMSG_EXIT_LOSTLAND_REQUEST8packDataER8CIStream`
- Address: 0x051ABC44, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15B7 CMSG_LOSTLAND_DONATE_RESOURCE_REQUEST (LOSTLAND)
- Symbol: `_ZN37CMSG_LOSTLAND_DONATE_RESOURCE_REQUEST8packDataER8CIStream`
- Address: 0x051AEC34, Size: 272
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15B9 CMSG_LOSTLAND_DONATE_HEROCHIP_REQUEST (LOSTLAND)
- Symbol: `_ZN37CMSG_LOSTLAND_DONATE_HEROCHIP_REQUEST8packDataER8CIStream`
- Address: 0x051AF1F8, Size: 272
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15BB CMSG_LOSTLAND_SHOP_BUY_REQUEST (LOSTLAND)
- Symbol: `_ZN30CMSG_LOSTLAND_SHOP_BUY_REQUEST8packDataER8CIStream`
- Address: 0x051AF7BC, Size: 272
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15BE CMSG_LOSTLAND_BAN_HERO_REQUEST (LOSTLAND)
- Symbol: `_ZN30CMSG_LOSTLAND_BAN_HERO_REQUEST8packDataER8CIStream`
- Address: 0x051AFE5C, Size: 388
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15C0 CMSG_LOSTLAND_HERO_VOTE_COUNT_REQUEST (LOSTLAND)
- Symbol: `_ZN37CMSG_LOSTLAND_HERO_VOTE_COUNT_REQUEST8packDataER8CIStream`
- Address: 0x051B04EC, Size: 216
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15C2 CMSG_LOSTLAND_CAMP_RANK_REQUEST (LOSTLAND)
- Symbol: `_ZN31CMSG_LOSTLAND_CAMP_RANK_REQUEST8packDataER8CIStream`
- Address: 0x051B0ACC, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15C4 CMSG_LOSTLAND_LEAGUE_RANK_REQUEST (LOSTLAND)
- Symbol: `_ZN33CMSG_LOSTLAND_LEAGUE_RANK_REQUEST8packDataER8CIStream`
- Address: 0x051B1568, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15C6 CMSG_LOSTLAND_PLAYER_RANK_REQUEST (LOSTLAND)
- Symbol: `_ZN33CMSG_LOSTLAND_PLAYER_RANK_REQUEST8packDataER8CIStream`
- Address: 0x051B2114, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15C8 CMSG_LOSTLAND_DONATE_CD_END (LOSTLAND)
- Symbol: `_ZN27CMSG_LOSTLAND_DONATE_CD_END8packDataER8CIStream`
- Address: 0x051B2B60, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15CA CMSG_LOSTLAND_MARK_REWARD_REQUEST (LOSTLAND)
- Symbol: `_ZN33CMSG_LOSTLAND_MARK_REWARD_REQUEST8packDataER8CIStream`
- Address: 0x051ABD3C, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15CC CMSG_LOSTLAND_HISTORY_REQUEST (LOSTLAND)
- Symbol: `_ZN29CMSG_LOSTLAND_HISTORY_REQUEST8packDataER8CIStream`
- Address: 0x051AD0F8, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15CE CMSG_LOSTLAND_LEAGUE_HISTORY_REQUEST (LOSTLAND)
- Symbol: `_ZN36CMSG_LOSTLAND_LEAGUE_HISTORY_REQUEST8packDataER8CIStream`
- Address: 0x051AD9C4, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15D0 CMSG_LOSTLAND_PLAYER_HISTORY_REQUEST (LOSTLAND)
- Symbol: `_ZN36CMSG_LOSTLAND_PLAYER_HISTORY_REQUEST8packDataER8CIStream`
- Address: 0x051AE2B0, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15D3 CMSG_LOSTLAND_SELF_DOMINION_REQUEST (LOSTLAND)
- Symbol: `_ZN35CMSG_LOSTLAND_SELF_DOMINION_REQUEST8packDataER8CIStream`
- Address: 0x051AA3E8, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15D5 CMSG_LOSTLAND_LEAGUE_BUILD_REQUEST (LOSTLAND)
- Symbol: `_ZN34CMSG_LOSTLAND_LEAGUE_BUILD_REQUEST8packDataER8CIStream`
- Address: 0x051AAD68, Size: 596
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15D9 CMSG_LOSTLAND_ACHIEVEMENT_LIST_REQUEST (LOSTLAND)
- Symbol: `_ZN38CMSG_LOSTLAND_ACHIEVEMENT_LIST_REQUEST8packDataER8CIStream`
- Address: 0x051B33D4, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15DC CMSG_LOSTLAND_ACHIEVEMENT_REQUEST (LOSTLAND)
- Symbol: `_ZN33CMSG_LOSTLAND_ACHIEVEMENT_REQUEST8packDataER8CIStream`
- Address: 0x051B403C, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15DE CMSG_LOSTLAND_ACHIEVEMENT_REWARD_REQUEST (LOSTLAND)
- Symbol: `_ZN40CMSG_LOSTLAND_ACHIEVEMENT_REWARD_REQUEST8packDataER8CIStream`
- Address: 0x051B4B9C, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15E0 CMSG_LEAGUE_BUILDING_OPERAT_REQUEST (LOSTLAND_BUILDINGS)
- Symbol: `_ZN35CMSG_LEAGUE_BUILDING_OPERAT_REQUEST8packDataER8CIStream`
- Address: 0x05156C84, Size: 424
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15E4 CMSG_LEAGUE_BUILDING_DETAIL_REQUEST (LOSTLAND_BUILDINGS)
- Symbol: `_ZN35CMSG_LEAGUE_BUILDING_DETAIL_REQUEST8packDataER8CIStream`
- Address: 0x05158BFC, Size: 596
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15EA CMSG_QUERY_LEAGUEBUILD_DEFEND_INFO (LOSTLAND_BUILDINGS)
- Symbol: `_ZN34CMSG_QUERY_LEAGUEBUILD_DEFEND_INFO8packDataER8CIStream`
- Address: 0x0515BEF8, Size: 596
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15EC CMSG_KICK_LEAGUE_BUILD_DEFEND_ARMY (LOSTLAND_BUILDINGS)
- Symbol: `_ZN34CMSG_KICK_LEAGUE_BUILD_DEFEND_ARMY8packDataER8CIStream`
- Address: 0x0515D1E0, Size: 648
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15F1 CMSG_LOSTLAND_LEAGUE_LATEST_REQUEST (LOSTLAND_BUILDINGS)
- Symbol: `_ZN35CMSG_LOSTLAND_LEAGUE_LATEST_REQUEST8packDataER8CIStream`
- Address: 0x051B4E00, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15FA CMSG_LOSTLAND_BUILDING_INDEX_OPEN_REQUEST (LOSTLAND_BUILDINGS)
- Symbol: `_ZN41CMSG_LOSTLAND_BUILDING_INDEX_OPEN_REQUEST8packDataER8CIStream`
- Address: 0x051B65D8, Size: 428
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x15FF CMSG_LOSTLAND_MONTH_CARD_REWARD_REQUEST (LOSTLAND_BUILDINGS)
- Symbol: `_ZN39CMSG_LOSTLAND_MONTH_CARD_REWARD_REQUEST8packDataER8CIStream`
- Address: 0x051A6AEC, Size: 600
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1FAB CMSG_QUERY_LOSTLAND_RUSH_EVENT (LOSTLAND_RUSH_EVENT)
- Symbol: `_ZN30CMSG_QUERY_LOSTLAND_RUSH_EVENT8packDataER8CIStream`
- Address: 0x04FA3FEC, Size: 668
- Total payload: 5 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |
| 2 | 1 | u8 | 0x07 |
| 3 | 1 | u8 | 0x08 |
| 4 | 1 | u8 | 0x09 |

### 0x1FAD CMSG_LOSTLAND_RUSH_EVENT_REWARD_REQUEST (LOSTLAND_RUSH_EVENT)
- Symbol: `_ZN39CMSG_LOSTLAND_RUSH_EVENT_REWARD_REQUEST8packDataER8CIStream`
- Address: 0x04FA4734, Size: 708
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1FAF CMSG_LOSTLAND_RUSH_EVENT_RANK_REQUEST (LOSTLAND_RUSH_EVENT)
- Symbol: `_ZN37CMSG_LOSTLAND_RUSH_EVENT_RANK_REQUEST8packDataER8CIStream`
- Address: 0x04FA4C3C, Size: 668
- Total payload: 5 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |
| 2 | 1 | u8 | 0x07 |
| 3 | 1 | u8 | 0x08 |
| 4 | 1 | u8 | 0x09 |

### 0x0C4F CMSG_LEGION_ACTION_REQUEST (LEGION)
- Symbol: `_ZN26CMSG_LEGION_ACTION_REQUEST8packDataER8CIStream`
- Address: 0x05114770, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0C51 CMSG_LEGION_CREATE_REQUEST (LEGION)
- Symbol: `_ZN26CMSG_LEGION_CREATE_REQUEST8packDataER8CIStream`
- Address: 0x05115634, Size: 376
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0C53 CMSG_LEGION_LIST_REQUEST (LEGION)
- Symbol: `_ZN24CMSG_LEGION_LIST_REQUEST8packDataER8CIStream`
- Address: 0x05116198, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0C55 CMSG_LEGION_INFO_REQUEST (LEGION)
- Symbol: `_ZN24CMSG_LEGION_INFO_REQUEST8packDataER8CIStream`
- Address: 0x0511690C, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0C57 CMSG_LEGION_JOIN_REQUEST (LEGION)
- Symbol: `_ZN24CMSG_LEGION_JOIN_REQUEST8packDataER8CIStream`
- Address: 0x051174A0, Size: 444
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0C59 CMSG_KICK_LEGION_MEMBER (LEGION)
- Symbol: `_ZN23CMSG_KICK_LEGION_MEMBER8packDataER8CIStream`
- Address: 0x05118240, Size: 272
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0C5C CMSG_LEGION_ADD_MEMBER_LIST_REQUEST (LEGION)
- Symbol: `_ZN35CMSG_LEGION_ADD_MEMBER_LIST_REQUEST8packDataER8CIStream`
- Address: 0x05118A24, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0C5E CMSG_CHANGE_LEGION_POSTION (LEGION)
- Symbol: `_ZN26CMSG_CHANGE_LEGION_POSTION8packDataER8CIStream`
- Address: 0x0511913C, Size: 376
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0C60 CMSG_CHANGE_LEGION_CHANGE_NAME_REQUEST (LEGION)
- Symbol: `_ZN38CMSG_CHANGE_LEGION_CHANGE_NAME_REQUEST8packDataER8CIStream`
- Address: 0x05119894, Size: 428
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0C63 CMSG_LEGION_RANK_REQUEST (LEGION)
- Symbol: `_ZN24CMSG_LEGION_RANK_REQUEST8packDataER8CIStream`
- Address: 0x0511A1DC, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0C65 CMSG_LEGION_SET_TALENT_REQUEST (LEGION)
- Symbol: `_ZN30CMSG_LEGION_SET_TALENT_REQUEST8packDataER8CIStream`
- Address: 0x0511ABB4, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0C67 CMSG_LEGION_CHANGE_POS_TIMES_REQUEST (LEGION)
- Symbol: `_ZN36CMSG_LEGION_CHANGE_POS_TIMES_REQUEST8packDataER8CIStream`
- Address: 0x0511AE58, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0C6E CMSG_LEGION_LATEST_REQUEST (LEGION)
- Symbol: `_ZN26CMSG_LEGION_LATEST_REQUEST8packDataER8CIStream`
- Address: 0x0511C9A0, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0C70 CMSG_LEGION_SELF_JOIN_REQUEST (LEGION)
- Symbol: `_ZN29CMSG_LEGION_SELF_JOIN_REQUEST8packDataER8CIStream`
- Address: 0x0511D094, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0C72 CMSG_LEGION_SELF_LEAVE_REQUEST (LEGION)
- Symbol: `_ZN30CMSG_LEGION_SELF_LEAVE_REQUEST8packDataER8CIStream`
- Address: 0x0511DBC8, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0C74 CMSG_LEGION_BATTLE_MAP_INFO_REQUEST (LEGION)
- Symbol: `_ZN35CMSG_LEGION_BATTLE_MAP_INFO_REQUEST8packDataER8CIStream`
- Address: 0x0511DE70, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0C76 CMSG_LEGION_RESOURCE_REQUEST (LEGION)
- Symbol: `_ZN28CMSG_LEGION_RESOURCE_REQUEST8packDataER8CIStream`
- Address: 0x0511E3DC, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0C78 CMSG_LEGION_MEMBER_INFO_REQUEST (LEGION)
- Symbol: `_ZN31CMSG_LEGION_MEMBER_INFO_REQUEST8packDataER8CIStream`
- Address: 0x0511EAE0, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0C7A CMSG_LEGION_ENEMY_POS_REQUEST (LEGION)
- Symbol: `_ZN29CMSG_LEGION_ENEMY_POS_REQUEST8packDataER8CIStream`
- Address: 0x0511F6F0, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0C7C CMSG_LEGION_VALUE_DETAIL_REQUEST (LEGION)
- Symbol: `_ZN32CMSG_LEGION_VALUE_DETAIL_REQUEST8packDataER8CIStream`
- Address: 0x0511FB90, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0E10 CMSG_LEGION_SEASON_ACTION_REQUEST (LEGION_SEASON)
- Symbol: `_ZN33CMSG_LEGION_SEASON_ACTION_REQUEST8packDataER8CIStream`
- Address: 0x05120034, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0E12 CMSG_LEGION_SEASON_ACTION_SELF_SCHEDULE_REQUEST (LEGION_SEASON)
- Symbol: `_ZN47CMSG_LEGION_SEASON_ACTION_SELF_SCHEDULE_REQUEST8packDataER8CIStream`
- Address: 0x051220AC, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0E16 CMSG_LEGION_SEASON_ACTION_GUESS_INFO_REQUEST (LEGION_SEASON)
- Symbol: `_ZN44CMSG_LEGION_SEASON_ACTION_GUESS_INFO_REQUEST8packDataER8CIStream`
- Address: 0x05122F70, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0E18 CMSG_LEGION_SEASON_ACTION_GUESS_BET_REQUEST (LEGION_SEASON)
- Symbol: `_ZN43CMSG_LEGION_SEASON_ACTION_GUESS_BET_REQUEST8packDataER8CIStream`
- Address: 0x05124604, Size: 324
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0E1A CMSG_LEGION_SEASON_ACTION_PLAYOFF_REQUEST (LEGION_SEASON)
- Symbol: `_ZN41CMSG_LEGION_SEASON_ACTION_PLAYOFF_REQUEST8packDataER8CIStream`
- Address: 0x0512557C, Size: 272
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0E1C CMSG_LEGION_SEASON_ACTION_HIS_PLAYER_REQUEST (LEGION_SEASON)
- Symbol: `_ZN44CMSG_LEGION_SEASON_ACTION_HIS_PLAYER_REQUEST8packDataER8CIStream`
- Address: 0x05126014, Size: 324
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0E1E CMSG_LEGION_SEASON_ACTION_HIS_MVP_REQUEST (LEGION_SEASON)
- Symbol: `_ZN41CMSG_LEGION_SEASON_ACTION_HIS_MVP_REQUEST8packDataER8CIStream`
- Address: 0x05126B34, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0E20 CMSG_LEGION_SEASON_ACTION_HIS_BEST_PLAYER_REQUEST (LEGION_SEASON)
- Symbol: `_ZN49CMSG_LEGION_SEASON_ACTION_HIS_BEST_PLAYER_REQUEST8packDataER8CIStream`
- Address: 0x05127508, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0E22 CMSG_LEGION_SEASON_ACTION_LIKE_PLAYER_REQUEST (LEGION_SEASON)
- Symbol: `_ZN45CMSG_LEGION_SEASON_ACTION_LIKE_PLAYER_REQUEST8packDataER8CIStream`
- Address: 0x05127EDC, Size: 272
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0E27 CMSG_LEGION_MEMBER_HIS_INFO_REQUEST (LEGION_SEASON)
- Symbol: `_ZN35CMSG_LEGION_MEMBER_HIS_INFO_REQUEST8packDataER8CIStream`
- Address: 0x05128EFC, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1AF7 CMSG_CLANPK_SIGNUP_REQUEST (CLANPK)
- Symbol: `_ZN26CMSG_CLANPK_SIGNUP_REQUEST8packDataER8CIStream`
- Address: 0x04FEA420, Size: 660
- Total payload: 5 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |
| 2 | 1 | u8 | 0x07 |
| 3 | 1 | u8 | 0x08 |
| 4 | 1 | u8 | 0x09 |

### 0x1AF9 CMSG_ENTER_CLANPK_VIEW (CLANPK)
- Symbol: `_ZN22CMSG_ENTER_CLANPK_VIEW8packDataER8CIStream`
- Address: 0x04FED08C, Size: 600
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1AFB CMSG_CLANPK_BATTLE_RECORD_REQUEST (CLANPK)
- Symbol: `_ZN33CMSG_CLANPK_BATTLE_RECORD_REQUEST8packDataER8CIStream`
- Address: 0x04FED684, Size: 600
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1AFD CMSG_CLANPK_LEVEL_RANK_VIEW_REQUEST (CLANPK)
- Symbol: `_ZN35CMSG_CLANPK_LEVEL_RANK_VIEW_REQUEST8packDataER8CIStream`
- Address: 0x04FF2914, Size: 668
- Total payload: 5 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |
| 2 | 1 | u8 | 0x07 |
| 3 | 1 | u8 | 0x08 |
| 4 | 1 | u8 | 0x09 |

### 0x1AFF CMSG_CLANPK_USER_RANK_VIEW_REQUEST (CLANPK)
- Symbol: `_ZN34CMSG_CLANPK_USER_RANK_VIEW_REQUEST8packDataER8CIStream`
- Address: 0x04FF3660, Size: 660
- Total payload: 5 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |
| 2 | 1 | u8 | 0x07 |
| 3 | 1 | u8 | 0x08 |
| 4 | 1 | u8 | 0x09 |

### 0x1B01 CMSG_ENTER_CLANPK_REQUEST (CLANPK)
- Symbol: `_ZN25CMSG_ENTER_CLANPK_REQUEST8packDataER8CIStream`
- Address: 0x04FF562C, Size: 600
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1B03 CMSG_EXIT_CLANPK_REQUEST (CLANPK)
- Symbol: `_ZN24CMSG_EXIT_CLANPK_REQUEST8packDataER8CIStream`
- Address: 0x04FF6E28, Size: 600
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1B04 CMSG_CLANPK_BUILDING_REQUEST (CLANPK)
- Symbol: `_ZN28CMSG_CLANPK_BUILDING_REQUEST8packDataER8CIStream`
- Address: 0x04FF4940, Size: 600
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1B06 CMSG_CLANPK_BUILD_UPGRADE_REQUEST (CLANPK)
- Symbol: `_ZN33CMSG_CLANPK_BUILD_UPGRADE_REQUEST8packDataER8CIStream`
- Address: 0x04FF8314, Size: 760
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1B08 CMSG_CLANPK_DONATE_REQUEST (CLANPK)
- Symbol: `_ZN26CMSG_CLANPK_DONATE_REQUEST8packDataER8CIStream`
- Address: 0x04FF8930, Size: 756
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1B0A CMSG_CLANPK_SET_DEFEND_HERO_REQUEST (CLANPK)
- Symbol: `_ZN35CMSG_CLANPK_SET_DEFEND_HERO_REQUEST8packDataER8CIStream`
- Address: 0x04FF8F10, Size: 1088
- Total payload: 1 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 1 | u8 | 0x48 |

### 0x1B0C CMSG_CLANPK_SET_ATTACK_HERO_REQUEST (CLANPK)
- Symbol: `_ZN35CMSG_CLANPK_SET_ATTACK_HERO_REQUEST8packDataER8CIStream`
- Address: 0x04FF9DBC, Size: 1088
- Total payload: 1 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 1 | u8 | 0x48 |

### 0x1B0E CMSG_CLANPK_SET_ASSIST_HERO_REQUEST (CLANPK)
- Symbol: `_ZN35CMSG_CLANPK_SET_ASSIST_HERO_REQUEST8packDataER8CIStream`
- Address: 0x04FF0884, Size: 708
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1B10 CMSG_CLANPK_GIVE_ASSIST_HERO_REQUEST (CLANPK)
- Symbol: `_ZN36CMSG_CLANPK_GIVE_ASSIST_HERO_REQUEST8packDataER8CIStream`
- Address: 0x04FF2008, Size: 668
- Total payload: 5 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |
| 2 | 1 | u8 | 0x07 |
| 3 | 1 | u8 | 0x08 |
| 4 | 1 | u8 | 0x09 |

### 0x1B14 CMSG_CLANPK_ASSIST_HERO_REQUEST (CLANPK)
- Symbol: `_ZN31CMSG_CLANPK_ASSIST_HERO_REQUEST8packDataER8CIStream`
- Address: 0x04FEECEC, Size: 600
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1B16 CMSG_CLANPK_QUERY_DEFEND_INFO (CLANPK)
- Symbol: `_ZN29CMSG_CLANPK_QUERY_DEFEND_INFO8packDataER8CIStream`
- Address: 0x04FFB16C, Size: 704
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1B18 CMSG_CLANPK_QUERY_ATTACK_INFO (CLANPK)
- Symbol: `_ZN29CMSG_CLANPK_QUERY_ATTACK_INFO8packDataER8CIStream`
- Address: 0x04FFCD30, Size: 600
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1B1A CMSG_CLANPK_START_ATTACK (CLANPK)
- Symbol: `_ZN24CMSG_CLANPK_START_ATTACK8packDataER8CIStream`
- Address: 0x050027C8, Size: 668
- Total payload: 5 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |
| 2 | 1 | u8 | 0x07 |
| 3 | 1 | u8 | 0x08 |
| 4 | 1 | u8 | 0x09 |

### 0x1B1F CMSG_CLANPK_MAILBOX_MAIL_REQUEST (CLANPK)
- Symbol: `_ZN32CMSG_CLANPK_MAILBOX_MAIL_REQUEST8packDataER8CIStream`
- Address: 0x05003368, Size: 704
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1B20 CMSG_CLANPK_MAILBOX_MAIL (CLANPK)
- Symbol: `_ZN32CMSG_CLANPK_MAILBOX_MAIL_REQUEST8packDataER8CIStream`
- Address: 0x05003368, Size: 704
- Total payload: 2 bytes
- Direction: C2S?

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1B21 CMSG_CLANPK_START_DEFEND (CLANPK)
- Symbol: `_ZN24CMSG_CLANPK_START_DEFEND8packDataER8CIStream`
- Address: 0x05002C9C, Size: 668
- Total payload: 5 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |
| 2 | 1 | u8 | 0x07 |
| 3 | 1 | u8 | 0x08 |
| 4 | 1 | u8 | 0x09 |

### 0x1B2D CMSG_CLANPK_DEFEND_AMRY_REQUEST (CLANPK)
- Symbol: `_ZN31CMSG_CLANPK_DEFEND_AMRY_REQUEST8packDataER8CIStream`
- Address: 0x04FEBA1C, Size: 668
- Total payload: 5 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |
| 2 | 1 | u8 | 0x07 |
| 3 | 1 | u8 | 0x08 |
| 4 | 1 | u8 | 0x09 |

### 0x1B32 CMSG_CLANPK_ACTIVITY_INFO_REQUEST (CLANPK)
- Symbol: `_ZN33CMSG_CLANPK_ACTIVITY_INFO_REQUEST8packDataER8CIStream`
- Address: 0x04FF441C, Size: 600
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1B34 CMSG_CLANPK_CHECK_SET_DEF_REQUEST (CLANPK)
- Symbol: `_ZN33CMSG_CLANPK_CHECK_SET_DEF_REQUEST8packDataER8CIStream`
- Address: 0x04FE5CCC, Size: 600
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1B36 CMSG_CLANPK_FIRST_LEVEL_REWARD_REQUEST (CLANPK)
- Symbol: `_ZN38CMSG_CLANPK_FIRST_LEVEL_REWARD_REQUEST8packDataER8CIStream`
- Address: 0x05004E7C, Size: 668
- Total payload: 5 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |
| 2 | 1 | u8 | 0x07 |
| 3 | 1 | u8 | 0x08 |
| 4 | 1 | u8 | 0x09 |

### 0x1666 CMSG_LEAGUEPASS_ACTION_TASK_INFO_REQUEST (LEAGUEPASS)
- Symbol: `_ZN40CMSG_LEAGUEPASS_ACTION_TASK_INFO_REQUEST8packDataER8CIStream`
- Address: 0x0516B394, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1668 CMSG_LEAGUEPASS_GROUP_RANK_INFO_REQUEST (LEAGUEPASS)
- Symbol: `_ZN39CMSG_LEAGUEPASS_GROUP_RANK_INFO_REQUEST8packDataER8CIStream`
- Address: 0x0516C2D4, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x166A CMSG_LEAGUEPASS_CONTRIBUTE_INFO_REQUEST (LEAGUEPASS)
- Symbol: `_ZN39CMSG_LEAGUEPASS_CONTRIBUTE_INFO_REQUEST8packDataER8CIStream`
- Address: 0x0516D134, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x166C CMSG_LEAGUEPASS_GET_REWARD_REQUEST (LEAGUEPASS)
- Symbol: `_ZN34CMSG_LEAGUEPASS_GET_REWARD_REQUEST8packDataER8CIStream`
- Address: 0x0516DDD0, Size: 264
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x166E CMSG_LEAGUEPASS_FRESH_TASK_REQUEST (LEAGUEPASS)
- Symbol: `_ZN34CMSG_LEAGUEPASS_FRESH_TASK_REQUEST8packDataER8CIStream`
- Address: 0x0516E0F0, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1670 CMSG_LEAGUEPASS_FINISH_TASK_REQUEST (LEAGUEPASS)
- Symbol: `_ZN35CMSG_LEAGUEPASS_FINISH_TASK_REQUEST8packDataER8CIStream`
- Address: 0x0516E6AC, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1F0F CMSG_LEAGUE_BIG_BOSS_DONATE_POINT_REQUEST (LEAGUE_BIG_BOSS)
- Symbol: `_ZN41CMSG_LEAGUE_BIG_BOSS_DONATE_POINT_REQUEST8packDataER8CIStream`
- Address: 0x05152844, Size: 600
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1F11 CMSG_LEAGUE_BIG_BOSS_DONATE_REQUEST (LEAGUE_BIG_BOSS)
- Symbol: `_ZN35CMSG_LEAGUE_BIG_BOSS_DONATE_REQUEST8packDataER8CIStream`
- Address: 0x05152C7C, Size: 668
- Total payload: 5 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |
| 2 | 1 | u8 | 0x07 |
| 3 | 1 | u8 | 0x08 |
| 4 | 1 | u8 | 0x09 |

### 0x1F13 CMSG_LEAGUE_BIG_BOSS_POINT_REQUEST (LEAGUE_BIG_BOSS)
- Symbol: `_ZN34CMSG_LEAGUE_BIG_BOSS_POINT_REQUEST8packDataER8CIStream`
- Address: 0x05153104, Size: 600
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1F17 CMSG_LEAGUE_BIG_BOSS_SET_BATTLE_TIME_REQUEST (LEAGUE_BIG_BOSS)
- Symbol: `_ZN44CMSG_LEAGUE_BIG_BOSS_SET_BATTLE_TIME_REQUEST8packDataER8CIStream`
- Address: 0x05153D04, Size: 700
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x1F1B CMSG_LEAGUE_BIG_BOSS_EMPTYPOS_REQUEST (LEAGUE_BIG_BOSS)
- Symbol: `_ZN37CMSG_LEAGUE_BIG_BOSS_EMPTYPOS_REQUEST8packDataER8CIStream`
- Address: 0x0515460C, Size: 600
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0A2B CMSG_SYNC_KING_CHESS_ACTION (KING_CHESS)
- Symbol: `_ZN27CMSG_SYNC_KING_CHESS_ACTION8packDataER8CIStream`
- Address: 0x050C41C0, Size: 688
- Total payload: 2 bytes
- Direction: BIDI

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0A2C CMSG_KING_CHESS_ACTION_DETAIL_INFO_REQUEST (KING_CHESS)
- Symbol: `_ZN42CMSG_KING_CHESS_ACTION_DETAIL_INFO_REQUEST8packDataER8CIStream`
- Address: 0x050C4554, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0A2E CMSG_KING_CHESS_RANK_REQUEST (KING_CHESS)
- Symbol: `_ZN28CMSG_KING_CHESS_RANK_REQUEST8packDataER8CIStream`
- Address: 0x050C4F9C, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0A30 CMSG_KING_CHESS_ENABLE_VIEW (KING_CHESS)
- Symbol: `_ZN27CMSG_KING_CHESS_ENABLE_VIEW8packDataER8CIStream`
- Address: 0x050C5928, Size: 216
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0A33 CMSG_KING_CHESS_OCCUPY_INFO_REQUEST (KING_CHESS)
- Symbol: `_ZN35CMSG_KING_CHESS_OCCUPY_INFO_REQUEST8packDataER8CIStream`
- Address: 0x050C71E4, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0A36 CMSG_KING_CHESS_SET_LOOK_CHAT (KING_CHESS)
- Symbol: `_ZN29CMSG_KING_CHESS_SET_LOOK_CHAT8packDataER8CIStream`
- Address: 0x050C7FB0, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0A49 CMSG_KING_CHESS_USER_VALUE_REQUEST (KING_CHESS)
- Symbol: `_ZN34CMSG_KING_CHESS_USER_VALUE_REQUEST8packDataER8CIStream`
- Address: 0x050CCEC4, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0A4B CMSG_KING_CHESS_SELF_INFO_REQUEST (KING_CHESS)
- Symbol: `_ZN33CMSG_KING_CHESS_SELF_INFO_REQUEST8packDataER8CIStream`
- Address: 0x050C7868, Size: 216
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0A4C CMSG_KING_CHESS_ALL_LEAGUE_INFO_REQUEST (KING_CHESS)
- Symbol: `_ZN39CMSG_KING_CHESS_ALL_LEAGUE_INFO_REQUEST8packDataER8CIStream`
- Address: 0x050CD794, Size: 180
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

### 0x0993 CMSG_KING_ROAD_REWARD_REQUEST (KING_ROAD)
- Symbol: `_ZN29CMSG_KING_ROAD_REWARD_REQUEST8packDataER8CIStream`
- Address: 0x050DC2C8, Size: 220
- Total payload: 2 bytes
- Direction: C2S

| Offset | Size | Type | Struct Offset |
|--------|------|------|---------------|
| 0 | 2 | u16 | 0x00 |

## Bot Automation Summary

### Priority 1 - Daily Automatable Actions

- 0x01ED CMSG_LEAGUE_DONATE [2B] [F&F] (LEAGUE_TECH_DONATE_SHOP)
- 0x07ED CMSG_LEAGUE_BATTLEFIELD_REWARD_CONFIG_REQUEST [2B] (LEAGUE_BATTLEFIELD)
- 0x07EF CMSG_LEAGUE_BATTLEFIELD_GET_REWARD_REQUEST [2B] (LEAGUE_BATTLEFIELD)
- 0x1AC5 CMSG_DAMAGE_HELP [2B] [F&F] (DAMAGE_HELP)
- 0x1ACD CMSG_DAMAGE_HELP_NOTIFY [F&F] (DAMAGE_HELP)
- 0x060E CMSG_KING_REWARD_INFO_REQUEST [2B] (DOMINION_ACTION_KING)
- 0x0610 CMSG_BESTOW_KING_REWARD_REQUEST [2B] (DOMINION_ACTION_KING)
- 0x0F20 CMSG_FORTRESS_DISTRIBUTE_REWARD_INFO_REQUEST [2B] (FORTRESS)
- 0x0F22 CMSG_BESTOW_FORTRESS_REWARD_REQUEST [2B] (FORTRESS)
- 0x15B7 CMSG_LOSTLAND_DONATE_RESOURCE_REQUEST [2B] (LOSTLAND)
- 0x15B9 CMSG_LOSTLAND_DONATE_HEROCHIP_REQUEST [2B] (LOSTLAND)
- 0x15C8 CMSG_LOSTLAND_DONATE_CD_END [2B] [F&F] (LOSTLAND)
- 0x15C9 CMSG_LOSTLAND_DONATE_INFO [F&F] (LOSTLAND)
- 0x15CA CMSG_LOSTLAND_MARK_REWARD_REQUEST [2B] (LOSTLAND)
- 0x15DE CMSG_LOSTLAND_ACHIEVEMENT_REWARD_REQUEST [2B] (LOSTLAND)
- 0x15FF CMSG_LOSTLAND_MONTH_CARD_REWARD_REQUEST [2B] (LOSTLAND_BUILDINGS)
- 0x1FAD CMSG_LOSTLAND_RUSH_EVENT_REWARD_REQUEST [2B] (LOSTLAND_RUSH_EVENT)
- 0x1B08 CMSG_CLANPK_DONATE_REQUEST [2B] (CLANPK)
- 0x1B36 CMSG_CLANPK_FIRST_LEVEL_REWARD_REQUEST [5B] (CLANPK)
- 0x166C CMSG_LEAGUEPASS_GET_REWARD_REQUEST [2B] (LEAGUEPASS)
- 0x1670 CMSG_LEAGUEPASS_FINISH_TASK_REQUEST [2B] (LEAGUEPASS)
- 0x1F0F CMSG_LEAGUE_BIG_BOSS_DONATE_POINT_REQUEST [2B] (LEAGUE_BIG_BOSS)
- 0x1F11 CMSG_LEAGUE_BIG_BOSS_DONATE_REQUEST [5B] (LEAGUE_BIG_BOSS)
- 0x0993 CMSG_KING_ROAD_REWARD_REQUEST [2B] (KING_ROAD)

### Priority 2 - Signup/Join Actions

- 0x07E5 CMSG_ENTER_LEAGUE_BATTLEFIELD_VIEW [F&F] (LEAGUE_BATTLEFIELD)
- 0x07F1 CMSG_ENTER_LEAGUE_BATTLEFIELD_REQUEST [F&F] (LEAGUE_BATTLEFIELD)
- 0x084C CMSG_WORLD_BATTLE_ENTER_REQUEST [F&F] (WORLD_BATTLE)
- 0x085B CMSG_WORLD_BATTLE_ENTER_VIEW_REQUEST (WORLD_BATTLE)
- 0x0966 CMSG_WORLD_BATTLE_JOIN_GROUP_REQUEST (WORLD_BATTLE_GROUPS)
- 0x0F0B CMSG_ENTER_FORTRESS_VIEW [F&F] (FORTRESS)
- 0x0F0F CMSG_FORTRESS_SIGNUP_REQUEST (FORTRESS)
- 0x0F13 CMSG_ENTER_FORTRESS_REQUEST [F&F] (FORTRESS)
- 0x15B1 CMSG_ENTER_LOSTLAND_VIEW [F&F] (LOSTLAND)
- 0x15B5 CMSG_ENTER_LOSTLAND_REQUEST [F&F] (LOSTLAND)
- 0x0C51 CMSG_LEGION_CREATE_REQUEST (LEGION)
- 0x0C57 CMSG_LEGION_JOIN_REQUEST (LEGION)
- 0x0C5A CMSG_NOTIFY_LEGION_MEMBER_JOIN (LEGION)
- 0x0C70 CMSG_LEGION_SELF_JOIN_REQUEST (LEGION)
- 0x1AF7 CMSG_CLANPK_SIGNUP_REQUEST (CLANPK)
- 0x1AF9 CMSG_ENTER_CLANPK_VIEW [F&F] (CLANPK)
- 0x1B01 CMSG_ENTER_CLANPK_REQUEST (CLANPK)

### Priority 3 - Info/Query (safe, read-only)

- 66 read-only query/info opcodes across all systems

### Fire-and-Forget Exploit Candidates

These opcodes can be sent rapidly without waiting for server response:

| Opcode | Name | System | Payload |
|--------|------|--------|---------|
| 0x01EC | CMSG_LEAGUE_TECH_UP | LEAGUE_TECH_DONATE_SHOP | ? |
| 0x01ED | CMSG_LEAGUE_DONATE | LEAGUE_TECH_DONATE_SHOP | 2B |
| 0x01FE | CMSG_LEAGUE_SHOP_BUY | LEAGUE_TECH_DONATE_SHOP | ? |
| 0x02AA | CMSG_LEAGUE_BOARD_LEAVE_WORD | LEAGUE_BOARD | 2B |
| 0x07E5 | CMSG_ENTER_LEAGUE_BATTLEFIELD_VIEW | LEAGUE_BATTLEFIELD | 2B |
| 0x07E7 | CMSG_QUERY_LEAGUE_BATTLEFIELD_ACTION | LEAGUE_BATTLEFIELD | 2B |
| 0x07F1 | CMSG_ENTER_LEAGUE_BATTLEFIELD_REQUEST | LEAGUE_BATTLEFIELD | 2B |
| 0x07F2 | CMSG_EXIT_LEAGUE_BATTLEFIELD_REQUEST | LEAGUE_BATTLEFIELD | 2B |
| 0x1AC3 | CMSG_DAMAGE_GIFT_INFO | DAMAGE_HELP | 2B |
| 0x1AC5 | CMSG_DAMAGE_HELP | DAMAGE_HELP | 2B |
| 0x1AC7 | CMSG_DAMAGE_BUY | DAMAGE_HELP | 2B |
| 0x1AC9 | CMSG_DAMAGE_BUY_ITEM | DAMAGE_HELP | 2B |
| 0x1ACB | CMSG_DAMAGE_SHARE | DAMAGE_HELP | 5B |
| 0x1ACD | CMSG_DAMAGE_HELP_NOTIFY | DAMAGE_HELP | ? |
| 0x0245 | CMSG_QUERY_DOMINION_INFO | DOMINION | 2B |
| 0x0246 | CMSG_QUERY_DOMINION_SIMPLE_BATTLE_INFO | DOMINION | 2B |
| 0x0258 | CMSG_QUERY_DOMINION_OFFICIAL_INFO | DOMINION | 2B |
| 0x025A | CMSG_SET_DOMINION_OFFICIAL | DOMINION | 2B |
| 0x060A | CMSG_DOMINION_ACTION_END | DOMINION_ACTION_KING | ? |
| 0x083E | CMSG_QUERY_WORLD_BATTLE_ACTION_CONFIG | WORLD_BATTLE | 2B |
| 0x084C | CMSG_WORLD_BATTLE_ENTER_REQUEST | WORLD_BATTLE | 2B |
| 0x084D | CMSG_WORLD_BATTLE_EXIT_REQUEST | WORLD_BATTLE | 2B |
| 0x0CF0 | CMSG_WORLD_BATTLE_NEW_SIGN_UP_REQUEST_NEW | WORLD_BATTLE | 2B |
| 0x096D | CMSG_WORLD_BATTLEFIELD_SELF_GROUP_REQUEST | WORLD_BATTLE_GROUPS | 2B |
| 0x0F0B | CMSG_ENTER_FORTRESS_VIEW | FORTRESS | 2B |
| 0x0F0D | CMSG_QUERY_FORTRESS_ACTION | FORTRESS | 2B |
| 0x0F13 | CMSG_ENTER_FORTRESS_REQUEST | FORTRESS | 2B |
| 0x0F14 | CMSG_EXIT_FORTRESS_REQUEST | FORTRESS | 2B |
| 0x15AE | CMSG_QUERY_LOSTLAND_ACTION_CONFIG | LOSTLAND | 2B |
| 0x15B1 | CMSG_ENTER_LOSTLAND_VIEW | LOSTLAND | 2B |
| 0x15B3 | CMSG_LOSTLAND_MAPINFO_REQUEST | LOSTLAND | 2B |
| 0x15B4 | CMSG_LOSTLAND_MAPINFO_RESPONSE | LOSTLAND | ? |
| 0x15B5 | CMSG_ENTER_LOSTLAND_REQUEST | LOSTLAND | 2B |
| 0x15B6 | CMSG_EXIT_LOSTLAND_REQUEST | LOSTLAND | 2B |
| 0x15C8 | CMSG_LOSTLAND_DONATE_CD_END | LOSTLAND | 2B |
| 0x15C9 | CMSG_LOSTLAND_DONATE_INFO | LOSTLAND | ? |
| 0x15D2 | CMSG_LOSTLAND_SELF_CAMP_AREA | LOSTLAND | ? |
| 0x15D3 | CMSG_LOSTLAND_SELF_DOMINION_REQUEST | LOSTLAND | 2B |
| 0x15D4 | CMSG_LOSTLAND_SELF_DOMINION_RESPONSE | LOSTLAND | ? |
| 0x15D5 | CMSG_LOSTLAND_LEAGUE_BUILD_REQUEST | LOSTLAND | 2B |
| 0x15DB | CMSG_LOSTLAND_ACHIEVEMENT_COMPLETE | LOSTLAND | ? |
| 0x15E3 | CMSG_SELF_LEAGUEBUILD_SYNC | LOSTLAND_BUILDINGS | ? |
| 0x15EA | CMSG_QUERY_LEAGUEBUILD_DEFEND_INFO | LOSTLAND_BUILDINGS | 2B |
| 0x15EC | CMSG_KICK_LEAGUE_BUILD_DEFEND_ARMY | LOSTLAND_BUILDINGS | 2B |
| 0x1FAB | CMSG_QUERY_LOSTLAND_RUSH_EVENT | LOSTLAND_RUSH_EVENT | 5B |
| 0x0C4F | CMSG_LEGION_ACTION_REQUEST | LEGION | 2B |
| 0x0C59 | CMSG_KICK_LEGION_MEMBER | LEGION | 2B |
| 0x0C5E | CMSG_CHANGE_LEGION_POSTION | LEGION | 2B |
| 0x0E10 | CMSG_LEGION_SEASON_ACTION_REQUEST | LEGION_SEASON | 2B |
| 0x0E26 | CMSG_LEGION_FINAL_POINT | LEGION_SEASON | ? |
| 0x1AF9 | CMSG_ENTER_CLANPK_VIEW | CLANPK | 2B |
| 0x1B03 | CMSG_EXIT_CLANPK_REQUEST | CLANPK | 2B |
| 0x1B16 | CMSG_CLANPK_QUERY_DEFEND_INFO | CLANPK | 2B |
| 0x1B18 | CMSG_CLANPK_QUERY_ATTACK_INFO | CLANPK | 2B |
| 0x1B1A | CMSG_CLANPK_START_ATTACK | CLANPK | 5B |
| 0x1B1F | CMSG_CLANPK_MAILBOX_MAIL_REQUEST | CLANPK | 2B |
| 0x1B20 | CMSG_CLANPK_MAILBOX_MAIL | CLANPK | 2B |
| 0x1B21 | CMSG_CLANPK_START_DEFEND | CLANPK | 5B |
| 0x1B23 | CMSG_CLANPK_ATTACK_BUILDING_BEGIN | CLANPK | ? |
| 0x1B24 | CMSG_CLANPK_ATTACK_BUILDING_END | CLANPK | ? |
| 0x1B26 | CMSG_CLANPK_THUNDER_ATTACK_END | CLANPK | ? |
| 0x1B27 | CMSG_CLANPK_CHAT_HISTORY | CLANPK | ? |
| 0x0A30 | CMSG_KING_CHESS_ENABLE_VIEW | KING_CHESS | 2B |
| 0x0A36 | CMSG_KING_CHESS_SET_LOOK_CHAT | KING_CHESS | 2B |
| 0x0A4B | CMSG_KING_CHESS_SELF_INFO_REQUEST | KING_CHESS | 2B |
| 0x0A4C | CMSG_KING_CHESS_ALL_LEAGUE_INFO_REQUEST | KING_CHESS | 2B |

## Cross-System Analysis

### Common Patterns Across War Systems

Most war systems follow a consistent pattern:
1. **SYS_INFO/CONFIG** - Server pushes system state on login
2. **ENTER_VIEW** - Client opens the UI (no gameplay effect)
3. **QUERY_ACTION** - Client requests current event status
4. **SIGNUP** - Client registers for the event
5. **ENTER** - Client enters the battlefield
6. **ACTION** - Gameplay actions during the event
7. **RANK_VIEW** - Check rankings
8. **REWARD** - Collect rewards
9. **EXIT** - Leave the battlefield

### Systems with Donate/Help (daily farm):

- LEAGUE_TECH_DONATE_SHOP: 0x01ED CMSG_LEAGUE_DONATE
- LOSTLAND: 0x15B7 CMSG_LOSTLAND_DONATE_RESOURCE_REQUEST
- LOSTLAND: 0x15B9 CMSG_LOSTLAND_DONATE_HEROCHIP_REQUEST
- LOSTLAND: 0x15C8 CMSG_LOSTLAND_DONATE_CD_END
- LOSTLAND: 0x15C9 CMSG_LOSTLAND_DONATE_INFO
- CLANPK: 0x1B08 CMSG_CLANPK_DONATE_REQUEST
- LEAGUE_BIG_BOSS: 0x1F0F CMSG_LEAGUE_BIG_BOSS_DONATE_POINT_REQUEST
- LEAGUE_BIG_BOSS: 0x1F11 CMSG_LEAGUE_BIG_BOSS_DONATE_REQUEST

### Systems with Shop/Buy (resource spending):

- LEAGUE_TECH_DONATE_SHOP: 0x01FE CMSG_LEAGUE_SHOP_BUY
- DAMAGE_HELP: 0x1AC7 CMSG_DAMAGE_BUY
- DAMAGE_HELP: 0x1AC9 CMSG_DAMAGE_BUY_ITEM
- LOSTLAND: 0x15BB CMSG_LOSTLAND_SHOP_BUY_REQUEST
- LOSTLAND: 0x15BD CMSG_SYNC_LOSTLAND_SHOP_BUY_TIMES

### Systems with Reward Collection:

- LEAGUE_BATTLEFIELD: 0x07EF CMSG_LEAGUE_BATTLEFIELD_GET_REWARD_REQUEST
- DOMINION_ACTION_KING: 0x0610 CMSG_BESTOW_KING_REWARD_REQUEST
- FORTRESS: 0x0F22 CMSG_BESTOW_FORTRESS_REWARD_REQUEST
- LOSTLAND: 0x15CA CMSG_LOSTLAND_MARK_REWARD_REQUEST
- LOSTLAND: 0x15DE CMSG_LOSTLAND_ACHIEVEMENT_REWARD_REQUEST
- LOSTLAND_BUILDINGS: 0x15FF CMSG_LOSTLAND_MONTH_CARD_REWARD_REQUEST
- LOSTLAND_RUSH_EVENT: 0x1FAD CMSG_LOSTLAND_RUSH_EVENT_REWARD_REQUEST
- CLANPK: 0x1B36 CMSG_CLANPK_FIRST_LEVEL_REWARD_REQUEST
- LEAGUEPASS: 0x166C CMSG_LEAGUEPASS_GET_REWARD_REQUEST
- KING_ROAD: 0x0993 CMSG_KING_ROAD_REWARD_REQUEST

## Statistics

- Total systems analyzed: 22
- Total opcodes: 388
- Constructors found in symbols: 387
- packData functions found: 174
- getData functions found: 225
- Fire-and-forget C2S opcodes: 66
- C2S (client to server): 188
- S2C (server to client): 199
- Bidirectional: 1

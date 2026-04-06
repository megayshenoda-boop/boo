# Major Discoveries - libgame.so Deep Analysis
## Date: 2026-04-04

---

## Discovery 1: 872 Opcode-to-CMSG Name Mappings

Extracted opcodes directly from ARM64 constructor code. Each CMSG constructor
stores its opcode at struct offset 0x02 (u16). Total: **872 unique CMSG opcodes**.

See `cmsg_opcodes.py` for full Python dict, `cmsg_opcode_map.md` for categorized list.

### Critical opcode corrections:
```
0x0323 = CMSG_HERO_SOLDIER_RECRUIT_REQUEST  (NOT pre-march!)
0x033E = CMSG_REQUEST_MONSTER_POS           (tile/monster search)
0x0CE8 = CMSG_START_MARCH_NEW              (confirmed)
0x0CEB = CMSG_ENABLE_VIEW_NEW              (confirmed)
0x0065 = CMSG_ITEM_USE                     (NEW - use items/speedups!)
```

**BIG FIX:** `0x0323` is **HERO_SOLDIER_RECRUIT_REQUEST**, not PRE_MARCH.
Previous gather tests were sending a recruit request before march - wrong!

---

## Discovery 2: Simple 2-Byte Payload Pattern

**39 out of 42 analyzed bot-useful CMSGs have just 2-byte payloads** (single u16).

The packData function for most CMSGs just writes 1 field:
- struct[0x00] = u16 value (item_id, reward_id, quest_id, etc.)

### Bot Commands (all 2-byte payload = just u16 id):
```
0x0065  CMSG_ITEM_USE                           item_id
0x0111  CMSG_CITY_BUFF_USE                      buff_id
0x01D3  CMSG_OUTFIRE_REQUEST                    (fire_type?)
0x01DE  CMSG_RECEIVE_SIGN_ACTIVITY              activity_id
0x0224  CMSG_ACHIEVEMENT_RECEIVE_REWARD_REQUEST  achievement_id
0x0280  CMSG_MONTH_REFRESH_REQUEST              (type)
0x0281  CMSG_DAY_REFRESH_REQUEST                (type)
0x0284  CMSG_SIGN_REQUEST                       sign_type
0x0285  CMSG_APPEND_SIGN_REQUEST                sign_type
0x028F  CMSG_NEW_ONLINE_REWARD_REQUEST          reward_id
0x0292  CMSG_RANDOM_ONLINE_REWARD_REQUEST       reward_id
0x0312  CMSG_EVERY_DAY_GIFTPACK_REWARD_REQUEST  giftpack_id
0x0390  CMSG_CAMEL_SHOP_BUY_REQUEST             item_id
0x062C  CMSG_RECEIVE_REWARD_REQUEST             quest_id
0x062F  CMSG_RECEIVE_REWARD_BATCH_REQUEST       batch_id
0x069D  CMSG_RECEIVE_ACCUMULATION_REWARD_REQUEST acc_id
0x06FB  CMSG_MICROPAYMENT_DAILY_REWARD_REQUEST  (id)
0x06FD  CMSG_DOWN_LOAD_REWARD_REQUEST           (type)
0x07BE  CMSG_MOBILIZATION_GET_REWARD_REQUEST    reward_id
```

### Exception - Multi-field payloads:
```
CMSG_POWER_TASK_REWARD_REQUEST: 8B (u16 + u32 + u16)
CMSG_START_MARCH_NEW: 46B (complex march struct)
CMSG_DESERT_TRADE_START_MARCH_REQUEST: complex
```

---

## Discovery 3: Key Opcode Pairs (Request -> Response)

From the 872-opcode map, we can identify request/response pairs:
```
0x0284 SIGN_REQUEST           -> 0x0283 (response)
0x028F NEW_ONLINE_REWARD_REQ  -> 0x028E (response)
0x062C RECEIVE_REWARD_REQ     -> 0x062B (response)
0x0065 ITEM_USE               -> (no explicit return in name)
0x0312 EVERYDAY_GIFT_REQ      -> 0x0311 (response)
0x0390 CAMEL_SHOP_BUY_REQ     -> 0x038F (response)
```

Pattern: Response opcode = Request opcode - 1 (common) or explicit RETURN pair.

---

## Discovery 4: 93+ Reward/Free Collection Endpoints

The game has massive number of free reward endpoints. All client-sendable:
- CMSG_RECEIVE_REWARD_REQUEST (quests)
- CMSG_RECEIVE_REWARD_BATCH_REQUEST (batch)
- CMSG_ACHIEVEMENT_RECEIVE_REWARD_REQUEST
- CMSG_NEW_ONLINE_REWARD_REQUEST
- CMSG_RANDOM_ONLINE_REWARD_REQUEST
- CMSG_EVERY_DAY_GIFTPACK_REWARD_REQUEST
- CMSG_ACTIVEGIFTS_ACTION_REQUEST / REWARD_REQUEST
- CMSG_LUCKY_TURNTABLE_TURN_REQUEST
- CMSG_LUCKY_SHOP_SCRATCH_CARD
- CMSG_MOBILIZATION_GET_REWARD_REQUEST
- CMSG_POWER_TASK_REWARD_REQUEST
- CMSG_MICROPAYMENT_DAILY_REWARD_REQUEST
- CMSG_DOWN_LOAD_REWARD_REQUEST
- CMSG_RECEIVE_ACCUMULATION_REWARD_REQUEST
- CMSG_BUILDING_SKIN_REWARD_REQUEST
- CMSG_KINGDOM_GIFT_LEVEL_REWARD_REQUEST
- CMSG_LOSTLAND_ACHIEVEMENT_REWARD_REQUEST
- ...and 70+ more

---

## Discovery 5: Fire-and-Forget Commands (No Response Expected)

46 CMSGs that have packData (client sends) but NO matching RETURN:
- CMSG_SIGN_REQUEST (0x0284) - Daily sign-in
- CMSG_DAY_REFRESH_REQUEST (0x0281)
- CMSG_MONTH_REFRESH_REQUEST (0x0280)
- CMSG_OUTFIRE_REQUEST (0x01D3) - Extinguish castle fire
- CMSG_NEW_ONLINE_REWARD_REQUEST (0x028F)
- CMSG_ARENA_BUY_TIMES_REQUEST (0x05EC)
- CMSG_ARENA_TIMES_RESTORE_REQUEST (0x05EB)
- CMSG_HERO_SOLDIER_RECRUIT_REQUEST (0x0323)
- CMSG_EXPEDITION_BUILDUP_REQUEST (0x02B7)

These are potential abuse targets since server may not validate thoroughly.

---

## Discovery 6: 173 Game Manager Classes

Key managers for bot automation:
- CDailyFreeGiftManager, CDailySignManager
- COnlineRewardsTaskManager, COnlineRewardsVipManager
- OneClickAccelerateManager (speed-up automation!)
- CItemSpeedUpConfigManager
- HeroTroopManager, TroopConfigManager
- CWatchTowerManager (march tracking)
- TaskDataManager
- CProductManager, CItemShopManager
- VipBuffManager, LeagueHelpDataManager
- ErrorMessageManager (error code lookup)
- GameConfigManager

---

## Discovery 7: 0x033E = CMSG_REQUEST_MONSTER_POS

The tile search opcode `0x033E` is actually "Request Monster Position".
Response is `0x033F`. This is what we used for finding resource tiles.

---

## Discovery 8: Game Config XML Files (139 total)

Data-defining XMLs found in .rodata:
- Soldiers_recruitXml, Soldiers_upXml
- Army_lossXml, Army_skinXml
- Soul_costXml, Player_limitXml
- Lord_level_growXml
- Red_envelopes_limitXml
- Kingdom_gift_reward_levelXml
- Activity_chess_buffXml
- Record_cost_group_configXml

---

---

## Discovery 9: START_MARCH_NEW (0x0CE8) Payload Format - FULLY DECODED

20 fields, 46 bytes base + N*4 bytes per troop entry:

| Offset | Size | Field |
|--------|------|-------|
| 0 | 2B | sub_type (u16) |
| 2 | 2B | march_type (u16) |
| 4-8 | 5x1B | 5 flag bytes (u8 each) |
| 9 | 8B | target_coords (u64 = packed x,y) |
| 17 | 2B | kingdom_id (u16) |
| 19 | 2B | march_slot (u16) |
| 21 | 1B | array_count (u8) |
| 22+ | N*4B | troop/hero array (u32 each) |
| +4B | 4B | tile_type/resource_id (u32) |
| +1B | 1B | sub_flag (u8) |
| +8B | 8B | rally_param (u64) |
| +1B | 1B | extra_flag_0 (u8) |
| +1B | 1B | extra_flag_1 (u8) |
| +8B | 8B | param_2 (u64) |
| +1B | 1B | extra_flag_2 (u8) |
| +4B | 4B | param_3 (u32) |

After payload serialization: writes length prefix, calls getServerKey(), then Encode().

---

## Discovery 10: March Flow From PCAPs

After sending 0x0CE8, server responds with:
1. **0x0033** (SYN_ATTRIBUTE) - resource deduction (food/gold spent)
2. **0x06C2** (SOLDIER_INFO) - updated troop counts
3. **0x0033** - more attribute changes
4. **0x0071** (MARCH_STATE) - march sync with coordinates + hero + player name string

0x0071 format (70 bytes): march_id(u32) + kingdom(u16*2) + flags + hero_id(u16) + coords(u16*4) + player_name_len(u16) + name_string

---

## Discovery 11: Game Data Structures Decoded

**ITEM_INFO (0x0064)**: u32 count + (u32 item_id, u32 quantity) * N = 8B per item
**BUILDING_INFO (0x0097)**: u16 count + 19B entries (u16 slot, u16 type, u16 level, 13B extra)
**SOLDIER_INFO (0x06C2)**: u32 count + entries (type bitmask: 1=inf,2=ranged,4=cav,8=siege)
**HERO_INFO (0x00AA)**: u32 count + 109B entries (u32 hero_id + fields)
**CHAT_HISTORY (0x026D)**: u16 channel + header + variable messages
**SYN_ATTRIBUTE (0x0033)**: u32 attr_id + u64 value (confirmed from PCAP)
**0x0037**: Error/status: u32 error_code + u32 param + u32 zero
**0x00B8**: March ACK: either 1B (0x00=ok) or 10B (with hero_ids)

---

## Discovery 12: AutoHangup & AutoAttackRebel Features

**AutoHangupManager** (55 symbols): Offline/idle auto-farming
- requestAutoHandupChange(type,flag,tier,troops,filter,time,bank,res_wish)
- CMSG_AUTO_HANDUP_CHANGE_REQUEST (opcode 0x1933 from constructor)
- CMSG_SYNC_AUTO_HANDUP (server sync)
- Features: auto-gather, auto-train, auto-monster, auto-bank
- Requires VIP privilege (isBuyPrivilegeGift check)

**LogicAutoAtkRebel** (42 methods): Auto-attack rebel monsters
- startFight(), autoAttackMonster(), findMonster(), attackMonster()
- checkEnergy(), useItem() (auto-use energy items)
- recuitSoldier() (auto-recruit troops)
- Uses CMSG_REQUEST_MONSTER_POS (0x033E) + CMSG_RESPONSE_MONSTER_POS (0x033F)
- canMarchExpedition() check before sending march
- Full flow: findMonster -> checkTeam -> attackMonster -> checkBattleResult -> repeat

**OneClickAccelerateManager** (16 symbols): One-click speed-up
- recordCanUseItems(), getUseItemsByRemainTime()
- Pure client-side: uses CMSG_ITEM_USE (0x0065) repeatedly
- No special opcode - just iterates speedup items and sends ITEM_USE for each

**CMSG_AUTO_JOIN_BUILDUP**: Auto-join alliance rallies
- OPEN_REQUEST / CLOSE_REQUEST opcodes
- Server-side state: CMSG_SYNC_AUTO_JOIN_BUILDUP_INFO

---

## Discovery 13: Vulnerability Analysis

**129 Fire-and-forget CMSGs** (53 requests + 76 others) with no server confirmation
**24 single-ID CMSGs** (2-byte payload) - enumerable targets
**93 reward CMSGs**, 6 without RETURN = no server validation visible
**0x0035 = CMSG_PM_COMMAND** - admin/GM command opcode!
**Replay risk**: Encrypted opcodes use predictable msg_value counter
**Rate limit strings**: cooldown (41), timer (298), limit (960), max (298)
**Resource validation**: mostly client-side UI checks, server checks exist for "not enough"

---

## Discovery 14: XML Config Files (690 total!)

Key game data XMLs from .rodata:
- item_speedup.xml, soldier.xml, client_building.xml, science.xml
- quest.xml, hero_equip.xml, server_map.xml, vip.xml, lord_skill.xml
- 690 total XML refs across 18 categories (items, buildings, troops, research, heroes, maps, quests, alliance, shop, gacha, UI, etc.)

---

## Discovery 15: Server Architecture

- Game server: port **7001** (main gameplay), port **7000** (alternate/second connection)
- Gateway: 54.93.167.80:5997
- 398 unique opcodes seen in PCAPs
- 64 client-only, 331 server-only, 3 bidirectional (0x0002, 0x0042, 0x0043)
- Heartbeat (0x0042): client sends 4B, server responds 8B
- Server time (0x0043): bidirectional, u32 values

---

## Key Next Steps

1. **Fix gather**: Remove 0x0323 (it's recruit, not pre-march). Send 0x0CE8 with correct payload format
2. **Implement CMSG_ITEM_USE (0x0065)**: 2-byte payload, use speedups/items
3. **Implement daily rewards**: SIGN, ONLINE_REWARD, GIFTPACK - all 2-byte
4. **OneClickAccelerate**: Just use ITEM_USE (0x0065) with speedup item IDs
5. **Alliance help automation**: CMSG_DAMAGE_HELP (0x1ACD)
6. **Auto-attack rebels**: Use the LogicAutoAtkRebel flow (findMonster->attackMonster)
7. **Decrypt PCAP marches**: Use server_key + Encode formula to verify payload format
8. **Map 0x0037 error codes**: Error code 22=timestamp?, 43=account?, 13=?

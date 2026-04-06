# Complete Bot Automation Summary
# IGG Conquerors (Lords Mobile) - Full Analysis Results
# Generated: 2026-04-05

## Analysis Coverage

| Report | File | Lines | Opcodes |
|--------|------|-------|---------|
| Alliance/War Systems | alliance_war_systems.md | 3,106 | 388 |
| Hero/Equipment | hero_equipment_systems.md | 530 | 22 |
| Chat/Social/Events | chat_social_events.md | 1,955 | 319 |
| VIP/Shop/Payment | vip_shop_payment.md | 12,044 | ~100 |
| Vulnerability Scan | vulnerability_deep_scan.md | 10,573 | 46 vulns |
| Arena/PvP | arena_pvp_systems.md | 204 | 30 |
| Previous findings | 12 reports | ~500K lines | 872 total |

**TOTAL: 872 CMSGs fully categorized, 46 vulnerabilities found (14 CRITICAL)**

---

## ALL AUTOMATABLE BOT COMMANDS (by priority)

### PRIORITY 1: Daily Routine (fire-and-forget, 2B payloads)

| Opcode | Command | Payload | Notes |
|--------|---------|---------|-------|
| 0x0284 | SIGN_REQUEST | 2B (u16=0) | Daily sign-in |
| 0x0285 | APPEND_SIGN | 2B | Makeup sign |
| 0x01DE | RECEIVE_SIGN_ACTIVITY | 2B | Sign activity reward |
| 0x028F | ONLINE_REWARD | 2B | Online time reward |
| 0x0292 | RANDOM_ONLINE_REWARD | 2B | Random online reward |
| 0x0312 | EVERYDAY_GIFT | 2B | Daily gift pack |
| 0x189D | EVERYDAY_GIFT_NEW | 2B | New daily gift (F&F!) |
| 0x062C | RECEIVE_REWARD | 2B | Quest reward |
| 0x062F | RECEIVE_REWARD_BATCH | 2B | Batch quest rewards |
| 0x069D | ACCUMULATION_REWARD | 2B | Accumulation reward |
| 0x06FB | MICROPAY_DAILY | 2B | Micropay daily |
| 0x06FD | DOWNLOAD_REWARD | 2B | Download reward (F&F!) |
| 0x07BE | MOBILIZATION_REWARD | 2B | Mobilization reward |
| 0x0224 | ACHIEVEMENT_REWARD | 2B | Achievement reward |
| 0x0226 | ACHIEVEMENT_SCORE_REWARD | 2B | Score reward |
| 0x0989 | LUXURY_REWARD | 2B | Luxury reward (F&F!) |
| 0x0993 | KING_ROAD_REWARD | 2B | King's Road reward |
| 0x0A07 | GAIN_EXP_REWARD | 2B | Championship EXP |
| 0x1ACD | ALLIANCE_HELP | 2B | Alliance help all |
| 0x01D3 | OUTFIRE | 2B | Extinguish fire |
| 0x0281 | DAY_REFRESH | 2B | Day refresh |
| 0x0280 | MONTH_REFRESH | 2B | Month refresh |

### PRIORITY 2: Resource Gathering & March

| Opcode | Command | Payload | Notes |
|--------|---------|---------|-------|
| 0x0CE8 | START_MARCH_NEW | 50B+N*4B | Encrypted, 20 fields |
| 0x0CE9 | CANCEL_MARCH_NEW | 8B | Cancel active march |
| 0x033E | REQUEST_MONSTER_POS | 2B | Find monster |
| 0x0CEB | ENABLE_VIEW_NEW | 10B | Required pre-march |
| 0x0065 | ITEM_USE | 2B+4B+4B | Speedups, shields, resources |
| 0x0111 | CITY_BUFF_USE | 2B | City buffs |

### PRIORITY 3: Training & Building

| Opcode | Command | Payload | Notes |
|--------|---------|---------|-------|
| 0x0CED | TRAIN | 19B | Encrypted, troop training |
| 0x0CEF | BUILD | 22B | Encrypted, build/upgrade |
| 0x0CEE | RESEARCH | 12B | Encrypted, research |
| 0x06C7 | TRAIN_ITEM_SPD | 6B | Speed up training |
| 0x06C9 | TRAIN_COMPLETE | 4B | Collect training |
| 0x06D4 | TRAIN_ONEKEY | 6B | One-key speed all |
| 0x009F | BUILD_HELP | 4B | Alliance build help |
| 0x00C6 | RESEARCH_HELP | 2B | Alliance research help |

### PRIORITY 4: Arena & PvP Automation

| Opcode | Command | Payload | Notes |
|--------|---------|---------|-------|
| 0x0CF4 | ARENA_MATCH_INFO_NEW | encrypted | Get opponents |
| 0x0CF5 | ARENA_CHANGE_MATCH_NEW | encrypted | Refresh opponents |
| 0x05F1 | ARENA_CHALLENGE | 2B | Start fight |
| 0x05EB | ARENA_TIMES_RESTORE | 2B | Restore attempts (F&F!) |
| 0x05EC | ARENA_BUY_TIMES | 2B | Buy attempts (F&F!) |
| 0x02B2 | EXPEDITION_INFO | 2B | Get expedition stages |
| 0x02B6 | EXPEDITION_BATTLE | 2B | Fight expedition |

### PRIORITY 5: Alliance/Guild Events

| Opcode | Command | Payload | Notes |
|--------|---------|---------|-------|
| 0x07EF | LEAGUE_BATTLEFIELD_REWARD | 2B | Guild Fest reward |
| 0x07F1 | ENTER_LEAGUE_BATTLEFIELD | 2B | Enter guild event (F&F!) |
| 0x166C | LEAGUEPASS_GET_REWARD | 2B | Guild Pass reward |
| 0x1670 | LEAGUEPASS_FINISH_TASK | 2B | Complete GP task |
| 0x1F0F | BIG_BOSS_DONATE_POINT | 2B | Guild Boss donate |
| 0x0C57 | LEGION_JOIN | 2B | Join legion |
| 0x15B7 | LOSTLAND_DONATE_RESOURCE | 2B | Lost Land donate |

### PRIORITY 6: Shop & Lottery (free spins)

| Opcode | Command | Payload | Notes |
|--------|---------|---------|-------|
| 0x039C | LUCKY_TURNTABLE_TURN | 2B | Lucky spin |
| 0x09A7 | LUCKY_SHOP_SCRATCH | 2B | Scratch card |
| 0x0E75 | WHEEL_TURN | 2B | Wheel spin |
| 0x1D4D | DOUBLE_LOTTERY_PLAY | 2B | Double lottery |
| 0x0B55 | LUCKY_LINE_OPEN | 2B | Lucky line |
| 0x038E | CAMEL_SHOP_INFO | 2B | Camel shop (F&F!) |
| 0x0390 | CAMEL_SHOP_BUY | 2B | Buy from camel |

### PRIORITY 7: Event Rewards (periodic)

| Opcode | Command | Payload | Notes |
|--------|---------|---------|-------|
| 0x16B2 | EXTRA_GIFTPACK_REWARD_NEW | 2B | Extra gift (F&F CRITICAL!) |
| 0x16CE | RETURN_EVENT_REWARD_NEW | 2B | Return event (F&F CRITICAL!) |
| 0x099F | EXCHANGE_GET_REWARD | 2B | Exchange reward |
| 0x13BD | SERVER_MISSION_RECEIVE | 2B | Server mission |
| 0x1453 | DAILYCONSUME_REWARD | 2B | Daily consume reward |
| 0x1774 | RECHARGEBONUS_REWARD | 2B | Recharge bonus |
| 0x15CA | LOSTLAND_MARK_REWARD | 2B | Lost Land mark reward |
| 0x15FF | LOSTLAND_MONTH_CARD | 2B | Lost Land month card |

---

## CRITICAL VULNERABILITIES (14 found)

### Fire-and-Forget Reward Exploits
These opcodes have NO server RETURN - potentially spammable:

| # | Opcode | Name | Exploit |
|---|--------|------|---------|
| 1 | 0x06FD | DOWNLOAD_REWARD | Spam claim, no confirmation |
| 2 | 0x0A05 | CHAMPIONSHIP_REWARD | Spam claim, no confirmation |
| 3 | 0x16B2 | EXTRA_GIFTPACK_REWARD_NEW | Spam claim, no confirmation |
| 4 | 0x16B4 | EXTRA_GIFTPACK_ACTION_NEW | Spam action, no confirmation |
| 5 | 0x16CE | RETURN_EVENT_REWARD_NEW | Spam claim, no confirmation |
| 6 | 0x189D | EVERYDAY_GIFT_NEW | Spam claim, no confirmation |
| 7 | 0x004D | FIRST_BIND_REWARD | One-time but no RETURN |
| 8 | 0x01DE | RECEIVE_SIGN_ACTIVITY | Spam claim, no confirmation |
| 9 | 0x069B | ADD_ACCUMULATION_GIFT | Add gift tracking |
| 10 | 0x06A1 | ACCUMULATION_GIFT_NEW | Add gift tracking (new) |
| 11 | 0x0989 | LUXURY_REWARD | Luxury reward spam |
| 12 | 0x0054 | USE_ITEM_CHANGE_BUBBLE | Item use bypass |
| 13 | 0x0065 | ITEM_USE | No RETURN, potential dupe |
| 14 | 0x0111 | CITY_BUFF_USE | No RETURN, spam buffs |

### Race Condition Targets
- `g_HeroLocks` - Hero troop locking mechanism found
- `_isTroopLocked` - Troop lock check (bypass = march same troops twice?)
- 1,792 `lock` references, 41 `mutex` references in binary
- `CRYPTO_atomic_*` functions suggest some thread-safety

### Parameter Manipulation
- All 2B payload opcodes: test with various u16 values (0-65535)
- March payload: negative troop counts? Zero kingdom_id?
- Shop buy: item_id enumeration, count=0 or count=MAX

### Admin/GM Opcode
- **0x0035 PM_COMMAND** - Admin/GM command, needs testing with various payloads

---

## BOT DAILY ROUTINE (recommended sequence)

```
Phase 1: Login & Setup
  gateway_connect -> game_connect -> wait for data packets

Phase 2: Daily Rewards (22 packets, ~7 seconds)
  0x0284 sign -> 0x0285 append_sign -> 0x01DE sign_activity
  0x028F online_reward -> 0x0292 random_online
  0x0312 everyday_gift -> 0x189D everyday_gift_new
  0x062C quest_reward -> 0x062F quest_batch
  0x069D accumulation -> 0x06FB micropay -> 0x06FD download
  0x07BE mobilization -> 0x0224 achievement -> 0x0993 king_road
  0x0A07 exp_reward -> 0x0989 luxury
  0x16B2 extra_gift -> 0x16CE return_event
  0x0281 day_refresh -> 0x0280 month_refresh
  0x1ACD alliance_help -> 0x01D3 extinguish_fire

Phase 3: Speedups (from inventory)
  Loop ITEM_USE(0x0065) for all speedup items (1100-1155)

Phase 4: Training
  0x0CED train(type, count) for each barracks

Phase 5: Building
  0x0CEF build(type, slot, UPGRADE) for next upgrade

Phase 6: Research
  0x0CEE research(tech_id, cat)

Phase 7: Gathering (repeat on timer)
  0x033E find_tile -> 0x0CEB enable_view -> 0x0CE8 gather
  Wait for march return, send next

Phase 8: Monster Hunting (repeat on timer)
  0x033E find_monster(level) -> wait 0x033F -> 0x0CE8 attack
  Wait for battle result -> use energy item -> repeat

Phase 9: Arena (if available)
  0x0CF4 get_opponents -> 0x05F1 challenge -> repeat 5x

Phase 10: Idle Loop
  Heartbeat every 60s, re-gather when march returns,
  collect timed rewards periodically
```

---

## FILE INDEX

| # | Script | Output | Status |
|---|--------|--------|--------|
| 50 | 50_alliance_war_analysis.py | alliance_war_systems.md | DONE |
| 51 | 51_hero_equipment_analysis.py | hero_equipment_systems.md | DONE |
| 52 | 52_chat_social_events_analysis.py | chat_social_events.md | DONE |
| 53 | 53_vip_shop_payment_analysis.py | vip_shop_payment.md | DONE |
| 54 | 54_vulnerability_deep_scan.py | vulnerability_deep_scan.md | DONE |
| 55 | 55_arena_pvp_analysis.py | arena_pvp_systems.md | DONE |

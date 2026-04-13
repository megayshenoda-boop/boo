# 57: Missing Bot Commands - Complete Catalog
# Date: 2026-04-09
# Purpose: Every opcode that analysis discovered but bot doesn't use yet

---

## Category 1: Daily Rewards (Fire-and-Forget, 2B payload)

Commands the bot SHOULD be calling but ISN'T:

| Opcode | CMSG Name | Payload | In Bot? | Priority |
|--------|-----------|---------|---------|----------|
| 0x189D | EVERYDAY_GIFT_NEW | 2B (u16=0) | ❌ NO | HIGH |
| 0x0226 | ACHIEVEMENT_SCORE_REWARD | 2B | ❌ NO | HIGH |
| 0x0989 | LUXURY_REWARD | 2B (F&F!) | ❌ NO | HIGH |
| 0x0993 | KING_ROAD_REWARD | 2B | ❌ NO | MEDIUM |
| 0x0A07 | GAIN_EXP_REWARD | 2B | ❌ NO | MEDIUM |
| 0x16B2 | EXTRA_GIFTPACK_REWARD_NEW | 2B (F&F CRITICAL!) | ❌ NO | CRITICAL |
| 0x16CE | RETURN_EVENT_REWARD_NEW | 2B (F&F CRITICAL!) | ❌ NO | CRITICAL |
| 0x004D | FIRST_BIND_REWARD | 2B (one-time) | ❌ NO | LOW |
| 0x0054 | USE_ITEM_CHANGE_BUBBLE | 2B (F&F!) | ❌ NO | LOW |

### Already in bot ✅:
- 0x0284 SIGN_REQUEST
- 0x0285 APPEND_SIGN
- 0x01DE RECEIVE_SIGN_ACTIVITY
- 0x028F ONLINE_REWARD
- 0x0292 RANDOM_ONLINE_REWARD
- 0x0312 EVERYDAY_GIFT
- 0x062C RECEIVE_REWARD
- 0x062F RECEIVE_REWARD_BATCH
- 0x069D ACCUMULATION_REWARD
- 0x06FB MICROPAY_DAILY
- 0x06FD DOWNLOAD_REWARD
- 0x07BE MOBILIZATION_REWARD
- 0x0224 ACHIEVEMENT_REWARD

---

## Category 2: Arena/PvP Automation

| Opcode | CMSG Name | Payload | In Bot? | Notes |
|--------|-----------|---------|---------|-------|
| 0x0CF4 | ARENA_MATCH_INFO_NEW | encrypted | ❌ NO | Get opponents list |
| 0x0CF5 | ARENA_CHANGE_MATCH_NEW | encrypted | ❌ NO | Refresh opponents |
| 0x05F1 | ARENA_CHALLENGE | 2B | ❌ NO | Start arena fight |
| 0x05EB | ARENA_TIMES_RESTORE | 2B (F&F!) | ❌ NO | Restore attempts |
| 0x05EC | ARENA_BUY_TIMES | 2B (F&F!) | ❌ NO | Buy arena attempts |

### Arena Full Automation Flow:
```
1. 0x0CF4 get_opponents → parse response
2. 0x05F1 challenge(opponent_id) → wait for battle result
3. Repeat 5x daily
4. 0x05EB restore_times when needed
```

---

## Category 3: Expedition/PvE

| Opcode | CMSG Name | Payload | In Bot? |
|--------|-----------|---------|---------|
| 0x02B2 | EXPEDITION_INFO | 2B | ❌ NO |
| 0x02B6 | EXPEDITION_BATTLE | 2B | ❌ NO |
| 0x02B7 | EXPEDITION_BUILDUP | 2B (F&F!) | ❌ NO |

---

## Category 4: Lottery/Free Spins

| Opcode | CMSG Name | Payload | In Bot? |
|--------|-----------|---------|---------|
| 0x039C | LUCKY_TURNTABLE_TURN | 2B | ❌ NO |
| 0x09A7 | LUCKY_SHOP_SCRATCH | 2B | ❌ NO |
| 0x0E75 | WHEEL_TURN | 2B | ❌ NO |
| 0x1D4D | DOUBLE_LOTTERY_PLAY | 2B | ❌ NO |
| 0x0B55 | LUCKY_LINE_OPEN | 2B | ❌ NO |

---

## Category 5: Guild/Alliance Events

| Opcode | CMSG Name | Payload | In Bot? |
|--------|-----------|---------|---------|
| 0x07EF | LEAGUE_BATTLEFIELD_REWARD | 2B | ❌ NO |
| 0x07F1 | ENTER_LEAGUE_BATTLEFIELD | 2B (F&F!) | ❌ NO |
| 0x166C | LEAGUEPASS_GET_REWARD | 2B | ❌ NO |
| 0x1670 | LEAGUEPASS_FINISH_TASK | 2B | ❌ NO |
| 0x1F0F | BIG_BOSS_DONATE_POINT | 2B | ❌ NO |
| 0x15B7 | LOSTLAND_DONATE_RESOURCE | 2B | ❌ NO |

---

## Category 6: Hero Management

| Opcode | CMSG Name | Payload | In Bot? | Notes |
|--------|-----------|---------|---------|-------|
| 0x0323 | HERO_SOLDIER_RECRUIT | 2B | ❌ NO | Recruit hero troops (NOT pre-march!) |
| 0x00A8 | HERO_QUEUE_CHANGE | complex | ❌ NO | Change hero lineup |

---

## Category 7: Additional Event Rewards

| Opcode | CMSG Name | Payload | In Bot? |
|--------|-----------|---------|---------|
| 0x099F | EXCHANGE_GET_REWARD | 2B | ❌ NO |
| 0x13BD | SERVER_MISSION_RECEIVE | 2B | ❌ NO |
| 0x1453 | DAILYCONSUME_REWARD | 2B | ❌ NO |
| 0x1774 | RECHARGEBONUS_REWARD | 2B | ❌ NO |
| 0x15CA | LOSTLAND_MARK_REWARD | 2B | ❌ NO |
| 0x15FF | LOSTLAND_MONTH_CARD | 2B | ❌ NO |
| 0x178F | LOST_KING_ROAD_REWARD | 2B | ❌ NO |
| 0x1DE6 | CONTINUOUS_TASK_REWARD | 2B | ❌ NO |
| 0x1E15 | ALLFORONE_REWARD | 2B | ❌ NO |

---

## Summary: 42 missing commands total

| Category | Count | Priority |
|----------|-------|----------|
| Daily Rewards | 9 | HIGH (free resources!) |
| Arena/PvP | 5 | MEDIUM |
| Expedition | 3 | MEDIUM |
| Lottery/Spins | 5 | LOW (RNG) |
| Guild Events | 6 | MEDIUM |
| Hero Management | 2 | LOW |
| Event Rewards | 9 | LOW-MEDIUM |
| **TOTAL** | **42** | - |

### Commands to add to `commands.py` (all 2B payload = trivial):

```python
# All follow this pattern:
def new_command(self, reward_id=0):
    return self._plain_packet(OPCODE, struct.pack('<H', reward_id))
```

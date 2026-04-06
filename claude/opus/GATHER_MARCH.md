# Gather & March Protocol - IGG Conquerors (الفاتحون)

## Status: ❌ NOT FULLY WORKING YET
March/Gather needs more discovery. This documents what we know so far.

---

## March Types
| Value | Type | الوصف |
|-------|------|-------|
| 1 | Gather (تجميع) | Collect resources from tile |
| 2 | Attack (هجوم) | Attack player/monster |
| 3 | Scout (استكشاف) | Scout target |
| 4 | Reinforce (تعزيز) | Reinforce ally |
| 5 | Rally (حشد) | Alliance rally |
| 6 | Defend (دفاع) | Garrison ally |

## March Type IDs (from PCAP)
| Hex | Dec | Used for |
|-----|-----|----------|
| 0x1748 | 5960 | Gather |
| 0x1749 | 5961 | Gather variant |

## Resource Tile Type
```python
RESOURCE_TILE = 23  # tile type for resource nodes
```

---

## Full Gather Sequence (from PCAP analysis)

### Pre-requisites
1. Must send **0x0023 AUTH** packet early after login
2. Must send multiple **0x0CEB ENABLE_VIEW** calls (PCAP shows 3+)
3. Must send **0x01D6 READY_SIG** before march

### Step-by-Step Flow
```
1. → 0x0023  AUTH packet (58B, NOT encrypted)
2. → 0x0CEB  ENABLE_VIEW (10B encrypted) × 3+
3. → 0x01D6  READY_SIG
4. → 0x006E  TILE_SELECT (5B): select resource tile
5. → 0x0323  HERO_SELECT (7B): select hero for march
6. → 0x0CE8  START_MARCH (46-62B encrypted): actual march command
7. ← 0x0071  MARCH_STATE return (confirms march started)
8. ← 0x076C  MARCH_VALIDATION (tile + hero + state)
9. ← 0x007C  COLLECT_STATE (resource collection started)
```

---

## Packet Structures

### 0x006E - TILE_SELECT (5 bytes, NOT encrypted)
```
[0:2]  u16 LE  tile_x
[2:4]  u16 LE  tile_y
[4]    u8      0x01
```

### 0x0323 - HERO_SELECT (7 bytes, NOT encrypted)
```
[0]    u8   0x00
[1]    u8   0x01
[2:6]  u32  hero_id (LE)
[6]    u8   0x00
```

### 0x0CE8 - START_MARCH - ⚠ THREE CONFLICTING STRUCTURES

**Structure A: From lords_bot/codec.py (62 bytes, from PCAP raw analysis):**
```
[0]      u8   march_slot (1 or 2)
[1:4]    3B   nonce/sub-ID
[4:6]    u16  march_type_id (0x1748=5960)
[6:9]    3B   zeros
[9]      u8   target_info_1 (0x77, 0x71)
[10]     u8   0x04 (constant)
[11]     u8   target_info_2 (0x8c, 0x89)
[12]     u8   0x02 (constant)
[13]     u8   0x05 (num hero types)
[14:38]  6 × u32  hero/troop IDs [201, 212, 206, 216, 224, 211]
[38:42]  u32  troop_count
[42:46]  4B   zeros
[46:49]  3B   flag area
[49:53]  u32  IGG_ID
[53:62]  9B   zeros
```

**Structure B: From claude/commands.py (32+var bytes, bot's version):**
```
[0:4]    u32  march_slot
[4:8]    u32  march_type
[8:12]   u32  target_x
[12:16]  u32  target_y
[16:20]  u32  troop_entry_count
[20:24]  u32  hero_id (0)
[24:28]  u32  reserved (0)
[28:32]  u32  reserved (0)
[32+]    variable: 8B per troop (4B troop_id + 4B count)
```

**Structure C: From GATHER_MARCH_FINDINGS.md (46 bytes):**
```
[0]      u8   march_slot
[1:4]    3B   random nonce
[4:6]    u16  march_type (0x1749=gather)
[6:9]    3B   zeros
[9:11]   u16  tile_x
[11:13]  u16  tile_y
[13]     u8   0x01 (action flag)
[14]     u8   hero_id (0xFF)
[15:18]  3B   zeros
[18]     u8   kingdom (0xB6=182)
[19:22]  3B   zeros
[22]     u8   0x04 (constant)
[23:33]  10B  zeros
[33:37]  u32  IGG_ID
[37:46]  9B   zeros
```

**⚠ ALL THREE ARE DIFFERENT. March is NOT working yet.
Need fresh PCAP capture of successful gather to determine correct structure.**

---

## Example Tile Coordinates (from captures)
| Tile X | Tile Y | Hex X | Hex Y |
|--------|--------|-------|-------|
| 682 | 570 | 0x02AA | 0x023A |
| 653 | 567 | 0x028D | 0x0235 |

---

## Known Issues (Why Bot March Fails)
1. **Missing 0x0023 AUTH** - Bot doesn't send auth packet early enough
2. **Missing 0x1B8B SESSION** - Optional but helps
3. **Missing 0x01D6 READY_SIG** - Not yet in bot
4. **Too few 0x0CEB calls** - Bot sends 1, PCAP shows 3+
5. **Payload structure unclear** - 46B vs 62B variants

## Success Signals
| Opcode | Meaning |
|--------|---------|
| 0x0071 | MARCH_STATE - march confirmed |
| 0x076C | MARCH_VALIDATION - tile + hero + state validated |
| 0x007C | COLLECT_STATE - gathering started |

## Failure Signals
- No 0x0071 response = march rejected
- 0x011C ERROR_CODE = server error

---

## Cancel March
### New-style: 0x0CE9 (encrypted)
### Old-style: 0x0073 (unencrypted)

---

## Search Map
### 0x033E - SEARCH_MAP_REQUEST (4 bytes)
### 0x033F - SEARCH_MAP_RESPONSE (variable)
Used to find resource tiles on the map.

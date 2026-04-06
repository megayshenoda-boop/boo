# Buildings Map - IGG Conquerors (الفاتحون)

## Building Operations
| Op Code | Operation |
|---------|-----------|
| 1 | Upgrade (ترقية) |
| 2 | Demolish (هدم) |
| 3 | Build New (بناء جديد) |

## Opcode: 0x0CEF (BUILD) - 22 bytes encrypted payload

### Version from claude/commands.py (what the bot sends):
```
[0]      u8   operation (1=upgrade, 2=demolish, 3=build_new)
[1]      u8   building_type
[2]      u8   zero
[3]      u8   slot
[4:11]   7B   zeros
[11]     u8   flag = 1
[12:16]  u32  IGG_ID (LE)
[16:22]  6B   zeros
```

### Version from game_ids.py PCAP analysis (what the real client sends):
```
[0]      u8   operation/sub_type
[1:3]    u16  building_type_or_slot (seen: 55)
[3]      u8   building_type_2 (seen: 52)
[4:7]    3B   zeros
[7:11]   4B   variable
[11]     u8   flag (0 or 1)
[12:16]  u32  IGG_ID
[16:22]  6B   zeros
```

**⚠ WARNING: These two structures CONFLICT. The bot's version (commands.py)
got a server response, but the PCAP structure may be more accurate.
Need more PCAP captures to verify exact byte layout.**

## Old-Style Opcodes (unencrypted)
| Opcode | Name | Description |
|--------|------|-------------|
| 0x009D | BUILD_OLD | Old build command (op=05 for demolish) |
| 0x009E | BUILD_RESPONSE | Build response |
| 0x009F | BUILD_HELP | Request alliance help |
| 0x00A1 | EXCHANGE_BUILD | Exchange/swap building |
| 0x00A4 | BUILD_ONEKEY | One-key build (instant) |

## Inner Buildings (slot = type)
| Slot | Type ID | Building Name | الاسم بالعربي |
|------|---------|---------------|---------------|
| 1 | 1 | Castle | القلعة |
| 2 | 2 | Wall | السور |
| 3 | 3 | Embassy | السفارة |
| 4 | 4 | Battle Hall | قاعة المعركة |
| 5 | 5 | Prison | السجن |
| 6 | 6 | Altar | المذبح |
| 7 | 7 | Watchtower | برج المراقبة |
| 8 | 8 | Treasure Trove | كنز الثروة |
| 13 | 13 | Shelter | الملجأ |
| 14 | 14 | Workshop | الورشة |
| 21 | 21 | Academy | الأكاديمية |
| 23 | 23 | Trading Post | مركز التجارة |
| 24 | 24 | Barracks | الثكنة |
| 28 | 28 | Hospital 1 | المستشفى ١ |
| 29 | 29 | Hospital 2 | المستشفى ٢ |
| 30 | 30 | Vault 1 | الخزنة ١ |
| 31 | 31 | Vault 2 | الخزنة ٢ |

## Outer Buildings (resource buildings - multiple slots per type)
| Type ID | Building Name | الاسم بالعربي |
|---------|---------------|---------------|
| 51 | Farm | المزرعة |
| 52 | Mine | المنجم |
| 53 | Lumber Mill | منشرة الخشب |
| 55 | Quarry | المحجر |
| 56 | Manor | القصر |
| 60 | Familiar Building | مبنى المألوف |

## Full Outer Slot Map (from test account)
| Slot | Type ID | Building | Level | Notes |
|------|---------|----------|-------|-------|
| 51 | 55 | Quarry | 7 | |
| 52 | 56 | Manor | 6 | |
| 53 | 52 | Mine | 8 | timer=5354 |
| 54 | 52 | Mine | 8 | timer=5354 |
| 56 | 51 | Farm | 5 | timer=20382 |
| 57 | 51 | Farm | 8 | timer=32839 |
| 58 | 52 | Mine | 8 | timer=5354 |
| 59 | 53 | Lumber Mill | 8 | timer=10907 |
| 60 | 51 | Farm | 1 | timer=3944 |
| 61 | 55 | Quarry | 6 | |
| 62 | 53 | Lumber Mill | 8 | timer=10955 |
| 63 | 55 | Quarry | 6 | |
| 64 | 56 | Manor | 6 | |
| 65 | 56 | Manor | 6 | |
| 83 | 60 | Familiar | 1 | |

## Call to Arms - Visual Slot → Real Slot Mapping (ALL 30 slots, PCAP verified)
| Visual Slot | Real Server Slot | Hex | Evidence |
|-------------|-----------------|-----|----------|
| 1 | 78 | 0x4E | PCAP isolated demolish |
| 2 | 77 | 0x4D | PCAP isolated demolish |
| 3 | 80 | 0x50 | PCAP isolated demolish |
| 4 | 76 | 0x4C | PCAP isolated demolish |
| 5 | 79 | 0x4F | PCAP isolated demolish |
| 6 | 70 | 0x46 | PCAP isolated demolish |
| 7 | 75 | 0x4B | PCAP isolated demolish |
| 8 | 66 | 0x42 | PCAP isolated demolish |
| 9 | 69 | 0x45 | PCAP isolated demolish |
| 10 | 72 | 0x48 | PCAP isolated demolish |
| 11 | 68 | 0x44 | PCAP isolated demolish |
| 12 | 67 | 0x43 | PCAP isolated demolish |
| 13 | 71 | 0x47 | PCAP isolated demolish |
| 14 | 64 | 0x40 | PCAP isolated demolish |
| 15 | 61 | 0x3D | PCAP isolated demolish |
| 16 | 65 | 0x41 | PCAP isolated demolish |
| 17 | 62 | 0x3E | PCAP isolated demolish |
| 18 | 63 | 0x3F | PCAP isolated demolish |
| 19 | 59 | 0x3B | PCAP isolated demolish |
| 20 | 60 | 0x3C | PCAP isolated demolish |
| 21 | 58 | 0x3A | PCAP isolated demolish |
| 22 | 57 | 0x39 | PCAP isolated demolish |
| 23 | 56 | 0x38 | PCAP isolated demolish |
| 24 | 55 | 0x37 | PCAP isolated demolish |
| 25 | 54 | 0x36 | PCAP isolated demolish |
| 26 | 53 | 0x35 | PCAP isolated demolish |
| 27 | 74 | 0x4A | PCAP isolated demolish |
| 28 | 52 | 0x34 | PCAP isolated demolish |
| 29 | 51 | 0x33 | PCAP isolated demolish |
| 30 | 73 | 0x49 | PCAP isolated demolish |

## Demolish Packet (old-style 0x009D, op=05) - PCAP VERIFIED
```
Total payload: 12 bytes
[0]      u8   op = 0x05 (demolish action code)
[1]      u8   slot_id (real server slot, NOT visual slot!)
[2:12]   10B  zeros
```

### Demolish Examples from PCAP (hex payloads):
```
Slot 53: 053500000000000000000000
Slot 52: 053400000000000000000000
Slot 61: 053d00000000000000000000
Slot 78: 054e00000000000000000000
Slot 77: 054d00000000000000000000
Slot 76: 054c00000000000000000000
Slot 79: 054f00000000000000000000
```

### Demolish Response (0x009E):
Server echoes back slot + building type + level info.

### Worker Response (0x0098):
```
0300003500000000000100000000000002000000000000
```
(3 workers, slot info)

## Server Response Opcodes
| Opcode | Name | Description |
|--------|------|-------------|
| 0x0097 | BUILDING_INFO | Building data on login (type + level per slot) |
| 0x0098 | WORKER_INFO | Worker status |
| 0x021C | BUILDING_STATE | Building state update after action |
| 0x02D1 | ACTION_CONFIRM | Action accepted |
| 0x11C8 | TIMER_SET | Build timer started |

## Building Type Detection on Outer Slots (from PCAP)
| Type Hex | Type ID | Observed on |
|----------|---------|-------------|
| 0x33 | 51 | Multiple visual slots |
| 0x34 | 52 | Farm type |
| 0x35 | 53 | Lumber type |
| 0x37 | 55 | Quarry on slot 72 |
| 0x38 | 56 | Manor on slot 78 |

## Upgradable Buildings (level 1, ready to upgrade)
| Slot | Type | Building | Current Level |
|------|------|----------|---------------|
| 3 | 3 | Embassy | 1 |
| 4 | 4 | Battle Hall | 1 |
| 5 | 5 | Prison | 1 |
| 6 | 6 | Altar | 1 |
| 7 | 7 | Watchtower | 1 |
| 8 | 8 | Treasure Trove | 1 |
| 13 | 13 | Shelter | 1 |
| 14 | 14 | Workshop | 1 |
| 61 | 55 | Quarry | 6 |
| 63 | 55 | Quarry | 6 |
| 83 | 60 | Familiar | 1 |

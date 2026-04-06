# Troops Map - IGG Conquerors (الفاتحون)

## Opcode: 0x0CED (TRAIN) - 19 bytes encrypted payload
```
[0:4]    u32  troop_type (1=infantry, 2=cavalry, 4=ranged, 8=siege)
[4:8]    u32  count (number of troops)
[8]      u8   zero/padding
[9:13]   u32  IGG_ID
[13:19]  6B   zeros
```

## Troop Categories (for TRAIN command)
| Category Value | Type | الاسم بالعربي |
|---------------|------|---------------|
| 1 | Infantry (مشاة) | TROOP_CAT_INFANTRY |
| 2 | Cavalry (فرسان) | TROOP_CAT_CAVALRY |
| 4 | Ranged (رماة) | TROOP_CAT_RANGED |
| 8 | Siege (حصار/عجلات) | TROOP_CAT_SIEGE |

## Troop Tier IDs (for hero/march selection - from claude/protocol.py)
**WARNING:** These IDs are from protocol.py but NOT verified by PCAP.
They may be used in march payloads, NOT in training.
| ID | Type | Tier |
|----|------|------|
| 101 | Infantry T1 | مشاة مستوى ١ |
| 102 | Infantry T2 | مشاة مستوى ٢ |
| 103 | Infantry T3 | مشاة مستوى ٣ |
| 104 | Infantry T4 | مشاة مستوى ٤ |
| 201 | Ranged T1 | رماة مستوى ١ |
| 202 | Ranged T2 | رماة مستوى ٢ |
| 203 | Ranged T3 | رماة مستوى ٣ |
| 204 | Ranged T4 | رماة مستوى ٤ |
| 301 | Cavalry T1 | فرسان مستوى ١ |
| 302 | Cavalry T2 | فرسان مستوى ٢ |
| 303 | Cavalry T3 | فرسان مستوى ٣ |
| 304 | Cavalry T4 | فرسان مستوى ٤ |
| 401 | Siege T1 | حصار مستوى ١ |
| 402 | Siege T2 | حصار مستوى ٢ |
| 403 | Siege T3 | حصار مستوى ٣ |
| 404 | Siege T4 | حصار مستوى ٤ |

## Current Troops (test account)
| Type | Alive | Wounded | Max Tier |
|------|-------|---------|----------|
| Infantry | 10,048 | 3,708 | T2 |
| Ranged | 3,786 | 5,971 | T2 |
| Cavalry | 16,296 | 3,004 | T1 |
| Siege | 16,846 | 2,904 | T1 |

## PCAP Verified Training (2026-03-17, all 4 types confirmed with 0x06C4 response)
```
Infantry  count=100: troop_type=1, response=0x06C4 ✅
Cavalry   count=100: troop_type=2, response=0x06C4 ✅
Ranged    count=100: troop_type=4, response=0x06C4 ✅
Wheels    count=100: troop_type=8, response=0x06C4 ✅
```

## Example Payloads from PCAP (plaintext hex, BEFORE encryption)
```
Successful train:  01000000e001000000c9aa1e7c000000000000  (Infantry, 480)
ENABLE_VIEW first: 01c9aa1e7c0000000001  (must send before TRAIN)
Cavalry 480:       02000000e001000067c0b86900000000
Ranged 480:        04000000e001000097c1b86900000000
```

## IMPORTANT: Labels in test_live.py are WRONG
test_live.py says "Ranged=type 2, Cavalry=type 3" but PCAP proved:
- type 2 = Cavalry (NOT Ranged)
- type 4 = Ranged (NOT Siege)
- type 3 = DOES NOT WORK

## Wheel/Siege Special Training Path
Before sending 0x0CED with troop_type=8, must send these prep packets:
```
0x099D (sub=0x0193)
0x099D (sub=0x0194)
0x099D (sub=0x0197)
0x099D (sub=0x0199)
```

## Training Success Signal
- Response opcode **0x06C4** = training queued successfully
- No 0x06C4 = training rejected

## Old-Style Training Opcodes (unencrypted)
| Opcode | Name | Description |
|--------|------|-------------|
| 0x06C3 | TRAIN_OLD | Old train command |
| 0x06C5 | TRAIN_GOLD | Train with gold speedup |
| 0x06C6 | TRAIN_GOLD_SPD | Gold speed training |
| 0x06C7 | TRAIN_ITEM_SPD | Item speedup for training |
| 0x06C9 | TRAIN_COMPLETE | Training complete signal |
| 0x06D4 | TRAIN_ONEKEY | One-key instant train |

## Healing Opcodes
| Opcode | Name | Description |
|--------|------|-------------|
| 0x06CB | HEAL | Heal troops |
| 0x06CD | HEAL_GOLD | Heal with gold |
| 0x06CE | HEAL_GOLD_SPD | Gold speed heal |
| 0x06CF | HEAL_ITEM_SPD | Item speedup for heal |
| 0x06D1 | HEAL_COMPLETE | Healing complete |
| 0x06D6 | HEAL_ONEKEY | One-key instant heal |

## Server Response
| Opcode | Name |
|--------|------|
| 0x06C2 | SOLDIER_INFO (troop counts on login) |
| 0x06EB | TRAINING_ENTRY (training queue update) |

## Default Formation (from PCAP)
```python
formation = [1046, 3002, 1035, 2008, 2019, 1009, 1024, 1016, 2009, 1025]
```

## Default Troop IDs for March (from PCAP)
```python
march_troops = [403, 405, 407, 411]
```

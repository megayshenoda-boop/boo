# Heroes Map - IGG Conquerors (الفاتحون)

## Known Heroes (test account)
| Hero ID | Name | الاسم | Level | Status |
|---------|------|-------|-------|--------|
| 201 | Rose Knight | فارس الورد | 29 | Active (default) |
| 206 | Trickster | المحتال | 24 | Available |
| 212 | Scarlet Bolt | البرق القرمزي | 20 | Available |
| 216 | Sage of Storms | حكيم العواصف | 23 | Available |
| 224 | Tracker | المتعقب | 22 | Available |

## Hero IDs Observed in PCAP
| Hex | Dec | Context |
|-----|-----|---------|
| 0xFF | 255 | Default/no hero selection |
| 0xF1 | 241 | Verified hero in gather |
| 0xF4 | 244 | Verified hero in gather |
| 0xC9 | 201 | Rose Knight |
| 0xCE | 206 | Trickster |
| 0xD4 | 212 | Scarlet Bolt |
| 0xD8 | 216 | Sage of Storms |
| 0xE0 | 224 | Tracker |

## Default Hero Set (for march/gather)
```python
# 6 hero/troop type IDs seen in gather PCAP:
march_heroes = [201, 212, 206, 216, 224, 211]
```

## Hero Selection Packet (0x0323, 7 bytes, NOT encrypted)
```
[0]    u8   0x00
[1]    u8   0x01
[2:6]  u32  hero_id (LE)
[6:7]  u8   0x00
```

## Hero Info Response (0x00AA)
Server sends hero data on login - contains:
- Hero IDs
- Hero levels
- Hero equipment
- Hero skills

## Monster Targets (for hero hunting)
| Monster ID | Level |
|-----------|-------|
| 4 | Level 4 |
| 5 | Level 5 |
| 6 | Level 6 |
| 7 | Level 7 |

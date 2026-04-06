# Research & Guild Tech - IGG Conquerors (الفاتحون)

## Research Opcode: 0x0CEE (encrypted)

### From claude/commands.py (what the bot sends - 12 bytes):
```
[0:4]    u32 LE  tech_id
[4:8]    u32 LE  tech_category
[8:12]   u32 LE  reserved = 0
```
Status: "GOT_RESPONSE" from server

### From game_ids.py PCAP notes (19B variant):
```
[0:4]    u32  research_type
[4:8]    u32  param/level
[8]      u8   zero
[9:13]   u32  IGG_ID
[13:19]  6B   zeros
```

**⚠ WARNING: Two payload sizes (12B vs 19B). Both seen in different sources.
libgame.so disassembly shows 21 fields (0x15) which suggests larger payload.
Need more PCAP verification.**

## Old-Style Research Opcodes
| Opcode | Name | Description |
|--------|------|-------------|
| 0x00BF | RESEARCH_OLD | Start research |
| 0x00C0 | RESEARCH_GOLD | Research with gold |
| 0x00C1 | RESEARCH_CANCEL | Cancel research |
| 0x00C3 | RESEARCH_GOLD_SPD | Gold speedup |
| 0x00C4 | RESEARCH_ITEM_SPD | Item speedup |
| 0x00C6 | RESEARCH_HELP | Alliance help |
| 0x00C7 | RESEARCH_ONEKEY | Instant research |

## Server Responses
| Opcode | Name |
|--------|------|
| 0x00BE | SCIENCE_INFO (research tree on login) |

## getData Field Count
Research serializes **21 fields** (0x15 from libgame.so)

---

## Guild Tech IDs (from test account)
```python
guild_techs = [0, 1, 2, 3, 4, 6, 9, 10, 14, 15, 16, 17, 18, 19,
               24, 25, 28, 29, 30, 33, 36, 37, 38, 39, 41, 42,
               43, 44, 47, 48, 69, 73, 74, 75, 101]
```
- Tech 101: Level 5
- All others: Level 1

## Guild Tech Opcodes
| Opcode | Name | Description |
|--------|------|-------------|
| 0x01EC | LEAGUE_TECH_UP | Upgrade alliance tech |
| 0x01ED | LEAGUE_DONATE_OLD | Alliance donation (old) |
| 0x0CEC | LEAGUE_DONATE | Alliance donation (encrypted) |
| 0x01FE | LEAGUE_SHOP_BUY | Alliance shop purchase |

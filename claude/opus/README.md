# Opus - IGG Conquerors Bot Reference (الفاتحون)
> Reference docs - VERIFIED against source files 2026-03-26

## Files
| File | Contents |
|------|----------|
| [BUILDINGS.md](BUILDINGS.md) | Building types, ALL 30 outer slots, demolish packets |
| [TROOPS.md](TROOPS.md) | Troop categories (1,2,4,8), training payload, healing |
| [ITEMS.md](ITEMS.md) | All item IDs: speedups, resources, gems, materials |
| [OPCODES.md](OPCODES.md) | Complete opcode reference with payload structures |
| [CONNECTION.md](CONNECTION.md) | Auth flow, gateway, encryption, server constants |
| [HEROES.md](HEROES.md) | Hero IDs, selection packet, monsters |
| [GATHER_MARCH.md](GATHER_MARCH.md) | March/gather protocol (3 conflicting structures!) |
| [RESEARCH.md](RESEARCH.md) | Research opcodes, guild tech IDs |

## Verification Status

### PCAP Verified ✅ (confirmed with server response)
- **Train** (0x0CED, 19B) - types 1,2,4,8 all got 0x06C4 response
- **Enable View** (0x0CEB, 10B) - ARM64 confirmed
- **Encryption** (CMsgCodec) - cracked, roundtrip tested
- **Demolish** (0x009D, 12B) - ALL 30 outer slots mapped from isolated PCAPs
- **Gateway Auth** (0x000B, 79B) - login flow verified

### Got Server Response (needs more verification)
- **Build/Upgrade** (0x0CEF, 22B) - response received but payload structure has conflicts
- **Research** (0x0CEE, 12B or 19B) - response received but two size variants

### NOT Working ❌
- **Gather/March** (0x0CE8) - THREE conflicting payload structures (46B, 62B, 32+var)
- **Item Use** (0x0065) - no response in tests
- **Speedups** (0x06C7 etc.) - untested

### Known Data Issues ⚠
1. **BUILD payload**: commands.py vs game_ids.py have different byte layouts
2. **RESEARCH payload**: 12B vs 19B variants
3. **MARCH payload**: 3 completely different structures
4. **Troop Tier IDs** (101-404): from protocol.py but NOT PCAP verified
5. **test_live.py labels are WRONG**: says "Ranged=2" but PCAP says "Cavalry=2"

## Source Code
- Clean bot: `D:\CascadeProjects\claude\`
- Original bot: `D:\CascadeProjects\lords_bot\`
- Research lab: `D:\CascadeProjects\codex_lab\`

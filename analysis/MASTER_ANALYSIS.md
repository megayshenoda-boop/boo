# libgame.so - Complete Analysis Report
**Updated: 2026-04-04**

---

## 1. Binary Overview

| Property | Value |
|----------|-------|
| File | libgame.so (104,080,728 bytes / ~99MB) |
| Architecture | ARM64 (AArch64), Little Endian, stripped |
| Engine | Cocos2d-x |
| Compiler | Clang 19.0.1 (Android NDK r530567e) |
| Total Symbols | 168,346 |
| CMSG Types | 3,337 unique protocol messages |
| Opcodes Found | **1,714** (1,712 mapped to CMSG names) |
| Classes | 3,394 (from typeinfo) |
| JNI Functions | 77 |
| PLT Entries | 48,049 |
| Encode Callers | 32 (template instantiations) |
| SendData Callers | 11 |

### Sections
| Section | Address | Size |
|---------|---------|------|
| .text | 0x03250E80 | 43,562,076 (41.5MB) |
| .rodata | 0x0255B000 | 4,329,528 (4.1MB) |
| .data.rel.ro | 0x05C9BF00 | 6,355,264 |
| .got.plt | 0x062D6E20 | 384,400 |
| .plt | 0x05BDC3F0 | 769,808 |

---

## 2. Encryption (CMsgCodec) - ARM64 CONFIRMED

### Functions
| Function | Address | PLT Stub | Signature |
|----------|---------|----------|-----------|
| **CMsgCodec::Encode** | 0x04F97C24 | 0x05C6DBA0 | `Encode(uint8_t* pkt, uint32_t server_key)` |
| **CMsgCodec::Decode** | 0x04F97D40 | - | `Decode(uint8_t* pkt, uint32_t sk, uint16_t& opcode)` |

### Encryption Formula (CONFIRMED from ARM64 disassembly)
```
encrypted[i] = ((msg_byte * 17 + plaintext[i]) ^ sk_byte ^ TABLE[i % 7]) & 0xFF
```

ARM64 implementation detail:
- `*17` = `ADD W, W, W, LSL #4` (compiler optimization: x + x*16 = x*17)
- `%7` = multiply by magic 0x2493 + shifts (compiler integer division trick)
- Loop: bytes 8 through packet_length

### Decryption Formula (inverse)
```
plaintext[i] = ((encrypted[i] ^ sk_byte ^ TABLE[i % 7]) - msg_byte * 17) & 0xFF
```

Decode also does:
1. **SIMD checksum verification** using NEON vector add (32 bytes at a time!)
2. **Verify byte check**: `header[6] ^ msg_low == 0xB7`

### Constants
| Constant | Value | Location |
|----------|-------|----------|
| CMSG_TABLE | [0x58, 0xEF, 0xD7, 0x14, 0xA2, 0x3B, 0x9C] | 0x028B723A (.rodata) |
| Verify | 0xB7 | Immediate in code |
| CQ_secret | "CQ_secret" | 0x025C05F0 (.rodata) |
| Min packet | 9 bytes | Validated in Encode |

### Packet Header (CONFIRMED from ARM64)
```
Offset  Size  Field      Write Order in Encode
------  ----  -----      ---------------------
0-1     u16   length     Set before Encode call
2-3     u16   opcode     Set before Encode call
4       u8    checksum   strb w9, [x8, #4]  (sum of encrypted bytes)
5       u8    msg_low    strb w0, [x8, #5]
6       u8    verify     strb w10, [x8, #6] (msg_low ^ 0xB7)
7       u8    msg_high   strb w9, [x8, #7]  (msg >> 8)
8+      N     data       Encrypted payload
```

---

## 3. Network Architecture

### GoSocket (3 methods)
| Method | Address | PLT Stub | Notes |
|--------|---------|----------|-------|
| sendData | 0x04F95CA8 | 0x05C6DB00 | 11 callers, trivial send() wrapper |
| connectSocket | 0x04F95880 | - | Async TCP, SO_REUSEADDR, O_NONBLOCK |
| closeSocket | 0x04F95B00 | - | |

### Message System
- `MessageSubject::sendMsg` - template-based message dispatch
- `MessageSubject::registerListener<T>` - handler registration
- 32 Encode callers = 32 generic packet serialization templates

### Endpoints
```
Gateway:    54.93.167.80:5997
CDN:        http://static-cq.igg.com
Push:       http://snd-storage30.igg.com/push.php
H5 Games:   http://static-cq.igg.com/H5Games/web/index.html
Facebook:   https://graph.facebook.com/v5.0/me/...
Fallback IP: 52.80.53.87
```

---

## 4. Opcode Map (1,714 opcodes / 1,712 mapped)

### Key Opcodes (Bot-relevant)
| Opcode | Our Name | Real CMSG Name | Constructor |
|--------|----------|----------------|-------------|
| 0x0020 | GAME_LOGIN | CMSG_ENTER_GAME_RETURN | 0x0517C10C |
| 0x0021 | WORLD_ENTRY | CMSG_USERINFO_REQUEST | 0x0517C3B4 |
| 0x0038 | INIT_DATA | CMSG_EXTRA_ATTRIBUTE_INFO | 0x0505D838 |
| 0x0042 | HEARTBEAT | CMSG_KEEP_LIVE_TEST | 0x0527CA48 |
| 0x0834 | FORMATION | CMSG_GET_DOMINION_TRADE_NEW_REQUEST | 0x0504A9C8 |
| 0x0CE7 | CANCEL_MARCH | CMSG_BACK_DEFEND_NEW | 0x05139714 |
| **0x0CE8** | **START_MARCH** | **CMSG_START_MARCH_NEW** | 0x05212268 |
| 0x0CEB | ENABLE_VIEW | CMSG_ENABLE_VIEW_NEW | 0x051F53FC |
| 0x0CED | TRAIN | CMSG_SOLDIER_NORMAL_PRODUCE_REQUEST_NEW | 0x052C6740 |
| 0x0CEE | RESEARCH | CMSG_SCIENCE_NORMAL_STUDY_REQUEST_NEW | 0x052B4EFC |
| 0x0CEF | BUILD | CMSG_BUILDING_OPERAT_REQUEST_NEW | 0x04FCC358 |
| **0x1B8B** | **SESSION_PKT** | **CMSG_PASSWORD_CHECK_REQUEST** | 0x0527367C |

### Statistics
- C2S (REQUEST/SEND): 531 opcodes
- S2C (RETURN/RECV): 491 opcodes
- SYNC: 263 opcodes
- Other: 429 opcodes

### Full map: `findings/opcode_map_complete.md` (1,714 entries)

---

## 5. Game Systems (26 categories, 3,337 CMSG types)

| # | System | C2S | S2C | SYNC | Total |
|---|--------|-----|-----|------|-------|
| 1 | Events/Activities | 154 | 277 | 73 | 565 |
| 2 | War Events | 147 | 246 | 48 | 520 |
| 3 | Rewards | 120 | 166 | 12 | 364 |
| 4 | Alliance/Guild | 60 | 89 | 75 | 305 |
| 5 | Shop/Store | 45 | 101 | 36 | 204 |
| 6 | System/Core | 14 | 19 | 130 | 181 |
| 7 | Kingdom/Map | 29 | 48 | 47 | 153 |
| 8 | Chat/Social | 33 | 57 | 32 | 152 |
| 9 | Heroes/Familiars | 27 | 60 | 7 | 140 |
| 10 | Troops/Training | 42 | 53 | 6 | 120 |
| 11 | Combat/Battle | 22 | 37 | 22 | 111 |
| 12 | Items/Inventory | 26 | 55 | 8 | 102 |
| 13 | March/Movement | 14 | 24 | 21 | 87 |
| 14 | Arena/PvP | 22 | 28 | 15 | 74 |
| 15 | Buildings | 18 | 32 | 4 | 74 |

Full breakdown: `findings/game_systems.md`

---

## 6. Critical Discovery: 0x1B8B = PASSWORD_CHECK_REQUEST

The packet that causes disconnects (0x1B8B) is actually **CMSG_PASSWORD_CHECK_REQUEST** - NOT a simple session/heartbeat packet. This explains why the server disconnects when we send invalid data.

This packet likely requires:
- Some form of password hash or token
- Specific fields related to account verification
- Proper sequencing with other auth packets

Constructor at **0x0527367C** - needs deeper disassembly to find field layout.

---

## 7. CRITICAL CORRECTION: Previous False Positives

Scripts 09/10 (MOVZ scan) found opcode constants that were actually in **OpenSSL/libcurl** code statically linked in the binary, NOT in game protocol handlers.

Evidence: strings near those locations include `ssl/ssl_lib.c`, `NTLM`, `Digest`, `Basic`, `Bearer`, `Content-Type`, `Authorization`.

The REAL game functions were found via:
1. PLT stub tracing (CMsgCodec::Encode PLT at 0x05C6DBA0)
2. GOT.PLT slot resolution (Encode GOT at 0x0631FA00)
3. BL caller scanning (32 callers found)
4. MOVZ LSL#16 + STR pattern for constructors (1,714 opcodes)
5. Symbol proximity matching (1,712 names resolved)

---

## 8. Security Observations

### Protocol Weaknesses
1. **Weak encryption**: XOR + add*17 with 7-byte table - trivially reversible
2. **Hardcoded keys**: CMSG_TABLE and CQ_secret in .rodata
3. **No TLS** for game protocol (raw TCP)
4. **Predictable packets**: Fixed format allows replay/injection
5. **Server key from 0x0038**: Single field provides decode capability

### Interesting C2S Opcodes for Bot
```
CMSG_BUILDING_OPERAT_ONEKEY_REQUEST    - One-key building (speed up?)
CMSG_SOLDIER_GOLD_PRODUCE_REQUEST      - Gold troop production
CMSG_ACTIVITY_GAIN_REQUEST             - Claim activity rewards
CMSG_ACTIVITY_REWARD_INFO_REQUEST      - Check available rewards
CMSG_ITEM_USE_REQUEST                  - Use items
CMSG_ITEM_SELL_REQUEST                 - Sell items
CMSG_AUTO_JOIN_BUILDUP_OPEN_REQUEST    - Auto-join alliance help
CMSG_SELF_MARCH_QUEUE_REQUEST          - Check march queue
CMSG_QUERY_MARCH_ARMY_INFO             - Query march army details
CMSG_HERO_QUEUE_CHANGE_REQUEST         - Change hero lineup
CMSG_VIP_STORE_BUY_REQUEST             - VIP store purchase
```

---

## 9. Files Index

### Analysis Scripts (D:\CascadeProjects\analysis\)
| Script | Purpose |
|--------|---------|
| 01-04 | ELF overview, symbols, CMSG extraction, categorization |
| 05-06 | Deep binary scan, opcode map in .rodata |
| 07-08 | Dispatch table (was wrong - not main table) |
| 09-10 | MOVZ scan (found SSL false positives) |
| 11 | Game system categorization |
| 12 | CMsgCodec disassembly |
| 13 | String extraction |
| 14 | Handler deep analysis |
| 15 | **CMSG_TABLE cross-references (found real Encode/Decode)** |
| 16 | **PLT/BL caller tracing (found 32 Encode callers)** |
| 17 | **Opcode-to-CMSG mapping (1,712 mapped)** |

### Findings (D:\CascadeProjects\analysis\findings\)
| File | Content |
|------|---------|
| encryption_deep.md | Full ARM64 encode/decode disassembly analysis |
| game_systems.md | 26 game system categories with all CMSG messages |
| handler_analysis.md | Deep disassembly of key handlers |
| key_opcodes.md | Summary of known opcodes |
| opcode_map_complete.md | **Complete 1,714-opcode map with CMSG names** |
| real_handlers.md | CMSG_TABLE cross-references and corrections |
| strings_and_constants.md | All extracted strings, URLs, IPs, constants |

### Other
| File | Content |
|------|---------|
| FINDINGS.md | Full CMSG message list (3,337 types) |
| MASTER_ANALYSIS.md | This file |

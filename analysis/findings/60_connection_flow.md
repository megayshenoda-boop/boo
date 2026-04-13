# 60: Connection Flow - Complete Map (Bot vs Game Client)
# Date: 2026-04-09
# Purpose: Document the exact connection flow and identify gaps

---

## Phase 1: Gateway Authentication

```
Bot                          Gateway (54.93.167.80:5997)
 |                                |
 |  0x000B (79B)                  |  Gateway Auth
 |  - version=1                   |  - igg_id
 |  - token=XOR(access_key,CQ)   |  - world_id
 |  - platform=2 (android)       |  - game_id=0x3F00FF0E
 |------------------------------->|
 |                                |
 |  0x000C                        |  Gateway Redirect
 |  - game_ip                     |
 |  - game_port                   |
 |  - session_token (32B ASCII)   |
 |<-------------------------------|
 |                                |
 ~~~~ Gateway connection closed ~~~~
```

**Status: ✅ Working**

---

## Phase 2: Game Server Login

```
Bot                          Game Server (xxx.xxx.xxx.xxx:7001)
 |                                |
 |  0x001F (64B)                  |  Game Login
 |  - version=1                   |
 |  - igg_id                      |
 |  - session_token (32B)         |
 |  - marker=0x0E                 |
 |  - game_id=0x3F00FF0E          |
 |------------------------------->|
 |                                |
 |  0x0020 (payload[0]=1)         |  Login OK
 |<-------------------------------|
 |                                |
 |  0x0021 (21B)                  |  World Entry
 |  - igg_id                      |
 |  - marker=0x0E                 |
 |  - game_id=0x3F00FF0E          |
 |  - trailer=0xB0025C00          |
 |------------------------------->|
```

**Status: ✅ Working**

---

## Phase 3: Data Flood (Server → Client)

After 0x0021, server sends a massive flood of data packets:

```
Server → Client (typical 200+ packets, ~50-200KB):

0x0038  CASTLE_DATA (830B) ← CONTAINS SERVER KEY AT FIELD 0x4F!
0x0034  PLAYER_PROFILE
0x0064  ITEM_INFO (1348B) ← Item inventory
0x0097  BUILDING_INFO (610B) ← ⚠️ NOT PARSED BY BOT!
0x0098  WORKER_INFO ← ⚠️ NOT PARSED!
0x06C2  SOLDIER_INFO (112B) ← Troop counts
0x00AA  HERO_INFO (549B) ← Hero data
0x07E4  VIP_INFO
0x0033  SYN_ATTRIBUTE (x many) ← Resource updates
0x026D  CHAT_HISTORY (x many)
0x036C  (spam sync, x many)
0x0001  (unknown, x many)
0x1B8A  PASSWORD_INFO ← ⚠️ GATE BYTE FOR 0x1B8B!
... 100+ more packets ...
```

**Status: ⚠️ PARTIAL - Bot reads but ignores many important opcodes**

---

## Phase 4: Init Request Flood (Client → Server)

After receiving data, bot sends init requests:

```
Bot → Server (from PCAP sequence):

0x0840  (4B)     ← Unknown purpose, bot sends this
0x17D4  (4B)     ← Unknown purpose
0x0AF2  (4B)     ← Unknown purpose  
0x0245  (4B)     ← Unknown purpose
0x0834  (38B)    ← FORMATION_SET (hero lineup)
0x0709  (4B)     ← Unknown purpose
0x0A2C  (4B)     ← Unknown purpose
0x1357  (4B)     ← CUSTOMGIFTS_ACTION
0x170D  (4B)     ← Unknown purpose
```

**Status: ✅ Bot sends same sequence**

---

## Phase 5: PASSWORD_CHECK (THE PROBLEM ZONE)

### Game Client (from PCAP):
```
1. Server sends 0x1B8A with gate byte
2. IF gate[4] != 0:
   Client sends 0x1B8B (22B) with challenge response
3. IF gate[4] == 0:
   Client does NOT send 0x1B8B
```

### Bot (CURRENT WRONG BEHAVIOR):
```
1. Bot does NOT listen for 0x1B8A
2. Bot sends 0x1B8B DIRECTLY → Server disconnects!
```

### Fix:
```
1. Bot listens for 0x1B8A in _listener_loop
2. IF gate[4] == 0 → Do nothing (most accounts)
3. IF gate[4] != 0 → Send 0x1B8B with proper challenge response
4. IF no 0x1B8A received → Do nothing
```

**Status: ❌ BROKEN - Root cause of march failures**

---

## Phase 6: Normal Gameplay

After PASSWORD_CHECK (or skipping it), the game enters normal mode:

```
Bot → Server:
  0x0042  Heartbeat (every ~15s)
  0x0CE8  START_MARCH_NEW (encrypted)
  0x0CEB  ENABLE_VIEW_NEW (encrypted)
  0x0CED  TRAIN (encrypted)
  0x0CEF  BUILD (encrypted)
  0x0CEE  RESEARCH (encrypted)
  0x0065  ITEM_USE (plain)
  0x0284  SIGN_REQUEST (plain)
  ... more commands ...

Server → Client:
  0x0042  Heartbeat response
  0x0033  SYN_ATTRIBUTE (resource updates)
  0x00B8  MARCH_ACK
  0x0071  MARCH_STATE (march position sync)
  0x0070  MARCH_RECALL (march returned)
  0x006F  SYNC_MARCH (march data sync)
  0x0037  ERROR_STATUS (error codes)
  0x036C  (periodic sync)
  0x0002  (periodic)
```

**Status: ⚠️ PARTIAL - Missing parsers for 0x0070, 0x006F, 0x0097**

---

## Timeline Comparison (from FINDINGS.md)

```
PCAP (game client):
  T+0.0s   0x001F Login
  T+0.1s   0x0021 World Entry
  T+0.1-0.8s  Data Flood received
  T+0.8s   Init Request Flood sent
  T+1.0s   0x1B8A received (gate)
  T+1.2s   0x1B8B sent (if gate != 0)
  T+1.5s   Normal gameplay begins
  
Bot (current):
  T+0.0s   0x001F Login
  T+0.1s   0x0021 World Entry
  T+0.1-10s Data Flood received (variable!)
  T+10s    Init Request Flood sent
  T+10.3s  0x1B8B sent DIRECTLY → DISCONNECT!
```

### Key Differences:
1. **Timing**: Bot takes 10x longer to send init flood (waiting recv_all)
2. **0x1B8A**: Bot never receives/processes it
3. **0x1B8B**: Bot sends without gate check

---

## Missing Server Packet Handlers

| Opcode | Name | Why Needed | Difficulty |
|--------|------|------------|------------|
| 0x1B8A | PASSWORD_INFO | Gate for 0x1B8B | EASY |
| 0x0097 | BUILDING_INFO | Auto-upgrade | MEDIUM |
| 0x0098 | WORKER_INFO | Builder availability | EASY |
| 0x00BE | SCIENCE_INFO | Research status | MEDIUM |
| 0x003F | VIP_INFO | March slot count | EASY |
| 0x0070 | MARCH_RECALL | Free march slot | EASY |
| 0x006F | SYNC_MARCH | March position | MEDIUM |
| 0x0043 | SERVER_TIME | Timers | EASY |

---

## Recommendations

1. **IMMEDIATE**: Add 0x1B8A handler, remove proactive 0x1B8B send
2. **SHORT TERM**: Add missing parsers (0x0097, 0x0070, 0x0043)
3. **MEDIUM TERM**: Improve init flood timing to match PCAP
4. **LONG TERM**: Auto-reconnect with full state recovery

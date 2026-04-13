# Response Map

Generated from `lords_bot/test_results.json` and `lords_bot/round2_results.json`.

## High-level view

| Opcode | Current meaning | Evidence | Most seen responses | Notes |
|---|---|---|---|---|
| `0x0065` | ITEM_USE | heartbeat_only | 0x0042(8B) x1 | mixed or weak evidence |
| `0x009D` | OLD_BUILD | response_pattern_seen | 0x026D(116B) x2, 0x026D(130B) x1, 0x036C(4B) x1 | mixed or weak evidence |
| `0x00BF` | OLD_RESEARCH | heartbeat_only | 0x0042(8B) x1 | mixed or weak evidence |
| `0x06C3` | OLD_TRAIN | silent_or_unverified | - | mixed or weak evidence |
| `0x0CEB` | ENABLE_VIEW in current protocol.py | response_pattern_seen | 0x0076(166B) x1, 0x0077(222B) x1, 0x0078(490B) x1, 0x0095(74B) x1 | doc drift |
| `0x0CED` | TRAIN in current protocol.py | mixed_signals | 0x026D(151B) x1, 0x026D(126B) x1, 0x0042(8B) x1, 0x026D(117B) x1 | doc drift, mixed or weak evidence |
| `0x0CEE` | RESEARCH in current protocol.py | mixed_signals | 0x0042(8B) x1, 0x026D(124B) x1, 0x026D(171B) x1, 0x036C(4B) x1 | mixed or weak evidence |
| `0x0CEF` | BUILD in current protocol.py | mixed_signals | 0x026D(174B) x1, 0x026D(337B) x1, 0x0042(8B) x1, 0x026D(169B) x1 | mixed or weak evidence |
| `0x0CF9` | BUILD_FIX in current protocol.py | silent_or_unverified | - | mixed or weak evidence |

## Detailed notes

### 0x0065 - ITEM_USE

- Evidence level: `heartbeat_only`
- Sources: test_results.json
- Status counts: `{'NO_RESPONSE': 1}`
- Top responses:
  - `0x0042(8B)` x1
- Note: only heartbeat was observed; this is not meaningful confirmation for the action itself.
- Sample names:
  - `test_results.json` | `NO_RESPONSE` | ITEM_USE (old)

### 0x009D - OLD_BUILD

- Evidence level: `response_pattern_seen`
- Sources: test_results.json
- Status counts: `{'NO_RESPONSE': 1}`
- Top responses:
  - `0x026D(116B)` x2
  - `0x026D(130B)` x1
  - `0x036C(4B)` x1
- Sample names:
  - `test_results.json` | `NO_RESPONSE` | OLD_BUILD

### 0x00BF - OLD_RESEARCH

- Evidence level: `heartbeat_only`
- Sources: test_results.json
- Status counts: `{'NO_RESPONSE': 1}`
- Top responses:
  - `0x0042(8B)` x1
- Note: only heartbeat was observed; this is not meaningful confirmation for the action itself.
- Sample names:
  - `test_results.json` | `NO_RESPONSE` | OLD_RESEARCH

### 0x06C3 - OLD_TRAIN

- Evidence level: `silent_or_unverified`
- Sources: test_results.json
- Status counts: `{'NO_RESPONSE': 1}`
- Top responses: none
- Sample names:
  - `test_results.json` | `NO_RESPONSE` | OLD_TRAIN

### 0x0CEB - ENABLE_VIEW in current protocol.py

- Evidence level: `response_pattern_seen`
- Sources: test_results.json
- Status counts: `{'GOT_RESPONSE': 1}`
- Top responses:
  - `0x0076(166B)` x1
  - `0x0077(222B)` x1
  - `0x0078(490B)` x1
  - `0x0095(74B)` x1
  - `0x007A(0B)` x1
  - `0x0773(70B)` x1
- Note: this opcode is involved in documentation drift and must be checked against `protocol.py` first.
- Sample names:
  - `test_results.json` | `GOT_RESPONSE` | TRAIN troops (confirmed working)

### 0x0CED - TRAIN in current protocol.py

- Evidence level: `mixed_signals`
- Sources: test_results.json, round2_results.json
- Status counts: `{'GOT_RESPONSE': 1, 'NO_RESPONSE': 1, 'SILENT': 1, 'RESPONSE': 1}`
- Top responses:
  - `0x026D(151B)` x1
  - `0x026D(126B)` x1
  - `0x0042(8B)` x1
  - `0x026D(117B)` x1
- Note: this opcode is involved in documentation drift and must be checked against `protocol.py` first.
- Sample names:
  - `test_results.json` | `GOT_RESPONSE` | BUILD upgrade Embassy (type=3, slot=3)
  - `test_results.json` | `NO_RESPONSE` | BUILD upgrade Watchtower (type=7, slot=7)
  - `round2_results.json` | `SILENT` | TRAIN (Capstone: SOLDIER_PRODUCE) - 10B
  - `round2_results.json` | `RESPONSE` | TRAIN (19B alt payload)

### 0x0CEE - RESEARCH in current protocol.py

- Evidence level: `mixed_signals`
- Sources: test_results.json, round2_results.json
- Status counts: `{'GOT_RESPONSE': 1, 'NO_RESPONSE': 1, 'RESPONSE': 1}`
- Top responses:
  - `0x0042(8B)` x1
  - `0x026D(124B)` x1
  - `0x026D(171B)` x1
  - `0x036C(4B)` x1
- Sample names:
  - `test_results.json` | `GOT_RESPONSE` | RESEARCH (19B, same structure as BUILD)
  - `test_results.json` | `NO_RESPONSE` | RESEARCH (10B, train-like structure)
  - `round2_results.json` | `RESPONSE` | RESEARCH (10B train-like)

### 0x0CEF - BUILD in current protocol.py

- Evidence level: `mixed_signals`
- Sources: test_results.json, round2_results.json
- Status counts: `{'GOT_RESPONSE': 1, 'SILENT': 1, 'RESPONSE': 2}`
- Top responses:
  - `0x026D(174B)` x1
  - `0x026D(337B)` x1
  - `0x0042(8B)` x1
  - `0x026D(169B)` x1
- Sample names:
  - `test_results.json` | `GOT_RESPONSE` | UNKNOWN 0x0CEF (22B from PCAP)
  - `round2_results.json` | `SILENT` | BUILD Embassy (Capstone: BUILDING_OPERAT) - 19B
  - `round2_results.json` | `RESPONSE` | BUILD Embassy (22B PCAP format)
  - `round2_results.json` | `RESPONSE` | BUILD Watchtower (22B, slot 7)

### 0x0CF9 - BUILD_FIX in current protocol.py

- Evidence level: `silent_or_unverified`
- Sources: test_results.json, round2_results.json
- Status counts: `{'NO_RESPONSE': 1, 'SILENT': 1}`
- Top responses: none
- Sample names:
  - `test_results.json` | `NO_RESPONSE` | BUILD_FIX 0x0CF9 (same payload as BUILD)
  - `round2_results.json` | `SILENT` | BUILD_FIX 0x0CF9 (22B)

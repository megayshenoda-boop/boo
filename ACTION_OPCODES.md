# Action Opcodes Discovery - Capture Analysis

## User Actions Performed (in order):
1. Upgrade mine to level 8
2. Used speedup on building upgrade
3. Trained 480 infantry
4. Used speedup on training
5. Sent gather march for wood level 3

## NEW Client Opcodes Found (8 unique):

### Clear-text Actions:
| Opcode | Size | Payload (hex) | Decoded |
|--------|------|---------------|---------|
| 0x009D | 16B  | varies | Status query / UI navigation (14 instances) |
| 0x06C7 | 16B  | `01000000 72040000 01000000` | u32: {1, 1138, 1} - possible COLLECT/CONFIRM |
| 0x0323 | 15B  | `000200 c9000000 ce000000` | bytes:{0,2,0} + u32:{201, 206} - MARCH START? |
| 0x0002 | 4B   | (empty) | Sync/done signal |

### Encrypted Actions (0x0CE* family):
| Opcode | Size | Notes |
|--------|------|-------|
| 0x0CEF | 30B  | Appears 2x - likely BUILD UPGRADE + USE SPEEDUP (building) |
| 0x0CED | 27B  | Appears 1x - likely TRAIN TROOPS |
| 0x0CE8 | 58B  | Appears 1x - likely START GATHER MARCH |
| 0x0CEB | 18B  | Already seen in init - encrypted channel |

### 0x009D Variants:
```
10009d00 0c360000 00000080 ef7fbc00  - pre-action query
10009d00 0c350000 00000088 f27fbc00  - pre-action query  
10009d00 04370000 000000a0 ef7fbc00  - post-upgrade query
10009d00 09370035 00000000 00000001  - repeated 6x during upgrade
10009d00 11370074 04000008 00000000  - post-speedup query
10009d00 1137007c 04000001 00000000  - post-training query (2x)
```

## Key Finding: Action Encryption
The game encrypts critical action packets (build, train, gather) using the 0x0CE* opcode family.
Clear-text opcodes (0x06C7, 0x0323) may be secondary confirmations or simpler actions.

## Server Response Opcodes (NEW):
- 0x0076 (170B) - contains player name "ssssaaal", guild info - MARCH/TROOP UPDATE
- 0x0077 (244B) - contains timestamps, coordinates - MARCH QUEUE UPDATE  
- 0x0078 (810B) - contains troop counts, timestamps - FULL STATE UPDATE
- 0x007A (4B) - empty ack

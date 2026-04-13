# 59: Error Codes & Server Responses - Complete Reference
# Date: 2026-04-09
# Purpose: Map all known error codes from 0x0037 packets and game behavior

---

## 0x0037 ERROR_STATUS Packet Format

```
Offset  Size  Type   Description
------  ----  ----   -----------
0       4B    u32    error_code
4       4B    u32    param (context-specific)
8       4B    u32    zero/reserved
```
Total: 12 bytes

## Known Error Codes (from PCAP analysis + bot logs)

| Code | Hex | Meaning | Context | Severity |
|------|-----|---------|---------|----------|
| 0 | 0x00 | Success / OK | Generic | INFO |
| 1 | 0x01 | Operation failed | Generic | ERROR |
| 2 | 0x02 | Invalid parameter | Bad opcode/field | ERROR |
| 3 | 0x03 | Insufficient resources | Train/build/research | WARN |
| 5 | 0x05 | Not enough troops | March | WARN |
| 7 | 0x07 | Cooldown active | Action on cooldown | WARN |
| 10 | 0x0A | Queue full | Training/building queue full | WARN |
| 13 | 0x0D | Invalid target | March to invalid tile | ERROR |
| 22 | 0x16 | Timestamp error | Server time mismatch | ERROR |
| 38 | 0x26 | March slot busy | All march slots in use | WARN |
| 43 | 0x2B | Account error | Session/auth issue | CRITICAL |
| 100 | 0x64 | Unknown | Seen in PCAPs | UNKNOWN |

## Error Code → Bot Action Mapping

```python
ERROR_ACTIONS = {
    0:  "success",           # Continue normally
    1:  "retry_once",        # Generic fail, retry
    2:  "fix_params",        # Check packet format
    3:  "wait_resources",    # Wait for resources to accumulate
    5:  "reduce_troops",     # Send fewer troops
    7:  "wait_cooldown",     # Wait and retry later
    10: "wait_queue_free",   # Wait for queue slot
    13: "find_new_target",   # Search for different tile
    22: "sync_time",         # Resync server time
    38: "wait_march_slot",   # Wait for march to return
    43: "reconnect",         # Session expired, reconnect
}
```

## 0x00B8 MARCH_ACK Response Codes

| Byte[0] | Meaning | Bot Action |
|---------|---------|------------|
| 0x00 | March started OK | Continue, wait for 0x0071 |
| 0x01 | March failed (generic) | Log error, retry |
| 0x02 | Invalid coordinates | Find new target |
| 0x03 | No troops available | Check troop count |
| 0x05 | All march slots full | Wait for return |

## ErrorMessageManager (from libgame.so)

The game has `ErrorMessageManager` class at symbol `0x0269B4F1`.
It loads error strings from XML configs:
- `error_message.xml` (not extracted yet)
- Contains human-readable error messages for each code

## Server Disconnect Reasons

Based on analysis of bot disconnects:

| Scenario | Timeout | Cause |
|----------|---------|-------|
| Send 0x1B8B unsolicited | ~0.2s | Server rejects PASSWORD_CHECK |
| No heartbeat | ~60s | Server drops idle connection |
| Invalid packet length | ~0.1s | Server parser error |
| Invalid server_key | ~0.3s | Encryption mismatch |
| Gateway token expired | immediate | Re-login needed |

## Implementation Notes

### For game_state.py:
```python
ERROR_CODES = {
    0: "OK", 1: "FAILED", 2: "INVALID_PARAM", 3: "NOT_ENOUGH_RESOURCES",
    5: "NOT_ENOUGH_TROOPS", 7: "COOLDOWN", 10: "QUEUE_FULL",
    13: "INVALID_TARGET", 22: "TIME_ERROR", 38: "MARCH_SLOT_BUSY",
    43: "ACCOUNT_ERROR",
}

def _parse_error(self, payload):
    if len(payload) < 12: return
    err_code, param, _ = struct.unpack('<III', payload[0:12])
    self.last_error = (err_code, param)
    msg = ERROR_CODES.get(err_code, f"UNKNOWN_{err_code}")
    _log(f"ERROR: {msg} (code={err_code}, param={param})", level="WARN")
```

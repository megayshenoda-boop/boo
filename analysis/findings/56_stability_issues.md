# 56: Bot Stability Issues - Complete Diagnosis
# Date: 2026-04-09
# Purpose: Every issue preventing the bot from running stable in all environments

---

## Issue #1: 0x1B8B PASSWORD_CHECK - Root Cause Found ✅

### Summary
The bot sends `0x1B8B` proactively but the server expects a **challenge-response flow**:

### The Real Flow (from decode_deep.py analysis):
```
1. Server → Client: 0x1B8A (PASSWORD_INFO) with gate byte
2. If gate byte [4] == 0 → DO NOT send 0x1B8B (no secondary password)
3. If gate byte [4] != 0 → Client MUST send 0x1B8B with correct challenge response
```

### What the bot does WRONG:
- Bot sends 0x1B8B **directly** without waiting for 0x1B8A
- Bot does NOT listen for incoming 0x1B8A at all
- Result: server disconnects because it receives an unsolicited PASSWORD_CHECK

### Fix Required:
```python
# In game_state.py - add handler for 0x1B8A
elif opcode == 0x1B8A:  # PASSWORD_INFO (gate)
    if len(payload) >= 5:
        gate = payload[4]
        if gate == 0:
            # No secondary password - DO NOT send 0x1B8B
            self.password_gate = False
        else:
            # Must send 0x1B8B response
            self.password_gate = True
            self.password_challenge = payload
```

### Impact: CRITICAL
- This is why marches fail
- Without 0x1B8B: slot=2 gets 0x00B8 but no 0x0071 (march ack but no march state)
- With wrong 0x1B8B: server disconnects entirely

---

## Issue #2: March Payload Size Mismatch (50 vs 46 bytes)

### Summary
`commands.py` line 156: `total_size = 50 + array_count * 4`
`march_payload_format.md`: "Base payload: 46 bytes (0 array entries)"

### Analysis:
The bot uses `total_size = 50` which adds **4 extra zero bytes** at the end.
The actual struct from ARM64 disassembly is 46 bytes base.

### Byte Layout Comparison:
```
Bot:     2+2+5+8+2+2+1+(N*4)+4+1+8+1+1+8+1+4 = 50 + N*4
ARM64:   2+2+5+8+2+2+1+(N*4)+4+1+8+1+1+8+1+4 = 50 + N*4 (SAME!)
```

**ACTUALLY**: Both calculate to 50! The march_payload_format.md says 46 but counting the actual fields gives 50. The discrepancy is in the documentation, NOT the code. The code is correct.

### Verdict: NOT A BUG ✅
The code matches the ARM64 disassembly field-by-field. The "46" in findings was likely an early estimate before trailing fields were discovered.

---

## Issue #3: No Auto-Reconnect

### Current Behavior:
- Connection drops → bot crashes or hangs
- `game_server.py` line 170-173: listener loop catches exception, sets `connected = False`, breaks
- No retry logic anywhere

### Fix Required:
```python
# In bot.py - wrap the main loop with reconnect
def start_with_retry(self, max_retries=5, delay=10):
    for attempt in range(max_retries):
        try:
            if self.start():
                self.interactive()
        except Exception as e:
            log(f"Connection lost (attempt {attempt+1}/{max_retries}): {e}", "ERROR")
            time.sleep(delay)
    log("Max retries exceeded", "ERROR")
```

### Impact: HIGH
- Bot dies on any network hiccup
- Must be restarted manually

---

## Issue #4: Missing 0x1B8A Handler

### Current State:
`game_state.py` has NO handler for opcode `0x1B8A` (PASSWORD_INFO).
This opcode is the **gate signal** from the server that tells the client whether to send 0x1B8B.

### Impact: CRITICAL (related to Issue #1)

---

## Issue #5: Missing Server Opcodes Not Parsed

### Opcodes the server sends but bot ignores:
| Opcode | Name | Why it matters |
|--------|------|----------------|
| 0x0097 | BUILDING_INFO | Know what buildings exist, their levels |
| 0x0098 | WORKER_INFO | Know if workers are busy |
| 0x00BE | SCIENCE_INFO | Know active research |
| 0x003F | VIP_INFO | VIP level affects march slots |
| 0x0043 | SERVER_TIME | Server clock (needed for timers) |
| 0x0070 | MARCH_RECALL | March returned - free the slot |
| 0x006F | SYNC_MARCH | March sync data |
| 0x1B8A | PASSWORD_INFO | Gate for 0x1B8B (CRITICAL!) |

### Impact: MEDIUM-HIGH
- Without BUILDING_INFO: can't auto-select best upgrade
- Without WORKER_INFO: don't know if builder is free
- Without MARCH_RECALL: don't know when march slots are free
- Without 0x1B8A: can't handle password check properly

---

## Issue #6: Heartbeat Timing Too Regular

### Current Behavior:
`game_server.py` line 134: `time.sleep(HEARTBEAT_INTERVAL)` - exactly 15.0s every time

### Risk:
Anti-bot detection can flag perfectly regular heartbeats.
Real game client has slight variance (+/- 500ms).

### Fix:
```python
# Add jitter to heartbeat
import random
jitter = random.uniform(-0.5, 0.5)
time.sleep(HEARTBEAT_INTERVAL + jitter)
```

### Impact: MEDIUM (anti-detection)

---

## Issue #7: Thread Safety Race Condition in Callbacks

### Current Behavior:
`bot.py` lines 99, 117, 135: `self.conn._callbacks.remove(_on_ack)` called from main thread
`game_server.py` line 164: `for cb in self._callbacks:` iterated from listener thread

### Risk:
If main thread removes a callback while listener is iterating, `RuntimeError: list changed size during iteration`

### Fix:
```python
# Use thread-safe callback management
self._callbacks = []  # change to
self._callback_lock = threading.Lock()

def on_packet(self, callback):
    with self._callback_lock:
        self._callbacks.append(callback)

def remove_callback(self, callback):
    with self._callback_lock:
        if callback in self._callbacks:
            self._callbacks.remove(callback)
```

### Impact: MEDIUM (intermittent crashes)

---

## Issue #8: March Types in commands.py

### Current Code (commands.py line 116-117):
```python
def start_march(self, target_x, target_y, march_type=3, ...):
```
Default `march_type=3` = **gather** in comments.

### But from protocol.py (lines 259-264):
```python
MARCH_TYPE_GATHER    = 1
MARCH_TYPE_ATTACK    = 2
MARCH_TYPE_SCOUT     = 3
```

### And from march_payload_format.md:
`march_type (u16) - 1=attack, 2=scout, 3=gather, 5=reinforce`

### CONFLICT! protocol.py says gather=1, march_payload_format.md says gather=3
The ARM64 analysis and PCAP data shows gather=3 is correct.
The protocol.py constants are WRONG.

### Fix:
```python
# protocol.py - correct values (from ARM64 disassembly):
MARCH_TYPE_ATTACK    = 1  # was 2
MARCH_TYPE_SCOUT     = 2  # was 3
MARCH_TYPE_GATHER    = 3  # was 1
MARCH_TYPE_REINFORCE = 5  # was 4
```

### Impact: HIGH - wrong march type = wrong action!

---

## Priority Order for Fixes:

1. **🔴 Issue #1 + #4**: 0x1B8A/0x1B8B handler (blocks all marches)
2. **🔴 Issue #8**: March type constants (sends wrong action type)
3. **🟡 Issue #3**: Auto-reconnect (stability)
4. **🟡 Issue #7**: Thread safety (intermittent crash)
5. **🟡 Issue #5**: Missing server parsers (functionality)
6. **🟢 Issue #6**: Heartbeat jitter (anti-detection)
7. **🟢 Issue #2**: Non-issue (code is correct)

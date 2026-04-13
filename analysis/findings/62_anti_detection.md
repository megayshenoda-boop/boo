# 62: Anti-Detection & Connection Security Analysis
# Date: 2026-04-09
# Purpose: Every risk that could get the bot detected/banned

---

## Risk 1: Heartbeat Timing Pattern ⚠️ MEDIUM

### Current Behavior:
```python
# game_server.py line 134:
time.sleep(HEARTBEAT_INTERVAL)  # Exactly 15.0s every time
```

### Detection Signature:
Perfect 15.000s intervals → obvious bot signature.
Real game client: 14.5-15.5s with slight jitter.

### Fix:
```python
import random
jitter = random.uniform(-0.5, 0.5)
time.sleep(HEARTBEAT_INTERVAL + jitter)
```

### Risk Level: MEDIUM
- Server-side timing analysis can flag this
- Easy fix, should be done immediately

---

## Risk 2: User-Agent String ⚠️ LOW

### Current Value:
```python
# config.py line 30:
USER_AGENT = f"{GAME_ID}/6.3.0 Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G9880 Build/N2G47H)"
```

### Issues:
1. Game version `6.3.0` may be outdated (server could reject old versions)
2. Device model `SM-G9880` is specific - if flagged, it's linked
3. Build `N2G47H` corresponds to Android 7.1.2 (old)

### Recommendation:
- Update version number to match current game version
- Use a common device (SM-G991B = Galaxy S21, more common)
- Or better: extract from real device via ADB

---

## Risk 3: Packet Timing After Login ⚠️ HIGH

### Current Behavior:
```python
# game_server.py:
# Bot sends 0x001F, waits for 0x0020, sends 0x0021
# Then recv_all_packets(timeout=10) - blocks for UP TO 10 seconds
# Then sends init flood requests
```

### VS Real Game Client (from PCAP):
```
T+0.000s  0x001F
T+0.100s  0x0020 received
T+0.110s  0x0021 sent
T+0.200s  First data packet received
T+0.800s  Init flood sent (0x0840, 0x17D4, etc.)
T+1.200s  0x1B8B sent
```

### Problem:
Bot waits full 10s timeout on recv_all_packets before sending init.
Game client sends init while STILL receiving data flood.

### Fix (non-blocking init flood):
```python
# After 0x0021, start listener thread immediately
# Send init requests after brief delay (0.5-1s), not after full timeout
threading.Thread(target=self._listener_loop, daemon=True).start()
time.sleep(0.8)  # Match PCAP timing
self._send_init_flood()  # 0x0840, 0x17D4, etc.
```

---

## Risk 4: Missing Client-Side Opcodes ⚠️ MEDIUM

### Opcodes the Game Client sends that Bot does NOT:

| Opcode | Timing | Purpose | Risk if Missing |
|--------|--------|---------|-----------------|
| 0x0042 | Periodic | Heartbeat | Server disconnect |
| 0x0840 | On login | Unknown init | Server flagging |
| 0x17D4 | On login | Unknown init | Server flagging |
| 0x0AF2 | On login | Unknown init | Server flagging |
| 0x0245 | On login | Unknown init | Server flagging |
| 0x0834 | On login | Formation set | Server flagging |
| 0x0709 | On login | Unknown init | Server flagging |
| 0x0A2C | On login | Unknown init | Server flagging |
| 0x099D | On login | Sub-requests | Server flagging |

### Bot init flood (game_server.py line 96-99):
```python
for op in [0x0840, 0x17D4, 0x0709, 0x0674, 0x0767, 0x0769]:
    self.gs_sock.sendall(build_packet(op))
for sub_id in [0x0193, 0x0198, 0x019D]:
    self.gs_sock.sendall(build_packet(0x099D, struct.pack('<I', sub_id)))
```

### MISSING from bot init:
- `0x0AF2` ← Present in PCAP, missing from bot
- `0x0245` ← Present in PCAP, missing from bot
- `0x0834` ← Present in PCAP (formation), BOT sends but later
- `0x0A2C` ← Present in PCAP, missing from bot
- `0x1357` ← Present in PCAP, missing from bot
- `0x170D` ← Present in PCAP, missing from bot

### Fix:
```python
# Complete init flood matching PCAP sequence:
INIT_FLOOD_SEQUENCE = [
    (0x0840, b''),
    (0x17D4, b''),
    (0x0AF2, b''),
    (0x0245, b''),
    (0x0834, FORMATION_DATA),  # 38 bytes
    (0x0709, b''),
    (0x0A2C, b''),
    (0x1357, struct.pack('<I', 2)),
    (0x170D, struct.pack('<I', 2)),
]
```

---

## Risk 5: No Response to Server Pings ⚠️ LOW

### From PCAP:
Server sends `0x0043` (SERVER_TIME) periodically.
Game client responds to `0x0043` with its own `0x0043`.
Bot: DOES NOT respond to `0x0043`.

### Fix:
```python
# In _listener_loop, after receiving 0x0043:
if opcode == 0x0043:
    # Echo back server time as response
    self.send(build_packet(0x0043, payload))
```

---

## Risk 6: Credential Exposure 🔴 HIGH

### Current config.py:
```python
EMAIL = os.environ.get("IGG_EMAIL", "hdadhybat@gmail.com")
PASSWORD = os.environ.get("IGG_PASSWORD", "AS123456")
STORED_ACCESS_KEY = os.environ.get("IGG_ACCESS_KEY", "63f22dbfb60fae3ae3d7671491329518")
```

### Problem:
Real email, password, and access key are HARDCODED as defaults!
Anyone who sees this file has full account access.

### Fix:
```python
EMAIL = os.environ.get("IGG_EMAIL", "")
PASSWORD = os.environ.get("IGG_PASSWORD", "")
STORED_ACCESS_KEY = os.environ.get("IGG_ACCESS_KEY", "")
```
And add a startup check:
```python
if not EMAIL or not PASSWORD:
    print("ERROR: Set IGG_EMAIL and IGG_PASSWORD environment variables!")
    sys.exit(1)
```

---

## Risk 7: Thread Safety ⚠️ MEDIUM

### Race Condition in Callbacks:
```python
# game_server.py line 164 (listener thread):
for cb in self._callbacks:    # iterating
    cb(opcode, payload)

# bot.py (main thread):
self.conn._callbacks.remove(_on_ack)  # modifying during iteration!
```

### Fix:
```python
self._callback_lock = threading.Lock()

def on_packet(self, callback):
    with self._callback_lock:
        self._callbacks.append(callback)

# In listener loop:
with self._callback_lock:
    cbs = list(self._callbacks)  # copy under lock
for cb in cbs:  # iterate copy
    cb(opcode, payload)
```

---

## Risk Summary

| # | Risk | Severity | Difficulty | Status |
|---|------|----------|------------|--------|
| 1 | Heartbeat jitter | MEDIUM | EASY | Not fixed |
| 2 | User-Agent outdated | LOW | EASY | Not fixed |
| 3 | Login timing | HIGH | MEDIUM | Not fixed |
| 4 | Missing init opcodes | MEDIUM | EASY | Partially fixed |
| 5 | No 0x0043 response | LOW | EASY | Not fixed |
| 6 | Credential exposure | HIGH | EASY | Not fixed |
| 7 | Thread safety | MEDIUM | EASY | Not fixed |

## Priority Fix Order:
1. 🔴 Credential exposure (security!)
2. 🔴 Login timing (detection risk)
3. 🟡 Missing init opcodes (detection risk)
4. 🟡 Thread safety (stability)
5. 🟡 Heartbeat jitter (detection risk)
6. 🟢 0x0043 response (low risk)
7. 🟢 User-Agent (low risk)

# 61: Missing Server Parsers - Implementation Guide
# Date: 2026-04-09
# Purpose: Exact code for parsing server packets the bot currently ignores

---

## Parser 1: 0x1B8A - PASSWORD_INFO (CRITICAL)

From decode_deep.py analysis, this is the gate signal:

```python
# In game_state.py - add to __init__:
self.password_gate = None       # None=not received, False=no pw, True=need pw
self.password_challenge = None  # Raw challenge from server

# Add handler in update():
elif opcode == 0x1B8A:
    self._parse_password_info(payload)

# Add parser:
def _parse_password_info(self, payload):
    """Parse PASSWORD_INFO (0x1B8A): gate signal for 0x1B8B.
    From decode_deep.py: payload[4] = gate byte.
    gate=0 → no secondary password, do NOT send 0x1B8B
    gate!=0 → must send 0x1B8B with challenge response
    """
    if len(payload) >= 5:
        gate = payload[4]
        if gate == 0:
            self.password_gate = False
            _log("PASSWORD_INFO: gate=0 (no secondary password)")
        else:
            self.password_gate = True
            self.password_challenge = payload
            _log(f"PASSWORD_INFO: gate={gate} (secondary password required!)", "WARN")
    else:
        self.password_gate = False
        _log(f"PASSWORD_INFO: short payload ({len(payload)}B), assuming no password")
```

---

## Parser 2: 0x0097 - BUILDING_INFO

From pcap_analysis.md and DISCOVERIES.md:
```
BUILDING_INFO (0x0097): u16 count + 19B entries
Entry: u16 slot, u16 type, u16 level, 13B extra
```

```python
# In game_state.py:
# __init__:
self.buildings = {}  # {slot_id: {'type': int, 'level': int, 'raw': bytes}}

# Handler:
elif opcode == 0x0097:
    self._parse_buildings(payload)

# Parser:
def _parse_buildings(self, payload):
    """Parse BUILDING_INFO (0x0097): u16 count + 19B entries.
    Each entry: u16 slot + u16 type + u16 level + 13B extra.
    """
    if len(payload) < 2:
        return
    count = struct.unpack('<H', payload[0:2])[0]
    pos = 2
    entry_size = 19
    for _ in range(count):
        if pos + entry_size > len(payload):
            break
        slot = struct.unpack('<H', payload[pos:pos+2])[0]
        btype = struct.unpack('<H', payload[pos+2:pos+4])[0]
        level = struct.unpack('<H', payload[pos+4:pos+6])[0]
        self.buildings[slot] = {
            'type': btype,
            'level': level,
            'raw': payload[pos:pos+entry_size],
        }
        pos += entry_size
    _log(f"BUILDING_INFO: {count} buildings parsed")
```

---

## Parser 3: 0x0043 - SERVER_TIME

```python
# In game_state.py:
# __init__:
self.server_time = 0

# Handler:
elif opcode == 0x0043:
    self._parse_server_time(payload)

# Parser:
def _parse_server_time(self, payload):
    """Parse SERVER_TIME (0x0043): u32 timestamp."""
    if len(payload) >= 4:
        self.server_time = struct.unpack('<I', payload[0:4])[0]
```

---

## Parser 4: 0x0070 - MARCH_RECALL

```python
# Handler:
elif opcode == 0x0070:
    self._parse_march_recall(payload)

# Parser:
def _parse_march_recall(self, payload):
    """Parse MARCH_RECALL (0x0070): march returned.
    Clean up the march from active marches dict.
    """
    if len(payload) >= 4:
        march_id = struct.unpack('<I', payload[0:4])[0]
        if march_id in self.marches:
            del self.marches[march_id]
            _log(f"MARCH_RECALL: march #{march_id} returned (freed slot)")
        else:
            _log(f"MARCH_RECALL: march #{march_id} (was not tracked)")
```

---

## Parser 5: 0x003F - VIP_INFO

```python
# Handler:
elif opcode == 0x003F:
    self._parse_vip_info(payload)

# Parser:
def _parse_vip_info(self, payload):
    """Parse VIP_INFO (0x003F): VIP level and march slots."""
    if len(payload) >= 2:
        self.vip_level = struct.unpack('<H', payload[0:2])[0]
        _log(f"VIP_INFO: level={self.vip_level}")
```

---

## Parser 6: 0x006F - SYNC_MARCH

```python
# Handler:
elif opcode == 0x006F:
    self._parse_sync_march(payload)

# Parser:
def _parse_sync_march(self, payload):
    """Parse SYNC_MARCH (0x006F): update march position/status."""
    if len(payload) >= 4:
        march_id = struct.unpack('<I', payload[0:4])[0]
        if march_id in self.marches:
            self.marches[march_id]['last_sync'] = time.time()
            self.marches[march_id]['sync_data'] = payload
        else:
            self.marches[march_id] = {
                'id': march_id,
                'last_sync': time.time(),
                'sync_data': payload,
            }
```

---

## Summary: What needs to change in game_state.py

### New __init__ attributes:
```python
self.password_gate = None
self.password_challenge = None
self.buildings = {}    # was list, change to dict
self.server_time = 0
```

### New opcode handlers (in update()):
```python
elif opcode == 0x1B8A:
    self._parse_password_info(payload)
elif opcode == 0x0097:
    self._parse_buildings(payload)
elif opcode == 0x0043:
    self._parse_server_time(payload)
elif opcode == 0x0070:
    self._parse_march_recall(payload)
elif opcode == 0x003F:
    self._parse_vip_info(payload)
elif opcode == 0x006F:
    self._parse_sync_march(payload)
```

### Updated summary():
```python
if self.buildings:
    lines.append(f"  Buildings: {len(self.buildings)}")
    for slot, info in sorted(self.buildings.items()):
        lines.append(f"    Slot {slot}: type={info['type']} level={info['level']}")
if self.server_time:
    lines.append(f"  Server time: {self.server_time}")
if self.password_gate is not None:
    lines.append(f"  Password gate: {'REQUIRED' if self.password_gate else 'not needed'}")
```

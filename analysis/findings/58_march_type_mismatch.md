# 58: March Type Constants - CRITICAL MISMATCH FOUND
# Date: 2026-04-09
# Purpose: Document the march_type value conflict between bot code and test scripts

---

## The Problem

There are THREE different march_type value systems in the codebase:

### 1. protocol.py constants (unused by commands.py!):
```python
MARCH_TYPE_GATHER    = 1
MARCH_TYPE_ATTACK    = 2
MARCH_TYPE_SCOUT     = 3
MARCH_TYPE_REINFORCE = 4
MARCH_TYPE_RALLY     = 5
MARCH_TYPE_DEFEND    = 6
```

### 2. commands.py start_march() comments & defaults:
```python
# march_type: 1=attack, 2=scout, 3=gather, 5=reinforce
def start_march(self, ..., march_type=3, ...):   # default 3
def gather(self, ...):    march_type=3
def attack(self, ...):    march_type=1
def scout(self, ...):     march_type=2
```

### 3. ALL test_gather_v*.py scripts (from PCAP analysis):
```python
MARCH_TYPE = 0x1749   # = 5961 decimal
# test_gather_clean.py uses 0x174A for wheat level 2
```

## Analysis

`0x1749` is NOT a simple enum! It's a **composite value** from the game client:
- `0x1749` hex = `5961` decimal
- `0x174A` hex = `5962` decimal (wheat level 2)
- These are likely `resource_level << 8 | base_march_type` or similar composite

### Possible decoding:
```
0x1749:
  High byte: 0x17 = 23
  Low byte:  0x49 = 73
  
OR maybe it's a tile/resource type ID, not a march type at all!
```

### From verify_layout.py:
```python
# PCAP march_type = 0x1749 (gather)
# If we decode with layout2 (offset shift), march_type = 0xDEFC (nonsense)
```

This confirms that `0x1749` is the correct value seen in PCAPs for gather marches.

## Impact

| Component | Uses | Value | Status |
|-----------|------|-------|--------|
| protocol.py | Not used anywhere | 1-6 | ❌ WRONG |
| commands.py gather() | Called by bot interactively | 3 | ❌ WRONG |
| test_gather_v*.py | All 16+ test scripts | 0x1749 | ✅ CORRECT (from PCAP) |
| commands.py attack() | Called by bot | 1 | ❓ UNKNOWN (no PCAP verified) |

## Root Cause

`protocol.py` defines simple enum constants (1-6) that were GUESSED.
The actual game uses composite march_type values like `0x1749`.
`commands.py` references the wrong constants.
**Test scripts found the correct value from PCAP** but this was never merged back into `commands.py`.

## Fix Required

### Option A: Update commands.py to use PCAP-verified values
```python
# In commands.py gather():
def gather(self, target_x, target_y, ...):
    return self.start_march(
        target_x, target_y, 
        march_type=0x1749,  # PCAP-verified gather type
        ...
    )
```

### Option B: Create proper march_type mapping
```python
# In protocol.py - from PCAP analysis:
MARCH_TYPE_GATHER_FOOD    = 0x1749  # Food tiles
MARCH_TYPE_GATHER_WHEAT2  = 0x174A  # Wheat level 2
# Attack/scout values need PCAP verification
```

### Immediate Action:
1. Fix `commands.py gather()` to use `0x1749` instead of `3`
2. Mark `protocol.py` MARCH_TYPE_* as UNVERIFIED
3. Capture PCAPs for attack/scout marches to get their real values

---

## Broader Lesson

This is a pattern of "analysis found truth, but bot code still uses guesses":
- The answer (0x1749) exists in 16+ test files
- But the main bot code (commands.py) never got updated
- protocol.py constants are still the original guesses

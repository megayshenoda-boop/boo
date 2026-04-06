#!/usr/bin/env python3
"""
34_missing_opcodes.py - Find opcodes for CMSGs not in constructor map
=====================================================================
0x0CED (TRAIN), 0x0CEE (RESEARCH), 0x0CEF (BUILD), 0x1B8B (PASSWORD)
These use the generic CMSG base class with opcode set externally.

Also: Find OneClickAccelerate, speedup, and alliance help opcodes.
"""
import struct, re, sys
sys.path.insert(0, r'D:\CascadeProjects\claude')

LIBGAME = r"D:\CascadeProjects\libgame.so"
with open(LIBGAME, "rb") as f:
    data = f.read()

DYNSTR_OFF = 0x682A10
DYNSYM_OFF = 0x2F8
DYNSYM_SIZE = 0x682758
RODATA_OFF = 0x255B000
RODATA_SIZE = 4329528
rodata = data[RODATA_OFF:RODATA_OFF + RODATA_SIZE]

# 1. Search for OneClickAccelerate
print("=== OneClickAccelerate ===")
for m in re.finditer(rb'OneClick[A-Za-z_]+', data[DYNSTR_OFF:DYNSTR_OFF+0x200000]):
    name = m.group().decode('ascii')
    if len(name) > 10 and len(name) < 100:
        print(f"  dynstr: {name}")

for m in re.finditer(rb'OneClick[A-Za-z_]+', rodata):
    name = m.group().decode('ascii')
    if len(name) > 10 and len(name) < 100:
        print(f"  rodata: {name}")

# 2. Search for speed-up related CMSGs
print("\n=== Speed-up CMSGs ===")
for m in re.finditer(rb'CMSG_[A-Z_]*(?:SPEED|ACCELER|INSTANT|SPEEDUP)[A-Z_]*', data[DYNSTR_OFF:DYNSTR_OFF+0x200000]):
    print(f"  {m.group().decode('ascii')}")

# 3. Search for help-related CMSGs
print("\n=== Alliance Help CMSGs ===")
for m in re.finditer(rb'CMSG_[A-Z_]*(?:HELP|ASSIST|DONATE)[A-Z_]*(?:C1Ev|8packData|7getData)', data[DYNSTR_OFF:DYNSTR_OFF+0x200000]):
    name = m.group().decode('ascii')
    if 'C1Ev' in name:
        print(f"  [ctor] {name}")
    elif 'packData' in name:
        print(f"  [send] {name}")
    elif 'getData' in name:
        print(f"  [recv] {name}")

# 4. Search for auto-related features
print("\n=== Auto/Automation Features ===")
for m in re.finditer(rb'(?:auto|Auto|AUTO)[A-Za-z_]{3,40}', rodata):
    name = m.group().decode('ascii')
    if len(name) > 5 and len(name) < 60 and 'NSt6' not in name:
        print(f"  {name}")

# 5. Find where 0x0CED, 0x0CEE, 0x0CEF constants appear
print("\n=== Opcode Constants in .rodata ===")
for opcode, name in [(0x0CED, 'TRAIN'), (0x0CEE, 'RESEARCH'), (0x0CEF, 'BUILD'),
                      (0x1B8B, 'PASSWORD_CHECK'), (0x0CE8, 'START_MARCH')]:
    # Search for u16 value in .rodata
    found = False
    le_bytes = struct.pack('<H', opcode)
    # Also search in dynstr for the hex value
    hex_str = f"0x{opcode:04X}".encode()
    hex_str2 = f"0x{opcode:04x}".encode()
    for m in re.finditer(re.escape(hex_str) + b'|' + re.escape(hex_str2), rodata):
        ctx_start = max(0, m.start() - 30)
        while ctx_start > 0 and rodata[ctx_start-1] != 0: ctx_start -= 1
        ctx_end = min(len(rodata), m.end() + 30)
        while ctx_end < len(rodata) and rodata[ctx_end] != 0: ctx_end += 1
        ctx = rodata[ctx_start:ctx_end].decode('ascii', errors='replace')
        print(f"  {name}: found '{ctx}'")
        found = True
    if not found:
        print(f"  {name} (0x{opcode:04X}): not found as string in .rodata")

# 6. Find SHIELD/PEACE/BUBBLE
print("\n=== Peace Shield / War Shield CMSGs ===")
for m in re.finditer(rb'CMSG_[A-Z_]*(?:SHIELD|PEACE|PROTECT|BUBBLE)[A-Z_]*(?:C1Ev|8packData)', data[DYNSTR_OFF:DYNSTR_OFF+0x200000]):
    print(f"  {m.group().decode('ascii')}")

# 7. Find TELEPORT/RELOCATE
print("\n=== Teleport/Relocate CMSGs ===")
for m in re.finditer(rb'CMSG_[A-Z_]*(?:TELEPORT|RELOCAT|RANDOM_MOVE|MIGRATE)[A-Z_]*(?:C1Ev|8packData)', data[DYNSTR_OFF:DYNSTR_OFF+0x200000]):
    print(f"  {m.group().decode('ascii')}")

# 8. Find VIEW/SCOUT
print("\n=== View/Scout CMSGs ===")
for m in re.finditer(rb'CMSG_[A-Z_]*(?:SCOUT|VIEW|LOOK)[A-Z_]*(?:C1Ev|8packData)', data[DYNSTR_OFF:DYNSTR_OFF+0x200000]):
    print(f"  {m.group().decode('ascii')}")

# 9. Recall march
print("\n=== Recall/Cancel March ===")
for m in re.finditer(rb'CMSG_[A-Z_]*(?:RECALL|CANCEL_MARCH|STOP_MARCH|RETURN_MARCH)[A-Z_]*(?:C1Ev|8packData)', data[DYNSTR_OFF:DYNSTR_OFF+0x200000]):
    print(f"  {m.group().decode('ascii')}")

# 10. Find treasure/chest opening
print("\n=== Treasure/Chest ===")
for m in re.finditer(rb'CMSG_[A-Z_]*(?:TREASURE|CHEST|OPEN_BOX|LOOT)[A-Z_]*(?:C1Ev|8packData)', data[DYNSTR_OFF:DYNSTR_OFF+0x200000]):
    print(f"  {m.group().decode('ascii')}")

# 11. VIP-related
print("\n=== VIP ===")
for m in re.finditer(rb'CMSG_[A-Z_]*VIP[A-Z_]*(?:C1Ev|8packData)', data[DYNSTR_OFF:DYNSTR_OFF+0x200000]):
    print(f"  {m.group().decode('ascii')}")

# 12. Quest/Task completion
print("\n=== Quest/Task ===")
for m in re.finditer(rb'CMSG_[A-Z_]*(?:QUEST|TASK|MISSION)[A-Z_]*(?:C1Ev|8packData)', data[DYNSTR_OFF:DYNSTR_OFF+0x200000]):
    name = m.group().decode('ascii')
    if 'CHAMPIONSHIP' not in name:
        print(f"  {name}")

print("\n=== DONE ===")

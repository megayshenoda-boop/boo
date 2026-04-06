#!/usr/bin/env python3
"""
31_packdata_analysis.py - Disassemble packData for key bot-useful CMSGs
=======================================================================
Find the actual packet format for:
- CMSG_RECEIVE_REWARD_REQUEST (collect rewards)
- CMSG_ITEM_USE (use items/speedups)
- CMSG_RECEIVE_SIGN_ACTIVITY (daily sign-in)
- CMSG_RECEIVE_FIRST_BIND_REWARD
- CMSG_LUCKY_SHOP_SCRATCH_CARD
- CMSG_DAY_REFRESH_REQUEST
- CMSG_SIGN_REQUEST
- CMSG_ACTIVEGIFTS_ACTION_REQUEST
- CMSG_NEW_ONLINE_REWARD_REQUEST
- CMSG_CITY_BUFF_USE
- CMSG_DESERT_TRADE_START_MARCH_REQUEST
"""
import struct, re, sys
sys.path.insert(0, r'D:\CascadeProjects\claude')
from capstone import *

LIBGAME = r"D:\CascadeProjects\libgame.so"
with open(LIBGAME, "rb") as f:
    data = f.read()

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

DYNSTR_OFF = 0x682A10
DYNSYM_OFF = 0x2F8
DYNSYM_SIZE = 0x682758

out = []
def p(msg):
    out.append(msg)
    try: print(msg)
    except: print(msg.encode('ascii','replace').decode())

def find_function(name_pattern):
    """Find function address from .dynsym by name pattern."""
    results = []
    pos = DYNSYM_OFF
    while pos + 24 <= DYNSYM_OFF + DYNSYM_SIZE:
        st_name = struct.unpack('<I', data[pos:pos+4])[0]
        st_info = data[pos+4]
        st_value = struct.unpack('<Q', data[pos+8:pos+16])[0]
        st_size = struct.unpack('<Q', data[pos+16:pos+24])[0]
        if st_name > 0 and st_name < 0x200000 and st_value > 0:
            name_end = data.index(b'\x00', DYNSTR_OFF + st_name)
            name = data[DYNSTR_OFF + st_name:name_end].decode('ascii', errors='replace')
            if name_pattern in name and '8packData' in name:
                results.append((name, st_value, st_size))
        pos += 24
    return results

def disasm_packdata(addr, max_bytes=800):
    """Disassemble packData function and extract field writes."""
    code = data[addr:addr + max_bytes]
    insns = list(md.disasm(code, addr))

    fields = []  # (offset, size, description)
    writes = []  # Raw write instructions
    bl_calls = []  # Function calls

    for i, insn in enumerate(insns):
        # Stop at ret
        if insn.mnemonic == 'ret' and insn.address > addr + 20:
            break

        # Track BL calls to CIStream methods
        if insn.mnemonic == 'bl':
            bl_calls.append((insn.address, insn.op_str))

        # Track struct reads from this pointer (x19, x20, x21 etc)
        if insn.mnemonic in ('ldrb', 'ldrh', 'ldr', 'ldrsb', 'ldrsh', 'ldrsw'):
            if '#' in insn.op_str:
                parts = insn.op_str.split('#')
                offset_str = parts[-1].rstrip(']').rstrip('!')
                try:
                    offset = int(offset_str, 0)
                    sizes = {'ldrb': 1, 'ldrsb': 1, 'ldrh': 2, 'ldrsh': 2, 'ldr': 4, 'ldrsw': 4}
                    size = sizes.get(insn.mnemonic, 4)
                    # Check if loading from x register (8 bytes)
                    if insn.mnemonic == 'ldr' and insn.op_str.split(',')[0].strip().startswith('x'):
                        size = 8
                    writes.append((insn.address, insn.mnemonic, offset, size, insn.op_str))
                except: pass

    return insns, writes, bl_calls

# ═══════════════════════════════════════════════════════════════
# Find and analyze key CMSGs
# ═══════════════════════════════════════════════════════════════
targets = [
    'CMSG_START_MARCH_NEW',
    'CMSG_ITEM_USE',
    'CMSG_RECEIVE_REWARD_REQUEST',
    'CMSG_RECEIVE_REWARD_BATCH_REQUEST',
    'CMSG_RECEIVE_SIGN_ACTIVITY',
    'CMSG_SIGN_REQUEST',
    'CMSG_DAY_REFRESH_REQUEST',
    'CMSG_NEW_ONLINE_REWARD_REQUEST',
    'CMSG_ACTIVEGIFTS_ACTION_REQUEST',
    'CMSG_CITY_BUFF_USE',
    'CMSG_CITY_BUFF_GET_USE',
    'CMSG_LUCKY_SHOP_SCRATCH_CARD',
    'CMSG_RECEIVE_FIRST_BIND_REWARD',
    'CMSG_DESERT_TRADE_START_MARCH_REQUEST',
    'CMSG_OUTFIRE_REQUEST',
    'CMSG_HERO_SOLDIER_RECRUIT_REQUEST',
    'CMSG_DAMAGE_HELP',
    'CMSG_DAMAGE_BUY',
    'CMSG_ACHIEVEMENT_RECEIVE_REWARD_REQUEST',
    'CMSG_CONTINUITY_GIFTPACK_ACTION_REQUEST',
    'CMSG_RECEIVE_LUXURY_REWARD',
    'CMSG_RECEIVE_ACCUMULATION_REWARD_REQUEST',
    'CMSG_CAMEL_SHOP_BUY_REQUEST',
    'CMSG_EVERY_DAY_GIFTPACK_REWARD_REQUEST',
    'CMSG_MONTH_REFRESH_REQUEST',
    'CMSG_APPEND_SIGN_REQUEST',
    'CMSG_ARENA_BUY_TIMES_REQUEST',
    'CMSG_BUY_MOBILIZATION_TASK_TIMES_REQUEST',
    'CMSG_POWER_TASK_REWARD_REQUEST',
    'CMSG_SERVER_MISSION_RECEIVE_REQUEST',
    'CMSG_RANDOM_ONLINE_REWARD_REQUEST',
    'CMSG_GAIN_REWARD_REQUEST_CHAMPIONSHIP',
    'CMSG_MOBILIZATION_GET_REWARD_REQUEST',
    'CMSG_MICROPAYMENT_DAILY_REWARD_REQUEST',
    'CMSG_TEAM_RECHARGE_QUICK_REWARD_REQUEST',
    'CMSG_WHEEL_REWARD_REQUEST',
    'CMSG_PASSWORD_CHECK_REQUEST',
    'CMSG_EXPEDITION_INFO_REQUEST',
]

p("=" * 80)
p("PACKDATA ANALYSIS - Bot-Useful CMSG Payload Formats")
p("=" * 80)

for target in targets:
    results = find_function(target)
    if not results:
        p(f"\n{'='*60}")
        p(f"  {target} - NOT FOUND in .dynsym")
        continue

    for name, addr, size in results:
        p(f"\n{'='*60}")
        p(f"  {target}")
        p(f"  Symbol: {name[:80]}")
        p(f"  Address: 0x{addr:08X}, Size: {size}")
        p(f"{'='*60}")

        if addr == 0 or addr > len(data):
            p(f"  Invalid address, skipping")
            continue

        max_bytes = min(size if size > 0 else 400, 1500)
        if max_bytes < 20:
            max_bytes = 400

        insns, writes, bl_calls = disasm_packdata(addr, max_bytes)

        # Print compact disassembly
        p(f"\n  Disassembly ({len(insns)} insns):")
        for insn in insns[:60]:
            line = f"    0x{insn.address:08X}: {insn.mnemonic:8s} {insn.op_str}"
            if insn.mnemonic == 'ret' and insn.address > addr + 20:
                p(line)
                break
            p(line)

        if writes:
            p(f"\n  Struct field reads:")
            # Deduplicate by offset
            seen = set()
            for iaddr, mnem, offset, size, op_str in sorted(writes, key=lambda x: x[2]):
                key = (offset, size)
                if key not in seen:
                    seen.add(key)
                    p(f"    [{mnem}] offset 0x{offset:02X} ({size}B) @ 0x{iaddr:08X}")

        if bl_calls:
            p(f"\n  Function calls:")
            for caddr, target_str in bl_calls[:15]:
                p(f"    0x{caddr:08X}: bl {target_str}")

# ═══════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════
with open(r'D:\CascadeProjects\analysis\findings\packdata_analysis.md', 'w', encoding='utf-8') as f:
    f.write("# PackData Analysis - Bot-Useful CMSG Formats\n\n")
    f.write('\n'.join(out))

p(f"\n\nSaved to findings/packdata_analysis.md")

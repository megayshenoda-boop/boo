#!/usr/bin/env python3
"""
32_payload_formats.py - Extract EXACT payload formats from packData
===================================================================
CIStream pattern:
  x1 = CIStream: [0x00]=buf_ptr, [0x08]=capacity, [0x0A]=position, [0x0C]=error
  x0 = this (CMSG struct)

  Writes to buffer = payload fields
  The key: track what's loaded from this (x0/x19) and written to CIStream buffer.
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

def find_packdata(name_contains):
    pos = DYNSYM_OFF
    while pos + 24 <= DYNSYM_OFF + DYNSYM_SIZE:
        st_name = struct.unpack('<I', data[pos:pos+4])[0]
        st_value = struct.unpack('<Q', data[pos+8:pos+16])[0]
        st_size = struct.unpack('<Q', data[pos+16:pos+24])[0]
        if st_name > 0 and st_name < 0x200000 and st_value > 0:
            name_end = data.index(b'\x00', DYNSTR_OFF + st_name)
            name = data[DYNSTR_OFF + st_name:name_end].decode('ascii', errors='replace')
            if name_contains in name and '8packData' in name:
                return (name, st_value, st_size)
        pos += 24
    return None

def find_constructor(name_contains):
    pos = DYNSYM_OFF
    while pos + 24 <= DYNSYM_OFF + DYNSYM_SIZE:
        st_name = struct.unpack('<I', data[pos:pos+4])[0]
        st_value = struct.unpack('<Q', data[pos+8:pos+16])[0]
        st_size = struct.unpack('<Q', data[pos+16:pos+24])[0]
        if st_name > 0 and st_name < 0x200000 and st_value > 0:
            name_end = data.index(b'\x00', DYNSTR_OFF + st_name)
            name = data[DYNSTR_OFF + st_name:name_end].decode('ascii', errors='replace')
            if name_contains in name and 'C1Ev' in name and '8packData' not in name and '7getData' not in name:
                return (name, st_value, st_size)
        pos += 24
    return None

def analyze_packdata(addr, size):
    """Analyze packData to extract payload format.

    CIStream write pattern (write u16):
        ldr x8, [x1]         ; buf_ptr
        ldrh w9, [x1, #0xa]  ; position
        ldrh w10, [x1, #8]   ; capacity
        add w11, w9, #2       ; new_pos = pos + 2
        cmp w11, w10          ; check overflow
        ldrh w10, [x0]        ; LOAD DATA FROM CMSG STRUCT
        strh w10, [x8, w9, uxtw]  ; WRITE TO BUFFER

    CIStream write u32 pattern uses add #4 instead of #2.
    CIStream write u8 uses add #1.
    """
    max_bytes = min(size if size > 0 else 600, 2000)
    code = data[addr:addr + max_bytes]
    insns = list(md.disasm(code, addr))

    # Track: what size is being written (from add wN, wN, #SIZE)
    # and what offset it comes from in x0/x19/x20

    payload_fields = []
    current_write_size = 0
    payload_offset = 0

    this_reg = 'x0'  # Usually x0, but may be moved to x19/x20

    for i, insn in enumerate(insns):
        if insn.mnemonic == 'ret' and insn.address > addr + 20:
            break

        # Detect this pointer save: mov x19, x0
        if insn.mnemonic == 'mov' and insn.op_str.startswith('x19, x0'):
            this_reg = 'x19'
        if insn.mnemonic == 'mov' and insn.op_str.startswith('x20, x0'):
            this_reg = 'x20'

        # Detect write size from: add wN, wN, #SIZE (position update)
        if insn.mnemonic == 'add' and '#' in insn.op_str:
            parts = insn.op_str.split('#')
            try:
                add_val = int(parts[-1], 0)
                if add_val in (1, 2, 4, 8):
                    # Check if this is position update (strh wN, [x1, #0xa] follows soon)
                    for j in range(i+1, min(i+6, len(insns))):
                        if 'strh' in insns[j].mnemonic and '#0xa' in insns[j].op_str:
                            current_write_size = add_val
                            break
            except:
                pass

        # Detect data load from CMSG struct
        if insn.mnemonic in ('ldrh', 'ldrb', 'ldr', 'ldrsb', 'ldrsh', 'ldrsw'):
            if f'[{this_reg}]' in insn.op_str or f'[{this_reg},' in insn.op_str:
                offset = 0
                if '#' in insn.op_str:
                    try:
                        offset = int(insn.op_str.split('#')[-1].rstrip(']').rstrip('!'), 0)
                    except:
                        pass

                sizes = {'ldrb': 1, 'ldrsb': 1, 'ldrh': 2, 'ldrsh': 2, 'ldr': 4, 'ldrsw': 4}
                field_size = sizes.get(insn.mnemonic, 4)
                if insn.mnemonic == 'ldr' and insn.op_str.split(',')[0].strip().startswith('x'):
                    field_size = 8

                # Check if this is followed by a strh/strb/str to buffer
                is_payload = False
                for j in range(i+1, min(i+8, len(insns))):
                    if insns[j].mnemonic in ('strh', 'strb', 'str') and 'uxtw' in insns[j].op_str:
                        is_payload = True
                        break

                if is_payload:
                    payload_fields.append({
                        'struct_offset': offset,
                        'size': current_write_size if current_write_size else field_size,
                        'payload_offset': payload_offset,
                        'insn_addr': insn.address,
                    })
                    payload_offset += current_write_size if current_write_size else field_size
                    current_write_size = 0

    return payload_fields

p("=" * 80)
p("PAYLOAD FORMAT ANALYSIS")
p("=" * 80)

targets = [
    ('CMSG_ITEM_USE', 'Use items/speedups'),
    ('CMSG_RECEIVE_REWARD_REQUEST', 'Collect quest rewards'),
    ('CMSG_RECEIVE_REWARD_BATCH_REQUEST', 'Collect batch rewards'),
    ('CMSG_RECEIVE_SIGN_ACTIVITY', 'Daily sign-in activity'),
    ('CMSG_SIGN_REQUEST', 'Daily sign'),
    ('CMSG_APPEND_SIGN_REQUEST', 'Makeup sign'),
    ('CMSG_DAY_REFRESH_REQUEST', 'Day refresh'),
    ('CMSG_MONTH_REFRESH_REQUEST', 'Month refresh'),
    ('CMSG_NEW_ONLINE_REWARD_REQUEST', 'Online reward'),
    ('CMSG_RANDOM_ONLINE_REWARD_REQUEST', 'Random online reward'),
    ('CMSG_ACTIVEGIFTS_ACTION_REQUEST', 'Active gifts'),
    ('CMSG_ACTIVEGIFTS_REWARD_REQUEST', 'Active gifts reward'),
    ('CMSG_CITY_BUFF_USE', 'City buff use'),
    ('CMSG_CITY_BUFF_GET_USE', 'City buff get+use'),
    ('CMSG_LUCKY_SHOP_SCRATCH_CARD', 'Lucky scratch card'),
    ('CMSG_RECEIVE_FIRST_BIND_REWARD', 'First bind reward'),
    ('CMSG_OUTFIRE_REQUEST', 'Put out fire'),
    ('CMSG_HERO_SOLDIER_RECRUIT_REQUEST', 'Hero recruit'),
    ('CMSG_DAMAGE_HELP', 'Alliance help'),
    ('CMSG_DAMAGE_BUY', 'Buy damage'),
    ('CMSG_ACHIEVEMENT_RECEIVE_REWARD_REQUEST', 'Achievement reward'),
    ('CMSG_RECEIVE_LUXURY_REWARD', 'VIP/Luxury reward'),
    ('CMSG_RECEIVE_ACCUMULATION_REWARD_REQUEST', 'Accumulation reward'),
    ('CMSG_EVERY_DAY_GIFTPACK_REWARD_REQUEST', 'Daily gift pack'),
    ('CMSG_CAMEL_SHOP_BUY_REQUEST', 'Camel shop buy'),
    ('CMSG_POWER_TASK_REWARD_REQUEST', 'Power task reward'),
    ('CMSG_SERVER_MISSION_RECEIVE_REQUEST', 'Server mission reward'),
    ('CMSG_MOBILIZATION_GET_REWARD_REQUEST', 'Mobilization reward'),
    ('CMSG_MICROPAYMENT_DAILY_REWARD_REQUEST', 'Micropayment daily'),
    ('CMSG_TEAM_RECHARGE_QUICK_REWARD_REQUEST', 'Team recharge reward'),
    ('CMSG_WHEEL_REWARD_REQUEST', 'Wheel reward'),
    ('CMSG_START_MARCH_NEW', 'Start march (gather/attack)'),
    ('CMSG_DESERT_TRADE_START_MARCH_REQUEST', 'Desert trade march'),
    ('CMSG_PASSWORD_CHECK_REQUEST', 'Password check (0x1B8B)'),
    ('CMSG_EXPEDITION_INFO_REQUEST', 'Expedition info'),
    ('CMSG_CONTINUITY_GIFTPACK_ACTION_REQUEST', 'Continuity gift'),
    ('CMSG_KING_ROAD_REWARD_REQUEST', 'King road reward'),
    ('CMSG_GAIN_EXP_REWARD_REQUEST', 'Exp reward'),
    ('CMSG_DOWN_LOAD_REWARD_REQUEST', 'Download reward'),
    ('CMSG_DOUBLE_LOTTERY_PLAY_REQUEST', 'Double lottery play'),
    ('CMSG_LOSTLAND_ACHIEVEMENT_REWARD_REQUEST', 'Lost land reward'),
    ('CMSG_ARENA_BUY_TIMES_REQUEST', 'Arena buy times'),
]

for cmsg_name, description in targets:
    result = find_packdata(cmsg_name)
    if not result:
        p(f"\n  {cmsg_name} ({description}): NOT FOUND")
        continue

    name, addr, size = result
    fields = analyze_packdata(addr, size)

    p(f"\n{'─'*60}")
    p(f"  {cmsg_name} ({description})")
    p(f"  Address: 0x{addr:08X}, Size: {size}B")

    if not fields:
        # Simple case - may just write from x0 directly
        # Let's check constructor to understand struct size
        ctor = find_constructor(cmsg_name)
        if ctor:
            p(f"  Constructor: 0x{ctor[1]:08X}")
        p(f"  Payload: analyzing direct writes...")

        # Brute force: just disasm and look for strh/strb to buffer
        max_bytes = min(size if size > 0 else 400, 1000)
        code = data[addr:addr + max_bytes]
        insns = list(md.disasm(code, addr))
        write_count = 0
        for insn in insns:
            if insn.mnemonic == 'ret' and insn.address > addr + 20:
                break
            if insn.mnemonic in ('strh', 'strb', 'str') and 'uxtw' in insn.op_str:
                write_count += 1
                p(f"    WRITE @ 0x{insn.address:08X}: {insn.mnemonic} {insn.op_str}")
        p(f"  Buffer writes: {write_count}")
    else:
        total_size = sum(f['size'] for f in fields)
        p(f"  Payload: {total_size} bytes, {len(fields)} fields:")
        for f in fields:
            p(f"    [{f['payload_offset']:2d}] struct[0x{f['struct_offset']:02X}] = {f['size']}B")

# ═══════════════════════════════════════════════════════════════
# Also check constructors for struct initialization
# ═══════════════════════════════════════════════════════════════
p(f"\n\n{'='*80}")
p("CONSTRUCTOR ANALYSIS - Default Values")
p(f"{'='*80}")

simple_cmsgs = [
    'CMSG_ITEM_USE',
    'CMSG_RECEIVE_REWARD_REQUEST',
    'CMSG_SIGN_REQUEST',
    'CMSG_RECEIVE_SIGN_ACTIVITY',
    'CMSG_DAY_REFRESH_REQUEST',
    'CMSG_NEW_ONLINE_REWARD_REQUEST',
    'CMSG_DAMAGE_HELP',
    'CMSG_OUTFIRE_REQUEST',
    'CMSG_RECEIVE_FIRST_BIND_REWARD',
    'CMSG_CITY_BUFF_USE',
    'CMSG_ACHIEVEMENT_RECEIVE_REWARD_REQUEST',
]

for cmsg_name in simple_cmsgs:
    ctor = find_constructor(cmsg_name)
    if not ctor:
        continue

    name, addr, size = ctor
    if addr == 0: continue

    p(f"\n  {cmsg_name} constructor @ 0x{addr:08X}")
    max_bytes = min(size if size > 0 else 200, 500)
    code = data[addr:addr + max_bytes]
    insns = list(md.disasm(code, addr))

    stores = []
    for insn in insns:
        if insn.mnemonic == 'ret' and insn.address > addr + 8:
            break
        # Look for stores to this (x0) - initial values
        if insn.mnemonic in ('strh', 'strb', 'str', 'stp') and 'x0' in insn.op_str:
            stores.append(f"    0x{insn.address:08X}: {insn.mnemonic} {insn.op_str}")
        # Also MOV that sets default values
        if insn.mnemonic.startswith('mov') and '#' in insn.op_str:
            stores.append(f"    0x{insn.address:08X}: {insn.mnemonic} {insn.op_str}")

    for s in stores[:10]:
        p(s)

# SAVE
with open(r'D:\CascadeProjects\analysis\findings\payload_formats.md', 'w', encoding='utf-8') as f:
    f.write("# Payload Format Analysis\n\n")
    f.write('\n'.join(out))

p(f"\n\nSaved to findings/payload_formats.md")

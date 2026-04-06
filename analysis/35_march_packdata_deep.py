#!/usr/bin/env python3
"""
35_march_packdata_deep.py - Deep analysis of CMSG_START_MARCH_NEW::packData
============================================================================
Address: 0x05212294, Size: 1252 bytes
ARM64 little-endian, CIStream serialization.

Key insight: The function has a complex control flow:
- Normal path: writes fields sequentially with capacity checks
- Error path: on capacity overflow, jumps back to error handler at 0x52122F8
  which goes to the encryption epilogue at 0x52123B8
- The backward branches to 0x52122D0/0x52122F8 are NOT loops - they're error exits
- The ONLY real loop is the array write at 0x05212324-0x05212364

Flow: prologue -> write_u16[0x00] -> cbz to 0x05212418 (main sequence)
      0x05212418: write_u16[0x02] -> write_u8[0x04..0x08] -> write_u64[0x10]
      -> write_u16[0x18] -> write_u16[0x1A] -> array loop (this+0x20 vector)
      -> write_u8 (array count) -> write_u32[0x38] -> THEN jumps to 0x0521261C
      -> write_u8[0x3C] -> write_u64[0x40] -> write_u8[0x48] -> write_u8[0x49]
      -> write_u64[0x50] -> write_u8[0x58] -> write_u32[0x5C]
      -> encryption epilogue (getServerKey + Encode)
"""
import struct
import sys
import os

try:
    from capstone import *
except ImportError:
    print("ERROR: capstone not installed. Run: pip install capstone")
    sys.exit(1)

LIBGAME = r"D:\CascadeProjects\libgame.so"
FUNC_ADDR = 0x05212294
FUNC_SIZE = 1252
FUNC_END = FUNC_ADDR + FUNC_SIZE
OUTPUT_DIR = r"D:\CascadeProjects\analysis\findings"

# ─────────────────────────────────────────────────────────────────
# Load and disassemble
# ─────────────────────────────────────────────────────────────────
with open(LIBGAME, "rb") as f:
    f.seek(FUNC_ADDR)
    code = f.read(FUNC_SIZE + 64)

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

all_insns = []
for insn in md.disasm(code, FUNC_ADDR):
    if insn.address >= FUNC_END:
        break
    all_insns.append(insn)

print(f"Disassembled {len(all_insns)} instructions")
print(f"Range: 0x{FUNC_ADDR:08X} - 0x{all_insns[-1].address:08X}")

# ─────────────────────────────────────────────────────────────────
# Manual flow trace - following the NORMAL execution path
# ─────────────────────────────────────────────────────────────────
# Based on reading the disassembly, here is the exact payload format:

print("\n" + "=" * 90)
print("PAYLOAD FORMAT (Manual Trace of Normal Execution Path)")
print("=" * 90)

# The CIStream write pattern for each field:
# 1. Check capacity: ldrh pos, [stream, #0xa]; ldrh cap, [stream, #8]; add new_pos, pos, #SIZE; cmp; b.hi error
# 2. Load buf_ptr: ldr buf, [stream]
# 3. Load value: ldr/ldrh/ldrb val, [this, #OFFSET]
# 4. Store to buf: str/strh/strb val, [buf, pos, uxtw]
# 5. Update pos: ldrh pos, [stream, #0xa]; add pos, pos, #SIZE; strh pos, [stream, #0xa]
# 6. Check error: ldr err, [stream, #0xc]; cbnz err, error_handler

fields = []  # (buf_offset, size, struct_offset, struct_size, name_guess, address)

# ── Field 0: STRUCT[0x00] u16 ──
# 0x052122DC: ldrh w9, [x19]           ; this[0x00]
# 0x052122E0: strh w9, [x22, w8, uxtw] ; write 2B
# 0x052122EC: add w9, w9, #2           ; pos += 2
fields.append((0, 2, 0x00, 2, "msg_id / sub_type (u16)", 0x052122E0))

# After this write, cbz w8(error), #0x5212418 jumps to main body

# ── Field 1: STRUCT[0x02] u16 ──  (at 0x05212430)
# 0x05212430: ldrh w10, [x19, #2]
# 0x05212438: strh w10, [x8, x9]       ; write 2B
# 0x05212444: add w9, w9, #2           ; pos += 2
fields.append((2, 2, 0x02, 2, "march_type (u16)", 0x05212438))

# ── Field 2: STRUCT[0x04] u8 ──  (at 0x05212464)
# 0x05212464: ldrb w10, [x19, #4]
# 0x05212468: strb w10, [x9, w8, uxtw] ; write 1B
# 0x05212474: add w9, w9, #1           ; pos += 1
fields.append((4, 1, 0x04, 1, "flag_byte_0 (u8)", 0x05212468))

# ── Field 3: STRUCT[0x05] u8 ──
# 0x05212494: ldrb w10, [x19, #5]
# 0x05212498: strb w10, [x9, w8, uxtw] ; write 1B
# 0x052124A4: add w9, w9, #1           ; pos += 1
fields.append((5, 1, 0x05, 1, "flag_byte_1 (u8)", 0x05212498))

# ── Field 4: STRUCT[0x06] u8 ──
# 0x052124C4: ldrb w10, [x19, #6]
# 0x052124C8: strb w10, [x9, w8, uxtw] ; write 1B
# 0x052124D4: add w9, w9, #1           ; pos += 1
fields.append((6, 1, 0x06, 1, "flag_byte_2 (u8)", 0x052124C8))

# ── Field 5: STRUCT[0x07] u8 ──
# 0x052124F4: ldrb w10, [x19, #7]
# 0x052124F8: strb w10, [x9, w8, uxtw] ; write 1B
# 0x05212504: add w9, w9, #1           ; pos += 1
fields.append((7, 1, 0x07, 1, "flag_byte_3 (u8)", 0x052124F8))

# ── Field 6: STRUCT[0x08] u8 ──
# 0x05212524: ldrb w10, [x19, #8]
# 0x05212528: strb w10, [x9, w8, uxtw] ; write 1B
# 0x05212534: add w9, w9, #1           ; pos += 1
fields.append((8, 1, 0x08, 1, "flag_byte_4 / hero_count? (u8)", 0x05212528))

# ── Field 7: STRUCT[0x10] u64 (8 bytes!) ──
# 0x05212548: add w10, w8, #8          ; capacity check for 8 bytes
# 0x05212558: ldr x10, [x19, #0x10]    ; 8-byte load!
# 0x0521255C: str x10, [x9, w8, uxtw]  ; write 8B (str x-reg)
# 0x05212568: add w9, w9, #8           ; pos += 8
fields.append((9, 8, 0x10, 8, "target_coords (u64 = two u32: x,y)", 0x0521255C))

# ── Field 8: STRUCT[0x18] u16 ──
# 0x0521258C: ldrh w10, [x19, #0x18]
# 0x05212590: strh w10, [x9, w8, uxtw] ; write 2B
# 0x0521259C: add w9, w9, #2           ; pos += 2
fields.append((17, 2, 0x18, 2, "kingdom_id / target_kingdom (u16)", 0x05212590))

# ── Field 9: STRUCT[0x1A] u16 ──
# 0x052125C0: ldrh w10, [x19, #0x1a]
# 0x052125C4: strh w10, [x9, w8, uxtw] ; write 2B
# 0x052125DC: add w12, w12, #2         ; pos += 2
fields.append((19, 2, 0x1A, 2, "march_slot / queue_id (u16)", 0x052125C4))

# ── Array loop: vector at this+0x20 (begin) / this+0x28 (end) ──
# 0x052125C8: mov x9, x19              ; x9 = this
# 0x052125CC: ldp x10, x11, [x9, #0x20]!  ; x10=begin, x11=end (with writeback: x9 = this+0x20)
# 0x052125D8: sub x11, x11, x10        ; byte_count = end - begin
# 0x052125E0: asr x10, x11, #2         ; elem_count = byte_count / 4
# Loop body at 0x05212324:
#   ldr x13, [x9]                       ; x9 = &begin (this+0x20), reload ptr
#   ldr w13, [x13, x8, lsl #2]          ; array[i] (4-byte elements)
#   str w13, [x14, w12, uxtw]           ; write 4B to buffer
#   add w12, w12, #4                    ; pos += 4
# This is count x 4-byte writes

# Before the array loop, at 0x05212600:
# 0x05212600: lsr x13, x11, #2          ; count = byte_diff >> 2
# 0x05212604: strb w13, [x12, w8, uxtw] ; write count as 1 byte!
# 0x0521260C: add w12, w8, #1           ; pos += 1

# WAIT - re-reading the flow more carefully:
# The array section has TWO parts:
# Part A (first encounter at 0x052122FC):
#   ldp x10, x11, [x9, #0x20]!  -> vector at this+0x20
#   Loop writes each u32 element
# Part B (second encounter after field 9 at 0x052125CC):
#   Same ldp pattern, re-reads the vector
#   But this time it writes the COUNT byte first, then may loop again
# Actually this is the SAME code re-entered from a different point

# The actual order in the NORMAL path:
# After field 9 (STRUCT[0x1A]), the code at 0x052125E8 does:
#   cbnz w8, #0x5212308   ; if error, jump to 0x5212308 (the array section)
#   But on normal path (no error): falls through to 0x052125EC
#   Then at 0x052125F8: b.hs #0x521238c (capacity error)
#   Then 0x052125FC-0x05212618: writes the array count byte + jumps to 0x5212308

# Let me re-trace more carefully...
# At 0x052125E8: cbnz w8, #0x5212308 - this checks error AFTER writing field 9
# Normal path: w8=0, so we DON'T branch, fall through to 0x052125EC
# 0x052125EC: ldrh w8, [x20, #0xa]     ; position
# 0x052125F0: ldrh w12, [x20, #8]      ; capacity
# 0x052125F4: cmp w8, w12
# 0x052125F8: b.hs #0x521238c          ; error if pos >= cap
# 0x052125FC: ldr x12, [x20]           ; buf_ptr
# 0x05212600: lsr x13, x11, #2         ; count = vector_byte_diff / 4
# 0x05212604: strb w13, [x12, w8, uxtw] ; WRITE 1B = array_count
# 0x05212608-0x05212614: pos += 1
# 0x05212618: b #0x5212308             ; unconditional jump to array processing

# At 0x05212308: tst x11, #0x3fc       ; check if count > 0
# If zero: b.eq #0x5212374 -> skip array loop
# If nonzero: fall through to loop at 0x05212324-0x05212364

fields.append((21, 1, -1, 0, "array_count (u8) = len(troop_vector)", 0x05212604))

# ── Array loop: N x u32 entries ──
# Each iteration writes 4 bytes from array[i]
fields.append((22, 4, -2, 0, "array[i] (u32) x N iterations [LOOP]", 0x05212330))

# After array loop, at 0x05212374-0x052123B0:
# ── Field: STRUCT[0x38] u32 ──
# 0x0521239C: ldr w10, [x19, #0x38]
# 0x052123A0: str w10, [x9, w8, uxtw]  ; write 4B
# 0x052123AC: add w8, w8, #4           ; pos += 4
fields.append((-1, 4, 0x38, 4, "tile_type / resource_id (u32)", 0x052123A0))

# After STRUCT[0x38], at 0x052123B4: cbz w9, #0x521261C (no error -> jump to 0x521261C)
# THIS is the continuation to the rest of the fields!

# ── Field: STRUCT[0x3C] u8 ── (at 0x0521262C)
# 0x0521262C: ldrb w10, [x19, #0x3c]
# 0x05212634: strb w10, [x9, x8]       ; write 1B (note: not uxtw but x8 extend)
# 0x05212640: add w8, w8, #1           ; pos += 1
fields.append((-1, 1, 0x3C, 1, "march_flag / sub_flag (u8)", 0x05212634))

# ── Field: STRUCT[0x40] u64 ──
# 0x05212664: ldr x10, [x19, #0x40]
# 0x05212668: str x10, [x9, w8, uxtw]  ; write 8B
# 0x05212674: add w8, w8, #8           ; pos += 8
fields.append((-1, 8, 0x40, 8, "rally_timestamp / march_param (u64)", 0x05212668))

# ── Field: STRUCT[0x48] u8 ──
# 0x05212694: ldrb w10, [x19, #0x48]
# 0x05212698: strb w10, [x9, w8, uxtw] ; write 1B
# 0x052126A4: add w8, w8, #1           ; pos += 1
fields.append((-1, 1, 0x48, 1, "extra_flag_0 (u8)", 0x05212698))

# ── Field: STRUCT[0x49] u8 ──
# 0x052126C4: ldrb w10, [x19, #0x49]
# 0x052126C8: strb w10, [x9, w8, uxtw] ; write 1B
# 0x052126D4: add w8, w8, #1           ; pos += 1
fields.append((-1, 1, 0x49, 1, "extra_flag_1 (u8)", 0x052126C8))

# ── Field: STRUCT[0x50] u64 ──
# 0x052126F8: ldr x10, [x19, #0x50]
# 0x052126FC: str x10, [x9, w8, uxtw]  ; write 8B
# 0x05212708: add w8, w8, #8           ; pos += 8
fields.append((-1, 8, 0x50, 8, "extra_param (u64)", 0x052126FC))

# ── Field: STRUCT[0x58] u8 ──
# 0x05212728: ldrb w10, [x19, #0x58]
# 0x0521272C: strb w10, [x9, w8, uxtw] ; write 1B
# 0x05212738: add w8, w8, #1           ; pos += 1
fields.append((-1, 1, 0x58, 1, "extra_flag_2 (u8)", 0x0521272C))

# ── Field: STRUCT[0x5C] u32 ──
# 0x0521275C: ldr w10, [x19, #0x5c]
# 0x05212764: str w10, [x9, x8]        ; write 4B
# 0x0521276C: add w8, w8, #4           ; pos += 4
fields.append((-1, 4, 0x5C, 4, "extra_param_2 (u32)", 0x05212764))

# After 0x05212774: b #0x52123b8 -> jump to encryption epilogue

# ─────────────────────────────────────────────────────────────────
# Compute actual buffer offsets
# ─────────────────────────────────────────────────────────────────
print("\nORDERED PAYLOAD FIELDS:")
print("-" * 90)

buf_offset = 0
ordered_fields = []
for i, (hint_off, size, struct_off, struct_sz, name, addr) in enumerate(fields):
    entry = {
        'index': i,
        'buf_offset': buf_offset,
        'size': size,
        'struct_offset': struct_off,
        'struct_size': struct_sz,
        'name': name,
        'addr': addr,
    }
    ordered_fields.append(entry)

    struct_str = f"STRUCT[0x{struct_off:02X}]" if struct_off >= 0 else "(computed)"
    print(f"  [{i:2d}] buf[{buf_offset:3d}..{buf_offset+size-1:3d}]  {size:2d}B  {struct_str:16s}  {name:45s}  @ 0x{addr:08X}")
    buf_offset += size

print(f"\n  Fixed payload size (no array): {buf_offset - 4} bytes + N*4 bytes for array")
print(f"  With 0 array elements: {buf_offset - 4} bytes")

# ─────────────────────────────────────────────────────────────────
# Print full annotated disassembly
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 90)
print("FULL ANNOTATED DISASSEMBLY")
print("=" * 90)

this_regs = {0, 19}
stream_regs = {1, 20}

for insn in all_insns:
    mnem = insn.mnemonic
    ops = insn.op_str
    ann = []

    if mnem == 'mov':
        parts = [p.strip() for p in ops.split(',')]
        if len(parts) == 2:
            if parts[1] in ('x0', 'x19') and parts[0].startswith('x'):
                ann.append(f"{parts[0]} = this")
            if parts[1] in ('x1', 'x20') and parts[0].startswith('x'):
                ann.append(f"{parts[0]} = CIStream")

    if mnem in ('ldrb', 'ldrh', 'ldr', 'ldrsb', 'ldrsh', 'ldrsw'):
        for tr in this_regs:
            if (f'x{tr},' in ops or f'x{tr}]' in ops) and '#' in ops:
                try:
                    off = int(ops.split('#')[-1].rstrip(']').strip(), 0)
                    sz_map = {'ldrb': 1, 'ldrsb': 1, 'ldrh': 2, 'ldrsh': 2, 'ldr': 4, 'ldrsw': 4}
                    sz = sz_map.get(mnem, 4)
                    dst = ops.split(',')[0].strip()
                    if dst.startswith('x') and mnem == 'ldr':
                        sz = 8
                    ann.append(f"STRUCT[0x{off:02X}] ({sz}B)")
                except: pass
            elif f'x{tr}]' in ops and '#' not in ops:
                ann.append("deref *this")

        for sr in stream_regs:
            if f'x{sr}]' in ops and '#' not in ops:
                ann.append("buf_ptr")
            elif f'x{sr}, #0xa' in ops:
                ann.append("position")
            elif f'x{sr}, #8' in ops or f'x{sr}, #0x8' in ops:
                ann.append("capacity")
            elif f'x{sr}, #0xc' in ops:
                ann.append("error")

    if mnem in ('strb', 'strh', 'str') and ('uxtw' in ops or (mnem in ('strb','strh','str') and ', x' in ops.split(']')[0] if ']' in ops else False)):
        if 'uxtw' in ops or ('x' in ops.split('[')[1].split(',')[1] if '[' in ops and ',' in ops.split('[')[1] else False):
            sz = {'strb': 1, 'strh': 2, 'str': 4}.get(mnem, 0)
            src = ops.split(',')[0].strip()
            if src.startswith('x') and mnem == 'str':
                sz = 8
            ann.append(f"** WRITE {sz}B **")

    if mnem == 'strh':
        for sr in stream_regs:
            if f'x{sr}, #0xa' in ops:
                ann.append("save pos")

    if mnem == 'str':
        for sr in stream_regs:
            if f'x{sr}, #0xc' in ops:
                ann.append("set error")

    if mnem in ('cbz', 'cbnz', 'tbz', 'tbnz') or mnem.startswith('b.'):
        try:
            target = int(ops.split('#')[-1].strip(), 0)
            if target < insn.address:
                if target in (0x052122D0, 0x052122F8, 0x052123B8, 0x0521238C):
                    ann.append(f"ERROR -> 0x{target:08X}")
                else:
                    ann.append(f"LOOP -> 0x{target:08X}")
            else:
                ann.append(f"-> 0x{target:08X}")
        except: pass

    if mnem == 'b' and '#' in ops:
        try:
            target = int(ops.split('#')[-1].strip(), 0)
            if target < insn.address:
                if target in (0x052122D0, 0x052122F8, 0x052123B8, 0x0521238C, 0x05212340, 0x05212308):
                    ann.append(f"JUMP -> 0x{target:08X}")
                else:
                    ann.append(f"LOOP -> 0x{target:08X}")
            else:
                ann.append(f"-> 0x{target:08X}")
        except: pass

    if mnem == 'bl':
        try:
            target = int(ops.split('#')[-1].strip() if '#' in ops else ops.strip(), 0)
            PLT = {0x05C6DBA0: "CMsgCodec::Encode", 0x05C6DBC0: "CMsgCodec::getServerKey"}
            ann.append(f"CALL {PLT.get(target, hex(target))}")
        except: pass

    if mnem == 'ret':
        ann.append("RETURN")

    if mnem == 'ldp':
        for tr in this_regs:
            if f'x{tr}' in ops:
                try:
                    off = int(ops.split('#')[-1].rstrip(']!').strip(), 0)
                    ann.append(f"load pair from this+0x{off:02X}")
                except: pass

    a = f"  ; {', '.join(ann)}" if ann else ""
    print(f"  0x{insn.address:08X}: {mnem:8s} {ops:45s}{a}")

# ─────────────────────────────────────────────────────────────────
# Summary of struct fields
# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 90)
print("CMSG_START_MARCH_NEW STRUCT LAYOUT")
print("=" * 90)

struct_map = {
    0x00: ("u16", "msg_id / sub_type"),
    0x02: ("u16", "march_type"),
    0x04: ("u8",  "flag_0"),
    0x05: ("u8",  "flag_1"),
    0x06: ("u8",  "flag_2"),
    0x07: ("u8",  "flag_3"),
    0x08: ("u8",  "flag_4 / hero_count?"),
    # 0x09-0x0F: padding
    0x10: ("u64", "target_coords (likely two u32: x, y packed)"),
    0x18: ("u16", "kingdom_id"),
    0x1A: ("u16", "march_slot / queue_id"),
    # 0x1C-0x1F: padding
    0x20: ("ptr",  "vector<u32>.begin (troop/hero array)"),
    0x28: ("ptr",  "vector<u32>.end"),
    0x30: ("ptr",  "vector<u32>.capacity_end (unused in packData)"),
    0x38: ("u32", "tile_type / resource_id"),
    0x3C: ("u8",  "march_flag / sub_flag"),
    # 0x3D-0x3F: padding
    0x40: ("u64", "rally_timestamp / march_param_1"),
    0x48: ("u8",  "extra_flag_0"),
    0x49: ("u8",  "extra_flag_1"),
    # 0x4A-0x4F: padding
    0x50: ("u64", "march_param_2"),
    0x58: ("u8",  "extra_flag_2"),
    # 0x59-0x5B: padding
    0x5C: ("u32", "extra_param / march_param_3"),
}

for off in sorted(struct_map):
    typ, name = struct_map[off]
    print(f"  [0x{off:02X}]  {typ:5s}  {name}")

# ─────────────────────────────────────────────────────────────────
# Generate markdown report
# ─────────────────────────────────────────────────────────────────
os.makedirs(OUTPUT_DIR, exist_ok=True)
report_path = os.path.join(OUTPUT_DIR, "march_payload_format.md")

with open(report_path, 'w', encoding='utf-8') as f:
    f.write("# CMSG_START_MARCH_NEW (0x0CE8) Payload Format\n\n")
    f.write(f"- **Function**: `packData` at `0x{FUNC_ADDR:08X}`\n")
    f.write(f"- **Size**: {FUNC_SIZE} bytes ({len(all_insns)} instructions)\n")
    f.write(f"- **Opcode**: 0x0CE8\n\n")

    f.write("## Payload Layout\n\n")
    f.write("The payload is variable-length due to a troop/hero array.\n")
    f.write("Fixed portion (without array) = 46 bytes + N*4 bytes for each array entry.\n\n")
    f.write("| # | Offset | Size | Struct Field | Type | Description |\n")
    f.write("|---|--------|------|-------------|------|-------------|\n")

    buf_off = 0
    for i, entry in enumerate(ordered_fields):
        struct_str = f"0x{entry['struct_offset']:02X}" if entry['struct_offset'] >= 0 else "computed"
        sz_str = f"{entry['size']}B"
        if entry['struct_offset'] == -2:
            f.write(f"| {i} | {buf_off}+ | {sz_str} each | vector[0x20] | u32[] | Troop/hero array (N entries) |\n")
        else:
            f.write(f"| {i} | {buf_off} | {sz_str} | [{struct_str}] | {'u'+str(entry['size']*8)} | {entry['name']} |\n")
        buf_off += entry['size']

    f.write(f"\n**Base payload**: 46 bytes (0 array entries) + N*4 per troop entry\n\n")

    f.write("## CMSG Struct Layout\n\n")
    f.write("| Offset | Type | Field |\n")
    f.write("|--------|------|-------|\n")
    for off in sorted(struct_map):
        typ, name = struct_map[off]
        f.write(f"| 0x{off:02X} | {typ} | {name} |\n")

    f.write("\n## Control Flow\n\n")
    f.write("```\n")
    f.write("packData(this=x0, stream=x1):\n")
    f.write("  x19 = this, x20 = stream\n")
    f.write("  \n")
    f.write("  write_u16 this[0x00]          ; msg sub-type\n")
    f.write("  if no_error: goto main_body (0x05212418)\n")
    f.write("  \n")
    f.write("main_body:\n")
    f.write("  write_u16 this[0x02]          ; march type\n")
    f.write("  write_u8  this[0x04]          ; flag 0\n")
    f.write("  write_u8  this[0x05]          ; flag 1\n")
    f.write("  write_u8  this[0x06]          ; flag 2\n")
    f.write("  write_u8  this[0x07]          ; flag 3\n")
    f.write("  write_u8  this[0x08]          ; flag 4\n")
    f.write("  write_u64 this[0x10]          ; target x,y (packed)\n")
    f.write("  write_u16 this[0x18]          ; kingdom\n")
    f.write("  write_u16 this[0x1A]          ; march slot\n")
    f.write("  \n")
    f.write("  ; Load vector from this+0x20\n")
    f.write("  begin, end = ldp [this, #0x20]\n")
    f.write("  count = (end - begin) / 4\n")
    f.write("  write_u8 count                ; array element count\n")
    f.write("  for i in 0..count:\n")
    f.write("    write_u32 begin[i]          ; array entry\n")
    f.write("  \n")
    f.write("  write_u32 this[0x38]          ; tile/resource type\n")
    f.write("  \n")
    f.write("  ; --- continues at 0x0521261C ---\n")
    f.write("  write_u8  this[0x3C]          ; sub-flag\n")
    f.write("  write_u64 this[0x40]          ; rally/param\n")
    f.write("  write_u8  this[0x48]          ; extra flag 0\n")
    f.write("  write_u8  this[0x49]          ; extra flag 1\n")
    f.write("  write_u64 this[0x50]          ; param 2\n")
    f.write("  write_u8  this[0x58]          ; extra flag 2\n")
    f.write("  write_u32 this[0x5C]          ; param 3\n")
    f.write("  \n")
    f.write("  ; Encryption epilogue (0x052123B8)\n")
    f.write("  buf[0] = position             ; write payload length\n")
    f.write("  key = getServerKey()\n")
    f.write("  Encode(buf, key)\n")
    f.write("  buf[0] = position             ; update after encoding\n")
    f.write("  return success\n")
    f.write("```\n\n")

    f.write("## Array (Troop/Hero List)\n\n")
    f.write("The vector at struct offset 0x20-0x28 is a `std::vector<uint32_t>`.\n")
    f.write("- `this[0x20]` = begin pointer\n")
    f.write("- `this[0x28]` = end pointer\n")
    f.write("- Element count = `(end - begin) / 4`\n")
    f.write("- Count is written as a u8 (max 255 entries)\n")
    f.write("- Each entry is a u32, likely encoding `troop_type << 16 | troop_count` or similar\n\n")

    f.write("## Key Addresses\n\n")
    f.write("| Address | Description |\n")
    f.write("|---------|-------------|\n")
    f.write("| 0x05212294 | Function entry (prologue) |\n")
    f.write("| 0x052122E0 | First write: this[0x00] u16 |\n")
    f.write("| 0x05212418 | Main body start (after first field) |\n")
    f.write("| 0x05212324 | Array loop body |\n")
    f.write("| 0x05212604 | Array count write |\n")
    f.write("| 0x0521261C | Post-array fields start |\n")
    f.write("| 0x052123B8 | Encryption epilogue |\n")
    f.write("| 0x05212414 | Return |\n\n")

    f.write("## Encoding\n\n")
    f.write("After all fields are serialized, the function:\n")
    f.write("1. Writes the current position (payload length) to `buf[0]` as u16\n")
    f.write("2. Calls `CMsgCodec::getServerKey()` -> server_key\n")
    f.write("3. Calls `CMsgCodec::Encode(buf, server_key)` to encrypt\n")
    f.write("4. Writes the final encoded position back to `buf[0]`\n")

    f.write("\n## Python Payload Builder (Template)\n\n")
    f.write("```python\n")
    f.write("import struct\n\n")
    f.write("def build_march_payload(\n")
    f.write("    sub_type,       # u16 - msg sub-type\n")
    f.write("    march_type,     # u16 - march type (attack, gather, etc.)\n")
    f.write("    flag_0,         # u8\n")
    f.write("    flag_1,         # u8\n")
    f.write("    flag_2,         # u8\n")
    f.write("    flag_3,         # u8\n")
    f.write("    flag_4,         # u8  (possibly hero count)\n")
    f.write("    target_x,      # u32 - target tile X\n")
    f.write("    target_y,      # u32 - target tile Y\n")
    f.write("    kingdom_id,    # u16 - target kingdom\n")
    f.write("    march_slot,    # u16 - march queue slot\n")
    f.write("    troop_array,   # list of u32 - troop entries\n")
    f.write("    tile_type,     # u32 - resource/tile type\n")
    f.write("    sub_flag,      # u8\n")
    f.write("    rally_param,   # u64\n")
    f.write("    extra_flag_0,  # u8\n")
    f.write("    extra_flag_1,  # u8\n")
    f.write("    param_2,       # u64\n")
    f.write("    extra_flag_2,  # u8\n")
    f.write("    param_3,       # u32\n")
    f.write("):\n")
    f.write("    buf = b''\n")
    f.write("    buf += struct.pack('<H', sub_type)\n")
    f.write("    buf += struct.pack('<H', march_type)\n")
    f.write("    buf += struct.pack('<5B', flag_0, flag_1, flag_2, flag_3, flag_4)\n")
    f.write("    buf += struct.pack('<II', target_x, target_y)  # u64 = two u32\n")
    f.write("    buf += struct.pack('<H', kingdom_id)\n")
    f.write("    buf += struct.pack('<H', march_slot)\n")
    f.write("    buf += struct.pack('<B', len(troop_array))\n")
    f.write("    for entry in troop_array:\n")
    f.write("        buf += struct.pack('<I', entry)\n")
    f.write("    buf += struct.pack('<I', tile_type)\n")
    f.write("    buf += struct.pack('<B', sub_flag)\n")
    f.write("    buf += struct.pack('<Q', rally_param)\n")
    f.write("    buf += struct.pack('<BB', extra_flag_0, extra_flag_1)\n")
    f.write("    buf += struct.pack('<Q', param_2)\n")
    f.write("    buf += struct.pack('<B', extra_flag_2)\n")
    f.write("    buf += struct.pack('<I', param_3)\n")
    f.write("    return buf  # 46 + N*4 bytes\n")
    f.write("```\n")

print(f"\nReport saved to: {report_path}")
print("Done.")

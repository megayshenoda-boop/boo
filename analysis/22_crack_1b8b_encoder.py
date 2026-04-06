#!/usr/bin/env python3
"""
22_crack_1b8b_encoder.py - Find the REAL encoding function for 0x1B8B
=====================================================================
Key insight: 0x1B8B's packData calls PLT 0x5c6dbb0, NOT 0x5c6dba0 (CMsgCodec::Encode).
So 0x1B8B uses a DIFFERENT encoder. We need to:
1. Resolve PLT 0x5c6dbb0 to its real function
2. Disassemble the real function
3. Compare with CMsgCodec::Encode to find differences
4. Also disassemble 0x1B8B's packData (0x05273690) to see full encoding flow
"""
import struct, sys
sys.path.insert(0, r'D:\CascadeProjects\claude')
from capstone import *
from protocol import CMSG_TABLE as TABLE

LIBGAME = r"D:\CascadeProjects\libgame.so"
with open(LIBGAME, "rb") as f:
    data = f.read()

text_addr = 0x3250E80
text_off = 0x3250E80
text_size = 43562076

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

def disasm_at(addr, count=80):
    foff = addr  # In this binary, file offset == virtual address for .text
    code = data[foff:foff + count * 4]
    return list(md.disasm(code, addr))

def fmt(insn):
    return f"  0x{insn.address:08X}: {insn.mnemonic:10s} {insn.op_str}"

# ═══════════════════════════════════════════════════════════════
# PART 1: Resolve PLT stubs to real functions
# ═══════════════════════════════════════════════════════════════
print("=" * 80)
print("PART 1: PLT Stub Resolution")
print("=" * 80)

plt_stubs = {
    0x05C6DBA0: "CMsgCodec::Encode (known)",
    0x05C6DBB0: "Unknown (used by 0x1B8B)",
    0x05C6DBC0: "Unknown (get server key?)",
    0x05C6DBD0: "Unknown (write_u16?)",
    0x05C6DBE0: "Unknown (write_u64?)",
}

for plt_addr, desc in sorted(plt_stubs.items()):
    print(f"\nPLT 0x{plt_addr:08X} ({desc}):")
    insns = disasm_at(plt_addr, 4)
    for insn in insns:
        print(fmt(insn))

    # PLT stub is: ADRP Xn, page; LDR Xn, [Xn, #off]; BR Xn
    # Resolve the GOT.PLT address
    if len(insns) >= 2:
        i0 = insns[0]
        i1 = insns[1]
        if i0.mnemonic == 'adrp' and i1.mnemonic == 'ldr':
            try:
                page = int(i0.op_str.split('#')[1], 0)
                off = int(i1.op_str.split('#')[1].rstrip(']'), 0)
                got_addr = page + off
                # Read the GOT.PLT entry to get real function address
                got_val = struct.unpack('<Q', data[got_addr:got_addr+8])[0]
                print(f"  -> GOT.PLT at 0x{got_addr:08X} = 0x{got_val:016X}")
                if text_addr <= got_val < text_addr + text_size:
                    print(f"  -> Real function at 0x{got_val:08X}")
                elif got_val == plt_addr:
                    print(f"  -> Points back to PLT (lazy binding, not resolved)")
                    # Try .rela.plt to find the symbol
            except:
                pass

# ═══════════════════════════════════════════════════════════════
# PART 2: Find PLT 0x5c6dbb0's real function via .rela.plt
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("PART 2: Resolve via .rela.plt and .dynsym")
print("=" * 80)

# Find .rela.plt section
# We need to find which GOT.PLT slot corresponds to PLT 0x5c6dbb0
# First, disassemble PLT stubs to get their GOT addresses
plt_got_map = {}
for plt_addr in sorted(plt_stubs.keys()):
    insns = disasm_at(plt_addr, 3)
    if len(insns) >= 2 and insns[0].mnemonic == 'adrp' and insns[1].mnemonic == 'ldr':
        try:
            page = int(insns[0].op_str.split('#')[1], 0)
            off = int(insns[1].op_str.split('#')[1].rstrip(']'), 0)
            got_addr = page + off
            plt_got_map[plt_addr] = got_addr
            print(f"  PLT 0x{plt_addr:08X} -> GOT 0x{got_addr:08X}")
        except:
            pass

# Find .rela.plt entries that match these GOT addresses
# .rela.plt is typically after .rela.dyn
# Search for .rela.plt section header
# Read ELF section headers
elf_shoff = struct.unpack('<Q', data[0x28:0x30])[0]
elf_shentsize = struct.unpack('<H', data[0x3A:0x3C])[0]
elf_shnum = struct.unpack('<H', data[0x3C:0x3E])[0]
elf_shstrndx = struct.unpack('<H', data[0x3E:0x40])[0]

# Read section header string table
shstr_off = struct.unpack('<Q', data[elf_shoff + elf_shstrndx * elf_shentsize + 0x18:
                                      elf_shoff + elf_shstrndx * elf_shentsize + 0x20])[0]

rela_plt_off = None
rela_plt_size = None
dynstr_off = 0x682A10
dynsym_off = 0x2F8

for i in range(elf_shnum):
    sh = elf_shoff + i * elf_shentsize
    sh_name_idx = struct.unpack('<I', data[sh:sh+4])[0]
    sh_type = struct.unpack('<I', data[sh+4:sh+8])[0]
    sh_offset = struct.unpack('<Q', data[sh+0x18:sh+0x20])[0]
    sh_size = struct.unpack('<Q', data[sh+0x20:sh+0x28])[0]

    name_end = data.index(b'\x00', shstr_off + sh_name_idx)
    name = data[shstr_off + sh_name_idx:name_end].decode('ascii', errors='replace')

    if name == '.rela.plt':
        rela_plt_off = sh_offset
        rela_plt_size = sh_size
        print(f"\n  .rela.plt: offset=0x{sh_offset:X}, size=0x{sh_size:X}")

if rela_plt_off:
    # Each .rela.plt entry is 24 bytes: [r_offset:8][r_info:8][r_addend:8]
    # r_offset = GOT.PLT address
    # r_info >> 32 = symbol index in .dynsym
    for got_addr in plt_got_map.values():
        for j in range(rela_plt_size // 24):
            entry_off = rela_plt_off + j * 24
            r_offset = struct.unpack('<Q', data[entry_off:entry_off+8])[0]
            r_info = struct.unpack('<Q', data[entry_off+8:entry_off+16])[0]

            if r_offset == got_addr:
                sym_idx = r_info >> 32
                # Read symbol from .dynsym
                sym_off = dynsym_off + sym_idx * 24
                st_name = struct.unpack('<I', data[sym_off:sym_off+4])[0]
                st_value = struct.unpack('<Q', data[sym_off+8:sym_off+16])[0]
                st_size = struct.unpack('<Q', data[sym_off+16:sym_off+24])[0]

                name_end = data.index(b'\x00', dynstr_off + st_name)
                sym_name = data[dynstr_off + st_name:name_end].decode('ascii', errors='replace')

                # Find which PLT this is
                for plt_a, g in plt_got_map.items():
                    if g == got_addr:
                        print(f"\n  PLT 0x{plt_a:08X} -> GOT 0x{got_addr:08X} -> symbol #{sym_idx}")
                        print(f"    Name: {sym_name}")
                        print(f"    Value: 0x{st_value:016X}, Size: {st_size}")

# ═══════════════════════════════════════════════════════════════
# PART 3: Disassemble 0x1B8B packData (0x05273690)
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("PART 3: 0x1B8B packData Disassembly (0x05273690)")
print("=" * 80)

pack_data_addr = 0x05273690
insns = disasm_at(pack_data_addr, 200)
for insn in insns:
    line = fmt(insn)
    # Annotate BL calls
    if insn.mnemonic == 'bl':
        try:
            target = int(insn.op_str.split('#')[1], 0) if '#' in insn.op_str else int(insn.op_str, 0)
            if target in plt_stubs:
                line += f"  ; << {plt_stubs[target]} >>"
            elif target == 0x05C6DBA0:
                line += "  ; << CMsgCodec::Encode >>"
        except:
            pass
    print(line)
    if insn.mnemonic == 'ret' and insn.address > pack_data_addr + 32:
        # Check if next insn is function prologue
        break

# ═══════════════════════════════════════════════════════════════
# PART 4: Disassemble the REAL function behind PLT 0x5c6dbb0
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("PART 4: Function behind PLT 0x5c6dbb0")
print("=" * 80)

# Try to find the real address from GOT
target_plt = 0x05C6DBB0
if target_plt in plt_got_map:
    got = plt_got_map[target_plt]
    got_val = struct.unpack('<Q', data[got:got+8])[0]
    if got_val != target_plt and text_addr <= got_val < text_addr + text_size:
        print(f"Real function at 0x{got_val:08X}:")
        insns = disasm_at(got_val, 200)
        for insn in insns:
            print(fmt(insn))
            if insn.mnemonic == 'ret' and insn.address > got_val + 32:
                break
    else:
        print(f"GOT points to 0x{got_val:016X} (lazy binding or external)")
        print("Trying to find the symbol and search for it in .text...")

# ═══════════════════════════════════════════════════════════════
# PART 5: Compare CMsgCodec::Encode (0x04F97C24) with the mystery function
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("PART 5: CMsgCodec::Encode (0x04F97C24) for comparison")
print("=" * 80)

encode_addr = 0x04F97C24
insns = disasm_at(encode_addr, 120)
for insn in insns[:80]:
    print(fmt(insn))

# ═══════════════════════════════════════════════════════════════
# PART 6: Alternative approach - what if the header bytes are NOT
# encrypted the same way? Maybe the entire 22-byte payload has a
# DIFFERENT structure for 0x1B8B
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("PART 6: Raw PCAP analysis - is the whole payload structure different?")
print("=" * 80)

from pathlib import Path

def read_pcap_streams(filepath):
    with open(filepath, 'rb') as f:
        magic = struct.unpack('<I', f.read(4))[0]
        endian = '<' if magic == 0xa1b2c3d4 else '>'
        f.read(20)
        streams = {}
        while True:
            hdr = f.read(16)
            if len(hdr) < 16: break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
            pdata = f.read(incl_len)
            if len(pdata) < incl_len: break
            if len(pdata) < 20: continue
            ihl = (pdata[0] & 0x0F) * 4
            if pdata[9] != 6: continue
            tcp = pdata[ihl:]
            if len(tcp) < 20: continue
            sp = struct.unpack('>H', tcp[0:2])[0]
            dp = struct.unpack('>H', tcp[2:4])[0]
            toff = ((tcp[12] >> 4) & 0xF) * 4
            pl = tcp[toff:]
            if not pl: continue
            gp = set(range(5990, 5999)) | set(range(7001, 7011))
            if dp in gp:
                streams.setdefault('C2S', bytearray()).extend(pl)
            elif sp in gp:
                streams.setdefault('S2C', bytearray()).extend(pl)
    return streams

def parse_packets(raw):
    packets = []
    pos = 0
    while pos + 4 <= len(raw):
        pkt_len = struct.unpack('<H', raw[pos:pos+2])[0]
        opcode = struct.unpack('<H', raw[pos+2:pos+4])[0]
        if pkt_len < 4 or pkt_len > 65535 or pos + pkt_len > len(raw): break
        packets.append((opcode, bytes(raw[pos:pos+pkt_len])))  # Include full packet!
        pos += pkt_len
    return packets

def extract_sk(s2c):
    for op, raw in s2c:
        if op == 0x0038:
            pl = raw[4:]
            if len(pl) > 100:
                ec = struct.unpack('<H', pl[0:2])[0]
                for idx in range(ec):
                    off = 2 + idx * 12
                    if off + 12 > len(pl): break
                    if struct.unpack('<I', pl[off:off+4])[0] == 0x4F:
                        return struct.unpack('<I', pl[off+4:off+8])[0]
    return None

# Collect all 0x1B8B full packets
pcap_dir = Path(r'D:\CascadeProjects')
pcaps = sorted(pcap_dir.glob('*.pcap'))
for sub in ['rebel_attack', 'codex_lab']:
    p = pcap_dir / sub
    if p.exists(): pcaps.extend(sorted(p.glob('*.pcap')))

samples = []
for pcap in pcaps:
    try:
        s = read_pcap_streams(pcap)
        if 'C2S' not in s or 'S2C' not in s: continue
        c2s = parse_packets(s['C2S'])
        s2c = parse_packets(s['S2C'])
        sk = extract_sk(s2c)
        if not sk: continue
        for op, raw in c2s:
            if op == 0x1B8B:
                samples.append({'pcap': pcap.name, 'raw': raw, 'sk': sk})
    except: continue

print(f"Collected {len(samples)} 0x1B8B packets")

# For each sample, try decrypting with different header assumptions
for i, s in enumerate(samples[:5]):
    raw = s['raw']
    sk_u32 = s['sk']
    sk = [sk_u32 & 0xFF, (sk_u32>>8) & 0xFF, (sk_u32>>16) & 0xFF, (sk_u32>>24) & 0xFF]

    print(f"\n  Sample {i}: {s['pcap']}")
    print(f"    Full packet ({len(raw)}B): {raw.hex()}")
    print(f"    SK: 0x{sk_u32:08X}")

    # Standard header: raw[0:4] = [len, opcode], raw[4:8] = [ck, ml, v, mh]
    # Try: what if the ENTIRE payload starting from byte 4 is encrypted differently?
    payload = raw[4:]  # 22 bytes

    # Hypothesis A: Standard 4-byte crypto header at [4:8], data at [8:]
    ck, ml, v, mh = payload[0], payload[1], payload[2], payload[3]
    enc = payload[4:]
    msg = [ml, mh]
    plain_a = bytearray(len(enc))
    for j in range(len(enc)):
        abs_i = j + 8
        plain_a[j] = ((enc[j] ^ sk[abs_i%4] ^ TABLE[abs_i%7]) - msg[abs_i%2]*17) & 0xFF
    sum_enc = sum(enc) & 0xFF
    print(f"    Hyp A (standard): ck=0x{ck:02X} sum_enc=0x{sum_enc:02X} match={'YES' if ck==sum_enc else 'NO'}")
    print(f"      plain: {plain_a.hex()}")

    # Hypothesis B: 0x1B8B has NO crypto header - entire payload is encrypted starting at abs_i=4
    plain_b = bytearray(len(payload))
    msg_b = [0, 0]  # no msg bytes
    for j in range(len(payload)):
        abs_i = j + 4
        plain_b[j] = ((payload[j] ^ sk[abs_i%4] ^ TABLE[abs_i%7]) - 0) & 0xFF
    print(f"    Hyp B (no header, msg=0): {plain_b.hex()}")

    # Hypothesis C: Different header layout - maybe [ck, v, ml, mh] or [ml, mh, ck, v]
    for order_name, indices in [
        ("ml,mh,ck,v", (0,1,2,3)),    # [ml, mh, ck, v]
        ("v,ck,ml,mh", (2,3,0,1)),    # verify, ck first
        ("mh,ml,v,ck", (3,2,1,0)),    # reversed
    ]:
        m_l = payload[indices[0]]
        m_h = payload[indices[1]]
        c_k = payload[indices[2]]
        ver = payload[indices[3]]
        msg_c = [m_l, m_h]
        enc_c = payload[4:]
        plain_c = bytearray(len(enc_c))
        for j in range(len(enc_c)):
            abs_i = j + 8
            plain_c[j] = ((enc_c[j] ^ sk[abs_i%4] ^ TABLE[abs_i%7]) - msg_c[abs_i%2]*17) & 0xFF
        sum_enc_c = sum(enc_c) & 0xFF
        ck_ok = c_k == sum_enc_c
        v_ok = ver == (m_l ^ 0xB7)
        if ck_ok or v_ok:
            print(f"    Hyp C ({order_name}): ck_ok={ck_ok} v_ok={v_ok}")
            print(f"      plain: {plain_c.hex()}")

# ═══════════════════════════════════════════════════════════════
# PART 7: Check if 0x1B8B uses XOR-only (no *17 multiply)
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("PART 7: Try XOR-only encryption (no *17)")
print("=" * 80)

for i, s in enumerate(samples[:5]):
    raw = s['raw']
    sk_u32 = s['sk']
    sk = [sk_u32 & 0xFF, (sk_u32>>8) & 0xFF, (sk_u32>>16) & 0xFF, (sk_u32>>24) & 0xFF]
    payload = raw[4:]

    # Try: plain[j] = payload[j] ^ sk[j%4] ^ TABLE[j%7]  (no *17, no msg)
    plain_xor = bytearray(len(payload))
    for j in range(len(payload)):
        abs_i = j + 4  # offset from start of full packet
        plain_xor[j] = (payload[j] ^ sk[abs_i%4] ^ TABLE[abs_i%7]) & 0xFF
    print(f"  Sample {i}: XOR-only (abs from 4): {plain_xor.hex()}")

    # Try: abs_i from 0
    plain_xor2 = bytearray(len(payload))
    for j in range(len(payload)):
        plain_xor2[j] = (payload[j] ^ sk[j%4] ^ TABLE[j%7]) & 0xFF
    print(f"  Sample {i}: XOR-only (abs from 0): {plain_xor2.hex()}")

# ═══════════════════════════════════════════════════════════════
# PART 8: What if the mystery encoder at 0x5c6dbb0 is actually
# GoSocket::sendData (no encryption at all)?
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("PART 8: Maybe 0x1B8B sends UNENCRYPTED?")
print("=" * 80)

# If unencrypted, the payload after [len:2][opcode:2] would be raw field data
# From password_check_analysis: 18 bytes of fields
# u16 + u16 + u16 + 4*u8 + u64

for i, s in enumerate(samples[:5]):
    raw = s['raw']
    payload = raw[4:]  # raw after header
    print(f"\n  Sample {i} ({s['pcap']}):")
    print(f"    Raw payload: {payload.hex()}")
    if len(payload) >= 18:
        f1 = struct.unpack('<H', payload[0:2])[0]
        f2 = struct.unpack('<H', payload[2:4])[0]
        f3 = struct.unpack('<H', payload[4:6])[0]
        b1, b2, b3, b4 = payload[6], payload[7], payload[8], payload[9]
        f4 = struct.unpack('<Q', payload[10:18])[0]
        print(f"    As unencrypted: u16={f1}, u16={f2}, u16={f3}, bytes=[{b1},{b2},{b3},{b4}], u64=0x{f4:016X}")
    if len(payload) >= 22:
        # Maybe 4 extra bytes at start are crypto header, rest is unencrypted
        f1 = struct.unpack('<H', payload[4:6])[0]
        f2 = struct.unpack('<H', payload[6:8])[0]
        f3 = struct.unpack('<H', payload[8:10])[0]
        b1, b2, b3, b4 = payload[10], payload[11], payload[12], payload[13]
        f4 = struct.unpack('<Q', payload[14:22])[0]
        print(f"    With 4B header: u16={f1}, u16={f2}, u16={f3}, bytes=[{b1},{b2},{b3},{b4}], u64=0x{f4:016X}")

print("\nDone.")

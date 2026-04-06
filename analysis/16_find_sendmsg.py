#!/usr/bin/env python3
"""
16_find_sendmsg.py - Find the real game sendMsg and packet dispatch
====================================================================
Strategy:
1. Find GoSocket::sendData callers (the final TCP send point)
2. Find doEncode callers (where encryption happens before send)
3. Trace backward from encode to find where opcodes are written to packets
4. Find registerListener string references for handler registration
"""

import struct, os
from collections import defaultdict

try:
    from capstone import *
except:
    os.system("pip install capstone")
    from capstone import *

LIBGAME = r"D:\CascadeProjects\libgame.so"
FINDINGS_DIR = r"D:\CascadeProjects\analysis\findings"
os.makedirs(FINDINGS_DIR, exist_ok=True)

# Known addresses
ENCODE_ADDR = 0x04F97C24    # doEncode function
DECODE_ADDR = 0x04F97D40    # doDecode function
GOSOCKET_SEND = 0x04F95CA8  # GoSocket::sendData
SENDMSG_STR = 0x00684FFF    # "sendMsg" string in dynstr

def read_binary():
    with open(LIBGAME, "rb") as f:
        return f.read()

def find_sections(data):
    """Find .text and .rodata sections"""
    e_shoff = struct.unpack_from("<Q", data, 0x28)[0]
    e_shentsize = struct.unpack_from("<H", data, 0x3A)[0]
    e_shnum = struct.unpack_from("<H", data, 0x3C)[0]
    e_shstrndx = struct.unpack_from("<H", data, 0x3E)[0]
    str_sh_offset = e_shoff + e_shstrndx * e_shentsize
    str_sh_off = struct.unpack_from("<Q", data, str_sh_offset + 0x18)[0]

    sections = {}
    for i in range(e_shnum):
        sh_offset = e_shoff + i * e_shentsize
        sh_name_idx = struct.unpack_from("<I", data, sh_offset)[0]
        sh_addr = struct.unpack_from("<Q", data, sh_offset + 0x10)[0]
        sh_off = struct.unpack_from("<Q", data, sh_offset + 0x18)[0]
        sh_size = struct.unpack_from("<Q", data, sh_offset + 0x20)[0]
        name_end = data.index(b'\x00', str_sh_off + sh_name_idx)
        name = data[str_sh_off + sh_name_idx:name_end].decode('ascii', errors='replace')
        sections[name] = (sh_addr, sh_off, sh_size)
    return sections

def find_bl_callers(data, text_addr, text_off, text_size, target_addr):
    """Find all BL instructions that call target_addr"""
    callers = []
    text_data = data[text_off:text_off + text_size]

    for offset in range(0, text_size, 4):
        insn = struct.unpack_from("<I", text_data, offset)[0]
        # BL imm26: 1001_01_imm26
        if (insn & 0xFC000000) != 0x94000000:
            continue
        imm26 = insn & 0x03FFFFFF
        # Sign extend 26-bit to proper signed Python int
        if imm26 >= 0x02000000:
            imm26 -= 0x04000000

        pc = text_addr + offset
        dest = (pc + imm26 * 4) & 0xFFFFFFFF

        if dest == target_addr:
            callers.append(pc)

    return callers

def find_function_entry(data, text_addr, text_off, addr):
    """Walk backward to find function prologue (STP X29, X30 or SUB SP)"""
    for back in range(4, 2000, 4):
        check_addr = addr - back
        file_off = text_off + (check_addr - text_addr)
        if file_off < text_off:
            break
        insn = struct.unpack_from("<I", data, file_off)[0]

        # STP X29, X30, [SP, #-N]! (push frame pointer)
        if (insn & 0xFFE07FFF) == 0xA9A07BFD or (insn & 0xFFE003FF) == 0xA9807BFD:
            return check_addr
        # SUB SP, SP, #imm (allocate stack frame)
        if (insn & 0xFFC003FF) == 0xD10003FF:
            return check_addr
    return addr - 200  # fallback

def disasm_range(data, text_addr, text_off, start, count):
    """Disassemble 'count' instructions from start"""
    md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
    md.detail = True

    file_off = text_off + (start - text_addr)
    code = data[file_off:file_off + count * 4]

    lines = []
    for insn in md.disasm(code, start):
        lines.append(f"  0x{insn.address:08X}:  {insn.mnemonic:12s} {insn.op_str}")
    return "\n".join(lines)

def find_string_refs(data, text_addr, text_off, text_size, rodata_addr, rodata_off, rodata_size, search_strings):
    """Find ADRP+ADD pairs that reference specific strings in .rodata"""
    results = defaultdict(list)
    text_data = data[text_off:text_off + text_size]

    # First, find string offsets in rodata
    string_addrs = {}
    for s in search_strings:
        s_bytes = s.encode('ascii')
        search_start = rodata_off
        search_end = rodata_off + rodata_size
        idx = data.find(s_bytes, search_start, search_end)
        while idx != -1:
            str_addr = rodata_addr + (idx - rodata_off)
            string_addrs[str_addr] = s
            idx = data.find(s_bytes, idx + 1, search_end)

    print(f"  Found {len(string_addrs)} string locations in .rodata")

    # Now scan .text for ADRP+ADD pairs pointing to these
    CHUNK = 4 * 1024 * 1024
    for chunk_start in range(0, text_size, CHUNK):
        chunk_end = min(chunk_start + CHUNK, text_size)
        chunk_data = text_data[chunk_start:chunk_end]
        chunk_addr = text_addr + chunk_start

        for offset in range(0, len(chunk_data) - 8, 4):
            insn = struct.unpack_from("<I", chunk_data, offset)[0]

            if (insn & 0x9F000000) != 0x90000000:
                continue

            immhi = (insn >> 5) & 0x7FFFF
            immlo = (insn >> 29) & 0x3
            imm = (immhi << 2) | immlo
            if imm & 0x100000:
                imm |= ~0x1FFFFF
                imm &= 0xFFFFFFFFFFFFFFFF

            pc_page = (chunk_addr + offset) & ~0xFFF
            target_page = (pc_page + (imm << 12)) & 0xFFFFFFFFFFFFFFFF
            rd = insn & 0x1F

            # Check ADD after ADRP
            if offset + 4 < len(chunk_data):
                next_insn = struct.unpack_from("<I", chunk_data, offset + 4)[0]
                if (next_insn & 0xFFC00000) == 0x91000000:
                    add_imm = (next_insn >> 10) & 0xFFF
                    add_rn = (next_insn >> 5) & 0x1F

                    if add_rn == rd:
                        full_addr = target_page + add_imm
                        if full_addr in string_addrs:
                            results[string_addrs[full_addr]].append(chunk_addr + offset)

    return results

def main():
    print("Loading libgame.so...")
    data = read_binary()
    sections = find_sections(data)

    text_addr, text_off, text_size = sections['.text']
    rodata_addr, rodata_off, rodata_size = sections['.rodata']

    print(f".text: 0x{text_addr:X}, size={text_size:,}")
    print(f".rodata: 0x{rodata_addr:X}, size={rodata_size:,}")

    report = []
    report.append("# Real Game Packet Send/Receive Analysis")
    report.append("")

    # 1. Find doEncode callers
    print("\n=== Finding doEncode callers ===")
    encode_callers = find_bl_callers(data, text_addr, text_off, text_size, ENCODE_ADDR)
    print(f"  Found {len(encode_callers)} callers of doEncode (0x{ENCODE_ADDR:08X})")

    report.append("## 1. doEncode Callers")
    report.append(f"Found **{len(encode_callers)}** functions that call doEncode at 0x{ENCODE_ADDR:08X}")
    report.append("")

    for i, caller in enumerate(encode_callers[:30]):
        func_entry = find_function_entry(data, text_addr, text_off, caller)
        report.append(f"### Caller {i+1}: BL at 0x{caller:08X} (function ~0x{func_entry:08X})")
        report.append("```asm")
        report.append(disasm_range(data, text_addr, text_off, func_entry, 80))
        report.append("```")
        report.append("")
        print(f"  Caller {i+1}: 0x{caller:08X} (func ~0x{func_entry:08X})")

    # 2. Find GoSocket::sendData callers
    print("\n=== Finding GoSocket::sendData callers ===")
    send_callers = find_bl_callers(data, text_addr, text_off, text_size, GOSOCKET_SEND)
    print(f"  Found {len(send_callers)} callers of sendData (0x{GOSOCKET_SEND:08X})")

    report.append("## 2. GoSocket::sendData Callers")
    report.append(f"Found **{len(send_callers)}** functions that call sendData at 0x{GOSOCKET_SEND:08X}")
    report.append("")

    for i, caller in enumerate(send_callers[:20]):
        func_entry = find_function_entry(data, text_addr, text_off, caller)
        report.append(f"### sendData Caller {i+1}: BL at 0x{caller:08X} (function ~0x{func_entry:08X})")
        report.append("```asm")
        report.append(disasm_range(data, text_addr, text_off, func_entry, 60))
        report.append("```")
        report.append("")
        print(f"  sendData Caller {i+1}: 0x{caller:08X}")

    # 3. Find doDecode callers
    print("\n=== Finding doDecode callers ===")
    decode_callers = find_bl_callers(data, text_addr, text_off, text_size, DECODE_ADDR)
    print(f"  Found {len(decode_callers)} callers of doDecode (0x{DECODE_ADDR:08X})")

    report.append("## 3. doDecode Callers")
    report.append(f"Found **{len(decode_callers)}** functions that call doDecode at 0x{DECODE_ADDR:08X}")
    report.append("")

    for i, caller in enumerate(decode_callers[:20]):
        func_entry = find_function_entry(data, text_addr, text_off, caller)
        report.append(f"### doDecode Caller {i+1}: BL at 0x{caller:08X} (function ~0x{func_entry:08X})")
        report.append("```asm")
        report.append(disasm_range(data, text_addr, text_off, func_entry, 60))
        report.append("```")
        report.append("")
        print(f"  doDecode Caller {i+1}: 0x{caller:08X}")

    # 4. Find "sendMsg" and "registerListener" string references
    print("\n=== Finding sendMsg/registerListener string refs ===")
    str_refs = find_string_refs(
        data, text_addr, text_off, text_size,
        rodata_addr, rodata_off, rodata_size,
        ["sendMsg", "registerListener", "CMsgCodec", "doDecode", "doEncode"]
    )

    report.append("## 4. Key String References")
    for s, addrs in str_refs.items():
        report.append(f"\n### \"{s}\" - {len(addrs)} references")
        for addr in addrs[:5]:
            report.append(f"  - 0x{addr:08X}")

    # 5. Find the encode variant functions (other CMSG_TABLE xrefs)
    print("\n=== Checking encode variant at 0x04F97F40 ===")
    variant_callers = find_bl_callers(data, text_addr, text_off, text_size, 0x04F97F40)
    print(f"  Found {len(variant_callers)} callers of encode variant")

    report.append("\n## 5. doEncode Variant (0x04F97F40) Callers")
    report.append(f"Found **{len(variant_callers)}** callers")
    for i, caller in enumerate(variant_callers[:10]):
        func_entry = find_function_entry(data, text_addr, text_off, caller)
        report.append(f"### Variant Caller {i+1}: BL at 0x{caller:08X} (function ~0x{func_entry:08X})")
        report.append("```asm")
        report.append(disasm_range(data, text_addr, text_off, func_entry, 60))
        report.append("```")

    # Write report
    out_path = os.path.join(FINDINGS_DIR, "sendmsg_analysis.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report))

    print(f"\nReport: {out_path} ({len(report)} lines)")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Full disassembly of 0x1B8B related functions from libgame.so
============================================================
1. LogicPassword::encodePassword (0x039FAD00)
2. CMSG_PASSWORD_CHECK_REQUEST::packData (0x05273690)
3. CMSG_PASSWORD_CHECK_REQUEST::C1 constructor (0x0527367C)
4. PLT 0x5c6dbb0 resolution
5. send-check helper (0x039FAC60)
6. loadLocalPassword (0x039FB2C8)
"""
import struct
from capstone import *

LIBGAME = r"D:\CascadeProjects\libgame.so"
with open(LIBGAME, "rb") as f:
    data = f.read()

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

def disasm_func(addr, max_insns=300, label=""):
    """Disassemble a function until RET or max_insns."""
    code = data[addr:addr + max_insns * 4]
    insns = list(md.disasm(code, addr))
    print(f"\n{'='*80}")
    print(f"  {label} @ 0x{addr:08X}")
    print(f"{'='*80}")
    
    ret_count = 0
    for i, insn in enumerate(insns):
        line = f"  0x{insn.address:08X}: {insn.mnemonic:10s} {insn.op_str}"
        
        # Annotate BL calls
        if insn.mnemonic in ('bl', 'b') and '#' in insn.op_str:
            try:
                target = int(insn.op_str.split('#')[1], 0)
                name = resolve_symbol(target)
                if name:
                    line += f"  ; {name}"
            except:
                pass
        
        # Annotate immediate values
        if insn.mnemonic == 'mov' or insn.mnemonic == 'movz':
            if '#' in insn.op_str:
                try:
                    val = int(insn.op_str.split('#')[1].split(',')[0], 0)
                    if val == 0xF4240:
                        line += "  ; = 1,000,000"
                    elif val == 0x4240:
                        line += "  ; low16 of 1,000,000 (0xF4240)"
                    elif val == 0x000F:
                        line += "  ; high16 of 1,000,000"
                    elif val == 0x2710:
                        line += "  ; = 10,000"
                    elif val == 0x186A0:
                        line += "  ; = 100,000"
                    elif val == 0x86a0:
                        line += "  ; low16 of 100,000"
                    elif val == 0xB7:
                        line += "  ; 0xB7 verify XOR constant"
                    elif val == 0x1B8B:
                        line += "  ; OPCODE 0x1B8B"
                except:
                    pass
        
        # Annotate ADRP for string references
        if insn.mnemonic == 'adrp':
            try:
                page = int(insn.op_str.split('#')[1], 0)
                line += f"  ; page=0x{page:08X}"
            except:
                pass
        
        print(line)
        
        if insn.mnemonic == 'ret':
            ret_count += 1
            if ret_count >= 1 and i > 3:
                # Check if this looks like end of function
                break
    
    return insns

# Known symbols for annotation
KNOWN_SYMBOLS = {
    0x05C6DBA0: "CMsgCodec::Encode",
    0x05C6DBB0: "UNKNOWN_ENCODER (PLT)",
    0x05C6DBC0: "PLT_unknown_2",
    0x05C6DBD0: "PLT_write_u16?",
    0x05C6DBE0: "PLT_write_u64?",
    0x05C21690: "LogicPassword::delayResetPassword",
    0x05C216A0: "CMainUI::updateSecondaryPassword",
    0x05C21700: "LogicPassword::loadLocalPassword",
    0x05C21710: "CMSG_PASSWORD_CHECK_RETURN::C1",
    0x05C21720: "LogicPassword::setSecondaryPasswordErrorCount",
    0x05C21730: "LogicPassword::decodePassword",
    0x05C21740: "LogicPassword::saveLocalPassword",
    0x05C21790: "CMSG_PASSWORD_CHECK_REQUEST::C1",
    0x05C217A0: "LogicPassword::encodePassword",
    0x05C217B0: "CMSG_PASSWORD_CHECK_REQUEST::packData",
    0x05BDCA50: "MessageSubject::singleton",
    0x05BDCD10: "MessageSubject::sendMsg",
    0x05BDD240: "std::string::assign",
    0x05BDCD20: "std::string::operator=",
    0x05BDC440: "operator new",
    0x05BDC460: "operator delete",
    0x05BDE040: "atoi",
    0x05BE1130: "cocos2d::RandomHelper::getEngine",
    0x05BEB7F0: "uniform_int_distribution::operator()(mt19937)",
    0x05BDC4A0: "__stack_chk_fail",
    0x039FAD00: "LogicPassword::encodePassword (REAL)",
    0x039FAC60: "send_check_password_helper",
    0x039FB2C8: "LogicPassword::loadLocalPassword (REAL)",
    0x05273690: "CMSG_PASSWORD_CHECK_REQUEST::packData (REAL)",
    0x0527367C: "CMSG_PASSWORD_CHECK_REQUEST::C1 (REAL)",
    0x034616E0: "uniform_int_distribution (REAL)",
    0x057DA9F8: "RandomHelper::getEngine (REAL)",
    0x03B83964: "MessageSubject::singleton (REAL)",
    0x03B842E4: "MessageSubject::sendMsg (REAL)",
}

def resolve_symbol(addr):
    return KNOWN_SYMBOLS.get(addr, None)

# ═══════════════════════════════════════════════════════════════
# 1. encodePassword - THE KEY FUNCTION
# ═══════════════════════════════════════════════════════════════
disasm_func(0x039FAD00, 200, "LogicPassword::encodePassword(string&, int)")

# ═══════════════════════════════════════════════════════════════
# 2. send-check helper - builds and sends the packet
# ═══════════════════════════════════════════════════════════════
disasm_func(0x039FAC60, 100, "send_check_password_helper")

# ═══════════════════════════════════════════════════════════════
# 3. CMSG_PASSWORD_CHECK_REQUEST constructor
# ═══════════════════════════════════════════════════════════════
disasm_func(0x0527367C, 20, "CMSG_PASSWORD_CHECK_REQUEST::C1")

# ═══════════════════════════════════════════════════════════════
# 4. CMSG_PASSWORD_CHECK_REQUEST::packData - THE ENCODER
# ═══════════════════════════════════════════════════════════════
disasm_func(0x05273690, 300, "CMSG_PASSWORD_CHECK_REQUEST::packData")

# ═══════════════════════════════════════════════════════════════
# 5. Resolve PLT 0x5c6dbb0
# ═══════════════════════════════════════════════════════════════
print(f"\n{'='*80}")
print(f"  PLT RESOLUTION: 0x05C6DBB0")
print(f"{'='*80}")

# Read PLT stub
plt_code = data[0x05C6DBB0:0x05C6DBB0 + 16]
plt_insns = list(md.disasm(plt_code, 0x05C6DBB0))
for insn in plt_insns:
    print(f"  0x{insn.address:08X}: {insn.mnemonic:10s} {insn.op_str}")

# Resolve GOT
if len(plt_insns) >= 2 and plt_insns[0].mnemonic == 'adrp':
    try:
        page = int(plt_insns[0].op_str.split('#')[1], 0)
        off_str = plt_insns[1].op_str
        off = int(off_str.split('#')[1].rstrip(']'), 0)
        got_addr = page + off
        got_val = struct.unpack('<Q', data[got_addr:got_addr+8])[0]
        print(f"  GOT @ 0x{got_addr:08X} -> 0x{got_val:016X}")
        
        if got_val != 0x05C6DBB0 and got_val > 0x03000000:
            print(f"\n  REAL FUNCTION at 0x{got_val:08X}:")
            disasm_func(got_val, 200, f"PLT 0x5C6DBB0 -> REAL @ 0x{got_val:08X}")
    except Exception as e:
        print(f"  Resolution failed: {e}")

# Also resolve PLT 0x5c6dba0 (CMsgCodec::Encode) for comparison
print(f"\n{'='*80}")
print(f"  PLT RESOLUTION: 0x05C6DBA0 (CMsgCodec::Encode)")
print(f"{'='*80}")
plt_code2 = data[0x05C6DBA0:0x05C6DBA0 + 16]
plt_insns2 = list(md.disasm(plt_code2, 0x05C6DBA0))
for insn in plt_insns2:
    print(f"  0x{insn.address:08X}: {insn.mnemonic:10s} {insn.op_str}")
if len(plt_insns2) >= 2 and plt_insns2[0].mnemonic == 'adrp':
    try:
        page = int(plt_insns2[0].op_str.split('#')[1], 0)
        off_str = plt_insns2[1].op_str
        off = int(off_str.split('#')[1].rstrip(']'), 0)
        got_addr = page + off
        got_val = struct.unpack('<Q', data[got_addr:got_addr+8])[0]
        print(f"  GOT @ 0x{got_addr:08X} -> 0x{got_val:016X}")
    except:
        pass

# ═══════════════════════════════════════════════════════════════
# 6. loadLocalPassword - to understand what password is loaded
# ═══════════════════════════════════════════════════════════════
disasm_func(0x039FB2C8, 300, "LogicPassword::loadLocalPassword")

# ═══════════════════════════════════════════════════════════════
# 7. Check rodata strings near encodePassword references
# ═══════════════════════════════════════════════════════════════
print(f"\n{'='*80}")
print(f"  RODATA STRINGS near password functions")
print(f"{'='*80}")

# Search for "SecondaryPassword" string
search = b"SecondaryPassword"
pos = 0
while True:
    pos = data.find(search, pos)
    if pos == -1: break
    context = data[pos:pos+40]
    print(f"  Found at 0x{pos:08X}: {context}")
    pos += 1

# Search for format strings used by encodePassword
for s in [b"%d", b"password", b"Password"]:
    pos = 0
    count = 0
    while count < 5:
        pos = data.find(s, pos)
        if pos == -1: break
        if pos > 0x02000000:  # Only in rodata area
            context = data[max(0,pos-4):pos+len(s)+20]
            try:
                print(f"  '{s.decode()}' at 0x{pos:08X}: {context[:30]}")
            except:
                pass
            count += 1
        pos += 1

# ═══════════════════════════════════════════════════════════════
# 8. CMsgCodec::Encode (real) for comparison
# ═══════════════════════════════════════════════════════════════
disasm_func(0x04F97C24, 150, "CMsgCodec::Encode (REAL at 0x04F97C24)")

print("\n\nDONE")

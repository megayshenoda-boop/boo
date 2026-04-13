#!/usr/bin/env python3
"""
ARM64 (AArch64) disassembler for CMSG_START_MARCH_NEW::packData
Reads raw bytes from libgame_new.so and decodes instructions.
"""
import struct
import sys

BINARY_PATH = r"D:\CascadeProjects\libgame_new.so"

# We'll read from constructor start to get full context
CONSTRUCTOR_OFFSET = 0x05212268
PACKDATA_OFFSET    = 0x05212294
READ_SIZE          = 1252 + (PACKDATA_OFFSET - CONSTRUCTOR_OFFSET)  # include constructor preamble

# ARM64 condition codes
COND_CODES = {
    0: "EQ", 1: "NE", 2: "CS/HS", 3: "CC/LO",
    4: "MI", 5: "PL", 6: "VS", 7: "VC",
    8: "HI", 9: "LS", 10: "GE", 11: "LT",
    12: "GT", 13: "LE", 14: "AL",
}

REG_NAMES_64 = {i: f"X{i}" for i in range(31)}
REG_NAMES_64[31] = "SP"  # or XZR depending on context
REG_NAMES_32 = {i: f"W{i}" for i in range(31)}
REG_NAMES_32[31] = "WZR"

def reg64(n):
    if n == 31: return "SP"
    return f"X{n}"

def reg64z(n):
    """X-register or XZR for zero register context"""
    if n == 31: return "XZR"
    return f"X{n}"

def reg32(n):
    if n == 31: return "WZR"
    return f"W{n}"

def sign_extend(val, bits):
    if val & (1 << (bits - 1)):
        val -= (1 << bits)
    return val

def decode_arm64(insn_word, addr):
    """Decode a single ARM64 instruction word. Returns (mnemonic, detail_str, flags)."""
    flags = []

    op = insn_word

    # NOP
    if op == 0xD503201F:
        return "NOP", "", []

    # RET
    if (op & 0xFFFFFC1F) == 0xD65F0000:
        rn = (op >> 5) & 0x1F
        return "RET", reg64(rn) if rn != 30 else "", []

    # BR / BLR
    if (op & 0xFFFFFC1F) == 0xD61F0000:
        rn = (op >> 5) & 0x1F
        return "BR", reg64(rn), []
    if (op & 0xFFFFFC1F) == 0xD63F0000:
        rn = (op >> 5) & 0x1F
        return "BLR", reg64(rn), ["CALL"]

    # B (unconditional branch)
    if (op >> 26) == 0b000101:
        imm26 = op & 0x03FFFFFF
        offset = sign_extend(imm26, 26) * 4
        target = addr + offset
        return "B", f"0x{target:08X}", ["BRANCH"]

    # BL (branch with link = function call)
    if (op >> 26) == 0b100101:
        imm26 = op & 0x03FFFFFF
        offset = sign_extend(imm26, 26) * 4
        target = addr + offset
        return "BL", f"0x{target:08X}", ["CALL"]

    # B.cond (conditional branch)
    if (op & 0xFF000010) == 0x54000000:
        cond = op & 0xF
        imm19 = (op >> 5) & 0x7FFFF
        offset = sign_extend(imm19, 19) * 4
        target = addr + offset
        cname = COND_CODES.get(cond, f"?{cond}")
        return f"B.{cname}", f"0x{target:08X}", ["BRANCH"]

    # CBZ / CBNZ
    if (op & 0x7E000000) == 0x34000000:
        sf = (op >> 31) & 1
        is_nz = (op >> 24) & 1
        imm19 = (op >> 5) & 0x7FFFF
        rt = op & 0x1F
        offset = sign_extend(imm19, 19) * 4
        target = addr + offset
        rname = reg64(rt) if sf else reg32(rt)
        mnem = "CBNZ" if is_nz else "CBZ"
        return mnem, f"{rname}, 0x{target:08X}", ["BRANCH"]

    # TBZ / TBNZ
    if (op & 0x7E000000) == 0x36000000:
        b5 = (op >> 31) & 1
        is_nz = (op >> 24) & 1
        b40 = (op >> 19) & 0x1F
        bit = (b5 << 5) | b40
        imm14 = (op >> 5) & 0x3FFF
        rt = op & 0x1F
        offset = sign_extend(imm14, 14) * 4
        target = addr + offset
        mnem = "TBNZ" if is_nz else "TBZ"
        rname = reg64(rt) if b5 else reg32(rt)
        return mnem, f"{rname}, #{bit}, 0x{target:08X}", ["BRANCH"]

    # STP / LDP (pre/post-index, signed offset) - Load/Store Pair
    if (op & 0x3E000000) == 0x28000000:
        opc = (op >> 30) & 3
        is_vector = (op >> 26) & 1
        mode = (op >> 23) & 3  # 0=no-alloc, 1=post, 2=signed-offset, 3=pre
        is_load = (op >> 22) & 1
        imm7 = (op >> 15) & 0x7F
        rt2 = (op >> 10) & 0x1F
        rn = (op >> 5) & 0x1F
        rt = op & 0x1F

        if not is_vector:
            sf = 1 if opc & 2 else 0  # opc=0 -> 32bit, opc=2 -> 64bit
            scale = 3 if sf else 2
        else:
            scale = opc + 2
            sf = 1 if opc >= 2 else 0

        offset = sign_extend(imm7, 7) << scale

        if not is_vector:
            r1 = reg64(rt) if sf else reg32(rt)
            r2 = reg64(rt2) if sf else reg32(rt2)
        else:
            r1 = f"Q{rt}" if opc == 2 else f"D{rt}" if opc == 1 else f"S{rt}"
            r2 = f"Q{rt2}" if opc == 2 else f"D{rt2}" if opc == 1 else f"S{rt2}"

        base = reg64(rn)
        mnem = "LDP" if is_load else "STP"

        flag_list = []
        if is_load:
            flag_list.append("LOAD")
        else:
            flag_list.append("STORE")
        if abs(offset) <= 0x10 and rn in range(20):  # struct access heuristic
            flag_list.append("STRUCT_ACCESS")

        if mode == 1:  # post-index
            detail = f"{r1}, {r2}, [{base}], #{offset}"
        elif mode == 3:  # pre-index
            detail = f"{r1}, {r2}, [{base}, #{offset}]!"
        else:  # signed offset
            if offset == 0:
                detail = f"{r1}, {r2}, [{base}]"
            else:
                detail = f"{r1}, {r2}, [{base}, #{offset}]"

        return mnem, detail, flag_list

    # LDR/STR (immediate, unsigned offset) - most common form
    # Also LDRB, LDRH, LDRSB, LDRSH, LDRSW, STRB, STRH
    if (op & 0x3B000000) == 0x39000000:
        size = (op >> 30) & 3  # 0=byte, 1=half, 2=word, 3=dword
        is_vector = (op >> 26) & 1
        opc = (op >> 22) & 3  # 0=store, 1=load, 2=load-signed(64), 3=load-signed(32)
        imm12 = (op >> 10) & 0xFFF
        rn = (op >> 5) & 0x1F
        rt = op & 0x1F

        scale = size
        offset = imm12 << scale

        flag_list = []

        if is_vector:
            if size == 0 and opc == 0:
                mnem = "STR"
                rname = f"B{rt}"
            elif size == 0 and opc == 1:
                mnem = "LDR"
                rname = f"B{rt}"
            elif size == 1 and opc == 0:
                mnem = "STR"
                rname = f"H{rt}"
            elif size == 1 and opc == 1:
                mnem = "LDR"
                rname = f"H{rt}"
            elif size == 2 and opc == 0:
                mnem = "STR"
                rname = f"S{rt}"
            elif size == 2 and opc == 1:
                mnem = "LDR"
                rname = f"S{rt}"
            elif size == 3 and opc == 0:
                mnem = "STR"
                rname = f"D{rt}"
            elif size == 3 and opc == 1:
                mnem = "LDR"
                rname = f"D{rt}"
            else:
                mnem = "LDR/STR(V)"
                rname = f"V{rt}"
            flag_list.append("VECTOR")
        else:
            if opc == 0:
                flag_list.append("STORE")
                if size == 0: mnem = "STRB"
                elif size == 1: mnem = "STRH"
                elif size == 2: mnem = "STR"
                else: mnem = "STR"
                rname = reg32(rt) if size < 3 else reg64(rt)
            elif opc == 1:
                flag_list.append("LOAD")
                if size == 0: mnem = "LDRB"
                elif size == 1: mnem = "LDRH"
                elif size == 2: mnem = "LDR"
                else: mnem = "LDR"
                rname = reg32(rt) if size < 3 else reg64(rt)
            elif opc == 2:
                flag_list.append("LOAD")
                if size == 0: mnem = "LDRSB"
                elif size == 1: mnem = "LDRSH"
                elif size == 2: mnem = "LDRSW"
                else: mnem = "PRFM"
                rname = reg64(rt) if size < 2 else reg64(rt) if size == 2 else f"#{rt}"
            else:
                flag_list.append("LOAD")
                if size == 0: mnem = "LDRSB"
                elif size == 1: mnem = "LDRSH"
                else: mnem = f"LDR?{size}.{opc}"
                rname = reg32(rt)

        base = reg64(rn)

        # Flag struct offset accesses
        if offset <= 0x80:
            flag_list.append(f"OFF=0x{offset:02X}")

        if offset == 0:
            detail = f"{rname}, [{base}]"
        else:
            detail = f"{rname}, [{base}, #0x{offset:X}]"

        return mnem, detail, flag_list

    # LDR/STR (register offset)
    if (op & 0x3B200C00) == 0x38200800:
        size = (op >> 30) & 3
        is_vector = (op >> 26) & 1
        opc = (op >> 22) & 3
        rm = (op >> 16) & 0x1F
        option = (op >> 13) & 7
        S = (op >> 12) & 1
        rn = (op >> 5) & 0x1F
        rt = op & 0x1F

        if opc == 0:
            if size == 0: mnem = "STRB"
            elif size == 1: mnem = "STRH"
            elif size == 2: mnem = "STR"
            else: mnem = "STR"
        else:
            if size == 0: mnem = "LDRB"
            elif size == 1: mnem = "LDRH"
            elif size == 2: mnem = "LDR"
            else: mnem = "LDR"

        rname = reg64(rt) if size == 3 else reg32(rt)
        ext_map = {2: "UXTW", 3: "LSL", 6: "SXTW", 7: "SXTX"}
        ext = ext_map.get(option, f"?{option}")
        rmn = reg64(rm) if option in (3, 7) else reg32(rm)

        if S and size > 0:
            detail = f"{rname}, [{reg64(rn)}, {rmn}, {ext} #{size}]"
        elif ext != "LSL":
            detail = f"{rname}, [{reg64(rn)}, {rmn}, {ext}]"
        else:
            detail = f"{rname}, [{reg64(rn)}, {rmn}]"

        return mnem, detail, ["LOAD" if opc else "STORE", "REG_OFF"]

    # LDR/STR (pre/post index)
    if (op & 0x3B200000) == 0x38000000:
        size = (op >> 30) & 3
        is_vector = (op >> 26) & 1
        opc = (op >> 22) & 3
        imm9 = (op >> 12) & 0x1FF
        idx_type = (op >> 10) & 3  # 0=unscaled, 1=post, 3=pre
        rn = (op >> 5) & 0x1F
        rt = op & 0x1F

        simm = sign_extend(imm9, 9)

        if opc == 0:
            if size == 0: mnem = "STRB"
            elif size == 1: mnem = "STRH"
            elif size == 2: mnem = "STR"
            else: mnem = "STR"
            flag_list = ["STORE"]
        elif opc == 1:
            if size == 0: mnem = "LDRB"
            elif size == 1: mnem = "LDRH"
            elif size == 2: mnem = "LDR"
            else: mnem = "LDR"
            flag_list = ["LOAD"]
        elif opc == 2:
            if size == 0: mnem = "LDRSB"
            elif size == 1: mnem = "LDRSH"
            elif size == 2: mnem = "LDRSW"
            else: mnem = "PRFM"
            flag_list = ["LOAD"]
        else:
            if size == 0: mnem = "LDRSB"
            elif size == 1: mnem = "LDRSH"
            else: mnem = f"LDR?{size}.{opc}"
            flag_list = ["LOAD"]

        rname = reg64(rt) if (size == 3 or (opc == 2 and size < 3)) else reg32(rt)
        base = reg64(rn)

        if idx_type == 0:  # unscaled
            mnem = "LDUR" if opc else "STUR"
            if size == 0: mnem += "B"
            elif size == 1: mnem += "H"
            detail = f"{rname}, [{base}, #{simm}]"
        elif idx_type == 1:  # post
            detail = f"{rname}, [{base}], #{simm}"
        elif idx_type == 3:  # pre
            detail = f"{rname}, [{base}, #{simm}]!"
        else:
            detail = f"{rname}, [{base}, #{simm}] (unprivileged)"

        if abs(simm) <= 0x80:
            flag_list.append(f"OFF={simm}")

        return mnem, detail, flag_list

    # LDR (literal) - PC-relative
    if (op & 0x3B000000) == 0x18000000:
        opc = (op >> 30) & 3
        is_vector = (op >> 26) & 1
        imm19 = (op >> 5) & 0x7FFFF
        rt = op & 0x1F
        offset = sign_extend(imm19, 19) * 4
        target = addr + offset

        if is_vector:
            sz = {0: "S", 1: "D", 2: "Q"}.get(opc, "?")
            rname = f"{sz}{rt}"
        else:
            rname = reg32(rt) if opc == 0 else reg64(rt)
            if opc == 2:
                return "LDRSW", f"{reg64(rt)}, 0x{target:08X}", ["LOAD", "PC_REL"]

        return "LDR", f"{rname}, 0x{target:08X}", ["LOAD", "PC_REL"]

    # ADRP
    if (op & 0x9F000000) == 0x90000000:
        rd = op & 0x1F
        immlo = (op >> 29) & 3
        immhi = (op >> 5) & 0x7FFFF
        imm = sign_extend((immhi << 2) | immlo, 21) << 12
        target = (addr & ~0xFFF) + imm
        return "ADRP", f"{reg64(rd)}, 0x{target:08X}", ["ADDR"]

    # ADR
    if (op & 0x9F000000) == 0x10000000:
        rd = op & 0x1F
        immlo = (op >> 29) & 3
        immhi = (op >> 5) & 0x7FFFF
        imm = sign_extend((immhi << 2) | immlo, 21)
        target = addr + imm
        return "ADR", f"{reg64(rd)}, 0x{target:08X}", ["ADDR"]

    # ADD/SUB (immediate)
    if (op & 0x1F000000) == 0x11000000:
        sf = (op >> 31) & 1
        is_sub = (op >> 30) & 1
        S = (op >> 29) & 1
        sh = (op >> 22) & 1
        imm12 = (op >> 10) & 0xFFF
        rn = (op >> 5) & 0x1F
        rd = op & 0x1F

        val = imm12 << (12 if sh else 0)

        rdn = reg64 if sf else reg32

        if is_sub and S and rd == 31:
            mnem = "CMP" if not is_sub or S else "CMN"
            if S and is_sub:
                return "CMP", f"{rdn(rn)}, #0x{val:X}", ["CMP"]

        if is_sub:
            mnem = "SUBS" if S else "SUB"
        else:
            mnem = "ADDS" if S else "ADD"

        if not is_sub and rd == 31 and S:
            mnem = "CMN"
            return mnem, f"{rdn(rn)}, #0x{val:X}", ["CMP"]

        # MOV alias for ADD Xd, SP, #0 or ADD SP, Xn, #0
        if not is_sub and not S and val == 0 and (rd == 31 or rn == 31):
            return "MOV", f"{rdn(rd)}, {rdn(rn)}", []

        detail = f"{rdn(rd)}, {rdn(rn)}, #0x{val:X}"

        flag_list = []
        # Check if this is adjusting struct pointer offset
        if val <= 0x80 and not is_sub:
            flag_list.append(f"OFF=0x{val:02X}")

        return mnem, detail, flag_list

    # ADD/SUB (shifted register)
    if (op & 0x1F200000) == 0x0B000000:
        sf = (op >> 31) & 1
        is_sub = (op >> 30) & 1
        S = (op >> 29) & 1
        shift = (op >> 22) & 3
        rm = (op >> 16) & 0x1F
        imm6 = (op >> 10) & 0x3F
        rn = (op >> 5) & 0x1F
        rd = op & 0x1F

        rdn = reg64 if sf else reg32

        if is_sub and S and rd == 31:
            mnem = "CMP"
            if imm6:
                sh_name = {0: "LSL", 1: "LSR", 2: "ASR"}.get(shift, "?")
                return mnem, f"{rdn(rn)}, {rdn(rm)}, {sh_name} #{imm6}", ["CMP"]
            return mnem, f"{rdn(rn)}, {rdn(rm)}", ["CMP"]

        if is_sub and not S and rn == 31:
            mnem = "NEG"
            return mnem, f"{rdn(rd)}, {rdn(rm)}", []

        mnem = ("SUB" if is_sub else "ADD") + ("S" if S else "")

        if imm6:
            sh_name = {0: "LSL", 1: "LSR", 2: "ASR"}.get(shift, "?")
            detail = f"{rdn(rd)}, {rdn(rn)}, {rdn(rm)}, {sh_name} #{imm6}"
        else:
            detail = f"{rdn(rd)}, {rdn(rn)}, {rdn(rm)}"

        return mnem, detail, []

    # ADD/SUB (extended register)
    if (op & 0x1FE00000) == 0x0B200000:
        sf = (op >> 31) & 1
        is_sub = (op >> 30) & 1
        S = (op >> 29) & 1
        rm = (op >> 16) & 0x1F
        option = (op >> 13) & 7
        imm3 = (op >> 10) & 7
        rn = (op >> 5) & 0x1F
        rd = op & 0x1F

        rdn = reg64 if sf else reg32
        ext_map = {0: "UXTB", 1: "UXTH", 2: "UXTW", 3: "UXTX",
                   4: "SXTB", 5: "SXTH", 6: "SXTW", 7: "SXTX"}
        ext = ext_map.get(option, "?")
        rmn = reg32(rm) if option < 4 else reg64(rm) if option >= 6 else reg32(rm)

        mnem = ("SUB" if is_sub else "ADD") + ("S" if S else "")

        if imm3:
            detail = f"{rdn(rd)}, {rdn(rn)}, {rmn}, {ext} #{imm3}"
        else:
            detail = f"{rdn(rd)}, {rdn(rn)}, {rmn}, {ext}"

        return mnem, detail, []

    # Logical (immediate) - AND, ORR, EOR, ANDS
    if (op & 0x1F800000) == 0x12000000:
        sf = (op >> 31) & 1
        opc2 = (op >> 29) & 3
        N = (op >> 22) & 1
        immr = (op >> 16) & 0x3F
        imms = (op >> 10) & 0x3F
        rn = (op >> 5) & 0x1F
        rd = op & 0x1F

        # Decode bitmask immediate
        len_val = 0
        if N:
            len_val = 6
        else:
            # Find highest set bit of NOT(imms)
            nimms = (~imms) & 0x3F
            for b in range(5, -1, -1):
                if nimms & (1 << b):
                    len_val = b + 1
                    break

        if len_val == 0:
            return "UNK_LOG_IMM", f"0x{op:08X}", []

        esize = 1 << len_val
        mask = (1 << esize) - 1
        levels = (1 << len_val) - 1
        S_val = imms & levels
        R_val = immr & levels

        # Generate the base pattern
        welem = (1 << (S_val + 1)) - 1
        # Rotate right by R
        welem = ((welem >> R_val) | (welem << (esize - R_val))) & ((1 << esize) - 1)

        # Replicate to 64 bits
        imm_val = 0
        for i in range(64 // esize):
            imm_val |= welem << (i * esize)

        if not sf:
            imm_val &= 0xFFFFFFFF

        rdn = reg64 if sf else reg32

        mnem_map = {0: "AND", 1: "ORR", 2: "EOR", 3: "ANDS"}
        mnem = mnem_map.get(opc2, "?LOG")

        # MOV alias: ORR Xd, XZR, #imm
        if opc2 == 1 and rn == 31:
            return "MOV", f"{rdn(rd)}, #0x{imm_val:X}", []

        # TST alias: ANDS XZR, Xn, #imm
        if opc2 == 3 and rd == 31:
            return "TST", f"{rdn(rn)}, #0x{imm_val:X}", ["CMP"]

        flag_list = []
        if opc2 == 2:
            flag_list.append("XOR")

        detail = f"{rdn(rd)}, {rdn(rn)}, #0x{imm_val:X}"
        return mnem, detail, flag_list

    # Logical (shifted register) - AND, BIC, ORR, ORN, EOR, EON, ANDS, BICS
    if (op & 0x1F000000) == 0x0A000000:
        sf = (op >> 31) & 1
        opc2 = (op >> 29) & 3
        shift = (op >> 22) & 3
        N = (op >> 21) & 1
        rm = (op >> 16) & 0x1F
        imm6 = (op >> 10) & 0x3F
        rn = (op >> 5) & 0x1F
        rd = op & 0x1F

        rdn = reg64 if sf else reg32

        base_map = {0: ("AND", "BIC"), 1: ("ORR", "ORN"), 2: ("EOR", "EON"), 3: ("ANDS", "BICS")}
        mnem = base_map[opc2][N]

        flag_list = []
        if opc2 == 2:
            flag_list.append("XOR")

        # MOV alias: ORR Xd, XZR, Xm
        if opc2 == 1 and not N and rn == 31 and imm6 == 0:
            return "MOV", f"{rdn(rd)}, {rdn(rm)}", []

        # MVN alias: ORN Xd, XZR, Xm
        if opc2 == 1 and N and rn == 31 and imm6 == 0:
            return "MVN", f"{rdn(rd)}, {rdn(rm)}", []

        # TST alias
        if opc2 == 3 and not N and rd == 31:
            mnem = "TST"
            if imm6:
                sh_name = {0: "LSL", 1: "LSR", 2: "ASR", 3: "ROR"}.get(shift, "?")
                return mnem, f"{rdn(rn)}, {rdn(rm)}, {sh_name} #{imm6}", ["CMP"]
            return mnem, f"{rdn(rn)}, {rdn(rm)}", ["CMP"]

        if imm6:
            sh_name = {0: "LSL", 1: "LSR", 2: "ASR", 3: "ROR"}.get(shift, "?")
            detail = f"{rdn(rd)}, {rdn(rn)}, {rdn(rm)}, {sh_name} #{imm6}"
        else:
            detail = f"{rdn(rd)}, {rdn(rn)}, {rdn(rm)}"

        return mnem, detail, flag_list

    # MOVZ / MOVK / MOVN
    if (op & 0x1F800000) == 0x12800000:
        sf = (op >> 31) & 1
        opc2 = (op >> 29) & 3
        hw = (op >> 21) & 3
        imm16 = (op >> 5) & 0xFFFF
        rd = op & 0x1F

        shift_amt = hw * 16
        rdn = reg64 if sf else reg32

        mnem_map = {0: "MOVN", 2: "MOVZ", 3: "MOVK"}
        mnem = mnem_map.get(opc2, f"MOV?{opc2}")

        # MOVZ with single hw=0 is just MOV alias
        if opc2 == 2 and hw == 0:
            mnem = "MOV"
            return mnem, f"{rdn(rd)}, #0x{imm16:X}", []

        if opc2 == 0:  # MOVN
            val = (~(imm16 << shift_amt)) & (0xFFFFFFFFFFFFFFFF if sf else 0xFFFFFFFF)
            return "MOV", f"{rdn(rd)}, #0x{val:X}", []

        if shift_amt:
            detail = f"{rdn(rd)}, #0x{imm16:X}, LSL #{shift_amt}"
        else:
            detail = f"{rdn(rd)}, #0x{imm16:X}"

        return mnem, detail, []

    # MADD / MSUB (includes MUL, MNEG aliases)
    if (op & 0x1FE00000) == 0x1B000000:
        sf = (op >> 31) & 1
        rm = (op >> 16) & 0x1F
        o0 = (op >> 15) & 1
        ra = (op >> 10) & 0x1F
        rn = (op >> 5) & 0x1F
        rd = op & 0x1F

        rdn = reg64 if sf else reg32

        if o0 == 0:
            if ra == 31:
                return "MUL", f"{rdn(rd)}, {rdn(rn)}, {rdn(rm)}", []
            return "MADD", f"{rdn(rd)}, {rdn(rn)}, {rdn(rm)}, {rdn(ra)}", []
        else:
            if ra == 31:
                return "MNEG", f"{rdn(rd)}, {rdn(rn)}, {rdn(rm)}", []
            return "MSUB", f"{rdn(rd)}, {rdn(rn)}, {rdn(rm)}, {rdn(ra)}", []

    # UBFM / SBFM / BFM (includes LSL, LSR, ASR, UBFX, SBFX, UXTB, UXTH, SXTB, SXTH, SXTW)
    if (op & 0x1F800000) == 0x13000000:
        sf = (op >> 31) & 1
        opc2 = (op >> 29) & 3
        N = (op >> 22) & 1
        immr = (op >> 16) & 0x3F
        imms = (op >> 10) & 0x3F
        rn = (op >> 5) & 0x1F
        rd = op & 0x1F

        rdn = reg64 if sf else reg32
        bits = 64 if sf else 32

        if opc2 == 2:  # UBFM
            # LSR alias: immr = shift amount, imms = bits-1
            if imms == (bits - 1):
                return "LSR", f"{rdn(rd)}, {rdn(rn)}, #{immr}", []
            # LSL alias: imms = bits-1-shift, immr = bits-shift
            if imms + 1 == immr:
                shift = bits - immr
                return "LSL", f"{rdn(rd)}, {rdn(rn)}, #{shift}", []
            # UXTB
            if immr == 0 and imms == 7:
                return "UXTB", f"{rdn(rd)}, {reg32(rn)}", []
            # UXTH
            if immr == 0 and imms == 15:
                return "UXTH", f"{rdn(rd)}, {reg32(rn)}", []
            # UBFX
            width = imms - immr + 1
            return "UBFX", f"{rdn(rd)}, {rdn(rn)}, #{immr}, #{width}", []

        elif opc2 == 0:  # SBFM
            if imms == (bits - 1):
                return "ASR", f"{rdn(rd)}, {rdn(rn)}, #{immr}", []
            if immr == 0 and imms == 7:
                return "SXTB", f"{rdn(rd)}, {reg32(rn)}", []
            if immr == 0 and imms == 15:
                return "SXTH", f"{rdn(rd)}, {reg32(rn)}", []
            if immr == 0 and imms == 31:
                return "SXTW", f"{reg64(rd)}, {reg32(rn)}", []
            width = imms - immr + 1
            if width > 0:
                return "SBFX", f"{rdn(rd)}, {rdn(rn)}, #{immr}, #{width}", []
            return "SBFM", f"{rdn(rd)}, {rdn(rn)}, #{immr}, #{imms}", []

        elif opc2 == 1:  # BFM
            if rn == 31:
                # BFC alias
                width = imms + 1
                lsb = (-immr) % bits
                return "BFC", f"{rdn(rd)}, #{lsb}, #{width}", []
            width = imms + 1
            return "BFM", f"{rdn(rd)}, {rdn(rn)}, #{immr}, #{imms}", []

    # CSEL / CSINC / CSINV / CSNEG (includes CSET, CINC aliases)
    if (op & 0x1FE00000) == 0x1A800000:
        sf = (op >> 31) & 1
        is_sub = (op >> 30) & 1
        rm = (op >> 16) & 0x1F
        cond = (op >> 12) & 0xF
        o2 = (op >> 10) & 1
        rn = (op >> 5) & 0x1F
        rd = op & 0x1F

        rdn = reg64 if sf else reg32
        cname = COND_CODES.get(cond, f"?{cond}")

        if is_sub == 0 and o2 == 0:
            mnem = "CSEL"
        elif is_sub == 0 and o2 == 1:
            if rn == rm and rn != 31:
                inv_cond = cond ^ 1
                return "CINC", f"{rdn(rd)}, {rdn(rn)}, {COND_CODES.get(inv_cond, '?')}", []
            if rn == 31 and rm == 31:
                inv_cond = cond ^ 1
                return "CSET", f"{rdn(rd)}, {COND_CODES.get(inv_cond, '?')}", []
            mnem = "CSINC"
        elif is_sub == 1 and o2 == 0:
            mnem = "CSINV"
            if rn == 31 and rm == 31:
                inv_cond = cond ^ 1
                return "CSETM", f"{rdn(rd)}, {COND_CODES.get(inv_cond, '?')}", []
        else:
            mnem = "CSNEG"

        detail = f"{rdn(rd)}, {rdn(rn)}, {rdn(rm)}, {cname}"
        return mnem, detail, []

    # CSEL (without S bit)
    if (op & 0x1FE00000) == 0x1A000000:
        sf = (op >> 31) & 1
        rm = (op >> 16) & 0x1F
        cond = (op >> 12) & 0xF
        rn = (op >> 5) & 0x1F
        rd = op & 0x1F
        rdn = reg64 if sf else reg32
        cname = COND_CODES.get(cond, f"?{cond}")
        return "CSEL", f"{rdn(rd)}, {rdn(rn)}, {rdn(rm)}, {cname}", []

    # UDIV / SDIV
    if (op & 0x1FE0FC00) == 0x1AC00800:
        sf = (op >> 31) & 1
        rm = (op >> 16) & 0x1F
        o1 = (op >> 10) & 1
        rn = (op >> 5) & 0x1F
        rd = op & 0x1F
        rdn = reg64 if sf else reg32
        mnem = "SDIV" if o1 else "UDIV"
        return mnem, f"{rdn(rd)}, {rdn(rn)}, {rdn(rm)}", []

    # LSLV / LSRV / ASRV / RORV (register shifts)
    if (op & 0x1FE0F000) == 0x1AC02000:
        sf = (op >> 31) & 1
        rm = (op >> 16) & 0x1F
        op2 = (op >> 10) & 3
        rn = (op >> 5) & 0x1F
        rd = op & 0x1F
        rdn = reg64 if sf else reg32
        mnem = {0: "LSL", 1: "LSR", 2: "ASR", 3: "ROR"}.get(op2, "?SH")
        return mnem, f"{rdn(rd)}, {rdn(rn)}, {rdn(rm)}", []

    # MRS / MSR (system registers)
    if (op & 0xFFF00000) == 0xD5300000:
        rt = op & 0x1F
        sysreg = (op >> 5) & 0x7FFF
        return "MRS", f"{reg64(rt)}, S{sysreg}", []
    if (op & 0xFFF00000) == 0xD5100000:
        rt = op & 0x1F
        sysreg = (op >> 5) & 0x7FFF
        return "MSR", f"S{sysreg}, {reg64(rt)}", []

    # Fallback
    top8 = (op >> 24) & 0xFF
    return f"UNK({top8:02X})", f"0x{op:08X}", []


def main():
    print(f"Opening {BINARY_PATH}")
    print(f"Constructor at 0x{CONSTRUCTOR_OFFSET:08X}")
    print(f"packData at   0x{PACKDATA_OFFSET:08X}")
    print(f"Reading {READ_SIZE} bytes from 0x{CONSTRUCTOR_OFFSET:08X}")
    print("=" * 100)

    with open(BINARY_PATH, "rb") as f:
        f.seek(CONSTRUCTOR_OFFSET)
        data = f.read(READ_SIZE)

    print(f"Read {len(data)} bytes\n")

    # Check if packData offset is a valid function start
    pd_rel = PACKDATA_OFFSET - CONSTRUCTOR_OFFSET
    print(f"=== Constructor area (0x{CONSTRUCTOR_OFFSET:08X} - 0x{PACKDATA_OFFSET:08X}) ===")

    in_packdata = False
    func_label = "constructor"

    for i in range(0, len(data), 4):
        if i + 4 > len(data):
            break

        word = struct.unpack_from("<I", data, i)[0]
        addr = CONSTRUCTOR_OFFSET + i

        if i == pd_rel:
            print(f"\n{'=' * 100}")
            print(f"=== packData function (0x{PACKDATA_OFFSET:08X}) ===")
            print(f"{'=' * 100}")
            in_packdata = True

        mnem, detail, flags = decode_arm64(word, addr)

        # Build flag string
        flag_str = ""
        if flags:
            flag_str = "  <<< " + ", ".join(flags)

        # Hex bytes
        hx = " ".join(f"{(word >> (b*8)) & 0xFF:02X}" for b in range(4))

        # Highlight interesting instructions
        highlight = ""
        if "CALL" in flags:
            highlight = " *** FUNCTION CALL ***"
        elif "XOR" in flags:
            highlight = " *** XOR ***"
        elif any(f.startswith("OFF=") for f in flags):
            for f in flags:
                if f.startswith("OFF="):
                    highlight = f" *** STRUCT OFFSET {f} ***"

        print(f"  0x{addr:08X}:  {hx}    {mnem:8s} {detail:50s}{flag_str}{highlight}")

        # Mark RET in constructor
        if not in_packdata and mnem == "RET":
            print(f"  --- RET found at 0x{addr:08X} (end of {'constructor' if not in_packdata else 'function'}) ---")

    # Summary
    print(f"\n{'=' * 100}")
    print("=== SUMMARY ===")
    print(f"{'=' * 100}")

    # Re-scan for summary
    calls = []
    xors = []
    struct_accesses = []
    branches = []

    for i in range(pd_rel, len(data), 4):
        if i + 4 > len(data):
            break
        word = struct.unpack_from("<I", data, i)[0]
        addr = CONSTRUCTOR_OFFSET + i
        mnem, detail, flags = decode_arm64(word, addr)

        if "CALL" in flags:
            calls.append((addr, mnem, detail))
        if "XOR" in flags:
            xors.append((addr, mnem, detail))
        for f in flags:
            if f.startswith("OFF="):
                struct_accesses.append((addr, mnem, detail, f))
        if "BRANCH" in flags:
            branches.append((addr, mnem, detail))

    print(f"\nFunction calls (BL/BLR): {len(calls)}")
    for addr, m, d in calls:
        print(f"  0x{addr:08X}: {m} {d}")

    print(f"\nXOR operations: {len(xors)}")
    for addr, m, d in xors:
        print(f"  0x{addr:08X}: {m} {d}")

    print(f"\nStruct offset accesses (small offsets): {len(struct_accesses)}")
    for addr, m, d, off in struct_accesses:
        print(f"  0x{addr:08X}: {m:8s} {d:50s} [{off}]")

    print(f"\nBranches: {len(branches)}")
    for addr, m, d in branches:
        print(f"  0x{addr:08X}: {m} {d}")


if __name__ == "__main__":
    main()

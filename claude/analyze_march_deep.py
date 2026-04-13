"""
Deep analysis of KingdomMap::doMarch and related functions.
Find what values get written to START_MARCH_NEW struct fields.
Focus on VA/VB session bytes.
"""
import struct
import sys
sys.path.insert(0, r"D:\CascadeProjects\lords_bot\re")
from analyze_start_march_population import (
    load_symbols, simplify_dataflow, direct_callers,
    decode_bl_target, decode_mov_imm, decode_ldst_uimm,
    decode_addsub_imm, decode_mov_reg
)

# Override LIB path
import analyze_start_march_population as asp
asp.LIB = r"D:\CascadeProjects\libgame_new.so"

def disasm_function(data, addr, size, label=""):
    """Raw disassembly with basic decode."""
    raw = data[addr:addr + size]
    print(f"\n{'='*70}")
    print(f"{label} @ 0x{addr:08X} ({size}B)")
    print(f"{'='*70}")

    for off in range(0, min(len(raw), size) - 3, 4):
        pc = addr + off
        inst = struct.unpack_from("<I", raw, off)[0]

        # Decode
        info = ""
        if (inst & 0xFC000000) == 0x94000000:  # BL
            target = decode_bl_target(pc, inst)
            info = f"BL 0x{target:08X}"
        else:
            parsed = decode_mov_imm(inst) or decode_ldst_uimm(inst) or decode_addsub_imm(inst) or decode_mov_reg(inst)
            if parsed:
                kind = parsed.get("kind", "?")
                if kind == "mov_imm":
                    info = f"MOV W/X{parsed['dst']}, #0x{parsed['imm']:X}"
                elif kind in ("str", "ldr"):
                    base = f"X{parsed['base']}" if parsed['base'] != 31 else "SP"
                    info = f"{kind.upper()}{parsed['scale']}B X{parsed['reg']}, [{base}, #0x{parsed['imm']:X}]"
                elif kind == "addsub_imm":
                    reg = f"X{parsed['dst']}" if parsed['width'] == 64 else f"W{parsed['dst']}"
                    src = f"X{parsed['src']}" if parsed['width'] == 64 else f"W{parsed['src']}"
                    if parsed['src'] == 31: src = "SP"
                    info = f"{parsed['op'].upper()} {reg}, {src}, #0x{parsed['imm']:X}"
                elif kind == "mov_reg":
                    info = f"MOV X{parsed['dst']}, X{parsed['src']}"

        print(f"  0x{pc:08X}: {inst:08X}  {info}")


def main():
    print("Loading symbols from libgame_new.so...")
    data, symbols, by_name, plt_slot_symbols = load_symbols()

    ctor = "_ZN20CMSG_START_MARCH_NEWC1Ev"
    pack = "_ZN20CMSG_START_MARCH_NEW8packDataER8CIStream"

    ctor_addr, _ = by_name[ctor]
    pack_addr, _ = by_name[pack]
    print(f"Constructor: 0x{ctor_addr:08X}")
    print(f"packData:    0x{pack_addr:08X}")

    # Key functions to analyze
    targets = {
        "KingdomMap::doMarch": "_ZN10KingdomMap7doMarchEiiimRKNSt6__ndk14listIiNS0_9allocatorIiEEEEiimi",
        "LogicAutoAtkRebel::onAttackMonster": "_ZN17LogicAutoAtkRebel15onAttackMonsterEiiimimi",
        "AutoHangupAttackMonsterUI::onAttackMonster": "_ZN25AutoHangupAttackMonsterUI15onAttackMonsterEiiimimi",
    }

    for label, mangled in targets.items():
        if mangled not in by_name:
            print(f"\n[SKIP] {label} not found")
            continue

        addr, size = by_name[mangled]
        print(f"\n{'#'*70}")
        print(f"# {label} @ 0x{addr:08X} ({size}B)")
        print(f"{'#'*70}")

        # Run dataflow analysis
        analysis = simplify_dataflow(
            data, addr, size,
            ctor_addr, ctor,
            pack_addr, pack,
            plt_slot_symbols,
        )

        if analysis["ctor_idx"] is None:
            print("  Constructor call NOT found in this function")
            # Still disassemble
            disasm_function(data, addr, min(size, 600), label)
            continue

        if analysis["pack_idx"] is None:
            print("  packData call NOT found in this function")
            disasm_function(data, addr, min(size, 600), label)
            continue

        ctor_pc = addr + analysis["ctor_idx"] * 4
        pack_pc = addr + analysis["pack_idx"] * 4
        print(f"  ctor call @ 0x{ctor_pc:08X}")
        print(f"  pack call @ 0x{pack_pc:08X}")
        print(f"  object base: sp+0x{analysis['object_sp']:X}" if analysis['object_sp'] else "  object base: unresolved")

        if analysis["writes"]:
            print(f"\n  === FIELD WRITES (between ctor and packData) ===")
            from collections import defaultdict
            by_field = defaultdict(list)
            for w in analysis["writes"]:
                by_field[w["field_off"]].append(w)

            for foff in sorted(by_field):
                for w in by_field[foff]:
                    field_name = {
                        0x00: "sub_type",
                        0x02: "march_type",
                        0x04: "flag_0", 0x05: "flag_1", 0x06: "flag_2",
                        0x07: "flag_3 (VA?)", 0x08: "flag_4",
                        0x10: "target_info_lo", 0x14: "target_info_hi",
                        0x18: "kingdom_id", 0x1A: "march_slot",
                        0x20: "troop_vec_begin", 0x28: "troop_vec_end",
                        0x38: "tile_type", 0x3C: "sub_flag",
                        0x40: "rally_param", 0x48: "extra_0",
                        0x49: "extra_1", 0x50: "param_2",
                        0x58: "extra_2", 0x5C: "param_3",
                    }.get(foff, f"unknown_0x{foff:02X}")
                    print(f"    +0x{foff:02X} ({field_name:20s}) <= [{w['store_width']}B] {w['src_desc']} @ 0x{w['pc']:08X}")
        else:
            print("  No field writes found between ctor and packData")

        # Also disassemble the region between ctor and packData
        start = addr + analysis["ctor_idx"] * 4
        end = addr + analysis["pack_idx"] * 4 + 4
        disasm_function(data, start, end - start, f"{label} (ctor->packData region)")


if __name__ == "__main__":
    main()

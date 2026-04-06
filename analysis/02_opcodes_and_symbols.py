"""
Phase 2: Opcode Discovery + Key Symbols
- Find all opcode values from exported symbols (mangled names contain them)
- Find encryption/codec class methods
- Find network handler dispatch tables
- Find game action functions
"""
import re, struct, sys
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection

SO_PATH = r"D:\CascadeProjects\libgame.so"

def demangle_basic(name):
    """Very basic C++ demangling - just clean up common patterns."""
    # Remove leading _Z
    return name

def main():
    with open(SO_PATH, 'rb') as f:
        elf = ELFFile(f)
        raw = None

    with open(SO_PATH, 'rb') as f:
        raw = f.read()

    # Get all symbols
    all_syms = []
    with open(SO_PATH, 'rb') as f:
        elf = ELFFile(f)
        for s in elf.iter_sections():
            if isinstance(s, SymbolTableSection):
                for sym in s.iter_symbols():
                    if sym.name:
                        all_syms.append((sym['st_value'], sym['st_size'], sym.name))

    all_syms.sort()
    print(f"Total symbols: {len(all_syms)}")

    # ── Find opcode-related symbols ──
    print("\n" + "=" * 80)
    print("OPCODE / HANDLER SYMBOLS")
    print("=" * 80)

    # Look for patterns like "0x0CE8", "0CE8", "opcode", "handler", "dispatch"
    opcode_syms = []
    handler_syms = []
    for addr, size, name in all_syms:
        nl = name.lower()
        if any(k in nl for k in ['opcode', 'handler', 'dispatch', 'recv', 'process', 'handle', 'packet', 'msg', 'cmd']):
            handler_syms.append((addr, size, name))
        # Check for hex opcode patterns in name
        if re.search(r'[0-9a-fA-F]{3,4}[^0-9a-fA-F]', name) or '0x' in name.lower():
            opcode_syms.append((addr, size, name))

    print(f"\nHandler-related symbols ({len(handler_syms)}):")
    for addr, size, name in handler_syms[:100]:
        print(f"  0x{addr:016X}  {size:8d}  {name}")

    # ── Find Encryption/Codec symbols ──
    print("\n" + "=" * 80)
    print("ENCRYPTION / CODEC SYMBOLS")
    print("=" * 80)

    crypto_syms = []
    for addr, size, name in all_syms:
        nl = name.lower()
        if any(k in nl for k in ['encrypt', 'decrypt', 'codec', 'cipher', 'encode', 'decode', 'crypt', 'cmsg', 'xor', 'aes', 'rc4', 'hmac', 'hash']):
            crypto_syms.append((addr, size, name))

    print(f"\nCrypto/Codec symbols ({len(crypto_syms)}):")
    for addr, size, name in crypto_syms[:100]:
        print(f"  0x{addr:016X}  {size:8d}  {name}")

    # ── Find Socket/Network symbols ──
    print("\n" + "=" * 80)
    print("NETWORK / SOCKET SYMBOLS")
    print("=" * 80)

    net_syms = []
    for addr, size, name in all_syms:
        nl = name.lower()
        if any(k in nl for k in ['socket', 'connect', 'gateway', 'tcp', 'net', 'send', 'gosocket', 'network', 'login', 'auth', '001f', '0020', '0021', '0038', '1b8b']):
            net_syms.append((addr, size, name))

    print(f"\nNetwork symbols ({len(net_syms)}):")
    for addr, size, name in net_syms[:100]:
        print(f"  0x{addr:016X}  {size:8d}  {name}")

    # ── Find Game Action symbols ──
    print("\n" + "=" * 80)
    print("GAME ACTION SYMBOLS")
    print("=" * 80)

    action_syms = []
    for addr, size, name in all_syms:
        nl = name.lower()
        if any(k in nl for k in ['march', 'gather', 'train', 'build', 'research', 'attack', 'recruit', 'action', 'troop', 'soldier', 'hero', 'city', 'castle']):
            action_syms.append((addr, size, name))

    print(f"\nGame action symbols ({len(action_syms)}):")
    for addr, size, name in action_syms[:150]:
        print(f"  0x{addr:016X}  {size:8d}  {name}")

    # ── Find config/data symbols ──
    print("\n" + "=" * 80)
    print("CONFIG / DATA SYMBOLS")
    print("=" * 80)

    cfg_syms = []
    for addr, size, name in all_syms:
        nl = name.lower()
        if any(k in nl for k in ['config', 'cfg', 'data', 'manager', 'mgr']):
            cfg_syms.append((addr, size, name))

    print(f"\nConfig/Manager symbols ({len(cfg_syms)}):")
    for addr, size, name in cfg_syms[:100]:
        print(f"  0x{addr:016X}  {size:8d}  {name}")

    # ── Scan .rodata for opcode tables ──
    print("\n" + "=" * 80)
    print("OPCODE VALUES IN .rodata (U16 LE scan)")
    print("=" * 80)

    # Known opcodes from our reverse engineering
    known_opcodes = {
        0x000B: 'GATEWAY_AUTH',
        0x000C: 'GATEWAY_REDIRECT',
        0x001F: 'GAME_LOGIN',
        0x0020: 'LOGIN_OK',
        0x0021: 'WORLD_ENTRY',
        0x0033: 'SYN_ATTRIBUTE',
        0x0037: 'TIMESTAMP',
        0x0038: 'INIT_DATA',
        0x0042: 'HEARTBEAT',
        0x0043: 'HEARTBEAT2',
        0x006E: 'SET_TILE',
        0x00AA: 'HERO_INFO',
        0x00B8: 'MARCH_ACK',
        0x0245: 'UNK_0245',
        0x02F2: 'SESSION_ERROR',
        0x0323: 'HERO_SELECT',
        0x033E: 'SEARCH_TILE',
        0x033F: 'SEARCH_RESULT',
        0x06C2: 'SOLDIER_INFO',
        0x0709: 'UNK_0709',
        0x0840: 'UNK_0840',
        0x0834: 'FORMATION_SET',
        0x0A2C: 'UNK_0A2C',
        0x0AF2: 'UNK_0AF2',
        0x099D: 'TROOP_QUERY',
        0x0CE7: 'CANCEL_MARCH',
        0x0CE8: 'START_MARCH',
        0x0CEB: 'ENABLE_VIEW',
        0x0CED: 'TRAIN',
        0x0CEE: 'RESEARCH',
        0x0CEF: 'BUILD',
        0x0EFF: 'UNK_0EFF',
        0x1357: 'UNK_1357',
        0x170D: 'UNK_170D',
        0x17D4: 'UNK_17D4',
        0x1B8B: 'SESSION_PKT',
        0x1C87: 'UNK_1C87',
        0x11FF: 'UNK_11FF',
    }

    # Find occurrences of known opcodes in the binary
    print(f"\nSearching for {len(known_opcodes)} known opcodes in binary:")
    for opcode, name in sorted(known_opcodes.items()):
        needle = struct.pack('<H', opcode)
        count = raw.count(needle)
        offsets = []
        pos = 0
        while len(offsets) < 5:
            idx = raw.find(needle, pos)
            if idx < 0: break
            offsets.append(idx)
            pos = idx + 1
        print(f"  0x{opcode:04X} ({name:<20}) found {count:5d}x  first_offsets={[hex(o) for o in offsets[:3]]}")

    # Find the GoSocket class
    print("\n" + "=" * 80)
    print("GoSocket / CMsgCodec in symbol names")
    print("=" * 80)
    gosocket_syms = [(a, s, n) for a, s, n in all_syms if 'GoSocket' in n or 'CMsgCodec' in n or 'CMsg' in n]
    for addr, size, name in gosocket_syms[:50]:
        print(f"  0x{addr:016X}  {size:8d}  {name}")

    # ── Raw strings for key protocol constants ──
    print("\n" + "=" * 80)
    print("HARDCODED PROTOCOL STRINGS")
    print("=" * 80)

    targets = [b'CQ_secret', b'CQ_', b'gateway', b'Gateway',
               b'5997', b'5991', b'7001', b'igg.com',
               b'conqueror', b'Conqueror',
               b'session', b'Session', b'1B8B', b'1b8b']

    for needle in targets:
        count = raw.count(needle)
        if count:
            offsets = []
            pos = 0
            while len(offsets) < 5:
                idx = raw.find(needle, pos)
                if idx < 0: break
                # Show context
                ctx_start = max(0, idx - 20)
                ctx_end = min(len(raw), idx + len(needle) + 40)
                ctx = raw[ctx_start:ctx_end]
                offsets.append(f"0x{idx:08X}: ...{ctx}...")
                pos = idx + 1
            print(f"\n  '{needle.decode()}' ({count}x):")
            for o in offsets[:3]:
                print(f"    {o}")

if __name__ == '__main__':
    main()

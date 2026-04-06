"""
Phase 3: Extract ALL CMSG_* message types from libgame.so symbols.
These are the actual named protocol messages used by the game.
Also extract GoSocket, encryption functions, and key class names.
"""
import re, struct, sys
from collections import Counter
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection

SO_PATH = r"D:\CascadeProjects\libgame.so"

def main():
    # Get all symbol names
    all_names = set()
    with open(SO_PATH, 'rb') as f:
        elf = ELFFile(f)
        for s in elf.iter_sections():
            if isinstance(s, SymbolTableSection):
                for sym in s.iter_symbols():
                    if sym.name:
                        all_names.add(sym.name)

    # Also extract from raw strings
    with open(SO_PATH, 'rb') as f:
        raw = f.read()

    # Extract CMSG_* patterns from symbols and strings
    cmsg_pattern = re.compile(rb'CMSG_[A-Z0-9_]+')
    cmsg_from_raw = set(m.group().decode() for m in cmsg_pattern.finditer(raw))

    # Also extract from symbol names
    for name in all_names:
        for m in re.finditer(r'CMSG_[A-Z0-9_]+', name):
            cmsg_from_raw.add(m.group())

    cmsg_types = sorted(cmsg_from_raw)

    print("=" * 80)
    print(f"ALL CMSG_* MESSAGE TYPES ({len(cmsg_types)} found)")
    print("=" * 80)

    # Group by category
    categories = {}
    for name in cmsg_types:
        parts = name.replace('CMSG_', '').split('_')
        cat = parts[0] if parts else 'OTHER'
        categories.setdefault(cat, []).append(name)

    for cat in sorted(categories.keys()):
        msgs = categories[cat]
        print(f"\n--- {cat} ({len(msgs)}) ---")
        for m in sorted(msgs):
            print(f"  {m}")

    # ── GoSocket class analysis ──
    print("\n\n" + "=" * 80)
    print("GoSocket CLASS METHODS")
    print("=" * 80)

    gosocket = []
    for name in sorted(all_names):
        if 'GoSocket' in name:
            # Try basic demangling
            clean = name
            gosocket.append(clean)

    for s in sorted(set(gosocket)):
        print(f"  {s}")

    # ── Find all classes with "encode" or "decode" in method names ──
    print("\n\n" + "=" * 80)
    print("ENCODE/DECODE/ENCRYPT/DECRYPT METHODS")
    print("=" * 80)

    codec_methods = []
    for name in sorted(all_names):
        nl = name.lower()
        if any(k in nl for k in ['encode', 'decode', 'encrypt', 'decrypt', 'doencod', 'dodecod']):
            codec_methods.append(name)

    for s in sorted(set(codec_methods))[:100]:
        print(f"  {s}")

    # ── Find "CQ_secret" and related protocol strings ──
    print("\n\n" + "=" * 80)
    print("PROTOCOL STRINGS")
    print("=" * 80)

    patterns = [
        rb'CQ_[a-zA-Z_]+',
        rb'gateway',
        rb'GoSocket',
        rb'CMsgCodec',
        rb'doDecode',
        rb'doEncode',
        rb'SERVER_KEY',
        rb'server_key',
        rb'session',
        rb'heartbeat',
        rb'login',
    ]

    for pat in patterns:
        matches = set(m.group().decode('ascii', errors='replace') for m in re.finditer(pat, raw, re.IGNORECASE))
        if matches:
            print(f"\n  Pattern '{pat.decode()}':")
            for m in sorted(matches):
                print(f"    {m}")

    # ── Find _RECV / _SEND patterns (C2S vs S2C) ──
    print("\n\n" + "=" * 80)
    print("SEND/RECV MESSAGE DIRECTION")
    print("=" * 80)

    send_msgs = [m for m in cmsg_types if '_SEND' in m]
    recv_msgs = [m for m in cmsg_types if '_RECV' in m or '_RETURN' in m]
    other_msgs = [m for m in cmsg_types if '_SEND' not in m and '_RECV' not in m and '_RETURN' not in m]

    print(f"\nC2S (SEND) messages ({len(send_msgs)}):")
    for m in sorted(send_msgs):
        print(f"  {m}")

    print(f"\nS2C (RECV/RETURN) messages ({len(recv_msgs)}):")
    for m in sorted(recv_msgs):
        print(f"  {m}")

    print(f"\nUnclear direction ({len(other_msgs)}):")
    for m in sorted(other_msgs):
        print(f"  {m}")

    # ── Find march/gather specific ──
    print("\n\n" + "=" * 80)
    print("MARCH / GATHER / ATTACK RELATED")
    print("=" * 80)

    for m in cmsg_types:
        ml = m.lower()
        if any(k in ml for k in ['march', 'gather', 'attack', 'scout', 'rally', 'battle', 'troop', 'soldier', 'army']):
            print(f"  {m}")

    # ── Key game classes ──
    print("\n\n" + "=" * 80)
    print("KEY GAME CLASSES (from typeinfo)")
    print("=" * 80)

    class_pattern = re.compile(rb'_ZTS(\d+)([A-Z][A-Za-z0-9_]+)')
    classes = set()
    for m in class_pattern.finditer(raw):
        length = int(m.group(1))
        name = m.group(2).decode('ascii', errors='replace')
        if len(name) == length:
            classes.add(name)

    interesting_classes = []
    for c in sorted(classes):
        cl = c.lower()
        if any(k in cl for k in ['socket', 'net', 'protocol', 'codec', 'msg', 'packet',
                                   'march', 'gather', 'attack', 'battle', 'troop',
                                   'hero', 'build', 'train', 'research', 'city',
                                   'game', 'logic', 'state', 'auth', 'login',
                                   'session', 'key', 'crypto', 'encrypt']):
            interesting_classes.append(c)

    print(f"\nInteresting game classes ({len(interesting_classes)}):")
    for c in sorted(interesting_classes):
        print(f"  {c}")

    print(f"\nALL classes ({len(classes)} total)")


if __name__ == '__main__':
    main()

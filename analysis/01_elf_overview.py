"""
Phase 1: ELF Structure Overview
- Architecture, sections, segments, symbols (imported/exported)
- String extraction (function names, class names, URLs, keys)
- Dynamic linking info
"""
import sys, struct, re
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection
from elftools.elf.dynamic import DynamicSection

SO_PATH = r"D:\CascadeProjects\libgame.so"

def main():
    with open(SO_PATH, 'rb') as f:
        elf = ELFFile(f)

        print("=" * 80)
        print("ELF OVERVIEW")
        print("=" * 80)
        print(f"  Class:        {elf.elfclass}-bit")
        print(f"  Arch:         {elf.get_machine_arch()}")
        print(f"  Endian:       {elf.little_endian and 'Little' or 'Big'}")
        print(f"  Entry point:  0x{elf.header.e_entry:016X}")
        print(f"  ELF type:     {elf.header.e_type}")
        print(f"  Sections:     {elf.num_sections()}")
        print(f"  Segments:     {elf.num_segments()}")

        print("\n" + "=" * 80)
        print("SECTIONS")
        print("=" * 80)
        print(f"{'Name':<30} {'Type':<18} {'Offset':>12} {'Size':>12} {'Flags'}")
        for s in elf.iter_sections():
            flags = ""
            if s.header.sh_flags & 0x1: flags += "W"
            if s.header.sh_flags & 0x2: flags += "A"
            if s.header.sh_flags & 0x4: flags += "X"
            print(f"  {s.name:<28} {s['sh_type']:<18} {s['sh_offset']:>12,} {s['sh_size']:>12,}  {flags}")

        print("\n" + "=" * 80)
        print("IMPORTED SYMBOLS (from external libs)")
        print("=" * 80)
        imports = []
        for s in elf.iter_sections():
            if isinstance(s, SymbolTableSection):
                for sym in s.iter_symbols():
                    if sym['st_shndx'] == 'SHN_UNDEF' and sym.name:
                        imports.append(sym.name)
        imports.sort()
        print(f"  Total imports: {len(imports)}")
        for name in imports[:200]:
            print(f"    {name}")
        if len(imports) > 200:
            print(f"  ... +{len(imports)-200} more")

        print("\n" + "=" * 80)
        print("EXPORTED SYMBOLS")
        print("=" * 80)
        exports = []
        for s in elf.iter_sections():
            if isinstance(s, SymbolTableSection):
                for sym in s.iter_symbols():
                    if sym['st_shndx'] != 'SHN_UNDEF' and sym.name and sym['st_value'] != 0:
                        exports.append((sym['st_value'], sym.name))
        exports.sort()
        print(f"  Total exports: {len(exports)}")
        for addr, name in exports[:200]:
            print(f"    0x{addr:016X}  {name}")
        if len(exports) > 200:
            print(f"  ... +{len(exports)-200} more")

        print("\n" + "=" * 80)
        print("DYNAMIC LIBRARIES (DT_NEEDED)")
        print("=" * 80)
        for s in elf.iter_sections():
            if isinstance(s, DynamicSection):
                for tag in s.iter_tags():
                    if tag.entry.d_tag == 'DT_NEEDED':
                        print(f"  {tag.needed}")

        # String extraction - key patterns
        print("\n" + "=" * 80)
        print("KEY STRINGS EXTRACTED")
        print("=" * 80)

    # Read raw bytes for string search
    with open(SO_PATH, 'rb') as f:
        raw = f.read()

    # Extract all printable strings ≥ 6 chars
    pattern = re.compile(rb'[\x20-\x7e]{6,}')
    all_strings = [m.group().decode('ascii', errors='replace') for m in pattern.finditer(raw)]
    all_strings = list(set(all_strings))
    all_strings.sort()

    # Categorize
    cats = {
        'URLs': [],
        'IPs/Hosts': [],
        'Crypto/Hash': [],
        'Opcodes/Protocol': [],
        'JNI/Java': [],
        'Encryption keys': [],
        'Error messages': [],
        'URLs/paths': [],
        'Interesting': [],
    }

    for s in all_strings:
        sl = s.lower()
        if 'http://' in sl or 'https://' in sl: cats['URLs'].append(s)
        elif re.match(r'\d+\.\d+\.\d+\.\d+', s): cats['IPs/Hosts'].append(s)
        elif any(k in sl for k in ['aes', 'des', 'rsa', 'sha', 'md5', 'hmac', 'cipher', 'encrypt', 'decrypt', 'base64']): cats['Crypto/Hash'].append(s)
        elif any(k in sl for k in ['opcode', 'packet', 'socket', 'connect', 'send', 'recv', 'header', 'payload', 'cq_secret', 'cq_']): cats['Opcodes/Protocol'].append(s)
        elif sl.startswith('java/') or sl.startswith('android/') or '()v' in sl or '()z' in sl or sl.startswith('com.igg'): cats['JNI/Java'].append(s)
        elif re.match(r'^[A-Za-z0-9+/]{20,}={0,2}$', s) and len(s) % 4 == 0: cats['Encryption keys'].append(s)
        elif any(k in sl for k in ['error', 'fail', 'invalid', 'wrong', 'reject', 'deny']): cats['Error messages'].append(s)

    for cat, items in cats.items():
        if items:
            print(f"\n--- {cat} ({len(items)}) ---")
            for x in sorted(set(items))[:50]:
                print(f"  {repr(x)}")


if __name__ == '__main__':
    main()

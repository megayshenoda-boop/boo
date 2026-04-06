"""
Phase 4: Clean extraction of all protocol data from libgame.so
- Deduplicated CMSG names (strip mangling suffixes)
- GoSocket methods
- Encryption functions
- March/Battle/Action related
- Write results to findings files
"""
import re, struct, sys
from collections import defaultdict
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection

SO_PATH = r"D:\CascadeProjects\libgame.so"
OUT_DIR = r"D:\CascadeProjects\analysis"

def clean_cmsg(name):
    """Strip C++ mangling suffixes from CMSG_* names."""
    # Remove known mangling tails
    for suffix in ['EJPS1_RKNS_12', 'EJPS3_RKNS_12', 'EENS_19__',
                   'C1E', 'C2E', 'D2E', 'EE', 'EEE', 'EPK', 'E3',
                   'ERK', 'ERKS_', '7', '8']:
        if name.endswith(suffix):
            name = name[:-len(suffix)]
            break
    # Remove trailing mangled type refs
    name = re.sub(r'ERK\d+CMSG_.*$', '', name)
    name = re.sub(r'\d+[A-Z_]+INFOEEENS.*$', '', name)
    name = re.sub(r'\d+[A-Z_]+INFOENS.*$', '', name)
    return name

def main():
    # Load symbols
    all_names = []
    with open(SO_PATH, 'rb') as f:
        elf = ELFFile(f)
        for s in elf.iter_sections():
            if isinstance(s, SymbolTableSection):
                for sym in s.iter_symbols():
                    if sym.name:
                        all_names.append((sym['st_value'], sym.name))

    # Load raw bytes
    with open(SO_PATH, 'rb') as f:
        raw = f.read()

    # ═══ 1. Extract ALL clean CMSG names ═══
    cmsg_raw = set()
    cmsg_pattern = re.compile(rb'CMSG_[A-Z0-9_]+')
    for m in cmsg_pattern.finditer(raw):
        cmsg_raw.add(m.group().decode())
    for _, name in all_names:
        for m in re.finditer(r'CMSG_[A-Z0-9_]+', name):
            cmsg_raw.add(m.group())

    # Clean and deduplicate
    cmsg_clean = set()
    for name in cmsg_raw:
        cleaned = clean_cmsg(name)
        if cleaned.startswith('CMSG_') and len(cleaned) > 6:
            cmsg_clean.add(cleaned)

    cmsg_list = sorted(cmsg_clean)

    # Separate by direction
    send_msgs = sorted(m for m in cmsg_list if m.endswith('_REQUEST') or m.endswith('_SEND'))
    recv_msgs = sorted(m for m in cmsg_list if m.endswith('_RETURN') or m.endswith('_RECV') or m.endswith('_INFO'))
    sync_msgs = sorted(m for m in cmsg_list if '_SYNC' in m or '_SYN_' in m or m.endswith('_LOGIN_INFO'))
    other_msgs = sorted(m for m in cmsg_list if m not in send_msgs and m not in recv_msgs and m not in sync_msgs)

    # ═══ 2. GoSocket methods ═══
    gosocket = set()
    for _, name in all_names:
        if 'GoSocket' in name:
            gosocket.add(name)

    # ═══ 3. Encode/Decode/Crypto ═══
    crypto = set()
    for _, name in all_names:
        nl = name.lower()
        if any(k in nl for k in ['encode', 'decode', 'encrypt', 'decrypt', 'cmsgcodec',
                                   'dodecod', 'doencod', 'xor_key', 'cq_secret']):
            crypto.add(name)

    # ═══ 4. March/Battle/Gather ═══
    march_msgs = sorted(m for m in cmsg_list if any(k in m.lower() for k in ['march', 'gather', 'attack', 'scout', 'rally', 'battle', 'troop', 'soldier', 'army', 'war', 'siege', 'reinforce']))

    # ═══ 5. Game classes from typeinfo ═══
    class_pattern = re.compile(rb'_ZTS(\d+)([A-Z][A-Za-z0-9_]+)')
    classes = set()
    for m in class_pattern.finditer(raw):
        length = int(m.group(1))
        name = m.group(2).decode('ascii', errors='replace')
        if len(name) == length:
            classes.add(name)

    # ═══ 6. Key strings ═══
    str_pattern = re.compile(rb'[\x20-\x7e]{8,}')
    all_strings = [m.group().decode('ascii', errors='replace') for m in str_pattern.finditer(raw)]

    urls = sorted(set(s for s in all_strings if 'http' in s.lower()))
    ips = sorted(set(s for s in all_strings if re.match(r'^\d+\.\d+\.\d+\.\d+', s)))
    protocol_strs = sorted(set(s for s in all_strings if any(k in s.lower() for k in
        ['cq_', 'gosocket', 'gateway', 'server_key', 'session', 'heartbeat',
         'opcode', 'packet', 'encrypt', 'decrypt', 'dodecode', 'doencode'])))

    # ═══ Write master findings file ═══
    with open(f"{OUT_DIR}/FINDINGS.md", 'w', encoding='utf-8') as f:
        f.write("# libgame.so Complete Analysis\n\n")
        f.write(f"**File**: libgame.so (104MB, ARM64 AArch64, stripped)\n")
        f.write(f"**Symbols**: {len(all_names)} total\n")
        f.write(f"**CMSG Types**: {len(cmsg_list)} unique (cleaned)\n")
        f.write(f"**Classes**: {len(classes)} from typeinfo\n\n")

        f.write("---\n\n## 1. Protocol Messages (CMSG)\n\n")

        f.write(f"### C2S (REQUEST/SEND) - {len(send_msgs)} messages\n")
        f.write("```\n")
        for m in send_msgs: f.write(f"{m}\n")
        f.write("```\n\n")

        f.write(f"### S2C (RETURN/RECV/INFO) - {len(recv_msgs)} messages\n")
        f.write("```\n")
        for m in recv_msgs: f.write(f"{m}\n")
        f.write("```\n\n")

        f.write(f"### SYNC messages - {len(sync_msgs)}\n")
        f.write("```\n")
        for m in sync_msgs: f.write(f"{m}\n")
        f.write("```\n\n")

        f.write(f"### Other - {len(other_msgs)}\n")
        f.write("```\n")
        for m in other_msgs: f.write(f"{m}\n")
        f.write("```\n\n")

        f.write("---\n\n## 2. March/Battle/Gather Messages\n\n")
        f.write("```\n")
        for m in march_msgs: f.write(f"{m}\n")
        f.write("```\n\n")

        f.write("---\n\n## 3. GoSocket Class\n\n")
        f.write("```\n")
        for s in sorted(gosocket): f.write(f"{s}\n")
        f.write("```\n\n")

        f.write("---\n\n## 4. Encryption/Codec Functions\n\n")
        f.write("```\n")
        for s in sorted(crypto): f.write(f"{s}\n")
        f.write("```\n\n")

        f.write("---\n\n## 5. Key Strings\n\n")
        f.write("### URLs\n```\n")
        for s in urls: f.write(f"{s}\n")
        f.write("```\n\n")
        f.write("### IPs\n```\n")
        for s in ips: f.write(f"{s}\n")
        f.write("```\n\n")
        f.write("### Protocol Strings\n```\n")
        for s in protocol_strs[:100]: f.write(f"{s}\n")
        f.write("```\n\n")

        f.write("---\n\n## 6. Key Game Classes\n\n")
        interesting = sorted(c for c in classes if any(k in c.lower() for k in
            ['socket', 'net', 'protocol', 'codec', 'msg', 'packet', 'march', 'gather',
             'attack', 'battle', 'troop', 'hero', 'build', 'train', 'research', 'city',
             'game', 'logic', 'state', 'auth', 'login', 'session', 'key', 'encrypt',
             'action', 'formation', 'army', 'soldier', 'quest', 'chat', 'league',
             'equip', 'item', 'shop', 'vip', 'resource', 'mail']))
        f.write("```\n")
        for c in interesting: f.write(f"{c}\n")
        f.write("```\n\n")

        f.write("---\n\n## 7. All Classes (Full List)\n\n")
        f.write("```\n")
        for c in sorted(classes): f.write(f"{c}\n")
        f.write("```\n")

    print(f"Written {OUT_DIR}/FINDINGS.md")

    # ═══ Print summary to console ═══
    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    print(f"  Total CMSG types: {len(cmsg_list)}")
    print(f"    C2S (REQUEST/SEND): {len(send_msgs)}")
    print(f"    S2C (RETURN/RECV):  {len(recv_msgs)}")
    print(f"    SYNC:               {len(sync_msgs)}")
    print(f"    Other:              {len(other_msgs)}")
    print(f"  GoSocket methods:     {len(gosocket)}")
    print(f"  Crypto functions:     {len(crypto)}")
    print(f"  March/Battle msgs:    {len(march_msgs)}")
    print(f"  Game classes:         {len(classes)}")

    print(f"\n{'='*80}")
    print("MARCH / BATTLE / GATHER MESSAGES")
    print(f"{'='*80}")
    for m in march_msgs:
        print(f"  {m}")

    print(f"\n{'='*80}")
    print("GOSOCKET METHODS (key)")
    print(f"{'='*80}")
    for s in sorted(gosocket):
        if any(k in s.lower() for k in ['send', 'recv', 'connect', 'encode', 'decode', 'init', 'close', 'read', 'write', 'process']):
            print(f"  {s}")

    print(f"\n{'='*80}")
    print("ENCRYPTION / CODEC")
    print(f"{'='*80}")
    for s in sorted(crypto):
        print(f"  {s}")

if __name__ == '__main__':
    main()

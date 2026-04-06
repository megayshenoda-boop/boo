#!/usr/bin/env python3
"""
13_game_strings.py - Extract and categorize game-related strings from libgame.so
Analyzes the ARM64 ELF shared object for Lords Mobile / IGG Conquerors.
"""

import re
import os
import struct
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    from elftools.elf.elffile import ELFFile
    from elftools.elf.sections import SymbolTableSection
except ImportError:
    print("Installing pyelftools...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyelftools"])
    from elftools.elf.elffile import ELFFile
    from elftools.elf.sections import SymbolTableSection

# ──────────────────────────── Config ────────────────────────────
LIBGAME = r"D:\CascadeProjects\libgame.so"
OUTPUT  = r"D:\CascadeProjects\analysis\findings\strings_and_constants.md"
MIN_STR_LEN = 4
MAX_STR_LEN = 2048

# Encryption code region to inspect for numeric constants
CRYPTO_REGION_START = 0x028B7200
CRYPTO_REGION_END   = 0x028B7300

# ──────────────────────────── Helpers ────────────────────────────

def extract_ascii_strings(data: bytes, min_len=MIN_STR_LEN, max_len=MAX_STR_LEN, base_offset=0):
    """Extract printable ASCII strings from binary data."""
    results = []
    current = bytearray()
    start = 0
    for i, b in enumerate(data):
        if 0x20 <= b <= 0x7e:
            if not current:
                start = i
            current.append(b)
        else:
            if len(current) >= min_len and len(current) <= max_len:
                results.append((base_offset + start, current.decode('ascii', errors='replace')))
            current = bytearray()
    if len(current) >= min_len and len(current) <= max_len:
        results.append((base_offset + start, current.decode('ascii', errors='replace')))
    return results


def demangle_symbol(name):
    """Try to demangle a C++ symbol. Falls back to the mangled name."""
    if not name.startswith('_Z'):
        return name
    try:
        result = subprocess.run(
            ['c++filt', name],
            capture_output=True, text=True, timeout=2
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    # Manual basic demangling for common patterns
    return _basic_demangle(name)


def _basic_demangle(name):
    """Very basic C++ name demangling for when c++filt is not available."""
    if not name.startswith('_Z'):
        return name
    s = name[2:]
    # Skip qualifiers
    if s.startswith('N'):
        s = s[1:]
    parts = []
    while s and s[0].isdigit():
        length = 0
        while s and s[0].isdigit():
            length = length * 10 + int(s[0])
            s = s[1:]
        if length > 0 and length <= len(s):
            parts.append(s[:length])
            s = s[length:]
        else:
            break
    if parts:
        return '::'.join(parts)
    return name


# ──────────────────────────── Main Extraction ────────────────────────────

def main():
    print(f"[*] Opening {LIBGAME} ...")
    findings = defaultdict(list)

    with open(LIBGAME, 'rb') as f:
        elf = ELFFile(f)
        print(f"    Architecture: {elf.get_machine_arch()}")
        print(f"    Sections: {elf.num_sections()}")

        # ── List sections for reference ──
        section_info = []
        for sec in elf.iter_sections():
            section_info.append((sec.name, sec['sh_type'], hex(sec['sh_offset']),
                                 hex(sec['sh_size']), hex(sec['sh_addr'])))

        # ── Extract .rodata strings ──
        rodata = elf.get_section_by_name('.rodata')
        if rodata is None:
            # Try to find it by iterating
            for sec in elf.iter_sections():
                if '.rodata' in sec.name:
                    rodata = sec
                    break

        rodata_strings = []
        if rodata:
            print(f"[*] Extracting strings from .rodata (offset=0x{rodata['sh_offset']:x}, "
                  f"size=0x{rodata['sh_size']:x}, addr=0x{rodata['sh_addr']:x})")
            rodata_data = rodata.data()
            rodata_strings = extract_ascii_strings(rodata_data, base_offset=rodata['sh_addr'])
            print(f"    Found {len(rodata_strings)} raw strings")
        else:
            print("[!] No .rodata section found, scanning full binary...")
            f.seek(0)
            full_data = f.read()
            rodata_strings = extract_ascii_strings(full_data)
            print(f"    Found {len(rodata_strings)} raw strings from full binary")

        # ── Also check .data section ──
        data_sec = elf.get_section_by_name('.data')
        data_strings = []
        if data_sec:
            print(f"[*] Extracting strings from .data (size=0x{data_sec['sh_size']:x})")
            data_strings = extract_ascii_strings(data_sec.data(), base_offset=data_sec['sh_addr'])
            print(f"    Found {len(data_strings)} strings from .data")

        all_strings = rodata_strings + data_strings

        # ──────────── Categorization ────────────

        # 1. URLs and endpoints
        print("[*] Categorizing: URLs and endpoints")
        url_pattern = re.compile(r'^(https?://|wss?://)\S+', re.IGNORECASE)
        for offset, s in all_strings:
            if url_pattern.match(s):
                findings['urls'].append((offset, s))

        # 2. IP addresses
        print("[*] Categorizing: IP addresses")
        ip_pattern = re.compile(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b')
        for offset, s in all_strings:
            m = ip_pattern.search(s)
            if m:
                # Validate it looks like a real IP
                parts = m.group(1).split('.')
                if all(0 <= int(p) <= 255 for p in parts):
                    findings['ip_addresses'].append((offset, s))

        # 3. Server hostnames
        print("[*] Categorizing: Server hostnames")
        hostname_patterns = [
            re.compile(r'[\w.-]+\.igg\.(com|net|io)', re.IGNORECASE),
            re.compile(r'[\w.-]+\.(amazonaws|cloudfront|cloudflare|akamai)', re.IGNORECASE),
            re.compile(r'[\w.-]+\.(gameserver|gamehost|game-server)', re.IGNORECASE),
            re.compile(r'[\w.-]+\.igg[\w]*\.\w+', re.IGNORECASE),
        ]
        for offset, s in all_strings:
            for pat in hostname_patterns:
                if pat.search(s):
                    findings['hostnames'].append((offset, s))
                    break

        # 4. Game config keys
        print("[*] Categorizing: Game config keys")
        config_keywords = [
            'max_march', 'train_speed', 'gather_speed', 'march_speed',
            'attack_power', 'defense_power', 'build_speed', 'research_speed',
            'troop_load', 'march_size', 'rally_size', 'hero_',
            'vip_', 'guild_', 'resource_', 'food_', 'stone_', 'wood_', 'ore_', 'gold_',
            'shelter_', 'hospital_', 'barracks_', 'castle_', 'wall_',
            'infantry_', 'cavalry_', 'ranged_', 'siege_',
            'buff_', 'boost_', 'bonus_', 'multiplier_',
            'cooldown', 'duration', 'capacity', 'limit',
            'unlock_', 'level_', 'upgrade_', 'requirement_',
        ]
        for offset, s in all_strings:
            s_lower = s.lower()
            for kw in config_keywords:
                if kw in s_lower:
                    findings['config_keys'].append((offset, s))
                    break

        # 5. Error messages
        print("[*] Categorizing: Error messages")
        error_keywords = ['error', 'fail', 'invalid', 'timeout', 'exception',
                          'denied', 'refused', 'disconnect', 'abort', 'corrupt',
                          'mismatch', 'expired', 'unauthorized', 'forbidden',
                          'overflow', 'underflow', 'null', 'nullptr', 'crash',
                          'fatal', 'panic', 'assert', 'violation']
        for offset, s in all_strings:
            s_lower = s.lower()
            if any(kw in s_lower for kw in error_keywords):
                # Filter out very short strings or single-word matches
                if len(s) >= 8:
                    findings['errors'].append((offset, s))

        # 6. Feature flags / config names (lowercase_with_underscores, 3+ parts)
        print("[*] Categorizing: Feature flags / config names")
        config_name_pattern = re.compile(r'^[a-z][a-z0-9]*(_[a-z0-9]+){1,}$')
        seen_configs = set()
        for offset, s in all_strings:
            if config_name_pattern.match(s) and len(s) >= 6 and len(s) <= 80:
                if s not in seen_configs:
                    seen_configs.add(s)
                    findings['feature_flags'].append((offset, s))

        # 7. Hardcoded secrets/keys
        print("[*] Categorizing: Hardcoded secrets/keys")
        secret_patterns = [
            re.compile(r'(api[_-]?key|secret|token|password|auth[_-]?key|private[_-]?key|'
                       r'access[_-]?key|session[_-]?key|encryption[_-]?key|aes[_-]?key|'
                       r'hmac|sign[_-]?key|client[_-]?secret|app[_-]?secret)', re.IGNORECASE),
            # Base64-ish long strings that might be keys
            re.compile(r'^[A-Za-z0-9+/=]{20,}$'),
            # Hex-looking strings of key-like length
            re.compile(r'^[0-9a-fA-F]{16,}$'),
        ]
        for offset, s in all_strings:
            for pat in secret_patterns:
                if pat.search(s):
                    # Exclude common false positives
                    if not any(fp in s.lower() for fp in ['copyright', 'license', 'version',
                                                           'android', 'java.lang', 'com.igg']):
                        findings['secrets'].append((offset, s))
                    break

        # 8. File paths
        print("[*] Categorizing: File paths")
        path_patterns = [
            re.compile(r'^/[\w./-]+\.\w+$'),  # Unix paths with extension
            re.compile(r'^\w+/[\w./-]+\.\w+$'),  # Relative paths
            re.compile(r'\.(?:png|jpg|jpeg|gif|bmp|xml|json|lua|csv|dat|bin|so|'
                       r'plist|conf|cfg|db|sqlite|pb|proto|mp3|ogg|wav|pvr|pkm|'
                       r'ttf|fnt|pem|crt|key|cer)$', re.IGNORECASE),
        ]
        seen_paths = set()
        for offset, s in all_strings:
            for pat in path_patterns:
                if pat.search(s) and '/' in s:
                    if s not in seen_paths:
                        seen_paths.add(s)
                        findings['file_paths'].append((offset, s))
                    break

        # 9. JSON/protobuf field names
        print("[*] Categorizing: JSON/protobuf field names")
        field_name_pattern = re.compile(r'^[a-z][a-zA-Z0-9]{2,20}$')
        field_counter = Counter()
        for _, s in all_strings:
            if field_name_pattern.match(s):
                field_counter[s] += 1
        # Keep fields that appear multiple times (likely used as keys)
        for field, count in field_counter.most_common(500):
            if count >= 2:
                findings['json_fields'].append((count, field))

        # 10. Numeric constants near encryption code
        print(f"[*] Extracting numeric constants near crypto region "
              f"0x{CRYPTO_REGION_START:08X}-0x{CRYPTO_REGION_END:08X}")

        # We need to find which section contains this address range
        crypto_constants = []
        for sec in elf.iter_sections():
            sec_start = sec['sh_addr']
            sec_end = sec_start + sec['sh_size']
            if sec_start <= CRYPTO_REGION_START < sec_end:
                file_offset = sec['sh_offset'] + (CRYPTO_REGION_START - sec_start)
                read_len = min(CRYPTO_REGION_END - CRYPTO_REGION_START, sec_end - CRYPTO_REGION_START)
                f.seek(file_offset)
                crypto_data = f.read(read_len)
                print(f"    Found in section '{sec.name}' at file offset 0x{file_offset:x}")

                # Extract 4-byte constants
                for i in range(0, len(crypto_data) - 3, 4):
                    val = struct.unpack('<I', crypto_data[i:i+4])[0]
                    addr = CRYPTO_REGION_START + i
                    crypto_constants.append((addr, val))

                # Also extract 8-byte constants
                for i in range(0, len(crypto_data) - 7, 8):
                    val = struct.unpack('<Q', crypto_data[i:i+8])[0]
                    addr = CRYPTO_REGION_START + i
                    crypto_constants.append((addr, val))

                # Check for strings in the region too
                crypto_strings = extract_ascii_strings(crypto_data, base_offset=CRYPTO_REGION_START)
                findings['crypto_strings'] = crypto_strings
                break

        # Also scan a wider region around the crypto area
        WIDE_START = CRYPTO_REGION_START - 0x1000
        WIDE_END = CRYPTO_REGION_END + 0x1000
        for sec in elf.iter_sections():
            sec_start = sec['sh_addr']
            sec_end = sec_start + sec['sh_size']
            if sec_start <= WIDE_START and sec_end >= WIDE_END:
                file_offset = sec['sh_offset'] + (WIDE_START - sec_start)
                read_len = WIDE_END - WIDE_START
                f.seek(file_offset)
                wide_data = f.read(read_len)
                wide_strings = extract_ascii_strings(wide_data, min_len=4, base_offset=WIDE_START)
                findings['crypto_nearby_strings'] = wide_strings
                print(f"    Found {len(wide_strings)} strings in wide crypto region")
                break

        findings['crypto_constants'] = crypto_constants

        # ── 11 & 12. Dynamic symbol table analysis ──
        print("[*] Analyzing dynamic symbol table (.dynsym / .dynstr)")
        class_names = set()
        key_functions = []
        all_demangled = []

        func_keywords = ['encode', 'decode', 'encrypt', 'decrypt', 'send', 'recv',
                         'connect', 'login', 'auth', 'token', 'key', 'session',
                         'march', 'attack', 'build', 'train', 'research',
                         'cipher', 'crypt', 'hash', 'hmac', 'aes', 'rsa',
                         'ssl', 'tls', 'socket', 'tcp', 'udp', 'http',
                         'packet', 'msg', 'message', 'codec', 'serial',
                         'protobuf', 'proto', 'parse', 'gather', 'troop',
                         'hero', 'guild', 'chat', 'war', 'rally', 'shield',
                         'resource', 'inventory', 'quest', 'event', 'shop',
                         'purchase', 'payment', 'iap', 'verify']

        for sec in elf.iter_sections():
            if isinstance(sec, SymbolTableSection):
                print(f"    Processing {sec.name} ({sec.num_symbols()} symbols)")
                for sym in sec.iter_symbols():
                    name = sym.name
                    if not name:
                        continue

                    demangled = demangle_symbol(name)
                    all_demangled.append((name, demangled))

                    # Extract class names from demangled names
                    if '::' in demangled:
                        parts = demangled.split('::')
                        # First part (or first few) are typically namespaces/classes
                        for part in parts[:-1]:
                            # Clean up template params
                            clean = re.sub(r'<.*>', '', part).strip()
                            if clean and len(clean) > 2 and clean[0].isupper():
                                class_names.add(clean)

                    # Check for key function signatures
                    name_lower = demangled.lower()
                    for kw in func_keywords:
                        if kw in name_lower:
                            key_functions.append((name, demangled))
                            break

        findings['class_names'] = sorted(class_names)
        findings['key_functions'] = key_functions
        print(f"    Found {len(class_names)} class names, {len(key_functions)} key functions")

        # ── Also look at .dynstr directly for additional strings ──
        dynstr = elf.get_section_by_name('.dynstr')
        if dynstr:
            print(f"[*] Scanning .dynstr section (size=0x{dynstr['sh_size']:x})")
            dynstr_data = dynstr.data()
            dynstr_strings = extract_ascii_strings(dynstr_data, min_len=3, base_offset=dynstr['sh_addr'])
            # Filter for interesting ones
            for offset, s in dynstr_strings:
                if any(kw in s.lower() for kw in ['igg', 'game', 'lord', 'castle', 'war',
                                                     'kingdom', 'mobile']):
                    findings['dynstr_game_strings'].append((offset, s))

        # ── Special: look for the encryption table and nearby data ──
        print("[*] Searching for known encryption table bytes [0x58, 0xef, 0xd7, 0x14, 0xa2, 0x3b, 0x9c]")
        table_bytes = bytes([0x58, 0xef, 0xd7, 0x14, 0xa2, 0x3b, 0x9c])
        f.seek(0)
        full_data = f.read()
        table_locations = []
        pos = 0
        while True:
            pos = full_data.find(table_bytes, pos)
            if pos == -1:
                break
            # Get context around it
            ctx_start = max(0, pos - 64)
            ctx_end = min(len(full_data), pos + 64)
            context = full_data[ctx_start:ctx_end]
            table_locations.append((pos, context))
            pos += 1
        findings['encryption_table_locations'] = table_locations
        print(f"    Found table at {len(table_locations)} location(s)")

        # For each location, try to map it to a section
        for loc_offset, _ in table_locations:
            for sec in elf.iter_sections():
                if sec['sh_offset'] <= loc_offset < sec['sh_offset'] + sec['sh_size']:
                    vaddr = sec['sh_addr'] + (loc_offset - sec['sh_offset'])
                    print(f"    Table at file offset 0x{loc_offset:x} -> "
                          f"section '{sec.name}' vaddr 0x{vaddr:x}")
                    break

        # ── Special: Search for "CQ_secret" and related auth strings ──
        print("[*] Searching for auth-related hardcoded strings")
        auth_search = ['CQ_secret', 'access_key', 'session_key', 'server_key',
                        'CMSG', 'SMSG', 'opcode', 'packet_id',
                        'login_token', 'auth_token', 'game_token',
                        'gateway', 'handshake', 'challenge']
        for needle in auth_search:
            needle_bytes = needle.encode('ascii')
            pos = full_data.find(needle_bytes)
            if pos != -1:
                # Get surrounding context
                ctx_start = max(0, pos - 32)
                ctx_end = min(len(full_data), pos + len(needle_bytes) + 32)
                context_bytes = full_data[ctx_start:ctx_end]
                context_ascii = ''.join(chr(b) if 0x20 <= b <= 0x7e else '.' for b in context_bytes)
                findings['auth_strings'].append((pos, needle, context_ascii))
                print(f"    Found '{needle}' at file offset 0x{pos:x}")

        # ── Section summary for reference ──
        findings['sections'] = section_info

    # ──────────────────────── Write Output ────────────────────────

    print(f"\n[*] Writing findings to {OUTPUT}")
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    with open(OUTPUT, 'w', encoding='utf-8') as out:
        out.write("# libgame.so String & Constant Analysis\n\n")
        out.write(f"**Binary:** `{LIBGAME}`  \n")
        out.write(f"**Size:** {os.path.getsize(LIBGAME):,} bytes  \n")
        out.write(f"**Total strings extracted:** {len(rodata_strings)} (.rodata) + {len(data_strings)} (.data)\n\n")
        out.write("---\n\n")

        # Section map
        out.write("## ELF Section Map\n\n")
        out.write("| Section | Type | Offset | Size | VAddr |\n")
        out.write("|---------|------|--------|------|-------|\n")
        for name, stype, offset, size, vaddr in findings['sections']:
            if name:
                out.write(f"| `{name}` | {stype} | {offset} | {size} | {vaddr} |\n")
        out.write("\n---\n\n")

        # 1. URLs
        out.write("## 1. URLs and Endpoints\n\n")
        urls = findings.get('urls', [])
        out.write(f"**Count:** {len(urls)}\n\n")
        if urls:
            # Deduplicate and sort
            seen = set()
            for offset, s in sorted(urls, key=lambda x: x[1]):
                if s not in seen:
                    seen.add(s)
                    out.write(f"- `0x{offset:08X}`: `{s}`\n")
        out.write("\n---\n\n")

        # 2. IP Addresses
        out.write("## 2. IP Addresses\n\n")
        ips = findings.get('ip_addresses', [])
        out.write(f"**Count:** {len(ips)}\n\n")
        seen = set()
        for offset, s in sorted(ips, key=lambda x: x[1]):
            if s not in seen:
                seen.add(s)
                out.write(f"- `0x{offset:08X}`: `{s}`\n")
        out.write("\n---\n\n")

        # 3. Server Hostnames
        out.write("## 3. Server Hostnames\n\n")
        hosts = findings.get('hostnames', [])
        out.write(f"**Count:** {len(hosts)}\n\n")
        seen = set()
        for offset, s in sorted(hosts, key=lambda x: x[1]):
            if s not in seen:
                seen.add(s)
                out.write(f"- `0x{offset:08X}`: `{s}`\n")
        out.write("\n---\n\n")

        # 4. Game Config Keys
        out.write("## 4. Game Config Keys\n\n")
        configs = findings.get('config_keys', [])
        out.write(f"**Count:** {len(configs)}\n\n")
        seen = set()
        for offset, s in sorted(configs, key=lambda x: x[1]):
            if s not in seen:
                seen.add(s)
                out.write(f"- `0x{offset:08X}`: `{s}`\n")
        out.write("\n---\n\n")

        # 5. Error Messages
        out.write("## 5. Error Messages\n\n")
        errors = findings.get('errors', [])
        out.write(f"**Count:** {len(errors)}\n\n")
        # Group by keyword
        error_groups = defaultdict(list)
        for offset, s in errors:
            for kw in error_keywords:
                if kw in s.lower():
                    error_groups[kw].append((offset, s))
                    break
        for kw in sorted(error_groups.keys()):
            out.write(f"### {kw.upper()}\n\n")
            seen = set()
            for offset, s in sorted(error_groups[kw], key=lambda x: x[1])[:50]:
                if s not in seen:
                    seen.add(s)
                    out.write(f"- `0x{offset:08X}`: `{s}`\n")
            out.write("\n")
        out.write("\n---\n\n")

        # 6. Feature Flags / Config Names
        out.write("## 6. Feature Flags / Config Names\n\n")
        flags = findings.get('feature_flags', [])
        out.write(f"**Count (unique):** {len(flags)}\n\n")
        # Group by prefix
        flag_groups = defaultdict(list)
        for offset, s in flags:
            prefix = s.split('_')[0]
            flag_groups[prefix].append((offset, s))

        # Show top groups
        top_prefixes = sorted(flag_groups.keys(), key=lambda p: -len(flag_groups[p]))
        for prefix in top_prefixes[:40]:
            items = flag_groups[prefix]
            if len(items) >= 3:
                out.write(f"### `{prefix}_*` ({len(items)} entries)\n\n")
                for offset, s in sorted(items, key=lambda x: x[1])[:30]:
                    out.write(f"- `{s}`\n")
                out.write("\n")
        # Also show interesting singletons
        out.write("### Notable Individual Flags\n\n")
        game_flag_kws = ['march', 'attack', 'gather', 'train', 'build', 'research',
                         'troop', 'hero', 'guild', 'war', 'rally', 'siege',
                         'resource', 'food', 'stone', 'wood', 'gold', 'ore',
                         'shield', 'boost', 'buff', 'speed', 'power', 'defense',
                         'encrypt', 'decrypt', 'packet', 'socket', 'server', 'client',
                         'login', 'auth', 'token', 'session', 'connect', 'send', 'recv']
        seen = set()
        for offset, s in flags:
            if any(kw in s for kw in game_flag_kws) and s not in seen:
                seen.add(s)
                out.write(f"- `{s}`\n")
        out.write("\n---\n\n")

        # 7. Hardcoded Secrets/Keys
        out.write("## 7. Potential Hardcoded Secrets/Keys\n\n")
        secrets = findings.get('secrets', [])
        out.write(f"**Count:** {len(secrets)}\n\n")
        seen = set()
        for offset, s in sorted(secrets, key=lambda x: x[1]):
            if s not in seen:
                seen.add(s)
                # Truncate very long strings
                display = s if len(s) <= 120 else s[:120] + "..."
                out.write(f"- `0x{offset:08X}`: `{display}`\n")
        out.write("\n---\n\n")

        # 8. File Paths
        out.write("## 8. File Paths\n\n")
        paths = findings.get('file_paths', [])
        out.write(f"**Count:** {len(paths)}\n\n")
        # Group by extension
        ext_groups = defaultdict(list)
        for offset, s in paths:
            ext = s.rsplit('.', 1)[-1].lower() if '.' in s else 'none'
            ext_groups[ext].append((offset, s))
        for ext in sorted(ext_groups.keys()):
            items = ext_groups[ext]
            out.write(f"### .{ext} ({len(items)} files)\n\n")
            seen = set()
            for offset, s in sorted(items, key=lambda x: x[1])[:50]:
                if s not in seen:
                    seen.add(s)
                    out.write(f"- `{s}`\n")
            if len(items) > 50:
                out.write(f"- ... and {len(items) - 50} more\n")
            out.write("\n")
        out.write("\n---\n\n")

        # 9. JSON/Protobuf Field Names
        out.write("## 9. Frequent JSON/Protobuf Field Names\n\n")
        fields = findings.get('json_fields', [])
        out.write(f"**Count (freq >= 2):** {len(fields)}\n\n")
        out.write("| Field | Occurrences |\n")
        out.write("|-------|------------|\n")
        for count, field in fields[:200]:
            out.write(f"| `{field}` | {count} |\n")
        out.write("\n---\n\n")

        # 10. Numeric Constants near Encryption Code
        out.write("## 10. Numeric Constants near Crypto Region\n\n")
        out.write(f"**Region:** `0x{CRYPTO_REGION_START:08X}` - `0x{CRYPTO_REGION_END:08X}`\n\n")

        crypto_consts = findings.get('crypto_constants', [])
        if crypto_consts:
            out.write("### 4-byte Constants (uint32)\n\n")
            out.write("| Address | Hex | Decimal |\n")
            out.write("|---------|-----|--------|\n")
            seen_addrs = set()
            for addr, val in crypto_consts:
                if addr not in seen_addrs and val < 0x100000000:
                    seen_addrs.add(addr)
                    out.write(f"| `0x{addr:08X}` | `0x{val:08X}` | {val} |\n")
            out.write("\n")

        crypto_strs = findings.get('crypto_strings', [])
        if crypto_strs:
            out.write("### Strings in Crypto Region\n\n")
            for offset, s in crypto_strs:
                out.write(f"- `0x{offset:08X}`: `{s}`\n")
            out.write("\n")

        nearby_strs = findings.get('crypto_nearby_strings', [])
        if nearby_strs:
            out.write("### Strings in Extended Crypto Region (+/- 0x1000)\n\n")
            for offset, s in nearby_strs:
                out.write(f"- `0x{offset:08X}`: `{s}`\n")
            out.write("\n")

        out.write("---\n\n")

        # Encryption table locations
        out.write("## Encryption Table Locations\n\n")
        out.write("**Known table:** `[0x58, 0xEF, 0xD7, 0x14, 0xA2, 0x3B, 0x9C]`\n\n")
        table_locs = findings.get('encryption_table_locations', [])
        out.write(f"**Found at:** {len(table_locs)} location(s)\n\n")
        for loc_offset, context in table_locs:
            out.write(f"### File Offset `0x{loc_offset:X}`\n\n")
            out.write("Context (hex dump, -64 to +64 bytes):\n\n")
            out.write("```\n")
            for i in range(0, len(context), 16):
                hex_part = ' '.join(f'{b:02X}' for b in context[i:i+16])
                ascii_part = ''.join(chr(b) if 0x20 <= b <= 0x7e else '.' for b in context[i:i+16])
                out.write(f"  {loc_offset - 64 + i:08X}  {hex_part:<48s}  {ascii_part}\n")
            out.write("```\n\n")
        out.write("---\n\n")

        # Auth strings
        out.write("## Auth-Related Hardcoded Strings\n\n")
        auth_strs = findings.get('auth_strings', [])
        for pos, needle, context in auth_strs:
            out.write(f"- **`{needle}`** at file offset `0x{pos:X}`\n")
            out.write(f"  - Context: `{context}`\n")
        out.write("\n---\n\n")

        # 11. Class Names
        out.write("## 11. C++ Class Names (from .dynsym)\n\n")
        class_list = findings.get('class_names', [])
        out.write(f"**Count:** {len(class_list)}\n\n")
        # Group alphabetically
        letter_groups = defaultdict(list)
        for name in class_list:
            letter_groups[name[0].upper()].append(name)
        for letter in sorted(letter_groups.keys()):
            items = letter_groups[letter]
            out.write(f"### {letter}\n\n")
            for name in sorted(items):
                out.write(f"- `{name}`\n")
            out.write("\n")
        out.write("---\n\n")

        # 12. Key Function Signatures
        out.write("## 12. Key Function Signatures\n\n")
        key_funcs = findings.get('key_functions', [])
        out.write(f"**Count:** {len(key_funcs)}\n\n")

        # Group by keyword
        func_groups = defaultdict(list)
        for mangled, demangled in key_funcs:
            for kw in func_keywords:
                if kw in demangled.lower():
                    func_groups[kw].append((mangled, demangled))
                    break

        for kw in sorted(func_groups.keys()):
            items = func_groups[kw]
            out.write(f"### `{kw}` ({len(items)} matches)\n\n")
            seen = set()
            for mangled, demangled in sorted(items, key=lambda x: x[1])[:40]:
                if demangled not in seen:
                    seen.add(demangled)
                    out.write(f"- `{demangled}`\n")
                    if mangled != demangled:
                        out.write(f"  - Mangled: `{mangled}`\n")
            if len(items) > 40:
                out.write(f"- ... and {len(items) - 40} more\n")
            out.write("\n")

        # Dynstr game strings
        dynstr_game = findings.get('dynstr_game_strings', [])
        if dynstr_game:
            out.write("---\n\n")
            out.write("## Bonus: Game-Related Strings from .dynstr\n\n")
            seen = set()
            for offset, s in sorted(dynstr_game, key=lambda x: x[1]):
                if s not in seen:
                    seen.add(s)
                    out.write(f"- `{s}`\n")

        # Summary statistics
        out.write("\n---\n\n")
        out.write("## Summary Statistics\n\n")
        out.write(f"| Category | Count |\n")
        out.write(f"|----------|-------|\n")
        out.write(f"| URLs/Endpoints | {len(findings.get('urls', []))} |\n")
        out.write(f"| IP Addresses | {len(findings.get('ip_addresses', []))} |\n")
        out.write(f"| Server Hostnames | {len(findings.get('hostnames', []))} |\n")
        out.write(f"| Game Config Keys | {len(findings.get('config_keys', []))} |\n")
        out.write(f"| Error Messages | {len(findings.get('errors', []))} |\n")
        out.write(f"| Feature Flags | {len(findings.get('feature_flags', []))} |\n")
        out.write(f"| Potential Secrets | {len(findings.get('secrets', []))} |\n")
        out.write(f"| File Paths | {len(findings.get('file_paths', []))} |\n")
        out.write(f"| JSON Fields (freq>=2) | {len(findings.get('json_fields', []))} |\n")
        out.write(f"| C++ Classes | {len(findings.get('class_names', []))} |\n")
        out.write(f"| Key Functions | {len(findings.get('key_functions', []))} |\n")
        out.write(f"| Encryption Table Locations | {len(findings.get('encryption_table_locations', []))} |\n")
        out.write(f"| Auth Strings Found | {len(findings.get('auth_strings', []))} |\n")

    print(f"\n[+] Done! Output written to: {OUTPUT}")
    print(f"    File size: {os.path.getsize(OUTPUT):,} bytes")


if __name__ == '__main__':
    main()

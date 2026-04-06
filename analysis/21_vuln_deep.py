#!/usr/bin/env python3
"""
Deep vulnerability analysis of libgame.so (ARM64 ELF, ~104MB).
Scans .rodata, .dynstr, .dynsym for security-relevant strings, URLs,
debug/admin features, crypto weaknesses, hardcoded IPs, and more.
"""

import struct
import re
import os
import sys
from collections import defaultdict
from datetime import datetime

LIBGAME = r"D:\CascadeProjects\libgame.so"
OPCODE_MAP = r"D:\CascadeProjects\analysis\findings\opcode_map_complete.md"
OUTPUT = r"D:\CascadeProjects\analysis\findings\vulnerability_deep.md"

# ELF section info (from prior analysis)
SECTIONS = {
    "text":   {"offset": 0x3250E80, "size": 43562076},
    "rodata": {"offset": 0x255B000, "size": 4329528},
    "dynstr": {"offset": 0x682A10, "size": None},  # will read a generous chunk
}

def read_section(f, name, extra_size=None):
    s = SECTIONS[name]
    f.seek(s["offset"])
    size = s["size"] or extra_size or 0x200000
    return f.read(size)

def extract_strings(data, min_len=4):
    """Extract printable ASCII strings from binary data."""
    result = []
    current = bytearray()
    start = 0
    for i, b in enumerate(data):
        if 0x20 <= b < 0x7f:
            if not current:
                start = i
            current.append(b)
        else:
            if len(current) >= min_len:
                result.append((start, current.decode('ascii', errors='replace')))
            current = bytearray()
    if len(current) >= min_len:
        result.append((start, current.decode('ascii', errors='replace')))
    return result

def search_strings_for_patterns(strings, patterns, case_insensitive=True):
    """Search extracted strings for regex patterns."""
    results = defaultdict(list)
    for offset, s in strings:
        for pat_name, pat in patterns.items():
            flags = re.IGNORECASE if case_insensitive else 0
            if re.search(pat, s, flags):
                results[pat_name].append((offset, s))
    return results

def parse_opcode_map(path):
    """Parse the opcode map markdown table."""
    opcodes = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line.startswith('|') or 'Opcode' in line or '---' in line:
                continue
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 6:
                try:
                    opcode_dec = int(parts[1])
                    opcode_hex = parts[2]
                    name = parts[3]
                    constructor = parts[4]
                    direction = parts[5]
                    opcodes.append({
                        'dec': opcode_dec,
                        'hex': opcode_hex,
                        'name': name,
                        'constructor': constructor,
                        'direction': direction,
                    })
                except (ValueError, IndexError):
                    pass
    return opcodes

def main():
    print(f"[*] Opening {LIBGAME} ...")
    f = open(LIBGAME, 'rb')

    # ===== Read sections =====
    print("[*] Reading .rodata section ...")
    rodata = read_section(f, "rodata")
    print(f"    Read {len(rodata):,} bytes from .rodata")

    print("[*] Reading .dynstr section ...")
    dynstr = read_section(f, "dynstr", extra_size=0x300000)
    print(f"    Read {len(dynstr):,} bytes from .dynstr area")

    print("[*] Extracting strings from .rodata ...")
    rodata_strings = extract_strings(rodata, min_len=5)
    print(f"    Found {len(rodata_strings):,} strings")

    print("[*] Extracting strings from .dynstr ...")
    dynstr_strings = extract_strings(dynstr, min_len=4)
    print(f"    Found {len(dynstr_strings):,} strings")

    results = {}

    # ===== 1. Server-side validation gaps =====
    print("\n[1] Searching for server-side validation/error strings ...")
    validation_patterns = {
        "invalid":    r'\binvalid\b',
        "illegal":    r'\billegal\b',
        "overflow":   r'\boverflow\b',
        "exceed":     r'\bexceed\b',
        "limit":      r'\blimit\b',
        "hack":       r'\bhack\b',
        "cheat":      r'\bcheat\b',
        "ban":        r'\bban\b',
        "error":      r'\berror\b',
        "forbidden":  r'\bforbidden\b',
        "deny":       r'\bdeny|denied\b',
        "reject":     r'\breject\b',
        "timeout":    r'\btimeout\b',
        "cooldown":   r'\bcooldown\b',
        "max_":       r'\bmax_\w+',
        "min_":       r'\bmin_\w+',
        "check_fail": r'check.{0,5}fail',
        "verify":     r'\bverify|verification\b',
        "validate":   r'\bvalidat',
        "permission": r'\bpermission\b',
        "privilege":  r'\bprivileg',
        "unauthorized": r'\bunauthoriz',
        "anti":       r'\banti.?cheat|anti.?hack|anti.?bot',
        "detect":     r'\bdetect',
        "sanity":     r'\bsanity',
        "bounds":     r'\bbounds?\b',
    }
    validation_hits = search_strings_for_patterns(rodata_strings, validation_patterns)
    total_v = sum(len(v) for v in validation_hits.values())
    print(f"    Found {total_v} validation-related strings across {len(validation_hits)} categories")
    results["validation"] = validation_hits

    # ===== 2. URLs and endpoints =====
    print("\n[2] Searching for URLs and endpoints ...")
    url_pattern = re.compile(rb'https?://[^\x00\x01-\x1f\x7f]{5,300}')
    url_matches = []
    for m in url_pattern.finditer(rodata):
        url = m.group().decode('ascii', errors='replace').rstrip('\\').rstrip('"').rstrip("'")
        url_matches.append((m.start(), url))
    print(f"    Found {len(url_matches)} URLs in .rodata")

    # Categorize URLs
    url_categories = defaultdict(list)
    for off, url in url_matches:
        url_lower = url.lower()
        if 'admin' in url_lower or 'manage' in url_lower:
            url_categories['admin'].append((off, url))
        elif 'debug' in url_lower or 'test' in url_lower:
            url_categories['debug_test'].append((off, url))
        elif 'api' in url_lower:
            url_categories['api'].append((off, url))
        elif 'cdn' in url_lower or 'static' in url_lower or 'resource' in url_lower or 'download' in url_lower:
            url_categories['cdn_resources'].append((off, url))
        elif 'analytics' in url_lower or 'track' in url_lower or 'log' in url_lower or 'stat' in url_lower:
            url_categories['analytics'].append((off, url))
        elif 'auth' in url_lower or 'login' in url_lower or 'oauth' in url_lower or 'token' in url_lower:
            url_categories['auth'].append((off, url))
        elif 'pay' in url_lower or 'purchase' in url_lower or 'billing' in url_lower or 'order' in url_lower:
            url_categories['payment'].append((off, url))
        elif 'igg' in url_lower or 'lordsmobile' in url_lower or 'conqueror' in url_lower:
            url_categories['igg_internal'].append((off, url))
        elif 'facebook' in url_lower or 'google' in url_lower or 'apple' in url_lower:
            url_categories['third_party_auth'].append((off, url))
        elif 'firebase' in url_lower or 'adjust' in url_lower or 'appsflyer' in url_lower:
            url_categories['sdk_services'].append((off, url))
        else:
            url_categories['other'].append((off, url))
    results["urls"] = url_categories

    # ===== 3. Debug/admin features =====
    print("\n[3] Searching for debug/admin/GM features ...")
    debug_patterns = {
        "debug":       r'\bdebug',
        "admin":       r'\badmin',
        "gm_":         r'\bgm_',
        "GM_":         r'GM_\w+',
        "test_":       r'\btest_',
        "backdoor":    r'\bbackdoor\b',
        "console":     r'\bconsole\b',
        "cheat_code":  r'cheat.?code',
        "god_mode":    r'god.?mode',
        "unlimited":   r'\bunlimited\b',
        "developer":   r'\bdeveloper\b',
        "devmode":     r'\bdevmode|dev.?mode\b',
        "internal":    r'\binternal\b',
        "secret":      r'\bsecret\b',
        "hidden":      r'\bhidden\b',
        "super_user":  r'super.?user|superuser',
        "root":        r'\broot\b',
        "master_key":  r'master.?key',
        "sandbox":     r'\bsandbox\b',
        "staging":     r'\bstaging\b',
        "whitelist":   r'\bwhitelist\b',
        "bypass":      r'\bbypass\b',
        "noclip":      r'\bnoclip\b',
        "godmode":     r'\bgodmode\b',
        "infinite":    r'\binfinite\b',
        "no_limit":    r'no.?limit',
        "free_":       r'\bfree_\w+',
    }
    debug_hits = search_strings_for_patterns(rodata_strings, debug_patterns)
    # Also check dynstr
    debug_hits_dynstr = search_strings_for_patterns(dynstr_strings, debug_patterns)
    total_d = sum(len(v) for v in debug_hits.values())
    total_dd = sum(len(v) for v in debug_hits_dynstr.values())
    print(f"    Found {total_d} debug/admin strings in .rodata, {total_dd} in .dynstr")
    results["debug_admin"] = {"rodata": debug_hits, "dynstr": debug_hits_dynstr}

    # ===== 4. Protocol manipulation =====
    print("\n[4] Analyzing protocol manipulation opportunities ...")
    opcodes = parse_opcode_map(OPCODE_MAP)
    print(f"    Loaded {len(opcodes)} opcodes from map")

    sync_opcodes = [o for o in opcodes if 'SYNC' in o['direction']]
    gm_admin_opcodes = [o for o in opcodes if re.search(r'GM|ADMIN|CHEAT|DEBUG|TEST', o['name'], re.IGNORECASE)]

    # Race condition: opcodes that touch same systems
    resource_opcodes = [o for o in opcodes if re.search(
        r'RESOURCE|ITEM|GOLD|GEM|DIAMOND|COIN|REWARD|COLLECT|LOOT|CHEST|BOX|EXCHANGE|TRADE|SHOP|BUY|SELL|CONSUME|SPEND',
        o['name'], re.IGNORECASE)]
    march_opcodes = [o for o in opcodes if re.search(r'MARCH|ATTACK|RALLY|SCOUT|DEFEND', o['name'], re.IGNORECASE)]
    building_opcodes = [o for o in opcodes if re.search(r'BUILD|CONSTRUCT|UPGRADE|WORKER', o['name'], re.IGNORECASE)]
    train_opcodes = [o for o in opcodes if re.search(r'TRAIN|RECRUIT|SOLDIER|ARMY|TROOP', o['name'], re.IGNORECASE)]

    results["protocol"] = {
        "sync_opcodes": sync_opcodes,
        "gm_admin_opcodes": gm_admin_opcodes,
        "resource_opcodes": resource_opcodes,
        "march_opcodes": march_opcodes,
        "building_opcodes": building_opcodes,
        "train_opcodes": train_opcodes,
    }
    print(f"    SYNC: {len(sync_opcodes)}, GM/Admin: {len(gm_admin_opcodes)}")
    print(f"    Resource: {len(resource_opcodes)}, March: {len(march_opcodes)}")
    print(f"    Building: {len(building_opcodes)}, Train: {len(train_opcodes)}")

    # ===== 5. Crypto weaknesses =====
    print("\n[5] Searching for crypto weaknesses ...")
    crypto_patterns = {
        "md5":           r'\bMD5|md5',
        "sha1":          r'\bSHA1|sha1(?!_)',
        "base64":        r'\bbase64|Base64',
        "xor":           r'\bXOR|xor_',
        "rc4":           r'\bRC4|rc4',
        "des":           r'\bDES_|des_',
        "ecb":           r'\bECB|ecb_mode',
        "weak_random":   r'\brand\(\)|srand|random_device',
        "hardcoded_key": r'(?:key|secret|password)\s*=\s*["\']',
        "ssl_ctx":       r'SSL_CTX|ssl_ctx',
        "x509":          r'X509|x509',
        "verify":        r'SSL_verify|verify_callback|VERIFY_NONE|VERIFY_PEER',
        "cert_pin":      r'pinning|certificate.?pin',
        "no_verify":     r'VERIFY_NONE|noverify|no.?verify|insecure',
        "aes":           r'\bAES|aes_',
        "rsa":           r'\bRSA|rsa_',
        "hmac":          r'\bHMAC|hmac',
        "pbkdf":         r'\bPBKDF|pbkdf',
        "blowfish":      r'\bBlowfish|blowfish',
    }
    crypto_rodata = search_strings_for_patterns(rodata_strings, crypto_patterns)
    crypto_dynstr = search_strings_for_patterns(dynstr_strings, crypto_patterns)
    total_cr = sum(len(v) for v in crypto_rodata.values())
    total_cd = sum(len(v) for v in crypto_dynstr.values())
    print(f"    Found {total_cr} crypto strings in .rodata, {total_cd} in .dynstr")
    results["crypto"] = {"rodata": crypto_rodata, "dynstr": crypto_dynstr}

    # ===== 6. Hardcoded IPs and ports =====
    print("\n[6] Searching for hardcoded IPs and ports ...")
    # IP:port pattern
    ip_port_re = re.compile(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?::\d{1,5})?)\b')
    ip_hits = []
    seen_ips = set()
    for off, s in rodata_strings:
        for m in ip_port_re.finditer(s):
            ip = m.group(1)
            # Filter out version-like strings (e.g. 1.0.0.1 without port)
            parts = ip.split(':')[0].split('.')
            try:
                if all(0 <= int(p) <= 255 for p in parts):
                    if ip not in seen_ips:
                        seen_ips.add(ip)
                        ip_hits.append((off, ip, s))
            except ValueError:
                pass
    print(f"    Found {len(ip_hits)} unique IPs/IP:port in .rodata")
    results["ips"] = ip_hits

    # ===== 7. Format string / memory corruption =====
    print("\n[7] Searching for format string patterns ...")
    fmt_patterns = {
        "format_n":   r'%n',  # dangerous - write to memory
        "format_s":   r'%s',
        "format_x":   r'%x',
        "format_p":   r'%p',
        "format_lx":  r'%l[xud]',
        "sprintf":    r'\bsprintf\b',
        "strcpy":     r'\bstrcpy\b',
        "strcat":     r'\bstrcat\b',
        "gets":       r'\bgets\b',
        "scanf":      r'\bscanf\b',
        "memcpy":     r'\bmemcpy\b',
        "buffer":     r'\bbuffer.?overflow|buf.?overflow',
    }
    fmt_rodata = search_strings_for_patterns(rodata_strings, fmt_patterns, case_insensitive=False)
    fmt_dynstr = search_strings_for_patterns(dynstr_strings, fmt_patterns, case_insensitive=False)
    total_fr = sum(len(v) for v in fmt_rodata.values())
    total_fd = sum(len(v) for v in fmt_dynstr.values())
    print(f"    Found {total_fr} format/memory strings in .rodata, {total_fd} in .dynstr")
    results["format_strings"] = {"rodata": fmt_rodata, "dynstr": fmt_dynstr}

    # ===== Also search for interesting constants / magic values in .rodata =====
    print("\n[8] Bonus: searching for interesting constants ...")
    bonus_patterns = {
        "CQ_secret":   r'CQ_secret',
        "password":    r'\bpassword\b',
        "token":       r'\btoken\b',
        "auth_key":    r'auth.?key|access.?key|api.?key',
        "session":     r'\bsession.?id|session.?key',
        "encryption":  r'\bencrypt|decrypt',
        "private_key": r'private.?key|priv.?key',
        "public_key":  r'public.?key|pub.?key',
        "certificate": r'\bcertificate\b',
        "signature":   r'\bsignature\b',
    }
    bonus_hits = search_strings_for_patterns(rodata_strings, bonus_patterns)
    total_b = sum(len(v) for v in bonus_hits.values())
    print(f"    Found {total_b} interesting constant strings")
    results["bonus"] = bonus_hits

    f.close()

    # ===== Generate report =====
    print("\n[*] Generating report ...")
    generate_report(results)
    print(f"[*] Report written to {OUTPUT}")

def fmt_opcode_table(opcodes, max_show=50):
    lines = []
    lines.append("| Opcode | Name | Direction |")
    lines.append("|--------|------|-----------|")
    for o in opcodes[:max_show]:
        lines.append(f"| {o['hex']} | {o['name']} | {o['direction']} |")
    if len(opcodes) > max_show:
        lines.append(f"| ... | ({len(opcodes) - max_show} more) | ... |")
    return '\n'.join(lines)

def fmt_string_hits(hits, max_per_cat=15):
    lines = []
    for cat in sorted(hits.keys()):
        items = hits[cat]
        if not items:
            continue
        lines.append(f"\n**{cat}** ({len(items)} hits):")
        for off, s in items[:max_per_cat]:
            # Truncate long strings
            display = s[:120] + "..." if len(s) > 120 else s
            lines.append(f"- `0x{off:06X}`: `{display}`")
        if len(items) > max_per_cat:
            lines.append(f"- ... and {len(items) - max_per_cat} more")
    return '\n'.join(lines)

def generate_report(results):
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(f"# Deep Vulnerability Analysis - libgame.so\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Target: libgame.so (ARM64 ELF, ~104MB)\n\n")
        f.write("---\n\n")

        # 1. Validation gaps
        f.write("## 1. Server-Side Validation Gaps\n\n")
        f.write("These strings reveal server-side checks and validation logic.\n\n")
        vh = results["validation"]
        total = sum(len(v) for v in vh.values())
        f.write(f"**Total: {total} validation-related strings found**\n\n")
        f.write(fmt_string_hits(vh, max_per_cat=20))
        f.write("\n\n---\n\n")

        # 2. URLs
        f.write("## 2. URLs and Endpoints\n\n")
        uc = results["urls"]
        total_urls = sum(len(v) for v in uc.values())
        f.write(f"**Total: {total_urls} URLs found**\n\n")
        for cat in sorted(uc.keys()):
            items = uc[cat]
            if not items:
                continue
            f.write(f"### {cat} ({len(items)} URLs)\n\n")
            seen = set()
            for off, url in items:
                if url not in seen:
                    seen.add(url)
                    display = url[:200] + "..." if len(url) > 200 else url
                    f.write(f"- `{display}`\n")
            f.write("\n")
        f.write("---\n\n")

        # 3. Debug/Admin
        f.write("## 3. Debug/Admin/GM Features\n\n")
        da = results["debug_admin"]
        f.write("### In .rodata\n\n")
        f.write(fmt_string_hits(da["rodata"], max_per_cat=20))
        f.write("\n\n### In .dynstr (exported symbols)\n\n")
        f.write(fmt_string_hits(da["dynstr"], max_per_cat=20))
        f.write("\n\n---\n\n")

        # 4. Protocol manipulation
        f.write("## 4. Protocol Manipulation Opportunities\n\n")
        proto = results["protocol"]

        f.write("### 4.1 SYNC Opcodes (Server->Client state sync, potential desync exploits)\n\n")
        f.write(f"**{len(proto['sync_opcodes'])} SYNC opcodes found** - these push server state to client.\n")
        f.write("A desync between client and server state could be exploited.\n\n")
        f.write(fmt_opcode_table(proto['sync_opcodes']))
        f.write("\n\n")

        f.write("### 4.2 GM/Admin Opcodes\n\n")
        if proto['gm_admin_opcodes']:
            f.write(fmt_opcode_table(proto['gm_admin_opcodes']))
        else:
            f.write("No explicit GM/ADMIN opcodes found in opcode names.\n")
        f.write("\n\n")

        f.write("### 4.3 Race Condition Targets\n\n")
        f.write("#### Resource-Related Opcodes (double-spend, duplication)\n\n")
        f.write(fmt_opcode_table(proto['resource_opcodes'], max_show=30))
        f.write("\n\n#### March/Attack Opcodes (timing exploits)\n\n")
        f.write(fmt_opcode_table(proto['march_opcodes'], max_show=30))
        f.write("\n\n#### Building Opcodes\n\n")
        f.write(fmt_opcode_table(proto['building_opcodes'], max_show=20))
        f.write("\n\n#### Training Opcodes\n\n")
        f.write(fmt_opcode_table(proto['train_opcodes'], max_show=20))
        f.write("\n\n---\n\n")

        # 5. Crypto
        f.write("## 5. Cryptographic Weaknesses\n\n")
        cr = results["crypto"]
        f.write("### In .rodata\n\n")
        f.write(fmt_string_hits(cr["rodata"], max_per_cat=15))
        f.write("\n\n### In .dynstr (exported/imported symbols)\n\n")
        f.write(fmt_string_hits(cr["dynstr"], max_per_cat=15))
        f.write("\n\n---\n\n")

        # 6. IPs
        f.write("## 6. Hardcoded IPs and Ports\n\n")
        ips = results["ips"]
        f.write(f"**{len(ips)} unique IPs found**\n\n")
        f.write("| IP/IP:Port | Context | Offset |\n")
        f.write("|------------|---------|--------|\n")
        for off, ip, ctx in ips[:60]:
            ctx_short = ctx[:80].replace('|', '/') if ctx != ip else ""
            f.write(f"| `{ip}` | `{ctx_short}` | 0x{off:06X} |\n")
        if len(ips) > 60:
            f.write(f"| ... | ({len(ips) - 60} more) | ... |\n")
        f.write("\n---\n\n")

        # 7. Format strings
        f.write("## 7. Memory Corruption Potential\n\n")
        fm = results["format_strings"]
        f.write("### In .rodata (format strings in data)\n\n")
        f.write(fmt_string_hits(fm["rodata"], max_per_cat=10))
        f.write("\n\n### In .dynstr (unsafe function imports)\n\n")
        f.write(fmt_string_hits(fm["dynstr"], max_per_cat=10))
        f.write("\n\n---\n\n")

        # 8. Bonus
        f.write("## 8. Interesting Constants (Secrets, Keys, Auth)\n\n")
        f.write(fmt_string_hits(results["bonus"], max_per_cat=20))
        f.write("\n\n---\n\n")

        # Summary
        f.write("## Summary & Key Findings\n\n")
        vh = results["validation"]
        f.write("### High Priority\n\n")
        f.write(f"1. **Validation strings**: {sum(len(v) for v in vh.values())} strings reveal server-side checks\n")
        f.write(f"2. **URLs found**: {total_urls} endpoints across {len(uc)} categories\n")
        f.write(f"3. **SYNC opcodes**: {len(proto['sync_opcodes'])} - potential state desync vectors\n")
        f.write(f"4. **Resource opcodes**: {len(proto['resource_opcodes'])} - race condition / double-spend targets\n")
        f.write(f"5. **Hardcoded IPs**: {len(ips)} unique addresses\n")
        f.write(f"6. **Crypto references**: {sum(len(v) for v in cr['rodata'].values()) + sum(len(v) for v in cr['dynstr'].values())} total\n")
        f.write("\n")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
28_deep_discovery.py - Comprehensive libgame.so analysis
========================================================
Discover: URLs, IPs, debug features, admin commands, crypto,
hidden strings, interesting constants, vulnerability patterns.
"""
import struct, re, sys
from collections import Counter

LIBGAME = r"D:\CascadeProjects\libgame.so"
with open(LIBGAME, "rb") as f:
    data = f.read()

# .rodata: offset 0x255B000, size 4329528
RODATA_OFF = 0x255B000
RODATA_SIZE = 4329528
rodata = data[RODATA_OFF:RODATA_OFF + RODATA_SIZE]

# .dynstr for symbol names
DYNSTR_OFF = 0x682A10
dynstr = data[DYNSTR_OFF:DYNSTR_OFF + 0x200000]  # ~2MB should be enough

out = []
def p(msg):
    out.append(msg)
    try: print(msg)
    except: print(msg.encode('ascii','replace').decode())

p("=" * 80)
p("DEEP DISCOVERY - libgame.so Analysis")
p("=" * 80)

# ═══════════════════════════════════════════════════════════════
# 1. ALL URLs (HTTP/HTTPS)
# ═══════════════════════════════════════════════════════════════
p("\n\n### 1. URLs Found in .rodata ###\n")
urls = set()
for m in re.finditer(rb'https?://[^\x00\x01-\x1f"\'<>\s]{5,200}', rodata):
    url = m.group().decode('ascii', errors='replace').rstrip('.')
    urls.add(url)

# Categorize
categories = {
    'Game API': [], 'CDN/Assets': [], 'Analytics': [],
    'Social/Auth': [], 'Payment': [], 'Admin/Debug': [],
    'SSL/Crypto': [], 'Other': []
}
for url in sorted(urls):
    u = url.lower()
    if any(x in u for x in ['admin', 'debug', 'test', 'dev', 'internal', 'gm_', 'backdoor']):
        categories['Admin/Debug'].append(url)
    elif any(x in u for x in ['igg.com', 'lordsmobile', 'conqueror', 'game']):
        categories['Game API'].append(url)
    elif any(x in u for x in ['cdn', 'asset', 'resource', 'download', 'update', 'patch']):
        categories['CDN/Assets'].append(url)
    elif any(x in u for x in ['analytics', 'track', 'log', 'stat', 'event', 'report']):
        categories['Analytics'].append(url)
    elif any(x in u for x in ['facebook', 'google', 'apple', 'oauth', 'login', 'auth', 'wechat', 'line']):
        categories['Social/Auth'].append(url)
    elif any(x in u for x in ['pay', 'purchase', 'store', 'bill', 'order', 'receipt']):
        categories['Payment'].append(url)
    elif any(x in u for x in ['ssl', 'cert', 'openssl', 'curl', 'ca-bundle']):
        categories['SSL/Crypto'].append(url)
    else:
        categories['Other'].append(url)

for cat, items in categories.items():
    if items:
        p(f"\n  [{cat}] ({len(items)}):")
        for url in items[:20]:
            p(f"    {url}")
        if len(items) > 20:
            p(f"    ... and {len(items)-20} more")

# ═══════════════════════════════════════════════════════════════
# 2. IP:PORT patterns
# ═══════════════════════════════════════════════════════════════
p("\n\n### 2. IP Addresses & Ports ###\n")
ips = set()
for m in re.finditer(rb'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(:\d{1,5})?', rodata):
    ip = m.group().decode('ascii')
    parts = ip.split(':')[0].split('.')
    if all(0 <= int(p_) <= 255 for p_ in parts):
        if not ip.startswith(('0.', '255.', '127.')):
            ips.add(ip)
for ip in sorted(ips):
    p(f"  {ip}")

# ═══════════════════════════════════════════════════════════════
# 3. Debug/Admin/GM/Cheat strings
# ═══════════════════════════════════════════════════════════════
p("\n\n### 3. Debug/Admin/GM/Cheat Strings ###\n")
patterns = [
    rb'[Dd]ebug[A-Z_]',
    rb'[Aa]dmin[A-Z_]',
    rb'[Gg][Mm]_\w+',
    rb'GM_\w+',
    rb'[Cc]heat\w*',
    rb'[Bb]ackdoor',
    rb'[Gg]od[Mm]ode',
    rb'[Uu]nlimited',
    rb'[Tt]est[Ss]erver',
    rb'[Tt]est[Mm]ode',
    rb'[Dd]ev[Mm]ode',
    rb'[Ss]ecret[Kk]ey',
    rb'[Mm]aster[Kk]ey',
    rb'[Bb]ypass',
    rb'noclip',
    rb'godmode',
    rb'infinite',
]
found_debug = set()
for pat in patterns:
    for m in re.finditer(pat, rodata):
        # Get surrounding context (null-terminated string)
        start = m.start()
        while start > 0 and rodata[start-1] != 0: start -= 1
        end = m.end()
        while end < len(rodata) and rodata[end] != 0: end += 1
        s = rodata[start:end].decode('ascii', errors='replace')
        if len(s) > 3 and len(s) < 200:
            found_debug.add(s)

for s in sorted(found_debug)[:100]:
    p(f"  {s}")

# ═══════════════════════════════════════════════════════════════
# 4. Hardcoded Keys, Tokens, Secrets
# ═══════════════════════════════════════════════════════════════
p("\n\n### 4. Hardcoded Keys/Tokens/Secrets ###\n")
secret_pats = [
    rb'[Ss]ecret["\s:=]+\w{8,}',
    rb'[Kk]ey["\s:=]+[A-Za-z0-9+/]{16,}',
    rb'[Tt]oken["\s:=]+[A-Za-z0-9+/]{16,}',
    rb'[Pp]assword["\s:=]+\w{6,}',
    rb'[A-Za-z0-9+/]{40,}={0,2}',  # Base64-like
    rb'-----BEGIN',
    rb'HMAC',
    rb'AES|DES|RSA|SHA256|MD5',
    rb'CQ_secret',
    rb'[Aa]pi[Kk]ey',
]
found_secrets = set()
for pat in secret_pats:
    for m in re.finditer(pat, rodata):
        start = max(0, m.start() - 20)
        while start > 0 and rodata[start-1] != 0: start -= 1
        end = m.end() + 20
        while end < len(rodata) and rodata[end] != 0: end += 1
        s = rodata[start:end].decode('ascii', errors='replace')
        if 5 < len(s) < 300 and not s.startswith('//'):
            found_secrets.add(s)

for s in sorted(found_secrets)[:50]:
    p(f"  {s}")

# ═══════════════════════════════════════════════════════════════
# 5. Error/Validation strings (reveal server-side checks)
# ═══════════════════════════════════════════════════════════════
p("\n\n### 5. Error/Validation Strings ###\n")
error_pats = [
    rb'[Ii]nvalid\s+\w+',
    rb'[Ii]llegal\s+\w+',
    rb'[Ee]xceed\s+\w+',
    rb'[Oo]verflow',
    rb'[Hh]ack\w*',
    rb'[Bb]an\w*',
    rb'[Kk]ick\w*',
    rb'[Bb]lock\w*',
    rb'not\s+enough',
    rb'not\s+allow',
    rb'forbidden',
    rb'permission\s+denied',
    rb'too\s+fast',
    rb'too\s+many',
    rb'cooldown',
    rb'rate\s+limit',
    rb'anti.?cheat',
    rb'detect\w*\s+cheat',
    rb'abnormal',
    rb'suspicious',
]
found_errors = set()
for pat in error_pats:
    for m in re.finditer(pat, rodata, re.IGNORECASE):
        start = m.start()
        while start > 0 and rodata[start-1] != 0: start -= 1
        end = m.end()
        while end < len(rodata) and rodata[end] != 0: end += 1
        s = rodata[start:end].decode('ascii', errors='replace')
        if 5 < len(s) < 200:
            found_errors.add(s)

for s in sorted(found_errors)[:80]:
    p(f"  {s}")

# ═══════════════════════════════════════════════════════════════
# 6. Interesting .dynsym symbols (GM, admin, debug, reward, free)
# ═══════════════════════════════════════════════════════════════
p("\n\n### 6. Interesting Dynamic Symbols ###\n")
sym_pats = [
    b'GM', b'Admin', b'Debug', b'Cheat', b'Free', b'Reward',
    b'Unlock', b'Hack', b'Speed', b'Unlimited', b'God',
    b'Test', b'Secret', b'Hidden', b'Backdoor', b'Bypass',
    b'VIP', b'Diamond', b'Gold', b'Gem', b'Premium',
    b'Purchase', b'Pay', b'Verify', b'Check', b'Validate',
    b'Ban', b'Kick', b'Punish', b'Detect',
    b'Encrypt', b'Decrypt', b'Key', b'Token', b'Auth',
    b'Exploit', b'Vuln', b'Overflow', b'Inject',
]
# Read .dynsym
DYNSYM_OFF = 0x2F8
DYNSYM_SIZE = 0x682758  # approximate
found_syms = {}
pos = DYNSYM_OFF
while pos + 24 <= DYNSYM_OFF + DYNSYM_SIZE:
    st_name = struct.unpack('<I', data[pos:pos+4])[0]
    st_value = struct.unpack('<Q', data[pos+8:pos+16])[0]
    if st_name > 0 and st_name < 0x200000:
        name_end = data.index(b'\x00', DYNSTR_OFF + st_name)
        name = data[DYNSTR_OFF + st_name:name_end]
        for pat in sym_pats:
            if pat.lower() in name.lower():
                found_syms[name.decode('ascii', errors='replace')] = st_value
                break
    pos += 24

for name in sorted(found_syms.keys())[:100]:
    addr = found_syms[name]
    # Demangle common C++ patterns
    short = name
    if short.startswith('_Z'):
        # Simple demangle
        short = name.replace('_ZN', '').replace('_Z', '')
    p(f"  0x{addr:08X} {short[:80]}")

# ═══════════════════════════════════════════════════════════════
# 7. Protocol message names with exploitable patterns
# ═══════════════════════════════════════════════════════════════
p("\n\n### 7. Exploitable CMSG Names ###\n")
exploit_keywords = [
    'FREE', 'REWARD', 'GIFT', 'CLAIM', 'COLLECT', 'CHEST',
    'SPEED', 'INSTANT', 'SKIP', 'COMPLETE',
    'UNLIMITED', 'INFINITE', 'MAX',
    'GM_', 'ADMIN', 'DEBUG', 'TEST',
    'DUPLICATE', 'CLONE', 'COPY',
    'DELETE', 'REMOVE', 'CANCEL',
    'EXCHANGE', 'CONVERT', 'TRADE',
    'MODIFY', 'CHANGE', 'SET',
    'BUY', 'PURCHASE', 'SHOP',
]
cmsg_syms = []
pos = DYNSYM_OFF
while pos + 24 <= DYNSYM_OFF + DYNSYM_SIZE:
    st_name = struct.unpack('<I', data[pos:pos+4])[0]
    st_value = struct.unpack('<Q', data[pos+8:pos+16])[0]
    if st_name > 0 and st_name < 0x200000:
        name_end = data.index(b'\x00', DYNSTR_OFF + st_name)
        name = data[DYNSTR_OFF + st_name:name_end].decode('ascii', errors='replace')
        if 'CMSG' in name:
            for kw in exploit_keywords:
                if kw in name.upper():
                    cmsg_syms.append((name, st_value, kw))
                    break
    pos += 24

# Group by keyword
from collections import defaultdict
by_kw = defaultdict(list)
for name, addr, kw in cmsg_syms:
    by_kw[kw].append((name, addr))

for kw in sorted(by_kw.keys()):
    items = by_kw[kw]
    p(f"\n  [{kw}] ({len(items)} CMSGs):")
    for name, addr in items[:10]:
        p(f"    0x{addr:08X} {name[:70]}")
    if len(items) > 10:
        p(f"    ... +{len(items)-10} more")

# ═══════════════════════════════════════════════════════════════
# 8. Certificate pinning / SSL bypass opportunities
# ═══════════════════════════════════════════════════════════════
p("\n\n### 8. SSL/Certificate Strings ###\n")
ssl_pats = [rb'SSL_CTX', rb'X509', rb'verify', rb'certificate', rb'pinning',
            rb'trust', rb'ca-cert', rb'CURLOPT_SSL', rb'peer_verify']
found_ssl = set()
for pat in ssl_pats:
    for m in re.finditer(pat, rodata, re.IGNORECASE):
        start = m.start()
        while start > 0 and rodata[start-1] != 0: start -= 1
        end = m.end()
        while end < len(rodata) and rodata[end] != 0: end += 1
        s = rodata[start:end].decode('ascii', errors='replace')
        if 5 < len(s) < 200:
            found_ssl.add(s)
for s in sorted(found_ssl)[:30]:
    p(f"  {s}")

# ═══════════════════════════════════════════════════════════════
# 9. Game config/tuning values (rates, multipliers, limits)
# ═══════════════════════════════════════════════════════════════
p("\n\n### 9. Game Config Strings ###\n")
config_pats = [rb'_rate', rb'_speed', rb'_cost', rb'_limit', rb'_max',
               rb'_bonus', rb'_buff', rb'_multiply', rb'_factor', rb'_percent',
               rb'_cooldown', rb'_interval', rb'_duration', rb'_timeout',
               rb'_capacity', rb'_count', rb'_level', rb'_tier']
found_config = set()
for pat in config_pats:
    for m in re.finditer(pat, rodata, re.IGNORECASE):
        start = m.start()
        while start > 0 and rodata[start-1] != 0: start -= 1
        end = m.end()
        while end < len(rodata) and rodata[end] != 0: end += 1
        s = rodata[start:end].decode('ascii', errors='replace')
        if 5 < len(s) < 100:
            found_config.add(s)
for s in sorted(found_config)[:60]:
    p(f"  {s}")

# ═══════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════
with open(r'D:\CascadeProjects\analysis\findings\deep_discovery.md', 'w', encoding='utf-8') as f:
    f.write("# Deep Discovery - libgame.so\n\n")
    f.write('\n'.join(out))

p(f"\n\nSaved to findings/deep_discovery.md")
p(f"Total findings: {len(urls)} URLs, {len(ips)} IPs, {len(found_debug)} debug strings,")
p(f"  {len(found_secrets)} secrets, {len(found_errors)} errors, {len(found_syms)} symbols,")
p(f"  {len(cmsg_syms)} exploitable CMSGs, {len(found_ssl)} SSL, {len(found_config)} configs")

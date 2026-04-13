"""Check libgame.so version and compare with current game version."""
import re, struct, os

BINARY = r"d:\CascadeProjects\libgame.so"
data = open(BINARY, "rb").read()
size_mb = len(data) / (1024*1024)
print(f"Binary size: {size_mb:.1f} MB ({len(data):,} bytes)")

# Check ELF header
if data[:4] == b'\x7fELF':
    bits = {1: 32, 2: 64}.get(data[4], 0)
    endian = {1: 'LE', 2: 'BE'}.get(data[5], '?')
    machine = struct.unpack('<H', data[18:20])[0] if endian == 'LE' else 0
    machines = {0x3: 'x86', 0x3E: 'x86_64', 0x28: 'ARM', 0xB7: 'AArch64'}
    print(f"ELF: {bits}-bit, {endian}, Machine: {machines.get(machine, hex(machine))}")

# Search for version-like strings near known game patterns
print("\n--- Version strings in .rodata ---")
# Look for patterns like "2.XX" or major.minor.patch near game-related context
version_patterns = [
    rb'(\d+\.\d+\.\d+[a-z]?)',  # generic version
]

# Find all readable strings that look like game versions
for m in re.finditer(rb'(?:version|Version|VERSION)[^\x00]{0,20}?(\d+\.\d+\.\d+)', data):
    ctx_start = max(0, m.start()-20)
    ctx = data[ctx_start:m.end()+10].replace(b'\x00', b'|')
    print(f"  0x{m.start():08X}: {ctx}")

# Look for build date/time strings
print("\n--- Build timestamps ---")
for m in re.finditer(rb'20[12]\d[-/][01]\d[-/][0-3]\d', data):
    ctx_start = max(0, m.start()-10)
    ctx_end = min(len(data), m.end()+30)
    ctx = data[ctx_start:ctx_end].replace(b'\x00', b'|')
    try:
        print(f"  0x{m.start():08X}: {ctx.decode('ascii', errors='replace')}")
    except:
        pass

# Look for IGG version protocol  
print("\n--- IGG/Protocol markers ---")
for pattern in [rb'igg_game_id', rb'protocol_version', rb'server_version', rb'game_id']:
    for m in re.finditer(pattern, data):
        ctx = data[m.start():m.start()+60].replace(b'\x00', b'|')
        print(f"  0x{m.start():08X}: {ctx}")

# Check for CMSG_START_MARCH_NEW and nearby opcodes
print("\n--- March-related symbols ---")
for pattern in [rb'CMSG_START_MARCH_NEW', rb'START_MARCH', rb'CMSG_START_MARCH\x00']:
    for m in re.finditer(pattern, data):
        ctx = data[m.start():m.start()+80].replace(b'\x00', b'|')
        print(f"  0x{m.start():08X}: {ctx.decode('ascii', errors='replace')}")

# Check packData function at the known address
print("\n--- packData for 0x0CE8 ---")
PACKDATA_ADDR = 0x05212294
FILE_OFFSET = PACKDATA_ADDR  # Assuming the address maps directly
# Actually need to find the offset. Check if we have section info
for m in re.finditer(rb'_ZN\d+CMSG_START_MARCH_NEW\d+packDataE', data):
    ctx = data[m.start():m.start()+80]
    print(f"  Symbol at 0x{m.start():08X}: {ctx[:60]}")

# Check for recent opcodes that might indicate version
# New features get new opcodes - check for high opcode numbers
print("\n--- Highest opcodes found ---")
opcode_pattern = rb'CMSG_[A-Z_]+\x00'
opcodes_found = []
for m in re.finditer(opcode_pattern, data):
    name = m.group().rstrip(b'\x00').decode('ascii', errors='replace')
    opcodes_found.append((m.start(), name))
print(f"  Total CMSG_ symbols: {len(opcodes_found)}")
if opcodes_found:
    # Show some from the end (likely newer)
    for off, name in opcodes_found[-10:]:
        print(f"  0x{off:08X}: {name}")

# Check the node login for version
print("\n--- Checking node login version ---")
node_login = r"d:\CascadeProjects\claude\node_login.js"
if os.path.exists(node_login):
    nl_data = open(node_login, 'r').read()
    for m in re.finditer(r'version.*?[\'"]([\d.]+)[\'"]', nl_data):
        print(f"  node_login version: {m.group(1)}")
    for m in re.finditer(r'gameVersion.*?[\'"]([\d.]+)[\'"]', nl_data):
        print(f"  node_login gameVersion: {m.group(1)}")

print("\nDone.")

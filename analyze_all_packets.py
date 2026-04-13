"""
Extract all 0x0CE* packets and analyze their msg_value + CMsgCodec metadata.
Also XOR corresponding positions across packets to check consistency.
"""
import struct

PCAP = r"d:\CascadeProjects\actions_capture.pcap"
SERVER_IP = bytes([54, 93, 192, 240])
PORT = 7000

def parse_pcap(path):
    with open(path, 'rb') as f:
        raw = f.read()
    magic = struct.unpack('<I', raw[:4])[0]
    if magic == 0xa1b2c3d4:
        endian = '<'
    else:
        endian = '>'
    off = 24
    c2s_stream = b''
    s2c_stream = b''
    while off < len(raw):
        ts_sec = struct.unpack(endian+'I', raw[off:off+4])[0]
        ts_usec = struct.unpack(endian+'I', raw[off+4:off+8])[0]
        incl_len = struct.unpack(endian+'I', raw[off+8:off+12])[0]
        off += 16
        pkt = raw[off:off+incl_len]
        off += incl_len
        if len(pkt) < 54: continue
        ip_start = 14
        proto = pkt[ip_start+9]
        if proto != 6: continue
        ihl = (pkt[ip_start] & 0xf) * 4
        tcp_start = ip_start + ihl
        src_port = struct.unpack('>H', pkt[tcp_start:tcp_start+2])[0]
        dst_port = struct.unpack('>H', pkt[tcp_start+2:tcp_start+4])[0]
        data_off = (pkt[tcp_start+12] >> 4) * 4
        payload_start = tcp_start + data_off
        tcp_payload = pkt[payload_start:]
        if len(tcp_payload) == 0: continue
        src_ip = pkt[ip_start+12:ip_start+16]
        dst_ip = pkt[ip_start+16:ip_start+20]
        if dst_ip == SERVER_IP and dst_port == PORT:
            c2s_stream += tcp_payload
        elif src_ip == SERVER_IP and src_port == PORT:
            s2c_stream += tcp_payload
    return c2s_stream, s2c_stream

def extract_packets(stream):
    pkts = []
    pos = 0
    while pos + 4 <= len(stream):
        pkt_len = struct.unpack('<H', stream[pos:pos+2])[0]
        if pkt_len < 4 or pos + pkt_len > len(stream): break
        opcode = struct.unpack('<H', stream[pos+2:pos+4])[0]
        payload = stream[pos+4:pos+pkt_len]
        pkts.append((opcode, payload))
        pos += pkt_len
    return pkts

c2s, s2c = parse_pcap(PCAP)
c2s_pkts = extract_packets(c2s)
s2c_pkts = extract_packets(s2c)

# Find all 0x0CE* packets
print("=== All 0x0CE* packets (client->server) ===")
ce_packets = []
for i, (op, pay) in enumerate(c2s_pkts):
    if 0x0CE0 <= op <= 0x0CEF:
        # CMsgCodec metadata at payload[0:4]
        # payload[0] = checksum
        # payload[1] = msg_value low
        # payload[2] = msg_value ^ 0xB7
        # payload[3] = msg_value >> 8
        if len(pay) >= 4:
            chk = pay[0]
            msg_lo = pay[1]
            msg_xor = pay[2]
            msg_hi = pay[3]
            msg_verify = msg_lo ^ 0xb7
            msg_value = msg_lo | (msg_hi << 8)
            print(f"  [{i:3d}] op=0x{op:04x} len={len(pay):3d} "
                  f"chk=0x{chk:02x} msg=0x{msg_value:04x} "
                  f"verify={'OK' if msg_xor == msg_verify else 'FAIL'} "
                  f"data={pay[:20].hex()}")
            ce_packets.append((op, pay, msg_value))

# Check if msg_value is consistent across packets
msg_values = set(mv for _,_,mv in ce_packets)
print(f"\nUnique msg_values: {[f'0x{m:04x}' for m in sorted(msg_values)]}")

# Now let's also check ALL packets for the msg pattern
print("\n=== Check msg_value pattern for ALL c2s packets ===")
msg_count = {}
for i, (op, pay) in enumerate(c2s_pkts):
    if len(pay) >= 4:
        msg_lo = pay[1]
        msg_xor = pay[2]
        if msg_lo ^ 0xb7 == msg_xor:
            msg_hi = pay[3]
            mv = msg_lo | (msg_hi << 8)
            msg_count[mv] = msg_count.get(mv, 0) + 1
print(f"msg_values with valid verify: {dict(sorted(msg_count.items()))}")

# XOR consistency test across 0x0CE8 packets
print("\n=== XOR consistency across 0x0CE8 packets ===")
ce8_packets = [(op, pay) for op, pay, mv in ce_packets if op == 0x0CE8]
if len(ce8_packets) >= 2:
    ref = ce8_packets[0][1]
    for idx, (op, pay) in enumerate(ce8_packets[1:], 1):
        maxlen = min(len(ref), len(pay))
        xor_data = bytes(a ^ b for a, b in zip(ref[:maxlen], pay[:maxlen]))
        # If encryption is same for all, XOR of two encrypted with same key = XOR of plaintexts
        print(f"  pkt0 ^ pkt{idx}: {xor_data[4:20].hex()} ...")

# Also check 0x0CEB packets
print("\n=== 0x0CEB packets ===")
ceb_packets = [(op, pay) for op, pay, mv in ce_packets if op == 0x0CEB]
for idx, (op, pay) in enumerate(ceb_packets):
    print(f"  [{idx}] {pay.hex()}")

# Try simple XOR key extraction assuming first packet's known plaintext
# For 0x0CE8: it's a gather action
# The payload after CMsgCodec decryption should be the action data
# Let's see if we can find patterns
print("\n=== Trying to find 28-byte XOR key ===")
# If encryption is simple XOR (no msg addition), key = cipher ^ plaintext
# Use the known relationship: key repeats every 28 bytes
if ce8_packets:
    pay = ce8_packets[0][1]
    print(f"First 0x0CE8 payload ({len(pay)} bytes):")
    for i in range(0, len(pay), 28):
        chunk = pay[i:i+28]
        print(f"  [{i:3d}] {chunk.hex()}")
    
    # XOR positions 4+28k for k=0,1,2... to check if they're the same
    print("\n  Position analysis (check if cipher[i] ^ cipher[i+28] == plaintext[i] ^ plaintext[i+28]):")
    for pos in range(4, min(28, len(pay)-28)):
        vals = []
        for k in range(len(pay) // 28 + 1):
            p = pos + k * 28
            if p < len(pay):
                vals.append(pay[p])
        if len(vals) >= 2:
            xors = [vals[j] ^ vals[j+1] for j in range(len(vals)-1)]
            print(f"    pos={pos:2d}: bytes={[f'0x{v:02x}' for v in vals]} xors={[f'0x{x:02x}' for x in xors]}")

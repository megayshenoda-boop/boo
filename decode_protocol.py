"""
Decode the captured IGG Conquerors protocol packets in detail.
Outputs a comprehensive findings document.
"""
import struct, os

PCAP_FILE = r"d:\CascadeProjects\capture.pcap"
OUTPUT_FILE = r"d:\CascadeProjects\protocol_findings.txt"

def parse_pcap(pcap_path):
    with open(pcap_path, 'rb') as f:
        ghdr = f.read(24)
        magic = struct.unpack('<I', ghdr[0:4])[0]
        endian = '<' if magic == 0xa1b2c3d4 else '>'
        link_type = struct.unpack(endian + 'I', ghdr[20:24])[0]
        packets = []
        pkt_num = 0
        while True:
            phdr = f.read(16)
            if len(phdr) < 16: break
            ts_sec, ts_usec, cap_len, orig_len = struct.unpack(endian + 'IIII', phdr)
            pkt_data = f.read(cap_len)
            if len(pkt_data) < cap_len: break
            pkt_num += 1
            offset = 0
            if link_type == 101: offset = 0
            elif link_type == 1: offset = 14
            elif link_type == 113: offset = 16
            if offset + 20 > len(pkt_data): continue
            ip_ver = (pkt_data[offset] >> 4) & 0xf
            if ip_ver != 4: continue
            ip_hdr_len = (pkt_data[offset] & 0xf) * 4
            ip_proto = pkt_data[offset + 9]
            if ip_proto != 6: continue
            src_ip = '.'.join(str(b) for b in pkt_data[offset+12:offset+16])
            dst_ip = '.'.join(str(b) for b in pkt_data[offset+16:offset+20])
            tcp_off = offset + ip_hdr_len
            if tcp_off + 20 > len(pkt_data): continue
            src_port = struct.unpack('>H', pkt_data[tcp_off:tcp_off+2])[0]
            dst_port = struct.unpack('>H', pkt_data[tcp_off+2:tcp_off+4])[0]
            tcp_hdr_len = ((pkt_data[tcp_off+12] >> 4) & 0xf) * 4
            payload = pkt_data[tcp_off + tcp_hdr_len:]
            if len(payload) == 0: continue
            packets.append({
                'num': pkt_num, 'ts': ts_sec + ts_usec/1e6,
                'src_ip': src_ip, 'src_port': src_port,
                'dst_ip': dst_ip, 'dst_port': dst_port,
                'payload': payload
            })
    return packets

def hex_dump(data, max_bytes=128):
    h = data[:max_bytes].hex()
    if len(data) > max_bytes:
        h += f"... ({len(data)}B total)"
    return h

def safe_ascii(data):
    return ''.join(chr(b) if 32 <= b < 127 else '.' for b in data)

def main():
    packets = parse_pcap(PCAP_FILE)
    
    # Separate IGG traffic
    gateway_ip = "54.93.167.80"
    gateway_port = 5997
    game_ip = "54.93.192.240"
    game_port = 7000
    
    gateway_pkts = [p for p in packets if 
        (p['dst_ip'] == gateway_ip and p['dst_port'] == gateway_port) or
        (p['src_ip'] == gateway_ip and p['src_port'] == gateway_port)]
    
    game_pkts = [p for p in packets if 
        (p['dst_ip'] == game_ip and p['dst_port'] == game_port) or
        (p['src_ip'] == game_ip and p['src_port'] == game_port)]
    
    out = []
    def w(s=""): out.append(s)
    
    w("=" * 80)
    w("IGG CONQUERORS (الفاتحون العصر الذهبي) - PROTOCOL ANALYSIS")
    w("Package: com.igg.android.conquerors")
    w(f"Capture: {os.path.basename(PCAP_FILE)} ({os.path.getsize(PCAP_FILE)} bytes)")
    w(f"Total TCP packets with payload: {len(packets)}")
    w("=" * 80)
    
    # =========================================================
    # PHASE 1: GATEWAY AUTH
    # =========================================================
    w()
    w("=" * 80)
    w("PHASE 1: GATEWAY AUTHENTICATION")
    w(f"Gateway: {gateway_ip}:{gateway_port}")
    w(f"Packets: {len(gateway_pkts)}")
    w("=" * 80)
    
    for p in gateway_pkts:
        d = p['payload']
        direction = "CLIENT -> GATEWAY" if p['dst_ip'] == gateway_ip else "GATEWAY -> CLIENT"
        op = struct.unpack('<H', d[2:4])[0] if len(d) >= 4 else -1
        pkt_len = struct.unpack('<H', d[0:2])[0] if len(d) >= 2 else len(d)
        
        w()
        w(f"--- Packet #{p['num']} [{direction}] ---")
        w(f"Opcode: 0x{op:04X}  Length: {pkt_len}B  Raw size: {len(d)}B")
        w(f"Hex: {d.hex()}")
        
        if op == 0x000B:
            w()
            w("  [0x000B] AUTH REQUEST (Client -> Gateway)")
            w(f"  Bytes 0-1:   {d[0:2].hex()} = Length: {pkt_len}")
            w(f"  Bytes 2-3:   {d[2:4].hex()} = Opcode: 0x000B")
            version = struct.unpack('<I', d[4:8])[0]
            w(f"  Bytes 4-7:   {d[4:8].hex()} = Version: {version}")
            w(f"  Bytes 8-11:  {d[8:12].hex()} = Padding/zeros")
            igg_id = struct.unpack('<I', d[12:16])[0]
            w(f"  Bytes 12-15: {d[12:16].hex()} = IGG ID: {igg_id}")
            w(f"  Bytes 16-19: {d[16:20].hex()} = Padding/zeros")
            token_len = struct.unpack('<H', d[20:22])[0]
            w(f"  Bytes 20-21: {d[20:22].hex()} = Token length: {token_len}")
            token = d[22:22+token_len]
            w(f"  Bytes 22-{22+token_len-1}: Token ({token_len}B): {token.hex()}")
            pos = 22 + token_len
            remaining = d[pos:]
            w(f"  Bytes {pos}-end: Remaining ({len(remaining)}B): {remaining.hex()}")
            # Try to decode remaining
            if len(remaining) >= 4:
                w(f"    Possible fields in remaining:")
                i = 0
                while i + 4 <= len(remaining):
                    val = struct.unpack('<I', remaining[i:i+4])[0]
                    w(f"    [{i}:{i+4}] = {remaining[i:i+4].hex()} = {val} (0x{val:08X})")
                    i += 4
                if i < len(remaining):
                    w(f"    [{i}:end] = {remaining[i:].hex()}")
        
        elif op == 0x000C:
            w()
            w("  [0x000C] AUTH RESPONSE (Gateway -> Client)")
            w(f"  Bytes 0-1:   {d[0:2].hex()} = Length: {pkt_len}")
            w(f"  Bytes 2-3:   {d[2:4].hex()} = Opcode: 0x000C")
            igg_id = struct.unpack('<I', d[4:8])[0]
            w(f"  Bytes 4-7:   {d[4:8].hex()} = IGG ID: {igg_id}")
            w(f"  Bytes 8-11:  {d[8:12].hex()} = Padding/zeros")
            
            pos = 12
            ip_len = struct.unpack('<H', d[pos:pos+2])[0]
            w(f"  Bytes {pos}-{pos+1}: {d[pos:pos+2].hex()} = IP string length: {ip_len}")
            pos += 2
            redirect_ip = d[pos:pos+ip_len].decode('ascii', errors='replace')
            w(f"  Bytes {pos}-{pos+ip_len-1}: {d[pos:pos+ip_len].hex()} = Redirect IP: \"{redirect_ip}\"")
            pos += ip_len
            
            redirect_port = struct.unpack('<H', d[pos:pos+2])[0]
            w(f"  Bytes {pos}-{pos+1}: {d[pos:pos+2].hex()} = Redirect Port: {redirect_port}")
            pos += 2
            
            token_len = struct.unpack('<H', d[pos:pos+2])[0]
            w(f"  Bytes {pos}-{pos+1}: {d[pos:pos+2].hex()} = Token length: {token_len}")
            pos += 2
            
            token = d[pos:pos+token_len]
            token_ascii = token.decode('ascii', errors='replace')
            w(f"  Bytes {pos}-{pos+token_len-1}: Token: \"{token_ascii}\"")
            w(f"  Token hex: {token.hex()}")
            pos += token_len
            
            remaining = d[pos:]
            w(f"  Bytes {pos}-end: Remaining ({len(remaining)}B): {remaining.hex()}")
            if len(remaining) >= 1:
                w(f"    Byte {pos}: {remaining[0]:02x} = {remaining[0]}")
            if len(remaining) >= 5:
                world_id = struct.unpack('<I', remaining[1:5])[0]
                w(f"    Bytes {pos+1}-{pos+4}: {remaining[1:5].hex()} = World ID: {world_id}")
            
            w()
            w(f"  >>> REDIRECT: {redirect_ip}:{redirect_port}")
            w(f"  >>> TOKEN: {token_ascii}")
            w(f"  >>> WORLD: {world_id if len(remaining) >= 5 else '?'}")
    
    # =========================================================
    # PHASE 2: GAME SERVER
    # =========================================================
    w()
    w("=" * 80)
    w("PHASE 2: GAME SERVER COMMUNICATION")
    w(f"Game Server: {game_ip}:{game_port}")
    w(f"Packets: {len(game_pkts)}")
    w("=" * 80)
    
    # Decode first few critical packets in detail
    for i, p in enumerate(game_pkts[:10]):
        d = p['payload']
        direction = "CLIENT -> SERVER" if p['dst_ip'] == game_ip else "SERVER -> CLIENT"
        
        # IGG packets can be concatenated; parse the first one
        if len(d) < 4: continue
        pkt_len = struct.unpack('<H', d[0:2])[0]
        op = struct.unpack('<H', d[2:4])[0]
        
        w()
        w(f"--- Game Packet #{i+1} (pkt#{p['num']}) [{direction}] ---")
        w(f"Opcode: 0x{op:04X}  Declared length: {pkt_len}B  Raw size: {len(d)}B")
        w(f"Hex: {hex_dump(d, 200)}")
        w(f"ASCII: {safe_ascii(d[:80])}")
        
        if op == 0x001F:
            w()
            w("  [0x001F] GAME SERVER LOGIN (Client -> Game Server)")
            w(f"  Bytes 0-1:   Length: {pkt_len}")
            w(f"  Bytes 2-3:   Opcode: 0x001F")
            version = struct.unpack('<I', d[4:8])[0]
            w(f"  Bytes 4-7:   {d[4:8].hex()} = Version: {version}")
            w(f"  Bytes 8-11:  {d[8:12].hex()} = Padding")
            igg_id = struct.unpack('<I', d[12:16])[0]
            w(f"  Bytes 12-15: {d[12:16].hex()} = IGG ID: {igg_id}")
            w(f"  Bytes 16-19: {d[16:20].hex()} = Padding")
            tok_len = struct.unpack('<H', d[20:22])[0]
            w(f"  Bytes 20-21: {d[20:22].hex()} = Token length: {tok_len}")
            token = d[22:22+tok_len]
            w(f"  Bytes 22-{22+tok_len-1}: Token: \"{token.decode('ascii', errors='replace')}\"")
            pos2 = 22 + tok_len
            remaining = d[pos2:]
            w(f"  Bytes {pos2}-end: Tail ({len(remaining)}B): {remaining.hex()}")
        
        elif op == 0x0020:
            w()
            w("  [0x0020] GAME SERVER LOGIN RESPONSE")
            w(f"  Full: {d.hex()}")
            if len(d) >= 5:
                status = d[4]
                w(f"  Byte 4: Status = {status} ({'OK' if status == 1 else 'FAIL'})")
        
        elif op == 0x0021:
            w()
            w("  [0x0021] WORLD ENTRY / SESSION INIT")
            w(f"  Bytes 0-1: Length: {pkt_len}")
            w(f"  Bytes 2-3: Opcode: 0x0021")
            if len(d) >= 8:
                igg_id = struct.unpack('<I', d[4:8])[0]
                w(f"  Bytes 4-7: {d[4:8].hex()} = IGG ID: {igg_id}")
            remaining = d[8:]
            w(f"  Bytes 8-end: {remaining.hex()}")
    
    # =========================================================
    # OPCODE SUMMARY
    # =========================================================
    w()
    w("=" * 80)
    w("OPCODE SUMMARY (ALL GAME SERVER PACKETS)")
    w("=" * 80)
    
    opcodes_out = {}
    opcodes_in = {}
    
    for p in game_pkts:
        d = p['payload']
        if len(d) < 4: continue
        
        # Handle concatenated packets
        pos = 0
        while pos + 4 <= len(d):
            pkt_len = struct.unpack('<H', d[pos:pos+2])[0]
            if pkt_len < 4 or pkt_len > 65000: break
            op = struct.unpack('<H', d[pos+2:pos+4])[0]
            
            is_out = p['dst_ip'] == game_ip
            target = opcodes_out if is_out else opcodes_in
            
            if op not in target:
                target[op] = {'count': 0, 'sizes': [], 'first_hex': ''}
            target[op]['count'] += 1
            target[op]['sizes'].append(pkt_len)
            if not target[op]['first_hex']:
                end = min(pos + pkt_len, len(d))
                target[op]['first_hex'] = d[pos:end].hex()[:160]
            
            if pkt_len <= len(d) - pos:
                pos += pkt_len
            else:
                break
    
    w()
    w("CLIENT -> SERVER opcodes:")
    for op in sorted(opcodes_out.keys()):
        info = opcodes_out[op]
        sizes = info['sizes']
        w(f"  0x{op:04X}: {info['count']}x, sizes={sizes}")
        w(f"    first: {info['first_hex'][:120]}")
    
    w()
    w("SERVER -> CLIENT opcodes:")
    for op in sorted(opcodes_in.keys()):
        info = opcodes_in[op]
        sizes = info['sizes']
        w(f"  0x{op:04X}: {info['count']}x, sizes={[s for s in sizes[:5]]}{'...' if len(sizes) > 5 else ''}")
        w(f"    first: {info['first_hex'][:120]}")
    
    # =========================================================
    # KEY FINDINGS
    # =========================================================
    w()
    w("=" * 80)
    w("KEY FINDINGS FOR BOT DEVELOPMENT")
    w("=" * 80)
    w()
    w("1. CONNECTION FLOW:")
    w("   Step 1: Connect TCP to Gateway 54.93.167.80:5997")
    w("   Step 2: Send 0x000B with IGG ID + 32-byte auth token")
    w("   Step 3: Receive 0x000C with redirect IP:port + session token")
    w("   Step 4: Connect TCP to Game Server (from 0x000C redirect)")
    w("   Step 5: Send 0x001F with IGG ID + session token (from 0x000C)")
    w("   Step 6: Receive 0x0020 (login accepted)")
    w("   Step 7: Send 0x0021 (world entry)")
    w("   Step 8: Receive game data flood")
    w()
    w("2. PACKET FORMAT:")
    w("   [2 bytes LE] total packet length (includes these 2 bytes)")
    w("   [2 bytes LE] opcode")
    w("   [variable]   payload")
    w()
    w("3. CAPTURED VALUES:")
    
    # Extract from gateway packets
    for p in gateway_pkts:
        d = p['payload']
        op = struct.unpack('<H', d[2:4])[0] if len(d) >= 4 else -1
        if op == 0x000B:
            igg_id = struct.unpack('<I', d[12:16])[0]
            token = d[22:54]
            w(f"   IGG ID: {igg_id}")
            w(f"   0x000B Token (32B): {token.hex()}")
        elif op == 0x000C:
            pos = 12
            ip_len = struct.unpack('<H', d[pos:pos+2])[0]
            pos += 2
            redirect_ip = d[pos:pos+ip_len].decode('ascii')
            pos += ip_len
            redirect_port = struct.unpack('<H', d[pos:pos+2])[0]
            pos += 2
            tok_len = struct.unpack('<H', d[pos:pos+2])[0]
            pos += 2
            session_token = d[pos:pos+tok_len].decode('ascii')
            pos += tok_len
            w(f"   Redirect: {redirect_ip}:{redirect_port}")
            w(f"   Session Token: {session_token}")
            if len(d) > pos + 4:
                world = struct.unpack('<I', d[pos+1:pos+5])[0]
                w(f"   World ID: {world}")
    
    # Write output
    text = '\n'.join(out)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(text)
    print(f"\n\nSaved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

"""
IGG Conquerors (الفاتحون العصر الذهبي) - Complete Bot
Gateway Auth -> Game Server Connection -> Game Data

Token formula: XOR(access_key, "CQ_secret" repeating)

Usage:
  python full_bot.py                    # Use stored access key
  python full_bot.py --adb              # Extract access key from device via ADB
  python full_bot.py --key <access_key> # Use provided access key
"""
import socket
import struct
import time
import subprocess
import re
import sys

# ==================== CONFIG ====================
IGG_ID = 2082384585
GAME_ID = "1057029902"
GATEWAY_IP = "54.93.167.80"
GATEWAY_PORT = 5997
WORLD_ID = 211
CQ_XOR_KEY = ("CQ_secret" * 4)[:32]  # "CQ_secretCQ_secretCQ_secretCQ_se"
GAME_ID_HEX = 0x3F00FF0E

# Stored access key from device (extracted from weg_login_file.xml)
STORED_ACCESS_KEY = "9f4675b1b1d1b9fd0a3db5145018469e"

# ADB path for MEmu emulator
ADB_PATH = r"D:\Program Files\Microvirt\MEmu\adb.exe"
ADB_DEVICE = "127.0.0.1:21503"

# ==================== ACCESS KEY EXTRACTION ====================
def extract_access_key_from_device():
    """Extract weg_Accesskey from device via ADB"""
    print("[ADB] Extracting access key from device...")
    try:
        cmd = [ADB_PATH, "-s", ADB_DEVICE, "shell",
               "cat /data/data/com.igg.android.conquerors/shared_prefs/weg_login_file.xml"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        match = re.search(r'weg_Accesskey">(.*?)<', result.stdout)
        if match:
            key = match.group(1)
            print(f"  Extracted: {key}")
            return key
    except Exception as e:
        print(f"  ADB extraction failed: {e}")
    return None

# ==================== TOKEN DERIVATION ====================
def derive_gateway_token(access_key):
    """Derive 0x000B token: XOR(access_key, "CQ_secret" repeating)"""
    xor_key = CQ_XOR_KEY.encode('ascii')
    key_bytes = access_key.encode('ascii')
    token = bytes(a ^ b for a, b in zip(key_bytes, xor_key))
    return token

# ==================== PACKET BUILDERS ====================
def build_000B(igg_id, token, world_id, game_id_hex=0x3F00FF0E):
    """Build 0x000B Gateway Auth packet (79 bytes)"""
    pkt = struct.pack('<H', 79)                # length
    pkt += struct.pack('<H', 0x000B)           # opcode
    pkt += struct.pack('<I', 1)                # version
    pkt += struct.pack('<I', 0)                # padding
    pkt += struct.pack('<I', igg_id)           # IGG ID
    pkt += struct.pack('<I', 0)                # padding
    pkt += struct.pack('<H', 32)               # token length
    pkt += token                                # 32-byte token
    pkt += struct.pack('<I', 0)                # padding
    pkt += struct.pack('<I', 2)                # platform (2=android)
    pkt += struct.pack('<I', 0)                # padding
    pkt += struct.pack('<I', world_id)         # world ID
    pkt += struct.pack('<I', game_id_hex)      # game ID hex
    pkt += struct.pack('<I', 0)                # padding
    pkt += struct.pack('B', 1)                 # tail byte
    assert len(pkt) == 79, f"0x000B packet size mismatch: {len(pkt)}"
    return pkt

def build_001F(igg_id, session_token, game_id_hex=0x3F00FF0E):
    """Build 0x001F Game Server Login packet (64 bytes)"""
    token_bytes = session_token.encode('ascii')
    pkt = struct.pack('<H', 64)                # length
    pkt += struct.pack('<H', 0x001F)           # opcode
    pkt += struct.pack('<I', 1)                # version
    pkt += struct.pack('<I', 0)                # padding
    pkt += struct.pack('<I', igg_id)           # IGG ID
    pkt += struct.pack('<I', 0)                # padding
    pkt += struct.pack('<H', 32)               # token length
    pkt += token_bytes                          # 32 ASCII session token
    # Tail bytes from captured packet: 0e 0e ff 00 3f 00 00 00 00 00
    pkt += bytes([0x0e])
    pkt += struct.pack('<I', game_id_hex)
    pkt += struct.pack('<I', 0)
    pkt += bytes([0x00])
    assert len(pkt) == 64, f"0x001F packet size mismatch: {len(pkt)}"
    return pkt

def build_0021(igg_id, game_id_hex=0x3F00FF0E):
    """Build 0x0021 World Entry packet (21 bytes)"""
    pkt = struct.pack('<H', 21)                # length
    pkt += struct.pack('<H', 0x0021)           # opcode
    pkt += struct.pack('<I', igg_id)           # IGG ID
    pkt += struct.pack('<I', 0)                # padding
    pkt += bytes([0x0e])
    pkt += struct.pack('<I', game_id_hex)
    # Tail from capture: b0 02 5c 00
    pkt += bytes([0xb0, 0x02, 0x5c, 0x00])
    # Pad to 21 bytes - check
    # So far: 2+2+4+4+1+4+4 = 21 ✓
    assert len(pkt) == 21, f"0x0021 packet size mismatch: {len(pkt)}"
    return pkt

# ==================== PACKET PARSING ====================
def parse_000C(data):
    """Parse 0x000C Gateway Auth Response"""
    if len(data) < 14:
        raise Exception(f"0x000C too short: {len(data)}")
    
    pkt_len = struct.unpack('<H', data[0:2])[0]
    opcode = struct.unpack('<H', data[2:4])[0]
    
    if opcode != 0x000C:
        raise Exception(f"Expected 0x000C, got 0x{opcode:04X}")
    
    igg_id = struct.unpack('<I', data[4:8])[0]
    # padding at 8-11
    pos = 12
    ip_len = struct.unpack('<H', data[pos:pos+2])[0]
    pos += 2
    redirect_ip = data[pos:pos+ip_len].decode('ascii')
    pos += ip_len
    redirect_port = struct.unpack('<H', data[pos:pos+2])[0]
    pos += 2
    tok_len = struct.unpack('<H', data[pos:pos+2])[0]
    pos += 2
    session_token = data[pos:pos+tok_len].decode('ascii')
    pos += tok_len
    
    # status byte + world_id
    status = data[pos] if pos < len(data) else None
    world_id = struct.unpack('<I', data[pos+1:pos+5])[0] if pos+5 <= len(data) else None
    
    return {
        'igg_id': igg_id,
        'redirect_ip': redirect_ip,
        'redirect_port': redirect_port,
        'session_token': session_token,
        'status': status,
        'world_id': world_id
    }

def parse_0020(data):
    """Parse 0x0020 Game Server Login Response"""
    if len(data) < 5:
        raise Exception(f"0x0020 too short: {len(data)}")
    opcode = struct.unpack('<H', data[2:4])[0]
    if opcode != 0x0020:
        raise Exception(f"Expected 0x0020, got 0x{opcode:04X}")
    status = data[4]
    return status

# ==================== TCP COMMUNICATION ====================
def tcp_recv(sock, timeout=10):
    """Receive data from TCP socket with timeout"""
    sock.settimeout(timeout)
    chunks = []
    try:
        while True:
            chunk = sock.recv(8192)
            if not chunk:
                break
            chunks.append(chunk)
            # Check if we have a complete packet
            data = b''.join(chunks)
            if len(data) >= 2:
                expected_len = struct.unpack('<H', data[0:2])[0]
                if len(data) >= expected_len:
                    break
    except socket.timeout:
        pass
    return b''.join(chunks)

def tcp_recv_all(sock, timeout=5):
    """Receive all available data with timeout"""
    sock.settimeout(timeout)
    chunks = []
    try:
        while True:
            chunk = sock.recv(65536)
            if not chunk:
                break
            chunks.append(chunk)
    except socket.timeout:
        pass
    return b''.join(chunks)

# ==================== MAIN BOT ====================
def main():
    print("=" * 60)
    print("IGG Conquerors Bot - Full Connection Flow")
    print("=" * 60)
    
    # ===== PHASE 1: HTTP LOGIN =====
    print("\n--- PHASE 1: HTTP LOGIN ---")
    
    udid = str(uuid.uuid4())
    uiid = str(uuid.uuid4())
    
    try:
        phpsessid = step1_get_phpsessid()
        sso_token = step2_login_igg(EMAIL, PASSWORD, phpsessid)
        access_token = step3_get_access_token(sso_token, udid)
    except Exception as e:
        print(f"\nHTTP LOGIN FAILED: {e}")
        return False
    
    print(f"\n  HTTP Login SUCCESS!")
    print(f"  Access Token: {access_token}")
    
    # ===== PHASE 2: GATEWAY AUTH =====
    print("\n--- PHASE 2: GATEWAY AUTH ---")
    
    # Derive token
    gateway_token = derive_gateway_token(access_token)
    print(f"  Gateway token: {gateway_token.hex()}")
    
    # Build 0x000B packet
    pkt_000B = build_000B(IGG_ID, gateway_token, WORLD_ID)
    print(f"  0x000B packet ({len(pkt_000B)}B): {pkt_000B.hex()}")
    
    # Connect to gateway
    print(f"\n  Connecting to Gateway {GATEWAY_IP}:{GATEWAY_PORT}...")
    gw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    gw_sock.settimeout(10)
    try:
        gw_sock.connect((GATEWAY_IP, GATEWAY_PORT))
        print(f"  Connected!")
    except Exception as e:
        print(f"  Gateway connection failed: {e}")
        return False
    
    # Send 0x000B
    print(f"  Sending 0x000B...")
    gw_sock.sendall(pkt_000B)
    
    # Receive 0x000C
    print(f"  Waiting for 0x000C response...")
    resp = tcp_recv(gw_sock, timeout=10)
    if not resp:
        print(f"  No response from gateway!")
        gw_sock.close()
        return False
    
    print(f"  Response ({len(resp)}B): {resp.hex()}")
    
    try:
        auth_result = parse_000C(resp)
    except Exception as e:
        print(f"  Failed to parse 0x000C: {e}")
        # Check if we got a rejection (channel 3)
        if len(resp) >= 5:
            opcode = struct.unpack('<H', resp[2:4])[0]
            if opcode == 0x000C:
                channel = resp[4] if len(resp) > 4 else -1
                print(f"  Opcode: 0x{opcode:04X}, first data byte: {channel}")
        gw_sock.close()
        return False
    
    gw_sock.close()
    
    print(f"\n  0x000C AUTH RESPONSE:")
    print(f"    Redirect: {auth_result['redirect_ip']}:{auth_result['redirect_port']}")
    print(f"    Session Token: {auth_result['session_token']}")
    print(f"    World ID: {auth_result['world_id']}")
    print(f"    Status: {auth_result['status']}")
    
    # ===== PHASE 3: GAME SERVER =====
    print("\n--- PHASE 3: GAME SERVER ---")
    
    game_ip = auth_result['redirect_ip']
    game_port = auth_result['redirect_port']
    session_token = auth_result['session_token']
    
    # Build 0x001F
    pkt_001F = build_001F(IGG_ID, session_token)
    print(f"  0x001F packet ({len(pkt_001F)}B): {pkt_001F.hex()}")
    
    # Connect to game server
    print(f"\n  Connecting to Game Server {game_ip}:{game_port}...")
    gs_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    gs_sock.settimeout(10)
    try:
        gs_sock.connect((game_ip, game_port))
        print(f"  Connected!")
    except Exception as e:
        print(f"  Game server connection failed: {e}")
        return False
    
    # Send 0x001F
    print(f"  Sending 0x001F (login)...")
    gs_sock.sendall(pkt_001F)
    
    # Receive 0x0020
    print(f"  Waiting for 0x0020 response...")
    resp = tcp_recv(gs_sock, timeout=10)
    if not resp:
        print(f"  No response from game server!")
        gs_sock.close()
        return False
    
    print(f"  Response ({len(resp)}B): {resp.hex()}")
    
    try:
        status = parse_0020(resp)
        print(f"  Login status: {status} ({'OK' if status == 1 else 'FAIL'})")
    except Exception as e:
        print(f"  Parse error: {e}")
        gs_sock.close()
        return False
    
    if status != 1:
        print(f"  Game server login REJECTED!")
        gs_sock.close()
        return False
    
    # Send 0x0021 (world entry)
    pkt_0021 = build_0021(IGG_ID)
    print(f"\n  Sending 0x0021 (world entry)...")
    print(f"  0x0021 packet ({len(pkt_0021)}B): {pkt_0021.hex()}")
    gs_sock.sendall(pkt_0021)
    
    # Receive game data
    print(f"  Waiting for game data...")
    game_data = tcp_recv_all(gs_sock, timeout=8)
    
    if game_data:
        print(f"\n  RECEIVED {len(game_data)} bytes of game data!")
        
        # Parse first few packets
        pos = 0
        pkt_count = 0
        while pos + 4 <= len(game_data) and pkt_count < 20:
            pkt_len = struct.unpack('<H', game_data[pos:pos+2])[0]
            opcode = struct.unpack('<H', game_data[pos+2:pos+4])[0]
            if pkt_len < 4 or pkt_len > 65000:
                break
            print(f"    Packet {pkt_count+1}: opcode=0x{opcode:04X} len={pkt_len}B")
            pkt_count += 1
            if pkt_len <= len(game_data) - pos:
                pos += pkt_len
            else:
                break
        
        if pkt_count > 0:
            print(f"\n  Total packets parsed: {pkt_count}")
    else:
        print(f"  No game data received")
    
    gs_sock.close()
    
    # ===== SUCCESS =====
    print("\n" + "=" * 60)
    print("BOT CONNECTION SUCCESSFUL!")
    print("=" * 60)
    print(f"  IGG ID:         {IGG_ID}")
    print(f"  Access Token:   {access_token}")
    print(f"  Gateway Token:  {gateway_token.hex()}")
    print(f"  Game Server:    {game_ip}:{game_port}")
    print(f"  Session Token:  {session_token}")
    print(f"  World ID:       {auth_result['world_id']}")
    print(f"  Game Data:      {len(game_data)} bytes")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

"""
IGG Conquerors - Persistent Bot with Keepalive
Connects to Gateway → Game Server → Stays connected with heartbeat

Usage:
  python persistent_bot.py                     # Use stored key
  python persistent_bot.py --adb               # Extract key from device
  python persistent_bot.py --key <access_key>  # Provide key manually
"""
import socket
import struct
import time
import threading
import subprocess
import re
import sys
import os
import json
from datetime import datetime

# ==================== CONFIG ====================
IGG_ID = 2082384585
GATEWAY_IP = "54.93.167.80"
GATEWAY_PORT = 5997
WORLD_ID = 211
GAME_ID_HEX = 0x3F00FF0E
CQ_XOR_KEY = ("CQ_secret" * 4)[:32]
HEARTBEAT_INTERVAL = 15.0  # seconds
STORED_ACCESS_KEY = "9f4675b1b1d1b9fd0a3db5145018469e"
ADB_PATH = r"D:\Program Files\Microvirt\MEmu\adb.exe"
ADB_DEVICE = "127.0.0.1:21503"

# ==================== OPCODE NAMES ====================
OPCODES = {
    # Client → Server
    0x000B: "GW_AUTH_REQ",
    0x001F: "GS_LOGIN_REQ",
    0x0020: "GS_LOGIN_RESP",
    0x0021: "WORLD_ENTRY",
    0x0042: "HEARTBEAT",
    0x0043: "MAP_PING",
    0x0674: "REQ_GUILD_INFO",
    0x0709: "REQ_MAIL_LIST",
    0x0767: "REQ_CHAT_ROOMS",
    0x0840: "REQ_INVENTORY",
    0x099D: "STATUS_QUERY",
    0x0CEB: "UNKNOWN_0CEB",
    0x1839: "REQ_EVENT_DATA",
    0x17D4: "REQ_SHOP_DATA",
    0x1C87: "CHAT_SEND",
    # Server → Client
    0x000C: "GW_AUTH_RESP",
    0x0034: "PLAYER_PROFILE",
    0x004A: "WORLD_RESOURCES",
    0x0064: "BUILDING_LIST",
    0x0076: "CHAT_HISTORY",
    0x0085: "ALLIANCE_MEMBERS",
    0x0097: "ALLIANCE_INFO",
    0x00AA: "BUILDING_QUEUE",
    0x036C: "SERVER_TICK",
    0x039B: "INIT_TIMESTAMP",
    0x0636: "MARCH_DATA_JSON",
    0x0640: "BATTLE_REPORT_JSON",
    0x0654: "GUILD_TECH",
    0x0675: "GUILD_DETAIL",
    0x070A: "MAIL_LIST_RESP",
    0x076A: "CHAT_ROOMS_RESP",
    0x0841: "INVENTORY_RESP",
    0x099E: "STATUS_RESP",
    0x0A00: "RESOURCE_TIMERS",
    0x0A02: "TECH_TREE",
    0x0A0A: "TROOP_DATA",
    0x0A0B: "HERO_DATA",
    0x0C4E: "QUEST_DATA",
    0x0F0A: "EVENT_NOTIFY",
    0x0F0E: "EVENT_DATA",
    0x07E4: "VIP_DATA",
    0x083F: "ITEM_DATA",
    0x084E: "EQUIPMENT_DATA",
    0x1519: "WAR_RALLY_DATA",
    0x157C: "MARCH_QUEUE",
    0x183A: "EVENT_DATA_RESP",
    0x1C88: "CHAT_SEND_RESP",
    0x01D4: "UNKNOWN_01D4",
    0x02F2: "KINGDOM_DATA",
    0x0282: "RESEARCH_QUEUE",
    0x015E: "TRAINING_QUEUE",
}

# ==================== LOGGING ====================
LOG_FILE = None

def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    line = f"[{ts}] [{level}] {msg}"
    print(line)
    if LOG_FILE:
        LOG_FILE.write(line + "\n")
        LOG_FILE.flush()

def opname(opcode):
    return OPCODES.get(opcode, f"UNK_{opcode:04X}")

# ==================== KEY EXTRACTION ====================
def extract_key_from_device():
    log("Extracting access key from device via ADB...")
    try:
        cmd = [ADB_PATH, "-s", ADB_DEVICE, "shell",
               "cat /data/data/com.igg.android.conquerors/shared_prefs/weg_login_file.xml"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        match = re.search(r'weg_Accesskey">(.*?)<', result.stdout)
        if match:
            key = match.group(1)
            log(f"Extracted key: {key}")
            return key
    except Exception as e:
        log(f"ADB extraction failed: {e}", "ERROR")
    return None

# ==================== TOKEN ====================
def derive_token(access_key):
    xor_key = CQ_XOR_KEY.encode('ascii')
    return bytes(a ^ b for a, b in zip(access_key.encode('ascii'), xor_key))

# ==================== PACKET IO ====================
def build_packet(opcode, payload=b''):
    length = 4 + len(payload)
    return struct.pack('<HH', length, opcode) + payload

def recv_packet(sock, timeout=10):
    """Receive one complete packet. Returns (opcode, payload, raw) or None."""
    sock.settimeout(timeout)
    try:
        header = b''
        while len(header) < 4:
            chunk = sock.recv(4 - len(header))
            if not chunk:
                return None
            header += chunk
        
        pkt_len, opcode = struct.unpack('<HH', header)
        payload_len = pkt_len - 4
        
        if payload_len < 0 or payload_len > 100000:
            log(f"Invalid packet length: {pkt_len}", "ERROR")
            return None
        
        payload = b''
        while len(payload) < payload_len:
            chunk = sock.recv(payload_len - len(payload))
            if not chunk:
                return None
            payload += chunk
        
        return (opcode, payload, header + payload)
    except socket.timeout:
        return None
    except Exception as e:
        log(f"recv error: {e}", "ERROR")
        return None

def recv_all_packets(sock, timeout=5):
    """Receive all available packets until timeout."""
    packets = []
    deadline = time.time() + timeout
    while time.time() < deadline:
        remaining = max(0.1, deadline - time.time())
        pkt = recv_packet(sock, timeout=remaining)
        if pkt is None:
            break
        packets.append(pkt)
    return packets

# ==================== PACKET BUILDERS ====================
def build_000B(igg_id, token, world_id):
    pkt = struct.pack('<HH', 79, 0x000B)
    pkt += struct.pack('<I', 1)          # version
    pkt += struct.pack('<I', 0)
    pkt += struct.pack('<I', igg_id)
    pkt += struct.pack('<I', 0)
    pkt += struct.pack('<H', 32)
    pkt += token
    pkt += struct.pack('<I', 0)
    pkt += struct.pack('<I', 2)          # platform=android
    pkt += struct.pack('<I', 0)
    pkt += struct.pack('<I', world_id)
    pkt += struct.pack('<I', GAME_ID_HEX)
    pkt += struct.pack('<I', 0)
    pkt += struct.pack('B', 1)
    return pkt

def build_001F(igg_id, session_token):
    st = session_token.encode('ascii')
    pkt = struct.pack('<HH', 64, 0x001F)
    pkt += struct.pack('<I', 1)
    pkt += struct.pack('<I', 0)
    pkt += struct.pack('<I', igg_id)
    pkt += struct.pack('<I', 0)
    pkt += struct.pack('<H', 32)
    pkt += st
    pkt += bytes([0x0e])
    pkt += struct.pack('<I', GAME_ID_HEX)
    pkt += struct.pack('<I', 0)
    pkt += bytes([0x00])
    return pkt

def build_0021(igg_id):
    pkt = struct.pack('<HH', 21, 0x0021)
    pkt += struct.pack('<I', igg_id)
    pkt += struct.pack('<I', 0)
    pkt += bytes([0x0e])
    pkt += struct.pack('<I', GAME_ID_HEX)
    pkt += bytes([0xb0, 0x02, 0x5c, 0x00])
    return pkt

def build_heartbeat(ms_elapsed):
    payload = struct.pack('<I', ms_elapsed) + struct.pack('<I', 0)
    return build_packet(0x0042, payload)

def build_map_ping(ms_elapsed):
    payload = struct.pack('<I', ms_elapsed) + b'\x00' * 12
    return build_packet(0x0043, payload)

# ==================== INITIAL REQUESTS ====================
def send_initial_requests(sock):
    """Send the same initial request sequence the real game client sends after 0x0021."""
    log("Sending initial request sequence...")
    
    # 0x0840 - Request inventory
    sock.sendall(build_packet(0x0840))
    log("  Sent 0x0840 (REQ_INVENTORY)")
    
    # 0x17D4 - Request shop data
    sock.sendall(build_packet(0x17D4))
    log("  Sent 0x17D4 (REQ_SHOP_DATA)")
    
    # 0x0709 - Request mail list
    sock.sendall(build_packet(0x0709))
    log("  Sent 0x0709 (REQ_MAIL_LIST)")
    
    # 0x1839 - Request event data (param=2)
    sock.sendall(build_packet(0x1839, struct.pack('<I', 2)))
    log("  Sent 0x1839 (REQ_EVENT_DATA)")
    
    # 0x0674 - Request guild info
    sock.sendall(build_packet(0x0674))
    log("  Sent 0x0674 (REQ_GUILD_INFO)")
    
    # 0x0767 + 0x0769 - Request chat rooms
    sock.sendall(build_packet(0x0767) + build_packet(0x0769))
    log("  Sent 0x0767+0x0769 (REQ_CHAT_ROOMS)")
    
    # 0x099D batch - Status queries
    for sub_id in [0x0193, 0x0194, 0x0196, 0x0197, 0x0198, 0x0199, 0x019b]:
        sock.sendall(build_packet(0x099D, struct.pack('<I', sub_id)))
    log("  Sent 0x099D x7 (STATUS_QUERY)")

# ==================== PARSE GAME DATA ====================
def parse_000C(data):
    pos = 4  # skip length+opcode already parsed
    igg_id = struct.unpack('<I', data[pos:pos+4])[0]; pos += 4
    pos += 4  # padding
    ip_len = struct.unpack('<H', data[pos:pos+2])[0]; pos += 2
    redirect_ip = data[pos:pos+ip_len].decode('ascii'); pos += ip_len
    redirect_port = struct.unpack('<H', data[pos:pos+2])[0]; pos += 2
    tok_len = struct.unpack('<H', data[pos:pos+2])[0]; pos += 2
    session_token = data[pos:pos+tok_len].decode('ascii'); pos += tok_len
    status = data[pos] if pos < len(data) else -1; pos += 1
    world_id = struct.unpack('<I', data[pos:pos+4])[0] if pos+4 <= len(data) else -1
    return {'ip': redirect_ip, 'port': redirect_port, 'token': session_token,
            'status': status, 'world': world_id}

# ==================== GAME STATE ====================
class GameState:
    def __init__(self):
        self.player_name = ""
        self.power = 0
        self.resources = {}  # {type_id: amount}
        self.buildings = {}  # {slot: {id, level}}
        self.marches = []    # active marches
        self.battles = []    # recent battles
        self.guild_name = ""
        self.vip_level = 0
        self.raw_packets = {}  # opcode -> [payloads]
    
    def update_from_packet(self, opcode, payload):
        if opcode not in self.raw_packets:
            self.raw_packets[opcode] = []
        self.raw_packets[opcode].append(payload)
        
        try:
            if opcode == 0x0034:
                self._parse_player_profile(payload)
            elif opcode == 0x004A:
                self._parse_world_resources(payload)
            elif opcode == 0x0636:
                self._parse_march_json(payload)
            elif opcode == 0x0640:
                self._parse_battle_json(payload)
            elif opcode == 0x07E4:
                self._parse_vip(payload)
            elif opcode == 0x084E:
                self._parse_equipment(payload)
        except Exception as e:
            pass  # Silently skip parse errors
    
    def _parse_player_profile(self, payload):
        if len(payload) < 10:
            return
        name_len = struct.unpack('<H', payload[0:2])[0]
        if 1 <= name_len <= 50 and 2 + name_len <= len(payload):
            try:
                self.player_name = payload[2:2+name_len].decode('utf-8')
            except:
                pass
        base = 2 + name_len
        # Power at base+6 as u32
        if base + 10 <= len(payload):
            self.power = struct.unpack('<I', payload[base+6:base+10])[0]
        # Resources as u32 at offset (base+31) with stride 8
        res_start = base + 31  # first non-zero resource byte
        res_names = ['food', 'stone', 'wood', 'ore', 'unknown', 'gold']
        for i, rname in enumerate(res_names):
            pos = res_start + i * 8
            if pos + 4 <= len(payload):
                val = struct.unpack('<I', payload[pos:pos+4])[0]
                if val > 0:
                    self.resources[rname] = val
    
    def _parse_world_resources(self, payload):
        if len(payload) < 6:
            return
        count = struct.unpack('<H', payload[0:2])[0]
        pos = 2
        for _ in range(min(count, 10)):
            if pos + 6 > len(payload):
                break
            res_type = struct.unpack('<H', payload[pos:pos+2])[0]
            res_val = struct.unpack('<I', payload[pos+2:pos+6])[0]
            self.resources[f'world_type_{res_type}'] = res_val
            pos += 6
    
    def _parse_march_json(self, payload):
        # Find JSON content in payload
        jsons = self._extract_json(payload)
        for j in jsons:
            self.marches.append(j)
    
    def _parse_battle_json(self, payload):
        jsons = self._extract_json(payload)
        for j in jsons:
            self.battles.append(j)
    
    def _parse_vip(self, payload):
        if len(payload) >= 8:
            self.vip_level = payload[7]  # VIP level as u8 at byte 7
    
    def _parse_equipment(self, payload):
        # Contains equipment holder name
        pass
    
    def _extract_json(self, payload):
        results = []
        data = payload
        while b'{' in data:
            start = data.index(b'{')
            depth = 0
            end = start
            for i in range(start, len(data)):
                if data[i:i+1] == b'{':
                    depth += 1
                elif data[i:i+1] == b'}':
                    depth -= 1
                    if depth == 0:
                        end = i + 1
                        break
            if end > start:
                try:
                    j = json.loads(data[start:end].decode('utf-8'))
                    results.append(j)
                except:
                    pass
                data = data[end:]
            else:
                break
        return results
    
    def summary(self):
        lines = []
        if self.player_name:
            lines.append(f"Player: {self.player_name}")
        if self.power:
            lines.append(f"Power: {self.power:,}")
        if self.vip_level:
            lines.append(f"VIP: {self.vip_level}")
        if self.resources:
            lines.append("Resources:")
            for k, v in sorted(self.resources.items()):
                if isinstance(v, int) and v > 0:
                    lines.append(f"  {k}: {v:,}")
        if self.marches:
            lines.append(f"Active marches: {len(self.marches)}")
            for m in self.marches[:3]:
                if isinstance(m, dict):
                    rid = m.get('nResourceID', '?')
                    exp = m.get('HeroExp', '?')
                    lines.append(f"  Resource={rid}, HeroExp={exp}")
        if self.battles:
            lines.append(f"Battle reports: {len(self.battles)}")
            for b in self.battles[:3]:
                if isinstance(b, dict):
                    army = b.get('army', '?')
                    win = b.get('bWin', '?')
                    lines.append(f"  Army={army}, Win={win}")
        lines.append(f"Unique opcodes received: {len(self.raw_packets)}")
        return '\n'.join(lines)

# ==================== BOT CLASS ====================
class ConquerorsBot:
    def __init__(self, access_key):
        self.access_key = access_key
        self.token = derive_token(access_key)
        self.gs_sock = None
        self.connected = False
        self.start_time = 0
        self.heartbeat_thread = None
        self.listener_thread = None
        self.running = False
        self.packet_counts = {}
        self.total_bytes_recv = 0
        self.total_bytes_sent = 0
        self.game_server_ip = None
        self.game_server_port = None
        self.session_token = None
        self.lock = threading.Lock()
        self.game_state = GameState()
    
    def connect_gateway(self):
        log(f"Connecting to Gateway {GATEWAY_IP}:{GATEWAY_PORT}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((GATEWAY_IP, GATEWAY_PORT))
        log("Gateway connected!")
        
        # Send 0x000B
        pkt = build_000B(IGG_ID, self.token, WORLD_ID)
        sock.sendall(pkt)
        self.total_bytes_sent += len(pkt)
        log(f"Sent 0x000B ({len(pkt)}B)")
        
        # Receive 0x000C
        resp_data = b''
        sock.settimeout(10)
        while len(resp_data) < 4:
            resp_data += sock.recv(4096)
        pkt_len = struct.unpack('<H', resp_data[0:2])[0]
        while len(resp_data) < pkt_len:
            resp_data += sock.recv(4096)
        
        opcode = struct.unpack('<H', resp_data[2:4])[0]
        if opcode != 0x000C:
            raise Exception(f"Expected 0x000C, got 0x{opcode:04X}")
        
        result = parse_000C(resp_data)
        sock.close()
        
        self.game_server_ip = result['ip']
        self.game_server_port = result['port']
        self.session_token = result['token']
        
        log(f"Gateway auth OK → Redirect to {result['ip']}:{result['port']}")
        log(f"  Session: {result['token']}")
        log(f"  World: {result['world']}")
        return result
    
    def connect_game_server(self):
        log(f"Connecting to Game Server {self.game_server_ip}:{self.game_server_port}...")
        self.gs_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gs_sock.settimeout(10)
        self.gs_sock.connect((self.game_server_ip, self.game_server_port))
        log("Game Server connected!")
        
        # Send 0x001F
        pkt = build_001F(IGG_ID, self.session_token)
        self.gs_sock.sendall(pkt)
        self.total_bytes_sent += len(pkt)
        log(f"Sent 0x001F ({len(pkt)}B)")
        
        # Receive 0x0020
        result = recv_packet(self.gs_sock, timeout=10)
        if result is None:
            raise Exception("No 0x0020 response")
        opcode, payload, raw = result
        self.total_bytes_recv += len(raw)
        
        if opcode != 0x0020:
            raise Exception(f"Expected 0x0020, got 0x{opcode:04X}")
        status = payload[0] if payload else -1
        if status != 1:
            raise Exception(f"Login rejected: status={status}")
        log(f"Login OK (status=1)")
        
        # Send 0x0021
        pkt = build_0021(IGG_ID)
        self.gs_sock.sendall(pkt)
        self.total_bytes_sent += len(pkt)
        log(f"Sent 0x0021 ({len(pkt)}B)")
        
        self.start_time = time.time()
        self.connected = True
        return True
    
    def _heartbeat_loop(self):
        """Send heartbeat every 15 seconds."""
        while self.running and self.connected:
            time.sleep(HEARTBEAT_INTERVAL)
            if not self.running or not self.connected:
                break
            try:
                ms = int((time.time() - self.start_time) * 1000)
                pkt = build_heartbeat(ms)
                with self.lock:
                    self.gs_sock.sendall(pkt)
                    self.total_bytes_sent += len(pkt)
                log(f"♥ Heartbeat sent (ms={ms})")
            except Exception as e:
                log(f"Heartbeat failed: {e}", "ERROR")
                self.connected = False
                break
    
    def _listener_loop(self):
        """Receive and log all incoming packets."""
        while self.running and self.connected:
            try:
                result = recv_packet(self.gs_sock, timeout=5)
                if result is None:
                    continue
                opcode, payload, raw = result
                self.total_bytes_recv += len(raw)
                name = opname(opcode)
                self.packet_counts[opcode] = self.packet_counts.get(opcode, 0) + 1
                
                # Log packet (suppress noisy ones)
                # Update game state
                self.game_state.update_from_packet(opcode, payload)
                
                if opcode == 0x0042:
                    pass  # heartbeat echo, don't spam
                elif opcode == 0x036C:
                    pass  # server tick, very frequent
                else:
                    log(f"← 0x{opcode:04X} {name} ({len(raw)}B)")
                    
            except Exception as e:
                if self.running:
                    log(f"Listener error: {e}", "ERROR")
                    self.connected = False
                break
    
    def send_packet(self, opcode, payload=b''):
        """Send a custom packet."""
        pkt = build_packet(opcode, payload)
        with self.lock:
            self.gs_sock.sendall(pkt)
            self.total_bytes_sent += len(pkt)
        log(f"→ 0x{opcode:04X} {opname(opcode)} ({len(pkt)}B)")
    
    def start(self):
        """Full connection flow."""
        log("=" * 60)
        log("IGG Conquerors Bot Starting")
        log("=" * 60)
        log(f"IGG ID: {IGG_ID}")
        log(f"Access Key: {self.access_key}")
        log(f"Token: {self.token.hex()}")
        
        # Phase 1: Gateway
        self.connect_gateway()
        
        # Phase 2: Game Server
        self.connect_game_server()
        
        # Phase 3: Receive initial game data flood
        log("Receiving initial game data...")
        initial_packets = recv_all_packets(self.gs_sock, timeout=8)
        for opcode, payload, raw in initial_packets:
            self.total_bytes_recv += len(raw)
            name = opname(opcode)
            self.packet_counts[opcode] = self.packet_counts.get(opcode, 0) + 1
            self.game_state.update_from_packet(opcode, payload)
            log(f"← 0x{opcode:04X} {name} ({len(raw)}B)")
        log(f"Initial data: {len(initial_packets)} packets, {self.total_bytes_recv} bytes")
        
        # Phase 4: Send initial requests (mimic real client)
        send_initial_requests(self.gs_sock)
        
        # Receive responses
        time.sleep(2)
        response_packets = recv_all_packets(self.gs_sock, timeout=5)
        for opcode, payload, raw in response_packets:
            self.total_bytes_recv += len(raw)
            name = opname(opcode)
            self.packet_counts[opcode] = self.packet_counts.get(opcode, 0) + 1
            self.game_state.update_from_packet(opcode, payload)
            log(f"← 0x{opcode:04X} {name} ({len(raw)}B)")
        log(f"Response data: {len(response_packets)} packets")
        
        # Show game state
        log("")
        log("=== GAME STATE ===")
        for line in self.game_state.summary().split('\n'):
            log(line)
        
        # Phase 5: Start keepalive + listener
        self.running = True
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self.listener_thread = threading.Thread(target=self._listener_loop, daemon=True)
        self.heartbeat_thread.start()
        self.listener_thread.start()
        
        log("")
        log("=" * 60)
        log("BOT ONLINE - Connected and keepalive active")
        log("=" * 60)
        log("")
        log("Commands:")
        log("  status   - Connection stats")
        log("  state    - Game state (resources, marches, etc)")
        log("  packets  - Packet counts")
        log("  hb       - Manual heartbeat")
        log("  guild    - Request guild info")
        log("  mail     - Request mail list")
        log("  inventory - Request inventory")
        log("  mapping  - Map ping")
        log("  raw <op_hex> [payload_hex] - Send raw packet")
        log("  dump <op_hex> - Dump raw packet data")
        log("  quit     - Disconnect and exit")
        log("")
        
        return True
    
    def interactive(self):
        """Interactive command loop."""
        try:
            while self.running and self.connected:
                try:
                    cmd = input("bot> ").strip()
                except EOFError:
                    break
                
                if not cmd:
                    continue
                
                parts = cmd.split(None, 1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                if command == "quit" or command == "exit":
                    break
                elif command == "status":
                    elapsed = time.time() - self.start_time
                    log(f"Connected: {self.connected}")
                    log(f"Uptime: {elapsed:.0f}s ({elapsed/60:.1f}m)")
                    log(f"Sent: {self.total_bytes_sent} bytes")
                    log(f"Recv: {self.total_bytes_recv} bytes")
                    log(f"Server: {self.game_server_ip}:{self.game_server_port}")
                elif command == "packets":
                    log("Packet counts:")
                    for op in sorted(self.packet_counts.keys()):
                        log(f"  0x{op:04X} {opname(op):25s} = {self.packet_counts[op]}x")
                elif command == "hb":
                    ms = int((time.time() - self.start_time) * 1000)
                    pkt = build_heartbeat(ms)
                    with self.lock:
                        self.gs_sock.sendall(pkt)
                        self.total_bytes_sent += len(pkt)
                    log(f"Manual heartbeat sent (ms={ms})")
                elif command == "raw":
                    try:
                        raw_parts = args.split(None, 1)
                        op = int(raw_parts[0], 16)
                        payload = bytes.fromhex(raw_parts[1]) if len(raw_parts) > 1 else b''
                        self.send_packet(op, payload)
                    except Exception as e:
                        log(f"Raw send error: {e}", "ERROR")
                elif command == "mapping":
                    ms = int((time.time() - self.start_time) * 1000)
                    pkt = build_map_ping(ms)
                    with self.lock:
                        self.gs_sock.sendall(pkt)
                        self.total_bytes_sent += len(pkt)
                    log(f"Map ping sent (ms={ms})")
                elif command == "guild":
                    self.send_packet(0x0674)
                elif command == "mail":
                    self.send_packet(0x0709)
                elif command == "inventory":
                    self.send_packet(0x0840)
                elif command == "state":
                    log("=== GAME STATE ===")
                    for line in self.game_state.summary().split('\n'):
                        log(line)
                elif command == "dump":
                    try:
                        op = int(args.strip(), 16)
                        if op in self.game_state.raw_packets:
                            payloads = self.game_state.raw_packets[op]
                            log(f"0x{op:04X}: {len(payloads)} packet(s)")
                            for i, p in enumerate(payloads[:3]):
                                log(f"  [{i}] {len(p)}B: {p[:128].hex()}")
                                # Try to find strings
                                strings = self.game_state._extract_json(p)
                                if strings:
                                    for j in strings[:3]:
                                        log(f"      JSON: {json.dumps(j, ensure_ascii=False)[:200]}")
                        else:
                            log(f"No packets for 0x{op:04X}")
                    except Exception as e:
                        log(f"Dump error: {e}")
                elif command == "help":
                    log("Commands: status, state, packets, hb, mapping, guild, mail, inventory, dump <op>, raw <op> [payload], quit")
                else:
                    log(f"Unknown command: {command}. Type 'help' for list.")
        except KeyboardInterrupt:
            pass
        
        self.stop()
    
    def stop(self):
        log("Shutting down...")
        self.running = False
        self.connected = False
        if self.gs_sock:
            try:
                self.gs_sock.close()
            except:
                pass
        
        log(f"Final stats:")
        log(f"  Total sent: {self.total_bytes_sent} bytes")
        log(f"  Total recv: {self.total_bytes_recv} bytes")
        log(f"  Unique opcodes seen: {len(self.packet_counts)}")
        if self.start_time:
            log(f"  Uptime: {time.time() - self.start_time:.0f}s")
        log("Bot stopped.")

# ==================== MAIN ====================
def main():
    global LOG_FILE
    
    # Setup log file
    log_path = os.path.join(os.path.dirname(__file__), "bot_session.log")
    LOG_FILE = open(log_path, "w", encoding="utf-8")
    
    # Get access key
    access_key = STORED_ACCESS_KEY
    
    if "--adb" in sys.argv:
        extracted = extract_key_from_device()
        if extracted:
            access_key = extracted
        else:
            log("ADB extraction failed, using stored key", "WARN")
    
    if "--key" in sys.argv:
        idx = sys.argv.index("--key")
        if idx + 1 < len(sys.argv):
            access_key = sys.argv[idx + 1]
        else:
            log("--key requires a value", "ERROR")
            return
    
    if not access_key or len(access_key) != 32:
        log(f"Invalid access key (length={len(access_key) if access_key else 0})", "ERROR")
        return
    
    # Create and run bot
    bot = ConquerorsBot(access_key)
    
    try:
        if bot.start():
            bot.interactive()
    except Exception as e:
        log(f"Bot error: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        bot.stop()
    
    LOG_FILE.close()

if __name__ == "__main__":
    main()

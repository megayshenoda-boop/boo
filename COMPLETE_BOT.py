"""
IGG Conquerors (الفاتحون) - COMPLETE BOT
=========================================
Full automation from HTTP Login to Encrypted Game Actions.

Flow:
  Phase 1: HTTP Login (4 steps) → access_token
  Phase 2: Gateway Auth (TCP) → redirect IP + session_token
  Phase 3: Game Server Login → game data flood
  Phase 4: Extract server_key from 0x0038
  Phase 5: Send encrypted actions (train/build/gather)

Usage:
  python COMPLETE_BOT.py                        # Use stored access key (skip HTTP)
  python COMPLETE_BOT.py --adb                  # Extract key from emulator via ADB
  python COMPLETE_BOT.py --key <access_key>     # Provide access key manually
  python COMPLETE_BOT.py --http                  # Full HTTP login flow (needs Node.js proxy for Cloudflare)

All secrets and algorithms are hardcoded - no external dependencies needed.
"""
import socket
import struct
import time
import threading
import hashlib
import hmac
import base64
import json
import random
import sys
import os
import subprocess
import re
import uuid
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote
from urllib.error import HTTPError, URLError
from http.cookiejar import CookieJar as _CookieJar
import urllib.request

# ╔══════════════════════════════════════════════════════════════╗
# ║                    CONSTANTS & SECRETS                       ║
# ╚══════════════════════════════════════════════════════════════╝

IGG_ID = 2082384585
GAME_ID = "1057029902"
GAME_ID_HEX = 0x3F00FF0E
GATEWAY_IP = "54.93.167.80"
GATEWAY_PORT = 5997
WORLD_ID = 211
HMAC_KEY = "07Z8D2AoYFGGivw40fEOj9swnpyF7Pw3ilKpVKnJ"
CQ_XOR_KEY = ("CQ_secret" * 4)[:32]  # "CQ_secretCQ_secretCQ_secretCQ_se"
USER_AGENT = "1057029902/6.1.0 Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G9880 Build/N2G47H)"
HEARTBEAT_INTERVAL = 15.0
STORED_ACCESS_KEY = "9f4675b1b1d1b9fd0a3db5145018469e"
ADB_PATH = r"D:\Program Files\Microvirt\MEmu\adb.exe"
ADB_DEVICE = "127.0.0.1:21503"

# Email/password for HTTP login
EMAIL = "minaadelzx12@gmail.com"
PASSWORD = "U112233u"

# CMsgCodec encryption table (extracted from libgame.so via ARM64 disassembly)
TABLE = [0x58, 0xef, 0xd7, 0x14, 0xa2, 0x3b, 0x9c]
SERVER_KEY_FIELD_ID = 0x4F  # Field 79 in 0x0038 packet

# Opcode names for logging
OPCODES = {
    0x000B: "GW_AUTH_REQ", 0x000C: "GW_AUTH_RESP",
    0x001F: "GS_LOGIN", 0x0020: "GS_LOGIN_RESP", 0x0021: "WORLD_ENTRY",
    0x0002: "HEARTBEAT_ECHO", 0x0034: "PLAYER_PROFILE", 0x0038: "CASTLE_DATA",
    0x004A: "WORLD_RESOURCES", 0x0042: "HEARTBEAT", 0x0043: "MAP_PING",
    0x0064: "BUILDING_LIST", 0x0085: "ALLIANCE_MEMBERS",
    0x0097: "ALLIANCE_INFO", 0x00AA: "BUILDING_QUEUE",
    0x015E: "TRAINING_QUEUE", 0x01D4: "UNK_01D4",
    0x036C: "SERVER_TICK", 0x039B: "INIT_TIMESTAMP",
    0x0636: "MARCH_DATA", 0x0640: "BATTLE_REPORT",
    0x0654: "GUILD_TECH", 0x0674: "REQ_GUILD_INFO",
    0x0675: "GUILD_DETAIL", 0x0709: "REQ_MAIL",
    0x0767: "REQ_CHAT", 0x07E4: "VIP_DATA",
    0x083F: "ITEM_DATA", 0x0840: "REQ_INVENTORY",
    0x084E: "EQUIPMENT_DATA", 0x099D: "STATUS_QUERY",
    0x0A00: "RESOURCE_TIMERS", 0x0A02: "TECH_TREE",
    0x0A0A: "TROOP_DATA", 0x0A0B: "HERO_DATA",
    0x0C4E: "QUEST_DATA", 0x0CE8: "ACTION_GATHER",
    0x0CEB: "ACTION_TRAIN", 0x0CED: "ACTION_BUILD",
    0x0CEF: "ACTION_UNK", 0x0F0A: "EVENT_NOTIFY",
    0x0F0E: "EVENT_DATA", 0x17D4: "REQ_SHOP",
}

# ╔══════════════════════════════════════════════════════════════╗
# ║                         LOGGING                              ║
# ╚══════════════════════════════════════════════════════════════╝

LOG_FILE = None

def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    line = f"[{ts}] [{level}] {msg}"
    print(line)
    if LOG_FILE:
        LOG_FILE.write(line + "\n")
        LOG_FILE.flush()

def opname(opcode):
    return OPCODES.get(opcode, f"0x{opcode:04X}")

# ╔══════════════════════════════════════════════════════════════╗
# ║                    CMsgCodec ENCRYPTION                      ║
# ║  Algorithm: enc[i] = ((plain[i] + msg*17) ^ sk ^ tbl) & FF  ║
# ╚══════════════════════════════════════════════════════════════╝

class CMsgCodec:
    """CMsgCodec Encoder/Decoder - CRACKED from libgame.so ARM64 disassembly."""

    def __init__(self, server_key_bytes):
        self.sk = list(server_key_bytes)

    @classmethod
    def from_u32(cls, key_u32):
        return cls([
            key_u32 & 0xFF, (key_u32 >> 8) & 0xFF,
            (key_u32 >> 16) & 0xFF, (key_u32 >> 24) & 0xFF,
        ])

    def decode(self, payload):
        if len(payload) < 5:
            return payload
        msg = [payload[1], payload[3]]
        dec = bytearray(len(payload) - 4)
        for p in range(4, len(payload)):
            i = p + 4
            table_b = TABLE[i % 7]
            sk_b = self.sk[i % 4]
            msg_b = msg[i % 2]
            intermediate = (payload[p] ^ sk_b ^ table_b) & 0xFF
            dec[p - 4] = (intermediate - msg_b * 17) & 0xFF
        return bytes(dec)

    def encode(self, opcode, action_data, msg_value=None):
        if msg_value is None:
            msg_value = random.randint(0, 0xFFFF)
        msg_lo = msg_value & 0xFF
        msg_hi = (msg_value >> 8) & 0xFF
        msg = [msg_lo, msg_hi]

        payload_len = 4 + len(action_data)
        total_len = 4 + payload_len
        pkt = bytearray(total_len)
        struct.pack_into('<H', pkt, 0, total_len)
        struct.pack_into('<H', pkt, 2, opcode)

        for j, b in enumerate(action_data):
            pkt[8 + j] = b

        checksum = 0
        for i in range(8, total_len):
            p = i - 4
            table_b = TABLE[i % 7]
            sk_b = self.sk[i % 4]
            msg_b = msg[i % 2]
            intermediate = (pkt[i] + msg_b * 17) & 0xFF
            enc_byte = (intermediate ^ sk_b ^ table_b) & 0xFF
            pkt[i] = enc_byte
            checksum = (checksum + enc_byte) & 0xFFFFFFFF

        pkt[4] = checksum & 0xFF
        pkt[5] = msg_lo
        pkt[6] = msg_lo ^ 0xB7
        pkt[7] = msg_hi
        return bytes(pkt)

    def decode_packet(self, raw_packet):
        if len(raw_packet) < 8:
            return None, None
        total_len = struct.unpack('<H', raw_packet[0:2])[0]
        opcode = struct.unpack('<H', raw_packet[2:4])[0]
        payload = raw_packet[4:total_len]
        action_data = self.decode(payload)
        return opcode, action_data


def extract_server_key_from_0x0038(payload):
    """Extract server_key u32 from 0x0038 packet. Field 0x4F = server key.
    Structure: [2B LE entry_count] then [entry_count * 12B entries]
    Each entry: [4B LE field_id][8B LE value]
    """
    if len(payload) < 14:
        return None
    entry_count = struct.unpack('<H', payload[0:2])[0]
    # Scan entries starting at offset 2, stride 12
    for idx in range(entry_count):
        off = 2 + idx * 12
        if off + 12 > len(payload):
            break
        field_id = struct.unpack('<I', payload[off:off+4])[0]
        if field_id == SERVER_KEY_FIELD_ID:
            return struct.unpack('<I', payload[off+4:off+8])[0]
    return None

# ╔══════════════════════════════════════════════════════════════╗
# ║                    ACTION DATA BUILDERS                      ║
# ╚══════════════════════════════════════════════════════════════╝

def build_train_action(igg_id, train_type=0x01, flag=0x01):
    """Build 0x0CEB train action data (10 bytes)."""
    data = bytearray(10)
    data[0] = train_type
    struct.pack_into('<I', data, 1, igg_id)
    data[9] = flag
    return bytes(data)

def build_build_action(igg_id, building_type=0x01, building_id=480):
    """Build 0x0CED build action data (19 bytes)."""
    data = bytearray(19)
    struct.pack_into('<I', data, 0, building_type)
    struct.pack_into('<I', data, 4, building_id)
    struct.pack_into('<I', data, 9, igg_id)
    return bytes(data)

def build_gather_action(igg_id, march_slot=1, march_type=0x1748,
                        troop_types=None, troop_count=2):
    """Build 0x0CE8 gather action data (62 bytes)."""
    if troop_types is None:
        troop_types = [201, 212, 206, 216, 224, 211]
    data = bytearray(62)
    data[0] = march_slot
    data[1] = random.randint(0, 255)
    data[2] = random.randint(0, 255)
    data[3] = random.randint(0, 255)
    struct.pack_into('<H', data, 4, march_type)
    data[12] = 0x02
    data[13] = 0x05
    for i, tid in enumerate(troop_types[:6]):
        struct.pack_into('<I', data, 14 + i*4, tid)
    struct.pack_into('<I', data, 38, troop_count)
    struct.pack_into('<I', data, 49, igg_id)
    return bytes(data)

# ╔══════════════════════════════════════════════════════════════╗
# ║                    PACKET IO HELPERS                         ║
# ╚══════════════════════════════════════════════════════════════╝

def build_packet(opcode, payload=b''):
    length = 4 + len(payload)
    return struct.pack('<HH', length, opcode) + payload

def recv_packet(sock, timeout=10):
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
        return None

def recv_all_packets(sock, timeout=5):
    packets = []
    deadline = time.time() + timeout
    while time.time() < deadline:
        remaining = max(0.1, deadline - time.time())
        pkt = recv_packet(sock, timeout=remaining)
        if pkt is None:
            break
        packets.append(pkt)
    return packets

# ╔══════════════════════════════════════════════════════════════╗
# ║                    TOKEN & AUTH                              ║
# ╚══════════════════════════════════════════════════════════════╝

def derive_gateway_token(access_key):
    """token = XOR(access_key_ascii, "CQ_secret" repeating to 32)"""
    xor_key = CQ_XOR_KEY.encode('ascii')
    return bytes(a ^ b for a, b in zip(access_key.encode('ascii'), xor_key))

def extract_key_from_adb():
    """Extract weg_Accesskey from device/emulator via ADB."""
    log("Extracting access key from device via ADB...")
    try:
        cmd = [ADB_PATH, "-s", ADB_DEVICE, "shell",
               "cat /data/data/com.igg.android.conquerors/shared_prefs/weg_login_file.xml"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        match = re.search(r'weg_Accesskey">(.*?)<', result.stdout)
        if match:
            key = match.group(1)
            log(f"ADB: Extracted key = {key}")
            return key
    except Exception as e:
        log(f"ADB extraction failed: {e}", "ERROR")
    return None

# ╔══════════════════════════════════════════════════════════════╗
# ║                    HTTP LOGIN (4 STEPS)                      ║
# ╚══════════════════════════════════════════════════════════════╝

def md5(s):
    return hashlib.md5(s.encode('utf-8') if isinstance(s, str) else s).hexdigest()

def generate_sign(params):
    keys = sorted(params.keys())
    parts = [f"{k}={params[k]}" for k in keys]
    joined = "&".join(parts)
    return md5(joined + md5(GAME_ID)).upper()

def http_login():
    """Full HTTP login flow. Returns access_token or None."""
    log("=== HTTP LOGIN START ===")
    udid = str(uuid.uuid4())
    uiid = str(uuid.uuid4())

    cookie_jar = _CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

    # Step 1: Get PHPSESSID
    log("Step 1: Getting PHPSESSID...")
    nonce1 = str(int(time.time() * 1000))
    sign1 = generate_sign({
        'for_audting': '0', 'resource': 'embed/entry', 'scenario': 'sign_in',
        'x-gpc-game-id': GAME_ID, 'x-gpc-nonce': nonce1,
        'x-gpc-udid': udid, 'x-gpc-uiid': uiid,
        'x_gpc_jsbridge': 'gpc_jsbridge_common/2.0.0_2;'
    })

    url1 = "https://account.igg.com/embed/entry?scenario=sign_in&for_audting=0&x_gpc_jsbridge=gpc_jsbridge_common%2F2.0.0_2%3B"
    req1 = Request(url1, headers={
        "User-Agent": USER_AGENT,
        "X-Requested-With": "com.igg.android.conquerors",
        "x-gpc-game-id": GAME_ID, "x-gpc-sign": sign1,
        "x-gpc-nonce": nonce1, "x-gpc-ver": "3.0",
        "x-gpc-udid": udid, "x-gpc-uiid": uiid
    })

    try:
        resp1 = opener.open(req1, timeout=15)
        resp1.read()
    except Exception as e:
        log(f"Step 1 error: {e}", "ERROR")
        return None

    phpsessid = None
    for cookie in cookie_jar:
        if cookie.name == "PHPSESSID":
            phpsessid = cookie.value
    if not phpsessid:
        log("Step 1: PHPSESSID not found!", "ERROR")
        return None
    log(f"Step 1: PHPSESSID = {phpsessid}")

    # Step 2: Email login
    log("Step 2: Email login...")
    login_body = f"email={quote(EMAIL)}&password={md5(PASSWORD)}&token="
    req2 = Request("https://account.igg.com/embed/login/email", data=login_body.encode(), headers={
        "User-Agent": USER_AGENT,
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://account.igg.com/embed/login/index",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    })

    try:
        resp2 = opener.open(req2, timeout=15)
        data2 = json.loads(resp2.read())
    except HTTPError as e:
        body = e.read().decode() if hasattr(e, 'read') else str(e)
        log(f"Step 2 HTTP error {e.code}: {body[:200]}", "ERROR")
        return None
    except Exception as e:
        log(f"Step 2 error: {e}", "ERROR")
        return None

    if data2.get("error", {}).get("code") != 0:
        log(f"Step 2: Login failed: {json.dumps(data2, ensure_ascii=False)[:200]}", "ERROR")
        return None
    log("Step 2: Login OK!")

    # Step 3: Get Platform JWT
    log("Step 3: Getting Platform JWT...")
    req3_body = f"user_id={IGG_ID}"
    req3 = Request("https://account.igg.com/embed/login/user_id", data=req3_body.encode(), headers={
        "User-Agent": USER_AGENT,
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://account.igg.com/embed/login/index",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    })

    try:
        resp3 = opener.open(req3, timeout=15)
        data3 = json.loads(resp3.read())
    except Exception as e:
        log(f"Step 3 error: {e}", "ERROR")
        return None

    redirect_url = data3.get("data", {}).get("redirectUrl", "")
    jwt_match = re.search(r'token=([^&]+)', redirect_url)
    if not jwt_match:
        log(f"Step 3: JWT not found in redirect URL", "ERROR")
        return None
    platform_jwt = jwt_match.group(1)
    log(f"Step 3: JWT ({len(platform_jwt)} chars)")

    # Step 4: Get Access Token (HMAC-SHA256)
    log("Step 4: Getting Access Token (HMAC-SHA256)...")
    step4_body = f"type=gpcaccount&platform_token={quote(json.dumps({'token': platform_jwt}))}"

    body_digest = base64.b64encode(
        hashlib.sha256(step4_body.encode()).digest()
    ).decode()

    nonce4 = str(int(time.time() * 1000))
    utc_date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())

    canonical = "\n".join([
        f"x-gpc-uiid: {uiid}",
        f"x-gpc-nonce: {nonce4}",
        "x-gpc-evo: 1;gpc=s2",
        f"x-gpc-game-id: {GAME_ID}",
        f"x-gpc-udid: {udid}",
        f"digest: SHA-256={body_digest}",
        f"date: {utc_date}",
        "POST /ums/member/access_token/platform HTTP/1.1"
    ])

    sig = base64.b64encode(
        hmac.new(HMAC_KEY.encode(), canonical.encode(), hashlib.sha256).digest()
    ).decode()

    auth_header = (
        f'hmac username="{GAME_ID}", algorithm="hmac-sha256", '
        f'headers="x-gpc-uiid x-gpc-nonce x-gpc-evo x-gpc-game-id x-gpc-udid digest date request-line", '
        f'signature="{sig}"'
    )

    req4 = Request("https://apis-dsa.iggapis.com/ums/member/access_token/platform",
                   data=step4_body.encode(), headers={
        "x-gpc-uiid": uiid, "x-gpc-nonce": nonce4,
        "x-gpc-evo": "1;gpc=s2", "x-gpc-game-id": GAME_ID,
        "x-gpc-udid": udid, "x-gpc-ver": "2.5", "x-gpc-family": "bmbkf3",
        "Date": utc_date, "Digest": f"SHA-256={body_digest}",
        "User-Agent": f"{USER_AGENT} GPCSDK/2.29.0-su.1-beta.1.0+137",
        "Authorization": auth_header,
        "Host": "apis-dsa.iggapis.com",
        "Content-Type": "application/x-www-form-urlencoded"
    })

    try:
        resp4 = opener.open(req4, timeout=15)
        data4 = json.loads(resp4.read())
    except HTTPError as e:
        body = e.read().decode() if hasattr(e, 'read') else str(e)
        log(f"Step 4 HTTP error {e.code}: {body[:300]}", "ERROR")
        return None
    except Exception as e:
        log(f"Step 4 error: {e}", "ERROR")
        return None

    access_token = data4.get("data", {}).get("access_token")
    if not access_token:
        log(f"Step 4: No access_token in response: {json.dumps(data4)[:200]}", "ERROR")
        return None

    log(f"Step 4: Access Token = {access_token}")
    log("=== HTTP LOGIN SUCCESS ===")
    return access_token

# ╔══════════════════════════════════════════════════════════════╗
# ║                    GATEWAY & GAME SERVER PACKETS             ║
# ╚══════════════════════════════════════════════════════════════╝

def build_000B(igg_id, token, world_id):
    pkt = struct.pack('<HH', 79, 0x000B)
    pkt += struct.pack('<I', 1)           # version
    pkt += struct.pack('<I', 0)
    pkt += struct.pack('<I', igg_id)
    pkt += struct.pack('<I', 0)
    pkt += struct.pack('<H', 32)          # token length
    pkt += token                           # 32 bytes
    pkt += struct.pack('<I', 0)
    pkt += struct.pack('<I', 2)           # platform=android
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

def parse_000C(payload):
    """Parse 0x000C Gateway response payload."""
    pos = 0
    igg = struct.unpack('<I', payload[pos:pos+4])[0]; pos += 4
    pos += 4  # padding
    ip_len = struct.unpack('<H', payload[pos:pos+2])[0]; pos += 2
    if ip_len <= 0 or ip_len > 50:
        return None
    redirect_ip = payload[pos:pos+ip_len].decode('ascii'); pos += ip_len
    redirect_port = struct.unpack('<H', payload[pos:pos+2])[0]; pos += 2
    tok_len = struct.unpack('<H', payload[pos:pos+2])[0]; pos += 2
    session_token = payload[pos:pos+tok_len].decode('ascii'); pos += tok_len
    status = payload[pos] if pos < len(payload) else -1; pos += 1
    world_id = struct.unpack('<I', payload[pos:pos+4])[0] if pos+4 <= len(payload) else -1
    return {
        'ip': redirect_ip, 'port': redirect_port,
        'token': session_token, 'status': status, 'world': world_id
    }

# ╔══════════════════════════════════════════════════════════════╗
# ║                    GAME STATE PARSER                         ║
# ╚══════════════════════════════════════════════════════════════╝

class GameState:
    def __init__(self):
        self.player_name = ""
        self.power = 0
        self.resources = {}
        self.vip_level = 0
        self.server_key = None
        self.raw_packets = {}

    def update(self, opcode, payload):
        if opcode not in self.raw_packets:
            self.raw_packets[opcode] = []
        self.raw_packets[opcode].append(payload)

        if opcode == 0x0038:
            key = extract_server_key_from_0x0038(payload)
            if key is not None:
                self.server_key = key
                log(f"*** SERVER KEY EXTRACTED: 0x{key:08x} ***")

        elif opcode == 0x0034:
            self._parse_profile(payload)

        elif opcode == 0x07E4:
            if len(payload) >= 8:
                self.vip_level = payload[7]

    def _parse_profile(self, payload):
        if len(payload) < 10:
            return
        name_len = struct.unpack('<H', payload[0:2])[0]
        if 1 <= name_len <= 50 and 2 + name_len <= len(payload):
            try:
                self.player_name = payload[2:2+name_len].decode('utf-8')
            except:
                pass
        base = 2 + name_len
        if base + 10 <= len(payload):
            self.power = struct.unpack('<I', payload[base+6:base+10])[0]
        res_start = base + 31
        res_names = ['food', 'stone', 'wood', 'ore', 'unknown', 'gold']
        for i, rname in enumerate(res_names):
            pos = res_start + i * 8
            if pos + 4 <= len(payload):
                val = struct.unpack('<I', payload[pos:pos+4])[0]
                if val > 0:
                    self.resources[rname] = val

    def summary(self):
        lines = []
        if self.player_name: lines.append(f"  Player: {self.player_name}")
        if self.power: lines.append(f"  Power: {self.power:,}")
        if self.vip_level: lines.append(f"  VIP: {self.vip_level}")
        if self.resources:
            lines.append("  Resources:")
            for k, v in sorted(self.resources.items()):
                if isinstance(v, int) and v > 0:
                    lines.append(f"    {k}: {v:,}")
        if self.server_key:
            lines.append(f"  Server Key: 0x{self.server_key:08x}")
        lines.append(f"  Unique opcodes: {len(self.raw_packets)}")
        return '\n'.join(lines)

# ╔══════════════════════════════════════════════════════════════╗
# ║                    MAIN BOT CLASS                            ║
# ╚══════════════════════════════════════════════════════════════╝

class ConquerorsBot:
    def __init__(self, access_key):
        self.access_key = access_key
        self.token = derive_gateway_token(access_key)
        self.gs_sock = None
        self.connected = False
        self.running = False
        self.start_time = 0
        self.game_state = GameState()
        self.codec = None  # Set after extracting server_key
        self.lock = threading.Lock()
        self.total_sent = 0
        self.total_recv = 0

    # ---- Phase 2: Gateway Auth ----
    def connect_gateway(self):
        log(f"Connecting to Gateway {GATEWAY_IP}:{GATEWAY_PORT}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((GATEWAY_IP, GATEWAY_PORT))
        log("Gateway connected!")

        pkt = build_000B(IGG_ID, self.token, WORLD_ID)
        sock.sendall(pkt)
        self.total_sent += len(pkt)
        log(f"Sent 0x000B ({len(pkt)}B)")

        result = recv_packet(sock, timeout=10)
        if result is None:
            sock.close()
            raise Exception("No response from Gateway")

        opcode, payload, raw = result
        self.total_recv += len(raw)

        if opcode != 0x000C:
            sock.close()
            raise Exception(f"Expected 0x000C, got 0x{opcode:04X}")

        info = parse_000C(payload)
        sock.close()

        if info is None or not info['ip']:
            raise Exception("Gateway returned empty redirect (access key expired?)")

        self.game_ip = info['ip']
        self.game_port = info['port']
        self.session_token = info['token']

        log(f"Gateway OK -> {info['ip']}:{info['port']}")
        log(f"Session: {info['token']}")
        log(f"World: {info['world']}")
        return info

    # ---- Phase 3: Game Server Login ----
    def connect_game_server(self):
        log(f"Connecting to Game Server {self.game_ip}:{self.game_port}...")
        self.gs_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gs_sock.settimeout(10)
        self.gs_sock.connect((self.game_ip, self.game_port))
        log("Game Server connected!")

        # Send 0x001F
        pkt = build_001F(IGG_ID, self.session_token)
        self.gs_sock.sendall(pkt)
        self.total_sent += len(pkt)
        log(f"Sent 0x001F ({len(pkt)}B)")

        result = recv_packet(self.gs_sock, timeout=10)
        if result is None:
            raise Exception("No 0x0020 response")
        opcode, payload, raw = result
        self.total_recv += len(raw)

        if opcode != 0x0020:
            raise Exception(f"Expected 0x0020, got 0x{opcode:04X}")
        status = payload[0] if payload else -1
        if status != 1:
            raise Exception(f"Login rejected: status={status}")
        log("Login OK (status=1)")

        # Send 0x0021
        pkt = build_0021(IGG_ID)
        self.gs_sock.sendall(pkt)
        self.total_sent += len(pkt)
        log(f"Sent 0x0021 ({len(pkt)}B)")
        self.start_time = time.time()
        self.connected = True

    # ---- Phase 4: Receive game data & extract server key ----
    def receive_game_data(self):
        log("Receiving initial game data...")
        packets = recv_all_packets(self.gs_sock, timeout=10)
        for opcode, payload, raw in packets:
            self.total_recv += len(raw)
            self.game_state.update(opcode, payload)
            name = opname(opcode)
            if opcode not in (0x036C, 0x0042):
                log(f"  <- 0x{opcode:04X} {name} ({len(raw)}B)")

        log(f"Received {len(packets)} packets, {self.total_recv} bytes")

        if self.game_state.server_key is None:
            log("Server key not found yet, sending initial requests...")
            for op in [0x0840, 0x17D4, 0x0709, 0x0674, 0x0767, 0x0769]:
                self.gs_sock.sendall(build_packet(op))
            for sub_id in [0x0193, 0x0198, 0x019D]:
                self.gs_sock.sendall(build_packet(0x099D, struct.pack('<I', sub_id)))

            more = recv_all_packets(self.gs_sock, timeout=8)
            for opcode, payload, raw in more:
                self.total_recv += len(raw)
                self.game_state.update(opcode, payload)
            log(f"Second wave: {len(more)} more packets")

        if self.game_state.server_key:
            self.codec = CMsgCodec.from_u32(self.game_state.server_key)
            log(f"CMsgCodec ready with key 0x{self.game_state.server_key:08x}")
        else:
            log("WARNING: Server key not found! Encrypted actions will not work.", "WARN")

    # ---- Heartbeat ----
    def _heartbeat_loop(self):
        while self.running and self.connected:
            time.sleep(HEARTBEAT_INTERVAL)
            if not self.running or not self.connected:
                break
            try:
                ms = int((time.time() - self.start_time) * 1000)
                pkt = build_heartbeat(ms)
                with self.lock:
                    self.gs_sock.sendall(pkt)
                    self.total_sent += len(pkt)
            except Exception as e:
                log(f"Heartbeat failed: {e}", "ERROR")
                self.connected = False
                break

    # ---- Listener ----
    def _listener_loop(self):
        while self.running and self.connected:
            try:
                result = recv_packet(self.gs_sock, timeout=5)
                if result is None:
                    continue
                opcode, payload, raw = result
                self.total_recv += len(raw)
                self.game_state.update(opcode, payload)

                if self.game_state.server_key and not self.codec:
                    self.codec = CMsgCodec.from_u32(self.game_state.server_key)
                    log(f"CMsgCodec now ready (key 0x{self.game_state.server_key:08x})")

                if opcode not in (0x0042, 0x036C, 0x0002):
                    log(f"  <- 0x{opcode:04X} {opname(opcode)} ({len(raw)}B)")
            except Exception as e:
                if self.running:
                    log(f"Listener error: {e}", "ERROR")
                    self.connected = False
                break

    # ---- Send Actions ----
    def send_train(self, train_type=0x01):
        if not self.codec:
            log("Cannot send: no server key!", "ERROR")
            return False
        data = build_train_action(IGG_ID, train_type=train_type)
        pkt = self.codec.encode(0x0CEB, data)
        with self.lock:
            self.gs_sock.sendall(pkt)
            self.total_sent += len(pkt)
        log(f"  -> ACTION_TRAIN 0x0CEB ({len(pkt)}B)")
        return True

    def send_build(self, building_type=1, building_id=480):
        if not self.codec:
            log("Cannot send: no server key!", "ERROR")
            return False
        data = build_build_action(IGG_ID, building_type, building_id)
        pkt = self.codec.encode(0x0CED, data)
        with self.lock:
            self.gs_sock.sendall(pkt)
            self.total_sent += len(pkt)
        log(f"  -> ACTION_BUILD 0x0CED ({len(pkt)}B)")
        return True

    def send_gather(self, march_slot=1, troop_count=2):
        if not self.codec:
            log("Cannot send: no server key!", "ERROR")
            return False
        data = build_gather_action(IGG_ID, march_slot=march_slot, troop_count=troop_count)
        pkt = self.codec.encode(0x0CE8, data)
        with self.lock:
            self.gs_sock.sendall(pkt)
            self.total_sent += len(pkt)
        log(f"  -> ACTION_GATHER 0x0CE8 ({len(pkt)}B)")
        return True

    def send_raw(self, opcode, payload=b''):
        pkt = build_packet(opcode, payload)
        with self.lock:
            self.gs_sock.sendall(pkt)
            self.total_sent += len(pkt)
        log(f"  -> 0x{opcode:04X} {opname(opcode)} ({len(pkt)}B)")

    # ---- Full Start ----
    def start(self):
        log("=" * 60)
        log("IGG Conquerors - COMPLETE BOT")
        log("=" * 60)
        log(f"IGG ID: {IGG_ID}")
        log(f"Access Key: {self.access_key}")
        log(f"Gateway Token: {self.token.hex()}")

        self.connect_gateway()
        self.connect_game_server()
        self.receive_game_data()

        log("")
        log("=== GAME STATE ===")
        log(self.game_state.summary())
        log("")

        self.running = True
        threading.Thread(target=self._heartbeat_loop, daemon=True).start()
        threading.Thread(target=self._listener_loop, daemon=True).start()

        log("=" * 60)
        log("BOT ONLINE - Ready for commands")
        log("=" * 60)
        log("")
        log("Commands:")
        log("  train          - Send train action (0x0CEB)")
        log("  build          - Send build action (0x0CED)")
        log("  gather         - Send gather action (0x0CE8)")
        log("  status         - Connection stats")
        log("  state          - Game state (player, resources)")
        log("  packets        - Unique opcode list")
        log("  raw <hex_op>   - Send raw unencrypted packet")
        log("  quit           - Disconnect")
        log("")
        return True

    def interactive(self):
        try:
            while self.running and self.connected:
                try:
                    cmd = input("bot> ").strip().lower()
                except EOFError:
                    break

                if not cmd:
                    continue

                parts = cmd.split(None, 1)
                command = parts[0]
                args = parts[1] if len(parts) > 1 else ""

                if command in ("quit", "exit"):
                    break
                elif command == "train":
                    self.send_train()
                elif command == "build":
                    self.send_build()
                elif command == "gather":
                    self.send_gather()
                elif command == "status":
                    elapsed = time.time() - self.start_time
                    log(f"Connected: {self.connected}")
                    log(f"Uptime: {elapsed:.0f}s ({elapsed/60:.1f}m)")
                    log(f"Sent: {self.total_sent} bytes | Recv: {self.total_recv} bytes")
                    log(f"Server: {self.game_ip}:{self.game_port}")
                    log(f"Server Key: {'0x'+format(self.game_state.server_key,'08x') if self.game_state.server_key else 'N/A'}")
                elif command == "state":
                    log("=== GAME STATE ===")
                    log(self.game_state.summary())
                elif command == "packets":
                    log("Unique opcodes received:")
                    for op in sorted(self.game_state.raw_packets.keys()):
                        cnt = len(self.game_state.raw_packets[op])
                        log(f"  0x{op:04X} {opname(op):25s} x{cnt}")
                elif command == "raw":
                    try:
                        raw_parts = args.split(None, 1)
                        op = int(raw_parts[0], 16)
                        payload = bytes.fromhex(raw_parts[1]) if len(raw_parts) > 1 else b''
                        self.send_raw(op, payload)
                    except Exception as e:
                        log(f"Raw send error: {e}", "ERROR")
                elif command == "help":
                    log("train, build, gather, status, state, packets, raw <op> [hex], quit")
                else:
                    log(f"Unknown command: {command}. Type 'help'.")
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
        log(f"Final: sent {self.total_sent}B, recv {self.total_recv}B")
        log("Bot stopped.")

# ╔══════════════════════════════════════════════════════════════╗
# ║                          MAIN                               ║
# ╚══════════════════════════════════════════════════════════════╝

def main():
    global LOG_FILE
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bot_session.log")
    LOG_FILE = open(log_path, "w", encoding="utf-8")

    access_key = None

    # Parse arguments
    if "--http" in sys.argv:
        access_key = http_login()
        if not access_key:
            log("HTTP login failed! Try --adb or --key instead.", "ERROR")
            LOG_FILE.close()
            return

    elif "--adb" in sys.argv:
        access_key = extract_key_from_adb()
        if not access_key:
            log("ADB extraction failed! Using stored key.", "WARN")
            access_key = STORED_ACCESS_KEY

    elif "--key" in sys.argv:
        idx = sys.argv.index("--key")
        if idx + 1 < len(sys.argv):
            access_key = sys.argv[idx + 1]
        else:
            log("--key requires a value", "ERROR")
            LOG_FILE.close()
            return

    if not access_key:
        access_key = STORED_ACCESS_KEY
        log(f"Using stored access key: {access_key}")

    if len(access_key) != 32:
        log(f"Invalid access key length: {len(access_key)} (need 32)", "ERROR")
        LOG_FILE.close()
        return

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

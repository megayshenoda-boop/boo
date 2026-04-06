"""
IGG Conquerors Bot - Packet I/O & Builders
============================================
Generic packet building/receiving + connection-specific packet builders.
"""
import socket
import struct
import time

from config import GAME_ID_HEX
from protocol import OP_HEARTBEAT


def build_packet(opcode, payload=b''):
    """Build a generic packet: [2B LE length][2B LE opcode][payload]"""
    length = 4 + len(payload)
    return struct.pack('<HH', length, opcode) + payload


def recv_packet(sock, timeout=10):
    """Receive a single packet from socket.
    Returns (opcode, payload, raw_bytes) or None on timeout/error."""
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
    except Exception:
        return None


def recv_all_packets(sock, timeout=5):
    """Receive all available packets within timeout.
    Returns list of (opcode, payload, raw_bytes)."""
    packets = []
    deadline = time.time() + timeout
    while time.time() < deadline:
        remaining = max(0.1, deadline - time.time())
        pkt = recv_packet(sock, timeout=remaining)
        if pkt is None:
            break
        packets.append(pkt)
    return packets


# ══════════════════════════════════════════════════════════════
#  CONNECTION PACKET BUILDERS
# ══════════════════════════════════════════════════════════════

def build_gateway_auth(igg_id, token, world_id):
    """Build 0x000B Gateway authentication packet (79 bytes).
    Token is 32-byte XOR-derived gateway token."""
    pkt = struct.pack('<HH', 79, 0x000B)
    pkt += struct.pack('<I', 1)           # version
    pkt += struct.pack('<I', 0)           # padding
    pkt += struct.pack('<I', igg_id)
    pkt += struct.pack('<I', 0)           # padding
    pkt += struct.pack('<H', 32)          # token length
    pkt += token                           # 32 bytes
    pkt += struct.pack('<I', 0)           # padding
    pkt += struct.pack('<I', 2)           # platform = android
    pkt += struct.pack('<I', 0)           # padding
    pkt += struct.pack('<I', world_id)
    pkt += struct.pack('<I', GAME_ID_HEX)
    pkt += struct.pack('<I', 0)           # padding
    pkt += struct.pack('B', 1)            # tail
    return pkt


def build_game_login(igg_id, session_token):
    """Build 0x001F Game Server login packet (64 bytes)."""
    st = session_token.encode('ascii')
    pkt = struct.pack('<HH', 64, 0x001F)
    pkt += struct.pack('<I', 1)           # version
    pkt += struct.pack('<I', 0)           # padding
    pkt += struct.pack('<I', igg_id)
    pkt += struct.pack('<I', 0)           # padding
    pkt += struct.pack('<H', 32)          # token length
    pkt += st                              # 32 bytes session token
    pkt += bytes([0x0e])                   # marker
    pkt += struct.pack('<I', GAME_ID_HEX)
    pkt += struct.pack('<I', 0)           # padding
    pkt += bytes([0x00])                   # tail
    return pkt


def build_world_entry(igg_id):
    """Build 0x0021 World entry request packet (21 bytes)."""
    pkt = struct.pack('<HH', 21, 0x0021)
    pkt += struct.pack('<I', igg_id)
    pkt += struct.pack('<I', 0)           # padding
    pkt += bytes([0x0e])                   # marker
    pkt += struct.pack('<I', GAME_ID_HEX)
    pkt += bytes([0xb0, 0x02, 0x5c, 0x00])  # trailer
    return pkt


def build_heartbeat(ms_elapsed):
    """Build 0x0042 heartbeat packet."""
    payload = struct.pack('<II', ms_elapsed, 0)
    return build_packet(OP_HEARTBEAT, payload)


def parse_gateway_response(payload):
    """Parse 0x000C Gateway redirect response.
    Returns dict with: ip, port, token, status, world."""
    pos = 0
    struct.unpack('<I', payload[pos:pos+4])[0]  # igg_id (ignored)
    pos += 4
    pos += 4  # padding
    ip_len = struct.unpack('<H', payload[pos:pos+2])[0]
    pos += 2
    if ip_len <= 0 or ip_len > 50:
        return None
    redirect_ip = payload[pos:pos+ip_len].decode('ascii')
    pos += ip_len
    redirect_port = struct.unpack('<H', payload[pos:pos+2])[0]
    pos += 2
    tok_len = struct.unpack('<H', payload[pos:pos+2])[0]
    pos += 2
    session_token = payload[pos:pos+tok_len].decode('ascii')
    pos += tok_len
    status = payload[pos] if pos < len(payload) else -1
    pos += 1
    world_id = struct.unpack('<I', payload[pos:pos+4])[0] if pos + 4 <= len(payload) else -1
    return {
        'ip': redirect_ip, 'port': redirect_port,
        'token': session_token, 'status': status, 'world': world_id
    }

"""
IGG Conquerors Bot - Gateway Connection
=========================================
TCP connection to Gateway server for authentication and redirect.
"""
import socket
from datetime import datetime

from config import GATEWAY_IP, GATEWAY_PORT, CQ_XOR_KEY
from packets import build_gateway_auth, recv_packet, parse_gateway_response
from protocol import OP_GATEWAY_REDIRECT


def _log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{ts}] [{level}] {msg}")


def derive_gateway_token(access_key):
    """Derive gateway token: XOR(access_key_ascii, "CQ_secret" repeating to 32)."""
    xor_key = CQ_XOR_KEY.encode('ascii')
    return bytes(a ^ b for a, b in zip(access_key.encode('ascii'), xor_key))


def connect_gateway(igg_id, access_key, world_id,
                    gateway_ip=None, gateway_port=None):
    """Connect to Gateway, authenticate, get game server redirect.

    Returns dict: {ip, port, token, status, world}
    Raises Exception on failure.
    """
    gateway_ip = gateway_ip or GATEWAY_IP
    gateway_port = gateway_port or GATEWAY_PORT

    token = derive_gateway_token(access_key)
    _log(f"Connecting to Gateway {gateway_ip}:{gateway_port}...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    try:
        sock.connect((gateway_ip, gateway_port))
        pkt = build_gateway_auth(igg_id, token, world_id)
        sock.sendall(pkt)
        _log(f"Sent 0x000B ({len(pkt)}B)")

        result = recv_packet(sock, timeout=10)
        if result is None:
            raise Exception("No response from Gateway")

        opcode, payload, raw = result
        if opcode != OP_GATEWAY_REDIRECT:
            raise Exception(f"Expected 0x000C, got 0x{opcode:04X}")

        info = parse_gateway_response(payload)
        if info is None or not info['ip']:
            raise Exception("Gateway returned empty redirect (access key expired?)")

        _log(f"Gateway OK -> {info['ip']}:{info['port']}, world={info['world']}")
        return info
    finally:
        sock.close()

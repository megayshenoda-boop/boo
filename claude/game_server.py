"""
IGG Conquerors Bot - Game Server Connection
=============================================
Manages TCP connection to the game server with heartbeat and listener threads.
"""
import socket
import struct
import time
import random
import threading
from datetime import datetime

from config import HEARTBEAT_INTERVAL
from protocol import OP_GAME_LOGIN_OK, OP_HEARTBEAT, opname
from packets import (
    build_packet, build_game_login, build_world_entry,
    build_heartbeat, recv_packet, recv_all_packets,
)
from codec import CMsgCodec
from game_state import GameState


def _log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{ts}] [{level}] {msg}")


class GameConnection:
    """Manages TCP connection to the game server."""

    def __init__(self, igg_id, game_ip, game_port, session_token):
        self.igg_id = igg_id
        self.game_ip = game_ip
        self.game_port = game_port
        self.session_token = session_token
        self.gs_sock = None
        self.connected = False
        self.running = False
        self.start_time = 0
        self.game_state = GameState()
        self.codec = None
        self.lock = threading.Lock()
        self.total_sent = 0
        self.total_recv = 0
        self._callbacks = []
        self._callback_lock = threading.Lock()
        self.heartbeat_paused = False

    def on_packet(self, callback):
        """Register callback for incoming packets: callback(opcode, payload)."""
        with self._callback_lock:
            self._callbacks.append(callback)

    def remove_callback(self, callback):
        """Thread-safe callback removal."""
        with self._callback_lock:
            if callback in self._callbacks:
                self._callbacks.remove(callback)

    def connect(self):
        """Full connection flow: login -> world entry -> receive game data -> extract server key."""
        _log(f"Connecting to Game Server {self.game_ip}:{self.game_port}...")
        self.gs_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gs_sock.settimeout(10)
        self.gs_sock.connect((self.game_ip, self.game_port))

        # Send 0x001F login
        pkt = build_game_login(self.igg_id, self.session_token)
        self.gs_sock.sendall(pkt)
        self.total_sent += len(pkt)
        _log(f"Sent 0x001F ({len(pkt)}B)")

        result = recv_packet(self.gs_sock, timeout=10)
        if result is None:
            raise Exception("No 0x0020 response")
        opcode, payload, raw = result
        self.total_recv += len(raw)
        if opcode != OP_GAME_LOGIN_OK:
            raise Exception(f"Expected 0x0020, got 0x{opcode:04X}")
        if not payload or payload[0] != 1:
            raise Exception(f"Login rejected: status={payload[0] if payload else -1}")
        _log("Login OK (status=1)")

        # Send 0x0021 world entry
        pkt = build_world_entry(self.igg_id)
        self.gs_sock.sendall(pkt)
        self.total_sent += len(pkt)
        _log(f"Sent 0x0021 ({len(pkt)}B)")
        self.start_time = time.time()
        self.connected = True

        # Receive initial game data flood
        _log("Receiving initial game data...")
        packets = recv_all_packets(self.gs_sock, timeout=10)
        for op, pl, raw in packets:
            self.total_recv += len(raw)
            self.game_state.update(op, pl)
            for cb in self._callbacks:
                cb(op, pl)
        _log(f"Received {len(packets)} packets, {self.total_recv} bytes")

        # If server key not found, request more data
        if self.game_state.server_key is None:
            _log("Server key not found, requesting more data...")
            for op in [0x0840, 0x17D4, 0x0709, 0x0674, 0x0767, 0x0769]:
                self.gs_sock.sendall(build_packet(op))
            for sub_id in [0x0193, 0x0198, 0x019D]:
                self.gs_sock.sendall(build_packet(0x099D, struct.pack('<I', sub_id)))
            more = recv_all_packets(self.gs_sock, timeout=8)
            for op, pl, raw in more:
                self.total_recv += len(raw)
                self.game_state.update(op, pl)

        # Initialize codec if server key found
        if self.game_state.server_key:
            self.codec = CMsgCodec.from_u32(self.game_state.server_key)
            _log(f"CMsgCodec ready (key 0x{self.game_state.server_key:08x})")
        else:
            _log("WARNING: Server key not found! Encrypted actions will not work.", "WARN")

        # Start background threads
        self.running = True
        threading.Thread(target=self._heartbeat_loop, daemon=True).start()
        threading.Thread(target=self._listener_loop, daemon=True).start()

        try:
            pname = self.game_state.player_name or 'unknown'
            _log(f"Connected! Player: {pname}")
        except Exception:
            _log("Connected! Player: (non-ASCII name)")
        return True

    def send(self, packet_bytes):
        """Send a pre-built packet (thread-safe)."""
        with self.lock:
            self.gs_sock.sendall(packet_bytes)
            self.total_sent += len(packet_bytes)
        opcode = struct.unpack('<H', packet_bytes[2:4])[0]
        _log(f"  -> {opname(opcode)} ({len(packet_bytes)}B)")

    def _heartbeat_loop(self):
        while self.running and self.connected:
            # Jitter ±0.5s to avoid bot detection (report 62)
            jitter = random.uniform(-0.5, 0.5)
            time.sleep(HEARTBEAT_INTERVAL + jitter)
            if not self.running or not self.connected:
                break
            if self.heartbeat_paused:
                continue
            try:
                ms = int((time.time() - self.start_time) * 1000)
                pkt = build_heartbeat(ms)
                with self.lock:
                    self.gs_sock.sendall(pkt)
                    self.total_sent += len(pkt)
            except Exception as e:
                _log(f"Heartbeat failed: {e}", "ERROR")
                self.connected = False

    def _listener_loop(self):
        while self.running and self.connected:
            try:
                result = recv_packet(self.gs_sock, timeout=5)
                if result is None:
                    continue
                opcode, payload, raw = result
                self.total_recv += len(raw)
                self.game_state.update(opcode, payload)

                # Late server key extraction
                if self.game_state.server_key and not self.codec:
                    self.codec = CMsgCodec.from_u32(self.game_state.server_key)
                    _log(f"CMsgCodec now ready (key 0x{self.game_state.server_key:08x})")

                # Thread-safe callback iteration (report 62 fix)
                with self._callback_lock:
                    cbs = list(self._callbacks)
                for cb in cbs:
                    cb(opcode, payload)

                # Log non-spam packets
                if opcode not in (OP_HEARTBEAT, 0x036C, 0x0002):
                    _log(f"  <- {opname(opcode)} ({len(raw)}B)")
            except Exception as e:
                if self.running:
                    _log(f"Listener error: {e}", "ERROR")
                    self.connected = False
                break

    def disconnect(self):
        """Graceful shutdown."""
        self.running = False
        self.connected = False
        if self.gs_sock:
            try:
                self.gs_sock.close()
            except Exception:
                pass
        _log(f"Disconnected. Sent {self.total_sent}B, Recv {self.total_recv}B")

    def status(self):
        """Connection stats dict."""
        elapsed = time.time() - self.start_time if self.start_time else 0
        return {
            'connected': self.connected,
            'uptime_seconds': int(elapsed),
            'server': f"{self.game_ip}:{self.game_port}",
            'total_sent': self.total_sent,
            'total_recv': self.total_recv,
            'server_key': f"0x{self.game_state.server_key:08x}" if self.game_state.server_key else None,
            'game_state': self.game_state.to_dict(),
        }

"""
gather_bot.py
=============
Standalone gather test - connects to game and sends a gather command.
Verified structure from 23 real PCAP decryptions (Mar 20-27, 2026).

Usage:
    python gather_bot.py <tile_x> <tile_y> [hero_id]
    python gather_bot.py 570 805          # hero 255
    python gather_bot.py 570 805 244      # hero 244

This file is self-contained and does NOT modify the claude/ directory.
"""
import sys
import os
import struct
import random
import time
import socket
import threading

# Add claude/ to path so we can use the existing modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'claude'))

from config import IGG_ID, WORLD_ID, STORED_ACCESS_KEY
from auth import http_login, extract_key_from_adb
from gateway import connect_gateway
from codec import CMsgCodec
from packets import build_packet, recv_packet, recv_all_packets, build_game_login, build_world_entry
from protocol import OP_GAME_LOGIN_OK, opname
from game_state import GameState


# ─────────────────────────────────────────────────────────────
# Verified packet builders (from 23 PCAP samples)
# ─────────────────────────────────────────────────────────────

OP_START_MARCH  = 0x0CE8   # gather/march
OP_ENABLE_VIEW  = 0x0CEB   # required prelude

MARCH_TYPE_GATHER = 0x1749  # constant in all 22 resource gather samples
MARCH_PURPOSE_GATHER = 0x04  # offset 22, resource gather
MARCH_PURPOSE_REBEL  = 0x02  # offset 22, rebel/monster attack


def build_gather(igg_id, codec, target_x, target_y, march_slot=1, hero_id=255):
    """
    Build 0x0CE8 gather march packet.

    Verified structure (46 bytes plaintext, from 23 PCAP decryptions):
      [0]     = march_slot (1-5)
      [1:4]   = nonce (3 random bytes, unique per march)
      [4:6]   = 0x1749 (march_type, u16 LE, CONSTANT for gather)
      [6:9]   = 0x00 × 3
      [9:11]  = tile_x (u16 LE)
      [11:13] = tile_y (u16 LE)
      [13]    = 0x01 (action_flag, CONSTANT)
      [14]    = hero_id (255 or 244)
      [15:18] = 0x00 × 3
      [18]    = 0xB6 (kingdom=182, CONSTANT)
      [19:22] = 0x00 × 3
      [22]    = 0x04 (march_purpose=gather, CONSTANT for resource)
      [23:33] = 0x00 × 10
      [33:37] = igg_id (u32 LE)
      [37:46] = 0x00 × 9
    """
    data = bytearray(46)
    data[0] = march_slot & 0xFF
    data[1:4] = os.urandom(3)                    # unique nonce
    struct.pack_into('<H', data, 4, MARCH_TYPE_GATHER)  # 0x1749
    struct.pack_into('<H', data, 9, target_x)
    struct.pack_into('<H', data, 11, target_y)
    data[13] = 0x01                               # action_flag
    data[14] = hero_id & 0xFF
    data[18] = 0xB6                               # kingdom
    data[22] = MARCH_PURPOSE_GATHER               # 0x04 = resource gather
    struct.pack_into('<I', data, 33, igg_id)
    return codec.encode(OP_START_MARCH, bytes(data))


def build_enable_view(igg_id, codec):
    """Build 0x0CEB prelude packet (required before gather)."""
    data = bytearray(10)
    data[0] = 0x01
    struct.pack_into('<I', data, 1, igg_id)
    data[9] = 0x01
    return codec.encode(OP_ENABLE_VIEW, bytes(data))


# ─────────────────────────────────────────────────────────────
# Minimal game connection (no background threads, just what we need)
# ─────────────────────────────────────────────────────────────

def log(msg):
    ts = time.strftime('%H:%M:%S')
    print(f"[{ts}] {msg}", flush=True)


def connect_and_gather(access_key, target_x, target_y, hero_id=255):
    """Full flow: gateway -> game server -> send gather -> wait for response."""

    # ── Step 1: Gateway ──────────────────────────────────────
    log("Connecting to gateway...")
    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    log(f"Gateway OK: game server = {gw['ip']}:{gw['port']}")

    # ── Step 2: Game server TCP ───────────────────────────────
    log(f"Connecting to game server {gw['ip']}:{gw['port']}...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((gw['ip'], gw['port']))

    # Send 0x001F login
    pkt = build_game_login(IGG_ID, gw['token'])
    sock.sendall(pkt)
    log(f"Sent 0x001F login ({len(pkt)}B)")

    # Wait for 0x0020 OK
    result = recv_packet(sock, timeout=10)
    if result is None or result[0] != OP_GAME_LOGIN_OK:
        raise Exception(f"Login failed: {result}")
    if not result[1] or result[1][0] != 1:
        raise Exception(f"Login rejected: status={result[1][0] if result[1] else -1}")
    log("Login OK")

    # Send 0x0021 world entry
    pkt = build_world_entry(IGG_ID)
    sock.sendall(pkt)
    log("Sent 0x0021 world entry")

    # ── Step 3: Receive initial flood, extract server key ─────
    log("Receiving game data...")
    gs = GameState()
    codec = None

    pkts = recv_all_packets(sock, timeout=8)
    for op, pl, raw in pkts:
        gs.update(op, pl)
    log(f"Received {len(pkts)} packets")

    if gs.server_key:
        codec = CMsgCodec.from_u32(gs.server_key)
        log(f"Server key: 0x{gs.server_key:08x}")
    else:
        # Request more data
        log("Key not found, requesting more data...")
        for op in [0x0840, 0x17D4, 0x0709, 0x0767, 0x0769]:
            sock.sendall(build_packet(op))
        more = recv_all_packets(sock, timeout=6)
        for op, pl, raw in more:
            gs.update(op, pl)
        if gs.server_key:
            codec = CMsgCodec.from_u32(gs.server_key)
            log(f"Server key: 0x{gs.server_key:08x}")
        else:
            raise Exception("Could not extract server key!")

    # ── Step 4: Start heartbeat thread ────────────────────────
    start_time = time.time()
    hb_running = [True]

    def heartbeat():
        while hb_running[0]:
            time.sleep(15)
            if not hb_running[0]: break
            try:
                ms = int((time.time() - start_time) * 1000)
                hb_pkt = build_packet(0x0042, struct.pack('<II', ms, 0))
                sock.sendall(hb_pkt)
            except Exception:
                break
    threading.Thread(target=heartbeat, daemon=True).start()

    # ── Step 5: Start listener thread (to catch 0x00B8) ───────
    received = []
    listen_running = [True]
    b8_event = threading.Event()

    def listener():
        while listen_running[0]:
            try:
                result = recv_packet(sock, timeout=2)
                if result is None:
                    continue
                op, pl, raw = result
                gs.update(op, pl)
                # Late key extraction
                if gs.server_key and not codec:
                    pass  # codec already set above
                # Log non-spam
                if op not in (0x0042, 0x036C, 0x0002):
                    log(f"  <- 0x{op:04X} ({len(raw)}B) {opname(op)}")
                if op == 0x00B8:
                    # Parse: [0]=count [1:5]=status_u32 [5]=action [6:10]=hero_u32
                    if len(pl) >= 10:
                        status = struct.unpack('<I', pl[1:5])[0]
                        hero_r = struct.unpack('<I', pl[6:10])[0]
                        log(f"  *** MARCH ACCEPTED! status={status} hero={hero_r} ***")
                    b8_event.set()
                    received.append(op)
                if op == 0x0071:
                    log(f"  *** MARCH STATE CONFIRMED (march started) ***")
                    received.append(op)
                if op == 0x007C:
                    log(f"  *** COLLECT STATE (troops arrived, collecting!) ***")
                    received.append(op)
            except Exception:
                break
    threading.Thread(target=listener, daemon=True).start()

    # Give listener a moment to settle
    time.sleep(0.5)

    # ── Step 6: Send gather sequence ──────────────────────────
    log(f"")
    log(f"Sending gather to tile=({target_x},{target_y}) hero={hero_id} slot=1")

    # 1. Enable view (prelude)
    ev_pkt = build_enable_view(IGG_ID, codec)
    sock.sendall(ev_pkt)
    log(f"  -> 0x0CEB enable_view ({len(ev_pkt)}B)")
    time.sleep(0.3)

    # 2. Gather march
    g_pkt = build_gather(IGG_ID, codec, target_x, target_y, march_slot=1, hero_id=hero_id)
    sock.sendall(g_pkt)
    log(f"  -> 0x0CE8 gather ({len(g_pkt)}B)")

    # Print payload for debug
    log(f"     encoded: {g_pkt[4:].hex()}")

    # ── Step 7: Wait for confirmation ─────────────────────────
    log(f"")
    log(f"Waiting for server response (up to 10s)...")
    got_accept = b8_event.wait(timeout=10)

    if got_accept:
        log(f"SUCCESS! Server accepted the march.")
        if 0x0071 in received:
            log(f"March confirmed active (0x0071 received)")
    else:
        log(f"TIMEOUT: No 0x00B8 received in 10s")
        log(f"  Possible reasons:")
        log(f"    1. Hero not available (already marching)")
        log(f"    2. Tile coordinates invalid")
        log(f"    3. No troops in formation")

    # Keep connection open briefly to catch any delayed responses
    time.sleep(3)

    hb_running[0] = False
    listen_running[0] = False
    sock.close()
    return got_accept


# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 3:
        print("Usage: python gather_bot.py <tile_x> <tile_y> [hero_id]")
        print("       hero_id: 255 (default) or 244")
        print()
        print("Examples:")
        print("  python gather_bot.py 570 805")
        print("  python gather_bot.py 570 805 244")
        print("  python gather_bot.py 650 576 255")
        sys.exit(1)

    tx = int(sys.argv[1])
    ty = int(sys.argv[2])
    hero = int(sys.argv[3]) if len(sys.argv) > 3 else 255

    # Use stored access key
    access_key = STORED_ACCESS_KEY
    if not access_key:
        print("No STORED_ACCESS_KEY in config.py - run HTTP login first")
        sys.exit(1)

    try:
        success = connect_and_gather(access_key, tx, ty, hero)
        sys.exit(0 if success else 1)
    except Exception as e:
        log(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

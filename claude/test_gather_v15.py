#!/usr/bin/env python3
"""
Gather Test v15 - Simplified, diagnostic approach
==================================================
1. Extract castle coords from init data
2. View our area, find tiles from 0x0076/0x0077
3. Try gather with AND without 0x0323
4. Log everything
"""
import sys, time, struct, random, subprocess, socket, os
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from codec import CMsgCodec
from packets import build_packet, build_game_login, build_world_entry, recv_packet
from protocol import OP_ENABLE_VIEW, OP_START_MARCH
from game_state import GameState

KINGDOM = 182
MARCH_TYPE = 0x1749

def log(msg):
    try:
        print(f"[{time.strftime('%H:%M:%S')}] {msg}")
    except UnicodeEncodeError:
        print(f"[{time.strftime('%H:%M:%S')}] {msg.encode('ascii', 'replace').decode()}")

def node_login():
    for attempt in range(3):
        try:
            result = subprocess.run(
                ['node', r'D:\CascadeProjects\lords_bot\http_login.mjs', EMAIL, PASSWORD, str(IGG_ID)],
                capture_output=True, text=True, timeout=30)
            key = result.stdout.strip()
            if len(key) == 32: return key
        except: pass
        if attempt < 2: time.sleep(3)
    return None

def recv_flood(sock, timeout=3):
    packets = []
    deadline = time.time() + timeout
    while time.time() < deadline:
        remaining = max(0.1, deadline - time.time())
        sock.settimeout(remaining)
        try:
            header = b''
            while len(header) < 4:
                chunk = sock.recv(4 - len(header))
                if not chunk: return packets
                header += chunk
            pkt_len, opcode = struct.unpack('<HH', header)
            payload_len = pkt_len - 4
            if payload_len < 0 or payload_len > 100000: return packets
            payload = b''
            while len(payload) < payload_len:
                chunk = sock.recv(payload_len - len(payload))
                if not chunk: return packets
                payload += chunk
            packets.append((opcode, payload))
        except socket.timeout: break
        except: break
    return packets

def get_castle_coords(init_pkts):
    """Try to find castle X,Y from 0x0038 attribute data."""
    for op, pl in init_pkts:
        if op == 0x0038 and len(pl) > 50:
            ec = struct.unpack('<H', pl[0:2])[0]
            attrs = {}
            for idx in range(ec):
                off = 2 + idx * 12
                if off + 12 > len(pl): break
                fid = struct.unpack('<I', pl[off:off+4])[0]
                val = struct.unpack('<I', pl[off+4:off+8])[0]
                attrs[fid] = val
            # Field IDs for castle X,Y (common: 0x01=x, 0x02=y or similar)
            # Let's dump all to find it
            log(f"  0x0038 has {len(attrs)} attributes")
            # Castle coords are often in low field IDs
            for fid in sorted(attrs.keys())[:30]:
                val = attrs[fid]
                if 100 < val < 2000:  # Likely coordinate range
                    log(f"    field 0x{fid:02X}={val} (possible coord)")
            return attrs
    return {}

def find_resource_tiles(packets):
    """Parse 0x0077 tile data to find resource tiles."""
    tiles = []
    for op, pl in packets:
        if op == 0x0077 and len(pl) >= 10:
            # 0x0077 contains tile/object data - try to extract coords
            # Format varies but typically has x,y coordinates
            tiles.append(pl)
    return tiles

def main():
    log("=== GATHER TEST v15 ===")

    access_key = node_login()
    if not access_key:
        log("LOGIN FAILED!"); return

    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    log(f"Server: {gw['ip']}:{gw['port']}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((gw['ip'], gw['port']))

    sock.sendall(build_game_login(IGG_ID, gw['token']))
    result = recv_packet(sock, timeout=10)
    if result is None or result[0] != 0x0020:
        log("Login failed"); sock.close(); return
    log("Login OK")

    sock.sendall(build_world_entry(IGG_ID))
    t0 = time.time()

    init_pkts = recv_flood(sock, timeout=6)
    log(f"{len(init_pkts)} init packets")

    gs = GameState()
    for op, pl in init_pkts:
        gs.update(op, pl)
    log(f"Player: {gs.player_name}, Power: {gs.power}")
    if not gs.server_key:
        log("No server key!"); sock.close(); return
    codec = CMsgCodec.from_u32(gs.server_key)
    log(f"Server key: 0x{gs.server_key:08X}")

    # Find castle coords
    attrs = get_castle_coords(init_pkts)

    # Check for march slots info
    for op, pl in init_pkts:
        if op == 0x0768:
            log(f"  MARCH_SLOT 0x0768 ({len(pl)}B): {pl.hex()}")
        if op == 0x0769:
            log(f"  MARCH_QUEUE 0x0769 ({len(pl)}B): {pl.hex()}")
        if op == 0x0071:
            log(f"  EXISTING MARCH 0x0071 ({len(pl)}B): {pl[:30].hex()}")

    # Setup
    log("\nSetup...")
    for opcode in [0x0840, 0x17D4, 0x0AF2, 0x0245]:
        sock.sendall(build_packet(opcode))
    formation = bytes.fromhex("0a00ba0b00000b040000d8070000e3070000f103000000040000f8030000d90700000104000016040000")
    sock.sendall(build_packet(0x0834, formation))
    sock.sendall(build_packet(0x0709))
    sock.sendall(build_packet(0x0A2C))
    time.sleep(1)
    recv_flood(sock, timeout=2)

    # Enable view
    log("Enable view...")
    ev = bytearray(10)
    ev[0] = 0x01
    struct.pack_into('<I', ev, 1, IGG_ID)
    ev[9] = 0x01
    sock.sendall(codec.encode(OP_ENABLE_VIEW, bytes(ev)))
    time.sleep(1)
    recv_flood(sock, timeout=2)

    # Try to find castle position from 0x0038 fields
    castle_x = attrs.get(0x01, 0)
    castle_y = attrs.get(0x02, 0)
    if castle_x == 0 or castle_y == 0:
        # Try other common field IDs
        for fx, fy in [(0x03, 0x04), (0x05, 0x06), (0x0A, 0x0B)]:
            cx = attrs.get(fx, 0)
            cy = attrs.get(fy, 0)
            if 100 < cx < 1500 and 100 < cy < 1500:
                castle_x, castle_y = cx, cy
                log(f"  Castle from fields 0x{fx:02X},0x{fy:02X}: ({cx},{cy})")
                break

    if castle_x == 0:
        castle_x, castle_y = 579, 830
        log(f"  No castle coords found, using PCAP default: ({castle_x},{castle_y})")

    # View our area
    log(f"Viewing area ({castle_x},{castle_y})...")
    sock.sendall(build_packet(0x006E, struct.pack('<HHB', castle_x, castle_y, 1)))
    time.sleep(2)
    view_pkts = recv_flood(sock, timeout=3)
    log(f"  Got {len(view_pkts)} view packets")
    tile_data = find_resource_tiles(view_pkts)
    log(f"  0x0077 tile packets: {len(tile_data)}")

    # Search for resource
    log("Searching for resource tile...")
    # Try different search types
    for search_payload in [
        bytes.fromhex("01040003"),  # food lv3
        bytes.fromhex("01030003"),  # food lv3 variant
        bytes.fromhex("01020003"),  # food lv3 variant
        bytes.fromhex("01010001"),  # any lv1
    ]:
        sock.sendall(build_packet(0x033E, search_payload))
        time.sleep(1)
        sp = recv_flood(sock, timeout=2)
        for op, pl in sp:
            if op == 0x033F and len(pl) >= 5:
                rtype = pl[0]
                tx = struct.unpack('<H', pl[1:3])[0]
                ty = struct.unpack('<H', pl[3:5])[0]
                log(f"  Search {search_payload.hex()}: type={rtype} ({tx},{ty})")
                if tx > 0 and ty > 0:
                    target_x, target_y = tx, ty
                    break
        else:
            continue
        break
    else:
        # No search worked, use hardcoded
        target_x, target_y = 570, 805
        log(f"  All searches failed! Using hardcoded ({target_x},{target_y})")

    # View target
    sock.sendall(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 1)))
    time.sleep(2)
    target_view = recv_flood(sock, timeout=3)
    log(f"  Target view: {len(target_view)} packets")
    for op, pl in target_view:
        if op == 0x0077:
            log(f"    0x0077 ({len(pl)}B)")

    # Heartbeat
    ms = int((time.time() - t0) * 1000)
    sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
    time.sleep(1)
    hb = recv_flood(sock, timeout=2)
    alive = any(op == 0x0042 for op, _ in hb)
    log(f"Alive: {'YES' if alive else 'NO'}")
    if not alive:
        sock.close(); return

    # ════════════════════════════════════════
    # GATHER - Try WITHOUT 0x0323 first (it worked before = got ACK)
    # ════════════════════════════════════════
    log(f"\n{'='*50}")
    log(f"GATHER to ({target_x},{target_y})")
    log(f"{'='*50}")

    # Build march plaintext - match PCAP exactly
    plain = bytearray(46)
    plain[0] = 1  # slot 1
    plain[1:4] = os.urandom(3)
    struct.pack_into('<H', plain, 4, MARCH_TYPE)
    struct.pack_into('<H', plain, 9, target_x)
    struct.pack_into('<H', plain, 11, target_y)
    plain[13] = 0x01
    plain[14] = 0xFF  # hero 255
    plain[18] = KINGDOM & 0xFF
    plain[22] = 0x04
    struct.pack_into('<I', plain, 33, IGG_ID)
    log(f"  Plain: {plain.hex()}")

    gather_pkt = codec.encode(OP_START_MARCH, bytes(plain))
    sock.sendall(gather_pkt)
    log(f"  Sent 0x0CE8 ({len(gather_pkt)}B)")

    # Wait and log EVERYTHING
    time.sleep(3)
    resp = recv_flood(sock, timeout=8)
    log(f"\nAll responses ({len(resp)}):")
    for op, pl in resp:
        if op == 0x0071:
            log(f"  *** 0x0071 MARCH STATE ({len(pl)}B): {pl[:40].hex()} ***")
        elif op == 0x076C:
            log(f"  *** 0x076C MARCH START ({len(pl)}B) ***")
        elif op == 0x0037:
            status = struct.unpack('<I', pl[8:12])[0] if len(pl) >= 12 else -1
            log(f"  0x0037: sub=0x{pl[0]:02X} status={status} full={pl.hex()}")
        elif op == 0x00B8:
            log(f"  0x00B8 ACK: {pl.hex()}")
        elif op in (0x0042, 0x036C):
            pass  # skip heartbeat/sync
        else:
            log(f"  0x{op:04X} ({len(pl)}B): {pl[:20].hex() if len(pl) > 0 else 'empty'}")

    # Extended wait
    got_march = False
    for i in range(8):
        pkts = recv_flood(sock, timeout=5)
        for op, pl in pkts:
            if op == 0x0071:
                got_march = True
                log(f"  *** MARCH! 0x0071 ({len(pl)}B) ***")
            elif op == 0x076C:
                got_march = True
                log(f"  *** START! 0x076C ({len(pl)}B) ***")
            elif op == 0x0037:
                status = struct.unpack('<I', pl[8:12])[0] if len(pl) >= 12 else -1
                log(f"  0x0037: status={status}")
        if got_march:
            break
        ms = int((time.time() - t0) * 1000)
        try:
            sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
        except:
            log("Connection lost!"); break

    log(f"\n{'='*50}")
    log(f"MARCH: {'YES!!!' if got_march else 'NO'}")
    log(f"{'='*50}")
    sock.close()

if __name__ == '__main__':
    main()

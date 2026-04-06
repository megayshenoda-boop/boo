"""
test_gather_now.py - Live gather test
Verified structure from 23 PCAP decryptions (Mar 20-27, 2026).
"""
import sys, time, struct, subprocess, random, socket
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from codec import CMsgCodec
from packets import build_packet, build_game_login, build_world_entry, recv_packet, recv_all_packets
from game_state import GameState
from protocol import OP_ENABLE_VIEW, OP_START_MARCH, opname

# Verified from 23 PCAPs
KINGDOM    = 182    # 0xB6
MARCH_TYPE = 0x1749
FORMATION  = bytes.fromhex("0a00ba0b00000b040000d8070000e3070000f103000000040000f8030000d90700000104000016040000")
TROOPS     = [0x0193, 0x0195, 0x0196, 0x0197, 0x0198, 0x0199, 0x019A, 0x019B]

def log(msg): print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

def fresh_login():
    log("HTTP login...")
    r = subprocess.run(
        ['node', r'D:\CascadeProjects\lords_bot\http_login.mjs', EMAIL, PASSWORD, str(IGG_ID)],
        capture_output=True, text=True, timeout=30
    )
    key = r.stdout.strip()
    if len(key) == 32:
        log(f"  Key: {key[:8]}...")
        return key
    log(f"  FAILED: {r.stderr[:100]}")
    return None

def recv_flood(sock, timeout=4):
    pkts = []
    t = time.time() + timeout
    while time.time() < t:
        sock.settimeout(max(0.2, t - time.time()))
        try:
            hdr = b''
            while len(hdr) < 4:
                c = sock.recv(4 - len(hdr))
                if not c: return pkts
                hdr += c
            plen, op = struct.unpack('<HH', hdr)
            rem = plen - 4
            pl = b''
            while len(pl) < rem:
                c = sock.recv(rem - len(pl))
                if not c: return pkts
                pl += c
            pkts.append((op, pl))
        except socket.timeout: break
        except: break
    return pkts

def build_gather(tile_x, tile_y, hero_id=255, slot=1):
    """46-byte plaintext verified from 23 PCAPs."""
    p = bytearray(46)
    p[0] = slot
    p[1], p[2], p[3] = random.randint(0,255), random.randint(0,255), random.randint(0,255)
    struct.pack_into('<H', p, 4, MARCH_TYPE)   # 0x1749
    struct.pack_into('<H', p, 9,  tile_x)
    struct.pack_into('<H', p, 11, tile_y)
    p[13] = 0x01                               # action flag
    p[14] = hero_id & 0xFF
    p[18] = KINGDOM                            # 0xB6
    p[22] = 0x04                               # resource gather
    struct.pack_into('<I', p, 33, IGG_ID)
    return bytes(p)

def main():
    hero   = int(sys.argv[1]) if len(sys.argv) > 1 else 255
    tile_x = int(sys.argv[2]) if len(sys.argv) > 2 else None
    tile_y = int(sys.argv[3]) if len(sys.argv) > 3 else None

    log(f"=== GATHER NOW | hero={hero} tile={f'({tile_x},{tile_y})' if tile_x else 'auto'} ===")

    # 1. Login
    key = fresh_login()
    if not key: return

    # 2. Gateway
    gw = connect_gateway(IGG_ID, key, WORLD_ID)
    log(f"Game server: {gw['ip']}:{gw['port']}")

    # 3. Connect
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((gw['ip'], gw['port']))

    sock.sendall(build_game_login(IGG_ID, gw['token']))
    r = recv_packet(sock, timeout=10)
    assert r and r[0] == 0x0020 and r[1][0] == 1, f"Login fail: {r}"
    log("Login OK")

    sock.sendall(build_world_entry(IGG_ID))
    t0 = time.time()

    # 4. Init flood + server key
    gs = GameState()
    for op, pl, _ in recv_all_packets(sock, timeout=6):
        gs.update(op, pl)
    if not gs.server_key:
        for op in [0x0840, 0x17D4, 0x0709, 0x0767, 0x0769]:
            sock.sendall(build_packet(op))
        for op, pl, _ in recv_all_packets(sock, timeout=5):
            gs.update(op, pl)
    assert gs.server_key, "No server key!"
    codec = CMsgCodec.from_u32(gs.server_key)
    log(f"Server key: 0x{gs.server_key:08X}")

    # 5. Setup sequence (from PCAP)
    sock.sendall(build_packet(0x0840))
    sock.sendall(build_packet(0x0245))
    sock.sendall(build_packet(0x0834, FORMATION))
    sock.sendall(build_packet(0x0709))
    sock.sendall(build_packet(0x0A2C))
    for tid in TROOPS:
        sock.sendall(build_packet(0x099D, struct.pack('<I', tid)))
    sock.sendall(build_packet(0x0767))
    sock.sendall(build_packet(0x0769))
    log("Setup sent")
    recv_flood(sock, 2)

    # 6. Enable view + source tile
    ev = bytearray(10); ev[0]=0x01; struct.pack_into('<I', ev, 1, IGG_ID); ev[9]=0x01
    sock.sendall(codec.encode(OP_ENABLE_VIEW, bytes(ev)))
    sock.sendall(build_packet(0x006E, bytes.fromhex("43023e0301")))  # source

    # 7. Find target tile (auto-search or manual)
    if not tile_x:
        sock.sendall(build_packet(0x033E, bytes([0x01, 0x04, 0x00, 0x03])))
        for op, pl in recv_flood(sock, 4):
            if op == 0x033F and len(pl) >= 5:
                tile_x = struct.unpack('<H', pl[1:3])[0]
                tile_y = struct.unpack('<H', pl[3:5])[0]
                log(f"Search result: ({tile_x},{tile_y})")
                break
    if not tile_x:
        tile_x, tile_y = 570, 805
        log(f"Fallback tile: ({tile_x},{tile_y})")

    sock.sendall(build_packet(0x006E, struct.pack('<HHB', tile_x, tile_y, 0x01)))
    log(f"Target: ({tile_x},{tile_y})")

    # Heartbeat
    ms = int((time.time()-t0)*1000)
    sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
    recv_flood(sock, 2)

    # 8. 0x0323 hero select (present in ALL gather PCAPs before 0x0CE8)
    # payload: [0x00, slot, 0x00, hero_id, 0x00, 0x00, 0x00]
    slot = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    hero_sel = bytes([0x00, slot, 0x00, hero & 0xFF, 0x00, 0x00, 0x00])
    sock.sendall(build_packet(0x0323, hero_sel))
    log(f"Sent 0x0323 hero_select: {hero_sel.hex()}")
    time.sleep(0.3)

    # 9. GATHER
    plain = build_gather(tile_x, tile_y, hero_id=hero, slot=slot)
    log(f"0x0CE8 plain: {plain.hex()}")
    sock.sendall(codec.encode(OP_START_MARCH, plain))
    log("Sent 0x0CE8 - waiting...")

    # 9. Wait for response (30s)
    b8=False; b8_ok=False; got71=False; got76c=False; got37=False; got79=False
    deadline = time.time() + 30
    while time.time() < deadline:
        pkts = recv_flood(sock, 3)
        if not pkts:
            ms = int((time.time()-t0)*1000)
            sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
            continue
        for op, pl in pkts:
            if op in (0x0042, 0x036C, 0x0002): continue
            log(f"  <- 0x{op:04X} ({len(pl)}B): {pl[:24].hex()}")
            if op == 0x00B8:
                b8=True
                if len(pl)>=10:
                    st=struct.unpack('<I',pl[1:5])[0]; hr=struct.unpack('<I',pl[6:10])[0]
                    b8_ok=(st==1)
                    log(f"     MARCH_ACCEPT status={st} hero={hr} {'OK' if b8_ok else 'FAIL'}")
            elif op == 0x0071: got71=True; log("     MARCH_STATE!")
            elif op == 0x076C: got76c=True; log("     MARCH_BUNDLE!")
            elif op == 0x0037:
                got37=True
                if len(pl)>=8:
                    mid=struct.unpack('<I',pl[4:8])[0]
                    log(f"     MARCH_ID=0x{mid:08X} ({mid})")
            elif op == 0x0079: got79=True; log("     MARCH_MOVE (troops on map!)")
            elif op == 0x0033: log(f"     SYNC_ATTR: {pl.hex()}")
        if got71 or got76c or (b8_ok and got79):
            break

    log("="*50)
    log(f"B8={b8}(ok={b8_ok}) 0x0071={got71} 0x076C={got76c} march_id={got37} march_move={got79}")
    if got76c or got71:    log(">>> SUCCESS! (full chain)")
    elif b8_ok and got79:  log(">>> SUCCESS! (B8+move = march active)")
    elif b8_ok and got37:  log(">>> SUCCESS! (B8+march_id = march started)")
    elif b8_ok:            log(">>> PARTIAL - B8 accepted, wait longer?")
    else:                  log(">>> FAILED - no response")
    log("="*50)
    sock.close()

if __name__ == '__main__':
    main()

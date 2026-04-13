#!/usr/bin/env python3
"""
Gather Debug - Check alive before/after, find valid resource tiles, try different slots.
"""
import sys, time, struct, random, subprocess, socket, threading
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from codec import CMsgCodec
from packets import build_packet, build_game_login, build_world_entry

MARCH_TYPE = 0x1749
KINGDOM = 182

def log(msg):
    ts = time.time()
    ms = int((ts % 1) * 1000)
    print(f"[{time.strftime('%H:%M:%S')}.{ms:03d}] {msg}", flush=True)

def node_login():
    r = subprocess.run(
        ['node', r'D:\CascadeProjects\lords_bot\http_login.mjs', EMAIL, PASSWORD, str(IGG_ID)],
        capture_output=True, text=True, timeout=30, encoding='utf-8', errors='replace'
    )
    key = r.stdout.strip()
    return key if len(key) == 32 else None

class PacketReader:
    def __init__(self, sock):
        self.sock = sock
        self.buf = b''

    def read_all(self, timeout=5):
        pkts = []
        deadline = time.time() + timeout
        while time.time() < deadline:
            self.sock.settimeout(max(0.05, deadline - time.time()))
            try:
                chunk = self.sock.recv(65536)
                if not chunk: break
                self.buf += chunk
            except socket.timeout:
                pass
            while len(self.buf) >= 4:
                pkt_len = struct.unpack('<H', self.buf[0:2])[0]
                if pkt_len < 4 or pkt_len > 100000:
                    self.buf = self.buf[1:]
                    continue
                if len(self.buf) < pkt_len: break
                op = struct.unpack('<H', self.buf[2:4])[0]
                pl = self.buf[4:pkt_len]
                pkts.append((op, pl))
                self.buf = self.buf[pkt_len:]
        return pkts

def extract_server_key(packets):
    for op, pl in packets:
        if op == 0x0038 and len(pl) > 100:
            count = struct.unpack('<H', pl[0:2])[0]
            for i in range(count):
                off = 2 + i * 12
                if off + 12 > len(pl): break
                fid = struct.unpack('<I', pl[off:off+4])[0]
                if fid == 0x4F:
                    return struct.unpack('<I', pl[off+4:off+8])[0]
    return None

def build_gather_plain(tile_x, tile_y, hero_id=0xFF, march_slot=2):
    p = bytearray(46)
    p[0] = march_slot & 0xFF
    p[1] = random.randint(0, 255)
    p[2] = random.randint(0, 255)
    p[3] = random.randint(0, 255)
    struct.pack_into('<H', p, 4, MARCH_TYPE)
    struct.pack_into('<H', p, 9, tile_x)
    struct.pack_into('<H', p, 11, tile_y)
    p[13] = 0x01
    p[14] = hero_id & 0xFF
    p[18] = KINGDOM & 0xFF
    struct.pack_into('<I', p, 22, 4)
    struct.pack_into('<I', p, 33, IGG_ID)
    return bytes(p)

def build_enable_view():
    p = bytearray(10)
    p[0] = 0x01
    struct.pack_into('<I', p, 1, IGG_ID)
    p[9] = 0x01
    return bytes(p)

hb_lock = threading.Lock()

def send_hb(sock):
    ms = int((time.time() - send_hb.start) * 1000)
    with hb_lock:
        try:
            sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
            return True
        except:
            return False
send_hb.start = 0

def heartbeat_loop(sock, stop_evt):
    while not stop_evt.wait(8):
        send_hb(sock)

def check_alive(sock, reader):
    send_hb(sock)
    ck = reader.read_all(timeout=3)
    return any(op == 0x0002 for op, _ in ck)

def parse_resource_sync(pl):
    """Try to extract resource tile coordinates from 0x0078."""
    tiles = []
    if len(pl) < 4:
        return tiles
    try:
        count = struct.unpack('<H', pl[0:2])[0]
        # Each resource entry seems to start with a u64 ID then coordinates
        # Let's just log the raw data for now
        log(f"  0x0078: {count} entries, {len(pl)}B, first 60: {pl[:60].hex()}")
    except:
        pass
    return tiles

def main():
    log(f"=== GATHER DEBUG === IGG={IGG_ID}")
    send_hb.start = time.time()

    access_key = node_login()
    if not access_key:
        log("LOGIN FAILED"); return
    log(f"Key OK")

    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    log(f"Game: {gw['ip']}:{gw['port']}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(15)
    sock.connect((gw['ip'], gw['port']))
    reader = PacketReader(sock)

    sock.sendall(build_game_login(IGG_ID, gw['token']))
    pkts = reader.read_all(timeout=3)
    if not any(op == 0x0020 and pl and pl[0] == 1 for op, pl in pkts):
        log("Login FAILED"); sock.close(); return
    log("Login OK")

    sock.sendall(build_world_entry(IGG_ID))
    flood = reader.read_all(timeout=6)
    log(f"Init: {len(flood)} pkts")

    sk = extract_server_key(flood)
    if not sk:
        log("No SK!"); sock.close(); return
    log(f"SK: 0x{sk:08X}")
    codec = CMsgCodec.from_u32(sk)

    # Start heartbeat thread
    stop = threading.Event()
    threading.Thread(target=heartbeat_loop, args=(sock, stop), daemon=True).start()

    # Setup
    for op in [0x0840, 0x17D4, 0x0AF2, 0x0245]:
        sock.sendall(build_packet(op))
    time.sleep(0.3)
    reader.read_all(timeout=1)

    # Enable view
    sock.sendall(codec.encode(0x0CEB, build_enable_view()))
    time.sleep(0.5)
    ev_resp = reader.read_all(timeout=2)

    # Log resource tiles from enable_view response
    log("\n--- Resource tiles from 0x0078 ---")
    for op, pl in ev_resp:
        if op == 0x0078:
            parse_resource_sync(pl)

    # Source + target tiles
    sock.sendall(build_packet(0x006E, struct.pack('<HHB', 579, 830, 0x01)))
    time.sleep(0.3)

    target_x, target_y = 550, 851
    sock.sendall(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 0x01)))
    time.sleep(0.5)

    # Check resource tiles from target area
    tile_resp = reader.read_all(timeout=2)
    log("\n--- Resource tiles near target ---")
    for op, pl in tile_resp:
        if op == 0x0078:
            parse_resource_sync(pl)
        elif op == 0x0077:
            log(f"  0x0077 MONSTER_SYNC ({len(pl)}B): {pl[:30].hex()}")
        elif op == 0x0091:
            log(f"  0x0091 ({len(pl)}B): {pl[:30].hex()}")

    # CHECK ALIVE before gather
    log("\n--- Alive check BEFORE gather ---")
    alive1 = check_alive(sock, reader)
    log(f"Alive BEFORE: {alive1}")
    if not alive1:
        log("Already dead!"); stop.set(); sock.close(); return

    # Hero select for slot 2
    sock.sendall(build_packet(0x0323, bytes([0x00, 0x02, 0x00, 0xFF, 0x00, 0x00, 0x00])))
    time.sleep(0.3)
    reader.read_all(timeout=0.5)

    # GATHER
    log(f"\n=== GATHER slot=2 -> ({target_x},{target_y}) ===")
    gp = build_gather_plain(target_x, target_y, hero_id=0xFF, march_slot=2)
    log(f"Plain: {gp.hex()}")
    sock.sendall(codec.encode(0x0CE8, gp))

    # Quick response (3s)
    time.sleep(0.5)
    quick = reader.read_all(timeout=3)
    log(f"\nQuick response ({len(quick)} pkts):")
    for op, pl in quick:
        if op not in (0x0042, 0x036C, 0x0002):
            log(f"  0x{op:04X} ({len(pl)}B): {pl[:50].hex() if pl else ''}")

    # Alive RIGHT AFTER gather
    log("\n--- Alive check AFTER gather ---")
    alive2 = check_alive(sock, reader)
    log(f"Alive AFTER: {alive2}")

    if alive2:
        # Wait more for delayed responses
        log("\nWaiting 15s for delayed responses...")
        delayed = reader.read_all(timeout=15)
        log(f"Delayed: {len(delayed)} pkts")
        for op, pl in delayed:
            if op not in (0x0042, 0x036C, 0x0002):
                log(f"  0x{op:04X} ({len(pl)}B): {pl[:50].hex() if pl else ''}")

        alive3 = check_alive(sock, reader)
        log(f"Alive FINAL: {alive3}")

    stop.set()
    sock.close()
    log("Done.")

if __name__ == '__main__':
    main()

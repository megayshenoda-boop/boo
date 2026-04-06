"""
Gather Test v5 - Based on v4 findings:
- Slot 1 occupied → use slot 2
- 0x00B8 received but no 0x0071
- Add 0x01D6 READY_SIG
- Add longer wait for 0x0071 (might be delayed)
- Try sending 0x0023 AUTH immediately after 0x0021 (before game data flood)
"""
import sys, time, struct, subprocess, random, socket, threading
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD, GATEWAY_IP, GATEWAY_PORT, GAME_ID_HEX
from gateway import connect_gateway
from codec import CMsgCodec, extract_server_key_from_0x0038
from packets import build_packet, recv_packet, build_game_login, build_world_entry
from protocol import opname, OP_ENABLE_VIEW, OP_START_MARCH, CMSG_TABLE

KINGDOM = 182
MARCH_TYPE = 0x1749
TURF_X, TURF_Y = 653, 567
TROOP_IDS = [403, 405, 407, 411]
FORMATION_TROOPS = [1046, 3002, 1035, 2008, 2019, 1009, 1024, 1016, 2009, 1025]

def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def node_login(email, password, igg_id):
    result = subprocess.run(
        ['node', r'D:\CascadeProjects\lords_bot\http_login.mjs', email, password, str(igg_id)],
        capture_output=True, text=True, timeout=30
    )
    return result.stdout.strip() if len(result.stdout.strip()) == 32 else None

def build_enable_view(codec, igg_id, view_type=0x01):
    data = bytearray(10)
    data[0] = view_type
    struct.pack_into('<I', data, 1, igg_id)
    data[9] = 0x01
    return codec.encode(OP_ENABLE_VIEW, bytes(data))

def build_gather_0ce8(codec, tile_x, tile_y, hero_id=255, march_slot=2):
    data = bytearray(46)
    data[0] = march_slot & 0xFF
    data[1] = random.randint(0, 255)
    data[2] = random.randint(0, 255)
    data[3] = random.randint(0, 255)
    struct.pack_into('<H', data, 4, MARCH_TYPE)
    struct.pack_into('<H', data, 9, tile_x)
    struct.pack_into('<H', data, 11, tile_y)
    data[13] = 0x01
    data[14] = hero_id & 0xFF
    data[18] = KINGDOM & 0xFF
    data[22] = 0x04
    struct.pack_into('<I', data, 33, IGG_ID)
    log(f"  Plaintext ({len(data)}B) slot={march_slot}: {data.hex()}")
    return codec.encode(OP_START_MARCH, bytes(data))

# ──── Custom connection with early 0x0023 AUTH ────
class GatherConnection:
    """Custom game connection that injects 0x0023 AUTH right after 0x0021."""
    def __init__(self, igg_id, ip, port, session_token, access_key):
        self.igg_id = igg_id
        self.ip = ip
        self.port = port
        self.session_token = session_token
        self.access_key = access_key
        self.sock = None
        self.codec = None
        self.start_time = time.time()
        self._callbacks = []
        self._listener = None
        self._running = False

    def on_packet(self, cb):
        self._callbacks.append(cb)

    def _dispatch(self, op, pl):
        for cb in self._callbacks:
            cb(op, pl)

    def send(self, data):
        try:
            self.sock.sendall(data)
        except:
            pass

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(15)
        self.sock.connect((self.ip, self.port))
        self.start_time = time.time()

        # 1. Send 0x001F login
        self.send(build_game_login(self.igg_id, self.session_token))
        log("  Sent 0x001F login")

        # 2. Recv 0x0020
        r = recv_packet(self.sock, timeout=10)
        if r:
            op, pl, _ = r
            log(f"  Got 0x{op:04X} ({len(pl)}B)")

        # 3. Send 0x0021
        self.send(build_world_entry(self.igg_id))
        log("  Sent 0x0021 world entry")

        # 4. Send 0x0023 AUTH immediately (before game data flood!)
        auth_data = bytearray(58)
        struct.pack_into('<Q', auth_data, 0, 1)
        struct.pack_into('<I', auth_data, 8, self.igg_id)
        struct.pack_into('<H', auth_data, 16, 32)
        key_bytes = self.access_key[:32].encode('ascii')
        auth_data[18:18+len(key_bytes)] = key_bytes
        auth_data[50] = 0x0E
        auth_data[51] = 0xFF
        auth_data[52] = 0x00
        auth_data[53] = 0x3F
        self.send(build_packet(0x0023, bytes(auth_data)))
        log("  Sent 0x0023 AUTH (early, before game data)")

        # 5. Receive game data flood
        log("  Receiving game data...")
        server_key = None
        packet_count = 0
        deadline = time.time() + 10
        while time.time() < deadline:
            r = recv_packet(self.sock, timeout=2)
            if r is None:
                break
            op, pl, _ = r
            packet_count += 1
            if op == 0x0038 and server_key is None:
                server_key = extract_server_key_from_0x0038(pl)
                if server_key:
                    log(f"  *** SERVER KEY: 0x{server_key:08x} ***")
            if op == 0x0024:
                log(f"  0x0024 AUTH response: {pl.hex()}")

        log(f"  Received {packet_count} packets")
        if server_key:
            self.codec = CMsgCodec.from_u32(server_key)
            log(f"  CMsgCodec ready")
        else:
            log("  WARNING: No server key!")

        # Start listener thread
        self._running = True
        self._listener = threading.Thread(target=self._listen, daemon=True)
        self._listener.start()

        # Start heartbeat
        self._hb = threading.Thread(target=self._heartbeat, daemon=True)
        self._hb.start()

    def _listen(self):
        while self._running:
            try:
                r = recv_packet(self.sock, timeout=3)
                if r is None:
                    continue
                op, pl, _ = r
                self._dispatch(op, pl)
            except:
                break

    def _heartbeat(self):
        while self._running:
            time.sleep(25)
            ms = int((time.time() - self.start_time) * 1000)
            try:
                self.send(build_packet(0x0042, struct.pack('<II', ms, 0)))
            except:
                break

    def disconnect(self):
        self._running = False
        try:
            self.sock.close()
        except:
            pass


responses = []
def on_packet(opcode, payload):
    responses.append((opcode, payload))

def drain(label="", timeout=3):
    time.sleep(timeout)
    found = []
    while responses:
        op, pl = responses.pop(0)
        if op not in (0x0042, 0x036C, 0x0002):
            found.append((op, pl))
    if found and label:
        log(f"  [{label}] {len(found)} responses:")
        for op, pl in found:
            prefix = pl[:20].hex() if pl else ""
            log(f"    <- 0x{op:04X} {opname(op)} ({len(pl)}B) {prefix}")
    return found


def main():
    log("=== GATHER TEST v5 (Early AUTH + READY_SIG) ===")

    access_key = node_login(EMAIL, PASSWORD, IGG_ID)
    if not access_key:
        log("Login failed!"); return
    log(f"Access key: {access_key[:8]}...")

    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)

    # Use custom connection with early 0x0023 AUTH
    gc = GatherConnection(IGG_ID, gw['ip'], gw['port'], gw['token'], access_key)
    gc.on_packet(on_packet)
    gc.connect()

    if not gc.codec:
        log("No codec!"); gc.disconnect(); return

    codec = gc.codec
    time.sleep(2)
    responses.clear()

    # ──── Setup ────
    log("\n=== SETUP ===")
    gc.send(build_packet(0x0840))
    gc.send(build_packet(0x0245))
    data = struct.pack('<H', len(FORMATION_TROOPS))
    for tid in FORMATION_TROOPS:
        data += struct.pack('<I', tid)
    gc.send(build_packet(0x0834, data))
    gc.send(build_packet(0x0709))
    gc.send(build_packet(0x0A2C))
    drain("SETUP", timeout=2)

    # ──── Search resource ────
    log("\n=== SEARCH ===")
    gc.send(build_packet(0x033E, bytes([0x01, 0x04, 0x00, 0x03])))
    time.sleep(3)
    target_x, target_y = None, None
    while responses:
        op, pl = responses.pop(0)
        if op == 0x033F and len(pl) >= 5:
            tx = struct.unpack('<H', pl[1:3])[0]
            ty = struct.unpack('<H', pl[3:5])[0]
            log(f"  Found: ({tx},{ty})")
            if target_x is None:
                target_x, target_y = tx, ty
        elif op not in (0x0042, 0x036C, 0x0002):
            log(f"  Search: 0x{op:04X} ({len(pl)}B)")
    if target_x is None:
        target_x, target_y = 650, 576
        log(f"  Default: ({target_x},{target_y})")

    # ──── Full PCAP sequence ────
    log("\n=== GATHER SEQUENCE (PCAP order) ===")

    # ENABLE_VIEW(1) + view tile
    log("1. ENABLE_VIEW(1) + view tile")
    gc.send(build_enable_view(codec, IGG_ID, 0x01))
    gc.send(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 0x01)))
    time.sleep(1)

    # ENABLE_VIEW(0) + troops
    log("2. ENABLE_VIEW(0) + troops")
    gc.send(build_enable_view(codec, IGG_ID, 0x00))
    for tid in TROOP_IDS:
        gc.send(build_packet(0x099D, struct.pack('<I', tid)))
    time.sleep(0.5)

    # Sync
    log("3. Sync")
    gc.send(build_packet(0x0767))
    gc.send(build_packet(0x0769))
    time.sleep(1)

    # ENABLE_VIEW(1) + source tile + target tile
    log("4. ENABLE_VIEW(1) + source + target tiles")
    gc.send(build_enable_view(codec, IGG_ID, 0x01))
    gc.send(build_packet(0x006E, struct.pack('<HHB', TURF_X, TURF_Y, 0x01)))
    time.sleep(1)
    gc.send(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 0x01)))
    time.sleep(1)

    # 0x01D6 READY_SIG
    log("5. READY_SIG (0x01D6)")
    gc.send(build_packet(0x01D6))
    time.sleep(2)

    # Drain before gather
    drain("PRE-GATHER", timeout=0.5)

    # Heartbeat
    log("6. Heartbeat")
    ms = int((time.time() - gc.start_time) * 1000)
    gc.send(build_packet(0x0042, struct.pack('<II', ms, 0)))
    time.sleep(1.5)

    # GATHER slot=2
    log(f"\n7. GATHER slot=2 -> ({target_x},{target_y})")
    gc.send(build_gather_0ce8(codec, target_x, target_y, hero_id=255, march_slot=2))

    # Wait longer for full response chain
    log("  Waiting 20s for response chain...")
    r = drain("GATHER", timeout=20)

    # Analysis
    opcodes_got = [op for op, _ in r]
    has_00b8 = 0x00B8 in opcodes_got
    has_0071 = 0x0071 in opcodes_got
    has_076c = 0x076C in opcodes_got
    has_007c = 0x007C in opcodes_got
    has_00b9 = 0x00B9 in opcodes_got
    has_0033 = 0x0033 in opcodes_got

    log(f"\n=== RESULT ===")
    log(f"  0x00B8 MARCH_ACCEPT:  {'YES' if has_00b8 else 'no'}")
    log(f"  0x0071 MARCH_STATE:   {'YES' if has_0071 else 'no'}")
    log(f"  0x076C MARCH_BUNDLE:  {'YES' if has_076c else 'no'}")
    log(f"  0x007C COLLECT_STATE: {'YES' if has_007c else 'no'}")
    log(f"  0x00B9 MARCH_ACK:     {'YES' if has_00b9 else 'no'}")
    log(f"  0x0033 ATTR_CHANGE:   {'YES' if has_0033 else 'no'}")

    for op, pl in r:
        if op in (0x00B8, 0x00B9, 0x0071, 0x076C, 0x0033, 0x0037, 0x007C):
            log(f"  Detail 0x{op:04X}: {pl.hex()}")

    if has_0071:
        log("\n  >>> MARCH CREATED! <<<")
    elif has_00b8 and not has_0071:
        log("\n  >>> PARTIAL: 0x00B8 but no 0x0071 - march NOT created <<<")
    else:
        log("\n  >>> FAILED <<<")

    # Wait for very late responses (0x007C collect can come 15+ seconds later)
    time.sleep(15)
    late = []
    while responses:
        op, pl = responses.pop(0)
        if op not in (0x0042, 0x036C, 0x0002):
            late.append((op, pl))
    if late:
        log("\nLate responses:")
        for op, pl in late:
            log(f"  <- 0x{op:04X} {opname(op)} ({len(pl)}B)")
            if op == 0x0071:
                log("  >>> LATE 0x0071 = MARCH CREATED! <<<")

    gc.disconnect()
    log("=== DONE ===")

if __name__ == '__main__':
    main()

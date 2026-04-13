#!/usr/bin/env python3
"""
Gather Final - Extract heroes from init, send proper 0x0323, manual heartbeats.
"""
import sys, time, struct, random, subprocess, socket
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from codec import CMsgCodec
from packets import build_packet, build_game_login, build_world_entry

MARCH_TYPE = 0x1749
KINGDOM = 182
T0 = 0

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}.{int((time.time()%1)*1000):03d}] {msg}", flush=True)

def node_login():
    r = subprocess.run(
        ['node', r'D:\CascadeProjects\lords_bot\http_login.mjs', EMAIL, PASSWORD, str(IGG_ID)],
        capture_output=True, text=True, timeout=30, encoding='utf-8', errors='replace'
    )
    key = r.stdout.strip()
    return key if len(key) == 32 else None

class PR:
    def __init__(self, sock):
        self.s = sock
        self.buf = b''
    def drain(self, timeout=3):
        pkts = []
        deadline = time.time() + timeout
        while time.time() < deadline:
            self.s.settimeout(max(0.05, deadline - time.time()))
            try:
                c = self.s.recv(65536)
                if not c: break
                self.buf += c
            except socket.timeout: pass
            while len(self.buf) >= 4:
                pl = struct.unpack('<H', self.buf[0:2])[0]
                if pl < 4 or pl > 100000: self.buf = self.buf[1:]; continue
                if len(self.buf) < pl: break
                op = struct.unpack('<H', self.buf[2:4])[0]
                pkts.append((op, self.buf[4:pl]))
                self.buf = self.buf[pl:]
        return pkts

def sk_from(pkts):
    for op, pl in pkts:
        if op == 0x0038 and len(pl) > 100:
            n = struct.unpack('<H', pl[0:2])[0]
            for i in range(n):
                o = 2 + i * 12
                if o + 12 > len(pl): break
                if struct.unpack('<I', pl[o:o+4])[0] == 0x4F:
                    return struct.unpack('<I', pl[o+4:o+8])[0]
    return None

def hb(s):
    ms = int((time.time() - T0) * 1000)
    s.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))

def gather_plain(tx, ty, hero_id=0xFF, slot=2, troops=None):
    """Build gather plaintext. If troops given, 62-byte format with troop array."""
    if troops is None:
        troops = []
    N = len(troops)
    size = 46 + N * 4
    p = bytearray(size)
    p[0] = slot
    p[1], p[2], p[3] = random.randint(0,255), random.randint(0,255), random.randint(0,255)
    struct.pack_into('<H', p, 4, MARCH_TYPE)
    struct.pack_into('<H', p, 9, tx)
    struct.pack_into('<H', p, 11, ty)
    p[13] = 0x01
    p[14] = hero_id & 0xFF
    p[18] = KINGDOM
    # [19:21] zeros
    p[21] = N  # troop/hero array count
    for i, tid in enumerate(troops):
        struct.pack_into('<I', p, 22 + i * 4, tid)
    off = 22 + N * 4
    struct.pack_into('<I', p, off, 4)  # purpose
    # zeros
    struct.pack_into('<I', p, off + 11, IGG_ID)  # igg_id
    return bytes(p)

def ev_plain():
    p = bytearray(10)
    p[0] = 0x01
    struct.pack_into('<I', p, 1, IGG_ID)
    p[9] = 0x01
    return bytes(p)

def build_0323_v1(hero_ids):
    """Format: [flag=0, count, heroes..., trailing=0] = PCAP-exact for 5 heroes"""
    payload = bytearray()
    payload.append(0x00)
    payload.append(len(hero_ids) & 0xFF)
    for hid in hero_ids:
        payload += struct.pack('<I', hid)
    payload.append(0x00)
    return build_packet(0x0323, bytes(payload))

def build_0323_v2(slot, support_heroes, lead_hero):
    """Format: [flag=0, slot, 4 support heroes, u16 lead, u8, u16] = ARM64 layout"""
    payload = bytearray()
    payload.append(0x00)
    payload.append(slot & 0xFF)
    for hid in support_heroes:
        payload += struct.pack('<I', hid)
    payload += struct.pack('<H', lead_hero)
    payload.append(0x00)
    payload += struct.pack('<H', 0)
    return build_packet(0x0323, bytes(payload))

def main():
    global T0
    log(f"=== GATHER FINAL === IGG={IGG_ID}")

    ak = node_login()
    if not ak: log("LOGIN FAIL"); return
    log("Key OK")

    gw = connect_gateway(IGG_ID, ak, WORLD_ID)
    log(f"Game: {gw['ip']}:{gw['port']}")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(15)
    s.connect((gw['ip'], gw['port']))
    r = PR(s)

    s.sendall(build_game_login(IGG_ID, gw['token']))
    pkts = r.drain(timeout=3)
    if not any(op == 0x0020 and pl and pl[0] == 1 for op, pl in pkts):
        log("Login FAIL"); s.close(); return
    log("Login OK")
    T0 = time.time()

    s.sendall(build_world_entry(IGG_ID))
    hb(s)
    flood = r.drain(timeout=6)
    log(f"Init: {len(flood)} pkts")

    sk = sk_from(flood)
    if not sk: log("No SK!"); s.close(); return
    log(f"SK: 0x{sk:08X}")
    codec = CMsgCodec.from_u32(sk)
    hb(s)

    # Log ALL unique opcodes and find hero data
    opcodes_seen = {}
    for op, pl in flood:
        opcodes_seen[op] = opcodes_seen.get(op, 0) + 1

    # Log hero-related packets
    log("\n--- Hero/Army packets in init flood ---")
    for op, pl in flood:
        if op == 0x00AA:  # HERO_INFO
            log(f"  0x00AA HERO_INFO ({len(pl)}B): {pl[:40].hex()}")
        elif op == 0x00B8:  # HERO_QUEUE_EXPEDITION
            log(f"  0x00B8 HERO_EXPEDITION ({len(pl)}B): {pl.hex()}")
        elif op == 0x00B7:  # HERO_CANDIDATE_QUEUE
            log(f"  0x00B7 HERO_CANDIDATE ({len(pl)}B): {pl[:40].hex()}")
        elif op == 0x0071:
            log(f"  0x0071 ({len(pl)}B): {pl[:30].hex()}")
        elif op == 0x06C2:
            log(f"  0x06C2 MARCH_DATA ({len(pl)}B): {pl[:30].hex()}")

    log(f"\nUnique opcodes: {len(opcodes_seen)}")
    for op in sorted(opcodes_seen.keys()):
        if opcodes_seen[op] > 1:
            log(f"  0x{op:04X}: {opcodes_seen[op]}x")

    hb(s)

    # Setup
    for op in [0x0840, 0x17D4, 0x0AF2, 0x0245]:
        s.sendall(build_packet(op))
    time.sleep(0.3)
    r.drain(timeout=1)
    hb(s)

    # Enable view
    s.sendall(codec.encode(0x0CEB, ev_plain()))
    time.sleep(0.3)
    r.drain(timeout=2)
    hb(s)

    # Tiles
    tx, ty = 550, 851
    s.sendall(build_packet(0x006E, struct.pack('<HHB', 579, 830, 0x01)))
    time.sleep(0.2)
    s.sendall(build_packet(0x006E, struct.pack('<HHB', tx, ty, 0x01)))
    time.sleep(0.3)
    r.drain(timeout=2)
    hb(s)

    slot = 2
    all_heroes = [201, 206, 212, 216, 224]

    # === Test V1: PCAP-exact [flag=0, count=5, 5 heroes, trailing=0] ===
    pkt_v1 = build_0323_v1(all_heroes)
    log(f"\n--- 0x0323 V1: [0,count={len(all_heroes)},heroes,0] ---")
    log(f"  Payload ({len(pkt_v1)-4}B): {pkt_v1[4:].hex()}")
    s.sendall(pkt_v1)
    time.sleep(1)
    resp_v1 = r.drain(timeout=2)
    for op, pl in resp_v1:
        if op not in (0x0042, 0x036C, 0x0002):
            log(f"  V1 <- 0x{op:04X} ({len(pl)}B): {pl[:40].hex() if pl else ''}")
    hb(s)

    # slot=2, hero=0xFF (slot=1 busy)
    hero = 0xFF
    slot = 2
    log(f"\n=== GATHER slot={slot} -> ({tx},{ty}) hero={hero} (46B) ===")
    gp = gather_plain(tx, ty, hero_id=hero, slot=slot)
    log(f"Plain ({len(gp)}B): {gp.hex()}")
    s.sendall(codec.encode(0x0CE8, gp))

    # Quick check 2s
    time.sleep(0.3)
    resp1 = r.drain(timeout=2)
    log(f"\nResponse ({len(resp1)} pkts) - ALL:")
    for op, pl in resp1:
        log(f"  0x{op:04X} ({len(pl)}B): {pl[:50].hex() if pl else 'empty'}")

    # Alive check right after (server echoes 0x0042, NOT 0x0002!)
    hb(s)
    ck = r.drain(timeout=3)
    alive_after = any(op == 0x0042 for op, _ in ck)
    log(f"Alive after gather: {alive_after}")
    for op, pl in ck:
        if op not in (0x036C,):
            log(f"  ck: 0x{op:04X} ({len(pl)}B)")

    if alive_after:
        # Wait for march to travel (9s in PCAP)
        log("\nWaiting 12s for march arrival...")
        for i in range(3):
            time.sleep(4)
            hb(s)
            pkts = r.drain(timeout=1)
            for op, pl in pkts:
                if op not in (0x0042, 0x036C, 0x0002):
                    log(f"  +{(i+1)*4}s: 0x{op:04X} ({len(pl)}B): {pl[:50].hex() if pl else ''}")

    hb(s)

    # Alive
    log("\n--- Alive check ---")
    hb(s)
    ck = r.drain(timeout=3)
    alive = any(op == 0x0042 for op, _ in ck)
    log(f"Alive: {alive}")

    s.close()
    log("Done.")

if __name__ == '__main__':
    main()

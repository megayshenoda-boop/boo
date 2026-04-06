"""
Smart Build Test: Read all buildings from 0x0097, then upgrade slot 27 (real=74)
"""
import sys, time, struct, subprocess
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from game_server import GameConnection
from commands import CommandEngine
from packets import build_packet
from protocol import opname

BUILDING_NAMES = {
    1: "Castle", 2: "Wall", 3: "Embassy", 4: "Battle Hall",
    5: "Prison", 6: "Altar", 7: "Watchtower", 8: "Treasure",
    13: "Shelter", 14: "Workshop", 21: "Academy", 23: "Trading Post",
    24: "Barracks", 28: "Hospital1", 29: "Hospital2", 30: "Vault1", 31: "Vault2",
    51: "Farm", 52: "Mine", 53: "Lumber Mill", 55: "Quarry", 56: "Manor", 60: "Familiar",
}

# Visual → Real slot mapping (PCAP verified)
VISUAL_TO_REAL = {
    1:78, 2:77, 3:80, 4:76, 5:79, 6:70, 7:75, 8:66, 9:69, 10:72,
    11:68, 12:67, 13:71, 14:64, 15:61, 16:65, 17:62, 18:63, 19:59, 20:60,
    21:58, 22:57, 23:56, 24:55, 25:54, 26:53, 27:74, 28:52, 29:51, 30:73,
}

def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def node_login(email, password, igg_id):
    result = subprocess.run(
        ['node', r'D:\CascadeProjects\lords_bot\http_login.mjs', email, password, str(igg_id)],
        capture_output=True, text=True, timeout=30
    )
    return result.stdout.strip() if len(result.stdout.strip()) == 32 else None

def parse_buildings(payload):
    """Parse 0x0097 BUILDING_INFO: [u16 count] + [count * 19B entries]"""
    if len(payload) < 2:
        return []
    count = struct.unpack('<H', payload[0:2])[0]
    buildings = []
    for i in range(count):
        off = 2 + i * 19
        if off + 6 > len(payload):
            break
        slot = struct.unpack('<H', payload[off:off+2])[0]
        btype = struct.unpack('<H', payload[off+2:off+4])[0]
        level = struct.unpack('<H', payload[off+4:off+6])[0]
        timer = struct.unpack('<I', payload[off+6:off+10])[0] if off+10 <= len(payload) else 0
        buildings.append({'slot': slot, 'type': btype, 'level': level, 'timer': timer})
    return buildings

responses = []
def on_packet(opcode, payload):
    responses.append((opcode, payload))

def wait_and_collect(label, timeout=6):
    time.sleep(timeout)
    found = []
    while responses:
        op, pl = responses.pop(0)
        if op not in (0x0042, 0x036C, 0x0002, 0x01E7):
            found.append((op, pl))
            log(f"    <- 0x{op:04X} {opname(op)} ({len(pl)}B)")
    if not found:
        log(f"    (no response for {label})")
    return found

def main():
    log("=== SMART BUILD TEST ===")

    access_key = node_login(EMAIL, PASSWORD, IGG_ID)
    if not access_key:
        log("Login failed!"); return
    log(f"Access key: {access_key[:8]}...")

    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    gc = GameConnection(IGG_ID, gw['ip'], gw['port'], gw['token'])
    gc.on_packet(on_packet)
    gc.connect()

    if not gc.codec:
        log("No codec!"); gc.disconnect(); return

    # ──── Parse 0x0097 building data ────
    log("")
    log("=== READING ALL BUILDINGS FROM 0x0097 ===")
    raw_0097 = gc.game_state.raw_packets.get(0x0097, [])
    all_buildings = {}
    for payload in raw_0097:
        for b in parse_buildings(payload):
            all_buildings[b['slot']] = b

    log(f"Total buildings found: {len(all_buildings)}")
    log("")

    # Show outer slots (51-83) which are the Call to Arms slots
    log("=== OUTER SLOTS (resource buildings) ===")
    for slot in sorted(all_buildings.keys()):
        if slot >= 51:
            b = all_buildings[slot]
            name = BUILDING_NAMES.get(b['type'], f"Unknown({b['type']})")
            timer_str = f" timer={b['timer']}" if b['timer'] > 0 else ""
            # Find visual slot
            visual = None
            for v, r in VISUAL_TO_REAL.items():
                if r == slot:
                    visual = v
                    break
            vis_str = f" [Visual #{visual}]" if visual else ""
            log(f"  Slot {slot:3d}: type={b['type']:3d} ({name:15s}) level={b['level']:2d}{timer_str}{vis_str}")

    # Show inner slots too
    log("")
    log("=== INNER SLOTS ===")
    for slot in sorted(all_buildings.keys()):
        if slot < 51:
            b = all_buildings[slot]
            name = BUILDING_NAMES.get(b['type'], f"Unknown({b['type']})")
            log(f"  Slot {slot:3d}: type={b['type']:3d} ({name:15s}) level={b['level']:2d}")

    # ──── Now upgrade slot 27 (real=74) ────
    target_real_slot = 74  # visual 27
    if target_real_slot in all_buildings:
        b = all_buildings[target_real_slot]
        name = BUILDING_NAMES.get(b['type'], f"Unknown({b['type']})")
        log(f"\n=== TARGET: Visual 27 = Real Slot {target_real_slot} ===")
        log(f"  Type: {b['type']} ({name}), Level: {b['level']}")
        log(f"  Will upgrade to level {b['level'] + 1}")

        cmd = CommandEngine(IGG_ID, gc.codec)
        time.sleep(2)
        responses.clear()

        # Try new-style 0x0CEF with correct building type
        log(f"\n  Sending UPGRADE (0x0CEF): type={b['type']}, slot={target_real_slot}, op=1")
        gc.send(cmd.upgrade(building_type=b['type'], slot=target_real_slot))
        r1 = wait_and_collect("Upgrade via 0x0CEF")

        # Also try old-style if new-style didn't work
        if not any(op in (0x02D1, 0x021C, 0x11C8, 0x009E, 0x0098) for op, _ in r1):
            log(f"\n  Trying OLD-STYLE 0x009D: op=0x01, slot={target_real_slot}")
            payload = bytearray(12)
            payload[0] = 0x01  # upgrade
            payload[1] = target_real_slot & 0xFF
            gc.send(build_packet(0x009D, bytes(payload)))
            r2 = wait_and_collect("Upgrade via 0x009D")
    else:
        log(f"\n  Slot {target_real_slot} NOT FOUND in building data!")
        log(f"  (Maybe it was demolished? Available outer slots: {[s for s in sorted(all_buildings.keys()) if s >= 51]})")

    time.sleep(3)
    gc.disconnect()
    log("=== DONE ===")

if __name__ == '__main__':
    main()

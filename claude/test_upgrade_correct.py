"""
Test CORRECT upgrade payload based on PCAP findings:
[0]=0x08 [1]=slot [3]=type [7:11]=0x92771E80 [12:16]=IGG_ID
"""
import sys, time, struct, subprocess
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from game_server import GameConnection
from codec import CMsgCodec
from packets import build_packet
from protocol import opname, OP_BUILD

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
    if len(payload) < 2: return []
    count = struct.unpack('<H', payload[0:2])[0]
    buildings = []
    for i in range(count):
        off = 2 + i * 19
        if off + 6 > len(payload): break
        buildings.append({
            'slot': struct.unpack('<H', payload[off:off+2])[0],
            'type': struct.unpack('<H', payload[off+2:off+4])[0],
            'level': struct.unpack('<H', payload[off+4:off+6])[0],
        })
    return buildings

def build_upgrade_packet(codec, slot, building_type, igg_id):
    """Build CORRECT upgrade payload from PCAP findings."""
    data = bytearray(22)
    data[0] = 0x08              # upgrade op (NOT 0x01!)
    data[1] = slot & 0xFF       # slot
    data[2] = 0x00
    data[3] = building_type & 0xFF  # building type
    # [4:7] = zeros
    # [7:11] = magic bytes 0x92771E80 (LE: 80 1e 77 92)
    data[7]  = 0x80
    data[8]  = 0x1e
    data[9]  = 0x77
    data[10] = 0x92
    data[11] = 0x00             # flag
    struct.pack_into('<I', data, 12, igg_id)  # [12:16] = IGG_ID
    # [16:22] = zeros

    log(f"  Plaintext: {data.hex()}")
    return codec.encode(OP_BUILD, bytes(data))

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
    log("=== CORRECT UPGRADE TEST ===")

    access_key = node_login(EMAIL, PASSWORD, IGG_ID)
    if not access_key:
        log("Login failed!"); return

    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    gc = GameConnection(IGG_ID, gw['ip'], gw['port'], gw['token'])
    gc.on_packet(on_packet)
    gc.connect()

    if not gc.codec:
        log("No codec!"); gc.disconnect(); return

    # Read buildings
    raw_0097 = gc.game_state.raw_packets.get(0x0097, [])
    buildings = {}
    for payload in raw_0097:
        for b in parse_buildings(payload):
            buildings[b['slot']] = b

    # Target: Visual 27 = Real slot 74
    target_slot = 74
    b = buildings.get(target_slot)
    if not b:
        log(f"Slot {target_slot} not found!"); gc.disconnect(); return

    log(f"\nTarget: Slot {target_slot}, Type {b['type']} (Farm), Level {b['level']}")
    log(f"Upgrading to level {b['level'] + 1}...")

    time.sleep(2)
    responses.clear()

    # Send CORRECT upgrade
    pkt = build_upgrade_packet(gc.codec, target_slot, b['type'], IGG_ID)
    gc.send(pkt)
    r = wait_and_collect("CORRECT Upgrade")

    # Check for success signals
    has_02d1 = any(op == 0x02D1 for op, _ in r)
    has_11c8 = any(op == 0x11C8 for op, _ in r)
    has_021c = any(op == 0x021C for op, _ in r)
    has_022b = any(op == 0x022B for op, _ in r)

    log(f"\n  Results:")
    log(f"    0x02D1 ACTION_CONFIRM:  {'YES!' if has_02d1 else 'no'}")
    log(f"    0x11C8 TIMER_SET:       {'YES!' if has_11c8 else 'no'}")
    log(f"    0x021C BUILDING_DATA:   {'YES!' if has_021c else 'no'}")
    log(f"    0x022B RESOURCE_DEDUCT: {'YES!' if has_022b else 'no'}")

    if has_02d1:
        log(f"\n  UPGRADE SUCCESS!")
    else:
        log(f"\n  Upgrade may have failed - check in game")

    time.sleep(3)
    gc.disconnect()
    log("=== DONE ===")

if __name__ == '__main__':
    main()

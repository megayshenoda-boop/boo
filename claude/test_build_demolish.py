"""
Test: Upgrade slot 27 (real=74) + Demolish slot 7 (real=75)
"""
import sys, time, struct, subprocess
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from game_server import GameConnection
from commands import CommandEngine
from packets import build_packet
from protocol import opname

def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def node_login(email, password, igg_id):
    result = subprocess.run(
        ['node', r'D:\CascadeProjects\lords_bot\http_login.mjs', email, password, str(igg_id)],
        capture_output=True, text=True, timeout=30
    )
    token = result.stdout.strip()
    return token if len(token) == 32 else None

responses = []
def on_packet(opcode, payload):
    responses.append((opcode, payload))

def wait_and_collect(label, timeout=6):
    time.sleep(timeout)
    found = []
    while responses:
        op, pl = responses.pop(0)
        if op not in (0x0042, 0x036C, 0x0002):  # skip heartbeat/tick
            found.append((op, pl))
            log(f"    <- 0x{op:04X} {opname(op)} ({len(pl)}B) payload={pl[:20].hex()}")
    if not found:
        log(f"    (no responses for {label})")
    return found

def main():
    log("=== BUILD & DEMOLISH TEST ===")

    # Login
    access_key = node_login(EMAIL, PASSWORD, IGG_ID)
    if not access_key:
        log("Login failed!"); return
    log(f"Access key: {access_key[:8]}...")

    # Gateway
    gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    log(f"Server: {gw['ip']}:{gw['port']}")

    # Connect
    gc = GameConnection(IGG_ID, gw['ip'], gw['port'], gw['token'])
    gc.on_packet(on_packet)
    gc.connect()

    if not gc.codec:
        log("No codec!"); gc.disconnect(); return

    cmd = CommandEngine(IGG_ID, gc.codec)
    time.sleep(3)
    responses.clear()

    # ──── TEST 1: DEMOLISH visual slot 7 = real slot 75 (0x4B) ────
    # Using PCAP-verified old-style 0x009D
    log("")
    log("=== TEST 1: DEMOLISH slot 7 (real=75, 0x4B) via 0x009D ===")
    demolish_payload = bytearray(12)
    demolish_payload[0] = 0x05  # demolish action code
    demolish_payload[1] = 75    # real slot id
    gc.send(build_packet(0x009D, bytes(demolish_payload)))
    r1 = wait_and_collect("Demolish slot 75")

    # Check for 0x009E (demolish response)
    has_009e = any(op == 0x009E for op, _ in r1)
    has_0098 = any(op == 0x0098 for op, _ in r1)
    log(f"  Demolish result: 0x009E={'YES' if has_009e else 'NO'}, 0x0098={'YES' if has_0098 else 'NO'}")

    # ──── TEST 2: UPGRADE visual slot 27 = real slot 74 (0x4A) ────
    # Try with new-style 0x0CEF
    # We don't know the building type, so try with type=0 or let server figure it out
    log("")
    log("=== TEST 2: UPGRADE slot 27 (real=74, 0x4A) via 0x0CEF ===")
    # First try: building_type from slot data - we'll try common types
    # Slot 74 is an outer slot, could be farm(51), mine(52), lumber(53), quarry(55), manor(56)
    # Let's try upgrade with operation=1, and see what the server says
    gc.send(cmd.upgrade(building_type=0, slot=74))
    r2 = wait_and_collect("Upgrade slot 74 (type=0)")

    # If no good response, try with specific building types
    if not any(op in (0x02D1, 0x021C, 0x11C8, 0x0097) for op, _ in r2):
        log("  No confirm, trying type=51 (farm)...")
        gc.send(cmd.upgrade(building_type=51, slot=74))
        r2b = wait_and_collect("Upgrade slot 74 (type=51)")

        if not any(op in (0x02D1, 0x021C, 0x11C8, 0x0097) for op, _ in r2b):
            log("  No confirm, trying type=52 (mine)...")
            gc.send(cmd.upgrade(building_type=52, slot=74))
            r2c = wait_and_collect("Upgrade slot 74 (type=52)")

    # ──── Also try old-style build for upgrade ────
    log("")
    log("=== TEST 3: UPGRADE slot 74 via old-style 0x009D (op=01) ===")
    upgrade_payload = bytearray(12)
    upgrade_payload[0] = 0x01  # upgrade action code
    upgrade_payload[1] = 74    # slot id (0x4A)
    gc.send(build_packet(0x009D, bytes(upgrade_payload)))
    r3 = wait_and_collect("Old-style upgrade slot 74")

    log("")
    log("=== DONE ===")
    time.sleep(3)
    gc.disconnect()

if __name__ == '__main__':
    main()

"""
Live Test Script - IGG Conquerors Bot
Tests: Node Login → Gateway → Game Server → Train → Build → Enable View
"""
import sys
import time
import struct
import subprocess
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from game_server import GameConnection
from commands import CommandEngine
from protocol import opname

def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def node_login(email, password, igg_id):
    """Use Node.js for HTTP login (bypasses Cloudflare issues)."""
    result = subprocess.run(
        ['node', r'D:\CascadeProjects\lords_bot\http_login.mjs', email, password, str(igg_id)],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        log(f"Node login STDERR: {result.stderr}")
        return None
    token = result.stdout.strip()
    if len(token) == 32:
        return token
    log(f"Node login returned unexpected: {token[:50]}")
    return None

# Track responses
responses = []
def on_packet(opcode, payload):
    responses.append((opcode, payload))

def wait_for_response(label, timeout=5):
    """Wait for server responses after sending a command."""
    time.sleep(timeout)
    found = []
    while responses:
        op, pl = responses.pop(0)
        found.append((op, pl, f"0x{op:04X} {opname(op)} ({len(pl)}B)"))
    if found:
        log(f"  Responses for {label}:")
        for _, _, desc in found:
            log(f"    <- {desc}")
    else:
        log(f"  No responses for {label}")
    return found

def main():
    log(f"=== LIVE TEST START ===")
    log(f"Account: {EMAIL} / IGG_ID: {IGG_ID}")

    # ──── STEP 1: Node.js HTTP Login ────
    log("--- STEP 1: HTTP Login (Node.js) ---")
    access_key = node_login(EMAIL, PASSWORD, IGG_ID)
    if not access_key:
        log("HTTP Login FAILED!")
        return
    log(f"Access Key: {access_key}")

    # ──── STEP 2: Gateway Auth ────
    log("--- STEP 2: Gateway Auth ---")
    try:
        gw = connect_gateway(IGG_ID, access_key, WORLD_ID)
    except Exception as e:
        log(f"Gateway FAILED: {e}")
        return
    log(f"Game Server: {gw['ip']}:{gw['port']}")
    log(f"Session Token: {gw['token'][:16]}...")

    # ──── STEP 3: Game Server Connect ────
    log("--- STEP 3: Game Server Connect ---")
    gc = GameConnection(IGG_ID, gw['ip'], gw['port'], gw['token'])
    gc.on_packet(on_packet)
    try:
        gc.connect()
    except Exception as e:
        log(f"Game Server FAILED: {e}")
        return

    gs = gc.game_state
    try:
        log(f"Player: {gs.player_name}")
    except Exception:
        log(f"Player: (non-ASCII name, {len(gs.player_name)} chars)")
    log(f"Server Key: {'0x{:08x}'.format(gs.server_key) if gs.server_key else 'NOT FOUND!'}")
    res = gs.resources
    log(f"Resources: food={res.get('food',0)}, stone={res.get('stone',0)}, wood={res.get('wood',0)}, ore={res.get('ore',0)}, gold={res.get('gold',0)}")
    log(f"Power: {gs.power}")

    if not gc.codec:
        log("CODEC NOT READY - cannot test encrypted commands!")
        gc.disconnect()
        return

    cmd = CommandEngine(IGG_ID, gc.codec)

    # Clear initial responses
    time.sleep(3)
    responses.clear()

    results = {}

    # ──── TEST 1: Enable View ────
    log("--- TEST 1: Enable View (0x0CEB) ---")
    gc.send(cmd.enable_view(0x01, 0x01))
    r1 = wait_for_response("Enable View")
    results['enable_view'] = r1

    # ──── TEST 2: Train Infantry (type=1) ────
    log("--- TEST 2: Train Infantry (type=1, count=10) ---")
    gc.send(cmd.train(troop_type=1, count=10))
    r2 = wait_for_response("Train Infantry")
    results['train_infantry'] = r2

    # ──── TEST 3: Train Cavalry (type=2) ────
    log("--- TEST 3: Train Cavalry (type=2, count=10) ---")
    gc.send(cmd.train(troop_type=2, count=10))
    r3 = wait_for_response("Train Cavalry")
    results['train_cavalry'] = r3

    # ──── TEST 4: Train Ranged (type=4) ────
    log("--- TEST 4: Train Ranged (type=4, count=10) ---")
    gc.send(cmd.train(troop_type=4, count=10))
    r4 = wait_for_response("Train Ranged")
    results['train_ranged'] = r4

    # ──── TEST 5: Train Wheels (type=8) ────
    log("--- TEST 5: Train Wheels (type=8, count=10) ---")
    gc.send(cmd.train(troop_type=8, count=10))
    r5 = wait_for_response("Train Wheels")
    results['train_wheels'] = r5

    # ──── TEST 6: Upgrade Embassy (slot=3, type=3) ────
    log("--- TEST 6: Upgrade Embassy (type=3, slot=3) ---")
    gc.send(cmd.upgrade(building_type=3, slot=3))
    r6 = wait_for_response("Upgrade Embassy")
    results['upgrade'] = r6

    # ──── TEST 7: Research ────
    log("--- TEST 7: Research (tech_id=1) ---")
    gc.send(cmd.research(tech_id=1, tech_category=0))
    r7 = wait_for_response("Research")
    results['research'] = r7

    # ──── SUMMARY ────
    log("")
    log("=" * 60)
    log("  TEST SUMMARY")
    log("=" * 60)
    log(f"  HTTP Login:     OK (access_key={access_key[:8]}...)")
    log(f"  Gateway Auth:   OK ({gw['ip']}:{gw['port']})")
    log(f"  Game Connect:   OK")
    log(f"  Server Key:     {'OK (0x{:08x})'.format(gs.server_key) if gs.server_key else 'MISSING!'}")
    try:
        log(f"  Player:         {gs.player_name}")
    except Exception:
        log(f"  Player:         (non-ASCII)")
    log(f"  Power:          {gs.power}")
    log("")

    for name, resp_list in results.items():
        opcodes = [f"0x{op:04X}" for op, _, _ in resp_list]
        has_confirm = any(op in (0x06C4, 0x02D1, 0x11C8, 0x021C) for op, _, _ in resp_list)
        status = "SUCCESS" if has_confirm else f"{len(resp_list)} responses"
        if not resp_list:
            status = "NO RESPONSE"
        log(f"  {name:20s}: {status} {opcodes}")

    # Late responses
    time.sleep(5)
    if responses:
        log("\nLate responses:")
        while responses:
            op, pl = responses.pop(0)
            log(f"  <- 0x{op:04X} {opname(op)} ({len(pl)}B)")

    gc.disconnect()
    log("=== DONE ===")

if __name__ == '__main__':
    main()

"""
Auto-run bot: connects, collects daily rewards, then gathers resources.
Non-interactive - runs everything automatically.
"""
import sys
import os
import time
import struct
import threading
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import IGG_ID, WORLD_ID, STORED_ACCESS_KEY
from protocol import opname
from auth import extract_key_from_adb
from gateway import connect_gateway
from game_server import GameConnection
from commands import CommandEngine
from packets import build_packet


def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    line = f"[{ts}] [{level}] {msg}"
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        print(line.encode('ascii', 'replace').decode('ascii'), flush=True)


def main():
    # Get access key
    access_key = STORED_ACCESS_KEY
    if "--adb" in sys.argv:
        access_key = extract_key_from_adb() or access_key

    if not access_key or len(access_key) != 32:
        log("No valid access key!", "ERROR")
        return

    log(f"Access Key: {access_key}")
    log(f"IGG ID: {IGG_ID}, World: {WORLD_ID}")

    # Phase 1: Gateway
    log("=" * 50)
    gw_info = connect_gateway(IGG_ID, access_key, WORLD_ID)
    log(f"Game server: {gw_info['ip']}:{gw_info['port']}")

    # Phase 2: Game Server
    conn = GameConnection(IGG_ID, gw_info['ip'], gw_info['port'], gw_info['token'])

    # Track interesting responses
    responses = []
    def on_pkt(op, pl):
        if op not in (0x0042, 0x036C, 0x0002):  # skip heartbeat/spam
            responses.append((op, pl))

    conn.on_packet(on_pkt)
    conn.connect()

    # Phase 3: Setup commands
    cmds = CommandEngine(IGG_ID, conn.codec)

    gs = conn.game_state
    log("=" * 50)
    log(f"Player: {gs.player_name or '(name)'}")
    log(f"Power: {gs.power:,}")
    log(f"VIP: {gs.vip_level}")
    log(f"Resources: food={gs.resources.get('food',0):,} stone={gs.resources.get('stone',0):,} wood={gs.resources.get('wood',0):,} ore={gs.resources.get('ore',0):,} gold={gs.resources.get('gold',0):,}")
    log(f"Troops: {gs.get_total_troops():,} ({len(gs.troops)} types)")
    log(f"Items: {len(gs.items)} types, Speedups: {len(gs.get_speedup_items())}")
    log(f"Server Key: 0x{gs.server_key:08x}")
    log("=" * 50)

    # =====================================================
    # Phase 4: Daily Rewards
    # =====================================================
    log("")
    log(">>> PHASE 4: DAILY REWARDS <<<")
    responses.clear()
    packets = cmds.daily_routine()
    for pkt in packets:
        conn.send(pkt)
        time.sleep(0.3)
    log(f"Sent {len(packets)} daily reward packets")
    time.sleep(2)

    # Check responses
    for op, pl in responses:
        log(f"  Response: {opname(op)} (0x{op:04X}) {len(pl)}B")
        if op == 0x0037:  # Error
            if len(pl) >= 8:
                code, param = struct.unpack('<II', pl[:8])
                log(f"    Error code={code} param={param}")
            else:
                log(f"    Error payload: {pl.hex()}")
        elif op == 0x0033:  # SYN_ATTRIBUTE (resource update)
            if len(pl) >= 12:
                attr_id = struct.unpack('<I', pl[:4])[0]
                value = struct.unpack('<Q', pl[4:12])[0]
                ATTRS = {1:'food', 2:'stone', 3:'wood', 4:'ore', 6:'gold'}
                name = ATTRS.get(attr_id, f'attr_{attr_id}')
                log(f"    {name} = {value:,}")

    # =====================================================
    # Phase 5: Try Gather
    # =====================================================
    log("")
    log(">>> PHASE 5: GATHER RESOURCES <<<")
    responses.clear()

    # Search for resource tile
    log("Searching for resource tile (type=4, food)...")
    found = threading.Event()
    tile_pos = [None, None]

    def on_search(op, pl):
        if op == 0x033F and len(pl) >= 5 and tile_pos[0] is None:
            tile_pos[0] = struct.unpack('<H', pl[1:3])[0]
            tile_pos[1] = struct.unpack('<H', pl[3:5])[0]
            found.set()

    conn.on_packet(on_search)
    conn.send(build_packet(0x033E, struct.pack('<BHB', 0x01, 0x04, 0x03)))
    found.wait(timeout=5)
    conn._callbacks.remove(on_search)

    if tile_pos[0] is not None:
        x, y = tile_pos[0], tile_pos[1]
        log(f"Found resource tile at ({x}, {y})")

        # Enable view first
        conn.send(cmds.enable_view())
        time.sleep(0.3)

        # Send gather march
        pkt = cmds.gather(x, y, march_slot=1)
        conn.send(pkt)
        log(f"Sent GATHER march to ({x},{y}) slot=1")

        # Wait for response
        time.sleep(5)
        log("Responses after gather:")
        for op, pl in responses:
            log(f"  {opname(op)} (0x{op:04X}) {len(pl)}B")
            if op == 0x0037:
                if len(pl) >= 8:
                    code, param = struct.unpack('<II', pl[:8])
                    log(f"    Error: code={code} param={param}")
            elif op == 0x00B8:
                log(f"    MARCH_ACK: status={pl[0] if pl else -1}")
            elif op == 0x0071:
                log(f"    MARCH_STATE! March started successfully!")
    else:
        log("No resource tile found. Trying fixed coord gather...", "WARN")

    # =====================================================
    # Phase 6: Try Hunt Monster
    # =====================================================
    log("")
    log(">>> PHASE 6: HUNT MONSTER <<<")
    responses.clear()

    log("Searching for level 1 monster...")
    monster_found = threading.Event()
    monster_pos = [None, None]

    def on_monster(op, pl):
        if op == 0x033F and len(pl) >= 5 and monster_pos[0] is None:
            monster_pos[0] = struct.unpack('<H', pl[1:3])[0]
            monster_pos[1] = struct.unpack('<H', pl[3:5])[0]
            monster_found.set()

    conn.on_packet(on_monster)
    conn.send(cmds.find_monster(1))
    monster_found.wait(timeout=5)
    conn._callbacks.remove(on_monster)

    if monster_pos[0] is not None:
        mx, my = monster_pos[0], monster_pos[1]
        log(f"Found monster at ({mx}, {my})")

        conn.send(cmds.enable_view())
        time.sleep(0.3)

        pkt = cmds.attack_monster(mx, my, march_slot=2)
        conn.send(pkt)
        log(f"Sent ATTACK march to monster ({mx},{my}) slot=2")

        time.sleep(5)
        log("Responses after monster attack:")
        for op, pl in responses:
            log(f"  {opname(op)} (0x{op:04X}) {len(pl)}B")
            if op == 0x0037:
                if len(pl) >= 8:
                    code, param = struct.unpack('<II', pl[:8])
                    log(f"    Error: code={code} param={param}")
            elif op == 0x00B8:
                log(f"    MARCH_ACK: status={pl[0] if pl else -1}")
            elif op == 0x0071:
                log(f"    MARCH_STATE! March started!")
    else:
        log("No monster found", "WARN")

    # =====================================================
    # Phase 7: Stay alive, report status
    # =====================================================
    log("")
    log(">>> BOT RUNNING - heartbeat active <<<")
    log("Waiting 30 seconds to observe responses...")

    time.sleep(30)

    # Final status
    log("")
    log("=== FINAL STATUS ===")
    s = conn.status()
    log(f"Connected: {s['connected']}")
    log(f"Uptime: {s['uptime_seconds']}s")
    log(f"Sent: {s['total_sent']}B | Recv: {s['total_recv']}B")
    log(f"Active marches: {len(gs.marches)}")

    conn.disconnect()
    log("Done!")


if __name__ == "__main__":
    main()

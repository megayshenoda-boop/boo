"""
IGG Conquerors (الفاتحون) - Complete Bot
=========================================
Main orchestrator: login -> connect -> interactive CLI.

Usage:
  python bot.py                        # Use stored access key
  python bot.py --adb                  # Extract key from emulator via ADB
  python bot.py --key <access_key>     # Provide access key manually
  python bot.py --http                 # Full HTTP login flow
"""
import sys
import os
import time
import struct
import threading
from datetime import datetime

# Add parent to path for package imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import IGG_ID, WORLD_ID, STORED_ACCESS_KEY
from protocol import opname, BUILDINGS, TROOPS, BUILD_OP_UPGRADE, BUILD_OP_DEMOLISH, BUILD_OP_BUILD_NEW
from auth import http_login, extract_key_from_adb
from gateway import connect_gateway
from game_server import GameConnection
from commands import CommandEngine


LOG_FILE = None


def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    line = f"[{ts}] [{level}] {msg}"
    try:
        print(line)
    except UnicodeEncodeError:
        print(line.encode('ascii', 'replace').decode('ascii'))
    if LOG_FILE:
        LOG_FILE.write(line + "\n")
        LOG_FILE.flush()


class ConquerorsBot:
    """Main bot orchestrator."""

    def __init__(self, access_key):
        self.access_key = access_key
        self.conn = None
        self.cmds = None

    def start(self):
        """Full startup: Gateway -> Game Server -> Commands."""
        log("=" * 60)
        log("IGG Conquerors - COMPLETE BOT")
        log("=" * 60)
        log(f"IGG ID: {IGG_ID}")
        log(f"Access Key: {self.access_key}")

        # Phase 1: Gateway
        gw_info = connect_gateway(IGG_ID, self.access_key, WORLD_ID)

        # Phase 2: Game Server
        self.conn = GameConnection(
            IGG_ID, gw_info['ip'], gw_info['port'], gw_info['token']
        )
        self.conn.connect()

        # Phase 3: Setup commands
        self.cmds = CommandEngine(IGG_ID, self.conn.codec)

        log("")
        log("=== GAME STATE ===")
        log(self.conn.game_state.summary())
        log("")
        log("=" * 60)
        log("BOT ONLINE - Ready for commands")
        log("=" * 60)
        self._print_help()
        return True

    def _search_tile(self, tile_type=0x04, timeout=5):
        """Send 0x033E tile search and wait for 0x033F response.
        Returns (x, y) or (None, None)."""
        from packets import build_packet
        found = threading.Event()
        result = [None, None]

        def _on_search(op, pl):
            if op == 0x033F and len(pl) >= 5 and result[0] is None:
                result[0] = struct.unpack('<H', pl[1:3])[0]
                result[1] = struct.unpack('<H', pl[3:5])[0]
                found.set()

        self.conn.on_packet(_on_search)
        self.conn.send(build_packet(0x033E, struct.pack('<BHB', 0x01, tile_type, 0x03)))
        found.wait(timeout=timeout)
        self.conn._callbacks.remove(_on_search)
        return result[0], result[1]

    def _wait_march_ack(self, timeout=8):
        """Wait for 0x00B8 march acknowledgement."""
        log("  Waiting for MARCH_ACK (0x00B8)...")
        ack = threading.Event()

        def _on_ack(op, pl):
            if op == 0x00B8:
                if len(pl) >= 1 and pl[0] == 0:
                    log("  >>> MARCH OK", "INFO")
                else:
                    log(f"  >>> MARCH response: {pl.hex()}", "WARN")
                ack.set()

        self.conn.on_packet(_on_ack)
        ack.wait(timeout=timeout)
        self.conn._callbacks.remove(_on_ack)
        if not ack.is_set():
            log("  No MARCH_ACK in time - check troops/slot", "WARN")

    def _wait_monster_pos(self, timeout=5):
        """Wait for 0x033F monster position response.
        Returns (x, y) or (None, None)."""
        found = threading.Event()
        result = [None, None]

        def _on_pos(op, pl):
            if op == 0x033F and len(pl) >= 5 and result[0] is None:
                result[0] = struct.unpack('<H', pl[1:3])[0]
                result[1] = struct.unpack('<H', pl[3:5])[0]
                found.set()

        self.conn.on_packet(_on_pos)
        found.wait(timeout=timeout)
        self.conn._callbacks.remove(_on_pos)
        return result[0], result[1]

    def _print_help(self):
        log("")
        log("=== COMMANDS ===")
        log("")
        log("-- March / Combat --")
        log("  gather [x y] [slot]           - Gather resources (auto-search if no coords)")
        log("  attack <x> <y> [slot]         - Attack target tile")
        log("  scout <x> <y>                 - Scout target tile")
        log("  find_monster [level]          - Search for monsters (level 1-5)")
        log("  hunt [level] [slot]           - Find + attack monster (auto-rebel)")
        log("")
        log("-- Building / Training --")
        log("  train [type] [count]          - Train troops (type: 1=inf,2=ranged,4=cav,8=siege)")
        log("  build <type> <slot> [op]      - Build/upgrade/demolish (op: 1=up,2=demolish,3=new)")
        log("  upgrade <type> <slot>         - Upgrade shortcut")
        log("  demolish <type> <slot>        - Demolish shortcut")
        log("  research <tech_id> [cat]      - Start research")
        log("  heal [slot]                   - Heal troops")
        log("")
        log("-- Rewards / Daily --")
        log("  daily                         - Collect ALL daily rewards (sign+online+gifts)")
        log("  sign                          - Daily sign-in only")
        log("  rewards                       - Collect all reward packets")
        log("  quest_reward <id>             - Claim specific quest reward")
        log("  achievement <id>              - Claim achievement reward")
        log("")
        log("-- Items / Speedups --")
        log("  use_item <id> [count]         - Use item (speedup, shield, etc.)")
        log("  speedup [category]            - Use all speedups (general/build/research/train/heal)")
        log("  speed_train <item_id> [slot]  - Speed up training with item")
        log("")
        log("-- Alliance / Social --")
        log("  alliance_help                 - Send alliance help to all")
        log("  fire                          - Extinguish castle fire")
        log("")
        log("-- Info / Debug --")
        log("  view                          - Enable view (0x0CEB)")
        log("  status                        - Connection stats")
        log("  state                         - Game state (player, resources, troops)")
        log("  items                         - Show inventory")
        log("  troops                        - Show troop counts")
        log("  packets                       - Unique opcodes received")
        log("  raw <hex_opcode> [hex_data]   - Send raw packet")
        log("  help                          - Show this help")
        log("  quit                          - Disconnect")
        log("")

    def interactive(self):
        """Interactive command loop."""
        try:
            while self.conn and self.conn.running and self.conn.connected:
                try:
                    cmd = input("bot> ").strip()
                except EOFError:
                    break

                if not cmd:
                    continue

                parts = cmd.split()
                command = parts[0].lower()
                args = parts[1:]

                try:
                    self._handle_command(command, args)
                except Exception as e:
                    log(f"Command error: {e}", "ERROR")
        except KeyboardInterrupt:
            pass
        self.stop()

    def _handle_command(self, command, args):
        if command in ("quit", "exit"):
            self.conn.running = False
            return

        elif command == "help":
            self._print_help()

        elif command == "train":
            troop_type = int(args[0]) if args else 1
            count = int(args[1]) if len(args) > 1 else 10
            pkt = self.cmds.train(troop_type, count)
            self.conn.send(pkt)
            log(f"  Trained {count} troops (type={troop_type})")

        elif command == "build":
            if len(args) < 2:
                log("Usage: build <building_type> <slot> [operation]", "ERROR")
                return
            btype = int(args[0])
            slot = int(args[1])
            op = int(args[2]) if len(args) > 2 else BUILD_OP_UPGRADE
            pkt = self.cmds.build(btype, slot, op)
            self.conn.send(pkt)
            op_name = {1: "upgrade", 2: "demolish", 3: "build_new"}.get(op, str(op))
            log(f"  {op_name} building type={btype} slot={slot}")

        elif command == "upgrade":
            if len(args) < 2:
                log("Usage: upgrade <building_type> <slot>", "ERROR")
                return
            pkt = self.cmds.upgrade(int(args[0]), int(args[1]))
            self.conn.send(pkt)

        elif command == "demolish":
            if len(args) < 2:
                log("Usage: demolish <building_type> <slot>", "ERROR")
                return
            pkt = self.cmds.demolish(int(args[0]), int(args[1]))
            self.conn.send(pkt)

        elif command == "research":
            if not args:
                log("Usage: research <tech_id> [category]", "ERROR")
                return
            tech_id = int(args[0])
            cat = int(args[1]) if len(args) > 1 else 0
            pkt = self.cmds.research(tech_id, cat)
            self.conn.send(pkt)
            log(f"  Research tech={tech_id} cat={cat}")

        elif command == "view":
            pkt = self.cmds.enable_view()
            self.conn.send(pkt)

        elif command == "gather":
            slot = int(args[2]) if len(args) > 2 else 1

            # Auto-search if no coordinates given
            if len(args) < 2:
                log("Searching for nearby resource tiles (0x033E)...")
                x, y = self._search_tile(tile_type=0x04)
                if x is None:
                    log("No resource tile found. Pass coords manually: gather <x> <y>", "ERROR")
                    return
                log(f"  Search found tile: ({x},{y})")
            else:
                x, y = int(args[0]), int(args[1])

            self.conn.send(self.cmds.enable_view())
            time.sleep(0.2)
            pkt = self.cmds.gather(x, y, march_slot=slot)
            self.conn.send(pkt)
            log(f"  Gather -> tile=({x},{y}) slot={slot}")
            self._wait_march_ack()

        elif command == "attack":
            if len(args) < 2:
                log("Usage: attack <x> <y> [slot]", "ERROR")
                return
            x, y = int(args[0]), int(args[1])
            slot = int(args[2]) if len(args) > 2 else 1
            self.conn.send(self.cmds.enable_view())
            time.sleep(0.2)
            pkt = self.cmds.attack(x, y, march_slot=slot)
            self.conn.send(pkt)
            log(f"  Attack -> tile=({x},{y}) slot={slot}")
            self._wait_march_ack()

        elif command == "scout":
            if len(args) < 2:
                log("Usage: scout <x> <y>", "ERROR")
                return
            x, y = int(args[0]), int(args[1])
            pkt = self.cmds.scout(x, y)
            self.conn.send(pkt)
            log(f"  Scout -> tile=({x},{y})")

        elif command == "find_monster":
            level = int(args[0]) if args else 1
            pkt = self.cmds.find_monster(level)
            self.conn.send(pkt)
            log(f"  Searching for level {level} monsters...")

        elif command == "hunt":
            level = int(args[0]) if args else 1
            slot = int(args[1]) if len(args) > 1 else 1
            log(f"  Hunting level {level} monster...")
            # Step 1: Find monster
            self.conn.send(self.cmds.find_monster(level))
            x, y = self._wait_monster_pos()
            if x is None:
                log("No monster found.", "ERROR")
                return
            log(f"  Monster found at ({x},{y})")
            # Step 2: Attack
            self.conn.send(self.cmds.enable_view())
            time.sleep(0.2)
            pkt = self.cmds.attack_monster(x, y, march_slot=slot)
            self.conn.send(pkt)
            log(f"  Attacking monster at ({x},{y}) slot={slot}")
            self._wait_march_ack()

        elif command == "use_item":
            if not args:
                log("Usage: use_item <item_id> [count] [target_id]", "ERROR")
                return
            item_id = int(args[0])
            count = int(args[1]) if len(args) > 1 else 1
            target = int(args[2]) if len(args) > 2 else 0
            pkt = self.cmds.use_item(item_id, count, target)
            self.conn.send(pkt)
            log(f"  Used item {item_id} x{count}")

        elif command == "speed_train":
            if not args:
                log("Usage: speed_train <item_id> [building_slot]", "ERROR")
                return
            item_id = int(args[0])
            slot = int(args[1]) if len(args) > 1 else 0
            pkt = self.cmds.speed_train(item_id, slot)
            self.conn.send(pkt)
            log(f"  Speed train with item {item_id}")

        elif command == "heal":
            slot = int(args[0]) if args else 0
            pkt = self.cmds.heal_troops(slot)
            self.conn.send(pkt)

        # -- Rewards / Daily --

        elif command == "daily":
            log("Collecting ALL daily rewards + alliance help...")
            packets = self.cmds.daily_routine()
            for pkt in packets:
                self.conn.send(pkt)
                time.sleep(0.3)
            log(f"  Sent {len(packets)} reward/daily packets")

        elif command == "sign":
            self.conn.send(self.cmds.daily_sign())
            log("  Daily sign-in sent")

        elif command == "rewards":
            packets = self.cmds.collect_all_rewards()
            for pkt in packets:
                self.conn.send(pkt)
                time.sleep(0.3)
            log(f"  Sent {len(packets)} reward collection packets")

        elif command == "quest_reward":
            if not args:
                log("Usage: quest_reward <quest_id>", "ERROR")
                return
            self.conn.send(self.cmds.quest_reward(int(args[0])))
            log(f"  Claimed quest reward {args[0]}")

        elif command == "achievement":
            if not args:
                log("Usage: achievement <achievement_id>", "ERROR")
                return
            self.conn.send(self.cmds.achievement_reward(int(args[0])))
            log(f"  Claimed achievement reward {args[0]}")

        # -- Speedups --

        elif command == "speedup":
            cat = args[0] if args else 'general'
            inv = self.conn.game_state.items
            if not inv:
                log("No items in inventory yet (wait for ITEM_INFO)", "WARN")
                return
            packets = self.cmds.use_all_speedups(inv, category=cat)
            if not packets:
                log(f"  No {cat} speedup items in inventory", "WARN")
                return
            for pkt in packets:
                self.conn.send(pkt)
                time.sleep(0.1)
            log(f"  Used {len(packets)} {cat} speedup items")

        # -- Alliance / Social --

        elif command == "alliance_help":
            self.conn.send(self.cmds.alliance_help())
            log("  Alliance help sent")

        elif command == "fire":
            self.conn.send(self.cmds.extinguish_fire())
            log("  Extinguish fire sent")

        # -- Info --

        elif command == "items":
            gs = self.conn.game_state
            if not gs.items:
                log("No items received yet (wait for ITEM_INFO 0x0064)", "WARN")
                return
            log(f"Inventory ({len(gs.items)} types):")
            for iid, qty in sorted(gs.items.items()):
                if qty > 0:
                    tag = " [SPEEDUP]" if 1100 <= iid <= 1155 else ""
                    log(f"  #{iid}: x{qty}{tag}")

        elif command in ("troops", "army"):
            gs = self.conn.game_state
            if not gs.troops:
                log("No troop data yet (wait for SOLDIER_INFO 0x06C2)", "WARN")
                return
            TROOP_NAMES = {1: "Infantry", 2: "Ranged", 4: "Cavalry", 8: "Siege"}
            log(f"Troops ({gs.get_total_troops():,} total):")
            for ttype, cnt in sorted(gs.troops.items()):
                name = TROOP_NAMES.get(ttype, f"Type_{ttype}")
                log(f"  {name} (type={ttype}): {cnt:,}")

        elif command == "status":
            s = self.conn.status()
            elapsed = s['uptime_seconds']
            log(f"Connected: {s['connected']}")
            log(f"Uptime: {elapsed}s ({elapsed/60:.1f}m)")
            log(f"Server: {s['server']}")
            log(f"Sent: {s['total_sent']}B | Recv: {s['total_recv']}B")
            log(f"Server Key: {s['server_key'] or 'N/A'}")

        elif command == "state":
            log("=== GAME STATE ===")
            log(self.conn.game_state.summary())

        elif command == "packets":
            log("Unique opcodes received:")
            for op in sorted(self.conn.game_state.raw_packets.keys()):
                cnt = len(self.conn.game_state.raw_packets[op])
                log(f"  0x{op:04X} {opname(op):25s} x{cnt}")

        elif command == "raw":
            if not args:
                log("Usage: raw <hex_opcode> [hex_payload]", "ERROR")
                return
            op = int(args[0], 16)
            payload = bytes.fromhex(args[1]) if len(args) > 1 else b''
            from packets import build_packet
            pkt = build_packet(op, payload)
            self.conn.send(pkt)

        elif command == "buildings":
            log("Building IDs:")
            for name, bid in sorted(BUILDINGS.items(), key=lambda x: x[1]):
                log(f"  {bid:3d} = {name}")

        elif command == "troops":
            log("Troop IDs:")
            for name, tid in sorted(TROOPS.items(), key=lambda x: x[1]):
                log(f"  {tid:3d} = {name}")

        else:
            log(f"Unknown command: {command}. Type 'help'.")

    def stop(self):
        """Graceful shutdown."""
        log("Shutting down...")
        if self.conn:
            self.conn.disconnect()
        log("Bot stopped.")


def main():
    global LOG_FILE
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(script_dir, "bot_session.log")
    LOG_FILE = open(log_path, "w", encoding="utf-8")

    access_key = None

    if "--http" in sys.argv:
        access_key = http_login()
        if not access_key:
            log("HTTP login failed! Try --adb or --key instead.", "ERROR")
            LOG_FILE.close()
            return

    elif "--adb" in sys.argv:
        access_key = extract_key_from_adb()
        if not access_key:
            log("ADB extraction failed! Using stored key.", "WARN")
            access_key = STORED_ACCESS_KEY

    elif "--key" in sys.argv:
        idx = sys.argv.index("--key")
        if idx + 1 < len(sys.argv):
            access_key = sys.argv[idx + 1]
        else:
            log("--key requires a value", "ERROR")
            LOG_FILE.close()
            return

    if not access_key:
        access_key = STORED_ACCESS_KEY
        log(f"Using stored access key: {access_key}")

    if len(access_key) != 32:
        log(f"Invalid access key length: {len(access_key)} (need 32)", "ERROR")
        LOG_FILE.close()
        return

    bot = ConquerorsBot(access_key)
    try:
        if bot.start():
            bot.interactive()
    except Exception as e:
        log(f"Bot error: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        bot.stop()

    LOG_FILE.close()


if __name__ == "__main__":
    main()

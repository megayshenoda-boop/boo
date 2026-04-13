"""
IGG Conquerors Bot - Auto Farm Module
=======================================
Autonomous farming loops for resource gathering, training, and daily rewards.
All loops respect error codes and reconnect logic.

Usage:
    farmer = AutoFarmer(bot)
    farmer.start_gather_loop()     # Auto-gather resources
    farmer.start_daily_loop()      # Auto-collect rewards every 24h
    farmer.start_train_loop()      # Auto-train troops when idle
"""
import time
import threading
from datetime import datetime

from error_codes import get_error_info, should_retry, should_reconnect


def _log(msg, level="FARM"):
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{ts}] [{level}] {msg}")


class AutoFarmer:
    """Manages automated farming activities."""

    def __init__(self, bot):
        self.bot = bot
        self.running = False
        self._threads = []
        # Configurable intervals (seconds)
        self.gather_check_interval = 60      # Check march status every 60s
        self.daily_interval = 3600 * 4       # Collect rewards every 4 hours
        self.train_interval = 300            # Check training every 5 min
        self.reward_delay = 1.5              # Delay between reward packets

    def start(self):
        """Start all farming loops."""
        self.running = True
        _log("Auto-farmer starting...")
        self._start_thread("gather", self._gather_loop)
        self._start_thread("daily", self._daily_loop)
        self._start_thread("train", self._train_loop)
        _log(f"Auto-farmer active ({len(self._threads)} threads)")

    def stop(self):
        """Stop all farming loops."""
        _log("Auto-farmer stopping...")
        self.running = False
        for t in self._threads:
            t.join(timeout=5)
        self._threads.clear()
        _log("Auto-farmer stopped")

    def _start_thread(self, name, target):
        t = threading.Thread(target=target, name=f"farm_{name}", daemon=True)
        t.start()
        self._threads.append(t)

    # ══════════════════════════════════════════════════════════
    #  GATHER LOOP
    # ══════════════════════════════════════════════════════════

    def _gather_loop(self):
        """Main gather loop: find resource → march → wait → repeat."""
        _log("Gather loop started")
        while self.running:
            try:
                conn = self.bot.conn
                if not conn or not conn.connected:
                    _log("Not connected, waiting...", "WARN")
                    time.sleep(30)
                    continue

                gs = conn.game_state
                active = len(gs.marches)
                max_slots = self._get_max_march_slots(gs)

                if active < max_slots:
                    _log(f"March slots: {active}/{max_slots} used, sending gather...")
                    # TODO: Implement tile search (0x033E) → response (0x033F) → gather
                    # For now, log that we'd gather
                    _log("TODO: Implement auto-search + gather flow")
                else:
                    _log(f"All march slots busy ({active}/{max_slots})")

                time.sleep(self.gather_check_interval)

            except Exception as e:
                _log(f"Gather loop error: {e}", "ERROR")
                time.sleep(30)

        _log("Gather loop stopped")

    # ══════════════════════════════════════════════════════════
    #  DAILY REWARDS LOOP
    # ══════════════════════════════════════════════════════════

    def _daily_loop(self):
        """Collect all daily rewards periodically."""
        _log("Daily rewards loop started")
        while self.running:
            try:
                conn = self.bot.conn
                if not conn or not conn.connected:
                    time.sleep(30)
                    continue

                _log("Collecting daily rewards...")
                cmd = self.bot.cmd
                if not cmd:
                    time.sleep(60)
                    continue

                # Original rewards
                packets = cmd.collect_all_rewards()
                for pkt in packets:
                    if not self.running:
                        break
                    conn.send(pkt)
                    time.sleep(self.reward_delay)

                # New rewards from audit
                new_packets = cmd.collect_new_rewards()
                for pkt in new_packets:
                    if not self.running:
                        break
                    conn.send(pkt)
                    time.sleep(self.reward_delay)

                _log(f"Sent {len(packets) + len(new_packets)} reward packets")

                # Alliance help
                try:
                    conn.send(cmd.alliance_help())
                except Exception:
                    pass

                _log(f"Next reward collection in {self.daily_interval}s")
                time.sleep(self.daily_interval)

            except Exception as e:
                _log(f"Daily loop error: {e}", "ERROR")
                time.sleep(60)

        _log("Daily rewards loop stopped")

    # ══════════════════════════════════════════════════════════
    #  TRAINING LOOP
    # ══════════════════════════════════════════════════════════

    def _train_loop(self):
        """Auto-train troops when queue is available."""
        _log("Training loop started")
        while self.running:
            try:
                conn = self.bot.conn
                if not conn or not conn.connected:
                    time.sleep(30)
                    continue

                # Check last error - if queue full, wait longer
                gs = conn.game_state
                if gs.last_error and gs.last_error[0] == 10:  # QUEUE_FULL
                    _log("Training queue full, waiting...")
                    time.sleep(120)
                    continue

                # TODO: Smart training based on troop composition
                # For now, just log status
                total = gs.get_total_troops() if hasattr(gs, 'get_total_troops') else 0
                _log(f"Troops: {total:,}")

                time.sleep(self.train_interval)

            except Exception as e:
                _log(f"Train loop error: {e}", "ERROR")
                time.sleep(60)

        _log("Training loop stopped")

    # ══════════════════════════════════════════════════════════
    #  HELPERS
    # ══════════════════════════════════════════════════════════

    def _get_max_march_slots(self, game_state):
        """Get max march slots based on VIP level."""
        vip = game_state.vip_level
        if vip >= 15:
            return 5
        elif vip >= 8:
            return 4
        elif vip >= 3:
            return 3
        elif vip >= 1:
            return 2
        return 1

    def status(self):
        """Return auto-farmer status dict."""
        return {
            'running': self.running,
            'threads': len(self._threads),
            'gather_interval': self.gather_check_interval,
            'daily_interval': self.daily_interval,
            'train_interval': self.train_interval,
        }

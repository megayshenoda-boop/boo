"""
IGG Conquerors Bot - Game State Parser
========================================
Tracks all received game data: player profile, resources, buildings, troops, etc.
"""
import struct
import time
from datetime import datetime

from protocol import (
    OP_CASTLE_DATA, OP_PLAYER_PROFILE,
    OP_ITEM_INFO, OP_SOLDIER_INFO, OP_HERO_INFO,
    OP_SYN_ATTRIBUTE, OP_MARCH_STATE, OP_ERROR_STATUS,
    OP_MARCH_ACK,
)
from codec import extract_server_key_from_0x0038


def _log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{ts}] [{level}] {msg}")


class GameState:
    """Tracks all received game data."""

    def __init__(self):
        self.player_name = ""
        self.power = 0
        self.resources = {}
        self.vip_level = 0
        self.server_key = None
        self.raw_packets = {}
        self.buildings = {}       # {slot_id: {type, level, raw}}
        self.troops = {}          # {troop_type: count}
        self.items = {}           # {item_id: quantity}
        self.heroes = {}          # {hero_id: hero_data_dict}
        self.marches = {}         # {march_id: march_data_dict}
        self.attributes = {}      # {attr_id: value} from SYN_ATTRIBUTE
        self.last_error = None    # (error_code, param, message) from 0x0037
        self.last_march_ack = None
        self.last_update = 0
        # New: Password gate (0x1B8A)
        self.password_gate = None       # None=not received, False=skip, True=need pw
        self.password_challenge = None  # Raw challenge payload
        # New: Server time
        self.server_time = 0

    def update(self, opcode, payload):
        """Process an incoming packet and update state."""
        if opcode not in self.raw_packets:
            self.raw_packets[opcode] = []
        self.raw_packets[opcode].append(payload)
        self.last_update = time.time()

        if opcode == OP_CASTLE_DATA:
            key = extract_server_key_from_0x0038(payload)
            if key is not None:
                self.server_key = key
                _log(f"*** SERVER KEY EXTRACTED: 0x{key:08x} ***")

        elif opcode == OP_PLAYER_PROFILE:
            self._parse_profile(payload)

        elif opcode == 0x07E4:
            if len(payload) >= 8:
                self.vip_level = payload[7]

        elif opcode == OP_ITEM_INFO:
            self._parse_items(payload)

        elif opcode == OP_SOLDIER_INFO:
            self._parse_soldiers(payload)

        elif opcode == OP_HERO_INFO:
            self._parse_heroes(payload)

        elif opcode == OP_SYN_ATTRIBUTE:
            self._parse_syn_attribute(payload)

        elif opcode == OP_MARCH_STATE:
            self._parse_march_state(payload)

        elif opcode == OP_ERROR_STATUS:
            self._parse_error(payload)

        elif opcode == OP_MARCH_ACK:
            self._parse_march_ack(payload)

        elif opcode == 0x1B8A:  # PASSWORD_INFO gate
            self._parse_password_info(payload)

        elif opcode == 0x0097:  # BUILDING_INFO
            self._parse_buildings(payload)

        elif opcode == 0x0070:  # MARCH_RECALL
            self._parse_march_recall(payload)

        elif opcode == 0x006F:  # SYNC_MARCH
            self._parse_sync_march(payload)

        elif opcode == 0x0043:  # SERVER_TIME
            self._parse_server_time(payload)

    def _parse_profile(self, payload):
        """Parse 0x0034 player profile packet."""
        if len(payload) < 10:
            return
        name_len = struct.unpack('<H', payload[0:2])[0]
        if 1 <= name_len <= 50 and 2 + name_len <= len(payload):
            try:
                self.player_name = payload[2:2+name_len].decode('utf-8')
            except Exception:
                pass
        base = 2 + name_len
        if base + 10 <= len(payload):
            self.power = struct.unpack('<I', payload[base+6:base+10])[0]
        res_start = base + 31
        res_names = ['food', 'stone', 'wood', 'ore', 'unknown', 'gold']
        for i, rname in enumerate(res_names):
            pos = res_start + i * 8
            if pos + 4 <= len(payload):
                val = struct.unpack('<I', payload[pos:pos+4])[0]
                if val > 0:
                    self.resources[rname] = val

    # ══════════════════════════════════════════════════════════
    #  PARSERS - Server Data Packets
    # ══════════════════════════════════════════════════════════

    def _parse_items(self, payload):
        """Parse ITEM_INFO (0x0064): u32 count + [u32 item_id, u32 qty] * N."""
        if len(payload) < 4:
            return
        count = struct.unpack('<I', payload[0:4])[0]
        pos = 4
        for _ in range(count):
            if pos + 8 > len(payload):
                break
            item_id, qty = struct.unpack('<II', payload[pos:pos+8])
            self.items[item_id] = qty
            pos += 8
        _log(f"ITEM_INFO: {count} items parsed ({len(self.items)} unique)")

    def _parse_soldiers(self, payload):
        """Parse SOLDIER_INFO (0x06C2): u32 count + entries.
        Troop types use bitmask: 1=infantry, 2=ranged, 4=cavalry, 8=siege.
        Entry format: u32 troop_type + u32 count (8B per entry, simplified).
        """
        if len(payload) < 4:
            return
        count = struct.unpack('<I', payload[0:4])[0]
        pos = 4
        entry_size = max(8, (len(payload) - 4) // count) if count > 0 else 8
        for _ in range(count):
            if pos + 8 > len(payload):
                break
            troop_type = struct.unpack('<I', payload[pos:pos+4])[0]
            troop_count = struct.unpack('<I', payload[pos+4:pos+8])[0]
            self.troops[troop_type] = troop_count
            pos += entry_size
        _log(f"SOLDIER_INFO: {count} troop types parsed")

    def _parse_heroes(self, payload):
        """Parse HERO_INFO (0x00AA): u32 count + 109B entries.
        We extract hero_id (u32 at offset 0) from each entry.
        """
        if len(payload) < 4:
            return
        count = struct.unpack('<I', payload[0:4])[0]
        pos = 4
        entry_size = 109
        for _ in range(count):
            if pos + entry_size > len(payload):
                break
            hero_id = struct.unpack('<I', payload[pos:pos+4])[0]
            self.heroes[hero_id] = {
                'id': hero_id,
                'raw': payload[pos:pos+entry_size],
            }
            pos += entry_size
        _log(f"HERO_INFO: {count} heroes parsed")

    def _parse_syn_attribute(self, payload):
        """Parse SYN_ATTRIBUTE (0x0033): u32 attr_id + u64 value.
        Updates resources and other attributes in real-time.
        """
        if len(payload) < 12:
            return
        attr_id = struct.unpack('<I', payload[0:4])[0]
        value = struct.unpack('<Q', payload[4:12])[0]
        self.attributes[attr_id] = value

        # Map known attribute IDs to resource names
        ATTR_FOOD  = 1
        ATTR_STONE = 2
        ATTR_WOOD  = 3
        ATTR_ORE   = 4
        ATTR_GOLD  = 6
        attr_map = {
            ATTR_FOOD: 'food', ATTR_STONE: 'stone', ATTR_WOOD: 'wood',
            ATTR_ORE: 'ore', ATTR_GOLD: 'gold',
        }
        if attr_id in attr_map:
            self.resources[attr_map[attr_id]] = value
            _log(f"SYN_ATTRIBUTE: {attr_map[attr_id]} = {value:,}")
        else:
            _log(f"SYN_ATTRIBUTE: attr_{attr_id} = {value}")

    def _parse_march_state(self, payload):
        """Parse MARCH_STATE (0x0071): march sync with coords, hero, player name.
        Format: march_id(u32) + kingdom(u16*2) + flags + hero_id(u16) +
                coords(u16*4) + player_name_len(u16) + name_string.
        """
        if len(payload) < 20:
            return
        march_id = struct.unpack('<I', payload[0:4])[0]
        march_data = {'id': march_id, 'raw_len': len(payload)}

        if len(payload) >= 8:
            march_data['kingdom_src'] = struct.unpack('<H', payload[4:6])[0]
            march_data['kingdom_dst'] = struct.unpack('<H', payload[6:8])[0]

        # Try to extract coordinates (approximate offsets from PCAP analysis)
        if len(payload) >= 24:
            march_data['hero_id'] = struct.unpack('<H', payload[12:14])[0]
            march_data['src_x'] = struct.unpack('<H', payload[14:16])[0]
            march_data['src_y'] = struct.unpack('<H', payload[16:18])[0]
            march_data['dst_x'] = struct.unpack('<H', payload[18:20])[0]
            march_data['dst_y'] = struct.unpack('<H', payload[20:22])[0]

        self.marches[march_id] = march_data
        _log(f"MARCH_STATE: march #{march_id} tracked (payload {len(payload)}B)")

    def _parse_error(self, payload):
        """Parse ERROR_STATUS (0x0037): u32 error_code + u32 param + u32 zero."""
        ERROR_CODES = {
            0: "OK", 1: "FAILED", 2: "INVALID_PARAM",
            3: "NOT_ENOUGH_RESOURCES", 5: "NOT_ENOUGH_TROOPS",
            7: "COOLDOWN", 10: "QUEUE_FULL", 13: "INVALID_TARGET",
            22: "TIME_ERROR", 38: "MARCH_SLOT_BUSY", 43: "ACCOUNT_ERROR",
        }
        if len(payload) < 12:
            return
        err_code, param, _ = struct.unpack('<III', payload[0:12])
        msg = ERROR_CODES.get(err_code, f"UNKNOWN_{err_code}")
        self.last_error = (err_code, param, msg)
        _log(f"ERROR: {msg} (code={err_code}, param={param})", level="WARN")

    def _parse_march_ack(self, payload):
        """Parse MARCH_ACK (0x00B8): 1B (0x00=ok) or 10B+ with details."""
        if len(payload) >= 1:
            status = payload[0]
            self.last_march_ack = status
            if status == 0:
                _log("MARCH_ACK: OK")
            else:
                _log(f"MARCH_ACK: status={status} (payload {len(payload)}B)", level="WARN")

    # ══════════════════════════════════════════════════════════
    #  NEW PARSERS (from audit reports 56-63)
    # ══════════════════════════════════════════════════════════

    def _parse_password_info(self, payload):
        """Parse PASSWORD_INFO (0x1B8A): gate signal for 0x1B8B.
        If gate byte [4] == 0: no secondary password, do NOT send 0x1B8B.
        If gate byte [4] != 0: must send 0x1B8B with challenge response.
        Discovery: decode_deep.py analysis confirmed this flow.
        """
        if len(payload) >= 5:
            gate = payload[4]
            if gate == 0:
                self.password_gate = False
                _log("PASSWORD_INFO: gate=0 (no secondary password - skip 0x1B8B)")
            else:
                self.password_gate = True
                self.password_challenge = payload
                _log(f"PASSWORD_INFO: gate={gate} (secondary password REQUIRED!)", "WARN")
        else:
            self.password_gate = False
            _log(f"PASSWORD_INFO: short payload ({len(payload)}B), assuming no password")

    def _parse_buildings(self, payload):
        """Parse BUILDING_INFO (0x0097): u16 count + 19B entries.
        Entry: u16 slot + u16 type + u16 level + 13B extra.
        """
        if len(payload) < 2:
            return
        count = struct.unpack('<H', payload[0:2])[0]
        pos = 2
        entry_size = 19
        for _ in range(count):
            if pos + entry_size > len(payload):
                break
            slot = struct.unpack('<H', payload[pos:pos+2])[0]
            btype = struct.unpack('<H', payload[pos+2:pos+4])[0]
            level = struct.unpack('<H', payload[pos+4:pos+6])[0]
            self.buildings[slot] = {
                'type': btype, 'level': level,
                'raw': payload[pos:pos+entry_size],
            }
            pos += entry_size
        _log(f"BUILDING_INFO: {count} buildings parsed")

    def _parse_march_recall(self, payload):
        """Parse MARCH_RECALL (0x0070): march returned, free the slot."""
        if len(payload) >= 4:
            march_id = struct.unpack('<I', payload[0:4])[0]
            if march_id in self.marches:
                del self.marches[march_id]
                _log(f"MARCH_RECALL: march #{march_id} returned (slot freed)")
            else:
                _log(f"MARCH_RECALL: march #{march_id} (was not tracked)")

    def _parse_sync_march(self, payload):
        """Parse SYNC_MARCH (0x006F): update march position."""
        if len(payload) >= 4:
            march_id = struct.unpack('<I', payload[0:4])[0]
            if march_id not in self.marches:
                self.marches[march_id] = {'id': march_id}
            self.marches[march_id]['last_sync'] = time.time()
            self.marches[march_id]['sync_data'] = payload

    def _parse_server_time(self, payload):
        """Parse SERVER_TIME (0x0043): u32 unix timestamp."""
        if len(payload) >= 4:
            self.server_time = struct.unpack('<I', payload[0:4])[0]

    # ══════════════════════════════════════════════════════════
    #  CONVENIENCE GETTERS
    # ══════════════════════════════════════════════════════════

    def get_speedup_items(self):
        """Return dict of speedup items from inventory {item_id: qty}."""
        return {k: v for k, v in self.items.items() if 1100 <= k <= 1155 and v > 0}

    def get_total_troops(self):
        """Return total troop count across all types."""
        return sum(self.troops.values())

    def has_available_march_slot(self, max_slots=5):
        """Check if there's a free march slot."""
        return len(self.marches) < max_slots

    def summary(self):
        """Human-readable game state summary."""
        lines = []
        if self.player_name:
            lines.append(f"  Player: {self.player_name}")
        if self.power:
            lines.append(f"  Power: {self.power:,}")
        if self.vip_level:
            lines.append(f"  VIP: {self.vip_level}")
        if self.resources:
            lines.append("  Resources:")
            for k, v in sorted(self.resources.items()):
                if isinstance(v, (int, float)) and v > 0:
                    lines.append(f"    {k}: {int(v):,}")
        if self.troops:
            lines.append(f"  Troops: {self.get_total_troops():,} ({len(self.troops)} types)")
        if self.heroes:
            lines.append(f"  Heroes: {len(self.heroes)}")
        if self.items:
            lines.append(f"  Items: {len(self.items)} types")
            speedups = self.get_speedup_items()
            if speedups:
                lines.append(f"    Speedups: {sum(speedups.values())} items")
        if self.buildings:
            lines.append(f"  Buildings: {len(self.buildings)}")
        if self.marches:
            lines.append(f"  Active marches: {len(self.marches)}")
        if self.last_error:
            lines.append(f"  Last error: {self.last_error[2]} (code={self.last_error[0]}, param={self.last_error[1]})")
        if self.password_gate is not None:
            lines.append(f"  Password gate: {'REQUIRED' if self.password_gate else 'not needed'}")
        if self.server_time:
            lines.append(f"  Server time: {self.server_time}")
        if self.server_key:
            lines.append(f"  Server Key: 0x{self.server_key:08x}")
        lines.append(f"  Unique opcodes: {len(self.raw_packets)}")
        return '\n'.join(lines)

    def to_dict(self):
        """Serializable state dict."""
        return {
            'player_name': self.player_name,
            'power': self.power,
            'resources': self.resources,
            'vip_level': self.vip_level,
            'server_key': f"0x{self.server_key:08x}" if self.server_key else None,
            'unique_opcodes': len(self.raw_packets),
            'last_update': self.last_update,
        }

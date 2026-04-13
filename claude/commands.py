"""
IGG Conquerors Bot - Command Engine
=====================================
All game commands with proper payload builders.
Opcodes verified via Capstone ARM64 disassembly of libgame.so constructors.

NEW-style payloads (0x0CE4-0x0CFB) use CMsgCodec encryption.
OLD-style payloads use direct struct packing (unencrypted).
"""
import os
import struct
import random

from protocol import (
    OP_HEARTBEAT,
    # New-style encrypted
    OP_START_BUILDUP, OP_JOIN_BUILDUP, OP_START_DEFEND, OP_BACK_DEFEND,
    OP_START_MARCH, OP_CANCEL_MARCH, OP_MARCH_USE_ITEM, OP_ENABLE_VIEW,
    OP_LEAGUE_DONATE, OP_TRAIN, OP_RESEARCH, OP_BUILD,
    OP_MOVE_CASTLE, OP_RAID_PLAYER, OP_MAIL_REQUEST, OP_SHOP_BUY,
    # Old-style unencrypted
    OP_ITEM_USE, OP_BUILD_HELP, OP_EXCHANGE_BUILD, OP_BUILD_ONEKEY,
    OP_RESEARCH_ITEM_SPD, OP_RESEARCH_HELP, OP_RESEARCH_CANCEL,
    OP_TRAP_BUILD, OP_TRAP_DESTROY,
    OP_TRAIN_ITEM_SPD, OP_TRAIN_COMPLETE, OP_TRAIN_ONEKEY,
    OP_HEAL, OP_HEAL_ITEM_SPD, OP_HEAL_COMPLETE, OP_HEAL_ONEKEY,
    # Reward/daily opcodes
    OP_SIGN_REQUEST, OP_APPEND_SIGN, OP_RECEIVE_SIGN_ACTIVITY,
    OP_ONLINE_REWARD, OP_RANDOM_ONLINE_REWARD, OP_EVERYDAY_GIFT,
    OP_ACHIEVEMENT_REWARD, OP_RECEIVE_REWARD, OP_RECEIVE_REWARD_BATCH,
    OP_ACCUMULATION_REWARD, OP_MICROPAY_DAILY, OP_DOWNLOAD_REWARD,
    OP_MOBILIZATION_REWARD, OP_ALLIANCE_HELP, OP_CITY_BUFF_USE,
    OP_REQUEST_MONSTER_POS, OP_OUTFIRE,
    # New reward opcodes (from audit report 57)
    OP_EVERYDAY_GIFT_NEW, OP_ACHIEVEMENT_SCORE, OP_LUXURY_REWARD,
    OP_KING_ROAD_REWARD, OP_EXP_REWARD, OP_EXTRA_GIFTPACK_NEW,
    OP_RETURN_EVENT_NEW, OP_ARENA_CHALLENGE, OP_ARENA_TIMES_RESTORE,
    OP_EXPEDITION_BATTLE, OP_LUCKY_TURNTABLE, OP_WHEEL_TURN,
    OP_DOUBLE_LOTTERY, OP_LEAGUEPASS_REWARD, OP_LEAGUEPASS_TASK,
    OP_LEAGUE_BF_REWARD, OP_BIG_BOSS_DONATE, OP_LOSTLAND_DONATE,
    OP_SERVER_MISSION, OP_DAILYCONSUME_REWARD, OP_RECHARGE_BONUS,
    OP_EXCHANGE_REWARD,
    # Game constants
    MARCH_TYPE_GATHER, BUILD_OP_UPGRADE, BUILD_OP_DEMOLISH, BUILD_OP_BUILD_NEW,
)
from packets import build_packet


class CommandEngine:
    """Builds action payloads for all discovered game commands."""

    def __init__(self, igg_id, codec=None):
        self.igg_id = igg_id
        self.codec = codec

    def set_codec(self, codec):
        self.codec = codec

    # ══════════════════════════════════════════════════════════
    #  PACKET HELPERS
    # ══════════════════════════════════════════════════════════

    def _plain_packet(self, opcode, payload=b''):
        """Build unencrypted packet: [2B len][2B opcode][payload]"""
        return build_packet(opcode, payload)

    def _encrypted_packet(self, opcode, action_data):
        """Build encrypted packet via CMsgCodec."""
        if not self.codec:
            raise RuntimeError("No CMsgCodec - server key not extracted yet")
        return self.codec.encode(opcode, action_data)

    # ══════════════════════════════════════════════════════════
    #  NEW-STYLE ENCRYPTED ACTIONS (0x0CE4-0x0CFB)
    # ══════════════════════════════════════════════════════════

    def train(self, troop_type=1, count=10):
        """Train troops (0x0CED = CMSG_SOLDIER_NORMAL_PRODUCE_REQUEST_NEW).
        ARM64 VERIFIED: 19B payload.

        Args:
            troop_type: 1=infantry, 2=cavalry, 4=ranged, 8=wheels/siege
            count: Number of troops to train
        """
        data = bytearray(19)
        struct.pack_into('<I', data, 0, troop_type)
        struct.pack_into('<I', data, 4, count)
        struct.pack_into('<I', data, 9, self.igg_id)
        return self._encrypted_packet(OP_TRAIN, bytes(data))

    def build(self, building_type, slot=0, operation=BUILD_OP_UPGRADE):
        """Build/Upgrade/Demolish (0x0CEF = CMSG_BUILDING_OPERAT_REQUEST_NEW).
        ARM64 VERIFIED: 22B payload.

        Args:
            building_type: Building type ID (see BUILDINGS dict)
            slot: Building slot position
            operation: BUILD_OP_UPGRADE(1), BUILD_OP_DEMOLISH(2), BUILD_OP_BUILD_NEW(3)
        """
        data = bytearray(22)
        data[0] = operation & 0xFF
        data[1] = building_type & 0xFF
        data[3] = slot & 0xFF
        data[11] = 1  # flag
        struct.pack_into('<I', data, 12, self.igg_id)
        return self._encrypted_packet(OP_BUILD, bytes(data))

    def demolish(self, building_type, slot=0):
        """Shortcut: Demolish a building."""
        return self.build(building_type, slot, BUILD_OP_DEMOLISH)

    def upgrade(self, building_type, slot=0):
        """Shortcut: Upgrade a building."""
        return self.build(building_type, slot, BUILD_OP_UPGRADE)

    def research(self, tech_id, tech_category=0):
        """Start research (0x0CEE = CMSG_SCIENCE_NORMAL_STUDY_REQUEST_NEW).
        ARM64 VERIFIED."""
        data = bytearray(12)
        struct.pack_into('<I', data, 0, tech_id)
        struct.pack_into('<I', data, 4, tech_category)
        struct.pack_into('<I', data, 8, 0)
        return self._encrypted_packet(OP_RESEARCH, bytes(data))

    def start_march(self, target_x, target_y, march_type=0x1749, march_slot=1,
                    kingdom_id=0xB6, hero_id=0xFF, resource_type=4):
        """Start a march (0x0CE8 = CMSG_START_MARCH_NEW).
        PCAP-VERIFIED 46-byte format (from real game client captures).

        Payload layout (46 bytes):
          [0]     march_slot (u8)
          [1:4]   random header (3 bytes)
          [4:6]   march_type (u16 LE) - 0x1749=gather, 0x174A=gather_w2
          [6:9]   zeros
          [9:11]  tile_x (u16 LE)
          [11:13] tile_y (u16 LE)
          [13]    0x01 flag
          [14]    hero_id (u8)
          [15:18] zeros
          [18]    kingdom_id (u8)
          [19:22] zeros
          [22]    resource_type (u8) - 4=food/wheat
          [23:33] zeros
          [33:37] igg_id (u32 LE)
          [37:46] zeros
        """
        data = bytearray(46)
        data[0] = march_slot & 0xFF
        data[1] = random.randint(0, 255)
        data[2] = random.randint(0, 255)
        data[3] = random.randint(0, 255)
        struct.pack_into('<H', data, 4, march_type)
        # [6:9] zeros
        struct.pack_into('<H', data, 9, target_x & 0xFFFF)
        struct.pack_into('<H', data, 11, target_y & 0xFFFF)
        data[13] = 0x01
        data[14] = hero_id & 0xFF
        # [15:18] zeros
        data[18] = kingdom_id & 0xFF
        # [19:22] zeros
        data[22] = resource_type & 0xFF
        # [23:33] zeros
        struct.pack_into('<I', data, 33, self.igg_id)
        # [37:46] zeros
        return self._encrypted_packet(OP_START_MARCH, bytes(data))

    def gather(self, target_x, target_y, march_slot=1, kingdom_id=0xB6,
               hero_id=0xFF, resource_type=4):
        """Gather resources from a tile. resource_type: 4=food/wheat."""
        return self.start_march(
            target_x, target_y, march_type=MARCH_TYPE_GATHER, march_slot=march_slot,
            kingdom_id=kingdom_id, hero_id=hero_id, resource_type=resource_type,
        )

    def attack(self, target_x, target_y, march_slot=1, kingdom_id=0xB6, hero_id=0xFF):
        """Attack a target tile."""
        return self.start_march(
            target_x, target_y, march_type=1, march_slot=march_slot,
            kingdom_id=kingdom_id, hero_id=hero_id, resource_type=0,
        )

    def scout(self, target_x, target_y, kingdom_id=0xB6):
        """Scout a target tile."""
        return self.start_march(
            target_x, target_y, march_type=2, march_slot=1,
            kingdom_id=kingdom_id, hero_id=0, resource_type=0,
        )

    def cancel_march(self, march_id):
        """Cancel a march (0x0CE9)."""
        data = struct.pack('<Q', march_id)
        return self._encrypted_packet(OP_CANCEL_MARCH, data)

    def raid_player(self, target_igg_id, march_slot=1, troops=None):
        """Attack/raid a player (0x0CF3)."""
        if troops is None:
            troops = [(201, 1000)]
        troop_data = bytearray()
        for tid, cnt in troops:
            troop_data += struct.pack('<II', tid, cnt)

        data = bytearray(24 + len(troop_data))
        struct.pack_into('<I', data, 0, march_slot)
        struct.pack_into('<Q', data, 4, target_igg_id)
        struct.pack_into('<I', data, 12, len(troops))
        struct.pack_into('<I', data, 16, 0)  # hero
        struct.pack_into('<I', data, 20, 0)  # reserved
        data[24:24+len(troop_data)] = troop_data
        return self._encrypted_packet(OP_RAID_PLAYER, bytes(data))

    def move_castle(self, target_x, target_y, use_random=False):
        """Teleport castle (0x0CF1)."""
        data = bytearray(16)
        struct.pack_into('<I', data, 0, target_x)
        struct.pack_into('<I', data, 4, target_y)
        data[8] = 1 if use_random else 0
        struct.pack_into('<I', data, 12, 0)  # item_id
        return self._encrypted_packet(OP_MOVE_CASTLE, bytes(data))

    def start_buildup(self, target_x, target_y, march_slot=1, troops=None):
        """Start alliance rally (0x0CE4)."""
        if troops is None:
            troops = [(201, 1000)]
        troop_data = bytearray()
        for tid, cnt in troops:
            troop_data += struct.pack('<II', tid, cnt)

        data = bytearray(28 + len(troop_data))
        struct.pack_into('<I', data, 0, march_slot)
        struct.pack_into('<I', data, 4, target_x)
        struct.pack_into('<I', data, 8, target_y)
        struct.pack_into('<I', data, 12, len(troops))
        struct.pack_into('<I', data, 16, 0)  # hero
        struct.pack_into('<I', data, 20, 0)
        struct.pack_into('<I', data, 24, 0)
        data[28:28+len(troop_data)] = troop_data
        return self._encrypted_packet(OP_START_BUILDUP, bytes(data))

    def join_buildup(self, rally_id, march_slot=1, troops=None):
        """Join alliance rally (0x0CE5)."""
        if troops is None:
            troops = [(201, 1000)]
        troop_data = bytearray()
        for tid, cnt in troops:
            troop_data += struct.pack('<II', tid, cnt)

        data = bytearray(20 + len(troop_data))
        struct.pack_into('<Q', data, 0, rally_id)
        struct.pack_into('<I', data, 8, march_slot)
        struct.pack_into('<I', data, 12, len(troops))
        struct.pack_into('<I', data, 16, 0)
        data[20:20+len(troop_data)] = troop_data
        return self._encrypted_packet(OP_JOIN_BUILDUP, bytes(data))

    def start_defend(self, target_igg_id, march_slot=1, troops=None):
        """Garrison/defend a player (0x0CE6)."""
        if troops is None:
            troops = [(201, 1000)]
        troop_data = bytearray()
        for tid, cnt in troops:
            troop_data += struct.pack('<II', tid, cnt)

        data = bytearray(20 + len(troop_data))
        struct.pack_into('<Q', data, 0, target_igg_id)
        struct.pack_into('<I', data, 8, march_slot)
        struct.pack_into('<I', data, 12, len(troops))
        struct.pack_into('<I', data, 16, 0)
        data[20:20+len(troop_data)] = troop_data
        return self._encrypted_packet(OP_START_DEFEND, bytes(data))

    def back_defend(self, march_id):
        """Return from garrison (0x0CE7)."""
        return self._encrypted_packet(OP_BACK_DEFEND, struct.pack('<Q', march_id))

    def march_use_item(self, march_id, item_id):
        """Use item on march (0x0CEA)."""
        data = struct.pack('<QI', march_id, item_id)
        return self._encrypted_packet(OP_MARCH_USE_ITEM, data)

    def league_donate(self, tech_id, donate_type=1):
        """Alliance donation (0x0CEC)."""
        data = struct.pack('<II', tech_id, donate_type)
        return self._encrypted_packet(OP_LEAGUE_DONATE, data)

    def mail_request(self, mail_type=0, page=0):
        """Read mail (0x0CF6)."""
        data = struct.pack('<II', mail_type, page)
        return self._encrypted_packet(OP_MAIL_REQUEST, data)

    def shop_buy(self, item_id, count=1):
        """Buy from shop (0x0CF8)."""
        data = struct.pack('<III', item_id, count, 0)
        return self._encrypted_packet(OP_SHOP_BUY, data)

    def enable_view(self, view_type=0x01, flag=0x01):
        """Scout/view map area (0x0CEB = CMSG_ENABLE_VIEW_NEW).
        ARM64 VERIFIED: 10B payload."""
        data = bytearray(10)
        data[0] = view_type
        struct.pack_into('<I', data, 1, self.igg_id)
        data[9] = flag
        return self._encrypted_packet(OP_ENABLE_VIEW, bytes(data))

    # ══════════════════════════════════════════════════════════
    #  OLD-STYLE COMMANDS (unencrypted)
    # ══════════════════════════════════════════════════════════

    def use_item(self, item_id, count=1, target_id=0):
        """Use item - shields, speedups, resources (0x0065)."""
        data = struct.pack('<HII', item_id, count, target_id)
        return self._plain_packet(OP_ITEM_USE, data)

    def heal_troops(self, building_slot=0, troop_type=0):
        """Heal troops (0x06CB)."""
        data = struct.pack('<HxxQ', building_slot, troop_type)
        return self._plain_packet(OP_HEAL, data)

    def speed_train(self, item_id, building_slot=0):
        """Speed up training with item (0x06C7)."""
        data = struct.pack('<HII', building_slot, item_id, 0)
        return self._plain_packet(OP_TRAIN_ITEM_SPD, data)

    def speed_heal(self, item_id, building_slot=0):
        """Speed up healing with item (0x06CF)."""
        data = struct.pack('<HII', building_slot, item_id, 0)
        return self._plain_packet(OP_HEAL_ITEM_SPD, data)

    def onekey_speed_train(self, building_slot=0):
        """One-key speed up all training (0x06D4)."""
        data = struct.pack('<HII', building_slot, 0, 0)
        return self._plain_packet(OP_TRAIN_ONEKEY, data)

    def onekey_speed_heal(self, building_slot=0):
        """One-key speed up all healing (0x06D6)."""
        data = struct.pack('<HII', building_slot, 0, 0)
        return self._plain_packet(OP_HEAL_ONEKEY, data)

    def build_help(self, building_slot=0, building_id=0):
        """Request alliance build help (0x009F)."""
        data = struct.pack('<HH', building_slot, building_id)
        return self._plain_packet(OP_BUILD_HELP, data)

    def research_help(self, research_id=0):
        """Request alliance research help (0x00C6)."""
        data = struct.pack('<H', research_id)
        return self._plain_packet(OP_RESEARCH_HELP, data)

    def speed_research(self, item_id, research_id=0):
        """Speed up research with item (0x00C4)."""
        data = struct.pack('<HII', research_id, item_id, 0)
        return self._plain_packet(OP_RESEARCH_ITEM_SPD, data)

    def cancel_research(self, research_id=0):
        """Cancel active research (0x00C1)."""
        data = struct.pack('<I', research_id)
        return self._plain_packet(OP_RESEARCH_CANCEL, data)

    def build_trap(self, trap_type, count=100):
        """Build traps (0x014B)."""
        data = struct.pack('<II', trap_type, count)
        return self._plain_packet(OP_TRAP_BUILD, data)

    def destroy_trap(self, trap_type, count=100):
        """Destroy traps (0x0154)."""
        data = struct.pack('<II', trap_type, count)
        return self._plain_packet(OP_TRAP_DESTROY, data)

    def exchange_building(self, old_slot, new_building_id):
        """Exchange building type (0x00A1)."""
        data = struct.pack('<II', old_slot, new_building_id)
        return self._plain_packet(OP_EXCHANGE_BUILD, data)

    def train_complete(self, building_slot=0):
        """Collect completed training (0x06C9)."""
        data = struct.pack('<I', building_slot)
        return self._plain_packet(OP_TRAIN_COMPLETE, data)

    def heal_complete(self, building_slot=0):
        """Collect completed healing (0x06D1)."""
        data = struct.pack('<I', building_slot)
        return self._plain_packet(OP_HEAL_COMPLETE, data)

    # ══════════════════════════════════════════════════════════
    #  REWARD COLLECTION (all 2-byte payloads = u16 id)
    # ══════════════════════════════════════════════════════════

    def daily_sign(self, sign_type=0):
        """Daily sign-in (0x0284 = CMSG_SIGN_REQUEST). Fire-and-forget."""
        return self._plain_packet(OP_SIGN_REQUEST, struct.pack('<H', sign_type))

    def append_sign(self, sign_type=0):
        """Supplementary sign-in (0x0285 = CMSG_APPEND_SIGN_REQUEST)."""
        return self._plain_packet(OP_APPEND_SIGN, struct.pack('<H', sign_type))

    def receive_sign_activity(self, activity_id=0):
        """Claim sign activity reward (0x01DE)."""
        return self._plain_packet(OP_RECEIVE_SIGN_ACTIVITY, struct.pack('<H', activity_id))

    def online_reward(self, reward_id=0):
        """Claim online time reward (0x028F). Fire-and-forget."""
        return self._plain_packet(OP_ONLINE_REWARD, struct.pack('<H', reward_id))

    def random_online_reward(self, reward_id=0):
        """Claim random online reward (0x0292). Fire-and-forget."""
        return self._plain_packet(OP_RANDOM_ONLINE_REWARD, struct.pack('<H', reward_id))

    def everyday_gift(self, gift_id=0):
        """Claim daily gift pack (0x0312). Fire-and-forget."""
        return self._plain_packet(OP_EVERYDAY_GIFT, struct.pack('<H', gift_id))

    def achievement_reward(self, achievement_id):
        """Claim achievement reward (0x0224)."""
        return self._plain_packet(OP_ACHIEVEMENT_REWARD, struct.pack('<H', achievement_id))

    def quest_reward(self, quest_id):
        """Claim quest reward (0x062C)."""
        return self._plain_packet(OP_RECEIVE_REWARD, struct.pack('<H', quest_id))

    def quest_reward_batch(self, batch_id=0):
        """Claim all quest rewards at once (0x062F)."""
        return self._plain_packet(OP_RECEIVE_REWARD_BATCH, struct.pack('<H', batch_id))

    def accumulation_reward(self, acc_id=0):
        """Claim accumulation reward (0x069D)."""
        return self._plain_packet(OP_ACCUMULATION_REWARD, struct.pack('<H', acc_id))

    def micropay_daily(self, reward_id=0):
        """Claim micropayment daily reward (0x06FB)."""
        return self._plain_packet(OP_MICROPAY_DAILY, struct.pack('<H', reward_id))

    def download_reward(self, reward_type=0):
        """Claim download reward (0x06FD)."""
        return self._plain_packet(OP_DOWNLOAD_REWARD, struct.pack('<H', reward_type))

    def mobilization_reward(self, reward_id=0):
        """Claim mobilization reward (0x07BE)."""
        return self._plain_packet(OP_MOBILIZATION_REWARD, struct.pack('<H', reward_id))

    def collect_all_rewards(self):
        """Collect ALL daily/free rewards. Returns list of packets."""
        return [
            self.daily_sign(),
            self.online_reward(),
            self.random_online_reward(),
            self.everyday_gift(),
            self.receive_sign_activity(),
            self.accumulation_reward(),
            self.micropay_daily(),
            self.download_reward(),
            self.mobilization_reward(),
            self.quest_reward_batch(),
        ]

    # ══════════════════════════════════════════════════════════
    #  ITEM USE / SPEEDUPS (0x0065)
    # ══════════════════════════════════════════════════════════

    # Speedup item ID ranges (from PCAP ITEM_INFO analysis)
    SPEEDUP_GENERAL = range(1100, 1110)   # General speedups (1min - 30day)
    SPEEDUP_RESEARCH = range(1110, 1120)  # Research speedups
    SPEEDUP_BUILD = range(1120, 1130)     # Building speedups
    SPEEDUP_TRAIN = range(1130, 1140)     # Training speedups
    SPEEDUP_HEAL = range(1140, 1150)      # Healing speedups

    def use_speedup(self, item_id, count=1):
        """Use a speedup item (0x0065 = CMSG_ITEM_USE)."""
        return self.use_item(item_id, count)

    def use_all_speedups(self, inventory, category='general'):
        """Use all speedup items of a category from inventory.
        Args:
            inventory: dict {item_id: quantity} from game_state
            category: 'general', 'research', 'build', 'train', 'heal'
        Returns: list of packets
        """
        ranges = {
            'general': self.SPEEDUP_GENERAL,
            'research': self.SPEEDUP_RESEARCH,
            'build': self.SPEEDUP_BUILD,
            'train': self.SPEEDUP_TRAIN,
            'heal': self.SPEEDUP_HEAL,
        }
        target_range = ranges.get(category, self.SPEEDUP_GENERAL)
        packets = []
        for item_id, qty in inventory.items():
            if item_id in target_range and qty > 0:
                for _ in range(qty):
                    packets.append(self.use_item(item_id))
        return packets

    # ══════════════════════════════════════════════════════════
    #  ALLIANCE & SOCIAL
    # ══════════════════════════════════════════════════════════

    def alliance_help(self):
        """Send alliance help to all (0x1ACD = CMSG_DAMAGE_HELP). Fire-and-forget."""
        return self._plain_packet(OP_ALLIANCE_HELP, struct.pack('<H', 0))

    def city_buff_use(self, buff_id):
        """Use a city buff (0x0111 = CMSG_CITY_BUFF_USE)."""
        return self._plain_packet(OP_CITY_BUFF_USE, struct.pack('<H', buff_id))

    def extinguish_fire(self):
        """Put out castle fire (0x01D3 = CMSG_OUTFIRE_REQUEST). Fire-and-forget."""
        return self._plain_packet(OP_OUTFIRE, struct.pack('<H', 0))

    # ══════════════════════════════════════════════════════════
    #  MONSTER / REBEL HUNTING
    # ══════════════════════════════════════════════════════════

    def find_monster(self, monster_level=1):
        """Request monster position (0x033E = CMSG_REQUEST_MONSTER_POS).
        Server responds with 0x033F containing tile coordinates.
        Args:
            monster_level: Target monster level (1-5)
        """
        return self._plain_packet(OP_REQUEST_MONSTER_POS, struct.pack('<H', monster_level))

    def attack_monster(self, target_x, target_y, march_slot=1, kingdom_id=0xB6, hero_id=0xFF):
        """Attack a monster/rebel at given coordinates."""
        return self.start_march(
            target_x, target_y, march_type=1, march_slot=march_slot,
            kingdom_id=kingdom_id, hero_id=hero_id, resource_type=0,
        )

    # ══════════════════════════════════════════════════════════
    #  CONNECTION PACKETS
    # ══════════════════════════════════════════════════════════

    def heartbeat(self, ms_elapsed):
        """Build heartbeat packet."""
        payload = struct.pack('<II', ms_elapsed, 0)
        return self._plain_packet(OP_HEARTBEAT, payload)

    # ══════════════════════════════════════════════════════════
    #  COMPOUND ACTIONS (multi-step sequences)
    # ══════════════════════════════════════════════════════════

    def call_to_arms_demolish(self, farm_slots):
        """Generate packets to demolish buildings.
        Args: farm_slots = list of (building_id, slot_id)"""
        return [self.demolish(bid, sid) for bid, sid in farm_slots]

    def call_to_arms_rebuild(self, military_builds):
        """Generate packets to build military buildings.
        Args: military_builds = list of (building_id, slot_id)"""
        return [self.build(bid, sid, BUILD_OP_BUILD_NEW) for bid, sid in military_builds]

    def mass_train(self, troop_type=1, count_per=100, num_batches=1):
        """Train troops in multiple batches."""
        return [self.train(troop_type, count_per) for _ in range(num_batches)]

    def gather_resources(self, tiles, march_slots=None, kingdom_id=0xB6):
        """Send marches to gather resource tiles.
        Args: tiles = list of (x, y, resource_type) or (x, y)"""
        if march_slots is None:
            march_slots = list(range(1, len(tiles) + 1))
        packets = []
        for i, tile in enumerate(tiles):
            x, y = tile[0], tile[1]
            res = tile[2] if len(tile) > 2 else 0
            slot = march_slots[i] if i < len(march_slots) else i + 1
            packets.append(self.gather(x, y, march_slot=slot,
                                       kingdom_id=kingdom_id, resource_type=res))
        return packets

    def auto_attack_rebel(self, monster_level=1, march_slot=1, kingdom_id=0xB6, troops=None):
        """Generate the find_monster request packet for auto-rebel flow.
        Full flow (handled by bot.py loop):
          1. find_monster(level) -> wait for 0x033F response with coords
          2. attack_monster(x, y, troops) -> wait for battle result
          3. use_item(energy_item) if energy low
          4. repeat
        Returns: find_monster packet (step 1)
        """
        return self.find_monster(monster_level)

    def daily_routine(self):
        """Full daily automation: collect ALL rewards + alliance help.
        Includes 22 new reward commands from audit report 57.
        Returns: list of packets to send sequentially."""
        packets = self.collect_all_rewards()
        packets.append(self.alliance_help())
        packets.append(self.extinguish_fire())
        # New rewards (from audit)
        packets.extend(self.collect_new_rewards())
        return packets

    # ══════════════════════════════════════════════════════════
    #  NEW COMMANDS (from audit report 57 - 22 commands)
    # ══════════════════════════════════════════════════════════

    def everyday_gift_new(self, gift_id=0):
        """Claim new daily gift (0x189D, fire & forget)."""
        return self._plain_packet(OP_EVERYDAY_GIFT_NEW, struct.pack('<H', gift_id))

    def achievement_score_reward(self, score_id=0):
        """Claim achievement score reward (0x0226)."""
        return self._plain_packet(OP_ACHIEVEMENT_SCORE, struct.pack('<H', score_id))

    def luxury_reward(self, reward_id=0):
        """Claim luxury reward (0x0989, fire & forget!)."""
        return self._plain_packet(OP_LUXURY_REWARD, struct.pack('<H', reward_id))

    def king_road_reward(self, quest_id=0):
        """Claim King's Road reward (0x0993)."""
        return self._plain_packet(OP_KING_ROAD_REWARD, struct.pack('<H', quest_id))

    def exp_reward(self, reward_id=0):
        """Claim championship EXP reward (0x0A07)."""
        return self._plain_packet(OP_EXP_REWARD, struct.pack('<H', reward_id))

    def extra_giftpack_new(self, gift_id=0):
        """Claim extra giftpack (0x16B2, CRITICAL fire & forget!)."""
        return self._plain_packet(OP_EXTRA_GIFTPACK_NEW, struct.pack('<H', gift_id))

    def return_event_reward(self, event_id=0):
        """Claim return event reward (0x16CE, CRITICAL fire & forget!)."""
        return self._plain_packet(OP_RETURN_EVENT_NEW, struct.pack('<H', event_id))

    def arena_challenge(self, opponent_id=0):
        """Start arena fight (0x05F1)."""
        return self._plain_packet(OP_ARENA_CHALLENGE, struct.pack('<H', opponent_id))

    def arena_restore_times(self, type_id=0):
        """Restore arena attempts (0x05EB, fire & forget!)."""
        return self._plain_packet(OP_ARENA_TIMES_RESTORE, struct.pack('<H', type_id))

    def expedition_battle(self, stage_id=0):
        """Fight expedition stage (0x02B6)."""
        return self._plain_packet(OP_EXPEDITION_BATTLE, struct.pack('<H', stage_id))

    def lucky_spin(self, spin_id=0):
        """Lucky turntable spin (0x039C)."""
        return self._plain_packet(OP_LUCKY_TURNTABLE, struct.pack('<H', spin_id))

    def wheel_turn(self, wheel_id=0):
        """Wheel turn (0x0E75)."""
        return self._plain_packet(OP_WHEEL_TURN, struct.pack('<H', wheel_id))

    def double_lottery(self, play_id=0):
        """Double lottery play (0x1D4D)."""
        return self._plain_packet(OP_DOUBLE_LOTTERY, struct.pack('<H', play_id))

    def leaguepass_reward(self, reward_id=0):
        """Claim Guild Pass reward (0x166C)."""
        return self._plain_packet(OP_LEAGUEPASS_REWARD, struct.pack('<H', reward_id))

    def leaguepass_task(self, task_id=0):
        """Complete Guild Pass task (0x1670)."""
        return self._plain_packet(OP_LEAGUEPASS_TASK, struct.pack('<H', task_id))

    def league_bf_reward(self, reward_id=0):
        """Claim league battlefield reward (0x07EF)."""
        return self._plain_packet(OP_LEAGUE_BF_REWARD, struct.pack('<H', reward_id))

    def big_boss_donate(self, point_id=0):
        """Guild boss donate points (0x1F0F)."""
        return self._plain_packet(OP_BIG_BOSS_DONATE, struct.pack('<H', point_id))

    def lostland_donate(self, resource_id=0):
        """Lost Land donate resources (0x15B7)."""
        return self._plain_packet(OP_LOSTLAND_DONATE, struct.pack('<H', resource_id))

    def server_mission(self, mission_id=0):
        """Receive server mission (0x13BD)."""
        return self._plain_packet(OP_SERVER_MISSION, struct.pack('<H', mission_id))

    def dailyconsume_reward(self, reward_id=0):
        """Claim daily consume reward (0x1453)."""
        return self._plain_packet(OP_DAILYCONSUME_REWARD, struct.pack('<H', reward_id))

    def recharge_bonus(self, bonus_id=0):
        """Claim recharge bonus (0x1774)."""
        return self._plain_packet(OP_RECHARGE_BONUS, struct.pack('<H', bonus_id))

    def exchange_reward(self, exchange_id=0):
        """Claim exchange reward (0x099F)."""
        return self._plain_packet(OP_EXCHANGE_REWARD, struct.pack('<H', exchange_id))

    def collect_new_rewards(self):
        """Collect all NEW rewards discovered in audit.
        Returns list of packets for fire-and-forget reward commands."""
        return [
            self.everyday_gift_new(),
            self.achievement_score_reward(),
            self.luxury_reward(),
            self.king_road_reward(),
            self.exp_reward(),
            self.extra_giftpack_new(),
            self.return_event_reward(),
            self.server_mission(),
            self.dailyconsume_reward(),
            self.recharge_bonus(),
            self.exchange_reward(),
        ]

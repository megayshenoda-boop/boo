#!/usr/bin/env python3
"""
50_alliance_war_analysis.py - Alliance & War Systems Binary Analysis
=====================================================================
Analyzes libgame.so for ALL alliance, guild, league, dominion, kingdom battle,
world battle, fortress, lost land, clan PK, and legion systems.

For each opcode:
  1. Find constructor -> confirm opcode value
  2. Find packData -> C2S payload format
  3. Find getData -> S2C response format
  4. Classify direction and fire-and-forget status

Output: analysis/findings/alliance_war_systems.md
"""
import struct
import sys
import os
import time

sys.path.insert(0, r'D:\CascadeProjects\claude')

LIBGAME = r"D:\CascadeProjects\libgame.so"
OUTPUT = r"D:\CascadeProjects\analysis\findings\alliance_war_systems.md"

print("Loading libgame.so...")
with open(LIBGAME, "rb") as f:
    data = f.read()
print(f"  Loaded {len(data):,} bytes")

# Try to use capstone for disassembly
try:
    from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
    md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
    md.detail = True
    HAS_CAPSTONE = True
    print("  Capstone loaded OK")
except ImportError:
    HAS_CAPSTONE = False
    print("  WARNING: capstone not available, payload analysis limited")

# ELF constants from prior analysis
DYNSTR_OFF = 0x682A10
DYNSYM_OFF = 0x2F8
DYNSYM_SIZE = 0x682758

# ============================================================================
# OPCODE DEFINITIONS - All alliance/war systems
# ============================================================================

SYSTEMS = {
    "LEAGUE_TECH_DONATE_SHOP": {
        "description": "Alliance tech upgrades, donations, and shop",
        "opcodes": {
            0x01EC: "CMSG_LEAGUE_TECH_UP",
            0x01ED: "CMSG_LEAGUE_DONATE",
            0x01FE: "CMSG_LEAGUE_SHOP_BUY",
        }
    },
    "LEAGUE_BOARD": {
        "description": "Alliance message board / bulletin",
        "opcodes": {
            0x02A8: "CMSG_LEAGUE_BOARD_REQUEST",
            0x02A9: "CMSG_LEAGUE_BOARD_RETURN",
            0x02AA: "CMSG_LEAGUE_BOARD_LEAVE_WORD",
            0x02AB: "CMSG_LEAGUE_BOARD_LEAVE_WORD_RETURN",
        }
    },
    "LEAGUE_LATEST": {
        "description": "Alliance latest news/log",
        "opcodes": {
            0x02DA: "CMSG_LEAGUE_LATEST_REQUEST",
            0x02DB: "CMSG_LEAGUE_LATEST_RETURN",
        }
    },
    "LEAGUE_STATUS": {
        "description": "Alliance status queries",
        "opcodes": {
            0x0F3C: "CMSG_LEAGUE_STATUS_REQUEST",
            0x0F3D: "CMSG_LEAGUE_STATUS_RETURN",
            0x0F3E: "CMSG_LEAGUE_UPDATE_STATUS_RETURN",
        }
    },
    "LEAGUE_BATTLEFIELD": {
        "description": "Alliance battlefield (Baron/guild fest)",
        "opcodes": {
            0x07E4: "CMSG_SYS_LEAGUE_BATTLEFIELD_INFO",
            0x07E5: "CMSG_ENTER_LEAGUE_BATTLEFIELD_VIEW",
            0x07E6: "CMSG_LEAGUE_BATTLEFIELD_ACTIVITY_VIEW_RETURN",
            0x07E7: "CMSG_QUERY_LEAGUE_BATTLEFIELD_ACTION",
            0x07E8: "CMSG_SYNC_LEAGUE_BATTLEFIELD_ACTION",
            0x07EA: "CMSG_LEAGUE_BATTLEFIELD_SIGNUP_RETURN",
            0x07EB: "CMSG_LEAGUE_BATTLEFIELD_RANK_VIEW_REQUEST",
            0x07EC: "CMSG_LEAGUE_BATTLEFIELD_RANK_VIEW_RETURN",
            0x07ED: "CMSG_LEAGUE_BATTLEFIELD_REWARD_CONFIG_REQUEST",
            0x07EE: "CMSG_LEAGUE_BATTLEFIELD_REWARD_CONFIG_RETURN",
            0x07EF: "CMSG_LEAGUE_BATTLEFIELD_GET_REWARD_REQUEST",
            0x07F0: "CMSG_LEAGUE_BATTLEFIELD_GET_REWARD_RETURN",
            0x07F1: "CMSG_ENTER_LEAGUE_BATTLEFIELD_REQUEST",
            0x07F2: "CMSG_EXIT_LEAGUE_BATTLEFIELD_REQUEST",
            0x07F5: "CMSG_LEAGUE_BATTLEFIELD_POINT_VIEW_REQUEST",
            0x07F6: "CMSG_LEAGUE_BATTLEFIELD_POINT_VIEW_RETURN",
            0x0C4E: "CMSG_SYNC_LEAGUE_BATTLEFIELD_CONFIG",
        }
    },
    "DAMAGE_HELP": {
        "description": "Alliance help/damage system (speed up timers)",
        "opcodes": {
            0x1AC2: "CMSG_SYNC_DAMAGE_INFO",
            0x1AC3: "CMSG_DAMAGE_GIFT_INFO",
            0x1AC4: "CMSG_DAMAGE_GIFT_INFO_RETURN",
            0x1AC5: "CMSG_DAMAGE_HELP",
            0x1AC6: "CMSG_DAMAGE_HELP_RETURN",
            0x1AC7: "CMSG_DAMAGE_BUY",
            0x1AC8: "CMSG_DAMAGE_BUY_RETURN",
            0x1AC9: "CMSG_DAMAGE_BUY_ITEM",
            0x1ACA: "CMSG_DAMAGE_BUY_ITEM_RETURN",
            0x1ACB: "CMSG_DAMAGE_SHARE",
            0x1ACC: "CMSG_DAMAGE_SHARE_RETURN",
            0x1ACD: "CMSG_DAMAGE_HELP_NOTIFY",
        }
    },
    "AUTO_JOIN_BUILDUP": {
        "description": "Auto-join alliance building rally",
        "opcodes": {
            0x1EAA: "CMSG_SYNC_AUTO_JOIN_BUILDUP_INFO",
            0x1EAC: "CMSG_AUTO_JOIN_BUILDUP_OPEN_RETURN",
            0x1EAE: "CMSG_AUTO_JOIN_BUILDUP_CLOSE_RETURN",
        }
    },
    "DOMINION": {
        "description": "Dominion/kingdom control system",
        "opcodes": {
            0x0244: "CMSG_SYNC_DOMINION_INFO",
            0x0245: "CMSG_QUERY_DOMINION_INFO",
            0x0246: "CMSG_QUERY_DOMINION_SIMPLE_BATTLE_INFO",
            0x0247: "CMSG_SYNC_DOMINION_SIMPLE_BATTLE_INFO",
            0x0258: "CMSG_QUERY_DOMINION_OFFICIAL_INFO",
            0x0259: "CMSG_SYNC_DOMINION_OFFICIAL_INFO",
            0x025A: "CMSG_SET_DOMINION_OFFICIAL",
            0x025B: "CMSG_SET_DOMINION_OFFICIAL_RESULT",
            0x0260: "CMSG_QUERY_DOMINION_DEFEND_NUM_REQUEST",
            0x0261: "CMSG_QUERY_DOMINION_DEFEND_NUM_RETURN",
            0x02F8: "CMSG_DOMINION_LATEST_REQUEST",
            0x02F9: "CMSG_DOMINION_LATEST_RETURN",
        }
    },
    "DOMINION_ACTION_KING": {
        "description": "Dominion action / King system (KvK rewards, officials)",
        "opcodes": {
            0x0604: "CMSG_QUERY_DOMINION_ACTION_INTEGRAL_REQUEST",
            0x0605: "CMSG_QUERY_DOMINION_ACTION_INTEGRAL_RETURN",
            0x0606: "CMSG_QUERY_DOMINION_ACTION_HISTORY_REQUEST",
            0x0607: "CMSG_QUERY_DOMINION_ACTION_HISTORY_RETURN",
            0x0608: "CMSG_QUERY_KING_INFO_REQUEST",
            0x0609: "CMSG_QUERY_KING_INFO_RETURN",
            0x060A: "CMSG_DOMINION_ACTION_END",
            0x060C: "CMSG_DOMINION_ACTION_SET_SLAVE_RETURN",
            0x060E: "CMSG_KING_REWARD_INFO_REQUEST",
            0x060F: "CMSG_KING_REWARD_INFO_RETURN",
            0x0610: "CMSG_BESTOW_KING_REWARD_REQUEST",
            0x0611: "CMSG_BESTOW_KING_REWARD_RETURN",
            0x0612: "CMSG_QUERY_SERVER_DOMINION_ACTION_INTEGRAL_REQUEST",
            0x0613: "CMSG_QUERY_SERVER_DOMINION_ACTION_INTEGRAL_RETURN",
            0x0614: "CMSG_QUERY_SERVER_DOMINION_ACTION_HISTORY_REQUEST",
            0x0615: "CMSG_QUERY_SERVER_DOMINION_ACTION_HISTORY_RETURN",
            0x0616: "CMSG_QUERY_SERVER_KING_INFO_REQUEST",
            0x0617: "CMSG_QUERY_SERVER_KING_INFO_RETURN",
        }
    },
    "WORLD_BATTLE": {
        "description": "World Battle / Wonder War system",
        "opcodes": {
            0x083E: "CMSG_QUERY_WORLD_BATTLE_ACTION_CONFIG",
            0x083F: "CMSG_SYNC_WORLD_BATTLE_ACTION_CONFIG",
            0x0840: "CMSG_WORLD_BATTLE_ACTION_REQUEST",
            0x0841: "CMSG_WORLD_BATTLE_ACTION_RETURN",
            0x0842: "CMSG_WORLD_BATTLE_ACTION_DETAIL_REQUEST",
            0x0843: "CMSG_WORLD_BATTLE_ACTION_DETAIL_RETURN",
            0x0846: "CMSG_WORLD_BATTLE_PLAYER_RANK_REQUEST",
            0x0847: "CMSG_WORLD_BATTLE_PLAYER_RANK_RETURN",
            0x0848: "CMSG_WORLD_BATTLE_GROUP_RANK_REQUEST",
            0x0849: "CMSG_WORLD_BATTLE_GROUP_RANK_RETURN",
            0x084A: "CMSG_WORLD_BATTLE_OVERLORD_RECORD_REQUEST",
            0x084B: "CMSG_WORLD_BATTLE_OVERLORD_RECORD_RETURN",
            0x084C: "CMSG_WORLD_BATTLE_ENTER_REQUEST",
            0x084D: "CMSG_WORLD_BATTLE_EXIT_REQUEST",
            0x084E: "CMSG_WORLD_BATTLEFIELD_SYS_INFO",
            0x084F: "CMSG_WORLD_BATTLE_SERVER_OFFICIAL_REQUEST",
            0x0850: "CMSG_WORLD_BATTLE_SERVER_OFFICIAL_RETURN",
            0x0851: "CMSG_WORLD_BATTLE_PLAYER_OFFICIAL_REQUEST",
            0x0852: "CMSG_WORLD_BATTLE_PLAYER_OFFICIAL_RETURN",
            0x0853: "CMSG_WORLD_BATTLE_SET_SERVER_OFFICIAL_REQUEST",
            0x0854: "CMSG_WORLD_BATTLE_SET_SERVER_OFFICIAL_RETURN",
            0x0855: "CMSG_WORLD_BATTLE_SET_PLAYER_OFFICIAL_REQUEST",
            0x0856: "CMSG_WORLD_BATTLE_SET_PLAYER_OFFICIAL_RETURN",
            0x085B: "CMSG_WORLD_BATTLE_ENTER_VIEW_REQUEST",
            0x085C: "CMSG_WORLD_BATTLE_ENTER_VIEW_RETURN",
            0x085F: "CMSG_WORLD_BATTLE_DOMINION_RECORD_REQUEST",
            0x0860: "CMSG_WORLD_BATTLE_DOMINION_RECORD_RETURN",
            0x0CF0: "CMSG_WORLD_BATTLE_NEW_SIGN_UP_REQUEST_NEW",
        }
    },
    "WORLD_BATTLE_GROUPS": {
        "description": "World Battle group/team management",
        "opcodes": {
            0x0961: "CMSG_WORLD_BATTLE_NEW_SIGN_UP_RETURN",
            0x0962: "CMSG_WORLD_BATTLE_GROUP_INFO_REQUEST",
            0x0963: "CMSG_WORLD_BATTLE_GROUP_INFO_RETURN",
            0x0964: "CMSG_WORLD_BATTLE_GROUP_MEMBER_REQUEST",
            0x0965: "CMSG_WORLD_BATTLE_GROUP_MEMBER_RETURN",
            0x0966: "CMSG_WORLD_BATTLE_JOIN_GROUP_REQUEST",
            0x0967: "CMSG_WORLD_BATTLE_JOIN_GROUP_RETURN",
            0x0968: "CMSG_WORLD_BATTLE_SET_POWER_REQUEST",
            0x0969: "CMSG_WORLD_BATTLE_SET_POWER_RETURN",
            0x096A: "CMSG_WORLD_BATTLE_KICK_MEMBER_REQUEST",
            0x096B: "CMSG_WORLD_BATTLE_KICK_MEMBER_RETURN",
            0x096C: "CMSG_WORLD_BATTLE_SYNC_BE_KICKED",
            0x096D: "CMSG_WORLD_BATTLEFIELD_SELF_GROUP_REQUEST",
            0x096F: "CMSG_WORLD_BATTLE_LEAVE_GROUP_REQUEST",
            0x0970: "CMSG_WORLD_BATTLE_LEAVE_GROUP_RETURN",
        }
    },
    "FORTRESS": {
        "description": "Fortress battle system (Darknest/Fortress)",
        "opcodes": {
            0x0F0A: "CMSG_SYS_FORTRESS_INFO",
            0x0F0B: "CMSG_ENTER_FORTRESS_VIEW",
            0x0F0C: "CMSG_FORTRESS_ACTIVITY_VIEW_RETURN",
            0x0F0D: "CMSG_QUERY_FORTRESS_ACTION",
            0x0F0E: "CMSG_SYNC_FORTRESS_ACTION",
            0x0F0F: "CMSG_FORTRESS_SIGNUP_REQUEST",
            0x0F10: "CMSG_FORTRESS_SIGNUP_RETURN",
            0x0F11: "CMSG_FORTRESS_RANK_VIEW_REQUEST",
            0x0F12: "CMSG_FORTRESS_RANK_VIEW_RETURN",
            0x0F13: "CMSG_ENTER_FORTRESS_REQUEST",
            0x0F14: "CMSG_EXIT_FORTRESS_REQUEST",
            0x0F1C: "CMSG_FORTRESS_LEVEL_RANK_VIEW_REQUEST",
            0x0F1D: "CMSG_FORTRESS_LEVEL_RANK_VIEW_RETURN",
            0x0F1E: "CMSG_FORTRESS_LEVEL_USER_RANK_VIEW_REQUEST",
            0x0F1F: "CMSG_FORTRESS_LEVEL_USER_RANK_VIEW_RETURN",
            0x0F20: "CMSG_FORTRESS_DISTRIBUTE_REWARD_INFO_REQUEST",
            0x0F21: "CMSG_FORTRESS_DISTRIBUTE_REWARD_INFO_RETURN",
            0x0F22: "CMSG_BESTOW_FORTRESS_REWARD_REQUEST",
            0x0F23: "CMSG_BESTOW_FORTRESS_REWARD_RETURN",
            0x0F24: "CMSG_FORTRESS_USER_VALUE_REQUEST",
            0x0F25: "CMSG_FORTRESS_USER_VALUE_RETURN",
        }
    },
    "LOSTLAND": {
        "description": "Lost Land / Lost Kingdom system",
        "opcodes": {
            0x15AE: "CMSG_QUERY_LOSTLAND_ACTION_CONFIG",
            0x15AF: "CMSG_SYNC_LOSTLAND_ACTION_CONFIG",
            0x15B0: "CMSG_SYS_LOSTLAND_INFO",
            0x15B1: "CMSG_ENTER_LOSTLAND_VIEW",
            0x15B2: "CMSG_LOSTLAND_ACTIVITY_VIEW_RETURN",
            0x15B3: "CMSG_LOSTLAND_MAPINFO_REQUEST",
            0x15B4: "CMSG_LOSTLAND_MAPINFO_RESPONSE",
            0x15B5: "CMSG_ENTER_LOSTLAND_REQUEST",
            0x15B6: "CMSG_EXIT_LOSTLAND_REQUEST",
            0x15B7: "CMSG_LOSTLAND_DONATE_RESOURCE_REQUEST",
            0x15B8: "CMSG_LOSTLAND_DONATE_RESOURCE_RETURN",
            0x15B9: "CMSG_LOSTLAND_DONATE_HEROCHIP_REQUEST",
            0x15BA: "CMSG_LOSTLAND_DONATE_HEROCHIP_RETURN",
            0x15BB: "CMSG_LOSTLAND_SHOP_BUY_REQUEST",
            0x15BC: "CMSG_LOSTLAND_SHOP_BUY_RETURN",
            0x15BD: "CMSG_SYNC_LOSTLAND_SHOP_BUY_TIMES",
            0x15BE: "CMSG_LOSTLAND_BAN_HERO_REQUEST",
            0x15BF: "CMSG_LOSTLAND_BAN_HERO_RETURN",
            0x15C0: "CMSG_LOSTLAND_HERO_VOTE_COUNT_REQUEST",
            0x15C1: "CMSG_LOSTLAND_HERO_VOTE_COUNT_RETURN",
            0x15C2: "CMSG_LOSTLAND_CAMP_RANK_REQUEST",
            0x15C3: "CMSG_LOSTLAND_CAMP_RANK_RETURN",
            0x15C4: "CMSG_LOSTLAND_LEAGUE_RANK_REQUEST",
            0x15C5: "CMSG_LOSTLAND_LEAGUE_RANK_RETURN",
            0x15C6: "CMSG_LOSTLAND_PLAYER_RANK_REQUEST",
            0x15C7: "CMSG_LOSTLAND_PLAYER_RANK_RETURN",
            0x15C8: "CMSG_LOSTLAND_DONATE_CD_END",
            0x15C9: "CMSG_LOSTLAND_DONATE_INFO",
            0x15CA: "CMSG_LOSTLAND_MARK_REWARD_REQUEST",
            0x15CB: "CMSG_LOSTLAND_MARK_REWARD_RETURN",
            0x15CC: "CMSG_LOSTLAND_HISTORY_REQUEST",
            0x15CD: "CMSG_LOSTLAND_HISTORY_RETURN",
            0x15CE: "CMSG_LOSTLAND_LEAGUE_HISTORY_REQUEST",
            0x15CF: "CMSG_LOSTLAND_LEAGUE_HISTORY_RETURN",
            0x15D0: "CMSG_LOSTLAND_PLAYER_HISTORY_REQUEST",
            0x15D1: "CMSG_LOSTLAND_PLAYER_HISTORY_RETURN",
            0x15D2: "CMSG_LOSTLAND_SELF_CAMP_AREA",
            0x15D3: "CMSG_LOSTLAND_SELF_DOMINION_REQUEST",
            0x15D4: "CMSG_LOSTLAND_SELF_DOMINION_RESPONSE",
            0x15D5: "CMSG_LOSTLAND_LEAGUE_BUILD_REQUEST",
            0x15D7: "CMSG_SYS_LOSTLAND_WEEK_BAN_HERO",
            0x15D8: "CMSG_ENTER_LOSTLAND_ERROR_RETURN",
            0x15D9: "CMSG_LOSTLAND_ACHIEVEMENT_LIST_REQUEST",
            0x15DA: "CMSG_LOSTLAND_ACHIEVEMENT_LIST_RETURN",
            0x15DB: "CMSG_LOSTLAND_ACHIEVEMENT_COMPLETE",
            0x15DC: "CMSG_LOSTLAND_ACHIEVEMENT_REQUEST",
            0x15DD: "CMSG_LOSTLAND_ACHIEVEMENT_RETURN",
            0x15DE: "CMSG_LOSTLAND_ACHIEVEMENT_REWARD_REQUEST",
            0x15DF: "CMSG_LOSTLAND_ACHIEVEMENT_REWARD_RETURN",
        }
    },
    "LOSTLAND_BUILDINGS": {
        "description": "Lost Land buildings and structures",
        "opcodes": {
            0x15E0: "CMSG_LEAGUE_BUILDING_OPERAT_REQUEST",
            0x15E1: "CMSG_LEAGUE_BUILDING_OPERAT_RETURN",
            0x15E3: "CMSG_SELF_LEAGUEBUILD_SYNC",
            0x15E4: "CMSG_LEAGUE_BUILDING_DETAIL_REQUEST",
            0x15E5: "CMSG_LEAGUE_BUILDING_DETAIL_RETURN",
            0x15E6: "CMSG_SYNC_ALL_LEAGUEBUILD_BATTLE_COUNT",
            0x15E7: "CMSG_ADD_LEAGUEBUILD",
            0x15E8: "CMSG_UPDATE_LEAGUEBUILD",
            0x15E9: "CMSG_DELETE_LEAGUEBUILD",
            0x15EA: "CMSG_QUERY_LEAGUEBUILD_DEFEND_INFO",
            0x15EB: "CMSG_SYNC_LEAGUEBUILD_DEFEND_INFO",
            0x15EC: "CMSG_KICK_LEAGUE_BUILD_DEFEND_ARMY",
            0x15F1: "CMSG_LOSTLAND_LEAGUE_LATEST_REQUEST",
            0x15F2: "CMSG_LOSTLAND_LEAGUE_LATEST_RETURN",
            0x15F3: "CMSG_UPDATE_LEAGUEBUILD_CONNECT_STATUS",
            0x15FA: "CMSG_LOSTLAND_BUILDING_INDEX_OPEN_REQUEST",
            0x15FB: "CMSG_LOSTLAND_BUILDING_INDEX_OPEN_RETURN",
            0x15FE: "CMSG_SYNC_LOSTLAND_MONTH_CARD_INFO",
            0x15FF: "CMSG_LOSTLAND_MONTH_CARD_REWARD_REQUEST",
            0x1600: "CMSG_LOSTLAND_MONTH_CARD_REWARD_RETURN",
        }
    },
    "LOSTLAND_RUSH_EVENT": {
        "description": "Lost Land rush event",
        "opcodes": {
            0x1FAB: "CMSG_QUERY_LOSTLAND_RUSH_EVENT",
            0x1FAC: "CMSG_SYNC_LOSTLAND_RUSH_EVENT",
            0x1FAD: "CMSG_LOSTLAND_RUSH_EVENT_REWARD_REQUEST",
            0x1FAE: "CMSG_LOSTLAND_RUSH_EVENT_REWARD_RETURN",
            0x1FAF: "CMSG_LOSTLAND_RUSH_EVENT_RANK_REQUEST",
            0x1FB0: "CMSG_LOSTLAND_RUSH_EVENT_RANK_RETURN",
        }
    },
    "LEGION": {
        "description": "Legion system (cross-server guild wars)",
        "opcodes": {
            0x0C4F: "CMSG_LEGION_ACTION_REQUEST",
            0x0C51: "CMSG_LEGION_CREATE_REQUEST",
            0x0C52: "CMSG_LEGION_CREATE_RETURN",
            0x0C53: "CMSG_LEGION_LIST_REQUEST",
            0x0C54: "CMSG_LEGION_LIST_RETURN",
            0x0C55: "CMSG_LEGION_INFO_REQUEST",
            0x0C56: "CMSG_LEGION_INFO_RETURN",
            0x0C57: "CMSG_LEGION_JOIN_REQUEST",
            0x0C58: "CMSG_LEGION_JOIN_RETURN",
            0x0C59: "CMSG_KICK_LEGION_MEMBER",
            0x0C5A: "CMSG_NOTIFY_LEGION_MEMBER_JOIN",
            0x0C5B: "CMSG_NOTIFY_LEGION_MEMBER_LEAVE",
            0x0C5C: "CMSG_LEGION_ADD_MEMBER_LIST_REQUEST",
            0x0C5D: "CMSG_LEGION_ADD_MEMBER_LIST_RETURN",
            0x0C5E: "CMSG_CHANGE_LEGION_POSTION",
            0x0C5F: "CMSG_NOTIFY_LEGION_MEMBER_CHANGE",
            0x0C60: "CMSG_CHANGE_LEGION_CHANGE_NAME_REQUEST",
            0x0C61: "CMSG_CHANGE_LEGION_CHANGE_NAME_RETURN",
            0x0C62: "CMSG_NOTIFY_LEGION_NAME_CHANGE",
            0x0C63: "CMSG_LEGION_RANK_REQUEST",
            0x0C64: "CMSG_LEGION_RANK_RETURN",
            0x0C65: "CMSG_LEGION_SET_TALENT_REQUEST",
            0x0C66: "CMSG_LEGION_SET_TALENT_RETURN",
            0x0C67: "CMSG_LEGION_CHANGE_POS_TIMES_REQUEST",
            0x0C68: "CMSG_LEGION_CHANGE_POS_TIMES_RETURN",
            0x0C69: "CMSG_NOTIFY_LEGION_CHANGE_POS_TIMES",
            0x0C6E: "CMSG_LEGION_LATEST_REQUEST",
            0x0C6F: "CMSG_LEGION_LATEST_RETURN",
            0x0C70: "CMSG_LEGION_SELF_JOIN_REQUEST",
            0x0C71: "CMSG_LEGION_SELF_JOIN_RETURN",
            0x0C72: "CMSG_LEGION_SELF_LEAVE_REQUEST",
            0x0C73: "CMSG_LEGION_SELF_LEAVE_RETURN",
            0x0C74: "CMSG_LEGION_BATTLE_MAP_INFO_REQUEST",
            0x0C75: "CMSG_LEGION_BATTLE_MAP_INFO_RETURN",
            0x0C76: "CMSG_LEGION_RESOURCE_REQUEST",
            0x0C77: "CMSG_LEGION_RESOURCE_RETURN",
            0x0C78: "CMSG_LEGION_MEMBER_INFO_REQUEST",
            0x0C79: "CMSG_LEGION_MEMBER_INFO_RETURN",
            0x0C7A: "CMSG_LEGION_ENEMY_POS_REQUEST",
            0x0C7B: "CMSG_LEGION_ENEMY_POS_RETURN",
            0x0C7C: "CMSG_LEGION_VALUE_DETAIL_REQUEST",
            0x0C7D: "CMSG_LEGION_VALUE_DETAIL_RETURN",
        }
    },
    "LEGION_SEASON": {
        "description": "Legion Season / Championship system",
        "opcodes": {
            0x0E10: "CMSG_LEGION_SEASON_ACTION_REQUEST",
            0x0E12: "CMSG_LEGION_SEASON_ACTION_SELF_SCHEDULE_REQUEST",
            0x0E13: "CMSG_LEGION_SEASON_ACTION_SELF_SCHEDULE_RETURN",
            0x0E16: "CMSG_LEGION_SEASON_ACTION_GUESS_INFO_REQUEST",
            0x0E17: "CMSG_LEGION_SEASON_ACTION_GUESS_INFO_RETURN",
            0x0E18: "CMSG_LEGION_SEASON_ACTION_GUESS_BET_REQUEST",
            0x0E19: "CMSG_LEGION_SEASON_ACTION_GUESS_BET_RETURN",
            0x0E1A: "CMSG_LEGION_SEASON_ACTION_PLAYOFF_REQUEST",
            0x0E1B: "CMSG_LEGION_SEASON_ACTION_PLAYOFF_RETURN",
            0x0E1C: "CMSG_LEGION_SEASON_ACTION_HIS_PLAYER_REQUEST",
            0x0E1D: "CMSG_LEGION_SEASON_ACTION_HIS_PLAYER_RETURN",
            0x0E1E: "CMSG_LEGION_SEASON_ACTION_HIS_MVP_REQUEST",
            0x0E1F: "CMSG_LEGION_SEASON_ACTION_HIS_MVP_RETURN",
            0x0E20: "CMSG_LEGION_SEASON_ACTION_HIS_BEST_PLAYER_REQUEST",
            0x0E21: "CMSG_LEGION_SEASON_ACTION_HIS_BEST_PLAYER_RETURN",
            0x0E22: "CMSG_LEGION_SEASON_ACTION_LIKE_PLAYER_REQUEST",
            0x0E23: "CMSG_LEGION_SEASON_ACTION_LIKE_PLAYER_RETURN",
            0x0E26: "CMSG_LEGION_FINAL_POINT",
            0x0E27: "CMSG_LEGION_MEMBER_HIS_INFO_REQUEST",
            0x0E28: "CMSG_LEGION_MEMBER_HIS_INFO_RETURN",
        }
    },
    "CLANPK": {
        "description": "Clan PK / Guild Showdown system",
        "opcodes": {
            0x1AF4: "CMSG_SYNC_CLANPK_CONFIG",
            0x1AF5: "CMSG_SYNC_CLANPK_INFO",
            0x1AF6: "CMSG_SYNC_CLANPK_FINAL_DETAIL_INFO",
            0x1AF7: "CMSG_CLANPK_SIGNUP_REQUEST",
            0x1AF8: "CMSG_CLANPK_SIGNUP_RETURN",
            0x1AF9: "CMSG_ENTER_CLANPK_VIEW",
            0x1AFA: "CMSG_CLANPK_ACTIVITY_VIEW_RETURN",
            0x1AFB: "CMSG_CLANPK_BATTLE_RECORD_REQUEST",
            0x1AFC: "CMSG_CLANPK_BATTLE_RECORD_RETURN",
            0x1AFD: "CMSG_CLANPK_LEVEL_RANK_VIEW_REQUEST",
            0x1AFE: "CMSG_CLANPK_LEVEL_RANK_VIEW_RETURN",
            0x1AFF: "CMSG_CLANPK_USER_RANK_VIEW_REQUEST",
            0x1B00: "CMSG_CLANPK_USER_RANK_VIEW_RETURN",
            0x1B01: "CMSG_ENTER_CLANPK_REQUEST",
            0x1B02: "CMSG_ENTER_CLANPK_RETURN",
            0x1B03: "CMSG_EXIT_CLANPK_REQUEST",
            0x1B04: "CMSG_CLANPK_BUILDING_REQUEST",
            0x1B05: "CMSG_CLANPK_BUILDING_RETURN",
            0x1B06: "CMSG_CLANPK_BUILD_UPGRADE_REQUEST",
            0x1B07: "CMSG_CLANPK_BUILD_UPGRADE_RETURN",
            0x1B08: "CMSG_CLANPK_DONATE_REQUEST",
            0x1B09: "CMSG_CLANPK_DONATE_RETURN",
            0x1B0A: "CMSG_CLANPK_SET_DEFEND_HERO_REQUEST",
            0x1B0B: "CMSG_CLANPK_SET_DEFEND_HERO_RETURN",
            0x1B0C: "CMSG_CLANPK_SET_ATTACK_HERO_REQUEST",
            0x1B0D: "CMSG_CLANPK_SET_ATTACK_HERO_RETURN",
            0x1B0E: "CMSG_CLANPK_SET_ASSIST_HERO_REQUEST",
            0x1B0F: "CMSG_CLANPK_SET_ASSIST_HERO_RETURN",
            0x1B10: "CMSG_CLANPK_GIVE_ASSIST_HERO_REQUEST",
            0x1B11: "CMSG_CLANPK_GIVE_ASSIST_HERO_RETURN",
            0x1B14: "CMSG_CLANPK_ASSIST_HERO_REQUEST",
            0x1B15: "CMSG_CLANPK_ASSIST_HERO_RETURN",
            0x1B16: "CMSG_CLANPK_QUERY_DEFEND_INFO",
            0x1B17: "CMSG_SYNC_CLANPK_DEFEND_INFO",
            0x1B18: "CMSG_CLANPK_QUERY_ATTACK_INFO",
            0x1B19: "CMSG_SYNC_CLANPK_ATTACK_INFO",
            0x1B1A: "CMSG_CLANPK_START_ATTACK",
            0x1B1B: "CMSG_CLANPK_START_ATTACK_RETURN",
            0x1B1D: "CMSG_SET_CLANPK_DEFEND_AMRY_INFO_RESULT",
            0x1B1F: "CMSG_CLANPK_MAILBOX_MAIL_REQUEST",
            0x1B20: "CMSG_CLANPK_MAILBOX_MAIL",
            0x1B21: "CMSG_CLANPK_START_DEFEND",
            0x1B22: "CMSG_CLANPK_START_DEFEND_RETURN",
            0x1B23: "CMSG_CLANPK_ATTACK_BUILDING_BEGIN",
            0x1B24: "CMSG_CLANPK_ATTACK_BUILDING_END",
            0x1B26: "CMSG_CLANPK_THUNDER_ATTACK_END",
            0x1B27: "CMSG_CLANPK_CHAT_HISTORY",
            0x1B28: "CMSG_UPDATE_CLANPK_DEFEND_AMRY_INFO",
            0x1B29: "CMSG_UPDATE_CLANPK_ATTACK_AMRY_INFO",
            0x1B2A: "CMSG_CLANPK_UPDATE_ASSIST_HERO",
            0x1B2B: "CMSG_CLANPK_UPDATE_BUILDING_INFO",
            0x1B2C: "CMSG_UPDATE_CLANPK_AMRY_INFO",
            0x1B2D: "CMSG_CLANPK_DEFEND_AMRY_REQUEST",
            0x1B2E: "CMSG_CLANPK_DEFEND_AMRY_RETURN",
            0x1B30: "CMSG_CLANPK_DEFEND_BUILDING_RETURN",
            0x1B31: "CMSG_CLANPK_ADD_KILL_VALUE",
            0x1B32: "CMSG_CLANPK_ACTIVITY_INFO_REQUEST",
            0x1B33: "CMSG_CLANPK_ACTIVITY_INFO_RETURN",
            0x1B34: "CMSG_CLANPK_CHECK_SET_DEF_REQUEST",
            0x1B35: "CMSG_CLANPK_CHECK_SET_DEF_RETURN",
            0x1B36: "CMSG_CLANPK_FIRST_LEVEL_REWARD_REQUEST",
            0x1B37: "CMSG_CLANPK_FIRST_LEVEL_REWARD_RETURN",
        }
    },
    "LEAGUEPASS": {
        "description": "League Pass / Guild Pass system",
        "opcodes": {
            0x1663: "CMSG_SYNC_LEAGUEPASS_ACTION",
            0x1666: "CMSG_LEAGUEPASS_ACTION_TASK_INFO_REQUEST",
            0x1667: "CMSG_LEAGUEPASS_ACTION_TASK_INFO_RETURN",
            0x1668: "CMSG_LEAGUEPASS_GROUP_RANK_INFO_REQUEST",
            0x1669: "CMSG_LEAGUEPASS_GROUP_RANK_INFO_RETURN",
            0x166A: "CMSG_LEAGUEPASS_CONTRIBUTE_INFO_REQUEST",
            0x166B: "CMSG_LEAGUEPASS_CONTRIBUTE_INFO_RETURN",
            0x166C: "CMSG_LEAGUEPASS_GET_REWARD_REQUEST",
            0x166D: "CMSG_LEAGUEPASS_GET_REWARD_RETURN",
            0x166E: "CMSG_LEAGUEPASS_FRESH_TASK_REQUEST",
            0x166F: "CMSG_LEAGUEPASS_FRESH_TASK_RETURN",
            0x1670: "CMSG_LEAGUEPASS_FINISH_TASK_REQUEST",
            0x1671: "CMSG_LEAGUEPASS_FINISH_TASK_RETURN",
            0x1672: "CMSG_SYNC_LEAGUEPASS_TASK_REFRESH",
            0x1673: "CMSG_SYNC_LEAGUEPASS_UPDATE_MY_TASK",
            0x1674: "CMSG_SYNC_LEAGUEPASS_ADVANCEDGIFT",
        }
    },
    "LEAGUE_BIG_BOSS": {
        "description": "League Big Boss / Guild Boss system",
        "opcodes": {
            0x1F0E: "CMSG_SYNC_LEAGUE_BIG_BOSS_CONFIG",
            0x1F0F: "CMSG_LEAGUE_BIG_BOSS_DONATE_POINT_REQUEST",
            0x1F10: "CMSG_LEAGUE_BIG_BOSS_DONATE_POINT_RETURN",
            0x1F11: "CMSG_LEAGUE_BIG_BOSS_DONATE_REQUEST",
            0x1F12: "CMSG_LEAGUE_BIG_BOSS_DONATE_RETURN",
            0x1F13: "CMSG_LEAGUE_BIG_BOSS_POINT_REQUEST",
            0x1F14: "CMSG_LEAGUE_BIG_BOSS_POINT_RETURN",
            0x1F17: "CMSG_LEAGUE_BIG_BOSS_SET_BATTLE_TIME_REQUEST",
            0x1F18: "CMSG_LEAGUE_BIG_BOSS_SET_BATTLE_TIME_RETURN",
            0x1F19: "CMSG_SYNC_LEAGUE_BIG_BOSS_INFO",
            0x1F1A: "CMSG_SYNC_LEAGUE_BIG_BOSS_REWARD_TIMES",
            0x1F1B: "CMSG_LEAGUE_BIG_BOSS_EMPTYPOS_REQUEST",
            0x1F1C: "CMSG_LEAGUE_BIG_BOSS_EMPTYPOS_RETURN",
        }
    },
    "KING_CHESS": {
        "description": "King Chess / Kingdom Clash board game",
        "opcodes": {
            0x0A29: "CMSG_KING_CHESS_SIGNUP_RETURN",
            0x0A2B: "CMSG_SYNC_KING_CHESS_ACTION",
            0x0A2C: "CMSG_KING_CHESS_ACTION_DETAIL_INFO_REQUEST",
            0x0A2D: "CMSG_KING_CHESS_ACTION_DETAIL_INFO_RETURN",
            0x0A2E: "CMSG_KING_CHESS_RANK_REQUEST",
            0x0A2F: "CMSG_KING_CHESS_RANK_RETURN",
            0x0A30: "CMSG_KING_CHESS_ENABLE_VIEW",
            0x0A33: "CMSG_KING_CHESS_OCCUPY_INFO_REQUEST",
            0x0A34: "CMSG_KING_CHESS_OCCUPY_INFO_RETURN",
            0x0A36: "CMSG_KING_CHESS_SET_LOOK_CHAT",
            0x0A37: "CMSG_KING_CHESS_SYNC_ALL_LEAGUE_INFO",
            0x0A3D: "CMSG_SYNC_LEAGUE_KING_CHESS_DEL",
            0x0A3E: "CMSG_SYNC_LEAGUE_KING_CHESS_ADD",
            0x0A41: "CMSG_SYNC_DEFEND_INFO_KING_CHESS",
            0x0A49: "CMSG_KING_CHESS_USER_VALUE_REQUEST",
            0x0A4A: "CMSG_KING_CHESS_USER_VALUE_RETURN",
            0x0A4B: "CMSG_KING_CHESS_SELF_INFO_REQUEST",
            0x0A4C: "CMSG_KING_CHESS_ALL_LEAGUE_INFO_REQUEST",
        }
    },
    "KING_ROAD": {
        "description": "King's Road quests",
        "opcodes": {
            0x0992: "CMSG_SYNC_KING_ROAD_QUEST_INFO",
            0x0993: "CMSG_KING_ROAD_REWARD_REQUEST",
            0x0994: "CMSG_KING_ROAD_REWARD_RETURN",
            0x0995: "CMSG_SYNC_KING_ROAD_ONE_QUEST_INFO",
        }
    },
}


# ============================================================================
# SYMBOL TABLE SEARCH FUNCTIONS
# ============================================================================

def iter_dynsym():
    """Iterate all dynamic symbols yielding (name, addr, size)."""
    pos = DYNSYM_OFF
    while pos + 24 <= DYNSYM_OFF + DYNSYM_SIZE:
        st_name = struct.unpack('<I', data[pos:pos+4])[0]
        st_value = struct.unpack('<Q', data[pos+8:pos+16])[0]
        st_size = struct.unpack('<Q', data[pos+16:pos+24])[0]
        if st_name > 0 and st_name < 0x300000 and st_value > 0:
            try:
                name_end = data.index(b'\x00', DYNSTR_OFF + st_name)
                name = data[DYNSTR_OFF + st_name:name_end].decode('ascii', errors='replace')
                yield (name, st_value, st_size)
            except:
                pass
        pos += 24


# Build symbol index for fast lookups
print("Building symbol index...")
sym_index = {}
for name, addr, size in iter_dynsym():
    sym_index[name] = (addr, size)
print(f"  Indexed {len(sym_index)} symbols")


def find_symbols(name_fragment, kind=None):
    """Find symbols containing name_fragment.
    kind: 'packData', 'getData', 'constructor', 'destructor', or None for all.
    """
    results = []
    for name, (addr, size) in sym_index.items():
        if name_fragment not in name:
            continue
        if kind == 'packData' and '8packData' not in name:
            continue
        if kind == 'getData' and '7getData' not in name:
            continue
        if kind == 'constructor' and 'C1Ev' not in name:
            continue
        if kind == 'constructor' and ('8packData' in name or '7getData' in name):
            continue
        if kind is None or (kind not in ('packData', 'getData', 'constructor')):
            pass
        results.append((name, addr, size))
    return results


def classify_opcode(name):
    """Classify opcode direction based on naming convention."""
    n = name.upper()
    if '_RETURN' in n or '_RESULT' in n:
        return 'S2C'
    if '_SYNC_' in n or n.startswith('CMSG_SYNC_') or '_SYS_' in n or n.startswith('CMSG_SYS_'):
        return 'S2C'
    if '_NOTIFY_' in n or n.startswith('CMSG_NOTIFY_'):
        return 'S2C'
    if '_REQUEST' in n:
        return 'C2S'
    if '_QUERY_' in n or n.startswith('CMSG_QUERY_'):
        return 'C2S'
    if '_ENTER_' in n and '_VIEW' in n:
        return 'C2S'
    if '_EXIT_' in n:
        return 'C2S'
    if '_SET_' in n:
        return 'C2S'
    if '_DONATE' in n or '_BUY' in n or '_SHOP_BUY' in n:
        return 'C2S'
    if '_SIGNUP' in n and '_RETURN' not in n:
        return 'C2S'
    if '_KICK_' in n or '_CHANGE_' in n:
        return 'C2S'
    if '_LEAVE_WORD' in n:
        return 'C2S'
    if '_START_ATTACK' in n or '_START_DEFEND' in n:
        return 'C2S'
    if '_ADD_' in n or '_DELETE_' in n or '_UPDATE_' in n:
        return 'S2C'  # server pushes
    if 'ENABLE_VIEW' in n:
        return 'C2S'
    return 'C2S?'  # default guess


def has_return_pair(opcode, name, all_opcodes_in_system):
    """Check if this REQUEST opcode has a _RETURN pair."""
    if '_REQUEST' in name:
        base = name.replace('_REQUEST', '_RETURN')
        for op, n in all_opcodes_in_system.items():
            if n == base:
                return True
        # Also check close opcodes
        for op, n in all_opcodes_in_system.items():
            if op == opcode + 1 and '_RETURN' in n:
                return True
    return False


def analyze_packdata_fields(addr, size):
    """Analyze packData function to extract payload fields using capstone."""
    if not HAS_CAPSTONE:
        return None, 0

    max_bytes = min(size if size > 0 else 600, 2000)
    code = data[addr:addr + max_bytes]
    try:
        insns = list(md.disasm(code, addr))
    except:
        return None, 0

    payload_fields = []
    current_write_size = 0
    payload_offset = 0
    this_reg = 'x0'

    for i, insn in enumerate(insns):
        if insn.mnemonic == 'ret' and insn.address > addr + 16:
            break

        # Detect this pointer save
        if insn.mnemonic == 'mov' and insn.op_str.startswith('x19, x0'):
            this_reg = 'x19'
        if insn.mnemonic == 'mov' and insn.op_str.startswith('x20, x0'):
            this_reg = 'x20'

        # Detect write size from position update: add wN, wN, #SIZE
        if insn.mnemonic == 'add' and '#' in insn.op_str:
            parts = insn.op_str.split('#')
            try:
                add_val = int(parts[-1].rstrip(']'), 0)
                if add_val in (1, 2, 4, 8):
                    for j in range(i+1, min(i+6, len(insns))):
                        if 'strh' in insns[j].mnemonic and '#0xa' in insns[j].op_str:
                            current_write_size = add_val
                            break
            except:
                pass

        # Detect data load from CMSG struct
        if insn.mnemonic in ('ldrh', 'ldrb', 'ldr', 'ldrsb', 'ldrsh', 'ldrsw'):
            if f'[{this_reg}]' in insn.op_str or f'[{this_reg},' in insn.op_str:
                offset = 0
                if '#' in insn.op_str:
                    try:
                        offset = int(insn.op_str.split('#')[-1].rstrip(']').rstrip('!'), 0)
                    except:
                        pass

                sizes = {'ldrb': 1, 'ldrsb': 1, 'ldrh': 2, 'ldrsh': 2, 'ldr': 4, 'ldrsw': 4}
                field_size = sizes.get(insn.mnemonic, 4)
                if insn.mnemonic == 'ldr' and insn.op_str.split(',')[0].strip().startswith('x'):
                    field_size = 8

                is_payload = False
                for j in range(i+1, min(i+8, len(insns))):
                    if insns[j].mnemonic in ('strh', 'strb', 'str') and 'uxtw' in insns[j].op_str:
                        is_payload = True
                        break

                if is_payload:
                    ws = current_write_size if current_write_size else field_size
                    payload_fields.append({
                        'struct_offset': offset,
                        'size': ws,
                        'payload_offset': payload_offset,
                    })
                    payload_offset += ws
                    current_write_size = 0

    total_size = payload_offset if payload_fields else 0
    return payload_fields, total_size


def analyze_getdata_fields(addr, size):
    """Analyze getData function to get approximate response size."""
    if not HAS_CAPSTONE:
        return None, 0

    max_bytes = min(size if size > 0 else 600, 2000)
    code = data[addr:addr + max_bytes]
    try:
        insns = list(md.disasm(code, addr))
    except:
        return None, 0

    read_fields = []
    current_read_size = 0
    read_offset = 0
    this_reg = 'x0'

    for i, insn in enumerate(insns):
        if insn.mnemonic == 'ret' and insn.address > addr + 16:
            break

        if insn.mnemonic == 'mov' and insn.op_str.startswith('x19, x0'):
            this_reg = 'x19'
        if insn.mnemonic == 'mov' and insn.op_str.startswith('x20, x0'):
            this_reg = 'x20'

        # getData reads from CIStream: ldrh/ldr from [x1, offset] then stores to struct
        # Look for add #N patterns for CIStream position advancement
        if insn.mnemonic == 'add' and '#' in insn.op_str:
            parts = insn.op_str.split('#')
            try:
                add_val = int(parts[-1].rstrip(']'), 0)
                if add_val in (1, 2, 4, 8):
                    # Check if reading from stream (loading from buffer pointer)
                    for j in range(max(0, i-6), i):
                        ops = insns[j].op_str
                        if insns[j].mnemonic in ('ldrh', 'ldrb', 'ldr') and 'uxtw' in ops:
                            read_fields.append({
                                'size': add_val,
                                'read_offset': read_offset,
                            })
                            read_offset += add_val
                            break
            except:
                pass

    total_size = read_offset if read_fields else 0
    return read_fields, total_size


def search_string_refs(search_str):
    """Find string in binary and return its offset."""
    encoded = search_str.encode('ascii', errors='ignore')
    pos = data.find(encoded)
    if pos >= 0:
        return pos
    return -1


def find_opcode_in_constructor(cmsg_name):
    """Search for constructor and try to extract opcode from it."""
    # Derive the class name fragment from CMSG name
    # e.g., CMSG_DAMAGE_HELP -> DamageHelp or damage_help
    short = cmsg_name.replace('CMSG_', '')

    # Search for the full name or common fragments
    constructors = find_symbols(short, kind='constructor')
    if not constructors:
        # Try lowercase/mixed case
        parts = short.split('_')
        camel = ''.join(p.capitalize() for p in parts)
        constructors = find_symbols(camel, kind='constructor')
    if not constructors:
        # Try just the last 2 parts
        parts = short.split('_')
        if len(parts) >= 2:
            camel = ''.join(p.capitalize() for p in parts[-2:])
            constructors = find_symbols(camel, kind='constructor')

    return constructors


# ============================================================================
# MAIN ANALYSIS
# ============================================================================

print("\n" + "=" * 70)
print("ALLIANCE & WAR SYSTEMS ANALYSIS")
print("=" * 70)

results = {}  # system_name -> list of opcode results

total_opcodes = sum(len(s["opcodes"]) for s in SYSTEMS.values())
analyzed = 0
found_pack = 0
found_get = 0
found_constructor = 0

for sys_name, sys_info in SYSTEMS.items():
    print(f"\n--- {sys_name}: {sys_info['description']} ---")
    sys_results = []

    # Build all_opcodes for this system (for return-pair checking)
    all_opcodes = sys_info["opcodes"]

    for opcode, cmsg_name in sorted(all_opcodes.items()):
        analyzed += 1
        direction = classify_opcode(cmsg_name)

        # Derive search fragments
        short_name = cmsg_name.replace('CMSG_', '')

        # Search for packData
        pack_results = find_symbols(short_name, kind='packData')
        pack_info = None
        pack_fields = None
        pack_size = 0

        if pack_results:
            found_pack += 1
            pname, paddr, psize = pack_results[0]
            pack_info = (pname, paddr, psize)
            pack_fields, pack_size = analyze_packdata_fields(paddr, psize)
            if direction == 'S2C':
                direction = 'BIDI'  # Has packData but classified as S2C => bidirectional

        # Search for getData
        get_results = find_symbols(short_name, kind='getData')
        get_info = None
        get_fields = None
        get_size = 0

        if get_results:
            found_get += 1
            gname, gaddr, gsize = get_results[0]
            get_info = (gname, gaddr, gsize)
            get_fields, get_size = analyze_getdata_fields(gaddr, gsize)

        # Search for constructor
        cons_results = find_symbols(short_name, kind='constructor')
        cons_info = None
        if cons_results:
            found_constructor += 1
            cons_info = cons_results[0]

        # Check fire-and-forget
        has_return = has_return_pair(opcode, cmsg_name, all_opcodes)
        is_fire_forget = (direction in ('C2S', 'C2S?')) and not has_return

        # Check for RETURN/SYNC in name (not fire-and-forget if it IS a return)
        if '_RETURN' in cmsg_name or '_RESULT' in cmsg_name or 'SYNC_' in cmsg_name or 'NOTIFY_' in cmsg_name:
            is_fire_forget = False

        result = {
            'opcode': opcode,
            'name': cmsg_name,
            'direction': direction,
            'pack_info': pack_info,
            'pack_fields': pack_fields,
            'pack_size': pack_size,
            'get_info': get_info,
            'get_fields': get_fields,
            'get_size': get_size,
            'constructor': cons_info,
            'fire_forget': is_fire_forget,
            'has_return': has_return,
        }
        sys_results.append(result)

        # Brief console output
        status = []
        if pack_info:
            status.append(f"pack={pack_size}B")
        if get_info:
            status.append(f"get={get_size}B")
        if cons_info:
            status.append("ctor")
        if is_fire_forget:
            status.append("F&F!")
        status_str = ", ".join(status) if status else "no-sym"
        print(f"  0x{opcode:04X} {cmsg_name}: {direction} [{status_str}]")

    results[sys_name] = sys_results


# ============================================================================
# GENERATE OUTPUT MARKDOWN
# ============================================================================

print(f"\n{'=' * 70}")
print(f"SUMMARY: {analyzed} opcodes analyzed")
print(f"  Constructors found: {found_constructor}")
print(f"  packData found: {found_pack}")
print(f"  getData found: {found_get}")
print(f"{'=' * 70}")

print(f"\nGenerating {OUTPUT} ...")

out = []
def w(line=""):
    out.append(line)

w("# Alliance & War Systems - Binary Analysis Report")
w(f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
w(f"# Source: libgame.so ({len(data):,} bytes)")
w(f"# Total opcodes analyzed: {analyzed}")
w(f"# Symbols found: {found_constructor} constructors, {found_pack} packData, {found_get} getData")
w()

# Summary table
w("## Quick Reference - All Systems")
w()
w("| System | Opcodes | C2S | S2C | Fire&Forget | Key Actions |")
w("|--------|---------|-----|-----|-------------|-------------|")

for sys_name, sys_info in SYSTEMS.items():
    res_list = results[sys_name]
    c2s = sum(1 for r in res_list if r['direction'] in ('C2S', 'C2S?', 'BIDI'))
    s2c = sum(1 for r in res_list if r['direction'] in ('S2C', 'BIDI'))
    ff = sum(1 for r in res_list if r['fire_forget'])
    total = len(res_list)

    # Find key actions (C2S with packData)
    key_acts = []
    for r in res_list:
        if r['pack_info'] and r['direction'] in ('C2S', 'C2S?', 'BIDI'):
            short = r['name'].replace('CMSG_', '').replace(sys_name.split('_')[0] + '_', '')
            key_acts.append(short)
    key_str = ", ".join(key_acts[:3]) if key_acts else "-"

    w(f"| {sys_name} | {total} | {c2s} | {s2c} | {ff} | {key_str} |")

w()

# Fire-and-forget summary
all_ff = []
for sys_name, res_list in results.items():
    for r in res_list:
        if r['fire_forget']:
            all_ff.append((sys_name, r))

if all_ff:
    w("## Fire-and-Forget Opcodes (No Server Response Expected)")
    w()
    w("These C2S opcodes have no matching _RETURN pair. They may be:")
    w("- One-way notifications to server")
    w("- Exploitable for rapid-fire actions without waiting")
    w("- Toggle/state changes that take effect immediately")
    w()
    w("| Opcode | Name | System | packData Size |")
    w("|--------|------|--------|---------------|")
    for sys_name, r in all_ff:
        ps = f"{r['pack_size']}B" if r['pack_info'] else "?"
        w(f"| 0x{r['opcode']:04X} | {r['name']} | {sys_name} | {ps} |")
    w()

# Detailed per-system sections
for sys_name, sys_info in SYSTEMS.items():
    res_list = results[sys_name]
    w(f"## {sys_name} - {sys_info['description']}")
    w()

    # Opcode table
    w("### Opcode Table")
    w()
    w("| Opcode | Name | Dir | Payload | Fields | Symbol Found |")
    w("|--------|------|-----|---------|--------|--------------|")

    for r in res_list:
        opcode = r['opcode']
        name = r['name'].replace('CMSG_', '')
        direction = r['direction']

        # Payload info
        if r['pack_info']:
            payload = f"{r['pack_size']}B (pack)"
        elif r['get_info']:
            payload = f"{r['get_size']}B (get)"
        else:
            payload = "-"

        # Fields
        if r['pack_fields'] and len(r['pack_fields']) > 0:
            field_parts = []
            for f in r['pack_fields']:
                sz_name = {1: 'u8', 2: 'u16', 4: 'u32', 8: 'u64'}.get(f['size'], f'?{f["size"]}')
                field_parts.append(f"{sz_name}@{f['struct_offset']:#x}")
            fields = " ".join(field_parts)
        elif r['get_fields'] and len(r['get_fields']) > 0:
            field_parts = []
            for f in r['get_fields']:
                sz_name = {1: 'u8', 2: 'u16', 4: 'u32', 8: 'u64'}.get(f['size'], f'?{f["size"]}')
                field_parts.append(sz_name)
            fields = " ".join(field_parts)
        else:
            fields = "-"

        # Symbol found
        sym_parts = []
        if r['constructor']:
            sym_parts.append("C")
        if r['pack_info']:
            sym_parts.append("P")
        if r['get_info']:
            sym_parts.append("G")
        sym_str = "+".join(sym_parts) if sym_parts else "-"
        if r['fire_forget']:
            sym_str += " F&F"

        w(f"| 0x{opcode:04X} | {name} | {direction} | {payload} | {fields} | {sym_str} |")

    w()

    # System flow
    c2s_ops = [r for r in res_list if r['direction'] in ('C2S', 'C2S?', 'BIDI')]
    s2c_ops = [r for r in res_list if r['direction'] in ('S2C', 'BIDI')]
    ff_ops = [r for r in res_list if r['fire_forget']]

    w("### System Flow")
    w()

    # Identify entry/exit/view patterns
    enter_ops = [r for r in res_list if 'ENTER' in r['name'] and '_RETURN' not in r['name']]
    exit_ops = [r for r in res_list if 'EXIT' in r['name'] and '_RETURN' not in r['name']]
    view_ops = [r for r in res_list if 'VIEW' in r['name'] and '_RETURN' not in r['name']]
    query_ops = [r for r in res_list if 'QUERY' in r['name'] and '_RETURN' not in r['name']]
    action_ops = [r for r in res_list if 'ACTION' in r['name'] and '_RETURN' not in r['name']]
    signup_ops = [r for r in res_list if 'SIGNUP' in r['name'] and '_RETURN' not in r['name']]

    if enter_ops or view_ops:
        w("**Entry Sequence:**")
        if view_ops:
            for r in view_ops:
                w(f"1. Send 0x{r['opcode']:04X} ({r['name']}) - Open view")
        if enter_ops:
            for r in enter_ops:
                w(f"2. Send 0x{r['opcode']:04X} ({r['name']}) - Enter")
        if signup_ops:
            for r in signup_ops:
                w(f"3. Send 0x{r['opcode']:04X} ({r['name']}) - Sign up")
        w()

    if query_ops:
        w("**Query/Info:**")
        for r in query_ops:
            w(f"- 0x{r['opcode']:04X} ({r['name']})")
        w()

    if exit_ops:
        w("**Exit:**")
        for r in exit_ops:
            w(f"- 0x{r['opcode']:04X} ({r['name']})")
        w()

    # Bot-useful findings
    w("### Bot-Useful Findings")
    w()

    bot_useful = []
    for r in res_list:
        name = r['name']
        if any(kw in name for kw in ['_REWARD', '_DONATE', '_BUY', '_HELP', '_SIGNUP',
                                       '_RECRUIT', '_COLLECT', '_CLAIM', '_USE',
                                       '_FINISH_TASK', '_FRESH_TASK', '_GET_REWARD']):
            if '_RETURN' not in name and '_RESULT' not in name:
                desc = "Automatable"
                if '_REWARD' in name or '_GET_REWARD' in name:
                    desc = "Reward collection"
                elif '_DONATE' in name:
                    desc = "Auto-donate"
                elif '_BUY' in name:
                    desc = "Auto-purchase"
                elif '_HELP' in name:
                    desc = "Auto-help alliance"
                elif '_SIGNUP' in name:
                    desc = "Auto-signup"
                elif '_FINISH_TASK' in name:
                    desc = "Auto-complete task"
                elif '_FRESH_TASK' in name:
                    desc = "Auto-refresh task"
                bot_useful.append((r, desc))

    if bot_useful:
        for r, desc in bot_useful:
            ps = f" ({r['pack_size']}B payload)" if r['pack_info'] else ""
            ff = " [FIRE-AND-FORGET]" if r['fire_forget'] else ""
            w(f"- **{desc}**: 0x{r['opcode']:04X} {r['name']}{ps}{ff}")
    else:
        w("- No obvious automatable actions found (mostly query/view opcodes)")
    w()

    # Vulnerability notes
    w("### Vulnerability Notes")
    w()

    if ff_ops:
        w(f"- **{len(ff_ops)} fire-and-forget opcodes** - can be sent without waiting for response")
        for r in ff_ops:
            w(f"  - 0x{r['opcode']:04X} {r['name']}")

    # Check for opcodes without return pair
    no_return = [r for r in c2s_ops if not r['has_return'] and '_REQUEST' in r['name']]
    if no_return:
        w(f"- **{len(no_return)} REQUEST opcodes without matching RETURN** - server may not validate:")
        for r in no_return:
            w(f"  - 0x{r['opcode']:04X} {r['name']}")

    if not ff_ops and not no_return:
        w("- All C2S opcodes have matching server responses (well-validated)")

    # Check for state manipulation
    set_ops = [r for r in res_list if '_SET_' in r['name'] and '_RETURN' not in r['name']]
    if set_ops:
        w(f"- **{len(set_ops)} SET operations** - potential for privilege escalation:")
        for r in set_ops:
            w(f"  - 0x{r['opcode']:04X} {r['name']}")

    w()
    w("---")
    w()


# ============================================================================
# PAYLOAD FORMAT DETAILS (for opcodes with packData)
# ============================================================================

w("## Detailed Payload Formats")
w()
w("Opcodes where packData was found and disassembled:")
w()

any_payload = False
for sys_name, res_list in results.items():
    for r in res_list:
        if r['pack_fields'] and len(r['pack_fields']) > 0:
            any_payload = True
            w(f"### 0x{r['opcode']:04X} {r['name']} ({sys_name})")
            w(f"- Symbol: `{r['pack_info'][0]}`")
            w(f"- Address: 0x{r['pack_info'][1]:08X}, Size: {r['pack_info'][2]}")
            w(f"- Total payload: {r['pack_size']} bytes")
            w(f"- Direction: {r['direction']}")
            w()
            w("| Offset | Size | Type | Struct Offset |")
            w("|--------|------|------|---------------|")
            for f in r['pack_fields']:
                sz_name = {1: 'u8', 2: 'u16', 4: 'u32', 8: 'u64'}.get(f['size'], f'bytes({f["size"]})')
                w(f"| {f['payload_offset']} | {f['size']} | {sz_name} | 0x{f['struct_offset']:02X} |")
            w()

if not any_payload:
    w("No packData payload formats were extracted. Symbols may be stripped or")
    w("use a different calling convention.")
    w()


# ============================================================================
# BOT AUTOMATION SUMMARY
# ============================================================================

w("## Bot Automation Summary")
w()
w("### Priority 1 - Daily Automatable Actions")
w()

priority1 = []
for sys_name, res_list in results.items():
    for r in res_list:
        name = r['name']
        if '_RETURN' in name or '_RESULT' in name or 'SYNC_' in name or 'NOTIFY_' in name:
            continue
        if any(kw in name for kw in ['_REWARD', '_DONATE', '_HELP', '_FINISH_TASK', '_GET_REWARD']):
            priority1.append((sys_name, r))

if priority1:
    for sys_name, r in priority1:
        ff = " [F&F]" if r['fire_forget'] else ""
        ps = f" [{r['pack_size']}B]" if r['pack_info'] else ""
        w(f"- 0x{r['opcode']:04X} {r['name']}{ps}{ff} ({sys_name})")
else:
    w("- None identified with high confidence")
w()

w("### Priority 2 - Signup/Join Actions")
w()
priority2 = []
for sys_name, res_list in results.items():
    for r in res_list:
        name = r['name']
        if '_RETURN' in name or 'SYNC_' in name:
            continue
        if any(kw in name for kw in ['_SIGNUP', '_JOIN', '_ENTER', '_CREATE']):
            priority2.append((sys_name, r))

if priority2:
    for sys_name, r in priority2:
        ff = " [F&F]" if r['fire_forget'] else ""
        w(f"- 0x{r['opcode']:04X} {r['name']}{ff} ({sys_name})")
else:
    w("- None identified")
w()

w("### Priority 3 - Info/Query (safe, read-only)")
w()
priority3_count = 0
for sys_name, res_list in results.items():
    for r in res_list:
        name = r['name']
        if any(kw in name for kw in ['_QUERY', '_INFO_REQUEST', '_RANK_REQUEST',
                                       '_LIST_REQUEST', '_VIEW_REQUEST', '_LATEST_REQUEST',
                                       '_HISTORY_REQUEST', '_CONFIG']):
            if '_RETURN' not in name:
                priority3_count += 1

w(f"- {priority3_count} read-only query/info opcodes across all systems")
w()

w("### Fire-and-Forget Exploit Candidates")
w()
w("These opcodes can be sent rapidly without waiting for server response:")
w()

ff_all = []
for sys_name, res_list in results.items():
    for r in res_list:
        if r['fire_forget']:
            ff_all.append((sys_name, r))

if ff_all:
    w("| Opcode | Name | System | Payload |")
    w("|--------|------|--------|---------|")
    for sys_name, r in ff_all:
        ps = f"{r['pack_size']}B" if r['pack_info'] else "?"
        w(f"| 0x{r['opcode']:04X} | {r['name']} | {sys_name} | {ps} |")
else:
    w("None identified - all C2S opcodes appear to have server responses.")
w()


# ============================================================================
# CROSS-SYSTEM ANALYSIS
# ============================================================================

w("## Cross-System Analysis")
w()

w("### Common Patterns Across War Systems")
w()
w("Most war systems follow a consistent pattern:")
w("1. **SYS_INFO/CONFIG** - Server pushes system state on login")
w("2. **ENTER_VIEW** - Client opens the UI (no gameplay effect)")
w("3. **QUERY_ACTION** - Client requests current event status")
w("4. **SIGNUP** - Client registers for the event")
w("5. **ENTER** - Client enters the battlefield")
w("6. **ACTION** - Gameplay actions during the event")
w("7. **RANK_VIEW** - Check rankings")
w("8. **REWARD** - Collect rewards")
w("9. **EXIT** - Leave the battlefield")
w()

w("### Systems with Donate/Help (daily farm):")
w()
donate_systems = []
for sys_name, res_list in results.items():
    donates = [r for r in res_list if 'DONATE' in r['name'] and '_RETURN' not in r['name']]
    if donates:
        donate_systems.append((sys_name, donates))
        for r in donates:
            w(f"- {sys_name}: 0x{r['opcode']:04X} {r['name']}")
w()

w("### Systems with Shop/Buy (resource spending):")
w()
for sys_name, res_list in results.items():
    buys = [r for r in res_list if ('_BUY' in r['name'] or '_SHOP' in r['name']) and '_RETURN' not in r['name']]
    if buys:
        for r in buys:
            w(f"- {sys_name}: 0x{r['opcode']:04X} {r['name']}")
w()

w("### Systems with Reward Collection:")
w()
for sys_name, res_list in results.items():
    rewards = [r for r in res_list if '_REWARD' in r['name'] and '_RETURN' not in r['name'] and '_RESULT' not in r['name'] and 'CONFIG' not in r['name'] and 'INFO' not in r['name'] and 'SYNC' not in r['name']]
    if rewards:
        for r in rewards:
            ff = " [F&F]" if r['fire_forget'] else ""
            w(f"- {sys_name}: 0x{r['opcode']:04X} {r['name']}{ff}")
w()


# ============================================================================
# STATISTICS
# ============================================================================

w("## Statistics")
w()
w(f"- Total systems analyzed: {len(SYSTEMS)}")
w(f"- Total opcodes: {analyzed}")
w(f"- Constructors found in symbols: {found_constructor}")
w(f"- packData functions found: {found_pack}")
w(f"- getData functions found: {found_get}")
w(f"- Fire-and-forget C2S opcodes: {len(ff_all)}")

c2s_total = sum(1 for res_list in results.values() for r in res_list if r['direction'] in ('C2S', 'C2S?'))
s2c_total = sum(1 for res_list in results.values() for r in res_list if r['direction'] == 'S2C')
bidi_total = sum(1 for res_list in results.values() for r in res_list if r['direction'] == 'BIDI')

w(f"- C2S (client to server): {c2s_total}")
w(f"- S2C (server to client): {s2c_total}")
w(f"- Bidirectional: {bidi_total}")
w()

# Write output
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

print(f"\nOutput written to: {OUTPUT}")
print(f"Total lines: {len(out)}")
print("DONE.")

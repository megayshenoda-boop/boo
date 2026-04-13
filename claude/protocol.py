"""
IGG Conquerors Bot - Protocol Constants
========================================
Opcodes extracted via Capstone ARM64 disassembly of libgame.so constructors.
2,272 opcodes mapped from 2,293 CMSG constructors.
"""

# ══════════════════════════════════════════════════════════════
#  CONNECTION FLOW OPCODES
# ══════════════════════════════════════════════════════════════
OP_GATEWAY_AUTH      = 0x000B  # CMSG_LOGIN
OP_GATEWAY_REDIRECT  = 0x000C  # CMSG_LOGIN_RETURN
OP_GAME_LOGIN        = 0x001F  # CMSG_ENTER_GAME_REQUEST
OP_GAME_LOGIN_OK     = 0x0020  # CMSG_ENTER_GAME_RETURN
OP_WORLD_ENTRY       = 0x0021  # CMSG_USERINFO_REQUEST
OP_HEARTBEAT         = 0x0042  # CMSG_KEEP_LIVE_TEST

# ══════════════════════════════════════════════════════════════
#  DATA OPCODES (Server -> Client)
# ══════════════════════════════════════════════════════════════
OP_SYN_ATTRIBUTE     = 0x0033  # CMSG_SYN_ATTRIBUTE_CHANGE (u32 attr_id + u64 value)
OP_PLAYER_PROFILE    = 0x0034  # CMSG_ATTRIBUTE_INFO
OP_PM_COMMAND        = 0x0035  # CMSG_PM_COMMAND (admin/GM)
OP_ERROR_STATUS      = 0x0037  # Error/status (u32 code + u32 param + u32 zero)
OP_CASTLE_DATA       = 0x0038  # CMSG_EXTRA_ATTRIBUTE_INFO (contains server_key!)
OP_VIP_INFO          = 0x003F  # CMSG_VIP_LOGIN_INFO
OP_SERVER_TIME       = 0x0043  # CMSG_SYN_SERVER_TIME
OP_ITEM_INFO         = 0x0064  # CMSG_ITEM_INFO (u32 count + [u32 id, u32 qty] * N)
OP_SYNC_MARCH        = 0x006F  # CMSG_SYNC_MARCH
OP_MARCH_RECALL      = 0x0070  # March recall/return (9B: march_id + kingdom + status)
OP_MARCH_STATE       = 0x0071  # March state sync (70B: march_id+kingdom+hero+coords+name)
OP_TILE_DATA         = 0x0076  # Tile data response
OP_TILE_DETAIL       = 0x0077  # Tile detail response
OP_NOTIFY_CASTLE     = 0x007B  # CMSG_NOTIFY_OWNER_CASTLE
OP_BUILDING_INFO     = 0x0097  # CMSG_BUILDING_INFO (u16 count + 19B entries)
OP_WORKER_INFO       = 0x0098  # CMSG_WORKER_INFO
OP_HERO_INFO         = 0x00AA  # CMSG_HERO_INFO (u32 count + 109B entries)
OP_MARCH_ACK         = 0x00B8  # March ACK (1B=ok or 10B with hero IDs)
OP_SCIENCE_INFO      = 0x00BE  # CMSG_SCIENCE_INFO
OP_CHAT_HISTORY      = 0x026D  # CMSG_CHAT_HISTORY (u16 channel + messages)
OP_SOLDIER_INFO      = 0x06C2  # CMSG_SYS_SOLDIER_INFO (u32 count + entries)
OP_PASSWORD_INFO     = 0x1B8A  # CMSG_PASSWORD_CHECK_RETURN (gate for 0x1B8B)
OP_PASSWORD_CHECK    = 0x1B8B  # CMSG_PASSWORD_CHECK_REQUEST (challenge-response)

# ══════════════════════════════════════════════════════════════
#  REWARD/DAILY OPCODES (fire-and-forget, 2B payload)
# ══════════════════════════════════════════════════════════════
OP_EVERYDAY_GIFT_NEW       = 0x189D  # Daily gift (fire & forget!)
OP_ACHIEVEMENT_SCORE       = 0x0226  # Achievement score reward
OP_LUXURY_REWARD           = 0x0989  # Luxury reward (F&F!)
OP_KING_ROAD_REWARD        = 0x0993  # King's Road reward
OP_EXP_REWARD              = 0x0A07  # Championship EXP
OP_EXTRA_GIFTPACK_NEW      = 0x16B2  # Extra giftpack (F&F CRITICAL!)
OP_RETURN_EVENT_NEW        = 0x16CE  # Return event reward (F&F CRITICAL!)
OP_ARENA_CHALLENGE         = 0x05F1  # Arena fight
OP_ARENA_TIMES_RESTORE     = 0x05EB  # Arena restore (F&F!)
OP_EXPEDITION_BATTLE       = 0x02B6  # Expedition fight
OP_LUCKY_TURNTABLE         = 0x039C  # Lucky spin
OP_WHEEL_TURN              = 0x0E75  # Wheel spin
OP_DOUBLE_LOTTERY          = 0x1D4D  # Double lottery
OP_LEAGUEPASS_REWARD       = 0x166C  # Guild Pass reward
OP_LEAGUEPASS_TASK         = 0x1670  # Guild Pass task
OP_LEAGUE_BF_REWARD        = 0x07EF  # League battlefield reward
OP_BIG_BOSS_DONATE         = 0x1F0F  # Guild boss donate
OP_LOSTLAND_DONATE         = 0x15B7  # Lost Land donate
OP_SERVER_MISSION          = 0x13BD  # Server mission
OP_DAILYCONSUME_REWARD     = 0x1453  # Daily consume
OP_RECHARGE_BONUS          = 0x1774  # Recharge bonus
OP_EXCHANGE_REWARD         = 0x099F  # Exchange reward

# ══════════════════════════════════════════════════════════════
#  NEW-STYLE ACTION OPCODES (Encrypted via CMsgCodec)
# ══════════════════════════════════════════════════════════════
OP_START_BUILDUP     = 0x0CE4  # CMSG_START_BUILDUP_NEW - Alliance rally start
OP_JOIN_BUILDUP      = 0x0CE5  # CMSG_JOIN_BUILDUP_NEW - Join rally
OP_START_DEFEND      = 0x0CE6  # CMSG_START_DEFEND_NEW - Garrison
OP_BACK_DEFEND       = 0x0CE7  # CMSG_BACK_DEFEND_NEW - Return from garrison
OP_START_MARCH       = 0x0CE8  # CMSG_START_MARCH_NEW - March/Gather/Attack/Scout
OP_CANCEL_MARCH      = 0x0CE9  # CMSG_CANCEL_MARCH_NEW
OP_MARCH_USE_ITEM    = 0x0CEA  # CMSG_MARCH_USE_ITEM_NEW
OP_ENABLE_VIEW       = 0x0CEB  # CMSG_ENABLE_VIEW_NEW - Scout/view map area (ARM64 CONFIRMED)
OP_LEAGUE_DONATE     = 0x0CEC  # CMSG_DO_LEAGUE_DONATE_CRIT_NEW
OP_TRAIN             = 0x0CED  # CMSG_SOLDIER_NORMAL_PRODUCE_REQUEST_NEW (ARM64 CONFIRMED)
OP_RESEARCH          = 0x0CEE  # CMSG_SCIENCE_NORMAL_STUDY_REQUEST_NEW (ARM64 CONFIRMED)
OP_BUILD             = 0x0CEF  # CMSG_BUILDING_OPERAT_REQUEST_NEW (ARM64 CONFIRMED)
OP_WORLD_BATTLE      = 0x0CF0  # CMSG_WORLD_BATTLE_NEW_SIGN_UP_REQUEST_NEW
OP_MOVE_CASTLE       = 0x0CF1  # CMSG_MOVE_CASTLE_NEW
OP_GET_OTHER_ATTR    = 0x0CF2  # CMSG_GET_OTHER_EXTRA_ATTRIBUTE_NEW
OP_RAID_PLAYER       = 0x0CF3  # CMSG_RAID_PLAYER_REQUEST_NEW
OP_ARENA_INFO        = 0x0CF4  # CMSG_ARENA_MATCH_INFO_REQUEST_NEW
OP_ARENA_CHANGE      = 0x0CF5  # CMSG_ARENA_CHANGE_MATCH_REQUEST_NEW
OP_MAIL_REQUEST      = 0x0CF6  # CMSG_MAILBOX_MAIL_REQUEST_NEW
OP_MAIL_OPERATION    = 0x0CF7  # CMSG_MAILBOX_MAIL_OPERATION_NEW
OP_SHOP_BUY          = 0x0CF8  # CMSG_ITEM_SHOP_BUY_REQUEST_NEW
OP_BUILD_FIX         = 0x0CF9  # CMSG_BUILDING_OPERAT_REQUEST_FIX_NEW
OP_MARCH_ONEKEY_ITEM = 0x0CFB  # CMSG_MARCH_USE_ITEM_ONEKEY

# ══════════════════════════════════════════════════════════════
#  OLD-STYLE OPCODES (unencrypted)
# ══════════════════════════════════════════════════════════════
# Items
OP_ITEM_USE           = 0x0065  # CMSG_ITEM_USE
OP_ITEM_USE_RESULT    = 0x0066  # CMSG_ITEM_USE_RESULT
OP_ITEM_SELL          = 0x0067  # CMSG_ITEM_SELL
OP_ITEM_USE_CHOOSE    = 0x0069  # CMSG_ITEM_USE_CHOOSE

# March (old)
OP_START_MARCH_OLD    = 0x0072  # CMSG_START_MARCH
OP_CANCEL_MARCH_OLD   = 0x0073  # CMSG_CANCEL_MARCH
OP_MOVE_CASTLE_OLD    = 0x0074  # CMSG_MOVE_CASTLE

# Building (old)
OP_BUILD_OLD          = 0x009D  # CMSG_BUILDING_OPERAT_REQUEST
OP_BUILD_HELP         = 0x009F  # CMSG_BUILDING_HELP_REQUEST
OP_EXCHANGE_BUILD     = 0x00A1  # CMSG_EXCHANGE_BUILDING_REQUEST
OP_BUILD_ONEKEY       = 0x00A4  # CMSG_BUILDING_OPERAT_ONEKEY_REQUEST

# Science/Research (old)
OP_RESEARCH_OLD       = 0x00BF  # CMSG_SCIENCE_NORMAL_STUDY_REQUEST
OP_RESEARCH_GOLD      = 0x00C0  # CMSG_SCIENCE_GOLD_STUDY_REQUEST
OP_RESEARCH_CANCEL    = 0x00C1  # CMSG_SCIENCE_CANCEL_STUDY_REQUEST
OP_RESEARCH_GOLD_SPD  = 0x00C3  # CMSG_SCIENCE_GOLD_SPEED
OP_RESEARCH_ITEM_SPD  = 0x00C4  # CMSG_SCIENCE_ITEM_SPEED
OP_RESEARCH_HELP      = 0x00C6  # CMSG_SCIENCE_HELP_REQUEST
OP_RESEARCH_ONEKEY    = 0x00C7  # CMSG_SCIENCE_ITEM_SPEED_ONEKEY

# Traps
OP_TRAP_BUILD         = 0x014B  # CMSG_TRAP_BUILD
OP_TRAP_CANCEL        = 0x014E  # CMSG_TRAP_BUILD_CANCEL
OP_TRAP_GOLD_SPD      = 0x0150  # CMSG_TRAP_GOLD_ACCELERATE
OP_TRAP_ITEM_SPD      = 0x0151  # CMSG_TRAP_ITEM_ACCELERATE
OP_TRAP_DESTROY       = 0x0154  # CMSG_TRAP_DESTROY
OP_TRAP_ONEKEY        = 0x0156  # CMSG_TRAP_ITEM_ACCELERATE_ONEKEY

# Soldier/Training (old)
OP_TRAIN_OLD          = 0x06C3  # CMSG_SOLDIER_NORMAL_PRODUCE_REQUEST
OP_TRAIN_GOLD         = 0x06C5  # CMSG_SOLDIER_GOLD_PRODUCE_REQUEST
OP_TRAIN_GOLD_SPD     = 0x06C6  # CMSG_SOLDIER_GOLD_SPEED_PRODUCE_REQUEST
OP_TRAIN_ITEM_SPD     = 0x06C7  # CMSG_SOLDIER_ITEM_SPEED_PRODUCE_REQUEST
OP_TRAIN_COMPLETE     = 0x06C9  # CMSG_SOLDIER_PRODUCE_OVER_REQUEST
OP_HEAL               = 0x06CB  # CMSG_SOLDIER_NORMAL_CURE_REQUEST
OP_HEAL_GOLD          = 0x06CD  # CMSG_SOLDIER_GOLD_CURE_REQUEST
OP_HEAL_GOLD_SPD      = 0x06CE  # CMSG_SOLDIER_GOLD_SPEED_CURE_REQUEST
OP_HEAL_ITEM_SPD      = 0x06CF  # CMSG_SOLDIER_ITEM_SPEED_CURE_REQUEST
OP_HEAL_COMPLETE      = 0x06D1  # CMSG_SOLDIER_CURE_OVER_REQUEST
OP_TRAIN_ONEKEY       = 0x06D4  # CMSG_SOLDIER_ITEM_SPEED_PRODUCE_ONEKEY_REQUEST
OP_HEAL_ONEKEY        = 0x06D6  # CMSG_SOLDIER_ITEM_SPEED_CURE_ONEKEY_REQUEST

# Alliance
OP_LEAGUE_TECH_UP     = 0x01EC  # CMSG_LEAGUE_SCIENCE_UPGRADE
OP_LEAGUE_DONATE_OLD  = 0x01ED  # CMSG_LEAGUE_SCIENCE_DONATE
OP_LEAGUE_SHOP_BUY    = 0x01FE  # CMSG_LEAGUE_SHOP_BUY

# ══════════════════════════════════════════════════════════════
#  NEWLY DISCOVERED OPCODES (2026-04-04, from constructor analysis)
# ══════════════════════════════════════════════════════════════
# Rewards & Daily - ALL 2-byte payload (u16 id)
OP_RECEIVE_SIGN_ACTIVITY  = 0x01DE  # CMSG_RECEIVE_SIGN_ACTIVITY
OP_OUTFIRE               = 0x01D3  # CMSG_OUTFIRE_REQUEST
OP_ACHIEVEMENT_REWARD    = 0x0224  # CMSG_ACHIEVEMENT_RECEIVE_REWARD_REQUEST
OP_POWER_TASK_REWARD     = 0x022C  # CMSG_POWER_TASK_REWARD_REQUEST (8B payload!)
OP_MONTH_REFRESH         = 0x0280  # CMSG_MONTH_REFRESH_REQUEST
OP_DAY_REFRESH           = 0x0281  # CMSG_DAY_REFRESH_REQUEST
OP_SIGN_REQUEST          = 0x0284  # CMSG_SIGN_REQUEST
OP_APPEND_SIGN           = 0x0285  # CMSG_APPEND_SIGN_REQUEST
OP_ONLINE_REWARD         = 0x028F  # CMSG_NEW_ONLINE_REWARD_REQUEST
OP_RANDOM_ONLINE_REWARD  = 0x0292  # CMSG_RANDOM_ONLINE_REWARD_REQUEST
OP_EXPEDITION_INFO       = 0x02B2  # CMSG_EXPEDITION_INFO_REQUEST
OP_EVERYDAY_GIFT         = 0x0312  # CMSG_EVERY_DAY_GIFTPACK_REWARD_REQUEST
OP_HERO_RECRUIT          = 0x0323  # CMSG_HERO_SOLDIER_RECRUIT_REQUEST (NOT pre-march!)
OP_REQUEST_MONSTER_POS   = 0x033E  # CMSG_REQUEST_MONSTER_POS (tile search)
OP_CAMEL_SHOP_INFO       = 0x038E  # CMSG_CAMEL_SHOP_INFO_REQUEST
OP_CAMEL_SHOP_BUY        = 0x0390  # CMSG_CAMEL_SHOP_BUY_REQUEST
OP_CAMEL_SHOP_REFRESH    = 0x0392  # CMSG_CAMEL_SHOP_REFRESH_REQUEST
OP_LUCKY_TURN            = 0x039C  # CMSG_LUCKY_TURNTABLE_TURN_REQUEST
OP_ARENA_BUY_TIMES       = 0x05EC  # CMSG_ARENA_BUY_TIMES_REQUEST
OP_RECEIVE_REWARD        = 0x062C  # CMSG_RECEIVE_REWARD_REQUEST
OP_RECEIVE_REWARD_BATCH  = 0x062F  # CMSG_RECEIVE_REWARD_BATCH_REQUEST
OP_ACCUMULATION_REWARD   = 0x069D  # CMSG_RECEIVE_ACCUMULATION_REWARD_REQUEST
OP_MICROPAY_DAILY        = 0x06FB  # CMSG_MICROPAYMENT_DAILY_REWARD_REQUEST
OP_DOWNLOAD_REWARD       = 0x06FD  # CMSG_DOWN_LOAD_REWARD_REQUEST
OP_MOBILIZATION_REWARD   = 0x07BE  # CMSG_MOBILIZATION_GET_REWARD_REQUEST
OP_ALLIANCE_HELP         = 0x1ACD  # CMSG_DAMAGE_HELP
OP_CITY_BUFF_USE         = 0x0111  # CMSG_CITY_BUFF_USE

# Auto-farming opcodes
OP_AUTO_HANDUP_CHANGE    = 0x1933  # CMSG_AUTO_HANDUP_CHANGE_REQUEST (VIP required)
OP_KING_ROAD_REWARD      = 0x0993  # CMSG_KING_ROAD_REWARD_REQUEST (2B)
OP_GAIN_EXP_REWARD       = 0x0A07  # CMSG_GAIN_EXP_REWARD_REQUEST (2B)
OP_LUXURY_REWARD         = 0x0989  # CMSG_RECEIVE_LUXURY_REWARD (2B)
OP_LUCKY_SHOP_CARD       = 0x09A7  # CMSG_LUCKY_SHOP_SCRATCH_CARD (2B)

# ══════════════════════════════════════════════════════════════
#  SERVER RESPONSE OPCODES (observed from PCAP)
# ══════════════════════════════════════════════════════════════
OP_ACTION_CONFIRM     = 0x02D1
OP_TIMER_SET          = 0x11C8
OP_BUILDING_DATA      = 0x021C
OP_RESOURCE_DEDUCT    = 0x022B
OP_TRAINING_ENTRY     = 0x06EB
OP_MARCH_DATA         = 0x0636

# ══════════════════════════════════════════════════════════════
#  OPCODE NAME MAP (for logging)
# ══════════════════════════════════════════════════════════════
OPCODE_NAMES = {
    0x0002: "HEARTBEAT_ECHO",
    0x000B: "GW_AUTH", 0x000C: "GW_REDIRECT",
    0x001F: "GS_LOGIN", 0x0020: "GS_LOGIN_OK", 0x0021: "WORLD_ENTRY",
    0x0033: "SYN_ATTRIBUTE", 0x0034: "PLAYER_PROFILE",
    0x0035: "PM_COMMAND", 0x0037: "ERROR_STATUS",
    0x0038: "CASTLE_DATA", 0x003F: "VIP_INFO",
    0x0042: "HEARTBEAT", 0x0043: "SERVER_TIME",
    0x004D: "FIRST_BIND_REWARD",
    0x0064: "ITEM_INFO", 0x0065: "ITEM_USE", 0x006F: "SYNC_MARCH",
    0x0070: "MARCH_RECALL", 0x0071: "MARCH_STATE",
    0x0076: "TILE_DATA", 0x0077: "TILE_DETAIL",
    0x007B: "NOTIFY_CASTLE",
    0x0097: "BUILDING_INFO", 0x0098: "WORKER_INFO",
    0x009D: "BUILD_OLD", 0x009E: "BUILD_RETURN", 0x009F: "BUILD_HELP",
    0x00AA: "HERO_INFO", 0x00B8: "MARCH_ACK", 0x00BE: "SCIENCE_INFO",
    0x00BF: "RESEARCH_OLD", 0x00C6: "RESEARCH_HELP",
    0x0111: "CITY_BUFF_USE",
    0x014B: "TRAP_BUILD",
    0x01D3: "OUTFIRE", 0x01DE: "RECEIVE_SIGN",
    0x021C: "BUILDING_DATA", 0x0224: "ACHIEVEMENT_REWARD",
    0x022B: "RESOURCE_DEDUCT", 0x022C: "POWER_TASK_REWARD",
    0x0280: "MONTH_REFRESH", 0x0281: "DAY_REFRESH",
    0x0284: "SIGN", 0x0285: "APPEND_SIGN",
    0x028F: "ONLINE_REWARD", 0x0292: "RANDOM_ONLINE_REWARD",
    0x02D1: "ACTION_CONFIRM",
    0x0312: "EVERYDAY_GIFT", 0x0323: "HERO_RECRUIT",
    0x033E: "REQUEST_MONSTER_POS", 0x033F: "MONSTER_POS_RESULT",
    0x036C: "SERVER_TICK", 0x0390: "CAMEL_SHOP_BUY",
    0x039B: "INIT_TS", 0x039C: "LUCKY_TURN",
    0x05EC: "ARENA_BUY_TIMES",
    0x0636: "MARCH_DATA", 0x062C: "RECEIVE_REWARD",
    0x062F: "RECEIVE_REWARD_BATCH",
    0x069D: "ACCUMULATION_REWARD",
    0x06C2: "SOLDIER_INFO",
    0x06C3: "TRAIN_OLD", 0x06CB: "HEAL",
    0x06C7: "SPEED_TRAIN", 0x06D4: "ONEKEY_SPEED_TRAIN",
    0x06EB: "TRAINING_ENTRY",
    0x0CE4: "START_BUILDUP", 0x0CE5: "JOIN_BUILDUP",
    0x0CE6: "START_DEFEND", 0x0CE7: "BACK_DEFEND",
    0x0CE8: "START_MARCH", 0x0CE9: "CANCEL_MARCH",
    0x0CEA: "MARCH_USE_ITEM", 0x0CEB: "ENABLE_VIEW",
    0x0CEC: "LEAGUE_DONATE", 0x0CED: "TRAIN",
    0x0CEE: "RESEARCH", 0x0CEF: "BUILD",
    0x0CF0: "WORLD_BATTLE", 0x0CF1: "MOVE_CASTLE",
    0x0CF3: "RAID_PLAYER", 0x0CF8: "SHOP_BUY",
    0x0CF9: "BUILD_FIX",
    0x026D: "CHAT_HISTORY",
    0x1933: "AUTO_HANDUP_CHANGE",
    0x1ACD: "ALLIANCE_HELP",
    0x11C8: "TIMER_SET",
    0x1ACD: "ALLIANCE_HELP",
    0x1B8B: "PASSWORD_CHECK",
}


def opname(opcode):
    """Get human-readable name for an opcode."""
    return OPCODE_NAMES.get(opcode, f"0x{opcode:04X}")


# ══════════════════════════════════════════════════════════════
#  GAME CONSTANTS
# ══════════════════════════════════════════════════════════════

BUILDINGS = {
    'castle': 1, 'barracks': 2, 'infirmary': 3, 'academy': 4,
    'workshop': 5, 'embassy': 6, 'prison': 7, 'altar': 8,
    'watchtower': 9, 'treasure_trove': 10, 'wall': 11,
    'farm': 12, 'lumber_mill': 13, 'quarry': 14, 'mine': 15,
    'manor': 16, 'battle_hall': 17, 'monster_base': 18,
    'cargo_ship': 19, 'gymnos': 20, 'spire': 21,
}

TROOPS = {
    'infantry_t1': 101, 'infantry_t2': 102, 'infantry_t3': 103, 'infantry_t4': 104,
    'ranged_t1': 201, 'ranged_t2': 202, 'ranged_t3': 203, 'ranged_t4': 204,
    'cavalry_t1': 301, 'cavalry_t2': 302, 'cavalry_t3': 303, 'cavalry_t4': 304,
    'siege_t1': 401, 'siege_t2': 402, 'siege_t3': 403, 'siege_t4': 404,
}

# March types (from PCAP analysis - NOT simple enums!)
# The game uses composite values, not sequential 1-6
MARCH_TYPE_GATHER    = 0x1749  # PCAP-verified (food tiles)
MARCH_TYPE_GATHER_W2 = 0x174A  # Wheat level 2 (from test_gather_clean.py)
MARCH_TYPE_ATTACK    = 2       # UNVERIFIED - needs PCAP confirmation
MARCH_TYPE_SCOUT     = 3       # UNVERIFIED - needs PCAP confirmation
MARCH_TYPE_REINFORCE = 5       # UNVERIFIED - needs PCAP confirmation
MARCH_TYPE_RALLY     = 6       # UNVERIFIED - needs PCAP confirmation

BUILD_OP_UPGRADE     = 1
BUILD_OP_DEMOLISH    = 2
BUILD_OP_BUILD_NEW   = 3

# CMsgCodec encryption lookup table (extracted from libgame.so ARM64)
CMSG_TABLE = [0x58, 0xef, 0xd7, 0x14, 0xa2, 0x3b, 0x9c]
SERVER_KEY_FIELD_ID = 0x4F  # Field 79 in 0x0038 packet

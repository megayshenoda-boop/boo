#!/usr/bin/env python3
"""
52_chat_social_events_analysis.py
=================================
Comprehensive analysis of chat, social, events, shops, gifts,
mini-games, mobilization, and server mission systems in libgame.so.

Searches for opcodes, constructors, packData/getData, fire-and-forget
patterns, reward endpoints, and complete message flows.

Output: D:\\CascadeProjects\\analysis\\findings\\chat_social_events.md
"""

import sys
import struct
import os
import re
from collections import defaultdict, OrderedDict

sys.path.insert(0, r'D:\CascadeProjects\claude')
sys.path.insert(0, r'D:\CascadeProjects\analysis\findings')

try:
    from cmsg_opcodes import CMSG_OPCODES
except ImportError:
    CMSG_OPCODES = {}
    print("[WARN] Could not import CMSG_OPCODES, using empty map")

try:
    from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
    HAS_CAPSTONE = True
except ImportError:
    HAS_CAPSTONE = False
    print("[WARN] capstone not available, skipping disassembly")

# ============================================================
# Binary setup
# ============================================================
BINARY = r'D:\CascadeProjects\libgame.so'
OUTPUT = r'D:\CascadeProjects\analysis\findings\chat_social_events.md'
DYNSTR_OFF = 0x682A10
DYNSYM_OFF = 0x2F8
DYNSYM_SIZE = 0x682758

with open(BINARY, 'rb') as f:
    data = f.read()

print(f"[*] Loaded {len(data):,} bytes from libgame.so")
print(f"[*] {len(CMSG_OPCODES)} opcodes in CMSG_OPCODES map")

if HAS_CAPSTONE:
    md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
    md.detail = True

# ============================================================
# Output buffer
# ============================================================
out_lines = []

def p(msg=""):
    out_lines.append(msg)
    try:
        print(msg)
    except Exception:
        print(msg.encode('ascii', 'replace').decode())

# ============================================================
# Symbol helpers
# ============================================================
_symbol_cache = None

def load_symbols():
    global _symbol_cache
    if _symbol_cache is not None:
        return _symbol_cache
    _symbol_cache = []
    pos = DYNSYM_OFF
    while pos + 24 <= DYNSYM_OFF + DYNSYM_SIZE:
        st_name = struct.unpack('<I', data[pos:pos+4])[0]
        st_value = struct.unpack('<Q', data[pos+8:pos+16])[0]
        st_size = struct.unpack('<Q', data[pos+16:pos+24])[0]
        if st_name > 0 and st_name < 0x300000 and st_value > 0:
            try:
                name_end = data.index(b'\x00', DYNSTR_OFF + st_name)
                name = data[DYNSTR_OFF + st_name:name_end].decode('ascii', errors='replace')
                _symbol_cache.append((name, st_value, st_size))
            except Exception:
                pass
        pos += 24
    print(f"[*] Loaded {len(_symbol_cache)} symbols")
    return _symbol_cache

def find_symbols(name_part, must_contain=None, must_not_contain=None):
    """Find all symbols containing name_part."""
    results = []
    for name, addr, size in load_symbols():
        if name_part in name:
            if must_contain and must_contain not in name:
                continue
            if must_not_contain and must_not_contain in name:
                continue
            results.append((name, addr, size))
    return results

def find_packdata(class_name):
    """Find packData symbol for a class."""
    hits = find_symbols(class_name, must_contain='8packData')
    return hits[0] if hits else None

def find_getdata(class_name):
    """Find getData symbol for a class."""
    hits = find_symbols(class_name, must_contain='7getData')
    return hits[0] if hits else None

def find_constructor(class_name):
    """Find constructor C1Ev/C2Ev for a class."""
    hits = find_symbols(class_name, must_contain='C1Ev')
    hits = [h for h in hits if '8packData' not in h[0] and '7getData' not in h[0]]
    if not hits:
        hits = find_symbols(class_name, must_contain='C2Ev')
        hits = [h for h in hits if '8packData' not in h[0] and '7getData' not in h[0]]
    return hits[0] if hits else None

def find_all_class_symbols(class_name):
    """Find all symbols for a class - constructor, packData, getData, etc."""
    all_syms = find_symbols(class_name)
    result = {
        'constructor': None,
        'packData': None,
        'getData': None,
        'other': []
    }
    for name, addr, size in all_syms:
        if '8packData' in name:
            result['packData'] = (name, addr, size)
        elif '7getData' in name:
            result['getData'] = (name, addr, size)
        elif 'C1Ev' in name or 'C2Ev' in name:
            if result['constructor'] is None:
                result['constructor'] = (name, addr, size)
        else:
            result['other'].append((name, addr, size))
    return result

# ============================================================
# Opcode extraction from constructor
# ============================================================
def extract_opcode_from_constructor(addr, size):
    """Extract opcode from constructor by looking for MOV with immediate."""
    if not HAS_CAPSTONE or not addr:
        return None
    max_bytes = min(size if size > 0 else 200, 400)
    code = data[addr:addr + max_bytes]
    try:
        insns = list(md.disasm(code, addr))
    except Exception:
        return None

    for insn in insns[:40]:
        if insn.mnemonic == 'ret':
            break
        # movz/movk pattern for opcode store
        if insn.mnemonic in ('mov', 'movz', 'orr') and '#' in insn.op_str:
            parts = insn.op_str.split('#')
            try:
                val = int(parts[-1].split(',')[0].strip().rstrip(']'), 0)
                if 0x100 <= val <= 0x2000:
                    return val
            except Exception:
                pass
        # str wN, [xN, #offset] where wN was loaded with opcode
        if insn.mnemonic == 'movz' and '#' in insn.op_str:
            parts = insn.op_str.split('#')
            try:
                val = int(parts[-1].split(',')[0].strip(), 0)
                if 0x100 <= val <= 0x2000:
                    return val
            except Exception:
                pass
    return None

# ============================================================
# Payload format analysis
# ============================================================
def analyze_packdata(addr, size):
    """Analyze packData to extract payload field sizes."""
    if not HAS_CAPSTONE or not addr:
        return []
    max_bytes = min(size if size > 0 else 600, 2000)
    code = data[addr:addr + max_bytes]
    try:
        insns = list(md.disasm(code, addr))
    except Exception:
        return []

    payload_fields = []
    current_write_size = 0
    payload_offset = 0
    this_reg = 'x0'

    for i, insn in enumerate(insns):
        if insn.mnemonic == 'ret' and insn.address > addr + 20:
            break

        if insn.mnemonic == 'mov' and insn.op_str.startswith('x19, x0'):
            this_reg = 'x19'
        if insn.mnemonic == 'mov' and insn.op_str.startswith('x20, x0'):
            this_reg = 'x20'

        if insn.mnemonic == 'add' and '#' in insn.op_str:
            parts = insn.op_str.split('#')
            try:
                add_val = int(parts[-1], 0)
                if add_val in (1, 2, 4, 8):
                    for j in range(i+1, min(i+6, len(insns))):
                        if 'strh' in insns[j].mnemonic and '#0xa' in insns[j].op_str:
                            current_write_size = add_val
                            break
            except Exception:
                pass

        if insn.mnemonic in ('ldrh', 'ldrb', 'ldr', 'ldrsb', 'ldrsh', 'ldrsw'):
            if f'[{this_reg}]' in insn.op_str or f'[{this_reg},' in insn.op_str:
                offset = 0
                if '#' in insn.op_str:
                    try:
                        offset = int(insn.op_str.split('#')[-1].rstrip(']').rstrip('!'), 0)
                    except Exception:
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
                    payload_fields.append({
                        'struct_offset': offset,
                        'size': current_write_size if current_write_size else field_size,
                        'payload_offset': payload_offset,
                    })
                    payload_offset += current_write_size if current_write_size else field_size
                    current_write_size = 0

    return payload_fields

def analyze_getdata(addr, size):
    """Analyze getData to extract response field sizes."""
    if not HAS_CAPSTONE or not addr:
        return []
    max_bytes = min(size if size > 0 else 600, 2000)
    code = data[addr:addr + max_bytes]
    try:
        insns = list(md.disasm(code, addr))
    except Exception:
        return []

    resp_fields = []
    current_read_size = 0
    resp_offset = 0

    for i, insn in enumerate(insns):
        if insn.mnemonic == 'ret' and insn.address > addr + 20:
            break

        # Read from CIStream: ldr + add wN, wN, #SIZE for position update
        if insn.mnemonic == 'add' and '#' in insn.op_str:
            parts = insn.op_str.split('#')
            try:
                add_val = int(parts[-1], 0)
                if add_val in (1, 2, 4, 8):
                    # Check for strh to position field nearby
                    for j in range(i+1, min(i+6, len(insns))):
                        if 'strh' in insns[j].mnemonic and '#0xa' in insns[j].op_str:
                            current_read_size = add_val
                            resp_fields.append({
                                'size': add_val,
                                'resp_offset': resp_offset,
                            })
                            resp_offset += add_val
                            break
            except Exception:
                pass

    return resp_fields

# ============================================================
# String search
# ============================================================
def find_strings(patterns, limit=50):
    """Find ASCII strings matching patterns."""
    results = defaultdict(list)
    current = bytearray()
    start_off = 0
    for i in range(len(data)):
        b = data[i]
        if 0x20 <= b < 0x7F:
            if len(current) == 0:
                start_off = i
            current.append(b)
        else:
            if 4 <= len(current) <= 300:
                s = current.decode('ascii', errors='ignore')
                s_lower = s.lower()
                for pat in patterns:
                    if pat.lower() in s_lower:
                        if len(results[pat]) < limit:
                            results[pat].append((start_off, s))
                        break
            current = bytearray()
    return results

# ============================================================
# System definitions
# ============================================================

# Each system: (section_name, opcode_ranges_or_list, class_name_patterns)
SYSTEMS = OrderedDict()

SYSTEMS['CHAT'] = {
    'title': 'Chat System',
    'opcodes': {
        0x026C: 'CHAT_BLOCK',
        0x026D: 'CHAT_HISTORY',
        0x026E: 'CHAT_CONTACT_OPERATION',
        0x026F: 'CHAT_SEND',
        0x0270: 'CHAT_SEND_RETURN',
        0x0271: 'CHAT_RECOMMEND_TRANSLATE',
        0x0272: 'CHAT_TRANSLATE_RETURN',
        0x0273: 'CHAT_ERROR',
        0x0274: 'CHAT_SHARE',
        0x0275: 'CHAT_DEL',
        0x0276: 'CHAT_NEW',
        0x0277: 'CHAT_BOX',
        0x0278: 'CHAT_BUBBLE_BUY',
        0x0279: 'CHAT_BUBBLE_SET',
        0x027A: 'CHAT_BLOCK_TALK',
        0x027B: 'CHAT_BLOCK_RETURN',
        0x027C: 'CHAT_GIFT_SEND',
        0x027D: 'CHAT_GIFT_RECEIVE',
        0x027E: 'CHAT_GIFT_RETURN',
    },
    'class_patterns': ['ChatSend', 'ChatHistory', 'ChatBlock', 'ChatShare',
                       'ChatBubble', 'ChatGift', 'ChatContact', 'ChatDel',
                       'ChatNew', 'ChatBox', 'ChatTranslate'],
    'string_patterns': ['chat_send', 'ChatManager', 'chatmsg', 'chat_block',
                        'chat_history', 'group_chat'],
}

SYSTEMS['GROUP_CHAT'] = {
    'title': 'Group Chat System',
    'opcodes': {
        0x0898: 'GROUP_CHAT_CREATE',
        0x0899: 'GROUP_CHAT_CREATE_RETURN',
        0x089A: 'GROUP_CHAT_DELETE',
        0x089B: 'GROUP_CHAT_DELETE_RETURN',
        0x089C: 'GROUP_CHAT_RENAME',
        0x089D: 'GROUP_CHAT_RENAME_RETURN',
        0x089E: 'GROUP_CHAT_ADD_MEMBER',
        0x089F: 'GROUP_CHAT_ADD_MEMBER_RETURN',
        0x08A0: 'GROUP_CHAT_DEL_MEMBER',
        0x08A1: 'GROUP_CHAT_DEL_MEMBER_RETURN',
        0x08A2: 'GROUP_CHAT_EXIT',
        0x08A3: 'GROUP_CHAT_EXIT_RETURN',
        0x08A4: 'GROUP_CHAT_INFO',
        0x08A5: 'GROUP_CHAT_INFO_RETURN',
        0x08A6: 'GROUP_CHAT_LIST',
        0x08A7: 'GROUP_CHAT_LIST_RETURN',
        0x08A8: 'GROUP_CHAT_SEND',
        0x08A9: 'GROUP_CHAT_SEND_RETURN',
    },
    'class_patterns': ['GroupChat', 'GroupChatCreate', 'GroupChatDelete',
                       'GroupChatRename', 'GroupChatMember', 'GroupChatSend',
                       'GroupChatInfo', 'GroupChatList', 'GroupChatExit'],
    'string_patterns': ['group_chat', 'GroupChatManager'],
}

SYSTEMS['HONOR'] = {
    'title': 'Honor System',
    'opcodes': {
        0x128E: 'HONOR_SYNC',
        0x128F: 'HONOR_SYNC_RETURN',
        0x1290: 'SET_CHAT_HONOR',
    },
    'class_patterns': ['Honor', 'ChatHonor', 'HonorSync', 'SetChatHonor'],
    'string_patterns': ['honor', 'chat_honor'],
}

SYSTEMS['FAVORITES'] = {
    'title': 'Favorites System',
    'opcodes': {
        0x02C6: 'FAVORITE_ADD',
        0x02C7: 'FAVORITE_ADD_RETURN',
        0x02C8: 'FAVORITE_DEL',
        0x02C9: 'FAVORITE_DEL_RETURN',
        0x02CA: 'FAVORITE_LIST',
        0x02CB: 'FAVORITE_LIST_RETURN',
    },
    'class_patterns': ['Favorite', 'FavoriteAdd', 'FavoriteDel', 'FavoriteList'],
    'string_patterns': ['favorite'],
}

SYSTEMS['STATUS'] = {
    'title': 'Status System',
    'opcodes': {
        0x02E4: 'STATUS_SET',
        0x02E5: 'STATUS_SET_RETURN',
        0x02E6: 'STATUS_GET',
    },
    'class_patterns': ['Status', 'StatusSet', 'StatusGet'],
    'string_patterns': ['status_set', 'status_get', 'player_status'],
}

SYSTEMS['FRIEND_GIFT'] = {
    'title': 'Friend Gift System',
    'opcodes': {
        0x186A: 'FRIEND_GIFT_SEND',
        0x186B: 'FRIEND_GIFT_SEND_RETURN',
        0x186C: 'FRIEND_GIFT_RECEIVE',
    },
    'class_patterns': ['FriendGift', 'FriendGiftSend', 'FriendGiftReceive'],
    'string_patterns': ['friend_gift', 'FriendGift'],
}

SYSTEMS['CYCLE_ACTION'] = {
    'title': 'Cycle Action (Recurring Events)',
    'opcodes': {
        0x02F0: 'CYCLE_ACTION_INFO',
        0x02F1: 'CYCLE_ACTION_INFO_RETURN',
        0x02F2: 'CYCLE_ACTION_REWARD',
        0x02F3: 'CYCLE_ACTION_REWARD_RETURN',
        0x02F4: 'CYCLE_ACTION_RANK',
        0x02F5: 'CYCLE_ACTION_RANK_RETURN',
    },
    'class_patterns': ['CycleAction', 'CycleActionInfo', 'CycleActionReward',
                       'CycleActionRank'],
    'string_patterns': ['cycle_action', 'CycleAction'],
}

SYSTEMS['OPERATION_ACTION'] = {
    'title': 'Operation Action (Special Events)',
    'opcodes': {
        0x09BA: 'OPERATION_ACTION_INFO',
        0x09BB: 'OPERATION_ACTION_INFO_RETURN',
        0x09BC: 'OPERATION_ACTION_REWARD',
        0x09BD: 'OPERATION_ACTION_REWARD_RETURN',
        0x09BE: 'OPERATION_ACTION_RANK',
    },
    'class_patterns': ['OperationAction', 'OperationActionInfo',
                       'OperationActionReward'],
    'string_patterns': ['operation_action', 'OperationAction'],
}

SYSTEMS['RUSH_ACTION'] = {
    'title': 'Rush Action Events',
    'opcodes': {
        0x125C: 'RUSH_ACTION_INFO',
        0x125D: 'RUSH_ACTION_INFO_RETURN',
        0x125E: 'RUSH_ACTION_REWARD',
    },
    'class_patterns': ['RushAction', 'RushActionInfo', 'RushActionReward'],
    'string_patterns': ['rush_action', 'RushAction'],
}

SYSTEMS['KINGDOM_ACTION'] = {
    'title': 'Kingdom Action Events',
    'opcodes': {
        0x0B5E: 'KINGDOM_ACTION_INFO',
        0x0B5F: 'KINGDOM_ACTION_INFO_RETURN',
        0x0B60: 'KINGDOM_ACTION_REWARD',
        0x0B61: 'KINGDOM_ACTION_REWARD_RETURN',
        0x0B62: 'KINGDOM_ACTION_RANK',
        0x0B63: 'KINGDOM_ACTION_RANK_RETURN',
        0x0B64: 'KINGDOM_ACTION_EXTRA',
    },
    'class_patterns': ['KingdomAction', 'KingdomActionInfo',
                       'KingdomActionReward', 'KingdomActionRank'],
    'string_patterns': ['kingdom_action', 'KingdomAction'],
}

SYSTEMS['WAR_LORD_ACTION'] = {
    'title': 'War Lord Action Events',
    'opcodes': {
        0x1388: 'WAR_LORD_ACTION_INFO',
        0x1389: 'WAR_LORD_ACTION_INFO_RETURN',
        0x138A: 'WAR_LORD_ACTION_REWARD',
        0x138B: 'WAR_LORD_ACTION_REWARD_RETURN',
        0x138C: 'WAR_LORD_ACTION_RANK',
        0x138D: 'WAR_LORD_ACTION_RANK_RETURN',
        0x138E: 'WAR_LORD_ACTION_EXTRA',
    },
    'class_patterns': ['WarLord', 'WarLordAction', 'WarLordInfo',
                       'WarLordReward', 'WarLordRank'],
    'string_patterns': ['war_lord', 'WarLord'],
}

SYSTEMS['KNIGHT_ACTION'] = {
    'title': 'Knight Action System',
    'opcodes': {
        0x0938: 'KNIGHT_ACTION_INFO',
        0x0939: 'KNIGHT_ACTION_INFO_RETURN',
        0x093A: 'KNIGHT_ACTION_RANK',
        0x093B: 'KNIGHT_ACTION_RANK_RETURN',
        0x093C: 'KNIGHT_ACTION_REWARD',
        0x093D: 'KNIGHT_ACTION_REWARD_RETURN',
        0x093E: 'KNIGHT_ACTION_BUY',
        0x093F: 'KNIGHT_ACTION_BUY_RETURN',
        0x0940: 'KNIGHT_ACTION_TASK_INFO',
        0x0941: 'KNIGHT_ACTION_TASK_INFO_RETURN',
        0x0942: 'KNIGHT_ACTION_TASK_REWARD',
        0x0943: 'KNIGHT_ACTION_TASK_REWARD_RETURN',
    },
    'class_patterns': ['KnightAction', 'KnightInfo', 'KnightReward',
                       'KnightRank', 'KnightBuy', 'KnightTask'],
    'string_patterns': ['knight_action', 'KnightAction'],
}

SYSTEMS['CHAMPIONSHIP'] = {
    'title': 'Championship System',
    'opcodes': {
        0x0A00: 'CHAMPIONSHIP_INFO',
        0x0A01: 'CHAMPIONSHIP_INFO_RETURN',
        0x0A02: 'CHAMPIONSHIP_APPLY',
        0x0A03: 'CHAMPIONSHIP_APPLY_RETURN',
        0x0A04: 'CHAMPIONSHIP_REWARD',
        0x0A05: 'CHAMPIONSHIP_REWARD_RETURN',
        0x0A06: 'CHAMPIONSHIP_RANK',
        0x0A07: 'CHAMPIONSHIP_RANK_RETURN',
        0x0A08: 'CHAMPIONSHIP_MATCH_INFO',
        0x0A09: 'CHAMPIONSHIP_MATCH_INFO_RETURN',
        0x0A0A: 'CHAMPIONSHIP_BET',
        0x0A0B: 'CHAMPIONSHIP_BET_RETURN',
    },
    'class_patterns': ['Championship', 'ChampionshipInfo', 'ChampionshipApply',
                       'ChampionshipReward', 'ChampionshipRank',
                       'ChampionshipMatch', 'ChampionshipBet'],
    'string_patterns': ['championship', 'Championship'],
}

SYSTEMS['KING_CHESS'] = {
    'title': 'King Chess System',
    'opcodes': {op: f'KING_CHESS_{hex(op)}' for op in range(0x0A29, 0x0A4D)},
    'class_patterns': ['KingChess', 'KingChessInfo', 'KingChessMove',
                       'KingChessReward', 'KingChessBuy'],
    'string_patterns': ['king_chess', 'KingChess'],
}

SYSTEMS['CAMEL_SHOP'] = {
    'title': 'Camel Shop',
    'opcodes': {
        0x038E: 'CAMEL_SHOP_INFO',
        0x038F: 'CAMEL_SHOP_INFO_RETURN',
        0x0390: 'CAMEL_SHOP_BUY',
        0x0391: 'CAMEL_SHOP_BUY_RETURN',
        0x0392: 'CAMEL_SHOP_REFRESH',
    },
    'class_patterns': ['CamelShop', 'CamelShopBuy', 'CamelShopInfo',
                       'CamelShopRefresh'],
    'string_patterns': ['camel_shop', 'CamelShop'],
}

SYSTEMS['LUCKY_TURNTABLE'] = {
    'title': 'Lucky Turntable (Spin)',
    'opcodes': {
        0x039B: 'LUCKY_TURNTABLE_INFO',
        0x039C: 'LUCKY_TURNTABLE_INFO_RETURN',
        0x039D: 'LUCKY_TURNTABLE_PLAY',
        0x039E: 'LUCKY_TURNTABLE_PLAY_RETURN',
        0x039F: 'LUCKY_TURNTABLE_REWARD',
        0x03A0: 'LUCKY_TURNTABLE_REWARD_RETURN',
        0x03A1: 'LUCKY_TURNTABLE_RANK',
    },
    'class_patterns': ['LuckyTurntable', 'TurntableInfo', 'TurntablePlay',
                       'TurntableReward', 'TurntableRank'],
    'string_patterns': ['lucky_turntable', 'turntable', 'LuckyTurntable'],
}

SYSTEMS['ROYAL_SHOP'] = {
    'title': 'Royal Shop',
    'opcodes': {
        0x0794: 'ROYAL_SHOP_INFO',
        0x0795: 'ROYAL_SHOP_INFO_RETURN',
        0x0796: 'ROYAL_SHOP_BUY',
        0x0797: 'ROYAL_SHOP_BUY_RETURN',
        0x0798: 'ROYAL_SHOP_REFRESH',
        0x0799: 'ROYAL_SHOP_REFRESH_RETURN',
    },
    'class_patterns': ['RoyalShop', 'RoyalShopBuy', 'RoyalShopInfo',
                       'RoyalShopRefresh'],
    'string_patterns': ['royal_shop', 'RoyalShop'],
}

SYSTEMS['LUCKY_SHOP'] = {
    'title': 'Lucky Shop (Scratch Cards)',
    'opcodes': {
        0x09A6: 'LUCKY_SHOP_INFO',
        0x09A7: 'LUCKY_SHOP_INFO_RETURN',
        0x09A8: 'LUCKY_SHOP_SCRATCH',
    },
    'class_patterns': ['LuckyShop', 'LuckyShopInfo', 'LuckyShopScratch',
                       'ScratchCard'],
    'string_patterns': ['lucky_shop', 'scratch_card', 'LuckyShop'],
}

SYSTEMS['REWARD_POINT_SHOP'] = {
    'title': 'Reward Point Shop',
    'opcodes': {
        0x0AF0: 'REWARD_POINT_SHOP_INFO',
        0x0AF1: 'REWARD_POINT_SHOP_INFO_RETURN',
        0x0AF2: 'REWARD_POINT_SHOP_BUY',
        0x0AF3: 'REWARD_POINT_SHOP_BUY_RETURN',
    },
    'class_patterns': ['RewardPointShop', 'RewardPointBuy', 'RewardPointInfo'],
    'string_patterns': ['reward_point_shop', 'RewardPoint'],
}

SYSTEMS['LUCKY_LINE'] = {
    'title': 'Lucky Line (Slot Machine)',
    'opcodes': {
        0x0B54: 'LUCKY_LINE_INFO',
        0x0B55: 'LUCKY_LINE_INFO_RETURN',
        0x0B56: 'LUCKY_LINE_PLAY',
        0x0B57: 'LUCKY_LINE_PLAY_RETURN',
        0x0B58: 'LUCKY_LINE_REWARD',
    },
    'class_patterns': ['LuckyLine', 'LuckyLineInfo', 'LuckyLinePlay',
                       'LuckyLineReward'],
    'string_patterns': ['lucky_line', 'LuckyLine'],
}

SYSTEMS['WHEEL'] = {
    'title': 'Wheel System',
    'opcodes': {
        0x0E74: 'WHEEL_INFO',
        0x0E75: 'WHEEL_INFO_RETURN',
        0x0E76: 'WHEEL_PLAY',
        0x0E77: 'WHEEL_PLAY_RETURN',
        0x0E78: 'WHEEL_REWARD',
    },
    'class_patterns': ['Wheel', 'WheelInfo', 'WheelPlay', 'WheelReward'],
    'string_patterns': ['wheel_info', 'wheel_play', 'Wheel'],
}

SYSTEMS['DOUBLE_LOTTERY'] = {
    'title': 'Double Lottery',
    'opcodes': {
        0x1D4C: 'DOUBLE_LOTTERY_INFO',
        0x1D4D: 'DOUBLE_LOTTERY_INFO_RETURN',
        0x1D4E: 'DOUBLE_LOTTERY_PLAY',
        0x1D4F: 'DOUBLE_LOTTERY_PLAY_RETURN',
        0x1D50: 'DOUBLE_LOTTERY_REWARD',
        0x1D51: 'DOUBLE_LOTTERY_REWARD_RETURN',
        0x1D52: 'DOUBLE_LOTTERY_RANK',
    },
    'class_patterns': ['DoubleLottery', 'DoubleLotteryInfo', 'DoubleLotteryPlay',
                       'DoubleLotteryReward'],
    'string_patterns': ['double_lottery', 'DoubleLottery'],
}

SYSTEMS['EVERYDAY_GIFTPACK'] = {
    'title': 'Everyday Gift Pack',
    'opcodes': {
        0x0311: 'EVERYDAY_GIFTPACK_INFO',
        0x0312: 'EVERYDAY_GIFTPACK_REWARD',
        0x0313: 'EVERYDAY_GIFTPACK_REWARD_RETURN',
    },
    'class_patterns': ['EveryDayGiftpack', 'EverydayGift', 'EveryDayGift'],
    'string_patterns': ['everyday_gift', 'EveryDayGift', 'every_day_giftpack'],
}

SYSTEMS['EVERYDAY_GIFTPACK_NEW'] = {
    'title': 'Everyday Gift Pack (New)',
    'opcodes': {
        0x189C: 'EVERYDAY_GIFTPACK_NEW_INFO',
        0x189D: 'EVERYDAY_GIFTPACK_NEW_INFO_RETURN',
        0x189E: 'EVERYDAY_GIFTPACK_NEW_REWARD',
    },
    'class_patterns': ['EveryDayGiftpackNew', 'EverydayGiftNew'],
    'string_patterns': ['everyday_giftpack_new', 'EveryDayGiftpackNew'],
}

SYSTEMS['ACTIVEGIFTS'] = {
    'title': 'Active Gifts System',
    'opcodes': {
        0x12F2: 'ACTIVEGIFTS_INFO',
        0x12F3: 'ACTIVEGIFTS_INFO_RETURN',
        0x12F4: 'ACTIVEGIFTS_ACTION',
        0x12F5: 'ACTIVEGIFTS_ACTION_RETURN',
        0x12F6: 'ACTIVEGIFTS_REWARD',
        0x12F7: 'ACTIVEGIFTS_REWARD_RETURN',
        0x12F8: 'ACTIVEGIFTS_RANK',
        0x12F9: 'ACTIVEGIFTS_RANK_RETURN',
        0x12FA: 'ACTIVEGIFTS_BUY',
        0x12FB: 'ACTIVEGIFTS_BUY_RETURN',
    },
    'class_patterns': ['ActiveGifts', 'ActiveGiftsInfo', 'ActiveGiftsAction',
                       'ActiveGiftsReward', 'ActiveGiftsRank', 'ActiveGiftsBuy'],
    'string_patterns': ['active_gifts', 'ActiveGifts', 'activegifts'],
}

SYSTEMS['CUSTOMGIFTS'] = {
    'title': 'Custom Gifts System',
    'opcodes': {
        0x1356: 'CUSTOMGIFTS_INFO',
        0x1357: 'CUSTOMGIFTS_INFO_RETURN',
        0x1358: 'CUSTOMGIFTS_ACTION',
        0x1359: 'CUSTOMGIFTS_ACTION_RETURN',
        0x135A: 'CUSTOMGIFTS_REWARD',
        0x135B: 'CUSTOMGIFTS_REWARD_RETURN',
    },
    'class_patterns': ['CustomGifts', 'CustomGiftsInfo', 'CustomGiftsAction',
                       'CustomGiftsReward'],
    'string_patterns': ['custom_gifts', 'CustomGifts', 'customgifts'],
}

SYSTEMS['EXTRA_GIFTPACK_NEW'] = {
    'title': 'Extra Gift Pack (New)',
    'opcodes': {
        0x16AF: 'EXTRA_GIFTPACK_NEW_INFO',
        0x16B0: 'EXTRA_GIFTPACK_NEW_INFO_RETURN',
        0x16B1: 'EXTRA_GIFTPACK_NEW_ACTION',
        0x16B2: 'EXTRA_GIFTPACK_NEW_ACTION_RETURN',
        0x16B3: 'EXTRA_GIFTPACK_NEW_REWARD',
        0x16B4: 'EXTRA_GIFTPACK_NEW_REWARD_RETURN',
        0x16B5: 'EXTRA_GIFTPACK_NEW_RANK',
    },
    'class_patterns': ['ExtraGiftpackNew', 'ExtraGiftNew'],
    'string_patterns': ['extra_giftpack', 'ExtraGiftpack'],
}

SYSTEMS['RETURN_EVENT'] = {
    'title': 'Return Event System',
    'opcodes': {
        0x16C6: 'RETURN_EVENT_INFO',
        0x16C7: 'RETURN_EVENT_INFO_RETURN',
        0x16C8: 'RETURN_EVENT_REWARD',
        0x16C9: 'RETURN_EVENT_REWARD_RETURN',
        0x16CA: 'RETURN_EVENT_TASK_INFO',
        0x16CB: 'RETURN_EVENT_TASK_INFO_RETURN',
        0x16CC: 'RETURN_EVENT_TASK_REWARD',
        0x16CD: 'RETURN_EVENT_TASK_REWARD_RETURN',
        0x16CE: 'RETURN_EVENT_SIGN',
        0x16CF: 'RETURN_EVENT_SIGN_RETURN',
    },
    'class_patterns': ['ReturnEvent', 'ReturnEventInfo', 'ReturnEventReward',
                       'ReturnEventTask', 'ReturnEventSign'],
    'string_patterns': ['return_event', 'ReturnEvent'],
}

SYSTEMS['RECHARGEBONUS'] = {
    'title': 'Recharge Bonus System',
    'opcodes': {
        0x1770: 'RECHARGEBONUS_INFO',
        0x1771: 'RECHARGEBONUS_INFO_RETURN',
        0x1772: 'RECHARGEBONUS_REWARD',
        0x1773: 'RECHARGEBONUS_REWARD_RETURN',
        0x1774: 'RECHARGEBONUS_BUY',
        0x1775: 'RECHARGEBONUS_BUY_RETURN',
    },
    'class_patterns': ['RechargeBonus', 'RechargeBonusInfo',
                       'RechargeBonusReward', 'RechargeBonusBuy'],
    'string_patterns': ['recharge_bonus', 'RechargeBonus'],
}

SYSTEMS['CONTINUITY_GIFTPACK'] = {
    'title': 'Continuity Gift Pack',
    'opcodes': {
        0x1838: 'CONTINUITY_GIFTPACK_INFO',
        0x1839: 'CONTINUITY_GIFTPACK_INFO_RETURN',
        0x183A: 'CONTINUITY_GIFTPACK_ACTION',
        0x183B: 'CONTINUITY_GIFTPACK_ACTION_RETURN',
        0x183C: 'CONTINUITY_GIFTPACK_REWARD',
        0x183D: 'CONTINUITY_GIFTPACK_REWARD_RETURN',
        0x183E: 'CONTINUITY_GIFTPACK_BUY',
        0x183F: 'CONTINUITY_GIFTPACK_BUY_RETURN',
        0x1840: 'CONTINUITY_GIFTPACK_RANK',
        0x1841: 'CONTINUITY_GIFTPACK_RANK_RETURN',
    },
    'class_patterns': ['ContinuityGiftpack', 'ContinuityGift'],
    'string_patterns': ['continuity_gift', 'ContinuityGift'],
}

SYSTEMS['KINGDOM_GIFT'] = {
    'title': 'Kingdom Gift System',
    'opcodes': {op: f'KINGDOM_GIFT_{hex(op)}' for op in range(0x18CE, 0x18DA)},
    'class_patterns': ['KingdomGift', 'KingdomGiftInfo', 'KingdomGiftReward',
                       'KingdomGiftAction'],
    'string_patterns': ['kingdom_gift', 'KingdomGift'],
}

SYSTEMS['NEWSERVER'] = {
    'title': 'New Server Events',
    'opcodes': {op: f'NEWSERVER_{hex(op)}' for op in range(0x1996, 0x19A4)},
    'class_patterns': ['NewServer', 'NewServerInfo', 'NewServerReward',
                       'NewServerAction', 'NewServerTask'],
    'string_patterns': ['new_server', 'NewServer', 'newserver'],
}

SYSTEMS['CONTINUOUS_TASK'] = {
    'title': 'Continuous Task System',
    'opcodes': {
        0x1DE2: 'CONTINUOUS_TASK_INFO',
        0x1DE3: 'CONTINUOUS_TASK_INFO_RETURN',
        0x1DE4: 'CONTINUOUS_TASK_REWARD',
        0x1DE5: 'CONTINUOUS_TASK_REWARD_RETURN',
        0x1DE6: 'CONTINUOUS_TASK_ACTION',
        0x1DE7: 'CONTINUOUS_TASK_ACTION_RETURN',
    },
    'class_patterns': ['ContinuousTask', 'ContinuousTaskInfo',
                       'ContinuousTaskReward'],
    'string_patterns': ['continuous_task', 'ContinuousTask'],
}

SYSTEMS['ALLFORONE'] = {
    'title': 'All For One System',
    'opcodes': {
        0x1E14: 'ALLFORONE_INFO',
        0x1E15: 'ALLFORONE_INFO_RETURN',
        0x1E16: 'ALLFORONE_ACTION',
        0x1E17: 'ALLFORONE_ACTION_RETURN',
        0x1E18: 'ALLFORONE_REWARD',
    },
    'class_patterns': ['AllForOne', 'AllForOneInfo', 'AllForOneAction',
                       'AllForOneReward'],
    'string_patterns': ['all_for_one', 'AllForOne', 'allforone'],
}

SYSTEMS['MINI_GAME'] = {
    'title': 'Mini Game System',
    'opcodes': {
        0x19C8: 'MINI_GAME_INFO',
        0x19C9: 'MINI_GAME_INFO_RETURN',
        0x19CA: 'MINI_GAME_START',
        0x19CB: 'MINI_GAME_START_RETURN',
        0x19CC: 'MINI_GAME_ACTION',
        0x19CD: 'MINI_GAME_ACTION_RETURN',
        0x19CE: 'MINI_GAME_RESULT',
        0x19CF: 'MINI_GAME_RESULT_RETURN',
        0x19D0: 'MINI_GAME_REWARD',
    },
    'class_patterns': ['MiniGame', 'MiniGameInfo', 'MiniGameStart',
                       'MiniGameAction', 'MiniGameResult', 'MiniGameReward'],
    'string_patterns': ['mini_game', 'MiniGame', 'minigame'],
}

SYSTEMS['CAMEL'] = {
    'title': 'Camel (Drive Camel Mini-game)',
    'opcodes': {
        0x09B0: 'CAMEL_INFO',
        0x09B1: 'CAMEL_INFO_RETURN',
        0x09B2: 'CAMEL_DRIVE',
        0x09B3: 'CAMEL_DRIVE_RETURN',
    },
    'class_patterns': ['Camel', 'CamelDrive', 'CamelInfo', 'DriveCamel'],
    'string_patterns': ['drive_camel', 'DriveCamel', 'camel_drive'],
}

SYSTEMS['MOBILIZATION'] = {
    'title': 'Mobilization System',
    'opcodes': {op: f'MOBILIZATION_{hex(op)}' for op in range(0x07B2, 0x07CB)},
    'class_patterns': ['Mobilization', 'MobilizationInfo', 'MobilizationReward',
                       'MobilizationTask', 'MobilizationRank', 'MobilizationBuy'],
    'string_patterns': ['mobilization', 'Mobilization'],
}

SYSTEMS['SERVER_MISSION'] = {
    'title': 'Server Mission System',
    'opcodes': {
        0x13BA: 'SERVER_MISSION_INFO',
        0x13BB: 'SERVER_MISSION_INFO_RETURN',
        0x13BC: 'SERVER_MISSION_REWARD',
        0x13BD: 'SERVER_MISSION_REWARD_RETURN',
        0x13BE: 'SERVER_MISSION_RANK',
        0x13BF: 'SERVER_MISSION_RANK_RETURN',
        0x13C0: 'SERVER_MISSION_EXTRA',
    },
    'class_patterns': ['ServerMission', 'ServerMissionInfo',
                       'ServerMissionReward', 'ServerMissionRank'],
    'string_patterns': ['server_mission', 'ServerMission'],
}


# ============================================================
# Analysis engine
# ============================================================
def analyze_system(sys_key, sys_def):
    """Analyze one system completely."""
    p(f"\n## {sys_def['title']}")
    p("")

    opcodes = sys_def['opcodes']
    class_patterns = sys_def['class_patterns']

    # 1) Opcode->CMSG name mapping from known database
    p(f"### Opcodes ({len(opcodes)} defined)")
    p("")
    p("| Opcode | Expected Name | CMSG_OPCODES Name | Has packData | Has getData |")
    p("|--------|--------------|-------------------|-------------|------------|")

    request_opcodes = []
    return_opcodes = []
    fire_and_forget = []

    for opcode, expected_name in sorted(opcodes.items()):
        known_name = CMSG_OPCODES.get(opcode, '-')
        if known_name != '-':
            known_name = known_name.replace('CMSG_', '')

        # Check if this is a request or return
        is_return = 'RETURN' in expected_name

        # Try to find symbols
        has_pack = '-'
        has_get = '-'

        # Search for class by expected name patterns
        for pat in class_patterns:
            pd = find_packdata(pat)
            gd = find_getdata(pat)
            if pd:
                has_pack = 'YES'
            if gd:
                has_get = 'YES'

        # Also check known CMSG name
        if known_name != '-':
            # Try shorter form
            short = known_name.replace('_REQUEST', '').replace('_RETURN', '')
            pd2 = find_packdata(short)
            gd2 = find_getdata(short)
            if pd2:
                has_pack = 'YES'
            if gd2:
                has_get = 'YES'

        if is_return:
            return_opcodes.append(opcode)
        else:
            request_opcodes.append(opcode)
            # Check if there's a corresponding RETURN
            if (opcode + 1) not in opcodes or 'RETURN' not in opcodes.get(opcode + 1, ''):
                fire_and_forget.append((opcode, expected_name))

        p(f"| 0x{opcode:04X} | {expected_name} | {known_name} | {has_pack} | {has_get} |")

    p("")

    # 2) Symbol search for constructors and methods
    p("### Binary Symbols Found")
    p("")
    all_found = []
    for pat in class_patterns:
        syms = find_symbols(pat)
        for name, addr, size in syms:
            all_found.append((name, addr, size))

    if all_found:
        # Deduplicate and categorize
        constructors = []
        pack_funcs = []
        get_funcs = []
        other_funcs = []

        seen = set()
        for name, addr, size in all_found:
            if name in seen:
                continue
            seen.add(name)
            if '8packData' in name:
                pack_funcs.append((name, addr, size))
            elif '7getData' in name:
                get_funcs.append((name, addr, size))
            elif 'C1Ev' in name or 'C2Ev' in name:
                constructors.append((name, addr, size))
            else:
                other_funcs.append((name, addr, size))

        if constructors:
            p(f"**Constructors** ({len(constructors)}):")
            for name, addr, size in constructors[:15]:
                # Try extracting opcode
                opc = extract_opcode_from_constructor(addr, size)
                opc_str = f" -> opcode=0x{opc:04X}" if opc else ""
                # Demangle roughly
                short = name.split('CMSG_')[-1].split('C1Ev')[0].split('C2Ev')[0] if 'CMSG_' in name else name[:80]
                p(f"- `{short}` @ 0x{addr:08X} (size={size}){opc_str}")
            if len(constructors) > 15:
                p(f"- ... and {len(constructors) - 15} more")
            p("")

        if pack_funcs:
            p(f"**packData functions** ({len(pack_funcs)}):")
            for name, addr, size in pack_funcs[:10]:
                fields = analyze_packdata(addr, size)
                short = name.split('CMSG_')[-1].split('8packData')[0] if 'CMSG_' in name else name[:80]
                if fields:
                    field_str = " | ".join(f"u{f['size']*8}@off={f['struct_offset']}" for f in fields)
                    total = sum(f['size'] for f in fields)
                    p(f"- `{short}` @ 0x{addr:08X}: [{field_str}] = {total}B total")
                else:
                    p(f"- `{short}` @ 0x{addr:08X}: (empty or unresolved)")
            if len(pack_funcs) > 10:
                p(f"- ... and {len(pack_funcs) - 10} more")
            p("")

        if get_funcs:
            p(f"**getData functions** ({len(get_funcs)}):")
            for name, addr, size in get_funcs[:10]:
                fields = analyze_getdata(addr, size)
                short = name.split('CMSG_')[-1].split('7getData')[0] if 'CMSG_' in name else name[:80]
                if fields:
                    field_str = " | ".join(f"u{f['size']*8}" for f in fields)
                    total = sum(f['size'] for f in fields)
                    p(f"- `{short}` @ 0x{addr:08X}: [{field_str}] = {total}B response")
                else:
                    p(f"- `{short}` @ 0x{addr:08X}: (complex/unresolved)")
            if len(get_funcs) > 10:
                p(f"- ... and {len(get_funcs) - 10} more")
            p("")

        if other_funcs:
            p(f"**Other methods** ({len(other_funcs)}):")
            for name, addr, size in other_funcs[:8]:
                short = name[:100]
                p(f"- `{short}` @ 0x{addr:08X}")
            if len(other_funcs) > 8:
                p(f"- ... and {len(other_funcs) - 8} more")
            p("")
    else:
        p("No symbols found for class patterns.")
        p("")

    # 3) Fire-and-forget analysis
    if fire_and_forget:
        p("### Fire-and-Forget Opcodes (No RETURN pair)")
        p("")
        for opc, name in fire_and_forget:
            p(f"- 0x{opc:04X} {name} -- potential free action / no server response needed")
        p("")

    # 4) Summary stats
    p(f"### Summary")
    p(f"- Request opcodes: {len(request_opcodes)}")
    p(f"- Return opcodes: {len(return_opcodes)}")
    p(f"- Fire-and-forget: {len(fire_and_forget)}")
    p(f"- Symbols found: {len(all_found)}")
    p("")

    return {
        'request_count': len(request_opcodes),
        'return_count': len(return_opcodes),
        'fire_and_forget': fire_and_forget,
        'symbols_found': len(all_found),
    }


# ============================================================
# Main execution
# ============================================================
p("# Chat, Social, Events & Mini-Games Analysis")
p("=" * 60)
p("")
p("Generated by 52_chat_social_events_analysis.py")
p(f"Binary: libgame.so ({len(data):,} bytes)")
p(f"Known CMSG opcodes: {len(CMSG_OPCODES)}")
p(f"Capstone available: {HAS_CAPSTONE}")
p("")

all_stats = {}

# ============================================================
# Analyze all systems
# ============================================================
for sys_key, sys_def in SYSTEMS.items():
    print(f"\n[*] Analyzing {sys_key}...")
    stats = analyze_system(sys_key, sys_def)
    all_stats[sys_key] = stats

# ============================================================
# String search for reward/free patterns
# ============================================================
p("\n## Reward & Free Resource String Search")
p("=" * 60)
p("")

print("[*] Searching for reward/free strings (this may take a moment)...")
reward_strings = find_strings([
    'free_reward', 'daily_reward', 'login_reward', 'online_reward',
    'collect_reward', 'claim_reward', 'auto_reward',
    'free_spin', 'free_draw', 'free_play', 'free_turn',
    'free_buy', 'free_chest', 'free_gift',
    'bonus_reward', 'first_reward', 'vip_reward',
    'sign_reward', 'check_in', 'checkin',
    'scratch_free', 'lottery_free',
    'recharge_reward', 'pay_reward',
], limit=20)

for pattern, hits in sorted(reward_strings.items()):
    if hits:
        p(f"### String pattern: `{pattern}`")
        for off, s in hits[:10]:
            p(f"- 0x{off:08X}: `{s[:120]}`")
        if len(hits) > 10:
            p(f"- ... and {len(hits) - 10} more")
        p("")

# ============================================================
# Additional: search for manager classes
# ============================================================
p("\n## Manager Classes Related to These Systems")
p("=" * 60)
p("")

print("[*] Searching for manager class symbols...")
manager_patterns = [
    'ChatManager', 'GroupChatManager', 'FavoriteManager',
    'ActionManager', 'EventManager', 'ActivityManager',
    'ShopManager', 'LotteryManager', 'GiftManager',
    'MobilizationManager', 'MissionManager', 'MiniGameManager',
    'ChampionshipManager', 'KnightManager', 'CamelManager',
    'WheelManager', 'RechargeManager', 'ReturnManager',
    'KingChessManager', 'HonorManager',
]

for mgr in manager_patterns:
    syms = find_symbols(mgr)
    if syms:
        p(f"### {mgr}")
        for name, addr, size in syms[:5]:
            short = name[:120]
            p(f"- `{short}` @ 0x{addr:08X} (size={size})")
        if len(syms) > 5:
            p(f"- ... and {len(syms) - 5} more")
        p("")

# ============================================================
# Bot Automation Opportunities
# ============================================================
p("\n## Bot Automation Opportunities")
p("=" * 60)
p("")

p("### Free Reward Collection (Fire-and-Forget)")
p("")
p("These opcodes have NO return pair, meaning the server processes them without")
p("requiring acknowledgement - ideal for automated collection:")
p("")

all_ff = []
for sys_key, stats in all_stats.items():
    for opc, name in stats.get('fire_and_forget', []):
        all_ff.append((opc, name, sys_key))

if all_ff:
    p("| Opcode | Name | System |")
    p("|--------|------|--------|")
    for opc, name, sys_key in sorted(all_ff):
        p(f"| 0x{opc:04X} | {name} | {sys_key} |")
    p("")
else:
    p("No fire-and-forget opcodes found across systems.")
    p("")

p("### Auto-Collect Strategy")
p("")
p("1. **Daily Gift Packs**: Send EVERYDAY_GIFTPACK_REWARD (0x0312) daily")
p("2. **Cycle Action Rewards**: Query CYCLE_ACTION_INFO, then collect CYCLE_ACTION_REWARD")
p("3. **Active Gifts**: Query info, then send ACTIVEGIFTS_REWARD for each completed tier")
p("4. **Lucky Shop**: Send LUCKY_SHOP_SCRATCH if free attempts available")
p("5. **Wheel Spins**: WHEEL_PLAY if free spin available, then WHEEL_REWARD")
p("6. **Double Lottery**: DOUBLE_LOTTERY_PLAY for free draws")
p("7. **Return Event**: RETURN_EVENT_SIGN for daily sign-in if applicable")
p("8. **Server Mission**: SERVER_MISSION_REWARD for completed milestones")
p("9. **Mobilization**: MOBILIZATION_GET_REWARD for task completion")
p("10. **Continuous Task**: CONTINUOUS_TASK_REWARD for streaks")
p("")

p("### Auto-Chat Strategy")
p("")
p("1. **Send chat**: CHAT_SEND (0x026F) with channel + message")
p("2. **Group chat**: GROUP_CHAT_SEND (0x08A8) to specific group")
p("3. **Chat history**: CHAT_HISTORY (0x026D) to read messages")
p("4. **Alliance help**: Can be automated via DAMAGE_HELP (0x1ACD)")
p("")

p("### Mini-Game Automation")
p("")
p("1. **Camel**: CAMEL_DRIVE (0x09B2) - automated path choices")
p("2. **Mini Game**: MINI_GAME_START -> MINI_GAME_ACTION -> MINI_GAME_RESULT flow")
p("3. **King Chess**: Board game with move-based interactions")
p("")

# ============================================================
# Vulnerabilities
# ============================================================
p("\n## Potential Vulnerabilities & Exploits")
p("=" * 60)
p("")

p("### Shop Exploits")
p("")
p("1. **Camel Shop Refresh** (0x0392): No RETURN pair - could refresh without cost check")
p("2. **Lucky Shop Scratch** (0x09A8): Fire-and-forget - may allow rapid scratching")
p("3. **Royal Shop Refresh** (0x0798): Forced refresh could cycle inventory")
p("4. **Reward Point Shop**: Buy items with points - check if points deducted server-side only")
p("")

p("### Reward Duplication Risks")
p("")
p("1. **Fire-and-forget rewards**: No return = no client confirmation needed")
p("   - Send reward opcode multiple times rapidly")
p("   - Server may not have rate limiting on all endpoints")
p("2. **Event reward timing**: Query info, collect reward, re-query")
p("   - Race condition between info sync and reward collection")
p("3. **Batch rewards**: Some systems have individual + batch reward opcodes")
p("   - Collecting both may yield double rewards")
p("")

p("### Chat Exploits")
p("")
p("1. **Chat Gift** (0x027C-0x027E): Gift sending via chat - check cost validation")
p("2. **Chat Bubble Buy** (0x0278): Purchase without gems check?")
p("3. **Chat Block/Unblock**: Rapid block/unblock for notification spam")
p("4. **Group Chat**: Create unlimited groups, add members without consent")
p("")

p("### Event Manipulation")
p("")
p("1. **Cycle/Operation/Rush Action**: All follow INFO->REWARD pattern")
p("   - Reward without meeting requirements if server doesn't validate")
p("2. **Kingdom Action Extra** (0x0B64): Extra opcode with no RETURN")
p("3. **War Lord Extra** (0x138E): Same pattern - extra action without response")
p("4. **Mobilization** (0x07B2-0x07CA): Large system - 25 opcodes")
p("   - Multiple reward endpoints to test")
p("   - Task completion may not be validated")
p("")

# ============================================================
# Grand Summary
# ============================================================
p("\n## Grand Summary")
p("=" * 60)
p("")

total_opcodes = sum(len(s['opcodes']) for s in SYSTEMS.values())
total_ff = len(all_ff)
total_syms = sum(s.get('symbols_found', 0) for s in all_stats.values())

p(f"- **Total systems analyzed**: {len(SYSTEMS)}")
p(f"- **Total opcodes covered**: {total_opcodes}")
p(f"- **Fire-and-forget opcodes**: {total_ff}")
p(f"- **Total binary symbols found**: {total_syms}")
p("")

p("### Systems by Size (opcode count)")
p("")
for sys_key, sys_def in sorted(SYSTEMS.items(), key=lambda x: len(x[1]['opcodes']), reverse=True):
    p(f"- {sys_def['title']}: {len(sys_def['opcodes'])} opcodes")
p("")

p("### Priority for Bot Implementation")
p("")
p("**HIGH** (free resources, daily automation):")
p("- Everyday Gift Pack, Active Gifts, Cycle Action, Server Mission")
p("- Online rewards, sign-in rewards, accumulation rewards")
p("")
p("**MEDIUM** (periodic events):")
p("- Lucky Turntable/Wheel/Double Lottery (free spins)")
p("- Mobilization tasks and rewards")
p("- Return Event (if player qualifies)")
p("")
p("**LOW** (complex/situational):")
p("- Championship, King Chess (require active participation)")
p("- Knight Action, War Lord Action (kingdom-wide)")
p("- Mini Games (need game logic implementation)")
p("")

# ============================================================
# Write output
# ============================================================
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out_lines))

print(f"\n[*] Analysis complete!")
print(f"[*] Output written to: {OUTPUT}")
print(f"[*] Total systems: {len(SYSTEMS)}")
print(f"[*] Total opcodes: {total_opcodes}")
print(f"[*] Fire-and-forget: {total_ff}")
print(f"[*] Symbols found: {total_syms}")

#!/usr/bin/env python3
"""
11_categorize_features.py
Categorize all CMSG protocol messages from FINDINGS.md into game systems.

Reads FINDINGS.md, extracts every CMSG_ name from the four sections
(C2S, S2C, SYNC, Other), categorizes by keyword patterns, and writes
a comprehensive report to findings/game_systems.md.
"""

import re
import os
from collections import defaultdict, OrderedDict

# ── Paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FINDINGS_PATH = os.path.join(SCRIPT_DIR, "FINDINGS.md")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "findings")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "game_systems.md")

# ── Direction classification ───────────────────────────────────────────
def classify_direction(name: str, section: str) -> str:
    """Classify a CMSG name as C2S, S2C, or SYNC based on suffix and section."""
    upper = name.upper()
    # Explicit SYNC
    if "SYNC" in upper or upper.endswith("_LOGIN_INFO"):
        return "SYNC"
    # C2S indicators
    if upper.endswith("_REQUEST") or upper.endswith("_SEND"):
        return "C2S"
    # S2C indicators
    if (upper.endswith("_RETURN") or upper.endswith("_RETURNE") or
        upper.endswith("_RECV") or upper.endswith("_NOTIFY") or
        upper.endswith("_NOTICE") or upper.endswith("_PUSH") or
        upper.endswith("_RESULT") or upper.endswith("_UPDATE") or
        upper.endswith("_BROADCAST")):
        return "S2C"
    # _INFO at end is usually S2C but not LOGIN_INFO (already handled)
    if upper.endswith("_INFO"):
        return "S2C"
    # Fall back to section header
    if section == "C2S":
        return "C2S"
    elif section == "S2C":
        return "S2C"
    elif section == "SYNC":
        return "SYNC"
    # "Other" section: try harder
    if "_RETURNE" in upper or "_RETURN" in upper:
        return "S2C"
    if "_REQUEST" in upper:
        return "C2S"
    return "OTHER"


# ── Category definitions (order matters: first match wins) ─────────────
# Patterns are matched against the FULL CMSG name (case-insensitive).
# More specific categories come before broader ones.
CATEGORIES = OrderedDict([

    # ── Auth / Session ──
    ("Auth/Login", [
        r"_LOGIN", r"_ENTER_GAME", r"_LOGOUT", r"_TOKEN",
        r"_SESSION", r"_ACCOUNT", r"_AUTH",
        r"_RECONNECT", r"_REGISTER", r"_BIND_",
        r"_PASSWORD", r"_VERIFY_CODE",
        r"_CHANGE_SERVER(?!_NAME)", r"_KICKOUT", r"_KICK_OUT",
        r"_CLIENT_OFFLINE", r"_KEEP_?LIVE",
    ]),

    # ── System / Core ──
    ("System/Core", [
        r"_HEARTBEAT", r"_PING", r"_CONFIG",
        r"_SERVER_TIME", r"_DAY_REFRESH", r"_SYSTEM",
        r"_VERSION", r"_COMPLETE_GUIDE", r"_GUIDE_",
        r"_SYNC_TIME", r"_CLIENT_INFO", r"_DEVICE",
        r"_DOWN_?LOAD_REWARD", r"_PUSH_SETTING",
        r"_CHANGE_PUSH", r"_CHANGE_LANGUAGE", r"_SETTING",
        r"_ANTI_CHEAT", r"_REPORT_BUG", r"_ERROR",
        r"_PATCH", r"_HOT_FIX", r"_MAINTENANCE",
        r"_SYNC_FORCE", r"_SYNC_ALL",
        r"_SYNC_NEW_USER", r"_SYNC_MARBLES",
        r"_CLIENT_LOG", r"_CLIENT_TRIGGER",
        r"_SERVER_MAINTAIN", r"_TIME_REFRESH",
        r"_ENABLE_VIEW", r"_PRELOAD_AD", r"_LOAD_AD",
        r"_WATCH_AD", r"_WEB_PLACARD",
        r"_NEWS_INFO", r"_MONTH_REFRESH",
        r"_SYNC_DAILY", r"_SYNC_FIXED",
        r"_SYNC_TRIGGER", r"_ADD_TRIGGER",
        r"_PM_COMMAND", r"_PM_EFFECT",
        r"_FIXED_TIME",
    ]),

    # ── War Events (large-scale PvP modes) - BEFORE Combat ──
    ("War Events", [
        r"_KINGDOM_WAR", r"_WORLD_BATTLE", r"_WORLD_WAR",
        r"_LEAGUE_BATTLE", r"_CLANPK",
        r"_LOSTLAND", r"_LOST_LAND", r"_LOST_ERA",
        r"_BATTLEFIELD",
        r"_GUILD_STANDOFF",
        r"_GIANT_INVASION",
        r"_LEGION_BATTLE", r"_LEGION_FINAL",
        r"_SYNC_WAR", r"_SYNC_BATTLE",
        r"_WAR_LORD", r"_QUERY_WAR",
    ]),

    # ── Secret / Exploration Mode ──
    ("Secret/Exploration", [
        r"_SECRET_TASK", r"_SECRET_BATTLE",
        r"_SECRET_OPEN", r"_SECRET_MOVE",
        r"_SECRET_UPDATE", r"_SECRET_MINING",
        r"_SECRET_ADD", r"_SECRET_SURPRISE",
        r"_SECRET_GOLD", r"_SECRET_NORMAL",
        r"_SECRET_SP", r"_SYS_SECRET",
        r"_SYNC_SECRET",
    ]),

    # ── Desert Trade - BEFORE March/Combat ──
    ("Desert Trade", [
        r"_DESERT_TRADE", r"_DESSERT_ACTION",
    ]),

    # ── March / Movement ──
    ("March/Movement", [
        r"_MARCH", r"_TRADE_MARCH",
        r"_SCOUT(?!_HERO)", r"_RALLY", r"_REINFORCE",
        r"_GARRISON", r"_RECALL", r"_SPEEDUP_MARCH",
        r"_CARAVAN", r"_TRANSPORT",
        r"_ALL_CAMELS", r"_DRIVE_CAMEL",
        r"_MOVE_CASTLE", r"_MIGRATE",
        r"_OBJECT_LEAVE",
    ]),

    # ── Combat / Battle ──
    ("Combat/Battle", [
        r"_ATTACK_", r"_ATTACK_REQUEST", r"_ATTACK_RETURN",
        r"_CANNON_BATTLE",
        r"_DEFEND(?!_AMRY|_BUILDING)",
        r"_SIEGE", r"_BOMBARDMENT", r"_DESTROY",
        r"_CITY_?DEFENSE", r"_ADD_CITYDEFENSE",
        r"_SHIELD", r"_PEACE_",
        r"_CATAPULT", r"_ASSAULT",
        r"_BATTLE_DETAIL", r"_BATTLE_LEADER",
        r"_BATTLE_REPORT", r"_BATTLE_RECORD",
        r"_COLLECTION_DELETE_RECORD", r"_COLLECTION_RECORD",
        r"_FIGHT_RECORD", r"_REQUEST_BATTLE", r"_RESPONSE_BATTLE",
        r"_OUTFIRE", r"_BURN",
        r"_TRAP_", r"_TRAP_BUILD", r"_TRAP_GOLD",
        r"_AUTO_ATKREBEL",
        r"_CASTLE_DUEL", r"_CASTLE_THUNDER",
        r"_RAID_PLAYER",
        r"_TOWER_MILITARY",
        r"_DAMAGE_HELP", r"_DAMAGE_GIFT", r"_DAMAGE_SHARE",
        r"_DAMAGE_BUY", r"_SYNC_DAMAGE",
        r"_CITY_BUFF",
    ]),

    # ── Troops / Training ──
    ("Troops/Training", [
        r"_SOLDIER", r"_TROOP",
        r"_RECRUIT", r"_CURE_",
        r"_TRAIN(?!_ACTION|_LIVE)", r"_DISMISS",
        r"_EMPLOY_WORKER", r"_WORKER",
        r"_ARMY_LOSS", r"_ARMY_SKIN", r"_AMRY_SKIN",
        r"_CHANGE_AMRY_SKIN",
        r"_SPEEDUP_TRAIN",
        r"_HOSPITAL", r"_HEAL_",
    ]),

    # ── Formation / Army Setup ──
    ("Formation/Army Setup", [
        r"_FORMATION", r"_LINEUP",
        r"_HERO_QUEUE", r"_QUEUE_CHANGE",
        r"_SET_(?:ATTACK|DEFEND|ASSIST)_HERO",
        r"_DEFEND_AMRY", r"_DEFEND_BUILDING",
    ]),

    # ── Buildings ──
    ("Buildings", [
        r"_BUILDING", r"_CONSTRUCT", r"_DEMOLISH",
        r"_EXCHANGE_BUILDING",
        r"_UPGRADE(?!_HERO|_EQUIP|_GEM|_JEWEL|_SKILL|_FAMILIAR|_PACT|_SIGIL|_LEADER|_SKIN|_LV)",
        r"_LEAGUEBUILD", r"_REBUILDING",
        r"_UPDATE_BUILDING",
    ]),

    # ── Research / Tech / Science ──
    ("Research/Tech", [
        r"_RESEARCH", r"_TECH(?!NOLOG)",
        r"_STUDY", r"_ACADEMY",
        r"_SCIENCE",
    ]),

    # ── Heroes / Familiars / Lord ──
    ("Heroes/Familiars", [
        r"_HERO(?!N|IC|_QUEUE|_COLLECTION)",
        r"_HERO_COLLECTION",
        r"_LEADER(?!FLAG|_CHANGE|ID)",
        r"_TALENT", r"_FAMILIAR", r"_PACT",
        r"_SIGIL", r"_RUNE(?!_STONE)",
        r"_LORD_SKILL", r"_LORD_BE",
        r"_LORD_CATCH", r"_LORD_PUNISH",
        r"_LORD_BACK", r"_LORD_EXECUTE",
        r"_LORD_LIKE", r"_LORD_PAY",
        r"_LORD_RELEASE", r"_LORD_SELF",
        r"_LORD_ESCAPE", r"_LORD_SET",
        r"_LORD_UPDATE", r"_GET_LORD",
        r"_SYNC_LORD", r"_CHANGE_LORD",
        r"_HONOR_SOUL", r"_SOUL_SMELT", r"_TURN_SOUL",
        r"_EXTRA_ATTRIBUTE", r"_STATUS_",
        r"_SYN_ATTRIBUTE", r"_SYN_EXTRA",
    ]),

    # ── Equipment / Forge ──
    ("Equipment/Forge", [
        r"_EQUIP(?!_HERO)", r"_FORGE",
        r"_GEM(?!_SEARCH|INI)", r"_JEWEL",
        r"_MATERIAL", r"_ENHANCE",
        r"_EMBED", r"_INLAY",
        r"_ACCESSORY", r"_ARTIFACT",
    ]),

    # ── Items / Inventory ──
    ("Items/Inventory", [
        r"_ITEM_", r"_USE_ITEM", r"_USEITEM",
        r"_BAG_", r"_INVENTORY",
        r"_CHEST", r"_TREASURE",
        r"_SPEED_?UP(?!_MARCH|_TRAIN|_RESEARCH)",
        r"_RESOURCE(?!_TILE|_POINT|_NODE)",
        r"_GATHER", r"_PRODUCE", r"_HARVEST",
        r"_DINAR", r"_ENERGY_CD",
    ]),

    # ── Alliance / Guild / Legion ──
    ("Alliance/Guild", [
        r"_LEAGUE_(?!BATTLE|PASS)", r"_DO_LEAGUE_",
        r"_CLAN_", r"_GUILD(?!_STANDOFF)",
        r"_ALLIANCE", r"_BUILDUP",
        r"_DONATE", r"_DONATION",
        r"_MEMBER_", r"_APPEND_SIGN",
        r"_LEGION(?!_BATTLE|_FINAL|_SEASON|_SELF)",
        r"_LEAGUEPASS",
        r"_CREATE_LEAGUE", r"_EXIT_LEAGUE", r"_QUERY_LEAGUE",
        r"_KICK_MEMBER", r"_HANDLE_APPLY", r"_HANDLE_INVITE",
        r"_INVITE_ENTER", r"_APPLY_ENTER", r"_UNAPPLY_ENTER",
        r"_SYNC_LEAGUEPASS", r"_SYNC_LEAGUE",
        r"_NOTIFY_LEGION",
        r"_NPC_HELP",
    ]),

    # ── Chat / Social / Friends ──
    ("Chat/Social", [
        r"_CHAT_", r"_CHAT_SEND",
        r"_MAIL(?!BOX_MAIL)", r"_MESSAGE",
        r"_FRIEND", r"_FTRIEND", r"_BLOCK_",
        r"_MUTE", r"_WHISPER", r"_BROADCAST",
        r"_TRANSLATE", r"_REPORT_PLAYER",
        r"_NAMEPLATE", r"_AVATAR",
        r"_SIGNATURE", r"_CUSTOM_HEAD",
        r"_CHANGE_NAME(?!PLATE)", r"_HONOR_FLAG",
        r"_LEADERFLAG", r"_CHANGE_LEADERFLAG",
        r"_INVITE_ADD", r"_INVITE_GOLD",
        r"_INVITE_PLAYER",
    ]),

    # ── Pets ──
    ("Pets", [
        r"_PET_",
    ]),

    # ── Events / Activities ──
    ("Events/Activities", [
        r"_ACTIVITY", r"_EVENT",
        r"_FESTIVAL", r"_ANNIVERSARY",
        r"_CARNIVAL", r"_CELEBRATION",
        r"_MOBILIZATION", r"_RUSH_EVENT",
        r"_GIFTPACK", r"_ACTIVEGIFTS", r"_CUSTOMGIFTS",
        r"_EXTRA_GIFTPACK",
        r"_ACTION_EXCHAGE", r"_ACTION_EXCHANGE",
        r"_COMMON_EXCHAGE", r"_COMMON_ACTION",
        r"_ALLFORONE", r"_BESTOW",
        r"_CYCLE_ACTION", r"_DAILYCONSUME",
        r"_DAILY_RECHARGE", r"_DAILY_TASKS",
        r"_DAILY_VIP", r"_DAILY_REWARD",
        r"_CHARGE_DAILY", r"_RECHARGE",
        r"_EVERY_DAY", r"_RETURN_EVENT",
        r"_REWARD_TASK", r"_DELETE_REWARD_TASK",
        r"_ACCUMULATION", r"_CHECK_IN",
        r"_CONTINUITY", r"_CONTINUOUS",
        r"_GENERAL_ACTIBITIES",
        r"_POST_TASK", r"_SERVER_MISSION",
        r"_NEW_ONLINE",
        r"_LEGION_SEASON", r"_LEGION_SELF",
        r"_THREEDAYS_ACTION", r"_SYNC_THREEDAYS",
        r"_OPERATION_ACTION", r"_QUERY_OPERATION",
        r"_SYNC_OPERATION",
        r"_POWER_TASKS",
        r"_SUPERCHAMPIONSHIP", r"_SYNC_CHAMPIONSHIP",
        r"_QUEST_CHAMPIONSHIP",
    ]),

    # ── Rewards (generic reward messages) ──
    ("Rewards", [
        r"_REWARD", r"_RECEIVE_",
        r"_AD_USE_TIMES", r"_AD_WATCHREWARD", r"_AD_SYNC",
        r"_FB_INVITE_REWARD", r"_ARMY_LOSS_REWARD",
        r"_KINGDOM_GIFT", r"_LUCKY_GIFT",
    ]),

    # ── Shop / Store / Lottery / Gambling ──
    ("Shop/Store", [
        r"_SHOP", r"_BUYONESHOP",
        r"_BUY_", r"_PURCHASE", r"_STORE",
        r"_CHARGE(?!_DAILY)",
        r"_VIP(?!_REWARD)", r"_PACKAGE",
        r"_LOTTERY", r"_LUCKY_DRAW",
        r"_LUCKY_TURNTABLE", r"_LUCKY_LINE",
        r"_LUCKY_RED", r"_RECEIVE_LUCKY",
        r"_DOUBLE_LOTTERY",
        r"_WISH", r"_WISHING", r"_FREE_WISHES",
        r"_SPIN", r"_WHEEL_TURN", r"_SYNC_WHEEL",
        r"_AUCTION", r"_BID_",
        r"_LATCH", r"_GOODLUCK", r"_SYNC_GOODLUCK",
        r"_OPEN_SESAME",
        r"_LUCKYPOT", r"_SYNC_LUCKYPOT",
        r"_GOLD_OPEN", r"_SYNC_GOLD",
        r"_INVEST_", r"_MARKET_",
        r"_MAGIC_LAMP", r"_UPDATA_MAGIC",
        r"_SEND_LUCKY", r"_SYS_LUCKY", r"_SYNC_LUCKY",
        r"_WEEK_CARD", r"_WEEKLY_SPECIAL", r"_SYNC_WEEKLY",
        r"_NEWSERVER_LIMITSHOP", r"_NEWSERVER_SIGNFUND",
        r"_SYNC_NEWSERVER",
        r"_SYNC_SUPERCHOOSEONE",
        r"_TRIBUTE", r"_SYS_TRIBUTE",
        r"_FIREWORKS",
        r"_ANSWER_USE",
    ]),

    # ── Kingdom / Map ──
    ("Kingdom/Map", [
        r"_KINGDOM(?!_WAR|_GIFT)", r"_WORLD(?!_BATTLE|_WAR)",
        r"_DOMINION", r"_TERRITORY",
        r"_TILE", r"_LAND_",
        r"_ZONE(?!_REWARD)", r"_REGION",
        r"_ALTAR", r"_THRONE",
        r"_FORTRESS", r"_BASE_",
        r"_WONDER", r"_SHRINE",
        r"_KING(?!_CHESS|DOM|_REWARD|HT)",
        r"_FAVORITE", r"_DEL_FAVORITE",
        r"_GET_MAP", r"_QUERY_MAP",
        r"_OPEN_AREA", r"_FOG_MINE",
        r"_SYNC_KINGDOM", r"_SYNC_DOMINION",
        r"_PLACEMENT", r"_HARBOR",
        r"_STATION_SYNC", r"_CASTLE_SYNC",
        r"_CAMEL_SYNC", r"_THIRDFORCE_SYNC",
        r"_START_LOOK",
    ]),

    # ── Arena / PvP ──
    ("Arena/PvP", [
        r"_ARENA", r"_COLOSSEUM",
        r"_AREN_HERO",
        r"_KING_CHESS", r"_ABANDON_KING_CHESS",
        r"_YAHTZEE",
        r"_PVE_CHALLENGE", r"_PVE_FAST", r"_PVE_FIGHT",
        r"_PVE_POINT", r"_PVE_SYNC",
        r"_MATCH_SERVER",
    ]),

    # ── Minigames ──
    ("Minigames", [
        r"_MINI_GAME", r"_MERGE_GAME", r"_MERGE_EVNET",
        r"_SOLOMON", r"_PLOT_QUEST",
        r"_UPDATE_QUEST", r"_DELETE_QUEST", r"_TRIGGER_QUEST",
    ]),

    # ── Monster / PvE ──
    ("Monster/PvE", [
        r"_MONSTER", r"_BOSS",
        r"_HUNT", r"_INVASION(?!$)",
        r"_EXPEDITION", r"_EXPLORE",
        r"_SECRET_BOSS",
        r"_ALIEN",
    ]),

    # ── Red Paper / Lucky Envelopes ──
    ("Red Packets", [
        r"_RED_PAPER", r"_SYNC_RED",
    ]),

    # ── Knight / Honor ──
    ("Knight", [
        r"_KNIGHT_",
    ]),

    # ── Skin / Cosmetics ──
    ("Skins/Cosmetics", [
        r"_SKIN(?!_FRAGMENT)", r"_CHANGE_SKIN",
    ]),

    # ── Player / Profile / Rank ──
    ("Player/Profile", [
        r"_RANK_", r"_RANK_INFO", r"_RANK_SIMPLE",
        r"_SERVER_PLAYER", r"_PLAYER_MIGRATE",
        r"_UPDATE_PLAYER", r"_REQUEST_PLAYER", r"_RESPONSE_PLAYER",
        r"_USERINFO", r"_GET_OTHER", r"_GET_MYSELF",
        r"_QUERY_NAME", r"_SYNC_NAME",
        r"_ACHIEVEMENT", r"_AF_INFO",
        r"_ATTRIBUTE_INFO", r"_EFFECT_INFO",
        r"_SYN_ALL", r"_SYN_OTHER", r"_SYN_MYSELF",
        r"_SYN_CLOSE", r"_SYN_MONTH", r"_SYN_SIGN",
        r"_SYN_FIGHT", r"_SYN_REBUILDING",
        r"_NEW_SYN", r"_SELF_LEAGUEBUILD",
        r"_SYNC_SUBSCRIPTION", r"_SYNC_HONOR",
        r"_SYNC_RETURN", r"_SYNC_SERVER",
        r"_SYNC_VEC", r"_SYNC_RUSH",
        r"_SYNC_AUTO",
        r"_NOTIFY_", r"_AUTO_HANDUP",
    ]),
])


def load_messages(filepath: str) -> list[tuple[str, str]]:
    """
    Parse FINDINGS.md and return list of (cmsg_name, section).
    Section is one of: 'C2S', 'S2C', 'SYNC', 'Other'.
    """
    messages = []
    current_section = None
    in_code_block = False
    section_map = {
        "C2S (REQUEST/SEND)": "C2S",
        "S2C (RETURN/RECV/INFO)": "S2C",
        "SYNC messages": "SYNC",
        "Other": "Other",
    }

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()

            # Detect section headers
            if stripped.startswith("### "):
                for key, val in section_map.items():
                    if key in stripped:
                        current_section = val
                        break
                else:
                    # Non-CMSG section (URLs, IPs, etc.) - stop parsing
                    if current_section and "URLs" in stripped:
                        current_section = None

            # Track code blocks
            if stripped == "```":
                in_code_block = not in_code_block
                continue

            # Extract CMSG names from code blocks
            if in_code_block and current_section and stripped.startswith("CMSG_"):
                messages.append((stripped, current_section))

    return messages


def categorize(name: str) -> str:
    """Return the first matching category for a CMSG name."""
    for cat_name, patterns in CATEGORIES.items():
        for pat in patterns:
            if re.search(pat, name, re.IGNORECASE):
                return cat_name
    return "Uncategorized"


def find_notable(name: str) -> str | None:
    """Flag messages that are especially interesting for bot development."""
    notable_patterns = {
        r"_MARCH.*REQUEST$": "March action (bot-relevant)",
        r"_TRAIN.*REQUEST$": "Training action",
        r"_BUILDING_OPERAT.*REQUEST$": "Building action",
        r"_RESEARCH.*REQUEST$": "Research action",
        r"_ATTACK.*REQUEST$": "Attack action",
        r"_RALLY.*REQUEST$": "Rally action",
        r"_SCOUT.*REQUEST$": "Scout action",
        r"_REINFORCE.*REQUEST$": "Reinforce action",
        r"_HEARTBEAT": "Keep-alive",
        r"_ENTER_GAME": "Session start",
        r"_CHAT_SEND$": "Chat send",
        r"_GATHER": "Resource gathering",
        r"_RECALL": "Recall march",
        r"_SPEEDUP": "Speed-up action",
        r"_CURE|_HEAL|_HOSPITAL": "Heal troops",
        r"_SHIELD|_PEACE": "Shield/peace",
        r"_USE_ITEM": "Item use",
        r"_DONATE": "Alliance donate",
        r"_FORMATION": "Formation setup",
        r"_ENABLE_VIEW": "Enable view (map)",
    }
    for pat, label in notable_patterns.items():
        if re.search(pat, name, re.IGNORECASE):
            return label
    return None


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load
    messages = load_messages(FINDINGS_PATH)
    print(f"[+] Loaded {len(messages)} CMSG messages from FINDINGS.md")

    # Categorize
    # Structure: category -> direction -> [names]
    categorized: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    notable_msgs: list[tuple[str, str, str, str]] = []  # (name, cat, dir, note)

    for name, section in messages:
        cat = categorize(name)
        direction = classify_direction(name, section)
        categorized[cat][direction].append(name)

        note = find_notable(name)
        if note:
            notable_msgs.append((name, cat, direction, note))

    # Sort categories: put Uncategorized last, rest by total descending
    cat_totals = {}
    for cat in categorized:
        total = sum(len(v) for v in categorized[cat].values())
        cat_totals[cat] = total

    sorted_cats = sorted(
        cat_totals.keys(),
        key=lambda c: (-1 if c == "Uncategorized" else cat_totals[c]),
        reverse=True,
    )
    # Move Uncategorized to end
    if "Uncategorized" in sorted_cats:
        sorted_cats.remove("Uncategorized")
        sorted_cats.append("Uncategorized")

    # ── Write report ───────────────────────────────────────────────────
    with open(OUTPUT_PATH, "w", encoding="utf-8") as out:
        out.write("# Game Systems - CMSG Protocol Categorization\n\n")
        out.write(f"**Total messages analyzed**: {len(messages)}  \n")
        unique_names = set(n for n, _ in messages)
        out.write(f"**Unique CMSG names**: {len(unique_names)}  \n")
        out.write(f"**Game systems identified**: {len(sorted_cats) - 1} + Uncategorized  \n\n")

        # Summary table
        out.write("## Summary\n\n")
        out.write("| # | Game System | C2S | S2C | SYNC | Other | Total |\n")
        out.write("|---|-------------|-----|-----|------|-------|-------|\n")

        grand_c2s = grand_s2c = grand_sync = grand_other = grand_total = 0
        for i, cat in enumerate(sorted_cats, 1):
            dirs = categorized[cat]
            c2s = len(dirs.get("C2S", []))
            s2c = len(dirs.get("S2C", []))
            sync = len(dirs.get("SYNC", []))
            other = len(dirs.get("OTHER", []))
            total = c2s + s2c + sync + other
            out.write(f"| {i} | **{cat}** | {c2s} | {s2c} | {sync} | {other} | {total} |\n")
            grand_c2s += c2s
            grand_s2c += s2c
            grand_sync += sync
            grand_other += other
            grand_total += total

        out.write(f"| | **TOTAL** | **{grand_c2s}** | **{grand_s2c}** | **{grand_sync}** | **{grand_other}** | **{grand_total}** |\n")
        out.write("\n")

        # Coverage stats
        uncat_count = cat_totals.get("Uncategorized", 0)
        coverage = ((grand_total - uncat_count) / grand_total * 100) if grand_total else 0
        out.write(f"**Categorization coverage**: {coverage:.1f}% ({grand_total - uncat_count}/{grand_total} messages categorized)\n\n")

        # Notable messages
        out.write("## Notable Messages (Bot-Relevant)\n\n")
        out.write("| Message | System | Direction | Note |\n")
        out.write("|---------|--------|-----------|------|\n")
        for name, cat, direction, note in sorted(notable_msgs, key=lambda x: (x[3], x[1], x[0])):
            out.write(f"| `{name}` | {cat} | {direction} | {note} |\n")
        out.write(f"\n*{len(notable_msgs)} notable messages identified.*\n\n")

        # Detailed per-category listing
        out.write("---\n\n")
        out.write("## Detailed Listings by Game System\n\n")

        for cat in sorted_cats:
            dirs = categorized[cat]
            total = cat_totals[cat]
            out.write(f"### {cat} ({total} messages)\n\n")

            for dir_label in ["C2S", "S2C", "SYNC", "OTHER"]:
                names = dirs.get(dir_label, [])
                if not names:
                    continue
                dir_display = {
                    "C2S": "Client -> Server (REQUEST/SEND)",
                    "S2C": "Server -> Client (RETURN/RECV)",
                    "SYNC": "SYNC",
                    "OTHER": "Unclassified Direction",
                }[dir_label]
                out.write(f"**{dir_display}** ({len(names)})\n\n")
                out.write("```\n")
                for n in sorted(names):
                    out.write(f"{n}\n")
                out.write("```\n\n")

            out.write("---\n\n")

    print(f"[+] Categorized into {len(sorted_cats)} game systems")
    print(f"[+] Found {len(notable_msgs)} notable/bot-relevant messages")
    print(f"[+] Coverage: {coverage:.1f}% ({grand_total - uncat_count}/{grand_total})")
    print(f"[+] Report written to: {OUTPUT_PATH}")

    # Print summary to console
    print(f"\n{'='*65}")
    print(f"{'#':<4} {'System':<28} {'C2S':>5} {'S2C':>5} {'SYNC':>5} {'Other':>5} {'Total':>6}")
    print("-" * 65)
    for i, cat in enumerate(sorted_cats, 1):
        dirs = categorized[cat]
        c2s = len(dirs.get("C2S", []))
        s2c = len(dirs.get("S2C", []))
        sync = len(dirs.get("SYNC", []))
        other = len(dirs.get("OTHER", []))
        total = c2s + s2c + sync + other
        print(f"{i:<4} {cat:<28} {c2s:>5} {s2c:>5} {sync:>5} {other:>5} {total:>6}")
    print("-" * 65)
    print(f"{'':4} {'TOTAL':<28} {grand_c2s:>5} {grand_s2c:>5} {grand_sync:>5} {grand_other:>5} {grand_total:>6}")

    # Print uncategorized prefixes for debugging
    if "Uncategorized" in categorized:
        from collections import Counter
        uncat_all = []
        for d in categorized["Uncategorized"].values():
            uncat_all.extend(d)
        prefixes = Counter()
        for name in uncat_all:
            parts = name.replace("CMSG_", "").split("_")
            prefix = parts[0] if len(parts) == 1 else f"{parts[0]}_{parts[1]}"
            prefixes[prefix] += 1
        print(f"\n[*] Top uncategorized prefixes:")
        for p, c in prefixes.most_common(20):
            print(f"    {p}: {c}")


if __name__ == "__main__":
    main()

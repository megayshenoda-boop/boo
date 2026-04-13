"""
WORKING Gather Bot - uses the correct 3-step protocol:
  1. 0x0CEB prelude (10B plaintext = build_train_action)
  2. 0x099D Ã— N troop selections (4B each, unencrypted)
  3. 0x0CE8 gather (46B plaintext)

Plaintext structures decoded from real game client PCAP:

0x0CEB prelude (10B):
  [0]    = train_type (0x01)
  [1:5]  = igg_id (LE u32)
  [5:9]  = zeros
  [9]    = flag (0x01)

0x0CE8 gather (46B):
  [0]    = march_slot (0x01)
  [1:4]  = random header bytes
  [4:6]  = march_type (LE u16, 0x1749 for gather)
  [6:9]  = zeros
  [9:11] = tile_x (LE u16)
  [11:13] = tile_y (LE u16)
  [13]   = flag (0x01)
  [14]   = hero_id (as u8, within u32 LE)
  [15:18] = zeros (rest of hero u32)
  [18]   = 0xB6 (troop tier indicator)
  [19:22] = zeros
  [22]   = 0x04 (troop type count?)
  [23:33] = zeros
  [33:37] = igg_id (LE u32)
  [37:46] = zeros

0x099D troop selection (4B, plain/unencrypted):
  [0:4] = troop_type_id (LE u32)
"""
from __future__ import annotations
import sys, struct, socket, time, threading, argparse, json, random, zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from COMPLETE_BOT import (
    CMsgCodec, build_000B, build_001F, build_0021, build_heartbeat,
    build_packet, build_train_action, derive_gateway_token,
    extract_server_key_from_0x0038, parse_000C, extract_key_from_adb,
    GATEWAY_IP, GATEWAY_PORT, WORLD_ID
)
from speed_train_replay_probe import PacketReader

IGG_ID = 577962733

# Default troop IDs for direct/manual flow.
DEFAULT_TROOPS = [403, 405, 406, 407, 411]

# Search-based success capture (PCAPdroid_21_Mar_11_22_28) used 7 IDs.
SEARCH_CAPTURE_TROOPS = [403, 404, 405, 406, 407, 409, 410]

# Troop formation IDs from real game capture (0x0834 packet)
# These are the account's available troop types
FORMATION_TROOPS = [1025, 1046, 2014, 3002, 1035, 2008, 2019, 1009, 1024, 1016]

# Verified 46-byte plaintexts decoded directly from successful PCAP sessions.
# We patch dynamic fields (slot, tile, hero, kingdom, igg_id) before encoding 0x0CE8.
GATHER_TEMPLATES = [
    {
        "name": "kpa_search_l1_probe_21mar",
        "hero": 255,
        "level": 1,
        "plain": "210d1e0ce94800cb20ed02732252ffcb204fb6cb204f04cb204f00cb204f00cb207e0238024f00cb204f00cb204f",
        "probe_only": True,
        "patch_slot": False,
        "tile_offset": 33,
        "igg_offset": 9,
    },
    {"name": "hero255_lvl1_cap_22mar", "hero": 255, "level": 1,
     "plain": "011be0c649170000008a02400201ff000000b60000000400000000000000000000ed027322000000000000000000"},
    {"name": "hero255_lvl1_cap_21mar_a", "hero": 255, "level": 1,
     "plain": "01386abb49170000006a02100201ff000000b60000000400000000000000000000ed027322000000000000000000"},
    {"name": "hero255_lvl1_cap_21mar_b", "hero": 255, "level": 1,
     "plain": "01e5d9be49170000009902520201ff000000b60000000400000000000000000000ed027322000000000000000000"},
    {"name": "hero255_lvl1_cap_21mar_c", "hero": 255, "level": 1,
     "plain": "015e1ebf49170000007e02380201ff000000b60000000400000000000000000000ed027322000000000000000000"},
    {"name": "hero244_lvl1_cap_22mar", "hero": 244, "level": 1,
     "plain": "01e400c549170000008402400201f4000000b60000000400000000000000000000ed027322000000000000000000"},
]

LOG_FILE = None

def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line)
    if LOG_FILE:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(line + '\n')


def choose_templates(hero_id: int, resource_level: int, allow_fallback: bool = False):
    accepted_templates = [t for t in GATHER_TEMPLATES if not t.get("probe_only")]
    hero_level = [
        t
        for t in accepted_templates
        if t["hero"] == hero_id and t["level"] == resource_level
    ]
    if hero_level and not allow_fallback:
        return hero_level, "exact(hero+level)"
    if not hero_level and not allow_fallback:
        return [], "none"

    ordered = []
    seen_names = set()
    for candidate in hero_level:
        if candidate["name"] not in seen_names:
            ordered.append(candidate)
            seen_names.add(candidate["name"])
    for candidate in accepted_templates:
        if candidate["hero"] == hero_id and candidate["name"] not in seen_names:
            ordered.append(candidate)
            seen_names.add(candidate["name"])
    for candidate in accepted_templates:
        if candidate["level"] == resource_level and candidate["name"] not in seen_names:
            ordered.append(candidate)
            seen_names.add(candidate["name"])
    for candidate in accepted_templates:
        if candidate["name"] not in seen_names:
            ordered.append(candidate)
            seen_names.add(candidate["name"])
    mode = "exact+fallback(multi-template)" if hero_level else "fallback(multi-template)"
    return ordered, mode


def parse_troop_ids(raw: str):
    values = []
    for part in raw.split(','):
        part = part.strip()
        if not part:
            continue
        values.append(int(part))
    return values


def parse_slot_ids(raw: str):
    values = []
    for part in raw.split(','):
        part = part.strip()
        if not part:
            continue
        slot = int(part)
        if slot < 1 or slot > 3:
            raise ValueError(f"Invalid slot {slot}; expected 1..3")
        values.append(slot)
    return values


def tile_key(tile_x: int, tile_y: int) -> str:
    return f"{tile_x},{tile_y}"


def load_recent_tiles(path: Path, ttl_seconds: float):
    now = time.time()
    if not path.exists():
        return {}
    try:
        raw = json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return {}
    if not isinstance(raw, dict):
        return {}

    cleaned = {}
    for key, ts in raw.items():
        if not isinstance(key, str):
            continue
        if not isinstance(ts, (int, float)):
            continue
        if ttl_seconds > 0 and (now - float(ts)) > ttl_seconds:
            continue
        cleaned[key] = float(ts)
    return cleaned


def save_recent_tiles(path: Path, recent_tiles: dict, max_entries: int):
    if max_entries > 0 and len(recent_tiles) > max_entries:
        sorted_items = sorted(recent_tiles.items(), key=lambda item: item[1], reverse=True)
        recent_tiles = dict(sorted_items[:max_entries])
    path.write_text(json.dumps(recent_tiles, ensure_ascii=True, indent=2), encoding='utf-8')


def build_search_payload(resource_type: int, resource_level: int) -> bytes:
    if not (1 <= resource_level <= 255):
        raise ValueError(f"Unsupported resource level: {resource_level}")

    # Real wheat captures show 0x033E payloads as:
    #   level 1 -> 01040003
    #   level 2 -> 02040003
    #   level 5 -> 05040003
    # So the first byte is level, while wheat search family is 0x04.
    if resource_type == 1:
        return bytes([resource_level & 0xFF, 0x04, 0x00, 0x03])

    # Other resource-family bytes are not fully decoded yet; keep the legacy
    # fallback format explicit instead of silently pretending it is verified.
    return bytes([resource_type & 0xFF, resource_level & 0xFF, 0x00, 0x03])


def build_1b8b_plain(seed32: int) -> bytes:
    seed = seed32.to_bytes(4, 'little')
    x_lo = (seed[2] + 0x13) & 0xFF
    x_hi = (seed[3] - 0x02) & 0xFF
    x = x_lo | (x_hi << 8)
    mid = ((x_hi + 0x22) & 0xFF) << 8 | ((x_lo + 0x73) & 0xFF)
    y = ((x_hi - 0x01) & 0xFF) << 8 | ((x_lo - 0x01) & 0xFF)
    return seed + struct.pack('<H', mid) + struct.pack('<H', x) * 2 + struct.pack('<H', y) * 4


def derive_1b8b_seed_candidates(session_body: str, server_key: int, password_info: bytes = b""):
    candidates = []
    seen = set()

    def add(label: str, value: int):
        value &= 0xFFFFFFFF
        if value in seen:
            return
        seen.add(value)
        candidates.append((label, value))

    session_bytes = b""
    if session_body:
        try:
            session_bytes = bytes.fromhex(session_body)
        except ValueError:
            session_bytes = b""

    add("server_key", server_key)
    add("crc32_session_ascii", zlib.crc32(session_body.encode("ascii")) if session_body else 0)
    if session_bytes:
        add("crc32_session_bytes", zlib.crc32(session_bytes))
        if len(session_bytes) >= 4:
            head_le = struct.unpack('<I', session_bytes[:4])[0]
            tail_le = struct.unpack('<I', session_bytes[-4:])[0]
            add("session_head_le", head_le)
            add("session_tail_le", tail_le)
            add("session_head_xor_server", head_le ^ server_key)
            add("session_tail_xor_server", tail_le ^ server_key)
        if len(session_bytes) >= 8:
            add("session_mid4_le", struct.unpack('<I', session_bytes[4:8])[0])
        if len(session_bytes) >= 12:
            add("session_mid8_le", struct.unpack('<I', session_bytes[8:12])[0])
    if password_info:
        add("crc32_1b8a", zlib.crc32(password_info))
        if len(password_info) >= 4:
            add("1b8a_head_le", struct.unpack('<I', password_info[:4])[0])

    return candidates


def resolve_1b8b_seed_from_label(session_ctx: dict, label: str) -> int | None:
    if not label:
        return None
    candidates = derive_1b8b_seed_candidates(
        str(session_ctx.get("session_body", "")),
        int(session_ctx.get("server_key", 0)),
        bytes(session_ctx.get("password_info", b"")),
    )
    for candidate_label, candidate_value in candidates:
        if candidate_label == label:
            return candidate_value
    return None


def search_tile_non_repeating(gs, reader, resource_type, resource_level,
                              recent_tiles: dict, max_attempts: int, retry_delay: float,
                              blocked_tiles=None):
    if max_attempts < 1:
        max_attempts = 1
    if blocked_tiles is None:
        blocked_tiles = set()

    last_tile = (None, None)
    for attempt in range(1, max_attempts + 1):
        tile_x, tile_y = search_tile(gs, reader, resource_type, resource_level)
        if tile_x is None:
            return None, None
        if tile_x == 0 and tile_y == 0:
            log(f"Search returned invalid zero tile=(0,0) attempt={attempt}/{max_attempts}; retrying...")
            time.sleep(max(0.0, retry_delay))
            continue
        last_tile = (tile_x, tile_y)
        key = tile_key(tile_x, tile_y)
        if key in blocked_tiles:
            log(f"Search returned blocked tile=({tile_x},{tile_y}) attempt={attempt}/{max_attempts}; retrying...")
            time.sleep(max(0.0, retry_delay))
            continue
        if key not in recent_tiles:
            if attempt > 1:
                log(f"Picked new tile after retries: ({tile_x},{tile_y}) on attempt {attempt}/{max_attempts}")
            return tile_x, tile_y
        log(
            f"Search returned recent tile=({tile_x},{tile_y}) "
            f"attempt={attempt}/{max_attempts}; retrying..."
        )
        time.sleep(max(0.0, retry_delay))

    if last_tile[0] is not None:
        log(
            f"ERROR: search exhausted {max_attempts} attempts and only returned recent tiles; "
            f"last=({last_tile[0]},{last_tile[1]})"
        )
    return None, None


def build_gather_from_template(template, tile_x, tile_y, hero_id, march_slot=1, kingdom=182):
    plain = bytearray.fromhex(template["plain"])
    if len(plain) != 46:
        raise ValueError(f"Template {template['name']} has invalid length {len(plain)} (expected 46).")
    patch_slot = template.get("patch_slot", True)
    slot_offset = int(template.get("slot_offset", 0))
    tile_offset = int(template.get("tile_offset", 9))
    hero_offset = int(template.get("hero_offset", 14))
    kingdom_offset = int(template.get("kingdom_offset", 18))
    patch_igg = template.get("patch_igg", True)
    igg_offset = int(template.get("igg_offset", 33))

    if patch_slot:
        if not (0 <= slot_offset < len(plain)):
            raise ValueError(f"Template {template['name']} has invalid slot_offset={slot_offset}")
        plain[slot_offset] = march_slot & 0xFF
    if not (0 <= tile_offset <= len(plain) - 4):
        raise ValueError(f"Template {template['name']} has invalid tile_offset={tile_offset}")
    if not (0 <= hero_offset < len(plain)):
        raise ValueError(f"Template {template['name']} has invalid hero_offset={hero_offset}")
    if not (0 <= kingdom_offset < len(plain)):
        raise ValueError(f"Template {template['name']} has invalid kingdom_offset={kingdom_offset}")

    # Randomize march nonce bytes [1:4] to avoid server rejecting duplicate IDs
    plain[1] = random.randint(0, 255)
    plain[2] = random.randint(0, 255)
    plain[3] = random.randint(0, 255)

    struct.pack_into('<HH', plain, tile_offset, tile_x, tile_y)
    plain[hero_offset] = hero_id & 0xFF
    plain[kingdom_offset] = kingdom & 0xFF
    if patch_igg:
        if not (0 <= igg_offset <= len(plain) - 4):
            raise ValueError(f"Template {template['name']} has invalid igg_offset={igg_offset}")
        struct.pack_into('<I', plain, igg_offset, IGG_ID)
    return bytes(plain), template["name"]


def connect_game(log_session_candidates: bool = False):
    """Full login: ADB key -> gateway -> game server + server key."""
    access_key = extract_key_from_adb()
    if not access_key:
        raise RuntimeError("No access key from ADB")
    log(f"Access key: {access_key[:8]}...")
    
    token = derive_gateway_token(access_key)
    gw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    gw.settimeout(10)
    gw.connect((GATEWAY_IP, GATEWAY_PORT))
    gw.sendall(build_000B(IGG_ID, token, WORLD_ID))
    hdr = b''
    while len(hdr) < 4:
        hdr += gw.recv(4 - len(hdr))
    pkt_len, op = struct.unpack('<HH', hdr)
    pl = b''
    while len(pl) < pkt_len - 4:
        pl += gw.recv(pkt_len - 4 - len(pl))
    gw.close()
    
    if op != 0x000C:
        raise RuntimeError(f"Gateway returned 0x{op:04X}")
    info = parse_000C(pl)
    if not info or not info.get('ip'):
        raise RuntimeError("Gateway empty redirect")
    log(f"Gateway -> {info['ip']}:{info['port']}")
    
    gs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    gs.settimeout(30)
    gs.connect((info['ip'], info['port']))
    reader = PacketReader(gs)
    gs.sendall(build_001F(IGG_ID, info['token']))
    login = reader.read_one(10)
    if not login or login[0] != 0x0020 or login[1][0] != 1:
        raise RuntimeError("Game login failed")
    log("Game login OK")
    gs.sendall(build_0021(IGG_ID))
    
    # Wait for server key
    server_key = None
    for _ in range(500):
        pkt = reader.read_one(2.0)
        if pkt is None:
            break
        rop, rpl, _ = pkt
        if rop == 0x0038:
            server_key = extract_server_key_from_0x0038(rpl)
            if server_key:
                log(f"Server key: 0x{server_key:08X}")
                break
    
    if not server_key:
        raise RuntimeError("No server key")
    
    codec = CMsgCodec.from_u32(server_key)
    
    # Drain remaining init flood
    saw_1b8a = False
    saw_0022 = False
    saw_0172 = False
    saw_036c = False
    session_ctx = {
        "server_key": server_key,
        "password_info": b"",
        "session_body": "",
        "session_status": None,
        "init_seen_0172": False,
        "init_seen_036c": False,
    }
    for _ in range(1000):
        pkt = reader.read_one(0.2)
        if pkt is None:
            break
        rop, rpl, _ = pkt
        if rop == 0x1B8A and not saw_1b8a:
            saw_1b8a = True
            session_ctx["password_info"] = rpl
            log(f"Init password-info 0x1B8A ({len(rpl)}B) payload={rpl.hex()}")
        elif rop == 0x0172 and not saw_0172:
            saw_0172 = True
            session_ctx["init_seen_0172"] = True
            log(f"Init recv 0x0172 ({len(rpl)}B)")
        elif rop == 0x036C and not saw_036c:
            saw_036c = True
            session_ctx["init_seen_036c"] = True
            log(f"Init recv 0x036C ({len(rpl)}B)")
        elif rop == 0x0022 and not saw_0022:
            saw_0022 = True
            body = ""
            status = None
            if len(rpl) >= 34:
                body = rpl[2:34].decode('ascii', errors='replace')
                status = rpl[-1]
            session_ctx["session_body"] = body
            session_ctx["session_status"] = status
            log(
                f"Init session-string 0x0022 ({len(rpl)}B) "
                f"body={body or '-'} status={status if status is not None else '-'} payload={rpl.hex()[:96]}"
            )
            if log_session_candidates:
                seeds = derive_1b8b_seed_candidates(
                    body,
                    server_key,
                    session_ctx["password_info"],
                )
                formatted = ", ".join(f"{label}=0x{value:08X}" for label, value in seeds)
                log(f"Session seed candidates: {formatted}")

    return gs, reader, codec, session_ctx


def search_tile(gs, reader, resource_type=1, resource_level=4):
    """Search for a resource tile."""
    search_payload = build_search_payload(resource_type, resource_level)
    gs.sendall(build_packet(0x033E, search_payload))
    mode = "verified-wheat" if resource_type == 1 else "legacy-unverified"
    log(
        f"Sent 0x033E search payload={search_payload.hex()} "
        f"(resource_type={resource_type} level={resource_level} mode={mode})"
    )
    
    for _ in range(20):
        pkt = reader.read_one(3.0)
        if pkt is None:
            break
        op, pl, _ = pkt
        if op == 0x033F and len(pl) >= 5:
            level_echo = pl[0]
            tile_x = struct.unpack('<H', pl[1:3])[0]
            tile_y = struct.unpack('<H', pl[3:5])[0]
            log(f"Recv 0x033F level_echo={level_echo} tile=({tile_x},{tile_y})")
            return tile_x, tile_y
    
    return None, None


def select_tile(gs, reader, tile_x, tile_y):
    """Select a tile on map."""
    pl = struct.pack('<HHB', tile_x, tile_y, 1)
    gs.sendall(build_packet(0x006E, pl))
    log(f"Sent 0x006E tile=({tile_x},{tile_y})")
    time.sleep(0.3)
    # Drain
    for _ in range(5):
        pkt = reader.read_one(0.3)
        if pkt is None:
            break


def send_troop_selections(gs, troop_ids):
    """Send 0x099D troop selection packets."""
    for tid in troop_ids:
        pl = struct.pack('<I', tid)
        gs.sendall(build_packet(0x099D, pl))
    log(f"Sent {len(troop_ids)}x 0x099D troops={troop_ids}")


def do_gather(gs, reader, codec, tile_x, tile_y, hero_id=255,
              march_slot=1, troop_ids=None, formation_ids=None,
              kingdom=182, resource_level=4, allow_template_fallback=False,
              max_template_attempts=0, template_wait_seconds=12.0,
              template_name='',
              send_hero_select=False, send_ready_sig=False, ready_sig_wait=0.6,
              skip_ui_setup=False,
              send_source_first=False, source_x=653, source_y=567,
              send_0840=False,
              send_setup_extras=False, send_1b8b_hex='',
              send_setup_17a3=True,
              send_1b8b_structured=False, send_1b8b_seed32=None,
              prelude_after_troops=False, send_setup_target_select=False,
              auto_search_sync_first=False, setup_recv_window=0.0,
              send_pre_0ce8_heartbeat=False, pre_0ce8_heartbeat_wait=1.0,
              send_post_0ce8_heartbeat=False, post_0ce8_heartbeat_delay=0.0,
              resource_type=1, allow_repeat_target=False, recent_tiles=None,
              max_search_attempts=8, search_retry_delay=0.3):
    """Execute gather flow and optionally resolve the target via in-flow search."""
    if formation_ids is None:
        formation_ids = FORMATION_TROOPS
    if troop_ids is None:
        troop_ids = DEFAULT_TROOPS

    resolved_tile_x = tile_x
    resolved_tile_y = tile_y

    if not skip_ui_setup:
        try:
            if send_0840:
                gs.sendall(build_packet(0x0840, b''))
                log("Sent 0x0840")

            if send_setup_target_select and resolved_tile_x is not None and resolved_tile_y is not None:
                setup_tile_pl = struct.pack('<HHB', resolved_tile_x, resolved_tile_y, 1)
                gs.sendall(build_packet(0x006E, setup_tile_pl))
                log(f"Sent setup 0x006E tile=({resolved_tile_x},{resolved_tile_y})")

            gs.sendall(build_packet(0x0245, b''))
            log("Sent 0x0245")

            formation_data = struct.pack('<H', len(formation_ids))
            for tid in formation_ids:
                formation_data += struct.pack('<I', tid)
            gs.sendall(build_packet(0x0834, formation_data))
            log(f"Sent 0x0834 formation ({len(formation_ids)} troops)")

            if send_setup_extras:
                gs.sendall(build_packet(0x0709, b''))
                gs.sendall(build_packet(0x0A2C, b''))
                setup_extra_names = ["0x0709", "0x0A2C"]
                if send_setup_17a3:
                    gs.sendall(build_packet(0x17A3, b'\x02\x00\x00\x00'))
                    setup_extra_names.append("0x17A3")
                log(f"Sent setup extras: {' + '.join(setup_extra_names)}")
                if send_1b8b_structured:
                    seed32 = send_1b8b_seed32 if send_1b8b_seed32 is not None else random.getrandbits(32)
                    plain_1b8b = build_1b8b_plain(seed32)
                    packet_1b8b = codec.encode(0x1B8B, plain_1b8b)
                    gs.sendall(packet_1b8b)
                    log(
                        f"Sent structured 0x1B8B seed32=0x{seed32:08X} "
                        f"plain={plain_1b8b.hex()} packet={packet_1b8b.hex()}"
                    )
                elif send_1b8b_hex:
                    try:
                        payload_1b8b = bytes.fromhex(send_1b8b_hex)
                    except ValueError:
                        log(f"ERROR invalid --send-1b8b hex payload: {send_1b8b_hex!r}")
                        return False, resolved_tile_x, resolved_tile_y, False
                    gs.sendall(build_packet(0x1B8B, payload_1b8b))
                    log(f"Sent 0x1B8B ({len(payload_1b8b)}B)")
        except OSError as exc:
            log(f"ERROR setup send failed: {exc}")
            return False, resolved_tile_x, resolved_tile_y, False

        time.sleep(0.5)
        saw_setup_17a4 = False
        try:
            if setup_recv_window > 0:
                deadline = time.time() + setup_recv_window
                while time.time() < deadline:
                    pkt = reader.read_one(0.2)
                    if pkt is None:
                        continue
                    op, pl, _ = pkt
                    if op == 0x17A4:
                        saw_setup_17a4 = True
                    if op not in (0x0002, 0x0042, 0x026D):
                        log(f"  Setup recv 0x{op:04X} ({len(pl)}B)")
            else:
                for _ in range(20):
                    pkt = reader.read_one(0.2)
                    if pkt is None:
                        break
                    op, pl, _ = pkt
                    if op == 0x17A4:
                        saw_setup_17a4 = True
                    if op not in (0x0002, 0x0042, 0x026D):
                        log(f"  Setup recv 0x{op:04X} ({len(pl)}B)")
        except OSError as exc:
            log(f"ERROR setup recv failed: {exc}")
            return False, resolved_tile_x, resolved_tile_y, False
        if send_setup_extras and not saw_setup_17a4:
            log("NOTE setup extras were sent but 0x17A4 did not appear in setup replies")

    prelude = build_train_action(IGG_ID, train_type=0x01, flag=0x01)

    auto_search_mode = resolved_tile_x is None or resolved_tile_y is None
    blocked_search_tiles = set()

    def send_source_tile():
        source_pl = struct.pack('<HHB', source_x, source_y, 1)
        gs.sendall(build_packet(0x006E, source_pl))
        log(f"Sent source 0x006E tile=({source_x},{source_y})")
        time.sleep(0.2)

    def send_prelude(send_source_now: bool = False):
        pkt = codec.encode(0x0CEB, prelude)
        gs.sendall(pkt)
        log(f"Sent 0x0CEB prelude: {prelude.hex()}")
        if send_source_now and send_source_first:
            send_source_tile()

    def send_troops():
        send_troop_selections(gs, troop_ids)

    def send_sync():
        gs.sendall(build_packet(0x0767, b''))
        gs.sendall(build_packet(0x0769, b''))
        log("Sent 0x0767 + 0x0769")

    def wait_for_search_prereq_sync(timeout_seconds: float = 1.5):
        deadline = time.time() + max(0.0, timeout_seconds)
        while time.time() < deadline:
            try:
                pkt = reader.read_one(0.2)
            except OSError as exc:
                log(f"ERROR waiting for sync replies before search failed: {exc}")
                return False
            if pkt is None:
                continue
            op, pl, _ = pkt
            if op == 0x099E:
                log(f"  Pre-search troop confirm 0x099E: {pl.hex()}")
            elif op == 0x0768:
                log(f"  Pre-search sync ack 0x0768 payload={pl.hex()}")
            elif op == 0x076A:
                log(f"  Pre-search sync ack 0x076A payload={pl.hex()[:80]}")
                return True
            elif op == 0x036C:
                log(f"  Pre-search aux 0x036C payload={pl.hex()[:80]}")
            elif op not in (0x0042, 0x0002):
                log(f"  Pre-search recv 0x{op:04X} ({len(pl)}B) payload={pl.hex()[:80]}")
        return True

    try:
        if auto_search_mode:
            if auto_search_sync_first and prelude_after_troops:
                log("Using search-specific pre-0x0CE8 order: troops -> sync -> prelude -> source")
                log("NOTE this matches the old strong baseline order.")
                send_troops()
                send_sync()
                send_prelude(send_source_now=False)
                if send_source_first:
                    send_source_tile()
            elif prelude_after_troops:
                log("Using search-specific pre-0x0CE8 order: troops -> prelude -> source -> sync")
                log("NOTE this differs from the old strong baseline order: troops -> sync -> prelude -> source")
                send_troops()
                send_prelude(send_source_now=False)
                if send_source_first:
                    send_source_tile()
                send_sync()
            else:
                log("Using search-specific pre-0x0CE8 order: prelude -> troops -> source -> sync")
                log("NOTE this differs from the old strong baseline order: sync happened before prelude/source")
                send_prelude(send_source_now=False)
                send_troops()
                if send_source_first:
                    send_source_tile()
                send_sync()
            if not wait_for_search_prereq_sync():
                return False, resolved_tile_x, resolved_tile_y, False
        elif prelude_after_troops:
            send_troops()
            send_sync()
            send_prelude(send_source_now=True)
        else:
            send_prelude(send_source_now=True)
            send_troops()
            send_sync()
    except OSError as exc:
        log(f"ERROR sending prelude/troops/sync failed: {exc}")
        return False, resolved_tile_x, resolved_tile_y, False

    if resolved_tile_x is None or resolved_tile_y is None:
        log("Resolving target tile via in-flow search after prelude/sync")
        if allow_repeat_target:
            resolved_tile_x, resolved_tile_y = search_tile(
                gs,
                reader,
                resource_type=resource_type,
                resource_level=resource_level,
            )
        else:
            resolved_tile_x, resolved_tile_y = search_tile_non_repeating(
                gs=gs,
                reader=reader,
                resource_type=resource_type,
                resource_level=resource_level,
                recent_tiles=recent_tiles or {},
                max_attempts=max_search_attempts,
                retry_delay=search_retry_delay,
                blocked_tiles=blocked_search_tiles,
            )
        if resolved_tile_x is None or resolved_tile_y is None:
            log("ERROR failed to resolve target tile during in-flow search")
            return False, resolved_tile_x, resolved_tile_y, False
    else:
        log(f"Using resolved target tile=({resolved_tile_x},{resolved_tile_y})")

    def pre_target_probe(timeout_seconds: float = 0.9):
        saw_map_snapshot = False
        deadline = time.time() + max(0.0, timeout_seconds)
        while time.time() < deadline:
            pkt = reader.read_one(0.2)
            if pkt is None:
                continue
            op, pl, _ = pkt
            if op == 0x0091:
                # Search-success PCAPs can show 0x0091 before 0x0CE8.
                log(f"  Target probe info 0x0091 ({len(pl)}B) payload={pl.hex()[:80]}")
                continue
            if op in (0x0080, 0x0082):
                # Search-success PCAPs can also show 0x0080/0x0082 before 0x0CE8.
                # Keep them visible in logs but do not reject the searched tile on
                # that basis alone.
                log(f"  Target probe context 0x{op:04X} ({len(pl)}B) payload={pl.hex()[:80]}")
                continue
            if op in (0x0076, 0x0077, 0x0078):
                saw_map_snapshot = True
                # Successful search-based PCAPs return 0x0076/0x0077/0x0078/0x007A
                # after selecting the searched tile. Treat them as normal map
                # snapshots unless an explicit weak opcode appears.
                log(f"  Target probe recv 0x{op:04X} ({len(pl)}B) payload={pl.hex()[:80]}")
                continue
            if op == 0x007A:
                log(f"  Target probe recv 0x{op:04X} ({len(pl)}B) payload={pl.hex()[:80]}")
                if saw_map_snapshot:
                    break
                continue
            if op not in (0x0002, 0x0042, 0x036C):
                log(f"  Target probe recv 0x{op:04X} ({len(pl)}B) payload={pl.hex()[:80]}")
        return []

    target_select_tries = max(1, max_search_attempts if auto_search_mode and not allow_repeat_target else 1)
    for target_try in range(1, target_select_tries + 1):
        tile_pl = struct.pack('<HHB', resolved_tile_x, resolved_tile_y, 1)
        try:
            gs.sendall(build_packet(0x006E, tile_pl))
        except OSError as exc:
            log(f"ERROR sending target 0x006E failed: {exc}")
            return False, resolved_tile_x, resolved_tile_y, False
        log(f"Re-sent 0x006E tile=({resolved_tile_x},{resolved_tile_y})")

        weak_seen = pre_target_probe()
        if not weak_seen:
            break

        if not auto_search_mode or allow_repeat_target:
            log("Target probe saw weak non-gather signals; continuing because auto-search replacement is disabled.")
            break
        if target_try >= target_select_tries:
            log("ERROR target probe kept returning weak signals; no more replacement attempts.")
            return False, resolved_tile_x, resolved_tile_y, False

        bad_key = tile_key(resolved_tile_x, resolved_tile_y)
        blocked_search_tiles.add(bad_key)
        log(
            f"Rejecting searched tile ({resolved_tile_x},{resolved_tile_y}) due to weak pre-0x0CE8 signals "
            f"{[f'0x{op:04X}' for op in weak_seen]}; searching another tile."
        )
        resolved_tile_x, resolved_tile_y = search_tile_non_repeating(
            gs=gs,
            reader=reader,
            resource_type=resource_type,
            resource_level=resource_level,
            recent_tiles=recent_tiles or {},
            max_attempts=max_search_attempts,
            retry_delay=search_retry_delay,
            blocked_tiles=blocked_search_tiles,
        )
        if resolved_tile_x is None or resolved_tile_y is None:
            log("ERROR failed to resolve replacement tile after weak target probe")
            return False, resolved_tile_x, resolved_tile_y, False

    if send_hero_select:
        try:
            hero_payload = bytes([0x00, 0x01, 0x00]) + struct.pack('<I', hero_id)
            gs.sendall(build_packet(0x0323, hero_payload))
            log(f"Sent 0x0323 hero_select hero={hero_id} payload={hero_payload.hex()}")
            time.sleep(0.2)
        except OSError as exc:
            log(f"ERROR sending 0x0323 hero select failed: {exc}")
            return False, resolved_tile_x, resolved_tile_y, False

    if send_ready_sig:
        try:
            gs.sendall(build_packet(0x01D6, b''))
            log("Sent 0x01D6 ready signal")
        except OSError as exc:
            log(f"ERROR sending 0x01D6 ready signal failed: {exc}")
            return False, resolved_tile_x, resolved_tile_y, False

        deadline = time.time() + max(0.0, ready_sig_wait)
        while time.time() < deadline:
            try:
                pkt = reader.read_one(0.2)
            except OSError as exc:
                log(f"ERROR waiting after 0x01D6 failed: {exc}")
                return False, resolved_tile_x, resolved_tile_y, False
            if pkt is None:
                continue
            op, pl, _ = pkt
            if op == 0x0037:
                log(f"Recv ready-sig reply 0x0037 payload={pl.hex()}")
            elif op == 0x0033:
                log(f"Recv ready-sig side-effect 0x0033 payload={pl.hex()}")
            elif op not in (0x0002, 0x0042, 0x036C):
                log(f"  Post-0x01D6 recv 0x{op:04X} ({len(pl)}B) payload={pl.hex()[:80]}")

    if send_pre_0ce8_heartbeat:
        try:
            hb_ms = int(time.monotonic() * 1000) & 0xFFFFFFFF
            gs.sendall(build_heartbeat(hb_ms))
            log(f"Sent pre-0x0CE8 heartbeat 0x0042 ms={hb_ms}")
        except OSError as exc:
            log(f"ERROR sending pre-0x0CE8 heartbeat failed: {exc}")
            return False, resolved_tile_x, resolved_tile_y, False

        deadline = time.time() + max(0.0, pre_0ce8_heartbeat_wait)
        while time.time() < deadline:
            try:
                pkt = reader.read_one(0.2)
            except OSError as exc:
                log(f"ERROR waiting pre-0x0CE8 heartbeat echo failed: {exc}")
                return False, resolved_tile_x, resolved_tile_y, False
            if pkt is None:
                continue
            op, pl, _ = pkt
            if op == 0x0042:
                log(f"Recv heartbeat echo 0x0042 payload={pl.hex()}")
                break
            if op not in (0x0002, 0x036C):
                log(f"  Pre-0x0CE8 recv 0x{op:04X} ({len(pl)}B) payload={pl.hex()[:80]}")

    time.sleep(0.3)

    templates, template_match_mode = choose_templates(
        hero_id=hero_id,
        resource_level=resource_level,
        allow_fallback=allow_template_fallback,
    )
    if template_name:
        templates = [t for t in templates if t["name"] == template_name]
        if not templates:
            templates = [t for t in GATHER_TEMPLATES if t["name"] == template_name]
        template_match_mode = f"forced({template_name})"
    if not templates:
        supported = sorted({(t["hero"], t["level"]) for t in GATHER_TEMPLATES})
        log(
            f"ERROR No accepted template for hero={hero_id} level={resource_level}. "
            f"Supported pairs={supported}. Use --allow-template-fallback if needed."
        )
        return False, resolved_tile_x, resolved_tile_y, False
    if max_template_attempts > 0:
        templates = templates[:max_template_attempts]

    soft_accept_ops = {0x00B8}
    confirm_success_ops = {0x0071, 0x007C, 0x076C}
    success_observed_ops = soft_accept_ops | confirm_success_ops
    strong_chain_ack_ops = {0x00B9}
    weak_success_ops = {0x00AA, 0x0091, 0x0080, 0x0082}
    error_ops = {0x011C}
    march_ops = {0x0076, 0x0077, 0x0078, 0x007A}
    gather_confirm_ops = {0x0071, 0x007C, 0x076C}
    target_marker = struct.pack('<HH', resolved_tile_x, resolved_tile_y)

    log(
        f"Template plan mode={template_match_mode} "
        f"count={len(templates)} names={[t['name'] for t in templates]}"
    )

    all_seen_ops = []
    all_weak_ops = []
    success = False
    soft_success = False

    for idx, template in enumerate(templates, start=1):
        if idx > 1:
            try:
                gs.sendall(build_packet(0x006E, tile_pl))
            except OSError as exc:
                log(f"ERROR re-selecting tile before retry #{idx} failed: {exc}")
                return False, resolved_tile_x, resolved_tile_y, False
            log(f"Re-sent 0x006E before retry #{idx} tile=({resolved_tile_x},{resolved_tile_y})")
            time.sleep(0.2)

        gather_plain, template_name = build_gather_from_template(
            template=template,
            tile_x=resolved_tile_x,
            tile_y=resolved_tile_y,
            hero_id=hero_id,
            march_slot=march_slot,
            kingdom=kingdom,
        )
        pkt = codec.encode(0x0CE8, gather_plain)
        try:
            gs.sendall(pkt)
        except OSError as exc:
            log(f"ERROR sending 0x0CE8 attempt={idx} failed: {exc}")
            return False, resolved_tile_x, resolved_tile_y, False
        log(
            f"Sent 0x0CE8 attempt={idx}/{len(templates)} "
            f"template={template_name}: {gather_plain.hex()}"
        )
        log(
            f"  march_slot={march_slot} tile=({resolved_tile_x},{resolved_tile_y}) "
            f"hero={hero_id} troops={len(troop_ids)}"
        )
        if send_post_0ce8_heartbeat:
            if post_0ce8_heartbeat_delay > 0:
                time.sleep(post_0ce8_heartbeat_delay)
            try:
                hb_ms = int(time.monotonic() * 1000) & 0xFFFFFFFF
                gs.sendall(build_heartbeat(hb_ms))
                log(f"Sent post-0x0CE8 heartbeat 0x0042 ms={hb_ms}")
            except OSError as exc:
                log(f"ERROR sending post-0x0CE8 heartbeat failed: {exc}")
                return False, resolved_tile_x, resolved_tile_y, False

        attempt_seen = []
        attempt_weak = []
        attempt_confirm = []
        attempt_soft = False
        attempt_ack = False
        attempt_chain_promoted = False
        march_seen_count = 0
        march_target_match = False
        attempt_error = False
        deadline = time.time() + template_wait_seconds
        while time.time() < deadline:
            pkt = reader.read_one(1.0)
            if pkt is None:
                continue
            op, pl, _ = pkt
            if op in success_observed_ops:
                attempt_seen.append(op)
                if op in soft_accept_ops:
                    log(f"SOFT 0x{op:04X} ({len(pl)}B) payload={pl.hex()[:60]}")
                    attempt_soft = True
                    log("NOTE 0x00B8 seen; waiting for confirm ops (0x0071/0x076C/0x007C) with target match.")
                else:
                    log(f"SUCCESS 0x{op:04X} ({len(pl)}B) payload={pl.hex()[:60]}")
                    if op == 0x007C or (op in gather_confirm_ops and target_marker in pl):
                        attempt_confirm.append(op)
                        log(
                            f"CONFIRM gather-target match via 0x{op:04X} "
                            f"tile=({resolved_tile_x},{resolved_tile_y})"
                        )
            elif op in weak_success_ops:
                log(f"WEAK 0x{op:04X} ({len(pl)}B) payload={pl.hex()[:60]}")
                attempt_weak.append(op)
                attempt_seen.append(op)
            elif op in error_ops:
                err = struct.unpack('<I', pl[:4])[0] if len(pl) >= 4 else -1
                log(f"ERROR 0x{op:04X} code={err}")
                attempt_seen.append(op)
                attempt_error = True
                break
            elif op in march_ops:
                log(f"MARCH 0x{op:04X} ({len(pl)}B) payload={pl.hex()[:80]}")
                attempt_seen.append(op)
                march_seen_count += 1
                if target_marker in pl:
                    march_target_match = True
            elif op in strong_chain_ack_ops:
                log(f"ACK 0x{op:04X} ({len(pl)}B) payload={pl.hex()[:60]}")
                attempt_seen.append(op)
                attempt_ack = True
            elif op == 0x099E:
                log(f"  Troop confirm 0x099E: {pl.hex()}")
                attempt_seen.append(op)
            elif op not in (0x0042, 0x0002, 0x036C):
                log(f"  Recv 0x{op:04X} ({len(pl)}B) payload={pl.hex()[:60]}")
                attempt_seen.append(op)

            if attempt_confirm:
                success = True
                break
            # Some real gather sessions return 0x00B8 + 0x00B9 without
            # 0x0071/0x076C/0x007C in the same short window. Only promote this
            # chain when we also observe post-send march traffic that matches
            # the selected target tile.
            if (
                not attempt_chain_promoted
                and attempt_soft
                and attempt_ack
                and march_seen_count > 0
                and march_target_match
                and not attempt_error
            ):
                attempt_chain_promoted = True
                success = True
                log(
                    "CONFIRM strong accept via chain 0x00B8 + 0x00B9 "
                    f"(march_seen={march_seen_count} march_target_match={march_target_match})"
                )
                break

        all_seen_ops.extend(attempt_seen)
        all_weak_ops.extend(attempt_weak)
        soft_success = soft_success or attempt_soft
        attempt_success = bool(attempt_confirm) or attempt_chain_promoted
        log(
            f"Attempt {idx} result: success={attempt_success} "
            f"error={attempt_error} strong_seen={[f'0x{op:04X}' for op in attempt_seen if op in confirm_success_ops]} "
            f"ack_seen={[f'0x{op:04X}' for op in attempt_seen if op in strong_chain_ack_ops]} "
            f"confirm_seen={[f'0x{op:04X}' for op in attempt_confirm]} "
            f"chain_promoted={attempt_chain_promoted} "
            f"soft_00b8={attempt_soft} "
            f"weak_seen={[f'0x{op:04X}' for op in attempt_weak]}"
        )

        if success:
            break
        time.sleep(0.2)

    log(
        f"Result: success={success} "
        f"soft_00b8={soft_success} "
        f"strong_seen={[f'0x{op:04X}' for op in all_seen_ops if op in confirm_success_ops]} "
        f"weak_seen={[f'0x{op:04X}' for op in all_weak_ops]}"
    )
    return success, resolved_tile_x, resolved_tile_y, soft_success


def main():
    global LOG_FILE
    
    parser = argparse.ArgumentParser(description="Gather Bot v3 - correct protocol")
    parser.add_argument('--hero', type=int, default=255, help='Hero ID')
    parser.add_argument('--slot', type=int, default=1, help='March slot (strict: 1..3)')
    parser.add_argument(
        '--slot-fallbacks',
        type=str,
        default='',
        help='Optional comma-separated fallback march slots to try after --slot (strict: 1..3, example: 2,3).',
    )
    parser.add_argument('--resource', type=int, default=1, 
                        help='Resource type: 1=wheat 2=stone 3=wood 4=ore 5=gold')
    parser.add_argument('--level', type=int, default=1, help='Resource level (templates validated mainly for 1-2)')
    parser.add_argument('--kingdom', type=int, default=182, help='Kingdom number')
    parser.add_argument(
        '--allow-template-fallback',
        action='store_true',
        help='Allow hero/level fallback template selection (disabled by default to avoid guesswork).',
    )
    parser.add_argument(
        '--max-template-attempts',
        type=int,
        default=0,
        help='Max number of template attempts per gather (0 = all matching templates).',
    )
    parser.add_argument(
        '--template-name',
        type=str,
        default='',
        help='Force a single template by name (example: hero255_lvl1_cap_22mar).',
    )
    parser.add_argument(
        '--template-wait-seconds',
        type=float,
        default=12.0,
        help='Seconds to wait for strong/weak responses after each template send.',
    )
    parser.add_argument(
        '--send-hero-select',
        action='store_true',
        help='Send 0x0323 hero select before 0x0CE8 attempts.',
    )
    parser.add_argument(
        '--send-ready-sig',
        action='store_true',
        help='Send 0x01D6 ready signal after target selection and before pre-0x0CE8 heartbeat.',
    )
    parser.add_argument(
        '--ready-sig-wait',
        type=float,
        default=0.6,
        help='Seconds to drain/log replies after sending 0x01D6 ready signal.',
    )
    parser.add_argument(
        '--skip-ui-setup',
        action='store_true',
        help='Skip 0x0840/0x0245/0x0834 setup and use a leaner gather flow.',
    )
    parser.add_argument(
        '--send-source-first',
        action='store_true',
        help='Send source 0x006E after 0x0CEB prelude (matches latest successful capture).',
    )
    parser.add_argument(
        '--send-0840',
        action='store_true',
        help='Include 0x0840 in setup phase (disabled by default for search-capture parity).',
    )
    parser.add_argument('--source-x', type=int, default=653, help='Source tile X for --send-source-first.')
    parser.add_argument('--source-y', type=int, default=567, help='Source tile Y for --send-source-first.')
    parser.add_argument(
        '--send-setup-extras',
        action='store_true',
        help='With full setup, also send 0x0709 + 0x0A2C + 0x17A3 before 0x0CEB.',
    )
    parser.add_argument(
        '--setup-no-17a3',
        action='store_true',
        help='When using --send-setup-extras, omit 0x17A3 and only send 0x0709 + 0x0A2C.',
    )
    parser.add_argument(
        '--send-1b8b',
        type=str,
        default='',
        help='Optional hex payload for 0x1B8B in full setup mode.',
    )
    parser.add_argument(
        '--send-1b8b-structured',
        action='store_true',
        help='Build 0x1B8B from the PCAP-derived plaintext structure and encode it with the current session codec.',
    )
    parser.add_argument(
        '--send-1b8b-seed32',
        type=lambda value: int(value, 0),
        default=None,
        help='Optional seed32 for --send-1b8b-structured (example: 0x67E1CE66). Random if omitted.',
    )
    parser.add_argument(
        '--send-1b8b-seed-label',
        type=str,
        default='',
        help='Resolve the 1B8B seed from the current session candidate list by label (example: session_head_le).',
    )
    parser.add_argument(
        '--prelude-after-troops',
        action='store_true',
        help='Send 0x099D/0x0767/0x0769 before 0x0CEB (alternate observed successful order).',
    )
    parser.add_argument(
        '--send-setup-target-select',
        action='store_true',
        help='Legacy mode: send target 0x006E inside setup before 0x0245/0x0834.',
    )
    parser.add_argument(
        '--preselect-target',
        action='store_true',
        help='Send one extra target 0x006E before do_gather flow starts.',
    )
    parser.add_argument(
        '--auto-search-sync-first',
        action='store_true',
        help='For auto-search runs, force the old strong-baseline order: troops -> sync -> prelude -> source.',
    )
    parser.add_argument(
        '--setup-recv-window',
        type=float,
        default=0.0,
        help='Additional setup read/drain window in seconds. If > 0, keep reading setup replies through empty reads until the window expires.',
    )
    parser.add_argument(
        '--send-pre-0ce8-heartbeat',
        action='store_true',
        help='Send 0x0042 heartbeat right before 0x0CE8 and wait briefly for echo.',
    )
    parser.add_argument(
        '--pre-0ce8-heartbeat-wait',
        type=float,
        default=1.0,
        help='Seconds to wait for pre-0x0CE8 heartbeat echo/traffic.',
    )
    parser.add_argument(
        '--send-post-0ce8-heartbeat',
        action='store_true',
        help='Send one 0x0042 heartbeat immediately after each 0x0CE8 send.',
    )
    parser.add_argument(
        '--post-0ce8-heartbeat-delay',
        type=float,
        default=0.0,
        help='Optional delay before sending post-0x0CE8 heartbeat (seconds).',
    )
    parser.add_argument(
        '--troops',
        type=str,
        default='',
        help='Comma-separated 0x099D troop IDs override (example: 403,405,406,407,411).',
    )
    parser.add_argument(
        '--allow-repeat-target',
        action='store_true',
        help='Allow auto-search to reuse recently used tiles (disabled by default).',
    )
    parser.add_argument(
        '--recent-tiles-file',
        type=str,
        default=str(Path(__file__).with_name('gather_recent_tiles.json')),
        help='Path to JSON cache for recent target tiles.',
    )
    parser.add_argument(
        '--recent-tiles-ttl-minutes',
        type=float,
        default=180.0,
        help='How long a used tile remains blocked for auto-search.',
    )
    parser.add_argument(
        '--recent-tiles-max',
        type=int,
        default=200,
        help='Max number of recent tiles kept in cache.',
    )
    parser.add_argument(
        '--max-search-attempts',
        type=int,
        default=8,
        help='Max auto-search retries to avoid repeated recent tiles.',
    )
    parser.add_argument(
        '--search-retry-delay',
        type=float,
        default=0.3,
        help='Delay between repeated search attempts (seconds).',
    )
    parser.add_argument(
        '--clear-recent-tiles',
        action='store_true',
        help='Clear recent-tiles cache at startup.',
    )
    parser.add_argument('--target-x', type=int, default=None, help='Override target tile X (skip 0x033E search).')
    parser.add_argument('--target-y', type=int, default=None, help='Override target tile Y (skip 0x033E search).')
    parser.add_argument(
        '--working-profile',
        action='store_true',
        help='Enable the current baseline flag bundle (0x0840 + setup extras + prelude-after-troops + source-first + pre-0x0CE8 heartbeat + auto-search sync-first order). Does not override heartbeat wait or slot fallbacks.',
    )
    parser.add_argument(
        '--accept-soft-00b8',
        action='store_true',
        help='Legacy mode: treat 0x00B8-only acceptance as provisional success (strict mode should keep this OFF).',
    )
    parser.add_argument(
        '--log-session-candidates',
        action='store_true',
        help='Log deterministic 1B8B seed candidates derived from the current 0x0022/0x1B8A session state.',
    )
    args = parser.parse_args()

    if args.working_profile:
        # Match the previously validated baseline flag bundle:
        # 0x0840 + setup extras + 5 troops + prelude-after-troops + source-first + pre-0CE8 heartbeat.
        # Intentionally leaves heartbeat wait and slot fallbacks to the explicit CLI/default values.
        args.send_0840 = True
        args.send_setup_extras = True
        args.prelude_after_troops = True
        args.send_source_first = True
        args.send_pre_0ce8_heartbeat = True
        args.auto_search_sync_first = True

    if args.slot < 1 or args.slot > 3:
        log(f"ERROR invalid --slot value: {args.slot}. Strict mode expects 1..3.")
        return

    if args.accept_soft_00b8:
        log("WARNING --accept-soft-00b8 is enabled; this weakens strict gather validation.")
    
    troop_ids = DEFAULT_TROOPS
    if args.troops.strip():
        try:
            troop_ids = parse_troop_ids(args.troops)
        except ValueError:
            log(f"ERROR invalid --troops value: {args.troops!r}")
            return
    if not troop_ids:
        log("ERROR troop list is empty; use at least one troop id")
        return

    slot_plan = [args.slot]
    if args.slot_fallbacks.strip():
        try:
            slot_plan.extend(parse_slot_ids(args.slot_fallbacks))
        except ValueError as exc:
            log(f"ERROR invalid --slot-fallbacks value: {exc}")
            return
    unique_slot_plan = []
    seen_slots = set()
    for slot in slot_plan:
        if slot not in seen_slots:
            unique_slot_plan.append(slot)
            seen_slots.add(slot)
    slot_plan = unique_slot_plan

    LOG_FILE = str(Path(__file__).parent / f"gather_v3_{time.strftime('%Y%m%d_%H%M%S')}.log")
    
    log("=" * 60)
    log("GATHER BOT v3 - Correct Protocol")
    log("=" * 60)
    log(
        f"hero={args.hero} slot={args.slot} resource_type={args.resource} level={args.level} "
        f"kingdom={args.kingdom} max_template_attempts={args.max_template_attempts} "
        f"template_name={args.template_name or 'auto'} "
        f"template_wait_seconds={args.template_wait_seconds} send_hero_select={args.send_hero_select} "
        f"send_ready_sig={args.send_ready_sig} ready_sig_wait={args.ready_sig_wait} "
        f"skip_ui_setup={args.skip_ui_setup} send_source_first={args.send_source_first} "
        f"send_0840={args.send_0840} "
        f"target_override=({args.target_x},{args.target_y}) troops={troop_ids} "
        f"slot_plan={slot_plan} accept_soft_00b8={args.accept_soft_00b8} "
        f"allow_repeat_target={args.allow_repeat_target} max_search_attempts={args.max_search_attempts} "
        f"recent_ttl_minutes={args.recent_tiles_ttl_minutes} "
        f"send_setup_extras={args.send_setup_extras} "
        f"send_1b8b={'structured' if args.send_1b8b_structured else ('raw' if args.send_1b8b else 'no')} "
        f"send_1b8b_seed32={f'0x{args.send_1b8b_seed32:08X}' if args.send_1b8b_seed32 is not None else '-'} "
        f"prelude_after_troops={args.prelude_after_troops} "
        f"send_setup_target_select={args.send_setup_target_select} "
        f"preselect_target={args.preselect_target} "
        f"working_profile={args.working_profile} "
        f"send_pre_0ce8_heartbeat={args.send_pre_0ce8_heartbeat} "
        f"pre_0ce8_heartbeat_wait={args.pre_0ce8_heartbeat_wait} "
        f"send_post_0ce8_heartbeat={args.send_post_0ce8_heartbeat} "
        f"post_0ce8_heartbeat_delay={args.post_0ce8_heartbeat_delay}"
    )
    
    gs, reader, codec, session_ctx = connect_game(log_session_candidates=args.log_session_candidates)

    resolved_1b8b_seed32 = args.send_1b8b_seed32
    if args.send_1b8b_seed_label:
        resolved_1b8b_seed32 = resolve_1b8b_seed_from_label(session_ctx, args.send_1b8b_seed_label)
        if resolved_1b8b_seed32 is None:
            log(f"ERROR unknown --send-1b8b-seed-label: {args.send_1b8b_seed_label!r}")
            gs.close()
            return
        log(f"Resolved 1B8B seed label {args.send_1b8b_seed_label} -> 0x{resolved_1b8b_seed32:08X}")

    recent_tiles_path = Path(args.recent_tiles_file)
    if args.clear_recent_tiles and recent_tiles_path.exists():
        recent_tiles_path.unlink()
        log(f"Cleared recent tile cache: {recent_tiles_path}")
    recent_ttl_seconds = max(0.0, args.recent_tiles_ttl_minutes * 60.0)
    recent_tiles = load_recent_tiles(recent_tiles_path, recent_ttl_seconds)
    log(f"Recent tile cache loaded: {len(recent_tiles)} entries from {recent_tiles_path}")
    
    # Start heartbeat
    start_time = time.time()
    stop_evt = threading.Event()
    def hb():
        while not stop_evt.wait(15):
            try:
                ms = int((time.time() - start_time) * 1000)
                gs.sendall(build_heartbeat(ms))
            except:
                break
    threading.Thread(target=hb, daemon=True).start()
    
    if (args.target_x is None) != (args.target_y is None):
        log("ERROR: --target-x and --target-y must be provided together")
        stop_evt.set()
        gs.close()
        return

    if args.target_x is not None and args.target_y is not None:
        tile_x, tile_y = args.target_x, args.target_y
        log(f"Using target override tile=({tile_x},{tile_y})")
        if not args.allow_repeat_target and tile_key(tile_x, tile_y) in recent_tiles:
            log(f"WARNING override tile ({tile_x},{tile_y}) exists in recent cache; continuing because override was explicit.")
    else:
        tile_x, tile_y = None, None
        log("Auto-search enabled: target tile will be resolved inside gather flow")
    
    if args.preselect_target:
        if tile_x is None or tile_y is None:
            log("Ignoring --preselect-target because auto-search resolves the target later in the flow")
        else:
            select_tile(gs, reader, tile_x, tile_y)
    else:
        log("Skipping preselect 0x006E before gather flow")
    
    success = False
    soft_success = False
    auto_search_run = args.target_x is None and args.target_y is None
    for slot_index, march_slot in enumerate(slot_plan, start=1):
        if slot_index > 1:
            log(f"Retrying gather with fallback slot {march_slot} ({slot_index}/{len(slot_plan)})")
            if auto_search_run:
                tile_x, tile_y = None, None
                log("Auto-search fallback: resetting target to force a fresh search result")
        success, tile_x, tile_y, slot_soft_success = do_gather(
            gs,
            reader,
            codec,
            tile_x,
            tile_y,
            hero_id=args.hero,
            march_slot=march_slot,
            troop_ids=troop_ids,
            kingdom=args.kingdom,
            resource_level=args.level,
            allow_template_fallback=args.allow_template_fallback,
            max_template_attempts=args.max_template_attempts,
            template_wait_seconds=args.template_wait_seconds,
            template_name=args.template_name,
            send_hero_select=args.send_hero_select,
            send_ready_sig=args.send_ready_sig,
            ready_sig_wait=args.ready_sig_wait,
            skip_ui_setup=args.skip_ui_setup,
            send_source_first=args.send_source_first,
            source_x=args.source_x,
            source_y=args.source_y,
            send_0840=args.send_0840,
            send_setup_extras=args.send_setup_extras,
            send_1b8b_hex=args.send_1b8b,
            send_setup_17a3=not args.setup_no_17a3,
            send_1b8b_structured=args.send_1b8b_structured,
            send_1b8b_seed32=resolved_1b8b_seed32,
            prelude_after_troops=args.prelude_after_troops,
            send_setup_target_select=args.send_setup_target_select,
            auto_search_sync_first=args.auto_search_sync_first,
            setup_recv_window=args.setup_recv_window,
            send_pre_0ce8_heartbeat=args.send_pre_0ce8_heartbeat,
            pre_0ce8_heartbeat_wait=args.pre_0ce8_heartbeat_wait,
            send_post_0ce8_heartbeat=args.send_post_0ce8_heartbeat,
            post_0ce8_heartbeat_delay=args.post_0ce8_heartbeat_delay,
            resource_type=args.resource,
            allow_repeat_target=args.allow_repeat_target,
            recent_tiles=recent_tiles,
            max_search_attempts=args.max_search_attempts,
            search_retry_delay=args.search_retry_delay,
        )
        soft_success = soft_success or slot_soft_success
        if success:
            log(f"GATHER STARTED (strong signal) via slot {march_slot}")
            break
        if slot_soft_success:
            log(f"SOFT ACCEPT (0x00B8-only) via slot {march_slot}")
            if args.accept_soft_00b8:
                success = True
                log(f"Treating 0x00B8-only as provisional success via slot {march_slot}")
                break

    if success:
        recent_tiles[tile_key(tile_x, tile_y)] = time.time()
        try:
            save_recent_tiles(recent_tiles_path, recent_tiles, args.recent_tiles_max)
            log(f"Saved recent tile ({tile_x},{tile_y}) to cache.")
        except Exception as exc:
            log(f"WARNING failed to save recent tile cache: {exc}")
    elif soft_success:
        log("Gather got 0x00B8-only soft acceptance but no strong target confirmation.")
    else:
        log("Gather not accepted (no strong signal)")
    
    stop_evt.set()
    gs.close()
    log(f"Log: {LOG_FILE}")


if __name__ == '__main__':
    main()

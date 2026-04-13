#!/usr/bin/env python3
"""
A/B Test: Connection with vs without 0x1B8B
============================================
Test A: Skip 0x1B8B entirely → does the bot stay connected?
Test B: Send correct 0x1B8B (NewEncode, constant plaintext) → does gather work?

This resolves the root cause: is 0x1B8B causing disconnects, or is it something else?
"""
import sys, time, struct, random, subprocess, socket, os
sys.path.insert(0, r'D:\CascadeProjects\claude')

from config import IGG_ID, WORLD_ID, EMAIL, PASSWORD
from gateway import connect_gateway
from codec import CMsgCodec
from packets import build_packet, build_game_login, build_world_entry, recv_packet
from protocol import opname, OP_ENABLE_VIEW, OP_START_MARCH
from game_state import GameState

# ═══════════════════════════════════════════════════════════════
PASSWORD_CHECK_PLAIN = bytes.fromhex("ed02732200000000ffffffffffffffff")
KINGDOM = 182

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def node_login(email, password, igg_id):
    for attempt in range(3):
        try:
            result = subprocess.run(
                ['node', r'D:\CascadeProjects\lords_bot\http_login.mjs', email, password, str(igg_id)],
                capture_output=True, text=True, timeout=30
            )
            key = result.stdout.strip()
            if len(key) == 32: return key
        except Exception as e:
            log(f"  Login attempt {attempt+1} failed: {e}")
        if attempt < 2: time.sleep(3)
    return None

def recv_flood(sock, timeout=3):
    packets = []
    deadline = time.time() + timeout
    while time.time() < deadline:
        remaining = max(0.1, deadline - time.time())
        sock.settimeout(remaining)
        try:
            header = b''
            while len(header) < 4:
                chunk = sock.recv(4 - len(header))
                if not chunk: return packets
                header += chunk
            pkt_len, opcode = struct.unpack('<HH', header)
            payload_len = pkt_len - 4
            if payload_len < 0 or payload_len > 100000: return packets
            payload = b''
            while len(payload) < payload_len:
                chunk = sock.recv(payload_len - len(payload))
                if not chunk: return packets
                payload += chunk
            packets.append((opcode, payload))
        except socket.timeout: break
        except: break
    return packets

def extract_server_key(packets):
    gs = GameState()
    for op, pl in packets:
        gs.update(op, pl)
        if gs.server_key is not None: return gs.server_key
    return None

def send_heartbeat(sock, start_time):
    ms = int((time.time() - start_time) * 1000)
    try:
        sock.sendall(build_packet(0x0042, struct.pack('<II', ms, 0)))
        return True
    except:
        return False

def check_alive(sock, start_time):
    """Send heartbeat and check if we get any response."""
    if not send_heartbeat(sock, start_time):
        return False
    time.sleep(1)
    try:
        resp = recv_flood(sock, timeout=3)
        return len(resp) > 0
    except:
        return False

def run_test(mode, access_key, gw):
    """
    mode='skip' → don't send 0x1B8B
    mode='send' → send correct 0x1B8B
    """
    label = "TEST A (SKIP 0x1B8B)" if mode == 'skip' else "TEST B (SEND 0x1B8B)"
    log(f"\n{'='*70}")
    log(f"  {label}")
    log(f"{'='*70}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    try:
        sock.connect((gw['ip'], gw['port']))
    except Exception as e:
        log(f"  Connect failed: {e}")
        return {'mode': mode, 'connected': False}

    result = {
        'mode': mode,
        'connected': True,
        'login_ok': False,
        'server_key': None,
        '1b8b_sent': False,
        '1b8b_response': None,
        'alive_after_1b8b': None,
        'alive_after_setup': None,
        'gather_sent': False,
        'gather_response': None,
        'march_started': False,
        'error_codes': [],
        'disconnect_point': None,
    }

    start_time = time.time()

    # ─── Game login ───
    log("  Login...")
    sock.sendall(build_game_login(IGG_ID, gw['token']))
    r = recv_packet(sock, timeout=10)
    if r is None or r[0] != 0x0020:
        log(f"  Login failed: {r}")
        result['disconnect_point'] = 'login'
        sock.close(); return result
    result['login_ok'] = True
    log("  Login OK")

    sock.sendall(build_world_entry(IGG_ID))

    # ─── Init flood ───
    log("  Receiving init flood...")
    init_pkts = recv_flood(sock, timeout=6)
    log(f"  {len(init_pkts)} init packets")

    # Check for S2C 0x1B8A
    for op, pl in init_pkts:
        if op == 0x1B8A:
            log(f"  *** S2C 0x1B8A received ({len(pl)}B): {pl[:10].hex()}")
            if pl:
                log(f"      byte[0]=0x{pl[0]:02X} (gate candidate)")

    server_key = extract_server_key(init_pkts)
    if server_key is None:
        log("  Server key not found, requesting more data...")
        for op in [0x0840, 0x17D4, 0x0709, 0x0674, 0x0767, 0x0769]:
            sock.sendall(build_packet(op))
        time.sleep(1)
        more = recv_flood(sock, timeout=5)
        init_pkts.extend(more)
        server_key = extract_server_key(init_pkts)

    if server_key is None:
        log("  ERROR: No server key!")
        result['disconnect_point'] = 'no_server_key'
        sock.close(); return result

    result['server_key'] = f"0x{server_key:08X}"
    log(f"  Server key: 0x{server_key:08X}")
    codec = CMsgCodec.from_u32(server_key)

    # ─── Heartbeat check 1 ───
    log("  Heartbeat check...")
    alive = check_alive(sock, start_time)
    log(f"  Alive: {alive}")
    if not alive:
        result['disconnect_point'] = 'before_1b8b'
        sock.close(); return result

    # ═══════════════════════════════════════════════════════════
    # 0x1B8B decision
    # ═══════════════════════════════════════════════════════════
    if mode == 'send':
        log("  *** Sending 0x1B8B (NewEncode, correct plaintext) ***")
        extra = os.urandom(2)
        pw_pkt = codec.encode_offset6(0x1B8B, PASSWORD_CHECK_PLAIN, extra=extra)
        log(f"  Packet ({len(pw_pkt)}B): {pw_pkt.hex()}")
        sock.sendall(pw_pkt)
        result['1b8b_sent'] = True

        time.sleep(1.5)
        pw_resp = recv_flood(sock, timeout=3)
        log(f"  Response after 0x1B8B: {len(pw_resp)} packets")
        for op, pl in pw_resp:
            log(f"    {opname(op)} ({len(pl)}B)")
            if op == 0x1B8C:
                result['1b8b_response'] = f"0x1B8C ({len(pl)}B): {pl.hex()}"
                log(f"    *** 0x1B8C PASSWORD_RETURN: {pl.hex()} ***")
            if op == 0x0037:
                if len(pl) >= 12:
                    err = struct.unpack('<I', pl[8:12])[0]
                    result['error_codes'].append(f"0x0037:{err}")
                    log(f"    *** ERROR 0x0037: status={err} ***")
    else:
        log("  *** SKIPPING 0x1B8B ***")
        time.sleep(1)

    # ─── Heartbeat check 2 ───
    alive2 = check_alive(sock, start_time)
    result['alive_after_1b8b'] = alive2
    log(f"  Alive after 0x1B8B phase: {alive2}")
    if not alive2:
        result['disconnect_point'] = 'after_1b8b'
        sock.close(); return result

    # ─── Setup packets ───
    log("  Setup packets...")
    for opcode in [0x0840, 0x17D4, 0x0AF2, 0x0245, 0x0709, 0x0A2C]:
        sock.sendall(build_packet(opcode))
        time.sleep(0.2)
    time.sleep(1)
    setup_resp = recv_flood(sock, timeout=3)
    log(f"  Setup response: {len(setup_resp)} packets")

    alive3 = check_alive(sock, start_time)
    result['alive_after_setup'] = alive3
    log(f"  Alive after setup: {alive3}")
    if not alive3:
        result['disconnect_point'] = 'after_setup'
        sock.close(); return result

    # ─── Enable view ───
    log("  Enable view...")
    enable_data = bytearray(10)
    enable_data[0] = 0x01
    struct.pack_into('<I', enable_data, 1, IGG_ID)
    enable_data[9] = 0x01
    sock.sendall(codec.encode(OP_ENABLE_VIEW, bytes(enable_data)))
    time.sleep(1)
    recv_flood(sock, timeout=2)

    # ─── Search for gather target ───
    log("  Searching for resource tile...")
    sock.sendall(build_packet(0x033E, bytes.fromhex("01040003")))
    time.sleep(2)
    search_pkts = recv_flood(sock, timeout=3)
    target_x, target_y = None, None
    for op, pl in search_pkts:
        if op == 0x033F and len(pl) >= 5:
            tx = struct.unpack('<H', pl[1:3])[0]
            ty = struct.unpack('<H', pl[3:5])[0]
            if target_x is None:
                target_x, target_y = tx, ty
                log(f"  Found tile: ({tx},{ty})")
    if target_x is None:
        target_x, target_y = 644, 576
        log(f"  Using fallback tile: ({target_x},{target_y})")

    # ─── View tile ───
    sock.sendall(build_packet(0x006E, struct.pack('<HHB', target_x, target_y, 0x01)))
    time.sleep(1)
    recv_flood(sock, timeout=2)

    # ─── GATHER ───
    log(f"  *** SENDING GATHER to ({target_x},{target_y}) ***")
    gather_plain = bytearray(46)
    gather_plain[0] = 2  # march slot
    gather_plain[1:4] = os.urandom(3)
    struct.pack_into('<H', gather_plain, 4, 0x1749)  # gather type
    struct.pack_into('<H', gather_plain, 9, target_x)
    struct.pack_into('<H', gather_plain, 11, target_y)
    gather_plain[13] = 0x01
    gather_plain[14] = 244  # hero_id
    gather_plain[18] = KINGDOM & 0xFF
    gather_plain[22] = 0x04  # gather purpose
    struct.pack_into('<I', gather_plain, 33, IGG_ID)
    gather_pkt = codec.encode(OP_START_MARCH, bytes(gather_plain))
    sock.sendall(gather_pkt)
    result['gather_sent'] = True
    log(f"  Sent 0x0CE8 ({len(gather_pkt)}B)")

    # ─── Wait for gather response ───
    log("  Waiting for response (30s)...")
    end_time = time.time() + 30
    got_march = False
    while time.time() < end_time:
        pkts = recv_flood(sock, timeout=3)
        if not pkts:
            if not send_heartbeat(sock, start_time):
                result['disconnect_point'] = 'during_gather_wait'
                break
            continue

        for op, pl in pkts:
            if op == 0x0037:
                if len(pl) >= 12:
                    err = struct.unpack('<I', pl[8:12])[0]
                    result['error_codes'].append(f"0x0037:{err}")
                    log(f"    0x0037 ERROR: status={err} data={pl.hex()}")
                result['gather_response'] = f"error"
            elif op == 0x00B8:
                log(f"    0x00B8 MARCH_ACK ({len(pl)}B): {pl.hex()}")
                result['gather_response'] = f"ack"
            elif op == 0x0071:
                log(f"    *** 0x0071 MARCH_STATE! ***")
                got_march = True
                result['march_started'] = True
            elif op == 0x076C:
                log(f"    *** 0x076C MARCH_START! ***")
                got_march = True
                result['march_started'] = True
            elif op in (0x1B8A, 0x1B8B, 0x1B8C):
                log(f"    {opname(op)} ({len(pl)}B): {pl[:20].hex()}")

        if got_march:
            log("  *** MARCH DETECTED! ***")
            break

        send_heartbeat(sock, start_time)

    # ─── Final alive check ───
    try:
        alive_final = check_alive(sock, start_time)
        log(f"  Final alive: {alive_final}")
        if not alive_final and result['disconnect_point'] is None:
            result['disconnect_point'] = 'end'
    except:
        if result['disconnect_point'] is None:
            result['disconnect_point'] = 'end_exception'

    sock.close()
    return result

def main():
    log("=== A/B TEST: 0x1B8B Skip vs Send ===")
    log(f"IGG_ID: {IGG_ID}")

    # ─── Login once ───
    log("\nHTTP Login...")
    access_key = node_login(EMAIL, PASSWORD, IGG_ID)
    if not access_key:
        log("LOGIN FAILED!"); return
    log(f"Access key: {access_key[:8]}...")

    # ═══════════════════════════════════════════════════════════
    # TEST A: SKIP 0x1B8B
    # ═══════════════════════════════════════════════════════════
    gw_a = connect_gateway(IGG_ID, access_key, WORLD_ID)
    log(f"Gateway A: {gw_a['ip']}:{gw_a['port']}")
    result_a = run_test('skip', access_key, gw_a)

    time.sleep(5)  # cooldown between tests

    # ─── Re-login for test B ───
    log("\nRe-login for Test B...")
    access_key2 = node_login(EMAIL, PASSWORD, IGG_ID)
    if not access_key2:
        log("RE-LOGIN FAILED!"); return

    # ═══════════════════════════════════════════════════════════
    # TEST B: SEND 0x1B8B
    # ═══════════════════════════════════════════════════════════
    gw_b = connect_gateway(IGG_ID, access_key2, WORLD_ID)
    log(f"Gateway B: {gw_b['ip']}:{gw_b['port']}")
    result_b = run_test('send', access_key2, gw_b)

    # ═══════════════════════════════════════════════════════════
    # COMPARISON
    # ═══════════════════════════════════════════════════════════
    log(f"\n{'='*70}")
    log(f"  RESULTS COMPARISON")
    log(f"{'='*70}")
    
    for label, r in [("A (SKIP)", result_a), ("B (SEND)", result_b)]:
        log(f"\n  Test {label}:")
        log(f"    Login:           {'OK' if r['login_ok'] else 'FAIL'}")
        log(f"    Server key:      {r['server_key']}")
        log(f"    0x1B8B sent:     {r['1b8b_sent']}")
        log(f"    0x1B8B response: {r['1b8b_response']}")
        log(f"    Alive after 1B8B:{r['alive_after_1b8b']}")
        log(f"    Alive after setup:{r['alive_after_setup']}")
        log(f"    Gather sent:     {r['gather_sent']}")
        log(f"    Gather response: {r['gather_response']}")
        log(f"    March started:   {r['march_started']}")
        log(f"    Errors:          {r['error_codes']}")
        log(f"    Disconnect at:   {r['disconnect_point']}")
    
    log(f"\n{'='*70}")
    if result_a['march_started'] and not result_b['march_started']:
        log("  CONCLUSION: 0x1B8B CAUSES PROBLEMS - skip it!")
    elif result_b['march_started'] and not result_a['march_started']:
        log("  CONCLUSION: 0x1B8B IS REQUIRED for gather!")
    elif result_a['march_started'] and result_b['march_started']:
        log("  CONCLUSION: Both work - 0x1B8B is optional!")
    elif result_a['disconnect_point'] and result_b['disconnect_point']:
        log("  CONCLUSION: Both disconnect - problem is NOT 0x1B8B!")
        log(f"  A disconnects at: {result_a['disconnect_point']}")
        log(f"  B disconnects at: {result_b['disconnect_point']}")
    else:
        log("  CONCLUSION: Needs further analysis")
    log(f"{'='*70}")

if __name__ == '__main__':
    main()

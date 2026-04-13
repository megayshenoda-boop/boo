"""
Fresh Gather Bot (v2) — Lords Mobile
======================================
Uses the robust networking from COMPLETE_BOT.py and speed_train_replay_probe.py
implements the exact 46-byte gather payload found in PCAP on 24-Mar-2026.

Flow: ENABLE_VIEW -> TILE_SELECT -> START_MARCH
"""
import argparse
import time
import sys
import threading
from pathlib import Path

# Add project root to path for imports
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from COMPLETE_BOT import CMsgCodec, extract_key_from_adb, extract_server_key_from_0x0038
from speed_train_replay_probe import connect_game, heartbeat_loop, wait_for_server_key


# ═══════════════════════════════════════════
#  PAYLOAD BUILDERS (from PCAP 24-Mar-2026)
# ═══════════════════════════════════════════

def build_enable_view(igg_id: int) -> bytes:
    """0x0CEB ENABLE_VIEW (10 bytes) -> encrypted."""
    data = bytearray(10)
    data[0] = 0x01
    data[1:5] = igg_id.to_bytes(4, 'little')
    data[9] = 0x01
    return bytes(data)

def build_tile_select(x: int, y: int) -> bytes:
    """0x006E TILE_SELECT (5 bytes) -> plain."""
    data = bytearray(5)
    data[0:2] = x.to_bytes(2, 'little')
    data[2:4] = y.to_bytes(2, 'little')
    data[4] = 0x01
    return bytes(data)

def build_gather(igg_id: int, x: int, y: int, march_slot: int = 1,
                 troop_type: int = 182, troop_count: int = 4) -> bytes:
    """0x0CE8 START_MARCH (46 bytes) -> encrypted."""
    import random
    data = bytearray(46)
    
    data[0] = march_slot & 0xFF
    data[1:4] = random.randbytes(3)         # nonce
    data[4:6] = (0x1749).to_bytes(2, 'little') # march_type
    
    # [9:13] coordinates = 0x006E payload exactly
    data[9:11] = x.to_bytes(2, 'little')
    data[11:13] = y.to_bytes(2, 'little')
    data[13] = 0x01
    
    data[14] = 0xFF
    data[18:20] = troop_type.to_bytes(2, 'little')
    data[22:24] = troop_count.to_bytes(2, 'little')
    
    data[33:37] = igg_id.to_bytes(4, 'little')
    
    return bytes(data)


# ═══════════════════════════════════════════
#  BOT EXECUTION
# ═══════════════════════════════════════════

def parse_args():
    parser = argparse.ArgumentParser(description="Fresh Gather Bot")
    parser.add_argument("--igg-id", type=int, required=True, help="Your numeric IGG ID")
    parser.add_argument("--access-key", type=str, default="", help="Leave empty to auto-pull from ADB")
    parser.add_argument("--x", type=int, required=True, help="Target tile X coordinate")
    parser.add_argument("--y", type=int, required=True, help="Target tile Y coordinate")
    parser.add_argument("--slot", type=int, default=1, help="March slot (1-5)")
    parser.add_argument("--troop-type", type=int, default=182, help="Troop type ID (e.g. 182 for T1 Inf)")
    parser.add_argument("--troop-count", type=int, default=4, help="Number of troops to send")
    return parser.parse_args()


def simple_log(msg: str):
    ts = time.strftime('%H:%M:%S')
    print(f"[{ts}] {msg}")


def main():
    args = parse_args()
    
    # 1. Get access key
    access_key = args.access_key or extract_key_from_adb()
    if not access_key:
        simple_log("ERROR: Could not get access key from ADB. Is MEmu running and game open?")
        return
        
    simple_log(f"Starting gather bot for IGG ID: {args.igg_id}")
    simple_log(f"Target tile: ({args.x}, {args.y})")
    
    # 2. Connect to game
    try:
        gs, reader = connect_game(access_key, args.igg_id, simple_log)
    except Exception as e:
        simple_log(f"Connection failed: {e}")
        return
        
    # Start heartbeat
    start_time = time.time()
    stop_event = threading.Event()
    threading.Thread(
        target=heartbeat_loop,
        args=(gs, start_time, stop_event, simple_log),
        daemon=True,
    ).start()
    
    # 3. Get server key & codec
    simple_log("Waiting for game data & server key...")
    try:
        server_key = None
        packet_count = 0
        while True:
            pkt = reader.read_one(timeout=8)
            if pkt is None:
                raise RuntimeError("Timeout before receiving server key")
            opcode, payload, raw = pkt
            packet_count += 1
            if opcode == 0x0038:
                key = extract_server_key_from_0x0038(payload)
                if key:
                    server_key = key
                    simple_log(f"Server key 0x{server_key:08X} at packet #{packet_count}")
                    break

        codec = CMsgCodec.from_u32(server_key)
        simple_log(f"Encryption ready (key: 0x{server_key:08X})")
    except Exception as e:
        simple_log(f"Failed to get server key: {e}")
        stop_event.set()
        gs.close()
        return
        
    # 4. GATHER FLOW (Atomic Sequence, NO DELAYS)
    try:
        # Step A: 0x0CEB Prelude
        prelude_plain = build_enable_view(args.igg_id)
        prelude_pkt = codec.encode(0x0CEB, prelude_plain)
        gs.sendall(prelude_pkt)
        simple_log("Sent 0x0CEB prelude")
        
        # Step B: 0x006E Tile Select
        tile_plain = build_tile_select(args.x, args.y)
        tile_header = (4 + len(tile_plain)).to_bytes(2, 'little') + (0x006E).to_bytes(2, 'little')
        gs.sendall(tile_header + tile_plain)
        simple_log(f"Sent 0x006E tile select at {args.x},{args.y}")
        
        # Step C: 0x0CE8 Gather
        gather_plain = build_gather(args.igg_id, args.x, args.y, args.slot, args.troop_type, args.troop_count)
        gather_pkt = codec.encode(0x0CE8, gather_plain)
        gs.sendall(gather_pkt)
        simple_log(f"Sent 0x0CE8 gather payload")
        
        # 5. Observe responses
        interesting = {
            0x009E: "BUILDING_OPERAT_RETURN",
            0x02D1: "ACTION_CONFIRM",
            0x0033: "SYN_ATTRIBUTE_CHANGE",
            0x021C: "STATE_SYNC",
            0x022B: "RESOURCE_DEDUCT",
            0x06C4: "SOLDIER_NORMAL_PRODUCE_RETURN",
            0x06EB: "TRAINING_ENTRY",
            0x0076: "CASTLE_SYNC",
            0x0077: "MONSTER_SYNC",
            0x0078: "RESOURCE_SYNC",
            0x007A: "QUERY_MAP_RESULT",
            0x011C: "ERROR_CODE",
            0x036C: "SERVER_TICK",
            0x081C: "MARCH_UPDATE",
            0x0340: "MAP_UPDATE",
        }
        
        simple_log("Waiting 12 seconds for server responses...")
        deadline = time.time() + 12.0
        while time.time() < deadline:
            pkt = reader.read_one(timeout=max(0.1, deadline - time.time()))
            if pkt:
                opcode, p, raw = pkt
                if opcode not in (0x0042, 0x0002):
                    name = interesting.get(opcode, "UNKNOWN")
                    if opcode in interesting or opcode == 0x011C:
                        simple_log(f" <- Recv 0x{opcode:04X} {name} ({len(p)}B)")
                    # if action confirm, we reached the server
                    if opcode == 0x02D1:
                        simple_log("    !!! ACTION CONFIRMED (0x02D1) !!!")
                    elif opcode == 0x011C:
                        simple_log("    !!! ERROR CODE (0x011C) !!!")
                        if len(p) >= 4:
                            err = struct.unpack('<I', p[0:4])[0]
                            simple_log(f"    Error code: {err}")
                            
    except KeyboardInterrupt:
        simple_log("Stopped by user")
    finally:
        stop_event.set()
        gs.close()
        simple_log("Disconnected.")

if __name__ == "__main__":
    main()

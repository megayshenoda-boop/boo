"""
Frida hook to capture 0x1B8B packet and find the checksum/verify computation.

Strategy:
1. Hook send() to capture the raw 0x1B8B packet
2. Scan libgame.so for the CMsgCodec TABLE [0x58,0xef,0xd7,0x14,0xa2,0x3b,0x9c]
3. Find the encode function and dump surrounding assembly
4. Hook the encode function to see plaintext vs header bytes
"""
import frida
import sys
import time
import struct
import os
from datetime import datetime

# Try USB first, fall back to remote
REMOTE_DEVICE = "127.0.0.1:27042"
PACKAGE = "com.igg.android.conquerors"


class _TeeWriter:
    def __init__(self, *targets):
        self.targets = targets

    def write(self, data):
        for target in self.targets:
            target.write(data)
        for target in self.targets:
            target.flush()

    def flush(self):
        for target in self.targets:
            target.flush()


LOG_HANDLE = None
ORIG_STDOUT = sys.stdout
ORIG_STDERR = sys.stderr

JS_HOOK = r"""
'use strict';

function safeFindExport(moduleName, exportName) {
    try {
        var mod = Process.getModuleByName(moduleName);
        if (mod && mod.findExportByName) {
            var p = mod.findExportByName(exportName);
            if (p) return p;
        }
    } catch (e0) {}
    try {
        var mod2 = Process.getModuleByName(moduleName);
        if (mod2 && mod2.getExportByName) {
            return mod2.getExportByName(exportName);
        }
    } catch (e1) {}
    try {
        if (Module.findExportByName) {
            return Module.findExportByName(moduleName, exportName);
        }
    } catch (e2) {}
    try {
        if (Module.getExportByName) {
            return Module.getExportByName(moduleName, exportName);
        }
    } catch (e3) {}
    try {
        if (Module.findGlobalExportByName) {
            return Module.findGlobalExportByName(exportName);
        }
    } catch (e4) {}
    try {
        if (Module.getGlobalExportByName) {
            return Module.getGlobalExportByName(exportName);
        }
    } catch (e5) {}
    return null;
}

function readHex(ptr, len) {
    var hex = "";
    for (var i = 0; i < len; i++) {
        try { hex += ("0" + ptr.add(i).readU8().toString(16)).slice(-2); }
        catch(e) { break; }
    }
    return hex;
}

function readBytes(ptr, len) {
    var arr = [];
    for (var i = 0; i < len; i++) {
        try { arr.push(ptr.add(i).readU8()); }
        catch(e) { break; }
    }
    return arr;
}

function emitBacktrace(ctx) {
    var bt = Thread.backtrace(ctx, Backtracer.ACCURATE)
        .map(function(addr) {
            var mod = Process.findModuleByAddress(addr);
            if (mod) {
                return mod.name + "!0x" + addr.sub(mod.base).toInt32().toString(16);
            }
            return addr.toString();
        });
    send({ type: "1B8B_BACKTRACE", backtrace: bt });
}

function emit1b8b(pktPtr, pktLen, callLen, transport, offset, ctx) {
    var bytes = readBytes(pktPtr, pktLen);
    var msg = {
        type: "1B8B_FOUND",
        transport: transport,
        call_len: callLen,
        packet_len: pktLen,
        offset: offset,
        hex: readHex(pktPtr, Math.min(pktLen, 128))
    };

    if (pktLen >= 8) {
        msg.ck_std = bytes[4];
        msg.ml_std = bytes[5];
        msg.v_std = bytes[6];
        msg.mh_std = bytes[7];
        msg.enc_hex_std = readHex(pktPtr.add(8), pktLen - 8);
    }
    if (pktLen >= 10) {
        msg.extra0 = bytes[4];
        msg.extra1 = bytes[5];
        msg.ck_off6 = bytes[6];
        msg.ml_off6 = bytes[7];
        msg.v_off6 = bytes[8];
        msg.mh_off6 = bytes[9];
        msg.enc_hex_off6 = readHex(pktPtr.add(10), pktLen - 10);
    }

    send(msg);
    emitBacktrace(ctx);
}

var transportDebugCount = {};
var opcodeStats = {};
var opcodeStreamIndex = 0;
var opcodeStreamLogLimit = 5000;
var fdPeerMap = {};

var getpeernamePtr = safeFindExport("libc.so", "getpeername");
var ntohsPtr = safeFindExport("libc.so", "ntohs");
var getpeernameFn = null;
var ntohsFn = null;

try {
    if (getpeernamePtr) {
        getpeernameFn = new NativeFunction(getpeernamePtr, "int", ["int", "pointer", "pointer"]);
    }
} catch (e0) {}

try {
    if (ntohsPtr) {
        ntohsFn = new NativeFunction(ntohsPtr, "uint16", ["uint16"]);
    }
} catch (e1) {}

function swap16(v) {
    return ((v & 0xff) << 8) | ((v >> 8) & 0xff);
}

function parseSockaddr(ptr) {
    if (!ptr || ptr.isNull()) return null;
    try {
        var family = ptr.readU16();
        if (family === 2) {
            var p = ptr.add(2).readU16();
            var port = ntohsFn ? ntohsFn(p) : swap16(p);
            var b0 = ptr.add(4).readU8();
            var b1 = ptr.add(5).readU8();
            var b2 = ptr.add(6).readU8();
            var b3 = ptr.add(7).readU8();
            return {
                family: "AF_INET",
                port: port,
                ip: b0 + "." + b1 + "." + b2 + "." + b3
            };
        }
        if (family === 10) {
            var p6 = ptr.add(2).readU16();
            var port6 = ntohsFn ? ntohsFn(p6) : swap16(p6);
            return {
                family: "AF_INET6",
                port: port6,
                ip: "::"
            };
        }
        return {
            family: "AF_" + family,
            port: -1,
            ip: ""
        };
    } catch (e0) {
        return null;
    }
}

function getPeerInfo(fd) {
    if (!getpeernameFn || fd < 0) return null;
    try {
        var addr = Memory.alloc(128);
        var addrLen = Memory.alloc(4);
        addrLen.writeU32(128);
        var rc = getpeernameFn(fd, addr, addrLen);
        if (rc !== 0) return null;
        return parseSockaddr(addr);
    } catch (e0) {
        return null;
    }
}

function isGamePort(port) {
    return port === 7001 || port === 7002 || port === 7003;
}

function fdKey(fd) {
    return "" + fd;
}

function setFdPeer(fd, info, source) {
    if (fd < 0 || !info) return;
    if (info.port <= 0) return;
    fdPeerMap[fdKey(fd)] = {
        family: info.family,
        ip: info.ip,
        port: info.port,
        source: source
    };
}

function getFdPeer(fd) {
    return fdPeerMap[fdKey(fd)] || null;
}

function clearFdPeer(fd) {
    try {
        delete fdPeerMap[fdKey(fd)];
    } catch (e0) {}
}

function opcodeHex(opcode) {
    return "0x" + ("0000" + opcode.toString(16)).slice(-4);
}

function noteOpcode(transport, opcode, pktLen, off, callLen, pktPtr, peerPort) {
    var key = opcodeHex(opcode);
    opcodeStats[key] = (opcodeStats[key] || 0) + 1;
    opcodeStreamIndex += 1;

    if (opcodeStats[key] === 1) {
        send({
            type: "opcode_new",
            transport: transport,
            peer_port: peerPort,
            opcode: key,
            packet_len: pktLen,
            offset: off,
            call_len: callLen,
            hex: readHex(pktPtr, Math.min(pktLen, 40))
        });
    }

    if (opcodeStreamIndex <= opcodeStreamLogLimit) {
        send({
            type: "opcode_pkt",
            idx: opcodeStreamIndex,
            transport: transport,
            peer_port: peerPort,
            opcode: key,
            packet_len: pktLen,
            offset: off,
            call_len: callLen,
            count: opcodeStats[key],
            hex: readHex(pktPtr, Math.min(pktLen, 40))
        });
    }

    if (opcodeStreamIndex % 100 === 0) {
        send({
            type: "opcode_progress",
            total: opcodeStreamIndex,
            unique: Object.keys(opcodeStats).length
        });
    }
}

// ========== PART 0: Track socket -> peer mapping ==========
var connectPtr = safeFindExport("libc.so", "connect");
if (connectPtr) {
    Interceptor.attach(connectPtr, {
        onEnter: function(args) {
            this.fd = -1;
            this.addr = null;
            try {
                this.fd = args[0].toInt32();
                this.addr = parseSockaddr(args[1]);
                if (this.addr && (this.addr.port === 7001 || this.addr.port === 7002 || this.addr.port === 7003)) {
                    send({
                        type: "fd_connect_attempt",
                        fd: this.fd,
                        peer: this.addr
                    });
                }
            } catch (e0) {}
        },
        onLeave: function(retval) {
            try {
                var rc = retval.toInt32();
                if (rc === 0 && this.fd >= 0 && this.addr) {
                    setFdPeer(this.fd, this.addr, "connect");
                    if (this.addr.port === 7001 || this.addr.port === 7002 || this.addr.port === 7003) {
                        send({
                            type: "fd_connect_ok",
                            fd: this.fd,
                            peer: this.addr
                        });
                    }
                }
            } catch (e1) {}
        }
    });
}

var closePtr = safeFindExport("libc.so", "close");
if (closePtr) {
    Interceptor.attach(closePtr, {
        onEnter: function(args) {
            try {
                var fd = args[0].toInt32();
                var peer = getFdPeer(fd);
                if (peer && isGamePort(peer.port)) {
                    send({
                        type: "fd_close",
                        fd: fd,
                        peer: peer
                    });
                }
                clearFdPeer(fd);
            } catch (e0) {}
        }
    });
}

// ========== PART 1: Hook transport send funcs to capture 0x1B8B ==========
function attachTransport(moduleName, name, bufIndex, lenIndex, fdIndex, sockaddrIndex) {
    var ptr = safeFindExport(moduleName, name);
    if (!ptr) return false;

    Interceptor.attach(ptr, {
        onEnter: function(args) {
            var len = 0;
            var buf = null;
            var fd = -1;
            var peer = null;
            var dest = null;
            var mapped = null;
            var peerPort = -1;
            var likelyGame = false;
            try {
                len = args[lenIndex].toInt32();
                buf = args[bufIndex];
            } catch (e0) {
                return;
            }

            try {
                if (fdIndex !== undefined && fdIndex >= 0) {
                    fd = args[fdIndex].toInt32();
                    peer = getPeerInfo(fd);
                }
            } catch (eFd) {}

            try {
                if (sockaddrIndex !== undefined && sockaddrIndex >= 0) {
                    dest = parseSockaddr(args[sockaddrIndex]);
                }
            } catch (eSa) {}

            try {
                if (fd >= 0) {
                    mapped = getFdPeer(fd);
                }
            } catch (eMap) {}

            if (fd >= 0 && dest && dest.port > 0) {
                setFdPeer(fd, dest, "sendto");
                mapped = getFdPeer(fd);
            }

            if (dest && dest.port > 0) {
                peerPort = dest.port;
            } else if (peer && peer.port > 0) {
                peerPort = peer.port;
            } else if (mapped && mapped.port > 0) {
                peerPort = mapped.port;
            }
            likelyGame = isGamePort(peerPort);
            var knownNonGame = (peerPort > 0 && !likelyGame);

            if (!buf || len < 4 || len > 65536) return;

            try {
                transportDebugCount[name] = (transportDebugCount[name] || 0) + 1;
                var shouldLogCall =
                    transportDebugCount[name] <= 200 ||
                    likelyGame ||
                    len >= 64 ||
                    name === "send" ||
                    name === "sendto";
                if (shouldLogCall) {
                    send({
                        type: "transport_call",
                        transport: name,
                        call_index: transportDebugCount[name],
                        fd: fd,
                        peer_port: peerPort,
                        likely_game: likelyGame,
                        peer: peer,
                        dest: dest,
                        mapped_peer: mapped,
                        len: len,
                        head: readHex(buf, Math.min(24, len))
                    });
                }

                // For plain write(), skip only known non-game sockets.
                // If peer port is unknown (-1), still parse so we don't miss world traffic.
                if (name === "write" && knownNonGame) {
                    return;
                }

                var off = 0;
                var saw1b8b = false;

                // Parse one send buffer as a stream of game packets.
                while (off + 4 <= len) {
                    var pktLen = buf.add(off).readU16();
                    var opcode = buf.add(off + 2).readU16();
                    if (pktLen < 4 || pktLen > 65535) break;
                    if (off + pktLen > len) break;

                    noteOpcode(name, opcode, pktLen, off, len, buf.add(off), peerPort);

                    if ((opcode >= 0x0CE0 && opcode <= 0x0CF0) || opcode === 0x1B8B || opcode === 0x0023 || opcode === 0x0021 || opcode === 0x001F) {
                        send({
                            type: "encrypted_pkt",
                            transport: name,
                            opcode: opcodeHex(opcode),
                            call_len: len,
                            packet_len: pktLen,
                            offset: off,
                            hex: readHex(buf.add(off), Math.min(pktLen, 80))
                        });
                    }

                    if (opcode === 0x1B8B) {
                        if (name === "write" && knownNonGame) {
                            off += pktLen;
                            continue;
                        }
                        saw1b8b = true;
                        emit1b8b(buf.add(off), pktLen, len, name, off, this.context);
                    }

                    off += pktLen;
                }

                // Fallback: scan for 0x1B8B signature with any plausible packet length
                // in case stream is wrapped/chunked and normal packet walking fails.
                if (!saw1b8b) {
                    for (var pos = 0; pos + 4 <= len; pos++) {
                        if (buf.add(pos + 2).readU8() === 0x8b &&
                            buf.add(pos + 3).readU8() === 0x1b) {
                            var sigLen = buf.add(pos).readU16();
                            if (sigLen >= 4 && sigLen <= 1024 && pos + sigLen <= len) {
                                if (name === "write" && knownNonGame) {
                                    continue;
                                }
                                saw1b8b = true;
                                emit1b8b(buf.add(pos), sigLen, len, name + ":sig", pos, this.context);
                            }
                        }
                    }
                }
            } catch(e1) {
                if ((transportDebugCount[name] || 0) <= 200 || likelyGame || len >= 64 || name === "send" || name === "sendto") {
                    send({
                        type: "transport_parse_error",
                        transport: name,
                        err: "" + e1
                    });
                }
            }
        }
    });
    return true;
}

var hooked = [];
[
    ["libc.so", "send", 1, 2, 0, -1],
    ["libc.so", "sendto", 1, 2, 0, 4],
    ["libc.so", "write", 1, 2, 0, -1],
    ["libssl.so", "SSL_write", 1, 2, -1, -1]
].forEach(function(spec) {
    if (attachTransport(spec[0], spec[1], spec[2], spec[3], spec[4], spec[5])) {
        hooked.push(spec[0] + "::" + spec[1]);
    }
});

if (hooked.length > 0) {
    send({type: "info", msg: "Hooked transport funcs: " + hooked.join(", ")});
} else {
    send({type: "info", msg: "No transport exports hooked (libc send/sendto/write, libssl SSL_write)"});
}

// ========== PART 2: Find CMsgCodec TABLE in libgame.so ==========
var libgame = Process.findModuleByName("libgame.so");
if (!libgame) {
    // Try alternative names
    var mods = Process.enumerateModules();
    for (var i = 0; i < mods.length; i++) {
        if (mods[i].name.indexOf("game") !== -1 || mods[i].name.indexOf("igg") !== -1) {
            send({type: "info", msg: "Found module: " + mods[i].name + " at " + mods[i].base + " size=" + mods[i].size});
        }
    }
}

if (libgame) {
    send({type: "info", msg: "libgame.so at " + libgame.base + " size=" + libgame.size});

    // Search for TABLE pattern: 58 ef d7 14 a2 3b 9c
    var tablePattern = "58 ef d7 14 a2 3b 9c";
    try {
        var matches = Memory.scanSync(libgame.base, libgame.size, tablePattern);
        send({type: "info", msg: "TABLE pattern matches: " + matches.length});

        for (var m = 0; m < matches.length; m++) {
            var addr = matches[m].address;
            var offset = addr.sub(libgame.base).toInt32();
            send({type: "table_found", addr: addr.toString(), offset: "0x" + offset.toString(16)});

            // Dump 32 bytes around the match for context
            send({type: "info", msg: "TABLE context: " + readHex(addr.sub(8), 48)});
        }
    } catch(e) {
        send({type: "info", msg: "TABLE scan error: " + e});
    }

    // Search for 0xB7 constant (verify XOR mask) near encode logic
    // In ARM64, 0xB7 might appear as an immediate in EOR instruction
    var b7Pattern = "b7 00 00 00";  // Little-endian 0xB7
    try {
        var b7matches = Memory.scanSync(libgame.base, libgame.size, b7Pattern);
        send({type: "info", msg: "0xB7 constant matches: " + b7matches.length});
        // Only show first 10
        for (var i = 0; i < Math.min(b7matches.length, 10); i++) {
            var off = b7matches[i].address.sub(libgame.base).toInt32();
            send({type: "info", msg: "  0xB7 at offset 0x" + off.toString(16) +
                  " ctx=" + readHex(b7matches[i].address.sub(16), 48)});
        }
    } catch(e) {}

    // Search for the multiply-by-17 pattern
    // ARM64: MUL or MADD with immediate 17 (0x11)
    // This is commonly: MOV Wn, #17; MUL Wd, Wm, Wn
    // Or encoded as LSL + ADD: (x << 4) + x = x * 17

    // Search for opcode 0x1B8B as a constant (7051 decimal, or 0x8B1B in LE)
    var op1b8b = "8b 1b";
    try {
        var opmatches = Memory.scanSync(libgame.base, libgame.size, op1b8b);
        send({type: "info", msg: "0x1B8B opcode constant matches: " + opmatches.length});
        // Show first 20 - one of these might be a CMP instruction
        for (var i = 0; i < Math.min(opmatches.length, 20); i++) {
            var off = opmatches[i].address.sub(libgame.base).toInt32();
            send({type: "info", msg: "  0x1B8B at 0x" + off.toString(16) +
                  " ctx=" + readHex(opmatches[i].address.sub(8), 32)});
        }
    } catch(e) {}
}

// ========== PART 3: Backtrace is emitted directly from transport hooks ==========

send({type: "info", msg: "=== ALL HOOKS READY ==="});
send({type: "info", msg: "Now log in to the game. 0x1B8B is sent during login sequence."});
send({type: "info", msg: "We need to capture: checksum formula + verify formula"});
"""

captured_1b8b = []
opcode_stats = {}
opcode_order = []


def is_target_process_name(name: str) -> bool:
    low = (name or "").lower()
    return "igg" in low or "conquerors" in low or "lords" in low


def find_latest_target_process(device):
    candidates = [proc for proc in device.enumerate_processes() if is_target_process_name(proc.name)]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.pid)


def attach_hook_script(device, pid: int, attached_sessions: dict) -> bool:
    if pid in attached_sessions:
        return False

    try:
        session = device.attach(pid)
    except Exception as exc:
        print(f"[WARN] Failed to attach PID {pid}: {exc}")
        return False

    try:
        script = session.create_script(JS_HOOK)
        script.on("message", on_message)
        script.load()
        attached_sessions[pid] = session
        print(f"[*] Attached to PID {pid}")
        return True
    except Exception as exc:
        print(f"[WARN] Failed to load script on PID {pid}: {exc}")
        try:
            session.detach()
        except Exception:
            pass
        return False

def on_message(msg, data):
    if msg["type"] == "send":
        p = msg["payload"]
        t = p.get("type", "")

        if t == "info":
            print(f"[INFO] {p['msg']}")
        elif t == "1B8B_FOUND":
            print(f"\n{'#'*70}")
            print(
                "  *** 0x1B8B CAPTURED! "
                f"transport={p.get('transport')} call_len={p.get('call_len')} "
                f"packet_len={p.get('packet_len')} offset={p.get('offset')} ***"
            )
            print(f"  Full hex: {p['hex']}")
            if all(k in p for k in ("ck_std", "ml_std", "v_std", "mh_std")):
                print(
                    "  std-header "
                    f"ck=0x{p['ck_std']:02X} ml=0x{p['ml_std']:02X} "
                    f"v=0x{p['v_std']:02X} mh=0x{p['mh_std']:02X} "
                    f"v^ml=0x{(p['v_std'] ^ p['ml_std']):02X}"
                )
                if "enc_hex_std" in p:
                    print(f"  enc_std: {p['enc_hex_std']}")
            if all(k in p for k in ("extra0", "extra1", "ck_off6", "ml_off6", "v_off6", "mh_off6")):
                print(
                    "  off6-header "
                    f"extra={p['extra0']:02X}{p['extra1']:02X} "
                    f"ck=0x{p['ck_off6']:02X} ml=0x{p['ml_off6']:02X} "
                    f"v=0x{p['v_off6']:02X} mh=0x{p['mh_off6']:02X} "
                    f"ml^0xB7=0x{(p['ml_off6'] ^ 0xB7):02X}"
                )
                if "enc_hex_off6" in p:
                    print(f"  enc_off6: {p['enc_hex_off6']}")
            print(f"{'#'*70}\n")
            captured_1b8b.append(p)
        elif t == "1B8B_BACKTRACE":
            print(f"\n{'='*70}")
            print("  0x1B8B CALL BACKTRACE:")
            for frame in p['backtrace']:
                print(f"    {frame}")
            print(f"{'='*70}\n")
        elif t == "encrypted_pkt":
            pkt_len = p.get("packet_len", p.get("len", "?"))
            off = p.get("offset", "?")
            tr = p.get("transport", "?")
            print(f"[ENC] {p['opcode']} pkt={pkt_len} off={off} via={tr}: {p['hex'][:60]}...")
        elif t == "transport_call":
            print(
                f"[TX] via={p.get('transport')} idx={p.get('call_index')} "
                f"fd={p.get('fd')} peer_port={p.get('peer_port')} "
                f"game={p.get('likely_game')} len={p.get('len')} head={p.get('head')}"
            )
        elif t == "transport_parse_error":
            print(f"[TX_ERR] via={p.get('transport')} err={p.get('err')}")
        elif t == "fd_connect_attempt":
            peer = p.get("peer") or {}
            print(
                f"[FD_CONNECT] attempt fd={p.get('fd')} "
                f"{peer.get('ip')}:{peer.get('port')} {peer.get('family')}"
            )
        elif t == "fd_connect_ok":
            peer = p.get("peer") or {}
            print(
                f"[FD_CONNECT] ok fd={p.get('fd')} "
                f"{peer.get('ip')}:{peer.get('port')} {peer.get('family')}"
            )
        elif t == "fd_close":
            peer = p.get("peer") or {}
            print(
                f"[FD_CLOSE] fd={p.get('fd')} "
                f"{peer.get('ip')}:{peer.get('port')}"
            )
        elif t == "opcode_new":
            op = p.get("opcode", "?")
            opcode_stats.setdefault(op, 0)
            if op not in opcode_order:
                opcode_order.append(op)
            print(
                f"[NEW_OP] {op} via={p.get('transport')} "
                f"peer_port={p.get('peer_port')} "
                f"pkt={p.get('packet_len')} off={p.get('offset')} "
                f"hex={p.get('hex')}"
            )
        elif t == "opcode_pkt":
            op = p.get("opcode", "?")
            count = p.get("count", 0)
            opcode_stats[op] = max(opcode_stats.get(op, 0), count)
            if op not in opcode_order:
                opcode_order.append(op)
            print(
                f"[OP] #{p.get('idx')} {op} via={p.get('transport')} "
                f"peer_port={p.get('peer_port')} "
                f"pkt={p.get('packet_len')} off={p.get('offset')} n={count}"
            )
        elif t == "opcode_progress":
            print(
                f"[OP_PROGRESS] total={p.get('total')} "
                f"unique={p.get('unique')}"
            )
        elif t == "table_found":
            print(f"\n*** TABLE found at {p['addr']} (offset {p['offset']}) ***\n")
        else:
            print(f"[{t}] {p}")
    elif msg["type"] == "error":
        print(f"[ERROR] {msg.get('description', msg)}")


def main():
    global LOG_HANDLE

    args = sys.argv[1:]
    spawn_mode = False
    no_wait = False
    stop_on_ctrl_c = False
    pid = None
    log_file_path = None

    idx = 0
    while idx < len(args):
        arg = args[idx]
        if arg == "--spawn":
            spawn_mode = True
        elif arg == "--no-wait":
            no_wait = True
        elif arg == "--stop-on-ctrl-c":
            stop_on_ctrl_c = True
        elif arg.startswith("--log-file="):
            log_file_path = arg.split("=", 1)[1].strip()
        elif arg == "--log-file" and idx + 1 < len(args):
            log_file_path = args[idx + 1].strip()
            idx += 1
        elif arg.isdigit():
            pid = int(arg)
        idx += 1

    if not log_file_path:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"frida_1b8b_{stamp}.log")

    try:
        LOG_HANDLE = open(log_file_path, "a", encoding="utf-8", buffering=1)
        sys.stdout = _TeeWriter(sys.stdout, LOG_HANDLE)
        sys.stderr = _TeeWriter(sys.stderr, LOG_HANDLE)
        print(f"[*] Log file: {log_file_path}")
    except OSError as exc:
        print(f"[WARN] Could not open log file '{log_file_path}': {exc}")

    print("=" * 70)
    print("  FRIDA 0x1B8B HUNTER")
    print("  Goal: Capture checksum + verify byte computation")
    print("=" * 70)

    # Try to connect
    device = None
    try:
        device = frida.get_usb_device(timeout=3)
        print("[*] Connected via USB")
    except:
        try:
            device = frida.get_device_manager().add_remote_device(REMOTE_DEVICE)
            print(f"[*] Connected via remote ({REMOTE_DEVICE})")
        except Exception as e:
            print(f"[!] Cannot connect: {e}")
            print(f"[!] Make sure frida-server is running on the emulator")
            print(f"[!] Try: adb forward tcp:27042 tcp:27042")
            return

    # Find / spawn / attach target process
    spawn_gating_enabled = False
    attached_sessions = {}

    def on_spawn_added(spawn):
        ident = getattr(spawn, "identifier", "")
        try:
            if PACKAGE in ident or is_target_process_name(ident):
                print(f"[*] spawn-added target: {ident} (PID {spawn.pid})")
                attach_hook_script(device, spawn.pid, attached_sessions)
            else:
                print(f"[*] spawn-added non-target: {ident} (PID {spawn.pid})")
        except Exception as exc:
            print(f"[WARN] spawn-added handler error for PID {spawn.pid}: {exc}")
        finally:
            try:
                device.resume(spawn.pid)
            except Exception:
                pass

    if spawn_mode:
        try:
            device.on("spawn-added", on_spawn_added)
            device.enable_spawn_gating()
            spawn_gating_enabled = True
            print("[*] Spawn gating enabled")
        except Exception as e:
            print(f"[WARN] Could not enable spawn gating: {e}")

        try:
            pid = device.spawn([PACKAGE])
            print(f"[*] Spawned {PACKAGE} (PID {pid})")
        except Exception as e:
            print(f"[!] Failed to spawn {PACKAGE}: {e}")
            return
    else:
        if pid is None:
            chosen = find_latest_target_process(device)
            if chosen:
                pid = chosen.pid
                print(f"[*] Found game process: {chosen.name} (PID {pid})")

        if pid is None and not no_wait:
            print("[*] Waiting for game process to appear...")
            while pid is None:
                time.sleep(1.5)
                chosen = find_latest_target_process(device)
                if chosen:
                    pid = chosen.pid
                    print(f"[*] Found game process: {chosen.name} (PID {pid})")
                    break

    if pid is None:
        print("[!] Game not found. Either:")
        print("    1. Start the game first, then run this script")
        print("    2. Pass PID as argument: python frida_1b8b.py <PID>")
        print("\n[*] Running processes:")
        for proc in device.enumerate_processes():
            if proc.pid > 100:
                print(f"    {proc.pid}: {proc.name}")
        return

    if not attach_hook_script(device, pid, attached_sessions):
        print("[WARN] Failed to attach initial target")
        if spawn_mode or no_wait:
            return
        print("[*] Waiting for an attachable target process...")
        while not attached_sessions:
            time.sleep(1.5)
            chosen = find_latest_target_process(device)
            if chosen:
                pid = chosen.pid
                attach_hook_script(device, pid, attached_sessions)
        print(f"[*] Recovered with attached PID {pid}")

    def discover_target_processes() -> bool:
        changed = False
        try:
            for proc in device.enumerate_processes():
                if is_target_process_name(proc.name):
                    if attach_hook_script(device, proc.pid, attached_sessions):
                        changed = True
        except Exception:
            pass
        return changed

    if spawn_mode:
        try:
            device.resume(pid)
            print(f"[*] Resumed spawned PID {pid}")
        except Exception as e:
            print(f"[!] Failed to resume spawned PID {pid}: {e}")

        # Multi-process games may move networking to sibling processes shortly after spawn.
        # Poll briefly for already-running siblings in addition to spawn-gating callbacks.
        discover_deadline = time.time() + 20.0
        while time.time() < discover_deadline:
            discover_target_processes()
            time.sleep(0.5)
    else:
        # Also attach siblings when running in non-spawn mode.
        discover_target_processes()

    print(f"[*] Hooked process count: {len(attached_sessions)}")

    print("\n" + "=" * 70)
    print("  WAITING FOR 0x1B8B PACKET...")
    print("  If already logged in: force-close and re-open the game")
    print("  0x1B8B is sent during the login/init sequence")
    print("  Press Ctrl+C to stop")
    print("=" * 70 + "\n")

    last_attach_count = len(attached_sessions)
    last_discover_ts = time.time()
    while True:
        try:
            time.sleep(1)
            now = time.time()
            if now - last_discover_ts >= 2.0:
                if discover_target_processes() or len(attached_sessions) != last_attach_count:
                    print(f"[*] Hooked process count updated: {len(attached_sessions)}")
                    last_attach_count = len(attached_sessions)
                last_discover_ts = now
        except KeyboardInterrupt:
            if stop_on_ctrl_c:
                break
            print("[*] Ctrl+C received but monitor is still running (use --stop-on-ctrl-c to exit).")

    print(f"\n\nCaptured {len(captured_1b8b)} 0x1B8B packets")
    for p in captured_1b8b:
        if all(k in p for k in ("ck_std", "ml_std", "v_std", "mh_std")):
            print(
                "  std "
                f"ck=0x{p['ck_std']:02X} ml=0x{p['ml_std']:02X} "
                f"v=0x{p['v_std']:02X} mh=0x{p['mh_std']:02X}"
            )
        elif all(k in p for k in ("ck_off6", "ml_off6", "v_off6", "mh_off6")):
            print(
                "  off6 "
                f"ck=0x{p['ck_off6']:02X} ml=0x{p['ml_off6']:02X} "
                f"v=0x{p['v_off6']:02X} mh=0x{p['mh_off6']:02X}"
            )

    if opcode_stats:
        print("\nOpcode summary (sorted by count desc):")
        for op, n in sorted(opcode_stats.items(), key=lambda kv: kv[1], reverse=True):
            print(f"  {op}: {n}")
        print("\nFirst-seen opcode order:")
        print("  " + " -> ".join(opcode_order))

    for pid_i, session_i in list(attached_sessions.items()):
        try:
            session_i.detach()
            print(f"[*] Detached PID {pid_i}")
        except Exception:
            pass

    if spawn_gating_enabled:
        try:
            device.disable_spawn_gating()
            print("[*] Spawn gating disabled")
        except Exception:
            pass

    print("Done!")

    if LOG_HANDLE is not None:
        try:
            sys.stdout = ORIG_STDOUT
            sys.stderr = ORIG_STDERR
            LOG_HANDLE.flush()
            LOG_HANDLE.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()

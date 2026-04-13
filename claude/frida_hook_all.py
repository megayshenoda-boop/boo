"""Frida hook - Capture ALL packets from game to see exact gather sequence"""
import frida, sys, time, datetime

SCRIPT = r"""
'use strict';

var gameFd = -1;
var captureAll = true;  // Capture everything!

function bytesToHex(buf, len) {
    var hex = '';
    for (var i = 0; i < len; i++) {
        var b = Memory.readU8(buf.add(i));
        hex += ('0' + (b & 0xff).toString(16)).slice(-2);
    }
    return hex;
}

function getU16LE(buf, off) {
    return Memory.readU8(buf.add(off)) | (Memory.readU8(buf.add(off+1)) << 8);
}

var sendAddr = Module.getExportByName('libc.so', 'send');
send('hook send at ' + sendAddr);

Interceptor.attach(sendAddr, {
    onEnter: function(args) {
        var fd = args[0].toInt32();
        var buf = args[1];
        var len = args[2].toInt32();
        
        if (len < 4 || len > 50000) return;
        
        var pktLen = getU16LE(buf, 0);
        var opcode = getU16LE(buf, 2);
        
        // Detect game socket by opcode
        if (opcode === 0x000B || opcode === 0x001F || opcode === 0x0CE8) {
            gameFd = fd;
        }
        
        // Capture ALL packets from game socket
        if (fd === gameFd) {
            var showLen = Math.min(len, 300);
            var hex = bytesToHex(buf, showLen);
            var ts = Date.now();
            send('C2S|' + ts + '|0x' + ('0000' + opcode.toString(16)).slice(-4) + '|' + len + '|' + hex);
        }
    }
});

var recvAddr = Module.getExportByName('libc.so', 'recv');
send('hook recv at ' + recvAddr);

Interceptor.attach(recvAddr, {
    onEnter: function(args) {
        this.fd = args[0].toInt32();
        this.buf = args[1];
    },
    onLeave: function(retval) {
        var n = retval.toInt32();
        if (this.fd !== gameFd || n < 4 || n > 50000) return;
        
        var opcode = getU16LE(this.buf, 2);
        
        var showLen = Math.min(n, 300);
        var hex = bytesToHex(this.buf, showLen);
        var ts = Date.now();
        send('S2C|' + ts + '|0x' + ('0000' + opcode.toString(16)).slice(-4) + '|' + n + '|' + hex);
    }
});

send('READY! Do a GATHER now!');
"""

def on_msg(msg, data):
    if msg['type'] == 'send':
        p = msg['payload']
        ts = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
        
        # Highlight important packets
        if '0CE8' in p.upper() or '0x0ce8' in p:
            print(f"\n[{ts}] *** GATHER PACKET: {p[:200]}...")
        elif '0323' in p:
            print(f"[{ts}] ### HERO: {p[:150]}...")
        elif '1B8B' in p:
            print(f"[{ts}] ### PASSWORD: {p[:150]}...")
        elif '00B8' in p or '00B9' in p or '0071' in p or '076C' in p:
            print(f"[{ts}] >>> MARCH RESP: {p[:150]}...")
        else:
            print(f"[{ts}] {p[:120]}...")
    elif msg['type'] == 'error':
        print(f"ERR: {msg['stack'][:200]}")

def main():
    print("[*] Connecting to emulator...")
    try:
        d = frida.get_device("127.0.0.1:21503")
        s = d.attach("Conquerors")
        sc = s.create_script(SCRIPT)
        sc.on('message', on_msg)
        sc.load()
        print("[*] Hooks active! Do a GATHER in-game now.\n")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Done.")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == '__main__':
    main()

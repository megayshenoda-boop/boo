"""Frida hook v2 - simpler, more compatible"""
import frida, sys, time

SCRIPT = r"""
'use strict';

var gameFd = -1;

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
        
        if (opcode === 0x0042 || opcode === 0x0020 || opcode === 0x0CE8 || 
            opcode === 0x0323 || opcode === 0x006E || opcode === 0x0CEB ||
            opcode === 0x000B || opcode === 0x0014) {
            gameFd = fd;
        }
        
        if (fd === gameFd && opcode !== 0x0042) {
            var showLen = Math.min(len, 200);
            var hex = bytesToHex(buf, showLen);
            send('C2S 0x' + ('0000' + opcode.toString(16)).slice(-4) + ' ' + len + 'B: ' + hex);
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
        
        if (opcode === 0x00B8 || opcode === 0x00B9 || opcode === 0x0323 ||
            opcode === 0x011C || opcode === 0x06C2 || opcode === 0x00AA ||
            opcode === 0x00B7) {
            var showLen = Math.min(n, 200);
            var hex = bytesToHex(this.buf, showLen);
            send('S2C 0x' + ('0000' + opcode.toString(16)).slice(-4) + ' ' + n + 'B: ' + hex);
        }
    }
});

send('READY - do a gather now!');
"""

def on_msg(msg, data):
    if msg['type'] == 'send':
        p = msg['payload']
        # Highlight important packets
        if '0ce8' in p.lower() or '0323' in p.lower() or '00b8' in p.lower() or '00b9' in p.lower():
            print(f"*** {p}")
        else:
            print(f"    {p}")
    elif msg['type'] == 'error':
        print(f"ERR: {msg['stack'][:200]}")

def main():
    print("[*] Connecting...")
    d = frida.get_device("127.0.0.1:21503")
    s = d.attach("Conquerors")
    sc = s.create_script(SCRIPT)
    sc.on('message', on_msg)
    sc.load()
    print("[*] Hooks active! Do a GATHER in-game now. Ctrl+C to stop.\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Done.")
        s.detach()

if __name__ == '__main__':
    main()

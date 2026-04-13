"""Frida hook - Capture ALL packets and save to log file for analysis"""
import frida, sys, time, datetime

LOG_FILE = r'D:\CascadeProjects\claude\frida_capture_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.log'

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

Interceptor.attach(sendAddr, {
    onEnter: function(args) {
        var fd = args[0].toInt32();
        var buf = args[1];
        var len = args[2].toInt32();
        
        if (len < 4 || len > 50000) return;
        
        var opcode = getU16LE(buf, 2);
        
        // Detect game socket
        if (opcode === 0x000B || opcode === 0x001F || opcode === 0x0CE8) {
            gameFd = fd;
        }
        
        // Capture ALL C2S packets
        if (fd === gameFd) {
            var hex = bytesToHex(buf, Math.min(len, 400));
            send('C2S|' + opcode.toString(16).padStart(4,'0') + '|' + len + '|' + hex);
        }
    }
});

var recvAddr = Module.getExportByName('libc.so', 'recv');

Interceptor.attach(recvAddr, {
    onEnter: function(args) {
        this.fd = args[0].toInt32();
        this.buf = args[1];
    },
    onLeave: function(retval) {
        var n = retval.toInt32();
        if (this.fd !== gameFd || n < 4 || n > 50000) return;
        
        var opcode = getU16LE(this.buf, 2);
        var hex = bytesToHex(this.buf, Math.min(n, 400));
        send('S2C|' + opcode.toString(16).padStart(4,'0') + '|' + n + '|' + hex);
    }
});

send('READY');
"""

def main():
    print(f"[*] Connecting to emulator...")
    print(f"[*] Log file: {LOG_FILE}")
    
    with open(LOG_FILE, 'w') as f:
        f.write(f"# Frida Capture - {datetime.datetime.now()}\n")
        f.write("# Format: DIR|op|len|hex\n")
        f.write("# Do a GATHER in-game to capture packets\n\n")
    
    try:
        d = frida.get_device("127.0.0.1:21503")
        # Try to find Conquerors process
        procs = d.enumerate_processes()
        pid = None
        for p in procs:
            if 'conquer' in p.name.lower():
                pid = p.pid
                print(f"[*] Found game: {p.name} (PID {pid})")
                break
        if not pid:
            print("[!] Game process not found!")
            return
        s = d.attach(pid)
        sc = s.create_script(SCRIPT)
        
        def on_msg(msg, data):
            if msg['type'] == 'send':
                p = msg['payload']
                ts = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
                line = f"{ts}|{p}"
                
                with open(LOG_FILE, 'a') as f:
                    f.write(line + '\n')
                
                # Show important packets on screen
                if '0CE8' in p.upper() or '00B8' in p or '00B9' in p or '0071' in p or '076C' in p:
                    print(f"[>>>] {line[:200]}")
                elif '1B8B' in p or '1C87' in p or '0323' in p:
                    print(f"[###] {line[:150]}")
        
        sc.on('message', on_msg)
        sc.load()
        print("[*] Hooks active! Do a GATHER now. Ctrl+C to stop.\n")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n[*] Done! Log saved to: {LOG_FILE}")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == '__main__':
    main()

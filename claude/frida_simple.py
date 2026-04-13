"""Simple Frida hook for packet capture"""
import frida, sys, time

SCRIPT = """
function readU8(ptr) {
    return ptr.readU8();
}

function getU16LE(ptr, off) {
    return readU8(ptr.add(off)) | (readU8(ptr.add(off + 1)) << 8);
}

function bytesToHex(ptr, len) {
    var hex = '';
    for (var i = 0; i < len && i < 300; i++) {
        var b = readU8(ptr.add(i));
        hex += ((b >> 4) & 0xF).toString(16);
        hex += (b & 0xF).toString(16);
    }
    return hex;
}

var gameFd = -1;

// Hook send
var sendPtr = Module.findExportByName('libc.so', 'send');
console.log('send at: ' + sendPtr);

Interceptor.attach(sendPtr, {
    onEnter: function(args) {
        var fd = args[0].toInt32();
        var buf = args[1];
        var len = args[2].toInt32();
        
        if (len < 4 || len > 10000) return;
        
        var opcode = getU16LE(buf, 2);
        
        // Detect game socket
        if (opcode === 0x000B || opcode === 0x001F) {
            gameFd = fd;
            console.log('Game FD detected: ' + fd);
        }
        
        // Log important packets
        if (fd === gameFd) {
            if (opcode === 0x0CE8 || opcode === 0x0323 || opcode === 0x1B8B || 
                opcode === 0x099D || opcode === 0x0769) {
                var hex = bytesToHex(buf, Math.min(len, 200));
                console.log('C2S 0x' + opcode.toString(16) + ' ' + len + 'B: ' + hex);
            }
        }
    }
});

// Hook recv  
var recvPtr = Module.findExportByName('libc.so', 'recv');
console.log('recv at: ' + recvPtr);

Interceptor.attach(recvPtr, {
    onEnter: function(args) {
        this.fd = args[0].toInt32();
        this.buf = args[1];
    },
    onLeave: function(retval) {
        var n = retval.toInt32();
        if (this.fd !== gameFd || n < 4 || n > 10000) return;
        
        var opcode = getU16LE(this.buf, 2);
        
        if (opcode === 0x00B8 || opcode === 0x00B9 || opcode === 0x0071 || opcode === 0x076C) {
            var hex = bytesToHex(this.buf, Math.min(n, 200));
            console.log('S2C 0x' + opcode.toString(16) + ' ' + n + 'B: ' + hex);
        }
    }
});

console.log('Hooks installed! Do a GATHER now.');
"""

def on_msg(msg, data):
    if msg['type'] == 'send':
        print(msg['payload'])
    elif msg['type'] == 'error':
        print('ERR:', msg.get('description', 'unknown'))

def main():
    print('[*] Connecting...')
    d = frida.get_device('127.0.0.1:21503')
    
    # Find game process
    procs = d.enumerate_processes()
    pid = None
    for p in procs:
        if 'conquer' in p.name.lower():
            pid = p.pid
            print(f'[*] Found: {p.name} (PID {pid})')
            break
    
    if not pid:
        print('[!] Game not found')
        return
    
    s = d.attach(pid)
    sc = s.create_script(SCRIPT)
    sc.on('message', on_msg)
    sc.load()
    
    print('[*] Ready! Do a GATHER now.')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('[*] Done')

if __name__ == '__main__':
    main()

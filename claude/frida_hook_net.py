"""Frida hook - capture send/recv only (no libgame hooks due to houdini)
Run this, then do a gather in-game to capture the real packets."""
import frida, sys, time, struct

SCRIPT = """
// Hook send() only - capture outgoing packets
var sendPtr = Module.findExportByName("libc.so", "send");
var writePtr = Module.findExportByName("libc.so", "write");

// Track game socket fd
var gameFd = -1;

if (sendPtr) {
    Interceptor.attach(sendPtr, {
        onEnter: function(args) {
            var fd = args[0].toInt32();
            var buf = args[1];
            var len = args[2].toInt32();
            
            if (len >= 4 && len < 50000) {
                var bytes = [];
                for (var i = 0; i < Math.min(len, 200); i++) {
                    bytes.push(buf.add(i).readU8());
                }
                var pktLen = bytes[0] | (bytes[1] << 8);
                var opcode = bytes[2] | (bytes[3] << 8);
                
                // Detect game socket by looking for known opcodes
                if (opcode === 0x0042 || opcode === 0x0020 || opcode === 0x0CE8 || 
                    opcode === 0x0323 || opcode === 0x006E || opcode === 0x0CEB) {
                    gameFd = fd;
                }
                
                if (fd === gameFd && opcode !== 0x0042) {
                    var hex = "";
                    for (var i = 0; i < bytes.length; i++) {
                        hex += ("0" + bytes[i].toString(16)).slice(-2);
                    }
                    send({type: "send", fd: fd, len: len, opcode: opcode, hex: hex});
                }
            }
        }
    });
    send({type: "info", msg: "Hooked send()"});
}

// Hook recv for responses
var recvfromPtr = Module.findExportByName("libc.so", "recvfrom");
if (recvfromPtr) {
    Interceptor.attach(recvfromPtr, {
        onEnter: function(args) {
            this.fd = args[0].toInt32();
            this.buf = args[1];
        },
        onLeave: function(retval) {
            var bytesRead = retval.toInt32();
            if (this.fd === gameFd && bytesRead >= 4 && bytesRead < 50000) {
                var bytes = [];
                for (var i = 0; i < Math.min(bytesRead, 200); i++) {
                    bytes.push(this.buf.add(i).readU8());
                }
                var pktLen = bytes[0] | (bytes[1] << 8);
                var opcode = bytes[2] | (bytes[3] << 8);
                
                if (opcode !== 0x0042 && opcode !== 0x036C && opcode !== 0x026D) {
                    var hex = "";
                    for (var i = 0; i < bytes.length; i++) {
                        hex += ("0" + bytes[i].toString(16)).slice(-2);
                    }
                    send({type: "recv", fd: this.fd, len: bytesRead, opcode: opcode, hex: hex});
                }
            }
        }
    });
    send({type: "info", msg: "Hooked recvfrom()"});
}

// Also hook read() as some implementations use read instead of recv
if (writePtr) {
    Interceptor.attach(writePtr, {
        onEnter: function(args) {
            var fd = args[0].toInt32();
            var buf = args[1];
            var len = args[2].toInt32();
            
            if (fd === gameFd && len >= 4 && len < 50000) {
                var bytes = [];
                for (var i = 0; i < Math.min(len, 200); i++) {
                    bytes.push(buf.add(i).readU8());
                }
                var opcode = bytes[2] | (bytes[3] << 8);
                if (opcode !== 0x0042) {
                    var hex = "";
                    for (var i = 0; i < bytes.length; i++) {
                        hex += ("0" + bytes[i].toString(16)).slice(-2);
                    }
                    send({type: "write", fd: fd, len: len, opcode: opcode, hex: hex});
                }
            }
        }
    });
    send({type: "info", msg: "Hooked write()"});
}

send({type: "info", msg: "All hooks ready! Do a GATHER in game now."});
"""

def on_message(message, data):
    if message['type'] == 'send':
        payload = message['payload']
        if payload.get('type') == 'info':
            print(f"[*] {payload['msg']}")
        elif payload.get('type') == 'send':
            op = payload['opcode']
            h = payload['hex']
            tag = ""
            if op == 0x0CE8: tag = " <<< GATHER!"
            elif op == 0x0323: tag = " <<< HERO_RECRUIT!"
            elif op == 0x006E: tag = " <<< TILE_SELECT"
            elif op == 0x0CEB: tag = " <<< ENABLE_VIEW"
            print(f"[SEND] op=0x{op:04X} len={payload['len']}{tag}")
            # Print hex in groups of 2
            for i in range(0, len(h), 80):
                print(f"  {h[i:i+80]}")
        elif payload.get('type') in ('recv', 'write'):
            op = payload['opcode']
            h = payload['hex']
            tag = ""
            if op == 0x00B8: tag = " <<< HERO_EXPEDITION!"
            elif op == 0x00B9: tag = " <<< MARCH_CONFIRM!"
            elif op == 0x011C: tag = " <<< ERROR!"
            elif op == 0x0323: tag = " <<< HERO_RECRUIT_RESP!"
            print(f"[{payload['type'].upper()}] op=0x{op:04X} len={payload['len']}{tag}")
            for i in range(0, len(h), 80):
                print(f"  {h[i:i+80]}")
    elif message['type'] == 'error':
        print(f"ERROR: {message['stack']}")

def main():
    print("[*] Connecting to emulator...")
    device = frida.get_device("127.0.0.1:21503")
    session = device.attach("Conquerors")
    
    script = session.create_script(SCRIPT)
    script.on('message', on_message)
    script.load()
    
    print("\n" + "="*60)
    print("  DO A GATHER IN GAME NOW!")
    print("  Select heroes, pick a resource tile, and march!")
    print("  This will capture the exact packet format.")
    print("="*60 + "\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Stopping...")
        session.detach()

if __name__ == '__main__':
    main()

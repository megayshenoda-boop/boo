// Hook send() to capture all outgoing game packets
// Also hook the CMsgCodec encode if we can find it

var libgame = Process.findModuleByName("libgame.so");
if (libgame) {
    send("[*] libgame.so base: " + libgame.base + " size: " + libgame.size);
} else {
    send("[!] libgame.so not loaded!");
}

// Hook libc send()
var sendPtr = Module.findExportByName("libc.so", "send");
if (sendPtr) {
    Interceptor.attach(sendPtr, {
        onEnter: function(args) {
            this.fd = args[0].toInt32();
            this.buf = args[1];
            this.len = args[2].toInt32();
            
            // Only log game packets (len >= 4)
            if (this.len >= 4 && this.len < 10000) {
                var data = new Uint8Array(ArrayBuffer.wrap(this.buf, this.len));
                var pktLen = data[0] | (data[1] << 8);
                var opcode = data[2] | (data[3] << 8);
                
                // Filter: only log march/gather related opcodes
                // 0x0CE8=gather, 0x0323=hero_recruit, 0x006E=tile, 0x0CEB=enable_view
                // 0x0042=heartbeat, 0x0840/0x17D4/0x0AF2/0x0245=setup
                var hex = "";
                for (var i = 0; i < Math.min(this.len, 100); i++) {
                    hex += ("0" + data[i].toString(16)).slice(-2);
                }
                
                if (opcode === 0x0CE8 || opcode === 0x0323 || opcode === 0x006E || 
                    opcode === 0x0CEB || opcode === 0x00B8 || opcode === 0x00B9) {
                    send("[SEND] fd=" + this.fd + " len=" + this.len + 
                         " pktLen=" + pktLen + " op=0x" + opcode.toString(16).padStart(4, '0') +
                         " hex=" + hex);
                } else if (opcode !== 0x0042) {
                    // Log non-heartbeat packets briefly
                    send("[send] fd=" + this.fd + " op=0x" + opcode.toString(16).padStart(4, '0') + 
                         " len=" + this.len);
                }
            }
        }
    });
    send("[*] Hooked send()");
}

// Hook recv/read to see server responses
var recvPtr = Module.findExportByName("libc.so", "recv");
if (recvPtr) {
    Interceptor.attach(recvPtr, {
        onEnter: function(args) {
            this.fd = args[0].toInt32();
            this.buf = args[1];
            this.len = args[2].toInt32();
        },
        onLeave: function(retval) {
            var bytesRead = retval.toInt32();
            if (bytesRead >= 4 && bytesRead < 10000) {
                var data = new Uint8Array(ArrayBuffer.wrap(this.buf, bytesRead));
                var pktLen = data[0] | (data[1] << 8);
                var opcode = data[2] | (data[3] << 8);
                
                // Only log march-related responses
                if (opcode === 0x00B8 || opcode === 0x00B9 || opcode === 0x0323 ||
                    opcode === 0x011C || opcode === 0x06C2) {
                    var hex = "";
                    for (var i = 0; i < Math.min(bytesRead, 60); i++) {
                        hex += ("0" + data[i].toString(16)).slice(-2);
                    }
                    send("[RECV] fd=" + this.fd + " op=0x" + opcode.toString(16).padStart(4, '0') +
                         " len=" + bytesRead + " hex=" + hex);
                }
            }
        }
    });
    send("[*] Hooked recv()");
}

// Try to hook the specific packData functions
if (libgame) {
    // CMSG_START_MARCH_NEW::packData at 0x05212294
    var packDataAddr = libgame.base.add(0x05212294);
    try {
        Interceptor.attach(packDataAddr, {
            onEnter: function(args) {
                this.thisPtr = args[0];
                this.streamPtr = args[1];
                send("[MARCH_packData] this=" + this.thisPtr + " stream=" + this.streamPtr);
                
                // Dump first 96 bytes of 'this' (the CMSG struct)
                var structData = new Uint8Array(ArrayBuffer.wrap(this.thisPtr, 96));
                var hex = "";
                for (var i = 0; i < 96; i++) {
                    hex += ("0" + structData[i].toString(16)).slice(-2);
                }
                send("[MARCH_struct] " + hex);
            },
            onLeave: function(retval) {
                // Read stream buffer to see what was written
                // CIStream: [0x0]=buf_ptr, [0x8]=capacity, [0xA]=position, [0xC]=error
                var bufPtr = this.streamPtr.readPointer();
                var pos = this.streamPtr.add(0xA).readU16();
                if (pos > 0 && pos < 200) {
                    var written = new Uint8Array(ArrayBuffer.wrap(bufPtr, pos));
                    var hex = "";
                    for (var i = 0; i < pos; i++) {
                        hex += ("0" + written[i].toString(16)).slice(-2);
                    }
                    send("[MARCH_payload] " + pos + "B: " + hex);
                }
            }
        });
        send("[*] Hooked CMSG_START_MARCH_NEW::packData at " + packDataAddr);
    } catch(e) {
        send("[!] Failed to hook packData: " + e);
    }
    
    // CMSG_HERO_SOLDIER_RECRUIT_REQUEST::packData at 0x050AF814
    var heroPackDataAddr = libgame.base.add(0x050AF814);
    try {
        Interceptor.attach(heroPackDataAddr, {
            onEnter: function(args) {
                this.thisPtr = args[0];
                this.streamPtr = args[1];
                send("[HERO_0323_packData] this=" + this.thisPtr + " stream=" + this.streamPtr);
                
                var structData = new Uint8Array(ArrayBuffer.wrap(this.thisPtr, 64));
                var hex = "";
                for (var i = 0; i < 64; i++) {
                    hex += ("0" + structData[i].toString(16)).slice(-2);
                }
                send("[HERO_0323_struct] " + hex);
            },
            onLeave: function(retval) {
                var bufPtr = this.streamPtr.readPointer();
                var pos = this.streamPtr.add(0xA).readU16();
                if (pos > 0 && pos < 200) {
                    var written = new Uint8Array(ArrayBuffer.wrap(bufPtr, pos));
                    var hex = "";
                    for (var i = 0; i < pos; i++) {
                        hex += ("0" + written[i].toString(16)).slice(-2);
                    }
                    send("[HERO_0323_payload] " + pos + "B: " + hex);
                }
            }
        });
        send("[*] Hooked CMSG_HERO_SOLDIER_RECRUIT_REQUEST::packData at " + heroPackDataAddr);
    } catch(e) {
        send("[!] Failed to hook hero packData: " + e);
    }
    
    // CMSG_START_MARCH_EX::packData at 0x05212ADC
    var exPackDataAddr = libgame.base.add(0x05212ADC);
    try {
        Interceptor.attach(exPackDataAddr, {
            onEnter: function(args) {
                this.thisPtr = args[0];
                this.streamPtr = args[1];
                send("[MARCH_EX_packData] this=" + this.thisPtr + " stream=" + this.streamPtr);
                
                var structData = new Uint8Array(ArrayBuffer.wrap(this.thisPtr, 96));
                var hex = "";
                for (var i = 0; i < 96; i++) {
                    hex += ("0" + structData[i].toString(16)).slice(-2);
                }
                send("[MARCH_EX_struct] " + hex);
            },
            onLeave: function(retval) {
                var bufPtr = this.streamPtr.readPointer();
                var pos = this.streamPtr.add(0xA).readU16();
                if (pos > 0 && pos < 200) {
                    var written = new Uint8Array(ArrayBuffer.wrap(bufPtr, pos));
                    var hex = "";
                    for (var i = 0; i < pos; i++) {
                        hex += ("0" + written[i].toString(16)).slice(-2);
                    }
                    send("[MARCH_EX_payload] " + pos + "B: " + hex);
                }
            }
        });
        send("[*] Hooked CMSG_START_MARCH_EX::packData at " + exPackDataAddr);
    } catch(e) {
        send("[!] Failed to hook EX packData: " + e);
    }
}

send("[*] All hooks installed. Do a gather in-game now!");

"""List loaded modules to find libgame.so"""
import frida, time

device = frida.get_device("127.0.0.1:21503")
session = device.attach("Conquerors")

script = session.create_script("""
var modules = Process.enumerateModules();
for (var i = 0; i < modules.length; i++) {
    var m = modules[i];
    if (m.name.indexOf("game") !== -1 || m.name.indexOf("igg") !== -1 || 
        m.name.indexOf("lords") !== -1 || m.name.indexOf("conquer") !== -1 ||
        m.size > 50000000) {
        send(m.name + " base=" + m.base + " size=" + m.size);
    }
}
send("Total modules: " + modules.length);
""")

def on_msg(msg, data):
    if msg['type'] == 'send':
        print(msg['payload'])
    else:
        print("ERR:", msg)

script.on('message', on_msg)
script.load()
time.sleep(2)
session.detach()

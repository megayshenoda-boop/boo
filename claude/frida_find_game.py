"""Find libgame.so - search ALL modules and memory maps"""
import frida, time

device = frida.get_device("127.0.0.1:21503")
session = device.attach("Conquerors")

script = session.create_script("""
// List ALL modules sorted by size
var modules = Process.enumerateModules();
modules.sort(function(a, b) { return b.size - a.size; });

send("=== Top 20 largest modules ===");
for (var i = 0; i < Math.min(20, modules.length); i++) {
    var m = modules[i];
    send(i + ": " + m.name + " base=" + m.base + " size=" + (m.size/1024/1024).toFixed(1) + "MB");
}

// Search for libgame specifically
send("\\n=== Searching for 'game' in module names ===");
for (var i = 0; i < modules.length; i++) {
    if (modules[i].name.toLowerCase().indexOf("game") !== -1) {
        send("  FOUND: " + modules[i].name + " base=" + modules[i].base + " size=" + modules[i].size);
    }
}

// Search memory ranges for libgame.so string
send("\\n=== Searching for libgame.so in /proc/self/maps ===");
try {
    var maps = new File("/proc/self/maps", "r");
    var line;
    while ((line = maps.readLine()) !== "") {
        if (line.indexOf("libgame") !== -1) {
            send("  MAP: " + line.trim());
        }
    }
    maps.close();
} catch(e) {
    send("  Error reading maps: " + e);
}

// Also check for the game's native libs
send("\\n=== Checking /proc/self/maps for conquerors ===");
try {
    var maps2 = new File("/proc/self/maps", "r");
    var line;
    var count = 0;
    while ((line = maps2.readLine()) !== "") {
        if (line.indexOf("conquerors") !== -1 && line.indexOf(".so") !== -1 && count < 10) {
            send("  " + line.trim());
            count++;
        }
    }
    maps2.close();
} catch(e) {
    send("  Error: " + e);
}
""")

def on_msg(msg, data):
    if msg['type'] == 'send':
        print(msg['payload'])
    else:
        print("ERR:", msg)

script.on('message', on_msg)
script.load()
time.sleep(3)
session.detach()

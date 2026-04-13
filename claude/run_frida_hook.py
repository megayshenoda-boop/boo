"""Run Frida hook on Lords Mobile to capture gather packets"""
import frida
import sys
import time

DEVICE_ID = "127.0.0.1:21503"
PROCESS_NAME = "Conquerors"

def on_message(message, data):
    if message['type'] == 'send':
        payload = message['payload']
        # Highlight important messages
        if any(tag in payload for tag in ['MARCH_packData', 'MARCH_payload', 'HERO_0323', 'MARCH_EX', '[SEND]', '[RECV]']):
            print(f"*** {payload}")
        else:
            print(f"    {payload}")
    elif message['type'] == 'error':
        print(f"ERROR: {message['stack']}")

def main():
    print(f"[*] Connecting to {DEVICE_ID}...")
    device = frida.get_device(DEVICE_ID)
    
    print(f"[*] Attaching to {PROCESS_NAME}...")
    session = device.attach(PROCESS_NAME)
    
    with open(r"d:\CascadeProjects\claude\frida_hook_send.js", "r") as f:
        script_code = f.read()
    
    script = session.create_script(script_code)
    script.on('message', on_message)
    script.load()
    
    print("[*] Hook active! Do a gather in-game. Press Ctrl+C to stop.")
    print("[*] Waiting for packets...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Detaching...")
        session.detach()
        print("[*] Done.")

if __name__ == '__main__':
    main()

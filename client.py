import sys
import os

if len(sys.argv) < 5:
    print("Usage: python3 client.py HOST PORT MOUSE_PATH KEYBOARD_PATH")
    exit()

host = sys.argv[1]
port = int(sys.argv[2])
mouse_path = sys.argv[3]
keyboard_path = sys.argv[4]
user = os.urandom(4)

from pythonosc.udp_client import SimpleUDPClient
import io
import struct
from threading import Thread

client = SimpleUDPClient(host, port)

client.send_message('/connect', (user))

codes = {
    105: 'left',
    106: 'right',
    103: 'up',
    108: 'down'
}

def handle_keyboard():
    with io.open(keyboard_path, mode="rb", buffering=24) as keyboard_f:
        while True:
            _, c, v = struct.unpack("x" * 16 + "HHI", keyboard_f.read(24))
            c = codes.get(c, c)
            client.send_message("/keyboard", (user, c, v))

def handle_mouse():
    with io.open(mouse_path, mode="rb", buffering=3) as mouse_f:
        while True:
            v, x, y = struct.unpack("bbb", mouse_f.read(3))
            client.send_message("/mouse", (user, v, x, -y))

keyboard_thread = Thread(target = handle_keyboard)
keyboard_thread.start()

mouse_thread = Thread(target = handle_mouse)
mouse_thread.start()

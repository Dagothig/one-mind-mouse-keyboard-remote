import sys
import os

if len(sys.argv) < 3:
    print("Usage: py3 client.py HOST PORT")
    exit()

host = sys.argv[1]
port = int(sys.argv[2])
user = os.urandom(4)

from pythonosc.udp_client import SimpleUDPClient
import keyboard
import mouse

client = SimpleUDPClient(host, port)

client.send_message('/connect', (user))

keyboard.on_press(lambda event: client.send_message("/keyboard", (user, 1, event.scan_code)))
keyboard.on_release(lambda event: client.send_message("/keyboard", (user, 0, event.scan_code)))

lx, ly = mouse.get_position()
def handle_mouse_event(event):
    global lx, ly
    v = (mouse.is_pressed('left') and 1 or 0) | (mouse.is_pressed('right') and 2 or 0)
    x, y = mouse.get_position()
    client.send_message("/mouse", (user, v, x - lx, y - ly))
    lx = x
    ly = y

mouse.hook(handle_mouse_event)

keyboard.wait()

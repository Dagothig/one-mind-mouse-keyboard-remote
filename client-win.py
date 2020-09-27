import sys
import os

if len(sys.argv) < 3:
    print("Usage: python3 client-win.py HOST PORT")
    exit()

host = sys.argv[1]
port = int(sys.argv[2])
user = os.urandom(4)

from pythonosc.udp_client import SimpleUDPClient
import keyboard
import mouse

client = SimpleUDPClient(host, port)

client.send_message('/connect', (user))

def handle_keyboard_event(event):
    v = 0 if event.event_type == keyboard.KEY_UP else 1 if event.event_type == keyboard.KEY_DOWN else None
    client.send_message("/keyboard", (user, event.scan_code, v))

lx, ly = mouse.get_position()
def handle_mouse_event(event):
    global lx, ly
    v = (mouse.is_pressed('left') and 1 or 0) | (mouse.is_pressed('right') and 2 or 0)
    x, y = mouse.get_position()
    client.send_message("/mouse", (user, v, x - lx, y - ly))
    lx = x
    ly = y

keyboard.hook(handle_keyboard_event)
mouse.hook(handle_mouse_event)

keyboard.wait()

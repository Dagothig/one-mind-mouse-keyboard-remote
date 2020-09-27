# netcat -u host port < /dev/input/by-id/kbd
# netcat -u host port < /dev/input/mouse0

import sys
import keyboard
import mouse
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import struct
from enum import Enum
from threading import Thread

# FIXME: keyboard doesn't understand scan codes unless we use keys at some point...
keyboard.key_to_scan_codes('b')
keyboard.on_press(lambda x: print(x.scan_code))

def on_key_press(address, key):
    keyboard.press(key)

def on_key_release(address, key):
    keyboard.release(key)

def on_move(address, x, y):
    mouse.move(x, y)

def on_button(address, ev):
    event_type, button = ev
    if event_type ==  mouse.UP:
        mouse.release(button)
    elif event.type ==  mouse.DOWN:
        mouse.press(button)
    elif event.type ==  mouse.DOUBLE:
        mouse.double_click(button)

def on_wheel(address, delta):
    mouse.wheel(delta)

dispatcher = Dispatcher()
dispatcher.map("/mouse/move", on_move)
dispatcher.map("/mouse/button", on_button)
dispatcher.map("/mouse/wheel", on_wheel)
dispatcher.map("/keyboard/press", on_key_press)
dispatcher.map("/keyboard/release", on_key_release)

with BlockingOSCUDPServer(('', 8000), dispatcher) as server:
    server.serve_forever()

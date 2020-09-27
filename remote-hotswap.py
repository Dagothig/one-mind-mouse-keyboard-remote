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

clients = {}

# FIXME: keyboard doesn't understand scan codes unless we use keys at some point...
keyboard.key_to_scan_codes('b')

def handle_connect(address, user):
    if user in clients:
        return
    clients[user] = {}

def handle_keyboard_event(address, user, c, v):
    handle_connect(address, user)
    if v == 1:
        keyboard.press(c)
    elif v == 0:
        keyboard.release(c)

def handle_mouse_event(address, user, v, x, y):
    handle_connect(address, user)
    left = v & 1
    left_pressed = mouse.is_pressed('left')
    if left and not left_pressed:
        mouse.press('left')
    if not left and left_pressed:
        mouse.release('left')

    right = (v >> 1) & 1
    right_pressed = mouse.is_pressed('right')
    if right and not right_pressed:
        mouse.press('right')
    if not right and right_pressed:
        mouse.release('right')

    mouse.move(x, y, False)

dispatcher = Dispatcher()
dispatcher.map('/connect', handle_connect)
dispatcher.map("/keyboard", handle_keyboard_event)
dispatcher.map("/mouse", handle_mouse_event)

with BlockingOSCUDPServer(('', 8000), dispatcher) as server:
    server.serve_forever()

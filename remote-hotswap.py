# netcat -u host port < /dev/input/by-id/kbd
# netcat -u host port < /dev/input/mouse0

import sys
import keyboard
import mouse
from socketserver import BaseRequestHandler, UDPServer
import struct
from enum import Enum
from threading import Thread

# FIXME: keyboard doesn't understand scan codes unless we use keys at some point...
keyboard.key_to_scan_codes('b')

class KeyboardUDPHandler(BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        for t, c, v in struct.iter_unpack("x" * 16 + "HHI", data):
            if c == 0:
                continue
            if v == 1:
                keyboard.press(c)
            elif v == 0:
                keyboard.release(c)
            elif v == 2:
                keyboard.send(c)

class MouseUDPHandler(BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        for v, x, y in struct.iter_unpack("bbb", data):
            left = v & 1
            if left and not mouse.is_pressed('left'):
                mouse.press('left')
            if not left and mouse.is_pressed('left'):
                mouse.release('left')
            
            right = (v >> 1) & 1
            if right and not mouse.is_pressed('right'):
                mouse.press('right')
            if not right and mouse.is_pressed('right'):
                mouse.release('right')

            mouse.move(x, -y, False)

with UDPServer(('', 8000), KeyboardUDPHandler) as server:
    server.serve_forever()

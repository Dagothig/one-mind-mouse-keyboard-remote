import sys

if len(sys.argv) < 2:
    print("Usage: python3 remote-hotswap.py INTERVAL")
    exit()

interval = int(sys.argv[1]) / 1000

import keyboard
import mouse
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from time import sleep
from enum import Enum
from threading import Thread
import pygame

active_client_index = 0
clients = []
pygame.mixer.init()
sounds = [pygame.mixer.Sound("sounds/{}.wav".format(i)) for i in range(10)]

class Client():
    def __init__(self, name):
        self.name = name
        self.keys = {}
        self.mouse = {}
        self.should_live = True

    def __eq__(self, name):
        return self.name == name

    def restore(self):
        for key in self.keys:
            is_pressed = keyboard.is_pressed(key)
            if not is_pressed and self.keys[key]:
                keyboard.press(key)
            if is_pressed and not self.keys[key]:
                keyboard.release(key)
        self.keys.clear()
        for btn in self.mouse:
            is_pressed = keyboard.is_pressed(btn)
            if not is_pressed and self.mouse[btn]:
                mouse.press(btn)
            if is_pressed and not self.mouse[btn]:
                mouse.release(btn)
        self.mouse.clear()

def find_client(name):
    try:
        index = clients.index(name)
        return index, clients[index]
    except:
        return 0, None

def switch_controls():
    global active_client_index
    while True:
        if len(clients) > 0:
            # Kill inactive clients
            old_client = clients[active_client_index]
            if old_client.should_live:
                old_client.should_live = False
                active_client_index = (active_client_index + 1) % len(clients)
            else:
                clients.pop(active_client_index)
            # Restore client state if it has changed
            if len(clients) > active_client_index:
                client = clients[active_client_index]
                if client != old_client:
                    client.restore()
            sounds[active_client_index].play()
        sleep(interval)

# FIXME: keyboard doesn't understand scan codes unless we use keys at some point...
keyboard.key_to_scan_codes('b')

def handle_connect(address, clientname):
    index, client = find_client(clientname)
    if not client:
        client = Client(clientname)
        clients.append(client)
    client.should_live = True
    return client, index == active_client_index

def handle_keyboard_event(address, clientname, c, v):
    client, active = handle_connect(address, clientname)

    client.keys[c] = v == 1

    if not active:
        return

    if v == 1:
        keyboard.press(c)
    elif v == 0:
        keyboard.release(c)

def handle_mouse_event(address, clientname, v, x, y):
    client, active = handle_connect(address, clientname)
    left = v & 1
    right = (v >> 1) & 1

    client.mouse['left'] = left == 1
    client.mouse['right'] = right == 1

    if not active:
        return

    left_pressed = mouse.is_pressed('left')
    if left and not left_pressed:
        mouse.press('left')
    if not left and left_pressed:
        mouse.release('left')

    right_pressed = mouse.is_pressed('right')
    if right and not right_pressed:
        mouse.press('right')
    if not right and right_pressed:
        mouse.release('right')

    mouse.move(x, y, False)

switch_thread = Thread(target = switch_controls)
switch_thread.start()

dispatcher = Dispatcher()
dispatcher.map('/connect', handle_connect)
dispatcher.map("/keyboard", handle_keyboard_event)
dispatcher.map("/mouse", handle_mouse_event)

with BlockingOSCUDPServer(('', 8000), dispatcher) as server:
    print("WOOOOOOOOOOO")
    sys.stdout.flush()
    server.serve_forever()
print("AAA")
sys.stdout.flush()

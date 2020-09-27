from pythonosc.udp_client import SimpleUDPClient
import keyboard
import mouse

mouse_path = "/dev/input/mouse0"
keyboard_path = "/dev/input/event2"

client = SimpleUDPClient("192.168.1.224", 8000)

keyboard.on_press(lambda ev: client.send_message('/keyboard/press', ev.name))
keyboard.on_release(lambda ev: client.send_message('/keyboard/release', ev.name))

def onMouse(ev):
    if type(ev) == mouse.MoveEvent:
        client.send_message('/mouse/move', (ev.x, ev.y))
    elif type(ev) == mouse.ButtonEvent:
        client.send_message('/mouse/button', (ev.event_type, ev.button))
    elif type(ev) == mouse.WheelEvent:
        client.send_message('/mouse/wheel', ev.delta)
mouse.hook(onMouse)

keyboard.wait()

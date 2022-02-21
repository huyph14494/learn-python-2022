import time
import threading
from pynput.keyboard import Listener, KeyCode, Key

delay=0.5
start_stop_key=KeyCode(char='s')
exit_key=KeyCode(char='e')

class ClickMouse(threading.Thread):
    def __init__(self, delay):
        super().__init__()
        self.delay = delay
        self.running = False
        self.program_running = True
    def start_clicking(self):
        self.running = True
    def stop_clicking(self):
        self.running = False
    def exit(self):
        self.program_running = False
    def run(self):
        print("start")
        while self.program_running:
            while self.running:
                print('1')
                time.sleep(self.delay)

click_thread = ClickMouse(delay)

def on_press(key):
    try:
        print('key {0} pressed'.format(key.char))
        if key == start_stop_key:
            if click_thread.running:
                click_thread.stop_clicking()
            else:
                click_thread.start_clicking()
    except AttributeError:
        print('special key {0} pressed'.format(key))
    

def on_release(key):
    if key == Key.esc:
        # Stop listener
        click_thread.exit()
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


click_thread.start()
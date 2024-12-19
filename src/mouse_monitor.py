from queue import Queue

import pynput
from pynput import mouse
import threading
import time
import tkinter

class MouseMonitor:

    def __init__(self, queue: Queue, n_clicks:tkinter.IntVar):
        self.queue = queue
        self.listener = mouse.Listener(on_click=self.on_click)
        self.n_clicks = n_clicks

    def on_click(self, x, y, button, pressed):
        data_row = {'time': time.time(), 'x': x, 'y': y, 'button': button, 'pressed': pressed}
        self.queue.put(data_row)
        if not pressed:
            self.n_clicks.set(self.n_clicks.get() + 1)
        print("monitor activity "+str(time.time()))

    def start(self):
        self.listener.start()

    def stop(self):
        self.listener.stop()
        self.listener = mouse.Listener(on_click=self.on_click)

import random
from pynput.mouse import Button, Controller
import pynput
import time
import math
from tkinter import ttk
from tkinter import *
import ctypes
import tkinter as tk


class AutoClicker:

    def __init__(self):
        self.mouse = Controller()

    def spam_clicks(self, button, number_clicks):
        self.mouse.click(button, number_clicks)

    def circumference_clicks(self, button, number_clicks, radius, interval):
        delta_angle = 2 * math.pi / number_clicks
        center = self.mouse.position
        self.mouse.position += radius, 0
        for i in range(number_clicks):
            self.mouse.click(button)
            self.mouse.position = center[0] + int(math.cos(i * delta_angle) * 200), center[1] + int(
                math.sin(i * delta_angle) * 200)
            time.sleep(interval)

    def circle_clicks(self, button, number_clicks, radius, interval):
        center = self.mouse.position
        for i in range(number_clicks):
            angle = 2 * math.pi * random.random()
            module = radius * random.random()
            self.mouse.position = center[0] + int(module * math.cos(angle)), center[1] + int(module * math.sin(angle))
            self.mouse.click(button)
            time.sleep(interval)

    def steady_clicks(self, button, number_clicks, interval):
        for i in range(number_clicks):
            self.mouse.click(button)
            time.sleep(interval)

    def zig_zag_clicks(self, button, number_clicks, max_distance, interval):
        for i in range(number_clicks):
            distance = max_distance * random.random()
            angle = 2 * math.pi * random.random()
            self.mouse.move(int(distance * math.cos(angle)), int(distance * math.sin(angle)))
            self.mouse.click(button)
            time.sleep(interval)

    def quicker_clicks(self, button, number_clicks, starting_interval, factor):
        for i in range(number_clicks):
            self.mouse.click(button)
            time.sleep(starting_interval)
            starting_interval *= factor


def main():
    autoclicker = AutoClicker()
    root = Tk()
    root.title("Simple Autoclicker")
    mainframe = ttk.Frame(root, padding="8 8 8 8")
    mainframe.grid(column=0, row=0)
    root.resizable(False, False)
    lag = DoubleVar(value=2)
    n_clicks = IntVar(value=10)
    frequency = DoubleVar(value=5)
    radius = IntVar(value=50)
    max_step = IntVar(value=25)
    speed_up = DoubleVar(value=1.1)
    lbl_keybindings = ttk.Label(mainframe, text="Keyboard bindings:")
    lbl_parameters = ttk.Label(mainframe, text="Parameters for autoclicker:")
    lbl_1 = ttk.Label(mainframe, text="\"Alt-1\"")
    lbl_2 = ttk.Label(mainframe, text="\"Alt-2\"")
    lbl_3 = ttk.Label(mainframe, text="\"Alt-3\"")
    lbl_4 = ttk.Label(mainframe, text="\"Alt-4\"")
    lbl_5 = ttk.Label(mainframe, text="\"Alt-5\"")
    lbl_6 = ttk.Label(mainframe, text="\"Alt-6\"")
    lbl_1_b = ttk.Label(mainframe, text="to run \"spam_clicks\"")
    lbl_2_b = ttk.Label(mainframe, text="to run \"steady_clicks\"")
    lbl_3_b = ttk.Label(mainframe, text="to run \"quicker_clicks\"")
    lbl_4_b = ttk.Label(mainframe, text="to run \"circumference_clicks\"")
    lbl_5_b = ttk.Label(mainframe, text="to run \"circle_clicks\"")
    lbl_6_b = ttk.Label(mainframe, text="to run \"zig_zag_clicks\"")
    lbl_p1 = ttk.Label(mainframe, text="lag before execution")
    lbl_p2 = ttk.Label(mainframe, text="number of clicks")
    lbl_p3 = ttk.Label(mainframe, text="frequency of clicks")
    lbl_p4 = ttk.Label(mainframe, text="radius of circle")
    lbl_p5 = ttk.Label(mainframe, text="max distance for zig-zag")
    lbl_p6 = ttk.Label(mainframe, text="speed up factor")
    p1_entry = ttk.Entry(mainframe, textvariable=lag)
    p2_entry = ttk.Entry(mainframe, textvariable=n_clicks)
    p3_entry = ttk.Entry(mainframe, textvariable=frequency)
    p4_entry = ttk.Entry(mainframe, textvariable=radius)
    p5_entry = ttk.Entry(mainframe, textvariable=max_step)
    p6_entry = ttk.Entry(mainframe, textvariable=speed_up)

    lbl_keybindings.grid(column=0, row=0, columnspan=2, padx=10, pady=10)
    lbl_parameters.grid(column=2, row=0, columnspan=2, padx=10, pady=10)
    lbl_1.grid(column=0, row=1, padx=5, pady=5)
    lbl_2.grid(column=0, row=2, padx=5, pady=5)
    lbl_3.grid(column=0, row=3, padx=5, pady=5)
    lbl_4.grid(column=0, row=4, padx=5, pady=5)
    lbl_5.grid(column=0, row=5, padx=5, pady=5)
    lbl_6.grid(column=0, row=6, padx=5, pady=5)
    lbl_1_b.grid(column=1, row=1, padx=5, pady=5, sticky=W)
    lbl_2_b.grid(column=1, row=2, padx=5, pady=5, sticky=W)
    lbl_3_b.grid(column=1, row=3, padx=5, pady=5, sticky=W)
    lbl_4_b.grid(column=1, row=4, padx=5, pady=5, sticky=W)
    lbl_5_b.grid(column=1, row=5, padx=5, pady=5, sticky=W)
    lbl_6_b.grid(column=1, row=6, padx=5, pady=5, sticky=W)
    lbl_p1.grid(column=2, row=1, padx=5, pady=5, sticky=W)
    lbl_p2.grid(column=2, row=2, padx=5, pady=5, sticky=W)
    lbl_p3.grid(column=2, row=3, padx=5, pady=5, sticky=W)
    lbl_p4.grid(column=2, row=4, padx=5, pady=5, sticky=W)
    lbl_p5.grid(column=2, row=5, padx=5, pady=5, sticky=W)
    lbl_p6.grid(column=2, row=6, padx=5, pady=5, sticky=W)
    p1_entry.grid(column=3, row=1, padx=5, pady=5, sticky=W)
    p2_entry.grid(column=3, row=2, padx=5, pady=5, sticky=W)
    p3_entry.grid(column=3, row=3, padx=5, pady=5, sticky=W)
    p4_entry.grid(column=3, row=4, padx=5, pady=5, sticky=W)
    p5_entry.grid(column=3, row=5, padx=5, pady=5, sticky=W)
    p6_entry.grid(column=3, row=6, padx=5, pady=5, sticky=W)

    root.bind("<Alt-KeyPress-1>",
              func=lambda event: dispatch(lag.get(), n_clicks.get(), radius.get(), frequency.get(), max_step.get(),
                                          speed_up.get(),
                                          autoclicker, 1))
    root.bind("<Alt-KeyPress-2>",
              func=lambda event: dispatch(lag.get(), n_clicks.get(), radius.get(), frequency.get(), max_step.get(),
                                          speed_up.get(),
                                          autoclicker, 2))
    root.bind("<Alt-KeyPress-3>",
              func=lambda event: dispatch(lag.get(), n_clicks.get(), radius.get(), frequency.get(), max_step.get(),
                                          speed_up.get(),
                                          autoclicker, 3))
    root.bind("<Alt-KeyPress-4>",
              func=lambda event: dispatch(lag.get(), n_clicks.get(), radius.get(), frequency.get(), max_step.get(),
                                          speed_up.get(),
                                          autoclicker, 4))
    root.bind("<Alt-KeyPress-5>",
              func=lambda event: dispatch(lag.get(), n_clicks.get(), radius.get(), frequency.get(), max_step.get(),
                                          speed_up.get(),
                                          autoclicker, 5))
    root.bind("<Alt-KeyPress-6>",
              func=lambda event: dispatch(lag.get(), n_clicks.get(), radius.get(), frequency.get(), max_step.get(),
                                          speed_up.get(),
                                          autoclicker, 6))
    root.mainloop()


def dispatch(lag, n_clicks, radius, frequency, max_distance, speedup, autoclicker: AutoClicker, Key):
    time.sleep(lag)
    if Key == 1:
        autoclicker.spam_clicks(pynput.mouse.Button.left, n_clicks)
    elif Key == 2:
        autoclicker.steady_clicks(pynput.mouse.Button.left, n_clicks, 1 / frequency)
    elif Key == 3:
        autoclicker.quicker_clicks(pynput.mouse.Button.left, n_clicks, 1 / frequency, speedup)
    elif Key == 4:
        autoclicker.circumference_clicks(pynput.mouse.Button.left, n_clicks, radius, 1 / frequency)
    elif Key == 5:
        autoclicker.circle_clicks(pynput.mouse.Button.left, n_clicks, radius, 1 / frequency)
    elif Key == 6:
        autoclicker.zig_zag_clicks(pynput.mouse.Button.left, n_clicks, max_distance, 1 / frequency)
    else:
        print("Unknown Key")


if __name__ == "__main__":
    PROCESS_PER_MONITOR_DPI_AWARE = 2
    ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
    main()

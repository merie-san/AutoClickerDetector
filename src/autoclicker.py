import random
from pynput.mouse import Button, Controller
import time
import math


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
    AutoClicker().quicker_clicks(Button.left, 50, 5, 0.9)


if __name__ == "__main__":
    main()

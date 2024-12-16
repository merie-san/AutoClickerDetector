from pynput import mouse
import ctypes
import csv
import time
import autoclicker
from tkinter import messagebox
from tkinter import *

PROCESS_PER_MONITOR_DPI_AWARE = 2


class TrainingDataGenerator:
    written_rows = 0

    def on_click(cls, x, y, button, pressed, csv_dict_writer: csv.DictWriter, is_auto_clicker, stop):
        """Callback method to record the mouse button event in a csv file through a given csv.DictWriter"""
        data_row = {'time': time.time(), 'x': x, 'y': y, 'button': button, 'pressed': pressed,
                    'abnormal': is_auto_clicker}
        csv_dict_writer.writerow(data_row)
        cls.written_rows += 1
        if cls.written_rows >= stop:
            return False

    def record_normal_clicks(cls, number_clicks, create_file=False):
        """Records a given number of mouse clicks"""
        written_rows = 0
        if create_file:
            modality = 'w'
        else:
            modality = 'a'
        with open('clean_training_data.csv', modality, newline='') as csv_file:
            csv_dict_writer = csv.DictWriter(csv_file, fieldnames=['time', 'x', 'y', 'button', 'pressed', 'abnormal'])
            if create_file:
                csv_dict_writer.writeheader()
            with mouse.Listener(
                    on_click=lambda x, y, button, pressed:
                    cls.on_click(x, y, button, pressed, csv_dict_writer, False, 2 * number_clicks)) as listener:
                listener.join()

    def record_abnormal_clicks(cls, create_file=False):
        """Records a given number of autoclicker-generated clicks"""
        written_rows = 0
        if create_file:
            modality = 'w'
        else:
            modality = 'a'
        with open('clean_training_data.csv', modality, newline='') as csv_file:
            csv_dict_writer = csv.DictWriter(csv_file, fieldnames=['time', 'x', 'y', 'button', 'pressed', 'abnormal'])
            if create_file:
                csv_dict_writer.writeheader()
            number_clicks = 300
            with mouse.Listener(
                    on_click=lambda x, y, button, pressed:
                    cls.on_click(x, y, button, pressed, csv_dict_writer, True, 2 * number_clicks)) as listener:
                clicker = autoclicker.AutoClicker()
                clicker.quicker_clicks(mouse.Button.left, number_clicks, 2, 0.99)
                listener.join()


def main():
    training_data_generator = TrainingDataGenerator()
    root = Tk()
    root.geometry("300x200+50+50")
    root.title("warning")
    text = Label(root, text="recording of normal data is beginning")
    text.pack()
    root.mainloop()
    time.sleep(10)
    training_data_generator.record_normal_clicks(1000)
    root = Tk()
    root.geometry("300x200+50+50")
    root.title("information")
    text = Label(root, text="recording of normal data has concluded")
    text.pack()
    root.mainloop()


if __name__ == "__main__":
    ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
    main()

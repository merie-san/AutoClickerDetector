from pynput import mouse
import ctypes
import csv
import time

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

    def record_normal_clicks(cls, number_clicks):
        """Records a given number of mouse clicks"""
        with open('training_data.csv', 'w', newline='') as csv_file:
            csv_dict_writer = csv.DictWriter(csv_file, fieldnames=['time', 'x', 'y', 'button', 'pressed', 'abnormal'])
            csv_dict_writer.writeheader()
            with mouse.Listener(
                    on_click=lambda x, y, button, pressed:
                    cls.on_click(x, y, button, pressed, csv_dict_writer, False, number_clicks)) as listener:
                listener.join()


def main():
    training_data_generator = TrainingDataGenerator()
    training_data_generator.record_normal_clicks(100)


if __name__ == "__main__":
    ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
    main()

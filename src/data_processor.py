import queue
from queue import Queue
import csv
import math
import threading
import pynput
import time

class DataProcessor:

    def __init__(self, input_queue: Queue, output_queue: Queue, batch_dim):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.batch_dim = batch_dim
        self.should_stop = False
        self.data_batch = []
        self.process_thread = threading.Thread(target=self.process_data)
        self.dict_pressed = None
        self.dict_released = None

    def start(self):
        self.should_stop = False
        self.process_thread.start()

    def stop(self):
        self.should_stop = True
        self.process_thread.join()
        self.process_thread = threading.Thread(target=self.process_data)

    def clean_queue(self):
        while not self.input_queue.qsize() == 0:
            self.input_queue.get_nowait()
        self.dict_pressed = None
        self.dict_released = None

    def process_data(self):
        while True:
            if self.should_stop:
                break
            try:
                if self.dict_pressed is None:
                    self.dict_pressed = self.input_queue.get_nowait()
                if self.dict_released is None:
                    self.dict_released = self.input_queue.get_nowait()
            except queue.Empty:
                time.sleep(0.2)
                continue
            if self.dict_pressed['pressed'] and not self.dict_released['pressed'] and self.dict_pressed['button'] == \
                    self.dict_released[
                        'button']:
                s_time = self.dict_pressed['time']
                duration = self.dict_released['time'] - s_time
                x = self.dict_pressed['x']
                y = self.dict_pressed['y']
                movement = math.hypot(self.dict_released['x'] - x, self.dict_released['y'] - y)
                button = self.dict_pressed['button']
                self.data_batch.append(
                    {'time': s_time, 'duration': duration, 'x': x, 'y': y, 'in-click mov': movement, 'button': button})
                print("processor activity "+str(time.time()))
                self.dict_pressed = None
                self.dict_released = None

            if len(self.data_batch) == self.batch_dim + 1:
                TTNC = []
                mouse_mov_x = []
                mouse_mov_y = []
                mouse_mov_r = []
                mouse_mov_a = []
                mean_dur = 0
                mean_x = 0
                mean_y = 0
                mean_d = 0
                left_ratio = 0

                for i in range(self.batch_dim):
                    TTNC.append(self.data_batch[i + 1]['time'] - self.data_batch[i]['time'])
                    mouse_mov_x.append(self.data_batch[i + 1]['x'] - self.data_batch[i]['x'])
                    mouse_mov_y.append(self.data_batch[i + 1]['y'] - self.data_batch[i]['y'])
                    mouse_mov_r.append(math.hypot(mouse_mov_x[i], mouse_mov_y[i]))
                    mouse_mov_a.append(math.atan2(mouse_mov_y[i], mouse_mov_x[i]))
                    mean_dur += self.data_batch[i]['duration']
                    mean_x += self.data_batch[i]['x']
                    mean_y += self.data_batch[i]['y']
                    mean_d += self.data_batch[i]['in-click mov']
                    if self.data_batch[i]['button'] == pynput.mouse.Button.left:
                        left_ratio += 1

                mean_mov_x = sum(mouse_mov_x) / self.batch_dim
                mean_mov_y = sum(mouse_mov_y) / self.batch_dim
                mean_mov_r = math.hypot(mean_mov_x, mean_mov_y)
                mean_mov_a = math.atan2(mean_mov_y, mean_mov_x)
                mean_TTNC = sum(TTNC) / self.batch_dim
                mean_dur = mean_dur / self.batch_dim
                mean_x = mean_x / self.batch_dim
                mean_y = mean_y / self.batch_dim
                mean_d = mean_d / self.batch_dim
                left_ratio = left_ratio / self.batch_dim

                std_TTNC = 0
                std_dur = 0
                std_x = 0
                std_y = 0
                std_mov_r = 0
                std_mov_a = 0
                std_d = 0

                for i in range(self.batch_dim):
                    std_TTNC += (TTNC[i] - mean_TTNC) ** 2
                    std_mov_r += (mouse_mov_r[i] - mean_mov_r) ** 2
                    std_mov_a += (mouse_mov_a[i] - mean_mov_a) ** 2
                    std_dur += (self.data_batch[i]['duration'] - mean_dur) ** 2
                    std_x += (self.data_batch[i]['x'] - mean_x) ** 2
                    std_y += (self.data_batch[i]['y'] - mean_y) ** 2
                    std_d += (self.data_batch[i]['in-click mov'] - mean_d) ** 2

                std_TTNC = math.sqrt(std_TTNC / self.batch_dim)
                std_mov_r = math.sqrt(std_mov_r / self.batch_dim)
                std_mov_a = math.sqrt(std_mov_a / self.batch_dim)
                std_dur = math.sqrt(std_dur / self.batch_dim)
                std_x = math.sqrt(std_x / self.batch_dim)
                std_y = math.sqrt(std_y / self.batch_dim)
                std_d = math.sqrt(std_d / self.batch_dim)

                self.data_batch = self.data_batch[self.batch_dim:]

                self.output_queue.put(
                    {"mean ttnc": mean_TTNC, "std ttnc": std_TTNC, "mean duration": mean_dur, "std duration": std_dur,
                     "mean x": mean_x, "mean y": mean_y, "std x": std_x, "std y": std_y, "mean mov module": mean_mov_r,
                     "mean mov angle": mean_mov_a, "std mov module": std_mov_r, "std mov angle": std_mov_a,
                     "mean in-click distance": mean_d, "std in-click distance": std_d, "left click ratio": left_ratio})

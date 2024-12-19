import queue

import pandas as pd
import pickle
from tkinter import *
from queue import Queue
import threading
import time


class MachineLearningModel:

    def __init__(self, pickled_model_file_path, pickled_scaler_file_path, queue: Queue, number_of_clicks: IntVar,
                 autoclicker_activity: BooleanVar, data_batch_dim):
        self.data_batch_queue = queue
        self.number_of_clicks = number_of_clicks
        self.autoclicker_activity = autoclicker_activity
        self.should_stop = False
        self.data_batch_dim = data_batch_dim
        self.data_dict = None
        self.model_thread = threading.Thread(target=self.predict_label)
        with open(pickled_model_file_path, "rb") as f, open(pickled_scaler_file_path, "rb") as g:
            self.model = pickle.load(f)
            self.scaler = pickle.load(g)

    def start(self):
        self.should_stop = False
        self.model_thread.start()

    def stop(self):
        self.should_stop = True
        self.model_thread.join()
        self.model_thread = threading.Thread(target=self.predict_label)

    def predict_label(self):
        while True:
            if self.should_stop:
                break
            try:
                self.data_dict = self.data_batch_queue.get_nowait()
            except queue.Empty:
                time.sleep(0.2)
                continue
            data = pd.DataFrame.from_dict(self.data_dict, orient='index').T.to_numpy()
            self.data_dict = None
            data = self.scaler.transform(data)
            prediction = self.model.predict(data)
            self.number_of_clicks.set(self.number_of_clicks.get() + self.data_batch_dim)
            print("model activity " + str(time.time()))
            if prediction[0]:
                self.autoclicker_activity.set(True)
            else:
                self.autoclicker_activity.set(False)

    def clean_queue(self):
        while not self.data_batch_queue.qsize() == 0:
            self.data_batch_queue.get_nowait()
        self.data_dict = None

import queue
from sklearn.pipeline import Pipeline
import pandas as pd
import pickle
from tkinter import *
from queue import Queue
import threading
import time
import csv


class MachineLearningModel:
    """Uses a sklearn model to predict labels of data batches"""

    def __init__(self, pickled_model_file_path, pickled_scaler_file_path, queue: Queue, number_of_clicks: IntVar,
                 autoclicker_activity: BooleanVar, data_batch_dim):
        self.data_batch_queue = queue
        self.number_of_clicks = number_of_clicks
        self.autoclicker_activity = autoclicker_activity
        self.should_stop = False
        self.data_batch_dim = data_batch_dim
        self.data_dict = None
        self.batch_time = None
        self.model_thread = threading.Thread(target=self.predict_label)
        self.csv_file = open('predicted_values.csv', 'w', newline='')
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=['time', 'batch dimension', 'prediction'])
        self.csv_writer.writeheader()
        with open(pickled_model_file_path, "rb") as f, open(pickled_scaler_file_path, "rb") as g:
            model = pickle.load(f)
            scaler = pickle.load(g)
            self.model = Pipeline([('scaler', scaler), ('model', model)])

    def start(self):
        if self.csv_file is None:
            self.csv_file = open('predicted_values.csv', 'a', newline='')
            self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=['time', 'batch dimension', 'prediction'])
        self.should_stop = False
        self.model_thread.start()

    def stop(self):
        self.should_stop = True
        self.model_thread.join()
        self.csv_file.close()
        self.csv_file = None
        self.csv_writer = None
        self.model_thread = threading.Thread(target=self.predict_label)

    def predict_label(self):
        while True:
            if self.should_stop:
                break
            try:
                data_dict_list = self.data_batch_queue.get_nowait()
                self.data_dict = data_dict_list[1]
                self.batch_time = data_dict_list[0]
            except queue.Empty:
                time.sleep(0.2)
                continue
            data = pd.DataFrame.from_dict(self.data_dict, orient='index').T.to_numpy()
            self.data_dict = None
            prediction = self.model.predict(data)
            self.number_of_clicks.set(self.number_of_clicks.get() + self.data_batch_dim)
            self.csv_writer.writerow(
                {'time': self.batch_time['time'], 'batch dimension': self.data_batch_dim, 'prediction': prediction[0]})
            print("model activity " + str(time.time()))
            self.batch_time = None
            if prediction[0]:
                self.autoclicker_activity.set(True)
            else:
                self.autoclicker_activity.set(False)

    def clean_queue(self):
        while not self.data_batch_queue.qsize() == 0:
            self.data_batch_queue.get_nowait()
        self.data_dict = None
        self.batch_time = None

import tkinter
from tkinter import ttk
from tkinter import *
import mouse_monitor
import ctypes
from queue import Queue
import data_processor
import machine_learning_model
from tkinter import messagebox

def halt(model: machine_learning_model.MachineLearningModel, processor: data_processor.DataProcessor,
         monitor: mouse_monitor.MouseMonitor):
    monitor.stop()
    processor.stop()
    model.stop()
    processor.clean_queue()
    model.clean_queue()


def restart(model: machine_learning_model.MachineLearningModel, processor: data_processor.DataProcessor,
            monitor: mouse_monitor.MouseMonitor):
    monitor.start()
    processor.start()
    model.start()


def terminate(root, model: machine_learning_model.MachineLearningModel, processor: data_processor.DataProcessor,
              monitor: mouse_monitor.MouseMonitor, button_describer: tkinter.StringVar):
    if button_describer.get() == "Stop":
        halt(model, processor, monitor)
    root.destroy()


def autoclicker_status_changed(bool_var: tkinter.BooleanVar, string_val: tkinter.StringVar, label: tkinter.Label):
    if bool_var.get():
        string_val.set("Detected")
        label.configure(foreground="red")
        messagebox.showwarning("Autoclicker Detector", "Autoclicker detected")
    else:
        string_val.set("None")
        label.configure(foreground="green")


def button_pressed(string_val: tkinter.StringVar, model: machine_learning_model.MachineLearningModel,
                   processor: data_processor.DataProcessor, monitor: mouse_monitor.MouseMonitor, ):
    if string_val.get() == "Stop":
        string_val.set("Restart")
        halt(model, processor, monitor)
    else:
        string_val.set("Stop")
        restart(model, processor, monitor)


def main():
    root = Tk()
    root.title("Autoclicker Detector")
    mainframe = ttk.Frame(root, padding="8 8 8 8")
    mainframe.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    n_clicks_checked = IntVar()
    n_clicks=IntVar()
    autoclicker_activity = BooleanVar()
    raw_data_queue = Queue()
    proc_data_queue = Queue()
    monitor = mouse_monitor.MouseMonitor(raw_data_queue, n_clicks)
    processor = data_processor.DataProcessor(raw_data_queue, proc_data_queue, 10)
    model = machine_learning_model.MachineLearningModel("mlp_cls.pkl", "scaler.pkl", proc_data_queue, n_clicks_checked,
                                                        autoclicker_activity, 10)
    autoclicker_activity_describer = StringVar(value="None")
    button_describer = StringVar(value="Stop")
    lbl1 = ttk.Label(mainframe, textvariable=n_clicks_checked)
    lbl1.grid(column=1, row=1, padx=5, pady=5)
    lbl2 = ttk.Label(mainframe, text="clicks have been checked in")
    lbl2.grid(column=2, row=1, padx=5, pady=5)
    lbl5=ttk.Label(mainframe, textvariable=n_clicks)
    lbl5.grid(column=3, row=1, padx=5, pady=5)
    lbl3 = ttk.Label(mainframe, text="autoclicker activity:")
    lbl3.grid(column=1, row=2, padx=5, pady=5)
    lbl4 = ttk.Label(mainframe, textvariable=autoclicker_activity_describer, foreground="green")
    lbl4.grid(column=2, row=2, padx=5, pady=5)
    button = ttk.Button(mainframe, textvariable=button_describer,
                        command=lambda: button_pressed(button_describer, model, processor, monitor, ))
    button.grid(column=3, row=3, padx=5, pady=5)
    autoclicker_activity.trace_add(mode="write",
                                   callback=lambda name, index, mode:
                                   autoclicker_status_changed(autoclicker_activity, autoclicker_activity_describer, lbl4))
    root.bind("<Escape>", func=lambda event: terminate(root, model, processor, monitor))
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", func=lambda: terminate(root, model, processor, monitor, button_describer))

    monitor.start()
    processor.start()
    model.start()
    root.mainloop()


if __name__ == "__main__":
    PROCESS_PER_MONITOR_DPI_AWARE = 2
    ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
    main()

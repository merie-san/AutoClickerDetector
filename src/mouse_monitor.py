from tkinter import ttk
from tkinter import *
import tkinter as tk
from tkinter.ttk import *
def end(*args):
    pass
root=Tk()
root.title("Autoclicker Detector")
mainframe=ttk.Frame(root, padding="8 8 8 8")
mainframe.grid(column=0, row=0)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
n_clicks=StringVar()
sus_level=StringVar()
ttk.Label(mainframe, textvariable=n_clicks).grid(column=1, row=1)
ttk.Label(mainframe, text="clicks have been checked").grid(column=2, row=1)
ttk.Label(mainframe, text="autoclicker activity:").grid(column=1, row=2)
ttk.Label(mainframe, textvariable=sus_level).grid(column=2, row=2)
ttk.Button(mainframe, text="Quit", command=end).grid(column=3, row=3)
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)
root.bind("<Return>", end)
root.resizable(False, False)
root.mainloop()
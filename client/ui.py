from queue import Queue
import tkinter as tk
from signals import *

class ServiceWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.status_label = tk.Label(text='Running', foreground='green').pack()


def ui_thread(q: Queue):
    app = ServiceWindow()
    app.master.title('Service window')
    app.master.geometry('400x200')
    app.mainloop()
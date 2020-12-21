from tkinter import *
from tkinter import messagebox

def info_message_box(msg):
    Tk().wm_withdraw() #hide the main window
    messagebox.showinfo('Information', str(msg))
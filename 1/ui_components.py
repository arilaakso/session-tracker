import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from config import *

def create_custom_fonts():
    default_font = tkfont.Font(family="Helvetica", size=FONT_SIZE)
    bold_font = tkfont.Font(family="Helvetica", size=FONT_SIZE, weight="bold")
    fixed_font = tkfont.Font(family="Courier", size=FONT_SIZE)  # Changed to Courier
    return default_font, bold_font, fixed_font

def set_dark_theme(root, default_font):
    root.configure(bg='#2b2b2b')
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TButton', background='#3b3b3b', foreground='white', padding=(10, 5), font=default_font)
    style.map('TButton', background=[('active', '#4b4b4b')])
    style.configure("TScrollbar", background="#4b4b4b", troughcolor="#2b2b2b", bordercolor="#2b2b2b", arrowcolor="white")

def create_listbox(parent, fixed_font):
    listbox_frame = tk.Frame(parent, bg='#2b2b2b')
    listbox_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    listbox = tk.Listbox(listbox_frame, width=LISTBOX_WIDTH, height=LISTBOX_HEIGHT, bg='#333333', fg='white', selectbackground='#555555', font=fixed_font)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    listbox_scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=listbox.yview)
    listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=listbox_scrollbar.set)
    return listbox

def create_summary_text(parent, fixed_font):
    summary_frame = tk.Frame(parent, bg='#2b2b2b')
    summary_frame.pack(pady=10, padx=10, fill=tk.X)

    summary_label = tk.Label(summary_frame, text="Daily Totals", bg='#2b2b2b', fg='white')
    summary_label.pack()

    summary_text_frame = tk.Frame(summary_frame, bg='#2b2b2b')
    summary_text_frame.pack(fill=tk.X, expand=True)

    summary_text = tk.Text(summary_text_frame, width=SUMMARY_WIDTH, height=SUMMARY_HEIGHT, bg='#333333', fg='white', font=fixed_font)
    summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    summary_scrollbar = ttk.Scrollbar(summary_text_frame, orient=tk.VERTICAL, command=summary_text.yview)
    summary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    summary_text.config(yscrollcommand=summary_scrollbar.set)
    return summary_text
import tkinter as tk
from timer_app import SessionTracker

def run_app():
    root = tk.Tk()
    app = SessionTracker(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()
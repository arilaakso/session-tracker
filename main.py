import tkinter as tk
from timer_app import SessionTracker

def run_app():
    root = tk.Tk()
    _ = SessionTracker(root)  # Use underscore to indicate intentional non-use
    root.mainloop()

if __name__ == "__main__":
    run_app()
    
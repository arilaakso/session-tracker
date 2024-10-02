import ctypes
import os
import threading
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import Canvas, ttk
from typing import Any, Dict, Optional

import pandas as pd
import pystray
from PIL import Image, ImageDraw

from config import (BUTTON_WIDTH, CHECK_INTERVAL, IDLE_THRESHOLD, LOG_FILE,
                    WINDOW_HEIGHT, WINDOW_WIDTH)
from ui_components import (create_custom_fonts, create_listbox,
                           create_summary_text, set_dark_theme)

# pylint: disable=attribute-defined-outside-init

class LASTINPUTINFO(ctypes.Structure):
    """Structure to hold last input info for Windows API."""
    _fields_ = [('cbSize', ctypes.c_uint), ('dwTime', ctypes.c_uint)]  # pylint: disable=attribute-defined-outside-init

def get_idle_duration():
    last_input = LASTINPUTINFO()
    last_input.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(last_input))
    millis = ctypes.windll.kernel32.GetTickCount() - last_input.dwTime
    return millis / 1000.0

class SessionTracker:
    """A class representing a session tracking application."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Session Tracker")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        
        self.session_start: Optional[datetime] = None
        self.is_running = False
        self.logs: list[Dict[str, Any]] = []
        self.allow_auto_start = True
        self.idle_threshold = IDLE_THRESHOLD
        self.last_active_time: Optional[datetime] = None

        self.default_font, self.bold_font, self.fixed_font = create_custom_fonts()
        self.root.option_add("*Font", self.default_font)
        set_dark_theme(self.root, self.default_font)
        
        # Initialize UI elements
        self.timer_frame: tk.Frame
        self.start_time_label: tk.Label
        self.duration_label: tk.Label
        self.status_canvas: Canvas
        self.status_indicator: int
        self.control_frame: tk.Frame
        self.start_button: ttk.Button
        self.end_button: ttk.Button
        self.icon_image: Image.Image
        
        self.create_ui()
        self.load_logs()
        self.create_tray_icon()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.update_timer()
        self.check_idle()

    def create_ui(self) -> None:
        self.create_timer_labels()
        self.create_status_indicator()
        self.create_control_buttons()
        self.summary_text = create_summary_text(self.root, self.fixed_font)
        self.listbox = create_listbox(self.root, self.fixed_font)
        self.root.bind("<Unmap>", lambda e: self.root.withdraw() if self.root.state() == 'iconic' else None)

    def create_timer_labels(self) -> None:
        self.timer_frame = tk.Frame(self.root, bg='#2b2b2b')
        self.timer_frame.pack(pady=10, fill=tk.X)

        self.start_time_label = tk.Label(self.timer_frame, text="Start Time: Not started", bg='#2b2b2b', fg='white', font=self.bold_font)
        self.start_time_label.pack(side=tk.LEFT, padx=(10, 0))

        self.duration_label = tk.Label(self.timer_frame, text="Duration: 00:00:00", bg='#2b2b2b', fg='white', font=self.bold_font)
        self.duration_label.pack(side=tk.LEFT, padx=(20, 0))

    def create_status_indicator(self) -> None:
        self.status_canvas = Canvas(self.timer_frame, width=20, height=20, bg='#2b2b2b', highlightthickness=0)
        self.status_canvas.pack(side=tk.LEFT, padx=(20, 10))
        self.status_indicator = self.status_canvas.create_oval(2, 2, 18, 18, fill='red')

    def create_control_buttons(self) -> None:
        self.control_frame = tk.Frame(self.root, bg='#2b2b2b')
        self.control_frame.pack(pady=10)

        self.start_button = ttk.Button(self.control_frame, text="Start", command=self.on_start, width=BUTTON_WIDTH)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.end_button = ttk.Button(self.control_frame, text="End", command=self.on_end, state=tk.DISABLED, width=BUTTON_WIDTH)
        self.end_button.pack(side=tk.LEFT, padx=5)

    def on_start(self) -> None:
        self.allow_auto_start = True
        self.start_session()

    def on_end(self) -> None:
        self.end_session()
        self.allow_auto_start = False

    def start_session(self) -> None:
        if not self.is_running:
            self.session_start = datetime.now()
            self.last_active_time = self.session_start
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.end_button.config(state=tk.NORMAL)
            self.allow_auto_start = True
            self.update_status_indicator()

    def end_session(self, idle_end: bool = False) -> None:
        if self.is_running and self.session_start and self.last_active_time:
            session_end = self.last_active_time if idle_end else datetime.now()
            self.is_running = False
            self.log_session(self.session_start, session_end)
            self.start_button.config(state=tk.NORMAL)
            self.end_button.config(state=tk.DISABLED)
            self.session_start = None
            self.update_status_indicator()
            self.update_timer()

    def update_status_indicator(self) -> None:
        color = 'green' if self.is_running else 'red'
        self.status_canvas.itemconfig(self.status_indicator, fill=color)
        if hasattr(self, 'icon'):
            fill_color = (0, 255, 0) if self.is_running else (255, 0, 0)
            self.icon_image = self.create_icon_image(fill_color)
            self.icon.icon = self.icon_image

    def update_timer(self) -> None:
        if self.is_running and self.session_start:
            current_time = datetime.now()
            duration = current_time - self.session_start
            duration_str = str(duration).split('.', maxsplit=1)[0]  # pylint: disable=C0207
            self.start_time_label.config(text=f"Start Time: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}")
            self.duration_label.config(text=f"Duration: {duration_str}")
        else:
            self.start_time_label.config(text="Start Time: Not started")
            self.duration_label.config(text="Duration: 00:00:00")
        
        self.update_status_indicator()
        self.root.after(1000, self.update_timer)

    def check_idle(self) -> None:
        """
        Check for user idle time and manage sessions accordingly.
        Ends the current session if idle time exceeds the threshold,
        or starts a new session when activity resumes.
        """
        idle_time = get_idle_duration()
        current_time = datetime.now()
        
        if self.is_running:
            if idle_time < self.idle_threshold:
                self.last_active_time = current_time
            elif idle_time >= self.idle_threshold:
                self.end_session(idle_end=True)
        elif self.allow_auto_start:
            if idle_time < self.idle_threshold:
                self.start_session()
                self.last_active_time = current_time
        
        self.root.after(CHECK_INTERVAL, self.check_idle)

    def log_session(self, start: datetime, end: datetime) -> None:
        """Log a completed session to the application's records."""
        weekday = start.strftime("%A")
        duration = end - start
        log_entry = {
            "StartTime": start.strftime("%Y-%m-%d %H:%M:%S"),
            "EndTime": end.strftime("%Y-%m-%d %H:%M:%S"),
            "Weekday": weekday,
            "Duration": str(duration).split('.', maxsplit=1)[0]
        }
        self.logs.insert(0, log_entry)
        self.listbox.insert(0, self.format_log_entry(log_entry))
        self.save_logs()
        self.update_daily_summary()

    def load_logs(self) -> None:
        """Load existing session logs from file."""
        if os.path.exists(LOG_FILE):
            df = pd.read_csv(LOG_FILE, sep=';')
            df = df.sort_values(by='StartTime', ascending=False)
            self.logs = df.to_dict('records')
            for log_entry in self.logs:
                self.listbox.insert(tk.END, self.format_log_entry(log_entry))
        else:
            with open(LOG_FILE, 'w', encoding='utf-8') as file:
                file.write("StartTime;EndTime;Weekday;Duration\n")
        self.update_daily_summary()

    def save_logs(self) -> None:
        df = pd.DataFrame(self.logs)
        df = df.sort_values(by='StartTime', ascending=False)
        df.to_csv(LOG_FILE, sep=';', index=False, mode='w')

    def format_log_entry(self, log_entry: Dict[str, Any]) -> str:
        start = datetime.strptime(log_entry['StartTime'], "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(log_entry['EndTime'], "%Y-%m-%d %H:%M:%S")
        weekday = start.strftime("%a")[:3]
        duration = datetime.strptime(log_entry['Duration'], "%H:%M:%S")
        
        return f"{start.strftime('%Y-%m-%d')} {weekday} {start.strftime('%H:%M')} - {end.strftime('%H:%M')} ({duration.strftime('%H:%M:%S')})"

    def update_daily_summary(self) -> None:
        """
        Update the daily summary of tracked sessions.
        Calculates total time and session count for each day.
        """
        daily_totals: Dict[str, Dict[str, Any]] = {}
        for log in self.logs:
            date = log['StartTime'].split()[0]
            weekday = log['Weekday']
            try:
                duration = datetime.strptime(log['Duration'], "%H:%M:%S")
                total_seconds = duration.hour * 3600 + duration.minute * 60 + duration.second
            except ValueError:
                continue
            
            if date in daily_totals:
                daily_totals[date]['total_seconds'] += total_seconds
                daily_totals[date]['session_count'] += 1
            else:
                daily_totals[date] = {
                    'total_seconds': total_seconds,
                    'weekday': weekday,
                    'session_count': 1
                }

        summary_text = "Date       | Weekday   | Total Time | Sessions\n"
        summary_text += "-" * 50 + "\n"
        
        for date, data in sorted(daily_totals.items(), reverse=True):
            total_duration = str(timedelta(seconds=data['total_seconds'])).split('.', maxsplit=1)[0]
            weekday = data['weekday'][:9].ljust(9)
            session_count = str(data['session_count']).rjust(8)
            summary_text += f"{date} | {weekday} | {total_duration:<10} | {session_count}\n"

        self.summary_text.delete('1.0', tk.END)
        self.summary_text.insert(tk.END, summary_text)

    def create_tray_icon(self) -> None:
        self.icon_image = self.create_icon_image((255, 0, 0))
        menu = pystray.Menu(
            pystray.MenuItem("Show", self.show_window, default=True),
            pystray.MenuItem("Exit", self.on_close)  # Changed from self.exit_app to self.on_close
        )
        self.icon = pystray.Icon("session_tracker", self.icon_image, "Session Tracker", menu)
        
        def setup(icon: 'pystray.Icon') -> None: # type: ignore
            icon.visible = True
        
        self.icon_thread = threading.Thread(target=self.icon.run, args=(setup,))
        self.icon_thread.daemon = True
        self.icon_thread.start()

    def create_icon_image(self, inner_color: tuple[int, int, int]) -> Image.Image:
        """
        Create an image for the system tray icon.
        Returns a circular icon with the specified inner color.
        """
        width = 64
        height = 64
        color1 = (0, 0, 0)
        image = Image.new('RGB', (width, height), color=(0, 0, 0))
        dc = ImageDraw.Draw(image)
        dc.ellipse([0, 0, width, height], fill=color1)
        dc.ellipse([int(width/4), int(height/4), int(width*3/4), int(height*3/4)], fill=inner_color)
        return image

    def show_window(self) -> None:
        """
        Toggle the visibility of the application window.
        Shows the window if it's hidden, hides it if it's visible.
        """
        self.root.after(0, self._toggle_window_visibility)

    def _toggle_window_visibility(self) -> None:
        if self.root.state() == 'withdrawn' or self.root.state() == 'iconic':
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            self.root.state('normal')
        else:
            self.root.withdraw()

    def on_close(self) -> None:
        if self.is_running:
            self.end_session()
        if hasattr(self, 'icon'):
            self.icon.stop()
        if hasattr(self, 'icon_thread') and self.icon_thread.is_alive():
            self.icon_thread.join(timeout=1.0)
        self.root.quit()
        self.root.destroy()

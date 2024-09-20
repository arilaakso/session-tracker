# Configuration parameters

# The file where session logs will be stored
LOG_FILE = "session_logs.csv"

# The time (in seconds) after which the user is considered idle
# A higher value means the app will wait longer before ending a session due to inactivity
# Idling is monitored using the Windows API's GetLastInputInfo function.
IDLE_THRESHOLD = 470  # seconds

# How often the app checks for user activity (in milliseconds)
# Lower values increase responsiveness but may slightly increase CPU usage
CHECK_INTERVAL = 5000  # milliseconds

FONT_SIZE = 12
BUTTON_WIDTH = 15
LISTBOX_HEIGHT = 5
SUMMARY_HEIGHT = 8

WINDOW_WIDTH = 550
WINDOW_HEIGHT = 450
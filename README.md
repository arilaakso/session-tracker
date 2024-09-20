# Session Tracker

Session Tracker is a simple, user-friendly application designed to help you monitor and log your work sessions automatically. It tracks your active time on the computer and provides a summary of your daily activities.

## Features

- Automatic session tracking based on user activity
- Manual start and stop controls
- Daily summary of work sessions
- System tray icon for easy access
- Dark mode interface

## Requirements

To run the Session Tracker, you need:

- Python 3.7 or higher
- tkinter (usually comes pre-installed with Python)
- pandas
- pystray
- Pillow (PIL)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/session-tracker.git
   cd session-tracker
   ```

2. Install the required packages:
   ```bash
   pip install pandas pystray Pillow
   ```

## Usage

Run the application using Python:

```
python main.py
```

The application will start and minimize to the system tray. You can access it by clicking on the tray icon.

- The session will start automatically when user activity is detected.
- You can manually start or end a session using the buttons in the main window.
- The application will automatically end a session after a period of inactivity.
- Daily summaries and session logs can be viewed in the main window.

## Configuration

You can customize the application behavior by modifying the `config.ini` file:

- `LOG_FILE`: Name of the file where session data is stored
- `IDLE_THRESHOLD`: Time in seconds before a session is considered inactive (default: 470 seconds)
- `CHECK_INTERVAL`: Interval in milliseconds to check for user activity (default: 5000 ms)

## Limitations

Please note the following limitations of the Session Tracker:

- The application considers user activity based only on mouse movements and keyboard input.
- Activities that don't involve mouse or keyboard interaction (such as watching a movie or participating in a video call) may be interpreted as inactivity, potentially causing the session to end prematurely.
- Even during video calls, if you're not actively using the mouse or keyboard, the application may consider this as idle time.
- If you're engaged in tasks that don't require frequent mouse or keyboard input, you may need to interact with the device periodically to prevent the session from ending.

## Troubleshooting

If you encounter any issues:

1. Ensure all required packages are installed correctly.
2. Check the log file for any error messages.
3. Make sure you have the necessary permissions to write to the log file location.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## File Structure

- `main.py`: The entry point of the application
- `timer_app.py`: Contains the core functionality of the session tracker
- `ui_components.py`: Defines the user interface components
- `config.py`: Handles configuration loading and management
- `config.ini`: Configuration file (make sure to remove any sensitive information before committing)

## Development

To set up the development environment:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. Install the development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

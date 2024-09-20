# Session Tracker

Session Tracker is a simple, user-friendly application designed to help you monitor and log your work sessions automatically. It tracks your active time on the computer and provides a summary of your daily activities.

## Features

- Automatic session tracking based on user activity
- Manual start and stop controls
- Daily summary of work sessions
- Detailed log of individual sessions
- System tray icon for easy access
- Dark mode interface

## Limitations

- The application currently detects user activity based only on mouse movement and keyboard input.
- Passive activities (e.g., watching videos, reading) without input may be incorrectly logged as idle time.
- Session tracking may not be accurate if the computer goes to sleep or hibernates.

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

You can customize the application behavior by modifying the `config.py` file:

- Adjust the inactivity threshold
- Change the log file location
- Customize the dark mode colors

## Troubleshooting

If you encounter any issues:

1. Ensure all required packages are installed correctly.
2. Check the log file for any error messages.
3. Make sure you have the necessary permissions to write to the log file location.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all contributors who have helped improve this project.
- Inspired by the need for a simple, automated time-tracking solution.

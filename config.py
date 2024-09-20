import configparser
import os

config = configparser.ConfigParser()
config_file = 'config.ini'

# Check if config.ini exists, if not create it with default values
if not os.path.exists(config_file):
    config['Files'] = {'LOG_FILE': 'session_logs.csv'}
    config['Timing'] = {'IDLE_THRESHOLD': '470', 'CHECK_INTERVAL': '5000'}
    config['UI'] = {
        'FONT_SIZE': '12',
        'BUTTON_WIDTH': '15',
        'LISTBOX_HEIGHT': '5',
        'SUMMARY_HEIGHT': '8',
        'WINDOW_WIDTH': '550',
        'WINDOW_HEIGHT': '450'
    }
    with open(config_file, 'w') as configfile:
        config.write(configfile)

config.read(config_file)

# Read values from config.ini
LOG_FILE = config.get('Files', 'LOG_FILE')
IDLE_THRESHOLD = config.getint('Timing', 'IDLE_THRESHOLD')
CHECK_INTERVAL = config.getint('Timing', 'CHECK_INTERVAL')
FONT_SIZE = config.getint('UI', 'FONT_SIZE')
BUTTON_WIDTH = config.getint('UI', 'BUTTON_WIDTH')
LISTBOX_HEIGHT = config.getint('UI', 'LISTBOX_HEIGHT')
SUMMARY_HEIGHT = config.getint('UI', 'SUMMARY_HEIGHT')
WINDOW_WIDTH = config.getint('UI', 'WINDOW_WIDTH')
WINDOW_HEIGHT = config.getint('UI', 'WINDOW_HEIGHT')

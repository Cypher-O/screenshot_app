# config.py
import os

# Application constants
APPLICATION_NAME = "Screenshot App"
ICON_PATH = "assets/icon.ico"
PLACEHOLDER_IMAGE = "assets/screenshot_placeholder.png"
SCREENSHOT_SOUND = "assets/screenshot.wav"
SCREENSHOTS_DIR_NAME = "Screenshots"

# Window titles and messages
SELECT_WINDOW_TITLE = "Select Window"
SELECT_WINDOW_PROMPT = "Select a window:"
NO_WINDOWS_FOUND = "No windows found."
NO_OPEN_WINDOWS_FOUND = "No open windows found."
NOTIFICATION_ERROR_TITLE = "Notification Error"
NOTIFICATION_ERROR_MESSAGE = "Neither dbus nor plyer notification support is available."
DBUS_ERROR_MESSAGE = "DBus Error: "
FULL_SCREEN_TOOLTIP = "Capture entire screen"
SELECT_AREA_TOOLTIP = "Capture a selected area"
SELECT_WINDOW_TOOLTIP = "Capture a selected window"
SCREENSHOT_CAPTURED_TITLE = "Screenshot Captured"
SCREENSHOT_CAPTURED_MESSAGE = "You can paste the image from the clipboard"
SCREENSHOT_FAILED_TITLE = "Screenshot Failed"
FULL_SCREEN_CAPTURE_FAILED_MESSAGE = "Failed to take full-screen screenshot."
WINDOW_CAPTURE_FAILED_MESSAGE = "Failed to take window screenshot."
AREA_CAPTURE_FAILED_MESSAGE = "Failed to crop area: "
WINDOW_LIST_FAILED = "Failed to list windows: "
SCREENSHOT_FAILED = "Failed to take screenshot"
WINDOW_GEOMETRY_FAILED = "Failed to get window geometry";
SCREENSHOT_IN_CLIPBOARD_FAILED = "Failed to place screenshot in clipboard:";

# Notification titles
SCREENSHOT_NOTIFICATION_TITLE = "Screenshot Captured"
SCREENSHOT_NOTIFICATION_MESSAGE = "You can paste the image from the clipboard"

# Screenshot file naming
SCREENSHOT_FILENAME_FORMAT = "Screenshot_from_%Y-%m-%d_%H-%M-%S.png"

# Other messages
ERROR_MESSAGE = "Error"
LOADING_PIXMAP_FAILED = "Failed to load screenshot pixmap."

# Default directories
PICTURES_DIR = os.path.join(os.path.expanduser("~"), "Pictures")
SCREENSHOTS_DIR = os.path.join(PICTURES_DIR, "Screenshots")

# Overlay settings
DIM_OPACITY = 0.08
DIM_COLOR = "rgba(0, 0, 0, 150)"

# Screenshot settings
FULL_SCREEN_DELAY = 500  # milliseconds
SELECTION_AREA_DELAY = 300  # milliseconds

# Notification settings
NOTIFICATION_TIMEOUT = 10  # seconds

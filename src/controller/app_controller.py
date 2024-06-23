import sys
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtWidgets import QApplication
from model.screenshot_handler import ScreenshotHandler
from utils.notification_handler import NotificationHandler
from view.app_view import AppView
from utils.config import FULL_SCREEN_TOOLTIP, SELECT_AREA_TOOLTIP, SELECT_WINDOW_TOOLTIP, SCREENSHOT_CAPTURED_TITLE, SCREENSHOT_CAPTURED_MESSAGE, SCREENSHOT_FAILED_TITLE, APPLICATION_NAME, FULL_SCREEN_CAPTURE_FAILED_MESSAGE, WINDOW_CAPTURE_FAILED_MESSAGE, SCREENSHOT_FAILED

class AppController:

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName(APPLICATION_NAME)

        self.view = AppView()
        self.view.show()  # Show the view here

        self.screenshot_handler = ScreenshotHandler()
        self.notification_handler = NotificationHandler()
        # self.sound_effect = QSoundEffect()
        # self.sound_effect.setSource(QUrl.fromLocalFile("assets/screenshot.wav"))  # Replace with your sound file

        self.connect_signals()

    def connect_signals(self):
        self.view.full_screen_button.clicked.connect(self.take_full_screen)
        self.view.area_button.clicked.connect(self.select_area)
        self.view.window_button.clicked.connect(self.select_window)
        self.screenshot_handler.finished.connect(self.on_screenshot_finished)

    def take_full_screen(self):
        self.view.showMinimized()  # Minimize the main window

        # Show dimming overlay before capturing screenshot
        self.screenshot_handler.dim_overlay.show()

        # Delay to ensure window minimizes properly before taking screenshot
        QTimer.singleShot(300, self.prepare_full_screen_capture)

    def prepare_full_screen_capture(self):
        # Hide the overlay to avoid capturing it
        self.screenshot_handler.dim_overlay.hide()

        # Additional delay to ensure the overlay is hidden before capturing
        QTimer.singleShot(500, self.capture_full_screen)  # Increased delay to 500ms

    def capture_full_screen(self):
        save_path = self.screenshot_handler.take_full_screen()

        if save_path:
            self.screenshot_handler.place_screenshot_in_clipboard(save_path)
            self.view.update_image(save_path)
            self.notification_handler.show_notification(SCREENSHOT_CAPTURED_TITLE, SCREENSHOT_CAPTURED_MESSAGE)
        else:
            self.notification_handler.show_notification(SCREENSHOT_FAILED_TITLE, FULL_SCREEN_CAPTURE_FAILED_MESSAGE)

        # Restore the main window
        self.view.showNormal()
        self.view.activateWindow()

    def select_area(self):
        self.view.showMinimized()  # Minimize the main window
        self.screenshot_handler.select_area()

    def select_window(self):
        save_path = self.screenshot_handler.select_window()
        if save_path:
            self.screenshot_handler.place_screenshot_in_clipboard(save_path)
            self.view.update_image(save_path)
            self.notification_handler.show_notification(SCREENSHOT_CAPTURED_TITLE, SCREENSHOT_CAPTURED_MESSAGE)
        else:
            self.notification_handler.show_notification(SCREENSHOT_FAILED_TITLE, WINDOW_CAPTURE_FAILED_MESSAGE)

    def on_screenshot_finished(self, save_path):
        self.view.showNormal()  # Restore the main window
        self.view.activateWindow()  # Bring the main window to the foreground
        if save_path:
            self.view.update_image(save_path)
            self.notification_handler.show_notification(SCREENSHOT_CAPTURED_TITLE, SCREENSHOT_CAPTURED_MESSAGE)
        else:
            self.notification_handler.show_notification(SCREENSHOT_FAILED_TITLE, SCREENSHOT_FAILED)

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_V and event.modifiers() & Qt.ControlModifier:
    #         self.screenshot_handler.paste_image_from_clipboard()
    #     else:
    #         super().keyPressEvent(event)

if __name__ == "__main__":
    controller = AppController()
    sys.exit(app.exec_())

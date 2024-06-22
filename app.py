import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QFileDialog, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt, QRect, QTimer
from screenshot import ScreenshotHandler
from notification import NotificationHandler

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Screenshot App'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        QApplication.setApplicationName(self.title)
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(100, 100, 400, 300)

        self.screenshot_handler = ScreenshotHandler()
        self.notification_handler = NotificationHandler()
        self.screenshot_handler.finished.connect(self.showAfterCapture)

        self.label = QLabel(self)
        self.label.setGeometry(10, 10, 380, 280)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setPixmap(QPixmap('screenshot_placeholder.png'))

        full_screen_button = QPushButton('Full Screen', self)
        full_screen_button.setToolTip('Capture entire screen')
        full_screen_button.move(20, 260)
        full_screen_button.clicked.connect(self.takeFullScreen)

        area_button = QPushButton('Select Area', self)
        area_button.setToolTip('Capture a selected area')
        area_button.move(120, 260)
        area_button.clicked.connect(self.selectArea)

        window_button = QPushButton('Select Window', self)
        window_button.setToolTip('Capture a specific window')
        window_button.move(240, 260)
        window_button.clicked.connect(self.selectWindow)

        self.show()

    def takeFullScreen(self):
        save_path = self.screenshot_handler.takeFullScreen()
        self.showNotificationIfValid(save_path)

    def selectArea(self):
        self.hide()
        self.screenshot_handler.selectArea()

    def selectWindow(self):
        save_path = self.screenshot_handler.selectWindow()
        if save_path:
            self.showAfterCapture(save_path)
            self.showNotificationIfValid(save_path)

    def showAfterCapture(self, save_path):
        self.show()
        self.showNotificationIfValid(save_path)

    def showNotificationIfValid(self, save_path):
        if save_path:
            self.notification_handler.showNotification("Screenshot Captured", "You can paste the image from the clipboard.")
            self.label.setPixmap(QPixmap(save_path).scaled(380, 280, Qt.KeepAspectRatio))

    def closeEvent(self, event):
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
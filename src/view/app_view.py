from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QDesktopWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

class AppView(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Screenshot App'
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('assets/icon.png'))
        self.setGeometry(100, 100, 400, 300)

        self.label = QLabel(self)
        self.label.setGeometry(10, 10, 380, 280)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setPixmap(QPixmap('assets/screenshot_placeholder.png'))

        self.full_screen_button = QPushButton('Full Screen', self)
        self.full_screen_button.setToolTip('Capture entire screen')
        self.full_screen_button.move(20, 260)

        self.area_button = QPushButton('Select Area', self)
        self.area_button.setToolTip('Capture a selected area')
        self.area_button.move(120, 260)

        self.window_button = QPushButton('Select Window', self)
        self.window_button.setToolTip('Capture a selected window')
        self.window_button.move(220, 260)

        self.center()
        self.show()
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def update_image(self, image_path):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            pixmap = QPixmap('screenshot_placeholder.png')
        self.label.setPixmap(pixmap.scaled(self.label.size(), Qt.KeepAspectRatio))

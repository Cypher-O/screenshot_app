from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QDesktopWidget, QHBoxLayout, QVBoxLayout
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
        self.setGeometry(100, 100, 600, 500)  # Increased window size

        # Central widget container
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Image label with more space
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMinimumSize(500, 400)  # Set a minimum size for the image label
        self.label.setPixmap(QPixmap('assets/screenshot_placeholder.png'))
        main_layout.addWidget(self.label, alignment=Qt.AlignCenter)

        # Button container layout
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)

        # Full Screen button
        self.full_screen_button = QPushButton('Full Screen')
        self.full_screen_button.setToolTip('Capture entire screen')
        button_layout.addWidget(self.full_screen_button)

        # Select Area button
        self.area_button = QPushButton('Select Area')
        self.area_button.setToolTip('Capture a selected area')
        button_layout.addWidget(self.area_button)

        # Select Window button
        self.window_button = QPushButton('Select Window')
        self.window_button.setToolTip('Capture a selected window')
        button_layout.addWidget(self.window_button)

        # Center the window on the screen
        self.center()

        # Show the window
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def update_image(self, image_path):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            pixmap = QPixmap('assets/screenshot_placeholder.png')
        self.label.setPixmap(pixmap.scaled(self.label.size(), Qt.KeepAspectRatio))

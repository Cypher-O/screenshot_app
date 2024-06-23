from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QBrush
from PyQt5.QtWidgets import QWidget, QApplication
from utils.config import DIM_COLOR

class DimOverlay(QWidget):
    def __init__(self):
        super().__init__(flags=Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 150);")
        self.setGeometry(QApplication.desktop().availableGeometry())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QBrush(QColor(0, 0, 0, 150)))

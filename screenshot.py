import os
import sys
import subprocess
from datetime import datetime
import pyautogui
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject, QRect, QPoint, QSize
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget, QRubberBand, QMainWindow, QApplication 
from PyQt5.QtGui import QPixmap, QPainter, QColor, QCursor


class SelectAreaWidget(QWidget):
    selection_made = pyqtSignal(QRect)

    def __init__(self):
        super().__init__()
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        self.setWindowOpacity(0.3)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCursor(QCursor(Qt.CrossCursor)) 

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.origin = event.pos()
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()

    def mouseMoveEvent(self, event):
        if not self.origin.isNull():
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.selection_made.emit(self.rubberBand.geometry())
            self.rubberBand.hide()
            self.close()

class ScreenshotHandler(QObject):
    finished = pyqtSignal(str)  # Signal emitted after screenshot capture

    def __init__(self):
        super().__init__()
        self.pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
        self.screenshots_dir = self.find_or_create_screenshots_dir(self.pictures_dir)

    def find_or_create_screenshots_dir(self, pictures_dir):
        screenshots_dir = os.path.join(pictures_dir, "Screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        return screenshots_dir

    def takeFullScreen(self):
        timestamp = datetime.now().strftime("Screenshot_from_%Y-%m-%d_%H-%M-%S.png")
        save_path = os.path.join(self.screenshots_dir, timestamp)

        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(save_path)
            return save_path
        except Exception as e:
            print(f"Failed to take screenshot: {str(e)}")
            return None

    def selectArea(self):
        self.selection_widget = SelectAreaWidget()
        self.selection_widget.selection_made.connect(self.crop_area)
        self.selection_widget.showFullScreen()

    def crop_area(self, rect):
        try:
            screen = QApplication.primaryScreen()
            screenshot = screen.grabWindow(0, rect.x(), rect.y(), rect.width(), rect.height())
            timestamp = datetime.now().strftime("Screenshot_from_%Y-%m-%d_%H-%M-%S.png")
            save_path = os.path.join(self.screenshots_dir, timestamp)
            screenshot.save(save_path)
            self.finished.emit(save_path)
        except Exception as e:
            print(f"Failed to crop area: {str(e)}")
            self.finished.emit(None)

    def selectWindow(self):
        if not self.is_linux():
            return None

        windows = self.list_windows()

        if windows:
            window_titles = [win['title'] for win in windows]
            selected, ok = QInputDialog.getItem(None, "Select Window", "Select a window:", window_titles, 0, False)

            if ok and selected:
                selected_window = next(win for win in windows if win['title'] == selected)
                save_path = self.capture_window(selected_window['id'])
                return save_path
        else:
            QMessageBox.warning(None, "No Windows Found", "No open windows found.")

        return None

    def list_windows(self):
        try:
            result = subprocess.run(['wmctrl', '-l'], capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')

            windows = []
            for line in lines:
                parts = line.split(maxsplit=3)
                if len(parts) >= 4:
                    window = {
                        'id': parts[0],
                        'desktop': parts[1],
                        'host': parts[2],
                        'title': parts[3]
                    }
                    windows.append(window)

            return windows
        except Exception as e:
            print(f"Failed to list windows: {str(e)}")
            return []

    def capture_window(self, window_id):
        try:
            # Use xwininfo and imagemagick to capture the window without bringing it to the front
            xwininfo_output = subprocess.check_output(['xwininfo', '-id', window_id]).decode()
            geometry = self.parse_geometry(xwininfo_output)

            if geometry:
                timestamp = datetime.now().strftime("Screenshot_from_%Y-%m-%d_%H-%M-%S.png")
                save_path = os.path.join(self.screenshots_dir, timestamp)
                subprocess.run(['import', '-window', window_id, save_path])
                self.finished.emit(save_path)
                return save_path
            else:
                print("Failed to get window geometry.")
                return None
        except Exception as e:
            print(f"Failed to capture window {window_id}: {str(e)}")
            return None

    def parse_geometry(self, xwininfo_output):
        lines = xwininfo_output.splitlines()
        geometry = {}
        for line in lines:
            if "Width:" in line:
                geometry['width'] = int(line.split()[-1])
            if "Height:" in line:
                geometry['height'] = int(line.split()[-1])
            if "Absolute upper-left X:" in line:
                geometry['x'] = int(line.split()[-1])
            if "Absolute upper-left Y:" in line:
                geometry['y'] = int(line.split()[-1])
        return geometry if 'width' in geometry and 'height' in geometry and 'x' in geometry and 'y' in geometry else None

    def is_linux(self):
        return sys.platform.startswith('linux')
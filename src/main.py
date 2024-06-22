import sys
from PyQt5.QtWidgets import QApplication
from controller.app_controller import AppController

def main():
    app = QApplication([])
    app.setApplicationName("Screenshot App")
    controller = AppController()
    app.exec_()

if __name__ == "__main__":
    main()
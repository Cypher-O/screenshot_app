import sys
import os
from PyQt5.QtWidgets import QApplication
from controller.app_controller import AppController
from PyQt5.QtGui import QIcon
from utils.config import APPLICATION_NAME, ICON_PATH

def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APPLICATION_NAME)

    try:
        # Set the application icon
        if os.path.exists(ICON_PATH):
            app_icon = QIcon(ICON_PATH)
            app.setWindowIcon(app_icon)
            print(f"Application icon set: {app_icon}")
            print(f"Icon exists: {not app_icon.isNull()}")
        else:
            print(f"Icon file does not exist: {icon_path}")

        controller = AppController()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Failed to load icon: {e}")

if __name__ == "__main__":
    main()

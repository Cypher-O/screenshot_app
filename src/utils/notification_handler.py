import sys
from PyQt5.QtWidgets import QMessageBox

try:
    import dbus
    from dbus.mainloop.qt import DBusQtMainLoop
    DBusQtMainLoop(set_as_default=True)
except ImportError:
    dbus = None

try:
    from plyer import notification as plyer_notification
except ImportError:
    plyer_notification = None

from utils.config import NOTIFICATION_ERROR_TITLE, NOTIFICATION_ERROR_MESSAGE, DBUS_ERROR_MESSAGE, SCREENSHOT_NOTIFICATION_TITLE, SCREENSHOT_NOTIFICATION_MESSAGE, APPLICATION_NAME

class NotificationHandler:

    def __init__(self):
        pass

    def show_notification(self, title, message):
        if dbus:
            self._show_dbus_notification(title, message)
        elif plyer_notification:
            self._show_plyer_notification(title, message)
        else:
            QMessageBox.warning(None, NOTIFICATION_ERROR_TITLE, NOTIFICATION_ERROR_MESSAGE)

    def _show_dbus_notification(self, title, message):
        try:
            bus = dbus.SessionBus()
            notifications = bus.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
            interface = dbus.Interface(notifications, 'org.freedesktop.Notifications')
            
            app_name = QApplication.applicationName() 
            interface.Notify(APPLICATION_NAME, 0, '', title, message, [], {}, -1)
        except dbus.exceptions.DBusException as e:
            print(f"{DB} {e}")
            if plyer_notification:
                self._show_plyer_notification(title, message)

    def _show_plyer_notification(self, title, message):
        plyer_notification.notify(
            title=title,
            message=message,
            app_name=APPLICATION_NAME,
            timeout=10,
        )

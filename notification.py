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

class NotificationHandler:

    def __init__(self):
        pass

    def showNotification(self, title, message):
        if dbus:
            self._showDBusNotification(title, message)
        elif plyer_notification:
            self._showPlyerNotification(title, message)
        else:
            QMessageBox.warning(None, "Notification Error", "Neither dbus nor plyer notification support is available.")

    def _showDBusNotification(self, title, message):
        try:
            bus = dbus.SessionBus()
            notifications = bus.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
            interface = dbus.Interface(notifications, 'org.freedesktop.Notifications')

            notification_id = interface.Notify('Screenshot App', 0, '', title, message, [], {}, -1)

        except dbus.exceptions.DBusException as e:
            print(f"DBus Error: {e}")
            if plyer_notification:
                self._showPlyerNotification(title, message)

    def _showPlyerNotification(self, title, message):
        plyer_notification.notify(
            title=title,
            message=message,
            app_name='Screenshot App',
            timeout=10,
        )

if __name__ == '__main__':
    # Test notification handlers
    handler = NotificationHandler()
    handler.showNotification("Test Title", "Test Message")

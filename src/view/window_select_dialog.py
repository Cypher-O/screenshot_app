from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QDialogButtonBox, QLabel, QListWidgetItem
from PyQt5.QtCore import Qt
from utils.config import SELECT_WINDOW_TITLE, SELECT_WINDOW_PROMPT

class WindowSelectDialog(QDialog):
    def __init__(self, windows, parent=None):
        super().__init__(parent)
        self.setWindowTitle(SELECT_WINDOW_TITLE)
        
        self.list_widget = QListWidget()
        for win in windows:
            item = QListWidgetItem(win['title'])
            item.setData(Qt.UserRole, win['id'])  # Store window ID as item data
            self.list_widget.addItem(item)
        
        self.label = QLabel(SELECT_WINDOW_PROMPT)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.button_box)
        self.setLayout(layout)
        
    def selected_window_id(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            return selected_item.data(Qt.UserRole)
        return None

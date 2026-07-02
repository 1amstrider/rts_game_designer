"""
Age Panel widget for managing ages.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QListWidgetItem, QPushButton, QLineEdit, QLabel,
    QMenu, QInputDialog, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QAction


class AgePanel(QWidget):
    """Widget for displaying and managing ages."""

    # Signals
    age_selected = Signal(str)  # age_id
    age_created = Signal(str)   # name
    age_renamed = Signal(str, str)  # age_id, new_name
    age_deleted = Signal(str)   # age_id

    def __init__(self):
        super().__init__()
        self.ages = []
        self.selected_age_id = None
        self._setup_ui()

    def _setup_ui(self):
        """Setup the age panel UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Header
        header = QHBoxLayout()
        title = QLabel("Ages")
        title.setStyleSheet("font-weight: 700; font-size: 13px; color: #ebf0f8;")
        header.addWidget(title)

        self.add_age_btn = QPushButton("+")
        self.add_age_btn.setFixedSize(28, 28)
        self.add_age_btn.setToolTip("Add Age")
        self.add_age_btn.clicked.connect(self._on_add_age)
        self.add_age_btn.setStyleSheet("""
            QPushButton {
                background-color: #182131;
                border: 1px solid #2b3648;
                border-radius: 6px;
                color: #ebf0f8;
                font-size: 16px;
            }
            QPushButton:hover {
                border-color: #6ea8fe;
                background-color: #20293a;
            }
        """)
        header.addStretch()
        header.addWidget(self.add_age_btn)
        layout.addLayout(header)

        # Age list
        self.age_list = QListWidget()
        self.age_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                border: 1px solid #2b3648;
                border-radius: 8px;
                padding: 8px 12px;
                margin: 2px;
                background-color: #20293a;
                color: #ebf0f8;
            }
            QListWidget::item:hover {
                border-color: #6ea8fe;
                background-color: #2a3548;
            }
            QListWidget::item:selected {
                border-color: #6ea8fe;
                background-color: rgba(110, 168, 254, 0.16);
            }
        """)
        self.age_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.age_list.customContextMenuRequested.connect(self._show_context_menu)
        self.age_list.currentItemChanged.connect(self._on_selection_changed)
        layout.addWidget(self.age_list, 1)

    def update_ages(self, ages: list, selected_id: str = None):
        """Update the age list."""
        self.ages = ages
        self.age_list.clear()

        for age in ages:
            age_id = age.get('id', age.get('name', ''))
            name = age.get('name', 'Unnamed Age')
            count = age.get('hero_count', 0)

            item = QListWidgetItem()
            item.setData(Qt.UserRole, age_id)

            widget = QWidget()
            item_layout = QHBoxLayout(widget)
            item_layout.setContentsMargins(8, 4, 8, 4)
            item_layout.setSpacing(8)

            name_label = QLabel(name)
            name_label.setStyleSheet("font-weight: 600; font-size: 13px;")
            item_layout.addWidget(name_label)

            item_layout.addStretch()

            count_badge = QLabel(str(count))
            count_badge.setStyleSheet("""
                QLabel {
                    background-color: rgba(142, 240, 200, 0.14);
                    border: 1px solid rgba(142, 240, 200, 0.25);
                    border-radius: 10px;
                    padding: 2px 8px;
                    color: #b9ffe6;
                    font-size: 11px;
                }
            """)
            item_layout.addWidget(count_badge)

            item.setSizeHint(widget.sizeHint())
            self.age_list.addItem(item)
            self.age_list.setItemWidget(item, widget)

            if selected_id and age_id == selected_id:
                self.age_list.setCurrentItem(item)

    def _on_selection_changed(self, current, previous):
        """Handle age selection change."""
        if current:
            age_id = current.data(Qt.UserRole)
            self.selected_age_id = age_id
            self.age_selected.emit(age_id)

    def _on_add_age(self):
        """Handle add age button."""
        name, ok = QInputDialog.getText(self, "New Age", "Age name:")
        if ok and name:
            self.age_created.emit(name)

    def _show_context_menu(self, pos):
        """Show context menu for age list."""
        item = self.age_list.itemAt(pos)
        if not item:
            return

        age_id = item.data(Qt.UserRole)
        menu = QMenu(self)

        rename_action = QAction("Rename", self)
        rename_action.triggered.connect(lambda: self._rename_age(age_id))
        menu.addAction(rename_action)

        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(lambda: self._delete_age(age_id))
        menu.addAction(delete_action)

        menu.exec(self.age_list.mapToGlobal(pos))

    def _rename_age(self, age_id: str):
        """Rename an age."""
        age = next((a for a in self.ages if a.get('id', a.get('name', '')) == age_id), None)
        if not age:
            return

        current_name = age.get('name', '')
        name, ok = QInputDialog.getText(self, "Rename Age", "New name:", text=current_name)
        if ok and name and name != current_name:
            self.age_renamed.emit(age_id, name)

    def _delete_age(self, age_id: str):
        """Delete an age."""
        reply = QMessageBox.question(
            self, "Delete Age",
            "Delete this age? Heroes will be moved to another age.",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.age_deleted.emit(age_id)
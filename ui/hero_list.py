"""
Hero List widget for displaying and selecting heroes.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QListWidgetItem, QLabel, QLineEdit, QComboBox,
    QPushButton, QMenu, QInputDialog, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QPixmap


class HeroList(QWidget):
    """Widget for displaying and managing hero list."""

    # Signals
    hero_selected = Signal(str)  # hero_id
    hero_created = Signal(str, str)  # name, age_id
    hero_duplicated = Signal(str)  # hero_id
    hero_deleted = Signal(str)  # hero_id
    hero_renamed = Signal(str, str)  # hero_id, new_name

    def __init__(self):
        super().__init__()
        self.heroes = []
        self.selected_hero_id = None
        self.current_age_filter = None
        self._setup_ui()

    def _setup_ui(self):
        """Setup the hero list UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Search and filter
        filter_layout = QVBoxLayout()
        filter_layout.setSpacing(4)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search heroes...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                background-color: #111723;
                border: 1px solid #2b3648;
                border-radius: 8px;
                padding: 8px 12px;
                color: #ebf0f8;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #6ea8fe;
            }
        """)
        self.search_box.textChanged.connect(self._on_search)
        filter_layout.addWidget(self.search_box)

        self.type_filter = QComboBox()
        self.type_filter.addItem("All Types")
        self.type_filter.setStyleSheet("""
            QComboBox {
                background-color: #111723;
                border: 1px solid #2b3648;
                border-radius: 8px;
                padding: 8px 12px;
                color: #ebf0f8;
                font-size: 13px;
            }
            QComboBox:focus {
                border-color: #6ea8fe;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.type_filter.currentTextChanged.connect(self._on_filter_changed)
        filter_layout.addWidget(self.type_filter)

        layout.addLayout(filter_layout)

        # Hero list
        self.hero_list = QListWidget()
        self.hero_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                border: 1px solid #2b3648;
                border-radius: 8px;
                margin: 2px;
                background-color: #20293a;
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
        self.hero_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.hero_list.customContextMenuRequested.connect(self._show_context_menu)
        self.hero_list.currentItemChanged.connect(self._on_selection_changed)
        layout.addWidget(self.hero_list, 1)

        # Add hero button
        self.add_hero_btn = QPushButton("+ Create Hero")
        self.add_hero_btn.setStyleSheet("""
            QPushButton {
                background-color: linear-gradient(135deg, #3f7ae0, #5da8ff);
                border: none;
                border-radius: 8px;
                padding: 10px;
                color: white;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: linear-gradient(135deg, #5da8ff, #7bc0ff);
            }
        """)
        self.add_hero_btn.clicked.connect(self._on_add_hero)
        layout.addWidget(self.add_hero_btn)

    def update_heroes(self, heroes: list, selected_id: str = None, age_filter: str = None):
        """Update the hero list."""
        self.heroes = heroes
        self.current_age_filter = age_filter

        # Update type filter
        types = set()
        for hero in heroes:
            htype = hero.get('unit_type', hero.get('role', 'Unknown'))
            if htype:
                types.add(htype)

        current = self.type_filter.currentText()
        self.type_filter.clear()
        self.type_filter.addItem("All Types")
        for t in sorted(types):
            self.type_filter.addItem(t)
        if current in [self.type_filter.itemText(i) for i in range(self.type_filter.count())]:
            self.type_filter.setCurrentText(current)

        self._apply_filters(selected_id)

    def _apply_filters(self, selected_id: str = None):
        """Apply search and type filters."""
        search_text = self.search_box.text().lower()
        type_filter = self.type_filter.currentText()

        self.hero_list.clear()

        for hero in self.heroes:
            # Age filter
            if self.current_age_filter and hero.get('age_id') != self.current_age_filter:
                continue

            # Search filter
            if search_text:
                haystack = ' '.join([
                    str(hero.get('name', '')),
                    str(hero.get('temple', '')),
                    str(hero.get('goddess', '')),
                    str(hero.get('unit_type', '')),
                    str(hero.get('role', '')),
                ]).lower()
                if search_text not in haystack:
                    continue

            # Type filter
            if type_filter != "All Types":
                htype = hero.get('unit_type', hero.get('role', 'Unknown'))
                if htype != type_filter:
                    continue

            # Create item
            self._add_hero_item(hero, selected_id)

    def _add_hero_item(self, hero: dict, selected_id: str = None):
        """Add a hero item to the list."""
        hero_id = hero.get('id', '')
        name = hero.get('name', 'Unnamed Hero')
        htype = hero.get('unit_type', hero.get('role', 'Unknown'))
        temple = hero.get('temple', hero.get('goddess', hero.get('age_id', '')))

        item = QListWidgetItem()
        item.setData(Qt.UserRole, hero_id)

        widget = QWidget()
        item_layout = QVBoxLayout(widget)
        item_layout.setContentsMargins(12, 8, 12, 8)
        item_layout.setSpacing(4)

        name_label = QLabel(name)
        name_label.setStyleSheet("font-weight: 700; font-size: 13px; color: #ebf0f8;")
        item_layout.addWidget(name_label)

        type_label = QLabel(htype)
        type_label.setStyleSheet("color: #9ba8be; font-size: 11px;")
        item_layout.addWidget(type_label)

        if temple:
            temple_label = QLabel(temple)
            temple_label.setStyleSheet("color: #6ea8fe; font-size: 11px;")
            item_layout.addWidget(temple_label)

        item.setSizeHint(widget.sizeHint())
        self.hero_list.addItem(item)
        self.hero_list.setItemWidget(item, widget)

        if selected_id and hero_id == selected_id:
            self.hero_list.setCurrentItem(item)

    def _on_selection_changed(self, current, previous):
        """Handle hero selection change."""
        if current:
            hero_id = current.data(Qt.UserRole)
            self.selected_hero_id = hero_id
            self.hero_selected.emit(hero_id)

    def _on_search(self):
        """Handle search text change."""
        self._apply_filters(self.selected_hero_id)

    def _on_filter_changed(self):
        """Handle type filter change."""
        self._apply_filters(self.selected_hero_id)

    def _on_add_hero(self):
        """Handle add hero button."""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox

        dialog = QDialog(self)
        dialog.setWindowTitle("Create Hero")
        dialog.setModal(True)
        layout = QVBoxLayout(dialog)

        name_edit = QLineEdit()
        name_edit.setPlaceholderText("Hero name")
        name_edit.setStyleSheet("""
            QLineEdit {
                background-color: #111723;
                border: 1px solid #2b3648;
                border-radius: 8px;
                padding: 8px 12px;
                color: #ebf0f8;
            }
        """)
        layout.addWidget(name_edit)

        age_combo = QComboBox()
        age_combo.addItem("No Age", "")
        for hero in self.heroes:
            age_id = hero.get('age_id')
            if age_id and age_combo.findData(age_id) == -1:
                age_combo.addItem(hero.get('age_name', age_id), age_id)
        layout.addWidget(age_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec() == QDialog.Accepted:
            name = name_edit.text().strip()
            age_id = age_combo.currentData()
            if name:
                self.hero_created.emit(name, age_id or "")

    def _show_context_menu(self, pos):
        """Show context menu for hero list."""
        item = self.hero_list.itemAt(pos)
        if not item:
            return

        hero_id = item.data(Qt.UserRole)
        hero = next((h for h in self.heroes if h.get('id') == hero_id), None)
        if not hero:
            return

        menu = QMenu(self)

        rename_action = QAction("Rename", self)
        rename_action.triggered.connect(lambda: self._rename_hero(hero_id))
        menu.addAction(rename_action)

        duplicate_action = QAction("Duplicate", self)
        duplicate_action.triggered.connect(lambda: self.hero_duplicated.emit(hero_id))
        menu.addAction(duplicate_action)

        menu.addSeparator()

        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(lambda: self._delete_hero(hero_id))
        menu.addAction(delete_action)

        menu.exec(self.hero_list.mapToGlobal(pos))

    def _rename_hero(self, hero_id: str):
        """Rename a hero."""
        hero = next((h for h in self.heroes if h.get('id') == hero_id), None)
        if not hero:
            return

        current_name = hero.get('name', '')
        name, ok = QInputDialog.getText(self, "Rename Hero", "New name:", text=current_name)
        if ok and name and name != current_name:
            self.hero_renamed.emit(hero_id, name)

    def _delete_hero(self, hero_id: str):
        """Delete a hero."""
        hero = next((h for h in self.heroes if h.get('id') == hero_id), None)
        if not hero:
            return

        reply = QMessageBox.question(
            self, "Delete Hero",
            f"Delete {hero.get('name', 'this hero')}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.hero_deleted.emit(hero_id)
"""
Compare Picker widget for selecting heroes to compare.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QHBoxLayout
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class ComparePicker(QWidget):
    """Widget for picking heroes to compare."""

    selection_changed = Signal(list)  # list of hero_ids

    def __init__(self):
        super().__init__()
        self.heroes = []
        self.selected_ids = set()
        self._setup_ui()

    def _setup_ui(self):
        """Setup the compare picker UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Title
        title = QLabel("Compare Selection")
        title.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #9ba8be;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                font-weight: 600;
            }
        """)
        layout.addWidget(title)

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
        self.hero_list.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.hero_list, 1)

    def update_heroes(self, heroes: list, selected_ids: list):
        """Update the hero list."""
        self.heroes = heroes
        self.selected_ids = set(selected_ids)

        self.hero_list.clear()

        for hero in heroes:
            hero_id = hero.get('id', '')
            name = hero.get('name', 'Unnamed Hero')
            age = hero.get('age_id', hero.get('age', 'Unknown'))

            item = QListWidgetItem()
            item.setData(Qt.UserRole, hero_id)

            widget = QWidget()
            item_layout = QHBoxLayout(widget)
            item_layout.setContentsMargins(12, 8, 12, 8)
            item_layout.setSpacing(8)

            name_label = QLabel(name)
            name_label.setStyleSheet("font-size: 13px; color: #ebf0f8;")
            item_layout.addWidget(name_label)

            item_layout.addStretch()

            age_badge = QLabel(age)
            age_badge.setStyleSheet("""
                QLabel {
                    background-color: rgba(142, 240, 200, 0.14);
                    border: 1px solid rgba(142, 240, 200, 0.25);
                    border-radius: 10px;
                    padding: 2px 8px;
                    color: #b9ffe6;
                    font-size: 11px;
                }
            """)
            item_layout.addWidget(age_badge)

            # Checkmark for selected
            if hero_id in self.selected_ids:
                check_label = QLabel("✓")
                check_label.setStyleSheet("color: #8ef0c8; font-weight: bold; font-size: 16px;")
                item_layout.addWidget(check_label)

            item.setSizeHint(widget.sizeHint())
            self.hero_list.addItem(item)
            self.hero_list.setItemWidget(item, widget)

    def _on_item_clicked(self, item):
        """Handle item click - toggle selection."""
        hero_id = item.data(Qt.UserRole)
        if hero_id in self.selected_ids:
            self.selected_ids.remove(hero_id)
        else:
            self.selected_ids.add(hero_id)

        self._refresh_visual()
        self.selection_changed.emit(list(self.selected_ids))

    def _refresh_visual(self):
        """Refresh the visual selection state."""
        for i in range(self.hero_list.count()):
            item = self.hero_list.item(i)
            widget = self.hero_list.itemWidget(item)
            if not widget:
                continue

            hero_id = item.data(Qt.UserRole)
            is_selected = hero_id in self.selected_ids

            # Find or create checkmark
            layout = widget.layout()
            if layout.count() > 3:
                check_label = layout.itemAt(3).widget()
                if check_label:
                    check_label.setVisible(is_selected)
            elif is_selected:
                # Add checkmark
                check_label = QLabel("✓")
                check_label.setStyleSheet("color: #8ef0c8; font-weight: bold; font-size: 16px;")
                layout.addWidget(check_label)
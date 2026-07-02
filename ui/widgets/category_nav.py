"""
Category Navigation widget for quick navigation to property categories.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QHBoxLayout
)
from PySide6.QtCore import Qt, Signal


class CategoryNav(QWidget):
    """Widget for navigating property categories."""

    category_clicked = Signal(str)  # category_id

    def __init__(self):
        super().__init__()
        self.categories = []
        self._setup_ui()

    def _setup_ui(self):
        """Setup the category nav UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Title
        title = QLabel("Feature Categories")
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

        # Category list
        self.category_list = QListWidget()
        self.category_list.setStyleSheet("""
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
        self.category_list.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.category_list, 1)

    def update_categories(self, categories: list):
        """Update the category list."""
        self.categories = categories

        self.category_list.clear()

        for cat in categories:
            cat_id = cat.get('id', '')
            name = cat.get('name', 'Unknown')
            prop_count = cat.get('property_count', 0)

            item = QListWidgetItem()
            item.setData(Qt.UserRole, cat_id)

            widget = QWidget()
            item_layout = QHBoxLayout(widget)
            item_layout.setContentsMargins(12, 10, 12, 10)
            item_layout.setSpacing(8)

            name_label = QLabel(name)
            name_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #ebf0f8;")
            item_layout.addWidget(name_label)

            item_layout.addStretch()

            if prop_count > 0:
                count_badge = QLabel(str(prop_count))
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
            self.category_list.addItem(item)
            self.category_list.setItemWidget(item, widget)

    def _on_item_clicked(self, item):
        """Handle category click."""
        cat_id = item.data(Qt.UserRole)
        self.category_clicked.emit(cat_id)
"""
Comparison Window for comparing multiple heroes side by side.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QLabel, QPushButton,
    QScrollArea, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QFont, QColor


class ComparisonWindow(QWidget):
    """Widget for comparing multiple heroes side by side."""

    # Signals
    refresh_requested = Signal()

    def __init__(self):
        super().__init__()
        self.heroes = []
        self.property_defs = {}
        self._setup_ui()

    def _setup_ui(self):
        """Setup the comparison window UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Compare Heroes")
        title.setStyleSheet("font-size: 16px; font-weight: 700; color: #ebf0f8;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        self.refresh_btn = QPushButton("Refresh Comparison")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: linear-gradient(135deg, #3f7ae0, #5da8ff);
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                color: white;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: linear-gradient(135deg, #5da8ff, #7bc0ff);
            }
        """)
        self.refresh_btn.clicked.connect(self.refresh_requested.emit)
        header_layout.addWidget(self.refresh_btn)

        layout.addLayout(header_layout)

        # Empty state
        self.empty_label = QLabel("Choose two or more heroes to compare from the right sidebar.")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet("""
            QLabel {
                color: #9ba8be;
                font-size: 14px;
                padding: 40px;
                border: 1px dashed #2b3648;
                border-radius: 12px;
                background-color: #181e29;
            }
        """)
        layout.addWidget(self.empty_label, 1)

        # Comparison table (hidden initially)
        self.table_scroll = QScrollArea()
        self.table_scroll.setWidgetResizable(True)
        self.table_scroll.setFrameShape(QFrame.NoFrame)
        self.table_scroll.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: #181e29;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #2b3648;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #6ea8fe;
            }
        """)
        self.table_scroll.hide()
        layout.addWidget(self.table_scroll, 1)

        self.compare_table = QTableWidget()
        self.compare_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1f22;
                border: 1px solid #2b3648;
                border-radius: 12px;
                gridline-color: #2b3648;
                font-size: 13px;
                color: #ebf0f8;
            }
            QHeaderView::section {
                background-color: #1c2534;
                border: none;
                border-right: 1px solid #2b3648;
                border-bottom: 1px solid #2b3648;
                padding: 10px;
                font-weight: 700;
                color: #ebf0f8;
            }
            QTableWidget::item {
                padding: 10px;
                border: none;
                border-right: 1px solid #2b3648;
                border-bottom: 1px solid #2b3648;
            }
            QTableWidget::item:selected {
                background-color: rgba(110, 168, 254, 0.16);
            }
        """)
        self.compare_table.verticalHeader().setVisible(False)
        self.compare_table.horizontalHeader().setStretchLastSection(True)
        self.compare_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.compare_table.setAlternatingRowColors(False)
        self.table_scroll.setWidget(self.compare_table)

    def set_heroes(self, heroes: list, property_defs: dict):
        """Set the heroes to compare."""
        self.heroes = heroes
        self.property_defs = property_defs

        if len(heroes) < 2:
            self._show_empty()
            return

        self._build_table()

    def _show_empty(self):
        """Show empty state."""
        self.table_scroll.hide()
        self.empty_label.show()

    def _build_table(self):
        """Build the comparison table."""
        self.empty_label.hide()
        self.table_scroll.show()

        # Get all property fields (excluding system fields)
        exclude_fields = {'id', 'name', 'age_id', 'description', 'images', 'created_at', 'updated_at', 'tags'}
        fields = [k for k in self.property_defs.keys() if k not in exclude_fields]

        # Also include core fields
        core_fields = ['name', 'age_id', 'unit_type', 'role', 'temple', 'goddess']
        for f in core_fields:
            if f not in fields:
                fields.insert(0, f)

        # Set up table
        self.compare_table.setRowCount(len(fields))
        self.compare_table.setColumnCount(len(self.heroes) + 1)

        # Headers
        headers = ["Field"] + [h.get('name', 'Unknown') for h in self.heroes]
        self.compare_table.setHorizontalHeaderLabels(headers)

        # Age names for display
        age_names = {}
        for hero in self.heroes:
            age_id = hero.get('age_id', '')
            # Could map age_id to name if we have age data

        for row, field in enumerate(fields):
            # Field name
            field_item = QTableWidgetItem(field)
            field_item.setFlags(field_item.flags() & ~Qt.ItemIsEditable)
            field_item.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
            self.compare_table.setItem(row, 0, field_item)

            # Values for each hero
            values = []
            for hero in self.heroes:
                value = hero.get(field, '')
                if field == 'age_id' and value:
                    value = age_names.get(value, value)
                values.append(str(value) if value else '—')

            # Check if values differ
            different = len(set(values)) > 1

            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                if different:
                    item.setBackground(QColor("#f0717830"))  # Highlight differences
                self.compare_table.setItem(row, col + 1, item)

        # Resize rows to content
        self.compare_table.resizeRowsToContents()

    def add_hero_images(self, heroes_with_images: list):
        """Add hero images to the table header."""
        # This would add a row with images at the top
        pass
"""
Toolbar widget for main window actions.
"""

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QLabel,
    QComboBox, QLineEdit, QMenu
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QIcon


class Toolbar(QWidget):
    """Main toolbar with project actions and mode switching."""

    # Signals
    new_project = Signal()
    open_project = Signal()
    save_project = Signal()
    export_excel = Signal()
    mode_changed = Signal(str)  # editor, compare, manage
    search_changed = Signal(str)
    show_preferences = Signal()

    def __init__(self):
        super().__init__()
        self.current_mode = "editor"
        self._setup_ui()

    def _setup_ui(self):
        """Setup the toolbar UI."""
        self.setFixedHeight(56)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(24, 30, 41, 0.92);
                border-bottom: 1px solid #2b3648;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(12)

        # Brand
        brand_layout = QHBoxLayout()
        brand_layout.setSpacing(12)

        badge = QLabel("G")
        badge.setFixedSize(28, 28)
        badge.setAlignment(Qt.AlignCenter)
        badge.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #6ea8fe, stop:1 #8ef0c8);
                border-radius: 8px;
                color: #09111f;
                font-weight: 900;
                font-size: 14px;
            }
        """)
        brand_layout.addWidget(badge)

        brand_text = QWidget()
        brand_text_layout = QVBoxLayout(brand_text)
        brand_text_layout.setContentsMargins(0, 0, 0, 0)
        brand_text_layout.setSpacing(0)

        title = QLabel("Game Character Designer")
        title.setStyleSheet("font-weight: 700; font-size: 14px; color: #ebf0f8;")
        brand_text_layout.addWidget(title)

        subtitle = QLabel("Offline hero editor with Excel-backed storage")
        subtitle.setStyleSheet("color: #9ba8be; font-size: 11px;")
        brand_text_layout.addWidget(subtitle)

        brand_layout.addWidget(brand_text)
        layout.addLayout(brand_layout)

        layout.addStretch()

        # Mode buttons
        self.mode_buttons = {}
        for mode_id, mode_name, shortcut in [
            ("editor", "Editor", "Ctrl+1"),
            ("compare", "Compare", "Ctrl+2"),
            ("manage", "Manage Schema", "Ctrl+3"),
        ]:
            btn = QPushButton(mode_name)
            btn.setCheckable(True)
            btn.setToolTip(f"{mode_name} ({shortcut})")
            btn.clicked.connect(lambda checked, m=mode_id: self._on_mode_clicked(m))
            btn.setStyleSheet(self._mode_button_style())
            self.mode_buttons[mode_id] = btn
            layout.addWidget(btn)

        self.mode_buttons["editor"].setChecked(True)

        layout.addStretch()

        # Status
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: rgba(110, 168, 254, 0.1);
                border: 1px solid rgba(110, 168, 254, 0.2);
                border-radius: 16px;
                padding: 6px 16px;
                color: #d7e6ff;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.status_label)

        # Project actions
        self.project_btn = QPushButton("Project Folder")
        self.project_btn.setToolTip("Change project folder (Ctrl+Shift+P)")
        self.project_btn.clicked.connect(self.open_project.emit)
        self.project_btn.setStyleSheet(self._action_button_style())
        layout.addWidget(self.project_btn)

        self.export_btn = QPushButton("Download Workbook")
        self.export_btn.setToolTip("Export to Excel (Ctrl+E)")
        self.export_btn.clicked.connect(self.export_excel.emit)
        self.export_btn.setStyleSheet(self._action_button_style())
        layout.addWidget(self.export_btn)

        self.save_btn = QPushButton("Save")
        self.save_btn.setToolTip("Save project (Ctrl+S)")
        self.save_btn.clicked.connect(self.save_project.emit)
        self.save_btn.setStyleSheet(self._primary_button_style())
        layout.addWidget(self.save_btn)

    def _mode_button_style(self) -> str:
        return """
            QPushButton {
                background-color: transparent;
                border: 1px solid transparent;
                border-radius: 8px;
                padding: 8px 16px;
                color: #9ba8be;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #20293a;
                border-color: #2b3648;
                color: #ebf0f8;
            }
            QPushButton:checked {
                background-color: rgba(110, 168, 254, 0.16);
                border-color: #6ea8fe;
                color: #6ea8fe;
                font-weight: 600;
            }
        """

    def _action_button_style(self) -> str:
        return """
            QPushButton {
                background-color: #182131;
                border: 1px solid #2b3648;
                border-radius: 8px;
                padding: 8px 16px;
                color: #ebf0f8;
                font-size: 13px;
            }
            QPushButton:hover {
                border-color: #6ea8fe;
                background-color: #20293a;
            }
        """

    def _primary_button_style(self) -> str:
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3f7ae0, stop:1 #5da8ff);
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                color: white;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5da8ff, stop:1 #7bc0ff);
            }
        """

    def _on_mode_clicked(self, mode: str):
        """Handle mode button click."""
        self.current_mode = mode
        for m, btn in self.mode_buttons.items():
            btn.setChecked(m == mode)
        self.mode_changed.emit(mode)

    def set_mode(self, mode: str):
        """Set the current mode programmatically."""
        self.current_mode = mode
        for m, btn in self.mode_buttons.items():
            btn.setChecked(m == mode)

    def set_status(self, message: str):
        """Update status label."""
        self.status_label.setText(message)
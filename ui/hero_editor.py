"""
Hero Editor widget for editing hero properties.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QLabel, QLineEdit, QTextEdit, QComboBox,
    QPushButton, QFrame, QGridLayout, QGroupBox,
    QCheckBox, QSpinBox, QDoubleSpinBox, QSplitter,
    QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QFont


class HeroEditor(QWidget):
    """Widget for editing a single hero's properties."""

    # Signals
    hero_changed = Signal(dict)  # property changes
    hero_renamed = Signal(str, str)  # hero_id, new_name
    hero_duplicated = Signal(str)  # hero_id
    hero_deleted = Signal(str)  # hero_id
    image_uploaded = Signal(str, str)  # hero_id, image_path
    compare_toggled = Signal(str)  # hero_id

    def __init__(self):
        super().__init__()
        self.current_hero = None
        self.property_widgets = {}
        self._setup_ui()

    def _setup_ui(self):
        """Setup the hero editor UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header with hero image and basic info
        header = self._create_header()
        layout.addWidget(header)

        # Scrollable property area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        self.property_container = QWidget()
        self.property_layout = QVBoxLayout(self.property_container)
        self.property_layout.setContentsMargins(12, 12, 12, 12)
        self.property_layout.setSpacing(12)
        scroll.setWidget(self.property_container)
        layout.addWidget(scroll, 1)

    def _create_header(self) -> QWidget:
        """Create the hero header with portrait and basic fields."""
        header = QWidget()
        header.setFixedHeight(320)
        header.setStyleSheet("""
            QWidget {
                background-color: #1e1f22;
                border-bottom: 1px solid #2b3648;
            }
        """)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # Portrait section
        portrait_frame = QFrame()
        portrait_frame.setFixedSize(220, 280)
        portrait_frame.setStyleSheet("""
            QFrame {
                border: 1px dashed #2b3648;
                border-radius: 12px;
                background-color: #20293a;
            }
        """)

        portrait_layout = QVBoxLayout(portrait_frame)
        portrait_layout.setAlignment(Qt.AlignCenter)

        self.portrait_label = QLabel("No Image")
        self.portrait_label.setAlignment(Qt.AlignCenter)
        self.portrait_label.setStyleSheet("color: #9ba8be; font-size: 14px;")
        self.portrait_label.setMinimumSize(200, 240)
        self.portrait_label.setScaledContents(True)
        portrait_layout.addWidget(self.portrait_label)

        # Portrait buttons
        portrait_btns = QHBoxLayout()
        self.upload_portrait_btn = QPushButton("Upload Portrait")
        self.upload_portrait_btn.clicked.connect(self._on_upload_portrait)
        self.upload_portrait_btn.setStyleSheet(self._button_style())
        portrait_btns.addWidget(self.upload_portrait_btn)

        self.add_images_btn = QPushButton("Add Images")
        self.add_images_btn.clicked.connect(self._on_add_images)
        self.add_images_btn.setStyleSheet(self._button_style())
        portrait_btns.addWidget(self.add_images_btn)

        portrait_layout.addLayout(portrait_btns)

        layout.addWidget(portrait_frame)

        # Right side - Meta fields and actions
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(12)

        # Hero name and type
        name_layout = QHBoxLayout()
        self.hero_name_edit = QLineEdit()
        self.hero_name_edit.setPlaceholderText("Hero Name")
        self.hero_name_edit.setStyleSheet(self._input_style())
        self.hero_name_edit.editingFinished.connect(self._on_name_changed)
        name_layout.addWidget(self.hero_name_edit)

        self.type_badge = QLabel("Unknown")
        self.type_badge.setStyleSheet("""
            QLabel {
                background-color: rgba(142, 240, 200, 0.14);
                border: 1px solid rgba(142, 240, 200, 0.25);
                border-radius: 8px;
                padding: 4px 12px;
                color: #b9ffe6;
                font-size: 12px;
            }
        """)
        name_layout.addWidget(self.type_badge)
        right_layout.addLayout(name_layout)

        # Meta grid for core fields
        self.meta_grid = QGridLayout()
        self.meta_grid.setSpacing(12)
        self.meta_grid.setColumnStretch(1, 1)
        right_layout.addLayout(self.meta_grid)

        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(8)

        self.rename_btn = QPushButton("Rename")
        self.rename_btn.clicked.connect(self._on_rename)
        self.rename_btn.setStyleSheet(self._button_style())
        action_layout.addWidget(self.rename_btn)

        self.move_age_btn = QPushButton("Move to Age")
        self.move_age_btn.clicked.connect(self._on_move_age)
        self.move_age_btn.setStyleSheet(self._button_style())
        action_layout.addWidget(self.move_age_btn)

        self.duplicate_btn = QPushButton("Duplicate")
        self.duplicate_btn.clicked.connect(self._on_duplicate)
        self.duplicate_btn.setStyleSheet(self._button_style())
        action_layout.addWidget(self.duplicate_btn)

        self.compare_btn = QPushButton("Add to Compare")
        self.compare_btn.clicked.connect(self._on_compare_toggle)
        self.compare_btn.setStyleSheet(self._button_style())
        action_layout.addWidget(self.compare_btn)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self._on_delete)
        self.delete_btn.setStyleSheet(self._button_style(danger=True))
        action_layout.addWidget(self.delete_btn)

        right_layout.addLayout(action_layout)
        right_layout.addStretch()

        layout.addWidget(right_widget, 1)

        return header

    def _input_style(self) -> str:
        return """
            QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                background-color: #111723;
                border: 1px solid #2b3648;
                border-radius: 8px;
                padding: 8px 12px;
                color: #ebf0f8;
                font-size: 13px;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border-color: #6ea8fe;
                box-shadow: 0 0 0 3px rgba(110, 168, 254, 0.16);
            }
        """

    def _button_style(self, danger=False) -> str:
        if danger:
            return """
                QPushButton {
                    background-color: rgba(240, 113, 120, 0.12);
                    border: 1px solid rgba(240, 113, 120, 0.35);
                    border-radius: 8px;
                    padding: 8px 16px;
                    color: #ffc6cb;
                    font-size: 13px;
                }
                QPushButton:hover {
                    border-color: #f07178;
                    background-color: rgba(240, 113, 120, 0.2);
                }
            """
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

    def load_hero(self, hero_data: dict, property_defs: list, age_options: list):
        """Load hero data into the editor."""
        self.current_hero = hero_data
        self.property_defs = {p['id']: p for p in property_defs} if property_defs else {}
        self.age_options = age_options

        # Update header
        self.hero_name_edit.setText(hero_data.get('name', ''))
        self.type_badge.setText(hero_data.get('unit_type', hero_data.get('role', 'Unknown')))

        # Update portrait
        portrait_path = hero_data.get('portrait', '')
        if portrait_path:
            pixmap = QPixmap(portrait_path)
            if not pixmap.isNull():
                self.portrait_label.setPixmap(pixmap.scaled(
                    200, 240, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.portrait_label.setText("Image not found")
        else:
            self.portrait_label.setText("No Image")

        # Update meta fields
        self._update_meta_fields()

        # Update property fields
        self._update_property_fields()

    def _update_meta_fields(self):
        """Update the meta grid with core fields."""
        # Clear existing
        for i in reversed(range(self.meta_grid.count())):
            item = self.meta_grid.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        # Core fields
        core_fields = [
            ('age_id', 'Age', 'combo', self.age_options),
            ('temple', 'Temple', 'text', None),
            ('goddess', 'Goddess', 'text', None),
            ('unit_type', 'Unit Type', 'text', None),
            ('role', 'Role', 'text', None),
        ]

        for row, (prop_id, label, widget_type, options) in enumerate(core_fields):
            lbl = QLabel(label)
            lbl.setStyleSheet("color: #9ba8be; font-size: 12px; font-weight: 600;")
            self.meta_grid.addWidget(lbl, row, 0)

            if widget_type == 'combo':
                widget = QComboBox()
                widget.addItems(options)
                current = self.current_hero.get(prop_id, '')
                if current:
                    widget.setCurrentText(current)
                widget.currentTextChanged.connect(
                    lambda text, pid=prop_id: self._on_property_changed(pid, text)
                )
            else:
                widget = QLineEdit()
                widget.setText(str(self.current_hero.get(prop_id, '')))
                widget.setStyleSheet(self._input_style())
                widget.editingFinished.connect(
                    lambda pid=prop_id, w=widget: self._on_property_changed(pid, w.text())
                )

            widget.setStyleSheet(self._input_style())
            self.meta_grid.addWidget(widget, row, 1)

    def _update_property_fields(self):
        """Update the property fields area with collapsible categories."""
        # Clear existing
        for i in reversed(range(self.property_layout.count())):
            item = self.property_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        # Group properties by category
        categories = {}
        for prop_id, prop_def in self.property_defs.items():
            cat = prop_def.get('category', 'Custom')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append((prop_id, prop_def))

        # Create collapsible sections
        for cat_name, props in categories.items():
            group = QGroupBox(cat_name)
            group.setCheckable(True)
            group.setChecked(True)
            group.setStyleSheet("""
                QGroupBox {
                    font-weight: 700;
                    font-size: 13px;
                    color: #ebf0f8;
                    border: 1px solid #2b3648;
                    border-radius: 10px;
                    margin-top: 16px;
                    padding-top: 16px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 12px;
                    padding: 0 8px;
                    background-color: #1e1f22;
                }
            """)

            group_layout = QGridLayout(group)
            group_layout.setSpacing(12)
            group_layout.setColumnStretch(1, 1)

            for idx, (prop_id, prop_def) in enumerate(props):
                row = idx // 2
                col = (idx % 2) * 2

                lbl = QLabel(prop_def.get('display_name', prop_id))
                lbl.setStyleSheet("color: #9ba8be; font-size: 12px; font-weight: 600;")
                group_layout.addWidget(lbl, row, col)

                widget = self._create_property_widget(prop_id, prop_def)
                widget.setStyleSheet(self._input_style())
                group_layout.addWidget(widget, row, col + 1)

            self.property_layout.addWidget(group)

        self.property_layout.addStretch()

    def _create_property_widget(self, prop_id: str, prop_def: dict) -> QWidget:
        """Create appropriate widget for property type."""
        prop_type = prop_def.get('type', 'text')
        value = self.current_hero.get(prop_id, prop_def.get('default', ''))

        if prop_type == 'textarea':
            widget = QTextEdit()
            widget.setPlainText(str(value))
            widget.setMinimumHeight(80)
            widget.textChanged.connect(
                lambda pid=prop_id, w=widget: self._on_property_changed(pid, w.toPlainText())
            )
        elif prop_type == 'integer':
            widget = QSpinBox()
            widget.setRange(prop_def.get('min', -999999), prop_def.get('max', 999999))
            widget.setValue(int(value) if value else 0)
            widget.valueChanged.connect(
                lambda val, pid=prop_id: self._on_property_changed(pid, val)
            )
        elif prop_type == 'float':
            widget = QDoubleSpinBox()
            widget.setRange(prop_def.get('min', -999999.0), prop_def.get('max', 999999.0))
            widget.setDecimals(prop_def.get('decimals', 2))
            widget.setValue(float(value) if value else 0.0)
            widget.valueChanged.connect(
                lambda val, pid=prop_id: self._on_property_changed(pid, val)
            )
        elif prop_type == 'boolean':
            widget = QCheckBox()
            widget.setChecked(bool(value))
            widget.toggled.connect(
                lambda checked, pid=prop_id: self._on_property_changed(pid, checked)
            )
        elif prop_type == 'enum':
            widget = QComboBox()
            widget.addItems(prop_def.get('options', []))
            if value:
                widget.setCurrentText(str(value))
            widget.currentTextChanged.connect(
                lambda text, pid=prop_id: self._on_property_changed(pid, text)
            )
        else:  # text
            widget = QLineEdit()
            widget.setText(str(value))
            widget.editingFinished.connect(
                lambda pid=prop_id, w=widget: self._on_property_changed(pid, w.text())
            )

        self.property_widgets[prop_id] = widget
        return widget

    def _on_property_changed(self, prop_id: str, value):
        """Handle property change."""
        if self.current_hero:
            self.current_hero[prop_id] = value
            self.hero_changed.emit({prop_id: value})

    def _on_name_changed(self):
        """Handle hero name change."""
        if self.current_hero:
            new_name = self.hero_name_edit.text()
            old_name = self.current_hero.get('name', '')
            if new_name != old_name:
                self.current_hero['name'] = new_name
                self.hero_renamed.emit(self.current_hero.get('id', ''), new_name)

    def _on_rename(self):
        """Handle rename button."""
        self._on_name_changed()

    def _on_move_age(self):
        """Handle move to age button."""
        pass  # TODO: Show dialog

    def _on_duplicate(self):
        """Handle duplicate button."""
        if self.current_hero:
            self.hero_duplicated.emit(self.current_hero.get('id', ''))

    def _on_delete(self):
        """Handle delete button."""
        if self.current_hero:
            self.hero_deleted.emit(self.current_hero.get('id', ''))

    def _on_compare_toggle(self):
        """Handle compare toggle."""
        if self.current_hero:
            self.compare_toggled.emit(self.current_hero.get('id', ''))

    def _on_upload_portrait(self):
        """Handle portrait upload."""
        pass  # TODO: File dialog

    def _on_add_images(self):
        """Handle add images."""
        pass  # TODO: File dialog

    def set_compare_state(self, is_selected: bool):
        """Update compare button state."""
        self.compare_btn.setText("Remove from Compare" if is_selected else "Add to Compare")
"""
Main application window for the RTS Game Designer.
This module provides the primary window layout with sidebar, main panel, and toolbar.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QSplitter, QStackedWidget, QMenuBar, QStatusBar
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QIcon


class MainWindow(QMainWindow):
    """Main application window with three-panel layout."""

    # Signals
    hero_selected = Signal(str)  # hero_id
    age_selected = Signal(str)   # age_id
    compare_requested = Signal(list)  # list of hero_ids
    save_requested = Signal()
    export_requested = Signal()

    def __init__(self, config=None):
        super().__init__()
        self.config = config
        self.current_mode = "editor"  # editor, compare, manage
        self._setup_ui()
        self._setup_menu()
        self._setup_shortcuts()

    def _setup_ui(self):
        """Setup the main window UI with three-panel layout."""
        self.setWindowTitle("RTS Game Designer")
        self.resize(1400, 900)

        # Central widget with splitter
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Main horizontal splitter (left panel | center | right panel)
        self.main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.main_splitter)

        # Left panel - Ages & Hero List
        self.left_panel = self._create_left_panel()
        self.main_splitter.addWidget(self.left_panel)

        # Center panel - Stacked widget for different modes
        self.center_stack = QStackedWidget()
        self.main_splitter.addWidget(self.center_stack)

        # Right panel - Navigation & Tools
        self.right_panel = self._create_right_panel()
        self.main_splitter.addWidget(self.right_panel)

        # Set splitter proportions (left: 280, center: 840, right: 280)
        self.main_splitter.setSizes([280, 840, 280])
        self.main_splitter.setCollapsible(0, True)
        self.main_splitter.setCollapsible(2, True)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def _create_left_panel(self) -> QWidget:
        """Create the left sidebar with Ages and Hero list."""
        from ui.age_panel import AgePanel
        from ui.hero_list import HeroList

        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(8)

        # Ages panel
        self.age_panel = AgePanel()
        self.age_panel.age_selected.connect(self.age_selected.emit)
        self.age_panel.age_created.connect(self._on_age_created)
        self.age_panel.age_renamed.connect(self._on_age_renamed)
        self.age_panel.age_deleted.connect(self._on_age_deleted)
        layout.addWidget(self.age_panel)

        # Hero list
        self.hero_list = HeroList()
        self.hero_list.hero_selected.connect(self.hero_selected.emit)
        self.hero_list.hero_created.connect(self._on_hero_created)
        self.hero_list.hero_duplicated.connect(self._on_hero_duplicated)
        self.hero_list.hero_deleted.connect(self._on_hero_deleted)
        self.hero_list.hero_renamed.connect(self._on_hero_renamed)
        layout.addWidget(self.hero_list, 1)

        return panel

    def _create_right_panel(self) -> QWidget:
        """Create the right sidebar with navigation and tools."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(16)

        # Compare selection
        from ui.widgets.compare_picker import ComparePicker
        self.compare_picker = ComparePicker()
        self.compare_picker.selection_changed.connect(self.compare_requested.emit)
        layout.addWidget(self.compare_picker)

        # Category navigation
        from ui.widgets.category_nav import CategoryNav
        self.category_nav = CategoryNav()
        self.category_nav.category_clicked.connect(self._on_category_clicked)
        layout.addWidget(self.category_nav, 1)

        return panel

    def _setup_menu(self):
        """Setup the menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        new_action = QAction("&New Project", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self._new_project)
        file_menu.addAction(new_action)

        open_action = QAction("&Open Project...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._open_project)
        file_menu.addAction(open_action)

        save_action = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_requested.emit)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save &As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self._save_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        export_action = QAction("&Export to Excel...", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_requested.emit)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu("&Edit")

        undo_action = QAction("&Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        edit_menu.addAction(undo_action)

        redo_action = QAction("&Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        prefs_action = QAction("&Preferences...", self)
        prefs_action.setShortcut("Ctrl+,")
        prefs_action.triggered.connect(self._show_preferences)
        edit_menu.addAction(prefs_action)

        # View menu
        view_menu = menubar.addMenu("&View")

        editor_mode = QAction("&Editor", self)
        editor_mode.setShortcut("Ctrl+1")
        editor_mode.triggered.connect(lambda: self.set_mode("editor"))
        view_menu.addAction(editor_mode)

        compare_mode = QAction("&Compare", self)
        compare_mode.setShortcut("Ctrl+2")
        compare_mode.triggered.connect(lambda: self.set_mode("compare"))
        view_menu.addAction(compare_mode)

        manage_mode = QAction("&Manage Schema", self)
        manage_mode.setShortcut("Ctrl+3")
        manage_mode.triggered.connect(lambda: self.set_mode("manage"))
        view_menu.addAction(manage_mode)

        # Help menu
        help_menu = menubar.addMenu("&Help")
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _setup_shortcuts(self):
        """Setup keyboard shortcuts."""
        pass  # Shortcuts are set in menu actions

    def set_mode(self, mode: str):
        """Switch between editor, compare, and manage modes."""
        self.current_mode = mode
        if mode == "editor":
            self.center_stack.setCurrentIndex(0)
        elif mode == "compare":
            self.center_stack.setCurrentIndex(1)
        elif mode == "manage":
            self.center_stack.setCurrentIndex(2)

    def set_center_widget(self, index: int, widget: QWidget):
        """Set a widget in the center stack at given index."""
        while self.center_stack.count() <= index:
            self.center_stack.addWidget(QWidget())
        self.center_stack.insertWidget(index, widget)
        self.center_stack.removeWidget(self.center_stack.widget(index + 1))

    def update_hero_list(self, heroes, selected_id=None, age_filter=None):
        """Update the hero list with new data."""
        self.hero_list.update_heroes(heroes, selected_id, age_filter)

    def update_age_list(self, ages, selected_id=None):
        """Update the age list with new data."""
        self.age_panel.update_ages(ages, selected_id)

    def update_compare_picker(self, heroes, selected_ids):
        """Update the compare picker with hero selection."""
        self.compare_picker.update_heroes(heroes, selected_ids)

    def update_category_nav(self, categories):
        """Update the category navigation panel."""
        self.category_nav.update_categories(categories)

    def show_status(self, message: str, timeout: int = 0):
        """Show message in status bar."""
        self.status_bar.showMessage(message, timeout)

    # Event handlers
    def _on_age_created(self, name: str):
        pass  # Handled by service layer

    def _on_age_renamed(self, age_id: str, new_name: str):
        pass

    def _on_age_deleted(self, age_id: str):
        pass

    def _on_hero_created(self, name: str, age_id: str):
        pass

    def _on_hero_duplicated(self, hero_id: str):
        pass

    def _on_hero_deleted(self, hero_id: str):
        pass

    def _on_hero_renamed(self, hero_id: str, new_name: str):
        pass

    def _on_category_clicked(self, category_id: str):
        pass

    def _new_project(self):
        pass

    def _open_project(self):
        pass

    def _save_as(self):
        pass

    def _show_preferences(self):
        pass

    def _show_about(self):
        pass
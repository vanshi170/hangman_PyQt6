import sys
from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QGridLayout
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QIcon, QKeySequence, QShortcut
from storage.settings import SettingsManager
from game.hangman_engine import HangmanEngine
from .home_page import HomePage
from .game_page import GamePage
from .summary_page import SummaryPage
from .stats_page import StatsPage
from .settings_page import SettingsPage
from .about_page import AboutPage
from .widgets.toast import ToastNotification
from .widgets.confetti import ConfettiWidget
from styles.style_constants import COLORS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = SettingsManager()
        self.engine = HangmanEngine()
        
        self.init_ui()
        self.restore_state()
        self.apply_theme()

    def init_ui(self):
        self.setWindowTitle("HangmanX")
        self.setMinimumSize(1000, 700)
        
        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Top Bar (Global Actions)
        top_bar = QWidget()
        top_bar.setFixedHeight(60)
        top_layout = QGridLayout(top_bar)
        top_layout.setColumnStretch(0, 1)
        top_layout.setColumnStretch(1, 0)
        top_layout.setColumnStretch(2, 1)
        top_layout.setContentsMargins(10, 0, 10, 0)
        
        # Left Side
        left_widget = QWidget()
        left_layout = QHBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        self.btn_back = QPushButton("Back")
        self.btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_back.setFixedWidth(100)
        self.btn_back.hide()
        self.btn_back.clicked.connect(self.show_home)
        left_layout.addWidget(self.btn_back)
        left_layout.addStretch()
        top_layout.addWidget(left_widget, 0, 0)
        
        # Center Side
        self.lbl_page_title = QLabel("")
        self.lbl_page_title.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.lbl_page_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(self.lbl_page_title, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Right Side
        right_widget = QWidget()
        right_layout = QHBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addStretch()
        
        self.btn_export_csv = QPushButton("Export CSV")
        self.btn_export_csv.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_export_csv.setFixedWidth(130)
        self.btn_export_csv.hide()
        right_layout.addWidget(self.btn_export_csv)
        
        self.btn_theme = QPushButton("Toggle Theme")
        self.btn_theme.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_theme.clicked.connect(self.toggle_theme)
        right_layout.addWidget(self.btn_theme)
        
        top_layout.addWidget(right_widget, 0, 2)
        
        main_layout.addWidget(top_bar)
        
        # Stacked Widget for Screens
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        
        # Initialize Pages
        self.home_page = HomePage()
        self.game_page = GamePage(self.engine)
        self.summary_page = SummaryPage(self.engine)
        self.stats_page = StatsPage()
        self.settings_page = SettingsPage()
        self.about_page = AboutPage()
        
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.game_page)
        self.stacked_widget.addWidget(self.summary_page)
        self.stacked_widget.addWidget(self.stats_page)
        self.stacked_widget.addWidget(self.settings_page)
        self.stacked_widget.addWidget(self.about_page)
        
        # Connect Signals
        self.home_page.playRequested.connect(self.start_game)
        self.home_page.statsRequested.connect(self.show_stats)
        self.home_page.settingsRequested.connect(self.show_settings)
        self.home_page.aboutRequested.connect(self.show_about)
        self.home_page.exitRequested.connect(self.close)
        
        self.btn_export_csv.clicked.connect(self.stats_page.export_csv)
        
        self.game_page.goHomeRequested.connect(self.show_home)
        self.game_page.gameFinished.connect(self.on_game_finished)
        
        self.summary_page.homeRequested.connect(self.show_home)
        self.summary_page.playAgainRequested.connect(self.play_again)
        
        self.stats_page.homeRequested.connect(self.show_home)
        self.settings_page.homeRequested.connect(self.show_home)
        self.about_page.homeRequested.connect(self.show_home)
        
        # Overlays
        self.toast = ToastNotification(self)
        self.confetti = ConfettiWidget(self)
        self.confetti.resize(self.size())
        
        # Shortcuts
        QShortcut(QKeySequence("F11"), self).activated.connect(self.toggle_fullscreen)
        QShortcut(QKeySequence("Esc"), self).activated.connect(self.handle_escape)
        QShortcut(QKeySequence("Ctrl+D"), self).activated.connect(self.toggle_theme)
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.confetti.resize(self.size())
        if hasattr(self, 'toast') and self.toast.isVisible():
            # Adjust toast position on resize
            parent_rect = self.rect()
            parent_pos = self.mapToGlobal(parent_rect.topLeft())
            x = parent_pos.x() + (parent_rect.width() - self.toast.width()) // 2
            y = parent_pos.y() + 40
            self.toast.move(x, y)

    def keyPressEvent(self, event):
        if self.stacked_widget.currentWidget() == self.game_page:
            if self.settings.get("keyboard_input_enabled"):
                self.game_page.handle_physical_key(event.text())
        super().keyPressEvent(event)

    def handle_escape(self):
        if self.isFullScreen():
            self.toggle_fullscreen()
        elif self.stacked_widget.currentWidget() != self.home_page:
            self.show_home()

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.settings.set("is_fullscreen", False)
        else:
            self.showFullScreen()
            self.settings.set("is_fullscreen", True)

    def toggle_theme(self):
        current = self.settings.get("theme")
        new_theme = "light" if current == "dark" else "dark"
        self.settings.set("theme", new_theme)
        self.apply_theme()
        
    def apply_theme(self):
        theme = self.settings.get("theme")
        colors = COLORS[theme]
        
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Update Icon (Use SVGs)
        icon_name = "moon" if theme == "light" else "sun"
        icon_path = os.path.join(base_dir, "assets", "icons", f"{icon_name}_{theme}.svg")
        
        # Replace backslashes with forward slashes for QSS and QIcon
        icon_path_qss = icon_path.replace("\\", "/")
        
        self.btn_theme.setIcon(QIcon(icon_path_qss))
        self.btn_theme.setText("")
        self.btn_theme.setStyleSheet(f"border: 1px solid {colors['border']}; border-radius: 8px; padding: 8px; background-color: {colors['card']};")
        
        # Paths for combo box arrows
        down_arrow = os.path.join(base_dir, "assets", "icons", f"down_arrow_{theme}.svg").replace("\\", "/")
        up_arrow = os.path.join(base_dir, "assets", "icons", f"up_arrow_{theme}.svg").replace("\\", "/")
        check_icon = os.path.join(base_dir, "assets", "icons", "check_dark.svg").replace("\\", "/")
        
        # Build QSS dynamically
        qss = f"""
            QMainWindow, QWidget#splashContainer, QStackedWidget > QWidget, QScrollArea, QScrollArea QWidget {{
                background-color: {colors['background']};
                color: {colors['text']};
            }}
            QLabel, QCheckBox {{
                color: {colors['text']};
            }}
            QCheckBox::indicator {{
                width: 24px;
                height: 24px;
                border: 2px solid {colors['border']};
                border-radius: 6px;
                background-color: {colors['card']};
            }}
            QCheckBox::indicator:hover {{
                border: 2px solid {colors['accent']};
            }}
            QCheckBox::indicator:checked {{
                background-color: {colors['accent']};
                border: 2px solid {colors['accent']};
                image: url({check_icon});
            }}
            QPushButton {{
                background-color: {colors['card']};
                color: {colors['text']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 10px 20px;
                font-family: 'Segoe UI', Inter;
                font-size: 14px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {colors['card_hover']};
            }}
            QPushButton[btnClass="primary"] {{
                background-color: {colors['accent']};
                color: #ffffff;
                border: none;
            }}
            QPushButton[btnClass="primary"]:hover {{
                background-color: {colors['accent_hover']};
            }}
            QPushButton[btnClass="success"] {{
                background-color: {colors['success']};
                color: #ffffff;
                border: none;
            }}
            QPushButton[btnClass="danger"] {{
                background-color: {colors['danger']};
                color: #ffffff;
                border: none;
            }}
            QComboBox {{
                background-color: {colors['card']};
                color: {colors['text']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 14px;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                image: url({down_arrow});
                width: 16px;
                height: 16px;
            }}
            QComboBox::down-arrow:on {{
                image: url({up_arrow});
            }}
            QComboBox QAbstractItemView {{
                background-color: {colors['card']};
                color: {colors['text']};
                selection-background-color: {colors['accent']};
            }}
            /* Keyboard Keys */
            QPushButton[keyState="unused"] {{
                background-color: {colors['card']};
                border: 1px solid {colors['border']};
            }}
            QPushButton[keyState="unused"]:hover {{
                background-color: {colors['card_hover']};
            }}
            QPushButton[keyState="correct"] {{
                background-color: {colors['success']};
                color: #ffffff;
                border: none;
            }}
            QPushButton[keyState="incorrect"] {{
                background-color: {colors['danger']};
                color: #ffffff;
                border: none;
            }}
        """
        self.setStyleSheet(qss)
        
        # Tell specific widgets to update
        self.game_page.canvas.set_theme_colors(colors['text'])
        self.stats_page.update_stats(theme)

    def transition_to(self, page_widget):
        self.btn_export_csv.setVisible(page_widget == self.stats_page)
        self.btn_back.setVisible(page_widget != self.home_page)
        
        if page_widget == self.stats_page:
            self.lbl_page_title.setText("Statistics")
        elif page_widget == self.settings_page:
            self.lbl_page_title.setText("Settings")
        elif page_widget == self.about_page:
            self.lbl_page_title.setText("About")
        else:
            self.lbl_page_title.setText("")
        
        if not self.settings.get("animations_enabled"):
            self.stacked_widget.setCurrentWidget(page_widget)
            return
            
        # Optional: Implement a fade or slide transition using QPropertyAnimation.
        # For simplicity, we just set current widget.
        # A true cross-fade requires rendering both to pixmaps.
        self.stacked_widget.setCurrentWidget(page_widget)

    def start_game(self, mode, difficulty, category):
        self.game_page.start_game(mode, difficulty, category)
        self.transition_to(self.game_page)

    def on_game_finished(self, unlocked_achievements):
        self.summary_page.update_summary()
        self.transition_to(self.summary_page)
        
        if self.engine.state == self.engine.STATE_WON:
            self.confetti.start()
            
        # Show achievement toasts sequentially
        delay = 0
        for ach in unlocked_achievements:
            # Need to capture ach properly
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(delay, lambda a=ach: self.toast.show_toast(f"Achievement Unlocked:\n{a}", 3000, "success"))
            delay += 3500

    def show_home(self):
        self.transition_to(self.home_page)

    def play_again(self):
        # Re-start with last known mode/diff/cat
        # This requires storing them in engine, which we do
        self.start_game(self.engine.mode, self.engine.difficulty, "Programming") # Need to refactor to save last category

    def show_stats(self):
        self.stats_page.update_stats(self.settings.get("theme"))
        self.transition_to(self.stats_page)
        
    def show_settings(self):
        self.transition_to(self.settings_page)

    def show_about(self):
        self.transition_to(self.about_page)

    def restore_state(self):
        if self.settings.get("is_fullscreen"):
            self.showFullScreen()
        else:
            w = self.settings.get("window_width")
            h = self.settings.get("window_height")
            x = self.settings.get("window_x")
            y = self.settings.get("window_y")
            
            if w and h:
                self.resize(w, h)
            if x is not None and y is not None:
                self.move(x, y)
                
            if self.settings.get("is_maximized"):
                self.showMaximized()

    def closeEvent(self, event):
        # Save window state
        self.settings.set("is_maximized", self.isMaximized())
        if not self.isFullScreen() and not self.isMaximized():
            self.settings.set("window_width", self.width())
            self.settings.set("window_height", self.height())
            self.settings.set("window_x", self.x())
            self.settings.set("window_y", self.y())
        super().closeEvent(event)

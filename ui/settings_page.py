from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal
from storage.settings import SettingsManager
from storage.statistics import StatisticsManager
from game.achievement_manager import AchievementManager

class SettingsPage(QWidget):
    homeRequested = pyqtSignal()
    themeChanged = pyqtSignal(str) # 'dark' or 'light'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = SettingsManager()
        self.layout = QVBoxLayout(self)
        
        self.layout.addStretch()
        
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.setSpacing(25)
        
        checkbox_style = "font-size: 22px;"
        
        # Options
        self.chk_sound = QCheckBox("Enable Sound Effects")
        self.chk_sound.setStyleSheet(checkbox_style)
        self.chk_sound.setChecked(self.settings.get("sound_enabled"))
        self.chk_sound.toggled.connect(lambda v: self.settings.set("sound_enabled", v))
        content_layout.addWidget(self.chk_sound)
        
        self.chk_anim = QCheckBox("Enable Animations")
        self.chk_anim.setStyleSheet(checkbox_style)
        self.chk_anim.setChecked(self.settings.get("animations_enabled"))
        self.chk_anim.toggled.connect(lambda v: self.settings.set("animations_enabled", v))
        content_layout.addWidget(self.chk_anim)
        
        self.chk_keyboard = QCheckBox("Enable Physical Keyboard Input")
        self.chk_keyboard.setStyleSheet(checkbox_style)
        self.chk_keyboard.setChecked(self.settings.get("keyboard_input_enabled"))
        self.chk_keyboard.toggled.connect(lambda v: self.settings.set("keyboard_input_enabled", v))
        content_layout.addWidget(self.chk_keyboard)
        
        content_layout.addSpacing(30)
        
        # Reset Button
        self.btn_reset = QPushButton("Reset All Progress")
        self.btn_reset.setMinimumSize(350, 65)
        self.btn_reset.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.btn_reset.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_reset.setProperty("btnClass", "danger")
        self.btn_reset.clicked.connect(self.confirm_reset)
        content_layout.addWidget(self.btn_reset)
        
        self.layout.addLayout(content_layout)
        
        self.layout.addStretch()

    def confirm_reset(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Reset Progress")
        msg.setText("Are you sure you want to completely reset all statistics, streaks, and achievements? This cannot be undone.")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        
        # Apply current stylesheet manually for QMessageBox if needed, or rely on app-wide.
        
        ret = msg.exec()
        if ret == QMessageBox.StandardButton.Yes:
            StatisticsManager().reset_statistics()
            AchievementManager().reset()
            # We could emit a signal to show a toast here

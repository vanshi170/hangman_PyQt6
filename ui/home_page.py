from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal
from game.word_manager import WordManager

class HomePage(QWidget):
    # Signals for navigation
    playRequested = pyqtSignal(str, str, str) # mode, difficulty, category
    statsRequested = pyqtSignal()
    settingsRequested = pyqtSignal()
    aboutRequested = pyqtSignal()
    exitRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.word_manager = WordManager()
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setSpacing(20)

        # Title
        self.title = QLabel("HangmanX")
        self.title.setObjectName("mainTitle")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 48px; font-weight: bold; color: #4f8cff; margin-bottom: 20px;")
        self.layout.addWidget(self.title)

        # Controls container
        controls_layout = QHBoxLayout()
        controls_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls_layout.setSpacing(15)

        # Mode Selection
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Standard", "Daily", "Custom"])
        self.mode_combo.setMinimumWidth(150)
        self.mode_combo.currentTextChanged.connect(self.on_mode_changed)
        controls_layout.addWidget(self.mode_combo)

        # Category Selection
        self.category_combo = QComboBox()
        self.category_combo.addItems(self.word_manager.get_available_categories())
        self.category_combo.setMinimumWidth(150)
        controls_layout.addWidget(self.category_combo)

        # Difficulty Selection
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Easy", "Medium", "Hard"])
        self.difficulty_combo.setMinimumWidth(150)
        controls_layout.addWidget(self.difficulty_combo)

        self.layout.addLayout(controls_layout)

        # Buttons
        buttons_layout = QVBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buttons_layout.setSpacing(15)

        self.btn_play = self.create_button("Play Game", "success")
        self.btn_play.clicked.connect(self.on_play_clicked)
        buttons_layout.addWidget(self.btn_play)

        self.btn_stats = self.create_button("Statistics")
        self.btn_stats.clicked.connect(self.statsRequested.emit)
        buttons_layout.addWidget(self.btn_stats)

        self.btn_settings = self.create_button("Settings")
        self.btn_settings.clicked.connect(self.settingsRequested.emit)
        buttons_layout.addWidget(self.btn_settings)
        
        self.btn_about = self.create_button("About")
        self.btn_about.clicked.connect(self.aboutRequested.emit)
        buttons_layout.addWidget(self.btn_about)

        self.btn_exit = self.create_button("Exit", "danger")
        self.btn_exit.clicked.connect(self.exitRequested.emit)
        buttons_layout.addWidget(self.btn_exit)

        self.layout.addLayout(buttons_layout)

    def create_button(self, text, style_class="secondary"):
        btn = QPushButton(text)
        btn.setMinimumSize(250, 45)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setProperty("btnClass", style_class)
        return btn

    def on_mode_changed(self, mode):
        # Disable category for Daily and Custom
        if mode in ["Daily", "Custom"]:
            self.category_combo.setEnabled(False)
        else:
            self.category_combo.setEnabled(True)

    def on_play_clicked(self):
        mode = self.mode_combo.currentText()
        difficulty = self.difficulty_combo.currentText()
        category = self.category_combo.currentText()
        self.playRequested.emit(mode, difficulty, category)

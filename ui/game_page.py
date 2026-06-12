from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QInputDialog, QFrame
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer, QPoint
from PyQt6.QtGui import QFont
from .widgets.hangman_canvas import HangmanCanvas
from assets.sounds.sound_manager import SoundManager

class GamePage(QWidget):
    goHomeRequested = pyqtSignal()
    gameFinished = pyqtSignal(list) # emits unlocked achievements

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.sound_manager = SoundManager()
        self.layout = QVBoxLayout(self)
        
        # Header (Score, Attempts)
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        
        self.score_label = QLabel("Score: 0")
        self.score_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(self.score_label)
        
        header_layout.addSpacing(30)
        
        self.attempts_label = QLabel("Attempts: 6")
        self.attempts_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(self.attempts_label)
        
        header_layout.addStretch()
        
        self.layout.addLayout(header_layout)
        
        
        # Main Game Area
        game_area = QHBoxLayout()
        
        # Hangman Canvas
        self.canvas = HangmanCanvas()
        game_area.addWidget(self.canvas)
        
        # Right Side (Word + Hint Button)
        right_panel = QVBoxLayout()
        right_panel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.word_label = QLabel()
        self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.word_label.setStyleSheet("font-size: 40px; letter-spacing: 10px; font-family: monospace; font-weight: bold;")
        right_panel.addWidget(self.word_label)
        
        right_panel.addSpacing(40)
        
        self.btn_hint = QPushButton("Use Hint (-20 pts)")
        self.btn_hint.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_hint.clicked.connect(self.on_hint_clicked)
        right_panel.addWidget(self.btn_hint, alignment=Qt.AlignmentFlag.AlignCenter)
        
        game_area.addLayout(right_panel)
        self.layout.addLayout(game_area)
        
        
        self.layout.addSpacing(20)
        
        # Hint text at the bottom
        self.hint_label = QLabel("")
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hint_label.setWordWrap(True)
        self.hint_label.setStyleSheet("font-size: 20px; color: #a3a3a3; font-style: italic;")
        self.layout.addWidget(self.hint_label)
        
        self.layout.addSpacing(40)

        # Shake Animation
        self.shake_anim = QPropertyAnimation(self.word_label, b"pos")
        self.shake_anim.setDuration(300)

    def start_game(self, mode, difficulty, category):
        custom_word = None
        if mode == "Custom":
            text, ok = QInputDialog.getText(self, "Custom Word", "Enter word for player to guess:")
            if ok and text:
                custom_word = text.strip()
            else:
                # Cancelled, go back
                self.goHomeRequested.emit()
                return

        self.engine.start_game(mode=mode, category=category, custom_word=custom_word, difficulty=difficulty)
        self.canvas.max_stage = self.engine.max_attempts
        self.hint_label.setText("")
        self.update_ui()
        self.canvas.set_stage(0)

    def update_ui(self):
        self.word_label.setText(self.engine.get_display_word())
        self.score_label.setText(f"Score: {self.engine.score_manager.current_score}")
        self.attempts_label.setText(f"Attempts: {self.engine.get_remaining_attempts()}")
        self.canvas.set_stage(self.engine.incorrect_guesses)

        # Disable hint if not allowed
        if not self.engine.DIFFICULTIES[self.engine.difficulty].get("hints_allowed", True):
            self.btn_hint.setEnabled(False)
            self.btn_hint.setText("Hints Disabled")
        elif self.engine.hints_used > 0:
            self.btn_hint.setEnabled(False)
            self.btn_hint.setText("Hint Used")
        else:
            self.btn_hint.setEnabled(self.engine.state == self.engine.STATE_PLAYING)
            self.btn_hint.setText(f"Use Hint (-{self.engine.score_manager.HINT_COST} pts)")

    def on_letter_clicked(self, letter):
        if self.engine.state != self.engine.STATE_PLAYING:
            return
            
        success, msg = self.engine.guess_letter(letter)
        if msg in ["Already Guessed", "Invalid Input"]:
            return

        if success:
            self.sound_manager.play("correct")
        else:
            self.sound_manager.play("wrong")
            self.shake_word()

        self.update_ui()
        self.check_game_over()

    def on_hint_clicked(self):
        success, hint = self.engine.use_hint()
        if success:
            self.sound_manager.play("correct")
            self.hint_label.setText(f"Hint: {hint}")
            self.update_ui()
            self.check_game_over()
        else:
            self.sound_manager.play("wrong")
            # Maybe show a toast for 'not enough score'
            self.shake_word()

    def handle_physical_key(self, text):
        if len(text) == 1 and text.isalpha():
            self.on_letter_clicked(text.upper())

    def shake_word(self):
        if not self.engine.settings.get("animations_enabled"):
            return
        pos = self.word_label.pos()
        self.shake_anim.setKeyValueAt(0, pos)
        self.shake_anim.setKeyValueAt(0.25, pos + QPoint(-10, 0)) # type: ignore
        self.shake_anim.setKeyValueAt(0.5, pos + QPoint(10, 0))   # type: ignore
        self.shake_anim.setKeyValueAt(0.75, pos + QPoint(-10, 0)) # type: ignore
        self.shake_anim.setKeyValueAt(1, pos)
        self.shake_anim.start()

    def check_game_over(self):
        if self.engine.state != self.engine.STATE_PLAYING:
            # End of game, wait 1 second then emit
            if self.engine.state == self.engine.STATE_WON:
                self.sound_manager.play("win")
            else:
                self.sound_manager.play("loss")
                
            unlocked = self.engine._finalize_game() # Get achievements
            QTimer.singleShot(1500, lambda: self.gameFinished.emit(unlocked))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal

class SummaryPage(QWidget):
    homeRequested = pyqtSignal()
    playAgainRequested = pyqtSignal()

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setSpacing(20)

        self.title_label = QLabel("Game Over")
        self.title_label.setObjectName("summaryTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        self.word_label = QLabel()
        self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.word_label.setStyleSheet("font-size: 32px; letter-spacing: 5px; color: #4f8cff; font-weight: bold;")
        self.layout.addWidget(self.word_label)

        # Stats Grid
        self.grid_container = QWidget()
        self.grid = QGridLayout(self.grid_container)
        self.grid.setSpacing(15)
        
        self.lbl_score = self.add_stat_row(0, "Score Earned:", "0")
        self.lbl_accuracy = self.add_stat_row(1, "Accuracy:", "0%")
        self.lbl_correct = self.add_stat_row(2, "Correct Guesses:", "0")
        self.lbl_incorrect = self.add_stat_row(3, "Incorrect Guesses:", "0")
        self.lbl_remaining = self.add_stat_row(4, "Remaining Attempts:", "0")

        self.layout.addWidget(self.grid_container, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.layout.addSpacing(30)

        # Buttons
        self.btn_play_again = QPushButton("Play Again")
        self.btn_play_again.setMinimumSize(200, 45)
        self.btn_play_again.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_play_again.setProperty("btnClass", "primary")
        self.btn_play_again.clicked.connect(self.playAgainRequested.emit)
        self.layout.addWidget(self.btn_play_again, alignment=Qt.AlignmentFlag.AlignCenter)

    def add_stat_row(self, row, label_text, value_text):
        lbl_title = QLabel(label_text)
        lbl_title.setStyleSheet("font-size: 16px; color: #94a3b8;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        lbl_val = QLabel(value_text)
        lbl_val.setStyleSheet("font-size: 16px; font-weight: bold;")
        lbl_val.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        self.grid.addWidget(lbl_title, row, 0)
        self.grid.addWidget(lbl_val, row, 1)
        return lbl_val

    def update_summary(self):
        state = self.engine.state
        if state == self.engine.STATE_WON:
            self.title_label.setText("Congratulations!")
            self.title_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #22c55e;")
        else:
            self.title_label.setText("Game Over")
            self.title_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #ef4444;")

        self.word_label.setText(self.engine.current_word)
        self.lbl_score.setText(str(self.engine.score_manager.current_score))
        
        # Calculate Accuracy
        correct_guesses = len([c for c in self.engine.guessed_letters if c in self.engine.current_word])
        total_guesses = len(self.engine.guessed_letters)
        accuracy = int((correct_guesses / total_guesses * 100)) if total_guesses > 0 else 0
        
        self.lbl_accuracy.setText(f"{accuracy}%")
        self.lbl_correct.setText(str(correct_guesses))
        self.lbl_incorrect.setText(str(self.engine.incorrect_guesses))
        self.lbl_remaining.setText(str(self.engine.get_remaining_attempts()))

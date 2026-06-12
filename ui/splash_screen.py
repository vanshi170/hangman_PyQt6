from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

class SplashScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(400, 300)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Background Container
        self.container = QWidget(self)
        self.container.setObjectName("splashContainer")
        self.container.setStyleSheet("""
            QWidget#splashContainer {
                background-color: #0f1117;
                border-radius: 16px;
                border: 2px solid #334155;
            }
        """)
        container_layout = QVBoxLayout(self.container)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Logo / Title
        self.title_label = QLabel("HangmanX")
        self.title_label.setStyleSheet("color: #4f8cff; font-family: 'Segoe UI', Inter; font-size: 36px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(self.title_label)
        
        self.subtitle_label = QLabel("Premium Word Game")
        self.subtitle_label.setStyleSheet("color: #94a3b8; font-family: 'Segoe UI', Inter; font-size: 14px;")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(self.subtitle_label)

        container_layout.addSpacing(30)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(6)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #1c1f26;
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background-color: #4f8cff;
                border-radius: 3px;
            }
        """)
        container_layout.addWidget(self.progress)
        
        self.layout.addWidget(self.container)

        self.progress_value = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)

    def start(self, callback):
        self.callback = callback
        self.show()
        self.timer.start(20) # 20ms * 100 = 2 seconds

    def update_progress(self):
        self.progress_value += 1
        self.progress.setValue(self.progress_value)
        if self.progress_value >= 100:
            self.timer.stop()
            self.close()
            if self.callback:
                self.callback()

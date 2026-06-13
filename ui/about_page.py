from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal

class AboutPage(QWidget):
    homeRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setSpacing(15)

        title = QLabel("About HangmanX")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #4f8cff;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title)

        version = QLabel("Version: 1.0.0")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(version)

        desc = QLabel("A premium desktop implementation of the classic Hangman game.\nBuilt with Python 3.12+ and PyQt6.")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(desc)
        
        self.layout.addSpacing(20)

        dev_info = QLabel("Developed for Portfolio & Showcase")
        dev_info.setStyleSheet("color: #94a3b8;")
        dev_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(dev_info)

        self.layout.addSpacing(30)

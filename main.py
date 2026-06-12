import sys
import traceback
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from logging_config import logger
from ui.splash_screen import SplashScreen
from ui.main_window import MainWindow

def global_exception_handler(exctype, value, tb):
    """Catch unhandled exceptions and log them."""
    error_msg = "".join(traceback.format_exception(exctype, value, tb))
    logger.critical(f"Unhandled Exception: {error_msg}")
    
    # Optionally show a generic error dialog to the user
    # (Be careful here if QApplication is not running or crashed badly)
    try:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Critical Error")
        msg.setText("A critical error has occurred. Please check the logs.")
        msg.setDetailedText(error_msg)
        msg.exec()
    except Exception:
        pass
        
    sys.exit(1)

def main():
    # Set global exception handler
    sys.excepthook = global_exception_handler
    
    logger.info("Starting HangmanX...")

    # Enable High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    app.setApplicationName("HangmanX")
    
    # Optionally load custom font here if available
    # QFontDatabase.addApplicationFont("path/to/font.ttf")

    # Show Splash Screen
    splash = SplashScreen()
    
    # We will pass a callback to the splash screen that shows the main window
    def on_splash_finished():
        global main_window
        main_window = MainWindow()
        main_window.show()

    splash.start(callback=on_splash_finished)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

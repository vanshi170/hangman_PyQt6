from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor

class ToastNotification(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.container = QWidget(self)
        self.container.setObjectName("toastContainer")
        self.container.setStyleSheet("""
            QWidget#toastContainer {
                background-color: #1c1f26;
                color: #f8fafc;
                border-radius: 8px;
                border: 1px solid #334155;
            }
        """)
        
        container_layout = QHBoxLayout(self.container)
        container_layout.setContentsMargins(16, 12, 16, 12)
        
        self.message_label = QLabel("")
        self.message_label.setStyleSheet("font-family: 'Segoe UI', Inter, sans-serif; font-size: 14px; font-weight: 500;")
        container_layout.addWidget(self.message_label)
        
        self.layout.addWidget(self.container)
        
        # Shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        self.container.setGraphicsEffect(shadow)
        
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide_toast)
        
        self.setWindowOpacity(0.0)

    def show_toast(self, message, duration_ms=2500, type="info"):
        self.message_label.setText(message)
        
        # Adjust colors based on type
        if type == "success":
            color = "#22c55e"
        elif type == "error":
            color = "#ef4444"
        elif type == "warning":
            color = "#eab308"
        else:
            color = "#4f8cff"
            
        self.container.setStyleSheet(f"""
            QWidget#toastContainer {{
                background-color: #1c1f26;
                color: #f8fafc;
                border-radius: 8px;
                border-left: 4px solid {color};
            }}
        """)
        
        self.adjustSize()
        
        # Position at top center of parent
        if self.parent():
            parent_rect = self.parent().rect()
            parent_pos = self.parent().mapToGlobal(parent_rect.topLeft())
            x = parent_pos.x() + (parent_rect.width() - self.width()) // 2
            y = parent_pos.y() + 40
            self.move(x, y)
            
        self.show()
        
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()
        
        self.timer.start(duration_ms)

    def hide_toast(self):
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.Type.InCubic)
        self.animation.finished.connect(self.hide)
        self.animation.start()

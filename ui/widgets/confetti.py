import math
import random
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import Qt, QTimer, QRectF

class ConfettiWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.particles = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_particles)
        self.is_running = False
        
        # Predefined colors for confetti
        self.colors = [
            QColor("#ef4444"), # Red
            QColor("#3b82f6"), # Blue
            QColor("#22c55e"), # Green
            QColor("#eab308"), # Yellow
            QColor("#a855f7"), # Purple
            QColor("#f97316")  # Orange
        ]

    def start(self, duration_ms=3000):
        self.particles = []
        width = self.width()
        
        # Create 150 particles
        for _ in range(150):
            x = width / 2 + random.uniform(-50, 50)
            y = self.height() / 2 + random.uniform(-50, 50)
            vx = random.uniform(-8, 8)
            vy = random.uniform(-15, -5)
            color = random.choice(self.colors)
            size = random.uniform(5, 12)
            rotation = random.uniform(0, 360)
            rot_speed = random.uniform(-10, 10)
            self.particles.append([x, y, vx, vy, color, size, rotation, rot_speed])
            
        self.is_running = True
        self.timer.start(16) # ~60fps
        
        # Stop after duration
        QTimer.singleShot(duration_ms, self.stop)
        
    def stop(self):
        self.is_running = False
        self.timer.stop()
        self.particles = []
        self.update()

    def update_particles(self):
        gravity = 0.4
        drag = 0.99
        
        for p in self.particles:
            p[2] *= drag # vx
            p[3] += gravity # vy
            p[0] += p[2] # x
            p[1] += p[3] # y
            p[6] += p[7] # rotation
            
        # Remove off-screen particles
        self.particles = [p for p in self.particles if p[1] < self.height() + 50]
        
        if not self.particles:
            self.stop()
            
        self.update()

    def paintEvent(self, event):
        if not self.is_running:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        for p in self.particles:
            x, y, _, _, color, size, rotation, _ = p
            painter.save()
            painter.translate(x, y)
            painter.rotate(rotation)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(color)
            # Draw a small rectangle
            painter.drawRect(QRectF(-size/2, -size/2, size, size*0.8))
            painter.restore()

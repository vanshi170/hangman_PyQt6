from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QTimer

class HangmanCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 350)
        self.stage = 0
        self.max_stage = 6
        
        # Colors
        self.wood_color = QColor("#d97706")
        self.rope_color = QColor("#fde047")
        self.body_color = QColor("#f8fafc") # Default to light text, can be updated via theme

    def set_theme_colors(self, body_color_hex):
        self.body_color = QColor(body_color_hex)
        self.update()

    def set_stage(self, stage):
        self.stage = min(stage, self.max_stage)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self.width()
        h = self.height()
        
        # Dimensions
        base_y = h - 20
        base_w = w * 0.6
        base_x = (w - base_w) / 2
        
        pole_x = w * 0.3
        pole_y = 40
        pole_h = base_y - pole_y
        
        beam_w = w * 0.4
        beam_x = pole_x
        
        rope_x = pole_x + beam_w - 20
        rope_y = pole_y
        rope_h = 40
        
        head_radius = 25
        head_y = rope_y + rope_h + head_radius
        
        body_y1 = head_y + head_radius
        body_y2 = body_y1 + 80
        
        # Pens
        wood_pen = QPen(self.wood_color, 8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        rope_pen = QPen(self.rope_color, 4, Qt.PenStyle.SolidLine)
        body_pen = QPen(self.body_color, 6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        
        # Always draw base and gallows (Stage 0 means empty gallows, wait, actually let's draw gallows always)
        painter.setPen(wood_pen)
        # Base
        painter.drawLine(int(base_x), int(base_y), int(base_x + base_w), int(base_y))
        # Pole
        painter.drawLine(int(pole_x), int(base_y), int(pole_x), int(pole_y))
        # Beam
        painter.drawLine(int(beam_x), int(pole_y), int(beam_x + beam_w), int(pole_y))
        # Support
        painter.drawLine(int(pole_x), int(pole_y + 40), int(pole_x + 40), int(pole_y))
        
        # Rope
        painter.setPen(rope_pen)
        painter.drawLine(int(rope_x), int(rope_y), int(rope_x), int(rope_y + rope_h))

        painter.setPen(body_pen)

        draw_head = self.stage >= 1
        draw_body = (self.max_stage <= 6 and self.stage >= 1) or (self.max_stage > 6 and self.stage >= 2)
        draw_l_arm = (self.max_stage <= 6 and self.stage >= 2) or (self.max_stage > 6 and self.stage >= 3)
        draw_r_arm = (self.max_stage <= 6 and self.stage >= 3) or (self.max_stage > 6 and self.stage >= 4)
        draw_l_leg = (self.max_stage <= 6 and self.stage >= 4) or (self.max_stage > 6 and self.stage >= 5)
        draw_r_leg = (self.max_stage <= 6 and self.stage >= 5) or (self.max_stage > 6 and self.stage >= 6)

        if draw_head:
            painter.drawEllipse(int(rope_x - head_radius), int(rope_y + rope_h), head_radius*2, head_radius*2)
        if draw_body:
            painter.drawLine(int(rope_x), int(body_y1), int(rope_x), int(body_y2))
        if draw_l_arm:
            painter.drawLine(int(rope_x), int(body_y1 + 10), int(rope_x - 40), int(body_y1 + 50))
        if draw_r_arm:
            painter.drawLine(int(rope_x), int(body_y1 + 10), int(rope_x + 40), int(body_y1 + 50))
        if draw_l_leg:
            painter.drawLine(int(rope_x), int(body_y2), int(rope_x - 30), int(body_y2 + 60))
        if draw_r_leg:
            painter.drawLine(int(rope_x), int(body_y2), int(rope_x + 30), int(body_y2 + 60))

        # Eyes logic
        draw_both_eyes = (self.max_stage <= 6 and self.stage >= 6) or (self.max_stage == 7 and self.stage >= 7)
        draw_left_eye_only = (self.max_stage >= 8 and self.stage >= 7)
        draw_right_eye_too = (self.max_stage >= 8 and self.stage >= 8)

        if draw_both_eyes or draw_left_eye_only or draw_right_eye_too:
            painter.setPen(QPen(self.body_color, 2))
            eyey = head_y - 5
            eyex_l = rope_x - 8
            eyex_r = rope_x + 8

            if draw_both_eyes or draw_left_eye_only:
                painter.drawLine(int(eyex_l - 4), int(eyey - 4), int(eyex_l + 4), int(eyey + 4))
                painter.drawLine(int(eyex_l - 4), int(eyey + 4), int(eyex_l + 4), int(eyey - 4))
            
            if draw_both_eyes or draw_right_eye_too:
                painter.drawLine(int(eyex_r - 4), int(eyey - 4), int(eyex_r + 4), int(eyey + 4))
                painter.drawLine(int(eyex_r - 4), int(eyey + 4), int(eyex_r + 4), int(eyey - 4))

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFileDialog
from PyQt6.QtCore import Qt, pyqtSignal
from storage.statistics import StatisticsManager
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class StatsPage(QWidget):
    homeRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.stats_manager = StatisticsManager()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Scroll Area for charts
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 5, 0, 0)
        
        # Text Stats
        self.text_stats_label = QLabel()
        self.text_stats_label.setStyleSheet("font-size: 16px; margin-top: 5px; margin-bottom: 5px;")
        self.content_layout.addWidget(self.text_stats_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Charts
        self.figure = Figure(figsize=(8, 12), dpi=100)
        self.figure.patch.set_alpha(1.0) # opaque background
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: transparent;")
        
        self.content_layout.addWidget(self.canvas)
        
        self.scroll_area.setWidget(self.content_widget)
        self.layout.addWidget(self.scroll_area)

    def export_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Statistics", "", "CSV Files (*.csv)")
        if file_path:
            self.stats_manager.export_csv(file_path)

    def update_stats(self, theme='dark'):
        self.text_stats_label.setText(
            f"Games Played: {self.stats_manager.get('games_played')} | "
            f"Win Rate: {self.stats_manager.get_win_rate():.1f}% | "
            f"Highest Score: {self.stats_manager.get('highest_score')} | "
            f"Total Letters: {self.stats_manager.get('total_letters_guessed')}"
        )
        
        self.figure.clear()
        
        text_color = '#f8fafc' if theme == 'dark' else '#0f172a'
        bg_color = '#0f1117' if theme == 'dark' else '#f8fafc'
        
        self.figure.set_facecolor(bg_color)
        
        import matplotlib.gridspec as gridspec
        gs = self.figure.add_gridspec(2, 2, height_ratios=[1, 1])
        
        # 1. Difficulty Usage (Bar)
        ax2 = self.figure.add_subplot(gs[0, 0])
        ax2.set_facecolor(bg_color)
        diffs = self.stats_manager.get("difficulties_played")
        labels = list(diffs.keys())
        values = list(diffs.values())
        ax2.bar(labels, values, color='#4f8cff')
        ax2.set_title('Difficulty Usage', color=text_color)
        ax2.tick_params(axis='x', colors=text_color)
        ax2.tick_params(axis='y', colors=text_color)
        for spine in ax2.spines.values():
            spine.set_color(text_color)
            
        # 2. Wins vs Losses (Pie)
        ax1 = self.figure.add_subplot(gs[0, 1])
        ax1.set_facecolor(bg_color)
        wins = self.stats_manager.get("games_won")
        losses = self.stats_manager.get("games_lost")
        if wins + losses > 0:
            ax1.pie([wins, losses], labels=['Wins', 'Losses'], colors=['#22c55e', '#ef4444'], autopct='%1.1f%%', textprops={'color': text_color})
        else:
            ax1.text(0.5, 0.5, "No Data", ha='center', va='center', color=text_color)
        ax1.set_title('Win/Loss Ratio', color=text_color)
            
        # 3. Score Progression (Line)
        ax3 = self.figure.add_subplot(gs[1, :])
        ax3.set_facecolor(bg_color)
        prog = self.stats_manager.get("score_progression")
        if prog:
            ax3.plot(range(1, len(prog)+1), prog, marker='o', color='#eab308')
        else:
            ax3.text(0.5, 0.5, "No Data", ha='center', va='center', color=text_color)
        ax3.set_title('Score Progression (Last 50)', color=text_color)
        ax3.tick_params(axis='x', colors=text_color)
        ax3.tick_params(axis='y', colors=text_color)
        for spine in ax3.spines.values():
            spine.set_color(text_color)

        self.figure.tight_layout(h_pad=5.0)
        self.canvas.draw()

import json
import os
import csv
from logging_config import logger

STATS_FILE = os.path.join("data", "statistics.json")

DEFAULT_STATS = {
    "games_played": 0,
    "games_won": 0,
    "games_lost": 0,
    "highest_score": 0,
    "total_score": 0,
    "total_letters_guessed": 0,
    "difficulties_played": {
        "Easy": 0,
        "Medium": 0,
        "Hard": 0
    },
    "score_progression": [] # List of scores from recent games
}

class StatisticsManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StatisticsManager, cls).__new__(cls)
            cls._instance._stats = {}
            cls._instance.load()
        return cls._instance

    def load(self):
        if not os.path.exists("data"):
            os.makedirs("data")
            
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._stats = {**DEFAULT_STATS, **data}
                logger.info("Statistics loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load statistics: {e}")
                self._stats = DEFAULT_STATS.copy()
        else:
            self._stats = DEFAULT_STATS.copy()
            self.save()

    def save(self):
        try:
            if not os.path.exists("data"):
                os.makedirs("data")
            with open(STATS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self._stats, f, indent=4)
            logger.info("Statistics saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save statistics: {e}")

    def get(self, key):
        return self._stats.get(key, DEFAULT_STATS.get(key))

    def update_stat(self, key, value, increment=False):
        if increment:
            current = self.get(key)
            if isinstance(current, dict):
                logger.warning(f"Cannot increment dictionary stat directly: {key}")
                return
            self._stats[key] = current + value
        else:
            self._stats[key] = value
        self.save()

    def record_game(self, won, score, difficulty, letters_guessed):
        self.update_stat("games_played", 1, increment=True)
        if won:
            self.update_stat("games_won", 1, increment=True)
        else:
            self.update_stat("games_lost", 1, increment=True)
        
        self.update_stat("total_score", score, increment=True)
        self.update_stat("total_letters_guessed", letters_guessed, increment=True)
        
        highest = self.get("highest_score")
        if score > highest:
            self.update_stat("highest_score", score)

        diffs = self.get("difficulties_played")
        if difficulty in diffs:
            diffs[difficulty] += 1
            self._stats["difficulties_played"] = diffs

        prog = self.get("score_progression")
        prog.append(score)
        # Keep last 50 games for the chart
        if len(prog) > 50:
            prog = prog[-50:]
        self._stats["score_progression"] = prog

        self.save()

    def get_win_rate(self):
        played = self.get("games_played")
        if played == 0:
            return 0.0
        return (self.get("games_won") / played) * 100

    def get_average_score(self):
        played = self.get("games_played")
        if played == 0:
            return 0.0
        return self.get("total_score") / played

    def reset_statistics(self):
        self._stats = DEFAULT_STATS.copy()
        self.save()
        logger.info("Statistics reset to defaults.")

    def export_csv(self, filepath):
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Stat", "Value"])
                writer.writerow(["Games Played", self.get("games_played")])
                writer.writerow(["Games Won", self.get("games_won")])
                writer.writerow(["Games Lost", self.get("games_lost")])
                writer.writerow(["Win Rate %", f"{self.get_win_rate():.2f}"])
                writer.writerow(["Highest Score", self.get("highest_score")])
                writer.writerow(["Average Score", f"{self.get_average_score():.2f}"])
                writer.writerow(["Total Letters Guessed", self.get("total_letters_guessed")])
                writer.writerow(["Easy Games", self.get("difficulties_played").get("Easy", 0)])
                writer.writerow(["Medium Games", self.get("difficulties_played").get("Medium", 0)])
                writer.writerow(["Hard Games", self.get("difficulties_played").get("Hard", 0)])
            logger.info(f"Statistics exported to CSV at {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to export CSV: {e}")
            return False

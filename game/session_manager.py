import time
from logging_config import logger

class SessionManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance.start_time = time.time()
            cls._instance.games_played = 0
            cls._instance.session_score = 0
        return cls._instance

    def record_game(self, score):
        self.games_played += 1
        self.session_score += score
        logger.debug(f"Session updated: {self.games_played} games, {self.session_score} score")

    def get_duration_seconds(self):
        return int(time.time() - self.start_time)
        
    def get_formatted_duration(self):
        seconds = self.get_duration_seconds()
        mins = seconds // 60
        secs = seconds % 60
        hours = mins // 60
        mins = mins % 60
        if hours > 0:
            return f"{hours}h {mins}m {secs}s"
        return f"{mins}m {secs}s"

    def reset_session(self):
        self.start_time = time.time()
        self.games_played = 0
        self.session_score = 0
        logger.info("Session reset")

import json
import os
from logging_config import logger

ACHIEVEMENTS_FILE = os.path.join("data", "achievements.json")

class AchievementManager:
    # Achievement Definitions: ID -> (Title, Description)
    ACHIEVEMENTS = {
        "first_win": ("First Victory", "Win your first game."),
        "win_5": ("5 Wins", "Win 5 games in total."),
        "win_10": ("10 Wins", "Win 10 games in total."),
        "perfect_game": ("Perfect Game", "Win a game without any incorrect guesses."),
        "100_correct": ("100 Correct Guesses", "Guess 100 correct letters across all games."),
        "no_hint": ("No Hint Victory", "Win a game without using any hints.")
    }

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AchievementManager, cls).__new__(cls)
            cls._instance.unlocked = []
            cls._instance.load()
        return cls._instance

    def load(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if os.path.exists(ACHIEVEMENTS_FILE):
            try:
                with open(ACHIEVEMENTS_FILE, 'r', encoding='utf-8') as f:
                    self.unlocked = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load achievements: {e}")
                self.unlocked = []
        else:
            self.unlocked = []
            self.save()

    def save(self):
        try:
            with open(ACHIEVEMENTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.unlocked, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save achievements: {e}")

    def unlock(self, ach_id):
        if ach_id in self.ACHIEVEMENTS and ach_id not in self.unlocked:
            self.unlocked.append(ach_id)
            self.save()
            title = self.ACHIEVEMENTS[ach_id][0]
            logger.info(f"Achievement Unlocked: {title}")
            return title
        return None

    def check_post_game(self, stats_manager, current_game_perfect, current_game_no_hint):
        """Checks and unlocks achievements based on stats and current game performance. Returns list of unlocked titles."""
        newly_unlocked = []
        
        wins = stats_manager.get("games_won")
        correct_guesses = stats_manager.get("total_letters_guessed") # Note: This is all guesses, we might need a separate correct guesses tracker

        if wins >= 1:
            title = self.unlock("first_win")
            if title: newly_unlocked.append(title)
            
        if wins >= 5:
            title = self.unlock("win_5")
            if title: newly_unlocked.append(title)
            
        if wins >= 10:
            title = self.unlock("win_10")
            if title: newly_unlocked.append(title)

        if current_game_perfect:
            title = self.unlock("perfect_game")
            if title: newly_unlocked.append(title)

        if current_game_no_hint:
            title = self.unlock("no_hint")
            if title: newly_unlocked.append(title)

        # Assuming for now total_letters_guessed is a good enough proxy, or we can add a specific stat for correct guesses.
        if correct_guesses >= 100:
            title = self.unlock("100_correct")
            if title: newly_unlocked.append(title)

        return newly_unlocked

    def reset(self):
        self.unlocked = []
        self.save()

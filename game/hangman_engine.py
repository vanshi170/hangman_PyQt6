from logging_config import logger
from .word_manager import WordManager
from .score_manager import ScoreManager
from storage.statistics import StatisticsManager
from storage.settings import SettingsManager
from .achievement_manager import AchievementManager
from .session_manager import SessionManager
import random

class HangmanEngine:
    # Game States
    STATE_PLAYING = "playing"
    STATE_WON = "won"
    STATE_LOST = "lost"

    # Difficulties config
    DIFFICULTIES = {
        "Easy": {"attempts": 8, "hints_allowed": True},
        "Medium": {"attempts": 7, "hints_allowed": False},
        "Hard": {"attempts": 6, "hints_allowed": False}
    }

    def __init__(self):
        self.word_manager = WordManager()
        self.score_manager = ScoreManager()
        self.stats_manager = StatisticsManager()
        self.settings = SettingsManager()
        self.achievement_manager = AchievementManager()
        self.session_manager = SessionManager()

        self.current_word = ""
        self.current_hint = ""
        self.guessed_letters = set()
        self.incorrect_guesses = 0
        self.max_attempts = 6
        self.state = self.STATE_PLAYING
        self.hints_used = 0
        self.difficulty = "Medium"
        self.mode = "Standard"

    def start_game(self, mode="Standard", category=None, custom_word=None, difficulty=None):
        self.mode = mode
        if difficulty is None:
            self.difficulty = self.settings.get("last_difficulty")
        else:
            self.difficulty = difficulty
            self.settings.set("last_difficulty", difficulty)
            
        config = self.DIFFICULTIES.get(self.difficulty, self.DIFFICULTIES["Medium"])
        self.max_attempts = config["attempts"]

        if mode == "Custom" and custom_word:
            self.current_word = custom_word.upper()
            self.current_hint = "Custom word provided by a friend"
        elif mode == "Daily":
            self.current_word, self.current_hint = self.word_manager.get_daily_word()
        else:
            self.current_word, self.current_hint = self.word_manager.get_random_word(category)

        self.guessed_letters.clear()
        self.incorrect_guesses = 0
        self.hints_used = 0
        self.score_manager.reset()
        self.state = self.STATE_PLAYING
        logger.info(f"Started new game. Word: {self.current_word}, Mode: {self.mode}, Difficulty: {self.difficulty}")

    def guess_letter(self, letter):
        if self.state != self.STATE_PLAYING:
            return False, "Game Over"

        letter = letter.upper()
        if not letter.isalpha() or len(letter) != 1:
            return False, "Invalid Input"

        if letter in self.guessed_letters:
            return False, "Already Guessed"

        self.guessed_letters.add(letter)

        if letter in self.current_word:
            self.score_manager.add_correct_guess()
            self._check_win_condition()
            return True, "Correct"
        else:
            self.incorrect_guesses += 1
            self._check_loss_condition()
            return False, "Incorrect"

    def use_hint(self):
        if self.state != self.STATE_PLAYING:
            return False, "Game Over"
            
        config = self.DIFFICULTIES.get(self.difficulty, self.DIFFICULTIES["Medium"])
        if not config.get("hints_allowed", True) and self.difficulty == "Hard":
            return False, "Hints disabled on Hard"

        if self.hints_used > 0:
            # Already unlocked the hint
            return True, self.current_hint

        if self.score_manager.use_hint():
            self.hints_used += 1
            return True, self.current_hint
        return False, "Not enough score"

    def _check_win_condition(self):
        if all(char in self.guessed_letters for char in self.current_word):
            self.state = self.STATE_WON
            unused = self.max_attempts - self.incorrect_guesses
            self.score_manager.add_completion_bonus(unused)
            self._finalize_game()

    def _check_loss_condition(self):
        if self.incorrect_guesses >= self.max_attempts:
            self.state = self.STATE_LOST
            self._finalize_game()

    def _finalize_game(self):
        won = (self.state == self.STATE_WON)
        
        # Streak tracking
        if won:
            self.score_manager.increment_streak()
        else:
            self.score_manager.reset_streak()
            
        # Stats update
        self.stats_manager.record_game(
            won=won, 
            score=self.score_manager.current_score, 
            difficulty=self.difficulty,
            letters_guessed=len(self.guessed_letters)
        )
        
        # Session update
        self.session_manager.record_game(self.score_manager.current_score)
        
        # Check Achievements
        perfect = (self.incorrect_guesses == 0)
        no_hint = (self.hints_used == 0)
        unlocked = self.achievement_manager.check_post_game(self.stats_manager, perfect, no_hint)
        
        logger.info(f"Game Finalized. State: {self.state}. Score: {self.score_manager.current_score}")
        return unlocked

    def get_display_word(self):
        return " ".join([char if char in self.guessed_letters else "_" for char in self.current_word])
        
    def get_remaining_attempts(self):
        return max(0, self.max_attempts - self.incorrect_guesses)

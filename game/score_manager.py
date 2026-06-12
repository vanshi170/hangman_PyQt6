from logging_config import logger

class ScoreManager:
    POINTS_CORRECT_GUESS = 10
    POINTS_COMPLETION = 50
    POINTS_UNUSED_ATTEMPT = 5
    HINT_COST = 20

    def __init__(self):
        self.current_score = 0
        self.streak = 0
        self.longest_streak = 0

    def reset(self):
        self.current_score = 0

    def add_correct_guess(self):
        self.current_score += self.POINTS_CORRECT_GUESS
        logger.debug(f"Score added: +{self.POINTS_CORRECT_GUESS}. Total: {self.current_score}")

    def add_completion_bonus(self, unused_attempts):
        bonus = self.POINTS_COMPLETION + (unused_attempts * self.POINTS_UNUSED_ATTEMPT)
        self.current_score += bonus
        logger.debug(f"Completion bonus: +{bonus}. Total: {self.current_score}")

    def use_hint(self):
        if self.current_score >= self.HINT_COST:
            self.current_score -= self.HINT_COST
            logger.debug(f"Hint used. Cost: -{self.HINT_COST}. Total: {self.current_score}")
            return True
        else:
            # Score can go below zero if they use hints early? The requirement says "consumes score".
            # If we allow negative or zero. Let's just deduct it and allow zero floor.
            self.current_score = max(0, self.current_score - self.HINT_COST)
            logger.debug(f"Hint used. Cost: -{self.HINT_COST}. Total (floored): {self.current_score}")
            return True

    def increment_streak(self):
        self.streak += 1
        if self.streak > self.longest_streak:
            self.longest_streak = self.streak
        logger.info(f"Win streak increased to {self.streak}")

    def reset_streak(self):
        self.streak = 0
        logger.info("Win streak reset to 0")

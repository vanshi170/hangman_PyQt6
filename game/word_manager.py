import random
import datetime
from logging_config import logger

class WordManager:
    DEFAULT_WORDS = {
        "PYTHON": "A popular programming language named after a snake",
        "COMPUTER": "An electronic device for storing and processing data",
        "PROGRAM": "A set of instructions that a computer can execute",
        "DEVELOPER": "A person who writes computer software",
        "KEYBOARD": "Input device used to input text to a computer device"
    }
    
    CATEGORIES = {
        "Programming": {**DEFAULT_WORDS, "ALGORITHM": "A step-by-step procedure for calculations", "VARIABLE": "A storage location paired with an associated symbolic name", "FUNCTION": "A block of organized, reusable code", "DATABASE": "An organized collection of data"},
        "Technology": {"INTERNET": "A global computer network", "HARDWARE": "The physical parts of a computer", "SOFTWARE": "Programs and other operating information used by a computer", "NETWORK": "Two or more computers connected together", "MONITOR": "An output device that displays information", "ROUTER": "A device that forwards data packets between networks"},
        "Countries": {"AUSTRALIA": "A country and continent surrounded by the Indian and Pacific oceans", "BRAZIL": "The largest country in South America", "CANADA": "A country in North America known for maple syrup", "DENMARK": "A Scandinavian country in Europe", "EGYPT": "A country linking northeast Africa with the Middle East", "FRANCE": "A country in Western Europe known for the Eiffel Tower"},
        "Animals": {"ELEPHANT": "A large mammal with a trunk", "GIRAFFE": "A tall African mammal with a very long neck", "KANGAROO": "A large plant-eating marsupial with a long powerful tail", "PENGUIN": "A flightless seabird", "DOLPHIN": "A small gregarious toothed whale", "TIGER": "A very large solitary cat with a yellow-orange coat and dark stripes"},
        "Movies": {"INCEPTION": "A movie about planting an idea in someone's mind through dreams", "MATRIX": "A movie about a simulated reality", "AVATAR": "A movie featuring blue humanoids on Pandora", "TITANIC": "A movie about a famous sinking ship", "GLADIATOR": "A movie about a Roman general who becomes a gladiator", "ALIEN": "A sci-fi horror movie featuring a terrifying extraterrestrial"}
    }

    def __init__(self):
        # We must support the original 5 words as the default assignment requirement
        self.categories = self.CATEGORIES.copy()

    def get_random_word(self, category=None):
        if category and category in self.categories:
            word_dict = self.categories[category]
        else:
            word_dict = self.DEFAULT_WORDS
            
        word = random.choice(list(word_dict.keys())).upper()
        hint = word_dict[word]
        logger.debug(f"Selected random word: {word} (Category: {category})")
        return word, hint

    def get_daily_word(self):
        """Uses a deterministic seed based on current date to pick the same word for everyone."""
        today_str = datetime.date.today().strftime("%Y%m%d")
        seed = int(today_str)
        rng = random.Random(seed)
        
        # Flatten all categories to get a large pool
        all_words = {}
        for words in self.categories.values():
            all_words.update(words)
            
        word = rng.choice(sorted(list(all_words.keys()))).upper()
        hint = all_words[word]
        logger.info(f"Daily challenge word for {today_str} generated.")
        return word, hint

    def get_available_categories(self):
        return list(self.categories.keys())

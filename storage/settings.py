import json
import os
import shutil
from logging_config import logger

SETTINGS_FILE = os.path.join("data", "settings.json")

DEFAULT_SETTINGS = {
    "theme": "dark",
    "sound_enabled": True,
    "animations_enabled": True,
    "keyboard_input_enabled": True,
    "last_difficulty": "Medium",
    "window_width": 1000,
    "window_height": 700,
    "window_x": None,
    "window_y": None,
    "is_maximized": False,
    "is_fullscreen": False
}

class SettingsManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SettingsManager, cls).__new__(cls)
            cls._instance._settings = {}
            cls._instance.load()
        return cls._instance

    def load(self):
        if not os.path.exists("data"):
            os.makedirs("data")
            
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._settings = {**DEFAULT_SETTINGS, **data}
                logger.info("Settings loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load settings: {e}")
                self._settings = DEFAULT_SETTINGS.copy()
        else:
            self._settings = DEFAULT_SETTINGS.copy()
            self.save()

    def save(self):
        try:
            if not os.path.exists("data"):
                os.makedirs("data")
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self._settings, f, indent=4)
            logger.info("Settings saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")

    def get(self, key):
        return self._settings.get(key, DEFAULT_SETTINGS.get(key))

    def set(self, key, value):
        if key in DEFAULT_SETTINGS:
            self._settings[key] = value
            self.save()
            logger.debug(f"Setting '{key}' updated to {value}")

    def export_settings(self, filepath):
        try:
            shutil.copy2(SETTINGS_FILE, filepath)
            logger.info(f"Settings exported to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to export settings: {e}")
            return False

    def import_settings(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self._settings = {**DEFAULT_SETTINGS, **data}
            self.save()
            logger.info(f"Settings imported from {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to import settings: {e}")
            return False

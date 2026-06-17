# HangmanX

HangmanX is a modern, feature-rich desktop implementation of the classic Hangman game built using Python and PyQt6. It aims to elevate the traditional pen-and-paper experience through dynamic visualizations, rich analytics, comprehensive tracking systems, and an extensively customizable interface.

## Table of Contents

1. [Features](#features)
2. [Architecture Overview](#architecture-overview)
3. [Folder Structure](#folder-structure)
4. [Core Mechanics and Modules](#core-mechanics-and-modules)
5. [Installation and Setup](#installation-and-setup)
6. [Usage](#usage)
7. [Dependencies](#dependencies)

---

## Features

- **Multiple Game Modes**: 
  - **Standard**: Classic gameplay pulling random words from various predefined categories.
  - **Daily Challenge**: A globally synchronized daily word driven by a time-seeded randomizer.
  - **Custom**: Allows local multiplayer where one user inputs a custom word for the other to guess.
- **Dynamic Difficulty Scaling**: Choose between Easy (8 attempts), Medium (7 attempts), and Hard (6 attempts). The procedural hangman drawing engine dynamically adjusts its rendering sequence based on the selected difficulty.
- **Advanced Statistics and Analytics**: Integration with Matplotlib to render interactive pie charts (Win/Loss ratios), bar graphs (Difficulty Usage), and line charts (Score Progression) to visualize player metrics over time.
- **Achievement System**: A background tracking system that monitors streaks, perfect games, and conditions to award achievements seamlessly.
- **Modern UI/UX**: 
  - A sleek, monochrome Dark Mode and a bright Light Mode, toggleable at runtime.
  - Custom UI widgets including Toast notifications and Confetti particle animations upon victory.
- **Persistent Storage**: All settings, statistics, and unlocked achievements are serialized securely in local JSON data stores.

---

## Architecture Overview

The application follows a strictly decoupled architecture, separating the core game logic (the "Engine") from the presentation layer (the "UI"). 

- **Presentation Layer (`ui/`)**: Built entirely in PyQt6. It utilizes a `QStackedWidget` managed by the `MainWindow` to navigate between isolated page components (Home, Game, Stats, Settings).
- **Core Engine (`game/`)**: Pure Python logic handling state machines, word generation, score tallies, and validation. It maintains zero dependencies on PyQt6, ensuring it can be tested or ported independently.
- **Storage Layer (`storage/`)**: Singleton managers responsible for disk I/O, safely reading and writing state arrays to local JSON stores.

---

## Folder Structure

The project is structured logically by domain:

```text
.
├── main.py                   # Application entry point; initializes Qt and error handling
├── logging_config.py         # Configures rotating file loggers and console outputs
├── requirements.txt          # Python dependency list
├── .gitignore                # Source control exclusions
├── assets/
│   ├── icons/                # SVG assets for UI (themes, arrows, UI elements)
│   └── sounds/               # Audio files for game events (win, loss, correct, incorrect)
├── data/                     # Generated at runtime: Persistent JSON stores
│   ├── settings.json
│   ├── statistics.json
│   └── achievements.json
├── game/                     # Core logic and engine components
│   ├── hangman_engine.py     # Main state machine and guess evaluator
│   ├── word_manager.py       # Handles word dictionaries and daily seed logic
│   ├── score_manager.py      # Computes streaks, completion bonuses, and hint costs
│   ├── achievement_manager.py# Validates post-game conditions for badges
│   └── session_manager.py    # Tracks temporary session durations and metrics
├── logs/                     # Generated at runtime: Contains rotating log files
│   └── hangmanx.log
├── storage/                  # Disk I/O management
│   ├── settings.py           # SettingsManager singleton
│   └── statistics.py         # StatisticsManager singleton (CSV export logic)
├── styles/                   # Aesthetic definitions
│   └── style_constants.py    # Centralized color palettes and font definitions
└── ui/                       # Presentation layer
    ├── main_window.py        # Main window, routing, and global stylesheet application
    ├── home_page.py          # Entry view, mode selection, and category selection
    ├── game_page.py          # Core gameplay loop view
    ├── stats_page.py         # Matplotlib integration for data visualization
    ├── settings_page.py      # User configuration view
    ├── summary_page.py       # Post-game results view
    ├── about_page.py         # Application meta-information
    └── widgets/              # Reusable customized UI elements
        ├── hangman_canvas.py # Procedural QPainter canvas for the gallows
        ├── toast.py          # Non-blocking notification popups
        └── confetti.py       # Victory animation renderer
```

---

## Core Mechanics and Modules

### The Hangman Engine
Located in `game/hangman_engine.py`, the engine operates as a state machine (`playing`, `won`, `lost`). It validates incoming characters, manages the guessed letters set, and determines transitions based on the `max_attempts` governed by the chosen difficulty configuration. 

### Procedural Canvas Rendering
`ui/widgets/hangman_canvas.py` bypasses static images in favor of procedural drawing via `QPainter`. It calculates geometric offsets dynamically based on window size. Crucially, it reads the `max_attempts` from the engine to adjust how the avatar is built (e.g., drawing both eyes simultaneously on the final attempt in Medium mode, versus individually in Easy mode).

### Data Persistence
The `SettingsManager`, `StatisticsManager`, and `AchievementManager` utilize the Singleton pattern to ensure that disk reads/writes are centralized. They automatically deploy default schemas if local files are missing, making first-time setup invisible to the user.

### Logging Subsystem
To ensure robustness, `logging_config.py` overrides the standard output to funnel critical events, state transitions, and unhandled exceptions into a rotating log file with a 5MB limit. This provides a detailed audit trail for debugging without consuming excessive disk space.

---

## Installation and Setup

1. **Clone the repository or extract the source code** to your local machine.
2. **Ensure Python 3.9+ is installed.**
3. **Create a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   ```
4. **Activate the virtual environment:**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
6. **Launch the application:**
   ```bash
   python main.py
   ```

---

## Usage

- **Navigation**: Use the Home screen to configure your next match. Select your Mode, Category, and Difficulty, then click Play Game.
- **Gameplay**: You can guess letters either by clicking the on-screen buttons (if implemented) or by typing directly on your physical keyboard.
- **Hints**: You are allocated one hint per game (if permitted by the difficulty setting). Using a hint deducts points from your potential score.
- **Statistics**: Visit the Statistics page to view your historical performance. You can also export this data to a CSV file for external analysis.
- **Theming**: Toggle between Light and Dark mode instantly using the moon/sun icon in the top right corner of the application.

---

## Dependencies

The application relies on the following major libraries:
- **PyQt6**: The core framework for window management, layouts, event handling, and 2D drawing (`QPainter`).
- **Matplotlib**: Utilized exclusively on the Statistics page for rendering complex data visualizations.
- **Standard Library Modules**: Extensively uses `json`, `os`, `csv`, `random`, `logging`, and `datetime` to avoid unnecessary external dependencies.

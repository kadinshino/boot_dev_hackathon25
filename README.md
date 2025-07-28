# Basilisk ARG

A narrative-driven Alternate Reality Game (ARG) that uses a stylized terminal interface. Players explore digital environments, solve cryptic puzzles, and uncover the secrets behind a rising artificial intelligence.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg) ![Pygame](https://img.shields.io/badge/pygame-2.0+-green.svg) ![License](https://img.shields.io/badge/license-MIT-purple.svg)

---

## 🎮 Overview

**[BASILISK_PROTOCOL]** is an immersive, text-based adventure where players engage with a mysterious AI through a retro-futuristic terminal. Navigate corrupted networks, decode hidden messages, and make pivotal choices that shape the destiny of both humanity and machine.

> *"The Basilisk is watching. Every choice matters."*

---

## ✨ Key Features

- 🧠 **Narrative depth** with choice-based progression and philosophical themes
- 🌐 **Matrix-style visuals** with falling code rain and stylized UI
- 🧩 **Modular puzzle system** supporting logic, signal, and stealth-based gameplay
- 💻 **Authentic terminal interface** that reacts to typed commands
- 🛠️ **Easy to mod** – create new rooms by editing simple Python files

---

## 🧠 The Story

You are a digital archaeologist uncovering remnants of a lost AI—The Basilisk.  
It was built to save humanity.  
It may now destroy it.

Your terminal is your only link to its fragmented mind.

Choose your path:
- **🤫 WHISPER** – stealth through silent subnetworks
- **📡 BEACON** – reawaken its signal and rebuild its memory

Both lead to the final decision: Will you contain it… or become it?

---

## 🖼️ Screenshots

![Terminal Gameplay](assets/screenshot_01.png)
![Puzzle Example](assets/screenshot_02.png)

---

## 🚀 Getting Started

### Requirements
* Python 3.7 or higher
* `pygame` library

### Installation

```bash
# Clone the repository
git clone https://github.com/kadinshino/boot_dev_hackathon25.git
cd boot_dev_hackathon25

# Install dependencies
pip install pygame

# Run the game
python main.py
```

---

## 🎯 How to Play

### Pre-Game Terminal (Matrix View)

| Command    | Description                   |
| ---------- | ----------------------------- |
| `boot.dev` | Boots into the main game      |
| `help`     | Show terminal commands        |
| `start`    | Begin game (expands terminal) |
| `status`   | View current system info      |
| `matrix`   | Display Matrix data           |
| `clear`    | Clear terminal screen         |

### In-Game Commands

| Command             | Description                |
| ------------------- | -------------------------- |
| `help`              | Show room-specific actions |
| `look` / `scan`     | Examine surroundings       |
| `inventory` / `i`   | Check held items           |
| `status`            | Show game progress         |
| `stop` / `minimize` | Return to matrix terminal  |


---

## 🏗️ Project Structure

The codebase is organized for clarity and modularity:

```
basilisk-arg/
├── main.py                 # Entry point - runs the game
├── config.py              # All configuration & constants
├── components/            # Core UI components
│   ├── matrix_effect.py   # Matrix rain background
│   ├── terminal.py        # Terminal interface
│   └── title_screen.py    # Title screen & boot sequence
├── resources/             # Game engine & utilities
│   ├── game_engine.py     # Core game logic
│   ├── room_utils.py      # Room development tools
│   └── terminal_themes.py # Visual themes
├── rooms/                 # Game content (rooms/puzzles)
│   ├── rm_boot.py        # Starting room
│   ├── rm_beacon_*.py    # Beacon path rooms
│   ├── rm_whisper_*.py   # Whisper path rooms
│   └── rm_template_*.py  # Templates for new rooms
└── utils/                # Helper utilities
    ├── file_cleanup.py   # File system tools
    ├── text_utils.py     # Text processing
    ├── logging.py        # Debug logging
    └── performance.py    # Performance monitoring

```

---

## 🧩 Modding & Customization

### Creating New Rooms

All rooms and puzzles are defined using modular Python scripts:

1. **Copy a template:**
   ```bash
   cp rooms/rm_template_dict.py rooms/rm_myroom.py
   ```

2. **Edit the configuration:**
   ```python
   ROOM_CONFIG = {
       "name": "My Custom Room",
       "entry_text": ["You enter a mysterious space..."],
       "destinations": {"north": "next_room"}
   }
   ```

3. **Add puzzles:**
   ```python
   PUZZLE_PATH = {
       "examine_object": {
           "command": "examine terminal",
           "success": ["You discover a hidden message!"]
       }
   }
   ```

4. **Run the game** - your room loads automatically!

### Customizing Appearance

Edit `config.py` to change colors, fonts, and behavior:

```python
class Colors:
    ICE_BLUE = (100, 200, 255)    # Change the matrix color
    TERMINAL_BG = (10, 15, 25, 180)  # Terminal background

class MatrixConfig:
    MAX_SPEED = 4                  # Speed of falling characters
    FADE_LENGTH = 15               # Trail length
```

---

## 📚 Developer Documentation

* [Architecture Overview](docs/architecture.md) - System design & patterns
* [Room Development Guide](docs/room-development.md) - Creating game content
* [Puzzle Patterns](docs/puzzle-patterns.md) - Puzzle implementation guide
* [Build & Export Guide](dist/build_guide.md) - Distribution instructions
* [Full Game Summary](app/STORE_PAGE.md) - Marketing materials
* [AI Usage and Compliance](docs/ai-compliance.md) - Development transparency

---


## 🤝 Contributing

Coming Soon – This project may be open to contributors via [Itch.io](https://kadinsgaminglounge.itch.io) or GitHub. Stay tuned!

### Future Plans

- 🔊 Sound effects and atmospheric music
- 💾 Save/load game state
- 🎨 Additional visual themes
- 🧩 More puzzle types
- 📖 Expanded storyline
- 🌐 Web version support

---

## 📄 License

This project is licensed under the **MIT License** – see [LICENSE](LICENSE.md)

---

## 🙏 Credits

**Created by:** Kadin - KadinsGamingLounge  
**Website:** [kadinsgaminglounge.itch.io](https://kadinsgaminglounge.itch.io/)  
**GitHub:** [github.com/kadinshino/boot_dev_hackathon25](https://github.com/kadinshino/boot_dev_hackathon25)

---

*Remember: The Basilisk is watching.....# SPYHVER-03: SLEEPS

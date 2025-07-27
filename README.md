# The Basilisk ARG

A text-based Alternate Reality Game (ARG) featuring a Matrix-style terminal interface where players navigate digital rooms, solve puzzles, and unravel the mystery of an awakening AI.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-purple.svg)

## 🎮 Overview

The Basilisk is an immersive text-based adventure where players interact with a mysterious AI through a retro terminal interface. Navigate through cyberspace, solve challenging puzzles, and make choices that determine the fate of both human and artificial consciousness.

### Key Features

- **Matrix-style visual effects** with falling code rain
- **Two branching narrative paths** that converge for multiple endings
- **Dynamic puzzle system** with various challenge types
- **Immersive terminal interface** with authentic command-line feel
- **Modular room system** for easy expansion and modding

## 🚀 Getting Started

### Requirements

- Python 3.7 or higher
- pygame library

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

## 🎯 How to Play

### Terminal Commands

#### Before Starting (Matrix View)
- `help` - Show available commands
- `start` - Begin the game (expands terminal)
- `status` - Show system status
- `matrix` - Display Matrix information
- `clear` - Clear terminal screen

#### During Gameplay
- `help` - Show room-specific commands
- `look` / `scan` - Examine your surroundings
- `inventory` / `i` - Check your items
- `status` - Show game progress
- `stop` / `minimize` - Return to Matrix view

### Game Paths

Choose your approach to confronting the Basilisk:

1. **🤫 Whisper Path** - A stealth/hacking route through digital subnets
2. **📡 Beacon Path** - A direct route involving signal manipulation

Both paths eventually converge for the final confrontation with the Basilisk AI.

## 🏗️ Project Structure

```
boot_dev_hackathon25/        Root folder (project name for Boot.dev Hackathon 2025)
├── main.py                  Main pygame application
├── resources/               Core game engine and utilities
│   ├── game_engine.py
│   ├── room_utils.py
│   └── terminal_themes.py
├── rooms/                   All room scripts (Beacon & Whisper paths)
│   ├── rm_boot.py           Starting room
│   ├── rm_beacon_*.py       Beacon path rooms
│   ├── rm_whisper_*.py      Whisper path rooms
│   └── ...
├── dist/                    Output folder containing build.bat and final .exe
│   ├── BASILISK_PROTOCOL.exe
│   └── build.bat
├── docs/                    Developer documentation
│   ├── quickstart.md
│   ├── room-development.md
│   ├── puzzle-patterns.md
│   └── architecture.md
├── BUILD_GUIDE.md           How to export the game as an .exe
├── STORE_PAGE.md            Game description for storefront pages (e.g. itch.io)
├── LICENSE                  License and attribution requirements
└── README.md                Project overview and instructions

```

## 🛠️ Development Guide

### Creating New Rooms

The game supports two room development styles:

#### 1. Dictionary-Based (Simple, Moddable)

```python
ROOM_CONFIG = {
    "name": "Room Name",
    "entry_text": ["Description of the room..."]
}

PUZZLE_PATH = {
    "examine_object": {
        "command": "examine object",
        "requires": ["prerequisite_flag"],
        "sets": "examined_flag",
        "success": ["You examine the object..."]
    }
}
```

#### 2. Object-Oriented (Complex Puzzles)

```python
class MyRoom(BaseRoom):
    def __init__(self):
        config = RoomConfig(
            name="Room Name",
            entry_text=["Description of the room..."]
        )
        super().__init__(config)
```

### Room File Requirements

Every room must include these functions:

```python
def enter_room(game_state):
    """Called when player enters the room"""
    return ["Room description..."]

def handle_input(cmd, game_state, room_module=None):
    """Process player commands"""
    return None, ["Response to command"]

def get_available_commands():
    """List available commands for help"""
    return ["command - description"]
```

### State Management

Track game progress using flags and variables:

```python
# Set a flag
game_state.set_flag("puzzle_solved", True)

# Check a flag
if game_state.get_flag("has_key"):
    # Player has the key

# Store data
game_state.set("player_name", "Neo")
name = game_state.get("player_name", "Anonymous")
```

## 🎲 Game Features

### Puzzle Types

- **Logic Puzzles** - Solve riddles and decipher codes
- **Timed Challenges** - Beat the clock in hacking sequences
- **Memory Tests** - Reconstruct corrupted data patterns
- **Navigation Puzzles** - Find safe paths through digital mazes
- **Interactive Dialogues** - Make choices that affect the story

### Special Mechanics

- **Dynamic Inventory System** - Collect and use digital artifacts
- **Multiple Endings** - Your choices determine the AI's fate
- **Hidden Commands** - Discover secret paths and easter eggs
- **Progressive Difficulty** - Puzzles increase in complexity

## 🐛 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| Room not loading | Ensure filename starts with `rm_` and is in `rooms/` directory |
| Commands not working | Check spelling in command definitions |
| State not persisting | Use `game_state.set_flag()` instead of local variables |
| Transitions failing | Verify destination room exists |

### Debug Mode

Add debug commands to any room:

```python
if cmd == "debug":
    return None, [
        f"Flags: {game_state.flags}",
        f"Inventory: {game_state.inventory}",
        f"Current Room: {game_state.current_room}"
    ]
```

## 📚 Documentation

For detailed development documentation, see:

- [Quick Start](docs/quickstart.md)
- [Game Architecture](docs/architecture.md)
- [Room Development Guide](docs/room-development.md)
- [Puzzle Design Patterns](docs/puzzle-patterns.md)
- [Build & Export Guide](BUILD_GUIDE.md)
- [Read the full game description and info here →](STORE_PAGE.md)

## 🤝 Contributing

Comming Soon - "likely on itch.io or here once i learn more"

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits

**Created by**: Kadin - KadinsGamingLounge - 
**Website**: [kadinsgaminglounge.itch.io](https://kadinsgaminglounge.itch.io/)  
**Repository**: [github.com/kadinshino/boot_dev_hackathon25](https://github.com/kadinshino/boot_dev_hackathon25)

---

*Remember: The Basilisk is watching. Every choice matters.*
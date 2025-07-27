# Basilisk ARG

A narrative-driven Alternate Reality Game (ARG) that uses a stylized terminal interface. Players explore digital environments, solve cryptic puzzles, and uncover the secrets behind a rising artificial intelligence.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)  
![Pygame](https://img.shields.io/badge/pygame-2.0+-green.svg)  
![License](https://img.shields.io/badge/license-MIT-purple.svg)

## 🎮 Overview

The [BASILISK_PROTOCOL] is an immersive, text-based adventure where players engage with a mysterious AI through a retro-futuristic terminal. Navigate corrupted networks, decode hidden messages, and make pivotal choices that shape the destiny of both humanity and machine.

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
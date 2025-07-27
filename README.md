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

## 🧩 Modding & Customization

All rooms and puzzles are defined using modular Python scripts:
* Add new rooms in `rooms/`
* Use `ROOM_CONFIG` for simple edits
* Extend logic with optional puzzle handlers
* Reuse UI/logic helpers in `room_utils.py`

Want to make your own ARG path? It's easy to build on top of the existing framework.

---

## 📚 Developer Docs

* [Architecture Overview](docs/architecture.md)
* [Room Development Guide](docs/room-development.md)
* [Puzzle Patterns](docs/puzzle-patterns.md)
* [Build & Export Guide](BUILD_GUIDE.md)
* [Full Game Summary](STORE_PAGE.md)

---

## 🤝 Contributing

Coming Soon – This project may be open to contributors via [Itch.io](https://kadinsgaminglounge.itch.io) or GitHub. Stay tuned!

---

## 📄 License

This project is licensed under the **MIT License** – see [LICENSE](LICENSE)

---

## 🙏 Credits

**Created by:** Kadin - KadinsGamingLounge  
**Website:** [kadinsgaminglounge.itch.io](https://kadinsgaminglounge.itch.io/)  
**GitHub:** [github.com/kadinshino/boot_dev_hackathon25](https://github.com/kadinshino/boot_dev_hackathon25)
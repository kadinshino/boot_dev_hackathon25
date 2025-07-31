# Architecture Overview

## Design Philosophy

The Basilisk ARG is built with two core principles in mind: **accessibility for modders** and **professional code organization**. Drawing from my experience with GameMaker Language (GML), I've created a Python-based architecture that feels familiar to game developers while remaining approachable for ARG fans who want to create their own content.

## Project Structure

```
├── LICENSE.md
├── README.md
├── app
│   └── __init__.py
├── components
│   ├── __init__.py
│   ├── data_rain_effect.py
│   ├── terminal.py
│   └── title_screen.py
├── developer_tools
│   ├── debug_tools
│   │   ├── index.py
│   │   ├── logging.py
│   │   └── performance.py
│   ├── dev_tool_notes.md
│   ├── game_compiler
│   │   ├── distribution_notes.md
│   │   ├── requirements.txt
│   │   └── windows_builder
│   │       ├── build.bat
│   │       └── build_guide.md
│   ├── spyher_tools
│   │   ├── build_spyhver.py
│   │   ├── encode_spyhver.py
│   │   ├── extract_spyhver.sh
│   │   ├── structure_spyhver.py
│   │   └── test script.py
│   └── store_assets
│       ├── STORE_PAGE.md
│       ├── screenshot_01.png
│       └── screenshot_02.png
├── docs
│   ├── ai-compliance.md
│   ├── architecture.md
│   ├── puzzle-patterns.md
│   └── room-development.md
├── main.py
├── resources
│   ├── __init__.py
│   └── game_engine.py
├── rooms
│   ├── __init__.py
│   ├── beacons_oop
│   │   ├── __init__.py
│   │   ├── rm_beacon_1.py
│   │   ├── rm_beacon_2.py
│   │   ├── rm_beacon_3.py
│   │   ├── rm_beacon_4.py
│   │   ├── rm_beacon_5.py
│   │   └── rm_beacon_convergence.py
│   ├── customs_args
│   │   ├── __init__.py
│   │   ├── rm_custom_entry.py
│   │   ├── rm_template_dict_demo.py
│   │   └── rm_template_oop_demo.py
│   ├── rm_boot_entry.py
│   └── whispers_dict
│       ├── __init__.py
│       ├── rm_whisper_1.py
│       ├── rm_whisper_2.py
│       ├── rm_whisper_3.py
│       ├── rm_whisper_4.py
│       ├── rm_whisper_5.py
│       └── rm_whisper_awaken.py
└── utils
    ├── .gitignore
    ├── __init__.py
    ├── file_cleanup.py
    ├── game_config.py
    ├── room_utils.py
    └── text_utils.py
```

## Quick Start for Content Creators

**You only need to focus on the `rooms/` folder!** Everything else is the engine that makes your rooms work.

### What Each Folder Does

#### 🎮 `rooms/` - Where the Magic Happens
This is where ALL game content lives. Each `.py` file is a self-contained room with its own puzzles, story, and logic. 

**To create content:**
1. Copy `rm_template_dict.py` or `rm_template_oop.py`
2. Rename it to `rm_yourroom.py`
3. Edit the content
4. Drop it in the `rooms/` folder
5. It automatically appears in the game!

**Example rooms:**
- `rm_boot.py` - The starting room where players begin
- `rm_beacon_1.py`, `rm_beacon_2.py` - Rooms along the "beacon" story path
- `rm_whisper_1.py`, `rm_whisper_2.py` - Rooms along the "whisper" story path

#### 📚 `resources/` - Your Toolkit
Contains the tools you'll use when creating rooms:
- `room_utils.py` - **IMPORTANT!** Contains all the helper functions for room creation:
  - `BaseRoom` - Base class for object-oriented rooms
  - `transition_to_room()` - Move players between rooms
  - `process_puzzle_command()` - Handle puzzle logic
  - `standard_commands()` - Built-in commands like "help" and "inventory"
- `game_engine.py` - The core engine (you won't modify this)
- `terminal_themes.py` - Visual customization options

#### ⚙️ Core Folders (Ignore These)
- `main.py` - Starts the game
- `config.py` - Game settings and constants
- `components/` - UI components (matrix effect, terminal display)
- `utils/` - Internal helper functions

## Why Two Development Styles?

### Dictionary-Based Rooms: For the Community

```python
ROOM_CONFIG = {
    "name": "Digital Archive",
    "entry_text": ["You enter a vast digital archive."]
}

PUZZLE_PATH = {
    "examine_terminal": {
        "command": "examine terminal",
        "success": ["The terminal flickers to life."]
    }
}
```

**Why I built this:**
- **Zero barrier to entry** - Anyone who can edit a text file can create rooms
- **Self-documenting** - The structure explains itself
- **ARG tradition** - Many ARGs thrive on community-created content
- **Rapid prototyping** - Test ideas without learning complex systems

### Object-Oriented Rooms: For Complex Mechanics

```python
class DigitalArchive(BaseRoom):
    def __init__(self):
        config = RoomConfig(
            name="Digital Archive",
            entry_text=["You enter a vast digital archive."]
        )
        super().__init__(config)
```

**Why I built this:**
- **Clean code organization** - Encapsulation and inheritance for complex puzzles
- **Reusable components** - Base classes for common room types
- **State management** - Easier to handle complex game states
- **Professional structure** - Maintainable for long-term development

## Module Loading System

My dynamic loading system automatically discovers and loads rooms:

```python
# Automatic discovery - just drop a file in rooms/
for file in os.listdir("rooms/"):
    if file.startswith("rm_") and file.endswith(".py"):
        # Automatically available in game
```

This means:
- **No registration required** - Drop in a file and it works
- **Hot-swappable** - Add/remove rooms without recompiling
- **Conflict-free** - Rooms don't interfere with each other
- **Community friendly** - Share a single `.py` file to add content

## For Modders: What You Need to Know

### 1. Start Here
- Open the `rooms/` folder
- Copy `rm_template_dict.py` (easier) or `rm_template_oop.py` (more powerful)
- Follow the extensive comments in the template

### 2. Use the Tools
The `room_utils.py` file provides everything you need:
```python
from resources.room_utils import (
    format_enter_lines,      # Format room entry text
    standard_commands,       # Handle common commands
    transition_to_room,      # Move to another room
    process_puzzle_command   # Process puzzle logic
)
```

### 3. Test Your Room
```bash
# Run the game
python main.py

# In game, type:
start  # Enter game mode

# Your room loads automatically!
```

### 4. Share Your Creation
Just share your `rm_*.py` file. Other players drop it in their `rooms/` folder and it works!

## Best Practices for Room Creation

1. **Use Clear Names**: `rm_puzzle_vault.py` not `rm_pv.py`
2. **Comment Your Code**: Others might want to learn from your puzzles
3. **Test Thoroughly**: Make sure players can't get stuck
4. **Be Creative**: The engine supports complex puzzles and storytelling
5. **Have Fun**: This is about community creativity!

## Example: Creating Your First Room

```python
# rooms/rm_my_first_room.py
from resources.room_utils import format_enter_lines, standard_commands, transition_to_room

ROOM_CONFIG = {
    "name": "My First Room",
    "entry_text": [
        "You've created your first room!",
        "A door leads north."
    ]
}

def enter_room(game_state):
    return format_enter_lines(ROOM_CONFIG["name"], ROOM_CONFIG["entry_text"])

def handle_input(cmd, game_state, room_module=None):
    if cmd.lower() == "go north":
        return transition_to_room("next_room", ["You walk through the door..."])
    
    # Handle standard commands
    result = standard_commands(cmd, game_state)
    if result:
        return None, result
    
    return None, ["Unknown command. Try 'go north'"]

def get_available_commands():
    return ["go north - proceed to the next room"]
```

That's it! Save this file in `rooms/` and it's playable immediately.

## Conclusion

The Basilisk ARG's architecture is designed to let you focus on what matters: **creating amazing content**. The engine handles all the complex stuff - you just write rooms and puzzles. Whether you're crafting a simple story room or a complex puzzle chamber, the tools are here to support your creativity.

Remember: **You only need the `rooms/` folder and `room_utils.py` to create content.** Everything else just makes it work.

*The architecture is watching. Every room matters.*

### SPYHVER-19: SHARDS.

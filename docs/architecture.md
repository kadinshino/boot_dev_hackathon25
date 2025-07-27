
---

````markdown
# Architecture Overview

## Design Philosophy

The Basilisk ARG is built on two core principles: **accessibility for modders** and **professional code organization**. Inspired by development patterns from GameMaker Language (GML), the goal was to create a Python-based system that feels familiar to game developers while remaining approachable for ARG fans who want to build their own content.

---

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
````

**Why this exists:**

* **Zero barrier to entry** – Anyone who can edit a text file can build content
* **Self-documenting** – The structure is readable and easy to modify
* **ARG tradition** – Community-driven content is central to ARGs
* **Rapid prototyping** – Test rooms without writing Python classes

This mirrors classic modding formats, where players could extend games using config-style files.

---

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

**Why this exists:**

* **Clean structure** – Encapsulation and inheritance for advanced logic
* **Reusable code** – Shared behavior across rooms
* **Better state handling** – Supports complex progression
* **Long-term maintainability** – Ideal for structured development

---

## 🏗️ Project Directory Layout

*An overview of the folder structure for `boot_dev_hackathon25`*

```
boot_dev_hackathon25/        Root folder (Boot.dev Hackathon 2025 project)
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
├── dist/                    Output folder for builds
│   ├── BASILISK_PROTOCOL.exe
│   └── build.bat
├── docs/                    Developer documentation
│   ├── quickstart.md
│   ├── room-development.md
│   ├── puzzle-patterns.md
│   └── architecture.md
├── BUILD_GUIDE.md           Instructions for exporting the game
├── STORE_PAGE.md            Game description for storefronts (e.g. itch.io)
├── LICENSE                  License and attribution information
└── README.md                General project overview
```

---

## GameMaker Heritage

Coming from GameMaker development, we carried over familiar design patterns.

### Room-Based Architecture

```
GameMaker:                     Python Equivalent:
├── Rooms/                     ├── rooms/
│   ├── rm_start              │   ├── rm_start.py
│   ├── rm_level_1            │   ├── rm_level_1.py
│   └── rm_boss               │   └── rm_boss.py
```

Just like GameMaker’s system, each room in Basilisk is:

* **Self-contained** – All logic in one file
* **Independently loadable** – Can be added/removed freely
* **Event-driven** – Responds to user input like GML events

---

### Event System Translation

| **GML Event**   | **Python Equivalent**                     |
| --------------- | ----------------------------------------- |
| Create Event    | `def __init__(self)`                      |
| Step Event      | `def update(self, game_state)`            |
| Key Press Event | `def handle_input(self, cmd, game_state)` |
| Draw Event      | `def get_display_text(self, game_state)`  |
| Room Start      | `def enter_room(self, game_state)`        |
| Room End        | `def exit_room(self, game_state)`         |

---

### State Management Pattern

```python
# GML: global.player_health = 100
# Python: game_state.set("player_health", 100)

# GML: if (instance_exists(obj_key)) 
# Python: if "key" in game_state.inventory:

# GML: room_goto(rm_next)
# Python: transition_to_room("rm_next", ["Leaving..."])
```

---

## Modular Design

### Core System (Protected)

```
resources/
├── game_engine.py      # Core engine (stable)
├── room_utils.py       # Base classes and utilities
└── terminal_themes.py  # Theme configurations
```

### Content Layer (Moddable)

```
rooms/
├── rm_*.py             # Official room scripts
├── custom_*.py         # Community-created rooms
└── mod_*.py            # Player modifications
```

This structure ensures:

* **Core stability** – Engine files stay untouched
* **Easy sharing** – Modders can share one `.py` file
* **Safe experimentation** – Mods don’t break the system
* **Cross-version compatibility** – Mods survive updates

---

## Module Loading System

Inspired by GameMaker’s dynamic resource tree, Basilisk uses auto-discovery:

```python
# Automatically load any room that starts with "rm_"
for file in os.listdir("rooms/"):
    if file.startswith("rm_") and file.endswith(".py"):
        # Load and register
```

**Benefits:**

* No need to register rooms manually
* Add/remove content without restarts
* Rooms remain sandboxed and conflict-free

---

## Why This Architecture?

### 🧩 Lowering the Barrier

* Writers and puzzle designers can create without programming
* Community-created content is encouraged
* No custom tools required — just a text editor

### 🧠 Professional Foundation

* OOP-based rooms enable advanced puzzle structures
* Shared logic via base classes (e.g. `BaseRoom`, `PuzzleCommand`)
* Cleaner long-term maintenance

### 🧪 Familiar Patterns

GameMaker developers will recognize:

* Room-based flow
* Event-driven input
* Global state model
* Asset-like file structure

### 🧰 Best of Both Worlds

* Beginners can start with dictionary rooms
* Devs can build OOP-based rooms
* Both styles work together in the same project

---

## Example: From GML to Python

### GameMaker

```gml
// Room Creation Code
global.terminal_active = false;
instance_create_layer(x, y, "Instances", obj_terminal);

// Step Event
if (keyboard_check_pressed(vk_space)) {
    if (distance_to_object(obj_player) < 32) {
        global.terminal_active = true;
        show_message("Terminal activated!");
    }
}
```

---

### Python – Dictionary Room

```python
PUZZLE_PATH = {
    "activate_terminal": {
        "command": "activate terminal",
        "sets": "terminal_active",
        "success": ["Terminal activated!"]
    }
}
```

---

### Python – OOP Room

```python
class TerminalRoom(BaseRoom):
    def _setup_puzzles(self):
        self.processor.add_command(
            PuzzleCommand(
                command="activate terminal",
                sets="terminal_active", 
                success=["Terminal activated!"]
            )
        )
```

---

## Performance Considerations

### Text-Based Advantages

No sprite rendering or collision detection means we focus on:

```python
# Basilisk Performance Priorities:
- Text parsing
- String operations
- Dynamic imports
- Flag lookups
```

---

### Lazy Room Loading

```python
# Only load room module if needed
def load_room(room_name):
    if room_name not in loaded_rooms:
        module = importlib.import_module(f"rooms.rm_{room_name}")
        loaded_rooms[room_name] = module
    return loaded_rooms[room_name]
```

* First load: \~5–10ms
* Re-entry (cached): <1ms
* Memory per room: \~1–2KB

---

### Unloading Distant Rooms

Rooms persist in memory unless manually cleared. You can free memory with:

```python
def unload_distant_rooms(current_room, game_state):
    """Unload rooms more than 3 steps away (optional memory cleanup)."""
    for room_name in list(loaded_rooms.keys()):
        if get_distance(current_room, room_name) > 3:
            del loaded_rooms[room_name]
```

> This is an optional optimization — call it manually after room transitions if needed.

---

### Dictionary vs OOP Room Performance

| Operation          | Dictionary Room | OOP Room    | Notes                          |
| ------------------ | --------------- | ----------- | ------------------------------ |
| Load Time          | \~5ms           | \~8ms       | OOP has instantiation overhead |
| Command Lookup     | O(n)            | O(1) w/ map | OOP enables faster dispatch    |
| Memory Usage       | \~1KB           | \~2KB       | Class objects have overhead    |
| Puzzle Flexibility | Linear          | High        | OOP allows advanced logic      |

---

## Optimization Tips

### For Dictionary Rooms

```python
# Sort common commands to the top
PUZZLE_PATH = {
    "look": {...},
    "examine": {...},
    "rare_action": {...}
}

# Use early returns
def handle_input(cmd, game_state):
    if cmd in ["look", "l"]:
        return quick_look_response()
    return process_puzzle_command(cmd, game_state, PUZZLE_PATH)
```

---

### For OOP Rooms

```python
class OptimizedRoom(BaseRoom):
    def __init__(self):
        super().__init__(config)
        self.patterns = {
            "use_item": re.compile(r"^use (\w+) on (\w+)$"),
            "combine": re.compile(r"^combine (\w+) with (\w+)$")
        }
        self._command_map = self._build_command_map()

    def _build_command_map(self):
        return {
            "look": self._handle_look,
            "examine": self._handle_examine
        }
```

---

## Conclusion

This architecture bridges:

* **Amateur creativity** and **professional engineering**
* **Simple configuration** and **powerful abstraction**
* **GameMaker traditions** and **Pythonic design**
* **Individual rooms** and **cohesive ARG experiences**

By supporting both dictionary and OOP room styles, *The Basilisk ARG* welcomes creators of all skill levels. Writers, puzzle designers, and developers can contribute meaningfully to a shared world, with tools that match their comfort zone.

> *The architecture is watching. Every room matters.*

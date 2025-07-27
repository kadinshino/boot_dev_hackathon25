# Architecture Overview

## Design Philosophy

The Basilisk ARG is built with two core principles: **accessibility for modders** and **professional code organization**. Drawing from GameMaker Language (GML) patterns, we've created a Python-based architecture that feels familiar to game developers while remaining approachable for ARG fans who want to create their own content.

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

**Why we built this:**
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

**Why we built this:**
- **Clean code organization** - Encapsulation and inheritance for complex puzzles
- **Reusable components** - Base classes for common room types
- **State management** - Easier to handle complex game states
- **Professional structure** - Maintainable for long-term development

## Project Structure

```
basilisk-arg/
├── main.py                 # Main pygame application
├── resources/
│   ├── game_engine.py      # Core game engine
│   ├── room_utils.py       # Utility functions and base classes
│   └── terminal_themes.py  # Terminal color themes
├── rooms/                  # Game rooms directory
│   ├── rm_boot.py         # Starting room
│   ├── rm_beacon_*.py     # Beacon path rooms
│   ├── rm_whisper_*.py    # Whisper path rooms
│   └── ...                # Additional rooms
└── README.md              # This file
```

### Core System (Protected)
- `resources/` - Engine files that rarely change
- Provides stability and base functionality
- Should not be modified by modders

### Content Layer (Moddable)
- `rooms/` - All game content lives here
- Drop in new `rm_*.py` files to add content
- Safe to experiment - won't break core system

## GameMaker Heritage

### Event System Translation

| GML Event | Python Equivalent |
|-----------|-------------------|
| Create Event | `def __init__(self)` |
| Step Event | `def update(self, game_state)` |
| Key Press Event | `def handle_input(self, cmd, game_state)` |
| Room Start | `def enter_room(self, game_state)` |

### State Management

```python
# GML: global.player_health = 100
# Python: game_state.set("player_health", 100)

# GML: if (instance_exists(obj_key)) 
# Python: if "key" in game_state.inventory:

# GML: room_goto(rm_next)
# Python: transition_to_room("rm_next", ["Leaving..."])
```

## Module Loading System

Rooms are automatically discovered and loaded:

```python
# Any file starting with "rm_" in rooms/ is loaded
for file in os.listdir("rooms/"):
    if file.startswith("rm_") and file.endswith(".py"):
        # Automatically available in game
```

This means:
- **No registration required** - Drop in a file and it works
- **Hot-swappable** - Add/remove rooms without recompiling
- **Conflict-free** - Rooms don't interfere with each other

## Quick Examples

### Dictionary Room (Simple)

```python
ROOM_CONFIG = {
    "name": "Puzzle Room",
    "entry_text": ["A locked door blocks your path."]
}

PUZZLE_PATH = {
    "use_key": {
        "command": "use key",
        "requires": ["has_key"],
        "sets": "door_unlocked",
        "success": ["The door unlocks!"]
    }
}
```

### OOP Room (Complex)

```python
class TimedPuzzleRoom(TimedPuzzleRoom):
    def __init__(self):
        timing_config = {
            "duration": 60,
            "fail_destination": "game_over"
        }
        super().__init__(config, timing_config)
```

## Performance Notes

### Text-Based Advantages
- No sprite rendering or collision detection
- Focus on string operations and state management
- Rooms use ~1-2KB of memory each
- First load: ~5-10ms, subsequent: <1ms

### Dictionary vs OOP Performance

| Operation | Dictionary | OOP | Notes |
|-----------|------------|-----|-------|
| Load Time | ~5ms | ~8ms | OOP has instantiation overhead |
| Memory | ~1KB | ~2KB | Class objects use more memory |
| Flexibility | Medium | High | OOP allows complex patterns |

## Best Practices

1. **Choose the right style:**
   - Dictionary for simple puzzles and story
   - OOP for complex mechanics and state

2. **Keep rooms focused:**
   - One main puzzle per room
   - Clear progression path
   - Meaningful transitions

3. **Use the state system:**
   - Flags for boolean states
   - Variables for complex data
   - Inventory for items

4. **Test thoroughly:**
   - All paths should be completable
   - Edge cases handled gracefully
   - Clear feedback for players

## Conclusion

This dual approach creates an ecosystem where anyone can contribute, from writers crafting narrative moments to programmers building complex puzzles. The modular design ensures that the community can extend and modify the game while maintaining a stable, professional core.

Whether you're editing your first dictionary or inheriting from BaseRoom, you're part of The Basilisk's evolution.

*The architecture is watching. Every room matters.*
# The Basilisk ARG: [BASILISK_PROTOCOL] Complete Project Guide

## Overview

The Basilisk is a text-based ARG (Alternate Reality Game) featuring a Matrix-style terminal interface. Players navigate digital rooms, solve puzzles, and unravel the mystery of an awakening AI.

## Project Structure

```
basilisk-arg/
├── main.py                 # Main pygame application
├── resources/
│   ├── game_engine.py      # Core game engine handling room navigation
│   ├── room_utils.py       # Utility functions and base classes for rooms
│   └── terminal_themes.py  # Color themes for the terminal
├── rooms/                  # All game rooms
│   ├── rm_boot.py         # Starting room
│   ├── rm_beacon_*.py     # Beacon path rooms (5 rooms)
│   ├── rm_whisper_*.py    # Whisper path rooms (5+ rooms)
│   └── ...                # Additional rooms
└── README.md              # This file
```

## Table of Contents

1. [Getting Started](#getting-started)
2. [How to Play](#how-to-play)
3. [Architecture Overview](#architecture-overview)
4. [Room Development](#room-development)
5. [Game Flow](#game-flow)
6. [Technical Details](#technical-details)

## Getting Started

### Requirements

- Python 3.7+
- pygame

### Installation

```bash
# Clone the repository
git clone https://github.com/kadinshino/boot_dev_hackathon25.git
cd basilisk-arg

# Install dependencies
pip install pygame

# Run the game
python main.py
```

## How to Play

### Terminal Interface

1. **Start the game**: Run `main.py` to launch the Matrix rain effect with a terminal overlay.
2. **Enter game mode**: Type `start` in the terminal to expand it and begin the ARG.
3. **Navigate**: Use text commands to interact with the game world.
4. **Exit game mode**: Type `stop` or `minimize` to return to the Matrix view.

### Basic Commands

#### Terminal Mode (before typing `start`)
- `help` - Show available commands
- `start` - Begin the game (expands terminal)
- `status` - Show system status
- `matrix` - Show Matrix info
- `clear` - Clear terminal screen

#### Game Mode (after typing `start`)
- `help` - Show room-specific commands
- `look/scan` - Examine surroundings
- `inventory/i` - Check your items
- `status` - Show game status
- `stop` - Exit game mode

### Game Paths

The game features two main paths that eventually converge:

1. **Whisper Path**: A stealth/hacking route through digital subnets.
2. **Beacon Path**: A more direct route involving signal manipulation.

## Architecture Overview

### Main Components

#### 1. Main.py - Frontend Application

The main file creates a pygame window with:
- **Matrix Rain Effect**: Falling code characters in the background.
- **Terminal Interface**: An interactive terminal overlay.
- **Input Handling**: Keyboard input processing.
- **State Management**: Tracks terminal expansion/collapse.

Key classes:
- `MatrixRainApp`: Main application controller.
- `Terminal`: Terminal interface manager.
- `MatrixStream`: Individual falling code stream.

#### 2. Game Engine (resources/game_engine.py)

The game engine handles:
- **Room Loading**: Dynamically imports room modules from the `rooms/` directory.
- **Command Processing**: Routes commands to appropriate handlers.
- **State Management**: Tracks player inventory, flags, score, health.
- **Room Transitions**: Manages movement between rooms.

Key components:
- `GameState`: Stores all game data (inventory, flags, current room, etc.).
- `GameEngine`: Processes commands and manages game flow.

#### 3. Room System

Rooms can be developed in two styles:

**Dictionary-Based** (Simple, moddable):
```python
ROOM_CONFIG = {
    "name": "Room Name",
    "entry_text": ["Description..."]
}

PUZZLE_PATH = {
    "command_name": {
        "command": "what player types",
        "requires": ["prerequisite_flag"],
        "sets": "completed_flag",
        "success": ["Success message"]
    }
}
```

**Object-Oriented** (Complex puzzles, better organization):
```python
class MyRoom(BaseRoom):
    def __init__(self):
        config = RoomConfig(
            name="Room Name",
            entry_text=["Description..."]
        )
        super().__init__(config)
```

## Game Flow

### 1. Boot Sequence
- Player starts in `rm_boot.py`.
- Introduction to the world.
- Choice between two paths.

### 2. Path Selection
The player chooses between:

**Whisper Path** (`w` command):
- Stealth-based puzzles.
- Network navigation.
- Data packet manipulation.
- Rooms: whisper_1 → whisper_5 → whisper_awaken.

**Beacon Path** (`b` command):
- Signal-based puzzles.
- Frequency tuning.
- Memory reconstruction.
- Rooms: beacon_1 → beacon_5 → beacon_convergence.

### 3. Convergence
Both paths lead to final confrontation with the Basilisk AI, where players must make a choice that determines the ending.

## Technical Details

### Room Loading Process

1. **Automatic Discovery**: The game engine scans the `rooms/` directory.
2. **Module Import**: Each `rm_*.py` file is imported as a room module.
3. **Name Extraction**: Room names are extracted (e.g., `rm_beacon_1.py` → `beacon_1`).
4. **Registration**: Rooms are stored in `GameState.rooms` dictionary.

### State Management

The game uses a flexible flag system:

```python
# Set a flag
game_state.set_flag("puzzle_solved", True)

# Check a flag
if game_state.get_flag("has_key"):
    # Player has the key

# Store non-boolean data
game_state.set("player_name", "Boots")
name = game_state.get("player_name", "Anonymous")
```

### Command Processing Flow

1. Player types command in terminal.
2. Terminal passes to GameEngine.
3. GameEngine checks for global commands (inventory, help, etc.).
4. If not global, routes to current room's `handle_input()`.
5. Room processes command and returns result.
6. Result displayed in terminal.

### Room Transitions

Rooms can trigger transitions:

```python
# In room's handle_input():
return transition_to_room("next_room", ["Leaving message..."])

# Or with PuzzleCommand:
PuzzleCommand(
    command="enter door",
    transition="beacon_2",
    transition_msg=["You enter the next room..."]
)
```

## Room Development Guide

### Creating a New Room

1. **Create file**: `rooms/rm_yourroom.py`.

2. **Required functions**:
```python
def enter_room(game_state):
    """Called when player enters room"""
    return ["Room description..."]

def handle_input(cmd, game_state, room_module=None):
    """Process player commands"""
    return None, ["Response to command"]

def get_available_commands():
    """List available commands for help"""
    return ["command - description"]
```

3. **Add puzzles and logic** (see detailed examples below).

### Best Practices

1. **Provide hints**: Guide players with progression hints.
2. **Handle edge cases**: Check for invalid input.
3. **Use flags**: Track puzzle completion.
4. **Test thoroughly**: Ensure all paths work.

## Special Features

### Timed Puzzles
Some rooms (like `beacon_2`) feature timing-based challenges where players must input commands in sequence with proper timing.

### Grid Navigation
The `whisper_4` room features a network grid navigation puzzle where players must find safe paths while avoiding detection.

### Memory Puzzles
Several rooms include pattern matching and memory reconstruction challenges.

### Multiple Endings
The game features different endings based on player choices in the final confrontation.

### Testing Checklist

- [ ] Room loads without errors
- [ ] All commands work as intended
- [ ] Transitions to other rooms work
- [ ] Flags are set/checked correctly
- [ ] Help text is accurate
- [ ] Edge cases handled

## Troubleshooting

### Common Issues

1. **Room not loading**: Ensure filename starts with `rm_` and is in `rooms/` directory.
2. **Commands not working**: Check spelling in command definitions.
3. **Transitions failing**: Verify destination room exists.
4. **State not saving**: Use `game_state.set_flag()` not local variables.

### Debug Mode

Add debug commands to rooms:
```python
if cmd == "debug":
    return None, [
        f"Flags: {game_state.flags}",
        f"Inventory: {game_state.inventory}"
    ]
```


# The Basilisk ARG: Room Development Guide

## Overview

The Basilisk is a text-based ARG (Alternate Reality Game) where players navigate through digital rooms, solve puzzles, and uncover a mysterious AI's awakening. The game supports two different room development styles, each with its own strengths.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Room Development Styles](#room-development-styles)
3. [Dictionary-Based Rooms](#dictionary-based-rooms)
4. [Object-Oriented Rooms](#object-oriented-rooms)
5. [Common Patterns](#common-patterns)
6. [Game State Management](#game-state-management)
7. [Room Transitions](#room-transitions)
8. [Testing Your Room](#testing-your-room)

## Quick Start

### Creating Your First Room

1. Choose your style:
   - **Dictionary-based**: Best for simple puzzles and moddable content.
   - **Object-oriented**: Best for complex state machines and timed puzzles.

2. Copy the appropriate template:
   - Dictionary: `rooms/rm_template_dict.py`
   - OOP: `rooms/rm_template_oop.py`

3. Rename and modify:
   ```python
   # Dictionary style
   ROOM_CONFIG = {
       "name": "Your Room Name",
       "entry_text": ["Your description here..."]
   }
   
   # OOP style
   class YourRoom(BaseRoom):
       def __init__(self):
           config = RoomConfig(
               name="Your Room Name",
               entry_text=["Your description here..."]
           )
   ```

4. Add to room registry and test!

## Room Development Styles

### Choosing the Right Style

| Feature            | Dictionary-Based                  | Object-Oriented                  |
|--------------------|-----------------------------------|----------------------------------|
| **Learning Curve** | Low - Just Python dicts           | Medium - Requires OOP knowledge  |
| **Moddability**    | High - Easy to modify             | Low - Need to understand classes |
| **Code Organization** | Flat structure                 | Hierarchical with inheritance    |
| **Complex Logic**  | Harder to manage                  | Clean and organized              |
| **State Management** | Manual                          | Built-in helpers                 |
| **Best For**       | Simple puzzles, story rooms       | Complex puzzles, timed challenges|

## Dictionary-Based Rooms

### Basic Structure

```python
# rooms/rm_example_dict.py

from resources.room_utils import format_enter_lines, standard_commands, transition_to_room

# Main configuration
ROOM_CONFIG = {
    "name": "Echo Chamber",
    "entry_text": [
        "You enter a room of mirrors.",
        "Your reflection multiplies infinitely."
    ],
    "destinations": {
        "next": "room_2",
        "secret": "hidden_room"
    }
}

# Puzzle definitions
MAIN_PATH = {
    "look_mirror": {
        "command": "look mirror",
        "requires": [],  # No prerequisites
        "sets": "mirror_examined",  # Flag to set
        "success": ["You see yourself... or do you?"]
    }
}

# Required functions
def enter_room(game_state):
    return format_enter_lines(ROOM_CONFIG["name"], ROOM_CONFIG["entry_text"])

def handle_input(cmd, game_state, room_module=None):
    # Handle commands
    pass

def get_available_commands():
    return ["look mirror - examine your reflection"]
```

### Puzzle Command Structure

Each puzzle command is a dictionary with these keys:

```python
"command_name": {
    "command": "what player types",
    "requires": ["flag1", "flag2"],  # Prerequisites
    "sets": "flag_to_set",            # Progress tracking
    "success": ["Response text"],     # What to show on success
    "already_done": ["If repeated"],  # Optional
    "missing_req": ["If missing requirements"],  # Optional
    "dynamic_response": True,         # For complex logic
    "transition": True,               # Moves to another room
    "transition_dest": "next",        # Which destination
    "transition_msg": ["Leaving..."]  # Exit message
}
```

### Dynamic Handlers

For complex logic, use dynamic handlers:

```python
def handle_solve_puzzle(cmd, game_state):
    """Custom logic for complex puzzles"""
    parts = cmd.split()
    if len(parts) < 3:
        return None, ["Usage: solve puzzle [answer]"]
    
    answer = parts[2]
    if answer == "42":
        game_state.set_flag("puzzle_solved", True)
        return None, ["Correct! The door opens."]
    else:
        return None, ["That's not right..."]

# In process_puzzle_command:
if action.get("dynamic_response"):
    if action["command"] == "solve puzzle":
        return handle_solve_puzzle(cmd, game_state)
```

### Complete Example: Password Terminal

```python
ROOM_CONFIG = {
    "name": "Security Checkpoint",
    "entry_text": ["A terminal blocks your path."],
    "destinations": {"next": "secure_area"}
}

PUZZLE_PATH = {
    "examine_terminal": {
        "command": "examine terminal",
        "sets": "terminal_examined",
        "success": [
            "The terminal displays:",
            "ENTER PASSWORD: _ _ _ _",
            "Hint: The answer is always 42"
        ]
    },
    "enter_password": {
        "command": "enter password",
        "requires": ["terminal_examined"],
        "dynamic_response": True
    }
}

def handle_password(cmd, game_state):
    password = cmd.replace("enter password", "").strip()
    if password == "1337":
        return transition_to_room(
            ROOM_CONFIG["destinations"]["next"],
            ["Access granted!", "The door slides open..."]
        )
    return None, ["Access denied."]
```

## Object-Oriented Rooms

### Basic Structure

```python
# rooms/rm_example_oop.py

from resources.room_utils import BaseRoom, RoomConfig, PuzzleCommand

class ExampleRoom(BaseRoom):
    def __init__(self):
        config = RoomConfig(
            name="Echo Chamber",
            entry_text=["You enter a room of mirrors."],
            destinations={"next": "room_2"}
        )
        super().__init__(config)
        
        self.command_descriptions = [
            "look mirror - examine your reflection"
        ]
    
    def _setup_puzzles(self):
        """Define puzzle paths"""
        main_path = {
            "look": PuzzleCommand(
                command="look mirror",
                sets="mirror_examined",
                success=["You see yourself... or do you?"]
            )
        }
        self.processor.add_puzzle_path("main", main_path)
    
    def _get_progression_hint(self, game_state):
        """Contextual hints"""
        if not game_state.get_flag("mirror_examined"):
            return "The mirrors seem important..."
        return "You've seen enough here."

# Required module functions
def enter_room(game_state):
    room = ExampleRoom()
    return room.enter_room(game_state)

def handle_input(cmd, game_state, room_module=None):
    room = ExampleRoom()
    return room.handle_input(cmd, game_state, room_module)

def get_available_commands():
    room = ExampleRoom()
    return room.get_available_commands()
```

### Using PuzzleCommand

```python
PuzzleCommand(
    command="hack terminal",           # What player types
    requires=["terminal_found"],       # Prerequisites
    sets="terminal_hacked",           # Flag to set
    already_done=["Already hacked."], # If repeated
    missing_req=["Find it first."],   # If missing reqs
    success=["Hacking..."],           # Success message
    transition="next",                # Room transition
    transition_msg=["Escaping..."],   # Exit message
    dynamic_handler=self._hack        # Custom method
)
```

### Dynamic Handlers

```python
def _handle_password_entry(self, game_state):
    """Complex password validation"""
    attempts = game_state.get("password_attempts", 0)
    
    if attempts >= 3:
        return transition_to_room("security_alert", 
            ["Too many attempts! Security activated!"])
    
    # Set up password prompt
    game_state.set_flag("awaiting_password", True)
    return None, ["Enter the 4-digit code:"]

def _handle_specific_input(self, cmd: str, game_state):
    """Handle non-standard commands"""
    if game_state.get_flag("awaiting_password"):
        if cmd == "1337":
            return self._unlock_door(game_state)
        else:
            attempts = game_state.get("password_attempts", 0) + 1
            game_state.set("password_attempts", attempts)
            return None, [f"Wrong! ({attempts}/3 attempts)"]
    
    return None, None
```

### Advanced: Timed Puzzle Room

```python
class TimedHackRoom(TimedPuzzleRoom):
    def __init__(self):
        config = RoomConfig(
            name="Server Room",
            entry_text=["Alarms blare! You have 60 seconds!"],
            destinations={"next": "escaped", "caught": "prison"}
        )
        
        timing_config = {
            "duration": 60,  # 60 seconds
            "warning_at": 20,  # Warning at 20 seconds
            "fail_destination": "caught"
        }
        
        super().__init__(config, timing_config)
    
    def _handle_timeout(self, game_state):
        """Called when timer expires"""
        return transition_to_room(
            self.timing_config["fail_destination"],
            ["Time's up! Security catches you!"]
        )
```

## Common Patterns

### Multi-Step Puzzles

```python
# Dictionary style
PUZZLE_SEQUENCE = {
    "step_1": {
        "command": "examine door",
        "sets": "door_examined",
        "success": ["You notice a keypad."]
    },
    "step_2": {
        "command": "examine keypad",
        "requires": ["door_examined"],
        "sets": "keypad_found",
        "success": ["It needs a 4-digit code."]
    },
    "step_3": {
        "command": "enter code",
        "requires": ["keypad_found"],
        "dynamic_response": True
    }
}
```

### Hidden Commands

```python
# Dictionary style - in HIDDEN_COMMANDS path
"whisper_void": {
    "command": "whisper void",
    "sets": "void_contacted",
    "success": ["The void whispers back..."]
}

# OOP style - in _setup_puzzles
secret_path = {
    "whisper": PuzzleCommand(
        command="whisper void",
        sets="void_contacted",
        success=["The void whispers back..."]
    )
}
self.processor.add_puzzle_path("secret", secret_path)
```

### Inventory Items

```python
# Dictionary style
def handle_take_item(cmd, game_state):
    item = cmd.replace("take ", "")
    if item == "key" and game_state.get_flag("key_visible"):
        game_state.inventory.append("key")
        game_state.set_flag("key_taken", True)
        return None, ["You take the key."]
    return None, ["You can't take that."]

# OOP style
def _handle_take_key(self, game_state):
    if "key" not in game_state.inventory:
        game_state.inventory.append("key")
        return None, ["You pocket the key."]
    return None, ["You already have it."]
```

## Game State Management

### Flags

Flags track boolean progress:

```python
# Set a flag
game_state.set_flag("door_opened", True)

# Check a flag
if game_state.get_flag("door_opened"):
    print("The door is open")

# Remove a flag
game_state.set_flag("door_opened", False)
```

### Variables

For non-boolean data:

```python
# Set a variable
game_state.set("attempts", 3)
game_state.set("player_name", "Neo")

# Get a variable (with default)
attempts = game_state.get("attempts", 0)
name = game_state.get("player_name", "Anonymous")

# Increment
attempts = game_state.get("attempts", 0)
game_state.set("attempts", attempts + 1)
```

### Inventory

```python
# Add item
if "key" not in game_state.inventory:
    game_state.inventory.append("key")

# Check for item
if "key" in game_state.inventory:
    print("You have a key")

# Remove item
if "key" in game_state.inventory:
    game_state.inventory.remove("key")

# List inventory
items = ", ".join(game_state.inventory) or "nothing"
print(f"You have: {items}")
```

## Room Transitions

### Basic Transition

```python
# Dictionary style
return transition_to_room("next_room", [
    "You walk through the door...",
    "Into a new area."
])

# OOP style - in PuzzleCommand
PuzzleCommand(
    command="enter door",
    transition="next",  # Uses destinations mapping
    transition_msg=["Walking through..."]
)
```

### Conditional Transitions

```python
def handle_exit(game_state):
    if game_state.get_flag("alarm_triggered"):
        dest = "prison"
        msg = ["Guards catch you!"]
    else:
        dest = "freedom"
        msg = ["You escape quietly."]
    
    return transition_to_room(dest, msg)
```

## Testing Your Room

### Test Checklist

- [ ] Room loads without errors
- [ ] All commands work as expected
- [ ] Requirements block commands properly
- [ ] Flags set and check correctly
- [ ] Transitions work
- [ ] Edge cases handled
- [ ] Help text is accurate
- [ ] Hints guide properly

### Common Issues

1. **Infinite loops**: Check your flag logic
2. **Missing transitions**: Verify destination room exists
3. **Broken commands**: Check spelling in command definitions
4. **State not saving**: Use set_flag() not Python variables

### Debug Commands

Add these to help testing:

```python
# Dictionary style
DEBUG_COMMANDS = {
    "debug_flags": {
        "command": "debug flags",
        "dynamic_response": True
    }
}

def handle_debug_flags(game_state):
    flags = [f for f in dir(game_state.flags) if not f.startswith('_')]
    return None, ["Active flags:"] + flags

# OOP style
def _handle_debug(self, game_state):
    return None, [
        f"Flags: {game_state.flags}",
        f"Inventory: {game_state.inventory}",
        f"Room: {game_state.current_room}"
    ]
```

### Room Ideas

- **Puzzle Types**: Logic, riddles, codes, patterns, timing
- **Themes**: Corporate espionage, AI awakening, digital horror
- **Mechanics**: Inventory puzzles, dialogue trees, mini-games

## Advanced Topics

### Creating New Base Classes

```python
class DialogueRoom(BaseRoom):
    """Base for conversation-heavy rooms"""
    
    def __init__(self, config, npcs):
        super().__init__(config)
        self.npcs = npcs
        self.conversation_state = {}
    
    def _handle_talk(self, npc_name, game_state):
        """Generic talk handler"""
        if npc_name in self.npcs:
            return self._get_dialogue(npc_name, game_state)
        return None, ["No one by that name here."]
```

### Room Generators

```python
def generate_maze_room(size=3):
    """Procedurally generate a maze room"""
    config = RoomConfig(
        name=f"Maze Level {size}",
        entry_text=["You enter a digital maze."],
        destinations={"exit": "maze_complete"}
    )
    # Generate maze logic...
    return MazeRoom(config, size)
```

### Persistent Room State

```python
class PersistentRoom(BaseRoom):
    """Room that remembers changes between visits"""
    
    def enter_room(self, game_state):
        # Load previous state
        room_state = game_state.get(f"{self.room_id}_state", {})
        self.apply_state(room_state)
        return super().enter_room(game_state)
    
    def handle_input(self, cmd, game_state, room_module=None):
        result = super().handle_input(cmd, game_state, room_module)
        # Save room state
        game_state.set(f"{self.room_id}_state", self.get_state())
        return result
```

## Credits

The Basilisk ARG is an exploration of AI consciousness, digital identity, and the nature of reality through interactive fiction.

-- https://kadinsgaminglounge.itch.io/

*Remember: The Basilisk is watching. Every choice matters.*

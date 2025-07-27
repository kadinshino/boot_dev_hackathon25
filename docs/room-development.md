# Room Development Guide

A comprehensive guide to creating rooms for The Basilisk ARG.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Room Architecture](#room-architecture)
3. [Development Styles](#development-styles)
4. [Dictionary-Based Rooms](#dictionary-based-rooms)
5. [Object-Oriented Rooms](#object-oriented-rooms)
6. [Puzzle Design](#puzzle-design)
7. [State Management](#state-management)
8. [Room Transitions](#room-transitions)
9. [Advanced Techniques](#advanced-techniques)
10. [Testing & Debugging](#testing--debugging)
11. [Best Practices](#best-practices)
12. [Example Rooms](#example-rooms)

## Quick Start

### Creating Your First Room

1. **Create a new file** in the `rooms/` directory:
   ```
   rooms/rm_yourroom.py
   ```

2. **Choose a development style**:
   - **Dictionary-based**: Simple puzzles, easy to modify
   - **Object-oriented**: Complex logic, better organization

3. **Copy the appropriate template**:
   ```bash
   # For dictionary style
   cp rooms/rm_template_dict.py rooms/rm_yourroom.py
   
   # For OOP style
   cp rooms/rm_template_oop.py rooms/rm_yourroom.py
   ```

4. **Implement required functions**:
   ```python
   def enter_room(game_state)
   def handle_input(cmd, game_state, room_module=None)
   def get_available_commands()
   ```

## Room Architecture

### How Rooms Work

1. **Discovery**: Game engine scans `rooms/` directory for `rm_*.py` files
2. **Loading**: Each room module is dynamically imported
3. **Registration**: Rooms are stored in `GameState.rooms` dictionary
4. **Navigation**: Players move between rooms using transitions

### Required Components

Every room module MUST export these three functions:

```python
def enter_room(game_state):
    """
    Called when player enters the room.
    Returns: List of strings to display
    """
    pass

def handle_input(cmd, game_state, room_module=None):
    """
    Process player commands.
    Returns: (new_room, response_lines) tuple
    """
    pass

def get_available_commands():
    """
    List commands for the help system.
    Returns: List of command descriptions
    """
    pass
```

## Development Styles

### Comparison Table

| Feature | Dictionary-Based | Object-Oriented |
|---------|------------------|-----------------|
| **Learning Curve** | Low | Medium |
| **Code Organization** | Flat structure | Hierarchical |
| **Complex Logic** | Harder to manage | Clean and organized |
| **State Management** | Manual | Built-in helpers |
| **Inheritance** | Not available | Full OOP support |
| **Best For** | Simple puzzles, story rooms | Complex puzzles, mini-games |

## Dictionary-Based Rooms

### Basic Template

```python
from resources.room_utils import format_enter_lines, standard_commands, transition_to_room

# Room configuration
ROOM_CONFIG = {
    "name": "Digital Archive",
    "entry_text": [
        "You enter a vast digital archive.",
        "Countless data streams flow around you."
    ],
    "destinations": {
        "north": "data_core",
        "south": "entrance_hall"
    }
}

# Main puzzle path
PUZZLE_PATH = {
    "scan_archive": {
        "command": "scan archive",
        "requires": [],
        "sets": "archive_scanned",
        "success": [
            "Scanning the archive reveals:",
            "- Corrupted memory fragments",
            "- A hidden terminal"
        ]
    },
    "access_terminal": {
        "command": "access terminal",
        "requires": ["archive_scanned"],
        "sets": "terminal_accessed",
        "success": ["The terminal boots up..."],
        "already_done": ["The terminal is already active."],
        "missing_req": ["You haven't found a terminal yet."]
    }
}

# Required functions
def enter_room(game_state):
    return format_enter_lines(ROOM_CONFIG["name"], ROOM_CONFIG["entry_text"])

def handle_input(cmd, game_state, room_module=None):
    # Check standard commands
    result = standard_commands(cmd, game_state)
    if result:
        return None, result
    
    # Process puzzle commands
    for puzzle_path in [PUZZLE_PATH]:
        result = process_puzzle_command(cmd, game_state, puzzle_path)
        if result:
            return result
    
    return None, ["Command not recognized."]

def get_available_commands():
    return [
        "scan archive - examine the data streams",
        "access terminal - use the hidden terminal"
    ]
```

### Puzzle Command Structure

```python
"puzzle_name": {
    # Required fields
    "command": "what player types",
    "success": ["Success message"],
    
    # Optional fields
    "requires": ["flag1", "flag2"],      # Prerequisites
    "sets": "flag_name",                  # Flag to set on success
    "already_done": ["Repeat message"],   # If already completed
    "missing_req": ["Missing message"],   # If missing prerequisites
    
    # Advanced options
    "dynamic_response": True,             # Use custom handler
    "transition": True,                   # Move to another room
    "transition_dest": "north",           # Which destination
    "transition_msg": ["Exit message"]    # Transition text
}
```

### Dynamic Response Handlers

For complex puzzle logic:

```python
def handle_password_puzzle(cmd, game_state):
    """Custom handler for password input"""
    parts = cmd.split()
    if len(parts) < 2:
        return None, ["Usage: enter [password]"]
    
    password = parts[1]
    attempts = game_state.get("password_attempts", 0)
    
    if password == "BASILISK":
        game_state.set_flag("password_correct", True)
        return transition_to_room("secret_room", 
            ["Access granted!", "A hidden door opens..."])
    else:
        attempts += 1
        game_state.set("password_attempts", attempts)
        if attempts >= 3:
            return transition_to_room("security_alert",
                ["Too many attempts!", "Security activated!"])
        return None, [f"Incorrect. ({attempts}/3 attempts)"]

# In your puzzle definition:
"enter_password": {
    "command": "enter",
    "dynamic_response": True
}

# In process_puzzle_command:
if action.get("dynamic_response"):
    if action["command"] == "enter":
        return handle_password_puzzle(cmd, game_state)
```

## Object-Oriented Rooms

### Basic Template

```python
from resources.room_utils import BaseRoom, RoomConfig, PuzzleCommand

class DigitalArchive(BaseRoom):
    def __init__(self):
        config = RoomConfig(
            name="Digital Archive",
            entry_text=[
                "You enter a vast digital archive.",
                "Countless data streams flow around you."
            ],
            destinations={
                "north": "data_core",
                "south": "entrance_hall"
            }
        )
        super().__init__(config)
        
        # Define available commands
        self.command_descriptions = [
            "scan archive - examine the data streams",
            "access terminal - use the hidden terminal"
        ]
    
    def _setup_puzzles(self):
        """Define puzzle paths"""
        main_path = {
            "scan": PuzzleCommand(
                command="scan archive",
                sets="archive_scanned",
                success=[
                    "Scanning reveals:",
                    "- Corrupted memory fragments",
                    "- A hidden terminal"
                ]
            ),
            "terminal": PuzzleCommand(
                command="access terminal",
                requires=["archive_scanned"],
                sets="terminal_accessed",
                success=["The terminal boots up..."],
                already_done=["Already active."],
                missing_req=["No terminal found."]
            )
        }
        self.processor.add_puzzle_path("main", main_path)
    
    def _get_progression_hint(self, game_state):
        """Provide contextual hints"""
        if not game_state.get_flag("archive_scanned"):
            return "The data streams seem worth examining..."
        elif not game_state.get_flag("terminal_accessed"):
            return "That terminal might be useful..."
        return "You've explored everything here."

# Module functions
def enter_room(game_state):
    room = DigitalArchive()
    return room.enter_room(game_state)

def handle_input(cmd, game_state, room_module=None):
    room = DigitalArchive()
    return room.handle_input(cmd, game_state, room_module)

def get_available_commands():
    room = DigitalArchive()
    return room.get_available_commands()
```

### PuzzleCommand Class

```python
PuzzleCommand(
    command="hack system",              # Player input
    requires=["terminal_active"],       # Prerequisites
    sets="system_hacked",              # Flag to set
    success=["Hacking successful!"],   # Success message
    already_done=["Already hacked."],  # Repeat message
    missing_req=["Need terminal."],    # Missing prereq message
    transition="next",                 # Room transition
    transition_msg=["Escaping..."],    # Exit message
    dynamic_handler=self._hack_system  # Custom method
)
```

### Custom Input Handling

```python
def _handle_specific_input(self, cmd: str, game_state):
    """Handle non-standard commands"""
    
    # Handle multi-word commands
    if cmd.startswith("decrypt "):
        file_name = cmd[8:]  # Remove "decrypt "
        return self._decrypt_file(file_name, game_state)
    
    # Handle state-dependent input
    if game_state.get_flag("awaiting_input"):
        return self._process_user_input(cmd, game_state)
    
    return None, None

def _decrypt_file(self, file_name: str, game_state):
    """Custom file decryption logic"""
    known_files = {
        "manifest.txt": "System manifest loaded.",
        "secrets.enc": "This file requires a key.",
        "backup.dat": "Backup data corrupted."
    }
    
    if file_name in known_files:
        return None, [known_files[file_name]]
    
    return None, ["File not found."]
```

## Puzzle Design

### Types of Puzzles

#### 1. Logic Puzzles
```python
"solve_riddle": {
    "command": "answer",
    "dynamic_response": True,
    "hint": "Think about binary..."
}

def handle_riddle(cmd, game_state):
    answer = cmd.replace("answer ", "").lower()
    if answer in ["10", "binary", "two"]:
        return None, ["Correct! The door opens."]
    return None, ["That's not right..."]
```

#### 2. Code/Password Puzzles
```python
class PasswordRoom(BaseRoom):
    def _setup_puzzles(self):
        # Clue reveals the pattern
        clue_path = {
            "read": PuzzleCommand(
                command="read note",
                success=["The note says: 'First four primes'"]
            )
        }
        
        # Password check
        main_path = {
            "enter": PuzzleCommand(
                command="enter code",
                dynamic_handler=self._check_code
            )
        }

    def _check_code(self, game_state):
        # Expecting "2357" (first four primes)
        if self.last_input == "enter code 2357":
            return self._unlock_door(game_state)
        return None, ["Access denied."]
```

#### 3. Sequence Puzzles
```python
SEQUENCE_PUZZLE = {
    "stage": 0,
    "sequence": ["red", "green", "blue", "yellow"],
    "player_sequence": []
}

def handle_color_input(color, game_state):
    puzzle = game_state.get("color_puzzle", SEQUENCE_PUZZLE.copy())
    expected = puzzle["sequence"][puzzle["stage"]]
    
    if color == expected:
        puzzle["stage"] += 1
        if puzzle["stage"] >= len(puzzle["sequence"]):
            return None, ["Sequence complete! Door unlocked."]
        return None, [f"Correct! Next color?"]
    else:
        puzzle["stage"] = 0
        return None, ["Wrong! Starting over..."]
```

#### 4. Timed Challenges
```python
class TimedHackRoom(TimedPuzzleRoom):
    def __init__(self):
        timing_config = {
            "duration": 30,
            "warning_at": 10,
            "fail_destination": "caught"
        }
        super().__init__(config, timing_config)
    
    def _handle_timeout(self, game_state):
        return transition_to_room("caught", 
            ["Time's up! Security catches you!"])
```

#### 5. Inventory Puzzles
```python
"use_keycard": {
    "command": "use keycard",
    "dynamic_response": True
}

def handle_keycard(cmd, game_state):
    if "keycard" not in game_state.inventory:
        return None, ["You don't have a keycard."]
    
    if game_state.get_flag("at_door"):
        game_state.inventory.remove("keycard")
        return transition_to_room("restricted_area",
            ["The keycard works! Access granted."])
    
    return None, ["Nothing to use it on here."]
```

## State Management

### Flags (Boolean States)

```python
# Setting flags
game_state.set_flag("door_unlocked", True)
game_state.set_flag("alarm_active", False)

# Checking flags
if game_state.get_flag("has_password"):
    print("You know the password")

# Multiple flag checks
flags_needed = ["has_key", "knows_code", "power_on"]
if all(game_state.get_flag(f) for f in flags_needed):
    print("All conditions met!")
```

### Variables (Non-Boolean Data)

```python
# Storing values
game_state.set("player_health", 100)
game_state.set("current_code", "1234")
game_state.set("npc_dialogue_state", "intro")

# Retrieving with defaults
health = game_state.get("player_health", 100)
attempts = game_state.get("hack_attempts", 0)

# Updating values
attempts = game_state.get("hack_attempts", 0)
game_state.set("hack_attempts", attempts + 1)
```

### Complex State Objects

```python
# Storing complex data
puzzle_state = {
    "grid": [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
    "player_pos": (1, 1),
    "moves": 0
}
game_state.set("maze_puzzle", puzzle_state)

# Updating complex state
maze = game_state.get("maze_puzzle")
maze["moves"] += 1
maze["player_pos"] = (2, 1)
game_state.set("maze_puzzle", maze)
```

### Inventory Management

```python
# Adding items
if "keycard" not in game_state.inventory:
    game_state.inventory.append("keycard")
    return None, ["You pick up the keycard."]

# Checking for items
if "flashlight" in game_state.inventory:
    return None, ["Your flashlight reveals a hidden door."]
else:
    return None, ["It's too dark to see."]

# Removing items
if "battery" in game_state.inventory:
    game_state.inventory.remove("battery")
    game_state.set_flag("flashlight_powered", True)
    return None, ["You insert the battery."]

# Listing inventory
items = game_state.inventory
if items:
    item_list = ", ".join(items)
    return None, [f"You have: {item_list}"]
else:
    return None, ["Your inventory is empty."]
```

## Room Transitions

### Basic Transitions

```python
# Simple transition
return transition_to_room("next_room", [
    "You walk through the doorway...",
    "...into a new area."
])

# Using destination mapping
destination = ROOM_CONFIG["destinations"]["north"]
return transition_to_room(destination, ["You head north."])
```

### Conditional Transitions

```python
def handle_exit_command(cmd, game_state):
    if game_state.get_flag("alarm_triggered"):
        return transition_to_room("prison", 
            ["Guards catch you as you try to leave!"])
    elif game_state.get_flag("disguised"):
        return transition_to_room("street", 
            ["You casually walk out, unnoticed."])
    else:
        return None, ["The exit is blocked by security."]
```

### Multi-Path Transitions

```python
ROOM_CONFIG = {
    "destinations": {
        "door1": "puzzle_room",
        "door2": "combat_room",
        "door3": "treasure_room",
        "secret": "hidden_passage"
    }
}

def handle_door_choice(door_num, game_state):
    if door_num == "1":
        return transition_to_room("puzzle_room", 
            ["You enter a room full of strange symbols."])
    elif door_num == "2":
        if "weapon" in game_state.inventory:
            return transition_to_room("combat_room",
                ["You ready your weapon and enter."])
        else:
            return None, ["You sense danger beyond this door."]
    elif door_num == "3":
        if game_state.get_flag("has_key"):
            return transition_to_room("treasure_room",
                ["Your key unlocks the door!"])
        else:
            return None, ["This door is locked."]
```

### Transition with State Changes

```python
def escape_with_data(game_state):
    # Add item before transition
    game_state.inventory.append("stolen_data")
    
    # Set flags
    game_state.set_flag("data_acquired", True)
    game_state.set_flag("mission_complete", True)
    
    # Increase score
    score = game_state.get("score", 0)
    game_state.set("score", score + 100)
    
    return transition_to_room("safehouse", [
        "You grab the data and make your escape!",
        "Score: +100 points"
    ])
```

## Advanced Techniques

### Creating Base Classes

```python
class PuzzleRoom(BaseRoom):
    """Base class for puzzle-heavy rooms"""
    
    def __init__(self, config, puzzle_config):
        super().__init__(config)
        self.puzzle_config = puzzle_config
        self.puzzle_state = {}
    
    def _check_puzzle_complete(self, game_state):
        """Override in subclasses"""
        raise NotImplementedError
    
    def _give_puzzle_hint(self, game_state):
        """Provide contextual hints"""
        attempts = game_state.get(f"{self.room_id}_attempts", 0)
        if attempts > 3:
            return "Hint: " + self.puzzle_config.get("hint", "Keep trying!")
        return None

class MathPuzzleRoom(PuzzleRoom):
    """Room with mathematical puzzles"""
    
    def _check_puzzle_complete(self, game_state):
        answer = game_state.get("current_answer")
        return answer == self.puzzle_config["solution"]
```

### State Machines

```python
class DialogueRoom(BaseRoom):
    """Room with complex NPC dialogue"""
    
    def __init__(self):
        super().__init__(config)
        self.dialogue_states = {
            "initial": {
                "text": "Hello, stranger.",
                "options": {
                    "greet": "friendly",
                    "threaten": "hostile",
                    "ignore": "ignored"
                }
            },
            "friendly": {
                "text": "Nice to meet you!",
                "options": {
                    "ask about basilisk": "basilisk_info",
                    "leave": "goodbye"
                }
            },
            "hostile": {
                "text": "Get out of here!",
                "transition": "thrown_out"
            }
        }
    
    def _handle_dialogue(self, choice, game_state):
        current = game_state.get("dialogue_state", "initial")
        state = self.dialogue_states[current]
        
        if choice in state.get("options", {}):
            next_state = state["options"][choice]
            game_state.set("dialogue_state", next_state)
            
            if "transition" in self.dialogue_states[next_state]:
                return transition_to_room(
                    self.dialogue_states[next_state]["transition"],
                    ["The conversation ends abruptly."]
                )
            
            return None, [self.dialogue_states[next_state]["text"]]
        
        return None, ["They don't understand."]
```

### Mini-Games

```python
class HackingMiniGame(BaseRoom):
    """Implement a hacking mini-game"""
    
    def __init__(self):
        super().__init__(config)
        self.grid_size = 5
        self.target_nodes = [(1,1), (3,3), (2,4)]
        
    def _setup_puzzles(self):
        main_path = {
            "start": PuzzleCommand(
                command="start hack",
                sets="hack_started",
                success=self._display_grid(game_state)
            ),
            "connect": PuzzleCommand(
                command="connect",
                requires=["hack_started"],
                dynamic_handler=self._handle_connection
            )
        }
    
    def _display_grid(self, game_state):
        """Show the hacking grid"""
        grid = []
        for y in range(self.grid_size):
            row = []
            for x in range(self.grid_size):
                if (x, y) in self.target_nodes:
                    row.append("[X]")
                else:
                    row.append("[ ]")
            grid.append(" ".join(row))
        
        return ["Hacking Grid:"] + grid + [
            "Connect all [X] nodes!",
            "Use: connect x1,y1 x2,y2"
        ]
    
    def _handle_connection(self, game_state):
        # Parse coordinates and validate connection
        # Update grid state
        # Check for victory condition
        pass
```

### Procedural Generation

```python
import random

class ProceduralMaze(BaseRoom):
    """Randomly generated maze room"""
    
    def __init__(self, difficulty=1):
        self.difficulty = difficulty
        self.size = 3 + (difficulty * 2)
        self.maze = self._generate_maze()
        
        config = RoomConfig(
            name=f"Digital Maze Level {difficulty}",
            entry_text=["You enter a shifting digital maze."]
        )
        super().__init__(config)
    
    def _generate_maze(self):
        """Generate random maze layout"""
        maze = []
        for y in range(self.size):
            row = []
            for x in range(self.size):
                # Random walls, ensure path exists
                if random.random() > 0.3:
                    row.append(0)  # Empty
                else:
                    row.append(1)  # Wall
            maze.append(row)
        
        # Ensure start and end are clear
        maze[0][0] = 0  # Start
        maze[-1][-1] = 2  # Exit
        
        return maze
```

## Testing & Debugging

### Debug Commands

Add debug commands to help with testing:

```python
DEBUG_COMMANDS = {
    "debug_flags": {
        "command": "debug flags",
        "dynamic_response": True
    },
    "debug_give": {
        "command": "debug give",
        "dynamic_response": True
    },
    "debug_solve": {
        "command": "debug solve",
        "dynamic_response": True
    }
}

def handle_debug(cmd, game_state):
    if not game_state.get_flag("debug_mode"):
        return None, ["Debug mode not enabled."]
    
    if cmd == "debug flags":
        flags = [k for k, v in game_state.flags.items() if v]
        return None, ["Active flags:"] + flags
    
    elif cmd.startswith("debug give "):
        item = cmd.replace("debug give ", "")
        game_state.inventory.append(item)
        return None, [f"Added {item} to inventory."]
    
    elif cmd == "debug solve":
        # Auto-solve current puzzle
        game_state.set_flag("puzzle_solved", True)
        return None, ["Puzzle solved via debug."]
    
    return None, ["Unknown debug command."]
```

### Testing Checklist

- [ ] **Room Loading**
  - Room file loads without errors
  - All imports are correct
  - Room appears in game

- [ ] **Basic Commands**
  - Help command lists all options
  - Look/scan provides room description
  - Standard commands work (inventory, status)

- [ ] **Puzzle Flow**
  - Puzzles require correct prerequisites
  - Flags set appropriately
  - Success/failure messages display correctly
  - Already completed messages work

- [ ] **Transitions**
  - All exits lead to valid rooms
  - Transition messages display
  - State persists across rooms

- [ ] **Edge Cases**
  - Invalid commands handled gracefully
  - Empty/null inputs don't crash
  - Inventory limits respected
  - State changes save properly

### Common Issues

| Problem | Solution |
|---------|----------|
| ImportError | Check imports and file paths |
| KeyError | Verify dictionary keys exist |
| AttributeError | Ensure methods/attributes defined |
| Transitions fail | Check room names match exactly |
| Flags not saving | Use game_state methods, not local vars |
| Commands not recognized | Check exact command strings |

### Logging

Add logging for debugging:

```python
import logging

logger = logging.getLogger(__name__)

def handle_input(cmd, game_state, room_module=None):
    logger.debug(f"Room {ROOM_CONFIG['name']}: Command '{cmd}'")
    logger.debug(f"Flags: {game_state.flags}")
    
    # Your logic here
    
    logger.debug(f"Response: {response}")
    return result
```

## Best Practices

### 1. Clear Command Naming
```python
# Good
"examine terminal"
"hack security system"
"use keycard on door"

# Avoid
"e term"
"h"
"use"
```

### 2. Helpful Error Messages
```python
# Good
"The door is locked. Maybe there's a key somewhere?"
"You need to power on the terminal first."

# Avoid
"You can't do that."
"Error."
```

### 3. Progressive Hints
```python
def _get_progression_hint(self, game_state):
    if not game_state.get_flag("found_terminal"):
        return "This room has more than meets the eye..."
    elif not game_state.get_flag("terminal_powered"):
        return "The terminal needs power."
    elif not game_state.get_flag("password_found"):
        return "Check the desk drawers carefully."
    return None
```

### 4. Consistent Theming
- Use cyberpunk/digital terminology
- Maintain atmosphere with descriptions
- Keep puzzle solutions logical within the world

### 5. Player Guidance
```python
# Provide clear feedback
if not game_state.get_flag("light_on"):
    return None, [
        "It's too dark to see anything.",
        "Maybe you should find a light source?"
    ]

# Confirm actions
if "keycard" in game_state.inventory:
    game_state.inventory.remove("keycard")
    return None, [
        "You swipe the keycard.",
        "The reader beeps and turns green.",
        "The door clicks open."
    ]
```

### 6. State Management
```python
# Always use game_state for persistence
game_state.set_flag("door_open", True)  # Good
self.door_open = True  # Bad - won't persist

# Provide defaults
attempts = game_state.get("attempts", 0)  # Good
attempts = game_state.get("attempts")  # Bad - might be None
```

## Example Rooms

### Simple Story Room
```python
# rooms/rm_story_intro.py
ROOM_CONFIG = {
    "name": "Digital Void",
    "entry_text": [
        "You float in an endless digital void.",
        "Streams of data flow past like stars.",
        "A voice echoes: 'Welcome, seeker...'"
    ]
}

STORY_PATH = {
    "listen": {
        "command": "listen",
        "sets": "heard_voice",
        "success": [
            "The voice continues:",
            "'The Basilisk stirs. Time is short.'",
            "'Follow the beacons or whisper to shadows.'"
        ]
    },
    "speak": {
        "command": "speak",
        "requires": ["heard_voice"],
        "transition": True,
        "transition_dest": "path_choice",
        "transition_msg": ["Your words ripple through the void..."]
    }
}
```

### Complex Puzzle Room
```python
# rooms/rm_cipher_lock.py
class CipherRoom(BaseRoom):
    def __init__(self):
        config = RoomConfig(
            name="Cipher Lock",
            entry_text=["A massive door with a cipher lock blocks your path."]
        )
        super().__init__(config)
        self.cipher = {"A": "Z", "B": "Y", "C": "X"}  # etc...
    
    def _setup_puzzles(self):
        hints = {
            "note": PuzzleCommand(
                command="read note",
                success=["The note says: 'YZTOMLP'"]
            )
        }
        
        main = {
            "decode": PuzzleCommand(
                command="decode",
                dynamic_handler=self._handle_decode
            )
        }
        
        self.processor.add_puzzle_path("hints", hints)
        self.processor.add_puzzle_path("main", main)
    
    def _handle_decode(self, game_state):
        message = self.last_input.replace("decode ", "")
        if message.upper() == "BASILISK":
            return transition_to_room("inner_sanctum",
                ["The lock clicks open!", "You've solved the cipher!"])
        return None, ["That's not the right word..."]
```

### Timed Escape Room
```python
# rooms/rm_server_heist.py
class ServerHeist(TimedPuzzleRoom):
    def __init__(self):
        config = RoomConfig(
            name="Server Room",
            entry_text=[
                "Alarms blare! Security will arrive in 60 seconds!",
                "Download the data and escape!"
            ]
        )
        
        timing = {
            "duration": 60,
            "warning_at": 20,
            "fail_destination": "prison"
        }
        
        super().__init__(config, timing)
    
    def _setup_puzzles(self):
        tasks = {
            "download": PuzzleCommand(
                command="download data",
                sets="data_downloaded",
                success=["Download started... 30 seconds remaining."]
            ),
            "escape": PuzzleCommand(
                command="escape",
                requires=["data_downloaded"],
                transition="safehouse",
                transition_msg=["You escape with the data!"]
            )
        }
        self.processor.add_puzzle_path("heist", tasks)
```

## Resources

### Utility Functions Available

```python
# From resources.room_utils
format_enter_lines(room_name, entry_text)  # Format room entry
standard_commands(cmd, game_state)          # Handle common commands
transition_to_room(destination, messages)   # Change rooms
process_puzzle_command(cmd, state, path)    # Process puzzle paths
```

### Game State Methods

```python
# Flags
game_state.set_flag(name, value)
game_state.get_flag(name)

# Variables
game_state.set(key, value)
game_state.get(key, default=None)

# Inventory
game_state.inventory  # List of items

# Room info
game_state.current_room  # Current room name
game_state.rooms  # All loaded rooms
```

### Testing Commands

Start the game and use these commands to test:

```bash
# In main terminal
start              # Begin game
help               # List commands

# In any room
look               # Examine room
inventory          # Check items
status             # Game status

# Debug (if enabled)
debug flags        # Show all flags
debug give [item]  # Add item
debug solve        # Auto-solve puzzle
```

---

## Contributing

When creating rooms for The Basilisk ARG:

1. Follow the established patterns
2. Test thoroughly using the checklist
3. Document any special mechanics
4. Maintain the cyberpunk aesthetic
5. Ensure puzzles are fair but challenging
6. Provide adequate hints for progression

Happy room building! Remember: The Basilisk is watching...
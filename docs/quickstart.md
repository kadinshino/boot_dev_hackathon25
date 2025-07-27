# Quick Start for GameMaker Developers

Welcome GameMaker developers! This guide translates familiar GML concepts to The Basilisk's Python architecture, helping you create rooms quickly using patterns you already know.

## GML → Python Rosetta Stone

### Basic Concepts

| GameMaker | Python Equivalent | Notes |
|-----------|-------------------|-------|
| `room_goto(rm_next)` | `transition_to_room("next", ["msg"])` | Include transition message |
| `instance_create()` | `game_state.inventory.append("item")` | Items are strings |
| `global.variable` | `game_state.set("variable", value)` | Persistent across rooms |
| `obj.variable` | `self.variable` (in OOP) | Instance variables |
| `if instance_exists()` | `if "item" in game_state.inventory:` | Check for items |
| `show_message()` | `return None, ["message"]` | Display text |
| `keyboard_check()` | `def handle_input(cmd, ...)` | Text commands instead |

### Room Structure Comparison

#### GameMaker Room:
```gml
// rm_puzzle Creation Code
global.door_locked = true;
instance_create_layer(100, 100, "Instances", obj_terminal);

// obj_player Step Event  
if keyboard_check_pressed(ord("E")) {
    if distance_to_object(obj_terminal) < 32 {
        with (obj_terminal) {
            event_user(0); // Activate terminal
        }
    }
}

// obj_terminal User Event 0
if global.has_password {
    global.door_locked = false;
    show_message("Door unlocked!");
    instance_destroy();
}
```

#### Python Equivalent:
```python
# rooms/rm_puzzle.py
ROOM_CONFIG = {
    "name": "Puzzle Room",
    "entry_text": ["A locked door blocks your path. A terminal glows nearby."],
    "destinations": {"north": "next_room"}
}

PUZZLE_PATH = {
    "use_terminal": {
        "command": "use terminal",
        "requires": ["has_password"],
        "sets": "door_unlocked",
        "success": ["Door unlocked!"],
        "missing_req": ["The terminal needs a password."]
    }
}

def handle_input(cmd, game_state, room_module=None):
    # Auto-handles the logic you'd write in Step/User events
    return process_puzzle_command(cmd, game_state, PUZZLE_PATH)
```

## Quick Translations

### 1. Variables & State

```gml
// GML
global.player_health = 100;
global.player_health -= 10;
if (global.player_health <= 0) {
    game_restart();
}
```

```python
# Python
game_state.set("player_health", 100)
health = game_state.get("player_health", 100)
game_state.set("player_health", health - 10)
if game_state.get("player_health", 100) <= 0:
    return transition_to_room("game_over", ["You died!"])
```

### 2. Object Interactions

```gml
// GML - Collision with key
if place_meeting(x, y, obj_key) {
    global.has_key = true;
    instance_destroy(obj_key);
    show_message("You got the key!");
}
```

```python
# Python - Taking items
"take_key": {
    "command": "take key",
    "requires": ["key_visible"],
    "dynamic_response": True
}

def handle_take_key(cmd, game_state):
    game_state.inventory.append("key")
    game_state.set_flag("key_taken", True)
    game_state.set_flag("key_visible", False)
    return None, ["You got the key!"]
```

### 3. Room Transitions

```gml
// GML
if (global.boss_defeated) {
    room_goto(rm_victory);
} else {
    room_goto(rm_game_over);
}
```

```python
# Python
if game_state.get_flag("boss_defeated"):
    return transition_to_room("victory", ["You win!"])
else:
    return transition_to_room("game_over", ["You lose!"])
```

### 4. Timers & Alarms

```gml
// GML
alarm[0] = room_speed * 5; // 5 seconds

// Alarm 0 Event
global.time_up = true;
show_message("Time's up!");
```

```python
# Python (using OOP TimedPuzzleRoom)
class TimedRoom(TimedPuzzleRoom):
    def __init__(self):
        timing_config = {
            "duration": 5,  # 5 seconds
            "fail_destination": "game_over"
        }
        super().__init__(config, timing_config)
    
    def _handle_timeout(self, game_state):
        return transition_to_room("game_over", ["Time's up!"])
```

## Creating Your First Room

### Step 1: Copy Template

```bash
# Start with dictionary style (easier)
cp rooms/rm_template_dict.py rooms/rm_myroom.py
```

### Step 2: Edit Like GML Room Creation Code

```python
# Think of this as Room Properties + Creation Code
ROOM_CONFIG = {
    "name": "My First Room",  # Like room caption
    "entry_text": [           # Like room start message
        "You enter a dark corridor.",
        "A faint light glows ahead."
    ],
    "destinations": {         # Like room exits
        "north": "rm_light_source",
        "south": "rm_entrance"
    }
}
```

### Step 3: Add Interactions (Like Object Events)

```python
# Instead of obj_button Step Event checking for collision
PUZZLE_PATH = {
    "press_button": {
        "command": "press button",
        "sets": "button_pressed",
        "success": ["Click! Something activated."]
    }
}

# Instead of obj_door Step Event checking flag
"open_door": {
    "command": "open door",  
    "requires": ["button_pressed"],
    "transition": True,
    "transition_dest": "north",
    "transition_msg": ["The door opens. You step through."]
}
```

## Common Patterns

### 1. The "Object in Room" Pattern

```gml
// GML: Multiple objects in room
instance_create(x1, y1, obj_key);
instance_create(x2, y2, obj_chest);
instance_create(x3, y3, obj_note);
```

```python
# Python: Describe objects, make them interactable
ROOM_CONFIG = {
    "entry_text": [
        "You see a key on the table.",
        "A chest sits in the corner.",  
        "A note is pinned to the wall."
    ]
}

PUZZLE_PATH = {
    "take_key": {"command": "take key", ...},
    "open_chest": {"command": "open chest", ...},
    "read_note": {"command": "read note", ...}
}
```

### 2. The "Inventory Check" Pattern

```gml
// GML: Using items
if keyboard_check_pressed(ord("U")) {
    if global.has_torch && global.in_dark_room {
        global.room_lit = true;
    }
}
```

```python
# Python: Conditional commands
"use_torch": {
    "command": "use torch",
    "dynamic_response": True
}

def handle_use_torch(cmd, game_state):
    if "torch" not in game_state.inventory:
        return None, ["You don't have a torch."]
    if not game_state.get_flag("in_dark_room"):
        return None, ["You don't need light here."]
    
    game_state.set_flag("room_lit", True)
    return None, ["The torch illuminates the room!"]
```

### 3. The "Multi-Step Puzzle" Pattern

```gml
// GML: Sequence tracking
if (global.puzzle_step == 0 && collision) {
    global.puzzle_step = 1;
} else if (global.puzzle_step == 1 && keyboard_check(ord("E"))) {
    global.puzzle_step = 2;
}
```

```python
# Python: Using flags for sequences
SEQUENCE = {
    "step1": {
        "command": "pull lever",
        "sets": "lever_pulled",
        "success": ["The lever clicks."]
    },
    "step2": {
        "command": "press button",
        "requires": ["lever_pulled"],
        "sets": "button_pressed",
        "success": ["The button glows."]
    },
    "step3": {
        "command": "turn dial",
        "requires": ["button_pressed"],
        "sets": "puzzle_complete",
        "success": ["The door opens!"]
    }
}
```

## Advanced: OOP for GameMaker Devs

Think of OOP rooms like GameMaker objects with inheritance:

```python
# Like parent objects in GameMaker
class PuzzleRoom(BaseRoom):  # Like obj_puzzle_parent
    def solve_puzzle(self):
        # Common puzzle logic
        pass

class MathPuzzle(PuzzleRoom):  # Like obj_math_puzzle : obj_puzzle_parent
    def solve_puzzle(self):
        # Specific math puzzle logic
        super().solve_puzzle()  # Like event_inherited()
```

## Debugging Tips

### 1. Debug Commands (Like show_debug_message)

```python
# Add to any room for testing
if cmd == "debug":
    return None, [
        f"Flags: {[f for f, v in game_state.flags.items() if v]}",
        f"Inventory: {game_state.inventory}",
        f"Variables: {game_state.variables}"
    ]
```

### 2. Test Without Restarting

Unlike GameMaker, you can test rooms individually:

```python
# Run just your room
python -c "import rooms.rm_myroom as room; print(room.get_available_commands())"
```

### 3. Common Gotchas

| GameMaker Habit | Python Fix |
|-----------------|------------|
| `if (thing)` works on undefined | Use `game_state.get("thing", False)` |
| Objects persist in room | Flags/inventory persist, room state doesn't |
| `instance_destroy()` removes object | Use flags: `set_flag("item_taken", True)` |
| Collision triggers automatically | Player must type commands |

## Quick Reference Card

```python
# Essential imports
from resources.room_utils import (
    format_enter_lines,      # Format room entry
    standard_commands,       # Handle look/inventory/etc
    transition_to_room,      # Change rooms
    process_puzzle_command   # Process your puzzles
)

# Room template
ROOM_CONFIG = {
    "name": "Room Name",
    "entry_text": ["Description"],
    "destinations": {"north": "next_room"}
}

PUZZLE_PATH = {
    "action": {
        "command": "do thing",
        "requires": ["have_thing"],  
        "sets": "thing_done",
        "success": ["It worked!"]
    }
}

def enter_room(game_state):
    return format_enter_lines(ROOM_CONFIG["name"], ROOM_CONFIG["entry_text"])

def handle_input(cmd, game_state, room_module=None):
    result = standard_commands(cmd, game_state)
    if result:
        return None, result
    
    return process_puzzle_command(cmd, game_state, PUZZLE_PATH)

def get_available_commands():
    return ["do thing - does the thing"]
```

## Next Steps

1. **Start Simple**: Make a basic room with one puzzle
2. **Test Often**: Run the game and try your commands
3. **Add Complexity**: Layer in more puzzles and state checks
4. **Share Your Work**: Drop your .py file in `rooms/` and it just works!

Remember: No more collision events or sprite management—just focus on the puzzles and story!

*Welcome to Python, GameMaker dev. The Basilisk awaits your creations.*
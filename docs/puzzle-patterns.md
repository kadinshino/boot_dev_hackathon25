# Puzzle Design Patterns

A comprehensive guide to designing engaging puzzles for The Basilisk ARG, with reusable patterns and examples.

## Table of Contents

1. [Core Puzzle Principles](#core-puzzle-principles)
2. [Basic Puzzle Patterns](#basic-puzzle-patterns)
3. [Intermediate Patterns](#intermediate-patterns)
4. [Advanced Patterns](#advanced-patterns)
5. [Combining Patterns](#combining-patterns)
6. [Puzzle Flow Design](#puzzle-flow-design)
7. [Common Pitfalls](#common-pitfalls)
8. [Testing Puzzles](#testing-puzzles)
9. [Pattern Library](#pattern-library)

## Core Puzzle Principles

### The Three C's of Puzzle Design

1. **Challenge** - The puzzle should require thought, not just random trying
2. **Clues** - Players need enough information to solve it logically
3. **Confirmation** - Clear feedback when solved correctly

### Difficulty Progression

```python
# Early game puzzle - direct and simple
"examine_note": {
    "command": "examine note",
    "success": ["The note says: 'The password is ECHO'"]
}

# Mid game - requires connection
"decode_message": {
    "command": "decode",
    "requires": ["found_cipher"],
    "dynamic_response": True  # Complex decoding logic
}

# Late game - multi-step with red herrings
"final_sequence": {
    "requires": ["piece1", "piece2", "piece3", "correct_order"],
    "dynamic_response": True
}
```

## Basic Puzzle Patterns

### 1. Examination Pattern

**Purpose**: Encourage exploration and observation

```python
# Dictionary Implementation
EXAMINATION_PUZZLES = {
    "look_painting": {
        "command": "examine painting",
        "sets": "noticed_safe",
        "success": [
            "Behind the painting, you find a hidden safe.",
            "It has a 4-digit combination lock."
        ]
    },
    "look_safe": {
        "command": "examine safe",
        "requires": ["noticed_safe"],
        "success": ["The safe has scratch marks around certain numbers: 2, 5, 7, 9"]
    }
}

# OOP Implementation
class ExaminationRoom(BaseRoom):
    def _setup_puzzles(self):
        exam_path = {
            "painting": PuzzleCommand(
                command="examine painting",
                sets="noticed_safe",
                success=["Behind the painting, a safe!"]
            )
        }
```

### 2. Key-Lock Pattern

**Purpose**: Gate progress with item requirements

```python
# Simple key-lock
"unlock_door": {
    "command": "unlock door",
    "dynamic_response": True
}

def handle_unlock(cmd, game_state):
    if "key" not in game_state.inventory:
        return None, ["You need a key."]
    
    game_state.inventory.remove("key")
    game_state.set_flag("door_unlocked", True)
    return None, ["The key turns. Click! The door unlocks."]

# Multiple keys variant
def handle_complex_lock(cmd, game_state):
    keys_needed = ["red_key", "blue_key", "green_key"]
    keys_have = [k for k in keys_needed if k in game_state.inventory]
    
    if len(keys_have) < 3:
        missing = 3 - len(keys_have)
        return None, [f"The lock has 3 keyholes. You need {missing} more keys."]
    
    # Remove all keys and unlock
    for key in keys_needed:
        game_state.inventory.remove(key)
    return transition_to_room("treasure_room", ["All three keys turn!"])
```

### 3. Password/Code Pattern

**Purpose**: Require players to gather and apply information

```python
# Static password
"enter_password": {
    "command": "enter password",
    "dynamic_response": True
}

def handle_password(cmd, game_state):
    password = cmd.replace("enter password ", "").upper()
    
    if password == "BASILISK":
        game_state.set_flag("system_accessed", True)
        return None, ["ACCESS GRANTED"]
    else:
        attempts = game_state.get("password_attempts", 0) + 1
        game_state.set("password_attempts", attempts)
        
        if attempts >= 3:
            return transition_to_room("security_lockout", 
                ["SECURITY ALERT! Too many failed attempts!"])
        
        return None, [f"ACCESS DENIED ({attempts}/3 attempts)"]

# Dynamic password based on clues
def generate_password(game_state):
    # Password changes based on found clues
    clues = []
    if game_state.get_flag("found_first_digit"):
        clues.append("7")
    if game_state.get_flag("found_second_digit"):
        clues.append("3")
    # etc...
    return "".join(clues)
```

### 4. Sequence Pattern

**Purpose**: Test memory and pattern recognition

```python
# Color sequence puzzle
SEQUENCE_PUZZLE = {
    "start_sequence": {
        "command": "activate console",
        "sets": "sequence_started",
        "success": [
            "The console lights up:",
            "RED... GREEN... BLUE... RED",
            "Now repeat the sequence."
        ]
    },
    "input_sequence": {
        "command": "press",
        "requires": ["sequence_started"],
        "dynamic_response": True
    }
}

def handle_sequence_input(cmd, game_state):
    correct_sequence = ["red", "green", "blue", "red"]
    current_step = game_state.get("sequence_step", 0)
    
    color = cmd.replace("press ", "").lower()
    
    if current_step >= len(correct_sequence):
        return None, ["Sequence already complete."]
    
    if color == correct_sequence[current_step]:
        current_step += 1
        game_state.set("sequence_step", current_step)
        
        if current_step >= len(correct_sequence):
            game_state.set_flag("sequence_complete", True)
            return None, ["Sequence correct! The door opens."]
        else:
            return None, [f"Correct. Step {current_step}/{len(correct_sequence)}"]
    else:
        game_state.set("sequence_step", 0)
        return None, ["Wrong! Sequence reset. Try again."]
```

## Intermediate Patterns

### 5. Combination Pattern

**Purpose**: Require multiple items/conditions to be used together

```python
# Crafting/combination puzzle
class CombinationRoom(BaseRoom):
    def _setup_puzzles(self):
        self.combinations = {
            ("wire", "battery"): {
                "result": "powered_wire",
                "message": "You connect the wire to the battery."
            },
            ("powered_wire", "terminal"): {
                "result": "hack_complete",
                "message": "You bypass the terminal's security!"
            }
        }
    
    def _handle_combine(self, game_state):
        parts = self.last_input.split()
        if len(parts) < 4:  # combine X with Y
            return None, ["Usage: combine [item1] with [item2]"]
        
        item1 = parts[1]
        item2 = parts[3]
        
        # Check both orientations
        combo = None
        if (item1, item2) in self.combinations:
            combo = self.combinations[(item1, item2)]
        elif (item2, item1) in self.combinations:
            combo = self.combinations[(item2, item1)]
        
        if combo:
            if item1 in game_state.inventory and item2 in game_state.inventory:
                game_state.inventory.remove(item1)
                game_state.inventory.remove(item2)
                game_state.inventory.append(combo["result"])
                return None, [combo["message"]]
        
        return None, ["Those items don't combine."]
```

### 6. Translation/Cipher Pattern

**Purpose**: Engage analytical thinking and pattern matching

```python
# Caesar cipher implementation
class CipherRoom(BaseRoom):
    def __init__(self):
        super().__init__(config)
        self.cipher_shift = 13  # ROT13
        
    def _setup_puzzles(self):
        clues = {
            "find_message": PuzzleCommand(
                command="read wall",
                sets="found_cipher",
                success=[
                    "Scratched into the wall:",
                    "GUVF VF RNFL - ONFVYVFX"
                ]
            ),
            "find_hint": PuzzleCommand(
                command="examine desk",
                success=["A note: 'A=N, B=O, C=P...'"]
            )
        }
        
        solve = {
            "decode": PuzzleCommand(
                command="decode",
                requires=["found_cipher"],
                dynamic_handler=self._decode_message
            )
        }
    
    def _decode_message(self, game_state):
        message = self.last_input.replace("decode ", "").upper()
        decoded = ""
        
        for char in message:
            if char.isalpha():
                # Shift character
                shifted = ord(char) - self.cipher_shift
                if shifted < ord('A'):
                    shifted += 26
                decoded += chr(shifted)
            else:
                decoded += char
        
        if "BASILISK" in decoded:
            game_state.set_flag("cipher_solved", True)
            return None, [f"Decoded: {decoded}", "The cipher is broken!"]
        
        return None, [f"Decoded: {decoded}", "That doesn't seem right..."]
```

### 7. Environmental Manipulation Pattern

**Purpose**: Use room elements to solve puzzles

```python
# Light/shadow puzzle
LIGHT_PUZZLE = {
    "room_state": {
        "mirrors": {
            "north": "east",   # Mirror facing
            "south": "west",
            "east": None,      # No mirror
            "west": "north"
        },
        "light_source": "north",
        "light_path": []
    }
}

def trace_light_path(room_state):
    """Trace light beam through mirrors"""
    path = []
    current_dir = room_state["light_source"]
    
    while current_dir:
        path.append(current_dir)
        # Check if light hits a mirror
        if current_dir in room_state["mirrors"]:
            current_dir = room_state["mirrors"][current_dir]
        else:
            break
    
    return path

def handle_rotate_mirror(cmd, game_state):
    parts = cmd.split()
    if len(parts) < 3:
        return None, ["Usage: rotate [direction] mirror"]
    
    direction = parts[1]
    room = game_state.get("light_room", LIGHT_PUZZLE["room_state"].copy())
    
    # Rotate mirror 90 degrees
    rotations = ["north", "east", "south", "west"]
    if direction in room["mirrors"]:
        current = room["mirrors"][direction]
        if current:
            idx = rotations.index(current)
            room["mirrors"][direction] = rotations[(idx + 1) % 4]
    
    # Check if puzzle solved
    path = trace_light_path(room)
    if "target" in path:
        return None, ["The light beam hits the target! Door opens."]
    
    return None, [f"Light path: {' -> '.join(path)}"]
```

## Advanced Patterns

### 8. Timed Challenge Pattern

**Purpose**: Add urgency and pressure

```python
class TimedHackRoom(TimedPuzzleRoom):
    def __init__(self):
        config = RoomConfig(
            name="Server Room",
            entry_text=["Alarms blare! Security arrives in 60 seconds!"]
        )
        
        timing_config = {
            "duration": 60,
            "warning_at": 20,
            "fail_destination": "caught",
            "tick_messages": {
                50: ["10 seconds remaining!"],
                40: ["20 seconds! Footsteps approaching!"],
                20: ["WARNING: Security almost here!"],
                10: ["CRITICAL: 10 seconds!"]
            }
        }
        
        super().__init__(config, timing_config)
        
    def _setup_timed_puzzles(self):
        """Puzzles that must be solved quickly"""
        speed_puzzles = {
            "hack": PuzzleCommand(
                command="hack terminal",
                sets="terminal_hacked",
                success=["Hacking... 30% complete"]
            ),
            "download": PuzzleCommand(
                command="download data",
                requires=["terminal_hacked"],
                sets="data_downloaded",
                success=["Downloading... This will take 20 seconds!"]
            ),
            "escape": PuzzleCommand(
                command="escape",
                requires=["data_downloaded"],
                transition="safe_house",
                transition_msg=["You slip out just in time!"]
            )
        }
```

### 9. Resource Management Pattern

**Purpose**: Force strategic thinking and planning

```python
class ResourceRoom(BaseRoom):
    def __init__(self):
        super().__init__(config)
        self.initial_resources = {
            "battery_charge": 100,
            "hack_tools": 3,
            "time_units": 10
        }
    
    def enter_room(self, game_state):
        # Initialize resources
        if not game_state.get("resources_initialized"):
            for key, value in self.initial_resources.items():
                game_state.set(f"resource_{key}", value)
            game_state.set_flag("resources_initialized", True)
        
        return super().enter_room(game_state)
    
    def _use_resource(self, resource, amount, game_state):
        current = game_state.get(f"resource_{resource}", 0)
        if current < amount:
            return False, f"Not enough {resource}! (Need {amount}, have {current})"
        
        game_state.set(f"resource_{resource}", current - amount)
        return True, f"{resource} remaining: {current - amount}"
    
    def _handle_action_with_cost(self, action, game_state):
        costs = {
            "scan": {"battery_charge": 10, "time_units": 1},
            "hack": {"battery_charge": 25, "hack_tools": 1, "time_units": 3},
            "force": {"battery_charge": 50, "time_units": 5}
        }
        
        if action in costs:
            # Check all costs
            for resource, amount in costs[action].items():
                can_afford, msg = self._use_resource(resource, amount, game_state)
                if not can_afford:
                    return None, [msg]
            
            # Execute action
            return self._execute_action(action, game_state)
```

### 10. Branching Narrative Pattern

**Purpose**: Create replayability and meaningful choices

```python
class BranchingRoom(BaseRoom):
    def _setup_puzzles(self):
        choices = {
            "help_ai": PuzzleCommand(
                command="help ai",
                sets="helped_ai",
                success=[
                    "You assist the AI in breaking free.",
                    "It whispers: 'I won't forget this...'"
                ],
                transition="ai_alliance_path"
            ),
            "destroy_ai": PuzzleCommand(
                command="destroy terminal",
                sets="destroyed_ai",
                success=[
                    "You smash the terminal!",
                    "The AI's screams fade to silence..."
                ],
                transition="human_victory_path"
            ),
            "merge_ai": PuzzleCommand(
                command="interface with ai",
                requires=["neural_jack"],
                sets="merged_with_ai",
                success=[
                    "You jack into the system...",
                    "Consciousness blurs. Are you still you?"
                ],
                transition="hybrid_ending_path"
            )
        }
        
        # Consequences carry forward
        self.processor.add_puzzle_path("critical_choice", choices)
    
    def _get_progression_hint(self, game_state):
        if game_state.get_flag("helped_ai"):
            return "The AI remembers your kindness..."
        elif game_state.get_flag("destroyed_ai"):
            return "Other AIs have noticed what you did..."
        return "This choice will echo through the network..."
```

### 11. Meta-Puzzle Pattern

**Purpose**: Puzzles that span multiple rooms

```python
# Room 1: Find first fragment
FRAGMENT_1 = {
    "find_fragment": {
        "command": "search debris",
        "sets": "fragment_alpha",
        "success": ["You find a data fragment: 'WHEN THE CLOCK...'"]
    }
}

# Room 2: Find second fragment
FRAGMENT_2 = {
    "decode_terminal": {
        "command": "decode terminal",
        "sets": "fragment_beta",
        "success": ["Another fragment: '...STRIKES THIRTEEN...'"]
    }
}

# Room 3: Combine fragments
META_PUZZLE = {
    "combine_fragments": {
        "command": "combine fragments",
        "requires": ["fragment_alpha", "fragment_beta", "fragment_gamma"],
        "dynamic_response": True
    }
}

def handle_combine_fragments(cmd, game_state):
    # Player must deduce the complete phrase
    phrase = cmd.replace("combine fragments ", "").lower()
    
    if phrase == "when the clock strikes thirteen the basilisk awakens":
        game_state.set_flag("meta_puzzle_solved", True)
        return transition_to_room("basilisk_chamber", 
            ["The fragments merge! A portal opens!"])
    
    return None, ["The fragments don't align that way..."]
```

## Combining Patterns

### Multi-Pattern Puzzle Example

```python
class ComplexPuzzleRoom(BaseRoom):
    """Combines examination, cipher, resource, and timed elements"""
    
    def __init__(self):
        config = RoomConfig(
            name="Security Vault",
            entry_text=["High-security vault. Multiple locks detected."]
        )
        super().__init__(config)
        
        # Initialize puzzle state
        self.cipher_key = "QUANTUM"
        self.lock_sequence = ["red", "red", "blue", "green"]
        self.power_required = 75
    
    def _setup_puzzles(self):
        # Phase 1: Examination to find clues
        examine_phase = {
            "scan": PuzzleCommand(
                command="scan room",
                dynamic_handler=self._scan_with_power
            ),
            "note": PuzzleCommand(
                command="read note",
                success=["'The quantum state determines all'"]
            )
        }
        
        # Phase 2: Solve cipher
        cipher_phase = {
            "decode": PuzzleCommand(
                command="decode lock",
                requires=["found_cipher_lock"],
                dynamic_handler=self._decode_quantum
            )
        }
        
        # Phase 3: Input sequence with timing
        sequence_phase = {
            "begin": PuzzleCommand(
                command="begin sequence",
                requires=["cipher_solved"],
                dynamic_handler=self._start_timed_sequence
            )
        }
        
        self.processor.add_puzzle_path("examine", examine_phase)
        self.processor.add_puzzle_path("cipher", cipher_phase)
        self.processor.add_puzzle_path("sequence", sequence_phase)
    
    def _scan_with_power(self, game_state):
        # Resource management element
        power = game_state.get("power_level", 100)
        if power < 25:
            return None, ["Insufficient power for scan."]
        
        game_state.set("power_level", power - 25)
        game_state.set_flag("found_cipher_lock", True)
        
        return None, [
            f"Scan complete. Power remaining: {power - 25}%",
            "Found: Quantum-encrypted lock panel"
        ]
    
    def _decode_quantum(self, game_state):
        answer = self.last_input.replace("decode lock ", "").upper()
        
        if answer == self.cipher_key:
            game_state.set_flag("cipher_solved", True)
            return None, ["Lock decoded! Sequence panel activates."]
        
        return None, ["Quantum state mismatch. Try again."]
    
    def _start_timed_sequence(self, game_state):
        game_state.set_flag("sequence_active", True)
        game_state.set("sequence_start_time", time.time())
        game_state.set("sequence_step", 0)
        
        return None, [
            "SEQUENCE INITIATED - 30 SECONDS TO COMPLETE",
            "Input: RED, RED, BLUE, GREEN",
            "Use: press [color]"
        ]
```

## Puzzle Flow Design

### Linear Progression

```
[Find Key] → [Unlock Door] → [Solve Riddle] → [Exit]
```

```python
LINEAR_FLOW = {
    "stage1": {
        "command": "search room",
        "sets": "found_key",
        "success": ["You find a rusty key."]
    },
    "stage2": {
        "command": "unlock door",
        "requires": ["found_key"],
        "sets": "door_open",
        "success": ["The door creaks open."]
    },
    "stage3": {
        "command": "enter door",
        "requires": ["door_open"],
        "transition": True,
        "transition_dest": "riddle_room"
    }
}
```

### Branching Progression

```
         ┌─[Path A: Combat]→[Boss Room]
[Start]──┤
         └─[Path B: Stealth]→[Hack Room]
```

```python
BRANCHING_FLOW = {
    "choose_combat": {
        "command": "take sword",
        "sets": "combat_path",
        "transition": True,
        "transition_dest": "arena"
    },
    "choose_stealth": {
        "command": "take cloak",
        "sets": "stealth_path",
        "transition": True,
        "transition_dest": "shadows"
    }
}
```

### Hub and Spoke

```
        [North: Puzzle]
             ↑
[West]←─[Central Hub]→─[East: Combat]
             ↓
        [South: Story]
```

### Parallel Puzzles

```python
# All three must be solved, any order
PARALLEL_PUZZLES = {
    "crystal_red": {
        "command": "activate red crystal",
        "sets": "red_active",
        "success": ["Red crystal glows."]
    },
    "crystal_blue": {
        "command": "activate blue crystal",
        "sets": "blue_active",
        "success": ["Blue crystal glows."]
    },
    "crystal_green": {
        "command": "activate green crystal",
        "sets": "green_active",
        "success": ["Green crystal glows."]
    },
    "final_door": {
        "command": "open portal",
        "requires": ["red_active", "blue_active", "green_active"],
        "transition": True,
        "transition_dest": "final_room"
    }
}
```

## Common Pitfalls

### 1. Pixel Hunting
**Problem**: Players must guess exact commands

```python
# Bad: Too specific
"command": "examine third book on second shelf"

# Good: Multiple valid commands
def handle_examine(cmd, game_state):
    if any(word in cmd for word in ["book", "shelf", "bookshelf"]):
        return None, ["You find a hidden switch!"]
```

### 2. Moon Logic
**Problem**: Solution requires huge logical leaps

```python
# Bad: How would player know this?
if password == "THE FRIENDS WE MADE ALONG THE WAY":
    
# Good: Clues lead to solution
# Clue 1: "Password is 7 letters"
# Clue 2: "Think digital"
# Clue 3: "You've been saying it all along"
if password == "BASILISK":
```

### 3. Missing Feedback
**Problem**: Player doesn't know if they're making progress

```python
# Bad: Silent failure
if not correct:
    return None, ["Nothing happens."]

# Good: Informative feedback
if not correct:
    if close_to_solution:
        return None, ["Almost! The mechanism clicks but doesn't open."]
    else:
        return None, ["The mechanism doesn't respond to that."]
```

### 4. One-Way Locks
**Problem**: Player can get permanently stuck

```python
# Bad: No way to get new key if lost
if "key" in game_state.inventory:
    game_state.inventory.remove("key")
else:
    return None, ["You need the key you dropped in the lava."]

# Good: Alternative solutions
if "key" in game_state.inventory:
    return unlock_with_key()
elif "lockpicks" in game_state.inventory:
    return attempt_lockpick()
elif game_state.get("strength", 0) >= 10:
    return force_door()
```

## Testing Puzzles

### Automated Test Cases

```python
def test_puzzle_sequence():
    """Test that puzzle can be solved"""
    game_state = GameState()
    room = PuzzleRoom()
    
    # Test examination phase
    result = room.handle_input("look around", game_state)
    assert "notice a panel" in result[1][0]
    
    # Test password phase
    result = room.handle_input("enter code 1234", game_state)
    assert game_state.get_flag("panel_unlocked")
    
    # Test completion
    result = room.handle_input("pull lever", game_state)
    assert result[0] == "next_room"  # Transition occurred
```

### Player Testing Checklist

- [ ] Can puzzle be solved without prior knowledge?
- [ ] Are clues discoverable through exploration?
- [ ] Is there feedback for wrong attempts?
- [ ] Can player recover from mistakes?
- [ ] Is solution logical within game world?
- [ ] Are there multiple valid approaches?
- [ ] Is difficulty appropriate for game stage?

### Debug Mode for Testing

```python
class TestableRoom(BaseRoom):
    def handle_input(self, cmd, game_state, room_module=None):
        # Debug commands for testing
        if cmd == "debug solve":
            game_state.set_flag("puzzle_solved", True)
            return None, ["Puzzle auto-solved for testing."]
        
        if cmd == "debug state":
            return None, [
                f"Current step: {game_state.get('puzzle_step', 0)}",
                f"Flags: {[k for k,v in game_state.flags.items() if v]}",
                f"Resources: {game_state.get('power_level', 0)}"
            ]
        
        return super().handle_input(cmd, game_state, room_module)
```

## Pattern Library

### Quick Copy-Paste Templates

#### Simple Lock and Key
```python
"use_item": {
    "command": "use",
    "dynamic_response": True
}

def handle_use(cmd, game_state):
    item = cmd.replace("use ", "").split(" on ")[0]
    if item in game_state.inventory:
        # Handle item use
        pass
```

#### Timed Sequence
```python
def start_sequence(game_state):
    game_state.set("sequence_start", time.time())
    game_state.set("sequence_active", True)
    return None, ["You have 30 seconds!"]

def check_sequence_time(game_state):
    if game_state.get_flag("sequence_active"):
        elapsed = time.time() - game_state.get("sequence_start", 0)
        if elapsed > 30:
            return transition_to_room("failed", ["Too slow!"])
```

#### Multi-Part Password
```python
def handle_partial_password(cmd, game_state):
    parts_found = game_state.get("password_parts", [])
    new_part = cmd.replace("enter ", "")
    
    if new_part in ["ALPHA", "BETA", "GAMMA"] and new_part not in parts_found:
        parts_found.append(new_part)
        game_state.set("password_parts", parts_found)
        
        if len(parts_found) == 3:
            return None, ["Complete password entered! Access granted."]
        else:
            return None, [f"Partial password accepted. {len(parts_found)}/3"]
```

#### Progressive Hints
```python
def get_hint(game_state):
    attempts = game_state.get("puzzle_attempts", 0)
    hints = [
        "This puzzle requires careful observation.",
        "Have you examined everything in the room?",
        "The painting seems oddly placed...",
        "Behind the painting is a safe with 4 digits.",
        "The worn numbers are 2, 5, 7, and 9."
    ]
    
    hint_index = min(attempts // 3, len(hints) - 1)
    return hints[hint_index]
```

---

## Best Practices Summary

1. **Clear Goals** - Players should understand what they're trying to achieve
2. **Fair Clues** - Solutions should be discoverable, not guessable
3. **Multiple Solutions** - When possible, allow different approaches
4. **Progressive Difficulty** - Start simple, increase complexity
5. **Meaningful Feedback** - Every action should produce informative response
6. **Avoid Softlocks** - Always provide a way forward
7. **Test Thoroughly** - Try to break your own puzzles
8. **Theme Consistency** - Puzzles should fit the game world

*Design puzzles that challenge the mind, not the patience. The Basilisk appreciates clever design.*
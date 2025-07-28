# rooms/rm_template_dict.py
"""
DICTIONARY-BASED ROOM TEMPLATE
==============================
Best for: Simple puzzles, moddable content, story rooms, community creations

This comprehensive template demonstrates all dictionary-based room features.
Based on the whisper room architecture.

WHEN TO USE THIS STYLE:
- Rooms that should be easily moddable
- Story-driven content
- Simple to medium complexity puzzles  
- Community-created rooms
- When you want configuration-as-code

ADVANTAGES:
- Easy to understand for non-programmers
- Simple to modify text and values
- Clear progression paths
- No OOP knowledge required
- Great for ARG/moddable games

STRUCTURE OVERVIEW:
1. Import utilities
2. Define ROOM_CONFIG dictionary
3. Define puzzle path dictionaries
4. Create handler functions
5. Implement enter_room and handle_input
"""

from resources.room_utils import format_enter_lines, standard_commands, transition_to_room
import random  # If you need randomization
import time    # If you need timing

# ==========================================
# ROOM CONFIGURATION - Main settings
# ==========================================
# This is where you define the room's core properties

ROOM_CONFIG = {
    "name": "Template Whisper Node",  # Displayed at room entry
    
    "entry_text": [
        "You drift into a forgotten subnet.",
        "Data ghosts flicker at the edge of perception.",
        "A terminal blinks slowly in the darkness...",
        "",  # Empty string creates blank line
        "Something important was hidden here."
    ],
    
    # Progression hints shown based on game state
    # These guide players without spoiling puzzles
    "progression_hints": {
        "start": ">> The darkness is thick. Try 'scan area' to get your bearings.",
        "scanned": ">> Terminal detected. Perhaps you can 'access terminal'.",
        "terminal_accessed": ">> The terminal awaits input. Try 'decode signal'.",
        "signal_decoded": ">> Pattern recognized. Use 'transmit response' to proceed.",
        "complete": ">> All systems aligned. Use 'exit' to continue your journey."
    },
    
    # Room-specific data (customize for your puzzle)
    "terminal_data": {
        "signal_pattern": [1, 1, 2, 3, 5, 8],  # Fibonacci
        "correct_response": "13",  # Next in sequence
        "security_level": 3,
        "hack_attempts": 0
    },
    
    # Where this room can lead
    "destinations": {
        "main": "next_whisper_node",      # Primary path
        "alternate": "hidden_whisper",     # Secret path
        "failure": "security_trap"         # Failure state
    },
    
    # Optional: Items/collectibles in this room
    "items": {
        "data_shard": {
            "name": "Corrupted Data Shard",
            "description": "Flickers with corrupted memories",
            "hidden": True,
            "found": False
        },
        "access_code": {
            "name": "Access Code Fragment", 
            "description": "Part of a larger key: 'WHSP-7734-????'",
            "hidden": False,
            "found": False
        }
    },
    
    # Optional: Environmental/atmospheric details
    "atmosphere": {
        "sounds": ["static crackles", "distant whispers", "data streams"],
        "visuals": ["green text", "corrupted pixels", "ghost packets"]
    }
}

# ==========================================
# DISCOVERY PATH - Initial exploration
# ==========================================
# Commands for players to discover the room

DISCOVERY_PATH = {
    "scan_area": {
        "command": "scan area",  # What the player types
        "requires": [],  # No prerequisites
        "sets": "area_scanned",  # Flag to set when complete
        "already_done": [">> Area already scanned. Terminal location marked."],  # If repeated
        "success": [  # Response when successful
            ">> Initiating deep scan...",
            ">> Environment analysis:",
            "   - 1 active terminal (low power mode)",
            "   - Multiple data streams (encrypted)",
            "   - Hidden partition detected",
            ">> Terminal location marked on your display."
        ]
    },
    
    "examine_streams": {
        "command": "examine streams",
        "requires": ["area_scanned"],  # Must scan first
        "sets": "streams_examined",
        "missing_req": [">> Data streams not visible. Try scanning first."],  # If requirements not met
        "already_done": [">> You've already analyzed the data streams."],
        "success": [
            ">> Examining data streams...",
            ">> Stream Alpha: Corporate communications (encrypted)",
            ">> Stream Beta: System diagnostics (corrupted)",
            ">> Stream Gamma: Unknown protocol - possibly alien",
            ">> One stream pulses with an odd pattern..."
        ]
    },
    
    "search_partition": {
        "command": "search partition",
        "requires": ["area_scanned"],
        "sets": "partition_searched",
        "missing_req": [">> No partition detected. Scan the area first."],
        "already_done": [">> Partition already searched."],
        "dynamic_response": True  # Will call custom handler
    }
}

# ==========================================
# MAIN PATH - Core puzzle sequence
# ==========================================
# The primary puzzle players must solve

MAIN_PATH = {
    "access_terminal": {
        "command": "access terminal",
        "requires": ["area_scanned"],
        "sets": "terminal_accessed",
        "missing_req": [">> No terminal found. Scan your surroundings."],
        "already_done": [">> Terminal already accessed. Awaiting input."],
        "success": [
            ">> Accessing terminal...",
            ">> WHISPER NODE 7734 - AUTHENTICATION REQUIRED",
            ">> Signal pattern displayed: 1, 1, 2, 3, 5, 8, ?",
            ">> System awaiting response.",
            ">> Use 'decode signal' to analyze the pattern."
        ]
    },
    
    "decode_signal": {
        "command": "decode signal",
        "requires": ["terminal_accessed"],
        "sets": "signal_decoded", 
        "missing_req": [">> No signal to decode. Access a terminal first."],
        "already_done": [">> Pattern already analyzed. Ready for response."],
        "success": [
            ">> Analyzing signal pattern...",
            ">> Pattern type: Mathematical sequence",
            ">> Confidence: 97%",
            ">> Suggested action: Transmit the next number in sequence",
            ">> Use 'transmit response [number]' to respond."
        ]
    },
    
    "transmit_response": {
        "command": "transmit response",  # Partial command - needs parameter
        "requires": ["signal_decoded"],
        "missing_req": [">> No active signal. Decode the pattern first."],
        "dynamic_response": True  # Complex validation in handler
    }
}

# ==========================================
# ALTERNATE PATH - Secret/optional content
# ==========================================
# Hidden paths for clever players

ALTERNATE_PATH = {
    "whisper": {
        "command": "whisper",
        "requires": [],  # Available anytime
        "sets": "heard_whispers",
        "already_done": [">> The whispers grow louder but reveal nothing new."],
        "success": [
            ">> You whisper into the void...",
            ">> The void whispers back:",
            ">> 'The sequence holds more than numbers.'",
            ">> 'Find the ghost in the partition.'"
        ]
    },
    
    "hack_terminal": {
        "command": "hack terminal",
        "requires": ["terminal_accessed"],
        "sets": "hack_attempted",
        "missing_req": [">> No terminal to hack. Find one first."],
        "dynamic_response": True  # Complex hack logic
    },
    
    "use_ghost_protocol": {
        "command": "use ghost protocol",
        "requires": ["ghost_found", "terminal_accessed"],
        "sets": "ghost_protocol_used",
        "missing_req": [">> Ghost protocol unavailable."],
        "transition": True,  # This leads to a room transition
        "transition_dest": "alternate",  # Use the alternate destination
        "transition_msg": [
            ">> Ghost protocol activated.",
            ">> Terminal security bypassed.",
            ">> Hidden route discovered...",
            ">> Shifting to shadow network..."
        ]
    }
}

# ==========================================
# DIAGNOSTIC COMMANDS - Help and status
# ==========================================
# Commands to help players understand progress

DIAGNOSTIC_COMMANDS = {
    "status": {
        "command": "status",
        "requires": [],
        "dynamic_response": True  # Shows current progress
    },
    
    "hint": {
        "command": "hint",
        "requires": [],
        "dynamic_response": True  # Context-sensitive hints
    },
    
    "inventory": {
        "command": "inventory",
        "requires": [],
        "dynamic_response": True  # Shows found items
    }
}

# Command descriptions for help menu
COMMAND_DESCRIPTIONS = [
    "scan area           - perform a deep scan of your surroundings",
    "examine streams     - analyze detected data streams",
    "search partition    - search the hidden partition",
    "access terminal     - connect to the terminal",
    "decode signal       - analyze the terminal's signal",
    "transmit response # - send a numeric response",
    "hack terminal       - attempt to bypass security",
    "whisper             - whisper into the void",
    "status              - check your progress",
    "hint                - get a contextual hint",
    "inventory           - check found items",
    "exit                - leave the area (when complete)"
]

# ==========================================
# DYNAMIC RESPONSE HANDLERS
# ==========================================
# Functions for complex command logic

def handle_search_partition(game_state):
    """Handle searching the hidden partition"""
    items = ROOM_CONFIG["items"]
    
    lines = [">> Searching hidden partition..."]
    
    # Check if ghost already found
    if game_state.get_flag("ghost_found"):
        lines.append(">> The partition is empty except for ghost traces.")
        return None, lines
    
    # Random chance to find something
    if random.random() > 0.7:  # 30% chance
        game_state.set_flag("ghost_found", True)
        lines.extend([
            ">> ALERT: Anomaly detected!",
            ">> Found: Ghost Protocol v2.3",
            ">> This ancient software could bypass security...",
            ">> 'use ghost protocol' when needed."
        ])
    else:
        lines.extend([
            ">> Searching...",
            ">> Found corrupted data fragments.",
            ">> Nothing immediately useful.",
            ">> Try searching again?"
        ])
    
    return None, lines

def handle_transmit_response(cmd, game_state):
    """Handle numeric response to terminal"""
    parts = cmd.split()
    if len(parts) < 3:
        return None, [">> Syntax: transmit response [number]"]
    
    try:
        response = int(parts[2])
    except ValueError:
        return None, [">> Response must be numeric."]
    
    correct = int(ROOM_CONFIG["terminal_data"]["correct_response"])
    
    if response == correct:
        game_state.set_flag("puzzle_solved", True)
        game_state.set_flag("access_code_found", True)
        return None, [
            ">> Response accepted!",
            ">> Terminal unlocking...",
            ">> Access granted to next node.",
            ">> Item found: Access Code Fragment",
            ">> Use 'exit' to proceed to the next area."
        ]
    else:
        # Track failed attempts
        attempts = game_state.get("hack_attempts", 0) + 1
        game_state.set("hack_attempts", attempts)
        
        if attempts >= 3:
            return transition_to_room(
                ROOM_CONFIG["destinations"]["failure"],
                [
                    ">> SECURITY ALERT!",
                    ">> Too many failed attempts.",
                    ">> Initiating lockdown...",
                    ">> You're being traced!"
                ]
            )
        
        return None, [
            f">> Incorrect response. ({attempts}/3 attempts)",
            ">> The pattern awaits the correct number.",
            ">> Hint: Look at the mathematical relationship."
        ]

def handle_hack_terminal(game_state):
    """Handle terminal hacking attempt"""
    if game_state.get_flag("hack_successful"):
        return None, [">> Terminal already compromised."]
    
    lines = [
        ">> Initiating hack sequence...",
        ">> Probing security layers..."
    ]
    
    # Make it harder if they've failed the puzzle
    hack_difficulty = 0.5 if game_state.get("hack_attempts", 0) > 0 else 0.3
    
    if random.random() > hack_difficulty:
        game_state.set_flag("hack_successful", True)
        game_state.set_flag("data_shard_found", True)
        lines.extend([
            ">> SUCCESS! Security bypassed.",
            ">> Terminal memory dumped.",
            ">> Found: Corrupted Data Shard",
            ">> Alternate route available via 'ghost protocol'."
        ])
    else:
        lines.extend([
            ">> Hack failed! Security too strong.",
            ">> Terminal entering lockdown.",
            ">> Try the legitimate solution."
        ])
    
    return None, lines

def handle_status(game_state):
    """Show current room progress"""
    lines = [">> ROOM STATUS:"]
    lines.append("")
    
    # Check main progress
    if game_state.get_flag("puzzle_solved"):
        lines.append("✓ Main puzzle: COMPLETE")
    elif game_state.get_flag("signal_decoded"):
        lines.append("◐ Main puzzle: Response needed")
    elif game_state.get_flag("terminal_accessed"):
        lines.append("◐ Main puzzle: Decode signal")
    elif game_state.get_flag("area_scanned"):
        lines.append("◐ Main puzzle: Access terminal")
    else:
        lines.append("✗ Main puzzle: Not started")
    
    # Check secrets
    secrets_found = 0
    if game_state.get_flag("ghost_found"):
        secrets_found += 1
    if game_state.get_flag("data_shard_found"):
        secrets_found += 1
    if game_state.get_flag("access_code_found"):
        secrets_found += 1
    
    lines.append(f"\nSecrets found: {secrets_found}/3")
    
    # Check attempts
    attempts = game_state.get("hack_attempts", 0)
    if attempts > 0:
        lines.append(f"Failed attempts: {attempts}/3")
    
    return None, lines

def handle_hint(game_state):
    """Provide contextual hints"""
    if not game_state.get_flag("area_scanned"):
        return None, [">> HINT: Start by scanning your environment."]
    
    if not game_state.get_flag("terminal_accessed"):
        return None, [">> HINT: You've found a terminal. Try accessing it."]
    
    if not game_state.get_flag("signal_decoded"):
        return None, [">> HINT: The terminal shows a pattern. Decode it."]
    
    if game_state.get_flag("signal_decoded") and not game_state.get_flag("puzzle_solved"):
        return None, [">> HINT: The sequence is mathematical. What comes after 8?"]
    
    if game_state.get_flag("puzzle_solved"):
        return None, [">> HINT: You've solved the main puzzle. Try 'exit' or explore secrets."]
    
    return None, [">> HINT: Explore everything. Some commands reveal themselves."]

def handle_inventory(game_state):
    """Show collected items"""
    lines = [">> INVENTORY:"]
    found_any = False
    
    for item_id, item in ROOM_CONFIG["items"].items():
        if game_state.get_flag(f"{item_id}_found"):
            lines.append(f"  - {item['name']}: {item['description']}")
            found_any = True
    
    if not found_any:
        lines.append("  (empty)")
    
    return None, lines

# ==========================================
# GENERIC PUZZLE PROCESSOR
# ==========================================
# This handles most standard puzzle commands

def process_puzzle_command(cmd, game_state, puzzle_config):
    """
    Generic processor for puzzle commands.
    Handles requirements, flags, and responses.
    
    This is what makes the dictionary system work!
    """
    for action_key, action in puzzle_config.items():
        # Check if this is the right command
        if cmd == action["command"] or cmd.startswith(action["command"] + " "):
            
            # Handle dynamic responses (custom logic)
            if action.get("dynamic_response"):
                if action["command"] == "search partition":
                    return handle_search_partition(game_state)
                elif action["command"] == "transmit response":
                    return handle_transmit_response(cmd, game_state)
                elif action["command"] == "hack terminal":
                    return handle_hack_terminal(game_state)
                elif action["command"] == "status":
                    return handle_status(game_state)
                elif action["command"] == "hint":
                    return handle_hint(game_state)
                elif action["command"] == "inventory":
                    return handle_inventory(game_state)
                continue
            
            # Check requirements
            for req in action.get("requires", []):
                if not game_state.get_flag(req):
                    return None, action.get("missing_req", [">> Requirement not met."])
            
            # Check if already done (for non-transition commands)
            if "sets" in action and game_state.get_flag(action["sets"]):
                return None, action.get("already_done", [">> Already completed."])
            
            # Set flag if specified
            if "sets" in action:
                game_state.set_flag(action["sets"], True)
            
            # Handle transition
            if action.get("transition"):
                dest = ROOM_CONFIG["destinations"][action.get("transition_dest", "main")]
                return transition_to_room(dest, action["transition_msg"])
            
            # Return success message
            return None, action["success"]
    
    return None, None

# ==========================================
# ROOM ENTRY POINT
# ==========================================

def enter_room(game_state):
    """
    Called when player enters the room.
    Sets up initial state and returns entry text.
    """
    lines = ROOM_CONFIG["entry_text"].copy()
    
    # Add progression hint based on current state
    if not game_state.get_flag("area_scanned"):
        hint = ROOM_CONFIG["progression_hints"]["start"]
    elif not game_state.get_flag("terminal_accessed"):
        hint = ROOM_CONFIG["progression_hints"]["scanned"]
    elif not game_state.get_flag("signal_decoded"):
        hint = ROOM_CONFIG["progression_hints"]["terminal_accessed"]
    elif not game_state.get_flag("puzzle_solved"):
        hint = ROOM_CONFIG["progression_hints"]["signal_decoded"]
    else:
        hint = ROOM_CONFIG["progression_hints"]["complete"]
    
    lines.extend(["", hint])
    
    # Optional: Add atmospheric details
    if random.random() > 0.5:
        sound = random.choice(ROOM_CONFIG["atmosphere"]["sounds"])
        lines.append(f">> You hear {sound} in the distance.")
    
    return format_enter_lines(ROOM_CONFIG["name"], lines)

# ==========================================
# INPUT HANDLER
# ==========================================

def handle_input(cmd, game_state, room_module=None):
    """
    Main input handler - processes all player commands.
    This is called for every command the player types.
    """
    # First, check standard commands (help, inventory, etc.)
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response
    
    cmd = cmd.lower().strip()
    
    # Special case: exit command
    if cmd == "exit":
        if game_state.get_flag("puzzle_solved"):
            return transition_to_room(
                ROOM_CONFIG["destinations"]["main"],
                [
                    ">> Exit confirmed.",
                    ">> Disconnecting from whisper node...",
                    ">> Routing to next subnet..."
                ]
            )
        else:
            return None, [">> Cannot exit. Terminal still locked."]
    
    # Check all puzzle paths in order
    all_paths = [
        DISCOVERY_PATH,
        MAIN_PATH,
        ALTERNATE_PATH,
        DIAGNOSTIC_COMMANDS
    ]
    
    for puzzle_config in all_paths:
        transition, response = process_puzzle_command(cmd, game_state, puzzle_config)
        if response is not None:
            return transition, response
    
    # No matching command found
    return None, [">> Unknown command. Type 'help' for options."]

# ==========================================
# HELP SYSTEM
# ==========================================

def get_available_commands():
    """
    Returns list of available commands for help menu.
    Called when player types 'help'.
    """
    return COMMAND_DESCRIPTIONS

# ==========================================
# QUICK REFERENCE FOR MODDING
# ==========================================
"""
CREATING YOUR OWN ROOM:

1. Copy this template and rename it
2. Update ROOM_CONFIG:
   - Change name and entry_text
   - Update progression_hints
   - Modify destinations
   - Add your own data structures

3. Define your puzzle paths:
   - DISCOVERY_PATH: Initial exploration
   - MAIN_PATH: Core puzzle
   - ALTERNATE_PATH: Secrets/optional
   - Add more paths as needed

4. Each puzzle command needs:
   - "command": what player types
   - "requires": list of required flags
   - "sets": flag to set when done
   - "success": response text
   - "already_done": if repeated
   - "missing_req": if requirements not met

5. For complex commands:
   - Set "dynamic_response": True
   - Create a handler function
   - Add to process_puzzle_command

6. Room transitions:
   - Set "transition": True
   - Set "transition_dest": key from destinations
   - Set "transition_msg": transition text

TIPS:
- Use flags to track progress: game_state.get_flag() / set_flag()
- Keep puzzles logical but not too obvious
- Hide secrets for code readers
- Test all paths and edge cases
- Comment your puzzle logic

COMMON PATTERNS:

Simple command:
    "look_around": {
        "command": "look around",
        "requires": [],
        "sets": "looked_around",
        "success": [">> You see things."]
    }

Command with parameters:
    "enter_code": {
        "command": "enter code",
        "requires": ["terminal_open"],
        "dynamic_response": True
    }

Multi-step puzzle:
    Step 1: sets "step_1_done"
    Step 2: requires ["step_1_done"], sets "step_2_done"
    Step 3: requires ["step_2_done"], transition to next room
"""# SPYHVER-44: WITHIN

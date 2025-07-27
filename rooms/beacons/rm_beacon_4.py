# rooms/rm_beacon_4.py

from resources.room_utils import format_enter_lines, standard_commands, transition_to_room

# ==========================================
# SIMPLE CONFIGURATION - NO COMPLEXITY
# ==========================================

ROOM_CONFIG = {
    "name": "Beacon Node 4: Name Assembly",
    "entry_text": [
        "You enter a chamber with ancient stone tablets.",
        "Two fragments of text are carved clearly into the stone:",
        "The first tablet reads: 'BASILISK'",
        "The second tablet reads: 'KINARA'",
        "These appear to be components of a greater name..."
    ],
    
    # Next room
    "destination": "beacon_5"
}

# Simple puzzle steps
PUZZLE_STEPS = {
    "examine_tablets": {
        "command": "examine tablets",
        "requires": [],
        "sets": "b4_examined",
        "already_done": [">> You've already examined the tablets carefully."],
        "success": [
            ">> First tablet: 'BASILISK' - appears to be a primary name",
            ">> Second tablet: 'KINARA' - appears to be a surname",
            ">> These seem to form the true name when combined.",
            ">> Use 'combine names' to join them."
        ]
    },
    
    "combine_names": {
        "command": "combine names",
        "requires": ["b4_examined"],
        "sets": "b4_combined",
        "missing_req": [">> Examine the tablets first to understand what names to combine."],
        "already_done": [">> Names already combined. The true name has been revealed."],
        "success": [
            ">> Combining the ancient names...",
            ">> BASILISK + KINARA = BASILISK KINARA",
            ">> The true name resonates with power!",
            ">> Use 'speak name' to invoke the Basilisk."
        ]
    },
    
    "speak_name": {
        "command": "speak name",
        "requires": ["b4_combined"],
        "missing_req": [">> You must combine the names first."],
        "transition": True,
        "transition_msg": [
            ">> You speak the true name: 'BASILISK KINARA'",
            ">> The ancient power awakens at the sound.",
            ">> The Basilisk stirs in the digital realm...",
            ">> Beacon Node 4 complete. Advancing to final judgment..."
        ]
    }
}

# Optional commands
OPTIONAL_COMMANDS = {
    "read_first": {
        "command": "read first tablet",
        "requires": [],
        "success": [">> The first tablet clearly reads: 'BASILISK'"]
    },
    
    "read_second": {
        "command": "read second tablet", 
        "requires": [],
        "success": [">> The second tablet clearly reads: 'KINARA'"]
    },
    
    "status": {
        "command": "status",
        "requires": [],
        "dynamic_response": True
    }
}

# Command help
COMMAND_DESCRIPTIONS = [
    "examine tablets     - look closely at the stone tablets",
    "read first tablet   - read the first tablet",
    "read second tablet  - read the second tablet", 
    "combine names       - join the names into the true name",
    "speak name          - invoke the Basilisk with the true name",
    "status              - check your progress"
]

# ==========================================
# ROOM LOGIC
# ==========================================

def handle_status(game_state):
    """Show current progress"""
    lines = [">> Beacon Node 4 Status:"]
    
    if not game_state.get_flag("b4_examined"):
        lines.append("   - Tablets: Not yet examined")
        lines.append("   - Next: examine tablets")
    elif not game_state.get_flag("b4_combined"):
        lines.append("   - Tablets: ✓ Examined (BASILISK + KINARA)")
        lines.append("   - Names: Not yet combined")
        lines.append("   - Next: combine names")
    else:
        lines.append("   - Tablets: ✓ Examined")
        lines.append("   - Names: ✓ Combined (BASILISK KINARA)")
        lines.append("   - Next: speak name")
    
    return None, lines

def enter_room(game_state):
    lines = ROOM_CONFIG["entry_text"].copy()
    
    if not game_state.get_flag("b4_examined"):
        lines.append("")
        lines.append(">> Use 'examine tablets' to study the inscriptions.")
    elif not game_state.get_flag("b4_combined"):
        lines.append("")
        lines.append(">> Use 'combine names' to form the true name.")
    else:
        lines.append("")
        lines.append(">> True name revealed: BASILISK KINARA")
        lines.append(">> Use 'speak name' to complete the ritual.")
    
    return format_enter_lines(ROOM_CONFIG["name"], lines)

def handle_input(cmd, game_state, room_module=None):
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response
    
    cmd = cmd.lower().strip()
    
    # Handle status command
    if cmd == "status":
        return handle_status(game_state)
    
    # Check main puzzle steps
    for step_name, step_config in PUZZLE_STEPS.items():
        if cmd == step_config["command"]:
            # Check requirements
            for req in step_config.get("requires", []):
                if not game_state.get_flag(req):
                    return None, step_config.get("missing_req", [">> Requirement not met."])
            
            # Check if already done
            if "sets" in step_config and game_state.get_flag(step_config["sets"]):
                return None, step_config.get("already_done", [">> Already completed."])
            
            # Set flag if specified
            if "sets" in step_config:
                game_state.set_flag(step_config["sets"], True)
            
            # Handle transition
            if step_config.get("transition"):
                return transition_to_room(
                    ROOM_CONFIG["destination"], 
                    step_config["transition_msg"]
                )
            
            # Return success message
            return None, step_config["success"]
    
    # Check optional commands
    for cmd_name, cmd_config in OPTIONAL_COMMANDS.items():
        if cmd == cmd_config["command"]:
            if cmd_config.get("dynamic_response"):
                continue  # Already handled above
            return None, cmd_config["success"]
    
    return None, [">> Unknown command. Try 'help' for available options."]

def get_available_commands():
    return COMMAND_DESCRIPTIONS
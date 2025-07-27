# rooms/rm_convergence_hub.py

from resources.room_utils import format_enter_lines, standard_commands, transition_to_room

# ==========================================
# ROOM CONFIGURATION
# ==========================================

ROOM_CONFIG = {
    "name": "CONVERGENCE HUB",
    "entry_text": [
        "You emerge in the Convergence Hub.",
        "Three data conduits spiral inward, converging on a central monolith.",
        "Each conduit pulses with the signature of the path you traveled..."
    ],
    
    # Path detection messages
    "path_messages": {
        "whisper": ">> WHISPER signal detected. Trace: Synnet Substream confirmed.",
        "beacon": ">> BEACON resonance aligned. Uplink path stable.",
        "hidden": ">> HIDDEN protocol breach acknowledged. Shadow key authenticated."
    },
    
    # Progression hints
    "progression_hints": {
        "all_paths": [
            "",
            ">> All paths merged. Core systems unlocked.",
            ">> Try 'initiate awakening' to continue."
        ],
        "partial_paths": [
            "",
            ">> Not all routes converge. You may 'activate monolith' to stabilize or continue exploration."
        ],
        "no_paths": [
            "",
            ">> No active conduits detected. Explore other areas to unlock pathways."
        ]
    },
    
    # Path flag mappings - checks any of these flags for each path
    "path_flags": {
        "whisper": ["whisper_port_connected", "w2_gamma_decrypted"],
        "beacon": ["beacon_main_activated", "beacon_override"],
        "hidden": ["drift_exit_recovered", "fragment_hidden_passage"]
    },
    
    # Next room destination
    "final_room": "whisper_7",
    
    # Transition messages
    "awakening_transition": [
        ">> SIGNAL COMPLETE.",
        ">> Conscious loop aligned.",
        ">> Reality threshold breached...",
        ">> Transferring to final domain..."
    ]
}

# Command responses
COMMAND_RESPONSES = {
    "activate_monolith": {
        "no_paths": [">> Insufficient energy paths. At least one conduit must be active."],
        "success": [
            ">> Routing remaining signal strength through conduits...",
            ">> Activated paths: {paths}",
            ">> Core logic pattern forming. Additional data may be unlocked in other nodes."
        ]
    },
    
    "initiate_awakening": {
        "incomplete": [">> Core incomplete. All three conduits must be stabilized."],
        "success": ROOM_CONFIG["awakening_transition"]
    },
    
    "hub_status": {
        "header": ">> Conduit Status:",
        "path_template": "   - {path}: {status}",
        "footer": [
            "",
            ">> Activate all three to unlock the path beyond."
        ]
    }
}

# Command descriptions for help
COMMAND_DESCRIPTIONS = [
    "hub status         - check which paths are active",
    "activate monolith  - stabilize the hub with available data paths",
    "initiate awakening - unlock final domain (all paths required)"
]

# ==========================================
# PATH DETECTION LOGIC
# ==========================================

def get_path_flags(game_state):
    """Check which paths the player has completed"""
    paths = {}
    
    for path_name, flag_list in ROOM_CONFIG["path_flags"].items():
        # Path is active if ANY of its associated flags are set
        paths[path_name] = any(game_state.get_flag(flag) for flag in flag_list)
    
    return paths

def get_active_path_names(paths):
    """Get list of activated path names"""
    return [name for name, active in paths.items() if active]

# ==========================================
# COMMAND HANDLERS
# ==========================================

def handle_activate_monolith(game_state):
    """Handle the activate monolith command"""
    paths = get_path_flags(game_state)
    activated_paths = get_active_path_names(paths)
    
    if not activated_paths:
        return COMMAND_RESPONSES["activate_monolith"]["no_paths"]
    
    # Format the success message with active paths
    response = []
    for line in COMMAND_RESPONSES["activate_monolith"]["success"]:
        if "{paths}" in line:
            path_list = ', '.join(p.upper() for p in activated_paths)
            response.append(line.format(paths=path_list))
        else:
            response.append(line)
    
    return response

def handle_initiate_awakening(game_state):
    """Handle the initiate awakening command"""
    paths = get_path_flags(game_state)
    
    if not all(paths.values()):
        return None, COMMAND_RESPONSES["initiate_awakening"]["incomplete"]
    
    # Transition to final room
    return transition_to_room(
        ROOM_CONFIG["final_room"], 
        COMMAND_RESPONSES["initiate_awakening"]["success"]
    )

def handle_hub_status(game_state):
    """Display the status of all conduits"""
    paths = get_path_flags(game_state)
    
    lines = [COMMAND_RESPONSES["hub_status"]["header"]]
    
    # Add status for each path
    for path_name, is_active in paths.items():
        status = "✔" if is_active else "✘"
        line = COMMAND_RESPONSES["hub_status"]["path_template"].format(
            path=path_name.capitalize(),
            status=status
        )
        lines.append(line)
    
    # Add footer
    lines.extend(COMMAND_RESPONSES["hub_status"]["footer"])
    
    return lines

# ==========================================
# MAIN ROOM INTERFACE
# ==========================================

def enter_room(game_state):
    """Called when entering the room"""
    lines = ROOM_CONFIG["entry_text"].copy()
    paths = get_path_flags(game_state)
    
    # Add messages for each active path
    for path_name, is_active in paths.items():
        if is_active:
            lines.append(ROOM_CONFIG["path_messages"][path_name])
    
    # Add appropriate progression hint
    active_count = sum(paths.values())
    
    if active_count == 3:
        lines.extend(ROOM_CONFIG["progression_hints"]["all_paths"])
    elif active_count > 0:
        lines.extend(ROOM_CONFIG["progression_hints"]["partial_paths"])
    else:
        lines.extend(ROOM_CONFIG["progression_hints"]["no_paths"])
    
    return format_enter_lines(ROOM_CONFIG["name"], lines)

def handle_input(cmd, game_state, room_module=None):
    """Process player commands"""
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response
    
    cmd = cmd.lower().strip()
    
    # Command routing
    if cmd == "activate monolith":
        return None, handle_activate_monolith(game_state)
    
    if cmd == "initiate awakening":
        return handle_initiate_awakening(game_state)
    
    if cmd == "hub status":
        return None, handle_hub_status(game_state)
    
    return None, [">> Unknown command. Try 'hub status', 'activate monolith', or 'initiate awakening'."]

def get_available_commands():
    """Return list of available commands"""
    return COMMAND_DESCRIPTIONS
# rooms/rm_whisper_6.py

from resources.room_utils import format_enter_lines, standard_commands, transition_to_room

# ==========================================
# ROOM CONFIGURATION
# ==========================================

ROOM_CONFIG = {
    "name": "Signal Convergence Chamber",
    "entry_text": [
        "You emerge into a vast chamber where three massive conduits spiral toward the center.",
        "Your whisper signal courses through the primary conduit, but the other two remain dark.",
        "Ancient protocol fragments drift in the air like digital ghosts..."
    ],
    
    # Progression hints
    "progression_hints": {
        "initial": ">> Your whisper path pulses with life. Try 'analyze conduits' to understand this place.",
        "analyzed": ">> The other paths echo with potential. Try 'trace phantom signals'.",
        "phantoms_found": ">> Phantom protocols detected. You can 'simulate beacon' or 'simulate hidden' to explore alternate realities.",
        "simulations_ready": ">> All pathways mapped. Use 'synchronize conduits' to proceed.",
        "synchronized": ">> Conduits aligned. The way forward opens. Use 'enter core' to continue."
    },
    
    # Next room destination
    "destination": "whisper_6"
}

# Phantom protocol data - what the other paths would have been
PHANTOM_PROTOCOLS = {
    "beacon": {
        "name": "Beacon Protocol",
        "description": "Signal amplification and broadcast systems",
        "signature": "UPLINK_ACTIVE",
        "echo_fragments": [
            "// BEACON NODE MEMORY FRAGMENT //",
            "Terminal_1_Status: HACKED",
            "Terminal_2_Status: HACKED", 
            "Terminal_3_Status: HACKED",
            "Beacon_Config: READY_TO_BROADCAST",
            "Signal_Sent: TRUE",
            "// END FRAGMENT //"
        ]
    },
    "hidden": {
        "name": "Hidden Protocol", 
        "description": "Stealth infiltration and data extraction",
        "signature": "SHADOW_KEY_AUTHENTICATED",
        "echo_fragments": [
            "// HIDDEN NODE MEMORY FRAGMENT //",
            "Stealth_Mode: ACTIVE",
            "Detection_Level: 0%",
            "Shadow_Routes: MAPPED",
            "Extraction_Complete: TRUE",
            "Ghost_Exit: SUCCESSFUL",
            "// END FRAGMENT //"
        ]
    }
}

# Discovery phase commands
DISCOVERY_PATH = {
    "analyze_conduits": {
        "command": "analyze conduits",
        "requires": [],
        "sets": "convergence_analyzed",
        "already_done": [">> Conduits already analyzed. Three pathways confirmed."],
        "success": [
            ">> Conduit Analysis Complete:",
            "   - Primary: WHISPER protocol [ACTIVE - your signal]",
            "   - Secondary: BEACON protocol [DORMANT - phantom traces]", 
            "   - Tertiary: HIDDEN protocol [DORMANT - shadow echoes]",
            ">> The other paths pulse with phantom energy. Try 'trace phantom signals'."
        ]
    },
    
    "trace_phantom_signals": {
        "command": "trace phantom signals",
        "requires": ["convergence_analyzed"],
        "sets": "phantoms_traced",
        "missing_req": [">> Unknown signal patterns. Analyze conduits first."],
        "already_done": [">> Phantom signals already traced."],
        "success": [
            ">> Tracing phantom protocol signatures...",
            "   - Beacon echoes: Broadcast amplification patterns detected",
            "   - Hidden echoes: Stealth infiltration residue found",
            ">> These paths exist in quantum superposition - roads not taken.",
            ">> You can 'simulate beacon' or 'simulate hidden' to explore these realities."
        ]
    }
}

# Simulation commands - explore alternate paths
SIMULATION_PATH = {
    "simulate_beacon": {
        "command": "simulate beacon",
        "requires": ["phantoms_traced"],
        "sets": "beacon_simulated",
        "missing_req": [">> No beacon signature detected."],
        "already_done": [">> Beacon simulation already complete."],
        "dynamic_response": True
    },
    
    "simulate_hidden": {
        "command": "simulate hidden", 
        "requires": ["phantoms_traced"],
        "sets": "hidden_simulated",
        "missing_req": [">> No hidden signature detected."],
        "already_done": [">> Hidden simulation already complete."],
        "dynamic_response": True
    }
}

# Final convergence commands
CONVERGENCE_PATH = {
    "synchronize_conduits": {
        "command": "synchronize conduits",
        "requires": ["beacon_simulated", "hidden_simulated"],
        "sets": "conduits_synchronized", 
        "missing_req": [">> Cannot synchronize. Simulate all phantom protocols first."],
        "already_done": [">> Conduits already synchronized."],
        "success": [
            ">> Synchronizing all protocol pathways...",
            "   - Whisper: Your lived experience",
            "   - Beacon: Simulated broadcast reality", 
            "   - Hidden: Simulated stealth reality",
            ">> All possible paths converged into singular experience.",
            ">> Quantum superposition collapsed. The core awaits."
        ]
    },
    
    "enter_core": {
        "command": "enter core",
        "requires": ["conduits_synchronized"],
        "missing_req": [">> Core access denied. Synchronize conduits first."],
        "transition": True,
        "transition_msg": [
            ">> Entering the awakening core...",
            ">> All paths, all choices, all possibilities merge into one truth..."
        ]
    }
}

# Optional exploration commands
EXPLORATION_COMMANDS = {
    "examine_whisper": {
        "command": "examine whisper conduit",
        "requires": ["convergence_analyzed"],
        "missing_req": [">> Conduits not analyzed yet."],
        "success": [
            ">> Your whisper conduit thrums with the energy of your journey:",
            "   - Node 1: Port connection established",
            "   - Node 2: Beacon fragments collected", 
            "   - Node 3: Memory fragments recovered",
            "   - Node 4: Grid traversal successful",
            "   - Node 5: Loop chamber resolved",
            ">> This path is complete and true."
        ]
    },
    
    "examine_beacon": {
        "command": "examine beacon conduit",
        "requires": ["convergence_analyzed"],
        "missing_req": [">> Conduits not analyzed yet."],
        "success": [
            ">> The beacon conduit flickers with phantom energy:",
            "   - Faint traces of terminal hack sequences",
            "   - Echo of broadcast configuration protocols",
            "   - Residual uplink transmission patterns",
            ">> This path exists in quantum potential."
        ]
    },
    
    "examine_hidden": {
        "command": "examine hidden conduit", 
        "requires": ["convergence_analyzed"],
        "missing_req": [">> Conduits not analyzed yet."],
        "success": [
            ">> The hidden conduit barely whispers its secrets:",
            "   - Shadow traces of stealth infiltration",
            "   - Ghostly extraction protocol fragments", 
            "   - Phantom detection avoidance patterns",
            ">> This path hides in the spaces between reality."
        ]
    },
    
    "convergence_status": {
        "command": "status",
        "requires": [],
        "dynamic_response": True
    }
}

# Command descriptions for help
COMMAND_DESCRIPTIONS = [
    "analyze conduits       - examine the three protocol pathways",
    "trace phantom signals  - detect echoes from alternate paths", 
    "simulate beacon        - explore the broadcast protocol reality",
    "simulate hidden        - explore the stealth protocol reality",
    "synchronize conduits   - merge all pathways into convergence",
    "enter core             - proceed to the awakening chamber",
    "examine [type] conduit - inspect whisper/beacon/hidden conduits",
    "status                 - check convergence progress"
]

# ==========================================
# SIMULATION HANDLERS
# ==========================================

def handle_beacon_simulation(game_state):
    """Simulate the beacon protocol experience"""
    protocol = PHANTOM_PROTOCOLS["beacon"]
    lines = [
        f">> Simulating {protocol['name']}...",
        f"   {protocol['description']}",
        "",
        ">> BEACON SIMULATION ACTIVE:",
    ]
    lines.extend(protocol["echo_fragments"])
    lines.extend([
        "",
        f">> Simulation complete. Signature acquired: {protocol['signature']}"
    ])
    
    return None, lines

def handle_hidden_simulation(game_state):
    """Simulate the hidden protocol experience"""
    protocol = PHANTOM_PROTOCOLS["hidden"]
    lines = [
        f">> Simulating {protocol['name']}...",
        f"   {protocol['description']}", 
        "",
        ">> HIDDEN SIMULATION ACTIVE:",
    ]
    lines.extend(protocol["echo_fragments"])
    lines.extend([
        "",
        f">> Simulation complete. Signature acquired: {protocol['signature']}"
    ])
    
    return None, lines

def handle_status(game_state):
    """Show convergence progress"""
    lines = [">> CONVERGENCE CHAMBER STATUS:"]
    
    # Whisper path (always complete if they're here)
    lines.append("   - Whisper Protocol: ✓ COMPLETE (your path)")
    
    # Analysis status
    if game_state.get_flag("convergence_analyzed"):
        lines.append("   - Conduit Analysis: ✓ COMPLETE")
    else:
        lines.append("   - Conduit Analysis: ✗ PENDING")
        return None, lines
    
    # Phantom tracing
    if game_state.get_flag("phantoms_traced"):
        lines.append("   - Phantom Signals: ✓ TRACED")
    else:
        lines.append("   - Phantom Signals: ✗ PENDING")
        return None, lines
    
    # Simulations
    beacon_sim = "✓" if game_state.get_flag("beacon_simulated") else "✗"
    hidden_sim = "✓" if game_state.get_flag("hidden_simulated") else "✗"
    lines.append(f"   - Beacon Simulation: {beacon_sim}")
    lines.append(f"   - Hidden Simulation: {hidden_sim}")
    
    # Synchronization
    if game_state.get_flag("conduits_synchronized"):
        lines.append("   - Conduit Sync: ✓ ALIGNED")
        lines.append("")
        lines.append(">> All pathways converged. Ready to 'enter core'.")
    else:
        lines.append("   - Conduit Sync: ✗ PENDING")
    
    return None, lines

# ==========================================
# ROOM LOGIC
# ==========================================

def enter_room(game_state):
    """Called when entering the room"""
    lines = ROOM_CONFIG["entry_text"].copy()
    
    # Add progression hint based on state
    if not game_state.get_flag("convergence_analyzed"):
        lines.extend(["", ROOM_CONFIG["progression_hints"]["initial"]])
    elif not game_state.get_flag("phantoms_traced"):
        lines.append(ROOM_CONFIG["progression_hints"]["analyzed"])
    elif not (game_state.get_flag("beacon_simulated") and game_state.get_flag("hidden_simulated")):
        lines.append(ROOM_CONFIG["progression_hints"]["phantoms_found"])
    elif not game_state.get_flag("conduits_synchronized"):
        lines.append(ROOM_CONFIG["progression_hints"]["simulations_ready"])
    else:
        lines.append(ROOM_CONFIG["progression_hints"]["synchronized"])
    
    return format_enter_lines(ROOM_CONFIG["name"], lines)

def process_puzzle_command(cmd, game_state, puzzle_config):
    """Generic puzzle command processor with dynamic response support"""
    for action_key, action in puzzle_config.items():
        if cmd == action["command"]:
            # Handle dynamic responses
            if action.get("dynamic_response"):
                if action["command"] == "simulate beacon":
                    return handle_beacon_simulation(game_state)
                elif action["command"] == "simulate hidden":
                    return handle_hidden_simulation(game_state)
                elif action["command"] == "status":
                    return handle_status(game_state)
                continue
            
            # Check requirements
            for req in action.get("requires", []):
                if not game_state.get_flag(req):
                    return None, action.get("missing_req", [">> Requirement not met."])
            
            # Check if already done
            if "sets" in action and game_state.get_flag(action["sets"]):
                return None, action.get("already_done", [">> Already completed."])
            
            # Set flag if specified
            if "sets" in action:
                game_state.set_flag(action["sets"], True)
            
            # Handle transition
            if action.get("transition"):
                return transition_to_room(
                    ROOM_CONFIG["destination"], 
                    action["transition_msg"]
                )
            
            # Return success message
            return None, action["success"]
    
    return None, None

def handle_input(cmd, game_state, room_module=None):
    """Process player commands"""
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response
    
    cmd = cmd.lower().strip()
    
    # Check all puzzle paths
    all_paths = [
        DISCOVERY_PATH,
        SIMULATION_PATH, 
        CONVERGENCE_PATH,
        EXPLORATION_COMMANDS
    ]
    
    for puzzle_config in all_paths:
        transition, response = process_puzzle_command(cmd, game_state, puzzle_config)
        if response is not None:
            return transition, response
    
    return None, [">> Unknown command. Try 'help' for available options."]

def get_available_commands():
    """Return list of available commands"""
    return COMMAND_DESCRIPTIONS
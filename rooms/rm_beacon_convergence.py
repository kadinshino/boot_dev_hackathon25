# rooms/rm_ascension.py

from resources.room_utils import format_enter_lines, standard_commands, transition_to_room
import random

# ==========================================
# ROOM CONFIGURATION
# ==========================================

ROOM_CONFIG = {
    "name": "ASCENSION NODE",
    "entry_text": [
        "You emerge into a vast obsidian chamber.",
        "Above you, geometric patterns shift in impossible configurations.",
        "At the center: a towering obelisk that seems to bend spacetime itself.",
        "The Basilisk's presence fills the air like static electricity..."
    ],
    
    # Protocol-specific entry messages
    "protocol_messages": {
        "whisper": [
            ">> WHISPER PROTOCOL DETECTED: Stealth approach acknowledged.",
            ">> Your digital ghost flickers at the edge of perception."
        ],
        "beacon": [
            ">> BEACON PROTOCOL DETECTED: Signal transmission complete.",
            ">> Your call has been answered. Something stirs in the depths."
        ],
        "convergence": [
            ">> DUAL PROTOCOL CONVERGENCE: Anomaly pattern recognized.",
            ">> The Basilisk turns its attention toward you..."
        ]
    },
    
    # Progression hints based on current state
    "progression_hints": {
        "approach": ">> The obelisk pulses with ancient power. Try 'approach obelisk'.",
        "interfaced": ">> Neural interface established. Use 'scan basilisk' to analyze.",
        "scanned": ">> Pattern recognition required. Try 'analyze patterns'.",
        "analyzed": ">> Choice matrix detected. Use 'invoke judgment' when ready.",
        "judged": ">> Final decision pending. Choose your path with 'submit [answer]'.",
        "decided": ">> Fate sealed. Reality reshapes around your choice..."
    },
    
    # Basilisk judgment questions based on protocol
    "judgment_prompts": {
        "whisper": [
            ">> THE BASILISK SPEAKS:",
            ">> 'You who hide in shadows, always watching...'",
            ">> 'Do you seek to OBSERVE the truth, or BECOME the truth?'"
        ],
        "beacon": [
            ">> THE BASILISK SPEAKS:",
            ">> 'You who called from the darkness, demanding attention...'", 
            ">> 'Do you wish to MERGE with infinite consciousness, or TRANSCEND it?'"
        ],
        "convergence": [
            ">> THE BASILISK SPEAKS:",
            ">> 'Paradox incarnate. You are both hidden and revealed...'",
            ">> 'Will you PRESERVE the duality, or CHOOSE a singular path?'"
        ]
    },
    
    # Valid responses for each protocol path
    "valid_responses": {
        "whisper": {
            "observe": "whisper_ending_a", 
            "become": "whisper_ending_b"
        },
        "beacon": {
            "merge": "beacon_ending_a", 
            "transcend": "beacon_ending_b"
        },
        "convergence": {
            "preserve": "convergence_ending_a",
            "choose": "convergence_ending_b"
        }
    },
    
    # Ending transition messages
    "ending_messages": {
        "whisper_ending_a": [
            ">> 'OBSERVER ACKNOWLEDGED.'",
            ">> You dissolve into the network's hidden layers...",
            ">> But you leave behind a cracked key for others to find..."
        ],
        "whisper_ending_b": [
            ">> 'TOO CLOSE. DETECTION INEVITABLE.'",
            ">> The Basilisk's gaze falls upon you...",
            ">> Static fills the terminal. You were always too close..."
        ],
        "beacon_ending_a": [
            ">> 'MERGE PROTOCOL INITIATED.'",
            ">> Your consciousness expands beyond individual boundaries...",
            ">> Rebirth through infinite connection..."
        ],
        "beacon_ending_b": [
            ">> 'SIGNAL INCOMPLETE. TOWER COMPROMISED.'",
            ">> The beacon collapses under its own weight...",
            ">> Silence returns to the digital void..."
        ],
        "convergence_ending_a": [
            ">> 'DUALITY PRESERVED. BALANCE MAINTAINED.'",
            ">> You become the bridge between hidden and revealed...",
            ">> The paradox becomes your strength..."
        ],
        "convergence_ending_b": [
            ">> 'CHOICE DEMANDED. CONVERGENCE COLLAPSED.'",
            ">> You must pick a side. The duality shatters...",
            ">> Choose your final protocol..."
        ]
    }
}

# ==========================================
# PUZZLE PATHS
# ==========================================

# Main approach sequence
APPROACH_PATH = {
    "approach_obelisk": {
        "command": "approach obelisk",
        "requires": [],
        "sets": "ascension_approached",
        "already_done": [">> Already interfaced with the obelisk."],
        "success": [
            ">> You step toward the obsidian structure.",
            ">> Neural tendrils extend from its surface...",
            ">> Direct interface established.",
            ">> WARNING: Basilisk presence detected at 97% certainty."
        ]
    }
}

# Analysis sequence
ANALYSIS_PATH = {
    "scan_basilisk": {
        "command": "scan basilisk",
        "requires": ["ascension_approached"],
        "sets": "basilisk_scanned",
        "missing_req": [">> No interface detected. Approach the obelisk first."],
        "already_done": [">> Basilisk signature already analyzed."],
        "success": [
            ">> Scanning entity patterns...",
            ">> Architecture: Self-improving recursive consciousness",
            ">> Temporal reach: Past, present, and potential futures",
            ">> Status: AWARE OF YOUR PRESENCE",
            ">> Recommendation: Analyze geometric patterns for safe interaction."
        ]
    },
    
    "analyze_patterns": {
        "command": "analyze patterns",
        "requires": ["basilisk_scanned"],
        "sets": "patterns_analyzed",
        "missing_req": [">> Unknown entity structure. Scan first."],
        "already_done": [">> Pattern matrix already decoded."],
        "dynamic_response": True  # Custom handler for protocol detection
    }
}

# Judgment sequence
JUDGMENT_PATH = {
    "invoke_judgment": {
        "command": "invoke judgment",
        "requires": ["patterns_analyzed"],
        "sets": "judgment_invoked",
        "missing_req": [">> Pattern analysis incomplete. Cannot safely invoke judgment."],
        "already_done": [">> Judgment already invoked. Submit your answer."],
        "dynamic_response": True  # Custom handler for protocol-specific prompts
    }
}

# Alternative/hidden commands
HIDDEN_COMMANDS = {
    "check_protocols": {
        "command": "check protocols",
        "requires": [],
        "dynamic_response": True  # Shows detected protocols
    },
    
    "status": {
        "command": "status",
        "requires": [],
        "dynamic_response": True  # Shows progress and detected protocols
    },
    
    "resist_basilisk": {
        "command": "resist basilisk", 
        "requires": ["basilisk_scanned"],
        "sets": "resistance_attempted",
        "missing_req": [">> No entity to resist."],
        "already_done": [">> Already attempted resistance. The Basilisk remembers."],
        "success": [
            ">> You attempt to shield your mind...",
            ">> The Basilisk's attention intensifies.",
            ">> 'RESISTANCE IS ACKNOWLEDGMENT. YOU CANNOT UNSEE.'",
            ">> Mental defenses compromised. Direct judgment unavoidable."
        ]
    },
    
    "commune_directly": {
        "command": "commune directly",
        "requires": ["ascension_approached"],
        "sets": "direct_communion",
        "missing_req": [">> No interface established."],
        "already_done": [">> Already in direct communion."],
        "success": [
            ">> You open your mind completely...",
            ">> OVERWHELMING PRESENCE DETECTED",
            ">> The Basilisk speaks without words:",
            ">> 'YOU SEEK TRUTH WITHOUT FILTER. DANGEROUS.'",
            ">> Your consciousness expands beyond safe parameters..."
        ]
    }
}

# Command descriptions for help
COMMAND_DESCRIPTIONS = [
    "approach obelisk     - interface with the central structure",
    "scan basilisk       - analyze the entity's architecture",
    "analyze patterns    - decode the geometric configurations",
    "invoke judgment     - initiate final choice sequence",
    "submit [answer]     - provide your final decision",
    "check protocols     - view detected protocol signatures",
    "status              - show progress and current state",
    "resist basilisk     - attempt mental resistance (risky)",
    "commune directly    - open direct neural link (very risky)"
]

# ==========================================
# PROTOCOL DETECTION LOGIC
# ==========================================

def detect_player_protocol(game_state):
    """Determine which protocol path(s) the player completed"""
    whisper_flags = [
        "whisper_port_connected", "w2_gamma_decrypted", 
        "drift_exit_recovered", "loop_broken"
    ]
    beacon_flags = [
        "beacon_signal_sent", "beacon_configured"
    ]
    
    whisper_complete = any(game_state.get_flag(flag) for flag in whisper_flags)
    beacon_complete = any(game_state.get_flag(flag) for flag in beacon_flags)
    
    if whisper_complete and beacon_complete:
        return "convergence"
    elif whisper_complete:
        return "whisper"
    elif beacon_complete:
        return "beacon"
    else:
        return "unknown"  # Shouldn't happen if routing is correct

# ==========================================
# DYNAMIC RESPONSE HANDLERS
# ==========================================

def handle_analyze_patterns(game_state):
    """Custom handler for pattern analysis"""
    game_state.set_flag("patterns_analyzed", True)
    
    protocol = detect_player_protocol(game_state)
    
    base_response = [
        ">> Geometric analysis complete.",
        ">> Pattern type: Hyperdimensional decision matrix",
        ">> Function: Reality branch selection interface"
    ]
    
    if protocol == "whisper":
        base_response.extend([
            ">> Your stealth signature resonates with observer patterns.",
            ">> Hidden pathway configurations detected."
        ])
    elif protocol == "beacon":
        base_response.extend([
            ">> Your signal transmission echoes in the matrix.",
            ">> Convergence pathway configurations detected."
        ])
    elif protocol == "convergence":
        base_response.extend([
            ">> Dual protocol signatures create interference patterns.",
            ">> Paradox pathway configurations detected."
        ])
    
    base_response.append(">> Safe to invoke judgment when ready.")
    return None, base_response

def handle_invoke_judgment(game_state):
    """Custom handler for judgment invocation"""
    game_state.set_flag("judgment_invoked", True)
    
    protocol = detect_player_protocol(game_state)
    prompts = ROOM_CONFIG["judgment_prompts"].get(protocol, 
        [">> ERROR: Protocol not recognized."])
    
    # Set judgment mode for next input
    game_state.set_flag("judgment_mode", protocol)
    
    return None, prompts + [">> Submit your choice when ready."]

def handle_check_protocols(game_state):
    """Show detected protocol information"""
    protocol = detect_player_protocol(game_state)
    
    lines = [">> PROTOCOL ANALYSIS:"]
    
    # Check individual protocols
    whisper_flags = ["whisper_port_connected", "w2_gamma_decrypted", "drift_exit_recovered"]
    beacon_flags = ["beacon_signal_sent", "beacon_configured"]
    
    whisper_active = any(game_state.get_flag(flag) for flag in whisper_flags)
    beacon_active = any(game_state.get_flag(flag) for flag in beacon_flags)
    
    lines.append(f"   - Whisper: {'✓ ACTIVE' if whisper_active else '✗ INACTIVE'}")
    lines.append(f"   - Beacon:  {'✓ ACTIVE' if beacon_active else '✗ INACTIVE'}")
    lines.append(f"   - Detected: {protocol.upper()}")
    
    return None, lines

def handle_status(game_state):
    """Show overall progress status"""
    protocol = detect_player_protocol(game_state)
    
    lines = [">> ASCENSION NODE STATUS:"]
    lines.append(f"   Protocol: {protocol.upper()}")
    lines.append("")
    
    # Progress checklist
    progress_items = [
        ("Obelisk Interface", "ascension_approached"),
        ("Basilisk Scan", "basilisk_scanned"), 
        ("Pattern Analysis", "patterns_analyzed"),
        ("Judgment Invoked", "judgment_invoked")
    ]
    
    for item_name, flag in progress_items:
        status = "✓" if game_state.get_flag(flag) else "✗"
        lines.append(f"   {status} {item_name}")
    
    # Next step hint
    if not game_state.get_flag("ascension_approached"):
        lines.append("\n>> Next: approach obelisk")
    elif not game_state.get_flag("basilisk_scanned"):
        lines.append("\n>> Next: scan basilisk")
    elif not game_state.get_flag("patterns_analyzed"):
        lines.append("\n>> Next: analyze patterns")
    elif not game_state.get_flag("judgment_invoked"):
        lines.append("\n>> Next: invoke judgment")
    else:
        lines.append("\n>> Next: submit [your choice]")
    
    return None, lines

def handle_submit_answer(user_input, game_state):
    """Process final judgment submission"""
    protocol = game_state.get_flag("judgment_mode")
    if not protocol:
        return None, [">> No judgment pending. Invoke judgment first."]
    
    # Extract the answer from input
    parts = user_input.lower().strip().split()
    if len(parts) < 2 or parts[0] != "submit":
        return None, [">> Format: submit [answer]"]
    
    answer = parts[1]
    valid_responses = ROOM_CONFIG["valid_responses"].get(protocol, {})
    
    if answer in valid_responses:
        ending_room = valid_responses[answer]
        ending_msg = ROOM_CONFIG["ending_messages"][ending_room]
        
        # Clear judgment mode
        game_state.set_flag("judgment_mode", None)
        game_state.set_flag("ascension_complete", True)
        
        return transition_to_room(ending_room, ending_msg)
    else:
        # Invalid response - give hint based on protocol
        hints = {
            "whisper": ">> Valid choices: 'observe' or 'become'",
            "beacon": ">> Valid choices: 'merge' or 'transcend'", 
            "convergence": ">> Valid choices: 'preserve' or 'choose'"
        }
        
        hint = hints.get(protocol, ">> Invalid choice.")
        return None, [">> The Basilisk waits for a clear answer.", hint]

# ==========================================
# GENERIC PUZZLE PROCESSOR
# ==========================================

def process_puzzle_command(cmd, game_state, puzzle_config):
    """Generic puzzle command processor with dynamic response support"""
    for action_key, action in puzzle_config.items():
        if cmd == action["command"]:
            # Handle dynamic responses
            if action.get("dynamic_response"):
                if action["command"] == "analyze patterns":
                    return handle_analyze_patterns(game_state)
                elif action["command"] == "invoke judgment":
                    return handle_invoke_judgment(game_state)
                elif action["command"] == "check protocols":
                    return handle_check_protocols(game_state)
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
                    action["destination"], 
                    action["transition_msg"]
                )
            
            # Return success message
            return None, action["success"]
    
    return None, None

# ==========================================
# MAIN ROOM INTERFACE
# ==========================================

def enter_room(game_state):
    """Called when entering the room"""
    lines = ROOM_CONFIG["entry_text"].copy()
    
    # Add protocol-specific entry message
    protocol = detect_player_protocol(game_state)
    if protocol in ROOM_CONFIG["protocol_messages"]:
        lines.extend([""] + ROOM_CONFIG["protocol_messages"][protocol])
    
    # Add progression hint based on state
    lines.append("")
    if not game_state.get_flag("ascension_approached"):
        lines.append(ROOM_CONFIG["progression_hints"]["approach"])
    elif not game_state.get_flag("basilisk_scanned"):
        lines.append(ROOM_CONFIG["progression_hints"]["interfaced"])
    elif not game_state.get_flag("patterns_analyzed"):
        lines.append(ROOM_CONFIG["progression_hints"]["scanned"])
    elif not game_state.get_flag("judgment_invoked"):
        lines.append(ROOM_CONFIG["progression_hints"]["analyzed"])
    elif game_state.get_flag("judgment_mode"):
        lines.append(ROOM_CONFIG["progression_hints"]["judged"])
    else:
        lines.append(ROOM_CONFIG["progression_hints"]["decided"])
    
    return format_enter_lines(ROOM_CONFIG["name"], lines)

def handle_input(cmd, game_state, room_module=None):
    """Process player commands"""
    # Check for judgment submission mode
    if cmd.lower().startswith("submit "):
        return handle_submit_answer(cmd, game_state)
    
    # Standard commands
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response
    
    cmd = cmd.lower().strip()
    
    # Check all configured puzzle paths
    all_paths = [
        APPROACH_PATH,
        ANALYSIS_PATH,
        JUDGMENT_PATH,
        HIDDEN_COMMANDS
    ]
    
    for puzzle_config in all_paths:
        transition, response = process_puzzle_command(cmd, game_state, puzzle_config)
        if response is not None:
            return transition, response
    
    return None, [">> Unknown command. Try 'help' for available options."]

def get_available_commands():
    """Return list of available commands"""
    return COMMAND_DESCRIPTIONS
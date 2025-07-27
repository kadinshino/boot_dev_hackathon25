# rooms/rm_whisper_3.py

from resources.room_utils import format_enter_lines, standard_commands, transition_to_room

# ==========================================
# PUZZLE CONFIGURATION - Easy to modify!
# ==========================================

ROOM_CONFIG = {
    "name": "Drift Cache",
    "entry_text": [
        "You drift into a fragmented memory bank.",
        "Corrupted log files hover in looping recursion.",
        "Fragments of ancient programs echo names of beasts..."
    ],
    
    # Progression hints
    "progression_hints": {
        "start": ">> Residual traces detected. Try 'scan logs'.",
        "scanned": ">> Three fractured archives found. Use 'analyze corruption'.",
        "extracting": ">> {recovered}/3 fragments recovered. Continue reconstruction...",
        "all_recovered": ">> All fragments recovered. Try 'compile memories'.",
        "compiled": ">> Sequence compiled. Final step: 'connect awakening'."
    },
    
    # Next room destination
    "destination": "whisper_4",
    
    # Hints that can be revealed with 'decrypt hints'
    "progressive_hints": [
        "'B__T_' — Identity.",
        "'D_T' — The myth that kills with a glance.",
        "'D_V' — Neural exit protocol."
    ]
}

# Memory fragment puzzles - the core of this room
MEMORY_FRAGMENTS = {
    "name": {
        "archive": "PROFILE.log",
        "hint": "B__T_",
        "expected": ["BOOTS"],
        "reveal": ">> Identity reconstructed: ORTHRUS",
        "extract_commands": ["extract profile", "extract name"]
    },
    "key": {
        "archive": "SYS.log", 
        "hint": "__T",
        "expected": ["DOT"],
        "reveal": ">> Key reconstructed: BASILISK",
        "extract_commands": ["extract sys", "extract key"]
    },
    "exit": {
        "archive": "PRV.log",
        "hint": "__V",
        "expected": ["DEV"],
        "reveal": ">> Exit reconstructed: SYNNET",
        "extract_commands": ["extract prv", "extract exit"]
    }
}

# Discovery phase commands
DISCOVERY_PATH = {
    "scan_logs": {
        "command": "scan logs",
        "requires": [],
        "sets": "drift_scanned",
        "already_done": [">> Logs already scanned. Archives detected."],
        "dynamic_response": True  # Custom handler for listing archives
    },
    
    "analyze_corruption": {
        "command": "analyze corruption",
        "requires": ["drift_scanned"],
        "sets": "drift_analyzed",
        "missing_req": [">> No data. 'scan logs' first."],
        "dynamic_response": True  # Now uses dynamic handler for status
    }
}

# Fragment extraction commands (dynamically generated)
EXTRACTION_COMMANDS = {}
for key, fragment in MEMORY_FRAGMENTS.items():
    for cmd in fragment["extract_commands"]:
        EXTRACTION_COMMANDS[f"{cmd}_{key}"] = {
            "command": cmd,
            "requires": ["drift_analyzed"],
            "sets": f"drift_{key}_extracted",
            "missing_req": [">> Must analyze corruption first."],
            "already_done": [f">> {fragment['archive']} already extracted."],
            "success": [
                f">> Extracting {fragment['archive']}...",
                f"   'FRAGMENT: {fragment['hint']}'",
                f"   'DECODING REQUIRED — use reconstruct {key} [word]'."
            ]
        }

# Final assembly commands
ASSEMBLY_PATH = {
    "compile_memories": {
        "command": "compile memories",
        "requires": ["drift_name_recovered", "drift_key_recovered", "drift_exit_recovered"],
        "sets": "drift_compiled",
        "missing_req": [">> Incomplete set. Recover all first."],
        "already_done": [">> Already compiled."],
        "success": [">> Compilation complete. Final link unlocked."]
    },
    
    "connect_awakening": {
        "command": "connect awakening",
        "requires": ["drift_compiled"],
        "missing_req": [">> Compilation incomplete."],
        "transition": True,
        "transition_msg": [">> Engaging awakening protocol..."]
    }
}

# Optional hint system
HINT_SYSTEM = {
    "decrypt_hints": {
        "command": "decrypt hints",
        "requires": [],
        "dynamic_response": True  # Custom handler for progressive hints
    },
    
    "status": {
        "command": "status",
        "requires": [],
        "dynamic_response": True  # Shows current progress
    }
}

# Command descriptions for help
COMMAND_DESCRIPTIONS = [
    "scan logs            - scan for archive entries",
    "analyze corruption   - reveal corruption method",
    "extract [key]        - extract 'name', 'key', or 'exit' fragment",
    "reconstruct [key] [word] - attempt to repair fragment",
    "compile memories     - finalize all fragments",
    "connect awakening    - enter final node",
    "decrypt hints        - receive a clue",
    "status               - check fragment recovery progress"
]

# ==========================================
# ROOM LOGIC - Generic handlers below
# ==========================================

def enter_room(game_state):
    lines = ROOM_CONFIG["entry_text"].copy()
    
    # Add progression hints based on state
    if not game_state.get_flag("drift_scanned"):
        lines.extend(["", ROOM_CONFIG["progression_hints"]["start"]])
    elif not game_state.get_flag("drift_analyzed"):
        lines.append(ROOM_CONFIG["progression_hints"]["scanned"])
    else:
        # Count recovered fragments
        recovered = sum(
            game_state.get_flag(f"drift_{key}_recovered") 
            for key in MEMORY_FRAGMENTS
        )
        if recovered < 3:
            hint = ROOM_CONFIG["progression_hints"]["extracting"].format(recovered=recovered)
            lines.append(hint)
        elif not game_state.get_flag("drift_compiled"):
            lines.append(ROOM_CONFIG["progression_hints"]["all_recovered"])
        else:
            lines.append(ROOM_CONFIG["progression_hints"]["compiled"])
    
    return format_enter_lines(ROOM_CONFIG["name"], lines)


def handle_scan_logs(game_state):
    """Custom handler for scan logs command"""
    # IMPORTANT: Set the flag here since dynamic handlers bypass normal flag setting
    game_state.set_flag("drift_scanned", True)
    
    response = [">> Memory scan complete:"]
    for fragment in MEMORY_FRAGMENTS.values():
        response.append(f"   - {fragment['archive']} [corruption]")
    response.append(">> Try 'analyze corruption'.")
    return None, response


def handle_analyze_corruption(game_state):
    """Enhanced analyze handler that shows fragment status"""
    # Set analyzed flag if first time
    if not game_state.get_flag("drift_analyzed"):
        game_state.set_flag("drift_analyzed", True)
    
    response = [
        ">> Corruption pattern: Mythological obfuscation.",
        ">> Reconstruction requires context-aware decoding.",
        "",
        ">> Fragment Status:"
    ]
    
    # Show status of each fragment
    for key, fragment in MEMORY_FRAGMENTS.items():
        status = "???"
        if game_state.get_flag(f"drift_{key}_recovered"):
            status = "RECOVERED"
        elif game_state.get_flag(f"drift_{key}_extracted"):
            status = "EXTRACTED (needs reconstruction)"
        else:
            status = "NOT EXTRACTED"
        
        response.append(f"   - {fragment['archive']} [{key}]: {status}")
    
    response.extend([
        "",
        ">> Use 'extract [archive]' to begin extraction."
    ])
    
    return None, response


def handle_status(game_state):
    """Show overall progress status"""
    response = [">> DRIFT CACHE STATUS:"]
    
    # Scan status
    if not game_state.get_flag("drift_scanned"):
        response.append("   Phase: Initial scan required")
        response.append("   Next: 'scan logs'")
        return None, response
    
    # Analysis status
    if not game_state.get_flag("drift_analyzed"):
        response.append("   Phase: Archives found, analysis needed")
        response.append("   Next: 'analyze corruption'")
        return None, response
    
    # Fragment recovery status
    response.append("   Phase: Fragment recovery in progress")
    response.append("")
    
    total_recovered = 0
    for key, fragment in MEMORY_FRAGMENTS.items():
        if game_state.get_flag(f"drift_{key}_recovered"):
            response.append(f"   [{key}] {fragment['archive']}: ✓ RECOVERED")
            total_recovered += 1
        elif game_state.get_flag(f"drift_{key}_extracted"):
            response.append(f"   [{key}] {fragment['archive']}: ~ EXTRACTED (hint: {fragment['hint']})")
        else:
            response.append(f"   [{key}] {fragment['archive']}: ✗ NOT EXTRACTED")
    
    response.append("")
    response.append(f"   Progress: {total_recovered}/3 fragments recovered")
    
    # Next step hint
    if total_recovered == 3:
        if game_state.get_flag("drift_compiled"):
            response.append("   Next: 'connect awakening'")
        else:
            response.append("   Next: 'compile memories'")
    elif any(game_state.get_flag(f"drift_{key}_extracted") and not game_state.get_flag(f"drift_{key}_recovered") 
             for key in MEMORY_FRAGMENTS):
        response.append("   Next: reconstruct extracted fragments")
    else:
        response.append("   Next: extract remaining fragments")
    
    return None, response


def handle_decrypt_hints(game_state):
    """Progressive hint system"""
    hints_used = game_state.get("drift_hints_given", 0)
    available_hints = ROOM_CONFIG["progressive_hints"]
    
    if hints_used >= len(available_hints):
        return None, [">> No more hints available."]
    
    game_state.set("drift_hints_given", hints_used + 1)
    return None, [f">> Hint {hints_used + 1}: {available_hints[hints_used]}"]


def handle_reconstruct_command(cmd, game_state):
    """Handle reconstruction attempts for fragments"""
    parts = cmd.split()
    if len(parts) < 3 or parts[0] != "reconstruct":
        return None, None
    
    key = parts[1]
    attempt = " ".join(parts[2:]).upper().replace(" ", "")
    
    if key not in MEMORY_FRAGMENTS:
        return None, [">> Unknown fragment type. Use 'name', 'key', or 'exit'."]
    
    if not game_state.get_flag(f"drift_{key}_extracted"):
        return None, [">> No data extracted for this fragment."]
    
    if game_state.get_flag(f"drift_{key}_recovered"):
        return None, [">> Already reconstructed."]
    
    fragment = MEMORY_FRAGMENTS[key]
    expected_normalized = [x.replace(" ", "") for x in fragment["expected"]]
    
    if attempt in expected_normalized:
        game_state.set_flag(f"drift_{key}_recovered", True)
        return None, [
            fragment["reveal"],
            f">> Memory fragment ({key}) recovered."
        ]
    
    return None, [f">> '{attempt}' is incorrect. Try again."]


def process_puzzle_command(cmd, game_state, puzzle_config):
    """Generic puzzle command processor with dynamic response support"""
    for action_key, action in puzzle_config.items():
        if cmd == action["command"]:
            # Handle dynamic responses
            if action.get("dynamic_response"):
                if action["command"] == "scan logs":
                    return handle_scan_logs(game_state)
                elif action["command"] == "decrypt hints":
                    return handle_decrypt_hints(game_state)
                elif action["command"] == "analyze corruption":
                    return handle_analyze_corruption(game_state)
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
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response
    
    cmd = cmd.lower().strip()
    
    # Check reconstruction commands first (they have variable format)
    if cmd.startswith("reconstruct "):
        transition, response = handle_reconstruct_command(cmd, game_state)
        if response is not None:
            return transition, response
    
    # Check all configured puzzle paths
    all_paths = [
        DISCOVERY_PATH,
        EXTRACTION_COMMANDS,
        ASSEMBLY_PATH,
        HINT_SYSTEM
    ]
    
    for puzzle_config in all_paths:
        transition, response = process_puzzle_command(cmd, game_state, puzzle_config)
        if response is not None:
            return transition, response
    
    return None, [">> Unknown command. Type 'help'."]


def get_available_commands():
    return COMMAND_DESCRIPTIONS
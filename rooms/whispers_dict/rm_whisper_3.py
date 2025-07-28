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
}

# Memory fragment puzzles - now with better hints and context
MEMORY_FRAGMENTS = {
    "identity": {
        "archive": "PROFILE.log",
        "corrupted": "B__T_S",
        "clues": [
            "Fragment 1: 'System booted from /dev/null'",
            "Fragment 2: 'Username: sysAdmin, Terminal: dev'", 
            "Fragment 3: 'Identity signature: BOOTS'"
        ],
        "solution": "BOOTS",
        "reveal": ">> Identity reconstructed: BOOTS - The ghost in the machine",
        "extract_commands": ["extract profile", "extract identity"]
    },
    "creature": {
        "archive": "BEAST.log", 
        "corrupted": "_RT_RU_",
        "clues": [
            "Fragment 1: 'Two-headed guardian of the underworld'",
            "Fragment 2: 'ORTH-*** protocol detected'",
            "Fragment 3: 'Cerberus sibling designation: ORTHRUS'"
        ],
        "solution": "ORTHRUS",
        "reveal": ">> Creature identified: ORTHRUS - The dual-headed watchdog",
        "extract_commands": ["extract beast", "extract creature"]
    },
    "protocol": {
        "archive": "EXIT.log",
        "corrupted": "B___L__K",
        "clues": [
            "Fragment 1: 'Gaze upon it and turn to stone'",
            "Fragment 2: 'Mythical serpent, death by sight'",
            "Fragment 3: 'Security protocol: BASILISK engaged'"
        ],
        "solution": "BASILISK",
        "reveal": ">> Exit protocol recovered: BASILISK - The killing gaze",
        "extract_commands": ["extract exit", "extract protocol"]
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
        "dynamic_response": True  # Shows corruption patterns
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
            "dynamic_response": True  # Custom handler for extraction
        }

# Fragment examination commands
EXAMINATION_COMMANDS = {
    "examine_fragments": {
        "command": "examine fragments",
        "requires": [],
        "dynamic_response": True  # Shows extracted fragments with clues
    },
    
    "decode_hints": {
        "command": "decode hints",
        "requires": ["drift_analyzed"],
        "dynamic_response": True  # Progressive hint system
    }
}

# Final assembly commands
ASSEMBLY_PATH = {
    "compile_memories": {
        "command": "compile memories",
        "requires": ["drift_identity_recovered", "drift_creature_recovered", "drift_protocol_recovered"],
        "sets": "drift_compiled",
        "missing_req": [">> Incomplete set. Recover all fragments first."],
        "already_done": [">> Already compiled."],
        "success": [
            ">> Memory compilation complete.",
            ">> BOOTS.DEV authenticated.",
            ">> ORTHRUS protocol recognized.",
            ">> BASILISK clearance granted.",
            ">> Final link unlocked."
        ]
    },
    
    "connect_awakening": {
        "command": "connect awakening",
        "requires": ["drift_compiled"],
        "missing_req": [">> Compilation incomplete."],
        "transition": True,
        "transition_msg": [">> Engaging awakening protocol..."]
    }
}

# Command descriptions for help
COMMAND_DESCRIPTIONS = [
    "scan logs            - scan for archive entries",
    "analyze corruption   - reveal corruption patterns",
    "extract [archive]    - extract 'identity', 'creature', or 'protocol' fragment",
    "examine fragments    - view extracted fragments and their clues",
    "reconstruct [type] [word] - attempt to repair fragment",
    "decode hints         - get additional hints for current fragments",
    "compile memories     - finalize all fragments",
    "connect awakening    - enter final node",
    "status               - check overall progress"
]

# ==========================================
# ROOM LOGIC - Enhanced handlers
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
    game_state.set_flag("drift_scanned", True)
    
    response = [">> Memory scan complete:"]
    for key, fragment in MEMORY_FRAGMENTS.items():
        response.append(f"   - {fragment['archive']} [corrupted: {fragment['corrupted']}]")
    response.extend([
        "",
        ">> Corruption type: Mythological cipher with missing characters.",
        ">> Try 'analyze corruption' for deeper inspection."
    ])
    return None, response


def handle_analyze_corruption(game_state):
    """Enhanced analyze handler that provides context"""
    if not game_state.get_flag("drift_analyzed"):
        game_state.set_flag("drift_analyzed", True)
    
    response = [
        ">> Corruption analysis complete:",
        ">> Pattern: Each file contains fragmented memories.",
        ">> Recovery method: Extract files, then examine clues to reconstruct.",
        "",
        ">> Archive Status:"
    ]
    
    for key, fragment in MEMORY_FRAGMENTS.items():
        if game_state.get_flag(f"drift_{key}_recovered"):
            status = f"✓ RECOVERED: {fragment['solution']}"
        elif game_state.get_flag(f"drift_{key}_extracted"):
            status = f"~ EXTRACTED: {fragment['corrupted']} (use 'examine fragments')"
        else:
            status = "✗ NOT EXTRACTED"
        
        response.append(f"   - {fragment['archive']} [{key}]: {status}")
    
    response.extend([
        "",
        ">> Use 'extract [type]' where type is: identity, creature, or protocol"
    ])
    
    return None, response


def handle_extract_command(cmd, game_state):
    """Handle extraction with immediate clue display"""
    # Find which fragment this extraction is for
    fragment_key = None
    for key, fragment in MEMORY_FRAGMENTS.items():
        if cmd in fragment["extract_commands"]:
            fragment_key = key
            break
    
    if not fragment_key:
        return None, None
    
    # Check if already extracted
    if game_state.get_flag(f"drift_{fragment_key}_extracted"):
        return None, [f">> {MEMORY_FRAGMENTS[fragment_key]['archive']} already extracted."]
    
    # Extract and show first clue
    game_state.set_flag(f"drift_{fragment_key}_extracted", True)
    fragment = MEMORY_FRAGMENTS[fragment_key]
    
    response = [
        f">> Extracting {fragment['archive']}...",
        f">> Corrupted data: {fragment['corrupted']}",
        "",
        ">> Memory fragments found:",
        f"   {fragment['clues'][0]}",
        "",
        f">> Use 'examine fragments' for all clues,",
        f">> or 'reconstruct {fragment_key} [word]' when ready."
    ]
    
    return None, response


def handle_examine_fragments(game_state):
    """Show all extracted fragments with their clues"""
    response = [">> EXTRACTED MEMORY FRAGMENTS:"]
    found_any = False
    
    for key, fragment in MEMORY_FRAGMENTS.items():
        if game_state.get_flag(f"drift_{key}_extracted"):
            found_any = True
            status = "RECOVERED" if game_state.get_flag(f"drift_{key}_recovered") else "CORRUPTED"
            response.extend([
                "",
                f"[{key.upper()}] {fragment['archive']} - {status}",
                f"Pattern: {fragment['corrupted']}"
            ])
            
            if not game_state.get_flag(f"drift_{key}_recovered"):
                response.append("Clues:")
                for clue in fragment["clues"]:
                    response.append(f"  - {clue}")
    
    if not found_any:
        response.append("   No fragments extracted yet.")
    else:
        response.extend([
            "",
            ">> Use 'reconstruct [type] [word]' to repair corrupted fragments."
        ])
    
    return None, response


def handle_decode_hints(game_state):
    """Progressive hint system that gives specific guidance"""
    hints_given = game_state.get("drift_hints_given", 0)
    
    # Build custom hints based on current state
    hints = []
    
    for key, fragment in MEMORY_FRAGMENTS.items():
        if game_state.get_flag(f"drift_{key}_extracted") and not game_state.get_flag(f"drift_{key}_recovered"):
            if key == "identity":
                hints.append("The identity combines a footwear item with a developer's domain...")
            elif key == "creature":
                hints.append("This two-headed beast shares its name with Cerberus's sibling...")
            elif key == "protocol":
                hints.append("The serpent whose gaze turns victims to stone...")
    
    if not hints:
        hints = ["All available fragments have been decoded, or none have been extracted."]
    
    if hints_given >= len(hints):
        return None, [">> No more hints available for current fragments."]
    
    game_state.set("drift_hints_given", hints_given + 1)
    return None, [f">> Hint: {hints[hints_given % len(hints)]}"]


def handle_reconstruct_command(cmd, game_state):
    """Handle reconstruction attempts for fragments"""
    parts = cmd.split()
    if len(parts) < 3 or parts[0] != "reconstruct":
        return None, None
    
    fragment_type = parts[1]
    attempt = " ".join(parts[2:]).upper().replace(" ", "")
    
    if fragment_type not in MEMORY_FRAGMENTS:
        return None, [">> Unknown fragment type. Use 'identity', 'creature', or 'protocol'."]
    
    if not game_state.get_flag(f"drift_{fragment_type}_extracted"):
        return None, [">> No data extracted for this fragment."]
    
    if game_state.get_flag(f"drift_{fragment_type}_recovered"):
        return None, [">> Already reconstructed."]
    
    fragment = MEMORY_FRAGMENTS[fragment_type]
    
    # Check solution (case insensitive, ignore spaces/punctuation)
    solution_normalized = fragment["solution"].upper().replace(" ", "").replace(".", "")
    
    if attempt == solution_normalized:
        game_state.set_flag(f"drift_{fragment_type}_recovered", True)
        return None, [
            fragment["reveal"],
            f">> Memory fragment ({fragment_type}) recovered successfully."
        ]
    
    # Provide feedback on close attempts
    if fragment_type == "identity" and "BOOTS" in attempt:
        return None, [">> Partial match detected. Check the full designation..."]
    elif fragment_type == "creature" and "ORTH" in attempt:
        return None, [">> Close! This beast has a specific Greek name..."]
    elif fragment_type == "protocol" and "BASI" in attempt:
        return None, [">> Almost there! Complete the mythical creature's name..."]
    
    return None, [f">> '{attempt}' is incorrect. Re-examine the clues."]


def handle_status(game_state):
    """Show overall progress status"""
    response = [">> DRIFT CACHE STATUS:"]
    
    # Scan status
    if not game_state.get_flag("drift_scanned"):
        response.extend([
            "   Phase: Initial scan required",
            "   Next: 'scan logs'"
        ])
        return None, response
    
    # Analysis status
    if not game_state.get_flag("drift_analyzed"):
        response.extend([
            "   Phase: Archives found, analysis needed",
            "   Next: 'analyze corruption'"
        ])
        return None, response
    
    # Fragment recovery status
    response.append("   Phase: Fragment recovery in progress")
    response.append("")
    
    total_recovered = 0
    for key, fragment in MEMORY_FRAGMENTS.items():
        if game_state.get_flag(f"drift_{key}_recovered"):
            response.append(f"   [{key}] {fragment['archive']}: ✓ {fragment['solution']}")
            total_recovered += 1
        elif game_state.get_flag(f"drift_{key}_extracted"):
            response.append(f"   [{key}] {fragment['archive']}: ~ Extracted (pattern: {fragment['corrupted']})")
        else:
            response.append(f"   [{key}] {fragment['archive']}: ✗ Not extracted")
    
    response.append(f"\n   Progress: {total_recovered}/3 fragments recovered")
    
    # Next step hint
    if total_recovered == 3:
        if game_state.get_flag("drift_compiled"):
            response.append("   Next: 'connect awakening'")
        else:
            response.append("   Next: 'compile memories'")
    elif any(game_state.get_flag(f"drift_{key}_extracted") and not game_state.get_flag(f"drift_{key}_recovered") 
             for key in MEMORY_FRAGMENTS):
        response.append("   Next: examine fragments and reconstruct")
    else:
        response.append("   Next: extract remaining fragments")
    
    return None, response


def process_puzzle_command(cmd, game_state, puzzle_config):
    """Generic puzzle command processor with dynamic response support"""
    for action_key, action in puzzle_config.items():
        if cmd == action["command"]:
            # Handle dynamic responses
            if action.get("dynamic_response"):
                if action["command"] == "scan logs":
                    return handle_scan_logs(game_state)
                elif action["command"] == "analyze corruption":
                    return handle_analyze_corruption(game_state)
                elif action["command"] == "examine fragments":
                    return handle_examine_fragments(game_state)
                elif action["command"] == "decode hints":
                    return handle_decode_hints(game_state)
                elif action["command"] == "status":
                    return handle_status(game_state)
                elif cmd in [ec["command"] for ec in EXTRACTION_COMMANDS.values()]:
                    return handle_extract_command(cmd, game_state)
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
        EXAMINATION_COMMANDS,
        ASSEMBLY_PATH
    ]
    
    for puzzle_config in all_paths:
        transition, response = process_puzzle_command(cmd, game_state, puzzle_config)
        if response is not None:
            return transition, response
    
    return None, [">> Unknown command. Type 'help'."]


def get_available_commands():
    return COMMAND_DESCRIPTIONS
# SPYHVER-39: WHEN

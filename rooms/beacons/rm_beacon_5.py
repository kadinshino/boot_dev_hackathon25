from resources.room_utils import format_enter_lines, standard_commands, transition_to_room
import random

ROOM_NAME = "Whisper Node 5"

# Correct signal pattern (can be randomized or static)
CORRECT_PATTERN = ["static", "burst", "static"]

# All valid signal segments
VALID_SEGMENTS = ["static", "burst", "tone", "hiss", "ping"]

def enter_room(game_state):
    lines = [
        "You descend into a volatile inspection chamber.",
        "Pulses of static beat like a drum — a watchdog AI scans for mismatched signals.",
        "To pass, you must inject a noise pattern that blends into its rhythm."
    ]
    
    if not game_state.get_flag("w5_scanned"):
        lines.append("")
        lines.append(">> Try 'scan noise' to analyze the signal environment.")
    elif not game_state.get_flag("w5_solved"):
        lines.append(">> Use 'inject [pattern]' to spoof the signal (e.g., inject static-burst-hiss).")
    else:
        lines.append(">> Signal bypass achieved. Use 'proceed' to continue.")

    return format_enter_lines(ROOM_NAME, lines)

def handle_input(cmd, game_state, room_module=None):
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response
    
    cmd_lower = cmd.strip().lower()
    
    # Step 1: Scan the noise pattern
    if cmd_lower == "scan noise":
        game_state.set_flag("w5_scanned", True)
        pattern_hint = ", ".join(CORRECT_PATTERN).upper()
        return None, [
            ">> Rhythm analyzer active...",
            f">> Watchdog pulse pattern detected: {pattern_hint}",
            ">> Use 'inject [pattern]' to spoof the rhythm (e.g., inject burst-tone-hiss)",
            f">> Valid segments: {', '.join(VALID_SEGMENTS)}"
        ]
    
    # Step 2: Inject a signal pattern
    if cmd_lower.startswith("inject "):
        if not game_state.get_flag("w5_scanned"):
            return None, [">> No signal context. Use 'scan noise' first."]

        pattern = cmd_lower[7:].strip().split("-")
        if len(pattern) != 3:
            return None, [">> Invalid format. Use: inject segment1-segment2-segment3"]

        for seg in pattern:
            if seg not in VALID_SEGMENTS:
                return None, [f">> Invalid segment '{seg}'. Valid: {', '.join(VALID_SEGMENTS)}"]

        correct = sum(1 for i in range(3) if pattern[i] == CORRECT_PATTERN[i])
        
        if correct == 3:
            game_state.set_flag("w5_solved", True)
            return None, [
                ">> Signal accepted. AI watchdog deceived.",
                ">> Proceeding unlocked. Type 'proceed' to continue."
            ]
        else:
            return None, [f">> Signal rejected. {correct}/3 segments aligned correctly."]
    
    # Optional: Give hint
    if cmd_lower == "hint":
        if not game_state.get_flag("w5_scanned"):
            return None, [">> No data to analyze. Try 'scan noise' first."]
        
        random_index = random.randint(0, 2)
        segment = CORRECT_PATTERN[random_index]
        return None, [f">> Hint: Segment {random_index + 1} is '{segment.upper()}'."]
    
    # Step 3: Proceed to next room
    if cmd_lower == "proceed":
        if not game_state.get_flag("w5_solved"):
            return None, [">> Cannot proceed. The signal has not been aligned."]
        
        return transition_to_room("beacon_convergence", [
            ">> You slip past the watchdog unnoticed...",
            ">> The chamber opens to a deeper system layer."
        ])
    
    # Remind user
    if cmd_lower in ["help", "signal help", "pattern help"]:
        return None, [
            ">> Commands:",
            "   scan noise       - analyze the signal environment",
            "   inject [pattern] - attempt to blend with the AI rhythm",
            "   hint             - get a clue about one correct segment",
            "   proceed          - move to next node (after success)",
            "",
            f"Valid segments: {', '.join(VALID_SEGMENTS)}",
            "Example: inject static-burst-static"
        ]
    
    return None, [">> Unknown command. Type 'help' for options."]

def get_available_commands():
    return [
        "scan noise        - analyze the signal environment",
        "inject [pattern]  - attempt to match the AI signal",
        "hint              - get a hint for one correct segment",
        "proceed           - continue after solving the puzzle",
        "help              - list available commands"
    ]

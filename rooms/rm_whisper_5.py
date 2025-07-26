from resources.room_utils import format_enter_lines, standard_commands, transition_to_room

# Constants for puzzle configuration
LOOP_SEQUENCE = ["init loop", "trace echo", "decode loop", "break loop"]
LOOP_HINTS = {
    "init loop": "The echo begins when you initialize...",
    "trace echo": "Something’s repeating. Trace it.",
    "decode loop": "Can you understand the pattern?",
    "break loop": "Break free."
}
LOOP_FLAG_ORDER = [
    "loop_init", "loop_traced", "loop_decoded", "loop_broken"
]

def enter_room(game_state):
    lines = [
        "You materialize in a digital resonance chamber.",
        "A high-frequency logic loop is running out of control.",
        "Signal fragments distort reality around you..."
    ]

    if not game_state.get_flag("loop_init"):
        lines.append("")
        lines.append(">> You feel caught in repetition. Try 'init loop'.")
    elif not game_state.get_flag("loop_traced"):
        lines.append(">> Loop repeating... Consider 'trace echo'.")
    elif not game_state.get_flag("loop_decoded"):
        lines.append(">> You sense a logic structure. Try 'decode loop'.")
    elif not game_state.get_flag("loop_broken"):
        lines.append(">> Loop integrity weakening... Try 'break loop'.")
    else:
        lines.append(">> LOOP TERMINATED.")
        lines.append(">> Output stabilized. Use 'exit loop' to proceed.")

    return format_enter_lines("LOOP CHAMBER", lines)

def handle_input(cmd, game_state, room_module=None):
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response

    cmd = cmd.lower().strip()

    if cmd in LOOP_SEQUENCE:
        flag = LOOP_FLAG_ORDER[LOOP_SEQUENCE.index(cmd)]
        if game_state.get_flag(flag):
            return None, [f">> '{cmd}' already completed."]
        # Check prerequisites
        prereq_index = LOOP_SEQUENCE.index(cmd) - 1
        if prereq_index >= 0 and not game_state.get_flag(LOOP_FLAG_ORDER[prereq_index]):
            hint = LOOP_HINTS[LOOP_SEQUENCE[prereq_index]]
            return None, [f">> Sequence error. Hint: {hint}"]
        game_state.set_flag(flag, True)
        return None, [f">> '{cmd}' successful. {LOOP_HINTS[cmd]}"]
    
    if cmd == "exit loop":
        if not game_state.get_flag("loop_broken"):
            return None, [">> Loop still active. Break it first."]
        return transition_to_room("convergence_hub", [">> Loop dissolved. You surge forward into converged pathways..."])

    if cmd == "loop status":
        lines = []
        for i, flag in enumerate(LOOP_FLAG_ORDER):
            status = "✔" if game_state.get_flag(flag) else "✘"
            lines.append(f"{LOOP_SEQUENCE[i].ljust(15)} - {status}")
        return None, [">> Loop Sequence Status:"] + lines

    return None, [">> Unknown command. Try 'loop status' or follow the sequence."]

def get_available_commands():
    return [
        "init loop       - initialize logic anomaly",
        "trace echo      - identify repetition patterns",
        "decode loop     - understand the logical structure",
        "break loop      - escape the looping sequence",
        "exit loop       - exit once loop is broken",
        "loop status     - show your progress through the loop"
    ]

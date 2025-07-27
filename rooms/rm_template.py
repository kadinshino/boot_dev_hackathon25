# Template Room Example
from resources.room_utils import format_enter_lines, standard_commands, transition_to_room
# from puzzles.fragment_reconstruction import handle_fragment_puzzle  # Example external puzzle

ROOM_CONFIG = {
    "name": "Template Node",
    "entry_text": [
        "You stand before a glowing terminal suspended in a void of shifting data.",
        "Commands ripple across the surface like waves—waiting to be deciphered."
    ],
    "hints": {
        "start": ">> Try 'scan terminal' to begin analysis.",
        "scanned": ">> Analysis complete. Use 'extract fragment [id]' to continue.",
        "solved": ">> All fragments recovered. Try 'compile data'."
    },
    "required_flags": [
        "template_scanned",
        "template_fragment_a",
        "template_fragment_b"
    ],
    "puzzle_type": "fragment_reconstruction",
}

def enter_room(game_state):
    return format_enter_lines(ROOM_CONFIG["name"], ROOM_CONFIG["entry_text"])

def handle_input(cmd, game_state, room_module=None):
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response

    # Puzzle routing
    if ROOM_CONFIG["puzzle_type"] == "fragment_reconstruction":
        return handle_fragment_puzzle(cmd, game_state, prefix="template")

    return None, [">> Unknown command. Type 'help' for available options."]

def get_available_commands():
    return [
        "scan terminal         - begin scanning for data fragments",
        "extract fragment [id] - recover a data segment",
        "compile data          - finalize recovery",
        "help                  - list commands"
    ]

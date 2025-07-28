# rooms/rm_custom_entry.py
"""
CUSTOM ARGS ENTRY - Community/Dev Launchpad
Lets users explore template demos or auto-run first valid custom room
"""

import os
from resources.room_utils import format_enter_lines, transition_to_room

# Constants
ROOMS_DIR = "rooms"
CUSTOM_PREFIX = "rm_custom_"
ENTRY_EXCLUDE = ["rm_custom_entry.py"]

def enter_room(game_state):
    return format_enter_lines("Custom ARGS Gateway", [
        ">> You’ve entered the parallel shell.",
        ">> This node contains development demos and community extensions.",
        "",
        "Available pathways:",
        " - dict_demo      → Explore dictionary-based template",
        " - oop_demo       → Explore object-oriented template",
        " - run custom     → Auto-launch first community ARG module",
        "",
        "To contribute: name your file like 'rm_custom_<name>.py'.",
        "The engine will load the first alphabetical match after 'entry'."
    ])


def handle_input(cmd, game_state, room_module=None):
    if cmd == "dict_demo":
        return transition_to_room("template_dict_demo", [
            ">> Initializing dictionary-based template experience..."
        ])
    elif cmd == "oop_demo":
        return transition_to_room("template_oop_demo", [
            ">> Booting object-oriented demo room..."
        ])
    elif cmd == "run custom":
        target = _find_first_custom_entry()
        if target:
            return transition_to_room(target, [f">> Launching community ARG: {target}"])
        else:
            return None, [">> No custom entry files found. Please add a file to /rooms starting with 'rm_custom_'."]

    return None, [">> Unknown command. Try: dict_demo, oop_demo, or run custom"]


def get_available_commands():
    return [
        "dict_demo - Enter the dictionary-style demo room",
        "oop_demo - Enter the object-oriented demo room",
        "run custom - Launch first available mod ARG"
    ]


# ========================================
# Custom Room Search Logic
# ========================================
def _find_first_custom_entry():
    """
    Returns the first rm_custom_*.py room file (excluding rm_custom_entry.py)
    with a matching room transition name (e.g., rm_custom_foo → custom_foo)
    """
    try:
        files = sorted([
            f for f in os.listdir(ROOMS_DIR)
            if f.startswith(CUSTOM_PREFIX) and f.endswith(".py") and f not in ENTRY_EXCLUDE
        ])
        if not files:
            return None
        # Get the first room filename, strip prefix + .py
        filename = files[0]
        return filename.replace(".py", "").replace("rm_", "")
    except Exception as e:
        print(f"[DEBUG] Failed to locate custom entry: {e}")
        return None

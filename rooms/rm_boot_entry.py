# rooms/rm_boot.py
"""
BOOT SECTOR - Shared entry room for Whisper and Beacon protocol paths
Handles:
- Player handle setup
- Protocol choice
- Routes into whisper_1, beacon_1, or custom_entry
"""

from utils.room_utils import format_enter_lines, transition_to_room

# =============================
# Constants
# =============================
PROTOCOL_FLAG = "protocol"
PROTOCOL_CHOSEN_FLAG = "protocol_selected"
VALID_PROTOCOLS = ["whisper", "beacon", "custom_args"]

# =============================
# Entry Point
# =============================
def enter_room(game_state):
    name = game_state.player_name

    # 1. Ask for handle if not set
    if not name:
        return _prompt_for_handle()

    # 2. Present protocol selection if not chosen
    if not game_state.get_flag(PROTOCOL_CHOSEN_FLAG):
        return _present_protocol_options(name)

    # 3. Auto-forward to selected protocol entry
    protocol = game_state.get_flag(PROTOCOL_FLAG)
    if protocol == "whisper":
        return transition_to_room("whisper_1", [">> Whisper Protocol re-engaged."])
    elif protocol == "beacon":
        return transition_to_room("beacon_1", [">> Beacon Protocol re-engaged."])
    elif protocol == "custom_args":
        return transition_to_room("custom_entry", [">> Launching Custom ARGS shell..."])

    return [">> Protocol error. Resetting boot sector..."]


# =============================
# Input Handler
# =============================
def handle_input(user_input, game_state, room_module=None):
    cmd = user_input.strip().lower()

    # Set name
    if cmd.startswith("set name "):
        return _handle_set_name(cmd, game_state)

    # Require handle first
    if not game_state.player_name:
        return None, [">> Please set your handle using: set name <your-handle>"]

    # Choose protocol
    if not game_state.get_flag(PROTOCOL_CHOSEN_FLAG):
        return _handle_protocol_selection(cmd, game_state)

    return None, [">> Protocol already selected. Proceed to the next node."]


# =============================
# Helpers: Prompts
# =============================
def _prompt_for_handle():
    return format_enter_lines("Boot Sector", [
        "SYSTEM BOOT COMPLETE...",
        ">> IDENTITY REQUIRED: Enter your handle (e.g., ghost, zero, networm)",
        "Type: set name <your-handle>"
    ])


def _present_protocol_options(name):
    return format_enter_lines("Protocol Selection", [
        f">> Welcome, {name}.",
        ">> You have accessed a dormant node.",
        ">> Three protocols remain operational...",
        "",
        "    (1) Whisper Protocol    — [Undetected Observation]",
        "    (2) Beacon Protocol     — [Signal Initiation Detected]",
        "    (3) Custom ARGS         — [Experimental access mode]",
        "",
        ">> Choose protocol: 'whisper', 'beacon', or 'custom_args'"
    ])


# =============================
# Helpers: Command Handlers
# =============================
def _handle_set_name(cmd, game_state):
    name = cmd.replace("set name", "").strip()
    if name:
        game_state.player_name = name
        response = [f">> Handle set to '{name}'."]
        response.extend(_present_protocol_options(name))
        return None, response
    else:
        return None, [">> Invalid handle. Try again."]


def _handle_protocol_selection(cmd, game_state):
    if cmd in VALID_PROTOCOLS:
        game_state.set_flag(PROTOCOL_CHOSEN_FLAG, True)
        game_state.set_flag(PROTOCOL_FLAG, cmd)

        if cmd == "whisper":
            return "whisper_1", [">> Whisper Protocol engaged. You fade into the stream..."]
        elif cmd == "beacon":
            return "beacon_1", [">> Beacon Protocol active. You call something from the dark..."]
        elif cmd == "custom_args":
            return "custom_entry", [">> Launching custom ARGS shell..."]

    return None, [">> Unknown protocol. Type 'whisper', 'beacon', or 'custom_args'."]

# SPYHVER-27: MATRICES

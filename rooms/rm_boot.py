# rooms/rm_boot.py
"""
BOOT SECTOR - Shared entry room for Whisper and Beacon protocol paths
Handles:
- Player handle setup
- Protocol choice
- Routes into whisper_1 or beacon_1
"""

from resources.room_utils import format_enter_lines

# =============================
# Constants
# =============================
PROTOCOL_FLAG = "protocol"
PROTOCOL_CHOSEN_FLAG = "protocol_selected"
VALID_PROTOCOLS = ["whisper", "beacon","system_hub"]

# =============================
# Entry Point
# =============================
def enter_room(game_state):
    name = game_state.player_name

    if not name:
        return _prompt_for_handle()

    if not game_state.get_flag(PROTOCOL_CHOSEN_FLAG):
        return _present_protocol_options(name)

    return [">> Protocol already chosen. Proceed with caution..."]

# =============================
# Input Handler
# =============================
def handle_input(user_input, game_state, room_module=None):

    cmd = user_input.strip().lower()

    if cmd.startswith("set name "):
        return _handle_set_name(cmd, game_state)

    if not game_state.player_name:
        return None, [">> Please set your handle using: set name <your-handle>"]

    if not game_state.get_flag(PROTOCOL_CHOSEN_FLAG):
        return _handle_protocol_selection(cmd, game_state)

    return None, [">> Protocol already selected. Continue onward."]


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
        ">> Two protocols remain operational.",
        "",
        "    (1) Whisper Protocol  — [Undetected Observation]",
        "    (2) Beacon Protocol   — [Signal Initiation Detected]",
        "",
        ">> Choose protocol: 'whisper' or 'beacon'"
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
            return "whisper_awaken", [">> Whisper Protocol engaged. You fade into the stream..."]

        elif cmd == "beacon":
            return "beacon_1", [">> Beacon Protocol active. You call something from the dark..."]

    return None, [">> Unknown protocol. Type 'whisper' or 'beacon'."]

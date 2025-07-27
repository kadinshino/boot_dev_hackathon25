"""
Room Utility Functions - Shared across all room modules
"""

def format_enter_lines(title, body_lines):
    return [
        f"\n=== {title.upper()} ===",
        *body_lines,
        ""
    ]

def print_inventory(game_state):
    inv = game_state.inventory
    return [f"Inventory: {', '.join(inv)}" if inv else "Inventory is empty."]

def describe_flags(game_state, prefix=""):
    return [f"{prefix}{k}: {v}" for k, v in game_state.flags.items()]

def load_room_intro(config):
    return format_enter_lines(config["name"], config["entry_text"])

def transition_to_room(game_state, new_room):
    game_state.current_room = new_room
    return f">> Transitioning to {new_room}..."

def flags_all_set(game_state, flags):
    return all(game_state.get_flag(f) for f in flags)

def flags_any_set(game_state, flags):
    return any(game_state.get_flag(f) for f in flags)

def get_room_path_type(room_name: str) -> str:
    name = room_name.lower()
    if "beacon" in name:
        return "beacon"
    if "whisper" in name:
        return "whisper"
    return "neutral"

# Puzzle step processing utility
def process_puzzle_command(cmd, game_state, steps_dict):
    cmd = cmd.strip().lower()
    for step_id, step in steps_dict.items():
        if cmd == step.get("command"):
            if not flags_all_set(game_state, step.get("requires", [])):
                return None, step.get("fail", [">> You can't do that yet."])
            if game_state.get_flag(step["sets"]):
                return None, step.get("already_done", [">> Already done."])
            game_state.set_flag(step["sets"])
            return step_id, step.get("success", [">> Success."])
    return None, None

# Global commands and router
GLOBAL_COMMANDS = {
    "look": lambda gs: [">> You scan the area... but nothing changes."],
    "observe": lambda gs: [">> You observe carefully, but nothing new stands out."],
    "scan": lambda gs: [">> You run a basic scan, but no anomalies are found."],
    "inventory": print_inventory,
    "inv": print_inventory,
    "i": print_inventory,
    "flags": lambda gs: describe_flags(gs),
    "help": lambda gs: [
        ">> Universal commands:",
        "  look / scan / observe - examine your surroundings",
        "  inventory / i         - view held items",
        "  flags                 - list game flags (debug)",
        "  help                  - show this help menu"
    ]
}

def standard_commands(cmd, game_state, room_module=None):
    cmd = cmd.strip().lower()

    if cmd in GLOBAL_COMMANDS:
        return True, GLOBAL_COMMANDS[cmd](game_state)

    if room_module and hasattr(room_module, "get_available_commands"):
        room_cmds = room_module.get_available_commands()
        if cmd == "help" and room_cmds:
            return True, [
                *GLOBAL_COMMANDS["help"](game_state),
                "",
                ">> Room-specific commands:",
                *[f"  {c}" for c in room_cmds]
            ]

    return False, None

# def debug_room_state(game_state):
#     return [
#         f">> Current room: {game_state.current_room}",
#         f">> Score: {game_state.score}",
#         f">> Health: {game_state.health}",
#         f">> Inventory: {', '.join(game_state.inventory)}",
#         f">> Flags: {len(game_state.flags)} total"
#     ]


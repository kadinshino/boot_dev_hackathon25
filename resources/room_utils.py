# # rooms/room_utils.py

# def format_enter_lines(title, body_lines):
#     return [
#         f"\n=== {title.upper()} ===",
#         *body_lines,
#         ""
#     ]

# def standard_commands(cmd, game_state, room_module=None):
#     cmd = cmd.strip().lower()

#     if cmd in ["look", "observe", "scan"]:
#         return True, [">> You scan the area... but nothing changes."]

#     elif cmd == "inventory":
#         inv = game_state.inventory
#         return True, [f"Inventory: {', '.join(inv)}" if inv else "Inventory is empty."]

#     elif cmd == "help":
#         lines = [
#             ">> Universal commands:",
#             "  look / scan     - examine your surroundings",
#             "  inventory        - view held items",
#             "  help             - show this help menu",
#         ]

#         if room_module and hasattr(room_module, "get_available_commands"):
#             room_cmds = room_module.get_available_commands()
#             if room_cmds:
#                 lines.append("")
#                 lines.append(">> Room-specific commands:")
#                 lines.extend([f"  {cmd}" for cmd in room_cmds])

#         return True, lines

#     return False, []

# def transition_to_room(next_room, lines=None):
#     if lines is None:
#         lines = []
#     return next_room, lines

# rooms/room_utils.py

def format_enter_lines(title, body_lines):
    return [f"\n=== {title.upper()} ===", *body_lines, ""]


def print_inventory(game_state):
    inv = game_state.inventory
    return f"Inventory: {', '.join(inv)}" if inv else "Inventory is empty."


def describe_flags(game_state, flag_list):
    return [f"{flag}: {'✔' if game_state.get_flag(flag) else '✘'}" for flag in flag_list]


def load_room_intro(config):
    return format_enter_lines(config.get("name", "Unknown Room"), config.get("entry_text", []))


def transition_to_room(next_room, lines=None):
    if lines is None:
        lines = []
    return next_room, lines


# Global command registry (expandable)
GLOBAL_COMMANDS = {
    "look": lambda g: [">> You scan the area... but nothing changes."],
    "scan": lambda g: [">> You scan the area... but nothing changes."],
    "observe": lambda g: [">> You scan the area... but nothing changes."],
    "inventory": lambda g: [print_inventory(g)],
    "debug": lambda g: debug_room_state(g),  # Optional dev command
}


def standard_commands(cmd, game_state, room_module=None):
    cmd = cmd.strip().lower()

    if cmd in GLOBAL_COMMANDS and GLOBAL_COMMANDS[cmd]:
        return True, GLOBAL_COMMANDS[cmd](game_state)

    elif cmd == "help":
        lines = [
            ">> Universal commands:",
            "  look / scan     - examine your surroundings",
            "  inventory        - view held items",
            "  help             - show this help menu",
        ]
        if room_module and hasattr(room_module, "get_available_commands"):
            room_cmds = room_module.get_available_commands()
            if room_cmds:
                lines.append("")
                lines.append(">> Room-specific commands:")
                lines.extend([f"  {cmd}" for cmd in room_cmds])
        return True, lines

    return False, []


def debug_room_state(game_state):
    return [
        f">> Current room: {game_state.current_room}",
        f">> Score: {game_state.score}",
        f">> Health: {game_state.health}",
        f">> Inventory: {', '.join(game_state.inventory)}",
        f">> Flags: {len(game_state.flags)} total"
    ]

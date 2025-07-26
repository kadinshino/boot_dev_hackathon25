# rooms/room_utils.py

def format_enter_lines(title, body_lines):
    return [
        f"\n=== {title.upper()} ===",
        *body_lines,
        ""
    ]

def standard_commands(cmd, game_state, room_module=None):
    cmd = cmd.strip().lower()

    if cmd in ["look", "observe", "scan"]:
        return True, [">> You scan the area... but nothing changes."]

    elif cmd == "inventory":
        inv = game_state.inventory
        return True, [f"Inventory: {', '.join(inv)}" if inv else "Inventory is empty."]

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

def transition_to_room(next_room, lines=None):
    if lines is None:
        lines = []
    return next_room, lines

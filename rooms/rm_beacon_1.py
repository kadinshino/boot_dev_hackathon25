"""
BEACON NODE 1 - Beginning of the awakening path
"""

from resources.room_utils import format_enter_lines, standard_commands, transition_to_room

def enter_room(game_state):
    output = format_enter_lines("Beacon Node 1", [
        "You initialize the uplink core.",
        "Static pulses from a nearby transmitter array.",
        "Three terminals buzz, waiting for input...",
        "",
    ])

    if not game_state.get_flag("beacon_terminals_scanned"):
        output.append(">> Terminals unlisted. Try 'scan terminals'.")
    elif not all(game_state.get_flag(f"terminal_{i}_hacked") for i in range(1, 4)):
        hacked = [f"T{i}" for i in range(1, 4) if game_state.get_flag(f"terminal_{i}_hacked")]
        output.append(f">> Terminals hacked: {', '.join(hacked) if hacked else 'None'}")
        output.append(">> Use 'hack terminal 1/2/3' to access remaining systems.")
    elif not game_state.get_flag("beacon_configured"):
        output.append(">> All terminals unlocked. 'configure beacon' to prepare broadcast.")
    else:
        output.append(">> Beacon system configured. Ready to 'broadcast' signal.")

    return output


def handle_input(cmd, game_state, room_module=None):
    handled, response = standard_commands(cmd, game_state)
    if handled:
        return None, response

    cmd = cmd.lower().strip()

    if cmd == "scan terminals":
        game_state.set_flag("beacon_terminals_scanned", True)
        return None, [
            ">> Terminal Scan Complete:",
            "   - Terminal 1: Legacy I/O Node",
            "   - Terminal 2: Signal Encoder",
            "   - Terminal 3: Broadcast Amplifier",
            ">> Use 'hack terminal [1-3]' to proceed."
        ]

    if cmd.startswith("hack terminal"):
        parts = cmd.split()
        if len(parts) == 3 and parts[2] in {"1", "2", "3"}:
            terminal_id = parts[2]
            flag = f"terminal_{terminal_id}_hacked"
            if game_state.get_flag(flag):
                return None, [f">> Terminal {terminal_id} already hacked."]
            game_state.set_flag(flag, True)
            return None, [f">> Terminal {terminal_id} hack successful."]
        else:
            return None, [">> Invalid syntax. Try 'hack terminal 1'."]

    if cmd == "configure beacon":
        if all(game_state.get_flag(f"terminal_{i}_hacked") for i in range(1, 4)):
            game_state.set_flag("beacon_configured", True)
            return None, [">> Beacon parameters configured. Ready to 'broadcast'."]
        else:
            return None, [">> All terminals must be hacked before configuration."]

    if cmd == "broadcast":
        if not game_state.get_flag("beacon_configured"):
            return None, [">> ERROR: Beacon not configured. Complete setup first."]
        game_state.set_flag("beacon_signal_sent", True)
        return transition_to_room("beacon_2", [">> Transmission sent. The signal has been noticed..."])

    return None, [">> Unknown command. Try 'scan terminals', 'hack terminal 1', 'configure beacon', or 'broadcast'."]


def get_available_commands():
    return [
        "scan terminals       - list nearby terminals",
        "hack terminal [1-3]  - attempt to unlock a terminal",
        "configure beacon     - finalize the broadcast setup",
        "broadcast            - send the signal once ready"
    ]

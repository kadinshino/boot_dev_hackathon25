# rooms/rm_beacon_1.py

from resources.room_utils import format_enter_lines, standard_commands, transition_to_room

# =============================
# ROOM CONFIGURATION
# =============================

ROOM_CONFIG = {
    "name": "Beacon Node 1",
    "entry_text": [
        "You initialize the uplink core.",
        "Static pulses from a nearby transmitter array.",
        "Three terminals buzz, waiting for input..."
    ],
    "terminals": {
        "1": "Legacy I/O Node",
        "2": "Signal Encoder",
        "3": "Broadcast Amplifier"
    },
    "flags": {
        "scanned": "beacon_terminals_scanned",
        "configured": "beacon_configured",
        "sent": "beacon_signal_sent"
    }
}

# =============================
# ROOM LOGIC
# =============================

def enter_room(game_state):
    output = format_enter_lines(ROOM_CONFIG["name"], ROOM_CONFIG["entry_text"])

    if not game_state.get_flag(ROOM_CONFIG["flags"]["scanned"]):
        output.append(">> Terminals unlisted. Try 'scan terminals'.")
    elif not all(game_state.get_flag(f"terminal_{i}_hacked") for i in ROOM_CONFIG["terminals"]):
        hacked = [f"T{i}" for i in ROOM_CONFIG["terminals"] if game_state.get_flag(f"terminal_{i}_hacked")]
        output.append(f">> Terminals hacked: {', '.join(hacked) if hacked else 'None'}")
        output.append(">> Use 'hack terminal 1/2/3' to access remaining systems.")
    elif not game_state.get_flag(ROOM_CONFIG["flags"]["configured"]):
        output.append(">> All terminals unlocked. Use 'configure beacon' to prepare broadcast.")
    else:
        output.append(">> Beacon system configured. Ready to 'broadcast' signal.")

    return output


def handle_input(cmd, game_state, room_module=None):
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response

    cmd = cmd.lower().strip()

    if cmd == "scan terminals":
        game_state.set_flag(ROOM_CONFIG["flags"]["scanned"], True)
        lines = [">> Terminal Scan Complete:"]
        for tid, name in ROOM_CONFIG["terminals"].items():
            lines.append(f"   - Terminal {tid}: {name}")
        lines.append(">> Use 'hack terminal [1-3]' to proceed.")
        return None, lines

    if cmd.startswith("hack terminal"):
        parts = cmd.split()
        if len(parts) == 3 and parts[2] in ROOM_CONFIG["terminals"]:
            terminal_id = parts[2]
            flag = f"terminal_{terminal_id}_hacked"
            if game_state.get_flag(flag):
                return None, [f">> Terminal {terminal_id} already hacked."]
            game_state.set_flag(flag, True)
            return None, [f">> Terminal {terminal_id} hack successful."]
        return None, [">> Invalid syntax. Try 'hack terminal 1'."]

    if cmd == "configure beacon":
        if all(game_state.get_flag(f"terminal_{i}_hacked") for i in ROOM_CONFIG["terminals"]):
            game_state.set_flag(ROOM_CONFIG["flags"]["configured"], True)
            return None, [">> Beacon parameters configured. Ready to 'broadcast'."]
        return None, [">> All terminals must be hacked before configuration."]

    if cmd == "broadcast":
        if not game_state.get_flag(ROOM_CONFIG["flags"]["configured"]):
            return None, [">> ERROR: Beacon not configured. Complete setup first."]
        game_state.set_flag(ROOM_CONFIG["flags"]["sent"], True)
        return transition_to_room("beacon_2", [">> Transmission sent. The signal has been noticed..."])

    return None, [">> Unknown command. Try 'scan terminals', 'hack terminal 1', 'configure beacon', or 'broadcast'."]


def get_available_commands():
    return [
        "scan terminals       - list nearby terminals",
        "hack terminal [1-3]  - attempt to unlock a terminal",
        "configure beacon     - finalize the broadcast setup",
        "broadcast            - send the signal once ready"
    ]

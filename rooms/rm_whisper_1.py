# rooms/rm_whisper_1.py

from resources.room_utils import format_enter_lines, standard_commands, transition_to_room

def enter_room(game_state):
    lines = [
        "You awaken in a dark subnet.",
        "Ghost packets drift silently through data fog.",
        "A flickering port glows softly. It awaits a command..."
    ]

    if not game_state.get_flag("whisper_scanned"):
        lines.append("")
        lines.append(">> You sense something hidden in the fog. Try 'scan fog'.")
    elif not game_state.get_flag("whisper_pinged"):
        lines.append(">> Port detected. Recommend 'ping port' to verify link integrity.")
    elif not game_state.get_flag("whisper_decrypted"):
        lines.append(">> Port handshake requires decoding. Try 'decrypt handshake'.")
    else:
        lines.append(">> Port interface unlocked. Use 'connect port' to proceed.")

    return format_enter_lines("Whisper Node 1", lines)


def handle_input(cmd, game_state, room_module=None):
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response

    cmd = cmd.lower().strip()

    if cmd == "scan fog":
        if game_state.get_flag("whisper_scanned"):
            return None, [">> Fog already scanned. Port silhouette confirmed."]
        game_state.set_flag("whisper_scanned", True)
        return None, [
            ">> Data fog analyzed.",
            "   - Latent pulse signature detected.",
            "   - Source: encrypted I/O port",
            "   - Status: dormant",
            ">> Try 'ping port'"
        ]

    if cmd == "ping port":
        if not game_state.get_flag("whisper_scanned"):
            return None, [">> No target in range. 'scan fog' first."]
        if game_state.get_flag("whisper_pinged"):
            return None, [">> Port already pinged. Awaiting handshake..."]
        game_state.set_flag("whisper_pinged", True)
        return None, [
            ">> Port response: weak but alive.",
            "   - Challenge sequence detected.",
            "   - Encryption tier: legacy AES-1.7",
            ">> Try 'decrypt handshake'"
        ]

    if cmd == "decrypt handshake":
        if not game_state.get_flag("whisper_pinged"):
            return None, [">> No active challenge detected. 'ping port' first."]
        if game_state.get_flag("whisper_decrypted"):
            return None, [">> Handshake already decrypted. Ready to connect."]
        game_state.set_flag("whisper_decrypted", True)
        return None, [
            ">> Decryption successful.",
            "   - Access vector stabilized",
            "   - Uplink ID confirmed: WHSPR-001",
            ">> Use 'connect port' to enter"
        ]

    if cmd == "connect port":
        if not game_state.get_flag("whisper_decrypted"):
            return None, [">> Access denied. Handshake decryption required."]
        game_state.set_flag("whisper_port_connected", True)
        return transition_to_room("whisper_2", [">> Port connected. You slip deeper into the whisper stream..."])

    return None, [">> Unknown command. Try 'scan fog', 'ping port', 'decrypt handshake', or 'connect port'."]


def get_available_commands():
    return [
        "scan fog            - analyze data fog for hidden I/O ports",
        "ping port           - probe the visible port for response",
        "decrypt handshake   - decode port challenge to enable access",
        "connect port        - interface with the port once decrypted"
    ]

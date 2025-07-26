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

    # Main path commands
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

    # Optional path: sniff / trace / spoof / inject / connect alt
    if cmd == "sniff stream":
        if not game_state.get_flag("whisper_scanned"):
            return None, [">> Stream too chaotic. 'scan fog' required first."]
        if game_state.get_flag("whisper_sniffed"):
            return None, [">> Already sniffed. Data echoes in silence..."]
        game_state.set_flag("whisper_sniffed", True)
        return None, [
            ">> Listening to data stream...",
            "   - Intercepted: 'WHSPR-ALT-GATE:{locked}'",
            "   - Fragment: '[F0]GR1D_N0D3~tr4c3_nul1'",
            ">> Try 'trace signal'?"
        ]

    if cmd == "trace signal":
        if not game_state.get_flag("whisper_sniffed"):
            return None, [">> No traceable packet. Use 'sniff stream' first."]
        if game_state.get_flag("whisper_traced"):
            return None, [">> Already traced. Ghost path remains dim."]
        game_state.set_flag("whisper_traced", True)
        return None, [
            ">> Signal trace initiated...",
            "   - Route: deprecated proxy loop",
            "   - Obfuscation: High",
            "   - Detected: Secondary port ghosted in subnet tail.",
            ">> Try 'spoof source' to impersonate probe origin."
        ]

    if cmd == "spoof source":
        if not game_state.get_flag("whisper_traced"):
            return None, [">> No valid target for spoofing."]
        if game_state.get_flag("whisper_spoofed"):
            return None, [">> Source identity already masked."]
        game_state.set_flag("whisper_spoofed", True)
        return None, [
            ">> Source spoofed as: system_routine[1729]",
            "   - Port AI confused.",
            "   - Access channel destabilizing...",
            ">> Try 'inject packet' before it collapses."
        ]

    if cmd == "inject packet":
        if not game_state.get_flag("whisper_spoofed"):
            return None, [">> Injection path invalid. Spoof first."]
        if game_state.get_flag("whisper_injected"):
            return None, [">> Packet already injected. System buffering..."]
        game_state.set_flag("whisper_injected", True)
        return None, [
            ">> Packet injection successful.",
            "   - Buffer overflow induced",
            "   - Alternate gate 'W-ALT-2' opened",
            ">> Optional route unlocked. Use 'connect alt' to diverge."
        ]

    if cmd == "connect alt":
        if not game_state.get_flag("whisper_injected"):
            return None, [">> Alternate port unavailable. Injection required."]
        return transition_to_room("whisper_2_alt", [">> You reroute through the shadow gate..."])

    # Alternate exploit path: sniff / compile / connect mimic
    if cmd == "compile exploit":
        if not game_state.get_flag("whisper_sniffed"):
            return None, [">> No exploit vector discovered."]
        if game_state.get_flag("whisper_exploit_ready"):
            return None, [">> Exploit already compiled."]
        game_state.set_flag("whisper_exploit_ready", True)
        return None, [
            ">> Assembling zero-day...",
            "   - Using legacy packet fragment and trace residue.",
            "   - Exploit compiled: PORT_MIMIC_17X ready",
            ">> You can now 'connect mimic' to trick the system."
        ]

    if cmd == "connect mimic":
        if not game_state.get_flag("whisper_exploit_ready"):
            return None, [">> Exploit not prepared. Compile first."]
        return transition_to_room("whisper_2_mimic", [">> System spoofed. Mimic connection stabilized..."])

    return None, [">> Unknown command. Try 'help' for available options."]


def get_available_commands():
    return [
        "scan fog            - analyze data fog for hidden I/O ports",
        "ping port           - probe the visible port for response",
        "decrypt handshake   - decode port challenge to enable access",
        "connect port        - interface with the port once decrypted",
        "sniff stream        - intercept ambient data transmissions",
        "trace signal        - follow packet ghost routes to hidden paths",
        "spoof source        - impersonate origin node",
        "inject packet       - overload input buffer with custom payload",
        "compile exploit     - build an alternate port bypass using packet traces",
        "connect alt         - access alternate gate (if unlocked)",
        "connect mimic       - spoof entry using compiled exploit"
    ]

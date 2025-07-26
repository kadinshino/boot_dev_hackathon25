# rooms/rm_whisper_2.py

from resources.room_utils import format_enter_lines, standard_commands, transition_to_room

def enter_room(game_state):
    lines = [
        "You phase into a buffer tunnel suspended in static.",
        "Above you, three pillars hum erratically — uplink beacons trying to stabilize.",
        "Ghost packets from your previous path still echo here..."
    ]

    if not game_state.get_flag("w2_scanned"):
        lines.append("")
        lines.append(">> The buffer distorts your senses. Try 'scan buffer'.")
    elif not game_state.get_flag("w2_sniffed"):
        lines.append(">> Three beacon signatures detected. 'sniff beacons' for analysis.")
    else:
        if not game_state.get_flag("w2_alpha_decrypted"):
            lines.append(">> Pillar Alpha flickers wildly. Try 'ping alpha'.")
        if not game_state.get_flag("w2_beta_decrypted"):
            lines.append(">> Pillar Beta emits corrupted Morse. Try 'ping beta'.")
        if not game_state.get_flag("w2_gamma_decrypted"):
            lines.append(">> Pillar Gamma bleeds scrambled light. Try 'ping gamma'.")
    
    if all([
        game_state.get_flag("w2_alpha_decrypted"),
        game_state.get_flag("w2_beta_decrypted"),
        game_state.get_flag("w2_gamma_decrypted")
    ]):
        lines.append(">> All pillars resonate in unison. Run 'connect uplink'.")

    return format_enter_lines("Whisper Node 2", lines)


def handle_input(cmd, game_state, room_module=None):
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response

    cmd = cmd.lower().strip()

    # Main path commands
    if cmd == "scan buffer":
        if game_state.get_flag("w2_scanned"):
            return None, [">> Buffer already analyzed. Three beacons detected."]
        game_state.set_flag("w2_scanned", True)
        return None, [
            ">> Buffer analysis complete.",
            "   - Signal strength: fluctuating",
            "   - Detected: 3 encrypted uplink nodes",
            "   - Designation: Alpha, Beta, Gamma",
            "   - Status: Desynchronized",
            ">> Try 'sniff beacons' to intercept their transmissions."
        ]

    if cmd == "sniff beacons":
        if not game_state.get_flag("w2_scanned"):
            return None, [">> No signals detected. 'scan buffer' first."]
        if game_state.get_flag("w2_sniffed"):
            return None, [">> Beacon frequencies already captured."]
        game_state.set_flag("w2_sniffed", True)
        return None, [
            ">> Intercepting beacon transmissions...",
            "   - Alpha: RSA-2048 encrypted pulse",
            "   - Beta: Legacy Morse over TCP/IP",
            "   - Gamma: Quantum-entangled photon stream",
            ">> Each beacon requires individual handshake. Use 'ping' commands."
        ]

    # Alpha pillar sequence
    if cmd == "ping alpha":
        if not game_state.get_flag("w2_sniffed"):
            return None, [">> Alpha beacon not identified. 'sniff beacons' first."]
        if game_state.get_flag("w2_alpha_pinged"):
            return None, [">> Alpha already responding. Ready for decryption."]
        game_state.set_flag("w2_alpha_pinged", True)
        return None, [
            ">> Alpha beacon response:",
            "   - Challenge key: 0xDEADBEEF",
            "   - Expecting prime factorization",
            ">> Try 'decrypt alpha' with proper key analysis."
        ]

    if cmd == "decrypt alpha":
        if not game_state.get_flag("w2_alpha_pinged"):
            return None, [">> No alpha handshake initiated. 'ping alpha' first."]
        if game_state.get_flag("w2_alpha_decrypted"):
            return None, [">> Alpha pillar already stable."]
        game_state.set_flag("w2_alpha_decrypted", True)
        return None, [
            ">> Factorization complete: 3735928559 = 48889 × 76423",
            ">> Alpha beacon stabilized. Hash lock disengaged.",
            "   - Fragment recovered: 'R3AL1TY_'"
        ]

    # Beta pillar sequence
    if cmd == "ping beta":
        if not game_state.get_flag("w2_sniffed"):
            return None, [">> Beta beacon not identified. 'sniff beacons' first."]
        if game_state.get_flag("w2_beta_pinged"):
            return None, [">> Beta already responding. Morse pattern active."]
        game_state.set_flag("w2_beta_pinged", True)
        return None, [
            ">> Beta beacon response:",
            "   - Signal: -.-- --- ..- .-. / ..-. ..- - ..- .-. .",
            "   - Translation required",
            ">> Try 'decrypt beta' to decode transmission."
        ]

    if cmd == "decrypt beta":
        if not game_state.get_flag("w2_beta_pinged"):
            return None, [">> No beta signal received. 'ping beta' first."]
        if game_state.get_flag("w2_beta_decrypted"):
            return None, [">> Beta pillar already stable."]
        game_state.set_flag("w2_beta_decrypted", True)
        return None, [
            ">> Morse decoded: 'YOUR FUTURE'",
            ">> Beta beacon synchronized. Stream re-aligned.",
            "   - Fragment recovered: 'AW41TS_'"
        ]

    # Gamma pillar sequence
    if cmd == "ping gamma":
        if not game_state.get_flag("w2_sniffed"):
            return None, [">> Gamma beacon not identified. 'sniff beacons' first."]
        if game_state.get_flag("w2_gamma_pinged"):
            return None, [">> Gamma already responding. Photon stream active."]
        game_state.set_flag("w2_gamma_pinged", True)
        return None, [
            ">> Gamma beacon response:",
            "   - Quantum state: |Ψ⟩ = α|0⟩ + β|1⟩",
            "   - Entanglement detected",
            ">> Try 'decrypt gamma' to collapse wavefunction."
        ]

    if cmd == "decrypt gamma":
        if not game_state.get_flag("w2_gamma_pinged"):
            return None, [">> No gamma entanglement. 'ping gamma' first."]
        if game_state.get_flag("w2_gamma_decrypted"):
            return None, [">> Gamma pillar already stable."]
        game_state.set_flag("w2_gamma_decrypted", True)
        return None, [
            ">> Wavefunction collapsed. State measured: |1⟩",
            ">> Gamma beacon synchronized. Scramble cleared.",
            "   - Fragment recovered: 'Y0U'"
        ]

    # Final connection
    if cmd == "connect uplink":
        if not all([
            game_state.get_flag("w2_alpha_decrypted"),
            game_state.get_flag("w2_beta_decrypted"),
            game_state.get_flag("w2_gamma_decrypted")
        ]):
            return None, [">> Uplink failed. Not all beacons decrypted."]
        return transition_to_room("whisper_3", [
            ">> Fragments assembled: 'R3AL1TY_AW41TS_Y0U'",
            ">> Uplink engaged. Your mind surges toward the outer stream..."
        ])

    # Alternative path commands
    if cmd == "trace fragments":
        alpha = "R3AL1TY_" if game_state.get_flag("w2_alpha_decrypted") else "???????"
        beta = "AW41TS_" if game_state.get_flag("w2_beta_decrypted") else "??????"
        gamma = "Y0U" if game_state.get_flag("w2_gamma_decrypted") else "???"
        return None, [
            ">> Fragment buffer status:",
            f"   - Alpha: {alpha}",
            f"   - Beta: {beta}",
            f"   - Gamma: {gamma}",
            ">> Complete all three to form uplink key."
        ]

    if cmd == "inject buffer overflow":
        if not game_state.get_flag("w2_sniffed"):
            return None, [">> No injection vector available."]
        if game_state.get_flag("w2_overflow_attempted"):
            return None, [">> Overflow already attempted. System compensated."]
        game_state.set_flag("w2_overflow_attempted", True)
        return None, [
            ">> Buffer overflow injection attempted...",
            "   - System response: Adaptive firewall engaged",
            "   - Side effect: Beacon sync rate increased by 12%",
            ">> Standard decryption still required, but faster now."
        ]

    if cmd == "spoof beacon":
        if not game_state.get_flag("w2_scanned"):
            return None, [">> No beacon signatures to spoof."]
        if game_state.get_flag("w2_beacon_spoofed"):
            return None, [">> Spoof already active. Fourth beacon mimicked."]
        game_state.set_flag("w2_beacon_spoofed", True)
        return None, [
            ">> Creating phantom beacon 'Delta'...",
            "   - Signature forged from existing patterns",
            "   - System confused: Processing priority shifted",
            ">> Hidden data cache exposed. Try 'scan cache'."
        ]

    if cmd == "scan cache":
        if not game_state.get_flag("w2_beacon_spoofed"):
            return None, [">> No cache access. Spoofing required."]
        return None, [
            ">> Hidden cache contents:",
            "   - Archived whisper logs from Node 0",
            "   - Corrupted user profile: 'N30_TH3_0N3'",
            "   - Emergency bypass code: [REDACTED]",
            ">> Interesting, but the main path remains through the beacons."
        ]

    return None, [">> Unknown command. Try 'help' for available options."]


def get_available_commands():
    return [
        "scan buffer          - analyze the buffer tunnel environment",
        "sniff beacons        - intercept beacon transmissions",
        "ping alpha           - initiate handshake with Alpha pillar",
        "ping beta            - initiate handshake with Beta pillar", 
        "ping gamma           - initiate handshake with Gamma pillar",
        "decrypt alpha        - stabilize Alpha beacon with proper key",
        "decrypt beta         - decode Beta beacon's Morse transmission",
        "decrypt gamma        - collapse Gamma beacon's quantum state",
        "connect uplink       - establish reality connection (all beacons required)",
        "trace fragments      - check collected key fragments",
        "inject buffer overflow - attempt to exploit the buffer system",
        "spoof beacon         - create a phantom fourth beacon",
        "scan cache           - examine hidden data (requires spoofing)"
    ]
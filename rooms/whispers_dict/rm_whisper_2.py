from utils.room_utils import format_enter_lines, standard_commands, transition_to_room

# ==========================================
# PUZZLE CONFIGURATION - Easy to modify!
# ==========================================

ROOM_CONFIG = {
    "name": "Whisper Node 2",
    "entry_text": [
        "You phase into a buffer tunnel suspended in static.",
        "Above you, three pillars hum erratically — uplink beacons trying to stabilize.",
        "Ghost packets from your previous path still echo here..."
    ],
    
    # Progression hints
    "progression_hints": {
        "start": ">> The buffer distorts your senses. Try 'scan buffer'.",
        "scanned": ">> Three beacon signatures detected. 'sniff beacons' for analysis.",
        "alpha_hint": ">> Pillar Alpha flickers wildly. Try 'ping alpha'.",
        "beta_hint": ">> Pillar Beta emits corrupted Morse. Try 'ping beta'.",
        "gamma_hint": ">> Pillar Gamma bleeds scrambled light. Try 'ping gamma'.",
        "all_complete": ">> All pillars resonate in unison. Run 'connect uplink'."
    },
    
    # Beacon fragments that will be collected
    "fragments": {
        "alpha": "R3AL1TY_",
        "beta": "AW41TS_",
        "gamma": "Y0U"
    },
    
    # Next room destination
    "destination": "whisper_3"
}

# Main puzzle path - Scan and analyze beacons
DISCOVERY_PATH = {
    "scan_buffer": {
        "command": "scan buffer",
        "requires": [],
        "sets": "w2_scanned",
        "already_done": [">> Buffer already analyzed. Three beacons detected."],
        "success": [
            ">> Buffer analysis complete.",
            "   - Signal strength: fluctuating",
            "   - Detected: 3 encrypted uplink nodes",
            "   - Designation: Alpha, Beta, Gamma",
            "   - Status: Desynchronized",
            ">> Try 'sniff beacons' to intercept their transmissions."
        ]
    },
    
    "sniff_beacons": {
        "command": "sniff beacons",
        "requires": ["w2_scanned"],
        "sets": "w2_sniffed",
        "missing_req": [">> No signals detected. 'scan buffer' first."],
        "already_done": [">> Beacon frequencies already captured."],
        "success": [
            ">> Intercepting beacon transmissions...",
            "   - Alpha: RSA-2048 encrypted pulse",
            "   - Beta: Legacy Morse over TCP/IP",
            "   - Gamma: Quantum-entangled photon stream",
            ">> Each beacon requires individual handshake. Use 'ping' commands."
        ]
    }
}

# Alpha beacon puzzle path
ALPHA_BEACON = {
    "ping_alpha": {
        "command": "ping alpha",
        "requires": ["w2_sniffed"],
        "sets": "w2_alpha_pinged",
        "missing_req": [">> Alpha beacon not identified. 'sniff beacons' first."],
        "already_done": [">> Alpha already responding. Ready for decryption."],
        "success": [
            ">> Alpha beacon response:",
            "   - Challenge key: 0xDEADBEEF",
            "   - Expecting prime factorization",
            ">> Try 'decrypt alpha' with proper key analysis."
        ]
    },
    
    "decrypt_alpha": {
        "command": "decrypt alpha",
        "requires": ["w2_alpha_pinged"],
        "sets": "w2_alpha_decrypted",
        "missing_req": [">> No alpha handshake initiated. 'ping alpha' first."],
        "already_done": [">> Alpha pillar already stable."],
        "success": [
            ">> Factorization complete: 3735928559 = 48889 × 76423",
            ">> Alpha beacon stabilized. Hash lock disengaged.",
            "   - Fragment recovered: 'R3AL1TY_'"
        ]
    }
}

# Beta beacon puzzle path
BETA_BEACON = {
    "ping_beta": {
        "command": "ping beta",
        "requires": ["w2_sniffed"],
        "sets": "w2_beta_pinged",
        "missing_req": [">> Beta beacon not identified. 'sniff beacons' first."],
        "already_done": [">> Beta already responding. Morse pattern active."],
        "success": [
            ">> Beta beacon response:",
            "   - Signal: -.-- --- ..- .-. / ..-. ..- - ..- .-. .",
            "   - Translation required",
            ">> Try 'decrypt beta' to decode transmission."
        ]
    },
    
    "decrypt_beta": {
        "command": "decrypt beta",
        "requires": ["w2_beta_pinged"],
        "sets": "w2_beta_decrypted",
        "missing_req": [">> No beta signal received. 'ping beta' first."],
        "already_done": [">> Beta pillar already stable."],
        "success": [
            ">> Morse decoded: 'YOUR FUTURE'",
            ">> Beta beacon synchronized. Stream re-aligned.",
            "   - Fragment recovered: 'AW41TS_'"
        ]
    }
}

# Gamma beacon puzzle path
GAMMA_BEACON = {
    "ping_gamma": {
        "command": "ping gamma",
        "requires": ["w2_sniffed"],
        "sets": "w2_gamma_pinged",
        "missing_req": [">> Gamma beacon not identified. 'sniff beacons' first."],
        "already_done": [">> Gamma already responding. Photon stream active."],
        "success": [
            ">> Gamma beacon response:",
            "   - Quantum state: |Ψ⟩ = α|0⟩ + β|1⟩",
            "   - Entanglement detected",
            ">> Try 'decrypt gamma' to collapse wavefunction."
        ]
    },
    
    "decrypt_gamma": {
        "command": "decrypt gamma",
        "requires": ["w2_gamma_pinged"],
        "sets": "w2_gamma_decrypted",
        "missing_req": [">> No gamma entanglement. 'ping gamma' first."],
        "already_done": [">> Gamma pillar already stable."],
        "success": [
            ">> Wavefunction collapsed. State measured: |1⟩",
            ">> Gamma beacon synchronized. Scramble cleared.",
            "   - Fragment recovered: 'Y0U'"
        ]
    }
}

# Final connection command
FINAL_PATH = {
    "connect_uplink": {
        "command": "connect uplink",
        "requires": ["w2_alpha_decrypted", "w2_beta_decrypted", "w2_gamma_decrypted"],
        "missing_req": [">> Uplink failed. Not all beacons decrypted."],
        "transition": True,
        "transition_msg": [
            ">> Fragments assembled: 'R3AL1TY_AW41TS_Y0U'",
            ">> Uplink engaged. Your mind surges toward the outer stream..."
        ]
    }
}

# Alternative/optional commands
ALTERNATE_COMMANDS = {
    "trace_fragments": {
        "command": "trace fragments",
        "requires": [],
        "dynamic_response": True  # Special flag for custom handling
    },
    
    "inject_overflow": {
        "command": "inject buffer overflow",
        "requires": ["w2_sniffed"],
        "sets": "w2_overflow_attempted",
        "missing_req": [">> No injection vector available."],
        "already_done": [">> Overflow already attempted. System compensated."],
        "success": [
            ">> Buffer overflow injection attempted...",
            "   - System response: Adaptive firewall engaged",
            "   - Side effect: Beacon sync rate increased by 12%",
            ">> Standard decryption still required, but faster now."
        ]
    },
    
    "spoof_beacon": {
        "command": "spoof beacon",
        "requires": ["w2_scanned"],
        "sets": "w2_beacon_spoofed",
        "missing_req": [">> No beacon signatures to spoof."],
        "already_done": [">> Spoof already active. Fourth beacon mimicked."],
        "success": [
            ">> Creating phantom beacon 'Delta'...",
            "   - Signature forged from existing patterns",
            "   - System confused: Processing priority shifted",
            ">> Hidden data cache exposed. Try 'scan cache'."
        ]
    },
    
    "scan_cache": {
        "command": "scan cache",
        "requires": ["w2_beacon_spoofed"],
        "missing_req": [">> No cache access. Spoofing required."],
        "success": [
            ">> Hidden cache contents:",
            "   - Archived whisper logs from Node 0",
            "   - Corrupted user profile: 'N30_TH3_0N3'",
            "   - Emergency bypass code: [REDACTED]",
            ">> Interesting, but the main path remains through the beacons."
        ]
    }
}

# Command descriptions for help
COMMAND_DESCRIPTIONS = [
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

# ==========================================
# ROOM LOGIC - Generic handlers below
# ==========================================

def enter_room(game_state):
    lines = ROOM_CONFIG["entry_text"].copy()
    
    # Add progression hints based on state
    if not game_state.get_flag("w2_scanned"):
        lines.extend(["", ROOM_CONFIG["progression_hints"]["start"]])
    elif not game_state.get_flag("w2_sniffed"):
        lines.append(ROOM_CONFIG["progression_hints"]["scanned"])
    else:
        # Check each beacon
        if not game_state.get_flag("w2_alpha_decrypted"):
            lines.append(ROOM_CONFIG["progression_hints"]["alpha_hint"])
        if not game_state.get_flag("w2_beta_decrypted"):
            lines.append(ROOM_CONFIG["progression_hints"]["beta_hint"])
        if not game_state.get_flag("w2_gamma_decrypted"):
            lines.append(ROOM_CONFIG["progression_hints"]["gamma_hint"])
    
    # Check if all beacons are complete
    if all([
        game_state.get_flag("w2_alpha_decrypted"),
        game_state.get_flag("w2_beta_decrypted"),
        game_state.get_flag("w2_gamma_decrypted")
    ]):
        lines.append(ROOM_CONFIG["progression_hints"]["all_complete"])
    
    return format_enter_lines(ROOM_CONFIG["name"], lines)


def handle_trace_fragments(game_state):
    """Special handler for the trace fragments command"""
    alpha = ROOM_CONFIG["fragments"]["alpha"] if game_state.get_flag("w2_alpha_decrypted") else "???????"
    beta = ROOM_CONFIG["fragments"]["beta"] if game_state.get_flag("w2_beta_decrypted") else "??????"
    gamma = ROOM_CONFIG["fragments"]["gamma"] if game_state.get_flag("w2_gamma_decrypted") else "???"
    
    return None, [
        ">> Fragment buffer status:",
        f"   - Alpha: {alpha}",
        f"   - Beta: {beta}",
        f"   - Gamma: {gamma}",
        ">> Complete all three to form uplink key."
    ]


def process_puzzle_command(cmd, game_state, puzzle_config):
    """Generic puzzle command processor"""
    for action_key, action in puzzle_config.items():
        if cmd == action["command"]:
            # Handle dynamic responses
            if action.get("dynamic_response"):
                if action["command"] == "trace fragments":
                    return handle_trace_fragments(game_state)
                continue
            
            # Check requirements
            for req in action.get("requires", []):
                if not game_state.get_flag(req):
                    return None, action.get("missing_req", [">> Requirement not met."])
            
            # Check if already done (for non-transition commands)
            if "sets" in action and game_state.get_flag(action["sets"]):
                return None, action.get("already_done", [">> Already completed."])
            
            # Set flag if specified
            if "sets" in action:
                game_state.set_flag(action["sets"], True)
            
            # Handle transition
            if action.get("transition"):
                return transition_to_room(ROOM_CONFIG["destination"], action["transition_msg"])
            
            # Return success message
            return None, action["success"]
    
    return None, None


def handle_input(cmd, game_state, room_module=None):
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response
    
    cmd = cmd.lower().strip()
    
    # Check all puzzle paths
    all_paths = [
        DISCOVERY_PATH,
        ALPHA_BEACON,
        BETA_BEACON,
        GAMMA_BEACON,
        FINAL_PATH,
        ALTERNATE_COMMANDS
    ]
    
    for puzzle_config in all_paths:
        transition, response = process_puzzle_command(cmd, game_state, puzzle_config)
        if response is not None:
            return transition, response
    
    return None, [">> Unknown command. Try 'help' for available options."]


def get_available_commands():
    return COMMAND_DESCRIPTIONS

# SPYHVER-38: AWAKENS

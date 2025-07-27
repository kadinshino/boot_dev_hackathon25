# rooms/rm_whisper_1.py

from resources.room_utils import format_enter_lines, standard_commands, transition_to_room

# ==========================================
# PUZZLE CONFIGURATION - Easy to modify!
# ==========================================

ROOM_CONFIG = {
    "name": "Whisper Node 1",
    "entry_text": [
        "You awaken in a dark subnet.",
        "Ghost packets drift silently through data fog.",
        "A flickering port glows softly. It awaits a command..."
    ],
    
    # Main puzzle progression hints
    "progression_hints": {
        "start": ">> You sense something hidden in the fog. Try 'scan fog'.",
        "scanned": ">> Port detected. Recommend 'ping port' to verify link integrity.",
        "pinged": ">> Port handshake requires decoding. Try 'decrypt handshake'.",
        "decrypted": ">> Port interface unlocked. Use 'connect port' to proceed."
    },
    
    # Next room destinations
    "destinations": {
        "main": "whisper_2",
        "alt": "whisper_2_alt",
        "mimic": "whisper_2_mimic"
    }
}

# Main puzzle path configuration
MAIN_PATH = {
    "scan_fog": {
        "command": "scan fog",
        "requires": [],
        "sets": "whisper_scanned",
        "already_done": [">> Fog already scanned. Port silhouette confirmed."],
        "success": [
            ">> Data fog analyzed.",
            "   - Latent pulse signature detected.",
            "   - Source: encrypted I/O port",
            "   - Status: dormant",
            ">> Try 'ping port'"
        ]
    },
    
    "ping_port": {
        "command": "ping port",
        "requires": ["whisper_scanned"],
        "sets": "whisper_pinged",
        "missing_req": [">> No target in range. 'scan fog' first."],
        "already_done": [">> Port already pinged. Awaiting handshake..."],
        "success": [
            ">> Port response: weak but alive.",
            "   - Challenge sequence detected.",
            "   - Encryption tier: legacy AES-1.7",
            ">> Try 'decrypt handshake'"
        ]
    },
    
    "decrypt_handshake": {
        "command": "decrypt handshake",
        "requires": ["whisper_pinged"],
        "sets": "whisper_decrypted",
        "missing_req": [">> No active challenge detected. 'ping port' first."],
        "already_done": [">> Handshake already decrypted. Ready to connect."],
        "success": [
            ">> Decryption successful.",
            "   - Access vector stabilized",
            "   - Uplink ID confirmed: WHSPR-001",
            ">> Use 'connect port' to enter"
        ]
    },
    
    "connect_port": {
        "command": "connect port",
        "requires": ["whisper_decrypted"],
        "sets": "whisper_port_connected",
        "missing_req": [">> Access denied. Handshake decryption required."],
        "transition": "main",
        "transition_msg": [">> Port connected. You slip deeper into the whisper stream..."]
    }
}

# Alternative path configuration
ALT_PATH = {
    "sniff_stream": {
        "command": "sniff stream",
        "requires": ["whisper_scanned"],
        "sets": "whisper_sniffed",
        "missing_req": [">> Stream too chaotic. 'scan fog' required first."],
        "already_done": [">> Already sniffed. Data echoes in silence..."],
        "success": [
            ">> Listening to data stream...",
            "   - Intercepted: 'WHSPR-ALT-GATE:{locked}'",
            "   - Fragment: '[F0]GR1D_N0D3~tr4c3_nul1'",
            ">> Try 'trace signal'?"
        ]
    },
    
    "trace_signal": {
        "command": "trace signal",
        "requires": ["whisper_sniffed"],
        "sets": "whisper_traced",
        "missing_req": [">> No traceable packet. Use 'sniff stream' first."],
        "already_done": [">> Already traced. Ghost path remains dim."],
        "success": [
            ">> Signal trace initiated...",
            "   - Route: deprecated proxy loop",
            "   - Obfuscation: High",
            "   - Detected: Secondary port ghosted in subnet tail.",
            ">> Try 'spoof source' to impersonate probe origin."
        ]
    },
    
    "spoof_source": {
        "command": "spoof source",
        "requires": ["whisper_traced"],
        "sets": "whisper_spoofed",
        "missing_req": [">> No valid target for spoofing."],
        "already_done": [">> Source identity already masked."],
        "success": [
            ">> Source spoofed as: system_routine[1729]",
            "   - Port AI confused.",
            "   - Access channel destabilizing...",
            ">> Try 'inject packet' before it collapses."
        ]
    },
    
    "inject_packet": {
        "command": "inject packet",
        "requires": ["whisper_spoofed"],
        "sets": "whisper_injected",
        "missing_req": [">> Injection path invalid. Spoof first."],
        "already_done": [">> Packet already injected. System buffering..."],
        "success": [
            ">> Packet injection successful.",
            "   - Buffer overflow induced",
            "   - Alternate gate 'W-ALT-2' opened",
            ">> Optional route unlocked. Use 'connect alt' to diverge."
        ]
    },
    
    "connect_alt": {
        "command": "connect alt",
        "requires": ["whisper_injected"],
        "missing_req": [">> Alternate port unavailable. Injection required."],
        "transition": "alt",
        "transition_msg": [">> You reroute through the shadow gate..."]
    }
}

# Exploit path configuration
EXPLOIT_PATH = {
    "compile_exploit": {
        "command": "compile exploit",
        "requires": ["whisper_sniffed"],
        "sets": "whisper_exploit_ready",
        "missing_req": [">> No exploit vector discovered."],
        "already_done": [">> Exploit already compiled."],
        "success": [
            ">> Assembling zero-day...",
            "   - Using legacy packet fragment and trace residue.",
            "   - Exploit compiled: PORT_MIMIC_17X ready",
            ">> You can now 'connect mimic' to trick the system."
        ]
    },
    
    "connect_mimic": {
        "command": "connect mimic",
        "requires": ["whisper_exploit_ready"],
        "missing_req": [">> Exploit not prepared. Compile first."],
        "transition": "mimic",
        "transition_msg": [">> System spoofed. Mimic connection stabilized..."]
    }
}

# Command descriptions for help
COMMAND_DESCRIPTIONS = [
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

# ==========================================
# ROOM LOGIC - Generic handlers below
# ==========================================

def enter_room(game_state):
    lines = ROOM_CONFIG["entry_text"].copy()
    
    # Add progression hint based on current state
    if not game_state.get_flag("whisper_scanned"):
        lines.extend(["", ROOM_CONFIG["progression_hints"]["start"]])
    elif not game_state.get_flag("whisper_pinged"):
        lines.append(ROOM_CONFIG["progression_hints"]["scanned"])
    elif not game_state.get_flag("whisper_decrypted"):
        lines.append(ROOM_CONFIG["progression_hints"]["decrypted"])
    else:
        lines.append(ROOM_CONFIG["progression_hints"]["decrypted"])
    
    return format_enter_lines(ROOM_CONFIG["name"], lines)


def process_puzzle_command(cmd, game_state, puzzle_config):
    """Generic puzzle command processor"""
    for action_key, action in puzzle_config.items():
        if cmd == action["command"]:
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
            if "transition" in action:
                dest = ROOM_CONFIG["destinations"][action["transition"]]
                return transition_to_room(dest, action["transition_msg"])
            
            # Return success message
            return None, action["success"]
    
    return None, None


def handle_input(cmd, game_state, room_module=None):
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response
    
    cmd = cmd.lower().strip()
    
    # Check all puzzle paths
    for puzzle_config in [MAIN_PATH, ALT_PATH, EXPLOIT_PATH]:
        transition, response = process_puzzle_command(cmd, game_state, puzzle_config)
        if response is not None:
            return transition, response
    
    return None, [">> Unknown command. Try 'help' for available options."]


def get_available_commands():
    return COMMAND_DESCRIPTIONS
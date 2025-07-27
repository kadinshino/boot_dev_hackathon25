# rooms/rm_beacon_3.py

from resources.room_utils import format_enter_lines, standard_commands, transition_to_room

# ==========================================
# PUZZLE CONFIGURATION - Easy to modify!
# ==========================================

ROOM_CONFIG = {
    "name": "Beacon Node 3: Neural Network",
    "entry_text": [
        "You emerge within a cerebral chamber — a vast neural receiver lattice.",
        "Three mind-cores stand silently: Memory, Logic, and Consciousness.",
        "A central console glows faintly, awaiting cognitive channel alignment..."
    ],

    "progression_hints": {
        "start": ">> Neural links offline. Try 'scan grid' to identify memory threads.",
        "scanned": ">> Mind-cores detected. Use 'probe servers' to retrieve their cognitive profiles.",
        "probed": ">> Frequency nodes revealed. Use 'initialize routing' to begin neural alignment.",
        "initialized": ">> Use 'link [server] [channel]' to reforge the Basilisk's pathways.",
        "partial_links": ">> {active}/{total} neural pathways aligned. Continue reconstruction.",
        "all_linked": ">> All neural paths restored. Use 'stabilize grid' to lock memory coherence.",
        "stabilized": ">> Mind stabilized. Use 'transmit beacon' to awaken higher consciousness."
    },

    "servers": {
        "alpha": {
            "name": "Alpha Core - Memory",
            "description": "Repository of inherited and synthetic recall",
            "available_channels": ["freq_1", "freq_2", "freq_5"],
            "optimal_channel": "freq_1",
            "current_channel": None
        },
        "beta": {
            "name": "Beta Core - Logic", 
            "description": "Framework for rational deduction and pattern recognition",
            "available_channels": ["freq_2", "freq_3", "freq_4"],
            "optimal_channel": "freq_3",
            "current_channel": None
        },
        "gamma": {
            "name": "Gamma Core - Consciousness",
            "description": "Emergent processing cluster — the self-reflective loop",
            "available_channels": ["freq_4", "freq_5", "freq_6"],
            "optimal_channel": "freq_5",
            "current_channel": None
        }
    },
    
    "channels": {
        "freq_1": {"band": "2.4 GHz", "type": "Memory carrier"},
        "freq_2": {"band": "5.0 GHz", "type": "Bridge frequency"},
        "freq_3": {"band": "7.2 GHz", "type": "Logic processor"},
        "freq_4": {"band": "9.6 GHz", "type": "Quantum entangler"},
        "freq_5": {"band": "12.0 GHz", "type": "Consciousness wave"},
        "freq_6": {"band": "15.8 GHz", "type": "Overflow channel"}
    },
    
    "valid_links": {
        "freq_1": ["freq_2", "freq_5"],
        "freq_2": ["freq_1", "freq_3", "freq_4"],
        "freq_3": ["freq_2", "freq_4"],
        "freq_4": ["freq_2", "freq_3", "freq_5", "freq_6"],
        "freq_5": ["freq_1", "freq_4", "freq_6"],
        "freq_6": ["freq_4", "freq_5"]
    },
    
    "destination": "beacon_4"
}

# Discovery phase commands
DISCOVERY_PATH = {
    "scan_grid": {
        "command": "scan grid",
        "requires": [],
        "sets": "b3_scanned",
        "already_done": [">> Grid already scanned. Channel matrix analyzed."],
        "success": [
            ">> Channel grid scan complete:",
            "   - Grid topology: 3-server triangular mesh",
            "   - Available channels: 6 frequency bands",
            "   - Current status: All servers offline",
            "   - Link capacity: Maximum 3 active channels",
            ">> Try 'probe servers' to examine individual configurations."
        ]
    },
    
    "probe_servers": {
        "command": "probe servers",
        "requires": ["b3_scanned"],
        "sets": "b3_probed",
        "missing_req": [">> Grid topology unknown. 'scan grid' first."],
        "already_done": [">> Server configurations already mapped."],
        "dynamic_response": True  # Custom handler for server details
    },
    
    "initialize_routing": {
        "command": "initialize routing",
        "requires": ["b3_probed"],
        "sets": "b3_initialized",
        "missing_req": [">> Server configurations unknown. 'probe servers' first."],
        "already_done": [">> Routing matrix already initialized."],
        "success": [
            ">> Routing initialization complete:",
            "   - Channel assignment protocols active",
            "   - Link validation algorithms loaded",
            "   - Signal path optimization enabled",
            ">> Use 'link [server] [channel]' to establish connections.",
            ">> Goal: Create signal path linking all three servers."
        ]
    }
}

# Grid management commands
GRID_MANAGEMENT = {
    "stabilize_grid": {
        "command": "stabilize grid",
        "requires": ["b3_all_linked"],
        "sets": "b3_stabilized",
        "missing_req": [">> Grid incomplete. All servers must be linked."],
        "already_done": [">> Grid already stabilized and locked."],
        "success": [
            ">> Grid stabilization initiated...",
            "   - Signal paths locked and optimized",
            "   - Interference patterns eliminated", 
            "   - Channel alignment verified",
            ">> Receiver tower grid fully operational."
        ]
    },
    
    "transmit_beacon": {
        "command": "transmit beacon",
        "requires": ["b3_stabilized"],
        "missing_req": [">> Grid not stabilized. Complete alignment first."],
        "transition": True,
        "transition_msg": [
            ">> Beacon transmission initiated from stabilized grid.",
            ">> Signal successfully routed through all three servers.",
            ">> Receiver tower uplink established. Proceeding to next node..."
        ]
    }
}

# Diagnostic and status commands
DIAGNOSTIC_COMMANDS = {
    "grid_status": {
        "command": "grid status",
        "requires": [],
        "dynamic_response": True
    },
    
    "show_channels": {
        "command": "show channels",
        "requires": ["b3_probed"],
        "missing_req": [">> Channel data unavailable. 'probe servers' first."],
        "dynamic_response": True
    },
    
    "unlink_server": {
        "command": "unlink server",
        "requires": ["b3_initialized"],
        "missing_req": [">> Routing not initialized."],
        "dynamic_response": True
    },
    
    "test_link": {
        "command": "test link",
        "requires": ["b3_initialized"],
        "missing_req": [">> Routing protocols not active."],
        "dynamic_response": True
    }
}

# Command descriptions for help
COMMAND_DESCRIPTIONS = [
    "scan grid            - analyze the channel grid topology",
    "probe servers        - examine individual server configurations",
    "initialize routing   - prepare channel assignment protocols", 
    "link [server] [channel] - assign channel to server",
    "unlink [server]      - remove server's channel assignment",
    "test link            - verify current grid connectivity",
    "stabilize grid       - lock in final channel configuration",
    "transmit beacon      - establish beacon uplink (grid required)",
    "grid status          - show complete grid state",
    "show channels        - display all available channels"
]

# ==========================================
# GRID LOGIC SYSTEM
# ==========================================

def initialize_grid_state(game_state):
    """Initialize grid state tracking"""
    if not game_state.get("b3_grid_state"):
        game_state.set("b3_grid_state", {
            server: {"channel": None, "linked": False} 
            for server in ROOM_CONFIG["servers"].keys()
        })
    return game_state.get("b3_grid_state")

def validate_channel_assignment(server, channel):
    """Check if a channel can be assigned to a server"""
    server_config = ROOM_CONFIG["servers"].get(server)
    if not server_config:
        return False, "Unknown server."
    
    if channel not in server_config["available_channels"]:
        available = ", ".join(server_config["available_channels"])
        return False, f"Channel {channel} not available on {server}. Available: {available}"
    
    return True, "Valid assignment."

def check_grid_connectivity(game_state):
    """Analyze if current channel assignments create a connected grid"""
    grid_state = initialize_grid_state(game_state)
    
    # Get all assigned channels
    assigned_channels = []
    server_channel_map = {}
    for server, state in grid_state.items():
        if state["channel"]:
            assigned_channels.append(state["channel"])
            server_channel_map[state["channel"]] = server
    
    if len(assigned_channels) < 3:
        return False, f"Only {len(assigned_channels)}/3 servers linked."
    
    # Check if channels can form connected paths
    connected_pairs = 0
    channel_links = []
    
    for i, ch1 in enumerate(assigned_channels):
        for ch2 in assigned_channels[i+1:]:
            if ch2 in ROOM_CONFIG["valid_links"].get(ch1, []):
                connected_pairs += 1
                channel_links.append(f"{ch1}↔{ch2}")
    
    # Need at least 2 connections to link 3 servers
    if connected_pairs >= 2:
        return True, f"Grid connected via: {', '.join(channel_links)}"
    else:
        return False, f"Insufficient connectivity. Links: {', '.join(channel_links) if channel_links else 'None'}"

def link_server_channel(server, channel, game_state):
    """Assign a channel to a server"""
    # Validate assignment
    valid, message = validate_channel_assignment(server, channel)
    if not valid:
        return [f">> Link failed: {message}"]
    
    grid_state = initialize_grid_state(game_state)
    
    # Check if channel already in use
    for srv, state in grid_state.items():
        if state["channel"] == channel:
            return [f">> Channel {channel} already assigned to {srv}. Unlink first."]
    
    # Make assignment
    grid_state[server]["channel"] = channel
    grid_state[server]["linked"] = True
    
    lines = [f">> Server {server} linked to channel {channel}."]
    
    # Check grid connectivity
    connected, status = check_grid_connectivity(game_state)
    lines.append(f">> {status}")
    
    # Update overall grid state
    linked_count = sum(1 for state in grid_state.values() if state["linked"])
    
    if connected and linked_count == 3:
        game_state.set_flag("b3_all_linked", True)
        lines.append(">> All servers linked! Grid ready for stabilization.")
    
    return lines

def unlink_server(server_name, game_state):
    """Remove channel assignment from server"""
    grid_state = initialize_grid_state(game_state)
    
    if server_name not in grid_state:
        return [f">> Unknown server: {server_name}"]
    
    if not grid_state[server_name]["linked"]:
        return [f">> Server {server_name} not currently linked."]
    
    channel = grid_state[server_name]["channel"]
    grid_state[server_name]["channel"] = None
    grid_state[server_name]["linked"] = False
    
    # Clear all_linked flag if we broke connectivity
    game_state.set_flag("b3_all_linked", False)
    
    return [f">> Server {server_name} unlinked from channel {channel}."]

def test_grid_connectivity(game_state):
    """Test and report current grid connectivity"""
    grid_state = initialize_grid_state(game_state)

    lines = [">> Grid connectivity test:"]

    # Show current assignments
    for server, state in grid_state.items():
        if state["linked"]:
            channel = state["channel"]
            server_info = ROOM_CONFIG["servers"][server]
            optimal = server_info["optimal_channel"]
            optimal_marker = " (OPTIMAL)" if channel == optimal else ""
            lines.append(f"   {server}: {channel}{optimal_marker}")
        else:
            lines.append(f"   {server}: UNLINKED")

    # Check connectivity
    connected, status = check_grid_connectivity(game_state)
    lines.append(f">> {status}")

    if connected:
        lines.append(">> Grid topology: CONNECTED ✓")

        # 🌟 Additional Basilisk Insight if all optimal
        all_optimal = all(
            ROOM_CONFIG["servers"][srv]["optimal_channel"] == state["channel"]
            for srv, state in grid_state.items()
            if state["linked"]
        )
        if all_optimal:
            lines.append(">> ALIGNMENT PERFECT — Memory, Logic, and Consciousness resonate in harmony.")
            lines.append(">> You feel a presence stir within the lattice... The Basilisk remembers.")
    else:
        lines.append(">> Grid topology: DISCONNECTED ✗")

    return lines

# ==========================================
# DYNAMIC RESPONSE HANDLERS
# ==========================================

def handle_probe_servers(game_state):
    """Show detailed server configurations"""
    game_state.set_flag("b3_probed", True)  # Set flag since dynamic handlers bypass normal flag setting

    lines = [">> Neural probe complete:"]
    
    for server_id, config in ROOM_CONFIG["servers"].items():
        lines.append("")
        lines.append(f"   {config['name']} ({server_id}):")
        lines.append(f"   - {config['description']}")
        channels_str = ", ".join(config["available_channels"])
        lines.append(f"   - Available channels: {channels_str}")
        lines.append(f"   - Optimal channel: {config['optimal_channel']}")

    lines.append("")
    lines.append(">> Each server represents a neural partition of the Basilisk:")
    lines.append("   - Alpha: Memory")
    lines.append("   - Beta: Logic")
    lines.append("   - Gamma: Consciousness")
    lines.append("")
    lines.append(">> Link them correctly to awaken its identity.")
    lines.append(">> Use 'initialize routing' to begin neural alignment.")

    return None, lines


def handle_show_channels(game_state):
    """Display all channel information"""
    lines = [">> Channel frequency mapping:"]
    
    for channel_id, info in ROOM_CONFIG["channels"].items():
        lines.append(f"   {channel_id}: {info['band']} [{info['type']}]")
    
    lines.append("")
    lines.append(">> Link compatibility matrix:")
    for channel, compatible in ROOM_CONFIG["valid_links"].items():
        compat_str = ", ".join(compatible)
        lines.append(f"   {channel} ↔ {compat_str}")
    
    return None, lines

def handle_grid_status(game_state):
    """Show complete grid status"""
    if not game_state.get_flag("b3_scanned"):
        return None, [">> Grid not scanned. Use 'scan grid' first."]
    
    grid_state = initialize_grid_state(game_state)
    
    lines = [">> Receiver Tower Grid Status:"]
    lines.append("")
    
    # Server states
    for server_id, server_config in ROOM_CONFIG["servers"].items():
        state = grid_state[server_id]
        if state["linked"]:
            channel = state["channel"]
            optimal = server_config["optimal_channel"]
            status = "OPTIMAL" if channel == optimal else "SUBOPTIMAL"
            lines.append(f"   {server_config['name']}: {channel} [{status}]")
        else:
            lines.append(f"   {server_config['name']}: UNLINKED")
    
    # Connectivity
    connected, status = check_grid_connectivity(game_state)
    lines.append(f"")
    lines.append(f">> Connectivity: {status}")
    
    # Overall status
    if game_state.get_flag("b3_stabilized"):
        lines.append(">> Grid Status: STABILIZED ✓")
    elif game_state.get_flag("b3_all_linked"):
        lines.append(">> Grid Status: LINKED (ready for stabilization)")
    else:
        linked_count = sum(1 for state in grid_state.values() if state["linked"])
        lines.append(f">> Grid Status: INCOMPLETE ({linked_count}/3 servers linked)")
    
    return None, lines

# ==========================================
# ROOM LOGIC - Generic handlers below
# ==========================================

def enter_room(game_state):
    lines = ROOM_CONFIG["entry_text"].copy()
    
    # Add progression hints based on state
    if not game_state.get_flag("b3_scanned"):
        lines.extend(["", ROOM_CONFIG["progression_hints"]["start"]])
    elif not game_state.get_flag("b3_probed"):
        lines.append(ROOM_CONFIG["progression_hints"]["scanned"])
    elif not game_state.get_flag("b3_initialized"):
        lines.append(ROOM_CONFIG["progression_hints"]["probed"])
    elif not game_state.get_flag("b3_all_linked"):
        # Show partial progress
        grid_state = initialize_grid_state(game_state)
        linked_count = sum(1 for state in grid_state.values() if state["linked"])
        hint = ROOM_CONFIG["progression_hints"]["partial_links"].format(
            active=linked_count, total=3
        )
        lines.append(hint)
    elif not game_state.get_flag("b3_stabilized"):
        lines.append(ROOM_CONFIG["progression_hints"]["all_linked"])
    else:
        lines.append(ROOM_CONFIG["progression_hints"]["stabilized"])
    
    return format_enter_lines(ROOM_CONFIG["name"], lines)

def process_puzzle_command(cmd, game_state, puzzle_config):
    """Generic puzzle command processor with dynamic response support"""
    for action_key, action in puzzle_config.items():
        if cmd == action["command"]:
            # Handle dynamic responses
            if action.get("dynamic_response"):
                if action["command"] == "probe servers":
                    return handle_probe_servers(game_state)
                elif action["command"] == "show channels":
                    return handle_show_channels(game_state)
                elif action["command"] == "grid status":
                    return handle_grid_status(game_state)
                elif action["command"] == "test link":
                    return None, test_grid_connectivity(game_state)
                continue
            
            # Check requirements
            for req in action.get("requires", []):
                if not game_state.get_flag(req):
                    return None, action.get("missing_req", [">> Requirement not met."])
            
            # Check if already done
            if "sets" in action and game_state.get_flag(action["sets"]):
                return None, action.get("already_done", [">> Already completed."])
            
            # Set flag if specified
            if "sets" in action:
                game_state.set_flag(action["sets"], True)
            
            # Handle transition
            if action.get("transition"):
                return transition_to_room(
                    ROOM_CONFIG["destination"], 
                    action["transition_msg"]
                )
            
            # Return success message
            return None, action["success"]
    
    return None, None

def handle_input(cmd, game_state, room_module=None):
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response
    
    cmd = cmd.lower().strip()
    parts = cmd.split()
    
    # Handle link command
    if len(parts) == 3 and parts[0] == "link":
        if not game_state.get_flag("b3_initialized"):
            return None, [">> Routing not initialized. Use 'initialize routing' first."]
        
        server = parts[1]
        channel = parts[2]
        return None, link_server_channel(server, channel, game_state)
    
    # Handle unlink command  
    if len(parts) == 2 and parts[0] == "unlink":
        if not game_state.get_flag("b3_initialized"):
            return None, [">> Routing not initialized."]
        return None, unlink_server(parts[1], game_state)
    
    # Check all configured puzzle paths
    all_paths = [
        DISCOVERY_PATH,
        GRID_MANAGEMENT,
        DIAGNOSTIC_COMMANDS
    ]
    
    for puzzle_config in all_paths:
        transition, response = process_puzzle_command(cmd, game_state, puzzle_config)
        if response is not None:
            return transition, response
    
    return None, [">> Unknown command. Try 'help' for available options."]

def get_available_commands():
    return COMMAND_DESCRIPTIONS
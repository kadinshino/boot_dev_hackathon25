from resources.room_utils import format_enter_lines, standard_commands, transition_to_room

# ============================================================================
# CONFIGURATION
# ============================================================================

# WHISPER_GRID = {

#         # Starting area (192.168.x.x range)
#         "192.168.1.1": {
#             "connections": ["192.168.1.2", "192.168.2.1"],
#             "safe": True,
#             "description": "Entry point - Home router"
#         },
#         "192.168.1.2": {
#             "connections": ["192.168.1.1", "192.168.1.3", "172.16.0.1"],
#             "safe": True,
#             "description": "Local subnet - IoT devices"
#         },
#         "192.168.1.3": {
#             "connections": ["192.168.1.2", "192.168.3.1"],
#             "safe": False,
#             "description": "Honeypot server - MONITORED",
#             "detection_increase": 25
#         },
#         "192.168.2.1": {
#             "connections": ["192.168.1.1", "192.168.2.2"],
#             "safe": True,
#             "description": "Guest network gateway"
#         },
#         "192.168.2.2": {
#             "connections": ["192.168.2.1", "172.16.1.1"],
#             "safe": False,
#             "description": "Corporate firewall - SCANNING",
#             "detection_increase": 20
#         },
#         "192.168.3.1": {
#             "connections": ["192.168.1.3", "172.16.2.1"],
#             "safe": True,
#             "description": "VPN endpoint - encrypted tunnel"
#         },
        
#         # Middle area (172.16.x.x range)
#         "172.16.0.1": {
#             "connections": ["192.168.1.2", "172.16.0.2", "172.16.1.1"],
#             "safe": True,
#             "description": "NAT gateway - traffic mixer"
#         },
#         "172.16.0.2": {
#             "connections": ["172.16.0.1", "10.1.1.1"],
#             "safe": False,
#             "description": "IDS sensor - DEEP PACKET INSPECTION",
#             "detection_increase": 30
#         },
#         "172.16.1.1": {
#             "connections": ["192.168.2.2", "172.16.0.1", "172.16.1.2"],
#             "safe": True,
#             "description": "Proxy chain alpha"
#         },
#         "172.16.1.2": {
#             "connections": ["172.16.1.1", "172.16.2.1", "10.1.2.1"],
#             "safe": True,
#             "description": "Tor entry node"
#         },
#         "172.16.2.1": {
#             "connections": ["192.168.3.1", "172.16.1.2", "172.16.2.2"],
#             "safe": True,
#             "description": "Anonymous relay"
#         },
#         "172.16.2.2": {
#             "connections": ["172.16.2.1", "10.0.1.1"],
#             "safe": False,
#             "description": "Government tap - TRACED",
#             "detection_increase": 40
#         },
        
#         # Exit area (10.x.x.x range)
#         "10.1.1.1": {
#             "connections": ["172.16.0.2", "10.1.1.2"],
#             "safe": False,
#             "description": "Border router - LOGGED",
#             "detection_increase": 15
#         },
#         "10.1.1.2": {
#             "connections": ["10.1.1.1", "10.0.0.1"],
#             "safe": True,
#             "description": "Exit proxy - final hop"
#         },
#         "10.1.2.1": {
#             "connections": ["172.16.1.2", "10.0.1.1"],
#             "safe": True,
#             "description": "Darknet gateway"
#         },
#         "10.0.1.1": {
#             "connections": ["172.16.2.2", "10.1.2.1", "10.0.0.1"],
#             "safe": True,
#             "description": "Hidden service endpoint"
#         },
#         "10.0.0.1": {
#             "connections": ["10.1.1.2", "10.0.1.1"],
#             "safe": True,
#             "description": "EXIT NODE - Freedom awaits"
#         }


# }

# ============================================================================
# CONFIGURATION
# ============================================================================

WHISPER_GRID = {

    "192.168.1.1": {
        "connections": ["192.168.1.2", "192.168.2.1","10.0.0.1"],
        "safe": True,
        "description": "Entry point - Home router"
    },
    "192.168.1.2": {
        "connections": ["192.168.1.1", "192.168.1.3", "172.16.0.1"],
        "safe": True,
        "description": "Local subnet - IoT devices"
    },
    "192.168.1.3": {
        "connections": ["192.168.1.2", "192.168.3.1"],
        "safe": False,
        "description": "Honeypot server - MONITORED",
        "detection_increase": 25
    },
    # ... (trimmed for brevity)
    "10.0.0.1": {
        "connections": ["10.1.1.2", "10.0.1.1"],
        "safe": True,
        "description": "EXIT NODE - Freedom awaits"
    }
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_node(ip):
    return WHISPER_GRID.get(ip, {})

def is_exit(ip):
    return ip == "10.0.0.1"

def get_detection(game_state):
    return game_state.get("detection_level", 0)

def add_detection(game_state, amount):
    level = min(get_detection(game_state) + amount, 100)
    game_state.set("detection_level", level)
    return level

# ============================================================================
# ROOM ENTRY
# ============================================================================

def enter_room(game_state):
    lines = [
        "You jack into Whisper Node 4: the Obfuscation Grid.",
        "Layered subnets stretch out before you in a virtual maze.",
        "Security pulses through each connection like a heartbeat."
    ]

    if game_state.get("grid_position") is None:
        game_state.set("grid_position", "192.168.1.1")
        game_state.set("detection_level", 0)
        game_state.set("path_history", ["192.168.1.1"])

    current_ip = game_state.get("grid_position")
    detection = get_detection(game_state)

    lines.append(f">> Current IP: {current_ip}")
    lines.append(f">> Detection Level: {detection}% {'[SAFE]' if detection < 50 else '[WARNING]' if detection < 80 else '[CRITICAL]'}")

    if not game_state.get_flag("grid_scanned"):
        lines.append(">> Topology unknown. Use 'scan network'.")
    else:
        lines.append(">> Use 'ping [IP]' and 'trace route [IP]' to navigate.")

    if is_exit(current_ip):
        lines.append(">> Exit node detected. Use 'connect exit' to proceed.")

    return format_enter_lines("Whisper: Obfuscation Grid", lines)

# ============================================================================
# INPUT HANDLER
# ============================================================================

def handle_input(cmd, game_state, room_module=None):
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response

    cmd = cmd.lower().strip()
    current_ip = game_state.get("grid_position", "192.168.1.1")
    node = get_node(current_ip)

    if cmd == "scan network":
        if game_state.get_flag("grid_scanned"):
            return None, [">> Already scanned."]
        game_state.set_flag("grid_scanned", True)
        return None, [
            ">> Topology scan complete.",
            "   - Exit node: 10.0.0.1",
            f"   - Total nodes: {len(WHISPER_GRID)}",
            "   - Threats detected: active",
            ">> Try 'ping [IP]' or 'trace route [IP]'"
        ]

    if cmd.startswith("ping "):
        if not game_state.get_flag("grid_scanned"):
            return None, [">> Scan the network first."]
        target = cmd[5:].strip()
        if target not in node["connections"]:
            return None, [f">> {target} not reachable from {current_ip}."]
        target_node = get_node(target)
        safety = "SAFE" if target_node["safe"] else "MONITORED"
        return None, [
            f">> Ping {target} successful:",
            f"   - {target_node['description']}",
            f"   - Status: {safety}",
            ">> Use 'trace route [IP]' to move."
        ]

    if cmd.startswith("trace route "):
        if not game_state.get_flag("grid_scanned"):
            return None, [">> Cannot navigate blind."]
        target = cmd[12:].strip()
        if target not in node["connections"]:
            return None, [f">> {target} is not directly connected to {current_ip}."]
        game_state.set("grid_position", target)
        history = game_state.get("path_history") or []
        history.append(target)
        game_state.set("path_history", history)

        lines = [f">> Tracing route to {target}...", f">> Arrived: {get_node(target)['description']}"]

        if not get_node(target)["safe"]:
            inc = get_node(target).get("detection_increase", 20)
            new_level = add_detection(game_state, inc)
            lines += [
                f">> ALERT: Intrusion detection triggered.",
                f">> Detection +{inc}% → {new_level}%"
            ]
            if new_level >= 100:
                return transition_to_room("security_cell", [
                    ">> DETECTION MAXED.",
                    ">> Security lockdown initiated.",
                    ">> Redirected to Security Cell..."
                ])
        return None, lines

    if cmd in ("trace history", "show path"):
        path = game_state.get("path_history") or []
        return None, [">> Route history:"] + [f"   {i+1}. {ip}" for i, ip in enumerate(path)]

    if cmd in ("scan neighbors", "list connections"):
        return None, [
            f">> Connections from {current_ip}:"
        ] + [f"   - {ip} [{'SAFE' if get_node(ip)['safe'] else 'MONITORED'}]" for ip in node["connections"]]

    if cmd == "spoof ip":
        if game_state.get_flag("grid_spoofed"):
            return None, [">> Already spoofed."]
        if get_detection(game_state) < 30:
            return None, [">> No need to spoof — detection too low."]
        game_state.set_flag("grid_spoofed", True)
        game_state.set("detection_level", max(0, get_detection(game_state) - 25))
        return None, [">> IP spoofed. Detection reduced by 25%."]

    if cmd == "inject noise":
        if game_state.get_flag("grid_noise_injected"):
            return None, [">> Network already jammed."]
        game_state.set_flag("grid_noise_injected", True)
        return None, [">> Injected noise packets. Next unsafe node triggers 10% less detection."]

    if cmd == "connect exit":
        if not is_exit(current_ip):
            return None, [">> No exit node at this location."]
        if get_detection(game_state) >= 80:
            return None, [">> Detection too high to exit safely."]
        return transition_to_room("whisper_5", [
            f">> Exit successful. Final detection: {get_detection(game_state)}%",
            ">> Whisper grid traversal complete. Initiating phase shift..."
        ])

    return None, [">> Unknown command. Try 'scan network', 'trace route [IP]', or 'connect exit'."]

# ============================================================================
# HELP
# ============================================================================

def get_available_commands():
    return [
        "scan network         - map network nodes",
        "ping [IP]            - probe adjacent IPs",
        "trace route [IP]     - move to a connected node",
        "scan neighbors       - list accessible IPs",
        "trace history        - show your route",
        "spoof ip             - reduce detection by 25% (once)",
        "inject noise         - reduce next threat detection (once)",
        "connect exit         - escape from final node"
    ]

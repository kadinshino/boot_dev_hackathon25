from resources.room_utils import format_enter_lines, standard_commands, transition_to_room
import random

# ============================================================================
# CONFIGURATION
# ============================================================================

# Simplified grid with clearer progression path
WHISPER_GRID = {
    # Starting area (192.168.x.x range) - SAFE ZONE
    "192.168.1.1": {
        "connections": ["192.168.1.2", "192.168.2.1"],
        "safe": True,
        "description": "Entry point - Home router (SAFE)",
        "zone": "start"
    },
    "192.168.1.2": {
        "connections": ["192.168.1.1", "192.168.1.3", "172.16.0.1"],
        "safe": True,
        "description": "Local subnet - IoT devices (SAFE)",
        "zone": "start"
    },
    "192.168.1.3": {
        "connections": ["192.168.1.2", "192.168.3.1"],
        "safe": False,
        "description": "Honeypot server - MONITORED",
        "detection_increase": 15,
        "zone": "start"
    },
    "192.168.2.1": {
        "connections": ["192.168.1.1", "192.168.2.2"],
        "safe": True,
        "description": "Guest network gateway (SAFE)",
        "zone": "start"
    },
    "192.168.2.2": {
        "connections": ["192.168.2.1", "172.16.1.1"],
        "safe": False,
        "description": "Corporate firewall - SCANNING",
        "detection_increase": 20,
        "zone": "start"
    },
    "192.168.3.1": {
        "connections": ["192.168.1.3", "172.16.2.1"],
        "safe": True,
        "description": "VPN endpoint - encrypted tunnel (SAFE)",
        "zone": "start"
    },
    
    # Middle area (172.16.x.x range) - MIXED ZONE
    "172.16.0.1": {
        "connections": ["192.168.1.2", "172.16.0.2", "172.16.1.1"],
        "safe": True,
        "description": "NAT gateway - traffic mixer (SAFE)",
        "zone": "middle"
    },
    "172.16.0.2": {
        "connections": ["172.16.0.1", "10.1.1.1"],
        "safe": False,
        "description": "IDS sensor - DEEP PACKET INSPECTION",
        "detection_increase": 25,
        "zone": "middle"
    },
    "172.16.1.1": {
        "connections": ["192.168.2.2", "172.16.0.1", "172.16.1.2"],
        "safe": True,
        "description": "Proxy chain alpha (SAFE)",
        "zone": "middle"
    },
    "172.16.1.2": {
        "connections": ["172.16.1.1", "172.16.2.1", "10.1.2.1"],
        "safe": True,
        "description": "Tor entry node (SAFE)",
        "zone": "middle"
    },
    "172.16.2.1": {
        "connections": ["192.168.3.1", "172.16.1.2", "172.16.2.2"],
        "safe": True,
        "description": "Anonymous relay (SAFE)",
        "zone": "middle"
    },
    "172.16.2.2": {
        "connections": ["172.16.2.1", "10.0.1.1"],
        "safe": False,
        "description": "Government tap - TRACED",
        "detection_increase": 30,
        "zone": "middle"
    },
    
    # Exit area (10.x.x.x range) - DANGER ZONE
    "10.1.1.1": {
        "connections": ["172.16.0.2", "10.1.1.2"],
        "safe": False,
        "description": "Border router - LOGGED",
        "detection_increase": 10,
        "zone": "exit"
    },
    "10.1.1.2": {
        "connections": ["10.1.1.1", "10.0.0.1"],
        "safe": True,
        "description": "Exit proxy - final hop (SAFE)",
        "zone": "exit"
    },
    "10.1.2.1": {
        "connections": ["172.16.1.2", "10.0.1.1"],
        "safe": True,
        "description": "Darknet gateway (SAFE)",
        "zone": "exit"
    },
    "10.0.1.1": {
        "connections": ["172.16.2.2", "10.1.2.1", "10.0.0.1"],
        "safe": True,
        "description": "Hidden service endpoint (SAFE)",
        "zone": "exit"
    },
    "10.0.0.1": {
        "connections": ["10.1.1.2", "10.0.1.1"],
        "safe": True,
        "description": "EXIT NODE - Freedom awaits",
        "zone": "exit"
    }
}

# Environmental messages based on detection level
WHISPER_MESSAGES = {
    0: [">> whisper: welcome to the grid...", ">> whisper: they haven't noticed you yet..."],
    20: [">> whisper: something stirs in the darkness...", ">> whisper: careful, they're listening..."],
    40: [">> whisper: the watchers have noticed...", ">> whisper: your signature is spreading..."],
    60: [">> whisper: they're closing in...", ">> whisper: time is running out..."],
    80: [">> whisper: DANGER DANGER DANGER", ">> whisper: escape while you still can..."]
}

# Backdoor locations (persistent safe paths)
BACKDOOR_CAPABLE = ["192.168.1.2", "172.16.1.1", "10.1.2.1"]

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
    # Apply noise reduction if active
    if game_state.get_flag("grid_noise_injected") and amount > 0:
        amount = max(0, amount - 10)
        game_state.set_flag("grid_noise_injected", False)
        
    level = min(get_detection(game_state) + amount, 100)
    game_state.set("detection_level", level)
    return level

def get_whisper_message(detection_level):
    """Get atmospheric message based on detection"""
    for threshold in sorted(WHISPER_MESSAGES.keys(), reverse=True):
        if detection_level >= threshold:
            return random.choice(WHISPER_MESSAGES[threshold])
    return ""

def get_zone_info(ip):
    """Get information about which zone an IP is in"""
    node = get_node(ip)
    zone = node.get("zone", "unknown")
    zone_descriptions = {
        "start": "Starting Zone (192.168.x.x) - Relatively safe",
        "middle": "Middle Zone (172.16.x.x) - Mixed security",
        "exit": "Exit Zone (10.x.x.x) - High security area"
    }
    return zone_descriptions.get(zone, "Unknown zone")

# ============================================================================
# PATHFINDING FUNCTIONS
# ============================================================================

def find_path(start, end, visited=None):
    """Simple BFS to find shortest path between nodes"""
    if visited is None:
        visited = set()
    
    if start == end:
        return [start]
    
    visited.add(start)
    queue = [(start, [start])]
    
    while queue:
        current, path = queue.pop(0)
        node = get_node(current)
        
        for next_ip in node.get("connections", []):
            if next_ip not in visited:
                new_path = path + [next_ip]
                if next_ip == end:
                    return new_path
                visited.add(next_ip)
                queue.append((next_ip, new_path))
    
    return None

def calculate_detection_cost(path, game_state):
    """Calculate total detection cost for a path"""
    total = 0
    for ip in path[1:]:  # Skip starting position
        node = get_node(ip)
        if not node.get("safe", True):
            increase = node.get("detection_increase", 20)
            # Check for backdoors
            if ip in game_state.get("backdoors", []):
                increase = 0
            total += increase
    return total

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
        game_state.set("backdoors", [])

    current_ip = game_state.get("grid_position")
    detection = get_detection(game_state)

    lines.append("")
    lines.append(f">> Current Location: {current_ip}")
    lines.append(f">> {get_node(current_ip)['description']}")
    lines.append(f">> Zone: {get_zone_info(current_ip)}")
    lines.append("")
    lines.append(f">> Detection Level: {detection}% {'[SAFE]' if detection < 40 else '[WARNING]' if detection < 70 else '[CRITICAL]'}")
    
    # Add whisper message
    whisper = get_whisper_message(detection)
    if whisper:
        lines.append(whisper)

    if not game_state.get_flag("grid_scanned"):
        lines.append("")
        lines.append(">> Topology unknown. Use 'scan network' to map the grid.")
    else:
        lines.append("")
        lines.append(">> Use 'ping [IP]' to probe nodes, 'trace [IP]' to move.")
        if is_exit(current_ip):
            lines.append(">> EXIT NODE REACHED! Use 'connect exit' to escape!")

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
    detection = get_detection(game_state)

    # Scan network - reveals topology
    if cmd == "scan network":
        if game_state.get_flag("grid_scanned"):
            return None, [">> Network already mapped."]
        game_state.set_flag("grid_scanned", True)
        return None, [
            ">> Topology scan complete.",
            "   - Exit node: 10.0.0.1",
            f"   - Total nodes: {len(WHISPER_GRID)}",
            "   - Safe nodes: " + str(sum(1 for n in WHISPER_GRID.values() if n["safe"])),
            "   - Monitored nodes: " + str(sum(1 for n in WHISPER_GRID.values() if not n["safe"])),
            "",
            ">> Commands unlocked: ping, trace, map, traceroute"
        ]

    # Map - show current zone connections
    if cmd == "map":
        if not game_state.get_flag("grid_scanned"):
            return None, [">> Scan the network first."]
        
        lines = [f">> Local network map from {current_ip}:"]
        lines.append(f">> Current zone: {get_zone_info(current_ip)}")
        lines.append("")
        
        # Show current node
        lines.append(f"YOU ARE HERE: {current_ip}")
        lines.append(f"  └─ {node['description']}")
        lines.append("")
        
        # Show connections
        lines.append("CONNECTIONS:")
        for ip in node["connections"]:
            conn_node = get_node(ip)
            safety = "SAFE" if conn_node["safe"] else f"MONITORED (+{conn_node.get('detection_increase', 20)}%)"
            backdoor = " [BACKDOOR]" if ip in game_state.get("backdoors", []) else ""
            lines.append(f"  → {ip} - {conn_node['description']} [{safety}]{backdoor}")
        
        return None, lines

    # Ping - probe a connected node
    if cmd.startswith("ping "):
        if not game_state.get_flag("grid_scanned"):
            return None, [">> Scan the network first."]
        
        target = cmd[5:].strip()
        if target not in node["connections"]:
            return None, [f">> {target} not directly reachable from {current_ip}."]
        
        target_node = get_node(target)
        safety = "SAFE" if target_node["safe"] else f"MONITORED (+{target_node.get('detection_increase', 20)}% detection)"
        backdoor = " [BACKDOOR INSTALLED]" if target in game_state.get("backdoors", []) else ""
        
        lines = [
            f">> Ping {target} successful:",
            f"   - {target_node['description']}",
            f"   - Status: {safety}{backdoor}",
            f"   - Zone: {get_zone_info(target)}"
        ]
        
        if target == "10.0.0.1":
            lines.append("   - ** EXIT NODE DETECTED **")
        
        return None, lines

    # Trace - move to a connected node
    if cmd.startswith("trace "):
        if not game_state.get_flag("grid_scanned"):
            return None, [">> Cannot navigate blind. Scan first."]
        
        target = cmd[6:].strip()
        if target not in node["connections"]:
            return None, [f">> {target} is not directly connected. Use 'traceroute' to find path."]
        
        # Move to new position
        game_state.set("grid_position", target)
        history = game_state.get("path_history", [])
        history.append(target)
        game_state.set("path_history", history)

        lines = [f">> Tracing route to {target}...", f">> Arrived: {get_node(target)['description']}"]

        # Check for detection
        target_node = get_node(target)
        if not target_node["safe"] and target not in game_state.get("backdoors", []):
            inc = target_node.get("detection_increase", 20)
            new_level = add_detection(game_state, inc)
            lines += [
                f">> ALERT: Intrusion detection triggered!",
                f">> Detection +{inc}% → {new_level}%"
            ]
            
            # Add atmospheric message
            whisper = get_whisper_message(new_level)
            if whisper:
                lines.append(whisper)
            
            # Check for capture
            if new_level >= 100:
                return transition_to_room("security_cell", [
                    ">> DETECTION MAXED!",
                    ">> Security lockdown initiated.",
                    ">> You've been traced and captured...",
                    ">> Redirecting to Security Cell..."
                ])
        elif target in game_state.get("backdoors", []):
            lines.append(">> Backdoor access - undetected entry.")
        
        return None, lines

    # Traceroute - find path to any node
    if cmd.startswith("traceroute "):
        if not game_state.get_flag("grid_scanned"):
            return None, [">> Network topology unknown."]
        
        target = cmd[11:].strip()
        if target not in WHISPER_GRID:
            return None, [">> Invalid IP address."]
        
        path = find_path(current_ip, target)
        if not path:
            return None, [">> No route found to " + target]
        
        detection_cost = calculate_detection_cost(path, game_state)
        
        lines = [">> Traceroute to " + target + ":"]
        for i, ip in enumerate(path):
            node_info = get_node(ip)
            prefix = "  " + ("└─" if i == len(path)-1 else "├─")
            safety = " [SAFE]" if node_info["safe"] else f" [+{node_info.get('detection_increase', 20)}%]"
            backdoor = " [BACKDOOR]" if ip in game_state.get("backdoors", []) else ""
            current = " ← YOU ARE HERE" if ip == current_ip else ""
            lines.append(f"{prefix} {ip}: {node_info['description']}{safety}{backdoor}{current}")
        
        lines.append("")
        lines.append(f">> Total hops: {len(path)-1}")
        lines.append(f">> Estimated detection increase: +{detection_cost}%")
        lines.append(f">> Current detection: {detection}% → Would be: {min(100, detection + detection_cost)}%")
        
        return None, lines

    # Backdoor - create persistent safe access
    if cmd.startswith("backdoor "):
        target = cmd[9:].strip()
        
        if target not in node["connections"]:
            return None, [">> Can only backdoor directly connected nodes."]
        
        if target not in BACKDOOR_CAPABLE:
            return None, [">> This node's architecture doesn't support backdoors."]
        
        if target in game_state.get("backdoors", []):
            return None, [">> Backdoor already installed."]
        
        if len(game_state.get("backdoors", [])) >= 2:
            return None, [">> Maximum backdoors (2) already installed."]
        
        backdoors = game_state.get("backdoors", [])
        backdoors.append(target)
        game_state.set("backdoors", backdoors)
        
        return None, [
            f">> Installing backdoor on {target}...",
            ">> Success! This node can now be accessed without detection.",
            f">> Backdoors installed: {len(backdoors)}/2"
        ]

    # History command
    if cmd in ("history", "path"):
        path = game_state.get("path_history", [])
        if len(path) <= 1:
            return None, [">> No movement history yet."]
        
        lines = [">> Route history:"]
        for i, ip in enumerate(path):
            lines.append(f"   {i}. {ip} - {get_node(ip)['description']}")
        return None, lines

    # Scan neighbors (quick local scan)
    if cmd in ("scan neighbors", "neighbors", "ls"):
        lines = [f">> Adjacent nodes from {current_ip}:"]
        for ip in node["connections"]:
            conn_node = get_node(ip)
            safety = "SAFE" if conn_node["safe"] else f"RISK +{conn_node.get('detection_increase', 20)}%"
            backdoor = " [BD]" if ip in game_state.get("backdoors", []) else ""
            lines.append(f"   {ip} [{safety}]{backdoor}")
        return None, lines

    # Spoof IP - one-time detection reduction
    if cmd == "spoof ip":
        if game_state.get_flag("grid_spoofed"):
            return None, [">> IP already spoofed. One-time use only."]
        
        if detection < 30:
            return None, [">> No need to spoof - detection still low."]
        
        game_state.set_flag("grid_spoofed", True)
        old_detection = detection
        game_state.set("detection_level", max(0, detection - 25))
        
        return None, [
            ">> Spoofing IP address...",
            f">> Success! Detection reduced: {old_detection}% → {get_detection(game_state)}%",
            ">> Spoof exhausted. Use wisely."
        ]

    # Inject noise - reduce next detection hit
    if cmd == "inject noise":
        if game_state.get_flag("grid_noise_injected"):
            return None, [">> Noise packets already in the stream."]
        
        game_state.set_flag("grid_noise_injected", True)
        return None, [
            ">> Injecting noise packets into data stream...",
            ">> Success! Next monitored node will trigger -10% detection.",
            ">> Effect active for one transition."
        ]

    # Proxy chain - show safe path if possible
    if cmd == "proxy chain":
        if not game_state.get_flag("grid_scanned"):
            return None, [">> Network not mapped."]
        
        # Try to find a safe path to exit
        all_paths = []
        exit_ip = "10.0.0.1"
        
        # Basic BFS to find all paths (limited depth)
        queue = [(current_ip, [current_ip], 0)]
        while queue and len(all_paths) < 3:
            pos, path, depth = queue.pop(0)
            if depth > 8:  # Limit search depth
                continue
                
            if pos == exit_ip:
                all_paths.append(path)
                continue
                
            for next_ip in get_node(pos)["connections"]:
                if next_ip not in path:
                    queue.append((next_ip, path + [next_ip], depth + 1))
        
        if not all_paths:
            return None, [">> No proxy chain found to exit."]
        
        # Find safest path
        best_path = min(all_paths, key=lambda p: calculate_detection_cost(p, game_state))
        cost = calculate_detection_cost(best_path, game_state)
        
        lines = [">> Analyzing proxy chains to exit..."]
        lines.append(f">> Safest route found ({cost}% detection):")
        for ip in best_path[1:]:  # Skip current position
            lines.append(f"   → {ip}")
        
        return None, lines

    # Connect exit - final escape
    if cmd == "connect exit":
        if not is_exit(current_ip):
            return None, [">> No exit node at this location."]
        
        if detection >= 80:
            return None, [
                ">> EXIT BLOCKED - Detection too high!",
                f">> Current: {detection}% (must be below 80%)",
                ">> They know you're here. Escape impossible."
            ]
        
        # Success!
        return transition_to_room("whisper_5", [
            ">> Initiating exit protocol...",
            f">> Final detection level: {detection}%",
            ">> Connection established to external network.",
            "",
            ">> You've navigated the labyrinth successfully.",
            ">> Slipping through the digital cracks...",
            ">> Reality awaits on the other side."
        ])

    # Progress command
    if cmd == "progress":
        lines = [">> GRID NAVIGATION PROGRESS:"]
        lines.append(f"   Current Position: {current_ip}")
        lines.append(f"   Nodes Visited: {len(set(game_state.get('path_history', [])))}/{len(WHISPER_GRID)}")
        lines.append(f"   Detection Level: {detection}%")
        lines.append(f"   Backdoors: {len(game_state.get('backdoors', []))}/2")
        lines.append(f"   Tools Used: " + ", ".join([
            "Spoofed" if game_state.get_flag("grid_spoofed") else "",
            "Noise" if game_state.get_flag("grid_noise_injected") else ""
        ]).strip(", ") or "None")
        
        # Distance to exit
        exit_path = find_path(current_ip, "10.0.0.1")
        if exit_path:
            lines.append(f"   Distance to Exit: {len(exit_path)-1} hops")
        
        return None, lines

    return None, [">> Unknown command. Try 'help' for available options."]

# ============================================================================
# HELP
# ============================================================================

def get_available_commands():
    return [
        "=== BASIC NAVIGATION ===",
        "scan network       - map the network topology",
        "map               - show local area connections",
        "ping [IP]         - probe an adjacent node",
        "trace [IP]        - move to a connected node",
        "traceroute [IP]   - find path to any node",
        "",
        "=== ADVANCED TOOLS ===",
        "backdoor [IP]     - install persistent access (max 2)",
        "proxy chain       - find safest route to exit",
        "spoof ip          - reduce detection by 25% (once)",
        "inject noise      - reduce next detection by 10% (once)",
        "",
        "=== STATUS ===",
        "history           - show movement history",
        "neighbors         - list adjacent nodes",
        "progress          - show overall progress",
        "",
        "=== OBJECTIVE ===",
        "connect exit      - escape when at 10.0.0.1 (detection < 80%)",
        "",
        "TIP: Some nodes can be backdoored for safe passage.",
        "TIP: Plan your route - detection accumulates!"
    ]
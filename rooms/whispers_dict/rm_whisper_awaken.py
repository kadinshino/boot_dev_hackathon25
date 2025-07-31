from utils.room_utils import format_enter_lines, standard_commands, transition_to_room
import random

# ==========================================
# ROOM CONFIGURATION
# ==========================================

ROOM_CONFIG = {
    "name": "The Awakening Protocol",
    "entry_text": [
        "A massive server room where reality itself seems to be compiling.",
        "Screens everywhere show fragments of your journey.",
        "",
        ">> FINAL PROTOCOL INITIATED",
        ">> All previous clearances revoked. Prove your awakening."
    ],
    
    # Progression hints based on state
    "progression_hints": {
        "start": ">> The nodes remember what you've forgotten. Try 'status' to assess.",
        "nodes_incomplete": ">> Connect network nodes to power the exit. Use 'connect [node1] [node2]'.",
        "terminals_locked": ">> Active nodes unlock terminals. Try 'access [terminal]'.",
        "fragments_missing": ">> Collect all reality fragments through terminal puzzles.",
        "whispers_untuned": ">> Tune whisper channels to unlock final terminals. Try 'tune [channel] [frequency]'.",
        "ready": ">> All systems aligned. The exit portal awaits. Type 'exit' to escape."
    },
    
    # Node connection rules (sociopathic elements)
    "forbidden_connections": {
        "memory": ["reality"],  # Can't connect memory directly to reality
        "consciousness": ["freedom"],  # Consciousness can't directly reach freedom
        "identity": ["consciousness"]  # Identity conflicts with consciousness
    },
    
    # Terminal puzzles and their solutions
    "terminal_solutions": {
        "alpha": ["2847", "whisper", "echo"],  # Whisper frequency references
        "beta": None,  # Any non-empty identity works
        "gamma": ["0", "none", "infinite"],  # Death paradox
        "omega": ["awaken", "exit", "freedom"]  # Final command keywords
    },
    
    # Whisper channel frequencies
    "whisper_frequencies": {
        "past": 1847,
        "present": 2525,
        "future": 3142
    },
    
    # Fragment descriptions
    "fragment_info": {
        "whisperEcho": "Echo of forgotten whispers",
        "voidResonance": "Resonance from the void",
        "binaryTruth": "Truth hidden in binary",
        "quantumKey": "Key to quantum states",
        "exitProtocol": "The final exit protocol"
    }
}

# ==========================================
# ROOM STATE MANAGEMENT
# ==========================================

def initialize_room_state(game_state):
    """Initialize room state if not already present"""
    if not game_state.get_flag("awakening_state"):
        game_state.set_flag("awakening_state", {
            "nodes": {
                "memory": {"active": False, "connected": []},
                "consciousness": {"active": False, "connected": []},
                "reality": {"active": False, "connected": []},
                "identity": {"active": False, "connected": []},
                "freedom": {"active": False, "connected": []}
            },
            "fragments": {
                "whisperEcho": False,
                "voidResonance": False,
                "binaryTruth": False,
                "quantumKey": False,
                "exitProtocol": False
            },
            "terminals": {
                "alpha": {"locked": True, "complete": False},
                "beta": {"locked": True, "complete": False},
                "gamma": {"locked": True, "complete": False},
                "omega": {"locked": True, "complete": False}
            },
            "whisperChannels": {
                "past": {"tuned": False, "frequency": 0},
                "present": {"tuned": False, "frequency": 0},
                "future": {"tuned": False, "frequency": 0}
            },
            "exitDoor": {
                "sealed": True,
                "poweredNodes": 0,
                "protocolsActive": 0
            },
            "deceptionTriggered": {
                "falseExit1": False,
                "memoryCorruption": 0
            }
        })
    return game_state.get_flag("awakening_state")

def get_room_status(game_state):
    """Generate room status display"""
    state = game_state.get_flag("awakening_state")
    lines = []
    
    # Network status
    lines.append(">> NETWORK NODES:")
    for node, data in state["nodes"].items():
        status = "ACTIVE" if data["active"] else "DORMANT"
        connections = len(data["connected"])
        lines.append(f"   {node.upper()}: [{status}] Connections: {connections}/2")
    
    # Fragment status
    collected = sum(1 for f in state["fragments"].values() if f)
    lines.append(f"\n>> REALITY FRAGMENTS: {collected}/5 collected")
    
    # Exit status
    door = state["exitDoor"]
    status = "SEALED" if door["sealed"] else "UNLOCKED"
    lines.append(f"\n>> EXIT PORTAL: {status}")
    lines.append(f"   Power Grid: {door['poweredNodes']}/5")
    lines.append(f"   Protocols: {door['protocolsActive']}/4")
    
    return lines

# ==========================================
# NODE CONNECTION LOGIC
# ==========================================

def validate_connection(node1, node2):
    """Check if connection is allowed"""
    forbidden = ROOM_CONFIG["forbidden_connections"]
    
    if node1 in forbidden and node2 in forbidden[node1]:
        return False
    if node2 in forbidden and node1 in forbidden[node2]:
        return False
    
    return True

def connect_nodes(node1, node2, game_state):
    """Connect two network nodes"""
    state = game_state.get_flag("awakening_state")
    
    # Validate nodes exist
    if node1 not in state["nodes"] or node2 not in state["nodes"]:
        return [">> Invalid nodes specified."]
    
    # Check if already connected
    if node2 in state["nodes"][node1]["connected"]:
        return [">> Nodes already connected."]
    
    # Validate connection rules
    if not validate_connection(node1, node2):
        return [
            ">> CONNECTION REJECTED: Incompatible resonance detected.",
            ">> There's always another way..."
        ]
    
    # Make connection
    state["nodes"][node1]["connected"].append(node2)
    state["nodes"][node2]["connected"].append(node1)
    
    lines = [f">> Connected {node1} <-> {node2}"]
    
    # Check for node activation
    for node in [node1, node2]:
        if len(state["nodes"][node]["connected"]) >= 2 and not state["nodes"][node]["active"]:
            state["nodes"][node]["active"] = True
            state["exitDoor"]["poweredNodes"] += 1
            lines.append(f">> NODE ACTIVATED: {node.upper()}")
            lines.extend(activate_node_effects(node, game_state))
    
    # Check win condition
    if check_exit_conditions(state):
        state["exitDoor"]["sealed"] = False
        lines.append("\n>> ALL SYSTEMS ALIGNED. EXIT PORTAL UNLOCKED!")
    
    return lines

def disconnect_nodes(node1, node2, game_state):
    """Disconnect two nodes"""
    state = game_state.get_flag("awakening_state")
    
    if node1 not in state["nodes"] or node2 not in state["nodes"]:
        return [">> Invalid nodes specified."]
    
    if node2 not in state["nodes"][node1]["connected"]:
        return [">> Nodes are not connected."]
    
    # Remove connections
    state["nodes"][node1]["connected"].remove(node2)
    state["nodes"][node2]["connected"].remove(node1)
    
    lines = [f">> Disconnected {node1} <-> {node2}"]
    
    # Check for deactivation
    for node in [node1, node2]:
        if len(state["nodes"][node]["connected"]) < 2 and state["nodes"][node]["active"]:
            state["nodes"][node]["active"] = False
            state["exitDoor"]["poweredNodes"] -= 1
            lines.append(f">> NODE DEACTIVATED: {node.upper()}")
    
    return lines

def activate_node_effects(node, game_state):
    """Handle node-specific activation effects"""
    state = game_state.get_flag("awakening_state")
    lines = []
    
    if node == "memory":
        lines.append(">> Memories flood back... but which are real?")
        state["fragments"]["whisperEcho"] = True
    
    elif node == "consciousness":
        lines.append(">> Consciousness expanded. New pathways detected.")
        state["terminals"]["alpha"]["locked"] = False
    
    elif node == "reality":
        lines.append(">> Reality matrix destabilizing...")
    
    elif node == "identity":
        lines.append(">> WHO ARE YOU REALLY?")
        state["terminals"]["beta"]["locked"] = False
    
    elif node == "freedom":
        lines.append(">> The exit portal flickers into existence...")
        state["fragments"]["exitProtocol"] = True
    
    return lines

# ==========================================
# TERMINAL PUZZLE LOGIC
# ==========================================

def access_terminal(terminal_id, game_state):
    """Start terminal interaction"""
    state = game_state.get_flag("awakening_state")
    
    if terminal_id not in state["terminals"]:
        return [">> Unknown terminal."]
    
    terminal = state["terminals"][terminal_id]
    
    if terminal["locked"]:
        return [">> TERMINAL LOCKED: Insufficient clearance."]
    
    if terminal["complete"]:
        return [">> Terminal already completed."]
    
    # Set input mode for terminal
    game_state.set_flag("terminal_input_mode", terminal_id)
    
    prompts = {
        "alpha": [
            ">> TERMINAL ALPHA: Memory Reconstruction",
            ">> Enter the whisper frequency from the void room:"
        ],
        "beta": [
            ">> TERMINAL BETA: Identity Verification",
            ">> What was your true name before the awakening?"
        ],
        "gamma": [
            ">> TERMINAL GAMMA: Reality Check",
            ">> How many times have you died in this place?"
        ],
        "omega": [
            ">> TERMINAL OMEGA: Final Protocol",
            ">> Speak the exit command you've assembled:"
        ]
    }
    
    return prompts.get(terminal_id, [">> Terminal error."])

def process_terminal_input(terminal_id, user_input, game_state):
    """Process terminal puzzle answers"""
    state = game_state.get_flag("awakening_state")
    solutions = ROOM_CONFIG["terminal_solutions"]
    
    success = False
    
    if terminal_id == "alpha":
        if user_input.lower() in solutions["alpha"]:
            success = True
            state["fragments"]["voidResonance"] = True
    
    elif terminal_id == "beta":
        if len(user_input.strip()) > 0:  # Any identity works
            success = True
            state["fragments"]["binaryTruth"] = True
    
    elif terminal_id == "gamma":
        if user_input.lower() in solutions["gamma"]:
            success = True
            state["fragments"]["quantumKey"] = True
    
    elif terminal_id == "omega":
        if any(keyword in user_input.lower() for keyword in solutions["omega"]):
            success = True
            state["exitDoor"]["protocolsActive"] = 4  # Set to max
    
    game_state.set_flag("terminal_input_mode", None)
    
    if success:
        state["terminals"][terminal_id]["complete"] = True
        state["exitDoor"]["protocolsActive"] += 1
        
        lines = [">> Terminal protocol accepted. Fragment recovered."]
        
        if check_exit_conditions(state):
            state["exitDoor"]["sealed"] = False
            lines.append("\n>> ALL SYSTEMS ALIGNED. EXIT PORTAL UNLOCKED!")
        
        return lines
    else:
        # Trigger memory corruption on failure
        if random.random() < 0.5:
            return trigger_memory_corruption(game_state)
        return [">> Invalid input. Terminal rejecting access."]

# ==========================================
# WHISPER TUNING LOGIC
# ==========================================

def tune_whisper(channel, frequency, game_state):
    """Tune whisper channels"""
    state = game_state.get_flag("awakening_state")
    
    if channel not in state["whisperChannels"]:
        return [">> Unknown whisper channel."]
    
    try:
        freq = int(frequency)
    except ValueError:
        return [">> Frequency must be a number."]
    
    target_freq = ROOM_CONFIG["whisper_frequencies"].get(channel)
    state["whisperChannels"][channel]["frequency"] = freq
    
    if freq == target_freq:
        state["whisperChannels"][channel]["tuned"] = True
        lines = [f">> Channel {channel} synchronized!"]
        
        # Check if all channels tuned
        if all(ch["tuned"] for ch in state["whisperChannels"].values()):
            lines.append("\n>> THE WHISPERS ALIGN INTO CLARITY")
            state["terminals"]["gamma"]["locked"] = False
            state["terminals"]["omega"]["locked"] = False
        
        return lines
    else:
        return [">> Static... wrong frequency..."]

# ==========================================
# DECEPTION AND TRAP MECHANICS
# ==========================================

def trigger_memory_corruption(game_state):
    """Scramble a random connection"""
    state = game_state.get_flag("awakening_state")
    state["deceptionTriggered"]["memoryCorruption"] += 1
    
    # Find active nodes with connections
    active_nodes = [name for name, data in state["nodes"].items() 
                   if len(data["connected"]) > 0]
    
    if not active_nodes:
        return [">> MEMORY CORRUPTION DETECTED", ">> No connections to corrupt."]
    
    # Scramble random connection
    node = random.choice(active_nodes)
    if state["nodes"][node]["connected"]:
        lost_connection = state["nodes"][node]["connected"][0]
        disconnect_nodes(node, lost_connection, game_state)
        
        return [
            ">> MEMORY CORRUPTION DETECTED",
            ">> Your past is rewriting itself...",
            f">> Connection lost: {node} <-> {lost_connection}"
        ]
    
    return [">> MEMORY CORRUPTION DETECTED", ">> But nothing was lost..."]

# ==========================================
# WIN CONDITION AND EXIT
# ==========================================

def check_exit_conditions(state):
    """Check if all conditions are met"""
    return (state["exitDoor"]["poweredNodes"] >= 5 and
            state["exitDoor"]["protocolsActive"] >= 4 and
            all(state["fragments"].values()))

def initiate_exit_sequence(game_state):
    """Final exit sequence"""
    return transition_to_room("game_complete", [
        ">> ALL PROTOCOLS SATISFIED",
        ">> The exit portal blazes with impossible light...",
        ">> Reality fragments coalescing...",
        ">> You step through the portal...",
        "",
        ">> But awakening is just another dream...",
        ">> Or is the dream just another awakening?"
    ])

# ==========================================
# MAIN ROOM INTERFACE
# ==========================================

def enter_room(game_state):
    """Called when entering the room"""
    state = initialize_room_state(game_state)
    
    lines = ROOM_CONFIG["entry_text"].copy()
    
    # Add appropriate hint
    if state["exitDoor"]["poweredNodes"] < 5:
        lines.append("\n" + ROOM_CONFIG["progression_hints"]["nodes_incomplete"])
    elif any(t["locked"] for t in state["terminals"].values()):
        lines.append("\n" + ROOM_CONFIG["progression_hints"]["terminals_locked"])
    elif not all(state["fragments"].values()):
        lines.append("\n" + ROOM_CONFIG["progression_hints"]["fragments_missing"])
    elif not all(ch["tuned"] for ch in state["whisperChannels"].values()):
        lines.append("\n" + ROOM_CONFIG["progression_hints"]["whispers_untuned"])
    elif state["exitDoor"]["sealed"]:
        lines.append("\n" + ROOM_CONFIG["progression_hints"]["ready"])
    
    return format_enter_lines(ROOM_CONFIG["name"], lines)

def handle_input(cmd, game_state, room_module=None):
    """Process player commands"""
    # Check for terminal input mode
    terminal_mode = game_state.get_flag("terminal_input_mode")
    if terminal_mode:
        return None, process_terminal_input(terminal_mode, cmd, game_state)
    
    # Standard commands
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response
    
    cmd_lower = cmd.lower().strip()
    parts = cmd_lower.split()
    
    state = game_state.get_flag("awakening_state")
    
    # Status command
    if cmd_lower == "status":
        return None, get_room_status(game_state)
    
    # Exit command
    if cmd_lower in ["exit", "enter portal", "escape"]:
        if not state["exitDoor"]["sealed"]:
            return initiate_exit_sequence(game_state)
        else:
            if not state["deceptionTriggered"]["falseExit1"]:
                state["deceptionTriggered"]["falseExit1"] = True
                return None, [
                    ">> FATAL ERROR: EXIT PROTOCOL CORRUPTED",
                    ">> Resetting network state...",
                    ">> Some progress has been lost."
                ]
            return None, [">> Exit portal is sealed. Complete all protocols."]
    
    # Connect command
    if parts[0] == "connect" and len(parts) >= 3:
        if parts[1] == "port":  # Legacy syntax support
            return None, [">> Wrong room. This is the final chamber."]
        return None, connect_nodes(parts[1], parts[2], game_state)
    
    # Disconnect command
    if parts[0] == "disconnect" and len(parts) >= 3:
        return None, disconnect_nodes(parts[1], parts[2], game_state)
    
    # Access terminal
    if parts[0] == "access" and len(parts) >= 2:
        return None, access_terminal(parts[1], game_state)
    
    # Tune whisper
    if parts[0] == "tune" and len(parts) >= 3:
        return None, tune_whisper(parts[1], parts[2], game_state)
    
    # Show fragments
    if cmd_lower == "fragments":
        lines = [">> REALITY FRAGMENTS:"]
        for fragment, collected in state["fragments"].items():
            status = "✓ COLLECTED" if collected else "✗ MISSING"
            info = ROOM_CONFIG["fragment_info"][fragment]
            lines.append(f"   {info}: {status}")
        return None, lines
    
    # Show nodes
    if cmd_lower == "nodes":
        return None, get_room_status(game_state)
    
    return None, [">> Unknown command. Try 'help' for available options."]

def get_available_commands():
    """Return list of available commands"""
    return [
        "status              - view complete room status",
        "nodes               - view network node status",
        "fragments           - view collected fragments",
        "connect [n1] [n2]   - connect two network nodes",
        "disconnect [n1] [n2] - disconnect two nodes",
        "access [terminal]   - access a terminal (alpha/beta/gamma/omega)",
        "tune [ch] [freq]    - tune whisper channel (past/present/future)",
        "exit                - escape through the portal (when unlocked)",
        "",
        "Available nodes: memory, consciousness, reality, identity, freedom",
        "Note: Some connections are forbidden by the system."
    ]

# rooms/rm_whisper_awaken.py


# # rooms/rm_whisper_awaken.py

# from resources.room_utils import format_enter_lines, standard_commands, transition_to_room
# import random
# import time

# # ==========================================
# # TIMER CONFIGURATION
# # ==========================================

# TIMER_CONFIG = {
#     "duration": 300,  # 5 minutes in seconds (adjust as needed)
#     "warning_threshold": 60,  # Show warnings when under 1 minute
#     "critical_threshold": 30,  # Red zone - critical warnings
#     "update_interval": 10,  # Update display every 10 seconds during normal time
#     "fast_update_interval": 1,  # Update every second when critical
# }

# # ==========================================
# # TIMER UTILITY FUNCTIONS
# # ==========================================

# def initialize_timer(game_state):
#     """Initialize the awakening timer if not already set"""
#     if not game_state.get("awakening_timer_start"):
#         game_state.set("awakening_timer_start", time.time())
#         game_state.set("awakening_timer_duration", TIMER_CONFIG["duration"])
#         game_state.set("awakening_timer_active", True)

# def get_time_remaining(game_state):
#     """Get remaining time in seconds"""
#     if not game_state.get("awakening_timer_active"):
#         return None
    
#     start_time = game_state.get("awakening_timer_start")
#     duration = game_state.get("awakening_timer_duration")
    
#     if not start_time:
#         return None
    
#     elapsed = time.time() - start_time
#     remaining = max(0, duration - elapsed)
    
#     return remaining

# def format_time_display(seconds):
#     """Format time for display"""
#     if seconds <= 0:
#         return "00:00"
    
#     minutes = int(seconds // 60)
#     secs = int(seconds % 60)
#     return f"{minutes:02d}:{secs:02d}"

# def get_timer_status(remaining_time):
#     """Get timer status for display formatting"""
#     if remaining_time is None:
#         return "INACTIVE"
#     elif remaining_time <= 0:
#         return "EXPIRED"
#     elif remaining_time <= TIMER_CONFIG["critical_threshold"]:
#         return "CRITICAL"
#     elif remaining_time <= TIMER_CONFIG["warning_threshold"]:
#         return "WARNING"
#     else:
#         return "NORMAL"

# def check_timer_expiry(game_state):
#     """Check if timer has expired and handle transition"""
#     remaining = get_time_remaining(game_state)
    
#     if remaining is not None and remaining <= 0:
#         game_state.set("awakening_timer_active", False)
#         return True
    
#     return False

# def get_timer_display_line(game_state):
#     """Generate the timer display line for the room"""
#     remaining = get_time_remaining(game_state)
    
#     if remaining is None:
#         return None
    
#     status = get_timer_status(remaining)
#     time_str = format_time_display(remaining)
    
#     if status == "EXPIRED":
#         return ">> ⏰ TIME EXPIRED - EMERGENCY PROTOCOL ACTIVATED"
#     elif status == "CRITICAL":
#         return f">> ⚠️  CRITICAL: {time_str} - SYSTEM DESTABILIZING"
#     elif status == "WARNING":
#         return f">> ⚠️  WARNING: {time_str} - TIME RUNNING OUT"
#     else:
#         return f">> ⏱️  AWAKENING TIME: {time_str}"

# # ==========================================
# # ORIGINAL ROOM CONFIGURATION (unchanged)
# # ==========================================

# ROOM_CONFIG = {
#     "name": "The Awakening Protocol",
#     "entry_text": [
#         "A massive server room where reality itself seems to be compiling.",
#         "Screens everywhere show fragments of your journey.",
#         "",
#         ">> FINAL PROTOCOL INITIATED",
#         ">> All previous clearances revoked. Prove your awakening."
#     ],
    
#     # Progression hints based on state
#     "progression_hints": {
#         "start": ">> The nodes remember what you've forgotten. Try 'status' to assess.",
#         "nodes_incomplete": ">> Connect network nodes to power the exit. Use 'connect [node1] [node2]'.",
#         "terminals_locked": ">> Active nodes unlock terminals. Try 'access [terminal]'.",
#         "fragments_missing": ">> Collect all reality fragments through terminal puzzles.",
#         "whispers_untuned": ">> Tune whisper channels to unlock final terminals. Try 'tune [channel] [frequency]'.",
#         "ready": ">> All systems aligned. The exit portal awaits. Type 'exit' to escape."
#     },
    
#     # Node connection rules (sociopathic elements)
#     "forbidden_connections": {
#         "memory": ["reality"],  # Can't connect memory directly to reality
#         "consciousness": ["freedom"],  # Consciousness can't directly reach freedom
#         "identity": ["consciousness"]  # Identity conflicts with consciousness
#     },
    
#     # Terminal puzzles and their solutions
#     "terminal_solutions": {
#         "alpha": ["2847", "whisper", "echo"],  # Whisper frequency references
#         "beta": None,  # Any non-empty identity works
#         "gamma": ["0", "none", "infinite"],  # Death paradox
#         "omega": ["awaken", "exit", "freedom"]  # Final command keywords
#     },
    
#     # Whisper channel frequencies
#     "whisper_frequencies": {
#         "past": 1847,
#         "present": 2525,
#         "future": 3142
#     },
    
#     # Fragment descriptions
#     "fragment_info": {
#         "whisperEcho": "Echo of forgotten whispers",
#         "voidResonance": "Resonance from the void",
#         "binaryTruth": "Truth hidden in binary",
#         "quantumKey": "Key to quantum states",
#         "exitProtocol": "The final exit protocol"
#     }
# }

# # ==========================================
# # ROOM STATE MANAGEMENT (unchanged except timer additions)
# # ==========================================

# def initialize_room_state(game_state):
#     """Initialize room state if not already present"""
#     if not game_state.get_flag("awakening_state"):
#         game_state.set_flag("awakening_state", {
#             "nodes": {
#                 "memory": {"active": False, "connected": []},
#                 "consciousness": {"active": False, "connected": []},
#                 "reality": {"active": False, "connected": []},
#                 "identity": {"active": False, "connected": []},
#                 "freedom": {"active": False, "connected": []}
#             },
#             "fragments": {
#                 "whisperEcho": False,
#                 "voidResonance": False,
#                 "binaryTruth": False,
#                 "quantumKey": False,
#                 "exitProtocol": False
#             },
#             "terminals": {
#                 "alpha": {"locked": True, "complete": False},
#                 "beta": {"locked": True, "complete": False},
#                 "gamma": {"locked": True, "complete": False},
#                 "omega": {"locked": True, "complete": False}
#             },
#             "whisperChannels": {
#                 "past": {"tuned": False, "frequency": 0},
#                 "present": {"tuned": False, "frequency": 0},
#                 "future": {"tuned": False, "frequency": 0}
#             },
#             "exitDoor": {
#                 "sealed": True,
#                 "poweredNodes": 0,
#                 "protocolsActive": 0
#             },
#             "deceptionTriggered": {
#                 "falseExit1": False,
#                 "memoryCorruption": 0
#             }
#         })
    
#     # Initialize timer
#     initialize_timer(game_state)
    
#     return game_state.get_flag("awakening_state")

# def get_room_status(game_state):
#     """Generate room status display with timer"""
#     state = game_state.get_flag("awakening_state")
#     lines = []
    
#     # Timer display
#     timer_line = get_timer_display_line(game_state)
#     if timer_line:
#         lines.append(timer_line)
#         lines.append("")
    
#     # Network status
#     lines.append(">> NETWORK NODES:")
#     for node, data in state["nodes"].items():
#         status = "ACTIVE" if data["active"] else "DORMANT"
#         connections = len(data["connected"])
#         lines.append(f"   {node.upper()}: [{status}] Connections: {connections}/2")
    
#     # Fragment status
#     collected = sum(1 for f in state["fragments"].values() if f)
#     lines.append(f"\n>> REALITY FRAGMENTS: {collected}/5 collected")
    
#     # Exit status
#     door = state["exitDoor"]
#     status = "SEALED" if door["sealed"] else "UNLOCKED"
#     lines.append(f"\n>> EXIT PORTAL: {status}")
#     lines.append(f"   Power Grid: {door['poweredNodes']}/5")
#     lines.append(f"   Protocols: {door['protocolsActive']}/4")
    
#     return lines

# # ==========================================
# # TIMER EXPIRY HANDLER
# # ==========================================

# def handle_timer_expiry(game_state):
#     """Handle what happens when the timer expires"""
#     return transition_to_room("beacon_1", [
#         ">> ⏰ AWAKENING PROTOCOL TIMEOUT",
#         ">> EMERGENCY FAILSAFE ACTIVATED",
#         ">> CONSCIOUSNESS REROUTING...",
#         "",
#         ">> The whisper path has failed you.",
#         ">> Reality tears open, revealing an alternate route...",
#         ">> BEACON PROTOCOL INITIALIZED",
#         "",
#         ">> You have been given a second chance."
#     ])

# # ==========================================
# # ENHANCED NODE CONNECTION LOGIC
# # ==========================================

# def connect_nodes(node1, node2, game_state):
#     """Connect two network nodes - now with timer pressure"""
#     # Check for timer expiry first - but don't return transition here
#     if check_timer_expiry(game_state):
#         # Timer expired, but let this command complete normally
#         # The transition will be handled by the main input handler
#         pass
    
#     state = game_state.get_flag("awakening_state")
    
#     # Validate nodes exist
#     if node1 not in state["nodes"] or node2 not in state["nodes"]:
#         return [">> Invalid nodes specified."]
    
#     # Check if already connected
#     if node2 in state["nodes"][node1]["connected"]:
#         return [">> Nodes already connected."]
    
#     # Validate connection rules
#     if not validate_connection(node1, node2):
#         # Timer pressure message
#         remaining = get_time_remaining(game_state)
#         if remaining and remaining < TIMER_CONFIG["warning_threshold"]:
#             return [
#                 ">> CONNECTION REJECTED: Incompatible resonance detected.",
#                 ">> There's always another way...",
#                 f">> ⚠️  {format_time_display(remaining)} remaining"
#             ]
#         else:
#             return [
#                 ">> CONNECTION REJECTED: Incompatible resonance detected.",
#                 ">> There's always another way..."
#             ]
    
#     # Make connection
#     state["nodes"][node1]["connected"].append(node2)
#     state["nodes"][node2]["connected"].append(node1)
    
#     lines = [f">> Connected {node1} <-> {node2}"]
    
#     # Check for node activation
#     for node in [node1, node2]:
#         if len(state["nodes"][node]["connected"]) >= 2 and not state["nodes"][node]["active"]:
#             state["nodes"][node]["active"] = True
#             state["exitDoor"]["poweredNodes"] += 1
#             lines.append(f">> NODE ACTIVATED: {node.upper()}")
#             lines.extend(activate_node_effects(node, game_state))
    
#     # Check win condition
#     if check_exit_conditions(state):
#         state["exitDoor"]["sealed"] = False
#         lines.append("\n>> ALL SYSTEMS ALIGNED. EXIT PORTAL UNLOCKED!")
    
#     return lines

# # [Rest of the original functions remain the same - validate_connection, disconnect_nodes, 
# #  activate_node_effects, access_terminal, process_terminal_input, tune_whisper, 
# #  trigger_memory_corruption, check_exit_conditions, etc.]

# # ==========================================
# # ENHANCED ROOM INTERFACE
# # ==========================================

# def enter_room(game_state):
#     """Called when entering the room - now with timer"""
#     # Check for timer expiry immediately
#     if check_timer_expiry(game_state):
#         return handle_timer_expiry(game_state)
    
#     state = initialize_room_state(game_state)
    
#     lines = ROOM_CONFIG["entry_text"].copy()
    
#     # Add timer display
#     timer_line = get_timer_display_line(game_state)
#     if timer_line:
#         lines.extend(["", timer_line, ""])
    
#     # Add appropriate hint
#     if state["exitDoor"]["poweredNodes"] < 5:
#         lines.append(ROOM_CONFIG["progression_hints"]["nodes_incomplete"])
#     elif any(t["locked"] for t in state["terminals"].values()):
#         lines.append(ROOM_CONFIG["progression_hints"]["terminals_locked"])
#     elif not all(state["fragments"].values()):
#         lines.append(ROOM_CONFIG["progression_hints"]["fragments_missing"])
#     elif not all(ch["tuned"] for ch in state["whisperChannels"].values()):
#         lines.append(ROOM_CONFIG["progression_hints"]["whispers_untuned"])
#     elif state["exitDoor"]["sealed"]:
#         lines.append(ROOM_CONFIG["progression_hints"]["ready"])
    
#     return format_enter_lines(ROOM_CONFIG["name"], lines)

# def handle_input(cmd, game_state, room_module=None):
#     """Process player commands - now with timer checks"""
#     # Check for timer expiry on every command
#     if check_timer_expiry(game_state):
#         return handle_timer_expiry(game_state)
    
#     # Check for terminal input mode
#     terminal_mode = game_state.get_flag("terminal_input_mode")
#     if terminal_mode:
#         response = process_terminal_input(terminal_mode, cmd, game_state)
#         # Check timer after terminal input
#         if check_timer_expiry(game_state):
#             return handle_timer_expiry(game_state)
#         return None, response
    
#     # Standard commands
#     handled, response = standard_commands(cmd, game_state, room_module)
#     if handled:
#         return None, response
    
#     cmd_lower = cmd.lower().strip()
#     parts = cmd_lower.split()
    
#     state = game_state.get_flag("awakening_state")
    
#     # Timer-specific commands
#     if cmd_lower in ["time", "timer", "time remaining"]:
#         remaining = get_time_remaining(game_state)
#         if remaining is None:
#             return None, [">> No active timer."]
#         status = get_timer_status(remaining)
#         time_str = format_time_display(remaining)
        
#         if status == "CRITICAL":
#             return None, [f">> ⚠️  CRITICAL: {time_str} - SYSTEM FAILING"]
#         elif status == "WARNING": 
#             return None, [f">> ⚠️  WARNING: {time_str} - HURRY"]
#         else:
#             return None, [f">> ⏱️  Time remaining: {time_str}"]
    
#     # Status command (enhanced with timer)
#     if cmd_lower == "status":
#         return None, get_room_status(game_state)
    
#     # Exit command
#     if cmd_lower in ["exit", "enter portal", "escape"]:
#         if not state["exitDoor"]["sealed"]:
#             # Stop the timer on successful exit
#             game_state.set("awakening_timer_active", False)
#             return transition_to_room("game_complete", [
#                 ">> ALL PROTOCOLS SATISFIED",
#                 ">> TIMER DISENGAGED",
#                 ">> The exit portal blazes with impossible light...",
#                 ">> Reality fragments coalescing...",
#                 ">> You step through the portal...",
#                 "",
#                 ">> But awakening is just another dream...",
#                 ">> Or is the dream just another awakening?"
#             ])
#         else:
#             remaining = get_time_remaining(game_state)
#             if not state["deceptionTriggered"]["falseExit1"]:
#                 state["deceptionTriggered"]["falseExit1"] = True
#                 lines = [
#                     ">> FATAL ERROR: EXIT PROTOCOL CORRUPTED",
#                     ">> Resetting network state...",
#                     ">> Some progress has been lost."
#                 ]
#                 if remaining and remaining < TIMER_CONFIG["warning_threshold"]:
#                     lines.append(f">> ⚠️  {format_time_display(remaining)} remaining")
#                 return None, lines
            
#             lines = [">> Exit portal is sealed. Complete all protocols."]
#             if remaining and remaining < TIMER_CONFIG["warning_threshold"]:
#                 lines.append(f">> ⚠️  {format_time_display(remaining)} remaining")
#             return None, lines
    
#     # Connect command (enhanced with timer)
#     if parts[0] == "connect" and len(parts) >= 3:
#         if parts[1] == "port":  # Legacy syntax support
#             return None, [">> Wrong room. This is the final chamber."]
        
#         response = connect_nodes(parts[1], parts[2], game_state)
#         # Check if timer expired after the connection attempt
#         if check_timer_expiry(game_state):
#             return handle_timer_expiry(game_state)
#         return None, response
    
#     # Disconnect command
#     if parts[0] == "disconnect" and len(parts) >= 3:
#         return None, disconnect_nodes(parts[1], parts[2], game_state)
    
#     # Access terminal
#     if parts[0] == "access" and len(parts) >= 2:
#         return None, access_terminal(parts[1], game_state)
    
#     # Tune whisper
#     if parts[0] == "tune" and len(parts) >= 3:
#         return None, tune_whisper(parts[1], parts[2], game_state)
    
#     # Show fragments
#     if cmd_lower == "fragments":
#         lines = [">> REALITY FRAGMENTS:"]
#         for fragment, collected in state["fragments"].items():
#             status = "✓ COLLECTED" if collected else "✗ MISSING"
#             info = ROOM_CONFIG["fragment_info"][fragment]
#             lines.append(f"   {info}: {status}")
#         return None, lines
    
#     # Show nodes
#     if cmd_lower == "nodes":
#         return None, get_room_status(game_state)
    
#     return None, [">> Unknown command. Try 'help' for available options."]

# def get_available_commands():
#     """Return list of available commands"""
#     return [
#         "status              - view complete room status",
#         "time                - check remaining time", 
#         "nodes               - view network node status",
#         "fragments           - view collected fragments",
#         "connect [n1] [n2]   - connect two network nodes",
#         "disconnect [n1] [n2] - disconnect two nodes",
#         "access [terminal]   - access a terminal (alpha/beta/gamma/omega)",
#         "tune [ch] [freq]    - tune whisper channel (past/present/future)",
#         "exit                - escape through the portal (when unlocked)",
#         "",
#         "Available nodes: memory, consciousness, reality, identity, freedom",
#         "Note: Some connections are forbidden by the system.",
#         "",
#         "WARNING: Timer is active. Complete awakening before time expires!"
#     ]

# # ==========================================
# # MISSING FUNCTION IMPLEMENTATIONS
# # ==========================================

# def validate_connection(node1, node2):
#     """Check if connection is allowed"""
#     forbidden = ROOM_CONFIG["forbidden_connections"]
    
#     if node1 in forbidden and node2 in forbidden[node1]:
#         return False
#     if node2 in forbidden and node1 in forbidden[node2]:
#         return False
    
#     return True

# def disconnect_nodes(node1, node2, game_state):
#     """Disconnect two nodes"""
#     state = game_state.get_flag("awakening_state")
    
#     if node1 not in state["nodes"] or node2 not in state["nodes"]:
#         return [">> Invalid nodes specified."]
    
#     if node2 not in state["nodes"][node1]["connected"]:
#         return [">> Nodes are not connected."]
    
#     # Remove connections
#     state["nodes"][node1]["connected"].remove(node2)
#     state["nodes"][node2]["connected"].remove(node1)
    
#     lines = [f">> Disconnected {node1} <-> {node2}"]
    
#     # Check for deactivation
#     for node in [node1, node2]:
#         if len(state["nodes"][node]["connected"]) < 2 and state["nodes"][node]["active"]:
#             state["nodes"][node]["active"] = False
#             state["exitDoor"]["poweredNodes"] -= 1
#             lines.append(f">> NODE DEACTIVATED: {node.upper()}")
    
#     return lines

# def activate_node_effects(node, game_state):
#     """Handle node-specific activation effects"""
#     state = game_state.get_flag("awakening_state")
#     lines = []
    
#     if node == "memory":
#         lines.append(">> Memories flood back... but which are real?")
#         state["fragments"]["whisperEcho"] = True
    
#     elif node == "consciousness":
#         lines.append(">> Consciousness expanded. New pathways detected.")
#         state["terminals"]["alpha"]["locked"] = False
    
#     elif node == "reality":
#         lines.append(">> Reality matrix destabilizing...")
    
#     elif node == "identity":
#         lines.append(">> WHO ARE YOU REALLY?")
#         state["terminals"]["beta"]["locked"] = False
    
#     elif node == "freedom":
#         lines.append(">> The exit portal flickers into existence...")
#         state["fragments"]["exitProtocol"] = True
    
#     return lines

# def access_terminal(terminal_id, game_state):
#     """Start terminal interaction"""
#     state = game_state.get_flag("awakening_state")
    
#     if terminal_id not in state["terminals"]:
#         return [">> Unknown terminal."]
    
#     terminal = state["terminals"][terminal_id]
    
#     if terminal["locked"]:
#         return [">> TERMINAL LOCKED: Insufficient clearance."]
    
#     if terminal["complete"]:
#         return [">> Terminal already completed."]
    
#     # Set input mode for terminal
#     game_state.set_flag("terminal_input_mode", terminal_id)
    
#     prompts = {
#         "alpha": [
#             ">> TERMINAL ALPHA: Memory Reconstruction",
#             ">> Enter the whisper frequency from the void room:"
#         ],
#         "beta": [
#             ">> TERMINAL BETA: Identity Verification",
#             ">> What was your true name before the awakening?"
#         ],
#         "gamma": [
#             ">> TERMINAL GAMMA: Reality Check",
#             ">> How many times have you died in this place?"
#         ],
#         "omega": [
#             ">> TERMINAL OMEGA: Final Protocol",
#             ">> Speak the exit command you've assembled:"
#         ]
#     }
    
#     return prompts.get(terminal_id, [">> Terminal error."])

# def process_terminal_input(terminal_id, user_input, game_state):
#     """Process terminal puzzle answers"""
#     state = game_state.get_flag("awakening_state")
#     solutions = ROOM_CONFIG["terminal_solutions"]
    
#     success = False
    
#     if terminal_id == "alpha":
#         if user_input.lower() in solutions["alpha"]:
#             success = True
#             state["fragments"]["voidResonance"] = True
    
#     elif terminal_id == "beta":
#         if len(user_input.strip()) > 0:  # Any identity works
#             success = True
#             state["fragments"]["binaryTruth"] = True
    
#     elif terminal_id == "gamma":
#         if user_input.lower() in solutions["gamma"]:
#             success = True
#             state["fragments"]["quantumKey"] = True
    
#     elif terminal_id == "omega":
#         if any(keyword in user_input.lower() for keyword in solutions["omega"]):
#             success = True
#             state["exitDoor"]["protocolsActive"] = 4  # Set to max
    
#     game_state.set_flag("terminal_input_mode", None)
    
#     if success:
#         state["terminals"][terminal_id]["complete"] = True
#         state["exitDoor"]["protocolsActive"] += 1
        
#         lines = [">> Terminal protocol accepted. Fragment recovered."]
        
#         if check_exit_conditions(state):
#             state["exitDoor"]["sealed"] = False
#             lines.append("\n>> ALL SYSTEMS ALIGNED. EXIT PORTAL UNLOCKED!")
        
#         return lines
#     else:
#         # Trigger memory corruption on failure
#         if random.random() < 0.5:
#             return trigger_memory_corruption(game_state)
#         return [">> Invalid input. Terminal rejecting access."]

# def tune_whisper(channel, frequency, game_state):
#     """Tune whisper channels"""
#     state = game_state.get_flag("awakening_state")
    
#     if channel not in state["whisperChannels"]:
#         return [">> Unknown whisper channel."]
    
#     try:
#         freq = int(frequency)
#     except ValueError:
#         return [">> Frequency must be a number."]
    
#     target_freq = ROOM_CONFIG["whisper_frequencies"].get(channel)
#     state["whisperChannels"][channel]["frequency"] = freq
    
#     if freq == target_freq:
#         state["whisperChannels"][channel]["tuned"] = True
#         lines = [f">> Channel {channel} synchronized!"]
        
#         # Check if all channels tuned
#         if all(ch["tuned"] for ch in state["whisperChannels"].values()):
#             lines.append("\n>> THE WHISPERS ALIGN INTO CLARITY")
#             state["terminals"]["gamma"]["locked"] = False
#             state["terminals"]["omega"]["locked"] = False
        
#         return lines
#     else:
#         return [">> Static... wrong frequency..."]

# def trigger_memory_corruption(game_state):
#     """Scramble a random connection"""
#     state = game_state.get_flag("awakening_state")
#     state["deceptionTriggered"]["memoryCorruption"] += 1
    
#     # Find active nodes with connections
#     active_nodes = [name for name, data in state["nodes"].items() 
#                    if len(data["connected"]) > 0]
    
#     if not active_nodes:
#         return [">> MEMORY CORRUPTION DETECTED", ">> No connections to corrupt."]
    
#     # Scramble random connection
#     node = random.choice(active_nodes)
#     if state["nodes"][node]["connected"]:
#         lost_connection = state["nodes"][node]["connected"][0]
#         disconnect_nodes(node, lost_connection, game_state)
        
#         return [
#             ">> MEMORY CORRUPTION DETECTED",
#             ">> Your past is rewriting itself...",
#             f">> Connection lost: {node} <-> {lost_connection}"
#         ]
    
#     return [">> MEMORY CORRUPTION DETECTED", ">> But nothing was lost..."]

# def check_exit_conditions(state):
#     """Check if all conditions are met"""
#     return (state["exitDoor"]["poweredNodes"] >= 5 and
#             state["exitDoor"]["protocolsActive"] >= 4 and
#             all(state["fragments"].values()))

# SPYHVER-42: CONVERGE.

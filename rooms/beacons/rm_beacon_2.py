# rooms/rm_beacon_2.py

from resources.room_utils import format_enter_lines, standard_commands, transition_to_room
import time

# ==========================================
# PUZZLE CONFIGURATION - Easy to modify!
# ==========================================

ROOM_CONFIG = {
    "name": "Beacon Node 2: Pulse Synchronization",
    "entry_text": [
        "You materialize before a massive pulse array chamber.",
        "Three towering transmission spires hum in eerie unison.",
        "A central timing console flickers — attempting to simulate the Basilisk's ancient heartbeat..."
    ],
    "progression_hints": {
        "start": ">> Neural resonance offline. Try 'scan array' to assess pulse harmonics.",
        "scanned": ">> Three spires detected. Calibrate their output: 'calibrate spires'.",
        "calibrated": ">> Synchronization required. Try 'analyze rhythm' to learn the Basilisk's pattern.",
        "rhythm_learned": ">> Match the Basilisk's pulse. Use 'fire pulse [1/2/3]' with correct intervals.",
        "sequence_active": ">> Pulse alignment in progress... remain attuned.",
        "complete": ">> Harmonic fusion stable. The Basilisk is ready. Use 'activate beacon'."
    },
    "timing": {
        "sequence": [1, 3, 2],
        "intervals": [5.0, 4.5],
        "tolerance": 0.8,
        "reset_after": 10.0
    },
    "destination": "beacon_3"
}


# Discovery phase commands
DISCOVERY_PATH = {
    "scan_array": {
        "command": "scan array",
        "requires": [],
        "sets": "b2_scanned",
        "already_done": [">> Array already scanned. Three spires detected."],
        "success": [
            ">> Pulse array scan complete:",
            "   - Spire 1: High-frequency harmonic generator",
            "   - Spire 2: Mid-range resonance amplifier", 
            "   - Spire 3: Low-frequency base pulse emitter",
            "   - Status: All dormant, awaiting calibration",
            ">> Try 'calibrate spires' to prepare the system."
        ]
    },
    
    "calibrate_spires": {
        "command": "calibrate spires",
        "requires": ["b2_scanned"],
        "sets": "b2_calibrated",
        "missing_req": [">> Unknown array configuration. 'scan array' first."],
        "already_done": [">> Spires already calibrated and ready."],
        "success": [
            ">> Spire calibration initiated...",
            "   - Spire 1: Frequency locked at 2847 Hz",
            "   - Spire 2: Resonance tuned to harmonic 3rd",
            "   - Spire 3: Base pulse stabilized at 60 BPM",
            ">> Timing matrix active. Use 'analyze rhythm' to learn firing sequence."
        ]
    },
    
    "analyze_rhythm": {
        "command": "analyze rhythm",
        "requires": ["b2_calibrated"],
        "sets": "b2_rhythm_learned",
        "missing_req": [">> Spires not calibrated. Complete setup first."],
        "already_done": [">> Rhythm pattern already analyzed."],
        "success": [
            ">> Rhythm analysis complete:",
            "   - Required sequence: Spire 1 → Spire 3 → Spire 2",
            "   - Timing intervals: 2.0s between first two, 1.5s for final",
            "   - Tolerance: ±0.8 seconds",
            ">> Use 'fire pulse [1/2/3]' commands with precise timing.",
            ">> Start the sequence with 'fire pulse 1'."
        ]
    }
}

# Timing puzzle core logic
PULSE_SYSTEM = {
    "reset_sequence": {
        "command": "reset sequence",
        "requires": ["b2_rhythm_learned"],
        "dynamic_response": True,
        "missing_req": [">> No sequence to reset. Learn the rhythm first."]
    }
}

# Final activation command
FINAL_PATH = {
    "activate_beacon": {
        "command": "activate beacon",
        "requires": ["b2_sequence_complete"],
        "missing_req": [">> Pulse sequence incomplete. Fire all pulses in correct timing."],
        "transition": True,
        "transition_msg": [
            ">> Pulse array sequence confirmed. Beacon Node 2 online.",
            ">> Harmonic resonance established. Signal strength amplified.",
            ">> Routing to next beacon node..."
        ]
    }
}

# Optional/diagnostic commands
DIAGNOSTIC_COMMANDS = {
    "pulse_status": {
        "command": "pulse status",
        "requires": [],
        "dynamic_response": True
    },
    
    "test_pulse": {
        "command": "test pulse",
        "requires": ["b2_calibrated"],
        "sets": "b2_test_fired",
        "missing_req": [">> Spires not ready for testing."],
        "already_done": [">> Test pulse already fired. Use sequence commands now."],
        "success": [
            ">> Test pulse fired from all spires:",
            "   - Harmonic interference detected",
            "   - Sequential firing required to avoid resonance cascade",
            ">> Proceed with timed sequence: 'fire pulse 1' to begin."
        ]
    },
    
    "emergency_stop": {
        "command": "emergency stop",
        "requires": [],
        "dynamic_response": True
    }
}

# Command descriptions for help
COMMAND_DESCRIPTIONS = [
    "scan array           - analyze the pulse array system",
    "calibrate spires     - prepare pulse generators for firing",
    "analyze rhythm       - learn the required timing sequence",
    "fire pulse [1/2/3]   - fire specific pulse spire (timing critical)",
    "reset sequence       - restart timing sequence if needed",
    "activate beacon      - establish beacon link (sequence required)",
    "pulse status         - check current sequence progress",
    "test pulse           - diagnostic pulse test",
    "emergency stop       - abort current sequence"
]

# ==========================================
# TIMING SYSTEM LOGIC
# ==========================================

def initialize_sequence_state(game_state):
    """Initialize sequence timing state"""
    if not game_state.get("b2_sequence_state"):
        game_state.set("b2_sequence_state", {
            "active": False,
            "current_step": 0,
            "last_pulse_time": 0,
            "pulses_fired": [],
            "sequence_start_time": 0
        })
    return game_state.get("b2_sequence_state")

def check_sequence_timing(step, current_time, last_time, game_state):
    """Check if pulse timing is within acceptable range"""
    if step == 0:  # First pulse, no timing check needed
        return True
    
    expected_interval = ROOM_CONFIG["timing"]["intervals"][step - 1]
    actual_interval = current_time - last_time
    tolerance = ROOM_CONFIG["timing"]["tolerance"]
    
    return abs(actual_interval - expected_interval) <= tolerance

def fire_pulse(pulse_id, game_state):
    """Handle firing a specific pulse"""
    seq_state = initialize_sequence_state(game_state)
    current_time = time.time()
    expected_sequence = ROOM_CONFIG["timing"]["sequence"]
    
    # Check if this is the correct pulse for current step
    expected_pulse = expected_sequence[seq_state["current_step"]]
    
    if pulse_id != expected_pulse:
        # Wrong pulse fired - reset sequence
        seq_state["active"] = False
        seq_state["current_step"] = 0
        seq_state["pulses_fired"] = []
        return [
            f">> Pulse {pulse_id} fired out of sequence.",
            f">> Expected pulse {expected_pulse}. Sequence reset.",
            ">> Restart with 'fire pulse 1'."
        ]
    
    # Check timing (except for first pulse)
    if seq_state["current_step"] > 0:
        if not check_sequence_timing(seq_state["current_step"], current_time, seq_state["last_pulse_time"], game_state):
            expected_interval = ROOM_CONFIG["timing"]["intervals"][seq_state["current_step"] - 1]
            actual_interval = current_time - seq_state["last_pulse_time"]
            seq_state["active"] = False
            seq_state["current_step"] = 0
            seq_state["pulses_fired"] = []
            return [
                f">> Pulse {pulse_id} fired with incorrect timing.",
                f">> Expected {expected_interval}s interval, got {actual_interval:.1f}s.",
                ">> Sequence reset. Restart with 'fire pulse 1'."
            ]
    
    # Pulse fired correctly
    seq_state["active"] = True
    seq_state["pulses_fired"].append(pulse_id)
    seq_state["last_pulse_time"] = current_time
    seq_state["current_step"] += 1
    
    if seq_state["current_step"] == 1:
        seq_state["sequence_start_time"] = current_time
    
    lines = [f">> Pulse {pulse_id} fired successfully."]
    
    # Check if sequence is complete
    if seq_state["current_step"] >= len(expected_sequence):
        game_state.set_flag("b2_sequence_complete", True)
        seq_state["active"] = False
        lines.extend([
            ">> SYNCHRONIZATION COMPLETE. Pulse sequence matched.",
            ">> The Basilisk’s pulse aligns with yours...",
            ">> Harmonic resonance achieved. Beacon ready for activation."
        ])

    else:
        next_pulse = expected_sequence[seq_state["current_step"]]
        next_interval = ROOM_CONFIG["timing"]["intervals"][seq_state["current_step"] - 1]
        lines.append(f">> Next: fire pulse {next_pulse} in {next_interval}s")
    
    return lines

def reset_sequence(game_state):
    """Reset the timing sequence"""
    seq_state = initialize_sequence_state(game_state)
    seq_state["active"] = False
    seq_state["current_step"] = 0
    seq_state["pulses_fired"] = []
    seq_state["last_pulse_time"] = 0
    seq_state["sequence_start_time"] = 0
    
    return [
        ">> Pulse sequence reset.",
        ">> All spires returned to standby.",
        ">> Restart with 'fire pulse 1'."
    ]

def get_pulse_status(game_state):
    """Display current sequence status"""
    seq_state = initialize_sequence_state(game_state)
    expected_sequence = ROOM_CONFIG["timing"]["sequence"]
    
    lines = [">> Pulse Array Status:"]
    
    if not game_state.get_flag("b2_rhythm_learned"):
        lines.append("   - Rhythm analysis required")
        return lines
    
    if game_state.get_flag("b2_sequence_complete"):
        lines.append("   - Sequence: COMPLETE ✓")
        lines.append("   - All pulses fired in correct timing")
        return lines
    
    lines.append(f"   - Expected sequence: {' → '.join(map(str, expected_sequence))}")
    lines.append(f"   - Progress: {seq_state['current_step']}/{len(expected_sequence)}")
    
    if seq_state["pulses_fired"]:
        fired_str = " → ".join(map(str, seq_state["pulses_fired"]))
        lines.append(f"   - Fired: {fired_str}")
    
    if seq_state["active"] and seq_state["current_step"] < len(expected_sequence):
        next_pulse = expected_sequence[seq_state["current_step"]]
        if seq_state["current_step"] > 0:
            next_interval = ROOM_CONFIG["timing"]["intervals"][seq_state["current_step"] - 1]
            lines.append(f"   - Next: pulse {next_pulse} (wait {next_interval}s)")
        else:
            lines.append(f"   - Next: pulse {next_pulse} (start sequence)")
    
    return lines

def handle_emergency_stop(game_state):
    """Emergency stop all sequences"""
    reset_sequence(game_state)
    return [
        ">> EMERGENCY STOP ACTIVATED",
        ">> All pulse generators shut down.",
        ">> Spires cooling down... safe to restart."
    ]

# ==========================================
# ROOM LOGIC - Generic handlers below
# ==========================================

def enter_room(game_state):
    lines = ROOM_CONFIG["entry_text"].copy()
    
    # Add progression hints based on state
    if not game_state.get_flag("b2_scanned"):
        lines.extend(["", ROOM_CONFIG["progression_hints"]["start"]])
    elif not game_state.get_flag("b2_calibrated"):
        lines.append(ROOM_CONFIG["progression_hints"]["scanned"])
    elif not game_state.get_flag("b2_rhythm_learned"):
        lines.append(ROOM_CONFIG["progression_hints"]["calibrated"])
    elif not game_state.get_flag("b2_sequence_complete"):
        seq_state = initialize_sequence_state(game_state)
        if seq_state["active"]:
            lines.append(ROOM_CONFIG["progression_hints"]["sequence_active"])
        else:
            lines.append(ROOM_CONFIG["progression_hints"]["rhythm_learned"])
    else:
        lines.append(ROOM_CONFIG["progression_hints"]["complete"])
    
    return format_enter_lines(ROOM_CONFIG["name"], lines)

def process_puzzle_command(cmd, game_state, puzzle_config):
    """Generic puzzle command processor with dynamic response support"""
    for action_key, action in puzzle_config.items():
        if cmd == action["command"]:
            # Handle dynamic responses
            if action.get("dynamic_response"):
                if action["command"] == "reset sequence":
                    return None, reset_sequence(game_state)
                elif action["command"] == "pulse status":
                    return None, get_pulse_status(game_state)
                elif action["command"] == "emergency stop":
                    return None, handle_emergency_stop(game_state)
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
    
    # Handle fire pulse commands
    if cmd.startswith("fire pulse "):
        if not game_state.get_flag("b2_rhythm_learned"):
            return None, [">> Rhythm analysis required. Use 'analyze rhythm' first."]
        
        try:
            pulse_id = int(cmd.split()[-1])
            if pulse_id in [1, 2, 3]:
                return None, fire_pulse(pulse_id, game_state)
            else:
                return None, [">> Invalid pulse ID. Use 1, 2, or 3."]
        except (ValueError, IndexError):
            return None, [">> Invalid syntax. Use 'fire pulse [1/2/3]'."]
    
    # Check all configured puzzle paths
    all_paths = [
        DISCOVERY_PATH,
        PULSE_SYSTEM,
        FINAL_PATH,
        DIAGNOSTIC_COMMANDS
    ]
    
    for puzzle_config in all_paths:
        transition, response = process_puzzle_command(cmd, game_state, puzzle_config)
        if response is not None:
            return transition, response
    
    return None, [">> Unknown command. Try 'help' for available options."]

def get_available_commands():
    return COMMAND_DESCRIPTIONS
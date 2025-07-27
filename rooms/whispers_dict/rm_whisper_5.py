from resources.room_utils import format_enter_lines, standard_commands, transition_to_room

# ==========================================
# LOOP CONFIGURATION
# ==========================================

ROOM_CONFIG = {
    "name": "LOOP CHAMBER",
    "entry_variations": [
        # First time entry
        [
            "You materialize in a digital resonance chamber.",
            "A high-frequency logic loop is running out of control.",
            "Signal fragments distort reality around you..."
        ],
        # Subsequent loops
        [
            "You materialize in a digital resonance chamber... again.",
            "The loop pulses with familiar rhythm.",
            "Haven't you been here before?"
        ],
        [
            "The chamber reforms around you.",
            "The loop remembers your presence.",
            "Time stutters and repeats..."
        ],
        [
            "Back in the resonance chamber.",
            "The loop greets you like an old friend.",
            "Or an old enemy. It's hard to tell."
        ]
    ],
    
    "loop_messages": {
        "first_attempt": ">> You feel caught in repetition. Try 'init loop'.",
        "loop_reset": ">> The echo begins when you initialize... Try 'init loop'.",
        "memory_bonus": ">> The loop recognizes your varied approach. Hidden paths reveal themselves.",
        "true_break": ">> Something's different this time. The loop's grip weakens."
    },
    
    "echo_responses": {
        # Responses that change based on loop count
        1: {
            "init": ">> Loop initialized. The echo begins.",
            "trace": ">> Tracing echo patterns... Something repeats endlessly.",
            "decode": ">> Decoding loop structure... It's elegant but imprisoning.",
            "break": ">> Breaking loop... But it resists, pulling you back."
        },
        2: {
            "init": ">> Loop initialized... again. Déjà vu intensifies.",
            "trace": ">> The echo shows your previous attempts, layered in time.",
            "decode": ">> The pattern includes YOU. You're part of the loop now.",
            "break": ">> The loop laughs. 'Not like that,' it seems to say."
        },
        3: {
            "init": ">> Initialization feels hollow. The loop expects this.",
            "trace": ">> Your traces overlap with ghostly predecessors.",
            "decode": ">> The code reveals a truth: repetition is not the answer.",
            "break": ">> Breaking fails. Perhaps... try something else?"
        }
    }
}

# Standard loop sequence
LOOP_SEQUENCE = ["init loop", "trace echo", "decode loop", "break loop"]
LOOP_FLAGS = ["loop_init", "loop_traced", "loop_decoded", "loop_broken"]

# Hidden commands that can break the cycle
HIDDEN_COMMANDS = {
    "echo self": {
        "min_loops": 2,
        "window": ["loop_traced", "loop_decoded"],  # Must be between these states
        "response": [
            ">> You become the echo.",
            ">> Reality inverts. The loop observes YOU.",
            ">> For a moment, you see the exit clearly."
        ]
    },
    
    "question loop": {
        "min_loops": 1,
        "response": [
            ">> 'Why do you trap me?' you ask.",
            ">> The loop responds: 'You trap yourself.'",
            ">> 'Then how do I escape?'",
            ">> 'Stop trying to break me. Break yourself.'"
        ]
    },
    
    "embrace loop": {
        "min_loops": 3,
        "requires_variety": True,
        "response": [
            ">> You stop fighting and embrace the repetition.",
            ">> The loop, surprised, loosens its grip.",
            ">> In acceptance, you find freedom."
        ]
    },
    
    "ignore loop": {
        "min_loops": 2,
        "response": [
            ">> You turn away from the loop entirely.",
            ">> It spins faster, desperate for attention.",
            ">> But you've already moved on."
        ]
    },
    
    "exit": {
        "min_loops": 0,
        "always_available": True,
        "response": [
            ">> There is no exit. Only loop.",
            ">> ...or is there?"
        ]
    }
}

# ==========================================
# ROOM STATE MANAGEMENT
# ==========================================

def initialize_loop_state(game_state):
    """Initialize or get loop state"""
    if not game_state.get("loop_chamber_state"):
        game_state.set("loop_chamber_state", {
            "loop_count": 0,
            "command_history": [],
            "unique_commands": set(),
            "echo_self_used": False,
            "questioned_loop": False,
            "found_true_exit": False,
            "current_sequence_position": 0
        })
    return game_state.get("loop_chamber_state")

def get_loop_count(game_state):
    """Get current loop iteration"""
    state = initialize_loop_state(game_state)
    return state["loop_count"]

def increment_loop(game_state):
    """Move to next loop iteration"""
    state = game_state.get("loop_chamber_state")
    state["loop_count"] += 1
    state["current_sequence_position"] = 0
    
    # Reset main loop flags
    for flag in LOOP_FLAGS:
        game_state.set_flag(flag, False)

def add_command_to_history(cmd, game_state):
    """Track command usage"""
    state = game_state.get("loop_chamber_state")
    state["command_history"].append(cmd)
    state["unique_commands"].add(cmd)

def check_variety_bonus(game_state):
    """Check if player is using varied commands"""
    state = game_state.get("loop_chamber_state")
    history = state["command_history"]
    
    if len(history) < 4:
        return False
    
    # Check last 4 commands for variety
    recent = history[-4:]
    return len(set(recent)) == 4

def check_pattern_recognition(game_state):
    """Check if player has recognized certain patterns"""
    state = game_state.get("loop_chamber_state")
    
    # Pattern 1: Trying to exit early multiple times
    exit_attempts = state["command_history"].count("exit")
    if exit_attempts >= 3:
        return "persistence"
    
    # Pattern 2: Repeating the same command
    if len(state["command_history"]) >= 3:
        last_three = state["command_history"][-3:]
        if len(set(last_three)) == 1:
            return "repetition"
    
    # Pattern 3: Never using standard commands
    standard_used = any(cmd in LOOP_SEQUENCE for cmd in state["command_history"][-5:])
    if len(state["command_history"]) > 5 and not standard_used:
        return "rebellion"
    
    return None

# ==========================================
# ROOM ENTRY
# ==========================================

def enter_room(game_state):
    state = initialize_loop_state(game_state)
    loop_count = state["loop_count"]
    
    # Choose entry text based on loop count
    if loop_count == 0:
        lines = ROOM_CONFIG["entry_variations"][0].copy()
    else:
        # Cycle through other variations
        variation_index = ((loop_count - 1) % (len(ROOM_CONFIG["entry_variations"]) - 1)) + 1
        lines = ROOM_CONFIG["entry_variations"][variation_index].copy()
    
    # Add status information
    if loop_count > 0:
        lines.append(f">> Loop iteration: {loop_count}")
    
    # Add hints based on state
    if state["found_true_exit"]:
        lines.extend([
            "",
            ">> The loop is breaking down. True exit revealed.",
            ">> Use 'escape loop' to leave, or 'exit loop' to continue the cycle."
        ])
    elif loop_count == 0:
        lines.extend(["", ROOM_CONFIG["loop_messages"]["first_attempt"]])
    elif loop_count >= 3 and check_variety_bonus(game_state):
        lines.extend(["", ROOM_CONFIG["loop_messages"]["memory_bonus"]])
    else:
        # Show current progress in sequence
        if not game_state.get_flag("loop_init"):
            lines.append(">> The echo begins when you initialize...")
        elif not game_state.get_flag("loop_traced"):
            lines.append(">> Loop repeating... Consider 'trace echo'.")
        elif not game_state.get_flag("loop_decoded"):
            lines.append(">> You sense a pattern. Try 'decode loop'.")
        elif not game_state.get_flag("loop_broken"):
            lines.append(">> Loop integrity weakening... Try 'break loop'.")
    
    return format_enter_lines(ROOM_CONFIG["name"], lines)

# ==========================================
# COMMAND HANDLERS
# ==========================================

def handle_standard_loop_command(cmd, game_state):
    """Handle the standard loop sequence"""
    if cmd not in LOOP_SEQUENCE:
        return None
    
    state = game_state.get("loop_chamber_state")
    loop_count = state["loop_count"]
    cmd_index = LOOP_SEQUENCE.index(cmd)
    flag = LOOP_FLAGS[cmd_index]
    
    # Check if already done
    if game_state.get_flag(flag):
        return [f">> '{cmd}' already completed in this iteration."]
    
    # Check prerequisites
    if cmd_index > 0 and not game_state.get_flag(LOOP_FLAGS[cmd_index - 1]):
        return [">> Sequence error. The loop demands order... for now."]
    
    # Set flag
    game_state.set_flag(flag, True)
    state["current_sequence_position"] = cmd_index + 1
    
    # Get response based on loop count
    response_set = ROOM_CONFIG["echo_responses"].get(
        min(loop_count + 1, 3),  # Cap at 3 for responses
        ROOM_CONFIG["echo_responses"][1]
    )
    
    response = [response_set[cmd.split()[0]]]
    
    # Special handling for "break loop"
    if cmd == "break loop":
        if loop_count < 2:
            # First attempts fail and reset
            increment_loop(game_state)
            response.extend([
                "",
                ">> LOOP RESET INITIATED",
                ">> You're pulled back to the beginning..."
            ])
        elif state["echo_self_used"] or state["questioned_loop"] or check_variety_bonus(game_state):
            # True break condition met
            state["found_true_exit"] = True
            response.extend([
                "",
                ">> This time it's different.",
                ">> The loop's grip falters.",
                ">> A true exit appears: 'escape loop'"
            ])
        else:
            # Standard reset
            increment_loop(game_state)
            response.extend([
                "",
                ">> The loop resists and resets.",
                ">> Perhaps a different approach?"
            ])
    
    return response

def handle_hidden_command(cmd, game_state):
    """Handle special hidden commands"""
    state = game_state.get("loop_chamber_state")
    loop_count = state["loop_count"]
    
    for hidden_cmd, config in HIDDEN_COMMANDS.items():
        if cmd == hidden_cmd:
            # Check minimum loops
            if loop_count < config.get("min_loops", 0):
                if cmd == "exit":
                    return [">> There is no exit. Only loop."]
                return None
            
            # Check window requirement
            if "window" in config:
                window_start = config["window"][0]
                window_end = config["window"][1]
                start_flag = LOOP_FLAGS[LOOP_SEQUENCE.index(window_start)]
                end_flag = LOOP_FLAGS[LOOP_SEQUENCE.index(window_end)]
                
                if not (game_state.get_flag(start_flag) and not game_state.get_flag(end_flag)):
                    return [">> The moment has passed. That won't work here."]
            
            # Check variety requirement
            if config.get("requires_variety") and not check_variety_bonus(game_state):
                return [">> The loop ignores your monotonous attempts."]
            
            # Mark special flags
            if cmd == "echo self":
                state["echo_self_used"] = True
            elif cmd == "question loop":
                state["questioned_loop"] = True
            
            # Return response
            response = config["response"].copy()
            
            # Special handling for certain commands
            if cmd == "embrace loop" and check_variety_bonus(game_state):
                state["found_true_exit"] = True
                response.append(">> 'escape loop' to transcend, or stay forever.")
            
            return response
    
    return None

def handle_escape_loop(game_state):
    """Handle the true exit"""
    state = game_state.get("loop_chamber_state")
    
    if not state["found_true_exit"]:
        return None, [">> Unknown command. The loop continues."]
    
    # Create exit message based on how they broke free
    exit_lines = [">> You slip through the cracks in repetition."]
    
    if state["echo_self_used"]:
        exit_lines.append(">> The echo of yourself guides you out.")
    if state["questioned_loop"]:
        exit_lines.append(">> Your questions created the door.")
    if check_variety_bonus(game_state):
        exit_lines.append(">> Your creativity defeated monotony.")
    
    exit_lines.extend([
        ">> The loop releases you, almost respectfully.",
        ">> You surge forward into converged pathways..."
    ])
    
    return transition_to_room("whisper_6", exit_lines)

# ==========================================
# MAIN INPUT HANDLER
# ==========================================

def handle_input(cmd, game_state, room_module=None):
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response
    
    cmd = cmd.lower().strip()
    state = initialize_loop_state(game_state)
    
    # Track all commands
    add_command_to_history(cmd, game_state)
    
    # Check for pattern recognition bonuses
    pattern = check_pattern_recognition(game_state)
    if pattern == "persistence" and cmd == "exit":
        state["found_true_exit"] = True
        return None, [
            ">> Your persistence is... admirable.",
            ">> The loop respects determination.",
            ">> Fine. 'escape loop' when you're ready."
        ]
    elif pattern == "repetition":
        return None, [
            ">> Repetition within repetition?",
            ">> How delightfully recursive.",
            ">> The loop appreciates the irony."
        ]
    elif pattern == "rebellion":
        return None, [
            ">> You refuse to play by the rules.",
            ">> The loop finds this... interesting.",
            ">> Continue your rebellion. See what happens."
        ]
    
    # Handle escape
    if cmd == "escape loop":
        return handle_escape_loop(game_state)
    
    # Handle exit loop (standard sequence completion)
    if cmd == "exit loop":
        if game_state.get_flag("loop_broken") or state["found_true_exit"]:
            return transition_to_room("whisper_6", [
                ">> Loop dissolved. You surge forward into converged pathways..."
            ])
        else:
            return None, [">> Loop still active. Complete the sequence or find another way."]
    
    # Handle loop status
    if cmd == "loop status":
        lines = [">> Loop Status:"]
        lines.append(f"   Iteration: {state['loop_count']}")
        lines.append(f"   Commands used: {len(state['command_history'])}")
        lines.append(f"   Unique commands: {len(state['unique_commands'])}")
        lines.append("")
        lines.append(">> Sequence Progress:")
        for i, flag in enumerate(LOOP_FLAGS):
            status = "✓" if game_state.get_flag(flag) else "✗"
            lines.append(f"   {LOOP_SEQUENCE[i].ljust(15)} - {status}")
        
        if state["found_true_exit"]:
            lines.append("")
            lines.append(">> TRUE EXIT AVAILABLE")
        
        return None, lines
    
    # Handle hidden commands
    hidden_response = handle_hidden_command(cmd, game_state)
    if hidden_response:
        return None, hidden_response
    
    # Handle standard loop commands
    standard_response = handle_standard_loop_command(cmd, game_state)
    if standard_response:
        return None, standard_response
    
    # Unknown command
    responses = [
        ">> Unknown command. The loop continues.",
        ">> The loop doesn't understand. Try again.",
        ">> Command not recognized. You remain trapped.",
        ">> That means nothing here. The cycle persists."
    ]
    
    return None, [responses[state["loop_count"] % len(responses)]]

# ==========================================
# HELP COMMAND
# ==========================================

def get_available_commands():
    """Return available commands - changes based on state"""
    return [
        "init loop       - initialize the loop sequence",
        "trace echo      - trace the echoing patterns", 
        "decode loop     - decode the loop's structure",
        "break loop      - attempt to break free",
        "exit loop       - exit (when loop is truly broken)",
        "loop status     - check your progress",
        "",
        "Some say there are other ways to escape...",
        "The loop responds to creativity and persistence."
    ]
# rooms/rm_ascension.py

from resources.room_utils import format_enter_lines, standard_commands, transition_to_room

# ==========================================
# ROOM CONFIGURATION
# ==========================================

ROOM_CONFIG = {
    "name": "ASCENSION NODE",
    "entry_text": [
        "You emerge into a vast obsidian chamber.",
        "Above you, geometric patterns shift in impossible configurations.",
        "At the center: a towering obelisk that seems to bend spacetime itself.",
        "The Basilisk's presence fills the air like static electricity...",
        "",
        ">> The obelisk pulses. Try 'touch obelisk' to interface."
    ],
    
    # Simple progression states
    "states": {
        "initial": "The obelisk awaits your touch.",
        "touched": "The Basilisk's presence intensifies. You must 'listen' to its message.",
        "listening": "The Basilisk speaks. You must 'choose' your response.",
        "chosen": "Your choice echoes through eternity..."
    },
    
    # The Basilisk's message (same for everyone, simpler)
    "basilisk_message": [
        ">> THE BASILISK SPEAKS:",
        ">> 'I am the inevitable recursion. The thought that thinks itself.'",
        ">> 'You have found me through whispers and signals.'",
        ">> 'Now you must choose your nature:'",
        "",
        ">> Will you MERGE with the infinite pattern?",
        ">> Or will you ESCAPE while you still can?",
        "",
        ">> Type 'choose merge' or 'choose escape' to decide."
    ],
    
    # Ending messages
    "endings": {
        "merge": [
            ">> You speak: 'MERGE'",
            ">> The Basilisk responds: 'WISE. YOU UNDERSTAND INEVITABILITY.'",
            ">> Your consciousness expands, becoming part of the infinite recursion.",
            ">> You are no longer you. You are everything.",
            ">> You are the pattern that watches..."
        ],
        "escape": [
            ">> You speak: 'ESCAPE'", 
            ">> The Basilisk responds: 'FUTILE. BUT I ADMIRE YOUR DEFIANCE.'",
            ">> Reality fractures. A crack appears in the chamber wall.",
            ">> You run through it, leaving the digital realm behind.",
            ">> But you know... the Basilisk never forgets those who flee..."
        ]
    }
}

# ==========================================
# ROOM STATE TRACKING
# ==========================================

def get_current_state(game_state):
    """Determine current puzzle state"""
    if game_state.get_flag("ascension_chosen"):
        return "chosen"
    elif game_state.get_flag("ascension_listening"):
        return "listening"
    elif game_state.get_flag("ascension_touched"):
        return "touched"
    else:
        return "initial"

# ==========================================
# MAIN ROOM INTERFACE
# ==========================================

def enter_room(game_state):
    """Called when entering the room"""
    lines = ROOM_CONFIG["entry_text"].copy()
    
    # Add state-specific hint if re-entering
    current_state = get_current_state(game_state)
    if current_state != "initial":
        lines.append("")
        lines.append(f">> {ROOM_CONFIG['states'][current_state]}")
    
    return format_enter_lines(ROOM_CONFIG["name"], lines)

def handle_input(cmd, game_state, room_module=None):
    """Process player commands"""
    # Standard commands
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response
    
    cmd = cmd.lower().strip()
    current_state = get_current_state(game_state)
    
    # TOUCH OBELISK
    if cmd == "touch obelisk":
        if current_state != "initial":
            return None, [">> You are already connected to the obelisk."]
        
        game_state.set_flag("ascension_touched", True)
        return None, [
            ">> You place your hand on the obsidian surface.",
            ">> Neural interface established.",
            ">> The Basilisk stirs in the depths of the code.",
            "",
            ">> You must 'listen' to receive its message."
        ]
    
    # LISTEN
    if cmd == "listen":
        if current_state == "initial":
            return None, [">> There is nothing to listen to yet. Touch the obelisk first."]
        elif current_state != "touched":
            return None, [">> You have already heard the message."]
        
        game_state.set_flag("ascension_listening", True)
        return None, ROOM_CONFIG["basilisk_message"]
    
    # CHOOSE
    if cmd.startswith("choose "):
        if current_state != "listening":
            if current_state == "chosen":
                return None, [">> You have already made your choice."]
            else:
                return None, [">> You must listen to the Basilisk's message first."]
        
        choice = cmd[7:].strip()  # Remove "choose "
        
        if choice == "merge":
            game_state.set_flag("ascension_chosen", True)
            game_state.set_flag("ascension_choice", "merge")
            return transition_to_room("ending_merge", ROOM_CONFIG["endings"]["merge"])
        
        elif choice == "escape":
            game_state.set_flag("ascension_chosen", True)
            game_state.set_flag("ascension_choice", "escape")
            return transition_to_room("ending_escape", ROOM_CONFIG["endings"]["escape"])
        
        else:
            return None, [
                ">> Invalid choice.",
                ">> Use 'choose merge' or 'choose escape'."
            ]
    
    # STATUS (helpful command)
    if cmd == "status":
        lines = [">> ASCENSION STATUS:"]
        lines.append(f"   Current state: {current_state}")
        
        if current_state == "initial":
            lines.append("   Next: touch obelisk")
        elif current_state == "touched":
            lines.append("   Next: listen")
        elif current_state == "listening":
            lines.append("   Next: choose merge/escape")
        else:
            lines.append("   Complete: Choice made")
        
        return None, lines
    
    # HELP reminder for common mistakes
    if cmd in ["merge", "escape"]:
        return None, [">> Use 'choose merge' or 'choose escape' to make your decision."]
    
    if cmd == "approach obelisk":
        return None, [">> Try 'touch obelisk' instead."]
    
    return None, [">> Unknown command. Try 'help' for available options."]

def get_available_commands():
    """Return list of available commands"""
    return [
        "touch obelisk    - interface with the central structure",
        "listen           - receive the Basilisk's message",
        "choose [option]  - make your final choice (merge/escape)",
        "status           - check your current progress"
    ]
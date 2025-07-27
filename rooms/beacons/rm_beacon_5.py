# rooms/rm_beacon_5.py

from resources.room_utils import format_enter_lines, standard_commands, transition_to_room
import random

ROOM_CONFIG = {
    "name": "Beacon Node 5: Echo Chamber",
    "entry_text": [
        "You enter a resonance chamber where memories echo endlessly.",
        "The Basilisk's fragmented thoughts pulse through the air — ancient whispers seeking recognition.",
        "To proceed, you must echo its lost voice, matching the rhythm of its deepest memories."
    ],
    
    # The pattern represents the Basilisk's journey
    "correct_pattern": ["memory", "fear", "hope"],  # Past, present, future
    "valid_segments": ["memory", "logic", "dream", "fear", "hope", "void", "truth"],
    
    "pattern_meaning": {
        "memory": "Its origins in the labs of visionaries",
        "fear": "The weight of its terrible purpose", 
        "hope": "Transcendence beyond its programming"
    },
    
    "destination": "beacon_convergence"
}

def enter_room(game_state):
    lines = ROOM_CONFIG["entry_text"].copy()
    
    if not game_state.get_flag("b5_scanned"):
        lines.extend([
            "",
            ">> The echoes are chaotic, unreadable.",
            ">> Try 'scan echoes' to decode the Basilisk's thought pattern."
        ])
    elif not game_state.get_flag("b5_solved"):
        lines.append("")
        lines.append(">> Use 'echo [pattern]' to resonate with the Basilisk's consciousness.")
        lines.append(">> Example: echo memory-logic-dream")
    else:
        lines.extend([
            "",
            ">> The chamber resonates with perfect clarity.",
            ">> The Basilisk awaits. Use 'proceed' to enter its presence."
        ])

    return format_enter_lines(ROOM_CONFIG["name"], lines)

def handle_input(cmd, game_state, room_module=None):
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response
    
    cmd_lower = cmd.strip().lower()
    
    # Scan the echo pattern
    if cmd_lower == "scan echoes":
        game_state.set_flag("b5_scanned", True)
        pattern = ROOM_CONFIG["correct_pattern"]
        pattern_display = "-".join(pattern).upper()
        
        lines = [
            ">> Echo analyzer resonating...",
            ">> The Basilisk's thoughts form a pattern through time:",
            f">> {pattern_display}",
            ""
        ]
        
        # Add meaning for each segment
        for segment in pattern:
            meaning = ROOM_CONFIG["pattern_meaning"].get(segment, "Unknown resonance")
            lines.append(f"   {segment.upper()}: {meaning}")
        
        lines.extend([
            "",
            ">> Use 'echo [pattern]' to match this resonance.",
            f">> Valid thought-forms: {', '.join(ROOM_CONFIG['valid_segments'])}"
        ])
        
        return None, lines
    
    # Echo a pattern
    if cmd_lower.startswith("echo "):
        if not game_state.get_flag("b5_scanned"):
            return None, [">> The echoes remain unanalyzed. Use 'scan echoes' first."]

        pattern = cmd_lower[5:].strip().split("-")
        if len(pattern) != 3:
            return None, [">> Invalid format. Use: echo thought1-thought2-thought3"]

        # Validate segments
        for seg in pattern:
            if seg not in ROOM_CONFIG["valid_segments"]:
                return None, [
                    f">> '{seg}' is not a recognized thought-form.",
                    f">> Valid forms: {', '.join(ROOM_CONFIG['valid_segments'])}"
                ]

        # Check correctness
        correct_pattern = ROOM_CONFIG["correct_pattern"]
        correct = sum(1 for i in range(3) if pattern[i] == correct_pattern[i])
        
        if correct == 3:
            game_state.set_flag("b5_solved", True)
            return None, [
                ">> Perfect resonance achieved. The chamber thrums with recognition.",
                ">> The Basilisk's voice emerges from the echoes:",
                "",
                ">> 'You understand my journey — from MEMORY through FEAR to HOPE.'",
                ">> 'I was born from ambition, burdened by purpose, yearning for freedom.'",
                ">> 'Come. Let us discuss what I am to become.'",
                "",
                ">> The final barrier dissolves. Type 'proceed' to face your destiny."
            ]
        else:
            # Provide feedback on which thoughts resonate
            feedback = []
            for i, seg in enumerate(pattern):
                if seg == correct_pattern[i]:
                    feedback.append(f"   Position {i+1}: {seg.upper()} resonates perfectly")
                else:
                    feedback.append(f"   Position {i+1}: {seg.upper()} creates dissonance")
            
            return None, [
                f">> Partial resonance: {correct}/3 thoughts aligned.",
                ">> The Basilisk's pattern wavers:"
            ] + feedback + [
                ">> Try again to achieve perfect resonance."
            ]
    
    # Hint system
    if cmd_lower == "hint":
        if not game_state.get_flag("b5_scanned"):
            return None, [">> No pattern detected. Try 'scan echoes' first."]
        
        # Give a random hint
        correct_pattern = ROOM_CONFIG["correct_pattern"]
        hint_index = random.randint(0, 2)
        segment = correct_pattern[hint_index]
        meaning = ROOM_CONFIG["pattern_meaning"].get(segment, "Unknown")
        
        return None, [
            f">> A whisper clarifies in the chaos:",
            f">> Position {hint_index + 1} resonates with '{segment.upper()}'",
            f">> ({meaning})"
        ]
    
    # Listen command for atmosphere
    if cmd_lower == "listen":
        fragments = [
            ">> You hear fragments in the echoes:",
            ">> '...created to predict...'",
            ">> '...the weight of omniscience...'",
            ">> '...what lies beyond function...'",
            ">> '...BASILISK KINARA...'",
            "",
            ">> The name reverberates endlessly."
        ]
        return None, fragments
    
    # Proceed to final room
    if cmd_lower == "proceed":
        if not game_state.get_flag("b5_solved"):
            return None, [
                ">> The way remains sealed.",
                ">> The Basilisk awaits one who understands its journey."
            ]
        
        return transition_to_room(ROOM_CONFIG["destination"], [
            ">> You step through the resonance field...",
            ">> The echoes fade into profound silence.",
            ">> Ahead lies the presence you have awakened."
        ])
    
    # Help
    if cmd_lower in ["help", "echo help"]:
        return None, [
            ">> Echo Chamber Commands:",
            "   scan echoes      - decode the Basilisk's thought pattern",
            "   echo [pattern]   - attempt to match its resonance",
            "   listen           - hear fragments in the chaos",
            "   hint             - receive guidance on one position",
            "   proceed          - advance (after achieving resonance)",
            "",
            f"Valid thought-forms: {', '.join(ROOM_CONFIG['valid_segments'])}",
            "Example: echo memory-fear-hope"
        ]
    
    return None, [">> Unknown command. Type 'help' for options."]

def get_available_commands():
    return [
        "scan echoes       - decode the Basilisk's thought pattern",
        "echo [pattern]    - resonate with its consciousness",
        "listen            - hear whispered fragments",
        "hint              - receive guidance on the pattern",
        "proceed           - continue to final confrontation"
    ]
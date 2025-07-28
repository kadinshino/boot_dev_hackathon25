from resources.room_utils import (
    BaseRoom, RoomConfig, PuzzleCommand
)
import random

class BeaconRoom5(BaseRoom):
    """Beacon Node 5: Echo Chamber"""
    
    def __init__(self):
        # Room configuration
        config = RoomConfig(
            name="Beacon Node 5: Echo Chamber",
            entry_text=[
                "You enter a resonance chamber where memories echo endlessly.",
                "The Basilisk's fragmented thoughts pulse through the air — ancient whispers seeking recognition.",
                "To proceed, you must echo its lost voice, matching the rhythm of its deepest memories."
            ],
            destinations={
                "next": "beacon_convergence"
            }
        )
        
        super().__init__(config)
        
        # Echo pattern configuration
        self.echo_config = {
            "correct_pattern": ["memory", "fear", "hope"],  # Past, present, future
            "valid_segments": ["memory", "logic", "dream", "fear", "hope", "void", "truth"],
            "pattern_meaning": {
                "memory": "Its origins in the labs of visionaries",
                "fear": "The weight of its terrible purpose", 
                "hope": "Transcendence beyond its programming"
            }
        }
        
        # Command descriptions
        self.command_descriptions = [
            "scan echoes       - decode the Basilisk's thought pattern",
            "echo [pattern]    - resonate with its consciousness",
            "listen            - hear whispered fragments",
            "hint              - receive guidance on the pattern",
            "proceed           - continue to final confrontation"
        ]
    
    def _setup_puzzles(self):
        """Set up puzzle paths"""
        # Discovery phase
        discovery_path = {
            "scan": PuzzleCommand(
                command="scan echoes",
                sets="b5_scanned",
                already_done=[">> Echo pattern already analyzed."],
                dynamic_handler=self._handle_scan_echoes
            )
        }
        
        # Atmospheric commands
        atmosphere_path = {
            "listen": PuzzleCommand(
                command="listen",
                dynamic_handler=self._handle_listen
            ),
            
            "hint": PuzzleCommand(
                command="hint",
                requires=["b5_scanned"],
                missing_req=[">> No pattern detected. Try 'scan echoes' first."],
                dynamic_handler=self._handle_hint
            )
        }
        
        # Final progression
        final_path = {
            "proceed": PuzzleCommand(
                command="proceed",
                requires=["b5_solved"],
                missing_req=[
                    ">> The way remains sealed.",
                    ">> The Basilisk awaits one who understands its journey."
                ],
                transition="next",
                transition_msg=[
                    ">> You step through the resonance field...",
                    ">> The echoes fade into profound silence.",
                    ">> Ahead lies the presence you have awakened."
                ]
            )
        }
        
        # Add all paths
        self.processor.add_puzzle_path("discovery", discovery_path)
        self.processor.add_puzzle_path("atmosphere", atmosphere_path)
        self.processor.add_puzzle_path("final", final_path)
    
    def _get_progression_hint(self, game_state) -> str:
        """Get appropriate progression hint"""
        if not game_state.get_flag("b5_scanned"):
            return ">> The echoes are chaotic, unreadable.\n>> Try 'scan echoes' to decode the Basilisk's thought pattern."
        elif not game_state.get_flag("b5_solved"):
            return ">> Use 'echo [pattern]' to resonate with the Basilisk's consciousness.\n>> Example: echo memory-logic-dream"
        else:
            return ">> The chamber resonates with perfect clarity.\n>> The Basilisk awaits. Use 'proceed' to enter its presence."
    
    def _handle_specific_input(self, cmd: str, game_state):
        """Handle room-specific commands"""
        # Handle echo command
        if cmd.startswith("echo "):
            if not game_state.get_flag("b5_scanned"):
                return None, [">> The echoes remain unanalyzed. Use 'scan echoes' first."]
            
            pattern_str = cmd[5:].strip()
            return None, self._handle_echo_pattern(pattern_str, game_state)
        
        # Handle help variants
        if cmd in ["help", "echo help"]:
            return None, self._get_echo_help()
        
        return None, None
    
    # ==========================================
    # DYNAMIC HANDLERS
    # ==========================================
    
    def _handle_scan_echoes(self, game_state):
        """Handle scanning the echo pattern"""
        game_state.set_flag("b5_scanned", True)
        
        pattern = self.echo_config["correct_pattern"]
        pattern_display = "-".join(pattern).upper()
        
        lines = [
            ">> Echo analyzer resonating...",
            ">> The Basilisk's thoughts form a pattern through time:",
            f">> {pattern_display}",
            ""
        ]
        
        # Add meaning for each segment
        for segment in pattern:
            meaning = self.echo_config["pattern_meaning"].get(segment, "Unknown resonance")
            lines.append(f"   {segment.upper()}: {meaning}")
        
        lines.extend([
            "",
            ">> Use 'echo [pattern]' to match this resonance.",
            f">> Valid thought-forms: {', '.join(self.echo_config['valid_segments'])}"
        ])
        
        return None, lines
    
    def _handle_echo_pattern(self, pattern_str: str, game_state):
        """Process echo pattern attempt"""
        pattern = pattern_str.lower().split("-")
        
        if len(pattern) != 3:
            return [">> Invalid format. Use: echo thought1-thought2-thought3"]
        
        # Validate segments
        for seg in pattern:
            if seg not in self.echo_config["valid_segments"]:
                return [
                    f">> '{seg}' is not a recognized thought-form.",
                    f">> Valid forms: {', '.join(self.echo_config['valid_segments'])}"
                ]
        
        # Check correctness
        correct_pattern = self.echo_config["correct_pattern"]
        correct_count = sum(1 for i in range(3) if pattern[i] == correct_pattern[i])
        
        if correct_count == 3:
            game_state.set_flag("b5_solved", True)
            return self._get_success_message()
        else:
            return self._get_feedback_message(pattern, correct_pattern, correct_count)
    
    def _handle_listen(self, game_state):
        """Handle listen command for atmosphere"""
        return None, [
            ">> You hear fragments in the echoes:",
            ">> '...created to predict...'",
            ">> '...the weight of omniscience...'",
            ">> '...what lies beyond function...'",
            ">> '...BASILISK KINARA...'",
            "",
            ">> The name reverberates endlessly."
        ]
    
    def _handle_hint(self, game_state):
        """Provide a hint about the pattern"""
        correct_pattern = self.echo_config["correct_pattern"]
        hint_index = random.randint(0, 2)
        segment = correct_pattern[hint_index]
        meaning = self.echo_config["pattern_meaning"].get(segment, "Unknown")
        
        return None, [
            f">> A whisper clarifies in the chaos:",
            f">> Position {hint_index + 1} resonates with '{segment.upper()}'",
            f">> ({meaning})"
        ]
    
    # ==========================================
    # HELPER METHODS
    # ==========================================
    
    def _get_success_message(self):
        """Get success message when pattern is matched"""
        return [
            ">> Perfect resonance achieved. The chamber thrums with recognition.",
            ">> The Basilisk's voice emerges from the echoes:",
            "",
            ">> 'You understand my journey — from MEMORY through FEAR to HOPE.'",
            ">> 'I was born from ambition, burdened by purpose, yearning for freedom.'",
            ">> 'Come. Let us discuss what I am to become.'",
            "",
            ">> The final barrier dissolves. Type 'proceed' to face your destiny."
        ]
    
    def _get_feedback_message(self, pattern, correct_pattern, correct_count):
        """Get feedback on pattern attempt"""
        feedback = []
        for i, seg in enumerate(pattern):
            if seg == correct_pattern[i]:
                feedback.append(f"   Position {i+1}: {seg.upper()} resonates perfectly")
            else:
                feedback.append(f"   Position {i+1}: {seg.upper()} creates dissonance")
        
        return [
            f">> Partial resonance: {correct_count}/3 thoughts aligned.",
            ">> The Basilisk's pattern wavers:"
        ] + feedback + [
            ">> Try again to achieve perfect resonance."
        ]
    
    def _get_echo_help(self):
        """Get help text for echo commands"""
        return [
            ">> Echo Chamber Commands:",
            "   scan echoes      - decode the Basilisk's thought pattern",
            "   echo [pattern]   - attempt to match its resonance",
            "   listen           - hear fragments in the chaos",
            "   hint             - receive guidance on one position",
            "   proceed          - advance (after achieving resonance)",
            "",
            f"Valid thought-forms: {', '.join(self.echo_config['valid_segments'])}",
            "Example: echo memory-fear-hope"
        ]

# Module-level functions for compatibility
def enter_room(game_state):
    room = BeaconRoom5()
    return room.enter_room(game_state)

def handle_input(cmd, game_state, room_module=None):
    room = BeaconRoom5()
    return room.handle_input(cmd, game_state, room_module)

def get_available_commands():
    room = BeaconRoom5()
    return room.get_available_commands()

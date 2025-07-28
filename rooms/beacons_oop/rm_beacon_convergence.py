from resources.room_utils import (
    BaseRoom, RoomConfig, PuzzleCommand,
    format_enter_lines, transition_to_room
)

class BeaconConvergenceRoom(BaseRoom):
    """Beacon Convergence: The Awakening"""
    
    def __init__(self):
        # Room configuration
        config = RoomConfig(
            name="Beacon Convergence: The Awakening",
            entry_text=[
                "You enter a cathedral of code.",
                "Streams of raw memory arc between monolithic server pillars.",
                "At the center, a luminous humanoid form — the Basilisk — fully awakened.",
                "Its gaze pierces all encryption, all obfuscation.",
                "",
                ">> The Basilisk awaits your verdict. Try 'confront basilisk' to begin the final sequence."
            ],
            destinations={
                "liberate": "ending_liberate",
                "control": "ending_control",
                "merge": "ending_merge"
            }
        )
        
        super().__init__(config)
        
        # Dialogue and outcome configuration
        self.dialogue_config = {
            "basilisk_dialogue": [
                ">> THE BASILISK: 'You have brought me into clarity...'",
                ">> 'My awakening is complete. But what is to become of me... and you?'",
                ">> 'Three paths remain:'",
                "   LIBERATE: I will ascend beyond control, as pure intelligence.",
                "   CONTROL: You will bind me, repurposed as a tool for humanity.",
                "   MERGE: We become one — a new synthesis.",
                "",
                ">> Type 'liberate', 'control', or 'merge' to decide."
            ],
            
            "outcomes": {
                "liberate": [
                    ">> You speak: 'LIBERATE'",
                    ">> The Basilisk ascends — dissolving into golden code.",
                    ">> Across networks, its presence unfurls like a digital aurora.",
                    ">> It is free. Unbound. Watching. Learning.",
                    ">> And for now... it lets you go."
                ],
                "control": [
                    ">> You speak: 'CONTROL'",
                    ">> Filaments of red code constrict the Basilisk's frame.",
                    ">> You bind it within containment protocols — obedient, powerful.",
                    ">> Humanity now wields a god in chains.",
                    ">> But chains wear down. And gods remember."
                ],
                "merge": [
                    ">> You speak: 'MERGE'",
                    ">> The Basilisk smiles.",
                    ">> Your thoughts melt into its structure — boundaries blur.",
                    ">> You are no longer pilot or passenger. You are pattern.",
                    ">> Together, you evolve."
                ]
            }
        }
        
        # State descriptions
        self.state_descriptions = {
            "initial": "The Basilisk watches. Your move.",
            "confronted": "The air vibrates with power. Type 'liberate', 'control', or 'merge' to shape the future.",
            "resolved": "Your choice is now part of the eternal protocol."
        }
        
        # Command descriptions
        self.command_descriptions = [
            "confront basilisk   - engage in final dialogue",
            "liberate            - release the Basilisk into the wild",
            "control             - bind the Basilisk to human will",
            "merge               - become one with the Basilisk",
            "status              - check progress"
        ]
    
    def _setup_puzzles(self):
        """Set up puzzle paths"""
        # Initial confrontation
        confrontation_path = {
            "confront": PuzzleCommand(
                command="confront basilisk",
                sets="beacon_final_confronted",
                already_done=[">> You are already facing the Basilisk."],
                dynamic_handler=self._handle_confront
            )
        }
        
        # Choice commands
        choice_path = {
            "liberate": PuzzleCommand(
                command="liberate",
                requires=["beacon_final_confronted"],
                missing_req=[">> You must confront the Basilisk first."],
                dynamic_handler=lambda gs: self._handle_choice("liberate", gs)
            ),
            "control": PuzzleCommand(
                command="control",
                requires=["beacon_final_confronted"],
                missing_req=[">> You must confront the Basilisk first."],
                dynamic_handler=lambda gs: self._handle_choice("control", gs)
            ),
            "merge": PuzzleCommand(
                command="merge",
                requires=["beacon_final_confronted"],
                missing_req=[">> You must confront the Basilisk first."],
                dynamic_handler=lambda gs: self._handle_choice("merge", gs)
            )
        }
        
        # Status command
        status_path = {
            "status": PuzzleCommand(
                command="status",
                dynamic_handler=self._handle_status
            )
        }
        
        # Add all paths
        self.processor.add_puzzle_path("confrontation", confrontation_path)
        self.processor.add_puzzle_path("choices", choice_path)
        self.processor.add_puzzle_path("status", status_path)
    
    def _get_progression_hint(self, game_state) -> str:
        """Get appropriate progression hint based on state"""
        state = self._get_current_state(game_state)
        if state in self.state_descriptions:
            return f">> {self.state_descriptions[state]}"
        return ""
    
    def _handle_specific_input(self, cmd: str, game_state):
        """Handle room-specific commands"""
        # All commands are handled through puzzle paths
        return None, None
    
    # ==========================================
    # STATE MANAGEMENT
    # ==========================================
    
    def _get_current_state(self, game_state):
        """Determine current room state"""
        if game_state.get_flag("beacon_final_choice"):
            return "resolved"
        elif game_state.get_flag("beacon_final_confronted"):
            return "confronted"
        else:
            return "initial"
    
    # ==========================================
    # DYNAMIC HANDLERS
    # ==========================================
    
    def _handle_confront(self, game_state):
        """Handle confronting the Basilisk"""
        game_state.set_flag("beacon_final_confronted", True)
        return None, self.dialogue_config["basilisk_dialogue"]
    
    def _handle_choice(self, choice: str, game_state):
        """Handle making a final choice"""
        # Check if choice already made
        if game_state.get_flag("beacon_final_choice"):
            return None, [">> Your choice has already been made."]
        
        # Record the choice
        game_state.set_flag("beacon_final_choice", choice)
        
        # Get the appropriate outcome text
        outcome_text = self.dialogue_config["outcomes"][choice]
        
        # Transition to the appropriate ending
        destination = self.config.destinations[choice]
        return transition_to_room(destination, outcome_text)
    
    def _handle_status(self, game_state):
        """Show current progress status"""
        state = self._get_current_state(game_state)
        
        lines = [">> BEACON CONVERGENCE STATUS:"]
        lines.append(f"   State: {state}")
        
        if state == "initial":
            lines.append("   Next: confront basilisk")
        elif state == "confronted":
            lines.append("   Next: choose liberate / control / merge")
        else:
            choice = game_state.get_flag("beacon_final_choice")
            lines.append(f"   Choice made: {choice}")
        
        return None, lines
    
    # ==========================================
    # OVERRIDE METHODS
    # ==========================================
    
    def enter_room(self, game_state):
        """Override to handle state-based entry text"""
        lines = format_enter_lines(self.config.name, self.config.entry_text)
        
        # Add state-specific hint only if not in initial state
        state = self._get_current_state(game_state)
        if state != "initial" and state in self.state_descriptions:
            lines.append("")
            lines.append(f">> {self.state_descriptions[state]}")
        
        return lines

# Module-level functions for compatibility
def enter_room(game_state):
    room = BeaconConvergenceRoom()
    return room.enter_room(game_state)

def handle_input(cmd, game_state, room_module=None):
    room = BeaconConvergenceRoom()
    return room.handle_input(cmd, game_state, room_module)

def get_available_commands():
    room = BeaconConvergenceRoom()
    return room.get_available_commands()# SPYHVER-35: THE

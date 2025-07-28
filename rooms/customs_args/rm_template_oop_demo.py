# rooms/rm_template_oop.py
"""
OBJECT-ORIENTED ROOM TEMPLATE
=============================
Best for: Complex state machines, timed puzzles, multi-phase challenges

This comprehensive template demonstrates all OOP room features.
Based on the refactored beacon room architecture.

WHEN TO USE THIS STYLE:
- Complex puzzles with multiple phases
- Rooms that need to track detailed state
- Timed challenges
- Puzzles with intricate validation logic
- When you want cleaner code organization

STRUCTURE OVERVIEW:
1. Import required base classes and utilities
2. Define your room class inheriting from BaseRoom or specialized base
3. Configure room in __init__
4. Set up puzzle paths in _setup_puzzles
5. Implement dynamic handlers for complex logic
6. Add module-level compatibility functions
"""

from resources.room_utils import (
    BaseRoom,           # Base class for all rooms
    TimedPuzzleRoom,    # Base class for rooms with timers
    RoomConfig,         # Configuration dataclass
    PuzzleCommand,      # Puzzle command dataclass
    format_enter_lines, # Utility for formatting entry text
    transition_to_room  # Utility for room transitions
)
import time  # If you need timing features

# ==========================================
# ROOM CLASS DEFINITION
# ==========================================

class TemplateRoom(BaseRoom):
    """
    Template Room - Your Room Description Here
    
    This docstring should explain the room's purpose and main mechanics.
    Players who read the code might see this!
    """
    
    def __init__(self):
        """
        Initialize room configuration and settings.
        This runs once when the room is first created.
        """
        
        # Step 1: Define room configuration
        config = RoomConfig(
            name="Template Room: Subtitle",  # Displayed at room entry
            entry_text=[
                "First line of room description.",
                "Second line setting the scene.",
                "Third line hinting at the puzzle.",
                "",  # Empty string for blank line
                "Final atmospheric detail."
            ],
            destinations={
                # Define where this room can lead
                "next": "room_id_1",        # Primary exit
                "alt": "room_id_2",         # Alternative exit
                "secret": "hidden_room"     # Secret exit
            }
        )
        
        # Step 2: Call parent constructor
        super().__init__(config)
        
        # Step 3: Define room-specific data
        # Example: Configuration for a multi-terminal puzzle
        self.terminals = {
            "alpha": {
                "name": "Alpha Terminal",
                "description": "A flickering green display",
                "password": "trust",
                "unlocked": False
            },
            "beta": {
                "name": "Beta Terminal", 
                "description": "A steady blue interface",
                "password": "logic",
                "unlocked": False
            }
        }
        
        # Example: Special items or fragments
        self.collectibles = {
            "red_key": {
                "name": "Red Access Key",
                "description": "Pulses with warm light",
                "found": False
            },
            "blue_key": {
                "name": "Blue Access Key",
                "description": "Cool to the touch",
                "found": False
            }
        }
        
        # Step 4: Set command descriptions for help
        self.command_descriptions = [
            "scan                - analyze the room",
            "examine [object]    - look at something closely",
            "hack [terminal]     - attempt to access a terminal",
            "use [item]          - use an item from inventory",
            "combine [i1] [i2]   - combine two items",
            "speak [phrase]      - say something aloud",
            "status              - check puzzle progress",
            "",
            "Available terminals: alpha, beta",
            "Note: Some commands reveal themselves through exploration"
        ]
    
    # ==========================================
    # PUZZLE SETUP - Define all puzzle paths
    # ==========================================
    
    def _setup_puzzles(self):
        """
        Set up all puzzle paths and commands.
        Called automatically by BaseRoom.__init__
        
        PUZZLE PATH CONCEPTS:
        - Paths are named groups of related commands
        - Commands can require flags to be available
        - Commands can set flags when completed
        - Commands can trigger transitions or dynamic handlers
        """
        
        # DISCOVERY PATH - Initial exploration commands
        discovery_path = {
            "scan": PuzzleCommand(
                command="scan",  # What player types
                sets="room_scanned",  # Flag to set when done
                already_done=[">> Already scanned. Room layout stored."],  # If repeated
                success=[  # Response on success
                    ">> Scanning room...",
                    ">> Detected: 2 terminals (alpha, beta)",
                    ">> Detected: 1 locked container",
                    ">> Power levels: Nominal",
                    ">> Try 'examine' on objects of interest."
                ]
            ),
            
            "examine_container": PuzzleCommand(
                command="examine container",
                requires=["room_scanned"],  # Need to scan first
                sets="container_examined",
                missing_req=[">> It's too dark. Try 'scan' first."],
                dynamic_handler=self._handle_examine_container  # Complex logic
            )
        }
        
        # HACKING PATH - Terminal access puzzles
        hacking_path = {
            "hack_alpha": PuzzleCommand(
                command="hack alpha",
                requires=["room_scanned"],
                missing_req=[">> Terminal not found. Scan first."],
                dynamic_handler=self._handle_hack_terminal_alpha
            ),
            
            "hack_beta": PuzzleCommand(
                command="hack beta",
                requires=["room_scanned"],
                missing_req=[">> Terminal not found. Scan first."],
                dynamic_handler=self._handle_hack_terminal_beta
            )
        }
        
        # COMBINATION PATH - Multi-step puzzle
        combination_path = {
            "combine_keys": PuzzleCommand(
                command="combine red blue",
                requires=["red_key_found", "blue_key_found"],
                sets="master_key_created",
                missing_req=[">> You need both keys first."],
                already_done=[">> Already created the master key."],
                success=[
                    ">> The keys resonate together...",
                    ">> They merge into a purple master key!",
                    ">> New item: Master Key"
                ]
            ),
            
            "unlock_exit": PuzzleCommand(
                command="use master key",
                requires=["master_key_created"],
                missing_req=[">> You don't have that item."],
                transition="next",  # Go to next room
                transition_msg=[  # Messages during transition
                    ">> The master key fits perfectly.",
                    ">> The exit door slides open with a hiss.",
                    ">> You step through into the unknown..."
                ]
            )
        }
        
        # SECRET PATH - Hidden commands for explorers
        secret_path = {
            "whisper": PuzzleCommand(
                command="whisper void",
                sets="void_contacted",
                success=[
                    ">> You whisper into the darkness...",
                    ">> The void whispers back: 'SEEK THE PATTERN'",
                    ">> A new understanding dawns."
                ]
            ),
            
            "pattern": PuzzleCommand(
                command="trace pattern",
                requires=["void_contacted"],
                missing_req=[">> What pattern? There's nothing here."],
                transition="secret",
                transition_msg=[
                    ">> You trace the hidden pattern in the air.",
                    ">> Reality flickers...",
                    ">> A secret passage opens!"
                ]
            )
        }
        
        # DIAGNOSTIC PATH - Help and status commands
        diagnostic_path = {
            "status": PuzzleCommand(
                command="status",
                dynamic_handler=self._handle_status
            ),
            
            "hint": PuzzleCommand(
                command="hint",
                dynamic_handler=self._handle_hint
            )
        }
        
        # Register all paths with the processor
        self.processor.add_puzzle_path("discovery", discovery_path)
        self.processor.add_puzzle_path("hacking", hacking_path)
        self.processor.add_puzzle_path("combination", combination_path)
        self.processor.add_puzzle_path("secret", secret_path)
        self.processor.add_puzzle_path("diagnostic", diagnostic_path)
    
    # ==========================================
    # PROGRESSION HINT - Guide the player
    # ==========================================
    
    def _get_progression_hint(self, game_state) -> str:
        """
        Return contextual hints based on game state.
        This is called by enter_room to guide players.
        
        Good hints:
        - Are specific to current state
        - Suggest next action without spoiling
        - Build atmosphere
        """
        
        if not game_state.get_flag("room_scanned"):
            return ">> The room is dim. Your scanner might help illuminate things."
        
        elif not game_state.get_flag("container_examined"):
            return ">> The terminals hum quietly. That container looks interesting too."
        
        elif not self._both_keys_found(game_state):
            if game_state.get_flag("red_key_found"):
                return ">> The red key pulses in your inventory. Its partner must be near."
            elif game_state.get_flag("blue_key_found"):
                return ">> The blue key feels incomplete alone. Keep searching."
            else:
                return ">> The terminals guard their secrets. Perhaps the right words will help."
        
        elif not game_state.get_flag("master_key_created"):
            return ">> Two keys, two colors... what happens when they meet?"
        
        else:
            return ">> The master key thrums with power. The exit awaits."
    
    # ==========================================
    # SPECIFIC INPUT HANDLER - Custom commands
    # ==========================================
    
    def _handle_specific_input(self, cmd: str, game_state):
        """
        Handle room-specific commands that don't fit the puzzle path model.
        This is called for any unmatched commands.
        
        Examples:
        - Commands with variable syntax
        - Free-form input
        - Complex parsing needs
        """
        
        # Example: Handle "examine [anything]" dynamically
        if cmd.startswith("examine "):
            target = cmd[8:].strip()
            return None, self._examine_anything(target, game_state)
        
        # Example: Handle password attempts
        if cmd.startswith("enter password "):
            password = cmd[15:].strip()
            return None, self._check_password(password, game_state)
        
        # Example: Handle speaking any phrase
        if cmd.startswith("speak "):
            phrase = cmd[6:].strip()
            return None, self._handle_speak(phrase, game_state)
        
        return None, None
    
    # ==========================================
    # DYNAMIC HANDLERS - Complex puzzle logic
    # ==========================================
    
    def _handle_examine_container(self, game_state):
        """
        Example of a dynamic handler for complex examination logic.
        These are referenced in PuzzleCommand(dynamic_handler=...)
        """
        game_state.set_flag("container_examined", True)
        
        lines = [
            ">> You approach the metal container.",
            ">> It's locked with a complex mechanism.",
            ">> Two key slots are visible - one red, one blue."
        ]
        
        # Dynamic content based on progress
        if game_state.get_flag("alpha_terminal_hacked"):
            lines.append(">> The alpha terminal's screen reflects off the metal.")
        
        if game_state.get_flag("beta_terminal_hacked"):
            lines.append(">> You notice beta terminal coordinates etched below: 27.3, 42.1")
        
        return None, lines
    
    def _handle_hack_terminal_alpha(self, game_state):
        """Handle hacking the alpha terminal"""
        if game_state.get_flag("alpha_terminal_hacked"):
            return None, [">> Terminal already unlocked."]
        
        # Set up password prompt
        game_state.set_flag("awaiting_alpha_password", True)
        
        return None, [
            ">> Accessing Alpha Terminal...",
            f">> {self.terminals['alpha']['description']}",
            ">> PASSWORD REQUIRED",
            ">> Hint: What binds but can break?",
            ">> Enter password: (type 'enter password [word]')"
        ]
    
    def _handle_hack_terminal_beta(self, game_state):
        """Handle hacking the beta terminal"""
        if game_state.get_flag("beta_terminal_hacked"):
            return None, [">> Terminal already unlocked."]
        
        lines = [
            ">> Accessing Beta Terminal...",
            f">> {self.terminals['beta']['description']}",
            ">> SECURITY CHALLENGE:"
        ]
        
        # Example: Different puzzle type - logic puzzle
        if not game_state.get_flag("beta_puzzle_shown"):
            game_state.set_flag("beta_puzzle_shown", True)
            lines.extend([
                ">> If 1=5, 2=25, 3=125, then 4=?",
                ">> Speak the answer to proceed."
            ])
        else:
            lines.append(">> The puzzle still awaits your answer.")
        
        return None, lines
    
    def _handle_status(self, game_state):
        """Show detailed room progress"""
        lines = [">> ROOM STATUS:"]
        lines.append("")
        
        # Scan status
        if game_state.get_flag("room_scanned"):
            lines.append("✓ Room scanned")
        else:
            lines.append("✗ Room not scanned")
        
        # Terminal status
        lines.append("")
        lines.append("TERMINALS:")
        for terminal_id, terminal in self.terminals.items():
            if game_state.get_flag(f"{terminal_id}_terminal_hacked"):
                lines.append(f"  ✓ {terminal['name']} - UNLOCKED")
            else:
                lines.append(f"  ✗ {terminal['name']} - LOCKED")
        
        # Key status
        lines.append("")
        lines.append("ITEMS:")
        if game_state.get_flag("red_key_found"):
            lines.append("  ✓ Red Key")
        if game_state.get_flag("blue_key_found"):
            lines.append("  ✓ Blue Key")
        if game_state.get_flag("master_key_created"):
            lines.append("  ✓ Master Key")
        
        # Progress percentage
        total_flags = 7  # Total possible progress flags
        completed = sum([
            game_state.get_flag("room_scanned"),
            game_state.get_flag("container_examined"),
            game_state.get_flag("alpha_terminal_hacked"),
            game_state.get_flag("beta_terminal_hacked"),
            game_state.get_flag("red_key_found"),
            game_state.get_flag("blue_key_found"),
            game_state.get_flag("master_key_created")
        ])
        
        lines.append("")
        lines.append(f"Progress: {completed}/{total_flags} ({int(completed/total_flags*100)}%)")
        
        return None, lines
    
    def _handle_hint(self, game_state):
        """Provide contextual hints"""
        # Smart hint system based on current progress
        if not game_state.get_flag("room_scanned"):
            return None, [">> HINT: Start by scanning your environment."]
        
        if game_state.get_flag("awaiting_alpha_password"):
            return None, [">> HINT: The password is about human connections..."]
        
        if game_state.get_flag("beta_puzzle_shown") and not game_state.get_flag("beta_terminal_hacked"):
            return None, [">> HINT: Look at the pattern. Each number relates to powers..."]
        
        if self._both_keys_found(game_state) and not game_state.get_flag("master_key_created"):
            return None, [">> HINT: You have both keys. Can they work together?"]
        
        return None, [">> HINT: Explore everything. Examine objects carefully."]
    
    # ==========================================
    # HELPER METHODS - Utilities and validation
    # ==========================================
    
    def _check_password(self, password: str, game_state):
        """Check password attempts for terminals"""
        if game_state.get_flag("awaiting_alpha_password"):
            if password.lower() == self.terminals["alpha"]["password"]:
                game_state.set_flag("alpha_terminal_hacked", True)
                game_state.set_flag("awaiting_alpha_password", False)
                game_state.set_flag("red_key_found", True)
                
                return [
                    ">> PASSWORD ACCEPTED",
                    ">> Alpha Terminal unlocked!",
                    ">> Terminal dispensing item...",
                    ">> Obtained: Red Access Key"
                ]
            else:
                return [">> ACCESS DENIED. Try again."]
        
        return [">> No password prompt active."]
    
    def _handle_speak(self, phrase: str, game_state):
        """Handle spoken phrases - for riddles and passwords"""
        # Beta terminal logic puzzle
        if game_state.get_flag("beta_puzzle_shown") and not game_state.get_flag("beta_terminal_hacked"):
            if phrase == "625" or phrase == "5^4":
                game_state.set_flag("beta_terminal_hacked", True)
                game_state.set_flag("blue_key_found", True)
                
                return [
                    ">> CORRECT ANSWER",
                    ">> Beta Terminal unlocked!",
                    ">> Terminal dispensing item...",
                    ">> Obtained: Blue Access Key"
                ]
            else:
                return [">> The terminal flashes red. Incorrect."]
        
        # Secret phrases
        if phrase.lower() == "hello darkness":
            return [">> The darkness replies: 'Hello, old friend.'"]
        
        return [f">> You speak '{phrase}' into the air. Nothing happens."]
    
    def _examine_anything(self, target: str, game_state):
        """Flexible examine handler"""
        examinations = {
            "floor": [">> The floor is surprisingly clean. Too clean."],
            "ceiling": [">> Data cables snake across the ceiling like digital vines."],
            "walls": [">> The walls pulse with faint circuitry patterns."],
            "self": [">> You are a digital ghost in the machine."],
            "terminals": [">> Two terminals: Alpha glows green, Beta glows blue."]
        }
        
        if target in examinations:
            return examinations[target]
        
        return [f">> You examine the {target}, but find nothing special."]
    
    def _both_keys_found(self, game_state) -> bool:
        """Check if player has both keys"""
        return (game_state.get_flag("red_key_found") and 
                game_state.get_flag("blue_key_found"))

# ==========================================
# MODULE-LEVEL COMPATIBILITY FUNCTIONS
# ==========================================
# These are required for the room to work with the game engine

def enter_room(game_state):
    """
    Called when player enters the room.
    Creates room instance and returns formatted entry text.
    """
    room = TemplateRoom()
    return room.enter_room(game_state)

def handle_input(cmd, game_state, room_module=None):
    """
    Called for each player command.
    Creates room instance and processes input.
    """
    room = TemplateRoom()
    return room.handle_input(cmd, game_state, room_module)

def get_available_commands():
    """
    Called when player types 'help'.
    Returns list of available commands.
    """
    room = TemplateRoom()
    return room.get_available_commands()# SPYHVER-45: THE

"""
Room Utility Functions - Reduces duplication across room modules
Enhanced with global restart functionality
"""

from typing import Dict, List, Tuple, Optional, Callable, Any

# ==========================================
# ROOM CONFIGURATION CLASSES
# ==========================================

class PuzzleCommand:
    """Represents a single puzzle command configuration"""
    def __init__(self, 
                 command: str,
                 requires: List[str] = None,
                 sets: str = None,
                 success: List[str] = None,
                 already_done: List[str] = None,
                 missing_req: List[str] = None,
                 transition: str = None,
                 transition_msg: List[str] = None,
                 dynamic_handler: Callable = None):
        self.command = command
        self.requires = requires or []
        self.sets = sets
        self.success = success or [">> Command completed."]
        self.already_done = already_done or [">> Already completed."]
        self.missing_req = missing_req or [">> Requirements not met."]
        self.transition = transition
        self.transition_msg = transition_msg
        self.dynamic_handler = dynamic_handler

class RoomConfig:
    """Centralized room configuration"""
    def __init__(self, 
                 name: str,
                 entry_text: List[str],
                 progression_hints: Dict[str, str] = None,
                 destinations: Dict[str, str] = None):
        self.name = name
        self.entry_text = entry_text
        self.progression_hints = progression_hints or {}
        self.destinations = destinations or {}

# ==========================================
# GAME STATE COMPATIBILITY HELPERS
# ==========================================

def get_flag_compat(game_state, flag: str, default: Any = False) -> Any:
    """Get flag value with compatibility for different GameState implementations"""
    if hasattr(game_state, 'get_flag'):
        return game_state.get_flag(flag, default)
    elif hasattr(game_state, 'game_flags'):
        return game_state.game_flags.get(flag, default)
    elif hasattr(game_state, 'flags'):
        return game_state.flags.get(flag, default)
    return default

def set_flag_compat(game_state, flag: str, value: Any = True) -> None:
    """Set flag value with compatibility for different GameState implementations"""
    if hasattr(game_state, 'set_flag'):
        game_state.set_flag(flag, value)
    elif hasattr(game_state, 'game_flags'):
        game_state.game_flags[flag] = value
    elif hasattr(game_state, 'flags'):
        game_state.flags[flag] = value

def clear_flag_compat(game_state, flag: str) -> bool:
    """Clear flag with compatibility for different GameState implementations"""
    if hasattr(game_state, 'clear_flag'):
        return game_state.clear_flag(flag)
    elif hasattr(game_state, 'game_flags') and flag in game_state.game_flags:
        del game_state.game_flags[flag]
        return True
    elif hasattr(game_state, 'flags') and flag in game_state.flags:
        del game_state.flags[flag]
        return True
    return False

# ==========================================
# GENERIC PUZZLE PROCESSOR
# ==========================================

class PuzzleProcessor:
    """Handles puzzle command processing for any room"""
    
    def __init__(self, room_config: RoomConfig):
        self.room_config = room_config
        self.puzzle_paths: Dict[str, Dict[str, PuzzleCommand]] = {}
        self.dynamic_handlers: Dict[str, Callable] = {}
    
    def add_puzzle_path(self, path_name: str, commands: Dict[str, PuzzleCommand]):
        """Add a named puzzle path with its commands"""
        self.puzzle_paths[path_name] = commands
    
    def add_dynamic_handler(self, command: str, handler: Callable):
        """Add a dynamic command handler"""
        self.dynamic_handlers[command] = handler
    
    def process_command(self, cmd: str, game_state) -> Tuple[Optional[str], Optional[List[str]]]:
        """Process any puzzle command across all paths"""
        # Check all puzzle paths
        for path_name, commands in self.puzzle_paths.items():
            for cmd_key, puzzle_cmd in commands.items():
                if cmd == puzzle_cmd.command:
                    return self._handle_puzzle_command(puzzle_cmd, game_state)
        
        # Check dynamic handlers
        if cmd in self.dynamic_handlers:
            return self.dynamic_handlers[cmd](game_state)
        
        return None, None
    
    def _handle_puzzle_command(self, puzzle_cmd: PuzzleCommand, game_state) -> Tuple[Optional[str], Optional[List[str]]]:
        """Handle a single puzzle command"""
        # Check if it has a dynamic handler
        if puzzle_cmd.dynamic_handler:
            return puzzle_cmd.dynamic_handler(game_state)
        
        # Check requirements
        for req in puzzle_cmd.requires:
            if not get_flag_compat(game_state, req):
                return None, puzzle_cmd.missing_req
        
        # Check if already done
        if puzzle_cmd.sets and get_flag_compat(game_state, puzzle_cmd.sets):
            return None, puzzle_cmd.already_done
        
        # Set flag if specified
        if puzzle_cmd.sets:
            set_flag_compat(game_state, puzzle_cmd.sets, True)
        
        # Handle transition
        if puzzle_cmd.transition:
            dest = self.room_config.destinations.get(puzzle_cmd.transition, puzzle_cmd.transition)
            return transition_to_room(dest, puzzle_cmd.transition_msg)
        
        # Return success message
        return None, puzzle_cmd.success

# ==========================================
# ENHANCED ROOM BASE CLASS
# ==========================================

class BaseRoom:
    """Base class for all rooms to reduce duplication"""
    
    def __init__(self, room_config: RoomConfig):
        self.config = room_config
        self.processor = PuzzleProcessor(room_config)
        self.command_descriptions = []
        self.last_input = ""  # Store last input for complex parsing
        self.room_id = room_config.name.lower().replace(" ", "_")
        self._setup_puzzles()
    
    def _setup_puzzles(self):
        """Override in subclasses to set up puzzle paths"""
        pass
    
    def enter_room(self, game_state) -> List[str]:
        """Standard room entry with progression hints"""
        lines = self.config.entry_text.copy()
        
        # Add progression hint based on state
        hint = self._get_progression_hint(game_state)
        if hint:
            lines.extend(["", hint])
        
        return format_enter_lines(self.config.name, lines)
    
    def _get_progression_hint(self, game_state) -> Optional[str]:
        """Override in subclasses for custom progression logic"""
        return None
    
    def handle_input(self, cmd: str, game_state, room_module=None) -> Tuple[Optional[str], List[str]]:
        """Standard input handler"""
        # Store the original input for complex parsing
        self.last_input = cmd
        
        # Check standard commands first (including global restart)
        handled, response = standard_commands(cmd, game_state, room_module)
        if handled:
            return None, response
        
        cmd = cmd.lower().strip()
        
        # Let subclass handle specific commands first
        transition, response = self._handle_specific_input(cmd, game_state)
        if response is not None:
            return transition, response
        
        # Process puzzle commands
        transition, response = self.processor.process_command(cmd, game_state)
        if response is not None:
            return transition, response
        
        return None, [">> Unknown command. Try 'help' for available options."]
    
    def _handle_specific_input(self, cmd: str, game_state) -> Tuple[Optional[str], Optional[List[str]]]:
        """Override in subclasses for room-specific commands"""
        return None, None
    
    def get_available_commands(self) -> List[str]:
        """Return command descriptions"""
        return self.command_descriptions

# ==========================================
# UTILITY FUNCTIONS
# ==========================================

def format_enter_lines(title: str, body_lines: List[str]) -> List[str]:
    """Format room entry text"""
    return [
        f"\n=== {title.upper()} ===",
        *body_lines,
        ""
    ]

def transition_to_room(new_room: str, transition_msg: List[str] = None) -> Tuple[str, List[str]]:
    """Transition to a new room with optional message"""
    if transition_msg:
        return new_room, transition_msg
    return new_room, [f">> Transitioning to {new_room}..."]

def print_inventory(game_state) -> List[str]:
    """Display inventory"""
    inv = game_state.inventory
    return [f"Inventory: {', '.join(inv)}" if inv else "Inventory is empty."]

def describe_flags(game_state, prefix: str = "") -> List[str]:
    """Debug: show all flags"""
    # Handle both possible attribute names for flags
    flags_dict = getattr(game_state, 'flags', None) or getattr(game_state, 'game_flags', {})
    return [f"{prefix}{k}: {v}" for k, v in flags_dict.items() if v]

# ==========================================
# RESTART FUNCTIONALITY
# ==========================================

def handle_restart_command(cmd: str, game_state) -> Tuple[bool, Optional[List[str]]]:
    """
    Handle restart commands globally across all rooms.
    Returns (handled, response) tuple.
    """
    parts = cmd.split()
    
    if parts[0] not in ['restart', 'reset']:
        return False, None
    
    if len(parts) == 1:
        # Just "restart" or "reset" - show options
        return True, [
            "=== RESTART OPTIONS ===",
            "restart room     - Reset current room puzzles",
            "restart game     - Reset entire game to beginning",
            "restart confirm  - Confirm full game reset",
            "",
            "Note: 'restart room' keeps your inventory and progress in other rooms"
        ]
    
    if len(parts) >= 2:
        option = parts[1]
        
        if option == "room":
            return True, restart_current_room(game_state)
        elif option == "game":
            return True, [
                "=== WARNING ===",
                "This will reset ALL progress, inventory, and flags!",
                "Type 'restart confirm' to proceed, or any other command to cancel."
            ]
        elif option == "confirm":
            return True, restart_entire_game(game_state)
    
    return True, ["Invalid restart command. Type 'restart' for options."]

def restart_current_room(game_state) -> List[str]:
    """Reset only the current room's state."""
    current_room = game_state.current_room
    
    # Handle both possible attribute names for flags
    flags_dict = getattr(game_state, 'flags', None) or getattr(game_state, 'game_flags', {})
    
    # Get all flags to clear
    flags_to_clear = []
    for flag in list(flags_dict.keys()):
        # Clear flags that contain the room name or are likely room-specific
        if (current_room in flag or 
            flag.startswith(current_room) or
            flag.endswith(f"_{current_room}") or
            # Also clear common room-specific patterns
            any(pattern in flag for pattern in [
                'terminal_accessed', 'password_entered', 'puzzle_solved',
                'door_opened', 'item_found', 'sequence_complete',
                '_examined', '_unlocked', '_activated', '_discovered'
            ])):
            flags_to_clear.append(flag)
    
    # Clear the flags
    for flag in flags_to_clear:
        if hasattr(game_state, 'flags'):
            del game_state.flags[flag]
        else:
            del game_state.game_flags[flag]
    
    lines = [
        f"=== RESTARTING ROOM: {current_room.upper()} ===",
        f"Cleared {len(flags_to_clear)} room-specific flags.",
        "Your inventory and progress in other rooms remain intact.",
        ""
    ]
    
    return lines

def restart_entire_game(game_state) -> List[str]:
    """Reset the entire game to initial state."""
    # Clear all flags - handle both possible attribute names
    if hasattr(game_state, 'flags'):
        game_state.flags.clear()
    elif hasattr(game_state, 'game_flags'):
        game_state.game_flags.clear()
    
    # Clear inventory
    game_state.inventory.clear()
    
    # Reset score and health if they exist
    if hasattr(game_state, 'score'):
        game_state.score = 0
    if hasattr(game_state, 'health'):
        game_state.health = 100
    
    # Clear any custom game state variables
    if hasattr(game_state, 'variables'):
        game_state.variables.clear()
    
    # Reset to starting room
    starting_room = 'boot' if hasattr(game_state, 'current_room') else 'start'
    if hasattr(game_state, 'current_room'):
        game_state.current_room = starting_room
    
    lines = [
        "=== GAME RESET COMPLETE ===",
        "All progress has been erased.",
        "Starting from the beginning...",
        ""
    ]
    
    return lines

# ==========================================
# STANDARD COMMANDS
# ==========================================

GLOBAL_COMMANDS = {
    "look": lambda gs: [">> You scan the area... but nothing changes."],
    "observe": lambda gs: [">> You observe carefully, but nothing new stands out."],
    "scan": lambda gs: [">> You run a basic scan, but no anomalies are found."],
    "inventory": print_inventory,
    "inv": print_inventory,
    "i": print_inventory,
    "flags": lambda gs: describe_flags(gs),
    "status": lambda gs: [
        ">> STATUS:",
        f"   Current Room: {gs.current_room if hasattr(gs, 'current_room') else 'unknown'}",
        f"   Inventory: {', '.join(gs.inventory) if gs.inventory else 'empty'}",
        f"   Score: {getattr(gs, 'score', 0)}",
        f"   Health: {getattr(gs, 'health', 100)}"
    ],
}

def standard_commands(cmd: str, game_state, room_module=None) -> Tuple[bool, Optional[List[str]]]:
    """Process standard/global commands"""
    cmd = cmd.strip().lower()
    
    # Check restart commands first
    handled, response = handle_restart_command(cmd, game_state)
    if handled:
        return True, response

    if cmd in GLOBAL_COMMANDS:
        return True, GLOBAL_COMMANDS[cmd](game_state)

    if cmd == "help":
        help_lines = [
            ">> Universal commands:",
            "  look / scan / observe - examine your surroundings",
            "  inventory / i         - view held items",
            "  status                - view current game status",
            "  restart               - restart options (room/game)",
            "  flags                 - list game flags (debug)",
            "  help                  - show this help menu"
        ]
        
        if room_module and hasattr(room_module, "get_available_commands"):
            room_cmds = room_module.get_available_commands()
            if room_cmds:
                help_lines.extend([
                    "",
                    ">> Room-specific commands:",
                    *[f"  {c}" for c in room_cmds]
                ])
        
        return True, help_lines

    return False, None

# ==========================================
# SPECIALIZED ROOM PATTERNS
# ==========================================

class TimedPuzzleRoom(BaseRoom):
    """Base for rooms with timing-based puzzles"""
    
    def __init__(self, room_config: RoomConfig, timing_config: Dict[str, Any]):
        self.timing_config = timing_config
        super().__init__(room_config)
    
    def initialize_sequence_state(self, game_state):
        """Initialize timing sequence state"""
        state_key = f"{self.config.name.lower().replace(' ', '_')}_sequence_state"
        if not game_state.get(state_key):
            game_state.set(state_key, {
                "active": False,
                "current_step": 0,
                "last_action_time": 0,
                "sequence_start_time": 0
            })
        return game_state.get(state_key)

class GridNavigationRoom(BaseRoom):
    """Base for rooms with grid/network navigation"""
    
    def __init__(self, room_config: RoomConfig, grid_config: Dict[str, Any]):
        self.grid_config = grid_config
        super().__init__(room_config)
    
    def get_current_position(self, game_state) -> str:
        """Get current position in grid"""
        return game_state.get("grid_position", self.grid_config.get("start_position"))
    
    def move_to_position(self, new_pos: str, game_state):
        """Move to new position in grid"""
        game_state.set("grid_position", new_pos)

class MemoryPuzzleRoom(BaseRoom):
    """Base for rooms with memory/pattern puzzles"""
    
    def __init__(self, room_config: RoomConfig, memory_config: Dict[str, Any]):
        self.memory_config = memory_config
        super().__init__(room_config)
    
    def check_pattern(self, input_pattern: List[str], game_state) -> bool:
        """Check if input matches required pattern"""
        correct_pattern = self.memory_config.get("correct_pattern", [])
        return input_pattern == correct_pattern

# ==========================================
# QUICK CONVERSION HELPERS
# ==========================================

def convert_puzzle_dict_to_commands(puzzle_dict: Dict[str, Dict]) -> Dict[str, PuzzleCommand]:
    """Convert old-style puzzle dict to PuzzleCommand objects"""
    commands = {}
    for key, config in puzzle_dict.items():
        commands[key] = PuzzleCommand(
            command=config.get("command"),
            requires=config.get("requires", []),
            sets=config.get("sets"),
            success=config.get("success"),
            already_done=config.get("already_done"),
            missing_req=config.get("missing_req"),
            transition=config.get("transition"),
            transition_msg=config.get("transition_msg"),
            dynamic_handler=config.get("dynamic_response")  # Will need custom handling
        )
    return commands

# ==========================================
# BACKWARDS COMPATIBILITY
# ==========================================

# For rooms using the old process_puzzle_command function
def process_puzzle_command(cmd, game_state, puzzle_config):
    """
    Legacy processor for puzzle commands.
    Kept for backwards compatibility with dictionary-based rooms.
    """
    for action_key, action in puzzle_config.items():
        # Check if this is the right command
        if cmd == action["command"] or cmd.startswith(action["command"] + " "):
            
            # Handle dynamic responses (custom logic)
            if action.get("dynamic_response"):
                # This would need to be handled by the room's custom logic
                return None, None
            
            # Check requirements
            for req in action.get("requires", []):
                if not get_flag_compat(game_state, req):
                    return None, action.get("missing_req", [">> Requirement not met."])
            
            # Check if already done (for non-transition commands)
            if "sets" in action and get_flag_compat(game_state, action["sets"]):
                return None, action.get("already_done", [">> Already completed."])
            
            # Set flag if specified
            if "sets" in action:
                set_flag_compat(game_state, action["sets"], True)
            
            # Handle transition
            if action.get("transition"):
                dest = action.get("transition_dest", "next")
                return transition_to_room(dest, action["transition_msg"])
            
            # Return success message
            return None, action["success"]
    
    return None, None
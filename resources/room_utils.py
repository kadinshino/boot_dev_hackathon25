# """
# Room Utility Functions - Shared across all room modules
# """

# def format_enter_lines(title, body_lines):
#     return [
#         f"\n=== {title.upper()} ===",
#         *body_lines,
#         ""
#     ]

# def print_inventory(game_state):
#     inv = game_state.inventory
#     return [f"Inventory: {', '.join(inv)}" if inv else "Inventory is empty."]

# def describe_flags(game_state, prefix=""):
#     return [f"{prefix}{k}: {v}" for k, v in game_state.flags.items()]

# def load_room_intro(config):
#     return format_enter_lines(config["name"], config["entry_text"])

# def transition_to_room(game_state, new_room):
#     game_state.current_room = new_room
#     return f">> Transitioning to {new_room}..."

# def flags_all_set(game_state, flags):
#     return all(game_state.get_flag(f) for f in flags)

# def flags_any_set(game_state, flags):
#     return any(game_state.get_flag(f) for f in flags)

# def get_room_path_type(room_name: str) -> str:
#     name = room_name.lower()
#     if "beacon" in name:
#         return "beacon"
#     if "whisper" in name:
#         return "whisper"
#     return "neutral"

# # Puzzle step processing utility
# def process_puzzle_command(cmd, game_state, steps_dict):
#     cmd = cmd.strip().lower()
#     for step_id, step in steps_dict.items():
#         if cmd == step.get("command"):
#             if not flags_all_set(game_state, step.get("requires", [])):
#                 return None, step.get("fail", [">> You can't do that yet."])
#             if game_state.get_flag(step["sets"]):
#                 return None, step.get("already_done", [">> Already done."])
#             game_state.set_flag(step["sets"])
#             return step_id, step.get("success", [">> Success."])
#     return None, None

# # Global commands and router
# GLOBAL_COMMANDS = {
#     "look": lambda gs: [">> You scan the area... but nothing changes."],
#     "observe": lambda gs: [">> You observe carefully, but nothing new stands out."],
#     "scan": lambda gs: [">> You run a basic scan, but no anomalies are found."],
#     "inventory": print_inventory,
#     "inv": print_inventory,
#     "i": print_inventory,
#     "flags": lambda gs: describe_flags(gs),
#     "help": lambda gs: [
#         ">> Universal commands:",
#         "  look / scan / observe - examine your surroundings",
#         "  inventory / i         - view held items",
#         "  flags                 - list game flags (debug)",
#         "  help                  - show this help menu"
#     ]
# }

# def standard_commands(cmd, game_state, room_module=None):
#     cmd = cmd.strip().lower()

#     if cmd in GLOBAL_COMMANDS:
#         return True, GLOBAL_COMMANDS[cmd](game_state)

#     if room_module and hasattr(room_module, "get_available_commands"):
#         room_cmds = room_module.get_available_commands()
#         if cmd == "help" and room_cmds:
#             return True, [
#                 *GLOBAL_COMMANDS["help"](game_state),
#                 "",
#                 ">> Room-specific commands:",
#                 *[f"  {c}" for c in room_cmds]
#             ]

#     return False, None

# # def debug_room_state(game_state):
# #     return [
# #         f">> Current room: {game_state.current_room}",
# #         f">> Score: {game_state.score}",
# #         f">> Health: {game_state.health}",
# #         f">> Inventory: {', '.join(game_state.inventory)}",
# #         f">> Flags: {len(game_state.flags)} total"
# #     ]

"""
Enhanced Room Utility Functions - Reduces duplication across room modules
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
            if not game_state.get_flag(req):
                return None, puzzle_cmd.missing_req
        
        # Check if already done
        if puzzle_cmd.sets and game_state.get_flag(puzzle_cmd.sets):
            return None, puzzle_cmd.already_done
        
        # Set flag if specified
        if puzzle_cmd.sets:
            game_state.set_flag(puzzle_cmd.sets, True)
        
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
        # Check standard commands first
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
# UTILITY FUNCTIONS (Enhanced)
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
    return [f"{prefix}{k}: {v}" for k, v in game_state.flags.items()]

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
}

def standard_commands(cmd: str, game_state, room_module=None) -> Tuple[bool, Optional[List[str]]]:
    """Process standard/global commands"""
    cmd = cmd.strip().lower()

    if cmd in GLOBAL_COMMANDS:
        return True, GLOBAL_COMMANDS[cmd](game_state)

    if cmd == "help":
        help_lines = [
            ">> Universal commands:",
            "  look / scan / observe - examine your surroundings",
            "  inventory / i         - view held items",
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
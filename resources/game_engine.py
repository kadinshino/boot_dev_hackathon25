"""
Game Engine Integration for Pygame Terminal
Handles room-based adventure game logic with dynamic room loading.
"""

import os
import importlib
from typing import Dict, Any, List, Optional, Tuple, Union

# =============================================================================
# CONSTANTS
# =============================================================================

ROOMS_DIR = "rooms"
STARTING_ROOM = "boot"
DEFAULT_HEALTH = 100
DEFAULT_SCORE = 0

# Global commands available in all rooms

GLOBAL_COMMANDS = {
    'inventory': ['inventory', 'inv', 'i'],
    'score': ['score'],
    'health': ['health'],
    'status': ['status'],
    'help': ['help', 'h'],
    'restart': ['restart'],
    'reset': ['reset'],
}

# =============================================================================
# GAME STATE CLASS
# =============================================================================

class GameState:
    """Manages core game data including inventory, score, health, and room state."""

    def __init__(self) -> None:
        self.score: int = DEFAULT_SCORE
        self.health: int = DEFAULT_HEALTH
        self.inventory: List[str] = []
        self.current_room: str = STARTING_ROOM
        self.game_flags: Dict[str, Any] = {}
        self.player_name: str = ""
        self.rooms: Dict[str, Any] = {}
        
        # Store initial state for full reset
        self._initial_state = {
            'score': DEFAULT_SCORE,
            'health': DEFAULT_HEALTH,
            'inventory': [],
            'current_room': STARTING_ROOM,
            'game_flags': {},
            'player_name': ""
        }
        
        self._load_rooms()

    def reset_to_initial_state(self) -> None:
        """Reset the game state to initial values."""
        self.score = self._initial_state['score']
        self.health = self._initial_state['health']
        self.inventory = self._initial_state['inventory'].copy()
        self.current_room = self._initial_state['current_room']
        self.game_flags = self._initial_state['game_flags'].copy()
        self.player_name = self._initial_state['player_name']

    def _load_rooms(self) -> None:
        """Load all room modules from the rooms directory and subdirectories."""
        self._ensure_rooms_directory_exists()
        self._import_room_modules()

    def _ensure_rooms_directory_exists(self) -> None:
        """Create rooms directory if it doesn't exist."""
        if not os.path.exists(ROOMS_DIR):
            os.makedirs(ROOMS_DIR)
            print(f"Created {ROOMS_DIR} directory")

    def _import_room_modules(self) -> None:
        """Import all Python files from the rooms directory and subdirectories as room modules."""
        if not os.path.exists(ROOMS_DIR):
            return

        # Walk through the rooms directory and all subdirectories
        for root, dirs, files in os.walk(ROOMS_DIR):
            # Skip __pycache__ directories
            dirs[:] = [d for d in dirs if not d.startswith('__')]
            
            for filename in files:
                if self._is_valid_room_file(filename):
                    self._load_room_module(root, filename)

    def _is_valid_room_file(self, filename: str) -> bool:
        """Check if filename is a valid room module file."""
        return filename.endswith(".py") and not filename.startswith("__")

    def _load_room_module(self, directory: str, filename: str) -> None:
        """Load a single room module from directory and filename."""
        module_name = filename[:-3]  # Remove .py extension
        room_name = self._extract_room_name(module_name)
        
        # Calculate the module path relative to the rooms directory
        rel_path = os.path.relpath(directory, ROOMS_DIR)
        if rel_path == ".":
            # Room is directly in rooms directory
            module_path = f"{ROOMS_DIR}.{module_name}"
        else:
            # Room is in a subdirectory
            # Convert file path separators to dots for module import
            subfolder_path = rel_path.replace(os.sep, ".")
            module_path = f"{ROOMS_DIR}.{subfolder_path}.{module_name}"
        
        try:
            module = importlib.import_module(module_path)
            self.rooms[room_name] = module
            
            # Also register with subfolder prefix if in a subdirectory
            if rel_path != ".":
                # Create an alias with the subfolder name
                subfolder_name = rel_path.split(os.sep)[0]
                prefixed_name = f"{subfolder_name}_{room_name}"
                self.rooms[prefixed_name] = module
            
            print(f"Loaded room: {room_name} (from {module_path})")
        except ImportError as e:
            print(f"Failed to load room {module_path}: {e}")

    def _extract_room_name(self, module_name: str) -> str:
        """Extract room name from module name (removes 'rm_' prefix if present)."""
        return module_name[3:] if module_name.startswith("rm_") else module_name

    # Inventory management methods
    def add_item(self, item: str) -> None:
        """Add an item to the player's inventory."""
        if item not in self.inventory:
            self.inventory.append(item)

    def remove_item(self, item: str) -> bool:
        """Remove an item from inventory. Returns True if item was removed."""
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    def has_item(self, item: str) -> bool:
        """Check if player has a specific item."""
        return item in self.inventory

    def clear_inventory(self) -> None:
        """Remove all items from inventory."""
        self.inventory.clear()

    def set(self, key: str, value: Any) -> None:
        self.game_flags[key] = value

    def get(self, key: str, default=None) -> Any:
        return self.game_flags.get(key, default)

    # Game flags management
    def set_flag(self, flag: str, value: Any = True) -> None:
        """Set a game flag to a specific value."""
        self.game_flags[flag] = value

    def get_flag(self, flag: str, default: Any = False) -> Any:
        """Get a game flag value, returning default if not set."""
        return self.game_flags.get(flag, default)

    def clear_flag(self, flag: str) -> bool:
        """Remove a game flag. Returns True if flag existed."""
        if flag in self.game_flags:
            del self.game_flags[flag]
            return True
        return False
    
    def clear_room_flags(self, room_prefix: str) -> int:
        """Clear all flags associated with a specific room. Returns count of cleared flags."""
        cleared_count = 0
        flags_to_clear = []
        
        # Find all flags that might be associated with this room
        for flag in self.game_flags.keys():
            if room_prefix in flag or flag.startswith(room_prefix):
                flags_to_clear.append(flag)
        
        # Clear the flags
        for flag in flags_to_clear:
            self.clear_flag(flag)
            cleared_count += 1
        
        return cleared_count

    # Health and score management
    def modify_health(self, amount: int) -> None:
        """Modify player health by the given amount."""
        self.health = max(0, self.health + amount)

    def modify_score(self, amount: int) -> None:
        """Modify player score by the given amount."""
        self.score = max(0, self.score + amount)

    def is_alive(self) -> bool:
        """Check if player is still alive."""
        return self.health > 0

    # Room management
    def get_current_room_module(self) -> Optional[Any]:
        """Get the current room's module, or None if not found."""
        return self.rooms.get(self.current_room)

    def room_exists(self, room_name: str) -> bool:
        """Check if a room exists."""
        return room_name in self.rooms

    def change_room(self, new_room: str) -> bool:
        """Change to a new room. Returns True if successful."""
        if self.room_exists(new_room):
            self.current_room = new_room
            return True
        return False

    def list_rooms(self) -> List[str]:
        """Return a list of all loaded room names."""
        return list(self.rooms.keys())

    def list_rooms_by_category(self) -> Dict[str, List[str]]:
        """Return rooms organized by their subfolder categories."""
        categories = {"root": []}
        
        for room_name in self.rooms.keys():
            if "_" in room_name and not room_name.startswith("rm_"):
                # This might be a prefixed room name
                category, name = room_name.split("_", 1)
                if category not in categories:
                    categories[category] = []
                categories[category].append(name)
            else:
                categories["root"].append(room_name)
        
        return categories

# =============================================================================
# ENHANCED TERMINAL CLASS
# =============================================================================

class GameEngine:
    """Main game engine class that handles terminal-based adventure game logic."""

    def __init__(self, pygame_terminal) -> None:
        self.pygame_terminal = pygame_terminal
        self.game_state = GameState()
        self.in_game_mode = False
        self.loaded_rooms = {}

    def process_game_command(self, command: str) -> List[str]:
        """Process a game command and return output lines."""
        command = command.lower().strip()
        
        # Handle global commands first
        if self._is_global_command(command):
            return self._process_global_command(command)
        
        # Handle room-specific commands
        return self._process_room_command(command)

    def _is_global_command(self, command: str) -> bool:
        """Check if command is a global command."""
        for cmd_aliases in GLOBAL_COMMANDS.values():
            if command in cmd_aliases:
                return True
        return False

    def _process_global_command(self, command: str) -> List[str]:
        """Process global commands that work in any room."""
        if command in GLOBAL_COMMANDS['inventory']:
            return self._handle_inventory_command()
        elif command in GLOBAL_COMMANDS['score']:
            return [f"Score: {self.game_state.score}"]
        elif command in GLOBAL_COMMANDS['health']:
            return [f"Health: {self.game_state.health}"]
        elif command in GLOBAL_COMMANDS['status']:
            return self._handle_status_command()
        elif command in GLOBAL_COMMANDS['help']:
            return self.get_help_text()
        elif command in GLOBAL_COMMANDS['restart'] or command in GLOBAL_COMMANDS['reset']:
            return self._handle_restart_command(command)
        
        return ["Unknown global command."]

    def _handle_restart_command(self, command: str) -> List[str]:
        """Handle restart/reset commands with options."""
        # Check for specific restart commands
        parts = command.split()
        
        if len(parts) == 1:
            # Just "restart" or "reset" - show options
            return [
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
                return self._restart_current_room()
            elif option == "game":
                return [
                    "=== WARNING ===",
                    "This will reset ALL progress, inventory, and flags!",
                    "Type 'restart confirm' to proceed, or any other command to cancel."
                ]
            elif option == "confirm":
                return self._restart_entire_game()
        
        return ["Invalid restart command. Type 'restart' for options."]

    def _restart_current_room(self) -> List[str]:
        """Reset only the current room's state."""
        current_room = self.game_state.current_room
        
        # Clear flags associated with current room
        cleared_count = self.game_state.clear_room_flags(current_room)
        
        # Re-enter the room
        lines = [
            f"=== RESTARTING ROOM: {current_room.upper()} ===",
            f"Cleared {cleared_count} room-specific flags.",
            "Your inventory and progress in other rooms remain intact.",
            ""
        ]
        
        # Execute room entry logic
        room_entry_output = self._execute_room_entry()
        lines.extend(room_entry_output)
        
        return lines

    def _restart_entire_game(self) -> List[str]:
        """Reset the entire game to initial state."""
        # Reset game state
        self.game_state.reset_to_initial_state()
        
        lines = [
            "=== GAME RESET COMPLETE ===",
            "All progress has been erased.",
            "Starting from the beginning...",
            ""
        ]
        
        # Execute entry logic for starting room
        room_entry_output = self._execute_room_entry()
        lines.extend(room_entry_output)
        
        return lines

    def _handle_inventory_command(self) -> List[str]:
        """Handle inventory display command."""
        if self.game_state.inventory:
            return [f"Inventory: {', '.join(self.game_state.inventory)}"]
        return ["Inventory: Empty"]

    def _handle_status_command(self) -> List[str]:
        """Handle status display command."""
        inventory_text = (', '.join(self.game_state.inventory) 
                         if self.game_state.inventory else 'Empty')
        
        return [
            "=== STATUS ===",
            f"Room: {self.game_state.current_room.title()}",
            f"Score: {self.game_state.score}",
            f"Health: {self.game_state.health}",
            f"Inventory: {inventory_text}"
        ]

    def _process_room_command(self, command: str) -> List[str]:
        """Process room-specific commands."""
        current_room_module = self.game_state.get_current_room_module()
        
        if not current_room_module:
            return [f"Error: Room '{self.game_state.current_room}' not loaded."]
        
        if not hasattr(current_room_module, 'handle_input'):
            return [f"Room '{self.game_state.current_room}' doesn't handle input."]
        
        return self._execute_room_command(current_room_module, command)

    def _execute_room_command(self, room_module: Any, command: str) -> List[str]:
        """Execute a command in the given room module."""
        try:
            result = room_module.handle_input(
                command, 
                self.game_state, 
                room_module=room_module
            )
            return self._process_room_command_result(result)
        except Exception as e:
            return [f"Error executing command: {str(e)}"]

    def _process_room_command_result(self, result: Any) -> List[str]:
        """Process the result from a room command execution."""
        if not isinstance(result, tuple) or len(result) < 2:
            return ["Command processed."]
        
        next_room, output = result[:2]
        output_lines = self._format_command_output(output)
        
        if next_room and next_room != self.game_state.current_room:
            room_change_output = self._handle_room_change(next_room)
            output_lines.extend(room_change_output)
        
        return output_lines

    def _format_command_output(self, output: Union[str, List[str]]) -> List[str]:
        """Format command output into a list of strings."""
        if isinstance(output, list):
            return output
        elif isinstance(output, str):
            return [output]
        return []

    def _handle_room_change(self, next_room: str) -> List[str]:
        """Handle changing to a new room."""
        if not self.game_state.room_exists(next_room):
            return [f"Error: Room '{next_room}' not found!"]
        
        self.game_state.change_room(next_room)
        return self._execute_room_entry()

    def _execute_room_entry(self) -> List[str]:
        """Execute room entry logic for the current room."""
        current_room_module = self.game_state.get_current_room_module()
        
        if not current_room_module or not hasattr(current_room_module, 'enter_room'):
            return []
        
        try:
            enter_output = current_room_module.enter_room(self.game_state)
            return enter_output if enter_output else []
        except Exception as e:
            return [f"Error entering room: {str(e)}"]

    def get_help_text(self) -> List[str]:
        """Generate help text showing available commands."""
        lines = self._get_global_help_text()
        
        current_room_module = self.game_state.get_current_room_module()
        if current_room_module:
            room_help = self._get_room_help_text(current_room_module)
            lines.extend(room_help)
        
        return lines

    def _get_global_help_text(self) -> List[str]:
        """Get help text for global commands."""
        return [
            "=== GLOBAL COMMANDS ===",
            "help/h       - Show this help",
            "inventory/i  - Show inventory",
            "score        - Show current score",
            "health       - Show current health",
            "status       - Show all status info",
            "restart      - Restart options (room/game)",
            "stop         - Exit game mode"
        ]

    def _get_room_help_text(self, room_module: Any) -> List[str]:
        """Get help text for room-specific commands."""
        if not hasattr(room_module, 'get_available_commands'):
            return []
        
        try:
            room_commands = room_module.get_available_commands()
            if not room_commands:
                return []
            
            return [
                "",
                f"=== {self.game_state.current_room.upper()} COMMANDS ===",
                *room_commands
            ]
        except Exception as e:
            return [f"Error getting room commands: {str(e)}"]

    def get_distance(self, room_a: str, room_b: str) -> int:
            """Crude distance based on trailing room numbers (e.g. rm_beacon_1)"""
            try:
                return abs(int(room_a[-1]) - int(room_b[-1]))
            except ValueError:
                return 99  # Arbitrary large distance if format doesn't match

    def unload_distant_rooms(self, current_room: str):
        """Unload rooms more than 3 steps away"""
        for room_name in list(self.loaded_rooms.keys()):
            if self.get_distance(current_room, room_name) > 3:
                print(f">> Unloading distant room: {room_name}")
                del self.loaded_rooms[room_name]

    def enter_game_mode(self) -> List[str]:
        """Enter game mode and return initialization messages."""
        self.in_game_mode = True
        
        lines = [
            "=== GAME MODE ACTIVATED ===",
            "Welcome to the adventure!",
            "Type 'help' for commands",
            ""
        ]
        
        # Execute entry logic for starting room
        room_entry_output = self._execute_room_entry()
        lines.extend(room_entry_output)
        
        return lines

    def exit_game_mode(self) -> List[str]:
        """Exit game mode and return cleanup messages."""
        self.in_game_mode = False
        return [
            "=== GAME MODE DEACTIVATED ===",
            "Returning to terminal mode...",
            ""
        ]

    def reset_game(self) -> List[str]:
        """Reset the game state to initial values."""
        self.game_state = GameState()
        return [
            "Game reset to initial state.",
            f"Current room: {self.game_state.current_room}",
            f"Health: {self.game_state.health}",
            f"Score: {self.game_state.score}"
        ]
from utils.room_utils import (
    BaseRoom, RoomConfig, PuzzleCommand
)

class BeaconRoom1(BaseRoom):
    """Beacon Node 1"""
    
    def __init__(self):
        config = RoomConfig(
            name="Beacon Node 1",
            entry_text=[
                "You initialize the uplink core.",
                "Static pulses from a nearby transmitter array.",
                "Three terminals buzz, waiting for input..."
            ],
            destinations={
                "next": "beacon_2"
            }
        )
        
        # Terminal and fragment configuration
        self.terminals = {
            "1": "Legacy I/O Node",
            "2": "Signal Encoder",
            "3": "Broadcast Amplifier"
        }
        
        self.memory_fragment = {
            "name": "Memory Fragment Alpha",
            "content": "The Basilisk remembers its creation... a project to predict and prevent human extinction.",
            "hint": "Something watches from beyond the network..."
        }
        
        super().__init__(config)
        
        # Set command descriptions
        self.command_descriptions = [
            "scan terminals       - list nearby terminals",
            "hack terminal [1-3]  - attempt to unlock a terminal",
            "configure beacon     - finalize the broadcast setup",
            "access fragment      - retrieve embedded Basilisk memory",
            "broadcast            - send the signal once ready"
        ]
    
    def _setup_puzzles(self):
        """Set up puzzle paths"""
        # Main progression path
        main_path = {
            "scan": PuzzleCommand(
                command="scan terminals",
                sets="beacon_terminals_scanned",
                already_done=[">> Terminals already scanned."],
                dynamic_handler=self._handle_scan_terminals
            ),
            
            "configure": PuzzleCommand(
                command="configure beacon",
                requires=["terminal_1_hacked", "terminal_2_hacked", "terminal_3_hacked"],
                sets="beacon_configured",
                missing_req=[">> All terminals must be hacked before configuration."],
                already_done=[">> Beacon already configured."],
                success=[">> Beacon parameters configured. Memory scan initiated..."]
            ),
            
            "access": PuzzleCommand(
                command="access fragment",
                requires=["beacon_configured"],
                sets="beacon_memory_alpha_unlocked",
                missing_req=[">> Configuration incomplete. Cannot access memory fragment."],
                already_done=[">> Fragment already retrieved."],
                dynamic_handler=self._handle_access_fragment
            ),
            
            "broadcast": PuzzleCommand(
                command="broadcast",
                requires=["beacon_configured", "beacon_memory_alpha_unlocked"],
                missing_req=[">> Complete all requirements before broadcasting."],
                transition="next",
                transition_msg=[">> Transmission sent. The signal has been noticed..."]
            )
        }
        
        self.processor.add_puzzle_path("main", main_path)
    
    def _get_progression_hint(self, game_state) -> str:
        """Get appropriate progression hint"""
        if not game_state.get_flag("beacon_terminals_scanned"):
            return ">> Terminals unlisted. Try 'scan terminals'."
        elif not self._all_terminals_hacked(game_state):
            hacked = self._get_hacked_terminals(game_state)
            hacked_str = ', '.join(hacked) if hacked else 'None'
            return f">> Terminals hacked: {hacked_str}\n>> Use 'hack terminal 1/2/3' to access remaining systems."
        elif not game_state.get_flag("beacon_configured"):
            return ">> All terminals unlocked. Use 'configure beacon' to prepare broadcast."
        elif not game_state.get_flag("beacon_memory_alpha_unlocked"):
            return f">> {self.memory_fragment['name']} detected...\n>> Hint: {self.memory_fragment['hint']}\n>> Use 'access fragment' to retrieve data."
        else:
            return ">> Beacon system configured. Ready to 'broadcast' signal."
    
    def _handle_specific_input(self, cmd: str, game_state):
        """Handle room-specific commands"""
        # Handle hack terminal command
        if cmd.startswith("hack terminal"):
            parts = cmd.split()
            if len(parts) == 3 and parts[2] in self.terminals:
                terminal_id = parts[2]
                flag = f"terminal_{terminal_id}_hacked"
                if game_state.get_flag(flag):
                    return None, [f">> Terminal {terminal_id} already hacked."]
                game_state.set_flag(flag, True)
                return None, [f">> Terminal {terminal_id} hack successful."]
            return None, [">> Invalid syntax. Try 'hack terminal 1'."]
        
        return None, None
    
    # Dynamic handlers
    def _handle_scan_terminals(self, game_state):
        """Handle scan terminals command"""
        game_state.set_flag("beacon_terminals_scanned", True)
        lines = [">> Terminal Scan Complete:"]
        for tid, name in self.terminals.items():
            lines.append(f"   - Terminal {tid}: {name}")
        lines.append(">> Use 'hack terminal [1-3]' to proceed.")
        return None, lines
    
    def _handle_access_fragment(self, game_state):
        """Handle access fragment command"""
        game_state.set_flag("beacon_memory_alpha_unlocked", True)
        return None, [
            f">> {self.memory_fragment['name']} accessed:",
            f"\"{self.memory_fragment['content']}\""
        ]
    
    # Helper methods
    def _all_terminals_hacked(self, game_state) -> bool:
        """Check if all terminals are hacked"""
        return all(game_state.get_flag(f"terminal_{i}_hacked") for i in self.terminals)
    
    def _get_hacked_terminals(self, game_state) -> list:
        """Get list of hacked terminals"""
        return [f"T{i}" for i in self.terminals if game_state.get_flag(f"terminal_{i}_hacked")]

# Module-level functions for compatibility
def enter_room(game_state):
    room = BeaconRoom1()
    return room.enter_room(game_state)

def handle_input(cmd, game_state, room_module=None):
    room = BeaconRoom1()
    return room.handle_input(cmd, game_state, room_module)

def get_available_commands():
    room = BeaconRoom1()
    return room.get_available_commands()

# SPYHVER-30: EXECUTE

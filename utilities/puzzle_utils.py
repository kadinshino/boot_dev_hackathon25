# resources/specialized_rooms.py
"""
Specialized base classes for common room patterns
"""

from typing import Dict, List, Tuple, Optional, Callable, Any
from resources.room_utils import BaseRoom, RoomConfig, PuzzleCommand

class CipherPuzzleRoom(BaseRoom):
    """Base class for rooms with cipher/decryption puzzles"""
    
    def __init__(self, room_config: RoomConfig, cipher_config: Dict[str, Any]):
        self.cipher_config = cipher_config
        super().__init__(room_config)
    
    def _setup_base_cipher_commands(self):
        """Set up common cipher commands"""
        # Scan command
        scan_cmd = PuzzleCommand(
            command="scan crystals",
            sets=f"{self.config.name.lower().replace(' ', '_')}_scanned",
            dynamic_handler=self._handle_scan_items
        )
        
        self.processor.add_puzzle_path("cipher_base", {"scan": scan_cmd})
    
    def _handle_scan_items(self, game_state):
        """Default scan handler - override for custom behavior"""
        flag_name = f"{self.config.name.lower().replace(' ', '_')}_scanned"
        game_state.set_flag(flag_name, True)
        
        lines = [">> Cipher items detected:"]
        for item_id, item_data in self.cipher_config.get("items", {}).items():
            lines.append(f"   - {item_data.get('name', item_id)}")
        
        return None, lines
    
    def validate_decryption(self, item_id: str, attempt: str) -> bool:
        """Validate a decryption attempt - override in subclasses"""
        return False


class NetworkPuzzleRoom(BaseRoom):
    """Base class for rooms with node/network connection puzzles"""
    
    def __init__(self, room_config: RoomConfig, network_config: Dict[str, Any]):
        self.network_config = network_config
        self.nodes = network_config.get("nodes", {})
        self.connections = network_config.get("connections", {})
        self.forbidden_connections = network_config.get("forbidden", {})
        super().__init__(room_config)
    
    def get_network_state(self, game_state) -> Dict[str, Any]:
        """Get or initialize network state"""
        state_key = f"{self.config.name.lower().replace(' ', '_')}_network"
        if not game_state.get(state_key):
            game_state.set(state_key, {
                node_id: {"connected_to": [], "active": False}
                for node_id in self.nodes
            })
        return game_state.get(state_key)
    
    def connect_nodes(self, node1: str, node2: str, game_state) -> List[str]:
        """Connect two nodes in the network"""
        if node1 not in self.nodes or node2 not in self.nodes:
            return [">> Invalid nodes specified."]
        
        # Check forbidden connections
        if self._is_forbidden_connection(node1, node2):
            return [">> Connection forbidden by network protocols."]
        
        network_state = self.get_network_state(game_state)
        
        # Make connection
        if node2 not in network_state[node1]["connected_to"]:
            network_state[node1]["connected_to"].append(node2)
            network_state[node2]["connected_to"].append(node1)
            
            # Check for activation
            self._check_node_activation(node1, network_state, game_state)
            self._check_node_activation(node2, network_state, game_state)
            
            return [f">> Connected {node1} <-> {node2}"]
        
        return [">> Nodes already connected."]
    
    def _is_forbidden_connection(self, node1: str, node2: str) -> bool:
        """Check if connection is forbidden"""
        if node1 in self.forbidden_connections:
            if node2 in self.forbidden_connections[node1]:
                return True
        if node2 in self.forbidden_connections:
            if node1 in self.forbidden_connections[node2]:
                return True
        return False
    
    def _check_node_activation(self, node: str, network_state: Dict, game_state):
        """Check if node should activate - override for custom logic"""
        connections_needed = self.network_config.get("activation_threshold", 2)
        if len(network_state[node]["connected_to"]) >= connections_needed:
            network_state[node]["active"] = True


class SequencePuzzleRoom(BaseRoom):
    """Base class for rooms with sequence/pattern matching puzzles"""
    
    def __init__(self, room_config: RoomConfig, sequence_config: Dict[str, Any]):
        self.sequence_config = sequence_config
        self.correct_sequence = sequence_config.get("correct_sequence", [])
        self.current_sequence = []
        super().__init__(room_config)
    
    def add_to_sequence(self, item: Any, game_state) -> Tuple[bool, List[str]]:
        """Add item to current sequence and check if correct"""
        self.current_sequence.append(item)
        
        # Check if sequence matches so far
        if not self._sequence_matches_partial():
            self.current_sequence = []
            return False, [">> Sequence incorrect. Resetting..."]
        
        # Check if complete
        if len(self.current_sequence) == len(self.correct_sequence):
            if self.current_sequence == self.correct_sequence:
                return True, [">> Sequence complete!"]
            else:
                self.current_sequence = []
                return False, [">> Full sequence incorrect. Resetting..."]
        
        # Partial match
        remaining = len(self.correct_sequence) - len(self.current_sequence)
        return False, [f">> Correct so far. {remaining} more needed."]
    
    def _sequence_matches_partial(self) -> bool:
        """Check if current sequence matches the start of correct sequence"""
        for i, item in enumerate(self.current_sequence):
            if i >= len(self.correct_sequence) or item != self.correct_sequence[i]:
                return False
        return True
    
    def reset_sequence(self):
        """Reset the current sequence"""
        self.current_sequence = []
        return [">> Sequence reset."]


class TimedSequenceRoom(SequencePuzzleRoom):
    """Extended sequence room with timing requirements"""
    
    def __init__(self, room_config: RoomConfig, sequence_config: Dict[str, Any]):
        super().__init__(room_config, sequence_config)
        self.timing_tolerance = sequence_config.get("timing_tolerance", 1.0)
        self.expected_intervals = sequence_config.get("intervals", [])
        self.last_action_time = 0
    
    def add_to_sequence_with_timing(self, item: Any, current_time: float, game_state) -> Tuple[bool, List[str]]:
        """Add item with timing check"""
        # Check timing if not first item
        if self.current_sequence and self.expected_intervals:
            interval_index = len(self.current_sequence) - 1
            if interval_index < len(self.expected_intervals):
                expected = self.expected_intervals[interval_index]
                actual = current_time - self.last_action_time
                
                if abs(actual - expected) > self.timing_tolerance:
                    self.current_sequence = []
                    return False, [
                        f">> Timing incorrect. Expected {expected}s, got {actual:.1f}s",
                        ">> Sequence reset."
                    ]
        
        self.last_action_time = current_time
        return self.add_to_sequence(item, game_state)


class FragmentCollectionRoom(BaseRoom):
    """Base class for rooms where you collect fragments/items"""
    
    def __init__(self, room_config: RoomConfig, fragment_config: Dict[str, Any]):
        self.fragment_config = fragment_config
        self.fragments = fragment_config.get("fragments", {})
        self.required_count = fragment_config.get("required_count", len(self.fragments))
        super().__init__(room_config)
    
    def collect_fragment(self, fragment_id: str, game_state) -> List[str]:
        """Collect a fragment"""
        if fragment_id not in self.fragments:
            return [">> Unknown fragment."]
        
        flag = f"{self.config.name.lower().replace(' ', '_')}_{fragment_id}_collected"
        if game_state.get_flag(flag):
            return [">> Fragment already collected."]
        
        game_state.set_flag(flag, True)
        fragment_info = self.fragments[fragment_id]
        
        lines = [
            f">> Fragment collected: {fragment_info.get('name', fragment_id)}",
            f">> {fragment_info.get('description', '')}"
        ]
        
        # Check if all collected
        collected_count = self.get_collected_count(game_state)
        if collected_count >= self.required_count:
            lines.append(">> All required fragments collected!")
            self._on_all_collected(game_state)
        else:
            lines.append(f">> Progress: {collected_count}/{self.required_count}")
        
        return lines
    
    def get_collected_count(self, game_state) -> int:
        """Get number of collected fragments"""
        count = 0
        for fragment_id in self.fragments:
            flag = f"{self.config.name.lower().replace(' ', '_')}_{fragment_id}_collected"
            if game_state.get_flag(flag):
                count += 1
        return count
    
    def _on_all_collected(self, game_state):
        """Called when all fragments collected - override for custom behavior"""
        pass
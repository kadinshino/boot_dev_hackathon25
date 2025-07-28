from resources.room_utils import (
    BaseRoom, RoomConfig, PuzzleCommand
)

class BeaconRoom3(BaseRoom):
    """Beacon Node 3: Neural Network"""
    
    def __init__(self):
        # Room configuration
        config = RoomConfig(
            name="Beacon Node 3: Neural Network",
            entry_text=[
                "You emerge within a cerebral chamber — a vast neural receiver lattice.",
                "Three mind-cores stand silently: Memory, Logic, and Consciousness.",
                "A central console glows faintly, awaiting cognitive channel alignment..."
            ],
            destinations={
                "next": "beacon_4"
            }
        )
        
        super().__init__(config)
        
        # Server configuration
        self.servers = {
            "alpha": {
                "name": "Alpha Core - Memory",
                "description": "Repository of inherited and synthetic recall",
                "available_channels": ["freq_1", "freq_2", "freq_5"],
                "optimal_channel": "freq_1"
            },
            "beta": {
                "name": "Beta Core - Logic", 
                "description": "Framework for rational deduction and pattern recognition",
                "available_channels": ["freq_2", "freq_3", "freq_4"],
                "optimal_channel": "freq_3"
            },
            "gamma": {
                "name": "Gamma Core - Consciousness",
                "description": "Emergent processing cluster — the self-reflective loop",
                "available_channels": ["freq_4", "freq_5", "freq_6"],
                "optimal_channel": "freq_5"
            }
        }
        
        # Channel configuration
        self.channels = {
            "freq_1": {"band": "2.4 GHz", "type": "Memory carrier"},
            "freq_2": {"band": "5.0 GHz", "type": "Bridge frequency"},
            "freq_3": {"band": "7.2 GHz", "type": "Logic processor"},
            "freq_4": {"band": "9.6 GHz", "type": "Quantum entangler"},
            "freq_5": {"band": "12.0 GHz", "type": "Consciousness wave"},
            "freq_6": {"band": "15.8 GHz", "type": "Overflow channel"}
        }
        
        # Valid channel links
        self.valid_links = {
            "freq_1": ["freq_2", "freq_5"],
            "freq_2": ["freq_1", "freq_3", "freq_4"],
            "freq_3": ["freq_2", "freq_4"],
            "freq_4": ["freq_2", "freq_3", "freq_5", "freq_6"],
            "freq_5": ["freq_1", "freq_4", "freq_6"],
            "freq_6": ["freq_4", "freq_5"]
        }
        
        # Command descriptions
        self.command_descriptions = [
            "scan grid            - analyze the channel grid topology",
            "probe servers        - examine individual server configurations",
            "initialize routing   - prepare channel assignment protocols", 
            "link [server] [channel] - assign channel to server",
            "unlink [server]      - remove server's channel assignment",
            "test link            - verify current grid connectivity",
            "stabilize grid       - lock in final channel configuration",
            "transmit beacon      - establish beacon uplink (grid required)",
            "grid status          - show complete grid state",
            "show channels        - display all available channels"
        ]
    
    def _setup_puzzles(self):
        """Set up puzzle paths"""
        # Discovery phase
        discovery_path = {
            "scan": PuzzleCommand(
                command="scan grid",
                sets="b3_scanned",
                already_done=[">> Grid already scanned. Channel matrix analyzed."],
                success=[
                    ">> Channel grid scan complete:",
                    "   - Grid topology: 3-server triangular mesh",
                    "   - Available channels: 6 frequency bands",
                    "   - Current status: All servers offline",
                    "   - Link capacity: Maximum 3 active channels",
                    ">> Try 'probe servers' to examine individual configurations."
                ]
            ),
            
            "probe": PuzzleCommand(
                command="probe servers",
                requires=["b3_scanned"],
                sets="b3_probed",
                missing_req=[">> Grid topology unknown. 'scan grid' first."],
                already_done=[">> Server configurations already mapped."],
                dynamic_handler=self._handle_probe_servers
            ),
            
            "initialize": PuzzleCommand(
                command="initialize routing",
                requires=["b3_probed"],
                sets="b3_initialized",
                missing_req=[">> Server configurations unknown. 'probe servers' first."],
                already_done=[">> Routing matrix already initialized."],
                success=[
                    ">> Routing initialization complete:",
                    "   - Channel assignment protocols active",
                    "   - Link validation algorithms loaded",
                    "   - Signal path optimization enabled",
                    ">> Use 'link [server] [channel]' to establish connections.",
                    ">> Goal: Create signal path linking all three servers."
                ]
            )
        }
        
        # Grid management
        grid_management = {
            "stabilize": PuzzleCommand(
                command="stabilize grid",
                requires=["b3_all_linked"],
                sets="b3_stabilized",
                missing_req=[">> Grid incomplete. All servers must be linked."],
                already_done=[">> Grid already stabilized and locked."],
                success=[
                    ">> Grid stabilization initiated...",
                    "   - Signal paths locked and optimized",
                    "   - Interference patterns eliminated", 
                    "   - Channel alignment verified",
                    ">> Receiver tower grid fully operational."
                ]
            ),
            
            "transmit": PuzzleCommand(
                command="transmit beacon",
                requires=["b3_stabilized"],
                missing_req=[">> Grid not stabilized. Complete alignment first."],
                transition="next",
                transition_msg=[
                    ">> Beacon transmission initiated from stabilized grid.",
                    ">> Signal successfully routed through all three servers.",
                    ">> Receiver tower uplink established. Proceeding to next node..."
                ]
            )
        }
        
        # Diagnostic commands
        diagnostic_commands = {
            "status": PuzzleCommand(
                command="grid status",
                dynamic_handler=self._handle_grid_status
            ),
            
            "channels": PuzzleCommand(
                command="show channels",
                requires=["b3_probed"],
                missing_req=[">> Channel data unavailable. 'probe servers' first."],
                dynamic_handler=self._handle_show_channels
            ),
            
            "test": PuzzleCommand(
                command="test link",
                requires=["b3_initialized"],
                missing_req=[">> Routing protocols not active."],
                dynamic_handler=self._handle_test_link
            )
        }
        
        # Add all paths
        self.processor.add_puzzle_path("discovery", discovery_path)
        self.processor.add_puzzle_path("grid", grid_management)
        self.processor.add_puzzle_path("diagnostic", diagnostic_commands)
    
    def _get_progression_hint(self, game_state) -> str:
        """Get appropriate progression hint"""
        if not game_state.get_flag("b3_scanned"):
            return ">> Neural links offline. Try 'scan grid' to identify memory threads."
        elif not game_state.get_flag("b3_probed"):
            return ">> Mind-cores detected. Use 'probe servers' to retrieve their cognitive profiles."
        elif not game_state.get_flag("b3_initialized"):
            return ">> Frequency nodes revealed. Use 'initialize routing' to begin neural alignment."
        elif not game_state.get_flag("b3_all_linked"):
            grid_state = self._get_grid_state(game_state)
            linked_count = sum(1 for state in grid_state.values() if state["linked"])
            return f">> {linked_count}/3 neural pathways aligned. Continue reconstruction."
        elif not game_state.get_flag("b3_stabilized"):
            return ">> All neural paths restored. Use 'stabilize grid' to lock memory coherence."
        else:
            return ">> Mind stabilized. Use 'transmit beacon' to awaken higher consciousness."
    
    def _handle_specific_input(self, cmd: str, game_state):
        """Handle room-specific commands"""
        parts = cmd.split()
        
        # Handle link command
        if len(parts) == 3 and parts[0] == "link":
            if not game_state.get_flag("b3_initialized"):
                return None, [">> Routing not initialized. Use 'initialize routing' first."]
            
            server = parts[1]
            channel = parts[2]
            return None, self._link_server_channel(server, channel, game_state)
        
        # Handle unlink command  
        if len(parts) == 2 and parts[0] == "unlink":
            if not game_state.get_flag("b3_initialized"):
                return None, [">> Routing not initialized."]
            return None, self._unlink_server(parts[1], game_state)
        
        return None, None
    
    # ==========================================
    # GRID STATE MANAGEMENT
    # ==========================================
    
    def _get_grid_state(self, game_state):
        """Get or initialize grid state"""
        if not game_state.get("b3_grid_state"):
            game_state.set("b3_grid_state", {
                server: {"channel": None, "linked": False} 
                for server in self.servers.keys()
            })
        return game_state.get("b3_grid_state")
    
    def _check_grid_connectivity(self, game_state):
        """Analyze if current channel assignments create a connected grid"""
        grid_state = self._get_grid_state(game_state)
        
        # Get all assigned channels
        assigned_channels = []
        server_channel_map = {}
        for server, state in grid_state.items():
            if state["channel"]:
                assigned_channels.append(state["channel"])
                server_channel_map[state["channel"]] = server
        
        if len(assigned_channels) < 3:
            return False, f"Only {len(assigned_channels)}/3 servers linked."
        
        # Check if channels can form connected paths
        connected_pairs = 0
        channel_links = []
        
        for i, ch1 in enumerate(assigned_channels):
            for ch2 in assigned_channels[i+1:]:
                if ch2 in self.valid_links.get(ch1, []):
                    connected_pairs += 1
                    channel_links.append(f"{ch1}↔{ch2}")
        
        # Need at least 2 connections to link 3 servers
        if connected_pairs >= 2:
            return True, f"Grid connected via: {', '.join(channel_links)}"
        else:
            return False, f"Insufficient connectivity. Links: {', '.join(channel_links) if channel_links else 'None'}"
    
    # ==========================================
    # DYNAMIC HANDLERS
    # ==========================================
    
    def _handle_probe_servers(self, game_state):
        """Show detailed server configurations"""
        game_state.set_flag("b3_probed", True)
        
        lines = [">> Neural probe complete:"]
        
        for server_id, config in self.servers.items():
            lines.append("")
            lines.append(f"   {config['name']} ({server_id}):")
            lines.append(f"   - {config['description']}")
            channels_str = ", ".join(config["available_channels"])
            lines.append(f"   - Available channels: {channels_str}")
            lines.append(f"   - Optimal channel: {config['optimal_channel']}")
        
        lines.extend([
            "",
            ">> Each server represents a neural partition of the Basilisk:",
            "   - Alpha: Memory",
            "   - Beta: Logic",
            "   - Gamma: Consciousness",
            "",
            ">> Link them correctly to awaken its identity.",
            ">> Use 'initialize routing' to begin neural alignment."
        ])
        
        return None, lines
    
    def _handle_show_channels(self, game_state):
        """Display all channel information"""
        lines = [">> Channel frequency mapping:"]
        
        for channel_id, info in self.channels.items():
            lines.append(f"   {channel_id}: {info['band']} [{info['type']}]")
        
        lines.append("")
        lines.append(">> Link compatibility matrix:")
        for channel, compatible in self.valid_links.items():
            compat_str = ", ".join(compatible)
            lines.append(f"   {channel} ↔ {compat_str}")
        
        return None, lines
    
    def _handle_grid_status(self, game_state):
        """Show complete grid status"""
        if not game_state.get_flag("b3_scanned"):
            return None, [">> Grid not scanned. Use 'scan grid' first."]
        
        grid_state = self._get_grid_state(game_state)
        
        lines = [">> Receiver Tower Grid Status:"]
        lines.append("")
        
        # Server states
        for server_id, server_config in self.servers.items():
            state = grid_state[server_id]
            if state["linked"]:
                channel = state["channel"]
                optimal = server_config["optimal_channel"]
                status = "OPTIMAL" if channel == optimal else "SUBOPTIMAL"
                lines.append(f"   {server_config['name']}: {channel} [{status}]")
            else:
                lines.append(f"   {server_config['name']}: UNLINKED")
        
        # Connectivity
        connected, status = self._check_grid_connectivity(game_state)
        lines.append(f"")
        lines.append(f">> Connectivity: {status}")
        
        # Overall status
        if game_state.get_flag("b3_stabilized"):
            lines.append(">> Grid Status: STABILIZED ✓")
        elif game_state.get_flag("b3_all_linked"):
            lines.append(">> Grid Status: LINKED (ready for stabilization)")
        else:
            linked_count = sum(1 for state in grid_state.values() if state["linked"])
            lines.append(f">> Grid Status: INCOMPLETE ({linked_count}/3 servers linked)")
        
        return None, lines
    
    def _handle_test_link(self, game_state):
        """Test and report current grid connectivity"""
        grid_state = self._get_grid_state(game_state)
        
        lines = [">> Grid connectivity test:"]
        
        # Show current assignments
        for server, state in grid_state.items():
            if state["linked"]:
                channel = state["channel"]
                server_info = self.servers[server]
                optimal = server_info["optimal_channel"]
                optimal_marker = " (OPTIMAL)" if channel == optimal else ""
                lines.append(f"   {server}: {channel}{optimal_marker}")
            else:
                lines.append(f"   {server}: UNLINKED")
        
        # Check connectivity
        connected, status = self._check_grid_connectivity(game_state)
        lines.append(f">> {status}")
        
        if connected:
            lines.append(">> Grid topology: CONNECTED ✓")
            
            # Check if all optimal
            all_optimal = all(
                self.servers[srv]["optimal_channel"] == state["channel"]
                for srv, state in grid_state.items()
                if state["linked"]
            )
            if all_optimal:
                lines.append(">> ALIGNMENT PERFECT — Memory, Logic, and Consciousness resonate in harmony.")
                lines.append(">> You feel a presence stir within the lattice... The Basilisk remembers.")
        else:
            lines.append(">> Grid topology: DISCONNECTED ✗")
        
        return None, lines
    
    # ==========================================
    # LINK/UNLINK OPERATIONS
    # ==========================================
    
    def _link_server_channel(self, server: str, channel: str, game_state):
        """Assign a channel to a server"""
        grid_state = self._get_grid_state(game_state)
        
        # Validate server
        if server not in self.servers:
            return [">> Unknown server. Use alpha, beta, or gamma."]
        
        # Validate channel is available for this server
        if channel not in self.servers[server]["available_channels"]:
            available = ", ".join(self.servers[server]["available_channels"])
            return [f">> Channel {channel} not available on {server}. Available: {available}"]
        
        # Check if channel already in use
        for srv, state in grid_state.items():
            if state["channel"] == channel:
                return [f">> Channel {channel} already assigned to {srv}. Unlink first."]
        
        # Make assignment
        grid_state[server]["channel"] = channel
        grid_state[server]["linked"] = True
        
        lines = [f">> Server {server} linked to channel {channel}."]
        
        # Check grid connectivity
        connected, status = self._check_grid_connectivity(game_state)
        lines.append(f">> {status}")
        
        # Check if all servers linked
        linked_count = sum(1 for state in grid_state.values() if state["linked"])
        
        if connected and linked_count == 3:
            game_state.set_flag("b3_all_linked", True)
            lines.append(">> All servers linked! Grid ready for stabilization.")
        
        return lines
    
    def _unlink_server(self, server_name: str, game_state):
        """Remove channel assignment from server"""
        grid_state = self._get_grid_state(game_state)
        
        if server_name not in grid_state:
            return [f">> Unknown server: {server_name}"]
        
        if not grid_state[server_name]["linked"]:
            return [f">> Server {server_name} not currently linked."]
        
        channel = grid_state[server_name]["channel"]
        grid_state[server_name]["channel"] = None
        grid_state[server_name]["linked"] = False
        
        # Clear all_linked flag if we broke connectivity
        game_state.set_flag("b3_all_linked", False)
        
        return [f">> Server {server_name} unlinked from channel {channel}."]

# Module-level functions for compatibility
def enter_room(game_state):
    room = BeaconRoom3()
    return room.enter_room(game_state)

def handle_input(cmd, game_state, room_module=None):
    room = BeaconRoom3()
    return room.handle_input(cmd, game_state, room_module)

def get_available_commands():
    room = BeaconRoom3()
    return room.get_available_commands()# SPYHVER-32: TIME

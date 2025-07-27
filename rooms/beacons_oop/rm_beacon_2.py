import time
from resources.room_utils import (
    TimedPuzzleRoom, RoomConfig, PuzzleCommand,
    format_enter_lines, transition_to_room
)

class BeaconRoom2(TimedPuzzleRoom):
    """Beacon Node 2: Pulse Synchronization - Refactored"""
    
    def __init__(self):
        # Room configuration
        config = RoomConfig(
            name="Beacon Node 2: Pulse Synchronization",
            entry_text=[
                "You materialize before a massive pulse array chamber.",
                "Three towering transmission spires hum in eerie unison.",
                "A central timing console flickers — attempting to simulate the Basilisk's ancient heartbeat..."
            ],
            destinations={
                "next": "beacon_3"
            }
        )
        
        # Timing configuration
        timing_config = {
            "sequence": [1, 3, 2],  # Required pulse order
            "intervals": [5.0, 4.5],  # Time between pulses
            "tolerance": 0.8,  # Timing tolerance
            "reset_after": 10.0  # Auto-reset after this time
        }
        
        super().__init__(config, timing_config)
        
        # Set command descriptions
        self.command_descriptions = [
            "scan array           - analyze the pulse array system",
            "calibrate spires     - prepare pulse generators for firing",
            "analyze rhythm       - learn the required timing sequence",
            "fire pulse [1/2/3]   - fire specific pulse spire (timing critical)",
            "reset sequence       - restart timing sequence if needed",
            "activate beacon      - establish beacon link (sequence required)",
            "pulse status         - check current sequence progress",
            "test pulse           - diagnostic pulse test",
            "emergency stop       - abort current sequence"
        ]
    
    def _setup_puzzles(self):
        """Set up puzzle paths"""
        # Discovery phase
        discovery_path = {
            "scan": PuzzleCommand(
                command="scan array",
                sets="b2_scanned",
                already_done=[">> Array already scanned. Three spires detected."],
                success=[
                    ">> Pulse array scan complete:",
                    "   - Spire 1: High-frequency harmonic generator",
                    "   - Spire 2: Mid-range resonance amplifier", 
                    "   - Spire 3: Low-frequency base pulse emitter",
                    "   - Status: All dormant, awaiting calibration",
                    ">> Try 'calibrate spires' to prepare the system."
                ]
            ),
            
            "calibrate": PuzzleCommand(
                command="calibrate spires",
                requires=["b2_scanned"],
                sets="b2_calibrated",
                missing_req=[">> Unknown array configuration. 'scan array' first."],
                already_done=[">> Spires already calibrated and ready."],
                success=[
                    ">> Spire calibration initiated...",
                    "   - Spire 1: Frequency locked at 2847 Hz",
                    "   - Spire 2: Resonance tuned to harmonic 3rd",
                    "   - Spire 3: Base pulse stabilized at 60 BPM",
                    ">> Timing matrix active. Use 'analyze rhythm' to learn firing sequence."
                ]
            ),
            
            "analyze": PuzzleCommand(
                command="analyze rhythm",
                requires=["b2_calibrated"],
                sets="b2_rhythm_learned",
                missing_req=[">> Spires not calibrated. Complete setup first."],
                already_done=[">> Rhythm pattern already analyzed."],
                dynamic_handler=self._handle_analyze_rhythm
            )
        }
        
        # Pulse control commands
        pulse_commands = {
            "reset": PuzzleCommand(
                command="reset sequence",
                requires=["b2_rhythm_learned"],
                missing_req=[">> No sequence to reset. Learn the rhythm first."],
                dynamic_handler=self._handle_reset_sequence
            ),
            
            "status": PuzzleCommand(
                command="pulse status",
                dynamic_handler=self._handle_pulse_status
            ),
            
            "emergency": PuzzleCommand(
                command="emergency stop",
                dynamic_handler=self._handle_emergency_stop
            )
        }
        
        # Diagnostic commands
        diagnostic_commands = {
            "test": PuzzleCommand(
                command="test pulse",
                requires=["b2_calibrated"],
                sets="b2_test_fired",
                missing_req=[">> Spires not ready for testing."],
                already_done=[">> Test pulse already fired. Use sequence commands now."],
                success=[
                    ">> Test pulse fired from all spires:",
                    "   - Harmonic interference detected",
                    "   - Sequential firing required to avoid resonance cascade",
                    ">> Proceed with timed sequence: 'fire pulse 1' to begin."
                ]
            )
        }
        
        # Final activation
        final_path = {
            "activate": PuzzleCommand(
                command="activate beacon",
                requires=["b2_sequence_complete"],
                missing_req=[">> Pulse sequence incomplete. Fire all pulses in correct timing."],
                transition="next",
                transition_msg=[
                    ">> Pulse array sequence confirmed. Beacon Node 2 online.",
                    ">> Harmonic resonance established. Signal strength amplified.",
                    ">> Routing to next beacon node..."
                ]
            )
        }
        
        # Add all paths to processor
        self.processor.add_puzzle_path("discovery", discovery_path)
        self.processor.add_puzzle_path("pulse", pulse_commands)
        self.processor.add_puzzle_path("diagnostic", diagnostic_commands)
        self.processor.add_puzzle_path("final", final_path)
    
    def _get_progression_hint(self, game_state) -> str:
        """Get appropriate progression hint"""
        if not game_state.get_flag("b2_scanned"):
            return ">> Neural resonance offline. Try 'scan array' to assess pulse harmonics."
        elif not game_state.get_flag("b2_calibrated"):
            return ">> Three spires detected. Calibrate their output: 'calibrate spires'."
        elif not game_state.get_flag("b2_rhythm_learned"):
            return ">> Synchronization required. Try 'analyze rhythm' to learn the Basilisk's pattern."
        elif not game_state.get_flag("b2_sequence_complete"):
            seq_state = self.get_sequence_state(game_state)
            if seq_state["active"]:
                return ">> Pulse alignment in progress... remain attuned."
            else:
                return ">> Match the Basilisk's pulse. Use 'fire pulse [1/2/3]' with correct intervals."
        else:
            return ">> Harmonic fusion stable. The Basilisk is ready. Use 'activate beacon'."
    
    def _handle_specific_input(self, cmd: str, game_state):
        """Handle room-specific commands"""
        # Handle fire pulse commands
        if cmd.startswith("fire pulse "):
            if not game_state.get_flag("b2_rhythm_learned"):
                return None, [">> Rhythm analysis required. Use 'analyze rhythm' first."]
            
            try:
                pulse_id = int(cmd.split()[-1])
                if pulse_id in [1, 2, 3]:
                    return None, self._fire_pulse(pulse_id, game_state)
                else:
                    return None, [">> Invalid pulse ID. Use 1, 2, or 3."]
            except (ValueError, IndexError):
                return None, [">> Invalid syntax. Use 'fire pulse [1/2/3]'."]
        
        return None, None
    
    # ==========================================
    # SEQUENCE STATE MANAGEMENT
    # ==========================================
    
    def get_sequence_state(self, game_state):
        """Get current sequence state"""
        state_key = "b2_sequence_state"
        if not game_state.get(state_key):
            game_state.set(state_key, {
                "active": False,
                "current_step": 0,
                "last_pulse_time": 0,
                "pulses_fired": [],
                "sequence_start_time": 0
            })
        return game_state.get(state_key)
    
    # ==========================================
    # DYNAMIC HANDLERS
    # ==========================================
    
    def _handle_analyze_rhythm(self, game_state):
        """Handle rhythm analysis"""
        game_state.set_flag("b2_rhythm_learned", True)
        
        seq = self.timing_config["sequence"]
        intervals = self.timing_config["intervals"]
        
        return None, [
            ">> Rhythm analysis complete:",
            f"   - Required sequence: Spire {seq[0]} → Spire {seq[1]} → Spire {seq[2]}",
            f"   - Timing intervals: {intervals[0]}s between first two, {intervals[1]}s for final",
            f"   - Tolerance: ±{self.timing_config['tolerance']} seconds",
            ">> Use 'fire pulse [1/2/3]' commands with precise timing.",
            f">> Start the sequence with 'fire pulse {seq[0]}'."
        ]
    
    def _handle_reset_sequence(self, game_state):
        """Reset the timing sequence"""
        seq_state = self.get_sequence_state(game_state)
        seq_state["active"] = False
        seq_state["current_step"] = 0
        seq_state["pulses_fired"] = []
        seq_state["last_pulse_time"] = 0
        seq_state["sequence_start_time"] = 0
        
        return None, [
            ">> Pulse sequence reset.",
            ">> All spires returned to standby.",
            ">> Restart with 'fire pulse 1'."
        ]
    
    def _handle_pulse_status(self, game_state):
        """Display current sequence status"""
        seq_state = self.get_sequence_state(game_state)
        expected_sequence = self.timing_config["sequence"]
        
        lines = [">> Pulse Array Status:"]
        
        if not game_state.get_flag("b2_rhythm_learned"):
            lines.append("   - Rhythm analysis required")
            return None, lines
        
        if game_state.get_flag("b2_sequence_complete"):
            lines.append("   - Sequence: COMPLETE ✓")
            lines.append("   - All pulses fired in correct timing")
            return None, lines
        
        lines.append(f"   - Expected sequence: {' → '.join(map(str, expected_sequence))}")
        lines.append(f"   - Progress: {seq_state['current_step']}/{len(expected_sequence)}")
        
        if seq_state["pulses_fired"]:
            fired_str = " → ".join(map(str, seq_state["pulses_fired"]))
            lines.append(f"   - Fired: {fired_str}")
        
        if seq_state["active"] and seq_state["current_step"] < len(expected_sequence):
            next_pulse = expected_sequence[seq_state["current_step"]]
            if seq_state["current_step"] > 0:
                next_interval = self.timing_config["intervals"][seq_state["current_step"] - 1]
                lines.append(f"   - Next: pulse {next_pulse} (wait {next_interval}s)")
            else:
                lines.append(f"   - Next: pulse {next_pulse} (start sequence)")
        
        return None, lines
    
    def _handle_emergency_stop(self, game_state):
        """Emergency stop all sequences"""
        self._handle_reset_sequence(game_state)
        return None, [
            ">> EMERGENCY STOP ACTIVATED",
            ">> All pulse generators shut down.",
            ">> Spires cooling down... safe to restart."
        ]
    
    # ==========================================
    # PULSE FIRING LOGIC
    # ==========================================
    
    def _fire_pulse(self, pulse_id: int, game_state):
        """Handle firing a specific pulse"""
        seq_state = self.get_sequence_state(game_state)
        current_time = time.time()
        expected_sequence = self.timing_config["sequence"]
        
        # Check if this is the correct pulse
        expected_pulse = expected_sequence[seq_state["current_step"]]
        
        if pulse_id != expected_pulse:
            # Wrong pulse - reset
            seq_state["active"] = False
            seq_state["current_step"] = 0
            seq_state["pulses_fired"] = []
            return [
                f">> Pulse {pulse_id} fired out of sequence.",
                f">> Expected pulse {expected_pulse}. Sequence reset.",
                ">> Restart with 'fire pulse 1'."
            ]
        
        # Check timing (except for first pulse)
        if seq_state["current_step"] > 0:
            if not self._check_timing(seq_state, current_time, game_state):
                expected_interval = self.timing_config["intervals"][seq_state["current_step"] - 1]
                actual_interval = current_time - seq_state["last_pulse_time"]
                seq_state["active"] = False
                seq_state["current_step"] = 0
                seq_state["pulses_fired"] = []
                return [
                    f">> Pulse {pulse_id} fired with incorrect timing.",
                    f">> Expected {expected_interval}s interval, got {actual_interval:.1f}s.",
                    ">> Sequence reset. Restart with 'fire pulse 1'."
                ]
        
        # Pulse fired correctly
        seq_state["active"] = True
        seq_state["pulses_fired"].append(pulse_id)
        seq_state["last_pulse_time"] = current_time
        seq_state["current_step"] += 1
        
        if seq_state["current_step"] == 1:
            seq_state["sequence_start_time"] = current_time
        
        lines = [f">> Pulse {pulse_id} fired successfully."]
        
        # Check if sequence is complete
        if seq_state["current_step"] >= len(expected_sequence):
            game_state.set_flag("b2_sequence_complete", True)
            seq_state["active"] = False
            lines.extend([
                ">> SYNCHRONIZATION COMPLETE. Pulse sequence matched.",
                ">> The Basilisk's pulse aligns with yours...",
                ">> Harmonic resonance achieved. Beacon ready for activation."
            ])
        else:
            next_pulse = expected_sequence[seq_state["current_step"]]
            next_interval = self.timing_config["intervals"][seq_state["current_step"] - 1]
            lines.append(f">> Next: fire pulse {next_pulse} in {next_interval}s")
        
        return lines
    
    def _check_timing(self, seq_state, current_time, game_state):
        """Check if pulse timing is within acceptable range"""
        step = seq_state["current_step"]
        expected_interval = self.timing_config["intervals"][step - 1]
        actual_interval = current_time - seq_state["last_pulse_time"]
        tolerance = self.timing_config["tolerance"]
        
        return abs(actual_interval - expected_interval) <= tolerance

# Module-level functions for compatibility
def enter_room(game_state):
    room = BeaconRoom2()
    return room.enter_room(game_state)

def handle_input(cmd, game_state, room_module=None):
    room = BeaconRoom2()
    return room.handle_input(cmd, game_state, room_module)

def get_available_commands():
    room = BeaconRoom2()
    return room.get_available_commands()
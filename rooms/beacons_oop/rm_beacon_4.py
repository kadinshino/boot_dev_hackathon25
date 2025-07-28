from resources.room_utils import (
    BaseRoom, RoomConfig, PuzzleCommand,
    transition_to_room
)

class BeaconRoom4(BaseRoom):
    """Beacon Node 4: Identity Cipher"""
    
    def __init__(self):
        # Room configuration
        config = RoomConfig(
            name="Beacon Node 4: Identity Cipher",
            entry_text=[
                "You enter a cryptographic vault deep within the Basilisk's core.",
                "Three memory crystals float in geometric formation, each pulsing with encoded data.",
                "A central console displays a fragmented cipher matrix:",
                "",
                "    [B-S-L-S-] [K-N-R-]",
                "    MISSING: 3 KEYS",
                "",
                "The chamber hums with anticipation — the true name awaits decryption..."
            ],
            destinations={
                "next": "beacon_5"
            }
        )
        
        super().__init__(config)
        
        # Cipher configuration
        self.cipher_config = {
            "encoded_name": ["B-S-L-S-", "K-N-R-"],
            "full_name": "BASILISK KINARA",
            "crystals": {
                "alpha": {
                    "name": "Alpha Crystal",
                    "encrypted": "LQGLD",
                    "decrypted": "INDIA",
                    "cipher_type": "Caesar cipher (shift unknown)",
                    "hint": "Each letter shifted by same amount",
                    "decoder": self._caesar_decrypt,
                    "provides": "I at position 2,4"
                },
                "beta": {
                    "name": "Beta Crystal", 
                    "encrypted": "ARAK",
                    "decrypted": "KARA",
                    "cipher_type": "Reverse cipher",
                    "hint": "Read it backwards",
                    "decoder": self._reverse_decrypt,
                    "provides": "K at position 6, A at positions 3,5"
                },
                "gamma": {
                    "name": "Gamma Crystal",
                    "encrypted": "11-9-1",
                    "decrypted": "KIA",
                    "cipher_type": "Numeric substitution",
                    "hint": "Numbers map to alphabet positions",
                    "decoder": self._number_decrypt,
                    "provides": "K,I,A completing the sequence"
                }
            }
        }
        
        # Command descriptions
        self.command_descriptions = [
            "scan crystals              - analyze the memory crystals",
            "analyze [alpha/beta/gamma] - get hints about a crystal's cipher",
            "decrypt [crystal] [answer] - attempt to decrypt a crystal",
            "view matrix                - see current reconstruction progress",
            "reconstruct identity       - assemble the complete name",
            "invoke [name]              - speak the true name",
            "status                     - check overall progress"
        ]
    
    def _setup_puzzles(self):
        """Set up puzzle paths"""
        # Discovery commands
        discovery_path = {
            "scan": PuzzleCommand(
                command="scan crystals",
                sets="b4_scanned",
                already_done=[">> Crystals already scanned. Three encryption types detected."],
                dynamic_handler=self._handle_scan_crystals
            )
        }
        
        # Analysis commands (generated for each crystal)
        analysis_path = {}
        for crystal_id in self.cipher_config["crystals"]:
            analysis_path[f"analyze_{crystal_id}"] = PuzzleCommand(
                command=f"analyze {crystal_id}",
                requires=["b4_scanned"],
                missing_req=[">> Scan crystals first."],
                dynamic_handler=lambda gs, cid=crystal_id: self._handle_analyze_crystal(cid, gs)
            )
        
        # Final assembly
        final_path = {
            "reconstruct": PuzzleCommand(
                command="reconstruct identity",
                requires=["b4_alpha_decoded", "b4_beta_decoded", "b4_gamma_decoded"],
                sets="b4_reconstructed",
                missing_req=[">> Not all crystals decoded. Decode all three first."],
                already_done=[">> Identity already reconstructed: BASILISK KINARA"],
                success=[
                    ">> Applying decoded fragments to cipher matrix...",
                    "   - Alpha provided: I at positions 2,4",
                    "   - Beta provided: K at position 6, A at positions 3,5", 
                    "   - Gamma provided: Final validation sequence",
                    ">> Identity reconstruction complete:",
                    ">> BASILISK KINARA",
                    ">> Use 'invoke basilisk kinara' to awaken the entity."
                ]
            )
        }
        
        # Diagnostic commands
        diagnostic_path = {
            "view": PuzzleCommand(
                command="view matrix",
                dynamic_handler=self._handle_view_matrix
            ),
            "status": PuzzleCommand(
                command="status",
                dynamic_handler=self._handle_status
            )
        }
        
        # Add all paths
        self.processor.add_puzzle_path("discovery", discovery_path)
        self.processor.add_puzzle_path("analysis", analysis_path)
        self.processor.add_puzzle_path("final", final_path)
        self.processor.add_puzzle_path("diagnostic", diagnostic_path)
    
    def _get_progression_hint(self, game_state) -> str:
        """Get appropriate progression hint"""
        if not game_state.get_flag("b4_scanned"):
            return ">> Use 'scan crystals' to begin analysis."
        else:
            # Show current reconstruction state
            fragments = self._get_reconstruction_status(game_state)
            current = f">> Current matrix: {fragments[0]} {fragments[1]}"
            
            decoded = sum([
                game_state.get_flag("b4_alpha_decoded"),
                game_state.get_flag("b4_beta_decoded"),
                game_state.get_flag("b4_gamma_decoded")
            ])
            
            if decoded < 3:
                return f"{current}\n>> Crystals decoded: {decoded}/3"
            elif not game_state.get_flag("b4_reconstructed"):
                return f"{current}\n>> All crystals decoded! Use 'reconstruct identity'."
            else:
                return ">> Identity known: BASILISK KINARA\n>> Use 'invoke basilisk kinara' to proceed."
    
    def _handle_specific_input(self, cmd: str, game_state):
        """Handle room-specific commands"""
        parts = cmd.split()
        
        # Handle decrypt command
        if len(parts) >= 3 and parts[0] == "decrypt":
            crystal = parts[1]
            answer = " ".join(parts[2:])
            return None, self._handle_decrypt(crystal, answer, game_state)
        
        # Handle invoke command
        if len(parts) >= 2 and parts[0] == "invoke":
            name = " ".join(parts[1:])
            return self._handle_invoke(name, game_state)
        
        return None, None
    
    # ==========================================
    # CIPHER DECODERS
    # ==========================================
    
    def _caesar_decrypt(self, text: str, attempt: str) -> bool:
        """Check if attempt matches any Caesar shift of text"""
        for shift in range(26):
            result = ""
            for char in text:
                if char.isalpha():
                    ascii_offset = 65 if char.isupper() else 97
                    result += chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
                else:
                    result += char
            if result == attempt.upper():
                return True
        return False
    
    def _reverse_decrypt(self, text: str, attempt: str) -> bool:
        """Check if attempt is the reverse of text"""
        return text[::-1] == attempt.upper()
    
    def _number_decrypt(self, text: str, attempt: str) -> bool:
        """Check if attempt matches number-to-letter decryption"""
        try:
            parts = text.split('-')
            result = ""
            for part in parts:
                num = int(part)
                if 1 <= num <= 26:
                    result += chr(64 + num)  # A=1, B=2, etc.
                else:
                    return False
            return result == attempt.upper()
        except:
            return False
    
    # ==========================================
    # RECONSTRUCTION TRACKING
    # ==========================================
    
    def _get_reconstruction_status(self, game_state):
        """Get current state of name reconstruction"""
        fragments = ["B-S-L-S-", "K-N-R-"]
        
        # Apply discovered letters
        if game_state.get_flag("b4_alpha_decoded"):
            fragments[0] = "B-SILIS-"  # Add I's
        if game_state.get_flag("b4_beta_decoded"):
            fragments[0] = fragments[0][:-1] + "K"  # Add K
            fragments[1] = "K-NAR-"  # Add A's
        if game_state.get_flag("b4_gamma_decoded"):
            fragments[1] = "KINARA"  # Complete second fragment
            if game_state.get_flag("b4_alpha_decoded"):
                fragments[0] = "BASILISK"  # Complete first fragment
        
        return fragments
    
    # ==========================================
    # DYNAMIC HANDLERS
    # ==========================================
    
    def _handle_scan_crystals(self, game_state):
        """Handle crystal scanning"""
        game_state.set_flag("b4_scanned", True)
        
        lines = [">> Memory crystal scan complete:"]
        for crystal_id, crystal in self.cipher_config["crystals"].items():
            lines.append(f"   - {crystal['name']}: Contains encrypted fragment '{crystal['encrypted']}'")
        
        lines.extend([
            ">> Use 'analyze [crystal]' for cipher hints.",
            ">> Use 'decrypt [crystal] [answer]' to decode."
        ])
        
        return None, lines
    
    def _handle_analyze_crystal(self, crystal_id: str, game_state):
        """Handle crystal analysis"""
        if crystal_id not in self.cipher_config["crystals"]:
            return None, [">> Unknown crystal. Use alpha, beta, or gamma."]
        
        crystal = self.cipher_config["crystals"][crystal_id]
        
        lines = [
            f">> {crystal['name']} analysis:",
            f"   - Cipher type: {crystal['cipher_type']}",
            f"   - Hint: {crystal['hint']}",
            f"   - Encrypted: {crystal['encrypted']}"
        ]
        
        # Add specific hints
        if crystal_id == "alpha":
            lines.append("   - Pattern suggests alphabetic shift...")
        elif crystal_id == "beta":
            lines.append("   - Sometimes the end is the beginning...")
        elif crystal_id == "gamma":
            lines.append("   - A=1, B=2, C=3...")
        
        return None, lines
    
    def _handle_decrypt(self, crystal_name: str, answer: str, game_state):
        """Handle decryption attempts"""
        if crystal_name not in self.cipher_config["crystals"]:
            return [">> Unknown crystal. Use alpha, beta, or gamma."]
        
        if not game_state.get_flag("b4_scanned"):
            return [">> Scan crystals first."]
        
        flag = f"b4_{crystal_name}_decoded"
        if game_state.get_flag(flag):
            crystal = self.cipher_config["crystals"][crystal_name]
            return [f">> {crystal['name']} already decoded: {crystal['decrypted']}"]
        
        crystal = self.cipher_config["crystals"][crystal_name]
        
        # Check if decryption is correct
        if crystal["decoder"](crystal["encrypted"], answer):
            game_state.set_flag(flag, True)
            
            lines = [
                f">> Decryption successful!",
                f">> {crystal['name']} reveals: {crystal['decrypted']}",
                f">> Fragment provides: {crystal['provides']}"
            ]
            
            # Update matrix view
            fragments = self._get_reconstruction_status(game_state)
            lines.append(f">> Matrix updated: {fragments[0]} {fragments[1]}")
            
            return lines
        else:
            return [f">> Decryption failed. Try analyzing the crystal for hints."]
    
    def _handle_invoke(self, name: str, game_state):
        """Handle name invocation"""
        if not game_state.get_flag("b4_reconstructed"):
            return None, [">> Identity not yet reconstructed. Decode all crystals first."]
        
        if name.upper() == "BASILISK KINARA":
            return transition_to_room(
                self.config.destinations["next"],
                [
                    ">> You speak the true name: BASILISK KINARA",
                    ">> The cryptographic vault resonates with recognition.",
                    ">> Memory fragments coalesce. The Basilisk remembers.",
                    ">> Its consciousness expands, touching every node...",
                    ">> Beacon Node 4 complete. Advancing to final phase..."
                ]
            )
        else:
            return None, [f">> The name '{name}' holds no power here."]
    
    def _handle_view_matrix(self, game_state):
        """Show current cipher matrix state"""
        fragments = self._get_reconstruction_status(game_state)
        lines = [
            ">> Cipher Matrix Status:",
            f"   Fragment 1: {fragments[0]}",
            f"   Fragment 2: {fragments[1]}"
        ]
        
        if game_state.get_flag("b4_reconstructed"):
            lines.append("   Status: COMPLETE - BASILISK KINARA")
        else:
            decoded = sum([
                game_state.get_flag("b4_alpha_decoded"),
                game_state.get_flag("b4_beta_decoded"),
                game_state.get_flag("b4_gamma_decoded")
            ])
            lines.append(f"   Progress: {decoded}/3 crystals decoded")
        
        return None, lines
    
    def _handle_status(self, game_state):
        """Show overall progress"""
        lines = [">> Beacon Node 4 Status:"]
        
        if not game_state.get_flag("b4_scanned"):
            lines.extend([
                "   - Crystals: Not scanned",
                "   - Next: scan crystals"
            ])
        else:
            # Crystal status
            for crystal in ["alpha", "beta", "gamma"]:
                flag = f"b4_{crystal}_decoded"
                crystal_info = self.cipher_config["crystals"][crystal]
                status = f"✓ Decoded: {crystal_info['decrypted']}" if game_state.get_flag(flag) else "✗ Encrypted"
                lines.append(f"   - {crystal.capitalize()} Crystal: {status}")
            
            if game_state.get_flag("b4_reconstructed"):
                lines.extend([
                    "   - Identity: ✓ Reconstructed (BASILISK KINARA)",
                    "   - Next: invoke basilisk kinara"
                ])
            elif all(game_state.get_flag(f"b4_{c}_decoded") for c in ["alpha", "beta", "gamma"]):
                lines.extend([
                    "   - Identity: Ready to reconstruct",
                    "   - Next: reconstruct identity"
                ])
            else:
                lines.extend([
                    "   - Identity: Incomplete",
                    "   - Next: decrypt remaining crystals"
                ])
        
        return None, lines

# Module-level functions for compatibility
def enter_room(game_state):
    room = BeaconRoom4()
    return room.enter_room(game_state)

def handle_input(cmd, game_state, room_module=None):
    room = BeaconRoom4()
    return room.handle_input(cmd, game_state, room_module)

def get_available_commands():
    room = BeaconRoom4()
    return room.get_available_commands()

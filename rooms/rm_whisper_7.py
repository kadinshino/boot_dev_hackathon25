from resources.room_utils import format_enter_lines, standard_commands, transition_to_room

# ============================================================================
# CONSTANTS
# ============================================================================

STAGE_FLAGS = [
    "awakening_scanned",
    "awakening_sequence_verified",
    "awakening_memory_synced",
    "awakening_logic_resolved",
    "awakening_exit_unlocked"
]

FRAGMENT_CODES = {
    "alpha": "R3AL1TY_",
    "beta": "AW41TS_",
    "gamma": "Y0U"
}

EXPECTED_SEQUENCE = ["inject uplink", "verify keychain", "compile logic", "unlock threshold"]

# ============================================================================
# ROOM CORE
# ============================================================================

def enter_room(game_state):
    lines = [
        "You awaken inside a fractal logic core.",
        "Consciousness flickers as data from all previous nodes floods your senses.",
        "Voices echo from the past... all paths, all errors, all truths—converging here."
    ]

    if not game_state.get_flag("awakening_scanned"):
        lines.append("")
        lines.append(">> Data stream unstable. Try 'scan core'.")
    elif not game_state.get_flag("awakening_sequence_verified"):
        lines.append(">> Begin uplink reconstruction. Use 'inject uplink'.")
    elif not game_state.get_flag("awakening_memory_synced"):
        lines.append(">> Memory key incomplete. Try 'verify keychain'.")
    elif not game_state.get_flag("awakening_logic_resolved"):
        lines.append(">> Logic structure unstable. Run 'compile logic'.")
    elif not game_state.get_flag("awakening_exit_unlocked"):
        lines.append(">> Final threshold locked. Use 'unlock threshold'.")
    else:
        lines.append(">> Conscious loop complete. Use 'awaken' to proceed...")

    return format_enter_lines("AWAKENING CORE", lines)

# ============================================================================
# INPUT HANDLER
# ============================================================================

def handle_input(cmd, game_state, room_module=None):
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response

    cmd = cmd.lower().strip()

    # STAGE 1: SCAN
    if cmd == "scan core":
        if game_state.get_flag("awakening_scanned"):
            return None, [">> Core already scanned."]
        game_state.set_flag("awakening_scanned", True)
        return None, [
            ">> Core structure recognized.",
            "   - Beacon fragments active",
            "   - Memory patterns detected",
            "   - Loop residue present",
            ">> Begin with 'inject uplink'."
        ]

    # STAGE 2: UPLINK
    if cmd == "inject uplink":
        if not game_state.get_flag("awakening_scanned"):
            return None, [">> Unstable core. Run 'scan core' first."]
        if game_state.get_flag("awakening_sequence_verified"):
            return None, [">> Uplink already injected."]
        game_state.set_flag("awakening_sequence_verified", True)
        return None, [
            ">> Uplink injection complete.",
            "   - Signal path restored",
            "   - Use 'verify keychain'"
        ]

    # STAGE 3: VERIFY MEMORY
    if cmd == "verify keychain":
        if not game_state.get_flag("awakening_sequence_verified"):
            return None, [">> Injection incomplete."]
        if game_state.get_flag("awakening_memory_synced"):
            return None, [">> Keychain already verified."]

        # Gather flags from beacon fragments
        alpha = game_state.get_flag("w2_alpha_decrypted")
        beta = game_state.get_flag("w2_beta_decrypted")
        gamma = game_state.get_flag("w2_gamma_decrypted")

        if not all([alpha, beta, gamma]):
            return None, [">> Keychain incomplete. Missing beacon fragments."]

        game_state.set_flag("awakening_memory_synced", True)
        return None, [
            ">> Memory key reconstructed:",
            f"   - {FRAGMENT_CODES['alpha']}{FRAGMENT_CODES['beta']}{FRAGMENT_CODES['gamma']}",
            ">> Keychain accepted. Proceed with 'compile logic'."
        ]

    # STAGE 4: COMPILE LOGIC
    if cmd == "compile logic":
        if not game_state.get_flag("awakening_memory_synced"):
            return None, [">> Memory key not yet validated."]
        if game_state.get_flag("awakening_logic_resolved"):
            return None, [">> Logic already compiled."]
        if not game_state.get_flag("loop_broken"):
            return None, [">> Residual loop detected. You must 'break loop' first in Loop Chamber."]

        game_state.set_flag("awakening_logic_resolved", True)
        return None, [
            ">> Logic matrix compiled successfully.",
            "   - Loop instability purged",
            "   - Signal integrity verified",
            ">> Final stage: 'unlock threshold'"
        ]

    # STAGE 5: EXIT UNLOCK
    if cmd == "unlock threshold":
        if not game_state.get_flag("awakening_logic_resolved"):
            return None, [">> Logic invalid. Compilation required."]
        if game_state.get_flag("awakening_exit_unlocked"):
            return None, [">> Threshold already unlocked."]
        game_state.set_flag("awakening_exit_unlocked", True)
        return None, [
            ">> Awakening threshold unlocked.",
            ">> Conscious stream stabilized."
        ]

    # FINAL
    if cmd == "awaken":
        if not game_state.get_flag("awakening_exit_unlocked"):
            return None, [">> Not ready. The threshold is still locked."]
        return transition_to_room("final_exit", [
            ">> You awaken.",
            ">> Memory aligned. Purpose recalibrated.",
            ">> You are now the anomaly...",
            ">> Preparing exit sequence..."
        ])

    # HIDDEN COMMAND: logic status
    if cmd == "logic status":
        stages = [
            f"Scan Core       - {'✔' if game_state.get_flag('awakening_scanned') else '✘'}",
            f"Inject Uplink   - {'✔' if game_state.get_flag('awakening_sequence_verified') else '✘'}",
            f"Verify Keychain - {'✔' if game_state.get_flag('awakening_memory_synced') else '✘'}",
            f"Compile Logic   - {'✔' if game_state.get_flag('awakening_logic_resolved') else '✘'}",
            f"Unlock Exit     - {'✔' if game_state.get_flag('awakening_exit_unlocked') else '✘'}"
        ]
        return None, [">> Awakening Progress:"] + stages

    return None, [">> Unknown command. Try 'logic status' or follow the awakening sequence."]

# ============================================================================
# AVAILABLE COMMANDS
# ============================================================================

def get_available_commands():
    return [
        "scan core          - analyze the awakening chamber",
        "inject uplink      - reconstruct your conscious signal",
        "verify keychain    - validate memory fragments from beacons",
        "compile logic      - build final logic tree (loop required)",
        "unlock threshold   - enable final exit",
        "awaken             - exit the logic core",
        "logic status       - (optional) check awakening progress"
    ]

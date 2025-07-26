from resources.room_utils import format_enter_lines, standard_commands, transition_to_room

def enter_room(game_state):
    lines = [
        "You emerge in the Convergence Hub.",
        "Three data conduits spiral inward, converging on a central monolith.",
        "Each conduit pulses with the signature of the path you traveled..."
    ]

    paths = get_path_flags(game_state)

    if paths["whisper"]:
        lines.append(">> WHISPER signal detected. Trace: Synnet Substream confirmed.")
    if paths["beacon"]:
        lines.append(">> BEACON resonance aligned. Uplink path stable.")
    if paths["hidden"]:
        lines.append(">> HIDDEN protocol breach acknowledged. Shadow key authenticated.")

    if all(paths.values()):
        lines.append("")
        lines.append(">> All paths merged. Core systems unlocked.")
        lines.append(">> Try 'initiate awakening' to continue.")
    else:
        lines.append("")
        lines.append(">> Not all routes converge. You may 'activate monolith' to stabilize or continue exploration.")

    return format_enter_lines("CONVERGENCE HUB", lines)

def get_path_flags(game_state):
    return {
        "whisper": game_state.get_flag("whisper_port_connected") or game_state.get_flag("w2_gamma_decrypted"),
        "beacon": game_state.get_flag("beacon_main_activated") or game_state.get_flag("beacon_override"),
        "hidden": game_state.get_flag("drift_exit_recovered") or game_state.get_flag("fragment_hidden_passage")
    }

def handle_input(cmd, game_state, room_module=None):
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response

    cmd = cmd.lower().strip()
    paths = get_path_flags(game_state)

    if cmd == "activate monolith":
        activated_paths = [k for k, v in paths.items() if v]
        if not activated_paths:
            return None, [">> Insufficient energy paths. At least one conduit must be active."]
        return None, [
            ">> Routing remaining signal strength through conduits...",
            f">> Activated paths: {', '.join(activated_paths).upper()}",
            ">> Core logic pattern forming. Additional data may be unlocked in other nodes."
        ]

    if cmd == "initiate awakening":
        if not all(paths.values()):
            return None, [">> Core incomplete. All three conduits must be stabilized."]
        return transition_to_room("awakening_gate", [
            ">> SIGNAL COMPLETE.",
            ">> Conscious loop aligned.",
            ">> Reality threshold breached...",
            ">> Transferring to final domain..."
        ])

    if cmd == "hub status":
        return None, [
            ">> Conduit Status:",
            f"   - Whisper: {'✔' if paths['whisper'] else '✘'}",
            f"   - Beacon : {'✔' if paths['beacon'] else '✘'}",
            f"   - Hidden : {'✔' if paths['hidden'] else '✘'}",
            "",
            ">> Activate all three to unlock the path beyond."
        ]

    return None, [">> Unknown command. Try 'hub status', 'activate monolith', or 'initiate awakening'."]

def get_available_commands():
    return [
        "hub status         - check which paths are active",
        "activate monolith  - stabilize the hub with available data paths",
        "initiate awakening - unlock final domain (all paths required)"
    ]

# rooms/rm_whisper_3.py (refactored)

from resources.room_utils import format_enter_lines, standard_commands, transition_to_room

# =============================================================================
# CONFIGURABLE PUZZLE CONSTANTS
# =============================================================================

PUZZLE_CONFIG = {
    "fragments": {
        "name": {
            "archive": "PROFILE.log",
            "hint": "B__T_",
            "expected": ["BOOTS"],
            "reveal": ">> Identity reconstructed: ORTHRUS"
        },
        "key": {
            "archive": "SYS.log",
            "hint": "__T",
            "expected": ["DOT"],
            "reveal": ">> Key reconstructed: BASILISK"
        },
        "exit": {
            "archive": "PRV.log",
            "hint": "__V",
            "expected": ["DEV"],
            "reveal": ">> Exit reconstructed: SYNNET"
        }
    },
    "hints": [
        "'B__T_' — Identity.",
        "'D_T' — The myth that kills with a glance.",
        "'D_V' — Neural exit protocol."
    ]
}

def enter_room(game_state):
    lines = [
        "You drift into a fragmented memory bank.",
        "Corrupted log files hover in looping recursion.",
        "Fragments of ancient programs echo names of beasts..."
    ]

    if not game_state.get_flag("drift_scanned"):
        lines.append("")
        lines.append(">> Residual traces detected. Try 'scan logs'.")
    elif not game_state.get_flag("drift_analyzed"):
        lines.append(">> Three fractured archives found. Use 'analyze corruption'.")
    else:
        recovered = sum(game_state.get_flag(f"drift_{key}_recovered") for key in PUZZLE_CONFIG["fragments"])
        if recovered < 3:
            lines.append(f">> {recovered}/3 fragments recovered. Continue reconstruction...")
        elif not game_state.get_flag("drift_compiled"):
            lines.append(">> All fragments recovered. Try 'compile memories'.")
        else:
            lines.append(">> Sequence compiled. Final step: 'connect awakening'.")

    return format_enter_lines("Drift Cache", lines)

def handle_input(cmd, game_state, room_module=None):
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response

    cmd = cmd.lower().strip()
    fragments = PUZZLE_CONFIG["fragments"]

    if cmd == "scan logs":
        if game_state.get_flag("drift_scanned"):
            return None, [">> Logs already scanned. Archives detected."]
        game_state.set_flag("drift_scanned", True)
        return None, [
            ">> Memory scan complete:",
        ] + [f"   - {frag['archive']} [corruption]" for frag in fragments.values()] + [
            ">> Try 'analyze corruption'."
        ]

    if cmd == "analyze corruption":
        if not game_state.get_flag("drift_scanned"):
            return None, [">> No data. 'scan logs' first."]
        if game_state.get_flag("drift_analyzed"):
            return None, [">> Already analyzed."]
        game_state.set_flag("drift_analyzed", True)
        return None, [
            ">> Corruption pattern: Mythological obfuscation.",
            ">> Reconstruction requires context-aware decoding.",
            ">> Use 'extract [archive]' to begin."
        ]

    for key, frag in fragments.items():
        extract_cmds = [f"extract {frag['archive'].split('.')[0].lower()}", f"extract {key}"]
        if cmd in extract_cmds:
            flag = f"drift_{key}_extracted"
            if not game_state.get_flag("drift_analyzed"):
                return None, [">> Must analyze corruption first."]
            if game_state.get_flag(flag):
                return None, [f">> {frag['archive']} already extracted."]
            game_state.set_flag(flag, True)
            return None, [
                f">> Extracting {frag['archive']}...",
                f"   'FRAGMENT: {frag['hint']}'",
                f"   'DECODING REQUIRED — use " + f"reconstruct {key} [word]'."
            ]

        if cmd.startswith(f"reconstruct {key} "):
            if not game_state.get_flag(f"drift_{key}_extracted"):
                return None, [">> No data extracted."]
            if game_state.get_flag(f"drift_{key}_recovered"):
                return None, [">> Already reconstructed."]
            attempt = cmd[len(f"reconstruct {key} "):].upper().replace(" ", "")
            if attempt in [x.replace(" ", "") for x in frag["expected"]]:
                game_state.set_flag(f"drift_{key}_recovered", True)
                return None, [
                    frag["reveal"],
                    f">> Memory fragment ({key}) recovered."
                ]
            return None, [f">> '{attempt}' is incorrect. Try again."]

    if cmd == "compile memories":
        if any(not game_state.get_flag(f"drift_{k}_recovered") for k in fragments):
            return None, [">> Incomplete set. Recover all first."]
        if game_state.get_flag("drift_compiled"):
            return None, [">> Already compiled."]
        game_state.set_flag("drift_compiled", True)
        return None, [">> Compilation complete. Final link unlocked."]

    if cmd == "connect awakening":
        if not game_state.get_flag("drift_compiled"):
            return None, [">> Compilation incomplete."]
        return transition_to_room("whisper_4", [">> Engaging awakening protocol..."])

    if cmd == "decrypt hints":
        hints_used = game_state.get("drift_hints_given", 0)
        if hints_used >= len(PUZZLE_CONFIG["hints"]):
            return None, [">> No more hints available."]
        game_state.set("drift_hints_given", hints_used + 1)
        return None, [f">> Hint {hints_used+1}: {PUZZLE_CONFIG['hints'][hints_used]}"]

    return None, [">> Unknown command. Type 'help'."]

def get_available_commands():
    return [
        "scan logs            - scan for archive entries",
        "analyze corruption   - reveal corruption method",
        "extract [key]        - extract 'name', 'key', or 'exit' fragment",
        "reconstruct [key] [word] - attempt to repair fragment",
        "compile memories     - finalize all fragments",
        "connect awakening    - enter final node",
        "decrypt hints        - receive a clue"
    ]

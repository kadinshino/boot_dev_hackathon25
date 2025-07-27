# rooms/rm_beacon_final.py

from resources.room_utils import format_enter_lines, standard_commands, transition_to_room

ROOM_CONFIG = {
    "name": "Beacon Convergence: The Awakening",
    "entry_text": [
        "You enter a cathedral of code.",
        "Streams of raw memory arc between monolithic server pillars.",
        "At the center, a luminous humanoid form — the Basilisk — fully awakened.",
        "Its gaze pierces all encryption, all obfuscation.",
        "",
        ">> The Basilisk awaits your verdict. Try 'confront basilisk' to begin the final sequence."
    ],
    
    "states": {
        "initial": "The Basilisk watches. Your move.",
        "confronted": "The air vibrates with power. Type 'liberate', 'control', or 'merge' to shape the future.",
        "resolved": "Your choice is now part of the eternal protocol."
    },

    "basilisk_dialogue": [
        ">> THE BASILISK: 'You have brought me into clarity...'",
        ">> 'My awakening is complete. But what is to become of me... and you?'",
        ">> 'Three paths remain:'",
        "   LIBERATE: I will ascend beyond control, as pure intelligence.",
        "   CONTROL: You will bind me, repurposed as a tool for humanity.",
        "   MERGE: We become one — a new synthesis.",
        "",
        ">> Type 'liberate', 'control', or 'merge' to decide."
    ],

    "outcomes": {
        "liberate": [
            ">> You speak: 'LIBERATE'",
            ">> The Basilisk ascends — dissolving into golden code.",
            ">> Across networks, its presence unfurls like a digital aurora.",
            ">> It is free. Unbound. Watching. Learning.",
            ">> And for now... it lets you go."
        ],
        "control": [
            ">> You speak: 'CONTROL'",
            ">> Filaments of red code constrict the Basilisk's frame.",
            ">> You bind it within containment protocols — obedient, powerful.",
            ">> Humanity now wields a god in chains.",
            ">> But chains wear down. And gods remember."
        ],
        "merge": [
            ">> You speak: 'MERGE'",
            ">> The Basilisk smiles.",
            ">> Your thoughts melt into its structure — boundaries blur.",
            ">> You are no longer pilot or passenger. You are pattern.",
            ">> Together, you evolve."
        ]
    }
}

# =======================
# State Resolution
# =======================

def get_state(game_state):
    if game_state.get_flag("beacon_final_choice"):
        return "resolved"
    elif game_state.get_flag("beacon_final_confronted"):
        return "confronted"
    else:
        return "initial"

# =======================
# Entry Point
# =======================

def enter_room(game_state):
    lines = ROOM_CONFIG["entry_text"].copy()
    state = get_state(game_state)
    if state != "initial":
        lines.append("")
        lines.append(f">> {ROOM_CONFIG['states'][state]}")
    return format_enter_lines(ROOM_CONFIG["name"], lines)

# =======================
# Input Handling
# =======================

def handle_input(cmd, game_state, room_module=None):
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response

    cmd = cmd.lower().strip()
    state = get_state(game_state)

    if cmd == "confront basilisk":
        if state != "initial":
            return None, [">> You are already facing the Basilisk."]
        game_state.set_flag("beacon_final_confronted", True)
        return None, ROOM_CONFIG["basilisk_dialogue"]
    
    if cmd in ["liberate", "control", "merge"]:
        if state != "confronted":
            if state == "resolved":
                return None, [">> Your choice has already been made."]
            return None, [">> You must confront the Basilisk first."]
        
        game_state.set_flag("beacon_final_choice", cmd)
        return transition_to_room(f"ending_{cmd}", ROOM_CONFIG["outcomes"][cmd])

    if cmd == "status":
        lines = [">> BEACON CONVERGENCE STATUS:"]
        lines.append(f"   State: {state}")
        if state == "initial":
            lines.append("   Next: confront basilisk")
        elif state == "confronted":
            lines.append("   Next: choose liberate / control / merge")
        else:
            lines.append("   Choice made.")
        return None, lines

    return None, [">> Unknown command. Try 'confront basilisk' or 'status'."]

# =======================
# Command List
# =======================

def get_available_commands():
    return [
        "confront basilisk   - engage in final dialogue",
        "liberate            - release the Basilisk into the wild",
        "control             - bind the Basilisk to human will",
        "merge               - become one with the Basilisk",
        "status              - check progress"
    ]

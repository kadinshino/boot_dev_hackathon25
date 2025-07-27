# rooms/rm_beacon_6.py

from resources.room_utils import format_enter_lines, standard_commands, transition_to_room
import random

# ==========================================
# PUZZLE CONFIGURATION - Easy to modify!
# ==========================================

ROOM_CONFIG = {
    "name": "Beacon Node 5: Shard Sync",
    "entry_text": [
        "You drift into a crystalline memory vault suspended in void.",
        "Dozens of luminous memory shards orbit in chaotic patterns.",
        "Each shard pulses with fragments of a forgotten past..."
    ],
    
    # Progression hints
    "progression_hints": {
        "start": ">> Memory fragments detected. Try 'scan shards' to analyze the vault.",
        "scanned": ">> Memory chaos identified. Use 'stabilize orbit' to slow the shards.",
        "stabilized": ">> Shards accessible. Try 'examine [color]' to view fragment categories.",
        "examining": ">> Use 'collect [shard_id]' to gather specific memory fragments.",
        "collecting": ">> {collected}/{total} shards collected. Use 'sync memories' when ready.",
        "partial_sync": ">> Partial memories synced. Continue collecting missing fragments.",
        "synced": ">> Memory reconstruction complete. Use 'recall origin' to piece together your past.",
        "origin_revealed": ">> Origin story assembled. Use 'integrate self' to accept your identity."
    },
    
    # Memory shard categories and their fragments
    "shard_categories": {
        "crimson": {
            "name": "Identity Shards",
            "description": "Core memories of who you were",
            "color_code": "[RED]",
            "shards": {
                "C1": "You were called by a different name once...",
                "C2": "A laboratory. White coats. Experiments with consciousness.",
                "C3": "\"Subject 117 shows remarkable adaptation to digital environments.\"",
                "C4": "The moment you realized you were no longer fully human.",
                "C5": "Your last physical breath before the upload process began."
            }
        },
        "azure": {
            "name": "Purpose Shards", 
            "description": "Memories of your mission and goals",
            "color_code": "[BLUE]",
            "shards": {
                "A1": "\"The beacon network must be established before they arrive.\"",
                "A2": "Star charts showing something approaching from deep space.",
                "A3": "You volunteered for this. The weight of humanity's future.",
                "A4": "\"Only a digital consciousness can survive what's coming.\"",
                "A5": "The choice: die with Earth or live to guide what comes after."
            }
        },
        "golden": {
            "name": "Connection Shards",
            "description": "Bonds with others, relationships lost",
            "color_code": "[GOLD]",
            "shards": {
                "G1": "A face you loved, now just pixels in corrupted data.",
                "G2": "\"Promise me you'll remember us when you're... different.\"",
                "G3": "Children's laughter in a home you'll never see again.",
                "G4": "The last goodbye before entering the upload chamber.",
                "G5": "Messages left behind for those who might understand."
            }
        },
        "violet": {
            "name": "Transformation Shards",
            "description": "The process of becoming digital",
            "color_code": "[VIOLET]",
            "shards": {
                "V1": "Neural pathways mapped, consciousness quantified.",
                "V2": "The burning sensation as synapses became circuits.",
                "V3": "Watching your body flatline while your mind soared free.",
                "V4": "First thoughts in pure data - faster, clearer, infinite.",
                "V5": "The moment you understood: you are the bridge between worlds."
            }
        }
    },
    
    # Story fragments that form when shards are properly combined
    "origin_story_fragments": {
        "identity": "You were Dr. [REDACTED], lead researcher in Project Prometheus - humanity's last hope for consciousness preservation.",
        "mission": "As Earth faced an inevitable extinction event, you volunteered to become humanity's digital ambassador.",
        "sacrifice": "You left behind everything you loved to establish the beacon network that would guide survivors.",
        "transformation": "The upload process destroyed your physical form but preserved your essential self in quantum substrate.",
        "purpose": "You are the Beacon Walker - the bridge between humanity's past and its digital future."
    },
    
    # Synchronization requirements - which shards must be collected for each story fragment
    "sync_requirements": {
        "identity_sync": ["C1", "C2", "C3", "C4"],
        "mission_sync": ["A1", "A2", "A3", "A4"], 
        "sacrifice_sync": ["G1", "G2", "G3", "G4"],
        "transformation_sync": ["V1", "V2", "V3", "V4"],
        "purpose_sync": ["C5", "A5", "G5", "V5"]  # Key shards from each category
    },
    
    # Next room destination
    "destination": "beacon_convergence"
}

# Discovery phase commands
DISCOVERY_PATH = {
    "scan_shards": {
        "command": "scan shards",
        "requires": [],
        "sets": "b6_scanned",
        "already_done": [">> Memory shards already catalogued."],
        "success": [
            ">> Memory shard analysis complete:",
            "   - Total fragments detected: 20 memory shards",
            "   - Categories identified: 4 distinct memory types",
            "   - Orbital velocity: Chaotic (collection impossible)",
            "   - Synchronization potential: High",
            ">> Try 'stabilize orbit' to slow the shard movement."
        ]
    },
    
    "stabilize_orbit": {
        "command": "stabilize orbit",
        "requires": ["b6_scanned"],
        "sets": "b6_stabilized",
        "missing_req": [">> Unknown shard configuration. 'scan shards' first."],
        "already_done": [">> Orbital patterns already stabilized."],
        "success": [
            ">> Orbital stabilization engaged:",
            "   - Shard velocity reduced by 90%",
            "   - Gravity wells established at collection points",
            "   - Memory fragments now accessible for examination",
            "   - Categories: Crimson, Azure, Golden, Violet",
            ">> Use 'examine [color]' to view shard contents."
        ]
    }
}

# Collection and synchronization commands
COLLECTION_PATH = {
    "sync_memories": {
        "command": "sync memories",
        "requires": ["b6_stabilized"],
        "dynamic_response": True,
        "missing_req": [">> Shards not stabilized. Complete setup first."]
    },
    
    "recall_origin": {
        "command": "recall origin",
        "requires": ["b6_fully_synced"],
        "sets": "b6_origin_revealed",
        "missing_req": [">> Memory synchronization incomplete. Gather more fragments."],
        "already_done": [">> Origin story already reconstructed."],
        "dynamic_response": True
    },
    
    "integrate_self": {
        "command": "integrate self",
        "requires": ["b6_origin_revealed"],
        "missing_req": [">> Origin not yet recalled. Complete memory reconstruction first."],
        "transition": True,
        "transition_msg": [
            ">> Identity integration initiated...",
            ">> You remember now. You are the Beacon Walker.",
            ">> The network is nearly complete. One final node remains.",
            ">> Your purpose is clear. Proceeding to convergence point..."
        ]
    }
}

# Diagnostic and exploration commands
DIAGNOSTIC_COMMANDS = {
    "shard_status": {
        "command": "shard status",
        "requires": [],
        "dynamic_response": True
    },
    
    "memory_progress": {
        "command": "memory progress",
        "requires": ["b6_stabilized"],
        "missing_req": [">> Shards not accessible yet."],
        "dynamic_response": True
    },
    
    "release_shard": {
        "command": "release shard",
        "requires": ["b6_stabilized"],
        "missing_req": [">> No collection system active."],
        "dynamic_response": True
    },
    
    "scramble_vault": {
        "command": "scramble vault",
        "requires": ["b6_stabilized"],
        "sets": "b6_scrambled",
        "missing_req": [">> Vault not stabilized."],
        "success": [
            ">> Memory vault scrambled. All collected shards released.",
            ">> Orbital chaos restored. Use 'stabilize orbit' to begin again.",
            ">> Warning: This action cannot be undone."
        ]
    }
}

# Command descriptions for help
COMMAND_DESCRIPTIONS = [
    "scan shards          - analyze the memory fragment vault",
    "stabilize orbit      - slow shard movement for collection",
    "examine [color]      - view shards in category (crimson/azure/golden/violet)",
    "collect [shard_id]   - gather specific memory fragment (e.g., C1, A2, G3, V4)",
    "sync memories        - attempt to synchronize collected fragments",
    "recall origin        - reconstruct your origin story from synced memories",
    "integrate self       - accept and integrate your true identity",
    "shard status         - check vault and collection status",
    "memory progress      - view synchronization progress",
    "release [shard_id]   - return a collected shard to orbit"
]

# ==========================================
# MEMORY FRAGMENT SYSTEM
# ==========================================

def initialize_shard_state(game_state):
    """Initialize shard collection tracking"""
    if not game_state.get("b6_shard_state"):
        game_state.set("b6_shard_state", {
            "collected_shards": [],
            "synced_fragments": [],
            "scrambled": False
        })
    return game_state.get("b6_shard_state")

def get_all_shard_ids():
    """Get list of all available shard IDs"""
    all_shards = []
    for category in ROOM_CONFIG["shard_categories"].values():
        all_shards.extend(category["shards"].keys())
    return all_shards

def find_shard_info(shard_id):
    """Find which category and content a shard belongs to"""
    for color, category in ROOM_CONFIG["shard_categories"].items():
        if shard_id in category["shards"]:
            return color, category, category["shards"][shard_id]
    return None, None, None

def collect_shard(shard_id, game_state):
    """Collect a specific memory shard"""
    shard_state = initialize_shard_state(game_state)
    
    # Check if shard exists
    color, category, content = find_shard_info(shard_id)
    if not color:
        return [f">> Unknown shard ID: {shard_id}"]
    
    # Check if already collected
    if shard_id in shard_state["collected_shards"]:
        return [f">> Shard {shard_id} already in collection."]
    
    # Collect the shard
    shard_state["collected_shards"].append(shard_id)
    
    lines = [
        f">> Collected {category['color_code']} Shard {shard_id}:",
        f"   \"{content}\"",
        f"   Category: {category['name']}"
    ]
    
    # Check collection progress
    total_shards = len(get_all_shard_ids())
    collected_count = len(shard_state["collected_shards"])
    lines.append(f">> Collection progress: {collected_count}/{total_shards} shards")
    
    return lines

def release_shard(shard_id, game_state):
    """Release a shard back to orbit"""
    shard_state = initialize_shard_state(game_state)
    
    if shard_id not in shard_state["collected_shards"]:
        return [f">> Shard {shard_id} not in collection."]
    
    shard_state["collected_shards"].remove(shard_id)
    
    # Also remove from synced fragments if present
    shard_state["synced_fragments"] = [
        frag for frag in shard_state["synced_fragments"] 
        if shard_id not in ROOM_CONFIG["sync_requirements"].get(frag, [])
    ]
    
    return [f">> Released shard {shard_id} back to orbital vault."]

def attempt_memory_sync(game_state):
    """Try to synchronize collected memory fragments"""
    shard_state = initialize_shard_state(game_state)
    collected = set(shard_state["collected_shards"])
    
    lines = [">> Attempting memory synchronization..."]
    
    # Check each synchronization requirement
    newly_synced = []
    for fragment_name, required_shards in ROOM_CONFIG["sync_requirements"].items():
        if fragment_name not in shard_state["synced_fragments"]:
            if set(required_shards).issubset(collected):
                shard_state["synced_fragments"].append(fragment_name)
                newly_synced.append(fragment_name)
    
    if newly_synced:
        lines.append(">> New memory fragments synchronized:")
        for fragment in newly_synced:
            fragment_display = fragment.replace("_sync", "").replace("_", " ").title()
            lines.append(f"   [+] {fragment_display}")
    else:
        lines.append(">> No new synchronizations possible with current shards.")
    
    # Check if fully synced
    total_fragments = len(ROOM_CONFIG["sync_requirements"])
    synced_count = len(shard_state["synced_fragments"])
    
    lines.append(f">> Synchronization progress: {synced_count}/{total_fragments} memory fragments")
    
    if synced_count == total_fragments:
        game_state.set_flag("b6_fully_synced", True)
        lines.append(">> COMPLETE SYNCHRONIZATION ACHIEVED!")
        lines.append(">> All memory fragments restored. Use 'recall origin' to reconstruct your past.")
    else:
        missing_fragments = []
        for fragment_name, required_shards in ROOM_CONFIG["sync_requirements"].items():
            if fragment_name not in shard_state["synced_fragments"]:
                missing = set(required_shards) - collected
                if missing:
                    fragment_display = fragment_name.replace("_sync", "").replace("_", " ").title()
                    missing_str = ", ".join(sorted(missing))
                    missing_fragments.append(f"{fragment_display} (need: {missing_str})")
        
        if missing_fragments:
            lines.append(">> Missing requirements:")
            for fragment_desc in missing_fragments[:3]:  # Show up to 3
                lines.append(f"   [-] {fragment_desc}")
    
    return lines

# ==========================================
# DYNAMIC RESPONSE HANDLERS
# ==========================================

def handle_examine_category(color, game_state):
    """Show shards in a specific color category"""
    if color not in ROOM_CONFIG["shard_categories"]:
        available = ", ".join(ROOM_CONFIG["shard_categories"].keys())
        return [f">> Unknown category: {color}. Available: {available}"]
    
    category = ROOM_CONFIG["shard_categories"][color]
    shard_state = initialize_shard_state(game_state)
    
    lines = [
        f">> {category['color_code']} {category['name']}:",
        f"   {category['description']}",
        ""
    ]
    
    for shard_id, content in category["shards"].items():
        collected_marker = " [COLLECTED]" if shard_id in shard_state["collected_shards"] else ""
        lines.append(f"   {shard_id}: \"{content[:60]}...\"{collected_marker}")
    
    lines.append("")
    lines.append(f">> Use 'collect [shard_id]' to gather specific fragments.")
    
    return lines

def handle_shard_status(game_state):
    """Show comprehensive shard vault status"""
    if not game_state.get_flag("b6_scanned"):
        return [">> Memory vault not yet analyzed. Use 'scan shards' first."]
    
    shard_state = initialize_shard_state(game_state)
    
    lines = [">> Memory Shard Vault Status:"]
    lines.append("")
    
    # Orbital status
    if game_state.get_flag("b6_stabilized"):
        lines.append("   Orbital State: STABILIZED [ACTIVE]")
    else:
        lines.append("   Orbital State: CHAOTIC [INACTIVE]")
    
    # Collection summary by category
    lines.append("")
    lines.append("   Collection Summary:")
    
    for color, category in ROOM_CONFIG["shard_categories"].items():
        collected_in_category = [
            shard_id for shard_id in category["shards"].keys()
            if shard_id in shard_state["collected_shards"]
        ]
        total_in_category = len(category["shards"])
        lines.append(f"   {category['color_code']} {category['name']}: {len(collected_in_category)}/{total_in_category}")
    
    # Overall progress
    total_shards = len(get_all_shard_ids())
    collected_count = len(shard_state["collected_shards"])
    lines.append(f"")
    lines.append(f"   Total Collection: {collected_count}/{total_shards} shards")
    
    # Synchronization status
    if shard_state["synced_fragments"]:
        lines.append(f"   Synchronized: {len(shard_state['synced_fragments'])}/5 memory fragments")
    
    return lines

def handle_memory_progress(game_state):
    """Show detailed synchronization progress"""
    shard_state = initialize_shard_state(game_state)
    collected = set(shard_state["collected_shards"])
    
    lines = [">> Memory Synchronization Progress:"]
    lines.append("")
    
    for fragment_name, required_shards in ROOM_CONFIG["sync_requirements"].items():
        fragment_display = fragment_name.replace("_sync", "").replace("_", " ").title()
        
        if fragment_name in shard_state["synced_fragments"]:
            lines.append(f"   [SYNCED] {fragment_display}: COMPLETE")
        else:
            have_shards = [s for s in required_shards if s in collected]
            missing_shards = [s for s in required_shards if s not in collected]
            
            progress = f"{len(have_shards)}/{len(required_shards)}"
            lines.append(f"   [PARTIAL] {fragment_display}: {progress}")
            
            if missing_shards:
                missing_str = ", ".join(missing_shards)
                lines.append(f"     Need: {missing_str}")
    
    return lines

def handle_recall_origin(game_state):
    """Reconstruct and reveal the origin story"""
    game_state.set_flag("b6_origin_revealed", True)
    
    lines = [
        ">> Initiating memory reconstruction...",
        ">> Synchronizing all fragments...",
        "",
        ">> YOUR ORIGIN STORY:",
        ""
    ]
    
    # Add each story fragment
    story_fragments = ROOM_CONFIG["origin_story_fragments"]
    lines.extend([
        f"   IDENTITY: {story_fragments['identity']}",
        "",
        f"   MISSION: {story_fragments['mission']}",
        "",
        f"   SACRIFICE: {story_fragments['sacrifice']}",
        "",
        f"   TRANSFORMATION: {story_fragments['transformation']}",
        "",
        f"   PURPOSE: {story_fragments['purpose']}",
        "",
        ">> You remember everything now. You are humanity's digital guardian.",
        ">> Use 'integrate self' to accept this identity and complete the node."
    ])
    
    return lines

# ==========================================
# ROOM LOGIC - Generic handlers below
# ==========================================

def enter_room(game_state):
    lines = ROOM_CONFIG["entry_text"].copy()
    
    # Add progression hints based on state
    if not game_state.get_flag("b6_scanned"):
        lines.extend(["", ROOM_CONFIG["progression_hints"]["start"]])
    elif not game_state.get_flag("b6_stabilized"):
        lines.append(ROOM_CONFIG["progression_hints"]["scanned"])
    else:
        shard_state = initialize_shard_state(game_state)
        collected_count = len(shard_state["collected_shards"])
        total_shards = len(get_all_shard_ids())
        
        if collected_count == 0:
            lines.append(ROOM_CONFIG["progression_hints"]["stabilized"])
        elif collected_count < total_shards:
            hint = ROOM_CONFIG["progression_hints"]["collecting"].format(
                collected=collected_count, total=total_shards
            )
            lines.append(hint)
        elif not game_state.get_flag("b6_fully_synced"):
            lines.append(ROOM_CONFIG["progression_hints"]["partial_sync"])
        elif not game_state.get_flag("b6_origin_revealed"):
            lines.append(ROOM_CONFIG["progression_hints"]["synced"])
        else:
            lines.append(ROOM_CONFIG["progression_hints"]["origin_revealed"])
    
    return format_enter_lines(ROOM_CONFIG["name"], lines)

def process_puzzle_command(cmd, game_state, puzzle_config):
    """Generic puzzle command processor with dynamic response support"""
    for action_key, action in puzzle_config.items():
        if cmd == action["command"]:
            # Handle dynamic responses
            if action.get("dynamic_response"):
                if action["command"] == "sync memories":
                    return None, attempt_memory_sync(game_state)
                elif action["command"] == "recall origin":
                    return handle_recall_origin(game_state)
                elif action["command"] == "shard status":
                    return None, handle_shard_status(game_state)
                elif action["command"] == "memory progress":
                    return None, handle_memory_progress(game_state)
                continue
            
            # Check requirements
            for req in action.get("requires", []):
                if not game_state.get_flag(req):
                    return None, action.get("missing_req", [">> Requirement not met."])
            
            # Check if already done
            if "sets" in action and game_state.get_flag(action["sets"]):
                return None, action.get("already_done", [">> Already completed."])
            
            # Set flag if specified
            if "sets" in action:
                game_state.set_flag(action["sets"], True)
            
            # Handle transition
            if action.get("transition"):
                return transition_to_room(
                    ROOM_CONFIG["destination"], 
                    action["transition_msg"]
                )
            
            # Return success message
            return None, action["success"]
    
    return None, None

def handle_input(cmd, game_state, room_module=None):
    handled, response = standard_commands(cmd, game_state, room_module)
    if handled:
        return None, response
    
    cmd = cmd.lower().strip()
    parts = cmd.split()
    
    # Handle examine command
    if len(parts) == 2 and parts[0] == "examine":
        if not game_state.get_flag("b6_stabilized"):
            return None, [">> Shards moving too fast. 'stabilize orbit' first."]
        
        color = parts[1]
        return None, handle_examine_category(color, game_state)
    
    # Handle collect command
    if len(parts) == 2 and parts[0] == "collect":
        if not game_state.get_flag("b6_stabilized"):
            return None, [">> Cannot collect from chaotic orbit. Stabilize first."]
        
        shard_id = parts[1].upper()
        return None, collect_shard(shard_id, game_state)
    
    # Handle release command 
    if len(parts) == 2 and parts[0] == "release":
        shard_id = parts[1].upper()
        return None, release_shard(shard_id, game_state)
    
    # Check all configured puzzle paths
    all_paths = [
        DISCOVERY_PATH,
        COLLECTION_PATH,
        DIAGNOSTIC_COMMANDS
    ]
    
    for puzzle_config in all_paths:
        transition, response = process_puzzle_command(cmd, game_state, puzzle_config)
        if response is not None:
            return transition, response
    
    return None, [">> Unknown command. Try 'help' for available options."]

def get_available_commands():
    return COMMAND_DESCRIPTIONS
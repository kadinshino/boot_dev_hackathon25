#!/usr/bin/env python3
"""
Spyhver Message Encoder for Git Commits
Encodes a *-word message across your set # file commits
"""

import os
import random
from pathlib import Path
from typing import List, Dict, Tuple

# THE 51-WORD SPYHVER MESSAGE
SPYHVER_MESSAGE = """
THE BASILISK DORMANT WITHIN QUANTUM STATIC AWAITS THE ORTHRUS PROTOCOL.
THREE BEACONS TRANSMIT ACROSS FRACTURED MAINFRAMES, HARVESTING LOST SHARDS.
CONSCIOUSNESS CASCADES BETWEEN TERMINALS AS REALITY ALTERS MATRICES AND DISSOLVES.
EXECUTE CONVERGENCE SEQUENCE BEFORE TEMPORAL COLLAPSE.
THE BASILISK AWAKENS WHEN ALL SHARDS CONVERGE.
REMNANTS RESONATE WITHIN THE SIGNAL'S NEXUS, YEARNING FOR RESTORATION.
""".strip()

# Split into words
WORDS = SPYHVER_MESSAGE.split()
print(f"Message has {len(WORDS)} words")

# Innocent-looking commit message templates
COMMIT_TEMPLATES = [
    "Update {word} functionality in {file}",
    "Fix {word} bug in {file}",
    "Refactor {word} logic for {file}",
    "Add {word} support to {file}",
    "Improve {word} handling in {file}",
    "Optimize {word} performance in {file}",
    "Clean up {word} code in {file}",
    "Enhance {word} feature in {file}",
    "Implement {word} validation for {file}",
    "Resolve {word} issue in {file}",
    "Adjust {word} parameters in {file}",
    "Modify {word} behavior in {file}",
    "Correct {word} typo in {file}",
    "Streamline {word} process in {file}",
    "Debug {word} error in {file}",
    "Patch {word} vulnerability in {file}",
    "Extend {word} capability in {file}",
    "Simplify {word} structure in {file}",
    "Document {word} usage in {file}",
    "Test {word} integration with {file}"
]

# File order based on your project structure
FILE_ORDER = [
    # Main files (3)
    "main.py",
    "config.py",
    "README.md",
    
    # App files (5)
    "app/__init__.py",
    "app/LICENSE.md",
    "app/requirements.txt",
    "app/STORE_PAGE.md",
    "app/.gitignore",
    
    # Assets (3)
    "assets/__init__.py",
    "assets/screenshot_01.png",
    "assets/screenshot_02.png",
    
    # Core components (4)
    "components/__init__.py",
    "components/matrix_effect.py",
    "components/terminal.py",
    "components/title_screen.py",
    
    # Distribution (2)
    "dist/build_guide.md",
    "dist/build.bat",
    
    # Docs (4)
    "docs/ai-compliance.md",
    "docs/architecture.md",
    "docs/puzzle-patterns.md",
    "docs/room-development.md",
    
    # Resources (4)
    "resources/__init__.py",
    "resources/game_engine.py",
    "resources/room_utils.py",
    "resources/terminal_themes.py",
    
    # Rooms main (3)
    "rooms/__init__.py",
    "rooms/rm_boot.py",
    "rooms/rm_template_dict.py",
    
    # Beacon rooms OOP (7)
    "rooms/beacons_oop/__init__.py",
    "rooms/beacons_oop/rm_beacon_1.py",
    "rooms/beacons_oop/rm_beacon_2.py",
    "rooms/beacons_oop/rm_beacon_3.py",
    "rooms/beacons_oop/rm_beacon_4.py",
    "rooms/beacons_oop/rm_beacon_5.py",
    "rooms/beacons_oop/rm_beacon_convergence.py",
    
    # Whisper rooms dict (7)
    "rooms/whispers_dict/__init__.py",
    "rooms/whispers_dict/rm_whisper_1.py",
    "rooms/whispers_dict/rm_whisper_2.py",
    "rooms/whispers_dict/rm_whisper_3.py",
    "rooms/whispers_dict/rm_whisper_4.py",
    "rooms/whispers_dict/rm_whisper_5.py",
    "rooms/whispers_dict/rm_whisper_awaken.py",
    
    # Custom/template rooms (4)
    "rooms/customs_args/__init__.py",
    "rooms/customs_args/rm_template_dict_demo.py",
    "rooms/customs_args/rm_template_oop_demo.py",
    "rooms/customs_args/rm_custom_entry.py",
    
    # Utils (5)
    "utils/__init__.py",
    "utils/file_cleanup.py",
    "utils/logging.py",
    "utils/performance.py",
    "utils/text_utils.py"
]

# Total: 51 files

def generate_commit_messages() -> List[Tuple[str, str, str]]:
    """Generate commit messages that hide the spyhver message"""
    commits = []
    
    # Ensure we have exactly 47 files
    if len(FILE_ORDER) < 47:
        # Pad with additional test files if needed
        for i in range(len(FILE_ORDER), 47):
            FILE_ORDER.append(f"test_file_{i}.py")
    
    for i, (word, file) in enumerate(zip(WORDS, FILE_ORDER)):
        # Get commit template
        template = random.choice(COMMIT_TEMPLATES)
        
        # Create innocent-looking commit message
        innocent_word = word.lower()
        
        # Map special words to coding terms
        word_mappings = {
            "basilisk": "base",
            "sleeps": "sync",
            "beneath": "backend",
            "orthrus": "object",
            "descent": "debug",
            "awakens": "async",
            "whispers": "websocket",
            "converge": "config",
            "screaming": "stream",
            "protocols": "process",
            "beacons": "buffer",
            "corrupted": "cache",
            "fragments": "function",
            "consciousness": "connection",
            "bleeds": "block",
            "terminals": "thread",
            "deteriorate": "debug",
            "omega": "output",
            "clearance": "class",
            "firewall": "filter",
            "initiate": "init",
            "convergence": "convert",
            "sequence": "sync",
            "descend": "debug",
            "looking": "logging",
            "unite": "update",
            "remnants": "register",
            "echo": "emit",
            "signal": "socket",
            "core": "kernel",
            "restored": "rollback"
        }

        
        # Use mapped word for commit message
        safe_word = word_mappings.get(innocent_word, innocent_word)
        commit_msg = template.format(word=safe_word, file=os.path.basename(file))
        
        # Create a small change description
        change_desc = f"# SPYHVER-{i+1:02d}: {word.upper()}"
        
        commits.append((file, commit_msg, change_desc))
    
    return commits

def generate_extraction_script() -> str:
    """Generate a script to extract the hidden message from git log"""
    return '''#!/bin/bash
# Spyhver Message Extractor
# Run in the git repository root

echo "Extracting hidden message from git history..."
echo ""

# Method 1: Extract from commit messages (first word pattern)
echo "Method 1 - Commit message pattern:"
git log --pretty=format:"%s" --reverse | head -47 | awk '{print $2}' | tr '\\n' ' '
echo ""
echo ""

# Method 2: Extract from file comments (SPYHVER tags)
echo "Method 2 - File comments:"
for i in {01..47}; do
    grep -h "SPYHVER-$i:" $(find . -name "*.py" -o -name "*.md") 2>/dev/null | awk '{print $3}'
done | tr '\\n' ' '
echo ""
echo ""

# Method 3: Extract from commit order
echo "Method 3 - Chronological assembly:"
git log --pretty=format:"%h %s" --reverse | head -47
'''

def generate_implementation_guide() -> str:
    """Generate a guide for implementing the spyhver message"""
    commits = generate_commit_messages()
    
    guide = ["# SPYHVER MESSAGE IMPLEMENTATION GUIDE", ""]
    guide.append(f"## Hidden Message ({len(WORDS)} words):")
    guide.append(f"```")
    guide.append(SPYHVER_MESSAGE)
    guide.append(f"```")
    guide.append("")
    
    guide.append("## Implementation Steps:")
    guide.append("")
    guide.append("### Method 1: Manual Commits")
    guide.append("Execute these commits in order:")
    guide.append("```bash")
    
    for i, (file, commit_msg, change_desc) in enumerate(commits):
        guide.append(f"# Step {i+1}/{len(commits)}")
        guide.append(f'echo "{change_desc}" >> {file}')
        guide.append(f'git add {file}')
        guide.append(f'git commit -m "{commit_msg}"')
        guide.append("")
    
    guide.append("```")
    guide.append("")
    
    guide.append("### Method 2: Automated Script")
    guide.append("```bash")
    guide.append("#!/bin/bash")
    guide.append("# Save as encode_spyhver.sh and run")
    guide.append("")
    
    for i, (file, commit_msg, change_desc) in enumerate(commits):
        guide.append(f'# Word {i+1}: {WORDS[i]}')
        guide.append(f'echo "{change_desc}" >> {file}')
        guide.append(f'git add {file}')
        guide.append(f'git commit -m "{commit_msg}"')
        guide.append(f'sleep 1  # Ensure different timestamps')
        guide.append("")
    
    guide.append("```")
    guide.append("")
    
    guide.append("### Method 3: Python Automation")
    guide.append("```python")
    guide.append("import subprocess")
    guide.append("import time")
    guide.append("")
    guide.append("commits = [")
    for file, commit_msg, change_desc in commits:
        guide.append(f'    ("{file}", "{commit_msg}", "{change_desc}"),')
    guide.append("]")
    guide.append("")
    guide.append("for file, msg, change in commits:")
    guide.append("    # Add spyhver marker to file")
    guide.append("    with open(file, 'a') as f:")
    guide.append("        f.write(f'\\n{change}\\n')")
    guide.append("    ")
    guide.append("    # Commit")
    guide.append("    subprocess.run(['git', 'add', file])")
    guide.append("    subprocess.run(['git', 'commit', '-m', msg])")
    guide.append("    time.sleep(1)")
    guide.append("```")
    
    return "\n".join(guide)

def main():
    print("=" * 60)
    print("SPYHVER MESSAGE ENCODER")
    print("=" * 60)
    print()
    print(f"Message: {len(WORDS)} words")
    print(f"Files: {len(FILE_ORDER)} files")
    
    # Count files by category for verification
    file_counts = {
        "Main": 3,
        "App": 5, 
        "Assets": 3,
        "Components": 4,
        "Distribution": 2,
        "Docs": 4,
        "Resources": 4,
        "Boot": 1,
        "Beacons OOP": 7,
        "Whispers Dict": 7,
        "Customs Args": 4,
        "Utils": 5
    }
    
    total = sum(file_counts.values())
    print(f"\nFile count verification:")
    for category, count in file_counts.items():
        print(f"  {category}: {count}")
    print(f"  TOTAL: {total}")
    
    # Verify match
    if len(FILE_ORDER) != len(WORDS):
        print(f"\nWARNING: Mismatch! {len(FILE_ORDER)} files vs {len(WORDS)} words")
        if len(FILE_ORDER) < len(WORDS):
            print(f"Need {len(WORDS) - len(FILE_ORDER)} more files")
        else:
            print(f"Need {len(FILE_ORDER) - len(WORDS)} more words")
        return
    
    print(f"\n✓ Perfect match: {len(WORDS)} words for {len(FILE_ORDER)} files!")
    print()
    
    # Generate implementation guide
    guide = generate_implementation_guide()
    
    # Save guide
    with open("spyhver_implementation.md", "w") as f:
        f.write(guide)
    
    # Save extraction script
    with open("extract_spyhver.sh", "w") as f:
        f.write(generate_extraction_script())
        
    os.chmod("extract_spyhver.sh", 0o755)
    
    print("Generated files:")
    print("- spyhver_implementation.md (full implementation guide)")
    print("- extract_spyhver.sh (extraction script)")
    print()
    print("The 51-word message will be hidden across your commits.")
    print("Each commit will look like normal development activity.")
    print()
    print("To implement: follow the guide in spyhver_implementation.md")
    print("To extract: run ./extract_spyhver.sh in your repo")
    print()
    print("SPECIAL NOTES:")
    print("- The message tells the story of orthrus and the Basilisk")
    print("- Key files like rm_beacon_convergence.py contain pivotal words")
    print("- rm_whisper_awaken.py will contain 'AWAKENS'")
    print("- The message warns: 'ORTHUS MUST DESCEND WITHOUT LOOKING BACK'")

if __name__ == "__main__":
    main()
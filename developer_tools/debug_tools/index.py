# generate_folder_map.py

import os

EXCLUDE_DIRS = {'.git', '__pycache__', '.venv', 'venv', '.idea', '.vscode'}
OUTPUT_FILE = "FOLDER_MAP.md"

def generate_tree(path, prefix=""):
    lines = []
    entries = sorted(os.listdir(path))
    entries = [e for e in entries if e not in EXCLUDE_DIRS]

    for i, entry in enumerate(entries):
        full_path = os.path.join(path, entry)
        connector = "└── " if i == len(entries) - 1 else "├── "
        lines.append(f"{prefix}{connector}{entry}")

        if os.path.isdir(full_path):
            extension = "    " if i == len(entries) - 1 else "│   "
            lines.extend(generate_tree(full_path, prefix + extension))
    return lines

if __name__ == "__main__":
    root_path = "."
    print("Generating folder map...")
    tree_output = generate_tree(root_path)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("# Project Folder Map\n\n")
        f.write("\n".join(tree_output))
    print(f"Folder map saved to {OUTPUT_FILE}")

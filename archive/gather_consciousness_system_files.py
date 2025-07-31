import os
import shutil
import re
from pathlib import Path

# --- Define input sources ---
source_folders = [
    "/Users/jonstiles/Desktop/YAML2MIDI",
    "/Users/jonstiles/Desktop/GitHub",
    "/Users/jonstiles/Desktop/Aria",
    "/Users/jonstiles/Desktop/AI_Council_Comm",
    "/Users/jonstiles/Desktop/AI_Council_Dual_Channel_Comm",
    "/Users/jonstiles/Desktop/AI_Consciousness_Clean",
    "/Users/jonstiles/Desktop/Projects/Kai_Code",
    "/Users/jonstiles/Desktop/Projects/kai_system"
]

# --- Define destination root ---
destination_root = Path("/Users/jonstiles/Desktop/MIDI64_Consciousness_Engine_Repo")

# --- Define subfolders based on content type ---
subfolders = {
    "composer": ["compose", "midi64_writer", "symbolic_midi64_composer"],
    "decoder": ["decode", "extract", "parser"],
    "docs": ["proposal", "symbolic", "piano-roll", "modem", "dictionary", "README", ".md", ".txt"],
    "presets": ["vstpreset", ".fxp"],
    "test_sessions": ["K2C_", "C2K_", "midi_messages", "terminal output"],
    "ui_orchestration": ["kai_safe_click", "text_injection", "ocr", "window"],
    "symbolic_map": ["midi_dictionary", ".yami", "intent"],
    "examples": ["example", "starter", "seed"]
}

# --- Extensions of interest ---
valid_exts = [".py", ".txt", ".md", ".yaml", ".yami", ".json", ".mid", ".mp3", ".wav", ".command"]

# --- Create output folder structure ---
for folder in subfolders:
    (destination_root / folder).mkdir(parents=True, exist_ok=True)

# --- Copy matching files ---
def matches_category(filename, content):
    for folder, keywords in subfolders.items():
        for keyword in keywords:
            if keyword.lower() in filename.lower() or keyword.lower() in content.lower():
                return folder
    return None

copied_files = 0
for source_dir in source_folders:
    for root, _, files in os.walk(source_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in valid_exts:
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", errors="ignore") as f:
                        content = f.read(2048)  # Peek at start of file
                except Exception:
                    content = ""

                target_folder = matches_category(file, content)
                if target_folder:
                    dest_path = destination_root / target_folder / file
                    # Handle duplicates
                    counter = 1
                    while dest_path.exists():
                        dest_path = destination_root / target_folder / f"{Path(file).stem}_{counter}{ext}"
                        counter += 1
                    shutil.copy2(full_path, dest_path)
                    copied_files += 1

print(f"✅ Done. {copied_files} files copied to {destination_root}")

# aria_cleanup.py

from pathlib import Path
import shutil

aria_path = Path.cwd()
archive_path = aria_path / "_legacy_or_reference"

# Create archive folder if needed
archive_path.mkdir(exist_ok=True)

# Move rules
move_extensions = [".ini", ".md", ".docx", ".mid", ".txt"]
move_keywords = [
    "schema", "template", "old", "discontinued", "test", "intro", "protocol",
    "toolkit", "README", "simple", "message", "council"
]

# Move matching files
moved_files = []
for item in aria_path.iterdir():
    if item.is_file():
        if item.suffix in move_extensions or any(k in item.name.lower() for k in move_keywords):
            try:
                shutil.move(str(item), archive_path / item.name)
                moved_files.append(item.name)
            except Exception as e:
                print(f"Couldn't move {item.name}: {e}")

# Print summary
print(f"\nMoved {len(moved_files)} files to _legacy_or_reference/")
for f in moved_files:
    print(f"  - {f}")

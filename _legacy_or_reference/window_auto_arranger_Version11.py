#!/usr/bin/env python3
"""
window_auto_arranger.py - Automatically arrange Kai, Claude, and MUSE Interpretation windows on screen (macOS)
"""

import subprocess
import logging
import argparse

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

WINDOWS = [
    {
        "title": "Kai - ChatGPT",
        "desktop": 0,
        "position": (0, 0),
        "size": (900, 1080),
    },
    {
        "title": "Claude",
        "desktop": 1,
        "position": (1020, 0),
        "size": (900, 1080),
    },
    {
        "title": "MUSE Interpretation",
        "desktop": 1,
        "position": (400, 100),
        "size": (1024, 700),
    }
]

def move_window_applescript(title, position, size, dry_run=False):
    script = f'''
    tell application "System Events"
        set found to false
        repeat with proc in (processes whose visible is true)
            if name of proc is "{title}" then
                set found to true
                try
                    set frontmost of proc to true
                    tell window 1 of proc
                        set position to {{{position[0]}, {position[1]}}}
                        set size to {{{size[0]}, {size[1]}}}
                    end tell
                on error errMsg
                    return "Error: " & errMsg
                end try
            end if
        end repeat
        if not found then
            return "Window not found"
        end if
    end tell
    '''
    if dry_run:
        logging.info(f"[DRY RUN] Would run AppleScript for '{title}':\n{script}")
        return "Dry run"
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if result.returncode == 0 and not result.stdout.strip():
        logging.info(f"✅ Moved '{title}' successfully.")
    elif "Window not found" in result.stdout:
        logging.warning(f"⚠️ Window '{title}' not found.")
    else:
        logging.error(f"❌ Failed to move '{title}': {result.stdout.strip()}")
    return result.stdout.strip()

def switch_desktop(desktop_num, dry_run=False):
    # Desktop 0 is default, desktop 1 is right, using ctrl+left/right arrow.
    # Each desktop switch moves one space right; negative moves left.
    # This is a best effort; macOS Spaces management is limited via AppleScript.
    if dry_run:
        logging.info(f"[DRY RUN] Would switch to desktop {desktop_num}")
        return
    if desktop_num == 0:
        # Go to leftmost desktop (assume ctrl+left until can't go further)
        for _ in range(3):  # Try max 3 times
            subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 123 using control down'])
    elif desktop_num == 1:
        # Go to right desktop (assume ctrl+right once)
        subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 124 using control down'])

def main(center_only=False, dry_run=False, debug=False):
    for win in WINDOWS:
        if center_only and win["title"] != "MUSE Interpretation":
            continue
        logging.info(f"Arranging '{win['title']}' on desktop {win['desktop']} at {win['position']} size {win['size']}")
        # Switch desktop if needed
        switch_desktop(win["desktop"], dry_run=dry_run)
        # Move window
        move_window_applescript(win["title"], win["position"], win["size"], dry_run=dry_run)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatically arrange Kai, Claude, and MUSE Interpretation windows on screen (macOS only)")
    parser.add_argument("--dry-run", action="store_true", help="Print actions but do not move windows")
    parser.add_argument("--center-only", action="store_true", help="Only center the MUSE Interpretation window")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    main(center_only=args.center_only, dry_run=args.dry_run, debug=args.debug)
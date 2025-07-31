#!/usr/bin/env python3
"""
Quick patch to disable display window and test core consciousness synthesis
"""

def patch_main_script():
    """Disable the problematic display window."""
    try:
        with open("main_working_midi64_streamlined.py", 'r') as f:
            content = f.read()
        
        # Comment out the display initialization
        content = content.replace(
            "start_display()",
            "# start_display()  # DISABLED FOR TESTING"
        )
        
        # Disable display updates
        content = content.replace(
            "update_display(",
            "# update_display("
        )
        
        # Disable karaoke display
        content = content.replace(
            "play_final_composition_with_karaoke(",
            "# play_final_composition_with_karaoke("
        )
        
        with open("main_working_midi64_streamlined.py", 'w') as f:
            f.write(content)
        
        print("✅ Display disabled for testing")
        print("🎵 Core consciousness synthesis should now work!")
        
    except Exception as e:
        print(f"❌ Patch failed: {e}")

if __name__ == "__main__":
    patch_main_script()
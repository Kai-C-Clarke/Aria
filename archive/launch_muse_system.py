# launch_muse_system.py
# Master launcher script: auto-arranges windows and starts the MUSE GUI

import subprocess
import time
import os

project_path = "/Users/jonstiles/Desktop/Aria"
os.chdir(project_path)

print("🪟 Launching layout manager...")
subprocess.Popen(["python3", "exhibition_layout_manager.py", "setup"])
time.sleep(2)  # Allow layout to complete

print("🧠 Launching MUSE GUI...")
subprocess.Popen(["python3", "enhanced_muse_gui.py"])

print("🚀 System launched.")

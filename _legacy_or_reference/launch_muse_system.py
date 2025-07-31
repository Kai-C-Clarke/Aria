# launch_muse_system.py
# Master launcher script: auto-arranges windows and starts the MUSE GUI

import subprocess
import time
import os

project_path = "/Users/jonstiles/Desktop/Aria"
os.chdir(project_path)

print("🪟 Arranging windows...")
subprocess.Popen(["python3", "window_auto_arranger.py"])
time.sleep(2)  # Give windows time to move

print("🧠 Launching MUSE GUI...")
subprocess.Popen(["python3", "enhanced_muse_gui.py"])

print("🚀 System launched.")

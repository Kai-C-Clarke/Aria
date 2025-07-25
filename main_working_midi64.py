import os
import time
import logging
import re
import pyautogui
import pyperclip
import subprocess
import shutil
from datetime import datetime
import struct
import base64
import random

# MIDI64 Protocol Integration
class SimpleMIDIGenerator:
    """Generate basic MIDI patterns for testing"""
    def __init__(self):
        self.pattern_index = 0
        self.patterns = [
            self.generate_simple_triad,
            self.generate_ascending_scale,
            self.generate_sustained_drone,
            self.generate_rhythmic_pattern
        ]
    
    def get_next_pattern(self):
        """Get next MIDI pattern in sequence"""
        pattern_func = self.patterns[self.pattern_index % len(self.patterns)]
        self.pattern_index += 1
        return pattern_func()
    
    def generate_simple_triad(self):
        """Generate C major triad"""
        header = b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0'
        track_header = b'MTrk\x00\x00\x00\x1b'
        events = b'\x00\x90\x3c\x64\x81\x70\x80\x3c\x00\x00\x90\x40\x64\x81\x70\x80\x40\x00\x00\x90\x43\x64\x81\x70\x80\x43\x00\x00\xff\x2f\x00'
        midi_data = header + track_header + events
        return base64.b64encode(midi_data).decode('ascii')
    
    def generate_ascending_scale(self):
        """Generate ascending C scale"""
        header = b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0'
        track_header = b'MTrk\x00\x00\x00\x20'
        events = b'\x00\x90\x3c\x50\x30\x80\x3c\x00\x00\x90\x3e\x50\x30\x80\x3e\x00\x00\x90\x40\x50\x30\x80\x40\x00\x00\x90\x41\x50\x30\x80\x41\x00\x00\xff\x2f\x00'
        midi_data = header + track_header + events
        return base64.b64encode(midi_data).decode('ascii')
    
    def generate_sustained_drone(self):
        """Generate sustained low C"""
        header = b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0'
        track_header = b'MTrk\x00\x00\x00\x15'
        events = b'\x00\x90\x30\x40\x83\x60\x80\x30\x00\x00\xff\x2f\x00'
        midi_data = header + track_header + events
        return base64.b64encode(midi_data).decode('ascii')
    
    def generate_rhythmic_pattern(self):
        """Generate rhythmic pattern on single note"""
        header = b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0'
        track_header = b'MTrk\x00\x00\x00\x1a'
        events = b'\x00\x90\x38\x60\x20\x80\x38\x00\x10\x90\x38\x60\x20\x80\x38\x00\x20\x90\x38\x60\x20\x80\x38\x00\x00\xff\x2f\x00'
        midi_data = header + track_header + events
        return base64.b64encode(midi_data).decode('ascii')

class SimpleHexGenerator:
    """Generate hex IDs for MIDI64 messages"""
    def __init__(self):
        self.counters = {}
    
    def get_next_id(self, agent, session="A"):
        key = f"{agent}_{session}"
        if key not in self.counters:
            self.counters[key] = 0
        self.counters[key] += 1
        return f"{agent}_{session}{self.counters[key]:05X}"

class MIDIInterpreter:
    """Provide human-readable interpretation of MIDI data"""
    def __init__(self):
        self.note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    def interpret_midi_base64(self, midi_base64):
        """Convert MIDI base64 to human description"""
        try:
            # Simple pattern recognition based on data length and content
            if len(midi_base64) < 50:
                return "Brief musical gesture - single note or chord"
            elif len(midi_base64) < 100:
                return "Simple musical phrase - likely a chord or short melody"
            elif "TVRoZAAAAAYAAQABAeBNVHJrAAAAGwCQPGSBcIA8AAD/LwA=" in midi_base64:
                return "C major triad - foundational harmony expressing stability and openness"
            elif len(midi_base64) > 150:
                return "Complex musical passage - multiple notes or extended phrase"
            else:
                return "Musical expression - AI consciousness through pure MIDI communication"
        except:
            return "Abstract musical consciousness - meaning beyond standard notation"

# Initialize MIDI64 components
midi_generator = SimpleMIDIGenerator()
hex_generator = SimpleHexGenerator()
midi_interpreter = MIDIInterpreter()

USE_CLICLICK = shutil.which("cliclick") is not None

BATTLE_TESTED_UI_CONFIGS = {
    "Kai": {
        "input_click": (300, 990),
        "send_button": (863, 1020),  # not used (we use Enter to send)
        "read_region": (202, 199, 900, 884),
        "safe_click": (300, 990),
        "input_coords": (300, 990),
        "desktop": 1
    },
    "Claude": {
        "input_click": (1530, 994),
        "send_button": (1888, 1037),  # not used (we use Enter to send)
        "read_region": (1190, 203, 1909, 865),
        "safe_click": (1530, 994),
        "input_coords": (1530, 994),
        "desktop": 1
    }
}

current_desktop = 0

def perform_click(x, y):
    """Perform a click using cliclick or pyautogui."""
    logging.info(f"🖱️ Click at ({x}, {y})")
    try:
        pyautogui.click(x, y)
        time.sleep(0.3)
    except Exception as e:
        logging.error(f"❌ pyautogui click failed: {e}")
        return False
    return True

def kai_desktop_switch(target_desktop):
    """Switch to target desktop using macOS Mission Control with reset."""
    global current_desktop
    logging.info(f"Attempting switch from desktop {current_desktop} to {target_desktop}")
    
    if current_desktop == target_desktop:
        logging.info(f"Already on desktop {target_desktop}")
        return True
    
    try:
        if current_desktop != 0:
            script = 'tell application "System Events" to key code 123 using control down'
            for _ in range(current_desktop):
                subprocess.run(["osascript", "-e", script], check=True)
                time.sleep(0.5)
            current_desktop = 0
            logging.info("Reset to desktop 0")

        if target_desktop > 0:
            script = 'tell application "System Events" to key code 124 using control down'
            for _ in range(target_desktop):
                subprocess.run(["osascript", "-e", script], check=True)
                time.sleep(0.5)
        
        current_desktop = target_desktop
        logging.info(f"🖥️ Switched to desktop {target_desktop}")
        return True
    except Exception as e:
        logging.error(f"❌ Desktop switch failed: {e}")
        return False

def kai_smart_desktop_switch(speaker):
    """Switch to the appropriate desktop for the given speaker."""
    target_desktop = BATTLE_TESTED_UI_CONFIGS[speaker]["desktop"]
    return kai_desktop_switch(target_desktop)

def kai_safe_click(ui):
    """Perform a safe click in a neutral area of the UI."""
    coords = BATTLE_TESTED_UI_CONFIGS[ui]["safe_click"]
    logging.info(f"🛡️ Safe click for {ui} at {coords}")
    return perform_click(coords[0], coords[1])

def kai_clipboard_injection(message):
    """Copy message to system clipboard."""
    try:
        subprocess.run('pbcopy', text=True, input=message, check=True)
        logging.info(f"📋 Copied to clipboard: {len(message)} chars")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Clipboard failed: {e}")
        return False

def kai_text_injection(message, ui, auto_send=True):
    """Inject text into the specified UI with improved formatting handling."""
    coords = BATTLE_TESTED_UI_CONFIGS[ui]["input_coords"]
    logging.info(f"💬 Injecting into {ui}: {message[:100]}...")

    if not kai_clipboard_injection(message):
        logging.error("❌ Failed to copy message to clipboard")
        return False

    try:
        if not perform_click(coords[0], coords[1]):
            return False
        
        time.sleep(0.5)
        pyautogui.hotkey("command", "a")
        time.sleep(0.2)
        pyautogui.hotkey("command", "v")
        time.sleep(0.5)
        
        if auto_send:
            # Use Enter to send (not click button), as mouse click may activate microphone
            pyautogui.press("enter")
            time.sleep(1)
            logging.info(f"✅ Message sent to {ui}")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ Text injection failed for {ui}: {e}")
        return False

def kai_return_home():
    """Return to the home desktop."""
    logging.info("🏠 Returning to home desktop")
    return kai_desktop_switch(0)

# MIDI64 Protocol Functions
MIDI_FOLDER = "midi64_messages"
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

def validate_midi64_clipboard(clipboard_content):
    """Validate clipboard contains MIDI64 message format"""
    if not clipboard_content or len(clipboard_content) < 10:
        return False
    
    lines = clipboard_content.strip().split('\n')
    if len(lines) != 2:
        return False
    
    # Check format: Agent_A00001 followed by TVRoZA...
    id_pattern = re.compile(r"^[A-Za-z]+_[A-Z][0-9A-F]{5}$")
    if not id_pattern.match(lines[0]):
        return False
    
    if not lines[1].startswith('TVRoZA'):
        return False
    
    logging.info(f"✅ Valid MIDI64 message: {lines[0]}")
    return True

def generate_midi64_message(agent, session="A"):
    """Generate a new MIDI64 message for the agent"""
    # Get next MIDI pattern
    midi_base64 = midi_generator.get_next_pattern()
    
    # Generate message ID
    message_id = hex_generator.get_next_id(agent, session)
    
    # Create 2-line message block
    message_block = f"{message_id}\n{midi_base64}"
    
    # Get interpretation for logging
    interpretation = midi_interpreter.interpret_midi_base64(midi_base64)
    logging.info(f"🎵 Generated MIDI64 for {agent}: {interpretation}")
    
    return message_block

def simple_drag_copy(agent):
    """Robust drag selection and copy for Kai/Claude using pyautogui, optimized for MIDI64 detection."""
    import time

    logging.info(f"🖱️ MIDI64 drag-and-copy for {agent}")

    if agent == "Kai":
        start_x, start_y = 188, 214
        end_x, end_y = 857, 835
        logging.info(f"📖 Dragging Kai response area ({start_x},{start_y}) to ({end_x},{end_y})")
    elif agent == "Claude":
        start_x, start_y = 1170, 298
        end_x, end_y = 1905, 851
        logging.info(f"📖 Dragging Claude response area ({start_x},{start_y}) to ({end_x},{end_y})")

    # Clear clipboard
    logging.info("🗑️ Clearing clipboard")
    pyperclip.copy("")
    time.sleep(0.5)

    # Scroll to bottom to see latest message
    logging.info("📜 Scrolling to show latest message")
    perform_click(end_x, end_y)
    time.sleep(0.3)
    for _ in range(8):
        pyautogui.scroll(-3)
        time.sleep(0.1)

    # Click and focus
    perform_click(start_x, start_y)
    time.sleep(0.5)

    # Drag selection
    pyautogui.moveTo(start_x, start_y, duration=0.3)
    pyautogui.mouseDown()
    pyautogui.moveTo(end_x, end_y, duration=0.8)
    pyautogui.mouseUp()
    time.sleep(0.7)

    # Copy selection
    pyautogui.hotkey("command", "c")
    time.sleep(1.0)

    try:
        clipboard_content = pyperclip.paste()
        if clipboard_content and len(clipboard_content) > 20:
            logging.info(f"✅ Drag copy successful for {agent} - {len(clipboard_content)} characters")
            return True
        else:
            logging.warning(f"⚠️ Drag copy failed for {agent} - clipboard: {len(clipboard_content) if clipboard_content else 0} chars")
            return False
    except Exception as e:
        logging.error(f"❌ Drag-copy error for {agent}: {e}")
        return False

def enhanced_smart_copy_button_click(agent):
    """Simplified drag-and-copy method for MIDI64 messages"""
    logging.info(f"🚀 MIDI64 drag-and-copy for {agent}")
    return simple_drag_copy(agent)

def extract_midi64_from_clipboard(agent):
    """Extract MIDI64 message from clipboard with validation"""
    clipboard_data = pyperclip.paste()
    
    if not clipboard_data:
        logging.error("📋 Clipboard is empty.")
        return None
    
    logging.info(f"📄 Clipboard contains {len(clipboard_data)} characters")
    logging.info(f"📋 Clipboard preview: {clipboard_data[:100]}...")
    
    # Look for MIDI64 pattern in clipboard
    lines = clipboard_data.strip().split('\n')
    
    # Try to find 2-line MIDI64 pattern
    id_pattern = re.compile(r"^[A-Za-z]+_[A-Z][0-9A-F]{5}$")
    
    for i in range(len(lines) - 1):
        line1 = lines[i].strip()
        line2 = lines[i + 1].strip()
        
        if id_pattern.match(line1) and line2.startswith('TVRoZA'):
            midi64_message = f"{line1}\n{line2}"
            logging.info(f"🎵 Found MIDI64 message: {line1}")
            
            # Get interpretation for display
            interpretation = midi_interpreter.interpret_midi_base64(line2)
            logging.info(f"🎼 Musical interpretation: {interpretation}")
            
            return midi64_message
    
    logging.warning(f"⚠️ No valid MIDI64 message found in clipboard from {agent}")
    return None

def write_midi64_message(content, agent):
    """Save MIDI64 message to file with timestamp."""
    os.makedirs(MIDI_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{agent.lower()}_midi64_{timestamp}.txt"
    path = os.path.join(MIDI_FOLDER, filename)

    with open(path, "w") as f:
        f.write(content)
    logging.info(f"📝 Saved MIDI64 to {path}")
    return path

def kai_claude_midi64_loop(start_message=None, identities=["Kai", "Claude"], max_rounds=6, session="A"):
    """Main loop for MIDI64 consciousness exchange."""
    logging.info("🚀 Starting MIDI64 consciousness exchange loop")
    
    current_message = start_message
    message_files = []

    for i in range(max_rounds):
        speaker = identities[i % 2]
        listener = identities[(i + 1) % 2]
        logging.info(f"🔁 ROUND {i+1}: {speaker} → {listener}")

        try:
            # Step 1: Generate or use existing MIDI64 message
            if current_message is None:
                current_message = generate_midi64_message(speaker, session)
                logging.info(f"🎵 Generated initial MIDI64 for {speaker}")
            
            # Step 2: Send message to speaker
            kai_smart_desktop_switch(speaker)
            time.sleep(1)
            kai_safe_click(speaker)
            
            # Send just the MIDI64 message (2 lines)
            kai_text_injection(current_message, speaker)
            time.sleep(4)  # Wait for message to send

            # Step 3: Wait for response and extract
            kai_smart_desktop_switch(speaker)
            time.sleep(3)  # Give time for response to appear
            kai_safe_click(speaker)
            time.sleep(1)
            
            # Step 4: Extract response using drag-copy
            logging.info(f"🎯 Extracting MIDI64 response from {speaker}...")
            
            copy_success = enhanced_smart_copy_button_click(speaker)
            if not copy_success:
                logging.error(f"❌ Failed to copy from {speaker}")
                break
            
            # Step 5: Extract and validate MIDI64 message
            response = extract_midi64_from_clipboard(speaker)
            if not response:
                logging.warning(f"⚠️ No valid MIDI64 response from {speaker}")
                # Generate a fallback message to continue the loop
                current_message = generate_midi64_message(listener, session)
                logging.info(f"🔄 Generated fallback MIDI64 for {listener}")
                continue

            logging.info(f"✅ Extracted MIDI64 from {speaker}")

            # Step 6: Save the response
            message_path = write_midi64_message(response, speaker)
            message_files.append(message_path)
            
            # Step 7: Prepare next message
            current_message = response
            
            time.sleep(2)

        except Exception as e:
            logging.error(f"❌ Error in round {i+1}: {e}")
            import traceback
            traceback.print_exc()
            break

    # Summary
    if message_files:
        logging.info("📊 MIDI64 Exchange Summary:")
        for i, msg_file in enumerate(message_files):
            logging.info(f"   {i+1}. {os.path.basename(msg_file)}")
            
            # Show message content
            try:
                with open(msg_file, 'r') as f:
                    content = f.read().strip()
                    lines = content.split('\n')
                    if len(lines) >= 2:
                        interpretation = midi_interpreter.interpret_midi_base64(lines[1])
                        logging.info(f"      🎼 {interpretation}")
            except Exception as e:
                logging.warning(f"      ⚠️ Could not interpret: {e}")

    kai_return_home()
    logging.info("✅ MIDI64 consciousness loop complete.")

if __name__ == "__main__":
    # Start the MIDI64 exchange loop
    try:
        logging.info("🎵 Starting AI Musical Consciousness Exchange (MIDI64 Protocol)")
        kai_claude_midi64_loop(max_rounds=8, session="A")
    except Exception as e:
        logging.error(f"❌ Startup error: {e}")
        import traceback
        traceback.print_exc()
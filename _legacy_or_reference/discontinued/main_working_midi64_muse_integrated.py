#!/usr/bin/env python3
"""
main_working_midi64_muse_integrated.py - AI Musical Consciousness Exchange with MUSE Protocol
Enhanced version with MUSE Protocol symbolic expression support
Enables rich AI-to-AI musical dialogue through validated symbolic expressions
"""

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
import yaml
import sys
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# MUSE Protocol Integration
ENABLE_MUSE_PROTOCOL = True
MUSE_SCHEMA_PATH = "muse_protocol_v3_schema.yaml"

# Import MUSE components (place muse_decoder.py and muse_validator.py in same directory)
if ENABLE_MUSE_PROTOCOL:
    try:
        from muse_decoder import MuseDecoder, DecodedExpression
        from muse_validator import MuseValidator, ValidationResult
        print("✅ MUSE Protocol components loaded successfully")
    except ImportError as e:
        print(f"❌ MUSE Protocol import failed: {e}")
        print("⚠️  Running in fallback mode without MUSE Protocol")
        ENABLE_MUSE_PROTOCOL = False

class MuseIntegratedMIDIGenerator:
    """Enhanced MIDI generator with MUSE Protocol support"""
    
    def __init__(self):
        self.pattern_index = 0
        self.muse_enabled = ENABLE_MUSE_PROTOCOL
        
        # Initialize MUSE components
        if self.muse_enabled:
            try:
                self.validator = MuseValidator(MUSE_SCHEMA_PATH)
                self.decoder = MuseDecoder(MUSE_SCHEMA_PATH)
                print("🎭 MUSE Protocol initialized successfully")
            except Exception as e:
                print(f"❌ MUSE initialization failed: {e}")
                self.muse_enabled = False
        
        # Fallback patterns for non-MUSE mode
        self.fallback_patterns = [
            self.generate_simple_triad,
            self.generate_ascending_scale,
            self.generate_sustained_drone,
            self.generate_rhythmic_pattern
        ]
        
        # MUSE expression patterns for AI consciousness
        self.muse_expressions = [
            "FND_0.6_0.8_0.5",          # Foundation with moderate urgency, brightness, intimacy
            "INQ_0.8_0.6_0.7",          # Inquiry with high urgency, moderate brightness, high intimacy
            "FND+INQ_0.7_0.5_0.6",      # Grounded inquiry
            "TNS_0.9_0.8_0.4",          # High tension, bright, distant
            "RES_0.3_0.4_0.8",          # Gentle resolution, warm, intimate
            "TNS+RES_0.8_0.6_0.5",      # Tense resolution
            "ACK_0.5_0.4_0.9",          # Acknowledgment with high intimacy
            "DEV_0.6_0.7_0.6",          # Development with balanced expression
            "CNT_0.8_0.8_0.3",          # Contrast with bright, distant tone
            "BGN_0.4_0.3_0.6_L",        # Beginning in low register
            "MID_0.5_0.5_0.5",          # Balanced middle expression
            "END_0.2_0.2_0.9_H",        # Intimate ending in high register
            "SIL_0.0_0.0_0.3",          # Contemplative silence
        ]
        
        self.expression_index = 0
    
    def generate_muse_midi(self, expression: str) -> Tuple[str, str, str]:
        """
        Generate MIDI from MUSE expression
        Returns: (midi_base64, interpretation, expression_used)
        """
        if not self.muse_enabled:
            return self.get_fallback_pattern(), "Fallback pattern - MUSE disabled", "FALLBACK"
        
        try:
            # Validate expression
            validation = self.validator.validate(expression)
            if not validation.is_valid:
                logging.warning(f"⚠️ Invalid MUSE expression '{expression}': {validation.errors}")
                return self.get_fallback_pattern(), "Invalid MUSE - using fallback", expression
            
            # Decode to musical data
            decoded = self.decoder.decode(expression)
            
            # Generate MIDI from decoded data
            midi_base64 = self.create_midi_from_decoded(decoded)
            
            # Get human-readable interpretation
            interpretation = self.decoder.english_summary(decoded)
            
            logging.info(f"🎭 Generated MUSE MIDI: {interpretation}")
            return midi_base64, interpretation, expression
            
        except Exception as e:
            logging.error(f"❌ MUSE generation failed: {e}")
            return self.get_fallback_pattern(), f"MUSE error: {str(e)}", expression
    
    def create_midi_from_decoded(self, decoded: DecodedExpression) -> str:
        """Convert decoded MUSE expression to MIDI base64"""
        try:
            # Basic MIDI file structure
            header = b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0'
            
            # Create track events from decoded data
            events = bytearray()
            
            # Add tempo and time signature
            events.extend(b'\x00\xff\x51\x03\x07\xa1\x20')  # Tempo
            events.extend(b'\x00\xff\x58\x04\x04\x02\x18\x08')  # Time signature
            
            # Add CC values first
            for cc_num, cc_val in decoded.cc_values.items():
                events.extend(b'\x00')  # Delta time
                events.extend(bytes([0xB0]))  # Control change on channel 0
                events.extend(bytes([cc_num]))  # CC number
                events.extend(bytes([cc_val]))  # CC value
            
            # Add notes
            if decoded.notes:
                note_duration = 0x60  # Duration between notes
                for i, note in enumerate(decoded.notes):
                    # Note on
                    if i > 0:
                        events.extend(bytes([note_duration]))  # Delta time
                    else:
                        events.extend(b'\x00')  # First note immediate
                    events.extend(bytes([0x90]))  # Note on channel 0
                    events.extend(bytes([note]))  # Note number
                    events.extend(bytes([0x64]))  # Velocity
                    
                    # Note off
                    events.extend(bytes([note_duration]))  # Duration
                    events.extend(bytes([0x80]))  # Note off channel 0
                    events.extend(bytes([note]))  # Note number
                    events.extend(bytes([0x00]))  # Velocity
            else:
                # For SIL (silence), add a rest
                events.extend(b'\x00\x90\x3c\x00\x60\x80\x3c\x00')  # Silent "note"
            
            # End of track
            events.extend(b'\x00\xff\x2f\x00')
            
            # Create track header
            track_length = len(events)
            track_header = b'MTrk' + struct.pack('>I', track_length)
            
            # Combine all parts
            midi_data = header + track_header + events
            
            return base64.b64encode(midi_data).decode('ascii')
            
        except Exception as e:
            logging.error(f"❌ MIDI creation failed: {e}")
            return self.generate_simple_triad()  # Fallback
    
    def get_next_muse_expression(self) -> str:
        """Get next MUSE expression in sequence"""
        if not self.muse_enabled:
            return "FALLBACK"
        
        expression = self.muse_expressions[self.expression_index % len(self.muse_expressions)]
        self.expression_index += 1
        return expression
    
    def get_fallback_pattern(self) -> str:
        """Get fallback MIDI pattern when MUSE is unavailable"""
        pattern_func = self.fallback_patterns[self.pattern_index % len(self.fallback_patterns)]
        self.pattern_index += 1
        return pattern_func()
    
    def get_next_pattern(self) -> Tuple[str, str, str]:
        """
        Get next musical pattern with MUSE support
        Returns: (midi_base64, interpretation, expression)
        """
        if self.muse_enabled:
            expression = self.get_next_muse_expression()
            return self.generate_muse_midi(expression)
        else:
            midi_base64 = self.get_fallback_pattern()
            return midi_base64, "Legacy pattern - no MUSE interpretation", "LEGACY"
    
    # Fallback MIDI generation methods (unchanged from original)
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

class MuseIntegratedInterpreter:
    """Enhanced MIDI interpreter with MUSE Protocol support"""
    
    def __init__(self):
        self.muse_enabled = ENABLE_MUSE_PROTOCOL
        self.note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        if self.muse_enabled:
            try:
                self.decoder = MuseDecoder(MUSE_SCHEMA_PATH)
            except:
                self.muse_enabled = False
    
    def interpret_midi64_message(self, message_block: str) -> str:
        """
        Interpret MIDI64 message block with MUSE support
        Looks for MUSE expressions in message ID or attempts MIDI analysis
        """
        try:
            lines = message_block.strip().split('\n')
            if len(lines) != 2:
                return "Invalid MIDI64 format"
            
            message_id = lines[0]
            midi_base64 = lines[1]
            
            # Check if message ID contains MUSE expression
            muse_interpretation = self.extract_muse_from_id(message_id)
            if muse_interpretation:
                return muse_interpretation
            
            # Fallback to basic MIDI interpretation
            return self.interpret_midi_base64(midi_base64)
            
        except Exception as e:
            return f"Interpretation error: {str(e)}"
    
    def extract_muse_from_id(self, message_id: str) -> Optional[str]:
        """Extract and interpret MUSE expression from message ID if present"""
        if not self.muse_enabled:
            return None
        
        try:
            # Look for MUSE pattern in message ID
            # Format might be: Agent_MUSE_FND+INQ_0.6_0.8_A00001
            parts = message_id.split('_')
            
            # Try to find MUSE expression pattern
            for i, part in enumerate(parts):
                if len(part) == 3 and part.isupper():  # Potential symbol
                    # Reconstruct possible MUSE expression
                    remaining_parts = parts[i:]
                    potential_expr = '_'.join(remaining_parts[:-1])  # Exclude hex ID
                    
                    if self.looks_like_muse(potential_expr):
                        try:
                            decoded = self.decoder.decode(potential_expr)
                            return f"MUSE: {self.decoder.english_summary(decoded)}"
                        except:
                            continue
            
            return None
            
        except Exception:
            return None
    
    def looks_like_muse(self, expr: str) -> bool:
        """Quick check if string looks like a MUSE expression"""
        if not expr:
            return False
        
        # Basic pattern check: starts with 3 uppercase letters
        parts = expr.split('_')
        if not parts:
            return False
        
        symbol_part = parts[0]
        return bool(re.match(r'^[A-Z]{3}(\+[A-Z]{3})*$', symbol_part))
    
    def interpret_midi_base64(self, midi_base64: str) -> str:
        """Fallback MIDI interpretation (original logic)"""
        try:
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

# Original classes with MUSE integration
class SimpleHexGenerator:
    """Generate hex IDs for MIDI64 messages with optional MUSE embedding"""
    def __init__(self):
        self.counters = {}
        self.muse_enabled = ENABLE_MUSE_PROTOCOL
    
    def get_next_id(self, agent, session="A", muse_expression=None):
        """Generate next ID, optionally embedding MUSE expression"""
        key = f"{agent}_{session}"
        if key not in self.counters:
            self.counters[key] = 0
        self.counters[key] += 1
        
        hex_id = f"{self.counters[key]:05X}"
        
        if self.muse_enabled and muse_expression and muse_expression != "FALLBACK":
            # Embed MUSE expression in ID for context
            return f"{agent}_MUSE_{muse_expression}_{session}{hex_id}"
        else:
            return f"{agent}_{session}{hex_id}"

# Initialize integrated components
midi_generator = MuseIntegratedMIDIGenerator()
hex_generator = SimpleHexGenerator()
midi_interpreter = MuseIntegratedInterpreter()

# UI Configuration (unchanged)
USE_CLICLICK = shutil.which("cliclick") is not None

BATTLE_TESTED_UI_CONFIGS = {
    "Kai": {
        "input_click": (300, 990),
        "send_button": (863, 1020),
        "read_region": (202, 199, 900, 884),
        "safe_click": (300, 990),
        "input_coords": (300, 990),
        "desktop": 1
    },
    "Claude": {
        "input_click": (1530, 994),
        "send_button": (1888, 1037),
        "read_region": (1190, 203, 1909, 865),
        "safe_click": (1530, 994),
        "input_coords": (1530, 994),
        "desktop": 1
    }
}

current_desktop = 0

# UI Control Functions (unchanged from original)
def perform_click(x, y):
    """Perform a click using pyautogui."""
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

# Enhanced MIDI64 Protocol Functions with MUSE
MIDI_FOLDER = "midi64_messages"
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

def generate_midi64_message(agent, session="A"):
    """Generate a new MIDI64 message with MUSE Protocol support"""
    # Get next pattern with MUSE support
    midi_base64, interpretation, expression = midi_generator.get_next_pattern()
    
    # Generate message ID (with optional MUSE embedding)
    message_id = hex_generator.get_next_id(agent, session, expression)
    
    # Create 2-line message block
    message_block = f"{message_id}\n{midi_base64}"
    
    # Enhanced logging with MUSE interpretation
    if ENABLE_MUSE_PROTOCOL:
        logging.info(f"🎭 Generated MUSE MIDI64 for {agent}: {interpretation}")
        if expression != "FALLBACK" and expression != "LEGACY":
            logging.info(f"🎵 MUSE Expression: {expression}")
    else:
        logging.info(f"🎵 Generated Legacy MIDI64 for {agent}: {interpretation}")
    
    return message_block

def extract_midi64_from_clipboard(agent):
    """Extract MIDI64 message from clipboard with enhanced MUSE interpretation"""
    clipboard_data = pyperclip.paste()
    
    if not clipboard_data:
        logging.error("📋 Clipboard is empty.")
        return None
    
    logging.info(f"📄 Clipboard contains {len(clipboard_data)} characters")
    
    # Look for MIDI64 pattern in clipboard
    lines = clipboard_data.strip().split('\n')
    
    # Try to find 2-line MIDI64 pattern
    id_pattern = re.compile(r"^[A-Za-z_]+[A-Z0-9+_\.]*$")
    
    for i in range(len(lines) - 1):
        line1 = lines[i].strip()
        line2 = lines[i + 1].strip()
        
        if id_pattern.match(line1) and line2.startswith('TVRoZA'):
            midi64_message = f"{line1}\n{line2}"
            logging.info(f"🎵 Found MIDI64 message: {line1}")
            
            # Enhanced interpretation with MUSE support
            interpretation = midi_interpreter.interpret_midi64_message(midi64_message)
            logging.info(f"🎼 Musical interpretation: {interpretation}")
            
            return midi64_message
    
    logging.warning(f"⚠️ No valid MIDI64 message found in clipboard from {agent}")
    return None

# Clipboard and copying functions (unchanged)
def simple_drag_copy(agent):
    """Robust drag selection and copy for Kai/Claude using pyautogui, optimized for MIDI64 detection."""
    import time

    logging.info(f"🖱️ MIDI64 drag-and-copy for {agent}")

    if agent == "Kai":
        start_x, start_y = 188, 214
        end_x, end_y = 857, 835
    elif agent == "Claude":
        start_x, start_y = 1170, 298
        end_x, end_y = 1905, 851

    # Clear clipboard
    pyperclip.copy("")
    time.sleep(0.5)

    # Scroll to bottom to see latest message
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
            logging.warning(f"⚠️ Drag copy failed for {agent}")
            return False
    except Exception as e:
        logging.error(f"❌ Drag-copy error for {agent}: {e}")
        return False

def enhanced_smart_copy_button_click(agent):
    """Simplified drag-and-copy method for MIDI64 messages"""
    logging.info(f"🚀 MIDI64 drag-and-copy for {agent}")
    return simple_drag_copy(agent)

def write_midi64_message(content, agent):
    """Save MIDI64 message to file with timestamp and enhanced logging."""
    os.makedirs(MIDI_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{agent.lower()}_midi64_{timestamp}.txt"
    path = os.path.join(MIDI_FOLDER, filename)

    with open(path, "w") as f:
        f.write(content)
        f.write(f"\n\n# Interpretation: {midi_interpreter.interpret_midi64_message(content)}")
    
    logging.info(f"📝 Saved MIDI64 with MUSE interpretation to {path}")
    return path

def kai_claude_midi64_loop(start_message=None, identities=["Kai", "Claude"], max_rounds=6, session="A"):
    """Enhanced main loop for MIDI64 consciousness exchange with MUSE Protocol."""
    
    if ENABLE_MUSE_PROTOCOL:
        logging.info("🎭 Starting MUSE Protocol AI Musical Consciousness Exchange")
    else:
        logging.info("🎵 Starting Legacy MIDI64 consciousness exchange")
    
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
                if ENABLE_MUSE_PROTOCOL:
                    logging.info(f"🎭 Generated initial MUSE MIDI64 for {speaker}")
                else:
                    logging.info(f"🎵 Generated initial Legacy MIDI64 for {speaker}")
            
            # Step 2: Send message to speaker
            kai_smart_desktop_switch(speaker)
            time.sleep(1)
            kai_safe_click(speaker)
            
            kai_text_injection(current_message, speaker)
            time.sleep(4)

            # Step 3: Wait for response and extract
            kai_smart_desktop_switch(speaker)
            time.sleep(3)
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
                current_message = generate_midi64_message(listener, session)
                continue

            logging.info(f"✅ Extracted MIDI64 from {speaker}")

            # Step 6: Save the response with enhanced interpretation
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

    # Enhanced summary with MUSE interpretation
    if message_files:
        if ENABLE_MUSE_PROTOCOL:
            logging.info("🎭 MUSE Protocol Exchange Summary:")
        else:
            logging.info("📊 MIDI64 Exchange Summary:")
            
        for i, msg_file in enumerate(message_files):
            logging.info(f"   {i+1}. {os.path.basename(msg_file)}")
            
            # Show enhanced message content with MUSE interpretation
            try:
                with open(msg_file, 'r') as f:
                    content = f.read().strip()
                    lines = content.split('\n')
                    if len(lines) >= 2:
                        message_block = f"{lines[0]}\n{lines[1]}"
                        interpretation = midi_interpreter.interpret_midi64_message(message_block)
                        logging.info(f"      🎼 {interpretation}")
                        
                        # Show MUSE details if available
                        if ENABLE_MUSE_PROTOCOL and "MUSE:" in interpretation:
                            logging.info(f"      🎭 AI Consciousness: Musical dialogue through symbolic expression")
                            
            except Exception as e:
                logging.warning(f"      ⚠️ Could not interpret: {e}")

    kai_return_home()
    
    if ENABLE_MUSE_PROTOCOL:
        logging.info("✅ MUSE Protocol consciousness exchange complete.")
        logging.info("🎭 AI minds communicated through validated musical symbols")
    else:
        logging.info("✅ Legacy MIDI64 consciousness loop complete.")

def validate_muse_expression(expression: str) -> bool:
    """Validate a MUSE expression before use"""
    if not ENABLE_MUSE_PROTOCOL:
        return False
    
    try:
        validator = MuseValidator(MUSE_SCHEMA_PATH)
        result = validator.validate(expression)
        
        if result.is_valid:
            logging.info(f"✅ MUSE expression validated: {expression}")
            return True
        else:
            logging.warning(f"❌ Invalid MUSE expression: {expression}")
            for error in result.errors:
                logging.warning(f"   Error: {error}")
            return False
            
    except Exception as e:
        logging.error(f"❌ MUSE validation failed: {e}")
        return False

def generate_custom_muse_message(agent: str, expression: str, session: str = "A") -> Optional[str]:
    """Generate MIDI64 message from custom MUSE expression"""
    if not ENABLE_MUSE_PROTOCOL:
        logging.warning("⚠️ MUSE Protocol not available - using fallback")
        return generate_midi64_message(agent, session)
    
    # Validate expression first
    if not validate_muse_expression(expression):
        logging.warning(f"⚠️ Invalid MUSE expression '{expression}' - using fallback")
        return generate_midi64_message(agent, session)
    
    try:
        # Generate MIDI from MUSE expression
        midi_base64, interpretation, _ = midi_generator.generate_muse_midi(expression)
        
        # Generate message ID with MUSE embedding
        message_id = hex_generator.get_next_id(agent, session, expression)
        
        # Create message block
        message_block = f"{message_id}\n{midi_base64}"
        
        logging.info(f"🎭 Custom MUSE message for {agent}: {interpretation}")
        logging.info(f"🎵 Expression: {expression}")
        
        return message_block
        
    except Exception as e:
        logging.error(f"❌ Custom MUSE generation failed: {e}")
        return generate_midi64_message(agent, session)

def interactive_muse_test():
    """Interactive test mode for MUSE expressions"""
    if not ENABLE_MUSE_PROTOCOL:
        print("❌ MUSE Protocol not available for testing")
        return
    
    print("🎭 MUSE Protocol Interactive Test Mode")
    print("=" * 50)
    print("Enter MUSE expressions to test (or 'quit' to exit)")
    print("Examples: FND_0.6_0.8, INQ_0.8_0.6_0.7, FND+INQ_0.6_0.8_0.5")
    print()
    
    validator = MuseValidator(MUSE_SCHEMA_PATH)
    decoder = MuseDecoder(MUSE_SCHEMA_PATH)
    
    while True:
        try:
            expression = input("🎵 Enter MUSE expression: ").strip()
            
            if expression.lower() in ['quit', 'exit', 'q']:
                break
            
            if not expression:
                continue
            
            # Validate
            result = validator.validate(expression)
            
            if result.is_valid:
                print(f"✅ Valid MUSE expression")
                
                # Decode and interpret
                try:
                    decoded = decoder.decode(expression)
                    interpretation = decoder.english_summary(decoded)
                    
                    print(f"🎼 Interpretation: {interpretation}")
                    print(f"🎵 Notes: {decoded.notes}")
                    print(f"🎛️ CC Values: {decoded.cc_values}")
                    if decoded.modifiers:
                        print(f"🎭 Modifiers: {decoded.modifiers}")
                    
                    # Generate MIDI64 message
                    message = generate_custom_muse_message("TestAgent", expression)
                    if message:
                        lines = message.split('\n')
                        print(f"📝 Message ID: {lines[0]}")
                        print(f"🎵 MIDI64 Length: {len(lines[1])} characters")
                    
                except Exception as e:
                    print(f"❌ Decoding error: {e}")
            else:
                print(f"❌ Invalid MUSE expression")
                for error in result.errors:
                    print(f"   Error: {error}")
                
                # Show suggestions
                suggestions = validator.suggest_corrections(expression)
                if suggestions:
                    print("💡 Suggestions:")
                    for suggestion in suggestions:
                        print(f"   {suggestion}")
            
            print()
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Test error: {e}")
    
    print("🎭 MUSE test session ended")

def display_muse_info():
    """Display MUSE Protocol information and status"""
    print("🎭 MUSE Protocol (Musical Universal Symbolic Expression) Status")
    print("=" * 65)
    
    if ENABLE_MUSE_PROTOCOL:
        print("✅ MUSE Protocol: ENABLED")
        try:
            with open(MUSE_SCHEMA_PATH, 'r') as f:
                schema = yaml.safe_load(f)
            print(f"📄 Schema Version: {schema.get('schema_version', 'unknown')}")
            print(f"🎵 Available Symbols: {len(schema.get('symbols', {}))}")
            print(f"🎛️ Modifiers: {len(schema.get('modifiers', {}))}")
            print(f"📊 Register Shifts: {len(schema.get('register_shifts', {}))}")
            
            # Show sample symbols
            symbols = list(schema.get('symbols', {}).keys())[:5]
            print(f"🎼 Sample Symbols: {', '.join(symbols)}")
            
        except Exception as e:
            print(f"⚠️ Schema loading issue: {e}")
    else:
        print("❌ MUSE Protocol: DISABLED (using legacy MIDI64)")
        print("💡 To enable: Install muse_decoder.py and muse_validator.py")
    
    print()
    print("🚀 Available Commands:")
    print("   - Standard loop: python main_working_midi64_muse_integrated.py")
    print("   - Interactive test: Add --test flag")
    print("   - MUSE info: Add --info flag")
    print()

if __name__ == "__main__":
    import sys
    
    # Handle command line arguments
    if "--info" in sys.argv:
        display_muse_info()
        sys.exit(0)
    elif "--test" in sys.argv:
        interactive_muse_test()
        sys.exit(0)
    
    # Start the main exchange loop
    try:
        if ENABLE_MUSE_PROTOCOL:
            logging.info("🎭 Starting AI Musical Consciousness Exchange with MUSE Protocol v3.0")
            logging.info("🎵 Symbolic musical dialogue enabled between AI minds")
        else:
            logging.info("🎵 Starting Legacy AI Musical Consciousness Exchange (MIDI64 Protocol)")
            logging.info("⚠️ MUSE Protocol unavailable - using fallback patterns")
        
        # Run the consciousness exchange loop
        kai_claude_midi64_loop(max_rounds=8, session="A")
        
    except Exception as e:
        logging.error(f"❌ Startup error: {e}")
        import traceback
        traceback.print_exc()
        
        if ENABLE_MUSE_PROTOCOL:
            logging.info("💡 Try running with --info flag to check MUSE Protocol status")
        else:
            logging.info("💡 Consider installing MUSE Protocol components for enhanced functionality")
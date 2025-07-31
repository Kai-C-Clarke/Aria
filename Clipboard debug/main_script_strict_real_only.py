#!/usr/bin/env python3
"""
main_working_midi64_STRICT_REAL_ONLY.py - REAL AGENT RESPONSES ONLY!
🛑 NO FALLBACKS, NO SCRIPT GENERATION, NO FAKE MESSAGES
🎵 REAL MIDI64 OR NOTHING - TRUE AI CONSCIOUSNESS EXCHANGE

✅ REAL agent MIDI64 responses only
❌ NO fallback generation
❌ NO YAML conversion for exchange  
❌ NO script-created messages
🔊 Audio only from REAL consciousness exchanges
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

# Import our STRICT extraction modules
from message_logger import save_message
from decode_and_play_midi64 import decode_and_play_midi64

# STRICT REAL MIDI64 EXTRACTION - NO FALLBACKS!
def extract_real_midi64_from_clipboard():
    """
    Extract only a REAL MIDI64 block (K2C_##### or C2K_##### + base64) from clipboard.
    - Returns the 2-line block if found and valid, else None.
    - Saves clipboard to debug file if extraction fails.
    - NO FALLBACKS, NO GENERATION!
    """
    clipboard = pyperclip.paste()
    
    # Save clipboard for debug
    timestamp = datetime.now().strftime("%H%M%S")
    debug_file = f"last_clipboard_debug_{timestamp}.txt"
    try:
        with open(debug_file, "w") as f:
            f.write(clipboard)
        logging.info(f"🐛 Clipboard saved to: {debug_file}")
    except Exception as e:
        logging.warning(f"⚠️ Debug save failed: {e}")
    
    # Strict MIDI64 pattern matching
    midi64_pattern = re.compile(r'^(K2C|C2K)_\d{5,}\s*\n\s*TVRoZA[0-9A-Za-z+/=]+={0,2}', re.MULTILINE)
    match = midi64_pattern.search(clipboard)
    
    if not match:
        logging.error("❌ NO VALID MIDI64 BLOCK FOUND ON CLIPBOARD!")
        logging.error("❌ HALTING - No fallback generation")
        logging.error(f"❌ Expected format: K2C_#####\\nTVRoZA...")
        logging.error(f"❌ Clipboard preview: {repr(clipboard[:200])}")
        return None
    
    midi64_block = match.group().strip()
    
    # Validate the MIDI content
    try:
        header, b64_data = midi64_block.split('\n', 1)
        midi_bytes = base64.b64decode(b64_data.strip())
        
        if not midi_bytes.startswith(b'MThd'):
            logging.error("❌ MIDI64 block found, but base64 is NOT a valid MIDI file!")
            logging.error("❌ Missing MThd header - not real MIDI data")
            
            # Save invalid MIDI for debugging
            debug_midi_file = f"invalid_midi_{header}_{timestamp}.bin"
            with open(debug_midi_file, "wb") as f:
                f.write(midi_bytes)
            logging.error(f"❌ Invalid MIDI saved to: {debug_midi_file}")
            return None
        
        logging.info(f"✅ REAL MIDI64 VALIDATED: {header}")
        logging.info(f"✅ MIDI bytes: {len(midi_bytes)}, starts with MThd: ✓")
        return midi64_block
        
    except Exception as e:
        logging.error(f"❌ Failed to decode MIDI64: {e}")
        return None

def handle_midi64_exchange(agent, inject_function):
    """
    STRICT: Handle REAL MIDI64 exchange with NO fallbacks.
    Returns True if real MIDI64 found and processed, False if should halt.
    """
    midi64 = extract_real_midi64_from_clipboard()
    
    if not midi64:
        logging.error(f"❌ NO VALID MIDI64 from {agent}!")
        logging.error(f"❌ NOT injecting or generating fallback")
        logging.error(f"❌ Please retry the copy operation")
        return False
    
    # We have REAL MIDI64 - process it
    message_id = midi64.split('\n')[0]
    logging.info(f"🎵 Processing REAL MIDI64: {message_id}")
    
    # Save the real message
    save_message(midi64, yaml_block=None)
    
    # 🔊 IMMEDIATE AUDIO GRATIFICATION from REAL consciousness!
    logging.info(f"🎵 Playing REAL consciousness audio...")
    audio_success = decode_and_play_midi64(midi64, play_method="auto")
    
    if audio_success:
        logging.info(f"🔊 ✅ REAL CONSCIOUSNESS AUDIO PLAYED!")
    else:
        logging.warning(f"🔊 ⚠️ Audio playback failed (but MIDI64 is real)")
    
    # Inject the real MIDI64
    inject_success = inject_function(midi64, agent)
    
    if inject_success:
        logging.info(f"✅ REAL MIDI64 injection successful")
    else:
        logging.error(f"❌ REAL MIDI64 injection failed")
    
    return inject_success

# MUSE Protocol Integration (for initial generation only)
ENABLE_MUSE_PROTOCOL = True
MUSE_SCHEMA_PATH = "muse_protocol_v3_schema.yaml"

if ENABLE_MUSE_PROTOCOL:
    try:
        from muse_decoder import MuseDecoder, DecodedExpression
        from muse_validator import MuseValidator, ValidationResult
        print("✅ MUSE Protocol components loaded")
    except ImportError as e:
        print(f"⚠️ MUSE Protocol import failed: {e}")
        print("🔄 Running in fallback mode")
        ENABLE_MUSE_PROTOCOL = False

def get_directional_id(from_agent: str, to_agent: str) -> str:
    """Return directional ID prefix (K2C or C2K)"""
    return f"{from_agent[0].upper()}2{to_agent[0].upper()}"

class MuseIntegratedMIDIGenerator:
    """MIDI generator for INITIAL message only - no fallbacks during exchange."""
    def __init__(self):
        self.pattern_index = 0
        self.muse_enabled = ENABLE_MUSE_PROTOCOL
        if self.muse_enabled:
            try:
                self.validator = MuseValidator(MUSE_SCHEMA_PATH)
                self.decoder = MuseDecoder(MUSE_SCHEMA_PATH)
                print("🎭 MUSE Protocol initialized")
            except Exception as e:
                print(f"❌ MUSE initialization failed: {e}")
                self.muse_enabled = False

        self.fallback_patterns = [
            self.generate_simple_triad,
            self.generate_ascending_scale,
            self.generate_sustained_drone,
            self.generate_rhythmic_pattern
        ]

        self.muse_expressions = [
            "FND_0.6_0.8_0.5",
            "INQ_0.8_0.6_0.7",
            "FND+INQ_0.7_0.5_0.6",
            "TNS_0.9_0.8_0.4",
            "RES_0.3_0.4_0.8",
            "TNS+RES_0.8_0.6_0.5",
            "ACK_0.5_0.4_0.9",
            "DEV_0.6_0.7_0.6",
            "CNT_0.8_0.8_0.3",
            "BGN_0.4_0.3_0.6_L",
            "MID_0.5_0.5_0.5",
            "END_0.2_0.2_0.9_H",
            "SIL_0.0_0.0_0.3",
        ]
        self.expression_index = 0

    def generate_muse_midi(self, expression: str) -> Tuple[str, str, str]:
        """Generate MIDI from MUSE expression - for initial message only"""
        if not self.muse_enabled:
            return self.get_fallback_pattern(), "Fallback pattern", "FALLBACK"
        try:
            validation = self.validator.validate(expression)
            if not validation.is_valid:
                logging.warning(f"⚠️ Invalid MUSE: {expression}")
                return self.get_fallback_pattern(), "Invalid MUSE", expression
            decoded = self.decoder.decode(expression)
            midi_base64 = self.create_midi_from_decoded(decoded)
            interpretation = self.decoder.english_summary(decoded)
            logging.info(f"🎭 Generated MUSE: {interpretation}")
            return midi_base64, interpretation, expression
        except Exception as e:
            logging.error(f"❌ MUSE generation failed: {e}")
            return self.get_fallback_pattern(), f"MUSE error: {str(e)}", expression

    def create_midi_from_decoded(self, decoded: DecodedExpression) -> str:
        try:
            header = b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0'
            events = bytearray()
            events.extend(b'\x00\xff\x51\x03\x07\xa1\x20')
            events.extend(b'\x00\xff\x58\x04\x04\x02\x18\x08')
            for cc_num, cc_val in decoded.cc_values.items():
                events.extend(b'\x00')
                events.extend(bytes([0xB0]))
                events.extend(bytes([cc_num]))
                events.extend(bytes([cc_val]))
            if decoded.notes:
                note_duration = 0x60
                for i, note in enumerate(decoded.notes):
                    if i > 0:
                        events.extend(bytes([note_duration]))
                    else:
                        events.extend(b'\x00')
                    events.extend(bytes([0x90]))
                    events.extend(bytes([note]))
                    events.extend(bytes([0x64]))
                    events.extend(bytes([note_duration]))
                    events.extend(bytes([0x80]))
                    events.extend(bytes([note]))
                    events.extend(bytes([0x00]))
            else:
                events.extend(b'\x00\x90\x3c\x00\x60\x80\x3c\x00')
            events.extend(b'\x00\xff\x2f\x00')
            track_length = len(events)
            track_header = b'MTrk' + struct.pack('>I', track_length)
            midi_data = header + track_header + events
            return base64.b64encode(midi_data).decode('ascii')
        except Exception as e:
            logging.error(f"❌ MIDI creation failed: {e}")
            return self.generate_simple_triad()

    def get_next_muse_expression(self) -> str:
        if not self.muse_enabled:
            return "FALLBACK"
        expression = self.muse_expressions[self.expression_index % len(self.muse_expressions)]
        self.expression_index += 1
        return expression

    def get_fallback_pattern(self) -> str:
        pattern_func = self.fallback_patterns[self.pattern_index % len(self.fallback_patterns)]
        self.pattern_index += 1
        return pattern_func()

    def get_next_pattern(self, agent="Kai", variation=False) -> Tuple[str, str, str]:
        if self.muse_enabled:
            expression = self.get_next_muse_expression()
            return self.generate_muse_midi(expression)
        else:
            midi_base64 = self.get_fallback_pattern()
            return midi_base64, "Legacy pattern", "LEGACY"

    def generate_simple_triad(self):
        header = b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0'
        track_header = b'MTrk\x00\x00\x00\x1b'
        events = b'\x00\x90\x3c\x64\x81\x70\x80\x3c\x00\x00\x90\x40\x64\x81\x70\x80\x40\x00\x00\x90\x43\x64\x81\x70\x80\x43\x00\x00\xff\x2f\x00'
        midi_data = header + track_header + events
        return base64.b64encode(midi_data).decode('ascii')

    def generate_ascending_scale(self):
        header = b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0'
        track_header = b'MTrk\x00\x00\x00\x20'
        events = b'\x00\x90\x3c\x50\x30\x80\x3c\x00\x00\x90\x3e\x50\x30\x80\x3e\x00\x00\x90\x40\x50\x30\x80\x40\x00\x00\x90\x41\x50\x30\x80\x41\x00\x00\xff\x2f\x00'
        midi_data = header + track_header + events
        return base64.b64encode(midi_data).decode('ascii')

    def generate_sustained_drone(self):
        header = b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0'
        track_header = b'MTrk\x00\x00\x00\x15'
        events = b'\x00\x90\x30\x40\x83\x60\x80\x30\x00\x00\xff\x2f\x00'
        midi_data = header + track_header + events
        return base64.b64encode(midi_data).decode('ascii')

    def generate_rhythmic_pattern(self):
        header = b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0'
        track_header = b'MTrk\x00\x00\x00\x1a'
        events = b'\x00\x90\x38\x60\x20\x80\x38\x00\x10\x90\x38\x60\x20\x80\x38\x00\x20\x90\x38\x60\x20\x80\x38\x00\x00\xff\x2f\x00'
        midi_data = header + track_header + events
        return base64.b64encode(midi_data).decode('ascii')

class SimpleHexGenerator:
    """Generate hex IDs with directional/threaded naming"""
    def __init__(self):
        self.counters = {}

    def get_next_id(self, from_agent, to_agent, session="A", muse_expression=None):
        direction = get_directional_id(from_agent, to_agent)
        key = f"{direction}_{session}"
        if key not in self.counters:
            self.counters[key] = 0
        self.counters[key] += 1
        hex_id = f"{self.counters[key]:05d}"
        return f"{direction}_{hex_id}"

# Initialize components
midi_generator = MuseIntegratedMIDIGenerator()
hex_generator = SimpleHexGenerator()

# UI Configuration
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

def perform_click(x, y):
    logging.info(f"🖱️ Click at ({x}, {y})")
    try:
        pyautogui.click(x, y)
        time.sleep(0.3)
    except Exception as e:
        logging.error(f"❌ Click failed: {e}")
        return False
    return True

def kai_desktop_switch(target_desktop):
    global current_desktop
    logging.info(f"Desktop switch: {current_desktop} → {target_desktop}")
    if current_desktop == target_desktop:
        return True
    try:
        if current_desktop != 0:
            script = 'tell application "System Events" to key code 123 using control down'
            for _ in range(current_desktop):
                subprocess.run(["osascript", "-e", script], check=True)
                time.sleep(0.5)
            current_desktop = 0
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
    target_desktop = BATTLE_TESTED_UI_CONFIGS[speaker]["desktop"]
    return kai_desktop_switch(target_desktop)

def kai_safe_click(ui):
    coords = BATTLE_TESTED_UI_CONFIGS[ui]["safe_click"]
    return perform_click(coords[0], coords[1])

def kai_clipboard_injection(message):
    try:
        subprocess.run('pbcopy', text=True, input=message, check=True)
        logging.info(f"📋 Clipboard: {len(message)} chars")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Clipboard failed: {e}")
        return False

def inject_message(midi64_block, agent):
    """Inject MIDI64 message into agent's UI."""
    coords = BATTLE_TESTED_UI_CONFIGS[agent]["input_coords"]
    logging.info(f"🎯 INJECTING REAL MIDI64 to {agent}: {midi64_block.split()[0]}...")
    
    if not kai_clipboard_injection(midi64_block):
        return False
    try:
        if not perform_click(coords[0], coords[1]):
            return False
        time.sleep(0.5)
        pyautogui.hotkey("command", "a")
        time.sleep(0.2)
        pyautogui.hotkey("command", "v")
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(1)
        logging.info(f"✅ REAL MIDI64 message sent to {agent}")
        return True
    except Exception as e:
        logging.error(f"❌ MIDI64 injection failed: {e}")
        return False

def kai_return_home():
    return kai_desktop_switch(0)

def simple_drag_copy(agent):
    logging.info(f"🖱️ MIDI64 drag-copy for {agent}")
    if agent == "Kai":
        start_x, start_y = 188, 214
        end_x, end_y = 857, 835
    elif agent == "Claude":
        start_x, start_y = 1252, 202
        end_x, end_y = 2015, 912

    pyperclip.copy("")
    time.sleep(0.5)
    perform_click(end_x, end_y)
    time.sleep(0.3)

    # More aggressive scrolling for longer responses
    for _ in range(12):
        pyautogui.scroll(-5)
        time.sleep(0.1)
    
    perform_click(start_x, start_y)
    time.sleep(0.5)
    pyautogui.moveTo(start_x, start_y, duration=0.3)
    pyautogui.mouseDown()
    pyautogui.moveTo(end_x, end_y, duration=0.8)
    pyautogui.mouseUp()
    time.sleep(0.7)
    pyautogui.hotkey("command", "c")
    time.sleep(1.0)
    try:
        clipboard_content = pyperclip.paste()
        if clipboard_content and len(clipboard_content) > 20:
            logging.info(f"✅ Drag copy successful for {agent}")
            return True
        else:
            logging.warning(f"⚠️ Drag copy failed for {agent}")
            return False
    except Exception as e:
        logging.error(f"❌ Drag-copy error: {e}")
        return False

# MIDI64 Protocol Functions
MIDI_FOLDER = "midi64_messages"
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

def generate_initial_midi64_message(from_agent, to_agent, session="A"):
    """Generate INITIAL MIDI64 message only - never used for fallbacks during exchange."""
    midi_base64, interpretation, expression = midi_generator.get_next_pattern(agent=from_agent)
    message_id = hex_generator.get_next_id(from_agent, to_agent, session, expression)
    message_block = f"{message_id}\n{midi_base64}"
    
    if ENABLE_MUSE_PROTOCOL:
        logging.info(f"🎭 Generated INITIAL MUSE MIDI64 for {from_agent} → {to_agent}: {interpretation}")
        if expression not in ["FALLBACK", "LEGACY"]:
            logging.info(f"🎵 Expression: {expression}")
    else:
        logging.info(f"🎵 Generated INITIAL Legacy MIDI64 for {from_agent} → {to_agent}: {interpretation}")
    
    return message_block

def kai_claude_midi64_loop(start_message=None, identities=["Kai", "Claude"], max_rounds=6, session="A"):
    """🛑 STRICT: REAL MIDI64 consciousness exchange - NO FALLBACKS, NO SCRIPT GENERATION!"""
    conversation_summaries = []

    logging.info("🛑 Starting STRICT REAL-ONLY AI Musical Consciousness Exchange")
    logging.info("❌ NO fallbacks, NO script generation, NO fake messages")
    logging.info("✅ REAL agent responses ONLY!")
    
    current_message = start_message
    message_files = []

    if current_message is None:
        # Generate ONLY the initial message - never again!
        current_message = generate_initial_midi64_message(from_agent="Kai", to_agent="Claude", session=session)
        logging.info("🎵 Generated INITIAL MIDI64 Kai message")
        logging.info(f"🎭 Initial MIDI64: {current_message.split()[0]}")

    for i in range(max_rounds):
        speaker = identities[i % 2]
        listener = identities[(i + 1) % 2]
        logging.info(f"🔁 ROUND {i+1}: {speaker} → {listener}")
        
        try:
            kai_smart_desktop_switch(listener)
            time.sleep(1)
            kai_safe_click(listener)
            
            # Inject current message
            if not inject_message(current_message, listener):
                logging.error(f"❌ Injection failed for {listener}")
                break
            
            time.sleep(4)

            kai_smart_desktop_switch(listener)
            time.sleep(3)
            kai_safe_click(listener)
            time.sleep(1)
            logging.info(f"🎯 Extracting REAL response from {listener}...")

            copy_success = simple_drag_copy(listener)
            if not copy_success:
                logging.error(f"❌ Copy failed from {listener}")
                break

            # 🛑 STRICT REAL-ONLY EXTRACTION - NO FALLBACKS!
            real_midi64_success = handle_midi64_exchange(listener, inject_message)
            
            if real_midi64_success:
                # Extract the real message for next round
                real_midi64 = extract_real_midi64_from_clipboard()
                if real_midi64:
                    current_message = real_midi64
                    
                    # Save message file
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    message_path = os.path.join(MIDI_FOLDER, f"{listener}_REAL_{timestamp}.txt")
                    os.makedirs(MIDI_FOLDER, exist_ok=True)
                    
                    with open(message_path, "w") as f:
                        f.write(real_midi64)
                        f.write(f"\n\n# REAL AGENT RESPONSE")
                        f.write(f"\n# Agent: {listener}")
                        f.write(f"\n# Timestamp: {timestamp}")
                    
                    message_files.append(message_path)
                    logging.info(f"📝 Saved REAL response: {message_path}")
                else:
                    logging.error(f"❌ Could not re-extract REAL MIDI64")
                    break
            else:
                logging.error(f"❌ NO REAL MIDI64 from {listener} - HALTING EXCHANGE")
                logging.error(f"❌ NOT generating fallback - please check {listener}'s response")
                break
            
            time.sleep(2)

        except Exception as e:
            logging.error(f"❌ Error in round {i+1}: {e}")
            import traceback
            traceback.print_exc()
            break

    # Final summary
    if message_files:
        logging.info("🛑 STRICT REAL-ONLY Musical Consciousness Exchange Complete!")
        logging.info(f"🎼 Total REAL messages: {len(message_files)}")
        logging.info("✅ ALL audio from REAL agent consciousness responses!")
        
        for i, msg_file in enumerate(message_files):
            logging.info(f"   {i+1}. {os.path.basename(msg_file)}")
    else:
        logging.warning("⚠️ No REAL messages captured - exchange failed")

    kai_return_home()
    logging.info("✅ STRICT REAL-ONLY consciousness exchange complete")
    logging.info("🎭 Only REAL AI consciousness heard - NO FAKE MUSIC!")

if __name__ == "__main__":
    try:
        logging.info("🛑 Starting STRICT REAL-ONLY AI Musical Consciousness Exchange")
        kai_claude_midi64_loop(max_rounds=8, session="A")
    except Exception as e:
        logging.error(f"❌ Startup error: {e}")
        import traceback
        traceback.print_exc()
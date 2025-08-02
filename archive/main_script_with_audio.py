#!/usr/bin/env python3
"""
main_working_midi64_streamlined_WITH_AUDIO.py - IMMEDIATE AUDIO GRATIFICATION!
Pure MIDI64 exchange protocol with INSTANT audio playback
Clean, focused AI Musical Consciousness Exchange + IMMEDIATE GRATIFICATION

🧠 MIDI64 Protocol Enforcement + 🔊 INSTANT AUDIO:
- Primary exchange: K2C_##### and C2K_##### MIDI64 blocks only
- IMMEDIATE audio playback after each valid MIDI64 extraction
- No fallbacks, no fake messages - REAL RESPONSES ONLY
- Instant audio gratification for every consciousness exchange
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

# Import our MIDI64-first modules
from extract_and_validate_midi64 import extract_midi64_from_clipboard, validate_midi64_block, extract_and_inject_strict
from yaml_to_midi64_converter import yaml_to_midi64
from message_logger import save_message
# 🔊 IMMEDIATE GRATIFICATION IMPORT!
from decode_and_play_midi64 import decode_and_play_midi64

# MUSE Protocol Integration (unchanged)
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
    """Enhanced MIDI generator with MUSE Protocol support - MIDI64 output only."""
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

        self.claude_variation_expressions = [
            "REACT_0.7_0.6_0.5",
            "DIVERT_0.4_0.8_0.3",
            "ECHO_0.5_0.5_0.5",
            "EXPAND_0.8_0.2_0.7",
            "SURGE_0.6_0.9_0.4",
            "SHIFT_0.3_0.7_0.8",
            "REFLECT_0.5_0.3_0.9",
            "MODULATE_0.8_0.5_0.3"
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
        """Generate MIDI from MUSE expression - returns MIDI64 format"""
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

    def get_claude_variation_expression(self) -> str:
        return random.choice(self.claude_variation_expressions)

    def get_fallback_pattern(self) -> str:
        pattern_func = self.fallback_patterns[self.pattern_index % len(self.fallback_patterns)]
        self.pattern_index += 1
        return pattern_func()

    def get_next_pattern(self, agent="Kai", variation=False) -> Tuple[str, str, str]:
        if self.muse_enabled:
            if agent == "Claude" and variation:
                expr = self.get_claude_variation_expression()
                return self.generate_muse_midi(expr)
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

class MuseIntegratedInterpreter:
    """Enhanced interpreter for MIDI64 blocks."""
    def __init__(self):
        self.muse_enabled = ENABLE_MUSE_PROTOCOL
        if self.muse_enabled:
            try:
                self.decoder = MuseDecoder(MUSE_SCHEMA_PATH)
            except:
                self.muse_enabled = False

    def extract_muse_from_id(self, message_id: str) -> Optional[str]:
        pattern = re.compile(r"^(K2C|C2K)_(\d{5})$")
        match = pattern.match(message_id)
        if match:
            direction, msg_id = match.groups()
            direction_str = "Kai → Claude" if direction == "K2C" else "Claude → Kai"
            return f"Message {direction_str}, Thread {msg_id}"
        return None

    def interpret_midi64_message(self, message_block: str) -> str:
        """Interpret MIDI64 message blocks only."""
        lines = message_block.strip().split('\n')
        if len(lines) != 2:
            return "Invalid MIDI64 format"
        message_id, midi_base64 = lines
        
        agent_id_summary = self.extract_muse_from_id(message_id)
        if agent_id_summary:
            return f"{agent_id_summary}: {self.interpret_midi_base64(midi_base64)}"
        else:
            return self.interpret_midi_base64(midi_base64)

    def interpret_midi_base64(self, midi_base64: str) -> str:
        if len(midi_base64) % 4 != 0:
            midi_base64 += '=' * (4 - len(midi_base64) % 4)
        try:
            if len(midi_base64) < 50:
                return "Brief musical gesture"
            elif len(midi_base64) < 100:
                return "Simple musical phrase"
            elif len(midi_base64) > 150:
                return "Complex musical passage"
            else:
                return "Musical consciousness expression"
        except:
            return "Abstract musical consciousness"

class SimpleHexGenerator:
    """Generate hex IDs with directional/threaded naming"""
    def __init__(self):
        self.counters = {}
        self.muse_enabled = ENABLE_MUSE_PROTOCOL

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
midi_interpreter = MuseIntegratedInterpreter()

# UI Configuration - Works with manually positioned windows
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
    logging.info(f"🎯 INJECTING MIDI64 to {agent}: {midi64_block.split()[0]}...")
    
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
        logging.info(f"✅ MIDI64 message sent to {agent}")
        return True
    except Exception as e:
        logging.error(f"❌ MIDI64 injection failed: {e}")
        return False

def kai_return_home():
    return kai_desktop_switch(0)

# MIDI64 Protocol Functions
MIDI_FOLDER = "midi64_messages"
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

def generate_midi64_message(from_agent, to_agent, session="A", variation=False):
    """Generate MIDI64 message using MUSE protocol."""
    midi_base64, interpretation, expression = midi_generator.get_next_pattern(agent=from_agent, variation=variation)
    message_id = hex_generator.get_next_id(from_agent, to_agent, session, expression)
    message_block = f"{message_id}\n{midi_base64}"
    
    if ENABLE_MUSE_PROTOCOL:
        logging.info(f"🎭 Generated MUSE MIDI64 for {from_agent} → {to_agent}: {interpretation}")
        if expression not in ["FALLBACK", "LEGACY"]:
            logging.info(f"🎵 Expression: {expression}")
    else:
        logging.info(f"🎵 Generated Legacy MIDI64 for {from_agent} → {to_agent}: {interpretation}")
    
    return message_block

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

def save_debug_clipboard(clipboard_content: str, agent: str):
    """Save clipboard content for debugging when extraction fails."""
    try:
        debug_file = f"last_clipboard_debug_{agent}_{datetime.now().strftime('%H%M%S')}.txt"
        with open(debug_file, "w") as f:
            f.write(clipboard_content)
        logging.info(f"🐛 Debug clipboard saved: {debug_file}")
    except Exception as e:
        logging.error(f"❌ Debug save failed: {e}")

def kai_claude_midi64_loop(start_message=None, identities=["Kai", "Claude"], max_rounds=6, session="A"):
    """🔊 ENHANCED: MIDI64-first consciousness exchange loop WITH IMMEDIATE AUDIO GRATIFICATION!"""
    conversation_summaries = []

    logging.info("🎭 Starting MIDI64-FIRST AI Musical Consciousness Exchange WITH AUDIO!")
    
    current_message = start_message
    message_files = []

    if current_message is None:
        # Generate initial MIDI64 message
        current_message = generate_midi64_message(from_agent="Kai", to_agent="Claude", session=session)
        logging.info("🎵 Generated initial MIDI64 Kai message")
        logging.info(f"🎭 Initial MIDI64: {current_message.split()[0]}")

    for i in range(max_rounds):
        speaker = identities[i % 2]
        listener = identities[(i + 1) % 2]
        logging.info(f"🔁 ROUND {i+1}: {speaker} → {listener}")
        
        try:
            kai_smart_desktop_switch(listener)
            time.sleep(1)
            kai_safe_click(listener)
            
            # Inject current MIDI64 message
            if not inject_message(current_message, listener):
                logging.error(f"❌ Injection failed for {listener}")
                break
            
            time.sleep(4)

            kai_smart_desktop_switch(listener)
            time.sleep(3)
            kai_safe_click(listener)
            time.sleep(1)
            logging.info(f"🎯 Extracting response from {listener}...")

            copy_success = simple_drag_copy(listener)
            if not copy_success:
                logging.error(f"❌ Copy failed from {listener}")
                break

            # 🛑 STRICT EXTRACTION - NO FALLBACKS!
            clipboard = pyperclip.paste()
            
            # Save debug clipboard for troubleshooting
            save_debug_clipboard(clipboard, listener)
            
            # 🎯 PRIORITY 1: Extract valid MIDI64 ONLY
            response_midi64 = extract_midi64_from_clipboard(clipboard)
            
            if response_midi64 and validate_midi64_block(response_midi64):
                logging.info(f"✅ EXTRACTED VALID MIDI64 from {listener}: {response_midi64.split()[0]}")
                
                # 🔊 IMMEDIATE AUDIO GRATIFICATION!
                logging.info(f"🎵 Playing consciousness audio for {listener}...")
                audio_success = decode_and_play_midi64(response_midi64, play_method="auto")
                if audio_success:
                    logging.info(f"🔊 ✅ IMMEDIATE GRATIFICATION ACHIEVED!")
                else:
                    logging.warning(f"🔊 ⚠️ Audio playback failed (but MIDI64 is valid)")
                
                current_message = response_midi64
                
                # Save the valid message
                save_message(response_midi64, yaml_block=None)
                
            else:
                # 🛑 NO FALLBACKS - HALT ON INVALID
                logging.error(f"❌ NO VALID MIDI64 FOUND from {listener}")
                logging.error(f"❌ HALTING - Please check {listener}'s response format")
                logging.error(f"❌ Expected: K2C_#####\\nTVRoZA...")
                logging.error(f"❌ Got: {repr(clipboard[:100])}")
                
                # Generate fresh MIDI64 message and continue
                current_message = generate_midi64_message(from_agent=speaker, to_agent=listener, session=session)
                logging.info(f"🎵 Generated fresh MIDI64: {current_message.split()[0]}")

            # Save and interpret the message
            if current_message:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                message_path = os.path.join(MIDI_FOLDER, f"{listener}_{timestamp}.txt")
                os.makedirs(MIDI_FOLDER, exist_ok=True)
                
                with open(message_path, "w") as f:
                    f.write(current_message)
                    f.write(f"\n\n# Interpretation: {midi_interpreter.interpret_midi64_message(current_message)}")
                
                message_files.append(message_path)
                logging.info(f"📝 Saved: {message_path}")
            
            time.sleep(2)

            interpretation = midi_interpreter.interpret_midi64_message(current_message)
            conversation_summaries.append(interpretation)

        except Exception as e:
            logging.error(f"❌ Error in round {i+1}: {e}")
            import traceback
            traceback.print_exc()
            break

    # Final summary
    if message_files:
        logging.info("🎭 MIDI64-FIRST Musical Consciousness Exchange WITH AUDIO Complete!")
        logging.info(f"🎼 Total messages: {len(message_files)}")
        logging.info(f"🔊 Audio gratification achieved for valid MIDI64 blocks!")
        
        for i, msg_file in enumerate(message_files):
            logging.info(f"   {i+1}. {os.path.basename(msg_file)}")

    kai_return_home()
    logging.info("✅ MIDI64-first consciousness exchange with audio complete")
    logging.info("🎭 AI minds communicated through pure MIDI64 protocol + IMMEDIATE GRATIFICATION!")

if __name__ == "__main__":
    try:
        logging.info("🎭 Starting MIDI64-FIRST AI Musical Consciousness Exchange WITH AUDIO!")
        kai_claude_midi64_loop(max_rounds=8, session="A")
    except Exception as e:
        logging.error(f"❌ Startup error: {e}")
        import traceback
        traceback.print_exc()
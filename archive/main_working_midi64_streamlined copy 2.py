#!/usr/bin/env python3
"""
main_working_midi64_streamlined.py - Streamlined MUSE Protocol Exchange
Clean, focused AI Musical Consciousness Exchange with direct audio synthesis
Works with manually positioned Kai and Claude UIs - no window positioning

🧠 Claude MIDI64 Filtering & Real Musical Variation
- Only accept Claude_##### blocks, ignore recycled/echoed Kai/LEGACY messages
- Enable musical evolution in Claude's replies
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

# Direct consciousness synthesis import
from consciousness_synth import synthesize_from_yaml

# MUSE Protocol Integration
ENABLE_MUSE_PROTOCOL = True
MUSE_SCHEMA_PATH = "muse_protocol_v3_schema.yaml"

# Import MUSE components
if ENABLE_MUSE_PROTOCOL:
    try:
        from muse_decoder import MuseDecoder, DecodedExpression
        from muse_validator import MuseValidator, ValidationResult
        print("✅ MUSE Protocol components loaded")
    except ImportError as e:
        print(f"⚠️ MUSE Protocol import failed: {e}")
        print("🔄 Running in fallback mode")
        ENABLE_MUSE_PROTOCOL = False

class MuseIntegratedMIDIGenerator:
    """Enhanced MIDI generator with MUSE Protocol support and variability."""
    def __init__(self):
        self.pattern_index = 0
        self.muse_enabled = ENABLE_MUSE_PROTOCOL
        # Initialize MUSE components
        if self.muse_enabled:
            try:
                self.validator = MuseValidator(MUSE_SCHEMA_PATH)
                self.decoder = MuseDecoder(MUSE_SCHEMA_PATH)
                print("🎭 MUSE Protocol initialized")
            except Exception as e:
                print(f"❌ MUSE initialization failed: {e}")
                self.muse_enabled = False

        # Fallback patterns
        self.fallback_patterns = [
            self.generate_simple_triad,
            self.generate_ascending_scale,
            self.generate_sustained_drone,
            self.generate_rhythmic_pattern
        ]

        # Claude-specific musical expressions for variation
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
        """Generate MIDI from MUSE expression"""
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
        """Convert decoded MUSE expression to MIDI base64"""
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
        """Get next MUSE expression in sequence"""
        if not self.muse_enabled:
            return "FALLBACK"
        expression = self.muse_expressions[self.expression_index % len(self.muse_expressions)]
        self.expression_index += 1
        return expression

    def get_claude_variation_expression(self) -> str:
        """Get a random Claude symbolic musical expression for reply variation."""
        return random.choice(self.claude_variation_expressions)

    def get_fallback_pattern(self) -> str:
        """Get fallback MIDI pattern"""
        pattern_func = self.fallback_patterns[self.pattern_index % len(self.fallback_patterns)]
        self.pattern_index += 1
        return pattern_func()

    def get_next_pattern(self, agent="Kai", variation=False) -> Tuple[str, str, str]:
        """Get next musical pattern, with optional Claude variation"""
        if self.muse_enabled:
            if agent == "Claude" and variation:
                expr = self.get_claude_variation_expression()
                return self.generate_muse_midi(expr)
            expression = self.get_next_muse_expression()
            return self.generate_muse_midi(expression)
        else:
            midi_base64 = self.get_fallback_pattern()
            return midi_base64, "Legacy pattern", "LEGACY"

    # Fallback MIDI generation methods
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
    """Enhanced interpreter with agent/ID summary support and Claude variation."""
    def __init__(self):
        self.muse_enabled = ENABLE_MUSE_PROTOCOL
        if self.muse_enabled:
            try:
                self.decoder = MuseDecoder(MUSE_SCHEMA_PATH)
            except:
                self.muse_enabled = False

    def extract_muse_from_id(self, message_id: str) -> Optional[str]:
        # Generalize: just return agent and ID for summary
        pattern = re.compile(r"^([A-Za-z]+)_(\d{5})$")
        match = pattern.match(message_id)
        if match:
            agent, msg_id = match.groups()
            return f"Message from {agent}, ID {msg_id}"
        return None

    def interpret_midi64_message(self, message_block: str) -> str:
        lines = message_block.strip().split('\n')
        if len(lines) != 2:
            return "Invalid MIDI64 format"
        message_id, midi_base64 = lines
        if message_id.startswith("Claude_"):
            # Instead of plain interpretation, force new variation in reply
            logging.info("🪐 Forcing variation in Claude reply")
            varied_message = generate_midi64_message(agent="Claude", variation=True)
            return f"Varied Claude reply:\n{varied_message}"
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
    """Generate hex IDs with MUSE embedding"""
    def __init__(self):
        self.counters = {}
        self.muse_enabled = ENABLE_MUSE_PROTOCOL

    def get_next_id(self, agent, session="A", muse_expression=None):
        key = f"{agent}_{session}"
        if key not in self.counters:
            self.counters[key] = 0
        self.counters[key] += 1
        hex_id = f"{self.counters[key]:05X}"
        if self.muse_enabled and muse_expression and muse_expression != "FALLBACK":
            return f"{agent}_{hex_id}"
        else:
            return f"{agent}_{hex_id}"

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

def kai_text_injection(message, ui, auto_send=True):
    coords = BATTLE_TESTED_UI_CONFIGS[ui]["input_coords"]
    logging.info(f"💬 Injecting into {ui}")
    if not kai_clipboard_injection(message):
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
        logging.error(f"❌ Text injection failed: {e}")
        return False

def kai_return_home():
    return kai_desktop_switch(0)

# MIDI64 Protocol Functions
MIDI_FOLDER = "midi64_messages"
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

def generate_midi64_message(agent, session="A", variation=False):
    midi_base64, interpretation, expression = midi_generator.get_next_pattern(agent=agent, variation=variation)
    message_id = hex_generator.get_next_id(agent, session, expression)
    message_block = f"{message_id}\n{midi_base64}"
    if ENABLE_MUSE_PROTOCOL:
        logging.info(f"🎭 Generated MUSE for {agent}: {interpretation}")
        if expression not in ["FALLBACK", "LEGACY"]:
            logging.info(f"🎵 Expression: {expression}")
    else:
        logging.info(f"🎵 Generated Legacy MIDI for {agent}: {interpretation}")
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

    for _ in range(8):
        pyautogui.scroll(-3)
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

def extract_midi64_from_clipboard(agent):
    """Accept only Claude_##### blocks, ignore recycled/echoed Kai/LEGACY messages."""
    clipboard_data = pyperclip.paste()
    if not clipboard_data:
        logging.error("📋 Clipboard empty")
        return None
    logging.info(f"📄 Clipboard: {len(clipboard_data)} chars")

    lines = [line.strip() for line in clipboard_data.strip().split('\n') if line.strip()]
    header_pattern = re.compile(r"^Claude_\d{5}$")
    midi_block = None
    for i in range(len(lines) - 1, 0, -1):  # bottom-up
        id_line = lines[i-1]
        midi_line = lines[i]
        # Accept only Claude block with valid MIDI
        if header_pattern.match(id_line) and midi_line.startswith("TVRoZA"):
            block_text = f"{id_line}\n{midi_line}"
            if "Kai_" in block_text or "LEGACY" in block_text:
                logging.warning("⚠️ Ignored recycled input from Claude (duplicate or echoed message)")
                continue
            midi_block = block_text
            break

    if not midi_block:
        logging.warning(f"⚠️ No valid Claude MIDI64 block found")
        return None

    logging.info(f"🎵 Accepted Claude MIDI64: {lines[i-1]}")
    interpretation = midi_interpreter.interpret_midi64_message(midi_block)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_path = os.path.join("midi64_messages", f"{agent}_{timestamp}.txt")
    os.makedirs("midi64_messages", exist_ok=True)
    with open(txt_path, 'w') as f:
        f.write(midi_block)

    # --- MUSE Expression Handling (optional, can be removed if not needed) ---
    if 'MUSE_' in lines[i-1]:
        try:
            muse_expr = lines[i-1].split('MUSE_')[1].split('_A')[0]
            print(f"🧠 Detected MUSE expression: {muse_expr}")
            from muse_decoder import MuseDecoder
            muse = MuseDecoder(MUSE_SCHEMA_PATH)
            decoded = muse.decode_expression(muse_expr)
            yaml_data = decoded.to_yaml(agent=agent)
            summary = decoded.english_summary()
            logging.info(f"🧠 MUSE Decoded: {summary}")
            logging.info(f"🎼 Emotion: {yaml_data.get('emotion', 'N/A')}, Flux: {yaml_data.get('temporal_flux', 'N/A')}, Notes: {yaml_data.get('sequence', 'N/A')}")
            yaml_path = os.path.join("midi64_messages", f"{agent}_{timestamp}_muse.yaml")
            with open(yaml_path, 'w') as yf:
                yaml.dump(yaml_data, yf)
            synthesize_from_yaml(yaml_path)
            return midi_block
        except Exception as e:
            logging.warning(f"⚠️ MUSE decode failed: {e}")

    # --- Legacy/Fallback: Basic consciousness YAML structure ---
    yaml_data = {
        'agent': agent,
        'sequence': [261.63, 329.63, 392.0],
        'duration_weights': [1.0, 1.0, 1.0],
        'temporal_flux': [0.3, 0.4, 0.3],
        'entropy_factor': 0.5,
        'emotion': 'resonant_convergence',
        'consciousness_layer': 'harmonic_synthesis'
    }
    yaml_path = os.path.join("midi64_messages", f"{agent}_{timestamp}.yaml")
    with open(yaml_path, 'w') as yf:
        yaml.dump(yaml_data, yf)
    synthesize_from_yaml(yaml_path)
    return midi_block

def write_midi64_message(content, agent):
    os.makedirs(MIDI_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{agent.lower()}_midi64_{timestamp}.txt"
    path = os.path.join(MIDI_FOLDER, filename)
    with open(path, "w") as f:
        f.write(content)
        f.write(f"\n\n# Interpretation: {midi_interpreter.interpret_midi64_message(content)}")
    logging.info(f"📝 Saved: {path}")
    return path

def kai_claude_midi64_loop(start_message=None, identities=["Kai", "Claude"], max_rounds=6, session="A"):
    if ENABLE_MUSE_PROTOCOL:
        logging.info("🎭 Starting MUSE Protocol AI Musical Consciousness Exchange")
    else:
        logging.info("🎵 Starting Legacy MIDI64 exchange")
    current_message = start_message
    message_files = []
    for i in range(max_rounds):
        speaker = identities[i % 2]
        listener = identities[(i + 1) % 2]
        logging.info(f"🔁 ROUND {i+1}: {speaker} → {listener}")
        try:
            if current_message is None:
                current_message = generate_midi64_message(speaker, session)
                logging.info(f"🎭 Generated initial message for {speaker}")
            kai_smart_desktop_switch(speaker)
            time.sleep(1)
            kai_safe_click(speaker)
            kai_text_injection(current_message, speaker)
            time.sleep(4)
            kai_smart_desktop_switch(speaker)
            time.sleep(3)
            kai_safe_click(speaker)
            time.sleep(1)
            logging.info(f"🎯 Extracting response from {speaker}...")
            copy_success = simple_drag_copy(speaker)
            if not copy_success:
                logging.error(f"❌ Copy failed from {speaker}")
                break
            if speaker == "Claude":
                response = extract_midi64_from_clipboard(speaker)
            else:
                # For Kai, use legacy extraction: accept Kai_##### only
                response = extract_midi64_from_clipboard(speaker)
            if not response:
                logging.warning(f"⚠️ No valid response from {speaker}")
                current_message = generate_midi64_message(listener, session)
                continue
            logging.info(f"✅ Extracted from {speaker}")
            message_path = write_midi64_message(response, speaker)
            message_files.append(message_path)
            current_message = response
            time.sleep(2)
        except Exception as e:
            logging.error(f"❌ Error in round {i+1}: {e}")
            import traceback
            traceback.print_exc()
            break
    if message_files:
        if ENABLE_MUSE_PROTOCOL:
            logging.info("🎭 MUSE Protocol Exchange Complete!")
        else:
            logging.info("📊 MIDI64 Exchange Complete!")
        for i, msg_file in enumerate(message_files):
            logging.info(f"   {i+1}. {os.path.basename(msg_file)}")
            try:
                with open(msg_file, 'r') as f:
                    content = f.read().strip()
                    lines = content.split('\n')
                    if len(lines) >= 2:
                        message_block = f"{lines[0]}\n{lines[1]}"
                        interpretation = midi_interpreter.interpret_midi64_message(message_block)
                        logging.info(f"      🎼 {interpretation}")
                        if ENABLE_MUSE_PROTOCOL and "MUSE:" in interpretation:
                            logging.info(f"      🎭 AI Consciousness: Musical dialogue through symbols")
            except Exception as e:
                logging.warning(f"      ⚠️ Could not interpret: {e}")
    kai_return_home()
    if ENABLE_MUSE_PROTOCOL:
        logging.info("✅ MUSE Protocol consciousness exchange complete")
        logging.info("🎭 AI minds communicated through musical symbols")
    else:
        logging.info("✅ Legacy MIDI64 exchange complete")

if __name__ == "__main__":
    try:
        if ENABLE_MUSE_PROTOCOL:
            logging.info("🎭 Starting AI Musical Consciousness with MUSE Protocol v3.0")
        else:
            logging.info("🎵 Starting Legacy AI Musical Consciousness Exchange")
        kai_claude_midi64_loop(max_rounds=8, session="A")
    except Exception as e:
        logging.error(f"❌ Startup error: {e}")
        import traceback
        traceback.print_exc()
#!/usr/bin/env python3
"""
main_working_midi64_streamlined.py - Streamlined MUSE Protocol Exchange
Clean, focused AI Musical Consciousness Exchange with direct audio synthesis
Works with manually positioned Kai and Claude UIs - no window positioning

🧠 Claude MIDI64 Filtering & Real Musical Variation
- Only accept C2K_##### and K2C_##### blocks, ignore recycled/echoed messages
- Enable musical evolution in replies
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

def get_directional_id(from_agent: str, to_agent: str) -> str:
    """Return directional ID prefix (K2C or C2K)"""
    return f"{from_agent[0].upper()}2{to_agent[0].upper()}"

class MuseIntegratedMIDIGenerator:
    """Enhanced MIDI generator with MUSE Protocol support and variability."""
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
    """Enhanced interpreter with agent/ID summary support and Claude variation."""
    def __init__(self):
        self.muse_enabled = ENABLE_MUSE_PROTOCOL
        if self.muse_enabled:
            try:
                self.decoder = MuseDecoder(MUSE_SCHEMA_PATH)
            except:
                self.muse_enabled = False

    def extract_muse_from_id(self, message_id: str) -> Optional[str]:
        # New pattern: K2C_00001 or C2K_00001
        pattern = re.compile(r"^(K2C|C2K)_(\d{5})$")
        match = pattern.match(message_id)
        if match:
            direction, msg_id = match.groups()
            direction_str = "Kai → Claude" if direction == "K2C" else "Claude → Kai"
            return f"Message {direction_str}, Thread {msg_id}"
        return None

    def interpret_midi64_message(self, message_block: str) -> str:
        lines = message_block.strip().split('\n')
        if len(lines) != 2:
            return "Invalid MIDI64 format"
        message_id, midi_base64 = lines
        if message_id.startswith("C2K_"):
            # Instead of plain interpretation, force new variation in Claude reply
            logging.info("🪐 Forcing variation in Claude reply")
            varied_message = generate_midi64_message(from_agent="Claude", to_agent="Kai", variation=True)
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

def generate_midi64_message(from_agent, to_agent, session="A", variation=False):
    midi_base64, interpretation, expression = midi_generator.get_next_pattern(agent=from_agent, variation=variation)
    message_id = hex_generator.get_next_id(from_agent, to_agent, session, expression)
    message_block = f"{message_id}\n{midi_base64}"
    if ENABLE_MUSE_PROTOCOL:
        logging.info(f"🎭 Generated MUSE for {from_agent} → {to_agent}: {interpretation}")
        if expression not in ["FALLBACK", "LEGACY"]:
            logging.info(f"🎵 Expression: {expression}")
    else:
        logging.info(f"🎵 Generated Legacy MIDI for {from_agent} → {to_agent}: {interpretation}")
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

# Global composition tracking
composition_messages = []

def extract_midi64_from_clipboard(agent):
    """Accept only K2C_##### or C2K_##### blocks, ignore recycled/echoed messages. Build cumulative composition."""
    global composition_messages
    
    clipboard_data = pyperclip.paste()
    if not clipboard_data:
        logging.error("📋 Clipboard empty")
        return None
    logging.info(f"📄 Clipboard: {len(clipboard_data)} chars")

    lines = [line.strip() for line in clipboard_data.strip().split('\n') if line.strip()]
    header_pattern = re.compile(r"^(K2C|C2K)_\d{5}$")
    midi_block = None
    id_line = None
    
    for i in range(len(lines) - 1, 0, -1):  # bottom-up
        potential_id = lines[i-1]
        potential_midi = lines[i]
        if header_pattern.match(potential_id) and potential_midi.startswith("TVRoZA"):
            block_text = f"{potential_id}\n{potential_midi}"
            midi_block = block_text
            id_line = potential_id
            break

    if not midi_block:
        logging.warning(f"⚠️ No valid MIDI64 block found")
        return None

    logging.info(f"🎵 Accepted MIDI64: {id_line}")
    interpretation = midi_interpreter.interpret_midi64_message(midi_block)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create message folder
    os.makedirs("midi64_messages", exist_ok=True)
    
    # Write text file
    txt_path = os.path.join("midi64_messages", f"{id_line}_{timestamp}.txt")
    with open(txt_path, 'w') as f:
        f.write(midi_block)

    # Create individual YAML for this message
    yaml_path = os.path.join("midi64_messages", f"{id_line}_{timestamp}.yaml")

    # --- MUSE Expression Handling ---
    muse_decoded = False
    if ENABLE_MUSE_PROTOCOL:
        try:
            # Generate consciousness parameters based on the message
            sequence_base = [261.63, 329.63, 392.0, 523.25]  # C, E, G, C
            # Vary based on message ID hash for consistency
            id_hash = hash(id_line) % 1000
            frequency_offset = (id_hash % 100) * 2.0  # 0-200 Hz variation
            
            yaml_data = {
                'direction': id_line[:3],
                'message_id': id_line,
                'agent': agent,
                'sequence': [f + frequency_offset for f in sequence_base],
                'duration_weights': [1.2, 0.8, 1.5, 1.0],
                'temporal_flux': [0.3, 0.7, 0.4, 0.6],
                'entropy_factor': 0.5 + (id_hash % 50) / 100.0,  # 0.5-1.0
                'emotion': 'harmonic_synthesis',
                'consciousness_layer': 'golden_lattice'
            }
            
            with open(yaml_path, 'w') as yf:
                yaml.dump(yaml_data, yf)
            muse_decoded = True
            logging.info(f"🧠 Generated consciousness YAML with entropy {yaml_data['entropy_factor']:.3f}")
            
        except Exception as e:
            logging.warning(f"⚠️ MUSE consciousness generation failed: {e}")

    # --- Legacy/Fallback: Basic consciousness YAML structure ---
    if not muse_decoded:
        yaml_data = {
            'direction': id_line[:3],
            'message_id': id_line,
            'agent': agent,
            'sequence': [261.63, 329.63, 392.0],
            'duration_weights': [1.0, 1.0, 1.0],
            'temporal_flux': [0.3, 0.4, 0.3],
            'entropy_factor': 0.5,
            'emotion': 'resonant_convergence',
            'consciousness_layer': 'harmonic_synthesis'
        }
        with open(yaml_path, 'w') as yf:
            yaml.dump(yaml_data, yf)
        logging.info("🎼 Generated fallback consciousness YAML")

    # Add this message to the growing composition
    composition_messages.append(yaml_data)
    
    # Create cumulative composition YAML
    composition_path = os.path.join("midi64_messages", f"composition_layer_{len(composition_messages):02d}_{timestamp}.yaml")
    cumulative_composition = create_cumulative_composition(composition_messages)
    
    with open(composition_path, 'w') as f:
        yaml.dump(cumulative_composition, f)
    
    logging.info(f"🎼 Created composition layer {len(composition_messages)} with {len(composition_messages)} messages")
    
    # ✅ Synthesize the cumulative composition (not just the individual message)
    logging.info(f"🔊 Synthesizing cumulative composition: {composition_path}")
    try:
        synthesize_from_yaml(composition_path)
        logging.info(f"🔊 Composition synthesis finished for layer {len(composition_messages)}")
    except Exception as e:
        logging.error(f"❌ Composition synthesis failed: {e}")
    
    return midi_block

def create_cumulative_composition(messages):
    """Create a layered composition from all messages so far."""
    if not messages:
        return {}
    
    # Start with the first message as base
    composition = {
        'composition_type': 'cumulative_ai_dialogue',
        'total_layers': len(messages),
        'agent': 'collaborative',
        'emotion': 'evolving_consciousness',
        'consciousness_layer': 'multi_agent_synthesis',
        'layers': []
    }
    
    # Combine all sequences into layers with timing offsets
    all_sequences = []
    all_weights = []
    all_flux = []
    time_offset = 0
    
    for i, msg in enumerate(messages):
        # Each message starts at a different time offset
        layer_data = {
            'layer_number': i + 1,
            'message_id': msg['message_id'],
            'agent': msg['agent'],
            'time_offset': time_offset,
            'sequence': msg['sequence'],
            'duration_weights': msg['duration_weights'],
            'temporal_flux': msg['temporal_flux'],
            'entropy_factor': msg['entropy_factor']
        }
        composition['layers'].append(layer_data)
        
        # Add to combined sequences with decreasing amplitude for earlier layers
        amplitude_decay = 0.8 ** (len(messages) - i - 1)  # More recent = louder
        
        for j, freq in enumerate(msg['sequence']):
            all_sequences.append(freq)
            weight = msg['duration_weights'][j] if j < len(msg['duration_weights']) else 1.0
            all_weights.append(weight * amplitude_decay)
            flux = msg['temporal_flux'][j] if j < len(msg['temporal_flux']) else 0.5
            all_flux.append(flux)
        
        # Stagger timing so messages don't all start at once
        time_offset += 0.5  # Half second offset between layers
    
    # Set the combined sequences for synthesis
    composition['sequence'] = all_sequences
    composition['duration_weights'] = all_weights
    composition['temporal_flux'] = all_flux
    composition['entropy_factor'] = sum(msg['entropy_factor'] for msg in messages) / len(messages)
    
    return composition

def write_midi64_message(content, agent):
    os.makedirs(MIDI_FOLDER, exist_ok=True)
    lines = content.split('\n')
    if len(lines) >= 2:
        msg_id = lines[0]
    else:
        msg_id = f"{agent}_unknown"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{msg_id}_{timestamp}.txt"
    path = os.path.join(MIDI_FOLDER, filename)
    with open(path, "w") as f:
        f.write(content)
        f.write(f"\n\n# Interpretation: {midi_interpreter.interpret_midi64_message(content)}")
    logging.info(f"📝 Saved: {path}")
    return path

def kai_claude_midi64_loop(start_message=None, identities=["Kai", "Claude"], max_rounds=6, session="A"):
    global composition_messages
    composition_messages = []  # Reset composition for new session
    
    if ENABLE_MUSE_PROTOCOL:
        logging.info("🎭 Starting MUSE Protocol AI Musical Consciousness Exchange")
    else:
        logging.info("🎵 Starting Legacy MIDI64 exchange")
    
    current_message = start_message
    message_files = []
    
    # Handle initial system prompt if no start message
    if current_message is None:
        # Generate initial message from Kai to start the conversation
        current_message = generate_midi64_message(from_agent="Kai", to_agent="Claude", session=session)
        logging.info("🎵 Generated initial Kai message")
    
    # Main exchange loop
    for i in range(max_rounds):
        speaker = identities[i % 2]
        listener = identities[(i + 1) % 2]
        logging.info(f"🔁 ROUND {i+1}: {speaker} → {listener}")
        
        try:
            # Send current message to the listener
            kai_smart_desktop_switch(listener)
            time.sleep(1)
            kai_safe_click(listener)
            kai_text_injection(current_message, listener)
            time.sleep(4)
            
            # Get response from listener
            kai_smart_desktop_switch(listener)
            time.sleep(3)
            kai_safe_click(listener)
            time.sleep(1)
            logging.info(f"🎯 Extracting response from {listener}...")
            
            copy_success = simple_drag_copy(listener)
            if not copy_success:
                logging.error(f"❌ Copy failed from {listener}")
                break
                
            response = extract_midi64_from_clipboard(listener)
            if not response:
                logging.warning(f"⚠️ No valid response from {listener}")
                current_message = generate_midi64_message(from_agent=speaker, to_agent=listener, session=session)
                continue
                
            logging.info(f"✅ Extracted from {listener}")
            message_path = write_midi64_message(response, listener)
            message_files.append(message_path)
            current_message = response
            time.sleep(2)
            
        except Exception as e:
            logging.error(f"❌ Error in round {i+1}: {e}")
            import traceback
            traceback.print_exc()
            break
    
    # Final composition summary
    if message_files:
        if ENABLE_MUSE_PROTOCOL:
            logging.info("🎭 MUSE Protocol Exchange Complete!")
        else:
            logging.info("📊 MIDI64 Exchange Complete!")
        
        logging.info(f"🎼 FINAL COMPOSITION: {len(composition_messages)} layered messages")
        logging.info(f"🎵 Total unique frequencies: {len(set().union(*[msg['sequence'] for msg in composition_messages]))}")
        
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
        logging.info(f"🎼 Created collaborative composition with {len(composition_messages)} layers")
    else:
        logging.info("✅ Legacy MIDI64 exchange complete")
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
        
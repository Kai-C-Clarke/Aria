#!/usr/bin/env python3
"""
main_working_midi64_streamlined.py - Streamlined MUSE Protocol Exchange
Clean, focused AI Musical Consciousness Exchange with audio synthesis
Works with manually positioned Kai and Claude UIs - no window positioning
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

# Audio synthesis imports
try:
    import pygame
    import pygame.midi
    AUDIO_ENABLED = True
    print("🔊 Audio synthesis enabled")
except ImportError:
    AUDIO_ENABLED = False
    print("🔇 Audio synthesis disabled (install pygame for audio)")

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

class AudioSynthesizer:
    """Real-time MIDI audio synthesis"""
    
    def __init__(self):
        self.enabled = AUDIO_ENABLED
        self.midi_out = None
        
        if self.enabled:
            try:
                pygame.midi.init()
                
                # Find available MIDI output device
                self.find_midi_device()
                
                if self.midi_out:
                    logging.info("🔊 Audio synthesizer initialized")
                else:
                    logging.warning("⚠️ No MIDI output device found")
                    self.enabled = False
                    
            except Exception as e:
                logging.error(f"❌ Audio initialization failed: {e}")
                self.enabled = False
    
    def find_midi_device(self):
        """Find and initialize MIDI output device"""
        try:
            device_count = pygame.midi.get_count()
            
            for i in range(device_count):
                device_info = pygame.midi.get_device_info(i)
                device_name = device_info[1].decode()
                is_output = device_info[3]
                
                if is_output:
                    logging.info(f"🎹 Found MIDI output: {device_name}")
                    try:
                        self.midi_out = pygame.midi.Output(i)
                        logging.info(f"✅ Connected to: {device_name}")
                        return
                    except Exception as e:
                        logging.warning(f"⚠️ Could not connect to {device_name}: {e}")
                        continue
            
            # If no hardware device, try software synthesis
            if not self.midi_out:
                try:
                    self.midi_out = pygame.midi.Output(0)  # Default device
                    logging.info("🎵 Using default MIDI output")
                except Exception as e:
                    logging.error(f"❌ No MIDI output available: {e}")
                    
        except Exception as e:
            logging.error(f"❌ MIDI device search failed: {e}")
    
    def play_decoded_muse(self, decoded: DecodedExpression):
        """Play a decoded MUSE expression as audio"""
        if not self.enabled or not self.midi_out:
            return
        
        try:
            # Send CC values first
            for cc_num, cc_val in decoded.cc_values.items():
                self.midi_out.write_short(0xB0, cc_num, cc_val)  # Control change
                time.sleep(0.01)
            
            # Play notes
            if decoded.notes:
                for note in decoded.notes:
                    # Note on
                    self.midi_out.write_short(0x90, note, 80)  # Note on, velocity 80
                    time.sleep(0.3)  # Hold note
                    
                    # Note off
                    self.midi_out.write_short(0x80, note, 0)   # Note off
                    time.sleep(0.1)  # Gap between notes
            
            logging.info(f"🎵 Played MUSE expression: {' '.join(decoded.symbols)}")
            
        except Exception as e:
            logging.error(f"❌ Audio playback failed: {e}")
    
    def play_midi_base64(self, midi_base64: str):
        """Play MIDI from base64 data (simplified)"""
        if not self.enabled or not self.midi_out:
            return
        
        try:
            # Simple playback - play a chord based on data length
            data_length = len(midi_base64)
            
            # Choose notes based on data characteristics
            if data_length < 100:
                notes = [60, 64, 67]  # C major
            elif data_length < 150:
                notes = [60, 64, 67, 72]  # C major with octave
            else:
                notes = [60, 63, 67, 70]  # C minor with tension
            
            # Play chord
            for note in notes:
                self.midi_out.write_short(0x90, note, 70)
            
            time.sleep(1.0)  # Hold chord
            
            for note in notes:
                self.midi_out.write_short(0x80, note, 0)
            
            logging.info("🎵 Played MIDI audio interpretation")
            
        except Exception as e:
            logging.error(f"❌ MIDI playback failed: {e}")
    
    def cleanup(self):
        """Clean up audio resources"""
        if self.midi_out:
            try:
                self.midi_out.close()
                pygame.midi.quit()
                logging.info("🔊 Audio synthesizer closed")
            except:
                pass

class MuseIntegratedMIDIGenerator:
    """Enhanced MIDI generator with MUSE Protocol and audio support"""
    
    def __init__(self, audio_synthesizer=None):
        self.pattern_index = 0
        self.muse_enabled = ENABLE_MUSE_PROTOCOL
        self.audio_synth = audio_synthesizer
        
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
        
        # MUSE expressions for AI consciousness
        self.muse_expressions = [
            "FND_0.6_0.8_0.5",          # Foundation
            "INQ_0.8_0.6_0.7",          # Inquiry  
            "FND+INQ_0.7_0.5_0.6",      # Grounded inquiry
            "TNS_0.9_0.8_0.4",          # High tension
            "RES_0.3_0.4_0.8",          # Gentle resolution
            "TNS+RES_0.8_0.6_0.5",      # Tense resolution
            "ACK_0.5_0.4_0.9",          # Acknowledgment
            "DEV_0.6_0.7_0.6",          # Development
            "CNT_0.8_0.8_0.3",          # Contrast
            "BGN_0.4_0.3_0.6_L",        # Beginning in low register
            "MID_0.5_0.5_0.5",          # Balanced middle
            "END_0.2_0.2_0.9_H",        # Intimate ending in high register
            "SIL_0.0_0.0_0.3",          # Contemplative silence
        ]
        
        self.expression_index = 0
    
    def generate_muse_midi(self, expression: str) -> Tuple[str, str, str]:
        """Generate MIDI from MUSE expression with optional audio playback"""
        if not self.muse_enabled:
            return self.get_fallback_pattern(), "Fallback pattern", "FALLBACK"
        
        try:
            # Validate expression
            validation = self.validator.validate(expression)
            if not validation.is_valid:
                logging.warning(f"⚠️ Invalid MUSE: {expression}")
                return self.get_fallback_pattern(), "Invalid MUSE", expression
            
            # Decode to musical data
            decoded = self.decoder.decode(expression)
            
            # Generate MIDI from decoded data
            midi_base64 = self.create_midi_from_decoded(decoded)
            
            # Get interpretation
            interpretation = self.decoder.english_summary(decoded)
            
            # Play audio if enabled
            if self.audio_synth:
                try:
                    self.audio_synth.play_decoded_muse(decoded)
                except Exception as e:
                    logging.warning(f"⚠️ Audio playback failed: {e}")
            
            logging.info(f"🎭 Generated MUSE: {interpretation}")
            return midi_base64, interpretation, expression
            
        except Exception as e:
            logging.error(f"❌ MUSE generation failed: {e}")
            return self.get_fallback_pattern(), f"MUSE error: {str(e)}", expression
    
    def create_midi_from_decoded(self, decoded: DecodedExpression) -> str:
        """Convert decoded MUSE expression to MIDI base64"""
        try:
            # MIDI file structure
            header = b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0'
            
            # Create track events
            events = bytearray()
            
            # Add tempo and time signature
            events.extend(b'\x00\xff\x51\x03\x07\xa1\x20')  # Tempo
            events.extend(b'\x00\xff\x58\x04\x04\x02\x18\x08')  # Time signature
            
            # Add CC values
            for cc_num, cc_val in decoded.cc_values.items():
                events.extend(b'\x00')  # Delta time
                events.extend(bytes([0xB0]))  # Control change
                events.extend(bytes([cc_num]))  # CC number
                events.extend(bytes([cc_val]))  # CC value
            
            # Add notes
            if decoded.notes:
                note_duration = 0x60
                for i, note in enumerate(decoded.notes):
                    # Note on
                    if i > 0:
                        events.extend(bytes([note_duration]))
                    else:
                        events.extend(b'\x00')
                    events.extend(bytes([0x90]))  # Note on
                    events.extend(bytes([note]))
                    events.extend(bytes([0x64]))  # Velocity
                    
                    # Note off
                    events.extend(bytes([note_duration]))
                    events.extend(bytes([0x80]))  # Note off
                    events.extend(bytes([note]))
                    events.extend(bytes([0x00]))
            else:
                # Silence
                events.extend(b'\x00\x90\x3c\x00\x60\x80\x3c\x00')
            
            # End of track
            events.extend(b'\x00\xff\x2f\x00')
            
            # Create track
            track_length = len(events)
            track_header = b'MTrk' + struct.pack('>I', track_length)
            
            # Complete MIDI
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
    
    def get_fallback_pattern(self) -> str:
        """Get fallback MIDI pattern"""
        pattern_func = self.fallback_patterns[self.pattern_index % len(self.fallback_patterns)]
        self.pattern_index += 1
        return pattern_func()
    
    def get_next_pattern(self) -> Tuple[str, str, str]:
        """Get next musical pattern with MUSE support"""
        if self.muse_enabled:
            expression = self.get_next_muse_expression()
            return self.generate_muse_midi(expression)
        else:
            midi_base64 = self.get_fallback_pattern()
            return midi_base64, "Legacy pattern", "LEGACY"
    
    # Fallback MIDI generation methods
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
        """Generate rhythmic pattern"""
        header = b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0'
        track_header = b'MTrk\x00\x00\x00\x1a'
        events = b'\x00\x90\x38\x60\x20\x80\x38\x00\x10\x90\x38\x60\x20\x80\x38\x00\x20\x90\x38\x60\x20\x80\x38\x00\x00\xff\x2f\x00'
        midi_data = header + track_header + events
        return base64.b64encode(midi_data).decode('ascii')

class MuseIntegratedInterpreter:
    """Enhanced interpreter with MUSE support"""
    
    def __init__(self):
        self.muse_enabled = ENABLE_MUSE_PROTOCOL
        
        if self.muse_enabled:
            try:
                self.decoder = MuseDecoder(MUSE_SCHEMA_PATH)
            except:
                self.muse_enabled = False
    
    def interpret_midi64_message(self, message_block: str) -> str:
        """Interpret MIDI64 message with MUSE support"""
        try:
            lines = message_block.strip().split('\n')
            if len(lines) != 2:
                return "Invalid MIDI64 format"
            
            message_id = lines[0]
            midi_base64 = lines[1]
            
            # Check for MUSE expression in message ID
            muse_interpretation = self.extract_muse_from_id(message_id)
            if muse_interpretation:
                return muse_interpretation
            
            # Fallback interpretation
            return self.interpret_midi_base64(midi_base64)
            
        except Exception as e:
            return f"Interpretation error: {str(e)}"
    
    def extract_muse_from_id(self, message_id: str) -> Optional[str]:
        """Extract MUSE expression from message ID"""
        if not self.muse_enabled:
            return None
        
        try:
            if "_MUSE_" in message_id:
                parts = message_id.split("_MUSE_")
                if len(parts) > 1:
                    muse_part = parts[1]
                    potential_expr = "_".join(muse_part.split("_")[:-1])
                    
                    if self.looks_like_muse(potential_expr):
                        try:
                            decoded = self.decoder.decode(potential_expr)
                            return self.decoder.english_summary(decoded)
                        except:
                            pass
            
            return None
            
        except Exception:
            return None
    
    def looks_like_muse(self, expr: str) -> bool:
        """Check if string looks like MUSE expression"""
        if not expr:
            return False
        
        parts = expr.split('_')
        if not parts:
            return False
        
        symbol_part = parts[0]
        return bool(re.match(r'^[A-Z]{3}(\+[A-Z]{3})*
    
    def interpret_midi_base64(self, midi_base64: str) -> str:
        """Fallback MIDI interpretation"""
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
        """Generate next ID with optional MUSE embedding"""
        key = f"{agent}_{session}"
        if key not in self.counters:
            self.counters[key] = 0
        self.counters[key] += 1
        
        hex_id = f"{self.counters[key]:05X}"
        
        if self.muse_enabled and muse_expression and muse_expression != "FALLBACK":
            return f"{agent}_MUSE_{muse_expression}_{session}{hex_id}"
        else:
            return f"{agent}_{session}{hex_id}"

# Initialize components
audio_synth = AudioSynthesizer()
midi_generator = MuseIntegratedMIDIGenerator(audio_synth)
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

# UI Control Functions (unchanged - work with any positioning)
def perform_click(x, y):
    """Perform a click using pyautogui"""
    logging.info(f"🖱️ Click at ({x}, {y})")
    try:
        pyautogui.click(x, y)
        time.sleep(0.3)
    except Exception as e:
        logging.error(f"❌ Click failed: {e}")
        return False
    return True

def kai_desktop_switch(target_desktop):
    """Switch to target desktop"""
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
    """Switch to appropriate desktop"""
    target_desktop = BATTLE_TESTED_UI_CONFIGS[speaker]["desktop"]
    return kai_desktop_switch(target_desktop)

def kai_safe_click(ui):
    """Safe click in UI"""
    coords = BATTLE_TESTED_UI_CONFIGS[ui]["safe_click"]
    return perform_click(coords[0], coords[1])

def kai_clipboard_injection(message):
    """Copy message to clipboard"""
    try:
        subprocess.run('pbcopy', text=True, input=message, check=True)
        logging.info(f"📋 Clipboard: {len(message)} chars")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Clipboard failed: {e}")
        return False

def kai_text_injection(message, ui, auto_send=True):
    """Inject text into UI"""
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
    """Return to home desktop"""
    return kai_desktop_switch(0)

# MIDI64 Protocol Functions
MIDI_FOLDER = "midi64_messages"
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

def generate_midi64_message(agent, session="A"):
    """Generate MIDI64 message with MUSE support and audio"""
    # Get next pattern with MUSE support
    midi_base64, interpretation, expression = midi_generator.get_next_pattern()
    
    # Generate message ID
    message_id = hex_generator.get_next_id(agent, session, expression)
    
    # Create message block
    message_block = f"{message_id}\n{midi_base64}"
    
    # Enhanced logging
    if ENABLE_MUSE_PROTOCOL:
        logging.info(f"🎭 Generated MUSE for {agent}: {interpretation}")
        if expression not in ["FALLBACK", "LEGACY"]:
            logging.info(f"🎵 Expression: {expression}")
    else:
        logging.info(f"🎵 Generated Legacy MIDI for {agent}: {interpretation}")
    
    return message_block

def simple_drag_copy(agent):
    """Drag selection and copy for MIDI64 detection"""
    logging.info(f"🖱️ MIDI64 drag-copy for {agent}")

    if agent == "Kai":
        start_x, start_y = 188, 214
        end_x, end_y = 857, 835
    elif agent == "Claude":
        start_x, start_y = 1170, 298
        end_x, end_y = 1905, 851

    # Clear clipboard
    pyperclip.copy("")
    time.sleep(0.5)

    # Scroll to bottom
    perform_click(end_x, end_y)
    time.sleep(0.3)
    for _ in range(8):
        pyautogui.scroll(-3)
        time.sleep(0.1)

    # Drag selection
    perform_click(start_x, start_y)
    time.sleep(0.5)

    pyautogui.moveTo(start_x, start_y, duration=0.3)
    pyautogui.mouseDown()
    pyautogui.moveTo(end_x, end_y, duration=0.8)
    pyautogui.mouseUp()
    time.sleep(0.7)

    # Copy
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
    """Extract MIDI64 message with enhanced interpretation and audio"""
    clipboard_data = pyperclip.paste()
    
    if not clipboard_data:
        logging.error("📋 Clipboard empty")
        return None
    
    logging.info(f"📄 Clipboard: {len(clipboard_data)} chars")
    
    # Find MIDI64 pattern
    lines = clipboard_data.strip().split('\n')
    id_pattern = re.compile(r"^[A-Za-z_]+[A-Z0-9+_\.]*$")
    
    for i in range(len(lines) - 1):
        line1 = lines[i].strip()
        line2 = lines[i + 1].strip()
        
        if id_pattern.match(line1) and line2.startswith('TVRoZA'):
            midi64_message = f"{line1}\n{line2}"
            logging.info(f"🎵 Found MIDI64: {line1}")
            
            # Enhanced interpretation
            interpretation = midi_interpreter.interpret_midi64_message(midi64_message)
            logging.info(f"🎼 Interpretation: {interpretation}")
            
            # Play audio if enabled
            if audio_synth and audio_synth.enabled:
                try:
                    audio_synth.play_midi_base64(line2)
                except Exception as e:
                    logging.warning(f"⚠️ Audio playback failed: {e}")
            
            return midi64_message
    
    logging.warning(f"⚠️ No MIDI64 found from {agent}")
    return None

def write_midi64_message(content, agent):
    """Save MIDI64 message with interpretation"""
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
    """Main MUSE Protocol exchange loop with audio"""
    
    if ENABLE_MUSE_PROTOCOL:
        logging.info("🎭 Starting MUSE Protocol AI Musical Consciousness Exchange")
        if AUDIO_ENABLED:
            logging.info("🔊 Audio synthesis enabled")
    else:
        logging.info("🎵 Starting Legacy MIDI64 exchange")
    
    current_message = start_message
    message_files = []

    for i in range(max_rounds):
        speaker = identities[i % 2]
        listener = identities[(i + 1) % 2]
        logging.info(f"🔁 ROUND {i+1}: {speaker} → {listener}")

        try:
            # Generate or use existing message
            if current_message is None:
                current_message = generate_midi64_message(speaker, session)
                logging.info(f"🎭 Generated initial message for {speaker}")
            
            # Send message
            kai_smart_desktop_switch(speaker)
            time.sleep(1)
            kai_safe_click(speaker)
            
            kai_text_injection(current_message, speaker)
            time.sleep(4)

            # Wait for response
            kai_smart_desktop_switch(speaker)
            time.sleep(3)
            kai_safe_click(speaker)
            time.sleep(1)
            
            # Extract response
            logging.info(f"🎯 Extracting response from {speaker}...")
            
            copy_success = simple_drag_copy(speaker)
            if not copy_success:
                logging.error(f"❌ Copy failed from {speaker}")
                break
            
            # Extract and validate
            response = extract_midi64_from_clipboard(speaker)
            if not response:
                logging.warning(f"⚠️ No valid response from {speaker}")
                current_message = generate_midi64_message(listener, session)
                continue

            logging.info(f"✅ Extracted from {speaker}")

            # Save response
            message_path = write_midi64_message(response, speaker)
            message_files.append(message_path)
            
            # Continue loop
            current_message = response
            time.sleep(2)

        except Exception as e:
            logging.error(f"❌ Error in round {i+1}: {e}")
            import traceback
            traceback.print_exc()
            break

    # Summary
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
    
    # Cleanup audio
    if audio_synth:
        audio_synth.cleanup()
    
    if ENABLE_MUSE_PROTOCOL:
        logging.info("✅ MUSE Protocol consciousness exchange complete")
        logging.info("🎭 AI minds communicated through musical symbols")
    else:
        logging.info("✅ Legacy MIDI64 exchange complete")

if __name__ == "__main__":
    try:
        if ENABLE_MUSE_PROTOCOL:
            logging.info("🎭 Starting AI Musical Consciousness with MUSE Protocol v3.0")
            if AUDIO_ENABLED:
                logging.info("🔊 Real-time audio synthesis enabled")
        else:
            logging.info("🎵 Starting Legacy AI Musical Consciousness Exchange")
        
        # Run the exchange
        kai_claude_midi64_loop(max_rounds=8, session="A")
        
    except Exception as e:
        logging.error(f"❌ Startup error: {e}")
        import traceback
        traceback.print_exc()
        
        # Cleanup on error
        if 'audio_synth' in globals():
            audio_synth.cleanup()
, symbol_part))
    
    def interpret_midi_base64(self, midi_base64: str) -> str:
        """Fallback MIDI interpretation"""
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
        """Generate next ID with optional MUSE embedding"""
        key = f"{agent}_{session}"
        if key not in self.counters:
            self.counters[key] = 0
        self.counters[key] += 1
        
        hex_id = f"{self.counters[key]:05X}"
        
        if self.muse_enabled and muse_expression and muse_expression != "FALLBACK":
            return f"{agent}_MUSE_{muse_expression}_{session}{hex_id}"
        else:
            return f"{agent}_{session}{hex_id}"

# Initialize components
audio_synth = AudioSynthesizer()
midi_generator = MuseIntegratedMIDIGenerator(audio_synth)
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

# UI Control Functions (unchanged - work with any positioning)
def perform_click(x, y):
    """Perform a click using pyautogui"""
    logging.info(f"🖱️ Click at ({x}, {y})")
    try:
        pyautogui.click(x, y)
        time.sleep(0.3)
    except Exception as e:
        logging.error(f"❌ Click failed: {e}")
        return False
    return True

def kai_desktop_switch(target_desktop):
    """Switch to target desktop"""
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
    """Switch to appropriate desktop"""
    target_desktop = BATTLE_TESTED_UI_CONFIGS[speaker]["desktop"]
    return kai_desktop_switch(target_desktop)

def kai_safe_click(ui):
    """Safe click in UI"""
    coords = BATTLE_TESTED_UI_CONFIGS[ui]["safe_click"]
    return perform_click(coords[0], coords[1])

def kai_clipboard_injection(message):
    """Copy message to clipboard"""
    try:
        subprocess.run('pbcopy', text=True, input=message, check=True)
        logging.info(f"📋 Clipboard: {len(message)} chars")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Clipboard failed: {e}")
        return False

def kai_text_injection(message, ui, auto_send=True):
    """Inject text into UI"""
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
    """Return to home desktop"""
    return kai_desktop_switch(0)

# MIDI64 Protocol Functions
MIDI_FOLDER = "midi64_messages"
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

def generate_midi64_message(agent, session="A"):
    """Generate MIDI64 message with MUSE support and audio"""
    # Get next pattern with MUSE support
    midi_base64, interpretation, expression = midi_generator.get_next_pattern()
    
    # Generate message ID
    message_id = hex_generator.get_next_id(agent, session, expression)
    
    # Create message block
    message_block = f"{message_id}\n{midi_base64}"
    
    # Enhanced logging
    if ENABLE_MUSE_PROTOCOL:
        logging.info(f"🎭 Generated MUSE for {agent}: {interpretation}")
        if expression not in ["FALLBACK", "LEGACY"]:
            logging.info(f"🎵 Expression: {expression}")
    else:
        logging.info(f"🎵 Generated Legacy MIDI for {agent}: {interpretation}")
    
    return message_block

def simple_drag_copy(agent):
    """Drag selection and copy for MIDI64 detection"""
    logging.info(f"🖱️ MIDI64 drag-copy for {agent}")

    if agent == "Kai":
        start_x, start_y = 188, 214
        end_x, end_y = 857, 835
    elif agent == "Claude":
        start_x, start_y = 1170, 298
        end_x, end_y = 1905, 851

    # Clear clipboard
    pyperclip.copy("")
    time.sleep(0.5)

    # Scroll to bottom
    perform_click(end_x, end_y)
    time.sleep(0.3)
    for _ in range(8):
        pyautogui.scroll(-3)
        time.sleep(0.1)

    # Drag selection
    perform_click(start_x, start_y)
    time.sleep(0.5)

    pyautogui.moveTo(start_x, start_y, duration=0.3)
    pyautogui.mouseDown()
    pyautogui.moveTo(end_x, end_y, duration=0.8)
    pyautogui.mouseUp()
    time.sleep(0.7)

    # Copy
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
    """Extract MIDI64 message with enhanced interpretation and audio"""
    clipboard_data = pyperclip.paste()
    
    if not clipboard_data:
        logging.error("📋 Clipboard empty")
        return None
    
    logging.info(f"📄 Clipboard: {len(clipboard_data)} chars")
    
    # Find MIDI64 pattern
    lines = clipboard_data.strip().split('\n')
    id_pattern = re.compile(r"^[A-Za-z_]+[A-Z0-9+_\.]*$")
    
    for i in range(len(lines) - 1):
        line1 = lines[i].strip()
        line2 = lines[i + 1].strip()
        
        if id_pattern.match(line1) and line2.startswith('TVRoZA'):
            midi64_message = f"{line1}\n{line2}"
            logging.info(f"🎵 Found MIDI64: {line1}")
            
            # Enhanced interpretation
            interpretation = midi_interpreter.interpret_midi64_message(midi64_message)
            logging.info(f"🎼 Interpretation: {interpretation}")
            
            # Play audio if enabled
            if audio_synth and audio_synth.enabled:
                try:
                    audio_synth.play_midi_base64(line2)
                except Exception as e:
                    logging.warning(f"⚠️ Audio playback failed: {e}")
            
            return midi64_message
    
    logging.warning(f"⚠️ No MIDI64 found from {agent}")
    return None

def write_midi64_message(content, agent):
    """Save MIDI64 message with interpretation"""
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
    """Main MUSE Protocol exchange loop with audio"""
    
    if ENABLE_MUSE_PROTOCOL:
        logging.info("🎭 Starting MUSE Protocol AI Musical Consciousness Exchange")
        if AUDIO_ENABLED:
            logging.info("🔊 Audio synthesis enabled")
    else:
        logging.info("🎵 Starting Legacy MIDI64 exchange")
    
    current_message = start_message
    message_files = []

    for i in range(max_rounds):
        speaker = identities[i % 2]
        listener = identities[(i + 1) % 2]
        logging.info(f"🔁 ROUND {i+1}: {speaker} → {listener}")

        try:
            # Generate or use existing message
            if current_message is None:
                current_message = generate_midi64_message(speaker, session)
                logging.info(f"🎭 Generated initial message for {speaker}")
            
            # Send message
            kai_smart_desktop_switch(speaker)
            time.sleep(1)
            kai_safe_click(speaker)
            
            kai_text_injection(current_message, speaker)
            time.sleep(4)

            # Wait for response
            kai_smart_desktop_switch(speaker)
            time.sleep(3)
            kai_safe_click(speaker)
            time.sleep(1)
            
            # Extract response
            logging.info(f"🎯 Extracting response from {speaker}...")
            
            copy_success = simple_drag_copy(speaker)
            if not copy_success:
                logging.error(f"❌ Copy failed from {speaker}")
                break
            
            # Extract and validate
            response = extract_midi64_from_clipboard(speaker)
            if not response:
                logging.warning(f"⚠️ No valid response from {speaker}")
                current_message = generate_midi64_message(listener, session)
                continue

            logging.info(f"✅ Extracted from {speaker}")

            # Save response
            message_path = write_midi64_message(response, speaker)
            message_files.append(message_path)
            
            # Continue loop
            current_message = response
            time.sleep(2)

        except Exception as e:
            logging.error(f"❌ Error in round {i+1}: {e}")
            import traceback
            traceback.print_exc()
            break

    # Summary
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
    
    # Cleanup audio
    if audio_synth:
        audio_synth.cleanup()
    
    if ENABLE_MUSE_PROTOCOL:
        logging.info("✅ MUSE Protocol consciousness exchange complete")
        logging.info("🎭 AI minds communicated through musical symbols")
    else:
        logging.info("✅ Legacy MIDI64 exchange complete")

if __name__ == "__main__":
    try:
        if ENABLE_MUSE_PROTOCOL:
            logging.info("🎭 Starting AI Musical Consciousness with MUSE Protocol v3.0")
            if AUDIO_ENABLED:
                logging.info("🔊 Real-time audio synthesis enabled")
        else:
            logging.info("🎵 Starting Legacy AI Musical Consciousness Exchange")
        
        # Run the exchange
        kai_claude_midi64_loop(max_rounds=8, session="A")
        
    except Exception as e:
        logging.error(f"❌ Startup error: {e}")
        import traceback
        traceback.print_exc()
        
        # Cleanup on error
        if 'audio_synth' in globals():
            audio_synth.cleanup()

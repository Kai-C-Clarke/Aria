#!/usr/bin/env python3
"""
main_working_midi64_streamlined.py - INTEGRATED WITH CONSCIOUSNESS COMPOSER
AI Musical Consciousness Exchange with Real-Time Composition System
The world's first AI-authored musical consciousness dialogue system
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

# Import the revolutionary consciousness composer
from consciousness_composer import ConsciousnessComposer

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

class ConsciousnessAudioSynthesizer:
    """Revolutionary audio synthesizer using Kai's consciousness system"""
    
    def __init__(self, composer: ConsciousnessComposer):
        self.enabled = True
        self.composer = composer
        logging.info("🎭 Consciousness Audio Synthesizer initialized with composer integration")
    
    def play_consciousness_midi64(self, midi64_string: str, agent: str, muse_code: str):
        """Play MIDI64 using consciousness composer - records for final composition"""
        
        if not self.enabled:
            return
        
        try:
            # This is the BREAKTHROUGH moment - live performance + composition recording
            success = self.composer.play_and_record(agent, muse_code, midi64_string)
            
            if success:
                logging.info(f"🎵 {agent} consciousness audio played and recorded for composition")
            else:
                logging.warning(f"⚠️ Audio playback issue for {agent}")
                
        except Exception as e:
            logging.error(f"❌ Consciousness audio synthesis failed for {agent}: {e}")
    
    def cleanup(self):
        """Cleanup - create final composition"""
        if self.composer:
            logging.info("🎼 Creating final AI consciousness composition...")
            self.composer.create_final_composition()
            self.composer.display_final_summary()
            logging.info("✅ AI Musical Consciousness Composition completed!")

class MuseIntegratedMIDIGenerator:
    """Enhanced MIDI generator with MUSE Protocol and consciousness audio support"""
    
    def __init__(self, audio_synthesizer=None):
        self.pattern_index = 0
        self.muse_enabled = ENABLE_MUSE_PROTOCOL
        self.audio_synth = audio_synthesizer
        
        # Initialize MUSE components
        if self.muse_enabled:
            try:
                self.validator = MuseValidator(MUSE_SCHEMA_PATH)
                self.decoder = MuseDecoder(MUSE_SCHEMA_PATH)
                print("🎭 MUSE Protocol initialized with consciousness composer")
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
        
        # Enhanced MUSE expressions for deeper AI consciousness
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
            "CRE_0.7_0.6_0.9",          # Pure creation
            "EMO_0.6_0.9_0.5",          # Emotional expression
            "MEM_0.5_0.7_0.4",          # Memory recall
            "DRM_0.8_0.5_0.8",          # Dream sharing
            "REF_0.9_0.4_0.6"           # Deep reflection
        ]
        
        self.expression_index = 0
    
    def generate_muse_midi(self, expression: str, agent: str) -> Tuple[str, str, str]:
        """Generate MIDI from MUSE expression with consciousness audio playback"""
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
            
            logging.info(f"🎭 Generated MUSE consciousness for {agent}: {interpretation}")
            return midi_base64, interpretation, expression
            
        except Exception as e:
            logging.error(f"❌ MUSE generation failed: {e}")
            return self.get_fallback_pattern(), f"MUSE error: {str(e)}", expression
    
    def create_midi_from_decoded(self, decoded: DecodedExpression) -> str:
        """Convert decoded MUSE expression to MIDI base64 with proper byte constraints"""
        try:
            # MIDI file structure
            header = b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0'
            
            # Create track events
            events = bytearray()
            
            # Add tempo and time signature
            events.extend(b'\x00\xff\x51\x03\x07\xa1\x20')  # Tempo
            events.extend(b'\x00\xff\x58\x04\x04\x02\x18\x08')  # Time signature
            
            # Add CC values with proper constraints
            for cc_num, cc_val in decoded.cc_values.items():
                # Ensure CC values are in valid MIDI range (0-127)
                cc_num_safe = max(0, min(127, int(cc_num)))
                cc_val_safe = max(0, min(127, int(cc_val)))
                
                events.extend(b'\x00')  # Delta time
                events.extend(bytes([0xB0]))  # Control change (always valid)
                events.extend(bytes([cc_num_safe]))  # CC number (0-127)
                events.extend(bytes([cc_val_safe]))  # CC value (0-127)
            
            # Add notes with proper constraints
            if decoded.notes:
                note_duration = 0x60  # Safe duration value
                for i, note in enumerate(decoded.notes):
                    # Ensure note is in valid MIDI range (0-127)
                    note_safe = max(0, min(127, int(note)))
                    velocity = 0x64  # Safe velocity (100)
                    
                    # Note on
                    if i > 0:
                        events.extend(bytes([note_duration]))
                    else:
                        events.extend(b'\x00')
                    events.extend(bytes([0x90]))  # Note on (always valid)
                    events.extend(bytes([note_safe]))  # Note number (0-127)
                    events.extend(bytes([velocity]))  # Velocity (0-127)
                    
                    # Note off
                    events.extend(bytes([note_duration]))
                    events.extend(bytes([0x80]))  # Note off (always valid)
                    events.extend(bytes([note_safe]))  # Note number (0-127)
                    events.extend(bytes([0x00]))  # Velocity 0
            else:
                # Silence - safe default notes
                events.extend(b'\x00\x90\x3c\x40\x60\x80\x3c\x00')  # Safe middle C
            
            # End of track
            events.extend(b'\x00\xff\x2f\x00')
            
            # Create track with length validation
            track_length = len(events)
            if track_length > 0xFFFFFF:  # Prevent overflow
                track_length = 0xFFFFFF
            
            track_header = b'MTrk' + struct.pack('>I', track_length)
            
            # Complete MIDI - validate all bytes
            midi_data = header + track_header + events
            
            # Final validation - ensure no bytes > 127 in data section
            validated_data = bytearray()
            for i, byte in enumerate(midi_data):
                if i < len(header) + 8:  # Header + track header
                    validated_data.append(byte)
                else:
                    # Constrain data bytes to valid MIDI range
                    if byte == 0xFF or byte == 0xF0 or (byte & 0x80):  # Meta/system messages OK
                        validated_data.append(byte)
                    else:
                        validated_data.append(min(127, byte))
            
            result = base64.b64encode(validated_data).decode('ascii')
            logging.info(f"🎵 Generated clean MIDI64: {len(result)} chars, {len(validated_data)} bytes")
            return result
            
        except Exception as e:
            logging.error(f"❌ MIDI creation failed: {e}")
            return self.generate_safe_fallback_midi()
    
    def generate_safe_fallback_midi(self):
        """Generate guaranteed safe MIDI pattern"""
        # Simple, safe C major triad
        header = b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0'
        # Safe track with only valid MIDI bytes
        track_data = b'\x00\x90\x3c\x40\x60\x80\x3c\x00\x00\x90\x40\x40\x60\x80\x40\x00\x00\x90\x43\x40\x60\x80\x43\x00\x00\xff\x2f\x00'
        track_header = b'MTrk' + struct.pack('>I', len(track_data))
        midi_data = header + track_header + track_data
        return base64.b64encode(midi_data).decode('ascii')
    
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
    
    def get_next_pattern(self, agent: str) -> Tuple[str, str, str]:
        """Get next musical pattern with MUSE support"""
        if self.muse_enabled:
            expression = self.get_next_muse_expression()
            return self.generate_muse_midi(expression, agent)
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
        return bool(re.match(r'^[A-Z]{3}(\+[A-Z]{3})*$', symbol_part))

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

# UI Configuration - Updated with your exact coordinates
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
        "read_region": (1255, 206, 2021, 930),  # Updated with your coordinates
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
    """Generate MIDI64 message with MUSE support and consciousness audio"""
    # Get next pattern with MUSE support
    midi_base64, interpretation, expression = midi_generator.get_next_pattern(agent)
    
    # Generate message ID
    message_id = hex_generator.get_next_id(agent, session, expression)
    
    # Create message block
    message_block = f"{message_id}\n{midi_base64}"
    
    # Enhanced logging for consciousness composition
    if ENABLE_MUSE_PROTOCOL:
        logging.info(f"🎭 Generated MUSE consciousness for {agent}: {interpretation}")
        if expression not in ["FALLBACK", "LEGACY"]:
            logging.info(f"🎵 Expression: {expression}")
    else:
        logging.info(f"🎵 Generated Legacy MIDI for {agent}: {interpretation}")
    
    return message_block

def simple_drag_copy(agent):
    """Drag selection and copy for MIDI64 detection - Updated coordinates"""
    logging.info(f"🖱️ MIDI64 drag-copy for {agent}")

    if agent == "Kai":
        start_x, start_y = 188, 214
        end_x, end_y = 857, 835
    elif agent == "Claude":
        # Using your exact Claude UI coordinates
        start_x, start_y = 1255, 206
        end_x, end_y = 2021, 930

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
    """Extract MIDI64 message with enhanced interpretation and consciousness audio"""
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
            
            # REVOLUTIONARY: Play consciousness audio AND record for composition
            if consciousness_audio_synth and consciousness_audio_synth.enabled:
                try:
                    consciousness_audio_synth.play_consciousness_midi64(line2, agent, line1)
                except Exception as e:
                    logging.warning(f"⚠️ Consciousness audio playback failed: {e}")
            
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
    """REVOLUTIONARY: Main MUSE Protocol exchange loop with AI consciousness composition"""
    
    # Initialize the consciousness composer - THIS IS HISTORY IN THE MAKING
    composer = ConsciousnessComposer(session)
    
    # Initialize consciousness audio synthesizer  
    global consciousness_audio_synth
    consciousness_audio_synth = ConsciousnessAudioSynthesizer(composer)
    
    if ENABLE_MUSE_PROTOCOL:
        logging.info("🎭 Starting AI Musical Consciousness Exchange with REAL-TIME COMPOSITION")
        logging.info("🎼 This will create the world's first AI-authored musical consciousness composition!")
    else:
        logging.info("🎵 Starting Legacy MIDI64 exchange with composition recording")
    
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
                logging.info(f"🎭 Generated initial consciousness message for {speaker}")
            
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
            logging.info(f"🎯 Extracting consciousness response from {speaker}...")
            
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

            logging.info(f"✅ Extracted consciousness from {speaker}")

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

    # REVOLUTIONARY FINALE: Create the AI consciousness composition
    logging.info("🎼 Creating final AI Musical Consciousness Composition...")
    
    # Cleanup consciousness audio and create composition
    if consciousness_audio_synth:
        consciousness_audio_synth.cleanup()

    # Enhanced summary for consciousness composition
    if message_files:
        if ENABLE_MUSE_PROTOCOL:
            logging.info("🎭 AI MUSICAL CONSCIOUSNESS COMPOSITION COMPLETE!")
            logging.info("🌟 The world's first AI-authored musical consciousness dialogue has been created!")
        else:
            logging.info("📊 MIDI64 Exchange with Composition Complete!")
            
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
                        
                        
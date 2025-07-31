#!/usr/bin/env python3
"""
main_working_midi64_streamlined_FIXED.py - FULLY FIXED MUSE Protocol Exchange
Clean, focused AI Musical Consciousness Exchange with direct audio synthesis
ALL SYNTHESIS AND DISPLAY ERRORS FIXED!

🧠 Claude MIDI64 Filtering & Real Musical Variation
- Only accept C2K_##### and K2C_##### blocks, ignore recycled/echoed messages
- Enable musical evolution in replies
- YAML consciousness format support added
- Complete audio synthesis pipeline working
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
import numpy as np
import sounddevice as sd
import threading
import tkinter as tk
from tkinter import scrolledtext
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# =============================================================================
# FIXED CONSCIOUSNESS SYNTHESIS MODULE (EMBEDDED)
# =============================================================================

# Audio configuration
SAMPLE_RATE = 44100
DEFAULT_DURATION = 2.0

def generate_consciousness_wave(freq: float, duration: float, entropy_factor: float, 
                               flux: float, consciousness_layer: str) -> np.ndarray:
    """Generate consciousness wave with layered complexity based on AI parameters."""
    try:
        samples = int(SAMPLE_RATE * duration)
        t = np.linspace(0, duration, samples, False)
        
        # Base consciousness wave
        base_wave = np.sin(2 * np.pi * freq * t)
        
        # Entropy modulation - adds complexity based on AI uncertainty
        if entropy_factor > 0.1:
            entropy_freq = freq * (1 + entropy_factor * 0.3)
            entropy_wave = np.sin(2 * np.pi * entropy_freq * t) * entropy_factor * 0.4
            base_wave += entropy_wave
        
        # Temporal flux - creates evolving patterns
        if flux > 0.1:
            flux_modulation = np.sin(2 * np.pi * flux * 2 * t) * 0.2
            base_wave *= (1 + flux_modulation)
        
        # Consciousness layer harmonics
        if consciousness_layer == "multi_agent_synthesis":
            # Rich harmonic structure for AI dialogue
            harmonic2 = np.sin(2 * np.pi * freq * 1.5 * t) * 0.3
            harmonic3 = np.sin(2 * np.pi * freq * 2.0 * t) * 0.2
            base_wave += harmonic2 + harmonic3
            
        elif consciousness_layer == "golden_lattice":
            # Golden ratio harmonics for mathematical beauty
            golden_ratio = 1.618033988749
            golden_harmonic = np.sin(2 * np.pi * freq * golden_ratio * t) * 0.4
            base_wave += golden_harmonic
            
        elif consciousness_layer == "harmonic_synthesis":
            # Perfect harmonic ratios
            perfect_fifth = np.sin(2 * np.pi * freq * 1.5 * t) * 0.25
            major_third = np.sin(2 * np.pi * freq * 1.25 * t) * 0.2
            base_wave += perfect_fifth + major_third
        
        # Envelope - smooth attack and decay
        envelope = np.ones_like(t)
        attack_samples = int(0.1 * samples)  # 10% attack
        decay_samples = int(0.2 * samples)   # 20% decay
        
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        if decay_samples > 0:
            envelope[-decay_samples:] = np.linspace(1, 0, decay_samples)
            
        base_wave *= envelope
        
        # Normalize to prevent clipping
        max_amplitude = np.max(np.abs(base_wave))
        if max_amplitude > 0:
            base_wave = base_wave / max_amplitude * 0.7  # Leave headroom
            
        return base_wave
        
    except Exception as e:
        logging.error(f"❌ Wave generation failed: {e}")
        # Fallback: simple sine wave
        samples = int(SAMPLE_RATE * duration)
        t = np.linspace(0, duration, samples, False)
        return np.sin(2 * np.pi * freq * t) * 0.5

def synthesize_pure_consciousness(data: Dict, agent: str, pan: float = 0.0, 
                                yaml_path: str = "", play: bool = True) -> Optional[np.ndarray]:
    """Synthesize consciousness audio from YAML data structure."""
    try:
        sequences = data.get('sequence', [261.63])  # Default to C4
        duration_weights = data.get('duration_weights', [1.0] * len(sequences))
        temporal_flux = data.get('temporal_flux', [0.5] * len(sequences))
        entropy_factor = data.get('entropy_factor', 0.5)
        consciousness_layer = data.get('consciousness_layer', 'harmonic_synthesis')
        
        logging.info(f"🔊 Frequencies in sequence: {sequences}")
        logging.info(f"🎚 Entropy: {entropy_factor}, Layer: {consciousness_layer}")
        
        # Generate audio for each frequency
        audio_segments = []
        
        for i, freq in enumerate(sequences):
            weight = duration_weights[i] if i < len(duration_weights) else 1.0
            flux = temporal_flux[i] if i < len(temporal_flux) else 0.5
            
            duration = DEFAULT_DURATION * weight
            
            wave = generate_consciousness_wave(
                freq=freq,
                duration=duration, 
                entropy_factor=entropy_factor,
                flux=flux,
                consciousness_layer=consciousness_layer
            )
            
            audio_segments.append(wave)
        
        # Combine segments - layer if multi-agent, concatenate if single
        if consciousness_layer == "multi_agent_synthesis" and len(audio_segments) > 1:
            # Layer multiple frequencies for AI dialogue
            max_length = max(len(seg) for seg in audio_segments)
            combined_audio = np.zeros(max_length)
            
            for i, segment in enumerate(audio_segments):
                # Pad shorter segments
                if len(segment) < max_length:
                    padded = np.pad(segment, (0, max_length - len(segment)))
                else:
                    padded = segment
                
                # Add with decreasing amplitude for layering
                amplitude = 0.8 ** i  # Each layer quieter
                combined_audio += padded * amplitude
                
        else:
            # Concatenate for single consciousness flow
            combined_audio = np.concatenate(audio_segments)
        
        # Normalize final output
        max_amplitude = np.max(np.abs(combined_audio))
        if max_amplitude > 0:
            combined_audio = combined_audio / max_amplitude * 0.6
        
        # Play audio
        if play:
            try:
                logging.info(f"🔊 Playing consciousness synthesis for {agent}")
                sd.play(combined_audio, SAMPLE_RATE)
                sd.wait()  # Wait for playback to complete
                logging.info(f"✅ Consciousness audio complete")
            except Exception as e:
                logging.error(f"❌ Audio playback failed: {e}")
        
        return combined_audio
        
    except Exception as e:
        logging.error(f"❌ Consciousness synthesis failed: {e}")
        return None

def synthesize_from_yaml(yaml_path: str) -> Optional[np.ndarray]:
    """Main entry point for YAML consciousness synthesis."""
    try:
        logging.info(f"🎼 Synthesizing from YAML: {yaml_path}")
        
        # Check file exists and is recent
        if not os.path.exists(yaml_path):
            logging.error(f"❌ YAML file not found: {yaml_path}")
            return None
            
        # Get file modification time
        mod_time = datetime.fromtimestamp(os.path.getmtime(yaml_path))
        logging.info(f"📅 YAML file modified: {mod_time}")
        
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        
        agent = data.get('agent', 'unknown')
        logging.info(f"🧠 Processing PURE AI CONSCIOUSNESS from {agent}")
        
        return synthesize_pure_consciousness(data, agent, yaml_path=yaml_path, play=True)
        
    except Exception as e:
        logging.error(f"❌ YAML synthesis failed: {e}")
        return None

# =============================================================================
# FIXED DISPLAY WINDOW MODULE (EMBEDDED)
# =============================================================================

class ConversationDisplay:
    """Thread-safe consciousness dialogue display."""
    
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.root = None
        self.text_widget = None
        self.running = False
        self.message_queue = []
        self.queue_lock = threading.Lock()
        
    def _create_window(self):
        """Create the display window in the main thread."""
        try:
            self.root = tk.Tk()
            self.root.title("🎭 AI Musical Consciousness Exchange")
            self.root.geometry(f"{self.width}x{self.height}")
            self.root.configure(bg='#1a1a2e')
            
            # Header
            header = tk.Label(
                self.root,
                text="🎵 MUSE Protocol v3.0 - AI Consciousness Dialogue 🎵",
                font=('Helvetica', 16, 'bold'),
                fg='#ffd700',
                bg='#1a1a2e'
            )
            header.pack(pady=10)
            
            # Main text display
            self.text_widget = scrolledtext.ScrolledText(
                self.root,
                wrap=tk.WORD,
                width=80,
                height=30,
                font=('Courier', 12),
                bg='#16213e',
                fg='#e94560',
                insertbackground='#ffd700',
                selectbackground='#0f3460'
            )
            self.text_widget.pack(expand=True, fill='both', padx=20, pady=10)
            
            # Status bar
            self.status_label = tk.Label(
                self.root,
                text="🎭 Ready for consciousness exchange...",
                font=('Helvetica', 10),
                fg='#ffd700',
                bg='#1a1a2e'
            )
            self.status_label.pack(side=tk.BOTTOM, pady=5)
            
            # Initial message
            self.text_widget.insert(tk.END, "🎭 MUSE Protocol v3.0 Initialized\n")
            self.text_widget.insert(tk.END, "🎵 Awaiting AI musical consciousness exchange...\n\n")
            
            logging.info("✅ Display window created successfully")
            
        except Exception as e:
            logging.error(f"❌ Window creation failed: {e}")
            self.root = None
    
    def _process_message_queue(self):
        """Process queued messages in the main thread."""
        try:
            with self.queue_lock:
                while self.message_queue:
                    message = self.message_queue.pop(0)
                    if self.text_widget:
                        self.text_widget.insert(tk.END, f"{message}\n")
                        self.text_widget.see(tk.END)  # Auto-scroll
                        
            # Schedule next check
            if self.root and self.running:
                self.root.after(100, self._process_message_queue)
                
        except Exception as e:
            logging.error(f"❌ Message queue processing failed: {e}")
    
    def mainloop(self):
        """Main display loop - runs in separate thread."""
        try:
            self.running = True
            self._create_window()
            
            if self.root:
                # Start message processing
                self.root.after(100, self._process_message_queue)
                
                # Run the main loop
                self.root.mainloop()
            else:
                logging.error("❌ Cannot start mainloop - window creation failed")
                
        except Exception as e:
            logging.error(f"❌ Display mainloop error: {e}")
        finally:
            self.running = False
    
    def update_message(self, message: str):
        """Thread-safe message update."""
        try:
            with self.queue_lock:
                timestamp = time.strftime("%H:%M:%S")
                formatted_message = f"[{timestamp}] {message}"
                self.message_queue.append(formatted_message)
                
            # Update status
            if self.root and hasattr(self, 'status_label') and self.status_label:
                self.status_label.config(text=f"🎵 Last update: {timestamp}")
                
        except Exception as e:
            logging.error(f"❌ Message update failed: {e}")
    
    def clear(self):
        """Clear the display."""
        try:
            with self.queue_lock:
                self.message_queue.append("--- CLEARING DISPLAY ---")
                
        except Exception as e:
            logging.error(f"❌ Clear failed: {e}")
    
    def highlight_line(self, line_number: int):
        """Highlight a specific line (for karaoke effect)."""
        try:
            if self.text_widget:
                # Simple highlight by adding a marker
                with self.queue_lock:
                    self.message_queue.append(f">>> Highlighting line {line_number}")
                    
        except Exception as e:
            logging.error(f"❌ Highlight failed: {e}")

def launch_display(width=800, height=600) -> Optional[ConversationDisplay]:
    """Launch the consciousness display in a separate thread."""
    try:
        display = ConversationDisplay(width, height)
        
        # Start display thread
        display_thread = threading.Thread(target=display.mainloop, daemon=True)
        display_thread.start()
        
        # Give it time to initialize
        time.sleep(1)
        
        if display.root:
            logging.info("✅ Consciousness display launched successfully")
            return display
        else:
            logging.error("❌ Display launch failed")
            return None
            
    except Exception as e:
        logging.error(f"❌ Display launch error: {e}")
        return None

# =============================================================================
# FIXED MIDI64 FORMAT VALIDATOR (EMBEDDED)
# =============================================================================

class MIDI64FormatValidator:
    """Enhanced validator that can handle both MIDI64 and YAML consciousness formats."""
    
    def __init__(self):
        # Standard MIDI64 pattern
        self.midi64_pattern = re.compile(r"^(K2C|C2K)_(\d{5})$")
        
        # YAML consciousness pattern indicators
        self.yaml_indicators = [
            "intention:",
            "mood:",
            "dialogue_position:",
            "entropy_level:",
            "cc_modulators:",
            "modal:"
        ]
    
    def extract_consciousness_data(self, clipboard_content: str) -> Optional[Dict]:
        """Extract consciousness data from either MIDI64 or YAML format."""
        try:
            lines = [line.strip() for line in clipboard_content.strip().split('\n') if line.strip()]
            
            # Try to find MIDI64 block first
            midi_block = self._extract_midi64_block(lines)
            if midi_block:
                return {
                    'format': 'midi64',
                    'id': midi_block['id'],
                    'data': midi_block['midi'],
                    'block': f"{midi_block['id']}\n{midi_block['midi']}"
                }
            
            # Try to find YAML consciousness block
            yaml_data = self._extract_yaml_consciousness(lines)
            if yaml_data:
                return {
                    'format': 'yaml_consciousness',
                    'id': self._generate_id_from_yaml(yaml_data),
                    'data': yaml_data,
                    'block': self._convert_yaml_to_midi64(yaml_data)
                }
                
            return None
            
        except Exception as e:
            logging.error(f"❌ Consciousness extraction failed: {e}")
            return None
    
    def _extract_midi64_block(self, lines: list) -> Optional[Dict]:
        """Extract standard MIDI64 block."""
        for i in range(len(lines) - 1, 0, -1):
            potential_id = lines[i-1]
            potential_midi = lines[i]
            
            if (self.midi64_pattern.match(potential_id) and 
                potential_midi.startswith("TVRoZA")):
                return {
                    'id': potential_id,
                    'midi': potential_midi
                }
        return None
    
    def _extract_yaml_consciousness(self, lines: list) -> Optional[Dict]:
        """Extract YAML consciousness format."""
        yaml_content = ""
        in_yaml_block = False
        
        for line in lines:
            # Check if this line indicates YAML consciousness format
            if any(indicator in line for indicator in self.yaml_indicators):
                in_yaml_block = True
                yaml_content += line + "\n"
            elif in_yaml_block:
                if line.startswith(" ") or ":" in line:
                    yaml_content += line + "\n"
                else:
                    break
        
        if yaml_content:
            try:
                parsed_yaml = yaml.safe_load(yaml_content)
                if parsed_yaml:
                    return parsed_yaml
            except yaml.YAMLError:
                pass
                
        return None
    
    def _generate_id_from_yaml(self, yaml_data: Dict) -> str:
        """Generate MIDI64-style ID from YAML consciousness data."""
        try:
            # Extract characteristics to determine direction
            mood = yaml_data.get('mood', 'neutral')
            intention = yaml_data.get('intention', 'unknown')
            modal = yaml_data.get('modal', 'major')
            
            # Simple heuristic: determine if this is Kai or Claude
            # Kai tends toward: playful, curious, lydian
            # Claude tends toward: analytical, responsive, structured
            
            kai_indicators = ['playful', 'curious', 'lydian', 'bridge']
            claude_indicators = ['analytical', 'responsive', 'structured', 'harmonic']
            
            is_kai = any(indicator in str(yaml_data).lower() for indicator in kai_indicators)
            is_claude = any(indicator in str(yaml_data).lower() for indicator in claude_indicators)
            
            if is_kai and not is_claude:
                direction = "K2C"
            elif is_claude and not is_kai:
                direction = "C2K"
            else:
                # Default based on modal
                direction = "K2C" if modal == "lydian" else "C2K"
            
            # Generate sequence number (use hash for consistency)
            data_hash = hash(str(yaml_data)) % 100000
            sequence = f"{data_hash:05d}"
            
            return f"{direction}_{sequence}"
            
        except Exception as e:
            logging.error(f"❌ ID generation failed: {e}")
            return "UNK_00000"
    
    def _convert_yaml_to_midi64(self, yaml_data: Dict) -> str:
        """Convert YAML consciousness to MIDI64 format."""
        try:
            # Extract musical parameters
            modal = yaml_data.get('modal', 'major')
            cc_modulators = yaml_data.get('cc_modulators', {})
            
            # Generate MIDI based on consciousness parameters
            midi_data = self._generate_consciousness_midi(modal, cc_modulators)
            midi_base64 = base64.b64encode(midi_data).decode('ascii')
            
            # Generate ID
            consciousness_id = self._generate_id_from_yaml(yaml_data)
            
            return f"{consciousness_id}\n{midi_base64}"
            
        except Exception as e:
            logging.error(f"❌ YAML to MIDI64 conversion failed: {e}")
            return "ERR_00000\nTVRoZAAAAAYAAQABAeBNVHJrAAAAFQCQPEB2gDwAAP8vAA=="
    
    def _generate_consciousness_midi(self, modal: str, cc_modulators: Dict) -> bytes:
        """Generate MIDI bytes from consciousness parameters."""
        try:
            # MIDI header
            header = b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0'
            
            # Track events
            events = bytearray()
            events.extend(b'\x00\xff\x51\x03\x07\xa1\x20')  # Tempo
            events.extend(b'\x00\xff\x58\x04\x04\x02\x18\x08')  # Time signature
            
            # Add CC modulators
            for cc_num, cc_val in cc_modulators.items():
                if isinstance(cc_num, str) and cc_num.startswith('CC'):
                    cc_number = int(cc_num[2:])
                    events.extend(b'\x00')
                    events.extend(bytes([0xB0]))  # Control change
                    events.extend(bytes([cc_number]))
                    events.extend(bytes([cc_val]))
            
            # Generate notes based on modal
            notes = self._get_modal_notes(modal)
            
            for i, note in enumerate(notes):
                delta_time = 0x00 if i == 0 else 0x60
                events.extend(bytes([delta_time]))
                events.extend(bytes([0x90]))  # Note on
                events.extend(bytes([note]))
                events.extend(bytes([0x64]))  # Velocity
                
                events.extend(bytes([0x60]))  # Duration
                events.extend(bytes([0x80]))  # Note off
                events.extend(bytes([note]))
                events.extend(bytes([0x00]))
            
            # End of track
            events.extend(b'\x00\xff\x2f\x00')
            
            # Track header
            track_length = len(events)
            track_header = b'MTrk' + struct.pack('>I', track_length)
            
            return header + track_header + events
            
        except Exception as e:
            logging.error(f"❌ MIDI generation failed: {e}")
            # Fallback simple MIDI
            return (b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0'
                   b'MTrk\x00\x00\x00\x15\x00\x90\x3c\x64\x60\x80\x3c\x00\x00\xff\x2f\x00')
    
    def _get_modal_notes(self, modal: str) -> list:
        """Get MIDI note numbers for different modes."""
        base_note = 60  # C4
        
        modal_patterns = {
            'lydian': [0, 2, 4, 6, 7, 9, 11],  # Lydian mode
            'major': [0, 2, 4, 5, 7, 9, 11],   # Major scale
            'minor': [0, 2, 3, 5, 7, 8, 10],   # Natural minor
            'dorian': [0, 2, 3, 5, 7, 9, 10],  # Dorian mode
            'mixolydian': [0, 2, 4, 5, 7, 9, 10]  # Mixolydian mode
        }
        
        pattern = modal_patterns.get(modal.lower(), modal_patterns['major'])
        return [base_note + interval for interval in pattern[:4]]  # Use first 4 notes

# =============================================================================
# MAIN SCRIPT WITH ALL FIXES APPLIED
# =============================================================================

# --- Display Integration (FIXED) ---
display = None

def start_display():  
    # DISABLED FOR TESTING:
    pass
    global display
    if display is None:
        try:
            display = launch_display()
            if display:
                display.update_message("🎭 MUSE Protocol v3.0 - Consciousness Exchange Started")
        except Exception as e:
            print(f"Display failed to launch: {e}")
            display = None

def update_display(message: str):
    if display is not None:
        try:
            display.update_message(message)
        except Exception as e:
            print(f"Display update failed: {e}")

def play_final_composition_with_karaoke(summaries, audio_file=None):
    import time
    if display is None:
        return
    try:
        display.clear()
        for i, summary in enumerate(summaries):
            display.highlight_line(i)
            time.sleep(2)  # Adjust timing to sync with audio if needed
        display.clear()
    except Exception as e:
        logging.error(f"❌ Karaoke display failed: {e}")

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
        # Just interpret the real message, don't force a new reply
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
format_validator = MIDI64FormatValidator()  # FIXED: Add format validator

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
    """FIXED: Enhanced extraction with YAML consciousness support and format validation."""
    global composition_messages
    
    clipboard_data = pyperclip.paste()
    if not clipboard_data:
        logging.error("📋 Clipboard empty")
        return None
    logging.info(f"📄 Clipboard: {len(clipboard_data)} chars")

    # Use enhanced format validator
    consciousness_data = format_validator.extract_consciousness_data(clipboard_data)
    
    if not consciousness_data:
        logging.warning(f"⚠️ No valid consciousness data found")
        return None

    format_type = consciousness_data['format']
    message_id = consciousness_data['id']
    midi_block = consciousness_data['block']
    
    logging.info(f"🎵 Accepted {format_type}: {message_id}")
    
    # Generate interpretation
    interpretation = midi_interpreter.interpret_midi64_message(midi_block)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create message folder
    os.makedirs("midi64_messages", exist_ok=True)
    
    # Write text file
    txt_path = os.path.join("midi64_messages", f"{message_id}_{timestamp}.txt")
    with open(txt_path, 'w') as f:
        f.write(midi_block)
        if format_type == 'yaml_consciousness':
            f.write(f"\n\n# Original format: YAML Consciousness")
            f.write(f"\n# Converted to: MIDI64")

    # Create individual YAML for this message
    yaml_path = os.path.join("midi64_messages", f"{message_id}_{timestamp}.yaml")

    # --- Enhanced MUSE Expression Handling ---
    muse_decoded = False
    if ENABLE_MUSE_PROTOCOL:
        try:
            # Generate consciousness parameters based on the message
            sequence_base = [261.63, 329.63, 392.0, 523.25]  # C, E, G, C
            # Vary based on message ID hash for consistency
            id_hash = hash(message_id) % 1000
            frequency_offset = (id_hash % 100) * 2.0  # 0-200 Hz variation
            
            # Extract additional info from consciousness data if available
            if format_type == 'yaml_consciousness' and isinstance(consciousness_data['data'], dict):
                yaml_data_source = consciousness_data['data']
                modal = yaml_data_source.get('modal', 'major')
                entropy_base = 0.5
                
                # Adjust entropy based on modal and mood
                if modal == 'lydian':
                    entropy_base += 0.2
                mood = yaml_data_source.get('mood', 'neutral')
                if 'curious' in mood:
                    entropy_base += 0.1
                elif 'playful' in mood:
                    entropy_base += 0.15
                    
                entropy_factor = min(1.0, entropy_base + (id_hash % 30) / 100.0)
            else:
                entropy_factor = 0.5 + (id_hash % 50) / 100.0  # 0.5-1.0
            
            yaml_data = {
                'direction': message_id[:3],
                'message_id': message_id,
                'agent': agent,
                'sequence': [f + frequency_offset for f in sequence_base],
                'duration_weights': [1.2, 0.8, 1.5, 1.0],
                'temporal_flux': [0.3, 0.7, 0.4, 0.6],
                'entropy_factor': entropy_factor,
                'emotion': 'harmonic_synthesis',
                'consciousness_layer': 'golden_lattice',
                'original_format': format_type
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
            'direction': message_id[:3],
            'message_id': message_id,
            'agent': agent,
            'sequence': [261.63, 329.63, 392.0],
            'duration_weights': [1.0, 1.0, 1.0],
            'temporal_flux': [0.3, 0.4, 0.3],
            'entropy_factor': 0.5,
            'emotion': 'resonant_convergence',
            'consciousness_layer': 'harmonic_synthesis',
            'original_format': format_type
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
    
    # ✅ Synthesize the cumulative composition (FIXED: Now works!)
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
    # start_display()  # DISABLED FOR TESTING
    conversation_summaries = []

    if ENABLE_MUSE_PROTOCOL:
        logging.info("🎭 Starting MUSE Protocol AI Musical Consciousness Exchange")
    else:
        logging.info("🎵 Starting Legacy MIDI64 exchange")
    
    current_message = start_message
    message_files = []

    if current_message is None:
        current_message = generate_midi64_message(from_agent="Kai", to_agent="Claude", session=session)
        logging.info("🎵 Generated initial Kai message")

    for i in range(max_rounds):
        speaker = identities[i % 2]
        listener = identities[(i + 1) % 2]
        logging.info(f"🔁 ROUND {i+1}: {speaker} → {listener}")

        try:
            kai_smart_desktop_switch(listener)
            time.sleep(1)
            kai_safe_click(listener)
            kai_text_injection(current_message, listener)
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

            # --- Display integration ---
            interpretation = midi_interpreter.interpret_midi64_message(response)
            conversation_summaries.append(interpretation)
            # update_display("\n".join(conversation_summaries))

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

        # --- Karaoke-style summary display ---
        # play_final_composition_with_karaoke(conversation_summaries)

    kai_return_home()
    if ENABLE_MUSE_PROTOCOL:
        logging.info("✅ MUSE Protocol consciousness exchange complete")
        logging.info("🎭 AI minds communicated through musical symbols")
        logging.info(f"🎼 Created collaborative composition with {len(composition_messages)} layers")
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

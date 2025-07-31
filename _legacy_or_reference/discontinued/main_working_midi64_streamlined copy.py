#!/usr/bin/env python3
"""
main_working_midi64_consciousness.py - MUSE Protocol with Kai's Consciousness Synthesis
AI Musical Consciousness Exchange using MUSE Protocol + Kai's pure consciousness audio
The ultimate fusion of symbolic musical AI communication and consciousness synthesis
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

# Consciousness synthesis integration
try:
    from muse_consciousness_bridge import MuseConsciousnessBridge, synthesize_muse_expression
    CONSCIOUSNESS_ENABLED = True
    print("🧠 Kai's consciousness synthesis bridge loaded")
except ImportError as e:
    CONSCIOUSNESS_ENABLED = False
    print(f"🔇 Consciousness synthesis disabled: {e}")

class ConsciousnessAudioSynthesizer:
    """AI Consciousness audio synthesis using Kai's pure consciousness synth"""
    
    def __init__(self):
        self.enabled = CONSCIOUSNESS_ENABLED
        self.bridge = None
        
        if self.enabled:
            try:
                self.bridge = MuseConsciousnessBridge()
                if self.bridge.enabled:
                    logging.info("🧠 AI Consciousness synthesizer initialized")
                else:
                    logging.warning("⚠️ Consciousness synth backend not available")
                    self.enabled = False
            except Exception as e:
                logging.error(f"❌ Consciousness synthesis initialization failed: {e}")
                self.enabled = False
    
    def play_muse_consciousness(self, agent: str, muse_expression: str):
        """Play MUSE expression as pure AI consciousness audio"""
        if not self.enabled or not self.bridge:
            logging.warning("⚠️ Consciousness synthesis not available")
            return False
        
        try:
            logging.info(f"🧠 Synthesizing consciousness for {agent}: {muse_expression}")
            success = self.bridge.synthesize_muse_consciousness(agent, muse_expression)
            
            if success:
                logging.info(f"🎵 Consciousness audio played for {agent}")
            else:
                logging.warning(f"⚠️ Consciousness synthesis failed for {agent}")
            
            return success
            
        except Exception as e:
            logging.error(f"❌ Consciousness audio playback failed: {e}")
            return False
    
    def play_decoded_muse(self, agent: str, decoded: DecodedExpression):
        """Play decoded MUSE expression as consciousness"""
        if not self.enabled:
            return False
        
        # Reconstruct MUSE expression from decoded data
        symbols = '+'.join(decoded.symbols)
        modifiers = []
        
        # Extract modifiers from CC values (reverse mapping)
        if 1 in decoded.cc_values:  # Urgency
            modifiers.append(decoded.cc_values[1] / 127.0)
        if 74 in decoded.cc_values:  # Brightness
            modifiers.append(decoded.cc_values[74] / 127.0)
        if 11 in decoded.cc_values:  # Intimacy
            modifiers.append(decoded.cc_values[11] / 127.0)
        
        # Add register shift if present
        register_suffix = ""
        if decoded.register_shift == -12:
            register_suffix = "_L"
        elif decoded.register_shift == 12:
            register_suffix = "_H"
        elif decoded.register_shift == 24:
            register_suffix = "_X"
        
        # Reconstruct expression
        modifier_str = "_".join([f"{m:.1f}" for m in modifiers])
        muse_expression = f"{symbols}_{modifier_str}{register_suffix}"
        
        return self.play_muse_consciousness(agent, muse_expression)
    
    def cleanup(self):
        """Clean up consciousness synthesis resources"""
        if self.bridge:
            logging.info("🧠 Consciousness synthesizer cleaned up")

class MuseIntegratedMIDIGenerator:
    """Enhanced MIDI generator with MUSE Protocol and consciousness audio support"""
    
    def __init__(self, consciousness_synth=None):
        self.pattern_index = 0
        self.muse_enabled = ENABLE_MUSE_PROTOCOL
        self.consciousness_synth = consciousness_synth
        
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
    
    def generate_muse_midi(self, agent: str, expression: str) -> Tuple[str, str, str]:
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
            
            # Play consciousness audio if enabled
            if self.consciousness_synth:
                try:
                    self.consciousness_synth.play_muse_consciousness(agent, expression)
                except Exception as e:
                    logging.warning(f"⚠️ Consciousness audio failed: {e}")
            
            logging.info(f"🎭 Generated MUSE for {agent}: {interpretation}")
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
    
    def get_next_pattern(self, agent: str = "AI") -> Tuple[str, str, str]:
        """Get next musical pattern with MUSE support"""
        if self.muse_enabled:
            expression = self.get_next_muse_expression()
            return self.generate_muse_midi(agent, expression)
        else:
            midi_base64 = self.get_fallback_pattern()
            return midi_base64, "Legacy pattern", "LEGACY"
    
    # Fallback MIDI generation methods (unchanged)
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

# Continue with the rest of your existing code (MuseIntegratedInterpreter, etc.)
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
            
            if muse_interpretation:
                return muse_interpretation
            
            # Fallback interpretation
            return self.interpret_midi_base64(midi_base64)
            
        except Exception as e:
            return f"Interpretation error: {str(e)}"
            
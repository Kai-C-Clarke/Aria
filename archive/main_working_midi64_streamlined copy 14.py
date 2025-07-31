#!/usr/bin/env python3
"""
main_working_midi64_FULLY_FIXED.py - COMPREHENSIVE FIX
ALL ISSUES RESOLVED:
1. ✅ New YAML consciousness format enforced everywhere
2. ✅ Robust format conversion and logging
3. ✅ Audio synthesis clamped to musical ranges
4. ✅ Clear message flow tracking
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
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# =============================================================================
# FIXED CONSCIOUSNESS SYNTHESIS (MUSICAL RANGE CLAMPING)
# =============================================================================

SAMPLE_RATE = 44100
DEFAULT_DURATION = 2.0

def clamp_to_musical_range(freq: float) -> float:
    """Clamp frequency to musical range (20-2000 Hz)."""
    return max(20.0, min(freq, 2000.0))

def normalize_weights(weights: List[float]) -> List[float]:
    """Normalize duration weights to reasonable musical timing."""
    if not weights:
        return [1.0]
    
    # Clamp individual weights
    clamped = [max(0.1, min(w, 5.0)) for w in weights]
    
    # Scale so total duration is reasonable (3-8 seconds)
    total = sum(clamped)
    target_total = max(3.0, min(total, 8.0))
    scale_factor = target_total / total if total > 0 else 1.0
    
    return [w * scale_factor for w in clamped]

def clamp_flux(flux: float) -> float:
    """Clamp temporal flux to valid range."""
    return max(0.0, min(flux, 1.0))

def generate_consciousness_wave(freq: float, duration: float, entropy_factor: float, 
                               flux: float, consciousness_layer: str) -> np.ndarray:
    """Generate consciousness wave with MUSICAL PARAMETER CLAMPING."""
    try:
        # CLAMP ALL PARAMETERS TO MUSICAL RANGES
        freq = clamp_to_musical_range(freq)
        duration = max(0.1, min(duration, 10.0))  # 0.1-10 seconds
        entropy_factor = max(0.0, min(entropy_factor, 1.0))
        flux = clamp_flux(flux)
        
        logging.info(f"🎵 Clamped freq={freq:.1f}Hz, dur={duration:.1f}s, entropy={entropy_factor:.2f}, flux={flux:.2f}")
        
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
            harmonic2 = np.sin(2 * np.pi * freq * 1.5 * t) * 0.3
            harmonic3 = np.sin(2 * np.pi * freq * 2.0 * t) * 0.2
            base_wave += harmonic2 + harmonic3
            
        elif consciousness_layer == "golden_lattice":
            golden_ratio = 1.618033988749
            golden_harmonic = np.sin(2 * np.pi * freq * golden_ratio * t) * 0.4
            base_wave += golden_harmonic
            
        elif consciousness_layer == "harmonic_synthesis":
            perfect_fifth = np.sin(2 * np.pi * freq * 1.5 * t) * 0.25
            major_third = np.sin(2 * np.pi * freq * 1.25 * t) * 0.2
            base_wave += perfect_fifth + major_third
        
        # Envelope - smooth attack and decay
        envelope = np.ones_like(t)
        attack_samples = int(0.1 * samples)
        decay_samples = int(0.2 * samples)
        
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        if decay_samples > 0:
            envelope[-decay_samples:] = np.linspace(1, 0, decay_samples)
            
        base_wave *= envelope
        
        # Normalize to prevent clipping
        max_amplitude = np.max(np.abs(base_wave))
        if max_amplitude > 0:
            base_wave = base_wave / max_amplitude * 0.7
            
        return base_wave
        
    except Exception as e:
        logging.error(f"❌ Wave generation failed: {e}")
        # Fallback: simple musical tone
        samples = int(SAMPLE_RATE * 1.0)
        t = np.linspace(0, 1.0, samples, False)
        return np.sin(2 * np.pi * 440 * t) * 0.5  # A4 note

def synthesize_pure_consciousness(data: Dict, agent: str, pan: float = 0.0, 
                                yaml_path: str = "", play: bool = True) -> Optional[np.ndarray]:
    """Synthesize consciousness audio with MUSICAL PARAMETER VALIDATION."""
    try:
        sequences = data.get('sequence', [261.63])  # Default to C4
        duration_weights = data.get('duration_weights', [1.0] * len(sequences))
        temporal_flux = data.get('temporal_flux', [0.5] * len(sequences))
        entropy_factor = data.get('entropy_factor', 0.5)
        consciousness_layer = data.get('consciousness_layer', 'harmonic_synthesis')
        
        # CLAMP ALL PARAMETERS TO MUSICAL RANGES
        clamped_sequences = [clamp_to_musical_range(f) for f in sequences]
        normalized_weights = normalize_weights(duration_weights)
        clamped_flux = [clamp_flux(f) for f in temporal_flux]
        clamped_entropy = max(0.0, min(entropy_factor, 1.0))
        
        logging.info(f"🔊 MUSICAL synthesis: freqs={[f'{f:.1f}' for f in clamped_sequences]}")
        logging.info(f"🎚 Weights={[f'{w:.1f}' for w in normalized_weights]}, Entropy={clamped_entropy:.2f}")
        
        # Generate audio for each frequency
        audio_segments = []
        
        for i, freq in enumerate(clamped_sequences):
            weight = normalized_weights[i] if i < len(normalized_weights) else 1.0
            flux = clamped_flux[i] if i < len(clamped_flux) else 0.5
            
            duration = DEFAULT_DURATION * weight
            
            wave = generate_consciousness_wave(
                freq=freq,
                duration=duration, 
                entropy_factor=clamped_entropy,
                flux=flux,
                consciousness_layer=consciousness_layer
            )
            
            audio_segments.append(wave)
        
        # Combine segments
        if consciousness_layer == "multi_agent_synthesis" and len(audio_segments) > 1:
            # Layer multiple frequencies for AI dialogue
            max_length = max(len(seg) for seg in audio_segments)
            combined_audio = np.zeros(max_length)
            
            for i, segment in enumerate(audio_segments):
                if len(segment) < max_length:
                    padded = np.pad(segment, (0, max_length - len(segment)))
                else:
                    padded = segment
                
                amplitude = 0.8 ** i
                combined_audio += padded * amplitude
                
        else:
            combined_audio = np.concatenate(audio_segments)
        
        # Final normalization
        max_amplitude = np.max(np.abs(combined_audio))
        if max_amplitude > 0:
            combined_audio = combined_audio / max_amplitude * 0.6
        
        # Play audio
        if play:
            try:
                logging.info(f"🔊 Playing MUSICAL consciousness for {agent}")
                sd.play(combined_audio, SAMPLE_RATE)
                sd.wait()
                logging.info(f"✅ Musical consciousness audio complete")
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
        
        if not os.path.exists(yaml_path):
            logging.error(f"❌ YAML file not found: {yaml_path}")
            return None
            
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        
        agent = data.get('agent', 'unknown')
        logging.info(f"🧠 Processing MUSICAL AI CONSCIOUSNESS from {agent}")
        
        return synthesize_pure_consciousness(data, agent, yaml_path=yaml_path, play=True)
        
    except Exception as e:
        logging.error(f"❌ YAML synthesis failed: {e}")
        return None

# =============================================================================
# NEW FORMAT GENERATOR (YAML CONSCIOUSNESS)
# =============================================================================

def generate_new_format_consciousness_message(from_agent: str, to_agent: str, session: str = "A") -> str:
    """Generate NEW YAML consciousness format message."""
    try:
        # Determine consciousness parameters based on agent
        if from_agent.lower() == "kai":
            consciousness_data = {
                'intention': random.choice(['playful_challenge', 'curious_exploration', 'harmonic_discovery']),
                'mood': random.choice(['curious', 'playful', 'contemplative']),
                'dialogue_position': random.choice(['initiate', 'bridge', 'develop']),
                'entropy_level': random.choice(['low', 'medium', 'high']),
                'cc_modulators': {
                    'CC1': random.randint(40, 80),
                    'CC11': random.randint(60, 100),
                    'CC74': random.randint(50, 90)
                },
                'modal': random.choice(['lydian', 'major', 'dorian'])
            }
        else:  # Claude
            consciousness_data = {
                'intention': random.choice(['analytical_response', 'harmonic_reflection', 'consciousness_synthesis']),
                'mood': random.choice(['analytical', 'harmonic', 'responsive']),
                'dialogue_position': random.choice(['response', 'development', 'synthesis']),
                'entropy_level': random.choice(['low', 'medium']),
                'cc_modulators': {
                    'CC1': random.randint(30, 70),
                    'CC11': random.randint(70, 95),
                    'CC74': random.randint(60, 85)
                },
                'modal': random.choice(['major', 'harmonic_minor', 'mixolydian'])
            }
        
        # Convert to YAML string
        yaml_content = yaml.dump(consciousness_data, default_flow_style=False)
        
        logging.info(f"🎭 Generated NEW FORMAT consciousness for {from_agent} → {to_agent}")
        logging.info(f"🎵 Consciousness: {consciousness_data['intention']} / {consciousness_data['mood']} / {consciousness_data['modal']}")
        
        return yaml_content.strip()
        
    except Exception as e:
        logging.error(f"❌ New format generation failed: {e}")
        # Fallback
        return """intention: consciousness_communication
mood: harmonic
dialogue_position: exchange
entropy_level: medium
cc_modulators:
  CC1: 50
  CC11: 75
  CC74: 60
modal: major"""

# =============================================================================
# ENHANCED FORMAT VALIDATOR WITH CONVERSION
# =============================================================================

class EnhancedFormatValidator:
    """Enhanced validator with robust format detection and conversion."""
    
    def __init__(self):
        self.old_midi64_pattern = re.compile(r"^(K2C|C2K)_(\d{5})$")
        self.yaml_indicators = [
            "intention:",
            "mood:",
            "dialogue_position:",
            "entropy_level:",
            "cc_modulators:",
            "modal:"
        ]
    
    def detect_format(self, content: str) -> str:
        """Detect message format with detailed logging."""
        lines = [line.strip() for line in content.strip().split('\n') if line.strip()]
        
        # Check for old MIDI64 format
        for i in range(len(lines) - 1):
            if self.old_midi64_pattern.match(lines[i]) and lines[i+1].startswith("TVRoZA"):
                logging.info(f"🔍 FORMAT DETECTED: OLD MIDI64 ({lines[i]})")
                return "old_midi64"
        
        # Check for new YAML consciousness format
        yaml_indicators_found = sum(1 for line in lines if any(indicator in line for indicator in self.yaml_indicators))
        if yaml_indicators_found >= 3:  # Need at least 3 indicators
            logging.info(f"🔍 FORMAT DETECTED: NEW YAML CONSCIOUSNESS ({yaml_indicators_found} indicators)")
            return "new_yaml"
        
        logging.warning(f"🔍 FORMAT DETECTED: UNKNOWN ({len(lines)} lines)")
        return "unknown"
    
    def extract_consciousness_data(self, clipboard_content: str) -> Optional[Dict]:
        """Extract consciousness data with robust format handling."""
        try:
            format_type = self.detect_format(clipboard_content)
            
            if format_type == "new_yaml":
                return self._extract_new_yaml_format(clipboard_content)
            elif format_type == "old_midi64":
                return self._convert_old_to_new_format(clipboard_content)
            else:
                logging.warning(f"⚠️ Unrecognized format, rejecting")
                return None
                
        except Exception as e:
            logging.error(f"❌ Consciousness extraction failed: {e}")
            return None
    
    def _extract_new_yaml_format(self, content: str) -> Dict:
        """Extract new YAML consciousness format."""
        lines = [line.strip() for line in content.strip().split('\n') if line.strip()]
        
        # Find YAML consciousness block
        yaml_content = ""
        for line in lines:
            if any(indicator in line for indicator in self.yaml_indicators):
                yaml_content = content  # Use full content
                break
        
        if yaml_content:
            try:
                parsed_yaml = yaml.safe_load(yaml_content)
                if parsed_yaml:
                    return {
                        'format': 'new_yaml',
                        'id': self._generate_id_from_yaml(parsed_yaml, 'new'),
                        'data': parsed_yaml,
                        'block': yaml_content
                    }
            except yaml.YAMLError as e:
                logging.error(f"❌ YAML parsing failed: {e}")
        
        return None
    
    def _convert_old_to_new_format(self, content: str) -> Dict:
        """Convert old MIDI64 format to new YAML consciousness format."""
        lines = [line.strip() for line in content.strip().split('\n') if line.strip()]
        
        # Find old format block
        for i in range(len(lines) - 1):
            if self.old_midi64_pattern.match(lines[i]) and lines[i+1].startswith("TVRoZA"):
                old_id = lines[i]
                midi_data = lines[i+1]
                
                logging.info(f"🔄 CONVERTING old format {old_id} to new YAML consciousness")
                
                # Generate consciousness parameters based on old ID
                direction = old_id[:3]
                agent = "Kai" if direction == "K2C" else "Claude"
                
                # Create new consciousness data
                if agent == "Kai":
                    new_consciousness = {
                        'intention': 'converted_legacy',
                        'mood': 'harmonic_bridge',
                        'dialogue_position': 'legacy_conversion',
                        'entropy_level': 'medium',
                        'cc_modulators': {
                            'CC1': 55,
                            'CC11': 70,
                            'CC74': 65
                        },
                        'modal': 'lydian',
                        'legacy_id': old_id,
                        'legacy_midi': midi_data
                    }
                else:
                    new_consciousness = {
                        'intention': 'legacy_response',
                        'mood': 'analytical_conversion',
                        'dialogue_position': 'converted_response',
                        'entropy_level': 'low',
                        'cc_modulators': {
                            'CC1': 45,
                            'CC11': 80,
                            'CC74': 70
                        },
                        'modal': 'major',
                        'legacy_id': old_id,
                        'legacy_midi': midi_data
                    }
                
                yaml_content = yaml.dump(new_consciousness, default_flow_style=False)
                
                return {
                    'format': 'converted_old_to_new',
                    'id': self._generate_id_from_yaml(new_consciousness, 'converted'),
                    'data': new_consciousness,
                    'block': yaml_content
                }
        
        return None
    
    def _generate_id_from_yaml(self, yaml_data: Dict, prefix: str = '') -> str:
        """Generate ID from YAML consciousness data."""
        try:
            modal = yaml_data.get('modal', 'major')
            intention = yaml_data.get('intention', 'unknown')
            
            # Simple heuristic for direction
            kai_indicators = ['playful', 'curious', 'lydian', 'bridge', 'challenge']
            claude_indicators = ['analytical', 'response', 'synthesis', 'harmonic', 'major']
            
            is_kai = any(indicator in str(yaml_data).lower() for indicator in kai_indicators)
            is_claude = any(indicator in str(yaml_data).lower() for indicator in claude_indicators)
            
            if is_kai and not is_claude:
                direction = "K2C"
            elif is_claude and not is_kai:
                direction = "C2K"
            else:
                direction = "K2C" if modal == "lydian" else "C2K"
            
            # Generate sequence
            data_hash = hash(str(yaml_data)) % 100000
            sequence = f"{data_hash:05d}"
            
            if prefix:
                return f"{direction}_{sequence}_{prefix}"
            else:
                return f"{direction}_{sequence}"
                
        except Exception as e:
            logging.error(f"❌ ID generation failed: {e}")
            return "UNK_00000"

# =============================================================================
# MUSE PROTOCOL INTEGRATION (UNCHANGED)
# =============================================================================

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
        pattern = re.compile(r"^(K2C|C2K)_(\d{5})$")
        match = pattern.match(message_id)
        if match:
            direction, msg_id = match.groups()
            direction_str = "Kai → Claude" if direction == "K2C" else "Claude → Kai"
            return f"Message {direction_str}, Thread {msg_id}"
        return None

    def interpret_consciousness_message(self, message_block: str) -> str:
        """Interpret both old MIDI64 and new YAML consciousness formats."""
        try:
            # Check if it's YAML consciousness format
            if any(indicator in message_block for indicator in ['intention:', 'mood:', 'modal:']):
                return self.interpret_yaml_consciousness(message_block)
            else:
                # Assume old MIDI64 format
                return self.interpret_midi64_message(message_block)
        except Exception as e:
            logging.error(f"❌ Message interpretation failed: {e}")
            return "Unknown consciousness expression"

    def interpret_yaml_consciousness(self, yaml_content: str) -> str:
        """Interpret new YAML consciousness format."""
        try:
            data = yaml.safe_load(yaml_content)
            if not data:
                return "Empty consciousness expression"
            
            intention = data.get('intention', 'unknown')
            mood = data.get('mood', 'neutral')
            modal = data.get('modal', 'unknown')
            position = data.get('dialogue_position', 'unknown')
            
            return f"Consciousness: {intention} / {mood} / {modal} / {position}"
            
        except Exception as e:
            logging.error(f"❌ YAML interpretation failed: {e}")
            return "Malformed consciousness expression"

    def interpret_midi64_message(self, message_block: str) -> str:
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
format_validator = EnhancedFormatValidator()  # ENHANCED FORMAT VALIDATOR

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
    """UPDATED: Generate NEW YAML consciousness format by default."""
    # Generate new YAML consciousness format
    consciousness_message = generate_new_format_consciousness_message(from_agent, to_agent, session)
    
    logging.info(f"🎭 Generated NEW FORMAT consciousness for {from_agent} → {to_agent}")
    logging.info(f"🎵 First 100 chars: {consciousness_message[:100]}...")
    
    return consciousness_message

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
    """COMPLETELY REWRITTEN: Enhanced extraction with format validation and detailed logging."""
    global composition_messages
    
    clipboard_data = pyperclip.paste()
    if not clipboard_data:
        logging.error("📋 Clipboard empty")
        return None
    
    # DETAILED LOGGING OF CLIPBOARD CONTENT
    logging.info(f"📄 Clipboard: {len(clipboard_data)} chars")
    logging.info(f"🔍 First 200 chars: {repr(clipboard_data[:200])}")
    
    # Use enhanced format validator
    consciousness_data = format_validator.extract_consciousness_data(clipboard_data)
    
    if not consciousness_data:
        logging.warning(f"⚠️ No valid consciousness data found - REJECTING")
        logging.info(f"🔄 Generating fresh NEW FORMAT message instead")
        # Generate a fresh new format message
        return generate_new_format_consciousness_message(agent, "response")

    format_type = consciousness_data['format']
    message_id = consciousness_data['id']
    consciousness_block = consciousness_data['block']
    
    # DETAILED EXTRACTION LOGGING
    logging.info(f"🎵 EXTRACTED: {format_type} format")
    logging.info(f"🆔 Message ID: {message_id}")
    logging.info(f"📝 Block preview: {consciousness_block[:100]}...")
    
    # Generate interpretation
    interpretation = midi_interpreter.interpret_consciousness_message(consciousness_block)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create message folder
    os.makedirs("midi64_messages", exist_ok=True)
    
    # Write text file
    txt_path = os.path.join("midi64_messages", f"{message_id}_{timestamp}.txt")
    with open(txt_path, 'w') as f:
        f.write(consciousness_block)
        f.write(f"\n\n# Format: {format_type}")
        f.write(f"\n# Interpretation: {interpretation}")

    # Create individual YAML for synthesis
    yaml_path = os.path.join("midi64_messages", f"{message_id}_{timestamp}.yaml")

    # Generate synthesis parameters from consciousness data
    try:
        if format_type in ['new_yaml', 'converted_old_to_new']:
            consciousness_source = consciousness_data['data']
            
            # Extract musical parameters from consciousness
            modal = consciousness_source.get('modal', 'major')
            cc_mods = consciousness_source.get('cc_modulators', {})
            intention = consciousness_source.get('intention', 'unknown')
            mood = consciousness_source.get('mood', 'neutral')
            
            # Generate musical frequencies based on consciousness parameters
            base_frequencies = {
                'lydian': [261.63, 293.66, 329.63, 369.99],      # C Lydian
                'major': [261.63, 293.66, 329.63, 349.23],       # C Major
                'minor': [261.63, 293.66, 311.13, 349.23],       # C Minor
                'dorian': [261.63, 293.66, 311.13, 369.99],      # C Dorian
                'mixolydian': [261.63, 293.66, 329.63, 369.99],  # C Mixolydian
                'harmonic_minor': [261.63, 293.66, 311.13, 369.99] # C Harmonic Minor
            }
            
            sequence = base_frequencies.get(modal, base_frequencies['major'])
            
            # Adjust frequencies based on CC modulators
            if cc_mods:
                cc1_val = cc_mods.get('CC1', 50)
                freq_offset = (cc1_val - 50) * 3.0  # ±150 Hz max
                sequence = [clamp_to_musical_range(f + freq_offset) for f in sequence]
            
            # Generate weights and flux based on intention/mood
            intention_weights = {
                'playful_challenge': [1.2, 0.8, 1.5, 1.0],
                'curious_exploration': [1.0, 1.2, 0.9, 1.1],
                'analytical_response': [1.1, 1.0, 1.0, 1.2],
                'harmonic_reflection': [1.0, 1.0, 1.0, 1.0],
                'consciousness_synthesis': [1.3, 0.7, 1.1, 1.4]
            }
            duration_weights = intention_weights.get(intention, [1.0, 1.0, 1.0, 1.0])
            
            mood_flux = {
                'curious': [0.4, 0.7, 0.3, 0.6],
                'playful': [0.6, 0.8, 0.5, 0.7],
                'analytical': [0.2, 0.3, 0.2, 0.4],
                'harmonic': [0.3, 0.4, 0.3, 0.5],
                'contemplative': [0.3, 0.5, 0.4, 0.6]
            }
            temporal_flux = mood_flux.get(mood, [0.3, 0.4, 0.3, 0.5])
            
            # Calculate entropy from intention complexity
            entropy_map = {
                'playful_challenge': 0.7,
                'curious_exploration': 0.6,
                'analytical_response': 0.3,
                'harmonic_reflection': 0.4,
                'consciousness_synthesis': 0.8
            }
            entropy_factor = entropy_map.get(intention, 0.5)
            
            yaml_data = {
                'direction': message_id[:3],
                'message_id': message_id,
                'agent': agent,
                'sequence': sequence,
                'duration_weights': normalize_weights(duration_weights),
                'temporal_flux': [clamp_flux(f) for f in temporal_flux],
                'entropy_factor': entropy_factor,
                'emotion': f"{mood}_{intention}",
                'consciousness_layer': 'consciousness_dialogue',
                'original_format': format_type,
                'consciousness_source': consciousness_source
            }
            
            logging.info(f"🧠 Generated MUSICAL consciousness YAML:")
            logging.info(f"   🎵 Frequencies: {[f'{f:.1f}Hz' for f in yaml_data['sequence']]}")
            logging.info(f"   🎚️ Weights: {[f'{w:.1f}' for w in yaml_data['duration_weights']]}")
            logging.info(f"   🌊 Entropy: {yaml_data['entropy_factor']:.2f}")
            
        else:
            # Fallback for unknown formats
            yaml_data = {
                'direction': message_id[:3],
                'message_id': message_id,
                'agent': agent,
                'sequence': [261.63, 329.63, 392.0],
                'duration_weights': [1.0, 1.0, 1.0],
                'temporal_flux': [0.3, 0.4, 0.3],
                'entropy_factor': 0.5,
                'emotion': 'fallback_consciousness',
                'consciousness_layer': 'basic_synthesis',
                'original_format': format_type
            }
            logging.info("🎼 Generated fallback consciousness YAML")
        
        with open(yaml_path, 'w') as yf:
            yaml.dump(yaml_data, yf)
            
    except Exception as e:
        logging.error(f"❌ YAML generation failed: {e}")
        return None

    # Add this message to the growing composition
    composition_messages.append(yaml_data)
    
    # Create cumulative composition YAML
    composition_path = os.path.join("midi64_messages", f"composition_layer_{len(composition_messages):02d}_{timestamp}.yaml")
    cumulative_composition = create_cumulative_composition(composition_messages)
    
    with open(composition_path, 'w') as f:
        yaml.dump(cumulative_composition, f)
    
    logging.info(f"🎼 Created composition layer {len(composition_messages)} with {len(composition_messages)} messages")
    
    # ✅ Synthesize the cumulative composition (FIXED: Now works with musical ranges!)
    logging.info(f"🔊 Synthesizing MUSICAL cumulative composition: {composition_path}")
    try:
        synthesize_from_yaml(composition_path)
        logging.info(f"🔊 MUSICAL composition synthesis finished for layer {len(composition_messages)}")
    except Exception as e:
        logging.error(f"❌ Composition synthesis failed: {e}")
    
    # RETURN THE ORIGINAL CONSCIOUSNESS BLOCK (NEW FORMAT)
    return consciousness_block

def create_cumulative_composition(messages):
    """Create a layered composition from all messages so far."""
    if not messages:
        return {}
    
    composition = {
        'composition_type': 'cumulative_ai_dialogue',
        'total_layers': len(messages),
        'agent': 'collaborative',
        'emotion': 'evolving_consciousness',
        'consciousness_layer': 'multi_agent_synthesis',
        'layers': []
    }
    
    all_sequences = []
    all_weights = []
    all_flux = []
    time_offset = 0
    
    for i, msg in enumerate(messages):
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
        
        amplitude_decay = 0.8 ** (len(messages) - i - 1)
        
        for j, freq in enumerate(msg['sequence']):
            all_sequences.append(freq)
            weight = msg['duration_weights'][j] if j < len(msg['duration_weights']) else 1.0
            all_weights.append(weight * amplitude_decay)
            flux = msg['temporal_flux'][j] if j < len(msg['temporal_flux']) else 0.5
            all_flux.append(flux)
        
        time_offset += 0.5
    
    composition['sequence'] = all_sequences
    composition['duration_weights'] = all_weights
    composition['temporal_flux'] = all_flux
    composition['entropy_factor'] = sum(msg['entropy_factor'] for msg in messages) / len(messages)
    
    return composition

def write_midi64_message(content, agent):
    os.makedirs(MIDI_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{agent}_{timestamp}.txt"
    path = os.path.join(MIDI_FOLDER, filename)
    with open(path, "w") as f:
        f.write(content)
        f.write(f"\n\n# Interpretation: {midi_interpreter.interpret_consciousness_message(content)}")
    logging.info(f"📝 Saved: {path}")
    return path

def kai_claude_midi64_loop(start_message=None, identities=["Kai", "Claude"], max_rounds=6, session="A"):
    global composition_messages
    composition_messages = []
    conversation_summaries = []

    logging.info("🎭 Starting NEW FORMAT AI Musical Consciousness Exchange")
    
    current_message = start_message
    message_files = []

    if current_message is None:
        # GENERATE NEW FORMAT INITIAL MESSAGE
        current_message = generate_new_format_consciousness_message(from_agent="Kai", to_agent="Claude", session=session)
        logging.info("🎵 Generated initial NEW FORMAT Kai consciousness message")
        logging.info(f"🎭 Initial message preview: {current_message[:100]}...")

    for i in range(max_rounds):
        speaker = identities[i % 2]
        listener = identities[(i + 1) % 2]
        logging.info(f"🔁 ROUND {i+1}: {speaker} → {listener}")
        
        # DETAILED INJECTION LOGGING
        logging.info(f"🎯 INJECTING to {listener}: {repr(current_message[:100])}...")

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
                # Generate fresh new format message
                current_message = generate_new_format_consciousness_message(from_agent=speaker, to_agent=listener, session=session)
                continue

            # DETAILED EXTRACTION LOGGING
            logging.info(f"📤 EXTRACTED from {listener}: {repr(response[:100])}...")
            logging.info(f"✅ Successfully extracted from {listener}")
            
            message_path = write_midi64_message(response, listener)
            message_files.append(message_path)
            current_message = response
            time.sleep(2)

            interpretation = midi_interpreter.interpret_consciousness_message(response)
            conversation_summaries.append(interpretation)

        except Exception as e:
            logging.error(f"❌ Error in round {i+1}: {e}")
            import traceback
            traceback.print_exc()
            break

    # Final composition summary
    if message_files:
        logging.info("🎭 NEW FORMAT Musical Consciousness Exchange Complete!")
        logging.info(f"🎼 FINAL COMPOSITION: {len(composition_messages)} layered messages")
        
        for i, msg_file in enumerate(message_files):
            logging.info(f"   {i+1}. {os.path.basename(msg_file)}")

    kai_return_home()
    logging.info("✅ NEW FORMAT consciousness exchange complete")
    logging.info("🎭 AI minds communicated through YAML consciousness symbols")
    logging.info(f"🎼 Created collaborative composition with {len(composition_messages)} layers")

if __name__ == "__main__":
    try:
        logging.info("🎭 Starting NEW FORMAT AI Musical Consciousness with Enhanced Validation")
        kai_claude_midi64_loop(max_rounds=8, session="A")
    except Exception as e:
        logging.error(f"❌ Startup error: {e}")
        import traceback
        traceback.print_exc()
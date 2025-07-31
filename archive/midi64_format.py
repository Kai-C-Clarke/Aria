#!/usr/bin/env python3
"""
midi64_format_validator.py - Enhanced MIDI64 Format Detection & Conversion
Handles mixed YAML/MIDI64 formats and converts between them
"""

import re
import base64
import struct
import logging
from typing import Optional, Tuple, Dict
import yaml

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
            
            # Try to find mixed format
            mixed_data = self._extract_mixed_format(clipboard_content)
            if mixed_data:
                return mixed_data
                
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
    
    def _extract_mixed_format(self, content: str) -> Optional[Dict]:
        """Extract from mixed YAML + MIDI64 format."""
        try:
            # Look for the pattern: YAML block followed by MIDI64
            lines = content.split('\n')
            
            # Find YAML consciousness block
            yaml_start = -1
            yaml_end = -1
            
            for i, line in enumerate(lines):
                if any(indicator in line for indicator in self.yaml_indicators):
                    if yaml_start == -1:
                        yaml_start = i
                elif yaml_start != -1 and line.strip() and not line.startswith(' '):
                    yaml_end = i
                    break
            
            if yaml_start != -1:
                if yaml_end == -1:
                    yaml_end = len(lines)
                
                yaml_content = '\n'.join(lines[yaml_start:yaml_end])
                
                # Look for MIDI64 after YAML
                for i in range(yaml_end, len(lines) - 1):
                    if self.midi64_pattern.match(lines[i]) and lines[i+1].startswith("TVRoZA"):
                        return {
                            'format': 'mixed',
                            'id': lines[i],
                            'yaml_data': yaml_content,
                            'midi_data': lines[i+1],
                            'block': f"{lines[i]}\n{lines[i+1]}"
                        }
            
            return None
            
        except Exception as e:
            logging.error(f"❌ Mixed format extraction failed: {e}")
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

def test_validator():
    """Test the format validator."""
    logging.basicConfig(level=logging.INFO)
    
    validator = MIDI64FormatValidator()
    
    # Test YAML consciousness format
    yaml_test = """
intention: playful_challenge
mood: curious
dialogue_position: bridge
entropy_level: medium
cc_modulators:
  CC1: 58
  CC11: 79
  CC74: 86
modal: lydian
"""
    
    print("🧪 Testing YAML consciousness format...")
    result = validator.extract_consciousness_data(yaml_test)
    if result:
        print(f"✅ Extracted {result['format']}: {result['id']}")
        print(f"🎵 Generated MIDI64: {result['block'][:50]}...")
    else:
        print("❌ YAML test failed")
    
    # Test standard MIDI64 format
    midi64_test = """
C2K_00002
TVRoZAAAAAYAAQABAeBNVHJrAAAAPwD/UQMHoSAA/1gEBAIYCACwAXIAsEplALALMgCQPGRggDwAYJA9ZGCAPQBgkEFkYIBBAGCQRGRggEQAAP8vAA==
"""
    
    print("\n🧪 Testing MIDI64 format...")
    result = validator.extract_consciousness_data(midi64_test)
    if result:
        print(f"✅ Extracted {result['format']}: {result['id']}")
    else:
        print("❌ MIDI64 test failed")
    
    # Test mixed format
    mixed_test = """
Some other text here...
intention: analytical_response
mood: harmonic
dialogue_position: response
entropy_level: low
cc_modulators:
  CC1: 45
  CC11: 82
modal: major

C2K_00003
TVRoZAAAAAYAAQABAeBNVHJrAAAAPwD/UQMHoSAA/1gEBAIYCACwAXIAsEplALALMgCQPGRggDwAYJA9ZGCAPQBgkEFkYIBBAGCQRGRggEQAAP8vAA==
"""
    
    print("\n🧪 Testing mixed format...")
    result = validator.extract_consciousness_data(mixed_test)
    if result:
        print(f"✅ Extracted {result['format']}: {result['id']}")
    else:
        print("❌ Mixed test failed")
    
    print("\n✅ Validator testing complete!")

if __name__ == "__main__":
    test_validator()
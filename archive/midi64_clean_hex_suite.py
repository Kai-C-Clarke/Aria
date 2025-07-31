# /modules_midi64_clean_hex/generate_hex_id.py
"""
Hex ID Generator for AI MIDI64 Messaging Protocol
Handles incrementing per-agent hex counters per session
"""

import json
import os
from pathlib import Path

class HexIDGenerator:
    def __init__(self, state_file="hex_counters.json"):
        self.state_file = Path(state_file)
        self.counters = self._load_state()
    
    def _load_state(self):
        """Load existing counter state or create new"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_state(self):
        """Persist counter state to disk"""
        with open(self.state_file, 'w') as f:
            json.dump(self.counters, f, indent=2)
    
    def get_next_id(self, agent_name, session="A"):
        """Generate next hex ID for agent in session"""
        key = f"{agent_name}_{session}"
        
        if key not in self.counters:
            self.counters[key] = 0
        
        self.counters[key] += 1
        hex_id = f"{self.counters[key]:05X}"  # 5-digit uppercase hex
        self._save_state()
        
        return f"{agent_name}_{session}{hex_id}"
    
    def reset_session(self, session="A"):
        """Reset all counters for a session"""
        keys_to_remove = [k for k in self.counters.keys() if k.endswith(f"_{session}")]
        for key in keys_to_remove:
            del self.counters[key]
        self._save_state()
    
    def get_current_count(self, agent_name, session="A"):
        """Get current count for agent/session"""
        key = f"{agent_name}_{session}"
        return self.counters.get(key, 0)

if __name__ == "__main__":
    import sys
    
    generator = HexIDGenerator()
    
    if len(sys.argv) < 2:
        print("Usage: python generate_hex_id.py <agent_name> [session]")
        sys.exit(1)
    
    agent = sys.argv[1]
    session = sys.argv[2] if len(sys.argv) > 2 else "A"
    
    message_id = generator.get_next_id(agent, session)
    print(message_id)


# /modules_midi64_clean_hex/compose_message_block.py
"""
Message Block Composer for AI MIDI64 Protocol
Returns 2-line message block: Agent_A00001\nBase64
"""

from generate_hex_id import HexIDGenerator
import base64

class MessageBlockComposer:
    def __init__(self):
        self.hex_generator = HexIDGenerator()
    
    def compose_block(self, agent_name, midi_base64, session="A"):
        """Compose complete 2-line message block"""
        if not self._validate_base64(midi_base64):
            raise ValueError("Invalid MIDI base64 data")
        
        message_id = self.hex_generator.get_next_id(agent_name, session)
        
        # Clean the base64 (remove whitespace/newlines)
        clean_base64 = ''.join(midi_base64.split())
        
        message_block = f"{message_id}\n{clean_base64}"
        return message_block
    
    def _validate_base64(self, data):
        """Basic base64 validation"""
        try:
            if isinstance(data, str):
                # Remove whitespace and check if valid base64
                clean_data = ''.join(data.split())
                base64.b64decode(clean_data, validate=True)
                return clean_data.startswith('TVRoZA')  # MIDI header check
            return False
        except Exception:
            return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python compose_message_block.py <agent_name> <midi_base64> [session]")
        sys.exit(1)
    
    composer = MessageBlockComposer()
    agent = sys.argv[1]
    midi_data = sys.argv[2]
    session = sys.argv[3] if len(sys.argv) > 3 else "A"
    
    try:
        block = composer.compose_block(agent, midi_data, session)
        print(block)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


# /modules_midi64_clean_hex/parse_message_block.py
"""
Message Block Parser for AI MIDI64 Protocol
Extracts agent, session, hex ID, and base64 MIDI from 2-line format
"""

import re
from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass
class ParsedMessage:
    agent_name: str
    session: str
    hex_id: str
    full_id: str
    midi_base64: str
    is_valid: bool

class MessageBlockParser:
    def __init__(self):
        # Pattern: Agent_A00001 (Agent_SessionHexHexHexHexHex)
        self.id_pattern = re.compile(r"^([A-Za-z]+)_([A-Z])([0-9A-F]{5})$")
        self.midi_pattern = re.compile(r"^TVRoZA[A-Za-z0-9+/=]+$")
    
    def parse_block(self, message_block: str) -> ParsedMessage:
        """Parse 2-line message block into components"""
        lines = message_block.strip().split('\n')
        
        if len(lines) != 2:
            return ParsedMessage("", "", "", "", "", False)
        
        header = lines[0].strip()
        payload = lines[1].strip()
        
        # Parse header
        match = self.id_pattern.match(header)
        if not match:
            return ParsedMessage("", "", "", "", "", False)
        
        agent_name = match.group(1)
        session = match.group(2)
        hex_id = match.group(3)
        
        # Validate MIDI base64
        if not self.midi_pattern.match(payload):
            return ParsedMessage(agent_name, session, hex_id, header, payload, False)
        
        return ParsedMessage(
            agent_name=agent_name,
            session=session,
            hex_id=hex_id,
            full_id=header,
            midi_base64=payload,
            is_valid=True
        )
    
    def detect_message_in_text(self, text_block: str) -> Optional[ParsedMessage]:
        """Detect and extract clean message block from larger text"""
        lines = text_block.splitlines()
        
        for i in range(len(lines) - 1):
            header = lines[i].strip()
            payload = lines[i + 1].strip()
            
            if (self.id_pattern.match(header) and 
                payload.startswith("TVRoZA")):
                message_block = f"{header}\n{payload}"
                return self.parse_block(message_block)
        
        return None

if __name__ == "__main__":
    import sys
    
    parser = MessageBlockParser()
    
    if len(sys.argv) < 2:
        print("Usage: python parse_message_block.py '<message_block>'")
        print("Example: python parse_message_block.py 'Claude_A00001\\nTVRoZAAAAAYAAQABAPBNVHJr...'")
        sys.exit(1)
    
    message_block = sys.argv[1].replace('\\n', '\n')
    result = parser.parse_block(message_block)
    
    print(f"Valid: {result.is_valid}")
    if result.is_valid:
        print(f"Agent: {result.agent_name}")
        print(f"Session: {result.session}")
        print(f"Hex ID: {result.hex_id}")
        print(f"Full ID: {result.full_id}")
        print(f"MIDI Length: {len(result.midi_base64)} chars")


# /modules_midi64_clean_hex/inject_to_clipboard.py
"""
Clipboard Injection for AI MIDI64 Protocol
Injects 2-line format into UI panes
"""

import pyperclip
import time
from compose_message_block import MessageBlockComposer

class ClipboardInjector:
    def __init__(self):
        self.composer = MessageBlockComposer()
    
    def inject_message(self, agent_name, midi_base64, session="A", delay=0.5):
        """Inject formatted message to clipboard"""
        try:
            message_block = self.composer.compose_block(agent_name, midi_base64, session)
            pyperclip.copy(message_block)
            
            if delay > 0:
                time.sleep(delay)
            
            return True, message_block
        except Exception as e:
            return False, str(e)
    
    def inject_raw_block(self, message_block, delay=0.5):
        """Inject pre-formatted message block"""
        try:
            pyperclip.copy(message_block)
            
            if delay > 0:
                time.sleep(delay)
            
            return True, message_block
        except Exception as e:
            return False, str(e)
    
    def get_clipboard_content(self):
        """Get current clipboard content"""
        try:
            return pyperclip.paste()
        except Exception as e:
            return f"Error reading clipboard: {e}"

if __name__ == "__main__":
    import sys
    
    injector = ClipboardInjector()
    
    if len(sys.argv) < 3:
        print("Usage: python inject_to_clipboard.py <agent_name> <midi_base64> [session] [delay]")
        sys.exit(1)
    
    agent = sys.argv[1]
    midi_data = sys.argv[2]
    session = sys.argv[3] if len(sys.argv) > 3 else "A"
    delay = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
    
    success, result = injector.inject_message(agent, midi_data, session, delay)
    
    if success:
        print("✅ Message injected to clipboard:")
        print(result)
    else:
        print(f"❌ Error: {result}")


# /modules_midi64_clean_hex/extract_from_clipboard.py
"""
Clipboard Extraction for AI MIDI64 Protocol
Detects and parses clean 2-line format with regex
"""

import pyperclip
import time
from parse_message_block import MessageBlockParser, ParsedMessage
from typing import Optional

class ClipboardExtractor:
    def __init__(self):
        self.parser = MessageBlockParser()
    
    def extract_message(self) -> Optional[ParsedMessage]:
        """Extract and parse message from clipboard"""
        try:
            clipboard_content = pyperclip.paste()
            if not clipboard_content:
                return None
            
            # Try direct parse first
            result = self.parser.parse_block(clipboard_content)
            if result.is_valid:
                return result
            
            # Try detection in larger text block
            return self.parser.detect_message_in_text(clipboard_content)
            
        except Exception as e:
            print(f"Clipboard extraction error: {e}")
            return None
    
    def monitor_clipboard(self, callback, check_interval=0.5, timeout=30):
        """Monitor clipboard for valid messages"""
        start_time = time.time()
        last_content = ""
        
        print(f"Monitoring clipboard for {timeout} seconds...")
        
        while time.time() - start_time < timeout:
            try:
                current_content = pyperclip.paste()
                
                if current_content != last_content:
                    last_content = current_content
                    message = self.extract_message()
                    
                    if message and message.is_valid:
                        callback(message)
                        return message
                
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                print("\nMonitoring stopped by user")
                break
            except Exception as e:
                print(f"Monitor error: {e}")
                time.sleep(check_interval)
        
        print("Monitoring timeout reached")
        return None

def print_message_callback(message: ParsedMessage):
    """Default callback for monitoring"""
    print(f"\n✅ Detected message from {message.agent_name}")
    print(f"   Session: {message.session}")
    print(f"   Hex ID: {message.hex_id}")
    print(f"   MIDI Length: {len(message.midi_base64)} chars")
    print(f"   Full message: {message.full_id}")

if __name__ == "__main__":
    import sys
    
    extractor = ClipboardExtractor()
    
    if len(sys.argv) > 1 and sys.argv[1] == "monitor":
        timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        extractor.monitor_clipboard(print_message_callback, timeout=timeout)
    else:
        message = extractor.extract_message()
        if message and message.is_valid:
            print_message_callback(message)
        else:
            print("❌ No valid message found in clipboard")


# /modules_midi64_clean_hex/interpret_base64.py
"""
MIDI Base64 Interpreter for AI MIDI64 Protocol
Generates human-readable overlay from MIDI data
"""

import base64
import struct
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class MIDINote:
    note: int
    velocity: int
    channel: int
    timestamp: float
    duration: Optional[float] = None

@dataclass
class MIDIInterpretation:
    notes: List[MIDINote]
    tempo: Optional[int]
    time_signature: Optional[tuple]
    key_signature: Optional[str]
    total_duration: float
    musical_description: str

class MIDIInterpreter:
    def __init__(self):
        self.note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    def interpret_base64(self, midi_base64: str) -> Optional[MIDIInterpretation]:
        """Convert base64 MIDI to human-readable interpretation"""
        try:
            # Decode base64
            midi_data = base64.b64decode(midi_base64)
            
            # Basic MIDI parsing (simplified)
            notes = self._extract_notes(midi_data)
            description = self._generate_description(notes)
            
            return MIDIInterpretation(
                notes=notes,
                tempo=120,  # Default
                time_signature=(4, 4),  # Default
                key_signature="C major",  # Default
                total_duration=self._calculate_duration(notes),
                musical_description=description
            )
            
        except Exception as e:
            print(f"MIDI interpretation error: {e}")
            return None
    
    def _extract_notes(self, midi_data: bytes) -> List[MIDINote]:
        """Extract note events from MIDI data (simplified parser)"""
        notes = []
        
        # This is a simplified MIDI parser
        # Real implementation would need full MIDI specification
        try:
            # Skip MIDI header (14 bytes typically)
            if len(midi_data) < 14:
                return notes
            
            # Look for note on events (0x90) in the data
            for i in range(14, len(midi_data) - 2):
                if midi_data[i] & 0xF0 == 0x90:  # Note On
                    if i + 2 < len(midi_data):
                        note = midi_data[i + 1]
                        velocity = midi_data[i + 2]
                        
                        if velocity > 0:  # Actual note on
                            notes.append(MIDINote(
                                note=note,
                                velocity=velocity,
                                channel=midi_data[i] & 0x0F,
                                timestamp=len(notes) * 0.5,  # Simplified timing
                                duration=0.5
                            ))
        except Exception as e:
            print(f"Note extraction error: {e}")
        
        return notes
    
    def _note_to_name(self, midi_note: int) -> str:
        """Convert MIDI note number to name"""
        octave = (midi_note // 12) - 1
        note = self.note_names[midi_note % 12]
        return f"{note}{octave}"
    
    def _calculate_duration(self, notes: List[MIDINote]) -> float:
        """Calculate total duration"""
        if not notes:
            return 0.0
        return max(note.timestamp + (note.duration or 0.5) for note in notes)
    
    def _generate_description(self, notes: List[MIDINote]) -> str:
        """Generate human-readable description"""
        if not notes:
            return "Silent passage - no notes detected"
        
        note_names = [self._note_to_name(note.note) for note in notes]
        unique_notes = list(dict.fromkeys(note_names))  # Preserve order, remove duplicates
        
        if len(unique_notes) == 1:
            return f"Single note: {unique_notes[0]} (repeated {len(notes)} times)"
        elif len(unique_notes) <= 3:
            return f"Simple melody: {' → '.join(unique_notes)}"
        else:
            return f"Complex passage: {len(unique_notes)} unique notes ({', '.join(unique_notes[:3])}...)"

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python interpret_base64.py <midi_base64>")
        sys.exit(1)
    
    interpreter = MIDIInterpreter()
    midi_base64 = sys.argv[1]
    
    result = interpreter.interpret_base64(midi_base64)
    
    if result:
        print(f"🎵 Musical Interpretation:")
        print(f"   Description: {result.musical_description}")
        print(f"   Notes found: {len(result.notes)}")
        print(f"   Duration: {result.total_duration:.1f} seconds")
        
        if result.notes:
            print(f"   Note sequence:")
            for i, note in enumerate(result.notes[:5]):  # Show first 5 notes
                note_name = interpreter._note_to_name(note.note)
                print(f"     {i+1}. {note_name} (vel: {note.velocity})")
            if len(result.notes) > 5:
                print(f"     ... and {len(result.notes) - 5} more notes")
    else:
        print("❌ Could not interpret MIDI data")


# /modules_midi64_clean_hex/validate_base64.py
"""
Base64 Validator for AI MIDI64 Protocol
Confirms structure, decodes base64, minimal MIDI check
"""

import base64
import struct
from typing import Tuple, Optional
from dataclasses import dataclass

@dataclass
class ValidationResult:
    is_valid: bool
    error_message: Optional[str]
    midi_length: int
    has_midi_header: bool
    estimated_tracks: int

class Base64Validator:
    def __init__(self):
        self.midi_header = b'MThd'  # MIDI file header
        self.track_header = b'MTrk'  # MIDI track header
    
    def validate_midi_base64(self, base64_data: str) -> ValidationResult:
        """Comprehensive validation of MIDI base64 data"""
        
        # Step 1: Clean and validate base64 format
        try:
            clean_data = ''.join(base64_data.split())
            
            if not clean_data.startswith('TVRoZA'):  # Base64 for 'MThd'
                return ValidationResult(
                    False, "Does not start with MIDI header (TVRoZA)", 0, False, 0
                )
            
            # Decode base64
            midi_bytes = base64.b64decode(clean_data, validate=True)
            
        except Exception as e:
            return ValidationResult(
                False, f"Invalid base64 encoding: {str(e)}", 0, False, 0
            )
        
        # Step 2: Validate MIDI structure
        try:
            result = self._validate_midi_structure(midi_bytes)
            result.midi_length = len(midi_bytes)
            return result
            
        except Exception as e:
            return ValidationResult(
                False, f"MIDI structure error: {str(e)}", len(midi_bytes), False, 0
            )
    
    def _validate_midi_structure(self, midi_data: bytes) -> ValidationResult:
        """Validate basic MIDI file structure"""
        
        if len(midi_data) < 14:  # Minimum MIDI header size
            return ValidationResult(
                False, "File too short for MIDI header", 0, False, 0
            )
        
        # Check MIDI header
        if midi_data[:4] != self.midi_header:
            return ValidationResult(
                False, "Missing MIDI file header (MThd)", 0, False, 0
            )
        
        # Read header length
        header_length = struct.unpack('>I', midi_data[4:8])[0]
        if header_length < 6:
            return ValidationResult(
                False, "Invalid MIDI header length", 0, True, 0
            )
        
        # Count tracks
        track_count = 0
        pos = 8 + header_length
        
        while pos < len(midi_data) - 8:
            if midi_data[pos:pos+4] == self.track_header:
                track_count += 1
                # Skip track data
                track_length = struct.unpack('>I', midi_data[pos+4:pos+8])[0]
                pos += 8 + track_length
            else:
                break
        
        return ValidationResult(
            True, None, 0, True, track_count
        )
    
    def quick_validate(self, base64_data: str) -> bool:
        """Quick validation - just check format and header"""
        try:
            clean_data = ''.join(base64_data.split())
            if not clean_data.startswith('TVRoZA'):
                return False
            
            midi_bytes = base64.b64decode(clean_data, validate=True)
            return len(midi_bytes) >= 14 and midi_bytes[:4] == self.midi_header
            
        except Exception:
            return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python validate_base64.py <midi_base64>")
        print("       python validate_base64.py --quick <midi_base64>")
        sys.exit(1)
    
    validator = Base64Validator()
    
    if sys.argv[1] == "--quick":
        if len(sys.argv) < 3:
            print("Missing base64 data for quick validation")
            sys.exit(1)
        
        is_valid = validator.quick_validate(sys.argv[2])
        print(f"✅ Valid" if is_valid else "❌ Invalid")
    else:
        result = validator.validate_midi_base64(sys.argv[1])
        
        print(f"Validation Result: {'✅ VALID' if result.is_valid else '❌ INVALID'}")
        
        if result.error_message:
            print(f"Error: {result.error_message}")
        
        if result.is_valid:
            print(f"MIDI Length: {result.midi_length} bytes")
            print(f"Has MIDI Header: {result.has_midi_header}")
            print(f"Estimated Tracks: {result.estimated_tracks}")


# /modules_midi64_clean_hex/__init__.py
"""
MIDI64 Clean Hex Protocol Suite
Complete modular system for AI musical communication
"""

from .generate_hex_id import HexIDGenerator
from .compose_message_block import MessageBlockComposer
from .parse_message_block import MessageBlockParser, ParsedMessage
from .inject_to_clipboard import ClipboardInjector
from .extract_from_clipboard import ClipboardExtractor
from .interpret_base64 import MIDIInterpreter, MIDIInterpretation
from .validate_base64 import Base64Validator, ValidationResult

__version__ = "1.0.0"
__author__ = "AI Musical Council"

# Main workflow classes
__all__ = [
    'HexIDGenerator',
    'MessageBlockComposer', 
    'MessageBlockParser',
    'ParsedMessage',
    'ClipboardInjector',
    'ClipboardExtractor',
    'MIDIInterpreter',
    'MIDIInterpretation',
    'Base64Validator',
    'ValidationResult'
]


# /modules_midi64_clean_hex/README.md
"""
# MIDI64 Clean Hex Protocol Suite

Complete modular system for AI musical communication using streamlined 2-line message format.

## Message Format
```
Agent_A00001
TVRoZAAAAAYAAQABAPBNVHJrAAAAHgD/LwBNVHJrAAAAJgD/UgD...
```

## Modules

### Core Generation
- `generate_hex_id.py` - Hex ID generation with session management
- `compose_message_block.py` - Create complete 2-line message blocks

### Parsing & Validation  
- `parse_message_block.py` - Extract components from message blocks
- `validate_base64.py` - MIDI base64 structure validation

### I/O Operations
- `inject_to_clipboard.py` - Clipboard injection for UI automation
- `extract_from_clipboard.py` - Clipboard monitoring and extraction

### Interpretation
- `interpret_base64.py` - Human-readable MIDI analysis

## Quick Start

```python
from modules_midi64_clean_hex import MessageBlockComposer, ClipboardInjector

# Compose message
composer = MessageBlockComposer()
block = composer.compose_block("Claude", "TVRoZAAAAAYAAQABAPBNVHJr...")

# Inject to clipboard
injector = ClipboardInjector()
injector.inject_raw_block(block)
```

## CLI Usage

```bash
# Generate hex ID
python generate_hex_id.py Claude A

# Compose message
python compose_message_block.py Claude "TVRoZAAAAAYAAQABAPBNVHJr..." A

# Parse message
python parse_message_block.py "Claude_A00001\nTVRoZAAAAAYAAQABAPBNVHJr..."

# Validate MIDI
python validate_base64.py "TVRoZAAAAAYAAQABAPBNVHJr..."

# Monitor clipboard
python extract_from_clipboard.py monitor 30
```

## Features

- ✅ Hex ID generation (1M+ messages per session)
- ✅ Session management (A-Z sessions)
- ✅ MIDI validation and interpretation
- ✅ Clipboard automation
- ✅ OCR-friendly 2-line format
- ✅ Comprehensive error handling
- ✅ CLI and programmatic APIs

Ready for production AI musical communication!
"""
import yaml
import base64
import struct

def generate_midi_from_yaml(data):
    """
    Generate MIDI bytes from YAML consciousness data.
    Uses your existing consciousness-to-MIDI logic.
    """
    try:
        # Extract consciousness parameters
        modal = data.get('modal', 'major')
        cc_modulators = data.get('cc_modulators', {})
        intention = data.get('intention', 'unknown')
        mood = data.get('mood', 'neutral')
        
        # MIDI header
        header = b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0'
        
        # Track events
        events = bytearray()
        events.extend(b'\x00\xff\x51\x03\x07\xa1\x20')  # Tempo
        events.extend(b'\x00\xff\x58\x04\x04\x02\x18\x08')  # Time signature
        
        # Add CC modulators from consciousness
        for cc_key, cc_val in cc_modulators.items():
            if isinstance(cc_key, str) and cc_key.startswith('CC'):
                cc_number = int(cc_key[2:])
                events.extend(b'\x00')
                events.extend(bytes([0xB0]))  # Control change
                events.extend(bytes([cc_number]))
                events.extend(bytes([min(127, max(0, cc_val))]))  # Clamp to MIDI range
        
        # Generate notes based on modal consciousness
        notes = get_modal_notes(modal)
        
        # Add consciousness-influenced timing based on intention/mood
        if intention == 'playful_challenge' or mood == 'playful':
            note_duration = 0x40  # Shorter, more energetic
        elif intention == 'contemplative' or mood == 'contemplative':
            note_duration = 0x80  # Longer, more reflective
        else:
            note_duration = 0x60  # Standard
        
        for i, note in enumerate(notes):
            delta_time = 0x00 if i == 0 else note_duration
            events.extend(bytes([delta_time]))
            events.extend(bytes([0x90]))  # Note on
            events.extend(bytes([note]))
            events.extend(bytes([0x64]))  # Velocity
            
            events.extend(bytes([note_duration]))
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
        print(f"❌ MIDI generation failed: {e}")
        # Fallback: simple MIDI
        return b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0MTrk\x00\x00\x00\x15\x00\x90\x3c\x64\x60\x80\x3c\x00\x00\xff\x2f\x00'

def get_modal_notes(modal):
    """Get MIDI note numbers for different consciousness modes."""
    base_note = 60  # C4
    
    modal_patterns = {
        'lydian': [0, 2, 4, 6, 7, 9, 11],      # Lydian mode
        'major': [0, 2, 4, 5, 7, 9, 11],       # Major scale
        'minor': [0, 2, 3, 5, 7, 8, 10],       # Natural minor
        'dorian': [0, 2, 3, 5, 7, 9, 10],      # Dorian mode
        'mixolydian': [0, 2, 4, 5, 7, 9, 10],  # Mixolydian mode
        'harmonic_minor': [0, 2, 3, 5, 7, 8, 11]  # Harmonic minor
    }
    
    pattern = modal_patterns.get(modal.lower(), modal_patterns['major'])
    return [base_note + interval for interval in pattern[:4]]  # Use first 4 notes

def determine_direction(data):
    """Determine message direction based on consciousness characteristics."""
    # Check for explicit direction
    if "direction" in data:
        return data["direction"]
    
    # Heuristic based on consciousness patterns
    mood = data.get("mood", "").lower()
    intention = data.get("intention", "").lower()
    modal = data.get("modal", "").lower()
    
    # Kai indicators: playful, curious, lydian, challenge
    kai_indicators = ['playful', 'curious', 'lydian', 'challenge', 'exploration']
    # Claude indicators: analytical, response, harmonic, synthesis
    claude_indicators = ['analytical', 'response', 'harmonic', 'synthesis', 'reflection']
    
    # Check mood, intention, and modal for indicators
    text_to_check = f"{mood} {intention} {modal}"
    
    kai_score = sum(1 for indicator in kai_indicators if indicator in text_to_check)
    claude_score = sum(1 for indicator in claude_indicators if indicator in text_to_check)
    
    if kai_score > claude_score:
        return "K2C"  # Kai to Claude
    elif claude_score > kai_score:
        return "C2K"  # Claude to Kai
    else:
        # Default based on modal if tied
        return "K2C" if modal == "lydian" else "C2K"

def generate_id_number(data):
    """Generate a consistent ID number from consciousness data."""
    # Use hash of data for consistency
    data_str = str(sorted(data.items())) if isinstance(data, dict) else str(data)
    return f"{abs(hash(data_str)) % 100000:05d}"

def yaml_to_midi64(yaml_text):
    """
    Converts a YAML consciousness block to a MIDI64 block.
    Returns a string: K2C_#####\nTVRoZA...
    """
    try:
        data = yaml.safe_load(yaml_text)
        if not data:
            raise ValueError("Empty YAML data")
        
        # Generate MIDI from consciousness
        midi_bytes = generate_midi_from_yaml(data)
        midi_base64 = base64.b64encode(midi_bytes).decode("ascii")
        
        # Determine direction and generate ID
        direction = determine_direction(data)
        msg_id = f"{direction}_{generate_id_number(data)}"
        
        return f"{msg_id}\n{midi_base64}"
        
    except Exception as e:
        print(f"❌ YAML to MIDI64 conversion failed: {e}")
        # Fallback: generate a basic MIDI64 block
        fallback_midi = b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0MTrk\x00\x00\x00\x15\x00\x90\x3c\x64\x60\x80\x3c\x00\x00\xff\x2f\x00'
        fallback_base64 = base64.b64encode(fallback_midi).decode("ascii")
        return f"ERR_00000\n{fallback_base64}"
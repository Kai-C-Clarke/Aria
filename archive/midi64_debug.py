import base64
import io
import mido

def debug_midi64_file(midi64_path):
    """Debug a MIDI64 file to understand its structure"""
    
    # Read the base64 data
    with open(midi64_path, "r") as f:
        midi64_text = f.read().strip()
    
    print(f"Raw MIDI64 text: {midi64_text}")
    print(f"Base64 text length: {len(midi64_text)}")
    
    try:
        # Decode base64
        midi64_bytes = base64.b64decode(midi64_text)
        print(f"Decoded bytes length: {len(midi64_bytes)}")
        
        # Show hex dump of first 20 bytes
        hex_dump = ' '.join(f'{b:02x}' for b in midi64_bytes[:20])
        print(f"First 20 bytes (hex): {hex_dump}")
        
        # Check if it starts with MIDI header
        if midi64_bytes[:4] == b'MThd':
            print("✓ Valid MIDI header found")
            header_length = int.from_bytes(midi64_bytes[4:8], 'big')
            print(f"Header length: {header_length}")
            if len(midi64_bytes) >= 8 + header_length:
                format_type = int.from_bytes(midi64_bytes[8:10], 'big')
                num_tracks = int.from_bytes(midi64_bytes[10:12], 'big')
                division = int.from_bytes(midi64_bytes[12:14], 'big')
                print(f"Format: {format_type}, Tracks: {num_tracks}, Division: {division}")
            else:
                print("✗ Header incomplete")
        else:
            print("✗ No valid MIDI header (should start with 'MThd')")
            
        # Try to load with mido
        try:
            mid = mido.MidiFile(file=io.BytesIO(midi64_bytes))
            print("✓ Successfully loaded with mido")
            print(f"Tracks: {len(mid.tracks)}")
            for i, track in enumerate(mid.tracks):
                print(f"  Track {i}: {len(track)} messages")
        except Exception as e:
            print(f"✗ Mido failed to load: {e}")
            
    except Exception as e:
        print(f"✗ Base64 decode failed: {e}")

def create_test_midi64():
    """Create a minimal valid MIDI file and encode as base64"""
    
    # Create a simple MIDI file
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    # Add a simple note
    track.append(mido.Message('program_change', program=12, time=0))
    track.append(mido.Message('note_on', channel=0, note=60, velocity=64, time=0))
    track.append(mido.Message('note_off', channel=0, note=60, velocity=64, time=480))
    
    # Save to bytes
    bytes_io = io.BytesIO()
    mid.save(file=bytes_io)
    midi_bytes = bytes_io.getvalue()
    
    # Encode as base64
    midi64 = base64.b64encode(midi_bytes).decode('ascii')
    
    print("Test MIDI64 (should work):")
    print(midi64)
    print(f"Length: {len(midi64)} chars, {len(midi_bytes)} bytes")
    
    return midi64

if __name__ == "__main__":
    print("=== Debugging existing MIDI64 file ===")
    debug_midi64_file("kai_phrase.midi64")
    
    print("\n=== Creating test MIDI64 ===")
    test_midi64 = create_test_midi64()
    
    # Save test file
    with open("test_phrase.midi64", "w") as f:
        f.write(test_midi64)
    print("\nSaved test_phrase.midi64")

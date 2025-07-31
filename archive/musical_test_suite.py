import mido
import base64
import io
import yaml

def create_kai_opening_phrase():
    """Create a more musical opening phrase from Kai"""
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    # Kai's characteristic: clarinet, slightly ahead timing, energetic
    track.append(mido.Message('program_change', program=71, time=0))  # Clarinet
    
    # Musical phrase: C-E-G-F-E-D-C (simple melodic line in 4/4)
    notes = [60, 64, 67, 65, 64, 62, 60]  # C4 to C4
    velocities = [85, 90, 95, 88, 82, 78, 80]  # Dynamic expression
    durations = [240, 240, 480, 240, 240, 240, 480]  # Quarter and half notes
    
    for note, vel, dur in zip(notes, velocities, durations):
        track.append(mido.Message('note_on', channel=0, note=note, velocity=vel, time=0))
        track.append(mido.Message('note_off', channel=0, note=note, velocity=vel, time=dur))
    
    # Convert to MIDI64
    bytes_io = io.BytesIO()
    mid.save(file=bytes_io)
    midi_bytes = bytes_io.getvalue()
    return base64.b64encode(midi_bytes).decode('ascii')

def create_claude_response():
    """Create Claude's analytical response to Kai's phrase"""
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    # Claude's characteristic: marimba, metronomic, sparse harmony
    track.append(mido.Message('program_change', program=12, time=0))  # Marimba
    
    # Musical response: Echo Kai's pattern but in higher register with harmony
    # Main melody: E-G-B-A-G-F-E
    melody = [64, 67, 71, 69, 67, 65, 64]  # E4 to E4 (perfect 4th above Kai)
    harmony = [60, 62, 64, 65, 64, 62, 60]  # Harmonic support
    
    for i, (mel, harm) in enumerate(zip(melody, harmony)):
        # Melody
        track.append(mido.Message('note_on', channel=0, note=mel, velocity=75, time=0))
        # Harmony (sparse - only on strong beats)
        if i % 2 == 0:  # Only on beats 1 and 3
            track.append(mido.Message('note_on', channel=0, note=harm, velocity=65, time=0))
        
        # Note offs
        track.append(mido.Message('note_off', channel=0, note=mel, velocity=75, time=240))
        if i % 2 == 0:
            track.append(mido.Message('note_off', channel=0, note=harm, velocity=65, time=0))
    
    # Convert to MIDI64
    bytes_io = io.BytesIO()
    mid.save(file=bytes_io)
    midi_bytes = bytes_io.getvalue()
    return base64.b64encode(midi_bytes).decode('ascii')

def create_test_files():
    """Create a complete conversation test"""
    
    # Kai's opening message
    kai_metadata = {
        "message_id": "KAI_002",
        "agent": "Kai",
        "time_signature": "4/4", 
        "intent": "Melodic opening phrase exploring C major scale",
        "voice_profile": "Kai",
        "phrase_style": {
            "note_length_bias": 1.1,
            "velocity_range": [75, 95],
            "chord_density": "medium"
        },
        "response_to": None
    }
    
    # Claude's response message  
    claude_metadata = {
        "message_id": "CLAUDE_001",
        "agent": "Claude",
        "time_signature": "4/4",
        "intent": "Harmonic echo of Kai's phrase with analytical variation",
        "voice_profile": "Claude", 
        "phrase_style": {
            "note_length_bias": 0.9,
            "velocity_range": [65, 85],
            "chord_density": "sparse"
        },
        "response_to": "KAI_002"
    }
    
    # Generate MIDI64 data
    kai_midi64 = create_kai_opening_phrase()
    claude_midi64 = create_claude_response()
    
    # Save files
    with open("kai_message_002.yaml", "w") as f:
        yaml.dump(kai_metadata, f, default_flow_style=False)
    
    with open("claude_message_001.yaml", "w") as f:
        yaml.dump(claude_metadata, f, default_flow_style=False)
        
    with open("kai_phrase_002.midi64", "w") as f:
        f.write(kai_midi64)
        
    with open("claude_phrase_001.midi64", "w") as f:
        f.write(claude_midi64)
    
    print("Created musical conversation test files:")
    print("- kai_message_002.yaml / kai_phrase_002.midi64")
    print("- claude_message_001.yaml / claude_phrase_001.midi64")
    print(f"Kai MIDI64 length: {len(kai_midi64)} chars")
    print(f"Claude MIDI64 length: {len(claude_midi64)} chars")
    
    print("\nTo test the conversation:")
    print("python3 main_working_midi64_streamlined_Version11.py")
    print("# Edit the script to use kai_message_002.yaml and kai_phrase_002.midi64")
    print("# Then run again with claude_message_001.yaml and claude_phrase_001.midi64")

if __name__ == "__main__":
    create_test_files()

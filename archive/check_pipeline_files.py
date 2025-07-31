import os
import mido
import base64
import io

def check_files():
    """Check what pipeline files exist and their contents"""
    
    files_to_check = [
        'render_pipeline.py',
        'voice_profiles.py', 
        'transcript_logger.py'
    ]
    
    print("🔍 Checking pipeline files...")
    
    for filename in files_to_check:
        if os.path.exists(filename):
            print(f"✓ {filename} exists")
            with open(filename, 'r') as f:
                content = f.read()
                print(f"  Size: {len(content)} characters")
                if 'def ' in content:
                    functions = [line.strip() for line in content.split('\n') if line.strip().startswith('def ')]
                    print(f"  Functions: {functions[:3]}...")  # Show first 3
                else:
                    print(f"  Preview: {content[:100]}...")
        else:
            print(f"✗ {filename} MISSING")
    
    return all(os.path.exists(f) for f in files_to_check)

def test_direct_midi_processing():
    """Test MIDI processing directly without the pipeline"""
    
    print("\n🧪 Testing direct MIDI processing...")
    
    # Read the sustained MIDI64
    with open("kai_phrase_sustained.midi64", "r") as f:
        midi64_text = f.read().strip()
    
    # Decode and load directly
    midi_bytes = base64.b64decode(midi64_text)
    mid = mido.MidiFile(file=io.BytesIO(midi_bytes))
    
    print(f"Original file: {len(mid.tracks)} tracks")
    
    # Show original timing
    track = mid.tracks[0]
    note_events = []
    current_time = 0
    
    for msg in track:
        current_time += msg.time
        if msg.type in ['note_on', 'note_off']:
            note_events.append((msg.type, current_time, msg.note, msg.velocity))
    
    print("Original note events:")
    for event in note_events[:10]:  # First 10 events
        print(f"  {event}")
    
    # Save directly without any processing
    output_path = "kai_direct_test.mid"
    mid.save(output_path)
    print(f"\nSaved direct copy to: {output_path}")
    
    # Now try to apply voice profile manually
    print("\n🔧 Applying voice profile manually...")
    
    # Modify the track directly
    modified_track = mido.MidiTrack()
    
    # Add program change for clarinet
    modified_track.append(mido.Message('program_change', program=71, time=0))
    
    # Copy and modify note events
    for msg in track:
        if msg.type == 'note_on':
            # Keep the note but maybe adjust velocity
            new_msg = msg.copy(velocity=min(127, int(msg.velocity * 1.1)))
            modified_track.append(new_msg)
        elif msg.type == 'note_off':
            # Extend the note duration by delaying the note_off
            extended_time = int(msg.time * 2.0)  # Double the duration
            new_msg = msg.copy(time=extended_time)
            modified_track.append(new_msg)
        else:
            # Copy other messages as-is
            modified_track.append(msg.copy())
    
    # Create new MIDI file with modified track
    modified_mid = mido.MidiFile()
    modified_mid.tracks.append(modified_track)
    
    modified_output = "kai_manually_extended.mid"
    modified_mid.save(modified_output)
    print(f"Saved manually extended version to: {modified_output}")
    
    return output_path, modified_output

def create_minimal_pipeline():
    """Create a minimal working pipeline if files are missing"""
    
    render_pipeline_content = '''import mido
import io
from voice_profiles import VOICE_PROFILES

def render_and_merge_message(midi_bytes, metadata, rest_mode="bar"):
    """Minimal rendering - just load and return MIDI"""
    
    # Load MIDI from bytes
    mid = mido.MidiFile(file=io.BytesIO(midi_bytes))
    
    print(f"Loaded MIDI: {len(mid.tracks)} tracks")
    
    # Get agent info
    agent = metadata.get("agent", "Unknown")
    print(f"Processing for agent: {agent}")
    
    # TODO: Apply voice profile transformations here
    # For now, just return the MIDI as-is
    
    return mid
'''
    
    voice_profiles_content = '''VOICE_PROFILES = {
    "Kai": {
        "voice_name": "Expressive Clarinet, warm mid-range",
        "program": 71,
        "pitch_range": (48, 72),
        "cc": {1: 25, 7: 100, 74: 85, 91: 40},
        "pan": 30,
        "timing_offset_ms": -5,
        "phrase_style": {
            "note_length_bias": 1.4,
            "velocity_range": (75, 105),
            "chord_density": "legato"
        }
    },
    "Claude": {
        "voice_name": "Warm Marimba, analytical mid-high range", 
        "program": 12,
        "pitch_range": (60, 84),
        "cc": {1: 60, 7: 100, 74: 30, 91: 20},
        "pan": 90,
        "timing_offset_ms": 0,
        "phrase_style": {
            "note_length_bias": 0.9,
            "velocity_range": (60, 100),
            "chord_density": "sparse"
        }
    }
}
'''
    
    transcript_logger_content = '''def log_transcript_entry(transcript_path, entry, mode="a", fmt="text"):
    """Simple transcript logging"""
    
    agent = entry.get("agent", "Unknown")
    time_sig = entry.get("time_signature", "")
    voice_name = entry.get("voice_name", "")
    intent = entry.get("intent", "")
    
    line = f"{agent} | {time_sig} | {voice_name} | Intent: {intent}\\n"
    
    with open(transcript_path, mode) as f:
        f.write(line)
    
    print(f"Logged transcript entry for {agent}")
'''
    
    # Write minimal files
    with open("render_pipeline.py", "w") as f:
        f.write(render_pipeline_content)
    
    with open("voice_profiles.py", "w") as f:
        f.write(voice_profiles_content)
        
    with open("transcript_logger.py", "w") as f:
        f.write(transcript_logger_content)
    
    print("✓ Created minimal pipeline files")

def main():
    files_exist = check_files()
    
    if not files_exist:
        print("\n🛠️ Some pipeline files are missing. Creating minimal versions...")
        create_minimal_pipeline()
    
    # Test direct processing
    direct_file, extended_file = test_direct_midi_processing()
    
    print(f"\n🎵 Test files created:")
    print(f"  {direct_file} - Direct copy (should be ultra-short)")
    print(f"  {extended_file} - Manually extended (should be longer)")
    print(f"\nPlay both files to see if manual extension works!")

if __name__ == "__main__":
    main()

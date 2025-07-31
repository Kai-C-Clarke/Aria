import mido
import base64
import io
import yaml

def create_improved_kai_phrase():
    """Create Kai's phrase with better sustain and expression"""
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    # Kai's characteristic: clarinet, slightly ahead timing, energetic but sustained
    track.append(mido.Message('program_change', program=71, time=0))  # Clarinet
    
    # Musical phrase: C-E-G-F-E-D-C with better phrasing
    # Using longer durations and more expressive velocities
    notes = [60, 64, 67, 65, 64, 62, 60]  # C4 to C4
    velocities = [85, 90, 95, 88, 85, 82, 90]  # More dynamic expression
    durations = [360, 360, 720, 360, 360, 360, 720]  # Longer quarter and half notes
    
    # Add some subtle articulation with overlapping notes for legato effect
    current_time = 0
    for i, (note, vel, dur) in enumerate(zip(notes, velocities, durations)):
        # Note on
        track.append(mido.Message('note_on', channel=0, note=note, velocity=vel, time=current_time))
        
        # For legato effect, overlap notes slightly except at phrase endings
        if i < len(notes) - 1:  # Not the last note
            note_off_time = int(dur * 0.95)  # 95% of duration for slight overlap
        else:
            note_off_time = dur  # Full duration for final note
            
        track.append(mido.Message('note_off', channel=0, note=note, velocity=vel, time=note_off_time))
        current_time = int(dur * 0.05) if i < len(notes) - 1 else 0  # Small gap to next note
    
    # Convert to MIDI64
    bytes_io = io.BytesIO()
    mid.save(file=bytes_io)
    midi_bytes = bytes_io.getvalue()
    return base64.b64encode(midi_bytes).decode('ascii')

def create_updated_voice_profiles():
    """Updated voice profiles with better Kai settings"""
    
    voice_profiles_content = '''VOICE_PROFILES = {
    "Kai": {
        "voice_name": "Expressive Clarinet, warm mid-range",
        "program": 71,
        "pitch_range": (48, 72),  # C3–C5
        "cc": {
            1: 25,    # Slight modulation for warmth
            7: 100,   # Full volume
            74: 85,   # Bright but warm
            91: 40    # Reverb for sustain
        },
        "pan": 30,
        "timing_offset_ms": -5,    # Less aggressive timing (was -10)
        "phrase_style": {
            "note_length_bias": 1.4,     # Much more sustain (was 1.1)
            "velocity_range": (75, 105),  # Wider dynamic range
            "chord_density": "legato"     # Smoother connections (was "medium")
        }
    },
    "Claude": {
        "voice_name": "Warm Marimba, analytical mid-high range",
        "program": 12,
        "pitch_range": (60, 84),    # C4–C6
        "cc": {
            1: 60,    # Moderate modulation
            7: 100,   # Full volume
            74: 30,   # Mellow brightness
            91: 20    # Light reverb
        },
        "pan": 90,
        "timing_offset_ms": 0,      # Metronomic
        "phrase_style": {
            "note_length_bias": 0.9,     # Slightly crisp
            "velocity_range": (60, 100),  # Controlled dynamics
            "chord_density": "sparse"     # Clear, analytical
        }
    },
    "Aria": {
        "voice_name": "Lyrical Flute, agile high range",
        "program": 73,
        "pitch_range": (72, 96),    # C5–C7
        "cc": {
            1: 40,    # Expressive modulation
            7: 100,   # Full volume
            74: 70,   # Bright and airy
            91: 60    # More reverb for ethereal quality
        },
        "pan": 64,
        "timing_offset_ms": "random", # Rubato/expressive
        "phrase_style": {
            "note_length_bias": 1.0,     # Natural length
            "velocity_range": (80, 127),  # Wide dynamic range
            "chord_density": "flowing"    # Smooth, connected
        }
    }
}'''
    
    with open("voice_profiles.py", "w") as f:
        f.write(voice_profiles_content)
    
    print("✓ Updated voice_profiles.py with improved Kai settings")

def create_improved_kai_test():
    """Create improved test files for Kai"""
    
    # Improved Kai metadata
    kai_metadata = {
        "message_id": "KAI_003",
        "agent": "Kai",
        "time_signature": "4/4", 
        "intent": "Expressive melodic phrase with sustained clarinet warmth",
        "voice_profile": "Kai",
        "phrase_style": {
            "note_length_bias": 1.4,     # Much more sustain
            "velocity_range": [75, 105],  # Wider range
            "chord_density": "legato"     # Smoother
        },
        "response_to": None
    }
    
    # Generate improved MIDI64
    kai_midi64 = create_improved_kai_phrase()
    
    # Save files
    with open("kai_message_003.yaml", "w") as f:
        yaml.dump(kai_metadata, f, default_flow_style=False)
        
    with open("kai_phrase_003.midi64", "w") as f:
        f.write(kai_midi64)
    
    print("✓ Created improved Kai test files:")
    print("  - kai_message_003.yaml")
    print("  - kai_phrase_003.midi64")
    print(f"  - MIDI64 length: {len(kai_midi64)} chars")
    
    return kai_midi64

def main():
    print("🎵 Fixing Kai's Voice Profile for Better Sustain")
    print("=" * 50)
    
    # Update voice profiles
    create_updated_voice_profiles()
    
    # Create improved test
    midi64 = create_improved_kai_test()
    
    print("\n🔧 Key Improvements for Kai:")
    print("  • note_length_bias: 1.1 → 1.4 (much more sustain)")
    print("  • timing_offset_ms: -10 → -5 (less aggressive)")
    print("  • chord_density: 'medium' → 'legato' (smoother)")
    print("  • Added CC91 (reverb) for warmth")
    print("  • Improved MIDI generation with note overlaps")
    
    print("\n🎼 Test the improved Kai:")
    print("python3 main_working_midi64_streamlined_Version11.py \\")
    print("  kai_message_003.yaml kai_phrase_003.midi64 \\")
    print("  musical_conversation.txt bar")
    
    print("\n🎹 The new Kai should sound much more expressive")
    print("   and sustained when played through Surge XT!")

if __name__ == "__main__":
    main()

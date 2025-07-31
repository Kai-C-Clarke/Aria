import mido
import base64
import io

def analyze_midi64_timing(midi64_text, name):
    """Analyze the actual timing in a MIDI64 file"""
    
    print(f"\n=== Analyzing {name} MIDI Timing ===")
    
    # Decode MIDI64
    midi_bytes = base64.b64decode(midi64_text)
    mid = mido.MidiFile(file=io.BytesIO(midi_bytes))
    
    print(f"Ticks per beat: {mid.ticks_per_beat}")
    print(f"Number of tracks: {len(mid.tracks)}")
    
    # Analyze the track
    track = mid.tracks[0]
    print(f"Number of messages: {len(track)}")
    
    current_time = 0
    note_events = []
    
    for msg in track:
        current_time += msg.time
        if msg.type == 'note_on' and msg.velocity > 0:
            note_events.append(('on', current_time, msg.note, msg.velocity))
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            note_events.append(('off', current_time, msg.note, msg.velocity))
        else:
            print(f"  {current_time:4d}: {msg}")
    
    # Calculate note durations
    active_notes = {}
    note_durations = []
    
    for event_type, time, note, velocity in note_events:
        if event_type == 'on':
            active_notes[note] = time
            print(f"  {time:4d}: Note {note} ON  (vel {velocity})")
        else:
            if note in active_notes:
                duration = time - active_notes[note]
                note_durations.append(duration)
                print(f"  {time:4d}: Note {note} OFF (duration: {duration} ticks)")
                del active_notes[note]
    
    if note_durations:
        avg_duration = sum(note_durations) / len(note_durations)
        print(f"\nNote Duration Analysis:")
        print(f"  Individual durations: {note_durations}")
        print(f"  Average duration: {avg_duration:.1f} ticks")
        print(f"  In beats (÷{mid.ticks_per_beat}): {avg_duration/mid.ticks_per_beat:.2f}")
        
        # Convert to milliseconds (assuming 120 BPM)
        ms_per_tick = (60000 / 120) / mid.ticks_per_beat  # 60000ms/min ÷ 120bpm ÷ ticks_per_beat
        avg_ms = avg_duration * ms_per_tick
        print(f"  Approximate duration: {avg_ms:.0f}ms (at 120 BPM)")
    
    return note_durations

def create_manually_sustained_kai():
    """Create Kai phrase with manually extended note durations"""
    
    mid = mido.MidiFile(ticks_per_beat=480)  # Higher resolution
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    # Kai's characteristic: clarinet
    track.append(mido.Message('program_change', program=71, time=0))
    
    # Much longer note durations - force sustain at MIDI level
    notes = [60, 64, 67, 65, 64, 62, 60]  # C4 to C4
    velocities = [85, 90, 95, 88, 85, 82, 90]
    durations = [960, 960, 1440, 960, 960, 960, 1440]  # Much longer (2x-3x longer)
    
    print("Creating sustained Kai phrase with durations:", durations)
    
    for note, vel, dur in zip(notes, velocities, durations):
        track.append(mido.Message('note_on', channel=0, note=note, velocity=vel, time=0))
        track.append(mido.Message('note_off', channel=0, note=note, velocity=vel, time=dur))
    
    # Convert to MIDI64
    bytes_io = io.BytesIO()
    mid.save(file=bytes_io)
    midi_bytes = bytes_io.getvalue()
    return base64.b64encode(midi_bytes).decode('ascii')

def main():
    print("🔍 Debugging Kai's Short Note Problem")
    
    # Load the current Kai MIDI64
    with open("kai_phrase_003.midi64", "r") as f:
        kai_midi64 = f.read().strip()
    
    # Analyze current timing
    durations = analyze_midi64_timing(kai_midi64, "Current Kai")
    
    # Create manually sustained version
    print("\n" + "="*50)
    print("Creating manually sustained Kai phrase...")
    sustained_midi64 = create_manually_sustained_kai()
    
    # Analyze new timing
    sustained_durations = analyze_midi64_timing(sustained_midi64, "Sustained Kai")
    
    # Save the sustained version
    with open("kai_phrase_sustained.midi64", "w") as f:
        f.write(sustained_midi64)
    
    print(f"\n📁 Saved sustained version to: kai_phrase_sustained.midi64")
    print(f"📏 MIDI64 length: {len(sustained_midi64)} chars")
    
    # Create metadata for sustained version
    import yaml
    sustained_metadata = {
        "message_id": "KAI_SUSTAINED",
        "agent": "Kai",
        "time_signature": "4/4", 
        "intent": "Manually sustained clarinet phrase (bypass voice profile)",
        "voice_profile": "Kai",
        "phrase_style": {
            "note_length_bias": 1.0,  # Not needed since manually sustained
            "velocity_range": [75, 105],
            "chord_density": "legato"
        },
        "response_to": None
    }
    
    with open("kai_message_sustained.yaml", "w") as f:
        yaml.dump(sustained_metadata, f, default_flow_style=False)
    
    print("\n🧪 Test the sustained version:")
    print("python3 main_working_midi64_streamlined_Version11.py \\")
    print("  kai_message_sustained.yaml kai_phrase_sustained.midi64 \\")
    print("  musical_conversation.txt bar")
    
    if durations and sustained_durations:
        improvement = (sum(sustained_durations) / len(sustained_durations)) / (sum(durations) / len(durations))
        print(f"\n📈 Duration improvement: {improvement:.1f}x longer notes")

if __name__ == "__main__":
    main()

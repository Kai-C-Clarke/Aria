import base64
import tempfile
from mido import MidiFile
import numpy as np
import sounddevice as sd
import time

SAMPLE_RATE = 44100

def hz_for_midi_note(midi_note):
    """Convert MIDI note number to frequency in Hz"""
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))

def midi64_to_frequencies(midi64_string):
    """Convert MIDI64 to frequency events"""
    midi_data = base64.b64decode(midi64_string)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mid") as tmp_midi_file:
        tmp_midi_file.write(midi_data)
        midi_path = tmp_midi_file.name

    midi_file = MidiFile(midi_path)
    note_events = []
    time_accumulator = 0
    for track in midi_file.tracks:
        for msg in track:
            time_accumulator += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                note_events.append({
                    'note': msg.note,
                    'freq': hz_for_midi_note(msg.note),
                    'time': time_accumulator / 1000.0
                })
    return note_events

def play_frequencies(events):
    """Play frequency events using simple sine wave synthesis"""
    if not events:
        print("🔇 No frequency events to play")
        return
    
    print(f"🎵 Playing {len(events)} frequency events...")
    
    # Simple synthesis approach
    duration = 0.5  # seconds per note
    
    for i, event in enumerate(events):
        freq = event['freq']
        print(f"🎼 Note {i+1}: {freq:.2f} Hz (MIDI {event['note']})")
        
        # Generate sine wave
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
        wave = 0.3 * np.sin(2 * np.pi * freq * t)
        
        # Simple envelope
        envelope = np.linspace(1.0, 0.1, len(t))
        wave = wave * envelope
        
        # Play
        sd.play(wave, SAMPLE_RATE)
        sd.wait()  # Wait for note to finish
        
        time.sleep(0.1)  # Brief gap between notes

if __name__ == "__main__":
    # Test with the provided MIDI64
    midi64_msg = "TVRoZAAAAAYAAQABAeBNVHJrAAAANwD/UQMHoSAA/1gEBAIYCACwAUwAsEplALALPwCQPGRggDwAYJBAZGCAQABgkENkYIBDAAD/LwA="
    print("🎭 Testing MIDI64 audio playback...")
    events = midi64_to_frequencies(midi64_msg)
    play_frequencies(events)
    print("✅ Audio test complete!")

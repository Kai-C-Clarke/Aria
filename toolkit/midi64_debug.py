
import base64
import tempfile
from mido import MidiFile

def midi64_to_audio_playback(midi64_string):
    # Step 1: Decode base64 MIDI64 string to bytes
    midi_data = base64.b64decode(midi64_string)

    # Step 2: Write to temporary .mid file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mid") as tmp_midi_file:
        tmp_midi_file.write(midi_data)
        midi_path = tmp_midi_file.name

    print(f"Temporary MIDI file saved to: {midi_path}")

    # Step 3: Parse .mid to extract note events (simplified for logging)
    midi_file = MidiFile(midi_path)
    note_events = []
    for track in midi_file.tracks:
        time_accumulator = 0
        for msg in track:
            time_accumulator += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                note_events.append({
                    'note': msg.note,
                    'time': round(time_accumulator / 1000.0, 3)
                })

    # Print note events (can forward these to your synth)
    print("Extracted Note Events:")
    for event in note_events:
        print(f"Note: {event['note']} at {event['time']}s")

    return note_events

# Example usage:
if __name__ == "__main__":
    test_midi64 = "TVRoZAAAAAYAAQABAeBNVHJrAAAANwD/UQMHoSAA/1gEBAIYCACwAUwAsEplALALPwCQPGRggDwAYJBAZGCAQABgkENkYIBDAAD/LwA="
    midi64_to_audio_playback(test_midi64)

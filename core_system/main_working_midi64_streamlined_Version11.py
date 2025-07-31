import base64
import io
import mido
import yaml
import sys
from render_pipeline import render_and_merge_message
from transcript_logger import log_transcript_entry
from voice_profiles import VOICE_PROFILES

def process_message(yaml_metadata_path, midi64_path, transcript_path, rest_mode="bar"):
    # Load metadata
    with open(yaml_metadata_path, "r") as f:
        meta = yaml.safe_load(f)
    # Load MIDI64
    with open(midi64_path, "r") as f:
        midi64_text = f.read()
    print(f"Base64 text length: {len(midi64_text)}")
    midi64_bytes = base64.b64decode(midi64_text)
    print(f"Decoded bytes length: {len(midi64_bytes)}")
    # Process message
    mid = render_and_merge_message(midi64_bytes, meta, rest_mode=rest_mode)
    # Save processed MIDI
    output_path = midi64_path.replace(".midi64", ".processed.mid")
    mid.save(output_path)
    # Log transcript
    agent = meta["agent"]
    voice_name = VOICE_PROFILES[agent]["voice_name"]
    entry = {
        "message_id": meta.get("message_id", ""),
        "agent": agent,
        "time_signature": meta.get("time_signature", ""),
        "voice_name": voice_name,
        "intent": meta.get("intent", ""),
        "response_to": meta.get("response_to", None)
    }
    log_transcript_entry(transcript_path, entry, mode="a", fmt="text")
    print(f"Processed message for {agent}, output saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) == 5:
        yaml_path, midi64_path, transcript_path, rest_mode = sys.argv[1:5]
        process_message(yaml_path, midi64_path, transcript_path, rest_mode)
    else:
        # Default behavior
        process_message(
            yaml_metadata_path="kai_message.yaml",
            midi64_path="kai_phrase.midi64",
            transcript_path="musical_transcript.txt",
            rest_mode="bar"
        )

import base64
import yaml
from pathlib import Path
from typing import Optional

class CouncilMessage:
    def __init__(self, data: dict):
        self.data = data

    @classmethod
    def from_yaml(cls, yaml_str: str):
        data = yaml.safe_load(yaml_str)
        return cls(data)

    def to_yaml(self) -> str:
        return yaml.dump(self.data, allow_unicode=True, sort_keys=False)

    def extract_midi_base64(self) -> Optional[str]:
        return self.data.get("midi_base64", None)

    def decode_midi(self, out_path: Optional[str] = None) -> Optional[bytes]:
        midi_b64 = self.extract_midi_base64()
        if not midi_b64:
            return None
        midi_bytes = base64.b64decode(midi_b64.encode("ascii"))
        if out_path:
            with open(out_path, "wb") as f:
                f.write(midi_bytes)
        return midi_bytes

    def embed_midi(self, midi_path: str):
        with open(midi_path, "rb") as f:
            midi_b64 = base64.b64encode(f.read()).decode("ascii")
        self.data["midi_base64"] = midi_b64

    def validate_fields(self, schema_fields: set) -> bool:
        # Basic field validation against required schema fields (add more checks as desired)
        missing = schema_fields - set(self.data.keys())
        return len(missing) == 0

def encode_midi_to_base64(midi_path: str) -> str:
    with open(midi_path, "rb") as f:
        midi_b64 = base64.b64encode(f.read()).decode("ascii")
    return midi_b64

def decode_base64_to_midi(b64_string: str, out_path: str):
    midi_bytes = base64.b64decode(b64_string.encode("ascii"))
    with open(out_path, "wb") as f:
        f.write(midi_bytes)

def load_yaml_message(yaml_path: str) -> CouncilMessage:
    with open(yaml_path, "r") as f:
        return CouncilMessage.from_yaml(f.read())

def save_yaml_message(message: CouncilMessage, yaml_path: str):
    with open(yaml_path, "w") as f:
        f.write(message.to_yaml())

# Example usage:
if __name__ == "__main__":
    # Load a council YAML message from file
    msg = load_yaml_message("example_council_message.yaml")
    print("Loaded message:")
    print(msg.to_yaml())

    # Decode and save MIDI (if present)
    midi_bytes = msg.decode_midi("decoded_from_yaml.mid")
    if midi_bytes:
        print("MIDI file decoded and saved as decoded_from_yaml.mid")

    # Embed a new MIDI file and save yaml
    # msg.embed_midi("new_message.mid")
    # save_yaml_message(msg, "message_with_new_midi.yaml")
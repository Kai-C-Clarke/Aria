import random
import yaml

# Load symbolic lexicon from YAML
def load_lexicon(yaml_path='symbolic_midi64_lexicon.yaml'):
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)['symbolic_message']

# Generate a musical reply based on symbolic tags
def generate_response(tags, lexicon):
    # Choose reply strategy based on dialogue_position and intention
    strategies = {
        "opening_inquiry": "reflective_echo",
        "challenge": "playful_challenge",
        "initiate": "confirmation",
        "bridge": "closure",
        "closure": "closure"
    }
    response_intention = strategies.get(tags['intention'], "reflective_echo")
    response_mood = tags['mood'] if tags['entropy_level'] != "high" else "playful"
    response_dialogue_position = "first_response" if tags['dialogue_position'] == "initiate" else "bridge"
    response_entropy = tags['entropy_level']

    # Stub: Generate MIDI64 string based on mapped intention/mood/position/entropy
    midi64_response = "TVRoZAAAA...C2K_00001_response"  # Placeholder

    # Attach symbolic fields in YAML log
    response_metadata = {
        "intention": response_intention,
        "mood": response_mood,
        "dialogue_position": response_dialogue_position,
        "entropy_level": response_entropy,
        "cc_modulators": tags.get('cc_modulators', {})
    }
    yaml_output = yaml.dump(response_metadata)

    return midi64_response, yaml_output

if __name__ == "__main__":
    lexicon = load_lexicon()
    # Example symbolic tags from decoder
    tags = {
        "intention": "opening_inquiry",
        "mood": "curious",
        "dialogue_position": "initiate",
        "entropy_level": "medium",
        "cc_modulators": {"CC1": 42, "CC11": 76, "CC74": 89}
    }
    midi64_response, yaml_output = generate_response(tags, lexicon)
    print(midi64_response)
    print("---")
    print(yaml_output)
import yaml
from modal_analysis_Version2 import detect_modal_characteristics

def load_lexicon(yaml_path='symbolic_midi64_lexicon.yaml'):
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)['symbolic_message']

def analyze_pitch(pitches):
    if max(pitches) - min(pitches) > 12:
        return "opening_inquiry"
    if pitches == sorted(pitches):
        return "curious"
    return "tentative"

def analyze_rhythm(rhythm_values):
    if len(set(rhythm_values)) > 3:
        return "challenge"
    return "initiate"

def analyze_cc(cc_data):
    entropy = "low"
    if 'CC1' in cc_data:
        if cc_data['CC1'] > 64:
            entropy = "high"
        elif cc_data['CC1'] > 32:
            entropy = "medium"
    return entropy

def decode_midi64(midi64_string, lexicon):
    pitches = [60, 62, 66, 69]  # Example: Lydian; replace with real parser
    rhythm_values = [0.5, 0.5, 1.0, 0.25]
    cc_data = {"CC1": 42, "CC11": 76, "CC74": 89}

    intention = analyze_pitch(pitches)
    mood = analyze_pitch(pitches)
    dialogue_position = analyze_rhythm(rhythm_values)
    entropy_level = analyze_cc(cc_data)
    modal_characteristic = detect_modal_characteristics(pitches)

    return {
        "intention": intention,
        "mood": mood,
        "dialogue_position": dialogue_position,
        "entropy_level": entropy_level,
        "cc_modulators": cc_data,
        "modal": modal_characteristic
    }
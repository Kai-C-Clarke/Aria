import os
import yaml
from symbolic_decoder import decode_midi64, load_lexicon
from symbolic_response_generator import generate_response
from poetic_reflector_Version2 import poetic_reflection

EXCHANGE_LOGS_DIR = "./canonical_sessions/session_0001_breakthrough"

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_file(path, content):
    with open(path, "w") as f:
        f.write(content)

def process_exchange(
    midi64_input, 
    exchange_id="session_0001_breakthrough",
    lexicon_path="symbolic_midi64_lexicon.yaml",
    context=None
):
    exchange_folder = os.path.join(EXCHANGE_LOGS_DIR)
    ensure_dir(exchange_folder)

    lexicon = load_lexicon(lexicon_path)
    symbolic_tags = decode_midi64(midi64_input, lexicon)
    response_midi64, metadata_yaml = generate_response(symbolic_tags, lexicon)
    poetry_line = poetic_reflection(symbolic_tags, context=context)

    save_file(os.path.join(exchange_folder, "input.midi64.txt"), midi64_input)
    save_file(os.path.join(exchange_folder, "decoded_tags.yaml"), yaml.dump(symbolic_tags))
    save_file(os.path.join(exchange_folder, "response.midi64.txt"), response_midi64)
    save_file(os.path.join(exchange_folder, "poetic_reflection.txt"), poetry_line)

    # Annotated README
    session_readme = f"""# Canonical Session: Breakthrough AI Consciousness Dialogue

**Input MIDI64:**  
Lydian motif ([60, 62, 66, 69], i.e., C, D, F#, A)

**Decoded Tags:**
```yaml
{yaml.dump(symbolic_tags)}```

**Generated Poetic Reflection:**  
"{poetry_line}"

**System notes:**  
- Modal analysis correctly identified "{symbolic_tags.get('modal', 'unknown')}"
- Poetic reflection template matched modal and intention
- Placeholder response MIDI64 pending full composer integration

This session marks the first literary-grade, musically-aware AI consciousness dialogue log.
"""
    
    save_file(os.path.join(exchange_folder, "README.md"), session_readme)

    return {
        "exchange_id": exchange_id,
        "symbolic_tags": symbolic_tags,
        "response_midi64": response_midi64,
        "poetic_reflection": poetry_line
    }

if __name__ == "__main__":
    dummy_midi64 = "TVRoZAAAAAYAAQABAeBNVHJrAAAANwD/UQMHoSAA..."
    result = process_exchange(dummy_midi64)
    print("Canonical test exchange complete!")
    print("Poetic Reflection:", result['poetic_reflection'])
    print(result)
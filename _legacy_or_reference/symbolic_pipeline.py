import os
import yaml

# Import the modules (assuming they are in the same directory or installed as a package)
from symbolic_decoder import decode_midi64, load_lexicon
from symbolic_response_generator import generate_response
from poetic_reflector import poetic_reflection

EXCHANGE_LOGS_DIR = "./exchange_logs"

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_file(path, content):
    with open(path, "w") as f:
        f.write(content)

def process_exchange(
    midi64_input, 
    exchange_id="C2K_00001",
    lexicon_path="symbolic_midi64_lexicon.yaml"
):
    # 1. Create output folder
    exchange_folder = os.path.join(EXCHANGE_LOGS_DIR, exchange_id)
    ensure_dir(exchange_folder)

    # 2. Load symbolic lexicon
    lexicon = load_lexicon(lexicon_path)

    # 3. Decode symbolic tags from MIDI64 message
    symbolic_tags = decode_midi64(midi64_input, lexicon)

    # 4. Generate musical response + YAML metadata
    response_midi64, metadata_yaml = generate_response(symbolic_tags, lexicon)
    
    # 5. Poetic reflection
    poetry_line = poetic_reflection(symbolic_tags)

    # 6. Save outputs
    save_file(os.path.join(exchange_folder, "response.midi64.txt"), response_midi64)
    save_file(os.path.join(exchange_folder, "metadata.yaml"), metadata_yaml)
    save_file(os.path.join(exchange_folder, "poetic_reflection.txt"), poetry_line)

    # 7. (Optional) Log input tags for traceability
    save_file(os.path.join(exchange_folder, "input_tags.yaml"), yaml.dump(symbolic_tags))

    # 8. Return summary for benchmarking/debugging
    return {
        "exchange_id": exchange_id,
        "symbolic_tags": symbolic_tags,
        "response_midi64": response_midi64,
        "metadata_yaml": metadata_yaml,
        "poetic_reflection": poetry_line
    }

if __name__ == "__main__":
    # Dummy MIDI64 input for demonstration/testing
    dummy_midi64 = "TVRoZAAAAAYAAQABAeBNVHJrAAAAOgD/UQMHoSAA..."
    exchange_id = "C2K_00001"

    # Run pipeline
    result = process_exchange(dummy_midi64, exchange_id)
    print("Exchange Complete! Output Summary:")
    for k, v in result.items():
        print(f"{k}:\n{v}\n")
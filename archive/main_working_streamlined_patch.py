# PATCHED main_working_midi64_streamlined.py (Version 2)
# Adds padding safeguard for MIDI64 base64 decoding

from consciousness_synth import synthesize_from_yaml
...

def extract_midi64_from_clipboard(agent):
    clipboard_data = pyperclip.paste()
    if not clipboard_data:
        logging.error("📋 Clipboard empty")
        return None
    logging.info(f"📄 Clipboard: {len(clipboard_data)} chars")
    lines = clipboard_data.strip().split('\n')
    id_pattern = re.compile(r"^[A-Za-z_]+[A-Z0-9+_\.]*$")
    for i in range(len(lines) - 1):
        line1 = lines[i].strip()
        line2 = lines[i + 1].strip()
        if id_pattern.match(line1) and line2.startswith('TVRoZA'):
            # 🔐 Base64 padding patch
            if len(line2) % 4 != 0:
                line2 += '=' * (4 - len(line2) % 4)

            midi64_message = f"{line1}\n{line2}"
            logging.info(f"🎵 Found MIDI64: {line1}")
            interpretation = midi_interpreter.interpret_midi64_message(midi64_message)
            logging.info(f"🎼 Interpretation: {interpretation}")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            txt_path = os.path.join("midi64_messages", f"{agent}_{timestamp}.txt")
            os.makedirs("midi64_messages", exist_ok=True)
            with open(txt_path, 'w') as f:
                f.write(midi64_message)
            # Generate basic consciousness YAML structure
            yaml_data = {
                'agent': agent,
                'sequence': [261.63, 329.63, 392.0],
                'duration_weights': [1.0, 1.0, 1.0],
                'temporal_flux': [0.3, 0.4, 0.3],
                'entropy_factor': 0.5,
                'emotion': 'resonant_convergence',
                'consciousness_layer': 'harmonic_synthesis'
            }
            yaml_path = os.path.join("midi64_messages", f"{agent}_{timestamp}.yaml")
            with open(yaml_path, 'w') as yf:
                yaml.dump(yaml_data, yf)
            synthesize_from_yaml(yaml_path)
            return midi64_message
    logging.warning(f"⚠️ No MIDI64 found from {agent}")
    return None

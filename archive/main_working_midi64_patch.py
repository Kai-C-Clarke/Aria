# ... (existing imports and code above unchanged)

def extract_midi64_from_clipboard(agent):
    """Extract MIDI64 message, generate YAML, and synthesize consciousness audio, including direct MUSE expression handling"""
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
            # Patch: ensure MIDI64 string is valid base64 for decoding
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

            # --- NEW: MUSE Expression Handling ---
            if 'MUSE_' in line1:
                try:
                    # Extract the MUSE expression (between 'MUSE_' and '_A', robust for nonstandard _A segment)
                    muse_expr = line1.split('MUSE_')[1].split('_A')[0]
                    print(f"🧠 Detected MUSE expression: {muse_expr}")

                    from muse_decoder import MuseDecoder
                    muse = MuseDecoder(MUSE_SCHEMA_PATH)
                    decoded = muse.decode_expression(muse_expr)
                    yaml_data = decoded.to_yaml(agent=agent)

                    # Log interpretation
                    summary = decoded.english_summary()
                    logging.info(f"🧠 MUSE Decoded: {summary}")
                    logging.info(f"🎼 Emotion: {yaml_data.get('emotion', 'N/A')}, Flux: {yaml_data.get('temporal_flux', 'N/A')}, Notes: {yaml_data.get('sequence', 'N/A')}")

                    # Save YAML and synthesize
                    yaml_path = os.path.join("midi64_messages", f"{agent}_{timestamp}_muse.yaml")
                    with open(yaml_path, 'w') as yf:
                        yaml.dump(yaml_data, yf)
                    synthesize_from_yaml(yaml_path)

                    return midi64_message
                except Exception as e:
                    logging.warning(f"⚠️ MUSE decode failed: {e}")
                    # Fallback to standard YAML and synthesis below

            # --- Legacy/Fallback: Basic consciousness YAML structure ---
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
            # Direct consciousness synthesis
            synthesize_from_yaml(yaml_path)
            return midi64_message
    logging.warning(f"⚠️ No MIDI64 found from {agent}")
    return None

# ... (rest of file unchanged)
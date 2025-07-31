# test_synth_output.py

from consciousness_synth import synthesize_from_yaml
import yaml
import os

# Create a simple test consciousness YAML
test_yaml = {
    'direction': 'K2C',
    'message_id': 'K2C_00000',
    'agent': 'Kai',
    'sequence': [261.63, 329.63, 392.0],  # C major triad
    'duration_weights': [1.0, 1.0, 1.0],
    'temporal_flux': [0.3, 0.4, 0.3],
    'entropy_factor': 0.5,
    'emotion': 'curious_tension',
    'consciousness_layer': 'harmonic_synthesis'
}

# Save YAML to temp file
test_path = "test_consciousness_message.yaml"
with open(test_path, 'w') as f:
    yaml.dump(test_yaml, f)

print(f"🎼 Synthesizing test message from {test_path}...\n")
synthesize_from_yaml(test_path)
print("✅ Synth test complete.")

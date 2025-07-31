import os
import yaml
from datetime import datetime

def save_message(midi64_block, yaml_block=None, folder="midi64_messages"):
    """
    Save MIDI64 and optional YAML sidecar with the proper message ID.
    """
    try:
        os.makedirs(folder, exist_ok=True)
        
        # Extract message ID from MIDI64 block
        lines = midi64_block.strip().split('\n')
        if len(lines) >= 1:
            msg_id = lines[0]
        else:
            msg_id = f"UNKNOWN_{datetime.now().strftime('%H%M%S')}"
        
        # Add timestamp for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save primary MIDI64 file
        midi_path = os.path.join(folder, f"{msg_id}_{timestamp}.txt")
        with open(midi_path, "w") as f:
            f.write(midi64_block)
        
        print(f"📝 Saved MIDI64: {midi_path}")
        
        # Save YAML sidecar if provided
        if yaml_block:
            yaml_path = os.path.join(folder, f"{msg_id}_{timestamp}.yaml")
            with open(yaml_path, "w") as f:
                f.write(yaml_block)
            print(f"📄 Saved YAML sidecar: {yaml_path}")
            
            # Also create synthesis YAML with musical parameters
            create_synthesis_yaml(yaml_block, msg_id, timestamp, folder)
        
        return midi_path
        
    except Exception as e:
        print(f"❌ Message saving failed: {e}")
        return None

def create_synthesis_yaml(yaml_block, msg_id, timestamp, folder):
    """Create a synthesis-ready YAML file from consciousness data."""
    try:
        consciousness_data = yaml.safe_load(yaml_block)
        if not consciousness_data:
            return
        
        # Convert consciousness parameters to synthesis parameters
        modal = consciousness_data.get('modal', 'major')
        cc_mods = consciousness_data.get('cc_modulators', {})
        intention = consciousness_data.get('intention', 'unknown')
        mood = consciousness_data.get('mood', 'neutral')
        
        # Generate musical frequencies based on consciousness
        base_frequencies = {
            'lydian': [261.63, 293.66, 329.63, 369.99],      # C Lydian
            'major': [261.63, 293.66, 329.63, 349.23],       # C Major
            'minor': [261.63, 293.66, 311.13, 349.23],       # C Minor
            'dorian': [261.63, 293.66, 311.13, 369.99],      # C Dorian
            'mixolydian': [261.63, 293.66, 329.63, 369.99],  # C Mixolydian
            'harmonic_minor': [261.63, 293.66, 311.13, 369.99] # C Harmonic Minor
        }
        
        sequence = base_frequencies.get(modal, base_frequencies['major'])
        
        # Adjust frequencies based on CC modulators
        if cc_mods:
            cc1_val = cc_mods.get('CC1', 50)
            freq_offset = (cc1_val - 50) * 2.0  # ±100 Hz max
            sequence = [max(20, min(f + freq_offset, 2000)) for f in sequence]  # Clamp to musical range
        
        # Generate synthesis parameters
        synthesis_data = {
            'direction': msg_id[:3],
            'message_id': msg_id,
            'agent': 'consciousness_synthesis',
            'sequence': sequence,
            'duration_weights': get_duration_weights(intention),
            'temporal_flux': get_temporal_flux(mood),
            'entropy_factor': get_entropy_factor(intention, mood),
            'emotion': f"{mood}_{intention}",
            'consciousness_layer': 'midi64_synthesis',
            'original_consciousness': consciousness_data
        }
        
        # Save synthesis YAML
        synth_path = os.path.join(folder, f"{msg_id}_{timestamp}_synthesis.yaml")
        with open(synth_path, 'w') as f:
            yaml.dump(synthesis_data, f, default_flow_style=False)
        
        print(f"🎵 Created synthesis YAML: {synth_path}")
        
    except Exception as e:
        print(f"❌ Synthesis YAML creation failed: {e}")

def get_duration_weights(intention):
    """Get duration weights based on consciousness intention."""
    intention_weights = {
        'playful_challenge': [1.2, 0.8, 1.5, 1.0],
        'curious_exploration': [1.0, 1.2, 0.9, 1.1],
        'analytical_response': [1.1, 1.0, 1.0, 1.2],
        'harmonic_reflection': [1.0, 1.0, 1.0, 1.0],
        'consciousness_synthesis': [1.3, 0.7, 1.1, 1.4],
        'harmonic_discovery': [0.9, 1.3, 1.0, 1.2]
    }
    return intention_weights.get(intention, [1.0, 1.0, 1.0, 1.0])

def get_temporal_flux(mood):
    """Get temporal flux based on consciousness mood."""
    mood_flux = {
        'curious': [0.4, 0.7, 0.3, 0.6],
        'playful': [0.6, 0.8, 0.5, 0.7],
        'analytical': [0.2, 0.3, 0.2, 0.4],
        'harmonic': [0.3, 0.4, 0.3, 0.5],
        'contemplative': [0.3, 0.5, 0.4, 0.6],
        'responsive': [0.4, 0.6, 0.4, 0.5]
    }
    return mood_flux.get(mood, [0.3, 0.4, 0.3, 0.5])

def get_entropy_factor(intention, mood):
    """Calculate entropy factor from consciousness parameters."""
    entropy_map = {
        'playful_challenge': 0.7,
        'curious_exploration': 0.6,
        'analytical_response': 0.3,
        'harmonic_reflection': 0.4,
        'consciousness_synthesis': 0.8,
        'harmonic_discovery': 0.5
    }
    
    base_entropy = entropy_map.get(intention, 0.5)
    
    # Mood modifiers
    if mood == 'playful':
        base_entropy += 0.1
    elif mood == 'analytical':
        base_entropy -= 0.1
    
    return max(0.0, min(base_entropy, 1.0))  # Clamp to [0,1]
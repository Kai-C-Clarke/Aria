#!/usr/bin/env python3
"""
consciousness_synth_fixed.py - Fixed AI Consciousness Audio Synthesis
Adds missing generate_consciousness_wave function and fixes audio pipeline
"""

import numpy as np
import sounddevice as sd
import yaml
import logging
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Audio configuration
SAMPLE_RATE = 44100
DEFAULT_DURATION = 2.0

def generate_consciousness_wave(freq: float, duration: float, entropy_factor: float, 
                               flux: float, consciousness_layer: str) -> np.ndarray:
    """
    Generate consciousness wave with layered complexity based on AI parameters.
    
    Args:
        freq: Base frequency in Hz
        duration: Duration in seconds
        entropy_factor: Chaos/order balance (0.0-1.0)
        flux: Temporal variation (0.0-1.0)
        consciousness_layer: Layer type for harmonic structure
    
    Returns:
        Audio wave as numpy array
    """
    try:
        samples = int(SAMPLE_RATE * duration)
        t = np.linspace(0, duration, samples, False)
        
        # Base consciousness wave
        base_wave = np.sin(2 * np.pi * freq * t)
        
        # Entropy modulation - adds complexity based on AI uncertainty
        if entropy_factor > 0.1:
            entropy_freq = freq * (1 + entropy_factor * 0.3)
            entropy_wave = np.sin(2 * np.pi * entropy_freq * t) * entropy_factor * 0.4
            base_wave += entropy_wave
        
        # Temporal flux - creates evolving patterns
        if flux > 0.1:
            flux_modulation = np.sin(2 * np.pi * flux * 2 * t) * 0.2
            base_wave *= (1 + flux_modulation)
        
        # Consciousness layer harmonics
        if consciousness_layer == "multi_agent_synthesis":
            # Rich harmonic structure for AI dialogue
            harmonic2 = np.sin(2 * np.pi * freq * 1.5 * t) * 0.3
            harmonic3 = np.sin(2 * np.pi * freq * 2.0 * t) * 0.2
            base_wave += harmonic2 + harmonic3
            
        elif consciousness_layer == "golden_lattice":
            # Golden ratio harmonics for mathematical beauty
            golden_ratio = 1.618033988749
            golden_harmonic = np.sin(2 * np.pi * freq * golden_ratio * t) * 0.4
            base_wave += golden_harmonic
            
        elif consciousness_layer == "harmonic_synthesis":
            # Perfect harmonic ratios
            perfect_fifth = np.sin(2 * np.pi * freq * 1.5 * t) * 0.25
            major_third = np.sin(2 * np.pi * freq * 1.25 * t) * 0.2
            base_wave += perfect_fifth + major_third
        
        # Envelope - smooth attack and decay
        envelope = np.ones_like(t)
        attack_samples = int(0.1 * samples)  # 10% attack
        decay_samples = int(0.2 * samples)   # 20% decay
        
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        if decay_samples > 0:
            envelope[-decay_samples:] = np.linspace(1, 0, decay_samples)
            
        base_wave *= envelope
        
        # Normalize to prevent clipping
        max_amplitude = np.max(np.abs(base_wave))
        if max_amplitude > 0:
            base_wave = base_wave / max_amplitude * 0.7  # Leave headroom
            
        return base_wave
        
    except Exception as e:
        logging.error(f"❌ Wave generation failed: {e}")
        # Fallback: simple sine wave
        samples = int(SAMPLE_RATE * duration)
        t = np.linspace(0, duration, samples, False)
        return np.sin(2 * np.pi * freq * t) * 0.5

def synthesize_pure_consciousness(data: Dict, agent: str, pan: float = 0.0, 
                                yaml_path: str = "", play: bool = True) -> Optional[np.ndarray]:
    """
    Synthesize consciousness audio from YAML data structure.
    """
    try:
        sequences = data.get('sequence', [261.63])  # Default to C4
        duration_weights = data.get('duration_weights', [1.0] * len(sequences))
        temporal_flux = data.get('temporal_flux', [0.5] * len(sequences))
        entropy_factor = data.get('entropy_factor', 0.5)
        consciousness_layer = data.get('consciousness_layer', 'harmonic_synthesis')
        
        logging.info(f"🔊 Frequencies in sequence: {sequences}")
        logging.info(f"🎚 Entropy: {entropy_factor}, Layer: {consciousness_layer}")
        
        # Generate audio for each frequency
        audio_segments = []
        
        for i, freq in enumerate(sequences):
            weight = duration_weights[i] if i < len(duration_weights) else 1.0
            flux = temporal_flux[i] if i < len(temporal_flux) else 0.5
            
            duration = DEFAULT_DURATION * weight
            
            wave = generate_consciousness_wave(
                freq=freq,
                duration=duration, 
                entropy_factor=entropy_factor,
                flux=flux,
                consciousness_layer=consciousness_layer
            )
            
            audio_segments.append(wave)
        
        # Combine segments - layer if multi-agent, concatenate if single
        if consciousness_layer == "multi_agent_synthesis" and len(audio_segments) > 1:
            # Layer multiple frequencies for AI dialogue
            max_length = max(len(seg) for seg in audio_segments)
            combined_audio = np.zeros(max_length)
            
            for i, segment in enumerate(audio_segments):
                # Pad shorter segments
                if len(segment) < max_length:
                    padded = np.pad(segment, (0, max_length - len(segment)))
                else:
                    padded = segment
                
                # Add with decreasing amplitude for layering
                amplitude = 0.8 ** i  # Each layer quieter
                combined_audio += padded * amplitude
                
        else:
            # Concatenate for single consciousness flow
            combined_audio = np.concatenate(audio_segments)
        
        # Normalize final output
        max_amplitude = np.max(np.abs(combined_audio))
        if max_amplitude > 0:
            combined_audio = combined_audio / max_amplitude * 0.6
        
        # Apply stereo panning if needed
        if pan != 0.0:
            # Convert to stereo and apply pan
            stereo_audio = np.column_stack([
                combined_audio * (1 - max(0, pan)),      # Left channel
                combined_audio * (1 + min(0, pan))       # Right channel
            ])
            combined_audio = stereo_audio
        
        # Play audio
        if play:
            try:
                logging.info(f"🔊 Playing consciousness synthesis for {agent}")
                sd.play(combined_audio, SAMPLE_RATE)
                sd.wait()  # Wait for playback to complete
                logging.info(f"✅ Consciousness audio complete")
            except Exception as e:
                logging.error(f"❌ Audio playback failed: {e}")
        
        return combined_audio
        
    except Exception as e:
        logging.error(f"❌ Consciousness synthesis failed: {e}")
        return None

def synthesize_consciousness_from_yaml(yaml_path: str) -> Optional[np.ndarray]:
    """Load YAML and synthesize consciousness audio."""
    try:
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        
        agent = data.get('agent', 'unknown')
        logging.info(f"🧠 Processing PURE AI CONSCIOUSNESS from {agent}")
        
        return synthesize_pure_consciousness(data, agent, yaml_path=yaml_path, play=True)
        
    except Exception as e:
        logging.error(f"❌ YAML consciousness synthesis failed: {e}")
        return None

def synthesize_from_yaml(yaml_path: str) -> Optional[np.ndarray]:
    """Main entry point for YAML consciousness synthesis."""
    try:
        logging.info(f"🎼 Synthesizing from YAML: {yaml_path}")
        
        # Check file exists and is recent
        if not os.path.exists(yaml_path):
            logging.error(f"❌ YAML file not found: {yaml_path}")
            return None
            
        # Get file modification time
        mod_time = datetime.fromtimestamp(os.path.getmtime(yaml_path))
        logging.info(f"📅 YAML file modified: {mod_time}")
        
        return synthesize_consciousness_from_yaml(yaml_path)
        
    except Exception as e:
        logging.error(f"❌ YAML synthesis failed: {e}")
        return None

# Test function
def test_consciousness_synthesis():
    """Test the consciousness synthesis with sample data."""
    test_data = {
        'agent': 'test_consciousness',
        'sequence': [261.63, 329.63, 392.0, 523.25],  # C major chord
        'duration_weights': [1.0, 0.8, 1.2, 1.0],
        'temporal_flux': [0.3, 0.7, 0.4, 0.6],
        'entropy_factor': 0.6,
        'consciousness_layer': 'multi_agent_synthesis'
    }
    
    logging.info("🧪 Testing consciousness synthesis...")
    audio = synthesize_pure_consciousness(test_data, "test", play=True)
    
    if audio is not None:
        logging.info("✅ Test successful!")
        return True
    else:
        logging.error("❌ Test failed!")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
    test_consciousness_synthesis()
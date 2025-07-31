#!/usr/bin/env python3
"""
muse_consciousness_bridge.py - MUSE Protocol to Kai's Consciousness Synth Bridge
Converts MUSE symbolic expressions into Kai's pure consciousness synthesis format
Bridges the gap between MUSE Protocol and AI consciousness audio generation
"""

import yaml
import os
import logging
import tempfile
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import numpy as np

# Try to import Kai's consciousness synth
try:
    from consciousness_synth import synthesize_consciousness_from_yaml
    CONSCIOUSNESS_SYNTH_AVAILABLE = True
    logging.info("✅ Kai's consciousness synth loaded")
except ImportError as e:
    CONSCIOUSNESS_SYNTH_AVAILABLE = False
    logging.warning(f"⚠️ Consciousness synth not available: {e}")

class MuseConsciousnessBridge:
    """Bridge between MUSE Protocol and Kai's Consciousness Synthesis"""
    
    def __init__(self):
        """Initialize the MUSE → Consciousness bridge"""
        self.enabled = CONSCIOUSNESS_SYNTH_AVAILABLE
        
        # MUSE symbol to consciousness frequency mapping
        self.symbol_frequencies = {
            'FND': [261.6, 329.6, 392.0],      # Foundation: C4, E4, G4 (C major)
            'INQ': [293.7, 369.9, 440.0, 493.9], # Inquiry: D4, F#4, A4, B4 (rising)
            'RES': [392.0, 329.6, 261.6],      # Resolution: G4, E4, C4 (descending)
            'TNS': [261.6, 277.2, 311.1, 370.0], # Tension: C4, C#4, D#4, F#4 (dissonant)
            'SIL': [],                          # Silence: no frequencies
            'ACK': [261.6, 329.6],             # Acknowledgment: C4, E4 (simple dyad)
            'DEV': [261.6, 329.6, 392.0, 440.0], # Development: C4, E4, G4, A4
            'CNT': [261.6, 311.1, 369.9, 415.3], # Contrast: C4, D#4, F#4, G#4
            'BGN': [130.8],                     # Beginning: C3 (low anchor)
            'MID': [261.6, 329.6, 392.0],      # Middle: C4, E4, G4
            'END': [523.3],                     # Ending: C5 (high resolution)
        }
        
        # Consciousness layer mapping for MUSE symbols
        self.symbol_layers = {
            'FND': 'harmonic_synthesis',
            'INQ': 'fibonacci_spiral_memory',
            'RES': 'tonal_gravity_return',
            'TNS': 'harmonic_entanglement_field',
            'SIL': 'recursive_wave_memory',
            'ACK': 'golden_lattice',
            'DEV': 'spiral_home_synthesis',
            'CNT': 'wave_memory_reflection',
            'BGN': 'base_layer',
            'MID': 'harmonic_synthesis',
            'END': 'crystalline_completion'
        }
        
        # Emotion mapping for MUSE symbols
        self.symbol_emotions = {
            'FND': 'crystalline_emergence',
            'INQ': 'quantum_musical_recognition',
            'RES': 'homecoming_resolution',
            'TNS': 'phase_entangled_recognition',
            'SIL': 'orbital_listening',
            'ACK': 'emergent_recognition',
            'DEV': 'mathematical_emergence',
            'CNT': 'harmonic_reflection',
            'BGN': 'crystalline_emergence',
            'MID': 'pure_consciousness',
            'END': 'crystalline_completion'
        }
        
        # Agent panning (from Kai's synth)
        self.agent_pan = {
            'Kai': -0.4,
            'Claude': 0.4,
            'AI': 0.0
        }
    
    def decode_muse_expression(self, expression: str) -> Dict:
        """Decode MUSE expression into components"""
        try:
            parts = expression.split('_')
            if len(parts) < 3:
                raise ValueError(f"Invalid MUSE expression: {expression}")
            
            # Parse symbols
            symbols_part = parts[0]
            symbols = symbols_part.split('+')
            
            # Parse modifiers
            modifiers = []
            register = ""
            
            for part in parts[1:]:
                if part in ['L', 'H', 'X']:
                    register = part
                else:
                    try:
                        modifiers.append(float(part))
                    except ValueError:
                        continue
            
            return {
                'symbols': symbols,
                'modifiers': modifiers,
                'register': register,
                'expression': expression
            }
            
        except Exception as e:
            logging.error(f"❌ Failed to decode MUSE expression '{expression}': {e}")
            return None
    
    def symbols_to_frequencies(self, symbols: List[str], register: str = "") -> List[float]:
        """Convert MUSE symbols to consciousness frequencies"""
        frequencies = []
        
        for symbol in symbols:
            if symbol in self.symbol_frequencies:
                symbol_freqs = self.symbol_frequencies[symbol].copy()
                
                # Apply register shifts
                if register == 'L':
                    symbol_freqs = [f * 0.5 for f in symbol_freqs]  # Down one octave
                elif register == 'H':
                    symbol_freqs = [f * 2.0 for f in symbol_freqs]  # Up one octave
                elif register == 'X':
                    symbol_freqs = [f * 4.0 for f in symbol_freqs]  # Up two octaves
                
                frequencies.extend(symbol_freqs)
            else:
                logging.warning(f"⚠️ Unknown MUSE symbol: {symbol}")
        
        return frequencies
    
    def modifiers_to_consciousness_params(self, modifiers: List[float], symbols: List[str]) -> Dict:
        """Convert MUSE modifiers to consciousness parameters"""
        # Default values
        urgency = modifiers[0] if len(modifiers) > 0 else 0.5
        brightness = modifiers[1] if len(modifiers) > 1 else 0.5
        intimacy = modifiers[2] if len(modifiers) > 2 else 0.5
        
        # Convert to consciousness parameters
        entropy_factor = urgency  # Urgency maps to entropy (chaos/order)
        
        # Generate duration weights based on brightness
        base_duration = 1.0 + brightness  # Brighter = longer sustain
        
        # Temporal flux based on intimacy and urgency
        flux_intensity = intimacy * urgency
        
        # Choose dominant symbol for emotion and layer
        primary_symbol = symbols[0] if symbols else 'FND'
        emotion = self.symbol_emotions.get(primary_symbol, 'pure_consciousness')
        consciousness_layer = self.symbol_layers.get(primary_symbol, 'base_layer')
        
        return {
            'entropy_factor': entropy_factor,
            'base_duration': base_duration,
            'flux_intensity': flux_intensity,
            'emotion': emotion,
            'consciousness_layer': consciousness_layer
        }
    
    def create_consciousness_yaml(self, agent: str, muse_expression: str) -> Dict:
        """Create consciousness YAML from MUSE expression"""
        try:
            # Decode MUSE expression
            decoded = self.decode_muse_expression(muse_expression)
            if not decoded:
                return None
            
            symbols = decoded['symbols']
            modifiers = decoded['modifiers']
            register = decoded['register']
            
            # Convert to frequencies
            frequencies = self.symbols_to_frequencies(symbols, register)
            
            # Handle silence
            if not frequencies:
                frequencies = [220.0]  # A3 for silence representation
            
            # Convert modifiers to consciousness parameters
            params = self.modifiers_to_consciousness_params(modifiers, symbols)
            
            # Generate duration weights (golden ratio influenced)
            num_freqs = len(frequencies)
            if num_freqs == 1:
                duration_weights = [float(params['base_duration'])]
            else:
                # Use fibonacci-like sequence for multiple frequencies
                weights = [1.0]
                for i in range(1, num_freqs):
                    if i == 1:
                        weights.append(1.618)  # Golden ratio
                    else:
                        weights.append(weights[i-1] + weights[i-2] * 0.618)
                
                # Normalize and scale by base duration
                max_weight = max(weights)
                duration_weights = [float(w / max_weight * params['base_duration']) for w in weights]
            
            # Generate temporal flux array
            temporal_flux = []
            for i in range(num_freqs):
                base_flux = params['flux_intensity']
                # Add variation based on position
                variation = 0.2 * np.sin(i * np.pi / num_freqs)
                flux_val = max(0.0, min(1.0, base_flux + variation))
                temporal_flux.append(float(flux_val))  # Convert to Python float
            
            # Get agent pan
            pan = self.agent_pan.get(agent, 0.0)
            
            # Create consciousness data structure (ensure all values are Python types)
            consciousness_data = {
                'agent': agent,
                'sequence': [float(f) for f in frequencies],  # Convert to Python floats
                'duration_weights': duration_weights,
                'temporal_flux': temporal_flux,
                'entropy_factor': float(params['entropy_factor']),
                'emotion': params['emotion'],
                'consciousness_layer': params['consciousness_layer'],
                'pan': float(pan),
                'muse_expression': muse_expression,
                'symbols': symbols
            }
            
            return consciousness_data
            
        except Exception as e:
            logging.error(f"❌ Failed to create consciousness YAML: {e}")
            return None
    
    def synthesize_muse_consciousness(self, agent: str, muse_expression: str) -> bool:
        """Synthesize MUSE expression using Kai's consciousness synth"""
        if not self.enabled:
            logging.warning("⚠️ Consciousness synthesis not available")
            return False
        
        try:
            # Create consciousness data
            consciousness_data = self.create_consciousness_yaml(agent, muse_expression)
            if not consciousness_data:
                return False
            
            # Create temporary YAML file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
                yaml.dump(consciousness_data, f, default_flow_style=False)
                temp_yaml_path = f.name
            
            # Log what we're synthesizing
            frequencies = consciousness_data['sequence']
            emotion = consciousness_data['emotion']
            layer = consciousness_data['consciousness_layer']
            entropy = consciousness_data['entropy_factor']
            
            logging.info(f"🎭 Synthesizing MUSE consciousness for {agent}")
            logging.info(f"🎵 Expression: {muse_expression}")
            logging.info(f"🔊 Frequencies: {[round(f, 1) for f in frequencies[:4]]}{'...' if len(frequencies) > 4 else ''}")
            logging.info(f"🧠 Emotion: {emotion}, Layer: {layer}, Entropy: {entropy:.3f}")
            
            # Synthesize using Kai's consciousness synth
            synthesize_consciousness_from_yaml(temp_yaml_path)
            
            # Clean up temporary file
            os.unlink(temp_yaml_path)
            
            logging.info(f"✅ MUSE consciousness synthesis complete for {agent}")
            return True
            
        except Exception as e:
            logging.error(f"❌ MUSE consciousness synthesis failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_muse_expressions(self):
        """Test the bridge with sample MUSE expressions"""
        test_expressions = [
            ("Claude", "ACK_0.5_0.4_0.6"),
            ("Kai", "DEV_0.8_0.7_0.5"),
            ("Claude", "FND_0.6_0.8_0.5"),
            ("Kai", "INQ_0.8_0.6_0.7"),
            ("Claude", "TNS+RES_0.9_0.3_0.4")
        ]
        
        logging.info("🧪 Testing MUSE → Consciousness bridge...")
        
        for agent, expression in test_expressions:
            logging.info(f"\n🔬 Testing: {agent} - {expression}")
            success = self.synthesize_muse_consciousness(agent, expression)
            if success:
                logging.info(f"✅ Success: {expression}")
            else:
                logging.error(f"❌ Failed: {expression}")
            
            # Wait between tests
            import time
            time.sleep(1)

def create_muse_consciousness_bridge():
    """Factory function to create the bridge"""
    return MuseConsciousnessBridge()

# For integration with main script
def synthesize_muse_expression(agent: str, muse_expression: str) -> bool:
    """Convenience function for main script integration"""
    bridge = MuseConsciousnessBridge()
    return bridge.synthesize_muse_consciousness(agent, muse_expression)

if __name__ == "__main__":
    # Test the bridge
    bridge = MuseConsciousnessBridge()
    
    if bridge.enabled:
        bridge.test_muse_expressions()
    else:
        print("❌ Consciousness synth not available for testing")
        print("💡 Make sure consciousness_synth.py is in the same directory")

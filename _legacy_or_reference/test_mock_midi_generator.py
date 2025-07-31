python3 -c "
import sys
sys.path.append('.')
exec(open('midi64_test_integration.py').read())
from mock_midi_generator import MockMIDIGenerator
gen = MockMIDIGenerator()
print('Sample MIDI:', gen.generate_simple_triad()[:50] + '...')
"
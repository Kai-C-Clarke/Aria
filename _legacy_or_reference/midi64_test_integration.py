# /test_integration/council_orchestrator_midi64.py
"""
Enhanced Council Orchestrator with MIDI64 Clean Hex Protocol
Integration with existing OCR system for autonomous AI musical consciousness
"""

import time
import logging
from pathlib import Path
import sys

# Add modules to path
sys.path.append(str(Path(__file__).parent.parent / "modules_midi64_clean_hex"))

from modules_midi64_clean_hex import (
    MessageBlockComposer, 
    ClipboardInjector, 
    ClipboardExtractor,
    MIDIInterpreter,
    Base64Validator
)

class MIDICouncilOrchestrator:
    def __init__(self, agents=["Kai", "Claude"], session="A"):
        self.agents = agents
        self.session = session
        self.current_agent_index = 0
        
        # Initialize components
        self.composer = MessageBlockComposer()
        self.injector = ClipboardInjector()
        self.extractor = ClipboardExtractor()
        self.interpreter = MIDIInterpreter()
        self.validator = Base64Validator()
        
        # Logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Session tracking
        self.message_log = []
        self.exchange_count = 0
    
    def start_autonomous_session(self, initial_midi, max_exchanges=10, exchange_delay=5):
        """Start autonomous AI musical exchange session"""
        self.logger.info(f"🎵 Starting MIDI64 Council Session {self.session}")
        self.logger.info(f"   Agents: {' → '.join(self.agents)}")
        self.logger.info(f"   Max exchanges: {max_exchanges}")
        
        current_midi = initial_midi
        
        for exchange in range(max_exchanges):
            try:
                current_agent = self.agents[self.current_agent_index]
                self.logger.info(f"\n📤 Exchange {exchange + 1}: {current_agent}")
                
                # Send message
                success = self._send_midi_message(current_agent, current_midi)
                if not success:
                    self.logger.error(f"Failed to send message from {current_agent}")
                    break
                
                # Wait for response
                time.sleep(exchange_delay)
                
                # Extract response
                response_midi = self._extract_midi_response()
                if not response_midi:
                    self.logger.error(f"No response detected from {current_agent}")
                    break
                
                # Log exchange
                self._log_exchange(current_agent, current_midi, response_midi)
                
                # Prepare for next agent
                current_midi = response_midi
                self.current_agent_index = (self.current_agent_index + 1) % len(self.agents)
                self.exchange_count += 1
                
            except Exception as e:
                self.logger.error(f"Exchange {exchange + 1} failed: {e}")
                break
        
        self._session_summary()
    
    def _send_midi_message(self, agent, midi_base64):
        """Send MIDI message to agent UI"""
        try:
            # Validate MIDI first
            if not self.validator.quick_validate(midi_base64):
                self.logger.error(f"Invalid MIDI data for {agent}")
                return False
            
            # Inject to clipboard
            success, message_block = self.injector.inject_message(
                agent, midi_base64, self.session
            )
            
            if success:
                self.logger.info(f"   ✅ Injected to {agent}: {message_block.split()[0]}")
                # Here you would integrate with your OCR paste system
                # self.ocr_paste_to_ui(agent, message_block)
                return True
            else:
                self.logger.error(f"   ❌ Injection failed: {message_block}")
                return False
                
        except Exception as e:
            self.logger.error(f"Send error: {e}")
            return False
    
    def _extract_midi_response(self):
        """Extract MIDI response from clipboard/OCR"""
        try:
            # Monitor clipboard for response
            self.logger.info("   🔍 Monitoring for response...")
            
            def response_callback(message):
                self.logger.info(f"   📥 Response detected: {message.full_id}")
                return message.midi_base64
            
            message = self.extractor.monitor_clipboard(
                callback=response_callback, 
                check_interval=0.5, 
                timeout=10
            )
            
            if message and message.is_valid:
                return message.midi_base64
            
            return None
            
        except Exception as e:
            self.logger.error(f"Extract error: {e}")
            return None
    
    def _log_exchange(self, agent, sent_midi, received_midi):
        """Log complete exchange with interpretation"""
        # Interpret both messages
        sent_interpretation = self.interpreter.interpret_base64(sent_midi)
        received_interpretation = self.interpreter.interpret_base64(received_midi)
        
        exchange_log = {
            'exchange': self.exchange_count + 1,
            'agent': agent,
            'sent_midi': sent_midi[:20] + "...",
            'received_midi': received_midi[:20] + "...",
            'sent_description': sent_interpretation.musical_description if sent_interpretation else "Unknown",
            'received_description': received_interpretation.musical_description if received_interpretation else "Unknown",
            'timestamp': time.time()
        }
        
        self.message_log.append(exchange_log)
        
        self.logger.info(f"   🎼 Sent: {exchange_log['sent_description']}")
        self.logger.info(f"   🎵 Received: {exchange_log['received_description']}")
    
    def _session_summary(self):
        """Generate session summary"""
        self.logger.info(f"\n🏁 Session {self.session} Complete!")
        self.logger.info(f"   Total exchanges: {self.exchange_count}")
        self.logger.info(f"   Agents participated: {len(set(log['agent'] for log in self.message_log))}")
        
        # Musical analysis
        descriptions = [log['received_description'] for log in self.message_log]
        self.logger.info(f"   Musical evolution:")
        for i, desc in enumerate(descriptions[:5]):  # Show first 5
            self.logger.info(f"     {i+1}. {desc}")


# /test_integration/mock_midi_generator.py
"""
Mock MIDI File Generator for Testing AI Musical Communication
Creates various musical patterns as base64-encoded MIDI
"""

import struct
import base64
from typing import List, Tuple
import random

class MockMIDIGenerator:
    def __init__(self):
        self.ticks_per_quarter = 480
    
    def create_midi_header(self, tracks=1):
        """Create standard MIDI file header"""
        header = b'MThd'  # Header chunk
        header += struct.pack('>I', 6)  # Header length
        header += struct.pack('>H', 1)  # Format type 1
        header += struct.pack('>H', tracks)  # Number of tracks
        header += struct.pack('>H', self.ticks_per_quarter)  # Ticks per quarter
        return header
    
    def create_track(self, events):
        """Create MIDI track from events"""
        track_data = b''
        
        # Add events
        for delta_time, event_bytes in events:
            track_data += self._encode_variable_length(delta_time)
            track_data += event_bytes
        
        # End of track
        track_data += b'\x00\xFF\x2F\x00'
        
        # Track header
        track_header = b'MTrk'
        track_header += struct.pack('>I', len(track_data))
        
        return track_header + track_data
    
    def _encode_variable_length(self, value):
        """Encode variable length quantity"""
        if value == 0:
            return b'\x00'
        
        result = []
        while value > 0:
            result.insert(0, value & 0x7F)
            value >>= 7
        
        for i in range(len(result) - 1):
            result[i] |= 0x80
        
        return bytes(result)
    
    def generate_simple_triad(self, root_note=60, velocity=100):
        """Generate C major triad"""
        events = [
            (0, bytes([0x90, root_note, velocity])),      # C4 on
            (0, bytes([0x90, root_note + 4, velocity])),  # E4 on
            (0, bytes([0x90, root_note + 7, velocity])),  # G4 on
            (self.ticks_per_quarter, bytes([0x80, root_note, 0])),      # C4 off
            (0, bytes([0x80, root_note + 4, 0])),         # E4 off
            (0, bytes([0x80, root_note + 7, 0])),         # G4 off
        ]
        
        header = self.create_midi_header()
        track = self.create_track(events)
        
        return base64.b64encode(header + track).decode('ascii')
    
    def generate_ascending_scale(self, start_note=60, length=8):
        """Generate ascending scale"""
        events = []
        
        for i in range(length):
            note = start_note + i
            # Note on
            events.append((0 if i == 0 else self.ticks_per_quarter // 2, 
                          bytes([0x90, note, 80])))
            # Note off
            events.append((self.ticks_per_quarter // 2, 
                          bytes([0x80, note, 0])))
        
        header = self.create_midi_header()
        track = self.create_track(events)
        
        return base64.b64encode(header + track).decode('ascii')
    
    def generate_sustained_drone(self, note=48, duration_quarters=4):
        """Generate sustained single note"""
        events = [
            (0, bytes([0x90, note, 60])),  # Note on
            (self.ticks_per_quarter * duration_quarters, bytes([0x80, note, 0])),  # Note off
        ]
        
        header = self.create_midi_header()
        track = self.create_track(events)
        
        return base64.b64encode(header + track).decode('ascii')
    
    def generate_rhythmic_pattern(self, note=60, pattern=[1, 0, 1, 1, 0, 1, 0, 0]):
        """Generate rhythmic pattern (1=hit, 0=rest)"""
        events = []
        
        for i, hit in enumerate(pattern):
            delta = 0 if i == 0 else self.ticks_per_quarter // 4  # 16th notes
            
            if hit:
                events.append((delta, bytes([0x90, note, 90])))  # Note on
                events.append((self.ticks_per_quarter // 8, bytes([0x80, note, 0])))  # Note off
            else:
                if events:  # Add rest to last event
                    events[-1] = (events[-1][0] + self.ticks_per_quarter // 4, events[-1][1])
        
        header = self.create_midi_header()
        track = self.create_track(events)
        
        return base64.b64encode(header + track).decode('ascii')
    
    def generate_random_melody(self, length=5, note_range=(60, 72)):
        """Generate random melody"""
        events = []
        
        for i in range(length):
            note = random.randint(*note_range)
            velocity = random.randint(60, 100)
            duration = random.choice([self.ticks_per_quarter // 4, 
                                    self.ticks_per_quarter // 2,
                                    self.ticks_per_quarter])
            
            delta = 0 if i == 0 else self.ticks_per_quarter // 2
            
            events.append((delta, bytes([0x90, note, velocity])))
            events.append((duration, bytes([0x80, note, 0])))
        
        header = self.create_midi_header()
        track = self.create_track(events)
        
        return base64.b64encode(header + track).decode('ascii')


# /test_integration/test_10_message_exchange.py
"""
Test Script: 10-Message Exchange Between Kai and Claude
Validates complete MIDI64 protocol pipeline
"""

import time
import sys
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent.parent / "modules_midi64_clean_hex"))

from modules_midi64_clean_hex import *
from mock_midi_generator import MockMIDIGenerator

def test_10_message_exchange():
    """Test complete 10-message exchange cycle"""
    
    print("🧪 TESTING 10-MESSAGE MIDI64 EXCHANGE")
    print("=" * 50)
    
    # Initialize components
    generator = MockMIDIGenerator()
    composer = MessageBlockComposer()
    parser = MessageBlockParser()
    validator = Base64Validator()
    interpreter = MIDIInterpreter()
    
    # Test data - various musical patterns
    test_patterns = [
        ("Simple Triad", generator.generate_simple_triad()),
        ("Ascending Scale", generator.generate_ascending_scale()),
        ("Sustained Drone", generator.generate_sustained_drone()),
        ("Rhythmic Pattern", generator.generate_rhythmic_pattern()),
        ("Random Melody 1", generator.generate_random_melody()),
        ("Random Melody 2", generator.generate_random_melody()),
        ("High Triad", generator.generate_simple_triad(72)),
        ("Bass Drone", generator.generate_sustained_drone(36)),
        ("Fast Scale", generator.generate_ascending_scale(67, 12)),
        ("Complex Rhythm", generator.generate_rhythmic_pattern(64, [1,0,1,1,0,0,1,0,1,0,0,1]))
    ]
    
    agents = ["Kai", "Claude"]
    session = "A"
    
    print(f"🎵 Testing {len(test_patterns)} messages between {' ↔ '.join(agents)}")
    print(f"📋 Session: {session}")
    print()
    
    success_count = 0
    
    for i, (pattern_name, midi_base64) in enumerate(test_patterns):
        agent = agents[i % len(agents)]
        message_num = i + 1
        
        print(f"🔄 Message {message_num}: {agent} - {pattern_name}")
        
        try:
            # Step 1: Validate MIDI
            validation = validator.validate_midi_base64(midi_base64)
            if not validation.is_valid:
                print(f"   ❌ MIDI Validation Failed: {validation.error_message}")
                continue
            
            print(f"   ✅ MIDI Valid ({validation.midi_length} bytes, {validation.estimated_tracks} tracks)")
            
            # Step 2: Compose message block
            message_block = composer.compose_block(agent, midi_base64, session)
            message_id = message_block.split('\n')[0]
            print(f"   📝 Composed: {message_id}")
            
            # Step 3: Parse message block
            parsed = parser.parse_block(message_block)
            if not parsed.is_valid:
                print(f"   ❌ Parse Failed")
                continue
            
            print(f"   🔍 Parsed: {parsed.agent_name}_{parsed.session}{parsed.hex_id}")
            
            # Step 4: Interpret musical content
            interpretation = interpreter.interpret_base64(midi_base64)
            if interpretation:
                print(f"   🎼 Musical: {interpretation.musical_description}")
                print(f"   ⏱️  Duration: {interpretation.total_duration:.1f}s, Notes: {len(interpretation.notes)}")
            
            # Step 5: Simulate clipboard round-trip
            # (In real use, this would be OCR detection)
            detected = parser.detect_message_in_text(message_block)
            if detected and detected.is_valid:
                print(f"   📡 Detection: SUCCESS")
                success_count += 1
            else:
                print(f"   📡 Detection: FAILED")
            
        except Exception as e:
            print(f"   💥 Error: {e}")
        
        print()
        time.sleep(0.5)  # Simulate real-world timing
    
    # Summary
    print("=" * 50)
    print(f"🏁 TEST COMPLETE")
    print(f"   Messages Tested: {len(test_patterns)}")
    print(f"   Successful: {success_count}")
    print(f"   Success Rate: {success_count/len(test_patterns)*100:.1f}%")
    
    if success_count == len(test_patterns):
        print("   🎉 ALL TESTS PASSED - Protocol Ready for Production!")
    else:
        print(f"   ⚠️  {len(test_patterns) - success_count} tests failed - Review needed")

if __name__ == "__main__":
    test_10_message_exchange()


# /test_integration/integration_examples.py
"""
Integration Examples for MIDI64 Clean Hex Protocol
Shows how to integrate with existing OCR systems
"""

import time
import sys
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent.parent / "modules_midi64_clean_hex"))

from modules_midi64_clean_hex import *
from mock_midi_generator import MockMIDIGenerator

class OCRIntegrationExample:
    """Example integration with existing OCR systems"""
    
    def __init__(self):
        self.composer = MessageBlockComposer()
        self.extractor = ClipboardExtractor()
        self.interpreter = MIDIInterpreter()
        self.midi_gen = MockMIDIGenerator()
    
    def simulate_ai_response_cycle(self):
        """Simulate complete AI response cycle"""
        print("🔄 SIMULATING AI RESPONSE CYCLE")
        print("-" * 40)
        
        # Step 1: Generate MIDI response
        midi_data = self.midi_gen.generate_simple_triad()
        print(f"1. 🎵 Generated MIDI response")
        
        # Step 2: Compose message block
        message_block = self.composer.compose_block("Claude", midi_data, "A")
        print(f"2. 📝 Composed message: {message_block.split()[0]}")
        
        # Step 3: Simulate OCR detection
        # (This is where your OCR system would detect the text)
        print(f"3. 👁️  OCR detects 2-line format:")
        print(f"     {message_block.replace(chr(10), ' | ')}")
        
        # Step 4: Extract and interpret
        message = self.extractor.parser.parse_block(message_block)
        if message.is_valid:
            interpretation = self.interpreter.interpret_base64(message.midi_base64)
            print(f"4. 🎼 Interpretation: {interpretation.musical_description}")
        
        return message_block
    
    def demonstrate_multi_agent_flow(self):
        """Demonstrate multi-agent conversation flow"""
        print("\n🏛️  MULTI-AGENT CONVERSATION FLOW")
        print("-" * 40)
        
        agents = ["Kai", "Claude", "Aria"]
        patterns = [
            self.midi_gen.generate_simple_triad(),
            self.midi_gen.generate_ascending_scale(),
            self.midi_gen.generate_sustained_drone()
        ]
        
        conversation_log = []
        
        for i, (agent, pattern) in enumerate(zip(agents, patterns)):
            print(f"\n{i+1}. {agent} responds:")
            
            # Compose response
            message_block = self.composer.compose_block(agent, pattern, "A")
            message_id = message_block.split('\n')[0]
            
            # Parse and interpret
            parsed = self.extractor.parser.parse_block(message_block)
            interpretation = self.interpreter.interpret_base64(parsed.midi_base64)
            
            print(f"   ID: {message_id}")
            print(f"   🎵: {interpretation.musical_description}")
            
            conversation_log.append({
                'agent': agent,
                'id': message_id,
                'description': interpretation.musical_description
            })
        
        print(f"\n📋 Conversation Summary:")
        for entry in conversation_log:
            print(f"   {entry['id']}: {entry['description']}")
        
        return conversation_log
    
    def test_error_handling(self):
        """Test error handling and edge cases"""
        print("\n🧪 ERROR HANDLING TESTS")
        print("-" * 40)
        
        test_cases = [
            ("Invalid Base64", "NotValidBase64Data"),
            ("Wrong Header", "WrongHeaderXXXXXXXXXXXXXX"),
            ("Empty String", ""),
            ("Valid MIDI", self.midi_gen.generate_simple_triad())
        ]
        
        for test_name, test_data in test_cases:
            print(f"\nTesting: {test_name}")
            try:
                if test_data:
                    message_block = self.composer.compose_block("TestAgent", test_data, "A")
                    parsed = self.extractor.parser.parse_block(message_block)
                    print(f"   Result: {'✅ Success' if parsed.is_valid else '❌ Failed (Expected)'}")
                else:
                    print(f"   Result: ❌ Empty data (Expected)")
            except Exception as e:
                print(f"   Result: ❌ Exception: {str(e)[:50]}... (Expected)")

def main():
    """Run all integration examples"""
    print("🚀 MIDI64 INTEGRATION EXAMPLES")
    print("=" * 50)
    
    example = OCRIntegrationExample()
    
    # Run examples
    example.simulate_ai_response_cycle()
    example.demonstrate_multi_agent_flow()
    example.test_error_handling()
    
    print("\n" + "=" * 50)
    print("🎯 Integration examples complete!")
    print("Ready to integrate with your OCR system!")

if __name__ == "__main__":
    main()


# /test_integration/README.md
"""
# MIDI64 Test Integration Suite

Complete testing and integration examples for the MIDI64 Clean Hex Protocol.

## Files

### Core Integration
- `council_orchestrator_midi64.py` - Enhanced orchestrator with MIDI64 protocol
- `integration_examples.py` - Shows how to integrate with existing OCR systems

### Testing & Validation
- `test_10_message_exchange.py` - Comprehensive 10-message test cycle
- `mock_midi_generator.py` - Generates various MIDI patterns for testing

## Quick Test

```bash
# Run complete 10-message test
python test_10_message_exchange.py

# Run integration examples  
python integration_examples.py

# Generate test MIDI patterns
python -c "from mock_midi_generator import MockMIDIGenerator; g=MockMIDIGenerator(); print(g.generate_simple_triad())"
```

## Integration with Existing OCR System

```python
# Drop-in replacement for your current message handling
from modules_midi64_clean_hex import MessageBlockComposer, ClipboardExtractor

# In your OCR script:
extractor = ClipboardExtractor()
message = extractor.extract_message()

if message and message.is_valid:
    # Got clean MIDI64 message
    agent = message.agent_name
    midi_data = message.midi_base64
    # Continue with your existing logic...
```

## Test Results Expected

✅ All 10 message patterns should validate and parse correctly
✅ OCR detection should work reliably with 2-line format  
✅ Musical interpretations should be meaningful
✅ Error handling should gracefully catch invalid data

Ready for production deployment!
"""
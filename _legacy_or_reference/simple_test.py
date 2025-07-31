# Simple MIDI64 Test - All code in one file

import struct
import base64
import json
import time
import random

class SimpleHexGenerator:
    def __init__(self):
        self.counter = 0
    
    def get_next_id(self, agent, session="A"):
        self.counter += 1
        return f"{agent}_{session}{self.counter:05X}"

class SimpleMIDIGenerator:
    def generate_simple_triad(self):
        # Create minimal MIDI file
        header = b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0'
        track_header = b'MTrk\x00\x00\x00\x1b'
        events = b'\x00\x90\x3c\x64\x81\x70\x80\x3c\x00\x00\xff\x2f\x00'
        midi_data = header + track_header + events
        return base64.b64encode(midi_data).decode('ascii')

class SimpleMessageComposer:
    def __init__(self):
        self.hex_gen = SimpleHexGenerator()
    
    def compose_block(self, agent, midi_base64, session="A"):
        message_id = self.hex_gen.get_next_id(agent, session)
        return f"{message_id}\n{midi_base64}"

# Quick test
print("🧪 SIMPLE MIDI64 TEST")
print("=" * 30)

# Initialize
composer = SimpleMessageComposer()
midi_gen = SimpleMIDIGenerator()

# Test 1: Generate MIDI
midi_data = midi_gen.generate_simple_triad()
print(f"✅ MIDI Generated: {len(midi_data)} chars")
print(f"   Preview: {midi_data[:50]}...")

# Test 2: Validate it starts with MIDI header
if midi_data.startswith('TVRoZA'):
    print("✅ MIDI Header Valid (TVRoZA)")
else:
    print("❌ MIDI Header Invalid")

# Test 3: Create message blocks
claude_block = composer.compose_block("Claude", midi_data, "A")
kai_block = composer.compose_block("Kai", midi_data, "A")

print(f"\n✅ Claude Message Block:")
lines = claude_block.split('\n')
print(f"   ID: {lines[0]}")
print(f"   MIDI: {lines[1][:50]}...")

print(f"\n✅ Kai Message Block:")
lines = kai_block.split('\n')
print(f"   ID: {lines[0]}")
print(f"   MIDI: {lines[1][:50]}...")

# Test 4: Simulate message exchange
print(f"\n🔄 Simulating 5-message exchange:")
agents = ["Claude", "Kai", "Claude", "Kai", "Claude"]

for i, agent in enumerate(agents):
    block = composer.compose_block(agent, midi_data, "A")
    message_id = block.split('\n')[0]
    print(f"   {i+1}. {message_id}")

print(f"\n🎯 Basic MIDI64 protocol working!")
print(f"📋 Ready for OCR integration!")

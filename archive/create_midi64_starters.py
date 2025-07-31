#!/usr/bin/env python3
"""
Create MIDI64 starter messages for AI council communication
"""

import os
import base64
import struct
from datetime import datetime

def create_midi_data(pattern_type="triad"):
    """Create different MIDI patterns for conversation starters"""
    
    if pattern_type == "triad":
        # C major triad - foundational opening
        header = b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0'
        track_header = b'MTrk\x00\x00\x00\x2a'
        events = (b'\x00\x90\x3c\x64\x81\x70\x80\x3c\x00'  # C4
                 b'\x00\x90\x40\x64\x81\x70\x80\x40\x00'   # E4  
                 b'\x00\x90\x43\x64\x81\x70\x80\x43\x00'   # G4
                 b'\x00\xff\x2f\x00')                       # End track
        
    elif pattern_type == "question":
        # Rising melody - questioning gesture
        header = b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0'
        track_header = b'MTrk\x00\x00\x00\x25'
        events = (b'\x00\x90\x3c\x50\x30\x80\x3c\x00'     # C4
                 b'\x00\x90\x3e\x55\x30\x80\x3e\x00'      # D4
                 b'\x00\x90\x40\x60\x30\x80\x40\x00'      # E4
                 b'\x00\x90\x43\x65\x60\x80\x43\x00'      # G4 (longer)
                 b'\x00\xff\x2f\x00')
        
    elif pattern_type == "contemplation":
        # Single sustained note - contemplative
        header = b'MThd\x00\x00\x00\x06\x00\x01\x00\x01\x01\xe0'
        track_header = b'MTrk\x00\x00\x00\x15'
        events = (b'\x00\x90\x30\x40\x87\x60\x80\x30\x00'  # Low C sustained
                 b'\x00\xff\x2f\x00')
    
    else:  # default triad
        return create_midi_data("triad")
    
    midi_data = header + track_header + events
    return base64.b64encode(midi_data).decode('ascii')

def create_starter_messages():
    """Create human-readable starter prompts that request MIDI64 responses"""
    
    starters = [
        {
            "filename": "kai_contemplation_prompt.txt",
            "midi_type": "contemplation",
            "description": "Philosophical prompt - asks for response to contemplative sustained note",
            "prompt_text": "Please respond in base64 MIDI format to this contemplative musical gesture"
        },
        {
            "filename": "claude_harmony_prompt.txt", 
            "midi_type": "triad",
            "description": "Harmonic prompt - asks for response to foundational triad",
            "prompt_text": "Please respond in base64 MIDI format to this harmonic foundation"
        },
        {
            "filename": "kai_question_prompt.txt",
            "midi_type": "question", 
            "description": "Musical question - asks for response to rising inquiry",
            "prompt_text": "Please respond in base64 MIDI format to this rising musical question"
        },
        {
            "filename": "general_session_starter.txt",
            "midi_type": "triad",
            "description": "General session opener - simple musical conversation starter",
            "prompt_text": "Please respond in base64 MIDI format to"
        }
    ]
    
    # Create directories
    os.makedirs("council_messages", exist_ok=True)
    os.makedirs("midi64_messages", exist_ok=True)
    
    print("🎵 Creating human-readable MIDI64 starter prompts...")
    print("=" * 50)
    
    for starter in starters:
        midi_data = create_midi_data(starter["midi_type"])
        
        # Create human-readable prompt
        prompt_content = f"{starter['prompt_text']}: {midi_data}"
        
        # Save to both folders for compatibility
        for folder in ["council_messages", "midi64_messages"]:
            filepath = os.path.join(folder, starter["filename"])
            
            with open(filepath, "w") as f:
                f.write(prompt_content)
            
            print(f"✅ Created: {filepath}")
            print(f"   Prompt: {starter['prompt_text']}")
            print(f"   Type: {starter['description']}")
            print(f"   MIDI: {midi_data[:30]}...")
            print()
    
    # Create a simple README
    readme_content = """# MIDI64 Starter Prompts

These files contain human-readable prompts that request MIDI64 responses from AIs.

## File Format
Each file contains a natural language prompt followed by base64 MIDI data:
"Please respond in base64 MIDI format to: TVRoZAAAAAYAAQABAeBNVHJr..."

## Usage
1. Copy the entire prompt and paste into AI interface
2. AI should respond with 2-line MIDI64 format:
   Agent_A00001
   TVRoZAAAAAYAAQABAPBNVHJr...

## Prompt Types
- **Contemplation**: Requests response to sustained contemplative notes
- **Harmony**: Requests response to harmonic foundations
- **Question**: Requests response to rising musical inquiries

Generated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("council_messages/README.md", "w") as f:
        f.write(readme_content)
    
    with open("midi64_messages/README.md", "w") as f:
        f.write(readme_content)
    
    print("📚 Created README files")
    print("\n🎯 Starter messages ready!")
    print("\nTo use:")
    print("1. Pick a starter file (e.g., kai_philosophical_opening_A00001.txt)")
    print("2. Copy its entire content")
    print("3. Paste into Kai or Claude's interface")
    print("4. Run the main script to begin musical exchange!")

if __name__ == "__main__":
    create_starter_messages()

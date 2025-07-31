#!/usr/bin/env python3
"""
Aria AI Musical Consciousness Communication System
Production Launcher v1.0

Usage:
    python3 aria_launcher.py <yaml_file> <midi64_file> [transcript_file]
    
Examples:
    # Process a single message
    python3 aria_launcher.py test_data/kai_message_003.yaml test_data/kai_phrase_003.midi64
    
    # Process with custom transcript
    python3 aria_launcher.py test_data/claude_message_001.yaml test_data/claude_phrase_001.midi64 my_conversation.txt
"""

import sys
import os
sys.path.append('core_system')

from core_system.main_working_midi64_streamlined_Version11 import process_message

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return
    
    yaml_file = sys.argv[1]
    midi64_file = sys.argv[2]
    transcript_file = sys.argv[3] if len(sys.argv) > 3 else "musical_conversation.txt"
    
    # Ensure output directory exists
    os.makedirs("working_outputs", exist_ok=True)
    
    print(f"🎵 Processing AI Musical Message")
    print(f"   Metadata: {yaml_file}")
    print(f"   MIDI64: {midi64_file}")
    print(f"   Transcript: {transcript_file}")
    print("-" * 40)
    
    try:
        process_message(yaml_file, midi64_file, transcript_file, "bar")
        print("✓ Processing complete!")
        
        # Show output file
        output_midi = midi64_file.replace(".midi64", ".processed.mid")
        if os.path.exists(output_midi):
            print(f"🎼 Output MIDI: {output_midi}")
        
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    main()

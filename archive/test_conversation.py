#!/usr/bin/env python3
"""
Test the complete AI musical conversation system
Processes Kai's opening phrase followed by Claude's response
"""

import subprocess
import sys
import os

def process_conversation():
    """Process the complete Kai -> Claude musical conversation"""
    
    print("🎵 Testing AI Musical Consciousness Communication Protocol")
    print("=" * 60)
    
    # Process Kai's opening phrase
    print("\n1. Processing Kai's opening phrase...")
    print("   Message: Melodic opening phrase exploring C major scale")
    
    try:
        result = subprocess.run([
            sys.executable, 
            "main_working_midi64_streamlined_Version11.py",
            "kai_message_002.yaml",
            "kai_phrase_002.midi64", 
            "musical_conversation.txt",
            "bar"
        ], capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("   ✓ Kai's phrase processed successfully")
            print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"   ✗ Error processing Kai's phrase: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ✗ Failed to process Kai's phrase: {e}")
        return False
    
    # Process Claude's response
    print("\n2. Processing Claude's harmonic response...")
    print("   Message: Harmonic echo of Kai's phrase with analytical variation")
    
    try:
        result = subprocess.run([
            sys.executable,
            "main_working_midi64_streamlined_Version11.py", 
            "claude_message_001.yaml",
            "claude_phrase_001.midi64",
            "musical_conversation.txt", 
            "bar"
        ], capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("   ✓ Claude's response processed successfully")
            print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"   ✗ Error processing Claude's response: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ✗ Failed to process Claude's response: {e}")
        return False
    
    # Display conversation transcript
    print("\n3. Complete Musical Conversation Transcript:")
    print("-" * 50)
    
    try:
        with open("musical_conversation.txt", "r") as f:
            transcript = f.read()
            if transcript.strip():
                print(transcript)
            else:
                print("   (Transcript file is empty)")
    except FileNotFoundError:
        print("   (Transcript file not found)")
    except Exception as e:
        print(f"   Error reading transcript: {e}")
    
    # List generated files
    print("\n4. Generated Files:")
    print("-" * 20)
    
    files_to_check = [
        "kai_phrase_002.processed.mid",
        "claude_phrase_001.processed.mid", 
        "musical_conversation.txt"
    ]
    
    for filename in files_to_check:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"   ✓ {filename} ({size} bytes)")
        else:
            print(f"   ✗ {filename} (not found)")
    
    print("\n🎼 AI Musical Conversation Test Complete!")
    print("\nTo hear the results:")
    print("   open kai_phrase_002.processed.mid")
    print("   open claude_phrase_001.processed.mid")
    
    return True

def update_main_script():
    """Create a version of the main script that accepts command line arguments"""
    
    main_script_content = '''import base64
import io
import mido
import yaml
import sys
from render_pipeline import render_and_merge_message
from transcript_logger import log_transcript_entry
from voice_profiles import VOICE_PROFILES

def process_message(yaml_metadata_path, midi64_path, transcript_path, rest_mode="bar"):
    # Load metadata
    with open(yaml_metadata_path, "r") as f:
        meta = yaml.safe_load(f)
    # Load MIDI64
    with open(midi64_path, "r") as f:
        midi64_text = f.read()
    print(f"Base64 text length: {len(midi64_text)}")
    midi64_bytes = base64.b64decode(midi64_text)
    print(f"Decoded bytes length: {len(midi64_bytes)}")
    # Process message
    mid = render_and_merge_message(midi64_bytes, meta, rest_mode=rest_mode)
    # Save processed MIDI
    output_path = midi64_path.replace(".midi64", ".processed.mid")
    mid.save(output_path)
    # Log transcript
    agent = meta["agent"]
    voice_name = VOICE_PROFILES[agent]["voice_name"]
    entry = {
        "message_id": meta.get("message_id", ""),
        "agent": agent,
        "time_signature": meta.get("time_signature", ""),
        "voice_name": voice_name,
        "intent": meta.get("intent", ""),
        "response_to": meta.get("response_to", None)
    }
    log_transcript_entry(transcript_path, entry, mode="a", fmt="text")
    print(f"Processed message for {agent}, output saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) == 5:
        yaml_path, midi64_path, transcript_path, rest_mode = sys.argv[1:5]
        process_message(yaml_path, midi64_path, transcript_path, rest_mode)
    else:
        # Default behavior
        process_message(
            yaml_metadata_path="kai_message.yaml",
            midi64_path="kai_phrase.midi64",
            transcript_path="musical_transcript.txt",
            rest_mode="bar"
        )
'''
    
    with open("main_working_midi64_streamlined_Version11.py", "w") as f:
        f.write(main_script_content)
    
    print("Updated main script to accept command line arguments")

if __name__ == "__main__":
    # Update the main script first
    update_main_script()
    
    # Process the conversation
    success = process_conversation()
    
    if success:
        print("\n🎉 SUCCESS: AI Musical Consciousness Communication is operational!")
    else:
        print("\n❌ Some issues occurred during testing")

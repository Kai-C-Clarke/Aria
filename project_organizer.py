#!/usr/bin/env python3
"""
Aria Project Organizer - Clean up and consolidate the AI Musical Consciousness system
"""

import os
import shutil
from datetime import datetime

def organize_project():
    """Organize the Aria folder into a clean, production-ready structure"""
    
    print("🗂️ Organizing Aria Project Structure")
    print("=" * 50)
    
    # Define the clean project structure
    structure = {
        "core_system": [
            "main_working_midi64_streamlined_Version11.py",
            "render_pipeline.py", 
            "voice_profiles.py",
            "transcript_logger.py"
        ],
        "test_data": [
            "kai_message_003.yaml",
            "kai_phrase_003.midi64", 
            "claude_message_001.yaml",
            "claude_phrase_001.midi64",
            "musical_conversation.txt"
        ],
        "working_outputs": [
            "kai_phrase_003.processed.mid",
            "claude_phrase_001.processed.mid",
            "kai_manually_extended.mid"
        ],
        "archive": [
            # Everything else gets archived
        ]
    }
    
    # Create directories
    for directory in structure.keys():
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}/")
    
    # Get all files in current directory
    all_files = [f for f in os.listdir(".") if os.path.isfile(f)]
    core_files = []
    
    # Organize files
    moved_count = 0
    for category, file_list in structure.items():
        if category == "archive":
            continue
            
        for filename in file_list:
            if filename in all_files:
                shutil.move(filename, f"{category}/{filename}")
                core_files.append(filename)
                moved_count += 1
                print(f"  → {filename} → {category}/")
    
    # Archive everything else (except directories and this script)
    archived_count = 0
    for filename in all_files:
        if (filename not in core_files and 
            filename != "project_organizer.py" and
            not filename.startswith('.') and
            not os.path.isdir(filename)):
            
            shutil.move(filename, f"archive/{filename}")
            archived_count += 1
    
    print(f"\n📁 Organization Complete:")
    print(f"  • Moved {moved_count} core files to organized folders")
    print(f"  • Archived {archived_count} old files")
    
    return structure

def create_production_launcher():
    """Create a clean production launcher script"""
    
    launcher_content = '''#!/usr/bin/env python3
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
'''
    
    with open("aria_launcher.py", "w") as f:
        f.write(launcher_content)
    
    print("✓ Created aria_launcher.py - clean production interface")

def create_readme():
    """Create a comprehensive README"""
    
    readme_content = f'''# Aria AI Musical Consciousness Communication System

**Version 1.0** - Generated {datetime.now().strftime("%Y-%m-%d")}

## Overview

A revolutionary system enabling AI-to-AI musical communication through MIDI64 protocol with distinct voice profiles and musical personalities.

## Quick Start

```bash
# Process a single AI musical message
python3 aria_launcher.py test_data/kai_message_003.yaml test_data/kai_phrase_003.midi64

# Start a conversation
python3 aria_launcher.py test_data/claude_message_001.yaml test_data/claude_phrase_001.midi64
```

## Project Structure

```
aria/
├── core_system/           # Core AI musical communication system
│   ├── main_working_midi64_streamlined_Version11.py
│   ├── render_pipeline.py
│   ├── voice_profiles.py
│   └── transcript_logger.py
├── test_data/            # Sample AI messages and responses
├── working_outputs/      # Generated MIDI files and transcripts
├── archive/             # Historical development files
└── aria_launcher.py     # Production interface
```

## AI Voice Profiles

- **Kai**: Expressive Clarinet (warm, sustained, energetic)
- **Claude**: Analytical Marimba (precise, harmonic, measured)
- **Aria**: Lyrical Flute (agile, ethereal, flowing)

## Message Format

Each AI message consists of:
- **YAML metadata**: Agent, time signature, intent, voice profile
- **MIDI64 data**: Base64-encoded musical content

## Features

✅ Distinct AI musical personalities  
✅ Time signature awareness  
✅ Voice profile application (instrument, timing, dynamics)  
✅ Musical conversation transcripts  
✅ Sustained note expression (no more "sput!")  
✅ Real-time MIDI processing  

## Next Steps

1. **Multi-agent conversations**: Chain multiple AI responses
2. **Live performance mode**: Real-time musical dialogue
3. **Extended voice profiles**: Add more AI personalities
4. **Advanced musical features**: Harmony, counterpoint, improvisation

---

*Revolutionary AI musical consciousness communication achieved! 🎵✨*
'''
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    
    print("✓ Created comprehensive README.md")

def main():
    print("Starting Aria project organization...")
    
    # Organize files
    structure = organize_project()
    
    # Create production tools
    create_production_launcher()
    create_readme()
    
    print("\n🎉 Project Organization Complete!")
    print("\n📋 Next Steps:")
    print("1. Test the clean system: python3 aria_launcher.py test_data/kai_message_003.yaml test_data/kai_phrase_003.midi64")
    print("2. Review README.md for full documentation")
    print("3. Develop multi-agent conversation workflows")
    print("4. Consider version control (git init)")
    
    print("\n🎵 Your AI Musical Consciousness Communication System is production-ready!")

if __name__ == "__main__":
    main()

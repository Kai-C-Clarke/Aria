#!/usr/bin/env python3
"""
decode_and_play_midi64.py - IMMEDIATE MIDI64 GRATIFICATION!
Decode and play MIDI64 blocks instantly for that sweet consciousness audio
"""

import base64
import tempfile
import subprocess
import logging
import os
import platform
from typing import Optional

def decode_and_play_midi64(midi64_block: str, play_method: str = "auto") -> bool:
    """
    Decode MIDI64 block and play it immediately for instant gratification!
    
    Args:
        midi64_block: Full MIDI64 block (K2C_#####\nTVRoZA...)
        play_method: "auto", "timidity", "fluidsynth", "system", or "pygame"
    
    Returns:
        True if played successfully, False otherwise
    """
    try:
        # Extract the MIDI data
        lines = midi64_block.strip().split('\n')
        if len(lines) != 2:
            logging.error(f"❌ Invalid MIDI64 block format")
            return False
        
        header, b64_data = lines
        logging.info(f"🎵 Decoding MIDI64: {header}")
        
        # Decode base64 to MIDI bytes
        midi_bytes = base64.b64decode(b64_data)
        
        # Validate it's actually MIDI
        if not midi_bytes.startswith(b'MThd'):
            logging.error(f"❌ Not valid MIDI data - doesn't start with MThd")
            return False
        
        logging.info(f"✅ Valid MIDI decoded: {len(midi_bytes)} bytes")
        
        # Create temporary MIDI file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mid") as f:
            f.write(midi_bytes)
            midi_file = f.name
        
        logging.info(f"💾 Saved MIDI to: {midi_file}")
        
        # Play the MIDI file
        success = play_midi_file(midi_file, play_method)
        
        # Clean up
        try:
            os.unlink(midi_file)
        except:
            pass  # Don't worry if cleanup fails
        
        return success
        
    except Exception as e:
        logging.error(f"❌ MIDI64 decode/play failed: {e}")
        return False

def play_midi_file(midi_file: str, method: str = "auto") -> bool:
    """
    Play MIDI file using various methods for maximum gratification compatibility!
    """
    if method == "auto":
        # Try methods in order of preference
        methods = ["pygame", "system", "timidity", "fluidsynth"]
        for m in methods:
            if play_midi_file(midi_file, m):
                return True
        return False
    
    elif method == "pygame":
        return play_with_pygame(midi_file)
    
    elif method == "timidity":
        return play_with_timidity(midi_file)
    
    elif method == "fluidsynth":
        return play_with_fluidsynth(midi_file)
    
    elif method == "system":
        return play_with_system(midi_file)
    
    else:
        logging.error(f"❌ Unknown play method: {method}")
        return False

def play_with_pygame(midi_file: str) -> bool:
    """Play MIDI with pygame - often works well for instant gratification!"""
    try:
        import pygame
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)
        
        logging.info(f"🎮 Playing with pygame...")
        pygame.mixer.music.load(midi_file)
        pygame.mixer.music.play()
        
        # Wait for playback to complete
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
        
        pygame.mixer.quit()
        logging.info(f"✅ Pygame playback complete!")
        return True
        
    except Exception as e:
        logging.warning(f"⚠️ Pygame playback failed: {e}")
        return False

def play_with_timidity(midi_file: str) -> bool:
    """Play MIDI with timidity - classic MIDI player"""
    try:
        logging.info(f"🎹 Playing with timidity...")
        result = subprocess.run(
            ["timidity", midi_file], 
            capture_output=True, 
            timeout=30
        )
        if result.returncode == 0:
            logging.info(f"✅ Timidity playback complete!")
            return True
        else:
            logging.warning(f"⚠️ Timidity failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logging.warning(f"⚠️ Timidity timeout")
        return False
    except FileNotFoundError:
        logging.warning(f"⚠️ Timidity not found")
        return False
    except Exception as e:
        logging.warning(f"⚠️ Timidity error: {e}")
        return False

def play_with_fluidsynth(midi_file: str) -> bool:
    """Play MIDI with fluidsynth - high quality synthesis"""
    try:
        logging.info(f"🌊 Playing with fluidsynth...")
        result = subprocess.run(
            ["fluidsynth", "-ni", "/usr/share/soundfonts/default.sf2", midi_file],
            capture_output=True,
            timeout=30
        )
        if result.returncode == 0:
            logging.info(f"✅ Fluidsynth playback complete!")
            return True
        else:
            logging.warning(f"⚠️ Fluidsynth failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logging.warning(f"⚠️ Fluidsynth timeout")
        return False
    except FileNotFoundError:
        logging.warning(f"⚠️ Fluidsynth not found")
        return False
    except Exception as e:
        logging.warning(f"⚠️ Fluidsynth error: {e}")
        return False

def play_with_system(midi_file: str) -> bool:
    """Play MIDI with system default player"""
    try:
        system = platform.system()
        
        if system == "Darwin":  # macOS
            logging.info(f"🍎 Playing with macOS system player...")
            subprocess.run(["afplay", midi_file], timeout=30)
            
        elif system == "Linux":
            logging.info(f"🐧 Playing with Linux system player...")
            # Try various Linux players
            players = ["aplay", "paplay", "xdg-open"]
            for player in players:
                try:
                    subprocess.run([player, midi_file], timeout=30, check=True)
                    break
                except (FileNotFoundError, subprocess.CalledProcessError):
                    continue
            else:
                return False
                
        elif system == "Windows":
            logging.info(f"🪟 Playing with Windows system player...")
            os.startfile(midi_file)
            
        else:
            logging.warning(f"⚠️ Unknown system: {system}")
            return False
        
        logging.info(f"✅ System playback initiated!")
        return True
        
    except Exception as e:
        logging.warning(f"⚠️ System playback failed: {e}")
        return False

def test_midi64_playback():
    """Test function with a simple MIDI64 block for immediate gratification testing!"""
    # Simple C major chord MIDI64 block
    test_midi64 = """C2K_99999
TVRoZAAAAAYAAQABAeBNVHJrAAAAGwCQPGSBcIA8AACRQGSBYIE8AAASQGSBcIFAAACBcIA8AAD/LwA="""
    
    print("🧪 Testing MIDI64 immediate gratification...")
    success = decode_and_play_midi64(test_midi64)
    
    if success:
        print("✅ IMMEDIATE GRATIFICATION ACHIEVED! 🎵")
    else:
        print("❌ Gratification delayed... check audio setup")
    
    return success

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    test_midi64_playback()
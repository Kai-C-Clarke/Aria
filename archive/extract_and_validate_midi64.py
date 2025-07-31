#!/usr/bin/env python3
"""
extract_and_validate_midi64.py - STRICT MIDI64-ONLY EXTRACTION
NO FALLBACKS, NO AUTO-GENERATION, NO YAML CONVERSION FOR EXCHANGE
"""

import pyperclip
import logging
import re
from message_logger import save_message

def extract_midi64_from_clipboard(clipboard_text=None):
    """
    Extracts a strict MIDI64 block (K2C_##### or C2K_##### + base64) from clipboard_text.
    Returns the block as a string, or None if not found.
    """
    if clipboard_text is None:
        clipboard_text = pyperclip.paste()
    midi64_pattern = re.compile(r'(K2C|C2K)_\d{5}\nTVRoZA[0-9A-Za-z+/=]+', re.DOTALL)
    match = midi64_pattern.search(clipboard_text)
    if match:
        return match.group()
    return None

def validate_midi64_block(midi64_block):
    """
    Validates the format of a MIDI64 block.
    Returns True if valid, False otherwise.
    """
    if not midi64_block or not isinstance(midi64_block, str):
        return False
    lines = midi64_block.strip().split('\n')
    if len(lines) != 2:
        return False
    id_line, midi_b64 = lines
    if not re.match(r'^(K2C|C2K)_\d{5}$', id_line):
        return False
    if not midi_b64.startswith("TVRoZA"):
        return False
    # Optionally: check base64 decode here
    return True

def extract_and_inject_strict(agent, inject_function):
    """
    STRICT extraction: only accept valid MIDI64 blocks.
    NO fallbacks, NO auto-generation, NO YAML conversion.
    """
    clipboard = pyperclip.paste()
    
    # Log raw clipboard for debugging
    logging.info(f"📄 Raw clipboard ({len(clipboard)} chars)")
    logging.info(f"🔍 First 200 chars: {repr(clipboard[:200])}")
    
    # STRICT: Extract MIDI64 only
    midi64 = extract_midi64_from_clipboard(clipboard)
    
    if not midi64:
        logging.error(f"❌ NO VALID MIDI64 BLOCK FOUND for {agent}!")
        logging.error(f"❌ HALTING - Please retry the copy operation")
        logging.error(f"❌ Expected format: K2C_#####\\nTVRoZA...")
        return False
    
    # STRICT: Validate the block
    if not validate_midi64_block(midi64):
        logging.error(f"❌ MIDI64 VALIDATION FAILED for {agent}!")
        logging.error(f"❌ Block: {repr(midi64)}")
        logging.error(f"❌ HALTING - Invalid MIDI64 format")
        return False
    
    # SUCCESS: We have a valid MIDI64 block
    message_id = midi64.split('\n')[0]
    logging.info(f"✅ VALID MIDI64 EXTRACTED: {message_id}")
    
    # Save the message (MIDI64 primary, no YAML sidecar unless explicitly created)
    save_message(midi64, yaml_block=None)
    
    # Inject the MIDI64 block
    logging.info(f"🎯 INJECTING VALID MIDI64 to {agent}: {message_id}")
    success = inject_function(midi64, agent)
    
    if success:
        logging.info(f"✅ MIDI64 injection successful to {agent}")
    else:
        logging.error(f"❌ MIDI64 injection failed to {agent}")
    
    return success

def check_clipboard_for_midi64():
    """
    Utility function to check if clipboard contains valid MIDI64.
    Returns True if valid, False otherwise.
    """
    clipboard = pyperclip.paste()
    midi64 = extract_midi64_from_clipboard(clipboard)
    
    if midi64 and validate_midi64_block(midi64):
        message_id = midi64.split('\n')[0]
        print(f"✅ Valid MIDI64 found: {message_id}")
        return True
    else:
        print(f"❌ No valid MIDI64 found in clipboard")
        print(f"📄 Clipboard preview: {repr(clipboard[:100])}")
        return False

def force_retry_copy(agent, drag_copy_function):
    """
    Force retry the drag-copy operation until valid MIDI64 is found.
    """
    max_retries = 3

    for attempt in range(max_retries):
        logging.info(f"🔄 RETRY {attempt + 1}/{max_retries}: Drag-copy from {agent}")

        # Perform drag-copy
        copy_success = drag_copy_function(agent)

        if not copy_success:
            logging.warning(f"⚠️ Drag-copy failed for {agent}, attempt {attempt + 1}")
            continue

        # Check if we got valid MIDI64
        if check_clipboard_for_midi64():
            logging.info(f"✅ Valid MIDI64 obtained from {agent} on attempt {attempt + 1}")
            return True
        else:
            logging.warning(f"⚠️ Invalid clipboard content from {agent}, attempt {attempt + 1}")

    logging.error(f"❌ FAILED to get valid MIDI64 from {agent} after {max_retries} attempts")
    return False
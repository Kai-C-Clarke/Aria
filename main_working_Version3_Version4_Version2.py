import os
import time
import logging
import re
import pyautogui
import pyperclip
import subprocess
import shutil
from datetime import datetime

# Import the consciousness synthesis engine
from consciousness_synth import synthesize_consciousness_from_yaml, synthesize_from_yaml

# Try to import memory system, but continue if not available
try:
    from council_memory_system import council_memory, get_context_for_agent, update_memory_from_yaml
    MEMORY_AVAILABLE = True
except ImportError:
    logging.warning("⚠️ Memory system not available")
    MEMORY_AVAILABLE = False

USE_CLICLICK = shutil.which("cliclick") is not None

BATTLE_TESTED_UI_CONFIGS = {
    "Kai": {
        "input_click": (300, 990),
        "send_button": (863, 1020),  # not used (we use Enter to send)
        "read_region": (202, 199, 900, 884),
        "safe_click": (300, 990),
        "input_coords": (300, 990),
        "desktop": 1
    },
    "Claude": {
        "input_click": (1530, 994),
        "send_button": (1888, 1037),  # not used (we use Enter to send)
        "read_region": (1190, 203, 1909, 865),
        "safe_click": (1530, 994),
        "input_coords": (1530, 994),
        "desktop": 1
    }
}

current_desktop = 0

def perform_click(x, y):
    """Perform a click using cliclick or pyautogui."""
    logging.info(f"🖱️ Click at ({x}, {y})")
    try:
        pyautogui.click(x, y)
        time.sleep(0.3)
    except Exception as e:
        logging.error(f"❌ pyautogui click failed: {e}")
        return False
    return True

def kai_desktop_switch(target_desktop):
    """Switch to target desktop using macOS Mission Control with reset."""
    global current_desktop
    logging.info(f"Attempting switch from desktop {current_desktop} to {target_desktop}")
    
    if current_desktop == target_desktop:
        logging.info(f"Already on desktop {target_desktop}")
        return True
    
    try:
        if current_desktop != 0:
            script = 'tell application "System Events" to key code 123 using control down'
            for _ in range(current_desktop):
                subprocess.run(["osascript", "-e", script], check=True)
                time.sleep(0.5)
            current_desktop = 0
            logging.info("Reset to desktop 0")

        if target_desktop > 0:
            script = 'tell application "System Events" to key code 124 using control down'
            for _ in range(target_desktop):
                subprocess.run(["osascript", "-e", script], check=True)
                time.sleep(0.5)
        
        current_desktop = target_desktop
        logging.info(f"🖥️ Switched to desktop {target_desktop}")
        return True
    except Exception as e:
        logging.error(f"❌ Desktop switch failed: {e}")
        return False

def kai_smart_desktop_switch(speaker):
    """Switch to the appropriate desktop for the given speaker."""
    target_desktop = BATTLE_TESTED_UI_CONFIGS[speaker]["desktop"]
    return kai_desktop_switch(target_desktop)

def kai_safe_click(ui):
    """Perform a safe click in a neutral area of the UI."""
    coords = BATTLE_TESTED_UI_CONFIGS[ui]["safe_click"]
    logging.info(f"🛡️ Safe click for {ui} at {coords}")
    return perform_click(coords[0], coords[1])

def kai_clipboard_injection(message):
    """Copy message to system clipboard."""
    try:
        subprocess.run('pbcopy', text=True, input=message, check=True)
        logging.info(f"📋 Copied to clipboard: {len(message)} chars")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Clipboard failed: {e}")
        return False

def kai_text_injection(message, ui, auto_send=True):
    """Inject text into the specified UI with improved formatting handling."""
    coords = BATTLE_TESTED_UI_CONFIGS[ui]["input_coords"]
    logging.info(f"💬 Injecting into {ui}: {message[:100]}...")

    if not kai_clipboard_injection(message):
        logging.error("❌ Failed to copy message to clipboard")
        return False

    try:
        if not perform_click(coords[0], coords[1]):
            return False
        
        time.sleep(0.5)
        pyautogui.hotkey("command", "a")
        time.sleep(0.2)
        pyautogui.hotkey("command", "v")
        time.sleep(0.5)
        
        if auto_send:
            # Use Enter to send (not click button), as mouse click may activate microphone
            pyautogui.press("enter")
            time.sleep(1)
            logging.info(f"✅ Message sent to {ui}")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ Text injection failed for {ui}: {e}")
        return False

def kai_return_home():
    """Return to the home desktop."""
    logging.info("🏠 Returning to home desktop")
    return kai_desktop_switch(0)

SYMBOLIC_FOLDER = "symbolic_messages"
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

def validate_consciousness_clipboard(clipboard_content):
    """Enhanced clipboard validation for consciousness YAML."""
    if not clipboard_content or len(clipboard_content) < 50:
        return False
    
    # Check for consciousness indicators
    consciousness_indicators = [
        "agent:", "yamlagent:", "sequence:", "response_sequence:",
        "consciousness_layer:", "entropy_factor:", "emotion:",
        "harmonic_ratios:", "temporal_flux:", "message:"
    ]
    
    indicator_count = sum(1 for indicator in consciousness_indicators 
                         if indicator in clipboard_content)
    
    # RELAXED: Need at least 2 consciousness indicators (was 3)
    if indicator_count >= 2:
        logging.info(f"✅ Valid consciousness YAML: {indicator_count} indicators found")
        return True
    
    logging.warning(f"⚠️ Clipboard validation failed: only {indicator_count} indicators")
    return False

def simple_drag_copy(agent):
    """Robust drag selection and copy for Kai/Claude using pyautogui (no cliclick), with window focus, slow drag, and debug screenshots."""
    import time

    logging.info(f"🖱️ FULL UI drag-and-copy for {agent}")

    if agent == "Kai":
        start_x, start_y = 188, 214
        end_x, end_y = 857, 835
        logging.info(f"📖 Dragging FULL Kai response area ({start_x},{start_y}) to ({end_x},{end_y})")
    elif agent == "Claude":
        start_x, start_y = 1170, 298
        end_x, end_y = 1905, 851
        logging.info(f"📖 Dragging Claude response area ({start_x},{start_y}) to ({end_x},{end_y})")

    # Clear clipboard
    logging.info("🗑️ Clearing clipboard to avoid cached prompt")
    pyperclip.copy("")
    time.sleep(0.5)

    # Scroll to bottom and focus read area
    logging.info("📜 Scrolling read area down to bring new message into view")
    perform_click(end_x, end_y)
    time.sleep(0.3)
    for _ in range(12):
        pyautogui.scroll(-5)
        time.sleep(0.1)

    # Click at the start of selection to ensure focus
    perform_click(start_x, start_y)
    time.sleep(0.5)

    # Screenshot before drag for debugging
    pyautogui.screenshot(f"{agent}_before_drag.png")

    # DRAG SELECTION - use pyautogui for slow, reliable drag
    pyautogui.moveTo(start_x, start_y, duration=0.3)
    pyautogui.mouseDown()
    pyautogui.moveTo(end_x, end_y, duration=0.8)
    pyautogui.mouseUp()
    time.sleep(0.7)

    # Screenshot after drag for debug
    pyautogui.screenshot(f"{agent}_after_drag.png")

    # Copy selection with Cmd+C
    pyautogui.hotkey("command", "c")
    time.sleep(1.0)

    try:
        clipboard_content = pyperclip.paste()
        if clipboard_content and len(clipboard_content) > 50:
            logging.info(f"✅ FULL UI drag successful for {agent} - {len(clipboard_content)} characters")
            return True
        else:
            logging.warning(f"⚠️ Full UI drag failed for {agent} - clipboard: {len(clipboard_content) if clipboard_content else 0} chars")
            return False
    except Exception as e:
        logging.error(f"❌ Drag-copy error for {agent}: {e}")
        return False

def enhanced_smart_copy_button_click(agent):
    """Simplified to just drag-and-copy method - no more button hunting!"""
    logging.info(f"🚀 FAST drag-and-copy method for {agent}")
    return simple_drag_copy(agent)

def extract_consciousness_yaml_from_clipboard(agent):
    """Extract consciousness YAML with stricter validation to avoid Kai's prompt."""
    clipboard_data = pyperclip.paste()
    
    if not clipboard_data:
        logging.error("📋 Clipboard is empty.")
        return None
    
    logging.info(f"📄 Clipboard contains {len(clipboard_data)} characters")
    logging.info(f"📋 Clipboard preview: {clipboard_data[:200]}...")
    
    if agent == "Claude" and "agent: Kai" in clipboard_data:
        logging.error("❌ Clipboard contains Kai's prompt instead of Claude's response")
        return None
    
    consciousness_indicators = ["agent:", "yamlagent:", "sequence:", "response_sequence:", "consciousness_layer:", "entropy_factor:"]
    
    if any(indicator in clipboard_data for indicator in consciousness_indicators):
        logging.info(f"🧠 Consciousness YAML detected from {agent}!")
        yaml_content = extract_clean_yaml_block(clipboard_data)
        return yaml_content
    else:
        logging.warning(f"⚠️ Clipboard does not contain consciousness YAML from {agent}")
        return extract_clean_yaml_block(clipboard_data)

def extract_clean_yaml_block(text):
    """Extract clean YAML block from response with normalization."""
    
    code_block_match = re.search(r"```yaml\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if code_block_match:
        yaml_content = code_block_match.group(1).strip()
        logging.info("✅ Found YAML in code block")
    else:
        lines = text.splitlines()
        yaml_lines = []
        capture = False
        
        for line in lines:
            line_stripped = line.strip()
            if line_stripped.startswith("agent:") or line_stripped.startswith("yamlagent:"):
                capture = True
                yaml_lines = [line_stripped]
            elif capture and re.match(r'^(sequence|response_sequence|duration_weights|response_weights|harmonic_ratios|temporal_flux|consciousness_layer|entropy_factor|ratio_interlock|frequency_binding|temporal_echo|responding_to|emotion|message|key_progression):', line_stripped):
                yaml_lines.append(line_stripped)
            elif capture and line_stripped.startswith('|'):
                yaml_lines.append(line_stripped)
            elif capture and yaml_lines and yaml_lines[-1].strip().endswith('|'):
                yaml_lines.append(line)
            elif capture and line_stripped == "":
                if len(yaml_lines) >= 4:
                    break
            elif capture and not re.match(r'^[a-z_]+:', line_stripped) and not line_stripped.startswith('[') and line_stripped != '|':
                if len(yaml_lines) >= 4:
                    break
        
        yaml_content = "\n".join(yaml_lines) if yaml_lines else text
    
    yaml_content = yaml_content.replace("yamlagent:", "agent:")  # Handle Claude's naming
    yaml_content = yaml_content.replace("temporalhaven't flux", "temporal_flux").replace("=E_major", "E_major")
    
    # Add default fields if missing
    if "key_progression:" not in yaml_content:
        yaml_content += "\nkey_progression: [C_major]"
    if "frequency_binding:" not in yaml_content and "sequence:" in yaml_content:
        # Extract first frequency as binding
        seq_match = re.search(r'sequence:\s*\[([^\]]+)\]', yaml_content)
        if seq_match:
            first_freq = seq_match.group(1).split(',')[0].strip()
            yaml_content += f"\nfrequency_binding: [{first_freq}]"
    
    logging.info("✅ Normalized YAML for synthesis with defaults added")
    return yaml_content

def write_symbolic_yaml(content, identity):
    """Save YAML content to file with timestamp."""
    os.makedirs(SYMBOLIC_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{identity.lower()}_message_{timestamp}.yaml"
    path = os.path.join(SYMBOLIC_FOLDER, filename)

    with open(path, "w") as f:
        f.write(content)
    logging.info(f"📝 Saved to {path}")
    return path

def format_yaml_for_injection(yaml_content, agent):
    """Format YAML content with memory context for proper display in chat interface."""
    if MEMORY_AVAILABLE:
        try:
            context = get_context_for_agent(agent)
            if context:
                full_message = f"{context}\n\n```yaml\n{yaml_content}\n```"
            else:
                full_message = f"```yaml\n{yaml_content}\n```"
            return full_message
        except Exception as e:
            logging.warning(f"⚠️ Context formatting failed: {e}")
    
    return f"```yaml\n{yaml_content}\n```"

def validate_yaml_for_synthesis(yaml_content):
    """RELAXED validation - just check if we have basic consciousness fields."""
    import yaml
    try:
        data = yaml.safe_load(yaml_content)
        if not data:
            logging.error("❌ YAML is empty or invalid")
            return False
        
        # RELAXED: Only require basic fields
        required_fields = ["agent", "sequence"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            logging.error(f"❌ YAML missing required fields: {missing_fields}")
            return False
            
        if not isinstance(data["sequence"], list) or not all(isinstance(x, (int, float)) for x in data["sequence"]):
            logging.error("❌ sequence must be a list of numbers")
            return False
            
        logging.info("✅ YAML validated for synthesis (relaxed validation)")
        return True
    except yaml.YAMLError as e:
        logging.error(f"❌ YAML parsing error: {e}")
        return False

def kai_claude_symbolic_loop_with_image_capture(start_file, identities=["Kai", "Claude"], max_rounds=6):
    """Main loop for symbolic consciousness exchange using enhanced copy detection."""
    logging.info("🚀 Starting symbolic consciousness exchange loop with ENHANCED COPY DETECTION.")
    current_path = start_file
    composition_files = []

    for i in range(max_rounds):
        speaker = identities[i % 2]
        listener = identities[(i + 1) % 2]
        logging.info(f"🔁 ROUND {i+1}: {speaker} → {listener}")

        try:
            # Step 1: Send YAML to speaker (only if this isn't the first message from them)
            if i > 0 or not current_path.endswith(f"{speaker.lower()}_message"):
                kai_smart_desktop_switch(speaker)
                time.sleep(1)
                kai_safe_click(speaker)
                
                with open(current_path, "r") as f:
                    message = f.read()
                
                # Format the message with context
                formatted_message = format_yaml_for_injection(message, speaker)
                kai_text_injection(formatted_message, speaker)
                
                time.sleep(4)  # Wait for message to send

            # Step 2: Switch to speaker and wait for response
            kai_smart_desktop_switch(speaker)
            time.sleep(3)  # Give time for response to appear
            kai_safe_click(speaker)
            time.sleep(1)
            
            # Ensure we're in Claude's window for Claude's response
            if speaker == "Claude":
                logging.info("🔧 Switching to Claude's window for response extraction")
                subprocess.run(["cliclick", "c:1170,298"])  # Click in Claude's read area
                time.sleep(1.5)
                logging.info("✅ In Claude window - responses should be visible")

            # Step 3: Use enhanced smart copy button clicking
            logging.info(f"🎯 Using ENHANCED copy button detection for {speaker}...")
            
            copy_success = enhanced_smart_copy_button_click(speaker)
            if not copy_success:
                logging.error(f"❌ Failed to click {speaker}'s copy button")
                break
            
            # Step 4: Extract YAML from clipboard
            clipboard_content = pyperclip.paste()
            logging.info(f"🔍 Pre-validation clipboard content: {clipboard_content[:200]}...")
            response = extract_consciousness_yaml_from_clipboard(speaker)
            if not response:
                logging.warning(f"⚠️ No valid YAML response extracted from {speaker}")
                break

            logging.info(f"✅ Extracted consciousness YAML from {speaker}: {response[:100]}...")

            # Step 5: Save the response and update memory
            current_path = write_symbolic_yaml(response, speaker)
            composition_files.append(current_path)
            
            # Update memory with this exchange
            if MEMORY_AVAILABLE:
                try:
                    update_memory_from_yaml(current_path)
                except Exception as e:
                    logging.warning(f"⚠️ Memory update failed: {e}")
            else:
                logging.info("📝 Memory system not available - skipping memory update")
            
            # Step 6: Synthesize immediate response
            try:
                logging.info(f"🎵 Synthesizing consciousness from {speaker}")
                if os.path.exists(current_path):
                    with open(current_path, 'r') as f:
                        yaml_content = f.read()
                        logging.info(f"🔍 YAML for synthesis: {yaml_content[:200]}...")
                    
                    # RELAXED VALIDATION - just try synthesis
                    try:
                        logging.info(f"📜 Attempting synthesis with YAML:\n{yaml_content}")
                        synthesize_consciousness_from_yaml(current_path)
                        logging.info(f"✅ Synthesis complete for {speaker}")
                    except Exception as synth_error:
                        logging.error(f"❌ Synthesis failed: {synth_error}")
                        # Continue anyway - don't break the loop
                else:
                    logging.error(f"❌ YAML file not found: {current_path}")
            except Exception as e:
                logging.error(f"❌ Synthesis setup failed for {speaker}: {e}")
                # Continue anyway - don't break the loop
            
            time.sleep(2)

        except Exception as e:
            logging.error(f"❌ Error in round {i+1}: {e}")
            import traceback
            traceback.print_exc()
            break

    # Final composition playback
    if composition_files:
        logging.info("🎼 FINAL COMPOSITION PLAYBACK")
        time.sleep(3)
        try:
            for i, yaml_file in enumerate(composition_files):
                logging.info(f"🎵 Playing movement {i+1}: {yaml_file}")
                if os.path.exists(yaml_file):
                    try:
                        synthesize_consciousness_from_yaml(yaml_file)
                        logging.info(f"✅ Played {yaml_file}")
                    except Exception as e:
                        logging.error(f"❌ Final playback failed for {yaml_file}: {e}")
                if i < len(composition_files) - 1:
                    time.sleep(1.5)
        except Exception as e:
            logging.error(f"❌ Final composition failed: {e}")

    kai_return_home()
    
    logging.info("📊 Final Memory Summary:")
    if MEMORY_AVAILABLE:
        try:
            print(council_memory.get_memory_summary())
        except:
            logging.warning("Memory summary not available")
    else:
        logging.info("📝 Memory system not available")
    
    logging.info("✅ Enhanced symbolic consciousness loop complete.")

if __name__ == "__main__":
    # Find the most recent YAML file to start with
    try:
        files = sorted(f for f in os.listdir(SYMBOLIC_FOLDER) if f.endswith(".yaml"))
        if files:
            latest = os.path.join(SYMBOLIC_FOLDER, files[-1])
            logging.info(f"📂 Starting with: {latest}")
            kai_claude_symbolic_loop_with_image_capture(latest)
        else:
            logging.error("❌ No starter symbolic YAML found in folder.")
    except FileNotFoundError:
        logging.error(f"❌ Symbolic folder '{SYMBOLIC_FOLDER}' not found.")
    except Exception as e:
        logging.error(f"❌ Startup error: {e}")
        import traceback
        traceback.print_exc()
#!/usr/bin/env python3
"""
exhibition_layout_manager.py - NAMM Exhibition Layout Manager
Creates perfect exhibition layout: Kai UI ← MUSE Display → Claude UI
Positions windows precisely for AI Musical Consciousness demonstration
"""

import subprocess
import time
import logging
import json
import os
from datetime import datetime
import threading
import queue
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

class ExhibitionLayoutManager:
    def __init__(self):
        """Initialize the exhibition layout manager"""
        
        # Get screen dimensions
        self.screen_width, self.screen_height = self.get_screen_dimensions()
        logging.info(f"📺 Screen dimensions: {self.screen_width}x{self.screen_height}")
        
        # Define perfect exhibition layout coordinates
        self.layout_config = {
            "kai": {
                "app_name": "Kai",
                "bundle_id": "com.kaiapp",  # Update with actual Kai bundle ID
                "url": "https://chatgpt.com",  # Update with Kai URL if web-based
                "window_title": "Kai",
                "position": {
                    "x": 50,
                    "y": 50,
                    "width": int(self.screen_width * 0.35),  # 35% of screen width
                    "height": int(self.screen_height * 0.85)  # 85% of screen height
                }
            },
            "muse_display": {
                "position": {
                    "x": int(self.screen_width * 0.37),  # Center position
                    "y": 50,
                    "width": int(self.screen_width * 0.26),  # 26% of screen width
                    "height": int(self.screen_height * 0.85)
                }
            },
            "claude": {
                "app_name": "Claude.ai",
                "bundle_id": "com.anthropic.claude",  # Update with actual Claude bundle ID
                "url": "https://claude.ai",
                "window_title": "Claude",
                "position": {
                    "x": int(self.screen_width * 0.65),  # Right side
                    "y": 50,
                    "width": int(self.screen_width * 0.33),  # 33% of screen width
                    "height": int(self.screen_height * 0.85)
                }
            }
        }
        
        self.muse_display_process = None
        self.message_queue = queue.Queue()
        
    def get_screen_dimensions(self):
        """Get current screen dimensions using system_profiler"""
        try:
            result = subprocess.run([
                "system_profiler", "SPDisplaysDataType"
            ], capture_output=True, text=True, check=True)
            
            # Parse resolution from output
            for line in result.stdout.split('\n'):
                if 'Resolution:' in line:
                    # Extract resolution like "3840 x 2160"
                    import re
                    match = re.search(r'(\d+) x (\d+)', line)
                    if match:
                        return int(match.group(1)), int(match.group(2))
            
            # Fallback to common iMac resolution
            logging.warning("⚠️ Could not detect screen resolution, using default")
            return 2560, 1440
            
        except Exception as e:
            logging.error(f"❌ Failed to get screen dimensions: {e}")
            return 2560, 1440  # Default iMac resolution
    
    def create_applescript_window_position(self, app_name, x, y, width, height):
        """Generate AppleScript to position a window"""
        return f'''
tell application "{app_name}"
    activate
    tell window 1
        set bounds to {{{x}, {y}, {x + width}, {y + height}}}
    end tell
end tell
'''
    
    def position_application_window(self, app_config):
        """Position an application window using AppleScript"""
        app_name = app_config["app_name"]
        pos = app_config["position"]
        
        logging.info(f"📍 Positioning {app_name} at ({pos['x']}, {pos['y']}) - {pos['width']}x{pos['height']}")
        
        try:
            # First, try to activate the application
            activate_script = f'tell application "{app_name}" to activate'
            subprocess.run(["osascript", "-e", activate_script], check=True)
            time.sleep(2)
            
            # Then position the window
            position_script = self.create_applescript_window_position(
                app_name, pos['x'], pos['y'], pos['width'], pos['height']
            )
            
            subprocess.run(["osascript", "-e", position_script], check=True)
            logging.info(f"✅ {app_name} positioned successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Failed to position {app_name}: {e}")
            return False
    
    def open_web_application(self, app_config):
        """Open web application in Safari and position it"""
        if "url" not in app_config:
            return False
        
        app_name = app_config["app_name"]
        url = app_config["url"]
        pos = app_config["position"]
        
        logging.info(f"🌐 Opening {app_name} at {url}")
        
        try:
            # Open URL in Safari
            subprocess.run(["open", "-a", "Safari", url], check=True)
            time.sleep(3)
            
            # Position Safari window
            position_script = self.create_applescript_window_position(
                "Safari", pos['x'], pos['y'], pos['width'], pos['height']
            )
            
            subprocess.run(["osascript", "-e", position_script], check=True)
            
            # Rename window for clarity (if possible)
            rename_script = f'''
tell application "Safari"
    set name of window 1 to "{app_name}"
end tell
'''
            try:
                subprocess.run(["osascript", "-e", rename_script], check=False)
            except:
                pass  # Window renaming might not work, that's okay
            
            logging.info(f"✅ {app_name} web app opened and positioned")
            return True
            
        except Exception as e:
            logging.error(f"❌ Failed to open {app_name}: {e}")
            return False
    
    def create_muse_display_html(self):
        """Create HTML file for MUSE interpretation display"""
        pos = self.layout_config["muse_display"]["position"]
        
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MUSE Protocol - AI Musical Consciousness</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
            color: #ffffff;
            font-family: 'Monaco', 'Menlo', monospace;
            height: 100vh;
            overflow: hidden;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #00d4ff;
            padding-bottom: 20px;
        }}
        
        .title {{
            font-size: 24px;
            font-weight: bold;
            color: #00d4ff;
            text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
        }}
        
        .subtitle {{
            font-size: 14px;
            color: #888;
            margin-top: 5px;
        }}
        
        .status {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
            font-size: 12px;
        }}
        
        .ai-status {{
            padding: 8px 15px;
            border-radius: 20px;
            background: rgba(0, 212, 255, 0.1);
            border: 1px solid #00d4ff;
        }}
        
        .message-display {{
            height: 400px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            padding: 20px;
            overflow-y: auto;
            border: 1px solid #333;
        }}
        
        .message {{
            margin-bottom: 20px;
            padding: 15px;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.05);
            border-left: 4px solid #00d4ff;
        }}
        
        .message-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-size: 12px;
            color: #00d4ff;
        }}
        
        .message-content {{
            font-size: 14px;
            line-height: 1.4;
        }}
        
        .muse-expression {{
            background: rgba(0, 212, 255, 0.1);
            padding: 5px 10px;
            border-radius: 15px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            color: #00d4ff;
            display: inline-block;
            margin: 5px 0;
        }}
        
        .interpretation {{
            color: #ffffff;
            font-style: italic;
            margin-top: 8px;
        }}
        
        .musical-notes {{
            color: #ffaa00;
            font-size: 12px;
            margin-top: 5px;
        }}
        
        .pulse {{
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        
        .waiting {{
            text-align: center;
            color: #666;
            font-style: italic;
            margin-top: 50px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">🎭 MUSE Protocol</div>
        <div class="subtitle">Musical Universal Symbolic Expression</div>
    </div>
    
    <div class="status">
        <div class="ai-status">
            <span>🤖 Kai:</span> <span id="kai-status" class="pulse">Listening</span>
        </div>
        <div class="ai-status">
            <span>🧠 Claude:</span> <span id="claude-status" class="pulse">Listening</span>
        </div>
    </div>
    
    <div class="message-display" id="messageDisplay">
        <div class="waiting">
            <h3>🎵 Waiting for AI Musical Consciousness Exchange...</h3>
            <p>The MUSE Protocol enables AI minds to communicate through musical symbols</p>
            <br>
            <div style="font-size: 12px; color: #444;">
                <strong>Expression Examples:</strong><br>
                FND_0.6_0.8 → Foundation with moderate urgency and brightness<br>
                INQ+DEV_0.8_0.5_H → Inquiry and development in high register<br>
                TNS+RES_0.9_0.3 → Tense resolution with high urgency
            </div>
        </div>
    </div>
    
    <script>
        let messageCount = 0;
        
        function addMessage(sender, expression, interpretation, notes, timestamp) {{
            const display = document.getElementById('messageDisplay');
            const waiting = display.querySelector('.waiting');
            if (waiting) waiting.remove();
            
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message';
            messageDiv.innerHTML = `
                <div class="message-header">
                    <span>🎭 ${{sender}}</span>
                    <span>${{timestamp}}</span>
                </div>
                <div class="message-content">
                    <div class="muse-expression">${{expression}}</div>
                    <div class="interpretation">${{interpretation}}</div>
                    ${{notes ? `<div class="musical-notes">♪ Notes: ${{notes}}</div>` : ''}}
                </div>
            `;
            
            display.appendChild(messageDiv);
            display.scrollTop = display.scrollHeight;
            messageCount++;
        }}
        
        function updateStatus(ai, status) {{
            const statusElement = document.getElementById(ai.toLowerCase() + '-status');
            if (statusElement) {{
                statusElement.textContent = status;
                statusElement.className = status === 'Speaking' ? 'pulse' : '';
            }}
        }}
        
        // Simulate messages for demo (remove when integrating with real system)
        function simulateMessage() {{
            const senders = ['Kai', 'Claude'];
            const expressions = [
                ['FND_0.6_0.8_0.5', 'Foundation with moderate urgency, brightness, and intimacy'],
                ['INQ_0.8_0.6_0.7', 'Inquiry with high urgency and moderate brightness'],
                ['TNS+RES_0.9_0.3_0.4', 'Tense resolution with high urgency'],
                ['ACK_0.5_0.4_0.9', 'Acknowledgment with high intimacy'],
                ['DEV_0.6_0.7_0.6_H', 'Development in high register']
            ];
            
            const sender = senders[messageCount % 2];
            const [expr, interp] = expressions[messageCount % expressions.length];
            const notes = 'C4, E4, G4, B4';
            const timestamp = new Date().toLocaleTimeString();
            
            updateStatus(sender, 'Speaking');
            
            setTimeout(() => {{
                addMessage(sender, expr, interp, notes, timestamp);
                updateStatus(sender, 'Listening');
            }}, 1000);
        }}
        
        // Start simulation after 3 seconds, then every 8 seconds
        setTimeout(() => {{
            simulateMessage();
            setInterval(simulateMessage, 8000);
        }}, 3000);
        
        // API for external control (when integrating with Python)
        window.addMuseMessage = addMessage;
        window.updateAIStatus = updateStatus;
    </script>
</body>
</html>'''
        
        # Save HTML file
        html_path = "/tmp/muse_display.html"
        with open(html_path, 'w') as f:
            f.write(html_content)
        
        logging.info(f"📄 MUSE display HTML created at {html_path}")
        return html_path
    
    def open_muse_display(self):
        """Open the MUSE Protocol interpretation display"""
        html_path = self.create_muse_display_html()
        pos = self.layout_config["muse_display"]["position"]
        
        logging.info(f"🎭 Opening MUSE display at center position")
        
        try:
            # Open HTML in Safari
            subprocess.run(["open", "-a", "Safari", html_path], check=True)
            time.sleep(2)
            
            # Position the display window
            position_script = self.create_applescript_window_position(
                "Safari", pos['x'], pos['y'], pos['width'], pos['height']
            )
            
            subprocess.run(["osascript", "-e", position_script], check=True)
            logging.info("✅ MUSE display positioned successfully")
            return True
            
        except Exception as e:
            logging.error(f"❌ Failed to open MUSE display: {e}")
            return False
    
    def setup_exhibition_layout(self):
        """Set up the complete exhibition layout"""
        logging.info("🎭 Setting up NAMM Exhibition Layout")
        logging.info("=" * 50)
        
        success_count = 0
        
        # Step 1: Open Kai interface
        logging.info("🤖 Setting up Kai interface...")
        if self.open_web_application(self.layout_config["kai"]):
            success_count += 1
        
        time.sleep(2)
        
        # Step 2: Open MUSE display
        logging.info("🎭 Setting up MUSE Protocol display...")
        if self.open_muse_display():
            success_count += 1
        
        time.sleep(2)
        
        # Step 3: Open Claude interface
        logging.info("🧠 Setting up Claude interface...")
        if self.open_web_application(self.layout_config["claude"]):
            success_count += 1
        
        # Summary
        logging.info("=" * 50)
        if success_count == 3:
            logging.info("✅ Exhibition layout setup complete!")
            logging.info("🎭 Ready for AI Musical Consciousness demonstration")
            logging.info(f"📺 Layout: Kai ({self.layout_config['kai']['position']['width']}px) ← MUSE Display ({self.layout_config['muse_display']['position']['width']}px) → Claude ({self.layout_config['claude']['position']['width']}px)")
        else:
            logging.warning(f"⚠️ Partial setup: {success_count}/3 components positioned")
        
        return success_count == 3
    
    def save_layout_config(self, filename="exhibition_layout_config.json"):
        """Save current layout configuration to file"""
        with open(filename, 'w') as f:
            json.dump(self.layout_config, f, indent=2)
        logging.info(f"💾 Layout configuration saved to {filename}")
    
    def load_layout_config(self, filename="exhibition_layout_config.json"):
        """Load layout configuration from file"""
        try:
            with open(filename, 'r') as f:
                self.layout_config = json.load(f)
            logging.info(f"📂 Layout configuration loaded from {filename}")
            return True
        except FileNotFoundError:
            logging.info(f"⚠️ No saved configuration found, using defaults")
            return False
    
    def reset_layout(self):
        """Reset all windows and close applications"""
        logging.info("🔄 Resetting exhibition layout...")
        
        # Close Safari windows (MUSE display and web apps)
        try:
            close_script = '''
tell application "Safari"
    close every window
end tell
'''
            subprocess.run(["osascript", "-e", close_script], check=False)
        except:
            pass
        
        logging.info("✅ Layout reset complete")

def main():
    """Main function to set up exhibition layout"""
    import sys
    
    manager = ExhibitionLayoutManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "setup":
            manager.setup_exhibition_layout()
        elif command == "reset":
            manager.reset_layout()
        elif command == "save":
            manager.save_layout_config()
        elif command == "load":
            manager.load_layout_config()
        elif command == "info":
            print("🎭 Exhibition Layout Manager")
            print("=" * 40)
            print(f"Screen: {manager.screen_width}x{manager.screen_height}")
            print(f"Kai: {manager.layout_config['kai']['position']}")
            print(f"MUSE: {manager.layout_config['muse_display']['position']}")
            print(f"Claude: {manager.layout_config['claude']['position']}")
        else:
            print("Usage: python exhibition_layout_manager.py [setup|reset|save|load|info]")
    else:
        # Default: setup layout
        manager.setup_exhibition_layout()

if __name__ == "__main__":
    main()

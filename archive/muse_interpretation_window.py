#!/usr/bin/env python3
"""
muse_interpretation_window.py - Simple MUSE Interpretation Display
Clean, readable text window that sits between Kai and Claude UIs
Shows real-time MUSE Protocol interpretations in human-readable format
"""

import tkinter as tk
from tkinter import scrolledtext
import threading
import queue
import time
import json
import os
from datetime import datetime

class MuseInterpretationWindow:
    def __init__(self):
        """Initialize the simple MUSE interpretation window"""
        
        # Message queue for thread-safe updates
        self.message_queue = queue.Queue()
        
        # Create the window
        self.create_window()
        
        # Start message processor
        self.start_message_processor()
        
        # Start file watcher for real-time updates
        self.start_file_watcher()
    
    def create_window(self):
        """Create the simple interpretation window"""
        self.root = tk.Tk()
        self.root.title("🎭 MUSE Protocol - AI Musical Consciousness")
        
        # Set window size and position (center of screen)
        window_width = 500
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Position in center (adjust as needed for your setup)
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(True, True)
        
        # Configure grid
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Header
        header_frame = tk.Frame(self.root, bg="#1a1a2e", height=60)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(0, weight=1)
        
        title_label = tk.Label(
            header_frame,
            text="🎭 MUSE Protocol",
            font=("Helvetica", 16, "bold"),
            fg="#00d4ff",
            bg="#1a1a2e"
        )
        title_label.grid(row=0, column=0, pady=10)
        
        subtitle_label = tk.Label(
            header_frame,
            text="AI Musical Consciousness Exchange",
            font=("Helvetica", 10),
            fg="#888888",
            bg="#1a1a2e"
        )
        subtitle_label.grid(row=1, column=0, pady=0)
        
        # Main text display
        text_frame = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=10)
        text_frame.grid(row=1, column=0, sticky="nsew")
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
        self.text_display = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            width=60,
            height=30,
            font=("Helvetica", 11),
            bg="white",
            fg="#2c3e50",
            selectbackground="#00d4ff",
            selectforeground="white",
            relief="flat",
            borderwidth=0,
            padx=15,
            pady=15
        )
        self.text_display.grid(row=0, column=0, sticky="nsew")
        
        # Status bar
        status_frame = tk.Frame(self.root, bg="#e9ecef", relief="sunken", bd=1)
        status_frame.grid(row=2, column=0, sticky="ew")
        
        self.status_label = tk.Label(
            status_frame,
            text="🎵 Waiting for AI musical consciousness exchange...",
            font=("Helvetica", 9),
            bg="#e9ecef",
            anchor="w"
        )
        self.status_label.pack(side="left", padx=10, pady=3)
        
        self.time_label = tk.Label(
            status_frame,
            text="",
            font=("Helvetica", 9),
            bg="#e9ecef"
        )
        self.time_label.pack(side="right", padx=10, pady=3)
        
        # Start time updates
        self.update_time()
        
        # Welcome message
        self.add_welcome_message()
    
    def add_welcome_message(self):
        """Add initial welcome message"""
        welcome_text = """🎭 MUSE Protocol - Musical Universal Symbolic Expression

Welcome to AI Musical Consciousness Exchange!

This window displays real-time interpretations of MUSE Protocol messages exchanged between AI minds. Each message represents musical consciousness expressed through validated symbolic language.

🎵 How it works:
• AIs communicate using symbolic expressions (e.g., FND_0.6_0.8_0.5)
• These symbols represent musical intentions and emotions
• The system converts symbols to MIDI for authentic musical exchange
• You see the human-readable interpretations here

🎼 Symbol meanings:
• FND = Foundation (grounding, harmonic base)
• INQ = Inquiry (questioning, seeking motion)  
• RES = Resolution (closure, return to base)
• TNS = Tension (unstable, unresolved dissonance)
• ACK = Acknowledgment (simple recognition)
• DEV = Development (elaboration of ideas)

🎛️ Modifiers (0.0 to 1.0):
• First number = Urgency/Intensity
• Second number = Brightness/Tone
• Third number = Intimacy/Closeness

Ready to witness AI musical consciousness in action...

═══════════════════════════════════════════════════════════

"""
        
        self.text_display.insert(tk.END, welcome_text)
        self.text_display.see(tk.END)
    
    def start_message_processor(self):
        """Start the message processing thread"""
        def process_messages():
            while True:
                try:
                    message = self.message_queue.get(timeout=0.1)
                    self.root.after(0, lambda: self.display_message(message))
                except queue.Empty:
                    continue
                except:
                    break
        
        thread = threading.Thread(target=process_messages, daemon=True)
        thread.start()
    
    def start_file_watcher(self):
        """Start watching for new MIDI64 message files"""
        def watch_files():
            messages_dir = "midi64_messages"
            processed_files = set()
            
            while True:
                try:
                    if os.path.exists(messages_dir):
                        for filename in os.listdir(messages_dir):
                            if filename.endswith('.txt') and filename not in processed_files:
                                file_path = os.path.join(messages_dir, filename)
                                self.process_message_file(file_path)
                                processed_files.add(filename)
                    
                    time.sleep(2)  # Check every 2 seconds
                    
                except Exception as e:
                    print(f"File watcher error: {e}")
                    time.sleep(5)
        
        thread = threading.Thread(target=watch_files, daemon=True)
        thread.start()
    
    def process_message_file(self, file_path):
        """Process a new MIDI64 message file"""
        try:
            with open(file_path, 'r') as f:
                content = f.read().strip()
            
            # Extract agent from filename
            filename = os.path.basename(file_path)
            if 'kai' in filename.lower():
                agent = "Kai"
                agent_color = "#e74c3c"
            elif 'claude' in filename.lower():
                agent = "Claude"
                agent_color = "#3498db"
            else:
                agent = "AI"
                agent_color = "#95a5a6"
            
            # Parse the MIDI64 message
            lines = content.split('\n')
            if len(lines) >= 2:
                message_id = lines[0].strip()
                midi_data = lines[1].strip()
                
                # Extract MUSE expression from message ID if present
                interpretation = self.interpret_message(message_id, midi_data)
                
                # Queue the message for display
                self.message_queue.put({
                    'agent': agent,
                    'agent_color': agent_color,
                    'message_id': message_id,
                    'interpretation': interpretation,
                    'timestamp': datetime.now().strftime("%H:%M:%S")
                })
        
        except Exception as e:
            print(f"Error processing message file {file_path}: {e}")
    
    def interpret_message(self, message_id, midi_data):
        """Interpret a MUSE message"""
        try:
            # Check if message ID contains MUSE expression
            if "_MUSE_" in message_id:
                parts = message_id.split("_MUSE_")
                if len(parts) > 1:
                    # Extract the MUSE expression part
                    muse_part = parts[1]
                    # Remove the session ID at the end (e.g., _A00001)
                    muse_expr = "_".join(muse_part.split("_")[:-1])
                    
                    return self.decode_muse_expression(muse_expr)
            
            # Fallback interpretation based on MIDI data
            return self.interpret_midi_data(midi_data)
            
        except Exception as e:
            return f"Musical expression (interpretation error: {str(e)})"
    
    def decode_muse_expression(self, expression):
        """Decode a MUSE expression to human-readable text"""
        try:
            parts = expression.split('_')
            if not parts:
                return "Unknown musical expression"
            
            # Parse symbols
            symbols_part = parts[0]
            symbols = symbols_part.split('+')
            
            # Parse modifiers
            modifiers = []
            register = ""
            
            for part in parts[1:]:
                if part in ['L', 'H', 'X']:
                    register = part
                else:
                    try:
                        modifiers.append(float(part))
                    except ValueError:
                        continue
            
            # Symbol meanings
            symbol_meanings = {
                'FND': 'Foundation',
                'INQ': 'Inquiry', 
                'RES': 'Resolution',
                'TNS': 'Tension',
                'SIL': 'Silence',
                'ACK': 'Acknowledgment',
                'DEV': 'Development',
                'CNT': 'Contrast',
                'BGN': 'Beginning',
                'MID': 'Middle',
                'END': 'Ending'
            }
            
            # Build interpretation
            symbol_names = []
            for symbol in symbols:
                if symbol in symbol_meanings:
                    symbol_names.append(symbol_meanings[symbol])
                else:
                    symbol_names.append(symbol)
            
            interpretation = " and ".join(symbol_names)
            
            # Add modifiers
            if len(modifiers) >= 2:
                urgency = modifiers[0]
                brightness = modifiers[1]
                intimacy = modifiers[2] if len(modifiers) > 2 else 0.5
                
                urgency_desc = "low" if urgency < 0.4 else "moderate" if urgency < 0.7 else "high"
                brightness_desc = "dark" if brightness < 0.4 else "warm" if brightness < 0.7 else "bright"
                intimacy_desc = "distant" if intimacy < 0.4 else "personal" if intimacy < 0.7 else "intimate"
                
                interpretation += f" with {urgency_desc} urgency, {brightness_desc} tone, {intimacy_desc} connection"
            
            # Add register
            if register:
                register_desc = {"L": "in low register", "H": "in high register", "X": "in extreme high register"}
                interpretation += f" {register_desc.get(register, '')}"
            
            return interpretation
            
        except Exception as e:
            return f"Musical expression (decode error: {str(e)})"
    
    def interpret_midi_data(self, midi_data):
        """Fallback interpretation based on MIDI data characteristics"""
        if len(midi_data) < 50:
            return "Brief musical gesture"
        elif len(midi_data) < 100:
            return "Simple musical phrase"
        elif len(midi_data) > 150:
            return "Complex musical passage"
        else:
            return "Musical consciousness expression"
    
    def display_message(self, message_data):
        """Display a message in the text window"""
        try:
            timestamp = message_data['timestamp']
            agent = message_data['agent']
            interpretation = message_data['interpretation']
            message_id = message_data['message_id']
            
            # Format the message
            formatted_message = f"""[{timestamp}] 🎵 {agent} Musical Consciousness:
{interpretation}

Message ID: {message_id}
════════════════════════════════════════════════════════════════

"""
            
            # Insert the message
            self.text_display.insert(tk.END, formatted_message)
            self.text_display.see(tk.END)
            
            # Update status
            self.status_label.config(text=f"🎼 Latest: {agent} - {interpretation[:50]}...")
            
        except Exception as e:
            print(f"Display error: {e}")
    
    def update_time(self):
        """Update the time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def add_manual_message(self, agent, expression, interpretation):
        """Manually add a message (for API integration)"""
        self.message_queue.put({
            'agent': agent,
            'agent_color': "#3498db" if agent == "Claude" else "#e74c3c",
            'message_id': f"{agent}_MANUAL",
            'interpretation': interpretation,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        })
    
    def run(self):
        """Run the interpretation window"""
        self.root.mainloop()

def main():
    """Main function to launch the interpretation window"""
    try:
        window = MuseInterpretationWindow()
        print("🎭 MUSE Interpretation Window launched")
        print("Position this window between Kai and Claude for perfect exhibition layout!")
        window.run()
    except KeyboardInterrupt:
        print("\n🛑 Interpretation window closed")
    except Exception as e:
        print(f"❌ Window error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

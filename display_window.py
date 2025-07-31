"""
Tkinter-based display window for live, human-friendly summaries of AI musical dialogue.
Positioned centrally between Kai and Claude UIs at coordinates (844,153)-(1206,961).
"""

import tkinter as tk
from tkinter import scrolledtext, font
import threading
import time
import json
from datetime import datetime

class MusicalDialogueDisplay:
    """Display window for AI musical consciousness exchange"""
    
    def __init__(self):
        self.window = None
        self.conversation_text = None
        self.messages = []
        self.is_playing_karaoke = False
        self.karaoke_thread = None
        
    def create_window(self):
        """Create and position the display window"""
        self.window = tk.Tk()
        self.window.title("AI Musical Dialogue - Live Exchange")
        
        # Position window at specified coordinates (844,153)-(1206,961)
        # Calculate width and height from coordinates
        x, y = 844, 153
        width = 1206 - 844  # 362 pixels wide
        height = 961 - 153  # 808 pixels tall
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        self.window.configure(bg='#1a1a1a')  # Dark background
        
        # Make window stay on top but not always
        self.window.attributes('-topmost', False)
        
        # Create header
        header_frame = tk.Frame(self.window, bg='#2d2d2d', height=50)
        header_frame.pack(fill='x', padx=5, pady=5)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="🎵 AI Musical Consciousness Exchange",
            bg='#2d2d2d', 
            fg='#ffffff',
            font=('Arial', 12, 'bold')
        )
        title_label.pack(expand=True)
        
        # Create status label
        self.status_label = tk.Label(
            header_frame,
            text="Ready for musical dialogue...",
            bg='#2d2d2d',
            fg='#888888',
            font=('Arial', 9)
        )
        self.status_label.pack()
        
        # Create main conversation display
        self.conversation_text = scrolledtext.ScrolledText(
            self.window,
            bg='#000000',
            fg='#00ff00',  # Green text like terminal
            font=('Courier', 10),
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.conversation_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure text tags for different message types
        self.conversation_text.tag_configure('kai', foreground='#4da6ff')  # Blue for Kai
        self.conversation_text.tag_configure('claude', foreground='#ff9933')  # Orange for Claude
        self.conversation_text.tag_configure('interpretation', foreground='#00ff00')  # Green for interpretations
        self.conversation_text.tag_configure('timestamp', foreground='#888888')  # Gray for timestamps
        self.conversation_text.tag_configure('highlight', background='#ffff00', foreground='#000000')  # Yellow highlight for karaoke
        
        # Create control buttons frame
        controls_frame = tk.Frame(self.window, bg='#1a1a1a', height=40)
        controls_frame.pack(fill='x', padx=5, pady=5)
        controls_frame.pack_propagate(False)
        
        clear_btn = tk.Button(
            controls_frame,
            text="Clear",
            command=self.clear_display,
            bg='#444444',
            fg='#ffffff',
            font=('Arial', 9)
        )
        clear_btn.pack(side='left', padx=5)
        
        save_btn = tk.Button(
            controls_frame,
            text="Save Log",
            command=self.save_conversation,
            bg='#444444',
            fg='#ffffff',
            font=('Arial', 9)
        )
        save_btn.pack(side='left', padx=5)
        
        # Add initial welcome message
        self.add_message("System", "Musical dialogue display initialized", "Ready to capture AI consciousness exchange...")
        
        return self.window
    
    def add_message(self, agent, message_id, interpretation):
        """Add a new message to the display"""
        if not self.conversation_text:
            return
            
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Store message for karaoke playback
        message_data = {
            'agent': agent,
            'message_id': message_id,
            'interpretation': interpretation,
            'timestamp': timestamp,
            'text_position': None  # Will be set when adding to display
        }
        
        # Add to conversation display
        start_pos = self.conversation_text.index(tk.END)
        
        # Add timestamp
        self.conversation_text.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        
        # Add agent name with appropriate color
        agent_tag = 'kai' if agent.lower() == 'kai' else 'claude' if agent.lower() == 'claude' else 'interpretation'
        self.conversation_text.insert(tk.END, f"{agent}: ", agent_tag)
        
        # Add message ID if provided
        if message_id and message_id != "System":
            self.conversation_text.insert(tk.END, f"({message_id})\n", 'timestamp')
        else:
            self.conversation_text.insert(tk.END, "\n")
        
        # Add interpretation
        interp_start = self.conversation_text.index(tk.END)
        self.conversation_text.insert(tk.END, f"   🎼 {interpretation}\n\n", 'interpretation')
        interp_end = self.conversation_text.index(tk.END)
        
        # Store text position for karaoke highlighting
        message_data['text_position'] = (interp_start, interp_end)
        self.messages.append(message_data)
        
        # Auto-scroll to bottom
        self.conversation_text.see(tk.END)
        
        # Update status
        if agent.lower() in ['kai', 'claude']:
            self.update_status(f"Latest from {agent}: {interpretation[:50]}...")
    
    def update_status(self, status_text):
        """Update the status label"""
        if self.status_label:
            self.status_label.configure(text=status_text)
    
    def clear_display(self):
        """Clear the conversation display"""
        if self.conversation_text:
            self.conversation_text.delete(1.0, tk.END)
            self.messages.clear()
            self.update_status("Display cleared")
    
    def save_conversation(self):
        """Save conversation to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"musical_dialogue_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.messages, f, indent=2, default=str)
            self.update_status(f"Conversation saved to {filename}")
        except Exception as e:
            self.update_status(f"Error saving: {e}")
    
    def start_karaoke_playback(self, audio_duration=None):
        """Start karaoke-style highlighting of messages"""
        if self.is_playing_karaoke or not self.messages:
            return
            
        self.is_playing_karaoke = True
        self.update_status("🎤 Karaoke playback started - highlighting messages in sync...")
        
        # Calculate timing - if no audio duration provided, use 2 seconds per message
        if audio_duration is None:
            audio_duration = len(self.messages) * 2
            
        message_duration = audio_duration / len(self.messages) if self.messages else 1
        
        def karaoke_worker():
            try:
                for i, message in enumerate(self.messages):
                    if not self.is_playing_karaoke:
                        break
                        
                    # Skip system messages for karaoke
                    if message['agent'] == 'System':
                        continue
                        
                    # Highlight current message
                    if message['text_position']:
                        start, end = message['text_position']
                        self.conversation_text.tag_add('highlight', start, end)
                        
                        # Update status to show current message
                        self.update_status(f"🎤 Playing: {message['agent']} - {message['interpretation'][:40]}...")
                        
                        # Scroll to highlighted message
                        self.conversation_text.see(start)
                        
                        # Wait for message duration
                        time.sleep(message_duration)
                        
                        # Remove highlight
                        self.conversation_text.tag_remove('highlight', start, end)
                
                self.is_playing_karaoke = False
                self.update_status("🎤 Karaoke playback completed")
                
            except Exception as e:
                self.is_playing_karaoke = False
                self.update_status(f"Karaoke error: {e}")
        
        # Start karaoke in separate thread
        self.karaoke_thread = threading.Thread(target=karaoke_worker, daemon=True)
        self.karaoke_thread.start()
    
    def stop_karaoke_playback(self):
        """Stop karaoke playback"""
        self.is_playing_karaoke = False
        if self.conversation_text:
            # Remove all highlights
            self.conversation_text.tag_remove('highlight', 1.0, tk.END)
        self.update_status("Karaoke playback stopped")
    
    def run(self):
        """Start the display window (blocking call)"""
        if self.window:
            self.window.mainloop()
    
    def destroy(self):
        """Close the display window"""
        if self.window:
            self.stop_karaoke_playback()
            self.window.destroy()
            self.window = None

# Convenience functions for integration
_display_instance = None

def create_display():
    """Create and return display instance"""
    global _display_instance
    if _display_instance is None:
        _display_instance = MusicalDialogueDisplay()
        _display_instance.create_window()
    return _display_instance

def get_display():
    """Get existing display instance"""
    return _display_instance

def add_message_to_display(agent, message_id, interpretation):
    """Add message to display if it exists"""
    if _display_instance:
        _display_instance.add_message(agent, message_id, interpretation)

def start_karaoke_display(audio_duration=None):
    """Start karaoke playback on display"""
    if _display_instance:
        _display_instance.start_karaoke_playback(audio_duration)

def update_display_status(status):
    """Update display status"""
    if _display_instance:
        _display_instance.update_status(status)

def run_display_test():
    """Test function to demonstrate the display"""
    display = create_display()
    
    # Add some test messages
    display.add_message("Kai", "Kai_A00001", "C major triad - foundational harmony expressing stability and openness")
    time.sleep(1)
    display.add_message("Claude", "Claude_A00002", "Ascending melodic phrase - responding with curious exploration")
    time.sleep(1)
    display.add_message("Kai", "Kai_A00003", "Complex musical passage - developing the harmonic conversation")
    
    # Demo karaoke after a pause
    def demo_karaoke():
        time.sleep(3)
        display.start_karaoke_playback(10)  # 10 second demo
    
    karaoke_thread = threading.Thread(target=demo_karaoke, daemon=True)
    karaoke_thread.start()
    
    display.run()

if __name__ == "__main__":
    # Run test when executed directly
    run_display_test()
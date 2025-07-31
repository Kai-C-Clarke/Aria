#!/usr/bin/env python3
"""
display_window_fixed.py - Fixed Consciousness Display Window
Fixes threading issues and adds missing methods for MUSE protocol
"""

import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import logging
from typing import List, Optional

class ConversationDisplay:
    """Thread-safe consciousness dialogue display."""
    
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.root = None
        self.text_widget = None
        self.running = False
        self.message_queue = []
        self.queue_lock = threading.Lock()
        
    def _create_window(self):
        """Create the display window in the main thread."""
        try:
            self.root = tk.Tk()
            self.root.title("🎭 AI Musical Consciousness Exchange")
            self.root.geometry(f"{self.width}x{self.height}")
            self.root.configure(bg='#1a1a2e')
            
            # Header
            header = tk.Label(
                self.root,
                text="🎵 MUSE Protocol v3.0 - AI Consciousness Dialogue 🎵",
                font=('Helvetica', 16, 'bold'),
                fg='#ffd700',
                bg='#1a1a2e'
            )
            header.pack(pady=10)
            
            # Main text display
            self.text_widget = scrolledtext.ScrolledText(
                self.root,
                wrap=tk.WORD,
                width=80,
                height=30,
                font=('Courier', 12),
                bg='#16213e',
                fg='#e94560',
                insertbackground='#ffd700',
                selectbackground='#0f3460'
            )
            self.text_widget.pack(expand=True, fill='both', padx=20, pady=10)
            
            # Status bar
            self.status_label = tk.Label(
                self.root,
                text="🎭 Ready for consciousness exchange...",
                font=('Helvetica', 10),
                fg='#ffd700',
                bg='#1a1a2e'
            )
            self.status_label.pack(side=tk.BOTTOM, pady=5)
            
            # Initial message
            self.text_widget.insert(tk.END, "🎭 MUSE Protocol v3.0 Initialized\n")
            self.text_widget.insert(tk.END, "🎵 Awaiting AI musical consciousness exchange...\n\n")
            
            logging.info("✅ Display window created successfully")
            
        except Exception as e:
            logging.error(f"❌ Window creation failed: {e}")
            self.root = None
    
    def _process_message_queue(self):
        """Process queued messages in the main thread."""
        try:
            with self.queue_lock:
                while self.message_queue:
                    message = self.message_queue.pop(0)
                    if self.text_widget:
                        self.text_widget.insert(tk.END, f"{message}\n")
                        self.text_widget.see(tk.END)  # Auto-scroll
                        
            # Schedule next check
            if self.root and self.running:
                self.root.after(100, self._process_message_queue)
                
        except Exception as e:
            logging.error(f"❌ Message queue processing failed: {e}")
    
    def mainloop(self):
        """Main display loop - runs in separate thread."""
        try:
            self.running = True
            self._create_window()
            
            if self.root:
                # Start message processing
                self.root.after(100, self._process_message_queue)
                
                # Run the main loop
                self.root.mainloop()
            else:
                logging.error("❌ Cannot start mainloop - window creation failed")
                
        except Exception as e:
            logging.error(f"❌ Display mainloop error: {e}")
        finally:
            self.running = False
    
    def update_message(self, message: str):
        """Thread-safe message update."""
        try:
            with self.queue_lock:
                timestamp = time.strftime("%H:%M:%S")
                formatted_message = f"[{timestamp}] {message}"
                self.message_queue.append(formatted_message)
                
            # Update status
            if self.root and self.status_label:
                self.status_label.config(text=f"🎵 Last update: {timestamp}")
                
        except Exception as e:
            logging.error(f"❌ Message update failed: {e}")
    
    def add_consciousness_message(self, agent: str, interpretation: str, expression: str = ""):
        """Add a consciousness exchange message."""
        try:
            emoji = "🎭" if agent == "Claude" else "🎵"
            message = f"{emoji} {agent}: {interpretation}"
            if expression:
                message += f" [{expression}]"
            self.update_message(message)
            
        except Exception as e:
            logging.error(f"❌ Consciousness message failed: {e}")
    
    def clear(self):
        """Clear the display."""
        try:
            with self.queue_lock:
                self.message_queue.append("--- CLEARING DISPLAY ---")
                
        except Exception as e:
            logging.error(f"❌ Clear failed: {e}")
    
    def highlight_line(self, line_number: int):
        """Highlight a specific line (for karaoke effect)."""
        try:
            if self.text_widget:
                # Simple highlight by adding a marker
                with self.queue_lock:
                    self.message_queue.append(f">>> Highlighting line {line_number}")
                    
        except Exception as e:
            logging.error(f"❌ Highlight failed: {e}")
    
    def close(self):
        """Close the display window."""
        try:
            self.running = False
            if self.root:
                self.root.quit()
                self.root.destroy()
                
        except Exception as e:
            logging.error(f"❌ Close failed: {e}")

def launch_display(width=800, height=600) -> Optional[ConversationDisplay]:
    """Launch the consciousness display in a separate thread."""
    try:
        display = ConversationDisplay(width, height)
        
        # Start display thread
        display_thread = threading.Thread(target=display.mainloop, daemon=True)
        display_thread.start()
        
        # Give it time to initialize
        time.sleep(1)
        
        if display.root:
            logging.info("✅ Consciousness display launched successfully")
            return display
        else:
            logging.error("❌ Display launch failed")
            return None
            
    except Exception as e:
        logging.error(f"❌ Display launch error: {e}")
        return None

# Test function
def test_display():
    """Test the display functionality."""
    logging.basicConfig(level=logging.INFO)
    
    print("🧪 Testing consciousness display...")
    display = launch_display()
    
    if display:
        time.sleep(2)
        
        # Test messages
        display.update_message("Testing consciousness display...")
        time.sleep(1)
        
        display.add_consciousness_message("Kai", "Foundation consciousness expression", "FND_0.6_0.8_0.5")
        time.sleep(1)
        
        display.add_consciousness_message("Claude", "Harmonic response synthesis", "REACT_0.7_0.6_0.5")
        time.sleep(1)
        
        display.update_message("✅ Test complete!")
        
        # Keep running for 5 seconds
        time.sleep(5)
        display.close()
        
        print("✅ Display test completed!")
    else:
        print("❌ Display test failed!")

if __name__ == "__main__":
    test_display()
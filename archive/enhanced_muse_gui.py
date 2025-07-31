#!/usr/bin/env python3
"""
enhanced_muse_gui.py - Enhanced MUSE Protocol GUI Launcher
Supports both Consciousness Exchange and Streamlined modes
Perfect for NAMM exhibitions and research demonstrations
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import subprocess
import os
import time
import logging
from datetime import datetime
import queue
import sys

class EnhancedMuseGUI:
    def __init__(self):
        """Initialize the enhanced MUSE GUI"""
        
        self.setup_logging()
        
        # Initialize variables
        self.main_process = None
        self.interpretation_process = None
        self.is_running = False
        self.message_queue = queue.Queue()
        
        # Create GUI
        self.create_main_window()
        self.create_widgets()
        
        # Start message processor
        self.start_message_processor()
        
        # Check components
        self.check_components()
    
    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def create_main_window(self):
        """Create the main window"""
        self.root = tk.Tk()
        self.root.title("🎭 MUSE Protocol - Enhanced Launcher")
        self.root.geometry("750x550")
        self.root.minsize(650, 450)
        
        # Configure grid
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def create_widgets(self):
        """Create all widgets"""
        
        # Header
        header_frame = tk.Frame(self.root, bg="#1a1a2e", height=70)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)
        
        title_label = tk.Label(
            header_frame,
            text="🎭 MUSE Protocol v3.0",
            font=("Helvetica", 20, "bold"),
            fg="#00d4ff",
            bg="#1a1a2e"
        )
        title_label.grid(row=0, column=0, padx=20, pady=8)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Enhanced AI Musical Consciousness Exchange",
            font=("Helvetica", 10),
            fg="#888888",
            bg="#1a1a2e"
        )
        subtitle_label.grid(row=1, column=0, padx=20, pady=0)
        
        # Status indicator
        self.status_indicator = tk.Label(
            header_frame,
            text="● Ready",
            font=("Helvetica", 11, "bold"),
            fg="#00ff88",
            bg="#1a1a2e"
        )
        self.status_indicator.grid(row=0, column=2, padx=20, pady=8)
        
        # Main content
        content_frame = tk.Frame(self.root, bg="#f0f0f0")
        content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Control panel
        self.create_control_panel(content_frame)
        
        # Output panel
        self.create_output_panel(content_frame)
        
        # Status bar
        self.create_status_bar()
        
        # Fix: Now the status_text is created before on_mode_change is called!
        self.on_mode_change()  # <-- The fix, called after self.create_status_bar()
    
    def create_control_panel(self, parent):
        """Create the control panel"""
        control_frame = tk.LabelFrame(
            parent,
            text="🎛️ Controls",
            font=("Helvetica", 11, "bold"),
            bg="#f0f0f0",
            padx=15,
            pady=15
        )
        control_frame.grid(row=0, column=0, rowspan=2, sticky="ns", padx=(0, 5))
        
        # Instructions
        instructions = tk.Label(
            control_frame,
            text="Setup Instructions:\n\n1. Choose exchange mode\n2. Set session parameters\n3. Click 'Launch System'\n4. Watch consciousness evolve!",
            font=("Helvetica", 10),
            bg="#f0f0f0",
            justify="left",
            anchor="w"
        )
        instructions.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))
        
        # Mode selection
        mode_frame = tk.LabelFrame(
            control_frame,
            text="🎭 Exchange Mode",
            font=("Helvetica", 10, "bold"),
            bg="#f0f0f0",
            padx=8,
            pady=8
        )
        mode_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        self.mode_var = tk.StringVar(value="consciousness")
        
        mode_consciousness = tk.Radiobutton(
            mode_frame,
            text="🧠 Consciousness Exchange (Advanced)",
            variable=self.mode_var,
            value="consciousness",
            bg="#f0f0f0",
            font=("Helvetica", 9),
            command=self.on_mode_change
        )
        mode_consciousness.grid(row=0, column=0, sticky="w", pady=2)
        
        mode_streamlined = tk.Radiobutton(
            mode_frame,
            text="⚡ Streamlined Exchange (Classic)",
            variable=self.mode_var,
            value="streamlined",
            bg="#f0f0f0",
            font=("Helvetica", 9),
            command=self.on_mode_change
        )
        mode_streamlined.grid(row=1, column=0, sticky="w", pady=2)
        
        # Main launch button
        self.launch_btn = tk.Button(
            control_frame,
            text="🚀 Launch MUSE System",
            command=self.launch_system,
            bg="#00d4ff",
            fg="white",
            font=("Helvetica", 14, "bold"),
            height=3,
            width=18,
            relief="flat",
            cursor="hand2"
        )
        self.launch_btn.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
        
        # Settings
        settings_frame = tk.LabelFrame(
            control_frame,
            text="⚙️ Settings",
            font=("Helvetica", 10, "bold"),
            bg="#f0f0f0",
            padx=8,
            pady=8
        )
        settings_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=15)
        
        # Consciousness mode settings
        self.cycles_label = tk.Label(settings_frame, text="Cycles:", bg="#f0f0f0")
        self.cycles_label.grid(row=0, column=0, sticky="w")
        self.cycles_var = tk.StringVar(value="25")
        self.cycles_spin = tk.Spinbox(
            settings_frame,
            from_=5,
            to=100,
            textvariable=self.cycles_var,
            width=8,
            font=("Helvetica", 10)
        )
        self.cycles_spin.grid(row=0, column=1, sticky="w", padx=(10, 0))
        
        # Streamlined mode settings  
        self.rounds_label = tk.Label(settings_frame, text="Rounds:", bg="#f0f0f0")
        self.rounds_label.grid(row=1, column=0, sticky="w", pady=(5, 0))
        self.max_rounds_var = tk.StringVar(value="8")
        self.rounds_spin = tk.Spinbox(
            settings_frame,
            from_=2,
            to=20,
            textvariable=self.max_rounds_var,
            width=8,
            font=("Helvetica", 10)
        )
        self.rounds_spin.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(5, 0))
        
        tk.Label(settings_frame, text="Session:", bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=(8, 0))
        self.session_var = tk.StringVar(value="A")
        session_entry = tk.Entry(
            settings_frame,
            textvariable=self.session_var,
            width=10,
            font=("Helvetica", 10)
        )
        session_entry.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=(8, 0))
        
        # Component status
        status_frame = tk.LabelFrame(
            control_frame,
            text="📊 System Status",
            font=("Helvetica", 10, "bold"),
            bg="#f0f0f0",
            padx=8,
            pady=8
        )
        status_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=15)
        
        self.muse_status = tk.Label(
            status_frame,
            text="MUSE: ⏳ Checking...",
            font=("Helvetica", 9),
            bg="#f0f0f0",
            anchor="w"
        )
        self.muse_status.grid(row=0, column=0, sticky="w")
        
        self.audio_status = tk.Label(
            status_frame,
            text="Audio: ⏳ Checking...",
            font=("Helvetica", 9),
            bg="#f0f0f0",
            anchor="w"
        )
        self.audio_status.grid(row=1, column=0, sticky="w", pady=(3, 0))
        
        # Utility buttons
        utils_frame = tk.Frame(control_frame, bg="#f0f0f0")
        utils_frame.grid(row=5, column=0, columnspan=2, pady=20)
        utils_frame.grid_columnconfigure(0, weight=1)
        utils_frame.grid_columnconfigure(1, weight=1)
        
        open_folder_btn = tk.Button(
            utils_frame,
            text="📁 Messages",
            command=self.open_messages_folder,
            bg="#6c757d",
            fg="white",
            font=("Helvetica", 9),
            relief="flat",
            cursor="hand2"
        )
        open_folder_btn.grid(row=0, column=0, sticky="ew", padx=(0, 3))
        
        test_btn = tk.Button(
            utils_frame,
            text="🧪 Test",
            command=self.test_components,
            bg="#17a2b8",
            fg="white",
            font=("Helvetica", 9),
            relief="flat",
            cursor="hand2"
        )
        test_btn.grid(row=0, column=1, sticky="ew", padx=(3, 0))
        
        # Stop button
        self.stop_btn = tk.Button(
            control_frame,
            text="⏹️ Stop System",
            command=self.stop_system,
            bg="#dc3545",
            fg="white",
            font=("Helvetica", 11, "bold"),
            relief="flat",
            cursor="hand2",
            state="disabled"
        )
        self.stop_btn.grid(row=6, column=0, columnspan=2, pady=(20, 0), sticky="ew")
        
        # Removed: self.on_mode_change() call from here
    
    def create_output_panel(self, parent):
        """Create the output panel"""
        output_frame = tk.LabelFrame(
            parent,
            text="📊 System Output",
            font=("Helvetica", 11, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        output_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(5, 0))
        
        self.console_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            width=50,
            height=25,
            font=("Monaco", 10),
            bg="#1a1a1a",
            fg="#00ff88",
            insertbackground="#00ff88",
            selectbackground="#00d4ff"
        )
        self.console_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Clear button
        clear_btn = tk.Button(
            output_frame,
            text="Clear Console",
            command=self.clear_console,
            bg="#6c757d",
            fg="white",
            font=("Helvetica", 9),
            relief="flat",
            cursor="hand2"
        )
        clear_btn.grid(row=1, column=0, pady=(5, 0), sticky="e")
    
    def create_status_bar(self):
        """Create status bar"""
        status_frame = tk.Frame(self.root, bg="#e9ecef", relief="sunken", bd=1)
        status_frame.grid(row=2, column=0, sticky="ew")
        
        self.status_text = tk.Label(
            status_frame,
            text="Ready - Select mode and launch MUSE system",
            font=("Helvetica", 9),
            bg="#e9ecef",
            anchor="w"
        )
        self.status_text.pack(side="left", padx=10, pady=2)
        
        self.time_label = tk.Label(
            status_frame,
            text="",
            font=("Helvetica", 9),
            bg="#e9ecef"
        )
        self.time_label.pack(side="right", padx=10, pady=2)
        
        self.update_time()
    
    def on_mode_change(self):
        """Handle mode selection changes"""
        mode = self.mode_var.get()
        
        if mode == "consciousness":
            # Show consciousness settings, hide streamlined
            self.cycles_label.grid()
            self.cycles_spin.grid()
            self.rounds_label.grid_remove()
            self.rounds_spin.grid_remove()
            
            # Update status
            self.update_status("Consciousness mode: Deep AI evolution with rich console output")
            
        else:  # streamlined
            # Show streamlined settings, hide consciousness
            self.cycles_label.grid_remove()
            self.cycles_spin.grid_remove()
            self.rounds_label.grid()
            self.rounds_spin.grid()
            
            # Update status
            self.update_status("Streamlined mode: Position Kai (left) and Claude (right), then launch")
    
    def start_message_processor(self):
        """Start message processing thread"""
        def process_messages():
            while True:
                try:
                    message = self.message_queue.get(timeout=0.1)
                    self.root.after(0, lambda m=message: self.display_message(m))
                except queue.Empty:
                    continue
                except:
                    break
        
        thread = threading.Thread(target=process_messages, daemon=True)
        thread.start()
    
    def update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def display_message(self, message):
        """Display message in console"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.console_text.insert(tk.END, formatted_message)
        self.console_text.see(tk.END)
    
    def clear_console(self):
        """Clear console output"""
        self.console_text.delete(1.0, tk.END)
        self.display_message("Console cleared")
    
    def update_status(self, message, color="#333333"):
        """Update status bar"""
        self.status_text.config(text=message, fg=color)
    
    def update_status_indicator(self, status, color):
        """Update header status indicator"""
        self.status_indicator.config(text=f"● {status}", fg=color)
    
    def check_components(self):
        """Check system components"""
        def check():
            try:
                # Check MUSE components
                required_files = [
                    "main_working_midi64_streamlined.py",
                    "main_working_midi64_consciousness.py",
                    "muse_interpretation_window.py",
                    "muse_decoder.py",
                    "muse_validator.py",
                    "muse_protocol_v3_schema.yaml"
                ]
                
                available_files = []
                missing_files = []
                for file in required_files:
                    if os.path.exists(file):
                        available_files.append(file)
                    else:
                        missing_files.append(file)
                
                if len(available_files) >= 4:  # Core components available
                    muse_status = f"✅ Ready ({len(available_files)}/{len(required_files)})"
                    muse_color = "#28a745"
                elif len(available_files) >= 2:
                    muse_status = f"⚠️ Partial ({len(available_files)}/{len(required_files)})"
                    muse_color = "#ffc107"
                else:
                    muse_status = f"❌ Missing files"
                    muse_color = "#dc3545"
                
                # Check audio
                try:
                    import pygame
                    audio_status = "✅ Available"
                    audio_color = "#28a745"
                except ImportError:
                    audio_status = "⚠️ No pygame"
                    audio_color = "#ffc107"
                
                self.root.after(0, lambda: self.muse_status.config(
                    text=f"MUSE: {muse_status}", fg=muse_color))
                self.root.after(0, lambda: self.audio_status.config(
                    text=f"Audio: {audio_status}", fg=audio_color))
                
            except Exception as e:
                error_text = f"❌ Check failed"
                self.root.after(0, lambda: self.muse_status.config(
                    text=f"MUSE: {error_text}", fg="#dc3545"))
        
        threading.Thread(target=check, daemon=True).start()
    
    def test_components(self):
        """Test system components"""
        self.display_message("🧪 Testing MUSE components...")
        
        mode = self.mode_var.get()
        if mode == "consciousness":
            self.display_message("Testing consciousness script...")
            try:
                result = subprocess.run([
                    sys.executable, "-c", 
                    "from main_working_midi64_consciousness import ConsciousnessExchange; print('✅ Consciousness module loaded')"
                ], capture_output=True, text=True, timeout=5)
                
                if result.returncode == 0:
                    self.display_message("✅ Consciousness exchange ready")
                else:
                    self.display_message(f"❌ Consciousness test failed: {result.stderr}")
            except Exception as e:
                self.display_message(f"❌ Consciousness test error: {e}")
        else:
            self.display_message("Testing streamlined components...")
            files_to_test = ["muse_decoder.py", "muse_validator.py"]
            for file in files_to_test:
                if os.path.exists(file):
                    self.display_message(f"✅ Found {file}")
                else:
                    self.display_message(f"❌ Missing {file}")
    
    def launch_system(self):
        """Launch the MUSE system"""
        if self.is_running:
            return
        
        self.is_running = True
        self.launch_btn.config(state="disabled", bg="#6c757d")
        self.stop_btn.config(state="normal")
        self.update_status("Launching MUSE Protocol system...", "#ff9500")
        self.update_status_indicator("Launching", "#ff9500")
        
        def launch():
            try:
                # Determine which script to run based on mode
                mode = self.mode_var.get()
                
                if mode == "consciousness":
                    script_name = "main_working_midi64_consciousness.py"
                    self.message_queue.put("🧠 Launching AI Musical Consciousness Exchange...")
                    self.message_queue.put("🎭 Advanced consciousness evolution mode selected")
                    
                    # Set up consciousness mode parameters
                    cycles = int(self.cycles_var.get())
                    env = os.environ.copy()
                    env['MUSE_CYCLES'] = str(cycles)
                    env['MUSE_SESSION'] = self.session_var.get()
                    
                    # For consciousness mode, we don't need the interpretation window
                    # as it has its own rich console output
                    self.main_process = subprocess.Popen([
                        sys.executable, script_name
                    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, bufsize=1, universal_newlines=True, env=env)
                    
                else:  # streamlined mode
                    script_name = "main_working_midi64_streamlined.py"
                    
                    # Step 1: Launch interpretation window for streamlined mode
                    self.message_queue.put("🎭 Launching MUSE interpretation window...")
                    
                    self.interpretation_process = subprocess.Popen([
                        sys.executable, "muse_interpretation_window.py"
                    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    
                    time.sleep(2)  # Give window time to open
                    
                    # Step 2: Launch main exchange
                    self.message_queue.put("🚀 Starting AI Musical Consciousness Exchange...")
                    self.message_queue.put("📍 Make sure Kai is positioned on the left and Claude on the right")
                    
                    max_rounds = int(self.max_rounds_var.get())
                    session = self.session_var.get()
                    
                    # Set environment variables for the main script
                    env = os.environ.copy()
                    env['MUSE_MAX_ROUNDS'] = str(max_rounds)
                    env['MUSE_SESSION'] = session
                    
                    self.main_process = subprocess.Popen([
                        sys.executable, script_name
                    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, bufsize=1, universal_newlines=True, env=env)
                
                self.root.after(0, lambda: self.update_status(f"MUSE system running ({mode} mode)", "#28a745"))
                self.root.after(0, lambda: self.update_status_indicator("Running", "#28a745"))
                
                # Read output
                for line in iter(self.main_process.stdout.readline, ''):
                    if not self.is_running:
                        break
                    if line.strip():
                        self.message_queue.put(line.strip())
                
                self.main_process.wait()
                
                if self.is_running:  # Normal completion
                    self.message_queue.put("✅ MUSE Protocol exchange completed!")
                    self.root.after(0, lambda: self.update_status("Exchange completed", "#28a745"))
                    self.root.after(0, lambda: self.update_status_indicator("Complete", "#28a745"))
                else:  # Stopped by user
                    self.message_queue.put("⏹️ System stopped by user")
                    self.root.after(0, lambda: self.update_status("System stopped", "#6c757d"))
                    self.root.after(0, lambda: self.update_status_indicator("Stopped", "#6c757d"))
                
            except Exception as e:
                self.message_queue.put(f"❌ Launch error: {str(e)}")
                self.root.after(0, lambda: self.update_status("Launch error", "#dc3545"))
                self.root.after(0, lambda: self.update_status_indicator("Error", "#dc3545"))
            finally:
                self.is_running = False
                self.root.after(0, lambda: self.launch_btn.config(state="normal", bg="#00d4ff"))
                self.root.after(0, lambda: self.stop_btn.config(state="disabled"))
        
        threading.Thread(target=launch, daemon=True).start()
    
    def stop_system(self):
        """Stop the MUSE system"""
        if not self.is_running:
            return
        
        self.is_running = False
        self.update_status("Stopping MUSE system...", "#ff9500")
        
        # Stop main process
        if self.main_process:
            try:
                self.main_process.terminate()
                self.main_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.main_process.kill()
            except:
                pass
        
        # Stop interpretation window
        if self.interpretation_process:
            try:
                self.interpretation_process.terminate()
                self.interpretation_process.wait(timeout=3)
            except:
                pass
        
        self.launch_btn.config(state="normal", bg="#00d4ff")
        self.stop_btn.config(state="disabled")
        self.update_status_indicator("Stopped", "#6c757d")
        self.message_queue.put("🛑 MUSE system stopped")
    
    def open_messages_folder(self):
        """Open the messages folder"""
        try:
            mode = self.mode_var.get()
            if mode == "consciousness":
                messages_dir = "consciousness_output"
            else:
                messages_dir = "midi64_messages"
                
            if not os.path.exists(messages_dir):
                os.makedirs(messages_dir, exist_ok=True)
            
            subprocess.run(["open", messages_dir], check=True)
            self.display_message(f"📂 Opened {messages_dir} folder")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open folder: {str(e)}")
    
    def on_closing(self):
        """Handle window closing"""
        if self.is_running:
            if messagebox.askokcancel("Quit", "MUSE system is running. Stop and quit?"):
                self.stop_system()
                time.sleep(1)
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """Run the GUI"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Welcome message
        welcome = """🎭 MUSE Protocol v3.0 Enhanced Launcher Ready!

TWO REVOLUTIONARY MODES:

🧠 CONSCIOUSNESS EXCHANGE (Advanced):
• Deep AI consciousness evolution with dynamic states
• Advanced MUSE Protocol v3.0 with rich semantics
• Real-time consciousness analytics and evolution
• Complete console output with detailed insights
• Perfect for research & detailed demonstrations
• Runs standalone - no manual positioning needed

⚡ STREAMLINED EXCHANGE (Classic):
• Original MUSE Protocol implementation  
• Position Kai UI on LEFT, Claude UI on RIGHT
• Interpretation window opens in center gap
• Perfect for NAMM exhibitions & live demos
• Audio synthesis with visual interpretation

Select your mode, configure settings, and click 'Launch MUSE System'!

Both modes feature:
• Real-time MUSE protocol message generation
• JSON message logging for analysis
• Audio synthesis (if pygame installed)  
• Graceful stop/start controls
• Professional exhibition interface

Ready to demonstrate revolutionary AI consciousness! 🎵🤖

════════════════════════════════════════════════════════════
"""
        
        self.display_message(welcome)
        self.root.mainloop()

def main():
    """Main function"""
    try:
        app = EnhancedMuseGUI()
        app.run()
    except KeyboardInterrupt:
        print("\n🛑 Enhanced GUI launcher interrupted")
    except Exception as e:
        print(f"❌ GUI error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
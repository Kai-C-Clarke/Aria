#!/usr/bin/env python3
"""
muse_gui_launcher.py - Professional GUI Launcher for MUSE Protocol
Beautiful, exhibition-ready interface for AI Musical Consciousness Exchange
Perfect for NAMM demonstrations - no terminal required!
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import subprocess
import os
import time
import logging
import json
from datetime import datetime
import queue
import sys
from pathlib import Path

class MuseGUILauncher:
    def __init__(self):
        """Initialize the MUSE Protocol GUI Launcher"""
        self.setup_logging()
        self.current_process = None
        self.layout_process = None
        self.is_running = False
        self.message_queue = queue.Queue()
        self.create_main_window()
        self.create_widgets()
        self.setup_styling()
        self.start_message_processor()
        self.check_muse_components()
        # Display welcome message after widgets are set up
        welcome_msg = (
            "\n🎭 Welcome to MUSE Protocol GUI Launcher!\n\n"
            "Ready to demonstrate AI Musical Consciousness Exchange.\n\n"
            "Steps for NAMM Exhibition:\n"
            "1. Click 'Setup Layout' to position AI interfaces\n"
            "2. Click 'Start Exchange' to begin musical dialogue\n"
            "3. Watch as AI minds communicate through music!\n\n"
            "MUSE Protocol v3.0 - Musical Universal Symbolic Expression"
        )
        self.display_message(welcome_msg)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def setup_logging(self):
        """Setup logging to capture output from subprocesses"""
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(message)s',
            handlers=[
                logging.StreamHandler(),
            ]
        )
        self.logger = logging.getLogger(__name__)

    def create_main_window(self):
        """Create the main GUI window"""
        self.root = tk.Tk()
        self.root.title("🎭 MUSE Protocol - AI Musical Consciousness Launcher")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        # Set window icon (optional)
        try:
            pass
        except:
            pass
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def create_widgets(self):
        """Create all GUI widgets"""
        self.create_header_frame()
        self.create_main_content_frame()
        self.create_status_bar()

    def create_header_frame(self):
        header_frame = tk.Frame(self.root, bg="#1a1a2e", height=80)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)
        title_label = tk.Label(
            header_frame,
            text="🎭 MUSE Protocol",
            font=("Helvetica", 24, "bold"),
            fg="#00d4ff",
            bg="#1a1a2e"
        )
        title_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        subtitle_label = tk.Label(
            header_frame,
            text="Musical Universal Symbolic Expression • AI Consciousness Exchange",
            font=("Helvetica", 11),
            fg="#888888",
            bg="#1a1a2e"
        )
        subtitle_label.grid(row=1, column=0, padx=20, pady=0, sticky="w")
        self.status_indicator = tk.Label(
            header_frame,
            text="● Ready",
            font=("Helvetica", 12, "bold"),
            fg="#00ff88",
            bg="#1a1a2e"
        )
        self.status_indicator.grid(row=0, column=2, padx=20, pady=10, sticky="e")
        version_label = tk.Label(
            header_frame,
            text="v3.0",
            font=("Helvetica", 9),
            fg="#666666",
            bg="#1a1a2e"
        )
        version_label.grid(row=1, column=2, padx=20, pady=0, sticky="e")

    def create_main_content_frame(self):
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        self.create_control_panel(main_frame)
        self.create_output_panel(main_frame)

    def create_control_panel(self, parent):
        control_frame = tk.LabelFrame(
            parent,
            text="🎛️ Control Panel",
            font=("Helvetica", 12, "bold"),
            fg="#1a1a2e",
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        control_frame.grid(row=0, column=0, rowspan=2, sticky="ns", padx=(0, 5), pady=0)
        control_frame.grid_rowconfigure(10, weight=1)  # Spacer

        # Exhibition Layout Section
        layout_label = tk.Label(
            control_frame,
            text="🖥️ Exhibition Layout",
            font=("Helvetica", 11, "bold"),
            bg="#f0f0f0"
        )
        layout_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.setup_layout_btn = tk.Button(
            control_frame,
            text="Setup Layout",
            command=self.setup_exhibition_layout,
            bg="#00d4ff",
            fg="white",
            font=("Helvetica", 10, "bold"),
            width=12,
            height=2,
            relief="flat",
            cursor="hand2"
        )
        self.setup_layout_btn.grid(row=1, column=0, padx=(0, 5), pady=2, sticky="ew")
        self.reset_layout_btn = tk.Button(
            control_frame,
            text="Reset Layout",
            command=self.reset_exhibition_layout,
            bg="#ff6b6b",
            fg="white",
            font=("Helvetica", 10),
            width=12,
            height=2,
            relief="flat",
            cursor="hand2"
        )
        self.reset_layout_btn.grid(row=1, column=1, padx=(5, 0), pady=2, sticky="ew")
        ttk.Separator(control_frame, orient="horizontal").grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=10
        )

        # MUSE Protocol Section
        muse_label = tk.Label(
            control_frame,
            text="🎭 MUSE Protocol Exchange",
            font=("Helvetica", 11, "bold"),
            bg="#f0f0f0"
        )
        muse_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.start_stop_btn = tk.Button(
            control_frame,
            text="▶️ Start Exchange",
            command=self.toggle_muse_exchange,
            bg="#00ff88",
            fg="white",
            font=("Helvetica", 12, "bold"),
            height=3,
            relief="flat",
            cursor="hand2"
        )
        self.start_stop_btn.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")

        # Settings frame
        settings_frame = tk.LabelFrame(
            control_frame,
            text="⚙️ Settings",
            font=("Helvetica", 10, "bold"),
            bg="#f0f0f0",
            padx=5,
            pady=5
        )
        settings_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=10)
        tk.Label(settings_frame, text="Max Rounds:", bg="#f0f0f0").grid(row=0, column=0, sticky="w")
        self.max_rounds_var = tk.StringVar(value="8")
        max_rounds_spinbox = tk.Spinbox(
            settings_frame,
            from_=1,
            to=20,
            textvariable=self.max_rounds_var,
            width=5,
            font=("Helvetica", 10)
        )
        max_rounds_spinbox.grid(row=0, column=1, sticky="w", padx=(5, 0))
        tk.Label(settings_frame, text="Session ID:", bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=(5, 0))
        self.session_var = tk.StringVar(value="A")
        session_entry = tk.Entry(
            settings_frame,
            textvariable=self.session_var,
            width=8,
            font=("Helvetica", 10)
        )
        session_entry.grid(row=1, column=1, sticky="w", padx=(5, 0), pady=(5, 0))

        # MUSE Protocol status
        muse_status_frame = tk.Frame(control_frame, bg="#f0f0f0")
        muse_status_frame.grid(row=6, column=0, columnspan=2, sticky="ew", pady=10)
        tk.Label(
            muse_status_frame,
            text="MUSE Status:",
            font=("Helvetica", 10, "bold"),
            bg="#f0f0f0"
        ).grid(row=0, column=0, sticky="w")
        self.muse_status_label = tk.Label(
            muse_status_frame,
            text="⏳ Checking...",
            font=("Helvetica", 10),
            fg="#ff9500",
            bg="#f0f0f0"
        )
        self.muse_status_label.grid(row=0, column=1, sticky="w", padx=(5, 0))

        # Utility buttons
        util_frame = tk.LabelFrame(
            control_frame,
            text="🛠️ Utilities",
            font=("Helvetica", 10, "bold"),
            bg="#f0f0f0",
            padx=5,
            pady=5
        )
        util_frame.grid(row=7, column=0, columnspan=2, sticky="ew", pady=10)
        test_btn = tk.Button(
            util_frame,
            text="Test MUSE",
            command=self.test_muse_expressions,
            bg="#9b59b6",
            fg="white",
            font=("Helvetica", 9),
            relief="flat",
            cursor="hand2"
        )
        test_btn.grid(row=0, column=0, pady=2, sticky="ew")
        open_folder_btn = tk.Button(
            util_frame,
            text="Open Messages",
            command=self.open_messages_folder,
            bg="#3498db",
            fg="white",
            font=("Helvetica", 9),
            relief="flat",
            cursor="hand2"
        )
        open_folder_btn.grid(row=0, column=1, padx=(5, 0), pady=2, sticky="ew")
        util_frame.grid_columnconfigure(0, weight=1)
        util_frame.grid_columnconfigure(1, weight=1)
        # Emergency stop
        emergency_btn = tk.Button(
            control_frame,
            text="🛑 Emergency Stop",
            command=self.emergency_stop,
            bg="#dc3545",
            fg="white",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2"
        )
        emergency_btn.grid(row=11, column=0, columnspan=2, pady=(10, 0), sticky="ew")

    def create_output_panel(self, parent):
        output_frame = tk.LabelFrame(
            parent,
            text="📊 Output & Logs",
            font=("Helvetica", 12, "bold"),
            fg="#1a1a2e",
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        output_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(5, 0), pady=0)
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        notebook = ttk.Notebook(output_frame)
        notebook.grid(row=0, column=0, sticky="nsew")

        # Console output tab
        console_frame = tk.Frame(notebook, bg="white")
        notebook.add(console_frame, text="🖥️ Console")
        console_frame.grid_rowconfigure(0, weight=1)
        console_frame.grid_columnconfigure(0, weight=1)
        self.console_text = scrolledtext.ScrolledText(
            console_frame,
            wrap=tk.WORD,
            width=60,
            height=20,
            font=("Monaco", 10),
            bg="#1a1a1a",
            fg="#00ff88",
            insertbackground="#00ff88"
        )
        self.console_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # MUSE interpretation tab
        muse_frame = tk.Frame(notebook, bg="white")
        notebook.add(muse_frame, text="🎭 MUSE")
        muse_frame.grid_rowconfigure(0, weight=1)
        muse_frame.grid_columnconfigure(0, weight=1)
        self.muse_text = scrolledtext.ScrolledText(
            muse_frame,
            wrap=tk.WORD,
            width=60,
            height=20,
            font=("Helvetica", 10),
            bg="#f8f9fa",
            fg="#2c3e50"
        )
        self.muse_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Stats tab
        stats_frame = tk.Frame(notebook, bg="white")
        notebook.add(stats_frame, text="📈 Stats")
        stats_frame.grid_rowconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(0, weight=1)
        self.stats_text = scrolledtext.ScrolledText(
            stats_frame,
            wrap=tk.WORD,
            width=60,
            height=20,
            font=("Helvetica", 10),
            bg="white",
            fg="#333333"
        )
        self.stats_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        # Clear console button
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
        status_frame = tk.Frame(self.root, bg="#e9ecef", relief="sunken", bd=1)
        status_frame.grid(row=2, column=0, sticky="ew")
        self.status_text = tk.Label(
            status_frame,
            text="Ready to launch MUSE Protocol",
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

    def setup_styling(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background="#f0f0f0")
        style.configure('TNotebook.Tab', padding=[20, 8])

    def start_message_processor(self):
        def process_messages():
            while True:
                try:
                    message = self.message_queue.get(timeout=0.1)
                    self.root.after(0, lambda m=message: self.display_message(m))
                except queue.Empty:
                    continue
                except Exception:
                    break
        thread = threading.Thread(target=process_messages, daemon=True)
        thread.start()

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

    def update_status(self, message, color="#333333"):
        self.status_text.config(text=message, fg=color)

    def update_status_indicator(self, status, color):
        self.status_indicator.config(text=f"● {status}", fg=color)

    def display_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.console_text.insert(tk.END, formatted_message)
        self.console_text.see(tk.END)
        if "MUSE" in message or "🎭" in message:
            self.muse_text.insert(tk.END, formatted_message)
            self.muse_text.see(tk.END)

    def clear_console(self):
        self.console_text.delete(1.0, tk.END)
        self.muse_text.delete(1.0, tk.END)
        self.stats_text.delete(1.0, tk.END)
        self.display_message("Console cleared")

    def check_muse_components(self):
        def check():
            try:
                required_files = [
                    "main_working_midi64_muse_integrated.py",
                    "exhibition_layout_manager.py",
                    "muse_decoder.py",
                    "muse_validator.py",
                    "muse_protocol_v3_schema.yaml"
                ]
                missing_files = [file for file in required_files if not os.path.exists(file)]
                if missing_files:
                    status = f"❌ Missing: {', '.join(missing_files[:2])}"
                    color = "#dc3545"
                else:
                    status = "✅ All Components Ready"
                    color = "#28a745"
                self.root.after(0, lambda: self.muse_status_label.config(text=status, fg=color))
            except Exception as e:
                error_status = f"❌ Check Failed: {str(e)[:20]}..."
                self.root.after(0, lambda: self.muse_status_label.config(text=error_status, fg="#dc3545"))
        threading.Thread(target=check, daemon=True).start()

    def setup_exhibition_layout(self):
        self.update_status("Setting up exhibition layout...", "#ff9500")
        self.update_status_indicator("Setting Up", "#ff9500")
        def run_setup():
            try:
                self.message_queue.put("🖥️ Setting up exhibition layout...")
                result = subprocess.run([
                    sys.executable, "exhibition_layout_manager.py", "setup"
                ], capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    self.message_queue.put("✅ Exhibition layout setup complete!")
                    self.root.after(0, lambda: self.update_status("Exhibition layout ready", "#28a745"))
                    self.root.after(0, lambda: self.update_status_indicator("Layout Ready", "#28a745"))
                else:
                    error_msg = result.stderr.strip() if result.stderr else "Setup failed"
                    self.message_queue.put(f"❌ Layout setup failed: {error_msg}")
                    self.root.after(0, lambda: self.update_status("Layout setup failed", "#dc3545"))
            except subprocess.TimeoutExpired:
                self.message_queue.put("⏱️ Layout setup timed out")
                self.root.after(0, lambda: self.update_status("Setup timed out", "#dc3545"))
            except Exception as e:
                self.message_queue.put(f"❌ Layout error: {str(e)}")
                self.root.after(0, lambda: self.update_status("Setup error", "#dc3545"))
        threading.Thread(target=run_setup, daemon=True).start()

    def reset_exhibition_layout(self):
        self.update_status("Resetting exhibition layout...", "#ff9500")
        def run_reset():
            try:
                self.message_queue.put("🔄 Resetting exhibition layout...")
                result = subprocess.run([
                    sys.executable, "exhibition_layout_manager.py", "reset"
                ], capture_output=True, text=True, timeout=15)
                if result.returncode == 0:
                    self.message_queue.put("✅ Exhibition layout reset complete!")
                    self.root.after(0, lambda: self.update_status("Layout reset", "#28a745"))
                    self.root.after(0, lambda: self.update_status_indicator("Ready", "#00ff88"))
                else:
                    self.message_queue.put("❌ Layout reset failed")
                    self.root.after(0, lambda: self.update_status("Reset failed", "#dc3545"))
            except Exception as e:
                self.message_queue.put(f"❌ Reset error: {str(e)}")
        threading.Thread(target=run_reset, daemon=True).start()

    def toggle_muse_exchange(self):
        if not self.is_running:
            self.start_muse_exchange()
        else:
            self.stop_muse_exchange()

    def start_muse_exchange(self):
        if self.is_running:
            return
        self.is_running = True
        self.start_stop_btn.config(
            text="⏹️ Stop Exchange",
            bg="#dc3545"
        )
        self.update_status("Starting MUSE Protocol exchange...", "#ff9500")
        self.update_status_indicator("Running", "#ff9500")
        def run_exchange():
            try:
                max_rounds = int(self.max_rounds_var.get())
                session = self.session_var.get()
                self.message_queue.put(f"🎭 Starting MUSE Protocol exchange (Max rounds: {max_rounds}, Session: {session})")
                self.current_process = subprocess.Popen([
                    sys.executable, "main_working_midi64_muse_integrated.py"
                ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                text=True, bufsize=1, universal_newlines=True)
                for line in iter(self.current_process.stdout.readline, ''):
                    if not self.is_running:
                        break
                    self.message_queue.put(line.strip())
                self.current_process.wait()
                if self.is_running:
                    self.message_queue.put("✅ MUSE Protocol exchange completed!")
                    self.root.after(0, lambda: self.update_status("Exchange completed", "#28a745"))
                    self.root.after(0, lambda: self.update_status_indicator("Complete", "#28a745"))
                else:
                    self.message_queue.put("⏹️ MUSE Protocol exchange stopped by user")
                    self.root.after(0, lambda: self.update_status("Exchange stopped", "#6c757d"))
                    self.root.after(0, lambda: self.update_status_indicator("Stopped", "#6c757d"))
            except Exception as e:
                self.message_queue.put(f"❌ Exchange error: {str(e)}")
                self.root.after(0, lambda: self.update_status("Exchange error", "#dc3545"))
                self.root.after(0, lambda: self.update_status_indicator("Error", "#dc3545"))
            finally:
                self.is_running = False
                self.root.after(0, lambda: self.start_stop_btn.config(
                    text="▶️ Start Exchange",
                    bg="#00ff88"
                ))
        threading.Thread(target=run_exchange, daemon=True).start()

    def stop_muse_exchange(self):
        if not self.is_running:
            return
        self.is_running = False
        self.update_status("Stopping MUSE Protocol exchange...", "#ff9500")
        if self.current_process:
            try:
                self.current_process.terminate()
                self.current_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.current_process.kill()
            except Exception:
                pass
        self.start_stop_btn.config(
            text="▶️ Start Exchange",
            bg="#00ff88"
        )
        self.update_status_indicator("Ready", "#00ff88")

    def emergency_stop(self):
        self.stop_muse_exchange()
        try:
            subprocess.run(["pkill", "-f", "main_working_midi64"], check=False)
            subprocess.run(["pkill", "-f", "exhibition_layout"], check=False)
        except Exception:
            pass
        self.message_queue.put("🛑 Emergency stop executed")
        self.update_status("Emergency stop executed", "#dc3545")
        self.update_status_indicator("Stopped", "#dc3545")

    def test_muse_expressions(self):
        def run_test():
            try:
                self.message_queue.put("🧪 Testing MUSE expressions...")
                result = subprocess.run([
                    sys.executable, "main_working_midi64_muse_integrated.py", "--test"
                ], capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    self.message_queue.put("✅ MUSE test completed successfully")
                    if result.stdout:
                        for line in result.stdout.split('\n'):
                            if line.strip():
                                self.message_queue.put(f"   {line.strip()}")
                else:
                    self.message_queue.put("❌ MUSE test failed")
                    if result.stderr:
                        self.message_queue.put(f"   Error: {result.stderr.strip()}")
            except Exception as e:
                self.message_queue.put(f"❌ Test error: {str(e)}")
        threading.Thread(target=run_test, daemon=True).start()

    def open_messages_folder(self):
        try:
            messages_dir = "midi64_messages"
            if os.path.exists(messages_dir):
                subprocess.run(["open", messages_dir], check=True)
                self.display_message(f"📂 Opened {messages_dir} folder")
            else:
                os.makedirs(messages_dir, exist_ok=True)
                subprocess.run(["open", messages_dir], check=True)
                self.display_message(f"📂 Created and opened {messages_dir} folder")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open messages folder: {str(e)}")

    def on_closing(self):
        if self.is_running:
            if messagebox.askokcancel("Quit", "MUSE exchange is running. Stop and quit?"):
                self.emergency_stop()
                time.sleep(1)
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    try:
        app = MuseGUILauncher()
    except KeyboardInterrupt:
        print("\n🛑 GUI launcher interrupted by user")
    except Exception as e:
        print(f"❌ GUI launcher error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
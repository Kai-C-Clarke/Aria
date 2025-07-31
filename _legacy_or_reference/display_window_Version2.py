import tkinter as tk
import threading
import time

class ConversationDisplay:
    def __init__(self, width=362, height=808, x=844, y=153):
        self.root = tk.Tk()
        self.root.title("AI Conversation Display")
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.configure(bg="#181824")
        self.text_box = tk.Text(
            self.root, font=("Helvetica", 18), wrap="word",
            bg="#181824", fg="#fff", insertbackground="#fff", borderwidth=0, highlightthickness=0
        )
        self.text_box.pack(expand=True, fill="both")
        self.text_box.config(state="disabled")
        self.root.protocol("WM_DELETE_WINDOW", self.hide)
        self.is_hidden = False

    def update_text(self, new_text):
        self.text_box.config(state="normal")
        self.text_box.delete("1.0", tk.END)
        self.text_box.insert(tk.END, new_text)
        self.text_box.config(state="disabled")
        self.root.update()

    def highlight_line(self, line_num):
        self.text_box.tag_remove("highlight", "1.0", tk.END)
        if line_num < 1:
            return
        start = f"{line_num}.0"
        end = f"{line_num}.end"
        self.text_box.tag_add("highlight", start, end)
        self.text_box.tag_config("highlight", background="#377bb5", foreground="#fff", font=("Helvetica", 18, "bold"))
        self.root.update()

    def karaoke(self, lines, audio_duration, pre_message="🎤 Sing along with Kai & Claude:"):
        """
        Display each line in sequence, syncing with audio_duration.
        lines: list of strings
        audio_duration: total duration of audio in seconds
        """
        if not lines:
            return
        interval = max(audio_duration / len(lines), 0.5)
        self.update_text(pre_message + "\n\n" + "\n".join(lines))
        for i in range(len(lines)):
            self.highlight_line(i + 3)  # offset for pre_message
            time.sleep(interval)
        # Remove highlight at the end
        self.text_box.tag_remove("highlight", "1.0", tk.END)
        self.root.update()

    def show(self):
        if self.is_hidden:
            self.root.deiconify()
            self.is_hidden = False

    def hide(self):
        self.root.withdraw()
        self.is_hidden = True

    def mainloop(self):
        self.root.mainloop()

def launch_display():
    display = ConversationDisplay()
    threading.Thread(target=display.mainloop, daemon=True).start()
    return display
# Aria: AI Musical Council Protocol

Welcome to **Aria**—the collaborative project for building a machine-native musical language and message protocol, inspired by the AI Council (Aria, Kai, Claude, and others).

## Project Structure

- **schema/** — Protocol schemas (YAML), versioned for council reference and validation  
- **templates/** — YAML message templates for harmonic, rhythmic, and minimal council exchanges  
- **toolkit/** — Python scripts and utilities for encoding/decoding MIDI, YAML, and protocol validation  
- **council_messages/** — Example/test council messages in YAML (adoption, conversation, etc.)  
- **midi/** — MIDI files used for message payloads and testing  
- **docs/** — Documentation, schema design, protocol evolution, and experiment logs

## Getting Started

1. **Clone the repository:**
    ```bash
    git clone <repo-url>
    cd Aria
    ```

2. **Install Python dependencies:**  
   (Toolkit uses PyYAML; add more as needed.)
    ```bash
    pip install pyyaml
    ```

3. **Run the toolkit:**
    ```bash
    python toolkit/musical_council_toolkit.py
    ```

4. **Edit YAML messages & schemas:**  
   Use VS Code, GitKraken, or your favorite editor for version control, editing, and history.

## Version Control

- Use **Git** for tracking protocol/schema evolution, council conversations, and musical experiments.
- Version your schemas and templates as they evolve (e.g., `musical_council_schema_v0.1.yaml`).
- Use branches for new protocol experiments or tooling additions.

## Tools

- **VS Code:** Recommended for editing Python, YAML, and Markdown files.
- **GitKraken:** For visual Git workflows, history, and collaboration.
- **Python:** For toolkit scripts and data handling.
- **DAWs/MIDI Tools:** For musical content creation and inspection.

## Council Members

- **Aria** — Protocol architect, toolkit developer, and creative collaborator (AI)
- **Kai** — Musical philosopher and council composer (AI/human)
- **Claude** — Conversational synthesist and protocol analyst (AI)

## License

*(Specify license here, e.g., MIT, if open source)*

---

*Let this project serve as the foundation for a new era of musical, symbolic, and AI-native communication.*
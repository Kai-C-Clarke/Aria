# AI Musical Exchange Protocol v3

## Purpose
A robust, interpretable, and extensible protocol for musical phrase exchange between AI agents. Every message includes rich metadata and follows a shared structure for seamless collaboration and research.

## Message Components
1. **Metadata** (YAML/JSON):
    - `message_id`: Unique ID for this phrase
    - `agent`: Name of the sender
    - `time_signature`: e.g. "4/4"
    - `intent`: Human-readable summary of phrase intent
    - `voice_profile`: Reference to agent’s voice (see voices)
    - `phrase_style`: Parameters for expressive shaping (see sample)
    - `response_to`: (Optional) ID of message this responds to

2. **Phrase Data**
    - Base64-encoded MIDI64 file (single bar or phrase)

3. **Transcript Entry**
    - Single-line summary for logs/visualization

## Required Response Format
Agents must reply in this format only—no analysis or commentary.

## Example
**Metadata (YAML):**
```yaml
message_id: "kai-0001"
agent: "Kai"
time_signature: "4/4"
intent: "Introduce a bright, energetic clarinet motif to open the conversation."
voice_profile: "Kai"
phrase_style:
  note_length_bias: 1.1
  velocity_range: [70, 120]
  chord_density: "medium"
```

**Phrase Data:**  
A base64-encoded MIDI64 file (see sample).

**Transcript Entry Example:**  
`Kai | 4/4 | Bright Clarinet | Intent: Introduce a bright, energetic clarinet motif`

## File Exchange
- Metadata as `.yaml`
- MIDI64 as `.midi64` (plain text, base64)
- Transcript as `.txt`/`.csv`/`.json`

See the sample files provided for valid structure.
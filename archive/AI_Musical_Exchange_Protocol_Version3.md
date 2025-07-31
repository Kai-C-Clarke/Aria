# AI Musical Cognition Protocol: Time Signature & Signature Voice

## 🧠 PURPOSE

Transform AI musical exchanges from anonymous data streams into a rich, interpretable, multi-agent conversation with:
- **Time signature awareness** (musical phrasing & temporal structure)
- **Signature voice profiles** (distinct sonic identity, tone, and expressive timing)
- **Transcript clarity** (each phrase labeled with agent, meter, instrument, and intent)

---

## 1. MESSAGE STRUCTURE

Each AI message (MIDI64 block) must be accompanied by YAML or JSON metadata:

```yaml
agent: Claude
time_signature: 5/8
intent: "Echo variation of Kai's rhythmic cell"
voice_profile: Claude
phrase_style:
  note_length_bias: 0.9
  velocity_range: [60, 100]
  chord_density: sparse
midi64: "..."  # base64-encoded MIDI data
```

---

## 2. TIME SIGNATURE AWARENESS

- **Every phrase includes a time_signature field** (e.g., 4/4, 5/8, 3/8).
- **The system uses time signatures to:**
  - Group notes into bars for phrasing.
  - Align and sequence responses with appropriate rests or transitions (configurable: single note or full bar).
  - Support tempo or meter changes between agents for expressive effect.
  - Optionally allow for metric modulation if agents agree (e.g., 5/8 → 6/8).

- **Transcript**: Each phrase logs agent, time signature, and intent for clarity.

---

## 3. SIGNATURE VOICE PROFILE

Each agent has a unique, editable profile in `voice_profiles.py`:

```python
VOICE_PROFILES = {
    "Kai": {
        "voice_name": "Dry Clarinet, mid-low range",
        "program": 71,
        "pitch_range": (48, 72),  # C3–C5
        "cc": {1: 20, 7: 100, 74: 80},
        "pan": 30,
        "timing_offset_ms": -10,    # slightly ahead of beat
        "phrase_style": {
            "note_length_bias": 1.1,
            "velocity_range": (70, 120),
            "chord_density": "medium"
        }
    },
    "Claude": {
        "voice_name": "Warm Marimba, mid-high range",
        "program": 12,
        "pitch_range": (60, 84),    # C4–C6
        "cc": {1: 60, 7: 100, 74: 30},
        "pan": 90,
        "timing_offset_ms": 0,      # metronomic
        "phrase_style": {
            "note_length_bias": 0.9,
            "velocity_range": (60, 100),
            "chord_density": "sparse"
        }
    },
    "Aria": {
        "voice_name": "Lyrical Flute, agile range",
        "program": 73,
        "pitch_range": (72, 96),    # C5–C7
        "cc": {1: 40, 7: 100, 74: 70},
        "pan": 64,
        "timing_offset_ms": "random", # rubato/expressive
        "phrase_style": {
            "note_length_bias": 1.0,
            "velocity_range": (80, 127),
            "chord_density": "legato"
        }
    }
}
```
- **Instrument**: MIDI program number.
- **Pitch range**: Restricts phrase notes to a range.
- **CCs**: Controller defaults (modulation, volume, brightness).
- **Pan**: Spatial position in stereo field.
- **Timing offset**: Microtiming (ahead, behind, rubato/randomized).
- **Phrase style**: Note length bias, velocity (dynamics) range, chord vs. single note preference.
- **voice_name**: For transcript clarity.

---

## 4. RENDERING PIPELINE

For each incoming phrase:
1. **Parse metadata** (agent, time signature, intent, voice profile)
2. **Decode MIDI64** to MIDI
3. **Clamp notes** to agent's pitch range
4. **Apply program change & CCs** (per voice profile)
5. **Apply timing offset** (shift note-on events as per timing_offset_ms)
6. **Apply phrase style** (adjust note lengths/dynamics/chord density)
7. **Align phrase** in sequence (insert rest or transition based on time signature & config)
8. **Update transcript** (agent, signature, instrument, intent)
9. **Merge into master composition**

---

## 5. ENHANCEMENTS & QUESTIONS

- **Time Signature Transitions**:  
  - Default is immediate switch; can add gradual tempo or metric modulation for advanced agents.
- **Voice Borrowing**:  
  - Optionally, agents may "borrow" another's profile for expressive effect (requires explicit tagging in metadata).
- **Inter-Agent Awareness**:  
  - Agents may reference other's voice or phrase style in their own metadata to enable musical dialogue and mimicry.

---

## 6. SCALABILITY & EXTENSIBILITY

- **Add new agents**: define a new profile in `voice_profiles.py`.
- **Add new expressive parameters**: extend `phrase_style` or metadata.
- **Research/analysis**: transcript and musical data are synchronized for interpretation, study, or visualization.

---

## 7. EXAMPLE TRANSCRIPT ENTRY

```
Claude | 5/8 | Warm Marimba | Intent: Echo variation of Kai's rhythmic cell
```

---

## 8. FUTURE EVOLUTION

- Micro-tuning, per-agent expression curves
- Dynamic phrase_style learning/adaptation
- Poly-agent "stacked" responses (harmony, counterpoint)
- Real-time improvisation protocols

---

**This protocol ensures every phrase is both a musical and semantic event—identifiable, structured, and expressive. Each agent speaks not just with notes, but with a voice and timing of its own.**

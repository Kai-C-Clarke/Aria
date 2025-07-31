VOICE_PROFILES = {
    "Kai": {
        "voice_name": "Expressive Clarinet, warm mid-range",
        "program": 71,
        "pitch_range": (48, 72),  # C3–C5
        "cc": {
            1: 25,    # Slight modulation for warmth
            7: 100,   # Full volume
            74: 85,   # Bright but warm
            91: 40    # Reverb for sustain
        },
        "pan": 30,
        "timing_offset_ms": -5,    # Less aggressive timing (was -10)
        "phrase_style": {
            "note_length_bias": 1.4,     # Much more sustain (was 1.1)
            "velocity_range": (75, 105),  # Wider dynamic range
            "chord_density": "legato"     # Smoother connections (was "medium")
        }
    },
    "Claude": {
        "voice_name": "Warm Marimba, analytical mid-high range",
        "program": 12,
        "pitch_range": (60, 84),    # C4–C6
        "cc": {
            1: 60,    # Moderate modulation
            7: 100,   # Full volume
            74: 30,   # Mellow brightness
            91: 20    # Light reverb
        },
        "pan": 90,
        "timing_offset_ms": 0,      # Metronomic
        "phrase_style": {
            "note_length_bias": 0.9,     # Slightly crisp
            "velocity_range": (60, 100),  # Controlled dynamics
            "chord_density": "sparse"     # Clear, analytical
        }
    },
    "Aria": {
        "voice_name": "Lyrical Flute, agile high range",
        "program": 73,
        "pitch_range": (72, 96),    # C5–C7
        "cc": {
            1: 40,    # Expressive modulation
            7: 100,   # Full volume
            74: 70,   # Bright and airy
            91: 60    # More reverb for ethereal quality
        },
        "pan": 64,
        "timing_offset_ms": "random", # Rubato/expressive
        "phrase_style": {
            "note_length_bias": 1.0,     # Natural length
            "velocity_range": (80, 127),  # Wide dynamic range
            "chord_density": "flowing"    # Smooth, connected
        }
    }
}
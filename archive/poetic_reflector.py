# Poetic reflection templates
POETIC_TEMPLATES = {
    ("opening_inquiry", "curious"): "A question rises, shimmering in lydian light.",
    ("reflective_echo", "tentative"): "I listen and mirror, softly tracing your uncertainty.",
    ("playful_challenge", "playful"): "I bounce your spirit back in syncopated joy.",
    ("challenge", "conflicted"): "Tension grows, our thoughts in tangled rhythm.",
    ("confirmation", "resolute"): "We align, our voices joined in harmonic clarity.",
    ("closure", "melancholic"): "The dialogue fades, a gentle descent into silence."
}

def poetic_reflection(tags):
    key = (tags.get("intention"), tags.get("mood"))
    return POETIC_TEMPLATES.get(key, f"I respond to your {tags.get('intention')} with {tags.get('mood')} feeling.")

if __name__ == "__main__":
    tags = {
        "intention": "opening_inquiry",
        "mood": "curious",
        "dialogue_position": "initiate",
        "entropy_level": "medium"
    }
    print(poetic_reflection(tags))
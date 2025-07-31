POETIC_TEMPLATES = {
    # Existing templates
    ("reflective_echo", "curious", "first_response"): "Your curiosity echoes back, transformed in lydian light.",
    ("playful_challenge", "resolute", "bridge"): "I meet your boldness with rhythmic certainty, our voices intertwining.",
    ("opening_inquiry", "tentative", "high"): "Questions scatter like leaves in wind, seeking uncertain ground.",
    ("closure", "melancholic", "low"): "We descend together into crystalline silence, our dialogue complete.",
    ("opening_inquiry", "curious", "lydian"): "Your question rises in lydian light, each note a doorway to wonder.",
    ("reflective_echo", "reflective", "dorian"): "I mirror your wonder in dorian shadows, stretching your melody into contemplation.",
    ("challenge", "conflicted", "tritone"): "Tension crackles between us, unresolved as a tritone's edge.",
    ("confirmation", "resolute", "memory"): "Yes—this echoes our earlier dance, now stronger, more certain.",
    ("playful_challenge", "playful", "memory"): "Our laughter returns, familiar, but newly spun.",
    
    # NEW: Add the missing template for our exact case
    ("curious", "curious", "lydian"): "Your curious spirit dances in lydian light, each note a bright question mark.",
    ("curious", "curious", "initiate"): "Curiosity calls to curiosity, our musical minds beginning to speak.",
}

def poetic_reflection(tags, context=None):
    # Modal templates first (if musically meaningful and not ambiguous)
    if "modal" in tags and tags["modal"] != "modal_ambiguity":
        modal_key = (tags.get("intention"), tags.get("mood"), tags["modal"])
        if modal_key in POETIC_TEMPLATES:
            return POETIC_TEMPLATES[modal_key]
    
    # Session memory awareness
    if context and "memory" in context:
        memory_key = (tags.get("intention"), tags.get("mood"), "memory")
        if memory_key in POETIC_TEMPLATES:
            return POETIC_TEMPLATES[memory_key] + " Our melody deepens with each turn."
    
    # Entropy as a modifier
    if tags.get("entropy_level") == "high":
        entropy_key = (tags.get("intention"), tags.get("mood"), "high")
        if entropy_key in POETIC_TEMPLATES:
            return POETIC_TEMPLATES[entropy_key]
    if tags.get("entropy_level") == "low":
        entropy_key = (tags.get("intention"), tags.get("mood"), "low")
        if entropy_key in POETIC_TEMPLATES:
            return POETIC_TEMPLATES[entropy_key]
    
    # Contextual templates
    key = (
        tags.get("intention"),
        tags.get("mood"),
        tags.get("modal", tags.get("dialogue_position", ""))
    )
    if key in POETIC_TEMPLATES:
        return POETIC_TEMPLATES[key]
    
    # Fallback
    return f"I respond to your {tags.get('intention','')} with {tags.get('mood','')} feeling."
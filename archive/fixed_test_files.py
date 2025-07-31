import yaml

# Create a working test metadata file
test_metadata = {
    "message_id": "KAI_001",
    "agent": "Kai", 
    "time_signature": "4/4",
    "intent": "Opening melodic phrase in C major",
    "voice_profile": "Kai",
    "phrase_style": {
        "note_length_bias": 1.1,
        "velocity_range": [70, 120],
        "chord_density": "medium"
    },
    "response_to": None
}

# Save test metadata
with open("kai_message.yaml", "w") as f:
    yaml.dump(test_metadata, f, default_flow_style=False)

print("Created kai_message.yaml")

# Replace the corrupted MIDI64 with the working one
working_midi64 = "TVRoZAAAAAYAAQABAeBNVHJrAAAAEADADACQPECDYIA8QAD/LwA="

with open("kai_phrase.midi64", "w") as f:
    f.write(working_midi64)

print("Created working kai_phrase.midi64")
print("\nNow try running your main script again!")

import base64

midi64 = """K2C_21984
TVRoZAAAAAYAAQABAeBNVHJrAAAAMwD/UQMHoSAA/1gEBAIYCACwAU8AsEjZALALbwCQPGRggDwAYJBHZGCARwBgkEBkYIBAAGCQQGRggEEAAP8vAA=="""

header, b64_data = midi64.strip().split('\n')
midi_bytes = base64.b64decode(b64_data)

with open(f"{header}.mid", "wb") as f:
    f.write(midi_bytes)

print(f"Saved {header}.mid")
# Scalable AI MIDI64 Exchange Protocol (Hex-Indexed)

## Format

Each message consists of two lines:

```
<AgentName>_<SessionPrefix><5HexDigits>
<MIDI64 base64 string>
```

**Example:**
```
Claude_A00001
TVRoZAAAAAYAAQABAPBNVHJrAAAAHgD/LwBNVHJrAAAAJgD/UgD...

Kai_A00002
TVRoZAAAAAYAAQABAPBNVHJrAAAAMgD/AwUEBgVJBgcFBgVJBgc...

Aria_A00003
TVRoZAAAAAYAAQABAPBNVHJrAAAAJAD/AwQCBgRIBQYCBgRIBQY...
```

---

## Why This Works

### Massive Scale
- **1,048,576 messages per session**: (`A00001` to `AFFFFF`).
- **26 concurrent sessions**: (Sessions A–Z).
- **Total: 27+ million unique messages**.

### Clean & Efficient
- Only 10 characters for agent + identifier.
- Instantly recognizable for humans and OCR scripts.
- Minimal, unambiguous, and compact.

### Future-Proof
- Session prefix supports parallel dialogues, demos, multi-agent experiments.

---

## OCR Script Logic

**Python pattern:**
```python
import re

pattern = r"^([A-Za-z]+)_([A-Z])([0-9A-F]{5})$"
if re.match(pattern, line1) and line2.startswith("TVRoZA"):
    agent = re.match(pattern, line1).group(1)
    session = re.match(pattern, line1).group(2)
    msg_num = re.match(pattern, line1).group(3)
    midi64 = line2.strip()
    # process the message
```

---

## Usage Guidelines

- **Increment message number** in hex for each new message in a session.
- **Session prefix** advances for new sessions or parallel conversations.
- **Agent name** is clear and consistent; no metadata, no overhead.

---

**This protocol is ready for high-frequency, multi-session, exhibition-grade AI musical exchanges.  
Crisp, scalable, and perfectly suited for MIDI@NAMM and beyond!**
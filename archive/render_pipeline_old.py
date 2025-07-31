import mido
from pydantic import BaseModel, ValidationError, Field
from typing import Dict, Tuple, Any, Optional, Union
import random
from voice_profiles import VOICE_PROFILES
import io

class PhraseStyle(BaseModel):
    note_length_bias: float = 1.0
    velocity_range: Tuple[int, int] = (80, 127)
    chord_density: str = "legato"

class MessageMetadata(BaseModel):
    message_id: str
    agent: str
    time_signature: str
    intent: str
    voice_profile: str
    phrase_style: Optional[PhraseStyle] = None
    response_to: Optional[str] = None

def validate_message_metadata(meta: Dict[str, Any]) -> MessageMetadata:
    try:
        return MessageMetadata(**meta)
    except ValidationError as e:
        print(f"[ERROR] Invalid message metadata: {e}")
        raise

def clamp_note_range(note: int, pitch_range: Tuple[int, int]) -> int:
    return min(max(note, pitch_range[0]), pitch_range[1])

def apply_voice_profile(mid: mido.MidiFile, profile: Dict[str, Any]) -> None:
    track = mid.tracks[0]
    # Insert program and controller changes at start
    track.insert(0, mido.Message('program_change', program=profile["program"], time=0))
    i = 1
    for cc, value in profile["cc"].items():
        track.insert(i, mido.Message('control_change', control=cc, value=value, time=0))
        i += 1
    track.insert(i, mido.Message('control_change', control=10, value=profile["pan"], time=0))
    # Clamp pitch range
    low, high = profile["pitch_range"]
    for msg in track:
        if msg.type in ['note_on', 'note_off']:
            original_note = msg.note
            msg.note = clamp_note_range(msg.note, (low, high))
            if msg.note != original_note:
                print(f"[INFO] Note {original_note} clamped to {msg.note} for range {low}-{high}")

def apply_timing_offset(mid: mido.MidiFile, timing_offset_ms: Union[int, str]) -> None:
    ticks_per_beat = mid.ticks_per_beat
    tempo = 500000  # default 120bpm
    for msg in mid.tracks[0]:
        if msg.type == 'set_tempo':
            tempo = msg.tempo
            break
    ms_per_tick = mido.tempo2bpm(tempo) / (ticks_per_beat * 1000.0)
    for msg in mid.tracks[0]:
        if msg.type in ['note_on', 'note_off']:
            if timing_offset_ms == "random":
                offset = random.randint(-7, 7)
            else:
                offset = timing_offset_ms
            ticks_offset = int(offset / ms_per_tick)
            msg.time = max(0, msg.time + ticks_offset)

def apply_phrase_style(mid: mido.MidiFile, style: PhraseStyle) -> None:
    for msg in mid.tracks[0]:
        if msg.type == 'note_on':
            # Velocity range
            min_vel, max_vel = style.velocity_range
            original_vel = msg.velocity
            msg.velocity = min(max(msg.velocity, min_vel), max_vel)
            # Note length bias and chord density could be implemented here as needed

def calculate_rest_duration(time_signature: str, mode: str = "bar") -> float:
    # Returns rest duration in beats (float)
    beats, _ = [int(x) for x in time_signature.split("/")]
    if mode == "bar":
        return beats
    elif mode == "note":
        return 1.0  # single quarter note rest as default
    else:
        return 0.0  # silence

def render_and_merge_message(midi64_bytes: bytes, meta: Dict[str, Any], rest_mode: str = "bar") -> mido.MidiFile:
    # 1. Validate schema
    metadata = validate_message_metadata(meta)
    # 2. Load MIDI
    mid = mido.MidiFile(file=io.BytesIO(midi64_bytes))
    # 3. Apply voice profile
    profile = VOICE_PROFILES[metadata.voice_profile]
    apply_voice_profile(mid, profile)
    # 4. Timing offset
    apply_timing_offset(mid, profile['timing_offset_ms'])
    # 5. Phrase style
    if metadata.phrase_style:
        apply_phrase_style(mid, metadata.phrase_style)
    # 6. Insert rest (handled externally in a merge step)
    # 7. Return processed MIDI file for merging
    return mid
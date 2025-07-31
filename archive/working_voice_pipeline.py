import mido
import io
from voice_profiles import VOICE_PROFILES

def apply_note_length_bias(track, bias):
    """Apply note length bias to a MIDI track"""
    
    if bias == 1.0:
        return track  # No change needed
    
    modified_track = mido.MidiTrack()
    
    for msg in track:
        if msg.type == 'note_off':
            # Extend or shorten note duration based on bias
            new_time = int(msg.time * bias)
            modified_track.append(msg.copy(time=new_time))
        else:
            # Copy other messages as-is
            modified_track.append(msg.copy())
    
    return modified_track

def apply_velocity_range(track, velocity_range):
    """Apply velocity range to note events"""
    
    min_vel, max_vel = velocity_range
    modified_track = mido.MidiTrack()
    
    for msg in track:
        if msg.type == 'note_on' and msg.velocity > 0:
            # Scale velocity to the specified range
            # Assuming original range is 64-127, scale to new range
            original_range = 127 - 64
            new_range = max_vel - min_vel
            scaled_vel = min_vel + int(((msg.velocity - 64) / original_range) * new_range)
            scaled_vel = max(min_vel, min(max_vel, scaled_vel))
            modified_track.append(msg.copy(velocity=scaled_vel))
        else:
            modified_track.append(msg.copy())
    
    return modified_track

def apply_voice_profile(mid, agent_name):
    """Apply complete voice profile to MIDI file"""
    
    profile = VOICE_PROFILES.get(agent_name)
    if not profile:
        print(f"No voice profile found for {agent_name}")
        return mid
    
    print(f"Applying voice profile for {agent_name}: {profile['voice_name']}")
    
    # Work on the first track
    if not mid.tracks:
        return mid
    
    track = mid.tracks[0]
    modified_track = mido.MidiTrack()
    
    # Add program change for instrument
    modified_track.append(mido.Message('program_change', program=profile['program'], time=0))
    
    # Add controller changes
    for cc_num, cc_value in profile.get('cc', {}).items():
        modified_track.append(mido.Message('control_change', control=cc_num, value=cc_value, time=0))
    
    # Add pan
    if 'pan' in profile:
        modified_track.append(mido.Message('control_change', control=10, value=profile['pan'], time=0))
    
    # Apply phrase style transformations
    phrase_style = profile.get('phrase_style', {})
    
    # Process each message in the original track
    for msg in track:
        if msg.type == 'program_change':
            # Skip original program change, we added our own
            continue
        elif msg.type == 'note_on' and msg.velocity > 0:
            # Apply velocity range
            velocity_range = phrase_style.get('velocity_range', (msg.velocity, msg.velocity))
            min_vel, max_vel = velocity_range
            # Simple scaling - keep original velocity proportions
            new_velocity = max(min_vel, min(max_vel, msg.velocity))
            modified_track.append(msg.copy(velocity=new_velocity))
        elif msg.type == 'note_off':
            # Apply note length bias
            note_length_bias = phrase_style.get('note_length_bias', 1.0)
            new_time = int(msg.time * note_length_bias)
            modified_track.append(msg.copy(time=new_time))
        else:
            # Copy other messages as-is
            modified_track.append(msg.copy())
    
    # Replace the track
    mid.tracks[0] = modified_track
    
    print(f"Applied voice profile: program={profile['program']}, note_length_bias={phrase_style.get('note_length_bias', 1.0)}")
    
    return mid

def render_and_merge_message(midi_bytes, metadata, rest_mode="bar"):
    """Full rendering pipeline with working voice profiles"""
    
    # Load MIDI from bytes
    mid = mido.MidiFile(file=io.BytesIO(midi_bytes))
    
    print(f"Loaded MIDI: {len(mid.tracks)} tracks")
    
    # Get agent info
    agent = metadata.get("agent", "Unknown")
    print(f"Processing for agent: {agent}")
    
    # Apply voice profile
    mid = apply_voice_profile(mid, agent)
    
    return mid

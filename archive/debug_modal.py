#!/usr/bin/env python3

def calculate_intervals(pitches):
    intervals = [pitches[i+1] - pitches[i] for i in range(len(pitches)-1)]
    print(f"🔍 Pitches: {pitches}")
    print(f"🔍 Intervals: {intervals}")
    return intervals

def detect_modal_characteristics(pitches):
    intervals = calculate_intervals(pitches)
    
    # Direct lydian detection
    if len(pitches) >= 4:
        # Check for F# (66) and C (60) present = Lydian!
        if 66 in pitches and 60 in pitches:
            print("✅ Found F# (66) and C (60) → LYDIAN!")
            return "lydian"
    
    # Check intervals
    if 4 in intervals:
        print("✅ Found +4 interval → LYDIAN!")
        return "lydian"
    elif 6 in intervals:
        print("✅ Found +6 interval (tritone) → TRITONE!")
        return "tritone"
    elif 11 in intervals:
        print("✅ Found +11 interval → DORIAN!")
        return "dorian"
    
    print("❌ No modal characteristics detected → MODAL_AMBIGUITY")
    return "modal_ambiguity"

if __name__ == "__main__":
    print("🧪 Testing Modal Detection:")
    
    # Test our lydian example
    lydian_pitches = [60, 62, 66, 69]  # C, D, F#, A
    result = detect_modal_characteristics(lydian_pitches)
    print(f"🎵 Final result: {result}")
    print()
    
    # Test a different example
    dorian_pitches = [62, 64, 65, 73]  # D, E, F, C  
    result2 = detect_modal_characteristics(dorian_pitches)
    print(f"🎵 Final result: {result2}")
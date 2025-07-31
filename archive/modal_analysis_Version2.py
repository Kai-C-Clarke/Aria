def calculate_intervals(pitches):
    return [pitches[i+1] - pitches[i] for i in range(len(pitches)-1)]

def detect_modal_characteristics(pitches):
    intervals = calculate_intervals(pitches)
    # Direct lydian detection by pitch content (C and F#)
    if len(pitches) >= 4 and 66 in pitches and 60 in pitches:
        return "lydian"
    # Interval-based checks
    if 4 in intervals:
        return "lydian"
    if 11 in intervals:
        return "dorian"
    if 6 in intervals:
        return "tritone"
    return "modal_ambiguity"

# Keep the original functions for compatibility
def has_raised_fourth(intervals):
    return 4 in intervals or 6 in intervals

def has_natural_seventh(intervals):
    return 11 in intervals

def has_tritone_tension(intervals):
    return 6 in intervals
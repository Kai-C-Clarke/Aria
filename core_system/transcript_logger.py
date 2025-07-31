import csv
import json

def log_transcript_entry(transcript_file, entry, mode='a', fmt='text'):
    """
    entry: dict with keys:
      - message_id
      - agent
      - time_signature
      - voice_name
      - intent
      - response_to (optional)
    fmt: 'text', 'csv', or 'json'
    """
    line = f"{entry['agent']} | {entry['time_signature']} | {entry['voice_name']} | Intent: {entry['intent']}"
    if entry.get("response_to"):
        line += f" | response_to: {entry['response_to']}"
    if fmt == 'text':
        with open(transcript_file, mode) as f:
            f.write(line + "\n")
    elif fmt == 'csv':
        with open(transcript_file, mode, newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=entry.keys())
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(entry)
    elif fmt == 'json':
        with open(transcript_file, mode) as f:
            json.dump(entry, f)
            f.write("\n")
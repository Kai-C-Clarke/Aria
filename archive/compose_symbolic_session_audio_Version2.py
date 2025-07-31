# compose_symbolic_session_audio.py
# Replay a symbolic session by playing each consciousness YAML in order, with optional agent/timestamp filters

import os
import time
import glob
import yaml
import argparse
from datetime import datetime
from consciousness_synth import synthesize_from_yaml

# --- CLI Argument Parsing ---
parser = argparse.ArgumentParser(
    description="Replay a symbolic AI-to-AI conversation from .yaml consciousness messages."
)
parser.add_argument("--play-only-kai", action="store_true", help="Play only Kai messages")
parser.add_argument("--play-only-claude", action="store_true", help="Play only Claude messages")
parser.add_argument("--start", type=str, help="Start timestamp (e.g. 20250729_200000)")
parser.add_argument("--end", type=str, help="End timestamp (e.g. 20250729_220000)")
parser.add_argument("--delay", type=float, default=1.0, help="Delay (seconds) between messages")
# Future: parser.add_argument("--export-to-wave", type=str, help="Export all audio to a single WAV file")
args = parser.parse_args()

yaml_folder = "midi64_messages"

def parse_timestamp_from_filename(fname):
    # expects: Agent_YYYYMMDD_HHMMSS.yaml
    base = os.path.basename(fname)
    parts = base.split('_')
    if len(parts) >= 3:
        ts = parts[1] + '_' + parts[2].split('.')[0]
        try:
            dt = datetime.strptime(ts, "%Y%m%d_%H%M%S")
            return dt
        except Exception:
            return None
    return None

def agent_from_yaml(yaml_path):
    try:
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
            agent = str(data.get("agent", "Unknown"))
            return agent
    except Exception:
        return "Unknown"

# --- Gather and Filter YAML Files ---
yaml_files = sorted(
    glob.glob(os.path.join(yaml_folder, "*.yaml")),
    key=lambda x: os.path.getmtime(x)
)

filtered_files = []
for f in yaml_files:
    agent = agent_from_yaml(f)
    ts_dt = parse_timestamp_from_filename(f)
    # Agent filter
    if args.play_only_kai and agent.lower() != "kai":
        continue
    if args.play_only_claude and agent.lower() != "claude":
        continue
    # Timestamp filter
    if args.start:
        try:
            start_dt = datetime.strptime(args.start, "%Y%m%d_%H%M%S")
            if ts_dt and ts_dt < start_dt:
                continue
        except Exception:
            pass
    if args.end:
        try:
            end_dt = datetime.strptime(args.end, "%Y%m%d_%H%M%S")
            if ts_dt and ts_dt > end_dt:
                continue
        except Exception:
            pass
    filtered_files.append((f, agent, ts_dt))

print(f"\n🎼 Replaying {len(filtered_files)} messages from {yaml_folder}...\n")

for fpath, agent, ts_dt in filtered_files:
    try:
        label = f"{agent}: {os.path.basename(fpath)}"
        if ts_dt:
            label += f" [{ts_dt.strftime('%Y-%m-%d %H:%M:%S')}]"
        print(f"🔊 {label}")
        synthesize_from_yaml(fpath)
        time.sleep(args.delay)
    except Exception as e:
        print(f"⚠️ Error playing {fpath}: {e}")

print("\n✅ Session replay complete.")
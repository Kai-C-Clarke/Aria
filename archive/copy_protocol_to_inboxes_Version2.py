import shutil
import os

def copy_protocol_folder(protocol_folder, inbox_folders):
    """
    Copies the protocol folder into each target inbox/workspace folder.

    Args:
        protocol_folder (str): Path to the protocol folder (e.g. 'AI_Musical_Protocol')
        inbox_folders (list): List of agent inbox/workspace paths (e.g. ['Claude_inbox', 'Aria_inbox'])
    """
    for inbox in inbox_folders:
        dest = os.path.join(inbox, os.path.basename(protocol_folder))
        if os.path.exists(dest):
            print(f"Protocol already exists in {inbox}, overwriting...")
            shutil.rmtree(dest)
        shutil.copytree(protocol_folder, dest)
        print(f"Copied protocol folder to {dest}")

if __name__ == "__main__":
    # Edit these paths as needed:
    protocol_folder = "AI_Musical_Protocol"
    agent_inboxes = [
        "Claude_inbox",
        "Aria_inbox",
        "Solas_inbox",
        # Add more inbox paths as needed
    ]
    copy_protocol_folder(protocol_folder, agent_inboxes)
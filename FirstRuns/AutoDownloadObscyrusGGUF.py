import os
from huggingface_hub import hf_hub_download, login

# Log in with the provided read-only token (optional for public repos, but included for safety)
login(token="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")

# Repository details
repo_id = "ScriptWizarddd/Obscyrus-8B-ClaudeFT"  # Adjust if the username or repo name changes
filename = "Obscyrus1-8B-ClaudeFT.gguf"  # Replace with the exact filename once uploaded (e.g., from HF repo files list)

# Download path: Creates ./GGUFs relative to the script's location
download_dir = os.path.join(os.path.dirname(__file__), "GGUFs")
os.makedirs(download_dir, exist_ok=True)

# Download the file
local_filepath = hf_hub_download(
    repo_id=repo_id,
    filename=filename,
    local_dir=download_dir,
    token="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"  # Use token again if needed
)

print(f"Model downloaded to: {local_filepath}")
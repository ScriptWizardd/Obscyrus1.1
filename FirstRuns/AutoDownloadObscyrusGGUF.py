import os
from huggingface_hub import hf_hub_download, login

# Get token from environment variable (set via export HF_TOKEN="your_token_here")
hf_token = os.getenv('HF_TOKEN')
if hf_token:
    login(token=hf_token)
else:
    print("Warning: No HF_TOKEN environment variable set. Assuming public repo access.")

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
    token=hf_token  # Use token if set
)

print(f"Model downloaded to: {local_filepath}")
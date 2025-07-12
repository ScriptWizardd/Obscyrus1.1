import os
from huggingface_hub import hf_hub_download, login

# Path to store the token
token_file = 'hf_token.txt'

# Check if token file exists
if os.path.exists(token_file):
    with open(token_file, 'r') as f:
        hf_token = f.read().strip()
    print("Loaded Hugging Face token from hf_token.txt.")
else:
    # Prompt user for token
    hf_token = input("Enter your Hugging Face token (required for download): ").strip()
    # Save to file
    with open(token_file, 'w') as f:
        f.write(hf_token)
    print("Hugging Face token saved to hf_token.txt for future use.")

# Login if token is provided (even if empty, but warn if empty)
if hf_token:
    login(token=hf_token)
else:
    print("Warning: No Hugging Face token provided. Assuming public repo access.")

# Repository details
repo_id = "ScriptWizarddd/Obscyrus-8B-ClaudeFT"  # From the provided URL
filename = "Obscyrus1-8B-ClaudeFT.gguf"  # Assuming this is the file name based on previous code

# Download path: Creates ./GGUFs relative to the script's location
download_dir = os.path.join(os.path.dirname(__file__), "GGUFs")
os.makedirs(download_dir, exist_ok=True)

# Download the file
local_filepath = hf_hub_download(
    repo_id=repo_id,
    filename=filename,
    local_dir=download_dir,
    token=hf_token if hf_token else None  # Use token if available
)

print(f"Model downloaded to: {local_filepath}")

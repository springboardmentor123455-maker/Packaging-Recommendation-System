from huggingface_hub import HfApi
import os

token = os.getenv("HF_TOKEN")
if not token:
    raise ValueError("HF_TOKEN environment variable not set. Please set HF_TOKEN in your environment.")
repo_id = "ragasudhaselvaraj/EcoPackAI"

api = HfApi()

print(f"Updating app code on {repo_id}...")

files_to_upload = [
    "Milestone_3/Module_5_Flask_Backend_API/app/routes.py"
]

# Upload files
for file in files_to_upload:
    if os.path.exists(file):
        print(f"Uploading {file}...")
        api.upload_file(
            path_or_fileobj=file,
            path_in_repo=file,
            repo_id=repo_id,
            repo_type="space",
            token=token
        )

print("App Update Complete! Space will rebuild now.")

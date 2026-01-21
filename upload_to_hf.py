from huggingface_hub import HfApi
import os

token = "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"
repo_id = "ragasudhaselvaraj/EcoPackAI"

api = HfApi()

print(f"Starting upload to {repo_id}...")

# Upload specific folders and files to avoid uploading giant unrelated things
folders_to_upload = [
    "Milestone_1",
    "Milestone_3",
    "infosys"
]
files_to_upload = [
    "Dockerfile",
    "README.md",
    "requirements.txt"
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

# Upload folders
for folder in folders_to_upload:
    if os.path.exists(folder):
        print(f"Uploading folder {folder}...")
        api.upload_folder(
            folder_path=folder,
            path_in_repo=folder,
            repo_id=repo_id,
            repo_type="space",
            token=token,
            ignore_patterns=[".git", "__pycache__", "*.pyc"]
        )

print("Upload Complete! Check your Space.")

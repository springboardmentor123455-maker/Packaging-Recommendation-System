from huggingface_hub import HfApi
import os
import glob

# Get the token from env (secure)
token = os.getenv("HF_TOKEN")
if not token:
    print("Error: HF_TOKEN environment variable not set.")
    exit(1)

repo_id = "ragasudhaselvaraj/EcoPackAI"
api = HfApi()

print(f"Starting FULL deployment to {repo_id}...")

# Root directory of the project (infosys folder)
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
print(f"Project Root: {root_dir}")

# Define what to upload
include_patterns = [
    "Dockerfile",
    "README.md",
    "Milestone_1/**/*",
    "Milestone_2/**/*",
    "Milestone_3/**/*"
]

files_to_upload = []

for pattern in include_patterns:
    full_pattern = os.path.join(root_dir, pattern)
    # recursive=True for **
    found_files = glob.glob(full_pattern, recursive=True)
    
    for file_path in found_files:
        if os.path.isfile(file_path):
            # Filtering
            if "__pycache__" in file_path:
                continue
            if ".git" in file_path:
                continue
            if ".DS_Store" in file_path:
                continue
            if file_path.endswith(".pyc"):
                continue
                
            # Calculate relative path for repo
            rel_path = os.path.relpath(file_path, root_dir)
            files_to_upload.append((file_path, rel_path))

print(f"Found {len(files_to_upload)} files to upload.")

# Batch upload is safer/faster for many files but api.upload_file is simpler for loop
# We'll use a loop but print progress.
count = 0
total = len(files_to_upload)

for local_path, repo_path in files_to_upload:
    count += 1
    # Windows path separator fix just in case, though HF handles it
    repo_path = repo_path.replace("\\", "/")
    
    print(f"[{count}/{total}] Uploading {repo_path}...")
    try:
        api.upload_file(
            path_or_fileobj=local_path,
            path_in_repo=repo_path,
            repo_id=repo_id,
            repo_type="space",
            token=token
        )
    except Exception as e:
        print(f"Failed to upload {repo_path}: {e}")

print("---------------------------------------------------")
print("FULL Deployment Completed! Check your Space logs.")
print(f"Space URL: https://huggingface.co/spaces/{repo_id}")

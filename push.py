#!/usr/bin/env python3
"""
Super Simple Git Push

Just pushes your code to an existing repository.
Works with GitHub or Hugging Face.

Usage:
  python push.py github  # Push to GitHub
  python push.py hf      # Push to Hugging Face
  python push.py --force # Force push
"""

import os
import sys
import argparse
import subprocess

# Install required packages if needed
try:
    import git
    import dotenv
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "GitPython", "python-dotenv"])
    import git
    import dotenv

# Load environment variables
dotenv.load_dotenv()

def push_to_remote(remote_name, force=False):
    """Push code to the specified remote"""
    try:
        # Get the repo
        repo = git.Repo('.')
        
        # Check if remote exists
        try:
            repo.remote(remote_name)
        except ValueError:
            if remote_name == "github" or remote_name == "origin":
                # Set up GitHub remote
                gh_username = os.getenv('GITHUB_USERNAME') or input("GitHub username: ")
                gh_token = os.getenv('GITHUB_TOKEN') or input("GitHub token: ")
                repo_name = os.getenv('REPO_NAME') or input("Repository name: ")
                url = f"https://{gh_username}:{gh_token}@github.com/{gh_username}/{repo_name}.git"
                repo.create_remote('origin', url)
                remote_name = 'origin'
                print(f"✅ Added GitHub remote")
            elif remote_name == "hf" or remote_name == "space":
                # Set up Hugging Face remote
                hf_username = os.getenv('HF_USERNAME') or input("Hugging Face username: ")
                hf_token = os.getenv('HF_TOKEN') or input("Hugging Face token: ")
                space_name = os.getenv('HF_SPACE_NAME') or input("Space name: ")
                url = f"https://{hf_username}:{hf_token}@huggingface.co/spaces/{hf_username}/{space_name}"
                repo.create_remote('space', url)
                remote_name = 'space'
                print(f"✅ Added Hugging Face remote")
        
        # Add all files
        repo.git.add(A=True)
        
        # Commit if there are changes
        try:
            repo.git.commit("-m", "Update")
            print("✅ Changes committed")
        except git.exc.GitCommandError as e:
            if "nothing to commit" in str(e):
                print("ℹ️ No changes to commit")
            else:
                print(f"❌ Commit error: {e}")
                return False
        
        # Push to remote
        try:
            if force:
                repo.git.push(remote_name, 'main', '--force')
                print(f"✅ Force pushed to {remote_name}")
            else:
                try:
                    repo.git.push(remote_name, 'main')
                except git.exc.GitCommandError:
                    # Branch might not exist yet
                    repo.git.push('-u', remote_name, 'main')
                print(f"✅ Pushed to {remote_name}")
            return True
        except git.exc.GitCommandError as e:
            print(f"❌ Push error: {e}")
            print("Try using --force if you need to overwrite remote changes")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Simple Git Push')
    parser.add_argument('remote', choices=['github', 'hf', 'origin', 'space'], 
                      help='Remote to push to (github/hf/origin/space)')
    parser.add_argument('--force', action='store_true', help='Force push')
    
    # Check if Git is initialized
    if not os.path.exists('.git'):
        print("Initializing Git repository...")
        git.Repo.init('.')
        print("✅ Git initialized")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Map shorthand to actual remote names
    remote_map = {
        'github': 'origin',
        'hf': 'space',
        'origin': 'origin',
        'space': 'space'
    }
    
    # Push to remote
    if push_to_remote(remote_map[args.remote], args.force):
        print("✨ Push successful! ✨")
    else:
        print("❌ Push failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
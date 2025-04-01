#!/usr/bin/env python3
"""
GitHub Repository Upload Script

This script automates the process of:
1. Creating a GitHub repository if it doesn't exist
2. Setting up a local Git repository
3. Adding your files to the repository
4. Pushing to GitHub
5. Configuring GitHub Actions for automated deployments to Hugging Face

Requirements:
- Python 3.6+
- python-dotenv
- requests
- GitPython
"""

import os
import sys
import argparse
import subprocess
import json
from pathlib import Path
from datetime import datetime

try:
    import dotenv
    import requests
    import git
except ImportError:
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv", "requests", "GitPython"])
    import dotenv
    import requests
    import git

# Load environment variables
dotenv.load_dotenv()

# Configuration from environment variables
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
PROJECT_NAME = os.getenv('PROJECT_NAME')
PROJECT_DESCRIPTION = os.getenv('PROJECT_DESCRIPTION', 'FastAPI text generation API with FLAN-T5')
HF_USERNAME = os.getenv('HF_USERNAME')
HF_SPACE_NAME = os.getenv('HF_SPACE_NAME')

# Derived values
GITHUB_REPO_URL = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{PROJECT_NAME}.git"


def check_env_vars():
    """Verify all required environment variables are set."""
    required_vars = ['GITHUB_USERNAME', 'GITHUB_TOKEN', 'PROJECT_NAME']
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        print(f"Error: Missing required environment variables: {', '.join(missing)}")
        print("Please create a .env file with the following variables:")
        print("""
GITHUB_USERNAME=your_github_username
GITHUB_TOKEN=your_github_token
PROJECT_NAME=your_project_name
PROJECT_DESCRIPTION=your_description  # Optional
        """)
        sys.exit(1)
    
    print("✅ All required environment variables are set")


def create_github_workflow(repo_path):
    """Create GitHub Actions workflow file for HF sync if HF credentials are available."""
    # Only create the workflow if HF credentials are available
    if not os.getenv('HF_USERNAME') or not os.getenv('HF_SPACE_NAME'):
        print("ℹ️ Skipping GitHub Actions workflow creation (HF_USERNAME or HF_SPACE_NAME not set)")
        return
    
    workflow_dir = os.path.join(repo_path, '.github', 'workflows')
    os.makedirs(workflow_dir, exist_ok=True)
    
    workflow_file = os.path.join(workflow_dir, 'sync-to-huggingface.yml')
    
    with open(workflow_file, 'w', encoding='utf-8') as f:
        f.write(f"""name: Sync to Hugging Face Space

on:
  push:
    branches: [main]
  workflow_dispatch:  # Enables manual triggering

jobs:
  sync-to-hub:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
          lfs: true
      
      - name: Push to Hugging Face Space
        env:
          HF_TOKEN: ${{{{ secrets.HF_TOKEN }}}}
        run: |
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git config --global user.name "GitHub Actions"
          git push https://{HF_USERNAME}:${{{{ secrets.HF_TOKEN }}}}@huggingface.co/spaces/{HF_USERNAME}/{HF_SPACE_NAME} main
""")
    
    print(f"✅ Created GitHub Actions workflow at {workflow_file}")


def update_readme(repo_path):
    """Update README with GitHub information."""
    readme_path = os.path.join(repo_path, 'README.md')
    
    if not os.path.exists(readme_path):
        # Create a basic README if it doesn't exist
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(f"# {PROJECT_NAME}\n\n{PROJECT_DESCRIPTION}\n")
    
    # Read the current README
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add GitHub section if it doesn't exist
    if "## GitHub Repository" not in content:
        github_info = f"""
## GitHub Repository

This project is hosted on GitHub:

- Repository: [https://github.com/{GITHUB_USERNAME}/{PROJECT_NAME}](https://github.com/{GITHUB_USERNAME}/{PROJECT_NAME})

### Development

1. Clone the repository:
   ```bash
   git clone https://github.com/{GITHUB_USERNAME}/{PROJECT_NAME}.git
   cd {PROJECT_NAME}
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Make your changes and push them to GitHub:
   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin main
   ```

Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content + github_info)
    
    print(f"✅ Updated README with GitHub information at {readme_path}")


def create_github_repo():
    """Create a new GitHub repository if it doesn't exist."""
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    repo_data = {
        'name': PROJECT_NAME,
        'description': PROJECT_DESCRIPTION,
        'private': False,
        'auto_init': False
    }
    
    response = requests.post(
        'https://api.github.com/user/repos',
        headers=headers,
        data=json.dumps(repo_data)
    )
    
    if response.status_code == 201:
        print(f"✅ Created GitHub repository: {GITHUB_USERNAME}/{PROJECT_NAME}")
        return True
    elif response.status_code == 422:  # Repository already exists
        print(f"ℹ️ GitHub repository already exists: {GITHUB_USERNAME}/{PROJECT_NAME}")
        return True
    else:
        print(f"❌ Failed to create GitHub repository: {response.status_code}")
        try:
            error_details = response.json()
            print(f"Error details: {error_details}")
        except:
            print(f"Response text: {response.text}")
        return False


def setup_local_git(repo_path):
    """Set up local git repository with GitHub remote."""
    # Initialize git repository if it's not already one
    if not os.path.exists(os.path.join(repo_path, '.git')):
        repo = git.Repo.init(repo_path)
        print(f"✅ Initialized git repository at {repo_path}")
    else:
        repo = git.Repo(repo_path)
        print(f"ℹ️ Git repository already exists at {repo_path}")
    
    # Configure git user
    with repo.config_writer() as git_config:
        if not git_config.has_section('user'):
            git_config.add_section('user')
        git_config.set_value('user', 'name', GITHUB_USERNAME)
        git_config.set_value('user', 'email', f"{GITHUB_USERNAME}@users.noreply.github.com")
    
    # Add GitHub remote
    try:
        github_remote = repo.remote('origin')
        github_remote.set_url(GITHUB_REPO_URL)
        print(f"ℹ️ Updated existing GitHub remote: origin")
        # Don't print the full URL with token for security
    except ValueError:
        repo.create_remote('origin', GITHUB_REPO_URL)
        print(f"✅ Added GitHub remote: origin")
        # Don't print the full URL with token for security
    
    return repo


def create_env_example(repo_path):
    """Create a .env.example file as a template."""
    env_example_path = os.path.join(repo_path, '.env.example')
    
    with open(env_example_path, 'w', encoding='utf-8') as f:
        f.write("""# GitHub Configuration
GITHUB_USERNAME=your_github_username
GITHUB_TOKEN=your_github_personal_access_token

# Project Configuration
PROJECT_NAME=your_project_name
PROJECT_DESCRIPTION=your_project_description

# Hugging Face Configuration (Optional, for GitHub Actions sync)
HF_USERNAME=your_huggingface_username
HF_SPACE_NAME=your_space_name
""")
    
    # Make sure .env is in .gitignore
    gitignore_path = os.path.join(repo_path, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '.env' not in content:
            with open(gitignore_path, 'a', encoding='utf-8') as f:
                f.write('\n# Environment variables\n.env\n')
    else:
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write('# Environment variables\n.env\n')
    
    print(f"✅ Created .env.example at {env_example_path}")


def commit_and_push(repo, message="Initial commit"):
    """Commit changes and push to GitHub."""
    # Add all files
    repo.git.add(A=True)
    
    # Commit
    try:
        repo.git.commit(m=message)
        print(f"✅ Committed changes with message: '{message}'")
    except git.exc.GitCommandError as e:
        if "nothing to commit" in str(e):
            print("ℹ️ No changes to commit")
            return True
        else:
            print(f"❌ Failed to commit: {e}")
            return False
    
    # Push to GitHub
    try:
        repo.git.push('origin', 'main')
        print("✅ Pushed changes to GitHub")
        return True
    except git.exc.GitCommandError as e:
        if "rejected" in str(e) and "non-fast-forward" in str(e):
            print("⚠️ Push rejected. The remote repository has changes that are not in your local repository.")
            choice = input("Do you want to force push? This will overwrite remote changes. (y/N): ")
            if choice.lower() == 'y':
                try:
                    repo.git.push('origin', 'main', force=True)
                    print("✅ Force pushed changes to GitHub")
                    return True
                except git.exc.GitCommandError as e2:
                    print(f"❌ Failed to force push to GitHub: {e2}")
                    return False
            else:
                print("❌ Push aborted. You may need to pull changes first: git pull origin main")
                return False
        else:
            print(f"❌ Failed to push to GitHub: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description='Upload project to GitHub')
    parser.add_argument('--path', type=str, default='.', help='Path to the project directory (default: current directory)')
    parser.add_argument('--create-repo', action='store_true', help='Create GitHub repository if it doesn\'t exist')
    parser.add_argument('--message', type=str, default='Initial commit', help='Commit message')
    parser.add_argument('--push', action='store_true', help='Push changes to GitHub after setup')
    parser.add_argument('--branch', type=str, default='main', help='Branch to push to (default: main)')
    
    args = parser.parse_args()
    
    # Force utf-8 encoding for output
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        # For Python < 3.7
        pass
    
    # Absolute path to the project directory
    repo_path = os.path.abspath(args.path)
    
    # Check if directory exists
    if not os.path.isdir(repo_path):
        print(f"Error: Directory '{repo_path}' does not exist")
        sys.exit(1)
    
    print(f"Setting up GitHub repository for {repo_path}")
    
    # Check environment variables
    check_env_vars()
    
    # Create GitHub repository if requested
    if args.create_repo:
        if not create_github_repo():
            sys.exit(1)
    
    # Set up local git repository
    repo = setup_local_git(repo_path)
    
    # Create .env.example file
    create_env_example(repo_path)
    
    # Create GitHub workflow if HF credentials are available
    create_github_workflow(repo_path)
    
    # Update README
    update_readme(repo_path)
    
    # Commit and push changes if requested
    if args.push:
        if not commit_and_push(repo, args.message):
            sys.exit(1)
    
    print("\n✨ GitHub setup completed successfully! ✨")
    print(f"GitHub Repository: https://github.com/{GITHUB_USERNAME}/{PROJECT_NAME}")
    
    if os.getenv('HF_USERNAME') and os.getenv('HF_SPACE_NAME'):
        print("\nTo enable automatic sync to Hugging Face Space:")
        print("1. Add the HF_TOKEN secret to your GitHub repository")
        print(f"   - Go to https://github.com/{GITHUB_USERNAME}/{PROJECT_NAME}/settings/secrets/actions")
        print("   - Add a new repository secret with name 'HF_TOKEN' and your Hugging Face token as the value")
    else:
        print("\nTo enable automatic sync to Hugging Face Space, add the following to your .env file:")
        print("HF_USERNAME=your_huggingface_username")
        print("HF_SPACE_NAME=your_space_name")
        print("Then run this script again with the --push flag")
    
    print("\nNext steps:")
    if not args.push:
        print("1. If you didn't push changes (--push), commit and push them manually")
    print("2. Clone your repository on other machines: git clone https://github.com/{GITHUB_USERNAME}/{PROJECT_NAME}.git")


if __name__ == "__main__":
    main()
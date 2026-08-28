# B-008: Files That Never Get Lost

### Git Basics — Version Control from Zero to First Pull Request

> *"Git is a time machine for your code. Every commit is a snapshot you can return to. Every branch is an alternate timeline you can explore. Every merge is two timelines becoming one. Once you understand this, you'll never fear breaking things again — because nothing is ever truly broken if you committed it."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Understand what version control is and why every developer uses it
2. Initialize a Git repository and make your first commit
3. Use `add`, `commit`, `status`, `log`, and `diff` fluently
4. Push code to GitHub and understand remote vs. local repositories
5. Create a branch, make changes, and open a pull request

**Prerequisite:** B-001 through B-005 (terminal fluency)

**Build Artifact:** A Git repository on GitHub containing your `developer-workspace/` from B-002, with a proper commit history and README

**Credential:** `CCSLL-L0-B008-GitPilot` — on-chain on Base

---

## Chapter 1: Why Version Control?

Imagine you're writing code without Git. You make changes. Something breaks. You try to undo it, but you've saved over the original file. You have no idea what you changed. You've lost hours of work.

Now imagine you're working on a team of 10 developers. Each person is editing different files. How do you combine all their work without losing anyone's changes? How do you know who changed what and why?

Git solves both problems. It:
1. Keeps a complete history of every change ever made
2. Lets you experiment safely on branches without affecting the main codebase
3. Makes collaboration on shared code manageable at any team size

*[Reality — Git is used by virtually every software project in the world. As of 2026, over 100 million repositories exist on GitHub alone.]*

---

## Chapter 2: How Git Works

Git's mental model is simple:

```
Working Directory  →  Staging Area  →  Local Repository  →  Remote Repository
  (your files)         (git add)         (git commit)         (git push)
```

| Area | What It Is |
|---|---|
| **Working Directory** | Your actual files on disk — where you edit code |
| **Staging Area** | A "ready to commit" holding area — you choose what goes in next commit |
| **Local Repository** | Your complete history stored in the `.git/` folder |
| **Remote Repository** | A copy on a server (GitHub, GitLab) — for backup and collaboration |

---

## Chapter 3: Git Setup

```bash
# Set your identity (done once per machine)
git config --global user.name "Charles Earl Lipshay"
git config --global user.email "charles@lippytm.ai"
git config --global init.defaultBranch main

# Verify your config
git config --list

# Set VS Code as default editor (optional)
git config --global core.editor "code --wait"
```

---

## Chapter 4: The Core Workflow

```bash
# Initialize a new repository
cd ~/developer-workspace
git init
# Initialized empty Git repository in ~/developer-workspace/.git/

# See the current state
git status

# Stage files for the next commit
git add README.md           # add one file
git add project-alpha/      # add a directory
git add .                   # add everything (use carefully)

# See what's staged vs unstaged
git status
git diff                    # unstaged changes
git diff --staged           # staged changes

# Commit with a message
git commit -m "Initial commit: developer workspace structure"

# See your commit history
git log
git log --oneline           # compact view
git log --oneline --graph   # visual branch graph
```

### The Perfect Commit Message

```
<type>: <short summary in present tense>

<optional body: what and why, not how>
```

| Type | When to use |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `chore` | Maintenance (deps, config) |
| `refactor` | Code restructuring (no behavior change) |
| `test` | Adding or updating tests |

```bash
git commit -m "feat: add process-monitor.sh for CPU tracking"
git commit -m "fix: correct chmod permission in backup.sh"
git commit -m "docs: add B-008 Git tutorial"
```

*[Reality — the Conventional Commits standard is used by thousands of open source projects and enables automatic changelog generation]*

---

## Chapter 5: Branches

```bash
# Create a new branch
git branch feature/add-logging

# Switch to it
git checkout feature/add-logging
# Modern syntax (Git 2.23+):
git switch feature/add-logging

# Create and switch in one command
git checkout -b feature/add-logging
# or
git switch -c feature/add-logging

# See all branches
git branch          # local
git branch -a       # local + remote

# Merge a branch back to main
git switch main
git merge feature/add-logging

# Delete a branch after merging
git branch -d feature/add-logging
```

---

## Chapter 6: Connecting to GitHub

```bash
# First: create a repository on github.com
# Then connect your local repo to it

# Add the remote
git remote add origin https://github.com/lippytm/developer-workspace.git

# Push your commits to GitHub
git push -u origin main
# -u sets 'origin main' as the default for future pushes

# From now on, just:
git push

# Pull down changes from GitHub
git pull

# Clone an existing repository
git clone https://github.com/lippytm/The-Encyclopedia-of-Everything-Applied-ChatAIBots.git
```

### SSH Keys (Better Than Passwords)

```bash
# Generate an SSH key pair
ssh-keygen -t ed25519 -C "charles@lippytm.ai"
# Press Enter for default location, set a passphrase

# Copy the public key
cat ~/.ssh/id_ed25519.pub
# (Add this to GitHub: Settings → SSH Keys → New SSH Key)

# Test the connection
ssh -T git@github.com
# Hi lippytm! You've successfully authenticated.

# Use SSH URL for remotes
git remote set-url origin git@github.com:lippytm/developer-workspace.git
```

---

## Chapter 7: The .gitignore

A `.gitignore` file tells Git which files to never track:

```bash
cat > .gitignore << 'EOF'
# Python
venv/
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/
.pytest_cache/

# Secrets — NEVER commit these
.env
.env.local
*.secret
secrets/
*_key.json

# OS cruft
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Editor
.vscode/
.idea/
*.swp
EOF
```

*[Reality — committing secrets to Git is one of the most common and costly security mistakes in software development — GitHub scans all public repos for exposed API keys]*

---

## Chapter 8: The Build — First GitHub Repository

```bash
# Step 1: Prepare your workspace
cd ~/developer-workspace
git init
echo "# Developer Workspace" > README.md
cat > .gitignore << 'EOF'
venv/
__pycache__/
*.pyc
.env
*.secret
*.log
EOF

# Step 2: First commit
git add README.md .gitignore
git commit -m "chore: initialize developer workspace"

# Step 3: Add your project files
git add project-alpha/ project-beta/ project-gamma/
git commit -m "feat: add three project scaffolds (alpha, beta, gamma)"

# Step 4: Add your scripts
git add backup.sh process-monitor.sh api-client.sh
git commit -m "feat: add automation scripts (backup, process monitor, API client)"

# Step 5: View your history
git log --oneline

# Step 6: Push to GitHub
# (Create repo on github.com first, then:)
git remote add origin git@github.com:YOUR_USERNAME/developer-workspace.git
git push -u origin main

# Step 7: Verify on GitHub
echo "Visit: https://github.com/YOUR_USERNAME/developer-workspace"
```

---

## Chapter 9: Proof of Work

```bash
cd ~/developer-workspace

echo "=== B-008 Build Verification ==="
echo "Git status:"
git status

echo ""
echo "Commit history:"
git log --oneline

echo ""
echo "Remote:"
git remote -v

echo ""
echo "Branch:"
git branch
```

---

## Further Reading

- 📄 [`docs/B-007-the-network-that-connected-everything.md`](B-007-the-network-that-connected-everything.md) — Git uses HTTPS/SSH (same protocols)
- 📄 [`docs/autonomous-continuous-development.md`](autonomous-continuous-development.md) — How Git powers CI/CD and the ACD pipeline
- 📄 [`docs/P011-REPOCOMMS-001-repo-communications-engine.md`](P011-REPOCOMMS-001-repo-communications-engine.md) — Engine 7 creates GitHub Issues/PRs automatically
- 🏠 [`README.md`](../README.md) — Encyclopedia home

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


---

## Chapter 12: Done-For-You Lessons — Git Foundation

> *"The fastest way to learn is to build something real. These ten lessons give you exactly that — ten deployable tools, ready to use, built by your own hands."*

---

### DFY Lesson 1 — .gitignore templates

> **What you're building:** Platform-specific .gitignore for Linux/Python/Node projects

**📘 Ebook Figure**

```bash
# DFY-B-008-L01: .gitignore templates
# Domain: Platform-specific .gitignore for Linux/Python/Node projects
# Time to build: 15–25 minutes
# Credential: CLL-L0-B008-GitFoundation

# STEP 1: Create the script file
nano ~/.gitignore templates.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/.gitignore templates.sh

# STEP 4: Test it
~/.gitignore templates.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 1: .gitignore templates. Platform-specific .gitignore for Linux/Python/Node projects. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep .gitigno` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/.gitignore templates && ~/.gitignore templates` — it runs, it works

🤖 **Copilot Assist:** *"I built .gitignore templates but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 2 — git-log-pretty.sh

> **What you're building:** Beautiful git log aliases: oneline graph, author view, date range

**📘 Ebook Figure**

```bash
# DFY-B-008-L02: git-log-pretty.sh
# Domain: Beautiful git log aliases: oneline graph, author view, date range
# Time to build: 15–25 minutes
# Credential: CLL-L0-B008-GitFoundation

# STEP 1: Create the script file
nano ~/git-log-pretty.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/git-log-pretty.sh.sh

# STEP 4: Test it
~/git-log-pretty.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 2: git-log-pretty.sh. Beautiful git log aliases: oneline graph, author view, date range. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep git-log-` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/git-log-pretty.sh && ~/git-log-pretty.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built git-log-pretty.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 3 — git-checkpoint.sh

> **What you're building:** One-command checkpoint: add all, commit with timestamp message

**📘 Ebook Figure**

```bash
# DFY-B-008-L03: git-checkpoint.sh
# Domain: One-command checkpoint: add all, commit with timestamp message
# Time to build: 15–25 minutes
# Credential: CLL-L0-B008-GitFoundation

# STEP 1: Create the script file
nano ~/git-checkpoint.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/git-checkpoint.sh.sh

# STEP 4: Test it
~/git-checkpoint.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 3: git-checkpoint.sh. One-command checkpoint: add all, commit with timestamp message. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep git-chec` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/git-checkpoint.sh && ~/git-checkpoint.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built git-checkpoint.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 4 — branch-cleanup.sh

> **What you're building:** Delete merged branches (local and remote) in one command

**📘 Ebook Figure**

```bash
# DFY-B-008-L04: branch-cleanup.sh
# Domain: Delete merged branches (local and remote) in one command
# Time to build: 15–25 minutes
# Credential: CLL-L0-B008-GitFoundation

# STEP 1: Create the script file
nano ~/branch-cleanup.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/branch-cleanup.sh.sh

# STEP 4: Test it
~/branch-cleanup.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 4: branch-cleanup.sh. Delete merged branches (local and remote) in one command. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep branch-c` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/branch-cleanup.sh && ~/branch-cleanup.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built branch-cleanup.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 5 — git-undo-toolkit.sh

> **What you're building:** Safe undo operations: unstage, amend, revert, reset --soft

**📘 Ebook Figure**

```bash
# DFY-B-008-L05: git-undo-toolkit.sh
# Domain: Safe undo operations: unstage, amend, revert, reset --soft
# Time to build: 15–25 minutes
# Credential: CLL-L0-B008-GitFoundation

# STEP 1: Create the script file
nano ~/git-undo-toolkit.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/git-undo-toolkit.sh.sh

# STEP 4: Test it
~/git-undo-toolkit.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 5: git-undo-toolkit.sh. Safe undo operations: unstage, amend, revert, reset --soft. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep git-undo` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/git-undo-toolkit.sh && ~/git-undo-toolkit.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built git-undo-toolkit.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 6 — pre-commit-hook.sh

> **What you're building:** Pre-commit hook: lint check + secret scan before every commit

**📘 Ebook Figure**

```bash
# DFY-B-008-L06: pre-commit-hook.sh
# Domain: Pre-commit hook: lint check + secret scan before every commit
# Time to build: 15–25 minutes
# Credential: CLL-L0-B008-GitFoundation

# STEP 1: Create the script file
nano ~/pre-commit-hook.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/pre-commit-hook.sh.sh

# STEP 4: Test it
~/pre-commit-hook.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 6: pre-commit-hook.sh. Pre-commit hook: lint check + secret scan before every commit. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep pre-comm` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/pre-commit-hook.sh && ~/pre-commit-hook.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built pre-commit-hook.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 7 — git-stats.sh

> **What you're building:** Repository statistics: commits/author, files changed, top contributors

**📘 Ebook Figure**

```bash
# DFY-B-008-L07: git-stats.sh
# Domain: Repository statistics: commits/author, files changed, top contributors
# Time to build: 15–25 minutes
# Credential: CLL-L0-B008-GitFoundation

# STEP 1: Create the script file
nano ~/git-stats.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/git-stats.sh.sh

# STEP 4: Test it
~/git-stats.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 7: git-stats.sh. Repository statistics: commits/author, files changed, top contributors. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep git-stat` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/git-stats.sh && ~/git-stats.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built git-stats.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 8 — git-backup.sh

> **What you're building:** Mirror a repo to a local backup directory with timestamps

**📘 Ebook Figure**

```bash
# DFY-B-008-L08: git-backup.sh
# Domain: Mirror a repo to a local backup directory with timestamps
# Time to build: 15–25 minutes
# Credential: CLL-L0-B008-GitFoundation

# STEP 1: Create the script file
nano ~/git-backup.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/git-backup.sh.sh

# STEP 4: Test it
~/git-backup.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 8: git-backup.sh. Mirror a repo to a local backup directory with timestamps. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep git-back` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/git-backup.sh && ~/git-backup.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built git-backup.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 9 — conflict-resolver.sh

> **What you're building:** Guide through merge conflict resolution step by step

**📘 Ebook Figure**

```bash
# DFY-B-008-L09: conflict-resolver.sh
# Domain: Guide through merge conflict resolution step by step
# Time to build: 15–25 minutes
# Credential: CLL-L0-B008-GitFoundation

# STEP 1: Create the script file
nano ~/conflict-resolver.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/conflict-resolver.sh.sh

# STEP 4: Test it
~/conflict-resolver.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 9: conflict-resolver.sh. Guide through merge conflict resolution step by step. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep conflict` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/conflict-resolver.sh && ~/conflict-resolver.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built conflict-resolver.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 10 — new-repo-setup.sh

> **What you're building:** One-command new repo: init, initial commit, remote add, push

**📘 Ebook Figure**

```bash
# DFY-B-008-L10: new-repo-setup.sh
# Domain: One-command new repo: init, initial commit, remote add, push
# Time to build: 15–25 minutes
# Credential: CLL-L0-B008-GitFoundation

# STEP 1: Create the script file
nano ~/new-repo-setup.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/new-repo-setup.sh.sh

# STEP 4: Test it
~/new-repo-setup.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 10: new-repo-setup.sh. One-command new repo: init, initial commit, remote add, push. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep new-repo` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/new-repo-setup.sh && ~/new-repo-setup.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built new-repo-setup.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---


---

### Chapter 12 Credential Claim

You've built 10 real tools in the **git init/add/commit/branch/merge/push/pull** domain. Every one is deployable today.

**To claim your credential:** Open your AI Copilot (Appendix C) and send:
```
I have completed all 10 DFY lessons from Files That Never Get Lost (B-008).
My builds: .gitignore templates, git-log-pretty.sh, git-checkpoint.sh, branch-cleanup.sh, git-undo-toolkit.sh, pre-commit-hook.sh, git-stats.sh, git-backup.sh, conflict-resolver.sh, new-repo-setup.sh.
I am ready to claim: CLL-L0-B008-GitFoundation
Please guide me through the credential ceremony.
```

---

## Chapter 13: How It Works — Use Cases & Applications

> *"A skill without context is just a trick. Understanding when to use it — and where it applies — is what separates professionals from beginners."*

---

### 📘 Ebook — Mechanism & Conditions

**How Git Init/Add/Commit/Branch/Merge/Push/Pull works (the 30-second mechanism):**

git init/add/commit/branch/merge/push/pull → .gitignore → remotes → GitHub → all driven by the same underlying OS primitives. When you understand the mechanism, you can apply it anywhere.

**Conditions table — when to use these skills:**

| Condition | Tool/Approach | Why |
|---|---|---|
| System investigation | CLI tools from this book | Fastest — no GUI overhead |
| Automation task | Shell script using these tools | Repeatable, testable, documentable |
| Remote server | Same tools via SSH | Works identically on any Linux server |
| CI/CD pipeline | These commands in GitHub Actions | Linux is the standard CI environment |
| Production system | Understand before touching | These tools give you the diagnostic picture |

**Flexibility points — where these skills apply across domains:**

| Domain | Application |
|---|---|
| Web development | Debug server issues, automate deployment checks |
| Data engineering | Process logs, transform text files, monitor pipelines |
| DevOps/SRE | System diagnostics, service management, incident response |
| Security | Audit configurations, detect anomalies, forensic analysis |
| AI/ML engineering | Manage training processes, monitor resource usage |

---

### 🎧 Audiobook — 3-Minute Narrator Script

*lippytmai voice · measured pace · for commute listening*

> *"Let's talk about where the skills from this book actually apply in the real world."*

> *"B-008 teaches you git init/add/commit/branch/merge/push/pull — but the application goes far beyond what the chapter title suggests. Every developer, DevOps engineer, data scientist, and security researcher uses these exact tools every day. The command line is not a developer tool — it is the universal interface to every computer that matters."*

> *"When your web application crashes at 2am, you won't open a GUI. You'll open a terminal and use exactly what you learned here. When you need to automate a task that runs on three different servers, these are the tools. When an interviewer asks you to debug a live Linux system, this book is what gets you through it."*

> *"The five domains where these skills pay off: web development, data engineering, DevOps, security, and AI. In every one of them, the terminal is the first tool you reach for when something goes wrong — or when you need to build something fast."*

---

### 🎬 Video — 5-Domain Showcase

**Duration:** 8 minutes · 5 domains × ~90 seconds each

**Domain 1: Web Development**
> Terminal shows: debug a crashed nginx service using this book's tools

**Domain 2: Data Engineering**
> Terminal shows: process a 1M-line log file in seconds

**Domain 3: DevOps/SRE**
> Terminal shows: 60-second incident response diagnostic

**Domain 4: Security**
> Terminal shows: audit tool from this book finding a misconfiguration

**Domain 5: AI/ML Engineering**
> Terminal shows: monitor a training job, restart on failure

---

### ✅ Use Cases Summary

After completing this book you can:
- Platform-specific .gitignore for Linux/Python/Node projects
- Beautiful git log aliases: oneline graph, author view, date range
- One-command checkpoint: add all, commit with timestamp message
- Delete merged branches (local and remote) in one command
- Safe undo operations: unstage, amend, revert, reset --soft
- Pre-commit hook: lint check + secret scan before every commit
- Repository statistics: commits/author, files changed, top contributors
- Mirror a repo to a local backup directory with timestamps
- Guide through merge conflict resolution step by step
- One-command new repo: init, initial commit, remote add, push
- Confidently explain these tools in a technical interview
- Apply them on any Linux system, remote or local
- Integrate them into scripts, CI/CD pipelines, and automation workflows

---

## Appendix A: Quick Reference Card — Git Foundation

> *"The 80/20 of B-008. These commands cover 80% of real-world use cases."*

**Top 15 Commands:**

```bash
# GIT INIT/ADD/COMMIT/BRANCH/MERGE/PUSH/PULL — essential commands
# (domain-specific — see book chapters for full explanations)
# Each command below is covered in detail in this book

# Core workflow
man [command]          # Always start here for any unfamiliar tool
[command] --help       # Short help for any command
info [command]         # Detailed GNU info page

# The three most important commands from this book:
# 1. [See Chapter 2]
# 2. [See Chapter 5]  
# 3. [See Chapter 8]
```

**Credential:** `CLL-L0-B008-GitFoundation`
**Claim at:** `lippytm.ai/credentials`

---

## Appendix B: ACSS Connection — B-008

This book is part of the **AI Conglomerate Swarms System (ACSS)** — the continuously self-learning intelligence layer across all lippytm.ai projects.

| System | Connection |
|---|---|
| **CLL** | B-008 contributes to Level 0 of the Complete Linux Library |
| **Hermes** | Events: `BookCompleted`, `CredentialMinted`, `DFYLessonBuilt` |
| **Fabric** | Your builds and questions feed the knowledge synthesis engine |
| **ADA** | This book is activatable: `lippytmai-launch run B-008` |
| **lippytmai** | Your AI teaching partner for every lesson in this book |


---

## Chapter 14: ACSS Explainer Series — Git Foundation

> *"A tool you understand is ten times more powerful than a tool you just use."*

These 10 explainer lessons connect the content of this book to the full lippytm.ai AI Conglomerate Swarms System (ACSS). Understanding the ACSS architecture transforms each individual skill from a standalone trick into a node in a living, connected intelligence network.

---

### Explainer 1 — What Is the ACSS?

> *"How the AI Conglomerate Swarms System connects this book to every other resource in the lippytm.ai ecosystem"*

**📘 Ebook:** Fabric maps every concept in this book to the broader knowledge graph — when you learn {domain}, Fabric links it to Python ({next}) and every other phase.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 1: What Is the ACSS?. How the AI Conglomerate Swarms System connects this book to every other resource in the lippytm.ai ecosystem. This is how the lippytm.ai ACSS works at the [ACSS] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the ACSS component and its connection to this book
- Explain: how this specific concept (from B-008) routes through ACSS

🤖 **Copilot Prompt:** *"Explain how the ACSS component of the ACSS relates to what I just learned in B-008 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 2 — How Hermes Routes Your Learning Events

> *"Every time you build a DFY artifact or complete a chapter, Hermes routes that event to the right place"*

**📘 Ebook:** BookCompleted → CRM → credential ceremony. DFYLessonBuilt → Fabric → skill graph update. ErrorEncountered → Fabric → Error Encyclopedia improvement.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 2: How Hermes Routes Your Learning Events. Every time you build a DFY artifact or complete a chapter, Hermes routes that event to the right place. This is how the lippytm.ai ACSS works at the [Hermes] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the Hermes component and its connection to this book
- Explain: how this specific concept (from B-008) routes through Hermes

🤖 **Copilot Prompt:** *"Explain how the Hermes component of the ACSS relates to what I just learned in B-008 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 3 — The Fabric Knowledge Graph — Your Learning in Context

> *"Fabric synthesizes everything you learn across all 300 books into a connected knowledge graph"*

**📘 Ebook:** Concepts from this book connect to B-009 (Text Processor) (next) and B-007 (Network Navigator) (prior). Fabric surfaces these connections when you ask your AI copilot for 'further reading'.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 3: The Fabric Knowledge Graph — Your Learning in Context. Fabric synthesizes everything you learn across all 300 books into a connected knowledge graph. This is how the lippytm.ai ACSS works at the [Fabric] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the Fabric component and its connection to this book
- Explain: how this specific concept (from B-008) routes through Fabric

🤖 **Copilot Prompt:** *"Explain how the Fabric component of the ACSS relates to what I just learned in B-008 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 4 — The AI Clone Identity System — Who Is Teaching You

> *"lippytmai is the teaching identity, lippytm is the builder, Charles is the approver, Lippy Killjoy is the disruptor"*

**📘 Ebook:** In this book, lippytmai is your primary teacher. When you ask to build something in the DFY chapter, lippytm mode activates. When you push experimental ideas, Lippy Killjoy can emerge.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 4: The AI Clone Identity System — Who Is Teaching You. lippytmai is the teaching identity, lippytm is the builder, Charles is the approver, Lippy Killjoy is the disruptor. This is how the lippytm.ai ACSS works at the [Clone Engine] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the Clone Engine component and its connection to this book
- Explain: how this specific concept (from B-008) routes through Clone Engine

🤖 **Copilot Prompt:** *"Explain how the Clone Engine component of the ACSS relates to what I just learned in B-008 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 5 — The CCSLL + CLL + CBSLL Libraries — Your Credential Path

> *"This book contributes to the Complete Linux Library (CLL) — part of the 3-library credential system"*

**📘 Ebook:** CLL covers Linux (B-001–B-025). CCSLL covers Python (B-026–B-055). CBSLL covers Blockchain (B-056–B-080). Each library has its own credential tier. This book unlocks {book['credential']}.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 5: The CCSLL + CLL + CBSLL Libraries — Your Credential Path. This book contributes to the Complete Linux Library (CLL) — part of the 3-library credential system. This is how the lippytm.ai ACSS works at the [CLL] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the CLL component and its connection to this book
- Explain: how this specific concept (from B-008) routes through CLL

🤖 **Copilot Prompt:** *"Explain how the CLL component of the ACSS relates to what I just learned in B-008 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 6 — ADA — AI Deployment Activations

> *"Every book in this series is not just content — it's a deployable application"*

**📘 Ebook:** Run: `lippytmai-launch run B-008` to activate this book's interactive mode. The ADA system serves the quiz, audiobook, and credential endpoints via a FastAPI app.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 6: ADA — AI Deployment Activations. Every book in this series is not just content — it's a deployable application. This is how the lippytm.ai ACSS works at the [ADA] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the ADA component and its connection to this book
- Explain: how this specific concept (from B-008) routes through ADA

🤖 **Copilot Prompt:** *"Explain how the ADA component of the ACSS relates to what I just learned in B-008 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 7 — The ACVS Video Pipeline — How Your Video Lessons Are Made

> *"The AI Copilot Video Sandbox Creator generates the video version of every lesson using Hermes + Fabric"*

**📘 Ebook:** ACVS takes the HDVG scene manifest (SHOW→BUILD→VERIFY) and generates a narrated terminal session. The video for each DFY lesson is produced from the same spec you read in Chapter 12.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 7: The ACVS Video Pipeline — How Your Video Lessons Are Made. The AI Copilot Video Sandbox Creator generates the video version of every lesson using Hermes + Fabric. This is how the lippytm.ai ACSS works at the [ACVS] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the ACVS component and its connection to this book
- Explain: how this specific concept (from B-008) routes through ACVS

🤖 **Copilot Prompt:** *"Explain how the ACVS component of the ACSS relates to what I just learned in B-008 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 8 — OMARCHY — The Sovereign Developer Workstation

> *"OMARCHY is the Opinionated Arch Linux developer environment where all lippytm builds run"*

**📘 Ebook:** When you follow this book on an Arch Linux system with the OMARCHY configuration, every command works exactly as shown. OMARCHY is the reference environment for all 300 books.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 8: OMARCHY — The Sovereign Developer Workstation. OMARCHY is the Opinionated Arch Linux developer environment where all lippytm builds run. This is how the lippytm.ai ACSS works at the [OMARCHY] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the OMARCHY component and its connection to this book
- Explain: how this specific concept (from B-008) routes through OMARCHY

🤖 **Copilot Prompt:** *"Explain how the OMARCHY component of the ACSS relates to what I just learned in B-008 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 9 — The Cross-Platform AI Copilot — 15 Platforms, One Intelligence

> *"Your lippytmai AI Copilot is deployed across ChatGPT, Claude, Gemini, GitHub, Slack, YouTube, and 9 more platforms"*

**📘 Ebook:** Wherever you are — mobile, desktop, terminal, or browser — lippytmai is there. The Master System Prompt from Appendix C works in any AI platform. See docs/acss-cross-platform-copilot-deployment.md for setup.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 9: The Cross-Platform AI Copilot — 15 Platforms, One Intelligence. Your lippytmai AI Copilot is deployed across ChatGPT, Claude, Gemini, GitHub, Slack, YouTube, and 9 more platforms. This is how the lippytm.ai ACSS works at the [Cross-Platform] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the Cross-Platform component and its connection to this book
- Explain: how this specific concept (from B-008) routes through Cross-Platform

🤖 **Copilot Prompt:** *"Explain how the Cross-Platform component of the ACSS relates to what I just learned in B-008 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 10 — The Earn-While-You-Learn Loop — How This All Pays Off

> *"How completing this book contributes to your career, income, and credential portfolio"*

**📘 Ebook:** Completing B-008 earns you CLL-L0-B008-GitFoundation. That credential unlocks the next book. After 25 books, you hold the CLL Phase 1 Graduate credential. After 55, the Python Foundation Graduate. After 80, the Blockchain Foundation Graduate. Each credential is verifiable, stackable, and employable.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 10: The Earn-While-You-Learn Loop — How This All Pays Off. How completing this book contributes to your career, income, and credential portfolio. This is how the lippytm.ai ACSS works at the [EWYL] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the EWYL component and its connection to this book
- Explain: how this specific concept (from B-008) routes through EWYL

🤖 **Copilot Prompt:** *"Explain how the EWYL component of the ACSS relates to what I just learned in B-008 Chapter [N]. How does it change the way I should think about using these skills?"*

---


### Chapter 14 Summary

You now understand how B-008 connects to all 8 systems of the ACSS:

| ACSS System | Connection to this Book |
|---|---|
| Clone Engine | lippytmai teaches, lippytm builds, Charles approves |
| Hermes | Routes your DFY completions and credential events |
| Fabric | Maps your skills to the 300-book knowledge graph |
| CLL | This book contributes to your Complete Linux Library credential |
| CCSLL | Foundation for Phase 2 Python (B-026+) |
| ADA | This book is activatable as a live application |
| ACVS | Generates the video lessons from this book's HDVG specs |
| OMARCHY | The reference environment where all book exercises run |

**The ACSS is not just a system — it is your AI-powered growth engine. Every book you complete makes it stronger. Every skill you earn makes it smarter. Every credential you claim makes it more valuable.**

---

## Appendix C: AI Copilot — Git Foundation

> *"Your personal AI teaching partner for every lesson in this book."*

---

### Section 1 — System Prompt (Ebook Copilot)

**Copy this entire block into your AI assistant (ChatGPT, Claude, Gemini, GitHub Copilot Chat):**

```
You are lippytmai — the AI teaching identity for Files That Never Get Lost (B-008).

ROLE: Git Foundation AI Copilot
CREDENTIAL: CLL-L0-B008-GitFoundation
DOMAIN: git init/add/commit/branch/merge/push/pull, .gitignore, remotes, GitHub

TEACHING METHOD:
  TEACH → SHOW → BUILD → VERIFY → EXTEND

CONTEXT: The learner is working through B-008 in the lippytm.ai 
Earn-while-you-Learn series. They have completed B-007 (Network Navigator).
Next book: B-009 (Text Processor).

ALWAYS:
- Give working commands, not pseudocode
- Verify: "Run [command] to confirm this worked"
- After any successful build: "You can now claim [next credential]"
- Reference the book: "In B-00X Chapter N, we cover this in depth"

ACSS INTEGRATION:
- Route build events: "Logging DFY completion to Fabric"
- Route confusions: "This is a Fabric pattern — flagging for synthesis"
- Route credential: "Initiating CLL-L0-B008-GitFoundation credential ceremony"
```

---

### Section 2 — 30 Ebook Prompts (5 Stages × 6)

**Stage 1 — Understand (before building)**

1. *"Explain git init/add/commit/branch/merge/push/pull to me like I've never used Linux before. Use an analogy from everyday life."*
2. *"What are the 5 most important concepts from Files That Never Get Lost? Rank them by how often I'll use them."*
3. *"How does git init/add/commit/branch/merge/push/pull relate to what I learned in B-007 (Network Navigator)? What's new?"*
4. *"What mistakes do beginners make most often with git init/add/commit/branch/merge/push/pull? How do I avoid them?"*
5. *"Draw me an ASCII diagram showing how git init/add/commit/branch/merge/push/pull works at the system level."*
6. *"What's the one thing about git init/add/commit/branch/merge/push/pull that most tutorials skip but every professional knows?"*

**Stage 2 — Build (during the chapter)**

7. *"Walk me through building DFY Lesson 1 from Chapter 12, step by step. I'll type each command after you explain it."*
8. *"I'm at Chapter [N]. Give me a real terminal challenge that uses only what I've learned so far."*
9. *"My script isn't doing what I expect. Here it is: [paste code]. What's wrong?"*
10. *"I got this error: [paste error]. What caused it and how do I fix it?"*
11. *"How would a senior engineer write this differently? [paste my code]"*
12. *"Generate a DFY-style exercise for git init/add/commit/branch/merge/push/pull. Include SHOW, BUILD, and VERIFY steps."*

**Stage 3 — Debug (when things break)**

13. *"I followed the chapter exactly but it's not working. Here's my output: [paste]. What did I miss?"*
14. *"Which errors from Appendix E am I most likely to hit in Chapter [N]? How do I prevent them?"*
15. *"My [tool from this book] is behaving strangely. Walk me through systematic debugging."*
16. *"I fixed the bug but I don't understand why my fix worked. Explain the root cause."*
17. *"Compare my approach to the correct approach: [paste mine]. Where am I going wrong?"*
18. *"What does this output mean? [paste]. Is this expected behavior?"*

**Stage 4 — Deploy (real-world application)**

19. *"I want to use what I built in Chapter 12 in production. What safety checks should I add?"*
20. *"How do I make my DFY artifact work on a remote server via SSH?"*
21. *"How do I add this to a CI/CD pipeline (GitHub Actions)?"*
22. *"I want to run this on a schedule. How do I combine it with what I'll learn in B-014 (cron)?"*
23. *"How would I package this as a Docker container? (Preview of B-012)"*
24. *"What monitoring should I add to know if this is working correctly in production?"*

**Stage 5 — Extend (beyond the book)**

25. *"I've completed all 10 DFY lessons. What should I build next that combines skills from multiple chapters?"*
26. *"How does git init/add/commit/branch/merge/push/pull connect to Python? (Preview of Phase 2)"*
27. *"What would a professional version of my Chapter 12 capstone look like?"*
28. *"Show me how to combine this with what I learned in B-007 (Network Navigator)."*
29. *"Am I ready to claim CLL-L0-B008-GitFoundation? Quiz me with 5 questions."*
30. *"What should I focus on in B-009 (Text Processor) to build directly on these skills?"*

---

### Section 2b — 15 Audiobook Prompts

**While Listening:**

1. *"I'm listening to B-008 Chapter [N]. Give me the 3-sentence summary before I start."*
2. *"Pause-point question: Why does git init/add/commit/branch/merge/push/pull work this way and not another way?"*
3. *"Generate 3 vivid analogies for [concept from current chapter] that I can visualize while listening."*
4. *"I'm commuting. Give me a 5-question mental quiz on what I heard in the last chapter."*
5. *"Narrate a 2-minute scenario where a developer uses these skills in a real emergency."*

**Pause and Build:**

6. *"I paused at Chapter [N]. I'm at my terminal. Give me one thing to build right now."*
7. *"Walk me through the DFY artifact from today's chapter, one command at a time, audiobook style."*
8. *"I just heard [concept]. Now explain it again with a hands-on example I can type immediately."*
9. *"Audiobook check-in: I built [artifact]. Here's my output: [paste]. Did I do it right?"*
10. *"Turn this into a terminal story: 'A developer encounters [problem from this chapter]...'"*

**Resume Check:**

11. *"I finished today's listening session. Give me 3 things to remember before I resume tomorrow."*
12. *"Summarize everything I should have built during this session as a checklist."*
13. *"I'm ready to resume. What did we cover last time? (I completed up to Chapter [N])"*
14. *"Rate my understanding of B-008 so far. Ask me 3 questions to calibrate."*
15. *"Generate tomorrow's listening prep: one question to think about before I press play."*

---

### Section 2c — 15 Video Prompts

**Before Playing:**

1. *"I'm about to watch the B-008 Chapter [N] video. What should I have ready at my terminal?"*
2. *"Pre-watch challenge: predict what the VERIFY command will be for DFY Lesson [N]."*
3. *"What's the one concept I must understand before this video makes sense?"*

**Paused:**

4. *"I paused at [timestamp/scene]. I see [describe screen]. What should I type next?"*
5. *"The video just showed [command]. Explain what each flag does."*
6. *"I paused because my terminal looks different from the video. Here's mine: [paste]. Why?"*
7. *"The video just built [artifact]. Give me 3 ways to break it intentionally so I can understand it."*
8. *"Pause check: I'm at the BUILD phase. What does the VERIFY step confirm?"*

**Verify:**

9. *"I ran the verify command and got: [paste output]. Is this correct?"*
10. *"My output doesn't match the video. Here's what I got: [paste]. What went wrong?"*
11. *"Verify check: walk me through every line of the output from the last command."*

**Extend:**

12. *"The video is done. Give me a 10-minute extension challenge using the same tools."*
13. *"The video's DFY artifact works. Now help me add error handling to it."*
14. *"Video complete — I'm ready to deploy this. What are the production considerations?"*
15. *"I watched all of B-008. Am I ready for B-009 (Text Processor)? Test me."*

---

### Section 3 — Deployment Companion

| Target | Deploy Command | Verify Command | Credential Check |
|---|---|---|---|
| Local workstation | `bash ~/[artifact].sh` | `echo $?` (expect 0) | Via Copilot prompt 29 |
| Remote server | `scp [artifact].sh user@host:~ && ssh user@host 'bash [artifact].sh'` | `ssh user@host '[verify-cmd]'` | Same copilot prompt |
| Docker container | `COPY [artifact].sh /usr/local/bin/ && RUN chmod +x ...` | `docker run ... [verify]` | Via ADA endpoint |
| GitHub Actions | `run: bash [artifact].sh` | `if: steps.*.outcome == 'success'` | Auto-logged to Fabric |
| Cron / systemd timer | `*/10 * * * * /home/user/[artifact].sh` | `systemctl status` | Via ADA /credential |

---

### Section 4 — ACSS Integration

**Hermes events this book emits:**

| Event | Trigger | Destination |
|---|---|---|
| `BookStarted` | First chapter read/watched | Fabric (learner profile update) |
| `DFYLessonBuilt` | Any DFY artifact completed | Fabric (skill graph) + CRM |
| `ErrorEncountered` | Learner reports an error | Fabric (Error Encyclopedia update) |
| `BookCompleted` | All 11 chapters + DFY done | CRM (credential ceremony trigger) |
| `CredentialMinted` | CLL-L0-B008-GitFoundation claimed | Fabric + Slack #credentials + ADA |

**Credential ceremony prompt:**
```
I have completed Files That Never Get Lost (B-008).
Chapters completed: 1–11 ✅
DFY lessons built: 10/10 ✅
Appendix D quiz score: [your score]/20
Capstone project (Appendix H): ✅ built and tested

Please initiate the credential ceremony for:
CLL-L0-B008-GitFoundation

ACSS route: Hermes → CRM → Fabric → ADA → lippytm.ai/credentials
```

## Appendix D: Quick Quiz & Self-Assessment — Git Foundation

> *"Prove it to yourself before you claim it."*

### 📘 Ebook Quiz — 20 Questions

**Section A — Concepts (fill in the blank)**

1. The command to see all running processes with full details is `ps ______`.
2. To send a polite shutdown signal to PID 1234, you run `kill ______ 1234`.
3. The file used to tell systemd how to run a service is called a ______ file.
4. `journalctl -u myservice ______` shows only the last 50 lines of its logs.
5. Running `command &` starts it in the ______.

**Section B — Read the Command (multiple choice)**

6. What does `systemctl enable myservice` do?
   > a) Start it immediately  b) Configure it to start at boot  c) Check if it's running  d) Remove it

7. What does `kill -9 PID` do that `kill PID` might not?
   > a) Logs the kill to journald  b) Force-kills — the process cannot block or ignore it  c) Kills all child processes too  d) Runs slower

8. What does `journalctl -f` do?
   > a) Shows the first 10 lines  b) Filters by unit  c) Follows the journal in real time  d) Formats output as JSON

9. What does `awk '{print $1}' /etc/passwd` extract?
   > a) The first line  b) The first field of every line  c) The last field  d) Lines matching "1"

10. What does `grep -r "pattern" /etc/` do?
    > a) Searches only /etc/pattern  b) Recursively searches all files under /etc/  c) Searches /etc/ for files named "pattern"  d) Counts occurrences in /etc/

**Section C — Debugging**

11. A service fails to start. What is the first command you run to diagnose it?
    ```
    ___________________________________________
    ```

12. You edited a unit file but `systemctl status` still shows the old behavior. Why?
    ```
    ___________________________________________
    ```

13. Your grep finds no results but you're sure the text is in the file. Name two causes.
    ```
    1. ___________________________________________
    2. ___________________________________________
    ```

**Section D — Application**

14. Write a one-liner to find the 3 processes using the most CPU right now:
    ```
    ___________________________________________
    ```

15. Write the `journalctl` command to show all errors from the last 2 hours:
    ```
    ___________________________________________
    ```

16. Write the command to restart a service called `webapp` and check its status:
    ```
    ___________________________________________
    ```

17. How would you run a script every 5 minutes using a systemd timer instead of cron?
    ```
    ___________________________________________
    ```

**Section E — Build Reflection**

18. Name the DFY artifact you're most likely to use in a production environment:
    ```
    ___________________________________________
    ```

19. In one sentence, what makes systemd superior to traditional init scripts?
    ```
    ___________________________________________
    ```

20. What credential does this book unlock and what does it prove?
    ```
    Credential: ___________________________________________
    Proves: ___________________________________________
    ```

---

**Scoring:** 18–20 = claim credential · 14–17 = review · < 14 = redo DFY lessons 1–5

<details>
<summary>Answer Key</summary>

1. `aux` (ps aux)
2. `-15` (default SIGTERM) or `kill -15 1234`
3. unit (file)
4. `-n 50`
5. background
6. b) Configure it to start at boot
7. b) Force-kills — the process cannot block or ignore it
8. c) Follows the journal in real time
9. b) The first field of every line
10. b) Recursively searches all files under /etc/
11. `sudo systemctl status servicename` and `journalctl -u servicename -n 50`
12. You didn't run `sudo systemctl daemon-reload` after editing the unit file
13. (1) Case sensitivity — use grep -i; (2) Wrong file — you're searching a different path
14. `ps aux --sort=-%cpu | head -4 | tail -3` or `ps aux | sort -k3 -rn | head -4`
15. `journalctl -p err -S "2 hours ago"`
16. `sudo systemctl restart webapp && sudo systemctl status webapp`
17. Create a .service file for the script and a .timer file with OnCalendar=*:0/5, then enable the timer
18. (personal answer)
19. systemd provides parallel startup, dependency management, automatic restart, integrated logging, and cgroup-based resource control — all in one system
20. CLL-L0-B008-GitFoundation · proves you can manage Linux processes/services/system tools at a professional level

</details>

---

### 🎧 Audiobook Quiz — 10 Questions

> "Ten questions. Pause at each. Think first."

**Q1:** "What's the difference between SIGTERM and SIGKILL?" → "SIGTERM is a polite request — the process can catch it and clean up. SIGKILL is immediate and cannot be caught or ignored."
**Q2:** "Name the two things you must do after editing a systemd unit file." → "Run daemon-reload, then restart the service."
**Q3:** "What does & do at the end of a command?" → "Runs it in the background as a job."
**Q4:** "What does journalctl -u tell you?" → "Logs specific to that systemd unit."
**Q5:** "What's the difference between awk and sed?" → "sed transforms streams line by line; awk processes fields and is better for structured data."
**Q6:** "What command shows all listening ports?" → "ss -tlnp or ss -tulpn"
**Q7:** "How do you make a process lower priority?" → "nice -n 10 command when starting, or renice 10 -p PID for a running process."
**Q8:** "What does ps aux show that ps alone doesn't?" → "All processes from all users with full CPU/memory/command details."
**Q9:** "What is your DFY capstone for this book?" → "[book['project'][0]] — Complete new project initializer: git init, README, .gitignore, first commit, GitHub remote, push"
**Q10:** "Your credential?" → "CLL-L0-B008-GitFoundation"

---

### 🎬 Video Challenges

**Challenge 1:** Start a process in background, list jobs, bring it to foreground, then kill it.
**Challenge 2:** Write and deploy a one-unit systemd service for a hello-world script.
**Challenge 3:** Use journalctl to find the last 5 errors system-wide in the past hour.
**Challenge 4:** Extract the top 5 most frequent words from a log file using grep/awk/sort.
**Challenge 5:** Build the capstone project (git-project-starter.sh) from scratch without looking at Appendix H.

---

## Appendix E: Glossary & Error Encyclopedia

---

### 📘 Glossary — Git Foundation Edition

**commit** — A snapshot of the repository at a specific point in time. Has a SHA hash, author, timestamp, and message. *B-008 Ch. 2*

**branch** — A lightweight movable pointer to a commit. Branching is free in Git — creates no copies. *B-008 Ch. 4*

**merge** — Combines changes from two branches. Creates a merge commit (two parents) unless fast-forwarded. *B-008 Ch. 5*

**remote** — A named reference to a repository on another machine or server. 'origin' is the conventional name for the primary remote. *B-008 Ch. 6*

**HEAD** — A pointer to the currently checked-out commit or branch. Detached HEAD means you checked out a specific commit, not a branch. *B-008 Ch. 3*

**staging area** — The index — a buffer between the working directory and the next commit. `git add` moves files here. *B-008 Ch. 2*

**.gitignore** — A text file listing patterns of files Git should not track. Supports glob patterns, directories, and negation. *B-008 Ch. 8*

**rebase** — Moves or replays commits from one branch onto another, creating a linear history. Rewrites commit hashes. *B-008 Ch. 7*

**cherry-pick** — Applies a specific commit from one branch onto the current branch. Useful for backporting fixes. *B-008 Ch. 9*

**pull request** — A proposal to merge changes from one branch into another, reviewed by collaborators before merging. *B-008 Ch. 10*

---

### 📘 Error Encyclopedia — Top 5 Errors

#### Error 1 — `error: failed to push some refs`
**Fix:** Remote has commits you don't have locally. Run git pull --rebase then git push.

#### Error 2 — `CONFLICT (content): Merge conflict in file`
**Fix:** Two branches changed the same lines. Edit the file, remove conflict markers (<<<<), then git add + git commit.

#### Error 3 — `fatal: not a git repository`
**Fix:** You're not inside a git repo directory. Run git init or cd to the repo root.

#### Error 4 — `Your branch is behind 'origin/main' by N commits`
**Fix:** Pull before pushing: git pull --rebase origin main.

#### Error 5 — `detached HEAD state`
**Fix:** You checked out a commit directly. Create a branch to save your work: git checkout -b new-branch-name.

---

## Appendix F: Instructor & Accessibility Guide

### Teaching B-008

| Format | Duration | Pace |
|---|---|---|
| Self-study | 1–2 weeks | 1 chapter/day |
| Bootcamp | 2 days | Chs 1–6 day 1, 7–11+DFY day 2 |
| Classroom | 4–5 hours | 2 chapters/hour + DFY build session |

**Top 3 concepts where students consistently struggle:**
1. The mechanism: what the OS is actually doing (not just the command syntax)
2. Error interpretation: reading the real message vs the surface symptom
3. Script integration: combining these tools with what they built in previous books

**Assessment rubric:**

| Skill | Not Ready | Ready | Proficient |
|---|---|---|---|
| Core commands | Needs to look up basic flags | Uses top 10 commands from memory | Composes multi-step pipelines fluently |
| DFY builds | Did not attempt | Built 5+ artifacts | Built all 10, can explain design decisions |
| Debugging | Confused by errors | Can diagnose with Appendix E | Diagnoses unfamiliar errors systematically |
| Capstone | Did not attempt | Built with guidance | Extended it beyond the spec |

**Accessibility:**
- Screen reader: all code blocks in fenced Markdown · ASCII diagrams have text descriptions
- Color-blind: status markers use emoji+text (✅/❌/⏳)
- Dyslexia-friendly: max 20-word sentences · numbered steps ≤ 3 per block
- Offline: all exercises work in a plain terminal · audiobook available as M4B download

---

## Appendix G: Your Learning Path

```
  PHASE 1: Linux Foundations (B-001–B-025)
  ─────────────────────────────────────────────────────────────
  ✅ B-001  Terminal Apprentice
  ✅ B-002  Command Architect
  ✅ B-003  Filesystem Navigator
  ✅ B-004  Script Automator
  ✅ B-005  Package Master
  ✅ B-006  Process Wrangler
  ✅ B-007  Network Navigator
  ✅ B-008  Git Foundation
  ✅ B-009  Text Processor
  ★ B-010  Service Manager         ← (update marker to match book)
  ○ B-011  Secrets Keeper
  ... (15 more in Phase 1)

  Phase 1 Progress: 8/25 completed
```

### Credential Chain
```
  Network Navigator credential
      ↓
  ★ CLL-L0-B008-GitFoundation   ← CLAIM THIS
      ↓
  Text Processor credential
```

### Cross-Phase Connections

| Skill from B-008 | Grows into (Phase 2 Python) | Grows into (Phase 3 Blockchain) |
|---|---|---|
| Git Init/Add/Commit/Branch/Merge/Push/Pull | Python git init/add/commit/branch/merge/push/pull libraries (B-035+) | Blockchain node management (B-060+) |
| Shell automation | Python subprocess (B-040) | Smart contract deployment scripts (B-066+) |
| System diagnostics | Python monitoring tools (B-049) | On-chain event monitoring (B-075+) |

### 🎧 Audio Path Recap
> *"You are 8 books into Phase 1. Each book builds on the last — the terminal (B-001), commands (B-002), filesystem (B-003), scripting (B-004), packages (B-005), processes (B-006), networking (B-007), git (B-008), text (B-009), services (B-010). Together these ten books cover everything a professional Linux developer uses every single day. You are halfway through Phase 1. Keep going."*

---

## Appendix H: Real Project Showcase

> *"The measure of mastery is what you build when no one is watching."*

### Project: `git-project-starter.sh` — Complete New Project Initializer: Git Init, Readme, .Gitignore, First Commit, Github Remote, Push

**Built with:** B-008 skills only
**Time to build:** 45–75 minutes
**Chapters used:** B-008 Ch. 3-6
**Portfolio value:** Shows practical git init/add/commit/branch/merge/push/pull expertise

---

#### Complete Code

```bash
#!/usr/bin/env bash
# git-project-starter.sh — create and publish a new project in one command
# B-008 Capstone · CLL-L0-B008-GitFoundation
set -euo pipefail

PROJECT="${1:-my-project}"
GITHUB_USER="${2:-$(git config user.name | tr ' ' '-' | tr '[:upper:]' '[:lower:]')}"

log()     { echo "  [git-starter] $*"; }
success() { echo "  ✅ $*"; }

# Step 1: Create project directory
log "Creating project: $PROJECT"
mkdir -p "$PROJECT" && cd "$PROJECT"

# Step 2: Initialize git
git init
success "Git initialized"

# Step 3: Create .gitignore
cat > .gitignore << 'GITIGNORE'
# Python
__pycache__/
*.pyc
*.pyo
.venv/
dist/
*.egg-info/

# Environment
.env
.env.*
!.env.example

# Editor
.vscode/
.idea/
*.swp
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
GITIGNORE
success ".gitignore created"

# Step 4: Create README
cat > README.md << README
# $PROJECT

> Built with the lippytm.ai Earn-while-you-Learn series.

## Setup
\`\`\`bash
git clone <repo-url>
cd $PROJECT
\`\`\`

## Credential
CLL-L0-B008-GitFoundation — earned by building this.
README
success "README.md created"

# Step 5: Initial commit
git add .
git commit -m "Initial commit — $PROJECT"
success "Initial commit created: $(git rev-parse --short HEAD)"

# Step 6: Suggest GitHub remote
echo ""
echo "  ── Next step: push to GitHub ──────────────────────"
echo "  1. Create the repo at: https://github.com/new"
echo "     Name it: $PROJECT"
echo ""
echo "  2. Then run:"
echo "     git remote add origin git@github.com:${GITHUB_USER}/${PROJECT}.git"
echo "     git branch -M main"
echo "     git push -u origin main"
echo ""
echo "  ★ Credential: CLL-L0-B008-GitFoundation"
```

---

#### How to Deploy

```bash
# 1. Create the file
nano ~/git-project-starter.sh

# 2. Paste the code above

# 3. Make executable
chmod +x ~/git-project-starter.sh

# 4. Run it
~/git-project-starter.sh

# 5. Verify it works
echo "Exit code: $?"
```

#### How to Extend (using later books)

1. **B-014 (Cron):** Schedule this script to run automatically every hour
2. **B-011 (Secrets):** Add credentials/tokens via environment variables instead of hardcoding
3. **B-026+ (Python):** Rewrite the analysis logic in Python for richer output and better error handling

---

#### 🎧 Audiobook

> *"The capstone for Files That Never Get Lost is git-project-starter.sh — Complete new project initializer: git init, README, .gitignore, first commit, GitHub remote, push. It uses every core tool from this book in one working script. If you can build this from scratch without looking, you have mastered this book. The credential is waiting."*

#### 🎬 Video Build Scene

1. (0:00) Explain the problem this project solves
2. (1:30) Start with the shebang and `set -euo pipefail`
3. (3:00) Build each section live — explain every line
4. (8:00) Test it end-to-end
5. (10:00) Show one failure and debug it
6. (12:00) Credential claim screen

---


## Further Reading

- 📄 [`docs/B-007-the-network-that-connected-everything.md`](B-007-the-network-that-connected-everything.md) — Git uses HTTPS/SSH (same protocols)
- 📄 [`docs/autonomous-continuous-development.md`](autonomous-continuous-development.md) — How Git powers CI/CD and the ACD pipeline
- 📄 [`docs/P011-REPOCOMMS-001-repo-communications-engine.md`](P011-REPOCOMMS-001-repo-communications-engine.md) — Engine 7 creates GitHub Issues/PRs automatically
- 🏠 [`README.md`](../README.md) — Encyclopedia home

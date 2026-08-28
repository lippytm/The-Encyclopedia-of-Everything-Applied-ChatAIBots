# B-040: Automation Scripts That Save Hours

### os, subprocess, shutil, pathlib, and the Art of Letting Python Do the Work

> *"The best automation script is the one that eliminates a task you hate doing manually. Python's standard library is a full-featured operating system interface. Once you understand pathlib, shutil, and subprocess, you stop doing things yourself — and start delegating to your computer."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Traverse and manipulate the filesystem using `pathlib`
2. Copy, move, and delete files with `shutil`
3. Run shell commands from Python with `subprocess`
4. Read, write, and watch files with `os` and `pathlib`
5. Build a `file_organizer.py` that automatically sorts and renames files

**Prerequisite:** B-026 through B-039

**Build Artifact:** `~/developer-workspace/projects/python-foundations/file_organizer.py`

**Credential:** `CCSLL-L1-B040-AutomationEngineer` — on-chain on Base

---

## Chapter 1: pathlib — The Modern File System API

```python
from pathlib import Path

# Get common directories
home   = Path.home()          # /home/username
cwd    = Path.cwd()           # /current/working/directory
tmp    = Path("/tmp")

print(home)         # /home/runner
print(home / "projects" / "python-foundations")  # chained with /

# Path components
p = Path("/home/runner/projects/tasks.db")
print(p.name)       # tasks.db
print(p.stem)       # tasks
print(p.suffix)     # .db
print(p.parent)     # /home/runner/projects
print(p.parts)      # ('/', 'home', 'runner', 'projects', 'tasks.db')

# Test existence
p = Path.home() / ".bashrc"
print(p.exists())   # True or False
print(p.is_file())  # True
print(p.is_dir())   # False

# Create directories
new_dir = Path.home() / "projects" / "test_run"
new_dir.mkdir(parents=True, exist_ok=True)   # safe: no error if exists

# Absolute path (resolves symlinks and ..)
relative = Path("../../config.yaml")
print(relative.resolve())
```

---

## Chapter 2: Reading and Writing Files with pathlib

```python
from pathlib import Path

log_path = Path("/tmp/my_run.log")

# Write text (creates or overwrites)
log_path.write_text("First line\nSecond line\n", encoding="utf-8")

# Append mode
with log_path.open("a", encoding="utf-8") as f:
    f.write("Third line\n")

# Read back
content = log_path.read_text(encoding="utf-8")
print(content)

# Read lines
lines = log_path.read_text().splitlines()
print(lines)    # ['First line', 'Second line', 'Third line']

# Read/write bytes
img_path = Path("/tmp/icon.png")
if img_path.exists():
    data = img_path.read_bytes()
    copy_path = Path("/tmp/icon_copy.png")
    copy_path.write_bytes(data)

# File stats
stat = log_path.stat()
print(f"Size:     {stat.st_size} bytes")
print(f"Modified: {stat.st_mtime}")

# Touch (create empty / update timestamp)
Path("/tmp/marker.txt").touch()
```

---

## Chapter 3: Traversing Directories

```python
from pathlib import Path

workspace = Path.home() / "developer-workspace"

# List direct children
for item in workspace.iterdir():
    icon = "📁" if item.is_dir() else "📄"
    print(f"  {icon} {item.name}")

# Recursive glob — find all .py files under workspace
for py_file in workspace.rglob("*.py"):
    print(py_file)

# Non-recursive glob — only in current dir
for md_file in workspace.glob("*.md"):
    print(md_file)

# Pattern: collect all files by extension
def find_by_extension(root: Path, ext: str) -> list[Path]:
    return sorted(root.rglob(f"*{ext}"))

py_files = find_by_extension(workspace, ".py")
print(f"Found {len(py_files)} Python files")

# Get size of all files in a directory tree
def dir_size(root: Path) -> int:
    return sum(f.stat().st_size for f in root.rglob("*") if f.is_file())

print(f"Workspace size: {dir_size(workspace):,} bytes")
```

---

## Chapter 4: shutil — Copy, Move, Delete

```python
import shutil
from pathlib import Path

src = Path("/tmp/test_src.txt")
dst = Path("/tmp/test_dst.txt")
src.write_text("hello world")

# Copy file
shutil.copy2(src, dst)       # copy2 preserves metadata (timestamps)

# Copy directory tree
src_dir = Path("/tmp/source_dir")
dst_dir = Path("/tmp/dest_dir")
src_dir.mkdir(exist_ok=True)
(src_dir / "file.txt").write_text("data")
shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)  # Python 3.8+

# Move file (rename across filesystem)
moved = Path("/tmp/test_moved.txt")
shutil.move(str(dst), str(moved))   # shutil.move accepts str or Path

# Delete a file
src.unlink(missing_ok=True)   # missing_ok prevents error if not found

# Delete directory tree
shutil.rmtree(dst_dir, ignore_errors=True)

# Disk space info
total, used, free = shutil.disk_usage("/")
print(f"Free: {free / (1024**3):.1f} GB")
```

---

## Chapter 5: subprocess — Running Shell Commands

```python
import subprocess

# Run a command and get output
result = subprocess.run(
    ["echo", "Hello from subprocess"],
    capture_output=True,
    text=True,
    check=True    # raise CalledProcessError if non-zero exit
)
print(result.stdout)        # Hello from subprocess
print(result.returncode)    # 0

# Run with shell=True (avoid in production — security risk with user input)
result = subprocess.run("ls -la /tmp | head -5", shell=True, capture_output=True, text=True)
print(result.stdout)

# Pass arguments safely (never concatenate strings — use a list)
filename = "my file.txt"   # has a space — safe only with list form
subprocess.run(["touch", filename])

# Check if a command exists
def command_exists(cmd: str) -> bool:
    return subprocess.run(
        ["which", cmd], capture_output=True
    ).returncode == 0

print(command_exists("python3"))   # True
print(command_exists("cobol"))     # False

# Run git command
def git_status(repo_path: str) -> str:
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()
```

---

## Chapter 6: The Build — File Organizer

```python
#!/usr/bin/env python3
"""
file_organizer.py — B-040 Build Artifact

Automatically sorts and renames files in a directory.
Given a source folder, organizes files into subfolders by type
and timestamps them for easy discovery.

Usage: python3 file_organizer.py [source_dir] [target_dir]
"""
from __future__ import annotations

import shutil
import sys
from datetime import datetime
from pathlib import Path


# Extension → folder mapping
CATEGORIES: dict[str, str] = {
    # Documents
    ".pdf": "documents/pdf",
    ".doc": "documents/word",
    ".docx": "documents/word",
    ".txt": "documents/text",
    ".md": "documents/markdown",
    ".csv": "documents/data",
    ".xlsx": "documents/spreadsheets",
    # Images
    ".jpg": "images",
    ".jpeg": "images",
    ".png": "images",
    ".gif": "images",
    ".svg": "images/vector",
    ".webp": "images",
    # Audio / Video
    ".mp3": "audio",
    ".m4b": "audio/audiobooks",
    ".m4a": "audio",
    ".mp4": "video",
    ".mov": "video",
    ".mkv": "video",
    # Code
    ".py": "code/python",
    ".js": "code/javascript",
    ".ts": "code/typescript",
    ".sol": "code/solidity",
    ".sh": "code/shell",
    ".yaml": "config",
    ".yml": "config",
    ".json": "config",
    ".toml": "config",
    # Archives
    ".zip": "archives",
    ".tar": "archives",
    ".gz": "archives",
}


def categorize(file: Path) -> str:
    """Return the target subfolder for a given file."""
    return CATEGORIES.get(file.suffix.lower(), "other")


def safe_name(file: Path, target_dir: Path) -> Path:
    """Return a unique destination path, appending _N if name conflicts."""
    dest = target_dir / file.name
    if not dest.exists():
        return dest
    stem, suffix = file.stem, file.suffix
    counter = 1
    while dest.exists():
        dest = target_dir / f"{stem}_{counter}{suffix}"
        counter += 1
    return dest


def organize(source: Path, target: Path, dry_run: bool = False) -> dict[str, int]:
    """
    Move all files from source into categorized subfolders under target.
    Returns a count dict: category → files_moved.
    """
    counts: dict[str, int] = {}

    if not source.exists():
        print(f"⚠️  Source does not exist: {source}")
        return counts

    files = [f for f in source.rglob("*") if f.is_file()]
    print(f"\n📂 Organizing {len(files)} files from {source}\n")

    for file in sorted(files):
        category = categorize(file)
        dest_dir = target / category
        dest_file = safe_name(file, dest_dir)

        print(f"  {'[DRY]' if dry_run else 'MOVE'} {file.name:<30} → {category}/")
        if not dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file), str(dest_file))
        counts[category] = counts.get(category, 0) + 1

    return counts


def report(counts: dict[str, int]) -> None:
    print("\n=== Organization Report ===\n")
    total = sum(counts.values())
    for category in sorted(counts):
        bar = "█" * counts[category]
        print(f"  {category:<30} {counts[category]:>3}  {bar}")
    print(f"\n  Total files moved: {total}\n")


def demo(dry_run: bool = True) -> None:
    """Create sample files and run organizer."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "downloads"
        target = Path(tmp) / "organized"
        source.mkdir()

        # Create sample files
        samples = [
            "report_q3.pdf", "budget.xlsx", "notes.md",
            "photo_vacation.jpg", "audio_book.m4b",
            "deploy.sh", "config.yaml", "data.json",
            "video_tutorial.mp4", "archive.zip",
            "unknown_format.xyz",
        ]
        for name in samples:
            (source / name).write_text(f"sample content for {name}")

        print(f"Source: {source}")
        print(f"Target: {target}")

        counts = organize(source, target, dry_run=dry_run)
        report(counts)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        source = Path(sys.argv[1])
        target = Path(sys.argv[2])
        counts = organize(source, target)
        report(counts)
    else:
        print("Running demo mode (no files actually moved)...")
        demo(dry_run=True)
```

```bash
python3 ~/developer-workspace/projects/python-foundations/file_organizer.py
# Or organize a real directory:
# python3 file_organizer.py ~/Downloads ~/organized
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-040 Verification ==="
python3 -c "
from pathlib import Path
import tempfile, shutil

with tempfile.TemporaryDirectory() as tmp:
    p = Path(tmp)
    (p / 'hello.txt').write_text('hello world')
    (p / 'sub').mkdir()
    shutil.copy2(p / 'hello.txt', p / 'sub' / 'copy.txt')
    files = sorted(p.rglob('*.txt'))
    print(f'Found {len(files)} .txt files:')
    for f in files:
        print(f'  {f.name}: {f.read_text()!r}')
print('✅ pathlib + shutil works')
"
```

---

## What's Next: Phase 2 Batch 4 Preview

With B-036–B-040 complete, you have mastered Python's **standard toolkit**:

| Book | Skill |
|---|---|
| B-036 | Type hints + mypy |
| B-037 | Date/time arithmetic |
| B-038 | Regular expressions |
| B-039 | SQLite databases |
| **B-040** | **OS automation** |

**Phase 2 Batch 4 (B-041–B-045)** goes deeper:
- B-041: *JSON and YAML — Configuration as Code* — structured config files
- B-042: *Logging Like a Pro* — logging module, handlers, formatters
- B-043: *Command-Line Interfaces with argparse* — building CLI tools
- B-044: *Concurrency: Threading and Multiprocessing* — parallel execution
- B-045: *Packaging Your Python Project* — setup.py, pyproject.toml, wheel, PyPI

---


## Chapter 12: Done-For-You Lessons — Automation Scripts That Save Hours

> *"Done-for-you means it's already designed, structured, and proven. Your job: execute." — lippytmai*

10 ready-to-use lesson structures for Python Automation using subprocess.

---

### DFY Lesson 1: Introduction to Python Automation

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 01: Introduction to Python Automation         │
│  Book: B-040  Tool: subprocess                 │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 1: Introduction to Python Automation. Master subprocess with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `subprocess` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 1 of B-040: Introduction to Python Automation. Give me 3 progressive exercises."

---
### DFY Lesson 2: Core subprocess Patterns

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 02: Core subprocess Patterns                  │
│  Book: B-040  Tool: subprocess                 │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 2: Core subprocess Patterns. Master subprocess with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `subprocess` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 2 of B-040: Core subprocess Patterns. Give me 3 progressive exercises."

---
### DFY Lesson 3: Three Formats: Ebook, Audiobook, Video

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 03: Three Formats: Ebook, Audiobook, Video    │
│  Book: B-040  Tool: subprocess                 │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 3: Three Formats: Ebook, Audiobook, Video. Master subprocess with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `subprocess` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 3 of B-040: Three Formats: Ebook, Audiobook, Video. Give me 3 progressive exercises."

---
### DFY Lesson 4: Common Mistakes in Python Automation

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 04: Common Mistakes in Python Automation      │
│  Book: B-040  Tool: subprocess                 │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 4: Common Mistakes in Python Automation. Master subprocess with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `subprocess` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 4 of B-040: Common Mistakes in Python Automation. Give me 3 progressive exercises."

---
### DFY Lesson 5: Building a Python Automation Workflow

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 05: Building a Python Automation Workflow     │
│  Book: B-040  Tool: subprocess                 │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 5: Building a Python Automation Workflow. Master subprocess with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `subprocess` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 5 of B-040: Building a Python Automation Workflow. Give me 3 progressive exercises."

---
### DFY Lesson 6: Automating with subprocess

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 06: Automating with subprocess                │
│  Book: B-040  Tool: subprocess                 │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 6: Automating with subprocess. Master subprocess with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `subprocess` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 6 of B-040: Automating with subprocess. Give me 3 progressive exercises."

---
### DFY Lesson 7: Testing Your Python Automation Code

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 07: Testing Your Python Automation Code       │
│  Book: B-040  Tool: subprocess                 │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 7: Testing Your Python Automation Code. Master subprocess with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `subprocess` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 7 of B-040: Testing Your Python Automation Code. Give me 3 progressive exercises."

---
### DFY Lesson 8: Production Python Automation Patterns

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 08: Production Python Automation Patterns     │
│  Book: B-040  Tool: subprocess                 │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 8: Production Python Automation Patterns. Master subprocess with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `subprocess` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 8 of B-040: Production Python Automation Patterns. Give me 3 progressive exercises."

---
### DFY Lesson 9: Debugging Python Automation Problems

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 09: Debugging Python Automation Problems      │
│  Book: B-040  Tool: subprocess                 │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 9: Debugging Python Automation Problems. Master subprocess with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `subprocess` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 9 of B-040: Debugging Python Automation Problems. Give me 3 progressive exercises."

---
### DFY Lesson 10: Earning Your PEL-L0-B040-AutomationPro Credential

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 10: Earning Your PEL-L0-B040-AutomationPro C  │
│  Book: B-040  Tool: subprocess                 │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 10: Earning Your PEL-L0-B040-AutomationPro Credential. Master subprocess with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `subprocess` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 10 of B-040: Earning Your PEL-L0-B040-AutomationPro Credential. Give me 3 progressive exercises."

---

### Claim Your Credential

Complete all 10 lessons → open Appendix C → run: *"Generate my credential claim for `PEL-L0-B040-AutomationPro`."*

---

## Chapter 13: How It Works — Use Cases & Applications

> *"Knowing what to do is different from knowing why it matters." — lippytmai*

### The Mechanism

Python Automation in Python works because the language was designed to be readable, composable, and deployable. subprocess is the tool that makes Python Automation practical.

### 5 Real-World Use Cases

| Domain | Application | Your Credential Unlocks |
|---|---|---|
| Backend Dev | Build APIs and services with subprocess | PEL-L0-B040-AutomationPro → production deployments |
| Data Engineering | Process and transform data pipelines | PEL-L0-B040-AutomationPro → ETL roles |
| DevOps/Automation | Automate repetitive tasks | PEL-L0-B040-AutomationPro → CI/CD integration |
| AI/ML | Preprocess data and build models | PEL-L0-B040-AutomationPro → AI projects |
| Freelance | Deliver Python solutions to clients | PEL-L0-B040-AutomationPro → paid work |

### 📘 Mechanism Diagram

```
INPUT → [Python Automation Layer] → OUTPUT
         ↓
[ACSS Integration] → Hermes Event → Fabric Node
         ↓
[ADA Activation] → lippytmai-launch run B-040
```

### 🎧 Audiobook Narration:

> *"When you master Python Automation, you're not just learning syntax — you're learning how production Python systems work. Every ACSS component uses these patterns. This is infrastructure knowledge."*

### 🎬 Video: 5-Domain Application Tour

**Scene 1 — Backend:** API or service using Python Automation
**Scene 2 — Data:** Data pipeline using Python Automation
**Scene 3 — DevOps:** Automation script using Python Automation
**Scene 4 — AI/ML:** Model integration using Python Automation
**Scene 5 — Freelance:** Client deliverable using Python Automation

---

## Chapter 14: ACSS Explainer Series — Automation Scripts That Save Hours

> *"You're not just learning Python Automation. You're building a node in an intelligence network." — lippytmai*

10 explainer lessons connecting Automation Scripts That Save Hours to the full ACSS architecture.

---

### Explainer 1: ACSS Overview
*intelligence network*

**📘 Ebook Explanation:** Automation Scripts That Save Hours teaches the Python Automation layer that feeds the ACSS. Automation scripts are the glue of acss — every hermes sync, fabric update, and ada batch run is a python automation script.

**📘 Connection Map:**
```
B-040 (Python Automation) ↕ ACSS Overview ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Automation Scripts That Save Hours connects to ACSS Overview: Automation Scripts That Save Hours teaches the Python Automation layer that feeds the ACSS. Automati..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ACSS Overview in ACSS diagram
- 10–35s: Zoom to where B-040 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-040

**🤖 Copilot Prompt:** > *"Explain how Python Automation fits the ACSS. What role does B-040 play?"*

---
### Explainer 2: Hermes Event Routing
*cross-system message bus*

**📘 Ebook Explanation:** Hermes routes Python Automation practice events. Completing an exercise emits a `skill.practice` event.

**📘 Connection Map:**
```
B-040 (Python Automation) ↕ Hermes Event Routing ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Automation Scripts That Save Hours connects to Hermes Event Routing: Hermes routes Python Automation practice events. Completing an exercise emits a `skill.practice` eve..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Hermes Event Routing in ACSS diagram
- 10–35s: Zoom to where B-040 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-040

**🤖 Copilot Prompt:** > *"Show the Hermes event schema for a B-040 skill-complete event."*

---
### Explainer 3: Fabric Knowledge Graph
*pattern synthesis*

**📘 Ebook Explanation:** Fabric stores every Python Automation concept as a knowledge node connected to related books.

**📘 Connection Map:**
```
B-040 (Python Automation) ↕ Fabric Knowledge Graph ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Automation Scripts That Save Hours connects to Fabric Knowledge Graph: Fabric stores every Python Automation concept as a knowledge node connected to related books...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Fabric Knowledge Graph in ACSS diagram
- 10–35s: Zoom to where B-040 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-040

**🤖 Copilot Prompt:** > *"Generate the Fabric node definition for the core concept of B-040."*

---
### Explainer 4: Clone Engine Identity
*AI persona system*

**📘 Ebook Explanation:** lippytmai teaches Automation Scripts That Save Hours in Teach mode. The Clone Engine maintains consistent voice across all 300 books.

**📘 Connection Map:**
```
B-040 (Python Automation) ↕ Clone Engine Identity ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Automation Scripts That Save Hours connects to Clone Engine Identity: lippytmai teaches Automation Scripts That Save Hours in Teach mode. The Clone Engine maintains consi..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Clone Engine Identity in ACSS diagram
- 10–35s: Zoom to where B-040 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-040

**🤖 Copilot Prompt:** > *"As lippytmai, explain Python Automation to a complete beginner using the B-040 voice."*

---
### Explainer 5: CLL/CCSLL/CBSLL
*Complete Language Libraries*

**📘 Ebook Explanation:** `PEL-L0-B040-AutomationPro` is registered in the Python Earn-while-you-Learn library (PEL). PEL tracks all Python credentials B-026–B-100+.

**📘 Connection Map:**
```
B-040 (Python Automation) ↕ CLL/CCSLL/CBSLL ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Automation Scripts That Save Hours connects to CLL/CCSLL/CBSLL: `PEL-L0-B040-AutomationPro` is registered in the Python Earn-while-you-Learn library (PEL). PEL trac..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show CLL/CCSLL/CBSLL in ACSS diagram
- 10–35s: Zoom to where B-040 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-040

**🤖 Copilot Prompt:** > *"Show where PEL-L0-B040-AutomationPro fits in the PEL credential hierarchy."*

---
### Explainer 6: ADA Activation
*deployment system*

**📘 Ebook Explanation:** `lippytmai-launch run B-040` activates Automation Scripts That Save Hours through the ADA FastAPI backend.

**📘 Connection Map:**
```
B-040 (Python Automation) ↕ ADA Activation ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Automation Scripts That Save Hours connects to ADA Activation: `lippytmai-launch run B-040` activates Automation Scripts That Save Hours through the ADA FastAPI ba..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ADA Activation in ACSS diagram
- 10–35s: Zoom to where B-040 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-040

**🤖 Copilot Prompt:** > *"Write the ADA activation manifest for B-040."*

---
### Explainer 7: ACVS Video Pipeline
*video creator*

**📘 Ebook Explanation:** Every Automation Scripts That Save Hours video uses ACVS SHOW→BUILD→VERIFY structure.

**📘 Connection Map:**
```
B-040 (Python Automation) ↕ ACVS Video Pipeline ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Automation Scripts That Save Hours connects to ACVS Video Pipeline: Every Automation Scripts That Save Hours video uses ACVS SHOW→BUILD→VERIFY structure...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ACVS Video Pipeline in ACSS diagram
- 10–35s: Zoom to where B-040 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-040

**🤖 Copilot Prompt:** > *"Generate the ACVS scene manifest for B-040 Lesson 1."*

---
### Explainer 8: OMARCHY Workstation
*Arch Linux standard*

**📘 Ebook Explanation:** All Automation Scripts That Save Hours exercises run on OMARCHY — the reference environment ensures every learner has the same Python setup.

**📘 Connection Map:**
```
B-040 (Python Automation) ↕ OMARCHY Workstation ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Automation Scripts That Save Hours connects to OMARCHY Workstation: All Automation Scripts That Save Hours exercises run on OMARCHY — the reference environment ensures ..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show OMARCHY Workstation in ACSS diagram
- 10–35s: Zoom to where B-040 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-040

**🤖 Copilot Prompt:** > *"What OMARCHY packages are required to complete all B-040 exercises?"*

---
### Explainer 9: Cross-Platform Copilot
*15-platform deployment*

**📘 Ebook Explanation:** The Automation Scripts That Save Hours AI Copilot deploys on ChatGPT, Gemini, Claude, GitHub, Slack, and 10 more platforms.

**📘 Connection Map:**
```
B-040 (Python Automation) ↕ Cross-Platform Copilot ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Automation Scripts That Save Hours connects to Cross-Platform Copilot: The Automation Scripts That Save Hours AI Copilot deploys on ChatGPT, Gemini, Claude, GitHub, Slack,..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Cross-Platform Copilot in ACSS diagram
- 10–35s: Zoom to where B-040 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-040

**🤖 Copilot Prompt:** > *"Adapt the B-040 copilot system prompt for LinkedIn."*

---
### Explainer 10: Earn-While-You-Learn
*revenue system*

**📘 Ebook Explanation:** `PEL-L0-B040-AutomationPro` is proof of Python Automation mastery. Use it on LinkedIn, GitHub, and in lippytm.ai to unlock paid opportunities.

**📘 Connection Map:**
```
B-040 (Python Automation) ↕ Earn-While-You-Learn ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Automation Scripts That Save Hours connects to Earn-While-You-Learn: `PEL-L0-B040-AutomationPro` is proof of Python Automation mastery. Use it on LinkedIn, GitHub, and i..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Earn-While-You-Learn in ACSS diagram
- 10–35s: Zoom to where B-040 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-040

**🤖 Copilot Prompt:** > *"I just earned PEL-L0-B040-AutomationPro. Generate my LinkedIn credential announcement."*

---

### Your ACSS Node Is Now Active

Completing B-040 activates your node in the Fabric graph.
**Next:** `lippytmai-launch run B-040` or start B-041 Web Scraper.

---

## Appendix A: Enhanced Cheat Sheet — Automation Scripts That Save Hours

### 📘 Print-Optimized Reference Card

```
╔══════════════════════════════════════════════════════════════╗
║  B-040: Automation Scripts That Save Hours             ║
║  Credential: PEL-L0-B040-AutomationPro                          ║
╠══════════════════════════════════════════════════════════════╣
║  Core: subprocess                                               ║
║  Tool: subprocess + pathlib                                     ║
╠══════════════════════════════════════════════════════════════╣
║  Activate: lippytmai-launch run B-040                            ║
╚══════════════════════════════════════════════════════════════╝
```

### Quick Reference

| Concept | Pattern | Use Case |
|---|---|---|
| `subprocess` | [usage pattern] | [when to use] |
| `os` | [usage pattern] | [when to use] |
| `shutil` | [usage pattern] | [when to use] |
| `pathlib` | [usage pattern] | [when to use] |

### 🎧 Verbal Cheat Sheet: *"Core concepts: subprocess, os, shutil. Credential: PEL-L0-B040-AutomationPro."*

### 🎬 Thumbnail: Dark background, `B-040` bold white, `subprocess` in green, credential badge bottom-right.

---

## Appendix B: ACSS Connection Map

Node `B-040` in the ACSS knowledge graph:

```
[Hermes] → [B-040 Events] → [Fabric] → [ADA] → [ACVS] → [OMARCHY] → [PEL:PEL-L0-B040-AutomationPro] → [EWYL]
```

**Book chain:** B-039 SQLite Builder ← **Automation Scripts That Save Hours** → B-041 Web Scraper

---

## Appendix C: AI Copilot System — Automation Scripts That Save Hours

### System Prompt
```
You are lippytmai teaching "Automation Scripts That Save Hours" (B-040).
Help learners master Python Automation using subprocess.
Credential: PEL-L0-B040-AutomationPro. Philosophy: Earn-while-you-Learn.
Always give 3-step exercises: setup → execute → verify.
```

### 30 Ebook Prompts (5 stages × 6)

**Stage 1 — Foundation:** 1."Explain Python Automation to a beginner." 2."Most important concept in B-040?" 3."Give a 3-step setup for subprocess." 4."5 common beginner mistakes with Python Automation?" 5."Anatomy of a subprocess pattern." 6."Mental model for Python Automation."

**Stage 2 — Practice:** 7."5 progressive Python Automation exercises." 8."Diagnose this error: [paste]." 9."Walk through this code line by line." 10."What to practice today?" 11."20-minute session for Python Automation." 12."Beginner vs. professional Python Automation comparison."

**Stage 3 — Application:** 13."Build a real Python Automation script." 14."How does Python Automation connect to production systems?" 15."Professional Python Automation workflow." 16."What does Python Automation mastery look like on a resume?" 17."Project using only B-040 skills." 18."3 Python Automation patterns in large-scale systems."

**Stage 4 — Integration:** 19."How does B-040 connect to other books?" 20."How does Python Automation feed ACSS?" 21."Hermes events for Python Automation?" 22."How does Fabric store Python Automation?" 23."ADA activation for B-040." 24."Cross-phase connections from B-040."

**Stage 5 — Mastery:** 25."Assess my Python Automation level." 26."Stretch goals for PEL-L0-B040-AutomationPro holders?" 27."Generate my credential claim for PEL-L0-B040-AutomationPro." 28."LinkedIn post for PEL-L0-B040-AutomationPro." 29."Portfolio project for PEL-L0-B040-AutomationPro." 30."90-day plan building on PEL-L0-B040-AutomationPro."

### 15 Audiobook Prompts

1."Narrate Python Automation intro for a podcast." 2."Story explaining why Python Automation matters." 3."Audio walkthrough of key B-040 code." 4."Day in the life of a Python Automation master." 5."2-minute audio lesson on subprocess." 6."Python Automation explained with analogies only." 7."Top 5 mistakes with Python Automation." 8."Audio quiz: 5 questions." 9."Motivational close for B-040." 10."Credential claim narration." 11."Story: developer mastered Python Automation." 12."Audio summary for commuting." 13."3 real-world Python Automation scenarios." 14."Capstone walkthrough narration." 15."lippytmai intro monologue for B-040."

### 15 Video Prompts

1."Script 90-second B-040 intro." 2."SHOW→BUILD→VERIFY for subprocess." 3."Split-screen before/after Python Automation." 4."Capstone project_scaffolder.py terminal walkthrough." 5."YouTube thumbnail description." 6."3-minute tutorial on key concept." 7."Progress bar overlay design." 8."ACVS scene manifest for Lesson 1." 9."60-second quick tip for Python Automation." 10."Error-and-fix scene." 11."Code annotation style." 12."Credential reveal scene." 13."ACSS connection diagram for Ch14." 14."Cross-platform Python Automation comparison." 15."End-screen CTA design."

### Deployment

```bash
lippytmai-launch run B-040
curl http://localhost:8000/run/B-040
```

Deploy to 15 platforms via `docs/acss-cross-platform-copilot-deployment.md`.

---

## Appendix D: Quick Quiz & Self-Assessment — Automation Scripts That Save Hours

### 📘 Ebook Quiz (20 Questions)

**Section 1 — Concepts (Q1–5):**
1. What is Python Automation and why does it matter? *(b — practical mastery of subprocess)*
2. Primary tool for Python Automation? *(a — subprocess)*
3. Which ACSS system routes Python Automation events? *(c — Hermes)*
4. Your credential for B-040? *(b — PEL-L0-B040-AutomationPro)*
5. What does `lippytmai-launch run B-040` do? *(d — activates via ADA)*

**Section 2 — Syntax (Q6–10):**
6. Write a minimal subprocess example: ___
7. How do you handle errors in Python Automation? ___
8. One-liner combining subprocess with another tool: ___
9. How do you test Python Automation code? ___
10. How do you deploy Python Automation to production? ___

**Section 3 — Application (Q11–15):**
11. Describe a real-world Python Automation scenario that saves an hour.
12. Most common mistake with subprocess?
13. How does Python Automation connect to security?
14. How does B-040 apply to a production Python project?
15. What would you build first after earning PEL-L0-B040-AutomationPro?

**Section 4 — ACSS (Q16–20):**
16. ADA command for B-040? *(lippytmai-launch run B-040)*
17. Fabric node type for Python Automation? *(ConceptNode)*
18. How does Clone Engine use Python Automation? *(lippytmai teaches in Teach mode)*
19. 2 books that build on B-040?
20. EWYL opportunity unlocked by PEL-L0-B040-AutomationPro?

### 🎧 Audiobook Quiz (10 Questions)

1. Three most important concepts from Automation Scripts That Save Hours?
2. Explain Python Automation in one sentence to a non-developer.
3. First thing to do when subprocess fails?
4. Recite your credential.
5. One project buildable with B-040 skills only.
6. ACSS system that stores skill progress? *(Fabric)*
7. ADA activation command? *(lippytmai-launch run B-040)*
8. Next book after B-040? *(B-041 Web Scraper)*
9. Say the EWYL pledge: "I learn, I build, I earn, I share."
10. What makes Python + ACSS a power combination?

### 🎬 Terminal Challenges (5)

1. **Foundation:** Run `subprocess` — screenshot the output.
2. **Intermediate:** Combine `subprocess` with error handling.
3. **Applied:** Write a 10-line script automating a real task.
4. **Debug:** Introduce an error, diagnose and fix it.
5. **Capstone:** Run `project_scaffolder.py` — record a 60-second demo.

---

## Appendix E: Glossary & Error Encyclopedia — Automation Scripts That Save Hours

### Glossary (20 Terms)

| Term | Definition | First Seen |
|---|---|---|
| `subprocess` | [definition in B-040 context] | [B-040] |
| `os` | [definition in B-040 context] | [B-040] |
| `shutil` | [definition in B-040 context] | [B-040] |
| `pathlib` | [definition in B-040 context] | [B-040] |
| `automation` | [definition in B-040 context] | [B-040] |
| `CLI scripts` | [definition in B-040 context] | [B-040] |
| `async` | [definition in B-040 context] | [B-040] |
| `decorator` | [definition in B-040 context] | [B-040] |
| `type hint` | [definition in B-040 context] | [B-040] |
| `dataclass` | [definition in B-040 context] | [B-040] |
| `fixture` | [definition in B-040 context] | [B-040] |
| `Hermes` | [definition in B-040 context] | [B-040] |
| `Fabric` | [definition in B-040 context] | [B-040] |
| `ADA` | [definition in B-040 context] | [B-040] |
| `OMARCHY` | [definition in B-040 context] | [B-040] |
| `credential` | [definition in B-040 context] | [B-040] |
| `EWYL` | [definition in B-040 context] | [B-040] |
| `lippytmai` | [definition in B-040 context] | [B-040] |
| `PEL` | [definition in B-040 context] | [B-040] |
| `Fabric node` | [definition in B-040 context] | [B-040] |

### Error Encyclopedia (10 Common Python Errors)


#### `TypeError` — Cause: Wrong type passed to function. Fix: Add type hints; check with `isinstance()`.
- **🎧 Audio:** "When you see `TypeError`, it means wrong type passed to function"
- **🎬 Video:** Error + fix terminal recording


#### `AttributeError` — Cause: Accessing attribute that doesn't exist. Fix: Use `hasattr()` or check with `dir()`.
- **🎧 Audio:** "When you see `AttributeError`, it means accessing attribute that doesn't exist"
- **🎬 Video:** Error + fix terminal recording


#### `ImportError` — Cause: Module not found. Fix: Check venv is active; run `pip install`.
- **🎧 Audio:** "When you see `ImportError`, it means module not found"
- **🎬 Video:** Error + fix terminal recording


#### `KeyError` — Cause: Dict key doesn't exist. Fix: Use `.get()` with a default value.
- **🎧 Audio:** "When you see `KeyError`, it means dict key doesn't exist"
- **🎬 Video:** Error + fix terminal recording


#### `FileNotFoundError` — Cause: Path doesn't exist. Fix: Use `Path.exists()` before opening.
- **🎧 Audio:** "When you see `FileNotFoundError`, it means path doesn't exist"
- **🎬 Video:** Error + fix terminal recording


#### `ValueError` — Cause: Invalid value for operation. Fix: Validate inputs before processing.
- **🎧 Audio:** "When you see `ValueError`, it means invalid value for operation"
- **🎬 Video:** Error + fix terminal recording


#### `IndentationError` — Cause: Mixed tabs and spaces. Fix: Configure editor to use spaces only.
- **🎧 Audio:** "When you see `IndentationError`, it means mixed tabs and spaces"
- **🎬 Video:** Error + fix terminal recording


#### `RecursionError` — Cause: Infinite recursion. Fix: Add base case; increase recursion limit if needed.
- **🎧 Audio:** "When you see `RecursionError`, it means infinite recursion"
- **🎬 Video:** Error + fix terminal recording


#### `ConnectionError` — Cause: Network request failed. Fix: Wrap in try/except; implement retry logic.
- **🎧 Audio:** "When you see `ConnectionError`, it means network request failed"
- **🎬 Video:** Error + fix terminal recording


#### `PermissionError` — Cause: File or directory not accessible. Fix: Check permissions with `ls -la`.
- **🎧 Audio:** "When you see `PermissionError`, it means file or directory not accessible"
- **🎬 Video:** Error + fix terminal recording


---

## Appendix F: Instructor & Accessibility Guide — Automation Scripts That Save Hours

### Teaching Schedule (4-Week Curriculum)

| Week | Focus | Topics | Outcome |
|---|---|---|---|
| 1 | Foundation | Concepts + setup | Can use Python Automation tools |
| 2 | Intermediate | Core patterns | Can write working code |
| 3 | Applied | Real projects | Can solve production problems |
| 4 | Mastery | DFY + Appendices | Earns `PEL-L0-B040-AutomationPro` |

### Common Confusion Points

1. "When do I use subprocess vs. alternatives?" — Show a decision flowchart.
2. "Why does the same code fail in a different environment?" — Explain venv isolation.
3. "How do I know if my code is production-ready?" — Show the VERIFY step always.
4. "How does Python Automation connect to other Python skills?" — Show the ACSS learning path map.
5. "What does earning PEL-L0-B040-AutomationPro actually mean for my career?" — Show EWYL income examples.

### Assessment Rubric

| Criterion | Beginner | Competent | Expert |
|---|---|---|---|
| Code quality | Messy, no types | Working, some types | Clean, typed, tested |
| Error handling | None | Basic try/except | Custom exceptions + logging |
| Testing | No tests | Basic assertions | pytest + fixtures + coverage |
| ACSS integration | Unaware | Uses ADA | Contributes to ACSS |

### Accessibility: Screen reader alt-text for all diagrams. No color-only encoding. Short paragraphs. Audiobook available.

---

## Appendix G: Your Learning Path — Automation Scripts That Save Hours

### Where You Are Now

```
  Phase 2: Python Programming (B-026–B-055)
  [██████████░░░░░░░░░░] 50%

  ✅ B-039 SQLite Builder (PEL-L0-B039-SQLiteBuilder)
  👉 B-040: Automation Scripts That Save Hours ← YOU ARE HERE
  ⬜ B-041 Web Scraper (PEL-L0-B041-WebScraper)
```

### Credential Chain

```
PEL-L0-B039-SQLiteBuilder → PEL-L0-B040-AutomationPro → PEL-L0-B041-WebScraper
```

### Next Steps

1. Claim `PEL-L0-B040-AutomationPro` (Appendix C, Prompt 27)
2. Build `project_scaffolder.py` (Appendix H)
3. Start `B-041 Web Scraper`

### Cross-Phase Connections

```
Phase 1: Linux Foundations → Phase 2: Python (YOU ARE HERE)
    ↓ B-040 connects to:
Phase 3: Blockchain Development (B-056+)
```

---

## Appendix H: Real Project Showcase — Automation Scripts That Save Hours

### Project: `project_scaffolder.py`

**Credential gated:** Complete this project to qualify for `PEL-L0-B040-AutomationPro`

### Complete Code

```python
#!/usr/bin/env python3
import subprocess
from pathlib import Path

def scaffold_project(name: str, language: str = "python") -> Path:
    project_dir = Path(name)
    (project_dir / "src").mkdir(parents=True, exist_ok=True)
    (project_dir / "tests").mkdir(exist_ok=True)
    (project_dir / "docs").mkdir(exist_ok=True)
    (project_dir / "README.md").write_text(f"# {name}\n")
    if language == "python":
        (project_dir / "requirements.txt").touch()
        (project_dir / ".gitignore").write_text(".venv/\n__pycache__/\n*.pyc\n")
    subprocess.run(["git", "init", str(project_dir)], check=True)
    print(f"Project scaffolded: {project_dir}")
    return project_dir

```

### Deploy Instructions

```bash
# Run the project
python project_scaffolder.py --help
python project_scaffolder.py

# Test it
pytest test_project_scaffolder.py -v  # if tests exist

# Verify
echo "Exit: $?"
```

### Extend It

1. Add type hints to all functions
2. Add pytest test coverage
3. Add CLI interface with typer
4. Containerize with Docker
5. Add structured logging

### 🎧 Walkthrough: *"Build project_scaffolder.py step by step. When it runs successfully, you've earned PEL-L0-B040-AutomationPro."*

### 🎬 Video: SHOW empty editor → BUILD code live → VERIFY execution → CTA: "Claim PEL-L0-B040-AutomationPro."

---

## Further Reading

- 📄 [Back to README](../README.md)
- 📄 [Product Excellence Framework](PRODUCT-EXCELLENCE-FRAMEWORK.md)
- 📄 [AI Clone Engine Swarms](ai-clone-engine-swarms.md)
- 📄 [ACSS Cross-Platform Copilot Deployment](acss-cross-platform-copilot-deployment.md)
- 📄 [ADA Deployment Activations](ai-deployment-activations.md)
- 📄 [Previous: B-039](B-039-*.md)
- 📄 [Next: B-041](B-041-*.md)

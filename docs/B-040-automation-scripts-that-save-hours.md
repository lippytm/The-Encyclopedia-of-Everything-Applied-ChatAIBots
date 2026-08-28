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

## Further Reading

- 📄 [`docs/B-039-sqlite-your-first-database.md`](B-039-sqlite-your-first-database.md) — Persisting data
- 📄 [`docs/B-036-type-hints-making-python-honest.md`](B-036-type-hints-making-python-honest.md) — Type safety
- 📄 [`docs/B-004-the-script-that-did-my-job.md`](B-004-the-script-that-did-my-job.md) — Shell scripting parallel
- 🏠 [`README.md`](../README.md) — Encyclopedia home

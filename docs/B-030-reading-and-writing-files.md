# B-030: Reading and Writing Files

### open(), read(), write(), pathlib, and the Log File Processor

> *"A program that can't persist data is a calculator. A program that reads and writes files is a system. The moment you learn to open a file, read its contents, and write something back, your programs gain memory. This is one of the most important skills in the entire curriculum."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Open, read, and write files using `open()` and context managers (`with`)
2. Handle common file errors (FileNotFoundError, PermissionError)
3. Use `pathlib.Path` for modern, cross-platform file operations
4. Read, parse, and write JSON files
5. Build a `log-processor.py` that reads a log file, extracts errors, and writes a report

**Prerequisite:** B-026 through B-029

**Build Artifact:** `~/developer-workspace/projects/python-foundations/log_processor.py`

**Credential:** `CCSLL-L1-B030-FileEngineer` — on-chain on Base

---

## Chapter 1: open() and Context Managers

```python
# The basic pattern for file I/O:
# open(path, mode) where mode is 'r' (read), 'w' (write), 'a' (append)

# ALWAYS use 'with' — it auto-closes the file, even on errors
with open("hello.txt", "w") as f:
    f.write("Hello, lippytmai!\n")
    f.write("This is line 2.\n")

# Reading the whole file at once
with open("hello.txt", "r") as f:
    content = f.read()
    print(content)

# Reading line by line (memory-efficient for large files)
with open("hello.txt", "r") as f:
    for line in f:
        print(line.strip())   # .strip() removes trailing \n

# Reading all lines into a list
with open("hello.txt", "r") as f:
    lines = f.readlines()
    print(lines)   # ['Hello, lippytmai!\n', 'This is line 2.\n']

# Appending to a file (doesn't overwrite)
with open("hello.txt", "a") as f:
    f.write("This is line 3.\n")
```

---

## Chapter 2: File Modes

```python
# Mode reference:
# 'r'  — read (default), file must exist
# 'w'  — write, creates file or truncates (clears) existing
# 'a'  — append, creates file or adds to end of existing
# 'x'  — exclusive create, fails if file already exists
# 'r+' — read and write
# 'b'  — binary mode (add to any: 'rb', 'wb', etc.)

# Write binary
with open("data.bin", "wb") as f:
    f.write(b"\x00\x01\x02\x03")

# Read binary
with open("data.bin", "rb") as f:
    data = f.read()
    print(data)   # b'\x00\x01\x02\x03'
```

---

## Chapter 3: Error Handling with Files

```python
# What happens when a file doesn't exist?
try:
    with open("nonexistent.txt", "r") as f:
        content = f.read()
except FileNotFoundError as e:
    print(f"File not found: {e}")

# What if we don't have permission?
try:
    with open("/etc/shadow", "r") as f:
        content = f.read()
except PermissionError as e:
    print(f"Permission denied: {e}")
except FileNotFoundError as e:
    print(f"File not found: {e}")

# The safe open pattern
def safe_read(path: str, default: str = "") -> str:
    """Read a file, returning default if it doesn't exist."""
    try:
        with open(path, "r") as f:
            return f.read()
    except (FileNotFoundError, PermissionError) as e:
        print(f"[warning] Could not read {path}: {e}")
        return default
```

---

## Chapter 4: pathlib — Modern File Paths

`pathlib.Path` is the modern, readable, cross-platform way to work with paths:

```python
from pathlib import Path

# Create Path objects
home = Path.home()              # /home/charles
workspace = home / "developer-workspace"   # / joins paths
projects = workspace / "projects" / "python-foundations"

# Check existence
print(workspace.exists())   # True or False
print(workspace.is_dir())   # True
print(workspace.is_file())  # False

# Create directories
projects.mkdir(parents=True, exist_ok=True)

# Path operations
p = Path("/home/charles/scripts/backup.sh")
print(p.name)          # backup.sh
print(p.stem)          # backup
print(p.suffix)        # .sh
print(p.parent)        # /home/charles/scripts

# Read and write with pathlib
(projects / "notes.txt").write_text("Phase 2 started!\n")
content = (projects / "notes.txt").read_text()
print(content)

# Glob patterns
scripts = list(Path.home().glob("scripts/*.sh"))
for script in scripts:
    print(script.name)

# Iterate a directory
for item in workspace.iterdir():
    kind = "DIR" if item.is_dir() else "FILE"
    print(f"  {kind}: {item.name}")
```

---

## Chapter 5: Reading and Writing JSON Files

```python
import json
from pathlib import Path

# Write a config file
config = {
    "app": "lippytmai",
    "version": "2.0",
    "books_active": 30,
    "phase": 2,
}

config_path = Path("~/developer-workspace/configs/app-config.json").expanduser()
config_path.parent.mkdir(parents=True, exist_ok=True)

with open(config_path, "w") as f:
    json.dump(config, f, indent=2)

print(f"Config written to {config_path}")

# Read it back
with open(config_path, "r") as f:
    loaded = json.load(f)

print(f"App: {loaded['app']} v{loaded['version']}")
print(f"Active books: {loaded['books_active']}")

# Pathlib shorthand (for small files)
config_path.write_text(json.dumps(config, indent=2))
loaded2 = json.loads(config_path.read_text())
```

---

## Chapter 6: The Build — Log Processor

```python
#!/usr/bin/env python3
"""
log_processor.py — B-030 Build Artifact

Reads a log file, extracts error and warning lines,
counts occurrences by level, and writes a structured report.
"""
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List


LOG_PATTERN = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)\s+"
    r"(?P<message>.+)"
)

SAMPLE_LOG = """\
2026-08-28 01:00:01 INFO     ADA deployment started for B-026
2026-08-28 01:00:02 DEBUG    Fetching Fabric context for book B-026
2026-08-28 01:00:03 INFO     Hermes: EBOOK_DRAFT_READY dispatched
2026-08-28 01:00:05 WARNING  ElevenLabs API response slow (1.8s)
2026-08-28 01:00:07 INFO     Audiobook generated: b026-python-apprentice.m4b
2026-08-28 01:00:08 ERROR    Credential mint failed: gas estimation error
2026-08-28 01:00:10 INFO     Retrying credential mint (attempt 2)
2026-08-28 01:00:12 INFO     Credential minted: CCSLL-L0-B026-PythonApprentice
2026-08-28 01:01:00 WARNING  Disk usage at 78% on /dev/sda1
2026-08-28 01:01:05 ERROR    Docker image push timeout: lippytmai/b026:latest
2026-08-28 01:01:10 INFO     ADA deployment complete for B-026
"""


def create_sample_log(path: Path) -> None:
    """Write a sample log file for demonstration."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(SAMPLE_LOG)


def parse_log(path: Path) -> List[dict]:
    """Parse a log file into a list of structured records."""
    records = []
    for line in path.read_text().splitlines():
        match = LOG_PATTERN.match(line.strip())
        if match:
            records.append(match.groupdict())
    return records


def analyze(records: List[dict]) -> dict:
    """Produce summary statistics from parsed log records."""
    counts: Dict[str, int] = defaultdict(int)
    errors: List[str] = []
    warnings: List[str] = []

    for rec in records:
        level = rec["level"]
        counts[level] += 1
        if level == "ERROR":
            errors.append(f"[{rec['timestamp']}] {rec['message']}")
        elif level == "WARNING":
            warnings.append(f"[{rec['timestamp']}] {rec['message']}")

    return {
        "total_lines":  len(records),
        "counts":       dict(counts),
        "errors":       errors,
        "warnings":     warnings,
        "has_issues":   bool(errors),
    }


def write_report(analysis: dict, report_path: Path) -> None:
    """Write a structured JSON report."""
    report = {
        "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        **analysis,
    }
    report_path.write_text(json.dumps(report, indent=2))
    print(f"Report written to: {report_path}")


def main() -> None:
    log_path    = Path("~/developer-workspace/logs/ada-sample.log").expanduser()
    report_path = Path("~/developer-workspace/logs/ada-report.json").expanduser()

    create_sample_log(log_path)
    records  = parse_log(log_path)
    analysis = analyze(records)
    write_report(analysis, report_path)

    print(f"\n=== Log Analysis Report ===")
    print(f"Total lines:  {analysis['total_lines']}")
    print(f"Counts:       {analysis['counts']}")
    print(f"Errors ({len(analysis['errors'])}):")
    for err in analysis["errors"]:
        print(f"  ❌ {err}")
    print(f"Warnings ({len(analysis['warnings'])}):")
    for warn in analysis["warnings"]:
        print(f"  ⚠️  {warn}")


if __name__ == "__main__":
    main()
```

```bash
python3 ~/developer-workspace/projects/python-foundations/log_processor.py
cat ~/developer-workspace/logs/ada-report.json
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-030 Verification ==="
python3 -c "
from pathlib import Path

# Write and read back
p = Path('/tmp/b030-test.txt')
p.write_text('B-030 file I/O works!\n')
print('Written:', p.read_text().strip())

# Path operations
print('Name:', p.name)
print('Suffix:', p.suffix)
print('Parent:', p.parent)
p.unlink()  # cleanup
print('File deleted.')
"
python3 ~/developer-workspace/projects/python-foundations/log_processor.py
```

---

## 🐍 Phase 2 Batch 1 — Python Foundations Launched

Books B-026–B-030 complete the first batch of the Python Foundations curriculum:

| Book | Title | Build Artifact |
|---|---|---|
| B-026 | Your First Python Program | `hello-lippytmai.py` |
| B-027 | Lists, Loops, and Logic | `grade-calculator.py` |
| B-028 | Functions That Do One Thing Well | `math_utils.py` |
| B-029 | Dictionaries: The Data Swiss Army Knife | `config_reader.py` |
| B-030 | Reading and Writing Files | `log_processor.py` |

---

## Further Reading

- 📄 [`docs/B-029-dictionaries-the-data-swiss-army-knife.md`](B-029-dictionaries-the-data-swiss-army-knife.md) — JSON and dicts used with files
- 📄 [`docs/B-018-the-log-that-tells-the-truth.md`](B-018-the-log-that-tells-the-truth.md) — Log files from the Linux series
- 📄 [`docs/B-023-archives-compression-and-backups.md`](B-023-archives-compression-and-backups.md) — Archiving files
- 🏠 [`README.md`](../README.md) — Encyclopedia home

# B-050: Python + Linux — The Power Combo

### subprocess, os, sys, shlex, and Python as a Linux System Manager

> *"Python was born on Unix. It was designed to talk to the operating system. When you combine Python's expressiveness with Linux's raw power, you get a system management language that beats shell scripts in every way: error handling, data structures, testing, and readability. This is the bridge between Phase 1 (Linux) and Phase 2 (Python). Both libraries, unified."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Run system commands safely with `subprocess`
2. Work with processes, signals, and system info via `os` and `sys`
3. Parse shell command strings safely with `shlex`
4. Build scripts that manage Linux system resources
5. Build a `system_manager.py` — a Python-powered Linux system toolkit

**Prerequisite:** B-040 (pathlib/subprocess intro), B-049 (logging)

**Libraries:** CCSLL + CLL (dual credential)

**Build Artifact:** `~/developer-workspace/projects/python-foundations/system_manager.py`

**Credential:** `CCSLL-L1-B050-SystemEngineer` + `CLL-L1-B050-LinuxPythonBridge` — on-chain on Base

---

## Chapter 1: subprocess — The Right Way to Run Commands

```python
import subprocess
from typing import Optional

# CORRECT: always pass a list — never concatenate strings with user input
result = subprocess.run(
    ["ls", "-la", "/tmp"],
    capture_output=True,
    text=True,
    check=True,      # raise CalledProcessError on non-zero exit code
)
print(result.stdout)
print(result.returncode)   # 0

# capture_output=True captures both stdout and stderr
result2 = subprocess.run(
    ["df", "-h"],
    capture_output=True,
    text=True,
)
if result2.returncode == 0:
    print(result2.stdout)
else:
    print(f"Error: {result2.stderr}")

# Timeout — prevent hanging forever
try:
    subprocess.run(["sleep", "10"], timeout=2)
except subprocess.TimeoutExpired:
    print("Command timed out")

# Check if a command exists
def command_exists(cmd: str) -> bool:
    return subprocess.run(
        ["which", cmd], capture_output=True
    ).returncode == 0

print(command_exists("git"))     # True
print(command_exists("xyz123"))  # False
```

---

## Chapter 2: shlex — Safe Command Parsing

```python
import shlex

# shlex.split handles quoting and spaces correctly
cmd = 'grep -r "hello world" /etc/hosts'
parts = shlex.split(cmd)
print(parts)   # ['grep', '-r', 'hello world', '/etc/hosts']

# shlex.quote escapes a string for safe shell use
user_input = "my file with spaces.txt"
quoted = shlex.quote(user_input)
print(quoted)  # 'my file with spaces.txt'

# Safe command construction from user input
def safe_grep(pattern: str, path: str) -> str:
    """Run grep safely, even with special characters in inputs."""
    cmd = ["grep", "-r", pattern, path]   # list form — always safe
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

# NEVER do this:
# os.system(f"grep -r {user_input} /etc")   ← shell injection risk
# subprocess.run(f"grep {user_input}", shell=True)  ← also dangerous
```

---

## Chapter 3: os Module — OS Interface

```python
import os
from pathlib import Path

# Process info
print(f"PID: {os.getpid()}")
print(f"Parent PID: {os.getppid()}")
print(f"User: {os.getlogin()}")
print(f"UID: {os.getuid()}")    # Linux/macOS only

# Environment
print(f"HOME: {os.environ.get('HOME')}")
print(f"PATH: {os.environ.get('PATH', '')[:60]}...")
os.environ["MY_VAR"] = "hello"    # set for current process + children

# Working directory
cwd = os.getcwd()
print(f"CWD: {cwd}")
os.chdir("/tmp")        # change CWD (for current process only)
os.chdir(cwd)           # change back

# File operations (prefer pathlib — these are the os equivalents)
os.makedirs("/tmp/testdir/sub", exist_ok=True)
os.rename("/tmp/testdir", "/tmp/testdir2")
os.rmdir("/tmp/testdir2/sub")   # only if empty
import shutil
shutil.rmtree("/tmp/testdir2", ignore_errors=True)

# Process execution (avoid os.system — use subprocess instead)
# os.system("ls") ← no output capture, no error handling
```

---

## Chapter 4: sys Module — Interpreter Interface

```python
import sys

# Python version
print(f"Python {sys.version}")
print(f"Version tuple: {sys.version_info}")
assert sys.version_info >= (3, 11), "Python 3.11+ required"

# Script arguments
# python3 script.py arg1 arg2
print(f"Script: {sys.argv[0]}")
print(f"Args: {sys.argv[1:]}")

# Exit codes (0 = success, non-zero = failure)
# sys.exit(0)    # success
# sys.exit(1)    # general error

# stdout / stderr
sys.stdout.write("Normal output\n")
sys.stderr.write("Error output\n")

# Module search path
print(sys.path[:3])

# Installed packages
import importlib.metadata
for pkg in sorted(importlib.metadata.packages_distributions()):
    pass   # iterate all installed packages

# Platform info
print(f"Platform: {sys.platform}")    # linux / darwin / win32
print(f"Prefix: {sys.prefix}")        # Python install dir
```

---

## Chapter 5: System Information

```python
import subprocess
import platform
from pathlib import Path

def system_info() -> dict[str, object]:
    """Collect system information."""
    info: dict[str, object] = {
        "os": platform.system(),
        "distro": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python": platform.python_version(),
    }

    # Disk usage
    result = subprocess.run(
        ["df", "-h", "--output=source,size,used,avail,pcent,target"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        info["disk"] = result.stdout.strip()

    # Memory
    meminfo = Path("/proc/meminfo")
    if meminfo.exists():
        lines = meminfo.read_text().splitlines()
        for line in lines[:3]:
            key, value = line.split(":", 1)
            info[key.strip()] = value.strip()

    # CPU count
    import os
    info["cpu_count"] = os.cpu_count()

    return info

for key, value in system_info().items():
    if "\n" in str(value):
        print(f"\n{key}:\n{value}")
    else:
        print(f"{key}: {value}")
```

---

## Chapter 6: The Build — system_manager.py

```python
#!/usr/bin/env python3
"""
system_manager.py — B-050 Build Artifact

A Python-powered Linux system management toolkit.
Commands: info, disk, processes, services, run

Usage:
    pip install typer
    python3 system_manager.py info
    python3 system_manager.py disk
    python3 system_manager.py processes --top 10
    python3 system_manager.py run 'ls -la /tmp'
"""
from __future__ import annotations

import os
import platform
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer

app = typer.Typer(
    name="sysmanager",
    help="Python + Linux system management toolkit (B-050)",
    add_completion=False,
)


def _run(cmd: list[str], timeout: int = 10) -> tuple[int, str, str]:
    """Run a command and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


@app.command()
def info() -> None:
    """Show system information."""
    typer.echo("\n=== System Information ===\n")
    items = [
        ("OS",       platform.system()),
        ("Release",  platform.release()),
        ("Version",  platform.version()[:60]),
        ("Machine",  platform.machine()),
        ("Python",   platform.python_version()),
        ("PID",      str(os.getpid())),
        ("CPU cores", str(os.cpu_count())),
        ("HOME",     os.environ.get("HOME", "?")),
        ("SHELL",    os.environ.get("SHELL", "?")),
    ]
    for label, value in items:
        typer.echo(f"  {label:<15} {value}")


@app.command()
def disk(
    path: str = typer.Argument("/", help="Mount point or path to check"),
) -> None:
    """Show disk usage."""
    typer.echo(f"\n=== Disk Usage: {path} ===\n")
    rc, out, err = _run(["df", "-h", path])
    if rc == 0:
        typer.echo(out)
    else:
        typer.echo(f"Error: {err}", err=True)
        raise typer.Exit(1)


@app.command()
def processes(
    top: int = typer.Option(15, "--top", "-n", help="Number of processes to show"),
    sort: str = typer.Option("cpu", "--sort", "-s", help="Sort by: cpu or mem"),
) -> None:
    """Show top processes by CPU or memory usage."""
    sort_col = "%cpu" if sort == "cpu" else "%mem"
    rc, out, err = _run(
        ["ps", "aux", "--sort", f"-{sort_col}"],
    )
    if rc != 0:
        typer.echo(f"ps error: {err}", err=True)
        raise typer.Exit(1)
    lines = out.splitlines()
    typer.echo(f"\n=== Top {top} Processes (by {sort}) ===\n")
    for line in lines[:top + 1]:   # +1 for header
        typer.echo(line)


@app.command()
def services(
    name: Optional[str] = typer.Argument(None, help="Service name to check (optional)"),
) -> None:
    """List or check systemd service status."""
    if name:
        rc, out, err = _run(["systemctl", "status", name])
        typer.echo(out or err)
    else:
        rc, out, err = _run(["systemctl", "list-units", "--type=service",
                              "--state=running", "--no-pager"])
        if rc == 0:
            typer.echo(out[:3000])   # truncate long lists
        else:
            typer.echo("systemd not available on this system.", err=True)


@app.command()
def run(
    command: str = typer.Argument(..., help="Shell command to run (quoted string)"),
    timeout: int = typer.Option(30, "--timeout", "-t"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    """Run a shell command safely (no shell injection)."""
    try:
        args = shlex.split(command)
    except ValueError as e:
        typer.echo(f"Parse error: {e}", err=True)
        raise typer.Exit(1)

    if verbose:
        typer.echo(f"Running: {args}")

    try:
        rc, out, err = _run(args, timeout=timeout)
        if out:
            typer.echo(out)
        if err:
            typer.echo(typer.style(err, fg="yellow"), err=True)
        if rc != 0:
            raise typer.Exit(rc)
    except subprocess.TimeoutExpired:
        typer.echo(f"Command timed out after {timeout}s", err=True)
        raise typer.Exit(1)
    except FileNotFoundError:
        typer.echo(f"Command not found: {args[0]}", err=True)
        raise typer.Exit(127)


if __name__ == "__main__":
    app()
```

```bash
pip install typer
python3 ~/developer-workspace/projects/python-foundations/system_manager.py info
python3 ~/developer-workspace/projects/python-foundations/system_manager.py disk /
python3 ~/developer-workspace/projects/python-foundations/system_manager.py run 'uname -a'
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-050 Verification ==="
python3 -c "
import subprocess, shlex, os, sys

# subprocess: run a safe command
result = subprocess.run(['uname', '-s'], capture_output=True, text=True)
print(f'OS: {result.stdout.strip()}')

# shlex: safely parse a command string
cmd = 'echo \"hello world\"'
parts = shlex.split(cmd)
print(f'Parsed: {parts}')

# os: environment and process
print(f'PID: {os.getpid()}')
print(f'HOME: {os.environ.get(\"HOME\", \"?\")}')

# sys: version check
assert sys.version_info >= (3, 11)
print(f'Python: {sys.version_info.major}.{sys.version_info.minor}')
print('✅ Python + Linux power combo works')
"
```

---

## Phase 2 Complete — What You've Built

Congratulations. **B-001 through B-050** — 50 books spanning two complete phases:

| Phase | Library | Books | Skills |
|---|---|---|---|
| Phase 1 | CLL | B-001–B-025 | Linux foundations, tools, automation |
| Phase 2 | CCSLL | B-026–B-050 | Python fundamentals → web → data → DevOps |

**Phase 3 Preview (B-051–B-075): Python Advanced**
- B-051–B-055: Data Science (NumPy, Matplotlib, data analysis)
- B-056–B-060: Web Development (Django/FastAPI full-stack)
- B-061–B-065: Blockchain + Python (Web3.py, smart contract interaction)
- B-066–B-070: AI/ML (scikit-learn, model training, deployment)
- B-071–B-075: Advanced Python (generators, metaclasses, C extensions)

---

## Further Reading

- 📄 [`docs/B-040-automation-scripts-that-save-hours.md`](B-040-automation-scripts-that-save-hours.md) — pathlib + shutil
- 📄 [`docs/B-049-logging-the-programs-memory.md`](B-049-logging-the-programs-memory.md) — Logging in system scripts
- 📄 [`docs/linux-blockchain-educational-ecosystem.md`](linux-blockchain-educational-ecosystem.md) — Linux + blockchain ecosystem
- 🏠 [`README.md`](../README.md) — Encyclopedia home

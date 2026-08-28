# B-005: Installing Things Without Breaking Things

### Package Managers, Python Environments, and the Art of Clean Setup

> *"A broken development environment is not a failure — it's a prerequisite. Every senior developer has destroyed their machine at least once and learned exactly how to set it up right the second time. This book gives you the second-time knowledge on your first attempt."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Use `apt` (Debian/Ubuntu) and `pacman` (Arch) to install, update, and remove software
2. Understand what a package manager actually does
3. Install Python 3.11+ and `pip` on any Linux system
4. Create and activate a Python virtual environment (`venv`)
5. Build a complete, isolated Python development environment

**Prerequisite:** B-001 through B-004 (terminal fluency, permissions, basic scripting)

**Build Artifact:** A fully configured Python development environment with `venv`, `pip`, and a working `hello_world.py` that you can run and share

**Credential:** `CLL-L1-B005-DevEnvironmentBuilder` — on-chain on Base

---

## Chapter 1: What Is a Package Manager?

When you install a program by downloading an `.exe` or `.dmg` and clicking through a wizard, you're trusting that installer to:

1. Copy files to the right locations
2. Register the program with the OS
3. Install dependencies (other software it needs)
4. Provide an uninstaller later

A **package manager** does all of this from the terminal, for thousands of programs, and keeps track of everything so you can upgrade or remove any package with one command.

Linux distributions ship with their own package managers:

| Distro Family | Package Manager | Install Command | Example |
|---|---|---|---|
| Debian, Ubuntu, WSL2 | `apt` | `sudo apt install <pkg>` | `sudo apt install python3` |
| Arch, OMARCHY, Manjaro | `pacman` | `sudo pacman -S <pkg>` | `sudo pacman -S python` |
| Fedora, RHEL | `dnf` | `sudo dnf install <pkg>` | `sudo dnf install python3` |
| macOS | `brew` (Homebrew) | `brew install <pkg>` | `brew install python` |
| Any Linux | `snap` | `sudo snap install <pkg>` | `sudo snap install code` |

*[Reality — all package managers listed above are actively maintained and widely used in production in 2026]*

---

## Chapter 2: apt — The Debian/Ubuntu Way

### Basic apt Commands

```bash
# Update the package list (always do this before installing)
sudo apt update

# Upgrade all installed packages to their latest versions
sudo apt upgrade

# Install a package
sudo apt install python3 python3-pip python3-venv

# Remove a package (keeps config files)
sudo apt remove python3

# Remove a package AND its config files
sudo apt purge python3

# Remove packages no longer needed
sudo apt autoremove

# Search for a package
apt search "python editor"

# Show information about a package before installing
apt show python3
```

### apt Workflow: Before You Install Anything

```bash
# The golden sequence
sudo apt update          # 1. Refresh the catalog
sudo apt upgrade -y      # 2. Apply pending updates
sudo apt install <pkg>   # 3. Install what you need
```

> *[Reality — `sudo apt update` downloads a fresh list of available packages from Ubuntu's servers. It does NOT install anything.]*

---

## Chapter 3: pacman — The Arch Linux Way

If you're on Arch Linux (or OMARCHY), you use `pacman`:

```bash
# Update package database and upgrade all packages
sudo pacman -Syu

# Install a package
sudo pacman -S python python-pip

# Remove a package
sudo pacman -R python

# Remove package + unused dependencies
sudo pacman -Rs python

# Search for a package
pacman -Ss python

# Show info about a package
pacman -Si python

# Show files installed by a package
pacman -Ql python
```

### The AUR — Arch User Repository

Arch also has the AUR (Arch User Repository) for community packages not in the official repos. Use `yay` to access it:

```bash
# Install yay (AUR helper) — do this once
cd /tmp
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si

# Then use yay like pacman
yay -S visual-studio-code-bin
yay -S google-chrome
```

---

## Chapter 4: Python — The Language of This Series

Python is the primary language for Chapters B-026 through B-055 and for all AI/ML work in this series. You'll use it for:

- Scripting and automation (B-026–B-035)
- Web APIs with FastAPI (Intermediate series)
- Machine learning and AI (Advanced series)
- Every P011 engine implementation

### Installing Python

**Ubuntu/Debian (WSL2):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-dev

# Verify
python3 --version
# Python 3.11.x or 3.12.x

pip3 --version
# pip 23.x from /usr/lib/python3/...
```

**Arch/OMARCHY:**
```bash
sudo pacman -Syu python python-pip

python --version    # On Arch, 'python' = python3
pip --version
```

**macOS:**
```bash
brew install python@3.12
python3 --version
pip3 --version
```

---

## Chapter 5: Virtual Environments — The Most Important Python Skill

Here's the problem: you're working on Project A that needs `requests==2.28.0` and Project B that needs `requests==2.31.0`. If you install both globally, only one version can win.

The solution: **virtual environments** — isolated Python installations per project.

```
Global Python
├── Python 3.12
└── pip packages (shared, can conflict ⚠️)

project-alpha/
└── venv/                    ← isolated environment
    ├── Python 3.12 (copy)
    └── pip packages (only for project-alpha ✓)

project-beta/
└── venv/                    ← different isolated environment
    ├── Python 3.12 (copy)
    └── pip packages (only for project-beta ✓)
```

### Creating and Using a Virtual Environment

```bash
# Navigate to your project
cd ~/developer-workspace/project-alpha

# Create the virtual environment
python3 -m venv venv

# Activate it (Linux/macOS)
source venv/bin/activate

# You'll see the prompt change:
# (venv) charles@lippytm-dev:~/developer-workspace/project-alpha$
# The (venv) prefix tells you it's active

# Now pip installs go INTO the venv, not globally
pip install requests

# See what's installed in this venv
pip list

# Deactivate when done
deactivate
# Prompt goes back to normal
```

> *[Reality — `source venv/bin/activate` is the single most important Python command for professional development. Never install packages globally for projects.]*

---

## Chapter 6: pip — Python Package Manager

```bash
# Always activate your venv first!
source venv/bin/activate

# Install a package
pip install requests

# Install a specific version
pip install requests==2.31.0

# Install from a requirements file
pip install -r requirements.txt

# List installed packages
pip list

# Show info about a package
pip show requests

# Uninstall
pip uninstall requests

# Save your current environment to a file
pip freeze > requirements.txt

# Upgrade a package
pip install --upgrade requests

# Upgrade pip itself
pip install --upgrade pip
```

### requirements.txt — Reproducible Environments

A `requirements.txt` file is the standard way to share your environment with others:

```bash
# After installing all your packages:
pip freeze > requirements.txt

# The file will look like:
cat requirements.txt
# certifi==2024.2.2
# charset-normalizer==3.3.2
# idna==3.6
# requests==2.31.0
# urllib3==2.2.1

# Anyone can now recreate your exact environment:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Chapter 7: The Build — Complete Python Dev Environment

This is your B-005 build artifact: a complete, isolated Python development environment with a working program.

```bash
# Step 1: Ensure Python is installed
python3 --version || sudo apt install python3 python3-pip python3-venv -y

# Step 2: Navigate to your project
cd ~/developer-workspace/project-alpha

# Step 3: Create the virtual environment
python3 -m venv venv

# Step 4: Activate it
source venv/bin/activate

# Step 5: Upgrade pip
pip install --upgrade pip

# Step 6: Install some useful packages
pip install requests rich

# Step 7: Write your first Python program
cat > src/hello_world.py << 'EOF'
#!/usr/bin/env python3
"""
hello_world.py — B-005 Build Artifact
lippytm.ai Earn-while-you-Learn Series

A working Python program demonstrating:
- Standard library usage
- Third-party library usage (rich, requests)
- Type hints
- Docstrings
"""
import sys
import datetime
from typing import Optional

try:
    from rich.console import Console
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


def build_system_table(name: str, venv_path: Optional[str] = None) -> None:
    """Display a system summary table using rich if available."""
    if not RICH_AVAILABLE:
        print(f"Hello from Python! Name: {name}")
        print(f"Python version: {sys.version}")
        print(f"Date: {datetime.datetime.now()}")
        return

    console = Console()
    table = Table(title="B-005: Python Dev Environment — ACTIVE ✓")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Developer", name)
    table.add_row("Python Version", sys.version.split(" ")[0])
    table.add_row("Date", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    table.add_row("Virtual Env", venv_path or "active")
    table.add_row("Platform", sys.platform)
    table.add_row("Credential", "CLL-L1-B005-DevEnvironmentBuilder (pending)")

    console.print(table)
    console.print("\n[bold green]✓ Build complete! Your Python dev environment is ready.[/bold green]")


if __name__ == "__main__":
    import os
    venv = os.environ.get("VIRTUAL_ENV", None)
    build_system_table(
        name=os.environ.get("USER", "Developer"),
        venv_path=venv,
    )
EOF

# Step 8: Make it executable
chmod +x src/hello_world.py

# Step 9: Save your requirements
pip freeze > requirements.txt

# Step 10: Run your program
python3 src/hello_world.py

# Step 11: Create a .gitignore (so you don't commit your venv to git)
cat > .gitignore << 'EOF'
venv/
__pycache__/
*.pyc
*.pyo
.env
*.egg-info/
dist/
build/
EOF
```

---

## Chapter 8: Proof of Work

```bash
# Activate venv if not already active
source ~/developer-workspace/project-alpha/venv/bin/activate

echo "=== B-005 Build Verification ==="
echo ""
echo "Python version:"
python3 --version

echo ""
echo "pip version:"
pip --version

echo ""
echo "Virtual environment:"
echo $VIRTUAL_ENV

echo ""
echo "Installed packages:"
pip list

echo ""
echo "Running hello_world.py:"
python3 ~/developer-workspace/project-alpha/src/hello_world.py

echo ""
echo "requirements.txt:"
cat ~/developer-workspace/project-alpha/requirements.txt
```

---

## Chapter 9: Mutation

```bash
# MUTATION 1: Use pyenv to manage multiple Python versions
curl https://pyenv.run | bash
# Add to ~/.bashrc:
# export PYENV_ROOT="$HOME/.pyenv"
# export PATH="$PYENV_ROOT/bin:$PATH"
# eval "$(pyenv init -)"

pyenv install 3.12.0
pyenv local 3.12.0    # Use 3.12 in this directory only

# MUTATION 2: Use uv (ultra-fast Python package manager, Rust-based)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv
source .venv/bin/activate
uv pip install requests rich

# MUTATION 3: Explore what's in the venv directory
ls -la ~/developer-workspace/project-alpha/venv/
ls -la ~/developer-workspace/project-alpha/venv/lib/
ls -la ~/developer-workspace/project-alpha/venv/lib/python3.*/site-packages/
# You'll see the actual package files — requests, rich, etc.
```

---

## Chapter 10: The Environment Hierarchy

Now you understand the full stack of your development environment:

```
Hardware (CPU, RAM, Disk)
    └── Linux Kernel (manages hardware)
        └── Shell (Bash) — you know this from B-001–B-004
            └── Package Manager (apt/pacman) — system-level software ← THIS BOOK
                └── Python 3.x — language runtime ← THIS BOOK
                    └── pip — Python package manager ← THIS BOOK
                        └── venv — project isolation ← THIS BOOK
                            └── Your Python code ← B-026+
```

Each layer isolates and controls the layer above it. This is the foundation every Python developer stands on.

---

## Chapter 11: What Comes Next

| Book | Title | What You'll Build |
|---|---|---|
| **B-006** | *The Process That Wouldn't Stop* | Process monitoring script in Bash |
| **B-007** | *The Network That Connected Everything* | First API call from the terminal |
| **B-008** | *Files That Never Get Lost* | First Git commit — version control |
| **B-026** | *Python: The Language That Does Everything* | Your first Python program with types |

---

## Appendix A: Quick Reference — Python Environment Commands

```bash
# Create venv
python3 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows CMD)
venv\Scripts\activate.bat

# Deactivate
deactivate

# Install package
pip install <package>

# Install from file
pip install -r requirements.txt

# Save environment
pip freeze > requirements.txt

# Show what's installed
pip list

# Remove venv (just delete the folder)
rm -rf venv/
```

---

## Further Reading

- 📄 [`docs/B-004-the-script-that-did-my-job.md`](B-004-the-script-that-did-my-job.md) — Bash skills used to set up this environment
- 📄 [`docs/linux-blockchain-educational-ecosystem.md`](linux-blockchain-educational-ecosystem.md) — Full Linux + blockchain curriculum
- 📄 [`docs/P011-STACK-001-repo-stack-profile.md`](P011-STACK-001-repo-stack-profile.md) — The full lippytm.ai technology stack
- 📄 [`docs/P011-EBOOK-000-course-series-master-plan.md`](P011-EBOOK-000-course-series-master-plan.md) — All 300 books
- 🏠 [`README.md`](../README.md) — Encyclopedia home

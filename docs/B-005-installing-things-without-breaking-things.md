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

## Chapter 12: Done-For-You Lessons

> *"The best tool setup is the one you never have to think about again — because it just works, on every machine, every time."*

Ten builds that turn package management from a source of confusion into a superpower you own and control.

| Icon | Format | What it is |
|---|---|---|
| 📘 | **Ebook** | Annotated command or architecture diagram |
| 🎧 | **Audiobook** | Narrator script — pause and build |
| 🎬 | **Video** | SHOW→BUILD→VERIFY terminal scene |

---

### DFY Lesson 1 — The pacman Cheat Card

**What you'll have:** A personal `pacman` quick-reference card covering install, remove, search, update, and audit.
**Time:** 10 minutes.

---

📘 **Ebook Figure**

```
pacman Quick Reference (Arch Linux / OMARCHY)
═══════════════════════════════════════════════

INSTALL
  pacman -S package          → install a package
  pacman -S pkg1 pkg2        → install multiple
  pacman -U file.pkg.tar.zst → install from local file

REMOVE
  pacman -R package          → remove (keep deps)
  pacman -Rs package         → remove + unused deps
  pacman -Rns package        → remove + deps + config files

UPDATE
  pacman -Syu                → sync + update all packages
  pacman -Sy                 → sync database only
  pacman -Su                 → update (database pre-synced)

SEARCH & INFO
  pacman -Ss keyword         → search repos
  pacman -Qs keyword         → search installed
  pacman -Si package         → info from repo
  pacman -Qi package         → info from installed
  pacman -Ql package         → list installed files

AUDIT
  pacman -Qe                 → explicitly installed packages
  pacman -Qdt                → orphaned dependencies
  pacman -Qo /path/to/file   → which package owns this file?
```

*Figure 12.1 — pacman is one of the most powerful package managers ever built. This card covers everything you'll need daily.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 1: The pacman Cheat Card.
>
> `pacman -Syu` keeps your entire system up to date. `pacman -Rs` removes a package AND everything it pulled in. `pacman -Qo` tells you which package owns any file on your system. These aren't obscure flags — they're the 20 commands that cover everything you'll do with your package manager for the next ten years. Build this card, keep it close, refer to it until they're automatic.
>
> Your deliverable is: a personal `pacman` reference card — install, remove, search, update, audit.
>
> Time to build: 10 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `pacman -Qo /usr/bin/git` → tells you exactly which package owns `git`. Instant.
- **BUILD:** Run each command family against a real package. Annotate what each does.
- **VERIFY:** `pacman -Qdt` → list orphaned packages. `pacman -Qe | wc -l` → count explicit installs.

---

### DFY Lesson 2 — Python venv Workflow Cheat Card

**What you'll have:** A printed or saved reference for the complete Python virtual environment lifecycle.
**Time:** 10 minutes.

---

📘 **Ebook Figure**

```
Python Virtual Environment Lifecycle
══════════════════════════════════════

CREATE
  python3 -m venv venv           → create in ./venv/
  python3 -m venv .venv          → hidden venv (preferred for projects)
  python3 -m venv --upgrade venv → upgrade in-place

ACTIVATE / DEACTIVATE
  source venv/bin/activate       → Linux/macOS
  deactivate                     → exit venv

INSPECT
  which python3                  → should show venv path when active
  python3 --version              → confirm Python version
  pip list                       → all installed packages
  pip show requests              → info for one package

INSTALL / MANAGE
  pip install requests           → install latest
  pip install requests==2.31.0   → install specific version
  pip install -r requirements.txt → install from file
  pip freeze > requirements.txt  → export all installed versions
  pip uninstall requests         → uninstall

BEST PRACTICES
  ✅  One venv per project
  ✅  Add venv/ and .venv/ to .gitignore
  ✅  Always pip freeze > requirements.txt before committing
  ❌  Never pip install into the system Python
```

*Figure 12.2 — A virtual environment is a bubble: everything inside stays inside, nothing leaks out.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 2: Python venv Workflow Cheat Card.
>
> The rule is simple: every Python project gets its own virtual environment, and you never install packages into the system Python. This card covers the complete lifecycle — create, activate, install, freeze, deactivate — in one reference you can print, pin to your wall, and refer to until the workflow is automatic. After this lesson, dependency conflicts stop being your problem.
>
> Your deliverable is: a Python venv lifecycle reference card — the complete workflow in one place.
>
> Time to build: 10 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** Two projects with conflicting `requests` versions — each in its own venv — both run without conflict.
- **BUILD:** Create venv. Activate. Install package. Freeze to requirements.txt. Deactivate.
- **VERIFY:** `which python3` outside venv → system Python. Inside venv → venv Python.

---

### DFY Lesson 3 — System Package Audit Script

**What you'll have:** `pkg-audit.sh` — shows all explicitly installed packages, orphans, and package age.
**Time:** 15 minutes.

---

📘 **Ebook Figure**

```bash
#!/usr/bin/env bash
# pkg-audit.sh — system package health report
echo "=== PACKAGE AUDIT REPORT — $(date +%F) ==="
echo ""
echo "--- Explicitly Installed ---"
pacman -Qe | wc -l
echo "  packages explicitly installed"
echo ""
echo "--- Orphaned Dependencies (safe to remove) ---"
pacman -Qdt 2>/dev/null || echo "  None. Clean."
echo ""
echo "--- Largest Packages ---"
pacman -Qi $(pacman -Qq) 2>/dev/null \
  | awk '/^Name/{name=$3} /^Installed Size/{print $4$5, name}' \
  | sort -rh | head -10
echo ""
echo "--- Recently Installed (last 10) ---"
grep "installed" /var/log/pacman.log | tail -10
```

*Figure 12.3 — Regular package audits keep your system lean, intentional, and free of forgotten dependencies.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 3: System Package Audit Script.
>
> Over time, systems accumulate packages: orphaned dependencies from software you removed, giant packages you forgot were installed, experimental tools you never cleaned up. This audit script gives you a full picture in one run — how many explicit installs, which packages are orphaned, which are the largest, and what was installed recently. Run it monthly as part of system maintenance.
>
> Your deliverable is: `pkg-audit.sh` — a complete system package health report.
>
> Time to build: 15 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `pkg-audit.sh` — 3 orphaned packages identified. Remove them. Re-run — clean.
- **BUILD:** Write script section by section. Test each `pacman` command standalone.
- **VERIFY:** Install a test package with a dependency. Uninstall it. Re-run audit — orphan appears.

---

### DFY Lesson 4 — AUR Helper Setup (yay)

**What you'll have:** `yay` installed and configured — access to 85,000+ community packages with one command.
**Time:** 20 minutes.

---

📘 **Ebook Figure**

```bash
# Install yay (Arch User Repository helper)
# Step 1: Install dependencies
sudo pacman -S --needed base-devel git

# Step 2: Clone yay
git clone https://aur.archlinux.org/yay.git /tmp/yay
cd /tmp/yay

# Step 3: Build and install
makepkg -si

# Step 4: Verify
yay --version

# Usage (same as pacman + AUR):
yay -S google-chrome         → AUR package
yay -S code                  → VS Code from AUR
yay -Syu                     → update pacman + AUR packages together
yay -Ps                       → print system stats
```

```
┌──────────────────────────────────────────────────┐
│ Official repos (pacman -S):  ~15,000 packages    │
│ AUR (yay -S):               ~85,000+ packages    │
│                              ──────────────────  │
│ Total with yay:             ~100,000+ packages   │
└──────────────────────────────────────────────────┘
```

*Figure 12.4 — yay is pacman with the AUR unlocked. Nearly any software you'll ever need is one command away.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 4: AUR Helper Setup (yay).
>
> The Arch User Repository contains over 85,000 packages — everything from niche developer tools to popular software like Google Chrome, VS Code, and Slack. yay is the bridge: it combines official repo packages and AUR packages into one unified `pacman`-style interface. After this lesson, software installation on Arch Linux becomes more powerful than any other distribution.
>
> Your deliverable is: `yay` installed and confirmed — the full AUR unlocked.
>
> Time to build: 20 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `yay -S google-chrome` → installs from AUR with no manual steps. `google-chrome &` → browser launches.
- **BUILD:** Clone yay. `makepkg -si`. Verify version. Install one AUR package.
- **VERIFY:** `yay -Syu` → updates both official and AUR packages in one command.

---

### DFY Lesson 5 — pip Requirements Management Script

**What you'll have:** `pip-sync.sh` — installs, audits, and cleans pip packages for a project in one command.
**Time:** 15 minutes.

---

📘 **Ebook Figure**

```bash
#!/usr/bin/env bash
set -euo pipefail
# pip-sync.sh — install, audit, and clean a Python project's dependencies
source ~/lib/colors.sh 2>/dev/null || true

PROJECT_DIR="${1:-.}"
VENV="$PROJECT_DIR/venv"
REQ="$PROJECT_DIR/requirements.txt"

# Activate or create venv
if [[ ! -d "$VENV" ]]; then
  info "Creating venv at $VENV..."
  python3 -m venv "$VENV"
fi
source "$VENV/bin/activate"

# Install from requirements.txt if it exists
if [[ -f "$REQ" ]]; then
  info "Installing from $REQ..."
  pip install -q -r "$REQ"
  success "All packages installed"
else
  warning "No requirements.txt found at $REQ"
fi

# Audit: check for outdated packages
info "Checking for outdated packages..."
pip list --outdated 2>/dev/null | tail -n +3 || echo "  All up to date."

# Freeze current state
pip freeze > "$REQ"
success "requirements.txt updated"
```

*Figure 12.5 — Reproducible environments start with a requirements.txt that's always current and always committed.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 5: pip Requirements Management Script.
>
> Running a Python project on a new machine should take one command. This script makes that true: create or activate the venv, install all dependencies from requirements.txt, check for outdated packages, and freeze the current state back to requirements.txt. Run it on every new machine and after every dependency change — and your Python environments stay reproducible.
>
> Your deliverable is: `pip-sync.sh` — one-command Python dependency management.
>
> Time to build: 15 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** Fresh machine, no venv. `pip-sync.sh ./my-project` → venv created, packages installed, requirements.txt updated.
- **BUILD:** Write script. Test on a project with requirements.txt. Test on one without.
- **VERIFY:** `pip list` inside activated venv matches contents of requirements.txt exactly.

---

### DFY Lesson 6 — Installed Packages Snapshot and Diff

**What you'll have:** `pkg-snap.sh` — save a package list snapshot and diff between any two dates.
**Time:** 15 minutes.

---

📘 **Ebook Figure**

```bash
#!/usr/bin/env bash
# pkg-snap.sh — snapshot and diff installed packages
SNAP_DIR="$HOME/.pkg-snapshots"
mkdir -p "$SNAP_DIR"

snapshot() {
  local snap="$SNAP_DIR/$(date +%Y%m%d).txt"
  pacman -Qe | sort > "$snap"
  echo "✅ Snapshot: $snap ($(wc -l < "$snap") packages)"
}

diff_snaps() {
  local files=($(ls -t "$SNAP_DIR"/*.txt 2>/dev/null))
  [[ ${#files[@]} -lt 2 ]] && echo "Need at least 2 snapshots" && return 1
  echo "=== Changes since ${files[1]} ==="
  diff "${files[1]}" "${files[0]}" | grep "^[<>]"
  echo "  < removed  |  > added"
}

case "${1:-snapshot}" in
  snapshot) snapshot ;;
  diff)     diff_snaps ;;
  *) echo "Usage: pkg-snap.sh [snapshot|diff]" ;;
esac
```

*Figure 12.6 — A package diff tells you exactly what changed between any two points in time — invaluable for debugging system behavior changes.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 6: Installed Packages Snapshot and Diff.
>
> 'My system was working fine last week, now this stops working' — that's when you need a package diff. This script saves a dated list of all explicitly installed packages. Run the diff and you'll see exactly what was installed or removed between then and now. Run a snapshot weekly and you'll always have a clean baseline to compare against.
>
> Your deliverable is: `pkg-snap.sh` — package snapshots with auditable diffs.
>
> Time to build: 15 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** Take snapshot. Install a test package. Snapshot again. `pkg-snap.sh diff` → new package shows in diff.
- **BUILD:** Write script. Test snapshot. Test diff.
- **VERIFY:** Remove the test package. Third snapshot. Diff shows it's gone.

---

### DFY Lesson 7 — Python Tool Installer Script

**What you'll have:** `install-python-tools.sh` — installs your standard Python toolbox in any new venv.
**Time:** 10 minutes.

---

📘 **Ebook Figure**

```bash
#!/usr/bin/env bash
set -euo pipefail
# install-python-tools.sh — standard Python developer toolbox
# Run after creating a new venv to get a consistent dev environment

TOOLS=(
  "black"          # code formatter
  "isort"          # import sorter
  "flake8"         # linter
  "mypy"           # type checker
  "pytest"         # test runner
  "pytest-cov"     # test coverage
  "ipython"        # interactive Python shell
  "httpx"          # HTTP client (modern requests)
  "python-dotenv"  # .env file support
  "rich"           # beautiful terminal output
)

echo "Installing Python developer toolbox..."
pip install -q "${TOOLS[@]}"
echo "✅ Installed: ${TOOLS[*]}"
echo ""
echo "Versions:"
for tool in black isort flake8 mypy pytest ipython; do
  version=$($tool --version 2>&1 | head -1)
  echo "  $tool: $version"
done
```

*Figure 12.7 — A consistent Python toolbox means every project starts with the same quality guardrails. black, flake8, mypy, pytest — these are the non-negotiables.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 7: Python Tool Installer Script.
>
> Every Python developer should have a standard toolbox: a formatter, a linter, a type checker, a test runner. This script installs all 10 of them into any venv in one command. When you start a new project, you run `install-python-tools.sh` right after creating the venv. Code quality infrastructure, installed before you write your first line of code.
>
> Your deliverable is: `install-python-tools.sh` — your complete Python toolbox in one command.
>
> Time to build: 10 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** Fresh venv. Run script. All 10 tools installed. `black --version` — confirmed.
- **BUILD:** Write script. Add your preferred tools. Test in a fresh venv.
- **VERIFY:** `pip list` shows all 10. Each tool's `--version` responds correctly.

---

### DFY Lesson 8 — Dotfiles Installer

**What you'll have:** `install-dotfiles.sh` — clones your dotfiles repo and creates all symlinks in one command.
**Time:** 20 minutes.

---

📘 **Ebook Figure**

```bash
#!/usr/bin/env bash
set -euo pipefail
# install-dotfiles.sh — clone dotfiles and link them to home directory
DOTFILES_REPO="https://github.com/lippytm/dotfiles.git"
DOTFILES_DIR="$HOME/.dotfiles"

# Clone
if [[ ! -d "$DOTFILES_DIR" ]]; then
  git clone "$DOTFILES_REPO" "$DOTFILES_DIR"
  echo "✅ Cloned to $DOTFILES_DIR"
fi

# Link
declare -A LINKS=(
  ["$DOTFILES_DIR/.bashrc"]="$HOME/.bashrc"
  ["$DOTFILES_DIR/.tmux.conf"]="$HOME/.tmux.conf"
  ["$DOTFILES_DIR/.gitconfig"]="$HOME/.gitconfig"
  ["$DOTFILES_DIR/nvim/"]="$HOME/.config/nvim"
)

for source in "${!LINKS[@]}"; do
  target="${LINKS[$source]}"
  ln -sfv "$source" "$target"
done
echo "✅ All dotfiles linked"
```

```
New machine setup becomes:
  1. pacman -S git bash
  2. ./install-dotfiles.sh
  3. Done — your exact environment, everywhere.
```

*Figure 12.8 — A dotfiles installer is a time machine: your exact environment on any machine in under 2 minutes.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 8: Dotfiles Installer.
>
> Setting up a new machine manually is a half-day project. With a dotfiles installer, it's two minutes. Clone the repo, run the script — every config file is in place, every alias is active, every tool is configured exactly the way you like it. This is the goal of everything you've built in B-001 through B-004: a single command that makes any machine yours.
>
> Your deliverable is: `install-dotfiles.sh` — your entire environment installed on any machine in 2 minutes.
>
> Time to build: 20 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** Fresh machine. `./install-dotfiles.sh` runs. Terminal opens — all aliases, colors, and config are there.
- **BUILD:** Create a `~/dotfiles/` directory. Move `.bashrc`, `.tmux.conf`, `.gitconfig` into it. Write installer. Create symlinks.
- **VERIFY:** Delete a symlink. Re-run installer — symlink recreated. Config unchanged.

---

### DFY Lesson 9 — System Restore Point Script

**What you'll have:** `restore-point.sh` — saves a full system state snapshot (packages + config) before major changes.
**Time:** 15 minutes.

---

📘 **Ebook Figure**

```bash
#!/usr/bin/env bash
set -euo pipefail
# restore-point.sh — system state snapshot before major changes
LABEL="${1:-manual}"
SNAP_DIR="$HOME/restore-points/$(date +%Y%m%d-%H%M%S)-$LABEL"
mkdir -p "$SNAP_DIR"

echo "📸 Creating restore point: $SNAP_DIR"

# Package lists
pacman -Qe > "$SNAP_DIR/packages-explicit.txt"
pacman -Qm > "$SNAP_DIR/packages-aur.txt" 2>/dev/null || true
echo "  ✅ Package list saved"

# Key config files
cp ~/.bashrc   "$SNAP_DIR/bashrc.bak"
cp ~/.gitconfig "$SNAP_DIR/gitconfig.bak" 2>/dev/null || true
cp ~/.tmux.conf "$SNAP_DIR/tmux.conf.bak" 2>/dev/null || true
echo "  ✅ Config files saved"

# System info
uname -a > "$SNAP_DIR/system-info.txt"
df -h    > "$SNAP_DIR/disk-usage.txt"
echo "  ✅ System info saved"

echo "✅ Restore point complete: $SNAP_DIR"
echo "  Reinstall with: pacman -S - < $SNAP_DIR/packages-explicit.txt"
```

*Figure 12.9 — A restore point takes 30 seconds. Recovering from a bad system update without one takes hours.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 9: System Restore Point Script.
>
> Before every major system update, before installing experimental software, before making any change you're not 100% sure about — run this script. It captures your package list, config files, and system state in a dated snapshot folder. If anything goes wrong, you have a complete record of what the system looked like before. 30 seconds of prevention for hours of recovery.
>
> Your deliverable is: `restore-point.sh` — a system state snapshot before any major change.
>
> Time to build: 15 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** `restore-point.sh pre-upgrade` → snapshot created. Run `pacman -Syu`. System upgrades.
- **BUILD:** Write script. Test with a label. Open the snapshot folder — all files present.
- **VERIFY:** `cat restore-points/*/packages-explicit.txt | wc -l` — count matches current `pacman -Qe | wc -l`.

---

### DFY Lesson 10 — New Machine Setup Playbook

**What you'll have:** `setup-machine.sh` — end-to-end new machine configuration in one idempotent script.
**Time:** 30 minutes.

---

📘 **Ebook Figure**

```bash
#!/usr/bin/env bash
set -euo pipefail
# setup-machine.sh — new machine playbook (idempotent)
# Run repeatedly — only does work that hasn't been done yet
source ~/lib/colors.sh 2>/dev/null || true

header "=== lippytmai Machine Setup ==="

# 1. System update
info "Step 1: System update..."
sudo pacman -Syu --noconfirm -q
success "System updated"

# 2. Install core tools
info "Step 2: Core tools..."
PACKAGES=(git neovim tmux htop ripgrep fd tree wget curl jq)
sudo pacman -S --needed --noconfirm "${PACKAGES[@]}" -q
success "Core tools installed"

# 3. Python setup
info "Step 3: Python..."
sudo pacman -S --needed --noconfirm python python-pip -q
success "Python ready"

# 4. Dotfiles
info "Step 4: Dotfiles..."
[[ ! -d "$HOME/.dotfiles" ]] && git clone https://github.com/lippytm/dotfiles.git "$HOME/.dotfiles"
~/bin/install-dotfiles.sh
success "Dotfiles linked"

# 5. SSH key
info "Step 5: SSH key..."
if [[ ! -f "$HOME/.ssh/id_ed25519.pub" ]]; then
  ssh-keygen -t ed25519 -C "lippytm@$(hostname)" -f "$HOME/.ssh/id_ed25519" -N ""
  success "SSH key generated: $(cat "$HOME/.ssh/id_ed25519.pub")"
  warning "Add above key to GitHub before pushing"
else
  success "SSH key exists"
fi

header "=== Setup Complete ==="
```

*Figure 12.10 — An idempotent setup script is safe to run repeatedly: it only does what hasn't been done. The mark of professional infrastructure.*

---

🎧 **Audiobook Callout**

> *[CALLOUT TONE]*
>
> "Done-For-You Moment. Lesson 10: New Machine Setup Playbook.
>
> This is the capstone build of B-005 and the culmination of everything in Phase 1's first five books. A single idempotent script that takes a fresh machine to fully configured — updated, core tools installed, Python ready, dotfiles linked, SSH key generated. Idempotent means safe to run multiple times: it checks what's already done and skips it. This is infrastructure-as-code for your personal workstation.
>
> Your deliverable is: `setup-machine.sh` — your complete new machine playbook in one command.
>
> Time to build: 30 minutes. Pause here. Build it. Then resume."
>
> *[CALLOUT TONE × 2]*

---

🎬 **Video Scene**

- **SHOW:** Fresh Arch Linux VM. `./setup-machine.sh` — all 5 steps run. Machine is production-ready.
- **BUILD:** Combine all DFY tools from B-001–B-005 into one orchestration script. Make each step idempotent.
- **VERIFY:** Run script a second time on the same machine — all steps say "already done" or "already installed". Zero errors.

---

> 🎓 **All 10 DFY lessons complete for B-005.** You've built: a `pacman` reference, a venv workflow card, a package auditor, `yay` (AUR access), pip sync automation, package snapshots, a Python toolbox installer, a dotfiles deployer, a restore point system, and a complete new machine setup playbook.
>
> **Together, B-001 through B-005 give you 50 real, working tools.** This is Phase 1 of the Earn-while-you-Learn track.
>
> **Next:** Claim your `CLL-L0-B005-PackageMaster` credential, then continue to B-006.

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

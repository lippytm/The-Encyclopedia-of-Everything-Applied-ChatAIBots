# B-035: Virtual Environments and pip

### venv, pip, requirements.txt, and the Reproducible Python Project

> *"A Python project without a virtual environment is a project waiting to break. Every serious Python project starts with python3 -m venv .venv — it is the single most important discipline in professional Python development. It ensures that your project's dependencies are isolated, reproducible, and portable."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Create, activate, and deactivate Python virtual environments with `venv`
2. Install, upgrade, and remove packages with `pip`
3. Produce and reproduce a `requirements.txt` dependency file
4. Understand `pyproject.toml` — the modern project configuration standard
5. Build a complete, reproducible Python project structure from scratch

**Prerequisite:** B-026 through B-034

**Build Artifact:** `~/developer-workspace/projects/python-foundations/` — a fully reproducible Python project with `venv`, `requirements.txt`, and `pyproject.toml`

**Credential:** `CCSLL-L1-B035-PythonEngineer` — on-chain on Base

---

## Chapter 1: Why Virtual Environments?

Without `venv`:
```bash
pip install requests        # installs globally
pip install requests==2.28  # different project needs older version
# CONFLICT — one version wins, the other project breaks
```

With `venv`:
```bash
# Project A
cd project-a && python3 -m venv .venv && source .venv/bin/activate
pip install requests==2.31   # isolated to project-a only

# Project B
cd project-b && python3 -m venv .venv && source .venv/bin/activate
pip install requests==2.28   # isolated to project-b only
# No conflict — each project has its own Python environment
```

---

## Chapter 2: Creating and Using Virtual Environments

```bash
# Create a venv
cd ~/developer-workspace/projects/python-foundations
python3 -m venv .venv

# What got created:
ls .venv/
# bin/  include/  lib/  pyvenv.cfg

# Activate (Linux/Mac/WSL2)
source .venv/bin/activate

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Your prompt changes to show the active venv:
# (.venv) charles@machine:~/developer-workspace/projects/python-foundations$

# Verify you're in the venv
which python3         # ~/developer-workspace/projects/python-foundations/.venv/bin/python3
python3 --version     # Python 3.12.x

# Deactivate when done
deactivate

# Delete the venv (just delete the folder — never commit it)
rm -rf .venv
```

---

## Chapter 3: pip — Installing Packages

```bash
# Always activate your venv FIRST, then use pip
source .venv/bin/activate

# Install a package
pip install requests

# Install a specific version
pip install requests==2.31.0

# Install with version constraints
pip install "requests>=2.28,<3.0"

# Install multiple packages at once
pip install requests pytest httpx

# Upgrade an installed package
pip install --upgrade requests

# Uninstall
pip uninstall requests

# List installed packages
pip list

# Show info about a package
pip show requests

# Search (deprecated — use pypi.org instead)
# pip search ...
```

---

## Chapter 4: requirements.txt — Reproducible Dependencies

```bash
# After installing all your packages:
pip freeze > requirements.txt

# See what was generated:
cat requirements.txt
# certifi==2024.2.2
# charset-normalizer==3.3.2
# idna==3.6
# requests==2.31.0
# urllib3==2.2.0
# pytest==8.1.1
# ... etc.

# On a new machine / new developer:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Exact same versions — every time, everywhere
```

**Two-tier requirements pattern** (best practice):

```bash
# requirements.in — what you directly depend on (loose)
# requests>=2.28
# pytest>=7.0
# httpx

# requirements.txt — pip freeze output (pinned, exact)
# certifi==2024.2.2
# requests==2.31.0
# ...
```

---

## Chapter 5: pyproject.toml — The Modern Standard

`pyproject.toml` (PEP 518, 621) replaces `setup.py` and `setup.cfg`:

```toml
# pyproject.toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "python-foundations"
version = "1.0.0"
description = "lippytmai Python Foundations — B-026 through B-035"
readme = "README.md"
requires-python = ">=3.10"
license = { text = "MIT" }
authors = [
    { name = "lippytmai", email = "ai@lippytm.ai" },
]

dependencies = [
    "requests>=2.28",
    "httpx>=0.24",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "mypy>=1.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]

[tool.mypy]
python_version = "3.12"
strict = true

[project.scripts]
lippytmai-python = "python_foundations.hello_lippytmai:main"
```

---

## Chapter 6: The Build — Complete Reproducible Project

```bash
# Full project setup from scratch
PROJECT="$HOME/developer-workspace/projects/python-foundations"
cd "$PROJECT"

# 1. Create venv
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install requests pytest pytest-cov httpx

# 3. Freeze requirements
pip freeze > requirements.txt
echo "requirements.txt generated:"
cat requirements.txt | head -10

# 4. Create project structure
mkdir -p {src,tests,docs}
touch src/__init__.py tests/__init__.py

# 5. Create .gitignore — NEVER commit .venv
cat > .gitignore << 'EOF'
# Virtual environment
.venv/
env/
venv/

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Test output
.pytest_cache/
.coverage
htmlcov/

# Environment files (B-011)
.env
*.env

# IDE
.vscode/
.idea/
*.swp
EOF

# 6. Create pyproject.toml
cat > pyproject.toml << 'EOF'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "python-foundations"
version = "0.1.0"
description = "lippytmai Python Foundations curriculum — B-026 through B-035"
requires-python = ">=3.10"

dependencies = [
    "requests>=2.28",
]

[project.optional-dependencies]
dev = ["pytest>=7.0", "pytest-cov>=4.0"]

[tool.pytest.ini_options]
testpaths = ["tests"]
EOF

# 7. Run tests
pytest tests/ -v --tb=short

echo ""
echo "✅ Reproducible Python project ready!"
echo "   Activate: source .venv/bin/activate"
echo "   Test:     pytest"
echo "   Install:  pip install -r requirements.txt"
```

---

## Chapter 7: The venv Workflow Cheat Sheet

```bash
# === Starting a new project ===
mkdir my-project && cd my-project
python3 -m venv .venv
source .venv/bin/activate    # always first
pip install <packages>
pip freeze > requirements.txt
echo ".venv/" >> .gitignore  # never commit venv

# === Returning to an existing project ===
cd my-project
source .venv/bin/activate
pip install -r requirements.txt   # if dependencies changed

# === Sharing with another developer ===
git clone <repo>
cd <repo>
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest   # verify everything works
```

---

## Chapter 8: Proof of Work

```bash
echo "=== B-035 Verification ==="
cd ~/developer-workspace/projects/python-foundations

# Show venv exists and is correct
echo "venv Python:"
.venv/bin/python3 --version

echo "Installed packages:"
.venv/bin/pip list | grep -E "requests|pytest|httpx"

echo "requirements.txt:"
cat requirements.txt | wc -l
echo "packages pinned"

echo "Project structure:"
ls -la
```

---

## 🐍 Phase 2 Batch 2 — Python Intermediate Complete

Books B-031–B-035 complete the second batch of Python Foundations:

| Book | Title | Build Artifact |
|---|---|---|
| B-031 | Errors That Tell the Truth | `robust_file_reader.py` |
| B-032 | The Internet in a Function | `api_client.py` |
| B-033 | Classes and Objects Made Simple | `bank_account.py` |
| B-034 | Testing Your Code | `tests/test_math_utils.py` |
| B-035 | Virtual Environments and pip | Complete project structure |

---

## Further Reading

- 📄 [`docs/B-005-installing-things-without-breaking-things.md`](B-005-installing-things-without-breaking-things.md) — venv basics from the Linux series
- 📄 [`docs/B-034-testing-your-code.md`](B-034-testing-your-code.md) — Running pytest inside the venv
- 📄 [`docs/B-011-environment-variables-and-secrets.md`](B-011-environment-variables-and-secrets.md) — .env files with Python projects
- 🏠 [`README.md`](../README.md) — Encyclopedia home

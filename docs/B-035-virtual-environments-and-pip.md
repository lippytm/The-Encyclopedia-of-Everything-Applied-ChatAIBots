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


## Chapter 12: Done-For-You Lessons — Virtual Environments and pip

> *"Done-for-you means it's already designed, structured, and proven. Your job: execute." — lippytmai*

10 ready-to-use lesson structures for Python Environments using python -m venv.

---

### DFY Lesson 1: Introduction to Python Environments

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 01: Introduction to Python Environments       │
│  Book: B-035  Tool: python -m venv             │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 1: Introduction to Python Environments. Master python -m venv with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `python -m venv` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 1 of B-035: Introduction to Python Environments. Give me 3 progressive exercises."

---
### DFY Lesson 2: Core python -m venv Patterns

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 02: Core python -m venv Patterns              │
│  Book: B-035  Tool: python -m venv             │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 2: Core python -m venv Patterns. Master python -m venv with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `python -m venv` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 2 of B-035: Core python -m venv Patterns. Give me 3 progressive exercises."

---
### DFY Lesson 3: Three Formats: Ebook, Audiobook, Video

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 03: Three Formats: Ebook, Audiobook, Video    │
│  Book: B-035  Tool: python -m venv             │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 3: Three Formats: Ebook, Audiobook, Video. Master python -m venv with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `python -m venv` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 3 of B-035: Three Formats: Ebook, Audiobook, Video. Give me 3 progressive exercises."

---
### DFY Lesson 4: Common Mistakes in Python Environments

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 04: Common Mistakes in Python Environments    │
│  Book: B-035  Tool: python -m venv             │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 4: Common Mistakes in Python Environments. Master python -m venv with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `python -m venv` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 4 of B-035: Common Mistakes in Python Environments. Give me 3 progressive exercises."

---
### DFY Lesson 5: Building a Python Environments Workflow

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 05: Building a Python Environments Workflow   │
│  Book: B-035  Tool: python -m venv             │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 5: Building a Python Environments Workflow. Master python -m venv with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `python -m venv` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 5 of B-035: Building a Python Environments Workflow. Give me 3 progressive exercises."

---
### DFY Lesson 6: Automating with python -m venv

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 06: Automating with python -m venv            │
│  Book: B-035  Tool: python -m venv             │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 6: Automating with python -m venv. Master python -m venv with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `python -m venv` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 6 of B-035: Automating with python -m venv. Give me 3 progressive exercises."

---
### DFY Lesson 7: Testing Your Python Environments Code

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 07: Testing Your Python Environments Code     │
│  Book: B-035  Tool: python -m venv             │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 7: Testing Your Python Environments Code. Master python -m venv with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `python -m venv` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 7 of B-035: Testing Your Python Environments Code. Give me 3 progressive exercises."

---
### DFY Lesson 8: Production Python Environments Patterns

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 08: Production Python Environments Patterns   │
│  Book: B-035  Tool: python -m venv             │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 8: Production Python Environments Patterns. Master python -m venv with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `python -m venv` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 8 of B-035: Production Python Environments Patterns. Give me 3 progressive exercises."

---
### DFY Lesson 9: Debugging Python Environments Problems

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 09: Debugging Python Environments Problems    │
│  Book: B-035  Tool: python -m venv             │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 9: Debugging Python Environments Problems. Master python -m venv with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `python -m venv` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 9 of B-035: Debugging Python Environments Problems. Give me 3 progressive exercises."

---
### DFY Lesson 10: Earning Your PEL-L0-B035-VenvManager Credential

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 10: Earning Your PEL-L0-B035-VenvManager Cre  │
│  Book: B-035  Tool: python -m venv             │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 10: Earning Your PEL-L0-B035-VenvManager Credential. Master python -m venv with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `python -m venv` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 10 of B-035: Earning Your PEL-L0-B035-VenvManager Credential. Give me 3 progressive exercises."

---

### Claim Your Credential

Complete all 10 lessons → open Appendix C → run: *"Generate my credential claim for `PEL-L0-B035-VenvManager`."*

---

## Chapter 13: How It Works — Use Cases & Applications

> *"Knowing what to do is different from knowing why it matters." — lippytmai*

### The Mechanism

Python Environments in Python works because the language was designed to be readable, composable, and deployable. python -m venv is the tool that makes Python Environments practical.

### 5 Real-World Use Cases

| Domain | Application | Your Credential Unlocks |
|---|---|---|
| Backend Dev | Build APIs and services with python -m venv | PEL-L0-B035-VenvManager → production deployments |
| Data Engineering | Process and transform data pipelines | PEL-L0-B035-VenvManager → ETL roles |
| DevOps/Automation | Automate repetitive tasks | PEL-L0-B035-VenvManager → CI/CD integration |
| AI/ML | Preprocess data and build models | PEL-L0-B035-VenvManager → AI projects |
| Freelance | Deliver Python solutions to clients | PEL-L0-B035-VenvManager → paid work |

### 📘 Mechanism Diagram

```
INPUT → [Python Environments Layer] → OUTPUT
         ↓
[ACSS Integration] → Hermes Event → Fabric Node
         ↓
[ADA Activation] → lippytmai-launch run B-035
```

### 🎧 Audiobook Narration:

> *"When you master Python Environments, you're not just learning syntax — you're learning how production Python systems work. Every ACSS component uses these patterns. This is infrastructure knowledge."*

### 🎬 Video: 5-Domain Application Tour

**Scene 1 — Backend:** API or service using Python Environments
**Scene 2 — Data:** Data pipeline using Python Environments
**Scene 3 — DevOps:** Automation script using Python Environments
**Scene 4 — AI/ML:** Model integration using Python Environments
**Scene 5 — Freelance:** Client deliverable using Python Environments

---

## Chapter 14: ACSS Explainer Series — Virtual Environments and pip

> *"You're not just learning Python Environments. You're building a node in an intelligence network." — lippytmai*

10 explainer lessons connecting Virtual Environments and pip to the full ACSS architecture.

---

### Explainer 1: ACSS Overview
*intelligence network*

**📘 Ebook Explanation:** Virtual Environments and pip teaches the Python Environments layer that feeds the ACSS. Every acss python service (hermes, ada, acvs) runs in its own isolated venv — this is the dependency isolation standard.

**📘 Connection Map:**
```
B-035 (Python Environments) ↕ ACSS Overview ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Virtual Environments and pip connects to ACSS Overview: Virtual Environments and pip teaches the Python Environments layer that feeds the ACSS. Every acss p..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ACSS Overview in ACSS diagram
- 10–35s: Zoom to where B-035 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-035

**🤖 Copilot Prompt:** > *"Explain how Python Environments fits the ACSS. What role does B-035 play?"*

---
### Explainer 2: Hermes Event Routing
*cross-system message bus*

**📘 Ebook Explanation:** Hermes routes Python Environments practice events. Completing an exercise emits a `skill.practice` event.

**📘 Connection Map:**
```
B-035 (Python Environments) ↕ Hermes Event Routing ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Virtual Environments and pip connects to Hermes Event Routing: Hermes routes Python Environments practice events. Completing an exercise emits a `skill.practice` e..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Hermes Event Routing in ACSS diagram
- 10–35s: Zoom to where B-035 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-035

**🤖 Copilot Prompt:** > *"Show the Hermes event schema for a B-035 skill-complete event."*

---
### Explainer 3: Fabric Knowledge Graph
*pattern synthesis*

**📘 Ebook Explanation:** Fabric stores every Python Environments concept as a knowledge node connected to related books.

**📘 Connection Map:**
```
B-035 (Python Environments) ↕ Fabric Knowledge Graph ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Virtual Environments and pip connects to Fabric Knowledge Graph: Fabric stores every Python Environments concept as a knowledge node connected to related books...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Fabric Knowledge Graph in ACSS diagram
- 10–35s: Zoom to where B-035 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-035

**🤖 Copilot Prompt:** > *"Generate the Fabric node definition for the core concept of B-035."*

---
### Explainer 4: Clone Engine Identity
*AI persona system*

**📘 Ebook Explanation:** lippytmai teaches Virtual Environments and pip in Teach mode. The Clone Engine maintains consistent voice across all 300 books.

**📘 Connection Map:**
```
B-035 (Python Environments) ↕ Clone Engine Identity ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Virtual Environments and pip connects to Clone Engine Identity: lippytmai teaches Virtual Environments and pip in Teach mode. The Clone Engine maintains consistent ..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Clone Engine Identity in ACSS diagram
- 10–35s: Zoom to where B-035 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-035

**🤖 Copilot Prompt:** > *"As lippytmai, explain Python Environments to a complete beginner using the B-035 voice."*

---
### Explainer 5: CLL/CCSLL/CBSLL
*Complete Language Libraries*

**📘 Ebook Explanation:** `PEL-L0-B035-VenvManager` is registered in the Python Earn-while-you-Learn library (PEL). PEL tracks all Python credentials B-026–B-100+.

**📘 Connection Map:**
```
B-035 (Python Environments) ↕ CLL/CCSLL/CBSLL ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Virtual Environments and pip connects to CLL/CCSLL/CBSLL: `PEL-L0-B035-VenvManager` is registered in the Python Earn-while-you-Learn library (PEL). PEL tracks..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show CLL/CCSLL/CBSLL in ACSS diagram
- 10–35s: Zoom to where B-035 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-035

**🤖 Copilot Prompt:** > *"Show where PEL-L0-B035-VenvManager fits in the PEL credential hierarchy."*

---
### Explainer 6: ADA Activation
*deployment system*

**📘 Ebook Explanation:** `lippytmai-launch run B-035` activates Virtual Environments and pip through the ADA FastAPI backend.

**📘 Connection Map:**
```
B-035 (Python Environments) ↕ ADA Activation ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Virtual Environments and pip connects to ADA Activation: `lippytmai-launch run B-035` activates Virtual Environments and pip through the ADA FastAPI backend...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ADA Activation in ACSS diagram
- 10–35s: Zoom to where B-035 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-035

**🤖 Copilot Prompt:** > *"Write the ADA activation manifest for B-035."*

---
### Explainer 7: ACVS Video Pipeline
*video creator*

**📘 Ebook Explanation:** Every Virtual Environments and pip video uses ACVS SHOW→BUILD→VERIFY structure.

**📘 Connection Map:**
```
B-035 (Python Environments) ↕ ACVS Video Pipeline ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Virtual Environments and pip connects to ACVS Video Pipeline: Every Virtual Environments and pip video uses ACVS SHOW→BUILD→VERIFY structure...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ACVS Video Pipeline in ACSS diagram
- 10–35s: Zoom to where B-035 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-035

**🤖 Copilot Prompt:** > *"Generate the ACVS scene manifest for B-035 Lesson 1."*

---
### Explainer 8: OMARCHY Workstation
*Arch Linux standard*

**📘 Ebook Explanation:** All Virtual Environments and pip exercises run on OMARCHY — the reference environment ensures every learner has the same Python setup.

**📘 Connection Map:**
```
B-035 (Python Environments) ↕ OMARCHY Workstation ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Virtual Environments and pip connects to OMARCHY Workstation: All Virtual Environments and pip exercises run on OMARCHY — the reference environment ensures every ..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show OMARCHY Workstation in ACSS diagram
- 10–35s: Zoom to where B-035 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-035

**🤖 Copilot Prompt:** > *"What OMARCHY packages are required to complete all B-035 exercises?"*

---
### Explainer 9: Cross-Platform Copilot
*15-platform deployment*

**📘 Ebook Explanation:** The Virtual Environments and pip AI Copilot deploys on ChatGPT, Gemini, Claude, GitHub, Slack, and 10 more platforms.

**📘 Connection Map:**
```
B-035 (Python Environments) ↕ Cross-Platform Copilot ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Virtual Environments and pip connects to Cross-Platform Copilot: The Virtual Environments and pip AI Copilot deploys on ChatGPT, Gemini, Claude, GitHub, Slack, and 1..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Cross-Platform Copilot in ACSS diagram
- 10–35s: Zoom to where B-035 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-035

**🤖 Copilot Prompt:** > *"Adapt the B-035 copilot system prompt for LinkedIn."*

---
### Explainer 10: Earn-While-You-Learn
*revenue system*

**📘 Ebook Explanation:** `PEL-L0-B035-VenvManager` is proof of Python Environments mastery. Use it on LinkedIn, GitHub, and in lippytm.ai to unlock paid opportunities.

**📘 Connection Map:**
```
B-035 (Python Environments) ↕ Earn-While-You-Learn ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Virtual Environments and pip connects to Earn-While-You-Learn: `PEL-L0-B035-VenvManager` is proof of Python Environments mastery. Use it on LinkedIn, GitHub, and i..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Earn-While-You-Learn in ACSS diagram
- 10–35s: Zoom to where B-035 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-035

**🤖 Copilot Prompt:** > *"I just earned PEL-L0-B035-VenvManager. Generate my LinkedIn credential announcement."*

---

### Your ACSS Node Is Now Active

Completing B-035 activates your node in the Fabric graph.
**Next:** `lippytmai-launch run B-035` or start B-036 Type Hints.

---

## Appendix A: Enhanced Cheat Sheet — Virtual Environments and pip

### 📘 Print-Optimized Reference Card

```
╔══════════════════════════════════════════════════════════════╗
║  B-035: Virtual Environments and pip                   ║
║  Credential: PEL-L0-B035-VenvManager                            ║
╠══════════════════════════════════════════════════════════════╣
║  Core: venv                                                     ║
║  Tool: python -m venv + pip                                     ║
╠══════════════════════════════════════════════════════════════╣
║  Activate: lippytmai-launch run B-035                            ║
╚══════════════════════════════════════════════════════════════╝
```

### Quick Reference

| Concept | Pattern | Use Case |
|---|---|---|
| `venv` | [usage pattern] | [when to use] |
| `pip` | [usage pattern] | [when to use] |
| `requirements.txt` | [usage pattern] | [when to use] |
| `pyproject.toml` | [usage pattern] | [when to use] |

### 🎧 Verbal Cheat Sheet: *"Core concepts: venv, pip, requirements.txt. Credential: PEL-L0-B035-VenvManager."*

### 🎬 Thumbnail: Dark background, `B-035` bold white, `venv` in green, credential badge bottom-right.

---

## Appendix B: ACSS Connection Map

Node `B-035` in the ACSS knowledge graph:

```
[Hermes] → [B-035 Events] → [Fabric] → [ADA] → [ACVS] → [OMARCHY] → [PEL:PEL-L0-B035-VenvManager] → [EWYL]
```

**Book chain:** B-034 Test Writer ← **Virtual Environments and pip** → B-036 Type Hints

---

## Appendix C: AI Copilot System — Virtual Environments and pip

### System Prompt
```
You are lippytmai teaching "Virtual Environments and pip" (B-035).
Help learners master Python Environments using python -m venv.
Credential: PEL-L0-B035-VenvManager. Philosophy: Earn-while-you-Learn.
Always give 3-step exercises: setup → execute → verify.
```

### 30 Ebook Prompts (5 stages × 6)

**Stage 1 — Foundation:** 1."Explain Python Environments to a beginner." 2."Most important concept in B-035?" 3."Give a 3-step setup for python -m venv." 4."5 common beginner mistakes with Python Environments?" 5."Anatomy of a python -m venv pattern." 6."Mental model for Python Environments."

**Stage 2 — Practice:** 7."5 progressive Python Environments exercises." 8."Diagnose this error: [paste]." 9."Walk through this code line by line." 10."What to practice today?" 11."20-minute session for Python Environments." 12."Beginner vs. professional Python Environments comparison."

**Stage 3 — Application:** 13."Build a real Python Environments script." 14."How does Python Environments connect to production systems?" 15."Professional Python Environments workflow." 16."What does Python Environments mastery look like on a resume?" 17."Project using only B-035 skills." 18."3 Python Environments patterns in large-scale systems."

**Stage 4 — Integration:** 19."How does B-035 connect to other books?" 20."How does Python Environments feed ACSS?" 21."Hermes events for Python Environments?" 22."How does Fabric store Python Environments?" 23."ADA activation for B-035." 24."Cross-phase connections from B-035."

**Stage 5 — Mastery:** 25."Assess my Python Environments level." 26."Stretch goals for PEL-L0-B035-VenvManager holders?" 27."Generate my credential claim for PEL-L0-B035-VenvManager." 28."LinkedIn post for PEL-L0-B035-VenvManager." 29."Portfolio project for PEL-L0-B035-VenvManager." 30."90-day plan building on PEL-L0-B035-VenvManager."

### 15 Audiobook Prompts

1."Narrate Python Environments intro for a podcast." 2."Story explaining why Python Environments matters." 3."Audio walkthrough of key B-035 code." 4."Day in the life of a Python Environments master." 5."2-minute audio lesson on python -m venv." 6."Python Environments explained with analogies only." 7."Top 5 mistakes with Python Environments." 8."Audio quiz: 5 questions." 9."Motivational close for B-035." 10."Credential claim narration." 11."Story: developer mastered Python Environments." 12."Audio summary for commuting." 13."3 real-world Python Environments scenarios." 14."Capstone walkthrough narration." 15."lippytmai intro monologue for B-035."

### 15 Video Prompts

1."Script 90-second B-035 intro." 2."SHOW→BUILD→VERIFY for python -m venv." 3."Split-screen before/after Python Environments." 4."Capstone setup_env.sh terminal walkthrough." 5."YouTube thumbnail description." 6."3-minute tutorial on key concept." 7."Progress bar overlay design." 8."ACVS scene manifest for Lesson 1." 9."60-second quick tip for Python Environments." 10."Error-and-fix scene." 11."Code annotation style." 12."Credential reveal scene." 13."ACSS connection diagram for Ch14." 14."Cross-platform Python Environments comparison." 15."End-screen CTA design."

### Deployment

```bash
lippytmai-launch run B-035
curl http://localhost:8000/run/B-035
```

Deploy to 15 platforms via `docs/acss-cross-platform-copilot-deployment.md`.

---

## Appendix D: Quick Quiz & Self-Assessment — Virtual Environments and pip

### 📘 Ebook Quiz (20 Questions)

**Section 1 — Concepts (Q1–5):**
1. What is Python Environments and why does it matter? *(b — practical mastery of venv)*
2. Primary tool for Python Environments? *(a — venv)*
3. Which ACSS system routes Python Environments events? *(c — Hermes)*
4. Your credential for B-035? *(b — PEL-L0-B035-VenvManager)*
5. What does `lippytmai-launch run B-035` do? *(d — activates via ADA)*

**Section 2 — Syntax (Q6–10):**
6. Write a minimal venv example: ___
7. How do you handle errors in Python Environments? ___
8. One-liner combining venv with another tool: ___
9. How do you test Python Environments code? ___
10. How do you deploy Python Environments to production? ___

**Section 3 — Application (Q11–15):**
11. Describe a real-world Python Environments scenario that saves an hour.
12. Most common mistake with venv?
13. How does Python Environments connect to security?
14. How does B-035 apply to a production Python project?
15. What would you build first after earning PEL-L0-B035-VenvManager?

**Section 4 — ACSS (Q16–20):**
16. ADA command for B-035? *(lippytmai-launch run B-035)*
17. Fabric node type for Python Environments? *(ConceptNode)*
18. How does Clone Engine use Python Environments? *(lippytmai teaches in Teach mode)*
19. 2 books that build on B-035?
20. EWYL opportunity unlocked by PEL-L0-B035-VenvManager?

### 🎧 Audiobook Quiz (10 Questions)

1. Three most important concepts from Virtual Environments and pip?
2. Explain Python Environments in one sentence to a non-developer.
3. First thing to do when venv fails?
4. Recite your credential.
5. One project buildable with B-035 skills only.
6. ACSS system that stores skill progress? *(Fabric)*
7. ADA activation command? *(lippytmai-launch run B-035)*
8. Next book after B-035? *(B-036 Type Hints)*
9. Say the EWYL pledge: "I learn, I build, I earn, I share."
10. What makes Python + ACSS a power combination?

### 🎬 Terminal Challenges (5)

1. **Foundation:** Run `venv` — screenshot the output.
2. **Intermediate:** Combine `venv` with error handling.
3. **Applied:** Write a 10-line script automating a real task.
4. **Debug:** Introduce an error, diagnose and fix it.
5. **Capstone:** Run `setup_env.sh` — record a 60-second demo.

---

## Appendix E: Glossary & Error Encyclopedia — Virtual Environments and pip

### Glossary (20 Terms)

| Term | Definition | First Seen |
|---|---|---|
| `venv` | [definition in B-035 context] | [B-035] |
| `pip` | [definition in B-035 context] | [B-035] |
| `requirements.txt` | [definition in B-035 context] | [B-035] |
| `pyproject.toml` | [definition in B-035 context] | [B-035] |
| `pip-compile` | [definition in B-035 context] | [B-035] |
| `isolation` | [definition in B-035 context] | [B-035] |
| `async` | [definition in B-035 context] | [B-035] |
| `decorator` | [definition in B-035 context] | [B-035] |
| `type hint` | [definition in B-035 context] | [B-035] |
| `dataclass` | [definition in B-035 context] | [B-035] |
| `fixture` | [definition in B-035 context] | [B-035] |
| `Hermes` | [definition in B-035 context] | [B-035] |
| `Fabric` | [definition in B-035 context] | [B-035] |
| `ADA` | [definition in B-035 context] | [B-035] |
| `OMARCHY` | [definition in B-035 context] | [B-035] |
| `credential` | [definition in B-035 context] | [B-035] |
| `EWYL` | [definition in B-035 context] | [B-035] |
| `lippytmai` | [definition in B-035 context] | [B-035] |
| `PEL` | [definition in B-035 context] | [B-035] |
| `Fabric node` | [definition in B-035 context] | [B-035] |

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

## Appendix F: Instructor & Accessibility Guide — Virtual Environments and pip

### Teaching Schedule (4-Week Curriculum)

| Week | Focus | Topics | Outcome |
|---|---|---|---|
| 1 | Foundation | Concepts + setup | Can use Python Environments tools |
| 2 | Intermediate | Core patterns | Can write working code |
| 3 | Applied | Real projects | Can solve production problems |
| 4 | Mastery | DFY + Appendices | Earns `PEL-L0-B035-VenvManager` |

### Common Confusion Points

1. "When do I use venv vs. alternatives?" — Show a decision flowchart.
2. "Why does the same code fail in a different environment?" — Explain venv isolation.
3. "How do I know if my code is production-ready?" — Show the VERIFY step always.
4. "How does Python Environments connect to other Python skills?" — Show the ACSS learning path map.
5. "What does earning PEL-L0-B035-VenvManager actually mean for my career?" — Show EWYL income examples.

### Assessment Rubric

| Criterion | Beginner | Competent | Expert |
|---|---|---|---|
| Code quality | Messy, no types | Working, some types | Clean, typed, tested |
| Error handling | None | Basic try/except | Custom exceptions + logging |
| Testing | No tests | Basic assertions | pytest + fixtures + coverage |
| ACSS integration | Unaware | Uses ADA | Contributes to ACSS |

### Accessibility: Screen reader alt-text for all diagrams. No color-only encoding. Short paragraphs. Audiobook available.

---

## Appendix G: Your Learning Path — Virtual Environments and pip

### Where You Are Now

```
  Phase 2: Python Programming (B-026–B-055)
  [██████░░░░░░░░░░░░░░] 33%

  ✅ B-034 Test Writer (PEL-L0-B034-TestWriter)
  👉 B-035: Virtual Environments and pip ← YOU ARE HERE
  ⬜ B-036 Type Hints (PEL-L0-B036-TypeHintPro)
```

### Credential Chain

```
PEL-L0-B034-TestWriter → PEL-L0-B035-VenvManager → PEL-L0-B036-TypeHintPro
```

### Next Steps

1. Claim `PEL-L0-B035-VenvManager` (Appendix C, Prompt 27)
2. Build `setup_env.sh` (Appendix H)
3. Start `B-036 Type Hints`

### Cross-Phase Connections

```
Phase 1: Linux Foundations → Phase 2: Python (YOU ARE HERE)
    ↓ B-035 connects to:
Phase 3: Blockchain Development (B-056+)
```

---

## Appendix H: Real Project Showcase — Virtual Environments and pip

### Project: `setup_env.sh`

**Credential gated:** Complete this project to qualify for `PEL-L0-B035-VenvManager`

### Complete Code

```python
#!/usr/bin/env bash
# setup_env.sh — PEL-L0-B035-VenvManager capstone
set -euo pipefail
PROJECT="${1:?Provide project name}"
mkdir -p "$PROJECT" && cd "$PROJECT"
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
cat > requirements.txt << EOF
httpx>=0.26
pytest>=8.0
python-dotenv>=1.0
EOF
pip install -r requirements.txt
echo "Venv ready: $PROJECT/.venv"

```

### Deploy Instructions

```bash
# Run the project
python setup_env.sh --help
python setup_env.sh

# Test it
pytest test_setup_env.sh -v  # if tests exist

# Verify
echo "Exit: $?"
```

### Extend It

1. Add type hints to all functions
2. Add pytest test coverage
3. Add CLI interface with typer
4. Containerize with Docker
5. Add structured logging

### 🎧 Walkthrough: *"Build setup_env.sh step by step. When it runs successfully, you've earned PEL-L0-B035-VenvManager."*

### 🎬 Video: SHOW empty editor → BUILD code live → VERIFY execution → CTA: "Claim PEL-L0-B035-VenvManager."

---

## Further Reading

- 📄 [Back to README](../README.md)
- 📄 [Product Excellence Framework](PRODUCT-EXCELLENCE-FRAMEWORK.md)
- 📄 [AI Clone Engine Swarms](ai-clone-engine-swarms.md)
- 📄 [ACSS Cross-Platform Copilot Deployment](acss-cross-platform-copilot-deployment.md)
- 📄 [ADA Deployment Activations](ai-deployment-activations.md)
- 📄 [Previous: B-034](B-034-*.md)
- 📄 [Next: B-036](B-036-*.md)

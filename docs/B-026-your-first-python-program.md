# B-026: Your First Python Program

### Hello, lippytm.ai — Python Install, REPL, Variables, and Your First Script

> *"Every Python program that has ever mattered started with the same thing: one line that did something. Python's design principle is that there should be one obvious way to do things. Learn that one obvious way, and everything else follows."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Install Python 3 correctly on Linux, macOS, and Windows (WSL2)
2. Use the Python REPL as an interactive calculator and experiment space
3. Write, save, and run your first Python script
4. Understand variables, data types, and `print()` output formatting
5. Build `hello-lippytmai.py` — a script that greets the user with system info

**Prerequisite:** B-001 through B-025 (Linux Foundations)

**Build Artifact:** `~/developer-workspace/projects/python-foundations/hello-lippytmai.py`

**Credential:** `CCSLL-L0-B026-PythonApprentice` — on-chain on Base

---

## Chapter 1: Why Python?

Python is the lingua franca of AI, data science, automation, and modern backend development. Every component of the ACSS uses Python:

| ACSS System | Python Role |
|---|---|
| **Hermes** | Event routing agents — FastAPI, asyncio |
| **Fabric** | Knowledge graph queries — NetworkX, LangChain |
| **ACVS** | `ACVSScriptAgent`, `SandboxSession` |
| **ADA** | FastAPI server, ElevenLabs audiobook pipeline |
| **Trading Bots** | ML signals, RL agents, execution layer |

*[Reality — Python is consistently ranked #1 or #2 in every major language popularity index (TIOBE, Stack Overflow, GitHub)]*

---

## Chapter 2: Installing Python

```bash
# On Ubuntu/Debian (including WSL2):
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# Verify
python3 --version      # Python 3.12.x
pip3 --version
which python3          # /usr/bin/python3

# On Arch Linux (B-017):
sudo pacman -S python python-pip

# Useful: make 'python' point to python3
# (many modern systems do this automatically)
which python           # if not found:
echo "alias python=python3" >> ~/.bashrc
echo "alias pip=pip3" >> ~/.bashrc
source ~/.bashrc
python --version
```

---

## Chapter 3: The Python REPL

REPL = Read-Eval-Print-Loop. Type Python, see results instantly:

```python
# Launch the REPL
python3

# >>> is the Python prompt
>>> print("Hello, lippytm.ai!")
Hello, lippytm.ai!

>>> 2 + 2
4

>>> 10 / 3
3.3333333333333335

>>> 10 // 3    # floor division
3

>>> 10 % 3     # modulo (remainder)
1

>>> 2 ** 10    # exponent
1024

>>> "lippytm" + ".ai"
'lippytm.ai'

>>> "echo" * 3
'echoechoecho'

>>> type(42)
<class 'int'>

>>> type(3.14)
<class 'float'>

>>> type("hello")
<class 'str'>

>>> type(True)
<class 'bool'>

# Exit the REPL
>>> exit()
# or Ctrl+D
```

---

## Chapter 4: Variables and Data Types

```python
# Variables — no type declaration needed
name = "Charles"
age = 42
temperature = 98.6
is_engineer = True
nothing = None

# Python's four core scalar types
print(type(name))          # <class 'str'>
print(type(age))           # <class 'int'>
print(type(temperature))   # <class 'float'>
print(type(is_engineer))   # <class 'bool'>

# Naming conventions (PEP 8)
user_name = "charles"      # snake_case for variables and functions
MAX_RETRIES = 3            # UPPER_SNAKE for constants
ClassName = "example"      # PascalCase for classes

# Multiple assignment
x, y, z = 1, 2, 3
first, *rest = [1, 2, 3, 4, 5]
print(first)   # 1
print(rest)    # [2, 3, 4, 5]
```

---

## Chapter 5: print() — Communicating with the World

```python
# Basic print
print("Hello, World!")

# f-strings (the modern way — Python 3.6+)
name = "Charles"
language = "Python"
version = 3.12
print(f"Hello, {name}! Using {language} {version}")

# Multi-line f-string
book_id = "B-026"
credential = "CCSLL-L0-B026-PythonApprentice"
print(f"""
Book:       {book_id}
Credential: {credential}
Status:     Active
""")

# Formatting numbers
pi = 3.14159265358979
print(f"Pi to 2 decimal places: {pi:.2f}")
print(f"Pi to 4 decimal places: {pi:.4f}")

count = 1_000_000
print(f"Count: {count:,}")     # 1,000,000 with comma separator

# print() separators and end
print("A", "B", "C", sep="-")      # A-B-C
print("Loading", end="")
print("...Done")                    # Loading...Done
```

---

## Chapter 6: Your First Real Python Script

```bash
# Create the project
mkcd ~/developer-workspace/projects/python-foundations
touch hello-lippytmai.py
nvim hello-lippytmai.py  # or nano, or any editor
```

```python
#!/usr/bin/env python3
"""
hello-lippytmai.py — B-026 Build Artifact

A greeting script that combines Python fundamentals with real system info.
The first milestone of the CCSLL Python Foundations curriculum.
"""

import platform
import datetime
import os


def get_system_info() -> dict:
    """Collect basic system information."""
    return {
        "hostname":    platform.node(),
        "os":          platform.system(),
        "os_release":  platform.release(),
        "python":      platform.python_version(),
        "user":        os.environ.get("USER", os.environ.get("USERNAME", "unknown")),
        "timestamp":   datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def greet(name: str, info: dict) -> str:
    """Build the greeting message."""
    return f"""
╔══════════════════════════════════════════════╗
║       Hello, {name}! Welcome to Python.       
║
║  System:  {info['os']} {info['os_release']}
║  Host:    {info['hostname']}
║  Python:  {info['python']}
║  User:    {info['user']}
║  Time:    {info['timestamp']}
║
║  Book:    B-026 — Your First Python Program
║  Cred:    CCSLL-L0-B026-PythonApprentice
╚══════════════════════════════════════════════╝
"""


def main() -> None:
    """Entry point."""
    name = input("What's your name? ").strip() or "lippytm.ai"
    info = get_system_info()
    print(greet(name, info))
    print("Phase 2 has begun. Python Foundations — Book 1 of 25.")


if __name__ == "__main__":
    main()
```

```bash
chmod +x hello-lippytmai.py
python3 hello-lippytmai.py
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-026 Verification ==="
python3 --version
python3 -c "import platform; print(f'Python {platform.python_version()} on {platform.system()}')"
python3 ~/developer-workspace/projects/python-foundations/hello-lippytmai.py
```

---


## Chapter 12: Done-For-You Lessons — Your First Python Program

> *"Done-for-you means it's already designed, structured, and proven. Your job: execute." — lippytmai*

10 ready-to-use lesson structures for Python Basics using python3.

---

### DFY Lesson 1: Introduction to Python Basics

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 01: Introduction to Python Basics             │
│  Book: B-026  Tool: python3                    │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 1: Introduction to Python Basics. Master python3 with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `python3` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 1 of B-026: Introduction to Python Basics. Give me 3 progressive exercises."

---
### DFY Lesson 2: Core python3 Patterns

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 02: Core python3 Patterns                     │
│  Book: B-026  Tool: python3                    │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 2: Core python3 Patterns. Master python3 with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `python3` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 2 of B-026: Core python3 Patterns. Give me 3 progressive exercises."

---
### DFY Lesson 3: Three Formats: Ebook, Audiobook, Video

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 03: Three Formats: Ebook, Audiobook, Video    │
│  Book: B-026  Tool: python3                    │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 3: Three Formats: Ebook, Audiobook, Video. Master python3 with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `python3` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 3 of B-026: Three Formats: Ebook, Audiobook, Video. Give me 3 progressive exercises."

---
### DFY Lesson 4: Common Mistakes in Python Basics

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 04: Common Mistakes in Python Basics          │
│  Book: B-026  Tool: python3                    │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 4: Common Mistakes in Python Basics. Master python3 with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `python3` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 4 of B-026: Common Mistakes in Python Basics. Give me 3 progressive exercises."

---
### DFY Lesson 5: Building a Python Basics Workflow

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 05: Building a Python Basics Workflow         │
│  Book: B-026  Tool: python3                    │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 5: Building a Python Basics Workflow. Master python3 with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `python3` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 5 of B-026: Building a Python Basics Workflow. Give me 3 progressive exercises."

---
### DFY Lesson 6: Automating with python3

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 06: Automating with python3                   │
│  Book: B-026  Tool: python3                    │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 6: Automating with python3. Master python3 with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `python3` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 6 of B-026: Automating with python3. Give me 3 progressive exercises."

---
### DFY Lesson 7: Testing Your Python Basics Code

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 07: Testing Your Python Basics Code           │
│  Book: B-026  Tool: python3                    │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 7: Testing Your Python Basics Code. Master python3 with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `python3` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 7 of B-026: Testing Your Python Basics Code. Give me 3 progressive exercises."

---
### DFY Lesson 8: Production Python Basics Patterns

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 08: Production Python Basics Patterns         │
│  Book: B-026  Tool: python3                    │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 8: Production Python Basics Patterns. Master python3 with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `python3` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 8 of B-026: Production Python Basics Patterns. Give me 3 progressive exercises."

---
### DFY Lesson 9: Debugging Python Basics Problems

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 09: Debugging Python Basics Problems          │
│  Book: B-026  Tool: python3                    │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 9: Debugging Python Basics Problems. Master python3 with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `python3` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 9 of B-026: Debugging Python Basics Problems. Give me 3 progressive exercises."

---
### DFY Lesson 10: Earning Your PEL-L0-B026-PythonBeginner Credential

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 10: Earning Your PEL-L0-B026-PythonBeginner   │
│  Book: B-026  Tool: python3                    │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 10: Earning Your PEL-L0-B026-PythonBeginner Credential. Master python3 with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `python3` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 10 of B-026: Earning Your PEL-L0-B026-PythonBeginner Credential. Give me 3 progressive exercises."

---

### Claim Your Credential

Complete all 10 lessons → open Appendix C → run: *"Generate my credential claim for `PEL-L0-B026-PythonBeginner`."*

---

## Chapter 13: How It Works — Use Cases & Applications

> *"Knowing what to do is different from knowing why it matters." — lippytmai*

### The Mechanism

Python Basics in Python works because the language was designed to be readable, composable, and deployable. python3 is the tool that makes Python Basics practical.

### 5 Real-World Use Cases

| Domain | Application | Your Credential Unlocks |
|---|---|---|
| Backend Dev | Build APIs and services with python3 | PEL-L0-B026-PythonBeginner → production deployments |
| Data Engineering | Process and transform data pipelines | PEL-L0-B026-PythonBeginner → ETL roles |
| DevOps/Automation | Automate repetitive tasks | PEL-L0-B026-PythonBeginner → CI/CD integration |
| AI/ML | Preprocess data and build models | PEL-L0-B026-PythonBeginner → AI projects |
| Freelance | Deliver Python solutions to clients | PEL-L0-B026-PythonBeginner → paid work |

### 📘 Mechanism Diagram

```
INPUT → [Python Basics Layer] → OUTPUT
         ↓
[ACSS Integration] → Hermes Event → Fabric Node
         ↓
[ADA Activation] → lippytmai-launch run B-026
```

### 🎧 Audiobook Narration:

> *"When you master Python Basics, you're not just learning syntax — you're learning how production Python systems work. Every ACSS component uses these patterns. This is infrastructure knowledge."*

### 🎬 Video: 5-Domain Application Tour

**Scene 1 — Backend:** API or service using Python Basics
**Scene 2 — Data:** Data pipeline using Python Basics
**Scene 3 — DevOps:** Automation script using Python Basics
**Scene 4 — AI/ML:** Model integration using Python Basics
**Scene 5 — Freelance:** Client deliverable using Python Basics

---

## Chapter 14: ACSS Explainer Series — Your First Python Program

> *"You're not just learning Python Basics. You're building a node in an intelligence network." — lippytmai*

10 explainer lessons connecting Your First Python Program to the full ACSS architecture.

---

### Explainer 1: ACSS Overview
*intelligence network*

**📘 Ebook Explanation:** Your First Python Program teaches the Python Basics layer that feeds the ACSS. Python is the primary language for all acss agents — hermes, fabric, and ada are all written in python.

**📘 Connection Map:**
```
B-026 (Python Basics) ↕ ACSS Overview ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Your First Python Program connects to ACSS Overview: Your First Python Program teaches the Python Basics layer that feeds the ACSS. Python is the primary..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ACSS Overview in ACSS diagram
- 10–35s: Zoom to where B-026 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-026

**🤖 Copilot Prompt:** > *"Explain how Python Basics fits the ACSS. What role does B-026 play?"*

---
### Explainer 2: Hermes Event Routing
*cross-system message bus*

**📘 Ebook Explanation:** Hermes routes Python Basics practice events. Completing an exercise emits a `skill.practice` event.

**📘 Connection Map:**
```
B-026 (Python Basics) ↕ Hermes Event Routing ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Your First Python Program connects to Hermes Event Routing: Hermes routes Python Basics practice events. Completing an exercise emits a `skill.practice` event...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Hermes Event Routing in ACSS diagram
- 10–35s: Zoom to where B-026 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-026

**🤖 Copilot Prompt:** > *"Show the Hermes event schema for a B-026 skill-complete event."*

---
### Explainer 3: Fabric Knowledge Graph
*pattern synthesis*

**📘 Ebook Explanation:** Fabric stores every Python Basics concept as a knowledge node connected to related books.

**📘 Connection Map:**
```
B-026 (Python Basics) ↕ Fabric Knowledge Graph ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Your First Python Program connects to Fabric Knowledge Graph: Fabric stores every Python Basics concept as a knowledge node connected to related books...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Fabric Knowledge Graph in ACSS diagram
- 10–35s: Zoom to where B-026 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-026

**🤖 Copilot Prompt:** > *"Generate the Fabric node definition for the core concept of B-026."*

---
### Explainer 4: Clone Engine Identity
*AI persona system*

**📘 Ebook Explanation:** lippytmai teaches Your First Python Program in Teach mode. The Clone Engine maintains consistent voice across all 300 books.

**📘 Connection Map:**
```
B-026 (Python Basics) ↕ Clone Engine Identity ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Your First Python Program connects to Clone Engine Identity: lippytmai teaches Your First Python Program in Teach mode. The Clone Engine maintains consistent voi..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Clone Engine Identity in ACSS diagram
- 10–35s: Zoom to where B-026 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-026

**🤖 Copilot Prompt:** > *"As lippytmai, explain Python Basics to a complete beginner using the B-026 voice."*

---
### Explainer 5: CLL/CCSLL/CBSLL
*Complete Language Libraries*

**📘 Ebook Explanation:** `PEL-L0-B026-PythonBeginner` is registered in the Python Earn-while-you-Learn library (PEL). PEL tracks all Python credentials B-026–B-100+.

**📘 Connection Map:**
```
B-026 (Python Basics) ↕ CLL/CCSLL/CBSLL ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Your First Python Program connects to CLL/CCSLL/CBSLL: `PEL-L0-B026-PythonBeginner` is registered in the Python Earn-while-you-Learn library (PEL). PEL tra..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show CLL/CCSLL/CBSLL in ACSS diagram
- 10–35s: Zoom to where B-026 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-026

**🤖 Copilot Prompt:** > *"Show where PEL-L0-B026-PythonBeginner fits in the PEL credential hierarchy."*

---
### Explainer 6: ADA Activation
*deployment system*

**📘 Ebook Explanation:** `lippytmai-launch run B-026` activates Your First Python Program through the ADA FastAPI backend.

**📘 Connection Map:**
```
B-026 (Python Basics) ↕ ADA Activation ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Your First Python Program connects to ADA Activation: `lippytmai-launch run B-026` activates Your First Python Program through the ADA FastAPI backend...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ADA Activation in ACSS diagram
- 10–35s: Zoom to where B-026 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-026

**🤖 Copilot Prompt:** > *"Write the ADA activation manifest for B-026."*

---
### Explainer 7: ACVS Video Pipeline
*video creator*

**📘 Ebook Explanation:** Every Your First Python Program video uses ACVS SHOW→BUILD→VERIFY structure.

**📘 Connection Map:**
```
B-026 (Python Basics) ↕ ACVS Video Pipeline ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Your First Python Program connects to ACVS Video Pipeline: Every Your First Python Program video uses ACVS SHOW→BUILD→VERIFY structure...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ACVS Video Pipeline in ACSS diagram
- 10–35s: Zoom to where B-026 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-026

**🤖 Copilot Prompt:** > *"Generate the ACVS scene manifest for B-026 Lesson 1."*

---
### Explainer 8: OMARCHY Workstation
*Arch Linux standard*

**📘 Ebook Explanation:** All Your First Python Program exercises run on OMARCHY — the reference environment ensures every learner has the same Python setup.

**📘 Connection Map:**
```
B-026 (Python Basics) ↕ OMARCHY Workstation ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Your First Python Program connects to OMARCHY Workstation: All Your First Python Program exercises run on OMARCHY — the reference environment ensures every lea..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show OMARCHY Workstation in ACSS diagram
- 10–35s: Zoom to where B-026 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-026

**🤖 Copilot Prompt:** > *"What OMARCHY packages are required to complete all B-026 exercises?"*

---
### Explainer 9: Cross-Platform Copilot
*15-platform deployment*

**📘 Ebook Explanation:** The Your First Python Program AI Copilot deploys on ChatGPT, Gemini, Claude, GitHub, Slack, and 10 more platforms.

**📘 Connection Map:**
```
B-026 (Python Basics) ↕ Cross-Platform Copilot ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Your First Python Program connects to Cross-Platform Copilot: The Your First Python Program AI Copilot deploys on ChatGPT, Gemini, Claude, GitHub, Slack, and 10 m..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Cross-Platform Copilot in ACSS diagram
- 10–35s: Zoom to where B-026 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-026

**🤖 Copilot Prompt:** > *"Adapt the B-026 copilot system prompt for LinkedIn."*

---
### Explainer 10: Earn-While-You-Learn
*revenue system*

**📘 Ebook Explanation:** `PEL-L0-B026-PythonBeginner` is proof of Python Basics mastery. Use it on LinkedIn, GitHub, and in lippytm.ai to unlock paid opportunities.

**📘 Connection Map:**
```
B-026 (Python Basics) ↕ Earn-While-You-Learn ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Your First Python Program connects to Earn-While-You-Learn: `PEL-L0-B026-PythonBeginner` is proof of Python Basics mastery. Use it on LinkedIn, GitHub, and in l..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Earn-While-You-Learn in ACSS diagram
- 10–35s: Zoom to where B-026 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-026

**🤖 Copilot Prompt:** > *"I just earned PEL-L0-B026-PythonBeginner. Generate my LinkedIn credential announcement."*

---

### Your ACSS Node Is Now Active

Completing B-026 activates your node in the Fabric graph.
**Next:** `lippytmai-launch run B-026` or start B-027 Python Lists.

---

## Appendix A: Enhanced Cheat Sheet — Your First Python Program

### 📘 Print-Optimized Reference Card

```
╔══════════════════════════════════════════════════════════════╗
║  B-026: Your First Python Program                      ║
║  Credential: PEL-L0-B026-PythonBeginner                         ║
╠══════════════════════════════════════════════════════════════╣
║  Core: python                                                   ║
║  Tool: python3                                                  ║
╠══════════════════════════════════════════════════════════════╣
║  Activate: lippytmai-launch run B-026                            ║
╚══════════════════════════════════════════════════════════════╝
```

### Quick Reference

| Concept | Pattern | Use Case |
|---|---|---|
| `python` | [usage pattern] | [when to use] |
| `print` | [usage pattern] | [when to use] |
| `variables` | [usage pattern] | [when to use] |
| `input` | [usage pattern] | [when to use] |

### 🎧 Verbal Cheat Sheet: *"Core concepts: python, print, variables. Credential: PEL-L0-B026-PythonBeginner."*

### 🎬 Thumbnail: Dark background, `B-026` bold white, `python` in green, credential badge bottom-right.

---

## Appendix B: ACSS Connection Map

Node `B-026` in the ACSS knowledge graph:

```
[Hermes] → [B-026 Events] → [Fabric] → [ADA] → [ACVS] → [OMARCHY] → [PEL:PEL-L0-B026-PythonBeginner] → [EWYL]
```

**Book chain:** B-025 Platform Deployer ← **Your First Python Program** → B-027 Python Lists

---

## Appendix C: AI Copilot System — Your First Python Program

### System Prompt
```
You are lippytmai teaching "Your First Python Program" (B-026).
Help learners master Python Basics using python3.
Credential: PEL-L0-B026-PythonBeginner. Philosophy: Earn-while-you-Learn.
Always give 3-step exercises: setup → execute → verify.
```

### 30 Ebook Prompts (5 stages × 6)

**Stage 1 — Foundation:** 1."Explain Python Basics to a beginner." 2."Most important concept in B-026?" 3."Give a 3-step setup for python3." 4."5 common beginner mistakes with Python Basics?" 5."Anatomy of a python3 pattern." 6."Mental model for Python Basics."

**Stage 2 — Practice:** 7."5 progressive Python Basics exercises." 8."Diagnose this error: [paste]." 9."Walk through this code line by line." 10."What to practice today?" 11."20-minute session for Python Basics." 12."Beginner vs. professional Python Basics comparison."

**Stage 3 — Application:** 13."Build a real Python Basics script." 14."How does Python Basics connect to production systems?" 15."Professional Python Basics workflow." 16."What does Python Basics mastery look like on a resume?" 17."Project using only B-026 skills." 18."3 Python Basics patterns in large-scale systems."

**Stage 4 — Integration:** 19."How does B-026 connect to other books?" 20."How does Python Basics feed ACSS?" 21."Hermes events for Python Basics?" 22."How does Fabric store Python Basics?" 23."ADA activation for B-026." 24."Cross-phase connections from B-026."

**Stage 5 — Mastery:** 25."Assess my Python Basics level." 26."Stretch goals for PEL-L0-B026-PythonBeginner holders?" 27."Generate my credential claim for PEL-L0-B026-PythonBeginner." 28."LinkedIn post for PEL-L0-B026-PythonBeginner." 29."Portfolio project for PEL-L0-B026-PythonBeginner." 30."90-day plan building on PEL-L0-B026-PythonBeginner."

### 15 Audiobook Prompts

1."Narrate Python Basics intro for a podcast." 2."Story explaining why Python Basics matters." 3."Audio walkthrough of key B-026 code." 4."Day in the life of a Python Basics master." 5."2-minute audio lesson on python3." 6."Python Basics explained with analogies only." 7."Top 5 mistakes with Python Basics." 8."Audio quiz: 5 questions." 9."Motivational close for B-026." 10."Credential claim narration." 11."Story: developer mastered Python Basics." 12."Audio summary for commuting." 13."3 real-world Python Basics scenarios." 14."Capstone walkthrough narration." 15."lippytmai intro monologue for B-026."

### 15 Video Prompts

1."Script 90-second B-026 intro." 2."SHOW→BUILD→VERIFY for python3." 3."Split-screen before/after Python Basics." 4."Capstone hello_world.py terminal walkthrough." 5."YouTube thumbnail description." 6."3-minute tutorial on key concept." 7."Progress bar overlay design." 8."ACVS scene manifest for Lesson 1." 9."60-second quick tip for Python Basics." 10."Error-and-fix scene." 11."Code annotation style." 12."Credential reveal scene." 13."ACSS connection diagram for Ch14." 14."Cross-platform Python Basics comparison." 15."End-screen CTA design."

### Deployment

```bash
lippytmai-launch run B-026
curl http://localhost:8000/run/B-026
```

Deploy to 15 platforms via `docs/acss-cross-platform-copilot-deployment.md`.

---

## Appendix D: Quick Quiz & Self-Assessment — Your First Python Program

### 📘 Ebook Quiz (20 Questions)

**Section 1 — Concepts (Q1–5):**
1. What is Python Basics and why does it matter? *(b — practical mastery of python)*
2. Primary tool for Python Basics? *(a — python)*
3. Which ACSS system routes Python Basics events? *(c — Hermes)*
4. Your credential for B-026? *(b — PEL-L0-B026-PythonBeginner)*
5. What does `lippytmai-launch run B-026` do? *(d — activates via ADA)*

**Section 2 — Syntax (Q6–10):**
6. Write a minimal python example: ___
7. How do you handle errors in Python Basics? ___
8. One-liner combining python with another tool: ___
9. How do you test Python Basics code? ___
10. How do you deploy Python Basics to production? ___

**Section 3 — Application (Q11–15):**
11. Describe a real-world Python Basics scenario that saves an hour.
12. Most common mistake with python?
13. How does Python Basics connect to security?
14. How does B-026 apply to a production Python project?
15. What would you build first after earning PEL-L0-B026-PythonBeginner?

**Section 4 — ACSS (Q16–20):**
16. ADA command for B-026? *(lippytmai-launch run B-026)*
17. Fabric node type for Python Basics? *(ConceptNode)*
18. How does Clone Engine use Python Basics? *(lippytmai teaches in Teach mode)*
19. 2 books that build on B-026?
20. EWYL opportunity unlocked by PEL-L0-B026-PythonBeginner?

### 🎧 Audiobook Quiz (10 Questions)

1. Three most important concepts from Your First Python Program?
2. Explain Python Basics in one sentence to a non-developer.
3. First thing to do when python fails?
4. Recite your credential.
5. One project buildable with B-026 skills only.
6. ACSS system that stores skill progress? *(Fabric)*
7. ADA activation command? *(lippytmai-launch run B-026)*
8. Next book after B-026? *(B-027 Python Lists)*
9. Say the EWYL pledge: "I learn, I build, I earn, I share."
10. What makes Python + ACSS a power combination?

### 🎬 Terminal Challenges (5)

1. **Foundation:** Run `python` — screenshot the output.
2. **Intermediate:** Combine `python` with error handling.
3. **Applied:** Write a 10-line script automating a real task.
4. **Debug:** Introduce an error, diagnose and fix it.
5. **Capstone:** Run `hello_world.py` — record a 60-second demo.

---

## Appendix E: Glossary & Error Encyclopedia — Your First Python Program

### Glossary (20 Terms)

| Term | Definition | First Seen |
|---|---|---|
| `python` | [definition in B-026 context] | [B-026] |
| `print` | [definition in B-026 context] | [B-026] |
| `variables` | [definition in B-026 context] | [B-026] |
| `input` | [definition in B-026 context] | [B-026] |
| `types` | [definition in B-026 context] | [B-026] |
| `strings` | [definition in B-026 context] | [B-026] |
| `async` | [definition in B-026 context] | [B-026] |
| `decorator` | [definition in B-026 context] | [B-026] |
| `type hint` | [definition in B-026 context] | [B-026] |
| `dataclass` | [definition in B-026 context] | [B-026] |
| `fixture` | [definition in B-026 context] | [B-026] |
| `Hermes` | [definition in B-026 context] | [B-026] |
| `Fabric` | [definition in B-026 context] | [B-026] |
| `ADA` | [definition in B-026 context] | [B-026] |
| `OMARCHY` | [definition in B-026 context] | [B-026] |
| `credential` | [definition in B-026 context] | [B-026] |
| `EWYL` | [definition in B-026 context] | [B-026] |
| `lippytmai` | [definition in B-026 context] | [B-026] |
| `PEL` | [definition in B-026 context] | [B-026] |
| `Fabric node` | [definition in B-026 context] | [B-026] |

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

## Appendix F: Instructor & Accessibility Guide — Your First Python Program

### Teaching Schedule (4-Week Curriculum)

| Week | Focus | Topics | Outcome |
|---|---|---|---|
| 1 | Foundation | Concepts + setup | Can use Python Basics tools |
| 2 | Intermediate | Core patterns | Can write working code |
| 3 | Applied | Real projects | Can solve production problems |
| 4 | Mastery | DFY + Appendices | Earns `PEL-L0-B026-PythonBeginner` |

### Common Confusion Points

1. "When do I use python vs. alternatives?" — Show a decision flowchart.
2. "Why does the same code fail in a different environment?" — Explain venv isolation.
3. "How do I know if my code is production-ready?" — Show the VERIFY step always.
4. "How does Python Basics connect to other Python skills?" — Show the ACSS learning path map.
5. "What does earning PEL-L0-B026-PythonBeginner actually mean for my career?" — Show EWYL income examples.

### Assessment Rubric

| Criterion | Beginner | Competent | Expert |
|---|---|---|---|
| Code quality | Messy, no types | Working, some types | Clean, typed, tested |
| Error handling | None | Basic try/except | Custom exceptions + logging |
| Testing | No tests | Basic assertions | pytest + fixtures + coverage |
| ACSS integration | Unaware | Uses ADA | Contributes to ACSS |

### Accessibility: Screen reader alt-text for all diagrams. No color-only encoding. Short paragraphs. Audiobook available.

---

## Appendix G: Your Learning Path — Your First Python Program

### Where You Are Now

```
  Phase 2: Python Programming (B-026–B-055)
  [░░░░░░░░░░░░░░░░░░░░] 3%

  ✅ B-025 Platform Deployer (CLL-L0-B025-PlatformDeployer)
  👉 B-026: Your First Python Program ← YOU ARE HERE
  ⬜ B-027 Python Lists (PEL-L0-B027-ListLoopLearner)
```

### Credential Chain

```
CLL-L0-B025-PlatformDeployer → PEL-L0-B026-PythonBeginner → PEL-L0-B027-ListLoopLearner
```

### Next Steps

1. Claim `PEL-L0-B026-PythonBeginner` (Appendix C, Prompt 27)
2. Build `hello_world.py` (Appendix H)
3. Start `B-027 Python Lists`

### Cross-Phase Connections

```
Phase 1: Linux Foundations → Phase 2: Python (YOU ARE HERE)
    ↓ B-026 connects to:
Phase 3: Blockchain Development (B-056+)
```

---

## Appendix H: Real Project Showcase — Your First Python Program

### Project: `hello_world.py`

**Credential gated:** Complete this project to qualify for `PEL-L0-B026-PythonBeginner`

### Complete Code

```python
#!/usr/bin/env python3
# hello_world.py — PEL-L0-B026-PythonBeginner capstone
name = input("What is your name? ")
print(f"Hello, {name}! Your Python journey starts now.")

```

### Deploy Instructions

```bash
# Run the project
python hello_world.py --help
python hello_world.py

# Test it
pytest test_hello_world.py -v  # if tests exist

# Verify
echo "Exit: $?"
```

### Extend It

1. Add type hints to all functions
2. Add pytest test coverage
3. Add CLI interface with typer
4. Containerize with Docker
5. Add structured logging

### 🎧 Walkthrough: *"Build hello_world.py step by step. When it runs successfully, you've earned PEL-L0-B026-PythonBeginner."*

### 🎬 Video: SHOW empty editor → BUILD code live → VERIFY execution → CTA: "Claim PEL-L0-B026-PythonBeginner."

---

## Further Reading

- 📄 [Back to README](../README.md)
- 📄 [Product Excellence Framework](PRODUCT-EXCELLENCE-FRAMEWORK.md)
- 📄 [AI Clone Engine Swarms](ai-clone-engine-swarms.md)
- 📄 [ACSS Cross-Platform Copilot Deployment](acss-cross-platform-copilot-deployment.md)
- 📄 [ADA Deployment Activations](ai-deployment-activations.md)
- 📄 [Previous: B-025](B-025-*.md)
- 📄 [Next: B-027](B-027-*.md)

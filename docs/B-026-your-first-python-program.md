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

## Further Reading

- 📄 [`docs/B-027-lists-loops-and-logic.md`](B-027-lists-loops-and-logic.md) — Python data structures and control flow
- 📄 [`docs/B-005-installing-things-without-breaking-things.md`](B-005-installing-things-without-breaking-things.md) — Virtual environments (venv)
- 📄 [`docs/ai-clone-engine-swarms.md`](ai-clone-engine-swarms.md) — How Python powers the ACSS
- 🏠 [`README.md`](../README.md) — Encyclopedia home

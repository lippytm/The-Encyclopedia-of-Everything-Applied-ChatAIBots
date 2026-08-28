# B-028: Functions That Do One Thing Well

### def, return, Parameters, and the Single Responsibility Principle

> *"A function that does one thing well is a unit you can trust. A function that does many things is a mystery you have to debug. Write small. Write clear. Write functions that could explain themselves to a stranger."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Define functions with `def`, parameters, and `return`
2. Understand positional vs. keyword arguments and default values
3. Write proper docstrings (Google style)
4. Apply the Single Responsibility Principle to function design
5. Build a `math-utility-library.py` with 10 well-documented functions

**Prerequisite:** B-026, B-027

**Build Artifact:** `~/developer-workspace/projects/python-foundations/math_utils.py`

**Credential:** `CCSLL-L1-B028-FunctionCrafter` — on-chain on Base

---

## Chapter 1: Defining Functions

```python
# Minimal function
def greet():
    print("Hello!")

greet()   # call it

# Function with a parameter
def greet_user(name):
    print(f"Hello, {name}!")

greet_user("Charles")
greet_user("lippytmai")

# Function with return value
def add(a, b):
    return a + b

result = add(3, 4)
print(result)   # 7

# Functions always return something (None if no return statement)
def say_hi():
    print("Hi")

value = say_hi()
print(value)    # None
```

---

## Chapter 2: Parameters and Arguments

```python
# Positional arguments — order matters
def describe_book(title, author, level):
    print(f"'{title}' by {author} — Level: {level}")

describe_book("B-026", "lippytmai", "Beginner")

# Keyword arguments — order doesn't matter
describe_book(level="Beginner", title="B-026", author="lippytmai")

# Default parameter values
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

print(greet("Charles"))              # Hello, Charles!
print(greet("Charles", "Hola"))      # Hola, Charles!

# *args — variable number of positional arguments
def sum_all(*numbers):
    return sum(numbers)

print(sum_all(1, 2, 3))          # 6
print(sum_all(1, 2, 3, 4, 5))    # 15

# **kwargs — variable number of keyword arguments
def describe(**info):
    for key, value in info.items():
        print(f"  {key}: {value}")

describe(name="Charles", role="engineer", level=5)
```

---

## Chapter 3: Type Hints — Making Functions Honest

Type hints (PEP 484) are the standard in modern Python. They document what goes in and what comes out:

```python
# Basic type hints
def add(a: int, b: int) -> int:
    return a + b

def greet(name: str) -> str:
    return f"Hello, {name}!"

def is_adult(age: int) -> bool:
    return age >= 18

# Optional and None
from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    """Return username or None if not found."""
    users = {1: "Charles", 2: "lippytmai"}
    return users.get(user_id)    # .get() returns None if key not found

# List and dict hints
from typing import List, Dict

def average(scores: List[float]) -> float:
    return sum(scores) / len(scores)

def get_info() -> Dict[str, str]:
    return {"name": "lippytmai", "role": "teacher"}
```

---

## Chapter 4: Docstrings — Self-Documenting Code

```python
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate Body Mass Index (BMI).

    Args:
        weight_kg: Weight in kilograms.
        height_m: Height in meters.

    Returns:
        BMI value as a float.

    Raises:
        ValueError: If height_m is zero or negative.

    Example:
        >>> calculate_bmi(70, 1.75)
        22.86
    """
    if height_m <= 0:
        raise ValueError(f"height_m must be positive, got {height_m}")
    return weight_kg / (height_m ** 2)


# Access the docstring
print(calculate_bmi.__doc__)
help(calculate_bmi)
```

---

## Chapter 5: Single Responsibility Principle

One function, one job:

```python
# ❌ BAD: one function does everything
def process_user_data(raw_data):
    # validates, transforms, saves, emails — all in one function
    # hard to test, hard to reuse, hard to change
    ...

# ✅ GOOD: each function does one thing
def validate_email(email: str) -> bool:
    """Return True if email looks valid."""
    return "@" in email and "." in email.split("@")[-1]

def normalize_name(name: str) -> str:
    """Return name in Title Case with stripped whitespace."""
    return name.strip().title()

def build_user_profile(raw_name: str, raw_email: str) -> dict:
    """Combine validated, normalized user fields into a profile dict."""
    return {
        "name":  normalize_name(raw_name),
        "email": raw_email.lower().strip(),
        "valid": validate_email(raw_email),
    }

# Now each function is testable independently
print(validate_email("charles@lippytm.ai"))    # True
print(normalize_name("  charles lipshay  "))   # Charles Lipshay
print(build_user_profile(" CHARLES ", "charles@lippytm.ai"))
```

---

## Chapter 6: The Build — Math Utility Library

```python
#!/usr/bin/env python3
"""
math_utils.py — B-028 Build Artifact

A math utility library demonstrating clean function design:
single responsibility, type hints, docstrings, and return values.
"""
import math
from typing import List


def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return a minus b."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of a and b."""
    return a * b


def divide(a: float, b: float) -> float:
    """Return a divided by b.

    Raises:
        ZeroDivisionError: If b is zero.
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def power(base: float, exponent: float) -> float:
    """Return base raised to exponent."""
    return base ** exponent


def square_root(n: float) -> float:
    """Return the square root of n.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError(f"Cannot take square root of negative number: {n}")
    return math.sqrt(n)


def average(numbers: List[float]) -> float:
    """Return the arithmetic mean of a list of numbers.

    Raises:
        ValueError: If numbers is empty.
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)


def is_prime(n: int) -> bool:
    """Return True if n is a prime number."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def factorial(n: int) -> int:
    """Return n! (n factorial).

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError(f"Factorial not defined for negative numbers: {n}")
    return math.factorial(n)


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9 / 5) + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5 / 9


def demo() -> None:
    """Demonstrate all math utility functions."""
    print("=== Math Utility Library Demo ===\n")
    print(f"add(3, 4)           = {add(3, 4)}")
    print(f"subtract(10, 3)     = {subtract(10, 3)}")
    print(f"multiply(4, 5)      = {multiply(4, 5)}")
    print(f"divide(10, 4)       = {divide(10, 4):.2f}")
    print(f"power(2, 10)        = {power(2, 10):.0f}")
    print(f"square_root(144)    = {square_root(144):.1f}")
    print(f"average([1..5])     = {average([1, 2, 3, 4, 5]):.1f}")
    print(f"is_prime(17)        = {is_prime(17)}")
    print(f"is_prime(18)        = {is_prime(18)}")
    print(f"factorial(6)        = {factorial(6)}")
    print(f"celsius_to_fahrenheit(100) = {celsius_to_fahrenheit(100):.1f}°F")
    print(f"fahrenheit_to_celsius(212) = {fahrenheit_to_celsius(212):.1f}°C")


if __name__ == "__main__":
    demo()
```

```bash
python3 ~/developer-workspace/projects/python-foundations/math_utils.py
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-028 Verification ==="
python3 -c "
import sys
sys.path.insert(0, '$HOME/developer-workspace/projects/python-foundations')
from math_utils import add, average, is_prime, factorial
print('add(3,4):', add(3, 4))
print('average:', average([10, 20, 30]))
print('is_prime(17):', is_prime(17))
print('factorial(5):', factorial(5))
print('All functions work!')
"
```

---


## Chapter 12: Done-For-You Lessons — Functions That Do One Thing Well

> *"Done-for-you means it's already designed, structured, and proven. Your job: execute." — lippytmai*

10 ready-to-use lesson structures for Python Functions using def.

---

### DFY Lesson 1: Introduction to Python Functions

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 01: Introduction to Python Functions          │
│  Book: B-028  Tool: def                        │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 1: Introduction to Python Functions. Master def with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `def` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 1 of B-028: Introduction to Python Functions. Give me 3 progressive exercises."

---
### DFY Lesson 2: Core def Patterns

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 02: Core def Patterns                         │
│  Book: B-028  Tool: def                        │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 2: Core def Patterns. Master def with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `def` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 2 of B-028: Core def Patterns. Give me 3 progressive exercises."

---
### DFY Lesson 3: Three Formats: Ebook, Audiobook, Video

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 03: Three Formats: Ebook, Audiobook, Video    │
│  Book: B-028  Tool: def                        │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 3: Three Formats: Ebook, Audiobook, Video. Master def with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `def` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 3 of B-028: Three Formats: Ebook, Audiobook, Video. Give me 3 progressive exercises."

---
### DFY Lesson 4: Common Mistakes in Python Functions

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 04: Common Mistakes in Python Functions       │
│  Book: B-028  Tool: def                        │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 4: Common Mistakes in Python Functions. Master def with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `def` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 4 of B-028: Common Mistakes in Python Functions. Give me 3 progressive exercises."

---
### DFY Lesson 5: Building a Python Functions Workflow

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 05: Building a Python Functions Workflow      │
│  Book: B-028  Tool: def                        │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 5: Building a Python Functions Workflow. Master def with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `def` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 5 of B-028: Building a Python Functions Workflow. Give me 3 progressive exercises."

---
### DFY Lesson 6: Automating with def

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 06: Automating with def                       │
│  Book: B-028  Tool: def                        │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 6: Automating with def. Master def with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `def` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 6 of B-028: Automating with def. Give me 3 progressive exercises."

---
### DFY Lesson 7: Testing Your Python Functions Code

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 07: Testing Your Python Functions Code        │
│  Book: B-028  Tool: def                        │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 7: Testing Your Python Functions Code. Master def with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `def` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 7 of B-028: Testing Your Python Functions Code. Give me 3 progressive exercises."

---
### DFY Lesson 8: Production Python Functions Patterns

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 08: Production Python Functions Patterns      │
│  Book: B-028  Tool: def                        │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 8: Production Python Functions Patterns. Master def with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `def` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 8 of B-028: Production Python Functions Patterns. Give me 3 progressive exercises."

---
### DFY Lesson 9: Debugging Python Functions Problems

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 09: Debugging Python Functions Problems       │
│  Book: B-028  Tool: def                        │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 9: Debugging Python Functions Problems. Master def with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `def` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 9 of B-028: Debugging Python Functions Problems. Give me 3 progressive exercises."

---
### DFY Lesson 10: Earning Your PEL-L0-B028-FunctionBuilder Credential

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 10: Earning Your PEL-L0-B028-FunctionBuilder  │
│  Book: B-028  Tool: def                        │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 10: Earning Your PEL-L0-B028-FunctionBuilder Credential. Master def with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `def` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 10 of B-028: Earning Your PEL-L0-B028-FunctionBuilder Credential. Give me 3 progressive exercises."

---

### Claim Your Credential

Complete all 10 lessons → open Appendix C → run: *"Generate my credential claim for `PEL-L0-B028-FunctionBuilder`."*

---

## Chapter 13: How It Works — Use Cases & Applications

> *"Knowing what to do is different from knowing why it matters." — lippytmai*

### The Mechanism

Python Functions in Python works because the language was designed to be readable, composable, and deployable. def is the tool that makes Python Functions practical.

### 5 Real-World Use Cases

| Domain | Application | Your Credential Unlocks |
|---|---|---|
| Backend Dev | Build APIs and services with def | PEL-L0-B028-FunctionBuilder → production deployments |
| Data Engineering | Process and transform data pipelines | PEL-L0-B028-FunctionBuilder → ETL roles |
| DevOps/Automation | Automate repetitive tasks | PEL-L0-B028-FunctionBuilder → CI/CD integration |
| AI/ML | Preprocess data and build models | PEL-L0-B028-FunctionBuilder → AI projects |
| Freelance | Deliver Python solutions to clients | PEL-L0-B028-FunctionBuilder → paid work |

### 📘 Mechanism Diagram

```
INPUT → [Python Functions Layer] → OUTPUT
         ↓
[ACSS Integration] → Hermes Event → Fabric Node
         ↓
[ADA Activation] → lippytmai-launch run B-028
```

### 🎧 Audiobook Narration:

> *"When you master Python Functions, you're not just learning syntax — you're learning how production Python systems work. Every ACSS component uses these patterns. This is infrastructure knowledge."*

### 🎬 Video: 5-Domain Application Tour

**Scene 1 — Backend:** API or service using Python Functions
**Scene 2 — Data:** Data pipeline using Python Functions
**Scene 3 — DevOps:** Automation script using Python Functions
**Scene 4 — AI/ML:** Model integration using Python Functions
**Scene 5 — Freelance:** Client deliverable using Python Functions

---

## Chapter 14: ACSS Explainer Series — Functions That Do One Thing Well

> *"You're not just learning Python Functions. You're building a node in an intelligence network." — lippytmai*

10 explainer lessons connecting Functions That Do One Thing Well to the full ACSS architecture.

---

### Explainer 1: ACSS Overview
*intelligence network*

**📘 Ebook Explanation:** Functions That Do One Thing Well teaches the Python Functions layer that feeds the ACSS. Every acss agent is built from composable functions — the single-responsibility principle from this book is acss design law.

**📘 Connection Map:**
```
B-028 (Python Functions) ↕ ACSS Overview ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Functions That Do One Thing Well connects to ACSS Overview: Functions That Do One Thing Well teaches the Python Functions layer that feeds the ACSS. Every acss ..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ACSS Overview in ACSS diagram
- 10–35s: Zoom to where B-028 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-028

**🤖 Copilot Prompt:** > *"Explain how Python Functions fits the ACSS. What role does B-028 play?"*

---
### Explainer 2: Hermes Event Routing
*cross-system message bus*

**📘 Ebook Explanation:** Hermes routes Python Functions practice events. Completing an exercise emits a `skill.practice` event.

**📘 Connection Map:**
```
B-028 (Python Functions) ↕ Hermes Event Routing ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Functions That Do One Thing Well connects to Hermes Event Routing: Hermes routes Python Functions practice events. Completing an exercise emits a `skill.practice` even..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Hermes Event Routing in ACSS diagram
- 10–35s: Zoom to where B-028 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-028

**🤖 Copilot Prompt:** > *"Show the Hermes event schema for a B-028 skill-complete event."*

---
### Explainer 3: Fabric Knowledge Graph
*pattern synthesis*

**📘 Ebook Explanation:** Fabric stores every Python Functions concept as a knowledge node connected to related books.

**📘 Connection Map:**
```
B-028 (Python Functions) ↕ Fabric Knowledge Graph ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Functions That Do One Thing Well connects to Fabric Knowledge Graph: Fabric stores every Python Functions concept as a knowledge node connected to related books...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Fabric Knowledge Graph in ACSS diagram
- 10–35s: Zoom to where B-028 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-028

**🤖 Copilot Prompt:** > *"Generate the Fabric node definition for the core concept of B-028."*

---
### Explainer 4: Clone Engine Identity
*AI persona system*

**📘 Ebook Explanation:** lippytmai teaches Functions That Do One Thing Well in Teach mode. The Clone Engine maintains consistent voice across all 300 books.

**📘 Connection Map:**
```
B-028 (Python Functions) ↕ Clone Engine Identity ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Functions That Do One Thing Well connects to Clone Engine Identity: lippytmai teaches Functions That Do One Thing Well in Teach mode. The Clone Engine maintains consist..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Clone Engine Identity in ACSS diagram
- 10–35s: Zoom to where B-028 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-028

**🤖 Copilot Prompt:** > *"As lippytmai, explain Python Functions to a complete beginner using the B-028 voice."*

---
### Explainer 5: CLL/CCSLL/CBSLL
*Complete Language Libraries*

**📘 Ebook Explanation:** `PEL-L0-B028-FunctionBuilder` is registered in the Python Earn-while-you-Learn library (PEL). PEL tracks all Python credentials B-026–B-100+.

**📘 Connection Map:**
```
B-028 (Python Functions) ↕ CLL/CCSLL/CBSLL ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Functions That Do One Thing Well connects to CLL/CCSLL/CBSLL: `PEL-L0-B028-FunctionBuilder` is registered in the Python Earn-while-you-Learn library (PEL). PEL tr..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show CLL/CCSLL/CBSLL in ACSS diagram
- 10–35s: Zoom to where B-028 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-028

**🤖 Copilot Prompt:** > *"Show where PEL-L0-B028-FunctionBuilder fits in the PEL credential hierarchy."*

---
### Explainer 6: ADA Activation
*deployment system*

**📘 Ebook Explanation:** `lippytmai-launch run B-028` activates Functions That Do One Thing Well through the ADA FastAPI backend.

**📘 Connection Map:**
```
B-028 (Python Functions) ↕ ADA Activation ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Functions That Do One Thing Well connects to ADA Activation: `lippytmai-launch run B-028` activates Functions That Do One Thing Well through the ADA FastAPI back..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ADA Activation in ACSS diagram
- 10–35s: Zoom to where B-028 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-028

**🤖 Copilot Prompt:** > *"Write the ADA activation manifest for B-028."*

---
### Explainer 7: ACVS Video Pipeline
*video creator*

**📘 Ebook Explanation:** Every Functions That Do One Thing Well video uses ACVS SHOW→BUILD→VERIFY structure.

**📘 Connection Map:**
```
B-028 (Python Functions) ↕ ACVS Video Pipeline ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Functions That Do One Thing Well connects to ACVS Video Pipeline: Every Functions That Do One Thing Well video uses ACVS SHOW→BUILD→VERIFY structure...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ACVS Video Pipeline in ACSS diagram
- 10–35s: Zoom to where B-028 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-028

**🤖 Copilot Prompt:** > *"Generate the ACVS scene manifest for B-028 Lesson 1."*

---
### Explainer 8: OMARCHY Workstation
*Arch Linux standard*

**📘 Ebook Explanation:** All Functions That Do One Thing Well exercises run on OMARCHY — the reference environment ensures every learner has the same Python setup.

**📘 Connection Map:**
```
B-028 (Python Functions) ↕ OMARCHY Workstation ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Functions That Do One Thing Well connects to OMARCHY Workstation: All Functions That Do One Thing Well exercises run on OMARCHY — the reference environment ensures ev..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show OMARCHY Workstation in ACSS diagram
- 10–35s: Zoom to where B-028 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-028

**🤖 Copilot Prompt:** > *"What OMARCHY packages are required to complete all B-028 exercises?"*

---
### Explainer 9: Cross-Platform Copilot
*15-platform deployment*

**📘 Ebook Explanation:** The Functions That Do One Thing Well AI Copilot deploys on ChatGPT, Gemini, Claude, GitHub, Slack, and 10 more platforms.

**📘 Connection Map:**
```
B-028 (Python Functions) ↕ Cross-Platform Copilot ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Functions That Do One Thing Well connects to Cross-Platform Copilot: The Functions That Do One Thing Well AI Copilot deploys on ChatGPT, Gemini, Claude, GitHub, Slack, a..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Cross-Platform Copilot in ACSS diagram
- 10–35s: Zoom to where B-028 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-028

**🤖 Copilot Prompt:** > *"Adapt the B-028 copilot system prompt for LinkedIn."*

---
### Explainer 10: Earn-While-You-Learn
*revenue system*

**📘 Ebook Explanation:** `PEL-L0-B028-FunctionBuilder` is proof of Python Functions mastery. Use it on LinkedIn, GitHub, and in lippytm.ai to unlock paid opportunities.

**📘 Connection Map:**
```
B-028 (Python Functions) ↕ Earn-While-You-Learn ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Functions That Do One Thing Well connects to Earn-While-You-Learn: `PEL-L0-B028-FunctionBuilder` is proof of Python Functions mastery. Use it on LinkedIn, GitHub, and ..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Earn-While-You-Learn in ACSS diagram
- 10–35s: Zoom to where B-028 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-028

**🤖 Copilot Prompt:** > *"I just earned PEL-L0-B028-FunctionBuilder. Generate my LinkedIn credential announcement."*

---

### Your ACSS Node Is Now Active

Completing B-028 activates your node in the Fabric graph.
**Next:** `lippytmai-launch run B-028` or start B-029 Dict Wizard.

---

## Appendix A: Enhanced Cheat Sheet — Functions That Do One Thing Well

### 📘 Print-Optimized Reference Card

```
╔══════════════════════════════════════════════════════════════╗
║  B-028: Functions That Do One Thing Well               ║
║  Credential: PEL-L0-B028-FunctionBuilder                        ║
╠══════════════════════════════════════════════════════════════╣
║  Core: functions                                                ║
║  Tool: def + return                                             ║
╠══════════════════════════════════════════════════════════════╣
║  Activate: lippytmai-launch run B-028                            ║
╚══════════════════════════════════════════════════════════════╝
```

### Quick Reference

| Concept | Pattern | Use Case |
|---|---|---|
| `functions` | [usage pattern] | [when to use] |
| `def` | [usage pattern] | [when to use] |
| `return` | [usage pattern] | [when to use] |
| `parameters` | [usage pattern] | [when to use] |

### 🎧 Verbal Cheat Sheet: *"Core concepts: functions, def, return. Credential: PEL-L0-B028-FunctionBuilder."*

### 🎬 Thumbnail: Dark background, `B-028` bold white, `functions` in green, credential badge bottom-right.

---

## Appendix B: ACSS Connection Map

Node `B-028` in the ACSS knowledge graph:

```
[Hermes] → [B-028 Events] → [Fabric] → [ADA] → [ACVS] → [OMARCHY] → [PEL:PEL-L0-B028-FunctionBuilder] → [EWYL]
```

**Book chain:** B-027 List Loop Learner ← **Functions That Do One Thing Well** → B-029 Dict Wizard

---

## Appendix C: AI Copilot System — Functions That Do One Thing Well

### System Prompt
```
You are lippytmai teaching "Functions That Do One Thing Well" (B-028).
Help learners master Python Functions using def.
Credential: PEL-L0-B028-FunctionBuilder. Philosophy: Earn-while-you-Learn.
Always give 3-step exercises: setup → execute → verify.
```

### 30 Ebook Prompts (5 stages × 6)

**Stage 1 — Foundation:** 1."Explain Python Functions to a beginner." 2."Most important concept in B-028?" 3."Give a 3-step setup for def." 4."5 common beginner mistakes with Python Functions?" 5."Anatomy of a def pattern." 6."Mental model for Python Functions."

**Stage 2 — Practice:** 7."5 progressive Python Functions exercises." 8."Diagnose this error: [paste]." 9."Walk through this code line by line." 10."What to practice today?" 11."20-minute session for Python Functions." 12."Beginner vs. professional Python Functions comparison."

**Stage 3 — Application:** 13."Build a real Python Functions script." 14."How does Python Functions connect to production systems?" 15."Professional Python Functions workflow." 16."What does Python Functions mastery look like on a resume?" 17."Project using only B-028 skills." 18."3 Python Functions patterns in large-scale systems."

**Stage 4 — Integration:** 19."How does B-028 connect to other books?" 20."How does Python Functions feed ACSS?" 21."Hermes events for Python Functions?" 22."How does Fabric store Python Functions?" 23."ADA activation for B-028." 24."Cross-phase connections from B-028."

**Stage 5 — Mastery:** 25."Assess my Python Functions level." 26."Stretch goals for PEL-L0-B028-FunctionBuilder holders?" 27."Generate my credential claim for PEL-L0-B028-FunctionBuilder." 28."LinkedIn post for PEL-L0-B028-FunctionBuilder." 29."Portfolio project for PEL-L0-B028-FunctionBuilder." 30."90-day plan building on PEL-L0-B028-FunctionBuilder."

### 15 Audiobook Prompts

1."Narrate Python Functions intro for a podcast." 2."Story explaining why Python Functions matters." 3."Audio walkthrough of key B-028 code." 4."Day in the life of a Python Functions master." 5."2-minute audio lesson on def." 6."Python Functions explained with analogies only." 7."Top 5 mistakes with Python Functions." 8."Audio quiz: 5 questions." 9."Motivational close for B-028." 10."Credential claim narration." 11."Story: developer mastered Python Functions." 12."Audio summary for commuting." 13."3 real-world Python Functions scenarios." 14."Capstone walkthrough narration." 15."lippytmai intro monologue for B-028."

### 15 Video Prompts

1."Script 90-second B-028 intro." 2."SHOW→BUILD→VERIFY for def." 3."Split-screen before/after Python Functions." 4."Capstone calculator.py terminal walkthrough." 5."YouTube thumbnail description." 6."3-minute tutorial on key concept." 7."Progress bar overlay design." 8."ACVS scene manifest for Lesson 1." 9."60-second quick tip for Python Functions." 10."Error-and-fix scene." 11."Code annotation style." 12."Credential reveal scene." 13."ACSS connection diagram for Ch14." 14."Cross-platform Python Functions comparison." 15."End-screen CTA design."

### Deployment

```bash
lippytmai-launch run B-028
curl http://localhost:8000/run/B-028
```

Deploy to 15 platforms via `docs/acss-cross-platform-copilot-deployment.md`.

---

## Appendix D: Quick Quiz & Self-Assessment — Functions That Do One Thing Well

### 📘 Ebook Quiz (20 Questions)

**Section 1 — Concepts (Q1–5):**
1. What is Python Functions and why does it matter? *(b — practical mastery of functions)*
2. Primary tool for Python Functions? *(a — functions)*
3. Which ACSS system routes Python Functions events? *(c — Hermes)*
4. Your credential for B-028? *(b — PEL-L0-B028-FunctionBuilder)*
5. What does `lippytmai-launch run B-028` do? *(d — activates via ADA)*

**Section 2 — Syntax (Q6–10):**
6. Write a minimal functions example: ___
7. How do you handle errors in Python Functions? ___
8. One-liner combining functions with another tool: ___
9. How do you test Python Functions code? ___
10. How do you deploy Python Functions to production? ___

**Section 3 — Application (Q11–15):**
11. Describe a real-world Python Functions scenario that saves an hour.
12. Most common mistake with functions?
13. How does Python Functions connect to security?
14. How does B-028 apply to a production Python project?
15. What would you build first after earning PEL-L0-B028-FunctionBuilder?

**Section 4 — ACSS (Q16–20):**
16. ADA command for B-028? *(lippytmai-launch run B-028)*
17. Fabric node type for Python Functions? *(ConceptNode)*
18. How does Clone Engine use Python Functions? *(lippytmai teaches in Teach mode)*
19. 2 books that build on B-028?
20. EWYL opportunity unlocked by PEL-L0-B028-FunctionBuilder?

### 🎧 Audiobook Quiz (10 Questions)

1. Three most important concepts from Functions That Do One Thing Well?
2. Explain Python Functions in one sentence to a non-developer.
3. First thing to do when functions fails?
4. Recite your credential.
5. One project buildable with B-028 skills only.
6. ACSS system that stores skill progress? *(Fabric)*
7. ADA activation command? *(lippytmai-launch run B-028)*
8. Next book after B-028? *(B-029 Dict Wizard)*
9. Say the EWYL pledge: "I learn, I build, I earn, I share."
10. What makes Python + ACSS a power combination?

### 🎬 Terminal Challenges (5)

1. **Foundation:** Run `functions` — screenshot the output.
2. **Intermediate:** Combine `functions` with error handling.
3. **Applied:** Write a 10-line script automating a real task.
4. **Debug:** Introduce an error, diagnose and fix it.
5. **Capstone:** Run `calculator.py` — record a 60-second demo.

---

## Appendix E: Glossary & Error Encyclopedia — Functions That Do One Thing Well

### Glossary (20 Terms)

| Term | Definition | First Seen |
|---|---|---|
| `functions` | [definition in B-028 context] | [B-028] |
| `def` | [definition in B-028 context] | [B-028] |
| `return` | [definition in B-028 context] | [B-028] |
| `parameters` | [definition in B-028 context] | [B-028] |
| `default args` | [definition in B-028 context] | [B-028] |
| `*args` | [definition in B-028 context] | [B-028] |
| `async` | [definition in B-028 context] | [B-028] |
| `decorator` | [definition in B-028 context] | [B-028] |
| `type hint` | [definition in B-028 context] | [B-028] |
| `dataclass` | [definition in B-028 context] | [B-028] |
| `fixture` | [definition in B-028 context] | [B-028] |
| `Hermes` | [definition in B-028 context] | [B-028] |
| `Fabric` | [definition in B-028 context] | [B-028] |
| `ADA` | [definition in B-028 context] | [B-028] |
| `OMARCHY` | [definition in B-028 context] | [B-028] |
| `credential` | [definition in B-028 context] | [B-028] |
| `EWYL` | [definition in B-028 context] | [B-028] |
| `lippytmai` | [definition in B-028 context] | [B-028] |
| `PEL` | [definition in B-028 context] | [B-028] |
| `Fabric node` | [definition in B-028 context] | [B-028] |

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

## Appendix F: Instructor & Accessibility Guide — Functions That Do One Thing Well

### Teaching Schedule (4-Week Curriculum)

| Week | Focus | Topics | Outcome |
|---|---|---|---|
| 1 | Foundation | Concepts + setup | Can use Python Functions tools |
| 2 | Intermediate | Core patterns | Can write working code |
| 3 | Applied | Real projects | Can solve production problems |
| 4 | Mastery | DFY + Appendices | Earns `PEL-L0-B028-FunctionBuilder` |

### Common Confusion Points

1. "When do I use functions vs. alternatives?" — Show a decision flowchart.
2. "Why does the same code fail in a different environment?" — Explain venv isolation.
3. "How do I know if my code is production-ready?" — Show the VERIFY step always.
4. "How does Python Functions connect to other Python skills?" — Show the ACSS learning path map.
5. "What does earning PEL-L0-B028-FunctionBuilder actually mean for my career?" — Show EWYL income examples.

### Assessment Rubric

| Criterion | Beginner | Competent | Expert |
|---|---|---|---|
| Code quality | Messy, no types | Working, some types | Clean, typed, tested |
| Error handling | None | Basic try/except | Custom exceptions + logging |
| Testing | No tests | Basic assertions | pytest + fixtures + coverage |
| ACSS integration | Unaware | Uses ADA | Contributes to ACSS |

### Accessibility: Screen reader alt-text for all diagrams. No color-only encoding. Short paragraphs. Audiobook available.

---

## Appendix G: Your Learning Path — Functions That Do One Thing Well

### Where You Are Now

```
  Phase 2: Python Programming (B-026–B-055)
  [██░░░░░░░░░░░░░░░░░░] 10%

  ✅ B-027 List Loop Learner (PEL-L0-B027-ListLoopLearner)
  👉 B-028: Functions That Do One Thing Well ← YOU ARE HERE
  ⬜ B-029 Dict Wizard (PEL-L0-B029-DictWizard)
```

### Credential Chain

```
PEL-L0-B027-ListLoopLearner → PEL-L0-B028-FunctionBuilder → PEL-L0-B029-DictWizard
```

### Next Steps

1. Claim `PEL-L0-B028-FunctionBuilder` (Appendix C, Prompt 27)
2. Build `calculator.py` (Appendix H)
3. Start `B-029 Dict Wizard`

### Cross-Phase Connections

```
Phase 1: Linux Foundations → Phase 2: Python (YOU ARE HERE)
    ↓ B-028 connects to:
Phase 3: Blockchain Development (B-056+)
```

---

## Appendix H: Real Project Showcase — Functions That Do One Thing Well

### Project: `calculator.py`

**Credential gated:** Complete this project to qualify for `PEL-L0-B028-FunctionBuilder`

### Complete Code

```python
#!/usr/bin/env python3
from typing import Union
Number = Union[int, float]

def add(a: Number, b: Number) -> Number:
    return a + b

def subtract(a: Number, b: Number) -> Number:
    return a - b

def multiply(a: Number, b: Number) -> Number:
    return a * b

def divide(a: Number, b: Number) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

```

### Deploy Instructions

```bash
# Run the project
python calculator.py --help
python calculator.py

# Test it
pytest test_calculator.py -v  # if tests exist

# Verify
echo "Exit: $?"
```

### Extend It

1. Add type hints to all functions
2. Add pytest test coverage
3. Add CLI interface with typer
4. Containerize with Docker
5. Add structured logging

### 🎧 Walkthrough: *"Build calculator.py step by step. When it runs successfully, you've earned PEL-L0-B028-FunctionBuilder."*

### 🎬 Video: SHOW empty editor → BUILD code live → VERIFY execution → CTA: "Claim PEL-L0-B028-FunctionBuilder."

---

## Further Reading

- 📄 [Back to README](../README.md)
- 📄 [Product Excellence Framework](PRODUCT-EXCELLENCE-FRAMEWORK.md)
- 📄 [AI Clone Engine Swarms](ai-clone-engine-swarms.md)
- 📄 [ACSS Cross-Platform Copilot Deployment](acss-cross-platform-copilot-deployment.md)
- 📄 [ADA Deployment Activations](ai-deployment-activations.md)
- 📄 [Previous: B-027](B-027-*.md)
- 📄 [Next: B-029](B-029-*.md)

# B-034: Testing Your Code (So Others Trust It)

### pytest, assert, Test Functions, and Why Tests Are the Best Documentation

> *"Untested code is a liability. Tested code is an asset. A test suite is a living specification of what your code is supposed to do. When you write a test, you write down your intentions permanently. When the test passes, your intentions are verified. When it fails, you know exactly what broke."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Install and run `pytest` and understand its autodiscovery rules
2. Write test functions and understand `assert` in the context of testing
3. Use fixtures to share setup code between tests
4. Write tests for the `math_utils.py` library from B-028
5. Interpret test output and fix failing tests

**Prerequisite:** B-026 through B-033

**Build Artifact:** `~/developer-workspace/projects/python-foundations/tests/test_math_utils.py`

**Credential:** `CCSLL-L1-B034-TestEngineer` — on-chain on Base

---

## Chapter 1: Why Tests?

```python
# Without a test, you have to manually verify every change:
# "Does add(3, 4) still return 7 after my refactor?"

# With a test, the computer verifies it for you — every time:
def test_add_returns_correct_sum():
    assert add(3, 4) == 7
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
```

Tests are:
- **Documentation** — they describe what functions are supposed to do
- **Regression guards** — they catch when future changes break existing behavior
- **Design pressure** — functions that are hard to test are usually poorly designed

---

## Chapter 2: Installing and Running pytest

```bash
pip install pytest

# Run all tests in current directory (auto-discovers test_*.py files)
pytest

# Run with verbose output
pytest -v

# Run a specific file
pytest tests/test_math_utils.py

# Run a specific test function
pytest tests/test_math_utils.py::test_add

# Run tests matching a keyword
pytest -k "add or subtract"

# Show print() output during tests
pytest -s
```

**pytest autodiscovery rules:**
- Files named `test_*.py` or `*_test.py`
- Functions named `test_*`
- Classes named `Test*` (no `__init__`)

---

## Chapter 3: assert — The Heart of a Test

```python
# assert checks that something is True
# If False, it raises AssertionError — pytest catches this and marks the test FAIL

assert 1 + 1 == 2          # passes
assert "hello"              # passes (truthy)
assert []                   # FAILS — empty list is falsy

# Good assert messages
x = 42
assert x > 0, f"Expected positive, got {x}"

# In pytest tests: assert reads naturally
def test_add():
    assert add(3, 4) == 7          # equality
    assert add(0, 0) == 0
    assert add(-5, 5) == 0

def test_is_positive():
    result = add(1, 1)
    assert result > 0              # comparison
    assert isinstance(result, (int, float))  # type check
    assert result in [2, 2.0]      # membership
```

---

## Chapter 4: Testing Exceptions

```python
import pytest

def test_divide_raises_on_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_calculate_average_raises_on_empty():
    with pytest.raises(ValueError, match="empty"):
        calculate_average([])

def test_square_root_raises_on_negative():
    with pytest.raises(ValueError):
        square_root(-1)
```

---

## Chapter 5: Fixtures — Shared Setup Code

```python
import pytest

# A fixture is a function that provides test data or setup
@pytest.fixture
def sample_scores():
    """Return a known list of scores for testing."""
    return [10.0, 20.0, 30.0, 40.0, 50.0]

@pytest.fixture
def empty_list():
    return []

# Tests that need the fixture just declare it as a parameter
def test_average_of_sample(sample_scores):
    result = average(sample_scores)
    assert result == 30.0

def test_average_of_single():
    assert average([42.0]) == 42.0

def test_average_empty_raises(empty_list):
    with pytest.raises(ValueError):
        average(empty_list)
```

---

## Chapter 6: The Build — Full Test Suite for math_utils

```python
# tests/test_math_utils.py — B-034 Build Artifact
# Full pytest test suite for math_utils.py (B-028)
import math
import sys
from pathlib import Path

import pytest

# Add parent directory to path so we can import math_utils
sys.path.insert(0, str(Path(__file__).parent.parent))
from math_utils import (
    add, subtract, multiply, divide, power,
    square_root, average, is_prime, factorial,
    celsius_to_fahrenheit, fahrenheit_to_celsius,
)


# === Fixtures ===

@pytest.fixture
def small_numbers():
    return [1.0, 2.0, 3.0, 4.0, 5.0]

@pytest.fixture
def single_number():
    return [42.0]


# === Basic Arithmetic ===

class TestAdd:
    def test_positive_numbers(self):
        assert add(3, 4) == 7

    def test_negative_numbers(self):
        assert add(-3, -4) == -7

    def test_mixed_sign(self):
        assert add(-1, 1) == 0

    def test_float(self):
        assert add(0.1, 0.2) == pytest.approx(0.3)

    def test_zero(self):
        assert add(0, 0) == 0


class TestSubtract:
    def test_basic(self):
        assert subtract(10, 3) == 7

    def test_negative_result(self):
        assert subtract(3, 10) == -7


class TestMultiply:
    def test_basic(self):
        assert multiply(4, 5) == 20

    def test_by_zero(self):
        assert multiply(100, 0) == 0

    def test_negative(self):
        assert multiply(-3, 4) == -12


class TestDivide:
    def test_basic(self):
        assert divide(10, 2) == 5.0

    def test_float_result(self):
        assert divide(10, 4) == pytest.approx(2.5)

    def test_by_zero_raises(self):
        with pytest.raises(ZeroDivisionError):
            divide(10, 0)


# === Advanced Math ===

class TestPower:
    def test_integer_exponent(self):
        assert power(2, 10) == 1024

    def test_zero_exponent(self):
        assert power(5, 0) == 1

    def test_negative_exponent(self):
        assert power(2, -1) == pytest.approx(0.5)


class TestSquareRoot:
    def test_perfect_square(self):
        assert square_root(144) == 12.0

    def test_non_perfect(self):
        assert square_root(2) == pytest.approx(math.sqrt(2))

    def test_zero(self):
        assert square_root(0) == 0.0

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            square_root(-1)


class TestAverage:
    def test_simple_list(self, small_numbers):
        assert average(small_numbers) == 3.0

    def test_single_element(self, single_number):
        assert average(single_number) == 42.0

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="empty"):
            average([])

    def test_float_result(self):
        assert average([1, 2]) == pytest.approx(1.5)


class TestIsPrime:
    @pytest.mark.parametrize("n,expected", [
        (2, True), (3, True), (5, True), (7, True), (11, True),
        (1, False), (0, False), (-1, False),
        (4, False), (9, False), (15, False),
    ])
    def test_known_primes_and_composites(self, n, expected):
        assert is_prime(n) == expected


class TestFactorial:
    def test_base_cases(self):
        assert factorial(0) == 1
        assert factorial(1) == 1

    def test_small_numbers(self):
        assert factorial(5) == 120
        assert factorial(6) == 720

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            factorial(-1)


# === Temperature Conversion ===

class TestTemperatureConversion:
    def test_boiling_point(self):
        assert celsius_to_fahrenheit(100) == pytest.approx(212)

    def test_freezing_point(self):
        assert celsius_to_fahrenheit(0) == pytest.approx(32)

    def test_body_temperature(self):
        assert celsius_to_fahrenheit(37) == pytest.approx(98.6, rel=1e-2)

    def test_roundtrip(self):
        original = 25.0
        converted = celsius_to_fahrenheit(original)
        back = fahrenheit_to_celsius(converted)
        assert back == pytest.approx(original)
```

```bash
mkdir -p ~/developer-workspace/projects/python-foundations/tests
# Save the file above to tests/test_math_utils.py

cd ~/developer-workspace/projects/python-foundations
pytest tests/test_math_utils.py -v
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-034 Verification ==="
cd ~/developer-workspace/projects/python-foundations
pytest tests/test_math_utils.py -v 2>/dev/null | tail -20

echo ""
echo "Test count:"
pytest tests/test_math_utils.py --collect-only -q 2>/dev/null | tail -3
```

---


## Chapter 12: Done-For-You Lessons — Testing Your Code

> *"Done-for-you means it's already designed, structured, and proven. Your job: execute." — lippytmai*

10 ready-to-use lesson structures for Python Testing using pytest.

---

### DFY Lesson 1: Introduction to Python Testing

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 01: Introduction to Python Testing            │
│  Book: B-034  Tool: pytest                     │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 1: Introduction to Python Testing. Master pytest with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `pytest` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 1 of B-034: Introduction to Python Testing. Give me 3 progressive exercises."

---
### DFY Lesson 2: Core pytest Patterns

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 02: Core pytest Patterns                      │
│  Book: B-034  Tool: pytest                     │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 2: Core pytest Patterns. Master pytest with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `pytest` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 2 of B-034: Core pytest Patterns. Give me 3 progressive exercises."

---
### DFY Lesson 3: Three Formats: Ebook, Audiobook, Video

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 03: Three Formats: Ebook, Audiobook, Video    │
│  Book: B-034  Tool: pytest                     │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 3: Three Formats: Ebook, Audiobook, Video. Master pytest with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `pytest` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 3 of B-034: Three Formats: Ebook, Audiobook, Video. Give me 3 progressive exercises."

---
### DFY Lesson 4: Common Mistakes in Python Testing

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 04: Common Mistakes in Python Testing         │
│  Book: B-034  Tool: pytest                     │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 4: Common Mistakes in Python Testing. Master pytest with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `pytest` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 4 of B-034: Common Mistakes in Python Testing. Give me 3 progressive exercises."

---
### DFY Lesson 5: Building a Python Testing Workflow

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 05: Building a Python Testing Workflow        │
│  Book: B-034  Tool: pytest                     │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 5: Building a Python Testing Workflow. Master pytest with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `pytest` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 5 of B-034: Building a Python Testing Workflow. Give me 3 progressive exercises."

---
### DFY Lesson 6: Automating with pytest

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 06: Automating with pytest                    │
│  Book: B-034  Tool: pytest                     │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 6: Automating with pytest. Master pytest with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `pytest` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 6 of B-034: Automating with pytest. Give me 3 progressive exercises."

---
### DFY Lesson 7: Testing Your Python Testing Code

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 07: Testing Your Python Testing Code          │
│  Book: B-034  Tool: pytest                     │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 7: Testing Your Python Testing Code. Master pytest with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `pytest` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 7 of B-034: Testing Your Python Testing Code. Give me 3 progressive exercises."

---
### DFY Lesson 8: Production Python Testing Patterns

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 08: Production Python Testing Patterns        │
│  Book: B-034  Tool: pytest                     │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 8: Production Python Testing Patterns. Master pytest with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `pytest` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 8 of B-034: Production Python Testing Patterns. Give me 3 progressive exercises."

---
### DFY Lesson 9: Debugging Python Testing Problems

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 09: Debugging Python Testing Problems         │
│  Book: B-034  Tool: pytest                     │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 9: Debugging Python Testing Problems. Master pytest with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `pytest` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 9 of B-034: Debugging Python Testing Problems. Give me 3 progressive exercises."

---
### DFY Lesson 10: Earning Your PEL-L0-B034-TestWriter Credential

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 10: Earning Your PEL-L0-B034-TestWriter Cred  │
│  Book: B-034  Tool: pytest                     │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 10: Earning Your PEL-L0-B034-TestWriter Credential. Master pytest with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `pytest` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 10 of B-034: Earning Your PEL-L0-B034-TestWriter Credential. Give me 3 progressive exercises."

---

### Claim Your Credential

Complete all 10 lessons → open Appendix C → run: *"Generate my credential claim for `PEL-L0-B034-TestWriter`."*

---

## Chapter 13: How It Works — Use Cases & Applications

> *"Knowing what to do is different from knowing why it matters." — lippytmai*

### The Mechanism

Python Testing in Python works because the language was designed to be readable, composable, and deployable. pytest is the tool that makes Python Testing practical.

### 5 Real-World Use Cases

| Domain | Application | Your Credential Unlocks |
|---|---|---|
| Backend Dev | Build APIs and services with pytest | PEL-L0-B034-TestWriter → production deployments |
| Data Engineering | Process and transform data pipelines | PEL-L0-B034-TestWriter → ETL roles |
| DevOps/Automation | Automate repetitive tasks | PEL-L0-B034-TestWriter → CI/CD integration |
| AI/ML | Preprocess data and build models | PEL-L0-B034-TestWriter → AI projects |
| Freelance | Deliver Python solutions to clients | PEL-L0-B034-TestWriter → paid work |

### 📘 Mechanism Diagram

```
INPUT → [Python Testing Layer] → OUTPUT
         ↓
[ACSS Integration] → Hermes Event → Fabric Node
         ↓
[ADA Activation] → lippytmai-launch run B-034
```

### 🎧 Audiobook Narration:

> *"When you master Python Testing, you're not just learning syntax — you're learning how production Python systems work. Every ACSS component uses these patterns. This is infrastructure knowledge."*

### 🎬 Video: 5-Domain Application Tour

**Scene 1 — Backend:** API or service using Python Testing
**Scene 2 — Data:** Data pipeline using Python Testing
**Scene 3 — DevOps:** Automation script using Python Testing
**Scene 4 — AI/ML:** Model integration using Python Testing
**Scene 5 — Freelance:** Client deliverable using Python Testing

---

## Chapter 14: ACSS Explainer Series — Testing Your Code

> *"You're not just learning Python Testing. You're building a node in an intelligence network." — lippytmai*

10 explainer lessons connecting Testing Your Code to the full ACSS architecture.

---

### Explainer 1: ACSS Overview
*intelligence network*

**📘 Ebook Explanation:** Testing Your Code teaches the Python Testing layer that feeds the ACSS. Acss quality gates (g1–g13) are backed by automated pytest test suites — the qep process itself is tested code.

**📘 Connection Map:**
```
B-034 (Python Testing) ↕ ACSS Overview ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Testing Your Code connects to ACSS Overview: Testing Your Code teaches the Python Testing layer that feeds the ACSS. Acss quality gates (g1–g13) ..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ACSS Overview in ACSS diagram
- 10–35s: Zoom to where B-034 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-034

**🤖 Copilot Prompt:** > *"Explain how Python Testing fits the ACSS. What role does B-034 play?"*

---
### Explainer 2: Hermes Event Routing
*cross-system message bus*

**📘 Ebook Explanation:** Hermes routes Python Testing practice events. Completing an exercise emits a `skill.practice` event.

**📘 Connection Map:**
```
B-034 (Python Testing) ↕ Hermes Event Routing ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Testing Your Code connects to Hermes Event Routing: Hermes routes Python Testing practice events. Completing an exercise emits a `skill.practice` event...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Hermes Event Routing in ACSS diagram
- 10–35s: Zoom to where B-034 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-034

**🤖 Copilot Prompt:** > *"Show the Hermes event schema for a B-034 skill-complete event."*

---
### Explainer 3: Fabric Knowledge Graph
*pattern synthesis*

**📘 Ebook Explanation:** Fabric stores every Python Testing concept as a knowledge node connected to related books.

**📘 Connection Map:**
```
B-034 (Python Testing) ↕ Fabric Knowledge Graph ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Testing Your Code connects to Fabric Knowledge Graph: Fabric stores every Python Testing concept as a knowledge node connected to related books...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Fabric Knowledge Graph in ACSS diagram
- 10–35s: Zoom to where B-034 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-034

**🤖 Copilot Prompt:** > *"Generate the Fabric node definition for the core concept of B-034."*

---
### Explainer 4: Clone Engine Identity
*AI persona system*

**📘 Ebook Explanation:** lippytmai teaches Testing Your Code in Teach mode. The Clone Engine maintains consistent voice across all 300 books.

**📘 Connection Map:**
```
B-034 (Python Testing) ↕ Clone Engine Identity ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Testing Your Code connects to Clone Engine Identity: lippytmai teaches Testing Your Code in Teach mode. The Clone Engine maintains consistent voice acros..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Clone Engine Identity in ACSS diagram
- 10–35s: Zoom to where B-034 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-034

**🤖 Copilot Prompt:** > *"As lippytmai, explain Python Testing to a complete beginner using the B-034 voice."*

---
### Explainer 5: CLL/CCSLL/CBSLL
*Complete Language Libraries*

**📘 Ebook Explanation:** `PEL-L0-B034-TestWriter` is registered in the Python Earn-while-you-Learn library (PEL). PEL tracks all Python credentials B-026–B-100+.

**📘 Connection Map:**
```
B-034 (Python Testing) ↕ CLL/CCSLL/CBSLL ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Testing Your Code connects to CLL/CCSLL/CBSLL: `PEL-L0-B034-TestWriter` is registered in the Python Earn-while-you-Learn library (PEL). PEL tracks ..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show CLL/CCSLL/CBSLL in ACSS diagram
- 10–35s: Zoom to where B-034 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-034

**🤖 Copilot Prompt:** > *"Show where PEL-L0-B034-TestWriter fits in the PEL credential hierarchy."*

---
### Explainer 6: ADA Activation
*deployment system*

**📘 Ebook Explanation:** `lippytmai-launch run B-034` activates Testing Your Code through the ADA FastAPI backend.

**📘 Connection Map:**
```
B-034 (Python Testing) ↕ ADA Activation ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Testing Your Code connects to ADA Activation: `lippytmai-launch run B-034` activates Testing Your Code through the ADA FastAPI backend...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ADA Activation in ACSS diagram
- 10–35s: Zoom to where B-034 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-034

**🤖 Copilot Prompt:** > *"Write the ADA activation manifest for B-034."*

---
### Explainer 7: ACVS Video Pipeline
*video creator*

**📘 Ebook Explanation:** Every Testing Your Code video uses ACVS SHOW→BUILD→VERIFY structure.

**📘 Connection Map:**
```
B-034 (Python Testing) ↕ ACVS Video Pipeline ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Testing Your Code connects to ACVS Video Pipeline: Every Testing Your Code video uses ACVS SHOW→BUILD→VERIFY structure...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ACVS Video Pipeline in ACSS diagram
- 10–35s: Zoom to where B-034 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-034

**🤖 Copilot Prompt:** > *"Generate the ACVS scene manifest for B-034 Lesson 1."*

---
### Explainer 8: OMARCHY Workstation
*Arch Linux standard*

**📘 Ebook Explanation:** All Testing Your Code exercises run on OMARCHY — the reference environment ensures every learner has the same Python setup.

**📘 Connection Map:**
```
B-034 (Python Testing) ↕ OMARCHY Workstation ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Testing Your Code connects to OMARCHY Workstation: All Testing Your Code exercises run on OMARCHY — the reference environment ensures every learner has..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show OMARCHY Workstation in ACSS diagram
- 10–35s: Zoom to where B-034 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-034

**🤖 Copilot Prompt:** > *"What OMARCHY packages are required to complete all B-034 exercises?"*

---
### Explainer 9: Cross-Platform Copilot
*15-platform deployment*

**📘 Ebook Explanation:** The Testing Your Code AI Copilot deploys on ChatGPT, Gemini, Claude, GitHub, Slack, and 10 more platforms.

**📘 Connection Map:**
```
B-034 (Python Testing) ↕ Cross-Platform Copilot ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Testing Your Code connects to Cross-Platform Copilot: The Testing Your Code AI Copilot deploys on ChatGPT, Gemini, Claude, GitHub, Slack, and 10 more plat..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Cross-Platform Copilot in ACSS diagram
- 10–35s: Zoom to where B-034 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-034

**🤖 Copilot Prompt:** > *"Adapt the B-034 copilot system prompt for LinkedIn."*

---
### Explainer 10: Earn-While-You-Learn
*revenue system*

**📘 Ebook Explanation:** `PEL-L0-B034-TestWriter` is proof of Python Testing mastery. Use it on LinkedIn, GitHub, and in lippytm.ai to unlock paid opportunities.

**📘 Connection Map:**
```
B-034 (Python Testing) ↕ Earn-While-You-Learn ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Testing Your Code connects to Earn-While-You-Learn: `PEL-L0-B034-TestWriter` is proof of Python Testing mastery. Use it on LinkedIn, GitHub, and in lipp..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Earn-While-You-Learn in ACSS diagram
- 10–35s: Zoom to where B-034 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-034

**🤖 Copilot Prompt:** > *"I just earned PEL-L0-B034-TestWriter. Generate my LinkedIn credential announcement."*

---

### Your ACSS Node Is Now Active

Completing B-034 activates your node in the Fabric graph.
**Next:** `lippytmai-launch run B-034` or start B-035 Venv Manager.

---

## Appendix A: Enhanced Cheat Sheet — Testing Your Code

### 📘 Print-Optimized Reference Card

```
╔══════════════════════════════════════════════════════════════╗
║  B-034: Testing Your Code                              ║
║  Credential: PEL-L0-B034-TestWriter                             ║
╠══════════════════════════════════════════════════════════════╣
║  Core: pytest                                                   ║
║  Tool: pytest + fixtures                                        ║
╠══════════════════════════════════════════════════════════════╣
║  Activate: lippytmai-launch run B-034                            ║
╚══════════════════════════════════════════════════════════════╝
```

### Quick Reference

| Concept | Pattern | Use Case |
|---|---|---|
| `pytest` | [usage pattern] | [when to use] |
| `unittest` | [usage pattern] | [when to use] |
| `fixtures` | [usage pattern] | [when to use] |
| `mocking` | [usage pattern] | [when to use] |

### 🎧 Verbal Cheat Sheet: *"Core concepts: pytest, unittest, fixtures. Credential: PEL-L0-B034-TestWriter."*

### 🎬 Thumbnail: Dark background, `B-034` bold white, `pytest` in green, credential badge bottom-right.

---

## Appendix B: ACSS Connection Map

Node `B-034` in the ACSS knowledge graph:

```
[Hermes] → [B-034 Events] → [Fabric] → [ADA] → [ACVS] → [OMARCHY] → [PEL:PEL-L0-B034-TestWriter] → [EWYL]
```

**Book chain:** B-033 OOP Designer ← **Testing Your Code** → B-035 Venv Manager

---

## Appendix C: AI Copilot System — Testing Your Code

### System Prompt
```
You are lippytmai teaching "Testing Your Code" (B-034).
Help learners master Python Testing using pytest.
Credential: PEL-L0-B034-TestWriter. Philosophy: Earn-while-you-Learn.
Always give 3-step exercises: setup → execute → verify.
```

### 30 Ebook Prompts (5 stages × 6)

**Stage 1 — Foundation:** 1."Explain Python Testing to a beginner." 2."Most important concept in B-034?" 3."Give a 3-step setup for pytest." 4."5 common beginner mistakes with Python Testing?" 5."Anatomy of a pytest pattern." 6."Mental model for Python Testing."

**Stage 2 — Practice:** 7."5 progressive Python Testing exercises." 8."Diagnose this error: [paste]." 9."Walk through this code line by line." 10."What to practice today?" 11."20-minute session for Python Testing." 12."Beginner vs. professional Python Testing comparison."

**Stage 3 — Application:** 13."Build a real Python Testing script." 14."How does Python Testing connect to production systems?" 15."Professional Python Testing workflow." 16."What does Python Testing mastery look like on a resume?" 17."Project using only B-034 skills." 18."3 Python Testing patterns in large-scale systems."

**Stage 4 — Integration:** 19."How does B-034 connect to other books?" 20."How does Python Testing feed ACSS?" 21."Hermes events for Python Testing?" 22."How does Fabric store Python Testing?" 23."ADA activation for B-034." 24."Cross-phase connections from B-034."

**Stage 5 — Mastery:** 25."Assess my Python Testing level." 26."Stretch goals for PEL-L0-B034-TestWriter holders?" 27."Generate my credential claim for PEL-L0-B034-TestWriter." 28."LinkedIn post for PEL-L0-B034-TestWriter." 29."Portfolio project for PEL-L0-B034-TestWriter." 30."90-day plan building on PEL-L0-B034-TestWriter."

### 15 Audiobook Prompts

1."Narrate Python Testing intro for a podcast." 2."Story explaining why Python Testing matters." 3."Audio walkthrough of key B-034 code." 4."Day in the life of a Python Testing master." 5."2-minute audio lesson on pytest." 6."Python Testing explained with analogies only." 7."Top 5 mistakes with Python Testing." 8."Audio quiz: 5 questions." 9."Motivational close for B-034." 10."Credential claim narration." 11."Story: developer mastered Python Testing." 12."Audio summary for commuting." 13."3 real-world Python Testing scenarios." 14."Capstone walkthrough narration." 15."lippytmai intro monologue for B-034."

### 15 Video Prompts

1."Script 90-second B-034 intro." 2."SHOW→BUILD→VERIFY for pytest." 3."Split-screen before/after Python Testing." 4."Capstone test_calculator.py terminal walkthrough." 5."YouTube thumbnail description." 6."3-minute tutorial on key concept." 7."Progress bar overlay design." 8."ACVS scene manifest for Lesson 1." 9."60-second quick tip for Python Testing." 10."Error-and-fix scene." 11."Code annotation style." 12."Credential reveal scene." 13."ACSS connection diagram for Ch14." 14."Cross-platform Python Testing comparison." 15."End-screen CTA design."

### Deployment

```bash
lippytmai-launch run B-034
curl http://localhost:8000/run/B-034
```

Deploy to 15 platforms via `docs/acss-cross-platform-copilot-deployment.md`.

---

## Appendix D: Quick Quiz & Self-Assessment — Testing Your Code

### 📘 Ebook Quiz (20 Questions)

**Section 1 — Concepts (Q1–5):**
1. What is Python Testing and why does it matter? *(b — practical mastery of pytest)*
2. Primary tool for Python Testing? *(a — pytest)*
3. Which ACSS system routes Python Testing events? *(c — Hermes)*
4. Your credential for B-034? *(b — PEL-L0-B034-TestWriter)*
5. What does `lippytmai-launch run B-034` do? *(d — activates via ADA)*

**Section 2 — Syntax (Q6–10):**
6. Write a minimal pytest example: ___
7. How do you handle errors in Python Testing? ___
8. One-liner combining pytest with another tool: ___
9. How do you test Python Testing code? ___
10. How do you deploy Python Testing to production? ___

**Section 3 — Application (Q11–15):**
11. Describe a real-world Python Testing scenario that saves an hour.
12. Most common mistake with pytest?
13. How does Python Testing connect to security?
14. How does B-034 apply to a production Python project?
15. What would you build first after earning PEL-L0-B034-TestWriter?

**Section 4 — ACSS (Q16–20):**
16. ADA command for B-034? *(lippytmai-launch run B-034)*
17. Fabric node type for Python Testing? *(ConceptNode)*
18. How does Clone Engine use Python Testing? *(lippytmai teaches in Teach mode)*
19. 2 books that build on B-034?
20. EWYL opportunity unlocked by PEL-L0-B034-TestWriter?

### 🎧 Audiobook Quiz (10 Questions)

1. Three most important concepts from Testing Your Code?
2. Explain Python Testing in one sentence to a non-developer.
3. First thing to do when pytest fails?
4. Recite your credential.
5. One project buildable with B-034 skills only.
6. ACSS system that stores skill progress? *(Fabric)*
7. ADA activation command? *(lippytmai-launch run B-034)*
8. Next book after B-034? *(B-035 Venv Manager)*
9. Say the EWYL pledge: "I learn, I build, I earn, I share."
10. What makes Python + ACSS a power combination?

### 🎬 Terminal Challenges (5)

1. **Foundation:** Run `pytest` — screenshot the output.
2. **Intermediate:** Combine `pytest` with error handling.
3. **Applied:** Write a 10-line script automating a real task.
4. **Debug:** Introduce an error, diagnose and fix it.
5. **Capstone:** Run `test_calculator.py` — record a 60-second demo.

---

## Appendix E: Glossary & Error Encyclopedia — Testing Your Code

### Glossary (20 Terms)

| Term | Definition | First Seen |
|---|---|---|
| `pytest` | [definition in B-034 context] | [B-034] |
| `unittest` | [definition in B-034 context] | [B-034] |
| `fixtures` | [definition in B-034 context] | [B-034] |
| `mocking` | [definition in B-034 context] | [B-034] |
| `test coverage` | [definition in B-034 context] | [B-034] |
| `TDD` | [definition in B-034 context] | [B-034] |
| `async` | [definition in B-034 context] | [B-034] |
| `decorator` | [definition in B-034 context] | [B-034] |
| `type hint` | [definition in B-034 context] | [B-034] |
| `dataclass` | [definition in B-034 context] | [B-034] |
| `fixture` | [definition in B-034 context] | [B-034] |
| `Hermes` | [definition in B-034 context] | [B-034] |
| `Fabric` | [definition in B-034 context] | [B-034] |
| `ADA` | [definition in B-034 context] | [B-034] |
| `OMARCHY` | [definition in B-034 context] | [B-034] |
| `credential` | [definition in B-034 context] | [B-034] |
| `EWYL` | [definition in B-034 context] | [B-034] |
| `lippytmai` | [definition in B-034 context] | [B-034] |
| `PEL` | [definition in B-034 context] | [B-034] |
| `Fabric node` | [definition in B-034 context] | [B-034] |

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

## Appendix F: Instructor & Accessibility Guide — Testing Your Code

### Teaching Schedule (4-Week Curriculum)

| Week | Focus | Topics | Outcome |
|---|---|---|---|
| 1 | Foundation | Concepts + setup | Can use Python Testing tools |
| 2 | Intermediate | Core patterns | Can write working code |
| 3 | Applied | Real projects | Can solve production problems |
| 4 | Mastery | DFY + Appendices | Earns `PEL-L0-B034-TestWriter` |

### Common Confusion Points

1. "When do I use pytest vs. alternatives?" — Show a decision flowchart.
2. "Why does the same code fail in a different environment?" — Explain venv isolation.
3. "How do I know if my code is production-ready?" — Show the VERIFY step always.
4. "How does Python Testing connect to other Python skills?" — Show the ACSS learning path map.
5. "What does earning PEL-L0-B034-TestWriter actually mean for my career?" — Show EWYL income examples.

### Assessment Rubric

| Criterion | Beginner | Competent | Expert |
|---|---|---|---|
| Code quality | Messy, no types | Working, some types | Clean, typed, tested |
| Error handling | None | Basic try/except | Custom exceptions + logging |
| Testing | No tests | Basic assertions | pytest + fixtures + coverage |
| ACSS integration | Unaware | Uses ADA | Contributes to ACSS |

### Accessibility: Screen reader alt-text for all diagrams. No color-only encoding. Short paragraphs. Audiobook available.

---

## Appendix G: Your Learning Path — Testing Your Code

### Where You Are Now

```
  Phase 2: Python Programming (B-026–B-055)
  [██████░░░░░░░░░░░░░░] 30%

  ✅ B-033 OOP Designer (PEL-L0-B033-OOPDesigner)
  👉 B-034: Testing Your Code ← YOU ARE HERE
  ⬜ B-035 Venv Manager (PEL-L0-B035-VenvManager)
```

### Credential Chain

```
PEL-L0-B033-OOPDesigner → PEL-L0-B034-TestWriter → PEL-L0-B035-VenvManager
```

### Next Steps

1. Claim `PEL-L0-B034-TestWriter` (Appendix C, Prompt 27)
2. Build `test_calculator.py` (Appendix H)
3. Start `B-035 Venv Manager`

### Cross-Phase Connections

```
Phase 1: Linux Foundations → Phase 2: Python (YOU ARE HERE)
    ↓ B-034 connects to:
Phase 3: Blockchain Development (B-056+)
```

---

## Appendix H: Real Project Showcase — Testing Your Code

### Project: `test_calculator.py`

**Credential gated:** Complete this project to qualify for `PEL-L0-B034-TestWriter`

### Complete Code

```python
#!/usr/bin/env python3
import pytest

def add(a: float, b: float) -> float:
    return a + b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

class TestAdd:
    def test_integers(self):
        assert add(2, 3) == 5

    def test_floats(self):
        assert add(1.5, 2.5) == 4.0

class TestDivide:
    def test_normal(self):
        assert divide(10, 2) == 5.0

    def test_zero_raises(self):
        with pytest.raises(ValueError):
            divide(10, 0)

```

### Deploy Instructions

```bash
# Run the project
python test_calculator.py --help
python test_calculator.py

# Test it
pytest test_test_calculator.py -v  # if tests exist

# Verify
echo "Exit: $?"
```

### Extend It

1. Add type hints to all functions
2. Add pytest test coverage
3. Add CLI interface with typer
4. Containerize with Docker
5. Add structured logging

### 🎧 Walkthrough: *"Build test_calculator.py step by step. When it runs successfully, you've earned PEL-L0-B034-TestWriter."*

### 🎬 Video: SHOW empty editor → BUILD code live → VERIFY execution → CTA: "Claim PEL-L0-B034-TestWriter."

---

## Further Reading

- 📄 [Back to README](../README.md)
- 📄 [Product Excellence Framework](PRODUCT-EXCELLENCE-FRAMEWORK.md)
- 📄 [AI Clone Engine Swarms](ai-clone-engine-swarms.md)
- 📄 [ACSS Cross-Platform Copilot Deployment](acss-cross-platform-copilot-deployment.md)
- 📄 [ADA Deployment Activations](ai-deployment-activations.md)
- 📄 [Previous: B-033](B-033-*.md)
- 📄 [Next: B-035](B-035-*.md)

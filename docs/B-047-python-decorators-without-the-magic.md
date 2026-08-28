# B-047: Python Decorators Without the Magic

### @decorator, functools.wraps, and Higher-Order Functions Demystified

> *"Decorators look like magic until you understand they're just functions that take a function and return a function. Once that clicks, the entire Python ecosystem opens up — timing, caching, logging, authentication, retry logic, rate limiting. All of it is just decorators. And you can write your own."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Understand what decorators are and how they work mechanically
2. Write decorators that preserve function metadata with `functools.wraps`
3. Build decorators that accept arguments (decorator factories)
4. Use built-in decorators: `@property`, `@classmethod`, `@staticmethod`, `@lru_cache`
5. Build a `decorators.py` toolkit with timing, logging, retry, and rate-limit decorators

**Prerequisite:** B-028 (functions), B-033 (classes), B-036 (type hints)

**Build Artifact:** `~/developer-workspace/projects/python-foundations/decorators.py`

**Credential:** `CCSLL-L1-B047-DecoratorMaster` — on-chain on Base

---

## Chapter 1: Decorators Are Just Functions

```python
# Without decorator syntax — showing the mechanism
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before the function")
        result = func(*args, **kwargs)
        print("After the function")
        return result
    return wrapper

def greet(name: str) -> str:
    return f"Hello, {name}!"

# Apply decorator manually
greet = my_decorator(greet)
print(greet("Charles"))

# The @ syntax is identical — just cleaner
@my_decorator
def greet2(name: str) -> str:
    return f"Hello, {name}!"

print(greet2("lippytmai"))
# Output:
# Before the function
# Hello, Charles!
# After the function
```

---

## Chapter 2: functools.wraps — Preserving Metadata

```python
import functools
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

# WITHOUT wraps — metadata is lost
def bad_decorator(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

print(add.__name__)   # wrapper  ← WRONG
print(add.__doc__)    # None     ← WRONG

# WITH wraps — metadata is preserved
def good_decorator(func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return func(*args, **kwargs)
    return wrapper

@good_decorator
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

print(multiply.__name__)   # multiply  ← CORRECT
print(multiply.__doc__)    # Multiply two numbers.  ← CORRECT
```

---

## Chapter 3: Timing and Logging Decorators

```python
import functools
import time
import logging
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

log = logging.getLogger(__name__)

def timer(func: Callable[P, R]) -> Callable[P, R]:
    """Measure and print execution time."""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[TIMER] {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

def log_calls(func: Callable[P, R]) -> Callable[P, R]:
    """Log function calls with arguments and return value."""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        log.debug("Calling %s(args=%s, kwargs=%s)", func.__name__, args, kwargs)
        result = func(*args, **kwargs)
        log.debug("%s returned %r", func.__name__, result)
        return result
    return wrapper

@timer
@log_calls
def slow_sum(n: int) -> int:
    """Sum all numbers from 1 to n."""
    return sum(range(n + 1))

print(slow_sum(1_000_000))
```

---

## Chapter 4: Decorator Factories (Decorators with Arguments)

```python
import functools
import time
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

# A decorator factory returns a decorator
def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable:
    """Retry the decorated function on exception."""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_error: Exception | None = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    print(f"[RETRY] Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_error or RuntimeError("All retries failed")
        return wrapper
    return decorator

def rate_limit(calls_per_second: float = 1.0) -> Callable:
    """Enforce a minimum delay between calls."""
    min_interval = 1.0 / calls_per_second
    last_called: list[float] = [0.0]

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            elapsed = time.time() - last_called[0]
            remaining = min_interval - elapsed
            if remaining > 0:
                time.sleep(remaining)
            last_called[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.1)
def unreliable_api_call(n: int) -> str:
    if n < 3:
        raise ConnectionError("Network flaky")
    return "success"

@rate_limit(calls_per_second=2)
def rate_limited_fetch(url: str) -> str:
    return f"fetched: {url}"
```

---

## Chapter 5: Built-in Decorators

```python
from functools import lru_cache, cached_property
from dataclasses import dataclass

# @lru_cache — memoize expensive computations
@lru_cache(maxsize=256)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(40))      # fast — results cached
print(fib.cache_info())   # CacheInfo(hits=..., misses=...)

# @property — computed attributes
class Circle:
    def __init__(self, radius: float) -> None:
        self._radius = radius

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Radius must be positive")
        self._radius = value

    @property
    def area(self) -> float:
        import math
        return math.pi * self._radius ** 2

c = Circle(5)
print(c.area)       # 78.53...
c.radius = 10
print(c.area)       # 314.15...

# @cached_property — computed once, cached as attribute
@dataclass
class Document:
    text: str

    @cached_property
    def word_count(self) -> int:
        return len(self.text.split())

doc = Document("hello world from lippytmai")
print(doc.word_count)   # computed once
print(doc.word_count)   # returned from cache (no recomputation)
```

---

## Chapter 6: The Build — Decorator Toolkit

```python
#!/usr/bin/env python3
"""
decorators.py — B-047 Build Artifact

A reusable decorator toolkit for Python projects.
Import any decorator into your own code.

Usage:
    from decorators import timer, retry, rate_limit, validate_types
"""
from __future__ import annotations

import functools
import logging
import time
from typing import Any, Callable, TypeVar

log = logging.getLogger(__name__)
_R = TypeVar("_R")


def timer(func: Callable[..., _R]) -> Callable[..., _R]:
    """Log function execution time (uses perf_counter for accuracy)."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> _R:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        log.debug("[TIMER] %s: %.4fs", func.__name__, elapsed)
        return result
    return wrapper


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[..., _R]], Callable[..., _R]]:
    """Retry with exponential backoff on specified exceptions."""
    def decorator(func: Callable[..., _R]) -> Callable[..., _R]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> _R:
            current_delay = delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        raise
                    log.warning("[RETRY] %s attempt %d/%d failed: %s",
                                func.__name__, attempt, max_attempts, e)
                    time.sleep(current_delay)
                    current_delay *= backoff
            raise RuntimeError("unreachable")
        return wrapper
    return decorator


def rate_limit(calls_per_second: float = 1.0) -> Callable[[Callable[..., _R]], Callable[..., _R]]:
    """Enforce minimum interval between consecutive calls."""
    min_interval = 1.0 / calls_per_second
    last_called: list[float] = [0.0]

    def decorator(func: Callable[..., _R]) -> Callable[..., _R]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> _R:
            wait = min_interval - (time.time() - last_called[0])
            if wait > 0:
                time.sleep(wait)
            last_called[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator


def log_calls(level: int = logging.DEBUG) -> Callable[[Callable[..., _R]], Callable[..., _R]]:
    """Log every call with arguments and return value."""
    def decorator(func: Callable[..., _R]) -> Callable[..., _R]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> _R:
            log.log(level, "→ %s(args=%s kwargs=%s)", func.__name__, args, kwargs)
            result = func(*args, **kwargs)
            log.log(level, "← %s = %r", func.__name__, result)
            return result
        return wrapper
    return decorator


def deprecated(message: str = "") -> Callable[[Callable[..., _R]], Callable[..., _R]]:
    """Mark a function as deprecated — warns on every call."""
    import warnings
    def decorator(func: Callable[..., _R]) -> Callable[..., _R]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> _R:
            warn_msg = f"{func.__name__} is deprecated. {message}".strip()
            warnings.warn(warn_msg, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def demo() -> None:
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(message)s")

    @timer
    def slow(n: int) -> int:
        return sum(range(n))

    @retry(max_attempts=3, delay=0.05)
    def flaky(counter: list[int]) -> str:
        counter[0] += 1
        if counter[0] < 3:
            raise ValueError(f"Still not ready (attempt {counter[0]})")
        return "success"

    @rate_limit(calls_per_second=5)
    def api_call(n: int) -> int:
        return n * 2

    @deprecated("Use fast() instead.")
    def old_function() -> str:
        return "old"

    print("--- timer ---")
    slow(10_000_000)

    print("\n--- retry ---")
    c: list[int] = [0]
    print(flaky(c))

    print("\n--- rate_limit ---")
    for i in range(3):
        api_call(i)
    print("3 calls completed with rate limit")

    print("\n--- deprecated ---")
    import warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        old_function()
        print(f"Warning: {w[0].message}")


if __name__ == "__main__":
    demo()
```

```bash
python3 ~/developer-workspace/projects/python-foundations/decorators.py
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-047 Verification ==="
python3 -c "
import functools, time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f'[TIMER] {func.__name__}: {elapsed:.4f}s')
        return result
    return wrapper

@timer
def compute(n: int) -> int:
    '''Sum 0..n.'''
    return sum(range(n))

result = compute(1_000_000)
print(f'Result: {result}')
print(f'Name preserved: {compute.__name__}')
print(f'Doc preserved:  {compute.__doc__}')
print('✅ Decorators work')
"
```

---


## Chapter 12: Done-For-You Lessons — Python Decorators Without the Magic

> *"Done-for-you means it's already designed, structured, and proven. Your job: execute." — lippytmai*

10 ready-to-use lesson structures for Python Decorators using @decorator.

---

### DFY Lesson 1: Introduction to Python Decorators

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 01: Introduction to Python Decorators         │
│  Book: B-047  Tool: @decorator                 │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 1: Introduction to Python Decorators. Master @decorator with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `@decorator` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 1 of B-047: Introduction to Python Decorators. Give me 3 progressive exercises."

---
### DFY Lesson 2: Core @decorator Patterns

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 02: Core @decorator Patterns                  │
│  Book: B-047  Tool: @decorator                 │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 2: Core @decorator Patterns. Master @decorator with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `@decorator` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 2 of B-047: Core @decorator Patterns. Give me 3 progressive exercises."

---
### DFY Lesson 3: Three Formats: Ebook, Audiobook, Video

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 03: Three Formats: Ebook, Audiobook, Video    │
│  Book: B-047  Tool: @decorator                 │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 3: Three Formats: Ebook, Audiobook, Video. Master @decorator with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `@decorator` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 3 of B-047: Three Formats: Ebook, Audiobook, Video. Give me 3 progressive exercises."

---
### DFY Lesson 4: Common Mistakes in Python Decorators

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 04: Common Mistakes in Python Decorators      │
│  Book: B-047  Tool: @decorator                 │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 4: Common Mistakes in Python Decorators. Master @decorator with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `@decorator` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 4 of B-047: Common Mistakes in Python Decorators. Give me 3 progressive exercises."

---
### DFY Lesson 5: Building a Python Decorators Workflow

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 05: Building a Python Decorators Workflow     │
│  Book: B-047  Tool: @decorator                 │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 5: Building a Python Decorators Workflow. Master @decorator with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `@decorator` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 5 of B-047: Building a Python Decorators Workflow. Give me 3 progressive exercises."

---
### DFY Lesson 6: Automating with @decorator

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 06: Automating with @decorator                │
│  Book: B-047  Tool: @decorator                 │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 6: Automating with @decorator. Master @decorator with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `@decorator` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 6 of B-047: Automating with @decorator. Give me 3 progressive exercises."

---
### DFY Lesson 7: Testing Your Python Decorators Code

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 07: Testing Your Python Decorators Code       │
│  Book: B-047  Tool: @decorator                 │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 7: Testing Your Python Decorators Code. Master @decorator with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `@decorator` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 7 of B-047: Testing Your Python Decorators Code. Give me 3 progressive exercises."

---
### DFY Lesson 8: Production Python Decorators Patterns

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 08: Production Python Decorators Patterns     │
│  Book: B-047  Tool: @decorator                 │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 8: Production Python Decorators Patterns. Master @decorator with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `@decorator` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 8 of B-047: Production Python Decorators Patterns. Give me 3 progressive exercises."

---
### DFY Lesson 9: Debugging Python Decorators Problems

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 09: Debugging Python Decorators Problems      │
│  Book: B-047  Tool: @decorator                 │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 9: Debugging Python Decorators Problems. Master @decorator with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `@decorator` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 9 of B-047: Debugging Python Decorators Problems. Give me 3 progressive exercises."

---
### DFY Lesson 10: Earning Your PEL-L0-B047-DecoratorPro Credential

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 10: Earning Your PEL-L0-B047-DecoratorPro Cr  │
│  Book: B-047  Tool: @decorator                 │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 10: Earning Your PEL-L0-B047-DecoratorPro Credential. Master @decorator with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `@decorator` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 10 of B-047: Earning Your PEL-L0-B047-DecoratorPro Credential. Give me 3 progressive exercises."

---

### Claim Your Credential

Complete all 10 lessons → open Appendix C → run: *"Generate my credential claim for `PEL-L0-B047-DecoratorPro`."*

---

## Chapter 13: How It Works — Use Cases & Applications

> *"Knowing what to do is different from knowing why it matters." — lippytmai*

### The Mechanism

Python Decorators in Python works because the language was designed to be readable, composable, and deployable. @decorator is the tool that makes Python Decorators practical.

### 5 Real-World Use Cases

| Domain | Application | Your Credential Unlocks |
|---|---|---|
| Backend Dev | Build APIs and services with @decorator | PEL-L0-B047-DecoratorPro → production deployments |
| Data Engineering | Process and transform data pipelines | PEL-L0-B047-DecoratorPro → ETL roles |
| DevOps/Automation | Automate repetitive tasks | PEL-L0-B047-DecoratorPro → CI/CD integration |
| AI/ML | Preprocess data and build models | PEL-L0-B047-DecoratorPro → AI projects |
| Freelance | Deliver Python solutions to clients | PEL-L0-B047-DecoratorPro → paid work |

### 📘 Mechanism Diagram

```
INPUT → [Python Decorators Layer] → OUTPUT
         ↓
[ACSS Integration] → Hermes Event → Fabric Node
         ↓
[ADA Activation] → lippytmai-launch run B-047
```

### 🎧 Audiobook Narration:

> *"When you master Python Decorators, you're not just learning syntax — you're learning how production Python systems work. Every ACSS component uses these patterns. This is infrastructure knowledge."*

### 🎬 Video: 5-Domain Application Tour

**Scene 1 — Backend:** API or service using Python Decorators
**Scene 2 — Data:** Data pipeline using Python Decorators
**Scene 3 — DevOps:** Automation script using Python Decorators
**Scene 4 — AI/ML:** Model integration using Python Decorators
**Scene 5 — Freelance:** Client deliverable using Python Decorators

---

## Chapter 14: ACSS Explainer Series — Python Decorators Without the Magic

> *"You're not just learning Python Decorators. You're building a node in an intelligence network." — lippytmai*

10 explainer lessons connecting Python Decorators Without the Magic to the full ACSS architecture.

---

### Explainer 1: ACSS Overview
*intelligence network*

**📘 Ebook Explanation:** Python Decorators Without the Magic teaches the Python Decorators layer that feeds the ACSS. Decorators are used throughout acss for @hermes_event instrumentation, @fabric_node caching, and @ada_route endpoint registration.

**📘 Connection Map:**
```
B-047 (Python Decorators) ↕ ACSS Overview ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Python Decorators Without the Magic connects to ACSS Overview: Python Decorators Without the Magic teaches the Python Decorators layer that feeds the ACSS. Decorat..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ACSS Overview in ACSS diagram
- 10–35s: Zoom to where B-047 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-047

**🤖 Copilot Prompt:** > *"Explain how Python Decorators fits the ACSS. What role does B-047 play?"*

---
### Explainer 2: Hermes Event Routing
*cross-system message bus*

**📘 Ebook Explanation:** Hermes routes Python Decorators practice events. Completing an exercise emits a `skill.practice` event.

**📘 Connection Map:**
```
B-047 (Python Decorators) ↕ Hermes Event Routing ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Python Decorators Without the Magic connects to Hermes Event Routing: Hermes routes Python Decorators practice events. Completing an exercise emits a `skill.practice` eve..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Hermes Event Routing in ACSS diagram
- 10–35s: Zoom to where B-047 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-047

**🤖 Copilot Prompt:** > *"Show the Hermes event schema for a B-047 skill-complete event."*

---
### Explainer 3: Fabric Knowledge Graph
*pattern synthesis*

**📘 Ebook Explanation:** Fabric stores every Python Decorators concept as a knowledge node connected to related books.

**📘 Connection Map:**
```
B-047 (Python Decorators) ↕ Fabric Knowledge Graph ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Python Decorators Without the Magic connects to Fabric Knowledge Graph: Fabric stores every Python Decorators concept as a knowledge node connected to related books...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Fabric Knowledge Graph in ACSS diagram
- 10–35s: Zoom to where B-047 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-047

**🤖 Copilot Prompt:** > *"Generate the Fabric node definition for the core concept of B-047."*

---
### Explainer 4: Clone Engine Identity
*AI persona system*

**📘 Ebook Explanation:** lippytmai teaches Python Decorators Without the Magic in Teach mode. The Clone Engine maintains consistent voice across all 300 books.

**📘 Connection Map:**
```
B-047 (Python Decorators) ↕ Clone Engine Identity ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Python Decorators Without the Magic connects to Clone Engine Identity: lippytmai teaches Python Decorators Without the Magic in Teach mode. The Clone Engine maintains cons..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Clone Engine Identity in ACSS diagram
- 10–35s: Zoom to where B-047 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-047

**🤖 Copilot Prompt:** > *"As lippytmai, explain Python Decorators to a complete beginner using the B-047 voice."*

---
### Explainer 5: CLL/CCSLL/CBSLL
*Complete Language Libraries*

**📘 Ebook Explanation:** `PEL-L0-B047-DecoratorPro` is registered in the Python Earn-while-you-Learn library (PEL). PEL tracks all Python credentials B-026–B-100+.

**📘 Connection Map:**
```
B-047 (Python Decorators) ↕ CLL/CCSLL/CBSLL ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Python Decorators Without the Magic connects to CLL/CCSLL/CBSLL: `PEL-L0-B047-DecoratorPro` is registered in the Python Earn-while-you-Learn library (PEL). PEL track..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show CLL/CCSLL/CBSLL in ACSS diagram
- 10–35s: Zoom to where B-047 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-047

**🤖 Copilot Prompt:** > *"Show where PEL-L0-B047-DecoratorPro fits in the PEL credential hierarchy."*

---
### Explainer 6: ADA Activation
*deployment system*

**📘 Ebook Explanation:** `lippytmai-launch run B-047` activates Python Decorators Without the Magic through the ADA FastAPI backend.

**📘 Connection Map:**
```
B-047 (Python Decorators) ↕ ADA Activation ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Python Decorators Without the Magic connects to ADA Activation: `lippytmai-launch run B-047` activates Python Decorators Without the Magic through the ADA FastAPI b..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ADA Activation in ACSS diagram
- 10–35s: Zoom to where B-047 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-047

**🤖 Copilot Prompt:** > *"Write the ADA activation manifest for B-047."*

---
### Explainer 7: ACVS Video Pipeline
*video creator*

**📘 Ebook Explanation:** Every Python Decorators Without the Magic video uses ACVS SHOW→BUILD→VERIFY structure.

**📘 Connection Map:**
```
B-047 (Python Decorators) ↕ ACVS Video Pipeline ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Python Decorators Without the Magic connects to ACVS Video Pipeline: Every Python Decorators Without the Magic video uses ACVS SHOW→BUILD→VERIFY structure...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ACVS Video Pipeline in ACSS diagram
- 10–35s: Zoom to where B-047 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-047

**🤖 Copilot Prompt:** > *"Generate the ACVS scene manifest for B-047 Lesson 1."*

---
### Explainer 8: OMARCHY Workstation
*Arch Linux standard*

**📘 Ebook Explanation:** All Python Decorators Without the Magic exercises run on OMARCHY — the reference environment ensures every learner has the same Python setup.

**📘 Connection Map:**
```
B-047 (Python Decorators) ↕ OMARCHY Workstation ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Python Decorators Without the Magic connects to OMARCHY Workstation: All Python Decorators Without the Magic exercises run on OMARCHY — the reference environment ensures..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show OMARCHY Workstation in ACSS diagram
- 10–35s: Zoom to where B-047 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-047

**🤖 Copilot Prompt:** > *"What OMARCHY packages are required to complete all B-047 exercises?"*

---
### Explainer 9: Cross-Platform Copilot
*15-platform deployment*

**📘 Ebook Explanation:** The Python Decorators Without the Magic AI Copilot deploys on ChatGPT, Gemini, Claude, GitHub, Slack, and 10 more platforms.

**📘 Connection Map:**
```
B-047 (Python Decorators) ↕ Cross-Platform Copilot ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Python Decorators Without the Magic connects to Cross-Platform Copilot: The Python Decorators Without the Magic AI Copilot deploys on ChatGPT, Gemini, Claude, GitHub, Slack..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Cross-Platform Copilot in ACSS diagram
- 10–35s: Zoom to where B-047 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-047

**🤖 Copilot Prompt:** > *"Adapt the B-047 copilot system prompt for LinkedIn."*

---
### Explainer 10: Earn-While-You-Learn
*revenue system*

**📘 Ebook Explanation:** `PEL-L0-B047-DecoratorPro` is proof of Python Decorators mastery. Use it on LinkedIn, GitHub, and in lippytm.ai to unlock paid opportunities.

**📘 Connection Map:**
```
B-047 (Python Decorators) ↕ Earn-While-You-Learn ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Python Decorators Without the Magic connects to Earn-While-You-Learn: `PEL-L0-B047-DecoratorPro` is proof of Python Decorators mastery. Use it on LinkedIn, GitHub, and in..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Earn-While-You-Learn in ACSS diagram
- 10–35s: Zoom to where B-047 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-047

**🤖 Copilot Prompt:** > *"I just earned PEL-L0-B047-DecoratorPro. Generate my LinkedIn credential announcement."*

---

### Your ACSS Node Is Now Active

Completing B-047 activates your node in the Fabric graph.
**Next:** `lippytmai-launch run B-047` or start B-048 Config.

---

## Appendix A: Enhanced Cheat Sheet — Python Decorators Without the Magic

### 📘 Print-Optimized Reference Card

```
╔══════════════════════════════════════════════════════════════╗
║  B-047: Python Decorators Without the Magic            ║
║  Credential: PEL-L0-B047-DecoratorPro                           ║
╠══════════════════════════════════════════════════════════════╣
║  Core: decorators                                               ║
║  Tool: @decorator + functools                                   ║
╠══════════════════════════════════════════════════════════════╣
║  Activate: lippytmai-launch run B-047                            ║
╚══════════════════════════════════════════════════════════════╝
```

### Quick Reference

| Concept | Pattern | Use Case |
|---|---|---|
| `decorators` | [usage pattern] | [when to use] |
| `@` | [usage pattern] | [when to use] |
| `functools.wraps` | [usage pattern] | [when to use] |
| `class decorators` | [usage pattern] | [when to use] |

### 🎧 Verbal Cheat Sheet: *"Core concepts: decorators, @, functools.wraps. Credential: PEL-L0-B047-DecoratorPro."*

### 🎬 Thumbnail: Dark background, `B-047` bold white, `decorators` in green, credential badge bottom-right.

---

## Appendix B: ACSS Connection Map

Node `B-047` in the ACSS knowledge graph:

```
[Hermes] → [B-047 Events] → [Fabric] → [ADA] → [ACVS] → [OMARCHY] → [PEL:PEL-L0-B047-DecoratorPro] → [EWYL]
```

**Book chain:** B-046 CLI Builder ← **Python Decorators Without the Magic** → B-048 Config

---

## Appendix C: AI Copilot System — Python Decorators Without the Magic

### System Prompt
```
You are lippytmai teaching "Python Decorators Without the Magic" (B-047).
Help learners master Python Decorators using @decorator.
Credential: PEL-L0-B047-DecoratorPro. Philosophy: Earn-while-you-Learn.
Always give 3-step exercises: setup → execute → verify.
```

### 30 Ebook Prompts (5 stages × 6)

**Stage 1 — Foundation:** 1."Explain Python Decorators to a beginner." 2."Most important concept in B-047?" 3."Give a 3-step setup for @decorator." 4."5 common beginner mistakes with Python Decorators?" 5."Anatomy of a @decorator pattern." 6."Mental model for Python Decorators."

**Stage 2 — Practice:** 7."5 progressive Python Decorators exercises." 8."Diagnose this error: [paste]." 9."Walk through this code line by line." 10."What to practice today?" 11."20-minute session for Python Decorators." 12."Beginner vs. professional Python Decorators comparison."

**Stage 3 — Application:** 13."Build a real Python Decorators script." 14."How does Python Decorators connect to production systems?" 15."Professional Python Decorators workflow." 16."What does Python Decorators mastery look like on a resume?" 17."Project using only B-047 skills." 18."3 Python Decorators patterns in large-scale systems."

**Stage 4 — Integration:** 19."How does B-047 connect to other books?" 20."How does Python Decorators feed ACSS?" 21."Hermes events for Python Decorators?" 22."How does Fabric store Python Decorators?" 23."ADA activation for B-047." 24."Cross-phase connections from B-047."

**Stage 5 — Mastery:** 25."Assess my Python Decorators level." 26."Stretch goals for PEL-L0-B047-DecoratorPro holders?" 27."Generate my credential claim for PEL-L0-B047-DecoratorPro." 28."LinkedIn post for PEL-L0-B047-DecoratorPro." 29."Portfolio project for PEL-L0-B047-DecoratorPro." 30."90-day plan building on PEL-L0-B047-DecoratorPro."

### 15 Audiobook Prompts

1."Narrate Python Decorators intro for a podcast." 2."Story explaining why Python Decorators matters." 3."Audio walkthrough of key B-047 code." 4."Day in the life of a Python Decorators master." 5."2-minute audio lesson on @decorator." 6."Python Decorators explained with analogies only." 7."Top 5 mistakes with Python Decorators." 8."Audio quiz: 5 questions." 9."Motivational close for B-047." 10."Credential claim narration." 11."Story: developer mastered Python Decorators." 12."Audio summary for commuting." 13."3 real-world Python Decorators scenarios." 14."Capstone walkthrough narration." 15."lippytmai intro monologue for B-047."

### 15 Video Prompts

1."Script 90-second B-047 intro." 2."SHOW→BUILD→VERIFY for @decorator." 3."Split-screen before/after Python Decorators." 4."Capstone hermes_decorator.py terminal walkthrough." 5."YouTube thumbnail description." 6."3-minute tutorial on key concept." 7."Progress bar overlay design." 8."ACVS scene manifest for Lesson 1." 9."60-second quick tip for Python Decorators." 10."Error-and-fix scene." 11."Code annotation style." 12."Credential reveal scene." 13."ACSS connection diagram for Ch14." 14."Cross-platform Python Decorators comparison." 15."End-screen CTA design."

### Deployment

```bash
lippytmai-launch run B-047
curl http://localhost:8000/run/B-047
```

Deploy to 15 platforms via `docs/acss-cross-platform-copilot-deployment.md`.

---

## Appendix D: Quick Quiz & Self-Assessment — Python Decorators Without the Magic

### 📘 Ebook Quiz (20 Questions)

**Section 1 — Concepts (Q1–5):**
1. What is Python Decorators and why does it matter? *(b — practical mastery of decorators)*
2. Primary tool for Python Decorators? *(a — decorators)*
3. Which ACSS system routes Python Decorators events? *(c — Hermes)*
4. Your credential for B-047? *(b — PEL-L0-B047-DecoratorPro)*
5. What does `lippytmai-launch run B-047` do? *(d — activates via ADA)*

**Section 2 — Syntax (Q6–10):**
6. Write a minimal decorators example: ___
7. How do you handle errors in Python Decorators? ___
8. One-liner combining decorators with another tool: ___
9. How do you test Python Decorators code? ___
10. How do you deploy Python Decorators to production? ___

**Section 3 — Application (Q11–15):**
11. Describe a real-world Python Decorators scenario that saves an hour.
12. Most common mistake with decorators?
13. How does Python Decorators connect to security?
14. How does B-047 apply to a production Python project?
15. What would you build first after earning PEL-L0-B047-DecoratorPro?

**Section 4 — ACSS (Q16–20):**
16. ADA command for B-047? *(lippytmai-launch run B-047)*
17. Fabric node type for Python Decorators? *(ConceptNode)*
18. How does Clone Engine use Python Decorators? *(lippytmai teaches in Teach mode)*
19. 2 books that build on B-047?
20. EWYL opportunity unlocked by PEL-L0-B047-DecoratorPro?

### 🎧 Audiobook Quiz (10 Questions)

1. Three most important concepts from Python Decorators Without the Magic?
2. Explain Python Decorators in one sentence to a non-developer.
3. First thing to do when decorators fails?
4. Recite your credential.
5. One project buildable with B-047 skills only.
6. ACSS system that stores skill progress? *(Fabric)*
7. ADA activation command? *(lippytmai-launch run B-047)*
8. Next book after B-047? *(B-048 Config)*
9. Say the EWYL pledge: "I learn, I build, I earn, I share."
10. What makes Python + ACSS a power combination?

### 🎬 Terminal Challenges (5)

1. **Foundation:** Run `decorators` — screenshot the output.
2. **Intermediate:** Combine `decorators` with error handling.
3. **Applied:** Write a 10-line script automating a real task.
4. **Debug:** Introduce an error, diagnose and fix it.
5. **Capstone:** Run `hermes_decorator.py` — record a 60-second demo.

---

## Appendix E: Glossary & Error Encyclopedia — Python Decorators Without the Magic

### Glossary (20 Terms)

| Term | Definition | First Seen |
|---|---|---|
| `decorators` | [definition in B-047 context] | [B-047] |
| `@` | [definition in B-047 context] | [B-047] |
| `functools.wraps` | [definition in B-047 context] | [B-047] |
| `class decorators` | [definition in B-047 context] | [B-047] |
| `@property` | [definition in B-047 context] | [B-047] |
| `async` | [definition in B-047 context] | [B-047] |
| `decorator` | [definition in B-047 context] | [B-047] |
| `type hint` | [definition in B-047 context] | [B-047] |
| `dataclass` | [definition in B-047 context] | [B-047] |
| `fixture` | [definition in B-047 context] | [B-047] |
| `Hermes` | [definition in B-047 context] | [B-047] |
| `Fabric` | [definition in B-047 context] | [B-047] |
| `ADA` | [definition in B-047 context] | [B-047] |
| `OMARCHY` | [definition in B-047 context] | [B-047] |
| `credential` | [definition in B-047 context] | [B-047] |
| `EWYL` | [definition in B-047 context] | [B-047] |
| `lippytmai` | [definition in B-047 context] | [B-047] |
| `PEL` | [definition in B-047 context] | [B-047] |
| `Fabric node` | [definition in B-047 context] | [B-047] |
| `clone identity` | [definition in B-047 context] | [B-047] |

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

## Appendix F: Instructor & Accessibility Guide — Python Decorators Without the Magic

### Teaching Schedule (4-Week Curriculum)

| Week | Focus | Topics | Outcome |
|---|---|---|---|
| 1 | Foundation | Concepts + setup | Can use Python Decorators tools |
| 2 | Intermediate | Core patterns | Can write working code |
| 3 | Applied | Real projects | Can solve production problems |
| 4 | Mastery | DFY + Appendices | Earns `PEL-L0-B047-DecoratorPro` |

### Common Confusion Points

1. "When do I use decorators vs. alternatives?" — Show a decision flowchart.
2. "Why does the same code fail in a different environment?" — Explain venv isolation.
3. "How do I know if my code is production-ready?" — Show the VERIFY step always.
4. "How does Python Decorators connect to other Python skills?" — Show the ACSS learning path map.
5. "What does earning PEL-L0-B047-DecoratorPro actually mean for my career?" — Show EWYL income examples.

### Assessment Rubric

| Criterion | Beginner | Competent | Expert |
|---|---|---|---|
| Code quality | Messy, no types | Working, some types | Clean, typed, tested |
| Error handling | None | Basic try/except | Custom exceptions + logging |
| Testing | No tests | Basic assertions | pytest + fixtures + coverage |
| ACSS integration | Unaware | Uses ADA | Contributes to ACSS |

### Accessibility: Screen reader alt-text for all diagrams. No color-only encoding. Short paragraphs. Audiobook available.

---

## Appendix G: Your Learning Path — Python Decorators Without the Magic

### Where You Are Now

```
  Phase 2: Python Programming (B-026–B-055)
  [██████████████░░░░░░] 73%

  ✅ B-046 CLI Builder (PEL-L0-B046-CLIBuilder)
  👉 B-047: Python Decorators Without the Magic ← YOU ARE HERE
  ⬜ B-048 Config (PEL-L0-B048-ConfigPro)
```

### Credential Chain

```
PEL-L0-B046-CLIBuilder → PEL-L0-B047-DecoratorPro → PEL-L0-B048-ConfigPro
```

### Next Steps

1. Claim `PEL-L0-B047-DecoratorPro` (Appendix C, Prompt 27)
2. Build `hermes_decorator.py` (Appendix H)
3. Start `B-048 Config`

### Cross-Phase Connections

```
Phase 1: Linux Foundations → Phase 2: Python (YOU ARE HERE)
    ↓ B-047 connects to:
Phase 3: Blockchain Development (B-056+)
```

---

## Appendix H: Real Project Showcase — Python Decorators Without the Magic

### Project: `hermes_decorator.py`

**Credential gated:** Complete this project to qualify for `PEL-L0-B047-DecoratorPro`

### Complete Code

```python
#!/usr/bin/env python3
import functools
import time
from typing import Callable

def hermes_event(event_type: str):
    """Decorator that emits a Hermes event after function execution."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            print(f"[Hermes] {event_type} | fn={func.__name__} | elapsed={elapsed:.3f}s")
            return result
        return wrapper
    return decorator

@hermes_event("skill.practice")
def run_exercise(book_id: str) -> str:
    return f"Exercise complete: {book_id}"

```

### Deploy Instructions

```bash
# Run the project
python hermes_decorator.py --help
python hermes_decorator.py

# Test it
pytest test_hermes_decorator.py -v  # if tests exist

# Verify
echo "Exit: $?"
```

### Extend It

1. Add type hints to all functions
2. Add pytest test coverage
3. Add CLI interface with typer
4. Containerize with Docker
5. Add structured logging

### 🎧 Walkthrough: *"Build hermes_decorator.py step by step. When it runs successfully, you've earned PEL-L0-B047-DecoratorPro."*

### 🎬 Video: SHOW empty editor → BUILD code live → VERIFY execution → CTA: "Claim PEL-L0-B047-DecoratorPro."

---

## Further Reading

- 📄 [Back to README](../README.md)
- 📄 [Product Excellence Framework](PRODUCT-EXCELLENCE-FRAMEWORK.md)
- 📄 [AI Clone Engine Swarms](ai-clone-engine-swarms.md)
- 📄 [ACSS Cross-Platform Copilot Deployment](acss-cross-platform-copilot-deployment.md)
- 📄 [ADA Deployment Activations](ai-deployment-activations.md)
- 📄 [Previous: B-046](B-046-*.md)
- 📄 [Next: B-048](B-048-*.md)

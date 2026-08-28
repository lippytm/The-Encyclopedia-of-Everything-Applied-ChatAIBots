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

## Further Reading

- 📄 [`docs/B-028-functions-that-do-one-thing-well.md`](B-028-functions-that-do-one-thing-well.md) — Functions as first-class values
- 📄 [`docs/B-033-classes-and-objects-made-simple.md`](B-033-classes-and-objects-made-simple.md) — @property, @classmethod
- 📄 [`docs/B-049-logging-the-programs-memory.md`](B-049-logging-the-programs-memory.md) — Logging inside decorators
- 🏠 [`README.md`](../README.md) — Encyclopedia home

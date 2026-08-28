# B-036: Type Hints — Making Python Honest

### mypy, Optional, Union, and the Art of Self-Documenting Code

> *"Python is dynamically typed, but your brain is not. Type hints don't change what Python does at runtime — they change what you and your tools understand at read time. A codebase with type hints is a codebase that explains itself. mypy catches bugs before they run. That is power."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Add type hints to function signatures and variable assignments
2. Use `Optional`, `Union`, `List`, `Dict`, `Tuple`, and `Callable` from `typing`
3. Use Python 3.10+ syntax (`X | Y` instead of `Union[X, Y]`)
4. Run `mypy` to catch type errors before execution
5. Build a type-safe `text-processing-toolkit.py` with 100% mypy-clean code

**Prerequisite:** B-026 through B-035

**Build Artifact:** `~/developer-workspace/projects/python-foundations/text_toolkit.py`

**Credential:** `CCSLL-L1-B036-TypeSafeEngineer` — on-chain on Base

---

## Chapter 1: Why Type Hints?

```python
# Without type hints — what does this function accept? What does it return?
def process(data, config):
    ...

# With type hints — completely self-documenting
def process(data: list[str], config: dict[str, int]) -> list[str]:
    ...

# Type hints don't affect runtime behavior:
def add(a: int, b: int) -> int:
    return a + b

add(1, 2)         # works
add("a", "b")     # also works at runtime — Python doesn't enforce hints
# But mypy WILL catch it as an error before you run the code
```

---

## Chapter 2: Basic Type Annotations

```python
# Variable annotations
name: str = "lippytmai"
count: int = 42
ratio: float = 3.14
active: bool = True
nothing: None = None

# Function annotations
def greet(name: str) -> str:
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    return a + b

def is_valid(email: str) -> bool:
    return "@" in email

def log(message: str) -> None:    # None return = no return value
    print(f"[LOG] {message}")

# Collections (Python 3.9+ — use built-in types directly)
def process_names(names: list[str]) -> list[str]:
    return [n.title() for n in names]

def count_words(text: str) -> dict[str, int]:
    from collections import Counter
    return dict(Counter(text.split()))

def get_coords() -> tuple[float, float]:
    return (37.7749, -122.4194)
```

---

## Chapter 3: Optional and Union

```python
from typing import Optional, Union

# Optional[X] means "X or None"
# Python 3.10+: X | None  (same thing)
def find_user(user_id: int) -> Optional[str]:
    users = {1: "Charles", 2: "lippytmai"}
    return users.get(user_id)   # returns str or None

# Union[X, Y] means "X or Y"
# Python 3.10+: X | Y  (same thing)
def to_number(value: Union[str, int, float]) -> float:
    return float(value)

# Python 3.10+ syntax (preferred)
def find_score(name: str) -> float | None:
    scores = {"Alice": 95.0, "Bob": 82.0}
    return scores.get(name)

def parse(value: str | int) -> int:
    return int(value)
```

---

## Chapter 4: Advanced Types

```python
from typing import Callable, Any, TypeVar
from collections.abc import Sequence, Mapping

# Callable[[arg_types], return_type]
def apply(func: Callable[[int], int], value: int) -> int:
    return func(value)

double = lambda x: x * 2
print(apply(double, 5))   # 10

# TypeVar — for generic functions
T = TypeVar("T")

def first(items: list[T]) -> T | None:
    return items[0] if items else None

print(first([1, 2, 3]))       # 1 (int)
print(first(["a", "b"]))      # "a" (str)

# Sequence — read-only list/tuple
def total(numbers: Sequence[float]) -> float:
    return sum(numbers)

total([1.0, 2.0])        # works
total((1.0, 2.0))        # also works — tuple is a Sequence
```

---

## Chapter 5: Running mypy

```bash
# Install mypy
pip install mypy

# Run on a single file
mypy text_toolkit.py

# Run with strict mode (recommended)
mypy --strict text_toolkit.py

# Run on entire project
mypy src/

# Common mypy errors and what they mean:
# error: Argument 1 to "add" has incompatible type "str"; expected "int"
# error: Item "None" of "Optional[str]" has no attribute "upper"
# error: Function is missing a return type annotation
```

---

## Chapter 6: The Build — Type-Safe Text Toolkit

```python
#!/usr/bin/env python3
"""
text_toolkit.py — B-036 Build Artifact

A type-safe text processing toolkit.
Run: mypy --strict text_toolkit.py  →  Success: no issues found
"""
from __future__ import annotations

import re
from collections import Counter
from typing import Optional


def word_count(text: str) -> int:
    """Count words in a string."""
    return len(text.split())


def char_frequency(text: str) -> dict[str, int]:
    """Return character frequency (excluding spaces)."""
    return dict(Counter(c for c in text.lower() if c != " "))


def top_words(text: str, n: int = 5) -> list[tuple[str, int]]:
    """Return the n most common words."""
    words = re.findall(r"\b\w+\b", text.lower())
    return Counter(words).most_common(n)


def truncate(text: str, max_len: int, suffix: str = "...") -> str:
    """Truncate text to max_len, appending suffix if truncated."""
    if len(text) <= max_len:
        return text
    return text[: max_len - len(suffix)] + suffix


def normalize_whitespace(text: str) -> str:
    """Replace runs of whitespace with a single space."""
    return re.sub(r"\s+", " ", text).strip()


def extract_emails(text: str) -> list[str]:
    """Extract all email addresses from text."""
    pattern = r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Z|a-z]{2,}\b"
    return re.findall(pattern, text)


def extract_urls(text: str) -> list[str]:
    """Extract all URLs from text."""
    pattern = r"https?://[^\s]+"
    return re.findall(pattern, text)


def is_palindrome(text: str) -> bool:
    """Return True if text is a palindrome (ignoring case and spaces)."""
    cleaned = re.sub(r"[^a-z0-9]", "", text.lower())
    return cleaned == cleaned[::-1]


def safe_split(text: str, delimiter: Optional[str] = None) -> list[str]:
    """Split text, returning empty list on empty input."""
    if not text.strip():
        return []
    return text.split(delimiter)


def demo() -> None:
    sample = """
    Hello, Charles! Contact us at hello@lippytm.ai or support@acss.dev.
    Visit https://lippytm.ai or https://docs.lippytm.ai/acss for docs.
    The quick brown fox jumps over the lazy dog. The dog barked.
    """

    print("=== Text Toolkit Demo ===\n")
    print(f"Word count:     {word_count(sample)}")
    print(f"Top 5 words:    {top_words(sample, 5)}")
    print(f"Emails:         {extract_emails(sample)}")
    print(f"URLs:           {extract_urls(sample)}")
    print(f"Truncated:      {truncate('Hello, lippytmai world!', 15)}")
    print(f"Palindrome:     {is_palindrome('racecar')}")
    print(f"Not palindrome: {is_palindrome('hello')}")
    print(f"Safe split '':  {safe_split('')}")
    print(f"Normalized:     {normalize_whitespace('  too   many   spaces  ')}")


if __name__ == "__main__":
    demo()
```

```bash
pip install mypy
mypy --strict ~/developer-workspace/projects/python-foundations/text_toolkit.py
python3 ~/developer-workspace/projects/python-foundations/text_toolkit.py
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-036 Verification ==="
python3 -c "
from typing import Optional, Union

def find(key: str) -> Optional[str]:
    data = {'a': 'alpha'}
    return data.get(key)

result = find('a')
if result is not None:
    print('Found:', result.upper())

result2 = find('z')
print('Not found:', result2)
print('✅ Type hints work')
"
python3 ~/developer-workspace/projects/python-foundations/text_toolkit.py
```

---

## Further Reading

- 📄 [`docs/B-028-functions-that-do-one-thing-well.md`](B-028-functions-that-do-one-thing-well.md) — Type hints introduced here
- 📄 [`docs/B-033-classes-and-objects-made-simple.md`](B-033-classes-and-objects-made-simple.md) — dataclass fields benefit from type hints
- 📄 [`docs/B-037-working-with-dates-and-times.md`](B-037-working-with-dates-and-times.md) — datetime type annotations
- 🏠 [`README.md`](../README.md) — Encyclopedia home

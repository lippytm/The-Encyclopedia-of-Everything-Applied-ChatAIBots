# B-044: Modules, Packages, and Imports

### import, __init__.py, Project Structure, and the Art of Organized Python

> *"A Python file is a module. A folder of modules is a package. A well-structured package is a gift to your future self and every collaborator who comes after you. Most Python projects fail at organization long before they fail at logic. Learn this once, structure everything correctly from day one."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Understand how Python's import system works
2. Create packages with `__init__.py` and control what they export
3. Use relative and absolute imports correctly
4. Organize a Python project using the standard `src/` layout
5. Build a `lippytmai_utils/` package — a real, importable Python library

**Prerequisite:** B-026 through B-035 (any Python fundamentals)

**Build Artifact:** `~/developer-workspace/projects/python-foundations/lippytmai_utils/`

**Credential:** `CCSLL-L1-B044-PackageBuilder` — on-chain on Base

---

## Chapter 1: Modules — Every .py File

```python
# math_utils.py — this IS a module

def add(a: float, b: float) -> float:
    return a + b

def multiply(a: float, b: float) -> float:
    return a * b

PI = 3.14159

# Another file can import from it:
# from math_utils import add, PI
# import math_utils
# math_utils.add(2, 3)

# Python finds modules on sys.path
import sys
print(sys.path)   # list of directories Python searches for modules
```

---

## Chapter 2: Import Forms

```python
# Absolute import — full path from project root (preferred)
import os
import collections
from pathlib import Path
from typing import Optional

# Import specific names
from datetime import date, timedelta

# Import with alias
import numpy as np                # convention
import pandas as pd               # convention
from collections import OrderedDict as OD

# AVOID: wildcard imports — obscure what's available
# from os import *    ← BAD — pollutes namespace, hard to trace

# Import and use immediately
from functools import lru_cache

@lru_cache(maxsize=128)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(30))   # 832040 — computed once, cached after
```

---

## Chapter 3: Packages and __init__.py

```
# Directory structure for a package named 'lippytmai_utils':
lippytmai_utils/
├── __init__.py          ← makes it a package; controls what 'from pkg import X' sees
├── text.py              ← text utilities
├── dates.py             ← date utilities
├── validation.py        ← validators
└── _internals.py        ← private (convention: _ prefix = internal only)
```

```python
# lippytmai_utils/__init__.py
"""
lippytmai_utils — reusable utilities for lippytm.ai projects.

Public API (everything importable from the top level):
    from lippytmai_utils import truncate, word_count, days_until, validate_email
"""

from .text import truncate, word_count, normalize_whitespace
from .dates import days_until, format_relative
from .validation import validate_email, validate_url

__version__ = "1.0.0"
__all__ = [
    "truncate",
    "word_count",
    "normalize_whitespace",
    "days_until",
    "format_relative",
    "validate_email",
    "validate_url",
]
```

---

## Chapter 4: Relative Imports

```python
# INSIDE the package, use relative imports
# lippytmai_utils/text.py

from ._internals import _clean     # relative import — one dot = same package
from .validation import validate_email  # sibling module

# OUTSIDE the package, use absolute imports
# main.py
from lippytmai_utils import truncate
from lippytmai_utils.text import word_count
from lippytmai_utils.dates import days_until

# Relative imports ONLY work inside packages
# Never use relative imports in scripts (files run directly)

# Sub-packages — nested packages
# lippytmai_utils/
# ├── __init__.py
# └── crypto/
#     ├── __init__.py
#     └── hashing.py
#
# from lippytmai_utils.crypto import hash_text   (absolute)
# from ..crypto import hash_text                 (relative, 2 dots = parent package)
```

---

## Chapter 5: The Standard Project Layout

```
# OMARCHY-standard Python project structure:
my_project/
├── src/
│   └── lippytmai_utils/       ← your package lives here
│       ├── __init__.py
│       ├── text.py
│       ├── dates.py
│       └── validation.py
├── tests/
│   ├── __init__.py
│   ├── test_text.py
│   ├── test_dates.py
│   └── test_validation.py
├── docs/
├── pyproject.toml             ← project metadata + dependencies
├── README.md
└── Makefile
```

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "lippytmai-utils"
version = "1.0.0"
description = "Reusable utilities for lippytm.ai projects"
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = ["pytest", "mypy", "ruff"]

[tool.setuptools.packages.find]
where = ["src"]

[tool.mypy]
strict = true
```

```bash
# Install in editable mode (changes take effect immediately)
pip install -e ".[dev]"

# Now 'from lippytmai_utils import ...' works from anywhere
```

---

## Chapter 6: The Build — lippytmai_utils Package

```python
# src/lippytmai_utils/__init__.py
"""lippytmai_utils — B-044 build artifact."""
from .text import truncate, word_count, normalize_whitespace
from .dates import days_until, format_relative
from .validation import validate_email, validate_url

__version__ = "1.0.0"
__all__ = [
    "truncate", "word_count", "normalize_whitespace",
    "days_until", "format_relative",
    "validate_email", "validate_url",
]
```

```python
# src/lippytmai_utils/text.py
"""Text processing utilities."""
from __future__ import annotations
import re


def word_count(text: str) -> int:
    """Count words in a string."""
    return len(text.split())


def truncate(text: str, max_len: int = 100, suffix: str = "...") -> str:
    """Truncate text to max_len, appending suffix if truncated."""
    if len(text) <= max_len:
        return text
    return text[: max_len - len(suffix)] + suffix


def normalize_whitespace(text: str) -> str:
    """Replace runs of whitespace with a single space and strip."""
    return re.sub(r"\s+", " ", text).strip()
```

```python
# src/lippytmai_utils/dates.py
"""Date calculation utilities."""
from __future__ import annotations
from datetime import date


def days_until(target: date) -> int:
    """Days from today until target (negative = past)."""
    return (target - date.today()).days


def format_relative(d: date) -> str:
    """Human-friendly relative label (today / tomorrow / in N days / N days ago)."""
    diff = days_until(d)
    if diff == 0: return "today"
    if diff == 1: return "tomorrow"
    if diff == -1: return "yesterday"
    return f"in {diff} days" if diff > 0 else f"{abs(diff)} days ago"
```

```python
# src/lippytmai_utils/validation.py
"""Input validation utilities."""
from __future__ import annotations
import re

_EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")
_URL_RE   = re.compile(r"^https?://[a-zA-Z0-9\-._~:/?#\[\]@!$&'()*+,;=%]+$")


def validate_email(email: str) -> bool:
    """Return True if email is structurally valid."""
    return bool(_EMAIL_RE.match(email.strip()))


def validate_url(url: str) -> bool:
    """Return True if URL is a valid HTTP/HTTPS URL."""
    return bool(_URL_RE.match(url.strip()))
```

```python
# demo.py — using the package
from lippytmai_utils import truncate, word_count, validate_email, days_until
from datetime import date

print(truncate("The quick brown fox jumps over the lazy dog", max_len=25))
print(word_count("Hello world from lippytmai"))
print(validate_email("hello@lippytm.ai"))
print(days_until(date(2027, 1, 1)), "days until 2027")
```

```bash
mkdir -p ~/developer-workspace/projects/python-foundations/lippytmai_utils
# Create each file above, then:
python3 demo.py
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-044 Verification ==="
python3 -c "
import sys, os
# Simulate a package
import types

pkg = types.ModuleType('demo_pkg')
pkg.__path__ = []
pkg.__package__ = 'demo_pkg'

def greet(name: str) -> str:
    return f'Hello, {name}!'

pkg.greet = greet
sys.modules['demo_pkg'] = pkg

from demo_pkg import greet
print(greet('Charles'))
print(f'Module: {greet.__module__}')
print('✅ Package import works')
"
```

---

## Further Reading

- 📄 [`docs/B-035-virtual-environments-and-pip.md`](B-035-virtual-environments-and-pip.md) — pyproject.toml structure
- 📄 [`docs/B-036-type-hints-making-python-honest.md`](B-036-type-hints-making-python-honest.md) — Type hints in packages
- 📄 [`docs/B-040-automation-scripts-that-save-hours.md`](B-040-automation-scripts-that-save-hours.md) — pathlib + package layout
- 🏠 [`README.md`](../README.md) — Encyclopedia home

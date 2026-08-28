# B-031: Errors That Tell the Truth

### try, except, raise, and the Art of Failing Gracefully

> *"A program that crashes with an unhelpful error message is worse than a program that crashes with no error. A program that handles errors gracefully and tells you exactly what went wrong — that's a program you can trust. Exceptions are not failures. They are messages."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Understand Python's exception hierarchy and the most common built-in exceptions
2. Write `try/except/else/finally` blocks correctly
3. Raise exceptions with informative messages using `raise`
4. Create custom exception classes that carry context
5. Build a `robust-file-reader.py` that handles every failure mode with a clear error message

**Prerequisite:** B-026 through B-030

**Build Artifact:** `~/developer-workspace/projects/python-foundations/robust_file_reader.py`

**Credential:** `CCSLL-L1-B031-ErrorHandler` — on-chain on Base

---

## Chapter 1: What Are Exceptions?

When Python encounters an error it cannot handle, it raises an **exception** — an object that describes what went wrong and where:

```python
# This raises a ZeroDivisionError
10 / 0

# This raises a TypeError
"hello" + 5

# This raises a FileNotFoundError
open("does-not-exist.txt")

# This raises a KeyError
d = {"a": 1}
d["b"]

# This raises an IndexError
lst = [1, 2, 3]
lst[10]

# This raises a ValueError
int("not a number")

# This raises an AttributeError
"hello".nonexistent_method()
```

All exceptions inherit from `BaseException`. The ones you'll handle are under `Exception`:

```
BaseException
└── Exception
    ├── ValueError        wrong value type or format
    ├── TypeError         wrong type
    ├── KeyError          dict key missing
    ├── IndexError        list index out of range
    ├── AttributeError    object has no such attribute
    ├── FileNotFoundError file doesn't exist
    ├── PermissionError   no access rights
    ├── ZeroDivisionError divided by zero
    ├── RuntimeError      general runtime problem
    └── OSError           operating system error (parent of File/Permission)
```

---

## Chapter 2: try / except

```python
# Basic pattern
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")

# Catch multiple specific exceptions
def safe_parse(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        print(f"'{value}' is not a valid integer")
        return 0
    except TypeError:
        print(f"Expected string, got {type(value).__name__}")
        return 0

safe_parse("42")       # 42
safe_parse("hello")    # error message + 0
safe_parse(None)       # error message + 0

# Catch and inspect the exception object
try:
    open("missing.txt")
except FileNotFoundError as e:
    print(f"Error: {e}")
    print(f"Error type: {type(e).__name__}")
    print(f"Filename: {e.filename}")

# Catch multiple exceptions in one line
try:
    data = {"key": "value"}["missing"]
except (KeyError, IndexError) as e:
    print(f"Access error: {e}")
```

---

## Chapter 3: else and finally

```python
# else runs ONLY when no exception was raised
# finally runs ALWAYS — even if an exception was raised

def read_number_from_file(path: str) -> float:
    try:
        with open(path) as f:
            text = f.read().strip()
            number = float(text)
    except FileNotFoundError:
        print(f"File not found: {path}")
        return 0.0
    except ValueError as e:
        print(f"File content is not a number: {e}")
        return 0.0
    else:
        # Only runs if no exception occurred
        print(f"Successfully read: {number}")
        return number
    finally:
        # Always runs — good for cleanup
        print("read_number_from_file complete")
```

---

## Chapter 4: raise — Signaling Your Own Errors

```python
from typing import List

def calculate_average(numbers: List[float]) -> float:
    if not numbers:
        raise ValueError("Cannot calculate average of an empty list")
    if not all(isinstance(n, (int, float)) for n in numbers):
        raise TypeError(f"All elements must be numeric, got: {numbers}")
    return sum(numbers) / len(numbers)

# Re-raise after logging
def load_config(path: str) -> dict:
    try:
        import json
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[error] Config file not found: {path}")
        raise   # re-raises the original exception
    except json.JSONDecodeError as e:
        print(f"[error] Invalid JSON in {path}: {e}")
        raise ValueError(f"Config file is not valid JSON: {path}") from e
```

---

## Chapter 5: Custom Exception Classes

```python
# Custom exceptions carry structured context
class BookNotFoundError(Exception):
    """Raised when an ebook cannot be found in the ADA registry."""

    def __init__(self, book_id: str, registry_path: str) -> None:
        self.book_id = book_id
        self.registry_path = registry_path
        super().__init__(
            f"Book '{book_id}' not found in registry at '{registry_path}'"
        )


class G13NotApprovedError(Exception):
    """Raised when trying to deploy a book that hasn't passed G13."""

    def __init__(self, book_id: str, qep_id: str) -> None:
        self.book_id = book_id
        self.qep_id = qep_id
        super().__init__(
            f"Book '{book_id}' cannot be deployed: "
            f"QEP '{qep_id}' not yet approved by Charles (G13)"
        )


class CredentialMintError(Exception):
    """Raised when on-chain credential minting fails."""
    pass


# Using custom exceptions
def deploy_book(book_id: str, registry: dict) -> None:
    if book_id not in registry:
        raise BookNotFoundError(book_id, "ada-registry.json")

    book = registry[book_id]
    if book.get("status") != "APPROVED":
        raise G13NotApprovedError(book_id, book.get("qep", "unknown"))

    print(f"Deploying {book_id}...")


# Catching custom exceptions
try:
    deploy_book("B-999", {})
except BookNotFoundError as e:
    print(f"Registry error: {e.book_id} — {e}")
except G13NotApprovedError as e:
    print(f"Approval required: {e.qep_id}")
```

---

## Chapter 6: The Build — Robust File Reader

```python
#!/usr/bin/env python3
"""
robust_file_reader.py — B-031 Build Artifact

Demonstrates comprehensive exception handling for file I/O operations.
Handles every failure mode with a clear, actionable error message.
"""
import json
from pathlib import Path
from typing import Any, Optional


class FileReadError(Exception):
    """Base exception for all file reading failures."""
    def __init__(self, path: str, reason: str) -> None:
        self.path = path
        self.reason = reason
        super().__init__(f"Cannot read '{path}': {reason}")


class FileParseError(FileReadError):
    """Raised when file content cannot be parsed."""
    pass


def read_text_file(path: str) -> str:
    """Read a text file, raising FileReadError on any failure."""
    p = Path(path)
    try:
        return p.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileReadError(path, "file does not exist")
    except PermissionError:
        raise FileReadError(path, "permission denied — try sudo?")
    except IsADirectoryError:
        raise FileReadError(path, f"'{path}' is a directory, not a file")
    except UnicodeDecodeError as e:
        raise FileReadError(path, f"not valid UTF-8 text: {e}")


def read_json_file(path: str) -> Any:
    """Read and parse a JSON file."""
    text = read_text_file(path)
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise FileParseError(
            path,
            f"invalid JSON at line {e.lineno}, column {e.colno}: {e.msg}"
        ) from e


def safe_read(path: str, default: Optional[str] = None) -> Optional[str]:
    """Read a file, returning default instead of raising on error."""
    try:
        return read_text_file(path)
    except FileReadError as e:
        print(f"[warning] {e}")
        return default


def demo() -> None:
    print("=== Robust File Reader Demo ===\n")

    # Test 1: valid file
    test_path = "/tmp/b031-test.txt"
    Path(test_path).write_text("Hello from B-031!\n")
    try:
        content = read_text_file(test_path)
        print(f"✅ Read success: {content.strip()}")
    except FileReadError as e:
        print(f"❌ {e}")

    # Test 2: missing file
    try:
        read_text_file("/tmp/nonexistent-b031.txt")
    except FileReadError as e:
        print(f"✅ Correctly caught: {e}")

    # Test 3: invalid JSON
    bad_json = "/tmp/b031-bad.json"
    Path(bad_json).write_text("{ this is not valid JSON }")
    try:
        read_json_file(bad_json)
    except FileParseError as e:
        print(f"✅ JSON parse error caught: {e.reason}")

    # Test 4: valid JSON
    good_json = "/tmp/b031-good.json"
    Path(good_json).write_text('{"book": "B-031", "level": 1}')
    data = read_json_file(good_json)
    print(f"✅ JSON loaded: book={data['book']}, level={data['level']}")

    # Test 5: safe_read returns default
    result = safe_read("/tmp/no-such-file.txt", default="(empty)")
    print(f"✅ safe_read default: '{result}'")

    print("\nAll error-handling scenarios demonstrated.")


if __name__ == "__main__":
    demo()
```

```bash
python3 ~/developer-workspace/projects/python-foundations/robust_file_reader.py
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-031 Verification ==="
python3 -c "
try:
    result = int('not-a-number')
except ValueError as e:
    print('✅ ValueError caught:', e)

try:
    d = {}
    d['missing']
except KeyError as e:
    print('✅ KeyError caught:', e)

print('✅ Exception handling works correctly')
"
python3 ~/developer-workspace/projects/python-foundations/robust_file_reader.py
```

---

## Further Reading

- 📄 [`docs/B-030-reading-and-writing-files.md`](B-030-reading-and-writing-files.md) — File I/O errors in context
- 📄 [`docs/B-032-the-internet-in-a-function.md`](B-032-the-internet-in-a-function.md) — HTTP error handling
- 🏠 [`README.md`](../README.md) — Encyclopedia home

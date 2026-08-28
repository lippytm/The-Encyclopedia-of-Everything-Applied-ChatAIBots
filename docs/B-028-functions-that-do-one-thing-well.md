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

## Further Reading

- 📄 [`docs/B-029-dictionaries-the-data-swiss-army-knife.md`](B-029-dictionaries-the-data-swiss-army-knife.md) — Dictionaries and JSON
- 📄 [`docs/B-027-lists-loops-and-logic.md`](B-027-lists-loops-and-logic.md) — Lists and loops used with functions
- 🏠 [`README.md`](../README.md) — Encyclopedia home

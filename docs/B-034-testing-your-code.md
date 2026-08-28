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

## Further Reading

- 📄 [`docs/B-028-functions-that-do-one-thing-well.md`](B-028-functions-that-do-one-thing-well.md) — The math_utils library being tested
- 📄 [`docs/B-033-classes-and-objects-made-simple.md`](B-033-classes-and-objects-made-simple.md) — Testing classes follows the same patterns
- 📄 [`docs/B-035-virtual-environments-and-pip.md`](B-035-virtual-environments-and-pip.md) — Installing pytest cleanly in a virtual environment
- 🏠 [`README.md`](../README.md) — Encyclopedia home

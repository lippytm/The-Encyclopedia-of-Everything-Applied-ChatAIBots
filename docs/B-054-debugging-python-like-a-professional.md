# B-054: Debugging Python Like a Professional

> *"Every bug is a question your program is asking you. Learning to debug means learning to listen."*

---

## Learning Objectives

By the end of this book you will:

1. Use `pdb` and `breakpoint()` to step through code interactively
2. Set conditional breakpoints, inspect call stacks, and watch variables
3. Debug FastAPI and async code effectively
4. Apply strategic logging as a permanent debugging layer
5. Use `py-spy` and `cProfile` to find performance bugs
6. Earn the `CCSLL-L1-B054-DebugEngineer` credential

---

## Chapter 1: The Debugging Mindset

Debugging is not guessing — it is a **scientific method**:

1. **Observe:** What is the actual behavior? What is the expected behavior?
2. **Hypothesize:** What could cause this difference?
3. **Test:** Add the smallest possible probe (breakpoint, log, assertion)
4. **Conclude:** Confirm the hypothesis or eliminate it

The worst debugging strategy is `print("here")` + `print("here2")` scattered everywhere and never removed.

---

## Chapter 2: `breakpoint()` — Your Most Powerful Tool

```python
from __future__ import annotations

def process_orders(orders: list[dict[str, object]]) -> list[dict[str, object]]:
    """Process a list of orders and return fulfilled ones."""
    fulfilled = []
    for order in orders:
        breakpoint()  # Execution pauses here — drop into pdb
        if order.get("status") == "paid" and order.get("items"):
            fulfilled.append({**order, "processed": True})
    return fulfilled
```

```
# pdb commands you use every day:
n        # next line (step over)
s        # step into function call
c        # continue to next breakpoint
l        # list current source context
p expr   # print expression
pp expr  # pretty-print expression
w        # where (print call stack)
u / d    # up / down the call stack
q        # quit debugger
```

`breakpoint()` is the Python 3.7+ equivalent of `import pdb; pdb.set_trace()` — prefer it.

---

## Chapter 3: Conditional Breakpoints

```python
from __future__ import annotations

def calculate_discount(price: float, quantity: int) -> float:
    """Apply bulk discount rules."""
    if quantity > 100:
        breakpoint()  # Only triggers when quantity > 100
    if quantity >= 10:
        return price * 0.9
    if quantity >= 50:
        return price * 0.8
    return price
```

In `pdb` you can also set conditional breakpoints on a line without modifying code:

```
# Inside pdb:
b filename.py:42, order['total'] > 1000   # break only when condition is true
```

---

## Chapter 4: Reading the Call Stack

```python
from __future__ import annotations
import traceback

def outer() -> None:
    inner()

def inner() -> None:
    raise ValueError("Something went wrong at the deepest level")

try:
    outer()
except ValueError:
    # Full traceback with local variables
    traceback.print_exc()

# Get structured traceback info
import sys
exc_type, exc_value, exc_tb = sys.exc_info()
```

When you're in `pdb` after a crash, `w` shows the full call stack. `u` and `d` move up/down. `p locals()` shows all variables at the current frame.

---

## Chapter 5: Strategic Logging as Permanent Debugging

```python
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

def process_payment(amount: float, currency: str, user_id: str) -> dict[str, object]:
    """Process a payment with full audit trail."""
    logger.info(
        "Processing payment",
        extra={"amount": amount, "currency": currency, "user_id": user_id},
    )
    try:
        # ... payment logic ...
        result = {"status": "success", "transaction_id": "txn_123"}
        logger.info("Payment successful", extra={"transaction_id": result["transaction_id"]})
        return result
    except Exception as exc:
        logger.exception(
            "Payment failed",
            extra={"amount": amount, "user_id": user_id, "error": str(exc)},
        )
        raise
```

The key insight: logs outlive debugging sessions. A well-logged function never needs `breakpoint()` in production.

---

## Chapter 6: Performance Debugging

```bash
# Profile with cProfile (built-in)
python3 -m cProfile -s cumulative my_script.py

# Profile a specific function
python3 -c "
import cProfile
import pstats
from my_module import slow_function
profiler = cProfile.Profile()
profiler.enable()
slow_function()
profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
"
```

```bash
# py-spy: zero-overhead sampling profiler for running processes
pip install py-spy

# Profile a running process
py-spy top --pid 12345

# Generate a flame graph
py-spy record -o profile.svg -- python3 my_script.py
```

---

## Chapter 7: Proof of Work — Debug a Broken Program

Save this buggy file as `broken.py`:

```python
from __future__ import annotations

def calculate_average(numbers: list[float]) -> float:
    """Calculate the average of a list of numbers."""
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)  # Bug: ZeroDivisionError on empty list

def find_max_product(items: list[dict[str, object]]) -> float:
    """Find the maximum product of price * quantity."""
    products = []
    for item in items:
        product = item["price"] * item["qty"]  # Bug: KeyError — field is "quantity"
        products.append(product)
    return max(products)

def transform_data(data: list[str]) -> list[int]:
    """Convert string numbers to integers, skipping invalid entries."""
    return [int(x) for x in data]  # Bug: ValueError on non-numeric strings

if __name__ == "__main__":
    print(calculate_average([]))
    print(find_max_product([{"price": 10.0, "quantity": 3}]))
    print(transform_data(["1", "2", "abc", "4"]))
```

Fix all three bugs using `breakpoint()` + `pdb`, then add guards:

```bash
python3 -m pdb broken.py
# Use: n, s, p, w to trace the crash
```

Fixed version demonstrates: empty list guard, KeyError with `.get()`, ValueError with `try/except` in comprehension.

**Credential earned:** `CCSLL-L1-B054-DebugEngineer`

---

## Further Reading

- 📄 [`docs/B-031-errors-that-tell-the-truth.md`](B-031-errors-that-tell-the-truth.md) — Exception handling foundations
- 📄 [`docs/B-049-logging-the-programs-memory.md`](B-049-logging-the-programs-memory.md) — Logging as permanent debugging
- 📄 [`docs/B-055-python-earn-while-you-learn-level-1-badge.md`](B-055-python-earn-while-you-learn-level-1-badge.md) — Phase 2 capstone
- 🏠 [`README.md`](../README.md) — Encyclopedia home

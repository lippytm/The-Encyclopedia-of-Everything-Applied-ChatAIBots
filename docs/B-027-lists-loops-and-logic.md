# B-027: Lists, Loops, and Logic

### FizzBuzz, Grade Calculators, and the Python Control Flow You'll Use Every Day

> *"A list holds the collection. A loop visits every item. An if statement makes the decision. These three primitives — combined in every conceivable way — are the foundation of 80% of the Python code ever written. Master them and you can write anything."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Create, index, slice, and modify Python lists
2. Write `for` and `while` loops with `break`, `continue`, and `else`
3. Use `if`/`elif`/`else` for branching logic
4. Combine loops, lists, and conditions to solve real problems
5. Build a `grade-calculator.py` that processes a list of scores and assigns letter grades

**Prerequisite:** B-026

**Build Artifact:** `~/developer-workspace/projects/python-foundations/grade-calculator.py`

**Credential:** `CCSLL-L0-B027-LogicBuilder` — on-chain on Base

---

## Chapter 1: Lists — Ordered Collections

```python
# Creating lists
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [42, "hello", True, 3.14, None]
empty = []

# Indexing (0-based)
print(fruits[0])     # apple
print(fruits[-1])    # cherry (last element)
print(fruits[-2])    # banana (second-to-last)

# Slicing [start:stop:step]
print(numbers[1:4])   # [2, 3, 4]
print(numbers[:3])    # [1, 2, 3]
print(numbers[2:])    # [3, 4, 5]
print(numbers[::2])   # [1, 3, 5] (every other)
print(numbers[::-1])  # [5, 4, 3, 2, 1] (reversed)

# Modifying lists
fruits.append("date")        # add to end
fruits.insert(1, "avocado")  # insert at index
fruits.remove("banana")      # remove by value
popped = fruits.pop()        # remove and return last
fruits.sort()                # sort in place
fruits.reverse()             # reverse in place

# List info
print(len(fruits))           # length
print("apple" in fruits)     # membership test
print(fruits.count("apple")) # occurrences
print(fruits.index("apple")) # first index of value
```

---

## Chapter 2: for Loops — Visiting Every Item

```python
# Basic for loop
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# With index using enumerate()
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# Range — when you need a numeric sequence
for i in range(5):          # 0, 1, 2, 3, 4
    print(i)

for i in range(1, 6):       # 1, 2, 3, 4, 5
    print(i)

for i in range(0, 10, 2):   # 0, 2, 4, 6, 8
    print(i)

# Iterating over strings
for char in "lippytmai":
    print(char, end=" ")

# Loop over a list and build a new list
squares = []
for n in range(1, 6):
    squares.append(n ** 2)
print(squares)  # [1, 4, 9, 16, 25]

# List comprehension — the Pythonic version
squares = [n ** 2 for n in range(1, 6)]
print(squares)  # [1, 4, 9, 16, 25]
```

---

## Chapter 3: while Loops — Loop Until a Condition is False

```python
# Basic while
count = 0
while count < 5:
    print(f"count = {count}")
    count += 1

# while with user input
answer = ""
while answer.lower() != "quit":
    answer = input("Type 'quit' to exit: ")
    print(f"You typed: {answer}")

# break — exit the loop immediately
for i in range(100):
    if i == 5:
        break
    print(i)
# Prints 0 1 2 3 4, then stops

# continue — skip to next iteration
for i in range(10):
    if i % 2 == 0:
        continue    # skip even numbers
    print(i)
# Prints 1 3 5 7 9

# while True — infinite loop with controlled exit
attempts = 0
while True:
    attempts += 1
    result = input("Enter 'yes': ")
    if result == "yes":
        print(f"Got it after {attempts} attempt(s)")
        break
    print("Try again.")
```

---

## Chapter 4: if / elif / else — Decision Making

```python
# Basic if
score = 85
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
elif score >= 60:
    print("D")
else:
    print("F")

# Comparison operators
# == equal, != not equal
# >  greater, < less
# >= greater or equal, <= less or equal

# Logical operators
age = 25
is_student = True
if age < 30 and is_student:
    print("Student discount applies")

if age < 18 or age > 65:
    print("Special pricing")

if not is_student:
    print("Full price")

# in — membership test
role = "admin"
if role in ["admin", "superuser", "root"]:
    print("Full access")

# Ternary expression (one-line if/else)
label = "pass" if score >= 60 else "fail"
print(label)
```

---

## Chapter 5: FizzBuzz — The Classic Logic Test

```python
# FizzBuzz: print 1–100
# - "Fizz" if divisible by 3
# - "Buzz" if divisible by 5
# - "FizzBuzz" if divisible by both
# - the number otherwise

for n in range(1, 101):
    if n % 15 == 0:        # check 15 first (both 3 and 5)
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)

# Pythonic one-liner version
result = ["FizzBuzz" if n % 15 == 0 else "Fizz" if n % 3 == 0 else "Buzz" if n % 5 == 0 else str(n)
          for n in range(1, 101)]
print(result[:10])  # first 10
```

---

## Chapter 6: The Build — Grade Calculator

```python
#!/usr/bin/env python3
"""
grade-calculator.py — B-027 Build Artifact

Processes a list of student scores and produces a grade report.
Demonstrates: lists, loops, conditionals, and f-string formatting.
"""
from typing import List


GRADE_SCALE = [
    (90, "A"),
    (80, "B"),
    (70, "C"),
    (60, "D"),
    (0,  "F"),
]


def assign_grade(score: float) -> str:
    """Convert a numeric score to a letter grade."""
    for threshold, letter in GRADE_SCALE:
        if score >= threshold:
            return letter
    return "F"


def calculate_stats(scores: List[float]) -> dict:
    """Calculate basic statistics for a list of scores."""
    if not scores:
        return {}
    return {
        "count":   len(scores),
        "average": sum(scores) / len(scores),
        "highest": max(scores),
        "lowest":  min(scores),
        "passing": sum(1 for s in scores if s >= 60),
    }


def print_report(students: List[dict]) -> None:
    """Print a formatted grade report."""
    print("\n" + "=" * 50)
    print(f"{'GRADE REPORT':^50}")
    print("=" * 50)
    print(f"{'Name':<20} {'Score':>6} {'Grade':>6}")
    print("-" * 50)

    scores = []
    for student in students:
        name = student["name"]
        score = student["score"]
        grade = assign_grade(score)
        scores.append(score)
        status = "✅" if score >= 60 else "❌"
        print(f"{name:<20} {score:>6.1f} {grade:>6}  {status}")

    print("-" * 50)
    stats = calculate_stats(scores)
    print(f"{'Average:':<20} {stats['average']:>6.1f}")
    print(f"{'Highest:':<20} {stats['highest']:>6.1f}")
    print(f"{'Lowest:':<20} {stats['lowest']:>6.1f}")
    print(f"{'Passing:':<20} {stats['passing']:>5}/{stats['count']}")
    print("=" * 50)


def main() -> None:
    students = [
        {"name": "Alice",   "score": 94.5},
        {"name": "Bob",     "score": 72.0},
        {"name": "Charlie", "score": 88.5},
        {"name": "Diana",   "score": 55.0},
        {"name": "Eve",     "score": 61.0},
        {"name": "Frank",   "score": 100.0},
        {"name": "Grace",   "score": 45.5},
    ]
    print_report(students)


if __name__ == "__main__":
    main()
```

```bash
python3 ~/developer-workspace/projects/python-foundations/grade-calculator.py
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-027 Verification ==="
python3 -c "
scores = [94.5, 72, 88.5, 55, 61, 100, 45.5]
for s in scores:
    grade = 'A' if s>=90 else 'B' if s>=80 else 'C' if s>=70 else 'D' if s>=60 else 'F'
    print(f'{s:.1f} -> {grade}')
"
python3 ~/developer-workspace/projects/python-foundations/grade-calculator.py
```

---

## Further Reading

- 📄 [`docs/B-028-functions-that-do-one-thing-well.md`](B-028-functions-that-do-one-thing-well.md) — Encapsulating logic in functions
- 📄 [`docs/B-026-your-first-python-program.md`](B-026-your-first-python-program.md) — Python variables and print()
- 🏠 [`README.md`](../README.md) — Encyclopedia home

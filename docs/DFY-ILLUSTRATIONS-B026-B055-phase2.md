# DFY Illustrations: Phase 2 Python Foundations (B-026–B-055)

## 900 Illustration Specs — Ebook + Audiobook + Video for All 300 DFY Lessons

> **📘 Ebook Figure** — Markdown-renderable visual anchored to the written lesson
> **🎧 Audiobook Callout** — Word-for-word narrator script (lippytmai voice)
> **🎬 Video Scene** — SHOW→BUILD→VERIFY frame description for terminal recording

*B-026 DFY-01 through B-028 DFY-05 are shown as full production specs — the template for all 300 lessons in this phase.*

---

## B-026 — Your First Python Program

---

### DFY-01: Hello World with Your Name

**📘 Ebook Figure — Annotated Code Block**
```python
# hello.py — your first Python program that does something real

import sys                              # ← access command-line arguments

def greet(name: str) -> str:           # ← type hint: input str, output str
    """Return a personalized greeting."""
    return f"Hello, {name}! Welcome to Python."   # ← f-string interpolation

if __name__ == "__main__":             # ← runs only when executed directly
    name = sys.argv[1] if len(sys.argv) > 1 else input("Your name: ")
    print(greet(name))                 # ← call the function, print result
```
```
$ python3 hello.py Charles
Hello, Charles! Welcome to Python.
```
*Figure 26.1: Every great program starts here. The `if __name__` guard is the first professional habit.*

**🎧 Audiobook Callout**
> *[CALLOUT TONE]*
> "Done-For-You Moment. Lesson 1: Hello World with Your Name.
> This isn't just 'Hello World.' This is your first program that takes input, processes it, and produces output — the three-act structure of every program you'll ever write. It uses a function, a type hint, an f-string, and a command-line argument. Four professional habits in 8 lines.
> Your deliverable is: `hello.py` — greets by name from a command-line argument or user input.
> Time to build: 5 minutes.
> Pause here. Build it. Then resume."
> *[CALLOUT TONE × 2]*

**🎬 Video Scene — SHOW→BUILD→VERIFY**
- **SHOW (0–15s):** `python3 hello.py Charles` → `Hello, Charles! Welcome to Python.`
- **BUILD (15s–4m):** Type each line. Explain `sys.argv`, f-strings, `if __name__`. No copy-paste.
- **VERIFY (4m–5m):** Run with name arg. Run without — shows `input()` prompt. Both work.

---

### DFY-02: Personal Info Card Generator

**📘 Ebook Figure — Architecture Map**
```
info_card.py output:
╔══════════════════════════════════════╗
║  🤖  lippytmai                       ║
║  Role: AI Teaching Agent             ║
║  Skills: Python · Linux · Solidity   ║
║  Repo: github.com/lippytm            ║
║  Credential: CCSLL-L1-B026          ║
╚══════════════════════════════════════╝

  Code structure:
  INFO = {                  ← config dict at top
    "name": "lippytmai",    ← change these 5 lines
    "role": "...",          ← for your personal card
    ...
  }
  def render_card(info):    ← pure function, easy to test
```
*Figure 26.2: A config dict at the top means anyone can customize this in 30 seconds.*

**🎧 Audiobook Callout**
> *[CALLOUT TONE]*
> "Done-For-You Moment. Lesson 2: Personal Info Card Generator.
> Think of this as a business card that lives in your terminal. Change five variables at the top, and every time you run the script you see a formatted card with your name, role, skills, and contact info. It's also your first real use of a dictionary, an f-string, and a function that returns a formatted string.
> Your deliverable is: `info_card.py` — your personalized terminal business card.
> Time to build: 15 minutes.
> Pause here. Build it. Then resume."
> *[CALLOUT TONE × 2]*

**🎬 Video Scene — SHOW→BUILD→VERIFY**
- **SHOW (0–15s):** `python3 info_card.py` — a formatted box appears with name, role, skills.
- **BUILD (15s–12m):** Config dict, `render_card()` function, box-drawing with print, f-strings.
- **VERIFY (12m–13m):** Change name and role. Rerun. Card updates instantly.

---

### DFY-03: Countdown Timer

**📘 Ebook Figure — Flow Diagram**
```
countdown.py --seconds 60

  Parse args (argparse)
        ↓
  Loop: remaining = 60, 59, 58 ...
        ↓
  Each iteration:
    print(f"\r⏱  {remaining:3d}s remaining", end="")  ← \r overwrites line
    time.sleep(1)
        ↓
  remaining == 0
        ↓
  print("\n✅ Time's up!")
  (optional: play sound via subprocess)
```
*Figure 26.3: `\r` moves the cursor to the start of the line without a newline — the trick behind live terminal updates.*

**🎧 Audiobook Callout**
> *[CALLOUT TONE]*
> "Done-For-You Moment. Lesson 3: Countdown Timer.
> Here's where Python starts feeling alive — a number counting down on a single line, overwriting itself each second with the `carriage return` character. You'll use this technique in progress bars, loading spinners, and live dashboards throughout your career.
> Your deliverable is: `countdown.py` — a live countdown timer with a visual display.
> Time to build: 20 minutes.
> Pause here. Build it. Then resume."
> *[CALLOUT TONE × 2]*

**🎬 Video Scene — SHOW→BUILD→VERIFY**
- **SHOW (0–15s):** `python3 countdown.py --seconds 10` — countdown runs, "Time's up!" appears.
- **BUILD (15s–16m):** `argparse`, `while` loop, `\r` trick, `sys.stdout.flush()`, `time.sleep`.
- **VERIFY (16m–17m):** Run 5-second countdown. Interrupt with `Ctrl+C` — graceful exit.

---

### DFY-04: Temperature Converter

**📘 Ebook Figure — Comparison Table**
```
Conversion formulas in code:
┌──────────────┬──────────────────────────────────┐
│ C → F        │ (celsius * 9/5) + 32             │
│ F → C        │ (fahrenheit - 32) * 5/9          │
│ C → K        │ celsius + 273.15                 │
│ K → C        │ kelvin - 273.15                  │
│ F → K        │ (fahrenheit - 32) * 5/9 + 273.15 │
│ K → F        │ (kelvin - 273.15) * 9/5 + 32     │
└──────────────┴──────────────────────────────────┘

$ python3 temp_convert.py 100 C F
100°C = 212.0°F
```
*Figure 26.4: A lookup dict of conversion functions makes adding new units a one-liner.*

**🎧 Audiobook Callout**
> *[CALLOUT TONE]*
> "Done-For-You Moment. Lesson 4: Temperature Converter.
> This script teaches you one of the most powerful Python patterns: storing functions in a dictionary. Instead of a long if-elif chain for six conversions, you have a two-line lookup. Adding a new conversion unit is a single dict entry.
> Your deliverable is: `temp_convert.py` — converts between Celsius, Fahrenheit, and Kelvin from the command line.
> Time to build: 10 minutes.
> Pause here. Build it. Then resume."
> *[CALLOUT TONE × 2]*

**🎬 Video Scene — SHOW→BUILD→VERIFY**
- **SHOW (0–15s):** `python3 temp_convert.py 37 C F` → `37°C = 98.6°F`
- **BUILD (15s–8m):** Six conversion functions, dispatch dict, `sys.argv` parsing, formatted output.
- **VERIFY (8m–9m):** Test all 6 conversion directions. Test invalid input — clean error message.

---

### DFY-05: BMI Calculator

**📘 Ebook Figure — Data Flow Map**
```
Input: weight=70kg, height=1.75m

  bmi = weight / (height ** 2)
      = 70 / (1.75 * 1.75)
      = 70 / 3.0625
      = 22.86

  Category lookup:
  < 18.5  → "Underweight"
  18.5–25 → "Normal weight"    ← 22.86 is here
  25–30   → "Overweight"
  ≥ 30    → "Obese"

Output: "BMI: 22.86 — Normal weight"
```
*Figure 26.5: Mapping a calculated value to a category is a fundamental pattern — you'll use it in every data pipeline.*

**🎧 Audiobook Callout**
> *[CALLOUT TONE]*
> "Done-For-You Moment. Lesson 5: BMI Calculator.
> The BMI formula is just two lines of math. The interesting part is the category lookup — mapping a continuous value to a named bucket. You'll use this pattern for credit scores, risk ratings, grade boundaries, sensor thresholds, and dozens of other real applications.
> Your deliverable is: `bmi.py` — calculates BMI and returns the category.
> Time to build: 15 minutes.
> Pause here. Build it. Then resume."
> *[CALLOUT TONE × 2]*

**🎬 Video Scene — SHOW→BUILD→VERIFY**
- **SHOW (0–15s):** `python3 bmi.py 70 1.75` → `BMI: 22.86 — Normal weight`
- **BUILD (15s–12m):** Formula, category dict with sorted boundaries, input validation.
- **VERIFY (12m–13m):** Test 4 inputs across all categories. Test negative input — error.

---

*[DFY-06 through DFY-10 for B-026 and full specs for B-027–B-055 follow the same three-format structure. They are produced by the `lippytmai` clone in TEACH mode during the book recording phase, triggered by Hermes event `ILLUS:{book_id}:{lesson}:READY`.]*

---

## Phase 2 Illustration Batch Production Schedule

| Batch | Books | Illustrations | Production Trigger |
|---|---|---|---|
| Batch 6 | B-026–B-030 | 150 | QEP-B026-B030 G13 approved ✅ |
| Batch 7 | B-031–B-035 | 150 | QEP-B031-B035 G13 approved ✅ |
| Batch 8 | B-036–B-040 | 150 | QEP-B036-B040 G13 approved ✅ |
| Batch 9 | B-041–B-045 | 150 | QEP-B041-B045 G13 approved ✅ |
| Batch 10 | B-046–B-050 | 150 | QEP-B046-B050 G13 approved ✅ |
| **Batch 11** | **B-051–B-055** | **150** | **QEP-B051-B055 awaiting G13** |

---

## Python-Specific Illustration Rules

In addition to the Phase 1 base rules, Phase 2 illustrations add:

### Ebook Code Annotations
Every code example gets **three layers of annotation**:
1. **Inline `# ← comment`** on any non-obvious line
2. **Section comment block** before each logical group
3. **Output block** showing exact terminal output after the code

```python
# ── Section header ───────────────────────────────────
import sys                              # ← stdlib: command-line access
from pathlib import Path               # ← modern path handling

def process(file: Path) -> list[str]:  # ← type hints: Path in, list out
    """Read lines from file, strip whitespace."""
    with file.open() as f:             # ← context manager: auto-close
        return [line.strip() for line in f]  # ← list comprehension
```

### Audiobook Python Callouts
Every Python callout includes a **"What Python teaches you here"** line:
> *"What Python teaches you in this lesson: {one-sentence insight about the language.}"*

### Video Python Scenes
Every Python video scene includes:
- **Editor view** for complex functions (Neovim with LSP hover)
- **Split view** for before/after comparisons (tmux, 2 panes)
- **Test run** always shows the exact output from the lesson deliverable

---

## Core Illustration Patterns for Phase 2 Topics

### For Functions and Classes
```
Function anatomy diagram:
  def function_name(param: type) -> return_type:
  │    │              │                │
  │    │              └─ typed input   └─ typed output
  │    └─ snake_case name
  └─ always def, never lambda for reusable functions
```

### For Error Handling
```
try/except flow:
  try:              ← attempt the risky operation
    result = risky()
  except SpecificError as e:    ← catch the most specific type first
    handle(e)       ← recover, log, or re-raise
  except Exception as e:        ← catch-all last
    log_and_reraise(e)
  else:             ← runs if NO exception
    process(result)
  finally:          ← ALWAYS runs (cleanup)
    cleanup()
```

### For Async Patterns
```
Sync (sequential):              Async (concurrent):
  fetch(url1) → 2s                fetch(url1) ─┐
  fetch(url2) → 2s                fetch(url2) ─┤ → all run at once
  fetch(url3) → 2s                fetch(url3) ─┘
  Total: 6s                       Total: ~2s
```

### For Type Hints
```
Type hint reading guide:
  list[str]           → a list where every item is a string
  dict[str, int]      → keys are strings, values are integers
  Optional[str]       → either a string or None
  str | None          → same as Optional[str] (Python 3.10+)
  Callable[[int], str]→ a function taking int, returning str
```

---

## DFY Illustration Index — Phase 2 Quick Reference

| Book | DFY-01 Type | DFY-05 Type | DFY-10 Type |
|---|---|---|---|
| B-026 | Annotated Code | Data Flow | Checklist |
| B-027 | Flow Diagram | Comparison | Annotated Code |
| B-028 | Architecture | Before/After | Template |
| B-029 | Comparison | Flow Diagram | Checklist |
| B-030 | Annotated Code | Flow Diagram | Template |
| B-031 | Architecture | Data Flow | Checklist |
| B-032 | Flow Diagram | Annotated Code | Checklist |
| B-033 | Architecture | Comparison | Checklist |
| B-034 | Flow Diagram | Data Flow | Checklist |
| B-035 | Before/After | Annotated Code | Template |
| B-036 | Annotated Code | Flow Diagram | Checklist |
| B-037 | Data Flow | Architecture | Template |
| B-038 | Annotated Code | Before/After | Template |
| B-039 | Flow Diagram | Architecture | Checklist |
| B-040 | Flow Diagram | Before/After | Checklist |
| B-041 | Flow Diagram | Before/After | Checklist |
| B-042 | Architecture | Flow Diagram | Checklist |
| B-043 | Comparison | Annotated Code | Template |
| B-044 | Architecture | Data Flow | Checklist |
| B-045 | Annotated Code | Flow Diagram | Checklist |
| B-046 | Before/After | Architecture | Checklist |
| B-047 | Flow Diagram | Annotated Code | Template |
| B-048 | Architecture | Before/After | Checklist |
| B-049 | Flow Diagram | Architecture | Checklist |
| B-050 | Comparison | Data Flow | Checklist |
| B-051 | Flow Diagram | Architecture | Checklist |
| B-052 | Comparison | Architecture | Checklist |
| B-053 | Before/After | Flow Diagram | Checklist |
| B-054 | Flow Diagram | Annotated Code | Checklist |
| B-055 | Architecture | Data Flow | Template |

---

## Further Reading

- 📄 [`docs/DFY-ILLUSTRATION-SYSTEM.md`](DFY-ILLUSTRATION-SYSTEM.md) — illustration standards
- 📄 [`docs/DFY-ILLUSTRATIONS-B001-B025-phase1.md`](DFY-ILLUSTRATIONS-B001-B025-phase1.md) — Phase 1 illustrations
- 📄 [`docs/DFY-B026-B055-phase2-python.md`](DFY-B026-B055-phase2-python.md) — Phase 2 DFY lessons
- 📄 [`docs/ai-copilot-video-sandbox-creator.md`](ai-copilot-video-sandbox-creator.md) — ACVS video pipeline
- 🏠 [`README.md`](../README.md) — Encyclopedia home

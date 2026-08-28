# B-037: Working with Dates and Times

### datetime, timedelta, timezone, and the Art of Scheduling

> *"Every program eventually needs to know what time it is. And every programmer eventually learns that time zones are a trap disguised as a solved problem. Learn datetime early. Respect UTC. And always store timestamps in ISO 8601 — your future self will thank you."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Create and format `date`, `time`, and `datetime` objects
2. Calculate durations using `timedelta`
3. Work correctly with time zones using `zoneinfo` (Python 3.9+)
4. Parse date strings with `strptime` and format with `strftime`
5. Build a `date-calculator.py` — a personal deadline and countdown tool

**Prerequisite:** B-036 (type hints recommended)

**Build Artifact:** `~/developer-workspace/projects/python-foundations/date_calculator.py`

**Credential:** `CCSLL-L1-B037-TimeEngineer` — on-chain on Base

---

## Chapter 1: The datetime Module

```python
from datetime import date, time, datetime, timedelta

# Today's date
today = date.today()
print(today)            # 2026-08-28
print(type(today))      # <class 'datetime.date'>

# Current datetime
now = datetime.now()
print(now)              # 2026-08-28 12:34:56.789

# Specific date
launch_day = date(2026, 1, 1)
print(launch_day)       # 2026-01-01

# Specific datetime
meeting = datetime(2026, 9, 1, 14, 30, 0)
print(meeting)          # 2026-09-01 14:30:00

# Access components
print(now.year, now.month, now.day)
print(now.hour, now.minute, now.second)
```

---

## Chapter 2: Formatting and Parsing

```python
from datetime import datetime

now = datetime.now()

# strftime — format datetime AS a string
print(now.strftime("%Y-%m-%d"))             # 2026-08-28
print(now.strftime("%B %d, %Y"))           # August 28, 2026
print(now.strftime("%A, %b %d %Y %H:%M")) # Thursday, Aug 28 2026 12:34
print(now.strftime("%I:%M %p"))            # 12:34 PM

# strptime — PARSE a string INTO a datetime
date_str = "2026-09-15"
parsed = datetime.strptime(date_str, "%Y-%m-%d")
print(parsed)                               # 2026-09-15 00:00:00

# ISO format (recommended for storage and APIs)
iso = now.isoformat()
print(iso)               # 2026-08-28T12:34:56.789000
back = datetime.fromisoformat(iso)
print(back)              # 2026-08-28 12:34:56.789000

# Common format codes
# %Y  4-digit year       %m  zero-padded month  %d  zero-padded day
# %H  24h hour           %I  12h hour           %M  minute  %S  second
# %A  weekday name       %B  month name         %p  AM/PM
# %f  microseconds       %Z  timezone name
```

---

## Chapter 3: timedelta — Working with Durations

```python
from datetime import date, datetime, timedelta

today = date.today()

# Create timedeltas
one_week = timedelta(weeks=1)
thirty_days = timedelta(days=30)
one_hour = timedelta(hours=1)
ninety_min = timedelta(minutes=90)

# Arithmetic with dates
next_week = today + one_week
last_month = today - thirty_days
print(next_week)    # 2026-09-04
print(last_month)   # 2026-07-29

# Difference between dates
start = date(2026, 1, 1)
end = date(2026, 12, 31)
gap = end - start
print(gap.days)     # 364
print(gap)          # 364 days, 0:00:00

# Days until a future event
release = date(2026, 11, 1)
days_left = (release - today).days
print(f"Days until release: {days_left}")

# Datetime arithmetic (hours, minutes, seconds)
event = datetime(2026, 9, 1, 9, 0)
two_hours_later = event + timedelta(hours=2)
print(two_hours_later)    # 2026-09-01 11:00:00
```

---

## Chapter 4: Time Zones — The Trap

```python
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo   # Python 3.9+

# RULE: always store timestamps as UTC
now_utc = datetime.now(tz=timezone.utc)
print(now_utc)          # 2026-08-28 12:34:56.789000+00:00
print(now_utc.isoformat())  # 2026-08-28T12:34:56.789000+00:00

# Convert to local time zones
pacific = ZoneInfo("America/Los_Angeles")
eastern = ZoneInfo("America/New_York")
london  = ZoneInfo("Europe/London")
tokyo   = ZoneInfo("Asia/Tokyo")

pacific_time = now_utc.astimezone(pacific)
eastern_time = now_utc.astimezone(eastern)
print(f"Pacific: {pacific_time.strftime('%H:%M %Z')}")
print(f"Eastern: {eastern_time.strftime('%H:%M %Z')}")

# List available timezones
import zoneinfo
# print(sorted(zoneinfo.available_timezones()))  # ~600 zones

# Naive vs Aware datetimes
naive = datetime.now()           # no timezone info — DANGEROUS for cross-system use
aware = datetime.now(tz=timezone.utc)  # has timezone — SAFE

# Best practice: ALWAYS use aware datetimes in production
```

---

## Chapter 5: Timestamps and Unix Epoch

```python
from datetime import datetime, timezone
import time

# Unix timestamp = seconds since 1970-01-01T00:00:00Z
now = datetime.now(tz=timezone.utc)
unix_ts = now.timestamp()
print(unix_ts)              # 1756393496.789

# Convert unix timestamp back to datetime
back = datetime.fromtimestamp(unix_ts, tz=timezone.utc)
print(back)                 # 2026-08-28 12:34:56+00:00

# Get current unix timestamp (faster, no datetime needed)
ts = time.time()
print(ts)                   # 1756393496.789

# Integer timestamp (for database storage)
ts_int = int(time.time())
print(ts_int)               # 1756393496

# ISO 8601 is the standard for human-readable exchange
print(now.isoformat())      # 2026-08-28T12:34:56.789000+00:00
```

---

## Chapter 6: The Build — Date Calculator

```python
#!/usr/bin/env python3
"""
date_calculator.py — B-037 Build Artifact

A personal deadline and countdown utility.
Usage: python3 date_calculator.py
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo


def days_until(target: date) -> int:
    """Return number of days from today until target date."""
    today = date.today()
    delta = target - today
    return delta.days


def days_since(past: date) -> int:
    """Return number of days since a past date."""
    return (date.today() - past).days


def add_business_days(start: date, n: int) -> date:
    """Add n business days (Mon–Fri) to start date."""
    current = start
    added = 0
    while added < n:
        current += timedelta(days=1)
        if current.weekday() < 5:   # 0=Mon, 4=Fri, 5=Sat, 6=Sun
            added += 1
    return current


def week_number(d: date) -> int:
    """Return ISO week number for a date."""
    return d.isocalendar()[1]


def format_relative(d: date) -> str:
    """Return a human-friendly relative label for a date."""
    today = date.today()
    diff = (d - today).days
    if diff == 0:
        return "today"
    if diff == 1:
        return "tomorrow"
    if diff == -1:
        return "yesterday"
    if diff > 0:
        return f"in {diff} days"
    return f"{abs(diff)} days ago"


def deadline_report(deadlines: dict[str, date]) -> None:
    """Print a formatted deadline report."""
    today = date.today()
    print(f"\n=== Deadline Report — {today.strftime('%B %d, %Y')} ===\n")
    print(f"{'Project':<30} {'Due Date':<15} {'Status':<20}")
    print("-" * 65)
    for name, due in sorted(deadlines.items(), key=lambda x: x[1]):
        diff = (due - today).days
        if diff < 0:
            status = f"⚠️  {abs(diff)} days overdue"
        elif diff == 0:
            status = "🔴 DUE TODAY"
        elif diff <= 3:
            status = f"🟠 {diff} days left"
        elif diff <= 7:
            status = f"🟡 {diff} days left"
        else:
            status = f"🟢 {diff} days left"
        print(f"{name:<30} {due.strftime('%Y-%m-%d'):<15} {status}")
    print()


def utc_now_display() -> None:
    """Display current time in multiple timezones."""
    now_utc = datetime.now(tz=timezone.utc)
    zones = {
        "UTC":         ZoneInfo("UTC"),
        "Los Angeles": ZoneInfo("America/Los_Angeles"),
        "New York":    ZoneInfo("America/New_York"),
        "London":      ZoneInfo("Europe/London"),
        "Tokyo":       ZoneInfo("Asia/Tokyo"),
    }
    print("\n=== Current Time Across Zones ===\n")
    for label, tz in zones.items():
        local = now_utc.astimezone(tz)
        print(f"  {label:<15} {local.strftime('%H:%M %Z  %Y-%m-%d')}")
    print()


def main() -> None:
    deadlines: dict[str, date] = {
        "B-036 Launch":             date(2026, 9, 1),
        "Phase 2 Batch 3 QEP":      date(2026, 9, 5),
        "ACSS v2 Release":          date(2026, 10, 1),
        "Q4 Curriculum Kickoff":    date(2026, 10, 15),
        "300-Book Milestone":       date(2027, 6, 1),
    }

    deadline_report(deadlines)
    utc_now_display()

    # Business day calculation
    today = date.today()
    two_weeks = add_business_days(today, 10)
    print(f"10 business days from today: {two_weeks.strftime('%B %d, %Y')}")
    print(f"Current ISO week number:     {week_number(today)}")


if __name__ == "__main__":
    main()
```

```bash
python3 ~/developer-workspace/projects/python-foundations/date_calculator.py
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-037 Verification ==="
python3 -c "
from datetime import date, timedelta

today = date.today()
future = date(2027, 1, 1)
days = (future - today).days
print(f'Days until 2027: {days}')

past = date(2020, 1, 1)
elapsed = (today - past).days
print(f'Days since 2020-01-01: {elapsed}')
print('✅ datetime works')
"
```

---


## Chapter 12: Done-For-You Lessons — Working with Dates and Times

> *"Done-for-you means it's already designed, structured, and proven. Your job: execute." — lippytmai*

10 ready-to-use lesson structures for Python Datetime using datetime.

---

### DFY Lesson 1: Introduction to Python Datetime

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 01: Introduction to Python Datetime           │
│  Book: B-037  Tool: datetime                   │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 1: Introduction to Python Datetime. Master datetime with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `datetime` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 1 of B-037: Introduction to Python Datetime. Give me 3 progressive exercises."

---
### DFY Lesson 2: Core datetime Patterns

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 02: Core datetime Patterns                    │
│  Book: B-037  Tool: datetime                   │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 2: Core datetime Patterns. Master datetime with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `datetime` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 2 of B-037: Core datetime Patterns. Give me 3 progressive exercises."

---
### DFY Lesson 3: Three Formats: Ebook, Audiobook, Video

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 03: Three Formats: Ebook, Audiobook, Video    │
│  Book: B-037  Tool: datetime                   │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 3: Three Formats: Ebook, Audiobook, Video. Master datetime with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `datetime` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 3 of B-037: Three Formats: Ebook, Audiobook, Video. Give me 3 progressive exercises."

---
### DFY Lesson 4: Common Mistakes in Python Datetime

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 04: Common Mistakes in Python Datetime        │
│  Book: B-037  Tool: datetime                   │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 4: Common Mistakes in Python Datetime. Master datetime with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `datetime` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 4 of B-037: Common Mistakes in Python Datetime. Give me 3 progressive exercises."

---
### DFY Lesson 5: Building a Python Datetime Workflow

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 05: Building a Python Datetime Workflow       │
│  Book: B-037  Tool: datetime                   │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 5: Building a Python Datetime Workflow. Master datetime with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `datetime` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 5 of B-037: Building a Python Datetime Workflow. Give me 3 progressive exercises."

---
### DFY Lesson 6: Automating with datetime

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 06: Automating with datetime                  │
│  Book: B-037  Tool: datetime                   │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 6: Automating with datetime. Master datetime with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `datetime` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 6 of B-037: Automating with datetime. Give me 3 progressive exercises."

---
### DFY Lesson 7: Testing Your Python Datetime Code

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 07: Testing Your Python Datetime Code         │
│  Book: B-037  Tool: datetime                   │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 7: Testing Your Python Datetime Code. Master datetime with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `datetime` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 7 of B-037: Testing Your Python Datetime Code. Give me 3 progressive exercises."

---
### DFY Lesson 8: Production Python Datetime Patterns

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 08: Production Python Datetime Patterns       │
│  Book: B-037  Tool: datetime                   │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 8: Production Python Datetime Patterns. Master datetime with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `datetime` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 8 of B-037: Production Python Datetime Patterns. Give me 3 progressive exercises."

---
### DFY Lesson 9: Debugging Python Datetime Problems

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 09: Debugging Python Datetime Problems        │
│  Book: B-037  Tool: datetime                   │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 9: Debugging Python Datetime Problems. Master datetime with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `datetime` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 9 of B-037: Debugging Python Datetime Problems. Give me 3 progressive exercises."

---
### DFY Lesson 10: Earning Your PEL-L0-B037-DatetimeMaster Credential

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 10: Earning Your PEL-L0-B037-DatetimeMaster   │
│  Book: B-037  Tool: datetime                   │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 10: Earning Your PEL-L0-B037-DatetimeMaster Credential. Master datetime with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `datetime` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 10 of B-037: Earning Your PEL-L0-B037-DatetimeMaster Credential. Give me 3 progressive exercises."

---

### Claim Your Credential

Complete all 10 lessons → open Appendix C → run: *"Generate my credential claim for `PEL-L0-B037-DatetimeMaster`."*

---

## Chapter 13: How It Works — Use Cases & Applications

> *"Knowing what to do is different from knowing why it matters." — lippytmai*

### The Mechanism

Python Datetime in Python works because the language was designed to be readable, composable, and deployable. datetime is the tool that makes Python Datetime practical.

### 5 Real-World Use Cases

| Domain | Application | Your Credential Unlocks |
|---|---|---|
| Backend Dev | Build APIs and services with datetime | PEL-L0-B037-DatetimeMaster → production deployments |
| Data Engineering | Process and transform data pipelines | PEL-L0-B037-DatetimeMaster → ETL roles |
| DevOps/Automation | Automate repetitive tasks | PEL-L0-B037-DatetimeMaster → CI/CD integration |
| AI/ML | Preprocess data and build models | PEL-L0-B037-DatetimeMaster → AI projects |
| Freelance | Deliver Python solutions to clients | PEL-L0-B037-DatetimeMaster → paid work |

### 📘 Mechanism Diagram

```
INPUT → [Python Datetime Layer] → OUTPUT
         ↓
[ACSS Integration] → Hermes Event → Fabric Node
         ↓
[ADA Activation] → lippytmai-launch run B-037
```

### 🎧 Audiobook Narration:

> *"When you master Python Datetime, you're not just learning syntax — you're learning how production Python systems work. Every ACSS component uses these patterns. This is infrastructure knowledge."*

### 🎬 Video: 5-Domain Application Tour

**Scene 1 — Backend:** API or service using Python Datetime
**Scene 2 — Data:** Data pipeline using Python Datetime
**Scene 3 — DevOps:** Automation script using Python Datetime
**Scene 4 — AI/ML:** Model integration using Python Datetime
**Scene 5 — Freelance:** Client deliverable using Python Datetime

---

## Chapter 14: ACSS Explainer Series — Working with Dates and Times

> *"You're not just learning Python Datetime. You're building a node in an intelligence network." — lippytmai*

10 explainer lessons connecting Working with Dates and Times to the full ACSS architecture.

---

### Explainer 1: ACSS Overview
*intelligence network*

**📘 Ebook Explanation:** Working with Dates and Times teaches the Python Datetime layer that feeds the ACSS. Utc timestamps are how hermes orders events, fabric tracks graph version history, and ada logs activation records.

**📘 Connection Map:**
```
B-037 (Python Datetime) ↕ ACSS Overview ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Working with Dates and Times connects to ACSS Overview: Working with Dates and Times teaches the Python Datetime layer that feeds the ACSS. Utc timestamps a..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ACSS Overview in ACSS diagram
- 10–35s: Zoom to where B-037 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-037

**🤖 Copilot Prompt:** > *"Explain how Python Datetime fits the ACSS. What role does B-037 play?"*

---
### Explainer 2: Hermes Event Routing
*cross-system message bus*

**📘 Ebook Explanation:** Hermes routes Python Datetime practice events. Completing an exercise emits a `skill.practice` event.

**📘 Connection Map:**
```
B-037 (Python Datetime) ↕ Hermes Event Routing ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Working with Dates and Times connects to Hermes Event Routing: Hermes routes Python Datetime practice events. Completing an exercise emits a `skill.practice` event..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Hermes Event Routing in ACSS diagram
- 10–35s: Zoom to where B-037 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-037

**🤖 Copilot Prompt:** > *"Show the Hermes event schema for a B-037 skill-complete event."*

---
### Explainer 3: Fabric Knowledge Graph
*pattern synthesis*

**📘 Ebook Explanation:** Fabric stores every Python Datetime concept as a knowledge node connected to related books.

**📘 Connection Map:**
```
B-037 (Python Datetime) ↕ Fabric Knowledge Graph ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Working with Dates and Times connects to Fabric Knowledge Graph: Fabric stores every Python Datetime concept as a knowledge node connected to related books...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Fabric Knowledge Graph in ACSS diagram
- 10–35s: Zoom to where B-037 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-037

**🤖 Copilot Prompt:** > *"Generate the Fabric node definition for the core concept of B-037."*

---
### Explainer 4: Clone Engine Identity
*AI persona system*

**📘 Ebook Explanation:** lippytmai teaches Working with Dates and Times in Teach mode. The Clone Engine maintains consistent voice across all 300 books.

**📘 Connection Map:**
```
B-037 (Python Datetime) ↕ Clone Engine Identity ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Working with Dates and Times connects to Clone Engine Identity: lippytmai teaches Working with Dates and Times in Teach mode. The Clone Engine maintains consistent ..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Clone Engine Identity in ACSS diagram
- 10–35s: Zoom to where B-037 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-037

**🤖 Copilot Prompt:** > *"As lippytmai, explain Python Datetime to a complete beginner using the B-037 voice."*

---
### Explainer 5: CLL/CCSLL/CBSLL
*Complete Language Libraries*

**📘 Ebook Explanation:** `PEL-L0-B037-DatetimeMaster` is registered in the Python Earn-while-you-Learn library (PEL). PEL tracks all Python credentials B-026–B-100+.

**📘 Connection Map:**
```
B-037 (Python Datetime) ↕ CLL/CCSLL/CBSLL ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Working with Dates and Times connects to CLL/CCSLL/CBSLL: `PEL-L0-B037-DatetimeMaster` is registered in the Python Earn-while-you-Learn library (PEL). PEL tra..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show CLL/CCSLL/CBSLL in ACSS diagram
- 10–35s: Zoom to where B-037 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-037

**🤖 Copilot Prompt:** > *"Show where PEL-L0-B037-DatetimeMaster fits in the PEL credential hierarchy."*

---
### Explainer 6: ADA Activation
*deployment system*

**📘 Ebook Explanation:** `lippytmai-launch run B-037` activates Working with Dates and Times through the ADA FastAPI backend.

**📘 Connection Map:**
```
B-037 (Python Datetime) ↕ ADA Activation ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Working with Dates and Times connects to ADA Activation: `lippytmai-launch run B-037` activates Working with Dates and Times through the ADA FastAPI backend...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ADA Activation in ACSS diagram
- 10–35s: Zoom to where B-037 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-037

**🤖 Copilot Prompt:** > *"Write the ADA activation manifest for B-037."*

---
### Explainer 7: ACVS Video Pipeline
*video creator*

**📘 Ebook Explanation:** Every Working with Dates and Times video uses ACVS SHOW→BUILD→VERIFY structure.

**📘 Connection Map:**
```
B-037 (Python Datetime) ↕ ACVS Video Pipeline ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Working with Dates and Times connects to ACVS Video Pipeline: Every Working with Dates and Times video uses ACVS SHOW→BUILD→VERIFY structure...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ACVS Video Pipeline in ACSS diagram
- 10–35s: Zoom to where B-037 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-037

**🤖 Copilot Prompt:** > *"Generate the ACVS scene manifest for B-037 Lesson 1."*

---
### Explainer 8: OMARCHY Workstation
*Arch Linux standard*

**📘 Ebook Explanation:** All Working with Dates and Times exercises run on OMARCHY — the reference environment ensures every learner has the same Python setup.

**📘 Connection Map:**
```
B-037 (Python Datetime) ↕ OMARCHY Workstation ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Working with Dates and Times connects to OMARCHY Workstation: All Working with Dates and Times exercises run on OMARCHY — the reference environment ensures every ..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show OMARCHY Workstation in ACSS diagram
- 10–35s: Zoom to where B-037 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-037

**🤖 Copilot Prompt:** > *"What OMARCHY packages are required to complete all B-037 exercises?"*

---
### Explainer 9: Cross-Platform Copilot
*15-platform deployment*

**📘 Ebook Explanation:** The Working with Dates and Times AI Copilot deploys on ChatGPT, Gemini, Claude, GitHub, Slack, and 10 more platforms.

**📘 Connection Map:**
```
B-037 (Python Datetime) ↕ Cross-Platform Copilot ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Working with Dates and Times connects to Cross-Platform Copilot: The Working with Dates and Times AI Copilot deploys on ChatGPT, Gemini, Claude, GitHub, Slack, and 1..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Cross-Platform Copilot in ACSS diagram
- 10–35s: Zoom to where B-037 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-037

**🤖 Copilot Prompt:** > *"Adapt the B-037 copilot system prompt for LinkedIn."*

---
### Explainer 10: Earn-While-You-Learn
*revenue system*

**📘 Ebook Explanation:** `PEL-L0-B037-DatetimeMaster` is proof of Python Datetime mastery. Use it on LinkedIn, GitHub, and in lippytm.ai to unlock paid opportunities.

**📘 Connection Map:**
```
B-037 (Python Datetime) ↕ Earn-While-You-Learn ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Working with Dates and Times connects to Earn-While-You-Learn: `PEL-L0-B037-DatetimeMaster` is proof of Python Datetime mastery. Use it on LinkedIn, GitHub, and in..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Earn-While-You-Learn in ACSS diagram
- 10–35s: Zoom to where B-037 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-037

**🤖 Copilot Prompt:** > *"I just earned PEL-L0-B037-DatetimeMaster. Generate my LinkedIn credential announcement."*

---

### Your ACSS Node Is Now Active

Completing B-037 activates your node in the Fabric graph.
**Next:** `lippytmai-launch run B-037` or start B-038 Regex.

---

## Appendix A: Enhanced Cheat Sheet — Working with Dates and Times

### 📘 Print-Optimized Reference Card

```
╔══════════════════════════════════════════════════════════════╗
║  B-037: Working with Dates and Times                   ║
║  Credential: PEL-L0-B037-DatetimeMaster                         ║
╠══════════════════════════════════════════════════════════════╣
║  Core: datetime                                                 ║
║  Tool: datetime + timezone                                      ║
╠══════════════════════════════════════════════════════════════╣
║  Activate: lippytmai-launch run B-037                            ║
╚══════════════════════════════════════════════════════════════╝
```

### Quick Reference

| Concept | Pattern | Use Case |
|---|---|---|
| `datetime` | [usage pattern] | [when to use] |
| `timedelta` | [usage pattern] | [when to use] |
| `timezone` | [usage pattern] | [when to use] |
| `strftime` | [usage pattern] | [when to use] |

### 🎧 Verbal Cheat Sheet: *"Core concepts: datetime, timedelta, timezone. Credential: PEL-L0-B037-DatetimeMaster."*

### 🎬 Thumbnail: Dark background, `B-037` bold white, `datetime` in green, credential badge bottom-right.

---

## Appendix B: ACSS Connection Map

Node `B-037` in the ACSS knowledge graph:

```
[Hermes] → [B-037 Events] → [Fabric] → [ADA] → [ACVS] → [OMARCHY] → [PEL:PEL-L0-B037-DatetimeMaster] → [EWYL]
```

**Book chain:** B-036 Type Hint Pro ← **Working with Dates and Times** → B-038 Regex

---

## Appendix C: AI Copilot System — Working with Dates and Times

### System Prompt
```
You are lippytmai teaching "Working with Dates and Times" (B-037).
Help learners master Python Datetime using datetime.
Credential: PEL-L0-B037-DatetimeMaster. Philosophy: Earn-while-you-Learn.
Always give 3-step exercises: setup → execute → verify.
```

### 30 Ebook Prompts (5 stages × 6)

**Stage 1 — Foundation:** 1."Explain Python Datetime to a beginner." 2."Most important concept in B-037?" 3."Give a 3-step setup for datetime." 4."5 common beginner mistakes with Python Datetime?" 5."Anatomy of a datetime pattern." 6."Mental model for Python Datetime."

**Stage 2 — Practice:** 7."5 progressive Python Datetime exercises." 8."Diagnose this error: [paste]." 9."Walk through this code line by line." 10."What to practice today?" 11."20-minute session for Python Datetime." 12."Beginner vs. professional Python Datetime comparison."

**Stage 3 — Application:** 13."Build a real Python Datetime script." 14."How does Python Datetime connect to production systems?" 15."Professional Python Datetime workflow." 16."What does Python Datetime mastery look like on a resume?" 17."Project using only B-037 skills." 18."3 Python Datetime patterns in large-scale systems."

**Stage 4 — Integration:** 19."How does B-037 connect to other books?" 20."How does Python Datetime feed ACSS?" 21."Hermes events for Python Datetime?" 22."How does Fabric store Python Datetime?" 23."ADA activation for B-037." 24."Cross-phase connections from B-037."

**Stage 5 — Mastery:** 25."Assess my Python Datetime level." 26."Stretch goals for PEL-L0-B037-DatetimeMaster holders?" 27."Generate my credential claim for PEL-L0-B037-DatetimeMaster." 28."LinkedIn post for PEL-L0-B037-DatetimeMaster." 29."Portfolio project for PEL-L0-B037-DatetimeMaster." 30."90-day plan building on PEL-L0-B037-DatetimeMaster."

### 15 Audiobook Prompts

1."Narrate Python Datetime intro for a podcast." 2."Story explaining why Python Datetime matters." 3."Audio walkthrough of key B-037 code." 4."Day in the life of a Python Datetime master." 5."2-minute audio lesson on datetime." 6."Python Datetime explained with analogies only." 7."Top 5 mistakes with Python Datetime." 8."Audio quiz: 5 questions." 9."Motivational close for B-037." 10."Credential claim narration." 11."Story: developer mastered Python Datetime." 12."Audio summary for commuting." 13."3 real-world Python Datetime scenarios." 14."Capstone walkthrough narration." 15."lippytmai intro monologue for B-037."

### 15 Video Prompts

1."Script 90-second B-037 intro." 2."SHOW→BUILD→VERIFY for datetime." 3."Split-screen before/after Python Datetime." 4."Capstone event_scheduler.py terminal walkthrough." 5."YouTube thumbnail description." 6."3-minute tutorial on key concept." 7."Progress bar overlay design." 8."ACVS scene manifest for Lesson 1." 9."60-second quick tip for Python Datetime." 10."Error-and-fix scene." 11."Code annotation style." 12."Credential reveal scene." 13."ACSS connection diagram for Ch14." 14."Cross-platform Python Datetime comparison." 15."End-screen CTA design."

### Deployment

```bash
lippytmai-launch run B-037
curl http://localhost:8000/run/B-037
```

Deploy to 15 platforms via `docs/acss-cross-platform-copilot-deployment.md`.

---

## Appendix D: Quick Quiz & Self-Assessment — Working with Dates and Times

### 📘 Ebook Quiz (20 Questions)

**Section 1 — Concepts (Q1–5):**
1. What is Python Datetime and why does it matter? *(b — practical mastery of datetime)*
2. Primary tool for Python Datetime? *(a — datetime)*
3. Which ACSS system routes Python Datetime events? *(c — Hermes)*
4. Your credential for B-037? *(b — PEL-L0-B037-DatetimeMaster)*
5. What does `lippytmai-launch run B-037` do? *(d — activates via ADA)*

**Section 2 — Syntax (Q6–10):**
6. Write a minimal datetime example: ___
7. How do you handle errors in Python Datetime? ___
8. One-liner combining datetime with another tool: ___
9. How do you test Python Datetime code? ___
10. How do you deploy Python Datetime to production? ___

**Section 3 — Application (Q11–15):**
11. Describe a real-world Python Datetime scenario that saves an hour.
12. Most common mistake with datetime?
13. How does Python Datetime connect to security?
14. How does B-037 apply to a production Python project?
15. What would you build first after earning PEL-L0-B037-DatetimeMaster?

**Section 4 — ACSS (Q16–20):**
16. ADA command for B-037? *(lippytmai-launch run B-037)*
17. Fabric node type for Python Datetime? *(ConceptNode)*
18. How does Clone Engine use Python Datetime? *(lippytmai teaches in Teach mode)*
19. 2 books that build on B-037?
20. EWYL opportunity unlocked by PEL-L0-B037-DatetimeMaster?

### 🎧 Audiobook Quiz (10 Questions)

1. Three most important concepts from Working with Dates and Times?
2. Explain Python Datetime in one sentence to a non-developer.
3. First thing to do when datetime fails?
4. Recite your credential.
5. One project buildable with B-037 skills only.
6. ACSS system that stores skill progress? *(Fabric)*
7. ADA activation command? *(lippytmai-launch run B-037)*
8. Next book after B-037? *(B-038 Regex)*
9. Say the EWYL pledge: "I learn, I build, I earn, I share."
10. What makes Python + ACSS a power combination?

### 🎬 Terminal Challenges (5)

1. **Foundation:** Run `datetime` — screenshot the output.
2. **Intermediate:** Combine `datetime` with error handling.
3. **Applied:** Write a 10-line script automating a real task.
4. **Debug:** Introduce an error, diagnose and fix it.
5. **Capstone:** Run `event_scheduler.py` — record a 60-second demo.

---

## Appendix E: Glossary & Error Encyclopedia — Working with Dates and Times

### Glossary (20 Terms)

| Term | Definition | First Seen |
|---|---|---|
| `datetime` | [definition in B-037 context] | [B-037] |
| `timedelta` | [definition in B-037 context] | [B-037] |
| `timezone` | [definition in B-037 context] | [B-037] |
| `strftime` | [definition in B-037 context] | [B-037] |
| `arrow` | [definition in B-037 context] | [B-037] |
| `dateutil` | [definition in B-037 context] | [B-037] |
| `async` | [definition in B-037 context] | [B-037] |
| `decorator` | [definition in B-037 context] | [B-037] |
| `type hint` | [definition in B-037 context] | [B-037] |
| `dataclass` | [definition in B-037 context] | [B-037] |
| `fixture` | [definition in B-037 context] | [B-037] |
| `Hermes` | [definition in B-037 context] | [B-037] |
| `Fabric` | [definition in B-037 context] | [B-037] |
| `ADA` | [definition in B-037 context] | [B-037] |
| `OMARCHY` | [definition in B-037 context] | [B-037] |
| `credential` | [definition in B-037 context] | [B-037] |
| `EWYL` | [definition in B-037 context] | [B-037] |
| `lippytmai` | [definition in B-037 context] | [B-037] |
| `PEL` | [definition in B-037 context] | [B-037] |
| `Fabric node` | [definition in B-037 context] | [B-037] |

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

## Appendix F: Instructor & Accessibility Guide — Working with Dates and Times

### Teaching Schedule (4-Week Curriculum)

| Week | Focus | Topics | Outcome |
|---|---|---|---|
| 1 | Foundation | Concepts + setup | Can use Python Datetime tools |
| 2 | Intermediate | Core patterns | Can write working code |
| 3 | Applied | Real projects | Can solve production problems |
| 4 | Mastery | DFY + Appendices | Earns `PEL-L0-B037-DatetimeMaster` |

### Common Confusion Points

1. "When do I use datetime vs. alternatives?" — Show a decision flowchart.
2. "Why does the same code fail in a different environment?" — Explain venv isolation.
3. "How do I know if my code is production-ready?" — Show the VERIFY step always.
4. "How does Python Datetime connect to other Python skills?" — Show the ACSS learning path map.
5. "What does earning PEL-L0-B037-DatetimeMaster actually mean for my career?" — Show EWYL income examples.

### Assessment Rubric

| Criterion | Beginner | Competent | Expert |
|---|---|---|---|
| Code quality | Messy, no types | Working, some types | Clean, typed, tested |
| Error handling | None | Basic try/except | Custom exceptions + logging |
| Testing | No tests | Basic assertions | pytest + fixtures + coverage |
| ACSS integration | Unaware | Uses ADA | Contributes to ACSS |

### Accessibility: Screen reader alt-text for all diagrams. No color-only encoding. Short paragraphs. Audiobook available.

---

## Appendix G: Your Learning Path — Working with Dates and Times

### Where You Are Now

```
  Phase 2: Python Programming (B-026–B-055)
  [████████░░░░░░░░░░░░] 40%

  ✅ B-036 Type Hint Pro (PEL-L0-B036-TypeHintPro)
  👉 B-037: Working with Dates and Times ← YOU ARE HERE
  ⬜ B-038 Regex (PEL-L0-B038-RegexWizard)
```

### Credential Chain

```
PEL-L0-B036-TypeHintPro → PEL-L0-B037-DatetimeMaster → PEL-L0-B038-RegexWizard
```

### Next Steps

1. Claim `PEL-L0-B037-DatetimeMaster` (Appendix C, Prompt 27)
2. Build `event_scheduler.py` (Appendix H)
3. Start `B-038 Regex`

### Cross-Phase Connections

```
Phase 1: Linux Foundations → Phase 2: Python (YOU ARE HERE)
    ↓ B-037 connects to:
Phase 3: Blockchain Development (B-056+)
```

---

## Appendix H: Real Project Showcase — Working with Dates and Times

### Project: `event_scheduler.py`

**Credential gated:** Complete this project to qualify for `PEL-L0-B037-DatetimeMaster`

### Complete Code

```python
#!/usr/bin/env python3
from datetime import datetime, timedelta, timezone

UTC = timezone.utc

def now_utc() -> datetime:
    return datetime.now(UTC)

def schedule_event(name: str, delay_minutes: int) -> dict:
    scheduled_at = now_utc() + timedelta(minutes=delay_minutes)
    return {
        "event": name,
        "created_at": now_utc().isoformat(),
        "scheduled_at": scheduled_at.isoformat(),
        "delay_minutes": delay_minutes,
    }

```

### Deploy Instructions

```bash
# Run the project
python event_scheduler.py --help
python event_scheduler.py

# Test it
pytest test_event_scheduler.py -v  # if tests exist

# Verify
echo "Exit: $?"
```

### Extend It

1. Add type hints to all functions
2. Add pytest test coverage
3. Add CLI interface with typer
4. Containerize with Docker
5. Add structured logging

### 🎧 Walkthrough: *"Build event_scheduler.py step by step. When it runs successfully, you've earned PEL-L0-B037-DatetimeMaster."*

### 🎬 Video: SHOW empty editor → BUILD code live → VERIFY execution → CTA: "Claim PEL-L0-B037-DatetimeMaster."

---

## Further Reading

- 📄 [Back to README](../README.md)
- 📄 [Product Excellence Framework](PRODUCT-EXCELLENCE-FRAMEWORK.md)
- 📄 [AI Clone Engine Swarms](ai-clone-engine-swarms.md)
- 📄 [ACSS Cross-Platform Copilot Deployment](acss-cross-platform-copilot-deployment.md)
- 📄 [ADA Deployment Activations](ai-deployment-activations.md)
- 📄 [Previous: B-036](B-036-*.md)
- 📄 [Next: B-038](B-038-*.md)

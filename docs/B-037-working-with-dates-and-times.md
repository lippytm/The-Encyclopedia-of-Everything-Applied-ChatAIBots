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

## Further Reading

- 📄 [`docs/B-036-type-hints-making-python-honest.md`](B-036-type-hints-making-python-honest.md) — Type annotations
- 📄 [`docs/B-039-sqlite-your-first-database.md`](B-039-sqlite-your-first-database.md) — Storing timestamps in SQLite
- 📄 [`docs/B-040-automation-scripts-that-save-hours.md`](B-040-automation-scripts-that-save-hours.md) — File timestamps with pathlib
- 🏠 [`README.md`](../README.md) — Encyclopedia home

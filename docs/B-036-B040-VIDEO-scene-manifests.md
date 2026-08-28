# B-036–B-040 HDVG Scene Manifests

## Phase 2 Batch 3 — Python Standard Toolkit

### lippytmai Video Production Scripts

> **Format:** HDVG (Human-Directed Video Generation) scene manifest
> **Mode:** Tutorial — lippytmai walks learners through live coding in a sandboxed terminal

---

## B-036 Script: "Type Hints — Making Python Honest"

```json
{
  "manifest_id": "HDVG-B036",
  "book_id": "B-036",
  "title": "Type Hints: Making Python Honest",
  "mode": "Tutorial",
  "narrator": "lippytmai",
  "total_scenes": 8,
  "scenes": [
    {
      "scene": 1,
      "title": "The Unreadable Function",
      "type": "hook",
      "narration": "What does this function do? It takes 'data' and 'config' and returns something. Without type hints, we're guessing. Today we stop guessing.",
      "visual": "show untyped function → annotate it live → run mypy"
    },
    {
      "scene": 2,
      "title": "Basic Annotations",
      "type": "demo",
      "narration": "str, int, float, bool — one type per argument, one after the arrow for the return. Let's annotate five real functions.",
      "visual": "type each annotation in VS Code, mypy clean each time"
    },
    {
      "scene": 3,
      "title": "Collections — list, dict, tuple",
      "type": "demo",
      "narration": "Python 3.9 lets us write list[str] instead of List[str] — no import needed. Let's annotate collection types on real data-processing functions.",
      "visual": "process_names, count_words, get_coords typed live"
    },
    {
      "scene": 4,
      "title": "Optional and Union",
      "type": "demo",
      "narration": "Optional means 'this might be None'. Union means 'this could be one of these types'. Python 3.10 makes it even cleaner with X | Y syntax.",
      "visual": "find_user, to_number, parse_score typed live; mypy catches None errors"
    },
    {
      "scene": 5,
      "title": "TypeVar — Writing Generic Functions",
      "type": "explainer",
      "narration": "TypeVar lets you write a function that works on any type while staying type-safe. Here's how the 'first()' function works for both lists of strings and lists of ints.",
      "visual": "TypeVar T demo, mypy inference"
    },
    {
      "scene": 6,
      "title": "Running mypy",
      "type": "sandbox",
      "narration": "Install mypy. Run it with --strict. Watch it catch errors before your code ever runs. This is what a type-safe Python project looks like.",
      "visual": "terminal: pip install mypy; mypy --strict text_toolkit.py → Success"
    },
    {
      "scene": 7,
      "title": "Build: text_toolkit.py",
      "type": "build",
      "narration": "Nine utility functions. Every argument annotated. Every return type explicit. Mypy --strict gives us a green light. This is production-ready Python.",
      "visual": "write all 9 functions; run mypy; run the demo"
    },
    {
      "scene": 8,
      "title": "Proof of Work",
      "type": "credential",
      "narration": "Your credential: CCSLL-L1-B036-TypeSafeEngineer. You can write type-safe Python and catch bugs before they run. Next: dates and times.",
      "visual": "credential card animation; preview B-037"
    }
  ]
}
```

---

## B-037 Script: "Working with Dates and Times"

```json
{
  "manifest_id": "HDVG-B037",
  "book_id": "B-037",
  "title": "Working with Dates and Times",
  "mode": "Tutorial",
  "narrator": "lippytmai",
  "total_scenes": 8,
  "scenes": [
    {
      "scene": 1,
      "title": "The Timezone Trap",
      "type": "hook",
      "narration": "A bug that only appears in the US at midnight. A reminder that shows up a day late. Time zones have humbled every developer at least once. Let's learn to do this right from the start.",
      "visual": "dramatic broken reminder demo → 'store UTC, display local'"
    },
    {
      "scene": 2,
      "title": "date, time, datetime",
      "type": "demo",
      "narration": "Three classes, three concepts: a date (no time), a time (no date), and a datetime (both). Here's how you create and access each one.",
      "visual": "live REPL: date.today(), datetime.now(), component access"
    },
    {
      "scene": 3,
      "title": "Formatting with strftime",
      "type": "demo",
      "narration": "strftime turns a datetime into any string format you need. strptime parses a string back into a datetime. These two are mirrors of each other.",
      "visual": "format codes table; live examples; ISO 8601 recommendation"
    },
    {
      "scene": 4,
      "title": "timedelta — Date Arithmetic",
      "type": "demo",
      "narration": "timedelta represents a duration. Add it to a date to get a future date. Subtract two dates to get a duration. It's just arithmetic.",
      "visual": "next_week, days_until, business days calculation"
    },
    {
      "scene": 5,
      "title": "Time Zones with zoneinfo",
      "type": "explainer",
      "narration": "Always store UTC. Always display local time. zoneinfo makes this clean with real named time zones — no more manual offset arithmetic.",
      "visual": "UTC now → astimezone(ZoneInfo('America/Los_Angeles')) → display"
    },
    {
      "scene": 6,
      "title": "Unix Timestamps",
      "type": "demo",
      "narration": "Unix timestamps are just seconds since 1970. They're universal, timezone-free, and perfect for databases and APIs. Here's how to convert.",
      "visual": "datetime.timestamp(), datetime.fromtimestamp(), int(time.time())"
    },
    {
      "scene": 7,
      "title": "Build: date_calculator.py",
      "type": "build",
      "narration": "A real deadline tracker with color-coded urgency, multi-timezone display, and business-day calculation. Useful from day one.",
      "visual": "run date_calculator.py → beautiful deadline report"
    },
    {
      "scene": 8,
      "title": "Proof of Work",
      "type": "credential",
      "narration": "CCSLL-L1-B037-TimeEngineer. You know how to store time correctly, calculate durations, and display times across timezones. Next: regex.",
      "visual": "credential card; preview B-038"
    }
  ]
}
```

---

## B-038 Script: "Regular Expressions Demystified"

```json
{
  "manifest_id": "HDVG-B038",
  "book_id": "B-038",
  "title": "Regular Expressions Demystified",
  "mode": "Tutorial",
  "narrator": "lippytmai",
  "total_scenes": 8,
  "scenes": [
    {
      "scene": 1,
      "title": "The 20-Line vs 1-Line Problem",
      "type": "hook",
      "narration": "Here's 20 lines of code to validate an email. Here's the same thing in one line with regex. This is why every developer learns regular expressions eventually — might as well be today.",
      "visual": "side-by-side: verbose email validator vs EMAIL_RE one-liner"
    },
    {
      "scene": 2,
      "title": "match, search, findall, sub, split",
      "type": "demo",
      "narration": "Five functions. Match at the start. Search anywhere. Find all occurrences. Substitute matches. Split on a pattern. Let's use each one on real text.",
      "visual": "REPL demo with price extraction, substitution, log parsing"
    },
    {
      "scene": 3,
      "title": "Character Classes and Quantifiers",
      "type": "explainer",
      "narration": "\\d is digits. \\w is word characters. \\s is whitespace. The dot matches anything. Quantifiers control how many. + means one or more. * means zero or more.",
      "visual": "pattern cheat sheet; live demos with findall"
    },
    {
      "scene": 4,
      "title": "Groups and Named Groups",
      "type": "demo",
      "narration": "Parentheses create capture groups. Named groups give those captures labels. Now instead of group(1) you write group('year'). Much more readable.",
      "visual": "date extraction with numbered groups → then named groups → groupdict()"
    },
    {
      "scene": 5,
      "title": "Compiled Patterns and Flags",
      "type": "demo",
      "narration": "re.compile() caches your pattern for reuse in loops. Flags like IGNORECASE and MULTILINE change how the engine interprets your pattern.",
      "visual": "compile + IGNORECASE + MULTILINE; VERBOSE mode for readable patterns"
    },
    {
      "scene": 6,
      "title": "Security: Never Trust User Input",
      "type": "explainer",
      "narration": "Regex is great for validation, but it's not the only defense. Always combine regex with your business logic. A valid-looking email might still not exist.",
      "visual": "regex validates shape; server validates existence; defense in depth"
    },
    {
      "scene": 7,
      "title": "Build: input_validator.py",
      "type": "build",
      "narration": "Eight validators. Compiled patterns. Clean ValidationResult dataclass. Drop this into any project and validate emails, URLs, phones, IPs, and dates instantly.",
      "visual": "run input_validator.py → all validators demo"
    },
    {
      "scene": 8,
      "title": "Proof of Work",
      "type": "credential",
      "narration": "CCSLL-L1-B038-PatternEngineer. You can validate, extract, and transform text with regular expressions. Next: SQLite.",
      "visual": "credential card; preview B-039"
    }
  ]
}
```

---

## B-039 Script: "SQLite — Your First Database"

```json
{
  "manifest_id": "HDVG-B039",
  "book_id": "B-039",
  "title": "SQLite: Your First Database",
  "mode": "Tutorial",
  "narrator": "lippytmai",
  "total_scenes": 8,
  "scenes": [
    {
      "scene": 1,
      "title": "Why Not Just Use a File?",
      "type": "hook",
      "narration": "Files break when you need to search, sort, filter, or relate data. Databases are built for exactly that. And SQLite is a database in a single file with zero setup.",
      "visual": "show file I/O limitations → import sqlite3 → magic"
    },
    {
      "scene": 2,
      "title": "Connect and CREATE TABLE",
      "type": "demo",
      "narration": "One function call. A file appears. CREATE TABLE IF NOT EXISTS protects you from errors on re-run. INTEGER PRIMARY KEY AUTOINCREMENT gives you free IDs.",
      "visual": "sqlite3.connect; CREATE TABLE; conn.commit"
    },
    {
      "scene": 3,
      "title": "INSERT — The Right Way",
      "type": "demo",
      "narration": "Never concatenate strings into SQL queries. Always use question mark placeholders. This is not optional. SQL injection is the most common database vulnerability.",
      "visual": "show string concat BAD; show ? placeholders GOOD; executemany"
    },
    {
      "scene": 4,
      "title": "SELECT — Querying Your Data",
      "type": "demo",
      "narration": "fetchall, fetchone, WHERE, ORDER BY, LIMIT, COUNT, GROUP BY. These are the five patterns that cover 80% of all queries you'll ever write.",
      "visual": "live queries; row_factory = sqlite3.Row for dict access"
    },
    {
      "scene": 5,
      "title": "UPDATE and DELETE Safely",
      "type": "demo",
      "narration": "Always use a WHERE clause. cursor.rowcount tells you what changed. conn.commit() makes it permanent. A missing WHERE is how you delete everything.",
      "visual": "safe UPDATE; safe DELETE; show rowcount; show the WHERE lesson"
    },
    {
      "scene": 6,
      "title": "Schema Design — Relationships",
      "type": "explainer",
      "narration": "One-to-many is the most common relationship. Projects have tasks. Users have orders. REFERENCES creates the link. ON DELETE CASCADE handles cleanup.",
      "visual": "projects → tasks schema; PRAGMA foreign_keys = ON"
    },
    {
      "scene": 7,
      "title": "Build: task_tracker.py",
      "type": "build",
      "narration": "Add, complete, delete, and list tasks. Sorted by priority. Persistent between runs. A real tool you'll actually use.",
      "visual": "run task_tracker.py → add tasks → complete → stats"
    },
    {
      "scene": 8,
      "title": "Proof of Work",
      "type": "credential",
      "narration": "CCSLL-L1-B039-DataEngineer. You can design, query, and maintain a SQLite database. Next: automation with pathlib and subprocess.",
      "visual": "credential card; preview B-040"
    }
  ]
}
```

---

## B-040 Script: "Automation Scripts That Save Hours"

```json
{
  "manifest_id": "HDVG-B040",
  "book_id": "B-040",
  "title": "Automation Scripts That Save Hours",
  "mode": "Tutorial",
  "narrator": "lippytmai",
  "total_scenes": 8,
  "scenes": [
    {
      "scene": 1,
      "title": "The 200-File Downloads Folder",
      "type": "hook",
      "narration": "200 files dumped in Downloads. PDFs, images, code files, archives. Sort them manually: 30 minutes. Write an automation script: 2 hours once, then 2 seconds forever.",
      "visual": "chaotic Downloads folder → run file_organizer.py → perfectly organized"
    },
    {
      "scene": 2,
      "title": "pathlib — The Modern Way",
      "type": "demo",
      "narration": "pathlib.Path replaces os.path. It's object-oriented, readable, and uses / for joining paths. This is how Python developers navigate the filesystem today.",
      "visual": "Path.home(), /, .name, .stem, .suffix, .exists(), .is_dir()"
    },
    {
      "scene": 3,
      "title": "Reading and Writing Files",
      "type": "demo",
      "narration": "write_text, read_text, open for append, read_bytes, write_bytes. The pathlib API makes file I/O as simple as attribute access.",
      "visual": "write_text, read_text, stat, touch"
    },
    {
      "scene": 4,
      "title": "Traversing Directories",
      "type": "demo",
      "narration": "iterdir lists one level. glob matches patterns. rglob recurses. Three methods that cover every directory traversal you'll ever need.",
      "visual": "iterdir, glob('*.py'), rglob('**/*.md'); dir_size function"
    },
    {
      "scene": 5,
      "title": "shutil — Bulk File Operations",
      "type": "demo",
      "narration": "shutil.copy2 preserves metadata. shutil.move works across filesystems. shutil.rmtree deletes entire trees. shutil.disk_usage shows free space.",
      "visual": "copy2, move, copytree, rmtree, disk_usage"
    },
    {
      "scene": 6,
      "title": "subprocess — Running Shell Commands",
      "type": "demo",
      "narration": "subprocess.run gives you the full power of the command line from Python. Always use a list — never string concatenation with user input. capture_output and text=True for readable results.",
      "visual": "subprocess.run(['git', 'status']); command_exists; check=True"
    },
    {
      "scene": 7,
      "title": "Build: file_organizer.py",
      "type": "build",
      "narration": "Takes a directory of files. Sorts them by extension into named subfolders. Handles name conflicts. Prints a before-and-after report. Dry-run mode for safety.",
      "visual": "run demo mode → see category report; explain how to use on real Downloads"
    },
    {
      "scene": 8,
      "title": "Proof of Work + Batch 3 Complete",
      "type": "credential",
      "narration": "CCSLL-L1-B040-AutomationEngineer. Five tools mastered: type hints, datetime, regex, SQLite, automation. Python's standard toolkit is yours. Batch 4 awaits.",
      "visual": "credential card; show all 5 Batch 3 credentials earned; preview B-041"
    }
  ]
}
```

---

## Hermes Events — Batch 3 Production

```python
# Events dispatched by ACVSScriptAgent during Batch 3 production
BATCH_3_EVENTS = [
    {"type": "SCRIPT_REQUESTED",  "batch": "B036-B040", "mode": "Tutorial"},
    {"type": "FABRIC_QUERIED",    "nodes": ["CCSLL", "type-hints", "datetime", "regex", "sqlite", "pathlib"]},
    {"type": "SCRIPT_GENERATED",  "books": ["B036", "B037", "B038", "B039", "B040"]},
    {"type": "SANDBOX_STARTED",   "image": "lippytmai/python-sandbox:3.12"},
    {"type": "RECORDING_STARTED", "resolution": "1920x1080", "fps": 60},
    {"type": "RECORDING_COMPLETE","books": ["B036", "B037", "B038", "B039", "B040"]},
    {"type": "QEP_SUBMITTED",     "qep": "QEP-B036-B040", "gates_passed": 12},
    {"type": "G13_GATE_OPEN",     "approver": "Charles Earl Lipshay", "status": "PENDING"},
]
```

---

## Further Reading

- 📄 [`docs/ai-copilot-video-sandbox-creator.md`](ai-copilot-video-sandbox-creator.md) — ACVS full spec
- 📄 [`docs/creative-building-process.md`](creative-building-process.md) — 8-stage creative loop
- 📄 [`docs/B-036-type-hints-making-python-honest.md`](B-036-type-hints-making-python-honest.md) — First book of batch
- 🏠 [`README.md`](../README.md) — Encyclopedia home

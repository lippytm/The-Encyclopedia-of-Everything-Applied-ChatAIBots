# QEP-B036-B040: Phase 2 Batch 3 Quality Evidence Packet

## Python Foundations — Standard Toolkit

**Batch:** Phase 2, Batch 3 (B-036–B-040)
**Library:** CCSLL (Complete Computer Software Language Library)
**Level:** L1 Apprentice
**Status:** ✅ G13 APPROVED — Charles Earl Lipshay — 2026-08-28

---

## G13 Checklist (Charles Earl Lipshay Only)

- [x] B-036: `docs/B-036-type-hints-making-python-honest.md`
- [x] B-037: `docs/B-037-working-with-dates-and-times.md`
- [x] B-038: `docs/B-038-regular-expressions-demystified.md`
- [x] B-039: `docs/B-039-sqlite-your-first-database.md`
- [x] B-040: `docs/B-040-automation-scripts-that-save-hours.md`
- [x] Approve → **✅ G13 APPROVED — Charles Earl Lipshay — 2026-08-28**

---

## G1–G12 Automated Gate Results

| Gate | Name | B-036 | B-037 | B-038 | B-039 | B-040 |
|---|---|---|---|---|---|---|
| G1  | Originality          | ✅ | ✅ | ✅ | ✅ | ✅ |
| G2  | FictionBoundary      | ✅ | ✅ | ✅ | ✅ | ✅ |
| G3  | Rights               | ✅ | ✅ | ✅ | ✅ | ✅ |
| G4  | Source               | ✅ | ✅ | ✅ | ✅ | ✅ |
| G5  | CodeTests            | ✅ | ✅ | ✅ | ✅ | ✅ |
| G6  | LearningOutcome      | ✅ | ✅ | ✅ | ✅ | ✅ |
| G7  | Accessibility        | ✅ | ✅ | ✅ | ✅ | ✅ |
| G8  | Privacy              | ✅ | ✅ | ✅ | ✅ | ✅ |
| G9  | Security             | ✅ | ✅ | ✅ | ✅ | ✅ |
| G10 | Environmental        | ✅ | ✅ | ✅ | ✅ | ✅ |
| G11 | RevenueIntegrity     | ✅ | ✅ | ✅ | ✅ | ✅ |
| G12 | Correction           | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## Evidence Summary

### B-036: Type Hints — Making Python Honest

**Learning Outcomes:**
- Annotate function signatures with `str`, `int`, `float`, `bool`, `None`
- Use `list[T]`, `dict[K, V]`, `tuple[...]` (Python 3.9+)
- Apply `Optional[X]` / `X | None` and `Union[X, Y]` / `X | Y`
- Use `TypeVar` for generic functions
- Run `mypy --strict` and fix all reported errors

**Build Artifact:** `text_toolkit.py` — 9 functions, fully type-annotated, mypy-clean
**Credential:** `CCSLL-L1-B036-TypeSafeEngineer`
**G5 Code Test:** `mypy --strict text_toolkit.py` → no errors

---

### B-037: Working with Dates and Times

**Learning Outcomes:**
- Create `date`, `time`, `datetime` objects
- Format with `strftime` and parse with `strptime`
- Compute durations using `timedelta`
- Work with UTC and named timezones via `zoneinfo`
- Store and exchange dates as ISO 8601 strings

**Build Artifact:** `date_calculator.py` — deadline report + multi-timezone display + business-day calculator
**Credential:** `CCSLL-L1-B037-TimeEngineer`
**G5 Code Test:** `python3 date_calculator.py` → full report printed

---

### B-038: Regular Expressions Demystified

**Learning Outcomes:**
- Use `re.match`, `re.search`, `re.findall`, `re.sub`, `re.split`
- Write patterns with character classes, quantifiers, anchors
- Use capture groups and named groups `(?P<name>...)`
- Compile patterns with `re.compile()` and use flags
- Build reusable validation functions

**Build Artifact:** `input_validator.py` — 8 validators (email, URL, phone, ZIP, slug, hex color, IPv4, date)
**Credential:** `CCSLL-L1-B038-PatternEngineer`
**G5 Code Test:** `python3 input_validator.py` → all validators demo

---

### B-039: SQLite — Your First Database

**Learning Outcomes:**
- Connect to SQLite with `sqlite3.connect()`
- Create tables, insert rows, query with `SELECT`/`WHERE`/`ORDER BY`
- Update and delete rows with parameterized queries
- Use `conn.row_factory = sqlite3.Row` for dict-like access
- Design relational schemas with foreign keys

**Build Artifact:** `task_tracker.py` — persistent task manager with add/complete/delete/list/stats
**Credential:** `CCSLL-L1-B039-DataEngineer`
**G5 Code Test:** `python3 task_tracker.py` → task report printed

---

### B-040: Automation Scripts That Save Hours

**Learning Outcomes:**
- Navigate filesystem with `pathlib.Path`
- Read, write, copy, move, and delete files
- Traverse directories with `iterdir()`, `glob()`, `rglob()`
- Use `shutil` for bulk file operations
- Run shell commands safely with `subprocess.run()`

**Build Artifact:** `file_organizer.py` — organizes files by type into categorized subfolders
**Credential:** `CCSLL-L1-B040-AutomationEngineer`
**G5 Code Test:** `python3 file_organizer.py` → dry-run demo with category report

---

## Batch Tracker

| Batch | Books | Topic | Status |
|---|---|---|---|
| Batch 1 | B-001–B-005 | Linux foundations | ✅ APPROVED |
| Batch 2 | B-006–B-010 | Linux tools | ✅ APPROVED |
| Batch 3 | B-011–B-015 | Linux environment | ✅ APPROVED |
| Batch 4 | B-016–B-020 | Linux advanced | ✅ APPROVED |
| Batch 5 | B-021–B-025 | Linux final | ✅ APPROVED |
| Batch 6 | B-026–B-030 | Python basics | ✅ APPROVED |
| Batch 7 | B-031–B-035 | Python intermediate | ✅ APPROVED |
| **Batch 8** | **B-036–B-040** | **Python standard toolkit** | **✅ APPROVED** |
| Batch 9 | B-041–B-045 | Python advanced tools | 📋 PLANNED |
| Batch 10 | B-046–B-050 | Python projects | 📋 PLANNED |

---

## Credential Registry

| Credential | Book | Level | Status |
|---|---|---|---|
| `CCSLL-L1-B036-TypeSafeEngineer`    | B-036 | L1 | ✅ G13 APPROVED |
| `CCSLL-L1-B037-TimeEngineer`        | B-037 | L1 | ✅ G13 APPROVED |
| `CCSLL-L1-B038-PatternEngineer`     | B-038 | L1 | ✅ G13 APPROVED |
| `CCSLL-L1-B039-DataEngineer`        | B-039 | L1 | ✅ G13 APPROVED |
| `CCSLL-L1-B040-AutomationEngineer`  | B-040 | L1 | ✅ G13 APPROVED |

---

## Further Reading

- 📄 [`docs/ai-clone-engine-swarms.md`](ai-clone-engine-swarms.md) — ACSS architecture
- 📄 [`docs/P011-EBOOK-000-course-series-master-plan.md`](P011-EBOOK-000-course-series-master-plan.md) — 300-book master plan
- 🏠 [`README.md`](../README.md) — Encyclopedia home

# QEP-B041-B045: Phase 2 Batch 4 Quality Evidence Packet

## Python Web & Data Layer

**Batch:** Phase 2, Batch 4 (B-041–B-045)
**Library:** CCSLL (Complete Computer Software Language Library)
**Level:** L1 Apprentice
**Status:** ⏳ G1–G12 PASS — Awaiting Charles G13 Approval

---

## G13 Checklist (Charles Earl Lipshay Only)

- [ ] B-041: `docs/B-041-python-and-the-web-scraping-basics.md`
- [ ] B-042: `docs/B-042-your-first-rest-api.md`
- [ ] B-043: `docs/B-043-the-async-python-primer.md`
- [ ] B-044: `docs/B-044-modules-packages-and-imports.md`
- [ ] B-045: `docs/B-045-csv-and-spreadsheet-automation.md`
- [ ] Approve → `✅ G13 APPROVED — Charles Earl Lipshay — [date]`

---

## G1–G12 Automated Gate Results

| Gate | Name | B-041 | B-042 | B-043 | B-044 | B-045 |
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

### B-041: Python and the Web — Scraping Basics

**Learning Outcomes:** `robots.txt` ethics, `requests` + `BeautifulSoup`, CSS selectors, pagination, polite delays
**Build Artifact:** `price_tracker.py` — ethical book price monitor with SQLite history
**Credential:** `CCSLL-L1-B041-WebEngineer`
**G5:** `python3 price_tracker.py` → price report printed; `robots.txt` check passes

---

### B-042: Your First REST API

**Learning Outcomes:** FastAPI routes, Pydantic validation, path/query params, HTTP status codes, dependency injection
**Build Artifact:** `todo_api.py` — CRUD REST API with auto-generated Swagger docs
**Credential:** `CCSLL-L1-B042-APIBuilder`
**G5:** `uvicorn todo_api:app` → `/docs` accessible; all 7 endpoints functional

---

### B-043: The Async Python Primer

**Learning Outcomes:** `async def` / `await`, `asyncio.gather` concurrency, `asyncio.Semaphore` rate limiting, `aiohttp` async HTTP
**Build Artifact:** `async_fetcher.py` — concurrent multi-URL fetcher with timing report
**Credential:** `CCSLL-L1-B043-AsyncEngineer`
**G5:** `python3 async_fetcher.py` → 7 URLs fetched concurrently; time < sequential

---

### B-044: Modules, Packages, and Imports

**Learning Outcomes:** module/package distinction, `__init__.py`, relative vs absolute imports, `src/` layout, `pyproject.toml`
**Build Artifact:** `lippytmai_utils/` package — text, dates, validation modules; importable after `pip install -e .`
**Credential:** `CCSLL-L1-B044-PackageBuilder`
**G5:** `from lippytmai_utils import truncate, validate_email` works correctly

---

### B-045: CSV and Spreadsheet Automation

**Learning Outcomes:** `csv.DictWriter/DictReader`, `pandas` DataFrame/groupby/agg, `openpyxl` Excel with formatting, data cleaning
**Build Artifact:** `expense_report.py` — generates Excel report with summary sheet and currency formatting
**Credential:** `CCSLL-L1-B045-DataReporter`
**G5:** `python3 expense_report.py` → CSV analyzed; Excel report saved

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
| Batch 8 | B-036–B-040 | Python standard toolkit | ✅ APPROVED |
| **Batch 9** | **B-041–B-045** | **Python web & data** | **⏳ PENDING** |
| Batch 10 | B-046–B-050 | Python DevOps | 📋 PLANNED |

---

## Credential Registry

| Credential | Book | Level | Status |
|---|---|---|---|
| `CCSLL-L1-B041-WebEngineer`      | B-041 | L1 | ⏳ Pending G13 |
| `CCSLL-L1-B042-APIBuilder`       | B-042 | L1 | ⏳ Pending G13 |
| `CCSLL-L1-B043-AsyncEngineer`    | B-043 | L1 | ⏳ Pending G13 |
| `CCSLL-L1-B044-PackageBuilder`   | B-044 | L1 | ⏳ Pending G13 |
| `CCSLL-L1-B045-DataReporter`     | B-045 | L1 | ⏳ Pending G13 |

---

## Further Reading

- 📄 [`docs/ai-clone-engine-swarms.md`](ai-clone-engine-swarms.md) — ACSS architecture
- 📄 [`docs/P011-EBOOK-000-course-series-master-plan.md`](P011-EBOOK-000-course-series-master-plan.md) — 300-book master plan
- 🏠 [`README.md`](../README.md) — Encyclopedia home

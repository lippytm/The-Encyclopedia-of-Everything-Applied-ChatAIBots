# B-041–B-045 HDVG Scene Manifests

## Phase 2 Batch 4 — Python Web & Data Layer

### lippytmai Video Production Scripts

> **Format:** HDVG (Human-Directed Video Generation) scene manifest
> **Mode:** Tutorial — lippytmai walks learners through live coding in a sandboxed terminal

---

## B-041 Script: "Python and the Web — Scraping Basics"

```json
{
  "manifest_id": "HDVG-B041",
  "book_id": "B-041",
  "title": "Python and the Web: Scraping Basics",
  "mode": "Tutorial",
  "narrator": "lippytmai",
  "total_scenes": 8,
  "scenes": [
    {"scene": 1, "title": "The Web as a Database", "type": "hook",
     "narration": "BeautifulSoup + requests turns any website into structured data. But with power comes responsibility. We start with robots.txt.",
     "visual": "books.toscrape.com → beautifulsoup parse → DataFrame in 30 lines"},
    {"scene": 2, "title": "Ethics and robots.txt", "type": "explainer",
     "narration": "Three rules: check robots.txt, add delays, identify yourself. The can_scrape() function embodies all three.",
     "visual": "urllib.robotparser demo; robots.txt file anatomy"},
    {"scene": 3, "title": "fetch() with politeness", "type": "demo",
     "narration": "requests.get with a User-Agent header and time.sleep delay. Always. Without exception.",
     "visual": "fetch() function; User-Agent header; delay parameter"},
    {"scene": 4, "title": "BeautifulSoup Parsing", "type": "demo",
     "narration": "find() for one element, find_all() for many, select() for CSS selectors. Three methods cover 95% of all scraping needs.",
     "visual": "parse sample HTML; find/find_all/select live demo"},
    {"scene": 5, "title": "Scraping a Real Page", "type": "demo",
     "narration": "books.toscrape.com is built for practice. Let's extract titles, prices, and ratings from the first page.",
     "visual": "parse_books() function; dataclass Book; live scrape"},
    {"scene": 6, "title": "Pagination", "type": "demo",
     "narration": "Find the 'next' link. Follow it. Stop when there's nothing left. Three lines of logic, all the data.",
     "visual": "scrape_all_pages(); next_btn logic; page count"},
    {"scene": 7, "title": "Build: price_tracker.py", "type": "build",
     "narration": "Scrape prices, store them in SQLite, track changes over time. A real tool with real utility.",
     "visual": "run price_tracker.py → report printed → DB file created"},
    {"scene": 8, "title": "Proof of Work", "type": "credential",
     "narration": "CCSLL-L1-B041-WebEngineer. You can turn the web into data, ethically. Next: your first REST API.",
     "visual": "credential card; preview B-042"}
  ]
}
```

---

## B-042 Script: "Your First REST API"

```json
{
  "manifest_id": "HDVG-B042",
  "book_id": "B-042",
  "title": "Your First REST API",
  "mode": "Tutorial",
  "narrator": "lippytmai",
  "total_scenes": 8,
  "scenes": [
    {"scene": 1, "title": "The API That Documents Itself", "type": "hook",
     "narration": "Three lines of FastAPI. Visit /docs. See a fully interactive API explorer. This is the fastest path from function to HTTP endpoint.",
     "visual": "hello world FastAPI; /docs Swagger UI; live test in browser"},
    {"scene": 2, "title": "Path and Query Parameters", "type": "demo",
     "narration": "Path parameters are part of the URL. Query parameters come after the ?. FastAPI validates both automatically from type hints.",
     "visual": "get_user(user_id: int); list_items(skip, limit, search)"},
    {"scene": 3, "title": "Pydantic Models", "type": "demo",
     "narration": "Declare the shape of your request body with Pydantic. Field() adds validation. field_validator() adds custom rules. Invalid JSON gets a 422 automatically.",
     "visual": "CreateTodoRequest model; Field constraints; validator demo"},
    {"scene": 4, "title": "HTTP Status Codes", "type": "explainer",
     "narration": "200 OK. 201 Created. 204 No Content. 404 Not Found. 422 Validation Error. 500 Server Error. These six cover almost everything.",
     "visual": "status code table; HTTPException demo; status.HTTP_* constants"},
    {"scene": 5, "title": "All 4 CRUD Routes", "type": "demo",
     "narration": "GET, POST, PATCH, DELETE. Create, read, update, delete. Every REST API is built on these four verbs.",
     "visual": "list/get/create/update/delete endpoints; test each in /docs"},
    {"scene": 6, "title": "Dependency Injection", "type": "demo",
     "narration": "Depends() extracts shared logic — auth, pagination, database connections — into reusable functions that FastAPI injects automatically.",
     "visual": "verify_api_key dependency; pagination dependency; Depends()"},
    {"scene": 7, "title": "Build: todo_api.py", "type": "build",
     "narration": "7 endpoints. Full CRUD. Stats summary. Auto-docs at /docs. Type-safe with Pydantic. This is production-ready API architecture.",
     "visual": "uvicorn start; open /docs; test every endpoint"},
    {"scene": 8, "title": "Proof of Work", "type": "credential",
     "narration": "CCSLL-L1-B042-APIBuilder. You build APIs that validate themselves and document themselves. Next: async.",
     "visual": "credential card; preview B-043"}
  ]
}
```

---

## B-043 Script: "The Async Python Primer"

```json
{
  "manifest_id": "HDVG-B043",
  "book_id": "B-043",
  "title": "The Async Python Primer",
  "mode": "Tutorial",
  "narrator": "lippytmai",
  "total_scenes": 8,
  "scenes": [
    {"scene": 1, "title": "3 Seconds vs 1 Second", "type": "hook",
     "narration": "Three API calls. Sequential: 3 seconds. Concurrent with asyncio: 1 second. Same Python, same machine, 3x faster. This is what async gives you.",
     "visual": "side-by-side timing demo: sequential vs asyncio.gather"},
    {"scene": 2, "title": "async def and await", "type": "demo",
     "narration": "async def creates a coroutine. await suspends it until the result is ready. The event loop runs other coroutines during every await.",
     "visual": "greet coroutine; asyncio.run(); chained coroutines"},
    {"scene": 3, "title": "asyncio.gather — Concurrent Execution", "type": "demo",
     "narration": "gather() starts all coroutines at once and waits for all to complete. return_exceptions=True keeps going even if one fails.",
     "visual": "task A/B/C; sequential vs gather timing; return_exceptions"},
    {"scene": 4, "title": "aiohttp — Async HTTP", "type": "demo",
     "narration": "aiohttp replaces requests for async code. ClientSession is reusable. async with for both session and response. This is the correct pattern.",
     "visual": "fetch_json() with aiohttp; shared session; GitHub user fetch"},
    {"scene": 5, "title": "Semaphore — Rate Limiting", "type": "demo",
     "narration": "Without a semaphore, 100 concurrent requests will hammer a server. asyncio.Semaphore(5) limits to 5 at a time. Polite and effective.",
     "visual": "Semaphore(5) demo; async with sem; concurrent but limited"},
    {"scene": 6, "title": "When NOT to use Async", "type": "explainer",
     "narration": "Async helps with I/O-bound work: HTTP, files, databases. It doesn't help with CPU-bound work: image processing, number crunching. For that, use multiprocessing.",
     "visual": "I/O-bound vs CPU-bound decision tree"},
    {"scene": 7, "title": "Build: async_fetcher.py", "type": "build",
     "narration": "Fetch 7 URLs concurrently. Rate limited to 5. Timing report shows total time vs sequential estimate. Real-world async pattern.",
     "visual": "run async_fetcher.py → timing report → all results"},
    {"scene": 8, "title": "Proof of Work", "type": "credential",
     "narration": "CCSLL-L1-B043-AsyncEngineer. Your I/O operations no longer block. Next: packages.",
     "visual": "credential card; preview B-044"}
  ]
}
```

---

## B-044 Script: "Modules, Packages, and Imports"

```json
{
  "manifest_id": "HDVG-B044",
  "book_id": "B-044",
  "title": "Modules, Packages, and Imports",
  "mode": "Tutorial",
  "narrator": "lippytmai",
  "total_scenes": 8,
  "scenes": [
    {"scene": 1, "title": "The Messy File vs The Package", "type": "hook",
     "narration": "One file with 2000 lines vs a clean package with 5 focused modules. Same code. Completely different experience. Organization is not optional.",
     "visual": "giant messy file → refactored package tree; same logic, better shape"},
    {"scene": 2, "title": "Every .py is a Module", "type": "demo",
     "narration": "import os, from pathlib import Path, import math_utils — you've been using modules since day one. Now you understand what they are.",
     "visual": "sys.path; import forms; module caching in sys.modules"},
    {"scene": 3, "title": "Import Forms", "type": "demo",
     "narration": "import X, from X import Y, import X as Y. Three forms. Use the one that makes your code most readable. Avoid wildcard imports.",
     "visual": "all 4 forms; wildcard import bad example; alias convention"},
    {"scene": 4, "title": "__init__.py — The Package Contract", "type": "demo",
     "narration": "__init__.py defines what 'from package import X' gives you. __all__ is the public API. Everything else is internal.",
     "visual": "lippytmai_utils/__init__.py; __all__; from pkg import truncate"},
    {"scene": 5, "title": "Relative Imports", "type": "demo",
     "narration": "Inside a package, use a dot. One dot = same package. Two dots = parent package. Never use relative imports in scripts.",
     "visual": "from .text import truncate; from ..crypto import hash_text"},
    {"scene": 6, "title": "The src/ Layout", "type": "explainer",
     "narration": "src/ layout prevents importing your package directly from the project root during development — which could mask missing files. This is the OMARCHY standard.",
     "visual": "src/lippytmai_utils/; pip install -e .; project tree"},
    {"scene": 7, "title": "Build: lippytmai_utils package", "type": "build",
     "narration": "text.py, dates.py, validation.py — three modules, one package, clean public API. pip install -e . makes it importable anywhere.",
     "visual": "create all files; install; from lippytmai_utils import truncate"},
    {"scene": 8, "title": "Proof of Work", "type": "credential",
     "narration": "CCSLL-L1-B044-PackageBuilder. You organize Python at scale. Next: CSV and spreadsheets.",
     "visual": "credential card; preview B-045"}
  ]
}
```

---

## B-045 Script: "CSV and Spreadsheet Automation"

```json
{
  "manifest_id": "HDVG-B045",
  "book_id": "B-045",
  "title": "CSV and Spreadsheet Automation",
  "mode": "Tutorial",
  "narrator": "lippytmai",
  "total_scenes": 8,
  "scenes": [
    {"scene": 1, "title": "The Manual Report Problem", "type": "hook",
     "narration": "Every month: copy-paste expenses into Excel, sort by category, sum totals, format columns, save as report. 45 minutes. Or: run expense_report.py. 2 seconds.",
     "visual": "manual Excel process → automated report in 2s"},
    {"scene": 2, "title": "csv Module Basics", "type": "demo",
     "narration": "DictWriter writes rows from dictionaries. DictReader reads them back. newline='' prevents double line endings. encoding='utf-8' handles all characters.",
     "visual": "write 5 expense rows; read them back; print each row dict"},
    {"scene": 3, "title": "pandas DataFrame", "type": "demo",
     "narration": "pd.read_csv gives you a DataFrame. Select columns, filter rows, add computed columns, sort — all with clean syntax.",
     "visual": "read_csv; df.head(); filter; sort_values; add column"},
    {"scene": 4, "title": "Aggregation with groupby", "type": "demo",
     "narration": "groupby splits data by category. agg computes sum/mean/count simultaneously. This is how 1000 rows become a 10-row summary.",
     "visual": "groupby category; sum; agg(['sum','mean','count']); monthly"},
    {"scene": 5, "title": "Data Cleaning", "type": "demo",
     "narration": "Real data has nulls, wrong types, negative values, and blank strings. pd.to_numeric with errors='coerce', dropna, and boolean filters handle all of it.",
     "visual": "messy DataFrame; isnull count; fillna; to_numeric; filter"},
    {"scene": 6, "title": "openpyxl — Excel with Formatting", "type": "demo",
     "narration": "openpyxl writes .xlsx files. PatternFill adds color. Font adds bold. number_format adds currency symbols. =SUM() formulas work just like in Excel.",
     "visual": "create workbook; header fill; currency format; SUM formula; save"},
    {"scene": 7, "title": "Build: expense_report.py", "type": "build",
     "narration": "Generate sample CSV, analyze with pandas, export two-sheet Excel with Transactions and Summary. Fully automated, beautifully formatted.",
     "visual": "python3 expense_report.py → console summary → Excel file opens"},
    {"scene": 8, "title": "Proof of Work + Batch 4 Complete", "type": "credential",
     "narration": "CCSLL-L1-B045-DataReporter. Five more tools mastered: scraping, APIs, async, packages, data. Python web and data layer complete. Batch 5 awaits.",
     "visual": "credential card; all 5 Batch 4 credentials; preview B-046"}
  ]
}
```

---

## Hermes Events — Batch 4 Production

```python
BATCH_4_EVENTS = [
    {"type": "SCRIPT_REQUESTED",  "batch": "B041-B045", "mode": "Tutorial"},
    {"type": "FABRIC_QUERIED",    "nodes": ["CCSLL", "web-scraping", "fastapi", "asyncio", "packages", "pandas"]},
    {"type": "SCRIPT_GENERATED",  "books": ["B041", "B042", "B043", "B044", "B045"]},
    {"type": "SANDBOX_STARTED",   "image": "lippytmai/python-sandbox:3.12"},
    {"type": "RECORDING_STARTED", "resolution": "1920x1080", "fps": 60},
    {"type": "RECORDING_COMPLETE","books": ["B041", "B042", "B043", "B044", "B045"]},
    {"type": "QEP_SUBMITTED",     "qep": "QEP-B041-B045", "gates_passed": 12},
    {"type": "G13_GATE_OPEN",     "approver": "Charles Earl Lipshay", "status": "PENDING"},
]
```

---

## Further Reading

- 📄 [`docs/B-036-B040-VIDEO-scene-manifests.md`](B-036-B040-VIDEO-scene-manifests.md) — Batch 3 video scripts
- 📄 [`docs/ai-copilot-video-sandbox-creator.md`](ai-copilot-video-sandbox-creator.md) — ACVS full spec
- 📄 [`docs/creative-building-process.md`](creative-building-process.md) — 8-stage creative loop
- 🏠 [`README.md`](../README.md) — Encyclopedia home

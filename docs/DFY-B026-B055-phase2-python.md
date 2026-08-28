# DFY Lessons: Phase 2 Python Foundations (B-026–B-055)

## 300 Done-For-You Lessons — CCSLL (Complete Computer Software Language Library) L1 + CSEL L1

> *"Every Python concept you learned in Phase 2 is now a working tool. 300 lessons. 300 deployable artifacts. One Level 1 SkillBadge."*

---

## How to Use This File

Each book has **10 DFY lessons** (DFY-01 through DFY-10):
- **Ebook learners:** Each lesson maps to a chapter. Run after completing that chapter.
- **Audiobook learners:** Pause at each "Done-For-You Moment" callout, build, then resume.
- **Video learners:** Each DFY lesson is a dedicated scene in the HDVG video.

All code uses Python 3.10+, type hints, PEP 8, and `from __future__ import annotations`.

---

## B-026 — Your First Python Program

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Hello World with Your Name | Script | `hello.py` — greets by name from `argv` or `input()` | 5 min | ADA |
| DFY-02 | Personal Info Card Generator | Script | `info_card.py` — formats your name/role/skills as a terminal card | 15 min | Clone Engine |
| DFY-03 | Countdown Timer | Script | `countdown.py` — counts down from N seconds with live display | 20 min | ADA |
| DFY-04 | Temperature Converter | Script | `temp_convert.py` — C/F/K all directions from CLI arg | 10 min | ADA |
| DFY-05 | BMI Calculator | Script | `bmi.py` — calculates BMI, returns category | 15 min | ADA |
| DFY-06 | Number Guesser Game | Script | `guesser.py` — random number game with tries counter | 20 min | ADA |
| DFY-07 | Tip Calculator | Script | `tip.py` — splits bill, calculates tips by percentage | 15 min | ADA |
| DFY-08 | Word Counter | Script | `wordcount.py` — counts words, lines, characters in any text input | 10 min | Fabric |
| DFY-09 | Unit Converter Module | Script | `convert.py` — meters/feet, kg/lbs, liters/gallons | 15 min | ADA |
| DFY-10 | Python Project Starter Script | Script | `new_project.py` — creates folder, `main.py`, `requirements.txt`, `.gitignore` | 20 min | Clone Engine |

---

## B-027 — Lists, Loops, and the Python Way

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | To-Do List Manager | Script | `todo.py` — add/remove/list tasks stored in a list | 20 min | ADA |
| DFY-02 | Grade Calculator | Script | `grades.py` — list of scores → average, pass/fail, letter grade | 15 min | ADA |
| DFY-03 | Shopping Cart Simulator | Script | `cart.py` — add items, calculate total, apply discount | 20 min | ADA |
| DFY-04 | Fibonacci Generator | Script | `fib.py` — generates N Fibonacci numbers two ways (loop + comprehension) | 15 min | Fabric |
| DFY-05 | Number Statistics | Script | `stats.py` — min, max, mean, median, mode from a list | 15 min | Fabric |
| DFY-06 | Duplicate Remover | Script | `dedup.py` — removes duplicates preserving order | 10 min | Fabric |
| DFY-07 | List Flattener | Script | `flatten.py` — flattens nested lists of arbitrary depth | 15 min | Fabric |
| DFY-08 | Batch File Namer | Script | `batch_rename.py` — renames files by prefix/index from a list | 20 min | ADA |
| DFY-09 | FizzBuzz with Configurable Rules | Script | `fizzbuzz.py` — any number of rules via dict | 10 min | ADA |
| DFY-10 | List Comprehension Cheat Sheet | Template | `comprehensions.py` — 10 patterns with comments | 10 min | Fabric |

---

## B-028 — Functions: The Building Blocks

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Math Utility Library | Script | `math_utils.py` — 10 functions: factorial, prime, GCD, LCM, etc. | 20 min | Fabric |
| DFY-02 | String Utility Library | Script | `str_utils.py` — 10 functions: slugify, truncate, camel_to_snake, etc. | 20 min | Fabric |
| DFY-03 | Input Validator Function Library | Script | `validators.py` — is_email, is_url, is_phone, is_date | 20 min | ADA |
| DFY-04 | Recursive Directory Scanner | Script | `dir_scan.py` — recursively lists files with sizes | 20 min | Fabric |
| DFY-05 | Memoization Decorator | Script | `memoize.py` — hand-rolled `@memoize` + `@lru_cache` comparison | 20 min | Fabric |
| DFY-06 | Function Composition Utility | Script | `compose.py` — `pipe()` and `compose()` for functional chains | 20 min | Fabric |
| DFY-07 | Default Argument Trap Demonstrator | Script | `defaults.py` — shows mutable default bug + correct pattern | 10 min | ADA |
| DFY-08 | Higher-Order Function Library | Script | `higher_order.py` — `map`, `filter`, `reduce` with real examples | 15 min | Fabric |
| DFY-09 | Partial Application Examples | Script | `partial_apply.py` — `functools.partial` for configurable functions | 15 min | Fabric |
| DFY-10 | Function Documentation Template | Template | `docstring_template.py` — Google-style + NumPy-style examples | 10 min | Clone Engine |

---

## B-029 — Dictionaries: The Power Data Structure

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Contact Book | Script | `contacts.py` — CRUD operations on a dict-based contact store | 20 min | ADA |
| DFY-02 | Word Frequency Counter | Script | `word_freq.py` — counts word frequency from text file using `Counter` | 15 min | Fabric |
| DFY-03 | Config Parser | Script | `config_parser.py` — reads `.env`-style file to dict with type coercion | 15 min | ADA |
| DFY-04 | JSON Schema Validator | Script | `validate_schema.py` — checks dict against required keys/types | 20 min | ADA |
| DFY-05 | Nested Dict Flattener | Script | `flatten_dict.py` — flattens `{a: {b: 1}}` to `{a.b: 1}` | 15 min | Fabric |
| DFY-06 | Inverted Index Builder | Script | `invert_index.py` — word → list of documents that contain it | 20 min | Fabric |
| DFY-07 | Cache Manager | Script | `cache.py` — TTL-based in-memory cache using `dict` + `time` | 25 min | ADA |
| DFY-08 | Data Grouper | Script | `group_by.py` — groups list of dicts by a key field | 15 min | Fabric |
| DFY-09 | Dict Diff Tool | Script | `dict_diff.py` — shows added/removed/changed keys between two dicts | 15 min | Fabric |
| DFY-10 | Dictionary Pattern Reference | Template | `dict_patterns.py` — 10 most useful dict patterns with comments | 10 min | Fabric |

---

## B-030 — Reading and Writing Files

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | File Reader with Error Handling | Script | `safe_reader.py` — reads file, handles missing/permission errors | 10 min | ADA |
| DFY-02 | CSV Report Generator | Script | `csv_report.py` — reads data, calculates stats, writes summary CSV | 20 min | ADA |
| DFY-03 | JSON Config Read/Write Tool | Script | `json_config.py` — read/update/write JSON config file atomically | 20 min | ADA |
| DFY-04 | Log File Rotator | Script | `log_rotator.py` — Python-native log rotation without `logrotate` | 20 min | ADA |
| DFY-05 | Bulk File Processor | Script | `bulk_process.py` — reads all `.txt` files in a dir, transforms, writes | 20 min | ADA |
| DFY-06 | File Watcher | Script | `file_watcher.py` — polls a file for changes, triggers callback | 20 min | Hermes |
| DFY-07 | Atomic File Writer | Script | `atomic_write.py` — write to temp, then rename — never corrupts | 15 min | ADA |
| DFY-08 | Directory Differ | Script | `dir_diff.py` — finds files in dir A not in dir B | 15 min | Fabric |
| DFY-09 | YAML Config Reader Template | Template | `yaml_config.py` — reads YAML with `PyYAML`, validates keys | 15 min | ADA |
| DFY-10 | File I/O Patterns Reference | Template | `file_patterns.py` — 10 patterns: context manager, streaming, binary | 10 min | Fabric |

---

## B-031 — Errors That Tell the Truth

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Custom Exception Hierarchy | Script | `exceptions.py` — base error + 5 typed subclasses for your app | 20 min | ADA |
| DFY-02 | Retry Decorator with Logging | Script | `retry.py` — `@retry(times=3, delay=1.0, exceptions=(IOError,))` | 20 min | ADA |
| DFY-03 | Error Context Manager | Script | `error_context.py` — `with suppress_and_log(ValueError):` pattern | 15 min | ADA |
| DFY-04 | Safe Division Library | Script | `safe_math.py` — `safe_divide`, `safe_sqrt`, `safe_log` with defaults | 10 min | Fabric |
| DFY-05 | API Response Error Handler | Script | `api_errors.py` — maps HTTP status codes to typed exceptions | 20 min | Hermes |
| DFY-06 | Database Error Recovery Pattern | Template | `db_errors.py` — `IntegrityError`/`OperationalError` handling with retry | 20 min | ADA |
| DFY-07 | Global Exception Logger | Script | `global_handler.py` — `sys.excepthook` replacement that logs + alerts | 15 min | Hermes |
| DFY-08 | Error Rate Monitor | Script | `error_rate.py` — counts exceptions per minute, alerts on spike | 20 min | Hermes |
| DFY-09 | Test Error Scenarios Template | Template | `test_errors.py` — pytest fixtures for testing all error branches | 15 min | ADA |
| DFY-10 | Exception Hierarchy Reference | Template | `exception_guide.py` — when to raise which exception type | 10 min | Fabric |

---

## B-032 — HTTP APIs: Talking to the World

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | GitHub API Client | Script | `github_client.py` — list repos, issues, PRs for any user | 20 min | Clone Engine |
| DFY-02 | Weather Dashboard | Script | `weather.py` — OpenWeatherMap API → formatted terminal output | 20 min | ADA |
| DFY-03 | REST API Tester | Script | `api_tester.py` — sends GET/POST/PUT/DELETE, shows response time | 15 min | Hermes |
| DFY-04 | JSON Response Flattener | Script | `json_flatten.py` — flattens nested API response to CSV | 15 min | Fabric |
| DFY-05 | API Rate Limiter | Script | `rate_limiter.py` — respects `X-RateLimit-*` headers automatically | 20 min | ADA |
| DFY-06 | Webhook Receiver (Flask) | Script | `webhook.py` — receives POST, validates signature, logs payload | 25 min | Hermes |
| DFY-07 | API Response Cacher | Script | `cached_api.py` — TTL-based cache for expensive API calls | 20 min | ADA |
| DFY-08 | Pagination Handler | Script | `paginate.py` — auto-fetches all pages from a paginated API | 20 min | Fabric |
| DFY-09 | API Key Rotation Template | Template | `api_keys.py` — rotates between N keys, tracks usage per key | 20 min | ADA |
| DFY-10 | API Integration Checklist | Checklist | 10 checks before shipping an API integration to production | 5 min | ADA |

---

## B-033 — Object-Oriented Python

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Product Catalog Class | Script | `catalog.py` — `Product`, `Catalog`, `CartItem` with type hints | 25 min | ADA |
| DFY-02 | Bank Account Simulator | Script | `bank.py` — `Account`, `SavingsAccount`, `CheckingAccount` with inheritance | 25 min | ADA |
| DFY-03 | Observer Pattern Implementation | Script | `observer.py` — `EventEmitter`, `Listener`, `emit()`, `subscribe()` | 25 min | Hermes |
| DFY-04 | Singleton Pattern Template | Template | `singleton.py` — thread-safe singleton using `__new__` | 15 min | ADA |
| DFY-05 | Factory Pattern Template | Template | `factory.py` — `AgentFactory.create(type)` — extensible object creation | 20 min | Clone Engine |
| DFY-06 | Dataclass-Based Config Object | Script | `config_obj.py` — frozen dataclass with `__post_init__` validation | 15 min | ADA |
| DFY-07 | Mixin Library | Script | `mixins.py` — `LogMixin`, `TimestampMixin`, `SerializeMixin` | 20 min | Fabric |
| DFY-08 | Abstract Base Class Template | Template | `abc_template.py` — `ABCPlugin` with enforced `execute()` interface | 15 min | Clone Engine |
| DFY-09 | `__repr__` and `__str__` Guide | Template | `repr_guide.py` — 5 patterns for human-readable object output | 10 min | Fabric |
| DFY-10 | OOP Design Checklist | Checklist | 10 questions before writing a new class | 5 min | ADA |

---

## B-034 — Testing with pytest

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Test Suite Bootstrap Script | Script | `init_tests.sh` — creates `tests/`, `conftest.py`, first passing test | 15 min | ADA |
| DFY-02 | Fixture Library Template | Template | `conftest.py` — 8 reusable fixtures (temp dir, mock DB, fake HTTP) | 20 min | ADA |
| DFY-03 | Parametrized Test Template | Template | `test_params.py` — `@pytest.mark.parametrize` for 5 edge cases | 15 min | ADA |
| DFY-04 | Mock External API Tests | Template | `test_api.py` — `responses` library to mock HTTP calls | 20 min | Hermes |
| DFY-05 | Coverage Report Generator | Script | `run_coverage.sh` — pytest + coverage + HTML report | 10 min | ADA |
| DFY-06 | Property-Based Test Template | Template | `test_hypothesis.py` — Hypothesis strategies for input fuzzing | 20 min | ADA |
| DFY-07 | Test Data Factory | Script | `factories.py` — `faker`-powered test data builders | 20 min | ADA |
| DFY-08 | Integration Test Template | Template | `test_integration.py` — real SQLite DB + real HTTP via `httpx` | 25 min | ADA |
| DFY-09 | CI Test Matrix Template | Template | `.github/workflows/test.yml` — matrix across Python 3.11/3.12 | 15 min | ADA |
| DFY-10 | Testing Readiness Checklist | Checklist | 12 items before marking a feature "tested and ready" | 5 min | ADA |

---

## B-035 — Virtual Environments and pip

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Project Bootstrap Script | Script | `bootstrap.sh` — creates venv, installs deps, verifies setup | 15 min | ADA |
| DFY-02 | `pyproject.toml` Template | Config | Full `pyproject.toml` with `[project]`, `[tool.pytest]`, `[tool.ruff]` | 15 min | ADA |
| DFY-03 | Dependency Audit Script | Script | `dep_audit.py` — checks for outdated + vulnerable packages | 15 min | Hermes |
| DFY-04 | Requirements Pinning Script | Script | `pin_deps.sh` — generates `requirements.txt` from `pip freeze` | 5 min | ADA |
| DFY-05 | Multi-Python Version Tester | Script | `tox_setup.sh` — creates `tox.ini` for Python 3.10–3.12 | 15 min | ADA |
| DFY-06 | Dev/Prod Dependency Separator | Config | `requirements/` layout: `base.txt`, `dev.txt`, `prod.txt` | 10 min | ADA |
| DFY-07 | `uv` Fast Setup Script | Script | `uv_setup.sh` — installs and uses `uv` for 10x faster installs | 15 min | ADA |
| DFY-08 | Virtual Environment Health Checker | Script | `venv_check.py` — verifies interpreter, packages, pip version | 10 min | ADA |
| DFY-09 | Package Version Constraint Guide | Template | `versioning.md` — `>=`, `~=`, `==` — when to use each | 10 min | Fabric |
| DFY-10 | Dependency Management Checklist | Checklist | 10 checks before adding a new package to a project | 5 min | ADA |

---

## B-036 — Type Hints: Making Python Honest

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Type-Annotated Utility Library | Script | `typed_utils.py` — 10 fully annotated utility functions | 20 min | Fabric |
| DFY-02 | `mypy` Config Template | Config | `pyproject.toml` `[tool.mypy]` section — strict mode | 10 min | ADA |
| DFY-03 | TypedDict Schema Library | Script | `schemas.py` — TypedDict for 5 common API response shapes | 20 min | Fabric |
| DFY-04 | Protocol Interface Library | Script | `protocols.py` — `Readable`, `Writable`, `Serializable` Protocols | 20 min | Fabric |
| DFY-05 | Generic Container Template | Template | `generic_repo.py` — `Repository[T]` generic base class | 20 min | Fabric |
| DFY-06 | Overloaded Function Template | Template | `overloads.py` — `@overload` for functions with multiple signatures | 15 min | Fabric |
| DFY-07 | `Annotated` Metadata Template | Template | `annotated.py` — `Annotated[int, Gt(0)]` with pydantic | 15 min | ADA |
| DFY-08 | Type Guard Template | Template | `type_guards.py` — `TypeGuard[User]` for narrowing | 15 min | Fabric |
| DFY-09 | Mypy Error Fixer Cheat Sheet | Template | `mypy_fixes.md` — 15 common mypy errors + exact fixes | 10 min | ADA |
| DFY-10 | Type Safety Checklist | Checklist | 10 items before calling a module "type-safe" | 5 min | ADA |

---

## B-037 — Working with Dates and Times

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Age Calculator | Script | `age.py` — precise age from birthdate including months/days | 10 min | ADA |
| DFY-02 | Business Days Calculator | Script | `bizdays.py` — N business days from any date, skip weekends+holidays | 20 min | ADA |
| DFY-03 | Countdown to Event Script | Script | `event_countdown.py` — days/hours/minutes until named event | 15 min | ADA |
| DFY-04 | Timezone Converter Tool | Script | `tz_convert.py` — converts time between any two IANA timezones | 15 min | ADA |
| DFY-05 | Meeting Scheduler Helper | Script | `meeting.py` — finds available slots across multiple timezones | 25 min | ADA |
| DFY-06 | Duration Formatter | Script | `duration.py` — converts seconds to `2h 34m 12s` human format | 10 min | Fabric |
| DFY-07 | Date Range Generator | Script | `daterange.py` — yields every date between start and end | 10 min | Fabric |
| DFY-08 | ISO 8601 Normalizer | Script | `iso_norm.py` — parses 10 common date formats to UTC ISO string | 20 min | Fabric |
| DFY-09 | Recurring Event Generator | Script | `recur.py` — daily/weekly/monthly recurrence with exceptions | 25 min | ADA |
| DFY-10 | Datetime Pattern Reference | Template | `datetime_patterns.py` — 10 essential datetime patterns | 10 min | Fabric |

---

## B-038 — Regular Expressions Demystified

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Email Validator with Regex | Script | `validate_email.py` — RFC-5321 email pattern with named groups | 15 min | ADA |
| DFY-02 | URL Parser with Regex | Script | `parse_url.py` — extracts scheme/host/path/query/fragment | 15 min | Fabric |
| DFY-03 | Log Line Parser | Script | `log_parser.py` — parses Apache/Nginx log lines to dicts | 20 min | Hermes |
| DFY-04 | Credit Card Number Masker | Script | `mask_cc.py` — masks all but last 4 digits safely | 10 min | Hermes |
| DFY-05 | Markdown Link Extractor | Script | `md_links.py` — extracts all `[text](url)` from a `.md` file | 10 min | Fabric |
| DFY-06 | Code Comment Stripper | Script | `strip_comments.py` — removes `#` and `//` comments from code | 15 min | Fabric |
| DFY-07 | Phone Number Normalizer | Script | `normalize_phone.py` — parses 10 formats to `+1 (555) 123-4567` | 15 min | ADA |
| DFY-08 | Password Strength Checker | Script | `pwstrength.py` — scores password by regex criteria | 15 min | Hermes |
| DFY-09 | HTML Tag Stripper | Script | `strip_html.py` — removes all HTML tags safely (no `eval`) | 10 min | Fabric |
| DFY-10 | Regex Pattern Library | Template | `regex_library.py` — 20 production-ready compiled patterns | 10 min | Fabric |

---

## B-039 — SQLite: Your First Database

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Product Inventory Database | Script | `inventory.py` — `Product` CRUD + search + low-stock alert | 25 min | ADA |
| DFY-02 | User Authentication Store | Script | `auth_db.py` — `bcrypt`-hashed passwords + session tokens | 25 min | ADA |
| DFY-03 | Time Tracker Database | Script | `timetrack.py` — start/stop timer, query hours by project | 25 min | ADA |
| DFY-04 | SQLite Backup Script | Script | `sqlite_backup.py` — hot backup using `VACUUM INTO` | 15 min | ADA |
| DFY-05 | Schema Migration Runner | Script | `migrate.py` — versioned SQL migrations with rollback | 25 min | ADA |
| DFY-06 | Full-Text Search Setup | Script | `fts.py` — SQLite FTS5 virtual table for document search | 20 min | Fabric |
| DFY-07 | SQLite to CSV Exporter | Script | `db_export.py` — exports any table to CSV with headers | 10 min | Fabric |
| DFY-08 | Query Profiler | Script | `query_profile.py` — times and explains each query | 15 min | Hermes |
| DFY-09 | Test Database Fixture | Template | `test_db.py` — pytest fixture for in-memory SQLite test DB | 15 min | ADA |
| DFY-10 | Database Design Checklist | Checklist | 10 items before creating your first production schema | 5 min | ADA |

---

## B-040 — Automation Scripts That Save Hours

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Photo Organizer by Date | Script | `photo_organize.py` — moves photos to `YYYY/MM/` folders by EXIF date | 25 min | ADA |
| DFY-02 | Project Scaffolding Generator | Script | `scaffold.py` — creates full project structure from a YAML template | 25 min | Clone Engine |
| DFY-03 | Email Report Sender | Script | `email_report.py` — sends daily summary via SMTP | 20 min | Hermes |
| DFY-04 | Bulk PDF Renamer | Script | `pdf_rename.py` — renames PDFs by extracted text/date | 20 min | ADA |
| DFY-05 | Duplicate File Remover | Script | `dedup_files.py` — MD5-based deduplication across directories | 20 min | ADA |
| DFY-06 | Website Uptime Monitor | Script | `uptime_monitor.py` — checks N URLs every N minutes, logs/alerts | 20 min | Hermes |
| DFY-07 | Data Sync Script | Script | `sync.py` — bidirectional file sync between two directories | 25 min | ADA |
| DFY-08 | Report Aggregator | Script | `aggregate.py` — merges N CSV files, dedupes, sorts, outputs one | 20 min | Fabric |
| DFY-09 | Screenshot Renamer | Script | `rename_screenshots.py` — renames `Screenshot_*.png` to `YYYY-MM-DD_HH-MM.png` | 10 min | ADA |
| DFY-10 | Automation Safety Checklist | Checklist | 10 items before running any automation on real data | 5 min | ADA |

---

## B-041 — Python and the Web: Scraping Basics

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Hacker News Top Stories Scraper | Script | `hn_scraper.py` — fetches top 10 stories to terminal | 20 min | Fabric |
| DFY-02 | Price Alert Bot | Script | `price_alert.py` — scrapes product price, emails when below threshold | 25 min | Hermes |
| DFY-03 | Job Board Aggregator | Script | `job_scraper.py` — scrapes listings from N sites, deduplicates | 25 min | ADA |
| DFY-04 | Link Harvester | Script | `link_harvest.py` — extracts all outbound links from any URL | 15 min | Fabric |
| DFY-05 | Sitemap Generator | Script | `sitemap.py` — crawls a site, builds `sitemap.xml` | 25 min | Fabric |
| DFY-06 | Table Extractor | Script | `table_extract.py` — extracts HTML tables to CSV using `pandas` | 15 min | Fabric |
| DFY-07 | Image Downloader | Script | `img_download.py` — finds all images on a page, downloads to folder | 20 min | ADA |
| DFY-08 | robots.txt Compliance Checker | Script | `robots_check.py` — checks if a URL is allowed before scraping | 10 min | Hermes |
| DFY-09 | Polite Scraper Template | Template | `polite_scraper.py` — rate limiting + retry + User-Agent + cache | 25 min | ADA |
| DFY-10 | Web Scraping Ethics Checklist | Checklist | 10 checks before scraping any website | 5 min | Hermes |

---

## B-042 — Your First REST API (FastAPI)

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Notes API | Script | `notes_api.py` — CRUD for notes with IDs, FastAPI + Pydantic | 25 min | ADA |
| DFY-02 | Authentication Middleware Template | Template | `auth.py` — ****** validation with `OAuth2PasswordBearer` | 25 min | ADA |
| DFY-03 | Background Task Runner Template | Template | `bg_tasks.py` — `BackgroundTasks` for async email/processing | 20 min | Hermes |
| DFY-04 | File Upload Endpoint | Script | `upload.py` — receives file, validates type, saves to disk | 20 min | ADA |
| DFY-05 | API Versioning Template | Template | `v1/`, `v2/` router structure with deprecation headers | 20 min | ADA |
| DFY-06 | Rate Limiting Middleware | Script | `rate_limit.py` — per-IP rate limiting with `slowapi` | 20 min | Hermes |
| DFY-07 | Pagination Response Template | Template | `paginate.py` — cursor-based pagination for list endpoints | 20 min | Fabric |
| DFY-08 | OpenAPI Schema Customizer | Template | `openapi.py` — custom tags, descriptions, examples | 15 min | ADA |
| DFY-09 | API Integration Test Template | Template | `test_api.py` — `httpx.AsyncClient` tests for all endpoints | 20 min | ADA |
| DFY-10 | API Launch Checklist | Checklist | 12 items before a REST API goes live | 5 min | ADA |

---

## B-043 — The Async Python Primer

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Async URL Fetcher | Script | `async_fetch.py` — fetches N URLs concurrently with `aiohttp` | 20 min | Hermes |
| DFY-02 | Async Task Queue | Script | `task_queue.py` — `asyncio.Queue` + N worker coroutines | 25 min | ADA |
| DFY-03 | Async File Processor | Script | `async_files.py` — reads N files concurrently with `aiofiles` | 20 min | ADA |
| DFY-04 | Semaphore Rate Limiter Template | Template | `semaphore.py` — limits concurrent operations with `asyncio.Semaphore` | 15 min | ADA |
| DFY-05 | Async Database Pool Template | Template | `async_db.py` — `aiosqlite` connection pool pattern | 20 min | ADA |
| DFY-06 | Async Event Bus | Script | `event_bus.py` — publish/subscribe pattern with `asyncio` queues | 25 min | Hermes |
| DFY-07 | Async Timeout Wrapper | Script | `timeout.py` — `asyncio.wait_for` with fallback value | 10 min | ADA |
| DFY-08 | Async Retry Decorator | Script | `async_retry.py` — exponential backoff for coroutines | 15 min | ADA |
| DFY-09 | Async vs Sync Performance Benchmark | Script | `bench.py` — measures sync vs async speedup for I/O tasks | 20 min | Fabric |
| DFY-10 | Async Patterns Reference | Template | `async_patterns.py` — 10 essential async patterns | 10 min | Fabric |

---

## B-044 — Modules, Packages, and Imports

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Personal Python Utility Package | Script | `myutils/` — `__init__.py`, `strings.py`, `files.py`, `dates.py` | 30 min | Clone Engine |
| DFY-02 | Installable Package Template | Config | `pyproject.toml` — `[build-system]` for `pip install -e .` | 15 min | ADA |
| DFY-03 | Plugin Architecture Template | Template | `plugins/` — auto-discovers and loads `Plugin` subclasses | 25 min | Clone Engine |
| DFY-04 | Lazy Import Pattern | Template | `lazy.py` — defers heavy imports until first use | 15 min | Fabric |
| DFY-05 | Namespace Package Template | Template | `namespace/` — PEP 420 namespace package structure | 15 min | Fabric |
| DFY-06 | Import Cycle Resolver | Template | `circular_fix.py` — TYPE_CHECKING + `if __name__` patterns | 15 min | Fabric |
| DFY-07 | Package Version Checker | Script | `check_version.py` — validates Python + package version requirements | 10 min | ADA |
| DFY-08 | `__all__` Export Controller | Template | `exports.py` — explicit public API with `__all__` | 10 min | ADA |
| DFY-09 | Package Documentation Generator | Script | `gen_docs.sh` — `pdoc` auto-docs from docstrings | 15 min | Fabric |
| DFY-10 | Package Design Checklist | Checklist | 10 items before publishing a package to PyPI | 5 min | ADA |

---

## B-045 — CSV and Spreadsheet Automation

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Sales Report Analyzer | Script | `sales_report.py` — monthly totals, top products, growth % | 25 min | ADA |
| DFY-02 | Excel Dashboard Generator | Script | `dashboard_xl.py` — `openpyxl` charts + conditional formatting | 30 min | ADA |
| DFY-03 | CSV Validator | Script | `csv_validate.py` — schema validation for uploaded CSV files | 20 min | ADA |
| DFY-04 | Multi-Sheet Report Builder | Script | `multi_sheet.py` — writes N dataframes to named Excel sheets | 20 min | ADA |
| DFY-05 | Data Cleaner Pipeline | Script | `clean_data.py` — drops nulls, normalizes strings, fixes types | 20 min | Fabric |
| DFY-06 | CSV Diff Tool | Script | `csv_diff.py` — shows row-level differences between two CSVs | 15 min | Fabric |
| DFY-07 | Pivot Table Generator | Script | `pivot.py` — `pandas` pivot on any column pair | 20 min | Fabric |
| DFY-08 | Scheduled Data Export | Script | `scheduled_export.py` — daily DB query → CSV → email attachment | 25 min | Hermes |
| DFY-09 | Large CSV Chunked Processor | Script | `chunk_process.py` — processes CSV in N-row chunks to avoid OOM | 20 min | ADA |
| DFY-10 | Data Quality Checklist | Checklist | 10 items before trusting any CSV dataset | 5 min | ADA |

---

## B-046 — Command-Line Tools with Python

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Git Status Summarizer CLI | Script | `git_status_cli.py` — typer CLI showing all repos' status at once | 20 min | Clone Engine |
| DFY-02 | Project Scaffolder CLI | Script | `scaffold_cli.py` — `click` CLI to generate new project from template | 25 min | Clone Engine |
| DFY-03 | Password Generator CLI | Script | `passgen.py` — typer CLI with length, complexity, count options | 15 min | ADA |
| DFY-04 | Color-Rich System Info CLI | Script | `sysinfo_cli.py` — rich tables for CPU, RAM, disk, network | 20 min | Hermes |
| DFY-05 | File Search CLI | Script | `search_cli.py` — recursive content search with highlight output | 20 min | Fabric |
| DFY-06 | Batch File Processor CLI | Script | `batch_cli.py` — processes files in parallel with progress bar | 25 min | ADA |
| DFY-07 | API Caller CLI | Script | `apicall.py` — any REST API from CLI with auth + JSON pretty output | 20 min | Hermes |
| DFY-08 | Database Query CLI | Script | `db_cli.py` — run SQLite queries from the command line | 20 min | ADA |
| DFY-09 | Report Generator CLI | Script | `report_cli.py` — outputs Markdown, HTML, or JSON from data | 25 min | ADA |
| DFY-10 | CLI Distribution Checklist | Checklist | 10 steps to package a typer CLI for `pip install` | 5 min | ADA |

---

## B-047 — Python Decorators Without the Magic

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Production Decorator Toolkit | Script | `dec_toolkit.py` — `@timer`, `@retry`, `@rate_limit`, `@log_calls` | 30 min | ADA |
| DFY-02 | `@validate_types` Decorator | Script | `validate_types.py` — runtime type checking using annotations | 20 min | ADA |
| DFY-03 | `@require_env` Decorator | Script | `require_env.py` — raises at call time if env vars missing | 15 min | ADA |
| DFY-04 | `@cache_result` with TTL | Script | `cache_ttl.py` — cached result expires after N seconds | 20 min | ADA |
| DFY-05 | `@singleton` Decorator | Script | `singleton_dec.py` — enforces one instance per class | 15 min | ADA |
| DFY-06 | `@deprecated` Warning Decorator | Script | `deprecated.py` — warns on call with replacement function name | 10 min | Clone Engine |
| DFY-07 | `@profile_memory` Decorator | Script | `profile_mem.py` — prints memory delta before/after function | 20 min | Hermes |
| DFY-08 | Class Decorator Template | Template | `class_dec.py` — adds `__repr__`, `__eq__`, logging to any class | 20 min | Fabric |
| DFY-09 | Decorator Stack Order Guide | Template | `dec_order.py` — demonstrates and explains decoration order | 10 min | Fabric |
| DFY-10 | Decorator Testing Template | Template | `test_decorators.py` — pytest tests for all 6 toolkit decorators | 15 min | ADA |

---

## B-048 — Environment Configuration Done Right

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Multi-Environment Config System | Script | `env_config.py` — Dev/Staging/Prod configs from one codebase | 25 min | ADA |
| DFY-02 | `.env.example` with Docs Generator | Script | `gen_env_docs.py` — creates annotated `.env.example` from pydantic model | 15 min | Clone Engine |
| DFY-03 | Config Validation on Startup | Script | `startup_check.py` — fails fast if required config is missing | 10 min | ADA |
| DFY-04 | Feature Flag Config | Script | `feature_flags.py` — boolean env vars control feature rollout | 20 min | ADA |
| DFY-05 | Kubernetes ConfigMap Template | Template | `configmap.yaml` — maps to env vars in deployment | 20 min | ADA |
| DFY-06 | Config Diff Tool | Script | `config_diff.py` — shows what changed between two config states | 15 min | Hermes |
| DFY-07 | Local Dev Config Template | Config | `.env.local` + `.env.test` + `.env.prod.example` starter kit | 10 min | ADA |
| DFY-08 | Config Change Audit Logger | Script | `config_audit.py` — logs every config change with timestamp | 15 min | Hermes |
| DFY-09 | Config Documentation Generator | Script | `config_docs.py` — generates README table from pydantic model | 15 min | Fabric |
| DFY-10 | Configuration Readiness Checklist | Checklist | 12 items before a new service goes to production | 5 min | ADA |

---

## B-049 — Logging: The Program's Memory

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Production Logging Setup Library | Script | `log_setup.py` — JSON + console handlers, `setup_logging()` | 20 min | Hermes |
| DFY-02 | Request ID Injector | Script | `request_id.py` — injects `request_id` via `ContextVar` into all logs | 20 min | Hermes |
| DFY-03 | Slow Query Logger | Script | `slow_query.py` — logs any DB query taking > threshold ms | 20 min | Hermes |
| DFY-04 | Audit Trail Logger | Script | `audit.py` — immutable append-only log for user actions | 20 min | Hermes |
| DFY-05 | Log Level Switcher | Script | `log_switch.py` — change log level at runtime via signal/env | 15 min | Hermes |
| DFY-06 | Structured Log Shipper | Script | `log_ship.py` — ships JSON logs to file for Loki/ELK ingestion | 20 min | Hermes |
| DFY-07 | Error Budget Logger | Script | `error_budget.py` — counts errors per hour, alerts at threshold | 20 min | Hermes |
| DFY-08 | Log Sampling Template | Template | `log_sample.py` — logs only 1-in-N DEBUG messages to reduce noise | 15 min | Hermes |
| DFY-09 | Log Replay Tool | Script | `log_replay.py` — reads JSON logs, replays events for debugging | 20 min | Hermes |
| DFY-10 | Logging Design Checklist | Checklist | 10 items: levels, format, rotation, sampling, shipping | 5 min | Hermes |

---

## B-050 — Python + Linux: The Power Combo

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | System Health Reporter | Script | `health.py` — CPU, RAM, disk, processes to structured JSON | 20 min | Hermes |
| DFY-02 | Service Manager CLI | Script | `svc_mgr.py` — Python-driven start/stop/restart/status for services | 25 min | ADA |
| DFY-03 | Disk Cleanup Automation | Script | `disk_cleanup.py` — removes old logs, cache, temp using `pathlib` | 20 min | ADA |
| DFY-04 | SSH Multi-Host Runner | Script | `multi_ssh.py` — runs a command on N hosts, collects output | 20 min | ADA |
| DFY-05 | Cron Job Python Wrapper | Script | `cron_runner.py` — wraps any script with logging + lock + alert | 20 min | Hermes |
| DFY-06 | System Metrics Exporter | Script | `metrics_export.py` — writes Prometheus-format metrics to file | 25 min | Hermes |
| DFY-07 | File Watcher Daemon | Script | `fwatch.py` — `inotify` via `watchdog` library, triggers callbacks | 25 min | Hermes |
| DFY-08 | Network Scanner | Script | `net_scan.py` — subnet ping sweep + open port check | 20 min | Hermes |
| DFY-09 | System Backup Orchestrator | Script | `backup_orch.py` — orchestrates rsync + SQLite dump + S3 upload | 30 min | ADA |
| DFY-10 | Linux+Python Integration Checklist | Checklist | 10 items when replacing a shell script with Python | 5 min | ADA |

---

## B-051 — Git with Python

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Multi-Repo Status Dashboard | Script | `repo_dashboard.py` — status/branch/ahead-behind for N repos | 25 min | Clone Engine |
| DFY-02 | Automated Release Notes Generator | Script | `release_notes.py` — commit log → Markdown changelog | 25 min | Clone Engine |
| DFY-03 | Stale Branch Reporter | Script | `stale_branches.py` — lists branches with no activity in N days | 20 min | Clone Engine |
| DFY-04 | Commit Message Linter | Script | `commit_lint.py` — enforces conventional commits via `post-commit` hook | 20 min | ADA |
| DFY-05 | PR Description Generator (AI Prompt) | Prompt | lippytmai prompt: generates PR description from diff + commits | 10 min | Clone Engine |
| DFY-06 | Git Tag Automator | Script | `auto_tag.py` — increments semver tag on release branch | 20 min | ADA |
| DFY-07 | Repository Archiver | Script | `repo_archive.py` — bundles repo to `.tar.gz` with manifest | 20 min | ADA |
| DFY-08 | GitHub Actions Trigger Script | Script | `trigger_workflow.py` — fires a GitHub Actions workflow via API | 15 min | Hermes |
| DFY-09 | Commit Stats Aggregator | Script | `commit_stats.py` — author breakdown, files changed, weekly cadence | 20 min | Hermes |
| DFY-10 | Git Automation Checklist | Checklist | 10 items before automating Git operations on a team repo | 5 min | ADA |

---

## B-052 — Your First Docker Container

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Multi-Stage Python Build Template | Template | `Dockerfile` — builder stage + slim runtime + non-root user | 20 min | ADA |
| DFY-02 | Docker Compose Dev+Prod Split | Template | `compose.dev.yml` + `compose.prod.yml` with overrides | 20 min | ADA |
| DFY-03 | Container Security Scanner Workflow | Workflow | GitHub Actions: `trivy` scan on every image build | 20 min | Hermes |
| DFY-04 | Health Check Endpoint + Docker HEALTHCHECK | Script | `health.py` endpoint + `HEALTHCHECK` in Dockerfile | 20 min | Hermes |
| DFY-05 | Image Build Speed Optimizer | Template | `Dockerfile` with layer caching, `--mount=type=cache` for pip | 20 min | ADA |
| DFY-06 | Secrets at Runtime Template | Template | `docker run --secret` + `docker compose secrets:` | 15 min | ADA |
| DFY-07 | Container Log Driver Config | Config | `docker-compose.yml` with `json-file` + `max-size`/`max-file` | 10 min | Hermes |
| DFY-08 | Non-Root User Setup Template | Template | `Dockerfile` — `useradd`, `chown`, `USER appuser` | 10 min | Hermes |
| DFY-09 | Docker Compose Override Template | Template | `docker-compose.override.yml` for local dev differences | 10 min | ADA |
| DFY-10 | Container Production Checklist | Checklist | 15 items before deploying a container to production | 5 min | ADA |

---

## B-053 — Environment Variables and Security

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Full Secrets Audit Script | Script | `secrets_scan.py` — scans all Python files for hardcoded patterns | 20 min | Hermes |
| DFY-02 | HashiCorp Vault Integration Template | Template | `vault_client.py` — reads secrets from Vault API | 25 min | ADA |
| DFY-03 | AWS Secrets Manager Client | Template | `aws_secrets.py` — reads secrets via `boto3` with caching | 20 min | ADA |
| DFY-04 | GitHub Secrets Sync Script | Script | `sync_secrets.py` — syncs `.env` to GitHub repo secrets via API | 20 min | Clone Engine |
| DFY-05 | Secret Expiry Tracker | Script | `secret_expiry.py` — reads expiry dates, alerts 30 days before | 20 min | Hermes |
| DFY-06 | `.env` File Differ | Script | `env_diff.py` — shows what keys changed between two `.env` files | 10 min | Hermes |
| DFY-07 | Pre-Commit Secret Detection Hook | Workflow | `detect-secrets` pre-commit hook + `.secrets.baseline` | 15 min | ADA |
| DFY-08 | Service Account Key Rotator | Script | `rotate_keys.py` — generates new key, updates config, removes old | 25 min | Hermes |
| DFY-09 | Minimal Privilege Config Template | Template | `.env` with read-only DB user, scoped API keys, short TTLs | 10 min | Hermes |
| DFY-10 | Secrets Management Maturity Checklist | Checklist | 15 items: from `.env` file to enterprise secrets management | 5 min | Hermes |

---

## B-054 — Debugging Python Like a Professional

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Post-Mortem Debug Session Template | Script | `pm_debug.py` — `pdb.pm()` on any exception with context | 15 min | ADA |
| DFY-02 | Variable Inspector Decorator | Script | `@inspect_vars` — prints all local variables at function entry/exit | 15 min | Fabric |
| DFY-03 | Assertion-Enhanced Debug Mode | Script | `debug_mode.py` — enables full assertions + verbose logging in dev | 10 min | ADA |
| DFY-04 | Memory Usage Tracker | Script | `mem_tracker.py` — `tracemalloc` snapshot diff between two points | 20 min | Hermes |
| DFY-05 | Flame Graph Generator Script | Script | `flame.sh` — `py-spy record` + open SVG in browser | 10 min | Hermes |
| DFY-06 | Test-Driven Bug Fix Template | Template | `tdd_fix.py` — write failing test → fix → verify green | 20 min | ADA |
| DFY-07 | Production-Safe Debug Logger | Script | `prod_debug.py` — samples verbose logs at 1% in production | 15 min | Hermes |
| DFY-08 | Exception Replay Tool | Script | `exc_replay.py` — serializes exception state for replay later | 20 min | Hermes |
| DFY-09 | Async Debug Tracer | Script | `async_trace.py` — traces coroutine execution with timing | 20 min | Hermes |
| DFY-10 | Bug Triage Checklist | Checklist | 10-step process from bug report to verified fix | 5 min | ADA |

---

## B-055 — Python L1 SkillBadge (Capstone)

| # | DFY Title | Type | Deliverable | Time | ACSS |
|---|---|---|---|---|---|
| DFY-01 | Complete Portfolio CLI Package | Script | `portfolio/` — installable, Docker-ready, fully tested CLI | 60 min | ADA |
| DFY-02 | Credential Registry Builder | Script | `build_registry.py` — auto-populates registry from your 30 artifacts | 25 min | ADA |
| DFY-03 | Portfolio Markdown Generator | Script | `gen_portfolio.py` — produces shareable `portfolio_l1.md` | 15 min | Clone Engine |
| DFY-04 | Proof-of-Work Artifact Verifier | Script | `verify_all.py` — checks all 30 artifacts exist + run correctly | 20 min | ADA |
| DFY-05 | Portfolio Test Suite | Template | `tests/` — 10 pytest tests covering all CLI commands | 20 min | ADA |
| DFY-06 | Portfolio Docker Image | Template | `Dockerfile` — multi-stage build, non-root, health check | 20 min | ADA |
| DFY-07 | LinkedIn Credential Card Template | Template | `linkedin_card.md` — ready-to-paste portfolio summary | 10 min | Clone Engine |
| DFY-08 | Peer Review Submission Package | Workflow | `submit.sh` — zips portfolio, generates manifest, submits to ADA | 15 min | ADA |
| DFY-09 | Phase 3 Learning Roadmap | Template | `roadmap_phase3.md` — your personalized blockchain learning path | 15 min | Clone Engine |
| DFY-10 | Phase 2 Complete Retrospective | Template | `retro_phase2.md` — what you built, what you learned, what's next | 20 min | Clone Engine |

---

## DFY Phase 2 Summary

| Phase | Books | DFY Lessons | Total Time (est.) |
|---|---|---|---|
| Phase 1 Linux (B-001–B-025) | 25 | 250 | ~52 hours |
| Phase 2 Python (B-026–B-055) | 30 | 300 | ~65 hours |
| **Total (Phases 1–2)** | **55** | **550** | **~117 hours** |

Each DFY lesson produces a **real, deployable artifact** — not exercises, not theory, but working tools you use immediately.

---

## Further Reading

- 📄 [`docs/DFY-LESSONS-SYSTEM.md`](DFY-LESSONS-SYSTEM.md) — DFY system overview
- 📄 [`docs/DFY-B001-B025-phase1-linux.md`](DFY-B001-B025-phase1-linux.md) — Phase 1 DFY lessons
- 📄 [`docs/ai-deployment-activations.md`](ai-deployment-activations.md) — ADA credential system
- 📄 [`docs/P011-EBOOK-000-course-series-master-plan.md`](P011-EBOOK-000-course-series-master-plan.md) — 300-book master plan
- 🏠 [`README.md`](../README.md) — Encyclopedia home

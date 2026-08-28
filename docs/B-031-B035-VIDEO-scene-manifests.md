# B-031–B-035 HDVG Scene Manifests

## Phase 2 Batch 2 — Python Intermediate

### lippytmai Video Production Scripts

> **Format:** HDVG (Human-Directed Video Generation) scene manifest
> **Mode:** Tutorial — lippytmai walks learners through live coding in a sandboxed terminal

---

## B-031 Script: "Errors That Tell the Truth"

```json
{
  "manifest_id": "HDVG-B031",
  "book_id": "B-031",
  "title": "Errors That Tell the Truth",
  "mode": "Tutorial",
  "narrator": "lippytmai",
  "total_scenes": 8,
  "scenes": [
    {"scene": 1, "title": "The Crash You Didn't Expect", "type": "hook",
     "narration": "Every program crashes eventually. The question is whether it crashes with information or in silence. Today you learn to write code that tells the truth when things go wrong.",
     "visual": "program crash → helpful error message vs silent failure"},
    {"scene": 2, "title": "try/except Basics", "type": "demo",
     "narration": "Wrap risky code in try. Catch specific exceptions in except. Handle the error. Keep the program running.",
     "visual": "file open; KeyError; ZeroDivisionError — each caught and handled"},
    {"scene": 3, "title": "Exception Hierarchy", "type": "explainer",
     "narration": "All exceptions inherit from BaseException. Most inherit from Exception. Catch specific types — never bare except.",
     "visual": "exception tree diagram; show why bare except is dangerous"},
    {"scene": 4, "title": "else and finally", "type": "demo",
     "narration": "else runs only when no exception occurred. finally runs always — perfect for cleanup like closing files or connections.",
     "visual": "file reading with try/except/else/finally"},
    {"scene": 5, "title": "Custom Exceptions", "type": "demo",
     "narration": "Define your own exception classes. Give them context. Make error messages specific to your domain.",
     "visual": "ValidationError, InsufficientFundsError classes"},
    {"scene": 6, "title": "raise and re-raise", "type": "demo",
     "narration": "raise creates an exception. raise (bare) re-raises the current one with its original traceback intact.",
     "visual": "raise ValueError; except → raise; logging before re-raise"},
    {"scene": 7, "title": "Build: robust_file_reader.py", "type": "build",
     "narration": "Read files with full error handling: missing file, permission denied, encoding errors, corrupt data. The robust way.",
     "visual": "complete robust_file_reader demo with all error paths"},
    {"scene": 8, "title": "Proof of Work", "type": "credential",
     "narration": "CCSLL-L1-B031-ErrorHandler. Your code now handles failure gracefully. Next: the internet.",
     "visual": "credential card; preview B-032"}
  ]
}
```

---

## B-032 Script: "The Internet in a Function"

```json
{
  "manifest_id": "HDVG-B032",
  "book_id": "B-032",
  "title": "The Internet in a Function",
  "mode": "Tutorial",
  "narrator": "lippytmai",
  "total_scenes": 8,
  "scenes": [
    {"scene": 1, "title": "APIs Are Everywhere", "type": "hook",
     "narration": "Weather, stock prices, AI models, payment systems — all APIs. Once you know how to call an HTTP API, you can talk to any service on the internet.",
     "visual": "GitHub API call → response in 3 lines of Python"},
    {"scene": 2, "title": "requests Basics", "type": "demo",
     "narration": "GET for reading. POST for creating. The response has a status code, headers, and a body. raise_for_status() handles errors automatically.",
     "visual": "requests.get, status_code, json(), text"},
    {"scene": 3, "title": "Headers and Authentication", "type": "demo",
     "narration": "APIs often require authentication. ****** in Authorization header is the most common pattern.",
     "visual": "headers dict; ******; GitHub authenticated request"},
    {"scene": 4, "title": "POST Requests with JSON", "type": "demo",
     "narration": "Creating resources sends data in the request body as JSON. requests handles serialization with json= parameter.",
     "visual": "POST body; Content-Type application/json; response parsing"},
    {"scene": 5, "title": "Error Handling for APIs", "type": "demo",
     "narration": "Network failures, rate limits, 404s, 500s — all need handling. Retry logic and exponential backoff are standard patterns.",
     "visual": "try/except requests.RequestException; retry decorator"},
    {"scene": 6, "title": "Working with Pagination", "type": "demo",
     "narration": "APIs return pages of results. Follow the next page URL until there's nothing left.",
     "visual": "GitHub repos pagination; while loop pattern"},
    {"scene": 7, "title": "Build: api_client.py", "type": "build",
     "narration": "A production-ready API client class: base URL, auth headers, retry logic, rate limiting, and full error handling.",
     "visual": "run api_client.py; live GitHub API demo"},
    {"scene": 8, "title": "Proof of Work", "type": "credential",
     "narration": "CCSLL-L1-B032-APIEngineer. You can speak HTTP fluently. Next: classes and objects.",
     "visual": "credential card; preview B-033"}
  ]
}
```

---

## B-033 Script: "Classes and Objects Made Simple"

```json
{
  "manifest_id": "HDVG-B033",
  "book_id": "B-033",
  "title": "Classes and Objects Made Simple",
  "mode": "Tutorial",
  "narrator": "lippytmai",
  "total_scenes": 8,
  "scenes": [
    {"scene": 1, "title": "Why Objects?", "type": "hook",
     "narration": "A function does one thing. An object groups related data and behavior. When your code has nouns — users, accounts, orders — it's time for classes.",
     "visual": "procedural bank code → class BankAccount refactor"},
    {"scene": 2, "title": "__init__ and self", "type": "demo",
     "narration": "__init__ runs when you create an instance. self is the instance itself. Every method gets self as its first argument.",
     "visual": "BankAccount.__init__; create instances; access attributes"},
    {"scene": 3, "title": "Methods", "type": "demo",
     "narration": "Instance methods operate on one object. Class methods operate on the class. Static methods are just regular functions that live on the class.",
     "visual": "deposit/withdraw; classmethod from_dict; staticmethod validate"},
    {"scene": 4, "title": "Inheritance", "type": "demo",
     "narration": "Subclasses inherit all methods of the parent. super() calls the parent implementation. Override what you need to change.",
     "visual": "Account → SavingsAccount → PremiumAccount inheritance chain"},
    {"scene": 5, "title": "dataclass — Classes Without Boilerplate", "type": "demo",
     "narration": "dataclass generates __init__, __repr__, and __eq__ automatically. For most data-holding classes, this is all you need.",
     "visual": "@dataclass Product, Order; comparison; asdict()"},
    {"scene": 6, "title": "Properties", "type": "demo",
     "narration": "@property lets you compute values on access. Getter/setter/deleter give you controlled attribute access without breaking the interface.",
     "visual": "@property balance; @balance.setter with validation"},
    {"scene": 7, "title": "Build: bank_account.py", "type": "build",
     "narration": "A complete banking system: Account base class, SavingsAccount and CheckingAccount subclasses, transaction history, and full test coverage.",
     "visual": "run bank_account.py; deposit/withdraw/transfer demo"},
    {"scene": 8, "title": "Proof of Work", "type": "credential",
     "narration": "CCSLL-L1-B033-OOPEngineer. You think in objects now. Next: testing your code.",
     "visual": "credential card; preview B-034"}
  ]
}
```

---

## B-034 Script: "Testing Your Code (So Others Trust It)"

```json
{
  "manifest_id": "HDVG-B034",
  "book_id": "B-034",
  "title": "Testing Your Code (So Others Trust It)",
  "mode": "Tutorial",
  "narrator": "lippytmai",
  "total_scenes": 8,
  "scenes": [
    {"scene": 1, "title": "Why Tests?", "type": "hook",
     "narration": "Untested code is code you're guessing works. Tests give you confidence to refactor, upgrade dependencies, and ship without fear.",
     "visual": "refactor without tests → breakage; refactor with tests → green"},
    {"scene": 2, "title": "pytest Basics", "type": "demo",
     "narration": "Name your file test_something.py. Name your function test_something. Run pytest. That's it.",
     "visual": "first test; pytest output; passing vs failing"},
    {"scene": 3, "title": "assert Statements", "type": "demo",
     "narration": "assert expression tells pytest what you expect. pytest shows you what went wrong when it fails.",
     "visual": "assertEqual pattern; assert with message; inspect failure output"},
    {"scene": 4, "title": "Fixtures", "type": "demo",
     "narration": "Fixtures provide shared setup for tests. @pytest.fixture runs before each test that requests it. scope controls how often.",
     "visual": "@pytest.fixture; function scope vs session scope; tmp_path built-in"},
    {"scene": 5, "title": "Parametrize — Test Many Cases at Once", "type": "demo",
     "narration": "@pytest.mark.parametrize runs the same test with different inputs. One test function, many test cases.",
     "visual": "parametrize with 5 input/output pairs; beautiful matrix output"},
    {"scene": 6, "title": "Mocking External Services", "type": "demo",
     "narration": "Tests shouldn't hit real APIs or databases. unittest.mock.patch replaces the real thing with a controllable fake.",
     "visual": "patch requests.get; MagicMock; assert_called_with"},
    {"scene": 7, "title": "Build: test suite for math_utils.py", "type": "build",
     "narration": "A complete test suite: unit tests, parametrized edge cases, fixture-based setup, and mocked external call. All green.",
     "visual": "pytest -v output; all tests passing; coverage report"},
    {"scene": 8, "title": "Proof of Work", "type": "credential",
     "narration": "CCSLL-L1-B034-TestEngineer. Tested code is trusted code. Next: virtual environments.",
     "visual": "credential card; preview B-035"}
  ]
}
```

---

## B-035 Script: "Virtual Environments and pip"

```json
{
  "manifest_id": "HDVG-B035",
  "book_id": "B-035",
  "title": "Virtual Environments and pip",
  "mode": "Tutorial",
  "narrator": "lippytmai",
  "total_scenes": 8,
  "scenes": [
    {"scene": 1, "title": "The Dependency Conflict", "type": "hook",
     "narration": "Project A needs requests==2.28. Project B needs requests==2.31. Without virtual environments, one of them breaks. With them, both work perfectly.",
     "visual": "conflict without venv; clean isolation with venv"},
    {"scene": 2, "title": "Creating a venv", "type": "demo",
     "narration": "python3 -m venv .venv creates an isolated Python environment. source .venv/bin/activate activates it. deactivate leaves it.",
     "visual": "terminal: create, activate, which python, which pip"},
    {"scene": 3, "title": "pip install and requirements.txt", "type": "demo",
     "narration": "pip install installs packages. pip freeze captures your exact versions. requirements.txt records them for reproducibility.",
     "visual": "pip install requests; pip freeze > requirements.txt; pip install -r"},
    {"scene": 4, "title": "pyproject.toml — The Modern Way", "type": "demo",
     "narration": "pyproject.toml is the modern standard for project metadata, dependencies, and build configuration. It replaces setup.py.",
     "visual": "pyproject.toml structure; [project.dependencies]; pip install -e ."},
    {"scene": 5, "title": "Common pip Commands", "type": "demo",
     "narration": "install, uninstall, upgrade, list, show, check. These five cover everything you need day to day.",
     "visual": "pip install --upgrade; pip show requests; pip check"},
    {"scene": 6, "title": "OMARCHY Standard Project Layout", "type": "explainer",
     "narration": "The lippytm.ai OMARCHY standard: src layout, .venv, pyproject.toml, tests/, docs/, Makefile. This is how every lippytm.ai Python project starts.",
     "visual": "tree view of OMARCHY Python project scaffold"},
    {"scene": 7, "title": "Build: Project Scaffold", "type": "build",
     "narration": "Set up a complete OMARCHY-standard Python project from scratch: venv, pyproject.toml, src layout, tests, and a Makefile with lint/test/build targets.",
     "visual": "mkdir, venv, pyproject.toml, src/__init__.py, tests/, Makefile"},
    {"scene": 8, "title": "Proof of Work", "type": "credential",
     "narration": "CCSLL-L1-B035-PythonEngineer. You build isolated, reproducible Python environments. Phase 2 Batch 2 complete. Next: the standard toolkit.",
     "visual": "credential card; all 5 Batch 2 credentials earned; preview B-036"}
  ]
}
```

---

## Hermes Events — Batch 2 Production

```python
BATCH_2_EVENTS = [
    {"type": "SCRIPT_REQUESTED",  "batch": "B031-B035", "mode": "Tutorial"},
    {"type": "FABRIC_QUERIED",    "nodes": ["CCSLL", "exceptions", "http-apis", "oop", "pytest", "venv"]},
    {"type": "SCRIPT_GENERATED",  "books": ["B031", "B032", "B033", "B034", "B035"]},
    {"type": "SANDBOX_STARTED",   "image": "lippytmai/python-sandbox:3.12"},
    {"type": "RECORDING_STARTED", "resolution": "1920x1080", "fps": 60},
    {"type": "RECORDING_COMPLETE","books": ["B031", "B032", "B033", "B034", "B035"]},
    {"type": "QEP_SUBMITTED",     "qep": "QEP-B031-B035", "gates_passed": 12},
    {"type": "G13_GATE_OPEN",     "approver": "Charles Earl Lipshay", "status": "APPROVED",
     "timestamp": "2026-08-28"},
]
```

---

## Further Reading

- 📄 [`docs/ai-copilot-video-sandbox-creator.md`](ai-copilot-video-sandbox-creator.md) — ACVS full spec
- 📄 [`docs/B-036-B040-VIDEO-scene-manifests.md`](B-036-B040-VIDEO-scene-manifests.md) — Batch 3 video scripts
- 📄 [`docs/creative-building-process.md`](creative-building-process.md) — 8-stage creative loop
- 🏠 [`README.md`](../README.md) — Encyclopedia home

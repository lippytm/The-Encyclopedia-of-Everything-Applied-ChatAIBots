# B-046–B-050 HDVG Video Scene Manifests

## Phase 2, Batch 5 — Python DevOps Layer

> 8-scene High-Density Video Guide (HDVG) scripts for each book in Batch 5.
> Identity: `lippytmai` (Teach mode) · Format: explainer + live-code demo · Creative gate: **HumanApprovalGate required before publish**

---

## B-046 — Command-Line Tools with Python

**Hook:** *"Every great CLI tool you've ever used — htop, git, docker — was written by someone who learned exactly what you're about to learn."*

| Scene | Type | Duration | Content |
|---|---|---|---|
| S1 | Hook | 0:00–0:45 | Demo: run `file_processor.py count ./docs` → instant output |
| S2 | Concept | 0:45–2:30 | CLIs vs scripts; the anatomy of a CLI tool (command, flags, args) |
| S3 | Code | 2:30–5:00 | `argparse` from scratch: `ArgumentParser`, `add_argument`, `parse_args` |
| S4 | Code | 5:00–8:00 | `click`: decorators as API — `@click.command`, `@click.option`, groups |
| S5 | Code | 8:00–11:00 | `typer`: type hints → CLI magic; subcommands with classes |
| S6 | Build | 11:00–14:00 | Full `file_processor.py`: count / search / stats / convert subcommands |
| S7 | Debug | 14:00–16:00 | Exit codes, error handling, `--verbose` flag, rich output |
| S8 | Credential | 16:00–17:00 | Proof of Work: `python3 file_processor.py --help` · `CCSLL-L1-B046-CLIEngineer` |

**Hermes event:** `HDVG:B046:RECORD_READY`
**Fabric node:** `CLITools → argparse → click → typer → file_processor`

---

## B-047 — Python Decorators Without the Magic

**Hook:** *"Every time you write `@app.route` or `@pytest.mark.parametrize` you're using a decorator. Today you'll build them yourself."*

| Scene | Type | Duration | Content |
|---|---|---|---|
| S1 | Hook | 0:00–0:45 | Show `@timer` and `@retry` in action — real output on screen |
| S2 | Concept | 0:45–2:30 | Functions as first-class objects; closures; the decorator pattern |
| S3 | Code | 2:30–5:00 | Bare-bones decorator; `functools.wraps`; why metadata matters |
| S4 | Code | 5:00–8:00 | Decorator factories (decorators that take arguments) |
| S5 | Code | 8:00–11:00 | `@retry`, `@rate_limit`, `@timer` — production-ready implementations |
| S6 | Code | 11:00–14:00 | `@log_calls`, `@lru_cache`, `@property`, `@cached_property` |
| S7 | Build | 14:00–16:00 | Assemble `decorators.py` toolkit; run all 4 demo sections |
| S8 | Credential | 16:00–17:00 | Proof of Work: metadata preserved demo · `CCSLL-L1-B047-DecoratorMaster` |

**Hermes event:** `HDVG:B047:RECORD_READY`
**Fabric node:** `Decorators → closures → functools → retry/rate_limit → toolkit`

---

## B-048 — Environment Configuration Done Right

**Hook:** *"Hard-coded secrets have leaked millions of credentials. After today, your apps will never have a config problem again."*

| Scene | Type | Duration | Content |
|---|---|---|---|
| S1 | Hook | 0:00–0:45 | Demo: `.env` change → app behavior changes instantly, zero code edit |
| S2 | Concept | 0:45–2:30 | 12-Factor App #3: config in environment; dev vs staging vs prod |
| S3 | Code | 2:30–5:00 | `python-dotenv`: `load_dotenv()`, `.env` format, `os.getenv` |
| S4 | Code | 5:00–8:00 | `pydantic-settings` BaseSettings: type validation, defaults, SecretStr |
| S5 | Code | 8:00–11:00 | Environment-specific configs: `DevConfig`, `ProdConfig`, `TestConfig` |
| S6 | Build | 11:00–14:00 | Full `config.py`: singleton `@lru_cache`, `get_settings()`, multi-env |
| S7 | Security | 14:00–16:00 | `SecretStr` never logs; `.gitignore` pattern; dotenv in Docker |
| S8 | Credential | 16:00–17:00 | Proof of Work: validation error demo · `CCSLL-L1-B048-ConfigEngineer` |

**Hermes event:** `HDVG:B048:RECORD_READY`
**Fabric node:** `Config → dotenv → pydantic-settings → SecretStr → multi-env`

---

## B-049 — Logging: The Program's Memory

**Hook:** *"Print statements disappear. Logs remember everything. Your future self will thank you."*

| Scene | Type | Duration | Content |
|---|---|---|---|
| S1 | Hook | 0:00–0:45 | Side-by-side: `print()` chaos vs structured JSON logs — grep wins |
| S2 | Concept | 0:45–2:30 | Log levels (DEBUG→CRITICAL); when to use each; the logger hierarchy |
| S3 | Code | 2:30–5:00 | `logging.getLogger(__name__)`: named loggers, propagation |
| S4 | Code | 5:00–8:00 | Handlers: `StreamHandler`, `FileHandler`, `RotatingFileHandler` |
| S5 | Code | 8:00–11:00 | Formatters: text vs JSON; `JSONFormatter` with timestamp/level/message |
| S6 | Code | 11:00–14:00 | `ContextFilter` + `ContextVar`: inject `request_id` into every log line |
| S7 | Build | 14:00–16:00 | Full `log_system.py`: `setup_logging()` + `get_logger()` library |
| S8 | Credential | 16:00–17:00 | Proof of Work: JSON log output · `CCSLL-L1-B049-LoggingEngineer` |

**Hermes event:** `HDVG:B049:RECORD_READY`
**Fabric node:** `Logging → handlers → formatters → JSONFormatter → ContextFilter`

---

## B-050 — Python + Linux: The Power Combo *(Milestone)*

**Hook:** *"Phase 1 gave you Linux. Phase 2 gave you Python. B-050 merges them. This is where real system engineers are born."*

| Scene | Type | Duration | Content |
|---|---|---|---|
| S1 | Milestone | 0:00–1:00 | Recap Phase 1 (25 books Linux) + Phase 2 (24 books Python) → this is the bridge |
| S2 | Concept | 1:00–2:30 | Python as a system language; when shell scripts hit limits |
| S3 | Code | 2:30–5:00 | `subprocess.run()`: `capture_output`, `check`, `timeout`, `text=True` |
| S4 | Code | 5:00–8:00 | `shlex.split()` for safe argument parsing; avoiding shell injection |
| S5 | Code | 8:00–11:00 | `os` + `sys`: platform info, env vars, process management, path ops |
| S6 | Build | 11:00–14:00 | `system_manager.py`: info / disk / processes / services / run commands |
| S7 | Phase3 | 14:00–16:00 | Phase 3 preview: data science → web dev → blockchain → AI/ML |
| S8 | Dual Credential | 16:00–17:30 | Proof of Work: 3 commands pass · `CCSLL-L1-B050-SystemEngineer` + `CLL-L1-B050-LinuxPythonBridge` |

**Hermes event:** `HDVG:B050:RECORD_READY` + `PHASE2:COMPLETE`
**Fabric nodes:** `subprocess → shlex → os/sys → system_manager → [CLL bridge] → [CCSLL bridge]`

---

## Batch Summary

| Book | Credential | Hermes Event | Gate |
|---|---|---|---|
| B-046 | `CCSLL-L1-B046-CLIEngineer` | `HDVG:B046:RECORD_READY` | ⏳ G13 |
| B-047 | `CCSLL-L1-B047-DecoratorMaster` | `HDVG:B047:RECORD_READY` | ⏳ G13 |
| B-048 | `CCSLL-L1-B048-ConfigEngineer` | `HDVG:B048:RECORD_READY` | ⏳ G13 |
| B-049 | `CCSLL-L1-B049-LoggingEngineer` | `HDVG:B049:RECORD_READY` | ⏳ G13 |
| B-050 | `CCSLL-L1-B050-SystemEngineer` + `CLL-L1-B050-LinuxPythonBridge` | `HDVG:B050:RECORD_READY` + `PHASE2:COMPLETE` | ⏳ G13 |

---

## Further Reading

- 📄 [`docs/ai-copilot-video-sandbox-creator.md`](ai-copilot-video-sandbox-creator.md) — ACVS video pipeline
- 📄 [`docs/creative-building-process.md`](creative-building-process.md) — 8-stage creative loop
- 📄 [`docs/QEP-B046-B050-phase2-batch5-quality-evidence-packet.md`](QEP-B046-B050-phase2-batch5-quality-evidence-packet.md) — Quality gates
- 🏠 [`README.md`](../README.md) — Encyclopedia home

# B-049: Logging — The Program's Memory

### logging module, levels, handlers, formatters, and Structured Logs

> *"print() is how you debug in development. logging is how you diagnose in production. Every print() statement is a lost opportunity to add timestamp, severity, source file, and line number. Every application that runs in the real world needs a structured log system. This book teaches you to build one."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Use Python's `logging` module with correct levels and loggers
2. Configure handlers (console, file, rotating file) and formatters
3. Use structured JSON logging for production systems
4. Integrate logging with decorators, exception handlers, and context
5. Build a `log_system.py` — a reusable structured logging library

**Prerequisite:** B-047 (decorators), B-048 (configuration)

**Build Artifact:** `~/developer-workspace/projects/python-foundations/log_system.py`

**Credential:** `CCSLL-L1-B049-LoggingEngineer` — on-chain on Base

---

## Chapter 1: Why Not print()?

```python
# ❌ print() — what you lose:
print("User logged in")
# No timestamp. No severity. No source file. No line number. No filtering.
# No way to turn it off in production. No way to send to a file and console.

# ✅ logging — what you gain:
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s:%(lineno)d — %(message)s",
)
log = logging.getLogger(__name__)

log.info("User logged in")
# 2026-08-28 12:00:00,000 INFO __main__:8 — User logged in

log.warning("API rate limit at 80%%")
log.error("Database connection failed")
log.debug("Processing record %d", 42)   # won't show at INFO level
```

---

## Chapter 2: Levels and Loggers

```python
import logging

# Five standard levels (increasing severity):
# DEBUG    10 — detailed diagnostic info
# INFO     20 — normal operational events
# WARNING  30 — something unexpected but not fatal
# ERROR    40 — an error occurred; operation failed
# CRITICAL 50 — application may not continue

# Named loggers — use __name__ for hierarchy
log = logging.getLogger(__name__)           # current module
db_log = logging.getLogger("myapp.db")     # database subsystem
api_log = logging.getLogger("myapp.api")   # API subsystem

# Root logger is the parent of all loggers
root = logging.getLogger()

# Logger hierarchy — parent/child relationship:
# root → myapp → myapp.db
# If myapp.db has no handlers, it propagates to myapp, then root
# Set level on root to control ALL loggers at once
logging.getLogger().setLevel(logging.WARNING)

# Or set per-subsystem:
logging.getLogger("myapp.db").setLevel(logging.DEBUG)
```

---

## Chapter 3: Handlers and Formatters

```python
import logging
import logging.handlers
from pathlib import Path

def configure_logging(log_dir: str = "/tmp") -> None:
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    # Formatter
    fmt = logging.Formatter(
        "%(asctime)s %(levelname)-8s %(name)s:%(lineno)d — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handler 1: Console (INFO and above)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(fmt)

    # Handler 2: File (all levels)
    log_path = Path(log_dir) / "app.log"
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)

    # Handler 3: Rotating file (max 5MB, keep 3 backups)
    rotating = logging.handlers.RotatingFileHandler(
        Path(log_dir) / "app_rotating.log",
        maxBytes=5 * 1024 * 1024,   # 5 MB
        backupCount=3,
        encoding="utf-8",
    )
    rotating.setLevel(logging.WARNING)
    rotating.setFormatter(fmt)

    root.addHandler(console)
    root.addHandler(file_handler)
    root.addHandler(rotating)

configure_logging()
log = logging.getLogger(__name__)
log.debug("This goes to file only")
log.info("This goes to console and file")
log.warning("This goes to all three handlers")
```

---

## Chapter 4: Structured JSON Logging

```python
import logging
import json
import traceback
from datetime import datetime, timezone

class JSONFormatter(logging.Formatter):
    """Format log records as single-line JSON for production log ingestion."""

    def format(self, record: logging.LogRecord) -> str:
        log_obj: dict[str, object] = {
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            "level":     record.levelname,
            "logger":    record.name,
            "message":   record.getMessage(),
            "module":    record.module,
            "function":  record.funcName,
            "line":      record.lineno,
        }
        # Include exception info if present
        if record.exc_info:
            log_obj["exception"] = {
                "type":       str(record.exc_info[0].__name__) if record.exc_info[0] else None,
                "message":    str(record.exc_info[1]),
                "traceback":  traceback.format_exception(*record.exc_info),
            }
        # Include extra fields passed to log calls
        for key, value in record.__dict__.items():
            if key not in logging.LogRecord.__dict__ and not key.startswith("_"):
                log_obj[key] = value
        return json.dumps(log_obj, default=str)

# Use it:
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.DEBUG)

log = logging.getLogger("myapp")
log.info("Request processed", extra={"user_id": 42, "duration_ms": 145})
# {"timestamp": "...", "level": "INFO", "message": "Request processed", "user_id": 42, ...}
```

---

## Chapter 5: contextvar and Context Logging

```python
import logging
from contextvars import ContextVar

# Store per-request context that automatically appears in all log lines
_request_id: ContextVar[str] = ContextVar("request_id", default="-")

class ContextFilter(logging.Filter):
    """Inject contextvar values into every log record."""
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = _request_id.get()  # type: ignore[attr-defined]
        return True

# Setup
log = logging.getLogger(__name__)
log.addFilter(ContextFilter())

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(request_id)s] %(levelname)s %(message)s"
))
log.addHandler(handler)
log.setLevel(logging.DEBUG)

# In a web request handler:
def handle_request(request_id: str) -> None:
    token = _request_id.set(request_id)
    try:
        log.info("Request started")
        log.info("Processing data")
        log.info("Request complete")
    finally:
        _request_id.reset(token)

handle_request("REQ-001")
handle_request("REQ-002")
# 2026-08-28 [REQ-001] INFO Request started
# 2026-08-28 [REQ-001] INFO Processing data
# ...
```

---

## Chapter 6: The Build — log_system.py

```python
#!/usr/bin/env python3
"""
log_system.py — B-049 Build Artifact

A reusable structured logging system for Python projects.
Provides console + rotating file logging with optional JSON format.

Usage:
    from log_system import setup_logging, get_logger
    setup_logging(level="DEBUG", log_dir="/var/log/myapp", json_format=True)
    log = get_logger(__name__)
    log.info("Server started", extra={"port": 8000})
"""
from __future__ import annotations

import json
import logging
import logging.handlers
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class JSONFormatter(logging.Formatter):
    """Single-line JSON log format for production ingestion."""

    _SKIP = frozenset(logging.LogRecord.__dict__) | {"message", "asctime"}

    def format(self, record: logging.LogRecord) -> str:
        obj: dict[str, object] = {
            "ts":       datetime.now(tz=timezone.utc).isoformat(),
            "level":    record.levelname,
            "logger":   record.name,
            "msg":      record.getMessage(),
            "module":   record.module,
            "fn":       record.funcName,
            "line":     record.lineno,
        }
        if record.exc_info:
            obj["exc"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "msg":  str(record.exc_info[1]),
                "tb":   traceback.format_exception(*record.exc_info),
            }
        for k, v in record.__dict__.items():
            if k not in self._SKIP and not k.startswith("_"):
                obj[k] = v
        return json.dumps(obj, default=str)


TEXT_FMT = "%(asctime)s %(levelname)-8s %(name)s:%(lineno)d — %(message)s"
DATE_FMT = "%Y-%m-%d %H:%M:%S"


def setup_logging(
    level: str = "INFO",
    log_dir: Optional[str] = None,
    json_format: bool = False,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
) -> None:
    """
    Configure root logger with console + optional rotating file handler.

    Args:
        level:        Minimum log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)
        log_dir:      Directory for log files. None = console only.
        json_format:  Use JSON formatter (production) or text (development)
        max_bytes:    Max log file size before rotation
        backup_count: Number of rotated files to keep
    """
    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Remove existing handlers
    root.handlers.clear()

    formatter: logging.Formatter = (
        JSONFormatter() if json_format
        else logging.Formatter(TEXT_FMT, datefmt=DATE_FMT)
    )

    # Console handler
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    root.addHandler(console)

    # File handler (rotating)
    if log_dir:
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(
            log_path / "app.log",
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)

    # Silence noisy third-party loggers
    for noisy in ("urllib3", "httpx", "asyncio"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger. Use __name__ for automatic module hierarchy."""
    return logging.getLogger(name)


def demo() -> None:
    setup_logging(level="DEBUG", log_dir="/tmp/lippytmai_logs", json_format=False)
    log = get_logger(__name__)

    log.debug("Debug message — detailed diagnostic")
    log.info("Application started successfully")
    log.warning("Config file not found, using defaults")
    log.error("Failed to connect to database")

    # Extra fields appear as key=value in structured logs
    log.info("Request processed", extra={"user_id": 42, "duration_ms": 123})

    # Exception logging
    try:
        result = 1 / 0
    except ZeroDivisionError:
        log.exception("Math error occurred")

    print("\n--- JSON format ---\n")
    setup_logging(level="INFO", json_format=True)
    log2 = get_logger("json_demo")
    log2.info("JSON log line", extra={"env": "production", "version": "1.0.0"})


if __name__ == "__main__":
    demo()
```

```bash
python3 ~/developer-workspace/projects/python-foundations/log_system.py
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-049 Verification ==="
python3 -c "
import logging, io

stream = io.StringIO()
handler = logging.StreamHandler(stream)
handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
log = logging.getLogger('test_b049')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

log.debug('debug msg')
log.info('info msg')
log.warning('warning msg')
log.error('error msg')

output = stream.getvalue()
print(output.strip())
assert 'WARNING' in output
assert 'ERROR' in output
print('✅ logging works')
"
```

---

## Further Reading

- 📄 [`docs/B-047-python-decorators-without-the-magic.md`](B-047-python-decorators-without-the-magic.md) — Logging decorator
- 📄 [`docs/B-048-environment-configuration-done-right.md`](B-048-environment-configuration-done-right.md) — LOG_LEVEL from config
- 📄 [`docs/B-050-python-plus-linux-the-power-combo.md`](B-050-python-plus-linux-the-power-combo.md) — Logs on Linux with systemd
- 🏠 [`README.md`](../README.md) — Encyclopedia home

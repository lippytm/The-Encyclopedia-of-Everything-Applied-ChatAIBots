# B-029: Dictionaries — The Data Swiss Army Knife

### dict, JSON, .get(), and the Key-Value Mindset

> *"A dictionary in Python is what a JSON object is on the web, what a hash map is in computer science, and what a filing cabinet is in an office. The key-value pair is one of the most powerful data structures ever invented. Once you understand it, you see it everywhere."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Create, access, modify, and iterate over Python dictionaries
2. Use `.get()`, `.setdefault()`, `.update()`, and `.pop()` safely
3. Convert between Python dicts and JSON
4. Use nested dicts to model real-world data
5. Build a `config-reader.py` that loads and validates JSON config files

**Prerequisite:** B-026, B-027, B-028

**Build Artifact:** `~/developer-workspace/projects/python-foundations/config_reader.py`

**Credential:** `CCSLL-L1-B029-DataEngineer` — on-chain on Base

---

## Chapter 1: Creating and Accessing Dictionaries

```python
# A dict maps keys to values
user = {
    "name":  "Charles Lipshay",
    "role":  "engineer",
    "level": 5,
    "active": True,
}

# Access by key
print(user["name"])      # Charles Lipshay
print(user["level"])     # 5

# KeyError if key doesn't exist
# print(user["email"])   # KeyError!

# Safe access with .get() — returns None or a default
print(user.get("email"))              # None
print(user.get("email", "not set"))   # not set
print(user.get("name", "unknown"))    # Charles Lipshay

# Check if key exists
if "role" in user:
    print(f"Role: {user['role']}")

# All keys, values, items
print(user.keys())    # dict_keys([...])
print(user.values())  # dict_values([...])
print(user.items())   # dict_items([(key, val), ...])
```

---

## Chapter 2: Modifying Dictionaries

```python
config = {"debug": False, "port": 8080}

# Add or update a key
config["host"] = "localhost"
config["port"] = 9000         # updates existing

# Update multiple keys at once
config.update({"debug": True, "workers": 4})

# Remove a key (and get its value)
old_port = config.pop("port", None)    # None if missing — safe
print(old_port)   # 9000

# Remove and get last inserted item (Python 3.7+, dicts are ordered)
key, value = config.popitem()

# Delete a key
del config["debug"]

# Clear everything
# config.clear()

# setdefault — set only if key is missing
config.setdefault("timeout", 30)    # sets timeout = 30
config.setdefault("timeout", 60)    # ignored — already set
print(config["timeout"])            # 30
```

---

## Chapter 3: Iterating Over Dictionaries

```python
book_scores = {
    "B-026": 94,
    "B-027": 88,
    "B-028": 91,
}

# Iterate over keys (default)
for key in book_scores:
    print(key)

# Iterate over values
for score in book_scores.values():
    print(score)

# Iterate over key-value pairs (most common)
for book_id, score in book_scores.items():
    grade = "A" if score >= 90 else "B" if score >= 80 else "C"
    print(f"{book_id}: {score} ({grade})")

# Dict comprehension — build a new dict from iteration
passing = {k: v for k, v in book_scores.items() if v >= 90}
print(passing)  # {'B-026': 94, 'B-028': 91}
```

---

## Chapter 4: Nested Dictionaries

```python
# ACSS agent registry (simplified)
agents = {
    "lippytmai": {
        "type":  "teacher",
        "mode":  "teach",
        "model": "gpt-4o",
        "repos": ["ChatAIBots", "ADA", "ACVS"],
    },
    "lippytm": {
        "type":  "builder",
        "mode":  "build",
        "model": "gpt-4o",
        "repos": ["all"],
    },
}

# Access nested data
print(agents["lippytmai"]["model"])        # gpt-4o
print(agents["lippytmai"]["repos"][0])     # ChatAIBots

# Safe nested access
print(agents.get("lippy-killjoy", {}).get("model", "not found"))  # not found

# Iterate over nested
for agent_id, info in agents.items():
    print(f"{agent_id}: {info['type']} | {info['model']}")
```

---

## Chapter 5: Python Dicts ↔ JSON

JSON (JavaScript Object Notation) is the universal data exchange format. Python dicts map directly:

```python
import json

# Dict to JSON string
config = {"host": "localhost", "port": 8080, "debug": True}
json_string = json.dumps(config)
print(json_string)
# '{"host": "localhost", "port": 8080, "debug": true}'

# Pretty-printed JSON
pretty = json.dumps(config, indent=2)
print(pretty)

# JSON string to dict
raw = '{"name": "Charles", "level": 5}'
data = json.loads(raw)
print(data["name"])   # Charles

# Read JSON from a file
with open("config.json", "r") as f:
    loaded = json.load(f)

# Write dict to a JSON file
with open("output.json", "w") as f:
    json.dump(config, f, indent=2)
```

---

## Chapter 6: The Build — Config Reader

```python
#!/usr/bin/env python3
"""
config_reader.py — B-029 Build Artifact

Loads, validates, and provides typed access to a JSON config file.
Demonstrates: dicts, JSON, .get(), nested access, type checking.
"""
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


DEFAULT_CONFIG: Dict[str, Any] = {
    "app_name":    "lippytmai",
    "version":     "1.0.0",
    "environment": "development",
    "server": {
        "host":    "localhost",
        "port":    8080,
        "workers": 4,
        "debug":   True,
    },
    "logging": {
        "level":   "INFO",
        "file":    "logs/app.log",
    },
    "credentials": {},
}

REQUIRED_KEYS = ["app_name", "version", "server"]


class ConfigReader:
    """Load and validate a JSON configuration file."""

    def __init__(self, config_path: Optional[str] = None) -> None:
        self._config: Dict[str, Any] = dict(DEFAULT_CONFIG)
        if config_path and Path(config_path).exists():
            self._load(config_path)
        self._validate()

    def _load(self, path: str) -> None:
        """Load config from a JSON file, merging over defaults."""
        with open(path, "r") as f:
            user_config = json.load(f)
        # Deep merge: update top-level keys, then nested dicts
        for key, value in user_config.items():
            if isinstance(value, dict) and key in self._config:
                self._config[key].update(value)
            else:
                self._config[key] = value
        print(f"[config] Loaded from {path}")

    def _validate(self) -> None:
        """Raise ValueError if required keys are missing."""
        for key in REQUIRED_KEYS:
            if key not in self._config:
                raise ValueError(f"Missing required config key: '{key}'")

    def get(self, *keys: str, default: Any = None) -> Any:
        """Get a config value by dotted path.

        Example:
            config.get("server", "port")   → 8080
            config.get("missing", "key")   → None (or default)
        """
        value = self._config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, default)
            else:
                return default
        return value

    def __repr__(self) -> str:
        return f"ConfigReader({json.dumps(self._config, indent=2)})"


def main() -> None:
    config = ConfigReader()
    print("=== Config Loaded ===")
    print(f"App:         {config.get('app_name')}")
    print(f"Version:     {config.get('version')}")
    print(f"Environment: {config.get('environment')}")
    print(f"Server:      {config.get('server', 'host')}:{config.get('server', 'port')}")
    print(f"Debug:       {config.get('server', 'debug')}")
    print(f"Log level:   {config.get('logging', 'level')}")
    print(f"Missing key: {config.get('does_not_exist', default='N/A')}")


if __name__ == "__main__":
    main()
```

```bash
python3 ~/developer-workspace/projects/python-foundations/config_reader.py
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-029 Verification ==="
python3 -c "
import json

# Dict creation and access
data = {'book': 'B-029', 'level': 1, 'credential': 'CCSLL-L1-B029-DataEngineer'}
print('Book:', data.get('book'))
print('Missing key:', data.get('author', 'not set'))

# JSON roundtrip
json_str = json.dumps(data, indent=2)
recovered = json.loads(json_str)
print('JSON roundtrip:', recovered['credential'])

# Dict comprehension
scores = {'A': 95, 'B': 82, 'C': 71, 'D': 55}
passing = {k: v for k, v in scores.items() if v >= 60}
print('Passing:', passing)
"
python3 ~/developer-workspace/projects/python-foundations/config_reader.py
```

---

## Further Reading

- 📄 [`docs/B-030-reading-and-writing-files.md`](B-030-reading-and-writing-files.md) — Reading JSON config files from disk
- 📄 [`docs/B-028-functions-that-do-one-thing-well.md`](B-028-functions-that-do-one-thing-well.md) — Functions used with dict processing
- 📄 [`docs/B-011-environment-variables-and-secrets.md`](B-011-environment-variables-and-secrets.md) — Config loading patterns from the Linux series
- 🏠 [`README.md`](../README.md) — Encyclopedia home

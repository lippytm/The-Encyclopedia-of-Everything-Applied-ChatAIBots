# B-048: Environment Configuration Done Right

### python-dotenv, pydantic-settings, and Secrets That Never End Up in Git

> *"The #1 cause of security breaches in developer projects: API keys hardcoded in source code, then committed to a public repository. The fix is simple and takes 10 minutes to learn. .env files keep secrets out of code. pydantic-settings validates your configuration at startup. Once you do this right, you never do it wrong again."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Use `.env` files to store secrets and configuration outside source code
2. Load `.env` values with `python-dotenv`
3. Validate and type-check all configuration with `pydantic-settings`
4. Use environment-specific configs (dev/staging/prod)
5. Build a `config.py` system used as a reusable configuration management module

**Prerequisite:** B-036 (type hints), B-033 (Pydantic is OOP-based)

**Build Artifact:** `~/developer-workspace/projects/python-foundations/config.py`

**Credential:** `CCSLL-L1-B048-ConfigEngineer` — on-chain on Base

---

## Chapter 1: The Problem with Hardcoded Config

```python
# ❌ DANGEROUS — never do this
API_KEY = "sk-prod-abc123XYZ789"           # hardcoded secret
DATABASE_URL = "******prod.db:5432/mydb"  # exposed credentials
DEBUG = True                                # prod settings in code

# Also wrong: .env file committed to git
# If .env is in your repo, it's the same as hardcoding.

# ✅ CORRECT PATTERN:
# 1. Store secrets in .env (or OS environment variables)
# 2. .env is listed in .gitignore — NEVER committed
# 3. Read with python-dotenv or pydantic-settings
# 4. Validate types at startup — crash early if config is wrong
```

---

## Chapter 2: python-dotenv Basics

```bash
# .env file — never commit this
API_KEY=sk-dev-abc123
DATABASE_URL=postgresql://localhost:5432/mydb
DEBUG=true
PORT=8000
MAX_RETRIES=3
```

```python
from dotenv import load_dotenv
import os

# Load .env into os.environ (does nothing if file missing)
load_dotenv()

# Access values
api_key = os.getenv("API_KEY")
debug   = os.getenv("DEBUG", "false").lower() == "true"
port    = int(os.getenv("PORT", "8000"))

print(f"API key starts with: {(api_key or '')[:8]}...")
print(f"Debug: {debug}")
print(f"Port: {port}")

# load_dotenv won't override existing environment variables
# Perfect for Docker/CI where env vars are injected by the platform
```

```python
# .gitignore — add these lines
# .env
# .env.local
# .env.*.local
# *.pem
# *.key
```

---

## Chapter 3: pydantic-settings — Validated Configuration

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr
from typing import Literal

class Settings(BaseSettings):
    """Application configuration — auto-loaded from .env and environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # API credentials — SecretStr prevents accidental logging
    api_key: SecretStr = Field(..., description="Primary API key")
    database_url: SecretStr = Field(..., description="Database connection string")

    # Application settings with defaults and validation
    debug: bool = False
    port: int = Field(default=8000, ge=1, le=65535)
    max_retries: int = Field(default=3, ge=1, le=10)
    environment: Literal["development", "staging", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

# Instantiate once at startup — crashes immediately on missing/invalid config
settings = Settings()

# Access values
print(f"Env: {settings.environment}")
print(f"Port: {settings.port}")
print(f"Debug: {settings.debug}")
# SecretStr protects secrets in logs/reprs:
print(f"API key repr: {settings.api_key}")  # '**********'
# Access actual value only when needed:
print(f"API key: {settings.api_key.get_secret_value()[:8]}...")
```

---

## Chapter 4: Environment-Specific Configuration

```bash
# .env.development
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=postgresql://localhost:5432/dev_db
API_KEY=sk-dev-localkey123

# .env.production
DEBUG=false
LOG_LEVEL=WARNING
DATABASE_URL=postgresql://prod-server:5432/prod_db
API_KEY=   # ← injected by deployment platform, NOT here
```

```python
import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

def get_env_file() -> str:
    env = os.getenv("APP_ENV", "development")
    env_file = Path(f".env.{env}")
    if env_file.exists():
        return str(env_file)
    return ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=get_env_file(),
        env_file_encoding="utf-8",
    )
    debug: bool = False
    log_level: str = "INFO"
    database_url: str = "sqlite:///./local.db"
    api_key: str = ""
    environment: str = os.getenv("APP_ENV", "development")

# Run with: APP_ENV=production python3 app.py
settings = Settings()
```

---

## Chapter 5: Settings Patterns

```python
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    api_key: str = "test-key"
    debug: bool = False
    port: int = 8000

@lru_cache
def get_settings() -> Settings:
    """Return the singleton settings instance (cached after first call)."""
    return Settings()

# Usage throughout the codebase:
def start_server() -> None:
    cfg = get_settings()
    print(f"Starting on port {cfg.port}, debug={cfg.debug}")

# In tests — override settings easily:
def test_with_override() -> None:
    import os
    os.environ["PORT"] = "9999"
    os.environ["DEBUG"] = "true"
    get_settings.cache_clear()   # clear cached singleton
    cfg = get_settings()
    assert cfg.port == 9999
    assert cfg.debug is True
    get_settings.cache_clear()   # cleanup
```

---

## Chapter 6: The Build — config.py

```python
#!/usr/bin/env python3
"""
config.py — B-048 Build Artifact

A production-ready configuration management system using pydantic-settings.
Create a .env file and import this module from any Python project.

Usage:
    pip install pydantic-settings python-dotenv
    from config import get_settings
    cfg = get_settings()
    print(cfg.port)
"""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _env_file() -> str:
    env = os.getenv("APP_ENV", "development")
    candidates = [f".env.{env}", f".env.{env}.local", ".env.local", ".env"]
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    return ".env"


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables and .env files.

    Priority (highest → lowest):
        1. OS environment variables
        2. .env.{APP_ENV}.local
        3. .env.local
        4. .env.{APP_ENV}
        5. .env
        6. Field defaults
    """

    model_config = SettingsConfigDict(
        env_file=_env_file(),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Identity
    app_name: str = Field("lippytmai-app", description="Application name")
    app_version: str = Field("1.0.0", description="Application version")
    environment: Literal["development", "staging", "production"] = "development"

    # Server
    host: str = Field("0.0.0.0", description="Bind host")
    port: int = Field(8000, ge=1, le=65535, description="Bind port")
    debug: bool = Field(False, description="Enable debug mode")

    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_format: str = "%(asctime)s %(levelname)s %(name)s: %(message)s"

    # Secrets (SecretStr hides values in repr/logs)
    api_key: SecretStr = Field(default=SecretStr("dev-key"), description="API key")
    database_url: SecretStr = Field(
        default=SecretStr("sqlite:///./local.db"),
        description="Database URL",
    )

    # Rate limits and performance
    max_retries: int = Field(3, ge=1, le=10)
    request_timeout: float = Field(30.0, gt=0)
    max_connections: int = Field(10, ge=1)

    @field_validator("environment")
    @classmethod
    def validate_env(cls, v: str) -> str:
        if v == "production" and os.getenv("API_KEY", "").startswith("dev-"):
            raise ValueError("Cannot use dev API key in production")
        return v

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        return self.environment == "development"

    def summary(self) -> dict[str, object]:
        """Return non-secret config summary safe for logging."""
        return {
            "app_name": self.app_name,
            "version": self.app_version,
            "environment": self.environment,
            "host": self.host,
            "port": self.port,
            "debug": self.debug,
            "log_level": self.log_level,
        }


@lru_cache
def get_settings() -> Settings:
    """Return the cached singleton Settings instance."""
    return Settings()


def demo() -> None:
    cfg = get_settings()
    print("\n=== Configuration Summary ===\n")
    for key, value in cfg.summary().items():
        print(f"  {key:<20} {value}")
    print(f"\n  {'is_production':<20} {cfg.is_production}")
    print(f"  {'api_key (repr)':<20} {cfg.api_key}")  # masked
    print(f"\n  Loaded from: {_env_file()}\n")


if __name__ == "__main__":
    demo()
```

```bash
pip install pydantic-settings python-dotenv
python3 ~/developer-workspace/projects/python-foundations/config.py
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-048 Verification ==="
python3 -c "
import os
os.environ['PORT'] = '9000'
os.environ['DEBUG'] = 'true'
os.environ['APP_NAME'] = 'test-app'

from pydantic_settings import BaseSettings

class Cfg(BaseSettings):
    port: int = 8000
    debug: bool = False
    app_name: str = 'default'

cfg = Cfg()
print(f'Port:  {cfg.port}')
print(f'Debug: {cfg.debug}')
print(f'Name:  {cfg.app_name}')
assert cfg.port == 9000
assert cfg.debug is True
print('✅ pydantic-settings works')
"
```

---

## Further Reading

- 📄 [`docs/B-011-environment-variables-and-secrets.md`](B-011-environment-variables-and-secrets.md) — Linux env vars foundation
- 📄 [`docs/B-042-your-first-rest-api.md`](B-042-your-first-rest-api.md) — FastAPI uses Settings via Depends()
- 📄 [`docs/B-049-logging-the-programs-memory.md`](B-049-logging-the-programs-memory.md) — Logging config from Settings
- 🏠 [`README.md`](../README.md) — Encyclopedia home

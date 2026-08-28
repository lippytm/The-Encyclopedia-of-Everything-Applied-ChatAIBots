# B-053: Environment Variables and Security

> *"The fastest way to leak your API keys is to commit them to Git. The fastest way to prevent that is already built into Python."*

---

## Learning Objectives

By the end of this book you will:

1. Understand why secrets must never be hardcoded or committed to version control
2. Apply a layered secrets management strategy (local → CI → production)
3. Use `python-dotenv`, `pydantic-settings`, and `SecretStr` securely
4. Detect and remediate accidental secret leaks with `git-secrets` and `truffleHog`
5. Apply the same patterns inside Docker and CI/CD environments
6. Earn the `CCSLL-L1-B053-SecureConfigEngineer` credential

---

## Chapter 1: The Anatomy of a Leaked Secret

Every week, secrets are accidentally committed to GitHub — API keys, database passwords, tokens. The consequences:

- Automated bots scrape GitHub and abuse keys within **seconds** of a push
- Keys rotated too slowly mean real data breaches
- Many cloud providers (AWS, GCP) have bot detectors and will email you — but only after the damage

The root cause is almost always the same: hardcoded strings or `.env` files committed to git.

---

## Chapter 2: What You Must Never Do

```python
# ❌ NEVER DO THIS
import openai

openai.api_key = "sk-proj-abc123XYZ..."  # hardcoded API key

# ❌ NEVER DO THIS EITHER
DATABASE_URL = "******ss@prod-db.example.com/myapp"
```

```bash
# ❌ NEVER COMMIT .env
git add .env
git commit -m "add config"   # <-- leaked forever in git history
```

---

## Chapter 3: The Correct Pattern — Environment Variables

```python
from __future__ import annotations
import os

# ✅ Read from environment — never hardcode
openai_key: str | None = os.environ.get("OPENAI_API_KEY")
if not openai_key:
    raise RuntimeError("OPENAI_API_KEY environment variable is required")
```

Your `.env` file lives only on your machine and in CI secrets — **never in git**:

```bash
# .env  (add to .gitignore BEFORE creating this file)
OPENAI_API_KEY=sk-proj-...
DATABASE_URL=******localhost:5432/myapp
SECRET_KEY=random-32-char-string-here
```

```bash
# .gitignore — always include these
.env
.env.*
!.env.example
```

---

## Chapter 4: python-dotenv and pydantic-settings (Secure)

```python
from __future__ import annotations
from functools import lru_cache
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Public config — safe to log
    app_name: str = "lippytmai"
    debug: bool = False
    log_level: str = "INFO"

    # Secrets — NEVER log these
    openai_api_key: SecretStr
    database_url: SecretStr
    secret_key: SecretStr

    def safe_summary(self) -> dict[str, object]:
        """Return a settings summary that is safe to log."""
        return {
            "app_name": self.app_name,
            "debug": self.debug,
            "log_level": self.log_level,
            "openai_api_key": "***SET***" if self.openai_api_key else "NOT SET",
            "database_url": "***SET***" if self.database_url else "NOT SET",
        }

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings singleton."""
    return Settings()
```

`SecretStr` values:
- Return `**********` when printed or logged
- Require `.get_secret_value()` to access the actual string
- Prevent accidental exposure in tracebacks and debug output

---

## Chapter 5: Secrets in Docker and CI/CD

**Docker:**
```bash
# ✅ Inject at runtime via --env-file
docker run --env-file .env myapp:latest

# ✅ Or individual -e flags
docker run -e OPENAI_API_KEY="${OPENAI_API_KEY}" myapp:latest

# ❌ Never bake secrets into the image
# RUN echo "sk-proj-..." > /app/.env   <-- visible in image history!
```

**GitHub Actions:**
```yaml
# .github/workflows/deploy.yml
jobs:
  deploy:
    steps:
      - name: Run app
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: python3 app.py
```

Secrets stored in GitHub → Settings → Secrets and Variables → Actions are **never** logged and are masked in output.

---

## Chapter 6: Detecting Leaked Secrets

```bash
# Install truffleHog for git history scanning
pip install trufflehog3

# Scan a local repo for secrets in all commits
trufflehog3 filesystem .

# Scan a GitHub repo
trufflehog3 github --repo https://github.com/lippytm/my-repo

# Pre-commit hook with detect-secrets
pip install detect-secrets
detect-secrets scan > .secrets.baseline
detect-secrets audit .secrets.baseline
```

```bash
# If you accidentally committed a secret:
# 1. Revoke the key immediately (before anything else)
# 2. Remove from git history with BFG Repo-Cleaner
# 3. Force-push the cleaned history
# 4. Rotate all other credentials on that system
```

---

## Chapter 7: Proof of Work — Secure Config System

Build `secure_config.py`:

```python
from __future__ import annotations
import sys
from functools import lru_cache
from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
    """Production-ready secure configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    app_name: str = "lippytmai"
    debug: bool = False
    log_level: str = "INFO"
    openai_api_key: SecretStr = SecretStr("")
    database_url: SecretStr = SecretStr("sqlite:///./dev.db")
    secret_key: SecretStr = SecretStr("dev-only-not-for-production")

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in allowed:
            raise ValueError(f"log_level must be one of {allowed}")
        return v.upper()

    def print_safe_summary(self) -> None:
        """Print config summary — secrets masked."""
        print(f"App: {self.app_name}")
        print(f"Debug: {self.debug}")
        print(f"Log level: {self.log_level}")
        print(f"OpenAI key: {'SET' if self.openai_api_key.get_secret_value() else 'NOT SET'}")
        print(f"DB URL: {'SET' if self.database_url.get_secret_value() else 'NOT SET'}")
        print(f"Secret key: {'CUSTOM' if self.secret_key.get_secret_value() != 'dev-only-not-for-production' else 'DEFAULT (unsafe for prod)'}")

@lru_cache(maxsize=1)
def get_config() -> AppConfig:
    return AppConfig()

if __name__ == "__main__":
    config = get_config()
    config.print_safe_summary()
    if config.debug:
        print("\n[WARNING] Debug mode is ON — never enable in production")
    sys.exit(0)
```

```bash
# Run without .env (uses defaults)
python3 secure_config.py

# Run with a .env file
echo 'APP_NAME=my-project\nDEBUG=true\nLOG_LEVEL=DEBUG' > .env
python3 secure_config.py
```

**Credential earned:** `CCSLL-L1-B053-SecureConfigEngineer`

---

## Further Reading

- 📄 [`docs/B-048-environment-configuration-done-right.md`](B-048-environment-configuration-done-right.md) — pydantic-settings deep dive
- 📄 [`docs/B-052-your-first-docker-container.md`](B-052-your-first-docker-container.md) — Secrets in containers
- 📄 [`docs/ai-clone-engine-swarms.md`](ai-clone-engine-swarms.md) — ACSS security layer
- 🏠 [`README.md`](../README.md) — Encyclopedia home

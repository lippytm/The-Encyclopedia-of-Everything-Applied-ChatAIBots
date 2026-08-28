# B-011: Environment Variables and Secrets

### The Rule Every Developer Must Know: Secrets Never in Code

> *"The most expensive mistake in software engineering is a single line: API_KEY='sk-prod-abc123'. Committed to a public GitHub repository. Sitting in the history forever, even after you delete it. This book teaches you the pattern that prevents that mistake — and makes your code work in any environment without changing a line."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Explain what environment variables are and why they exist
2. Set, read, and export environment variables in Bash
3. Use `.env` files with `python-dotenv` and `direnv`
4. Understand the difference between configuration and secrets
5. Build a secure configuration loader that never hardcodes credentials

**Prerequisite:** B-001 through B-010

**Build Artifact:** A Python config loader module + `.env` file + `.env.example` template + updated `.gitignore`

**Credential:** `CCSLL-L0-B011-SecretKeeper` — on-chain on Base

---

## Chapter 1: What Are Environment Variables?

Your program runs in an **environment** — a set of named values that it can read at startup. Environment variables are key-value pairs, set outside your code, that your code can access.

```bash
# See all environment variables currently set
env
printenv

# See a specific one
echo $HOME
echo $USER
echo $PATH
```

The `$PATH` variable is a classic example: it's a colon-separated list of directories where your shell looks for commands. When you type `python3`, the shell searches every directory in `$PATH` until it finds it.

*[Reality — environment variables are the standard mechanism for 12-Factor App configuration, used by every major cloud platform and CI/CD system]*

---

## Chapter 2: Setting Environment Variables

```bash
# Set for the current shell session (disappears when terminal closes)
export DATABASE_URL="postgresql://localhost:5432/mydb"
export API_KEY="test-key-only-local"

# Read it back
echo $DATABASE_URL

# Set for a single command only
DATABASE_URL="test-db" python3 app.py

# Make permanent: add to ~/.bashrc or ~/.zshrc
echo 'export EDITOR="nano"' >> ~/.bashrc
source ~/.bashrc

# Unset a variable
unset API_KEY

# See if a variable is set
[ -z "$API_KEY" ] && echo "API_KEY not set"
```

---

## Chapter 3: The .env File Pattern

For development, you store variables in a `.env` file — a simple key=value text file. The crucial rule: **`.env` is never committed to Git**.

```bash
# .env — your local secrets (NEVER commit this)
DATABASE_URL=postgresql://localhost:5432/devdb
SECRET_KEY=dev-secret-key-change-in-production
API_KEY=sk-dev-test-key-not-real
DEBUG=true
PORT=8000
```

```bash
# .env.example — the template you DO commit (no real values)
DATABASE_URL=postgresql://localhost:5432/yourdb
SECRET_KEY=replace-with-random-secret
API_KEY=replace-with-your-api-key
DEBUG=false
PORT=8000
```

```bash
# .gitignore — ensure .env is ALWAYS ignored
cat >> .gitignore << 'EOF'
.env
.env.local
.env.*.local
*.secret
secrets/
EOF
```

*[Reality — the `.env` / `.env.example` pattern is a universal convention across Python, Node.js, Ruby, Go, and virtually every modern web framework]*

---

## Chapter 4: python-dotenv

Load `.env` files into Python applications:

```bash
source venv/bin/activate
pip install python-dotenv
```

```python
# config.py — B-011 Build Artifact
"""
Secure configuration loader using environment variables and .env files.
Never hardcodes credentials. Always validates required variables at startup.
"""
import os
import sys
from typing import Optional
from dotenv import load_dotenv

load_dotenv()  # loads .env file into os.environ

class Config:
    """Application configuration loaded from environment variables."""

    # Required — will raise at startup if missing
    DATABASE_URL: str = os.environ["DATABASE_URL"]
    SECRET_KEY: str = os.environ["SECRET_KEY"]

    # Optional with defaults
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    PORT: int = int(os.getenv("PORT", "8000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Optional — may be None
    API_KEY: Optional[str] = os.getenv("API_KEY")

    @classmethod
    def validate(cls) -> None:
        """Validate config at startup — fail fast if something is missing."""
        required = ["DATABASE_URL", "SECRET_KEY"]
        missing = [key for key in required if not os.getenv(key)]
        if missing:
            print(f"FATAL: Missing required environment variables: {missing}")
            print("Copy .env.example to .env and fill in the values.")
            sys.exit(1)

    @classmethod
    def summary(cls) -> dict:
        """Safe summary — never includes actual secret values."""
        return {
            "DATABASE_URL": cls.DATABASE_URL[:20] + "..." if cls.DATABASE_URL else None,
            "SECRET_KEY": "***set***" if cls.SECRET_KEY else "***MISSING***",
            "DEBUG": cls.DEBUG,
            "PORT": cls.PORT,
            "LOG_LEVEL": cls.LOG_LEVEL,
            "API_KEY": "***set***" if cls.API_KEY else None,
        }


if __name__ == "__main__":
    Config.validate()
    print("Configuration loaded successfully:")
    for key, value in Config.summary().items():
        print(f"  {key}: {value}")
```

---

## Chapter 5: direnv — Per-Directory Environments

`direnv` automatically loads `.env` files when you `cd` into a directory:

```bash
# Install
sudo apt install direnv   # Ubuntu/Debian
sudo pacman -S direnv     # Arch

# Add to ~/.bashrc
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
source ~/.bashrc

# Allow a directory's .env file
cd ~/developer-workspace/project-alpha
direnv allow .
# Now .env is loaded automatically whenever you enter this directory
```

---

## Chapter 6: The Build

```bash
# Step 1: Create .env
cd ~/developer-workspace/project-alpha
cat > .env << 'EOF'
DATABASE_URL=postgresql://localhost:5432/devdb
SECRET_KEY=dev-not-for-production-replace-me
API_KEY=test-api-key-local-only
DEBUG=true
PORT=8000
EOF

# Step 2: Create .env.example (safe to commit)
cat > .env.example << 'EOF'
DATABASE_URL=postgresql://localhost:5432/yourdb
SECRET_KEY=replace-with-random-secret-min-32-chars
API_KEY=replace-with-your-api-key
DEBUG=false
PORT=8000
EOF

# Step 3: Update .gitignore
echo '.env' >> .gitignore

# Step 4: Install python-dotenv and write config.py
source venv/bin/activate
pip install python-dotenv
# (save config.py from Chapter 4 to src/config.py)

# Step 5: Run the config loader
python3 src/config.py

# Step 6: Verify .env is gitignored
git status
# .env should NOT appear in git status
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-011 Build Verification ==="
echo ".env file exists (should NOT be shown in git status):"
git -C ~/developer-workspace/project-alpha status | grep -v ".env" | head -10

echo ""
echo ".env.example exists and is tracked:"
git -C ~/developer-workspace/project-alpha status .env.example

echo ""
echo "Config loader runs:"
cd ~/developer-workspace/project-alpha && python3 src/config.py
```

---

## Further Reading

- 📄 [`docs/B-008-files-that-never-get-lost.md`](B-008-files-that-never-get-lost.md) — Git: why .env must be in .gitignore
- 📄 [`docs/B-012-the-container-that-held-everything.md`](B-012-the-container-that-held-everything.md) — Docker uses the same env var pattern
- 📄 [`docs/linux-blockchain-educational-ecosystem.md`](linux-blockchain-educational-ecosystem.md) — Blockchain nodes use env vars for RPC keys
- 🏠 [`README.md`](../README.md) — Encyclopedia home

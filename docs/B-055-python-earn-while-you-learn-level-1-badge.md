# B-055: Python Earn-while-you-Learn: Level 1 Badge

> *"A credential means nothing if you can't prove it. A portfolio means everything because the proof is the work."*

---

## Learning Objectives

By the end of this book you will:

1. Synthesize everything learned in Phase 2 (B-026–B-055) into a single deployable project
2. Apply the full CCSLL L1 stack: types, testing, logging, config, async, CLI, Docker, Git
3. Submit your portfolio for peer review and AI-assisted evaluation
4. Understand how the lippytm.ai credential system works
5. Earn the `CCSLL-L1-BADGE-PythonFoundations` SkillBadge — your Python Level 1 credential

---

## Chapter 1: What You've Mastered in Phase 2

Phase 2 covered 30 books across 6 batches. Here is what you now know:

| Batch | Books | Skills |
|---|---|---|
| Batch 6 | B-026–B-030 | Python basics: programs, lists, functions, dicts, files |
| Batch 7 | B-031–B-035 | Exceptions, HTTP APIs, OOP, pytest, virtual environments |
| Batch 8 | B-036–B-040 | Type hints, datetime, regex, SQLite, automation scripts |
| Batch 9 | B-041–B-045 | Web scraping, FastAPI, async, packages, CSV/pandas |
| Batch 10 | B-046–B-050 | CLI tools, decorators, config, logging, Python+Linux |
| Batch 11 | B-051–B-055 | Git+Python, Docker, secrets, debugging, this capstone |

That is **30 books, 30 build artifacts, 30 individual credentials** — and now one SkillBadge to prove the whole stack.

---

## Chapter 2: The Capstone Project — lippytmai Portfolio CLI

Build a CLI tool called `portfolio` that:

1. **Lists** all your earned CCSLL credentials (reads from a local JSON registry)
2. **Verifies** a credential by checking its proof-of-work artifact exists
3. **Generates** a portfolio Markdown file ready to share
4. **Submits** a portfolio package (ZIP) to a local ADA endpoint

This project intentionally uses every skill from Phase 2.

---

## Chapter 3: Project Structure

```
portfolio/
├── pyproject.toml
├── .env.example
├── Dockerfile
├── .dockerignore
├── src/
│   └── portfolio/
│       ├── __init__.py
│       ├── config.py          # pydantic-settings (B-048/B-053)
│       ├── models.py          # dataclasses + type hints (B-036)
│       ├── registry.py        # JSON credential registry (B-039/B-040)
│       ├── verifier.py        # artifact verification (B-031/B-054)
│       ├── generator.py       # Markdown generator (B-037/B-038)
│       ├── cli.py             # typer CLI (B-046)
│       └── logger.py          # structured logging (B-049)
└── tests/
    ├── test_registry.py       # pytest (B-034)
    └── test_verifier.py
```

---

## Chapter 4: The Core Models

```python
# src/portfolio/models.py
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class CredentialStatus(Enum):
    EARNED = "earned"
    PENDING = "pending"
    UNVERIFIED = "unverified"

@dataclass
class Credential:
    """A single earned credential from the CCSLL system."""
    id: str                              # e.g. CCSLL-L1-B026-PythonFirstSteps
    book_id: str                         # e.g. B-026
    title: str
    library: str                         # CCSLL, CLL, CBSLL, CSEL
    level: int
    earned_at: datetime
    proof_artifact: str                  # path to build artifact
    status: CredentialStatus = CredentialStatus.PENDING

@dataclass
class Portfolio:
    """A complete L1 credential portfolio."""
    owner: str
    generated_at: datetime = field(default_factory=datetime.now)
    credentials: list[Credential] = field(default_factory=list)

    @property
    def earned_count(self) -> int:
        return sum(1 for c in self.credentials if c.status == CredentialStatus.EARNED)

    @property
    def completion_pct(self) -> float:
        if not self.credentials:
            return 0.0
        return (self.earned_count / len(self.credentials)) * 100
```

---

## Chapter 5: The Registry and Verifier

```python
# src/portfolio/registry.py
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from .models import Credential, CredentialStatus

def load_registry(path: Path) -> list[Credential]:
    """Load credential registry from a JSON file."""
    if not path.exists():
        return []
    with path.open() as f:
        data = json.load(f)
    return [
        Credential(
            id=item["id"],
            book_id=item["book_id"],
            title=item["title"],
            library=item["library"],
            level=item["level"],
            earned_at=datetime.fromisoformat(item["earned_at"]),
            proof_artifact=item["proof_artifact"],
            status=CredentialStatus(item.get("status", "pending")),
        )
        for item in data
    ]
```

```python
# src/portfolio/verifier.py
from __future__ import annotations
import logging
from pathlib import Path
from .models import Credential, CredentialStatus

logger = logging.getLogger(__name__)

def verify_credential(credential: Credential, base_path: Path) -> CredentialStatus:
    """Verify a credential by checking its proof artifact exists."""
    artifact = base_path / credential.proof_artifact
    if artifact.exists():
        logger.info("Credential verified: %s", credential.id)
        return CredentialStatus.EARNED
    logger.warning("Artifact not found for %s: %s", credential.id, artifact)
    return CredentialStatus.UNVERIFIED
```

---

## Chapter 6: The CLI

```python
# src/portfolio/cli.py
from __future__ import annotations
import json
from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table
from .registry import load_registry
from .verifier import verify_credential
from .models import CredentialStatus

app = typer.Typer(name="portfolio", help="lippytmai CCSLL L1 Portfolio Manager")
console = Console()

@app.command()
def list_credentials(
    registry: Path = typer.Option(Path("credentials.json"), help="Credential registry file"),
) -> None:
    """List all credentials in the registry."""
    creds = load_registry(registry)
    table = Table(title="CCSLL L1 Credentials")
    table.add_column("ID")
    table.add_column("Book")
    table.add_column("Status")
    for cred in creds:
        color = "green" if cred.status == CredentialStatus.EARNED else "yellow"
        table.add_row(cred.id, cred.book_id, f"[{color}]{cred.status.value}[/{color}]")
    console.print(table)

@app.command()
def verify(
    registry: Path = typer.Option(Path("credentials.json")),
    base: Path = typer.Option(Path("."), help="Base path for artifacts"),
) -> None:
    """Verify all credential proof artifacts."""
    creds = load_registry(registry)
    verified = 0
    for cred in creds:
        cred.status = verify_credential(cred, base)
        if cred.status == CredentialStatus.EARNED:
            verified += 1
    console.print(f"[green]✅ {verified}/{len(creds)} credentials verified[/green]")

if __name__ == "__main__":
    app()
```

---

## Chapter 7: Proof of Work — Submit Your Portfolio

```bash
# 1. Set up the project
python3 -m venv .venv && source .venv/bin/activate
pip install typer rich pydantic-settings gitpython

# 2. Create your credentials.json with at least 5 entries
# 3. Run the CLI
python3 -m portfolio list
python3 -m portfolio verify

# 4. Run the tests
pytest tests/ -v

# 5. Build the Docker image
docker build -t lippytmai-portfolio:l1 .
docker run --rm lippytmai-portfolio:l1 list

# 6. Generate the portfolio report
python3 -m portfolio generate --output portfolio_l1.md
```

**Evidence packet contents:**
- `credentials.json` — 10+ earned credentials
- `portfolio_l1.md` — generated Markdown portfolio
- `pytest` output — all tests pass
- `docker run` output — CLI runs in container

**Credential earned:** `CCSLL-L1-BADGE-PythonFoundations` *(SkillBadge — Phase 2 Complete)*

---

## What's Next: Phase 3 — Blockchain Foundations (B-056–B-080)

Phase 2 gave you Python. Phase 3 gives you the blockchain:

| Batch | Books | Topic |
|---|---|---|
| Batch 12 | B-056–B-060 | Blockchain basics, wallets, explorers, testnets, smart contracts |
| Batch 13 | B-061–B-065 | Solidity, Foundry, ERC-20, web3.py |
| Batch 14 | B-066–B-070 | Events, gas, structs, access control, ERC-721 NFTs |
| Batch 15 | B-071–B-075 | Deployment, cast, errors, DeFi, Solana |
| Batch 16 | B-076–B-080 | IPFS, security, on-chain credentials, The Graph, L1 Badge |

The Python skills from Phase 2 combine with blockchain in B-065 (*Interacting with Contracts via Python*) — one of the most powerful integrations in the ACSS.

---

## Further Reading

- 📄 [`docs/ai-clone-engine-swarms.md`](ai-clone-engine-swarms.md) — ACSS and the credential system
- 📄 [`docs/ai-deployment-activations.md`](ai-deployment-activations.md) — How ADA activates SkillBadges
- 📄 [`docs/B-056-what-is-a-blockchain-really.md`](B-056-what-is-a-blockchain-really.md) — Phase 3 starts here
- 🏠 [`README.md`](../README.md) — Encyclopedia home

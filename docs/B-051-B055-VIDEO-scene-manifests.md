# B-051–B-055 HDVG Video Scene Manifests

## Phase 2, Batch 6 — Python DevOps + Capstone

> 8-scene High-Density Video Guide (HDVG) scripts for each book in Batch 6.
> Identity: `lippytmai` (Teach mode) · Format: explainer + live-code demo · Creative gate: **HumanApprovalGate required before publish**

---

## B-051 — Git with Python

**Hook:** *"Git commands are powerful. Git + Python is unstoppable — automate the entire history of your projects."*

| Scene | Type | Duration | Content |
|---|---|---|---|
| S1 | Hook | 0:00–0:45 | Run `commit_reporter.py local .` → JSON output of last 10 commits |
| S2 | Concept | 0:45–2:30 | Why Python over shell for Git automation; GitPython vs subprocess vs API |
| S3 | Code | 2:30–5:00 | `GitPython`: `Repo`, `iter_commits`, `repo_summary` function |
| S4 | Code | 5:00–8:00 | Making commits with Python: `index.add`, `index.commit`, `Actor` |
| S5 | Code | 8:00–11:00 | `PyGitHub`: auth, `get_repo`, `get_pulls`, `get_commits` pagination |
| S6 | Build | 11:00–14:00 | Assemble full `commit_reporter.py` with `local` + `remote` subcommands |
| S7 | Live | 14:00–16:00 | Run against real repo; show JSON report; schedule with cron |
| S8 | Credential | 16:00–17:00 | Proof of Work demo · `CCSLL-L1-B051-GitEngineer` |

**Hermes event:** `HDVG:B051:RECORD_READY`
**Fabric node:** `GitPython → PyGitHub → commit_reporter → CCSLL-L1-B051`

---

## B-052 — Your First Docker Container

**Hook:** *"Stop saying 'it works on my machine.' Start shipping containers that work on every machine."*

| Scene | Type | Duration | Content |
|---|---|---|---|
| S1 | Hook | 0:00–0:45 | Before/after: raw Python install pain vs `docker run` instant deploy |
| S2 | Concept | 0:45–2:30 | VM vs container; layers; image = snapshot; container = running instance |
| S3 | Code | 2:30–5:00 | Write `Dockerfile` from scratch; `FROM`, `WORKDIR`, `COPY`, `RUN`, `CMD` |
| S4 | Code | 5:00–8:00 | `.dockerignore`; why layer order matters; `python:3.12-slim` vs full |
| S5 | Code | 8:00–11:00 | `docker build`, `run`, `ps`, `logs`, `exec -it`, `inspect` |
| S6 | Build | 11:00–14:00 | Containerize B-051 `commit_reporter.py` with `Dockerfile.reporter` |
| S7 | Compose | 14:00–16:00 | `docker-compose.yml`: api + db services; `depends_on`, healthcheck |
| S8 | Credential | 16:00–17:00 | Proof of Work: `docker run` JSON output · `CSEL-L1-B052-ContainerEngineer` |

**Hermes event:** `HDVG:B052:RECORD_READY`
**Fabric node:** `Dockerfile → layers → docker CLI → compose → CSEL-L1-B052`

---

## B-053 — Environment Variables and Security

**Hook:** *"Hardcoded secrets are the #1 cause of data breaches in developer projects. This is the video that stops that."*

| Scene | Type | Duration | Content |
|---|---|---|---|
| S1 | Hook | 0:00–0:45 | Show: bot scrapes GitHub, abuses leaked API key in < 60 seconds |
| S2 | Concept | 0:45–2:30 | The 12-Factor App config principle; what never goes in git |
| S3 | Code | 2:30–5:00 | `python-dotenv`: `load_dotenv()`, `.env` format, `.gitignore` pattern |
| S4 | Code | 5:00–8:00 | `pydantic-settings` + `SecretStr`: why `print(settings)` shows `***` |
| S5 | Code | 8:00–11:00 | Docker `--env-file`; GitHub Actions secrets; never bake in image |
| S6 | Build | 11:00–14:00 | Full `secure_config.py`: validators, `print_safe_summary`, `@lru_cache` |
| S7 | Security | 14:00–16:00 | `trufflehog3` scan; what to do when you leak a secret |
| S8 | Credential | 16:00–17:00 | Proof of Work: masked output demo · `CCSLL-L1-B053-SecureConfigEngineer` |

**Hermes event:** `HDVG:B053:RECORD_READY`
**Fabric node:** `SecretStr → dotenv → trufflehog → CCSLL-L1-B053`

---

## B-054 — Debugging Python Like a Professional

**Hook:** *"Every senior developer you admire has one skill in common: they can find bugs faster than anyone else on the team."*

| Scene | Type | Duration | Content |
|---|---|---|---|
| S1 | Hook | 0:00–0:45 | Demo: hit a bug, use `breakpoint()`, find root cause in 60 seconds |
| S2 | Concept | 0:45–2:30 | Debugging as scientific method: observe, hypothesize, test, conclude |
| S3 | Code | 2:30–5:00 | `breakpoint()` + pdb: n/s/c/l/p/pp/w/u/d/q — all the commands you need |
| S4 | Code | 5:00–8:00 | Conditional breakpoints; post-mortem debugging with `pdb.pm()` |
| S5 | Code | 8:00–11:00 | Strategic logging: `logger.exception()`, structured extra fields |
| S6 | Code | 11:00–14:00 | `cProfile`: find the slow function; `py-spy`: zero-overhead profiling |
| S7 | Build | 14:00–16:00 | Debug `broken.py`: reproduce and fix 3 bugs using pdb |
| S8 | Credential | 16:00–17:00 | Proof of Work: fixed output + test pass · `CCSLL-L1-B054-DebugEngineer` |

**Hermes event:** `HDVG:B054:RECORD_READY`
**Fabric node:** `pdb → breakpoint → cProfile → py-spy → CCSLL-L1-B054`

---

## B-055 — Python Earn-while-you-Learn: Level 1 Badge *(Milestone)*

**Hook:** *"30 books. 30 build artifacts. 30 credentials. One badge to prove the whole stack. This is your Python Level 1 graduation."*

| Scene | Type | Duration | Content |
|---|---|---|---|
| S1 | Milestone | 0:00–1:00 | Phase 2 montage: recap all 6 batches, 30 build artifacts |
| S2 | Concept | 1:00–2:30 | What a SkillBadge is; how the CCSLL credential system works |
| S3 | Code | 2:30–5:00 | Portfolio project structure; `Credential` + `Portfolio` dataclasses |
| S4 | Code | 5:00–8:00 | `registry.py` + `verifier.py` — load JSON, verify artifacts |
| S5 | Code | 8:00–11:00 | CLI with `typer + rich`: `list`, `verify` commands with color output |
| S6 | Build | 11:00–14:00 | Full `pytest` run; Docker build + `docker run list` |
| S7 | Phase3 | 14:00–16:00 | Phase 3 preview: B-056–B-080 Blockchain Foundations |
| S8 | SkillBadge | 16:00–17:30 | Submit portfolio · `CCSLL-L1-BADGE-PythonFoundations` minted 🎓 |

**Hermes event:** `HDVG:B055:RECORD_READY` + `PHASE2:COMPLETE:PYTHON_FOUNDATIONS`
**Fabric nodes:** `Portfolio → Credential → typer → rich → pytest → Docker → [BADGE mint]`

---

## Batch Summary

| Book | Credential | Hermes Event | Gate |
|---|---|---|---|
| B-051 | `CCSLL-L1-B051-GitEngineer` | `HDVG:B051:RECORD_READY` | ⏳ G13 |
| B-052 | `CSEL-L1-B052-ContainerEngineer` | `HDVG:B052:RECORD_READY` | ⏳ G13 |
| B-053 | `CCSLL-L1-B053-SecureConfigEngineer` | `HDVG:B053:RECORD_READY` | ⏳ G13 |
| B-054 | `CCSLL-L1-B054-DebugEngineer` | `HDVG:B054:RECORD_READY` | ⏳ G13 |
| B-055 | `CCSLL-L1-BADGE-PythonFoundations` | `HDVG:B055:RECORD_READY` + `PHASE2:COMPLETE` | ⏳ G13 |

---

## Further Reading

- 📄 [`docs/ai-copilot-video-sandbox-creator.md`](ai-copilot-video-sandbox-creator.md) — ACVS video pipeline
- 📄 [`docs/creative-building-process.md`](creative-building-process.md) — 8-stage creative loop
- 📄 [`docs/QEP-B051-B055-phase2-batch6-quality-evidence-packet.md`](QEP-B051-B055-phase2-batch6-quality-evidence-packet.md) — Quality gates
- 🏠 [`README.md`](../README.md) — Encyclopedia home

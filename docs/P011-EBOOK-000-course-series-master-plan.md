# P-011-EBOOK-000 — Course Series Master Plan
### *300 Ebooks and Audiobooks: Programmer, Blockchain Developer, and Linux Engineer — Beginner to Advanced*

> *"The best textbook is one that knows what you already know, adapts to how fast you learn, costs nothing to update, and earns the author a verifiable credential every time a student builds something real."*
> — Charles Earl Lipshay (lippytm.ai)

---

## Overview

This document is the **master plan** for the lippytm.ai **300-book educational course series** — 100 Beginner titles, 100 Intermediate titles, and 100 Advanced titles — covering programming, blockchain development, Linux systems, and AI engineering.

Every book in the series:
1. **Sources from** ChatGPT, Claude, Gemini, GitHub, and all lippytm.ai repositories via the ACSS (AI Conglomerate Swarms System)
2. **Is authored by** the AI Clone Engine (lippytmai primary, lippytm builder, Lippy Killjoy creative where marked) with Charles Earl Lipshay as human principal and final approver
3. **Contains** real code that runs, real tests that pass, real blockchain transactions on public testnets
4. **Earns** Earn-while-you-Learn credentials for readers who complete the build exercises
5. **Follows** the Prompt #11 12-step episode pattern (Fable → Reality → Questions → Data → Build → Test → Privacy → Business → Proof → Mutation → Correction → Archive)

*[Reality]* All code and technical claims in this series are verified. *[Speculative]* Future AI teaching loop integrations are marked speculative. *[Fiction]* Fable 5 story chapters are clearly marked as fictional dramatization.

---

## 1. Series Structure

### 1.1 Three Tracks

| Track | Books | Target Reader | Starting Point | Ending Point |
|---|---|---|---|---|
| **Beginner** | B-001 → B-100 | Zero experience; first terminal | Zero experience | CCSLL L1 + Linux L1 + CBSLL L0 |
| **Intermediate** | I-001 → I-100 | Some coding experience; wants to build | CCSLL L1–L2 | CCSLL L3 + CBSLL L2 + Linux L2 |
| **Advanced** | A-001 → A-100 | Working developer; wants mastery | CCSLL L3 | CCSLL L5 + CBSLL L4 + ACSS Architect |

### 1.2 Book Format (All Titles)

Every book in the series follows this structure:

```
Title Page
Earn-while-you-Learn Credential Map (which SkillBadges this book unlocks)
Fiction Boundary Notice (Fable 5 characters are fictional)

Chapter 1 — The Fable (Fictional story introducing the problem)
Chapter 2 — The Reality (What's actually true; sources cited)
Chapter 3 — The Questions (IF / MAYBE / WHY NOT / DON'T DO THAT)
Chapter 4 — The Data Model (diagrams, schemas, architecture)
Chapter 5 — The Build (code lab — all code runs and is tested)
Chapter 6 — The Tests (how to verify your build works)
Chapter 7 — The Review (privacy, security, accessibility, ethics)
Chapter 8 — The Business (entrepreneurship angle; honest earning claims)
Chapter 9 — Proof of Learning (quiz, submission, credential gate)
Chapter 10 — The Next Mutation (what to build next)
Chapter 11 — Corrections and Archive (known issues; update history)

Appendix A — Full Code Listings
Appendix B — Glossary
Appendix C — Further Reading (ACSS encyclopedia cross-links)
```

### 1.3 AI Multi-Source Synthesis Process

Each book is synthesized from:

| Source | Role | How Used |
|---|---|---|
| **Claude (Anthropic)** | Deep reasoning, nuanced explanations, ethics | Chapters 2, 3, 7, 8 — conceptual and ethical content |
| **ChatGPT (OpenAI)** | Clear step-by-step instructions, code samples | Chapters 4, 5, 6 — procedural and build content |
| **Gemini (Google)** | Large-context synthesis, multimodal diagrams | Chapter 4 — architecture diagrams; cross-referencing |
| **GitHub Copilot** | Code generation, test writing, inline docs | Appendix A — full code listings with tests |
| **lippytm.ai repos** | Source of all ACSS examples, real projects | All chapters — real-world grounding |
| **Fabric KB** | Pattern synthesis, quality scoring | Quality gate before publication |
| **Charles (human)** | Final approval on every production title | HumanApprovalGate — required for all Level 4+ content |

---

## 2. Beginner Series (B-001 → B-100)

**Mission:** Take someone with zero coding experience to their first working Python program, first Bash script, first Linux server, and first deployed smart contract.

**Credential path:** CCSLL L0 → L1, CLL L0 → L1, CBSLL L0

### 2.1 Beginner Books 1–25: Linux and Bash Foundations

| # | Title | Core Topic | Build Artifact | Credential |
|---|---|---|---|---|
| B-001 | *The Terminal and the Curious Mind* | What is a terminal? What is Linux? | Create your first directory and file | CLL L0 |
| B-002 | *Commands That Actually Work* | Essential Bash commands: ls, cd, mkdir, cp, mv, rm | Organize a project directory | CLL L0 |
| B-003 | *The File That Remembered Everything* | File permissions, users, groups | Set up a secure project directory | CLL L1 |
| B-004 | *The Script That Did My Job* | Writing your first Bash script | Automated file backup script | CLL L1 |
| B-005 | *Installing Things Without Breaking Things* | Package managers: apt, pacman, brew | Set up a Python dev environment | CLL L1 |
| B-006 | *The Process That Wouldn't Stop* | Processes, jobs, kill, htop | Process monitor script | CLL L1 |
| B-007 | *The Network That Connected Everything* | Networking basics: ping, curl, netstat | API call from the terminal | CLL L1 |
| B-008 | *Files That Never Get Lost* | Git basics: init, add, commit, push | First GitHub commit | CCSLL L0 |
| B-009 | *Working with Text Like a Pro* | grep, sed, awk, cut | Log parser script | CLL L1 |
| B-010 | *The Service That Started Itself* | systemd: units, enable, status, logs | Autostart a script on Linux | CLL L1 |
| B-011 | *Environment Variables and Secrets* | env vars, .env files, secrets never in code | Secure config loader | CCSLL L0 |
| B-012 | *The Container That Held Everything* | Docker basics: pull, run, build, compose | Run PostgreSQL locally | CSEL L0 |
| B-013 | *SSH: The Secure Handshake* | SSH keys, remote login, scp | Connect to a VPS | CLL L1 |
| B-014 | *Cron: The Machine That Never Forgets* | cron jobs, crontab syntax | Scheduled backup job | CLL L1 |
| B-015 | *The Editor That Does Everything* | Neovim basics (OMARCHY standard) | Write and run a script in Neovim | CLL L1 |
| B-016 | *Pipes, Redirects, and Composition* | `|` `>` `>>` `<` | Data pipeline one-liner | CLL L1 |
| B-017 | *The Arch Linux Advantage* | Arch Linux philosophy, AUR, pacman | OMARCHY bootstrap | CLL L1 |
| B-018 | *Log Files Tell the Truth* | Reading logs, journalctl, logrotate | Log analysis script | CLL L1 |
| B-019 | *Securing Your Linux Machine* | Firewall, fail2ban, SSH hardening | Hardened server config | CLL L1 |
| B-020 | *Disk Space: The Resource That Runs Out* | df, du, lsblk, fstab | Disk monitor alert script | CLL L1 |
| B-021 | *The Linux Filesystem Explained* | FHS: /etc, /var, /home, /usr, /tmp | File organization system | CLL L1 |
| B-022 | *Shell Functions and Aliases* | Functions, aliases, .bashrc/.zshrc | Personal productivity toolkit | CLL L1 |
| B-023 | *Archives, Compression, and Backups* | tar, gzip, rsync, snapshots | Automated backup system | CLL L1 |
| B-024 | *The User Who Could Do Anything* | sudo, root, user management, groups | Multi-user Linux setup | CLL L1 |
| B-025 | *Linux on Every Platform* | Linux on VPS, WSL, Raspberry Pi, cloud | Deploy on 3 environments | CLL L1 |

### 2.2 Beginner Books 26–55: Python Foundations

| # | Title | Core Topic | Build Artifact | Credential |
|---|---|---|---|---|
| B-026 | *Your First Python Program* | Python install, REPL, print, variables | Hello, lippytm.ai! | CCSLL L0 |
| B-027 | *Lists, Loops, and Logic* | Lists, for/while loops, if/else | FizzBuzz + grade calculator | CCSLL L0 |
| B-028 | *Functions That Do One Thing Well* | def, return, parameters, docstrings | Math utility library | CCSLL L1 |
| B-029 | *Dictionaries: The Data Swiss Army Knife* | dict, JSON, .get(), items() | JSON config reader | CCSLL L1 |
| B-030 | *Reading and Writing Files* | open(), read(), write(), pathlib | Log file processor | CCSLL L1 |
| B-031 | *Errors That Tell the Truth* | try/except, raise, custom exceptions | Robust file reader | CCSLL L1 |
| B-032 | *The Internet in a Function* | requests/httpx, APIs, JSON responses | Weather API client | CCSLL L1 |
| B-033 | *Classes and Objects Made Simple* | class, __init__, methods, dataclasses | Bank account simulator | CCSLL L1 |
| B-034 | *Testing Your Code (So Others Trust It)* | pytest, assert, test functions | Full test suite for B-028 | CCSLL L1 |
| B-035 | *Virtual Environments and pip* | venv, pip, requirements.txt, pyproject.toml | Reproducible Python project | CCSLL L1 |
| B-036 | *Type Hints: Making Python Honest* | type hints, mypy, Optional, Union | Type-safe utility functions | CCSLL L1 |
| B-037 | *Working with Dates and Times* | datetime, timedelta, timezone | Date calculator + scheduler | CCSLL L1 |
| B-038 | *Regular Expressions Demystified* | re module, match, search, groups | Email/URL validator | CCSLL L1 |
| B-039 | *SQLite: Your First Database* | sqlite3, CREATE TABLE, INSERT, SELECT | Personal task tracker | CCSLL L1 |
| B-040 | *Automation Scripts That Save Hours* | os, subprocess, shutil, pathlib | File organizer + renamer | CCSLL L1 |
| B-041 | *Python and the Web: Scraping Basics* | BeautifulSoup, requests, robots.txt ethics | Price tracker (ethical) | CCSLL L1 |
| B-042 | *Your First REST API* | FastAPI, GET/POST, pydantic models | Todo list API | CCSLL L1 |
| B-043 | *The Async Python Primer* | asyncio, async def, await | Concurrent API fetcher | CCSLL L1 |
| B-044 | *Modules, Packages, and Imports* | import, __init__.py, project structure | Organized Python package | CCSLL L1 |
| B-045 | *CSV and Spreadsheet Automation* | csv, pandas basics, openpyxl | Expense report generator | CCSLL L1 |
| B-046 | *Command-Line Tools with Python* | argparse, click, typer | CLI file processor | CCSLL L1 |
| B-047 | *Python Decorators Without the Magic* | @decorator, functools, wraps | Timing + logging decorators | CCSLL L1 |
| B-048 | *Environment Configuration Done Right* | python-dotenv, pydantic-settings | Config management system | CCSLL L1 |
| B-049 | *Logging: The Program's Memory* | logging, levels, handlers, formatters | Structured log system | CCSLL L1 |
| B-050 | *Python + Linux: The Power Combo* | subprocess, os, sys, shlex | Linux system manager in Python | CCSLL L1 + CLL L1 |
| B-051 | *Git with Python* | GitPython, GitHub API | Automated commit reporter | CCSLL L1 |
| B-052 | *Your First Docker Container* | Dockerfile, .dockerignore, docker build/run | Containerized Python app | CSEL L1 |
| B-053 | *Environment Variables and Security* | Secrets management, never hardcode | Secure Python app config | CCSLL L1 |
| B-054 | *Debugging Python Like a Professional* | pdb, breakpoint, logging debug | Debug a broken program | CCSLL L1 |
| B-055 | *Python Earn-while-you-Learn: Level 1 Badge* | Project: build + test + document + submit | Full Python L1 portfolio | CCSLL L1 SkillBadge |

### 2.3 Beginner Books 56–80: Web3 and Blockchain First Steps

| # | Title | Core Topic | Build Artifact | Credential |
|---|---|---|---|---|
| B-056 | *What Is a Blockchain? (Really)* | Blockchain fundamentals, no hype | Blockchain explainer diagram | CBSLL L0 |
| B-057 | *Your First Crypto Wallet* | MetaMask, private keys, seed phrases, safety | Wallet + test ETH received | CBSLL L0 |
| B-058 | *Reading the Blockchain* | Etherscan, block explorers, transactions | Transaction trace report | CBSLL L0 |
| B-059 | *Testnets: The Blockchain Sandbox* | Sepolia, Holesky, Solana devnet, faucets | Received testnet ETH + SOL | CBSLL L0 |
| B-060 | *What Is a Smart Contract?* | EVM, bytecode, ABI, why they matter | Smart contract anatomy diagram | CBSLL L0 |
| B-061 | *Installing the Blockchain Toolkit* | Foundry, cast, forge, anvil on Linux | OMARCHY blockchain bootstrap | CBSLL L1 |
| B-062 | *Your First Solidity Contract* | pragma, contract, state variables, functions | `HelloWorld.sol` deployed to Sepolia | CBSLL L1 |
| B-063 | *Testing Smart Contracts with Forge* | forge test, test functions, assertions | Passing test suite | CBSLL L1 |
| B-064 | *The ERC-20 Token Explained* | Token standards, balances, transfers | Deploy your own test token | CBSLL L1 |
| B-065 | *Interacting with Contracts via Python* | web3.py, contract ABI, call vs send | Python contract reader | CBSLL L1 |
| B-066 | *Events and Logs on the Blockchain* | emit, event, indexed, filtering | Event listener in Python | CBSLL L1 |
| B-067 | *Gas: The Blockchain's Energy* | Gas, gas limit, baseFee, priority fee | Gas estimator script | CBSLL L1 |
| B-068 | *Solidity Types: From Basics to Structs* | uint, string, address, mapping, struct | Student registry contract | CBSLL L1 |
| B-069 | *Ownable and Access Control* | Ownable.sol, onlyOwner, OpenZeppelin | Gated function contract | CBSLL L1 |
| B-070 | *The ERC-721 NFT Explained* | Non-fungible tokens, tokenURI, metadata | Mint your first NFT | CBSLL L1 |
| B-071 | *Deploying Contracts for Real* | forge script, --verify, Etherscan | Verified contract on Sepolia | CBSLL L1 |
| B-072 | *Reading Contract Data with cast* | cast call, cast balance, cast block | Chain data analyzer | CBSLL L1 |
| B-073 | *Errors, Reverts, and Custom Errors* | require, revert, custom error types | Error-safe contract | CBSLL L1 |
| B-074 | *What Is DeFi? (Without the Hype)* | AMMs, liquidity pools, lending, real risks | DeFi explainer + safety guide | CBSLL L1 |
| B-075 | *Your First Solana Program* | Solana basics, CLI, devnet, SOL | Deployed Solana hello-world | CBSLL L1 |
| B-076 | *What Is IPFS?* | Content addressing, pins, gateways | Upload file to IPFS | CBSLL L1 |
| B-077 | *Smart Contract Security Basics* | Reentrancy, overflow, access control | Slither audit on your contract | CBSLL L1 |
| B-078 | *On-Chain Identity and Credentials* | ERC-721 SkillBadges, lippytm.ai system | Receive your first SkillBadge | CBSLL L1 |
| B-079 | *The Graph: Querying the Blockchain* | GraphQL, subgraphs, indexers | Simple subgraph query | CBSLL L1 |
| B-080 | *Blockchain Earn-while-you-Learn: L1 Badge* | Project: full blockchain L1 portfolio | Submit + mint CBSLL L1 badge | CBSLL L1 SkillBadge |

### 2.4 Beginner Books 81–100: AI, Chatbots, and the ACSS First Look

| # | Title | Core Topic | Build Artifact | Credential |
|---|---|---|---|---|
| B-081 | *What Is AI? (Without the Magic)* | ML, LLMs, training, inference, limitations | AI concept explainer | CCSLL L0 |
| B-082 | *Your First API Call to an LLM* | Anthropic/OpenAI API, prompts, responses | Python LLM hello-world | CCSLL L1 |
| B-083 | *Prompts That Actually Work* | Prompt engineering: system, user, context | Prompt template library | CCSLL L1 |
| B-084 | *The Chatbot From Scratch* | P011-BOT Level 1: static KB chatbot | Working chatbot in 50 lines | CCSLL L1 |
| B-085 | *What Is a Knowledge Base?* | Embeddings, vector search, RAG concept | Qdrant quick-start | CCSLL L1 |
| B-086 | *Building Your First RAG System* | P011-BOT Level 2: Qdrant + Claude | Encyclopedia RAG chatbot | CCSLL L2 |
| B-087 | *Slack Bots for Learners* | Slack Bolt, slash commands | `/ask` command working | CCSLL L1 |
| B-088 | *What Is the ACSS?* | Hermes, Fabric, Clone Engine overview | ACSS diagram + walkthrough | CCSLL L1 |
| B-089 | *GitHub Copilot for Beginners* | Inline suggestions, chat, Copilot CLI | 3 Copilot-assisted builds | CCSLL L1 |
| B-090 | *AI Ethics for Builders* | Bias, privacy, consent, AI disclosure | Ethics checklist for your projects | CCSLL L1 |
| B-091 | *Version Control for AI Projects* | Git for AI: data versioning, model tracking | MLflow experiment tracked | CCSLL L1 |
| B-092 | *The AI Teaching Loop* | How lippytmai learns; RLHF concept | Feedback loop diagram | CCSLL L1 |
| B-093 | *Robots That Learn to Program* | ROS2 basics, EEEP platform first look | ROS2 hello-world node | CSEL L1 |
| B-094 | *Linux for AI Engineers* | GPU Linux, CUDA basics, Python on Linux | GPU Python environment | CLL L1 + CSEL L1 |
| B-095 | *The Earn-while-you-Learn Economy* | How credentials, rewards, and honest earning work | Personal earning plan | CCSLL L1 |
| B-096 | *What Is Web3 + AI?* | Intersection of AI and blockchain | Diagram + explainer | CBSLL L1 |
| B-097 | *CI/CD for Beginners* | GitHub Actions: first workflow | Passing CI pipeline | CCSLL L1 |
| B-098 | *The Privacy Engineer's Mindset* | GDPR, consent, PII, no-secrets rule | Privacy checklist | CCSLL L1 |
| B-099 | *Fable 5: The Clone Who Wouldn't Stop Learning* | Fictional synthesis of all Beginner concepts | Written reflection + quiz | CCSLL L1 |
| B-100 | *Beginner Graduation: Build Your Portfolio* | Compile all B-series artifacts | Complete portfolio PR + 3 credentials | CCSLL L1 + CLL L1 + CBSLL L1 |

---

## 3. Intermediate Series (I-001 → I-100)

**Mission:** Take a working beginner developer to production-grade systems: DeFi protocols, REST APIs, CI/CD pipelines, RAG chatbots, and multi-sig governance.

**Credential path:** CCSLL L2–L3, CLL L2, CBSLL L2–L3

### 3.1 Intermediate Theme Clusters

| Cluster | Books | Focus |
|---|---|---|
| **Python → Production** | I-001 → I-020 | FastAPI, async, testing, Docker, PostgreSQL |
| **Linux → SysAdmin** | I-021 → I-040 | systemd, networking, security, Ansible, K8s intro |
| **Solidity → DeFi** | I-041 → I-060 | ERC-20/721/1155, AMMs, lending, auditing, ZK intro |
| **AI → RAG + Fine-Tune** | I-061 → I-075 | LangChain, Qdrant, AMIL, fine-tuning basics |
| **Full-Stack Blockchain App** | I-076 → I-090 | Frontend + contract + indexer + CI/CD |
| **ACSS Integration** | I-091 → I-100 | Hermes, Fabric, Slack CRM, P011 engines |

*(Full title-by-title list in `P011-EBOOK-INTERMEDIATE.md` — to be created in Phase 2)*

---

## 4. Advanced Series (A-001 → A-100)

**Mission:** Take an experienced developer to ACSS architecture mastery: ZK proofs, RL trading agents, autonomous CI/CD, multi-chain protocol design, and Fabric pattern contributions.

**Credential path:** CCSLL L4–L5, CBSLL L4–L5, ACSS Architect (Charles review)

### 4.1 Advanced Theme Clusters

| Cluster | Books | Focus |
|---|---|---|
| **ZK Proofs in Practice** | A-001 → A-015 | Circom, snarkjs, on-chain verifiers, recursive proofs |
| **RL Trading Agents** | A-016 → A-030 | Gymnasium, PPO, live execution, risk models |
| **Protocol Design** | A-031 → A-050 | AMM math, MEV, Cosmos SDK, Substrate, cross-chain |
| **ACSS Architecture** | A-051 → A-065 | Building Fabric modules, Hermes extensions, AMIL fine-tuning |
| **Autonomous Systems** | A-066 → A-080 | ACD self-evolution, multi-agent coordination, AI safety |
| **Humanoid AI + Robotics** | A-081 → A-095 | ROS2 advanced, humanoid dev stack, EEEP platform |
| **ACSS Contributor** | A-096 → A-100 | Quality Evidence Packets, Charles review process |

*(Full title-by-title list in `P011-EBOOK-ADVANCED.md` — to be created in Phase 3)*

---

## 5. Production Pipeline

Every book passes through this automated pipeline before publication:

```
1. SYNTHESIS      Claude + ChatGPT + Gemini + GitHub → raw draft
        │
        ▼
2. FACT-CHECK     Fabric KB + external sources → claims verified
        │
        ▼
3. CODE VERIFY    All code examples run (Pytest + Forge) → 100% pass
        │
        ▼
4. QUALITY GATES  P011 12-gate pipeline → OriginalityGate through CorrectionGate
        │
        ▼
5. HUMAN REVIEW   Charles approves (Level 4+ content) or automated release
        │
        ▼
6. PUBLISH        Markdown → PDF (ebook) + SSML → MP3 (audiobook)
        │
        ▼
7. CREDENTIAL     Reader completion → SkillBadge mint on Base
        │
        ▼
8. EVOLUTION      Fabric tracks reader outcomes → book v2 improvements
```

---

## 6. Audiobook Specifications

Each title has a parallel audiobook edition:

| Component | Specification |
|---|---|
| **Narration voice** | lippytmai AI voice (ElevenLabs or equivalent) with human editing |
| **Code chapters** | Companion PDF provided; code read aloud as pseudocode summaries |
| **Format** | MP3 + M4B, chapter-marked |
| **Length** | Beginner: 45–90 min; Intermediate: 90–180 min; Advanced: 180–360 min |
| **Fable chapters** | Full dramatic narration; Lippy Killjoy chapters use character voice |
| **Quality gate** | Human listening review before release |

---

## 7. Earn-while-you-Learn Revenue Model

*Learning-to-Earning boundary: Approved learners may earn through verified contributions, teaching, building, and certified delivery. This program does not guarantee income, employment, funding, investment returns, or business success.*

| Revenue Stream | Mechanism |
|---|---|
| **Book sales** | Direct sales via lippytm.ai platform |
| **Credential verification** | Employers verify on-chain SkillBadges |
| **Teaching bounties** | Learners who teach others earn referral credentials |
| **Build submissions** | Quality build artifacts published to ecosystem earn recognition |
| **Content contributions** | Approved contributions to Fabric patterns earn ACSS Contributor status |

---

## 8. Phase Delivery Schedule

| Phase | Books | Target |
|---|---|---|
| **Phase 1** | B-001 → B-025 (Linux foundations) | Q4 2026 |
| **Phase 2** | B-026 → B-055 (Python foundations) | Q1 2027 |
| **Phase 3** | B-056 → B-080 (Blockchain foundations) | Q1 2027 |
| **Phase 4** | B-081 → B-100 (AI + ACSS first look) | Q2 2027 |
| **Phase 5** | I-001 → I-050 (Intermediate Part 1) | Q2 2027 |
| **Phase 6** | I-051 → I-100 (Intermediate Part 2) | Q3 2027 |
| **Phase 7** | A-001 → A-050 (Advanced Part 1) | Q3 2027 |
| **Phase 8** | A-051 → A-100 (Advanced Part 2) | Q4 2027 |

---

## Further Reading

- 📄 [`docs/P011-PLAN-001-curriculum-planner.md`](P011-PLAN-001-curriculum-planner.md) — Engine 3: the planner that personalizes each book's exercises per learner
- 📄 [`docs/P011-ENGINE-001-prompt11-engines.md`](P011-ENGINE-001-prompt11-engines.md) — all 8 engines that power the synthesis and quality pipeline
- 📄 [`docs/P011-BOT-001-chatbot-knowledge-base-learning-path.md`](P011-BOT-001-chatbot-knowledge-base-learning-path.md) — the 6-level path this series is built on
- 📄 [`docs/educational-environmental-ecosystems.md`](educational-environmental-ecosystems.md) — EEEP: the platform the Advanced robotics series extends
- 📄 [`docs/linux-blockchain-educational-ecosystem.md`](linux-blockchain-educational-ecosystem.md) — LBEE: the technical substrate for B-001–B-080
- 📄 [`docs/ai-model-intelligence-layer.md`](ai-model-intelligence-layer.md) — AMIL: model selection for the synthesis pipeline
- 📄 [`EARN_WHILE_YOU_LEARN.md`](../EARN_WHILE_YOU_LEARN.md) — The earn-while-you-learn philosophy behind every credential
- 🏠 [`README.md`](../README.md) — Encyclopedia home

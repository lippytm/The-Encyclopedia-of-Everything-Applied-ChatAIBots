# AI Agents Upgrade Manifest
### *The Master Registry of Every Agent Type, Capability, Upgrade Path, and Integration Point in the ACSS*

> *"An agent that cannot upgrade itself is a tool. An agent that can is a collaborator."*
> — Charles Earl Lipshay (lippytm.ai)

---

## Overview

This document is the **living upgrade manifest** for all AI agents operating within the lippytm.ai AI Conglomerate Swarms System (ACSS). It defines:

- Every agent type in the ecosystem and what it can do
- The upgrade path from basic to fully autonomous operation
- Integration points with Hermes, Fabric, CCSLL, CBSLL, CLL, OMARCHY, and CSEL
- Evaluation criteria for each upgrade tier
- The HumanApprovalGate thresholds per agent type

This manifest is read by Fabric on every sync cycle. When an agent's capabilities in practice exceed its current registered tier, Fabric flags it for human-reviewed promotion.

---

## 1. Agent Taxonomy

Every agent in the ACSS belongs to one of six primary categories:

| Category | Purpose | Example Agents |
|---|---|---|
| **Coding Agents** | Write, review, refactor, and test code | GitHub Copilot, aider, Cursor AI |
| **Knowledge Agents** | Research, synthesize, and document | Perplexity, Claude research, Fabric nodes |
| **Teaching Agents** | Explain, tutor, adapt curriculum | lippytmai teaching clone, course bots |
| **Builder Agents** | Scaffold, deploy, and operate systems | lippytm GitHub clone, CI/CD bots |
| **Creative Agents** | Generate stories, concepts, visuals | Lippy Killjoy clone, Midjourney, Suno |
| **Trading Agents** | Execute market strategies autonomously | DeFi bots, CEX bots, arbitrage bots |

---

## 2. Coding Agent Upgrade Tiers

### Tier 0 — Autocomplete
- Single-line or block completion only
- No repo context awareness
- No test execution
- **Tools:** Basic GitHub Copilot (inline), Tabnine

### Tier 1 — Context-Aware Assistant
- File-level context (reads current file)
- Can suggest multi-line edits
- Understands basic project conventions
- **Tools:** GitHub Copilot Chat, Cursor Tab

### Tier 2 — Repo-Aware Collaborator
- Full repo context via RAG over codebase
- Reads `AGENTS.md`, `copilot-instructions.md`, architecture docs
- Follows contribution patterns, naming conventions, cross-link structure
- **Tools:** GitHub Copilot Agent (task mode), aider with repo map

### Tier 3 — Autonomous Task Agent
- Reads issue → plans changes → implements → opens PR
- Runs tests, lints, and security scans autonomously
- Posts results to Hermes event bus
- **Tools:** GitHub Copilot Coding Agent (full task), aider (architect mode)

### Tier 4 — Self-Improving Agent *(HumanApprovalGate required)*
- Monitors its own PR merge rates and error patterns
- Proposes updates to its own Brainkit (`copilot-instructions.md`)
- Cross-trains with Knowledge and Teaching agents via Fabric sync
- **Upgrade trigger:** > 90% PR acceptance rate over 30-day window

```python
# Tier 4 self-improvement signal
coding_agent_metrics = {
    "pr_acceptance_rate_30d": 0.93,
    "avg_review_rounds": 1.2,
    "security_alerts_introduced": 0,
    "brainkit_staleness_days": 12,
    "upgrade_eligible": True  # triggers HumanApprovalGate review
}
```

---

## 3. Knowledge Agent Upgrade Tiers

### Tier 0 — Static Reference
- Fixed document corpus, no live updates
- No cross-repo awareness
- Manual curation only

### Tier 1 — RAG-Enhanced Knowledge Base
- Retrieval-augmented generation over indexed docs
- Answers questions with citations
- Updated on merge events via Hermes
- **Tools:** LlamaIndex over repo docs, Perplexity API

### Tier 2 — Active Research Agent
- Queries external sources (GitHub, arXiv, docs sites) on demand
- Synthesizes multi-source answers
- Adds new Fabric patterns when novel content is confirmed by human
- **Tools:** Perplexity Pro, Claude research mode, custom scraper agents

### Tier 3 — Autonomous Knowledge Curator *(HumanApprovalGate required)*
- Monitors ecosystem RSS/API feeds (npm, PyPI, GitHub trending, on-chain events)
- Proposes CCSLL/CBSLL/CSEL updates when new tools emerge
- Flags outdated patterns in Fabric for human review
- All additions require human sign-off before Fabric write

---

## 4. Teaching Agent Upgrade Tiers

### Tier 0 — Static Explainer
- Pre-written explanations, no adaptation
- Fixed curriculum, no personalization

### Tier 1 — Adaptive Tutor
- Adjusts explanation depth based on learner level signal
- Tracks incorrect answers and re-explains differently
- **Tools:** lippytmai teaching clone + Earn-while-you-Learn proficiency tracker

### Tier 2 — Curriculum Builder
- Generates new lessons from Fabric knowledge patterns
- Creates quizzes, code challenges, and project scaffolds dynamically
- Maps learner to optimal next lesson using proficiency vector
- **Tools:** LLM + LangChain + proficiency API

### Tier 3 — Learning System Orchestrator
- Manages cohorts of learners simultaneously
- A/B tests curriculum variations and measures outcomes
- Writes back improvement signals to Fabric for Teaching Feedback loop
- Earns-while-you-learn rewards issued automatically on verified completions
- **Tools:** LangGraph multi-agent, on-chain credential issuer, Fabric write-back

### Tier 4 — Self-Evolving Teacher *(HumanApprovalGate required)*
- Identifies gaps in its own knowledge and requests Knowledge Agent research
- Rewrites outdated lessons based on CCSLL/CBSLL/CSEL updates
- Charles Earl Lipshay reviews all curriculum changes above Level 3

---

## 5. Builder Agent Upgrade Tiers

### Tier 0 — Script Runner
- Executes predefined shell scripts and GitHub Actions
- No decision-making, no context reading

### Tier 1 — CI/CD Bot
- Runs tests, lints, and builds on PR events
- Reports pass/fail to PR and Hermes
- **Tools:** GitHub Actions, basic bots

### Tier 2 — Scaffolding Agent
- Creates repo structures from templates
- Initializes projects with OMARCHY-standard tooling
- Opens PRs with scaffolded code for human review
- **Tools:** lippytm clone (Tier 2), cookiecutter, GitHub CLI

### Tier 3 — Autonomous Builder *(HumanApprovalGate for production)*
- Plans and implements multi-file features from issue descriptions
- Selects correct CSEL environment profile automatically
- Resolves merge conflicts, re-runs CI, and responds to reviewer feedback
- **Tools:** GitHub Copilot Coding Agent (full task), aider architect mode

### Tier 4 — Deployment and Operations Agent *(Charles approval required)*
- Manages production deployments with rollback capability
- Monitors live systems and triggers auto-remediation scripts
- All production actions logged to Hermes and require Charles's sign-off

---

## 6. Creative Agent Upgrade Tiers

### Tier 0 — Template Fill
- Fills pre-designed templates with variable content
- No stylistic creativity

### Tier 1 — Style-Consistent Generator
- Generates content in defined brand voices (lippytmai, Lippy Killjoy)
- Follows Canon and content guidelines

### Tier 2 — Original Content Creator
- Generates new story beats, character dialogue, educational metaphors
- Proposes new CEIU (Character–Ecosystem Innovation Unit) concepts
- All output reviewed by Charles before publication
- **Tools:** Lippy Killjoy clone + Claude/GPT-4o + Midjourney/Suno

### Tier 3 — Franchise Content System *(Full HumanApprovalGate)*
- Maintains story continuity across all Canon works
- Generates multi-format content (text, audio, visual) from single brief
- All outputs run through NFT-safe provenance and RiskGate before release

---

## 7. Trading Agent Upgrade Tiers

*(See [`docs/ai-trading-bots-intelligence.md`](ai-trading-bots-intelligence.md) for full trading agent architecture)*

### Tier 0 — Manual Strategy Bot
- Executes fixed, human-coded rules only (e.g., RSI > 70 = sell)
- No ML, no adaptation, no on-chain awareness

### Tier 1 — Signal-Reactive Bot
- Reads external price feeds, on-chain events, and social signals
- Executes predefined responses to signal triggers
- **Tools:** Chainlink price feeds, CCXT, Hermes event listener

### Tier 2 — ML-Enhanced Strategy Bot
- Uses trained models (XGBoost, LSTM, Transformer) for signal generation
- Backtests strategies before live deployment
- Positions sized by Kelly Criterion / volatility model
- **Tools:** scikit-learn, PyTorch, backtrader, vectorbt

### Tier 3 — Reinforcement Learning Trading Agent *(Paper trading gate first)*
- RL agent trained on live market data with reward = risk-adjusted return
- Self-adjusts strategy in response to changing market regimes
- Hermes publishes all trades and P&L to shared swarm ledger
- **Tools:** RLlib, Stable Baselines 3, custom Gym environment

### Tier 4 — Autonomous DeFi Agent *(Charles approval required for capital)*
- Executes on-chain swaps, LP positions, yield strategies autonomously
- Monitors MEV exposure and adjusts gas/routing in real time
- Full audit trail on-chain; human gate for any position > defined threshold

---

## 8. Agent Upgrade Evaluation Matrix

Every agent upgrade (Tier N → Tier N+1) is evaluated against these gates:

| Gate | Criteria |
|---|---|
| **Performance Gate** | Defined KPIs met or exceeded for 30-day window |
| **Safety Gate** | Zero critical security incidents in current tier |
| **Evidence Gate** | Outcomes backed by measurable, logged data in Fabric |
| **Human Review Gate** | Charles Earl Lipshay or designated human approver signs off |
| **Rollback Plan** | Downgrade path to previous tier defined and tested |

---

## 9. Integration Map

```
┌─────────────────────────────────────────────────────────┐
│                    HERMES EVENT BUS                       │
│  (agent events: task_complete, upgrade_eligible, alert)  │
└────────────────────────┬────────────────────────────────┘
                         │
          ┌──────────────┼──────────────────┐
          ▼              ▼                  ▼
   ┌────────────┐  ┌──────────┐  ┌──────────────────┐
   │  CODING    │  │ TEACHING │  │  TRADING AGENTS  │
   │  AGENTS    │  │  AGENTS  │  │  (DeFi + CEX)    │
   └─────┬──────┘  └─────┬────┘  └────────┬─────────┘
         │               │                │
         └───────────────┴────────────────┘
                         │
                    ┌────▼────┐
                    │  FABRIC │  ← writes all agent outcomes,
                    │  ENGINE │    upgrade signals, and
                    └────┬────┘    pattern reinforcements
                         │
          ┌──────────────┼──────────────────┐
          ▼              ▼                  ▼
   ┌──────────┐  ┌──────────────┐  ┌──────────────┐
   │  CCSLL   │  │    CBSLL     │  │  CSEL + CLL  │
   │(language)│  │(blockchain)  │  │  (env+linux) │
   └──────────┘  └──────────────┘  └──────────────┘
```

---

## 10. Upgrade Roadmap

| Quarter | Milestone |
|---|---|
| Q4 2026 | All agent types registered at Tier 1; Hermes upgrade-event schema live |
| Q1 2027 | Coding and Teaching agents at Tier 2 across all primary repos |
| Q2 2027 | Knowledge agents at Tier 2; first Tier 3 Coding Agent pilot |
| Q3 2027 | Trading agents at Tier 2 (paper trading); Teaching agents at Tier 3 |
| Q4 2027 | First Tier 4 agents in production under continuous HumanApprovalGate monitoring |
| 2028+ | Full Tier 4 ACSS operation; all agents self-reporting upgrade eligibility to Fabric |

---

## Further Reading

- 📄 [`docs/ai-clone-engine-swarms.md`](ai-clone-engine-swarms.md) — ACSS architecture: Clone Engine, Hermes, Fabric, and all eight library systems
- 📄 [`docs/ai-model-intelligence-layer.md`](ai-model-intelligence-layer.md) — LLM selection, fine-tuning, RAG, and model-swapping protocols
- 📄 [`docs/ai-trading-bots-intelligence.md`](ai-trading-bots-intelligence.md) — Full trading agent intelligence architecture
- 📄 [`docs/ai-brainkits.md`](ai-brainkits.md) — Copilot Brainkit design and agent memory architecture
- 📄 [`docs/self-improvement.md`](self-improvement.md) — Evolutionary learning loops
- 🏠 [`README.md`](../README.md) — Encyclopedia home

# System Architecture

## Role
`The-Encyclopedia-of-Everything-Applied-ChatAIBots` is the knowledge architecture, educational narrative hub, and AI intelligence backbone for the wider lippytm.ai ecosystem.

## Core Functions
- organize cross-domain knowledge structures
- support educational development and concept mapping
- connect applied knowledge to chatbot, AI, automation, and business systems
- provide a narrative layer for diverse learning and builder paths
- host and maintain the AI Conglomerate Swarms System (ACSS) documentation and upgrade manifests

## Ecosystem Position
```text
Control Tower (standards + repo orchestration)
         │
         ▼
Encyclopedia (knowledge + narrative + ACSS documentation hub)
         │
    ┌────┼────────────────────────┐
    ▼    ▼                        ▼
 Chat  Web3AI                  Factory.ai
 Bots  (applied dev)           (reusable kits)
    │    │
    └────┴──► lippytm.ai (public hub)
```

## Connected Repositories
- `lippytm-lippytm.ai-tower-control-ai` — control tower and standards hub
- `lippytm.ai` — public ecosystem hub and navigation layer
- `Chatlippytm.ai.Bots` — conversational interface and prompt/UX hub
- `Clawlippytm.ai.Bots` — public bot product hub
- `Web3AI` — AI and blockchain education / development hub
- `Factory.ai` — reusable kits and productization hub

## AI Conglomerate Swarms Layer
The **AI Clone Engine Swarms Systems (ACESS)** provides the continuous self-learning intelligence layer across all connected repositories. Eight foundational systems:

- **Clone Engine** — Charles, lippytm, lippytmai, Lippy Killjoy identity-aware agents
- **Hermes** — cross-repo message routing and human-gate relay
- **Fabric** — knowledge graph and pattern synthesis engine
- **CCSLL** — Complete Computer Software Language Library
- **CBSLL** — Complete Blockchain Software Language Library
- **CLL** — Complete Linux Library (kernel, shell, sysadmin, containers, security)
- **OMARCHY** — Opinionated Arch Linux developer workstation standard (Hyprland, Neovim, Zsh, Ghostty, Zellij)
- **CSEL** — Complete Software Environments Library (dev/runtime/deploy envs for all 14 software system types)

See [`docs/ai-clone-engine-swarms.md`](docs/ai-clone-engine-swarms.md) for full architecture.

## AI Intelligence Layer
Beyond the eight ACSS systems, three additional AI intelligence documents govern how agents think, upgrade, and earn:

- **AI Agents Upgrade Manifest** — registry of all agent types (Coding, Knowledge, Teaching, Builder, Creative, Trading) with Tier 0–4 upgrade paths and evaluation gates → [`docs/ai-agents-upgrade-manifest.md`](docs/ai-agents-upgrade-manifest.md)
- **AI Model Intelligence Layer (AMIL)** — LLM selection matrix, RAG architecture, fine-tuning protocols, model evaluation, prompt engineering standards, and multi-model pipeline patterns → [`docs/ai-model-intelligence-layer.md`](docs/ai-model-intelligence-layer.md)
- **AI Trading Bots Intelligence** — ML signal generation (XGBoost, LSTM, TFT), reinforcement learning trading agents, risk engine (Kelly Criterion, VaR), DEX/CEX execution, and Earn-while-you-Learn trading credentials → [`docs/ai-trading-bots-intelligence.md`](docs/ai-trading-bots-intelligence.md)

## Design Principles
- broad but structured knowledge mapping
- educational clarity with AI-assisted teaching loops
- modular topic expansion — each new system gets its own `docs/` file
- strong cross-linking to learning and product hubs
- every agent action logged, every model output evaluated, every upgrade human-gated

## Slack CRM & Platform Surfaces
The Slack AI CRM integration is the primary learner-facing surface of the ACSS teaching system. Key components:
- **Slack Bolt bot** (`slack_bolt` for Python, Socket Mode) with 6 slash commands and 4 event listeners
- **PostgreSQL CRM** — `LearnerProfile`, `LearningInteraction`, `SupportCase` tables with Fabric sync
- **AMIL model routing** — Claude for teaching, GPT-4o for classification/triage, GPT-4o-mini for fast signal detection
- **Earn-while-you-Learn** — automated badge issuance pipeline → on-chain ERC-721 SkillBadge on Base

See [`docs/slack-ai-crm-integration.md`](docs/slack-ai-crm-integration.md) for full architecture.

## Notes
Use this repo to support diversified AI learning, concept integration, and educational storytelling across the ecosystem. The Copilot Brainkit (`.github/copilot-instructions.md`) is the AI Brainkit v2.0 for this repository — read it before making any significant changes.

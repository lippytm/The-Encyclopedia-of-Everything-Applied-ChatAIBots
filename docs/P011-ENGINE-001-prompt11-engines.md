# P-011-ENGINE-001 — The 8 Prompt #11 Engines
### *Architecture, Responsibilities, and ACSS Integration for Every Engine in the Prompt #11 System*

> *"A prompt is not a question — it is an engine. Eight engines, one system, one mission: intake every idea, classify every pattern, plan every build, document every lesson, review every quality gate, spread awareness, communicate across repos, and support every learner."*
> — Charles Earl Lipshay (lippytm.ai)

---

## Overview

Prompt #11 is the **educational intelligence orchestration system** of the lippytm.ai AI Conglomerate Swarms System. It is composed of **8 engines** — each a specialized agent pipeline that handles one category of the learn-build-earn cycle.

This document defines every engine's role, trigger conditions, inputs, outputs, ACSS integration points, and Python implementation patterns.

---

## 1. Engine Map Overview

```
                         ┌──────────────────────────────┐
                         │     PROMPT #11 SYSTEM        │
                         │  (AI Conglomerate Swarms)     │
                         └──────────────┬───────────────┘
                                        │
          ┌─────────────────────────────┼─────────────────────────────┐
          │                             │                             │
   ┌──────▼──────┐              ┌───────▼──────┐              ┌──────▼──────┐
   │  1. INTAKE  │              │ 2. CLASSIFY  │              │ 3. PLANNING │
   │  (receive)  │              │  (sort+tag)  │              │  (design)   │
   └──────┬──────┘              └───────┬──────┘              └──────┬──────┘
          │                             │                             │
          └─────────────────────────────┼─────────────────────────────┘
                                        │
          ┌─────────────────────────────┼─────────────────────────────┐
          │                             │                             │
   ┌──────▼──────┐              ┌───────▼──────┐              ┌──────▼──────┐
   │  4. DOCS    │              │ 5. QUALITY   │              │ 6. AWARENESS│
   │ (document)  │              │  REVIEW      │              │  (observe)  │
   └──────┬──────┘              └───────┬──────┘              └──────┬──────┘
          │                             │                             │
          └─────────────────────────────┼─────────────────────────────┘
                                        │
                      ┌─────────────────┴─────────────────┐
                      │                                   │
               ┌──────▼──────┐                   ┌────────▼─────┐
               │  7. REPO    │                   │  8. CRM      │
               │  COMMS      │                   │  SUPPORT     │
               └─────────────┘                   └──────────────┘
```

---

## 2. Engine 1 — Intake

**Role:** Receive all incoming signals — user questions, GitHub issues, Slack messages, Hermes events, cron triggers — and route them to the correct downstream engine.

**Triggers:**
- New Slack message or slash command
- GitHub issue or PR opened
- Hermes event received
- Scheduled cron (nightly audit)
- Webhook from external platform

**Inputs:** Raw signal (text, event JSON, webhook payload)

**Outputs:** Normalized `IntakeEvent` published to Hermes

```python
# acss/p011/engines/intake.py
"""Prompt #11 Engine 1 — Intake: normalize and route all incoming signals."""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal, Any


IntakeSource = Literal[
    "slack_message", "slack_command", "github_issue", "github_pr",
    "hermes_event", "cron", "webhook", "api_call"
]


@dataclass
class IntakeEvent:
    event_id: str
    source: IntakeSource
    raw_payload: dict[str, Any]
    normalized_text: str
    learner_id: str | None
    repo: str | None
    priority: Literal["critical", "high", "normal", "low"] = "normal"
    received_at: datetime = field(default_factory=datetime.utcnow)
    routed_to_engine: str | None = None


class IntakeEngine:
    """Normalizes incoming signals into IntakeEvents and routes via Hermes."""

    PRIORITY_KEYWORDS = {
        "critical": ["urgent", "broken", "down", "security", "bug", "error"],
        "high": ["help", "blocked", "question", "issue"],
        "low": ["suggestion", "idea", "feedback"],
    }

    def __init__(self, hermes_client: Any) -> None:
        self.hermes = hermes_client

    async def ingest(self, source: IntakeSource, payload: dict[str, Any]) -> IntakeEvent:
        """Normalize a raw signal into an IntakeEvent and publish to Hermes."""
        text = self._extract_text(source, payload)
        priority = self._detect_priority(text)
        learner_id = payload.get("user_id") or payload.get("sender_id")
        repo = payload.get("repository", {}).get("full_name") if "repository" in payload else None

        event = IntakeEvent(
            event_id=f"p11_intake_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}",
            source=source,
            raw_payload=payload,
            normalized_text=text,
            learner_id=learner_id,
            repo=repo,
            priority=priority,
        )

        # Route to downstream engine via Hermes
        target_engine = self._route(source, text)
        event.routed_to_engine = target_engine
        await self.hermes.publish(
            event_type=f"p11.intake.{target_engine}",
            payload=event.__dict__,
        )
        return event

    def _extract_text(self, source: IntakeSource, payload: dict) -> str:
        extractors = {
            "slack_message": lambda p: p.get("text", ""),
            "slack_command": lambda p: p.get("text", ""),
            "github_issue": lambda p: f"{p.get('title','')} {p.get('body','')}",
            "github_pr": lambda p: f"{p.get('title','')} {p.get('body','')}",
            "hermes_event": lambda p: str(p.get("payload", "")),
            "cron": lambda p: p.get("description", "scheduled_check"),
            "webhook": lambda p: str(p),
            "api_call": lambda p: p.get("query", ""),
        }
        return extractors.get(source, lambda p: str(p))(payload)

    def _detect_priority(self, text: str) -> Literal["critical", "high", "normal", "low"]:
        lower = text.lower()
        for priority, keywords in self.PRIORITY_KEYWORDS.items():
            if any(kw in lower for kw in keywords):
                return priority  # type: ignore[return-value]
        return "normal"

    def _route(self, source: IntakeSource, text: str) -> str:
        if source in ("slack_message", "slack_command"):
            if any(w in text.lower() for w in ("help", "how", "what", "why", "explain")):
                return "classification"
            if any(w in text.lower() for w in ("support", "issue", "bug", "broken")):
                return "crm_support"
        if source in ("github_issue", "github_pr"):
            return "quality_review"
        if source == "cron":
            return "awareness"
        return "classification"
```

---

## 3. Engine 2 — Classification

**Role:** Tag, categorize, and score every intake event so downstream engines know exactly what kind of learning action, support request, documentation task, or system event they are dealing with.

**Inputs:** `IntakeEvent` from Hermes

**Outputs:** `ClassifiedEvent` with tags, category, topic, and routing metadata

**ACSS models:** GPT-4o for structured JSON classification, Fabric for topic taxonomy lookup

```python
# acss/p011/engines/classification.py
"""Prompt #11 Engine 2 — Classification: tag and categorize intake events."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Any


TopicArea = Literal[
    "ai_systems", "blockchain", "linux_systems", "web_dev",
    "mobile_dev", "data_engineering", "crm_systems", "robotics",
    "trading_bots", "earn_while_you_learn", "documentation", "meta"
]

ContentType = Literal[
    "question", "build_request", "bug_report", "support_case",
    "curriculum_request", "feedback", "announcement", "automation_trigger"
]


@dataclass
class ClassifiedEvent:
    intake_event_id: str
    topic_area: TopicArea
    content_type: ContentType
    proficiency_level: int  # 0–5 (CCSLL scale)
    tags: list[str]
    routing_score: dict[str, float]  # engine → confidence
    requires_human: bool
    classified_by_model: str


class ClassificationEngine:
    """Uses GPT-4o + Fabric taxonomy to classify intake events."""

    CLASSIFICATION_PROMPT = """Classify the following learner message for the lippytm.ai encyclopedia system.

Return JSON with these fields:
- topic_area: one of [ai_systems, blockchain, linux_systems, web_dev, mobile_dev, data_engineering, crm_systems, robotics, trading_bots, earn_while_you_learn, documentation, meta]
- content_type: one of [question, build_request, bug_report, support_case, curriculum_request, feedback, announcement, automation_trigger]
- proficiency_level: 0-5 (0=total beginner, 5=master/contributor)
- tags: array of 2-5 lowercase topic tags
- requires_human: true if this needs HumanApprovalGate (Level 4+, production, or sensitive)

Message: {message}"""

    def __init__(self, amil_client: Any, fabric_client: Any) -> None:
        self.amil = amil_client
        self.fabric = fabric_client

    async def classify(self, intake_event_id: str, text: str) -> ClassifiedEvent:
        """Classify an intake event using GPT-4o + Fabric topic taxonomy."""
        # 1. Enrich with Fabric topic context
        fabric_ctx = await self.fabric.get_topic_taxonomy()

        # 2. Classify with GPT-4o (best for structured JSON output)
        result = await self.amil.call_json(
            model="gpt-4o",
            prompt=self.CLASSIFICATION_PROMPT.format(message=text),
            schema={
                "type": "object",
                "required": ["topic_area", "content_type", "proficiency_level", "tags", "requires_human"],
            },
        )

        # 3. Calculate routing scores (which engines should handle this?)
        routing_score = self._calculate_routing_scores(
            result["content_type"], result["topic_area"]
        )

        # 4. Store in Fabric for pattern learning
        await self.fabric.store_classification(
            event_id=intake_event_id,
            classification=result,
        )

        return ClassifiedEvent(
            intake_event_id=intake_event_id,
            topic_area=result["topic_area"],
            content_type=result["content_type"],
            proficiency_level=result["proficiency_level"],
            tags=result["tags"],
            routing_score=routing_score,
            requires_human=result["requires_human"],
            classified_by_model="gpt-4o",
        )

    def _calculate_routing_scores(
        self, content_type: str, topic_area: str
    ) -> dict[str, float]:
        base_scores: dict[str, float] = {
            "planning": 0.2,
            "documentation": 0.2,
            "quality_review": 0.2,
            "awareness": 0.2,
            "repo_comms": 0.2,
            "crm_support": 0.2,
        }
        if content_type == "question":
            base_scores["planning"] = 0.9
        elif content_type == "build_request":
            base_scores["planning"] = 0.8
            base_scores["documentation"] = 0.6
        elif content_type == "bug_report":
            base_scores["quality_review"] = 0.95
            base_scores["crm_support"] = 0.7
        elif content_type == "support_case":
            base_scores["crm_support"] = 0.95
        elif content_type == "automation_trigger":
            base_scores["repo_comms"] = 0.9
            base_scores["awareness"] = 0.8
        return base_scores
```

---

## 4. Engine 3 — Planning

**Role:** Design and sequence learning plans, build agendas, and curriculum paths based on a classified event and the learner's current proficiency profile.

**Inputs:** `ClassifiedEvent` + Learner proficiency from Fabric

**Outputs:** A structured `LearningPlan` with ordered steps, resources, and expected outcomes

**ACSS models:** Claude 3.5 for deep reasoning and curriculum design

---

## 5. Engine 4 — Documentation

**Role:** Generate, update, and maintain encyclopedia documentation. Triggered by build completions, new patterns in Fabric, merged PRs, and curriculum additions.

**Inputs:** Build artifacts, Fabric pattern signals, PR diffs, Hermes events

**Outputs:** New or updated `.md` files committed to the repository

**ACSS integration:** ACD `AutonomousPRReviewer` and `FabricEvolutionEngine` feed directly into this engine

**Key rule:** All documentation generated by this engine must follow the encyclopedia format:
title → epigraph blockquote → `---` → numbered `##` sections → Further Reading

---

## 6. Engine 5 — Quality Review

**Role:** Verify that every build artifact, document, code example, and credential meets the P011 quality standards before it progresses or earns a credential.

**Quality Gates (in order):**

| Gate | What It Checks | Automatic? |
|---|---|---|
| **OriginalityGate** | No plagiarism, no copyright violation | Automated |
| **FictionBoundaryGate** | Fictional characters never merged with real data | Automated |
| **RightsGate** | All media and content has verified rights | Automated |
| **SourceGate** | All factual claims cite a source | Automated |
| **CodeTestGate** | All code has passing tests ≥ 80% coverage | Automated (Pytest/Forge) |
| **LearningOutcomeGate** | Measurable learning objectives present | Automated |
| **AccessibilityGate** | Readable at 8th grade level | Automated |
| **PrivacyGate** | No PII, no secrets committed | Automated |
| **SecurityGate** | No security vulnerabilities (Slither, CodeQL) | Automated |
| **EnvironmentalGate** | Resource usage documented | Automated |
| **RevenueIntegrityGate** | Earning claims are honest and bounded | Automated |
| **CorrectionGate** | Correction procedure defined | Automated |
| **HumanApprovalGate** | Charles signs off for Level 4+ | Manual — Charles only |

---

## 7. Engine 6 — Awareness

**Role:** Continuously monitor the state of the entire ecosystem — all repos, all agents, all learners — and surface signals that other engines need to act on.

**What it watches:**
- CI/CD health across all lippytm.ai repositories
- Learner engagement metrics (active vs. churned learners)
- Fabric pattern confidence scores (is a pattern degrading?)
- Node health (Ethereum, Solana, Cosmos validators)
- Model performance drift (is Claude slower this week?)
- Credential issuance rate (are learners progressing?)

**Outputs:** Hermes events published on any anomaly or positive signal

---

## 8. Engine 7 — Repo Communication

**Role:** Manage all cross-repository communication — GitHub issue/PR creation, cross-repo Hermes events, clone agent coordination, and the Fabric-triggered auto-improvement PR pipeline.

**Triggers:**
- Fabric detects an improvement opportunity (publishes to Hermes)
- A learner completes a build that should be mirrored across repos
- A security alert requires a PR in multiple repos
- ACD self-evolution loop generates a new improvement proposal

**Key tool:** The ACD `FabricEvolutionEngine` (`docs/autonomous-continuous-development.md` §5)

---

## 9. Engine 8 — CRM Support

**Role:** Handle every learner support interaction — questions, escalations, complaints, correction requests — with AI-assisted triage and human-approval gates for sensitive cases.

**Full reference:** `docs/P011-CRM-001-learning-system.md` and `docs/slack-ai-crm-integration.md`

**SLA tiers:**

| Priority | Response Target | Resolution Target | Handler |
|---|---|---|---|
| **P1 — Critical** | < 15 min | < 2 hours | Hermes → lippytm clone → Charles |
| **P2 — High** | < 1 hour | < 1 day | lippytmai teaching agent |
| **P3 — Normal** | < 4 hours | < 3 days | lippytmai teaching agent |
| **P4 — Low** | < 1 day | < 1 week | Async KB answer |

---

## 10. Engine Interconnect Map

```
intake ──▶ classification ──▶ planning ──▶ documentation
   │              │                │
   └──▶ crm_support        quality_review ◀─────────────┘
                  │                │
           awareness ◀─────────────┘
                  │
           repo_comms ──▶ (cross-repo Hermes events)
```

All 8 engines publish and subscribe via **Hermes**. All pattern learning flows into **Fabric**. All model calls route through **AMIL**. All human decisions go through the **HumanApprovalGate** (Charles Earl Lipshay).

---

## 11. Next Evolutions

| Engine | Planned Upgrade | Target Quarter |
|---|---|---|
| Intake | Voice input via Whisper API (robot learner audio) | Q4 2026 |
| Classification | Fine-tuned lippytmai classifier (replaces GPT-4o) | Q1 2027 |
| Planning | Multi-week adaptive curriculum (tracks long-term goals) | Q4 2026 |
| Documentation | Auto-generates encyclopedia entries from build logs | Q4 2026 |
| Quality Review | Automated learner outcome measurement (A/B tests) | Q1 2027 |
| Awareness | Real-time learner engagement dashboard on Slack | Q4 2026 |
| Repo Comms | Multi-repo atomic commit coordination via Hermes | Q1 2027 |
| CRM Support | On-chain complaint resolution with verifiable outcome | Q2 2027 |

---

## Further Reading

- 📄 [`docs/P011-BOT-001-chatbot-knowledge-base-learning-path.md`](P011-BOT-001-chatbot-knowledge-base-learning-path.md) — chatbot learning path powered by these engines
- 📄 [`docs/P011-STACK-001-repo-stack-profile.md`](P011-STACK-001-repo-stack-profile.md) — technology stack behind each engine
- 📄 [`docs/P011-CRM-001-learning-system.md`](P011-CRM-001-learning-system.md) — Engine 8 (CRM Support) in full detail
- 📄 [`docs/ai-clone-engine-swarms.md`](ai-clone-engine-swarms.md) — ACSS: the infrastructure all 8 engines run on
- 📄 [`docs/autonomous-continuous-development.md`](autonomous-continuous-development.md) — ACD: Engine 7 (Repo Comms) backbone
- 📄 [`PROMPT_11_LANGUAGE_LIBRARY.md`](../PROMPT_11_LANGUAGE_LIBRARY.md) — Prompt #11 language library overview
- 🏠 [`README.md`](../README.md) — Encyclopedia home

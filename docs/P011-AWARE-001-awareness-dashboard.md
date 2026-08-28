# P-011-AWARE-001 — Awareness Engine (Engine 6)
### *Real-Time Learner and Ecosystem Monitoring for the Prompt #11 System*

> *"Awareness is not surveillance. It is the system paying attention to itself — knowing where learners are thriving, where they are stuck, where pipelines are failing, and where the next improvement lives — so that nothing goes unnoticed and nothing stays broken."*
> — Charles Earl Lipshay (lippytm.ai)

---

## Overview

**Engine 6 — Awareness** is the nervous system of the Prompt #11 ecosystem. It continuously monitors every signal from every learner, every pipeline, every AI model, every blockchain node, and every repository — and surfaces anomalies and opportunities to the engines that can act on them.

Unlike surveillance, the Awareness Engine:
- Monitors **aggregate patterns**, not individual surveillance
- Operates with **consent** — all learners opt in to learning analytics
- **Publishes to Hermes** rather than storing private data centrally
- Respects the **fiction boundary** — never conflates fictional events with real learner data

---

## 1. What the Awareness Engine Monitors

### 1.1 Learner Engagement Signals

| Signal | Source | Threshold → Action |
|---|---|---|
| **Daily Active Learners** | CRM `/activity` | Drop > 20% week-on-week → Engine 3 re-engagement plan |
| **Lesson Completion Rate** | Fabric plan progress | < 40% completion → curriculum plan simplified |
| **Streak Length** | CRM learner profiles | Streak breaks > 3 days → Hermes re-engagement event |
| **Quiz Pass Rate** | P011-BOT chatbot | < 70% pass rate for a topic → lesson content revised |
| **Credential Velocity** | On-chain mint events | 0 credentials minted in 7 days → engagement review |
| **Support Case Volume** | P011-CRM-001 | > 5 P1 cases in 1 hour → escalation to Charles |
| **Learner Dropout Point** | Fabric plan progress | Which step do most learners abandon? → step redesigned |

### 1.2 Pipeline Health Signals

| Signal | Source | Threshold → Action |
|---|---|---|
| **CI Failure Rate** | ACD / GitHub Actions | > 10% failure rate → `PipelineGuardian` triggered |
| **Deploy Success Rate** | Hermes deploy events | < 95% → ACD auto-revert check |
| **AI Review Latency** | AMIL metrics | P95 > 8 seconds → model routing review |
| **RAG Retrieval Quality** | Fabric KB metrics | Mean relevance < 0.7 → KB re-index triggered |
| **Hermes Event Backlog** | Hermes queue | > 1000 events → capacity alert to lippytm clone |
| **Fabric Pattern Confidence** | Fabric self-report | < 0.6 on active patterns → Fabric re-training |

### 1.3 Infrastructure Health Signals

| Signal | Source | Threshold → Action |
|---|---|---|
| **Ethereum Node Sync** | LBEE health monitor | Behind > 100 blocks → alert + auto-restart |
| **Solana Validator Uptime** | systemd + Hermes | < 95% uptime → lippytm clone alert |
| **Qdrant Vector DB Health** | Qdrant `/health` | Unreachable > 30 sec → fallback KB activated |
| **PostgreSQL Connections** | CRM DB pool | > 90% pool used → connection limit raised |
| **Disk Space** | Linux `df` monitoring | < 20 GB free → cleanup + alert |

### 1.4 Model Performance Drift

| Signal | Source | Threshold → Action |
|---|---|---|
| **Claude 3.5 Latency** | AMIL metrics | P95 > 6s → route to GPT-4o fallback |
| **GPT-4o JSON Error Rate** | AMIL metrics | > 5% invalid JSON → prompt revision |
| **Embedding Drift** | Fabric KB metrics | Cosine similarity degradation → re-embed KB |
| **Fine-Tune Performance** | lippytmai eval | ROUGE score drop > 10% → re-training flag |

---

## 2. Awareness Engine Implementation

```python
# acss/p011/engines/awareness/awareness_engine.py
"""
Prompt #11 Engine 6 — Awareness Engine.
Continuously monitors learner engagement, pipeline health, infrastructure, and model performance.
Publishes anomaly and opportunity events to Hermes.
"""

from __future__ import annotations
import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Literal
import httpx


SignalCategory = Literal[
    "learner_engagement", "pipeline_health", "infrastructure",
    "model_performance", "credential_velocity", "security"
]

SignalSeverity = Literal["info", "warning", "critical"]


@dataclass
class AwarenessSignal:
    signal_id: str
    category: SignalCategory
    name: str
    severity: SignalSeverity
    current_value: float | int | str
    threshold: float | int | str
    description: str
    recommended_action: str
    requires_human: bool
    detected_at: datetime


class AwarenessEngine:
    """
    Engine 6: Real-time monitoring of the Prompt #11 ecosystem.

    Runs as a continuous async loop; checks all signal categories
    on configurable intervals and publishes events to Hermes.
    """

    # Check intervals (seconds)
    LEARNER_INTERVAL = 300    # 5 minutes
    PIPELINE_INTERVAL = 60    # 1 minute
    INFRA_INTERVAL = 120      # 2 minutes
    MODEL_INTERVAL = 180      # 3 minutes

    def __init__(
        self,
        hermes_client: Any,
        fabric_client: Any,
        crm_client: Any,
        amil_client: Any,
        config: dict[str, Any],
    ) -> None:
        self.hermes = hermes_client
        self.fabric = fabric_client
        self.crm = crm_client
        self.amil = amil_client
        self.config = config
        self._running = False

    async def start(self) -> None:
        """Start all monitoring loops concurrently."""
        self._running = True
        await asyncio.gather(
            self._learner_loop(),
            self._pipeline_loop(),
            self._infra_loop(),
            self._model_loop(),
        )

    async def stop(self) -> None:
        self._running = False

    # ── Learner Engagement Loop ─────────────────────────────────────────────

    async def _learner_loop(self) -> None:
        while self._running:
            signals = await self._check_learner_engagement()
            await self._publish_signals(signals)
            await asyncio.sleep(self.LEARNER_INTERVAL)

    async def _check_learner_engagement(self) -> list[AwarenessSignal]:
        signals = []
        metrics = await self.crm.get_engagement_metrics(window_days=7)

        # Weekly active learner drop
        if metrics["wau_change_pct"] < -20:
            signals.append(AwarenessSignal(
                signal_id=f"aware_learner_drop_{datetime.utcnow().strftime('%Y%m%d%H%M')}",
                category="learner_engagement",
                name="weekly_active_learner_drop",
                severity="warning",
                current_value=metrics["wau_change_pct"],
                threshold=-20,
                description=f"Weekly active learners dropped {abs(metrics['wau_change_pct']):.0f}% vs last week.",
                recommended_action="Engine 3: generate re-engagement curriculum for churned learners",
                requires_human=False,
                detected_at=datetime.utcnow(),
            ))

        # Lesson completion rate
        if metrics["lesson_completion_rate"] < 0.40:
            signals.append(AwarenessSignal(
                signal_id=f"aware_completion_low_{datetime.utcnow().strftime('%Y%m%d%H%M')}",
                category="learner_engagement",
                name="low_lesson_completion_rate",
                severity="warning",
                current_value=metrics["lesson_completion_rate"],
                threshold=0.40,
                description=f"Only {metrics['lesson_completion_rate']:.0%} of lessons are being completed.",
                recommended_action="Engine 3: simplify curriculum steps; Engine 4: improve lesson content",
                requires_human=False,
                detected_at=datetime.utcnow(),
            ))

        # Support case spike
        recent_p1 = metrics.get("p1_cases_last_hour", 0)
        if recent_p1 > 5:
            signals.append(AwarenessSignal(
                signal_id=f"aware_support_spike_{datetime.utcnow().strftime('%Y%m%d%H%M')}",
                category="learner_engagement",
                name="support_case_spike",
                severity="critical",
                current_value=recent_p1,
                threshold=5,
                description=f"{recent_p1} P1 support cases in the last hour.",
                recommended_action="Immediate escalation to Charles via HumanApprovalGate",
                requires_human=True,
                detected_at=datetime.utcnow(),
            ))

        return signals

    # ── Pipeline Health Loop ────────────────────────────────────────────────

    async def _pipeline_loop(self) -> None:
        while self._running:
            signals = await self._check_pipeline_health()
            await self._publish_signals(signals)
            await asyncio.sleep(self.PIPELINE_INTERVAL)

    async def _check_pipeline_health(self) -> list[AwarenessSignal]:
        signals = []
        metrics = await self.fabric.get_pipeline_metrics(window_hours=1)

        if metrics.get("ci_failure_rate", 0) > 0.10:
            signals.append(AwarenessSignal(
                signal_id=f"aware_ci_fail_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                category="pipeline_health",
                name="high_ci_failure_rate",
                severity="warning",
                current_value=metrics["ci_failure_rate"],
                threshold=0.10,
                description=f"CI failure rate is {metrics['ci_failure_rate']:.0%} over the last hour.",
                recommended_action="ACD PipelineGuardian: inspect failure patterns",
                requires_human=False,
                detected_at=datetime.utcnow(),
            ))

        rag_quality = metrics.get("rag_mean_relevance", 1.0)
        if rag_quality < 0.70:
            signals.append(AwarenessSignal(
                signal_id=f"aware_rag_drift_{datetime.utcnow().strftime('%Y%m%d%H%M')}",
                category="pipeline_health",
                name="rag_quality_degradation",
                severity="warning",
                current_value=rag_quality,
                threshold=0.70,
                description=f"RAG mean relevance score dropped to {rag_quality:.2f} (threshold: 0.70).",
                recommended_action="Fabric: re-index encyclopedia KB; check embedding model drift",
                requires_human=False,
                detected_at=datetime.utcnow(),
            ))

        return signals

    # ── Infrastructure Loop ─────────────────────────────────────────────────

    async def _infra_loop(self) -> None:
        while self._running:
            signals = await self._check_infrastructure()
            await self._publish_signals(signals)
            await asyncio.sleep(self.INFRA_INTERVAL)

    async def _check_infrastructure(self) -> list[AwarenessSignal]:
        signals = []
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Check Qdrant
            try:
                r = await client.get(f"{self.config['qdrant_url']}/health")
                if r.status_code != 200:
                    raise Exception("unhealthy")
            except Exception:
                signals.append(AwarenessSignal(
                    signal_id=f"aware_qdrant_down_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                    category="infrastructure",
                    name="qdrant_unreachable",
                    severity="critical",
                    current_value="unreachable",
                    threshold="reachable",
                    description="Qdrant vector store is unreachable — RAG responses will degrade.",
                    recommended_action="Restart Qdrant container; activate static KB fallback",
                    requires_human=False,
                    detected_at=datetime.utcnow(),
                ))
        return signals

    # ── Model Performance Loop ──────────────────────────────────────────────

    async def _model_loop(self) -> None:
        while self._running:
            signals = await self._check_model_performance()
            await self._publish_signals(signals)
            await asyncio.sleep(self.MODEL_INTERVAL)

    async def _check_model_performance(self) -> list[AwarenessSignal]:
        signals = []
        metrics = await self.amil.get_performance_metrics(window_minutes=30)

        for model_id, model_metrics in metrics.items():
            p95_latency = model_metrics.get("p95_latency_ms", 0)
            if "claude" in model_id and p95_latency > 6000:
                signals.append(AwarenessSignal(
                    signal_id=f"aware_claude_slow_{datetime.utcnow().strftime('%Y%m%d%H%M')}",
                    category="model_performance",
                    name="claude_high_latency",
                    severity="warning",
                    current_value=p95_latency,
                    threshold=6000,
                    description=f"Claude P95 latency is {p95_latency}ms — exceeds 6s threshold.",
                    recommended_action="AMIL: route teaching tasks to GPT-4o-mini temporarily",
                    requires_human=False,
                    detected_at=datetime.utcnow(),
                ))

        return signals

    # ── Signal Publisher ────────────────────────────────────────────────────

    async def _publish_signals(self, signals: list[AwarenessSignal]) -> None:
        for signal in signals:
            event_type = f"p11.awareness.{signal.category}.{signal.severity}"
            await self.hermes.publish(event_type, signal.__dict__)

            # Critical signals requiring human: go directly to HumanApprovalGate
            if signal.requires_human and signal.severity == "critical":
                await self.hermes.publish_human_gate(
                    gate_type="awareness_critical",
                    principal="charles_earl_lipshay",
                    context={
                        "signal": signal.name,
                        "description": signal.description,
                        "recommended_action": signal.recommended_action,
                    },
                )
```

---

## 3. Awareness Dashboard (Slack)

The Awareness Engine surfaces its most important metrics as a Slack report posted to a dedicated `#acss-awareness` channel:

```python
# acss/p011/engines/awareness/slack_dashboard.py
"""
Posts a real-time awareness dashboard to Slack every hour.
Shows learner engagement, pipeline health, infrastructure status, and model performance.
"""

from __future__ import annotations
from datetime import datetime
from typing import Any


class SlackAwarenessDashboard:
    """Formats and posts the ACSS awareness dashboard to Slack."""

    CHANNEL = "#acss-awareness"

    def __init__(self, slack_client: Any, fabric: Any, crm: Any, amil: Any) -> None:
        self.slack = slack_client
        self.fabric = fabric
        self.crm = crm
        self.amil = amil

    async def post_hourly_report(self) -> None:
        learner = await self.crm.get_engagement_metrics(window_days=1)
        pipeline = await self.fabric.get_pipeline_metrics(window_hours=1)
        models = await self.amil.get_performance_metrics(window_minutes=60)

        # Build Block Kit dashboard
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🤖 ACSS Awareness Report — {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC",
                },
            },
            {"type": "divider"},
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*👤 Active Learners (24h)*\n{learner['daily_active']}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*📚 Lessons Completed (24h)*\n{learner['lessons_completed_today']}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*🏅 Credentials Issued (7d)*\n{learner['credentials_issued_week']}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*🎫 Open Support Cases*\n{learner['open_support_cases']}",
                    },
                ],
            },
            {"type": "divider"},
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": (
                            f"*🔧 CI Success Rate*\n"
                            f"{'✅' if pipeline['ci_success_rate'] >= 0.90 else '⚠️'} "
                            f"{pipeline['ci_success_rate']:.0%}"
                        ),
                    },
                    {
                        "type": "mrkdwn",
                        "text": (
                            f"*🧠 RAG Quality*\n"
                            f"{'✅' if pipeline.get('rag_mean_relevance', 1.0) >= 0.70 else '⚠️'} "
                            f"{pipeline.get('rag_mean_relevance', 1.0):.2f}"
                        ),
                    },
                ],
            },
        ]

        await self.slack.client.chat_postMessage(
            channel=self.CHANNEL,
            blocks=blocks,
            text="ACSS Hourly Awareness Report",
        )
```

---

## 4. Awareness → Fabric Learning Loop

Every signal the Awareness Engine detects feeds back into Fabric as a training signal:

```
AwarenessEngine detects signal
         │
         ▼
Hermes event published (p11.awareness.*)
         │
    ┌────▼────────────────────────────────┐
    │ Engine that handles it (ACD, E3,   │
    │ CRM Support, lippytm clone, etc.)  │
    └────┬────────────────────────────────┘
         │ Resolution event published
         ▼
    Fabric records:
    - What signal triggered action
    - What action was taken
    - Did it resolve the issue?
    - How long did resolution take?
         │
         ▼
    Fabric pattern confidence updated
    Future similar signals → better recommendations
```

---

## 5. ACSS Integration Map

| Signal Category | ACSS System | Action |
|---|---|---|
| Learner engagement drop | Hermes → Engine 3 | Re-engagement curriculum generated |
| Support case spike | Hermes → HumanApprovalGate | Charles notified |
| CI failure rate high | Hermes → ACD PipelineGuardian | Self-healing triggered |
| RAG quality drop | Hermes → Fabric | KB re-index scheduled |
| Model latency high | Hermes → AMIL | Model routing table updated |
| Qdrant unreachable | Hermes → Slack CRM | Static KB fallback activated |
| Credential velocity zero | Hermes → Engine 3 + Slack | Learner engagement nudge |

---

## Further Reading

- 📄 [`docs/P011-ENGINE-001-prompt11-engines.md`](P011-ENGINE-001-prompt11-engines.md) — All 8 engines overview
- 📄 [`docs/P011-PLAN-001-curriculum-planner.md`](P011-PLAN-001-curriculum-planner.md) — Engine 3: receives re-engagement triggers from Awareness
- 📄 [`docs/autonomous-continuous-development.md`](autonomous-continuous-development.md) — ACD: pipeline health signals feed from Awareness
- 📄 [`docs/ai-model-intelligence-layer.md`](ai-model-intelligence-layer.md) — AMIL: model performance signals monitored by Awareness
- 📄 [`docs/slack-ai-crm-integration.md`](slack-ai-crm-integration.md) — Slack CRM: the delivery surface for Awareness dashboard
- 🏠 [`README.md`](../README.md) — Encyclopedia home

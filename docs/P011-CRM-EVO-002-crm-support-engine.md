# P011-CRM-EVO-002 — CRM Support Engine (Engine 8)

## The Memory of Every Learner Who Ever Built Something

> *"A great teacher never forgets a student. Engine 8 never forgets a learner — it knows what they've built, where they're stuck, when they're ready for the next level, and what to say to bring them back."*
> — lippytmai, Teach Mode

---

## Overview

**Engine 8: CRM Support (CRMSupportEngine)** is the relationship intelligence layer of the Prompt #11 pipeline. It maintains a full longitudinal profile for every learner, node operator, and contributor across the entire lippytm.ai ecosystem — from their first terminal session (B-001) through to deploying a full GESN Network node (A-100).

Engine 8 listens on the Hermes event bus for signals from Engines 4–7, updates learner CRM records, fires personalized Slack/email outreach, evaluates curriculum upgrade eligibility, tracks revenue events, and feeds aggregated insights back into Fabric for continuous system improvement.

| Property | Value |
|---|---|
| **Engine ID** | ENGINE-008 |
| **ACSS System** | Hermes + Fabric + Slack CRM |
| **Primary Clone** | `lippytmai` (Teach mode for outreach) / `lippytm` (data/infra) |
| **Approval Gate** | G13 HumanApprovalGate for revenue decisions ≥ $500 impact |
| **Input Sources** | Engine 7 (all badge/QEP events), GESN push (completion events), Blockchain (on-chain badge mints) |
| **Output Channels** | PostgreSQL CRM DB, Slack DMs, Email (via SMTP/SendGrid), Hermes Fabric log, GESN learner profile API |
| **Language** | Python 3.11+ |
| **Dependencies** | `asyncpg`, `sqlalchemy[asyncio]`, `slack-sdk`, `httpx`, `pydantic`, `sendgrid` |

---

## 1. Learner Data Model

Every learner in the CRM is represented by a `LearnerProfile` — the canonical record that accumulates across every book they read, every video they watch, every mission they complete, and every badge they earn.

```python
# docs/examples/p011_crm_data_model.py
"""
CRMSupportEngine — Engine 8 data models.
"""
from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CurriculumLevel(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    GRADUATE = "graduate"  # completed A-100 + GESN Genesis


class LearnerStatus(str, enum.Enum):
    ACTIVE = "active"
    AT_RISK = "at_risk"        # no activity for 7+ days
    CHURNED = "churned"        # no activity for 30+ days
    GRADUATED = "graduated"    # completed full track
    NODE_OPERATOR = "node_operator"  # running a GESN node


class BadgeRecord(BaseModel):
    badge_name: str
    badge_level: str                    # beginner / intermediate / advanced / gesn-*
    token_id: int
    contract_address: str
    chain: str = "base"
    tx_hash: str
    minted_at: datetime
    mission_id: Optional[str] = None
    ebook_id: Optional[str] = None      # e.g. "B-042"


class LearnerProfile(BaseModel):
    crm_learner_id: int
    wallet_address: Optional[str] = None
    slack_user_id: Optional[str] = None
    email: Optional[str] = None

    # Curriculum position
    current_level: CurriculumLevel = CurriculumLevel.BEGINNER
    current_ebook_id: str = "B-001"
    current_mission_id: Optional[str] = None
    completed_ebook_ids: list[str] = Field(default_factory=list)
    completed_mission_ids: list[str] = Field(default_factory=list)

    # Credentials
    badges: list[BadgeRecord] = Field(default_factory=list)
    badge_count: int = 0
    ccsll_level: int = 0                # 0=Curious → 5=Master
    cbsll_level: int = 0
    cll_level: int = 0

    # Engagement
    status: LearnerStatus = LearnerStatus.ACTIVE
    streak_days: int = 0
    last_activity_at: Optional[datetime] = None
    total_build_time_minutes: int = 0
    quiz_pass_rate: float = 0.0         # rolling 30-day average

    # Revenue
    lifetime_value_usd: float = 0.0
    last_purchase_at: Optional[datetime] = None
    upsell_eligible: bool = False
    gesn_node_operator: bool = False

    # ACSS metadata
    hermes_routing_tag: str = "lippytmai"
    fabric_pattern_confidence: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## 2. PostgreSQL Schema

Engine 8 persists all learner data in a PostgreSQL database (the same cluster as the Slack AI CRM in `slack-ai-crm-integration.md`):

```sql
-- Engine 8: CRM Support learner tables
-- docs/examples/engine8_schema.sql

CREATE TABLE learners (
    crm_learner_id    SERIAL PRIMARY KEY,
    wallet_address    VARCHAR(42) UNIQUE,
    slack_user_id     VARCHAR(32) UNIQUE,
    email             VARCHAR(255),
    current_level     VARCHAR(20) NOT NULL DEFAULT 'beginner',
    current_ebook_id  VARCHAR(10) NOT NULL DEFAULT 'B-001',
    status            VARCHAR(20) NOT NULL DEFAULT 'active',
    streak_days       INTEGER NOT NULL DEFAULT 0,
    badge_count       INTEGER NOT NULL DEFAULT 0,
    ccsll_level       SMALLINT NOT NULL DEFAULT 0,
    cbsll_level       SMALLINT NOT NULL DEFAULT 0,
    cll_level         SMALLINT NOT NULL DEFAULT 0,
    quiz_pass_rate    NUMERIC(5,4) NOT NULL DEFAULT 0,
    lifetime_value    NUMERIC(12,2) NOT NULL DEFAULT 0,
    upsell_eligible   BOOLEAN NOT NULL DEFAULT FALSE,
    node_operator     BOOLEAN NOT NULL DEFAULT FALSE,
    last_activity_at  TIMESTAMPTZ,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE learner_badges (
    id               SERIAL PRIMARY KEY,
    crm_learner_id   INTEGER REFERENCES learners(crm_learner_id) ON DELETE CASCADE,
    badge_name       VARCHAR(255) NOT NULL,
    badge_level      VARCHAR(50) NOT NULL,
    token_id         INTEGER NOT NULL,
    contract_address VARCHAR(42) NOT NULL,
    chain            VARCHAR(32) NOT NULL DEFAULT 'base',
    tx_hash          VARCHAR(66) NOT NULL UNIQUE,
    mission_id       VARCHAR(50),
    ebook_id         VARCHAR(10),
    minted_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE learner_completions (
    id               SERIAL PRIMARY KEY,
    crm_learner_id   INTEGER REFERENCES learners(crm_learner_id) ON DELETE CASCADE,
    content_type     VARCHAR(20) NOT NULL,   -- 'ebook' | 'mission' | 'video'
    content_id       VARCHAR(50) NOT NULL,
    completed_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    quiz_score       NUMERIC(5,4),
    build_minutes    INTEGER DEFAULT 0
);

CREATE TABLE crm_events (
    id               SERIAL PRIMARY KEY,
    crm_learner_id   INTEGER REFERENCES learners(crm_learner_id) ON DELETE CASCADE,
    event_type       VARCHAR(50) NOT NULL,
    payload          JSONB NOT NULL DEFAULT '{}',
    source_engine    VARCHAR(30) NOT NULL,
    correlation_id   VARCHAR(64) NOT NULL,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_learners_status ON learners(status);
CREATE INDEX idx_learners_level ON learners(current_level);
CREATE INDEX idx_learners_upsell ON learners(upsell_eligible) WHERE upsell_eligible = TRUE;
CREATE INDEX idx_crm_events_learner ON crm_events(crm_learner_id, created_at DESC);
```

---

## 3. CRMSupportEngine — Python Implementation

```python
# docs/examples/p011_crm_support_engine.py
"""
CRMSupportEngine — Engine 8 of the Prompt #11 pipeline.
Processes ACSS events to maintain learner profiles and drive engagement.
"""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

import asyncpg
import httpx
from slack_sdk.web.async_client import AsyncWebClient

logger = logging.getLogger("engine8.crm")

UTC = timezone.utc

# Level upgrade thresholds
LEVEL_THRESHOLDS = {
    "beginner":     {"ebooks_required": 10, "badges_required": 3, "quiz_pass_rate": 0.70},
    "intermediate": {"ebooks_required": 30, "badges_required": 8, "quiz_pass_rate": 0.75},
    "advanced":     {"ebooks_required": 60, "badges_required": 15, "quiz_pass_rate": 0.80},
}


class CRMSupportEngine:
    """
    Engine 8: CRM Support Engine.
    Maintains learner profiles, fires engagement outreach, evaluates upgrades.
    """

    def __init__(
        self,
        db_dsn: str,
        slack_token: str,
        hermes_endpoint: str,
        gesn_api_endpoint: str,
        sendgrid_api_key: str,
    ) -> None:
        self.db_dsn = db_dsn
        self.slack = AsyncWebClient(token=slack_token)
        self.hermes_endpoint = hermes_endpoint
        self.gesn_api_endpoint = gesn_api_endpoint
        self.sendgrid_api_key = sendgrid_api_key
        self._pool: Optional[asyncpg.Pool] = None

    async def connect(self) -> None:
        self._pool = await asyncpg.create_pool(self.db_dsn, min_size=2, max_size=10)
        logger.info("Engine8: CRM database pool connected")

    async def close(self) -> None:
        if self._pool:
            await self._pool.close()

    # ── Event Handlers (called by Engine 7 / Hermes) ─────────────────────────

    async def on_badge_minted(
        self,
        crm_learner_id: int,
        badge_name: str,
        badge_level: str,
        token_id: int,
        contract_address: str,
        tx_hash: str,
        ebook_id: Optional[str] = None,
        mission_id: Optional[str] = None,
        correlation_id: str = "",
    ) -> None:
        """Process a BADGE_MINTED event from Engine 7."""
        async with self._pool.acquire() as conn:
            # 1. Insert badge record
            await conn.execute(
                """
                INSERT INTO learner_badges
                    (crm_learner_id, badge_name, badge_level, token_id,
                     contract_address, tx_hash, ebook_id, mission_id)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                ON CONFLICT (tx_hash) DO NOTHING
                """,
                crm_learner_id, badge_name, badge_level,
                token_id, contract_address, tx_hash, ebook_id, mission_id,
            )

            # 2. Update learner badge count + last activity
            row = await conn.fetchrow(
                """
                UPDATE learners
                SET badge_count = badge_count + 1,
                    last_activity_at = NOW(),
                    streak_days = streak_days + 1,
                    updated_at = NOW()
                WHERE crm_learner_id = $1
                RETURNING badge_count, current_level, slack_user_id, email
                """,
                crm_learner_id,
            )

            # 3. Log CRM event
            await conn.execute(
                """
                INSERT INTO crm_events (crm_learner_id, event_type, payload, source_engine, correlation_id)
                VALUES ($1, 'BADGE_MINTED', $2, 'ENGINE-008', $3)
                """,
                crm_learner_id,
                {"badge_name": badge_name, "token_id": token_id, "tx_hash": tx_hash},
                correlation_id,
            )

        # 4. Send congratulations outreach
        if row["slack_user_id"]:
            await self._slack_badge_congrats(
                row["slack_user_id"], badge_name, token_id, row["badge_count"]
            )

        # 5. Evaluate upsell / level upgrade
        await self._evaluate_upgrade(crm_learner_id)

        logger.info("Engine8: badge_minted processed for learner %d — %s", crm_learner_id, badge_name)

    async def on_ebook_completed(
        self,
        crm_learner_id: int,
        ebook_id: str,
        quiz_score: float,
        build_minutes: int,
        correlation_id: str = "",
    ) -> None:
        """Process an ebook completion event."""
        async with self._pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO learner_completions
                    (crm_learner_id, content_type, content_id, quiz_score, build_minutes)
                VALUES ($1, 'ebook', $2, $3, $4)
                """,
                crm_learner_id, ebook_id, quiz_score, build_minutes,
            )
            # Update rolling quiz pass rate (30-day window)
            await conn.execute(
                """
                UPDATE learners
                SET total_build_time_minutes = total_build_time_minutes + $2,
                    last_activity_at = NOW(),
                    updated_at = NOW()
                WHERE crm_learner_id = $1
                """,
                crm_learner_id, build_minutes,
            )
            # Recalculate quiz pass rate
            avg = await conn.fetchval(
                """
                SELECT AVG(quiz_score)
                FROM learner_completions
                WHERE crm_learner_id = $1
                  AND content_type = 'ebook'
                  AND completed_at > NOW() - INTERVAL '30 days'
                """,
                crm_learner_id,
            )
            await conn.execute(
                "UPDATE learners SET quiz_pass_rate = $2 WHERE crm_learner_id = $1",
                crm_learner_id, float(avg or 0.0),
            )

        await self._evaluate_upgrade(crm_learner_id)

    async def on_at_risk_detected(self, crm_learner_id: int) -> None:
        """Called by Engine 6 when a learner has been inactive for 7+ days."""
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT slack_user_id, email, current_ebook_id FROM learners WHERE crm_learner_id = $1",
                crm_learner_id,
            )
        if not row:
            return
        await conn.execute(
            "UPDATE learners SET status = 'at_risk', updated_at = NOW() WHERE crm_learner_id = $1",
            crm_learner_id,
        )
        if row["slack_user_id"]:
            await self.slack.chat_postMessage(
                channel=row["slack_user_id"],
                text=(
                    f":wave: Hey! We noticed you haven't continued with *{row['current_ebook_id']}* in a while. "
                    f"Your streak is waiting — pick up where you left off and earn your next badge! :trophy:"
                ),
            )
        logger.info("Engine8: at_risk outreach sent to learner %d", crm_learner_id)

    # ── Upgrade Evaluation ───────────────────────────────────────────────────

    async def _evaluate_upgrade(self, crm_learner_id: int) -> None:
        """Check if learner meets threshold for curriculum level upgrade."""
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT l.current_level, l.badge_count, l.quiz_pass_rate, l.slack_user_id,
                       COUNT(c.id) AS completed_ebooks
                FROM learners l
                LEFT JOIN learner_completions c
                       ON c.crm_learner_id = l.crm_learner_id AND c.content_type = 'ebook'
                WHERE l.crm_learner_id = $1
                GROUP BY l.current_level, l.badge_count, l.quiz_pass_rate, l.slack_user_id
                """,
                crm_learner_id,
            )
        if not row:
            return

        current = row["current_level"]
        thresholds = LEVEL_THRESHOLDS.get(current)
        if not thresholds:
            return  # already at graduate level

        if (
            row["completed_ebooks"] >= thresholds["ebooks_required"]
            and row["badge_count"] >= thresholds["badges_required"]
            and float(row["quiz_pass_rate"]) >= thresholds["quiz_pass_rate"]
        ):
            next_levels = {"beginner": "intermediate", "intermediate": "advanced", "advanced": "graduate"}
            next_level = next_levels[current]
            async with self._pool.acquire() as conn:
                await conn.execute(
                    "UPDATE learners SET current_level = $2, upsell_eligible = TRUE, updated_at = NOW() "
                    "WHERE crm_learner_id = $1",
                    crm_learner_id, next_level,
                )
            if row["slack_user_id"]:
                await self.slack.chat_postMessage(
                    channel=row["slack_user_id"],
                    text=(
                        f":star2: Congratulations! You've unlocked the *{next_level.upper()}* track! "
                        f"Continue your journey and earn even more advanced credentials. "
                        f"Check your GESN dashboard to see your new missions!"
                    ),
                )
            logger.info("Engine8: learner %d upgraded to %s", crm_learner_id, next_level)

    # ── Slack Outreach ────────────────────────────────────────────────────────

    async def _slack_badge_congrats(
        self,
        slack_user_id: str,
        badge_name: str,
        token_id: int,
        total_badges: int,
    ) -> None:
        await self.slack.chat_postMessage(
            channel=slack_user_id,
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            f":medal: *Badge Earned: {badge_name}*\n"
                            f"Token ID: `#{token_id}` · Total badges: *{total_badges}*\n"
                            f"Your credential is on-chain on Base. Keep building! :rocket:"
                        ),
                    },
                },
                {"type": "divider"},
            ],
            text=f"Badge earned: {badge_name}",
        )

    # ── Nightly Churn Scan ────────────────────────────────────────────────────

    async def run_nightly_churn_scan(self) -> None:
        """
        Run nightly: mark at_risk / churned learners and trigger re-engagement outreach.
        Called by APScheduler at 02:00 UTC.
        """
        async with self._pool.acquire() as conn:
            # Mark churned (30+ days inactive)
            churned = await conn.fetch(
                """
                UPDATE learners
                SET status = 'churned', updated_at = NOW()
                WHERE status IN ('active', 'at_risk')
                  AND last_activity_at < NOW() - INTERVAL '30 days'
                RETURNING crm_learner_id
                """
            )
            # Mark at_risk (7+ days inactive but not yet churned)
            at_risk = await conn.fetch(
                """
                UPDATE learners
                SET status = 'at_risk', updated_at = NOW()
                WHERE status = 'active'
                  AND last_activity_at < NOW() - INTERVAL '7 days'
                RETURNING crm_learner_id
                """
            )

        await asyncio.gather(
            *[self.on_at_risk_detected(r["crm_learner_id"]) for r in at_risk],
            return_exceptions=True,
        )

        logger.info(
            "Engine8 nightly scan: %d churned, %d at_risk processed",
            len(churned), len(at_risk),
        )

    # ── Fabric Reporting ──────────────────────────────────────────────────────

    async def report_cohort_metrics_to_fabric(self) -> None:
        """Push aggregated CRM metrics to Fabric for pattern learning."""
        async with self._pool.acquire() as conn:
            metrics = await conn.fetchrow(
                """
                SELECT
                    COUNT(*) FILTER (WHERE status = 'active')       AS active_learners,
                    COUNT(*) FILTER (WHERE status = 'at_risk')      AS at_risk_learners,
                    COUNT(*) FILTER (WHERE status = 'churned')      AS churned_learners,
                    COUNT(*) FILTER (WHERE upsell_eligible = TRUE)  AS upsell_eligible,
                    AVG(quiz_pass_rate)                             AS avg_quiz_pass_rate,
                    AVG(streak_days)                                AS avg_streak_days,
                    SUM(lifetime_value)                             AS total_ltv
                FROM learners
                """
            )
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{self.hermes_endpoint}/fabric/metrics",
                json={"engine": "ENGINE-008", "metrics": dict(metrics)},
                timeout=10,
            )
        logger.info("Engine8: cohort metrics reported to Fabric")
```

---

## 4. Engagement Outreach Templates

Engine 8 uses a template library for all learner-facing messages. Every template is reviewed through the 13-gate Quality Review process (Engine 5) before activation.

| Template ID | Trigger | Channel | Clone Identity |
|---|---|---|---|
| `CRM-BADGE-001` | Badge minted | Slack DM | `lippytmai` |
| `CRM-UPGRADE-001` | Level upgrade unlocked | Slack DM | `lippytmai` |
| `CRM-ATRISK-001` | 7-day inactivity | Slack DM | `lippytmai` |
| `CRM-REENGAGED-001` | At-risk learner completes content | Slack DM | `lippytmai` |
| `CRM-CHURN-001` | 30-day inactivity | Email (SendGrid) | `lippytmai` |
| `CRM-UPSELL-001` | Upsell eligibility met | Slack DM + Email | `lippytmai` |
| `CRM-GESN-NODE-001` | GESN node operator application | Charles review | `lippytm` (GitHub) |
| `CRM-GRADUATION-001` | A-100 + GESN Genesis completed | Slack DM + Email | Charles (personal) |

All outreach uses `lippytmai` voice (Teach mode). `CRM-GRADUATION-001` is the only template personally sent by Charles. *[Reality — Charles drafts this template; `lippytmai` triggers delivery]*

---

## 5. Integration Map

```
Engine 5 (QR)       ──QEP_COMPLETE──────────► Engine 7 ──BADGE_MINTED──► Engine 8
                                                                           │
GESN Push Service   ──MISSION_COMPLETE─────────────────────────────────► Engine 8
                                                                           │
Blockchain (Base)   ──BadgeMinted event (on-chain)──────────────────────► Engine 8
                                                                           │
Engine 6 (Awareness)──AT_RISK signal───────────────────────────────────► Engine 8
                                                                           │
                                                              ┌────────────┘
                                                              │
                                          ┌─────────────┬────┴────────────┐
                                          ▼             ▼                 ▼
                                    PostgreSQL     Slack DM          Hermes/Fabric
                                    CRM Update     Outreach          Metrics Log
```

---

## 6. Revenue Integrity (G11)

Engine 8 enforces the Learning-to-Earning boundary defined in `P011-EBOOK-000`:

- **No learner data is sold** to third parties. Ever.
- Upsell recommendations are generated internally from curriculum progress signals only.
- Revenue events ≥ $500 impact trigger G13 HumanApprovalGate — Charles must approve any bulk discount, affiliate payout, or node licensing fee above this threshold.
- All revenue events are logged to the `crm_events` table with `source_engine = 'ENGINE-008'` and a `correlation_id` traceable back to the original ebook/badge event.

*[Reality — the $500 threshold is configurable; default is $500 USD equivalent at time of event]*

---

## Further Reading

- **[Engine 7: Repo Communications](P011-REPOCOMMS-001-repo-communications-engine.md)** — the broadcast layer that delivers events to Engine 8
- **[Engine 6: Awareness Dashboard](P011-AWARE-001-awareness-dashboard.md)** — the monitoring engine that detects at-risk learners and notifies Engine 8
- **[Engine 5: Quality Review](P011-QR-001-quality-review-engine.md)** — G11 Revenue Integrity gate that Engine 8 enforces
- **[Slack AI CRM Integration](slack-ai-crm-integration.md)** — the shared Slack infrastructure and PostgreSQL cluster
- **[GESN Platform](P011-GESN-001-gamer-educational-systems-networks.md)** — the mission completion events that feed Engine 8
- **[All 8 P011 Engines Overview](P011-ENGINE-001-prompt11-engines.md)** — the complete engine map
- **[← README](../README.md)** — main encyclopedia index

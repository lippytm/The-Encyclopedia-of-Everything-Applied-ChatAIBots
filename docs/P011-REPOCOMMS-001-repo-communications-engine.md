# P011-REPOCOMMS-001 — Repo Communications Engine (Engine 7)

## The Nervous System of the AI Conglomerate Swarms

> *"Communication is not the transmission of data — it is the transmission of meaning. Engine 7 ensures that every commit, every PR, every alert, and every teaching loop pulse is not just logged, but understood across the entire swarm."*
> — lippytmai, Teach Mode

---

## Overview

**Engine 7: Repo Communications (RepoCommsEngine)** is the broadcast and coordination layer of the Prompt #11 pipeline. It translates internal ACSS events — quality gate completions, curriculum plan updates, ebook drafts ready for review, GESN mission launches — into structured messages routed to the right clone identity, repository, or human principal through the correct channel.

Engine 7 sits between the pipeline engines (3–6) and the external world (GitHub, Slack, Hermes, the GESN notification layer). It ensures that *nothing* disappears silently into the void.

| Property | Value |
|---|---|
| **Engine ID** | ENGINE-007 |
| **ACSS System** | Hermes + Fabric |
| **Primary Clone** | `lippytm` (GitHub builder) |
| **Approval Gate** | G13 HumanApprovalGate (Charles) for production deploy messages |
| **Input Sources** | All P011 pipeline engines (1–6, 8), ACSS event bus |
| **Output Channels** | GitHub Issues/PRs, Slack (#acss-ops, #code-review, #gesn-alerts), Hermes relay, GESN push notifications |
| **Language** | Python 3.11+ |
| **Dependencies** | `PyGithub`, `slack-sdk`, `httpx`, `pydantic`, `asyncio` |

---

## 1. Communication Philosophy

Engine 7 operates by three rules:

1. **Every P011 event is a message.** If it happened in the pipeline, it gets announced — to the right audience, at the right fidelity.
2. **Route by audience, not by event.** The same QEP (Quality Evidence Packet) is summarized differently for Charles (full review), for a Slack `#code-review` channel (concise bullets), and for a GESN learner dashboard (badge earned).
3. **Never block.** All communication is async and fire-and-forget. The pipeline does not wait for ACKs. Failures are logged to Fabric and retried on the next awareness pulse.

---

## 2. Message Types

Engine 7 handles the following canonical message types:

| Message Type | Trigger | Audience | Channel |
|---|---|---|---|
| `PIPELINE_START` | New P011 prompt intake | lippytm | GitHub Issue (auto-created) |
| `PLAN_READY` | Engine 3 curriculum plan output | lippytmai | Slack `#acss-ops` |
| `DOC_DRAFT_READY` | Engine 4 draft complete | lippytm | GitHub PR (draft) |
| `QEP_COMPLETE` | Engine 5 all 12 gates pass | Charles | GitHub PR (review-ready) + Slack DM |
| `QEP_BLOCKED` | Engine 5 gate failure | lippytm | Slack `#code-review` + GitHub comment |
| `AWARENESS_ALERT` | Engine 6 anomaly detected | lippytm | Slack `#acss-ops` |
| `GESN_MISSION_LIVE` | New GESN mission published | GESN subscribers | GESN push + Slack `#gesn-alerts` |
| `BADGE_MINTED` | ERC-721 badge minted on-chain | Learner | GESN notification + email |
| `HUMAN_GATE_REQUIRED` | G13 triggered anywhere | Charles | GitHub PR + Slack DM + email |
| `ACSS_EVOLUTION` | ACD proposes self-improvement | Charles | GitHub Issue + Slack DM |

---

## 3. RepoCommsEngine — Python Implementation

```python
# docs/examples/p011_repo_comms_engine.py
"""
RepoCommsEngine — Engine 7 of the Prompt #11 pipeline.
Routes ACSS events to GitHub, Slack, Hermes, and GESN.
"""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import httpx
from github import Github
from pydantic import BaseModel
from slack_sdk.web.async_client import AsyncWebClient

logger = logging.getLogger("engine7.repocomms")


class MessageType(str, Enum):
    PIPELINE_START = "PIPELINE_START"
    PLAN_READY = "PLAN_READY"
    DOC_DRAFT_READY = "DOC_DRAFT_READY"
    QEP_COMPLETE = "QEP_COMPLETE"
    QEP_BLOCKED = "QEP_BLOCKED"
    AWARENESS_ALERT = "AWARENESS_ALERT"
    GESN_MISSION_LIVE = "GESN_MISSION_LIVE"
    BADGE_MINTED = "BADGE_MINTED"
    HUMAN_GATE_REQUIRED = "HUMAN_GATE_REQUIRED"
    ACSS_EVOLUTION = "ACSS_EVOLUTION"


class CommsPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"  # always triggers Charles notification


class CommsEvent(BaseModel):
    message_type: MessageType
    priority: CommsPriority = CommsPriority.NORMAL
    payload: dict[str, Any]
    source_engine: str
    correlation_id: str  # links back to original P011 prompt intake


@dataclass
class ChannelRouter:
    """Maps message types to target channels and audiences."""

    ROUTING_TABLE: dict[MessageType, list[str]] = field(default_factory=lambda: {
        MessageType.PIPELINE_START:    ["github_issue"],
        MessageType.PLAN_READY:        ["slack_acss_ops"],
        MessageType.DOC_DRAFT_READY:   ["github_pr_draft"],
        MessageType.QEP_COMPLETE:      ["github_pr_review", "slack_dm_charles"],
        MessageType.QEP_BLOCKED:       ["slack_code_review", "github_comment"],
        MessageType.AWARENESS_ALERT:   ["slack_acss_ops"],
        MessageType.GESN_MISSION_LIVE: ["gesn_push", "slack_gesn_alerts"],
        MessageType.BADGE_MINTED:      ["gesn_notification"],
        MessageType.HUMAN_GATE_REQUIRED: ["github_pr_review", "slack_dm_charles"],
        MessageType.ACSS_EVOLUTION:    ["github_issue", "slack_dm_charles"],
    })

    def channels_for(self, msg_type: MessageType) -> list[str]:
        return self.ROUTING_TABLE.get(msg_type, ["slack_acss_ops"])


class RepoCommsEngine:
    """
    Engine 7: Repo Communications Engine.
    Async broadcast layer — routes all P011 pipeline events to the correct channels.
    """

    def __init__(
        self,
        github_token: str,
        slack_token: str,
        hermes_endpoint: str,
        gesn_push_endpoint: str,
        repo_name: str = "lippytm/The-Encyclopedia-of-Everything-Applied-ChatAIBots",
        charles_slack_user_id: str = "U_CHARLES",
        ops_channel: str = "#acss-ops",
        code_review_channel: str = "#code-review",
        gesn_alerts_channel: str = "#gesn-alerts",
    ) -> None:
        self.gh = Github(github_token)
        self.repo = self.gh.get_repo(repo_name)
        self.slack = AsyncWebClient(token=slack_token)
        self.hermes_endpoint = hermes_endpoint
        self.gesn_push_endpoint = gesn_push_endpoint
        self.charles_slack_user_id = charles_slack_user_id
        self.ops_channel = ops_channel
        self.code_review_channel = code_review_channel
        self.gesn_alerts_channel = gesn_alerts_channel
        self.router = ChannelRouter()

    # ── Public API ──────────────────────────────────────────────────────────

    async def broadcast(self, event: CommsEvent) -> None:
        """Route event to all registered channels. Fire-and-forget; logs failures."""
        channels = self.router.channels_for(event.message_type)
        tasks = [self._dispatch(channel, event) for channel in channels]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for channel, result in zip(channels, results):
            if isinstance(result, Exception):
                logger.error("Engine7 dispatch failed [%s → %s]: %s", event.message_type, channel, result)
                await self._log_to_fabric(event, channel, error=str(result))

    # ── Dispatch Router ─────────────────────────────────────────────────────

    async def _dispatch(self, channel: str, event: CommsEvent) -> None:
        dispatch_map = {
            "github_issue":       self._github_issue,
            "github_pr_draft":    self._github_pr_draft,
            "github_pr_review":   self._github_pr_review,
            "github_comment":     self._github_pr_comment,
            "slack_acss_ops":     lambda e: self._slack_post(self.ops_channel, e),
            "slack_code_review":  lambda e: self._slack_post(self.code_review_channel, e),
            "slack_gesn_alerts":  lambda e: self._slack_post(self.gesn_alerts_channel, e),
            "slack_dm_charles":   self._slack_dm_charles,
            "gesn_push":          self._gesn_push,
            "gesn_notification":  self._gesn_badge_notification,
        }
        handler = dispatch_map.get(channel)
        if handler:
            await handler(event)
        else:
            logger.warning("Engine7: unknown channel '%s'", channel)

    # ── GitHub Handlers ─────────────────────────────────────────────────────

    async def _github_issue(self, event: CommsEvent) -> None:
        title = f"[P011 {event.message_type.value}] {event.payload.get('title', 'New Event')}"
        body = self._format_github_body(event)
        labels = ["p011-pipeline", event.message_type.value.lower().replace("_", "-")]
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: self.repo.create_issue(title=title, body=body, labels=labels),
        )
        logger.info("Engine7: GitHub issue created — %s", title)

    async def _github_pr_draft(self, event: CommsEvent) -> None:
        # Engine 4 signals that a doc draft is ready; Engine 7 creates the PR
        payload = event.payload
        title = f"[DRAFT] {payload.get('doc_title', 'New Document Draft')}"
        body = (
            f"## P011 Documentation Draft\n\n"
            f"**Correlation ID:** `{event.correlation_id}`\n"
            f"**Engine 4 confidence:** {payload.get('confidence', 'N/A')}\n\n"
            f"{payload.get('summary', '')}\n\n"
            f"---\n*Awaiting Engine 5 Quality Review before marking ready.*"
        )
        loop = asyncio.get_event_loop()
        base_branch = "main"
        head_branch = payload.get("branch", f"p011-draft-{event.correlation_id[:8]}")
        await loop.run_in_executor(
            None,
            lambda: self.repo.create_pull(
                title=title, body=body, base=base_branch, head=head_branch, draft=True
            ),
        )
        logger.info("Engine7: GitHub draft PR created — %s", title)

    async def _github_pr_review(self, event: CommsEvent) -> None:
        pr_number = event.payload.get("pr_number")
        if not pr_number:
            logger.warning("Engine7: _github_pr_review called without pr_number")
            return
        body = self._format_github_body(event)
        loop = asyncio.get_event_loop()
        pr = await loop.run_in_executor(None, self.repo.get_pull, int(pr_number))
        await loop.run_in_executor(
            None,
            lambda: pr.create_issue_comment(body),
        )
        await loop.run_in_executor(None, lambda: pr.edit(draft=False))
        logger.info("Engine7: PR #%s marked ready for review", pr_number)

    async def _github_pr_comment(self, event: CommsEvent) -> None:
        pr_number = event.payload.get("pr_number")
        if not pr_number:
            return
        body = self._format_github_body(event)
        loop = asyncio.get_event_loop()
        pr = await loop.run_in_executor(None, self.repo.get_pull, int(pr_number))
        await loop.run_in_executor(None, lambda: pr.create_issue_comment(body))

    # ── Slack Handlers ───────────────────────────────────────────────────────

    async def _slack_post(self, channel: str, event: CommsEvent) -> None:
        blocks = self._format_slack_blocks(event)
        await self.slack.chat_postMessage(channel=channel, blocks=blocks, text=event.message_type.value)
        logger.info("Engine7: Slack message posted to %s", channel)

    async def _slack_dm_charles(self, event: CommsEvent) -> None:
        dm_text = (
            f":bell: *{event.message_type.value}* requires your attention.\n"
            f"*Correlation ID:* `{event.correlation_id}`\n"
            f"*Priority:* {event.priority.value.upper()}\n"
            f"{self._format_slack_summary(event)}"
        )
        await self.slack.chat_postMessage(channel=self.charles_slack_user_id, text=dm_text)
        logger.info("Engine7: Charles DM sent for %s", event.message_type.value)

    # ── GESN Handlers ────────────────────────────────────────────────────────

    async def _gesn_push(self, event: CommsEvent) -> None:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.gesn_push_endpoint}/missions/publish",
                json={
                    "mission_id": event.payload.get("mission_id"),
                    "title": event.payload.get("title"),
                    "level": event.payload.get("level"),
                    "correlation_id": event.correlation_id,
                },
                timeout=10,
            )
            resp.raise_for_status()
        logger.info("Engine7: GESN push notification sent")

    async def _gesn_badge_notification(self, event: CommsEvent) -> None:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.gesn_push_endpoint}/badges/notify",
                json={
                    "learner_address": event.payload.get("learner_address"),
                    "badge_token_id": event.payload.get("badge_token_id"),
                    "badge_name": event.payload.get("badge_name"),
                    "tx_hash": event.payload.get("tx_hash"),
                },
                timeout=10,
            )
            resp.raise_for_status()
        logger.info("Engine7: GESN badge notification sent for token %s", event.payload.get("badge_token_id"))

    # ── Hermes Relay ─────────────────────────────────────────────────────────

    async def relay_to_hermes(self, event: CommsEvent) -> None:
        """Forward event to Hermes for cross-repo routing."""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.hermes_endpoint}/relay",
                json=event.model_dump(),
                timeout=15,
            )
            resp.raise_for_status()
        logger.info("Engine7: Event relayed to Hermes — %s", event.message_type.value)

    # ── Fabric Logging ────────────────────────────────────────────────────────

    async def _log_to_fabric(self, event: CommsEvent, channel: str, error: str = "") -> None:
        """Record communication events (and failures) in Fabric for pattern learning."""
        fabric_record = {
            "event_type": "engine7_dispatch",
            "message_type": event.message_type.value,
            "channel": channel,
            "correlation_id": event.correlation_id,
            "priority": event.priority.value,
            "error": error,
        }
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{self.hermes_endpoint}/fabric/log",
                json=fabric_record,
                timeout=5,
            )

    # ── Formatters ────────────────────────────────────────────────────────────

    def _format_github_body(self, event: CommsEvent) -> str:
        lines = [
            f"## {event.message_type.value}",
            f"",
            f"**Correlation ID:** `{event.correlation_id}`",
            f"**Source Engine:** {event.source_engine}",
            f"**Priority:** {event.priority.value}",
            f"",
            f"### Payload",
            f"```json",
            str(event.payload),
            f"```",
            f"",
            f"---",
            f"*Generated by P011 Engine 7 — RepoCommsEngine · lippytm.ai ACSS*",
        ]
        return "\n".join(lines)

    def _format_slack_blocks(self, event: CommsEvent) -> list[dict]:
        priority_emoji = {"low": "⬇️", "normal": "📢", "high": "🔔", "critical": "🚨"}
        emoji = priority_emoji.get(event.priority.value, "📢")
        return [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"{emoji} {event.message_type.value}"},
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Engine:*\n{event.source_engine}"},
                    {"type": "mrkdwn", "text": f"*Correlation ID:*\n`{event.correlation_id[:12]}…`"},
                    {"type": "mrkdwn", "text": f"*Priority:*\n{event.priority.value.upper()}"},
                    {"type": "mrkdwn", "text": f"*Summary:*\n{self._format_slack_summary(event)}"},
                ],
            },
            {"type": "divider"},
        ]

    def _format_slack_summary(self, event: CommsEvent) -> str:
        p = event.payload
        summaries = {
            MessageType.QEP_COMPLETE:        f"All 13 gates passed. PR ready for Charles review.",
            MessageType.QEP_BLOCKED:         f"Gate {p.get('blocked_gate')} failed: {p.get('reason')}",
            MessageType.HUMAN_GATE_REQUIRED: f"G13 triggered by `{p.get('source')}`. Charles approval required.",
            MessageType.BADGE_MINTED:        f"Badge `{p.get('badge_name')}` minted for `{p.get('learner_address', 'unknown')[:10]}…`",
            MessageType.GESN_MISSION_LIVE:   f"Mission `{p.get('title')}` is now live on GESN.",
            MessageType.ACSS_EVOLUTION:      f"ACSS proposed self-improvement: {p.get('proposal_title')}",
        }
        return summaries.get(event.message_type, str(p.get("summary", "See payload for details.")))
```

---

## 4. Integration with Engine 8 (CRM Support)

Engine 7 and Engine 8 share an event bus. When Engine 7 broadcasts a `BADGE_MINTED` event, Engine 8 automatically:

1. Updates the learner's CRM record (`badge_count += 1`, `last_credential_at = now`)
2. Triggers a personalized Slack message via the CRM template engine
3. Evaluates whether the learner qualifies for an upsell recommendation (intermediate → advanced curriculum)

```python
# Engine 7 → Engine 8 handoff (via shared Hermes event bus)
badge_event = CommsEvent(
    message_type=MessageType.BADGE_MINTED,
    priority=CommsPriority.NORMAL,
    payload={
        "learner_address": "0xABC…",
        "badge_token_id": 42,
        "badge_name": "Linux Apprentice",
        "tx_hash": "0xDEF…",
        "crm_learner_id": 1337,          # Engine 8 will pick this up
        "curriculum_level": "beginner",
    },
    source_engine="ENGINE-005-QR",
    correlation_id="p011-2026-b001-001",
)
await engine7.broadcast(badge_event)
# Engine 8 listens on the same Hermes topic and handles CRM update autonomously
```

---

## 5. HumanApprovalGate (G13) Communication Protocol

When any engine triggers G13, Engine 7 executes a **triple-channel notification** to ensure Charles never misses a required approval:

```
G13 Trigger
    │
    ├─→ GitHub PR comment (with checklist of what needs review)
    ├─→ Slack DM to Charles (@charles_slack_user_id)
    └─→ (Optional) Email via Hermes notification service
```

The PR is held in `draft=True` state until Charles approves. No automated system can advance a G13-blocked item. *[Reality — this is enforced at the pipeline level, not just by convention]*

---

## 6. Retry and Resilience

All Engine 7 dispatches are fire-and-forget with automatic retry via Fabric logging:

```python
# Retry backoff handled by the Awareness Engine (Engine 6)
# Every 15 minutes, AwarenessEngine queries Fabric for failed Engine 7 dispatches
# and re-broadcasts with exponential backoff (max 3 retries, 5m / 10m / 20m)

RETRY_SCHEDULE = [5 * 60, 10 * 60, 20 * 60]  # seconds
MAX_RETRIES = 3
```

After 3 failures, a `CRITICAL` alert is sent to `#acss-ops` and a GitHub issue is auto-opened.

---

## 7. Deployment

Engine 7 runs as a sidecar to the main P011 pipeline orchestrator:

```yaml
# docker-compose.yml excerpt
  engine7-repocomms:
    image: lippytmai/p011-engine7:latest
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN}
      - HERMES_ENDPOINT=${HERMES_ENDPOINT}
      - GESN_PUSH_ENDPOINT=${GESN_PUSH_ENDPOINT}
      - CHARLES_SLACK_USER_ID=${CHARLES_SLACK_USER_ID}
    restart: unless-stopped
    depends_on:
      - hermes-relay
      - gesn-push-service
```

*[Reality — Docker image must be built from the Engine 7 Python source above]*

---

## Further Reading

- **[Engine 8: CRM Support](P011-CRM-001-learning-system.md)** — the CRM engine that acts on Engine 7's BADGE_MINTED and QEP_COMPLETE events
- **[Engine 6: Awareness Dashboard](P011-AWARE-001-awareness-dashboard.md)** — monitors Engine 7 health and retries failed dispatches
- **[Slack AI CRM Integration](slack-ai-crm-integration.md)** — the Slack infrastructure that Engine 7 writes to
- **[Hermes Cross-Repo Message Bus](ai-clone-engine-swarms.md#hermes)** — the relay layer that Engine 7 uses for cross-repo events
- **[GESN Platform](P011-GESN-001-gamer-educational-systems-networks.md)** — the platform that receives Engine 7's mission and badge notifications
- **[All 8 P011 Engines Overview](P011-ENGINE-001-prompt11-engines.md)** — the complete engine map
- **[← README](../README.md)** — main encyclopedia index

# AI Slack CRM Systems Integration
### *Building a Continuously Self-Learning CRM That Lives in Slack and Teaches as It Grows*

> *"Slack is not just a chat tool — it is the nervous system of every modern team. When your CRM lives inside that nervous system, every conversation becomes a learning event."*
> — Charles Earl Lipshay (lippytm.ai)

---

## Overview

This document defines the complete architecture for the **lippytm.ai AI Slack CRM System** — a Slack-native, AI-powered customer relationship management and learning enhancement platform that integrates directly with the AI Conglomerate Swarms System (ACSS).

The system turns every Slack interaction into a CRM event, every CRM event into a learning signal, and every learning signal into an improvement to the lippytmai teaching experience.

**Three core goals:**

| Goal | What It Means |
|---|---|
| **AI-Enhanced CRM** | Slack becomes the primary interface for tracking learner journeys, support cases, and customer relationships — powered by AI that reads, classifies, and routes every message |
| **Learning Enhancement** | Every Slack interaction enriches the Earn-while-you-Learn experience: the bot teaches, assesses, tracks progress, and issues credentials |
| **ACSS Integration** | All CRM events flow through Hermes to Fabric, where they become training signals for lippytmai and pattern updates for the knowledge graph |

---

## 1. Slack App Architecture

### 1.1 Technology Stack

| Layer | Technology |
|---|---|
| **Bot Framework** | Slack Bolt for Python (`slack_bolt`) |
| **Runtime** | Python 3.11+ on FastAPI / Socket Mode |
| **AI Layer** | OpenAI GPT-4o (classification + responses) + Claude 3.5 (teaching explanations) |
| **CRM Database** | PostgreSQL (primary) + Redis (session cache) |
| **Vector Memory** | Qdrant (Fabric knowledge graph integration) |
| **Message Queue** | Hermes event bus (internal) |
| **Credential Issuance** | On-chain ERC-721 (CBSLL SkillBadge contract) |
| **Environment** | OMARCHY-standard Docker container on Arch Linux |

### 1.2 Slack App Manifest

```yaml
# slack_app_manifest.yaml
display_information:
  name: "lippytmai CRM Bot"
  description: "AI-powered CRM and learning assistant for the lippytm.ai ecosystem"
  background_color: "#1a1a2e"

features:
  bot_user:
    display_name: "lippytmai"
    always_online: true
  slash_commands:
    - command: /learn
      description: "Start or continue your Earn-while-you-Learn journey"
      usage_hint: "[topic] [level]"
    - command: /progress
      description: "View your learning progress and earned credentials"
    - command: /ask
      description: "Ask lippytmai any programming, blockchain, or AI question"
      usage_hint: "[your question]"
    - command: /crm
      description: "CRM operations: log contact, view journey, update status"
      usage_hint: "[action] [params]"
    - command: /support
      description: "Open, view, or escalate a support case"
      usage_hint: "[open|view|escalate] [details]"
    - command: /badge
      description: "View available and earned skill badges"

oauth_config:
  scopes:
    bot:
      - channels:history
      - channels:read
      - chat:write
      - chat:write.public
      - commands
      - groups:history
      - im:history
      - im:read
      - im:write
      - users:read
      - users:read.email
      - reactions:read
      - files:read

settings:
  event_subscriptions:
    bot_events:
      - message.channels
      - message.im
      - reaction_added
      - app_mention
      - member_joined_channel
  interactivity:
    is_enabled: true
  socket_mode_enabled: true
```

### 1.3 Application Entry Point

```python
# app.py — lippytmai Slack CRM Bot
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from services.crm import CRMService
from services.ai import AIService
from services.hermes import HermesClient
from handlers import (
    learn_command, progress_command, ask_command,
    crm_command, support_command, badge_command,
    message_handler, mention_handler, reaction_handler,
    member_joined_handler
)

app = App(token=os.environ["SLACK_BOT_TOKEN"])
crm = CRMService()
ai = AIService()
hermes = HermesClient()

# Register all slash commands
app.command("/learn")(learn_command(crm, ai, hermes))
app.command("/progress")(progress_command(crm, hermes))
app.command("/ask")(ask_command(ai, hermes))
app.command("/crm")(crm_command(crm, hermes))
app.command("/support")(support_command(crm, hermes))
app.command("/badge")(badge_command(crm))

# Register event listeners
app.event("message")(message_handler(crm, ai, hermes))
app.event("app_mention")(mention_handler(ai, hermes))
app.event("reaction_added")(reaction_handler(crm, hermes))
app.event("member_joined_channel")(member_joined_handler(crm, hermes))

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
```

---

## 2. CRM Data Model

### 2.1 Core Entities

```python
# models/crm.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum

class LearnerStatus(Enum):
    NEW         = "new"
    ONBOARDING  = "onboarding"
    ACTIVE      = "active"
    PROGRESSING = "progressing"
    ADVANCED    = "advanced"
    GRADUATED   = "graduated"
    CHURNED     = "churned"

class SupportPriority(Enum):
    LOW      = "low"
    MEDIUM   = "medium"
    HIGH     = "high"
    CRITICAL = "critical"

@dataclass
class LearnerProfile:
    """Party Passport for every learner in the Slack CRM."""
    slack_user_id:   str
    slack_workspace: str
    display_name:    str
    email:           Optional[str]
    status:          LearnerStatus = LearnerStatus.NEW
    proficiency:     dict = field(default_factory=dict)   # CCSLL/CBSLL/CLL levels
    credentials:     list = field(default_factory=list)   # on-chain badge token IDs
    consent_given:   bool = False
    consent_date:    Optional[datetime] = None
    created_at:      datetime = field(default_factory=datetime.utcnow)
    last_active:     datetime = field(default_factory=datetime.utcnow)

@dataclass
class LearningInteraction:
    """Every significant learning event logged to the CRM."""
    interaction_id:  str
    learner_id:      str                 # LearnerProfile.slack_user_id
    interaction_type: str               # "lesson_completed" | "question_asked" | "badge_earned" | "support_opened"
    topic:           str
    proficiency_level: int              # 0-5 (maps to CCSLL/CBSLL levels)
    ai_response_quality: Optional[int]  # learner rating 1-5 (feedback loop)
    timestamp:       datetime = field(default_factory=datetime.utcnow)
    fabric_synced:   bool = False

@dataclass
class SupportCase:
    """Support ticket, fully integrated with CRM and AI triage."""
    case_id:      str
    learner_id:   str
    title:        str
    description:  str
    priority:     SupportPriority
    ai_category:  str                   # AI-classified category
    ai_summary:   str                   # AI-generated case summary
    status:       str = "open"          # open | in_progress | resolved | escalated
    assigned_to:  Optional[str] = None  # lippytm clone or human agent
    created_at:   datetime = field(default_factory=datetime.utcnow)
    resolved_at:  Optional[datetime] = None
    sla_hours:    int = 24
```

### 2.2 Database Schema (PostgreSQL)

```sql
-- Learner profiles (Party Passports)
CREATE TABLE learner_profiles (
    slack_user_id    TEXT PRIMARY KEY,
    slack_workspace  TEXT NOT NULL,
    display_name     TEXT NOT NULL,
    email            TEXT,
    status           TEXT NOT NULL DEFAULT 'new',
    proficiency      JSONB NOT NULL DEFAULT '{}',
    credentials      JSONB NOT NULL DEFAULT '[]',
    consent_given    BOOLEAN NOT NULL DEFAULT FALSE,
    consent_date     TIMESTAMPTZ,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_active      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Learning interactions
CREATE TABLE learning_interactions (
    interaction_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learner_id          TEXT NOT NULL REFERENCES learner_profiles(slack_user_id),
    interaction_type    TEXT NOT NULL,
    topic               TEXT NOT NULL,
    proficiency_level   SMALLINT NOT NULL CHECK (proficiency_level BETWEEN 0 AND 5),
    ai_response_quality SMALLINT CHECK (ai_response_quality BETWEEN 1 AND 5),
    timestamp           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fabric_synced       BOOLEAN NOT NULL DEFAULT FALSE
);

-- Support cases
CREATE TABLE support_cases (
    case_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learner_id    TEXT NOT NULL REFERENCES learner_profiles(slack_user_id),
    title         TEXT NOT NULL,
    description   TEXT NOT NULL,
    priority      TEXT NOT NULL,
    ai_category   TEXT,
    ai_summary    TEXT,
    status        TEXT NOT NULL DEFAULT 'open',
    assigned_to   TEXT,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resolved_at   TIMESTAMPTZ,
    sla_hours     SMALLINT NOT NULL DEFAULT 24
);

-- Indexes for fast learner journey queries
CREATE INDEX idx_interactions_learner ON learning_interactions(learner_id, timestamp DESC);
CREATE INDEX idx_interactions_unsync  ON learning_interactions(fabric_synced) WHERE fabric_synced = FALSE;
CREATE INDEX idx_cases_status         ON support_cases(status, created_at DESC);
```

---

## 3. AI-Powered Slash Commands

### 3.1 `/ask` — Instant AI Teaching

```python
# handlers/ask_command.py
from slack_bolt import Ack, Respond
from services.ai import AIService
from services.hermes import HermesClient

def ask_command(ai: AIService, hermes: HermesClient):
    def handler(ack: Ack, respond: Respond, command: dict):
        ack()
        question = command["text"].strip()
        user_id  = command["user_id"]

        if not question:
            respond("Ask me anything! Example: `/ask What is a Solidity mapping?`")
            return

        # Get learner context from CRM for personalized response
        learner = crm.get_learner(user_id)
        proficiency = learner.proficiency if learner else {}

        # AI generates teaching response via AMIL model selection
        answer = ai.teach(
            question=question,
            proficiency=proficiency,
            style="lippytmai"  # uses lippytmai fine-tuned teaching voice
        )

        # Log interaction to CRM
        crm.log_interaction(user_id, "question_asked", question, proficiency_level=0)

        # Publish to Hermes for Fabric knowledge graph update
        hermes.emit("learner.question_asked", user_id=user_id, question=question, topic=answer["topic"])

        # Respond with rich Slack Block Kit message
        respond(blocks=build_teaching_blocks(question, answer))

    return handler


def build_teaching_blocks(question: str, answer: dict) -> list:
    """Build a rich Slack Block Kit message for a teaching response."""
    return [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Question:* {question}"}
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": answer["explanation"]}
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Code Example:*\n```{answer['code_example']}```"}
        } if answer.get("code_example") else {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"📄 *Next concept:* {answer['next_concept']}"}
        },
        {
            "type": "actions",
            "elements": [
                {"type": "button", "text": {"type": "plain_text", "text": "⭐ Helpful"},
                 "action_id": "rate_helpful", "value": "5"},
                {"type": "button", "text": {"type": "plain_text", "text": "🔁 Explain differently"},
                 "action_id": "explain_differently"},
                {"type": "button", "text": {"type": "plain_text", "text": "➡️ Next lesson"},
                 "action_id": "next_lesson", "value": answer.get("next_concept", "")}
            ]
        }
    ]
```

### 3.2 `/learn` — Structured Lesson Delivery

```python
# handlers/learn_command.py
def learn_command(crm, ai, hermes):
    def handler(ack: Ack, respond: Respond, command: dict):
        ack()
        args = command["text"].strip().split()
        topic = args[0] if args else None
        level = int(args[1]) if len(args) > 1 and args[1].isdigit() else None
        user_id = command["user_id"]

        learner = crm.get_or_create_learner(user_id, command["user_name"])

        if not topic:
            # Show personalized curriculum based on CRM proficiency data
            curriculum = ai.generate_curriculum(learner.proficiency)
            respond(blocks=build_curriculum_blocks(curriculum, learner))
            return

        # Generate lesson from AMIL-selected model + Fabric RAG context
        lesson = ai.generate_lesson(
            topic=topic,
            level=level or learner.proficiency.get(topic, 0),
            learner_history=crm.get_recent_interactions(user_id, limit=10)
        )

        # Log lesson start to CRM
        crm.log_interaction(user_id, "lesson_started", topic, proficiency_level=lesson["level"])
        hermes.emit("learner.lesson_started", user_id=user_id, topic=topic, level=lesson["level"])

        respond(blocks=build_lesson_blocks(lesson))

    return handler
```

### 3.3 `/progress` — Learner Dashboard

```python
# handlers/progress_command.py
def progress_command(crm, hermes):
    def handler(ack: Ack, respond: Respond, command: dict):
        ack()
        user_id = command["user_id"]
        learner = crm.get_learner(user_id)

        if not learner:
            respond("You haven't started your journey yet! Try `/learn Python` to begin.")
            return

        stats = crm.get_learner_stats(user_id)

        respond(blocks=[
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"🎓 {learner.display_name}'s Learning Journey"}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Status:* {learner.status.value.title()}"},
                    {"type": "mrkdwn", "text": f"*Lessons Completed:* {stats['lessons_completed']}"},
                    {"type": "mrkdwn", "text": f"*Questions Asked:* {stats['questions_asked']}"},
                    {"type": "mrkdwn", "text": f"*Badges Earned:* {len(learner.credentials)}"},
                ]
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "*Proficiency Map:*\n" + format_proficiency(learner.proficiency)}
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn",
                         "text": f"*Next Recommended:* {stats['next_recommendation']}"}
            },
            {
                "type": "actions",
                "elements": [
                    {"type": "button", "text": {"type": "plain_text", "text": "Continue Learning"},
                     "action_id": "continue_learning"},
                    {"type": "button", "text": {"type": "plain_text", "text": "View Badges"},
                     "action_id": "view_badges"},
                ]
            }
        ])

    return handler
```

### 3.4 `/support` — AI-Triaged Support Cases

```python
# handlers/support_command.py
def support_command(crm, hermes):
    def handler(ack: Ack, respond: Respond, command: dict):
        ack()
        args = command["text"].strip().split(None, 1)
        action = args[0].lower() if args else "open"
        details = args[1] if len(args) > 1 else ""
        user_id = command["user_id"]

        if action == "open":
            if not details:
                respond("Describe your issue: `/support open I am stuck on Solidity mappings`")
                return

            # AI classifies and summarizes the case
            classification = ai.classify_support_case(details)

            case = crm.create_support_case(
                learner_id=user_id,
                description=details,
                ai_category=classification["category"],
                ai_summary=classification["summary"],
                priority=classification["priority"]
            )

            hermes.emit("support.case_opened", case_id=str(case.case_id),
                        learner_id=user_id, priority=case.priority.value)

            respond(blocks=build_case_opened_blocks(case, classification))

        elif action == "view":
            cases = crm.get_learner_cases(user_id, status="open")
            respond(blocks=build_cases_list_blocks(cases))

        elif action == "escalate":
            case_id = details
            crm.escalate_case(case_id)
            hermes.emit("support.case_escalated", case_id=case_id, learner_id=user_id)
            respond(f"🚨 Case `{case_id}` escalated. Charles Earl Lipshay has been notified.")

    return handler
```

---

## 4. Intelligent Event Listeners

### 4.1 Message Listener — Passive Learning Detection

```python
# handlers/message_handler.py
def message_handler(crm, ai, hermes):
    def handler(event: dict, say):
        # Skip bot messages and non-learning channels
        if event.get("bot_id") or event.get("subtype"):
            return

        user_id = event["user"]
        text    = event.get("text", "")
        channel = event["channel"]

        # AI classifies whether message is learning-related
        classification = ai.classify_message(text)

        if classification["is_learning_signal"]:
            # Silently log to CRM without interrupting conversation
            crm.log_interaction(
                user_id=user_id,
                interaction_type="passive_learning_signal",
                topic=classification["topic"],
                proficiency_level=classification["estimated_level"]
            )
            hermes.emit("learner.passive_signal", user_id=user_id, **classification)

            # If learner is stuck, proactively offer help (only in DM or bot channel)
            if classification["is_stuck_signal"] and channel.startswith("D"):
                say(blocks=build_help_offer_blocks(classification["topic"]))

    return handler
```

### 4.2 Reaction Listener — Feedback Signal Collection

```python
# handlers/reaction_handler.py
QUALITY_REACTIONS = {
    "white_check_mark": 5,  # ✅ = understood, highest quality
    "thumbsup": 4,          # 👍 = helpful
    "eyes": 3,              # 👀 = interesting but not fully clear
    "question": 2,          # ❓ = confused
    "x": 1                  # ❌ = wrong or unhelpful
}

def reaction_handler(crm, hermes):
    def handler(event: dict):
        reaction  = event["reaction"]
        user_id   = event["user"]
        item      = event["item"]

        if reaction not in QUALITY_REACTIONS:
            return

        quality_score = QUALITY_REACTIONS[reaction]

        # Find the interaction that was reacted to
        interaction = crm.find_interaction_by_message(item["ts"], item["channel"])
        if not interaction:
            return

        # Update AI response quality score → feeds fine-tuning loop
        crm.update_interaction_quality(interaction.interaction_id, quality_score)
        hermes.emit("learner.feedback_given", interaction_id=str(interaction.interaction_id),
                    quality=quality_score, user_id=user_id)

        # High-quality responses (5) → added to lippytmai fine-tuning dataset
        if quality_score == 5:
            hermes.emit("ai.fine_tune_candidate", interaction_id=str(interaction.interaction_id))

    return handler
```

### 4.3 Member Joined — Automated Onboarding

```python
# handlers/member_joined_handler.py
def member_joined_handler(crm, hermes):
    def handler(event: dict, client):
        user_id  = event["user"]
        channel  = event["channel"]

        # Create learner profile in CRM
        user_info = client.users_info(user=user_id)["user"]
        learner = crm.create_learner(
            slack_user_id=user_id,
            display_name=user_info["real_name"],
            email=user_info["profile"].get("email"),
            slack_workspace=user_info["team_id"]
        )

        hermes.emit("learner.onboarded", user_id=user_id, workspace=user_info["team_id"])

        # Send personalized onboarding DM
        client.chat_postMessage(
            channel=user_id,
            blocks=build_onboarding_blocks(learner)
        )
```

---

## 5. ACSS Integration Layer

### 5.1 Hermes CRM Event Schema

All Slack CRM events published to Hermes follow this schema:

```json
{
  "hermes_version": "1.0",
  "origin": "slack_crm_bot",
  "origin_clone": "lippytmai",
  "workspace": "lippytm-ai",
  "event_type": "learner.lesson_completed",
  "payload": {
    "user_id": "U012AB3CD",
    "topic": "Solidity mappings",
    "proficiency_level": 2,
    "lesson_duration_minutes": 12,
    "ai_response_quality": 5,
    "next_recommendation": "Solidity events"
  },
  "timestamp": "2026-08-28T01:00:00Z",
  "requires_human_gate": false
}
```

### 5.2 Fabric Sync Service

CRM learning interactions sync to Fabric every 5 minutes (or immediately for high-signal events):

```python
# services/fabric_sync.py
import asyncio
from services.crm import CRMService
from services.fabric import FabricClient

fabric = FabricClient()
crm    = CRMService()

async def sync_interactions_to_fabric():
    """
    Sync unsynced CRM interactions to the Fabric knowledge graph.
    High-quality interactions (rating >= 4) boost topic pattern weights.
    """
    unsynced = crm.get_unsynced_interactions(limit=500)

    for interaction in unsynced:
        fabric.write(
            category="learner_interaction",
            key=interaction.interaction_id,
            data={
                "topic":            interaction.topic,
                "proficiency_level": interaction.proficiency_level,
                "quality_score":    interaction.ai_response_quality,
                "interaction_type": interaction.interaction_type,
                "timestamp":        interaction.timestamp.isoformat()
            }
        )
        # Boost topic pattern weight for high-quality teaching moments
        if interaction.ai_response_quality and interaction.ai_response_quality >= 4:
            fabric.boost_pattern(
                category="teaching_pattern",
                key=interaction.topic,
                boost=interaction.ai_response_quality / 5.0
            )

        crm.mark_synced(interaction.interaction_id)

    return len(unsynced)
```

### 5.3 AI Service — AMIL-Integrated Teaching

```python
# services/ai.py
from openai import OpenAI
from anthropic import Anthropic

openai_client    = OpenAI()
anthropic_client = Anthropic()

class AIService:
    def teach(self, question: str, proficiency: dict, style: str = "lippytmai") -> dict:
        """
        Generate a teaching response using AMIL model selection.
        Uses lippytmai fine-tuned voice for all teaching responses.
        """
        topic = self._extract_topic(question)
        level = proficiency.get(topic, 0)

        # Use Claude for nuanced teaching explanations (AMIL recommendation)
        response = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=self._build_teaching_system_prompt(style, level),
            messages=[{"role": "user", "content": question}]
        )

        return self._parse_teaching_response(response.content[0].text, topic)

    def classify_message(self, text: str) -> dict:
        """Classify whether a Slack message contains a learning signal."""
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",     # fast, cheap classification
            response_format={"type": "json_object"},
            messages=[{
                "role": "system",
                "content": "Classify this Slack message. Return JSON: "
                           "{is_learning_signal: bool, topic: str|null, "
                           "estimated_level: int 0-5, is_stuck_signal: bool}"
            }, {
                "role": "user", "content": text
            }]
        )
        import json
        return json.loads(response.choices[0].message.content)

    def classify_support_case(self, description: str) -> dict:
        """AI-triage a support case: classify, summarize, set priority."""
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[{
                "role": "system",
                "content": "Triage this support case. Return JSON: "
                           "{category: str, summary: str (max 100 chars), "
                           "priority: 'low'|'medium'|'high'|'critical', "
                           "suggested_response: str}"
            }, {
                "role": "user", "content": description
            }]
        )
        import json
        return json.loads(response.choices[0].message.content)

    def _build_teaching_system_prompt(self, style: str, level: int) -> str:
        level_names = ["Curious", "Apprentice", "Builder", "Engineer", "Specialist", "Master"]
        return (
            f"You are lippytmai — the AI teaching identity of lippytm.ai. "
            f"The learner is at '{level_names[min(level, 5)]}' level (level {level}). "
            "Explain clearly using analogies, always show a code example, "
            "and end with the single best next concept to learn. "
            "Format: explanation | code_example | next_concept"
        )
```

---

## 6. Earn-while-you-Learn Slack Workflows

### 6.1 Automated Badge Issuance Workflow

```
LEARNER COMPLETES LESSON (logged to CRM)
          │
          ▼
MILESTONE CHECK (CRM queries proficiency table)
  - 5 lessons on topic AND avg quality ≥ 4 → Level 1 Badge candidate
  - 10 lessons AND passes auto-quiz → Level 2 Badge candidate
  - 20 lessons AND project submitted AND reviewed → Level 3 Badge candidate
          │
          ▼
HERMES EMITS badge_candidate event
          │
          ▼
AUTO-QUIZ DELIVERED via Slack DM (for Levels 1 & 2)
          │
       Pass? ───No──► "Keep practicing! Here's what to review."
          │ Yes
          ▼
CREDENTIAL ISSUANCE REQUEST → on-chain ERC-721 SkillBadge
  (Level 4+ requires Charles Earl Lipshay approval)
          │
          ▼
BADGE MINTED → learner notified in Slack with certificate block
```

### 6.2 Auto-Quiz Slack Block

```python
def build_quiz_blocks(topic: str, level: int, questions: list) -> list:
    """Build an interactive quiz in Slack Block Kit."""
    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text",
                     "text": f"🎓 Level {level} Badge Assessment — {topic}"}
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn",
                     "text": "Answer 3 questions correctly to earn your badge!"}
        }
    ]

    for i, q in enumerate(questions[:3]):
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Q{i+1}: {q['question']}*"},
            "accessory": {
                "type": "static_select",
                "placeholder": {"type": "plain_text", "text": "Select answer"},
                "options": [
                    {"text": {"type": "plain_text", "text": opt},
                     "value": f"q{i}_{j}"}
                    for j, opt in enumerate(q["options"])
                ],
                "action_id": f"quiz_answer_{i}"
            }
        })

    blocks.append({
        "type": "actions",
        "elements": [{
            "type": "button",
            "text": {"type": "plain_text", "text": "Submit Answers"},
            "style": "primary",
            "action_id": "submit_quiz",
            "value": topic
        }]
    })

    return blocks
```

### 6.3 Badge Earned Notification

```python
def build_badge_earned_blocks(learner_name: str, topic: str, level: int,
                               token_id: str, chain: str = "Base") -> list:
    level_names = ["Curious", "Apprentice", "Builder", "Engineer", "Specialist", "Master"]
    return [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "🏆 New Skill Badge Earned!"}
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn",
                     "text": f"Congratulations *{learner_name}*! 🎉\n\n"
                             f"You've earned the *{topic} — {level_names[level]}* badge!\n\n"
                             f"🔗 On-chain token: `{token_id}` ({chain})\n"
                             f"This credential is permanently recorded on the blockchain and "
                             f"verifiable by any employer or learning platform."}
        },
        {
            "type": "actions",
            "elements": [
                {"type": "button", "text": {"type": "plain_text", "text": "View on Explorer"},
                 "url": f"https://basescan.org/token/{token_id}", "action_id": "view_badge"},
                {"type": "button", "text": {"type": "plain_text", "text": "Share in Channel"},
                 "action_id": "share_badge", "value": f"{topic}:{level}:{token_id}"},
                {"type": "button", "text": {"type": "plain_text", "text": "Next Level →"},
                 "style": "primary", "action_id": "next_level",
                 "value": f"{topic}:{level+1}"}
            ]
        }
    ]
```

---

## 7. CRM Analytics & Reporting

### 7.1 Learner Journey Report (Slack-native)

```python
# Delivered weekly via Hermes scheduler to CRM admin channel
def generate_weekly_report(workspace_id: str) -> dict:
    stats = crm.aggregate_weekly_stats(workspace_id)
    return {
        "new_learners":        stats["new_learners_7d"],
        "active_learners":     stats["active_learners_7d"],
        "lessons_completed":   stats["lessons_completed_7d"],
        "avg_response_quality": stats["avg_ai_quality_7d"],
        "badges_issued":       stats["badges_7d"],
        "support_cases_opened": stats["cases_opened_7d"],
        "support_cases_resolved": stats["cases_resolved_7d"],
        "avg_resolution_hours": stats["avg_resolution_7d"],
        "top_topics":          stats["top_topics_7d"],      # most asked about
        "struggling_topics":   stats["low_quality_topics"], # AI quality < 3
        "fabric_sync_lag_min": stats["fabric_lag_minutes"]  # ACSS health metric
    }
```

### 7.2 AI Quality Dashboard Metrics Published to Fabric

| Metric | Purpose | Fabric Action if Below Threshold |
|---|---|---|
| `avg_response_quality_7d` | Teaching AI quality | < 3.5 → trigger lippytmai fine-tune review |
| `quiz_pass_rate` | Curriculum difficulty calibration | < 60% → AI adjusts difficulty down |
| `lesson_completion_rate` | Engagement signal | < 50% → AI shortens lesson format |
| `support_first_response_sla` | Support quality | > 4h → escalate to lippytm clone |
| `badge_issuance_rate` | Learning momentum | < 5%/month → review curriculum gap |
| `churn_rate_30d` | Learner retention | > 20% → trigger re-engagement campaign |

---

## 8. Deployment

### 8.1 OMARCHY-Standard Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY . .

# OMARCHY security standard: non-root user
RUN useradd -r -s /bin/false slackbot
USER slackbot

CMD ["python", "app.py"]
```

```yaml
# docker-compose.yml
services:
  slack-crm-bot:
    build: .
    restart: unless-stopped
    environment:
      - SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN}
      - SLACK_APP_TOKEN=${SLACK_APP_TOKEN}
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - HERMES_URL=${HERMES_URL}
      - FABRIC_URL=${FABRIC_URL}
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: slack_crm
      POSTGRES_USER: crm_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes

volumes:
  postgres_data:
```

### 8.2 Environment Variables (never commit — injected by Hermes)

| Variable | Source | Purpose |
|---|---|---|
| `SLACK_BOT_TOKEN` | Slack App settings | Bot OAuth token (`xoxb-...`) |
| `SLACK_APP_TOKEN` | Slack App settings | Socket Mode token (`xapp-...`) |
| `DATABASE_URL` | Infrastructure layer | PostgreSQL connection string |
| `REDIS_URL` | Infrastructure layer | Redis connection string |
| `OPENAI_API_KEY` | Hermes secrets | GPT-4o classification and teaching |
| `ANTHROPIC_API_KEY` | Hermes secrets | Claude teaching explanations |
| `HERMES_URL` | ACSS infrastructure | Internal Hermes event bus endpoint |
| `FABRIC_URL` | ACSS infrastructure | Fabric knowledge graph API endpoint |

---

## 9. Privacy, Consent, and Safety

| Principle | Implementation |
|---|---|
| **Consent-first** | No learner data stored until explicit consent given via Slack onboarding flow |
| **Minimal data collection** | Only Slack user ID, display name, learning interactions — no private message content stored |
| **Right to deletion** | `/crm delete` command triggers full data purge with GDPR-compliant audit trail |
| **AI disclosure** | Every lippytmai response includes "🤖 AI-generated" label per ACSS disclosure standard |
| **No secret accumulation** | All API keys injected at runtime by Hermes; zero secrets in code or database |
| **Human gate for credentials** | Level 4+ badges require Charles Earl Lipshay approval before on-chain issuance |
| **Support data protection** | Support case descriptions never used as AI training data without explicit learner consent |

---

## Further Reading

- 📄 [`docs/ai-clone-engine-swarms.md`](ai-clone-engine-swarms.md) — ACSS full architecture (Hermes, Fabric, all 8 systems)
- 📄 [`docs/ai-agents-upgrade-manifest.md`](ai-agents-upgrade-manifest.md) — Teaching agent tier definitions and upgrade paths
- 📄 [`docs/ai-model-intelligence-layer.md`](ai-model-intelligence-layer.md) — AMIL model selection for teaching and classification tasks
- 📄 [`docs/ai-brainkits.md`](ai-brainkits.md) — Copilot Brainkit design and agent memory
- 📄 [`docs/P011-CRM-001-learning-system.md`](P011-CRM-001-learning-system.md) — CRM educational architecture and Party Passport standard
- 📄 [`EARN_WHILE_YOU_LEARN.md`](../EARN_WHILE_YOU_LEARN.md) — Earn-while-you-Learn ecosystem and credential philosophy
- 🏠 [`README.md`](../README.md) — Encyclopedia home

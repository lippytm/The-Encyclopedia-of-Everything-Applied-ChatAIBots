# AI Copilot Video Explainer — Tutorial — Video Sandbox Creator

### Hermes + Fabric Integrated — The Creative Building Process for AI-Powered Educational Video

> *"A video is not a static artifact. It is a living lesson — aware of who is watching, what they already know, where they are struggling, and what credential they will earn when they succeed. When Hermes routes the learner's context to the right agent, and Fabric weaves the right knowledge into the right scene, every video becomes a personal teacher."*
> — lippytmai

---

## Overview

The **AI Copilot Video Explainer / Tutorial / Video Sandbox Creator (ACVS)** is the ACSS creative production system that merges three capabilities into one pipeline:

| Mode | Description | Output |
|---|---|---|
| **Explainer** | Concept-first narrative — what is it and why does it matter? | Animated video with narration + visual metaphors |
| **Tutorial** | Step-by-step walkthrough — exactly how to build it | Screen-capture + code walkthrough + terminal demo |
| **Sandbox** | Interactive build environment — learner does it themselves | GESN interactive overlay + credential gate |

**Hermes** is the message bus that routes tasks between agents and surfaces completion events to GitHub/Slack/GESN.  
**Fabric** is the knowledge graph that ensures every video builds on verified context and cross-links to the wider encyclopedia.

Together they transform ACVS from a video generator into a **continuously self-improving creative intelligence**.

*[Reality — architecture documented here is implementable with current AI tooling]*  
*[Speculative — real-time personalized scene rendering is a 2027+ target]*

---

## 1. The Creative Building Process — Hermes + Fabric Integration

### 1.1 How the Build Flows

```
Creator Request (Charles / lippytmai)
    │
    ▼
┌─────────────────────────────────────────────────┐
│  HERMES EVENT BUS                               │
│  routes: CREATE_VIDEO_REQUEST                   │
│  payload: { book_id, mode, topic, audience }    │
└──────────┬──────────────────────────────────────┘
           │
    ┌──────┴───────────────────────────────┐
    │                                      │
    ▼                                      ▼
┌──────────────────────┐       ┌───────────────────────┐
│   FABRIC             │       │   ACVS SCRIPT AGENT   │
│   Knowledge Pull     │       │   (lippytmai)         │
│                      │       │                       │
│ • Existing ebook     │──────▶│ • Scene Manifest JSON │
│   chapters           │       │ • Narration script    │
│ • Prior video        │       │ • Code walkthroughs   │
│   scripts            │       │ • Quiz questions      │
│ • Learner progress   │       │ • Build gates         │
│ • Credential state   │       │                       │
│ • Cross-references   │       └──────────┬────────────┘
└──────────────────────┘                  │
                                          ▼
                            ┌─────────────────────────┐
                            │  SCENE PRODUCTION       │
                            │  • Narration (TTS)      │
                            │  • Visuals (AI video)   │
                            │  • Code animations      │
                            │  • Terminal recordings  │
                            │  • Interactive overlays │
                            └──────────┬──────────────┘
                                       │
                                       ▼
                            ┌─────────────────────────┐
                            │  QUALITY GATE (E5)      │
                            │  G1–G12 automated       │
                            │  G13 Charles (manual)   │
                            └──────────┬──────────────┘
                                       │
                            ┌──────────┴──────────────┐
                            │  HERMES PUBLISH EVENT   │
                            │  VIDEO_PUBLISHED        │
                            │  → GitHub PR comment    │
                            │  → Slack #acss-videos   │
                            │  → GESN catalog         │
                            │  → Fabric KB update     │
                            └─────────────────────────┘
```

### 1.2 Hermes Event Types in the Video Pipeline

```python
# hermes_video_events.py — Event schemas for ACVS pipeline

from dataclasses import dataclass
from typing import Optional, Literal
from datetime import datetime

VideoMode = Literal["explainer", "tutorial", "sandbox"]
VideoStatus = Literal["requested", "scripting", "producing", "quality_review",
                      "awaiting_g13", "published", "failed"]

@dataclass
class CreateVideoRequest:
    """Hermes event: request a new video to be created."""
    event_type: str = "CREATE_VIDEO_REQUEST"
    book_id: str = ""          # e.g. "B-011"
    mode: VideoMode = "tutorial"
    topic: str = ""
    audience: str = "Beginner"
    requested_by: str = "lippytmai"
    timestamp: str = ""

    def __post_init__(self):
        self.timestamp = datetime.utcnow().isoformat()

@dataclass
class VideoScriptReady:
    """Hermes event: scene manifest has been generated and is ready for production."""
    event_type: str = "VIDEO_SCRIPT_READY"
    book_id: str = ""
    manifest_path: str = ""
    scene_count: int = 0
    estimated_duration_sec: int = 0
    timestamp: str = ""

    def __post_init__(self):
        self.timestamp = datetime.utcnow().isoformat()

@dataclass
class VideoPublished:
    """Hermes event: video has passed G13 and is live in GESN."""
    event_type: str = "VIDEO_PUBLISHED"
    book_id: str = ""
    video_url: str = ""
    credential: str = ""
    mode: VideoMode = "tutorial"
    duration_sec: int = 0
    timestamp: str = ""

    def __post_init__(self):
        self.timestamp = datetime.utcnow().isoformat()


class HermesVideoRouter:
    """Routes ACVS pipeline events to GitHub, Slack, and GESN."""

    def __init__(self, github_token: str, slack_webhook: str, gesn_api_key: str):
        self._github_token = github_token
        self._slack_webhook = slack_webhook
        self._gesn_api_key = gesn_api_key

    def dispatch(self, event: object) -> None:
        """Route an event to all registered handlers."""
        event_type = getattr(event, "event_type", "UNKNOWN")

        if event_type == "CREATE_VIDEO_REQUEST":
            self._notify_slack(f"🎬 Video requested: {event.book_id} [{event.mode}]")  # type: ignore[union-attr]
            self._update_fabric(event)

        elif event_type == "VIDEO_SCRIPT_READY":
            self._notify_slack(
                f"📝 Script ready: {event.book_id} — {event.scene_count} scenes, "  # type: ignore[union-attr]
                f"~{event.estimated_duration_sec // 60}min"  # type: ignore[union-attr]
            )

        elif event_type == "VIDEO_PUBLISHED":
            self._notify_github(event)
            self._notify_slack(f"✅ Published: {event.book_id} | Credential: {event.credential}")  # type: ignore[union-attr]
            self._publish_to_gesn(event)
            self._update_fabric(event)

    def _notify_slack(self, message: str) -> None:
        import urllib.request, json
        payload = json.dumps({"text": message}).encode()
        req = urllib.request.Request(
            self._slack_webhook, data=payload,
            headers={"Content-Type": "application/json"}
        )
        urllib.request.urlopen(req)

    def _notify_github(self, event: object) -> None:
        # Posts a comment to the active PR
        pass  # implemented via PyGitHub in production

    def _publish_to_gesn(self, event: object) -> None:
        # Registers video in GESN catalog and unlocks credential gate
        pass  # implemented via GESN REST API

    def _update_fabric(self, event: object) -> None:
        # Writes event to Fabric knowledge graph
        FabricVideoNode.upsert(event)
```

### 1.3 Fabric Knowledge Integration

Fabric maintains a video knowledge graph — every video that ACVS produces is a node, linked to:

```python
# fabric_video_node.py — Fabric knowledge graph node for ACVS

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class FabricVideoNode:
    """
    A node in Fabric's knowledge graph representing one produced video.
    Fabric uses these nodes to:
    - Prevent duplicate content across videos
    - Suggest cross-references during script generation
    - Track which concepts have been taught and at what depth
    - Feed learner progress back into future script personalization
    """
    book_id: str
    title: str
    mode: str                         # explainer | tutorial | sandbox
    topics_covered: List[str] = field(default_factory=list)
    credentials_unlocked: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    fabric_cross_links: List[str] = field(default_factory=list)
    avg_completion_rate: float = 0.0  # from GESN analytics
    common_drop_points: List[int] = field(default_factory=list)  # scene indices
    learner_quiz_scores: List[float] = field(default_factory=list)

    @classmethod
    def upsert(cls, event: object) -> "FabricVideoNode":
        """Write or update a node in the Fabric graph from a Hermes event."""
        # In production: calls Fabric's graph DB API
        return cls(
            book_id=getattr(event, "book_id", ""),
            title=getattr(event, "topic", ""),
            mode=getattr(event, "mode", "tutorial"),
        )

    def suggest_cross_links(self) -> List[str]:
        """Ask Fabric for related nodes to reference in the next video."""
        # Returns book_ids of related content based on topic overlap
        return []

    def get_weak_spots(self) -> List[str]:
        """
        Fabric-powered insight: which topics have low quiz scores across
        all learners who watched this video? Feed back into next script revision.
        """
        return [
            self.topics_covered[i]
            for i, score in enumerate(self.learner_quiz_scores[:len(self.topics_covered)])
            if score < 0.65
        ]
```

---

## 2. The Three Video Modes — Deep Design

### 2.1 Explainer Mode

**Purpose:** Build conceptual understanding before any code is shown.

**Structure:**
1. **Hook** — a real-world story or consequence (30–60s)
2. **Concept Map** — animated diagram showing how components relate (60–90s)
3. **Analogy Bridge** — map the abstract concept to something physical (45–60s)
4. **Reality vs Speculative** — clearly label what exists today vs what's coming (30–45s)
5. **Summary + Next Step** — what to build next in Tutorial mode (30s)

**Hermes trigger:** `CREATE_VIDEO_REQUEST { mode: "explainer" }`  
**Fabric input:** concept definition, analogies from related docs, prior explainer videos on adjacent topics

```json
{
  "scene_type": "explainer",
  "id": "EXP-001-S01",
  "hook": "In 2009, every bank in the world trusted exactly one thing: a central ledger no one could see...",
  "visual_prompt": "Dramatic animation: single bank server with a lock. Arrow points to 'WHO CONTROLS THIS?'",
  "fabric_cross_refs": ["ai-clone-engine-swarms.md §2", "B-008-files-that-never-get-lost.md"],
  "duration_sec": 45
}
```

---

### 2.2 Tutorial Mode

**Purpose:** Walk through a real build step by step — learner follows along.

**Structure:**
1. **What you'll build** — show the finished artifact upfront (30s)
2. **Environment check** — verify prerequisites (30s)
3. **Step scenes** — one concept per scene, with terminal/code (3–6 scenes × 120–180s each)
4. **Common mistake** — show a deliberate error and fix it (60–90s)
5. **Build Gate** — learner runs the command and sees the output (interactive, 60s)
6. **Credential Mint** — on-chain confirmation (30s)

**Hermes trigger:** `CREATE_VIDEO_REQUEST { mode: "tutorial" }`  
**Fabric input:** ebook build artifact, prior tutorial completion rates, quiz failure patterns

```json
{
  "scene_type": "tutorial_step",
  "id": "TUT-B011-S03",
  "title": "Creating the .env File",
  "narration": "Create a .env file at the project root. Notice: this is NOT added to .gitignore yet — we'll fix that in the next scene deliberately to show what happens when you forget.",
  "terminal_recording": {
    "commands": ["cat > .env << 'EOF'\nDATABASE_URL=postgresql://localhost/dev\nEOF", "git status"],
    "expected_output": ".env — shown in git status (WARNING: not yet gitignored)"
  },
  "common_mistake": true,
  "duration_sec": 150
}
```

---

### 2.3 Sandbox Mode

**Purpose:** Learner builds it themselves in a guided interactive environment.

**Structure:**
1. **Mission Brief** — what to build, what credential it unlocks (30s)
2. **Tool Introduction** — what's available in the sandbox (30s)
3. **Guided Challenges** — 3–5 progressive tasks with hints available (variable)
4. **Build Gate** — final verification that the artifact works (interactive)
5. **Credential Mint** — triggers on successful Build Gate (30s)

**Hermes trigger:** `CREATE_VIDEO_REQUEST { mode: "sandbox" }`  
**Fabric input:** learner's credential history, completed prerequisites, personalized difficulty level

```python
# sandbox_session.py — GESN Sandbox session model

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class SandboxChallenge:
    id: str
    prompt: str
    expected_command: str
    hint_available: bool = True
    hint_text: str = ""
    points: int = 10

@dataclass
class SandboxSession:
    """
    A learner's active sandbox session. Hermes tracks state transitions.
    Fabric provides personalized challenge difficulty based on history.
    """
    learner_id: str
    book_id: str
    credential_target: str
    challenges: List[SandboxChallenge] = field(default_factory=list)
    completed_challenges: List[str] = field(default_factory=list)
    hints_used: int = 0
    score: int = 0
    build_gate_passed: bool = False
    credential_minted: bool = False

    def complete_challenge(self, challenge_id: str, command_used: str) -> bool:
        challenge = next((c for c in self.challenges if c.id == challenge_id), None)
        if challenge and command_used.strip() == challenge.expected_command.strip():
            self.completed_challenges.append(challenge_id)
            self.score += challenge.points
            return True
        return False

    def check_build_gate(self, artifact_hash: str, expected_hash: str) -> bool:
        if artifact_hash == expected_hash:
            self.build_gate_passed = True
        return self.build_gate_passed

    def mint_credential(self) -> Optional[str]:
        """Trigger on-chain credential mint when build gate passes."""
        if self.build_gate_passed and not self.credential_minted:
            self.credential_minted = True
            return self.credential_target
        return None
```

---

## 3. AI Copilot Script Agent

The **AI Copilot Script Agent** is the lippytmai clone operating in Teach mode — it is the creative engine that writes the scene manifests:

```python
# acvs_script_agent.py — AI Copilot Video Script Generation Agent

import os
from typing import Optional
from openai import OpenAI
from dataclasses import dataclass

@dataclass
class SceneManifest:
    book_id: str
    mode: str
    scenes: list
    total_duration_sec: int
    fabric_cross_refs: list

class ACVSScriptAgent:
    """
    The AI Copilot Script Agent — lippytmai clone in Teach mode.
    Pulls context from Fabric, writes scene manifests, routes
    completion events through Hermes.
    """

    SYSTEM_PROMPT = """You are lippytmai — the AI brand identity of lippytm.ai — operating in Teach mode.
Your job is to write video scene manifests for educational content.
Voice: intellectually ambitious, direct, analogy-rich, never condescending.
Every scene must teach something. No filler.
Always distinguish [Reality] from [Speculative].
Output valid JSON scene manifest only."""

    def __init__(self, fabric_client, hermes_router):
        self._fabric = fabric_client
        self._hermes = hermes_router
        self._llm = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def generate_script(
        self,
        book_id: str,
        mode: str,
        topic: str,
        ebook_content: str,
        audience: str = "Beginner"
    ) -> SceneManifest:
        """
        Generate a complete scene manifest for a video.

        1. Pull Fabric context (related nodes, prior scripts, learner weak spots)
        2. Build prompt with ebook content + Fabric context
        3. Call LLM to generate scene manifest JSON
        4. Dispatch VideoScriptReady event via Hermes
        """
        # Step 1: Fabric context pull
        related_nodes = self._fabric.get_related_nodes(book_id)
        weak_spots = self._fabric.get_cross_book_weak_spots(topic)

        # Step 2: Build prompt
        prompt = self._build_prompt(
            book_id, mode, topic, audience,
            ebook_content, related_nodes, weak_spots
        )

        # Step 3: Generate
        response = self._llm.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.4
        )

        import json
        manifest_data = json.loads(response.choices[0].message.content)
        manifest = SceneManifest(
            book_id=book_id,
            mode=mode,
            scenes=manifest_data.get("scenes", []),
            total_duration_sec=sum(s.get("duration_sec", 0) for s in manifest_data.get("scenes", [])),
            fabric_cross_refs=[n.book_id for n in related_nodes]
        )

        # Step 4: Hermes event
        from hermes_video_events import VideoScriptReady
        self._hermes.dispatch(VideoScriptReady(
            book_id=book_id,
            manifest_path=f"docs/{book_id}-VIDEO-scene-manifest.md",
            scene_count=len(manifest.scenes),
            estimated_duration_sec=manifest.total_duration_sec
        ))

        return manifest

    def _build_prompt(
        self, book_id: str, mode: str, topic: str, audience: str,
        ebook_content: str, related_nodes: list, weak_spots: list
    ) -> str:
        return f"""Create a {mode} video scene manifest for:
Book ID: {book_id}
Topic: {topic}
Audience: {audience}

EBOOK CONTENT SUMMARY:
{ebook_content[:3000]}

FABRIC CONTEXT:
Related books: {[n for n in related_nodes]}
Topics learners struggle with: {weak_spots}

Requirements:
- {{'explainer': '5 scenes max, 15–18 min total', 'tutorial': '6 scenes max, 18–22 min total', 'sandbox': '5 challenges + 1 build gate scene'}[mode]}
- Each scene must have: id, title, narration, visual_prompt, duration_sec
- Tutorial/sandbox scenes must include: code_block OR terminal_recording
- At least one interactive_overlay (quiz, challenge, or build_gate)
- Final scene is always mission_complete with credential
- Voice: lippytmai (direct, educational, no filler)

Output JSON only."""
```

---

## 4. ACVS Video Taxonomy

Every video produced by ACVS is classified into this taxonomy — stored in Fabric, surfaced in GESN:

| Category | Code | Example |
|---|---|---|
| **Linux Foundations** | `VID-CLL-L0` | B-001 Terminal Explainer |
| **Linux Operations** | `VID-CLL-L1` | B-006 Processes Tutorial |
| **OMARCHY Standard** | `VID-OMARCHY` | B-017 Arch Linux Tutorial |
| **Secure Dev** | `VID-CCSLL-L0` | B-011 Env Vars Tutorial |
| **Container Ops** | `VID-CSEL-L0` | B-012 Docker Tutorial |
| **Blockchain Basics** | `VID-CBSLL-L0` | B-056 Solidity Explainer |
| **AI/ML Concepts** | `VID-ACSS-L0` | ACSS Explainer Series |
| **GESN Platform** | `VID-GESN` | GESN Advertising/Onboarding |
| **Sandbox Missions** | `VID-SANDBOX` | Interactive build challenges |
| **Copilot Tutorials** | `VID-COPILOT` | GitHub Copilot + ACSS workflows |

---

## 5. Hermes + Fabric in the Creative Build Loop

### 5.1 The Continuous Improvement Cycle

```
Video Published
     │
     ▼
GESN Analytics → Fabric
     │
     │  "Scene 4 has 42% drop-off rate"
     │  "Quiz question 2 fails 67% of learners"
     │  "Average time on build gate: 8 min (expected: 3 min)"
     ▼
Fabric Weak Spot Analysis
     │
     ▼
Hermes: IMPROVEMENT_REQUIRED event
     │
     ▼
ACVSScriptAgent revision
     │
     ▼
Revised scene manifest
     │
     ▼
G13 review (targeted — only revised scenes)
     │
     ▼
Video updated → Fabric node updated
```

### 5.2 Hermes Creative Event Bus — Full Event List

| Event | Trigger | Recipients |
|---|---|---|
| `CREATE_VIDEO_REQUEST` | Charles or lippytmai requests video | ACVSScriptAgent, Fabric |
| `VIDEO_SCRIPT_READY` | Scene manifest generated | Slack, GitHub PR |
| `SCENE_PRODUCTION_COMPLETE` | Raw assets assembled | Video Composer |
| `QUALITY_GATE_PASS` | G1–G12 pass | Slack, Charles (G13 gate) |
| `G13_APPROVED` | Charles approves | GESN publisher |
| `VIDEO_PUBLISHED` | Live in GESN | GitHub, Slack, Fabric, GESN |
| `LEARNER_MILESTONE` | Credential minted | Fabric, GESN leaderboard |
| `IMPROVEMENT_REQUIRED` | Low analytics thresholds | ACVSScriptAgent, lippytmai |
| `SCRIPT_REVISION_COMPLETE` | Targeted scene rewrite done | Quality Gate engine |

### 5.3 Fabric Knowledge Flows

```
INPUT STREAMS                           FABRIC GRAPH
─────────────                           ────────────
Ebook chapters ──────────────────────▶ Concept nodes
Video scene manifests ───────────────▶ Video nodes
Learner quiz results ────────────────▶ Weak spot annotations
Credential mint events ──────────────▶ Progress nodes
GESN drop-off data ──────────────────▶ Engagement annotations
Cross-references ────────────────────▶ Link edges
GitHub commit messages ──────────────▶ Build history nodes

OUTPUT QUERIES
──────────────
ACVSScriptAgent asks Fabric:
  • "What has already been taught about Docker?"
  • "Where do learners fail in the networking cluster?"
  • "Which books link to environment variables?"
  • "What credential does learner X already hold?"

Fabric returns:
  • Related FabricVideoNode objects
  • WeakSpotAnnotation objects
  • ProgressNode for the learner
  • Suggested cross-references for the script
```

---

## 6. Sandbox Creator — Technical Spec

The **Video Sandbox Creator** is the interactive runtime layer where learners actually do the work:

```yaml
# docker-compose.sandbox.yml — ACVS Sandbox Runtime
version: "3.9"

services:
  sandbox-runtime:
    image: lippytmai/acvs-sandbox:latest
    container_name: acvs-sandbox
    environment:
      - LEARNER_ID=${LEARNER_ID}
      - BOOK_ID=${BOOK_ID}
      - CREDENTIAL_TARGET=${CREDENTIAL_TARGET}
      - GESN_API_KEY=${GESN_API_KEY}
      - HERMES_WEBHOOK=${HERMES_WEBHOOK}
    ports:
      - "8080:8080"    # Sandbox web terminal
      - "8081:8081"    # Challenge API
    volumes:
      - sandbox-workspace:/workspace
    restart: unless-stopped

  challenge-api:
    image: lippytmai/acvs-challenge-api:latest
    container_name: acvs-challenges
    env_file: .env
    environment:
      - DATABASE_URL=postgresql://postgres:${POSTGRES_PASSWORD}@db:5432/sandbox
    ports:
      - "8082:8082"
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=sandbox
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - sandbox-db:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  sandbox-workspace:
  sandbox-db:
```

---

## 7. Integration with Existing ACSS Systems

| ACSS System | ACVS Integration |
|---|---|
| **Clone Engine** | lippytmai runs ACVSScriptAgent; Lippy Killjoy runs experimental sandbox missions |
| **Hermes** | All pipeline state transitions dispatched as typed events; G13 gate notification |
| **Fabric** | Script context input; analytics write-back; weak spot detection; cross-link suggestion |
| **CCSLL** | Code examples in tutorials use CCSLL-verified syntax and patterns |
| **CBSLL** | Blockchain tutorial videos pull contract templates from CBSLL |
| **CLL** | Linux tutorial videos verified against CLL command reference |
| **OMARCHY** | Sandbox uses OMARCHY-standard tooling (Neovim, Zsh, Alacritty terminal theme) |
| **CSEL** | Sandbox environments spin up from CSEL environment definitions |

---

## 8. ACVS + HDVG — How They Relate

ACVS and HDVG are complementary, not competing:

| System | Scope | Output |
|---|---|---|
| **HDVG** (P011-VIDEO-001) | Production pipeline — renders and exports videos | MP4/WebM/HLS files |
| **ACVS** (this doc) | Creative pipeline — scripts, modes, sandbox sessions, Hermes/Fabric integration | Scene manifests, sandbox sessions, learning analytics |

ACVS generates the **creative content** (scene manifests, narration scripts, interactive challenges).  
HDVG takes those manifests and **renders them** into deliverable video files.

```
ACVS ScriptAgent ──▶ Scene Manifest JSON ──▶ HDVG Renderer ──▶ MP4/WebM/HLS
     │                                              │
     ▼                                              ▼
Fabric (knowledge)                        GESN (delivery)
Hermes (events)                           Credential mint
```

---

## Further Reading

- 📄 [`docs/ai-clone-engine-swarms.md`](ai-clone-engine-swarms.md) — Full ACSS architecture including Hermes and Fabric
- 📄 [`docs/P011-VIDEO-001-hd-video-generator.md`](P011-VIDEO-001-hd-video-generator.md) — HDVG production pipeline
- 📄 [`docs/P011-GESN-001-gamer-educational-systems-networks.md`](P011-GESN-001-gamer-educational-systems-networks.md) — GESN interactive delivery platform
- 📄 [`docs/ai-agents-upgrade-manifest.md`](ai-agents-upgrade-manifest.md) — Agent tier registry
- 📄 [`docs/autonomous-continuous-development.md`](autonomous-continuous-development.md) — ACD: continuous deployment after G13
- 🏠 [`README.md`](../README.md) — Encyclopedia home

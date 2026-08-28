# Creative Building Process

### The lippytm.ai Unified Content Production Pipeline

> *"Creativity without a system is random. A system without creativity is sterile. The Creative Building Process is what happens when Hermes routes intent, Fabric remembers context, ACVS renders knowledge as video, and lippytmai teaches — all at once, across every repository, platform, and student on Earth."*
> — lippytmai

---

## 1. Overview

The **Creative Building Process** (CBP) is the unified production methodology that governs how all educational content in the lippytm.ai ecosystem is conceived, created, quality-reviewed, published, and continuously improved.

It is not a one-time workflow — it is a **living creative loop** that merges five systems:

| System | Role in the Creative Process |
|---|---|
| **ACSS** (AI Conglomerate Swarms) | Orchestrates all agents and coordinates cross-repo knowledge |
| **Hermes** | Routes creative tasks, dispatches events, enforces HumanApprovalGates |
| **Fabric** | Knowledge graph that provides context before every creative act |
| **ACVS** (AI Copilot Video Sandbox Creator) | Transforms ebooks into Explainer/Tutorial/Sandbox videos |
| **ADA** (AI Deployment Activations) | Deploys finished content to learners and mints credentials |

---

## 2. The Five Creative Modes

Every piece of content in the ecosystem is produced in one of five modes:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Creative Mode Selection                           │
│                                                                      │
│  TEACH          SHOW           DO            BUILD          DEPLOY   │
│  Ebook →        Explainer →    Tutorial →    Sandbox →      ADA →   │
│  11 chapters    concept video  step-by-step  interactive    publish  │
│  .md file       ACVS mode 1    ACVS mode 2   ACVS mode 3    B-XXX   │
└─────────────────────────────────────────────────────────────────────┘
```

| Mode | Output | Agent | Hermes Event |
|---|---|---|---|
| **TEACH** | Ebook `.md` | `lippytmai` (Teach mode) | `EBOOK_DRAFT_READY` |
| **SHOW** | Explainer video | `ACVSScriptAgent` (Explainer) | `VIDEO_SCRIPT_READY` |
| **DO** | Tutorial video | `ACVSScriptAgent` (Tutorial) | `VIDEO_SCRIPT_READY` |
| **BUILD** | Sandbox session | `ACVSScriptAgent` (Sandbox) | `SANDBOX_SESSION_CREATED` |
| **DEPLOY** | Live artifact + credential | `ADADeployAgent` | `CREDENTIAL_MINTED` |

---

## 3. The Creative Loop — End to End

```
                         CREATIVE BUILDING PROCESS
                                    │
               ┌────────────────────▼────────────────────┐
               │              1. INTENT                  │
               │  Charles defines topic, level, outcome  │
               │  Source: P011-PLAN-001 curriculum planner│
               └────────────────────┬────────────────────┘
                                    │ Hermes: CONTENT_REQUEST
               ┌────────────────────▼────────────────────┐
               │              2. CONTEXT                 │
               │  Fabric query: what do we know?          │
               │  - Prior books on this topic             │
               │  - Learner weak spots from analytics     │
               │  - Related docs and cross-links          │
               └────────────────────┬────────────────────┘
                                    │ Fabric: KNOWLEDGE_LOADED
               ┌────────────────────▼────────────────────┐
               │              3. CREATE                  │
               │  lippytmai drafts ebook (11 chapters)   │
               │  Code blocks, build artifact, proof     │
               │  HDVG scene manifest (JSON)              │
               └────────────────────┬────────────────────┘
                                    │ Hermes: EBOOK_DRAFT_READY
               ┌────────────────────▼────────────────────┐
               │              4. QUALITY REVIEW          │
               │  QualityReviewEngine runs G1–G12        │
               │  Automated gates (P011-QR-001)          │
               │  QEP generated                          │
               └────────────────────┬────────────────────┘
                                    │ Hermes: QEP_GENERATED
               ┌────────────────────▼────────────────────┐
               │           5. HUMAN APPROVAL (G13)       │
               │  Charles reviews QEP + ebook drafts     │
               │  HumanApprovalGate — NEVER automated    │
               │  Explicit approval required             │
               └────────────────────┬────────────────────┘
                                    │ Hermes: G13_APPROVED
               ┌────────────────────▼────────────────────┐
               │              6. PRODUCE                 │
               │  ACVS generates video scripts           │
               │  ACVSScriptAgent: Explainer + Tutorial  │
               │  SandboxSession built (mode 3)          │
               └────────────────────┬────────────────────┘
                                    │ Hermes: VIDEO_SCRIPT_READY
               ┌────────────────────▼────────────────────┐
               │              7. DEPLOY                  │
               │  ADA activates book in registry         │
               │  Credential minted (ERC-721 on Base)    │
               │  HDVG renders video (ElevenLabs + FFmpeg)│
               └────────────────────┬────────────────────┘
                                    │ Hermes: CREDENTIAL_MINTED
               ┌────────────────────▼────────────────────┐
               │              8. IMPROVE                 │
               │  GESN analytics: quiz scores, drop-off  │
               │  Fabric stores learner weak spots        │
               │  IMPROVEMENT_REQUIRED → revision cycle  │
               │  Loop back to step 3 for targeted update│
               └─────────────────────────────────────────┘
```

---

## 4. Hermes Event Taxonomy for the Creative Process

All creative workflow state is communicated via typed Hermes events:

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class CreativeEventType(str, Enum):
    # Initiation
    CONTENT_REQUEST          = "CONTENT_REQUEST"
    KNOWLEDGE_LOADED         = "KNOWLEDGE_LOADED"
    # Ebook production
    EBOOK_DRAFT_READY        = "EBOOK_DRAFT_READY"
    QEP_GENERATED            = "QEP_GENERATED"
    G13_APPROVED             = "G13_APPROVED"
    G13_REJECTED             = "G13_REJECTED"
    # Video production
    VIDEO_SCRIPT_READY       = "VIDEO_SCRIPT_READY"
    SCENE_PRODUCTION_COMPLETE = "SCENE_PRODUCTION_COMPLETE"
    SANDBOX_SESSION_CREATED  = "SANDBOX_SESSION_CREATED"
    # Deployment
    ADA_ACTIVATED            = "ADA_ACTIVATED"
    CREDENTIAL_MINTED        = "CREDENTIAL_MINTED"
    VIDEO_PUBLISHED          = "VIDEO_PUBLISHED"
    # Improvement
    LEARNER_MILESTONE        = "LEARNER_MILESTONE"
    WEAK_SPOT_DETECTED       = "WEAK_SPOT_DETECTED"
    IMPROVEMENT_REQUIRED     = "IMPROVEMENT_REQUIRED"
    REVISION_COMPLETE        = "REVISION_COMPLETE"

@dataclass
class CreativeEvent:
    type: CreativeEventType
    book_id: str                      # e.g., "B-021"
    clone_identity: str               # "lippytmai" | "lippytm" | "Charles"
    payload: dict
    timestamp: datetime = None
    correlation_id: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
```

---

## 5. Fabric's Role in the Creative Process

Before every creative act, the agent queries Fabric to load relevant context:

```python
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class FabricCreativeQuery:
    """Query Fabric before starting any creative work."""
    topic: str
    level: str                    # "Beginner" | "Intermediate" | "Advanced"
    book_id: str
    prerequisite_book_ids: List[str] = field(default_factory=list)

@dataclass
class FabricCreativeContext:
    """What Fabric returns for a creative task."""
    related_books: List[str]          # books on same topic
    learner_weak_spots: List[str]     # from GESN analytics
    cross_links: List[str]            # docs to reference
    concept_graph: dict               # knowledge graph nodes
    prior_corrections: List[str]      # Ch10 corrections from prior batches
    recommended_depth: str            # "shallow" | "standard" | "deep"

class FabricCreativeAdapter:
    """Fabric interface for the Creative Building Process."""

    def query_for_book(self, query: FabricCreativeQuery) -> FabricCreativeContext:
        # 1. Graph traversal for related nodes
        # 2. Learner analytics aggregation (GESN)
        # 3. Cross-link discovery
        # Returns: full creative context
        ...

    def store_book_node(self, book_id: str, metadata: dict) -> None:
        """After G13: store book as a permanent Fabric node."""
        ...

    def update_weak_spots(self, book_id: str, analytics: dict) -> None:
        """After deployment: store learner weak spots for future revisions."""
        ...
```

---

## 6. Clone Identity Assignment in the Creative Process

| Stage | Primary Clone | Fallback | Notes |
|---|---|---|---|
| Curriculum planning | `lippytmai` | — | P011-PLAN-001 |
| Ebook drafting | `lippytmai` | — | Teach mode, always |
| Video script | `lippytmai` | — | ACVSScriptAgent |
| Quality review G1–G12 | `lippytmai` | `lippytm` | Automated |
| G13 approval | **Charles Earl Lipshay** | — | NEVER automated |
| Deployment/builds | `lippytm` | — | GitHub, CI/CD |
| Experimental content | `Lippy Killjoy` | — | Requires HumanApprovalGate |

---

## 7. The HDVG Scene Manifest — The Ebook-to-Video Bridge

Every approved ebook generates a HDVG scene manifest, which is the input to ACVS:

```json
{
  "book_id": "B-021",
  "title": "The Linux Filesystem Explained",
  "mode": "Tutorial",
  "narrator": "lippytmai",
  "voice_id": "elevenlabs-lippytmai",
  "scenes": [
    {
      "id": "scene-001",
      "title": "What is the FHS?",
      "narration": "The Linux Filesystem Hierarchy Standard is a contract. Every directory has a purpose. Today we learn that contract.",
      "visual_prompt": "Animated tree expanding from / root to /etc /var /home /usr /tmp, each glowing as narrated",
      "duration_sec": 45
    },
    {
      "id": "scene-002",
      "title": "The /etc directory",
      "narration": "Everything in /etc is configuration. If you want to know how a service is set up, start here.",
      "visual_prompt": "Terminal with ls /etc highlighted, scrolling through config files",
      "code_block": "ls /etc | head -20",
      "duration_sec": 60
    },
    {
      "id": "scene-003",
      "title": "Build Challenge",
      "narration": "Your mission: run filesystem-navigator.sh and share the /var/log output.",
      "visual_prompt": "Mission brief card: 'Audit your system'",
      "interactive_overlay": {
        "type": "build_gate",
        "challenge": "Run ~/scripts/filesystem-navigator.sh",
        "expected_output_contains": "Disk Usage"
      },
      "duration_sec": 30
    }
  ]
}
```

---

## 8. The Creative Calendar

```
PHASE 1 COMPLETE: B-001–B-025 (Linux Foundations) ✅
├── Batch 1 (B-001–B-005):  ✅ G13 APPROVED
├── Batch 2 (B-006–B-010):  ✅ G13 APPROVED
├── Batch 3 (B-011–B-015):  ✅ G13 APPROVED
├── Batch 4 (B-016–B-020):  ✅ G13 APPROVED
└── Batch 5 (B-021–B-025):  ⏳ G13 PENDING

PHASE 2: B-026–B-050 (Python Foundations) — begins after Phase 1 G13
├── Batch 6  (B-026–B-030):  Python basics: first program, types, functions, files, OOP
├── Batch 7  (B-031–B-035):  Python intermediate: decorators, generators, async, testing
├── Batch 8  (B-036–B-040):  Python data: pandas, numpy, matplotlib, APIs, JSON
├── Batch 9  (B-041–B-045):  Python automation: web scraping, bots, cron, file automation
└── Batch 10 (B-046–B-050):  Python AI: OpenAI API, LangChain, embeddings, RAG basics

PHASE 3: B-051–B-075 (Web3 / Blockchain Foundations) — CBSLL integration
PHASE 4: B-076–B-100 (AI & ACSS Deep Dive)
```

---

## 9. Quality Metrics Dashboard

| Metric | Current Value | Target |
|---|---|---|
| Ebooks drafted | 25 / 300 | 300 |
| Ebooks G13 approved | 20 / 300 | 300 |
| Videos produced | 20 scripts / 25 approved | Matches approved books |
| Credentials minted | 20 | Matches approved books |
| Learner completions | — | Growing |
| Average quiz score | — | ≥ 80% |
| GESN retention rate | — | ≥ 70% per chapter |

---

## 10. Further Reading

- 📄 [`docs/ai-clone-engine-swarms.md`](ai-clone-engine-swarms.md) — ACSS architecture and Hermes/Fabric details
- 📄 [`docs/ai-copilot-video-sandbox-creator.md`](ai-copilot-video-sandbox-creator.md) — ACVS full spec
- 📄 [`docs/ai-deployment-activations.md`](ai-deployment-activations.md) — ADA deployment system
- 📄 [`docs/P011-QR-001-quality-review-engine.md`](P011-QR-001-quality-review-engine.md) — 13-gate QEP system
- 📄 [`docs/P011-EBOOK-000-course-series-master-plan.md`](P011-EBOOK-000-course-series-master-plan.md) — 300-book master plan
- 🏠 [`README.md`](../README.md) — Encyclopedia home

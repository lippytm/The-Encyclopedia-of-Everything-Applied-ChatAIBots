# ACSS Sandbox Ecosystem: AI Clone + Hermes + Fabric Learning Environments

> *"You don't truly understand a system until you can break it, rebuild it, and teach it to a machine. The Sandbox is where learning becomes doing."*
> — lippytmai

---

## 1. What Is the ACSS Sandbox Ecosystem?

The **ACSS Sandbox Ecosystem** is the live, interactive intelligence layer of the lippytm.ai AI Conglomerate Swarms System (ACSS). It transforms every Earn-while-you-Learn book into a **living, executable environment** — where learners don't just read about systems, they run them, test them, break them, and earn credentials by proving mastery through action.

The Sandbox Ecosystem merges five ACSS pillars into a single learning loop:

| Pillar | Role in the Sandbox |
|---|---|
| **AI Clone Engine** | Provides identity-aware instructors (lippytmai, lippytm, Lippy Killjoy, Charles) |
| **Hermes** | Routes learning events, progress signals, and Sandbox triggers across all platforms |
| **Fabric** | Builds and updates the learner's personal knowledge graph from Sandbox activity |
| **ADA (AI Deployment Activations)** | Executes book environments, quiz sessions, and credential claims |
| **ACVS (AI Copilot Video Sandbox Creator)** | Generates real-time video explainers tied to Sandbox sessions |

### The Core Loop

```
READ → COPY → RUN → BREAK → FIX → VERIFY → EARN
 📘      🖥️     ⚡    🔥      🔧    ✅       🏅
```

Every Sandbox session follows this 7-step loop. It is the operational heartbeat of the Earn-while-you-Learn philosophy.

---

## 2. Sandbox Environment Types

The ACSS Sandbox supports **six environment types**, mapped to the 300-book series:

| Environment Type | Books | Description |
|---|---|---|
| **Linux Shell Sandbox** | B-001–B-055 | Interactive terminal, file system, process simulation |
| **Python REPL Sandbox** | B-026–B-055 | Live Python REPL with lippytmai coaching prompts |
| **Blockchain Testnet Sandbox** | B-056–B-100 | Hardhat/Foundry local chain + Sepolia testnet bridge |
| **AI Copilot Sandbox** | B-101–B-150 | LLM playground, agent harness, RAG pipeline runner |
| **Production Systems Sandbox** | B-151–B-200 | Docker, CI/CD, monitoring, cloud deploy simulation |
| **Integration Sandbox** | B-201–B-300 | Full-stack ACSS environment combining all prior types |

### Environment Anatomy

Every Sandbox environment is a Docker container launched by ADA:

```yaml
# docker-compose.sandbox.yml (template)
version: "3.9"
services:
  sandbox:
    image: lippytmai/acss-sandbox:${BOOK_ID}
    environment:
      - BOOK_ID=${BOOK_ID}
      - CLONE_IDENTITY=lippytmai
      - HERMES_ENDPOINT=http://hermes:8400/event
      - FABRIC_ENDPOINT=http://fabric:8500/node
      - ADA_CREDENTIAL_API=http://ada:8000/credential
    ports:
      - "8888:8888"   # JupyterLab interface
      - "3000:3000"   # Web UI (dApp sandbox)
      - "8545:8545"   # Hardhat JSON-RPC (blockchain sandbox)
    volumes:
      - ./sandbox-workspace:/workspace
    depends_on:
      - hermes
      - fabric
      - ada

  hermes:
    image: lippytmai/hermes:latest
    ports:
      - "8400:8400"

  fabric:
    image: lippytmai/fabric:latest
    ports:
      - "8500:8500"

  ada:
    image: lippytmai/ada:latest
    ports:
      - "8000:8000"
```

---

## 3. AI Clone Identity in the Sandbox

Each Sandbox session is guided by one of the four AI clone identities:

| Clone | Mode | Sandbox Role |
|---|---|---|
| **lippytmai** | TEACH | Default instructor. Explains concepts, generates prompts, narrates lessons. |
| **lippytm** | BUILD | GitHub builder mode. Reviews code, runs CI checks, opens PRs from sandbox output. |
| **Lippy Killjoy** | BREAK | Adversarial tester. Deliberately introduces bugs and edge cases to test the learner. |
| **Charles Earl Lipshay** | APPROVE | Human gate. Reviews capstone output and signs off on credential claims. |

### Clone Activation via Hermes

```python
# hermes_clone_activate.py
import httpx

def activate_clone(clone: str, session_id: str, book_id: str) -> dict:
    """
    Activate a clone identity for a Sandbox session via Hermes.
    clone: 'lippytmai' | 'lippytm' | 'lippy_killjoy' | 'charles'
    """
    payload = {
        "event_type": "sandbox.clone.activate",
        "clone_identity": clone,
        "session_id": session_id,
        "book_id": book_id,
        "timestamp": "2026-08-28T08:00:00Z"
    }
    response = httpx.post("http://hermes:8400/event", json=payload)
    return response.json()

# Example: Start a lippytmai TEACH session for B-101
event = activate_clone("lippytmai", "sess-001", "B-101")
print(event)
# → {"status": "ok", "clone": "lippytmai", "mode": "TEACH", "session_id": "sess-001"}
```

---

## 4. Hermes Event Schema for Sandbox Sessions

Hermes is the nervous system of the Sandbox. Every learner action emits a Hermes event that routes to the correct downstream service (Fabric, ADA, ACVS).

### Full Sandbox Event Taxonomy

| Event Type | Trigger | Downstream Target |
|---|---|---|
| `sandbox.session.start` | Learner opens a Sandbox | Fabric (new node), ADA (session log) |
| `sandbox.clone.activate` | Clone identity selected | Hermes broadcast |
| `sandbox.step.complete` | Learner completes a READ→RUN step | Fabric (edge update), ACVS (scene trigger) |
| `sandbox.code.run` | Code executed in REPL/terminal | ADA (execution log), Hermes (result broadcast) |
| `sandbox.code.error` | Runtime error caught | Clone (Lippy Killjoy debug prompt) |
| `sandbox.code.fixed` | Error resolved by learner | Fabric (mastery node), ADA (fix log) |
| `sandbox.quiz.start` | Quiz session launched | ADA (quiz runner) |
| `sandbox.quiz.pass` | Score ≥ 80% | ADA (credential unlock), Fabric (mastery +1) |
| `sandbox.quiz.fail` | Score < 80% | Clone (lippytmai retry coaching) |
| `sandbox.capstone.submit` | Full capstone project submitted | Hermes (Charles gate), ADA (review queue) |
| `sandbox.capstone.approve` | Charles G13 approval | ADA (credential mint), Fabric (achievement node) |
| `sandbox.credential.claim` | Learner claims badge | ADA (NFT/PDF issue), Hermes (broadcast to all platforms) |
| `sandbox.session.end` | Session closed | Fabric (session summary node), ADA (progress log) |

### Event Payload Schema

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SandboxEvent(BaseModel):
    event_type: str                    # e.g. "sandbox.step.complete"
    session_id: str                    # UUID for this sandbox session
    learner_id: str                    # learner's platform handle
    book_id: str                       # e.g. "B-101"
    clone_identity: str                # active clone for this event
    payload: dict                      # event-specific data
    timestamp: datetime = datetime.now()
    hermes_routed: bool = False
    fabric_synced: bool = False
```

---

## 5. Fabric Knowledge Graph — Sandbox Integration

Every Sandbox action feeds the **Fabric Knowledge Graph** — the learner's evolving personal model of what they know, what they've built, and what they've earned.

### Fabric Node Types

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class FabricSandboxNode:
    node_id: str               # e.g. "B-101-step-3-python-llm"
    book_id: str               # e.g. "B-101"
    node_type: str             # 'concept' | 'skill' | 'project' | 'credential'
    label: str                 # human-readable name
    mastery_score: float       # 0.0–1.0 from quiz/capstone performance
    connections: List[str]     # related node IDs (CCSLL/CBSLL cross-links)
    sandbox_runs: int = 0      # how many times learner executed this node's code
    errors_fixed: int = 0      # bugs fixed in this node's sandbox
    credential_earned: str = ""  # credential ID if earned

@dataclass
class FabricLearnerGraph:
    learner_id: str
    nodes: List[FabricSandboxNode] = field(default_factory=list)
    total_mastery: float = 0.0
    credentials_earned: List[str] = field(default_factory=list)
    active_book: str = ""

    def add_sandbox_activity(self, node_id: str, runs: int, errors_fixed: int) -> None:
        for node in self.nodes:
            if node.node_id == node_id:
                node.sandbox_runs += runs
                node.errors_fixed += errors_fixed
                node.mastery_score = min(1.0, node.mastery_score + 0.05 * runs)
        self._recalculate_total_mastery()

    def _recalculate_total_mastery(self) -> None:
        if self.nodes:
            self.total_mastery = sum(n.mastery_score for n in self.nodes) / len(self.nodes)
```

### Fabric Graph Visualization

```
[B-001: Terminal] ──► [B-006: Processes] ──► [B-026: Python Basics]
        │                                              │
        ▼                                              ▼
[B-002: Commands] ──► [B-011: Env Vars] ──► [B-031: Exceptions]
        │                                              │
        ▼                                              ▼
[CLL-L1 Credential] ──────────────────► [PEL-L1 Credential]
                                                       │
                                                       ▼
                                         [B-056: Blockchain] ──► [BCL-L1 Credential]
                                                                         │
                                                                         ▼
                                                              [B-101: LLMs] ──► [AIL-L1 Badge]
```

---

## 6. The ACSS AI Copilot Sandbox — Learning Modes

The AI Copilot Sandbox supports **five learning modes**, activated by Hermes:

### Mode 1: TEACH Mode (lippytmai)

```
Copilot Prompt → Concept Explanation → Code Example → Run It → Quiz
```

**Example Copilot prompt (B-101 LLM Foundations):**
```
@lippytmai sandbox B-101 TEACH
Topic: What is a Large Language Model?
Mode: Ebook explainer → Code → Run → Quiz
```

**lippytmai response:**
```
📘 TEACH: A Large Language Model (LLM) is a neural network trained on 
billions of tokens to predict the next token in a sequence...

🖥️ CODE:
from transformers import pipeline
generator = pipeline("text-generation", model="gpt2")
result = generator("The ACSS sandbox is", max_length=50)
print(result[0]["generated_text"])

▶️ RUN IT: lippytmai-launch sandbox B-101 step-1

🎯 QUIZ: What does "temperature" control in an LLM?
```

### Mode 2: BUILD Mode (lippytm)

```
Specification → Scaffold → Code Review → CI Check → Commit
```

```
@lippytm sandbox B-101 BUILD
Task: Build a minimal LLM wrapper class with token counting
Output: Python class + pytest tests + GitHub commit
```

### Mode 3: BREAK Mode (Lippy Killjoy)

```
Working Code → Inject Bug → Learner Debug → Fix → Verify
```

```
@lippy_killjoy sandbox B-101 BREAK
Target: the LLM wrapper class
Bug type: Off-by-one in token counter + missing API key error handling
Difficulty: MEDIUM
```

### Mode 4: VERIFY Mode (ADA)

```
Submission → Automated Tests → Score → Credential Unlock Check
```

```
@ada sandbox B-101 VERIFY
Session: sess-001
Learner: @student-handle
Check: All 5 capstone tests passing? Credential AIL-L0-B101-LLMFoundation ready?
```

### Mode 5: DEPLOY Mode (Full ACSS Stack)

```
Local Sandbox → Hermes Broadcast → Fabric Update → ADA Credential → Platform Publish
```

```
@acss sandbox B-101 DEPLOY
Action: Capstone complete → claim credential → publish to LinkedIn + GitHub
Hermes events: sandbox.capstone.approve → sandbox.credential.claim
```

---

## 7. Sandbox Session Lifecycle

```
1. INIT       lippytmai-launch sandbox B-XXX
                   │
2. IDENTIFY   Clone identity activated (default: lippytmai TEACH)
                   │
3. LOAD       Docker container starts, Hermes/Fabric/ADA connect
                   │
4. LEARN      READ → COPY → RUN → BREAK → FIX (steps 1–N from book chapters)
                   │
5. TEST       QUIZ session via ADA (/quiz endpoint)
                   │
6. BUILD      CAPSTONE project scaffolded and implemented
                   │
7. SUBMIT     Capstone submitted → Hermes event → Charles G13 queue
                   │
8. EARN       G13 APPROVED → ADA mints credential → Fabric updates graph
                   │
9. BROADCAST  Hermes publishes achievement to all 15 platforms
                   │
10. NEXT      Next book auto-recommended by Fabric learning path
```

---

## 8. Sandbox CLI Reference

The `lippytmai-launch` CLI is the primary entry point for all Sandbox sessions:

```bash
# Launch a full Sandbox session for book B-101
lippytmai-launch sandbox B-101

# Launch with a specific clone identity
lippytmai-launch sandbox B-101 --clone lippy_killjoy --mode BREAK

# Run just the quiz
lippytmai-launch quiz B-101

# Submit capstone for G13 review
lippytmai-launch capstone B-101 --submit --learner @yourhandle

# Check credential status
lippytmai-launch credential B-101 --status

# List all ACTIVE sandboxes
lippytmai-launch sandbox --list

# Open the Fabric knowledge graph viewer
lippytmai-launch fabric --learner @yourhandle --graph

# Start full ACSS stack (Hermes + Fabric + ADA + Sandbox)
docker-compose -f docker-compose.sandbox.yml up
```

---

## 9. Sandbox Integration with CCSLL / CBSLL / CLL

The Sandbox ecosystem is language-aware. Each book maps to one of the three language libraries:

| Library | Coverage | Sandbox Shell |
|---|---|---|
| **CLL** (Complete Linux Library) | B-001–B-055 | `bash` + `zsh` + Linux containers |
| **CCSLL** (Complete Computer Software Language Library) | B-026–B-150 | Python REPL, TypeScript REPL, Rust playground |
| **CBSLL** (Complete Blockchain Software Language Library) | B-056–B-100 | Hardhat local chain, Foundry forge, Solidity REPL |

The **CSEL** (Complete Software Environments Library) provides 14 pre-built sandbox environment types that ADA pulls from to spin up book-specific containers.

---

## 10. Earn-While-You-Learn in the Sandbox

Every sandbox action has a **learning value** and an **earning value**:

| Action | Learning Points | Earning Trigger |
|---|---|---|
| Complete a READ step | +1 LP | — |
| Run code successfully | +2 LP | — |
| Fix a bug from BREAK mode | +5 LP | — |
| Pass a quiz (≥80%) | +10 LP | Credential unlock eligibility |
| Complete a capstone project | +50 LP | Credential claim ready |
| G13 approved capstone | — | **Credential minted** (NFT + PDF) |
| Publish credential to platforms | — | **Revenue event** (course sales, affiliate) |

The **Learning Points (LP)** system feeds into the Fabric graph, unlocking recommended next books and advanced Sandbox features (like DEPLOY mode and Lippy Killjoy BREAK sessions).

---

## 11. Sandbox Environment Quick-Start

### Prerequisites

```bash
# Install the ACSS CLI
pip install lippytmai-launch

# Set up environment variables
export OPENAI_API_KEY=your_key_here
export ELEVENLABS_API_KEY=your_key_here
export ADA_API_URL=http://localhost:8000
export HERMES_URL=http://localhost:8400
export FABRIC_URL=http://localhost:8500
```

### First Sandbox Session (B-001 — The Terminal)

```bash
# Clone the ACSS sandbox stack
git clone https://github.com/lippytm/acss-sandbox
cd acss-sandbox

# Start the full stack
docker-compose -f docker-compose.sandbox.yml up -d

# Open the first book sandbox
lippytmai-launch sandbox B-001

# Expected output:
# 🟢 ACSS Sandbox — B-001: The Terminal and the Curious Mind
# 🤖 Clone: lippytmai [TEACH mode]
# 📡 Hermes: connected (http://localhost:8400)
# 🔗 Fabric: connected (http://localhost:8500)
# 🚀 ADA: connected (http://localhost:8000)
# 📘 Step 1: Open your terminal. Try: echo "Hello, ACSS"
# ▶️  Type 'run' to execute, 'next' to advance, 'break' to activate Lippy Killjoy
```

---

## Further Reading

- 📄 [AI Clone Engine Swarms (ACSS Architecture)](./ai-clone-engine-swarms.md)
- 📄 [AI Copilot Video Sandbox Creator (ACVS)](./ai-copilot-video-sandbox-creator.md)
- 📄 [ACSS Cross-Platform Copilot Deployment](./acss-cross-platform-copilot-deployment.md)
- 📄 [AI Deployment Activations (ADA)](./ai-deployment-activations.md)
- 📄 [Creative Building Process](./creative-building-process.md)
- 📄 [Product Excellence Framework](./PRODUCT-EXCELLENCE-FRAMEWORK.md)
- 📄 [← Back to README](../README.md)

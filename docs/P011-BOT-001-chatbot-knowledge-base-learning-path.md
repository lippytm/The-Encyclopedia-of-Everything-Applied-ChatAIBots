# P-011-BOT-001 — Applied Chatbot Knowledge-Base Learning Path
### *From First Prompt to Production AI Chatbot — The Complete Earn-while-you-Learn Journey*

> *"A chatbot without a knowledge base is an echo. A chatbot with a knowledge base is a teacher. A chatbot with a living, evolving knowledge base connected to a swarm of AI agents is a civilization."*
> — Charles Earl Lipshay (lippytm.ai)

---

## Overview

This document is the canonical **applied chatbot knowledge-base learning path** for the Prompt #11 ecosystem. It maps the complete journey — from understanding what a chatbot and knowledge base are, to building a production-grade AI chatbot powered by the full ACSS stack (Hermes + Fabric + AMIL + CCSLL/CBSLL).

Every step produces a working, testable artifact. Every completed artifact earns an Earn-while-you-Learn credential. Every credential is tracked on-chain as a SkillBadge (ERC-721 on Base).

---

## 1. What Is a Knowledge-Base Chatbot?

| Term | Definition | Example in This Ecosystem |
|---|---|---|
| **Chatbot** | Software that converses with a user in natural language via a defined interface | Slack `/ask` command handler |
| **Knowledge Base (KB)** | Structured + unstructured information store that the chatbot retrieves answers from | ACSS Fabric (vector store + knowledge graph) |
| **RAG** | Retrieval-Augmented Generation — fetch relevant KB chunks, inject into LLM prompt | Fabric → Qdrant → Claude prompt |
| **AI Chatbot** | A chatbot backed by an LLM for understanding and generation, not just pattern matching | lippytmai agent on Slack |
| **CRM Chatbot** | Chatbot that reads/writes customer/learner relationship data | Slack AI CRM (`LearnerProfile`, `/progress`) |
| **Autonomous Agent** | Chatbot that takes actions (search, write files, call APIs) without per-action human approval | ACSS coding/teaching agents (Tier 3+) |

---

## 2. The 6-Level Learning Path

### Level 0 — Curious: Understand the Concepts

**Goal:** Know what a chatbot, knowledge base, LLM, and RAG are. Use an existing chatbot.

**Lessons:**
- What is a Large Language Model? (no code required)
- What is a prompt? What is context? What is a token?
- Try: Ask Claude a question via API. Read the response.
- Explore: The Slack AI CRM chatbot commands (`/ask`, `/learn`)

**Build artifact:** A plain-text prompt file that asks Claude to explain one concept from this encyclopedia. Save it as `prompts/my-first-prompt.txt`.

```text
# prompts/my-first-prompt.txt
You are lippytmai, an AI teaching assistant in the lippytm.ai ecosystem.

The learner has asked: "What is a knowledge base, and how does it make a chatbot smarter?"

Explain this in 3 short paragraphs at a beginner level. Use a real-world analogy.
Give one example from the lippytm.ai AI Conglomerate Swarms System.
```

**Credential:** CCSLL L0 — Curious / First Prompt

---

### Level 1 — Apprentice: Build Your First Chatbot

**Goal:** Build a working chatbot that responds to user messages using a hardcoded knowledge base.

**Lessons:**
- Python basics: functions, dictionaries, `if/else`
- What is an API? HTTP requests in Python with `httpx`
- OpenAI / Anthropic API authentication

**Build artifact — simple knowledge-base chatbot:**

```python
# chatbots/level1_kb_chatbot.py
"""Level 1 — Simple knowledge-base chatbot backed by a static FAQ dictionary."""

import os
import httpx

# Static knowledge base (Level 1 — no vector store yet)
KNOWLEDGE_BASE: dict[str, str] = {
    "what is acss": (
        "ACSS stands for AI Conglomerate Swarms System. It is the self-learning "
        "intelligence layer for all lippytm.ai projects. It merges 8 systems: "
        "Clone Engine, Hermes, Fabric, CCSLL, CBSLL, CLL, OMARCHY, and CSEL."
    ),
    "what is hermes": (
        "Hermes is the cross-repo message bus of the ACSS. It routes events between "
        "all repositories and platforms, and includes a HumanApprovalGate for decisions "
        "that require Charles's review."
    ),
    "what is fabric": (
        "Fabric is the knowledge graph and pattern synthesis engine of the ACSS. "
        "It stores all learning events, detects recurring patterns, and drives the "
        "self-improvement loop."
    ),
    "what is earn while you learn": (
        "Earn-while-you-Learn is the lippytm.ai philosophy: every learning action "
        "produces a verifiable credential, and verified credentials unlock earning "
        "opportunities (contributions, teaching, building, trading, and more)."
    ),
}


def find_answer(question: str) -> str | None:
    """Find the best matching answer in the static knowledge base."""
    q = question.lower().strip("?").strip()
    for key, answer in KNOWLEDGE_BASE.items():
        if key in q or all(word in q for word in key.split()):
            return answer
    return None


def ask_llm_fallback(question: str, api_key: str) -> str:
    """Fall back to Claude API when no KB match is found."""
    response = httpx.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": "claude-3-haiku-20240307",
            "max_tokens": 256,
            "messages": [{"role": "user", "content": question}],
        },
    )
    return response.json()["content"][0]["text"]


def chat(question: str) -> str:
    """Main chatbot entry point."""
    # 1. Try static KB first (fast, free)
    kb_answer = find_answer(question)
    if kb_answer:
        return f"[KB] {kb_answer}"

    # 2. Fall back to LLM
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if api_key:
        return f"[LLM] {ask_llm_fallback(question, api_key)}"

    return "I don't know the answer to that yet. Add it to the knowledge base!"


if __name__ == "__main__":
    print("Level 1 KB Chatbot — type 'quit' to exit")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit"):
            break
        print(f"Bot: {chat(user_input)}\n")
```

```python
# tests/test_level1_kb_chatbot.py
import pytest
from chatbots.level1_kb_chatbot import find_answer, chat

def test_kb_match():
    assert "ACSS" in find_answer("what is acss")

def test_kb_no_match():
    assert find_answer("what is the weather today") is None

def test_chat_kb_response():
    result = chat("what is hermes")
    assert result.startswith("[KB]")
    assert "message bus" in result
```

**Credential:** CCSLL L1 — Apprentice / First Chatbot

---

### Level 2 — Builder: Add a Real Knowledge Base with Vector Search

**Goal:** Replace the static dictionary with a vector store (Qdrant) for semantic search. Add document ingestion.

**Lessons:**
- What is a vector embedding? What is semantic similarity?
- How does RAG work: embed → store → retrieve → generate
- Qdrant: collections, points, search
- `sentence-transformers` for local embeddings

**Build artifact — RAG chatbot:**

```python
# chatbots/level2_rag_chatbot.py
"""
Level 2 — RAG chatbot with Qdrant vector store.
Ingests encyclopedia docs, retrieves semantically relevant chunks, passes to Claude.
"""

from __future__ import annotations
import os
import pathlib
import httpx
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

COLLECTION = "encyclopedia"
EMBED_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 500  # characters per chunk


class EncyclopediaKnowledgeBase:
    """Vector knowledge base built from the Encyclopedia of Everything Applied."""

    def __init__(self, qdrant_url: str = "http://localhost:6333") -> None:
        self.client = QdrantClient(url=qdrant_url)
        self.encoder = SentenceTransformer(EMBED_MODEL)
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        existing = [c.name for c in self.client.get_collections().collections]
        if COLLECTION not in existing:
            self.client.create_collection(
                collection_name=COLLECTION,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )

    def ingest_directory(self, docs_dir: str) -> int:
        """Ingest all .md files from a directory into the knowledge base."""
        docs_path = pathlib.Path(docs_dir)
        points: list[PointStruct] = []
        point_id = 0

        for md_file in docs_path.glob("**/*.md"):
            content = md_file.read_text(encoding="utf-8")
            # Chunk the document
            for i in range(0, len(content), CHUNK_SIZE):
                chunk = content[i : i + CHUNK_SIZE]
                if len(chunk.strip()) < 50:
                    continue
                vector = self.encoder.encode(chunk).tolist()
                points.append(
                    PointStruct(
                        id=point_id,
                        vector=vector,
                        payload={
                            "text": chunk,
                            "source": str(md_file.relative_to(docs_path)),
                        },
                    )
                )
                point_id += 1

        self.client.upsert(collection_name=COLLECTION, points=points)
        return point_id

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """Retrieve the most semantically relevant chunks for a query."""
        query_vector = self.encoder.encode(query).tolist()
        results = self.client.search(
            collection_name=COLLECTION,
            query_vector=query_vector,
            limit=top_k,
        )
        return [
            {"text": r.payload["text"], "source": r.payload["source"], "score": r.score}
            for r in results
        ]


class RAGChatbot:
    """Level 2 RAG chatbot: retrieve context from KB, then generate with Claude."""

    SYSTEM_PROMPT = """You are lippytmai, an AI teaching assistant for the lippytm.ai ecosystem.
Answer questions using only the provided knowledge base context.
If the context doesn't contain the answer, say so clearly.
Always cite the source document name from the context."""

    def __init__(self, kb: EncyclopediaKnowledgeBase, anthropic_api_key: str) -> None:
        self.kb = kb
        self.api_key = anthropic_api_key

    def ask(self, question: str) -> str:
        # 1. Retrieve relevant chunks
        chunks = self.kb.search(question, top_k=3)
        context = "\n\n".join(
            f"[Source: {c['source']}]\n{c['text']}" for c in chunks
        )

        # 2. Build RAG prompt
        user_message = f"""Knowledge Base Context:
{context}

---
Learner Question: {question}"""

        # 3. Generate with Claude
        response = httpx.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 512,
                "system": self.SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": user_message}],
            },
            timeout=30.0,
        )
        return response.json()["content"][0]["text"]
```

**Credential:** CCSLL L2 — Builder / RAG Chatbot

---

### Level 3 — Engineer: Connect to Slack + CRM

**Goal:** Deploy the RAG chatbot as a production Slack bot. Add learner profile tracking (CRM). Connect to Hermes.

**Lessons:**
- Slack Bolt for Python: socket mode, slash commands, Block Kit
- PostgreSQL: learner profiles, interaction logs
- Environment variables and secrets management (NEVER hardcode keys)
- Async Python: `asyncio`, `async def`

**Key reference:** `docs/slack-ai-crm-integration.md` — the complete Level 3 build reference.

```python
# Integration checkpoint: verify the full Level 3 stack is running
async def health_check() -> dict:
    """Verify all Level 3 components are reachable."""
    import asyncio
    import httpx

    results = {}
    async with httpx.AsyncClient(timeout=5.0) as client:
        # Check Qdrant
        try:
            r = await client.get("http://localhost:6333/collections")
            results["qdrant"] = "ok" if r.status_code == 200 else "error"
        except Exception:
            results["qdrant"] = "unreachable"

        # Check PostgreSQL
        try:
            import asyncpg
            conn = await asyncpg.connect(os.environ["DATABASE_URL"])
            await conn.fetchval("SELECT 1")
            await conn.close()
            results["postgres"] = "ok"
        except Exception:
            results["postgres"] = "unreachable"

        # Check Hermes
        try:
            r = await client.get(f"{os.environ.get('HERMES_URL','http://localhost:8080')}/health")
            results["hermes"] = "ok" if r.status_code == 200 else "error"
        except Exception:
            results["hermes"] = "unreachable"

    return results
```

**Credential:** CCSLL L3 — Engineer / Production Slack CRM Chatbot

---

### Level 4 — Specialist: Build an Autonomous Teaching Agent

**Goal:** Upgrade the chatbot to an autonomous teaching agent that plans multi-lesson curricula, tracks learner progress, adapts to proficiency, and issues on-chain credentials.

**Lessons:**
- ReAct (Reason + Act) agent pattern
- Tool calling with LLMs (function calling / tool use)
- Curriculum planning with Fabric knowledge graph
- On-chain credential minting (ERC-721 on Base)
- The HumanApprovalGate pattern for Level 4+ skills

**Architecture diagram:**

```
Learner (Slack)
    │
    ▼ /ask or /learn
[Slack Bolt Handler]
    │
    ▼
[lippytmai Teaching Agent] ── tools ──▶ [KB Search (Qdrant)]
    │                                   [Progress DB (PostgreSQL)]
    │                                   [Curriculum Planner (Fabric)]
    │                                   [Badge Issuer (Base ERC-721)]
    │
    ▼
[AMIL Model Router] ──▶ Claude 3.5 (teaching)
                    ──▶ GPT-4o (tool calling, JSON)
    │
    ▼
[Hermes] ──▶ broadcasts "teaching_interaction" event to all repos
```

```python
# chatbots/level4_teaching_agent.py
"""
Level 4 — Autonomous teaching agent with tool calling and curriculum planning.
Uses the ReAct pattern: Reason → Act (call tool) → Observe → Repeat → Respond.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict[str, Any]
    fn: Callable[..., Any]


class TeachingAgent:
    """
    Autonomous teaching agent that plans curricula, tracks progress,
    and issues on-chain credentials.

    Tools available:
    - search_kb: semantic search in encyclopedia KB
    - get_learner_progress: fetch learner's current proficiency
    - plan_next_lesson: Fabric curriculum planning
    - issue_credential: mint ERC-721 SkillBadge on Base
    - request_human_approval: HumanApprovalGate for Level 4+ actions
    """

    MAX_TOOL_ROUNDS = 5  # prevent infinite loops

    def __init__(self, tools: list[Tool], amil_client: Any, hermes_client: Any) -> None:
        self.tools = {t.name: t for t in tools}
        self.amil = amil_client
        self.hermes = hermes_client

    async def teach(self, learner_id: str, question: str) -> str:
        """Run the ReAct teaching loop for a learner question."""
        conversation: list[dict] = [{"role": "user", "content": question}]
        tool_schema = [
            {
                "name": t.name,
                "description": t.description,
                "input_schema": t.parameters,
            }
            for t in self.tools.values()
        ]

        for _ in range(self.MAX_TOOL_ROUNDS):
            response = await self.amil.call(
                model="claude-3-5-sonnet-20241022",
                messages=conversation,
                tools=tool_schema,
                system=f"""You are lippytmai, an autonomous teaching agent.
Learner ID: {learner_id}
Use tools to search the knowledge base, check learner progress, and plan the best lesson.
Always verify what the learner already knows before teaching.
Issue credentials only after verifying competency via the progress tool.""",
            )

            if response.stop_reason == "end_turn":
                return response.content[0].text

            # Process tool calls
            for block in response.content:
                if block.type == "tool_use":
                    tool_fn = self.tools.get(block.name)
                    if tool_fn:
                        result = await tool_fn.fn(**block.input)
                        conversation.append({
                            "role": "assistant",
                            "content": response.content,
                        })
                        conversation.append({
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": block.id,
                                    "content": str(result),
                                }
                            ],
                        })
                        break

        return "Teaching session complete. Check your progress dashboard with /progress."
```

**Credential:** CCSLL L4 — Specialist / Autonomous Teaching Agent *(requires Charles review)*

---

### Level 5 — Master: Contribute to the ACSS Fabric

**Goal:** Build a new Fabric pattern module that improves the entire ecosystem's teaching intelligence. This is a contribution to the live ACSS — it affects every learner on every platform.

**Lessons:**
- Fabric pattern schema and knowledge graph structure
- Multi-repo coordination via Hermes
- ACSS self-evolution loop (ACD `FabricEvolutionEngine`)
- Contributing to a production AI system: PR discipline, evidence packets, rollback

**Deliverable:** A merged PR to the ACSS Fabric module that adds a new teaching pattern, with:
1. Pattern definition (what triggers it, what it teaches, what it produces)
2. Automated test suite (Pytest, ≥ 90% coverage)
3. Hermes event schema for the pattern
4. Quality Evidence Packet (QEP): learner outcomes, A/B test results, rollback plan
5. Charles's HumanApprovalGate sign-off

**Credential:** ACSS Fabric Contributor — Master *(Charles review and on-chain endorsement required)*

---

## 3. Chatbot Quality Standards (All Levels)

Every chatbot built in this ecosystem must meet these standards before earning a credential:

| Standard | Check | Tool |
|---|---|---|
| **No hallucination** | All factual claims cite KB source | RAG source attribution |
| **No secrets in code** | API keys, tokens only from env vars | `runtime-tools-secret_scanning` |
| **Tests pass** | ≥ 80% coverage for all Python code | Pytest + coverage |
| **Privacy** | No PII stored without consent | Privacy review checklist |
| **Accessible** | Responses readable at 8th grade level | Readability test |
| **Hermes integration** | All interactions published as events | Hermes event schema |
| **Graceful degradation** | Works when Qdrant/LLM/DB offline | Health check + fallback |
| **Fiction boundary** | Fictional characters never merged with real CRM | FictionBoundaryGate |

---

## 4. Earn-while-you-Learn Credential Map

```
L0: First Prompt            → CCSLL L0 SkillBadge (auto-issued)
L1: First Chatbot           → CCSLL L1 SkillBadge (auto-issued)
L2: RAG Chatbot             → CCSLL L2 SkillBadge (auto-issued)
L3: Production Slack CRM    → CCSLL L3 SkillBadge (auto-issued)
L4: Autonomous Agent        → CCSLL L4 SkillBadge (Charles review)
L5: Fabric Contributor      → ACSS Fabric Contributor (Charles endorsement)
```

All SkillBadges are ERC-721 tokens on Base. L4+ credentials lock until Charles approves the Quality Evidence Packet.

---

## 5. Next Actions

1. **Complete your Level 0 prompt file** — save it to `prompts/my-first-prompt.txt` in your fork.
2. **Run the Level 1 chatbot** — test all 4 KB entries and verify fallback behavior.
3. **Spin up Qdrant** — `docker run -p 6333:6333 qdrant/qdrant` and ingest the encyclopedia docs.
4. **Connect to Slack** — follow `docs/slack-ai-crm-integration.md` §2 for app setup.
5. **Open a PR** — document what you learned. Every contribution earns recognition.

---

## Further Reading

- 📄 [`docs/P011-STACK-001-repo-stack-profile.md`](P011-STACK-001-repo-stack-profile.md) — full technology stack for this learning path
- 📄 [`docs/P011-ENGINE-001-prompt11-engines.md`](P011-ENGINE-001-prompt11-engines.md) — the 8 Prompt #11 engines that power this chatbot
- 📄 [`docs/slack-ai-crm-integration.md`](slack-ai-crm-integration.md) — complete Level 3 Slack CRM reference
- 📄 [`docs/ai-model-intelligence-layer.md`](ai-model-intelligence-layer.md) — AMIL: which model to use for which chatbot task
- 📄 [`docs/ai-clone-engine-swarms.md`](ai-clone-engine-swarms.md) — ACSS: the swarm that powers every Level 4+ agent
- 📄 [`docs/P011-CRM-001-learning-system.md`](P011-CRM-001-learning-system.md) — CRM Educational Entertainment system
- 🏠 [`README.md`](../README.md) — Encyclopedia home

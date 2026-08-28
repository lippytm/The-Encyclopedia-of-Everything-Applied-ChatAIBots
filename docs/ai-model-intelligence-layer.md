# AI Model Intelligence Layer
### *LLM Selection, Fine-Tuning, RAG, Evaluation, and Model-Swapping Protocols for the ACSS*

> *"The model is not the mind. The mind is the system that knows which model to call, when, and why."*
> — Charles Earl Lipshay (lippytm.ai)

---

## Overview

The **AI Model Intelligence Layer (AMIL)** is the decision-making framework that governs which AI models are used for which tasks across all lippytm clone agents. It answers four core questions:

1. **Selection** — Which model is best for this task right now?
2. **Augmentation** — How do we make that model smarter with project-specific context?
3. **Evaluation** — Is the model performing well enough to trust?
4. **Evolution** — When and how do we upgrade, fine-tune, or swap models?

AMIL is maintained by Fabric and queried by Hermes for every significant clone task.

---

## 1. Model Selection Framework

### 1.1 The ACSS Model Roster

| Model | Provider | Strengths | Primary Use in ACSS |
|---|---|---|---|
| **Claude 3.5 / 4** | Anthropic | Long context, nuanced reasoning, safety | Complex architecture docs, multi-file refactors, teaching explanations |
| **GPT-4o / o3** | OpenAI | Code generation, tool use, JSON reliability | Structured data tasks, API integrations, trading signal parsing |
| **Gemini 1.5 / 2 Pro** | Google | Massive context window (1M+), multimodal | Codebase-wide analysis, image + code tasks |
| **Llama 3 / 3.1** | Meta (local) | Privacy-safe, free, customizable via fine-tune | Offline builds, OMARCHY local dev, sensitive code |
| **Mistral / Mixtral** | Mistral AI | Fast, efficient, instruction-following | High-volume routine tasks, batch code generation |
| **DeepSeek Coder** | DeepSeek | Specialized code intelligence | Solidity/Rust review, competitive coding tasks |
| **Qwen2.5-Coder** | Alibaba | Strong multilingual code | Non-English project docs, international learner support |
| **Codestral** | Mistral AI | Code completion specialist | OMARCHY inline completions, low-latency fill-in-middle |

### 1.2 Model Selection Matrix

| Task Type | Latency Need | Privacy | Recommended Model |
|---|---|---|---|
| Complex reasoning / architecture design | Low | Standard | Claude 4 / GPT-o3 |
| High-volume code generation | Medium | Standard | GPT-4o / Mistral Large |
| Full codebase analysis | Low | Standard | Gemini 2 Pro (1M context) |
| Local / offline build assistance | Any | **High** | Llama 3.1 / Mistral (Ollama) |
| Smart contract audit | Low | Standard | DeepSeek Coder + Claude audit pass |
| Inline code completion | **Ultra-low** | Standard | Codestral / Copilot (GitHub) |
| Teaching explanation | Medium | Standard | Claude 3.5 / lippytmai fine-tune |
| Trading signal analysis | **Real-time** | Standard | GPT-4o (tool mode) + custom signal model |
| Creative / Canon writing | Low | Standard | Claude + Lippy Killjoy fine-tune |
| Multimodal (diagram → code) | Low | Standard | Gemini 2 Pro / GPT-4o Vision |

### 1.3 Fabric-Driven Model Selection

Fabric maintains a live **model performance scoreboard** updated after every significant agent task:

```python
# Fabric model selection query
def select_model(task: dict) -> str:
    """
    Returns the optimal model ID for a given task based on
    Fabric's live performance scoreboard and task requirements.
    """
    task_type = task["type"]           # e.g., "code_review", "teaching", "trading"
    latency_class = task["latency"]    # "realtime" | "interactive" | "batch"
    privacy_flag = task["privacy"]     # True if sensitive data involved
    budget_class = task["budget"]      # "free" | "standard" | "premium"

    if privacy_flag:
        return fabric.get("best_local_model", default="llama3.1:70b")

    scores = fabric.query("model_scoreboard", filters={
        "task_type": task_type,
        "latency_class": latency_class,
        "budget_class": budget_class
    })
    return scores[0]["model_id"]  # highest-scoring model for this context
```

---

## 2. Context Augmentation (RAG & Brainkits)

### 2.1 Retrieval-Augmented Generation (RAG) Architecture

Every ACSS clone agent is augmented with project-specific context at query time using RAG. This prevents hallucination and ensures outputs match real repository conventions.

```
USER TASK / QUERY
       │
       ▼
  QUERY EXPANSION
  (Hermes enriches with task metadata)
       │
       ▼
  VECTOR RETRIEVAL
  (Fabric graph → top-K relevant chunks)
  ┌──────────────────────────────────┐
  │ - Repository architecture docs   │
  │ - Recent commit diffs            │
  │ - CCSLL / CBSLL / CSEL profiles  │
  │ - Clone identity permissions     │
  │ - Prior task outcomes            │
  └──────────────────────────────────┘
       │
       ▼
  CONTEXT ASSEMBLY
  (system prompt + retrieved chunks + task)
       │
       ▼
  LLM INFERENCE
  (selected model via AMIL matrix)
       │
       ▼
  OUTPUT VALIDATION
  (safety check + format check + Hermes log)
       │
       ▼
  RESULT → PR / Lesson / Trade / Doc
```

### 2.2 Embedding Models for Fabric

| Use Case | Embedding Model | Dimensions |
|---|---|---|
| Code search | `text-embedding-3-large` (OpenAI) | 3072 |
| Doc/knowledge search | `nomic-embed-text` (local, Ollama) | 768 |
| Semantic code similarity | `voyage-code-3` (Voyage AI) | 1024 |
| Multilingual docs | `multilingual-e5-large` | 1024 |

### 2.3 Vector Store Configuration

```python
# Fabric vector store setup
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

fabric_vector_store = QdrantClient(url="http://localhost:6333")

fabric_vector_store.create_collection(
    collection_name="acss_knowledge",
    vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
)
# Collections: code_chunks | docs | commit_history | on_chain_events | agent_outcomes
```

### 2.4 Brainkit Injection Protocol

Every clone agent receives a Brainkit injection at session start:

```
TIER 1 BRAINKIT (always injected):
  - Repository purpose and architecture (copilot-instructions.md)
  - Clone identity and permissions
  - Active task description

TIER 2 BRAINKIT (injected for complex tasks):
  + Recent commit history (last 20 commits)
  + Relevant CCSLL / CBSLL / CSEL environment profile
  + Similar past task outcomes from Fabric

TIER 3 BRAINKIT (injected for architectural decisions):
  + Full cross-repo dependency map
  + ACSS agent upgrade manifest (agent_type + current tier)
  + Human gate requirements for this task type
```

---

## 3. Fine-Tuning Protocols

### 3.1 When to Fine-Tune

| Scenario | Action |
|---|---|
| General task performance is good | Use RAG + Brainkit. Do NOT fine-tune. |
| Model consistently misses lippytm.ai voice/style | Fine-tune on Canon and Encyclopedia examples |
| Model makes recurring errors on specific language/framework | Fine-tune on CCSLL/CBSLL corrections dataset |
| Teaching agent explanations rated poorly by learners | Fine-tune on high-rated explanation pairs |
| Trading agent signal model underperforms | Fine-tune time-series model on new market data |

### 3.2 Fine-Tuning Dataset Structure

```jsonl
{"messages": [
  {"role": "system", "content": "You are lippytmai, teaching Solidity smart contracts in the Earn-while-you-Learn style. Be educational, use analogies, and always link to the next concept."},
  {"role": "user", "content": "Explain what a mapping is in Solidity."},
  {"role": "assistant", "content": "A mapping in Solidity is like a dictionary in Python or an object in JavaScript — it stores key-value pairs on the blockchain. Unlike a regular database, you can't iterate over it or get its size; you can only look up a value by its exact key. Think of it as a vault with infinite numbered slots — you can store or retrieve from any slot instantly, but you can't count the slots or browse them.\n\n```solidity\nmapping(address => uint256) public balances;\nbalances[msg.sender] = 100; // store\nuint256 myBalance = balances[msg.sender]; // retrieve\n```\n\nNext concept → [Learn about events and why they are the blockchain's logging system](docs/cbsll-events.md)."}
]}
```

### 3.3 Fine-Tuning Infrastructure

| Step | Tool |
|---|---|
| Dataset curation | Human review + automated quality filter (perplexity score) |
| Training (OpenAI models) | OpenAI fine-tuning API (`gpt-4o-mini` → `gpt-4o`) |
| Training (open models) | Axolotl or Unsloth on GPU (NVIDIA A100 / H100) |
| Evaluation | RAGAS, custom benchmark suite, human review panel |
| Deployment | Ollama (local), vLLM (server), OpenAI fine-tuned endpoint |
| Version control | Model weights hashed and referenced in Fabric; old weights archived |

---

## 4. Model Evaluation Framework

### 4.1 Evaluation Dimensions

| Dimension | Metric | Target |
|---|---|---|
| **Correctness** | % outputs verified correct by tests / human review | > 90% |
| **Relevance** | RAGAS context relevance score | > 0.80 |
| **Safety** | % outputs passing safety classifier | 100% |
| **Style Consistency** | lippytm.ai voice match score (human panel, 1-5) | > 4.0 |
| **Latency** | p95 response time for task type | < 8s interactive, < 60s batch |
| **Cost Efficiency** | Cost per accepted output (tokens × price ÷ acceptance rate) | Minimize |

### 4.2 Automated Evaluation Pipeline

```python
# AMIL evaluation pipeline — runs on every 100 agent task completions
def evaluate_model_batch(model_id: str, task_type: str, batch_size: int = 100):
    results = fabric.query("agent_outcomes", filters={
        "model_id": model_id,
        "task_type": task_type,
        "limit": batch_size
    })
    
    metrics = {
        "correctness": compute_correctness(results),
        "relevance": compute_ragas_relevance(results),
        "safety_pass_rate": compute_safety(results),
        "style_score": compute_style_match(results),
        "p95_latency_ms": compute_latency_p95(results),
        "cost_per_accepted": compute_cost_efficiency(results)
    }
    
    fabric.write("model_scoreboard", model_id=model_id, task_type=task_type, **metrics)
    
    if metrics["correctness"] < 0.85 or metrics["safety_pass_rate"] < 1.0:
        hermes.emit("model.performance_alert", model_id=model_id, metrics=metrics)
    
    return metrics
```

### 4.3 Model Swap Protocol

When evaluation signals that a model is underperforming:

1. **Hermes emits** `model.swap_candidate` event
2. **Fabric** selects the next-best model from the scoreboard
3. **Shadow deployment** — new model runs in parallel for 48 hours, outputs compared
4. **Charles reviews** A/B comparison dashboard
5. **Approved swap** — Hermes updates all clone routing tables
6. **Old model** archived with performance log

---

## 5. Prompt Engineering Standards

### 5.1 The ACSS Prompt Architecture

Every prompt sent by a clone agent follows a five-layer structure:

```
LAYER 1: IDENTITY
"You are [clone_id] — [role description]. You operate within [repo/project context]."

LAYER 2: TASK
"Your task is: [specific, measurable action]."

LAYER 3: CONTEXT
"Relevant context: [RAG-retrieved chunks from Fabric]"

LAYER 4: CONSTRAINTS
"Constraints: [identity permissions, output format, safety rules, word limit]"

LAYER 5: OUTPUT FORMAT
"Respond with: [JSON schema / markdown format / code block spec]"
```

### 5.2 Prompt Quality Checklist

Before a prompt template is registered in Fabric:

- [ ] Identity layer specifies clone_id and repo context
- [ ] Task layer uses a verb + measurable outcome (not "help with" — use "generate", "review", "explain")
- [ ] Context layer pulls from Fabric, not static text
- [ ] Constraints layer includes format spec and max length
- [ ] Output format includes at least one concrete example
- [ ] Tested on 10 diverse inputs; pass rate ≥ 90%
- [ ] Human-reviewed by lippytm or Charles before production registration

### 5.3 Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|---|---|---|
| "Write good code" | Vague, unmeasurable | "Write a Python function that [specific behavior], with type hints, docstring, and unit test" |
| Pasting entire files as context | Exceeds context window; dilutes signal | Use Fabric RAG to retrieve only relevant chunks |
| No output format spec | Unpredictable response structure | Always include JSON schema or markdown template |
| Assuming model remembers prior tasks | Stateless inference; Fabric is the memory | Always inject relevant history from Fabric |
| One prompt for all task types | Each task type needs tuned instructions | Use AMIL task-type routing to select prompt template |

---

## 6. Multi-Model Pipelines

### 6.1 Ensemble Patterns

For high-stakes tasks (architecture decisions, security reviews, smart contract audits), the ACSS uses **multi-model ensemble** pipelines:

```
TASK INPUT
    │
    ├──► Model A (Claude 4)         ─┐
    ├──► Model B (GPT-4o)           ─┼──► CONSENSUS ENGINE ──► FINAL OUTPUT
    └──► Model C (DeepSeek Coder)   ─┘    (majority vote OR
                                          human review if
                                          disagreement > 30%)
```

### 6.2 Chain-of-Thought Pipelines

For complex reasoning tasks:

```python
# Multi-step reasoning pipeline
pipeline = [
    {"step": "decompose", "model": "claude-4", "prompt_template": "decompose_task"},
    {"step": "research",  "model": "gemini-2-pro", "prompt_template": "research_context"},
    {"step": "implement", "model": "gpt-4o",       "prompt_template": "implement_solution"},
    {"step": "review",    "model": "deepseek-coder","prompt_template": "security_review"},
    {"step": "format",    "model": "gpt-4o-mini",  "prompt_template": "format_output"},
]
# Each step's output becomes next step's context, logged to Fabric at each checkpoint
```

### 6.3 Agent Collaboration Patterns

| Pattern | When to Use | Models Involved |
|---|---|---|
| **Researcher + Writer** | Long-form docs, curriculum | Gemini (research) → Claude (write) |
| **Coder + Reviewer** | Critical code changes | GPT-4o (code) → DeepSeek (review) |
| **Brainstormer + Filter** | Creative/Canon work | GPT-4o (generate 10) → Claude (select + refine) |
| **Planner + Executor** | Multi-step tasks | Claude (plan) → aider/lippytm clone (execute) |
| **Translator + Validator** | On-chain data → human insight | Custom (parse) → GPT-4o (explain) → human (verify) |

---

## 7. Model Governance and Safety

| Principle | Protocol |
|---|---|
| **No model accesses production secrets** | All model calls routed through Hermes; secrets injected at infra level, never in prompts |
| **No model writes to production without human gate** | Model outputs → PR / draft → human review → merge |
| **Model outputs are logged, not assumed correct** | Every significant output stored in Fabric with model_id, timestamp, and task_id |
| **Fine-tune data is curated, not auto-scraped** | All training data reviewed by human panel before use |
| **Model costs are tracked per clone and per task** | Hermes logs token usage; Fabric computes cost-per-outcome for budget optimization |
| **No model can change its own Brainkit** | Brainkit updates proposed by agent, approved and committed by human |

---

## Further Reading

- 📄 [`docs/ai-agents-upgrade-manifest.md`](ai-agents-upgrade-manifest.md) — Agent tier definitions and upgrade paths
- 📄 [`docs/ai-clone-engine-swarms.md`](ai-clone-engine-swarms.md) — ACSS full architecture
- 📄 [`docs/ai-brainkits.md`](ai-brainkits.md) — Copilot Brainkit design and agent memory
- 📄 [`docs/ai-trading-bots-intelligence.md`](ai-trading-bots-intelligence.md) — Trading agent ML architecture
- 📄 [`docs/self-improvement.md`](self-improvement.md) — Evolutionary learning and AI self-improvement
- 🏠 [`README.md`](../README.md) — Encyclopedia home

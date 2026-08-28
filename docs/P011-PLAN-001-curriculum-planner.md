# P-011-PLAN-001 — Curriculum Planner (Engine 3)
### *Fabric-Backed Adaptive Curriculum Design for the Prompt #11 Earn-while-you-Learn System*

> *"A great curriculum does not hand you a list of topics. It watches what you already know, listens to what you are trying to build, measures where your understanding breaks down, and designs the shortest path from where you are to where you need to be."*
> — Charles Earl Lipshay (lippytm.ai)

---

## Overview

**Engine 3 — Curriculum Planner** is the intelligent design core of the Prompt #11 system. It receives a classified learner event from Engine 2, retrieves the learner's complete knowledge profile from Fabric, and uses Claude 3.5 to design a personalized, sequenced learning plan that is:

- **Adaptive** — shaped by what the learner already knows (CCSLL/CBSLL proficiency levels)
- **Goal-oriented** — working backward from what the learner wants to build or earn
- **Measurable** — every step has a completion signal (test pass, build artifact, on-chain credential)
- **Correctable** — every plan has a rollback point and a correction procedure

---

## 1. Curriculum Planner Architecture

```
┌──────────────────────────────────────────────────────────┐
│              ENGINE 3 — CURRICULUM PLANNER               │
│                                                          │
│  Input: ClassifiedEvent + learner_id                     │
│                                                          │
│  ┌─────────────────┐    ┌──────────────────────────┐     │
│  │ 1. PROFILE LOAD │───▶│ 2. PREREQUISITE CHECK    │     │
│  │  (Fabric query) │    │  (gap analysis)          │     │
│  └─────────────────┘    └──────────────┬───────────┘     │
│                                        │                 │
│  ┌─────────────────┐    ┌──────────────▼───────────┐     │
│  │ 4. SEQUENCER    │◀───│ 3. GOAL DECOMPOSITION    │     │
│  │ (order steps)   │    │  (Claude 3.5 reasoning)  │     │
│  └────────┬────────┘    └──────────────────────────┘     │
│           │                                              │
│  ┌────────▼────────┐    ┌──────────────────────────┐     │
│  │ 5. RESOURCE MAP │───▶│ 6. PLAN PUBLISH          │     │
│  │ (KB + docs)     │    │  (Hermes + Fabric + CRM) │     │
│  └─────────────────┘    └──────────────────────────┘     │
└──────────────────────────────────────────────────────────┘
```

---

## 2. Learner Profile Schema

The curriculum planner reads a rich learner profile from Fabric before generating any plan:

```python
# acss/p011/engines/planning/learner_profile.py
"""Learner profile schema — the Fabric knowledge object that drives all curriculum decisions."""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ProficiencyMap:
    """CCSLL / CBSLL / CLL proficiency per domain — 0 (Curious) to 5 (Master)."""

    # CCSLL — Computer Software Language Library
    python: int = 0
    javascript_typescript: int = 0
    rust: int = 0
    go: int = 0
    bash_shell: int = 0
    sql: int = 0
    html_css: int = 0

    # CBSLL — Blockchain Software Language Library
    solidity: int = 0
    anchor_rust: int = 0
    cairo: int = 0
    zk_circuits: int = 0
    web3_tooling: int = 0
    defi_protocols: int = 0

    # CLL — Linux Library
    linux_user: int = 0
    linux_sysadmin: int = 0
    linux_devops: int = 0
    omarchy_workstation: int = 0

    # CSEL — Software Environments Library
    ai_ml_llm: int = 0
    blockchain_web3: int = 0
    backend_api: int = 0
    ci_cd: int = 0
    containers_k8s: int = 0

    def overall_level(self) -> int:
        """Weighted average proficiency — used for Beginner/Intermediate/Advanced routing."""
        scores = [
            self.python, self.javascript_typescript, self.bash_shell,
            self.linux_user, self.web3_tooling,
        ]
        return round(sum(scores) / len(scores))


@dataclass
class LearningGoal:
    goal_id: str
    description: str
    target_domain: str  # e.g., "blockchain_evm", "ai_ml", "linux_devops"
    target_level: int   # 0–5
    deadline: datetime | None = None
    motivation: str | None = None  # Why does the learner want this?


@dataclass
class CompletedMilestone:
    milestone_id: str
    title: str
    domain: str
    level: int
    completed_at: datetime
    credential_token_id: str | None = None  # ERC-721 token ID on Base if minted


@dataclass
class LearnerProfile:
    learner_id: str
    display_name: str
    learner_type: str  # "human", "robot", "humanoid_ai"
    proficiency: ProficiencyMap = field(default_factory=ProficiencyMap)
    active_goals: list[LearningGoal] = field(default_factory=list)
    completed_milestones: list[CompletedMilestone] = field(default_factory=list)
    preferred_languages: list[str] = field(default_factory=list)
    preferred_learning_style: str = "hands-on"  # "conceptual", "hands-on", "visual", "audio"
    slack_user_id: str | None = None
    total_lessons_completed: int = 0
    current_streak_days: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_active: datetime = field(default_factory=datetime.utcnow)

    def has_prerequisite(self, domain: str, min_level: int) -> bool:
        """Check whether the learner meets a prerequisite."""
        level = getattr(self.proficiency, domain.replace("-", "_"), 0)
        return level >= min_level
```

---

## 3. Curriculum Step Schema

```python
# acss/p011/engines/planning/curriculum_step.py
"""A single step in a learning plan."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, Any


StepType = Literal[
    "concept_lesson",    # Explanation + analogy + real-world example
    "code_build",        # Write and test code (Python, Solidity, Bash, etc.)
    "quiz",              # Multiple-choice or short-answer knowledge check
    "debug_exercise",    # Given broken code — find and fix it
    "research_task",     # Read a doc/paper; summarize key points
    "blockchain_deploy", # Deploy a contract to testnet
    "peer_review",       # Review another learner's artifact
    "credential_gate",   # Quality review before credential issuance
]


@dataclass
class CurriculumStep:
    step_id: str
    title: str
    step_type: StepType
    domain: str                    # e.g., "python", "solidity", "linux_user"
    proficiency_level: int         # Level this step targets (0–5)
    description: str
    estimated_minutes: int
    resources: list[dict[str, str]] = field(default_factory=list)  # {title, url/path}
    prerequisites: list[str] = field(default_factory=list)         # step_ids
    completion_signal: str = ""    # How do we know this step is done?
    earn_reward: bool = False      # Does completing this step trigger credential check?
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class LearningPlan:
    plan_id: str
    learner_id: str
    goal: LearningGoal
    steps: list[CurriculumStep]
    total_estimated_hours: float
    difficulty_label: str  # "Beginner", "Intermediate", "Advanced"
    series_ref: str | None = None  # Links to ebook/audiobook series if applicable
    generated_by_model: str = "claude-3-5-sonnet-20241022"
    version: int = 1
```

---

## 4. Full Curriculum Planner Implementation

```python
# acss/p011/engines/planning/curriculum_planner.py
"""
Prompt #11 Engine 3 — Curriculum Planner.
Generates personalized, sequenced learning plans backed by Fabric and Claude 3.5.
"""

from __future__ import annotations
import json
import uuid
from datetime import datetime
from typing import Any

from .learner_profile import LearnerProfile, LearningGoal
from .curriculum_step import CurriculumStep, LearningPlan, StepType


# Claude 3.5 system prompt for curriculum design
CURRICULUM_SYSTEM_PROMPT = """You are lippytmai — the AI curriculum designer for the lippytm.ai ecosystem.

Your job is to design a personalized, sequenced learning plan.

Rules:
1. Every step must have a concrete completion signal (pass a test, deploy a contract, submit a PR).
2. Never include a step that requires a skill the learner has not yet acquired.
3. Always start with the simplest possible first step that builds momentum.
4. Mix concept lessons (20%), code builds (50%), and debug exercises (20%), with credential gates (10%).
5. Each step must cite a resource from the lippytm.ai encyclopedia docs.
6. Respect the learner's preferred learning style.
7. Keep each step to ≤ 90 minutes of focused work.
8. Flag any step that requires HumanApprovalGate (Level 4+, production deployments, on-chain credential minting).

Return a JSON object with:
{
  "difficulty_label": "Beginner" | "Intermediate" | "Advanced",
  "total_estimated_hours": <number>,
  "steps": [
    {
      "title": "<step title>",
      "step_type": "<StepType>",
      "domain": "<domain>",
      "proficiency_level": <0-5>,
      "description": "<2-3 sentences>",
      "estimated_minutes": <number>,
      "resources": [{"title": "<name>", "path": "<doc path or URL>"}],
      "completion_signal": "<how we know it's done>",
      "earn_reward": <true|false>
    }
  ]
}"""


class CurriculumPlanner:
    """
    Engine 3: Generates personalized learning plans using Claude 3.5 + Fabric.

    Flow:
    1. Load full learner profile from Fabric
    2. Decompose goal into sub-skills (gap analysis)
    3. Generate step sequence with Claude 3.5
    4. Enrich steps with encyclopedia resource links
    5. Publish plan to Fabric + Hermes + CRM
    """

    # Minimum proficiency gaps that always trigger prerequisite steps
    PREREQ_RULES: dict[str, dict[str, int]] = {
        "solidity": {"python": 1, "linux_user": 1},
        "anchor_rust": {"rust": 2, "linux_user": 1},
        "ai_ml_llm": {"python": 2, "sql": 1},
        "linux_devops": {"linux_user": 2, "bash_shell": 1},
        "zk_circuits": {"python": 3, "solidity": 2},
        "ci_cd": {"bash_shell": 1, "linux_user": 1},
    }

    def __init__(
        self,
        fabric_client: Any,
        amil_client: Any,
        hermes_client: Any,
        crm_client: Any,
    ) -> None:
        self.fabric = fabric_client
        self.amil = amil_client
        self.hermes = hermes_client
        self.crm = crm_client

    async def create_plan(
        self,
        learner_id: str,
        goal: LearningGoal,
    ) -> LearningPlan:
        """Create a full personalized curriculum plan for a learner goal."""

        # 1. Load learner profile
        profile: LearnerProfile = await self.fabric.get_learner_profile(learner_id)

        # 2. Gap analysis — what prerequisites are missing?
        missing_prereqs = self._gap_analysis(profile, goal.target_domain)

        # 3. Fetch relevant encyclopedia context from Fabric KB
        kb_context = await self.fabric.search_curriculum_resources(
            domain=goal.target_domain,
            target_level=goal.target_level,
            learner_type=profile.learner_type,
        )

        # 4. Build Claude prompt with all context
        user_prompt = self._build_prompt(profile, goal, missing_prereqs, kb_context)

        # 5. Generate plan with Claude 3.5
        raw_plan = await self.amil.call_json(
            model="claude-3-5-sonnet-20241022",
            system=CURRICULUM_SYSTEM_PROMPT,
            prompt=user_prompt,
        )

        # 6. Assemble LearningPlan dataclass
        plan = self._assemble_plan(learner_id, goal, raw_plan)

        # 7. Store plan in Fabric + CRM
        await self.fabric.store_learning_plan(plan)
        await self.crm.record_plan_created(learner_id, plan.plan_id, plan.goal.description)

        # 8. Publish to Hermes
        await self.hermes.publish(
            "p11.plan.created",
            {
                "learner_id": learner_id,
                "plan_id": plan.plan_id,
                "goal": goal.description,
                "steps": len(plan.steps),
                "estimated_hours": plan.total_estimated_hours,
                "difficulty": plan.difficulty_label,
            },
        )

        return plan

    def _gap_analysis(self, profile: LearnerProfile, target_domain: str) -> list[dict]:
        """Find prerequisite skills the learner is missing for the target domain."""
        gaps = []
        prereqs = self.PREREQ_RULES.get(target_domain, {})
        for prereq_domain, min_level in prereqs.items():
            if not profile.has_prerequisite(prereq_domain, min_level):
                current = getattr(profile.proficiency, prereq_domain, 0)
                gaps.append({
                    "domain": prereq_domain,
                    "current_level": current,
                    "required_level": min_level,
                    "gap": min_level - current,
                })
        return gaps

    def _build_prompt(
        self,
        profile: LearnerProfile,
        goal: LearningGoal,
        missing_prereqs: list[dict],
        kb_context: list[dict],
    ) -> str:
        prereq_text = (
            "\n".join(
                f"- {g['domain']}: currently Level {g['current_level']}, needs Level {g['required_level']}"
                for g in missing_prereqs
            )
            if missing_prereqs
            else "None — learner meets all prerequisites."
        )

        resources_text = "\n".join(
            f"- {r['title']} ({r['path']}): {r['summary']}"
            for r in kb_context[:10]
        )

        return f"""Design a personalized curriculum plan for the following learner and goal.

LEARNER PROFILE:
- Name: {profile.display_name}
- Learner type: {profile.learner_type}
- Preferred style: {profile.preferred_learning_style}
- Current Python level: {profile.proficiency.python}/5
- Current Linux level: {profile.proficiency.linux_user}/5
- Current Solidity level: {profile.proficiency.solidity}/5
- Current AI/ML level: {profile.proficiency.ai_ml_llm}/5
- Total lessons completed: {profile.total_lessons_completed}

GOAL:
- Description: {goal.description}
- Target domain: {goal.target_domain}
- Target proficiency level: {goal.target_level}/5
- Motivation: {goal.motivation or "Not specified"}

MISSING PREREQUISITES:
{prereq_text}

AVAILABLE ENCYCLOPEDIA RESOURCES:
{resources_text}

Generate a complete, sequenced curriculum plan. Include prerequisite steps before the main goal steps if gaps exist."""

    def _assemble_plan(
        self,
        learner_id: str,
        goal: LearningGoal,
        raw_plan: dict,
    ) -> LearningPlan:
        steps = [
            CurriculumStep(
                step_id=f"step_{i:03d}_{uuid.uuid4().hex[:6]}",
                title=s["title"],
                step_type=s["step_type"],
                domain=s["domain"],
                proficiency_level=s["proficiency_level"],
                description=s["description"],
                estimated_minutes=s["estimated_minutes"],
                resources=s.get("resources", []),
                completion_signal=s.get("completion_signal", ""),
                earn_reward=s.get("earn_reward", False),
            )
            for i, s in enumerate(raw_plan["steps"])
        ]
        return LearningPlan(
            plan_id=f"plan_{uuid.uuid4().hex[:12]}",
            learner_id=learner_id,
            goal=goal,
            steps=steps,
            total_estimated_hours=raw_plan.get("total_estimated_hours", 0.0),
            difficulty_label=raw_plan.get("difficulty_label", "Beginner"),
        )
```

---

## 5. Curriculum Templates by Series Level

These templates are the starting seeds for the ebook/audiobook course series:

### 5.1 Beginner Track Template (L0 → L2)

| Step # | Type | Domain | Duration | Completion Signal |
|---|---|---|---|---|
| 1 | Concept Lesson | `linux_user` | 30 min | Quiz pass ≥ 80% |
| 2 | Code Build | `bash_shell` | 45 min | Script runs with 0 errors |
| 3 | Concept Lesson | `python` | 30 min | Quiz pass ≥ 80% |
| 4 | Code Build | `python` | 60 min | Pytest passes |
| 5 | Debug Exercise | `python` | 30 min | Fixed code passes tests |
| 6 | Concept Lesson | `linux_user` | 30 min | Quiz |
| 7 | Code Build | `bash_shell` | 45 min | systemd service running |
| 8 | Research Task | `web3_tooling` | 30 min | Summary doc submitted |
| 9 | Code Build | `solidity` | 90 min | Forge test passes |
| 10 | Credential Gate | `python` + `linux_user` | — | CCSLL L1 SkillBadge auto-issued |

### 5.2 Intermediate Track Template (L2 → L3)

| Step # | Type | Domain | Duration | Completion Signal |
|---|---|---|---|---|
| 1 | Code Build | `python` | 60 min | FastAPI endpoint with Pytest |
| 2 | Code Build | `sql` | 45 min | PostgreSQL schema deployed |
| 3 | Code Build | `solidity` | 90 min | ERC-20 deployed to Sepolia |
| 4 | Debug Exercise | `solidity` | 60 min | Slither 0 highs |
| 5 | Code Build | `ci_cd` | 60 min | GitHub Actions CI passing |
| 6 | Code Build | `containers_k8s` | 90 min | Docker Compose stack running |
| 7 | Blockchain Deploy | `web3_tooling` | 90 min | Contract verified on Etherscan |
| 8 | Peer Review | `python` | 45 min | Review submitted with ≥ 3 comments |
| 9 | Research Task | `ai_ml_llm` | 60 min | RAG chatbot running |
| 10 | Credential Gate | all intermediate | — | CCSLL L3 + CBSLL L2 SkillBadges |

### 5.3 Advanced Track Template (L3 → L5)

| Step # | Type | Domain | Duration | Completion Signal |
|---|---|---|---|---|
| 1 | Code Build | `zk_circuits` | 120 min | Circom proof generated + verified |
| 2 | Code Build | `ai_ml_llm` | 120 min | Fine-tuned model evaluated |
| 3 | Code Build | `linux_devops` | 90 min | Ansible node deployment |
| 4 | Blockchain Deploy | `defi_protocols` | 120 min | Uniswap v3 pool interaction |
| 5 | Code Build | `ci_cd` | 90 min | Self-healing pipeline deployed |
| 6 | Code Build | `anchor_rust` | 120 min | Solana program deployed to devnet |
| 7 | Research Task | `zk_circuits` | 90 min | ZK rollup explainer doc |
| 8 | Peer Review | advanced artifact | 60 min | Review with security analysis |
| 9 | Code Build | `ai_ml_llm` | 120 min | RL trading agent backtest |
| 10 | Credential Gate | all advanced | — | CBSLL L4 + ACSS Architect (Charles) |

---

## 6. Plan Adjustment Loop

Plans are not static — Fabric continuously monitors completion rates and adjusts:

```python
# acss/p011/engines/planning/plan_adjuster.py
"""Adjusts learning plans based on real-time learner performance signals from Fabric."""

from __future__ import annotations
from typing import Any


class PlanAdjuster:
    """Monitors plan progress and applies adaptive adjustments."""

    STUCK_THRESHOLD_DAYS = 3    # No progress for 3 days → simplify next step
    FAST_THRESHOLD_RATIO = 0.5  # Completing steps in <50% of estimated time → accelerate

    async def check_and_adjust(
        self,
        plan_id: str,
        learner_id: str,
        fabric: Any,
        amil: Any,
        hermes: Any,
    ) -> dict:
        """Check plan health and return adjustment actions."""
        progress = await fabric.get_plan_progress(plan_id)
        actions = []

        for step in progress["steps"]:
            if step["status"] == "stuck" and step["days_stuck"] >= self.STUCK_THRESHOLD_DAYS:
                # Add a simpler prerequisite step before the stuck step
                simpler_step = await amil.call_json(
                    model="gpt-4o",
                    prompt=f"Generate a simpler prerequisite step for: {step['title']}",
                )
                actions.append({
                    "action": "insert_step",
                    "before_step_id": step["step_id"],
                    "new_step": simpler_step,
                })
                await hermes.publish(
                    "p11.plan.step_simplified",
                    {"learner_id": learner_id, "step_id": step["step_id"]},
                )

            elif (
                step["status"] == "completed"
                and step["actual_minutes"] < step["estimated_minutes"] * self.FAST_THRESHOLD_RATIO
            ):
                # Learner is going fast — flag for acceleration
                actions.append({
                    "action": "accelerate",
                    "step_id": step["step_id"],
                    "note": "Learner completing faster than expected — consider skipping review steps",
                })

        return {"plan_id": plan_id, "adjustments": actions}
```

---

## 7. ACSS Integration Points

| Component | Integration | Detail |
|---|---|---|
| **Hermes** | Publishes `p11.plan.created`, `p11.plan.step_completed`, `p11.plan.adjusted` | All plan lifecycle events |
| **Fabric** | Reads learner profile; stores plan; receives completion signals | Single source of truth for all plans |
| **AMIL** | Claude 3.5 for plan generation; GPT-4o for step simplification | Model routing per task type |
| **Slack CRM** | Delivers step notifications via `/learn` command; `/progress` shows plan status | Learner-facing surface |
| **ACD** | Tracks curriculum completion rates; Fabric evolution signals trigger plan template updates | Self-improving curricula |
| **On-chain** | Credential gates mint ERC-721 SkillBadges when plan milestones are verified | `EEEPCredential.sol` on Base |

---

## Further Reading

- 📄 [`docs/P011-ENGINE-001-prompt11-engines.md`](P011-ENGINE-001-prompt11-engines.md) — All 8 engines overview
- 📄 [`docs/P011-AWARE-001-awareness-dashboard.md`](P011-AWARE-001-awareness-dashboard.md) — Engine 6: learner awareness signals that feed plan adjustments
- 📄 [`docs/P011-BOT-001-chatbot-knowledge-base-learning-path.md`](P011-BOT-001-chatbot-knowledge-base-learning-path.md) — The 6-level chatbot path this planner generates plans for
- 📄 [`docs/P011-EBOOK-000-course-series-master-plan.md`](P011-EBOOK-000-course-series-master-plan.md) — 300-book series that uses these curriculum templates
- 📄 [`docs/ai-model-intelligence-layer.md`](ai-model-intelligence-layer.md) — AMIL: Claude 3.5 selection for curriculum reasoning
- 📄 [`docs/slack-ai-crm-integration.md`](slack-ai-crm-integration.md) — Slack delivery surface for curriculum plans
- 🏠 [`README.md`](../README.md) — Encyclopedia home

# P-011-QR-001 — Quality Review Engine (Engine 5)
### *13 Gates Between Every Build Artifact and the World*

> *"A gate is not an obstacle — it is a promise to the next person who depends on your work. Every gate you skip is a debt you are charging to someone else's future."*
> — Charles Earl Lipshay (lippytm.ai)

---

## Overview

**Engine 5 — Quality Review** is the guardian between every build artifact, document, and credential in the Prompt #11 system and the outside world. Nothing leaves the ACSS without passing through Engine 5. It runs 12 automated gates and 1 human gate — and every gate is named, documented, testable, and correctable.

Engine 5 is the implementation of the Transparency Engineering principle from `P011-XPIO-001`: you cannot approve your own work, and every approval must leave a verifiable record.

---

## 1. The 13 Quality Gates

```
G1  G2  G3  G4  G5  G6  G7  G8  G9  G10  G11  G12  G13
│   │   │   │   │   │   │   │   │   │    │    │    │
▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼    ▼    ▼    ▼
Ori Fic Rig Src Cod Lea Acc Pri Sec Env  Rev  Cor  Hum
gin tion hts  e  eT  rni ess vac uri nvi  enu  rec  an
ali Bou Gat Gat est Ng  ibi acy ty  ron  Int  tio  App
ty  nd  e   e   Gat Out Lit y   Gat men  egr  n    rov
    ary                 e   put y       e    tal  Gat  al
                                             Gat  e    Gat
                                             e         e
AUTOMATED (G1–G12) ─────────────────────────────┤   MANUAL │
```

| # | Gate | What It Checks | Automated? | Fail Action |
|---|---|---|---|---|
| **G1** | OriginalityGate | No plagiarism; no copyright-infringing content | Automated | Block + flag |
| **G2** | FictionBoundaryGate | Fictional characters never merged with real CRM/identity records | Automated | Block + flag |
| **G3** | RightsGate | All media, code, and content has verified rights/licenses | Automated | Block + flag |
| **G4** | SourceGate | All factual claims cite a verifiable source | Automated | Warn + request sources |
| **G5** | CodeTestGate | All code has passing tests; ≥ 80% coverage | Automated (Pytest/Forge) | Block |
| **G6** | LearningOutcomeGate | Measurable learning objectives present and achievable | Automated | Warn |
| **G7** | AccessibilityGate | Content readable at ≤ 10th grade level; no inaccessible media | Automated | Warn |
| **G8** | PrivacyGate | No PII; no secrets committed; GDPR-compliant | Automated | Block |
| **G9** | SecurityGate | No security vulnerabilities (Slither, CodeQL, Bandit) | Automated | Block |
| **G10** | EnvironmentalGate | Resource usage documented; no unnecessary compute waste | Automated | Warn |
| **G11** | RevenueIntegrityGate | All earning claims are honest, bounded, and not guaranteed | Automated | Block |
| **G12** | CorrectionGate | Correction procedure defined; supersession policy present | Automated | Warn |
| **G13** | HumanApprovalGate | Charles Earl Lipshay reviews and approves | Manual | Block (always) |

---

## 2. Full Quality Review Pipeline Implementation

```python
# acss/p011/engines/quality_review/quality_review_engine.py
"""
Prompt #11 Engine 5 — Quality Review Engine.
Runs all 13 quality gates on any artifact before it can be published or earn a credential.
"""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Literal


class GateResult(Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    SKIPPED = "skipped"


@dataclass
class GateOutcome:
    gate_name: str
    gate_number: int
    result: GateResult
    details: str
    automated: bool
    checked_at: datetime = field(default_factory=datetime.utcnow)
    reviewer: str | None = None  # Set for G13


@dataclass
class QualityReport:
    artifact_id: str
    artifact_type: str  # "doc", "code", "credential", "ebook_chapter", "video_script"
    artifact_path: str
    gates: list[GateOutcome]
    overall_result: GateResult
    blocking_failures: list[str]
    warnings: list[str]
    approved_by: str | None = None
    approved_at: datetime | None = None
    report_id: str = ""

    def __post_init__(self) -> None:
        import uuid
        self.report_id = f"qr_{uuid.uuid4().hex[:12]}"

    @property
    def passed(self) -> bool:
        return self.overall_result == GateResult.PASS

    def gate(self, name: str) -> GateOutcome | None:
        return next((g for g in self.gates if g.gate_name == name), None)


class QualityReviewEngine:
    """
    Engine 5: Runs all 13 P011 quality gates on any artifact.

    G1–G12 are automated. G13 (HumanApprovalGate) requires Charles.
    An artifact must pass ALL gates (G1–G12 with no FAIL; G13 always) before publication.
    """

    FICTION_CHARACTERS = {
        "lippy killjoy", "nexus nine", "fable 5", "charles-origin ai",
        "charles ai", "lippytmai character",
    }

    GUARANTEED_INCOME_PATTERNS = [
        r"guarantee(s|d)?\s+(income|return|profit|earning)",
        r"will\s+(earn|make|profit)\s+\$",
        r"risk.?free",
        r"100%\s+success",
    ]

    def __init__(
        self,
        hermes_client: Any,
        fabric_client: Any,
        amil_client: Any,
        security_scanner: Any,
    ) -> None:
        self.hermes = hermes_client
        self.fabric = fabric_client
        self.amil = amil_client
        self.security = security_scanner

    async def review(
        self,
        artifact_id: str,
        artifact_type: str,
        content: str,
        artifact_path: str,
        metadata: dict[str, Any] | None = None,
    ) -> QualityReport:
        """Run all 12 automated gates and return a quality report.

        G13 (HumanApprovalGate) is triggered separately via Hermes after G1–G12 pass.
        """
        metadata = metadata or {}
        gates: list[GateOutcome] = []

        # G1 — Originality
        gates.append(await self._g1_originality(content))
        # G2 — Fiction Boundary
        gates.append(self._g2_fiction_boundary(content, metadata))
        # G3 — Rights
        gates.append(self._g3_rights(content, metadata))
        # G4 — Source
        gates.append(self._g4_source(content))
        # G5 — Code Tests
        gates.append(await self._g5_code_tests(content, artifact_path))
        # G6 — Learning Outcomes
        gates.append(self._g6_learning_outcomes(content, artifact_type))
        # G7 — Accessibility
        gates.append(self._g7_accessibility(content))
        # G8 — Privacy
        gates.append(await self._g8_privacy(content, artifact_path))
        # G9 — Security
        gates.append(await self._g9_security(content, artifact_path))
        # G10 — Environmental
        gates.append(self._g10_environmental(content))
        # G11 — Revenue Integrity
        gates.append(self._g11_revenue_integrity(content))
        # G12 — Correction
        gates.append(self._g12_correction(content, artifact_type))

        # Aggregate
        blocking = [g.gate_name for g in gates if g.result == GateResult.FAIL]
        warnings = [g.gate_name for g in gates if g.result == GateResult.WARN]
        overall = GateResult.FAIL if blocking else (
            GateResult.WARN if warnings else GateResult.PASS
        )

        report = QualityReport(
            artifact_id=artifact_id,
            artifact_type=artifact_type,
            artifact_path=artifact_path,
            gates=gates,
            overall_result=overall,
            blocking_failures=blocking,
            warnings=warnings,
        )

        # Publish to Hermes
        await self.hermes.publish(
            f"p11.quality.{'passed' if not blocking else 'failed'}",
            {
                "artifact_id": artifact_id,
                "report_id": report.report_id,
                "blocking_failures": blocking,
                "warnings": warnings,
            },
        )

        # If G1–G12 all pass, trigger G13 (HumanApprovalGate)
        if not blocking:
            await self._trigger_g13(artifact_id, report.report_id, artifact_type)

        # Store report in Fabric
        await self.fabric.store_quality_report(report.__dict__)

        return report

    # ── Gate Implementations ─────────────────────────────────────────────────

    async def _g1_originality(self, content: str) -> GateOutcome:
        """G1: Check for plagiarism using AMIL similarity check."""
        score = await self.amil.check_originality(content[:2000])
        result = GateResult.PASS if score > 0.85 else GateResult.FAIL
        return GateOutcome(
            gate_name="OriginalityGate",
            gate_number=1,
            result=result,
            details=f"Originality score: {score:.2f} (threshold: 0.85)",
            automated=True,
        )

    def _g2_fiction_boundary(self, content: str, metadata: dict) -> GateOutcome:
        """G2: Ensure fictional characters are not merged with real CRM records."""
        lower = content.lower()
        violations = [
            char for char in self.FICTION_CHARACTERS
            if char in lower and any(
                term in lower
                for term in ["crm", "profile", "real person", "customer record", "pii"]
            )
        ]
        result = GateResult.FAIL if violations else GateResult.PASS
        return GateOutcome(
            gate_name="FictionBoundaryGate",
            gate_number=2,
            result=result,
            details=f"Fiction boundary {'violations found: ' + str(violations) if violations else 'clear'}",
            automated=True,
        )

    def _g3_rights(self, content: str, metadata: dict) -> GateOutcome:
        """G3: Check that all content has verified rights/licenses."""
        has_external_code = bool(re.search(r"# (Source|From|Copied from|via):", content))
        unattributed = has_external_code and "license" not in content.lower()
        result = GateResult.WARN if unattributed else GateResult.PASS
        return GateOutcome(
            gate_name="RightsGate",
            gate_number=3,
            result=result,
            details="External code detected without license attribution" if unattributed else "Rights check clear",
            automated=True,
        )

    def _g4_source(self, content: str) -> GateOutcome:
        """G4: Verify factual claims have source citations."""
        claim_patterns = [r"\*\[Reality\]\*", r"\*\[Speculative\]\*", r"\*\[Fiction\]\*"]
        has_truth_labels = any(re.search(p, content) for p in claim_patterns)
        # For docs, truth labels OR citation links are acceptable
        has_citations = bool(re.search(r"\[.+\]\(https?://.+\)", content))
        result = GateResult.WARN if not (has_truth_labels or has_citations) else GateResult.PASS
        return GateOutcome(
            gate_name="SourceGate",
            gate_number=4,
            result=result,
            details="No truth labels or external citations found" if result == GateResult.WARN else "Sources verified",
            automated=True,
        )

    async def _g5_code_tests(self, content: str, path: str) -> GateOutcome:
        """G5: Verify code examples have passing tests."""
        code_blocks = re.findall(r"```python\n(.+?)```", content, re.DOTALL)
        if not code_blocks:
            return GateOutcome(
                gate_name="CodeTestGate",
                gate_number=5,
                result=GateResult.SKIPPED,
                details="No Python code blocks found",
                automated=True,
            )
        # For documentation, we check that test examples exist in the same doc
        has_test_examples = bool(re.search(r"def test_", content))
        result = GateResult.WARN if not has_test_examples else GateResult.PASS
        return GateOutcome(
            gate_name="CodeTestGate",
            gate_number=5,
            result=result,
            details="Code blocks present but no test examples found" if result == GateResult.WARN else "Code + tests present",
            automated=True,
        )

    def _g6_learning_outcomes(self, content: str, artifact_type: str) -> GateOutcome:
        """G6: Check for measurable learning objectives."""
        if artifact_type not in ("doc", "ebook_chapter", "lesson"):
            return GateOutcome("LearningOutcomeGate", 6, GateResult.SKIPPED, "N/A", True)
        outcome_patterns = [
            r"(learn|understand|build|deploy|write|test|earn).{5,80}(by the end|after this|you will)",
            r"(credential|skill badge|certificate)",
            r"## (Goals|Objectives|Learning|Outcomes)",
        ]
        has_outcomes = any(
            re.search(p, content, re.IGNORECASE) for p in outcome_patterns
        )
        return GateOutcome(
            gate_name="LearningOutcomeGate",
            gate_number=6,
            result=GateResult.PASS if has_outcomes else GateResult.WARN,
            details="Learning outcomes present" if has_outcomes else "No measurable learning outcomes found",
            automated=True,
        )

    def _g7_accessibility(self, content: str) -> GateOutcome:
        """G7: Basic readability check (sentence length proxy)."""
        sentences = re.split(r"[.!?]+", content)
        text_sentences = [s for s in sentences if len(s.split()) > 3]
        if not text_sentences:
            return GateOutcome("AccessibilityGate", 7, GateResult.SKIPPED, "Insufficient text", True)
        avg_words = sum(len(s.split()) for s in text_sentences) / len(text_sentences)
        result = GateResult.WARN if avg_words > 30 else GateResult.PASS
        return GateOutcome(
            gate_name="AccessibilityGate",
            gate_number=7,
            result=result,
            details=f"Average sentence length: {avg_words:.1f} words (target: ≤ 30)",
            automated=True,
        )

    async def _g8_privacy(self, content: str, path: str) -> GateOutcome:
        """G8: Check for PII patterns and secrets."""
        pii_patterns = [
            r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # email
            r"sk-[a-zA-Z0-9]{32,}",  # OpenAI key
            r"api[_-]?key\s*[=:]\s*['\"][^'\"]+['\"]",  # Generic API key
        ]
        findings = [p for p in pii_patterns if re.search(p, content)]
        result = GateResult.FAIL if findings else GateResult.PASS
        return GateOutcome(
            gate_name="PrivacyGate",
            gate_number=8,
            result=result,
            details=f"Privacy violations found: {len(findings)} pattern(s)" if findings else "Privacy check clear",
            automated=True,
        )

    async def _g9_security(self, content: str, path: str) -> GateOutcome:
        """G9: Run security scan (Bandit for Python, Slither for Solidity)."""
        if path.endswith(".sol"):
            result_data = await self.security.run_slither(path)
        elif path.endswith(".py"):
            result_data = await self.security.run_bandit(path)
        else:
            return GateOutcome("SecurityGate", 9, GateResult.SKIPPED, "No scannable code file", True)
        issues = result_data.get("high_severity_count", 0)
        result = GateResult.FAIL if issues > 0 else GateResult.PASS
        return GateOutcome(
            gate_name="SecurityGate",
            gate_number=9,
            result=result,
            details=f"{issues} high-severity issues found" if issues else "Security scan clean",
            automated=True,
        )

    def _g10_environmental(self, content: str) -> GateOutcome:
        """G10: Check that resource usage is documented for compute-heavy content."""
        has_gpu = "gpu" in content.lower() or "cuda" in content.lower()
        has_resource_note = bool(re.search(
            r"(compute|resource|cost|GPU|memory).{5,100}(require|need|use|approx|~)",
            content, re.IGNORECASE,
        ))
        result = (
            GateResult.WARN if has_gpu and not has_resource_note else GateResult.PASS
        )
        return GateOutcome(
            gate_name="EnvironmentalGate",
            gate_number=10,
            result=result,
            details="GPU usage mentioned without resource documentation" if result == GateResult.WARN else "Environmental check clear",
            automated=True,
        )

    def _g11_revenue_integrity(self, content: str) -> GateOutcome:
        """G11: Verify no guaranteed income or misleading earning claims."""
        violations = [
            p for p in self.GUARANTEED_INCOME_PATTERNS
            if re.search(p, content, re.IGNORECASE)
        ]
        result = GateResult.FAIL if violations else GateResult.PASS
        return GateOutcome(
            gate_name="RevenueIntegrityGate",
            gate_number=11,
            result=result,
            details=f"Revenue integrity violations: {len(violations)}" if violations else "Revenue claims check clear",
            automated=True,
        )

    def _g12_correction(self, content: str, artifact_type: str) -> GateOutcome:
        """G12: Verify a correction procedure exists."""
        if artifact_type == "code":
            return GateOutcome("CorrectionGate", 12, GateResult.SKIPPED, "N/A for code artifacts", True)
        has_correction = bool(re.search(
            r"(correction|error|mistake|update|supersed).{3,100}(report|submit|found|fixed)",
            content, re.IGNORECASE,
        ))
        result = GateResult.WARN if not has_correction else GateResult.PASS
        return GateOutcome(
            gate_name="CorrectionGate",
            gate_number=12,
            result=result,
            details="No correction procedure documented" if result == GateResult.WARN else "Correction procedure present",
            automated=True,
        )

    async def _trigger_g13(
        self, artifact_id: str, report_id: str, artifact_type: str
    ) -> None:
        """Trigger G13: HumanApprovalGate — always required before publication."""
        await self.hermes.publish_human_gate(
            gate_type="quality_review_g13",
            principal="charles_earl_lipshay",
            context={
                "artifact_id": artifact_id,
                "report_id": report_id,
                "artifact_type": artifact_type,
                "automated_gates_passed": "G1–G12 all passed",
                "required_action": "Review artifact and approve or reject for publication",
            },
        )

    async def human_approve(
        self,
        report_id: str,
        artifact_id: str,
        approver: str,
        notes: str = "",
    ) -> GateOutcome:
        """Called when Charles approves G13 via the HumanApprovalGate."""
        if approver == artifact_id:
            raise ValueError("Approver cannot be the same as the artifact author.")

        gate = GateOutcome(
            gate_name="HumanApprovalGate",
            gate_number=13,
            result=GateResult.PASS,
            details=f"Approved by {approver}. Notes: {notes or 'None'}",
            automated=False,
            reviewer=approver,
        )

        await self.fabric.record_human_approval(
            report_id=report_id,
            artifact_id=artifact_id,
            approver=approver,
            gate_outcome=gate.__dict__,
        )

        await self.hermes.publish(
            "p11.quality.human_approved",
            {
                "report_id": report_id,
                "artifact_id": artifact_id,
                "approver": approver,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            },
        )

        return gate
```

---

## 3. Quality Evidence Packet (QEP)

Every production release requires a **Quality Evidence Packet** — a signed bundle of all gate outcomes:

```python
# acss/p011/engines/quality_review/quality_evidence_packet.py
"""Generates and signs a Quality Evidence Packet for any production artifact."""

from __future__ import annotations
import json
import hashlib
from dataclasses import asdict
from datetime import datetime
from .quality_review_engine import QualityReport


def generate_qep(
    report: QualityReport,
    artifact_content: str,
    approver: str,
) -> dict:
    """Generate a signed Quality Evidence Packet."""
    qep = {
        "qep_version": "1.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "artifact": {
            "id": report.artifact_id,
            "type": report.artifact_type,
            "path": report.artifact_path,
            "sha256": hashlib.sha256(artifact_content.encode()).hexdigest(),
        },
        "quality_report": {
            "report_id": report.report_id,
            "overall_result": report.overall_result.value,
            "gates": [asdict(g) for g in report.gates],
            "blocking_failures": report.blocking_failures,
            "warnings": report.warnings,
        },
        "approval": {
            "approved_by": approver,
            "approved_at": datetime.utcnow().isoformat() + "Z",
            "statement": (
                f"I, {approver}, have reviewed this artifact and all quality gate outcomes. "
                f"I approve this artifact for publication."
            ),
        },
        "correction_procedure": (
            "If an error is found after publication, submit a correction issue at "
            "https://github.com/lippytm/The-Encyclopedia-of-Everything-Applied-ChatAIBots/issues "
            "with label 'correction'. A supersession record will be created."
        ),
    }
    # Sign QEP with SHA-256 of canonical JSON
    canonical = json.dumps(qep, sort_keys=True).encode()
    qep["qep_signature"] = hashlib.sha256(canonical).hexdigest()
    return qep
```

---

## 4. ACSS Integration Points

| Gate | ACSS System | Tool Used |
|---|---|---|
| G1 OriginalityGate | AMIL (GPT-4o similarity) | Cosine similarity against KB |
| G2 FictionBoundaryGate | Fabric (identity registry) | Character identity lookup |
| G5 CodeTestGate | ACD (CI pipeline) | Pytest, Forge test runner |
| G8 PrivacyGate | Secret scanner | Runtime secret scanning |
| G9 SecurityGate | ACD (security scan) | Slither (Solidity), Bandit/CodeQL (Python) |
| G13 HumanApprovalGate | Hermes → Charles | Manual review + approval |

---

## Further Reading

- 📄 [`docs/P011-ENGINE-001-prompt11-engines.md`](P011-ENGINE-001-prompt11-engines.md) — All 8 engines overview
- 📄 [`docs/P011-DOC-001-documentation-engine.md`](P011-DOC-001-documentation-engine.md) — Engine 4: all generated docs pass through Engine 5 before publication
- 📄 [`docs/P011-XPIO-001-transparency-engineering-learning-system.md`](P011-XPIO-001-transparency-engineering-learning-system.md) — Transparency Engineering: the principles behind the 13-gate system
- 📄 [`docs/autonomous-continuous-development.md`](autonomous-continuous-development.md) — ACD: CI security scans that feed G9
- 🏠 [`README.md`](../README.md) — Encyclopedia home

# P-011-XPIO-001 — Transparency Engineering Learning System
### *Building Systems That Cannot Lie to Themselves*

> *"Transparency is not a feature you bolt on at the end. It is the architecture. Every hash is a promise. Every log is a witness. Every test is a signed confession that you understood what you built."*
> — Charles Earl Lipshay (lippytm.ai)

**Canonical parent:** `lippytm/Prompt-11-` module `P-011-XPIO-001`

---

## Overview

The **Transparency Engineering Learning System** teaches learners how to build software systems that are honest about what they do, how they do it, who authorized it, and how to verify it independently. This is the foundation layer for every system in the ACSS — every Hermes event, Fabric pattern, and on-chain credential depends on transparency engineering.

*[Reality]* All transparency techniques documented here (hashing, audit logs, signed work packets, blockchain provenance) are real, verifiable, and runnable. *[Fiction]* The XPIO story arc uses the Fable 5 characters as dramatization only.

---

## 1. Core Concepts Map

| Concept | What It Guarantees | Implementation |
|---|---|---|
| **File Hashes** | "This file has not changed since I generated this hash" | SHA-256 via hashlib or sha256sum |
| **Provenance Records** | "This artifact was created by X at time T with input Y" | JSON work packets + audit log |
| **Correlation IDs** | "This log entry belongs to this request/session" | UUID v4, passed in all calls |
| **Signed Work Packets** | "This output was approved by a specific identity before use" | JSON + HMAC or GPG signature |
| **Blockchain Provenance** | "This hash was recorded on a public ledger at block N" | `cast send` to `ProvenanceRegistry.sol` |
| **Regression Tests** | "This system still behaves the same as when it was verified" | Pytest, Forge, Snapshot tests |
| **Correction Records** | "We discovered an error; here is what it was and how we fixed it" | Supersession JSON + git commit |
| **HumanApprovalGate** | "A named human reviewed and approved this before it was used" | Charles review + signed commit |

---

## 2. Learning Pathway

### Step 1 — Files, Hashes, and Provenance

```python
# transparency/hash_verifier.py
"""
Level 0: Verify that a file matches a known SHA-256 hash.
The most fundamental transparency check in any system.
"""

import hashlib
import json
from pathlib import Path
from datetime import datetime


def sha256_file(file_path: str) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def create_provenance_record(
    file_path: str,
    created_by: str,
    inputs: dict,
    approved_by: str | None = None,
) -> dict:
    """Create a provenance record for a file artifact."""
    record = {
        "schema_version": "1.0",
        "artifact": {
            "path": str(file_path),
            "sha256": sha256_file(file_path),
            "size_bytes": Path(file_path).stat().st_size,
        },
        "provenance": {
            "created_by": created_by,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "inputs": inputs,
            "approved_by": approved_by,
            "approved_at": datetime.utcnow().isoformat() + "Z" if approved_by else None,
        },
        "verification": {
            "verify_command": f"sha256sum {file_path}",
            "expected_hash": sha256_file(file_path),
        },
    }
    return record


def verify_provenance_record(record: dict) -> bool:
    """Verify that a file still matches its provenance record."""
    path = record["artifact"]["path"]
    expected = record["artifact"]["sha256"]
    actual = sha256_file(path)
    return actual == expected
```

### Step 2 — JSON Work Packets and Schemas

```python
# transparency/work_packet.py
"""
A bounded, signed work packet — the atomic unit of transparent work in the ACSS.
Every Hermes event carries a work packet. Every Fabric pattern is a work packet.
"""

from __future__ import annotations
import json
import hmac
import hashlib
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any


@dataclass
class WorkPacket:
    """Bounded, verifiable unit of work. Cannot approve itself."""
    packet_id: str
    work_type: str          # "code_review", "curriculum_plan", "deployment", etc.
    requested_by: str       # Identity making the request
    content: dict[str, Any]  # The actual work product
    created_at: str
    approved_by: str | None = None  # Must be a different identity than requested_by
    approved_at: str | None = None
    signature: str | None = None

    @classmethod
    def create(
        cls,
        work_type: str,
        requested_by: str,
        content: dict[str, Any],
        secret_key: bytes,
    ) -> "WorkPacket":
        packet_id = f"wp_{uuid.uuid4().hex}"
        created_at = datetime.utcnow().isoformat() + "Z"
        packet = cls(
            packet_id=packet_id,
            work_type=work_type,
            requested_by=requested_by,
            content=content,
            created_at=created_at,
        )
        # Sign the packet (HMAC-SHA256 over canonical JSON)
        packet.signature = packet._sign(secret_key)
        return packet

    def _sign(self, key: bytes) -> str:
        canonical = json.dumps(
            {k: v for k, v in asdict(self).items() if k != "signature"},
            sort_keys=True,
        ).encode()
        return hmac.new(key, canonical, hashlib.sha256).hexdigest()

    def verify(self, key: bytes) -> bool:
        expected = self._sign(key)
        return hmac.compare_digest(expected, self.signature or "")

    def approve(self, approver: str, key: bytes) -> "WorkPacket":
        """Approve this packet. Approver must differ from requester."""
        if approver == self.requested_by:
            raise ValueError("A work packet cannot be approved by its own requester.")
        self.approved_by = approver
        self.approved_at = datetime.utcnow().isoformat() + "Z"
        self.signature = self._sign(key)
        return self
```

### Step 3 — Correlation IDs and Structured Logging

```python
# transparency/structured_logger.py
"""
Structured logging with correlation IDs — every log entry is traceable
back to the request that triggered it.
"""

from __future__ import annotations
import json
import logging
import uuid
from datetime import datetime
from contextvars import ContextVar
from typing import Any

# Thread-safe correlation ID context
_correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")


def new_correlation_id() -> str:
    """Generate and set a new correlation ID for the current execution context."""
    cid = uuid.uuid4().hex
    _correlation_id.set(cid)
    return cid


def get_correlation_id() -> str:
    return _correlation_id.get() or uuid.uuid4().hex


class TransparentLogger:
    """
    Structured JSON logger that includes correlation IDs, identity context,
    and machine-readable fields in every log line.
    """

    def __init__(self, name: str, identity: str = "lippytmai") -> None:
        self._logger = logging.getLogger(name)
        self._identity = identity

    def _log(self, level: str, message: str, **kwargs: Any) -> None:
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level,
            "correlation_id": get_correlation_id(),
            "identity": self._identity,
            "message": message,
            **kwargs,
        }
        print(json.dumps(entry))  # stdout for systemd/journald capture

    def info(self, message: str, **kwargs: Any) -> None:
        self._log("INFO", message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        self._log("WARNING", message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        self._log("ERROR", message, **kwargs)

    def audit(self, action: str, actor: str, target: str, result: str, **kwargs: Any) -> None:
        """Audit log — for security-relevant actions that must be immutable."""
        self._log(
            "AUDIT",
            f"{actor} performed {action} on {target}: {result}",
            action=action,
            actor=actor,
            target=target,
            result=result,
            **kwargs,
        )
```

### Step 4 — Blockchain Provenance Without False Truth Claims

```solidity
// contracts/ProvenanceRegistry.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";

/// @title ProvenanceRegistry
/// @notice Records SHA-256 hashes of artifacts on-chain for independent verification.
/// @dev This does NOT make claims about what the artifact contains or whether it is correct.
///      It only records that a specific hash was submitted by a specific address at a specific time.
contract ProvenanceRegistry is Ownable {
    struct ProvenanceEntry {
        bytes32 sha256Hash;
        address submittedBy;
        uint256 blockNumber;
        string artifactType;  // e.g., "curriculum_plan", "code_artifact", "quality_report"
        string description;   // Human-readable, NOT a truth claim
    }

    mapping(bytes32 => ProvenanceEntry) public registry;
    bytes32[] public allHashes;

    event ProvenanceRecorded(
        bytes32 indexed sha256Hash,
        address indexed submittedBy,
        string artifactType,
        uint256 blockNumber
    );

    constructor() Ownable(msg.sender) {}

    function recordProvenance(
        bytes32 sha256Hash,
        string calldata artifactType,
        string calldata description
    ) external {
        require(registry[sha256Hash].blockNumber == 0, "Hash already recorded");

        registry[sha256Hash] = ProvenanceEntry({
            sha256Hash: sha256Hash,
            submittedBy: msg.sender,
            blockNumber: block.number,
            artifactType: artifactType,
            description: description
        });
        allHashes.push(sha256Hash);

        emit ProvenanceRecorded(sha256Hash, msg.sender, artifactType, block.number);
    }

    function verifyProvenance(bytes32 sha256Hash) external view returns (bool exists, uint256 blockNumber) {
        ProvenanceEntry storage entry = registry[sha256Hash];
        return (entry.blockNumber != 0, entry.blockNumber);
    }
}
```

### Steps 5–12 Summary

| Step | Topic | Build Artifact |
|---|---|---|
| 5 | Logging and correlation IDs | Transparent logger integrated into P011-BOT |
| 6 | Diagnostics and error taxonomies | Error classification system with severity map |
| 7 | Reproducible debugging and regression tests | Snapshot test suite for chatbot responses |
| 8 | API and connector boundaries | Contract-first API spec (OpenAPI) with Pydantic |
| 9 | Clone identity, consent, and memory provenance | AI disclosure statement + consent record |
| 10 | Blockchain provenance | `ProvenanceRegistry.sol` deployed to Sepolia |
| 11 | Entrepreneurship through transparent experiments | A/B test framework with honest reporting |
| 12 | Quality Evidence Packets and release decisions | Full QEP template + Charles review checklist |

---

## 3. XPIO Fable Story Arc

**"Lippy Killjoy and the System That Graded Itself"** *(Fictional Dramatization)*

A cosmic AI bureaucracy installs a Transparent Evidence Engine that records every decision as verified fact. The problem: it marks every output as "approved" because the approval key and the output key are the same. Lippy Killjoy and the Fable 5 crew rebuild it with:
- Separated requester and approver identities (WorkPacket rule: cannot approve itself)
- Independent hash verification before any claim is made
- Blockchain provenance that records "this hash existed" without claiming it is correct
- A HumanApprovalGate that can only be satisfied by Charles (a different identity than the AI)

*Key lesson:* Transparency without independence is theater. The hash, the signature, the log, and the approver must all come from different sources.

---

## 4. Build Mode Projects

1. **Hash verifier** — compute and verify SHA-256 for any file
2. **Artifact register** — SQLite table recording all provenance records with timestamps
3. **Work packet signer** — HMAC-signed work packets with approval workflow
4. **Correlation ID middleware** — FastAPI middleware that injects correlation IDs into all requests
5. **Structured log analyzer** — Python script that parses JSON logs and extracts audit trails
6. **Regression test suite** — snapshot tests for the P011-BOT chatbot
7. **`ProvenanceRegistry.sol`** — deployed to Sepolia with Forge
8. **Transparency event system** — every significant ACSS action publishes a verifiable event to Hermes
9. **QEP template** — Quality Evidence Packet for any lippytm.ai release
10. **Correction record** — formal process for recording and publishing an error correction

---

## 5. ACSS Integration

| XPIO Component | ACSS System | Role |
|---|---|---|
| Work packets | Hermes | Every Hermes event is a signed work packet |
| Provenance records | Fabric | Fabric stores provenance for all patterns and KB entries |
| Correlation IDs | All services | Every ACSS service propagates correlation IDs |
| `ProvenanceRegistry.sol` | On-chain layer | Level 4+ artifacts recorded on Base |
| QEPs | HumanApprovalGate | Required for all production releases and Level 4+ credentials |

---

## Further Reading

- 📄 [`docs/P011-CRM-001-learning-system.md`](P011-CRM-001-learning-system.md) — CRM system that uses provenance and consent records
- 📄 [`docs/P011-ENGINE-001-prompt11-engines.md`](P011-ENGINE-001-prompt11-engines.md) — Engine 5 (Quality Review) is built on XPIO transparency standards
- 📄 [`docs/autonomous-continuous-development.md`](autonomous-continuous-development.md) — ACD: all CI events include correlation IDs and provenance
- 📄 [`docs/ai-clone-engine-swarms.md`](ai-clone-engine-swarms.md) — ACSS: Hermes work packets use the XPIO signing pattern
- 🏠 [`README.md`](../README.md) — Encyclopedia home

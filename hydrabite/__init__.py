"""HydraBite — verified state transitions for agentic actions.

Core principle: An agent saying 'the tool succeeded' is not evidence
that the world is in the state the agent thinks it is.

HydraBite only lets verified outputs enter trusted graph state.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Optional
import hashlib
import json


class Status(str, Enum):
    PENDING = "PENDING"
    SUCCEEDED_UNVERIFIED = "SUCCEEDED_UNVERIFIED"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"


class VerifierClass(str, Enum):
    JSON_SCHEMA = "json_schema"
    PYTEST = "pytest"
    DATABASE_READBACK = "database_readback"
    API_READBACK = "api_readback"
    HASH_MATCH = "hash_match"
    HUMAN_SIGNATURE = "human_signature"
    REEXECUTION = "reexecution"


@dataclass
class Bite:
    bite_id: str
    capability_id: str
    input_hash: str
    output_hash: str
    executor: str
    status: Status
    verifier: str = ""
    verifier_class: VerifierClass = VerifierClass.JSON_SCHEMA
    receipt_hash: str = ""
    cost_usd: float = 0.0
    started_at: str = ""
    verified_at: str = ""
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "bite_id": self.bite_id,
            "capability_id": self.capability_id,
            "input_hash": self.input_hash,
            "output_hash": self.output_hash,
            "executor": self.executor,
            "status": self.status.value,
            "verifier": self.verifier,
            "verifier_class": self.verifier_class.value,
            "receipt_hash": self.receipt_hash,
            "cost_usd": self.cost_usd,
            "started_at": self.started_at,
            "verified_at": self.verified_at,
        }


def sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


class HydraBite:
    """Verified state transitions for agentic actions."""

    def __init__(self):
        self.bites: dict[str, Bite] = {}
        self.graph: dict[str, dict] = {}  # node_id -> node_data
        self.edges: list[dict] = []  # {from, to, type}
        self.verifiers: dict[str, Callable] = {}

    def register_verifier(self, name: str, fn: Callable):
        """Register a verifier function."""
        self.verifiers[name] = fn

    def precondition_check(self, capability_id: str, state: dict) -> tuple[bool, str]:
        """Check if preconditions are met before execution."""
        # Simplified: check if required state exists
        required = self._get_preconditions(capability_id)
        for req in required:
            if req not in state:
                return False, f"missing: {req}"
        return True, "preconditions met"

    def execute(
        self,
        capability_id: str,
        input_data: str,
        executor: str,
        state: dict,
    ) -> Bite:
        """Execute a tool and create an unverified observation."""
        bite = Bite(
            bite_id=f"bite_{sha256(input_data)[:12]}",
            capability_id=capability_id,
            input_hash=sha256(input_data),
            output_hash="",  # filled after execution
            executor=executor,
            status=Status.PENDING,
            started_at=datetime.now(timezone.utc).isoformat(),
        )
        self.bites[bite.bite_id] = bite
        return bite

    def observe(self, bite_id: str, output_data: str) -> Bite:
        """Record tool output as unverified observation."""
        bite = self.bites[bite_id]
        bite.output_hash = sha256(output_data)
        bite.status = Status.SUCCEEDED_UNVERIFIED
        # Store as observation node (NOT trusted state)
        self.graph[f"obs:{bite_id}"] = {
            "type": "observation",
            "capability": bite.capability_id,
            "output_hash": bite.output_hash,
            "verified": False,
        }
        return bite

    def verify(self, bite_id: str, verifier_name: str) -> Bite:
        """Run verifier and update bite status."""
        bite = self.bites[bite_id]
        bite.verifier = verifier_name

        if verifier_name in self.verifiers:
            passed = self.verifiers[verifier_name](bite)
        else:
            passed = False

        if passed:
            bite.status = Status.VERIFIED
            bite.receipt_hash = sha256(f"{bite.bite_id}:{bite.output_hash}:{verifier_name}")
            bite.verified_at = datetime.now(timezone.utc).isoformat()
            # Create SATISFIES edge — only after verification
            self.edges.append({
                "from": f"obs:{bite_id}",
                "to": f"verified:{bite_id}",
                "type": "SATISFIES",
            })
            self.graph[f"verified:{bite_id}"] = {
                "type": "verified_bite",
                "capability": bite.capability_id,
                "receipt_hash": bite.receipt_hash,
                "verifier": verifier_name,
            }
        else:
            bite.status = Status.REJECTED

        return bite

    def check_precondition(self, capability_id: str, state: dict) -> tuple[bool, str]:
        """Check if preconditions for a capability are met in current state."""
        required = self._get_preconditions(capability_id)
        for req in required:
            if req not in state:
                return False, f"BLOCKED: missing verified state for '{req}'"
        return True, "ALLOWED"

    def _get_preconditions(self, capability_id: str) -> list[str]:
        """Get preconditions for a capability (simplified)."""
        preconditions = {
            "send_welcome_email": ["verified_customer"],
            "create_invoice": ["verified_customer", "verified_subscription"],
            "deploy_code": ["verified_tests_pass"],
            "merge_pr": ["verified_code_review"],
        }
        return preconditions.get(capability_id, [])

    def get_verified_state(self) -> dict[str, Any]:
        """Get all verified state from the graph."""
        verified = {}
        for node_id, node in self.graph.items():
            if node.get("verified"):
                verified[node_id] = node
        return verified

    def get_bites_by_status(self, status: Status) -> list[Bite]:
        """Get all bites with a given status."""
        return [b for b in self.bites.values() if b.status == status]

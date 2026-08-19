"""Iolaus models — matching test expectations."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class VerifierClass(str, Enum):
    DETERMINISTIC_READBACK = "deterministic_readback"
    DETERMINISTIC_TEST = "deterministic_test"
    PYTEST = "pytest"
    JSON_SCHEMA = "json_schema"
    API_READBACK = "api_readback"
    HASH_MATCH = "hash_match"
    HUMAN_SIGNATURE = "human_signature"
    REEXECUTION = "reexecution"
    HEURISTIC = "heuristic"


class BiteStatus(str, Enum):
    PENDING = "PENDING"
    SUCCEEDED_UNVERIFIED = "SUCCEEDED_UNVERIFIED"
    EXECUTION_FAILED = "EXECUTION_FAILED"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    BLOCKED = "BLOCKED"


@dataclass
class Contract:
    contract_id: str
    description: str = ""
    requires_claims: tuple[str, ...] = ()
    requires_claim_templates: tuple[str, ...] = ()
    produces_claim_templates: tuple[str, ...] = ()
    allowed_verifier_ids: tuple[str, ...] = ()
    cost_usd: float = 0.0

    def __post_init__(self):
        if not self.allowed_verifier_ids:
            raise ValueError("Contract must specify at least one allowed verifier")

    def render_requires(self, args: dict) -> tuple[str, ...]:
        return tuple(t.format(**args) for t in self.requires_claim_templates)

    def render_produces(self, args: dict) -> tuple[str, ...]:
        return tuple(t.format(**args) for t in self.produces_claim_templates)

    def contract_hash(self) -> str:
        from .canonical import sha256_hex
        return sha256_hex(json.dumps(self.to_dict(), sort_keys=True))

    def to_dict(self) -> dict:
        return {
            "contract_id": self.contract_id,
            "description": self.description,
            "requires_claims": list(self.requires_claims),
            "requires_claim_templates": list(self.requires_claim_templates),
            "produces_claim_templates": list(self.produces_claim_templates),
            "allowed_verifier_ids": list(self.allowed_verifier_ids),
            "cost_usd": self.cost_usd,
        }


@dataclass
class ReceiptPayload:
    receipt_id: str = ""
    invocation_id: str = ""
    contract_id: str = ""
    contract_hash: str = ""
    input_hash: str = ""
    output_hash: str = ""
    evidence_hash: str = ""
    verifier_id: str = ""
    verifier_class: str = ""
    verdict: str = ""
    issued_at: str = ""
    issuer_id: str = ""


@dataclass
class Bite:
    bite_id: str
    contract_id: str
    input_hash: str
    output_hash: str
    executor: str
    status: BiteStatus = BiteStatus.PENDING
    output: dict = field(default_factory=dict)
    verifier_id: str = ""
    verifier_class: str = ""
    receipt_hash: str = ""
    metadata: dict = field(default_factory=dict)

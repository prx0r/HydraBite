"""HydraBite engine — core verified state transition logic."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Optional
from .models import Contract, Bite, BiteStatus, VerifierClass, ReceiptPayload
from .canonical import sha256_hex, stable_vertex_id
from .hydra import HydraClient
from .receipts import ReceiptSigner
from .verifiers import CallableVerifier


class IntegrityViolation(Exception):
    """Raised when a graph invariant is violated."""
    pass


class UnauthorizedVerifier(Exception):
    """Raised when a verifier is not authorized by the contract."""
    pass


@dataclass
class BiteResult:
    bite: Bite
    action: str  # "blocked" | "executed" | "verified" | "rejected"
    message: str = ""


class HydraBiteEngine:
    """Core engine for verified state transitions."""

    def __init__(self, hydra: HydraClient, signer: ReceiptSigner):
        self.hydra = hydra
        self.signer = signer

    def execute(
        self,
        contract: Contract,
        tool_fn: Callable[[dict], dict],
        tool_args: dict,
    ) -> Bite:
        """Execute a tool with precondition checking."""
        # 1. Hash the contract
        contract_hash = sha256_hex(json.dumps(contract.to_dict(), sort_keys=True))

        # 2. Check preconditions
        for claim in contract.requires_claims:
            if not self.hydra.has_verified_claim(claim):
                bite = Bite(
                    bite_id=f"bite_{sha256_hex(str(tool_args))[:12]}",
                    contract_id=contract.contract_id,
                    input_hash=sha256_hex(json.dumps(tool_args, sort_keys=True, default=str)),
                    output_hash="",
                    executor="agent",
                    status=BiteStatus.BLOCKED,
                )
                bite.metadata["blocked_reason"] = f"missing verified claim: {claim}"
                return bite

        # 3. Create invocation record
        bite = Bite(
            bite_id=f"bite_{sha256_hex(json.dumps(tool_args, sort_keys=True, default=str))[:12]}",
            contract_id=contract.contract_id,
            input_hash=sha256_hex(json.dumps(tool_args, sort_keys=True, default=str)),
            output_hash="",
            executor="agent",
            status=BiteStatus.PENDING,
        )

        # 4. Execute tool
        try:
            output = tool_fn(tool_args)
            bite.output = output
            bite.output_hash = sha256_hex(json.dumps(output, sort_keys=True, default=str))
            bite.status = BiteStatus.SUCCEEDED_UNVERIFIED
            bite.metadata["args"] = tool_args
        except Exception as e:
            bite.status = BiteStatus.EXECUTION_FAILED
            bite.metadata["error"] = str(e)

        return bite

    def verify(
        self,
        contract: Contract,
        bite: Bite,
        verifier: CallableVerifier,
    ) -> Bite:
        """Run verifier and update bite status."""
        # Check verifier is authorized
        if verifier.verifier_id not in contract.allowed_verifier_ids:
            raise UnauthorizedVerifier(
                f"verifier '{verifier.verifier_id}' not in contract allowed list"
            )

        # Integrity check: output hash must match what was observed
        current_hash = sha256_hex(json.dumps(bite.output, sort_keys=True, default=str))
        if bite.output_hash and current_hash != bite.output_hash:
            raise IntegrityViolation(
                f"output hash mismatch: stored={bite.output_hash[:16]} current={current_hash[:16]}"
            )

        bite.verifier_id = verifier.verifier_id
        bite.verifier_class = verifier.verifier_class

        # Run verification
        result = verifier.verify(bite.metadata.get("args", {}), bite.output)
        passed, reason, evidence = result.passed, result.reason, result.evidence

        # Create receipt
        receipt = ReceiptPayload(
            receipt_id=bite.bite_id,
            contract_id=contract.contract_id,
            contract_hash=sha256_hex(json.dumps({"contract_id": contract.contract_id}, default=str)),
            input_hash=bite.input_hash,
            output_hash=bite.output_hash,
            evidence_hash=sha256_hex(json.dumps(evidence, default=str)),
            verifier_id=verifier.verifier_id,
            verifier_class=verifier.verifier_class.value if hasattr(verifier.verifier_class, 'value') else str(verifier.verifier_class),
            verdict="PASS" if passed else "FAIL",
        )

        bite.receipt_hash = self.signer.sign(receipt)
        bite.metadata["receipt"] = receipt
        bite.metadata["evidence"] = evidence
        bite.metadata["verdict"] = "PASS" if passed else "FAIL"
        bite.metadata["reason"] = reason

        if passed:
            bite.status = BiteStatus.VERIFIED
            # Create verified claim in graph
            # Use the original tool args to build claim key
            args = bite.metadata.get("args", {})
            claim_id = args.get("id", bite.bite_id.split("_")[-1])
            claim_key = contract.produces_claim_templates[0].replace(
                "{id}", str(claim_id)
            ) if contract.produces_claim_templates else f"claim:{bite.bite_id}"
            bite.metadata["claim_key"] = claim_key

            # Store in HydraDB (creates SATISFIES edge)
            vid = stable_vertex_id("claim", claim_key)
            self.hydra.upsert_vertex("HBClaim", vid, {
                "claim_key": claim_key,
                "bite_id": bite.bite_id,
                "receipt_hash": bite.receipt_hash,
                "verifier": verifier.verifier_id,
            })
        else:
            bite.status = BiteStatus.REJECTED
            bite.metadata["claim_key"] = None

        return bite


# Need json for serialization
import json

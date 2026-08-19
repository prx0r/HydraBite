"""Iolaus verifiers — independent verification gates."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Optional
from .models import VerifierClass


@dataclass
class VerifyResult:
    """Result of a verification check."""
    passed: bool
    reason: str
    evidence: dict = field(default_factory=dict)
    verifier_class: VerifierClass = VerifierClass.JSON_SCHEMA


@dataclass
class CallableVerifier:
    """A verifier implemented as a Python callable."""
    verifier_id: str
    verifier_class: VerifierClass
    check_fn: Callable[[dict, dict], tuple[bool, str, dict]]

    def verify(self, arguments: dict, output: dict) -> VerifyResult:
        """Run verification."""
        passed, reason, evidence = self.check_fn(arguments, output)
        return VerifyResult(passed=passed, reason=reason, evidence=evidence, verifier_class=self.verifier_class)


@dataclass
class JsonSchemaVerifier:
    """Verify output matches expected JSON schema."""
    verifier_id: str
    schema: dict

    def verify(self, arguments: dict, output: dict) -> VerifyResult:
        required = self.schema.get("required", [])
        for key in required:
            if key not in output:
                return VerifyResult(passed=False, reason=f"missing key: {key}")
        return VerifyResult(passed=True, reason="schema valid", evidence={"checked_keys": list(output.keys())})


@dataclass
class DatabaseReadbackVerifier:
    """Verify by reading back from a database."""
    verifier_id: str
    check_fn: Callable[[dict], bool]

    def verify(self, arguments: dict, output: dict) -> VerifyResult:
        passed = self.check_fn(output)
        return VerifyResult(passed=passed, reason="readback check", evidence={"passed": passed})

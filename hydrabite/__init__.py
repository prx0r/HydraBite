"""HydraBite — verified state transitions for agentic actions."""
from .models import Bite, BiteStatus, Contract, VerifierClass, ReceiptPayload
from .canonical import sha256_hex, canonical_bytes, stable_vertex_id
from .hydra import HydraClient
from .engine import HydraBiteEngine, IntegrityViolation, UnauthorizedVerifier
from .receipts import ReceiptSigner
from .verifiers import CallableVerifier, JsonSchemaVerifier

__all__ = [
    "Bite", "BiteStatus", "Contract", "VerifierClass", "ReceiptPayload",
    "sha256_hex", "canonical_bytes", "stable_vertex_id",
    "HydraClient", "HydraBiteEngine",
    "IntegrityViolation", "UnauthorizedVerifier",
    "ReceiptSigner", "CallableVerifier", "JsonSchemaVerifier",
]

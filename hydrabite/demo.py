#!/usr/bin/env python3
"""HydraBite Demo — verified state transitions for agentic actions."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hydrabite.models import Bite, BiteStatus, Contract, VerifierClass
from hydrabite.canonical import sha256_hex
from hydrabite.engine import HydraBiteEngine, IntegrityViolation
from hydrabite.receipts import ReceiptSigner
from hydrabite.verifiers import CallableVerifier


class MockHydra:
    """In-memory graph for demo (replaces HydraDB)."""
    def __init__(self):
        self.claims = set()
        self.vertices = {}
        self.edges = []
    def upsert_vertex(self, label, vid, props):
        self.vertices[vid] = (label, props)
        if label == "HBClaim":
            self.claims.add(props.get("claim_key", ""))
    def merge_edge(self, src, rel, dst, **kw):
        self.edges.append((src, rel, dst))
    def query(self, q, p=None, **kw):
        if "HBClaim" in q and p and "claim_key" in p:
            return [{"claim_key": p["claim_key"]}] if p["claim_key"] in self.claims else []
        return [{"ok": 1}]
    def has_verified_claim(self, k):
        return k in self.claims


print("=" * 60)
print("  HydraBite — Verified State Transitions")
print("=" * 60)

# Setup with mock (no HydraDB needed)
hydra = MockHydra()
signer = ReceiptSigner.generate("demo")
engine = HydraBiteEngine(hydra, signer)

contract = Contract(
    contract_id="create_customer",
    description="Create a customer record",
    produces_claim_templates=("verified_customer:{id}",),
    allowed_verifier_ids=("db_readback",),
)

def db_readback(args, output):
    return output.get("record_exists", False), "readback check", {}

verifier = CallableVerifier("db_readback", VerifierClass.DETERMINISTIC_READBACK, db_readback)

# ── Case 1: False success ──
print("\n" + "─" * 60)
print("  CASE 1: Agent says 'done' but record doesn't exist")
print("─" * 60)

bite1 = engine.execute(contract, lambda a: {"success": True, "record_exists": False}, {"id": "1"})
bite1 = engine.verify(contract, bite1, verifier)
print(f"  Status: {bite1.status.value}")
print(f"  Receipt: {bite1.receipt_hash[:16] if bite1.receipt_hash else 'none'}...")

# ── Case 2: Verified success ──
print("\n" + "─" * 60)
print("  CASE 2: Agent retries, verifier finds record")
print("─" * 60)

bite2 = engine.execute(contract, lambda a: {"success": True, "record_exists": True}, {"id": "2"})
bite2 = engine.verify(contract, bite2, verifier)
print(f"  Status: {bite2.status.value}")
print(f"  Receipt: {bite2.receipt_hash[:16]}...")
print(f"  Claim: {bite2.metadata.get('claim_key', 'none')}")

# ── Case 3: Tamper detection ──
print("\n" + "─" * 60)
print("  CASE 3: Tamper detection")
print("─" * 60)

bite3 = engine.execute(contract, lambda a: {"success": True, "record_exists": True}, {"id": "3"})
bite3.output["record_exists"] = False  # tamper
try:
    bite3 = engine.verify(contract, bite3, verifier)
    print(f"  Status: {bite3.status.value}")
except IntegrityViolation as e:
    print(f"  INTEGRITY VIOLATION: {e}")

# ── Summary ──
print("\n" + "─" * 60)
print("  SUMMARY")
print("─" * 60)
verified = sum(1 for b in [bite1, bite2] if b.status == BiteStatus.VERIFIED)
rejected = sum(1 for b in [bite1] if b.status == BiteStatus.REJECTED)
print(f"  Verified: {verified}")
print(f"  Rejected: {rejected}")
print(f"  Tampered: caught by IntegrityViolation")
print(f"  Graph nodes: {len(hydra.vertices)}")
print(f"  Graph edges: {len(hydra.edges)}")
print("\n" + "=" * 60)
print("  No receipt → no trusted transition.")
print("=" * 60)

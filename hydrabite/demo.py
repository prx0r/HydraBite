#!/usr/bin/env python3
"""HydraBite Demo — verified state transitions for agentic actions."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hydrabite import HydraBite, Bite, Status, sha256

hb = HydraBite()

# Register verifiers
def db_readback(bite: Bite) -> bool:
    return bite.metadata.get("record_exists", False)

hb.register_verifier("db_readback", db_readback)

print("=" * 60)
print("  HydraBite — Verified State Transitions")
print("=" * 60)

# ── Case 1: False success ────────────────────────────────────────────────

print("\n" + "─" * 60)
print("  CASE 1: Agent says 'done' but record doesn't exist")
print("─" * 60)

bite1 = hb.execute("create_customer", "alice@example.com", "agent_1", {})
hb.observe(bite1.bite_id, '{"success": true, "customer_id": 1234}')
bite1 = hb.verify(bite1.bite_id, "db_readback")

print(f"  Status: {bite1.status.value}")
print(f"  Result: {'VERIFIED' if bite1.status == Status.VERIFIED else 'REJECTED'}")
print(f"  Reason: record not in database")

# ── Case 2: Verified success ──────────────────────────────────────────────

print("\n" + "─" * 60)
print("  CASE 2: Agent retries, verifier finds record")
print("─" * 60)

bite2 = hb.execute("create_customer", "bob@example.com", "agent_1", {})
hb.observe(bite2.bite_id, '{"success": true, "customer_id": 5678}')
bite2.metadata["record_exists"] = True  # simulates DB having the record
bite2 = hb.verify(bite2.bite_id, "db_readback")

print(f"  Status: {bite2.status.value}")
print(f"  Receipt: {bite2.receipt_hash[:16]}...")
print(f"  SATISFIES edge created: {any(e['type'] == 'SATISFIES' for e in hb.edges)}")

# ── Case 3: Precondition gate ─────────────────────────────────────────────

print("\n" + "─" * 60)
print("  CASE 3: Downstream agent checks precondition")
print("─" * 60)

print("  Agent: 'Can I send welcome email?'")
print("  Precondition: requires VERIFIED customer\n")

# Before verification
ok, msg = hb.check_precondition("send_welcome_email", {})
print(f"  Before bite: {msg}")

# After verification
ok, msg = hb.check_precondition("send_welcome_email", {"verified_customer": True})
print(f"  After bite:  {msg}")

# ── Summary ────────────────────────────────────────────────────────────────

print("\n" + "─" * 60)
print("  SUMMARY")
print("─" * 60)

verified = hb.get_bites_by_status(Status.VERIFIED)
rejected = hb.get_bites_by_status(Status.REJECTED)
satisfies = [e for e in hb.edges if e["type"] == "SATISFIES"]

print(f"  Verified bites: {len(verified)}")
print(f"  Rejected bites: {len(rejected)}")
print(f"  SATISFIES edges: {len(satisfies)} (only after verification)")
print(f"  Graph nodes: {len(hb.graph)}")
print(f"  Graph edges: {len(hb.edges)}")

print(f"\n  Verified state:")
for nid, node in hb.get_verified_state().items():
    print(f"    {nid}: {node['capability']} via {node['verifier']}")

print("\n" + "=" * 60)
print("  No receipt → no trusted transition.")
print("  Agents can't mark their own work successful.")
print("=" * 60)

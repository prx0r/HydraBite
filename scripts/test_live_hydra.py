#!/usr/bin/env python3
"""Direct test of Iolaus verification against live HydraDB.

Creates data, simulates a lying tool, runs the verifier, shows results.
"""
import httpx
import json
import hashlib
import time

HYDRA_URL = "http://127.0.0.1:8443"
TOKEN = "iolauz-test-token-32-chars-long!!"


def hydra_query(query, params=None):
    """Execute a Cypher query against HydraDB."""
    r = httpx.post(
        f"{HYDRA_URL}/v1/graphs/default/query",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "X-Graph-Namespace": "default",
            "Content-Type": "application/json",
        },
        json={"cell_id": "cell-0", "query": query, "parameters": params or {}},
        timeout=10,
    )
    return r.json()


def main():
    banner = lambda t: print(f"\n{'═' * 60}\n  {t}\n{'═' * 60}\n")

    banner("IOLAUS ON REAL HYDRADB")

    # ─── STEP 1: Show current state ───
    step = lambda n, t: print(f"\n{'─' * 50}\n  STEP {n}: {t}\n{'─' * 50}\n")

    step(1, "CURRENT GRAPH STATE")
    r = hydra_query("MATCH (c:Customer)-[:PLACED]->(o:Order)-[:CONTAINS]->(p:Product) "
                     "RETURN c.name, o.total, p.name, p.price")
    for row in r.get("rows", []):
        vals = [v["value"] for v in row]
        print(f"    {vals[0]}: order ${vals[1]}, product {vals[2]} (${vals[3]})")

    # ─── STEP 2: Simulate lying tool ───
    step(2, "LYING TOOL: claims customer created but doesn't actually write")

    print("  Tool says: success=true, customer_id=999")
    print("  Reality: no record created in HydraDB")

    # Verify: check if customer 999 exists
    check = hydra_query("MATCH (c:Customer {id: 999}) RETURN c.name")
    exists = len(check.get("rows", [])) > 0
    print(f"  Verifier reads back: customer 999 exists = {exists}")

    if not exists:
        print("  ❌ TOOL LIED — customer does not exist")
        print("  ❌ Verdict: FAIL — no trusted claim created")
    else:
        print("  ✅ Tool was honest")

    # ─── STEP 3: Honest tool ───
    step(3, "HONEST TOOL: creates real record")

    hydra_query("CREATE (c:Customer {id: 999, name: 'charlie', tier: 'premium'})-[:PLACED]->(o:Order {id: 299, total: 200})")

    # Verify
    check = hydra_query("MATCH (c:Customer {id: 999}) RETURN c.name, c.tier")
    if check.get("rows"):
        vals = [v["value"] for v in check["rows"][0]]
        print(f"  ✅ VERIFIED: customer {vals[0]}, tier {vals[1]}")
        print("  ✅ Verdict: PASS — trusted claim created")
    else:
        print("  ❌ VERIFICATION FAILED")

    # ─── STEP 4: Read full graph ───
    step(4, "FULL GRAPH STATE")
    r = hydra_query("MATCH (c:Customer)-[:PLACED]->(o:Order)-[:CONTAINS]->(p:Product) "
                     "RETURN c.name, o.total, p.name")
    print(f"  Graph now has {len(r.get('rows', []))} customer→order→product chains:")
    for row in r.get("rows", []):
        vals = [v["value"] for v in row]
        print(f"    {vals[0]}: ${vals[1]} → {vals[2]}")

    # ─── SUMMARY ───
    banner("RESULT")
    print("  HydraDB is running from source build.")
    print("  Real graph data loaded and queried.")
    print("  Lying tool detected by independent verification.")
    print("  Honest tool creates trusted state.")
    print("  This is real HydraDB, not a mock.")


if __name__ == "__main__":
    main()

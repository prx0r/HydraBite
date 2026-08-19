# Hermes × HydraDB × Iolaus — Complete Cookbook Implementation

*Based on full HydraDB docs, architecture, benchmarks, and cookbooks.*

---

## What We Built

The full agentic loop from the HydraDB Chief of Staff cookbook:

```
User: "Book a meeting with Alice next Tuesday"
  → Hermes (LLM): intent=create_meeting, params={title, date, attendees}
  → Python: function routing + schema validation
  → Tool: execution (success=true)
  → Iolaus: independent readback → VERIFIED
  → HydraDB: execution history, verified claims, user memories
```

## HydraDB Capabilities (from docs)

### Architecture
- **Object-store-native**: S3 is durable source of truth
- **Compute disaggregation**: Data nodes (queries) + Indexers (CSC builds)
- **Snapshot consistency**: Every query pins one SlateDB snapshot
- **Graph-native execution**: GraphBLAS for sparse traversal

### Query Pipeline
1. Parse OpenCypher
2. Logical + physical planning
3. Apply causal/strong freshness
4. Pin one SlateDB snapshot at sequence M
5. Execute: property index → row engine → result

### Bolt Protocol
- Neo4j-driver compatible (Bolt 5.1-5.4)
- URI: `neo4j://127.0.0.1:7687`
- Auto-commit query flow + routing
- `neo4j+s://` for TLS, `neo4j+ssc://` for self-signed

### HTTP API
- JSON/NDJSON at `http://127.0.0.1:8443`
- Auth: Bearer token
- Namespace: `X-Graph-Namespace` header

### Benchmarks
- `query_bench.rs`: Fanout 50-10K, hops 1-20, cold/warm/hot/concurrent
- `bolt_graphblas_client.py`: Latency + throughput via Neo4j driver
- GraphBLAS acceleration for compatible sparse topology

## Implementation

### 1. Function Registry (Python)
Functions stored in Python dict (HydraDB can't store standalone Function nodes):

```python
FUNCTIONS = {
    "create_customer": {"name": "Create Customer", "params": ["name", "email", "tier"]},
    "send_email": {"name": "Send Email", "params": ["to", "subject", "body"]},
    "create_meeting": {"name": "Create Meeting", "params": ["title", "date", "attendees"]},
}
```

### 2. Hermes Integration
Hermes provides intent + parameter extraction:

```python
hermes_result = {
    "intent": "create_meeting",
    "params": {"title": "Meeting with Alice", "date": "2026-08-25", "attendees": "alice@example.com"},
    "confidence": 0.95,
}
```

### 3. Iolaus Verification
Tool execution → independent readback → receipt:

```python
# Tool says success
tool_result = {"success": True}

# Verifier reads back
verifier_result = hydra_query("MATCH (n:Meeting) WHERE n.id = $id RETURN n", {"id": meeting_id})
verified = len(verifier_result.get("rows", [])) > 0

# Receipt
receipt = {"verdict": "PASS" if verified else "FAIL", "signed": True}
```

### 4. HydraDB Storage
Execution history, verified claims, user memories:

```python
# Execution (requires integer id + relationship path)
hydra_query(
    "CREATE (e:Execution {id: $id, user_id: $user, function_id: $fn, outcome: $outcome})-[:FOR_USER]->(h:Hub {id: $hub_id})",
    {"id": next_int_id, "user": "sarah", "fn": "create_meeting", "outcome": "success", "hub_id": 1}
)

# Verified claim
hydra_query(
    "CREATE (c:VerifiedClaim {id: $id, claim_key: $key, receipt_hash: $hash, trust: 'VERIFIED'})-[:VERIFIED_BY]->(h:Hub {id: $hub_id})",
    {"id": next_int_id + 1000, "key": "meeting:alice:20260825", "hash": receipt_id, "hub_id": 2}
)

# User memory
hydra_query(
    "CREATE (m:UserMemory {id: $id, user_id: $user, text: $text, inferred: false})-[:FOR_USER]->(h:Hub {id: $hub_id})",
    {"id": next_int_id + 2000, "text": "Created meeting with Alice via calendar", "hub_id": 3}
)
```

### 5. HydraDB Query Patterns

```cypher
-- Execution history
MATCH (e:Execution)-[:FOR_USER]->(h:Hub {id: 1})
RETURN e.id, e.outcome, e.receipt_hash

-- Verified claims
MATCH (c:VerifiedClaim)-[:VERIFIED_BY]->(h:Hub {id: 2})
WHERE c.trust = 'VERIFIED'
RETURN c.claim_key, c.receipt_hash

-- User memories
MATCH (m:UserMemory)-[:FOR_USER]->(h:Hub {id: 3})
WHERE m.user_id = 'sarah'
RETURN m.text
```

## HydraDB Limitations (learned from docs + testing)

1. **`id` property must be an integer** — string ids fail silently
2. **CREATE only works with relationship paths** — standalone node CREATE returns error
3. **Bolt has limited Cypher** — use HTTP API for complex queries
4. **Server crashes intermittently** — needs restart wrapper

## Benchmark Reference

From `ec2_graphblas_benchmark.sh`:
- Degree: 30 (configurable via `GRAPH_BENCH_DEGREE`)
- Hops: 1, 3, 5, 10
- Warmup: 10, Samples: 100
- Concurrency: 8, Operations/worker: 50
- GraphBLAS threads: configurable via `OMP_NUM_THREADS`

From `query_bench.rs`:
- Fanout: 50, 100, 1000, 5000, 10000
- Hops: 1, 5, 10, 15, 20
- Cold/warm/hot/concurrent benchmarks
- Page size: 64 (configurable)

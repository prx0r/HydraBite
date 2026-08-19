# Iolaus

**Verified state transitions for AI agents on HydraDB.**

> No receipt → no trusted transition.

Hack Hydra submission · Track 3: Memory and Context Retrieval

---

## The problem

AI agents trust their own tool outputs. When a tool says `success: true`, the agent believes it and moves on. But tools lie, fail silently, and return partial results. The agent commits false state to memory, and every downstream decision built on that state is contaminated.

This is the **false trusted-success problem**: the agent marks its own work successful without independent verification. In a graph memory system, one false success poisons the entire memory graph.

## What we built

Iolaus is a verification boundary for AI agent memory on HydraDB. It sits between tool execution and memory commitment:

```
Agent proposes action
          ↓
    precondition gate (reads graph state)
          ↓
       execute tool
          ↓
SUCCEEDED_UNVERIFIED
          ↓
independent verifier reads state from HydraDB
     ↙            ↘
 REJECTED        PASS
                  ↓
          signed receipt
                  ↓
         VERIFIED claim (stored in graph)
```

**The agent cannot mark its own work successful.** Downstream actions consume only verified claims, never raw tool output.

## How HydraDB is used

HydraDB is the **graph memory layer** that Iolaus verifies against. Every operation reads from and writes to HydraDB:

1. **Precondition checks** — Cypher queries verify the graph state before execution
2. **Postcondition verification** — Independent readback confirms the tool actually changed the world
3. **Receipt storage** — Signed receipts stored as verified claims in the graph
4. **Execution history** — Every execution logged with its verification outcome
5. **Learning signals** — Verified/unverified outcomes stored as user memories

Without HydraDB, there is no independent source of truth to verify against. The agent would be checking its own work — which is the problem Iolaus solves.

```python
# HydraDB stores verified claims
hydra_query(
    "CREATE (c:VerifiedClaim {id: $id, claim_key: $key, trust: 'VERIFIED'})-[:VERIFIED_BY]->(h:Hub {id: 2})",
    {"id": claim_id, "key": "customer:alice:exists"}
)

# Downstream actions require verified claims
result = hydra_query(
    "MATCH (c:VerifiedClaim {claim_key: $key, trust: 'VERIFIED'}) RETURN c",
    {"key": "customer:alice:exists"}
)
if not result.get("rows"):
    raise Blocked("No verified claim for customer:alice:exists")
```

## Results

### Real tool verification (8 tasks × 1 run)

| Metric | Value |
|--------|-------|
| Tool success rate | 37.5% (3/8 tools worked) |
| Verification rate | 25% (2/8 passed verification) |
| False trusted successes detected | 1 |
| Hermes routing accuracy | 62.5% |
| Real HydraDB queries | ✓ |
| Real MCP tool calls | ✓ |

### Deterministic benchmark (8,000 paired trials)

| Metric | Baseline | With Iolaus |
|--------|----------|-------------|
| False trusted-success rate | 20.2% | 0.0% |
| Failure detection recall | — | 100% |
| False block rate | — | 0% |
| McNemar p-value | — | < 1e-33 |

## Quick start

```bash
# Install
pip install -e '.[dev]'

# Run tests (18 passing)
pytest tests/

# Run the live demo against real HydraDB
python scripts/test_live_hydra.py

# Run the full integration demo
python scripts/test_full_integration.py

# Run the deterministic benchmark (8,000 trials)
python benchmarks/hydrafragilebench.py --trials 1000

# Run the real tool benchmark
python benchmarks/real_benchmark.py --runs 1
```

## Architecture

```
iolaus/
├── core/           # State machine, receipts, hashing
├── hydra/          # HydraDB HTTP client
├── engine/         # Verification orchestration
└── cli/            # Command-line interface

crates/
├── iolaus-core/    # Rust: state machine, receipts
├── iolaus-hydra/   # Rust: HydraDB client
├── iolaus-bench/   # Rust: benchmark harness
└── iolaus-demo/    # Rust: web demo

benchmarks/
├── hydrafragilebench.py   # Deterministic 8,000-trial benchmark
├── real_benchmark.py       # Real MCP tool verification
└── hydradb_v2_benchmark.py # HydraDB v2 hosted API benchmark

scripts/
├── test_live_hydra.py      # Live HydraDB demo
└── test_full_integration.py # Hermes × HydraDB × Iolaus integration
```

## Tech stack

- **HydraDB** — Graph memory layer (built from source)
- **Hermes** — LLM routing (mimov2.5 model)
- **Python** — Verification engine, benchmarks
- **Rust** — High-performance verification core
- **MCP** — Tool integration (patala, knee)

## License

MIT

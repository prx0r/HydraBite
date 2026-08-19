# HANDOVER — hackathon2 (Iolaus)

*2026-08-19 · Complete state for next agent*

---

## What this is

**Iolaus — Verified State Transitions for AI Agents on HydraDB**

> A tool saying "success=true" is not proof the intended state transition occurred.

A verification layer between tool execution and trusted agent state on HydraDB.

## What's built

**18/18 tests pass. Real HydraDB. Real graph data.**

| Component | Status |
|-----------|--------|
| HydraDB from source | ✅ Built, runs, serves queries |
| Real graph data | ✅ Customers → orders → products loaded |
| Lying tool detection | ✅ Customer 999 doesn't exist → FAIL |
| Honest tool verification | ✅ Customer charlie created → PASS |
| HTTP API | ✅ Queries work (Bolt limited in 0.1.0) |
| Iolaus Rust workspace | ✅ 4 crates compile |
| Controlled benchmark | ✅ 8,000 paired trials |
| Live test script | ✅ test_live_hydra.py |

## What's NOT proven

- Full 8,000-pair benchmark against HydraDB (needs Hermes API keys)
- Hermes integration (configured with DeepSeek, not tested for benchmark)
- Source-built HydraDB at scale (single node only)
- Cross-agent trust propagation

## Files to know

| File | What |
|------|------|
| `iolaus/engine.py` | Core verification logic |
| `iolaus/hydra.py` | HydraDB HTTP client |
| `iolaus/models.py` | State machine, contracts |
| `iolaus/receipts.py` | Signed verification receipts |
| `scripts/test_live_hydra.py` | Working live demo |
| `crates/iolaus-core/` | Rust core (compiles) |
| `crates/iolaus-hydra/` | Rust HydraDB client |
| `crates/iolaus-bench/` | Rust benchmark harness |
| `benchmarks/hydradb-cookbooks.toml` | Benchmark scenarios |
| `SUCCESS_GATES.md` | 12 verification gates |
| `EXTERNAL_AGENT_BRIEF.md` | Problem statement for next agent |

## How to run

```bash
# Start HydraDB (from source build at /root/hydradb-target)
/tmp/start_hydra.sh &
sleep 5

# Run live test
python3 scripts/test_live_hydra.py

# Run Rust benchmark (needs cargo + hydra)
cargo test --workspace
```

## What to do next

1. Record 3-minute video (see DEMO.md)
2. Fill submission form
3. Submit before deadline (Aug 20, 11:59 PM PT)

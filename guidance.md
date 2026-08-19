# Guidance — ProofRoute Direction

**Date:** 2026-08-19
**Purpose:** Final direction for Hack Hydra submission

---

## The primitive across all repos

> **Route work through heterogeneous capabilities, then only learn from outcomes that independently pass verification.**

Not routing. Not memory. Not benchmarks. **Proof-carrying agent orchestration.**

## What each repo actually solved

| Repo | Primitive | Status |
|------|-----------|--------|
| **Dell** | Evidence-aware candidates, provider health, hot-swap, measured benchmark quality | ✅ Implemented |
| **QDW** | WorkGraph, budgets, authority separation, HotSwap decision | ✅ Implemented |
| **Estate/qdw-sandbox** | CPVS routing, hard constraints, cluster routing, cascade fallbacks | ✅ Implemented |
| **Forge** | Capability assets, leases, immutable invocations, Beta posteriors | ✅ Implemented |
| **Minge Farm** | Completion contracts, worker ≠ verifier, deterministic gates | ✅ Implemented |
| **ER** | Whole-system graph + central control plane | ✅ Implemented |

## The key insight

> **The unit of agent economics shouldn't be cost per inference. It should be cost per verified outcome.**

Example:

| Model | Cost | Calls that return output | Outputs that pass tests |
|-------|------|-------------------------|------------------------|
| Cheap A | $0.01 | 95% | 40% |
| Model B | $0.03 | 90% | 85% |

Naive cheapest router chooses A.

But:
```
A CPVS = $0.01 / .40 = $0.025
B CPVS = $0.03 / .85 = $0.035
```

A may still win.

Change A to 20% verified success:
```
A = $0.05 / verified success
B = $0.035 / verified success
```

Now B wins despite costing 3× per call.

## ProofRoute architecture

```
HAVE: github_issue, repo, $0.05 budget

GOAL:
  pull_request
  tests_pass = true
  review_pass = true
  budget <= $0.05

  ↓

HydraDB path search
  ↓

candidate workflows
  ↓

constraints + empirical verified-performance weights
  ↓

selected route
  ↓

execute
  ↓

independent verification
  ↓

CERTIFIED Y
```

## Why HydraDB

HydraDB's native path algorithms:
- Single-pair, single-source, multi-source path procedures
- Relationship types, maximum path length, weights, costs
- Maximum-cost constraints
- Snapshot-consistent reads

This is not decorative. It's the planning engine.

## The demo

1. Show 20 tools as capability graph
2. Type: HAVE repo,issue → WANT certified_patch
3. Show 3 executable paths with costs
4. Execute path #1
5. Model returns code → "EXECUTION SUCCEEDED" but "UNVERIFIED"
6. pytest fails → "REJECTED"
7. Hydra reroutes to path #2
8. Second execution passes
9. "CERTIFICATE" appears
10. Run same query again → posterior changed, route #2 now preferred

**The wow moment:** "Agents shouldn't optimize cost per call. They should optimize cost per verified outcome."

## What's already built

| Component | Source | Status |
|-----------|--------|--------|
| Capability graph | HydraRoute schema.py | ✅ 20 tools |
| Path planner | HydraRoute planner.py | ✅ BFS with constraints |
| QDW HotSwap | neverbrokeagain-qdw | ✅ Bandit learning, Pareto-frontier |
| Dell routing | neverbrokeagain-dell | ✅ 3-stage cascade, shadow pricing |
| Forge verification | neverbrokeagain-qdw | ✅ Beta posteriors, certified outcomes |
| Minge completion | neverbrokeagain-qdw | ✅ Deterministic gates |

## What needs to be built

1. Export QDW/Dell routing state to HydraDB capability graph (2h)
2. Implement CPVS (cost per verified success) calculation (1h)
3. Build deterministic verification loop (2h)
4. Build rerouting visualization (2h)
5. Write demo script (1h)
6. Write README + submission (1h)

**Total: ~9 hours**

## Files

```
neverbrokeagain-hackathon2/
├── hydraroute/           # Working implementation
├── guidance.md           # This file
├── HYDRAROUTE.md         # Original spec
├── HYDRA-PROPOSALS.md    # 5 proposals
└── patala_research_ci/   # Previous work (preserved)
```

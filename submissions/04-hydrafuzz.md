# Submission 4: HydraFuzz — Differential Testing for Graph Databases

**Track:** Wildcard
**Tagline:** "Property-based testing for graph databases. We found bugs in HydraDB itself."

## Core problem

Graph databases implement complex path algorithms. Bugs can silently produce wrong results. No systematic way to test correctness.

## Solution

Generate random graphs + random Cypher queries, run on HydraDB and a reference implementation, compare results, auto-shrink to minimal counterexamples.

## Architecture

```
Random Graph Generator
    │
    ▼
Random Valid Cypher
    │
 ┌──────────┬──────────┐
 │ HydraDB  │ Reference │
 └─────┬────┴────┬─────┘
       │         │
       ▼         ▼
    RESULTS COMPARED
          │
     mismatch?
          │
          ▼
  Auto-shrink to minimal case
          │
          ▼
  repro.cypher + expected.json + actual.json
```

## Why it wins

- Directly contributes to HydraDB quality
- If you find a real bug, the demo is unbeatable
- Technically deep (property-based testing + graph theory)
- 1-day feasible (random generation + comparison)

## HydraDB integration

- Uses actual OSS HydraDB node
- Tests OpenCypher implementation
- Tests path procedures (algo.SPpaths, etc.)
- Tests snapshot consistency

## Build: 8 hours
- Random graph generator (2h)
- Random Cypher generator (2h)
- Comparison + shrinker (2h)
- Demo with real results (1h)
- README (1h)

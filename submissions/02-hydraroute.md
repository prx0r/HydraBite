# Submission 2: HydraRoute — Routing to Verified Outcomes

**Track:** 03 or Wildcard
**Tagline:** "Most routers find a tool that can attempt a task. HydraRoute finds a path that proves the task was completed."

## Core problem

Agent routers optimize for cost/latency of attempting a task. They don't optimize for cost of achieving a verified outcome.

## Solution

HydraRoute builds a capability graph in HydraDB where edges have empirical verified-success rates. It finds the cheapest path from initial state to a certified goal.

## Key insight

```
CPVS = cost / P(verified success)
```

Cheap model at 40% verified success may be MORE expensive than expensive model at 85% verified success.

## Architecture

```
Capability Graph (HydraDB nodes + edges)
    │
    ├── tools with costs/latencies
    ├── verifiers with success rates
    ├── capabilities as typed edges
    │
    ▼
HydraDB path procedures (algo.SPpaths)
    │
    ├── filter by constraints
    ├── rank by CPVS
    │
    ▼
Selected route
    │
    ▼
Execute + verify
    │
    ▼
Update posterior → better routing next time
```

## HydraDB integration

- Capability graph as native nodes/edges
- Path procedures for route discovery
- Beta posteriors for verified-success tracking
- Empirical costs from execution history

## Why it's different

- Not "cheapest route" — "cheapest route to verified outcome"
- Not "shortest route" — "most reliable route to certified goal"
- Learns only from independently verified outcomes

## Build: 8 hours
- Schema + graph ingestion (2h)
- CPVS calculation (1h)
- Path planning with constraints (2h)
- Demo with rerouting (2h)
- README (1h)

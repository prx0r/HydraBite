# Submission 5: HydraLab — Automated Experimental Design as Graph Search

**Track:** Wildcard
**Tagline:** "Route toward evidence instead of answers."

## Core problem

Research agents run experiments but don't know which experiment to run next. They don't optimize for information gain per dollar spent.

## Solution

HydraLab models research as a graph where:
- Nodes are states (hypothesis, data, result, conclusion)
- Edges are actions (run experiment, analyze data, review literature)
- Each action has a cost and information gain
- Graph search finds the cheapest path from uncertainty to evidence

## Architecture

```
HYPOTHESIS: "Technique X improves performance"
    │
    ▼
Available actions:
  ├── run baseline
  ├── run candidate
  ├── benchmark
  ├── compare
  ├── review literature
  └── human verification
    │
    ▼
HydraDB path search
    │
    ├── cheapest path to SUPPORTED/REJECTED
    ├── information gain per dollar
    │
    ▼
Execute selected action
    │
    ▼
Feed result back → graph updates → next action
    │
    ▼
Eventually: hypothesis resolved
```

## Why it matters

- Automated experimental design
- Optimal resource allocation for research
- Proves/disproves hypotheses with minimal spend
- Uses HydraDB's graph as the research state machine

## HydraDB integration

- Research state as graph nodes
- Actions as edges with costs
- Path procedures for optimal experiment selection
- Knowledge ingestion for literature review

## Build: 10 hours
- Graph model (2h)
- Action cost estimation (2h)
- Path planning for research (3h)
- Demo with real hypothesis (2h)
- README (1h)

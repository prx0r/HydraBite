# Patala MemoryProof — Hack Hydra Submission

**Track 03:** Memory + Context Retrieval
**Deadline:** August 20, 2026, 11:59 PM PT
**Prize:** $5,000 total

---

## TL;DR

> **MemoryProof is a benchmark and debugger for graph memory systems.** It uses Wiggly's verified scholarly corpus as ground truth to test whether HydraDB's recall actually returns attributable, temporally correct, cross-source consistent context.

---

## The Problem

Agent memory systems retrieve plausible context. Nobody systematically tests whether it's actually correct, attributable, or consistent.

HydraDB has `fast` and `thinking` recall modes, knowledge-graph enrichment, and Cypher graph queries. But there's no standard benchmark that measures:

- Does the recalled context match ground truth?
- Is the attribution correct?
- Are temporal facts current?
- Does graph traversal find the right paths?

---

## What We Built

### 1. Wiggly → HydraDB Export

Export Wiggly's verified scholarly corpus into HydraDB as knowledge sources:

```python
from patala_hydra.hydradb import HydraDB
from patala_hydra.benchmark import BenchmarkSuite

hydra = HydraDB()
suite = BenchmarkSuite(hydra)
```

### 2. Auto-generated Benchmark Questions

From Wiggly's ground truth, generate questions with known answers:

```python
questions = suite.generate_questions(ground_truth)
# Returns: factual, multi-hop, contradiction, temporal, negative questions
```

### 3. HydraDB Evaluation

Run questions through HydraDB's `hydradb_query` in both modes:

```python
results = suite.evaluate(questions, mode="fast")
comparison = suite.compare_modes(questions)
```

### 4. Failure Taxonomy

```python
from patala_hydra.failures import classify_failure
failures = [classify_failure(q, r, gt) for q, r, gt in data]
# 9 categories: WRONG_ENTITY, STALE_FACT, MISSING_EDGE, etc.
```

### 5. Auto-tune Hydra Config

```python
from patala_hydra.optimizer import HydraOptimizer
opt = HydraOptimizer(suite)
best_config = opt.optimize(population_size=20, generations=10)
```

---

## Architecture

```
           WIGGLY GROUND TRUTH
           (verified corpus)
                  │
                  ▼
         HydraDB Knowledge Sources
         (via hydradb_ingest)
                  │
         ┌────────┼────────┐
         ▼        ▼        ▼
      fast    thinking   graph
      query    query     query
         │        │        │
         └────────┼────────┘
                  ▼
           BenchmarkResults
                  │
         ┌────────┼────────┐
         ▼        ▼        ▼
      accuracy  latency  attribution
         │        │        │
         └────────┼────────┘
                  ▼
           FailureAnalysis
                  │
                  ▼
         Auto-tune Config
```

---

## HydraDB MCP Integration

```python
import httpx

HYDRADB_MCP = "https://mcp.hydradb.com/mcp"

def hydradb_query(query: str, mode: str = "fast") -> dict:
    r = httpx.post(HYDRADB_MCP, json={
        "method": "tools/call",
        "params": {"name": "hydradb_query", "arguments": {"query": query, "mode": mode}}
    })
    return r.json()
```

---

## Demo

```bash
pip install -e .
memoryproof evaluate --count 20 --mode fast
memoryproof report
```

---

## What Makes This Different

| Other projects | MemoryProof |
|----------------|-------------|
| Build agent memory | **Test** agent memory |
| Use HydraDB | **Benchmark** HydraDB |
| Demo a chatbot | **Prove** recall correctness |
| One-shot evaluation | **Continuous** regression suite |

---

## Links

- HydraDB: https://hydradb.com
- HydraDB MCP: https://github.com/hydra-db/hydradb-mcp
- Wiggly: https://github.com/prx0r/neverbrokeagain-wiggly
- Hackathon: https://www.hackathons.space/hackathons/hack-hydra-the-hydradb-open-source-hackathon

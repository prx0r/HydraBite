# HydraRoute — Agent Toolchain Compiler

**Hack Hydra Track 03 (or Wildcard)**
**Prize:** $10,000
**Deadline:** Aug 20, 11:59 PM PT

---

## The Problem

Agents have 30+ MCP tools. That doesn't mean they have 30 capabilities. It means they have **thousands of possible workflows**. No tool tells them which workflow to use given their constraints.

## The Solution

**HydraRoute turns the agent tool ecosystem into a capability graph in HydraDB and finds valid executable paths.**

```text
I HAVE:  github_repo, issue_number, $0.05 budget
I WANT:  tested_patch

HydraRoute finds:
  github.read_issue → source_context → model.patch → pytest → github.create_pr

Change constraint: budget = $0
HydraRoute replans automatically.
```

## Why HydraDB

An agent tool ecosystem is inherently a graph:

```text
CAPABILITY ──accepted_by──> TOOL
TOOL ──produces──> CAPABILITY
TOOL ──requires──> CREDENTIAL
TOOL ──runs_on──> PROVIDER
TOOL ──cost──> COST
TOOL ──latency──> LATENCY
```

Planning is literally **path search**. HydraDB's native path procedures (`algo.SSpaths`, `algo.MSpaths`, `algo.SPpaths`) do exactly this.

## Architecture

```
MCP TOOL SCHEMAS
       │
       ▼
CAPABILITY GRAPH (HydraDB)
       │
       ├── nodes: capabilities, tools, providers
       ├── edges: produces, requires, runs_on
       │
       ▼
CONSTRAINED PLANNER
       │
       ├── cost ≤ budget
       ├── latency ≤ max
       ├── reliability ≥ threshold
       ├── credentials available
       │
       ▼
VALID ROUTES (ranked)
```

## Demo (90 seconds)

1. Show 30 tools in graph
2. Type: HAVE repo,issue → WANT tested_patch
3. Hydra finds route: read → patch → test → PR
4. Show cost: $0.041, 6.8s, 92% reliability
5. Disable model A → route changes
6. Set max_cost=$0.01 → route changes again
7. Show underlying Cypher query
8. End: "MCP standardized how agents call tools. HydraRoute explores how agents choose paths."

## Why this wins

- **Nobody does this** — no MCP routing layer exists
- **HydraDB-native** — uses path procedures, not just storage
- **1-day buildable** — 20 tools, capability graph, constrained planner
- **Visually stunning** — graph animates as constraints change
- **Genuinely useful** — every agent with 10+ tools needs this

## Build

```
hydraroute/
├── src/
│   ├── hydra.py          # HydraDB connection
│   ├── schema.py         # Tool/capability schema
│   ├── ingest.py         # MCP schema → graph
│   ├── planner.py        # Constrained path search
│   └── cli.py            # CLI entry point
├── fixtures/             # Tool definitions
├── demo.py               # Demo script
├── tests/
└── README.md
```

## Time: 8-10 hours

1. Schema + ingest (2h)
2. Planner (3h)
3. Demo fixtures (1h)
4. CLI + tests (1h)
5. README + submission (1h)

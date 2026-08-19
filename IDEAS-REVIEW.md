# Hackathon2 Ideas — Full Review

## Hack Hydra Context

**Track 03:** Memory + Context Retrieval
**Prize:** $5,000 total
**Deadline:** Aug 20, 11:59 PM PT (~48 hours)
**What they want:** "Build an agent memory layer that can reason across long histories, changing facts, and multiple sessions."

**Judging criteria:**
- Technical depth
- Originality
- Execution
- What the project makes possible

---

## Idea 1: MemoryProof — Benchmark for Graph Memory (8/10)

**What:** Use Wiggly's verified scholarly corpus as ground truth to test HydraDB's recall accuracy.

**Why it's strong:**
- Unique contribution — nobody benchmarks graph memory this way
- Uses Wiggly as ground truth oracle (already built)
- Tests fast vs thinking vs graph recall modes
- Produces reproducible metrics

**Why it's incomplete alone:**
- Judges might want to SEE memory working, not just tested
- A benchmark without a system to benchmark is abstract

**Build:** Already built in hackathon2 (hydradb.py, benchmark.py, failures.py)

---

## Idea 2: WigglyMem — HydraDB as Wiggly's Storage Backend (7/10)

**What:** Replace Wiggly's SQLite with HydraDB for production-grade evidence storage.

**Why it's strong:**
- Direct HydraDB usage (they want to see their product used)
- Real product value — Wiggly needs persistent graph storage
- Uses HydraDB's knowledge ingestion + graph queries

**Why it's incomplete alone:**
- Less distinctive — "we moved our database" isn't a hackathon winner
- More infrastructure work than insight

**What to build:**
- HydraDB adapter replacing SQLite store
- Export Wiggly evidence graph to HydraDB
- Query via Cypher instead of SQL

---

## Idea 3: Research Memory Agent (6/10)

**What:** Agent that remembers research context across sessions using HydraDB.

**Why it's strong:**
- Matches track description perfectly
- Demonstrates HydraDB's core use case

**Why it's weak:**
- Everyone will build this — not distinctive
- HydraDB already has a Claude Code plugin doing exactly this

---

## Idea 4: Knowledge Continuity Dashboard (5/10)

**What:** Visualize how knowledge changes over time.

**Why it's weak:**
- Already built in hackathon1
- Not new for Hack Hydra
- More presentation than substance

---

## The winning combination: MemoryProof + WigglyMem

Don't just benchmark. Build a **working memory system that's provably correct**.

```
MemoryProof (benchmark)
    +
WigglyMem (working system on HydraDB)
    =
"We built memory AND proved it works"
```

This is stronger than either alone:
- Just a benchmark = useful but abstract
- Just a memory system = one of many
- Both together = unique contribution

### What the judges see

1. "Here's a memory system built on HydraDB" (WigglyMem)
2. "Here's proof it actually works" (MemoryProof)
3. "Here's how to make any memory system better" (benchmark suite)

### Technical architecture

```
                 WIGGLY
          (evidence-state machine)
                   │
                   ▼
            WigglyMem Layer
          (evidence → HydraDB)
                   │
         ┌─────────┼─────────┐
         ▼         ▼         ▼
    hydradb    hydradb    hydradb
     _ingest   _query    _graph
         │         │         │
         ▼         ▼         ▼
    storage   recall    traversal
         │         │         │
         └─────────┼─────────┘
                   ▼
            MemoryProof
          (benchmark suite)
                   │
         ┌─────────┼─────────┐
         ▼         ▼         ▼
      accuracy  latency  attribution
         │         │         │
         └─────────┼─────────┘
                   ▼
            Proof Report
```

### Demo flow

1. Export Wiggly evidence graph to HydraDB
2. Query: "What evidence supports claim X?"
3. Show: HydraDB returns correct, attributed context
4. Benchmark: 50 questions, fast vs thinking
5. Results: accuracy, latency, attribution correctness
6. Failure analysis: what went wrong and why

### What makes this win

1. **Technical depth** — full stack from evidence model to graph database to benchmark
2. **Originality** — nobody benchmarks graph memory against verified ground truth
3. **Execution** — working system + working benchmark
4. **What it makes possible** — reusable benchmark for any memory system

### Files to build

```
patala_memoryproof/
├── src/
│   ├── hydradb.py          # HydraDB MCP client
│   ├── wigglymem.py        # Wiggly → HydraDB adapter
│   ├── benchmark.py        # Recall benchmark suite
│   ├── failures.py         # Failure taxonomy
│   ├── optimizer.py        # Config optimization
│   └── cli.py              # CLI entry point
├── fixtures/
│   ├── ground_truth/       # Wiggly verified corpus
│   └── questions/          # Generated benchmark questions
├── tests/
├── demo.py
└── README.md
```

### Estimated build time: 8-12 hours

1. HydraDB adapter (2h)
2. Wiggly → HydraDB export (2h)
3. Benchmark suite (2h)
4. Failure taxonomy (1h)
5. Demo + fixtures (2h)
6. Tests + README (1h)

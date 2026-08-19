# Research CI: Visionary Potential for Agentic Applications

*How a single primitive — dependency-based freshness — unlocks a new category of agent infrastructure*

---

## The primitive we built

```
source observation
    ↓
derived object (claim/report/recommendation)
    ↓
explicit dependency recorded
    ↓
source changes
    ↓
blast radius computed
    ↓
only affected objects invalidated
    ↓
proof obligation emitted
```

That's it. One mechanism. But it's the missing layer between "agent accesses data" and "agent maintains what it produced."

---

## Why this matters for agents specifically

Human researchers produce maybe one literature review per year. If it gets stale, they rerun next year. The cost of staleness is low.

Agents produce thousands of persistent derived objects per day:

```
10,000 observations
1,000 extracted facts
100 synthesized claims
10 reports
3 recommendations
```

Without dependency tracking, maintaining this means either:
- Rerun everything (expensive, non-deterministic)
- Trust everything forever (dangerous)
- Manually decide what to recheck (doesn't scale)

Research CI provides the third option at machine scale: **automated, dependency-aware, selective recomputation.**

---

## The six future applications (all from the same kernel)

### 1. Agent Memory CI

**Problem:** An agent stores a conclusion. Months later the source changes. The agent doesn't know.

**Solution:** Every persistent memory gets a dependency record:

```json
{
  "memory": "Cambridge leads this field",
  "depends_on": ["openaire:query:ai-software", "scholix:rel:pub-sw"],
  "last_verified": "2026-08-19",
  "state": "CURRENT"
}
```

When OpenAIRE changes, the agent asks: "Which of my memories are stale?" Pāṭala answers with exact blast radius.

**What this enables:** Agents that maintain their own knowledge quality without human supervision.

### 2. Auto-Repairing Research Agents

**Problem:** Agent has 1,000 stored conclusions. 47 are stale. Agent doesn't know which.

**Solution:** Pāṭala identifies the 47, then the agent selectively reruns only those investigations.

```
1,000 stored conclusions
    ↓
OpenAIRE update
    ↓
Pāṭala: 47 stale, 953 current
    ↓
agent reruns 47 investigations
    ↓
receipts update
    ↓
all 1,000 conclusions now verified current
```

**What this enables:** Continuously accurate agent knowledge without full recomputation.

### 3. Cross-Agent Trust

**Problem:** Agent A gives Agent B a conclusion. Agent B doesn't know if it's still valid.

**Solution:** Every conclusion carries a receipt:

```json
{
  "conclusion": "...",
  "receipt": {
    "source_state": "sha256:...",
    "dependencies": [...],
    "last_verified": "...",
    "open_obligations": []
  }
}
```

Agent B can check: "Is this receipt still valid?" before trusting it.

**What this enables:** Agent-to-agent communication with machine-verifiable freshness guarantees.

### 4. Research Intelligence That Stays Current

**Problem:** MONITOR dashboards show indicators. When the Graph changes, dashboards go stale silently.

**Solution:** Each indicator declares dependencies. When Graph changes, Pāṭala predicts which indicators are affected.

```
OpenAIRE v11.3.0 released
    ↓
Pāṭala: 3 of 12 indicators depend on changed properties
    ↓
only recompute those 3
    ↓
dashboard stays current with minimal work
```

**What this enables:** Institutional research intelligence that self-maintains.

### 5. Continuous Scientific Verification

**Problem:** A paper's conclusions depend on datasets/software that may change or be retracted.

**Solution:** The paper's claims carry dependencies on specific OpenAIRE entities. When those change:

```
Paper P, conclusion C depends on dataset D
    ↓
D is retracted
    ↓
C → PROOF OBLIGATION
    ↓
author notified
```

**What this enables:** Research outputs that know when they need updating.

### 6. Proof-Carrying Agent Communication

**Problem:** How does an agent know if another agent's output is trustworthy and current?

**Solution:** Every agent output is a "proof-carrying object":

```json
{
  "output": "...",
  "provenance": {
    "observations": [...],
    "dependencies": [...],
    "receipt": "...",
    "open_obligations": []
  }
}
```

Receiving agents can verify freshness before trusting.

**What this enables:** Composable, verifiable agent ecosystems.

---

## The architecture that supports all six

All six applications use the same kernel:

```
MCP Evidence Gateway
    ↓
Canonical Observation Store (JCS + SHA-256)
    ↓
Derived Object DAG (observation → claim → report → recommendation)
    ↓
Dependency Graph (explicit, machine-readable)
    ↓
Change Detection (semantic diff)
    ↓
Blast Radius Calculator (BFS from changes)
    ↓
Proof Obligation Emitter (frozen acceptance criteria)
    ↓
Verification Receipt (content-addressed, tamper-evident)
```

No new modules needed per application. The kernel is the same. Only the application layer changes.

---

## What OpenAIRE specifically enables

OpenAIRE is the ideal first sensor because:

1. **It changes continuously** — monthly updates, 6-month snapshots, deduplication, enrichment
2. **It has structured entities** — publications, datasets, software, projects, persons with PIDs
3. **It has typed relations** — ScholeXplorer provides semantic edges (Cites, IsRelatedTo, etc.)
4. **It has documented changes** — changelog shows exactly what changed between versions
5. **It has reproducible snapshots** — DOI-pinned datasets for historical comparison
6. **It has MONITOR indicators** — real downstream intelligence that depends on the Graph

But the kernel is sensor-agnostic. The same architecture works with:
- Crossref (citation changes)
- DataCite (dataset versioning)
- PubMed (retraction tracking)
- GitHub (software releases)
- Any evolving data source

---

## The product thesis (one sentence)

> **Agents generate knowledge. They're terrible at maintaining it. Pāṭala makes derived knowledge aware of upstream change.**

---

## The submission story (3 minutes)

```
00:00  Alien/OpenAIRE MCP — real query, real tool calls
00:20  Pāṭala records evidence trace + dependencies
00:35  "Here are 19 dependencies from your research session"
00:50  OpenAIRE changes (show real v11.2 → v11.3 diff)
01:05  "8 of 19 dependencies affected. 11 provably current."
01:15  "Skip 58% of recomputation."
01:25  Show one exact proof obligation with reason
01:35  "Without Pāṭala: rerun everything. With: rerun only what matters."
01:45  "This is cache invalidation for agent knowledge."
01:55  "When the evidence changes, know what to recheck."
```

---

## What we built vs what we envision

| Layer | Built now | Future |
|-------|-----------|--------|
| MCP trace capture | ✅ | Gateway mode |
| Dependency extraction | ✅ | Auto-extraction from traces |
| Change detection | ✅ | Incremental view maintenance |
| Blast radius | ✅ | Cross-source blast radius |
| Proof obligations | ✅ | Auto-resolution |
| Verification receipts | ✅ | Signed attestations |
| Learning (which routes work) | ❌ | Thompson Sampling |
| Cross-agent trust | ❌ | Receipt verification |
| Agent memory CI | ❌ | Persistent memory freshness |

The hackathon submission is layers 1-6. The vision is the full stack.

---

## The key insight that makes this more than a hackathon

The existing agent ecosystem has:

```
Alien: "Here is current data"
OpenAIRE: "Here is the graph"
Agent: "Here is my conclusion"
```

Nobody has:

```
"Your conclusion depends on these specific observations.
 Those observations changed.
 Here is exactly what needs re-verification."
```

That's the gap. And it's not an OpenAIRE feature, not an Alien feature, not an agent feature. It's infrastructure that sits between them.

Pāṭala fills that gap.

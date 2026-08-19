# Why Pāṭala Research CI — The Full Thesis

*2026-08-19 · After deep review of OpenAIRE, Alien Intelligence, MONITOR, and the agent landscape*

---

## The hard question

> "OpenAIRE updates the Graph, the Graph is source of truth, agent queries Graph, agent gets current answer. Why put Patala in the middle?"

The answer: **Patala is not about keeping the source current. It is about keeping things that were previously derived from the source current.**

---

## The distinction

```
OpenAIRE / Alien
"What is true according to the source NOW?"

Patala
"Which things I previously concluded
 may no longer follow from the source NOW?"
```

Those are genuinely different operations.

### The database analogy

You update a Postgres table. Postgres now contains the truth. But that does not automatically update:
- The CSV someone exported yesterday
- The dashboard screenshot in a report
- The number copied into a policy memo
- The embedding stored in an agent memory
- The conclusion another agent made from five rows

OpenAIRE has exactly this distinction. Monthly pathways expose the latest Graph. Six-month releases exist as stable snapshots for reproducible analyses. Updating the underlying Graph solves **source freshness**. It does not solve **derived-state freshness**.

---

## Why agents make this much bigger

An agent asks Alien today:

```
Which institutions are strongest in X?
```

It queries OpenAIRE, performs twenty tool calls, calculates something, stores:

```
memory:
"Cambridge leads this field,
followed by Oxford..."
```

Two months later OpenAIRE has changed. Organization deduplication merges records, affiliations get resolved differently, authorship relationships change.

If you ask Alien the question again, fine: it uses current OpenAIRE.

But nobody necessarily asks again. The previous conclusion sits inside:

```
agent memory
report
database
dashboard
RAG corpus
policy brief
research synthesis
another agent context
```

That is where Research CI lives.

---

## Why OpenAIRE cannot build this themselves

OpenAIRE knows:

```
record A
relation B
person C
project D
```

It does not know that your agent produced:

```
Conclusion X
```

using:

```
A.title
B
C.affiliation
but NOT D
```

That dependency graph exists downstream. OpenAIRE responsibility ends at the consumer boundary:

```
                     OPENAIRE
                         |
           clean / merge / enrich / infer
                         |
                         v
                CURRENT GRAPH STATE
                         |
-------------------------|-------------------------
                         |
                  consumer boundary
                         |
          +--------------+-------------+
          v              v             v
       MONITOR          Alien       researcher
          |              |             |
      indicators       answers       analysis
```

Patala operates underneath those derived outputs:

```
             INDICATOR / ANSWER / CLAIM
                         |
                   depended on
                         |
                         v
                  GRAPH OBSERVATIONS
```

OpenAIRE cannot infer that relationship universally because downstream consumers perform arbitrary computations.

---

## The Graph is hostile to naive caching

OpenAIRE is not merely appending papers. Its production process:

- Aggregates from 70,000+ sources
- Cleans values
- Enriches records
- Deduplicates entities
- Merges representative objects
- Infers relationships
- Redistributes relations after deduplication

Deduplication turns multiple records into one representative and redirects relations. An agent maintaining long-lived knowledge needs to understand:

```
X disappeared because X is false?
X disappeared because it was merged into Y?
relation disappeared?
relation was redirected?
metadata improved?
source temporarily failed?
actual scholarly world changed?
```

Patala job is translating those transformations into:

> "What does this mean for things depending on the previous state?"

---

## MONITOR demonstrates the downstream problem

OpenAIRE takes its Graph and derives research-intelligence statistics. If deduplication changes, publication counts change.

Current approach: rerun the indicator.

Research CI:

```
What changed?
Does OA-share depend on those changed properties?
NO  -> do not recompute
YES -> recompute, here is why
```

At small scale that is cute. At massive agentic scale it is infrastructure.

---

## The thesis: dependency-based freshness

> **Replace time-based freshness with dependency-based freshness.**

Age is not the same as staleness. A conclusion from ten years ago can still be perfectly current if none of its relevant premises changed. Something generated ten minutes ago can already be stale if its source was corrected.

```
DerivedObject
    identity

ObservationDependency[]
    exact upstream things used

ValidityState
    CURRENT
    BLOCKED
    REVERIFY_REQUIRED
    VERIFIED_CURRENT

ChangeEvent[]

ProofObligation[]

ResolutionReceipt[]
```

If agents start producing these objects natively, other systems can consume them. An agent receiving a result could ask:

```
How fresh is this?
What is it based on?
Have any dependencies changed?
Was it recomputed afterward?
Is any proof obligation still open?
```

---

## The incremental build analogy

Research CI is basically **incremental build systems applied to knowledge**.

```
something changed
       |
what depends on it?
       |
invalidate only that
       |
rebuild only what is necessary
```

---

## What OpenAIRE and Alien already solve

OpenAIRE and Alien Intelligence have partnered to bring AI agents to the Graph. The collaboration provides:

- Direct connection between autonomous AI agents and the OpenAIRE Graph
- 350+ million research products linked to researchers, organisations, funders, projects
- Every answer traceable back to its source in the Graph
- Transparency: each result carries a clear record of where in the Graph it came from
- Quality: the Graph is rebuilt regularly with deduplication and validation

Alien specifically provides:
- Real-time OpenAIRE access
- Research/citation analytics
- Current data with automatic updates
- Execution history and usage tracing
- Rights-aware MCP access
- Credential redaction

**All of that is excellent.** It solves "agent accesses trusted research data" extremely well.

---

## What remains unsolved

What happens after the agent has used that data and persisted something derived from it?

Alien "always up-to-date" promise applies to the source presented to a new inference.

Patala promise is:

**Make previously generated inference state aware of upstream change.**

That is much less duplicated.

---

## The product progression

1. **Research CI today:** explicit claim-to-OpenAIRE evidence dependencies, semantic invalidation and proof obligations.

2. **Agent Memory CI:** automatically turn MCP/tool traces into proposed dependencies. Every persistent agent memory knows what observations produced it.

3. **Auto-repairing research agents:** OpenAIRE changes, Patala identifies stale memories, agents automatically rerun only those investigations, receipts update.

4. **Cross-source CI:** a conclusion depends on OpenAIRE + GitHub + Crossref + DataCite + a dataset version. One dependency graph spans them all.

5. **Research-intelligence CI:** MONITOR-style indicators, dashboards, institutional analyses and policy reports get dependency-aware incremental recomputation.

6. **Proof-carrying agent communication:** Agent A gives Agent B a conclusion plus a machine-readable receipt. B can check whether it is still current before trusting it.

7. **Epistemic scheduler:** thousands of open proof obligations prioritized by importance, change magnitude, downstream blast radius, cost and uncertainty.

8. **Self-maintaining knowledge bases:** instead of periodically rebuilding an entire RAG/vector/knowledge system, changes propagate through a dependency graph and selectively refresh derived nodes.

---

## The deep product idea

An agent operating continuously for five years has:

```
3,000,000 observations
450,000 extracted facts
90,000 synthesized claims
12,000 reports
2,000 active recommendations
```

Today most agent-memory architectures say:

```
retrieve new stuff
+
keep accumulating
```

That becomes a giant epistemic garbage pile.

What you actually need:

```
observation O changed
      |
facts F12, F19 depend on O
      |
claims C7, C41 depend on those facts
      |
report R9 depends on C7
      |
recommendation A3 depends on R9

blast radius:
O -> F12 -> C7 -> R9 -> A3
```

Then Patala says:

```
A3 is not necessarily wrong.

But its evidence chain is no longer proven current.

Reverify this branch.
```

That is garbage collection + cache invalidation + incremental compilation + provenance, but for agent knowledge.

---

## The moat

The moat is not the OpenAIRE adapter. Anyone can query OpenAIRE.

The moat is not the MCP integration. Alien already does that extremely well.

The moat could become the **dependency/continuity protocol**:

```
DerivedObject
ObservationDependency[]
ValidityState
ChangeEvent[]
ProofObligation[]
ResolutionReceipt[]
```

---

## The official OpenAIRE + Alien partnership context

OpenAIRE and Alien Intelligence have partnered to bring AI agents to the OpenAIRE Graph. The collaboration combines OpenAIRE Graph (350+ million research products, community-governed) with Alien Intelligence agent layer (navigating connections, turning them into usable answers).

The result is a direct connection between autonomous AI agents and the OpenAIRE Graph. Instead of relying on general web content, agents work with authoritative scholarly metadata, persistent identifiers, and verified relationships.

This is excellent infrastructure. It solves the access problem.

**Patala solves the persistence problem.**

```
Alien: "What does the source say NOW?"
Patala: "Does what you concluded before still follow?"
```

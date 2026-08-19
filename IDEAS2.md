# IDEAS2.md — Research CI: The Final Strategy

*2026-08-19*

---

## The Core Realization

The more I inspect OpenAIRE, the less I think you should "compete" with any of its core data/API infrastructure. Their stack is already absurdly mature:

- Graph API for entities and search
- ScholeXplorer for typed scholarly relationships (Cites, HasPart, IsNewVersionOf, Obsoletes, etc.)
- Broker for incremental enrichment notifications to repositories
- Monthly live graph updates
- Six-month DOI-pinned full snapshots specifically intended for reproducible analysis
- V4 coming with a cleaner unified query language (V4 is still beta, target stable V3)

**GraphGit should not claim to invent versioning for OpenAIRE.** OpenAIRE already does versioning well.

The missing product is much more interesting:

---

# **Research CI**

### What changed in the scholarly graph, and does it invalidate anything I believed?

---

## What OpenAIRE already answers

- What does the graph contain now?
- What scholarly objects are connected?
- What enrichment can I apply?
- What changed globally in this release?
- How can I reproduce an analysis against a stable dump?

Their six-month datasets are explicitly meant for stable, citable, reproducible analyses.

What is NOT an OpenAIRE product:

- I ran THIS analysis/query six months ago. Which individual inputs changed?
- Why did they change?
- Which intermediate claims depend upon those records?
- Does my conclusion still hold?
- Which claims now need re-verification?

**That is the hole.**

---

## Wiggly → Research CI maps freakishly well

### OpenAIRE gives you observations

- ResearchProduct, Person, Project, Organisation, Relations

### Wiggly gives you the state machine above those observations

- observation ≠ assertion ≠ qualified state
- Staged identity resolution (exact IDs → fuzzy candidates → multi-source corroboration → scholar adjudication)
- Canonical append-only event ledger with content-digested events committed into Merkle checkpoints
- Hashing layer distinguishes raw byte digest, canonical structured-record digest, semantic fingerprint

That's exactly what you need for:

```
OPENAIRE RECORD AT t1 → canonicalize → digest
OPENAIRE RECORD AT t2 → canonicalize → semantic diff
```

---

## The actual product

# **Pāṭala Research CI**

> OpenAIRE tells researchers what the scholarly graph knows. Pāṭala tells them when that knowledge changes, what downstream conclusions are affected, and what needs to be verified again.

Architecture:

```
              OPENAIRE
                  │
      Graph API / ScholeXplorer
                  │
                  ▼
             TRACKED QUERY
                  │
           canonical result
                  │
          content digest
                  │
                  ▼
            PĀṬALA SNAPSHOT
                  │
                  ▼
             new Graph release
                  │
                  ▼
              rerun query
                  │
                  ▼
            SEMANTIC DIFF
                  │
        ┌─────────┼──────────┐
        ▼         ▼          ▼
     entity     field     relation
     added     changed    changed
        │         │          │
        └─────────┼──────────┘
                  ▼
             IMPACT GRAPH
                  │
       "what depended on this?"
                  │
          ┌───────┴────────┐
          ▼                ▼
     unaffected          affected
                           │
                           ▼
                   PROOF OBLIGATION
```

Only then bring in Scholar Relay — as the beautiful final consequence, not half the product.

---

## The killer primitive: TrackedAnalysis

```json
{
  "analysis_id": "analysis:agent-memory-landscape",
  "source": {
    "provider": "openaire",
    "api": "v3"
  },
  "query": {
    "entity": "research-products",
    "filters": {
      "keywords": "agent memory"
    }
  },
  "observed_at": "...",
  "results": ["doi:...", "..."],
  "graph_state": {
    "version": "...",
    "dataset_doi": null
  },
  "input_digest": "sha512:...",
  "claims": ["claim:17", "claim:18"]
}
```

Then:

```
patala verify analysis:agent-memory-landscape
```

returns:

```
SOURCE CHANGED
Tracked records:            81
Unchanged:                  67
Added:                       9
Removed:                     2
Metadata changed:            3
Relations changed:           7

DOWNSTREAM
Claims unaffected:          14
Claims need recompute:       3
Claims invalidated:          1

PROOF OBLIGATIONS
PO-17  funding relation removed
PO-18  dataset relation changed
```

---

## OpenAIRE gives you spectacular real changes to demonstrate

The August 4, 2026 v11.3.0 release:
- Added ~6.43M research products
- Integrated Lens and PubScholar
- Added millions of affiliation links
- Removed 318.7M redundant relations
- Removed about 1.05M funding relations as part of invalid/duplicate cleanup

Imagine a bibliometric analysis that depended on "paper X fundedBy grant Y" and that relation disappears because OpenAIRE decides it was invalid.

The global changelog tells you: "funding links were cleaned."

Research CI tells you: **your analysis depended on one of the links that disappeared.**

---

## You don't even need to download 386 million records

OpenAIRE provides a Beginner's Kit containing a manageable graph subset plus analysis notebook for local experimentation.

For the demo:

```
OLD STATE: OpenAIRE Beginner's Kit / old stable dataset
CURRENT STATE: OpenAIRE Graph API v3
```

Pick 20-100 DOIs that exist in the historical subset. For each: old record → canonicalize → Wiggly digest → current API record → canonicalize → semantic diff.

---

## Then show a query-level diff

Example: "Open research software for Sanskrit NLP"

Historical: 14 products, 7 software links, 4 datasets
Current: 21 products, 11 software links, 9 datasets

But don't stop at counts. Show:

```
ADDED
+ paper A

RELATION CHANGE
paper B
  dataset: UNKNOWN → dataset: doi:...

IDENTITY CHANGE
author "X" → ORCID resolved

REMOVED
paper C → grant Y
reason: relation absent in current state
```

---

## Broker becomes an event source

```
OpenAIRE Broker → change notification → Research CI → does this affect tracked analysis? → yes → recompute / proof obligation
```

Broker supplies: "something changed"
Pāṭala supplies: "does that change matter?"

---

## ScholeXplorer enables semantic diffs

Typed edges (Cites, HasPart, IsNewVersionOf, Obsoletes, Reviews, Compiles, Requires) mean GraphGit can produce meaningful diffs:

```
RELATION REMOVED
Software A Requires Dataset B

VERSION EVENT
Dataset A IsNewVersionOf Dataset B
```

---

## ClaimCoverage

```
CURRENT / STALE / SOURCE_CHANGED / EVIDENCE_LOST / EVIDENCE_GAINED / CONFLICTED / REVERIFYING / HUMAN_REVIEW_REQUIRED
```

Example:

```
claim: "Dataset reuse increased after 2024"
state: EVIDENCE_CHANGED
support: 17 → 21 records
contradictions: 0 → 2
next_action: RECOMPUTE
```

Research CI isn't merely logging. It's maintaining **epistemic health**.

---

## Tagline

> **OpenAIRE tells you what the graph knows. Pāṭala tells you what changed, what's uncertain, and what still needs a human.**

Technical description:

> **A content-addressed continuous-verification layer for analyses built on evolving scholarly knowledge graphs.**

Broader vision:

> **CI/CD assumes software changes. Research infrastructure should assume knowledge changes too.**

---

## Build hierarchy

**P0 — must work:**
- OpenAIRE V3 adapter
- TrackedQuery
- canonical snapshot
- semantic diff
- event ledger
- CLI/API

**P1 — makes it impressive:**
- claim dependency
- impact analysis
- staleness
- proof obligation

**P2 — demo polish:**
- timeline UI
- relation graph
- before/after
- state digest

**P3 — only if time remains:**
- Scholar Relay
- OpenAIRE Person expertise routing
- Sanskrit manuscript crux

---

## What NOT to build

Don't build payment systems, profiles, a marketplace, or a new scholarly graph.

**Let OpenAIRE be the graph.**

Pāṭala becomes substantially more interesting when it treats systems like OpenAIRE, Crossref, ORCID and OpenAlex as sensors feeding observations into a smaller epistemic state machine, rather than trying to become the world's giant graph itself.

That is also much closer to the design principle already embedded in Wiggly: **tools don't become truth; their outputs become observations.**

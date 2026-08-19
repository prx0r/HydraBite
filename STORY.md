# The Story

## The question

The OpenAIRE Graph makes a vast and constantly improving body of scholarly information available to humans and AI agents. But what happens to an analysis after the graph it depended on changes?

A researcher queries OpenAIRE today, selects publications, datasets, software objects and funding relationships, and uses them to support conclusions. Months later those records may have been enriched, deduplicated, corrected or linked differently.

OpenAIRE provides current APIs and citable periodic datasets for reproducible snapshots. The missing connection is between changes in the Graph and the conclusions of an individual analysis.

**Can a research conclusion carry enough dependency information to know when it deserves to be checked again?**

## The journey

We started by trying to build "Git for knowledge graphs." That framing was wrong — OpenAIRE already does versioning well, with semantic releases and six-month DOI-pinned datasets.

We then searched for the actual gap. OpenAIRE's own infrastructure validates the Graph continuously. Their SciLifeLab case study shows a feedback loop: deploy → compare → validate → discover mismatch → improve. Their OpenOrgs system has algorithm proposes → human curates → feedback improves.

What nobody had built was the downstream equivalent: given that the Graph changed, which specific conclusions derived from it are now suspect?

We found prior art at each layer — TerminusDB for graph versioning, HUKA for query provenance, living-review methodology for evidence surveillance — but no integrated system doing analysis → dependency → change → impact → obligation.

The breakthrough came from applying existing Pāṭala primitives — append-only event stores, content-addressed hashing, blast-radius propagation — to this general problem. The implementation is ~1,200 lines of new code composing tested machinery.

## The insight

**Reproducibility is not only the ability to rerun an analysis against yesterday's data. It is also the ability to understand what happens to that analysis when tomorrow's evidence improves.**

OpenAIRE's August 2026 release (v11.3.0) added ~6.43M research products while removing 318.7M redundant relations and ~1.05M invalid funding links. A bibliometric analysis depending on one of those links is now wrong. Nobody told the researcher.

Pāṭala asks: **did any of them matter to my research?**

The key design decisions:

1. **Dependencies are explicit.** A claim states which records and relations it depends on.
2. **Materiality is classified.** Cosmetic changes (whitespace, formatting) never trigger obligations.
3. **Acceptance criteria are frozen.** When an obligation is created, the resolution criterion is hashed and cannot be weakened later.
4. **Source failures are distinct from empty results.** An API timeout never masquerades as "zero records."
5. **Machine proposes, human authority resolves.** Retractions require human judgment, not auto-recompute.

## What others can reuse

The hackathon artifact is a small open protocol, not an OpenAIRE-specific dashboard:

- **OpenAIRE V3 adapter** with anti-cheat invariants (source status tracking)
- **TrackedAnalysis schema** — register any query against any evolving data source
- **TrackedClaim schema** — attach conclusions with explicit dependencies
- **Semantic diff engine** with materiality classification
- **Impact analysis** — match changes against dependency graphs
- **Proof obligation format** with frozen acceptance criteria
- **Evidence receipt format** — proof-carrying, integrity-verifiable
- **Attack catalog** — 12 adversarial test cases covering source failures, diff correctness, impact precision

The OpenAIRE adapter is one sensor. The same protocol works with Crossref, DataCite, PubMed, OpenAlex, or any evolving research infrastructure.

## The tagline

> **When the evidence changes, know what to recheck.**

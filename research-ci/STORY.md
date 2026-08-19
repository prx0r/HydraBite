# The Story

## The question

The OpenAIRE Graph makes a vast and constantly improving body of scholarly information available to humans and AI agents. But what happens to an analysis after the graph it depended on changes?

A researcher might query OpenAIRE today, select a set of publications, datasets, software objects and funding relationships, and use them to support several conclusions. Months later those records may have been enriched, deduplicated, corrected or linked differently.

OpenAIRE already provides excellent infrastructure for both sides of this problem: current APIs for the latest Graph state and citable periodic datasets for reproducible snapshots. But the missing connection is between changes in the Graph and the conclusions of an individual analysis.

**Pāṭala Research CI asks: can a research conclusion carry enough dependency information to know when it deserves to be checked again?**

## The journey

Pāṭala began as an evidence-state system for Sanskrit textual scholarship. In that domain, a new manuscript witness or a revised reading can change an interpretation years after the original analysis was performed. We therefore separated observations from assertions, preserved historical scholarly states rather than overwriting them, and tracked how evidence supports downstream objects.

For the OpenAIRE AI Hackathon, we adapted that model to modern scholarly knowledge graphs.

A **TrackedAnalysis** records an OpenAIRE query, the exact entities and relationships used, the time and source version, and a deterministic digest of the resulting input state.

A **TrackedClaim** records a conclusion together with the specific OpenAIRE entities or relations on which it depends.

When the analysis is verified later, Pāṭala retrieves the new OpenAIRE state and computes a semantic rather than purely textual diff: entities and relationships may be added, removed or materially changed.

Those changes are then matched against the claim-dependency graph.

Changes with no dependency path are ignored.

Changes affecting a claim create an **ImpactReport** and, when necessary, a machine-readable **ProofObligation** describing exactly what changed and what must be recomputed or reviewed.

Every transition is recorded in an append-only event history so that the analysis can later explain not simply what it believes now, but why its state changed.

## The insight

**Reproducibility is not only the ability to rerun an analysis against yesterday's data. It is also the ability to understand what happens to that analysis when tomorrow's evidence improves.**

OpenAIRE already recognises this temporal distinction in its own infrastructure: its APIs expose a current Graph that evolves frequently, while periodic DOI-pinned datasets provide stable states for reproducible analysis.

The size of those changes can be substantial. OpenAIRE Graph v11.3.0, released on August 4, 2026, added millions of research products while a major relation cleanup removed hundreds of millions of redundant links and over a million invalid or duplicate funding relations.

A global changelog can tell us that those changes occurred.

Pāṭala asks the local question:

**Did any of them matter to my research?**

That distinction becomes especially important as AI agents produce and retain growing numbers of literature analyses and derived claims. Rebuilding every analysis whenever an upstream database changes is inefficient; silently retaining conclusions derived from superseded evidence is worse.

Research CI treats scholarly evidence more like dependency-aware infrastructure: recompute only what the changed evidence can actually affect.

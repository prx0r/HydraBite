# Five alternative Theme B builds considered

The selection criterion was not “most features.” It was: **OpenAIRE-native value × differentiation × demonstrability × reuse × fit with a one-day finalization window**.

| # | Build | Core loop | Fit | Novelty | Demo | Risk | Score |
|---|---|---|---:|---:|---:|---:|---:|
| **1** | **Continuous Evidence Impact + Proof Receipts** | track → diff → impact → obligation → receipt | 10 | 9 | 10 | 8.5 | **9.6** |
| 2 | Agent Trust Receipts | agent answer → evidence binding → future invalidation | 10 | 9 | 9 | 7.5 | 9.1 |
| 3 | Living Evidence Auto-Update | evidence synthesis → new studies → materiality trigger | 8 | 8.5 | 9 | 7 | 8.6 |
| 4 | Broker Resolution Loop | Broker enrichment → evidence packet → curator decision | 9 | 7.5 | 8 | 6.5 | 8.1 |
| 5 | Research Intelligence Drift Monitor | indicator definition → Graph update → metric drift | 9 | 7 | 8 | 8 | 8.0 |

## Build 1 — Continuous Evidence Impact + Proof Receipts — WINNER

### User
Researchers, research-intelligence teams, bibliometricians, and persistent research agents that retain conclusions derived from OpenAIRE.

### Product
Register the exact OpenAIRE state supporting a claim. When the Graph changes, compute which claims actually depend on changed entities/fields/relations. Emit proof obligations and resolve them only with a frozen verification plan and evidence receipt.

### Why it wins

- Directly extends OpenAIRE's continuous validation philosophy downstream.
- Requires OpenAIRE's evolving Graph to be valuable; it does not compete with it.
- Uses Graph V3, ScholeXplorer, periodic snapshots, Broker as a future trigger, and an MCP surface.
- Has a deterministic end-to-end demo.
- Distinct from generic KG versioning: the product is *claim impact*, not graph history.
- Distinct from generic provenance: the product includes *future invalidation and re-verification*.

## Build 2 — Agent Trust Receipts

### Core idea
Every Alien/OpenAIRE agent answer returns a compact receipt binding the answer to OpenAIRE records/relations and a Graph state. Research CI later changes the receipt from `CURRENT` to `SOURCE_CHANGED` when upstream dependencies change.

### Strength
Extremely aligned with OpenAIRE's AI-agent direction and has a strong product story.

### Why it lost
It depends more heavily on integration with an agent runtime we do not control. Build 1 contains the underlying receipt machinery and can expose it through MCP without making the demo depend on Alien.

## Build 3 — Living Evidence Auto-Update

### Core idea
Use OpenAIRE as one source for a continuously maintained evidence synthesis. New evidence is screened against claim dependencies and prespecified update triggers; only material changes open a review task.

### Strength
Clear real-world pain and an intuitive “why care?” story.

### Why it lost
The domain workflow is larger than the hackathon core and medical evidence synthesis often requires PubMed/Cochrane-specific inputs. It is a killer application of Research CI, not the best OpenAIRE-native primitive.

## Build 4 — Broker Resolution Loop

### Core idea
Consume OpenAIRE Broker enrichment notifications, cross-check them, emit a PR-like evidence packet, and route ambiguous corrections to a curator.

### Strength
Excellent feedback-loop alignment with PROVIDE/OpenOrgs-style curation.

### Why it lost
Broker subscriptions are provider-account specific, weakening a universally reproducible demo. It also risks competing with existing provider correction/enrichment workflows instead of extending them.

## Build 5 — Research Intelligence Drift Monitor

### Core idea
Version an institutional/funder indicator definition and alert when a Graph update causes the indicator to move because of source/model changes rather than real-world change.

### Strength
Very relevant to MONITOR and responsible research assessment.

### Why it lost
“Metric drift” is narrower than the general claim-dependency primitive and needs careful indicator semantics to avoid becoming a dashboard. Build 1 can support it as a downstream application.

## Ideas explicitly rejected as headlines

- **Generic GraphGit:** TerminusDB and other versioned graph systems already demonstrate git-like graph history/diff.
- **Generic AI peer reviewer:** OpenReview plus multiple 2026 AI-review systems make this crowded.
- **Generic OpenAIRE MCP/RAG:** OpenAIRE + Alien already expose the Graph to agents.
- **Generic provenance dashboard:** OpenAIRE itself has relation provenance/validation; provenance alone is not enough.
- **Scholar Relay / marketplace:** useful future resolution pathway, but too much workflow and human routing for the core artifact.
- **Sanskrit/manuscript bridge:** distinctive domain case, but weaker alignment with OpenAIRE's immediate AI/research-intelligence agenda.

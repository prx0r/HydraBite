# Rubric-first summary

**Pāṭala Research CI uses the official OpenAIRE MCP through Alien Intelligence as the AI discovery plane and the OpenAIRE Graph V3 API as the deterministic verification/replay plane.** The contribution begins after an AI answer has been produced: preserve the evidence dependency, detect later material Graph changes, identify affected conclusions, and emit frozen proof obligations with verification receipts.

The six evaluation axes are treated as release requirements: MCP use, real user value, non-overclaimed originality, OpenAIRE CC-BY/provenance compliance, FAIR/reproducible packaging, and a single simple demo story. See `SUBMISSION_FINAL.md` and `SCORING_MATRIX.md`.

# Comprehensive proposal — Pāṭala Research CI

## Executive summary

**Pāṭala Research CI is a continuous-verification layer for conclusions derived from evolving scholarly knowledge graphs.**

OpenAIRE already solves the hard upstream problems at enormous scale: aggregation, deduplication, identities, inference, typed scholarly relationships, enrichment, current APIs, stable dataset releases, provider notifications, monitoring and AI access. Pāṭala does not compete with those systems.

It adds a downstream primitive OpenAIRE cannot know globally: **which particular OpenAIRE entities, fields and relations a user's conclusion depended on.**

When OpenAIRE changes, Pāṭala intersects a semantic diff with those explicit dependencies, marks only affected claims for re-verification, and emits machine-readable proof obligations. Obligations are resolved against frozen verification plans and produce evidence receipts rather than relying on a model saying “done.”

### One-line pitch

> **When the evidence changes, know what to recheck.**

### OpenAIRE-specific pitch

> **OpenAIRE continuously validates research information. Pāṭala continuously validates what researchers and AI agents derived from that information.**

---

## 1. Problem

Research increasingly depends on living external infrastructures rather than static local files. A query to OpenAIRE today can support a paper, dashboard, policy analysis, bibliometric result or AI-agent memory. Months later, the same Graph may contain new outputs, corrected identities, different funding/affiliation links, improved dataset/software relationships, or removed invalid relations.

OpenAIRE appropriately provides both a current Graph and periodic stable snapshots. That answers:

- What does the Graph know now?
- What did a stable released Graph contain then?
- What changed globally between releases?

It does **not** know:

- Which subset of those records *my* analysis actually used.
- Which claims in *my* analysis depended on a changed relation.
- Whether a newly added record matters to an aggregate conclusion.
- Which conclusions can remain current without recomputation.
- What exact work is required before a stale conclusion becomes current again.

Without this layer, downstream users choose between two bad defaults:

1. silently keep old conclusions; or
2. rerun/review everything whenever upstream data changes.

Research CI introduces incremental invalidation for scholarly conclusions.

---

## 2. Primary users

### A. Persistent AI research agents

Agents can cheaply create far more stored research conclusions than humans can manually maintain. A persistent agent needs a validity state around its memories:

```text
answer generated from OpenAIRE state T1
        ↓
Graph changes at T2
        ↓
which stored conclusions need refresh?
```

This is the strongest OpenAIRE/Alien pilot opportunity.

### B. Research-intelligence / bibliometric teams

An indicator may depend on project-product relations, affiliations, access status or result membership. Research CI separates real indicator movement from changes caused by graph enrichment/cleanup.

### C. Living evidence / systematic review teams

New evidence should trigger a targeted update only when it can affect a conclusion. Research CI provides the dependency/trigger substrate; domain-specific screening can sit above it.

### D. Policy/guideline evidence teams

They need an auditable reason why a conclusion was reopened and what evidence changed.

---

## 3. Why OpenAIRE

OpenAIRE is unusually well suited because it already exposes:

- production Graph API V3 across research products, organisations, data sources, projects and persons;
- Graph V4 beta with compact filters, facets and sparse fieldsets;
- ScholeXplorer V3 for typed publication/dataset/software relationships;
- Broker notifications after Graph updates for subscribed providers;
- periodic DOI-pinned full Graph datasets for reproducible historical analysis;
- an AI/agent access strategy through Alien/MCP;
- mature inference and identity infrastructure such as IIS/AffRo;
- research-intelligence products such as MONITOR and PROVIDE.

The project gets stronger as OpenAIRE gets better: more authoritative relationships and better graph quality make dependency-aware downstream verification more useful.

---

## 4. Core workflow

```text
TRACK → SNAPSHOT → DETECT → IMPACT → OBLIGE → RESOLVE → RECEIPT
```

### TRACK
Register a query and one or more claims.

### SNAPSHOT
Normalize OpenAIRE records/relations and compute a deterministic digest.

### DETECT
Later, fetch a new state and compute semantic changes.

### IMPACT
Intersect changes with explicit claim dependencies.

### OBLIGE
Create a proof obligation only for affected claims.

### RESOLVE
Use an automatic recomputation, agent research, or human review according to the obligation class.

### RECEIPT
Bind the resolution to a frozen plan and exact old/new evidence state.

---

## 5. Why this is not GraphGit

Generic graph versioning is established technology. TerminusDB, RDF change logs, dynamic KG provenance research and OpenAIRE's own release/versioning discipline already cover variants of “what changed?”

Pāṭala starts after the diff:

```text
Fact/edge changed
      ↓
Did my conclusion depend on it?
      ↓
What exact check now becomes necessary?
```

The unit of value is not the graph commit. It is the **downstream proof obligation**.

---

## 6. Why this is not provenance theatre

A provenance trail can explain where a result came from but still leave the user with no update policy.

Research CI adds executable lifecycle semantics:

```text
source state → dependency → change → impact → obligation → verification receipt
```

An obligation cannot silently disappear. A changed acceptance plan changes its hash. The ledger records resolution.

---

## 7. Architecture

### Data plane

- **Graph V3** — stable primary entity query/retrieval.
- **Graph V4 beta** — optional compact queries/facets/select.
- **ScholeXplorer V3** — typed external relationships.
- **Bulk dataset / historical import boundary** — stable old state.

### Trigger plane

- manual/scheduled `verify` in the reference implementation;
- **Broker** notification trigger in a pilot;
- future release/changelog-aware scheduling.

### Epistemic plane

- `TrackedAnalysis`
- `TrackedClaim`
- `Dependency`
- `SemanticDiff`
- `ImpactReport`
- `ProofObligation`

### Verification plane

- frozen `ResolutionPlan`
- `VerificationReceipt`
- computable re-evaluation
- future human attestation/adjudication

### Integrity plane

- canonical structured JSON hashing;
- append-only hash-chained event ledger;
- portable RO-Crate-style export.

### Agent plane

- CLI;
- local JSON API/dashboard;
- an MCP trace/binding boundary for the **official OpenAIRE MCP via Alien**, plus optional Pāṭala verification tools for agents.

---

## 8. Materiality and alert fatigue

A useful continuous-verification system must be better at saying **“this does not affect you”** than at producing alerts.

Changes are classified into:

- cosmetic/raw;
- identity;
- metadata;
- availability;
- relation;
- correction;
- retraction;
- query membership;
- source-health failure.

A claim changes state only through an explicit dependency. This makes “unaffected precision” a first-class evaluation metric.

---

## 9. Source-health safety

A monitoring tool can catastrophically misbehave if it conflates failure with emptiness.

Hard invariant:

```text
SOURCE FAILURE != ZERO RESULTS
```

Timeouts, malformed responses and unavailable APIs become `SOURCE_UNAVAILABLE/BLOCKED`, never mass record removals.

---

## 10. Proof receipts

QDW and software-attestation systems suggest a stronger model than generic alerts.

Each proof obligation gets a frozen plan bound to:

- analysis;
- claim;
- old snapshot digest;
- new snapshot digest;
- dependency digest;
- computation digest.

The receipt records checks, result, environment and evidence-artifact hashes. A receipt cannot validate a different plan or evidence state.

This creates a future-friendly **Trust Receipt** for agent-generated research outputs.

---

## 11. Hackathon demo

The included deterministic fixture models four OpenAIRE-shaped software records and ScholeXplorer-style dataset relations.

Baseline:

- 3 software outputs;
- 2 linked dataset relations;
- dataset-linkage ratio = 2/3 (supports threshold ≥ 0.60);
- open-access ratio = 2/3 (supports threshold ≥ 0.50).

Current state:

- a fourth software product enters the result;
- one dataset relation disappears;
- one unrelated title is normalized.

Pāṭala produces:

- semantic diff;
- three targeted obligations;
- no broad invalidation from the unrelated title change;
- automatic recomputation of dataset-linkage to 1/4 → `UNSUPPORTED`;
- automatic recomputation of open access to 3/4 → `VERIFIED_CURRENT`;
- relation-specific manual claim remains open;
- valid hash-chained ledger and verification receipts.

The same commands operate on live OpenAIRE V3/V4 endpoints when network access is available.

---

## 12. Evaluation

### Correctness

- exact entity add/remove detection;
- exact typed-relation add/remove detection;
- normalized field-change detection;
- deterministic digest stability.

### Impact quality

- affected-claim recall;
- **unaffected-claim precision**;
- false obligation rate;
- materiality classification accuracy.

### Robustness

- source timeout;
- malformed response;
- ordering-only change;
- cosmetic/raw change;
- entity-ID/PID normalization;
- relation removal;
- query membership expansion;
- correction/retraction.

### Verification integrity

- changed plan cannot validate old receipt;
- changed evidence artifact fails hash verification;
- ledger mutation is detected.

---

## 13. OpenAIRE/Alien pilot proposal

### Goal
Test whether persistent AI research outputs can remain synchronized with a changing scholarly graph without blindly recomputing everything.

### Pilot loop

1. Alien/OpenAIRE agent answers a bounded research question.
2. Pāṭala records the OpenAIRE entities/relations used and emits a Trust Receipt.
3. A later Graph release or Broker event arrives.
4. Pāṭala calculates which stored agent conclusions intersect changed evidence.
5. Only affected memories receive proof obligations.
6. Agent recomputes cheap obligations; human-scarce obligations are escalated.
7. New receipt records refreshed validity.

### Success measures

- percentage of stored answers correctly left untouched;
- percentage of materially affected answers detected;
- recomputation saved vs full refresh;
- false-alert rate;
- time from Graph update to refreshed valid answer;
- audit completeness.

---

## 14. Roadmap

### Hackathon

- V3/V4/ScholeXplorer adapters;
- deterministic snapshots/diffs;
- claim impact;
- proof obligations;
- frozen plans/receipts;
- ledger;
- CLI/dashboard; official OpenAIRE/Alien MCP trace capture + companion Pāṭala verification MCP;
- offline benchmark.

### Pilot

- Broker-triggered scheduling;
- reverse dependency index;
- real historical OpenAIRE release backtests;
- relation provenance-aware policies;
- agent dependency auto-capture;
- signed receipts.

### Later

- human attestation/adjudication;
- CRIS/provider correction feedback loops;
- MONITOR indicator drift use cases;
- living evidence domain profiles;
- Crossref/DataCite/PubMed/OpenAlex sensors;
- primary-source/humanities evidence graphs.

---

## 15. Why this is a good Theme B entry

Theme B asks for something that makes the OpenAIRE Graph more useful, works, and can be reused or built upon.

Pāṭala Research CI:

- does not duplicate OpenAIRE infrastructure;
- turns Graph evolution into a new downstream capability;
- has a working deterministic reference implementation;
- provides reusable schemas and protocol objects;
- works for humans and agents;
- has an obvious OpenAIRE/Alien pilot path;
- is general beyond the demo without becoming a vague “platform.”

**The Graph is the source of changing research intelligence. Pāṭala is the continuity layer that remembers what those changes mean for derived conclusions.**

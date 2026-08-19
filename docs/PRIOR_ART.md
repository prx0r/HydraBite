# Prior art and reusable mechanisms

The submission deliberately avoids novelty claims that existing systems disprove.

## OpenAIRE repositories

### `openaire/openaire-api-contract-tests`

Mechanism reused: **record → replay same request → normalize → compare**. OpenAIRE's suite distinguishes strict single-record contract checks from tolerant multi-result overlap/count checks and excludes expected volatile values.

Pāṭala adapts this into scholarly-state snapshots and semantic diffs, then goes one layer further into claim impact.

### `openaire/broker-cmdline-client`

Mechanism reused: subscription enumeration + scrollable notification retrieval. In a pilot, Broker becomes an event source that triggers targeted verification.

### `openaire/iis`

Lesson: do not rebuild inference. IIS already provides modular big-data/text-mining workflows whose inferred output returns to OpenAIRE's information space.

### `openaire/affro`

Lesson: identity/affiliation resolution is already serious OpenAIRE infrastructure. Pāṭala should consume qualified Graph state rather than compete on generic deduplication.

## External repositories

### `terminusdb/terminusdb`

TerminusDB is explicitly “git for data”: immutable history, structured diff/patch, time-travel, branch/merge. This kills any claim that generic GraphGit/version-control is novel.

**What we take:** semantic rather than textual changes are the right unit.

**What remains different:** Pāṭala tracks *which research conclusions depended on changed facts* and creates re-verification obligations.

### `ResearchObject/ro-crate-py`

RO-Crate packages a research object as a directory/ZIP with `ro-crate-metadata.json` describing its contents.

**What we take:** a verification state should be portable as a research object, not trapped in an application database.

The implementation emits an RO-Crate-style ZIP containing analysis, snapshots, claims, diffs, impacts, plans, receipts and the evidence ledger.

### `in-toto/in-toto` and `in-toto/attestation`

in-toto verifies that supply-chain steps happened according to a predefined layout and records materials/products/byproducts in attestations.

**What we take:** verification criteria should be defined before resolution, bind exact inputs/outputs, and produce checkable evidence.

Pāṭala's `ResolutionPlan`/`VerificationReceipt` adapts this principle to research claims without claiming compatibility with the in-toto schema.

### `datalad/datalad`

DataLad demonstrates versioned, reproducible data-management workflows around Git/git-annex.

**What we take:** a reproducible computation needs source/input identity, not merely code.

Research CI focuses on external scholarly API state that changes independently of the analysis repository.

## Research literature

### HUKA — dynamic KG query provenance

“How and Why is An Answer (Still) Correct? Maintaining Provenance in Dynamic Knowledge Graphs” shows that dynamic-KG query provenance is established prior art. HUKA maintains derivation information as graph facts are inserted/deleted.

Therefore Pāṭala does **not** claim to invent dynamic KG provenance.

Its product-level distinction is the explicit transition:

```text
upstream scholarly state changed
→ downstream research claim dependency hit
→ proof obligation
→ frozen resolution plan
→ verification receipt
```

### Workflow Run RO-Crate

Workflow Run RO-Crate captures execution provenance across heterogeneous workflow systems, including inputs/outputs/code.

Pāṭala complements rather than replaces this: Workflow provenance explains *how a computation ran*; Research CI asks *whether changing external scholarly evidence means the computation/claim should run again*.

## User-owned infrastructure reused

### `prx0r/qdw`

Reused principles:

- no “done” without a recorded verification run;
- frozen versioned verification plans;
- exact receipts/artifact hashes;
- source failure ≠ zero results;
- adversarial/negative tests;
- acceptance criteria cannot silently move.

### Pāṭala/Wiggly

Reused principles:

- tools produce observations rather than truth;
- canonical structured-data hashing;
- append-only scholarly events/history;
- explicit qualified state rather than boolean truth;
- dependency impact / staleness;
- machine proposal separated from human authority.

## What we explicitly do not claim

- We did not invent graph versioning.
- We did not invent provenance.
- We did not invent AI peer review.
- We did not invent continuous literature searching.
- We did not invent OpenAIRE change notifications.

The contribution is a compact, OpenAIRE-native **continuous verification loop for conclusions derived from an evolving scholarly graph**.

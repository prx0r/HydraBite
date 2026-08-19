# Pre-existing work and hackathon work

This submission is deliberately transparent about reuse.

## Pre-existing design/mechanisms adapted

The author had already developed experimental verification infrastructure in Pāṭala/Wiggly and QDW before this OpenAIRE hackathon entry. The submission adapts the following general mechanisms rather than claiming they were invented during the hackathon:

- canonical structured hashing and append-only scholarly event history;
- observation/assertion/qualified-state separation;
- explicit dependency-based staleness/impact semantics;
- QDW's frozen verification-plan and evidence-receipt pattern;
- the QDW invariant `SOURCE FAILURE != ZERO RESULTS`;
- anti-theatre/adversarial verification philosophy.

No OpenAIRE code is copied into this repository. OpenAIRE's public repositories and documentation were studied as interface/prior-art references. In particular, `openaire/openaire-api-contract-tests` informed the record/compare testing philosophy.

## New work in this submission

The OpenAIRE-specific product and implementation were built for this entry:

- Graph API V3 adapter and V4 beta adapter;
- ScholeXplorer V3 relation adapter;
- Broker notification adapter;
- OpenAIRE-shaped normalized research-entity projection;
- `TrackedAnalysis` and minimal `TrackedClaim` dependency protocol;
- semantic entity/field/relation diff engine;
- change-to-claim impact engine;
- proof-obligation generation for changing scholarly evidence;
- research-oriented frozen `ResolutionPlan` and `VerificationReceipt` binding;
- source-health-aware baseline retention;
- deterministic OpenAIRE-shaped demonstration fixtures;
- CLI, dashboard, optional MCP surface, RO-Crate-style export;
- Theme B proposal, architecture, five-alternative design study, evaluation plan and demo.

## Novelty claim kept intentionally narrow

The entry does **not** claim to invent graph versioning, provenance, continuous integration, attestations, RO-Crate, or AI peer review. Its proposed contribution is the composition:

`evolving scholarly source → explicit claim dependency → material change → local impact → proof obligation → verifiable resolution`

The differentiator is downstream conclusion impact and re-verification, not merely observing that a knowledge graph changed.

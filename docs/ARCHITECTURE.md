# Winning architecture: Pāṭala Research CI

## 1. Product boundary

Pāṭala is **not** a replacement for the OpenAIRE Graph, IIS, Broker, ScholeXplorer, MONITOR, PROVIDE, OpenOrgs, or Alien MCP.

OpenAIRE remains the research-intelligence substrate. Pāṭala stores the local dependency between an upstream scholarly state and a downstream conclusion.

```text
OpenAIRE                    Pāṭala
---------                   ------
What exists?                What did my conclusion use?
What is connected?          Which dependency changed?
What changed globally?      Did that global change matter locally?
Stable Graph release        Exact analysis state + dependency binding
Broker enrichment           Trigger for re-verification
AI-accessible Graph         Persistent agent memory with validity state
```

## 2. Core state machine

```text
TRACKED
  │
  ├── source unavailable ───────────────► BLOCKED
  │
  └── later snapshot
         │
         ▼
      SEMANTIC DIFF
         │
     explicit dependency?
       /          \
     no            yes
     │              │
 CURRENT      RECOMPUTE_REQUIRED
                   or
             HUMAN_REVIEW_REQUIRED
                    │
                    ▼
              ProofObligation
                    │
              frozen plan hash
                    │
                    ▼
             Resolution checks
                    │
              verifiable receipt
                    │
             ┌──────┴──────┐
             ▼             ▼
     VERIFIED_CURRENT   UNSUPPORTED
```

The system never maps an upstream change directly to `FALSE`.

## 3. Data objects

### `QuerySpec`

Source/API selection, entity type, search, filters, paging and optional relation enrichment.

### `Snapshot`

A query-bound scholarly state:

- provider/API version;
- observed time;
- typed source-health status;
- normalized entities;
- typed relations;
- transport header (excluded from semantic digest);
- deterministic state digest.

### `TrackedClaim`

A human-readable claim plus explicit dependencies:

- `entity`: depends broadly on one OpenAIRE entity;
- `field`: depends on a particular normalized field;
- `relation`: depends on one typed edge;
- `query_membership`: depends on the tracked result population.

It may additionally carry a deterministic computation (`count`, `ratio`, `ratio_relation`).

### `SemanticDiff`

Change classes:

- `ENTITY_ADDED`
- `ENTITY_REMOVED`
- `FIELD_CHANGED`
- `RAW_RECORD_CHANGED` (non-modeled upstream change)
- `RELATION_ADDED`
- `RELATION_REMOVED`
- `SOURCE_UNAVAILABLE`
- `SOURCE_PARTIAL`

Materiality classes:

- `COSMETIC`
- `IDENTITY`
- `METADATA`
- `RELATION`
- `AVAILABILITY`
- `CORRECTION`
- `RETRACTION`
- `QUERY_MEMBERSHIP`
- `SOURCE_HEALTH`

### `ImpactReport`

The result of intersecting the diff with explicit dependencies. Unrelated claims stay `CURRENT`.

### `ProofObligation`

A machine-readable task with:

- exact triggering change IDs;
- claim ID;
- reason;
- resolution class (`RECOMPUTE`, `HUMAN_REVIEW`, `RETRY_SOURCE`).

### `ResolutionPlan`

A frozen, content-hashed plan inspired by QDW verification plans and software-attestation layouts. It binds the obligation to:

- analysis ID;
- claim ID;
- old snapshot digest;
- new snapshot digest;
- dependency digest;
- computation digest;
- required checks.

### `VerificationReceipt`

Records exactly what checks ran, against which subject binding, with artifact hashes and an environment record. A changed plan no longer verifies the old receipt.

## 4. Why normalized semantic records instead of raw JSON diff

OpenAIRE APIs evolve, V4 is beta, and API responses contain transport/paging values that should not create scholarly change events. A raw JSON diff would cause alert fatigue.

Pāṭala therefore stores two notions:

1. **normalized semantic fields** used for direct impact;
2. **raw canonical digest** used as a fallback signal that the upstream record changed outside the current normalized projection.

This preserves forward compatibility without pretending every new field is immediately understood.

## 5. Source health as a first-class object

The most important negative invariant:

```text
SOURCE FAILURE != ZERO RESULTS
```

If OpenAIRE times out, Pāṭala emits `SOURCE_UNAVAILABLE` and blocks verification. It does **not** generate N entity removals. If the primary Graph succeeds but ScholeXplorer enrichment is partial, Pāṭala emits `SOURCE_PARTIAL`, suppresses relation deletions, blocks relation-dependent claims, and can still evaluate claims that only depend on the healthy primary Graph plane. Failed/partial observations never replace the last known-good baseline. This pattern was adapted from QDW's anti-cheat/source-health doctrine and is essential for a change-monitoring service.

## 6. Impact semantics

Impact propagation is deliberately conservative.

- Query membership change affects claims that explicitly declare `query_membership`.
- A field change affects field dependencies on that entity/path.
- A removed relation affects matching relation dependencies.
- Retraction/correction on a depended-on entity escalates to human review.
- No matching dependency means `CURRENT`.

Future versions can add richer typed dependency edges (`GROUNDS`, `USES_AS_PREMISE`, `USES_AS_WARRANT`) from Pāṭala's scholarly review engine without changing the core protocol.

## 7. Resolution semantics

For a computable claim, a proof obligation can be resolved automatically by recomputing against the current snapshot.

For a non-computable claim, the resolution plan requires an evidence artifact and can later be connected to Pāṭala's HumanAttestation / adjudication model.

The key rule is:

> **No obligation is closed solely because an agent says it is fixed.**

## 8. Event history

Every lifecycle transition is appended to a hash-chained JSONL ledger:

```text
analysis.tracked
analysis.verified
obligation.resolved
...
```

Each event binds the previous hash. `verify-ledger` detects mutation of historical entries.

This lightweight portable ledger is the hackathon implementation. Pāṭala/Wiggly's larger architecture can use stronger event stores and Merkle checkpoints without changing the public objects.

## 9. Agent-native design

An optional MCP server exposes:

- `list_tracked_analyses`
- `verify_analysis`
- `list_proof_obligations`
- `verify_ledger`

A persistent agent can therefore treat claim validity as state rather than silently caching an answer forever.

## 10. Scaling path

Hackathon MVP:

```text
local JSON state + bounded API queries
```

Pilot:

```text
Broker / scheduled Graph update
→ queue affected TrackedAnalyses
→ incremental entity/relation refresh
→ impact graph
→ obligations
```

Large institutional deployment:

```text
bulk/BigQuery Graph snapshots
→ columnar normalized state
→ entity/relation change index
→ dependency reverse index
→ event bus
→ institution/agent-specific obligations
```

The public protocol stays the same at each scale.

# Architecture

## The full loop

```
                       OPENAIRE
                          │
              ┌───────────┴───────────┐
              │                       │
        Graph API V3            ScholeXplorer
              │                       │
              └───────────┬───────────┘
                          ▼
                     Normalizer
                          │
              stable identity / relations
                          │
                          ▼
                Canonical Snapshot
                          │
                    JCS + digest
                          │
                          ▼
                   TrackedAnalysis
                          │
                ┌─────────┴─────────┐
                │                   │
           snapshot T₁         snapshot T₂
                │                   │
                └─────────┬─────────┘
                          ▼
                     SemanticDiff
                          │
                          ▼
                 Dependency Matcher
                          │
                    ┌─────┴─────┐
                    │           │
               unaffected     affected
                                │
                                ▼
                          ImpactReport
                                │
                                ▼
                       ProofObligation
                                │
                                ▼
                         Pāṭala Ledger
```

## Future layers

```
Broker
  ↓
automatic change trigger

Crux
  ↓
which premise is decisive?

Scholar Relay
  ↓
which human expertise is required?
```

## Materiality taxonomy

Not all changes are equal:

```
COSMETIC        — formatting, display
IDENTITY        — ORCID added, author resolved
METADATA        — title corrected, date changed
RELATION        — dataset link added/removed
AVAILABILITY    — open access status changed
VERSION         — new dataset version
CORRECTION      — retraction/correction
RETRACTION      — paper retracted
```

Claim policies map materiality to impact:

```
claim depends on DATASET_RELATION
→ dataset relation removal = RECOMPUTE

claim does not depend on AFFILIATION
→ affiliation update = UNAFFECTED
```

## Hard invariants

```
R1. Upstream source change ≠ claim invalidation.
R2. A claim is affected only through an explicit dependency.
R3. Absence in a new snapshot is recorded as absence,
    not automatically interpreted as falsehood.
R4. Pāṭala never claims OpenAIRE invalidated a conclusion;
    Pāṭala reports that an input changed.
R5. Every proof obligation identifies the exact change
    that generated it.
R6. Same snapshots + same dependency graph
    → same ImpactReport.
R7. Historical snapshots/events are append-only.
R8. Machine-generated dependencies are PROPOSED
    until accepted when human authority is required.
```

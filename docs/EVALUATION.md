# Evaluation and anti-theatre plan

A continuous-verification system is dangerous if it merely produces convincing alerts. The evaluation therefore prioritizes *false invalidation* and source-failure behavior.

## Current release proof

The included offline suite verifies:

- deterministic canonical hashing;
- list-order preservation where scholarly order can matter;
- volatile transport fields can be excluded;
- empty result ≠ source failure;
- V3 query construction;
- V4 beta unified filter/select construction;
- ScholeXplorer link normalization;
- Broker subscription adapter behavior;
- entity/field/relation diffing;
- unrelated field change does not trigger relation-only claim;
- source failure never becomes mass deletion;
- relation-ratio computation can flip a conclusion;
- frozen plan receipt binding;
- ledger tamper detection;
- partial ScholeXplorer failure cannot manufacture relation deletion;
- failed verification cannot advance the last known-good snapshot;
- full track → verify → impact → oblige → resolve flow.

Run:

```bash
python -m unittest discover -s tests -v
python scripts/verify_release.py
```

## Release gates

| Gate | Requirement |
|---|---|
| R0 Compile | Every Python module compiles |
| R1 Unit | deterministic core behavior passes |
| R2 Adapter contract | V3/V4/ScholeXplorer/Broker request shapes covered |
| R3 Semantic diff | known fixtures produce exact change classes |
| R4 Impact isolation | unrelated claims remain current |
| R5 Source failure | outage cannot generate deletions |
| R6 Verification | frozen plan + receipt binding passes |
| R7 Integrity | historical ledger mutation is detected |
| R8 E2E | demo produces obligations + automatic resolutions |

## Pilot benchmark

Construct historical pairs from OpenAIRE released snapshots/current Graph states and label downstream claims.

Metrics:

- `change_precision`, `change_recall`;
- `impact_recall` — affected claims found;
- `unaffected_precision` — claims left current were truly unaffected;
- `proof_obligation_precision`;
- `recompute_savings` vs full rerun;
- `source_failure_false_deletion_rate` (target: 0);
- receipt/ledger verification success.

## Adversarial cases to add

1. API timeout.
2. HTTP 429 followed by success.
3. malformed JSON.
4. partial pagination.
5. result ordering only.
6. title punctuation only.
7. author order change (must not be silently normalized away).
8. DOI canonicalization/case difference.
9. entity leaves query because filter-sensitive metadata changes.
10. relation disappears.
11. inferred relation replaced by harvested relation.
12. correction/retraction appears.
13. V4 schema field rename.
14. ScholeXplorer unavailable while Graph V3 succeeds (partial state, not zero relations).
15. tampered receipt artifact.
16. changed resolution criteria under same obligation.

## Definition of “works”

The artifact is not considered proven because the code imports or the demo prints a result. `BUILD_CERTIFICATE.json` records compile/test/E2E commands and artifact hashes for the exact packaged tree.

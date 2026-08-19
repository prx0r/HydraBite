# Reusable Pāṭala Infrastructure

## What already exists

Research CI is an adaptation of pre-existing Pāṭala primitives. That makes the project stronger, not weaker.

| Primitive | Source | What it does |
|-----------|--------|-------------|
| JCS canonicalization + content hashing | `openpatalaproject/patala/hashing.py` | `DigestSet`, `canonical_jcs()`, `semantic_fingerprint()` — three hash types for raw bytes, canonical structured records, semantic fingerprints |
| Append-only event ledger + Merkle checkpoints | `openpatalaproject/patala/events.py` | `EventStore` with cursor-based pagination, checkpoint verification |
| Blast-radius + staleness propagation | `fuck-off/lib/staleness.py` | RKA dependency walking, stale/affected/unaffected classification, rebuild ordering |
| Crux / perturbation analysis | `fuck-off/lib/epistemic.py` | 4-axis Authority + EpistemicEnvelope + perturbation-based load-bearing premise detection |
| Content-addressed run recording | `sanskritbenchy/pipeline/run_recorder.py` | `sha256(gold ‖ code ‖ config) → out_hash`, nanopublication model |
| Staged identity resolution | `openpatalaproject/patala/resolver.py` | R0-R5 (exact → crosswalk → bibliographic → fuzzy → multi-source → adjudication) |
| Schema registry | `openpatalaproject/patala/schema_registry.py` | Immutable, versioned schemas with freeze semantics |
| Review reducer | `fuck-off/lib/review.py` | State machine: AWAITING → REVIEWING → CORRECTION → ALIGNED → HUMAN_OVERRIDE |
| System provenance | `fuck-off/lib/system_provenance.py` | OS audits its own construction (9/9 proof) |

## What needs to be built new

| Module | Lines | Purpose |
|--------|-------|---------|
| `openaire.py` | ~80 | V3 adapter: fetch, normalize, canonicalize |
| `tracked.py` | ~40 | TrackedAnalysis + TrackedClaim dataclasses |
| `diff.py` | ~80 | Semantic diff engine |
| `impact.py` | ~60 | Walk claim deps against diff |
| `obligations.py` | ~30 | ProofObligation generation |
| `ledger.py` | ~40 | Thin wrapper around events.py |
| `cli.py` | ~100 | CLI interface |
| **Total** | **~430** | |

## The philosophy

> Tools don't become truth; their outputs become observations.

This principle from Wiggly becomes: OpenAIRE observations feed into Pāṭala's epistemic state machine. The machine never claims to be more certain than its inputs. Changes upstream produce proof obligations downstream, not silent invalidations.

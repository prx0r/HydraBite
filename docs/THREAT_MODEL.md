# Threat model and anti-theatre rules

## Claim being defended

Iolaus claims only:

> **For transitions covered by a declared verifier, raw executor output cannot create a trusted `HBClaim`; only an authorized PASS receipt can.**

It does not claim the verifier is omniscient.

## Failure modes

### Executor lies or silently fails
**Defense:** output is `HBObservation`, not `HBClaim`. Deterministic external readback can reject it.

### Executor and verifier are the same model
**Defense:** contracts authorize explicit verifier IDs/classes. Judge-facing demo uses deterministic database readback. Human/heuristic verifiers remain possible but visibly weaker classes.

### Receipt tampering
**Defense:** receipt payload binds contract hash, input hash, output hash and evidence hash; Ed25519 signature verification detects modification.

### Receipt signature interpreted as semantic proof
**Defense:** explicitly forbidden. Signature proves issuer/integrity of the receipt envelope. The verifier class and evidence define the bounded semantic claim.

### Fake Hydra integration
**Defense:** certification requires a real graph-node readiness check, Hydra Prometheus marker, OpenCypher roundtrip, and Hydra-native `algo.MSpaths`. There is no mock fallback in `scripts/certify.sh`.

### Unit test adapter mistaken for production store
A tiny `RecordingHydra` exists only in `tests/test_engine_logic.py` to test local Python policy. It is neither imported by production code nor accepted by the live certificate. Live tests are in `tests/integration` and hard-fail without HydraDB.

### Verifier itself is wrong
Out of scope for universal resolution. Iolaus makes the verifier explicit and therefore replaceable/auditable. Stronger future policies can require quorum, independent re-execution, human approval, TEE/ZK evidence, or domain-specific validators.

### Replay / duplicate side effects
The MVP records input hashes but does not yet implement a distributed idempotency lease. Production extension: contract-level idempotency keys and duplicate suppression before executor dispatch.

### Concurrent conflicting claims
The MVP treats claims as append-only evidence objects. It does not implement contradiction adjudication or temporal supersession. Those belong above the atomic verified-transition primitive.

## Honest evidence ladder

From weakest to strongest *for a given claim*, not universally:

1. `HEURISTIC` — LLM/model judgment; useful signal, not deterministic proof.
2. `STRUCTURAL` — schema/shape validation.
3. `HUMAN_APPROVAL` — named human attestation.
4. `DETERMINISTIC_READBACK` — reads external target state and checks postcondition.
5. `DETERMINISTIC_TEST` — reproducible test suite/assertion.
6. `INDEPENDENT_REEXECUTION` — separate implementation reproduces bounded result.
7. `CRYPTOGRAPHIC` — proves a specified computation/attestation, not arbitrary real-world truth.

The ordering is contextual; a human may be the correct authority for subjective approval while a ZK proof cannot prove a semantic business judgment.

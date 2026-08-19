# Testing and validation strategy

## Rule

**Passing local Python tests is not proof of HydraDB integration.**

The repository deliberately separates:

```text
unit/policy verification
from
live HydraDB verification
```

## Layer 1 — static / unit

```bash
./scripts/smoke.sh
```

Checks:
- Python source compiles;
- canonical hash behavior;
- receipt signing/tamper detection;
- contract rendering;
- verifier behavior;
- policy invariant that FAIL evidence does not create a claim;
- unauthorized verifier rejection.

`tests/test_engine_logic.py` contains a tiny recording adapter strictly for policy tests. Production code does not import it.

## Layer 2 — Hydra runtime identity proof

```bash
iolaus prove-hydra --json validation/hydra-proof.json
```

Hard conditions:

1. `/readyz` responds.
2. `/metrics` contains `graph_runtime_ready`.
3. OpenCypher write/read roundtrip succeeds.
4. Hydra-specific native `algo.MSpaths` succeeds.

This is designed to fail against an ordinary fake HTTP service.

## Layer 3 — end-to-end semantic failure tests

`tests/integration/test_verified_transition.py` reproduces:

```text
tool reports success
external state absent
verifier FAIL
no HBClaim
next action BLOCKED
```

and the positive counterpart.

The test does not skip if Hydra is unavailable. The CI live job must start Hydra first.

## Layer 4 — failure-oriented benchmark

```bash
python benchmarks/false_success_bench.py
```

A deterministic sequence of honest, silent-failure and wrong-record executions compares:

```text
naive baseline: tool.success == true → commit
Iolaus: verifier PASS → commit
```

The benchmark is accepted only if Iolaus creates zero false trusted commits and promotes every honest case.

## Layer 5 — full certificate

```bash
./scripts/certify.sh
```

Produces `validation/RUN_CERTIFICATE.json` only after all live gates pass. The certificate hashes the primary evidence files and records the exact Hydra container RepoDigest executed.

## Artifact builder limitation

The environment used to assemble this source pack had Python and the required Python libraries but no Docker, Rust/Cargo, GraphBLAS toolchain or outbound GitHub clone path. Therefore only the static/unit layer was executed there. `validation/LOCAL_VALIDATION.json` records that limitation explicitly instead of fabricating a live certificate.

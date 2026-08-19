# HydraBite — Hack Hydra submission

**Verified state transitions for AI agents.**

HydraDB already gives action-capable agents a strong function-selection loop: register functions as knowledge, decide what to call, execute through an orchestrator, then feed outcomes back so future decisions improve.

HydraBite targets one missing boundary in that loop:

> **A tool saying “success” is not proof that the intended state transition occurred.**

A CRM API can silently fail. A deployment command can exit 0 before the service is healthy. A coding agent can say “fixed” while tests fail. If optimistic outputs are immediately treated as trusted history, future agent decisions learn from false state.

HydraBite changes one rule:

> **No receipt → no trusted transition.**

Every action has a small contract: verified claims it requires, claims it may produce, and the verifier(s) authorized to certify it. Execution results are written to HydraDB only as `SUCCEEDED_UNVERIFIED` observations. An independent verifier then checks the declared postcondition. HydraBite signs and stores the verifier evidence. Only a PASS receipt can create a trusted `HBClaim`, and only those claims can enable downstream actions.

The live demo deliberately uses a lying tool that returns `success=true` without creating the requested CRM record. HydraBite rejects it, creates no trusted claim, and blocks the downstream welcome email. The same action succeeds after a deterministic readback proves the record exists.

The project uses the **HydraDB OSS graph-node directly** via its OpenCypher HTTP API. The anti-cheat certification requires `/readyz`, HydraDB's `graph_runtime_ready` Prometheus marker, a real graph write/read roundtrip, and HydraDB's native `algo.MSpaths` procedure. No mock or hosted memory API can generate the live certificate.

The narrow benchmark adds one metric to Hydra's existing routing/plan metrics: **false-success commit rate**. A naive baseline trusts `success=true`; HydraBite requires the postcondition. The acceptance gate is zero false trusted commits across adversarial semantic-failure cases.

The closest research, such as ToolGate, already shows why pre/postcondition-gated tool state matters. HydraBite's contribution is making that verifier-gated transition a durable, traversable HydraDB primitive at the exact point where agent execution becomes shared state and future learning signal.

Once this primitive exists, better routing, self-healing workflows, certified agent reputation, human/cryptographic verifiers and cost-per-verified-success optimization become downstream graph problems. This submission deliberately builds the prerequisite, not all of them.

# Final integration-agent prompt

You are the final implementation/release agent for **HydraBite — verified state transitions for AI agents on HydraDB**.

## Non-negotiable product claim
Do not turn this into memory infrastructure, a generic router, a large benchmark platform, blockchain middleware or an LLM evaluator.

The one hard problem is:

> Raw tool/agent output must not become trusted HydraDB state until a contract-authorized independent verifier establishes the declared postcondition.

Mantra: **No receipt → no trusted transition.**

## Your job

1. Place this pack in the target Hack Hydra submission repository on a clean branch.
2. Preserve the small graph schema and trusted-state invariant.
3. Start the real HydraDB OSS graph-node using `scripts/start_hydradb.sh`.
4. Fix any OpenCypher compatibility issues against the current exact HydraDB release. Do not work around them with a mock or another database.
5. Run `./scripts/certify.sh` until it produces `validation/RUN_CERTIFICATE.json` with status `PROVEN_LIVE_HYDRADB`.
6. Inspect every generated evidence file and confirm timestamps/digests belong to the current final HEAD.
7. Run the dashboard demo manually and capture a 2-minute video using `judging/DEMO_SCRIPT.md`.
8. Pin the final `HYDRADB_IMAGE` by immutable RepoDigest/tag in release documentation after a successful run.
9. Re-open the research sources in `research/SOURCES.md`; pin exact identifiers for papers still marked for recheck. Do not invent citations.
10. Replace stale Hackathon1/MemoryProof/OpenAIRE material in the target submission repo rather than mixing products.
11. Update README repository URLs, author metadata, screenshots/video links and final commit SHA.
12. Push/upload only after live certification passes.

## Anti-cheat acceptance gates

A final submission is invalid if any are true:
- live Hydra integration is skipped;
- an in-memory/SQLite graph substitutes for HydraDB;
- hosted Hydra Memory/MCP is substituted for OSS graph-node;
- the demo prints success while Hydra writes actually failed;
- `RUN_CERTIFICATE.json` predates final HEAD;
- benchmark results are hand-written instead of generated;
- a receipt signature is described as proving semantic truth;
- executor self-report is accepted as postcondition proof.

## Required commands

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[dev,demo]'
./scripts/certify.sh
uvicorn demo.app:app --port 8080
```

Then independently inspect:

```bash
cat validation/hydra-proof.json
cat validation/false-success-bench.json
cat validation/RUN_CERTIFICATE.json
```

## Required behavioral checks

- Lying `create_customer` returns `success=true` but must become `REJECTED`.
- No customer `HBClaim` may exist after that failure.
- Welcome action must be `BLOCKED` and external email queue untouched.
- Honest customer write must become `VERIFIED` after readback.
- Claim integrity path must resolve through PASS receipt → invocation → contract + observation.
- Welcome action must then become executable and independently VERIFIED.
- Tampering with signed receipt payload must fail signature verification.
- Hydra native probe must include a successful `algo.MSpaths` call.

## Pitch discipline

Use these lines:

> HydraDB already helps agents decide what to do. HydraBite decides when we're allowed to believe it worked.

> A 200 response is an observation, not a verified state transition.

> No receipt → no trusted transition.

> The missing metric is false-success commit rate.

> We did not build every downstream feature. We built the prerequisite that makes them trustworthy.

Be precise about prior work: ToolGate is the closest research neighbor. The novelty is the HydraDB-native durable verified transition integrated into the execution-feedback seam, not claiming verification itself was never studied.

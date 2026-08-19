# Judge FAQ

## Isn't this just ToolGate?
ToolGate is the closest research neighbor and should be credited. Its important idea is Hoare-style pre/postcondition gating of trusted tool state. HydraBite is a deliberately small systems implementation of that trust boundary **as durable HydraDB graph state**, with signed receipts, verifier identities, downstream claim gating, Hydra-native certification, and direct positioning in Hydra's function-routing feedback loop.

## Why does this need a graph database?
One verification decision does not. The value appears as transitions compose. A trusted claim links to its receipt, invocation, contract, verifier and prerequisites. That lineage becomes queryable across long-running multi-agent workflows. Hydra's path procedures can later find proven execution paths without rebuilding lineage from scattered logs.

## Isn't HTTP 200 normally enough?
It proves the server responded successfully at the protocol level. It does not prove the domain postcondition: the intended CRM record, healthy deployment, correct patch, booked meeting, or transferred state actually exists.

## Why not just call the API again after every write?
That is exactly a good deterministic verifier. HydraBite standardizes what happens **around** that readback: authorization, evidence hashing, receipt signing, trusted-state promotion and downstream gating.

## Is the Ed25519 signature the proof?
No. It proves receipt integrity/issuer. The verifier evidence establishes the bounded claim. The verifier class is explicit to prevent cryptographic theatre.

## Why not blockchain?
The MVP does not need consensus or on-chain payments. ERC-8004 is a useful future interoperability target for validation/reputation. The hackathon value is first making verified transitions native to HydraDB.

## What if the verifier lies?
Then the bounded trust model is only as good as that verifier. HydraBite makes this visible rather than hidden. Future contracts can require stronger classes, multiple validators, human approval, independent re-execution, TEE/ZK attestations, or quorum.

## Why not solve routing directly?
Routing is crowded and Hydra already does it. The graph edge label “succeeded” is only useful if it means something. HydraBite solves the prerequisite that makes adaptive routing and reputation materially safer.

## What is the one success criterion?
A semantic failure where the tool says success must **never** create a trusted claim unless the declared verifier also passes.

## How do I know this really used HydraDB?
Run `./scripts/certify.sh`. It refuses to generate `RUN_CERTIFICATE.json` unless the OSS graph-node exposes readiness/metrics, completes an actual OpenCypher roundtrip, and executes HydraDB-native `algo.MSpaths`.

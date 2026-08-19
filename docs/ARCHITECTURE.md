# Architecture

## One responsibility

Iolaus owns the transition:

```text
UNVERIFIED execution output → VERIFIED shared state
```

It does not own semantic function selection, LLM reasoning, application auth, workflow scheduling, or the external system being mutated.

## Components

### `HydraClient`
A thin direct client for HydraDB OSS `graph-node` HTTP/OpenCypher. Its live probe requires a real Hydra-specific native path call.

### `Contract`
Declares:
- verified claims required before execution;
- verified claims the action may produce;
- authorized verifier IDs;
- side-effect/reversibility metadata.

The contract is content-hashed before invocation.

### `IolausEngine.execute`
1. Ensure immutable-ish contract node exists by `(contract_id, contract_hash)`.
2. Query verified prerequisite claims in HydraDB.
3. If missing, return `BLOCKED` without calling the tool.
4. Create `HBInvocation` in HydraDB.
5. Execute the external function.
6. Store the returned JSON as `HBObservation` with `SUCCEEDED_UNVERIFIED` or `EXECUTION_FAILED`.

Crucially, there is no trust promotion here.

### `Verifier`
An independent gate with a stable ID and explicit verifier class. MVP verifier classes distinguish deterministic readback/tests from human, heuristic and cryptographic mechanisms.

### `IolausEngine.verify`
1. Ensure verifier is authorized by the contract.
2. Run verifier against the declared arguments and observed output.
3. Hash the evidence.
4. Construct and Ed25519-sign a receipt payload bound to contract/input/output/evidence hashes.
5. Persist the receipt to HydraDB.
6. On PASS only, create `HBClaim` nodes and their receipt lineage.

## Why append rather than mutate

The MVP intentionally records invocations, observations and receipts as new nodes rather than overwriting a single mutable “status” object. This preserves the evidence path and avoids making “current status” the canonical history.

Multiple receipts can theoretically exist for one invocation. Product policy can later define quorum/precedence rules; the MVP uses one contract-authorized verifier per demo transition.

## Trusted-state query

A precondition is true only when a claim has a PASS receipt:

```cypher
MATCH (c:HBClaim {claim_key: $claim_key})
      -[:VERIFIED_BY]->(r:HBReceipt {verdict: 'PASS'})
RETURN c.claim_key
LIMIT 1
```

A tool's `HBObservation` is never used for this query.

## Future Hydra-native routing

Once the graph accumulates verified transitions, capability edges may include empirical `cost`, `latency`, and verified-success statistics. HydraDB's native bounded path procedures can then search candidate workflows under cost constraints.

That is intentionally downstream of the MVP. The hard prerequisite is ensuring the edge outcome is trustworthy enough to learn from.

## HydraDB identity / mutation compatibility

The inspected HydraDB OSS revision uses integer vertex IDs as mutation identity and documents a deliberately bounded OpenCypher write subset. Iolaus therefore does not assume Neo4j's broader mutation surface.

String domain IDs (`inv_…`, `bite_…`, claim keys, verifier IDs) are mapped to deterministic positive 63-bit vertex IDs with SHA-256 domain separation. The readable string remains a node property.

Vertex upserts use the documented transport batch form:

```cypher
UNWIND $rows AS row
MERGE (n {id: row.vertex})
SET n:HBClaim, n.claim_key = row.claim_key
```

Edges use the documented matched relationship upsert form with a deterministic relationship ID. Every mutation is followed by a **strong readback** before the engine advances. This is intentional: an empty mutation response is not treated as proof that the graph changed.

# Current limitations

HydraBite v0.1 is intentionally an atomic primitive, not a complete agent platform.

- **Verifier quality is external.** HydraBite enforces that a verifier exists and is authorized; it does not magically make a poor verifier correct.
- **One verifier is enough in the MVP.** No quorum, conflicting receipt adjudication or validator reputation yet.
- **Claims are monotonic.** No expiry, supersession, revocation or contradiction semantics are implemented in this one-day build.
- **No distributed idempotency lease.** Input hashes are recorded, but production duplicate-side-effect prevention needs contract-specific idempotency keys/leases.
- **No general planner/router.** HydraDB already owns function selection in the target recipe. Verified historical transitions are designed to become better routing signal later.
- **No blockchain integration.** ERC-8004 is a future interoperability option, not a dependency.
- **No universal semantic proof.** Ed25519 protects receipt integrity. Different verifier classes establish different bounded claims.
- **Demo world is deterministic.** SQLite represents an external target system solely so silent failures have auditable ground truth. It is not used as HydraBite's graph store.

These limits are deliberate scope control. The hackathon claim is only the verified transition boundary.

# Mechanisms Reference — What to Pinch, What to Optimize

*2026-08-19 · Catalog of reusable mechanisms from QDW, sanskritbenchy, fuck-off, and the current Research CI implementation*

---

## Current Research CI Architecture (what each module does)

| Module | Mechanism | What it does | Limitation |
|--------|-----------|-------------|------------|
| `openaire.py` | HTTP client + normalization | Fetches V3 records, normalizes fields | No learning, no adaptation |
| `canonical.py` | JCS-style hashing | Deterministic JSON digest | Stateless, no versioning |
| `diff.py` | Record-level comparison | Compares snapshots, classifies materiality | No temporal tracking, no confidence |
| `impact.py` | Dependency graph walk | Matches changes to claim dependencies | Binary (affected/unaffected), no severity |
| `obligations.py` | Frozen proof obligations | Emits RECOMPUTE/HUMAN_REVIEW | No priority, no cost model |
| `verification.py` | Resolution plan + receipt | Frozen plan → execution → receipt | No learning from outcomes |
| `ledger.py` | Hash-chained event store | Append-only with integrity checks | No Merkle proofs, no signing |
| `mcp_trace.py` | Credential redaction + hashing | Captures MCP tool calls | Manual dependency declaration |
| `service.py` | Orchestrator | Coordinates track/verify/resolve | No scheduling, no prioritization |

---

## Mechanisms to Pinch (from QDW)

### 1. Thompson Sampling Bandit (from `hotswap/persistent.py`)

**What it does:** Each verification route has a Beta(alpha, beta) posterior. After each outcome, alpha increments on success, beta on failure. Thompson sampling draws from the posterior for exploration decisions.

**Why it matters for Research CI:** Currently obligations are RECOMPUTE or HUMAN_REVIEW with no learning. Over time, the system should learn: "verifications that rerun query X tend to succeed" vs "verifications that require human judgment tend to need it."

**Reuse:** Direct import of `PersistentBanditStore` pattern.

### 2. UCB1-style Scheduler (from `scheduler.py`)

**What it does:**
```python
net_value = expected_value * confidence - expected_cost - risk + urgency
allocation_index = mean_utility + exploration * sqrt(log(total) / sample_count)
```

**Why it matters:** Currently all proof obligations have equal priority. Should be prioritized by: downstream blast radius, cost of recomputation, likelihood of actually being stale, urgency.

**Reuse:** The `net_value` + `allocation_index` formula directly.

### 3. Wilson Lower Bound (from `hotswap/stats.py`)

**What it does:** One-sided 95% confidence lower bound for success rates. Used to guard against overconfident low-sample routes.

**Why it matters:** When we say "indicator I5 is CURRENT with 95% confidence," that confidence should account for sample size. A conclusion based on 3 records is less certain than one based on 3000.

### 4. VerificationService Evidence Chain (from `proof/verification_service.py`)

**What it does:** Records git SHA + environment + each command's stdout/stderr hashes + artifact hashes. Later re-verifies without rerunning.

**Why it matters:** Our `verification.py` is simpler. The QDW version is more robust — it re-verifies the entire chain from the receipt alone.

### 5. BuildCertificate (from `proof/certificate_v2.py`)

**What it does:** Binds git SHA + plan hash + artifact set hash + environment hash into a self-verifying certificate. Re-issues on every commit.

**Why it matters:** Our BUILD_CERTIFICATE.json is static. Should be re-issued after every verification run.

### 6. Test Guard AST Analysis (from `proof/test_guard.py`)

**What it does:** Scans test files for fake-green patterns: `assert True`, empty tests, skip/xfail decorators.

**Why it matters:** Our MONITOR CI benchmark could use this to verify its own tests aren't fake-green.

### 7. Work Graph DAG with Leases (from `graph/store.py`)

**What it does:** PENDING → READY → LEASED → RUNNING → VERIFYING → SUCCEEDED. Lease expiration, priority ordering, retry management.

**Why it matters:** Our obligations are flat. Should be a DAG with dependencies between obligations.

### 8. Merkle Sealing (from `ledger/merkle.py` + `events.py`)

**What it does:** Each event hashes previous event. Epochs are sealed into Merkle trees. Inclusion proofs for sparse verification.

**Why it matters:** Our ledger is hash-chained but lacks Merkle proofs. Adding epoch sealing would make verification more efficient.

---

## Mechanisms to Pinch (from sanskritbenchy)

### 9. Content-Addressed Run Recording (from `pipeline/run_recorder.py`)

**What it does:**
```python
run_signature = sha256(gold_hash || code_sha || config_sha)
out_hash = sha256(metrics || raw_outputs)
nanopublication = {assertion, evidence, provenance}
kind = epistemic_kind(DECLARED → OBSERVED → DERIVED → VERIFIED)
```

**Why it matters:** Our proof obligations don't track their epistemic level. Should distinguish: DECLARED (we think it changed) → OBSERVED (we measured it) → DERIVED (we computed impact) → VERIFIED (deterministic gate passed).

### 10. Deterministic Proof Gates (from `pipeline/translation_proof.py`)

**What it does:** 5 constraint checks, no model needed:
- source binding (no hallucination)
- coverage (no dropped content)
- abstention (no source-echoing)
- term consistency (no within-text drift)
- citation grounding (no invented terms)

**Why it matters:** Our verification only checks source status. Should also check: did the recomputation actually produce a different result? Is the new result internally consistent?

### 11. Challenge Set Generation (from `pipeline/sanskrit_mqm.py`)

**What it does:** Deterministic perturbations per error family (negation removal, antonym swapping, subject-object swapping, compound re-ordering).

**Why it matters:** Our attack catalog (`verification/attacks.py`) has 12 cases. Could generate more using this pattern — systematic perturbation factories.

### 12. Tree Search over Strategies (from `pipeline/tree_search.py`)

**What it does:** Best-first search over translation strategies, scored by real computed metric on fixed gold. Anti-theater: score is a REAL number, never LLM opinion.

**Why it matters:** Could apply to "which verification strategy should we use for this obligation?" — search over recomputation approaches, score by actual quality metrics.

### 13. Hypothesis Lab (from `pipeline/hypothesis_lab.py`)

**What it does:** OBSERVE failures → REASON (cluster into error families) → HYPOTHESIZE (generate configs targeting failures) → TEST → KEEP/DISCARD. Closed loop.

**Why it matters:** When our impact predictions are wrong (false positives/negatives), we should learn. Hypothesis lab pattern: "why did we predict wrong? generate better prediction rules."

### 14. Kendall's Tau Meta-Evaluation (from `pipeline/validate_benchmark.py`)

**What it does:** Proves the benchmark is better than existing ones by computing correlation with human judgment.

**Why it matters:** Our MONITOR CI benchmark should validate itself. Are our indicators actually meaningful? Do they correlate with real research intelligence outcomes?

### 15. Epistemic Kind Ladder (DECLARED → OBSERVED → DERIVED → VERIFIED)

**What it does:** Classifies every result by trust level. Only VERIFIED is "real."

**Why it matters:** Our ClaimState has CURRENT/SOURCE_CHANGED/RECOMPUTE/HUMAN_REVIEW but no epistemic level. Should add: how confident are we that this state assessment is correct?

### 16. Multi-Reference Benchmark with Alternative Senses (from `pipeline/benchmark_registry.py`)

**What it does:** Retains multiple valid translations per passage. Doesn't penalize alternative interpretations.

**Why it matters:** An indicator like "OA share" could legitimately be computed slightly differently by different methods. Should track: "this indicator has 3 valid computation methods, 2 agree, 1 differs."

---

## Mechanisms to Pinch (from fuck-off)

### 17. 4-Axis Authority Model (from `lib/epistemic.py`)

**What it does:** Authority across generation, evidence, review, publication axes. Each has a ladder. Ceiling = max across axes. Invariant: projection_ceiling <= parent_ceiling.

**Why it matters:** Our ClaimState is flat. Should be multi-dimensional: "this claim is MACHINE_PROPOSED on evidence axis, NOT_REVIEWED on review axis, PRIVATE on publication axis."

### 18. Herdr Reducer (from `lib/review.py`)

**What it does:** State machine: AWAITING → REVIEWING → CORRECTION → ALIGNED → HUMAN_OVERRIDE. Findings have severity (BLOCKING/NON_BLOCKING). Human can override.

**Why it matters:** Our proof obligations jump from OPEN to RESOLVED. Should have intermediate states with findings.

### 19. Blast-Radius Propagation (from `lib/staleness.py`)

**What it does:** Builds dependency index, walks forward from changes, produces stale set + rebuild order + review queue.

**Why it matters:** Our `impact.py` does this but simpler. The fuck-off version also produces `incremental_rebuild_order` (what to recompute first) and `file_review_queue` (what needs human review).

### 20. MAP-Elites Evolution (from `lib/evolve.py`)

**What it does:** Multi-dimensional fitness (fidelity, coverage, robustness, novelty, cost, latency). Niche functions for diversity. Pareto-dominance for selection.

**Why it matters:** Could evolve verification strategies over time. Which verification approaches are most effective for which types of obligations?

### 21. Misconception Repair Cascade (from `lib/misconception.py`)

**What it does:** When learners get things wrong, compute misconception likelihood (cluster_size, persistence, ambiguity_signal, novice_rate). If above threshold → flag for review. When fixed → blast-radius propagate fix.

**Why it matters:** When our impact predictions are wrong, that's a "misconception" in the dependency model. Should track: "we keep falsely predicting X is affected" → fix the dependency model.

### 22. Wrong-Answer-to-Neighbor (from `lib/education.py`)

**What it does:** Maps wrong answers to known epistemic neighbors. Classifies failure type (rival_proposition, scope_inflation, wrong_technical_sense).

**Why it matters:** When an indicator value changes unexpectedly, classify WHY: "query membership changed" vs "field value changed" vs "relation semantics changed."

### 23. Deterministic Scheduler (from `lib/next_action.py`)

**What it does:** `P(v) = w1*D + w2*B + w3*U + w4*Q + w5*R - w6*C` — deterministic priority formula based on dependency depth, blast radius, urgency, quality, recency, cost.

**Why it matters:** Our obligations have no priority. Should use: `priority = blast_radius * urgency * (1/cost)`.

---

## Optimization Opportunities

### A. Add Confidence/Severity to Impact

Currently: binary (AFFECTED / UNAFFECTED)

Proposed:
```python
class ClaimImpact:
    state: str  # CURRENT, SOURCE_CHANGED, RECOMPUTE, HUMAN_REVIEW
    confidence: float  # 0.0-1.0 (Wilson lower bound)
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    blast_radius: int  # how many downstream objects depend on this
    reasoning: str  # exact dependency path that triggered this
```

### B. Add Priority to Obligations

Currently: flat list

Proposed:
```python
class ProofObligation:
    priority: float  # blast_radius * urgency * (1/cost)
    estimated_cost: float  # time/compute to reverify
    confidence: float  # how sure we are this is needed
    rebuild_order: int  # what to recompute first
```

### C. Add Epistemic Levels to Claims

Currently: flat state

Proposed:
```python
class TrackedClaim:
    state: str  # CURRENT, STALE, etc.
    epistemic_level: str  # DECLARED, OBSERVED, DERIVED, VERIFIED
    authority: dict  # 4-axis authority model
    last_verified: str  # when was this last confirmed
    verification_count: int  # how many times verified
```

### D. Add Learning from Verification Outcomes

Currently: no learning

Proposed: Thompson Sampling bandit over verification routes. After each verification, update posterior:
- success → alpha += 1
- failure → beta += 1

Use for: "should we auto-recompute or route to human?" over time.

### E. Add Merkle Proofs to Ledger

Currently: hash chain

Proposed: Merkle tree with epoch sealing + inclusion proofs. Enables efficient sparse verification without replaying entire history.

### F. Add Deterministic Gate to Verification

Currently: verify source status + check plan

Proposed: After recomputation, run deterministic checks:
- Is the new result internally consistent?
- Does it match expected bounds?
- Is it materially different from the old result?
- If same result, close obligation as NO_CHANGE.

---

## Priority: What to implement first

1. **Wilson confidence** on impact predictions (easy, high value)
2. **Priority scoring** on obligations (easy, high value)
3. **Epistemic levels** on claims (medium, high value)
4. **Deterministic post-verification gates** (medium, high value)
5. **Thompson Sampling** for verification routing (hard, medium value)
6. **MAP-Elites** for strategy evolution (hard, low immediate value)

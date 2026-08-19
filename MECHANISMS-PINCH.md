# Mechanisms Pinchable from Papers + Repos + Crypto

## From ToolGate (2601.04688)

**Mechanism: Hoare-style pre/postcondition contracts for LLM tool calling**

```text
Tool schema
    ↓
precondition check (does current state satisfy requirements?)
    ↓
gate decision (ALLOW / BLOCK)
    ↓
execute tool
    ↓
postcondition check (does result match expected effects?)
    ↓
commit to symbolic state
```

**What to pinch:**
- The precondition/postcondition formalism
- Symbolic state space as typed key-value mapping
- Runtime verification before committing state

**What they DON'T have:**
- No graph database (just in-memory state)
- No path queries
- No persistent execution history
- No routing based on verified outcomes

**Our adaptation:** Store contracts + state in HydraDB graph. Use path procedures for execution traces.

---

## From Contract2Tool (2606.07904)

**Mechanism: Infer tool contracts from metadata, schemas, documentation, and execution traces**

```text
Tool metadata + schemas + docs + execution traces
    ↓
contract inference
    ↓
normalized symbolic contracts (preconditions, effects, risk, cost)
    ↓
causal tool filtering
```

**What to pinch:**
- Contract inference from multiple evidence sources
- Hybrid documentation-and-trace evidence
- Risk level as contract component
- Cost as contract component

**What they DON'T have:**
- No graph storage
- No path queries
- No verified state transitions

**Our adaptation:** Store inferred contracts in HydraDB as Capability nodes.

---

## From Agent Receipts (inchwormz)

**Mechanism: Hash-chained execution receipts with typed trust**

```text
Agent executes
    ↓
receipt event (BLAKE3 + Ed25519)
    ↓
hash chain
    ↓
typed trust (integrity, check outcome, applicability)
    ↓
Beta-Binomial calibration
    ↓
withheld-by-default Reliability Index
```

**What to pinch:**
- Hash-chained receipts
- Typed trust levels
- Beta-Binomial calibration
- Withheld-by-default (don't give scores until sample size is large enough)

**What they DON'T have:**
- No graph database
- No pre/postcondition gates
- No SATISFIES edges
- No path procedures

**Our adaptation:** Store receipts as HydraDB Receipt nodes. Create SATISFIES edges after verification.

---

## From 1inch / UniswapX (crypto routers)

**Mechanism: Multi-path swap routing with cost optimization**

```text
Token A → Token B
    ↓
find all possible routes (direct, multi-hop, NLP)
    ↓
for each route:
    calculate: gas cost + slippage + fee
    ↓
select cheapest route
    ↓
execute
```

**What to pinch:**
- Multi-path exploration
- Cost optimization across routes
- Slippage/fee modeling
- Fallback routes

**What they DON'T have:**
- No verification of execution success
- No pre/postconditions
- No graph database

**Our adaptation:** Use similar multi-path exploration but add verification gates. CPVS = cost / P(verified success).

---

## From LiteLLM (★56K)

**Mechanism: Unified LLM routing with fallbacks, circuit breakers, cost tracking**

```text
Request → model selection → fallback chain → cost tracking → health monitoring
```

**What to pinch:**
- Fallback chains
- Circuit breakers
- Cost tracking per request
- Health monitoring per provider

**What they DON'T have:**
- No pre/postconditions
- No verification of output quality
- No graph storage

**Our adaptation:** Use LiteLLM for provider selection, add HydraBite verification on top.

---

## From opencode-hive

**Mechanism: Cost-aware model routing with specialist delegation**

```text"
Orchestrator reads request
    ↓
determines domain (python, go, ops, etc.)
    ↓
fans out to specialists
    ↓
each specialist uses appropriate model tier
```

**What to pinch:**
- Domain-based routing
- Parallel specialist execution
- Model tier selection per task type

**What they DON'T have:**
- No verification
- No graph storage
- No pre/postconditions

---

## From QDW HotSwap (our own code)

**Mechanism: Pareto-frontier route selection with bandit learning**

```text"
Task → candidate routes → bandit assessment → Pareto frontier → execution
    ↓
result → update bandit posterior
    ↓
next task uses updated posteriors
```

**What to pinch:**
- Bandit learning (Thompson sampling)
- Pareto-frontier selection
- Quota shadow pricing
- Unknown ≠ average

---

## From Dell Router (our own code)

**Mechanism: 3-stage cascade with CPVS**

```
Stage 1: Classify task
Stage 2: Route to provider (CPVS optimization)
Stage 3: Escalate if needed
```

**What to pinch:**
- CPVS = cost / P(verified success)
- Shadow pricing for scarce resources
- Cascade fallback

---

## The synthesis: what HydraBite should steal

| From | Mechanism | How we adapt |
|------|-----------|-------------|
| **ToolGate** | Hoare pre/postconditions | Store contracts in HydraDB graph |
| **Contract2Tool** | Contract inference from traces | Infer contracts, store as Capability nodes |
| **Agent Receipts** | Hash-chained receipts, typed trust | Store receipts as HydraDB Receipt nodes |
| **1inch/UniswapX** | Multi-path routing + cost optimization | Add verification gates to routing |
| **LiteLLM** | Fallback chains, circuit breakers | Use for provider selection + add verification |
| **opencode-hive** | Domain-based specialist routing | Route to verified specialists |
| **QDW HotSwap** | Bandit learning, Pareto-frontier | Learn from verified outcomes only |
| **Dell Router** | CPVS, shadow pricing | Core optimization criterion |

## What's genuinely novel in HydraBite

1. **Graph-native** — all of the above stored in HydraDB as nodes/edges
2. **Pre + post** — check BEFORE and AFTER (ToolGate only does post)
3. **SATISFIES edges** — only created after verification
4. **Path procedures** — query execution traces via Cypher
5. **CPVS optimization** — route to verified outcomes, not just attempts
6. **HydraDB integration** — leverages sponsor's own infrastructure

## The one-liner

> **HydraBite combines ToolGate's pre/postconditions, Agent Receipts' typed trust, and HydraDB's graph into a single verified state transition system.**

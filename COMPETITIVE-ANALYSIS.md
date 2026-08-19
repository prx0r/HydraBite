# Competitive Analysis — What HydraDB already has vs what we build

## What HydraDB provides (from docs)

| Feature | Status |
|---------|--------|
| Knowledge ingestion (PDFs, Slack, Notion) | ✅ Done |
| Memory ingestion (preferences, traits) | ✅ Done |
| Hybrid search (semantic + BM25) | ✅ Done |
| Graph context (entity/relation triplets) | ✅ Done |
| Forceful relations (memory-to-memory links) | ✅ Done |
| Feedback loop (agent reports bad queries) | ✅ Done |
| AI Chief of Staff (function selection) | ✅ Cookbook |
| Multi-step reasoning | ✅ Cookbook |
| Self-improving from execution | ✅ Cookbook |
| Multi-tenant isolation | ✅ Done |

## What HydraDB does NOT provide

| Gap | Why it matters |
|-----|---------------|
| Verification of agent actions | No pre/postcondition checking |
| Receipts | No formal proof of execution |
| Capability graph | No typed tool/capability nodes |
| Precondition gates | No pre-execution validation |
| Postcondition verification | No post-execution validation |
| Trusted state transitions | No distinction between observed and verified |

## Competitor analysis

| Competitor | Focus | Overlap | Our differentiation |
|------------|-------|---------|-------------------|
| **Agent Receipts** (★2) | Hash-chained execution receipts | HIGH — both verify actions | We're graph-native; they're standalone |
| **agent-spec** (★445) | Intent → task contracts → verification | MEDIUM — code, not agent actions | They verify code; we verify actions |
| **Semantic Agent** | Policy-bound verified execution | MEDIUM — similar concept | Semantic-specific; we're HydraDB-native |
| **FactoryGate** | Structural policy guardrails for CI/CD | LOW — code structure | Different domain |
| **hydradb-zisk-receipts** | Private context receipts with ZK | LOW — privacy, not verification | Different goal |

## Key differentiation

**Agent Receipts** is the closest competitor. But:

1. Standalone system, not graph-native
2. Doesn't use HydraDB's graph capabilities
3. Doesn't enable routing based on verified outcomes
4. No pre/postcondition gates
5. No SATISFIES edges in a graph
6. No path procedures for execution traces

**HydraBite adds:**
- Graph-native (HydraDB as canonical state store)
- Pre/postcondition gates (check BEFORE and AFTER)
- SATISFIES edges enable routing, self-healing, auditability
- Path procedures for execution trace queries
- Verifiers as first-class graph nodes

**The pitch:**

> Agent Receipts is a verification tool.
> HydraBite is verification as a graph primitive that enables routing, self-healing, and auditability.

## What's already built in our repos

| Component | Source | Reuse |
|-----------|--------|-------|
| Bandit learning | QDW HotSwap | ✅ Route optimization |
| CPVS routing | Dell | ✅ Cost per verified success |
| Beta posteriors | Forge | ✅ Verified success tracking |
| Completion contracts | Minge Farm | ✅ Deterministic verification gates |
| Path planner | HydraRoute | ✅ BFS over capability graph |
| CoverageDimension | Wiggly | ✅ What we don't know yet |
| Proof obligations | Research CI | ✅ What needs re-verification |

## Sources stolen from

| Source | What we take |
|--------|-------------|
| ToolGate (2026) | Pre/postcondition contracts for tool execution |
| HyperAgent (2026) | Schemas as graph nodes, tools as state transitions |
| VPR (2026) | Learn only from grounded verifier signals |
| ERC-8004 | Portable agent identity and validation receipts |
| Agent Receipts | Hash-chained receipts, typed trust, Beta-Binomial calibration |
| Contract2Tool | Causal pre/postconditions for tools |

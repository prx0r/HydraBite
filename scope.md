# Scope — Current Best Guidance

**Date:** 2026-08-19
**Purpose:** Definitive direction for Hack Hydra

---

## Core thesis

> **An agent saying "the tool succeeded" is not evidence that the world is now in the state the agent thinks it is. HydraBite only lets verified outputs enter trusted graph state.**

## The one hard problem

> **Can an agent safely commit a tool result to shared state?**

Nothing broader. Nothing vaguer.

## HydraBite — verified state transitions for AI agents

```text
HydraDB chooses action
        ↓
precondition gate
        ↓
execute
        ↓
UNVERIFIED OBSERVATION
        ↓
postcondition / verifier
      ↙       ↘
  REJECT      PASS
               ↓
        VERIFIED BITE
               ↓
       trusted graph state
```

**No receipt → no trusted transition.**

## What HydraBite is NOT

- Not a router
- Not memory
- Not a benchmark
- Not a chatbot
- Not "another agent framework"

## What HydraBite IS

An **epistemic commit boundary** for agentic software.

## The Bite data model

```json
{
  "bite_id": "bite_...",
  "capability_id": "create_jira_ticket",
  "contract_hash": "sha256:...",
  "input_hash": "sha256:...",
  "output_hash": "sha256:...",
  "executor": "agent_A",
  "status": "VERIFIED",
  "verifier": "jira_readback_v1",
  "verifier_class": "DETERMINATIVE_POSTCONDITION",
  "receipt_hash": "sha256:...",
  "cost_usd": 0.004,
  "started_at": "...",
  "verified_at": "..."
}
```

## Verifier types

| Verifier | What it proves |
|----------|---------------|
| `json_schema` | structurally valid output |
| `pytest` | specified tests pass |
| `database_postcondition` | target record exists |
| `API_readback` | side effect occurred |
| `hash_match` | artifact unchanged |
| `human_signature` | person approved |
| `reexecution` | independent implementation agreed |
| `zk_receipt` | deterministic computation ran |
| `llm_judge` | heuristic semantic approval only |

## HydraDB graph model

```text
(:Schema)
(:Capability)
(:Invocation)
(:Artifact)
(:Verifier)
(:Receipt)

Capability -[:REQUIRES]-> Schema
Capability -[:PRODUCES]-> Schema
Invocation -[:USES]-> Capability
Invocation -[:CONSUMED]-> Artifact
Invocation -[:OBSERVED]-> Artifact
Receipt -[:VERIFIES]-> Invocation
Receipt -[:ISSUED_BY]-> Verifier
Artifact -[:SATISFIES]-> Schema
```

**Key invariant:** `SATISFIES` is only created after verification.

## What this unlocks

```
verified transitions
    ↓
reliable routing (cheapest path to verified goal)
    ↓
self-healing workflows (retry with different verifier)
    ↓
agent markets (reputation from verified outcomes)
    ↓
auditability (complete execution provenance)
```

## Demo (90 seconds)

1. Agent calls create_customer_record → "success"
2. HydraBite: SUCCEEDED_UNVERIFIED
3. Verifier queries DB → record doesn't exist → REJECTED
4. Agent calls again → verifier finds record → VERIFIED
5. Receipt appears in graph
6. Next agent asks "can I send email?" → precondition met → ALLOWED

## What's already built in our repos

| Component | Source | Status |
|-----------|--------|--------|
| Bandit learning | QDW HotSwap | ✅ |
| CPVS routing | Dell | ✅ |
| Beta posteriors | Forge | ✅ |
| Completion contracts | Minge Farm | ✅ |
| Path planner | HydraRoute | ✅ |
| Capability graph | HydraRoute schema | ✅ |

## Build plan (1 day)

1. HydraDB connection + schema (1h)
2. Bite data model + ingestion (1h)
3. Precondition/postcondition gates (2h)
4. Verifier implementations (2h)
5. Demo with 3 cases (2h)
6. README + submission (1h)

**Total: ~9 hours**

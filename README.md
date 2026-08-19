# Iolaus

**Verified state transitions for AI agents on HydraDB.**

> No receipt → no trusted transition.

An agent returning `success: true` is an **observation**, not proof that the world changed as intended. Iolaus puts one small verification boundary between tool execution and shared agent state:

```
Agent proposes action
              ↓
        precondition gate
              ↓
           execute tool
              ↓
    SUCCEEDED_UNVERIFIED
              ↓
   independent verifier reads state
         ↙            ↘
     REJECTED        PASS
                       ↓
               signed receipt
                       ↓
              VERIFIED claim
```

**The agent cannot mark its own work successful.** Downstream actions consume only verified claims, never raw tool output.

---

## The demo

```
1. Tool lies (returns success:true, writes nothing)
   → verifier reads DB, record absent
   → FAIL receipt, no trusted claim

2. Agent tries downstream action
   → BLOCKED: requires verified claim

3. Tool honest (writes real record)
   → verifier reads DB, record exists
   → PASS receipt, claim created

4. Agent tries downstream action
   → ALLOWED
```

---

## How it works

- Tool executes → `SUCCEEDED_UNVERIFIED`
- Independent verifier reads actual state
- PASS → signed receipt → `VERIFIED` claim
- FAIL → no claim → downstream blocked

---

## Why HydraDB

HydraDB stores the trusted state, invocation lineage, receipts and claims in its graph. Verification uses real OpenCypher queries and HydraDB's native algorithms.

---

## Quick start

```bash
pip install -e '.[dev]'
pytest tests/
python -m iolaus.cli demo
```

## License

MIT

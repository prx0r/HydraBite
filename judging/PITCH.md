# Pitch

## 20 seconds

HydraDB already helps agents decide what action to take. **HydraBite answers the next question: when are we allowed to believe the action worked?** Tool output enters HydraDB as an observation, not truth. An independent verifier checks the declared postcondition; only a PASS receipt creates trusted graph state. **No receipt, no trusted transition.**

## 60 seconds

A tool returning `success=true` can still fail semantically. The CRM record might not exist. The deployment might be unhealthy. The coding agent might not have fixed the test.

That is dangerous for an AI Chief of Staff because execution outcomes become future routing and memory signal.

HydraBite adds one commit boundary. Every action declares the verified state it requires, the state it claims to produce, and who is allowed to verify it. The tool runs, but its result is stored only as `SUCCEEDED_UNVERIFIED`. Then an independent verifier reads the actual target state. If verification fails, HydraBite stores the failure receipt and creates no trusted claim. Downstream actions stay blocked. If it passes, HydraBite signs a receipt and promotes only that bounded claim into trusted HydraDB state.

The demo uses a tool that literally lies: it says the customer was created while writing nothing. HydraBite catches it. Then the honest call passes, and the downstream email becomes executable.

The missing metric is **false-success commit rate**. Hydra already optimizes function selection; HydraBite makes the outcome edges trustworthy enough to learn from.

## 3-minute narrative

### 0:00 — problem
“Hydra's Chief of Staff can choose and chain actions. Here is the dangerous line in every agent orchestrator: `result = tool(); log(result); learn(result)`. A 200 response is not the world state.”

### 0:30 — primitive
“HydraBite inserts exactly one state machine: `UNVERIFIED → PASS receipt → TRUSTED`, or `UNVERIFIED → FAIL → REJECTED`. The executor is never its own verifier.”

### 1:00 — demo
Run lying customer tool. Show `success=true` and `SUCCEEDED_UNVERIFIED`. Run CRM readback: absent → FAIL. Try welcome email: BLOCKED.

Run honest customer tool. Readback passes. Show receipt hash and graph claim. Run welcome email: now VERIFIED.

### 2:00 — Hydra native
Show `hydrabite prove-hydra`: readiness, metrics marker, OpenCypher write/read, `algo.MSpaths`. “The trusted graph is HydraDB itself. There is no mock path in certification.”

### 2:25 — why now / frontier
“ToolGate and related research show contract-gated tool state is the right direction; receipt and validation standards show how to attest bounded execution. HydraBite puts that boundary directly into Hydra's action graph.”

### 2:45 — unlock
“Once every successful transition means verified success, Hydra can route on cost per verified outcome, retry semantic failures, chain only proven predecessor states, and build agent reputation from receipts. We did not build all of that. We built the prerequisite.”

### Close
**“HydraDB decides what an agent should do. HydraBite makes sure the graph only learns from what actually happened.”**

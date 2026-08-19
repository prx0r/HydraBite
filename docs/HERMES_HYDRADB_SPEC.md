# Spec: Hermes × HydraDB Full Agentic Integration

*Implement the HydraDB Chief of Staff cookbook with Hermes as the LLM, HydraDB as the graph, and Aletheia as the verification layer.*

---

## Architecture

```
USER (natural language task)
         │
         ▼
    HERMES (LLM)
    ├── understands intent
    ├── extracts parameters
    ├── plans multi-step execution
    │
    ▼
    HYDRADB (graph)
    ├── function knowledge objects
    ├── user preference memory
    ├── execution history
    └── learning signals
         │
         ▼
    IOLAUS (verification)
    ├── precondition check
    ├── tool execution
    ├── independent readback
    ├── signed receipt
    └── trusted state promotion
         │
         ▼
    EXTERNAL APIS (real actions)
    ├── CRM (customers)
    ├── Calendar (events)
    ├── Slack (messages)
    ├── GitHub (repos)
    └── etc.
```

## Components

### 1. HydraDB Graph Schema

```cypher
// Function knowledge objects
(:Function {
  id: string,
  name: string,
  description: string,
  schema_json: string,
  oauth_provider: string,
  collections: [string],
  side_effects: string,
  deprecated: boolean
})

// User preference memory
(:UserMemory {
  user_id: string,
  text: string,
  inferred: boolean,
  created_at: timestamp
})

// Execution history
(:Execution {
  id: string,
  user_id: string,
  function_id: string,
  task: string,
  outcome: string,  // success | failure | timeout | user_rejected
  latency_ms: int,
  receipt_hash: string,
  created_at: timestamp
})

// Verified claims
(:VerifiedClaim {
  claim_key: string,
  receipt_hash: string,
  verifier_id: string,
  trust: string,  // VERIFIED | UNVERIFIED
  created_at: timestamp
})

// Relationships
(user)-[:PREFERS]->(memory)
(execution)-[:USED_FUNCTION]->(function)
(execution)-[:FOR_USER]->(user)
(claim)-[:VERIFIED_BY]->(execution)
(execution)-[:VERIFIED_BY]->(receipt)
```

### 2. Hermes Integration

Hermes provides:
- Natural language understanding
- Parameter extraction from task descriptions
- Multi-step plan generation
- Model routing (Haiku → Sonnet → Opus → human)

Hermes does NOT provide:
- Graph storage (that's HydraDB)
- Function execution (that's the registry)
- Verification (that's Iolaus)
- Learning signal (that's HydraDB memory)

### 3. The Full Loop

```
USER: "Book a meeting with Alice next Tuesday"

HERMES:
  intent: create_calendar_event
  params: {attendee: "alice", date: "next Tuesday"}
  confidence: 0.95

HYDRADB:
  match: create_calendar_event
  preconditions: none required
  function schema: {...}
  user preferences: "Sarah prefers calendar, not email"

IOLAUS:
  precondition check: PASS (no verified claims required)
  tool execution: google_calendar API
  independent readback: event exists in calendar
  receipt: PASS (Ed25519 signed)
  trusted state: VERIFIED

HYDRADB (feedback):
  execution logged: success
  user preference updated: "Sarah uses calendar for meetings"
```

### 4. Fault Detection (what Iolaus adds)

```
TOOL SAYS: success=true
VERIFIER READS: event does NOT exist
VERDICT: FAIL
TRUSTED STATE: not created
DOWNSTREAM: blocked

vs

TOOL SAYS: success=true
VERIFIER READS: event exists
VERDICT: PASS
TRUSTED STATE: VERIFIED
DOWNSTREAM: allowed
```

### 5. Learning Loop

```
EXECUTION SUCCESS → positive memory in HydraDB
EXECUTION FAILURE → negative memory in HydraDB
USER REJECTED → correction memory in HydraDB

HydraDB uses these signals for:
  - function routing (which function for which task type)
  - user personalization (which channels each user prefers)
  - failure avoidance (which functions tend to fail)
```

## Benchmark

The existing benchmark tests 8 cookbook-derived failure scenarios:
1. Silent CRM write
2. False-green deployment
3. Unsafe multi-step cascade
4. False human handoff
5. Accepted-but-not-indexed ingestion
6. Zero-evidence financial answer
7. Wrong-quarter financial evidence
8. Proactive competitive briefing

Each scenario is tested with 1,000 paired trials (baseline vs Iolaus).

## Files

| File | Purpose |
|------|---------|
| `crates/iolaus-core/` | State machine, receipts, hashing |
| `crates/iolaus-hydra/` | HydraDB HTTP client |
| `crates/iolaus-bench/` | Benchmark harness + Hermes integration |
| `crates/iolaus-demo/` | Web demo (baseline vs verified) |
| `fixtures/hydradb/` | Test data (43 nodes, 19 edges, 13 functions) |
| `scripts/` | Build, start, test scripts |
| `benchmarks/` | Failure scenarios |

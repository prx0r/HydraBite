# Mechanisms Mined from Vision Docs

## Most relevant for Hack Hydra (Memory + Context Retrieval)

### 1. Four-Layer Identity Model (from newbuild1)
```
IDENTITY    ≠ CONTENT    ≠ INTERPRETATION    ≠ REPRESENTATION
UUIDv7      ≠ bytes      ≠ belief            ≠ API response
```
**Application:** Every memory in HydraDB should have 4 separate identities. This is the Eigenius pattern formalized.

### 2. CoverageDimension as epistemic state (from patalapath2)
```
state + confidence + evidence_count + last_checked + search_protocol + next_action
```
**Application:** Not "is this memory complete?" but "what don't we know yet, and what would improve it?"

### 3. Scholarly Contribution Packet (from commentarialgraph)
```
questions answered, claims made, interpretations proposed,
evidence used, arguments, disagreements, open questions
```
**Application:** Every memory should carry its contribution context, not just the fact.

### 4. Blast Radius via dependency graph (from ideastrends)
```
observation → claim → plan → recommendation
       ↓
one changes → walk DEPENDS_ON edges → invalidate downstream
```
**Application:** The core MemoryCI mechanism.

### 5. Temporal belief tracking (from patalapath2)
```
t1: "deadline = September 1"
t2: "deadline = August 24"
→ plan from t1 is stale
→ recommendation from t1 needs re-verification
```
**Application:** Track when facts were true, detect temporal contradictions.

### 6. Evidence-backed recall (from scholarproof)
```
"Scholar X interprets A as B.
 Scholar Y objects because C.
 The disagreement turns on crux E.
 Here is the evidence for each."
```
**Application:** Every recalled memory comes with its source chain.

### 7. Self-healing via MELD pattern (from arxiv research)
```
status CRDT: insert | merge | relate | conflict | reject
→ reconverges after partitions
→ never silently discards contradictions
```
**Application:** When memories conflict, preserve both and mark for adjudication.

### 8. Verification-gated updates (from scholarproof)
```
human verification → signed attestation → Merkle checkpoint
```
**Application:** High-stakes memory changes require human confirmation.

### 9. WorkCoverage as frontier (from patalapath2)
```
identity: RESOLVED | UNRESOLVED
source: ETEXT | MANUSCRIPT | NONE
coverage: FULL | PARTIAL | UNKNOWN
next_action: "query NAK/NGMPP"
```
**Application:** Not just "what do we know?" but "what should we look for next?"

### 10. Proof obligations (from scholarproof)
```
OBLIGATION: re-verify claim X because source Y changed
ACTION: deterministic recompute OR human adjudication
STATUS: OPEN → IN_PROGRESS → RESOLVED
```
**Application:** The output of blast-radius analysis.

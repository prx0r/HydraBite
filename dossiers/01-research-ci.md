# Dossier 1: Pāṭala Research CI

**Status:** #1 pick for OpenAIRE AI Hackathon
**Score:** 9.2/10
**Category:** Continuous verification for research built on evolving scholarly graphs

---

## TL;DR

OpenAIRE makes open scholarly intelligence queryable by agents. Pāṭala Research CI makes conclusions derived from that intelligence continuously verifiable.

When the OpenAIRE Graph changes (records added/removed/modified, relations invalidated), Pāṭala tells you which of your downstream research conclusions are now stale, why, and what needs re-verification.

---

## The Problem

A researcher queries OpenAIRE, builds an analysis, publishes a conclusion. Three months later, OpenAIRE removes 318.7M redundant relations and 1.05M invalid funding links. The analysis depends on some of those links. Nobody tells the researcher. The conclusion is now wrong and nobody knows.

OpenAIRE provides:
- What the graph contains now
- What changed globally in each release
- Stable 6-month snapshots for reproducibility

OpenAIRE does NOT provide:
- "Your specific analysis depended on records that changed"
- "These downstream conclusions are now stale"
- "These claims need re-verification"

---

## The Product

### Core loop

```
TRACK → SNAPSHOT → DETECT → IMPACT → OBLIGE
```

1. **TRACK**: Register a research analysis against OpenAIRE (query + filters + timestamp)
2. **SNAPSHOT**: Fetch results, canonicalize records, compute content digest, store
3. **DETECT**: When new OpenAIRE state arrives, compute semantic diff against snapshot
4. **IMPACT**: Walk claim dependencies, identify affected conclusions
5. **OBLIGE**: Emit machine-readable proof obligations for re-verification

### Architecture

```
              OPENAIRE
                  │
      Graph API / ScholeXplorer
                  │
                  ▼
             TRACKED QUERY
                  │
           canonical result
                  │
          content digest
                  │
                  ▼
            PĀṬALA SNAPSHOT
                  │
                  ▼
             new Graph release
                  │
                  ▼
              rerun query
                  │
                  ▼
            SEMANTIC DIFF
                  │
        ┌─────────┼──────────┐
        ▼         ▼          ▼
     entity     field     relation
     added     changed    changed
        │         │          │
        └─────────┼──────────┘
                  ▼
             IMPACT GRAPH
                  │
       "what depended on this?"
                  │
          ┌───────┴────────┐
          ▼                ▼
     unaffected          affected
                           │
                           ▼
                   PROOF OBLIGATION
```

### Data model

```python
@dataclass
class TrackedAnalysis:
    id: str                          # "analysis:open-software-availability"
    query: dict                      # OpenAIRE V3 query params
    source_provider: str             # "openaire"
    source_api: str                  # "v3"
    observed_at: str                 # ISO timestamp
    results: list[str]               # entity IDs
    graph_version: str | None        # OpenAIRE version if known
    input_digest: str                # sha512 of canonicalized results
    claims: list[str]                # IDs of dependent claims

@dataclass
class TrackedClaim:
    id: str                          # "claim:17"
    text: str                        # human-readable
    dependencies: list[str]          # entity/relation IDs this depends on
    state: ClaimState                # CURRENT | STALE | SOURCE_CHANGED | ...

@dataclass
class SemanticDiff:
    analysis_id: str
    old_digest: str
    new_digest: str
    records_added: list[str]
    records_removed: list[str]
    fields_changed: list[FieldChange]
    relations_added: list[Relation]
    relations_removed: list[Relation]

@dataclass
class ImpactReport:
    analysis_id: str
    diff: SemanticDiff
    claims_unaffected: list[str]
    claims_stale: list[str]
    claims_recompute: list[str]

@dataclass
class ProofObligation:
    id: str
    claim_id: str
    reason: str                      # "relation removed", "field changed", ...
    evidence: dict                   # what changed
    action: str                      # "RECOMPUTE" | "HUMAN_REVIEW"
```

### CLI

```bash
# Track an analysis
patala track \
  --name "open-software-availability" \
  --query "type:software,from_publication_year:2024" \
  --entity research-products

# Verify against current state
patala verify analysis:open-software-availability

# Output:
# SOURCE CHANGED
# Tracked records:            81
# Unchanged:                  67
# Added:                       9
# Removed:                     2
# Metadata changed:            3
# Relations changed:           7
#
# IMPACT
# claim:17       STALE
# claim:18       UNAFFECTED
# claim:19       RECOMPUTE
#
# PROOF OBLIGATIONS
# PO-17  relation B→software:Y removed
# PO-19  author affiliation changed

# View event log
patala log

# Show impact for a specific change
patala impact --change <diff-id>
```

### API

```
POST   /v1/analyses              # register tracked analysis
GET    /v1/analyses              # list tracked analyses
GET    /v1/analyses/{id}         # get analysis details
POST   /v1/analyses/{id}/verify  # trigger verification
GET    /v1/analyses/{id}/diff    # get semantic diff
GET    /v1/analyses/{id}/impact  # get impact report
POST   /v1/claims                # register a claim with dependencies
GET    /v1/proof-obligations     # list pending proof obligations
GET    /v1/log                   # event ledger
```

---

## Reusable from existing code

| Component | Source | What to reuse |
|-----------|--------|---------------|
| JCS canonicalization | `openpatalaproject/patala/hashing.py` | `DigestSet`, `canonical_jcs()`, `semantic_fingerprint()` |
| Event ledger | `openpatalaproject/patala/events.py` | `EventStore`, Merkle checkpoints |
| Blast-radius / staleness | `fuck-off/lib/staleness.py` | RKA dependency walking, stale/affected/unaffected classification |
| Claim model | `fuck-off/lib/epistemic.py` | `EpistemicEnvelope`, 4-axis Authority |
| Content-addressed runs | `sanskritbenchy/pipeline/run_recorder.py` | `sha256(gold ‖ code ‖ config)` pattern |
| OpenAIRE client | `hackathon1/explore_api.py` | V3/V4 API calls |

## New code needed (~300 lines)

1. `openaire.py` — V3 adapter (fetch, normalize, canonicalize)
2. `tracked.py` — TrackedAnalysis + TrackedClaim dataclasses
3. `diff.py` — Semantic diff engine (~80 lines)
4. `impact.py` — Walk claim deps against diff (~60 lines)
5. `cli.py` — CLI wrapper (~100 lines)

---

## Demo script

```bash
# 1. Track an analysis
patala track \
  --name "sanskrit-nlp-software" \
  --search "Sanskrit NLP" \
  --type software

# Shows: 14 software products tracked, digest sha512:abc123...

# 2. Wait for OpenAIRE update (or use simulated update)

# 3. Verify
patala verify analysis:sanskrit-nlp-software

# Shows:
# GRAPH CHANGES
# 2 records added, 1 relation removed, 3 fields changed
#
# IMPACT
# claim:1 "Open Sanskrit NLP tools exist" → UNAFFECTED
# claim:2 "Most have linked datasets" → STALE (relation removed)
# claim:3 "Python dominates" → RECOMPUTE (new records may change proportion)
#
# PROOF OBLIGATIONS
# PO-2: Re-evaluate "most have linked datasets"
#        because product:B→dataset:D relation was removed

# 4. View event log
patala log

# Shows append-only ledger of track/verify/diff/obligation events
```

---

## Why this wins

1. **Genuinely novel**: No existing tool does OpenAIRE analysis → claim dependency → change → impact → proof obligation
2. **OpenAIRE-native**: Uses their V3 API, references their releases, works with their 6-month snapshots
3. **Built on proven primitives**: Event ledger, content hashing, blast-radius propagation already tested (97 experiments, 52 kernels)
4. **Real problem**: OpenAIRE's Aug 2026 release removed 318.7M relations — any analysis depending on those is now wrong
5. **Reusable**: Other researchers can track their own analyses against any evolving graph
6. **Honest**: Doesn't try to compete with OpenAIRE's data infrastructure

---

## Files to create

```
hackathon1/
├── patala_research_ci/
│   ├── __init__.py
│   ├── openaire.py          # V3 adapter
│   ├── tracked.py           # TrackedAnalysis, TrackedClaim
│   ├── diff.py              # Semantic diff engine
│   ├── impact.py            # Dependency walker
│   ├── ledger.py            # Event store (thin wrapper)
│   ├── cli.py               # CLI interface
│   └── api.py               # FastAPI (stretch)
├── data/
│   ├── tracked/             # Saved analysis snapshots
│   └── claims/              # Claim definitions
├── fixtures/                # Before/after OpenAIRE examples
├── tests/
│   └── test_diff.py
└── README.md
```

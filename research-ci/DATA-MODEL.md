# Data Model

## TrackedAnalysis

```json
{
  "analysis_id": "analysis:open-software-2026",
  "title": "Open research software in agentic AI",
  "source": {
    "provider": "openaire",
    "api": "v3"
  },
  "query": {
    "entity": "research-products",
    "search": "agentic AI",
    "filters": {
      "type": "software"
    }
  },
  "observed_at": "2026-08-19T...",
  "source_version": "11.3.0",
  "result_ids": [],
  "snapshot_digest": "sha512:...",
  "claims": [
    "claim:software-growth",
    "claim:dataset-linkage"
  ]
}
```

## TrackedClaim

```json
{
  "claim_id": "claim:dataset-linkage",
  "text": "Most sampled software outputs have linked datasets.",
  "dependencies": [
    {
      "kind": "entity",
      "ref": "openaire:..."
    },
    {
      "kind": "relation",
      "source": "openaire:...",
      "predicate": "IsRelatedTo",
      "target": "doi:..."
    }
  ],
  "status": "CURRENT"
}
```

## SemanticDiff

```json
{
  "added_entities": [],
  "removed_entities": [],
  "changed_fields": [],
  "added_relations": [],
  "removed_relations": []
}
```

## ImpactReport

```json
{
  "unaffected": ["claim:1"],
  "source_changed": ["claim:2"],
  "recompute": ["claim:3"],
  "human_review": []
}
```

## ProofObligation

```json
{
  "claim": "claim:3",
  "reason": "Supporting OpenAIRE relation disappeared",
  "change_ref": "diff:...",
  "recommended_action": "RECOMPUTE",
  "resolution_class": "AUTOMATIC_RECOMPUTE",
  "status": "OPEN"
}
```

## Resolution classes

```
AUTOMATIC_RECOMPUTE  — agent can recompute
AGENT_RESEARCH       — agent needs new evidence
HUMAN_VALIDATION     — human judgment required
NO_ACTION            — not material enough
```

## Trust Receipt

```json
{
  "claim": "claim:17",
  "derived_from": {
    "provider": "OpenAIRE",
    "graph_version": "11.3.0",
    "query_digest": "...",
    "result_digest": "..."
  },
  "dependencies": ["openaire:...", "relation:..."],
  "last_verified": "...",
  "status": "CURRENT",
  "open_obligations": []
}
```

# OpenAIRE full-stack integration

## Principle

Use every OpenAIRE layer for the job it is already good at; add only the missing downstream continuity layer.

## 1. Graph API V3 — required data plane

**Status:** production, OpenAIRE's latest recommended Graph API.

Pāṭala uses V3 as the default for:

- `/v3/research-products`
- `/v3/organizations`
- `/v3/datasources`
- `/v3/projects`
- `/v3/persons`

The adapter supports search/filter parameters, paging and cursor-based multi-page collection. All source failures remain typed.

**Why V3 is core:** a hackathon submission should not depend on a beta contract when OpenAIRE explicitly recommends V3.

## 2. Graph API V4 — optional query/analytics plane

**Status:** beta.

The implementation supports V4 behind `--api v4`, including:

- unified `filter=field:value,...` syntax;
- sparse `select` fieldsets;
- facets;
- cursor pagination;
- optional `mailto` polite-pool parameter in the Python client.

**Why include it:** V4 is strategically useful for compact agent-generated queries and lower-bandwidth snapshotting. **Why not depend on it:** endpoints/parameters may still change.

## 3. ScholeXplorer V3 — semantic relation plane

**Status:** beta/future-primary ScholeXplorer version, recommended for new development.

Pāṭala can enrich each fetched research product through its persistent identifier and normalize Scholix relationships into:

```text
source PID
relation semantic
subtype
target PID
source/target type
publisher metadata
```

This is especially useful because a relation diff is semantically stronger than a generic changed field:

```text
Software S --Cites--> Dataset D
```

can become a direct `TrackedClaim` dependency.

## 4. Broker API — event/trigger plane

The Broker already emits enrichment notifications after Graph updates for subscribed content providers.

Pāṭala includes adapters for:

- listing subscriber subscriptions;
- scrolling notifications by subscription ID.

The hackathon demo does **not** require Broker credentials or a provider subscription. In a pilot, Broker notifications become a low-latency trigger:

```text
Broker notification
       ↓
identify affected OpenAIRE entities
       ↓
reverse lookup TrackedAnalyses using them
       ↓
verify only those analyses
```

This avoids polling the entire research universe.

## 5. Six-month Graph datasets / Beginner's Kit / BigQuery — historical and bulk plane

OpenAIRE explicitly separates frequent current access from periodic stable/citable dataset releases.

Pāṭala treats those releases as ideal baselines for:

- reproducible historical snapshots;
- backtesting change impact;
- large-scale institution/funder pilots;
- benchmark fixtures where “before” is immutable.

The reference implementation's `track_from_snapshot()` is the offline/historical import boundary. A production bulk adapter can map OpenAIRE dump rows to the same normalized entity/relation objects.

## 6. OpenAIRE relation provenance — preserved, not replaced

OpenAIRE relations already expose semantics, provenance/trust/validation in the Graph model. Pāṭala must never market itself as “adding provenance OpenAIRE lacks.”

Instead it adds **downstream dependency provenance**:

```text
OpenAIRE relation R exists with OpenAIRE provenance
                   │
                   ▼
my analysis used R to support claim C
                   │
                   ▼
R changes
                   │
                   ▼
C receives a proof obligation
```

## 7. IIS — upstream inference engine

IIS is a mature OpenAIRE subsystem that ingests the information space, runs modular processing/data-mining workflows, and feeds inferred data back into the Graph.

Research CI sits **after** this inference layer. It does not attempt to reimplement citation matching, project linking, dataset/software extraction, classification or affiliation resolution.

A particularly useful future integration is to preserve an OpenAIRE relation's inference/provenance metadata in the change object, allowing policies such as:

```text
harvested relation removed      → recompute
inferred low-confidence relation changed → recompute + inspect provenance
human-linked relation corrected → human review
```

## 8. API contract-test lineage

OpenAIRE's own `openaire-api-contract-tests` project records API snapshots before a backend change and replays the same queries afterward, using strict comparisons for single-record lookups and tolerant overlap/count comparisons for multi-result searches.

Pāṭala generalizes the **record/compare discipline**, not the purpose:

```text
OpenAIRE contract tests:
Did our API remain equivalent after infrastructure change?

Pāṭala Research CI:
Did the changed scholarly state affect any downstream conclusion?
```

## 9. Alien/OpenAIRE MCP — required AI discovery plane

The hackathon explicitly routes participants through the **official OpenAIRE MCP plugged into Alien's AI Gateway**. Research CI treats that MCP as the first-class AI discovery/control surface rather than reimplementing it.

Pāṭala adds a complementary evidence boundary:

```text
Alien/OpenAIRE MCP tool call
        ↓
credential-redacted MCPTrace + digest
        ↓
bind to TrackedAnalysis
        ↓
canonical Graph V3 snapshot
        ↓
later semantic diff / impact / proof obligation
```

The package also exposes an optional **Pāṭala MCP server** (`record_openaire_mcp_call`, `bind_mcp_trace`, `verify_analysis`, `list_proof_obligations`) so an AI client can use both MCP servers in one workflow. This is intentionally not a substitute for Alien's connector: Alien/OpenAIRE supplies scholarly discovery; Pāṭala supplies persistence, impact and re-verification.

`artifacts/alien_mcp_trace.example.json` is synthetic and exists only to test the trace format. A real participant-owned Alien call should be captured before final submission if credentials are available.

## 10. PROVIDE / repository correction — future feedback plane

Research CI's first direction is downstream: **Graph change → analysis impact**.

A later direction can be upstream:

```text
analysis discovers discrepancy
→ evidence packet
→ qualified human validation
→ structured correction proposal
→ existing OpenAIRE/provider curation path
```

This should integrate with existing PROVIDE/Broker/OpenOrgs workflows rather than introduce a parallel mutation channel.

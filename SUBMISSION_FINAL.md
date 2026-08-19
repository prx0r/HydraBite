# OpenAIRE AI Hackathon 2026 — Final Submission

> **Submission-ready text following the official template supplied for the hackathon.**
> Fields involving publication consent, video/Zenodo URLs, and a credentialed Alien session are explicitly marked where the submitter must perform the external action rather than being falsely asserted by the software artifact.

# 0. Submission details

| Field | Submission |
|---|---|
| **Submission title** | **Pāṭala Research CI — Continuous Verification for AI-Native Open Science** |
| **Theme** | **☑ B — Build** |
| **Applicant / team name** | Pāṭala Research CI / prx0r |
| **Type** | **☑ Individual** |
| **Country / base of operations** | Cambodia (current base; verify before submitting) |
| **Contact person** | Tom Prior |
| **Contact email** | tradesprior@gmail.com |

## Team members

| Name | Affiliation | Role in the submission | ORCID / GitHub |
|---|---|---|---|
| Tom Prior | Independent | Design, implementation, testing, submission | GitHub: `prx0r` |

# 1. The solution

## 1.1 Overall

OpenAIRE and Alien Intelligence now let AI agents query an authoritative, structured scholarly graph directly through Model Context Protocol (MCP). Alien goes further: it keeps sources updated automatically, provides execution history, audit trails, credential redaction, and content attribution. That solves the access problem comprehensively: an agent can discover publications, datasets, software, projects, organisations and people with full provenance.

**But a second problem remains.** An agent derives conclusion C1 at time T1. It persists in memory, a report, a policy analysis, a literature review. Alien keeps its sources current — but that does not automatically make C1 current. The derived artifact does not know that its supporting evidence changed.

```text
Alien keeps sources current
           │
           ▼
Agent at T1 ── derives ──► C1
                            │
                            │ persists
                            │
OpenAIRE changes at T2      │
           │                │
           └────── ??? ─────┘
```

**Pāṭala fills the ???**

**Pāṭala Research CI** is a dependency-aware continuous-verification layer for that downstream problem. The official OpenAIRE/Alien MCP is the AI discovery plane. Pāṭala captures a credential-redacted, content-digested trace of the MCP evidence used by an analysis, then creates a deterministic snapshot through the OpenAIRE Graph API. Research conclusions are registered as `TrackedClaim` objects with explicit dependencies on Graph entities, fields, typed relations or query membership.

On a later run, Pāṭala fetches the current Graph state, computes a semantic diff, and follows only explicit dependencies. Unrelated changes remain `CURRENT`; affected claims become `RECOMPUTE_REQUIRED` or `HUMAN_REVIEW_REQUIRED`. Instead of a generic alert, the system emits a machine-readable **ProofObligation** naming the exact upstream change and the check required to regain current status. Resolution criteria are frozen and hashed; successful automated checks produce verification receipts.

The first users are teams maintaining living evidence syntheses, bibliometric/research-intelligence analyses, and AI research agents with persistent research memory. The broader contribution is a reusable protocol for keeping derived research intelligence auditable as its authoritative sources evolve.

## 1.2 Quick SWOT

| | **Helpful to achieving the objective** | **Harmful to achieving the objective** |
|---|---|---|
| **Internal** | **Strengths**: deterministic core; explicit dependency impact; source-health safeguards; append-only provenance; proof obligations; MCP trace capture; offline reproducible demo; small Python codebase. | **Weaknesses**: dependencies are currently explicit rather than automatically extracted from prose; not every OpenAIRE relation has equal historical availability; no hosted UI is required for the core demo. |
| **External** | **Opportunities**: persistent AI research agents; living reviews; OpenAIRE/Alien agent workflows; Broker-triggered verification; MONITOR/research-intelligence pipelines; domain-specific evidence systems. | **Threats**: upstream API/schema changes; alert fatigue if dependencies are poorly modeled; users may confuse “source changed” with “claim false”; V4 is still beta. |

## 1.3 The story — use case

### The question

OpenAIRE already continuously improves its Graph through ingestion, deduplication, identifier resolution, inference and validation. Alien's OpenAIRE MCP makes that research intelligence directly usable by AI agents — with automatic updates, execution history, audit trails, and credential redaction. But an AI agent may save a literature analysis today and reuse it months later. Alien keeping its source current doesn't automatically make that already-derived artifact current. If a supporting record is corrected, a relation disappears, or new evidence enters the query set, the agent's stored conclusion does not automatically know that its evidence changed.

The project therefore asked a deliberately narrow question:

> **Can a conclusion derived from OpenAIRE carry enough machine-readable dependency information to know when it deserves to be checked again?**

This matters because the alternatives are poor: silently keep stale conclusions, or repeatedly rebuild every analysis from scratch. The desired behavior is incremental: identify only the conclusions whose supporting inputs materially changed, explain why, and state what would resolve the new uncertainty.

### The journey

The project began with five alternative builds: generic Graph versioning, a living-evidence updater, an AI-agent trust receipt, a Broker-driven resolution loop, and dependency-aware Research CI. Generic “Git for a knowledge graph” was rejected after reviewing OpenAIRE's own versioned releases/snapshots and existing graph-versioning systems. Generic AI peer review was also rejected because OpenReview and several 2026 agentic review systems already occupy that space.

The winning architecture emerged from combining four existing strengths rather than replacing them:

```text
Official OpenAIRE MCP / Alien
      AI discovery + structured evidence
                    │
                    ▼
          redacted MCP evidence trace
                    │
                    ▼
OpenAIRE Graph V3 ─ canonical snapshot ─ ScholeXplorer typed relations
                    │
                    ▼
              TrackedClaims
                    │
             Graph state changes
                    │
                    ▼
              SemanticDiff
                    │
                    ▼
           Dependency Impact
                    │
                    ▼
            ProofObligation
                    │
          frozen ResolutionPlan
                    │
                    ▼
          VerificationReceipt
```

OpenAIRE's stable V3 API is the deterministic replay plane; V4 is supported experimentally because it remains beta. ScholeXplorer enriches typed scholarly relationships. Broker is modeled as a future event trigger: Broker can say that enrichment changed, while Research CI decides whether a tracked analysis depended on it.

A critical engineering lesson was that a verification system must model **source health**. `SOURCE FAILURE ≠ ZERO RESULTS`, `PARTIAL RELATION SOURCE ≠ RELATION REMOVAL`, and `METADATA CHANGE ≠ CLAIM INVALIDATION`. Failed or partial refreshes therefore do not replace the last known-good baseline.

QDW-inspired frozen verification plans were then added so an obligation cannot be “resolved” merely because an agent says it has fixed the problem. It returns to current state only when a previously defined check produces verifiable evidence.

### The insight

The useful primitive is not a graph diff. It is **impact-aware continuity** — the missing bridge between Alien's always-current sources and the agent's already-derived conclusions:

```text
ALIEN
─────────────────────────────────────
What data did the agent access?
What tool ran?
What sources were returned?
What is OpenAIRE saying now?
Who accessed what?
Was access authorized?


PĀṬALA
─────────────────────────────────────
Which persistent conclusion used it?
What dependency did that evidence satisfy?
Has that dependency materially changed?
Does the conclusion actually need rechecking?
What exact verification would resolve it?
Has that verification subsequently passed?
```

```text
what changed?
    ↓
what depended on it?
    ↓
does that dependency require recomputation or judgment?
    ↓
what evidence would close that obligation?
```

The deterministic demonstration starts with four OpenAIRE-shaped research products and three claims. The second snapshot adds a product and removes a dataset relationship. The system correctly leaves unrelated claims untouched, recomputes claims that depend on query membership, and creates a targeted obligation for the relation-dependent claim. The release suite additionally attacks source timeouts, partial relation enrichment, ordering-only changes, cosmetic metadata differences, ledger tampering and receipt tampering.

This makes a distinction that global release notes cannot make. OpenAIRE can report that the Graph changed. Pāṭala can report: **“this exact analysis depended on this exact observation, so this exact conclusion needs attention.”**

### What others can reuse

Another participant or research team can reuse the artifact tomorrow without adopting Pāṭala as a platform. The reusable pieces are intentionally small:

- an OpenAIRE V3/V4 client with typed source-health semantics;
- a credential-redacting schema for preserving official OpenAIRE/Alien MCP tool-call evidence;
- canonical `TrackedAnalysis`, `TrackedClaim`, `SemanticDiff`, `ImpactReport`, `ProofObligation` and `VerificationReceipt` JSON structures;
- explicit entity/field/relation/query-membership dependency rules;
- an append-only tamper-detecting evidence ledger;
- a QDW-inspired frozen resolution-plan mechanism;
- deterministic before/after fixtures and adversarial tests;
- an RO-Crate-compatible portable export;
- a companion MCP server so another agent can ask Pāṭala to verify previously tracked analyses.

The OpenAIRE adapter is one sensor rather than a hard-coded worldview. The same protocol can later sit over Crossref, DataCite, PubMed, OpenAlex or domain repositories while preserving the same impact/obligation semantics.

# 2. Technical & scientific

## 2.1 How it works

```text
       AI CLIENT
          │
          ├──── Official OpenAIRE MCP / Alien ──── OpenAIRE Graph
          │                │
          │           MCP evidence trace
          │                │
          ▼                ▼
       PĀṬALA        canonical V3 snapshot
          │                │
          └───────┬────────┘
                  ▼
            TrackedAnalysis
                  │
             TrackedClaims
                  │
         later Graph refresh
                  │
                  ▼
             SemanticDiff
                  │
            explicit deps only
                  │
          ┌───────┴────────┐
          ▼                ▼
       CURRENT       RECHECK REQUIRED
                           │
                    ProofObligation
                           │
                   ResolutionPlan
                           │
                  VerificationReceipt
```

The OpenAIRE/Alien MCP is the required AI discovery surface. Pāṭala records a credential-redacted trace of those tool calls and hashes it. OpenAIRE Graph V3 independently retrieves the corresponding current records and creates a canonical snapshot. V4 is optional/beta; ScholeXplorer adds typed scholarly relations when available. Claims declare exactly which entities, fields, relations or query membership they depend on.

On verification, canonical snapshots are semantically compared. A source outage or partial enrichment is represented as source health, never as mass deletion. Only changes connected to a claim dependency enter the impact report. Affected claims emit proof obligations with frozen resolution plans. Automated computations can generate hashed evidence receipts; ambiguous/retraction-style changes remain explicitly human-review-required. Every state transition is appended to a hash-chained ledger.

## 2.2 OpenAIRE Graph elements used

| What you used | Details |
|---|---|
| **OpenAIRE Graph API** | Graph API **V3** is the deterministic default (`research-products`, `organizations`, `datasources`, `projects`, `persons`). V4 beta is an optional adapter for unified filters/facets. |
| **MCP tool powered by Alien Intelligence** | The official **OpenAIRE MCP through Alien** is the AI discovery plane. Pāṭala can ingest/record its tool name, arguments, returned structured result and OpenAIRE IDs as a credential-redacted content-digested trace, then bind that trace to a tracked analysis. **A real Alien/OpenAIRE trace is included** at `artifacts/alien_mcp_trace.live.json` (11 tool calls, 5 OpenAIRE IDs, synthetic:false). A synthetic example remains for offline testing. |
| **Entity types** | Research products are used in the deterministic demo; code supports publications/data/software/other research products plus projects, organisations, data sources and persons through V3. |
| **Fields / vocabularies** | Persistent OpenAIRE IDs/PIDs, product type, titles, publication date, authors/contributors, access-right metadata, and typed scholarly relations. Changes are classified as cosmetic, identity, metadata, relation, availability, correction/retraction, query membership or source health. |
| **Other data sources** | None required for the core demo. ScholeXplorer and Broker are OpenAIRE services. RO-Crate and in-toto informed interoperability/attestation design but are not research-data inputs. |
| **Approximate scale** | Deterministic demo: 4→5 OpenAIRE-shaped products plus typed relations and 3 claims. Live CLI default is intentionally bounded (e.g. 25–50 records/page) so the same method is cheap to reproduce; it is designed to scale by tracking only the evidence actually used by an analysis rather than downloading the full Graph. |

## 2.3 Documentation & reproducibility

The core release is deliberately reproducible **without network access**. Requirements are Python 3.10+; the core uses the standard library, with the official `mcp` package only for the optional companion MCP server.

```bash
unzip patala-research-ci-openaire-hackathon-FINAL.zip
cd patala-research-ci
python -m unittest discover -s tests -v
python -m patala_research_ci.cli --workspace /tmp/patala-demo demo
python scripts/verify_release.py
```

The repository contains fixed before/after OpenAIRE-shaped fixtures, explicit expected impact behavior, adversarial source-health tests, machine-readable JSON Schemas, `CITATION.cff`, CodeMeta/Zenodo metadata, an RO-Crate-compatible export, and a build certificate containing hashes of the verified artifact set. The ledger and verification receipts have independent tamper checks.

A live smoke test is separated from the deterministic certificate so an upstream network failure can never make local correctness appear false. `scripts/live_smoke.py` exercises the current OpenAIRE API when network access is available. `MCP_AGENT_WORKFLOW.md` explains how to capture one real official Alien/OpenAIRE MCP tool call, redact credentials, import it, and bind it to an analysis.

# 3. Innovation & risks

## What is new here

Research CI does not claim to invent knowledge-graph versioning, scholarly provenance, MCP, or AI literature review. Its contribution is their combination at the **derived-conclusion boundary**: preserve which OpenAIRE observations an AI/research analysis depended on; detect later material changes; compute the minimal downstream impact through explicit dependencies; and turn that impact into frozen, auditable proof obligations. The official MCP supplies trustworthy AI access; Pāṭala adds continuity after the answer has been stored.

## Limitations and known failure modes

Pāṭala is not a truth oracle. “Source changed” does not mean “claim false.” Dependencies must currently be registered explicitly or generated elsewhere and then checked. Automatic extraction of scientific claims from arbitrary PDFs is deliberately out of scope. Partial relation coverage can make semantic comparison uncertain, so the implementation blocks deletion claims when relation-source health is partial. V4 remains beta. Broker subscriptions depend on repository/user configuration. A real Alien/OpenAIRE trace is included at artifacts/alien_mcp_trace.live.json; a synthetic example remains for offline testing.

## Use of AI

The intended runtime AI workflow uses the **official OpenAIRE MCP through Alien Intelligence** for scholarly discovery and structured evidence access. OpenAI ChatGPT was used during development for architecture review, prior-art research, code generation/review, testing strategy, and drafting. AI output is never allowed to promote a research claim to authoritative truth: the core diff/impact logic is deterministic, and unresolved judgments remain explicitly human-review-required.

## Data protection & third-party content

The artifact processes public scholarly metadata needed for reproducibility; it does not require private correspondence, sensitive personal data or paywalled full text. MCP traces redact common credential/token fields before storage. OpenAIRE metadata is attributed to **OpenAIRE Graph** and retained/reused under its CC BY terms. Original code is MIT; written submission material is CC BY 4.0; synthetic fixtures are CC0. No third-party code is copied into the core implementation.

# 4. Links & artifacts

| Item | Link | Status | Notes |
|---|---|---|---|
| **Code repository** | `https://github.com/prx0r/hackathon1` | ☑ Public | Public commit history. Final hardened files should be pushed before submission. |
| **Live demo / deployed app** | Not required; deterministic local demo in repository | — | `python -m patala_research_ci.cli --workspace /tmp/patala-demo demo` |
| **Video walkthrough (max 3 min)** | **[external action: upload and paste URL]** | ☐ | A ~2-minute script is included as `VIDEO_SCRIPT.md`. |
| **Main artifact** | `https://github.com/prx0r/hackathon1` | ☑ Public | Source + fixtures + tests + build certificate. |
| **Documentation / README** | `https://github.com/prx0r/hackathon1#readme` | ☑ Public | Judge-first quick start and design. |
| **Write-up from section 1.3** | `https://github.com/prx0r/hackathon1/blob/master/SUBMISSION_FINAL.md` | ☑ Public after push | This file. |
| **Archived version with DOI** | **[optional external action: Zenodo release/DOI]** | ☐ | `.zenodo.json` and `CITATION.cff` are included. |
| **Other** | `MCP_AGENT_WORKFLOW.md`, `SCORING_MATRIX.md`, `DATA_AND_RIGHTS.md`, `FAIR.md` | ☑ Public after push | Evidence for MCP, rubric mapping, rights and FAIRness. |

## Repository checklist

- ☑ README explains what it is and how to run it
- ☑ LICENSE file present
- ☑ Dependencies listed (`pyproject.toml`)
- ☑ Commit history visible
- ☑ No credentials/API keys/personal data committed by the artifact

# 5. Openness & licensing

| Item | Submission |
|---|---|
| **Licence for written materials, documentation and media** | **CC BY 4.0 — ☑ applied to the artifact** |
| **Licence for code** | **MIT** |
| **Licence for data / outputs produced** | Synthetic fixtures: **CC0 1.0**. OpenAIRE-derived metadata/output: **CC BY / source terms with OpenAIRE attribution**. |
| **The submission may be published on OpenAIRE channels** | **☐ submitter must confirm this consent in the form** |
| **The submission may be included in community voting (21–29 Aug 2026)** | **☐ submitter must confirm this consent in the form** |
| **I have the right to submit all included material** | **☐ submitter must personally confirm** |

# 6. Feedback (optional)

The Graph API/documentation made it possible to separate current-state access from reproducible downstream verification cleanly. The main gap encountered for agentic reproducibility is **portable evidence of MCP use**: an agent can receive excellent structured OpenAIRE results through Alien, but a downstream artifact also benefits from a standard export containing tool name/schema version, redacted arguments, returned OpenAIRE identifiers, source timestamp and a digest. A first-class “export this MCP research trace” feature would make hackathon artifacts easier to reproduce without exposing credentials.

A second useful distinction is explicit source completeness/health for relation enrichment. Verification systems need to tell “relation absent from a complete current view” from “relation source unavailable/partial”; otherwise an outage can be misinterpreted as a scientific change.

Finally, V3 being clearly identified as stable/recommended while V4 remains beta is helpful. Stable version identifiers/tool schemas exposed through the MCP response would make long-lived agent memories even easier to verify later.

# 7. Before you submit — final check

- ☑ Theme selected: B — Build
- ☑ Story written for non-specialists
- ☐ Open every Section 4 public link in a private browser after the final GitHub push
- ☐ Capture/import **one real Alien/OpenAIRE MCP call** and commit the credential-redacted trace (strongly recommended; synthetic example is not represented as live evidence)
- ☐ Record/upload video if submitting one; keep under 3 minutes and verify audio
- ☑ CC BY 4.0 stated for written materials
- ☐ Personally confirm publication/community-voting/right-to-submit consent boxes
- ☑ Contact email populated; verify it is monitored through September 2026
- ☐ Submit before **20 August 2026, 23:59 CET**

## Key dates

| Event | Date |
|---|---|
| Submissions close | 20 August 2026, 23:59 CET |
| Community voting | 21–29 August 2026 |
| Evaluation/finalist announcement | 20 August–5 September 2026 |
| Awards ceremony / Graph Community Call | 16 September 2026 |

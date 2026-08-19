# Dossier 5: Contribution Ledger

**Status:** Strategic longer-term
**Score:** 7.2/10
**Category:** Track diverse scholarly contributions as first-class events

---

## TL;DR

Every scholarly contribution — not just publications — becomes a recorded event with role, activity, evidence, and provenance. Integrates with MyResearchFolio for research assessment.

---

## The Problem

MyResearchFolio is moving beyond publication metrics toward diverse contribution profiles. But there's no standardized event format for:
- Data curation
- Validation
- Adjudication
- Transcription
- Entity resolution
- Counterexamples

---

## The Product

```yaml
ScholarlyContributionEvent:
  contributor:
    orcid: "0000-0002-3789-9238"
    name: "E. Richard Gold"
  role: ADJUDICATOR
  object:
    type: CLAIM
    id: "claim:17"
  activity: EXPERT_ADJUDICATION
  evidence:
    - "checked manuscript reading against 3 witnesses"
    - "confirmed institutional affiliation via ROR"
  decision: "reading X confirmed over reading Y"
  timestamp: "2026-08-19T10:30:00Z"
  provenance:
    protocol: "patala-scholar-relay"
    version: "1.0"
  citation:
    doi: "..."
    format: "APA"
```

---

## Reusable

- MyResearchFolio API (researcher profiles)
- Scholar attestation from fuck-off/lib
- Event ledger from events.py
- ORCID integration from OpenAIRE adapters

## New code needed (~100 lines)

Event schema + MyResearchFolio adapter.

---

## Why this is fifth

Strategic killer but needs MyResearchFolio to mature first. Good as "future extension" mention. The CRediT-style taxonomy is the right direction but too early for a hackathon.

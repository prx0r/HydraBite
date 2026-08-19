# Dossier 4: Broker Agent

**Status:** Most immediately useful, least distinctive
**Score:** 7.5/10
**Category:** Evidence-backed enrichment proposals from OpenAIRE Broker events

---

## TL;DR

When OpenAIRE Broker notifies a repository of an enrichment (missing ORCID, project link, etc.), the Broker Agent generates an evidence bundle with confidence score before proposing the change. Never silently mutate — produce a PR-like review.

---

## The Problem

OpenAIRE Broker emits events like "Add ORCID X to author Y" but repositories must trust the suggestion blindly. No evidence, no confidence, no cross-validation.

---

## The Product

```
BROKER EVENT
  "Add ORCID 0000-0002-3789-9238 to author E. Richard Gold"

        ↓

PROOF AGENT

  checks:
    - ORCID registry: confirms profile exists
    - Crossref: confirms same name on publications
    - OpenAlex: confirms affiliation match
    - ROR: confirms institution exists
    - Co-author network: confirms collaborations

        ↓

EVIDENCE BUNDLE

  support: [OpenAIRE, ORCID, Crossref, OpenAlex]
  contradictions: []
  confidence: 0.97
  decision: PROPOSE_ACCEPT
  evidence_digest: sha256:...
```

---

## Reusable

- OpenAIRE Broker API (subscription + notification feed)
- VerificationService from qdw/qdw/proof/
- Content hashing from hashing.py

## New code needed (~200 lines)

Broker client + evidence gatherer + confidence scorer.

---

## Why this is fourth

Most immediately useful — repositories actually need this. But it's not distinctive enough for a hackathon win. The evidence bundle idea is good but overlaps with existing enrichment confidence.

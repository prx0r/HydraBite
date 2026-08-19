# Dossier 3: Scholar Relay

**Status:** Stretch feature for Research CI
**Score:** 7.8/10
**Category:** Route proof obligations to qualified humans via OpenAIRE Person graph

---

## TL;DR

When a proof obligation requires human judgment, Scholar Relay uses OpenAIRE's Person/Organization graph to find qualified researchers, then routes the question with evidence packet.

---

## The Problem

Automated verification can handle many re-checks, but some require genuine human expertise:
- Conflicting manuscript readings
- Interpretive disagreements
- Contextual judgment calls

Nobody currently routes "this scholarly question needs a human" to the right human using the scholarly graph.

---

## The Product

```
PROOF OBLIGATION
  requires: expert_judgment
  topic: "Sanskrit manuscript reading"
  domain: "Kashmir Shaivism"

        ↓

OpenAIRE Person Graph
  query: researchers affiliated with institutions
         that have published on this topic

        ↓

CANDIDATE EXPERTS
  ranked by:
    - publication count in domain
    - recency
    - institutional affiliation
    - ORCID presence

        ↓

EVIDENCE PACKET
  passages, witnesses, bibliography,
  competing readings, model arguments

        ↓

HUMAN ADJUDICATION
  decision recorded as signed event
```

---

## Reusable

- OpenAIRE Person API (V3 `/v1/persons`)
- Crux engine from fuck-off/lib
- Event ledger from events.py
- Scholar attestation model from patalacheckpoints

## New code needed (~150 lines)

Person query adapter + evidence packet builder + routing logic.

---

## Why this is third

Beautiful consequence of Research CI, but not the headline. Show as "future extension" in one slide. The OpenAIRE Person graph integration is the novel part — using the scholarly network as part of an AI workflow.

# DOSSIERS INDEX — Top 10 Ideas

*2026-08-19 · Ranked by hackathon fit · Each with honest challenge review*

---

## Final Rankings

| # | Idea | Score | Threat | Status | Challenge |
|---|------|-------|--------|--------|-----------|
| **1** | **[Pāṭala Research CI](01-research-ci.md)** | **9.2** | LOW | **BUILD THIS** | [Challenge](CHALLENGE-01-research-ci.md) |
| **2** | **[Pāṭala Crux](02-crux.md)** | **8.6** | MEDIUM | Stretch feature | [Challenge](CHALLENGE-02-crux.md) |
| 3 | [Scholar Relay](03-scholar-relay.md) | 7.8 | MED-HIGH | Future extension | [Challenge](CHALLENGE-03-scholar-relay.md) |
| 4 | [Broker Agent](04-broker-agent.md) | 7.5 | LOW-MED | Not for this hackathon | [Challenge](CHALLENGE-04-broker-agent.md) |
| 5 | [Contribution Ledger](05-contribution-ledger.md) | 7.2 | VERY LOW | Future vision | [Challenge](CHALLENGE-05-contribution-ledger.md) |
| 6 | [Counterfactual Engine](06-counterfactual.md) | 7.0 | MEDIUM | Future vision | [Challenge](CHALLENGE-06-counterfactual.md) |
| 7 | [Verified-Statement Marketplace](07-verified-marketplace.md) | 6.8 | LOW-MED | Long-term | [Challenge](CHALLENGE-07-verified-marketplace.md) |
| 8 | [OpenScience CI](08-open-science-ci.md) | 6.5 | VERY LOW | Not for this hackathon | [Challenge](CHALLENGE-08-open-science-ci.md) |
| 9 | [Manuscript Reality Bridge](09-manuscript-bridge.md) | 6.2 | LOW-MED | Future extension | [Challenge](CHALLENGE-09-manuscript-bridge.md) |
| 10 | [Adaptive Knowledge Graph](10-adaptive-kg.md) | 6.0 | MED-HIGH | Reference only | [Challenge](CHALLENGE-10-adaptive-kg.md) |

---

## What to Build Tomorrow

**ONE product: Pāṭala Research CI**

```
TRACK → SNAPSHOT → DETECT → IMPACT → OBLIGE
```

**ONE stretch feature: Pāṭala Crux** (if time permits)

**ONE slide: Future vision** (Scholar Relay + Manuscript Bridge + Contribution Ledger)

---

## What NOT to Build

- ❌ AI peer reviewer (crowded — CMU, Peerispect, ReviewGrounder, DeepReviewer)
- ❌ Generic KG versioning (TerminusDB, RDF Delta exist)
- ❌ Generic OpenAIRE MCP/RAG (Alien already did it)
- ❌ Research dashboards (MONITOR exists)
- ❌ Organisation dedup (AffRo + OpenOrgs exist)
- ❌ Adaptive KG tutoring (DeepTutor, pykt-toolkit exist)

---

## The Hackathon Story

> OpenAIRE makes open scholarly intelligence queryable by agents.
> Pāṭala Research CI makes conclusions derived from that intelligence continuously verifiable.

> CI/CD assumes software changes. Research infrastructure should assume knowledge changes too.

---

## Existing Code to Reuse

| Component | Source | Lines |
|-----------|--------|-------|
| JCS canonicalization + hashing | `openpatalaproject/patala/hashing.py` | reuse |
| Event ledger + Merkle checkpoints | `openpatalaproject/patala/events.py` | reuse |
| Blast-radius + staleness | `fuck-off/lib/staleness.py` | reuse |
| Crux / perturbation | `fuck-off/lib/epistemic.py` | reuse |
| Content-addressed runs | `sanskritbenchy/pipeline/run_recorder.py` | reuse |
| OpenAIRE V3 client | `hackathon1/explore_api.py` | adapt |

**New code needed: ~300-400 lines total**

---

## Deadline

**August 20, 2026 (23:59 CET)** — tomorrow.

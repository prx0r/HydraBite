# Dossier 6: Counterfactual Engine

**Status:** Vision B from fuck-off, most intellectually ambitious
**Score:** 7.0/10
**Category:** "What if this assumption were false?" — whole-graph counterfactual analysis

---

## TL;DR

Given a knowledge graph, identify which assumptions are most load-bearing across the entire graph. If THERMODYNAMICS were false, 11 downstream claims collapse. The Counterfactual Engine computes this systematically.

---

## The Problem

Researchers know some claims depend on others but don't know:
- Which assumptions are most load-bearing globally
- How many downstream claims collapse if an assumption is false
- Where the graph is most fragile

---

## The Product

```bash
patala counterfactual --graph openaire-subset

# Output:
# LOAD-BEARING ANALYSIS
#
# THERMODYNAMICS
#   downstream_claims: 11
#   fragility_score: 0.89
#   independent_routes: 2
#   VERDICT: HIGH LOAD-BEARING
#
# PHYSICS
#   downstream_claims: 47
#   fragility_score: 0.31
#   independent_routes: 12
#   VERDICT: LOW LOAD-BEARING (many independent routes)
#
# MOST FRAGILE CLAIMS
#   claim:42 — depends on 1 route only
#   claim:17 — depends on 2 routes, both from same source
```

### ResearchValue formula

```
ResearchValue(claim) = load_bearing × (1 − verifier_strength) × crux_pressure
```

---

## Reusable

- Staleness/blast-radius from fuck-off/lib/staleness.py (dependency walking)
- Epistemic envelope from fuck-off/lib/epistemic.py
- MAP-Elites from fuck-off/lib/evolve.py (evolutionary search over counterfactual space)

## New code needed (~200 lines)

Counterfactual scanner + load-bearing computation + visualization.

---

## Why this is sixth

Most intellectually ambitious. The "THERMODYNAMICS vs PHYSICS" finding from the fuck-off repo is genuinely cool. But it's harder to demo with OpenAIRE data specifically — works better on a curated epistemic graph.

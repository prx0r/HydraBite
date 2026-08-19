# Challenge: Counterfactual Engine

## The hard truth

**"THERMODYNAMICS was found to be more load-bearing than PHYSICS — 11 downstream claims collapse if false."** That's a cool finding from the fuck-off repo. But it was computed over a curated epistemic graph of ~50 claims, not a 386M-record scholarly graph.

Scaling counterfactual analysis to a real knowledge graph is a **fundamentally different problem.** You can't遍历 all possible premise removals on millions of claims.

## The real question

Is this a research tool (compute counterfactuals over a small, curated argument graph) or a product (automated load-bearing analysis over OpenAIRE)?

If research tool: intellectually interesting, small audience.
If product: the scaling problem kills you.

## Competitors

| Repo | Stars | What it does | Threat |
|------|-------|-------------|--------|
| [counterfactual_KGR](https://github.com/LenaZellinger/counterfactual_KGR) | 5 | Counterfactual reasoning with KGs | MEDIUM — but QA-focused |
| [CoCES](https://github.com/plvorg/CoCES) | 0 | Counterfactual evidence subgraph | LOW — drug repurposing |
| Do-calculus libraries | — | Causal inference | REFERENCE — theoretical foundation |
| CausalNex (McKinsey) | — | Causal reasoning toolkit | ADJACENT — different domain |

## Reusable from competitors

- counterfactual_KGR's evaluation methodology
- CoCES's evidence subgraph approach
- CausalNex/DoWhy for causal inference foundations

## Verdict

**Intellectually the most ambitious.** The "load-bearing analysis" framing is unique. But the scaling problem is real — this works over curated small graphs, not 386M records. Position as: "Experimental layer for curated evidence graphs. Extends Research CI's change detection to hypothetical scenarios."

Better as a "future vision" slide than a demo.
